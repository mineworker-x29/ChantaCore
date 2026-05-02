from __future__ import annotations

from chanta_core.skills.skill import Skill


class SkillRegistry:
    """Simple registry placeholder for future skill discovery."""

    def __init__(self) -> None:
        self._skills: dict[str, Skill] = {}

    def register(self, skill: Skill) -> None:
        self._skills[skill.skill_id] = skill

    def get(self, skill_id: str) -> Skill | None:
        return self._skills.get(skill_id)
