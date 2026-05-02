from __future__ import annotations

from typing import Any

from chanta_core.ocel.factory import new_event_id
from chanta_core.ocel.models import OCELRecord, OCELEvent
from chanta_core.utility.time import utc_now_iso


class OCELMapper:
    """Compatibility mapper for legacy AgentEvent-shaped records."""

    def map_agent_event(self, value: Any) -> OCELRecord | None:
        if hasattr(value, "to_dict"):
            return self.map_agent_event_dict(value.to_dict())
        if isinstance(value, dict):
            return self.map_agent_event_dict(value)
        return None

    def map_agent_event_dict(self, value: dict[str, Any]) -> OCELRecord | None:
        runtime_event_type = value.get("event_type")
        if not runtime_event_type:
            return None
        event = OCELEvent(
            event_id=value.get("event_id") or new_event_id("evt"),
            event_activity=str(runtime_event_type),
            event_timestamp=value.get("timestamp") or utc_now_iso(),
            event_attrs={
                "runtime_event_type": runtime_event_type,
                "source_runtime": "chanta_core_legacy_mapper",
                "session_id": value.get("session_id"),
                "trace_id": value.get("session_id"),
                "actor_type": "agent",
                "actor_id": value.get("agent_id"),
                "payload": value.get("payload") or {},
            },
        )
        return OCELRecord(event=event, objects=[], relations=[])
