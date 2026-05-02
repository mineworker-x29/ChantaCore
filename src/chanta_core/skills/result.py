from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SkillExecutionResult:
    skill_id: str
    skill_name: str
    success: bool
    output_text: str | None
    output_attrs: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "skill_name": self.skill_name,
            "success": self.success,
            "output_text": self.output_text,
            "output_attrs": self.output_attrs,
            "error": self.error,
        }
