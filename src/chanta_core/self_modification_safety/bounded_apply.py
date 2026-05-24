from __future__ import annotations

from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any
from uuid import uuid4

from chanta_core.self_modification_safety.candidate import PatchCandidate
from chanta_core.self_modification_safety.draft import DiffPreviewArtifact, PatchDraft, PatchOperationDraft
from chanta_core.self_modification_safety.dry_run import PatchDryRunReport
from chanta_core.self_modification_safety.review_gate import (
    ApplyGateAuthorization,
    ApplyGateState,
    RollbackPlanDescriptor,
)
from chanta_core.self_modification_safety.static_safety import PatchStaticSafetyReport
from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace.errors import WorkspacePathViolationError
from chanta_core.workspace.read_service import resolve_workspace_path


SELF_MODIFICATION_BOUNDED_APPLY_VERSION = "v0.22.6"
SELF_MODIFICATION_BOUNDED_APPLY_STATE = "self_modification_bounded_patch_applied"
BOUNDED_PATCH_APPLY_SKILL_ID = "skill:self_modification_bounded_patch_apply"
CONFIRMATION_PHRASE = "APPLY BOUNDED PATCH"


@dataclass(frozen=True)
class BoundedPatchApplyRequest:
    apply_gate_id: str
    authorization_id: str
    patch_candidate_id: str
    draft_id: str
    preview_id: str
    dry_run_report_id: str
    static_safety_report_id: str
    rollback_plan_id: str
    operator_confirmation: bool
    confirmation_phrase: str | None = None
    expected_target_hashes: dict[str, str] = field(default_factory=dict)
    max_files: int = 1
    max_operations: int = 10
    strictness: str = "strict"

    def normalized(self) -> "BoundedPatchApplyRequest":
        return BoundedPatchApplyRequest(
            apply_gate_id=str(self.apply_gate_id or "").strip(),
            authorization_id=str(self.authorization_id or "").strip(),
            patch_candidate_id=str(self.patch_candidate_id or "").strip(),
            draft_id=str(self.draft_id or "").strip(),
            preview_id=str(self.preview_id or "").strip(),
            dry_run_report_id=str(self.dry_run_report_id or "").strip(),
            static_safety_report_id=str(self.static_safety_report_id or "").strip(),
            rollback_plan_id=str(self.rollback_plan_id or "").strip(),
            operator_confirmation=bool(self.operator_confirmation),
            confirmation_phrase=str(self.confirmation_phrase).strip() if self.confirmation_phrase else None,
            expected_target_hashes={str(key): str(value) for key, value in self.expected_target_hashes.items()},
            max_files=max(1, int(self.max_files)),
            max_operations=max(1, int(self.max_operations)),
            strictness=self.strictness or "strict",
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "apply_gate_id": self.apply_gate_id,
            "authorization_id": self.authorization_id,
            "patch_candidate_id": self.patch_candidate_id,
            "draft_id": self.draft_id,
            "preview_id": self.preview_id,
            "dry_run_report_id": self.dry_run_report_id,
            "static_safety_report_id": self.static_safety_report_id,
            "rollback_plan_id": self.rollback_plan_id,
            "operator_confirmation": self.operator_confirmation,
            "confirmation_phrase_present": self.confirmation_phrase is not None,
            "expected_target_hashes": dict(self.expected_target_hashes),
            "max_files": self.max_files,
            "max_operations": self.max_operations,
            "strictness": self.strictness,
        }


@dataclass(frozen=True)
class ApplyAuthorizationValidationResult:
    validation_id: str
    apply_gate_id: str
    authorization_id: str
    authorization_exists: bool
    gate_status_open: bool
    authorized_for_bounded_apply: bool
    authorized_next_version: str
    single_use: bool
    consumed: bool
    expired: bool
    patch_ids_match: bool
    rollback_plan_matches: bool
    operator_confirmed: bool
    validation_status: str
    failed_reasons: list[str]
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "validation_id": self.validation_id,
            "apply_gate_id": self.apply_gate_id,
            "authorization_id": self.authorization_id,
            "authorization_exists": self.authorization_exists,
            "gate_status_open": self.gate_status_open,
            "authorized_for_bounded_apply": self.authorized_for_bounded_apply,
            "authorized_next_version": self.authorized_next_version,
            "single_use": self.single_use,
            "consumed": self.consumed,
            "expired": self.expired,
            "patch_ids_match": self.patch_ids_match,
            "rollback_plan_matches": self.rollback_plan_matches,
            "operator_confirmed": self.operator_confirmed,
            "validation_status": self.validation_status,
            "failed_reasons": list(self.failed_reasons),
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class PreApplyTargetRevalidationResult:
    result_id: str
    target_id: str
    relative_path: str
    expected_hash: str | None
    current_hash: str | None
    hash_matches: bool
    target_exists: bool
    target_is_file: bool
    private_boundary_risk: bool
    secret_risk: bool
    generated_file_risk: bool
    revalidation_status: str
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "target_id": self.target_id,
            "relative_path": self.relative_path,
            "expected_hash": self.expected_hash,
            "current_hash": self.current_hash,
            "hash_matches": self.hash_matches,
            "target_exists": self.target_exists,
            "target_is_file": self.target_is_file,
            "private_boundary_risk": self.private_boundary_risk,
            "secret_risk": self.secret_risk,
            "generated_file_risk": self.generated_file_risk,
            "revalidation_status": self.revalidation_status,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class PreApplyOperationRevalidationResult:
    result_id: str
    operation_id: str
    target_id: str
    anchor_still_matches: bool
    old_text_still_matches: bool
    operation_within_scope: bool
    would_apply_in_memory: bool
    revalidation_status: str
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "operation_id": self.operation_id,
            "target_id": self.target_id,
            "anchor_still_matches": self.anchor_still_matches,
            "old_text_still_matches": self.old_text_still_matches,
            "operation_within_scope": self.operation_within_scope,
            "would_apply_in_memory": self.would_apply_in_memory,
            "revalidation_status": self.revalidation_status,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class PreApplyRevalidationReport:
    report_id: str
    created_at: str
    patch_candidate_id: str
    draft_id: str
    preview_id: str
    target_revalidation_results: list[PreApplyTargetRevalidationResult]
    operation_revalidation_results: list[PreApplyOperationRevalidationResult]
    revalidation_status: str
    target_drift_detected: bool
    private_boundary_clear: bool
    secret_boundary_clear: bool
    safe_to_mutate_under_gate: bool
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "created_at": self.created_at,
            "patch_candidate_id": self.patch_candidate_id,
            "draft_id": self.draft_id,
            "preview_id": self.preview_id,
            "target_revalidation_results": [item.to_dict() for item in self.target_revalidation_results],
            "operation_revalidation_results": [item.to_dict() for item in self.operation_revalidation_results],
            "revalidation_status": self.revalidation_status,
            "target_drift_detected": self.target_drift_detected,
            "private_boundary_clear": self.private_boundary_clear,
            "secret_boundary_clear": self.secret_boundary_clear,
            "safe_to_mutate_under_gate": self.safe_to_mutate_under_gate,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class BoundedPatchApplyOperation:
    operation_id: str
    operation_type: str
    target_id: str
    relative_path: str
    approved_operation_ref: dict[str, Any]
    applied: bool
    applied_line_start: int | None
    applied_line_end: int | None
    added_line_count: int
    removed_line_count: int
    operation_status: str
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "operation_type": self.operation_type,
            "target_id": self.target_id,
            "relative_path": self.relative_path,
            "approved_operation_ref": dict(self.approved_operation_ref),
            "applied": self.applied,
            "applied_line_start": self.applied_line_start,
            "applied_line_end": self.applied_line_end,
            "added_line_count": self.added_line_count,
            "removed_line_count": self.removed_line_count,
            "operation_status": self.operation_status,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class WorkspaceFileChangeRecord:
    change_id: str
    target_id: str
    relative_path: str
    change_type: str
    before_hash: str
    after_hash: str
    before_line_count: int | None
    after_line_count: int | None
    applied_operation_ids: list[str]
    rollback_plan_id: str
    workspace_file_changed_event_id: str | None
    raw_content_emitted: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "change_id": self.change_id,
            "target_id": self.target_id,
            "relative_path": self.relative_path,
            "change_type": self.change_type,
            "before_hash": self.before_hash,
            "after_hash": self.after_hash,
            "before_line_count": self.before_line_count,
            "after_line_count": self.after_line_count,
            "applied_operation_ids": list(self.applied_operation_ids),
            "rollback_plan_id": self.rollback_plan_id,
            "workspace_file_changed_event_id": self.workspace_file_changed_event_id,
            "raw_content_emitted": self.raw_content_emitted,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class BoundedPatchApplyTransaction:
    transaction_id: str
    created_at: str
    apply_gate_id: str
    authorization_id: str
    patch_candidate_id: str
    draft_id: str
    preview_id: str
    rollback_plan_id: str
    validation_result: ApplyAuthorizationValidationResult
    pre_apply_revalidation_report: PreApplyRevalidationReport
    operations: list[BoundedPatchApplyOperation]
    file_changes: list[WorkspaceFileChangeRecord]
    transaction_status: str
    authorization_consumed: bool
    rollback_plan_available: bool
    post_apply_verification_required: bool = True
    post_apply_verified: bool = False
    shell_executed: bool = False
    test_lint_executed: bool = False
    raw_content_emitted: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "transaction_id": self.transaction_id,
            "created_at": self.created_at,
            "apply_gate_id": self.apply_gate_id,
            "authorization_id": self.authorization_id,
            "patch_candidate_id": self.patch_candidate_id,
            "draft_id": self.draft_id,
            "preview_id": self.preview_id,
            "rollback_plan_id": self.rollback_plan_id,
            "validation_result": self.validation_result.to_dict(),
            "pre_apply_revalidation_report": self.pre_apply_revalidation_report.to_dict(),
            "operations": [item.to_dict() for item in self.operations],
            "file_changes": [item.to_dict() for item in self.file_changes],
            "transaction_status": self.transaction_status,
            "authorization_consumed": self.authorization_consumed,
            "rollback_plan_available": self.rollback_plan_available,
            "post_apply_verification_required": self.post_apply_verification_required,
            "post_apply_verified": self.post_apply_verified,
            "shell_executed": self.shell_executed,
            "test_lint_executed": self.test_lint_executed,
            "raw_content_emitted": self.raw_content_emitted,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class BoundedPatchApplyFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    target_ref: dict[str, Any] | None
    operation_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "finding_type": self.finding_type,
            "message": self.message,
            "target_ref": dict(self.target_ref) if self.target_ref else None,
            "operation_ref": dict(self.operation_ref) if self.operation_ref else None,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "withdrawal_condition": self.withdrawal_condition,
        }


@dataclass(frozen=True)
class BoundedPatchApplyReport:
    report_id: str
    created_at: str
    request: BoundedPatchApplyRequest
    transaction: BoundedPatchApplyTransaction | None
    findings: list[BoundedPatchApplyFinding]
    apply_status: str
    changed_file_count: int
    applied_operation_count: int
    failed_operation_count: int
    workspace_file_changed_emitted: bool
    authorization_consumed: bool
    rollback_plan_available: bool
    post_apply_verification_required: bool = True
    post_apply_verified: bool = False
    outcome_recorded: bool = False
    shell_executed: bool = False
    test_lint_executed: bool = False
    raw_content_emitted: bool = False
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until post-apply verification and outcome are recorded."

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "created_at": self.created_at,
            "request": self.request.to_dict(),
            "transaction": self.transaction.to_dict() if self.transaction else None,
            "findings": [item.to_dict() for item in self.findings],
            "apply_status": self.apply_status,
            "changed_file_count": self.changed_file_count,
            "applied_operation_count": self.applied_operation_count,
            "failed_operation_count": self.failed_operation_count,
            "workspace_file_changed_emitted": self.workspace_file_changed_emitted,
            "authorization_consumed": self.authorization_consumed,
            "rollback_plan_available": self.rollback_plan_available,
            "post_apply_verification_required": self.post_apply_verification_required,
            "post_apply_verified": self.post_apply_verified,
            "outcome_recorded": self.outcome_recorded,
            "shell_executed": self.shell_executed,
            "test_lint_executed": self.test_lint_executed,
            "raw_content_emitted": self.raw_content_emitted,
            "limitations": list(self.limitations),
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "validity_horizon": self.validity_horizon,
        }


@dataclass(frozen=True)
class BoundedPatchApplyResult:
    report: BoundedPatchApplyReport

    def to_dict(self) -> dict[str, Any]:
        return {"report": self.report.to_dict()}


class BoundedPatchApplySourceService:
    def __init__(
        self,
        *,
        workspace_root: str | Path | None = None,
        apply_gates: dict[str, ApplyGateState] | None = None,
        authorizations: dict[str, ApplyGateAuthorization] | None = None,
        patch_candidates: dict[str, PatchCandidate] | None = None,
        patch_drafts: dict[str, PatchDraft] | None = None,
        diff_previews: dict[str, DiffPreviewArtifact] | None = None,
        dry_run_reports: dict[str, PatchDryRunReport] | None = None,
        static_safety_reports: dict[str, PatchStaticSafetyReport] | None = None,
        rollback_plans: dict[str, RollbackPlanDescriptor] | None = None,
    ) -> None:
        self.workspace_root = Path(workspace_root or ".").resolve(strict=False)
        self.apply_gates = dict(apply_gates or {})
        self.authorizations = dict(authorizations or {})
        self.patch_candidates = dict(patch_candidates or {})
        self.patch_drafts = dict(patch_drafts or {})
        self.diff_previews = dict(diff_previews or {})
        self.dry_run_reports = dict(dry_run_reports or {})
        self.static_safety_reports = dict(static_safety_reports or {})
        self.rollback_plans = dict(rollback_plans or {})

    def load_apply_gate(self, apply_gate_id: str) -> ApplyGateState | None:
        return self.apply_gates.get(apply_gate_id)

    def load_authorization(self, authorization_id: str) -> ApplyGateAuthorization | None:
        return self.authorizations.get(authorization_id)

    def load_patch_candidate(self, patch_candidate_id: str) -> PatchCandidate | None:
        return self.patch_candidates.get(patch_candidate_id)

    def load_patch_draft(self, draft_id: str) -> PatchDraft | None:
        return self.patch_drafts.get(draft_id)

    def load_diff_preview(self, preview_id: str) -> DiffPreviewArtifact | None:
        return self.diff_previews.get(preview_id)

    def load_dry_run_report(self, report_id: str) -> PatchDryRunReport | None:
        return self.dry_run_reports.get(report_id)

    def load_static_safety_report(self, report_id: str) -> PatchStaticSafetyReport | None:
        return self.static_safety_reports.get(report_id)

    def load_rollback_plan(self, rollback_plan_id: str) -> RollbackPlanDescriptor | None:
        return self.rollback_plans.get(rollback_plan_id)

    def read_target_text(self, relative_path: str) -> tuple[str | None, str | None]:
        try:
            target = resolve_workspace_path(self.workspace_root, relative_path)
        except Exception:
            return None, None
        if not target.exists() or not target.is_file():
            return None, None
        data = target.read_bytes()
        if b"\x00" in data:
            return None, None
        text = data.decode("utf-8")
        return text, _hash_text(text)


class ApplyAuthorizationValidationService:
    def validate(
        self,
        request: BoundedPatchApplyRequest,
        apply_gate: ApplyGateState | None,
        authorization: ApplyGateAuthorization | None,
        rollback_plan: RollbackPlanDescriptor | None,
    ) -> ApplyAuthorizationValidationResult:
        failed: list[str] = []
        exists = authorization is not None
        gate_open = bool(apply_gate and apply_gate.gate_status == "open" and apply_gate.apply_gate_opened)
        stage_ok = bool(authorization and authorization.authorized_for_stage == "bounded_patch_apply")
        next_version = authorization.authorized_next_version if authorization else ""
        single_use = bool(authorization and authorization.single_use)
        consumed = bool(authorization and authorization.consumed)
        expired = bool(authorization and authorization.expires_at and authorization.expires_at <= utc_now_iso())
        ids_match = bool(
            authorization
            and authorization.apply_gate_id == request.apply_gate_id
            and authorization.patch_candidate_id == request.patch_candidate_id
            and authorization.draft_id == request.draft_id
            and authorization.preview_id == request.preview_id
            and authorization.dry_run_report_id == request.dry_run_report_id
        )
        rollback_matches = bool(
            authorization
            and rollback_plan
            and authorization.rollback_plan_id == request.rollback_plan_id
            and rollback_plan.rollback_plan_id == request.rollback_plan_id
            and rollback_plan.rollback_possible
        )
        confirmed = bool(request.operator_confirmation and request.confirmation_phrase == CONFIRMATION_PHRASE)
        if apply_gate is None:
            failed.append("missing_apply_gate")
        elif not gate_open:
            failed.append("apply_gate_not_open")
        if not exists:
            failed.append("missing_authorization")
        if exists and next_version != SELF_MODIFICATION_BOUNDED_APPLY_VERSION:
            failed.append("authorization_next_version_mismatch")
        if exists and not stage_ok:
            failed.append("authorization_stage_mismatch")
        if exists and not single_use:
            failed.append("authorization_not_single_use")
        if consumed:
            failed.append("authorization_consumed")
        if expired:
            failed.append("authorization_expired")
        if exists and not ids_match:
            failed.append("authorization_id_mismatch")
        if not rollback_matches:
            failed.append("rollback_plan_missing_or_mismatch")
        if not confirmed:
            failed.append("operator_confirmation_missing")
        return ApplyAuthorizationValidationResult(
            validation_id=f"apply_authorization_validation:{uuid4()}",
            apply_gate_id=request.apply_gate_id,
            authorization_id=request.authorization_id,
            authorization_exists=exists,
            gate_status_open=gate_open,
            authorized_for_bounded_apply=stage_ok and next_version == SELF_MODIFICATION_BOUNDED_APPLY_VERSION,
            authorized_next_version=next_version,
            single_use=single_use,
            consumed=consumed,
            expired=expired,
            patch_ids_match=ids_match,
            rollback_plan_matches=rollback_matches,
            operator_confirmed=confirmed,
            validation_status="passed" if not failed else "blocked",
            failed_reasons=failed,
            evidence_refs=[{"ref_type": "bounded_apply_version", "version": SELF_MODIFICATION_BOUNDED_APPLY_VERSION}],
        )


class PreApplyRevalidationService:
    def __init__(self, *, source_service: BoundedPatchApplySourceService | None = None) -> None:
        self.source_service = source_service or BoundedPatchApplySourceService()

    def revalidate(
        self,
        request: BoundedPatchApplyRequest,
        draft: PatchDraft | None,
        dry_run_report: PatchDryRunReport | None,
    ) -> PreApplyRevalidationReport:
        if draft is None:
            return _empty_revalidation(request, "missing_patch_draft")
        operations = draft.operations[: request.max_operations]
        target_results: list[PreApplyTargetRevalidationResult] = []
        operation_results: list[PreApplyOperationRevalidationResult] = []
        dry_hashes = {
            item.target_id: item.content_hash_before
            for item in (dry_run_report.target_snapshots if dry_run_report else [])
            if item.content_hash_before
        }
        target_ids = {str(op.target_ref.get("target_id") or "") for op in operations}
        for context in draft.target_context_refs:
            if context.target_id not in target_ids:
                continue
            relative_path = context.relative_path or ""
            text, current_hash = self.source_service.read_target_text(relative_path)
            expected_hash = request.expected_target_hashes.get(context.target_id) or request.expected_target_hashes.get(relative_path) or dry_hashes.get(context.target_id)
            exists = text is not None
            target_status = _target_revalidation_status(
                exists=exists,
                hash_matches=bool(expected_hash and current_hash == expected_hash),
                private_boundary_risk=context.private_boundary_risk,
                secret_risk=_is_secret_path(relative_path),
            )
            target_results.append(
                PreApplyTargetRevalidationResult(
                    result_id=f"pre_apply_target_revalidation:{uuid4()}",
                    target_id=context.target_id,
                    relative_path=relative_path,
                    expected_hash=expected_hash,
                    current_hash=current_hash,
                    hash_matches=bool(expected_hash and current_hash == expected_hash),
                    target_exists=exists,
                    target_is_file=exists,
                    private_boundary_risk=context.private_boundary_risk,
                    secret_risk=_is_secret_path(relative_path),
                    generated_file_risk=_is_generated_path(relative_path),
                    revalidation_status=target_status,
                    evidence_refs=[{"ref_type": "patch_target_context_ref", "context_id": context.context_id}],
                )
            )
        content_by_target = {
            item.target_id: self.source_service.read_target_text(item.relative_path)[0] or ""
            for item in target_results
            if item.target_exists
        }
        dry_operation_ids = {
            item.operation_id
            for item in (dry_run_report.operation_results if dry_run_report else [])
            if item.result_status in {"passed", "warning"} and item.would_apply_in_memory
        }
        for operation in operations:
            target_id = str(operation.target_ref.get("target_id") or "")
            content = content_by_target.get(target_id, "")
            old_matches = _old_text_matches(operation, content)
            anchor_matches = _anchor_matches(operation, content)
            in_scope = operation.operation_id in dry_operation_ids if dry_operation_ids else operation.operation_status == "drafted"
            would_apply = _simulate_content_update(operation, content) is not None
            status = "passed" if old_matches and anchor_matches and in_scope and would_apply else "blocked"
            operation_results.append(
                PreApplyOperationRevalidationResult(
                    result_id=f"pre_apply_operation_revalidation:{uuid4()}",
                    operation_id=operation.operation_id,
                    target_id=target_id,
                    anchor_still_matches=anchor_matches,
                    old_text_still_matches=old_matches,
                    operation_within_scope=in_scope,
                    would_apply_in_memory=would_apply,
                    revalidation_status=status,
                    evidence_refs=[{"ref_type": "patch_operation_draft", "operation_id": operation.operation_id}],
                )
            )
        status = _aggregate_status([item.revalidation_status for item in target_results + operation_results])
        drift = any(item.expected_hash and not item.hash_matches for item in target_results)
        private_clear = all(not item.private_boundary_risk for item in target_results)
        secret_clear = all(not item.secret_risk for item in target_results)
        return PreApplyRevalidationReport(
            report_id=f"pre_apply_revalidation_report:{uuid4()}",
            created_at=utc_now_iso(),
            patch_candidate_id=request.patch_candidate_id,
            draft_id=request.draft_id,
            preview_id=request.preview_id,
            target_revalidation_results=target_results,
            operation_revalidation_results=operation_results,
            revalidation_status=status,
            target_drift_detected=drift,
            private_boundary_clear=private_clear,
            secret_boundary_clear=secret_clear,
            safe_to_mutate_under_gate=status == "passed" and not drift and private_clear and secret_clear,
            evidence_refs=[{"ref_type": "bounded_apply_version", "version": SELF_MODIFICATION_BOUNDED_APPLY_VERSION}],
        )


class BoundedWorkspaceWriter:
    def __init__(self, *, workspace_root: str | Path | None = None) -> None:
        self.workspace_root = Path(workspace_root or ".").resolve(strict=False)

    def write_text_atomically(self, relative_path: str, new_content: str, expected_before_hash: str) -> WorkspaceFileChangeRecord:
        target = resolve_workspace_path(self.workspace_root, relative_path)
        if not target.exists() or not target.is_file():
            raise FileNotFoundError("Bounded apply target is missing or is not a file.")
        before_bytes = target.read_bytes()
        if b"\x00" in before_bytes:
            raise ValueError("Bounded apply target is binary.")
        before_text = before_bytes.decode("utf-8")
        before_hash = _hash_text(before_text)
        if before_hash != expected_before_hash:
            raise ValueError("Expected before hash does not match current target hash.")
        temporary = target.with_name(f".{target.name}.bounded-apply-{uuid4().hex}.tmp")
        with temporary.open("w", encoding="utf-8", newline="") as handle:
            handle.write(new_content)
        temporary.replace(target)
        after_text = target.read_text(encoding="utf-8")
        return WorkspaceFileChangeRecord(
            change_id=f"workspace_file_change_record:{uuid4()}",
            target_id="unknown",
            relative_path=relative_path,
            change_type="text_patch",
            before_hash=before_hash,
            after_hash=_hash_text(after_text),
            before_line_count=_line_count(before_text),
            after_line_count=_line_count(after_text),
            applied_operation_ids=[],
            rollback_plan_id="",
            workspace_file_changed_event_id=None,
            raw_content_emitted=False,
            evidence_refs=[{"ref_type": "bounded_workspace_writer", "version": SELF_MODIFICATION_BOUNDED_APPLY_VERSION}],
        )


class BoundedPatchApplyEngine:
    def __init__(
        self,
        *,
        source_service: BoundedPatchApplySourceService | None = None,
        writer: BoundedWorkspaceWriter | None = None,
    ) -> None:
        self.source_service = source_service or BoundedPatchApplySourceService()
        self.writer = writer or BoundedWorkspaceWriter(workspace_root=self.source_service.workspace_root)

    def apply(
        self,
        request: BoundedPatchApplyRequest,
        draft: PatchDraft | None,
        revalidation: PreApplyRevalidationReport,
        rollback_plan: RollbackPlanDescriptor,
    ) -> tuple[list[BoundedPatchApplyOperation], list[WorkspaceFileChangeRecord], str]:
        if draft is None or not revalidation.safe_to_mutate_under_gate:
            return [], [], "blocked"
        if len({item.relative_path for item in revalidation.target_revalidation_results}) > request.max_files:
            return [], [], "blocked"
        operations: list[BoundedPatchApplyOperation] = []
        changes: list[WorkspaceFileChangeRecord] = []
        by_target = {item.target_id: item for item in revalidation.target_revalidation_results}
        content_by_target = {
            item.target_id: self.source_service.read_target_text(item.relative_path)[0] or ""
            for item in revalidation.target_revalidation_results
        }
        applied_by_path: dict[str, list[str]] = {}
        new_content_by_path: dict[str, str] = {}
        for operation in draft.operations[: request.max_operations]:
            target_id = str(operation.target_ref.get("target_id") or "")
            target = by_target.get(target_id)
            if target is None or target.revalidation_status not in {"passed", "warning"}:
                operations.append(_operation_record(operation, target_id, "", False, "blocked"))
                continue
            current = new_content_by_path.get(target.relative_path, content_by_target.get(target_id, ""))
            updated = _simulate_content_update(operation, current)
            if updated is None:
                operations.append(_operation_record(operation, target_id, target.relative_path, False, "failed"))
                continue
            new_content_by_path[target.relative_path] = updated
            applied_by_path.setdefault(target.relative_path, []).append(operation.operation_id)
            operations.append(_operation_record(operation, target_id, target.relative_path, True, "applied"))
        if any(item.operation_status in {"failed", "blocked"} for item in operations):
            return operations, [], "failed"
        for target in revalidation.target_revalidation_results:
            if target.relative_path not in new_content_by_path:
                continue
            change = self.writer.write_text_atomically(
                target.relative_path,
                new_content_by_path[target.relative_path],
                target.current_hash or "",
            )
            changes.append(
                replace(
                    change,
                    target_id=target.target_id,
                    rollback_plan_id=rollback_plan.rollback_plan_id,
                    applied_operation_ids=applied_by_path.get(target.relative_path, []),
                )
            )
        return operations, changes, "applied" if changes else "failed"


class WorkspaceFileChangedEventService:
    def emit_file_changed(
        self,
        change_record: WorkspaceFileChangeRecord,
        transaction_id: str,
    ) -> WorkspaceFileChangeRecord:
        return replace(
            change_record,
            workspace_file_changed_event_id=f"workspace_file_changed:{uuid4()}",
            evidence_refs=[
                *change_record.evidence_refs,
                {"ref_type": "bounded_patch_apply_transaction", "transaction_id": transaction_id},
            ],
        )


class ApplyAuthorizationConsumeService:
    def consume(self, authorization: ApplyGateAuthorization, transaction_id: str) -> ApplyGateAuthorization:
        return replace(
            authorization,
            consumed=True,
            patch_applied=True,
            file_write_performed=True,
            workspace_file_changed_emitted=True,
            evidence_refs=[
                *authorization.evidence_refs,
                {"ref_type": "bounded_patch_apply_transaction", "transaction_id": transaction_id},
            ],
        )


class BoundedPatchApplyFindingService:
    def build_findings(
        self,
        validation: ApplyAuthorizationValidationResult,
        revalidation: PreApplyRevalidationReport,
        transaction: BoundedPatchApplyTransaction | None,
    ) -> list[BoundedPatchApplyFinding]:
        findings = [
            _finding("critical", reason, f"Apply blocked by {reason}.", None, None)
            for reason in validation.failed_reasons
        ]
        if revalidation.target_drift_detected:
            findings.append(_finding("critical", "target_hash_drift", "Target hash drift blocks bounded apply.", None, None))
        for target in revalidation.target_revalidation_results:
            target_ref = target.to_dict()
            if target.private_boundary_risk:
                findings.append(_finding("critical", "private_boundary_risk", "Private boundary blocks bounded apply.", target_ref, None))
            if target.secret_risk:
                findings.append(_finding("critical", "secret_boundary_risk", "Secret boundary blocks bounded apply.", target_ref, None))
            if not target.target_exists:
                findings.append(_finding("critical", "target_missing", "Target is missing.", target_ref, None))
            if target.generated_file_risk:
                findings.append(_finding("warning", "generated_file_risk", "Generated file risk is visible.", target_ref, None))
        for operation in revalidation.operation_revalidation_results:
            if operation.revalidation_status not in {"passed", "warning"}:
                findings.append(
                    _finding(
                        "critical",
                        "operation_revalidation_failed",
                        "Operation failed pre-apply revalidation.",
                        None,
                        operation.to_dict(),
                    )
                )
        if transaction and transaction.file_changes:
            findings.append(_finding("info", "workspace_file_changed_emitted", "workspace_file_changed was emitted.", None, None))
        findings.append(
            _finding(
                "info",
                "post_apply_verification_required",
                "Post-apply verification remains required after bounded apply.",
                None,
                None,
            )
        )
        return findings or [_finding("info", "ok", "Bounded apply state is visible.", None, None)]


class BoundedPatchApplyReportService:
    def __init__(
        self,
        *,
        source_service: BoundedPatchApplySourceService | None = None,
        validation_service: ApplyAuthorizationValidationService | None = None,
        revalidation_service: PreApplyRevalidationService | None = None,
        engine: BoundedPatchApplyEngine | None = None,
        event_service: WorkspaceFileChangedEventService | None = None,
        consume_service: ApplyAuthorizationConsumeService | None = None,
        finding_service: BoundedPatchApplyFindingService | None = None,
    ) -> None:
        self.source_service = source_service or BoundedPatchApplySourceService()
        self.validation_service = validation_service or ApplyAuthorizationValidationService()
        self.revalidation_service = revalidation_service or PreApplyRevalidationService(source_service=self.source_service)
        self.engine = engine or BoundedPatchApplyEngine(source_service=self.source_service)
        self.event_service = event_service or WorkspaceFileChangedEventService()
        self.consume_service = consume_service or ApplyAuthorizationConsumeService()
        self.finding_service = finding_service or BoundedPatchApplyFindingService()

    def build_report(self, request: BoundedPatchApplyRequest) -> BoundedPatchApplyReport:
        normalized = request.normalized()
        apply_gate = self.source_service.load_apply_gate(normalized.apply_gate_id)
        authorization = self.source_service.load_authorization(normalized.authorization_id)
        self.source_service.load_patch_candidate(normalized.patch_candidate_id)
        draft = self.source_service.load_patch_draft(normalized.draft_id)
        dry_run = self.source_service.load_dry_run_report(normalized.dry_run_report_id)
        self.source_service.load_static_safety_report(normalized.static_safety_report_id)
        rollback_plan = self.source_service.load_rollback_plan(normalized.rollback_plan_id)
        validation = self.validation_service.validate(normalized, apply_gate, authorization, rollback_plan)
        revalidation = self.revalidation_service.revalidate(normalized, draft, dry_run)
        transaction: BoundedPatchApplyTransaction | None = None
        if validation.validation_status == "passed" and revalidation.safe_to_mutate_under_gate and authorization and rollback_plan:
            operations, changes, status = self.engine.apply(normalized, draft, revalidation, rollback_plan)
            transaction_id = f"bounded_patch_apply_transaction:{uuid4()}"
            emitted_changes = [self.event_service.emit_file_changed(change, transaction_id) for change in changes]
            consumed = bool(emitted_changes)
            if consumed:
                self.source_service.authorizations[authorization.authorization_id] = self.consume_service.consume(authorization, transaction_id)
            transaction = BoundedPatchApplyTransaction(
                transaction_id=transaction_id,
                created_at=utc_now_iso(),
                apply_gate_id=normalized.apply_gate_id,
                authorization_id=normalized.authorization_id,
                patch_candidate_id=normalized.patch_candidate_id,
                draft_id=normalized.draft_id,
                preview_id=normalized.preview_id,
                rollback_plan_id=normalized.rollback_plan_id,
                validation_result=validation,
                pre_apply_revalidation_report=revalidation,
                operations=operations,
                file_changes=emitted_changes,
                transaction_status=status,
                authorization_consumed=consumed,
                rollback_plan_available=True,
                post_apply_verification_required=True,
                post_apply_verified=False,
                shell_executed=False,
                test_lint_executed=False,
                raw_content_emitted=False,
                evidence_refs=[{"ref_type": "bounded_apply_version", "version": SELF_MODIFICATION_BOUNDED_APPLY_VERSION}],
            )
        findings = self.finding_service.build_findings(validation, revalidation, transaction)
        status = transaction.transaction_status if transaction else "blocked"
        changed = len(transaction.file_changes) if transaction else 0
        applied_ops = sum(1 for item in transaction.operations if item.applied) if transaction else 0
        failed_ops = sum(1 for item in transaction.operations if item.operation_status in {"failed", "blocked"}) if transaction else 0
        return BoundedPatchApplyReport(
            report_id=f"bounded_patch_apply_report:{uuid4()}",
            created_at=utc_now_iso(),
            request=normalized,
            transaction=transaction,
            findings=findings,
            apply_status=status,
            changed_file_count=changed,
            applied_operation_count=applied_ops,
            failed_operation_count=failed_ops,
            workspace_file_changed_emitted=bool(transaction and transaction.file_changes),
            authorization_consumed=bool(transaction and transaction.authorization_consumed),
            rollback_plan_available=bool(rollback_plan and rollback_plan.rollback_possible),
            post_apply_verification_required=True,
            post_apply_verified=False,
            outcome_recorded=False,
            shell_executed=False,
            test_lint_executed=False,
            raw_content_emitted=False,
            limitations=[
                "Bounded apply is controlled mutation, not autonomous self-editing.",
                "Only approved workspace-relative text targets are eligible.",
                "Post-apply verification is deferred to v0.22.7.",
            ],
            withdrawal_conditions=[
                "Withdraw if shell, test/lint, rollback, or post-apply verification executes.",
                "Withdraw if file writes occur outside BoundedWorkspaceWriter.",
                "Withdraw if workspace_file_changed is emitted before a successful bounded write.",
            ],
        )


class SelfModificationBoundedApplyService:
    def __init__(self, *, report_service: BoundedPatchApplyReportService | None = None) -> None:
        self.report_service = report_service or BoundedPatchApplyReportService()

    def apply_bounded_patch(self, request: BoundedPatchApplyRequest) -> BoundedPatchApplyResult:
        return BoundedPatchApplyResult(report=self.report_service.build_report(request))

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": SELF_MODIFICATION_BOUNDED_APPLY_VERSION,
            "layer": "self_modification_safety",
            "subject": "bounded_patch_apply",
            "principles": [
                "bounded apply is controlled mutation",
                "apply authorization is single-use",
                "pre-apply revalidation is mandatory",
                "workspace_file_changed must be OCEL-visible",
                "post-apply verification is still required",
            ],
            "bounded_file_write_enabled": True,
            "file_write_enabled": False,
            "apply_patch_enabled": False,
            "safe_to_apply": False,
            "external_patch_tool_allowed": False,
            "shell_executed": False,
            "test_lint_executed": False,
            "post_apply_verified": False,
            "llm_judge_enabled": False,
            "no_file_mutation_occurred": True,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "version": SELF_MODIFICATION_BOUNDED_APPLY_VERSION,
            "layer": "self_modification_safety",
            "state": SELF_MODIFICATION_BOUNDED_APPLY_STATE,
            "source_read_models": [
                "ApplyGateState",
                "RollbackPlanState",
                "PatchDryRunState",
                "PatchStaticSafetyState",
                "PatchDraftState",
                "PatchCandidateState",
            ],
            "target_read_models": [
                "BoundedPatchApplyState",
                "WorkspaceFileChangeState",
                "PostApplyVerificationRequiredState",
                "RollbackEligibilityState",
            ],
            "effect_types": ["read_only_observation", "state_candidate_created", "workspace_file_changed"],
            "safe_to_apply": False,
            "file_write_enabled": False,
            "apply_patch_enabled": False,
            "no_file_mutation_occurred": True,
        }

    def render_result_cli(self, result: BoundedPatchApplyResult) -> str:
        report = result.report
        transaction = report.transaction
        first_change = transaction.file_changes[0] if transaction and transaction.file_changes else None
        return "\n".join(
            [
                "Self-Modification Bounded Patch Apply",
                f"version={SELF_MODIFICATION_BOUNDED_APPLY_VERSION}",
                "layer=self_modification_safety",
                f"report_id={report.report_id}",
                f"apply_status={report.apply_status}",
                f"transaction_id={transaction.transaction_id if transaction else ''}",
                f"changed_file_count={report.changed_file_count}",
                f"applied_operation_count={report.applied_operation_count}",
                f"failed_operation_count={report.failed_operation_count}",
                f"before_hash={first_change.before_hash if first_change else ''}",
                f"after_hash={first_change.after_hash if first_change else ''}",
                f"workspace_file_changed_event_id={first_change.workspace_file_changed_event_id if first_change else ''}",
                f"authorization_consumed={str(report.authorization_consumed).lower()}",
                f"rollback_plan_available={str(report.rollback_plan_available).lower()}",
                f"post_apply_verification_required={str(report.post_apply_verification_required).lower()}",
                f"post_apply_verified={str(report.post_apply_verified).lower()}",
                "next_required_step=v0.22.7 Post-Apply Verification & Outcome",
                "raw_full_file_content_printed=False",
                "private_full_paths_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_pig_report_cli(self) -> str:
        report = self.build_pig_report()
        return "\n".join(
            [
                "Self-Modification Bounded Patch Apply PIG Report",
                f"version={report['version']}",
                f"layer={report['layer']}",
                f"subject={report['subject']}",
                f"principles={','.join(report['principles'])}",
                f"bounded_file_write_enabled={str(report['bounded_file_write_enabled']).lower()}",
                f"file_write_enabled={str(report['file_write_enabled']).lower()}",
                f"apply_patch_enabled={str(report['apply_patch_enabled']).lower()}",
                f"safe_to_apply={str(report['safe_to_apply']).lower()}",
                f"external_patch_tool_allowed={str(report['external_patch_tool_allowed']).lower()}",
                f"shell_executed={str(report['shell_executed']).lower()}",
                f"test_lint_executed={str(report['test_lint_executed']).lower()}",
                f"post_apply_verified={str(report['post_apply_verified']).lower()}",
                f"llm_judge_enabled={str(report['llm_judge_enabled']).lower()}",
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
                "Self-Modification Bounded Patch Apply OCPX Projection",
                f"version={projection['version']}",
                f"layer={projection['layer']}",
                f"state={projection['state']}",
                f"source_read_models={','.join(projection['source_read_models'])}",
                f"target_read_models={','.join(projection['target_read_models'])}",
                f"effect_types={','.join(projection['effect_types'])}",
                f"safe_to_apply={str(projection['safe_to_apply']).lower()}",
                f"file_write_enabled={str(projection['file_write_enabled']).lower()}",
                f"apply_patch_enabled={str(projection['apply_patch_enabled']).lower()}",
                f"no_file_mutation_occurred={str(projection['no_file_mutation_occurred']).lower()}",
                "No file mutation occurred.",
                "raw_file_content_printed=False",
                "raw_full_file_content_printed=False",
                "private_full_paths_printed=False",
                "raw_secrets_printed=False",
            ]
        )


def _empty_revalidation(request: BoundedPatchApplyRequest, reason: str) -> PreApplyRevalidationReport:
    return PreApplyRevalidationReport(
        report_id=f"pre_apply_revalidation_report:{uuid4()}",
        created_at=utc_now_iso(),
        patch_candidate_id=request.patch_candidate_id,
        draft_id=request.draft_id,
        preview_id=request.preview_id,
        target_revalidation_results=[],
        operation_revalidation_results=[],
        revalidation_status="blocked",
        target_drift_detected=False,
        private_boundary_clear=False,
        secret_boundary_clear=False,
        safe_to_mutate_under_gate=False,
        evidence_refs=[{"ref_type": "pre_apply_revalidation_block", "reason": reason}],
    )


def _target_revalidation_status(
    *,
    exists: bool,
    hash_matches: bool,
    private_boundary_risk: bool,
    secret_risk: bool,
) -> str:
    if not exists or private_boundary_risk or secret_risk:
        return "blocked"
    if not hash_matches:
        return "blocked"
    return "passed"


def _aggregate_status(statuses: list[str]) -> str:
    if not statuses:
        return "blocked"
    if "blocked" in statuses:
        return "blocked"
    if "failed" in statuses:
        return "failed"
    if "warning" in statuses:
        return "warning"
    return "passed"


def _operation_record(
    operation: PatchOperationDraft,
    target_id: str,
    relative_path: str,
    applied: bool,
    status: str,
) -> BoundedPatchApplyOperation:
    return BoundedPatchApplyOperation(
        operation_id=operation.operation_id,
        operation_type=operation.operation_type,
        target_id=target_id,
        relative_path=relative_path,
        approved_operation_ref={"ref_type": "patch_operation_draft", "operation_id": operation.operation_id},
        applied=applied,
        applied_line_start=operation.anchor_ref.line_start if operation.anchor_ref else None,
        applied_line_end=operation.anchor_ref.line_end if operation.anchor_ref else None,
        added_line_count=operation.added_line_count,
        removed_line_count=operation.removed_line_count,
        operation_status=status,
        evidence_refs=[{"ref_type": "bounded_apply_version", "version": SELF_MODIFICATION_BOUNDED_APPLY_VERSION}],
    )


def _simulate_content_update(operation: PatchOperationDraft, content: str) -> str | None:
    old = operation.old_text_preview or ""
    new = operation.new_text_preview or ""
    if operation.operation_type == "text_replace":
        if not old or old not in content:
            return None
        return content.replace(old, new, 1)
    if operation.operation_type == "insert_after":
        anchor_text = operation.anchor_ref.anchor_text_preview if operation.anchor_ref else None
        if not anchor_text or anchor_text not in content:
            return None
        return content.replace(anchor_text, anchor_text + "\n" + new, 1)
    if operation.operation_type in {"append_block", "comment_only_change"}:
        suffix = "\n" if content and not content.endswith("\n") else ""
        return content + suffix + new
    return None


def _old_text_matches(operation: PatchOperationDraft, content: str) -> bool:
    if operation.operation_type == "text_replace":
        return bool(operation.old_text_preview and operation.old_text_preview in content)
    return True


def _anchor_matches(operation: PatchOperationDraft, content: str) -> bool:
    anchor = operation.anchor_ref
    if anchor is None or anchor.anchor_type in {"eof", "unknown"}:
        return True
    if anchor.ambiguous:
        return False
    if anchor.anchor_text_preview:
        return content.count(anchor.anchor_text_preview) == 1
    return True


def _finding(
    severity: str,
    finding_type: str,
    message: str,
    target_ref: dict[str, Any] | None,
    operation_ref: dict[str, Any] | None,
) -> BoundedPatchApplyFinding:
    return BoundedPatchApplyFinding(
        finding_id=f"bounded_patch_apply_finding:{uuid4()}",
        severity=severity,
        finding_type=finding_type,
        message=message,
        target_ref=target_ref,
        operation_ref=operation_ref,
        evidence_refs=[{"ref_type": "bounded_apply_version", "version": SELF_MODIFICATION_BOUNDED_APPLY_VERSION}],
        withdrawal_condition="Withdraw if bounded apply bypasses authorization or writes outside BoundedWorkspaceWriter.",
    )


def _hash_text(text: str) -> str:
    import hashlib

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _line_count(text: str | None) -> int:
    if not text:
        return 0
    return len(text.splitlines())


def _is_secret_path(relative_path: str | None) -> bool:
    if not relative_path:
        return False
    lowered = relative_path.lower()
    return any(token in lowered for token in [".env", "secret", "credential", "private_key", "token"])


def _is_generated_path(relative_path: str | None) -> bool:
    if not relative_path:
        return False
    lowered = relative_path.lower()
    return any(token in lowered for token in ["generated", "__pycache__", ".min."])
