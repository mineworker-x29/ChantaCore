from __future__ import annotations

from typing import Any, Callable

from chanta_core.runtime.loop import ProcessRunLoop
from chanta_core.utility.time import utc_now_iso
from chanta_core.workers.heartbeat import WorkerHeartbeat, WorkerHeartbeatStore
from chanta_core.workers.queue import WorkerQueueService
from chanta_core.workers.worker import Worker


class WorkerRunner:
    def __init__(
        self,
        *,
        worker: Worker | None = None,
        queue_service: WorkerQueueService | None = None,
        process_run_loop_factory: Callable[[], Any] | None = None,
        heartbeat_store: WorkerHeartbeatStore | None = None,
        trace_service=None,
    ) -> None:
        self.worker = worker or Worker()
        self.queue_service = queue_service or WorkerQueueService()
        self.process_run_loop_factory = process_run_loop_factory or ProcessRunLoop
        self.heartbeat_store = heartbeat_store or WorkerHeartbeatStore()
        self.trace_service = trace_service

    def run_once(self) -> dict[str, Any]:
        self.emit_heartbeat(None, "idle", {"stage": "before_claim"})
        job = self.queue_service.claim_next(self.worker.worker_id)
        if job is None:
            self._record("emit_worker_heartbeat", None, "idle", {"no_job": True})
            return {"status": "idle", "job": None}

        self._record("claim_process_job", job, "claimed")
        running = self.queue_service.mark_running(job.job_id, self.worker.worker_id)
        self._record("start_worker_job", running, "running")
        self.emit_heartbeat(running.job_id, "running")
        process_instance_id = running.process_instance_id or f"process_instance:{running.job_id}"
        session_id = running.session_id or f"worker-session-{running.job_id}"

        try:
            loop = self.process_run_loop_factory()
            result = loop.run(
                process_instance_id=process_instance_id,
                session_id=session_id,
                agent_id=running.agent_id,
                user_input=running.user_input,
                system_prompt=str(running.job_attrs.get("system_prompt") or "")
                if running.job_attrs.get("system_prompt") is not None
                else None,
                skill_id=running.requested_skill_id,
            )
            if getattr(result, "status", None) == "failed":
                raise RuntimeError(str(getattr(result, "result_attrs", {}).get("error") or "Process run failed"))
            completed = self.queue_service.mark_completed(
                running.job_id,
                self.worker.worker_id,
                process_instance_id=getattr(result, "process_instance_id", process_instance_id),
            )
            self.emit_heartbeat(completed.job_id, "completed")
            self._record("complete_worker_job", completed, "completed")
            return {
                "status": "completed",
                "job": completed.to_dict(),
                "process_result": result.to_dict() if hasattr(result, "to_dict") else {},
            }
        except Exception as error:
            failed_or_requeued = self.queue_service.mark_failed(
                running.job_id,
                self.worker.worker_id,
                str(error),
            )
            status = "retried" if failed_or_requeued.status == "queued" else "failed"
            self.emit_heartbeat(failed_or_requeued.job_id, status, {"error": str(error)})
            self._record("fail_worker_job", failed_or_requeued, status, {"error": str(error)})
            return {"status": status, "job": failed_or_requeued.to_dict(), "error": str(error)}

    def emit_heartbeat(
        self,
        job_id: str | None,
        status: str,
        attrs: dict[str, Any] | None = None,
    ) -> WorkerHeartbeat:
        heartbeat = WorkerHeartbeat.create(
            worker_id=self.worker.worker_id,
            job_id=job_id,
            status=status,
            heartbeat_attrs=attrs or {},
        )
        self.heartbeat_store.append(heartbeat)
        self._record("emit_worker_heartbeat", None, status, heartbeat.to_dict())
        return heartbeat

    def _record(
        self,
        event_activity: str,
        job,
        status: str,
        attrs: dict[str, Any] | None = None,
    ) -> None:
        if self.trace_service is None:
            return
        recorder = getattr(self.trace_service, "record_worker_lifecycle_event", None)
        if recorder is None:
            return
        recorder(
            event_activity=event_activity,
            worker=self.worker,
            job=job,
            status=status,
            event_attrs={**(attrs or {}), "recorded_at": utc_now_iso()},
        )
