from __future__ import annotations

from chanta_core.skills.skill import Skill


def builtin_llm_chat_skill() -> Skill:
    return Skill(
        skill_id="skill:llm_chat",
        skill_name="llm_chat",
        description=(
            "Use the configured local or remote LLM provider to answer the "
            "user request."
        ),
        execution_type="llm",
        input_schema={},
        output_schema={},
        skill_attrs={
            "provider_mode": "configured",
            "is_builtin": True,
        },
    )
