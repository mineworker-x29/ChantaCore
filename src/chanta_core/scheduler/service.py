from __future__ import annotations

from dataclasses import replace
from typing import Any

from chanta_core.scheduler.errors import ProcessScheduleNotFoundError
from chanta_core.scheduler.evaluator import ScheduleEvaluation, ScheduleEvaluator
from chanta_core.scheduler.schedule import ProcessSchedule, new_process_schedule_id
from chanta_core.scheduler.store import ProcessScheduleStore
from chanta_core.utility.time import utc_now_iso
from chanta_core.workers.queue import WorkerQueueService


class SchedulerService:
    def __init__(
        self,
        *,
        schedule_store: ProcessScheduleStore | None = None,
        evaluator: ScheduleEvaluator | None = None,
        queue_service: WorkerQueueService | None = None,
    ) -> None:
        self.schedule_store = schedule_store or ProcessScheduleStore()
        self.evaluator = evaluator or ScheduleEvaluator()
        self.queue_service = queue_service or WorkerQueueService()

    def create_once_schedule(
        self,
        *,
        schedule_name: str,
        user_input: str,
        agent_id: str,
        run_at: str,
        requested_skill_id: str | None = None,
        priority: int = 0,
        max_retries: int = 0,
        schedule_attrs: dict[str, Any] | None = None,
    ) -> ProcessSchedule:
        now = utc_now_iso()
        schedule = ProcessSchedule(
            schedule_id=new_process_schedule_id(),
            schedule_name=schedule_name,
            status="active",
            schedule_type="once",
            user_input=user_input,
            agent_id=agent_id,
            requested_skill_id=requested_skill_id,
            priority=priority,
            max_retries=max_retries,
            interval_seconds=None,
            run_at=run_at,
            last_run_at=None,
            next_run_at=run_at,
            created_at=now,
            updated_at=now,
            schedule_attrs=schedule_attrs or {},
        )
        self.schedule_store.upsert(schedule)
        return schedule

    def create_interval_schedule(
        self,
        *,
        schedule_name: str,
        user_input: str,
        agent_id: str,
        interval_seconds: int,
        requested_skill_id: str | None = None,
        priority: int = 0,
        max_retries: int = 0,
        schedule_attrs: dict[str, Any] | None = None,
    ) -> ProcessSchedule:
        now = utc_now_iso()
        schedule = ProcessSchedule(
            schedule_id=new_process_schedule_id(),
            schedule_name=schedule_name,
            status="active",
            schedule_type="interval",
            user_input=user_input,
            agent_id=agent_id,
            requested_skill_id=requested_skill_id,
            priority=priority,
            max_retries=max_retries,
            interval_seconds=interval_seconds,
            run_at=None,
            last_run_at=None,
            next_run_at=None,
            created_at=now,
            updated_at=now,
            schedule_attrs=schedule_attrs or {},
        )
        schedule = replace(
            schedule,
            next_run_at=self.evaluator.compute_next_run_at(schedule, from_iso=now),
        )
        self.schedule_store.upsert(schedule)
        return schedule

    def pause(self, schedule_id: str) -> ProcessSchedule:
        return self._set_status(schedule_id, "paused")

    def resume(self, schedule_id: str) -> ProcessSchedule:
        return self._set_status(schedule_id, "active")

    def cancel(self, schedule_id: str) -> ProcessSchedule:
        return self._set_status(schedule_id, "cancelled")

    def list_active(self) -> list[ProcessSchedule]:
        return self.schedule_store.list_active()

    def evaluate_due(
        self,
        now_iso: str | None = None,
    ) -> list[tuple[ProcessSchedule, ScheduleEvaluation]]:
        due: list[tuple[ProcessSchedule, ScheduleEvaluation]] = []
        for schedule in self.schedule_store.list_active():
            evaluation = self.evaluator.evaluate(schedule, now_iso=now_iso)
            if evaluation.is_due:
                due.append((schedule, evaluation))
        return due

    def enqueue_due(self, now_iso: str | None = None) -> dict[str, Any]:
        now = now_iso or utc_now_iso()
        active = self.schedule_store.list_active()
        due: list[tuple[ProcessSchedule, ScheduleEvaluation]] = []
        errors: list[dict[str, Any]] = []
        job_ids: list[str] = []
        schedule_ids: list[str] = []
        for schedule in active:
            evaluation = self.evaluator.evaluate(schedule, now_iso=now)
            if evaluation.is_due:
                due.append((schedule, evaluation))
        for schedule, _evaluation in due:
            try:
                job = self.queue_service.enqueue_process_run(
                    user_input=schedule.user_input,
                    agent_id=schedule.agent_id,
                    requested_skill_id=schedule.requested_skill_id,
                    priority=schedule.priority,
                    max_retries=schedule.max_retries,
                    job_attrs={
                        "schedule_id": schedule.schedule_id,
                        "schedule_name": schedule.schedule_name,
                        "scheduled": True,
                    },
                )
                job_ids.append(job.job_id)
                schedule_ids.append(schedule.schedule_id)
                self.schedule_store.upsert(self._after_enqueue(schedule, now))
            except Exception as error:
                errors.append({"schedule_id": schedule.schedule_id, "error": str(error)})
        return {
            "evaluated_count": len(active),
            "due_count": len(due),
            "enqueued_count": len(job_ids),
            "job_ids": job_ids,
            "schedule_ids": schedule_ids,
            "errors": errors,
        }

    def _after_enqueue(self, schedule: ProcessSchedule, now_iso: str) -> ProcessSchedule:
        if schedule.schedule_type == "once":
            return replace(
                schedule,
                status="completed",
                last_run_at=now_iso,
                updated_at=now_iso,
            )
        next_run_at = self.evaluator.compute_next_run_at(schedule, from_iso=now_iso)
        return replace(
            schedule,
            last_run_at=now_iso,
            next_run_at=next_run_at,
            updated_at=now_iso,
        )

    def _set_status(self, schedule_id: str, status: str) -> ProcessSchedule:
        schedule = self._require(schedule_id)
        updated = replace(schedule, status=status, updated_at=utc_now_iso())
        self.schedule_store.upsert(updated)
        return updated

    def _require(self, schedule_id: str) -> ProcessSchedule:
        schedule = self.schedule_store.get(schedule_id)
        if schedule is None:
            raise ProcessScheduleNotFoundError(f"Process schedule not found: {schedule_id}")
        return schedule
