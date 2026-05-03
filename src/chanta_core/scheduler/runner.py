from __future__ import annotations

from typing import Any

from chanta_core.scheduler.service import SchedulerService


class SchedulerRunner:
    def __init__(
        self,
        *,
        scheduler_service: SchedulerService | None = None,
        trace_service=None,
    ) -> None:
        self.scheduler_service = scheduler_service or SchedulerService()
        self.trace_service = trace_service

    def run_once(self, now_iso: str | None = None) -> dict[str, Any]:
        self._record("run_scheduler_once", "started", {"now_iso": now_iso})
        summary = self.scheduler_service.enqueue_due(now_iso=now_iso)
        self._record("run_scheduler_once", "completed", summary)
        return summary

    def _record(self, event_activity: str, status: str, attrs: dict[str, Any]) -> None:
        if self.trace_service is None:
            return
        recorder = getattr(self.trace_service, "record_scheduler_lifecycle_event", None)
        if recorder is None:
            return
        recorder(
            event_activity=event_activity,
            schedule=None,
            job_id=None,
            status=status,
            event_attrs=attrs,
        )
