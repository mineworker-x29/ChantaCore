from __future__ import annotations

from dataclasses import replace
from typing import Any

from chanta_core.utility.time import utc_now_iso
from chanta_core.workers.errors import ProcessJobClaimError, ProcessJobNotFoundError
from chanta_core.workers.job import ProcessJob, new_process_job_id
from chanta_core.workers.store import ProcessJobStore


class WorkerQueueService:
    def __init__(self, job_store: ProcessJobStore | None = None) -> None:
        self.job_store = job_store or ProcessJobStore()

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
        job = ProcessJob(
            job_id=new_process_job_id(),
            job_type="process_run",
            status="queued",
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
        self.job_store.upsert(job)
        return job

    def claim_next(self, worker_id: str) -> ProcessJob | None:
        queued = self.job_store.list_queued(limit=1)
        if not queued:
            return None
        now = utc_now_iso()
        job = replace(
            queued[0],
            status="claimed",
            claimed_by_worker_id=worker_id,
            claimed_at=now,
            updated_at=now,
        )
        self.job_store.upsert(job)
        return job

    def mark_running(self, job_id: str, worker_id: str) -> ProcessJob:
        job = self._require_claimed_or_running(job_id, worker_id)
        updated = replace(job, status="running", updated_at=utc_now_iso())
        self.job_store.upsert(updated)
        return updated

    def mark_completed(
        self,
        job_id: str,
        worker_id: str,
        process_instance_id: str | None = None,
    ) -> ProcessJob:
        job = self._require_claimed_or_running(job_id, worker_id)
        now = utc_now_iso()
        updated = replace(
            job,
            status="completed",
            process_instance_id=process_instance_id or job.process_instance_id,
            completed_at=now,
            failed_at=None,
            updated_at=now,
        )
        self.job_store.upsert(updated)
        return updated

    def mark_failed(self, job_id: str, worker_id: str, error: str) -> ProcessJob:
        job = self._require_claimed_or_running(job_id, worker_id)
        now = utc_now_iso()
        if job.retry_count < job.max_retries:
            updated = replace(
                job,
                status="queued",
                retry_count=job.retry_count + 1,
                updated_at=now,
                last_error=error,
                claimed_at=None,
                claimed_by_worker_id=None,
            )
        else:
            updated = replace(
                job,
                status="failed",
                failed_at=now,
                updated_at=now,
                last_error=error,
            )
        self.job_store.upsert(updated)
        return updated

    def cancel(self, job_id: str, reason: str) -> ProcessJob:
        job = self._require(job_id)
        now = utc_now_iso()
        attrs = dict(job.job_attrs)
        attrs["cancel_reason"] = reason
        updated = replace(
            job,
            status="cancelled",
            updated_at=now,
            last_error=reason,
            job_attrs=attrs,
        )
        self.job_store.upsert(updated)
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

    def _require_claimed_or_running(self, job_id: str, worker_id: str) -> ProcessJob:
        job = self._require(job_id)
        if job.claimed_by_worker_id != worker_id:
            raise ProcessJobClaimError(
                f"Process job {job_id} is not claimed by worker {worker_id}."
            )
        if job.status not in {"claimed", "running"}:
            raise ProcessJobClaimError(
                f"Process job {job_id} is not claimed/running: {job.status}."
            )
        return job
