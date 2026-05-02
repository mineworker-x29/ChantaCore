from __future__ import annotations

from typing import Any

from chanta_core.skills.skill import Skill


class SkillExecutor:
    """Placeholder executor; concrete skill invocation is not part of v0.2."""

    def execute(self, skill: Skill, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return {
            "skill_id": skill.skill_id,
            "skill_name": skill.skill_name,
            "status": "not_implemented",
            "payload": payload or {},
        }
