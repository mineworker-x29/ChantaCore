from __future__ import annotations

import json
import sqlite3
from typing import Any

from chanta_core.ocel.schema import REQUIRED_INDEXES, REQUIRED_TABLES
from chanta_core.ocel.store import OCELStore


class OCELValidator:
    def __init__(self, store: OCELStore | None = None) -> None:
        self.store = store or OCELStore()

    def validate_structure(self) -> dict[str, Any]:
        self.store.initialize()
        with sqlite3.connect(self.store.db_path) as connection:
            rows = connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
            index_rows = connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'index'"
            ).fetchall()
        existing_tables = {str(row[0]) for row in rows}
        existing_indexes = {str(row[0]) for row in index_rows}
        missing_tables = sorted(REQUIRED_TABLES - existing_tables)
        missing_indexes = sorted(REQUIRED_INDEXES - existing_indexes)
        return {
            "valid": not missing_tables,
            "required_tables_exist": not missing_tables,
            "missing_tables": missing_tables,
            "table_count": len(existing_tables),
            "missing_indexes": missing_indexes,
            "index_count": len(existing_indexes),
        }

    def validate_minimum_counts(self) -> dict[str, Any]:
        event_count = self.store.fetch_event_count()
        object_count = self.store.fetch_object_count()
        event_object_relation_count = self.store.fetch_event_object_relation_count()
        object_object_relation_count = self.store.fetch_object_object_relation_count()
        events_without_event_object_relation = (
            self._fetch_events_without_event_object_relation_count()
        )
        return {
            "valid": event_count > 0
            and object_count > 0
            and event_object_relation_count > 0,
            "event_count": event_count,
            "object_count": object_count,
            "event_object_relation_count": event_object_relation_count,
            "object_object_relation_count": object_object_relation_count,
            "events_without_event_object_relation": (
                events_without_event_object_relation
            ),
            "duplicate_relations": self.validate_duplicate_relations(),
        }

    def validate_session_trace(self, session_id: str) -> dict[str, Any]:
        events = self.store.fetch_events_by_session(session_id)
        return {
            "valid": len(events) > 0,
            "session_id": session_id,
            "session_events_count": len(events),
            "event_activities": [event["event_activity"] for event in events],
        }

    def validate_duplicate_relations(self) -> dict[str, Any]:
        self.store.initialize()
        details = {
            "event_object": self._fetch_duplicate_relation_groups(
                table_name="event_object",
                key_columns=[
                    "ocel_event_id",
                    "ocel_object_id",
                    "ocel_qualifier",
                ],
            ),
            "object_object": self._fetch_duplicate_relation_groups(
                table_name="object_object",
                key_columns=[
                    "ocel_source_id",
                    "ocel_target_id",
                    "ocel_qualifier",
                ],
            ),
            "chanta_event_object_relation_ext": (
                self._fetch_duplicate_relation_groups(
                    table_name="chanta_event_object_relation_ext",
                    key_columns=["event_id", "object_id", "qualifier"],
                )
            ),
            "chanta_object_object_relation_ext": (
                self._fetch_duplicate_relation_groups(
                    table_name="chanta_object_object_relation_ext",
                    key_columns=[
                        "source_object_id",
                        "target_object_id",
                        "qualifier",
                    ],
                )
            ),
        }
        event_object_duplicate_count = len(details["event_object"])
        object_object_duplicate_count = len(details["object_object"])
        chanta_event_object_relation_ext_duplicate_count = len(
            details["chanta_event_object_relation_ext"]
        )
        chanta_object_object_relation_ext_duplicate_count = len(
            details["chanta_object_object_relation_ext"]
        )
        return {
            "valid": event_object_duplicate_count == 0
            and object_object_duplicate_count == 0
            and chanta_event_object_relation_ext_duplicate_count == 0
            and chanta_object_object_relation_ext_duplicate_count == 0,
            "event_object_duplicate_count": event_object_duplicate_count,
            "object_object_duplicate_count": object_object_duplicate_count,
            "chanta_event_object_relation_ext_duplicate_count": (
                chanta_event_object_relation_ext_duplicate_count
            ),
            "chanta_object_object_relation_ext_duplicate_count": (
                chanta_object_object_relation_ext_duplicate_count
            ),
            "details": details,
        }

    def validate_canonical_model(self) -> dict[str, Any]:
        structure = self.validate_structure()
        duplicate_relations = self.validate_duplicate_relations()
        self.store.initialize()
        required_columns = {
            "chanta_event_payload": {
                "event_id",
                "event_activity",
                "event_timestamp",
                "event_attrs_json",
            },
            "chanta_object_state": {
                "object_id",
                "object_type",
                "object_attrs_json",
            },
            "chanta_event_object_relation_ext": {
                "event_id",
                "object_id",
                "qualifier",
                "relation_attrs_json",
            },
            "chanta_object_object_relation_ext": {
                "source_object_id",
                "target_object_id",
                "qualifier",
                "relation_attrs_json",
            },
        }
        table_columns: dict[str, list[str]] = {}
        missing_columns: dict[str, list[str]] = {}
        with sqlite3.connect(self.store.db_path) as connection:
            for table_name, columns in required_columns.items():
                existing = self._table_columns(connection, table_name)
                table_columns[table_name] = sorted(existing)
                missing = sorted(columns - existing)
                if missing:
                    missing_columns[table_name] = missing
        return {
            "valid": structure["valid"]
            and not missing_columns
            and duplicate_relations["valid"],
            "canonical_event_model": "event_activity/event_timestamp/event_attrs_json",
            "canonical_object_model": "object_type/object_attrs_json",
            "canonical_relation_model": "relation_attrs_json",
            "required_tables_exist": structure["required_tables_exist"],
            "missing_tables": structure["missing_tables"],
            "missing_indexes": structure["missing_indexes"],
            "missing_columns": missing_columns,
            "table_columns": table_columns,
            "duplicate_relations": duplicate_relations,
        }

    def validate_export_readiness(self) -> dict[str, Any]:
        self.store.initialize()
        event_count = self.store.fetch_event_count()
        object_count = self.store.fetch_object_count()
        event_object_relation_count = self.store.fetch_event_object_relation_count()
        object_object_relation_count = self.store.fetch_object_object_relation_count()
        events_without_relations = self._fetch_events_without_event_object_relation_count()
        with sqlite3.connect(self.store.db_path) as connection:
            malformed_attrs_json_count = self._malformed_json_count(
                connection,
                "chanta_event_payload",
                "event_attrs_json",
            ) + self._malformed_json_count(
                connection,
                "chanta_object_state",
                "object_attrs_json",
            ) + self._malformed_json_count(
                connection,
                "chanta_event_object_relation_ext",
                "relation_attrs_json",
            ) + self._malformed_json_count(
                connection,
                "chanta_object_object_relation_ext",
                "relation_attrs_json",
            )
            missing_timestamps = self._blank_count(
                connection,
                "chanta_event_payload",
                "event_timestamp",
            )
            missing_event_activity = self._blank_count(
                connection,
                "chanta_event_payload",
                "event_activity",
            )
            missing_object_type = self._blank_count(
                connection,
                "chanta_object_state",
                "object_type",
            )
        relation_count = event_object_relation_count + object_object_relation_count
        return {
            "valid": event_count > 0
            and object_count > 0
            and malformed_attrs_json_count == 0
            and missing_timestamps == 0
            and missing_event_activity == 0
            and missing_object_type == 0
            and self.validate_duplicate_relations()["valid"],
            "event_count": event_count,
            "object_count": object_count,
            "relation_count": relation_count,
            "event_object_relation_count": event_object_relation_count,
            "object_object_relation_count": object_object_relation_count,
            "events_without_relations": events_without_relations,
            "malformed_attrs_json_count": malformed_attrs_json_count,
            "missing_timestamps": missing_timestamps,
            "missing_event_activity": missing_event_activity,
            "missing_object_type": missing_object_type,
            "duplicate_relations": self.validate_duplicate_relations(),
        }

    def _fetch_events_without_event_object_relation_count(self) -> int:
        self.store.initialize()
        with sqlite3.connect(self.store.db_path) as connection:
            row = connection.execute(
                """
                SELECT COUNT(*)
                FROM event
                LEFT JOIN event_object
                    ON event_object.ocel_event_id = event.ocel_id
                WHERE event_object.ocel_object_id IS NULL
                """
            ).fetchone()
        return int(row[0])

    def _fetch_duplicate_relation_groups(
        self,
        *,
        table_name: str,
        key_columns: list[str],
    ) -> list[dict[str, Any]]:
        selected_columns = ", ".join(key_columns)
        group_columns = ", ".join(key_columns)
        query = f"""
            SELECT {selected_columns}, COUNT(*) AS row_count
            FROM {table_name}
            GROUP BY {group_columns}
            HAVING COUNT(*) > 1
            ORDER BY row_count DESC
        """
        with sqlite3.connect(self.store.db_path) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(query).fetchall()
        return [dict(row) for row in rows]

    @staticmethod
    def _table_columns(
        connection: sqlite3.Connection,
        table_name: str,
    ) -> set[str]:
        rows = connection.execute(f"PRAGMA table_info({table_name})").fetchall()
        return {str(row[1]) for row in rows}

    @staticmethod
    def _blank_count(
        connection: sqlite3.Connection,
        table_name: str,
        column_name: str,
    ) -> int:
        row = connection.execute(
            f"""
            SELECT COUNT(*)
            FROM {table_name}
            WHERE {column_name} IS NULL
                OR TRIM({column_name}) = ''
            """
        ).fetchone()
        return int(row[0])

    @staticmethod
    def _malformed_json_count(
        connection: sqlite3.Connection,
        table_name: str,
        column_name: str,
    ) -> int:
        rows = connection.execute(f"SELECT {column_name} FROM {table_name}").fetchall()
        malformed = 0
        for row in rows:
            raw = row[0]
            if raw in (None, ""):
                continue
            try:
                json.loads(raw)
            except Exception:
                malformed += 1
        return malformed
