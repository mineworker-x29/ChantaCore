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
            "activity_sequence": self.activity_sequence(view),
            "activity_counts": self.count_events_by_activity(view),
            "event_types": self.count_events_by_type(view),
            "object_types": self.count_objects_by_type(view),
        }

    def summarize_process_instance_view(self, view: OCPXProcessView) -> dict[str, Any]:
        process_instances = [
            item.object_id
            for item in view.objects
            if item.object_type == "process_instance"
        ]
        return {
            **self.summarize_view(view),
            "process_instance_ids": process_instances,
            "process_instance_count": len(process_instances),
        }

    def activity_sequence(self, view: OCPXProcessView) -> list[str]:
        return [event.event_activity for event in view.events]

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
