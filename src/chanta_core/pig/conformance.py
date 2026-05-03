from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.ocpx.models import OCPXProcessView
from chanta_core.utility.time import utc_now_iso


@dataclass(frozen=True)
class PIGConformanceIssue:
    issue_id: str
    severity: str
    issue_type: str
    title: str
    description: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
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
class PIGConformanceReport:
    report_id: str
    scope: str
    process_instance_id: str | None
    session_id: str | None
    status: str
    checked_at: str
    issues: list[PIGConformanceIssue] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)
    report_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "scope": self.scope,
            "process_instance_id": self.process_instance_id,
            "session_id": self.session_id,
            "status": self.status,
            "checked_at": self.checked_at,
            "issues": [issue.to_dict() for issue in self.issues],
            "summary": self.summary,
            "report_attrs": self.report_attrs,
        }


class PIGConformanceService:
    """Lightweight advisory checks for ChantaCore runtime trace contracts."""

    SUCCESS_ACTIVITIES = [
        "start_process_instance",
        "start_process_run_loop",
        "decide_next_activity",
        "select_skill",
        "execute_skill",
        "observe_result",
        "record_outcome",
        "complete_process_instance",
    ]

    def __init__(
        self,
        *,
        ocpx_loader: OCPXLoader | None = None,
        ocpx_engine: OCPXEngine | None = None,
    ) -> None:
        self.ocpx_loader = ocpx_loader or OCPXLoader()
        self.ocpx_engine = ocpx_engine or OCPXEngine()

    def check_recent(self, limit: int = 20) -> PIGConformanceReport:
        return self.check_view(
            self.ocpx_loader.load_recent_view(limit=limit),
            scope="recent",
        )

    def check_process_instance(
        self,
        process_instance_id: str,
    ) -> PIGConformanceReport:
        return self.check_view(
            self.ocpx_loader.load_process_instance_view(process_instance_id),
            scope="process_instance",
        )

    def check_session(self, session_id: str) -> PIGConformanceReport:
        return self.check_view(
            self.ocpx_loader.load_session_view(session_id),
            scope="session",
        )

    def check_view(
        self,
        view: OCPXProcessView,
        *,
        scope: str = "view",
    ) -> PIGConformanceReport:
        activity_sequence = self.ocpx_engine.activity_sequence(view)
        object_types = self._object_types(view)
        issues: list[PIGConformanceIssue] = []

        if not activity_sequence:
            return self._report(
                view=view,
                scope=scope,
                status="unknown",
                issues=[
                    self._issue(
                        severity="info",
                        issue_type="unknown_variant",
                        title="No runtime events available",
                        description="The selected view does not contain enough events for runtime self-conformance checks.",
                    )
                ],
                summary_attrs={"event_count": 0, "object_count": len(view.objects)},
            )

        self._check_minimum_activities(activity_sequence, issues)
        self._check_order(activity_sequence, issues)
        self._check_relation_coverage(view, issues)
        self._check_outcome_consistency(activity_sequence, object_types, issues)
        self._check_failure_consistency(activity_sequence, object_types, issues)
        self._check_decision_contract(view, issues)

        return self._report(
            view=view,
            scope=scope,
            status=self._status_for_issues(issues),
            issues=issues,
            summary_attrs={
                "event_count": len(view.events),
                "object_count": len(view.objects),
                "activity_count": len(activity_sequence),
                "activity_sequence": activity_sequence,
                "object_types": sorted(object_types),
            },
        )

    def _check_minimum_activities(
        self,
        activity_sequence: list[str],
        issues: list[PIGConformanceIssue],
    ) -> None:
        activity_set = set(activity_sequence)
        success_path = "complete_process_instance" in activity_set
        failure_path = (
            "fail_process_instance" in activity_set
            or "fail_skill_execution" in activity_set
        )
        if success_path:
            for activity in self.SUCCESS_ACTIVITIES:
                if activity not in activity_set:
                    issues.append(
                        self._issue(
                            severity="warning",
                            issue_type="missing_activity",
                            title=f"Missing expected activity: {activity}",
                            description=(
                                "A completed ProcessRunLoop trace is missing an expected runtime activity."
                            ),
                            issue_attrs={"missing_activity": activity},
                        )
                    )
        if failure_path and "fail_process_instance" not in activity_set:
            issues.append(
                self._issue(
                    severity="warning",
                    issue_type="invalid_failure_path",
                    title="Skill failure was not followed by process failure",
                    description=(
                        "fail_skill_execution appears without fail_process_instance; recovery is not modeled in v0.6.7."
                    ),
                    issue_attrs={"missing_activity": "fail_process_instance"},
                )
            )

    def _check_order(
        self,
        activity_sequence: list[str],
        issues: list[PIGConformanceIssue],
    ) -> None:
        checks = [
            ("select_skill", "execute_skill"),
            ("execute_skill", "observe_result"),
            ("record_outcome", "complete_process_instance"),
            ("call_llm", "receive_llm_response"),
        ]
        for before, after in checks:
            before_index = self._first_index(activity_sequence, before)
            after_index = self._first_index(activity_sequence, after)
            if before_index is None or after_index is None:
                continue
            if before_index > after_index:
                issues.append(
                    self._issue(
                        severity="warning",
                        issue_type="invalid_success_path",
                        title=f"Activity order warning: {before} after {after}",
                        description=(
                            "Runtime activity order differs from the expected ProcessRunLoop contract fragment."
                        ),
                        issue_attrs={
                            "expected_before": before,
                            "expected_after": after,
                            "before_index": before_index,
                            "after_index": after_index,
                        },
                    )
                )

    def _check_relation_coverage(
        self,
        view: OCPXProcessView,
        issues: list[PIGConformanceIssue],
    ) -> None:
        coverage = self.ocpx_engine.compute_relation_coverage(view)
        if float(coverage.get("coverage_ratio") or 0.0) < 1.0:
            issues.append(
                self._issue(
                    severity="warning",
                    issue_type="missing_relation",
                    title="Some events lack related objects",
                    description=(
                        "Runtime self-conformance expects each event to retain event-object context."
                    ),
                    issue_attrs=coverage,
                )
            )

    def _check_outcome_consistency(
        self,
        activity_sequence: list[str],
        object_types: set[str],
        issues: list[PIGConformanceIssue],
    ) -> None:
        if "complete_process_instance" in activity_sequence and "outcome" not in object_types:
            issues.append(
                self._issue(
                    severity="warning",
                    issue_type="missing_outcome",
                    title="Completed trace has no outcome object",
                    description=(
                        "complete_process_instance is present, but no outcome object is visible in the OCPX view."
                    ),
                )
            )

    def _check_failure_consistency(
        self,
        activity_sequence: list[str],
        object_types: set[str],
        issues: list[PIGConformanceIssue],
    ) -> None:
        if (
            "fail_process_instance" in activity_sequence
            or "fail_skill_execution" in activity_sequence
        ) and "error" not in object_types:
            issues.append(
                self._issue(
                    severity="warning",
                    issue_type="missing_error_object",
                    title="Failure trace has no error object",
                    description=(
                        "Failure activities are present, but no error object is visible in the OCPX view."
                    ),
                )
            )

    def _check_decision_contract(
        self,
        view: OCPXProcessView,
        issues: list[PIGConformanceIssue],
    ) -> None:
        decision_events = [
            event for event in view.events if event.event_activity == "decide_skill"
        ]
        if not decision_events:
            return
        selected_skill_ids = {
            str(event.event_attrs.get("selected_skill_id"))
            for event in decision_events
            if event.event_attrs.get("selected_skill_id")
        }
        if not selected_skill_ids:
            issues.append(
                self._issue(
                    severity="info",
                    issue_type="decision_contract_warning",
                    title="Decision event has no selected skill id",
                    description=(
                        "decide_skill exists, but selected_skill_id is not visible in event attributes."
                    ),
                )
            )
            return
        downstream_skill_ids = {
            str(event.event_attrs.get("skill_id"))
            for event in view.events
            if event.event_activity in {"select_skill", "execute_skill"}
            and event.event_attrs.get("skill_id")
        }
        missing = sorted(selected_skill_ids - downstream_skill_ids)
        if missing:
            issues.append(
                self._issue(
                    severity="info",
                    issue_type="decision_contract_warning",
                    title="Selected skill not observed downstream",
                    description=(
                        "A decide_skill event selected a skill that was not visible in select_skill or execute_skill events."
                    ),
                    issue_attrs={"selected_skill_ids": missing},
                )
            )

    def _report(
        self,
        *,
        view: OCPXProcessView,
        scope: str,
        status: str,
        issues: list[PIGConformanceIssue],
        summary_attrs: dict[str, Any],
    ) -> PIGConformanceReport:
        severity_counts: dict[str, int] = {"info": 0, "warning": 0, "error": 0}
        for issue in issues:
            severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1
        process_instance_id = self._process_instance_id(view)
        return PIGConformanceReport(
            report_id=f"pig_conformance_report:{uuid4()}",
            scope=scope,
            process_instance_id=process_instance_id,
            session_id=view.session_id,
            status=status,
            checked_at=utc_now_iso(),
            issues=issues,
            summary={
                **summary_attrs,
                "issue_count": len(issues),
                "severity_counts": severity_counts,
            },
            report_attrs={
                "advisory": True,
                "diagnostic_only": True,
                "formal_process_mining_conformance": False,
                "view_id": view.view_id,
                "view_source": view.source,
            },
        )

    @staticmethod
    def _status_for_issues(issues: list[PIGConformanceIssue]) -> str:
        if not issues:
            return "conformant"
        if any(issue.severity == "error" for issue in issues):
            return "nonconformant"
        if any(issue.severity == "warning" for issue in issues):
            return "warning"
        return "conformant"

    def _issue(
        self,
        *,
        severity: str,
        issue_type: str,
        title: str,
        description: str,
        evidence_refs: list[dict[str, Any]] | None = None,
        issue_attrs: dict[str, Any] | None = None,
    ) -> PIGConformanceIssue:
        return PIGConformanceIssue(
            issue_id=f"pig_conformance_issue:{uuid4()}",
            severity=severity,
            issue_type=issue_type,
            title=title,
            description=description,
            evidence_refs=evidence_refs or [],
            issue_attrs=issue_attrs or {},
        )

    @staticmethod
    def _first_index(activity_sequence: list[str], activity: str) -> int | None:
        try:
            return activity_sequence.index(activity)
        except ValueError:
            return None

    @staticmethod
    def _object_types(view: OCPXProcessView) -> set[str]:
        return {item.object_type for item in view.objects}

    @staticmethod
    def _process_instance_id(view: OCPXProcessView) -> str | None:
        process_instance_id = view.view_attrs.get("process_instance_id")
        if process_instance_id:
            return str(process_instance_id)
        for item in view.objects:
            if item.object_type == "process_instance":
                return item.object_id
        for event in view.events:
            if event.event_attrs.get("process_instance_id"):
                return str(event.event_attrs["process_instance_id"])
        return None
