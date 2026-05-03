import json

from chanta_core.workers import ProcessJobStore, WorkerQueueService


def test_process_job_store_upsert_and_queries(tmp_path) -> None:
    store = ProcessJobStore(tmp_path / "jobs.jsonl")
    queue = WorkerQueueService(store)
    job = queue.enqueue_process_run(
        user_input="hello",
        agent_id="agent",
        priority=2,
        max_retries=1,
    )

    assert store.get(job.job_id).status == "queued"
    assert store.list_by_status("queued") == [job]
    assert store.list_queued()[0].job_id == job.job_id
    assert store.recent(1)[0].job_id == job.job_id
    assert store.load_all()


def test_process_job_store_status_updates_persist(tmp_path) -> None:
    store = ProcessJobStore(tmp_path / "jobs.jsonl")
    queue = WorkerQueueService(store)
    job = queue.enqueue_process_run(user_input="run", agent_id="agent")
    claimed = queue.claim_next("worker:test")
    running = queue.mark_running(claimed.job_id, "worker:test")
    completed = queue.mark_completed(running.job_id, "worker:test", "process_instance:done")

    reloaded = ProcessJobStore(tmp_path / "jobs.jsonl")
    assert reloaded.get(job.job_id).status == "completed"
    assert reloaded.get(job.job_id).process_instance_id == "process_instance:done"
    assert reloaded.list_by_status("completed")[0].job_id == job.job_id


def test_process_job_store_invalid_jsonl_row_skipped(tmp_path) -> None:
    path = tmp_path / "jobs.jsonl"
    path.write_text("{bad json}\n", encoding="utf-8")

    assert ProcessJobStore(path).load_all() == []


def test_process_job_store_save_snapshot(tmp_path) -> None:
    store = ProcessJobStore(tmp_path / "jobs.jsonl")
    queue = WorkerQueueService(store)
    job = queue.enqueue_process_run(user_input="run", agent_id="agent")
    store.save_snapshot([job])

    raw = json.loads((tmp_path / "process_jobs_state.json").read_text(encoding="utf-8"))
    assert raw[0]["job_id"] == job.job_id
