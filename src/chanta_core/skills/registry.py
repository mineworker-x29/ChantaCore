from __future__ import annotations

from chanta_core.skills.builtin import (
    create_apply_approved_patch_skill,
    create_check_self_conformance_skill,
    create_echo_skill,
    create_ingest_human_pi_skill,
    create_inspect_ocel_recent_skill,
    create_llm_chat_skill,
    create_propose_file_edit_skill,
    create_run_worker_once_skill,
    create_run_scheduler_once_skill,
    create_summarize_pi_artifacts_skill,
    create_summarize_process_trace_skill,
    create_summarize_text_skill,
)
from chanta_core.skills.errors import SkillRegistryError
from chanta_core.skills.skill import Skill


class SkillRegistry:
    """Small registry for built-in and later configured skills."""

    def __init__(self, *, include_builtins: bool = True) -> None:
        self._skills_by_id: dict[str, Skill] = {}
        self._ids_by_name: dict[str, str] = {}
        if include_builtins:
            self.register_builtin_skills()

    def register(self, skill: Skill) -> None:
        skill.validate()
        existing = self._skills_by_id.get(skill.skill_id)
        if existing is not None:
            if existing == skill:
                return
            raise SkillRegistryError(
                f"Skill already registered with different definition: {skill.skill_id}"
            )
        existing_id_for_name = self._ids_by_name.get(skill.skill_name)
        if existing_id_for_name is not None and existing_id_for_name != skill.skill_id:
            raise SkillRegistryError(
                f"Skill name already registered for another skill_id: {skill.skill_name}"
            )
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
            skill = create_llm_chat_skill()
            self.register(skill)
        return skill

    def require(self, skill_id_or_name: str) -> Skill:
        skill = self.get(skill_id_or_name)
        if skill is None:
            raise SkillRegistryError(f"Skill is not registered: {skill_id_or_name}")
        return skill

    def register_builtin_skills(self) -> None:
        self.register(create_apply_approved_patch_skill())
        self.register(create_llm_chat_skill())
        self.register(create_check_self_conformance_skill())
        self.register(create_echo_skill())
        self.register(create_ingest_human_pi_skill())
        self.register(create_propose_file_edit_skill())
        self.register(create_run_worker_once_skill())
        self.register(create_run_scheduler_once_skill())
        self.register(create_summarize_text_skill())
        self.register(create_inspect_ocel_recent_skill())
        self.register(create_summarize_pi_artifacts_skill())
        self.register(create_summarize_process_trace_skill())

    def list_skills(self) -> list[Skill]:
        return [self._skills_by_id[skill_id] for skill_id in sorted(self._skills_by_id)]
