from __future__ import annotations

from typing import TYPE_CHECKING

from chanta_core.scheduler.service import SchedulerService
from chanta_core.scheduler.store import ProcessScheduleStore
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.request import ToolRequest
from chanta_core.tools.result import ToolResult
from chanta_core.tools.tool import Tool

if TYPE_CHECKING:
    from chanta_core.scheduler.runner import SchedulerRunner


def create_scheduler_tool() -> Tool:
    return Tool(
        tool_id="tool:scheduler",
        tool_name="scheduler",
        description="Internal scheduler gateway for one-time and interval process runs.",
        tool_kind="internal",
        safety_level="internal_compute",
        supported_operations=[
            "create_once_schedule",
            "create_interval_schedule",
            "pause_schedule",
            "resume_schedule",
            "cancel_schedule",
            "list_active",
            "evaluate_due",
            "enqueue_due",
            "run_once",
            "recent_schedules",
        ],
        input_schema={},
        output_schema={},
        tool_attrs={
            "is_builtin": True,
            "internal_harness": True,
            "requires_external_tool": False,
            "allows_shell": False,
            "allows_network": False,
            "is_daemon": False,
        },
    )


def execute_scheduler_tool(
    *,
    tool: Tool,
    request: ToolRequest,
    context: ToolExecutionContext,
    scheduler_service: SchedulerService | None = None,
    scheduler_runner: "SchedulerRunner | None" = None,
    process_schedule_store: ProcessScheduleStore | None = None,
    trace_service=None,
    **_,
) -> ToolResult:
    service = scheduler_service or SchedulerService(
        schedule_store=process_schedule_store or ProcessScheduleStore()
    )
    if scheduler_runner is None:
        from chanta_core.scheduler.runner import SchedulerRunner

        runner = SchedulerRunner(scheduler_service=service, trace_service=trace_service)
    else:
        runner = scheduler_runner
    operation = request.operation
    try:
        if operation == "create_once_schedule":
            schedule = service.create_once_schedule(
                schedule_name=str(request.input_attrs.get("schedule_name") or "Scheduled process"),
                user_input=str(request.input_attrs.get("user_input") or ""),
                agent_id=str(request.input_attrs.get("agent_id") or context.agent_id),
                run_at=str(request.input_attrs.get("run_at") or ""),
                requested_skill_id=request.input_attrs.get("requested_skill_id"),
                priority=int(request.input_attrs.get("priority") or 0),
                max_retries=int(request.input_attrs.get("max_retries") or 0),
                schedule_attrs=dict(request.input_attrs.get("schedule_attrs") or {}),
            )
            _record(trace_service, "create_process_schedule", schedule, "active")
            return _success(request, tool, f"Created schedule: {schedule.schedule_id}", {"schedule": schedule.to_dict(), "schedule_id": schedule.schedule_id})
        if operation == "create_interval_schedule":
            schedule = service.create_interval_schedule(
                schedule_name=str(request.input_attrs.get("schedule_name") or "Interval process"),
                user_input=str(request.input_attrs.get("user_input") or ""),
                agent_id=str(request.input_attrs.get("agent_id") or context.agent_id),
                interval_seconds=int(request.input_attrs.get("interval_seconds") or 0),
                requested_skill_id=request.input_attrs.get("requested_skill_id"),
                priority=int(request.input_attrs.get("priority") or 0),
                max_retries=int(request.input_attrs.get("max_retries") or 0),
                schedule_attrs=dict(request.input_attrs.get("schedule_attrs") or {}),
            )
            _record(trace_service, "create_process_schedule", schedule, "active")
            return _success(request, tool, f"Created interval schedule: {schedule.schedule_id}", {"schedule": schedule.to_dict(), "schedule_id": schedule.schedule_id})
        if operation == "pause_schedule":
            schedule = service.pause(str(request.input_attrs.get("schedule_id") or ""))
            _record(trace_service, "pause_process_schedule", schedule, "paused")
            return _success(request, tool, f"Paused schedule: {schedule.schedule_id}", {"schedule": schedule.to_dict()})
        if operation == "resume_schedule":
            schedule = service.resume(str(request.input_attrs.get("schedule_id") or ""))
            _record(trace_service, "resume_process_schedule", schedule, "active")
            return _success(request, tool, f"Resumed schedule: {schedule.schedule_id}", {"schedule": schedule.to_dict()})
        if operation == "cancel_schedule":
            schedule = service.cancel(str(request.input_attrs.get("schedule_id") or ""))
            _record(trace_service, "cancel_process_schedule", schedule, "cancelled")
            return _success(request, tool, f"Cancelled schedule: {schedule.schedule_id}", {"schedule": schedule.to_dict()})
        if operation == "list_active":
            schedules = [item.to_dict() for item in service.list_active()]
            return _success(request, tool, f"Active schedules: {len(schedules)}", {"schedules": schedules})
        if operation == "evaluate_due":
            now_iso = request.input_attrs.get("now_iso")
            due = service.evaluate_due(now_iso=str(now_iso) if now_iso else None)
            _record(trace_service, "evaluate_process_schedule", None, "evaluated", {"due_count": len(due)})
            return _success(
                request,
                tool,
                f"Due schedules: {len(due)}",
                {"due": [{"schedule": schedule.to_dict(), "evaluation": evaluation.to_dict()} for schedule, evaluation in due]},
            )
        if operation == "enqueue_due":
            now_iso = request.input_attrs.get("now_iso")
            summary = service.enqueue_due(now_iso=str(now_iso) if now_iso else None)
            _record(trace_service, "enqueue_scheduled_process", None, "enqueued", summary)
            return _success(request, tool, f"Enqueued scheduled jobs: {summary['enqueued_count']}", {"summary": summary})
        if operation == "run_once":
            now_iso = request.input_attrs.get("now_iso")
            summary = runner.run_once(now_iso=str(now_iso) if now_iso else None)
            return _success(request, tool, f"Scheduler run_once enqueued: {summary['enqueued_count']}", {"summary": summary})
        if operation == "recent_schedules":
            limit = int(request.input_attrs.get("limit") or 20)
            schedules = [item.to_dict() for item in service.schedule_store.recent(limit)]
            return _success(request, tool, f"Recent schedules: {len(schedules)}", {"schedules": schedules})
    except Exception as error:
        return ToolResult.create(
            tool_request_id=request.tool_request_id,
            tool_id=tool.tool_id,
            operation=request.operation,
            success=False,
            output_text=None,
            output_attrs={
                "exception_type": type(error).__name__,
                "failure_stage": "scheduler_tool",
                "operation": operation,
            },
            error=str(error),
        )

    return ToolResult.create(
        tool_request_id=request.tool_request_id,
        tool_id=tool.tool_id,
        operation=request.operation,
        success=False,
        output_text=None,
        output_attrs={"exception_type": "ToolDispatchError", "failure_stage": "scheduler_tool"},
        error=f"Unsupported tool:scheduler operation: {operation}",
    )


def _success(
    request: ToolRequest,
    tool: Tool,
    output_text: str,
    output_attrs: dict,
) -> ToolResult:
    return ToolResult.create(
        tool_request_id=request.tool_request_id,
        tool_id=tool.tool_id,
        operation=request.operation,
        success=True,
        output_text=output_text,
        output_attrs=output_attrs,
    )


def _record(
    trace_service,
    event_activity: str,
    schedule,
    status: str,
    attrs: dict | None = None,
) -> None:
    if trace_service is None:
        return
    recorder = getattr(trace_service, "record_scheduler_lifecycle_event", None)
    if recorder is None:
        return
    recorder(
        event_activity=event_activity,
        schedule=schedule,
        job_id=None,
        status=status,
        event_attrs=attrs or {},
    )
