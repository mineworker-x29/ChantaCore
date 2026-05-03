from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest
from chanta_core.workers import ProcessJobStore, WorkerQueueService


def context() -> ToolExecutionContext:
    return ToolExecutionContext(
        process_instance_id="process_instance:worker-conformance",
        session_id="session-worker-conformance",
        agent_id="chanta_core_default",
    )


def request(operation: str, input_attrs: dict | None = None) -> ToolRequest:
    return ToolRequest.create(
        tool_id="tool:worker",
        operation=operation,
        process_instance_id="process_instance:worker-conformance",
        session_id="session-worker-conformance",
        agent_id="chanta_core_default",
        input_attrs=input_attrs or {},
    )


def test_worker_tool_check_queue_conformance_recent_jobs(tmp_path) -> None:
    job_store = ProcessJobStore(tmp_path / "jobs.jsonl")
    queue = WorkerQueueService(job_store)
    dispatcher = ToolDispatcher(process_job_store=job_store, queue_service=queue)

    dispatcher.dispatch(request("enqueue_process_run", {"user_input": "run"}), context())
    result = dispatcher.dispatch(request("check_queue_conformance"), context())

    assert result.success is True
    assert result.output_attrs["status"] in {"conformant", "warning", "nonconformant", "unknown"}
    assert "issues" in result.output_attrs["report"]


def test_worker_tool_check_queue_conformance_single_job(tmp_path) -> None:
    job_store = ProcessJobStore(tmp_path / "jobs.jsonl")
    queue = WorkerQueueService(job_store)
    dispatcher = ToolDispatcher(process_job_store=job_store, queue_service=queue)
    enqueue_result = dispatcher.dispatch(request("enqueue_process_run", {"user_input": "run"}), context())

    result = dispatcher.dispatch(
        request(
            "check_queue_conformance",
            {"job_id": enqueue_result.output_attrs["job_id"]},
        ),
        context(),
    )

    assert result.success is True
    assert result.output_attrs["report"]["job_id"] == enqueue_result.output_attrs["job_id"]
