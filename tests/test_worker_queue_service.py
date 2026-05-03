from chanta_core.workers import ProcessJobStore, WorkerQueueService


def queue(tmp_path) -> WorkerQueueService:
    return WorkerQueueService(ProcessJobStore(tmp_path / "jobs.jsonl"))


def test_enqueue_process_run_creates_queued_job(tmp_path) -> None:
    service = queue(tmp_path)

    job = service.enqueue_process_run(user_input="hello", agent_id="agent")

    assert job.status == "queued"
    assert job.job_type == "process_run"
    assert service.summary()["queued_count"] == 1


def test_claim_next_highest_priority_then_earliest(tmp_path) -> None:
    service = queue(tmp_path)
    low = service.enqueue_process_run(user_input="low", agent_id="agent", priority=0)
    high = service.enqueue_process_run(user_input="high", agent_id="agent", priority=5)

    claimed = service.claim_next("worker:one")

    assert claimed.job_id == high.job_id
    assert claimed.status == "claimed"
    assert service.job_store.get(low.job_id).status == "queued"


def test_mark_running_and_completed(tmp_path) -> None:
    service = queue(tmp_path)
    job = service.enqueue_process_run(user_input="run", agent_id="agent")
    claimed = service.claim_next("worker:one")
    running = service.mark_running(claimed.job_id, "worker:one")
    completed = service.mark_completed(running.job_id, "worker:one")

    assert running.status == "running"
    assert completed.status == "completed"
    assert service.summary()["completed_count"] == 1


def test_mark_failed_without_retry(tmp_path) -> None:
    service = queue(tmp_path)
    job = service.enqueue_process_run(user_input="run", agent_id="agent")
    claimed = service.claim_next("worker:one")
    running = service.mark_running(claimed.job_id, "worker:one")
    failed = service.mark_failed(running.job_id, "worker:one", "boom")

    assert failed.status == "failed"
    assert failed.last_error == "boom"


def test_mark_failed_with_retry_requeues(tmp_path) -> None:
    service = queue(tmp_path)
    job = service.enqueue_process_run(user_input="run", agent_id="agent", max_retries=1)
    claimed = service.claim_next("worker:one")
    running = service.mark_running(claimed.job_id, "worker:one")
    retried = service.mark_failed(running.job_id, "worker:one", "boom")

    assert retried.status == "queued"
    assert retried.retry_count == 1
    assert retried.claimed_by_worker_id is None


def test_cancel(tmp_path) -> None:
    service = queue(tmp_path)
    job = service.enqueue_process_run(user_input="run", agent_id="agent")
    cancelled = service.cancel(job.job_id, "not needed")

    assert cancelled.status == "cancelled"
    assert cancelled.job_attrs["cancel_reason"] == "not needed"
