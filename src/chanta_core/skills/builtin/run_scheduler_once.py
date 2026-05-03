from __future__ import annotations

from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill
from chanta_core.scheduler import ProcessScheduleStore, SchedulerService
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest
from chanta_core.workers import ProcessJobStore, WorkerQueueService


def create_run_scheduler_once_skill() -> Skill:
    return Skill(
        skill_id="skill:run_scheduler_once",
        skill_name="run_scheduler_once",
        description="Run one local scheduler evaluation/enqueue pass synchronously.",
        execution_type="builtin_scheduler",
        input_schema={},
        output_schema={},
        tags=["builtin", "scheduler", "internal-harness"],
        skill_attrs={
            "is_builtin": True,
            "requires_llm": False,
            "requires_external_tool": False,
            "uses_scheduler": True,
        },
    )


def execute_run_scheduler_once_skill(
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
    schedule_store_path = context.context_attrs.get("process_schedule_store_path")
    process_job_store_path = context.context_attrs.get("process_job_store_path")
    scheduler_service = None
    if schedule_store_path or process_job_store_path:
        scheduler_service = SchedulerService(
            schedule_store=ProcessScheduleStore(
                schedule_store_path or "data/scheduler/process_schedules.jsonl"
            ),
            queue_service=WorkerQueueService(
                ProcessJobStore(process_job_store_path or "data/workers/process_jobs.jsonl")
            ),
        )
    result = ToolDispatcher(
        trace_service=trace_service,
        scheduler_service=scheduler_service,
    ).dispatch(
        ToolRequest.create(
            tool_id="tool:scheduler",
            operation="run_once",
            process_instance_id=context.process_instance_id,
            session_id=context.session_id,
            agent_id=context.agent_id,
            input_attrs={
                "now_iso": context.context_attrs.get("now_iso"),
            },
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
