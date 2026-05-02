from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.utility.time import utc_now_iso


def create_event_id() -> str:
    return str(uuid4())


def utc_timestamp() -> str:
    return utc_now_iso()


@dataclass(frozen=True)
class AgentEvent:
    event_type: str
    session_id: str
    agent_id: str
    payload: dict[str, Any]
    event_id: str = field(default_factory=create_event_id)
    timestamp: str = field(default_factory=utc_timestamp)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "session_id": self.session_id,
            "agent_id": self.agent_id,
            "timestamp": self.timestamp,
            "payload": self.payload,
        }
