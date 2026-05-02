from __future__ import annotations

from uuid import uuid4

from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.models import OCPXEventView, OCPXObjectView, OCPXProcessView


class OCPXLoader:
    def __init__(self, store: OCELStore | None = None) -> None:
        self.store = store or OCELStore()

    def load_session_view(self, session_id: str) -> OCPXProcessView:
        rows = self.store.fetch_events_by_session(session_id)
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
