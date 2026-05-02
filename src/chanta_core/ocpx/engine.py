from __future__ import annotations

from typing import Any

from chanta_core.ocpx.models import OCPXProcessView


class OCPXEngine:
    def summarize_view(self, view: OCPXProcessView) -> dict[str, Any]:
        return {
            "view_id": view.view_id,
            "source": view.source,
            "session_id": view.session_id,
            "event_count": len(view.events),
            "object_count": len(view.objects),
            "activity_counts": self.count_events_by_activity(view),
            "event_types": self.count_events_by_type(view),
            "object_types": self.count_objects_by_type(view),
        }

    def count_events_by_type(self, view: OCPXProcessView) -> dict[str, int]:
        return self.count_events_by_activity(view)

    def count_events_by_activity(self, view: OCPXProcessView) -> dict[str, int]:
        counts: dict[str, int] = {}
        for event in view.events:
            counts[event.event_activity] = counts.get(event.event_activity, 0) + 1
        return counts

    def count_objects_by_type(self, view: OCPXProcessView) -> dict[str, int]:
        counts: dict[str, int] = {}
        for item in view.objects:
            counts[item.object_type] = counts.get(item.object_type, 0) + 1
        return counts
