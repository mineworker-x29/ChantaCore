from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.self_modification_safety.candidate import (
    ModificationTargetRef,
    PatchCandidate,
    PatchCandidateFinding,
    PatchConstraintDescriptor,
    PatchIntentDescriptor,
    PatchPreliminaryRiskAssessment,
    PatchScopeDescriptor,
)
from chanta_core.self_modification_safety.models import SelfModificationAllowedPatchPolicy
from chanta_core.utility.time import utc_now_iso


SELF_MODIFICATION_PATCH_DRAFT_VERSION = "v0.22.2"
SELF_MODIFICATION_PATCH_DRAFT_STATE = "self_modification_patch_draft_diff_preview_created"
PATCH_DRAFT_CREATE_SKILL_ID = "skill:self_modification_patch_draft_create"
DIFF_PREVIEW_SKILL_ID = "skill:self_modification_diff_preview"


@dataclass(frozen=True)
class PatchDraftCreateRequest:
    patch_candidate_id: str
    request_id: str | None = None
    target_refs: list[dict[str, Any]] = field(default_factory=list)
    operation_hints: list[dict[str, Any]] = field(default_factory=list)
    requested_preview_format: str = "unified_diff_like"
    include_target_context: bool = True
    max_context_lines: int = 12
    max_hunks: int = 3
    max_added_lines: int = 80
    max_removed_lines: int = 80
    allow_no_action: bool = True
    allow_needs_more_input: bool = True
    strictness: str = "standard"

    def normalized(self) -> "PatchDraftCreateRequest":
        return PatchDraftCreateRequest(
            patch_candidate_id=str(self.patch_candidate_id or "").strip(),
            request_id=str(self.request_id).strip() if self.request_id else None,
            target_refs=[dict(item) for item in self.target_refs],
            operation_hints=[dict(item) for item in self.operation_hints],
            requested_preview_format=self.requested_preview_format
            if self.requested_preview_format in {"unified_diff_like", "structured", "summary"}
            else "unified_diff_like",
            include_target_context=bool(self.include_target_context),
            max_context_lines=max(0, int(self.max_context_lines)),
            max_hunks=max(1, int(self.max_hunks)),
            max_added_lines=max(0, int(self.max_added_lines)),
            max_removed_lines=max(0, int(self.max_removed_lines)),
            allow_no_action=bool(self.allow_no_action),
            allow_needs_more_input=bool(self.allow_needs_more_input),
            strictness=self.strictness or "standard",
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "patch_candidate_id": self.patch_candidate_id,
            "request_id": self.request_id,
            "target_refs": [dict(item) for item in self.target_refs],
            "operation_hints": [_sanitize_dict(item) for item in self.operation_hints],
            "requested_preview_format": self.requested_preview_format,
            "include_target_context": self.include_target_context,
            "max_context_lines": self.max_context_lines,
            "max_hunks": self.max_hunks,
            "max_added_lines": self.max_added_lines,
            "max_removed_lines": self.max_removed_lines,
            "allow_no_action": self.allow_no_action,
            "allow_needs_more_input": self.allow_needs_more_input,
            "strictness": self.strictness,
        }


@dataclass(frozen=True)
class PatchTargetContextRef:
    context_id: str
    target_id: str
    target_type: str
    relative_path: str | None
    content_available: bool
    content_source: str
    line_range_start: int | None
    line_range_end: int | None
    truncated: bool
    redacted: bool
    private_boundary_risk: bool
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "context_id": self.context_id,
            "target_id": self.target_id,
            "target_type": self.target_type,
            "relative_path": self.relative_path,
            "content_available": self.content_available,
            "content_source": self.content_source,
            "line_range_start": self.line_range_start,
            "line_range_end": self.line_range_end,
            "truncated": self.truncated,
            "redacted": self.redacted,
            "private_boundary_risk": self.private_boundary_risk,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class PatchAnchorRef:
    anchor_id: str
    target_id: str
    relative_path: str | None
    anchor_type: str
    anchor_text_preview: str | None
    line_start: int | None
    line_end: int | None
    confidence: str
    ambiguous: bool
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "anchor_id": self.anchor_id,
            "target_id": self.target_id,
            "relative_path": self.relative_path,
            "anchor_type": self.anchor_type,
            "anchor_text_preview": self.anchor_text_preview,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "confidence": self.confidence,
            "ambiguous": self.ambiguous,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class PatchOperationDraft:
    operation_id: str
    operation_type: str
    target_ref: dict[str, Any]
    anchor_ref: PatchAnchorRef | None
    old_text_preview: str | None
    new_text_preview: str | None
    rationale: str
    added_line_count: int
    removed_line_count: int
    operation_status: str
    applies_cleanly: bool | None = None
    static_safety_checked: bool = False
    dry_run_checked: bool = False
    applied: bool = False
    file_write_enabled: bool = False
    apply_patch_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "operation_type": self.operation_type,
            "target_ref": dict(self.target_ref),
            "anchor_ref": self.anchor_ref.to_dict() if self.anchor_ref else None,
            "old_text_preview": self.old_text_preview,
            "new_text_preview": self.new_text_preview,
            "rationale": self.rationale,
            "added_line_count": self.added_line_count,
            "removed_line_count": self.removed_line_count,
            "operation_status": self.operation_status,
            "applies_cleanly": self.applies_cleanly,
            "static_safety_checked": self.static_safety_checked,
            "dry_run_checked": self.dry_run_checked,
            "applied": self.applied,
            "file_write_enabled": self.file_write_enabled,
            "apply_patch_enabled": self.apply_patch_enabled,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class DiffHunkPreview:
    hunk_id: str
    target_id: str
    relative_path: str | None
    operation_id: str
    original_line_start: int | None
    original_line_count: int | None
    new_line_start: int | None
    new_line_count: int | None
    context_lines_preview: list[str]
    removed_lines_preview: list[str]
    added_lines_preview: list[str]
    truncated: bool
    redacted: bool
    applies_cleanly: bool | None = None
    dry_run_checked: bool = False
    applied: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "hunk_id": self.hunk_id,
            "target_id": self.target_id,
            "relative_path": self.relative_path,
            "operation_id": self.operation_id,
            "original_line_start": self.original_line_start,
            "original_line_count": self.original_line_count,
            "new_line_start": self.new_line_start,
            "new_line_count": self.new_line_count,
            "context_lines_preview": list(self.context_lines_preview),
            "removed_lines_preview": list(self.removed_lines_preview),
            "added_lines_preview": list(self.added_lines_preview),
            "truncated": self.truncated,
            "redacted": self.redacted,
            "applies_cleanly": self.applies_cleanly,
            "dry_run_checked": self.dry_run_checked,
            "applied": self.applied,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class PatchDraftFinding:
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
class PatchDraft:
    draft_id: str
    patch_candidate_id: str
    request_id: str | None
    created_at: str
    target_context_refs: list[PatchTargetContextRef]
    anchors: list[PatchAnchorRef]
    operations: list[PatchOperationDraft]
    findings: list[PatchDraftFinding]
    lifecycle_state: str = "preview_created"
    draft_status: str = "draft_only"
    candidate_status: str = "candidate_only"
    static_safety_checked: bool = False
    dry_run_checked: bool = False
    review_approved: bool = False
    apply_gate_opened: bool = False
    applied: bool = False
    file_write_enabled: bool = False
    apply_patch_enabled: bool = False
    execution_enabled: bool = False
    materialized: bool = False
    promoted: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "draft_id": self.draft_id,
            "patch_candidate_id": self.patch_candidate_id,
            "request_id": self.request_id,
            "created_at": self.created_at,
            "target_context_refs": [item.to_dict() for item in self.target_context_refs],
            "anchors": [item.to_dict() for item in self.anchors],
            "operations": [item.to_dict() for item in self.operations],
            "findings": [item.to_dict() for item in self.findings],
            "lifecycle_state": self.lifecycle_state,
            "draft_status": self.draft_status,
            "candidate_status": self.candidate_status,
            "static_safety_checked": self.static_safety_checked,
            "dry_run_checked": self.dry_run_checked,
            "review_approved": self.review_approved,
            "apply_gate_opened": self.apply_gate_opened,
            "applied": self.applied,
            "file_write_enabled": self.file_write_enabled,
            "apply_patch_enabled": self.apply_patch_enabled,
            "execution_enabled": self.execution_enabled,
            "materialized": self.materialized,
            "promoted": self.promoted,
        }


@dataclass(frozen=True)
class DiffPreviewArtifact:
    preview_id: str
    draft_id: str
    patch_candidate_id: str
    created_at: str
    preview_format: str
    target_refs: list[dict[str, Any]]
    hunk_previews: list[DiffHunkPreview]
    findings: list[PatchDraftFinding]
    preview_text_sanitized: str | None
    truncated: bool
    redacted: bool
    lifecycle_state: str = "preview_created"
    preview_status: str = "preview_only"
    static_safety_checked: bool = False
    dry_run_checked: bool = False
    applies_cleanly: bool | None = None
    applied: bool = False
    file_write_enabled: bool = False
    apply_patch_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "preview_id": self.preview_id,
            "draft_id": self.draft_id,
            "patch_candidate_id": self.patch_candidate_id,
            "created_at": self.created_at,
            "preview_format": self.preview_format,
            "target_refs": [dict(item) for item in self.target_refs],
            "hunk_previews": [item.to_dict() for item in self.hunk_previews],
            "findings": [item.to_dict() for item in self.findings],
            "preview_text_sanitized": self.preview_text_sanitized,
            "truncated": self.truncated,
            "redacted": self.redacted,
            "lifecycle_state": self.lifecycle_state,
            "preview_status": self.preview_status,
            "static_safety_checked": self.static_safety_checked,
            "dry_run_checked": self.dry_run_checked,
            "applies_cleanly": self.applies_cleanly,
            "applied": self.applied,
            "file_write_enabled": self.file_write_enabled,
            "apply_patch_enabled": self.apply_patch_enabled,
        }


@dataclass(frozen=True)
class PatchDraftNeedsMoreInputCandidate:
    candidate_id: str
    patch_candidate_id: str | None
    reason: str
    missing_inputs: list[str]
    evidence_refs: list[dict[str, Any]]
    recommended_review_decision: str = "needs_more_input"
    candidate_status: str = "candidate_only"
    applied: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "patch_candidate_id": self.patch_candidate_id,
            "reason": self.reason,
            "missing_inputs": list(self.missing_inputs),
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "recommended_review_decision": self.recommended_review_decision,
            "candidate_status": self.candidate_status,
            "applied": self.applied,
        }


@dataclass(frozen=True)
class PatchDraftNoActionCandidate:
    candidate_id: str
    patch_candidate_id: str | None
    reason: str
    evidence_refs: list[dict[str, Any]]
    recommended_review_decision: str = "no_action"
    candidate_status: str = "candidate_only"
    applied: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "patch_candidate_id": self.patch_candidate_id,
            "reason": self.reason,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "recommended_review_decision": self.recommended_review_decision,
            "candidate_status": self.candidate_status,
            "applied": self.applied,
        }


@dataclass(frozen=True)
class PatchDraftDiffPreviewResult:
    patch_candidate: PatchCandidate | None
    draft: PatchDraft | None
    diff_preview: DiffPreviewArtifact | None
    no_action_candidate: PatchDraftNoActionCandidate | None
    needs_more_input_candidate: PatchDraftNeedsMoreInputCandidate | None
    findings: list[PatchDraftFinding]

    def to_dict(self) -> dict[str, Any]:
        return {
            "patch_candidate": self.patch_candidate.to_dict() if self.patch_candidate else None,
            "draft": self.draft.to_dict() if self.draft else None,
            "diff_preview": self.diff_preview.to_dict() if self.diff_preview else None,
            "no_action_candidate": self.no_action_candidate.to_dict() if self.no_action_candidate else None,
            "needs_more_input_candidate": self.needs_more_input_candidate.to_dict()
            if self.needs_more_input_candidate
            else None,
            "findings": [item.to_dict() for item in self.findings],
        }


class PatchDraftPolicyService:
    def decide(
        self,
        *,
        request: PatchDraftCreateRequest,
        patch_candidate: PatchCandidate | None,
        findings: list[PatchDraftFinding],
    ) -> str:
        normalized = request.normalized()
        if patch_candidate is None:
            return "needs_more_input" if normalized.allow_needs_more_input else "blocked"
        hard_types = {
            "candidate_not_candidate_only",
            "candidate_already_applied",
            "operation_type_forbidden",
            "operation_scope_exceeds_limit",
            "added_lines_exceed_limit",
            "removed_lines_exceed_limit",
            "private_boundary_risk",
            "secret_content_risk",
        }
        if any(item.finding_type in hard_types for item in findings):
            return "no_action" if normalized.allow_no_action else "blocked"
        if any(item.finding_type in {"target_context_unavailable", "anchor_ambiguous", "anchor_not_found"} for item in findings):
            return "needs_more_input" if normalized.allow_needs_more_input else "blocked"
        return "preview_created"


class PatchDraftSourceService:
    def __init__(self, patch_candidates: dict[str, PatchCandidate] | None = None, *, allow_synthetic: bool = False) -> None:
        self.patch_candidates = dict(patch_candidates or {})
        self.allow_synthetic = allow_synthetic

    def load_patch_candidate(self, patch_candidate_id: str) -> PatchCandidate | None:
        candidate = self.patch_candidates.get(patch_candidate_id)
        if candidate is not None:
            return candidate
        if self.allow_synthetic:
            return _synthetic_patch_candidate(patch_candidate_id)
        return None

    def collect_target_context(
        self,
        request: PatchDraftCreateRequest,
        patch_candidate: PatchCandidate,
    ) -> list[PatchTargetContextRef]:
        normalized = request.normalized()
        contexts: list[PatchTargetContextRef] = []
        target_refs = patch_candidate.target_refs or [_target_from_dict(item) for item in normalized.target_refs]
        hints = normalized.operation_hints
        for target in target_refs:
            hint = _hint_for_target(hints, target)
            has_context = bool(hint.get("provided_context") or hint.get("old_text_preview") or hint.get("new_text_preview"))
            contexts.append(
                PatchTargetContextRef(
                    context_id=f"patch_target_context_ref:{uuid4()}",
                    target_id=target.target_id,
                    target_type=target.target_type,
                    relative_path=target.relative_path,
                    content_available=has_context,
                    content_source="provided_context" if has_context else "unavailable",
                    line_range_start=_optional_int(hint.get("line_range_start")),
                    line_range_end=_optional_int(hint.get("line_range_end")),
                    truncated=True,
                    redacted=True,
                    private_boundary_risk=target.private_boundary_risk,
                    evidence_refs=[
                        {"ref_type": "patch_candidate_target_ref", "target_id": target.target_id},
                        {"ref_type": "sanitized_target_context", "version": SELF_MODIFICATION_PATCH_DRAFT_VERSION},
                    ],
                )
            )
        return contexts


class PatchAnchorCollector:
    def collect_anchors(
        self,
        context_refs: list[PatchTargetContextRef],
        request: PatchDraftCreateRequest,
    ) -> list[PatchAnchorRef]:
        hints = request.normalized().operation_hints
        anchors: list[PatchAnchorRef] = []
        for context in context_refs:
            hint = _hint_for_context(hints, context)
            anchor_type = str(hint.get("anchor_type") or "eof")
            if anchor_type not in {"exact_text", "line_range", "symbol", "heading", "eof", "unknown"}:
                anchor_type = "unknown"
            ambiguous = bool(hint.get("ambiguous_anchor", False))
            anchor_preview = _sanitize_text(hint.get("anchor_text_preview") or hint.get("anchor_text"), limit=160)
            anchors.append(
                PatchAnchorRef(
                    anchor_id=f"patch_anchor_ref:{uuid4()}",
                    target_id=context.target_id,
                    relative_path=context.relative_path,
                    anchor_type=anchor_type,
                    anchor_text_preview=anchor_preview,
                    line_start=_optional_int(hint.get("line_start")),
                    line_end=_optional_int(hint.get("line_end")),
                    confidence="low" if ambiguous else str(hint.get("confidence") or "medium"),
                    ambiguous=ambiguous,
                    evidence_refs=[
                        {"ref_type": "sanitized_anchor_hint", "version": SELF_MODIFICATION_PATCH_DRAFT_VERSION}
                    ],
                )
            )
        return anchors


class PatchOperationDraftBuilder:
    def __init__(self, patch_policy: SelfModificationAllowedPatchPolicy | None = None) -> None:
        self.patch_policy = patch_policy or SelfModificationAllowedPatchPolicy()

    def build_operations(
        self,
        request: PatchDraftCreateRequest,
        patch_candidate: PatchCandidate,
        context_refs: list[PatchTargetContextRef],
        anchors: list[PatchAnchorRef],
    ) -> list[PatchOperationDraft]:
        normalized = request.normalized()
        hints = normalized.operation_hints or [{"operation_type": patch_candidate.intent.allowed_patch_type_candidate}]
        operations: list[PatchOperationDraft] = []
        for index, context in enumerate(context_refs):
            hint = _hint_for_context(hints, context) if hints else {}
            anchor = _anchor_for_context(anchors, context)
            operation_type = str(hint.get("operation_type") or patch_candidate.intent.allowed_patch_type_candidate or "comment_only_change")
            old_preview = _sanitize_text(hint.get("old_text_preview"), limit=320)
            new_preview = _sanitize_text(hint.get("new_text_preview") or hint.get("insert_text_preview"), limit=320)
            added = _line_count(new_preview)
            removed = _line_count(old_preview)
            status = "drafted"
            if operation_type not in self.patch_policy.allowed_patch_types:
                status = "blocked"
            elif added > normalized.max_added_lines or removed > normalized.max_removed_lines:
                status = "blocked"
            elif anchor and anchor.ambiguous:
                status = "needs_more_input"
            elif context.content_source == "unavailable" and operation_type != "append_block":
                status = "needs_more_input"
            operations.append(
                PatchOperationDraft(
                    operation_id=f"patch_operation_draft:{uuid4()}",
                    operation_type=operation_type,
                    target_ref=context.to_dict(),
                    anchor_ref=anchor,
                    old_text_preview=old_preview,
                    new_text_preview=new_preview or _default_new_preview(index),
                    rationale=str(hint.get("rationale") or "Candidate-only patch operation preview."),
                    added_line_count=added or 1,
                    removed_line_count=removed,
                    operation_status=status,
                    applies_cleanly=None,
                    static_safety_checked=False,
                    dry_run_checked=False,
                    applied=False,
                    file_write_enabled=False,
                    apply_patch_enabled=False,
                    evidence_refs=[
                        {"ref_type": "patch_draft_policy", "version": SELF_MODIFICATION_PATCH_DRAFT_VERSION}
                    ],
                )
            )
        return operations[: normalized.max_hunks]


class DiffPreviewBuilder:
    def build_preview(self, draft: PatchDraft, request: PatchDraftCreateRequest) -> DiffPreviewArtifact:
        normalized = request.normalized()
        hunk_previews: list[DiffHunkPreview] = []
        for operation in draft.operations[: normalized.max_hunks]:
            target_id = str(operation.target_ref.get("target_id") or "unknown")
            relative_path = operation.target_ref.get("relative_path")
            anchor = operation.anchor_ref
            hunk_previews.append(
                DiffHunkPreview(
                    hunk_id=f"diff_hunk_preview:{uuid4()}",
                    target_id=target_id,
                    relative_path=str(relative_path) if relative_path else None,
                    operation_id=operation.operation_id,
                    original_line_start=anchor.line_start if anchor else None,
                    original_line_count=operation.removed_line_count or None,
                    new_line_start=anchor.line_start if anchor else None,
                    new_line_count=operation.added_line_count or None,
                    context_lines_preview=_bounded_lines(anchor.anchor_text_preview if anchor else None, normalized.max_context_lines),
                    removed_lines_preview=_bounded_lines(operation.old_text_preview, normalized.max_context_lines),
                    added_lines_preview=_bounded_lines(operation.new_text_preview, normalized.max_context_lines),
                    truncated=True,
                    redacted=True,
                    applies_cleanly=None,
                    dry_run_checked=False,
                    applied=False,
                    evidence_refs=[
                        {"ref_type": "patch_operation_draft", "operation_id": operation.operation_id}
                    ],
                )
            )
        return DiffPreviewArtifact(
            preview_id=f"diff_preview:{uuid4()}",
            draft_id=draft.draft_id,
            patch_candidate_id=draft.patch_candidate_id,
            created_at=draft.created_at,
            preview_format=normalized.requested_preview_format,
            target_refs=[item.to_dict() for item in draft.target_context_refs],
            hunk_previews=hunk_previews,
            findings=list(draft.findings),
            preview_text_sanitized=_render_sanitized_preview(hunk_previews, normalized.requested_preview_format),
            truncated=True,
            redacted=True,
            lifecycle_state="preview_created",
            preview_status="preview_only",
            static_safety_checked=False,
            dry_run_checked=False,
            applies_cleanly=None,
            applied=False,
            file_write_enabled=False,
            apply_patch_enabled=False,
        )


class PatchDraftFindingService:
    def __init__(self, patch_policy: SelfModificationAllowedPatchPolicy | None = None) -> None:
        self.patch_policy = patch_policy or SelfModificationAllowedPatchPolicy()

    def evaluate(
        self,
        request: PatchDraftCreateRequest,
        patch_candidate: PatchCandidate | None,
        context_refs: list[PatchTargetContextRef],
        anchors: list[PatchAnchorRef],
        operations: list[PatchOperationDraft],
    ) -> list[PatchDraftFinding]:
        normalized = request.normalized()
        findings: list[PatchDraftFinding] = []
        if patch_candidate is None:
            findings.append(_draft_finding("warning", "missing_patch_candidate", "Patch candidate is required.", None, None))
            return findings
        if patch_candidate.candidate_status != "candidate_only":
            findings.append(_draft_finding("error", "candidate_not_candidate_only", "Patch candidate is not candidate-only.", None, None))
        if patch_candidate.applied:
            findings.append(_draft_finding("critical", "candidate_already_applied", "Applied candidates cannot be drafted.", None, None))
        for context in context_refs:
            target_ref = context.to_dict()
            if context.content_source == "unavailable":
                findings.append(
                    _draft_finding("warning", "target_context_unavailable", "Target context is unavailable.", target_ref, None)
                )
            if context.private_boundary_risk:
                findings.append(
                    _draft_finding("critical", "private_boundary_risk", "Target context crosses private boundary risk.", target_ref, None)
                )
            if context.redacted:
                findings.append(_draft_finding("info", "raw_content_redacted", "Raw target content is redacted.", target_ref, None))
        for anchor in anchors:
            if anchor.ambiguous:
                findings.append(
                    _draft_finding("warning", "anchor_ambiguous", "Patch anchor is ambiguous.", None, anchor.to_dict())
                )
            if anchor.anchor_type == "unknown":
                findings.append(_draft_finding("warning", "anchor_not_found", "Patch anchor is unknown.", None, anchor.to_dict()))
        if len(operations) > normalized.max_hunks:
            findings.append(_draft_finding("error", "operation_scope_exceeds_limit", "Operation count exceeds max hunks.", None, None))
        for operation in operations:
            operation_ref = operation.to_dict()
            if operation.operation_type not in self.patch_policy.allowed_patch_types:
                findings.append(
                    _draft_finding("error", "operation_type_forbidden", "Operation type is not allowed.", None, operation_ref)
                )
            if operation.added_line_count > normalized.max_added_lines:
                findings.append(_draft_finding("error", "added_lines_exceed_limit", "Added line count exceeds limit.", None, operation_ref))
            if operation.removed_line_count > normalized.max_removed_lines:
                findings.append(
                    _draft_finding("error", "removed_lines_exceed_limit", "Removed line count exceeds limit.", None, operation_ref)
                )
            if operation.operation_status == "needs_more_input":
                findings.append(_draft_finding("warning", "needs_more_input", "Operation needs more input.", None, operation_ref))
        findings.extend(
            [
                _draft_finding("info", "static_safety_not_performed", "Static safety is deferred to v0.22.3.", None, None),
                _draft_finding("info", "dry_run_not_performed", "Dry-run is not performed in v0.22.2.", None, None),
                _draft_finding("info", "apply_not_allowed", "Patch apply is not allowed in v0.22.2.", None, None),
            ]
        )
        return findings or [_draft_finding("info", "ok", "Patch draft and diff preview are preview-only.", None, None)]


class SelfModificationDiffPreviewService:
    def __init__(
        self,
        *,
        source_service: PatchDraftSourceService | None = None,
        anchor_collector: PatchAnchorCollector | None = None,
        operation_builder: PatchOperationDraftBuilder | None = None,
        preview_builder: DiffPreviewBuilder | None = None,
        finding_service: PatchDraftFindingService | None = None,
        policy_service: PatchDraftPolicyService | None = None,
    ) -> None:
        self.source_service = source_service or PatchDraftSourceService()
        self.anchor_collector = anchor_collector or PatchAnchorCollector()
        self.operation_builder = operation_builder or PatchOperationDraftBuilder()
        self.preview_builder = preview_builder or DiffPreviewBuilder()
        self.finding_service = finding_service or PatchDraftFindingService()
        self.policy_service = policy_service or PatchDraftPolicyService()

    def create_patch_draft_and_preview(self, request: PatchDraftCreateRequest) -> PatchDraftDiffPreviewResult:
        normalized = request.normalized()
        patch_candidate = self.source_service.load_patch_candidate(normalized.patch_candidate_id)
        if patch_candidate is None:
            findings = self.finding_service.evaluate(normalized, None, [], [], [])
            return self._non_preview_result(normalized, None, findings, "needs_more_input")
        context_refs = self.source_service.collect_target_context(normalized, patch_candidate)
        anchors = self.anchor_collector.collect_anchors(context_refs, normalized)
        operations = self.operation_builder.build_operations(normalized, patch_candidate, context_refs, anchors)
        findings = self.finding_service.evaluate(normalized, patch_candidate, context_refs, anchors, operations)
        decision = self.policy_service.decide(request=normalized, patch_candidate=patch_candidate, findings=findings)
        if decision != "preview_created":
            return self._non_preview_result(normalized, patch_candidate, findings, decision)
        created_at = utc_now_iso()
        draft = PatchDraft(
            draft_id=f"patch_draft:{uuid4()}",
            patch_candidate_id=patch_candidate.candidate_id,
            request_id=normalized.request_id or patch_candidate.request_id,
            created_at=created_at,
            target_context_refs=context_refs,
            anchors=anchors,
            operations=operations,
            findings=findings,
            lifecycle_state="preview_created",
            draft_status="draft_only",
            candidate_status="candidate_only",
            static_safety_checked=False,
            dry_run_checked=False,
            review_approved=False,
            apply_gate_opened=False,
            applied=False,
            file_write_enabled=False,
            apply_patch_enabled=False,
            execution_enabled=False,
            materialized=False,
            promoted=False,
        )
        preview = self.preview_builder.build_preview(draft, normalized)
        return PatchDraftDiffPreviewResult(
            patch_candidate=patch_candidate,
            draft=draft,
            diff_preview=preview,
            no_action_candidate=None,
            needs_more_input_candidate=None,
            findings=findings,
        )

    def _non_preview_result(
        self,
        request: PatchDraftCreateRequest,
        patch_candidate: PatchCandidate | None,
        findings: list[PatchDraftFinding],
        decision: str,
    ) -> PatchDraftDiffPreviewResult:
        if decision == "no_action" or decision == "blocked":
            return PatchDraftDiffPreviewResult(
                patch_candidate=patch_candidate,
                draft=None,
                diff_preview=None,
                no_action_candidate=PatchDraftNoActionCandidate(
                    candidate_id=f"patch_draft_no_action_candidate:{uuid4()}",
                    patch_candidate_id=patch_candidate.candidate_id if patch_candidate else request.patch_candidate_id,
                    reason="Patch draft is blocked or not actionable under v0.22.2 policy.",
                    evidence_refs=_finding_evidence(findings),
                    recommended_review_decision="no_action",
                    candidate_status="candidate_only",
                    applied=False,
                ),
                needs_more_input_candidate=None,
                findings=findings,
            )
        return PatchDraftDiffPreviewResult(
            patch_candidate=patch_candidate,
            draft=None,
            diff_preview=None,
            no_action_candidate=None,
            needs_more_input_candidate=PatchDraftNeedsMoreInputCandidate(
                candidate_id=f"patch_draft_needs_more_input_candidate:{uuid4()}",
                patch_candidate_id=patch_candidate.candidate_id if patch_candidate else request.patch_candidate_id,
                reason="More input is required before patch draft preview can proceed.",
                missing_inputs=_missing_inputs(findings),
                evidence_refs=_finding_evidence(findings),
                recommended_review_decision="needs_more_input",
                candidate_status="candidate_only",
                applied=False,
            ),
            findings=findings,
        )

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "report_name": "Self-Modification Patch Draft/Diff Preview PIG Report",
            "version": SELF_MODIFICATION_PATCH_DRAFT_VERSION,
            "layer": "self_modification_safety",
            "subject": "patch_draft_diff_preview",
            "principles": [
                "patch draft is not patch apply",
                "diff preview is not file mutation",
                "diff preview is not dry-run",
                "preview-created does not mean safety-checked",
            ],
            "file_write_enabled": False,
            "apply_patch_enabled": False,
            "dry_run_enabled": False,
            "static_safety_passed": False,
            "patch_apply_enabled": False,
            "llm_judge_enabled": False,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "projection_name": "Self-Modification Patch Draft/Diff Preview OCPX Projection",
            "state": SELF_MODIFICATION_PATCH_DRAFT_STATE,
            "version": SELF_MODIFICATION_PATCH_DRAFT_VERSION,
            "source_read_models": [
                "SelfModificationRequestState",
                "PatchCandidateState",
                "SelfModificationPatchPolicyState",
                "SelfModificationLifecyclePolicyState",
                "SelfRuntimeBoundaryState",
                "SelfPolicyGateState",
            ],
            "target_read_models": [
                "PatchDraftState",
                "DiffPreviewState",
                "PatchOperationDraftState",
                "PatchDraftFindingState",
            ],
            "effect_types": ["read_only_observation", "state_candidate_created"],
        }

    def render_result_cli(self, result: PatchDraftDiffPreviewResult) -> str:
        draft_id = result.draft.draft_id if result.draft else "none"
        preview_id = result.diff_preview.preview_id if result.diff_preview else "none"
        candidate_id = (
            result.patch_candidate.candidate_id
            if result.patch_candidate
            else result.needs_more_input_candidate.patch_candidate_id
            if result.needs_more_input_candidate
            else result.no_action_candidate.patch_candidate_id
            if result.no_action_candidate
            else "none"
        )
        return "\n".join(
            [
                "Self-Modification Patch Draft / Diff Preview",
                "version=v0.22.2",
                "layer=self_modification_safety",
                f"draft_id={draft_id}",
                f"preview_id={preview_id}",
                f"candidate_id={candidate_id}",
                "lifecycle_state=preview_created",
                "draft_status=draft_only",
                "preview_status=preview_only",
                "static_safety_checked=false",
                "dry_run_checked=false",
                "applies_cleanly=unknown",
                "review_approved=false",
                "apply_gate_opened=false",
                "applied=false",
                "file_write_enabled=false",
                "apply_patch_enabled=false",
                "next_required_step=v0.22.3 Patch Static Safety Check",
                "No file mutation occurred.",
                "private_full_paths_printed=False",
                "raw_full_file_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_view_cli(self, *, object_id: str, object_type: str) -> str:
        return "\n".join(
            [
                f"Self-Modification {object_type.title()} View",
                "version=v0.22.2",
                "layer=self_modification_safety",
                f"{object_type}_id={object_id}",
                "status=not_persisted_in_v0.22.2",
                "lifecycle_state=preview_created",
                "static_safety_checked=false",
                "dry_run_checked=false",
                "applies_cleanly=unknown",
                "applied=false",
                "file_write_enabled=false",
                "apply_patch_enabled=false",
                "next_required_step=v0.22.3 Patch Static Safety Check",
                "No file mutation occurred.",
                "private_full_paths_printed=False",
                "raw_full_file_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_findings_cli(self, *, preview_id: str) -> str:
        return "\n".join(
            [
                "Self-Modification Diff Preview Findings",
                "version=v0.22.2",
                "layer=self_modification_safety",
                f"preview_id={preview_id}",
                "finding_types=static_safety_not_performed,dry_run_not_performed,apply_not_allowed",
                "static_safety_checked=false",
                "dry_run_checked=false",
                "applied=false",
                "file_write_enabled=false",
                "apply_patch_enabled=false",
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
                "Self-Modification Patch Draft/Diff Preview PIG Report",
                "version=v0.22.2",
                "layer=self_modification_safety",
                f"subject={report['subject']}",
                f"principles={','.join(report['principles'])}",
                f"file_write_enabled={str(report['file_write_enabled']).lower()}",
                f"apply_patch_enabled={str(report['apply_patch_enabled']).lower()}",
                f"dry_run_enabled={str(report['dry_run_enabled']).lower()}",
                f"static_safety_passed={str(report['static_safety_passed']).lower()}",
                f"patch_apply_enabled={str(report['patch_apply_enabled']).lower()}",
                f"llm_judge_enabled={str(report['llm_judge_enabled']).lower()}",
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
                "Self-Modification Patch Draft/Diff Preview OCPX Projection",
                "version=v0.22.2",
                "layer=self_modification_safety",
                f"state={projection['state']}",
                f"source_read_models={','.join(projection['source_read_models'])}",
                f"target_read_models={','.join(projection['target_read_models'])}",
                f"effect_types={','.join(projection['effect_types'])}",
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


def _draft_finding(
    severity: str,
    finding_type: str,
    message: str,
    target_ref: dict[str, Any] | None,
    operation_ref: dict[str, Any] | None,
) -> PatchDraftFinding:
    return PatchDraftFinding(
        finding_id=f"patch_draft_finding:{uuid4()}",
        severity=severity,
        finding_type=finding_type,
        message=message,
        target_ref=target_ref,
        operation_ref=operation_ref,
        evidence_refs=[{"ref_type": "self_modification_patch_draft_policy", "version": "v0.22.2"}],
        withdrawal_condition=(
            "Withdraw if v0.22.2 writes files, applies patches, performs dry-run, or opens an apply gate."
        ),
    )


def _synthetic_patch_candidate(patch_candidate_id: str) -> PatchCandidate:
    target = ModificationTargetRef(
        target_id=f"modification_target_ref:{uuid4()}",
        target_type="workspace_file",
        root_id="workspace",
        relative_path="README.md",
        path_status="verified",
        file_kind="docs",
        current_state_ref={"ref_type": "workspace_path_metadata", "relative_path": "README.md"},
        private_boundary_risk=False,
        secret_file_risk=False,
        generated_file_risk=False,
        evidence_refs=[{"ref_type": "cli_synthetic_candidate_target", "version": "v0.22.2"}],
    )
    intent = PatchIntentDescriptor(
        intent_id=f"patch_intent:{uuid4()}",
        goal_text="CLI preview request",
        intent_type="docs",
        requested_patch_type="comment_only_change",
        allowed_patch_type_candidate="comment_only_change",
        forbidden_patch_type_detected=False,
        requires_file_content=False,
        requires_diff_generation=True,
        requires_operator_clarification=False,
        notes=["Synthetic CLI candidate for read-only preview rendering."],
    )
    scope = PatchScopeDescriptor(
        scope_id=f"patch_scope:{uuid4()}",
        target_count=1,
        max_target_files=1,
        target_refs=[target],
        scope_status="ok",
        scope_risk_reasons=[],
    )
    return PatchCandidate(
        candidate_id=patch_candidate_id,
        request_id=f"self_modification_request:{uuid4()}",
        created_at=utc_now_iso(),
        title="Synthetic candidate-only preview",
        goal_text="CLI preview request",
        target_refs=[target],
        intent=intent,
        scope=scope,
        constraints=[
            PatchConstraintDescriptor(
                constraint_id="constraint:no_file_write_in_v0_22_2",
                constraint_type="safety_boundary",
                description="File mutation is not allowed in v0.22.2.",
                severity="hard_block",
                source_ref={"ref_type": "self_modification_safety_contract", "version": "v0.22.0"},
            )
        ],
        preliminary_risk=PatchPreliminaryRiskAssessment(
            risk_id=f"patch_preliminary_risk:{uuid4()}",
            risk_level="low",
            target_risks=[],
            policy_risks=[],
            boundary_risks=[],
            forbidden_patch_risks=[],
            requires_review=True,
            safe_to_generate_diff=False,
            safe_to_apply=False,
        ),
        findings=[
            PatchCandidateFinding(
                finding_id=f"patch_candidate_finding:{uuid4()}",
                severity="info",
                finding_type="diff_generation_deferred",
                message="Diff preview is rendered as sanitized v0.22.2 artifact.",
                target_ref=target.to_dict(),
                evidence_refs=[{"ref_type": "cli_synthetic_candidate", "version": "v0.22.2"}],
                withdrawal_condition="Withdraw if CLI preview writes files or applies patches.",
            )
        ],
        evidence_refs=[{"ref_type": "cli_synthetic_candidate", "version": "v0.22.2"}],
    )


def _target_from_dict(raw: dict[str, Any]) -> ModificationTargetRef:
    return ModificationTargetRef(
        target_id=str(raw.get("target_id") or f"modification_target_ref:{uuid4()}"),
        target_type=str(raw.get("target_type") or "unknown"),
        root_id=str(raw.get("root_id")) if raw.get("root_id") else None,
        relative_path=str(raw.get("relative_path")) if raw.get("relative_path") else None,
        path_status=str(raw.get("path_status") or "unknown"),
        file_kind=str(raw.get("file_kind")) if raw.get("file_kind") else None,
        current_state_ref=dict(raw.get("current_state_ref")) if isinstance(raw.get("current_state_ref"), dict) else None,
        private_boundary_risk=bool(raw.get("private_boundary_risk", False)),
        secret_file_risk=bool(raw.get("secret_file_risk", False)),
        generated_file_risk=bool(raw.get("generated_file_risk", False)),
        evidence_refs=[dict(item) for item in raw.get("evidence_refs", []) if isinstance(item, dict)],
    )


def _hint_for_target(hints: list[dict[str, Any]], target: ModificationTargetRef) -> dict[str, Any]:
    for hint in hints:
        if hint.get("target_id") == target.target_id or hint.get("relative_path") == target.relative_path:
            return dict(hint)
    return dict(hints[0]) if hints else {}


def _hint_for_context(hints: list[dict[str, Any]], context: PatchTargetContextRef) -> dict[str, Any]:
    for hint in hints:
        if hint.get("target_id") == context.target_id or hint.get("relative_path") == context.relative_path:
            return dict(hint)
    return dict(hints[0]) if hints else {}


def _anchor_for_context(anchors: list[PatchAnchorRef], context: PatchTargetContextRef) -> PatchAnchorRef | None:
    for anchor in anchors:
        if anchor.target_id == context.target_id:
            return anchor
    return None


def _optional_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _sanitize_dict(raw: dict[str, Any]) -> dict[str, Any]:
    return {str(key): _sanitize_text(value, limit=320) if isinstance(value, str) else value for key, value in raw.items()}


def _sanitize_text(value: Any, *, limit: int) -> str | None:
    if value is None:
        return None
    text = str(value).replace("\r", "\n")
    text = text.replace("\x00", "")
    text = "\n".join(line[:limit] for line in text.splitlines()[:12])
    if len(text) > limit:
        text = text[:limit]
    return text


def _line_count(value: str | None) -> int:
    if not value:
        return 0
    return max(1, len(value.splitlines()))


def _bounded_lines(value: str | None, limit: int) -> list[str]:
    if not value or limit <= 0:
        return []
    return [_sanitize_text(line, limit=160) or "" for line in value.splitlines()[:limit]]


def _default_new_preview(index: int) -> str:
    return f"# preview-only candidate change {index + 1}"


def _render_sanitized_preview(hunks: list[DiffHunkPreview], preview_format: str) -> str | None:
    if preview_format == "structured":
        return f"structured_hunk_count={len(hunks)}"
    if preview_format == "summary":
        return f"diff_preview_hunks={len(hunks)}; applied=false"
    lines: list[str] = []
    for hunk in hunks:
        path = hunk.relative_path or "unknown"
        lines.extend([f"--- a/{path}", f"+++ b/{path}", "@@ sanitized preview @@" ])
        lines.extend(f" {line}" for line in hunk.context_lines_preview)
        lines.extend(f"-{line}" for line in hunk.removed_lines_preview)
        lines.extend(f"+{line}" for line in hunk.added_lines_preview)
    return "\n".join(lines) if lines else None


def _finding_evidence(findings: list[PatchDraftFinding]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for finding in findings:
        refs.append({"ref_type": "patch_draft_finding", "finding_type": finding.finding_type})
    return refs


def _missing_inputs(findings: list[PatchDraftFinding]) -> list[str]:
    mapping = {
        "missing_patch_candidate": "existing_patch_candidate",
        "target_context_unavailable": "sanitized_target_context",
        "anchor_ambiguous": "unambiguous_patch_anchor",
        "anchor_not_found": "patch_anchor",
        "needs_more_input": "operation_detail",
    }
    missing = [mapping[item.finding_type] for item in findings if item.finding_type in mapping]
    return _unique(missing) or ["operator_clarification"]


def _unique(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
