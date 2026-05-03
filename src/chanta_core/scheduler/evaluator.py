from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any

from chanta_core.scheduler.schedule import ProcessSchedule
from chanta_core.utility.time import utc_now_iso


@dataclass(frozen=True)
class ScheduleEvaluation:
    schedule_id: str
    is_due: bool
    reason: str
    evaluated_at: str
    next_run_at: str | None
    evaluation_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schedule_id": self.schedule_id,
            "is_due": self.is_due,
            "reason": self.reason,
            "evaluated_at": self.evaluated_at,
            "next_run_at": self.next_run_at,
            "evaluation_attrs": self.evaluation_attrs,
        }


class ScheduleEvaluator:
    def evaluate(
        self,
        schedule: ProcessSchedule,
        now_iso: str | None = None,
    ) -> ScheduleEvaluation:
        evaluated_at = now_iso or utc_now_iso()
        try:
            now = _parse_iso(evaluated_at)
            if schedule.status != "active":
                return self._result(schedule, False, "schedule_not_active", evaluated_at)
            if schedule.schedule_type == "once":
                if not schedule.run_at:
                    return self._result(schedule, False, "once_schedule_missing_run_at", evaluated_at)
                return self._result(
                    schedule,
                    now >= _parse_iso(schedule.run_at),
                    "once_schedule_due" if now >= _parse_iso(schedule.run_at) else "once_schedule_not_due",
                    evaluated_at,
                )
            if schedule.schedule_type == "interval":
                next_run_at = schedule.next_run_at or self.compute_next_run_at(schedule)
                if not next_run_at:
                    return self._result(schedule, False, "interval_schedule_missing_next_run_at", evaluated_at)
                due = now >= _parse_iso(next_run_at)
                return self._result(
                    schedule,
                    due,
                    "interval_schedule_due" if due else "interval_schedule_not_due",
                    evaluated_at,
                    next_run_at=next_run_at,
                )
            return self._result(schedule, False, "unknown_schedule_type", evaluated_at)
        except Exception as error:
            return self._result(
                schedule,
                False,
                "invalid_schedule_timestamp",
                evaluated_at,
                evaluation_attrs={"error": str(error)},
            )

    def compute_next_run_at(
        self,
        schedule: ProcessSchedule,
        from_iso: str | None = None,
    ) -> str | None:
        if schedule.schedule_type != "interval" or not schedule.interval_seconds:
            return None
        base = _parse_iso(from_iso or schedule.next_run_at or schedule.created_at)
        return _format_iso(base + timedelta(seconds=schedule.interval_seconds))

    @staticmethod
    def _result(
        schedule: ProcessSchedule,
        is_due: bool,
        reason: str,
        evaluated_at: str,
        *,
        next_run_at: str | None = None,
        evaluation_attrs: dict[str, Any] | None = None,
    ) -> ScheduleEvaluation:
        return ScheduleEvaluation(
            schedule_id=schedule.schedule_id,
            is_due=is_due,
            reason=reason,
            evaluated_at=evaluated_at,
            next_run_at=next_run_at or schedule.next_run_at,
            evaluation_attrs=evaluation_attrs or {},
        )


def _parse_iso(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def _format_iso(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
