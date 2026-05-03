from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Any

from chanta_core.scheduler.schedule import ProcessSchedule


class ProcessScheduleStore:
    def __init__(
        self,
        path: str | Path = "data/scheduler/process_schedules.jsonl",
        *,
        state_path: str | Path | None = None,
    ) -> None:
        self.path = Path(path)
        self.state_path = Path(state_path) if state_path else self.path.with_name(
            "process_schedules_state.json"
        )

    def append(self, schedule: ProcessSchedule) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(schedule.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")

    def load_all(self) -> list[ProcessSchedule]:
        if not self.path.exists():
            return []
        schedules: list[ProcessSchedule] = []
        for line_number, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                schedules.append(_schedule_from_dict(json.loads(line)))
            except Exception as error:
                warnings.warn(
                    f"Skipping invalid process schedule JSONL row {line_number}: {error}",
                    RuntimeWarning,
                    stacklevel=2,
                )
        return schedules

    def recent(self, limit: int = 20) -> list[ProcessSchedule]:
        return self.load_all()[-max(0, limit) :]

    def get(self, schedule_id: str) -> ProcessSchedule | None:
        return self._state_by_id().get(schedule_id)

    def list_by_status(self, status: str) -> list[ProcessSchedule]:
        return [item for item in self._state_by_id().values() if item.status == status]

    def list_active(self) -> list[ProcessSchedule]:
        items = self.list_by_status("active")
        return sorted(items, key=lambda item: (item.next_run_at or item.run_at or item.created_at, item.schedule_id))

    def upsert(self, schedule: ProcessSchedule) -> None:
        state = self._state_by_id()
        state[schedule.schedule_id] = schedule
        self.save_snapshot(list(state.values()))
        self.append(schedule)

    def save_snapshot(self, schedules: list[ProcessSchedule]) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        payload = [item.to_dict() for item in sorted(schedules, key=lambda item: item.schedule_id)]
        self.state_path.write_text(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2),
            encoding="utf-8",
        )

    def _state_by_id(self) -> dict[str, ProcessSchedule]:
        if self.state_path.exists():
            try:
                raw = json.loads(self.state_path.read_text(encoding="utf-8"))
                if isinstance(raw, list):
                    return {
                        schedule.schedule_id: schedule
                        for schedule in (
                            _schedule_from_dict(item) for item in raw if isinstance(item, dict)
                        )
                    }
            except Exception as error:
                warnings.warn(
                    f"Skipping invalid process schedule state snapshot: {error}",
                    RuntimeWarning,
                    stacklevel=2,
                )
        state: dict[str, ProcessSchedule] = {}
        for schedule in self.load_all():
            state[schedule.schedule_id] = schedule
        if state:
            self.save_snapshot(list(state.values()))
        return state


def _schedule_from_dict(data: dict[str, Any]) -> ProcessSchedule:
    return ProcessSchedule(
        schedule_id=str(data["schedule_id"]),
        schedule_name=str(data.get("schedule_name") or ""),
        status=str(data.get("status") or "active"),
        schedule_type=str(data.get("schedule_type") or "once"),
        user_input=str(data.get("user_input") or ""),
        agent_id=str(data.get("agent_id") or "chanta_core_default"),
        requested_skill_id=data.get("requested_skill_id"),
        priority=int(data.get("priority") or 0),
        max_retries=int(data.get("max_retries") or 0),
        interval_seconds=(
            int(data["interval_seconds"]) if data.get("interval_seconds") is not None else None
        ),
        run_at=data.get("run_at"),
        last_run_at=data.get("last_run_at"),
        next_run_at=data.get("next_run_at"),
        created_at=str(data.get("created_at") or ""),
        updated_at=str(data.get("updated_at") or ""),
        schedule_attrs=dict(data.get("schedule_attrs") or {}),
    )
