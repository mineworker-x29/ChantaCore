from __future__ import annotations

import sqlite3

from chanta_core.ocel.store import OCELStore


class OCELQueryService:
    def __init__(self, store: OCELStore | None = None) -> None:
        self.store = store or OCELStore()

    def session_summary(self, session_id: str) -> dict[str, object]:
        events = self.store.fetch_events_by_session(session_id)
        related_object_ids: set[str] = set()
        for event in events:
            for item in self.store.fetch_related_objects_for_event(event["event_id"]):
                related_object_ids.add(item["object_id"])
        return {
            "session_id": session_id,
            "event_count": len(events),
            "object_count": len(related_object_ids),
            "event_activities": [event["event_activity"] for event in events],
        }

    def relation_counts_for_session(self, session_id: str) -> dict[str, object]:
        events = self.store.fetch_events_by_session(session_id)
        event_object_relations = self.session_event_object_relations(session_id)
        object_relations = self.session_object_relations(session_id)
        object_ids = {
            relation["object_id"] for relation in event_object_relations
        }
        return {
            "session_id": session_id,
            "event_count": len(events),
            "object_count": len(object_ids),
            "event_object_relation_count": len(event_object_relations),
            "object_object_relation_count": len(object_relations),
        }

    def session_event_object_relations(
        self,
        session_id: str,
    ) -> list[dict[str, object]]:
        self.store.initialize()
        with sqlite3.connect(self.store.db_path) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                """
                SELECT
                    relation.event_id,
                    relation.object_id,
                    relation.qualifier,
                    relation.relation_attrs_json
                FROM chanta_event_object_relation_ext AS relation
                JOIN event_object AS session_relation
                    ON session_relation.ocel_event_id = relation.event_id
                JOIN chanta_event_payload AS payload
                    ON payload.event_id = relation.event_id
                WHERE session_relation.ocel_object_id = ?
                    AND session_relation.ocel_qualifier = 'session_context'
                ORDER BY payload.event_timestamp ASC, relation.qualifier ASC
                """,
                (f"session:{session_id}",),
            ).fetchall()
        return [dict(row) for row in rows]

    def session_object_relations(
        self,
        session_id: str,
    ) -> list[dict[str, object]]:
        object_ids = [
            str(relation["object_id"])
            for relation in self.session_event_object_relations(session_id)
        ]
        unique_object_ids = sorted(set(object_ids))
        if not unique_object_ids:
            return []

        placeholders = ", ".join("?" for _ in unique_object_ids)
        query = f"""
            SELECT
                source_object_id,
                target_object_id,
                qualifier,
                relation_attrs_json
            FROM chanta_object_object_relation_ext
            WHERE source_object_id IN ({placeholders})
                OR target_object_id IN ({placeholders})
            ORDER BY qualifier ASC, source_object_id ASC, target_object_id ASC
        """
        with sqlite3.connect(self.store.db_path) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                query,
                unique_object_ids + unique_object_ids,
            ).fetchall()
        return [dict(row) for row in rows]

    def recent_events(self, limit: int = 20) -> list[dict[str, object]]:
        return self.store.fetch_recent_events(limit=limit)

    def object_type_counts(self) -> dict[str, int]:
        self.store.initialize()
        with sqlite3.connect(self.store.db_path) as connection:
            rows = connection.execute(
                """
                SELECT object_type, COUNT(*)
                FROM chanta_object_state
                GROUP BY object_type
                ORDER BY object_type ASC
                """
            ).fetchall()
        return {str(row[0]): int(row[1]) for row in rows}
