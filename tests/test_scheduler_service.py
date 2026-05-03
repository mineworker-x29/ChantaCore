from dataclasses import replace

from chanta_core.scheduler import ProcessScheduleStore, SchedulerService
from chanta_core.workers import ProcessJobStore, WorkerQueueService


def service(tmp_path) -> SchedulerService:
    return SchedulerService(
        schedule_store=ProcessScheduleStore(tmp_path / "schedules.jsonl"),
        queue_service=WorkerQueueService(ProcessJobStore(tmp_path / "jobs.jsonl")),
    )


def test_create_once_and_interval_schedule(tmp_path) -> None:
    scheduler = service(tmp_path)
    once = scheduler.create_once_schedule(
        schedule_name="once",
        user_input="run once",
        agent_id="agent",
        run_at="2026-01-01T00:00:00Z",
    )
    interval = scheduler.create_interval_schedule(
        schedule_name="interval",
        user_input="run interval",
        agent_id="agent",
        interval_seconds=60,
    )

    assert once.schedule_type == "once"
    assert interval.schedule_type == "interval"
    assert interval.next_run_at is not None


def test_pause_resume_cancel(tmp_path) -> None:
    scheduler = service(tmp_path)
    schedule = scheduler.create_once_schedule(
        schedule_name="once",
        user_input="run",
        agent_id="agent",
        run_at="2026-01-01T00:00:00Z",
    )

    assert scheduler.pause(schedule.schedule_id).status == "paused"
    assert scheduler.resume(schedule.schedule_id).status == "active"
    assert scheduler.cancel(schedule.schedule_id).status == "cancelled"


def test_evaluate_due(tmp_path) -> None:
    scheduler = service(tmp_path)
    schedule = scheduler.create_once_schedule(
        schedule_name="once",
        user_input="run",
        agent_id="agent",
        run_at="2026-01-01T00:00:00Z",
    )

    due = scheduler.evaluate_due(now_iso="2026-01-01T00:00:01Z")

    assert due[0][0].schedule_id == schedule.schedule_id
    assert due[0][1].is_due is True


def test_enqueue_due_creates_job_and_completes_once_schedule(tmp_path) -> None:
    scheduler = service(tmp_path)
    schedule = scheduler.create_once_schedule(
        schedule_name="once",
        user_input="run",
        agent_id="agent",
        run_at="2026-01-01T00:00:00Z",
        requested_skill_id="skill:echo",
    )

    summary = scheduler.enqueue_due(now_iso="2026-01-01T00:00:01Z")
    job = scheduler.queue_service.job_store.get(summary["job_ids"][0])

    assert summary["enqueued_count"] == 1
    assert scheduler.schedule_store.get(schedule.schedule_id).status == "completed"
    assert job.job_attrs["schedule_id"] == schedule.schedule_id
    assert job.requested_skill_id == "skill:echo"


def test_interval_schedule_advances_next_run_at(tmp_path) -> None:
    scheduler = service(tmp_path)
    schedule = scheduler.create_interval_schedule(
        schedule_name="interval",
        user_input="run",
        agent_id="agent",
        interval_seconds=30,
    )
    scheduler.schedule_store.upsert(replace(schedule, next_run_at="2026-01-01T00:00:00Z"))

    summary = scheduler.enqueue_due(now_iso="2026-01-01T00:00:01Z")
    updated = scheduler.schedule_store.get(schedule.schedule_id)

    assert summary["enqueued_count"] == 1
    assert updated.status == "active"
    assert updated.next_run_at == "2026-01-01T00:00:31Z"
