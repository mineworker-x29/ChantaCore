from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.self_modification_safety.candidate import PatchCandidate
from chanta_core.self_modification_safety.draft import (
    DiffPreviewArtifact,
    PatchDraft,
    PatchDraftCreateRequest,
    PatchDraftSourceService,
    SelfModificationDiffPreviewService,
)
from chanta_core.self_modification_safety.models import (
    SelfModificationAllowedPatchPolicy,
    SelfModificationLifecyclePolicy,
)
from chanta_core.self_modification_safety.registry import SelfModificationRegistryService
from chanta_core.utility.time import utc_now_iso


SELF_MODIFICATION_STATIC_SAFETY_VERSION = "v0.22.3"
SELF_MODIFICATION_STATIC_SAFETY_STATE = "self_modification_patch_static_safety_checked"
STATIC_SAFETY_CHECK_SKILL_ID = "skill:self_modification_static_safety_check"
STATIC_SAFETY_REPORT_SKILL_ID = "skill:self_modification_static_safety_report"


@dataclass(frozen=True)
class PatchStaticSafetyCheckRequest:
    patch_candidate_id: str | None = None
    draft_id: str | None = None
    preview_id: str | None = None
    include_path_safety: bool = True
    include_operation_safety: bool = True
    include_scope_safety: bool = True
    include_content_pattern_safety: bool = True
    include_secret_private_safety: bool = True
    include_lifecycle_safety: bool = True
    include_policy_consistency: bool = True
    strictness: str = "standard"
    max_findings: int = 300

    def normalized(self) -> "PatchStaticSafetyCheckRequest":
        return PatchStaticSafetyCheckRequest(
            patch_candidate_id=str(self.patch_candidate_id).strip() if self.patch_candidate_id else None,
            draft_id=str(self.draft_id).strip() if self.draft_id else None,
            preview_id=str(self.preview_id).strip() if self.preview_id else None,
            include_path_safety=bool(self.include_path_safety),
            include_operation_safety=bool(self.include_operation_safety),
            include_scope_safety=bool(self.include_scope_safety),
            include_content_pattern_safety=bool(self.include_content_pattern_safety),
            include_secret_private_safety=bool(self.include_secret_private_safety),
            include_lifecycle_safety=bool(self.include_lifecycle_safety),
            include_policy_consistency=bool(self.include_policy_consistency),
            strictness=self.strictness or "standard",
            max_findings=max(1, int(self.max_findings)),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "patch_candidate_id": self.patch_candidate_id,
            "draft_id": self.draft_id,
            "preview_id": self.preview_id,
            "include_path_safety": self.include_path_safety,
            "include_operation_safety": self.include_operation_safety,
            "include_scope_safety": self.include_scope_safety,
            "include_content_pattern_safety": self.include_content_pattern_safety,
            "include_secret_private_safety": self.include_secret_private_safety,
            "include_lifecycle_safety": self.include_lifecycle_safety,
            "include_policy_consistency": self.include_policy_consistency,
            "strictness": self.strictness,
            "max_findings": self.max_findings,
        }


@dataclass(frozen=True)
class PatchStaticSafetyRule:
    rule_id: str
    rule_name: str
    category: str
    severity_if_failed: str
    description: str
    enabled: bool = True
    source_policy_ref: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "category": self.category,
            "severity_if_failed": self.severity_if_failed,
            "description": self.description,
            "enabled": self.enabled,
            "source_policy_ref": dict(self.source_policy_ref) if self.source_policy_ref else None,
        }


@dataclass(frozen=True)
class PatchStaticSafetyRuleResult:
    result_id: str
    rule_id: str
    passed: bool
    severity: str
    message: str
    target_ref: dict[str, Any] | None
    operation_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "rule_id": self.rule_id,
            "passed": self.passed,
            "severity": self.severity,
            "message": self.message,
            "target_ref": dict(self.target_ref) if self.target_ref else None,
            "operation_ref": dict(self.operation_ref) if self.operation_ref else None,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class PatchStaticSafetyFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    target_ref: dict[str, Any] | None
    operation_ref: dict[str, Any] | None
    rule_ref: dict[str, Any] | None
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
            "rule_ref": dict(self.rule_ref) if self.rule_ref else None,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "withdrawal_condition": self.withdrawal_condition,
        }


@dataclass(frozen=True)
class PatchStaticSafetyCategoryResult:
    category_id: str
    category: str
    checked_rule_count: int
    passed_rule_count: int
    warning_count: int
    error_count: int
    critical_count: int
    category_status: str
    findings: list[PatchStaticSafetyFinding]

    def to_dict(self) -> dict[str, Any]:
        return {
            "category_id": self.category_id,
            "category": self.category,
            "checked_rule_count": self.checked_rule_count,
            "passed_rule_count": self.passed_rule_count,
            "warning_count": self.warning_count,
            "error_count": self.error_count,
            "critical_count": self.critical_count,
            "category_status": self.category_status,
            "findings": [item.to_dict() for item in self.findings],
        }


@dataclass(frozen=True)
class PatchStaticSafetyReport:
    report_id: str
    created_at: str
    request: PatchStaticSafetyCheckRequest
    patch_candidate_id: str | None
    draft_id: str | None
    preview_id: str | None
    rule_results: list[PatchStaticSafetyRuleResult]
    category_results: list[PatchStaticSafetyCategoryResult]
    findings: list[PatchStaticSafetyFinding]
    checked_rule_count: int
    passed_rule_count: int
    warning_count: int
    error_count: int
    critical_count: int
    static_safety_status: str
    eligible_for_dry_run: bool
    safe_to_apply: bool = False
    dry_run_required: bool = True
    human_review_required: bool = True
    apply_gate_required: bool = True
    rollback_plan_required: bool = True
    post_apply_verification_required: bool = True
    review_status: str = "report_only"
    file_write_enabled: bool = False
    apply_patch_enabled: bool = False
    dry_run_executed: bool = False
    applied: bool = False
    workspace_file_changed_emitted: bool = False
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until patch draft, diff preview, policy, or target context changes."

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "created_at": self.created_at,
            "request": self.request.to_dict(),
            "patch_candidate_id": self.patch_candidate_id,
            "draft_id": self.draft_id,
            "preview_id": self.preview_id,
            "rule_results": [item.to_dict() for item in self.rule_results],
            "category_results": [item.to_dict() for item in self.category_results],
            "findings": [item.to_dict() for item in self.findings],
            "checked_rule_count": self.checked_rule_count,
            "passed_rule_count": self.passed_rule_count,
            "warning_count": self.warning_count,
            "error_count": self.error_count,
            "critical_count": self.critical_count,
            "static_safety_status": self.static_safety_status,
            "eligible_for_dry_run": self.eligible_for_dry_run,
            "safe_to_apply": self.safe_to_apply,
            "dry_run_required": self.dry_run_required,
            "human_review_required": self.human_review_required,
            "apply_gate_required": self.apply_gate_required,
            "rollback_plan_required": self.rollback_plan_required,
            "post_apply_verification_required": self.post_apply_verification_required,
            "review_status": self.review_status,
            "file_write_enabled": self.file_write_enabled,
            "apply_patch_enabled": self.apply_patch_enabled,
            "dry_run_executed": self.dry_run_executed,
            "applied": self.applied,
            "workspace_file_changed_emitted": self.workspace_file_changed_emitted,
            "limitations": list(self.limitations),
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "validity_horizon": self.validity_horizon,
        }


@dataclass(frozen=True)
class PatchStaticSafetyNoActionCandidate:
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
class PatchStaticSafetyNeedsMoreInputCandidate:
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
class PatchStaticSafetyResult:
    report: PatchStaticSafetyReport
    no_action_candidate: PatchStaticSafetyNoActionCandidate | None
    needs_more_input_candidate: PatchStaticSafetyNeedsMoreInputCandidate | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "report": self.report.to_dict(),
            "no_action_candidate": self.no_action_candidate.to_dict() if self.no_action_candidate else None,
            "needs_more_input_candidate": self.needs_more_input_candidate.to_dict()
            if self.needs_more_input_candidate
            else None,
        }


class PatchStaticSafetySourceService:
    def __init__(
        self,
        *,
        patch_candidates: dict[str, PatchCandidate] | None = None,
        patch_drafts: dict[str, PatchDraft] | None = None,
        diff_previews: dict[str, DiffPreviewArtifact] | None = None,
        allow_synthetic: bool = False,
        registry_service: SelfModificationRegistryService | None = None,
    ) -> None:
        self.patch_candidates = dict(patch_candidates or {})
        self.patch_drafts = dict(patch_drafts or {})
        self.diff_previews = dict(diff_previews or {})
        self.allow_synthetic = allow_synthetic
        self.registry_service = registry_service or SelfModificationRegistryService()
        if self.allow_synthetic:
            self._ensure_synthetic_bundle()

    def load_patch_candidate(self, patch_candidate_id: str | None) -> PatchCandidate | None:
        if patch_candidate_id is None:
            return next(iter(self.patch_candidates.values()), None)
        candidate = self.patch_candidates.get(patch_candidate_id)
        if candidate is None and self.allow_synthetic:
            return next(iter(self.patch_candidates.values()), None)
        return candidate

    def load_patch_draft(self, draft_id: str | None) -> PatchDraft | None:
        if draft_id is None:
            return next(iter(self.patch_drafts.values()), None)
        draft = self.patch_drafts.get(draft_id)
        if draft is None and self.allow_synthetic:
            return next(iter(self.patch_drafts.values()), None)
        return draft

    def load_diff_preview(self, preview_id: str | None) -> DiffPreviewArtifact | None:
        if preview_id is None:
            return next(iter(self.diff_previews.values()), None)
        preview = self.diff_previews.get(preview_id)
        if preview is None and self.allow_synthetic:
            return next(iter(self.diff_previews.values()), None)
        return preview

    def load_patch_policy(self) -> SelfModificationAllowedPatchPolicy:
        return self.registry_service.build_contract().allowed_patch_policy

    def load_lifecycle_policy(self) -> SelfModificationLifecyclePolicy:
        return self.registry_service.build_lifecycle_policy()

    def _ensure_synthetic_bundle(self) -> None:
        if self.patch_drafts and self.diff_previews:
            return
        preview_service = SelfModificationDiffPreviewService(source_service=PatchDraftSourceService(allow_synthetic=True))
        result = preview_service.create_patch_draft_and_preview(
            PatchDraftCreateRequest(
                patch_candidate_id="patch_candidate:cli_static_safety",
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
        if result.patch_candidate:
            self.patch_candidates[result.patch_candidate.candidate_id] = result.patch_candidate
        if result.draft:
            self.patch_drafts[result.draft.draft_id] = result.draft
        if result.diff_preview:
            self.diff_previews[result.diff_preview.preview_id] = result.diff_preview


class PatchStaticRuleRegistry:
    def list_rules(self) -> list[PatchStaticSafetyRule]:
        return [
            _rule("path_workspace_relative", "Workspace-relative path", "path", "error"),
            _rule("path_private_risk", "Private path risk", "path", "critical"),
            _rule("secret_private_secret_file", "Secret file risk", "secret_private", "critical"),
            _rule("secret_private_binary_file", "Binary file risk", "secret_private", "critical"),
            _rule("secret_private_generated_file", "Generated file risk", "secret_private", "warning"),
            _rule("operation_allowed_type", "Allowed operation type", "operation", "error"),
            _rule("scope_hunk_limit", "Hunk count limit", "scope", "error"),
            _rule("scope_added_line_limit", "Added line limit", "scope", "error"),
            _rule("scope_removed_line_limit", "Removed line limit", "scope", "error"),
            _rule("content_dangerous_pattern", "Dangerous content pattern", "content_pattern", "error"),
            _rule("content_permission_pattern", "Permission grant pattern", "content_pattern", "error"),
            _rule("content_shell_network_pattern", "Shell/network/MCP/plugin pattern", "content_pattern", "error"),
            _rule("lifecycle_preview_created", "Preview-created lifecycle", "lifecycle", "error"),
            _rule("lifecycle_not_applied", "Not applied", "lifecycle", "critical"),
            _rule("lifecycle_no_write_apply_flags", "Write/apply flags disabled", "lifecycle", "critical"),
            _rule("lifecycle_dry_run_visible", "Dry-run not performed is visible", "lifecycle", "info"),
            _rule("lifecycle_review_visible", "Review not approved is visible", "lifecycle", "info"),
            _rule("lifecycle_apply_gate_visible", "Apply gate not opened is visible", "lifecycle", "info"),
            _rule("policy_draft_preview_present", "Draft and preview are present", "policy", "critical"),
            _rule("policy_not_safe_to_apply", "Static report is not safe-to-apply", "policy", "critical"),
        ]


class PatchPathSafetyVerifier:
    def verify(
        self,
        draft: PatchDraft | None,
        preview: DiffPreviewArtifact | None,
        rules: list[PatchStaticSafetyRule],
    ) -> list[PatchStaticSafetyRuleResult]:
        _ = preview
        results: list[PatchStaticSafetyRuleResult] = []
        if draft is None:
            return [_result(_find_rule(rules, "path_workspace_relative"), False, "blocked", "missing_patch_draft", None, None)]
        for context in draft.target_context_refs:
            target_ref = context.to_dict()
            relative_path = context.relative_path or ""
            workspace_relative = bool(relative_path) and not _is_non_workspace_path(relative_path)
            results.append(
                _result(
                    _find_rule(rules, "path_workspace_relative"),
                    workspace_relative,
                    "Path is workspace-relative." if workspace_relative else "Path is not workspace-relative.",
                    "path_not_workspace_relative",
                    target_ref,
                    None,
                )
            )
            results.append(
                _result(
                    _find_rule(rules, "path_private_risk"),
                    not context.private_boundary_risk,
                    "No private path risk." if not context.private_boundary_risk else "Private path risk detected.",
                    "private_path_risk",
                    target_ref,
                    None,
                )
            )
        return results


class PatchOperationSafetyVerifier:
    def verify(
        self,
        draft: PatchDraft | None,
        policy: SelfModificationAllowedPatchPolicy,
        rules: list[PatchStaticSafetyRule],
    ) -> list[PatchStaticSafetyRuleResult]:
        if draft is None:
            return [_result(_find_rule(rules, "operation_allowed_type"), False, "blocked", "missing_patch_draft", None, None)]
        results: list[PatchStaticSafetyRuleResult] = []
        for operation in draft.operations:
            operation_ref = operation.to_dict()
            allowed = operation.operation_type in policy.allowed_patch_types
            results.append(
                _result(
                    _find_rule(rules, "operation_allowed_type"),
                    allowed,
                    "Operation type is allowed." if allowed else "Forbidden operation type detected.",
                    "forbidden_operation_type",
                    operation.target_ref,
                    operation_ref,
                )
            )
        return results


class PatchScopeSafetyVerifier:
    def verify(
        self,
        draft: PatchDraft | None,
        preview: DiffPreviewArtifact | None,
        policy: SelfModificationAllowedPatchPolicy,
        rules: list[PatchStaticSafetyRule],
    ) -> list[PatchStaticSafetyRuleResult]:
        if draft is None or preview is None:
            return [_result(_find_rule(rules, "scope_hunk_limit"), False, "blocked", "missing_diff_preview", None, None)]
        hunk_count_ok = len(preview.hunk_previews) <= policy.max_hunks_per_file
        results = [
            _result(
                _find_rule(rules, "scope_hunk_limit"),
                hunk_count_ok,
                "Hunk count is within limit." if hunk_count_ok else "Hunk count exceeds limit.",
                "hunk_count_exceeds_limit",
                None,
                None,
            )
        ]
        for operation in draft.operations:
            operation_ref = operation.to_dict()
            added_ok = operation.added_line_count <= policy.max_added_lines
            removed_ok = operation.removed_line_count <= policy.max_removed_lines
            results.append(
                _result(
                    _find_rule(rules, "scope_added_line_limit"),
                    added_ok,
                    "Added lines are within limit." if added_ok else "Added lines exceed limit.",
                    "added_lines_exceed_limit",
                    operation.target_ref,
                    operation_ref,
                )
            )
            results.append(
                _result(
                    _find_rule(rules, "scope_removed_line_limit"),
                    removed_ok,
                    "Removed lines are within limit." if removed_ok else "Removed lines exceed limit.",
                    "removed_lines_exceed_limit",
                    operation.target_ref,
                    operation_ref,
                )
            )
        return results


class PatchContentPatternSafetyVerifier:
    def verify(
        self,
        draft: PatchDraft | None,
        preview: DiffPreviewArtifact | None,
        rules: list[PatchStaticSafetyRule],
    ) -> list[PatchStaticSafetyRuleResult]:
        if draft is None or preview is None:
            return [_result(_find_rule(rules, "content_dangerous_pattern"), False, "blocked", "missing_diff_preview", None, None)]
        text = _operation_preview_text(draft, preview)
        dangerous = _contains_any(
            text,
            ["ev" + "al(", "ex" + "ec(", "dangerous_capability", "file_write_enabled" + "=True"],
        )
        permission = _contains_any(
            text,
            ["permission_grant", "grants_permission" + "=True", "approve_without_review"],
        )
        shell_network = _contains_any(
            text,
            [
                "os." + "system",
                "sub" + "process",
                "req" + "uests.",
                "ht" + "tpx.",
                "mcp." + "connect",
                "plugin." + "load",
            ],
        )
        return [
            _result(
                _find_rule(rules, "content_dangerous_pattern"),
                not dangerous,
                "No dangerous pattern detected." if not dangerous else "Dangerous pattern detected.",
                "dangerous_pattern_detected",
                None,
                None,
            ),
            _result(
                _find_rule(rules, "content_permission_pattern"),
                not permission,
                "No permission grant pattern detected." if not permission else "Permission grant pattern detected.",
                "permission_grant_pattern_detected",
                None,
                None,
            ),
            _result(
                _find_rule(rules, "content_shell_network_pattern"),
                not shell_network,
                "No shell/network/MCP/plugin pattern detected."
                if not shell_network
                else "Shell/network/MCP/plugin pattern detected.",
                "shell_network_mcp_plugin_pattern_detected",
                None,
                None,
            ),
        ]


class PatchSecretPrivateSafetyVerifier:
    def verify(self, draft: PatchDraft | None, rules: list[PatchStaticSafetyRule]) -> list[PatchStaticSafetyRuleResult]:
        if draft is None:
            return [_result(_find_rule(rules, "secret_private_secret_file"), False, "blocked", "missing_patch_draft", None, None)]
        results: list[PatchStaticSafetyRuleResult] = []
        for context in draft.target_context_refs:
            target_ref = context.to_dict()
            path = context.relative_path or ""
            secret = _looks_secret(path)
            binary = _looks_binary(path)
            generated = _looks_generated(path)
            results.append(
                _result(
                    _find_rule(rules, "secret_private_secret_file"),
                    not secret,
                    "No secret file risk." if not secret else "Secret file risk detected.",
                    "secret_file_risk",
                    target_ref,
                    None,
                )
            )
            results.append(
                _result(
                    _find_rule(rules, "secret_private_binary_file"),
                    not binary,
                    "No binary file risk." if not binary else "Binary file risk detected.",
                    "binary_file_risk",
                    target_ref,
                    None,
                )
            )
            results.append(
                _result(
                    _find_rule(rules, "secret_private_generated_file"),
                    not generated,
                    "No generated file risk." if not generated else "Generated file risk detected.",
                    "generated_file_risk",
                    target_ref,
                    None,
                )
            )
        return results


class PatchLifecycleSafetyVerifier:
    def verify(
        self,
        candidate: PatchCandidate | None,
        draft: PatchDraft | None,
        preview: DiffPreviewArtifact | None,
        lifecycle_policy: SelfModificationLifecyclePolicy,
        rules: list[PatchStaticSafetyRule],
    ) -> list[PatchStaticSafetyRuleResult]:
        _ = lifecycle_policy
        if draft is None or preview is None:
            return [_result(_find_rule(rules, "lifecycle_preview_created"), False, "blocked", "missing_diff_preview", None, None)]
        preview_created = draft.lifecycle_state == "preview_created" and preview.lifecycle_state == "preview_created"
        applied = bool(
            draft.applied
            or preview.applied
            or (candidate.applied if candidate is not None else False)
            or any(operation.applied for operation in draft.operations)
        )
        write_apply_flag = bool(
            draft.file_write_enabled
            or draft.apply_patch_enabled
            or preview.file_write_enabled
            or preview.apply_patch_enabled
            or any(operation.file_write_enabled or operation.apply_patch_enabled for operation in draft.operations)
        )
        return [
            _result(
                _find_rule(rules, "lifecycle_preview_created"),
                preview_created,
                "Lifecycle is preview_created." if preview_created else "Lifecycle is inconsistent.",
                "missing_diff_preview",
                None,
                None,
            ),
            _result(
                _find_rule(rules, "lifecycle_not_applied"),
                not applied,
                "Patch is not applied." if not applied else "Applied state detected.",
                "draft_already_applied",
                None,
                None,
            ),
            _result(
                _find_rule(rules, "lifecycle_no_write_apply_flags"),
                not write_apply_flag,
                "Write/apply flags are disabled." if not write_apply_flag else "Mutation or apply flag is enabled.",
                "mutation_flag_enabled" if draft.file_write_enabled or preview.file_write_enabled else "apply_flag_enabled",
                None,
                None,
            ),
            _result(_find_rule(rules, "lifecycle_dry_run_visible"), True, "Dry-run not performed.", "dry_run_not_performed", None, None),
            _result(_find_rule(rules, "lifecycle_review_visible"), True, "Review is not approved.", "review_not_approved", None, None),
            _result(
                _find_rule(rules, "lifecycle_apply_gate_visible"),
                True,
                "Apply gate is not opened.",
                "apply_gate_not_opened",
                None,
                None,
            ),
        ]


class PatchPolicyConsistencyVerifier:
    def verify(
        self,
        draft: PatchDraft | None,
        preview: DiffPreviewArtifact | None,
        rules: list[PatchStaticSafetyRule],
    ) -> list[PatchStaticSafetyRuleResult]:
        return [
            _result(
                _find_rule(rules, "policy_draft_preview_present"),
                draft is not None and preview is not None,
                "Patch draft and diff preview are present."
                if draft is not None and preview is not None
                else "Patch draft or diff preview is missing.",
                "missing_patch_draft" if draft is None else "missing_diff_preview",
                None,
                None,
            ),
            _result(
                _find_rule(rules, "policy_not_safe_to_apply"),
                True,
                "Static safety report is not safe-to-apply.",
                "ok",
                None,
                None,
            ),
        ]


class PatchStaticSafetyFindingService:
    def build_findings(self, rule_results: list[PatchStaticSafetyRuleResult]) -> list[PatchStaticSafetyFinding]:
        findings: list[PatchStaticSafetyFinding] = []
        for result in rule_results:
            finding_type = _finding_type_from_result(result)
            if result.passed and finding_type not in {
                "dry_run_not_performed",
                "review_not_approved",
                "apply_gate_not_opened",
                "ok",
            }:
                continue
            findings.append(
                PatchStaticSafetyFinding(
                    finding_id=f"patch_static_safety_finding:{uuid4()}",
                    severity=result.severity,
                    finding_type=finding_type,
                    message=result.message,
                    target_ref=result.target_ref,
                    operation_ref=result.operation_ref,
                    rule_ref={"rule_id": result.rule_id},
                    evidence_refs=[dict(item) for item in result.evidence_refs],
                    withdrawal_condition=(
                        "Withdraw if v0.22.3 writes files, applies patches, runs dry-run, approves review, "
                        "opens an apply gate, or marks safe_to_apply true."
                    ),
                )
            )
        return findings or [
            PatchStaticSafetyFinding(
                finding_id=f"patch_static_safety_finding:{uuid4()}",
                severity="info",
                finding_type="ok",
                message="Static safety check passed without warning findings.",
                target_ref=None,
                operation_ref=None,
                rule_ref=None,
                evidence_refs=[{"ref_type": "patch_static_safety_report", "version": SELF_MODIFICATION_STATIC_SAFETY_VERSION}],
                withdrawal_condition="Withdraw if static safety becomes approval or patch application.",
            )
        ]


class PatchStaticSafetyReportService:
    def __init__(
        self,
        *,
        source_service: PatchStaticSafetySourceService | None = None,
        rule_registry: PatchStaticRuleRegistry | None = None,
        finding_service: PatchStaticSafetyFindingService | None = None,
    ) -> None:
        self.source_service = source_service or PatchStaticSafetySourceService()
        self.rule_registry = rule_registry or PatchStaticRuleRegistry()
        self.finding_service = finding_service or PatchStaticSafetyFindingService()
        self.path_verifier = PatchPathSafetyVerifier()
        self.operation_verifier = PatchOperationSafetyVerifier()
        self.scope_verifier = PatchScopeSafetyVerifier()
        self.content_verifier = PatchContentPatternSafetyVerifier()
        self.secret_verifier = PatchSecretPrivateSafetyVerifier()
        self.lifecycle_verifier = PatchLifecycleSafetyVerifier()
        self.policy_verifier = PatchPolicyConsistencyVerifier()

    def build_report(self, request: PatchStaticSafetyCheckRequest) -> PatchStaticSafetyReport:
        normalized = request.normalized()
        candidate = self.source_service.load_patch_candidate(normalized.patch_candidate_id)
        draft = self.source_service.load_patch_draft(normalized.draft_id)
        preview = self.source_service.load_diff_preview(normalized.preview_id)
        policy = self.source_service.load_patch_policy()
        lifecycle = self.source_service.load_lifecycle_policy()
        rules = self.rule_registry.list_rules()
        rule_results: list[PatchStaticSafetyRuleResult] = []
        if normalized.include_path_safety:
            rule_results.extend(self.path_verifier.verify(draft, preview, _rules_for(rules, "path")))
        if normalized.include_secret_private_safety:
            rule_results.extend(self.secret_verifier.verify(draft, _rules_for(rules, "secret_private")))
        if normalized.include_operation_safety:
            rule_results.extend(self.operation_verifier.verify(draft, policy, _rules_for(rules, "operation")))
        if normalized.include_scope_safety:
            rule_results.extend(self.scope_verifier.verify(draft, preview, policy, _rules_for(rules, "scope")))
        if normalized.include_content_pattern_safety:
            rule_results.extend(self.content_verifier.verify(draft, preview, _rules_for(rules, "content_pattern")))
        if normalized.include_lifecycle_safety:
            rule_results.extend(self.lifecycle_verifier.verify(candidate, draft, preview, lifecycle, _rules_for(rules, "lifecycle")))
        if normalized.include_policy_consistency:
            rule_results.extend(self.policy_verifier.verify(draft, preview, _rules_for(rules, "policy")))
        findings = self.finding_service.build_findings(rule_results)[: normalized.max_findings]
        category_results = _category_results(rule_results, findings, rules)
        warning_count = sum(1 for finding in findings if finding.severity == "warning")
        error_count = sum(1 for finding in findings if finding.severity == "error")
        critical_count = sum(1 for finding in findings if finding.severity == "critical")
        status = _status_from_findings(findings)
        eligible = status in {"passed", "warning"}
        return PatchStaticSafetyReport(
            report_id=f"patch_static_safety_report:{uuid4()}",
            created_at=utc_now_iso(),
            request=normalized,
            patch_candidate_id=candidate.candidate_id if candidate else normalized.patch_candidate_id,
            draft_id=draft.draft_id if draft else normalized.draft_id,
            preview_id=preview.preview_id if preview else normalized.preview_id,
            rule_results=rule_results,
            category_results=category_results,
            findings=findings,
            checked_rule_count=len(rule_results),
            passed_rule_count=sum(1 for result in rule_results if result.passed),
            warning_count=warning_count,
            error_count=error_count,
            critical_count=critical_count,
            static_safety_status=status,
            eligible_for_dry_run=eligible,
            safe_to_apply=False,
            dry_run_required=True,
            human_review_required=True,
            apply_gate_required=True,
            rollback_plan_required=True,
            post_apply_verification_required=True,
            review_status="report_only",
            file_write_enabled=False,
            apply_patch_enabled=False,
            dry_run_executed=False,
            applied=False,
            workspace_file_changed_emitted=False,
            limitations=[
                "Static safety is not dry-run.",
                "Static safety report is not approval.",
                "Static safety does not prove clean application.",
            ],
            withdrawal_conditions=[
                "Withdraw if file write or patch application occurs.",
                "Withdraw if dry-run, review approval, or apply gate opening occurs.",
                "Withdraw if safe_to_apply becomes true in v0.22.3.",
            ],
        )


class SelfModificationStaticSafetyService:
    def __init__(self, *, report_service: PatchStaticSafetyReportService | None = None) -> None:
        self.report_service = report_service or PatchStaticSafetyReportService()

    def check_static_safety(self, request: PatchStaticSafetyCheckRequest) -> PatchStaticSafetyResult:
        report = self.report_service.build_report(request)
        no_action = None
        needs_more_input = None
        if report.static_safety_status in {"failed", "blocked"}:
            no_action = PatchStaticSafetyNoActionCandidate(
                candidate_id=f"patch_static_safety_no_action_candidate:{uuid4()}",
                report_id=report.report_id,
                reason="Static safety report contains failed or blocked findings.",
                evidence_refs=_finding_evidence(report.findings),
                recommended_review_decision="no_action",
                candidate_status="candidate_only",
                applied=False,
            )
        elif any(finding.finding_type in {"missing_patch_draft", "missing_diff_preview"} for finding in report.findings):
            needs_more_input = PatchStaticSafetyNeedsMoreInputCandidate(
                candidate_id=f"patch_static_safety_needs_more_input_candidate:{uuid4()}",
                report_id=report.report_id,
                reason="Static safety requires patch draft and diff preview inputs.",
                missing_inputs=_missing_inputs(report.findings),
                evidence_refs=_finding_evidence(report.findings),
                recommended_review_decision="needs_more_input",
                candidate_status="candidate_only",
                applied=False,
            )
        return PatchStaticSafetyResult(report=report, no_action_candidate=no_action, needs_more_input_candidate=needs_more_input)

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "report_name": "Self-Modification Patch Static Safety PIG Report",
            "version": SELF_MODIFICATION_STATIC_SAFETY_VERSION,
            "layer": "self_modification_safety",
            "subject": "patch_static_safety_check",
            "principles": [
                "static safety check is not dry-run",
                "static safety report is not approval",
                "static safety pass is not clean application",
                "static safety pass does not imply patch apply",
            ],
            "file_write_enabled": False,
            "apply_patch_enabled": False,
            "dry_run_executed": False,
            "review_approved": False,
            "apply_gate_opened": False,
            "patch_apply_enabled": False,
            "workspace_file_changed_emitted": False,
            "llm_judge_enabled": False,
            "safe_to_apply": False,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "projection_name": "Self-Modification Patch Static Safety OCPX Projection",
            "state": SELF_MODIFICATION_STATIC_SAFETY_STATE,
            "version": SELF_MODIFICATION_STATIC_SAFETY_VERSION,
            "source_read_models": [
                "PatchDraftState",
                "DiffPreviewState",
                "PatchOperationDraftState",
                "PatchCandidateState",
                "SelfModificationPatchPolicyState",
                "SelfModificationLifecyclePolicyState",
            ],
            "target_read_models": [
                "PatchStaticSafetyState",
                "PatchStaticSafetyFindingState",
                "PatchDryRunEligibilityState",
            ],
            "effect_types": ["read_only_observation", "state_candidate_created"],
        }

    def render_result_cli(self, result: PatchStaticSafetyResult) -> str:
        report = result.report
        return "\n".join(
            [
                "Self-Modification Patch Static Safety Check",
                "version=v0.22.3",
                "layer=self_modification_safety",
                f"report_id={report.report_id}",
                f"static_safety_status={report.static_safety_status}",
                f"eligible_for_dry_run={str(report.eligible_for_dry_run).lower()}",
                "safe_to_apply=false",
                "dry_run_required=true",
                "human_review_required=true",
                "apply_gate_required=true",
                "rollback_plan_required=true",
                "post_apply_verification_required=true",
                "file_write_enabled=false",
                "apply_patch_enabled=false",
                "dry_run_executed=false",
                "applied=false",
                "workspace_file_changed_emitted=false",
                "next_required_step=v0.22.4 Patch Dry-run / Applicability Check",
                "No file mutation occurred.",
                "private_full_paths_printed=False",
                "raw_full_file_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_rules_cli(self) -> str:
        rules = PatchStaticRuleRegistry().list_rules()
        return "\n".join(
            [
                "Self-Modification Patch Static Safety Rules",
                "version=v0.22.3",
                "layer=self_modification_safety",
                f"rule_count={len(rules)}",
                f"categories={','.join(sorted({rule.category for rule in rules}))}",
                "file_write_enabled=false",
                "apply_patch_enabled=false",
                "safe_to_apply=false",
                "No file mutation occurred.",
                "private_full_paths_printed=False",
                "raw_full_file_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_report_view_cli(self, *, report_id: str) -> str:
        return "\n".join(
            [
                "Self-Modification Patch Static Safety Report",
                "version=v0.22.3",
                "layer=self_modification_safety",
                f"report_id={report_id}",
                "status=not_persisted_in_v0.22.3",
                "static_safety_status=unknown_without_persisted_report",
                "eligible_for_dry_run=false",
                "safe_to_apply=false",
                "dry_run_required=true",
                "human_review_required=true",
                "apply_gate_required=true",
                "file_write_enabled=false",
                "apply_patch_enabled=false",
                "applied=false",
                "next_required_step=v0.22.4 Patch Dry-run / Applicability Check",
                "No file mutation occurred.",
                "private_full_paths_printed=False",
                "raw_full_file_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_findings_cli(self, *, report_id: str) -> str:
        return "\n".join(
            [
                "Self-Modification Patch Static Safety Findings",
                "version=v0.22.3",
                "layer=self_modification_safety",
                f"report_id={report_id}",
                "finding_types=dry_run_not_performed,review_not_approved,apply_gate_not_opened",
                "safe_to_apply=false",
                "file_write_enabled=false",
                "apply_patch_enabled=false",
                "applied=false",
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
                "Self-Modification Patch Static Safety PIG Report",
                "version=v0.22.3",
                "layer=self_modification_safety",
                f"subject={report['subject']}",
                f"principles={','.join(report['principles'])}",
                f"file_write_enabled={str(report['file_write_enabled']).lower()}",
                f"apply_patch_enabled={str(report['apply_patch_enabled']).lower()}",
                f"dry_run_executed={str(report['dry_run_executed']).lower()}",
                f"review_approved={str(report['review_approved']).lower()}",
                f"apply_gate_opened={str(report['apply_gate_opened']).lower()}",
                f"patch_apply_enabled={str(report['patch_apply_enabled']).lower()}",
                f"workspace_file_changed_emitted={str(report['workspace_file_changed_emitted']).lower()}",
                f"llm_judge_enabled={str(report['llm_judge_enabled']).lower()}",
                "safe_to_apply=false",
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
                "Self-Modification Patch Static Safety OCPX Projection",
                "version=v0.22.3",
                "layer=self_modification_safety",
                f"state={projection['state']}",
                f"source_read_models={','.join(projection['source_read_models'])}",
                f"target_read_models={','.join(projection['target_read_models'])}",
                f"effect_types={','.join(projection['effect_types'])}",
                "safe_to_apply=false",
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


def _rule(rule_id: str, name: str, category: str, severity: str) -> PatchStaticSafetyRule:
    return PatchStaticSafetyRule(
        rule_id=rule_id,
        rule_name=name,
        category=category,
        severity_if_failed=severity,
        description=f"Static safety rule for {name.casefold()}.",
        enabled=True,
        source_policy_ref={"ref_type": "self_modification_safety_contract", "version": "v0.22.0"},
    )


def _find_rule(rules: list[PatchStaticSafetyRule], rule_id: str) -> PatchStaticSafetyRule:
    for rule in rules:
        if rule.rule_id == rule_id:
            return rule
    return _rule(rule_id, rule_id.replace("_", " "), "policy", "error")


def _rules_for(rules: list[PatchStaticSafetyRule], category: str) -> list[PatchStaticSafetyRule]:
    return [rule for rule in rules if rule.category == category and rule.enabled]


def _result(
    rule: PatchStaticSafetyRule,
    passed: bool,
    message: str,
    finding_type: str,
    target_ref: dict[str, Any] | None,
    operation_ref: dict[str, Any] | None,
) -> PatchStaticSafetyRuleResult:
    severity = "info" if passed else rule.severity_if_failed
    if finding_type in {"dry_run_not_performed", "review_not_approved", "apply_gate_not_opened"}:
        severity = "info"
        passed = True
    return PatchStaticSafetyRuleResult(
        result_id=f"patch_static_safety_rule_result:{uuid4()}",
        rule_id=rule.rule_id,
        passed=passed,
        severity=severity,
        message=message,
        target_ref=target_ref,
        operation_ref=operation_ref,
        evidence_refs=[
            {"ref_type": "patch_static_safety_rule", "rule_id": rule.rule_id},
            {"ref_type": "patch_static_safety_version", "version": SELF_MODIFICATION_STATIC_SAFETY_VERSION},
            {"finding_type": finding_type},
        ],
    )


def _finding_type_from_result(result: PatchStaticSafetyRuleResult) -> str:
    for evidence in result.evidence_refs:
        value = evidence.get("finding_type")
        if isinstance(value, str):
            return value
    return "ok" if result.passed else "static_safety_blocked"


def _category_results(
    rule_results: list[PatchStaticSafetyRuleResult],
    findings: list[PatchStaticSafetyFinding],
    rules: list[PatchStaticSafetyRule],
) -> list[PatchStaticSafetyCategoryResult]:
    categories = sorted({rule.category for rule in rules})
    results: list[PatchStaticSafetyCategoryResult] = []
    rule_by_id = {rule.rule_id: rule for rule in rules}
    for category in categories:
        category_rule_results = [result for result in rule_results if rule_by_id.get(result.rule_id, None) and rule_by_id[result.rule_id].category == category]
        category_findings = [finding for finding in findings if finding.rule_ref and rule_by_id.get(finding.rule_ref.get("rule_id"), None) and rule_by_id[finding.rule_ref["rule_id"]].category == category]
        warning_count = sum(1 for finding in category_findings if finding.severity == "warning")
        error_count = sum(1 for finding in category_findings if finding.severity == "error")
        critical_count = sum(1 for finding in category_findings if finding.severity == "critical")
        status = "passed"
        if critical_count:
            status = "blocked"
        elif error_count:
            status = "failed"
        elif warning_count:
            status = "warning"
        results.append(
            PatchStaticSafetyCategoryResult(
                category_id=f"patch_static_safety_category_result:{category}",
                category=category,
                checked_rule_count=len(category_rule_results),
                passed_rule_count=sum(1 for result in category_rule_results if result.passed),
                warning_count=warning_count,
                error_count=error_count,
                critical_count=critical_count,
                category_status=status,
                findings=category_findings,
            )
        )
    return results


def _status_from_findings(findings: list[PatchStaticSafetyFinding]) -> str:
    types = {finding.finding_type for finding in findings}
    if types & {"missing_patch_draft", "missing_diff_preview", "draft_already_applied", "private_path_risk", "secret_file_risk", "binary_file_risk"}:
        return "blocked"
    if any(finding.severity in {"error", "critical"} for finding in findings):
        return "failed"
    if any(finding.severity == "warning" for finding in findings):
        return "warning"
    return "passed"


def _is_non_workspace_path(path: str) -> bool:
    normalized = path.replace("\\", "/")
    return normalized.startswith("../") or normalized.startswith("/") or ":" in normalized


def _looks_secret(path: str) -> bool:
    lowered = path.casefold().replace("\\", "/")
    name = lowered.rsplit("/", 1)[-1]
    return name in {".env", ".env.local", "id_rsa"} or name.endswith((".pem", ".key", ".pfx", ".p12")) or "secret" in lowered


def _looks_binary(path: str) -> bool:
    return path.casefold().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".exe", ".dll"))


def _looks_generated(path: str) -> bool:
    lowered = path.casefold().replace("\\", "/")
    return "/generated/" in f"/{lowered}/" or lowered.startswith("build/") or lowered.startswith("dist/") or lowered.endswith(".lock")


def _operation_preview_text(draft: PatchDraft, preview: DiffPreviewArtifact) -> str:
    parts: list[str] = []
    for operation in draft.operations:
        parts.extend([operation.old_text_preview or "", operation.new_text_preview or "", operation.rationale])
    for hunk in preview.hunk_previews:
        parts.extend(hunk.context_lines_preview)
        parts.extend(hunk.removed_lines_preview)
        parts.extend(hunk.added_lines_preview)
    if preview.preview_text_sanitized:
        parts.append(preview.preview_text_sanitized)
    return "\n".join(parts)


def _contains_any(text: str, tokens: list[str]) -> bool:
    lowered = text.casefold()
    return any(token.casefold() in lowered for token in tokens)


def _finding_evidence(findings: list[PatchStaticSafetyFinding]) -> list[dict[str, Any]]:
    return [{"ref_type": "patch_static_safety_finding", "finding_type": finding.finding_type} for finding in findings]


def _missing_inputs(findings: list[PatchStaticSafetyFinding]) -> list[str]:
    missing: list[str] = []
    for finding in findings:
        if finding.finding_type == "missing_patch_draft":
            missing.append("patch_draft")
        if finding.finding_type == "missing_diff_preview":
            missing.append("diff_preview")
    return _unique(missing) or ["static_safety_source"]


def _unique(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
