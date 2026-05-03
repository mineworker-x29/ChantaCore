from chanta_core.scheduler import ProcessScheduleStore, SchedulerService
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest
from chanta_core.workers import ProcessJobStore, WorkerQueueService


def context() -> ToolExecutionContext:
    return ToolExecutionContext(
        process_instance_id="process_instance:scheduler-tool",
        session_id="session-scheduler-tool",
        agent_id="chanta_core_default",
    )


def request(operation: str, input_attrs: dict | None = None) -> ToolRequest:
    return ToolRequest.create(
        tool_id="tool:scheduler",
        operation=operation,
        process_instance_id="process_instance:scheduler-tool",
        session_id="session-scheduler-tool",
        agent_id="chanta_core_default",
        input_attrs=input_attrs or {},
    )


def dispatcher(tmp_path) -> ToolDispatcher:
    service = SchedulerService(
        schedule_store=ProcessScheduleStore(tmp_path / "schedules.jsonl"),
        queue_service=WorkerQueueService(ProcessJobStore(tmp_path / "jobs.jsonl")),
    )
    return ToolDispatcher(scheduler_service=service)


def test_scheduler_tool_create_once_and_list_active(tmp_path) -> None:
    tool_dispatcher = dispatcher(tmp_path)
    created = tool_dispatcher.dispatch(
        request(
            "create_once_schedule",
            {
                "schedule_name": "once",
                "user_input": "run",
                "run_at": "2026-01-01T00:00:00Z",
            },
        ),
        context(),
    )
    active = tool_dispatcher.dispatch(request("list_active"), context())

    assert created.success is True
    assert created.output_attrs["schedule_id"].startswith("process_schedule:")
    assert len(active.output_attrs["schedules"]) == 1


def test_scheduler_tool_create_interval_evaluate_enqueue_and_recent(tmp_path) -> None:
    tool_dispatcher = dispatcher(tmp_path)
    created = tool_dispatcher.dispatch(
        request(
            "create_interval_schedule",
            {
                "schedule_name": "interval",
                "user_input": "run",
                "interval_seconds": 30,
            },
        ),
        context(),
    )
    schedule_id = created.output_attrs["schedule_id"]
    service = tool_dispatcher.scheduler_service
    schedule = service.schedule_store.get(schedule_id)
    service.schedule_store.upsert(
        schedule.__class__(**{**schedule.to_dict(), "next_run_at": "2026-01-01T00:00:00Z"})
    )

    due = tool_dispatcher.dispatch(
        request("evaluate_due", {"now_iso": "2026-01-01T00:00:01Z"}),
        context(),
    )
    enqueued = tool_dispatcher.dispatch(
        request("enqueue_due", {"now_iso": "2026-01-01T00:00:01Z"}),
        context(),
    )
    recent = tool_dispatcher.dispatch(request("recent_schedules"), context())

    assert due.output_attrs["due"]
    assert enqueued.output_attrs["summary"]["enqueued_count"] == 1
    assert recent.output_attrs["schedules"]


def test_scheduler_tool_run_once(tmp_path) -> None:
    tool_dispatcher = dispatcher(tmp_path)
    tool_dispatcher.dispatch(
        request(
            "create_once_schedule",
            {
                "schedule_name": "once",
                "user_input": "run",
                "run_at": "2026-01-01T00:00:00Z",
            },
        ),
        context(),
    )

    result = tool_dispatcher.dispatch(
        request("run_once", {"now_iso": "2026-01-01T00:00:01Z"}),
        context(),
    )

    assert result.success is True
    assert result.output_attrs["summary"]["enqueued_count"] == 1


def test_scheduler_tool_pause_resume_cancel(tmp_path) -> None:
    tool_dispatcher = dispatcher(tmp_path)
    created = tool_dispatcher.dispatch(
        request(
            "create_once_schedule",
            {
                "schedule_name": "once",
                "user_input": "run",
                "run_at": "2026-01-01T00:00:00Z",
            },
        ),
        context(),
    )
    schedule_id = created.output_attrs["schedule_id"]

    assert tool_dispatcher.dispatch(request("pause_schedule", {"schedule_id": schedule_id}), context()).success is True
    assert tool_dispatcher.dispatch(request("resume_schedule", {"schedule_id": schedule_id}), context()).success is True
    assert tool_dispatcher.dispatch(request("cancel_schedule", {"schedule_id": schedule_id}), context()).success is True
