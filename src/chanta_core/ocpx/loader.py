from __future__ import annotations

import json
import sqlite3
from typing import Any
from uuid import uuid4

from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.models import OCPXEventView, OCPXObjectView, OCPXProcessView


class OCPXLoader:
    def __init__(self, store: OCELStore | None = None) -> None:
        self.store = store or OCELStore()

    def load_session_view(self, session_id: str) -> OCPXProcessView:
        session_object_id = (
            session_id if session_id.startswith("session:") else f"session:{session_id}"
        )
        rows = self._merge_event_rows(
            self.store.fetch_events_by_session(session_id),
            self.store.fetch_events_by_object(session_object_id, qualifier="parent_session"),
            self.store.fetch_events_by_object(session_object_id, qualifier="child_session"),
        )
        return self._build_view(
            rows=rows,
            source="ocel_store:session",
            session_id=session_id,
            view_attrs={"loader": "OCPXLoader"},
        )

    def load_recent_view(self, limit: int = 20) -> OCPXProcessView:
        rows = self.store.fetch_recent_events(limit=limit)
        return self._build_view(
            rows=list(reversed(rows)),
            source="ocel_store:recent",
            session_id=None,
            view_attrs={"loader": "OCPXLoader", "limit": limit},
        )

    def load_process_instance_view(self, process_instance_id: str) -> OCPXProcessView:
        rows = self._merge_event_rows(
            self.store.fetch_events_by_object(
                process_instance_id,
                qualifier="process_context",
            ),
            self.store.fetch_events_by_object(
                process_instance_id,
                qualifier="parent_process",
            ),
            self.store.fetch_events_by_object(
                process_instance_id,
                qualifier="child_process",
            ),
        )
        return self._build_view(
            rows=rows,
            source="ocel_store:process_instance",
            session_id=None,
            view_attrs={
                "loader": "OCPXLoader",
                "process_instance_id": process_instance_id,
            },
        )

    def load_session_process_instances(
        self,
        session_id: str,
    ) -> list[dict[str, Any]]:
        self.store.initialize()
        session_object_id = (
            session_id if session_id.startswith("session:") else f"session:{session_id}"
        )
        with sqlite3.connect(self.store.db_path) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                """
                SELECT
                    object_state.object_id,
                    object_state.object_type,
                    object_state.object_attrs_json,
                    relation.qualifier
                FROM chanta_object_object_relation_ext AS relation
                JOIN chanta_object_state AS object_state
                    ON object_state.object_id = relation.source_object_id
                WHERE relation.target_object_id = ?
                    AND relation.qualifier = 'handled_in_session'
                    AND object_state.object_type = 'process_instance'
                ORDER BY object_state.object_id ASC
                """,
                (session_object_id,),
            ).fetchall()
        return [
            {
                "object_id": row["object_id"],
                "object_type": row["object_type"],
                "object_attrs": json.loads(row["object_attrs_json"] or "{}"),
                "qualifier": row["qualifier"],
            }
            for row in rows
        ]

    def _build_view(
        self,
        *,
        rows: list[dict],
        source: str,
        session_id: str | None,
        view_attrs: dict,
    ) -> OCPXProcessView:
        events: list[OCPXEventView] = []
        objects_by_id: dict[str, OCPXObjectView] = {}

        for row in rows:
            related_objects = self.store.fetch_related_objects_for_event(row["event_id"])
            for item in related_objects:
                objects_by_id[item["object_id"]] = OCPXObjectView(
                    object_id=item["object_id"],
                    object_type=item["object_type"],
                    object_attrs=item["object_attrs"],
                )
            events.append(
                OCPXEventView(
                    event_id=row["event_id"],
                    event_activity=row["event_activity"],
                    event_timestamp=row["event_timestamp"],
                    related_objects=related_objects,
                    event_attrs=row["event_attrs"],
                )
            )

        return OCPXProcessView(
            view_id=f"ocpx_view:{uuid4()}",
            source=source,
            session_id=session_id,
            events=events,
            objects=list(objects_by_id.values()),
            view_attrs=view_attrs,
        )

    @staticmethod
    def _merge_event_rows(*row_groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
        merged_rows: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        for rows in row_groups:
            for row in rows:
                event_id = str(row["event_id"])
                if event_id in seen_ids:
                    continue
                merged_rows.append(row)
                seen_ids.add(event_id)
        return merged_rows
