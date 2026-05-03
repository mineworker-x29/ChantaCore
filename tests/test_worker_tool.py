from dataclasses import dataclass, field

from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest
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


def context() -> ToolExecutionContext:
    return ToolExecutionContext(
        process_instance_id="process_instance:worker-tool",
        session_id="session-worker-tool",
        agent_id="chanta_core_default",
    )


def request(operation: str, input_attrs: dict | None = None) -> ToolRequest:
    return ToolRequest.create(
        tool_id="tool:worker",
        operation=operation,
        process_instance_id="process_instance:worker-tool",
        session_id="session-worker-tool",
        agent_id="chanta_core_default",
        input_attrs=input_attrs or {},
    )


def dispatcher(tmp_path) -> ToolDispatcher:
    job_store = ProcessJobStore(tmp_path / "jobs.jsonl")
    queue = WorkerQueueService(job_store)
    heartbeats = WorkerHeartbeatStore(tmp_path / "heartbeats.jsonl")
    runner = WorkerRunner(
        queue_service=queue,
        heartbeat_store=heartbeats,
        process_run_loop_factory=CompletingLoop,
    )
    return ToolDispatcher(
        process_job_store=job_store,
        queue_service=queue,
        worker_runner=runner,
        worker_heartbeat_store=heartbeats,
    )


def test_worker_tool_enqueue_and_summary(tmp_path) -> None:
    tool_dispatcher = dispatcher(tmp_path)

    result = tool_dispatcher.dispatch(
        request("enqueue_process_run", {"user_input": "run", "priority": 3}),
        context(),
    )
    summary = tool_dispatcher.dispatch(request("queue_summary"), context())

    assert result.success is True
    assert result.output_attrs["job_id"].startswith("process_job:")
    assert summary.output_attrs["summary"]["queued_count"] == 1


def test_worker_tool_run_once_with_fake_runner(tmp_path) -> None:
    tool_dispatcher = dispatcher(tmp_path)
    tool_dispatcher.dispatch(request("enqueue_process_run", {"user_input": "run"}), context())

    result = tool_dispatcher.dispatch(request("run_once"), context())

    assert result.success is True
    assert result.output_attrs["run_once"]["status"] == "completed"


def test_worker_tool_recent_jobs_and_heartbeats(tmp_path) -> None:
    tool_dispatcher = dispatcher(tmp_path)
    tool_dispatcher.dispatch(request("enqueue_process_run", {"user_input": "run"}), context())
    tool_dispatcher.dispatch(request("run_once"), context())

    jobs = tool_dispatcher.dispatch(request("recent_jobs"), context())
    heartbeats = tool_dispatcher.dispatch(request("recent_heartbeats"), context())

    assert jobs.success is True
    assert jobs.output_attrs["jobs"]
    assert heartbeats.success is True
    assert heartbeats.output_attrs["heartbeats"]


def test_worker_tool_claim_next(tmp_path) -> None:
    tool_dispatcher = dispatcher(tmp_path)
    tool_dispatcher.dispatch(request("enqueue_process_run", {"user_input": "run"}), context())

    result = tool_dispatcher.dispatch(request("claim_next", {"worker_id": "worker:test"}), context())

    assert result.success is True
    assert result.output_attrs["job"]["status"] == "claimed"
