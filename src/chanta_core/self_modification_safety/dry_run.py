from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.self_modification_safety.candidate import PatchCandidate
from chanta_core.self_modification_safety.draft import (
    DiffPreviewArtifact,
    PatchAnchorRef,
    PatchDraft,
    PatchDraftCreateRequest,
    PatchDraftSourceService,
    PatchOperationDraft,
    SelfModificationDiffPreviewService,
)
from chanta_core.self_modification_safety.static_safety import (
    PatchStaticSafetyCheckRequest,
    PatchStaticSafetyReport,
    PatchStaticSafetyReportService,
    PatchStaticSafetySourceService,
    SelfModificationStaticSafetyService,
)
from chanta_core.utility.time import utc_now_iso


SELF_MODIFICATION_DRY_RUN_VERSION = "v0.22.4"
SELF_MODIFICATION_DRY_RUN_STATE = "self_modification_patch_dry_run_applicability_checked"
DRY_RUN_SKILL_ID = "skill:self_modification_dry_run"
APPLICABILITY_CHECK_SKILL_ID = "skill:self_modification_applicability_check"


@dataclass(frozen=True)
class PatchDryRunCheckRequest:
    patch_candidate_id: str | None = None
    draft_id: str | None = None
    preview_id: str | None = None
    static_safety_report_id: str | None = None
    include_target_snapshot: bool = True
    include_anchor_check: bool = True
    include_operation_simulation: bool = True
    include_conflict_detection: bool = True
    include_result_hash: bool = True
    max_target_bytes: int = 512000
    max_operations: int = 10
    max_findings: int = 300
    strictness: str = "standard"

    def normalized(self) -> "PatchDryRunCheckRequest":
        return PatchDryRunCheckRequest(
            patch_candidate_id=str(self.patch_candidate_id).strip() if self.patch_candidate_id else None,
            draft_id=str(self.draft_id).strip() if self.draft_id else None,
            preview_id=str(self.preview_id).strip() if self.preview_id else None,
            static_safety_report_id=str(self.static_safety_report_id).strip() if self.static_safety_report_id else None,
            include_target_snapshot=bool(self.include_target_snapshot),
            include_anchor_check=bool(self.include_anchor_check),
            include_operation_simulation=bool(self.include_operation_simulation),
            include_conflict_detection=bool(self.include_conflict_detection),
            include_result_hash=bool(self.include_result_hash),
            max_target_bytes=max(1, int(self.max_target_bytes)),
            max_operations=max(1, int(self.max_operations)),
            max_findings=max(1, int(self.max_findings)),
            strictness=self.strictness or "standard",
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "patch_candidate_id": self.patch_candidate_id,
            "draft_id": self.draft_id,
            "preview_id": self.preview_id,
            "static_safety_report_id": self.static_safety_report_id,
            "include_target_snapshot": self.include_target_snapshot,
            "include_anchor_check": self.include_anchor_check,
            "include_operation_simulation": self.include_operation_simulation,
            "include_conflict_detection": self.include_conflict_detection,
            "include_result_hash": self.include_result_hash,
            "max_target_bytes": self.max_target_bytes,
            "max_operations": self.max_operations,
            "max_findings": self.max_findings,
            "strictness": self.strictness,
        }


@dataclass(frozen=True)
class PatchDryRunEnginePolicy:
    policy_id: str = "patch_dry_run_engine_policy:v0.22.4"
    in_memory_only: bool = True
    external_patch_tool_allowed: bool = False
    shell_execution_allowed: bool = False
    file_write_allowed: bool = False
    apply_patch_allowed: bool = False
    workspace_file_changed_allowed: bool = False
    test_lint_execution_allowed: bool = False
    allow_full_content_output: bool = False
    max_target_bytes: int = 512000
    preserve_line_endings: bool = True
    preserve_encoding: bool = True
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "in_memory_only": self.in_memory_only,
            "external_patch_tool_allowed": self.external_patch_tool_allowed,
            "shell_execution_allowed": self.shell_execution_allowed,
            "file_write_allowed": self.file_write_allowed,
            "apply_patch_allowed": self.apply_patch_allowed,
            "workspace_file_changed_allowed": self.workspace_file_changed_allowed,
            "test_lint_execution_allowed": self.test_lint_execution_allowed,
            "allow_full_content_output": self.allow_full_content_output,
            "max_target_bytes": self.max_target_bytes,
            "preserve_line_endings": self.preserve_line_endings,
            "preserve_encoding": self.preserve_encoding,
            "notes": list(self.notes),
        }


@dataclass(frozen=True)
class PatchDryRunTargetSnapshot:
    snapshot_id: str
    target_id: str
    relative_path: str | None
    content_available: bool
    snapshot_source: str
    content_hash_before: str | None
    byte_count: int | None
    line_count: int | None
    encoding: str | None
    line_ending: str | None
    truncated: bool
    redacted: bool
    private_boundary_risk: bool
    secret_risk: bool
    generated_file_risk: bool
    raw_content_emitted: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    _content_for_simulation: str | None = field(default=None, repr=False, compare=False)

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "target_id": self.target_id,
            "relative_path": self.relative_path,
            "content_available": self.content_available,
            "snapshot_source": self.snapshot_source,
            "content_hash_before": self.content_hash_before,
            "byte_count": self.byte_count,
            "line_count": self.line_count,
            "encoding": self.encoding,
            "line_ending": self.line_ending,
            "truncated": self.truncated,
            "redacted": self.redacted,
            "private_boundary_risk": self.private_boundary_risk,
            "secret_risk": self.secret_risk,
            "generated_file_risk": self.generated_file_risk,
            "raw_content_emitted": self.raw_content_emitted,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class PatchAnchorApplicabilityCheck:
    check_id: str
    operation_id: str
    target_id: str
    anchor_id: str | None
    anchor_type: str | None
    match_count: int
    matched_line_start: int | None
    matched_line_end: int | None
    ambiguous: bool
    found: bool
    anchor_status: str
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "operation_id": self.operation_id,
            "target_id": self.target_id,
            "anchor_id": self.anchor_id,
            "anchor_type": self.anchor_type,
            "match_count": self.match_count,
            "matched_line_start": self.matched_line_start,
            "matched_line_end": self.matched_line_end,
            "ambiguous": self.ambiguous,
            "found": self.found,
            "anchor_status": self.anchor_status,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class PatchDryRunConflict:
    conflict_id: str
    operation_id: str
    target_id: str
    conflict_type: str
    severity: str
    message: str
    expected_ref: dict[str, Any] | None
    actual_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "conflict_id": self.conflict_id,
            "operation_id": self.operation_id,
            "target_id": self.target_id,
            "conflict_type": self.conflict_type,
            "severity": self.severity,
            "message": self.message,
            "expected_ref": dict(self.expected_ref) if self.expected_ref else None,
            "actual_ref": dict(self.actual_ref) if self.actual_ref else None,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class PatchDryRunOperationResult:
    result_id: str
    operation_id: str
    target_id: str
    operation_type: str
    anchor_check: PatchAnchorApplicabilityCheck | None
    would_apply_in_memory: bool
    applied_in_memory: bool
    conflict_count: int
    conflicts: list[PatchDryRunConflict]
    resulting_content_hash: str | None
    resulting_line_count: int | None
    result_status: str
    file_write_performed: bool = False
    workspace_file_changed_emitted: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "operation_id": self.operation_id,
            "target_id": self.target_id,
            "operation_type": self.operation_type,
            "anchor_check": self.anchor_check.to_dict() if self.anchor_check else None,
            "would_apply_in_memory": self.would_apply_in_memory,
            "applied_in_memory": self.applied_in_memory,
            "conflict_count": self.conflict_count,
            "conflicts": [item.to_dict() for item in self.conflicts],
            "resulting_content_hash": self.resulting_content_hash,
            "resulting_line_count": self.resulting_line_count,
            "result_status": self.result_status,
            "file_write_performed": self.file_write_performed,
            "workspace_file_changed_emitted": self.workspace_file_changed_emitted,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class PatchApplicabilityFinding:
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
class PatchDryRunReport:
    report_id: str
    created_at: str
    request: PatchDryRunCheckRequest
    patch_candidate_id: str | None
    draft_id: str | None
    preview_id: str | None
    static_safety_report_id: str | None
    engine_policy: PatchDryRunEnginePolicy
    target_snapshots: list[PatchDryRunTargetSnapshot]
    operation_results: list[PatchDryRunOperationResult]
    findings: list[PatchApplicabilityFinding]
    checked_operation_count: int
    passed_operation_count: int
    warning_operation_count: int
    failed_operation_count: int
    blocked_operation_count: int
    conflict_count: int
    dry_run_status: str
    eligible_for_review: bool
    safe_to_apply: bool = False
    human_review_required: bool = True
    apply_gate_required: bool = True
    rollback_plan_required: bool = True
    post_apply_verification_required: bool = True
    review_status: str = "report_only"
    file_write_enabled: bool = False
    apply_patch_enabled: bool = False
    file_write_performed: bool = False
    patch_applied: bool = False
    workspace_file_changed_emitted: bool = False
    shell_executed: bool = False
    test_lint_executed: bool = False
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until target file, patch draft, diff preview, or policy changes."

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "created_at": self.created_at,
            "request": self.request.to_dict(),
            "patch_candidate_id": self.patch_candidate_id,
            "draft_id": self.draft_id,
            "preview_id": self.preview_id,
            "static_safety_report_id": self.static_safety_report_id,
            "engine_policy": self.engine_policy.to_dict(),
            "target_snapshots": [item.to_dict() for item in self.target_snapshots],
            "operation_results": [item.to_dict() for item in self.operation_results],
            "findings": [item.to_dict() for item in self.findings],
            "checked_operation_count": self.checked_operation_count,
            "passed_operation_count": self.passed_operation_count,
            "warning_operation_count": self.warning_operation_count,
            "failed_operation_count": self.failed_operation_count,
            "blocked_operation_count": self.blocked_operation_count,
            "conflict_count": self.conflict_count,
            "dry_run_status": self.dry_run_status,
            "eligible_for_review": self.eligible_for_review,
            "safe_to_apply": self.safe_to_apply,
            "human_review_required": self.human_review_required,
            "apply_gate_required": self.apply_gate_required,
            "rollback_plan_required": self.rollback_plan_required,
            "post_apply_verification_required": self.post_apply_verification_required,
            "review_status": self.review_status,
            "file_write_enabled": self.file_write_enabled,
            "apply_patch_enabled": self.apply_patch_enabled,
            "file_write_performed": self.file_write_performed,
            "patch_applied": self.patch_applied,
            "workspace_file_changed_emitted": self.workspace_file_changed_emitted,
            "shell_executed": self.shell_executed,
            "test_lint_executed": self.test_lint_executed,
            "limitations": list(self.limitations),
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "validity_horizon": self.validity_horizon,
        }


@dataclass(frozen=True)
class PatchDryRunNeedsMoreInputCandidate:
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
class PatchDryRunNoActionCandidate:
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
class PatchDryRunResult:
    report: PatchDryRunReport
    no_action_candidate: PatchDryRunNoActionCandidate | None
    needs_more_input_candidate: PatchDryRunNeedsMoreInputCandidate | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "report": self.report.to_dict(),
            "no_action_candidate": self.no_action_candidate.to_dict() if self.no_action_candidate else None,
            "needs_more_input_candidate": self.needs_more_input_candidate.to_dict()
            if self.needs_more_input_candidate
            else None,
        }


class PatchDryRunSourceService:
    def __init__(
        self,
        *,
        patch_candidates: dict[str, PatchCandidate] | None = None,
        patch_drafts: dict[str, PatchDraft] | None = None,
        diff_previews: dict[str, DiffPreviewArtifact] | None = None,
        static_safety_reports: dict[str, PatchStaticSafetyReport] | None = None,
        allow_synthetic: bool = False,
    ) -> None:
        self.patch_candidates = dict(patch_candidates or {})
        self.patch_drafts = dict(patch_drafts or {})
        self.diff_previews = dict(diff_previews or {})
        self.static_safety_reports = dict(static_safety_reports or {})
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

    def load_target_snapshots(
        self,
        request: PatchDryRunCheckRequest,
        draft: PatchDraft | None,
    ) -> list[PatchDryRunTargetSnapshot]:
        if draft is None or not request.include_target_snapshot:
            return []
        snapshots: list[PatchDryRunTargetSnapshot] = []
        for context in draft.target_context_refs:
            content = _simulation_content_for_context(context.target_id, draft.operations)
            content_bytes = content.encode("utf-8")
            if len(content_bytes) > request.max_target_bytes:
                content = content_bytes[: request.max_target_bytes].decode("utf-8", errors="ignore")
                truncated = True
            else:
                truncated = context.truncated
            relative_path = context.relative_path
            snapshots.append(
                PatchDryRunTargetSnapshot(
                    snapshot_id=f"patch_dry_run_target_snapshot:{uuid4()}",
                    target_id=context.target_id,
                    relative_path=relative_path,
                    content_available=context.content_available or bool(content),
                    snapshot_source="provided_context" if context.content_available else "bounded_text_read",
                    content_hash_before=_hash_text(content) if content else None,
                    byte_count=len(content.encode("utf-8")) if content else None,
                    line_count=_line_count(content) if content else None,
                    encoding="utf-8" if content else None,
                    line_ending=_line_ending(content) if content else None,
                    truncated=truncated,
                    redacted=context.redacted,
                    private_boundary_risk=context.private_boundary_risk,
                    secret_risk=_is_secret_path(relative_path),
                    generated_file_risk=_is_generated_path(relative_path),
                    raw_content_emitted=False,
                    evidence_refs=[
                        {"ref_type": "patch_target_context_ref", "context_id": context.context_id},
                        {"ref_type": "patch_dry_run_version", "version": SELF_MODIFICATION_DRY_RUN_VERSION},
                    ],
                    _content_for_simulation=content,
                )
            )
        return snapshots

    def _ensure_synthetic_bundle(self) -> None:
        if self.patch_drafts and self.diff_previews and self.static_safety_reports:
            return
        diff_service = SelfModificationDiffPreviewService(source_service=PatchDraftSourceService(allow_synthetic=True))
        draft_result = diff_service.create_patch_draft_and_preview(
            PatchDraftCreateRequest(
                patch_candidate_id="patch_candidate:cli_dry_run",
                operation_hints=[
                    {
                        "relative_path": "README.md",
                        "operation_type": "comment_only_change",
                        "anchor_type": "eof",
                        "provided_context": "sanitized context only",
                        "new_text_preview": "# preview-only candidate change",
                    }
                ],
            )
        )
        if draft_result.patch_candidate:
            self.patch_candidates[draft_result.patch_candidate.candidate_id] = draft_result.patch_candidate
        if draft_result.draft:
            self.patch_drafts[draft_result.draft.draft_id] = draft_result.draft
        if draft_result.diff_preview:
            self.diff_previews[draft_result.diff_preview.preview_id] = draft_result.diff_preview
        if draft_result.patch_candidate and draft_result.draft and draft_result.diff_preview:
            static_service = SelfModificationStaticSafetyService(
                report_service=PatchStaticSafetyReportService(
                    source_service=PatchStaticSafetySourceService(
                        patch_candidates={draft_result.patch_candidate.candidate_id: draft_result.patch_candidate},
                        patch_drafts={draft_result.draft.draft_id: draft_result.draft},
                        diff_previews={draft_result.diff_preview.preview_id: draft_result.diff_preview},
                    )
                )
            )
            static_result = static_service.check_static_safety(
                PatchStaticSafetyCheckRequest(
                    patch_candidate_id=draft_result.patch_candidate.candidate_id,
                    draft_id=draft_result.draft.draft_id,
                    preview_id=draft_result.diff_preview.preview_id,
                )
            )
            self.static_safety_reports[static_result.report.report_id] = static_result.report


class PatchAnchorApplicabilityService:
    def check_anchor(
        self,
        operation: PatchOperationDraft,
        target_snapshot: PatchDryRunTargetSnapshot | None,
    ) -> PatchAnchorApplicabilityCheck:
        target_id = str(operation.target_ref.get("target_id") or target_snapshot.target_id if target_snapshot else "unknown")
        anchor = operation.anchor_ref
        if target_snapshot is None or not target_snapshot.content_available:
            return _anchor_check(operation, target_id, anchor, 0, None, None, "blocked")
        content = target_snapshot._content_for_simulation or ""
        if anchor is None:
            return _anchor_check(operation, target_id, None, 0, None, None, "not_applicable")
        if anchor.ambiguous:
            return _anchor_check(operation, target_id, anchor, 2, None, None, "ambiguous")
        if anchor.anchor_type == "eof":
            line = max(1, _line_count(content))
            return _anchor_check(operation, target_id, anchor, 1, line, line, "matched")
        if anchor.anchor_type == "line_range" and anchor.line_start is not None:
            return _anchor_check(operation, target_id, anchor, 1, anchor.line_start, anchor.line_end or anchor.line_start, "matched")
        needle = anchor.anchor_text_preview or operation.old_text_preview or ""
        if not needle:
            return _anchor_check(operation, target_id, anchor, 0, None, None, "not_applicable")
        match_count = content.count(needle)
        if match_count == 0:
            return _anchor_check(operation, target_id, anchor, 0, None, None, "missing")
        if match_count > 1:
            return _anchor_check(operation, target_id, anchor, match_count, None, None, "ambiguous")
        start = _line_number_for_index(content, content.find(needle))
        return _anchor_check(operation, target_id, anchor, 1, start, start + max(0, _line_count(needle) - 1), "matched")


class PatchInMemoryApplicabilityEngine:
    def __init__(self, *, anchor_service: PatchAnchorApplicabilityService | None = None) -> None:
        self.anchor_service = anchor_service or PatchAnchorApplicabilityService()

    def simulate_operations(
        self,
        draft: PatchDraft | None,
        preview: DiffPreviewArtifact | None,
        target_snapshots: list[PatchDryRunTargetSnapshot],
        policy: PatchDryRunEnginePolicy,
    ) -> list[PatchDryRunOperationResult]:
        _ = preview
        if draft is None:
            return []
        snapshots = {item.target_id: item for item in target_snapshots}
        results: list[PatchDryRunOperationResult] = []
        for operation in draft.operations:
            target_id = str(operation.target_ref.get("target_id") or "")
            snapshot = snapshots.get(target_id)
            anchor_check = self.anchor_service.check_anchor(operation, snapshot)
            conflicts = _conflicts_from_anchor(operation, target_id, anchor_check)
            content = snapshot._content_for_simulation if snapshot else None
            new_content: str | None = None
            would_apply = False
            if policy.in_memory_only and content is not None and anchor_check.anchor_status in {"matched", "not_applicable"}:
                new_content, extra_conflicts = _simulate_operation(operation, content)
                conflicts.extend(extra_conflicts)
                would_apply = new_content is not None and not extra_conflicts
            applied_in_memory = would_apply
            status = _operation_status(conflicts, snapshot)
            results.append(
                PatchDryRunOperationResult(
                    result_id=f"patch_dry_run_operation_result:{uuid4()}",
                    operation_id=operation.operation_id,
                    target_id=target_id,
                    operation_type=operation.operation_type,
                    anchor_check=anchor_check,
                    would_apply_in_memory=would_apply,
                    applied_in_memory=applied_in_memory,
                    conflict_count=len(conflicts),
                    conflicts=conflicts,
                    resulting_content_hash=_hash_text(new_content) if new_content and policy.in_memory_only else None,
                    resulting_line_count=_line_count(new_content) if new_content else None,
                    result_status=status,
                    file_write_performed=False,
                    workspace_file_changed_emitted=False,
                    evidence_refs=[
                        {"ref_type": "patch_operation_draft", "operation_id": operation.operation_id},
                        {"ref_type": "in_memory_only", "version": SELF_MODIFICATION_DRY_RUN_VERSION},
                    ],
                )
            )
        return results


class PatchDryRunConflictDetector:
    def detect_conflicts(self, operation_results: list[PatchDryRunOperationResult]) -> list[PatchDryRunConflict]:
        conflicts: list[PatchDryRunConflict] = []
        seen: set[tuple[str, int | None]] = set()
        for result in operation_results:
            conflicts.extend(result.conflicts)
            line = result.anchor_check.matched_line_start if result.anchor_check else None
            key = (result.target_id, line)
            if line is not None and key in seen:
                conflicts.append(
                    _conflict(
                        result.operation_id,
                        result.target_id,
                        "overlapping_hunks",
                        "error",
                        "Multiple operations target the same anchor line.",
                    )
                )
            seen.add(key)
        return conflicts


class PatchDryRunFindingService:
    def build_findings(
        self,
        request: PatchDryRunCheckRequest,
        static_report: PatchStaticSafetyReport | None,
        target_snapshots: list[PatchDryRunTargetSnapshot],
        operation_results: list[PatchDryRunOperationResult],
    ) -> list[PatchApplicabilityFinding]:
        findings: list[PatchApplicabilityFinding] = []
        if static_report is None:
            findings.append(_finding("critical", "missing_static_safety_report", "Static safety report is required.", None, None))
        elif static_report.static_safety_status not in {"passed", "warning"}:
            findings.append(
                _finding("critical", "static_safety_not_passed", "Static safety report is failed or blocked.", None, None)
            )
        if not target_snapshots:
            severity = "critical" if request.strictness == "strict" else "error"
            findings.append(_finding(severity, "target_snapshot_unavailable", "Target snapshot is unavailable.", None, None))
        for snapshot in target_snapshots:
            target_ref = snapshot.to_dict()
            if snapshot.private_boundary_risk:
                findings.append(_finding("critical", "private_boundary_block", "Private boundary blocks dry-run.", target_ref, None))
            if snapshot.secret_risk:
                findings.append(_finding("critical", "secret_boundary_block", "Secret boundary blocks dry-run.", target_ref, None))
            if snapshot.truncated:
                findings.append(
                    _finding("warning", "truncated_context_unreliable", "Truncated target context reduces applicability certainty.", target_ref, None)
                )
            if snapshot.redacted:
                findings.append(
                    _finding("warning", "redacted_context_unreliable", "Redacted target context reduces applicability certainty.", target_ref, None)
                )
        for result in operation_results:
            operation_ref = result.to_dict()
            for conflict in result.conflicts:
                severity = conflict.severity
                finding_type = _finding_type_from_conflict(conflict.conflict_type)
                findings.append(_finding(severity, finding_type, conflict.message, conflict.actual_ref, operation_ref))
            if result.result_status == "passed":
                findings.append(_finding("info", "dry_run_passed", "Operation applies to the in-memory buffer.", None, operation_ref))
        if operation_results and all(item.result_status in {"passed", "warning"} for item in operation_results):
            findings.append(
                _finding(
                    "info",
                    "eligible_for_review",
                    "Dry-run result permits moving to human review, not apply.",
                    None,
                    None,
                )
            )
        findings.append(_finding("info", "not_safe_to_apply", "Dry-run is not apply permission.", None, None))
        return findings[: request.max_findings]


class PatchDryRunReportService:
    def __init__(
        self,
        *,
        source_service: PatchDryRunSourceService | None = None,
        engine: PatchInMemoryApplicabilityEngine | None = None,
        conflict_detector: PatchDryRunConflictDetector | None = None,
        finding_service: PatchDryRunFindingService | None = None,
    ) -> None:
        self.source_service = source_service or PatchDryRunSourceService()
        self.engine = engine or PatchInMemoryApplicabilityEngine()
        self.conflict_detector = conflict_detector or PatchDryRunConflictDetector()
        self.finding_service = finding_service or PatchDryRunFindingService()

    def build_report(self, request: PatchDryRunCheckRequest) -> PatchDryRunReport:
        normalized = request.normalized()
        candidate = self.source_service.load_patch_candidate(normalized.patch_candidate_id)
        draft = self.source_service.load_patch_draft(normalized.draft_id)
        preview = self.source_service.load_diff_preview(normalized.preview_id)
        static_report = self.source_service.load_static_safety_report(normalized.static_safety_report_id)
        policy = PatchDryRunEnginePolicy(max_target_bytes=normalized.max_target_bytes)
        snapshots = self.source_service.load_target_snapshots(normalized, draft)
        operation_results = self.engine.simulate_operations(draft, preview, snapshots, policy)[
            : normalized.max_operations
        ]
        all_conflicts = self.conflict_detector.detect_conflicts(operation_results) if normalized.include_conflict_detection else []
        findings = self.finding_service.build_findings(normalized, static_report, snapshots, operation_results)
        operation_conflict_keys = {
            (conflict.operation_id, conflict.target_id, conflict.conflict_type)
            for result in operation_results
            for conflict in result.conflicts
        }
        for conflict in all_conflicts:
            key = (conflict.operation_id, conflict.target_id, conflict.conflict_type)
            if key in operation_conflict_keys:
                continue
            findings.append(
                _finding(
                    conflict.severity,
                    _finding_type_from_conflict(conflict.conflict_type),
                    conflict.message,
                    conflict.actual_ref,
                    {"ref_type": "patch_operation_draft", "operation_id": conflict.operation_id},
                )
            )
        if candidate and candidate.applied:
            findings.append(_finding("critical", "candidate_already_applied", "Applied candidate blocks dry-run.", None, None))
        if draft and draft.applied:
            findings.append(_finding("critical", "draft_already_applied", "Applied draft blocks dry-run.", None, None))
        status = _dry_run_status(findings, operation_results)
        eligible = status in {"passed", "warning"}
        return PatchDryRunReport(
            report_id=f"patch_dry_run_report:{uuid4()}",
            created_at=utc_now_iso(),
            request=normalized,
            patch_candidate_id=candidate.candidate_id if candidate else normalized.patch_candidate_id,
            draft_id=draft.draft_id if draft else normalized.draft_id,
            preview_id=preview.preview_id if preview else normalized.preview_id,
            static_safety_report_id=static_report.report_id if static_report else normalized.static_safety_report_id,
            engine_policy=policy,
            target_snapshots=snapshots,
            operation_results=operation_results,
            findings=findings[: normalized.max_findings],
            checked_operation_count=len(operation_results),
            passed_operation_count=sum(1 for item in operation_results if item.result_status == "passed"),
            warning_operation_count=sum(1 for item in operation_results if item.result_status == "warning"),
            failed_operation_count=sum(1 for item in operation_results if item.result_status == "failed"),
            blocked_operation_count=sum(1 for item in operation_results if item.result_status == "blocked"),
            conflict_count=len(all_conflicts),
            dry_run_status=status,
            eligible_for_review=eligible,
            safe_to_apply=False,
            human_review_required=True,
            apply_gate_required=True,
            rollback_plan_required=True,
            post_apply_verification_required=True,
            review_status="report_only",
            file_write_enabled=False,
            apply_patch_enabled=False,
            file_write_performed=False,
            patch_applied=False,
            workspace_file_changed_emitted=False,
            shell_executed=False,
            test_lint_executed=False,
            limitations=[
                "Patch dry-run is in-memory only.",
                "Dry-run pass is not human review approval.",
                "Dry-run pass is not apply permission.",
            ],
            withdrawal_conditions=[
                "Withdraw if workspace file mutation occurs.",
                "Withdraw if external patch command, shell, test, or lint execution occurs.",
                "Withdraw if dry-run marks safe_to_apply true.",
            ],
        )


class SelfModificationDryRunService:
    def __init__(self, *, report_service: PatchDryRunReportService | None = None) -> None:
        self.report_service = report_service or PatchDryRunReportService()

    def check_applicability(self, request: PatchDryRunCheckRequest) -> PatchDryRunResult:
        report = self.report_service.build_report(request)
        no_action = None
        needs_more_input = None
        if report.dry_run_status in {"failed", "blocked"}:
            no_action = PatchDryRunNoActionCandidate(
                candidate_id=f"patch_dry_run_no_action_candidate:{uuid4()}",
                report_id=report.report_id,
                reason="Dry-run applicability report contains failed or blocked findings.",
                evidence_refs=_finding_evidence(report.findings),
                recommended_review_decision="no_action",
                candidate_status="candidate_only",
                applied=False,
            )
        elif any(item.finding_type == "target_snapshot_unavailable" for item in report.findings):
            needs_more_input = PatchDryRunNeedsMoreInputCandidate(
                candidate_id=f"patch_dry_run_needs_more_input_candidate:{uuid4()}",
                report_id=report.report_id,
                reason="Dry-run requires target snapshot input.",
                missing_inputs=["target_snapshot"],
                evidence_refs=_finding_evidence(report.findings),
                recommended_review_decision="needs_more_input",
                candidate_status="candidate_only",
                applied=False,
            )
        return PatchDryRunResult(report=report, no_action_candidate=no_action, needs_more_input_candidate=needs_more_input)

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "report_name": "Self-Modification Patch Dry-run Applicability PIG Report",
            "version": SELF_MODIFICATION_DRY_RUN_VERSION,
            "layer": "self_modification_safety",
            "subject": "patch_dry_run_applicability_check",
            "principles": [
                "dry-run is not apply",
                "dry-run is not file mutation",
                "dry-run pass is not human approval",
                "dry-run pass is not apply gate",
                "dry-run pass only permits moving to human review stage",
            ],
            "in_memory_only": True,
            "file_write_performed": False,
            "patch_applied": False,
            "workspace_file_changed_emitted": False,
            "shell_executed": False,
            "test_lint_executed": False,
            "safe_to_apply": False,
            "llm_judge_enabled": False,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "projection_name": "Self-Modification Patch Dry-run Applicability OCPX Projection",
            "state": SELF_MODIFICATION_DRY_RUN_STATE,
            "version": SELF_MODIFICATION_DRY_RUN_VERSION,
            "source_read_models": [
                "PatchStaticSafetyState",
                "PatchDraftState",
                "DiffPreviewState",
                "PatchOperationDraftState",
                "PatchCandidateState",
                "SelfModificationLifecyclePolicyState",
            ],
            "target_read_models": [
                "PatchDryRunState",
                "PatchApplicabilityState",
                "PatchDryRunConflictState",
                "PatchReviewEligibilityState",
            ],
            "effect_types": ["read_only_observation", "state_candidate_created"],
        }

    def render_result_cli(self, result: PatchDryRunResult) -> str:
        report = result.report
        return "\n".join(
            [
                "Self-Modification Patch Dry-run Applicability Check",
                "version=v0.22.4",
                "layer=self_modification_safety",
                f"report_id={report.report_id}",
                f"dry_run_status={report.dry_run_status}",
                f"eligible_for_review={str(report.eligible_for_review).lower()}",
                "safe_to_apply=false",
                "human_review_required=true",
                "apply_gate_required=true",
                "rollback_plan_required=true",
                "post_apply_verification_required=true",
                "file_write_enabled=false",
                "apply_patch_enabled=false",
                "file_write_performed=false",
                "patch_applied=false",
                "workspace_file_changed_emitted=false",
                "shell_executed=false",
                "test_lint_executed=false",
                "next_required_step=v0.22.5 Human Review & Apply Gate",
                "No file mutation occurred.",
                "private_full_paths_printed=False",
                "raw_target_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_report_view_cli(self, *, report_id: str) -> str:
        return "\n".join(
            [
                "Self-Modification Patch Dry-run Report",
                "version=v0.22.4",
                "layer=self_modification_safety",
                f"report_id={report_id}",
                "status=not_persisted_in_v0.22.4",
                "dry_run_status=unknown_without_persisted_report",
                "eligible_for_review=false",
                "safe_to_apply=false",
                "human_review_required=true",
                "apply_gate_required=true",
                "file_write_performed=false",
                "patch_applied=false",
                "workspace_file_changed_emitted=false",
                "shell_executed=false",
                "test_lint_executed=false",
                "next_required_step=v0.22.5 Human Review & Apply Gate",
                "No file mutation occurred.",
                "private_full_paths_printed=False",
                "raw_target_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_conflicts_cli(self, *, report_id: str) -> str:
        return "\n".join(
            [
                "Self-Modification Patch Dry-run Conflicts",
                "version=v0.22.4",
                "layer=self_modification_safety",
                f"report_id={report_id}",
                "conflict_types=anchor_missing,anchor_ambiguous,old_text_mismatch,context_mismatch,operation_order_conflict,overlapping_hunks",
                "safe_to_apply=false",
                "file_write_performed=false",
                "patch_applied=false",
                "workspace_file_changed_emitted=false",
                "No file mutation occurred.",
                "private_full_paths_printed=False",
                "raw_target_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_pig_report_cli(self) -> str:
        report = self.build_pig_report()
        return "\n".join(
            [
                "Self-Modification Patch Dry-run Applicability PIG Report",
                "version=v0.22.4",
                "layer=self_modification_safety",
                f"subject={report['subject']}",
                f"principles={','.join(report['principles'])}",
                f"in_memory_only={str(report['in_memory_only']).lower()}",
                f"file_write_performed={str(report['file_write_performed']).lower()}",
                f"patch_applied={str(report['patch_applied']).lower()}",
                f"workspace_file_changed_emitted={str(report['workspace_file_changed_emitted']).lower()}",
                f"shell_executed={str(report['shell_executed']).lower()}",
                f"test_lint_executed={str(report['test_lint_executed']).lower()}",
                "file_write_enabled=false",
                "apply_patch_enabled=false",
                "safe_to_apply=false",
                f"llm_judge_enabled={str(report['llm_judge_enabled']).lower()}",
                "no_file_mutation_occurred=true",
                "No file mutation occurred.",
                "private_full_paths_printed=False",
                "raw_file_content_printed=False",
                "raw_target_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_ocpx_projection_cli(self) -> str:
        projection = self.build_ocpx_projection()
        return "\n".join(
            [
                "Self-Modification Patch Dry-run Applicability OCPX Projection",
                "version=v0.22.4",
                "layer=self_modification_safety",
                f"state={projection['state']}",
                f"source_read_models={','.join(projection['source_read_models'])}",
                f"target_read_models={','.join(projection['target_read_models'])}",
                f"effect_types={','.join(projection['effect_types'])}",
                "safe_to_apply=false",
                "file_write_enabled=false",
                "apply_patch_enabled=false",
                "file_write_performed=false",
                "patch_applied=false",
                "workspace_file_changed_emitted=false",
                "no_file_mutation_occurred=true",
                "No file mutation occurred.",
                "private_full_paths_printed=False",
                "raw_file_content_printed=False",
                "raw_target_content_printed=False",
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


def _simulation_content_for_context(target_id: str, operations: list[PatchOperationDraft]) -> str:
    parts: list[str] = []
    for operation in operations:
        op_target_id = str(operation.target_ref.get("target_id") or "")
        if op_target_id != target_id:
            continue
        if operation.anchor_ref and operation.anchor_ref.anchor_text_preview and operation.old_text_preview:
            parts.append(operation.anchor_ref.anchor_text_preview)
        elif operation.old_text_preview:
            parts.append(operation.old_text_preview)
        if operation.operation_type in {"append_block", "comment_only_change"}:
            parts.append("")
    return "\n".join(parts) or "sanitized context only"


def _anchor_check(
    operation: PatchOperationDraft,
    target_id: str,
    anchor: PatchAnchorRef | None,
    match_count: int,
    line_start: int | None,
    line_end: int | None,
    status: str,
) -> PatchAnchorApplicabilityCheck:
    return PatchAnchorApplicabilityCheck(
        check_id=f"patch_anchor_applicability_check:{uuid4()}",
        operation_id=operation.operation_id,
        target_id=target_id,
        anchor_id=anchor.anchor_id if anchor else None,
        anchor_type=anchor.anchor_type if anchor else None,
        match_count=match_count,
        matched_line_start=line_start,
        matched_line_end=line_end,
        ambiguous=status == "ambiguous",
        found=status == "matched",
        anchor_status=status,
        evidence_refs=[{"ref_type": "patch_anchor_ref", "anchor_id": anchor.anchor_id if anchor else None}],
    )


def _conflicts_from_anchor(
    operation: PatchOperationDraft,
    target_id: str,
    anchor_check: PatchAnchorApplicabilityCheck,
) -> list[PatchDryRunConflict]:
    if anchor_check.anchor_status == "missing":
        return [_conflict(operation.operation_id, target_id, "anchor_missing", "error", "Patch anchor is missing.")]
    if anchor_check.anchor_status == "ambiguous":
        return [_conflict(operation.operation_id, target_id, "anchor_ambiguous", "error", "Patch anchor is ambiguous.")]
    if anchor_check.anchor_status == "blocked":
        return [
            _conflict(
                operation.operation_id,
                target_id,
                "target_snapshot_unavailable",
                "critical",
                "Target snapshot is unavailable.",
            )
        ]
    return []


def _simulate_operation(
    operation: PatchOperationDraft,
    content: str,
) -> tuple[str | None, list[PatchDryRunConflict]]:
    target_id = str(operation.target_ref.get("target_id") or "unknown")
    old = operation.old_text_preview or ""
    new = operation.new_text_preview or ""
    if operation.operation_type == "text_replace":
        if not old or old not in content:
            return None, [_conflict(operation.operation_id, target_id, "old_text_mismatch", "error", "Old text preview did not match.")]
        return content.replace(old, new, 1), []
    if operation.operation_type == "insert_after":
        anchor_text = operation.anchor_ref.anchor_text_preview if operation.anchor_ref else None
        if anchor_text and anchor_text in content:
            return content.replace(anchor_text, anchor_text + "\n" + new, 1), []
        return None, [_conflict(operation.operation_id, target_id, "context_mismatch", "error", "Insert anchor context did not match.")]
    if operation.operation_type in {"append_block", "comment_only_change"}:
        suffix = "\n" if content and not content.endswith("\n") else ""
        return content + suffix + new, []
    return None, [_conflict(operation.operation_id, target_id, "operation_order_conflict", "error", "Operation type is not simulatable.")]


def _conflict(
    operation_id: str,
    target_id: str,
    conflict_type: str,
    severity: str,
    message: str,
) -> PatchDryRunConflict:
    return PatchDryRunConflict(
        conflict_id=f"patch_dry_run_conflict:{uuid4()}",
        operation_id=operation_id,
        target_id=target_id,
        conflict_type=conflict_type,
        severity=severity,
        message=message,
        expected_ref={"ref_type": "patch_operation_draft", "operation_id": operation_id},
        actual_ref={"ref_type": "patch_dry_run_target_snapshot", "target_id": target_id},
        evidence_refs=[{"ref_type": "patch_dry_run_version", "version": SELF_MODIFICATION_DRY_RUN_VERSION}],
    )


def _operation_status(conflicts: list[PatchDryRunConflict], snapshot: PatchDryRunTargetSnapshot | None) -> str:
    if snapshot is None or any(item.severity == "critical" for item in conflicts):
        return "blocked"
    if any(item.severity == "error" for item in conflicts):
        return "failed"
    if snapshot.truncated or snapshot.redacted:
        return "warning"
    return "passed"


def _finding(
    severity: str,
    finding_type: str,
    message: str,
    target_ref: dict[str, Any] | None,
    operation_ref: dict[str, Any] | None,
) -> PatchApplicabilityFinding:
    return PatchApplicabilityFinding(
        finding_id=f"patch_applicability_finding:{uuid4()}",
        severity=severity,
        finding_type=finding_type,
        message=message,
        target_ref=target_ref,
        operation_ref=operation_ref,
        evidence_refs=[{"ref_type": "patch_dry_run_version", "version": SELF_MODIFICATION_DRY_RUN_VERSION}],
        withdrawal_condition="Withdraw if workspace files are changed or dry-run is treated as apply permission.",
    )


def _finding_type_from_conflict(conflict_type: str) -> str:
    return {
        "anchor_missing": "anchor_missing",
        "anchor_ambiguous": "anchor_ambiguous",
        "old_text_mismatch": "old_text_mismatch",
        "context_mismatch": "context_mismatch",
        "operation_order_conflict": "operation_conflict",
        "overlapping_hunks": "overlapping_hunks",
        "target_snapshot_unavailable": "target_snapshot_unavailable",
        "private_boundary_block": "private_boundary_block",
        "secret_boundary_block": "secret_boundary_block",
    }.get(conflict_type, "operation_conflict")


def _dry_run_status(
    findings: list[PatchApplicabilityFinding],
    operation_results: list[PatchDryRunOperationResult],
) -> str:
    finding_types = {item.finding_type for item in findings}
    if finding_types & {
        "missing_static_safety_report",
        "static_safety_not_passed",
        "private_boundary_block",
        "secret_boundary_block",
        "target_snapshot_unavailable",
        "candidate_already_applied",
        "draft_already_applied",
    }:
        return "blocked"
    if any(item.severity == "critical" for item in findings):
        return "blocked"
    if any(item.result_status == "failed" for item in operation_results) or any(item.severity == "error" for item in findings):
        return "failed"
    if any(item.result_status == "warning" for item in operation_results) or any(item.severity == "warning" for item in findings):
        return "warning"
    return "passed" if operation_results else "blocked"


def _finding_evidence(findings: list[PatchApplicabilityFinding]) -> list[dict[str, Any]]:
    return [{"finding_type": item.finding_type, "severity": item.severity} for item in findings[:20]]


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _line_count(text: str | None) -> int:
    if not text:
        return 0
    return max(1, len(text.splitlines()))


def _line_ending(text: str) -> str:
    return "crlf" if "\r\n" in text else "lf"


def _line_number_for_index(text: str, index: int) -> int:
    return text[: max(index, 0)].count("\n") + 1


def _is_secret_path(relative_path: str | None) -> bool:
    if not relative_path:
        return False
    lowered = relative_path.replace("\\", "/").casefold()
    return lowered.endswith(".env") or "/.env" in lowered or "secret" in lowered


def _is_generated_path(relative_path: str | None) -> bool:
    if not relative_path:
        return False
    lowered = relative_path.replace("\\", "/").casefold()
    return "generated" in lowered or lowered.startswith("build/")
