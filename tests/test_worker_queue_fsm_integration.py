import pytest

from chanta_core.workers import (
    ProcessJobInvalidTransitionError,
    ProcessJobStore,
    WorkerQueueService,
)


def queue(tmp_path) -> WorkerQueueService:
    return WorkerQueueService(ProcessJobStore(tmp_path / "jobs.jsonl"))


def test_queue_service_uses_fsm_for_normal_lifecycle(tmp_path) -> None:
    service = queue(tmp_path)
    job = service.enqueue_process_run(user_input="run", agent_id="agent")
    claimed = service.claim_next("worker:one")
    running = service.mark_running(claimed.job_id, "worker:one")
    completed = service.mark_completed(running.job_id, "worker:one")

    assert job.status == "queued"
    assert claimed.status == "claimed"
    assert running.status == "running"
    assert completed.status == "completed"
    assert completed.job_attrs["last_transition"]["event_activity"] == "complete_worker_job"


def test_queue_service_retry_behavior_uses_fsm(tmp_path) -> None:
    service = queue(tmp_path)
    job = service.enqueue_process_run(
        user_input="run",
        agent_id="agent",
        max_retries=1,
    )
    claimed = service.claim_next("worker:one")
    running = service.mark_running(claimed.job_id, "worker:one")
    retried = service.mark_failed(running.job_id, "worker:one", "boom")

    assert retried.status == "queued"
    assert retried.retry_count == 1
    assert retried.claimed_by_worker_id is None
    assert retried.last_error == "boom"


def test_queue_service_final_failure_uses_fsm(tmp_path) -> None:
    service = queue(tmp_path)
    job = service.enqueue_process_run(user_input="run", agent_id="agent")
    claimed = service.claim_next("worker:one")
    running = service.mark_running(claimed.job_id, "worker:one")
    failed = service.mark_failed(running.job_id, "worker:one", "boom")

    assert failed.status == "failed"
    assert failed.last_error == "boom"


def test_queue_service_rejects_invalid_direct_transition(tmp_path) -> None:
    service = queue(tmp_path)
    job = service.enqueue_process_run(user_input="run", agent_id="agent")
    claimed = service.claim_next("worker:one")

    with pytest.raises(ProcessJobInvalidTransitionError):
        service.mark_completed(claimed.job_id, "worker:one")


def test_queue_service_cancel_queued_job(tmp_path) -> None:
    service = queue(tmp_path)
    job = service.enqueue_process_run(user_input="run", agent_id="agent")
    cancelled = service.cancel(job.job_id, "not needed")

    assert cancelled.status == "cancelled"
    assert cancelled.job_attrs["cancel_reason"] == "not needed"
