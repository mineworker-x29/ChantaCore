from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.utility.time import utc_now_iso


def new_worker_id() -> str:
    return f"worker:{uuid4()}"


@dataclass(frozen=True)
class Worker:
    worker_id: str = field(default_factory=new_worker_id)
    worker_name: str = "local_worker"
    status: str = "idle"
    created_at: str = field(default_factory=utc_now_iso)
    last_heartbeat_at: str | None = None
    worker_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "worker_id": self.worker_id,
            "worker_name": self.worker_name,
            "status": self.status,
            "created_at": self.created_at,
            "last_heartbeat_at": self.last_heartbeat_at,
            "worker_attrs": self.worker_attrs,
        }
