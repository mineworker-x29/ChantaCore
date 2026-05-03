from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any

from chanta_core.utility.time import utc_now_iso
from chanta_core.workers.errors import ProcessJobInvalidTransitionError
from chanta_core.workers.job import ProcessJob

JOB_STATUS_QUEUED = "queued"
JOB_STATUS_CLAIMED = "claimed"
JOB_STATUS_RUNNING = "running"
JOB_STATUS_COMPLETED = "completed"
JOB_STATUS_FAILED = "failed"
JOB_STATUS_CANCELLED = "cancelled"

ENQUEUE_PROCESS_JOB = "enqueue_process_job"
CLAIM_PROCESS_JOB = "claim_process_job"
START_WORKER_JOB = "start_worker_job"
COMPLETE_WORKER_JOB = "complete_worker_job"
FAIL_WORKER_JOB = "fail_worker_job"
RETRY_PROCESS_JOB = "retry_process_job"
CANCEL_PROCESS_JOB = "cancel_process_job"


@dataclass(frozen=True)
class ProcessJobStateTransition:
    from_status: str | None
    event_activity: str
    to_status: str
    requires_worker: bool
    transition_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "from_status": self.from_status,
            "event_activity": self.event_activity,
            "to_status": self.to_status,
            "requires_worker": self.requires_worker,
            "transition_attrs": self.transition_attrs,
        }


class ProcessJobStateMachine:
    def __init__(
        self,
        transitions: list[ProcessJobStateTransition] | None = None,
    ) -> None:
        self.transitions = transitions or default_process_job_transitions()

    def allowed_transitions(
        self,
        status: str | None,
    ) -> list[ProcessJobStateTransition]:
        normalized = self._normalize_status(status)
        return [
            transition
            for transition in self.transitions
            if transition.from_status == normalized
        ]

    def can_transition(
        self,
        current_status: str | None,
        event_activity: str,
    ) -> bool:
        return self._find_transition(current_status, event_activity) is not None

    def transition(
        self,
        job: ProcessJob,
        event_activity: str,
        *,
        worker_id: str | None = None,
        error: str | None = None,
        process_instance_id: str | None = None,
        now_iso: str | None = None,
    ) -> ProcessJob:
        current_status = self._status_for_event(job.status, event_activity)
        transition = self._find_transition(current_status, event_activity)
        if transition is None:
            raise ProcessJobInvalidTransitionError(
                f"Invalid process job transition: {current_status} + {event_activity}"
            )
        if transition.requires_worker and not worker_id:
            raise ProcessJobInvalidTransitionError(
                f"Process job transition requires worker_id: {event_activity}"
            )

        now = now_iso or utc_now_iso()
        attrs = dict(job.job_attrs)
        attrs["last_transition"] = {
            "from_status": transition.from_status,
            "event_activity": event_activity,
            "to_status": transition.to_status,
            "worker_id": worker_id,
            "transitioned_at": now,
        }
        updates: dict[str, Any] = {
            "status": transition.to_status,
            "updated_at": now,
            "job_attrs": attrs,
        }

        if event_activity == CLAIM_PROCESS_JOB:
            updates["claimed_by_worker_id"] = worker_id
            updates["claimed_at"] = now
        elif event_activity == START_WORKER_JOB:
            updates["failed_at"] = None
        elif event_activity == COMPLETE_WORKER_JOB:
            updates["completed_at"] = now
            updates["failed_at"] = None
            if process_instance_id:
                updates["process_instance_id"] = process_instance_id
        elif event_activity == FAIL_WORKER_JOB:
            updates["failed_at"] = now
            updates["last_error"] = error
        elif event_activity == RETRY_PROCESS_JOB:
            updates["retry_count"] = job.retry_count + 1
            updates["last_error"] = error
            updates["claimed_at"] = None
            updates["claimed_by_worker_id"] = None
            updates["failed_at"] = None
        elif event_activity == CANCEL_PROCESS_JOB:
            updates["last_error"] = error
            if error:
                attrs["cancel_reason"] = error
                updates["job_attrs"] = attrs

        return replace(job, **updates)

    def _find_transition(
        self,
        current_status: str | None,
        event_activity: str,
    ) -> ProcessJobStateTransition | None:
        normalized = self._normalize_status(current_status)
        for transition in self.transitions:
            if (
                transition.from_status == normalized
                and transition.event_activity == event_activity
            ):
                return transition
        return None

    @staticmethod
    def _normalize_status(status: str | None) -> str | None:
        if status in {"", "new"}:
            return None
        return status

    @staticmethod
    def _status_for_event(status: str | None, event_activity: str) -> str | None:
        if event_activity == ENQUEUE_PROCESS_JOB:
            return ProcessJobStateMachine._normalize_status(status)
        return status


def default_process_job_transitions() -> list[ProcessJobStateTransition]:
    return [
        ProcessJobStateTransition(None, ENQUEUE_PROCESS_JOB, JOB_STATUS_QUEUED, False),
        ProcessJobStateTransition(
            JOB_STATUS_QUEUED,
            CLAIM_PROCESS_JOB,
            JOB_STATUS_CLAIMED,
            True,
        ),
        ProcessJobStateTransition(
            JOB_STATUS_CLAIMED,
            START_WORKER_JOB,
            JOB_STATUS_RUNNING,
            True,
        ),
        ProcessJobStateTransition(
            JOB_STATUS_RUNNING,
            COMPLETE_WORKER_JOB,
            JOB_STATUS_COMPLETED,
            True,
        ),
        ProcessJobStateTransition(
            JOB_STATUS_RUNNING,
            FAIL_WORKER_JOB,
            JOB_STATUS_FAILED,
            True,
        ),
        ProcessJobStateTransition(
            JOB_STATUS_QUEUED,
            CANCEL_PROCESS_JOB,
            JOB_STATUS_CANCELLED,
            False,
        ),
        ProcessJobStateTransition(
            JOB_STATUS_CLAIMED,
            CANCEL_PROCESS_JOB,
            JOB_STATUS_CANCELLED,
            False,
        ),
        ProcessJobStateTransition(
            JOB_STATUS_FAILED,
            RETRY_PROCESS_JOB,
            JOB_STATUS_QUEUED,
            False,
        ),
        ProcessJobStateTransition(
            JOB_STATUS_RUNNING,
            RETRY_PROCESS_JOB,
            JOB_STATUS_QUEUED,
            True,
        ),
    ]
