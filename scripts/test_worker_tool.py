from __future__ import annotations

import tempfile
from pathlib import Path

from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest
from chanta_core.workers import ProcessJobStore, WorkerHeartbeatStore, WorkerQueueService


def request(operation: str, input_attrs: dict | None = None) -> ToolRequest:
    return ToolRequest.create(
        tool_id="tool:worker",
        operation=operation,
        process_instance_id="process_instance:worker-tool-script",
        session_id="session-worker-tool-script",
        agent_id="chanta_core_default",
        input_attrs=input_attrs or {},
    )


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        job_store = ProcessJobStore(Path(tmp) / "jobs.jsonl")
        queue = WorkerQueueService(job_store)
        heartbeats = WorkerHeartbeatStore(Path(tmp) / "heartbeats.jsonl")
        dispatcher = ToolDispatcher(
            process_job_store=job_store,
            queue_service=queue,
            worker_heartbeat_store=heartbeats,
        )
        context = ToolExecutionContext(
            process_instance_id="process_instance:worker-tool-script",
            session_id="session-worker-tool-script",
            agent_id="chanta_core_default",
        )
        enqueue = dispatcher.dispatch(
            request("enqueue_process_run", {"user_input": "queued via tool"}),
            context,
        )
        summary = dispatcher.dispatch(request("queue_summary"), context)
        recent = dispatcher.dispatch(request("recent_jobs"), context)
        conformance = dispatcher.dispatch(request("check_queue_conformance"), context)
        print(enqueue.output_text)
        print(summary.output_attrs["summary"])
        print(f"recent_jobs={len(recent.output_attrs['jobs'])}")
        print(f"queue_conformance={conformance.output_attrs['status']}")


if __name__ == "__main__":
    main()
