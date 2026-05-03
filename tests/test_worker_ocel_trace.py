from dataclasses import dataclass, field

from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest
from chanta_core.traces.trace_service import TraceService
from chanta_core.workers import (
    ProcessJobStore,
    WorkerHeartbeatStore,
    WorkerQueueService,
    WorkerRunner,
)


@dataclass(frozen=True)
class FakeProcessResult:
    process_instance_id: str
    status: str = "completed"
    result_attrs: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "process_instance_id": self.process_instance_id,
            "status": self.status,
            "result_attrs": self.result_attrs,
        }


class CompletingLoop:
    def run(self, **kwargs):
        return FakeProcessResult(process_instance_id=kwargs["process_instance_id"])


def test_worker_tool_lifecycle_ocel_trace(tmp_path) -> None:
    store = OCELStore(tmp_path / "worker.sqlite")
    trace_service = TraceService(ocel_store=store)
    job_store = ProcessJobStore(tmp_path / "jobs.jsonl")
    queue = WorkerQueueService(job_store)
    heartbeats = WorkerHeartbeatStore(tmp_path / "heartbeats.jsonl")
    runner = WorkerRunner(
        queue_service=queue,
        heartbeat_store=heartbeats,
        process_run_loop_factory=CompletingLoop,
        trace_service=trace_service,
    )
    dispatcher = ToolDispatcher(
        trace_service=trace_service,
        process_job_store=job_store,
        queue_service=queue,
        worker_runner=runner,
        worker_heartbeat_store=heartbeats,
    )
    context = ToolExecutionContext(
        process_instance_id="process_instance:worker-ocel",
        session_id="session-worker-ocel",
        agent_id="chanta_core_default",
    )

    dispatcher.dispatch(
        ToolRequest.create(
            tool_id="tool:worker",
            operation="enqueue_process_run",
            process_instance_id=context.process_instance_id,
            session_id=context.session_id,
            agent_id=context.agent_id,
            input_attrs={"user_input": "run"},
        ),
        context,
    )
    result = dispatcher.dispatch(
        ToolRequest.create(
            tool_id="tool:worker",
            operation="run_once",
            process_instance_id=context.process_instance_id,
            session_id=context.session_id,
            agent_id=context.agent_id,
        ),
        context,
    )

    assert result.success is True
    activities = [event["event_activity"] for event in store.fetch_recent_events(50)]
    assert "execute_tool_operation" in activities
    assert "complete_tool_operation" in activities
    assert "claim_process_job" in activities
    assert "start_worker_job" in activities
    assert "complete_worker_job" in activities
    assert OCELValidator(store).validate_duplicate_relations()["valid"] is True
