from __future__ import annotations

from typing import Any

from chanta_core.utility.time import utc_now_iso
from chanta_core.workers.errors import ProcessJobClaimError, ProcessJobNotFoundError
from chanta_core.workers.fsm import (
    CANCEL_PROCESS_JOB,
    CLAIM_PROCESS_JOB,
    COMPLETE_WORKER_JOB,
    ENQUEUE_PROCESS_JOB,
    FAIL_WORKER_JOB,
    RETRY_PROCESS_JOB,
    START_WORKER_JOB,
    ProcessJobStateMachine,
)
from chanta_core.workers.job import ProcessJob, new_process_job_id
from chanta_core.workers.store import ProcessJobStore
from chanta_core.workers.worker import Worker


class WorkerQueueService:
    def __init__(
        self,
        job_store: ProcessJobStore | None = None,
        *,
        state_machine: ProcessJobStateMachine | None = None,
        trace_service=None,
    ) -> None:
        self.job_store = job_store or ProcessJobStore()
        self.state_machine = state_machine or ProcessJobStateMachine()
        self.trace_service = trace_service

    def enqueue_process_run(
        self,
        *,
        user_input: str,
        agent_id: str,
        session_id: str | None = None,
        process_instance_id: str | None = None,
        requested_skill_id: str | None = None,
        priority: int = 0,
        max_retries: int = 0,
        job_attrs: dict[str, Any] | None = None,
    ) -> ProcessJob:
        now = utc_now_iso()
        pending = ProcessJob(
            job_id=new_process_job_id(),
            job_type="process_run",
            status="new",
            user_input=user_input,
            process_instance_id=process_instance_id,
            session_id=session_id,
            agent_id=agent_id,
            requested_skill_id=requested_skill_id,
            priority=priority,
            retry_count=0,
            max_retries=max_retries,
            created_at=now,
            updated_at=now,
            job_attrs=job_attrs or {},
        )
        job = self.state_machine.transition(
            pending,
            ENQUEUE_PROCESS_JOB,
            now_iso=now,
        )
        self.job_store.upsert(job)
        self._record_transition(ENQUEUE_PROCESS_JOB, pending, job)
        return job

    def claim_next(self, worker_id: str) -> ProcessJob | None:
        queued = self.job_store.list_queued(limit=1)
        if not queued:
            return None
        before = queued[0]
        job = self.state_machine.transition(
            before,
            CLAIM_PROCESS_JOB,
            worker_id=worker_id,
        )
        self.job_store.upsert(job)
        self._record_transition(CLAIM_PROCESS_JOB, before, job, worker_id=worker_id)
        return job

    def mark_running(self, job_id: str, worker_id: str) -> ProcessJob:
        job = self._require_claimed_by_worker(job_id, worker_id)
        updated = self.state_machine.transition(
            job,
            START_WORKER_JOB,
            worker_id=worker_id,
        )
        self.job_store.upsert(updated)
        self._record_transition(START_WORKER_JOB, job, updated, worker_id=worker_id)
        return updated

    def mark_completed(
        self,
        job_id: str,
        worker_id: str,
        process_instance_id: str | None = None,
    ) -> ProcessJob:
        job = self._require_claimed_by_worker(job_id, worker_id)
        updated = self.state_machine.transition(
            job,
            COMPLETE_WORKER_JOB,
            worker_id=worker_id,
            process_instance_id=process_instance_id or job.process_instance_id,
        )
        self.job_store.upsert(updated)
        self._record_transition(COMPLETE_WORKER_JOB, job, updated, worker_id=worker_id)
        return updated

    def mark_failed(self, job_id: str, worker_id: str, error: str) -> ProcessJob:
        job = self._require_claimed_by_worker(job_id, worker_id)
        if job.retry_count < job.max_retries:
            updated = self.state_machine.transition(
                job,
                RETRY_PROCESS_JOB,
                worker_id=worker_id,
                error=error,
            )
            event_activity = RETRY_PROCESS_JOB
        else:
            updated = self.state_machine.transition(
                job,
                FAIL_WORKER_JOB,
                worker_id=worker_id,
                error=error,
            )
            event_activity = FAIL_WORKER_JOB
        self.job_store.upsert(updated)
        self._record_transition(
            event_activity,
            job,
            updated,
            worker_id=worker_id,
            error=error,
        )
        return updated

    def cancel(self, job_id: str, reason: str) -> ProcessJob:
        job = self._require(job_id)
        updated = self.state_machine.transition(
            job,
            CANCEL_PROCESS_JOB,
            error=reason,
        )
        self.job_store.upsert(updated)
        self._record_transition(CANCEL_PROCESS_JOB, job, updated, error=reason)
        return updated

    def summary(self) -> dict[str, Any]:
        counts: dict[str, int] = {}
        for job in self.job_store._state_by_id().values():
            counts[job.status] = counts.get(job.status, 0) + 1
        return {
            "job_count": sum(counts.values()),
            "counts_by_status": counts,
            "queued_count": counts.get("queued", 0),
            "running_count": counts.get("running", 0),
            "completed_count": counts.get("completed", 0),
            "failed_count": counts.get("failed", 0),
        }

    def _require(self, job_id: str) -> ProcessJob:
        job = self.job_store.get(job_id)
        if job is None:
            raise ProcessJobNotFoundError(f"Process job not found: {job_id}")
        return job

    def _require_claimed_by_worker(self, job_id: str, worker_id: str) -> ProcessJob:
        job = self._require(job_id)
        if job.claimed_by_worker_id != worker_id:
            raise ProcessJobClaimError(
                f"Process job {job_id} is not claimed by worker {worker_id}."
            )
        return job

    def _record_transition(
        self,
        event_activity: str,
        before: ProcessJob | None,
        after: ProcessJob,
        *,
        worker_id: str | None = None,
        error: str | None = None,
    ) -> None:
        if self.trace_service is None:
            return
        recorder = getattr(self.trace_service, "record_worker_lifecycle_event", None)
        if recorder is None:
            return
        worker = Worker(
            worker_id=worker_id or "worker:queue",
            worker_name=worker_id or "queue",
        )
        event_attrs = {
            "from_status": before.status if before is not None else None,
            "to_status": after.status,
            "job_id": after.job_id,
            "worker_id": worker_id,
            "retry_count": after.retry_count,
            "max_retries": after.max_retries,
            "transition_valid": True,
            "source": "worker_queue_fsm",
            "recorded_at": utc_now_iso(),
        }
        if error:
            event_attrs["error"] = error
        recorder(
            event_activity=event_activity,
            worker=worker,
            job=after,
            status=after.status,
            event_attrs=event_attrs,
        )
