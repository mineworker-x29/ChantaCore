from __future__ import annotations

from typing import Any

from chanta_core.ocpx.models import OCPXProcessView


class OCPXValidator:
    def validate_process_view(self, view: OCPXProcessView) -> dict[str, Any]:
        event_ids = [event.event_id for event in view.events]
        object_ids = [item.object_id for item in view.objects]
        return {
            "valid": len(event_ids) == len(set(event_ids))
            and len(object_ids) == len(set(object_ids)),
            "event_count": len(event_ids),
            "object_count": len(object_ids),
            "duplicate_event_ids": len(event_ids) - len(set(event_ids)),
            "duplicate_object_ids": len(object_ids) - len(set(object_ids)),
        }
