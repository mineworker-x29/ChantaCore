from __future__ import annotations

import json
import shutil
import sqlite3
from pathlib import Path
from typing import Any

from chanta_core.ocel.models import OCELRecord, OCELRelation
from chanta_core.ocel.schema import (
    DDL_STATEMENTS,
    QUERY_INDEX_STATEMENTS,
    UNIQUE_INDEX_STATEMENTS,
)
from chanta_core.utility.time import utc_now_iso


def _json_dumps(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _json_loads(raw_value: str | None) -> dict[str, Any]:
    if not raw_value:
        return {}
    loaded = json.loads(raw_value)
    if isinstance(loaded, dict):
        return loaded
    return {"value": loaded}


class OCELStore:
    def __init__(
        self,
        db_path: str | Path = "data/ocel/chanta_core_ocel.sqlite",
    ) -> None:
        self.db_path = Path(db_path)

    def initialize(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as connection:
            for statement in DDL_STATEMENTS:
                connection.execute(statement)
            self._ensure_development_schema_compatibility(connection)
            for statement in UNIQUE_INDEX_STATEMENTS:
                try:
                    connection.execute(statement)
                except sqlite3.IntegrityError:
                    # Existing development stores may contain pre-v0.3.1 duplicates.
                    # Validation reports them; new inserts are guarded below.
                    continue
            for statement in QUERY_INDEX_STATEMENTS:
                connection.execute(statement)
            connection.commit()

    def append_record(
        self,
        record: OCELRecord,
        raw_event: dict[str, Any] | None = None,
    ) -> None:
        self.initialize()
        with sqlite3.connect(self.db_path) as connection:
            event = record.event
            connection.execute(
                "INSERT OR IGNORE INTO event(ocel_id, ocel_type) VALUES(?, ?)",
                (event.event_id, event.event_activity),
            )
            self._upsert_event_payload(connection, record)

            for item in record.objects:
                connection.execute(
                    "INSERT OR REPLACE INTO object(ocel_id, ocel_type) VALUES(?, ?)",
                    (item.object_id, item.object_type),
                )
                self._upsert_object_state(connection, item.object_id, item.object_type, item.object_attrs)

            for relation in record.relations:
                if relation.relation_kind == "event_object":
                    self._insert_event_object_relation(connection, relation)
                elif relation.relation_kind == "object_object":
                    self._insert_object_object_relation(connection, relation)
                else:
                    raise ValueError(f"Unknown OCEL relation kind: {relation.relation_kind}")

            if raw_event is not None:
                connection.execute(
                    """
                    INSERT INTO chanta_raw_event_mirror(
                        event_id,
                        raw_json,
                        created_at
                    )
                    VALUES(?, ?, ?)
                    """,
                    (
                        event.event_id,
                        _json_dumps(raw_event),
                        utc_now_iso(),
                    ),
                )

            connection.commit()

    def append_records(self, records: list[OCELRecord]) -> None:
        for record in records:
            self.append_record(record)

    def fetch_event_count(self) -> int:
        return self._fetch_count("event")

    def fetch_object_count(self) -> int:
        return self._fetch_count("object")

    def fetch_event_object_relation_count(self) -> int:
        return self._fetch_count("event_object")

    def fetch_object_object_relation_count(self) -> int:
        return self._fetch_count("object_object")

    def fetch_recent_events(self, limit: int = 20) -> list[dict[str, Any]]:
        self.initialize()
        with sqlite3.connect(self.db_path) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                """
                SELECT
                    event.ocel_id AS event_id,
                    event.ocel_type AS event_activity,
                    payload.event_timestamp,
                    payload.event_attrs_json
                FROM event
                JOIN chanta_event_payload AS payload
                    ON payload.event_id = event.ocel_id
                ORDER BY payload.event_timestamp DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [self._event_row_to_dict(row) for row in rows]

    def fetch_events_by_session(self, session_id: str) -> list[dict[str, Any]]:
        self.initialize()
        session_object_id = f"session:{session_id}"
        with sqlite3.connect(self.db_path) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                """
                SELECT DISTINCT
                    event.ocel_id AS event_id,
                    event.ocel_type AS event_activity,
                    payload.event_timestamp,
                    payload.event_attrs_json
                FROM event
                JOIN chanta_event_payload AS payload
                    ON payload.event_id = event.ocel_id
                JOIN event_object
                    ON event_object.ocel_event_id = event.ocel_id
                WHERE event_object.ocel_object_id = ?
                    AND event_object.ocel_qualifier = 'session_context'
                ORDER BY payload.event_timestamp ASC
                """,
                (session_object_id,),
            ).fetchall()
        return [self._event_row_to_dict(row) for row in rows]

    def fetch_objects_by_type(self, object_type: str) -> list[dict[str, Any]]:
        self.initialize()
        with sqlite3.connect(self.db_path) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                """
                SELECT
                    object_id,
                    object_type,
                    object_attrs_json
                FROM chanta_object_state
                WHERE object_type = ?
                ORDER BY object_id ASC
                """,
                (object_type,),
            ).fetchall()
        return [self._object_row_to_dict(row) for row in rows]

    def fetch_related_objects_for_event(
        self,
        event_id: str,
    ) -> list[dict[str, Any]]:
        self.initialize()
        with sqlite3.connect(self.db_path) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                """
                SELECT
                    object_state.object_id,
                    object_state.object_type,
                    object_state.object_attrs_json,
                    relation.qualifier,
                    relation.relation_attrs_json
                FROM chanta_event_object_relation_ext AS relation
                JOIN chanta_object_state AS object_state
                    ON object_state.object_id = relation.object_id
                WHERE relation.event_id = ?
                ORDER BY relation.qualifier ASC, relation.object_id ASC
                """,
                (event_id,),
            ).fetchall()
        return [self._related_object_row_to_dict(row) for row in rows]

    def copy_database_to(self, target_path: str | Path) -> Path:
        self.initialize()
        target = Path(target_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(self.db_path, target)
        return target

    def _upsert_event_payload(
        self,
        connection: sqlite3.Connection,
        record: OCELRecord,
    ) -> None:
        columns = self._table_columns(connection, "chanta_event_payload")
        event = record.event
        event_attrs = dict(event.event_attrs)
        values: dict[str, Any] = {
            "event_id": event.event_id,
            "event_activity": event.event_activity,
            "event_timestamp": event.event_timestamp,
            "event_attrs_json": _json_dumps(event_attrs),
        }
        # Compatibility writes for pre-v0.3.2 development DBs.
        if "timestamp" in columns:
            values["timestamp"] = event.event_timestamp
        if "activity" in columns:
            values["activity"] = event.event_activity
        if "source_runtime" in columns:
            values["source_runtime"] = str(event_attrs.get("source_runtime") or "chanta_core")
        if "session_id" in columns:
            values["session_id"] = event_attrs.get("session_id")
        if "trace_id" in columns:
            values["trace_id"] = event_attrs.get("trace_id")
        if "actor_type" in columns:
            values["actor_type"] = event_attrs.get("actor_type")
        if "actor_id" in columns:
            values["actor_id"] = event_attrs.get("actor_id")
        if "status" in columns:
            values["status"] = event_attrs.get("lifecycle")
        if "attributes_json" in columns:
            values["attributes_json"] = _json_dumps(event_attrs)

        self._insert_or_replace(connection, "chanta_event_payload", values)

    def _upsert_object_state(
        self,
        connection: sqlite3.Connection,
        object_id: str,
        object_type: str,
        object_attrs: dict[str, Any],
    ) -> None:
        columns = self._table_columns(connection, "chanta_object_state")
        values: dict[str, Any] = {
            "object_id": object_id,
            "object_type": object_type,
            "object_attrs_json": _json_dumps(object_attrs),
        }
        # Compatibility writes for pre-v0.3.2 development DBs.
        if "object_key" in columns:
            values["object_key"] = str(object_attrs.get("object_key") or object_id)
        if "display_name" in columns:
            values["display_name"] = object_attrs.get("display_name")
        if "state_json" in columns:
            values["state_json"] = _json_dumps(object_attrs)
        if "created_at" in columns:
            values["created_at"] = object_attrs.get("created_at") or utc_now_iso()
        if "updated_at" in columns:
            values["updated_at"] = object_attrs.get("updated_at") or utc_now_iso()

        self._insert_or_replace(connection, "chanta_object_state", values)

    def _insert_event_object_relation(
        self,
        connection: sqlite3.Connection,
        relation: OCELRelation,
    ) -> None:
        connection.execute(
            """
            INSERT OR IGNORE INTO event_object(
                ocel_event_id,
                ocel_object_id,
                ocel_qualifier
            )
            SELECT ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1
                FROM event_object
                WHERE ocel_event_id = ?
                    AND ocel_object_id = ?
                    AND ocel_qualifier = ?
            )
            """,
            (
                relation.source_id,
                relation.target_id,
                relation.qualifier,
                relation.source_id,
                relation.target_id,
                relation.qualifier,
            ),
        )
        values = {
            "event_id": relation.source_id,
            "object_id": relation.target_id,
            "qualifier": relation.qualifier,
            "relation_attrs_json": _json_dumps(relation.relation_attrs),
        }
        columns = self._table_columns(connection, "chanta_event_object_relation_ext")
        if "relation_order" in columns:
            values["relation_order"] = int(relation.relation_attrs.get("relation_order", 0))
        if "attributes_json" in columns:
            values["attributes_json"] = _json_dumps(relation.relation_attrs)
        self._insert_relation_if_absent(
            connection=connection,
            table_name="chanta_event_object_relation_ext",
            values=values,
            key_columns=["event_id", "object_id", "qualifier"],
        )

    def _insert_object_object_relation(
        self,
        connection: sqlite3.Connection,
        relation: OCELRelation,
    ) -> None:
        connection.execute(
            """
            INSERT OR IGNORE INTO object_object(
                ocel_source_id,
                ocel_target_id,
                ocel_qualifier
            )
            SELECT ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1
                FROM object_object
                WHERE ocel_source_id = ?
                    AND ocel_target_id = ?
                    AND ocel_qualifier = ?
            )
            """,
            (
                relation.source_id,
                relation.target_id,
                relation.qualifier,
                relation.source_id,
                relation.target_id,
                relation.qualifier,
            ),
        )
        values = {
            "source_object_id": relation.source_id,
            "target_object_id": relation.target_id,
            "qualifier": relation.qualifier,
            "relation_attrs_json": _json_dumps(relation.relation_attrs),
        }
        columns = self._table_columns(connection, "chanta_object_object_relation_ext")
        if "relation_order" in columns:
            values["relation_order"] = int(relation.relation_attrs.get("relation_order", 0))
        if "attributes_json" in columns:
            values["attributes_json"] = _json_dumps(relation.relation_attrs)
        self._insert_relation_if_absent(
            connection=connection,
            table_name="chanta_object_object_relation_ext",
            values=values,
            key_columns=["source_object_id", "target_object_id", "qualifier"],
        )

    def _fetch_count(self, table_name: str) -> int:
        self.initialize()
        with sqlite3.connect(self.db_path) as connection:
            row = connection.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()
        return int(row[0])

    @staticmethod
    def _event_row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
        event_attrs = _json_loads(row["event_attrs_json"])
        event_activity = row["event_activity"]
        event_timestamp = row["event_timestamp"]
        return {
            "event_id": row["event_id"],
            "event_activity": event_activity,
            "event_timestamp": event_timestamp,
            "event_attrs": event_attrs,
            # Compatibility keys for scripts and older lightweight consumers.
            "event_type": event_activity,
            "activity": event_activity,
            "timestamp": event_timestamp,
            "attributes": event_attrs,
        }

    @staticmethod
    def _object_row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
        object_attrs = _json_loads(row["object_attrs_json"])
        object_key = object_attrs.get("object_key") or row["object_id"]
        return {
            "object_id": row["object_id"],
            "object_type": row["object_type"],
            "object_attrs": object_attrs,
            # Compatibility keys for current OCPX/PIG scripts.
            "object_key": object_key,
            "display_name": object_attrs.get("display_name"),
            "state": object_attrs,
        }

    @staticmethod
    def _related_object_row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
        item = OCELStore._object_row_to_dict(row)
        item["qualifier"] = row["qualifier"]
        item["relation_attrs"] = _json_loads(row["relation_attrs_json"])
        item["relation_attributes"] = item["relation_attrs"]
        return item

    @staticmethod
    def _insert_or_replace(
        connection: sqlite3.Connection,
        table_name: str,
        values: dict[str, Any],
    ) -> None:
        columns = list(values)
        placeholders = ", ".join("?" for _ in columns)
        column_sql = ", ".join(columns)
        connection.execute(
            f"INSERT OR REPLACE INTO {table_name}({column_sql}) VALUES({placeholders})",
            [values[column] for column in columns],
        )

    @staticmethod
    def _insert_relation_if_absent(
        *,
        connection: sqlite3.Connection,
        table_name: str,
        values: dict[str, Any],
        key_columns: list[str],
    ) -> None:
        columns = list(values)
        column_sql = ", ".join(columns)
        placeholders = ", ".join("?" for _ in columns)
        where_sql = " AND ".join(f"{column} = ?" for column in key_columns)
        connection.execute(
            f"""
            INSERT OR IGNORE INTO {table_name}({column_sql})
            SELECT {placeholders}
            WHERE NOT EXISTS (
                SELECT 1 FROM {table_name}
                WHERE {where_sql}
            )
            """,
            [values[column] for column in columns]
            + [values[column] for column in key_columns],
        )

    @staticmethod
    def _table_columns(
        connection: sqlite3.Connection,
        table_name: str,
    ) -> set[str]:
        rows = connection.execute(f"PRAGMA table_info({table_name})").fetchall()
        return {str(row[1]) for row in rows}

    @classmethod
    def _ensure_development_schema_compatibility(
        cls,
        connection: sqlite3.Connection,
    ) -> None:
        cls._add_column_if_missing(
            connection,
            "chanta_event_payload",
            "event_activity",
            "TEXT",
        )
        cls._add_column_if_missing(
            connection,
            "chanta_event_payload",
            "event_timestamp",
            "TEXT",
        )
        cls._add_column_if_missing(
            connection,
            "chanta_event_payload",
            "event_attrs_json",
            "TEXT",
        )
        cls._add_column_if_missing(
            connection,
            "chanta_object_state",
            "object_attrs_json",
            "TEXT",
        )
        cls._add_column_if_missing(
            connection,
            "chanta_event_object_relation_ext",
            "relation_attrs_json",
            "TEXT",
        )
        cls._add_column_if_missing(
            connection,
            "chanta_object_object_relation_ext",
            "relation_attrs_json",
            "TEXT",
        )

    @classmethod
    def _add_column_if_missing(
        cls,
        connection: sqlite3.Connection,
        table_name: str,
        column_name: str,
        column_type: str,
    ) -> None:
        columns = cls._table_columns(connection, table_name)
        if column_name not in columns:
            connection.execute(
                f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
            )
