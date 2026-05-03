from __future__ import annotations

from chanta_core.utility.time import utc_now_iso
from chanta_core.workers import ProcessJob, ProcessJobStateMachine
from chanta_core.workers.fsm import (
    CLAIM_PROCESS_JOB,
    COMPLETE_WORKER_JOB,
    ENQUEUE_PROCESS_JOB,
    START_WORKER_JOB,
)


def make_job() -> ProcessJob:
    now = utc_now_iso()
    return ProcessJob(
        job_id="process_job:script",
        job_type="process_run",
        status="new",
        user_input="run",
        process_instance_id=None,
        session_id=None,
        agent_id="chanta_core_default",
        requested_skill_id=None,
        priority=0,
        retry_count=0,
        max_retries=0,
        created_at=now,
        updated_at=now,
    )


def main() -> None:
    fsm = ProcessJobStateMachine()
    queued = fsm.transition(make_job(), ENQUEUE_PROCESS_JOB)
    claimed = fsm.transition(queued, CLAIM_PROCESS_JOB, worker_id="worker:script")
    running = fsm.transition(claimed, START_WORKER_JOB, worker_id="worker:script")
    completed = fsm.transition(running, COMPLETE_WORKER_JOB, worker_id="worker:script")
    print(f"statuses={[queued.status, claimed.status, running.status, completed.status]}")
    try:
        fsm.transition(completed, START_WORKER_JOB, worker_id="worker:script")
    except Exception as error:
        print(f"invalid_transition_error={type(error).__name__}")


if __name__ == "__main__":
    main()
