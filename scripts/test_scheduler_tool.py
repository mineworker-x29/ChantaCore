from __future__ import annotations

import tempfile
from pathlib import Path

from chanta_core.scheduler import ProcessScheduleStore, SchedulerService
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest
from chanta_core.workers import ProcessJobStore, WorkerQueueService


def request(operation: str, attrs: dict | None = None) -> ToolRequest:
    return ToolRequest.create(
        tool_id="tool:scheduler",
        operation=operation,
        process_instance_id="process_instance:scheduler-tool-script",
        session_id="session-scheduler-tool-script",
        agent_id="chanta_core_default",
        input_attrs=attrs or {},
    )


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        service = SchedulerService(
            schedule_store=ProcessScheduleStore(Path(tmp) / "schedules.jsonl"),
            queue_service=WorkerQueueService(ProcessJobStore(Path(tmp) / "jobs.jsonl")),
        )
        dispatcher = ToolDispatcher(scheduler_service=service)
        context = ToolExecutionContext(
            process_instance_id="process_instance:scheduler-tool-script",
            session_id="session-scheduler-tool-script",
            agent_id="chanta_core_default",
        )
        created = dispatcher.dispatch(
            request(
                "create_once_schedule",
                {
                    "schedule_name": "tool once",
                    "user_input": "scheduled via tool",
                    "run_at": "2026-01-01T00:00:00Z",
                },
            ),
            context,
        )
        run = dispatcher.dispatch(
            request("run_once", {"now_iso": "2026-01-01T00:00:01Z"}),
            context,
        )
        recent = dispatcher.dispatch(request("recent_schedules"), context)
        print(created.output_text)
        print(run.output_attrs["summary"])
        print(f"recent_schedules={len(recent.output_attrs['schedules'])}")


if __name__ == "__main__":
    main()
