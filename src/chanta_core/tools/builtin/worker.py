from __future__ import annotations

from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.request import ToolRequest
from chanta_core.tools.result import ToolResult
from chanta_core.tools.tool import Tool
from typing import TYPE_CHECKING

from chanta_core.workers.heartbeat import WorkerHeartbeatStore
from chanta_core.workers.queue import WorkerQueueService
from chanta_core.workers.store import ProcessJobStore
from chanta_core.workers.worker import Worker

if TYPE_CHECKING:
    from chanta_core.workers.runner import WorkerRunner


def create_worker_tool() -> Tool:
    return Tool(
        tool_id="tool:worker",
        tool_name="worker",
        description="Internal worker queue and background process gateway.",
        tool_kind="internal",
        safety_level="internal_compute",
        supported_operations=[
            "enqueue_process_run",
            "claim_next",
            "run_once",
            "queue_summary",
            "recent_jobs",
            "recent_heartbeats",
            "check_queue_conformance",
        ],
        input_schema={},
        output_schema={},
        tool_attrs={
            "is_builtin": True,
            "internal_harness": True,
            "requires_external_tool": False,
            "allows_shell": False,
            "allows_network": False,
        },
    )


def execute_worker_tool(
    *,
    tool: Tool,
    request: ToolRequest,
    context: ToolExecutionContext,
    queue_service: WorkerQueueService | None = None,
    worker_runner: "WorkerRunner | None" = None,
    heartbeat_store: WorkerHeartbeatStore | None = None,
    process_job_store: ProcessJobStore | None = None,
    queue_conformance_service=None,
    trace_service=None,
    **_,
) -> ToolResult:
    job_store = process_job_store or ProcessJobStore()
    queue = queue_service or WorkerQueueService(job_store, trace_service=trace_service)
    heartbeats = heartbeat_store or WorkerHeartbeatStore()
    if worker_runner is None:
        from chanta_core.workers.runner import WorkerRunner

        runner = WorkerRunner(
            queue_service=queue,
            heartbeat_store=heartbeats,
            trace_service=trace_service,
        )
    else:
        runner = worker_runner
    operation = request.operation
    try:
        if operation == "enqueue_process_run":
            job = queue.enqueue_process_run(
                user_input=str(request.input_attrs.get("user_input") or context.context_attrs.get("user_input") or ""),
                agent_id=str(request.input_attrs.get("agent_id") or context.agent_id),
                session_id=request.input_attrs.get("session_id") or context.session_id,
                process_instance_id=request.input_attrs.get("process_instance_id"),
                requested_skill_id=request.input_attrs.get("requested_skill_id"),
                priority=int(request.input_attrs.get("priority") or 0),
                max_retries=int(request.input_attrs.get("max_retries") or 0),
                job_attrs=dict(request.input_attrs.get("job_attrs") or {}),
            )
            _record_worker_event(
                trace_service,
                event_activity="enqueue_process_job",
                worker=Worker(worker_id="worker:queue", worker_name="queue"),
                job=job,
                status="queued",
            )
            return _success(
                request,
                tool,
                f"Enqueued process job: {job.job_id}",
                {"job": job.to_dict(), "job_id": job.job_id},
            )
        if operation == "claim_next":
            worker_id = str(request.input_attrs.get("worker_id") or "worker:tool")
            job = queue.claim_next(worker_id)
            if job is not None:
                _record_worker_event(
                    trace_service,
                    event_activity="claim_process_job",
                    worker=Worker(worker_id=worker_id, worker_name=worker_id),
                    job=job,
                    status="claimed",
                )
            return _success(
                request,
                tool,
                "Claimed process job." if job else "No queued process job.",
                {"job": job.to_dict() if job else None, "worker_id": worker_id},
            )
        if operation == "run_once":
            result = runner.run_once()
            return _success(
                request,
                tool,
                f"Worker run_once status: {result.get('status')}",
                {"run_once": result},
            )
        if operation == "queue_summary":
            summary = queue.summary()
            return _success(request, tool, "Worker queue summary.", {"summary": summary})
        if operation == "recent_jobs":
            limit = int(request.input_attrs.get("limit") or 20)
            jobs = [job.to_dict() for job in job_store.recent(limit)]
            return _success(request, tool, f"Recent process jobs: {len(jobs)}", {"jobs": jobs})
        if operation == "recent_heartbeats":
            limit = int(request.input_attrs.get("limit") or 20)
            rows = [item.to_dict() for item in heartbeats.recent(limit)]
            return _success(
                request,
                tool,
                f"Recent worker heartbeats: {len(rows)}",
                {"heartbeats": rows},
            )
        if operation == "check_queue_conformance":
            service = queue_conformance_service
            if service is None:
                from chanta_core.pig.queue_conformance import PIGQueueConformanceService

                service = PIGQueueConformanceService(job_store=job_store)
            job_id = request.input_attrs.get("job_id")
            if job_id:
                report = service.check_job(str(job_id))
            else:
                report = service.check_recent_jobs(int(request.input_attrs.get("limit") or 20))
            return _success(
                request,
                tool,
                f"Queue conformance status: {report.status}",
                {"report": report.to_dict(), "status": report.status},
            )
    except Exception as error:
        return ToolResult.create(
            tool_request_id=request.tool_request_id,
            tool_id=tool.tool_id,
            operation=request.operation,
            success=False,
            output_text=None,
            output_attrs={
                "exception_type": type(error).__name__,
                "failure_stage": "worker_tool",
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
        output_attrs={"exception_type": "ToolDispatchError", "failure_stage": "worker_tool"},
        error=f"Unsupported tool:worker operation: {operation}",
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


def _record_worker_event(
    trace_service,
    *,
    event_activity: str,
    worker: Worker,
    job,
    status: str,
) -> None:
    if trace_service is None:
        return
    recorder = getattr(trace_service, "record_worker_lifecycle_event", None)
    if recorder is None:
        return
    recorder(
        event_activity=event_activity,
        worker=worker,
        job=job,
        status=status,
        event_attrs={"source": "tool:worker"},
    )
