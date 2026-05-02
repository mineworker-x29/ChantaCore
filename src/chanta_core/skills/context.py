from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SkillExecutionContext:
    process_instance_id: str
    session_id: str
    agent_id: str
    user_input: str
    system_prompt: str | None
    event_attrs: dict[str, Any] = field(default_factory=dict)
    context_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "process_instance_id": self.process_instance_id,
            "session_id": self.session_id,
            "agent_id": self.agent_id,
            "user_input": self.user_input,
            "system_prompt": self.system_prompt,
            "event_attrs": self.event_attrs,
            "context_attrs": self.context_attrs,
        }
