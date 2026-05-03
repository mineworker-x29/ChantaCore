from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.utility.time import utc_now_iso


def new_process_schedule_id() -> str:
    return f"process_schedule:{uuid4()}"


@dataclass(frozen=True)
class ProcessSchedule:
    schedule_id: str
    schedule_name: str
    status: str
    schedule_type: str
    user_input: str
    agent_id: str
    requested_skill_id: str | None
    priority: int
    max_retries: int
    interval_seconds: int | None
    run_at: str | None
    last_run_at: str | None
    next_run_at: str | None
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)
    schedule_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schedule_id": self.schedule_id,
            "schedule_name": self.schedule_name,
            "status": self.status,
            "schedule_type": self.schedule_type,
            "user_input": self.user_input,
            "agent_id": self.agent_id,
            "requested_skill_id": self.requested_skill_id,
            "priority": self.priority,
            "max_retries": self.max_retries,
            "interval_seconds": self.interval_seconds,
            "run_at": self.run_at,
            "last_run_at": self.last_run_at,
            "next_run_at": self.next_run_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "schedule_attrs": self.schedule_attrs,
        }
