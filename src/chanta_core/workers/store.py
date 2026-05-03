from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Any

from chanta_core.workers.job import ProcessJob


class ProcessJobStore:
    def __init__(
        self,
        path: str | Path = "data/workers/process_jobs.jsonl",
        *,
        state_path: str | Path | None = None,
    ) -> None:
        self.path = Path(path)
        self.state_path = Path(state_path) if state_path else self.path.with_name(
            "process_jobs_state.json"
        )

    def append(self, job: ProcessJob) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(job.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")

    def load_all(self) -> list[ProcessJob]:
        rows: list[ProcessJob] = []
        if not self.path.exists():
            return rows
        for line_number, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                rows.append(_job_from_dict(json.loads(line)))
            except Exception as error:
                warnings.warn(
                    f"Skipping invalid process job JSONL row {line_number}: {error}",
                    RuntimeWarning,
                    stacklevel=2,
                )
        return rows

    def recent(self, limit: int = 20) -> list[ProcessJob]:
        return self.load_all()[-max(0, limit) :]

    def get(self, job_id: str) -> ProcessJob | None:
        return self._state_by_id().get(job_id)

    def list_by_status(self, status: str) -> list[ProcessJob]:
        return [job for job in self._state_by_id().values() if job.status == status]

    def list_queued(self, limit: int = 20) -> list[ProcessJob]:
        queued = self.list_by_status("queued")
        queued.sort(key=lambda job: (-job.priority, job.created_at, job.job_id))
        return queued[: max(0, limit)]

    def save_snapshot(self, jobs: list[ProcessJob]) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        payload = [job.to_dict() for job in sorted(jobs, key=lambda item: item.job_id)]
        self.state_path.write_text(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2),
            encoding="utf-8",
        )

    def upsert(self, job: ProcessJob) -> None:
        state = self._state_by_id()
        state[job.job_id] = job
        self.save_snapshot(list(state.values()))
        self.append(job)

    def _state_by_id(self) -> dict[str, ProcessJob]:
        if self.state_path.exists():
            try:
                raw = json.loads(self.state_path.read_text(encoding="utf-8"))
                if isinstance(raw, list):
                    return {
                        job.job_id: job
                        for job in (_job_from_dict(item) for item in raw if isinstance(item, dict))
                    }
            except Exception as error:
                warnings.warn(
                    f"Skipping invalid process job state snapshot: {error}",
                    RuntimeWarning,
                    stacklevel=2,
                )
        state: dict[str, ProcessJob] = {}
        for job in self.load_all():
            state[job.job_id] = job
        if state:
            self.save_snapshot(list(state.values()))
        return state


def _job_from_dict(data: dict[str, Any]) -> ProcessJob:
    return ProcessJob(
        job_id=str(data["job_id"]),
        job_type=str(data.get("job_type") or "process_run"),
        status=str(data.get("status") or "queued"),
        user_input=str(data.get("user_input") or ""),
        process_instance_id=data.get("process_instance_id"),
        session_id=data.get("session_id"),
        agent_id=str(data.get("agent_id") or "chanta_core_default"),
        requested_skill_id=data.get("requested_skill_id"),
        priority=int(data.get("priority") or 0),
        retry_count=int(data.get("retry_count") or 0),
        max_retries=int(data.get("max_retries") or 0),
        created_at=str(data.get("created_at") or ""),
        updated_at=str(data.get("updated_at") or ""),
        claimed_at=data.get("claimed_at"),
        claimed_by_worker_id=data.get("claimed_by_worker_id"),
        completed_at=data.get("completed_at"),
        failed_at=data.get("failed_at"),
        last_error=data.get("last_error"),
        job_attrs=dict(data.get("job_attrs") or {}),
    )
