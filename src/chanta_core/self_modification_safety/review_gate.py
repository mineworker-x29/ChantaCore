from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.self_modification_safety.candidate import PatchCandidate
from chanta_core.self_modification_safety.draft import DiffPreviewArtifact, PatchDraft
from chanta_core.self_modification_safety.dry_run import (
    PatchDryRunCheckRequest,
    PatchDryRunReport,
    PatchDryRunReportService,
    PatchDryRunSourceService,
)
from chanta_core.self_modification_safety.static_safety import PatchStaticSafetyReport
from chanta_core.utility.time import utc_now_iso


SELF_MODIFICATION_REVIEW_GATE_VERSION = "v0.22.5"
SELF_MODIFICATION_REVIEW_GATE_STATE = "self_modification_human_review_apply_gate_checked"
REVIEW_GATE_SKILL_ID = "skill:self_modification_review_gate"
APPLY_GATE_SKILL_ID = "skill:self_modification_apply_gate"
ROLLBACK_PLAN_SKILL_ID = "skill:self_modification_rollback_plan"


@dataclass(frozen=True)
class HumanReviewRequest:
    review_request_id: str
    created_at: str
    patch_candidate_id: str
    draft_id: str
    preview_id: str
    static_safety_report_id: str
    dry_run_report_id: str
    requested_by: str
    review_scope: str
    summary_refs: list[dict[str, Any]]
    risk_refs: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]]
    raw_patch_content_included: bool = False
    raw_file_content_included: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "review_request_id": self.review_request_id,
            "created_at": self.created_at,
            "patch_candidate_id": self.patch_candidate_id,
            "draft_id": self.draft_id,
            "preview_id": self.preview_id,
            "static_safety_report_id": self.static_safety_report_id,
            "dry_run_report_id": self.dry_run_report_id,
            "requested_by": self.requested_by,
            "review_scope": self.review_scope,
            "summary_refs": [dict(item) for item in self.summary_refs],
            "risk_refs": [dict(item) for item in self.risk_refs],
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "raw_patch_content_included": self.raw_patch_content_included,
            "raw_file_content_included": self.raw_file_content_included,
        }


@dataclass(frozen=True)
class HumanReviewDecision:
    decision_id: str
    review_request_id: str
    decided_at: str
    reviewer_type: str
    reviewer_ref: dict[str, Any] | None
    decision: str
    decision_reason: str | None
    approved_for_apply_gate: bool
    approved_for_direct_apply: bool = False
    required_followups: list[str] = field(default_factory=list)
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "review_request_id": self.review_request_id,
            "decided_at": self.decided_at,
            "reviewer_type": self.reviewer_type,
            "reviewer_ref": dict(self.reviewer_ref) if self.reviewer_ref else None,
            "decision": self.decision,
            "decision_reason": self.decision_reason,
            "approved_for_apply_gate": self.approved_for_apply_gate,
            "approved_for_direct_apply": self.approved_for_direct_apply,
            "required_followups": list(self.required_followups),
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class ApplyGatePreconditionCheck:
    check_id: str
    patch_candidate_id: str
    draft_id: str
    preview_id: str
    static_safety_report_id: str
    dry_run_report_id: str
    review_decision_id: str | None
    static_safety_passed: bool
    dry_run_passed: bool
    eligible_for_review: bool
    review_approved: bool
    rollback_plan_available: bool
    private_boundary_clear: bool
    secret_boundary_clear: bool
    target_still_within_scope: bool
    apply_gate_allowed: bool
    failed_preconditions: list[str]
    warning_preconditions: list[str]
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "patch_candidate_id": self.patch_candidate_id,
            "draft_id": self.draft_id,
            "preview_id": self.preview_id,
            "static_safety_report_id": self.static_safety_report_id,
            "dry_run_report_id": self.dry_run_report_id,
            "review_decision_id": self.review_decision_id,
            "static_safety_passed": self.static_safety_passed,
            "dry_run_passed": self.dry_run_passed,
            "eligible_for_review": self.eligible_for_review,
            "review_approved": self.review_approved,
            "rollback_plan_available": self.rollback_plan_available,
            "private_boundary_clear": self.private_boundary_clear,
            "secret_boundary_clear": self.secret_boundary_clear,
            "target_still_within_scope": self.target_still_within_scope,
            "apply_gate_allowed": self.apply_gate_allowed,
            "failed_preconditions": list(self.failed_preconditions),
            "warning_preconditions": list(self.warning_preconditions),
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class RollbackPlanDescriptor:
    rollback_plan_id: str
    patch_candidate_id: str
    draft_id: str
    preview_id: str
    plan_type: str
    rollback_possible: bool
    rollback_scope: str
    before_snapshot_refs: list[dict[str, Any]]
    reverse_operation_refs: list[dict[str, Any]]
    limitations: list[str]
    rollback_execution_enabled: bool = False
    rollback_executed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "rollback_plan_id": self.rollback_plan_id,
            "patch_candidate_id": self.patch_candidate_id,
            "draft_id": self.draft_id,
            "preview_id": self.preview_id,
            "plan_type": self.plan_type,
            "rollback_possible": self.rollback_possible,
            "rollback_scope": self.rollback_scope,
            "before_snapshot_refs": [dict(item) for item in self.before_snapshot_refs],
            "reverse_operation_refs": [dict(item) for item in self.reverse_operation_refs],
            "limitations": list(self.limitations),
            "rollback_execution_enabled": self.rollback_execution_enabled,
            "rollback_executed": self.rollback_executed,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class ApplyGateFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    target_ref: dict[str, Any] | None
    gate_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "finding_type": self.finding_type,
            "message": self.message,
            "target_ref": dict(self.target_ref) if self.target_ref else None,
            "gate_ref": dict(self.gate_ref) if self.gate_ref else None,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "withdrawal_condition": self.withdrawal_condition,
        }


@dataclass(frozen=True)
class ApplyGateAuthorization:
    authorization_id: str
    apply_gate_id: str
    patch_candidate_id: str
    draft_id: str
    preview_id: str
    dry_run_report_id: str
    review_decision_id: str
    rollback_plan_id: str
    authorized_for_stage: str = "bounded_patch_apply"
    authorized_next_version: str = "v0.22.6"
    expires_at: str | None = None
    single_use: bool = True
    consumed: bool = False
    patch_applied: bool = False
    file_write_performed: bool = False
    workspace_file_changed_emitted: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "authorization_id": self.authorization_id,
            "apply_gate_id": self.apply_gate_id,
            "patch_candidate_id": self.patch_candidate_id,
            "draft_id": self.draft_id,
            "preview_id": self.preview_id,
            "dry_run_report_id": self.dry_run_report_id,
            "review_decision_id": self.review_decision_id,
            "rollback_plan_id": self.rollback_plan_id,
            "authorized_for_stage": self.authorized_for_stage,
            "authorized_next_version": self.authorized_next_version,
            "expires_at": self.expires_at,
            "single_use": self.single_use,
            "consumed": self.consumed,
            "patch_applied": self.patch_applied,
            "file_write_performed": self.file_write_performed,
            "workspace_file_changed_emitted": self.workspace_file_changed_emitted,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class ApplyGateState:
    apply_gate_id: str
    created_at: str
    patch_candidate_id: str
    draft_id: str
    preview_id: str
    static_safety_report_id: str
    dry_run_report_id: str
    review_decision_id: str | None
    rollback_plan_id: str | None
    precondition_check: ApplyGatePreconditionCheck
    authorization: ApplyGateAuthorization | None
    gate_status: str
    review_approved: bool
    apply_gate_opened: bool
    eligible_for_bounded_apply: bool
    safe_to_apply: bool = False
    patch_applied: bool = False
    file_write_performed: bool = False
    workspace_file_changed_emitted: bool = False
    shell_executed: bool = False
    test_lint_executed: bool = False
    findings: list[ApplyGateFinding] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "apply_gate_id": self.apply_gate_id,
            "created_at": self.created_at,
            "patch_candidate_id": self.patch_candidate_id,
            "draft_id": self.draft_id,
            "preview_id": self.preview_id,
            "static_safety_report_id": self.static_safety_report_id,
            "dry_run_report_id": self.dry_run_report_id,
            "review_decision_id": self.review_decision_id,
            "rollback_plan_id": self.rollback_plan_id,
            "precondition_check": self.precondition_check.to_dict(),
            "authorization": self.authorization.to_dict() if self.authorization else None,
            "gate_status": self.gate_status,
            "review_approved": self.review_approved,
            "apply_gate_opened": self.apply_gate_opened,
            "eligible_for_bounded_apply": self.eligible_for_bounded_apply,
            "safe_to_apply": self.safe_to_apply,
            "patch_applied": self.patch_applied,
            "file_write_performed": self.file_write_performed,
            "workspace_file_changed_emitted": self.workspace_file_changed_emitted,
            "shell_executed": self.shell_executed,
            "test_lint_executed": self.test_lint_executed,
            "findings": [item.to_dict() for item in self.findings],
            "limitations": list(self.limitations),
        }


@dataclass(frozen=True)
class HumanReviewApplyGateReport:
    report_id: str
    created_at: str
    review_request: HumanReviewRequest
    review_decision: HumanReviewDecision | None
    rollback_plan: RollbackPlanDescriptor | None
    apply_gate_state: ApplyGateState
    findings: list[ApplyGateFinding]
    report_status: str
    review_status: str
    gate_status: str
    eligible_for_bounded_apply: bool
    safe_to_apply: bool = False
    patch_applied: bool = False
    file_write_performed: bool = False
    workspace_file_changed_emitted: bool = False
    shell_executed: bool = False
    test_lint_executed: bool = False
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until target file, patch draft, dry-run report, review decision, rollback plan, or policy changes."

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "created_at": self.created_at,
            "review_request": self.review_request.to_dict(),
            "review_decision": self.review_decision.to_dict() if self.review_decision else None,
            "rollback_plan": self.rollback_plan.to_dict() if self.rollback_plan else None,
            "apply_gate_state": self.apply_gate_state.to_dict(),
            "findings": [item.to_dict() for item in self.findings],
            "report_status": self.report_status,
            "review_status": self.review_status,
            "gate_status": self.gate_status,
            "eligible_for_bounded_apply": self.eligible_for_bounded_apply,
            "safe_to_apply": self.safe_to_apply,
            "patch_applied": self.patch_applied,
            "file_write_performed": self.file_write_performed,
            "workspace_file_changed_emitted": self.workspace_file_changed_emitted,
            "shell_executed": self.shell_executed,
            "test_lint_executed": self.test_lint_executed,
            "limitations": list(self.limitations),
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "validity_horizon": self.validity_horizon,
        }


@dataclass(frozen=True)
class ApplyGateNeedsMoreInputCandidate:
    candidate_id: str
    report_id: str | None
    reason: str
    missing_inputs: list[str]
    evidence_refs: list[dict[str, Any]]
    recommended_review_decision: str = "needs_more_input"
    candidate_status: str = "candidate_only"
    applied: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "report_id": self.report_id,
            "reason": self.reason,
            "missing_inputs": list(self.missing_inputs),
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "recommended_review_decision": self.recommended_review_decision,
            "candidate_status": self.candidate_status,
            "applied": self.applied,
        }


@dataclass(frozen=True)
class ApplyGateNoActionCandidate:
    candidate_id: str
    report_id: str | None
    reason: str
    evidence_refs: list[dict[str, Any]]
    recommended_review_decision: str = "no_action"
    candidate_status: str = "candidate_only"
    applied: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "report_id": self.report_id,
            "reason": self.reason,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "recommended_review_decision": self.recommended_review_decision,
            "candidate_status": self.candidate_status,
            "applied": self.applied,
        }


@dataclass(frozen=True)
class HumanReviewApplyGateResult:
    report: HumanReviewApplyGateReport
    no_action_candidate: ApplyGateNoActionCandidate | None
    needs_more_input_candidate: ApplyGateNeedsMoreInputCandidate | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "report": self.report.to_dict(),
            "no_action_candidate": self.no_action_candidate.to_dict() if self.no_action_candidate else None,
            "needs_more_input_candidate": self.needs_more_input_candidate.to_dict()
            if self.needs_more_input_candidate
            else None,
        }


class HumanReviewSourceService:
    def __init__(
        self,
        *,
        patch_candidates: dict[str, PatchCandidate] | None = None,
        patch_drafts: dict[str, PatchDraft] | None = None,
        diff_previews: dict[str, DiffPreviewArtifact] | None = None,
        static_safety_reports: dict[str, PatchStaticSafetyReport] | None = None,
        dry_run_reports: dict[str, PatchDryRunReport] | None = None,
        allow_synthetic: bool = False,
    ) -> None:
        self.patch_candidates = dict(patch_candidates or {})
        self.patch_drafts = dict(patch_drafts or {})
        self.diff_previews = dict(diff_previews or {})
        self.static_safety_reports = dict(static_safety_reports or {})
        self.dry_run_reports = dict(dry_run_reports or {})
        self.allow_synthetic = allow_synthetic
        if self.allow_synthetic:
            self._ensure_synthetic_bundle()

    def load_patch_candidate(self, patch_candidate_id: str | None) -> PatchCandidate | None:
        return _load_by_id(self.patch_candidates, patch_candidate_id, self.allow_synthetic)

    def load_patch_draft(self, draft_id: str | None) -> PatchDraft | None:
        return _load_by_id(self.patch_drafts, draft_id, self.allow_synthetic)

    def load_diff_preview(self, preview_id: str | None) -> DiffPreviewArtifact | None:
        return _load_by_id(self.diff_previews, preview_id, self.allow_synthetic)

    def load_static_safety_report(self, report_id: str | None) -> PatchStaticSafetyReport | None:
        return _load_by_id(self.static_safety_reports, report_id, self.allow_synthetic)

    def load_dry_run_report(self, report_id: str | None) -> PatchDryRunReport | None:
        return _load_by_id(self.dry_run_reports, report_id, self.allow_synthetic)

    def _ensure_synthetic_bundle(self) -> None:
        if self.dry_run_reports:
            return
        source = PatchDryRunSourceService(allow_synthetic=True)
        dry_run = PatchDryRunReportService(source_service=source).build_report(PatchDryRunCheckRequest())
        self.patch_candidates.update(source.patch_candidates)
        self.patch_drafts.update(source.patch_drafts)
        self.diff_previews.update(source.diff_previews)
        self.static_safety_reports.update(source.static_safety_reports)
        self.dry_run_reports[dry_run.report_id] = dry_run


class HumanReviewRequestService:
    def create_review_request(
        self,
        *,
        patch_candidate_id: str,
        draft_id: str,
        preview_id: str,
        static_safety_report_id: str,
        dry_run_report_id: str,
        requested_by: str = "operator",
        review_scope: str = "approve_for_apply_gate",
    ) -> HumanReviewRequest:
        return HumanReviewRequest(
            review_request_id=f"human_review_request:{uuid4()}",
            created_at=utc_now_iso(),
            patch_candidate_id=patch_candidate_id,
            draft_id=draft_id,
            preview_id=preview_id,
            static_safety_report_id=static_safety_report_id,
            dry_run_report_id=dry_run_report_id,
            requested_by=requested_by if requested_by in {"operator", "system", "agent"} else "operator",
            review_scope=review_scope,
            summary_refs=[{"ref_type": "sanitized_patch_summary", "version": SELF_MODIFICATION_REVIEW_GATE_VERSION}],
            risk_refs=[{"ref_type": "dry_run_report", "report_id": dry_run_report_id}],
            evidence_refs=[
                {"ref_type": "patch_candidate", "id": patch_candidate_id},
                {"ref_type": "patch_draft", "id": draft_id},
                {"ref_type": "diff_preview", "id": preview_id},
                {"ref_type": "patch_static_safety_report", "id": static_safety_report_id},
                {"ref_type": "patch_dry_run_report", "id": dry_run_report_id},
            ],
            raw_patch_content_included=False,
            raw_file_content_included=False,
        )


class HumanReviewDecisionService:
    def record_decision(
        self,
        *,
        review_request_id: str,
        decision: str,
        decision_reason: str | None = None,
        reviewer_ref: dict[str, Any] | None = None,
        reviewer_type: str = "operator",
    ) -> HumanReviewDecision:
        normalized = decision if decision in {"approve", "reject", "revise", "no_action", "needs_more_input"} else "needs_more_input"
        followups = [] if normalized == "approve" else [f"operator_decision_{normalized}"]
        return HumanReviewDecision(
            decision_id=f"human_review_decision:{uuid4()}",
            review_request_id=review_request_id,
            decided_at=utc_now_iso(),
            reviewer_type=reviewer_type if reviewer_type in {"operator", "authorized_reviewer"} else "operator",
            reviewer_ref=dict(reviewer_ref) if reviewer_ref else None,
            decision=normalized,
            decision_reason=decision_reason,
            approved_for_apply_gate=normalized == "approve",
            approved_for_direct_apply=False,
            required_followups=followups,
            evidence_refs=[{"ref_type": "human_review_request", "id": review_request_id}],
        )


class RollbackPlanService:
    def build_rollback_plan(
        self,
        *,
        patch_candidate_id: str,
        draft_id: str,
        preview_id: str,
        draft: PatchDraft | None = None,
    ) -> RollbackPlanDescriptor:
        operation_refs = (
            [{"ref_type": "patch_operation_draft", "operation_id": item.operation_id} for item in draft.operations]
            if draft
            else []
        )
        before_refs = (
            [{"ref_type": "sanitized_before_snapshot", "target_id": item.target_id} for item in draft.target_context_refs]
            if draft
            else []
        )
        possible = bool(operation_refs)
        return RollbackPlanDescriptor(
            rollback_plan_id=f"rollback_plan_descriptor:{uuid4()}",
            patch_candidate_id=patch_candidate_id,
            draft_id=draft_id,
            preview_id=preview_id,
            plan_type="reverse_patch" if possible else "unavailable",
            rollback_possible=possible,
            rollback_scope="same_file" if possible else "unknown",
            before_snapshot_refs=before_refs,
            reverse_operation_refs=operation_refs,
            limitations=[
                "Rollback plan is a descriptor only in v0.22.5.",
                "Rollback execution is deferred.",
                "Raw full before content is not included.",
            ],
            rollback_execution_enabled=False,
            rollback_executed=False,
            evidence_refs=[{"ref_type": "rollback_plan_version", "version": SELF_MODIFICATION_REVIEW_GATE_VERSION}],
        )


class ApplyGatePreconditionService:
    def check_preconditions(
        self,
        *,
        static_safety_report: PatchStaticSafetyReport | None,
        dry_run_report: PatchDryRunReport | None,
        review_decision: HumanReviewDecision | None,
        rollback_plan: RollbackPlanDescriptor | None,
        patch_candidate_id: str,
        draft_id: str,
        preview_id: str,
    ) -> ApplyGatePreconditionCheck:
        static_passed = bool(static_safety_report and static_safety_report.static_safety_status in {"passed", "warning"})
        dry_passed = bool(dry_run_report and dry_run_report.dry_run_status in {"passed", "warning"})
        eligible = bool(dry_run_report and dry_run_report.eligible_for_review)
        review_approved = bool(review_decision and review_decision.approved_for_apply_gate and review_decision.decision == "approve")
        rollback_available = bool(rollback_plan and rollback_plan.rollback_possible)
        private_clear = not _has_finding(dry_run_report, "private_boundary_block") if dry_run_report else False
        secret_clear = not _has_finding(dry_run_report, "secret_boundary_block") if dry_run_report else False
        target_scope = bool(dry_run_report and not _has_finding(dry_run_report, "target_scope_changed"))
        failed: list[str] = []
        if not static_passed:
            failed.append("static_safety_report_required_or_not_passed")
        if not dry_passed:
            failed.append("dry_run_report_required_or_not_passed")
        if not eligible:
            failed.append("dry_run_eligible_for_review_required")
        if not review_approved:
            failed.append("review_approval_required")
        if not rollback_available:
            failed.append("rollback_plan_required")
        if not private_clear:
            failed.append("private_boundary_clear_required")
        if not secret_clear:
            failed.append("secret_boundary_clear_required")
        if not target_scope:
            failed.append("target_still_within_scope_required")
        return ApplyGatePreconditionCheck(
            check_id=f"apply_gate_precondition_check:{uuid4()}",
            patch_candidate_id=patch_candidate_id,
            draft_id=draft_id,
            preview_id=preview_id,
            static_safety_report_id=static_safety_report.report_id if static_safety_report else "",
            dry_run_report_id=dry_run_report.report_id if dry_run_report else "",
            review_decision_id=review_decision.decision_id if review_decision else None,
            static_safety_passed=static_passed,
            dry_run_passed=dry_passed,
            eligible_for_review=eligible,
            review_approved=review_approved,
            rollback_plan_available=rollback_available,
            private_boundary_clear=private_clear,
            secret_boundary_clear=secret_clear,
            target_still_within_scope=target_scope,
            apply_gate_allowed=not failed,
            failed_preconditions=failed,
            warning_preconditions=[],
            evidence_refs=[{"ref_type": "apply_gate_version", "version": SELF_MODIFICATION_REVIEW_GATE_VERSION}],
        )


class ApplyGateFindingService:
    def build_findings(
        self,
        precondition_check: ApplyGatePreconditionCheck,
        review_decision: HumanReviewDecision | None,
        rollback_plan: RollbackPlanDescriptor | None,
    ) -> list[ApplyGateFinding]:
        findings: list[ApplyGateFinding] = []
        for failed in precondition_check.failed_preconditions:
            findings.append(_finding(_finding_type_for_precondition(failed), "critical", failed, precondition_check.check_id))
        if review_decision:
            if review_decision.decision == "reject":
                findings.append(_finding("review_rejected", "error", "Human review rejected the candidate.", precondition_check.check_id))
            if review_decision.decision == "revise":
                findings.append(_finding("review_requested_revision", "warning", "Human review requested revision.", precondition_check.check_id))
            if review_decision.decision == "needs_more_input":
                findings.append(_finding("review_needs_more_input", "warning", "Human review needs more input.", precondition_check.check_id))
            if review_decision.approved_for_direct_apply:
                findings.append(_finding("direct_apply_forbidden", "critical", "Direct apply approval is forbidden.", precondition_check.check_id))
        if rollback_plan and not rollback_plan.rollback_possible:
            findings.append(_finding("rollback_not_possible", "critical", "Rollback is not possible.", precondition_check.check_id))
        if precondition_check.apply_gate_allowed:
            findings.append(_finding("apply_gate_opened", "info", "Apply gate may open for bounded apply stage.", precondition_check.check_id))
        else:
            findings.append(_finding("apply_gate_not_allowed", "error", "Apply gate cannot open.", precondition_check.check_id))
        return findings or [_finding("ok", "info", "Apply gate preconditions are visible.", precondition_check.check_id)]


class ApplyGateService:
    def __init__(self, *, precondition_service: ApplyGatePreconditionService | None = None) -> None:
        self.precondition_service = precondition_service or ApplyGatePreconditionService()
        self.finding_service = ApplyGateFindingService()

    def evaluate_gate(
        self,
        *,
        patch_candidate_id: str,
        draft_id: str,
        preview_id: str,
        static_safety_report: PatchStaticSafetyReport | None,
        dry_run_report: PatchDryRunReport | None,
        review_decision: HumanReviewDecision | None,
        rollback_plan: RollbackPlanDescriptor | None,
    ) -> ApplyGateState:
        check = self.precondition_service.check_preconditions(
            static_safety_report=static_safety_report,
            dry_run_report=dry_run_report,
            review_decision=review_decision,
            rollback_plan=rollback_plan,
            patch_candidate_id=patch_candidate_id,
            draft_id=draft_id,
            preview_id=preview_id,
        )
        gate_status = _gate_status(check, review_decision)
        apply_gate_id = f"apply_gate_state:{uuid4()}"
        authorization = None
        if gate_status == "open" and review_decision and rollback_plan and dry_run_report:
            authorization = ApplyGateAuthorization(
                authorization_id=f"apply_gate_authorization:{uuid4()}",
                apply_gate_id=apply_gate_id,
                patch_candidate_id=patch_candidate_id,
                draft_id=draft_id,
                preview_id=preview_id,
                dry_run_report_id=dry_run_report.report_id,
                review_decision_id=review_decision.decision_id,
                rollback_plan_id=rollback_plan.rollback_plan_id,
                evidence_refs=[{"ref_type": "apply_gate_precondition_check", "check_id": check.check_id}],
            )
        findings = self.finding_service.build_findings(check, review_decision, rollback_plan)
        return ApplyGateState(
            apply_gate_id=apply_gate_id,
            created_at=utc_now_iso(),
            patch_candidate_id=patch_candidate_id,
            draft_id=draft_id,
            preview_id=preview_id,
            static_safety_report_id=static_safety_report.report_id if static_safety_report else "",
            dry_run_report_id=dry_run_report.report_id if dry_run_report else "",
            review_decision_id=review_decision.decision_id if review_decision else None,
            rollback_plan_id=rollback_plan.rollback_plan_id if rollback_plan else None,
            precondition_check=check,
            authorization=authorization,
            gate_status=gate_status,
            review_approved=check.review_approved,
            apply_gate_opened=gate_status == "open",
            eligible_for_bounded_apply=gate_status == "open",
            safe_to_apply=False,
            patch_applied=False,
            file_write_performed=False,
            workspace_file_changed_emitted=False,
            shell_executed=False,
            test_lint_executed=False,
            findings=findings,
            limitations=[
                "Apply gate is not patch apply.",
                "Bounded apply is deferred to v0.22.6.",
                "safe_to_apply remains false in v0.22.5.",
            ],
        )


class HumanReviewApplyGateReportService:
    def build_report(
        self,
        *,
        review_request: HumanReviewRequest,
        review_decision: HumanReviewDecision | None,
        rollback_plan: RollbackPlanDescriptor | None,
        apply_gate_state: ApplyGateState,
    ) -> HumanReviewApplyGateReport:
        review_status = _review_status(review_decision)
        report_status = _report_status(apply_gate_state)
        return HumanReviewApplyGateReport(
            report_id=f"human_review_apply_gate_report:{uuid4()}",
            created_at=utc_now_iso(),
            review_request=review_request,
            review_decision=review_decision,
            rollback_plan=rollback_plan,
            apply_gate_state=apply_gate_state,
            findings=list(apply_gate_state.findings),
            report_status=report_status,
            review_status=review_status,
            gate_status=apply_gate_state.gate_status,
            eligible_for_bounded_apply=apply_gate_state.eligible_for_bounded_apply,
            safe_to_apply=False,
            patch_applied=False,
            file_write_performed=False,
            workspace_file_changed_emitted=False,
            shell_executed=False,
            test_lint_executed=False,
            limitations=[
                "Review decision is not execution.",
                "Apply gate is not patch apply.",
                "Rollback plan is a descriptor only.",
            ],
            withdrawal_conditions=[
                "Withdraw if files are written or patches are applied.",
                "Withdraw if safe_to_apply becomes true in v0.22.5.",
                "Withdraw if rollback execution or post-apply verification occurs.",
            ],
        )


class SelfModificationReviewGateService:
    def __init__(self, *, source_service: HumanReviewSourceService | None = None) -> None:
        self.source_service = source_service or HumanReviewSourceService()
        self.request_service = HumanReviewRequestService()
        self.decision_service = HumanReviewDecisionService()
        self.rollback_service = RollbackPlanService()
        self.apply_gate_service = ApplyGateService()
        self.report_service = HumanReviewApplyGateReportService()

    def request_review(
        self,
        *,
        patch_candidate_id: str | None = None,
        draft_id: str | None = None,
        preview_id: str | None = None,
        static_safety_report_id: str | None = None,
        dry_run_report_id: str | None = None,
    ) -> HumanReviewRequest:
        candidate = self.source_service.load_patch_candidate(patch_candidate_id)
        draft = self.source_service.load_patch_draft(draft_id)
        preview = self.source_service.load_diff_preview(preview_id)
        static_report = self.source_service.load_static_safety_report(static_safety_report_id)
        dry_report = self.source_service.load_dry_run_report(dry_run_report_id)
        return self.request_service.create_review_request(
            patch_candidate_id=candidate.candidate_id if candidate else (patch_candidate_id or "patch_candidate:unknown"),
            draft_id=draft.draft_id if draft else (draft_id or "patch_draft:unknown"),
            preview_id=preview.preview_id if preview else (preview_id or "diff_preview:unknown"),
            static_safety_report_id=static_report.report_id if static_report else (static_safety_report_id or "patch_static_safety_report:unknown"),
            dry_run_report_id=dry_report.report_id if dry_report else (dry_run_report_id or "patch_dry_run_report:unknown"),
        )

    def record_review_decision(
        self,
        *,
        review_request_id: str,
        decision: str,
        decision_reason: str | None = None,
        reviewer_ref: dict[str, Any] | None = None,
    ) -> HumanReviewDecision:
        return self.decision_service.record_decision(
            review_request_id=review_request_id,
            decision=decision,
            decision_reason=decision_reason,
            reviewer_ref=reviewer_ref,
        )

    def evaluate_apply_gate(
        self,
        *,
        review_request: HumanReviewRequest,
        review_decision: HumanReviewDecision | None,
        rollback_plan: RollbackPlanDescriptor | None = None,
    ) -> HumanReviewApplyGateResult:
        draft = self.source_service.load_patch_draft(review_request.draft_id)
        static_report = self.source_service.load_static_safety_report(review_request.static_safety_report_id)
        dry_report = self.source_service.load_dry_run_report(review_request.dry_run_report_id)
        plan = rollback_plan or self.rollback_service.build_rollback_plan(
            patch_candidate_id=review_request.patch_candidate_id,
            draft_id=review_request.draft_id,
            preview_id=review_request.preview_id,
            draft=draft,
        )
        state = self.apply_gate_service.evaluate_gate(
            patch_candidate_id=review_request.patch_candidate_id,
            draft_id=review_request.draft_id,
            preview_id=review_request.preview_id,
            static_safety_report=static_report,
            dry_run_report=dry_report,
            review_decision=review_decision,
            rollback_plan=plan,
        )
        report = self.report_service.build_report(
            review_request=review_request,
            review_decision=review_decision,
            rollback_plan=plan,
            apply_gate_state=state,
        )
        no_action = None
        needs_more_input = None
        if report.gate_status in {"blocked", "rejected", "closed"}:
            no_action = ApplyGateNoActionCandidate(
                candidate_id=f"apply_gate_no_action_candidate:{uuid4()}",
                report_id=report.report_id,
                reason="Apply gate did not open.",
                evidence_refs=_finding_evidence(report.findings),
            )
        if report.gate_status in {"needs_more_input", "revise_required"}:
            needs_more_input = ApplyGateNeedsMoreInputCandidate(
                candidate_id=f"apply_gate_needs_more_input_candidate:{uuid4()}",
                report_id=report.report_id,
                reason="Apply gate requires more input or revision.",
                missing_inputs=list(state.precondition_check.failed_preconditions),
                evidence_refs=_finding_evidence(report.findings),
            )
        return HumanReviewApplyGateResult(report=report, no_action_candidate=no_action, needs_more_input_candidate=needs_more_input)

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "report_name": "Self-Modification Human Review Apply Gate PIG Report",
            "version": SELF_MODIFICATION_REVIEW_GATE_VERSION,
            "layer": "self_modification_safety",
            "subject": "human_review_apply_gate",
            "principles": [
                "review decision is not execution",
                "review approval is not file mutation",
                "apply gate is not patch apply",
                "apply gate requires dry-run pass",
                "apply gate requires rollback plan",
                "apply gate requires explicit operator approval",
            ],
            "review_decision_allowed": True,
            "apply_gate_state_allowed": True,
            "patch_applied": False,
            "file_write_performed": False,
            "workspace_file_changed_emitted": False,
            "safe_to_apply": False,
            "shell_executed": False,
            "test_lint_executed": False,
            "llm_judge_enabled": False,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "projection_name": "Self-Modification Human Review Apply Gate OCPX Projection",
            "state": SELF_MODIFICATION_REVIEW_GATE_STATE,
            "version": SELF_MODIFICATION_REVIEW_GATE_VERSION,
            "source_read_models": [
                "PatchDryRunState",
                "PatchApplicabilityState",
                "PatchStaticSafetyState",
                "PatchDraftState",
                "DiffPreviewState",
                "PatchCandidateState",
                "SelfModificationLifecyclePolicyState",
            ],
            "target_read_models": [
                "HumanReviewState",
                "ApplyGateState",
                "RollbackPlanState",
                "BoundedApplyEligibilityState",
            ],
            "effect_types": ["read_only_observation", "state_candidate_created", "gate_state_created"],
        }

    def render_review_request_cli(self, request: HumanReviewRequest) -> str:
        return "\n".join(
            [
                "Self-Modification Human Review Request",
                "version=v0.22.5",
                "layer=self_modification_safety",
                f"review_request_id={request.review_request_id}",
                f"patch_candidate_id={request.patch_candidate_id}",
                f"draft_id={request.draft_id}",
                f"preview_id={request.preview_id}",
                f"dry_run_report_id={request.dry_run_report_id}",
                "raw_patch_content_included=false",
                "raw_file_content_included=false",
                "safe_to_apply=false",
                "patch_applied=false",
                "file_write_performed=false",
                "workspace_file_changed_emitted=false",
                "next_required_step=v0.22.5 Human Review Decision",
                "No file mutation occurred.",
                "private_full_paths_printed=False",
                "raw_full_file_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_decision_cli(self, decision: HumanReviewDecision) -> str:
        return "\n".join(
            [
                "Self-Modification Human Review Decision",
                "version=v0.22.5",
                "layer=self_modification_safety",
                f"review_decision_id={decision.decision_id}",
                f"review_request_id={decision.review_request_id}",
                f"decision={decision.decision}",
                f"approved_for_apply_gate={str(decision.approved_for_apply_gate).lower()}",
                "approved_for_direct_apply=false",
                "safe_to_apply=false",
                "patch_applied=false",
                "file_write_performed=false",
                "workspace_file_changed_emitted=false",
                "next_required_step=v0.22.5 Apply Gate Evaluation",
                "No file mutation occurred.",
                "private_full_paths_printed=False",
                "raw_full_file_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_result_cli(self, result: HumanReviewApplyGateResult) -> str:
        report = result.report
        state = report.apply_gate_state
        auth = state.authorization
        return "\n".join(
            [
                "Self-Modification Human Review Apply Gate",
                "version=v0.22.5",
                "layer=self_modification_safety",
                f"report_id={report.report_id}",
                f"review_request_id={report.review_request.review_request_id}",
                f"review_decision_id={report.review_decision.decision_id if report.review_decision else 'missing'}",
                f"apply_gate_id={state.apply_gate_id}",
                f"gate_status={state.gate_status}",
                f"eligible_for_bounded_apply={str(state.eligible_for_bounded_apply).lower()}",
                "safe_to_apply=false",
                "patch_applied=false",
                "file_write_performed=false",
                "workspace_file_changed_emitted=false",
                "shell_executed=false",
                "test_lint_executed=false",
                f"authorized_next_version={auth.authorized_next_version if auth else 'none'}",
                "next_required_step=v0.22.6 Bounded Patch Apply",
                "No file mutation occurred.",
                "private_full_paths_printed=False",
                "raw_full_file_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_gate_view_cli(self, *, apply_gate_id: str) -> str:
        return "\n".join(
            [
                "Self-Modification Apply Gate View",
                "version=v0.22.5",
                "layer=self_modification_safety",
                f"apply_gate_id={apply_gate_id}",
                "gate_status=not_persisted_in_v0.22.5",
                "eligible_for_bounded_apply=false",
                "safe_to_apply=false",
                "patch_applied=false",
                "file_write_performed=false",
                "workspace_file_changed_emitted=false",
                "authorized_next_version=v0.22.6",
                "next_required_step=v0.22.6 Bounded Patch Apply",
                "No file mutation occurred.",
                "private_full_paths_printed=False",
                "raw_full_file_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_rollback_plan_view_cli(self, *, rollback_plan_id: str) -> str:
        return "\n".join(
            [
                "Self-Modification Rollback Plan View",
                "version=v0.22.5",
                "layer=self_modification_safety",
                f"rollback_plan_id={rollback_plan_id}",
                "rollback_execution_enabled=false",
                "rollback_executed=false",
                "patch_applied=false",
                "file_write_performed=false",
                "workspace_file_changed_emitted=false",
                "safe_to_apply=false",
                "No file mutation occurred.",
                "private_full_paths_printed=False",
                "raw_full_file_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_pig_report_cli(self) -> str:
        report = self.build_pig_report()
        return "\n".join(
            [
                "Self-Modification Human Review Apply Gate PIG Report",
                "version=v0.22.5",
                "layer=self_modification_safety",
                f"subject={report['subject']}",
                f"principles={','.join(report['principles'])}",
                f"review_decision_allowed={str(report['review_decision_allowed']).lower()}",
                f"apply_gate_state_allowed={str(report['apply_gate_state_allowed']).lower()}",
                "patch_applied=false",
                "file_write_performed=false",
                "workspace_file_changed_emitted=false",
                "safe_to_apply=false",
                "shell_executed=false",
                "test_lint_executed=false",
                f"llm_judge_enabled={str(report['llm_judge_enabled']).lower()}",
                "file_write_enabled=false",
                "apply_patch_enabled=false",
                "no_file_mutation_occurred=true",
                "No file mutation occurred.",
                "private_full_paths_printed=False",
                "raw_file_content_printed=False",
                "raw_full_file_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_ocpx_projection_cli(self) -> str:
        projection = self.build_ocpx_projection()
        return "\n".join(
            [
                "Self-Modification Human Review Apply Gate OCPX Projection",
                "version=v0.22.5",
                "layer=self_modification_safety",
                f"state={projection['state']}",
                f"source_read_models={','.join(projection['source_read_models'])}",
                f"target_read_models={','.join(projection['target_read_models'])}",
                f"effect_types={','.join(projection['effect_types'])}",
                "safe_to_apply=false",
                "patch_applied=false",
                "file_write_performed=false",
                "workspace_file_changed_emitted=false",
                "file_write_enabled=false",
                "apply_patch_enabled=false",
                "no_file_mutation_occurred=true",
                "No file mutation occurred.",
                "private_full_paths_printed=False",
                "raw_file_content_printed=False",
                "raw_full_file_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )


def _load_by_id(items: dict[str, Any], object_id: str | None, allow_synthetic: bool) -> Any | None:
    if object_id is None:
        return next(iter(items.values()), None)
    found = items.get(object_id)
    if found is None and allow_synthetic:
        return next(iter(items.values()), None)
    return found


def _has_finding(report: PatchDryRunReport | None, finding_type: str) -> bool:
    return bool(report and any(item.finding_type == finding_type for item in report.findings))


def _finding(finding_type: str, severity: str, message: str, check_id: str) -> ApplyGateFinding:
    return ApplyGateFinding(
        finding_id=f"apply_gate_finding:{uuid4()}",
        severity=severity,
        finding_type=finding_type,
        message=message,
        target_ref=None,
        gate_ref={"ref_type": "apply_gate_precondition_check", "check_id": check_id},
        evidence_refs=[{"ref_type": "review_gate_version", "version": SELF_MODIFICATION_REVIEW_GATE_VERSION}],
        withdrawal_condition="Withdraw if review/apply gate writes files, applies patches, or marks safe_to_apply true.",
    )


def _finding_type_for_precondition(precondition: str) -> str:
    return {
        "static_safety_report_required_or_not_passed": "static_safety_not_passed",
        "dry_run_report_required_or_not_passed": "dry_run_not_passed",
        "dry_run_eligible_for_review_required": "dry_run_not_passed",
        "review_approval_required": "missing_review_decision",
        "rollback_plan_required": "missing_rollback_plan",
        "private_boundary_clear_required": "private_boundary_risk",
        "secret_boundary_clear_required": "secret_boundary_risk",
        "target_still_within_scope_required": "target_scope_changed",
    }.get(precondition, "apply_gate_not_allowed")


def _gate_status(check: ApplyGatePreconditionCheck, decision: HumanReviewDecision | None) -> str:
    if decision:
        if decision.decision == "reject":
            return "rejected"
        if decision.decision == "revise":
            return "revise_required"
        if decision.decision == "needs_more_input":
            return "needs_more_input"
        if decision.decision == "no_action":
            return "closed"
    if check.apply_gate_allowed:
        return "open"
    if "review_approval_required" in check.failed_preconditions:
        return "needs_more_input"
    return "blocked"


def _review_status(decision: HumanReviewDecision | None) -> str:
    if decision is None:
        return "missing"
    return {
        "approve": "approved",
        "reject": "rejected",
        "revise": "revise_required",
        "no_action": "no_action",
        "needs_more_input": "needs_more_input",
    }.get(decision.decision, "needs_more_input")


def _report_status(state: ApplyGateState) -> str:
    if state.gate_status == "open":
        return "passed"
    if state.gate_status in {"needs_more_input", "revise_required"}:
        return "warning"
    if state.gate_status == "rejected":
        return "failed"
    return "blocked"


def _finding_evidence(findings: list[ApplyGateFinding]) -> list[dict[str, Any]]:
    return [{"finding_type": item.finding_type, "severity": item.severity} for item in findings[:20]]
