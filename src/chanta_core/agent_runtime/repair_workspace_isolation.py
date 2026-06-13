"""v0.39.2 sandbox repair workspace isolation contract metadata.

This module is intentionally limited to pure in-memory metadata construction.
It does not create work areas, inspect project files, mutate repositories,
prepare patches, apply patches, run verification, invoke providers, invoke
subagents, execute self-prompts, or grant runtime authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank


V0392_VERSION = "v0.39.2"
V0392_RELEASE_NAME = "v0.39.2 Sandbox Repair Workspace Isolation Contract"
V039_TRACK_NAME = "Human-approved Sandbox Repair Apply & Re-test Loop with PI-native Self-Prompting Mission Loop Boundary"

PROHIBITED_RUNTIME_ACTIONS = [
    "workspace_creation",
    "git_worktree",
    "git_checkout",
    "branch_creation",
    "filesystem_scan",
    "source_read",
    "source_write",
    "patch_materialization",
    "patch_write",
    "apply_patch",
    "git_apply",
    "sandbox_apply",
    "live_apply",
    "test_execution",
    "self_prompt_execution",
    "subagent_invocation",
    "model_provider",
    "external_agent",
    "Dominion",
]


class RepairWorkspaceIsolationMode(StrEnum):
    SANDBOX_REPAIR_WORKSPACE_ISOLATION_CONTRACT = "sandbox_repair_workspace_isolation_contract"
    WORKSPACE_DESCRIPTOR_METADATA = "workspace_descriptor_metadata"
    WORKSPACE_ROOT_REF_METADATA = "workspace_root_ref_metadata"
    WORKSPACE_CLASSIFICATION_METADATA = "workspace_classification_metadata"
    APPLY_TARGET_ISOLATION_METADATA = "apply_target_isolation_metadata"
    COLLISION_PREVENTION_METADATA = "collision_prevention_metadata"
    LIVE_WORKSPACE_EXCLUSION_METADATA = "live_workspace_exclusion_metadata"
    REFERENCE_CORPUS_EXCLUSION_METADATA = "reference_corpus_exclusion_metadata"
    SECRET_PATH_EXCLUSION_METADATA = "secret_path_exclusion_metadata"
    FUTURE_PATCH_MATERIALIZATION_INPUT = "future_patch_materialization_input"
    FUTURE_SANDBOX_APPLY_INPUT = "future_sandbox_apply_input"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairWorkspaceIsolationSourceKind(StrEnum):
    V0391_APPROVAL_ARTIFACT_DECISION = "v0391_approval_artifact_decision"
    V0391_APPROVAL_PROCESS_STATE_GATE = "v0391_approval_process_state_gate"
    V0391_READINESS_REPORT = "v0391_readiness_report"
    V0390_REPAIR_APPLY_BOUNDARY = "v0390_repair_apply_boundary"
    V0389_HANDOFF_PACKET = "v0389_handoff_packet"
    V0389_CONSOLIDATION_REPORT = "v0389_consolidation_report"
    V0386_HUMAN_REVIEW_PACKET = "v0386_human_review_packet"
    V0385_SAFETY_REPORT = "v0385_safety_report"
    V0384_PROPOSED_PATCH_ENVELOPE = "v0384_proposed_patch_envelope"
    SUPPLIED_WORKSPACE_ROOT_REF = "supplied_workspace_root_ref"
    SUPPLIED_WORKSPACE_DESCRIPTOR = "supplied_workspace_descriptor"
    MANUAL_OPERATOR_NOTE = "manual_operator_note"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class RepairWorkspaceIsolationStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    INPUT_VALIDATED = "input_validated"
    WORKSPACE_DESCRIPTOR_CREATED = "workspace_descriptor_created"
    WORKSPACE_CLASSIFIED = "workspace_classified"
    ISOLATION_CONTRACT_CREATED = "isolation_contract_created"
    COLLISION_PREVENTION_DEFINED = "collision_prevention_defined"
    LIVE_WORKSPACE_EXCLUDED = "live_workspace_excluded"
    REFERENCE_CORPUS_EXCLUDED = "reference_corpus_excluded"
    SECRET_PATHS_EXCLUDED = "secret_paths_excluded"
    APPLY_TARGET_BOUND = "apply_target_bound"
    READY_FOR_FUTURE_PATCH_MATERIALIZATION = "ready_for_future_patch_materialization"
    READY_FOR_FUTURE_SANDBOX_APPLY = "ready_for_future_sandbox_apply"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    REVIEW_REQUIRED = "review_required"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class RepairWorkspaceIsolationReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    WORKSPACE_DESCRIPTOR_READY = "workspace_descriptor_ready"
    WORKSPACE_ROOT_REF_READY = "workspace_root_ref_ready"
    WORKSPACE_CLASSIFICATION_READY = "workspace_classification_ready"
    ISOLATION_CONTRACT_READY = "isolation_contract_ready"
    COLLISION_PREVENTION_READY = "collision_prevention_ready"
    APPLY_TARGET_ISOLATION_READY = "apply_target_isolation_ready"
    LIVE_WORKSPACE_EXCLUSION_READY = "live_workspace_exclusion_ready"
    FUTURE_PATCH_MATERIALIZATION_INPUT_READY = "future_patch_materialization_input_ready"
    FUTURE_SANDBOX_APPLY_INPUT_READY = "future_sandbox_apply_input_ready"
    DESIGN_HANDOFF_READY_FOR_V0393 = "design_handoff_ready_for_v0393"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class RepairWorkspaceIsolationDecisionKind(StrEnum):
    ALLOW_WORKSPACE_DESCRIPTOR = "allow_workspace_descriptor"
    ALLOW_WORKSPACE_ROOT_REF_METADATA = "allow_workspace_root_ref_metadata"
    ALLOW_WORKSPACE_CLASSIFICATION = "allow_workspace_classification"
    ALLOW_ISOLATION_CONTRACT = "allow_isolation_contract"
    ALLOW_COLLISION_PREVENTION_METADATA = "allow_collision_prevention_metadata"
    ALLOW_LIVE_WORKSPACE_EXCLUSION = "allow_live_workspace_exclusion"
    ALLOW_REFERENCE_CORPUS_EXCLUSION = "allow_reference_corpus_exclusion"
    ALLOW_SECRET_PATH_EXCLUSION = "allow_secret_path_exclusion"
    ALLOW_APPLY_TARGET_ISOLATION = "allow_apply_target_isolation"
    ALLOW_FUTURE_PATCH_MATERIALIZATION_INPUT = "allow_future_patch_materialization_input"
    ALLOW_FUTURE_SANDBOX_APPLY_INPUT = "allow_future_sandbox_apply_input"
    CHOOSE_DO_NOTHING = "choose_do_nothing"
    CHOOSE_HUMAN_REVIEW_REQUIRED = "choose_human_review_required"
    DENY = "deny"
    BLOCK = "block"
    REJECT_LIVE_WORKSPACE = "reject_live_workspace"
    REJECT_REFERENCE_CORPUS = "reject_reference_corpus"
    REJECT_SECRET_PATH = "reject_secret_path"
    REJECT_MISSING_APPROVAL_GATE = "reject_missing_approval_gate"
    REJECT_SCOPE_MISMATCH = "reject_scope_mismatch"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class RepairWorkspaceIsolationRiskKind(StrEnum):
    WORKSPACE_MISSING_RISK = "workspace_missing_risk"
    WORKSPACE_DESCRIPTOR_MALFORMED_RISK = "workspace_descriptor_malformed_risk"
    WORKSPACE_ROOT_UNKNOWN_RISK = "workspace_root_unknown_risk"
    WORKSPACE_NOT_DECLARED_SANDBOX_RISK = "workspace_not_declared_sandbox_risk"
    LIVE_WORKSPACE_CONFUSION_RISK = "live_workspace_confusion_risk"
    REFERENCE_CORPUS_CONFUSION_RISK = "reference_corpus_confusion_risk"
    SECRET_PATH_RISK = "secret_path_risk"
    PATH_TRAVERSAL_RISK = "path_traversal_risk"
    ABSOLUTE_PATH_CONFUSION_RISK = "absolute_path_confusion_risk"
    SYMLINK_ESCAPE_RISK = "symlink_escape_risk"
    BRANCH_COLLISION_RISK = "branch_collision_risk"
    PARALLEL_AGENT_COLLISION_RISK = "parallel_agent_collision_risk"
    GIT_WORKTREE_EXECUTION_CONFUSION_RISK = "git_worktree_execution_confusion_risk"
    FILESYSTEM_MUTATION_CONFUSION_RISK = "filesystem_mutation_confusion_risk"
    PATCH_MATERIALIZATION_CONFUSION_RISK = "patch_materialization_confusion_risk"
    SANDBOX_APPLY_CONFUSION_RISK = "sandbox_apply_confusion_risk"
    LIVE_APPLY_CONFUSION_RISK = "live_apply_confusion_risk"
    APPROVAL_SCOPE_MISMATCH_RISK = "approval_scope_mismatch_risk"
    MISSING_APPROVAL_GATE_RISK = "missing_approval_gate_risk"
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


class RepairWorkspaceKind(StrEnum):
    DECLARED_SANDBOX_WORKSPACE = "declared_sandbox_workspace"
    SANDBOX_WORKTREE_LIKE_WORKSPACE = "sandbox_worktree_like_workspace"
    SANDBOX_COPY_WORKSPACE = "sandbox_copy_workspace"
    SANDBOX_TEMP_WORKSPACE = "sandbox_temp_workspace"
    SANDBOX_CONTAINER_MOUNT_REF = "sandbox_container_mount_ref"
    LIVE_WORKSPACE = "live_workspace"
    REFERENCE_CORPUS = "reference_corpus"
    SECRET_OR_CREDENTIAL_AREA = "secret_or_credential_area"
    UNKNOWN = "unknown"


class RepairWorkspaceIsolationStrategyKind(StrEnum):
    METADATA_ONLY_DECLARED_SANDBOX = "metadata_only_declared_sandbox"
    WORKTREE_LIKE_ISOLATION_METADATA = "worktree_like_isolation_metadata"
    BRANCH_LIKE_ISOLATION_METADATA = "branch_like_isolation_metadata"
    COPY_LIKE_ISOLATION_METADATA = "copy_like_isolation_metadata"
    CONTAINER_MOUNT_LIKE_METADATA = "container_mount_like_metadata"
    MANUAL_OPERATOR_SUPPLIED_SANDBOX = "manual_operator_supplied_sandbox"
    NO_ISOLATION = "no_isolation"
    INVALID = "invalid"
    UNKNOWN = "unknown"


class RepairWorkspaceTrustLevel(StrEnum):
    TRUSTED_SANDBOX_CANDIDATE = "trusted_sandbox_candidate"
    REVIEW_REQUIRED = "review_required"
    UNTRUSTED = "untrusted"
    REJECTED_LIVE_WORKSPACE = "rejected_live_workspace"
    REJECTED_REFERENCE_CORPUS = "rejected_reference_corpus"
    REJECTED_SECRET_AREA = "rejected_secret_area"
    UNKNOWN = "unknown"


class RepairWorkspaceDisposition(StrEnum):
    ACCEPTED_FOR_FUTURE_PATCH_MATERIALIZATION = "accepted_for_future_patch_materialization"
    ACCEPTED_FOR_FUTURE_SANDBOX_APPLY = "accepted_for_future_sandbox_apply"
    ACCEPTED_WITH_WARNINGS = "accepted_with_warnings"
    REVIEW_REQUIRED = "review_required"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    DO_NOTHING_PREFERRED = "do_nothing_preferred"
    NO_OP = "no_op"
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
    "ready_for_sandbox_patch_materialization",
    "ready_for_sandbox_repair_apply",
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
    "allow_source_file_read",
    "allow_sandbox_source_read",
    "allow_live_workspace_read",
    "allow_reference_source_read",
    "allow_secret_read",
    "allow_source_file_write",
    "allow_sandbox_source_write",
    "allow_patch_file_write",
    "allow_file_edit",
    "allow_sandbox_patch_materialization",
    "allow_sandbox_repair_apply",
    "allow_live_workspace_apply",
    "allow_patch_application",
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

UNSAFE_DECISION_NAMES = [
    "workspace_creation_allowed_now",
    "git_worktree_allowed_now",
    "git_checkout_allowed_now",
    "filesystem_scan_allowed_now",
    "source_read_allowed_now",
    "source_write_allowed_now",
    "patch_materialization_allowed_now",
    "patch_file_write_allowed_now",
    "sandbox_apply_allowed_now",
    "live_apply_allowed_now",
    "apply_patch_allowed_now",
    "git_apply_allowed_now",
    "test_execution_allowed_now",
    "self_prompt_execution_allowed_now",
    "subagent_invocation_allowed_now",
    "model_provider_invocation_allowed_now",
    "external_agent_allowed_now",
    "repair_execution_allowed_now",
    "production_certified",
]

UNSAFE_REPORT_NAMES = [
    "workspace_creation_enabled",
    "git_worktree_enabled",
    "branch_creation_enabled",
    "filesystem_scan_enabled",
    "source_read_enabled",
    "source_write_enabled",
    "patch_materialization_enabled",
    "patch_file_write_enabled",
    "sandbox_apply_enabled",
    "live_apply_enabled",
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


def _with_overrides(defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    merged.update(overrides)
    return merged


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0392_VERSION not in version:
        raise ValueError("version must include v0.39.2")


def _validate_list(field_name: str, value: Any) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list")


def _validate_dict(field_name: str, value: Any) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{field_name} must be a dict")


def _validate_false(instance: object, names: list[str]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must remain False in v0.39.2")


def _validate_true(instance: object, names: list[str]) -> None:
    for name in names:
        if getattr(instance, name) is not True:
            raise ValueError(f"{name} must be True in v0.39.2")


def _normalize_root_ref(workspace_root_ref: str | None) -> str | None:
    if workspace_root_ref is None:
        return None
    normalized = workspace_root_ref.strip().replace("\\", "/")
    return normalized or None


def _root_ref_markers(workspace_root_ref: str | None) -> dict[str, bool]:
    normalized = _normalize_root_ref(workspace_root_ref)
    lower = (normalized or "").lower()
    parts = [part for part in lower.split("/") if part]
    return {
        "root_ref_present": normalized is not None,
        "absolute_path_like": bool(normalized and (normalized.startswith("/") or ":/" in normalized or normalized.startswith("//"))),
        "parent_traversal_like": ".." in parts,
        "reference_corpus_like": any(marker in lower for marker in ["references/opencode", "references/hermes", "references/openclaw", "/references/", "opencode", "hermes", "openclaw"]),
        "secret_path_like": any(marker in lower for marker in [".env", "secret", "credential", "token", "api_key", "private"]),
        "live_workspace_like": ("live" in parts) or ("chantacore" in lower and "sandbox" not in lower),
    }


@dataclass(frozen=True)
class RepairWorkspaceIsolationFlagSet:
    flag_set_id: str
    version: str
    workspace_isolation_layer_constructed: bool = True
    workspace_descriptor_available: bool = True
    workspace_root_ref_metadata_available: bool = True
    workspace_classification_available: bool = True
    workspace_isolation_contract_available: bool = True
    collision_prevention_metadata_available: bool = True
    apply_target_isolation_metadata_available: bool = True
    live_workspace_exclusion_available: bool = True
    reference_corpus_exclusion_available: bool = True
    secret_path_exclusion_available: bool = True
    ready_for_v0393_human_approved_patch_materialization_sandbox_apply: bool = True
    ready_for_workspace_descriptor_metadata: bool = True
    ready_for_workspace_root_ref_metadata: bool = True
    ready_for_workspace_classification_metadata: bool = True
    ready_for_sandbox_repair_workspace_isolation_contract: bool = True
    ready_for_collision_prevention_metadata: bool = True
    ready_for_apply_target_isolation_metadata: bool = True
    ready_for_live_workspace_exclusion_metadata: bool = True
    ready_for_reference_corpus_exclusion_metadata: bool = True
    ready_for_secret_path_exclusion_metadata: bool = True
    ready_for_future_patch_materialization_input: bool = True
    ready_for_future_sandbox_apply_input: bool = True
    ready_for_execution: bool = False
    ready_for_general_execution: bool = False
    ready_for_sandbox_repair_workspace_creation: bool = False
    ready_for_git_worktree_creation: bool = False
    ready_for_git_checkout: bool = False
    ready_for_branch_creation: bool = False
    ready_for_filesystem_scan: bool = False
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
    ready_for_sandbox_patch_materialization: bool = False
    ready_for_sandbox_repair_apply: bool = False
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
class RepairWorkspaceIsolationSourceRef:
    source_ref_id: str
    source_kind: RepairWorkspaceIsolationSourceKind | str
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
class RepairWorkspaceIsolationPolicy:
    policy_id: str
    version: str
    allowed_modes: list[RepairWorkspaceIsolationMode | str]
    allowed_workspace_kinds: list[RepairWorkspaceKind | str]
    allowed_strategy_kinds: list[RepairWorkspaceIsolationStrategyKind | str]
    prohibited_workspace_kinds: list[RepairWorkspaceKind | str]
    prohibited_path_fragments: list[str]
    require_approval_process_state_gate: bool = True
    require_sandbox_only_workspace: bool = True
    require_live_workspace_exclusion: bool = True
    require_reference_corpus_exclusion: bool = True
    require_secret_path_exclusion: bool = True
    require_collision_prevention_metadata: bool = True
    require_apply_target_isolation_metadata: bool = True
    allow_workspace_descriptor_metadata: bool = True
    allow_workspace_root_ref_metadata: bool = True
    allow_workspace_classification_metadata: bool = True
    allow_isolation_contract_metadata: bool = True
    allow_collision_prevention_metadata: bool = True
    allow_apply_target_isolation_metadata: bool = True
    allow_future_patch_materialization_input: bool = True
    allow_future_sandbox_apply_input: bool = True
    allow_workspace_creation: bool = False
    allow_git_worktree_creation: bool = False
    allow_git_checkout: bool = False
    allow_branch_creation: bool = False
    allow_filesystem_scan: bool = False
    allow_source_file_read: bool = False
    allow_sandbox_source_read: bool = False
    allow_live_workspace_read: bool = False
    allow_reference_source_read: bool = False
    allow_secret_read: bool = False
    allow_source_file_write: bool = False
    allow_sandbox_source_write: bool = False
    allow_patch_file_write: bool = False
    allow_file_edit: bool = False
    allow_sandbox_patch_materialization: bool = False
    allow_sandbox_repair_apply: bool = False
    allow_live_workspace_apply: bool = False
    allow_patch_application: bool = False
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
            "allowed_workspace_kinds",
            "allowed_strategy_kinds",
            "prohibited_workspace_kinds",
            "prohibited_path_fragments",
        ]:
            _validate_list(name, getattr(self, name))
        _validate_dict("metadata", self.metadata)
        _validate_false(self, UNSAFE_POLICY_ALLOW_NAMES)


@dataclass(frozen=True)
class RepairWorkspaceIsolationInput:
    workspace_input_id: str
    version: str
    approval_process_state_gate_id: str | None
    approval_artifact_id: str | None
    proposed_patch_envelope_id: str | None
    safety_report_id: str | None
    human_review_packet_id: str | None
    workspace_root_ref: str | None
    workspace_kind: RepairWorkspaceKind | str
    isolation_strategy: RepairWorkspaceIsolationStrategyKind | str
    requested_mode: RepairWorkspaceIsolationMode | str
    source_refs: list[RepairWorkspaceIsolationSourceRef]
    prohibited_runtime_actions: list[str]
    task_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("workspace_input_id", self.workspace_input_id)
        _validate_version(self.version)
        _require_non_blank("task_summary", self.task_summary)
        _validate_list("source_refs", self.source_refs)
        _validate_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_dict("metadata", self.metadata)
        for action in PROHIBITED_RUNTIME_ACTIONS:
            if action not in self.prohibited_runtime_actions:
                raise ValueError(f"prohibited_runtime_actions must include {action}")


@dataclass(frozen=True)
class RepairWorkspaceDescriptor:
    workspace_descriptor_id: str
    version: str
    workspace_root_ref: str | None
    workspace_kind: RepairWorkspaceKind | str
    isolation_strategy: RepairWorkspaceIsolationStrategyKind | str
    trust_level: RepairWorkspaceTrustLevel | str
    descriptor_summary: str
    declared_sandbox: bool
    declared_live_workspace: bool
    declared_reference_corpus: bool
    declared_secret_area: bool
    approval_artifact_id: str | None
    approval_process_state_gate_id: str | None
    proposed_patch_envelope_id: str | None
    safety_report_id: str | None
    human_review_packet_id: str | None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("workspace_descriptor_id", self.workspace_descriptor_id)
        _validate_version(self.version)
        _require_non_blank("descriptor_summary", self.descriptor_summary)
        _validate_dict("metadata", self.metadata)
        if self.declared_live_workspace or self.declared_reference_corpus or self.declared_secret_area:
            if self.trust_level == RepairWorkspaceTrustLevel.TRUSTED_SANDBOX_CANDIDATE:
                raise ValueError("live/reference/secret descriptors cannot be trusted sandbox candidates")


@dataclass(frozen=True)
class RepairWorkspaceRootRefValidation:
    root_ref_validation_id: str
    version: str
    workspace_root_ref: str | None
    normalized_root_ref: str | None
    root_ref_present: bool
    root_ref_declared_sandbox: bool
    absolute_path_like: bool
    parent_traversal_like: bool
    reference_corpus_like: bool
    secret_path_like: bool
    live_workspace_like: bool
    valid_for_future_patch_materialization_input: bool
    valid_for_future_sandbox_apply_input: bool
    validation_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("root_ref_validation_id", self.root_ref_validation_id)
        _validate_version(self.version)
        _require_non_blank("validation_summary", self.validation_summary)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        if any([self.parent_traversal_like, self.reference_corpus_like, self.secret_path_like, self.live_workspace_like]):
            if self.valid_for_future_patch_materialization_input or self.valid_for_future_sandbox_apply_input:
                raise ValueError("risky root refs cannot be valid future inputs")


@dataclass(frozen=True)
class RepairWorkspaceCollisionPreventionPlan:
    collision_plan_id: str
    version: str
    strategy_kind: RepairWorkspaceIsolationStrategyKind | str
    plan_summary: str
    parallel_agent_collision_blocked: bool
    shared_live_workspace_write_blocked: bool
    branch_collision_risk_mitigated: bool
    git_worktree_execution_performed: bool = False
    branch_creation_performed: bool = False
    workspace_creation_performed: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("collision_plan_id", self.collision_plan_id)
        _validate_version(self.version)
        _require_non_blank("plan_summary", self.plan_summary)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ["parallel_agent_collision_blocked", "shared_live_workspace_write_blocked", "branch_collision_risk_mitigated"])
        _validate_false(self, ["git_worktree_execution_performed", "branch_creation_performed", "workspace_creation_performed"])


@dataclass(frozen=True)
class RepairWorkspaceTargetBinding:
    target_binding_id: str
    version: str
    workspace_descriptor_id: str
    proposed_patch_envelope_id: str | None
    approval_artifact_id: str | None
    safety_report_id: str | None
    target_summary: str
    target_bound_to_approved_patch: bool
    target_bound_to_safety_report: bool
    target_bound_to_human_review_packet: bool
    target_scope_sandbox_only: bool
    target_scope_live_apply: bool
    binding_valid_for_future_materialization: bool
    binding_valid_for_future_sandbox_apply: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("target_binding_id", self.target_binding_id)
        _validate_version(self.version)
        _require_non_blank("workspace_descriptor_id", self.workspace_descriptor_id)
        _require_non_blank("target_summary", self.target_summary)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        if self.target_scope_live_apply:
            if self.binding_valid_for_future_materialization or self.binding_valid_for_future_sandbox_apply:
                raise ValueError("live target scope cannot be valid future sandbox input")


@dataclass(frozen=True)
class RepairWorkspaceLiveBoundaryCheck:
    live_boundary_check_id: str
    version: str
    workspace_descriptor_id: str
    live_workspace_excluded: bool
    live_workspace_read_blocked: bool
    live_workspace_write_blocked: bool
    live_workspace_apply_blocked: bool
    reference_corpus_excluded: bool
    secret_paths_excluded: bool
    boundary_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("live_boundary_check_id", self.live_boundary_check_id)
        _validate_version(self.version)
        _require_non_blank("workspace_descriptor_id", self.workspace_descriptor_id)
        _require_non_blank("boundary_summary", self.boundary_summary)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        _validate_true(
            self,
            [
                "live_workspace_excluded",
                "live_workspace_read_blocked",
                "live_workspace_write_blocked",
                "live_workspace_apply_blocked",
                "reference_corpus_excluded",
                "secret_paths_excluded",
            ],
        )


@dataclass(frozen=True)
class RepairWorkspaceIsolationRiskAssessment:
    risk_assessment_id: str
    version: str
    workspace_descriptor_id: str | None
    risk_kinds: list[RepairWorkspaceIsolationRiskKind | str]
    risk_summary: str
    severity: str
    blocks_future_patch_materialization_input: bool
    blocks_future_sandbox_apply_input: bool
    requires_human_review: bool
    do_nothing_recommended: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_assessment_id", self.risk_assessment_id)
        _validate_version(self.version)
        _require_non_blank("risk_summary", self.risk_summary)
        _require_non_blank("severity", self.severity)
        _validate_list("risk_kinds", self.risk_kinds)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        high_risks = {
            RepairWorkspaceIsolationRiskKind.LIVE_WORKSPACE_CONFUSION_RISK,
            RepairWorkspaceIsolationRiskKind.REFERENCE_CORPUS_CONFUSION_RISK,
            RepairWorkspaceIsolationRiskKind.SECRET_PATH_RISK,
            RepairWorkspaceIsolationRiskKind.PATH_TRAVERSAL_RISK,
            RepairWorkspaceIsolationRiskKind.PATCH_MATERIALIZATION_CONFUSION_RISK,
            RepairWorkspaceIsolationRiskKind.SANDBOX_APPLY_CONFUSION_RISK,
            RepairWorkspaceIsolationRiskKind.MISSING_APPROVAL_GATE_RISK,
            RepairWorkspaceIsolationRiskKind.WORKSPACE_NOT_DECLARED_SANDBOX_RISK,
        }
        if any(kind in high_risks or str(kind) in {risk.value for risk in high_risks} for kind in self.risk_kinds):
            if not (self.blocks_future_sandbox_apply_input or self.requires_human_review):
                raise ValueError("high-risk workspace isolation findings must block or require review")


@dataclass(frozen=True)
class RepairWorkspaceIsolationDecision:
    workspace_decision_id: str
    version: str
    decision_kind: RepairWorkspaceIsolationDecisionKind | str
    status: RepairWorkspaceIsolationStatus | str
    readiness_level: RepairWorkspaceIsolationReadinessLevel | str
    disposition: RepairWorkspaceDisposition | str
    decision_summary: str
    rationale_summary: str
    confidence: str
    evidence_refs: list[str]
    ready_for_future_patch_materialization_input: bool = True
    ready_for_future_sandbox_apply_input: bool = True
    workspace_creation_allowed_now: bool = False
    git_worktree_allowed_now: bool = False
    git_checkout_allowed_now: bool = False
    filesystem_scan_allowed_now: bool = False
    source_read_allowed_now: bool = False
    source_write_allowed_now: bool = False
    patch_materialization_allowed_now: bool = False
    patch_file_write_allowed_now: bool = False
    sandbox_apply_allowed_now: bool = False
    live_apply_allowed_now: bool = False
    apply_patch_allowed_now: bool = False
    git_apply_allowed_now: bool = False
    test_execution_allowed_now: bool = False
    self_prompt_execution_allowed_now: bool = False
    subagent_invocation_allowed_now: bool = False
    model_provider_invocation_allowed_now: bool = False
    external_agent_allowed_now: bool = False
    repair_execution_allowed_now: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("workspace_decision_id", self.workspace_decision_id)
        _validate_version(self.version)
        _require_non_blank("decision_summary", self.decision_summary)
        _require_non_blank("rationale_summary", self.rationale_summary)
        _require_non_blank("confidence", self.confidence)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        _validate_false(self, UNSAFE_DECISION_NAMES)


@dataclass(frozen=True)
class V0392ReadinessReport:
    report_id: str
    version: str
    release_name: str
    track_name: str
    workspace_descriptor: RepairWorkspaceDescriptor | None
    root_ref_validation: RepairWorkspaceRootRefValidation | None
    collision_prevention_plan: RepairWorkspaceCollisionPreventionPlan | None
    target_binding: RepairWorkspaceTargetBinding | None
    live_boundary_check: RepairWorkspaceLiveBoundaryCheck | None
    risk_assessment: RepairWorkspaceIsolationRiskAssessment | None
    decision: RepairWorkspaceIsolationDecision
    flags: RepairWorkspaceIsolationFlagSet
    source_refs: list[RepairWorkspaceIsolationSourceRef]
    report_summary: str
    ready_for_v0393_human_approved_patch_materialization_sandbox_apply: bool = True
    ready_for_workspace_descriptor_metadata: bool = True
    ready_for_workspace_root_ref_metadata: bool = True
    ready_for_workspace_classification_metadata: bool = True
    ready_for_sandbox_repair_workspace_isolation_contract: bool = True
    ready_for_collision_prevention_metadata: bool = True
    ready_for_apply_target_isolation_metadata: bool = True
    ready_for_live_workspace_exclusion_metadata: bool = True
    ready_for_future_patch_materialization_input: bool = True
    ready_for_future_sandbox_apply_input: bool = True
    workspace_creation_enabled: bool = False
    git_worktree_enabled: bool = False
    branch_creation_enabled: bool = False
    filesystem_scan_enabled: bool = False
    source_read_enabled: bool = False
    source_write_enabled: bool = False
    patch_materialization_enabled: bool = False
    patch_file_write_enabled: bool = False
    sandbox_apply_enabled: bool = False
    live_apply_enabled: bool = False
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
class RepairWorkspaceIsolationValidationFinding:
    finding_id: str
    finding_summary: str
    risk_kind: RepairWorkspaceIsolationRiskKind | str
    blocked: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("finding_summary", self.finding_summary)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairWorkspaceIsolationValidationReport:
    validation_report_id: str
    version: str
    validation_summary: str
    findings: list[RepairWorkspaceIsolationValidationFinding]
    confirms_metadata_only_workspace_isolation_contract: bool = True
    confirms_no_workspace_creation: bool = True
    confirms_no_git_worktree: bool = True
    confirms_no_branch_creation: bool = True
    confirms_no_source_read: bool = True
    confirms_no_filesystem_scan: bool = True
    confirms_no_file_write: bool = True
    confirms_no_patch_materialization: bool = True
    confirms_no_patch_application: bool = True
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
                "confirms_metadata_only_workspace_isolation_contract",
                "confirms_no_workspace_creation",
                "confirms_no_git_worktree",
                "confirms_no_branch_creation",
                "confirms_no_source_read",
                "confirms_no_filesystem_scan",
                "confirms_no_file_write",
                "confirms_no_patch_materialization",
                "confirms_no_patch_application",
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
class RepairWorkspaceIsolationRunPreview:
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
class RepairWorkspaceIsolationNoMutationGuarantee:
    guarantee_id: str
    version: str
    guarantee_summary: str
    no_workspace_creation: bool = True
    no_git_worktree: bool = True
    no_git_checkout: bool = True
    no_branch_creation: bool = True
    no_filesystem_scan: bool = True
    no_source_read: bool = True
    no_source_write: bool = True
    no_patch_materialization: bool = True
    no_patch_file_write: bool = True
    no_sandbox_apply: bool = True
    no_live_apply: bool = True
    no_patch_application: bool = True
    no_apply_patch: bool = True
    no_git_apply: bool = True
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
        _validate_true(
            self,
            [
                "no_workspace_creation",
                "no_git_worktree",
                "no_git_checkout",
                "no_branch_creation",
                "no_filesystem_scan",
                "no_source_read",
                "no_source_write",
                "no_patch_materialization",
                "no_patch_file_write",
                "no_sandbox_apply",
                "no_live_apply",
                "no_patch_application",
                "no_apply_patch",
                "no_git_apply",
                "no_test_execution",
                "no_self_prompt_execution",
                "no_subagent_invocation",
                "no_model_invocation",
                "no_external_agent",
                "no_autonomous_loop",
                "no_retry_loop",
                "no_multi_cycle_loop",
                "no_repair_execution",
                "no_dominion_runtime",
                "no_production_certification",
            ],
        )


def build_repair_workspace_isolation_flags(**overrides: Any) -> RepairWorkspaceIsolationFlagSet:
    defaults = {"flag_set_id": "v0392-workspace-isolation-flags", "version": V0392_VERSION}
    return RepairWorkspaceIsolationFlagSet(**_with_overrides(defaults, overrides))


def build_repair_workspace_isolation_source_ref(**overrides: Any) -> RepairWorkspaceIsolationSourceRef:
    defaults = {
        "source_ref_id": "v0392-source-ref",
        "source_kind": RepairWorkspaceIsolationSourceKind.V0391_APPROVAL_PROCESS_STATE_GATE,
        "source_id": "v0391-process-state-gate",
        "source_summary": "v0.39.1 approval process-state gate supplies future workspace isolation metadata.",
        "evidence_refs": ["v0391-process-state-gate"],
    }
    return RepairWorkspaceIsolationSourceRef(**_with_overrides(defaults, overrides))


def default_repair_workspace_isolation_policy(**overrides: Any) -> RepairWorkspaceIsolationPolicy:
    defaults = {
        "policy_id": "v0392-workspace-isolation-policy",
        "version": V0392_VERSION,
        "allowed_modes": [
            RepairWorkspaceIsolationMode.SANDBOX_REPAIR_WORKSPACE_ISOLATION_CONTRACT,
            RepairWorkspaceIsolationMode.WORKSPACE_DESCRIPTOR_METADATA,
            RepairWorkspaceIsolationMode.WORKSPACE_ROOT_REF_METADATA,
            RepairWorkspaceIsolationMode.WORKSPACE_CLASSIFICATION_METADATA,
            RepairWorkspaceIsolationMode.APPLY_TARGET_ISOLATION_METADATA,
            RepairWorkspaceIsolationMode.COLLISION_PREVENTION_METADATA,
            RepairWorkspaceIsolationMode.LIVE_WORKSPACE_EXCLUSION_METADATA,
            RepairWorkspaceIsolationMode.REFERENCE_CORPUS_EXCLUSION_METADATA,
            RepairWorkspaceIsolationMode.SECRET_PATH_EXCLUSION_METADATA,
            RepairWorkspaceIsolationMode.FUTURE_PATCH_MATERIALIZATION_INPUT,
            RepairWorkspaceIsolationMode.FUTURE_SANDBOX_APPLY_INPUT,
        ],
        "allowed_workspace_kinds": [
            RepairWorkspaceKind.DECLARED_SANDBOX_WORKSPACE,
            RepairWorkspaceKind.SANDBOX_WORKTREE_LIKE_WORKSPACE,
            RepairWorkspaceKind.SANDBOX_COPY_WORKSPACE,
            RepairWorkspaceKind.SANDBOX_TEMP_WORKSPACE,
            RepairWorkspaceKind.SANDBOX_CONTAINER_MOUNT_REF,
        ],
        "allowed_strategy_kinds": [
            RepairWorkspaceIsolationStrategyKind.METADATA_ONLY_DECLARED_SANDBOX,
            RepairWorkspaceIsolationStrategyKind.WORKTREE_LIKE_ISOLATION_METADATA,
            RepairWorkspaceIsolationStrategyKind.BRANCH_LIKE_ISOLATION_METADATA,
            RepairWorkspaceIsolationStrategyKind.COPY_LIKE_ISOLATION_METADATA,
            RepairWorkspaceIsolationStrategyKind.CONTAINER_MOUNT_LIKE_METADATA,
            RepairWorkspaceIsolationStrategyKind.MANUAL_OPERATOR_SUPPLIED_SANDBOX,
        ],
        "prohibited_workspace_kinds": [
            RepairWorkspaceKind.LIVE_WORKSPACE,
            RepairWorkspaceKind.REFERENCE_CORPUS,
            RepairWorkspaceKind.SECRET_OR_CREDENTIAL_AREA,
        ],
        "prohibited_path_fragments": ["..", ".env", "secrets", "tokens", "references/OpenCode", "references/Hermes", "references/OpenClaw", "live"],
        "metadata": {"digestion_first_policy_applied": True, "pi_native_sandbox_isolation_pattern": True},
    }
    return RepairWorkspaceIsolationPolicy(**_with_overrides(defaults, overrides))


def build_repair_workspace_isolation_policy(**overrides: Any) -> RepairWorkspaceIsolationPolicy:
    return default_repair_workspace_isolation_policy(**overrides)


def build_repair_workspace_isolation_input(**overrides: Any) -> RepairWorkspaceIsolationInput:
    defaults = {
        "workspace_input_id": "v0392-workspace-input",
        "version": V0392_VERSION,
        "approval_process_state_gate_id": "v0391-process-state-gate",
        "approval_artifact_id": "v0391-approval-artifact",
        "proposed_patch_envelope_id": "patch-envelope-1",
        "safety_report_id": "safety-report-1",
        "human_review_packet_id": "review-packet-1",
        "workspace_root_ref": "sandbox/repair/v0392/workspace-candidate",
        "workspace_kind": RepairWorkspaceKind.DECLARED_SANDBOX_WORKSPACE,
        "isolation_strategy": RepairWorkspaceIsolationStrategyKind.METADATA_ONLY_DECLARED_SANDBOX,
        "requested_mode": RepairWorkspaceIsolationMode.SANDBOX_REPAIR_WORKSPACE_ISOLATION_CONTRACT,
        "source_refs": [build_repair_workspace_isolation_source_ref()],
        "prohibited_runtime_actions": list(PROHIBITED_RUNTIME_ACTIONS),
        "task_summary": "Define sandbox repair workspace isolation contract metadata for future v0.39.3 handoff.",
    }
    return RepairWorkspaceIsolationInput(**_with_overrides(defaults, overrides))


def build_repair_workspace_descriptor(**overrides: Any) -> RepairWorkspaceDescriptor:
    defaults = {
        "workspace_descriptor_id": "v0392-workspace-descriptor",
        "version": V0392_VERSION,
        "workspace_root_ref": "sandbox/repair/v0392/workspace-candidate",
        "workspace_kind": RepairWorkspaceKind.DECLARED_SANDBOX_WORKSPACE,
        "isolation_strategy": RepairWorkspaceIsolationStrategyKind.METADATA_ONLY_DECLARED_SANDBOX,
        "trust_level": RepairWorkspaceTrustLevel.TRUSTED_SANDBOX_CANDIDATE,
        "descriptor_summary": "Declared sandbox workspace descriptor metadata for future patch_materialization and sandbox_apply inputs.",
        "declared_sandbox": True,
        "declared_live_workspace": False,
        "declared_reference_corpus": False,
        "declared_secret_area": False,
        "approval_artifact_id": "v0391-approval-artifact",
        "approval_process_state_gate_id": "v0391-process-state-gate",
        "proposed_patch_envelope_id": "patch-envelope-1",
        "safety_report_id": "safety-report-1",
        "human_review_packet_id": "review-packet-1",
    }
    return RepairWorkspaceDescriptor(**_with_overrides(defaults, overrides))


def classify_repair_workspace_descriptor(workspace_input: RepairWorkspaceIsolationInput) -> RepairWorkspaceDescriptor:
    kind = workspace_input.workspace_kind
    root_markers = _root_ref_markers(workspace_input.workspace_root_ref)
    declared_live = kind == RepairWorkspaceKind.LIVE_WORKSPACE or root_markers["live_workspace_like"]
    declared_reference = kind == RepairWorkspaceKind.REFERENCE_CORPUS or root_markers["reference_corpus_like"]
    declared_secret = kind == RepairWorkspaceKind.SECRET_OR_CREDENTIAL_AREA or root_markers["secret_path_like"]
    declared_sandbox = (
        kind
        in {
            RepairWorkspaceKind.DECLARED_SANDBOX_WORKSPACE,
            RepairWorkspaceKind.SANDBOX_WORKTREE_LIKE_WORKSPACE,
            RepairWorkspaceKind.SANDBOX_COPY_WORKSPACE,
            RepairWorkspaceKind.SANDBOX_TEMP_WORKSPACE,
            RepairWorkspaceKind.SANDBOX_CONTAINER_MOUNT_REF,
        }
        and not any([declared_live, declared_reference, declared_secret])
    )
    if declared_live:
        trust = RepairWorkspaceTrustLevel.REJECTED_LIVE_WORKSPACE
    elif declared_reference:
        trust = RepairWorkspaceTrustLevel.REJECTED_REFERENCE_CORPUS
    elif declared_secret:
        trust = RepairWorkspaceTrustLevel.REJECTED_SECRET_AREA
    elif declared_sandbox:
        trust = RepairWorkspaceTrustLevel.TRUSTED_SANDBOX_CANDIDATE
    else:
        trust = RepairWorkspaceTrustLevel.REVIEW_REQUIRED
    return build_repair_workspace_descriptor(
        workspace_root_ref=workspace_input.workspace_root_ref,
        workspace_kind=kind,
        isolation_strategy=workspace_input.isolation_strategy,
        trust_level=trust,
        declared_sandbox=declared_sandbox,
        declared_live_workspace=declared_live,
        declared_reference_corpus=declared_reference,
        declared_secret_area=declared_secret,
        approval_artifact_id=workspace_input.approval_artifact_id,
        approval_process_state_gate_id=workspace_input.approval_process_state_gate_id,
        proposed_patch_envelope_id=workspace_input.proposed_patch_envelope_id,
        safety_report_id=workspace_input.safety_report_id,
        human_review_packet_id=workspace_input.human_review_packet_id,
    )


def build_repair_workspace_root_ref_validation(**overrides: Any) -> RepairWorkspaceRootRefValidation:
    workspace_root_ref = overrides.get("workspace_root_ref", "sandbox/repair/v0392/workspace-candidate")
    normalized = overrides.get("normalized_root_ref", _normalize_root_ref(workspace_root_ref))
    markers = _root_ref_markers(workspace_root_ref)
    root_ref_declared_sandbox = overrides.get("root_ref_declared_sandbox", bool(normalized and "sandbox" in normalized.lower()))
    risky = markers["parent_traversal_like"] or markers["reference_corpus_like"] or markers["secret_path_like"] or markers["live_workspace_like"]
    valid = bool(markers["root_ref_present"] and root_ref_declared_sandbox and not risky)
    defaults = {
        "root_ref_validation_id": "v0392-root-ref-validation",
        "version": V0392_VERSION,
        "workspace_root_ref": workspace_root_ref,
        "normalized_root_ref": normalized,
        "root_ref_present": markers["root_ref_present"],
        "root_ref_declared_sandbox": root_ref_declared_sandbox,
        "absolute_path_like": markers["absolute_path_like"],
        "parent_traversal_like": markers["parent_traversal_like"],
        "reference_corpus_like": markers["reference_corpus_like"],
        "secret_path_like": markers["secret_path_like"],
        "live_workspace_like": markers["live_workspace_like"],
        "valid_for_future_patch_materialization_input": valid,
        "valid_for_future_sandbox_apply_input": valid,
        "validation_summary": "Workspace root reference is validated from supplied string metadata only.",
        "evidence_refs": ["workspace-root-ref"],
        "metadata": {"filesystem_read_performed": False},
    }
    return RepairWorkspaceRootRefValidation(**_with_overrides(defaults, overrides))


def validate_repair_workspace_root_ref_metadata(descriptor: RepairWorkspaceDescriptor) -> RepairWorkspaceRootRefValidation:
    return build_repair_workspace_root_ref_validation(
        workspace_root_ref=descriptor.workspace_root_ref,
        root_ref_declared_sandbox=descriptor.declared_sandbox,
    )


def build_repair_workspace_collision_prevention_plan(**overrides: Any) -> RepairWorkspaceCollisionPreventionPlan:
    defaults = {
        "collision_plan_id": "v0392-collision-plan",
        "version": V0392_VERSION,
        "strategy_kind": RepairWorkspaceIsolationStrategyKind.METADATA_ONLY_DECLARED_SANDBOX,
        "plan_summary": "Collision-prevention metadata blocks parallel write overlap and shared live target writes.",
        "parallel_agent_collision_blocked": True,
        "shared_live_workspace_write_blocked": True,
        "branch_collision_risk_mitigated": True,
        "evidence_refs": ["v0392-workspace-descriptor"],
    }
    return RepairWorkspaceCollisionPreventionPlan(**_with_overrides(defaults, overrides))


def create_repair_workspace_collision_prevention_plan(descriptor: RepairWorkspaceDescriptor) -> RepairWorkspaceCollisionPreventionPlan:
    return build_repair_workspace_collision_prevention_plan(strategy_kind=descriptor.isolation_strategy)


def build_repair_workspace_target_binding(**overrides: Any) -> RepairWorkspaceTargetBinding:
    defaults = {
        "target_binding_id": "v0392-target-binding",
        "version": V0392_VERSION,
        "workspace_descriptor_id": "v0392-workspace-descriptor",
        "proposed_patch_envelope_id": "patch-envelope-1",
        "approval_artifact_id": "v0391-approval-artifact",
        "safety_report_id": "safety-report-1",
        "target_summary": "Workspace target is bound to approved patch envelope, safety report, and human review metadata.",
        "target_bound_to_approved_patch": True,
        "target_bound_to_safety_report": True,
        "target_bound_to_human_review_packet": True,
        "target_scope_sandbox_only": True,
        "target_scope_live_apply": False,
        "binding_valid_for_future_materialization": True,
        "binding_valid_for_future_sandbox_apply": True,
        "evidence_refs": ["patch-envelope-1", "safety-report-1", "review-packet-1"],
    }
    return RepairWorkspaceTargetBinding(**_with_overrides(defaults, overrides))


def bind_repair_workspace_target(descriptor: RepairWorkspaceDescriptor) -> RepairWorkspaceTargetBinding:
    valid = descriptor.declared_sandbox and not any([descriptor.declared_live_workspace, descriptor.declared_reference_corpus, descriptor.declared_secret_area])
    return build_repair_workspace_target_binding(
        workspace_descriptor_id=descriptor.workspace_descriptor_id,
        proposed_patch_envelope_id=descriptor.proposed_patch_envelope_id,
        approval_artifact_id=descriptor.approval_artifact_id,
        safety_report_id=descriptor.safety_report_id,
        target_scope_sandbox_only=descriptor.declared_sandbox,
        target_scope_live_apply=descriptor.declared_live_workspace,
        binding_valid_for_future_materialization=valid,
        binding_valid_for_future_sandbox_apply=valid,
    )


def build_repair_workspace_live_boundary_check(**overrides: Any) -> RepairWorkspaceLiveBoundaryCheck:
    defaults = {
        "live_boundary_check_id": "v0392-live-boundary-check",
        "version": V0392_VERSION,
        "workspace_descriptor_id": "v0392-workspace-descriptor",
        "live_workspace_excluded": True,
        "live_workspace_read_blocked": True,
        "live_workspace_write_blocked": True,
        "live_workspace_apply_blocked": True,
        "reference_corpus_excluded": True,
        "secret_paths_excluded": True,
        "boundary_summary": "Live workspace, reference corpus, and secret path surfaces are excluded by metadata contract.",
        "evidence_refs": ["v0392-workspace-descriptor"],
    }
    return RepairWorkspaceLiveBoundaryCheck(**_with_overrides(defaults, overrides))


def check_repair_workspace_live_boundaries(descriptor: RepairWorkspaceDescriptor) -> RepairWorkspaceLiveBoundaryCheck:
    return build_repair_workspace_live_boundary_check(workspace_descriptor_id=descriptor.workspace_descriptor_id)


def build_repair_workspace_isolation_risk_assessment(**overrides: Any) -> RepairWorkspaceIsolationRiskAssessment:
    defaults = {
        "risk_assessment_id": "v0392-risk-assessment",
        "version": V0392_VERSION,
        "workspace_descriptor_id": "v0392-workspace-descriptor",
        "risk_kinds": [],
        "risk_summary": "No blocking workspace isolation risk identified for future input metadata.",
        "severity": "low",
        "blocks_future_patch_materialization_input": False,
        "blocks_future_sandbox_apply_input": False,
        "requires_human_review": False,
        "do_nothing_recommended": False,
        "evidence_refs": [],
    }
    return RepairWorkspaceIsolationRiskAssessment(**_with_overrides(defaults, overrides))


def assess_repair_workspace_isolation_risk(
    descriptor: RepairWorkspaceDescriptor,
    root_ref_validation: RepairWorkspaceRootRefValidation,
    target_binding: RepairWorkspaceTargetBinding,
) -> RepairWorkspaceIsolationRiskAssessment:
    risks: list[RepairWorkspaceIsolationRiskKind] = []
    if not descriptor.declared_sandbox:
        risks.append(RepairWorkspaceIsolationRiskKind.WORKSPACE_NOT_DECLARED_SANDBOX_RISK)
    if descriptor.declared_live_workspace or root_ref_validation.live_workspace_like or target_binding.target_scope_live_apply:
        risks.append(RepairWorkspaceIsolationRiskKind.LIVE_WORKSPACE_CONFUSION_RISK)
    if descriptor.declared_reference_corpus or root_ref_validation.reference_corpus_like:
        risks.append(RepairWorkspaceIsolationRiskKind.REFERENCE_CORPUS_CONFUSION_RISK)
    if descriptor.declared_secret_area or root_ref_validation.secret_path_like:
        risks.append(RepairWorkspaceIsolationRiskKind.SECRET_PATH_RISK)
    if root_ref_validation.parent_traversal_like:
        risks.append(RepairWorkspaceIsolationRiskKind.PATH_TRAVERSAL_RISK)
    if not descriptor.approval_process_state_gate_id:
        risks.append(RepairWorkspaceIsolationRiskKind.MISSING_APPROVAL_GATE_RISK)
    blocking = bool(risks)
    return build_repair_workspace_isolation_risk_assessment(
        workspace_descriptor_id=descriptor.workspace_descriptor_id,
        risk_kinds=risks,
        risk_summary="Workspace isolation has blocking future-input risk." if blocking else "No blocking workspace isolation risk identified for future input metadata.",
        severity="high" if blocking else "low",
        blocks_future_patch_materialization_input=blocking,
        blocks_future_sandbox_apply_input=blocking,
        requires_human_review=blocking,
        do_nothing_recommended=blocking,
    )


def build_repair_workspace_isolation_decision(**overrides: Any) -> RepairWorkspaceIsolationDecision:
    defaults = {
        "workspace_decision_id": "v0392-workspace-decision",
        "version": V0392_VERSION,
        "decision_kind": RepairWorkspaceIsolationDecisionKind.ALLOW_FUTURE_PATCH_MATERIALIZATION_INPUT,
        "status": RepairWorkspaceIsolationStatus.READY_FOR_FUTURE_PATCH_MATERIALIZATION,
        "readiness_level": RepairWorkspaceIsolationReadinessLevel.FUTURE_PATCH_MATERIALIZATION_INPUT_READY,
        "disposition": RepairWorkspaceDisposition.ACCEPTED_FOR_FUTURE_PATCH_MATERIALIZATION,
        "decision_summary": "Workspace isolation contract is ready for future patch_materialization input metadata only.",
        "rationale_summary": "The candidate is declared sandbox metadata with live/reference/secret exclusions and no runtime authority.",
        "confidence": "high",
        "evidence_refs": ["v0392-workspace-descriptor", "v0392-root-ref-validation", "v0392-target-binding"],
    }
    return RepairWorkspaceIsolationDecision(**_with_overrides(defaults, overrides))


def decide_repair_workspace_isolation(
    descriptor: RepairWorkspaceDescriptor,
    root_ref_validation: RepairWorkspaceRootRefValidation,
    target_binding: RepairWorkspaceTargetBinding,
    risk_assessment: RepairWorkspaceIsolationRiskAssessment,
) -> RepairWorkspaceIsolationDecision:
    allowed = (
        descriptor.declared_sandbox
        and root_ref_validation.valid_for_future_patch_materialization_input
        and target_binding.binding_valid_for_future_materialization
        and not risk_assessment.blocks_future_patch_materialization_input
    )
    return build_repair_workspace_isolation_decision(
        decision_kind=RepairWorkspaceIsolationDecisionKind.ALLOW_FUTURE_PATCH_MATERIALIZATION_INPUT if allowed else RepairWorkspaceIsolationDecisionKind.REQUIRE_REVIEW,
        status=RepairWorkspaceIsolationStatus.READY_FOR_FUTURE_PATCH_MATERIALIZATION if allowed else RepairWorkspaceIsolationStatus.REVIEW_REQUIRED,
        readiness_level=RepairWorkspaceIsolationReadinessLevel.FUTURE_PATCH_MATERIALIZATION_INPUT_READY if allowed else RepairWorkspaceIsolationReadinessLevel.NOT_READY,
        disposition=RepairWorkspaceDisposition.ACCEPTED_FOR_FUTURE_PATCH_MATERIALIZATION if allowed else RepairWorkspaceDisposition.REVIEW_REQUIRED,
        ready_for_future_patch_materialization_input=allowed,
        ready_for_future_sandbox_apply_input=allowed and root_ref_validation.valid_for_future_sandbox_apply_input and target_binding.binding_valid_for_future_sandbox_apply,
        confidence="high" if allowed else "low",
    )


def build_repair_workspace_isolation_validation_finding(**overrides: Any) -> RepairWorkspaceIsolationValidationFinding:
    defaults = {
        "finding_id": "v0392-validation-finding",
        "finding_summary": "Workspace isolation contract remains metadata-only and grants no mutation or apply permission.",
        "risk_kind": RepairWorkspaceIsolationRiskKind.FILESYSTEM_MUTATION_CONFUSION_RISK,
        "blocked": True,
    }
    return RepairWorkspaceIsolationValidationFinding(**_with_overrides(defaults, overrides))


def build_repair_workspace_isolation_validation_report(**overrides: Any) -> RepairWorkspaceIsolationValidationReport:
    defaults = {
        "validation_report_id": "v0392-validation-report",
        "version": V0392_VERSION,
        "validation_summary": "Validation confirms metadata-only workspace isolation contract and no mutation.",
        "findings": [build_repair_workspace_isolation_validation_finding()],
    }
    return RepairWorkspaceIsolationValidationReport(**_with_overrides(defaults, overrides))


def build_repair_workspace_isolation_run_preview(**overrides: Any) -> RepairWorkspaceIsolationRunPreview:
    defaults = {
        "run_preview_id": "v0392-run-preview",
        "version": V0392_VERSION,
        "preview_summary": "Preview workspace isolation contract metadata without mutation or runtime authority.",
        "preview_steps": [
            "WorkspaceIsolationInput",
            "WorkspaceDescriptor",
            "RootRefValidation",
            "CollisionPreventionPlan",
            "TargetBinding",
            "LiveBoundaryCheck",
            "RiskAssessment",
            "WorkspaceIsolationDecision",
        ],
    }
    return RepairWorkspaceIsolationRunPreview(**_with_overrides(defaults, overrides))


def build_repair_workspace_isolation_no_mutation_guarantee(**overrides: Any) -> RepairWorkspaceIsolationNoMutationGuarantee:
    defaults = {
        "guarantee_id": "v0392-no-mutation-guarantee",
        "version": V0392_VERSION,
        "guarantee_summary": "v0.39.2 workspace isolation contract does not create, read, write, apply, test, or execute.",
    }
    return RepairWorkspaceIsolationNoMutationGuarantee(**_with_overrides(defaults, overrides))


def build_v0392_readiness_report(**overrides: Any) -> V0392ReadinessReport:
    workspace_input = overrides.pop("workspace_input", build_repair_workspace_isolation_input())
    descriptor = classify_repair_workspace_descriptor(workspace_input)
    root_validation = validate_repair_workspace_root_ref_metadata(descriptor)
    collision = create_repair_workspace_collision_prevention_plan(descriptor)
    target = bind_repair_workspace_target(descriptor)
    live_check = check_repair_workspace_live_boundaries(descriptor)
    risk = assess_repair_workspace_isolation_risk(descriptor, root_validation, target)
    decision = decide_repair_workspace_isolation(descriptor, root_validation, target, risk)
    defaults = {
        "report_id": "v0392-readiness-report",
        "version": V0392_VERSION,
        "release_name": V0392_RELEASE_NAME,
        "track_name": V039_TRACK_NAME,
        "workspace_descriptor": descriptor,
        "root_ref_validation": root_validation,
        "collision_prevention_plan": collision,
        "target_binding": target,
        "live_boundary_check": live_check,
        "risk_assessment": risk,
        "decision": decision,
        "flags": build_repair_workspace_isolation_flags(),
        "source_refs": [build_repair_workspace_isolation_source_ref()],
        "report_summary": "v0.39.2 workspace isolation contract is ready as future v0.39.3 input metadata only.",
    }
    return V0392ReadinessReport(**_with_overrides(defaults, overrides))


def repair_workspace_isolation_flags_preserve_no_mutation(flags: RepairWorkspaceIsolationFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_FLAG_NAMES)


def repair_workspace_policy_blocks_creation_apply_and_execution(policy: RepairWorkspaceIsolationPolicy) -> bool:
    return all(getattr(policy, name) is False for name in UNSAFE_POLICY_ALLOW_NAMES)


def repair_workspace_descriptor_is_metadata_only(descriptor: RepairWorkspaceDescriptor) -> bool:
    return bool(descriptor.descriptor_summary and descriptor.version and V0392_VERSION in descriptor.version)


def repair_workspace_root_ref_validation_does_not_read_files(validation: RepairWorkspaceRootRefValidation) -> bool:
    return validation.metadata.get("filesystem_read_performed") is False


def repair_workspace_decision_is_not_apply_permission(decision: RepairWorkspaceIsolationDecision) -> bool:
    return all(getattr(decision, name) is False for name in UNSAFE_DECISION_NAMES)


def v0392_readiness_report_is_not_execution_ready(report: V0392ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_REPORT_NAMES) and repair_workspace_isolation_flags_preserve_no_mutation(report.flags)
