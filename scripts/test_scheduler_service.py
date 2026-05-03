from __future__ import annotations

import tempfile
from pathlib import Path

from chanta_core.scheduler import ProcessScheduleStore, SchedulerService
from chanta_core.workers import ProcessJobStore, WorkerQueueService


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        scheduler = SchedulerService(
            schedule_store=ProcessScheduleStore(Path(tmp) / "schedules.jsonl"),
            queue_service=WorkerQueueService(ProcessJobStore(Path(tmp) / "jobs.jsonl")),
        )
        schedule = scheduler.create_once_schedule(
            schedule_name="due once",
            user_input="scheduled process",
            agent_id="chanta_core_default",
            run_at="2026-01-01T00:00:00Z",
        )
        summary = scheduler.enqueue_due(now_iso="2026-01-01T00:00:01Z")
        print(f"schedule_id={schedule.schedule_id}")
        print(f"enqueued_count={summary['enqueued_count']}")
        print(f"job_ids={summary['job_ids']}")
        print(f"schedule_status={scheduler.schedule_store.get(schedule.schedule_id).status}")


if __name__ == "__main__":
    main()
