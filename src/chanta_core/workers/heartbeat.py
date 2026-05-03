from __future__ import annotations

import json
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import uuid4

from chanta_core.utility.time import utc_now_iso


def new_worker_heartbeat_id() -> str:
    return f"worker_heartbeat:{uuid4()}"


@dataclass(frozen=True)
class WorkerHeartbeat:
    heartbeat_id: str
    worker_id: str
    job_id: str | None
    status: str
    emitted_at: str = field(default_factory=utc_now_iso)
    heartbeat_attrs: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        worker_id: str,
        job_id: str | None,
        status: str,
        heartbeat_attrs: dict[str, Any] | None = None,
    ) -> "WorkerHeartbeat":
        return cls(
            heartbeat_id=new_worker_heartbeat_id(),
            worker_id=worker_id,
            job_id=job_id,
            status=status,
            heartbeat_attrs=heartbeat_attrs or {},
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "heartbeat_id": self.heartbeat_id,
            "worker_id": self.worker_id,
            "job_id": self.job_id,
            "status": self.status,
            "emitted_at": self.emitted_at,
            "heartbeat_attrs": self.heartbeat_attrs,
        }


class WorkerHeartbeatStore:
    def __init__(self, path: str | Path = "data/workers/worker_heartbeats.jsonl") -> None:
        self.path = Path(path)

    def append(self, heartbeat: WorkerHeartbeat) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(heartbeat.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")

    def recent(self, limit: int = 20) -> list[WorkerHeartbeat]:
        if not self.path.exists():
            return []
        rows: list[WorkerHeartbeat] = []
        for line_number, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                rows.append(_heartbeat_from_dict(json.loads(line)))
            except Exception as error:
                warnings.warn(
                    f"Skipping invalid worker heartbeat JSONL row {line_number}: {error}",
                    RuntimeWarning,
                    stacklevel=2,
                )
        return rows[-max(0, limit) :]


def _heartbeat_from_dict(data: dict[str, Any]) -> WorkerHeartbeat:
    return WorkerHeartbeat(
        heartbeat_id=str(data["heartbeat_id"]),
        worker_id=str(data["worker_id"]),
        job_id=data.get("job_id"),
        status=str(data.get("status") or "unknown"),
        emitted_at=str(data.get("emitted_at") or ""),
        heartbeat_attrs=dict(data.get("heartbeat_attrs") or {}),
    )
