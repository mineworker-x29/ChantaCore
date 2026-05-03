from __future__ import annotations

from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest


def create_run_worker_once_skill() -> Skill:
    return Skill(
        skill_id="skill:run_worker_once",
        skill_name="run_worker_once",
        description="Run one local worker queue job synchronously.",
        execution_type="builtin_worker",
        input_schema={},
        output_schema={},
        tags=["builtin", "worker", "internal-harness"],
        skill_attrs={
            "is_builtin": True,
            "requires_llm": False,
            "requires_external_tool": False,
            "uses_worker_queue": True,
        },
    )


def execute_run_worker_once_skill(
    *,
    skill: Skill,
    context: SkillExecutionContext,
    trace_service=None,
    **_,
) -> SkillExecutionResult:
    tool_context = ToolExecutionContext(
        process_instance_id=context.process_instance_id,
        session_id=context.session_id,
        agent_id=context.agent_id,
        context_attrs=context.context_attrs,
    )
    result = ToolDispatcher(trace_service=trace_service).dispatch(
        ToolRequest.create(
            tool_id="tool:worker",
            operation="run_once",
            process_instance_id=context.process_instance_id,
            session_id=context.session_id,
            agent_id=context.agent_id,
            input_attrs={},
            request_attrs={"source_skill_id": skill.skill_id},
        ),
        tool_context,
    )
    return SkillExecutionResult(
        skill_id=skill.skill_id,
        skill_name=skill.skill_name,
        success=result.success,
        output_text=result.output_text,
        output_attrs={"execution_type": skill.execution_type, **result.output_attrs},
        error=result.error,
    )
