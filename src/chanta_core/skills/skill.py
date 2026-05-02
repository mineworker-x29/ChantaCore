from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.skills.errors import SkillValidationError


@dataclass(frozen=True)
class Skill:
    """Capability descriptor used by the skill dispatch runtime."""

    skill_id: str
    skill_name: str
    description: str
    execution_type: str
    input_schema: dict[str, Any] = field(default_factory=dict)
    output_schema: dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    skill_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "skill_name": self.skill_name,
            "description": self.description,
            "execution_type": self.execution_type,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "tags": self.tags,
            "skill_attrs": self.skill_attrs,
        }

    def validate(self) -> None:
        if not self.skill_id:
            raise SkillValidationError("skill_id must not be empty")
        if not self.skill_id.startswith("skill:"):
            raise SkillValidationError("skill_id must start with 'skill:'")
        if not self.skill_name:
            raise SkillValidationError("skill_name must not be empty")
        if not self.execution_type:
            raise SkillValidationError("execution_type must not be empty")
        if not isinstance(self.input_schema, dict):
            raise SkillValidationError("input_schema must be a dict")
        if not isinstance(self.output_schema, dict):
            raise SkillValidationError("output_schema must be a dict")
        if not isinstance(self.tags, list) or not all(isinstance(item, str) for item in self.tags):
            raise SkillValidationError("tags must be a list[str]")
        if not isinstance(self.skill_attrs, dict):
            raise SkillValidationError("skill_attrs must be a dict")
