from __future__ import annotations

from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill


def create_echo_skill() -> Skill:
    return Skill(
        skill_id="skill:echo",
        skill_name="echo",
        description="Return the user input as-is for deterministic skill dispatch testing.",
        execution_type="builtin",
        input_schema={},
        output_schema={},
        tags=["builtin", "deterministic", "test"],
        skill_attrs={
            "is_builtin": True,
            "requires_llm": False,
            "requires_external_tool": False,
        },
    )


def execute_echo_skill(
    *,
    skill: Skill,
    context: SkillExecutionContext,
    **_,
) -> SkillExecutionResult:
    return SkillExecutionResult(
        skill_id=skill.skill_id,
        skill_name=skill.skill_name,
        success=True,
        output_text=context.user_input,
        output_attrs={
            "execution_type": skill.execution_type,
            "echoed": True,
            "response_length": len(context.user_input),
        },
    )
