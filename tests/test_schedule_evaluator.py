from dataclasses import replace

from chanta_core.scheduler import ScheduleEvaluator, SchedulerService


def make_once(tmp_path, run_at: str):
    return SchedulerService().create_once_schedule(
        schedule_name="once",
        user_input="run",
        agent_id="agent",
        run_at=run_at,
    )


def test_once_schedule_due_when_now_after_run_at() -> None:
    schedule = make_once(None, "2026-01-01T00:00:00Z")
    evaluation = ScheduleEvaluator().evaluate(schedule, now_iso="2026-01-01T00:00:01Z")

    assert evaluation.is_due is True
    assert evaluation.reason == "once_schedule_due"


def test_once_schedule_not_due_before_run_at() -> None:
    schedule = make_once(None, "2026-01-01T00:00:10Z")
    evaluation = ScheduleEvaluator().evaluate(schedule, now_iso="2026-01-01T00:00:01Z")

    assert evaluation.is_due is False


def test_interval_schedule_due_when_now_after_next_run_at() -> None:
    schedule = SchedulerService().create_interval_schedule(
        schedule_name="interval",
        user_input="run",
        agent_id="agent",
        interval_seconds=10,
    )
    schedule = replace(schedule, next_run_at="2026-01-01T00:00:00Z")

    evaluation = ScheduleEvaluator().evaluate(schedule, now_iso="2026-01-01T00:00:01Z")

    assert evaluation.is_due is True
    assert evaluation.reason == "interval_schedule_due"


def test_paused_schedule_not_due() -> None:
    schedule = replace(make_once(None, "2026-01-01T00:00:00Z"), status="paused")

    evaluation = ScheduleEvaluator().evaluate(schedule, now_iso="2026-01-01T00:00:01Z")

    assert evaluation.is_due is False
    assert evaluation.reason == "schedule_not_active"


def test_invalid_timestamp_handled_safely() -> None:
    schedule = make_once(None, "not-a-time")

    evaluation = ScheduleEvaluator().evaluate(schedule, now_iso="2026-01-01T00:00:01Z")

    assert evaluation.is_due is False
    assert evaluation.reason == "invalid_schedule_timestamp"


def test_next_run_at_computation() -> None:
    schedule = SchedulerService().create_interval_schedule(
        schedule_name="interval",
        user_input="run",
        agent_id="agent",
        interval_seconds=30,
    )

    assert ScheduleEvaluator().compute_next_run_at(
        schedule,
        from_iso="2026-01-01T00:00:00Z",
    ) == "2026-01-01T00:00:30Z"
