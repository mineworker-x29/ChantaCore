from __future__ import annotations

from chanta_core.skills.builtin import builtin_llm_chat_skill
from chanta_core.skills.skill import Skill


class SkillRegistry:
    """Small registry for built-in and later configured skills."""

    def __init__(self, *, include_builtins: bool = True) -> None:
        self._skills_by_id: dict[str, Skill] = {}
        self._ids_by_name: dict[str, str] = {}
        if include_builtins:
            self.register(builtin_llm_chat_skill())

    def register(self, skill: Skill) -> None:
        self._skills_by_id[skill.skill_id] = skill
        self._ids_by_name[skill.skill_name] = skill.skill_id

    def get(self, skill_id_or_name: str) -> Skill | None:
        if skill_id_or_name in self._skills_by_id:
            return self._skills_by_id[skill_id_or_name]
        skill_id = self._ids_by_name.get(skill_id_or_name)
        if skill_id is None:
            return None
        return self._skills_by_id.get(skill_id)

    def get_builtin_llm_chat(self) -> Skill:
        skill = self.get("skill:llm_chat")
        if skill is None:
            skill = builtin_llm_chat_skill()
            self.register(skill)
        return skill

    def list_skills(self) -> list[Skill]:
        return list(self._skills_by_id.values())
