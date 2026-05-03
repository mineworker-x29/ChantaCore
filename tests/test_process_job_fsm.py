import pytest

from chanta_core.utility.time import utc_now_iso
from chanta_core.workers import (
    ProcessJob,
    ProcessJobInvalidTransitionError,
    ProcessJobStateMachine,
)
from chanta_core.workers.fsm import (
    CANCEL_PROCESS_JOB,
    CLAIM_PROCESS_JOB,
    COMPLETE_WORKER_JOB,
    ENQUEUE_PROCESS_JOB,
    FAIL_WORKER_JOB,
    RETRY_PROCESS_JOB,
    START_WORKER_JOB,
)


def make_job(status: str = "new", retry_count: int = 0, max_retries: int = 1) -> ProcessJob:
    now = utc_now_iso()
    return ProcessJob(
        job_id="process_job:test",
        job_type="process_run",
        status=status,
        user_input="run",
        process_instance_id=None,
        session_id=None,
        agent_id="agent",
        requested_skill_id=None,
        priority=0,
        retry_count=retry_count,
        max_retries=max_retries,
        created_at=now,
        updated_at=now,
    )


def test_allowed_process_job_transitions() -> None:
    fsm = ProcessJobStateMachine()

    queued = fsm.transition(make_job(), ENQUEUE_PROCESS_JOB)
    claimed = fsm.transition(queued, CLAIM_PROCESS_JOB, worker_id="worker:one")
    running = fsm.transition(claimed, START_WORKER_JOB, worker_id="worker:one")
    completed = fsm.transition(running, COMPLETE_WORKER_JOB, worker_id="worker:one")

    assert queued.status == "queued"
    assert claimed.status == "claimed"
    assert claimed.claimed_by_worker_id == "worker:one"
    assert running.status == "running"
    assert completed.status == "completed"


def test_failed_retry_and_cancel_transitions() -> None:
    fsm = ProcessJobStateMachine()
    queued = fsm.transition(make_job(), ENQUEUE_PROCESS_JOB)
    cancelled = fsm.transition(queued, CANCEL_PROCESS_JOB, error="not needed")

    running = fsm.transition(
        fsm.transition(queued, CLAIM_PROCESS_JOB, worker_id="worker:one"),
        START_WORKER_JOB,
        worker_id="worker:one",
    )
    failed = fsm.transition(running, FAIL_WORKER_JOB, worker_id="worker:one", error="boom")
    retried = fsm.transition(failed, RETRY_PROCESS_JOB, error="retry")

    assert cancelled.status == "cancelled"
    assert cancelled.job_attrs["cancel_reason"] == "not needed"
    assert failed.status == "failed"
    assert failed.last_error == "boom"
    assert retried.status == "queued"
    assert retried.retry_count == 1


@pytest.mark.parametrize(
    ("status", "activity"),
    [
        ("queued", COMPLETE_WORKER_JOB),
        ("completed", START_WORKER_JOB),
        ("cancelled", CLAIM_PROCESS_JOB),
        ("failed", COMPLETE_WORKER_JOB),
    ],
)
def test_invalid_transitions_are_rejected(status: str, activity: str) -> None:
    with pytest.raises(ProcessJobInvalidTransitionError):
        ProcessJobStateMachine().transition(
            make_job(status=status),
            activity,
            worker_id="worker:one",
        )


def test_worker_required_transitions_fail_without_worker_id() -> None:
    with pytest.raises(ProcessJobInvalidTransitionError):
        ProcessJobStateMachine().transition(make_job(status="queued"), CLAIM_PROCESS_JOB)
