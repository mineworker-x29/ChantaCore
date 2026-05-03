from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.utility.time import utc_now_iso
from chanta_core.workers.job import ProcessJob
from chanta_core.workers.store import ProcessJobStore


@dataclass(frozen=True)
class QueueConformanceIssue:
    issue_id: str
    severity: str
    issue_type: str
    title: str
    description: str
    evidence_refs: list[dict[str, Any]]
    issue_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "issue_id": self.issue_id,
            "severity": self.severity,
            "issue_type": self.issue_type,
            "title": self.title,
            "description": self.description,
            "evidence_refs": self.evidence_refs,
            "issue_attrs": self.issue_attrs,
        }


@dataclass(frozen=True)
class QueueConformanceReport:
    report_id: str
    scope: str
    job_id: str | None
    status: str
    checked_at: str
    issues: list[QueueConformanceIssue]
    summary: dict[str, Any]
    report_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "scope": self.scope,
            "job_id": self.job_id,
            "status": self.status,
            "checked_at": self.checked_at,
            "issues": [issue.to_dict() for issue in self.issues],
            "summary": self.summary,
            "report_attrs": self.report_attrs,
        }


class PIGQueueConformanceService:
    def __init__(
        self,
        *,
        job_store: ProcessJobStore | None = None,
        ocpx_loader: OCPXLoader | None = None,
        ocpx_engine: OCPXEngine | None = None,
    ) -> None:
        self.job_store = job_store or ProcessJobStore()
        self.ocpx_loader = ocpx_loader or OCPXLoader()
        self.ocpx_engine = ocpx_engine or OCPXEngine()

    def check_job(self, job_id: str) -> QueueConformanceReport:
        job = self.job_store.get(job_id)
        if job is None:
            issue = _issue(
                severity="warning",
                issue_type="missing_job",
                title="Process job not found",
                description=f"No current process job state exists for {job_id}.",
                evidence_refs=[{"job_id": job_id}],
            )
            return self._report(
                scope="job",
                job_id=job_id,
                issues=[issue],
                summary={"job_count": 0},
            )
        return self.check_job_sequence(job)

    def check_recent_jobs(self, limit: int = 20) -> QueueConformanceReport:
        jobs = self._current_jobs(limit)
        if not jobs:
            return self._report(
                scope="recent_jobs",
                job_id=None,
                issues=[],
                summary={"job_count": 0},
                status_override="unknown",
            )
        issues: list[QueueConformanceIssue] = []
        status_counts: dict[str, int] = {}
        retry_jobs = 0
        for job in jobs:
            status_counts[job.status] = status_counts.get(job.status, 0) + 1
            if job.retry_count:
                retry_jobs += 1
            issues.extend(self._issues_for_job(job, activity_sequence=None))
        return self._report(
            scope="recent_jobs",
            job_id=None,
            issues=issues,
            summary={
                "job_count": len(jobs),
                "status_counts": status_counts,
                "failed_jobs": status_counts.get("failed", 0),
                "retry_jobs": retry_jobs,
            },
        )

    def check_job_sequence(
        self,
        job: ProcessJob,
        activity_sequence: list[str] | None = None,
    ) -> QueueConformanceReport:
        issues = self._issues_for_job(job, activity_sequence=activity_sequence)
        return self._report(
            scope="job",
            job_id=job.job_id,
            issues=issues,
            summary={
                "job_id": job.job_id,
                "job_status": job.status,
                "retry_count": job.retry_count,
                "max_retries": job.max_retries,
                "activity_sequence_available": activity_sequence is not None,
            },
        )

    def _issues_for_job(
        self,
        job: ProcessJob,
        *,
        activity_sequence: list[str] | None,
    ) -> list[QueueConformanceIssue]:
        issues: list[QueueConformanceIssue] = []
        evidence = [{"job_id": job.job_id, "status": job.status}]
        if job.retry_count > job.max_retries:
            issues.append(
                _issue(
                    severity="error",
                    issue_type="retry_limit_exceeded",
                    title="Retry count exceeds max retries",
                    description="The process job retry_count is greater than max_retries.",
                    evidence_refs=evidence,
                    issue_attrs={
                        "retry_count": job.retry_count,
                        "max_retries": job.max_retries,
                    },
                )
            )
        if job.status in {"claimed", "running"} and not job.claimed_by_worker_id:
            issues.append(
                _issue(
                    severity="warning",
                    issue_type="missing_claimed_worker",
                    title="Claimed/running job has no worker",
                    description="Claimed and running jobs should retain claimed_by_worker_id.",
                    evidence_refs=evidence,
                )
            )
        if job.status == "failed" and not (job.last_error or self._has(activity_sequence, "fail_worker_job")):
            issues.append(
                _issue(
                    severity="warning",
                    issue_type="missing_failure_evidence",
                    title="Failed job has no failure evidence",
                    description="Failed jobs should have last_error or fail_worker_job evidence.",
                    evidence_refs=evidence,
                )
            )
        if job.status == "cancelled" and job.completed_at:
            issues.append(
                _issue(
                    severity="error",
                    issue_type="cancelled_completed_conflict",
                    title="Cancelled job also has completion timestamp",
                    description="A cancelled process job should not also be completed.",
                    evidence_refs=evidence,
                    issue_attrs={"completed_at": job.completed_at},
                )
            )
        if activity_sequence is not None:
            issues.extend(self._sequence_issues(job, activity_sequence))
        return issues

    def _sequence_issues(
        self,
        job: ProcessJob,
        activity_sequence: list[str],
    ) -> list[QueueConformanceIssue]:
        issues: list[QueueConformanceIssue] = []
        if job.status == "completed":
            for activity in [
                "enqueue_process_job",
                "claim_process_job",
                "start_worker_job",
                "complete_worker_job",
            ]:
                if activity not in activity_sequence:
                    issues.append(
                        _issue(
                            severity="warning",
                            issue_type="missing_lifecycle_activity",
                            title=f"Missing {activity}",
                            description="Completed jobs should have complete queue lifecycle evidence.",
                            evidence_refs=[{"job_id": job.job_id, "activity": activity}],
                        )
                    )
        order_checks = [
            ("claim_process_job", "start_worker_job"),
            ("start_worker_job", "complete_worker_job"),
            ("start_worker_job", "fail_worker_job"),
        ]
        for before, after in order_checks:
            if not self._ordered(activity_sequence, before, after):
                issues.append(
                    _issue(
                        severity="warning",
                        issue_type="invalid_activity_order",
                        title=f"{before} should precede {after}",
                        description="Queue lifecycle activity order is inconsistent.",
                        evidence_refs=[{"job_id": job.job_id}],
                        issue_attrs={"before": before, "after": after},
                    )
                )
        if "retry_process_job" in activity_sequence:
            retry_index = activity_sequence.index("retry_process_job")
            prefix = activity_sequence[:retry_index]
            if "start_worker_job" not in prefix and "fail_worker_job" not in prefix:
                issues.append(
                    _issue(
                        severity="warning",
                        issue_type="invalid_retry_evidence",
                        title="Retry appears without prior worker execution evidence",
                        description="Retry lifecycle evidence should follow a worker execution path.",
                        evidence_refs=[{"job_id": job.job_id}],
                    )
                )
        return issues

    def _current_jobs(self, limit: int) -> list[ProcessJob]:
        jobs = list(self.job_store._state_by_id().values())
        jobs.sort(key=lambda item: (item.updated_at, item.job_id))
        return jobs[-max(0, limit) :]

    def _report(
        self,
        *,
        scope: str,
        job_id: str | None,
        issues: list[QueueConformanceIssue],
        summary: dict[str, Any],
        status_override: str | None = None,
    ) -> QueueConformanceReport:
        return QueueConformanceReport(
            report_id=f"queue_conformance_report:{uuid4()}",
            scope=scope,
            job_id=job_id,
            status=status_override or _status_from_issues(issues),
            checked_at=utc_now_iso(),
            issues=issues,
            summary={
                **summary,
                "issue_count": len(issues),
                "diagnostic_only": True,
                "advisory": True,
            },
            report_attrs={"read_only": True},
        )

    @staticmethod
    def _has(activity_sequence: list[str] | None, activity: str) -> bool:
        return bool(activity_sequence and activity in activity_sequence)

    @staticmethod
    def _ordered(activity_sequence: list[str], before: str, after: str) -> bool:
        if before not in activity_sequence or after not in activity_sequence:
            return True
        return activity_sequence.index(before) < activity_sequence.index(after)


def _issue(
    *,
    severity: str,
    issue_type: str,
    title: str,
    description: str,
    evidence_refs: list[dict[str, Any]],
    issue_attrs: dict[str, Any] | None = None,
) -> QueueConformanceIssue:
    return QueueConformanceIssue(
        issue_id=f"queue_conformance_issue:{uuid4()}",
        severity=severity,
        issue_type=issue_type,
        title=title,
        description=description,
        evidence_refs=evidence_refs,
        issue_attrs=issue_attrs or {},
    )


def _status_from_issues(issues: list[QueueConformanceIssue]) -> str:
    if any(issue.severity == "error" for issue in issues):
        return "nonconformant"
    if any(issue.severity == "warning" for issue in issues):
        return "warning"
    return "conformant"
