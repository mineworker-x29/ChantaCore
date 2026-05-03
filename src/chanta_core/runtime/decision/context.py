from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.pig.guidance import PIGGuidance


@dataclass(frozen=True)
class DecisionContext:
    process_instance_id: str
    session_id: str
    agent_id: str
    user_input: str
    available_skill_ids: list[str]
    explicit_skill_id: str | None
    pig_guidance: list[PIGGuidance]
    context_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "process_instance_id": self.process_instance_id,
            "session_id": self.session_id,
            "agent_id": self.agent_id,
            "user_input": self.user_input,
            "available_skill_ids": self.available_skill_ids,
            "explicit_skill_id": self.explicit_skill_id,
            "pig_guidance": [item.to_dict() for item in self.pig_guidance],
            "context_attrs": self.context_attrs,
        }
