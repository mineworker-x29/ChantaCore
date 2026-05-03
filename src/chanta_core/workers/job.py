from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.utility.time import utc_now_iso


def new_process_job_id() -> str:
    return f"process_job:{uuid4()}"


@dataclass(frozen=True)
class ProcessJob:
    job_id: str
    job_type: str
    status: str
    user_input: str
    process_instance_id: str | None
    session_id: str | None
    agent_id: str
    requested_skill_id: str | None
    priority: int
    retry_count: int
    max_retries: int
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)
    claimed_at: str | None = None
    claimed_by_worker_id: str | None = None
    completed_at: str | None = None
    failed_at: str | None = None
    last_error: str | None = None
    job_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "job_id": self.job_id,
            "job_type": self.job_type,
            "status": self.status,
            "user_input": self.user_input,
            "process_instance_id": self.process_instance_id,
            "session_id": self.session_id,
            "agent_id": self.agent_id,
            "requested_skill_id": self.requested_skill_id,
            "priority": self.priority,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "claimed_at": self.claimed_at,
            "claimed_by_worker_id": self.claimed_by_worker_id,
            "completed_at": self.completed_at,
            "failed_at": self.failed_at,
            "last_error": self.last_error,
            "job_attrs": self.job_attrs,
        }
