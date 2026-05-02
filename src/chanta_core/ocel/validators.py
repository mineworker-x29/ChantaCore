from __future__ import annotations

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
