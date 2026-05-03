from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.scheduler import ProcessScheduleStore, SchedulerService
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest
from chanta_core.traces.trace_service import TraceService
from chanta_core.workers import ProcessJobStore, WorkerQueueService


def test_scheduler_tool_ocel_trace(tmp_path) -> None:
    store = OCELStore(tmp_path / "scheduler.sqlite")
    trace_service = TraceService(ocel_store=store)
    scheduler = SchedulerService(
        schedule_store=ProcessScheduleStore(tmp_path / "schedules.jsonl"),
        queue_service=WorkerQueueService(ProcessJobStore(tmp_path / "jobs.jsonl")),
    )
    dispatcher = ToolDispatcher(trace_service=trace_service, scheduler_service=scheduler)
    context = ToolExecutionContext(
        process_instance_id="process_instance:scheduler-ocel",
        session_id="session-scheduler-ocel",
        agent_id="chanta_core_default",
    )

    dispatcher.dispatch(
        ToolRequest.create(
            tool_id="tool:scheduler",
            operation="create_once_schedule",
            process_instance_id=context.process_instance_id,
            session_id=context.session_id,
            agent_id=context.agent_id,
            input_attrs={
                "schedule_name": "once",
                "user_input": "run",
                "run_at": "2026-01-01T00:00:00Z",
            },
        ),
        context,
    )
    result = dispatcher.dispatch(
        ToolRequest.create(
            tool_id="tool:scheduler",
            operation="run_once",
            process_instance_id=context.process_instance_id,
            session_id=context.session_id,
            agent_id=context.agent_id,
            input_attrs={"now_iso": "2026-01-01T00:00:01Z"},
        ),
        context,
    )

    assert result.success is True
    activities = [event["event_activity"] for event in store.fetch_recent_events(50)]
    assert "create_process_schedule" in activities
    assert "run_scheduler_once" in activities
    assert "execute_tool_operation" in activities
    assert "complete_tool_operation" in activities
    assert OCELValidator(store).validate_duplicate_relations()["valid"] is True
