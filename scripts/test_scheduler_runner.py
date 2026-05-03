from __future__ import annotations

import tempfile
from pathlib import Path

from chanta_core.scheduler import ProcessScheduleStore, SchedulerRunner, SchedulerService
from chanta_core.workers import ProcessJobStore, WorkerQueueService


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        scheduler = SchedulerService(
            schedule_store=ProcessScheduleStore(Path(tmp) / "schedules.jsonl"),
            queue_service=WorkerQueueService(ProcessJobStore(Path(tmp) / "jobs.jsonl")),
        )
        scheduler.create_once_schedule(
            schedule_name="runner once",
            user_input="scheduled via runner",
            agent_id="chanta_core_default",
            run_at="2026-01-01T00:00:00Z",
        )
        summary = SchedulerRunner(scheduler_service=scheduler).run_once(
            now_iso="2026-01-01T00:00:01Z"
        )
        print(f"due_count={summary['due_count']}")
        print(f"enqueued_count={summary['enqueued_count']}")
        print(f"job_ids={summary['job_ids']}")


if __name__ == "__main__":
    main()
