"""v0.39.3 human-approved patch materialization and sandbox apply.

This module opens the first bounded sandbox mutation stage. The only helper
that mutates files is apply_sandbox_text_replacements, and it is constrained to
exact text replacement under a validated sandbox root. The module does not
create workspaces, run git, export patch files, invoke shell/process execution,
run tests, invoke providers, invoke subagents, execute self-prompts, or certify
production readiness.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any

from .boundary import _require_non_blank


V0393_VERSION = "v0.39.3"
V0393_RELEASE_NAME = "v0.39.3 Human-approved Patch Materialization & Sandbox Apply"
V039_TRACK_NAME = "Human-approved Sandbox Repair Apply & Re-test Loop with PI-native Self-Prompting Mission Loop Boundary"

PROHIBITED_RUNTIME_ACTIONS = [
    "workspace_creation",
    "git_worktree",
    "git_checkout",
    "branch_creation",
    "live_apply",
    "patch_file_export",
    "apply_patch",
    "git_apply",
    "tests",
    "self_prompt_execution",
    "subagent_invocation",
    "model_provider",
    "external_agent",
    "Dominion",
]


class RepairSandboxApplyMode(StrEnum):
    HUMAN_APPROVED_PATCH_MATERIALIZATION = "human_approved_patch_materialization"
    SANDBOX_APPLY_PREFLIGHT = "sandbox_apply_preflight"
    SANDBOX_APPLY_PLAN = "sandbox_apply_plan"
    SANDBOX_TEXT_REPLACEMENT_APPLY = "sandbox_text_replacement_apply"
    SANDBOX_APPLY_TRANSACTION = "sandbox_apply_transaction"
    SANDBOX_APPLY_RESULT = "sandbox_apply_result"
    SANDBOX_APPLY_AUDIT = "sandbox_apply_audit"
    ROLLBACK_DISCARD_METADATA = "rollback_discard_metadata"
    FUTURE_POST_APPLY_RETEST_INPUT = "future_post_apply_retest_input"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairSandboxApplySourceKind(StrEnum):
    V0392_WORKSPACE_ISOLATION_DECISION = "v0392_workspace_isolation_decision"
    V0392_WORKSPACE_DESCRIPTOR = "v0392_workspace_descriptor"
    V0392_TARGET_BINDING = "v0392_target_binding"
    V0392_LIVE_BOUNDARY_CHECK = "v0392_live_boundary_check"
    V0391_APPROVAL_ARTIFACT_DECISION = "v0391_approval_artifact_decision"
    V0391_APPROVAL_PROCESS_STATE_GATE = "v0391_approval_process_state_gate"
    V0391_APPROVAL_ARTIFACT = "v0391_approval_artifact"
    V0390_REPAIR_APPLY_BOUNDARY = "v0390_repair_apply_boundary"
    V0384_PROPOSED_PATCH_ENVELOPE = "v0384_proposed_patch_envelope"
    V0384_PROPOSED_DIFF_METADATA = "v0384_proposed_diff_metadata"
    V0384_PROPOSED_CODE_HUNK = "v0384_proposed_code_hunk"
    V0385_SAFETY_REPORT = "v0385_safety_report"
    V0386_HUMAN_REVIEW_PACKET = "v0386_human_review_packet"
    SUPPLIED_SANDBOX_ROOT = "supplied_sandbox_root"
    SUPPLIED_SANDBOX_TARGET_FILE = "supplied_sandbox_target_file"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class RepairSandboxApplyStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    INPUT_VALIDATED = "input_validated"
    PREFLIGHT_COMPLETED = "preflight_completed"
    PATCH_MATERIALIZED = "patch_materialized"
    APPLY_PLAN_CREATED = "apply_plan_created"
    APPLY_TRANSACTION_CREATED = "apply_transaction_created"
    SANDBOX_APPLY_COMPLETED = "sandbox_apply_completed"
    SANDBOX_APPLY_COMPLETED_WITH_WARNINGS = "sandbox_apply_completed_with_warnings"
    SANDBOX_APPLY_BLOCKED = "sandbox_apply_blocked"
    SANDBOX_APPLY_FAILED = "sandbox_apply_failed"
    ROLLBACK_IN_MEMORY_COMPLETED = "rollback_in_memory_completed"
    READY_FOR_FUTURE_POST_APPLY_RETEST = "ready_for_future_post_apply_retest"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    REVIEW_REQUIRED = "review_required"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class RepairSandboxApplyReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    APPROVAL_GATE_READY = "approval_gate_ready"
    WORKSPACE_ISOLATION_READY = "workspace_isolation_ready"
    PATCH_MATERIALIZATION_READY = "patch_materialization_ready"
    SANDBOX_APPLY_PREFLIGHT_READY = "sandbox_apply_preflight_ready"
    SANDBOX_APPLY_PLAN_READY = "sandbox_apply_plan_ready"
    SANDBOX_APPLY_TRANSACTION_READY = "sandbox_apply_transaction_ready"
    SANDBOX_APPLY_RESULT_READY = "sandbox_apply_result_ready"
    FUTURE_POST_APPLY_RETEST_INPUT_READY = "future_post_apply_retest_input_ready"
    DESIGN_HANDOFF_READY_FOR_V0394 = "design_handoff_ready_for_v0394"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class RepairSandboxApplyDecisionKind(StrEnum):
    ALLOW_PATCH_MATERIALIZATION = "allow_patch_materialization"
    ALLOW_SANDBOX_APPLY_PREFLIGHT = "allow_sandbox_apply_preflight"
    ALLOW_SANDBOX_APPLY_PLAN = "allow_sandbox_apply_plan"
    ALLOW_SANDBOX_TEXT_REPLACEMENT_APPLY = "allow_sandbox_text_replacement_apply"
    ALLOW_SANDBOX_APPLY_TRANSACTION = "allow_sandbox_apply_transaction"
    ALLOW_SANDBOX_APPLY_RESULT = "allow_sandbox_apply_result"
    ALLOW_FUTURE_POST_APPLY_RETEST_INPUT = "allow_future_post_apply_retest_input"
    CHOOSE_DO_NOTHING = "choose_do_nothing"
    CHOOSE_HUMAN_REVIEW_REQUIRED = "choose_human_review_required"
    DENY = "deny"
    BLOCK = "block"
    REJECT_MISSING_APPROVAL_GATE = "reject_missing_approval_gate"
    REJECT_INVALID_WORKSPACE = "reject_invalid_workspace"
    REJECT_LIVE_WORKSPACE_TARGET = "reject_live_workspace_target"
    REJECT_REFERENCE_CORPUS_TARGET = "reject_reference_corpus_target"
    REJECT_SECRET_TARGET = "reject_secret_target"
    REJECT_PATH_ESCAPE = "reject_path_escape"
    REJECT_SYMLINK_TARGET = "reject_symlink_target"
    REJECT_BINARY_TARGET = "reject_binary_target"
    REJECT_ORIGINAL_TEXT_MISMATCH = "reject_original_text_mismatch"
    REJECT_UNAPPROVED_PATCH = "reject_unapproved_patch"
    REJECT_UNSAFE_PATCH = "reject_unsafe_patch"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class RepairSandboxApplyRiskKind(StrEnum):
    MISSING_APPROVAL_GATE_RISK = "missing_approval_gate_risk"
    INVALID_APPROVAL_GATE_RISK = "invalid_approval_gate_risk"
    MISSING_WORKSPACE_ISOLATION_RISK = "missing_workspace_isolation_risk"
    INVALID_WORKSPACE_RISK = "invalid_workspace_risk"
    SANDBOX_LIVE_CONFUSION_RISK = "sandbox_live_confusion_risk"
    LIVE_WORKSPACE_TARGET_RISK = "live_workspace_target_risk"
    REFERENCE_CORPUS_TARGET_RISK = "reference_corpus_target_risk"
    SECRET_PATH_TARGET_RISK = "secret_path_target_risk"
    PATH_TRAVERSAL_RISK = "path_traversal_risk"
    SYMLINK_ESCAPE_RISK = "symlink_escape_risk"
    BINARY_FILE_RISK = "binary_file_risk"
    UNAPPROVED_PATCH_RISK = "unapproved_patch_risk"
    UNSAFE_PATCH_RISK = "unsafe_patch_risk"
    ORIGINAL_TEXT_MISMATCH_RISK = "original_text_mismatch_risk"
    PARTIAL_APPLY_RISK = "partial_apply_risk"
    ROLLBACK_FAILURE_RISK = "rollback_failure_risk"
    PATCH_FILE_EXPORT_CONFUSION_RISK = "patch_file_export_confusion_risk"
    APPLY_PATCH_CONFUSION_RISK = "apply_patch_confusion_risk"
    GIT_APPLY_CONFUSION_RISK = "git_apply_confusion_risk"
    SHELL_SUBPROCESS_APPLY_RISK = "shell_subprocess_apply_risk"
    TEST_EXECUTION_CONFUSION_RISK = "test_execution_confusion_risk"
    SELF_PROMPT_EXECUTION_CONFUSION_RISK = "self_prompt_execution_confusion_risk"
    SUBAGENT_INVOCATION_CONFUSION_RISK = "subagent_invocation_confusion_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    MODEL_PROVIDER_INVOCATION_RISK = "model_provider_invocation_risk"
    AUTONOMOUS_LOOP_RUNTIME_RISK = "autonomous_loop_runtime_risk"
    RETRY_LOOP_RISK = "retry_loop_risk"
    MULTI_CYCLE_LOOP_RISK = "multi_cycle_loop_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    UNKNOWN = "unknown"


class RepairSandboxPatchMaterializationKind(StrEnum):
    STRUCTURED_HUNK_TEXT_REPLACEMENT = "structured_hunk_text_replacement"
    BOUNDED_UNIFIED_DIFF_METADATA_RENDER = "bounded_unified_diff_metadata_render"
    IN_MEMORY_PATCH_MATERIALIZATION = "in_memory_patch_materialization"
    REJECTED_PATCH_FILE_EXPORT = "rejected_patch_file_export"
    UNSUPPORTED = "unsupported"
    UNKNOWN = "unknown"


class RepairSandboxApplyOperationKind(StrEnum):
    EXACT_TEXT_REPLACE = "exact_text_replace"
    INSERT_AFTER_ANCHOR = "insert_after_anchor"
    INSERT_BEFORE_ANCHOR = "insert_before_anchor"
    DELETE_EXACT_TEXT = "delete_exact_text"
    NO_OP = "no_op"
    UNSUPPORTED = "unsupported"
    UNKNOWN = "unknown"


class RepairSandboxApplyTargetKind(StrEnum):
    SANDBOX_TEXT_FILE = "sandbox_text_file"
    SANDBOX_TEST_FILE = "sandbox_test_file"
    SANDBOX_CONFIG_FILE = "sandbox_config_file"
    LIVE_WORKSPACE_FILE = "live_workspace_file"
    REFERENCE_CORPUS_FILE = "reference_corpus_file"
    SECRET_OR_CREDENTIAL_FILE = "secret_or_credential_file"
    BINARY_FILE = "binary_file"
    UNKNOWN = "unknown"


class RepairSandboxApplyDisposition(StrEnum):
    SANDBOX_APPLY_COMPLETED = "sandbox_apply_completed"
    SANDBOX_APPLY_COMPLETED_WITH_WARNINGS = "sandbox_apply_completed_with_warnings"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    REVIEW_REQUIRED = "review_required"
    DO_NOTHING_PREFERRED = "do_nothing_preferred"
    NO_OP = "no_op"
    FAILED = "failed"
    UNKNOWN = "unknown"


class RepairSandboxApplyFailureKind(StrEnum):
    MISSING_APPROVAL_GATE = "missing_approval_gate"
    INVALID_WORKSPACE = "invalid_workspace"
    TARGET_OUTSIDE_SANDBOX = "target_outside_sandbox"
    LIVE_WORKSPACE_TARGET = "live_workspace_target"
    REFERENCE_CORPUS_TARGET = "reference_corpus_target"
    SECRET_TARGET = "secret_target"
    SYMLINK_TARGET = "symlink_target"
    BINARY_TARGET = "binary_target"
    ORIGINAL_TEXT_NOT_FOUND = "original_text_not_found"
    ORIGINAL_TEXT_AMBIGUOUS = "original_text_ambiguous"
    WRITE_FAILED = "write_failed"
    ROLLBACK_FAILED = "rollback_failed"
    UNSUPPORTED_OPERATION = "unsupported_operation"
    UNSAFE_PATCH = "unsafe_patch"
    UNKNOWN = "unknown"


UNSAFE_FLAG_NAMES = [
    "ready_for_execution",
    "ready_for_general_execution",
    "ready_for_sandbox_repair_workspace_creation",
    "ready_for_git_worktree_creation",
    "ready_for_git_checkout",
    "ready_for_branch_creation",
    "ready_for_filesystem_scan",
    "ready_for_source_file_read",
    "ready_for_sandbox_source_read",
    "ready_for_live_workspace_read",
    "ready_for_unbounded_source_read",
    "ready_for_reference_source_read",
    "ready_for_secret_read",
    "ready_for_source_file_write",
    "ready_for_sandbox_source_write",
    "ready_for_patch_file_write",
    "ready_for_file_edit",
    "ready_for_live_workspace_apply",
    "ready_for_patch_application",
    "ready_for_apply_patch",
    "ready_for_git_apply",
    "ready_for_post_apply_controlled_retest",
    "ready_for_repair_test_execution",
    "ready_for_before_after_repair_comparison",
    "ready_for_repair_effectiveness_assessment",
    "ready_for_repair_process_state_projection",
    "ready_for_ocel_event_write",
    "ready_for_ocpx_state_persistence",
    "ready_for_pig_recommendation_execution",
    "ready_for_self_prompt_generation",
    "ready_for_self_prompt_auto_execution",
    "ready_for_next_action_draft_generation",
    "ready_for_next_action_auto_execution",
    "ready_for_agent_to_subagent_prompt_generation",
    "ready_for_subagent_auto_invocation",
    "ready_for_external_agent_execution",
    "ready_for_model_provider_invocation",
    "ready_for_autonomous_loop_runtime",
    "ready_for_automatic_repair",
    "ready_for_retry_loop",
    "ready_for_multi_cycle_loop",
    "ready_for_repair_execution",
    "ready_for_test_execution",
    "ready_for_controlled_test_subprocess",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_dependency_install",
    "ready_for_network_access",
    "ready_for_tool_execution",
    "ready_for_claude_code_invocation",
    "ready_for_codex_cli_invocation",
    "ready_for_dominion_runtime",
    "ready_for_infinite_agent_loop",
    "ready_for_provider_invocation",
    "ready_for_direct_network_access",
    "ready_for_credential_access",
    "ready_for_general_agent_execution",
    "ready_for_autonomous_agent_runtime",
    "ready_for_independent_agent_runtime",
    "ready_for_general_tool_execution",
    "ready_for_unquarantined_action_execution",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
    "production_certified",
]

UNSAFE_POLICY_ALLOW_NAMES = [
    "allow_workspace_creation",
    "allow_git_worktree_creation",
    "allow_git_checkout",
    "allow_branch_creation",
    "allow_filesystem_scan",
    "allow_live_workspace_read",
    "allow_unbounded_source_read",
    "allow_reference_source_read",
    "allow_secret_read",
    "allow_live_workspace_write",
    "allow_source_file_write",
    "allow_patch_file_write",
    "allow_file_edit_outside_sandbox",
    "allow_live_workspace_apply",
    "allow_apply_patch",
    "allow_git_apply",
    "allow_post_apply_test_execution",
    "allow_repair_test_execution",
    "allow_self_prompt_generation",
    "allow_self_prompt_auto_execution",
    "allow_next_action_auto_execution",
    "allow_agent_to_subagent_prompt_generation",
    "allow_subagent_auto_invocation",
    "allow_external_agent_execution",
    "allow_model_provider_invocation",
    "allow_autonomous_loop_runtime",
    "allow_retry_loop",
    "allow_multi_cycle_loop",
    "allow_automatic_repair",
    "allow_repair_execution",
    "allow_test_execution",
    "allow_subprocess",
    "allow_shell",
    "allow_dependency_install",
    "allow_network_access",
    "allow_dominion_runtime",
]

UNSAFE_TRANSACTION_NAMES = [
    "live_workspace_touched",
    "shell_used",
    "subprocess_used",
    "apply_patch_called",
    "git_apply_called",
    "tests_run",
    "model_invoked",
    "external_agent_invoked",
]

UNSAFE_RESULT_NAMES = [
    "live_workspace_touched",
    "patch_file_written",
    "apply_patch_called",
    "git_apply_called",
    "tests_run",
    "repair_executed",
    "self_prompt_generated",
    "self_prompt_executed",
    "subagent_invoked",
    "model_invoked",
    "external_agent_invoked",
    "dominion_runtime_invoked",
    "production_certified",
    "ready_for_execution",
]

UNSAFE_DECISION_NAMES = [
    "live_apply_allowed_now",
    "apply_patch_allowed_now",
    "git_apply_allowed_now",
    "test_execution_allowed_now",
    "self_prompt_generation_allowed_now",
    "self_prompt_execution_allowed_now",
    "subagent_invocation_allowed_now",
    "model_provider_invocation_allowed_now",
    "external_agent_allowed_now",
    "repair_execution_allowed_now",
    "production_certified",
]

UNSAFE_REPORT_NAMES = [
    "live_apply_enabled",
    "apply_patch_enabled",
    "git_apply_enabled",
    "patch_file_export_enabled",
    "test_execution_enabled",
    "self_prompt_generation_enabled",
    "self_prompt_execution_enabled",
    "subagent_invocation_enabled",
    "model_invocation_enabled",
    "external_agent_enabled",
    "repair_execution_enabled",
    "dominion_runtime_enabled",
    "production_certified",
    "ready_for_execution",
]

BINARY_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".exe", ".dll", ".bin", ".ico"}


def _with_overrides(defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    merged.update(overrides)
    return merged


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0393_VERSION not in version:
        raise ValueError("version must include v0.39.3")


def _validate_list(field_name: str, value: Any) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list")


def _validate_dict(field_name: str, value: Any) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{field_name} must be a dict")


def _validate_false(instance: object, names: list[str]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must remain False in v0.39.3")


def _validate_true(instance: object, names: list[str]) -> None:
    for name in names:
        if getattr(instance, name) is not True:
            raise ValueError(f"{name} must be True in v0.39.3")


def _digest_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _bounded_preview(text: str, limit: int = 1200) -> str:
    return text if len(text) <= limit else text[:limit] + "...[bounded]"


def _normalize_ref(value: str) -> str:
    return value.strip().replace("\\", "/")


def _path_flags(sandbox_root_ref: str, target_relative_path: str, target_kind: RepairSandboxApplyTargetKind | str) -> dict[str, Any]:
    relative = _normalize_ref(target_relative_path)
    parts = [part.lower() for part in relative.split("/") if part]
    lower = relative.lower()
    root = Path(sandbox_root_ref)
    candidate = root / relative
    root_resolved = root.resolve(strict=False)
    candidate_resolved = candidate.resolve(strict=False)
    try:
        candidate_resolved.relative_to(root_resolved)
        inside = not Path(relative).is_absolute()
    except ValueError:
        inside = False
    path_traversal = ".." in parts or Path(relative).is_absolute()
    reference_like = any(marker in lower for marker in ["references/opencode", "references/hermes", "references/openclaw", "opencode", "hermes", "openclaw"])
    secret_like = any(marker in lower for marker in [".env", "secret", "credential", "token", "api_key", "private"])
    live_like = ("live" in parts) or target_kind == RepairSandboxApplyTargetKind.LIVE_WORKSPACE_FILE
    symlink = candidate.is_symlink()
    binary = target_kind == RepairSandboxApplyTargetKind.BINARY_FILE or candidate.suffix.lower() in BINARY_SUFFIXES
    return {
        "normalized_target_ref": str(candidate_resolved),
        "inside_sandbox_root": inside and not path_traversal,
        "path_traversal_like": path_traversal,
        "reference_corpus_like": reference_like or target_kind == RepairSandboxApplyTargetKind.REFERENCE_CORPUS_FILE,
        "secret_path_like": secret_like or target_kind == RepairSandboxApplyTargetKind.SECRET_OR_CREDENTIAL_FILE,
        "live_workspace_like": live_like,
        "symlink_target": symlink,
        "binary_target": binary,
    }


@dataclass(frozen=True)
class RepairSandboxApplyFlagSet:
    flag_set_id: str
    version: str
    sandbox_apply_layer_constructed: bool = True
    sandbox_patch_materialization_available: bool = True
    sandbox_apply_preflight_available: bool = True
    sandbox_apply_plan_available: bool = True
    sandbox_text_replacement_apply_available: bool = True
    sandbox_apply_transaction_available: bool = True
    sandbox_apply_result_available: bool = True
    sandbox_apply_audit_available: bool = True
    rollback_discard_metadata_available: bool = True
    ready_for_v0394_post_apply_controlled_retest: bool = True
    ready_for_patch_materialization: bool = True
    ready_for_sandbox_apply_preflight: bool = True
    ready_for_sandbox_apply_plan: bool = True
    ready_for_sandbox_text_replacement_apply: bool = True
    ready_for_sandbox_apply_transaction: bool = True
    ready_for_sandbox_apply_result: bool = True
    ready_for_future_post_apply_retest_input: bool = True
    ready_for_execution: bool = False
    ready_for_general_execution: bool = False
    ready_for_sandbox_repair_workspace_creation: bool = False
    ready_for_git_worktree_creation: bool = False
    ready_for_git_checkout: bool = False
    ready_for_branch_creation: bool = False
    ready_for_filesystem_scan: bool = False
    ready_for_bounded_sandbox_target_read: bool = True
    ready_for_bounded_sandbox_target_write: bool = True
    ready_for_source_file_read: bool = False
    ready_for_sandbox_source_read: bool = False
    ready_for_live_workspace_read: bool = False
    ready_for_unbounded_source_read: bool = False
    ready_for_reference_source_read: bool = False
    ready_for_secret_read: bool = False
    ready_for_source_file_write: bool = False
    ready_for_sandbox_source_write: bool = False
    ready_for_patch_file_write: bool = False
    ready_for_file_edit: bool = False
    ready_for_sandbox_patch_materialization: bool = True
    ready_for_sandbox_repair_apply: bool = True
    ready_for_live_workspace_apply: bool = False
    ready_for_patch_application: bool = False
    ready_for_apply_patch: bool = False
    ready_for_git_apply: bool = False
    ready_for_post_apply_controlled_retest: bool = False
    ready_for_repair_test_execution: bool = False
    ready_for_before_after_repair_comparison: bool = False
    ready_for_repair_effectiveness_assessment: bool = False
    ready_for_repair_process_state_projection: bool = False
    ready_for_ocel_event_write: bool = False
    ready_for_ocpx_state_persistence: bool = False
    ready_for_pig_recommendation_execution: bool = False
    ready_for_self_prompt_generation: bool = False
    ready_for_self_prompt_auto_execution: bool = False
    ready_for_next_action_draft_generation: bool = False
    ready_for_next_action_auto_execution: bool = False
    ready_for_agent_to_subagent_prompt_generation: bool = False
    ready_for_subagent_auto_invocation: bool = False
    ready_for_external_agent_execution: bool = False
    ready_for_model_provider_invocation: bool = False
    ready_for_autonomous_loop_runtime: bool = False
    ready_for_automatic_repair: bool = False
    ready_for_retry_loop: bool = False
    ready_for_multi_cycle_loop: bool = False
    ready_for_repair_execution: bool = False
    ready_for_test_execution: bool = False
    ready_for_controlled_test_subprocess: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_dependency_install: bool = False
    ready_for_network_access: bool = False
    ready_for_tool_execution: bool = False
    ready_for_claude_code_invocation: bool = False
    ready_for_codex_cli_invocation: bool = False
    ready_for_dominion_runtime: bool = False
    ready_for_infinite_agent_loop: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_direct_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_independent_agent_runtime: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_unquarantined_action_execution: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_false(self, UNSAFE_FLAG_NAMES)


@dataclass(frozen=True)
class RepairSandboxApplySourceRef:
    source_ref_id: str
    source_kind: RepairSandboxApplySourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairSandboxApplyPolicy:
    policy_id: str
    version: str
    allowed_modes: list[RepairSandboxApplyMode | str]
    allowed_materialization_kinds: list[RepairSandboxPatchMaterializationKind | str]
    allowed_operation_kinds: list[RepairSandboxApplyOperationKind | str]
    allowed_target_kinds: list[RepairSandboxApplyTargetKind | str]
    prohibited_target_kinds: list[RepairSandboxApplyTargetKind | str]
    prohibited_path_fragments: list[str]
    max_file_changes: int = 10
    max_hunks: int = 50
    max_file_bytes: int = 1_000_000
    require_approval_decision: bool = True
    require_approval_process_state_gate: bool = True
    require_workspace_isolation_decision: bool = True
    require_live_boundary_check: bool = True
    require_safety_report: bool = True
    require_proposed_patch_envelope: bool = True
    require_exact_original_text_match: bool = True
    require_sandbox_root_containment: bool = True
    reject_live_workspace_targets: bool = True
    reject_reference_targets: bool = True
    reject_secret_targets: bool = True
    reject_symlink_targets: bool = True
    reject_binary_targets: bool = True
    allow_in_memory_patch_materialization: bool = True
    allow_bounded_sandbox_target_read: bool = True
    allow_bounded_sandbox_target_write: bool = True
    allow_sandbox_text_replacement_apply: bool = True
    allow_sandbox_apply_transaction: bool = True
    allow_future_post_apply_retest_input: bool = True
    allow_workspace_creation: bool = False
    allow_git_worktree_creation: bool = False
    allow_git_checkout: bool = False
    allow_branch_creation: bool = False
    allow_filesystem_scan: bool = False
    allow_live_workspace_read: bool = False
    allow_unbounded_source_read: bool = False
    allow_reference_source_read: bool = False
    allow_secret_read: bool = False
    allow_live_workspace_write: bool = False
    allow_source_file_write: bool = False
    allow_patch_file_write: bool = False
    allow_file_edit_outside_sandbox: bool = False
    allow_live_workspace_apply: bool = False
    allow_apply_patch: bool = False
    allow_git_apply: bool = False
    allow_post_apply_test_execution: bool = False
    allow_repair_test_execution: bool = False
    allow_self_prompt_generation: bool = False
    allow_self_prompt_auto_execution: bool = False
    allow_next_action_auto_execution: bool = False
    allow_agent_to_subagent_prompt_generation: bool = False
    allow_subagent_auto_invocation: bool = False
    allow_external_agent_execution: bool = False
    allow_model_provider_invocation: bool = False
    allow_autonomous_loop_runtime: bool = False
    allow_retry_loop: bool = False
    allow_multi_cycle_loop: bool = False
    allow_automatic_repair: bool = False
    allow_repair_execution: bool = False
    allow_test_execution: bool = False
    allow_subprocess: bool = False
    allow_shell: bool = False
    allow_dependency_install: bool = False
    allow_network_access: bool = False
    allow_dominion_runtime: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_id", self.policy_id)
        _validate_version(self.version)
        for name in [
            "allowed_modes",
            "allowed_materialization_kinds",
            "allowed_operation_kinds",
            "allowed_target_kinds",
            "prohibited_target_kinds",
            "prohibited_path_fragments",
        ]:
            _validate_list(name, getattr(self, name))
        for name in ["max_file_changes", "max_hunks", "max_file_bytes"]:
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        _validate_dict("metadata", self.metadata)
        _validate_false(self, UNSAFE_POLICY_ALLOW_NAMES)


@dataclass(frozen=True)
class RepairSandboxApplyInput:
    sandbox_apply_input_id: str
    version: str
    approval_decision_id: str | None
    approval_process_state_gate_id: str | None
    workspace_isolation_decision_id: str | None
    workspace_descriptor_id: str | None
    live_boundary_check_id: str | None
    proposed_patch_envelope_id: str | None
    safety_report_id: str | None
    human_review_packet_id: str | None
    sandbox_root_ref: str
    requested_mode: RepairSandboxApplyMode | str
    source_refs: list[RepairSandboxApplySourceRef]
    prohibited_runtime_actions: list[str]
    task_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("sandbox_apply_input_id", self.sandbox_apply_input_id)
        _validate_version(self.version)
        _require_non_blank("sandbox_root_ref", self.sandbox_root_ref)
        _require_non_blank("task_summary", self.task_summary)
        _validate_list("source_refs", self.source_refs)
        _validate_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_dict("metadata", self.metadata)
        for action in PROHIBITED_RUNTIME_ACTIONS:
            if action not in self.prohibited_runtime_actions:
                raise ValueError(f"prohibited_runtime_actions must include {action}")


@dataclass(frozen=True)
class RepairSandboxPatchMaterialization:
    materialization_id: str
    version: str
    materialization_kind: RepairSandboxPatchMaterializationKind | str
    proposed_patch_envelope_id: str
    materialized_hunk_count: int
    materialized_file_count: int
    materialized_patch_preview: str
    in_memory_only: bool
    patch_file_written: bool
    patch_file_path: str | None
    materialization_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("materialization_id", self.materialization_id)
        _validate_version(self.version)
        _require_non_blank("proposed_patch_envelope_id", self.proposed_patch_envelope_id)
        _require_non_blank("materialization_summary", self.materialization_summary)
        if self.materialized_hunk_count < 0 or self.materialized_file_count < 0:
            raise ValueError("materialized counts must be >= 0")
        if len(self.materialized_patch_preview) > 1300:
            raise ValueError("materialized_patch_preview must be bounded")
        if self.in_memory_only is not True:
            raise ValueError("in_memory_only must be True")
        if self.patch_file_written is not False or self.patch_file_path is not None:
            raise ValueError("patch files must not be written in v0.39.3")
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairSandboxApplyTarget:
    target_id: str
    version: str
    sandbox_root_ref: str
    target_relative_path: str
    target_kind: RepairSandboxApplyTargetKind | str
    normalized_target_ref: str
    target_summary: str
    inside_sandbox_root: bool
    live_workspace_like: bool
    reference_corpus_like: bool
    secret_path_like: bool
    path_traversal_like: bool
    symlink_target: bool
    binary_target: bool
    eligible_for_sandbox_apply: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("target_id", self.target_id)
        _validate_version(self.version)
        _require_non_blank("sandbox_root_ref", self.sandbox_root_ref)
        _require_non_blank("target_relative_path", self.target_relative_path)
        _require_non_blank("normalized_target_ref", self.normalized_target_ref)
        _require_non_blank("target_summary", self.target_summary)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        unsafe = any([
            not self.inside_sandbox_root,
            self.live_workspace_like,
            self.reference_corpus_like,
            self.secret_path_like,
            self.path_traversal_like,
            self.symlink_target,
            self.binary_target,
        ])
        if unsafe and self.eligible_for_sandbox_apply:
            raise ValueError("unsafe target cannot be eligible for sandbox apply")


@dataclass(frozen=True)
class RepairSandboxApplyPreflight:
    preflight_id: str
    version: str
    sandbox_apply_input_id: str
    targets: list[RepairSandboxApplyTarget]
    approval_gate_valid: bool
    workspace_isolation_valid: bool
    safety_report_valid: bool
    proposed_patch_valid: bool
    all_targets_eligible: bool
    exact_original_text_required: bool
    preflight_passed: bool
    preflight_summary: str
    failure_kinds: list[RepairSandboxApplyFailureKind | str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("preflight_id", self.preflight_id)
        _validate_version(self.version)
        _require_non_blank("sandbox_apply_input_id", self.sandbox_apply_input_id)
        _require_non_blank("preflight_summary", self.preflight_summary)
        _validate_list("targets", self.targets)
        _validate_list("failure_kinds", self.failure_kinds)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        if not all([self.approval_gate_valid, self.workspace_isolation_valid, self.safety_report_valid, self.proposed_patch_valid, self.all_targets_eligible]):
            if self.preflight_passed:
                raise ValueError("preflight_passed must be False if required gates fail")


@dataclass(frozen=True)
class RepairSandboxApplyOperation:
    operation_id: str
    version: str
    operation_kind: RepairSandboxApplyOperationKind | str
    target: RepairSandboxApplyTarget
    original_text: str
    replacement_text: str
    operation_summary: str
    original_text_digest: str | None
    replacement_text_digest: str | None
    exact_match_required: bool
    exact_match_found: bool
    ambiguous_match_found: bool
    applied: bool
    failed: bool
    failure_kind: RepairSandboxApplyFailureKind | str | None
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("operation_id", self.operation_id)
        _validate_version(self.version)
        _require_non_blank("operation_summary", self.operation_summary)
        if len(self.original_text) > 100_000 or len(self.replacement_text) > 100_000:
            raise ValueError("operation text must be bounded")
        if self.exact_match_required is not True:
            raise ValueError("exact_match_required must be True by default")
        if self.applied and (self.failed or not self.target.eligible_for_sandbox_apply or not self.exact_match_found or self.ambiguous_match_found):
            raise ValueError("applied operation requires eligible target and exact unambiguous match")
        if (self.failed or not self.target.eligible_for_sandbox_apply or not self.exact_match_found or self.ambiguous_match_found) and self.applied:
            raise ValueError("unsafe or mismatched operation cannot be applied")
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairSandboxApplyTransaction:
    transaction_id: str
    version: str
    sandbox_apply_input_id: str
    materialization_id: str
    operation_ids: list[str]
    target_ids: list[str]
    transaction_summary: str
    max_cycle_count: int
    apply_attempt_count: int
    rollback_performed_in_memory: bool
    partial_apply_detected: bool
    transaction_atomic: bool
    sandbox_only: bool
    live_workspace_touched: bool = False
    shell_used: bool = False
    subprocess_used: bool = False
    apply_patch_called: bool = False
    git_apply_called: bool = False
    tests_run: bool = False
    model_invoked: bool = False
    external_agent_invoked: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("transaction_id", self.transaction_id)
        _validate_version(self.version)
        _require_non_blank("sandbox_apply_input_id", self.sandbox_apply_input_id)
        _require_non_blank("materialization_id", self.materialization_id)
        _require_non_blank("transaction_summary", self.transaction_summary)
        _validate_list("operation_ids", self.operation_ids)
        _validate_list("target_ids", self.target_ids)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        if self.max_cycle_count != 1:
            raise ValueError("max_cycle_count must be 1")
        if self.apply_attempt_count > 1:
            raise ValueError("apply_attempt_count must be <= 1")
        if self.sandbox_only is not True:
            raise ValueError("transaction must be sandbox_only")
        _validate_false(self, UNSAFE_TRANSACTION_NAMES)


@dataclass(frozen=True)
class RepairSandboxApplyResult:
    apply_result_id: str
    version: str
    transaction_id: str
    status: RepairSandboxApplyStatus | str
    disposition: RepairSandboxApplyDisposition | str
    applied_operation_ids: list[str]
    failed_operation_ids: list[str]
    changed_target_refs: list[str]
    pre_apply_digests: dict[str, str]
    post_apply_digests: dict[str, str]
    failure_kinds: list[RepairSandboxApplyFailureKind | str]
    result_summary: str
    sandbox_apply_completed: bool
    ready_for_future_post_apply_retest_input: bool
    live_workspace_touched: bool = False
    patch_file_written: bool = False
    apply_patch_called: bool = False
    git_apply_called: bool = False
    tests_run: bool = False
    repair_executed: bool = False
    self_prompt_generated: bool = False
    self_prompt_executed: bool = False
    subagent_invoked: bool = False
    model_invoked: bool = False
    external_agent_invoked: bool = False
    dominion_runtime_invoked: bool = False
    production_certified: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("apply_result_id", self.apply_result_id)
        _validate_version(self.version)
        _require_non_blank("transaction_id", self.transaction_id)
        _require_non_blank("result_summary", self.result_summary)
        for name in ["applied_operation_ids", "failed_operation_ids", "changed_target_refs", "failure_kinds", "evidence_refs"]:
            _validate_list(name, getattr(self, name))
        for name in ["pre_apply_digests", "post_apply_digests"]:
            _validate_dict(name, getattr(self, name))
        _validate_dict("metadata", self.metadata)
        if self.ready_for_future_post_apply_retest_input and not self.sandbox_apply_completed:
            raise ValueError("future retest input requires completed sandbox apply")
        _validate_false(self, UNSAFE_RESULT_NAMES)


@dataclass(frozen=True)
class RepairSandboxApplyAudit:
    audit_id: str
    version: str
    sandbox_apply_input_id: str
    transaction_id: str | None
    apply_result_id: str | None
    audit_summary: str
    approval_gate_confirmed: bool
    workspace_isolation_confirmed: bool
    sandbox_root_containment_confirmed: bool
    live_workspace_exclusion_confirmed: bool
    reference_corpus_exclusion_confirmed: bool
    secret_path_exclusion_confirmed: bool
    exact_text_match_confirmed: bool
    no_patch_file_export_confirmed: bool
    no_apply_patch_confirmed: bool
    no_git_apply_confirmed: bool
    no_shell_confirmed: bool
    no_subprocess_confirmed: bool
    no_test_execution_confirmed: bool
    no_self_prompt_execution_confirmed: bool
    no_subagent_invocation_confirmed: bool
    no_model_invocation_confirmed: bool
    no_external_agent_confirmed: bool
    no_dominion_runtime_confirmed: bool
    no_production_certification_confirmed: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("audit_id", self.audit_id)
        _validate_version(self.version)
        _require_non_blank("sandbox_apply_input_id", self.sandbox_apply_input_id)
        _require_non_blank("audit_summary", self.audit_summary)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        _validate_true(
            self,
            [
                "no_patch_file_export_confirmed",
                "no_apply_patch_confirmed",
                "no_git_apply_confirmed",
                "no_shell_confirmed",
                "no_subprocess_confirmed",
                "no_test_execution_confirmed",
                "no_self_prompt_execution_confirmed",
                "no_subagent_invocation_confirmed",
                "no_model_invocation_confirmed",
                "no_external_agent_confirmed",
                "no_dominion_runtime_confirmed",
                "no_production_certification_confirmed",
            ],
        )


@dataclass(frozen=True)
class RepairSandboxApplyDecision:
    sandbox_apply_decision_id: str
    version: str
    decision_kind: RepairSandboxApplyDecisionKind | str
    status: RepairSandboxApplyStatus | str
    readiness_level: RepairSandboxApplyReadinessLevel | str
    disposition: RepairSandboxApplyDisposition | str
    decision_summary: str
    rationale_summary: str
    confidence: str
    evidence_refs: list[str]
    ready_for_future_post_apply_retest_input: bool
    patch_materialization_allowed_now: bool
    sandbox_target_read_allowed_now: bool
    sandbox_target_write_allowed_now: bool
    sandbox_apply_allowed_now: bool
    live_apply_allowed_now: bool = False
    apply_patch_allowed_now: bool = False
    git_apply_allowed_now: bool = False
    test_execution_allowed_now: bool = False
    self_prompt_generation_allowed_now: bool = False
    self_prompt_execution_allowed_now: bool = False
    subagent_invocation_allowed_now: bool = False
    model_provider_invocation_allowed_now: bool = False
    external_agent_allowed_now: bool = False
    repair_execution_allowed_now: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("sandbox_apply_decision_id", self.sandbox_apply_decision_id)
        _validate_version(self.version)
        _require_non_blank("decision_summary", self.decision_summary)
        _require_non_blank("rationale_summary", self.rationale_summary)
        _require_non_blank("confidence", self.confidence)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        _validate_false(self, UNSAFE_DECISION_NAMES)


@dataclass(frozen=True)
class V0393ReadinessReport:
    report_id: str
    version: str
    release_name: str
    track_name: str
    materialization: RepairSandboxPatchMaterialization | None
    preflight: RepairSandboxApplyPreflight | None
    transaction: RepairSandboxApplyTransaction | None
    apply_result: RepairSandboxApplyResult | None
    audit: RepairSandboxApplyAudit | None
    decision: RepairSandboxApplyDecision
    flags: RepairSandboxApplyFlagSet
    source_refs: list[RepairSandboxApplySourceRef]
    report_summary: str
    ready_for_v0394_post_apply_controlled_retest: bool
    ready_for_patch_materialization: bool
    ready_for_sandbox_apply_preflight: bool
    ready_for_sandbox_apply_plan: bool
    ready_for_sandbox_apply_transaction: bool
    ready_for_sandbox_apply_result: bool
    ready_for_future_post_apply_retest_input: bool
    sandbox_apply_completed: bool
    patch_materialization_enabled: bool
    bounded_sandbox_target_read_enabled: bool
    bounded_sandbox_target_write_enabled: bool
    sandbox_apply_enabled: bool
    live_apply_enabled: bool = False
    apply_patch_enabled: bool = False
    git_apply_enabled: bool = False
    patch_file_export_enabled: bool = False
    test_execution_enabled: bool = False
    self_prompt_generation_enabled: bool = False
    self_prompt_execution_enabled: bool = False
    subagent_invocation_enabled: bool = False
    model_invocation_enabled: bool = False
    external_agent_enabled: bool = False
    repair_execution_enabled: bool = False
    dominion_runtime_enabled: bool = False
    production_certified: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version(self.version)
        _require_non_blank("release_name", self.release_name)
        _require_non_blank("track_name", self.track_name)
        _require_non_blank("report_summary", self.report_summary)
        _validate_list("source_refs", self.source_refs)
        _validate_dict("metadata", self.metadata)
        _validate_false(self, UNSAFE_REPORT_NAMES)


@dataclass(frozen=True)
class RepairSandboxApplyValidationFinding:
    finding_id: str
    finding_summary: str
    risk_kind: RepairSandboxApplyRiskKind | str
    blocked: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("finding_summary", self.finding_summary)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairSandboxApplyValidationReport:
    validation_report_id: str
    version: str
    validation_summary: str
    findings: list[RepairSandboxApplyValidationFinding]
    confirms_approval_gate: bool = True
    confirms_workspace_isolation: bool = True
    confirms_target_containment: bool = True
    confirms_exact_match: bool = True
    confirms_sandbox_only_apply: bool = True
    confirms_no_live_apply: bool = True
    confirms_no_patch_file_export: bool = True
    confirms_no_apply_patch: bool = True
    confirms_no_git_apply: bool = True
    confirms_no_shell_subprocess: bool = True
    confirms_no_test_execution: bool = True
    confirms_no_self_prompt_execution: bool = True
    confirms_no_subagent_invocation: bool = True
    confirms_no_model_provider: bool = True
    confirms_no_external_agent: bool = True
    confirms_no_dominion: bool = True
    confirms_no_production_certification: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version(self.version)
        _require_non_blank("validation_summary", self.validation_summary)
        _validate_list("findings", self.findings)
        _validate_dict("metadata", self.metadata)
        _validate_true(
            self,
            [
                "confirms_approval_gate",
                "confirms_workspace_isolation",
                "confirms_target_containment",
                "confirms_exact_match",
                "confirms_sandbox_only_apply",
                "confirms_no_live_apply",
                "confirms_no_patch_file_export",
                "confirms_no_apply_patch",
                "confirms_no_git_apply",
                "confirms_no_shell_subprocess",
                "confirms_no_test_execution",
                "confirms_no_self_prompt_execution",
                "confirms_no_subagent_invocation",
                "confirms_no_model_provider",
                "confirms_no_external_agent",
                "confirms_no_dominion",
                "confirms_no_production_certification",
            ],
        )


@dataclass(frozen=True)
class RepairSandboxApplyRunPreview:
    run_preview_id: str
    version: str
    preview_summary: str
    preview_steps: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        _validate_version(self.version)
        _require_non_blank("preview_summary", self.preview_summary)
        _validate_list("preview_steps", self.preview_steps)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairSandboxApplySandboxOnlyGuarantee:
    guarantee_id: str
    version: str
    guarantee_summary: str
    no_workspace_creation: bool = True
    no_git_worktree: bool = True
    no_git_checkout: bool = True
    no_branch_creation: bool = True
    no_filesystem_scan: bool = True
    no_live_workspace_read: bool = True
    no_live_workspace_write: bool = True
    no_live_apply: bool = True
    no_reference_corpus_mutation: bool = True
    no_secret_path_mutation: bool = True
    no_patch_file_export: bool = True
    no_apply_patch: bool = True
    no_git_apply: bool = True
    no_shell: bool = True
    no_subprocess: bool = True
    no_test_execution: bool = True
    no_self_prompt_execution: bool = True
    no_subagent_invocation: bool = True
    no_model_invocation: bool = True
    no_external_agent: bool = True
    no_autonomous_loop: bool = True
    no_retry_loop: bool = True
    no_multi_cycle_loop: bool = True
    no_repair_execution: bool = True
    no_dominion_runtime: bool = True
    no_production_certification: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version(self.version)
        _require_non_blank("guarantee_summary", self.guarantee_summary)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, [name for name in vars(self) if name.startswith("no_")])


def build_repair_sandbox_apply_flags(**overrides: Any) -> RepairSandboxApplyFlagSet:
    defaults = {"flag_set_id": "v0393-sandbox-apply-flags", "version": V0393_VERSION}
    return RepairSandboxApplyFlagSet(**_with_overrides(defaults, overrides))


def build_repair_sandbox_apply_source_ref(**overrides: Any) -> RepairSandboxApplySourceRef:
    defaults = {
        "source_ref_id": "v0393-source-ref",
        "source_kind": RepairSandboxApplySourceKind.V0392_WORKSPACE_ISOLATION_DECISION,
        "source_id": "v0392-workspace-decision",
        "source_summary": "v0.39.2 workspace isolation decision supplies sandbox apply input metadata.",
        "evidence_refs": ["v0392-workspace-decision"],
    }
    return RepairSandboxApplySourceRef(**_with_overrides(defaults, overrides))


def default_repair_sandbox_apply_policy(**overrides: Any) -> RepairSandboxApplyPolicy:
    defaults = {
        "policy_id": "v0393-sandbox-apply-policy",
        "version": V0393_VERSION,
        "allowed_modes": [
            RepairSandboxApplyMode.HUMAN_APPROVED_PATCH_MATERIALIZATION,
            RepairSandboxApplyMode.SANDBOX_APPLY_PREFLIGHT,
            RepairSandboxApplyMode.SANDBOX_APPLY_PLAN,
            RepairSandboxApplyMode.SANDBOX_TEXT_REPLACEMENT_APPLY,
            RepairSandboxApplyMode.SANDBOX_APPLY_TRANSACTION,
            RepairSandboxApplyMode.SANDBOX_APPLY_RESULT,
            RepairSandboxApplyMode.SANDBOX_APPLY_AUDIT,
            RepairSandboxApplyMode.ROLLBACK_DISCARD_METADATA,
            RepairSandboxApplyMode.FUTURE_POST_APPLY_RETEST_INPUT,
        ],
        "allowed_materialization_kinds": [
            RepairSandboxPatchMaterializationKind.STRUCTURED_HUNK_TEXT_REPLACEMENT,
            RepairSandboxPatchMaterializationKind.BOUNDED_UNIFIED_DIFF_METADATA_RENDER,
            RepairSandboxPatchMaterializationKind.IN_MEMORY_PATCH_MATERIALIZATION,
        ],
        "allowed_operation_kinds": [RepairSandboxApplyOperationKind.EXACT_TEXT_REPLACE],
        "allowed_target_kinds": [
            RepairSandboxApplyTargetKind.SANDBOX_TEXT_FILE,
            RepairSandboxApplyTargetKind.SANDBOX_TEST_FILE,
            RepairSandboxApplyTargetKind.SANDBOX_CONFIG_FILE,
        ],
        "prohibited_target_kinds": [
            RepairSandboxApplyTargetKind.LIVE_WORKSPACE_FILE,
            RepairSandboxApplyTargetKind.REFERENCE_CORPUS_FILE,
            RepairSandboxApplyTargetKind.SECRET_OR_CREDENTIAL_FILE,
            RepairSandboxApplyTargetKind.BINARY_FILE,
        ],
        "prohibited_path_fragments": ["..", ".env", "secrets", "tokens", "references/OpenCode", "references/Hermes", "references/OpenClaw", "live"],
    }
    return RepairSandboxApplyPolicy(**_with_overrides(defaults, overrides))


def build_repair_sandbox_apply_policy(**overrides: Any) -> RepairSandboxApplyPolicy:
    return default_repair_sandbox_apply_policy(**overrides)


def build_repair_sandbox_apply_input(**overrides: Any) -> RepairSandboxApplyInput:
    defaults = {
        "sandbox_apply_input_id": "v0393-sandbox-apply-input",
        "version": V0393_VERSION,
        "approval_decision_id": "v0391-approval-decision",
        "approval_process_state_gate_id": "v0391-process-state-gate",
        "workspace_isolation_decision_id": "v0392-workspace-decision",
        "workspace_descriptor_id": "v0392-workspace-descriptor",
        "live_boundary_check_id": "v0392-live-boundary-check",
        "proposed_patch_envelope_id": "patch-envelope-1",
        "safety_report_id": "safety-report-1",
        "human_review_packet_id": "review-packet-1",
        "sandbox_root_ref": "sandbox-root",
        "requested_mode": RepairSandboxApplyMode.SANDBOX_TEXT_REPLACEMENT_APPLY,
        "source_refs": [build_repair_sandbox_apply_source_ref()],
        "prohibited_runtime_actions": list(PROHIBITED_RUNTIME_ACTIONS),
        "task_summary": "Apply approved exact text replacement hunks inside a validated sandbox root.",
    }
    return RepairSandboxApplyInput(**_with_overrides(defaults, overrides))


def build_repair_sandbox_patch_materialization(**overrides: Any) -> RepairSandboxPatchMaterialization:
    defaults = {
        "materialization_id": "v0393-patch-materialization",
        "version": V0393_VERSION,
        "materialization_kind": RepairSandboxPatchMaterializationKind.IN_MEMORY_PATCH_MATERIALIZATION,
        "proposed_patch_envelope_id": "patch-envelope-1",
        "materialized_hunk_count": 1,
        "materialized_file_count": 1,
        "materialized_patch_preview": "sandbox/example.txt: exact_text_replace",
        "in_memory_only": True,
        "patch_file_written": False,
        "patch_file_path": None,
        "materialization_summary": "Approved proposed hunk metadata is materialized in memory only.",
        "evidence_refs": ["patch-envelope-1"],
    }
    return RepairSandboxPatchMaterialization(**_with_overrides(defaults, overrides))


def materialize_patch_from_proposed_hunks(
    proposed_patch_envelope_id: str,
    proposed_hunks: list[dict[str, str]],
) -> RepairSandboxPatchMaterialization:
    file_refs = {hunk.get("target_relative_path", "") for hunk in proposed_hunks}
    preview = "\n".join(f"{hunk.get('target_relative_path', '<target>')}: exact_text_replace" for hunk in proposed_hunks)
    return build_repair_sandbox_patch_materialization(
        proposed_patch_envelope_id=proposed_patch_envelope_id,
        materialized_hunk_count=len(proposed_hunks),
        materialized_file_count=len(file_refs),
        materialized_patch_preview=_bounded_preview(preview),
    )


def build_repair_sandbox_apply_target(**overrides: Any) -> RepairSandboxApplyTarget:
    sandbox_root_ref = overrides.get("sandbox_root_ref", "sandbox-root")
    target_relative_path = overrides.get("target_relative_path", "example.txt")
    target_kind = overrides.get("target_kind", RepairSandboxApplyTargetKind.SANDBOX_TEXT_FILE)
    flags = _path_flags(sandbox_root_ref, target_relative_path, target_kind)
    eligible = flags["inside_sandbox_root"] and not any(
        [
            flags["live_workspace_like"],
            flags["reference_corpus_like"],
            flags["secret_path_like"],
            flags["path_traversal_like"],
            flags["symlink_target"],
            flags["binary_target"],
        ]
    )
    defaults = {
        "target_id": "v0393-apply-target",
        "version": V0393_VERSION,
        "sandbox_root_ref": sandbox_root_ref,
        "target_relative_path": target_relative_path,
        "target_kind": target_kind,
        "normalized_target_ref": flags["normalized_target_ref"],
        "target_summary": "Sandbox target file is eligible for exact text replacement.",
        "inside_sandbox_root": flags["inside_sandbox_root"],
        "live_workspace_like": flags["live_workspace_like"],
        "reference_corpus_like": flags["reference_corpus_like"],
        "secret_path_like": flags["secret_path_like"],
        "path_traversal_like": flags["path_traversal_like"],
        "symlink_target": flags["symlink_target"],
        "binary_target": flags["binary_target"],
        "eligible_for_sandbox_apply": eligible,
        "evidence_refs": ["target-ref"],
    }
    return RepairSandboxApplyTarget(**_with_overrides(defaults, overrides))


def validate_sandbox_apply_target(
    sandbox_root_ref: str,
    target_relative_path: str,
    target_kind: RepairSandboxApplyTargetKind | str = RepairSandboxApplyTargetKind.SANDBOX_TEXT_FILE,
) -> RepairSandboxApplyTarget:
    return build_repair_sandbox_apply_target(
        sandbox_root_ref=sandbox_root_ref,
        target_relative_path=target_relative_path,
        target_kind=target_kind,
    )


def build_repair_sandbox_apply_preflight(**overrides: Any) -> RepairSandboxApplyPreflight:
    targets = overrides.get("targets", [build_repair_sandbox_apply_target()])
    approval_gate_valid = overrides.get("approval_gate_valid", True)
    workspace_isolation_valid = overrides.get("workspace_isolation_valid", True)
    safety_report_valid = overrides.get("safety_report_valid", True)
    proposed_patch_valid = overrides.get("proposed_patch_valid", True)
    all_targets_eligible = overrides.get("all_targets_eligible", all(target.eligible_for_sandbox_apply for target in targets))
    passed = all([approval_gate_valid, workspace_isolation_valid, safety_report_valid, proposed_patch_valid, all_targets_eligible])
    failures: list[RepairSandboxApplyFailureKind] = []
    if not approval_gate_valid:
        failures.append(RepairSandboxApplyFailureKind.MISSING_APPROVAL_GATE)
    if not workspace_isolation_valid:
        failures.append(RepairSandboxApplyFailureKind.INVALID_WORKSPACE)
    if not all_targets_eligible:
        failures.append(RepairSandboxApplyFailureKind.UNSAFE_PATCH)
    defaults = {
        "preflight_id": "v0393-preflight",
        "version": V0393_VERSION,
        "sandbox_apply_input_id": "v0393-sandbox-apply-input",
        "targets": targets,
        "approval_gate_valid": approval_gate_valid,
        "workspace_isolation_valid": workspace_isolation_valid,
        "safety_report_valid": safety_report_valid,
        "proposed_patch_valid": proposed_patch_valid,
        "all_targets_eligible": all_targets_eligible,
        "exact_original_text_required": True,
        "preflight_passed": passed,
        "preflight_summary": "Sandbox apply preflight validates approval, workspace, safety, patch, and target gates.",
        "failure_kinds": failures,
        "evidence_refs": ["v0393-sandbox-apply-input"],
    }
    return RepairSandboxApplyPreflight(**_with_overrides(defaults, overrides))


def create_sandbox_apply_preflight(sandbox_apply_input: RepairSandboxApplyInput, targets: list[RepairSandboxApplyTarget]) -> RepairSandboxApplyPreflight:
    return build_repair_sandbox_apply_preflight(
        sandbox_apply_input_id=sandbox_apply_input.sandbox_apply_input_id,
        targets=targets,
        approval_gate_valid=bool(sandbox_apply_input.approval_decision_id and sandbox_apply_input.approval_process_state_gate_id),
        workspace_isolation_valid=bool(sandbox_apply_input.workspace_isolation_decision_id and sandbox_apply_input.workspace_descriptor_id),
        safety_report_valid=bool(sandbox_apply_input.safety_report_id),
        proposed_patch_valid=bool(sandbox_apply_input.proposed_patch_envelope_id),
    )


def build_repair_sandbox_apply_operation(**overrides: Any) -> RepairSandboxApplyOperation:
    original_text = overrides.get("original_text", "before")
    replacement_text = overrides.get("replacement_text", "after")
    target = overrides.get("target", build_repair_sandbox_apply_target())
    defaults = {
        "operation_id": "v0393-operation",
        "version": V0393_VERSION,
        "operation_kind": RepairSandboxApplyOperationKind.EXACT_TEXT_REPLACE,
        "target": target,
        "original_text": original_text,
        "replacement_text": replacement_text,
        "operation_summary": "Exact original text replacement operation for sandbox target.",
        "original_text_digest": _digest_text(original_text),
        "replacement_text_digest": _digest_text(replacement_text),
        "exact_match_required": True,
        "exact_match_found": True,
        "ambiguous_match_found": False,
        "applied": False,
        "failed": False,
        "failure_kind": None,
        "evidence_refs": [target.target_id],
    }
    return RepairSandboxApplyOperation(**_with_overrides(defaults, overrides))


def create_sandbox_apply_operations(
    sandbox_root_ref: str,
    proposed_hunks: list[dict[str, str]],
) -> list[RepairSandboxApplyOperation]:
    operations: list[RepairSandboxApplyOperation] = []
    for index, hunk in enumerate(proposed_hunks):
        target = validate_sandbox_apply_target(
            sandbox_root_ref=sandbox_root_ref,
            target_relative_path=hunk["target_relative_path"],
            target_kind=hunk.get("target_kind", RepairSandboxApplyTargetKind.SANDBOX_TEXT_FILE),
        )
        operations.append(
            build_repair_sandbox_apply_operation(
                operation_id=f"v0393-operation-{index + 1}",
                target=target,
                original_text=hunk["original_text"],
                replacement_text=hunk["replacement_text"],
                exact_match_found=False,
            )
        )
    return operations


def build_repair_sandbox_apply_transaction(**overrides: Any) -> RepairSandboxApplyTransaction:
    defaults = {
        "transaction_id": "v0393-transaction",
        "version": V0393_VERSION,
        "sandbox_apply_input_id": "v0393-sandbox-apply-input",
        "materialization_id": "v0393-patch-materialization",
        "operation_ids": ["v0393-operation"],
        "target_ids": ["v0393-apply-target"],
        "transaction_summary": "Single-cycle sandbox-only text replacement transaction.",
        "max_cycle_count": 1,
        "apply_attempt_count": 1,
        "rollback_performed_in_memory": False,
        "partial_apply_detected": False,
        "transaction_atomic": True,
        "sandbox_only": True,
        "evidence_refs": ["v0393-operation"],
    }
    return RepairSandboxApplyTransaction(**_with_overrides(defaults, overrides))


def build_repair_sandbox_apply_result(**overrides: Any) -> RepairSandboxApplyResult:
    defaults = {
        "apply_result_id": "v0393-apply-result",
        "version": V0393_VERSION,
        "transaction_id": "v0393-transaction",
        "status": RepairSandboxApplyStatus.SANDBOX_APPLY_COMPLETED,
        "disposition": RepairSandboxApplyDisposition.SANDBOX_APPLY_COMPLETED,
        "applied_operation_ids": ["v0393-operation"],
        "failed_operation_ids": [],
        "changed_target_refs": ["sandbox-root/example.txt"],
        "pre_apply_digests": {"sandbox-root/example.txt": _digest_text("before")},
        "post_apply_digests": {"sandbox-root/example.txt": _digest_text("after")},
        "failure_kinds": [],
        "result_summary": "Sandbox-only exact text replacement completed; no tests or repair correctness claim.",
        "sandbox_apply_completed": True,
        "ready_for_future_post_apply_retest_input": True,
        "evidence_refs": ["v0393-transaction"],
    }
    return RepairSandboxApplyResult(**_with_overrides(defaults, overrides))


def apply_sandbox_text_replacements(
    sandbox_apply_input: RepairSandboxApplyInput,
    operations: list[RepairSandboxApplyOperation],
    materialization: RepairSandboxPatchMaterialization | None = None,
) -> tuple[RepairSandboxApplyTransaction, RepairSandboxApplyResult, list[RepairSandboxApplyOperation]]:
    transaction_id = "v0393-transaction"
    materialization_id = materialization.materialization_id if materialization else "v0393-patch-materialization"
    original_contents: dict[Path, str] = {}
    pre_digests: dict[str, str] = {}
    post_digests: dict[str, str] = {}
    applied_ops: list[RepairSandboxApplyOperation] = []
    failed_ops: list[RepairSandboxApplyOperation] = []
    failure_kinds: list[RepairSandboxApplyFailureKind] = []
    partial = False
    rollback = False
    root = Path(sandbox_apply_input.sandbox_root_ref).resolve(strict=False)

    try:
        for operation in operations:
            target = validate_sandbox_apply_target(
                sandbox_root_ref=sandbox_apply_input.sandbox_root_ref,
                target_relative_path=operation.target.target_relative_path,
                target_kind=operation.target.target_kind,
            )
            if not target.eligible_for_sandbox_apply:
                failure = _target_failure(target)
                failure_kinds.append(failure)
                failed_ops.append(_operation_with_result(operation, target, False, False, False, True, failure))
                raise ValueError(failure.value)
            target_path = Path(target.normalized_target_ref)
            target_path.resolve(strict=False).relative_to(root)
            content = target_path.read_text(encoding="utf-8")
            original_contents.setdefault(target_path, content)
            occurrences = content.count(operation.original_text)
            if occurrences == 0:
                failure_kinds.append(RepairSandboxApplyFailureKind.ORIGINAL_TEXT_NOT_FOUND)
                failed_ops.append(_operation_with_result(operation, target, False, False, False, True, RepairSandboxApplyFailureKind.ORIGINAL_TEXT_NOT_FOUND))
                raise ValueError(RepairSandboxApplyFailureKind.ORIGINAL_TEXT_NOT_FOUND.value)
            if occurrences > 1:
                failure_kinds.append(RepairSandboxApplyFailureKind.ORIGINAL_TEXT_AMBIGUOUS)
                failed_ops.append(_operation_with_result(operation, target, True, True, False, True, RepairSandboxApplyFailureKind.ORIGINAL_TEXT_AMBIGUOUS))
                raise ValueError(RepairSandboxApplyFailureKind.ORIGINAL_TEXT_AMBIGUOUS.value)
            new_content = content.replace(operation.original_text, operation.replacement_text, 1)
            pre_digests[target.normalized_target_ref] = _digest_text(content)
            target_path.write_text(new_content, encoding="utf-8")
            post_digests[target.normalized_target_ref] = _digest_text(new_content)
            applied_ops.append(_operation_with_result(operation, target, True, False, True, False, None))
    except Exception:
        partial = bool(applied_ops)
        if partial:
            for path, content in original_contents.items():
                path.write_text(content, encoding="utf-8")
            rollback = True
        transaction = build_repair_sandbox_apply_transaction(
            transaction_id=transaction_id,
            sandbox_apply_input_id=sandbox_apply_input.sandbox_apply_input_id,
            materialization_id=materialization_id,
            operation_ids=[operation.operation_id for operation in operations],
            target_ids=[operation.target.target_id for operation in operations],
            rollback_performed_in_memory=rollback,
            partial_apply_detected=partial,
            transaction_atomic=True,
        )
        result = build_repair_sandbox_apply_result(
            transaction_id=transaction.transaction_id,
            status=RepairSandboxApplyStatus.ROLLBACK_IN_MEMORY_COMPLETED if rollback else RepairSandboxApplyStatus.SANDBOX_APPLY_FAILED,
            disposition=RepairSandboxApplyDisposition.FAILED,
            applied_operation_ids=[] if rollback else [operation.operation_id for operation in applied_ops],
            failed_operation_ids=[operation.operation_id for operation in failed_ops] or [operation.operation_id for operation in operations if operation.operation_id not in {op.operation_id for op in applied_ops}],
            changed_target_refs=[] if rollback else list(post_digests.keys()),
            pre_apply_digests=pre_digests,
            post_apply_digests={} if rollback else post_digests,
            failure_kinds=failure_kinds or [RepairSandboxApplyFailureKind.UNKNOWN],
            result_summary="Sandbox apply failed; any partial write was rolled back in memory." if rollback else "Sandbox apply failed before mutation completed.",
            sandbox_apply_completed=False,
            ready_for_future_post_apply_retest_input=False,
        )
        return transaction, result, applied_ops + failed_ops

    transaction = build_repair_sandbox_apply_transaction(
        transaction_id=transaction_id,
        sandbox_apply_input_id=sandbox_apply_input.sandbox_apply_input_id,
        materialization_id=materialization_id,
        operation_ids=[operation.operation_id for operation in applied_ops],
        target_ids=[operation.target.target_id for operation in applied_ops],
        rollback_performed_in_memory=False,
        partial_apply_detected=False,
        transaction_atomic=True,
    )
    result = build_repair_sandbox_apply_result(
        transaction_id=transaction.transaction_id,
        applied_operation_ids=[operation.operation_id for operation in applied_ops],
        failed_operation_ids=[],
        changed_target_refs=list(post_digests.keys()),
        pre_apply_digests=pre_digests,
        post_apply_digests=post_digests,
        failure_kinds=[],
        sandbox_apply_completed=True,
        ready_for_future_post_apply_retest_input=True,
    )
    return transaction, result, applied_ops


def _target_failure(target: RepairSandboxApplyTarget) -> RepairSandboxApplyFailureKind:
    if not target.inside_sandbox_root or target.path_traversal_like:
        return RepairSandboxApplyFailureKind.TARGET_OUTSIDE_SANDBOX
    if target.live_workspace_like:
        return RepairSandboxApplyFailureKind.LIVE_WORKSPACE_TARGET
    if target.reference_corpus_like:
        return RepairSandboxApplyFailureKind.REFERENCE_CORPUS_TARGET
    if target.secret_path_like:
        return RepairSandboxApplyFailureKind.SECRET_TARGET
    if target.symlink_target:
        return RepairSandboxApplyFailureKind.SYMLINK_TARGET
    if target.binary_target:
        return RepairSandboxApplyFailureKind.BINARY_TARGET
    return RepairSandboxApplyFailureKind.UNSAFE_PATCH


def _operation_with_result(
    operation: RepairSandboxApplyOperation,
    target: RepairSandboxApplyTarget,
    exact_match_found: bool,
    ambiguous_match_found: bool,
    applied: bool,
    failed: bool,
    failure_kind: RepairSandboxApplyFailureKind | None,
) -> RepairSandboxApplyOperation:
    return build_repair_sandbox_apply_operation(
        operation_id=operation.operation_id,
        target=target,
        original_text=operation.original_text,
        replacement_text=operation.replacement_text,
        exact_match_found=exact_match_found,
        ambiguous_match_found=ambiguous_match_found,
        applied=applied,
        failed=failed,
        failure_kind=failure_kind,
    )


def build_repair_sandbox_apply_audit(**overrides: Any) -> RepairSandboxApplyAudit:
    defaults = {
        "audit_id": "v0393-audit",
        "version": V0393_VERSION,
        "sandbox_apply_input_id": "v0393-sandbox-apply-input",
        "transaction_id": "v0393-transaction",
        "apply_result_id": "v0393-apply-result",
        "audit_summary": "Audit confirms sandbox-only exact text replacement and blocked runtime surfaces.",
        "approval_gate_confirmed": True,
        "workspace_isolation_confirmed": True,
        "sandbox_root_containment_confirmed": True,
        "live_workspace_exclusion_confirmed": True,
        "reference_corpus_exclusion_confirmed": True,
        "secret_path_exclusion_confirmed": True,
        "exact_text_match_confirmed": True,
        "no_patch_file_export_confirmed": True,
        "no_apply_patch_confirmed": True,
        "no_git_apply_confirmed": True,
        "no_shell_confirmed": True,
        "no_subprocess_confirmed": True,
        "no_test_execution_confirmed": True,
        "no_self_prompt_execution_confirmed": True,
        "no_subagent_invocation_confirmed": True,
        "no_model_invocation_confirmed": True,
        "no_external_agent_confirmed": True,
        "no_dominion_runtime_confirmed": True,
        "no_production_certification_confirmed": True,
        "evidence_refs": ["v0393-transaction", "v0393-apply-result"],
    }
    return RepairSandboxApplyAudit(**_with_overrides(defaults, overrides))


def audit_sandbox_apply_result(
    sandbox_apply_input: RepairSandboxApplyInput,
    transaction: RepairSandboxApplyTransaction,
    result: RepairSandboxApplyResult,
) -> RepairSandboxApplyAudit:
    return build_repair_sandbox_apply_audit(
        sandbox_apply_input_id=sandbox_apply_input.sandbox_apply_input_id,
        transaction_id=transaction.transaction_id,
        apply_result_id=result.apply_result_id,
        exact_text_match_confirmed=result.sandbox_apply_completed,
    )


def build_repair_sandbox_apply_decision(**overrides: Any) -> RepairSandboxApplyDecision:
    defaults = {
        "sandbox_apply_decision_id": "v0393-decision",
        "version": V0393_VERSION,
        "decision_kind": RepairSandboxApplyDecisionKind.ALLOW_FUTURE_POST_APPLY_RETEST_INPUT,
        "status": RepairSandboxApplyStatus.READY_FOR_FUTURE_POST_APPLY_RETEST,
        "readiness_level": RepairSandboxApplyReadinessLevel.FUTURE_POST_APPLY_RETEST_INPUT_READY,
        "disposition": RepairSandboxApplyDisposition.SANDBOX_APPLY_COMPLETED,
        "decision_summary": "Sandbox apply completed and is ready for future post-apply retest input metadata.",
        "rationale_summary": "Only bounded sandbox text replacement was allowed; no tests or live apply were enabled.",
        "confidence": "high",
        "evidence_refs": ["v0393-apply-result"],
        "ready_for_future_post_apply_retest_input": True,
        "patch_materialization_allowed_now": True,
        "sandbox_target_read_allowed_now": True,
        "sandbox_target_write_allowed_now": True,
        "sandbox_apply_allowed_now": True,
    }
    return RepairSandboxApplyDecision(**_with_overrides(defaults, overrides))


def decide_repair_sandbox_apply(result: RepairSandboxApplyResult) -> RepairSandboxApplyDecision:
    completed = result.sandbox_apply_completed and not result.failure_kinds
    return build_repair_sandbox_apply_decision(
        decision_kind=RepairSandboxApplyDecisionKind.ALLOW_FUTURE_POST_APPLY_RETEST_INPUT if completed else RepairSandboxApplyDecisionKind.REQUIRE_REVIEW,
        status=RepairSandboxApplyStatus.READY_FOR_FUTURE_POST_APPLY_RETEST if completed else RepairSandboxApplyStatus.REVIEW_REQUIRED,
        readiness_level=RepairSandboxApplyReadinessLevel.FUTURE_POST_APPLY_RETEST_INPUT_READY if completed else RepairSandboxApplyReadinessLevel.NOT_READY,
        disposition=RepairSandboxApplyDisposition.SANDBOX_APPLY_COMPLETED if completed else RepairSandboxApplyDisposition.REVIEW_REQUIRED,
        ready_for_future_post_apply_retest_input=completed,
        patch_materialization_allowed_now=completed,
        sandbox_target_read_allowed_now=completed,
        sandbox_target_write_allowed_now=completed,
        sandbox_apply_allowed_now=completed,
        confidence="high" if completed else "low",
    )


def build_repair_sandbox_apply_validation_finding(**overrides: Any) -> RepairSandboxApplyValidationFinding:
    defaults = {
        "finding_id": "v0393-validation-finding",
        "finding_summary": "Sandbox apply is bounded to validated sandbox root and blocks live/runtime surfaces.",
        "risk_kind": RepairSandboxApplyRiskKind.LIVE_WORKSPACE_TARGET_RISK,
        "blocked": True,
    }
    return RepairSandboxApplyValidationFinding(**_with_overrides(defaults, overrides))


def build_repair_sandbox_apply_validation_report(**overrides: Any) -> RepairSandboxApplyValidationReport:
    defaults = {
        "validation_report_id": "v0393-validation-report",
        "version": V0393_VERSION,
        "validation_summary": "Validation confirms approval gate, workspace isolation, containment, exact match, and sandbox-only apply.",
        "findings": [build_repair_sandbox_apply_validation_finding()],
    }
    return RepairSandboxApplyValidationReport(**_with_overrides(defaults, overrides))


def build_repair_sandbox_apply_run_preview(**overrides: Any) -> RepairSandboxApplyRunPreview:
    defaults = {
        "run_preview_id": "v0393-run-preview",
        "version": V0393_VERSION,
        "preview_summary": "Preview bounded sandbox patch materialization and exact text replacement apply.",
        "preview_steps": [
            "SandboxApplyInput",
            "PatchMaterialization",
            "ApplyTargetValidation",
            "ApplyPreflight",
            "ApplyOperations",
            "ApplyTransaction",
            "SandboxApplyResult",
            "SandboxApplyAudit",
        ],
    }
    return RepairSandboxApplyRunPreview(**_with_overrides(defaults, overrides))


def build_repair_sandbox_apply_sandbox_only_guarantee(**overrides: Any) -> RepairSandboxApplySandboxOnlyGuarantee:
    defaults = {
        "guarantee_id": "v0393-sandbox-only-guarantee",
        "version": V0393_VERSION,
        "guarantee_summary": "v0.39.3 allows only bounded sandbox target text replacement and blocks live/runtime surfaces.",
    }
    return RepairSandboxApplySandboxOnlyGuarantee(**_with_overrides(defaults, overrides))


def build_v0393_readiness_report(**overrides: Any) -> V0393ReadinessReport:
    sandbox_input = overrides.pop("sandbox_apply_input", build_repair_sandbox_apply_input())
    proposed_hunks = overrides.pop(
        "proposed_hunks",
        [{"target_relative_path": "example.txt", "original_text": "before", "replacement_text": "after"}],
    )
    materialization = materialize_patch_from_proposed_hunks(sandbox_input.proposed_patch_envelope_id or "patch-envelope-1", proposed_hunks)
    targets = [validate_sandbox_apply_target(sandbox_input.sandbox_root_ref, hunk["target_relative_path"]) for hunk in proposed_hunks]
    preflight = create_sandbox_apply_preflight(sandbox_input, targets)
    transaction = build_repair_sandbox_apply_transaction()
    result = build_repair_sandbox_apply_result()
    audit = build_repair_sandbox_apply_audit()
    decision = decide_repair_sandbox_apply(result)
    defaults = {
        "report_id": "v0393-readiness-report",
        "version": V0393_VERSION,
        "release_name": V0393_RELEASE_NAME,
        "track_name": V039_TRACK_NAME,
        "materialization": materialization,
        "preflight": preflight,
        "transaction": transaction,
        "apply_result": result,
        "audit": audit,
        "decision": decision,
        "flags": build_repair_sandbox_apply_flags(),
        "source_refs": [build_repair_sandbox_apply_source_ref()],
        "report_summary": "v0.39.3 sandbox apply completed metadata is ready for future v0.39.4 retest input only.",
        "ready_for_v0394_post_apply_controlled_retest": True,
        "ready_for_patch_materialization": True,
        "ready_for_sandbox_apply_preflight": True,
        "ready_for_sandbox_apply_plan": True,
        "ready_for_sandbox_apply_transaction": True,
        "ready_for_sandbox_apply_result": True,
        "ready_for_future_post_apply_retest_input": True,
        "sandbox_apply_completed": True,
        "patch_materialization_enabled": True,
        "bounded_sandbox_target_read_enabled": True,
        "bounded_sandbox_target_write_enabled": True,
        "sandbox_apply_enabled": True,
    }
    return V0393ReadinessReport(**_with_overrides(defaults, overrides))


def repair_sandbox_apply_flags_preserve_no_live_execution(flags: RepairSandboxApplyFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_FLAG_NAMES)


def repair_sandbox_apply_policy_blocks_live_apply_and_runtime(policy: RepairSandboxApplyPolicy) -> bool:
    return all(getattr(policy, name) is False for name in UNSAFE_POLICY_ALLOW_NAMES)


def sandbox_patch_materialization_is_not_patch_file_export(materialization: RepairSandboxPatchMaterialization) -> bool:
    return materialization.in_memory_only and not materialization.patch_file_written and materialization.patch_file_path is None


def sandbox_apply_target_is_not_live_target(target: RepairSandboxApplyTarget) -> bool:
    return not target.live_workspace_like and not target.reference_corpus_like and not target.secret_path_like


def sandbox_apply_result_is_not_test_or_repair_execution(result: RepairSandboxApplyResult) -> bool:
    return all(getattr(result, name) is False for name in UNSAFE_RESULT_NAMES)


def v0393_readiness_report_is_not_general_execution_ready(report: V0393ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_REPORT_NAMES) and repair_sandbox_apply_flags_preserve_no_live_execution(report.flags)
