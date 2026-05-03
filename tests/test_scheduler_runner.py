from chanta_core.scheduler import ProcessScheduleStore, SchedulerRunner, SchedulerService
from chanta_core.workers import ProcessJobStore, WorkerQueueService


def test_scheduler_runner_run_once_enqueues_due_schedule(tmp_path) -> None:
    scheduler = SchedulerService(
        schedule_store=ProcessScheduleStore(tmp_path / "schedules.jsonl"),
        queue_service=WorkerQueueService(ProcessJobStore(tmp_path / "jobs.jsonl")),
    )
    scheduler.create_once_schedule(
        schedule_name="once",
        user_input="run",
        agent_id="agent",
        run_at="2026-01-01T00:00:00Z",
    )

    summary = SchedulerRunner(scheduler_service=scheduler).run_once(
        now_iso="2026-01-01T00:00:01Z"
    )

    assert summary["due_count"] == 1
    assert summary["enqueued_count"] == 1


def test_scheduler_runner_no_due_schedule(tmp_path) -> None:
    scheduler = SchedulerService(
        schedule_store=ProcessScheduleStore(tmp_path / "schedules.jsonl"),
        queue_service=WorkerQueueService(ProcessJobStore(tmp_path / "jobs.jsonl")),
    )
    scheduler.create_once_schedule(
        schedule_name="once",
        user_input="run",
        agent_id="agent",
        run_at="2026-01-01T00:00:10Z",
    )

    summary = SchedulerRunner(scheduler_service=scheduler).run_once(
        now_iso="2026-01-01T00:00:01Z"
    )

    assert summary["due_count"] == 0
    assert summary["enqueued_count"] == 0
