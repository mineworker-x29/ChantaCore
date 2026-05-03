from dataclasses import replace

from chanta_core.scheduler import ProcessScheduleStore, SchedulerService


def test_schedule_store_upsert_load_get_and_status_lists(tmp_path) -> None:
    store = ProcessScheduleStore(tmp_path / "schedules.jsonl")
    service = SchedulerService(schedule_store=store)
    schedule = service.create_once_schedule(
        schedule_name="once",
        user_input="run",
        agent_id="agent",
        run_at="2026-01-01T00:00:00Z",
    )

    assert store.get(schedule.schedule_id).schedule_name == "once"
    assert store.list_active()[0].schedule_id == schedule.schedule_id
    assert store.list_by_status("active")[0].schedule_id == schedule.schedule_id
    assert store.recent(1)[0].schedule_id == schedule.schedule_id
    assert store.load_all()


def test_schedule_store_state_persists(tmp_path) -> None:
    store = ProcessScheduleStore(tmp_path / "schedules.jsonl")
    service = SchedulerService(schedule_store=store)
    schedule = service.create_once_schedule(
        schedule_name="once",
        user_input="run",
        agent_id="agent",
        run_at="2026-01-01T00:00:00Z",
    )
    store.upsert(replace(schedule, status="paused"))

    reloaded = ProcessScheduleStore(tmp_path / "schedules.jsonl")
    assert reloaded.get(schedule.schedule_id).status == "paused"


def test_schedule_store_invalid_jsonl_row_skipped(tmp_path) -> None:
    path = tmp_path / "schedules.jsonl"
    path.write_text("{bad json}\n", encoding="utf-8")

    assert ProcessScheduleStore(path).load_all() == []
