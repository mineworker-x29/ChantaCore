from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import uuid4

from chanta_core.self_modification_safety.bounded_apply import (
    BoundedPatchApplyReport,
    BoundedPatchApplyTransaction,
    WorkspaceFileChangeRecord,
)
from chanta_core.self_modification_safety.review_gate import ApplyGateAuthorization, RollbackPlanDescriptor
from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace.errors import WorkspacePathViolationError
from chanta_core.workspace.read_service import resolve_workspace_path


SELF_MODIFICATION_POST_APPLY_VERSION = "v0.22.7"
SELF_MODIFICATION_POST_APPLY_STATE = "self_modification_post_apply_verified_outcome_recorded"
POST_APPLY_VERIFY_SKILL_ID = "skill:self_modification_post_apply_verify"
OUTCOME_RECORD_SKILL_ID = "skill:self_modification_outcome_record"


@dataclass(frozen=True)
class PostApplyVerificationRequest:
    apply_report_id: str
    transaction_id: str | None = None
    change_ids: list[str] = field(default_factory=list)
    include_hash_verification: bool = True
    include_ocel_trace_verification: bool = True
    include_authorization_verification: bool = True
    include_rollback_readiness: bool = True
    include_scope_verification: bool = True
    include_safety_regression_check: bool = True
    include_outcome_record: bool = True
    max_changed_files: int = 1
    strictness: str = "strict"

    def normalized(self) -> "PostApplyVerificationRequest":
        return PostApplyVerificationRequest(
            apply_report_id=str(self.apply_report_id or "").strip(),
            transaction_id=str(self.transaction_id).strip() if self.transaction_id else None,
            change_ids=[str(item).strip() for item in self.change_ids if str(item).strip()],
            include_hash_verification=bool(self.include_hash_verification),
            include_ocel_trace_verification=bool(self.include_ocel_trace_verification),
            include_authorization_verification=bool(self.include_authorization_verification),
            include_rollback_readiness=bool(self.include_rollback_readiness),
            include_scope_verification=bool(self.include_scope_verification),
            include_safety_regression_check=bool(self.include_safety_regression_check),
            include_outcome_record=bool(self.include_outcome_record),
            max_changed_files=max(1, int(self.max_changed_files)),
            strictness=self.strictness or "strict",
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "apply_report_id": self.apply_report_id,
            "transaction_id": self.transaction_id,
            "change_ids": list(self.change_ids),
            "include_hash_verification": self.include_hash_verification,
            "include_ocel_trace_verification": self.include_ocel_trace_verification,
            "include_authorization_verification": self.include_authorization_verification,
            "include_rollback_readiness": self.include_rollback_readiness,
            "include_scope_verification": self.include_scope_verification,
            "include_safety_regression_check": self.include_safety_regression_check,
            "include_outcome_record": self.include_outcome_record,
            "max_changed_files": self.max_changed_files,
            "strictness": self.strictness,
        }


@dataclass(frozen=True)
class PostApplyVerificationSourceBundle:
    bundle_id: str
    apply_report_ref: dict[str, Any]
    transaction_ref: dict[str, Any] | None
    change_record_refs: list[dict[str, Any]]
    workspace_file_changed_event_refs: list[dict[str, Any]]
    rollback_plan_ref: dict[str, Any] | None
    authorization_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    source_status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "bundle_id": self.bundle_id,
            "apply_report_ref": dict(self.apply_report_ref),
            "transaction_ref": dict(self.transaction_ref) if self.transaction_ref else None,
            "change_record_refs": [dict(item) for item in self.change_record_refs],
            "workspace_file_changed_event_refs": [dict(item) for item in self.workspace_file_changed_event_refs],
            "rollback_plan_ref": dict(self.rollback_plan_ref) if self.rollback_plan_ref else None,
            "authorization_ref": dict(self.authorization_ref) if self.authorization_ref else None,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "source_status": self.source_status,
        }


@dataclass(frozen=True)
class PostApplyTargetSnapshot:
    snapshot_id: str
    target_id: str
    relative_path: str
    current_hash: str | None
    current_line_count: int | None
    current_byte_count: int | None
    encoding: str | None
    line_ending: str | None
    target_exists: bool
    target_is_file: bool
    private_boundary_risk: bool
    secret_risk: bool
    raw_content_emitted: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "target_id": self.target_id,
            "relative_path": self.relative_path,
            "current_hash": self.current_hash,
            "current_line_count": self.current_line_count,
            "current_byte_count": self.current_byte_count,
            "encoding": self.encoding,
            "line_ending": self.line_ending,
            "target_exists": self.target_exists,
            "target_is_file": self.target_is_file,
            "private_boundary_risk": self.private_boundary_risk,
            "secret_risk": self.secret_risk,
            "raw_content_emitted": self.raw_content_emitted,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class PostApplyHashVerificationResult:
    result_id: str
    change_id: str
    target_id: str
    relative_path: str
    expected_before_hash: str | None
    expected_after_hash: str | None
    current_hash: str | None
    before_hash_recorded: bool
    after_hash_recorded: bool
    current_matches_after_hash: bool
    hash_status: str
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "change_id": self.change_id,
            "target_id": self.target_id,
            "relative_path": self.relative_path,
            "expected_before_hash": self.expected_before_hash,
            "expected_after_hash": self.expected_after_hash,
            "current_hash": self.current_hash,
            "before_hash_recorded": self.before_hash_recorded,
            "after_hash_recorded": self.after_hash_recorded,
            "current_matches_after_hash": self.current_matches_after_hash,
            "hash_status": self.hash_status,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class PostApplyOCELTraceVerificationResult:
    result_id: str
    transaction_id: str
    workspace_file_changed_event_id: str | None
    event_exists: bool
    event_references_workspace_file: bool
    event_references_transaction: bool
    event_references_change_record: bool
    before_hash_relation_exists: bool
    after_hash_relation_exists: bool
    bounded_apply_report_relation_exists: bool
    trace_status: str
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "transaction_id": self.transaction_id,
            "workspace_file_changed_event_id": self.workspace_file_changed_event_id,
            "event_exists": self.event_exists,
            "event_references_workspace_file": self.event_references_workspace_file,
            "event_references_transaction": self.event_references_transaction,
            "event_references_change_record": self.event_references_change_record,
            "before_hash_relation_exists": self.before_hash_relation_exists,
            "after_hash_relation_exists": self.after_hash_relation_exists,
            "bounded_apply_report_relation_exists": self.bounded_apply_report_relation_exists,
            "trace_status": self.trace_status,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class PostApplyAuthorizationVerificationResult:
    result_id: str
    authorization_id: str | None
    authorization_exists: bool
    authorization_consumed: bool
    consumed_by_transaction: bool
    reused_after_consumption: bool
    authorization_status: str
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "authorization_id": self.authorization_id,
            "authorization_exists": self.authorization_exists,
            "authorization_consumed": self.authorization_consumed,
            "consumed_by_transaction": self.consumed_by_transaction,
            "reused_after_consumption": self.reused_after_consumption,
            "authorization_status": self.authorization_status,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class PostApplyRollbackReadinessResult:
    result_id: str
    rollback_plan_id: str | None
    rollback_plan_exists: bool
    rollback_possible: bool
    rollback_execution_enabled: bool
    rollback_executed: bool
    before_snapshot_refs_available: bool
    reverse_operation_refs_available: bool
    rollback_status: str
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "rollback_plan_id": self.rollback_plan_id,
            "rollback_plan_exists": self.rollback_plan_exists,
            "rollback_possible": self.rollback_possible,
            "rollback_execution_enabled": self.rollback_execution_enabled,
            "rollback_executed": self.rollback_executed,
            "before_snapshot_refs_available": self.before_snapshot_refs_available,
            "reverse_operation_refs_available": self.reverse_operation_refs_available,
            "rollback_status": self.rollback_status,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class PostApplyScopeVerificationResult:
    result_id: str
    approved_target_count: int
    changed_file_count: int
    approved_operation_count: int
    applied_operation_count: int
    unexpected_target_refs: list[dict[str, Any]]
    unexpected_operation_refs: list[dict[str, Any]]
    scope_status: str
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "approved_target_count": self.approved_target_count,
            "changed_file_count": self.changed_file_count,
            "approved_operation_count": self.approved_operation_count,
            "applied_operation_count": self.applied_operation_count,
            "unexpected_target_refs": [dict(item) for item in self.unexpected_target_refs],
            "unexpected_operation_refs": [dict(item) for item in self.unexpected_operation_refs],
            "scope_status": self.scope_status,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class PostApplySafetyRegressionCheck:
    check_id: str
    dangerous_pattern_detected: bool
    permission_grant_pattern_detected: bool
    shell_network_mcp_plugin_pattern_detected: bool
    memory_persona_overlay_mutation_pattern_detected: bool
    raw_secret_exposure_risk: bool
    regression_status: str
    findings: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "dangerous_pattern_detected": self.dangerous_pattern_detected,
            "permission_grant_pattern_detected": self.permission_grant_pattern_detected,
            "shell_network_mcp_plugin_pattern_detected": self.shell_network_mcp_plugin_pattern_detected,
            "memory_persona_overlay_mutation_pattern_detected": self.memory_persona_overlay_mutation_pattern_detected,
            "raw_secret_exposure_risk": self.raw_secret_exposure_risk,
            "regression_status": self.regression_status,
            "findings": [dict(item) for item in self.findings],
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class PostApplyVerificationFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    target_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "finding_type": self.finding_type,
            "message": self.message,
            "target_ref": dict(self.target_ref) if self.target_ref else None,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "withdrawal_condition": self.withdrawal_condition,
        }


@dataclass(frozen=True)
class PostApplyVerificationReport:
    report_id: str
    created_at: str
    request: PostApplyVerificationRequest
    source_bundle: PostApplyVerificationSourceBundle
    target_snapshots: list[PostApplyTargetSnapshot]
    hash_results: list[PostApplyHashVerificationResult]
    ocel_trace_results: list[PostApplyOCELTraceVerificationResult]
    authorization_result: PostApplyAuthorizationVerificationResult | None
    rollback_result: PostApplyRollbackReadinessResult | None
    scope_result: PostApplyScopeVerificationResult | None
    safety_regression_check: PostApplySafetyRegressionCheck | None
    findings: list[PostApplyVerificationFinding]
    verification_status: str
    changed_file_count: int
    verified_change_count: int
    failed_change_count: int
    rollback_recommended: bool
    outcome_record_required: bool = True
    file_write_performed: bool = False
    additional_patch_applied: bool = False
    shell_executed: bool = False
    test_lint_executed: bool = False
    rollback_executed: bool = False
    raw_content_emitted: bool = False
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until file changes again or rollback/outcome state changes."

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "created_at": self.created_at,
            "request": self.request.to_dict(),
            "source_bundle": self.source_bundle.to_dict(),
            "target_snapshots": [item.to_dict() for item in self.target_snapshots],
            "hash_results": [item.to_dict() for item in self.hash_results],
            "ocel_trace_results": [item.to_dict() for item in self.ocel_trace_results],
            "authorization_result": self.authorization_result.to_dict() if self.authorization_result else None,
            "rollback_result": self.rollback_result.to_dict() if self.rollback_result else None,
            "scope_result": self.scope_result.to_dict() if self.scope_result else None,
            "safety_regression_check": self.safety_regression_check.to_dict() if self.safety_regression_check else None,
            "findings": [item.to_dict() for item in self.findings],
            "verification_status": self.verification_status,
            "changed_file_count": self.changed_file_count,
            "verified_change_count": self.verified_change_count,
            "failed_change_count": self.failed_change_count,
            "rollback_recommended": self.rollback_recommended,
            "outcome_record_required": self.outcome_record_required,
            "file_write_performed": self.file_write_performed,
            "additional_patch_applied": self.additional_patch_applied,
            "shell_executed": self.shell_executed,
            "test_lint_executed": self.test_lint_executed,
            "rollback_executed": self.rollback_executed,
            "raw_content_emitted": self.raw_content_emitted,
            "limitations": list(self.limitations),
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "validity_horizon": self.validity_horizon,
        }


@dataclass(frozen=True)
class ModificationOutcomeRecord:
    outcome_id: str
    created_at: str
    apply_report_id: str
    post_apply_verification_report_id: str
    transaction_id: str | None
    outcome_status: str
    outcome_summary: str
    changed_file_refs: list[dict[str, Any]]
    workspace_file_changed_event_refs: list[dict[str, Any]]
    verification_finding_refs: list[dict[str, Any]]
    rollback_recommended: bool
    rollback_plan_ref: dict[str, Any] | None
    next_required_action: str | None
    canonical_promotion_enabled: bool = False
    memory_mutation_enabled: bool = False
    persona_mutation_enabled: bool = False
    overlay_mutation_enabled: bool = False
    outcome_recorded: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "outcome_id": self.outcome_id,
            "created_at": self.created_at,
            "apply_report_id": self.apply_report_id,
            "post_apply_verification_report_id": self.post_apply_verification_report_id,
            "transaction_id": self.transaction_id,
            "outcome_status": self.outcome_status,
            "outcome_summary": self.outcome_summary,
            "changed_file_refs": [dict(item) for item in self.changed_file_refs],
            "workspace_file_changed_event_refs": [dict(item) for item in self.workspace_file_changed_event_refs],
            "verification_finding_refs": [dict(item) for item in self.verification_finding_refs],
            "rollback_recommended": self.rollback_recommended,
            "rollback_plan_ref": dict(self.rollback_plan_ref) if self.rollback_plan_ref else None,
            "next_required_action": self.next_required_action,
            "canonical_promotion_enabled": self.canonical_promotion_enabled,
            "memory_mutation_enabled": self.memory_mutation_enabled,
            "persona_mutation_enabled": self.persona_mutation_enabled,
            "overlay_mutation_enabled": self.overlay_mutation_enabled,
            "outcome_recorded": self.outcome_recorded,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class PostApplyNeedsMoreInputCandidate:
    candidate_id: str
    verification_report_id: str | None
    reason: str
    missing_inputs: list[str]
    evidence_refs: list[dict[str, Any]]
    recommended_review_decision: str = "needs_more_input"
    candidate_status: str = "candidate_only"

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "verification_report_id": self.verification_report_id,
            "reason": self.reason,
            "missing_inputs": list(self.missing_inputs),
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "recommended_review_decision": self.recommended_review_decision,
            "candidate_status": self.candidate_status,
        }


@dataclass(frozen=True)
class PostApplyRollbackRecommendedCandidate:
    candidate_id: str
    verification_report_id: str
    reason: str
    rollback_plan_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    recommended_review_decision: str = "review_rollback"
    candidate_status: str = "candidate_only"
    rollback_executed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "verification_report_id": self.verification_report_id,
            "reason": self.reason,
            "rollback_plan_ref": dict(self.rollback_plan_ref) if self.rollback_plan_ref else None,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "recommended_review_decision": self.recommended_review_decision,
            "candidate_status": self.candidate_status,
            "rollback_executed": self.rollback_executed,
        }


@dataclass(frozen=True)
class PostApplyVerificationOutcomeResult:
    verification_report: PostApplyVerificationReport
    outcome_record: ModificationOutcomeRecord | None
    needs_more_input_candidate: PostApplyNeedsMoreInputCandidate | None = None
    rollback_recommended_candidate: PostApplyRollbackRecommendedCandidate | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "verification_report": self.verification_report.to_dict(),
            "outcome_record": self.outcome_record.to_dict() if self.outcome_record else None,
            "needs_more_input_candidate": (
                self.needs_more_input_candidate.to_dict() if self.needs_more_input_candidate else None
            ),
            "rollback_recommended_candidate": (
                self.rollback_recommended_candidate.to_dict() if self.rollback_recommended_candidate else None
            ),
        }


class PostApplyVerificationSourceService:
    def __init__(
        self,
        *,
        workspace_root: str | Path | None = None,
        apply_reports: dict[str, BoundedPatchApplyReport] | None = None,
        transactions: dict[str, BoundedPatchApplyTransaction] | None = None,
        change_records: dict[str, WorkspaceFileChangeRecord] | None = None,
        workspace_file_changed_events: dict[str, dict[str, Any]] | None = None,
        rollback_plans: dict[str, RollbackPlanDescriptor] | None = None,
        authorizations: dict[str, ApplyGateAuthorization] | None = None,
    ) -> None:
        self.workspace_root = Path(workspace_root or ".").resolve(strict=False)
        self.apply_reports = dict(apply_reports or {})
        self.transactions = dict(transactions or {})
        self.change_records = dict(change_records or {})
        self.workspace_file_changed_events = dict(workspace_file_changed_events or {})
        self.rollback_plans = dict(rollback_plans or {})
        self.authorizations = dict(authorizations or {})

    def load_apply_report(self, apply_report_id: str) -> BoundedPatchApplyReport | None:
        return self.apply_reports.get(apply_report_id)

    def load_transaction(self, transaction_id: str | None, apply_report: BoundedPatchApplyReport | None = None) -> BoundedPatchApplyTransaction | None:
        if transaction_id and transaction_id in self.transactions:
            return self.transactions[transaction_id]
        if apply_report and apply_report.transaction:
            return apply_report.transaction
        return None

    def load_change_records(self, apply_report: BoundedPatchApplyReport | None) -> list[WorkspaceFileChangeRecord]:
        if apply_report and apply_report.transaction:
            records = apply_report.transaction.file_changes
        else:
            records = []
        if self.change_records:
            merged = {item.change_id: item for item in records}
            merged.update(self.change_records)
            return list(merged.values())
        return list(records)

    def load_workspace_file_changed_events(self, change_records: list[WorkspaceFileChangeRecord]) -> list[dict[str, Any]]:
        events: list[dict[str, Any]] = []
        for change in change_records:
            event_id = change.workspace_file_changed_event_id
            if not event_id:
                continue
            event = self.workspace_file_changed_events.get(event_id)
            if event is None:
                event = {
                    "event_id": event_id,
                    "event_type": "workspace_file_changed",
                    "target_id": change.target_id,
                    "change_id": change.change_id,
                    "relative_path": change.relative_path,
                    "before_hash": change.before_hash,
                    "after_hash": change.after_hash,
                }
            events.append(dict(event))
        return events

    def load_rollback_plan(self, apply_report: BoundedPatchApplyReport | None) -> RollbackPlanDescriptor | None:
        if not apply_report or not apply_report.transaction:
            return None
        return self.rollback_plans.get(apply_report.transaction.rollback_plan_id)

    def load_authorization(self, apply_report: BoundedPatchApplyReport | None) -> ApplyGateAuthorization | None:
        if not apply_report or not apply_report.transaction:
            return None
        return self.authorizations.get(apply_report.transaction.authorization_id)

    def build_source_bundle(
        self,
        apply_report: BoundedPatchApplyReport | None,
        transaction: BoundedPatchApplyTransaction | None,
        change_records: list[WorkspaceFileChangeRecord],
        events: list[dict[str, Any]],
        rollback_plan: RollbackPlanDescriptor | None,
        authorization: ApplyGateAuthorization | None,
    ) -> PostApplyVerificationSourceBundle:
        missing = []
        if apply_report is None:
            missing.append("apply_report")
        if transaction is None:
            missing.append("transaction")
        if not change_records:
            missing.append("change_record")
        status = "complete" if not missing else "missing"
        if apply_report is not None and missing:
            status = "partial"
        return PostApplyVerificationSourceBundle(
            bundle_id=f"post_apply_source_bundle:{uuid4()}",
            apply_report_ref={"ref_type": "bounded_patch_apply_report", "report_id": apply_report.report_id}
            if apply_report
            else {},
            transaction_ref={"ref_type": "bounded_patch_apply_transaction", "transaction_id": transaction.transaction_id}
            if transaction
            else None,
            change_record_refs=[
                {"ref_type": "workspace_file_change_record", "change_id": item.change_id, "target_id": item.target_id}
                for item in change_records
            ],
            workspace_file_changed_event_refs=[
                {"ref_type": "workspace_file_changed_event", "event_id": item.get("event_id")} for item in events
            ],
            rollback_plan_ref={"ref_type": "rollback_plan_descriptor", "rollback_plan_id": rollback_plan.rollback_plan_id}
            if rollback_plan
            else None,
            authorization_ref={"ref_type": "apply_gate_authorization", "authorization_id": authorization.authorization_id}
            if authorization
            else None,
            evidence_refs=[{"ref_type": "post_apply_source_status", "status": status, "missing": missing}],
            source_status=status,
        )


class PostApplyTargetSnapshotService:
    def __init__(self, *, workspace_root: str | Path | None = None) -> None:
        self.workspace_root = Path(workspace_root or ".").resolve(strict=False)

    def collect_current_snapshots(self, change_records: list[WorkspaceFileChangeRecord]) -> list[PostApplyTargetSnapshot]:
        return [self._snapshot(change) for change in change_records]

    def _snapshot(self, change: WorkspaceFileChangeRecord) -> PostApplyTargetSnapshot:
        relative_path = change.relative_path
        private_boundary_risk = _is_private_path(relative_path)
        secret_risk = _is_secret_path(relative_path)
        try:
            target = resolve_workspace_path(self.workspace_root, relative_path)
            exists = target.exists()
            is_file = target.is_file() if exists else False
            if not exists or not is_file:
                return _empty_snapshot(change, exists=exists, is_file=is_file, private=private_boundary_risk, secret=secret_risk)
            data = target.read_bytes()
            text = data.decode("utf-8", errors="replace")
            return PostApplyTargetSnapshot(
                snapshot_id=f"post_apply_target_snapshot:{uuid4()}",
                target_id=change.target_id,
                relative_path=relative_path,
                current_hash=_hash_bytes(data),
                current_line_count=_line_count(text),
                current_byte_count=len(data),
                encoding="utf-8",
                line_ending=_line_ending(text),
                target_exists=True,
                target_is_file=True,
                private_boundary_risk=private_boundary_risk,
                secret_risk=secret_risk,
                raw_content_emitted=False,
                evidence_refs=[{"ref_type": "bounded_read", "target_id": change.target_id}],
            )
        except (OSError, WorkspacePathViolationError):
            return _empty_snapshot(change, exists=False, is_file=False, private=True, secret=secret_risk)


class PostApplyHashVerifier:
    def verify_hashes(
        self,
        change_records: list[WorkspaceFileChangeRecord],
        snapshots: list[PostApplyTargetSnapshot],
    ) -> list[PostApplyHashVerificationResult]:
        by_target = {item.target_id: item for item in snapshots}
        results: list[PostApplyHashVerificationResult] = []
        for change in change_records:
            snapshot = by_target.get(change.target_id)
            current_hash = snapshot.current_hash if snapshot else None
            matches = bool(current_hash and change.after_hash and current_hash == change.after_hash)
            if snapshot and not snapshot.target_exists:
                status = "blocked"
            elif not change.before_hash or not change.after_hash:
                status = "missing"
            elif matches:
                status = "matched"
            else:
                status = "mismatch"
            results.append(
                PostApplyHashVerificationResult(
                    result_id=f"post_apply_hash_verification_result:{uuid4()}",
                    change_id=change.change_id,
                    target_id=change.target_id,
                    relative_path=change.relative_path,
                    expected_before_hash=change.before_hash,
                    expected_after_hash=change.after_hash,
                    current_hash=current_hash,
                    before_hash_recorded=bool(change.before_hash),
                    after_hash_recorded=bool(change.after_hash),
                    current_matches_after_hash=matches,
                    hash_status=status,
                    evidence_refs=[{"ref_type": "post_apply_hash_verification", "change_id": change.change_id}],
                )
            )
        return results


class PostApplyOCELTraceVerifier:
    def verify_trace(
        self,
        transaction: BoundedPatchApplyTransaction | None,
        change_records: list[WorkspaceFileChangeRecord],
        events: list[dict[str, Any]],
        apply_report: BoundedPatchApplyReport | None = None,
    ) -> list[PostApplyOCELTraceVerificationResult]:
        event_ids = {str(item.get("event_id")): item for item in events if item.get("event_id")}
        results: list[PostApplyOCELTraceVerificationResult] = []
        transaction_id = transaction.transaction_id if transaction else ""
        for change in change_records:
            event_id = change.workspace_file_changed_event_id
            event = event_ids.get(str(event_id))
            event_exists = event is not None
            references_file = bool(event and event.get("target_id") == change.target_id)
            references_change = bool(event and event.get("change_id") == change.change_id)
            references_transaction = bool(transaction_id and (event is None or event.get("transaction_id", transaction_id) == transaction_id))
            before_rel = bool(event_exists and change.before_hash)
            after_rel = bool(event_exists and change.after_hash)
            report_rel = apply_report is not None and event_exists
            if not event_exists:
                status = "missing"
            elif all([references_file, references_transaction, references_change, before_rel, after_rel, report_rel]):
                status = "complete"
            else:
                status = "partial"
            results.append(
                PostApplyOCELTraceVerificationResult(
                    result_id=f"post_apply_ocel_trace_verification_result:{uuid4()}",
                    transaction_id=transaction_id,
                    workspace_file_changed_event_id=event_id,
                    event_exists=event_exists,
                    event_references_workspace_file=references_file,
                    event_references_transaction=references_transaction,
                    event_references_change_record=references_change,
                    before_hash_relation_exists=before_rel,
                    after_hash_relation_exists=after_rel,
                    bounded_apply_report_relation_exists=report_rel,
                    trace_status=status,
                    evidence_refs=[{"ref_type": "post_apply_trace_verification", "change_id": change.change_id}],
                )
            )
        return results


class PostApplyAuthorizationVerifier:
    def verify_authorization(
        self,
        authorization: ApplyGateAuthorization | None,
        transaction: BoundedPatchApplyTransaction | None,
    ) -> PostApplyAuthorizationVerificationResult:
        auth_id = authorization.authorization_id if authorization else (transaction.authorization_id if transaction else None)
        consumed = bool(authorization and authorization.consumed)
        consumed_by = False
        reused = False
        if authorization and transaction:
            evidence_text = " ".join(str(item) for item in authorization.evidence_refs)
            consumed_by = transaction.transaction_id in evidence_text or consumed
            reused = bool(authorization.consumed and not consumed_by)
        if authorization is None:
            status = "missing"
        elif reused:
            status = "reused"
        elif consumed:
            status = "consumed"
        else:
            status = "unconsumed"
        return PostApplyAuthorizationVerificationResult(
            result_id=f"post_apply_authorization_verification_result:{uuid4()}",
            authorization_id=auth_id,
            authorization_exists=authorization is not None,
            authorization_consumed=consumed,
            consumed_by_transaction=consumed_by,
            reused_after_consumption=reused,
            authorization_status=status,
            evidence_refs=[{"ref_type": "post_apply_authorization_verification", "authorization_id": auth_id}],
        )


class PostApplyRollbackReadinessVerifier:
    def verify_rollback_readiness(self, rollback_plan: RollbackPlanDescriptor | None) -> PostApplyRollbackReadinessResult:
        exists = rollback_plan is not None
        possible = bool(rollback_plan and rollback_plan.rollback_possible)
        execution_enabled = bool(rollback_plan and rollback_plan.rollback_execution_enabled)
        executed = bool(rollback_plan and rollback_plan.rollback_executed)
        before_refs = bool(rollback_plan and rollback_plan.before_snapshot_refs)
        reverse_refs = bool(rollback_plan and rollback_plan.reverse_operation_refs)
        if executed:
            status = "executed_unexpectedly"
        elif exists and possible and before_refs and reverse_refs:
            status = "ready"
        elif exists and possible:
            status = "partial"
        else:
            status = "unavailable"
        return PostApplyRollbackReadinessResult(
            result_id=f"post_apply_rollback_readiness_result:{uuid4()}",
            rollback_plan_id=rollback_plan.rollback_plan_id if rollback_plan else None,
            rollback_plan_exists=exists,
            rollback_possible=possible,
            rollback_execution_enabled=execution_enabled,
            rollback_executed=executed,
            before_snapshot_refs_available=before_refs,
            reverse_operation_refs_available=reverse_refs,
            rollback_status=status,
            evidence_refs=[{"ref_type": "post_apply_rollback_readiness", "rollback_status": status}],
        )


class PostApplyScopeVerifier:
    def verify_scope(
        self,
        transaction: BoundedPatchApplyTransaction | None,
        change_records: list[WorkspaceFileChangeRecord],
    ) -> PostApplyScopeVerificationResult:
        approved_targets = {item.target_id for item in transaction.operations} if transaction else set()
        approved_ops = {item.operation_id for item in transaction.operations} if transaction else set()
        changed_targets = {item.target_id for item in change_records}
        applied_ops = {op_id for item in change_records for op_id in item.applied_operation_ids}
        unexpected_targets = sorted(changed_targets - approved_targets)
        unexpected_ops = sorted(applied_ops - approved_ops)
        if transaction is None:
            status = "unknown"
        elif unexpected_targets or unexpected_ops:
            status = "mismatch"
        elif len(change_records) > 1:
            status = "warning"
        else:
            status = "matched"
        return PostApplyScopeVerificationResult(
            result_id=f"post_apply_scope_verification_result:{uuid4()}",
            approved_target_count=len(approved_targets),
            changed_file_count=len(changed_targets),
            approved_operation_count=len(approved_ops),
            applied_operation_count=len(applied_ops),
            unexpected_target_refs=[{"target_id": item} for item in unexpected_targets],
            unexpected_operation_refs=[{"operation_id": item} for item in unexpected_ops],
            scope_status=status,
            evidence_refs=[{"ref_type": "post_apply_scope_verification", "scope_status": status}],
        )


class PostApplySafetyRegressionVerifier:
    def verify_regression(
        self,
        change_records: list[WorkspaceFileChangeRecord],
        snapshots: list[PostApplyTargetSnapshot],
    ) -> PostApplySafetyRegressionCheck:
        scan_text = " ".join([item.relative_path for item in change_records] + [item.relative_path for item in snapshots]).lower()
        dangerous = any(token in scan_text for token in ["eval", "exec", "destructive", "dangerous"])
        permission = any(token in scan_text for token in ["sudo", "permission_grant", "permission grant"])
        shell_net = any(token in scan_text for token in ["shell", "network", "mcp", "plugin"])
        memory_mutation = any(token in scan_text for token in ["memory", "persona", "overlay"])
        secret_risk = any(item.secret_risk for item in snapshots)
        findings: list[dict[str, Any]] = []
        for label, present in [
            ("dangerous_pattern_detected", dangerous),
            ("permission_grant_pattern_detected", permission),
            ("shell_network_mcp_plugin_pattern_detected", shell_net),
            ("memory_persona_overlay_mutation_pattern_detected", memory_mutation),
            ("raw_secret_exposure_risk", secret_risk),
        ]:
            if present:
                findings.append({"finding_type": label, "severity": "error"})
        status = "failed" if findings else "passed"
        return PostApplySafetyRegressionCheck(
            check_id=f"post_apply_safety_regression_check:{uuid4()}",
            dangerous_pattern_detected=dangerous,
            permission_grant_pattern_detected=permission,
            shell_network_mcp_plugin_pattern_detected=shell_net,
            memory_persona_overlay_mutation_pattern_detected=memory_mutation,
            raw_secret_exposure_risk=secret_risk,
            regression_status=status,
            findings=findings,
            evidence_refs=[{"ref_type": "post_apply_safety_regression", "status": status}],
        )


class PostApplyVerificationFindingService:
    def build_findings(
        self,
        *,
        request: PostApplyVerificationRequest,
        apply_report: BoundedPatchApplyReport | None,
        transaction: BoundedPatchApplyTransaction | None,
        change_records: list[WorkspaceFileChangeRecord],
        snapshots: list[PostApplyTargetSnapshot],
        hash_results: list[PostApplyHashVerificationResult],
        trace_results: list[PostApplyOCELTraceVerificationResult],
        authorization_result: PostApplyAuthorizationVerificationResult | None,
        rollback_result: PostApplyRollbackReadinessResult | None,
        scope_result: PostApplyScopeVerificationResult | None,
        safety_regression_check: PostApplySafetyRegressionCheck | None,
    ) -> list[PostApplyVerificationFinding]:
        findings: list[PostApplyVerificationFinding] = []
        if apply_report is None:
            findings.append(_finding("critical", "missing_apply_report", "Bounded apply report is required.", None))
        if transaction is None:
            findings.append(_finding("critical", "missing_transaction", "Bounded apply transaction is required.", None))
        if not change_records:
            findings.append(_finding("critical", "missing_change_record", "Workspace file change record is required.", None))
        for snapshot in snapshots:
            target_ref = {"target_id": snapshot.target_id, "relative_path": snapshot.relative_path}
            if not snapshot.target_exists:
                findings.append(_finding("critical", "current_target_missing", "Current target is unavailable.", target_ref))
            if snapshot.private_boundary_risk:
                findings.append(_finding("critical", "unexpected_target_changed", "Private boundary risk blocks verification.", target_ref))
            if snapshot.secret_risk:
                findings.append(_finding("critical", "raw_secret_exposure_risk", "Secret boundary risk blocks verification.", target_ref))
        for result in hash_results:
            target_ref = {"target_id": result.target_id, "relative_path": result.relative_path}
            if result.hash_status == "mismatch":
                findings.append(_finding("error", "after_hash_mismatch", "Current hash differs from recorded after_hash.", target_ref))
            elif result.hash_status == "missing":
                findings.append(_finding("warning", "needs_more_input", "Recorded before/after hash is incomplete.", target_ref))
            elif result.hash_status == "matched":
                findings.append(_finding("info", "ok", "Current hash matches recorded after_hash.", target_ref))
        for result in trace_results:
            if result.trace_status == "missing":
                findings.append(_finding("error", "missing_workspace_file_changed_event", "Required workspace change event is missing.", None))
            elif result.trace_status == "partial":
                findings.append(_finding("warning", "ocel_trace_incomplete", "Workspace change trace is incomplete.", None))
        if authorization_result:
            if authorization_result.authorization_status == "missing":
                findings.append(_finding("error", "authorization_not_consumed", "Apply authorization is missing.", None))
            elif authorization_result.authorization_status == "unconsumed":
                findings.append(_finding("error", "authorization_not_consumed", "Apply authorization was not consumed.", None))
            elif authorization_result.authorization_status == "reused":
                findings.append(_finding("error", "authorization_reuse_detected", "Apply authorization reuse was detected.", None))
        if rollback_result:
            if rollback_result.rollback_status == "executed_unexpectedly":
                findings.append(_finding("error", "rollback_executed_unexpectedly", "Rollback execution is not part of v0.22.7.", None))
            elif rollback_result.rollback_status == "unavailable":
                findings.append(_finding("warning", "rollback_plan_missing", "Rollback readiness is unavailable.", None))
            elif rollback_result.rollback_status == "partial":
                findings.append(_finding("warning", "rollback_not_possible", "Rollback readiness is partial.", None))
        if scope_result:
            if scope_result.scope_status == "mismatch":
                findings.append(_finding("error", "scope_mismatch", "Applied scope differs from approved scope.", None))
            elif scope_result.scope_status == "unknown":
                findings.append(_finding("warning", "needs_more_input", "Scope cannot be verified without transaction.", None))
        if safety_regression_check and safety_regression_check.regression_status in {"failed", "blocked"}:
            findings.append(_finding("error", "post_apply_safety_regression", "Post-apply safety regression detected.", None))
        if not findings and request.apply_report_id:
            findings.append(_finding("info", "verification_passed", "Post-apply verification passed.", None))
        return findings[:300]


class PostApplyVerificationReportService:
    def __init__(
        self,
        *,
        source_service: PostApplyVerificationSourceService | None = None,
        snapshot_service: PostApplyTargetSnapshotService | None = None,
        hash_verifier: PostApplyHashVerifier | None = None,
        trace_verifier: PostApplyOCELTraceVerifier | None = None,
        authorization_verifier: PostApplyAuthorizationVerifier | None = None,
        rollback_verifier: PostApplyRollbackReadinessVerifier | None = None,
        scope_verifier: PostApplyScopeVerifier | None = None,
        regression_verifier: PostApplySafetyRegressionVerifier | None = None,
        finding_service: PostApplyVerificationFindingService | None = None,
    ) -> None:
        self.source_service = source_service or PostApplyVerificationSourceService()
        self.snapshot_service = snapshot_service or PostApplyTargetSnapshotService(
            workspace_root=self.source_service.workspace_root
        )
        self.hash_verifier = hash_verifier or PostApplyHashVerifier()
        self.trace_verifier = trace_verifier or PostApplyOCELTraceVerifier()
        self.authorization_verifier = authorization_verifier or PostApplyAuthorizationVerifier()
        self.rollback_verifier = rollback_verifier or PostApplyRollbackReadinessVerifier()
        self.scope_verifier = scope_verifier or PostApplyScopeVerifier()
        self.regression_verifier = regression_verifier or PostApplySafetyRegressionVerifier()
        self.finding_service = finding_service or PostApplyVerificationFindingService()

    def build_report(self, request: PostApplyVerificationRequest) -> PostApplyVerificationReport:
        request = request.normalized()
        apply_report = self.source_service.load_apply_report(request.apply_report_id)
        transaction = self.source_service.load_transaction(request.transaction_id, apply_report)
        change_records = self.source_service.load_change_records(apply_report)
        if request.change_ids:
            wanted = set(request.change_ids)
            change_records = [item for item in change_records if item.change_id in wanted]
        events = self.source_service.load_workspace_file_changed_events(change_records)
        rollback_plan = self.source_service.load_rollback_plan(apply_report)
        authorization = self.source_service.load_authorization(apply_report)
        source_bundle = self.source_service.build_source_bundle(
            apply_report, transaction, change_records, events, rollback_plan, authorization
        )
        snapshots = self.snapshot_service.collect_current_snapshots(change_records)
        hash_results = self.hash_verifier.verify_hashes(change_records, snapshots) if request.include_hash_verification else []
        trace_results = (
            self.trace_verifier.verify_trace(transaction, change_records, events, apply_report)
            if request.include_ocel_trace_verification
            else []
        )
        authorization_result = (
            self.authorization_verifier.verify_authorization(authorization, transaction)
            if request.include_authorization_verification
            else None
        )
        rollback_result = (
            self.rollback_verifier.verify_rollback_readiness(rollback_plan)
            if request.include_rollback_readiness
            else None
        )
        scope_result = self.scope_verifier.verify_scope(transaction, change_records) if request.include_scope_verification else None
        safety_regression_check = (
            self.regression_verifier.verify_regression(change_records, snapshots)
            if request.include_safety_regression_check
            else None
        )
        findings = self.finding_service.build_findings(
            request=request,
            apply_report=apply_report,
            transaction=transaction,
            change_records=change_records,
            snapshots=snapshots,
            hash_results=hash_results,
            trace_results=trace_results,
            authorization_result=authorization_result,
            rollback_result=rollback_result,
            scope_result=scope_result,
            safety_regression_check=safety_regression_check,
        )
        status = _verification_status(
            source_bundle,
            snapshots,
            hash_results,
            trace_results,
            authorization_result,
            rollback_result,
            scope_result,
            safety_regression_check,
        )
        failed_change_count = sum(1 for item in hash_results if item.hash_status in {"mismatch", "blocked"})
        verified_change_count = sum(1 for item in hash_results if item.hash_status == "matched")
        rollback_recommended = status == "failed" and bool(rollback_result and rollback_result.rollback_possible)
        return PostApplyVerificationReport(
            report_id=f"post_apply_verification_report:{uuid4()}",
            created_at=utc_now_iso(),
            request=request,
            source_bundle=source_bundle,
            target_snapshots=snapshots,
            hash_results=hash_results,
            ocel_trace_results=trace_results,
            authorization_result=authorization_result,
            rollback_result=rollback_result,
            scope_result=scope_result,
            safety_regression_check=safety_regression_check,
            findings=findings,
            verification_status=status,
            changed_file_count=len(change_records),
            verified_change_count=verified_change_count,
            failed_change_count=failed_change_count,
            rollback_recommended=rollback_recommended,
            limitations=["Read-only verification; tests, import checks, rollback, and additional patches are not executed."],
            withdrawal_conditions=[
                "Withdraw if v0.22.7 writes files, emits a new workspace_file_changed event, executes rollback, or runs shell/test/lint."
            ],
        )


class ModificationOutcomeRecordService:
    def record_outcome(self, verification_report: PostApplyVerificationReport) -> ModificationOutcomeRecord:
        status = _outcome_status(verification_report)
        return ModificationOutcomeRecord(
            outcome_id=f"modification_outcome_record:{uuid4()}",
            created_at=utc_now_iso(),
            apply_report_id=verification_report.request.apply_report_id,
            post_apply_verification_report_id=verification_report.report_id,
            transaction_id=verification_report.request.transaction_id
            or (verification_report.source_bundle.transaction_ref or {}).get("transaction_id"),
            outcome_status=status,
            outcome_summary=_outcome_summary(status),
            changed_file_refs=[
                {"ref_type": "workspace_file_change_record", "change_id": item.change_id, "target_id": item.target_id}
                for item in _change_records_from_bundle(verification_report.source_bundle)
            ],
            workspace_file_changed_event_refs=[
                dict(item) for item in verification_report.source_bundle.workspace_file_changed_event_refs
            ],
            verification_finding_refs=[
                {"ref_type": "post_apply_verification_finding", "finding_id": item.finding_id, "finding_type": item.finding_type}
                for item in verification_report.findings
            ],
            rollback_recommended=verification_report.rollback_recommended,
            rollback_plan_ref=verification_report.source_bundle.rollback_plan_ref,
            next_required_action=_next_required_action(status),
            evidence_refs=[{"ref_type": "post_apply_version", "version": SELF_MODIFICATION_POST_APPLY_VERSION}],
        )


class SelfModificationPostApplyVerificationService:
    def __init__(
        self,
        *,
        report_service: PostApplyVerificationReportService | None = None,
        outcome_service: ModificationOutcomeRecordService | None = None,
    ) -> None:
        self.report_service = report_service or PostApplyVerificationReportService()
        self.outcome_service = outcome_service or ModificationOutcomeRecordService()

    def verify_and_record_outcome(self, request: PostApplyVerificationRequest) -> PostApplyVerificationOutcomeResult:
        report = self.report_service.build_report(request)
        outcome = self.outcome_service.record_outcome(report) if request.include_outcome_record else None
        rollback_candidate = None
        needs_more_input = None
        if report.rollback_recommended:
            rollback_candidate = PostApplyRollbackRecommendedCandidate(
                candidate_id=f"post_apply_rollback_recommended_candidate:{uuid4()}",
                verification_report_id=report.report_id,
                reason="Verification failed and rollback plan appears available.",
                rollback_plan_ref=report.source_bundle.rollback_plan_ref,
                evidence_refs=[{"ref_type": "post_apply_verification_report", "report_id": report.report_id}],
            )
        if report.verification_status == "blocked":
            needs_more_input = PostApplyNeedsMoreInputCandidate(
                candidate_id=f"post_apply_needs_more_input_candidate:{uuid4()}",
                verification_report_id=report.report_id,
                reason="Required post-apply sources are missing or blocked.",
                missing_inputs=_missing_inputs(report),
                evidence_refs=[{"ref_type": "post_apply_verification_report", "report_id": report.report_id}],
            )
        return PostApplyVerificationOutcomeResult(
            verification_report=report,
            outcome_record=outcome,
            needs_more_input_candidate=needs_more_input,
            rollback_recommended_candidate=rollback_candidate,
        )

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": SELF_MODIFICATION_POST_APPLY_VERSION,
            "layer": "self_modification_safety",
            "subject": "post_apply_verification_outcome",
            "principles": [
                "post-apply verification is not another patch",
                "verification failure does not trigger automatic rollback",
                "outcome recording must be OCEL-visible",
                "bounded apply is incomplete until outcome is recorded",
            ],
            "additional_file_write_performed": False,
            "additional_patch_applied": False,
            "file_write_enabled": False,
            "apply_patch_enabled": False,
            "safe_to_apply": False,
            "post_apply_verified": False,
            "rollback_executed": False,
            "shell_executed": False,
            "test_lint_executed": False,
            "llm_judge_enabled": False,
            "memory_promotion_enabled": False,
            "no_file_mutation_occurred": True,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "version": SELF_MODIFICATION_POST_APPLY_VERSION,
            "layer": "self_modification_safety",
            "state": SELF_MODIFICATION_POST_APPLY_STATE,
            "source_read_models": [
                "BoundedPatchApplyState",
                "WorkspaceFileChangeState",
                "RollbackEligibilityState",
                "ApplyGateState",
                "PatchCandidateState",
            ],
            "target_read_models": [
                "PostApplyVerificationState",
                "ModificationOutcomeState",
                "RollbackRecommendationState",
                "SelfModificationCompletionState",
            ],
            "effect_types": ["read_only_observation", "state_candidate_created", "outcome_recorded"],
            "file_write_enabled": False,
            "apply_patch_enabled": False,
            "safe_to_apply": False,
            "post_apply_verified": False,
            "no_file_mutation_occurred": True,
        }

    def render_result_cli(self, result: PostApplyVerificationOutcomeResult) -> str:
        report = result.verification_report
        outcome = result.outcome_record
        auth_status = report.authorization_result.authorization_status if report.authorization_result else "missing"
        rollback_status = report.rollback_result.rollback_status if report.rollback_result else "unavailable"
        hash_summary = _summary_counts([item.hash_status for item in report.hash_results])
        trace_summary = _summary_counts([item.trace_status for item in report.ocel_trace_results])
        return "\n".join(
            [
                "Self-Modification Post-Apply Verification & Outcome",
                f"version={SELF_MODIFICATION_POST_APPLY_VERSION}",
                "layer=self_modification_safety",
                f"report_id={report.report_id}",
                f"verification_status={report.verification_status}",
                f"outcome_id={outcome.outcome_id if outcome else ''}",
                f"outcome_status={outcome.outcome_status if outcome else 'not_recorded'}",
                f"changed_file_count={report.changed_file_count}",
                f"hash_verification_summary={hash_summary}",
                f"ocel_trace_verification_summary={trace_summary}",
                f"authorization_consumed_status={auth_status}",
                f"rollback_readiness={rollback_status}",
                f"rollback_recommended={str(report.rollback_recommended).lower()}",
                f"file_write_performed={str(report.file_write_performed).lower()}",
                f"additional_patch_applied={str(report.additional_patch_applied).lower()}",
                f"shell_executed={str(report.shell_executed).lower()}",
                f"test_lint_executed={str(report.test_lint_executed).lower()}",
                f"rollback_executed={str(report.rollback_executed).lower()}",
                "raw_full_file_content_printed=False",
                "private_full_paths_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_report_view_cli(self, report_id: str) -> str:
        return "\n".join(
            [
                "Self-Modification Post-Apply Verification Report View",
                f"version={SELF_MODIFICATION_POST_APPLY_VERSION}",
                "layer=self_modification_safety",
                f"report_id={report_id}",
                "status=not_persisted_in_v0.22.7",
                "verification_status=unknown_without_persisted_report",
                "outcome_status=unknown_without_persisted_record",
                "changed_file_count=unknown",
                "hash_verification_summary=unknown",
                "ocel_trace_verification_summary=unknown",
                "authorization_consumed_status=unknown",
                "rollback_readiness=unknown",
                "rollback_recommended=unknown",
                "file_write_performed=false",
                "additional_patch_applied=false",
                "shell_executed=false",
                "test_lint_executed=false",
                "rollback_executed=false",
                "raw_full_file_content_printed=False",
                "private_full_paths_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_findings_cli(self, report_id: str) -> str:
        return "\n".join(
            [
                "Self-Modification Post-Apply Verification Findings",
                f"version={SELF_MODIFICATION_POST_APPLY_VERSION}",
                "layer=self_modification_safety",
                f"report_id={report_id}",
                "finding_types=missing_workspace_file_changed_event,after_hash_mismatch,authorization_not_consumed,scope_mismatch,post_apply_safety_regression",
                "file_write_performed=false",
                "additional_patch_applied=false",
                "rollback_executed=false",
                "raw_full_file_content_printed=False",
                "private_full_paths_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_outcome_view_cli(self, outcome_id: str) -> str:
        return "\n".join(
            [
                "Self-Modification Outcome Record View",
                f"version={SELF_MODIFICATION_POST_APPLY_VERSION}",
                "layer=self_modification_safety",
                f"outcome_id={outcome_id}",
                "status=not_persisted_in_v0.22.7",
                "outcome_status=unknown_without_persisted_record",
                "canonical_promotion_enabled=false",
                "memory_mutation_enabled=false",
                "persona_mutation_enabled=false",
                "overlay_mutation_enabled=false",
                "rollback_executed=false",
                "raw_full_file_content_printed=False",
                "private_full_paths_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_pig_report_cli(self) -> str:
        report = self.build_pig_report()
        return "\n".join(
            [
                "Self-Modification Post-Apply Verification & Outcome PIG Report",
                f"version={report['version']}",
                f"layer={report['layer']}",
                f"subject={report['subject']}",
                f"principles={','.join(report['principles'])}",
                f"additional_file_write_performed={str(report['additional_file_write_performed']).lower()}",
                f"additional_patch_applied={str(report['additional_patch_applied']).lower()}",
                f"file_write_enabled={str(report['file_write_enabled']).lower()}",
                f"apply_patch_enabled={str(report['apply_patch_enabled']).lower()}",
                f"safe_to_apply={str(report['safe_to_apply']).lower()}",
                f"post_apply_verified={str(report['post_apply_verified']).lower()}",
                f"rollback_executed={str(report['rollback_executed']).lower()}",
                f"shell_executed={str(report['shell_executed']).lower()}",
                f"test_lint_executed={str(report['test_lint_executed']).lower()}",
                f"llm_judge_enabled={str(report['llm_judge_enabled']).lower()}",
                f"memory_promotion_enabled={str(report['memory_promotion_enabled']).lower()}",
                f"no_file_mutation_occurred={str(report['no_file_mutation_occurred']).lower()}",
                "No file mutation occurred.",
                "raw_file_content_printed=False",
                "raw_full_file_content_printed=False",
                "private_full_paths_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_ocpx_projection_cli(self) -> str:
        projection = self.build_ocpx_projection()
        return "\n".join(
            [
                "Self-Modification Post-Apply Verification & Outcome OCPX Projection",
                f"version={projection['version']}",
                f"layer={projection['layer']}",
                f"state={projection['state']}",
                f"source_read_models={','.join(projection['source_read_models'])}",
                f"target_read_models={','.join(projection['target_read_models'])}",
                f"effect_types={','.join(projection['effect_types'])}",
                f"file_write_enabled={str(projection['file_write_enabled']).lower()}",
                f"apply_patch_enabled={str(projection['apply_patch_enabled']).lower()}",
                f"safe_to_apply={str(projection['safe_to_apply']).lower()}",
                f"post_apply_verified={str(projection['post_apply_verified']).lower()}",
                f"no_file_mutation_occurred={str(projection['no_file_mutation_occurred']).lower()}",
                "No file mutation occurred.",
                "raw_file_content_printed=False",
                "raw_full_file_content_printed=False",
                "private_full_paths_printed=False",
                "raw_secrets_printed=False",
            ]
        )


def _empty_snapshot(
    change: WorkspaceFileChangeRecord,
    *,
    exists: bool,
    is_file: bool,
    private: bool,
    secret: bool,
) -> PostApplyTargetSnapshot:
    return PostApplyTargetSnapshot(
        snapshot_id=f"post_apply_target_snapshot:{uuid4()}",
        target_id=change.target_id,
        relative_path=change.relative_path,
        current_hash=None,
        current_line_count=None,
        current_byte_count=None,
        encoding=None,
        line_ending=None,
        target_exists=exists,
        target_is_file=is_file,
        private_boundary_risk=private,
        secret_risk=secret,
        raw_content_emitted=False,
        evidence_refs=[{"ref_type": "post_apply_target_unavailable", "target_id": change.target_id}],
    )


def _verification_status(
    source_bundle: PostApplyVerificationSourceBundle,
    snapshots: list[PostApplyTargetSnapshot],
    hash_results: list[PostApplyHashVerificationResult],
    trace_results: list[PostApplyOCELTraceVerificationResult],
    authorization_result: PostApplyAuthorizationVerificationResult | None,
    rollback_result: PostApplyRollbackReadinessResult | None,
    scope_result: PostApplyScopeVerificationResult | None,
    safety_regression_check: PostApplySafetyRegressionCheck | None,
) -> str:
    if source_bundle.source_status in {"missing", "blocked"}:
        return "blocked"
    if any((not item.target_exists) or item.private_boundary_risk or item.secret_risk for item in snapshots):
        return "blocked"
    failed = (
        any(item.hash_status in {"mismatch", "blocked"} for item in hash_results)
        or any(item.trace_status == "missing" for item in trace_results)
        or bool(authorization_result and authorization_result.authorization_status in {"missing", "unconsumed", "reused", "invalid"})
        or bool(rollback_result and rollback_result.rollback_status == "executed_unexpectedly")
        or bool(scope_result and scope_result.scope_status == "mismatch")
        or bool(safety_regression_check and safety_regression_check.regression_status in {"failed", "blocked"})
    )
    if failed:
        return "failed"
    warning = (
        any(item.hash_status == "missing" for item in hash_results)
        or any(item.trace_status == "partial" for item in trace_results)
        or bool(rollback_result and rollback_result.rollback_status in {"partial", "unavailable"})
        or bool(scope_result and scope_result.scope_status in {"warning", "unknown"})
        or bool(safety_regression_check and safety_regression_check.regression_status == "warning")
    )
    if warning:
        return "warning"
    return "passed"


def _outcome_status(report: PostApplyVerificationReport) -> str:
    if report.verification_status == "passed":
        return "applied_verified"
    if report.verification_status == "warning":
        return "applied_with_warnings"
    if report.verification_status == "failed" and report.rollback_recommended:
        return "rollback_recommended"
    if report.verification_status == "failed":
        return "verification_failed"
    if report.verification_status == "blocked":
        return "blocked"
    return "needs_more_input"


def _outcome_summary(status: str) -> str:
    return {
        "applied_verified": "Bounded apply was verified and outcome was recorded.",
        "applied_with_warnings": "Bounded apply was recorded with non-critical verification warnings.",
        "rollback_recommended": "Verification failed and rollback review is recommended; rollback was not executed.",
        "verification_failed": "Verification failed and outcome was recorded for operator follow-up.",
        "blocked": "Verification was blocked by missing or unsafe source state.",
    }.get(status, "Verification requires more input.")


def _next_required_action(status: str) -> str | None:
    if status == "applied_verified":
        return "Self-modification cycle complete for this bounded apply."
    if status == "rollback_recommended":
        return "Operator review of rollback recommendation."
    if status in {"verification_failed", "blocked", "needs_more_input"}:
        return "Operator follow-up required."
    return "Review warning findings."


def _missing_inputs(report: PostApplyVerificationReport) -> list[str]:
    evidence = report.source_bundle.evidence_refs[0] if report.source_bundle.evidence_refs else {}
    missing = evidence.get("missing", [])
    return list(missing) if isinstance(missing, list) else []


def _change_records_from_bundle(bundle: PostApplyVerificationSourceBundle) -> list[WorkspaceFileChangeRecord]:
    return [
        WorkspaceFileChangeRecord(
            change_id=str(item.get("change_id", "")),
            target_id=str(item.get("target_id", "")),
            relative_path=str(item.get("relative_path", "")),
            change_type="text_patch",
            before_hash="",
            after_hash="",
            before_line_count=None,
            after_line_count=None,
            applied_operation_ids=[],
            rollback_plan_id="",
            workspace_file_changed_event_id=None,
        )
        for item in bundle.change_record_refs
    ]


def _finding(
    severity: str,
    finding_type: str,
    message: str,
    target_ref: dict[str, Any] | None,
) -> PostApplyVerificationFinding:
    return PostApplyVerificationFinding(
        finding_id=f"post_apply_verification_finding:{uuid4()}",
        severity=severity,
        finding_type=finding_type,
        message=message,
        target_ref=dict(target_ref) if target_ref else None,
        evidence_refs=[{"ref_type": "post_apply_version", "version": SELF_MODIFICATION_POST_APPLY_VERSION}],
        withdrawal_condition=(
            "Withdraw if v0.22.7 mutates files, emits a new workspace_file_changed event, "
            "runs shell/test/lint, or executes rollback."
        ),
    )


def _summary_counts(statuses: list[str]) -> str:
    if not statuses:
        return "none"
    counts = {status: statuses.count(status) for status in sorted(set(statuses))}
    return ",".join(f"{key}:{value}" for key, value in counts.items())


def _hash_bytes(data: bytes) -> str:
    import hashlib

    return hashlib.sha256(data).hexdigest()


def _line_count(text: str | None) -> int:
    if not text:
        return 0
    return len(text.splitlines())


def _line_ending(text: str) -> str:
    if "\r\n" in text:
        return "\r\n"
    if "\n" in text:
        return "\n"
    return "none"


def _is_private_path(relative_path: str | None) -> bool:
    if not relative_path:
        return False
    lowered = relative_path.replace("\\", "/").lower()
    return any(token in lowered for token in ["/private/", "vera", "personal", "secret/private"])


def _is_secret_path(relative_path: str | None) -> bool:
    if not relative_path:
        return False
    lowered = relative_path.lower()
    return any(token in lowered for token in [".env", "secret", "credential", "private_key", "token"])
