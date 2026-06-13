"""v0.39.1 approval artifact intake and authenticity gate metadata.

This module is intentionally limited to pure in-memory metadata construction.
It does not grant approval, grant apply permission, create workspaces,
materialize patches, apply patches, run tests, invoke providers, invoke
subagents, execute self-prompts, or grant runtime authority.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank


V0391_VERSION = "v0.39.1"
V0391_RELEASE_NAME = "v0.39.1 Approval Artifact Intake & Authenticity Gate"
V039_TRACK_NAME = "Human-approved Sandbox Repair Apply & Re-test Loop with PI-native Self-Prompting Mission Loop Boundary"

PROHIBITED_RUNTIME_ACTIONS = [
    "approval grant",
    "apply permission",
    "sandbox apply",
    "live apply",
    "patch write",
    "apply_patch",
    "git apply",
    "test execution",
    "self-prompt execution",
    "subagent invocation",
    "model provider",
    "external agent",
    "Dominion",
]


class RepairApprovalArtifactMode(StrEnum):
    APPROVAL_ARTIFACT_INTAKE = "approval_artifact_intake"
    APPROVAL_ARTIFACT_SCHEMA_VALIDATION = "approval_artifact_schema_validation"
    APPROVAL_ARTIFACT_AUTHENTICITY_GATE = "approval_artifact_authenticity_gate"
    APPROVAL_SCOPE_VALIDATION = "approval_scope_validation"
    APPROVAL_EXPIRATION_VALIDATION = "approval_expiration_validation"
    APPROVAL_REVIEWER_IDENTITY_METADATA = "approval_reviewer_identity_metadata"
    APPROVAL_PATCH_ENVELOPE_BINDING = "approval_patch_envelope_binding"
    APPROVAL_SAFETY_REPORT_BINDING = "approval_safety_report_binding"
    APPROVAL_REVIEW_PACKET_BINDING = "approval_review_packet_binding"
    APPROVAL_PROCESS_STATE_TRANSITION_GATE = "approval_process_state_transition_gate"
    FUTURE_SANDBOX_WORKSPACE_ISOLATION_INPUT = "future_sandbox_workspace_isolation_input"
    FUTURE_SANDBOX_APPLY_PRECONDITION_INPUT = "future_sandbox_apply_precondition_input"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairApprovalArtifactSourceKind(StrEnum):
    V0390_REPAIR_APPLY_BOUNDARY = "v0390_repair_apply_boundary"
    V0389_HANDOFF_PACKET = "v0389_handoff_packet"
    V0389_CONSOLIDATION_REPORT = "v0389_consolidation_report"
    V0386_HUMAN_REVIEW_PACKET = "v0386_human_review_packet"
    V0386_APPROVAL_REQUEST_CONTRACT = "v0386_approval_request_contract"
    V0385_SAFETY_REPORT = "v0385_safety_report"
    V0384_PROPOSED_PATCH_ENVELOPE = "v0384_proposed_patch_envelope"
    V0383_SCOPE_PLAN = "v0383_scope_plan"
    MANUAL_HUMAN_APPROVAL_NOTE = "manual_human_approval_note"
    OPERATOR_SUPPLIED_APPROVAL_ARTIFACT = "operator_supplied_approval_artifact"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class RepairApprovalArtifactStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    RECEIVED = "received"
    SCHEMA_VALIDATED = "schema_validated"
    AUTHENTICITY_ASSESSED = "authenticity_assessed"
    SCOPE_VALIDATED = "scope_validated"
    EXPIRATION_VALIDATED = "expiration_validated"
    BOUND_TO_REVIEW_PACKET = "bound_to_review_packet"
    BOUND_TO_SAFETY_REPORT = "bound_to_safety_report"
    BOUND_TO_PATCH_ENVELOPE = "bound_to_patch_envelope"
    PROCESS_STATE_GATE_CREATED = "process_state_gate_created"
    READY_FOR_FUTURE_WORKSPACE_ISOLATION = "ready_for_future_workspace_isolation"
    READY_FOR_FUTURE_SANDBOX_APPLY_PRECONDITION = "ready_for_future_sandbox_apply_precondition"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    EXPIRED = "expired"
    REVIEW_REQUIRED = "review_required"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class RepairApprovalArtifactReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    APPROVAL_INTAKE_READY = "approval_intake_ready"
    SCHEMA_VALIDATION_READY = "schema_validation_ready"
    AUTHENTICITY_GATE_READY = "authenticity_gate_ready"
    SCOPE_VALIDATION_READY = "scope_validation_ready"
    EXPIRATION_VALIDATION_READY = "expiration_validation_ready"
    REVIEW_PACKET_BINDING_READY = "review_packet_binding_ready"
    SAFETY_REPORT_BINDING_READY = "safety_report_binding_ready"
    PATCH_ENVELOPE_BINDING_READY = "patch_envelope_binding_ready"
    PROCESS_STATE_TRANSITION_GATE_READY = "process_state_transition_gate_ready"
    FUTURE_WORKSPACE_ISOLATION_INPUT_READY = "future_workspace_isolation_input_ready"
    FUTURE_SANDBOX_APPLY_PRECONDITION_INPUT_READY = "future_sandbox_apply_precondition_input_ready"
    DESIGN_HANDOFF_READY_FOR_V0392 = "design_handoff_ready_for_v0392"
    DESIGN_HANDOFF_READY_FOR_V0393 = "design_handoff_ready_for_v0393"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class RepairApprovalArtifactDecisionKind(StrEnum):
    ALLOW_APPROVAL_ARTIFACT_INTAKE = "allow_approval_artifact_intake"
    ALLOW_SCHEMA_VALIDATION = "allow_schema_validation"
    ALLOW_AUTHENTICITY_ASSESSMENT = "allow_authenticity_assessment"
    ALLOW_SCOPE_VALIDATION = "allow_scope_validation"
    ALLOW_EXPIRATION_VALIDATION = "allow_expiration_validation"
    ALLOW_REVIEW_PACKET_BINDING = "allow_review_packet_binding"
    ALLOW_SAFETY_REPORT_BINDING = "allow_safety_report_binding"
    ALLOW_PATCH_ENVELOPE_BINDING = "allow_patch_envelope_binding"
    ALLOW_PROCESS_STATE_TRANSITION_GATE = "allow_process_state_transition_gate"
    ALLOW_FUTURE_WORKSPACE_ISOLATION_INPUT = "allow_future_workspace_isolation_input"
    ALLOW_FUTURE_SANDBOX_APPLY_PRECONDITION_INPUT = "allow_future_sandbox_apply_precondition_input"
    CHOOSE_DO_NOTHING = "choose_do_nothing"
    CHOOSE_HUMAN_REVIEW_REQUIRED = "choose_human_review_required"
    DENY = "deny"
    BLOCK = "block"
    REJECT_EXPIRED = "reject_expired"
    REJECT_SCOPE_MISMATCH = "reject_scope_mismatch"
    REJECT_MISSING_BINDING = "reject_missing_binding"
    REJECT_UNSAFE_PATCH = "reject_unsafe_patch"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class RepairApprovalArtifactRiskKind(StrEnum):
    APPROVAL_ARTIFACT_MISSING_RISK = "approval_artifact_missing_risk"
    APPROVAL_ARTIFACT_MALFORMED_RISK = "approval_artifact_malformed_risk"
    APPROVAL_AUTHENTICITY_UNCERTAIN_RISK = "approval_authenticity_uncertain_risk"
    REVIEWER_IDENTITY_UNKNOWN_RISK = "reviewer_identity_unknown_risk"
    REVIEWER_AUTHORITY_UNKNOWN_RISK = "reviewer_authority_unknown_risk"
    APPROVAL_EXPIRED_RISK = "approval_expired_risk"
    APPROVAL_SCOPE_MISMATCH_RISK = "approval_scope_mismatch_risk"
    PATCH_ENVELOPE_BINDING_MISSING_RISK = "patch_envelope_binding_missing_risk"
    SAFETY_REPORT_BINDING_MISSING_RISK = "safety_report_binding_missing_risk"
    REVIEW_PACKET_BINDING_MISSING_RISK = "review_packet_binding_missing_risk"
    APPROVAL_REPLAY_RISK = "approval_replay_risk"
    APPROVAL_OVERBROAD_SCOPE_RISK = "approval_overbroad_scope_risk"
    APPROVAL_FOR_LIVE_APPLY_RISK = "approval_for_live_apply_risk"
    APPLY_PERMISSION_CONFUSION_RISK = "apply_permission_confusion_risk"
    APPROVAL_GRANT_CONFUSION_RISK = "approval_grant_confusion_risk"
    SANDBOX_APPLY_CONFUSION_RISK = "sandbox_apply_confusion_risk"
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


class RepairApprovalArtifactKind(StrEnum):
    EXPLICIT_HUMAN_APPROVAL_TEXT = "explicit_human_approval_text"
    SIGNED_TEXT_METADATA = "signed_text_metadata"
    REVIEWER_ATTESTATION_METADATA = "reviewer_attestation_metadata"
    REVIEW_PACKET_ATTACHED_APPROVAL = "review_packet_attached_approval"
    APPROVAL_REQUEST_RESPONSE_METADATA = "approval_request_response_metadata"
    MANUAL_OPERATOR_NOTE = "manual_operator_note"
    TEST_FIXTURE_APPROVAL = "test_fixture_approval"
    INVALID_ARTIFACT = "invalid_artifact"
    UNKNOWN = "unknown"


class RepairApprovalScopeKind(StrEnum):
    PROPOSED_PATCH_ENVELOPE_SCOPE = "proposed_patch_envelope_scope"
    PROPOSED_FILE_CHANGE_SCOPE = "proposed_file_change_scope"
    PROPOSED_HUNK_SCOPE = "proposed_hunk_scope"
    SAFETY_VALIDATED_PATCH_SCOPE = "safety_validated_patch_scope"
    HUMAN_REVIEW_PACKET_SCOPE = "human_review_packet_scope"
    SANDBOX_APPLY_FUTURE_SCOPE = "sandbox_apply_future_scope"
    LIVE_APPLY_FORBIDDEN_SCOPE = "live_apply_forbidden_scope"
    UNKNOWN = "unknown"


class RepairApprovalAuthenticitySignalKind(StrEnum):
    REVIEWER_ID_PRESENT = "reviewer_id_present"
    REVIEWER_ROLE_PRESENT = "reviewer_role_present"
    APPROVAL_PHRASE_PRESENT = "approval_phrase_present"
    APPROVAL_TIMESTAMP_PRESENT = "approval_timestamp_present"
    APPROVAL_NONCE_PRESENT = "approval_nonce_present"
    APPROVAL_ARTIFACT_DIGEST_PRESENT = "approval_artifact_digest_present"
    APPROVAL_SCOPE_PRESENT = "approval_scope_present"
    PATCH_ENVELOPE_REF_PRESENT = "patch_envelope_ref_present"
    REVIEW_PACKET_REF_PRESENT = "review_packet_ref_present"
    SAFETY_REPORT_REF_PRESENT = "safety_report_ref_present"
    MISSING_REVIEWER_ID = "missing_reviewer_id"
    MISSING_APPROVAL_PHRASE = "missing_approval_phrase"
    MISSING_TIMESTAMP = "missing_timestamp"
    MISSING_SCOPE = "missing_scope"
    MISSING_PATCH_BINDING = "missing_patch_binding"
    SUSPICIOUS_OR_INCOMPLETE = "suspicious_or_incomplete"
    UNKNOWN = "unknown"


class RepairApprovalExpirationStatus(StrEnum):
    NOT_EVALUATED = "not_evaluated"
    FRESH = "fresh"
    NEAR_EXPIRY = "near_expiry"
    EXPIRED = "expired"
    MISSING_TIMESTAMP = "missing_timestamp"
    MISSING_EXPIRATION_POLICY = "missing_expiration_policy"
    INVALID_TIMESTAMP = "invalid_timestamp"
    UNKNOWN = "unknown"


class RepairApprovalDisposition(StrEnum):
    ACCEPTED_FOR_FUTURE_GATE = "accepted_for_future_gate"
    ACCEPTED_WITH_WARNINGS = "accepted_with_warnings"
    REVIEW_REQUIRED = "review_required"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    EXPIRED = "expired"
    SCOPE_MISMATCH = "scope_mismatch"
    DO_NOTHING_PREFERRED = "do_nothing_preferred"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairApprovalConfidenceLevel(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INCONCLUSIVE = "inconclusive"
    UNKNOWN = "unknown"


SAFE_FLAG_NAMES = [
    "approval_artifact_layer_constructed",
    "approval_artifact_intake_available",
    "approval_schema_validation_available",
    "approval_authenticity_gate_available",
    "approval_scope_validation_available",
    "approval_expiration_validation_available",
    "approval_reviewer_identity_metadata_available",
    "approval_patch_envelope_binding_available",
    "approval_safety_report_binding_available",
    "approval_review_packet_binding_available",
    "approval_process_state_transition_gate_available",
    "ready_for_v0392_sandbox_workspace_isolation",
    "ready_for_v0393_human_approved_patch_materialization_sandbox_apply",
    "ready_for_approval_artifact_intake",
    "ready_for_approval_artifact_schema_validation",
    "ready_for_approval_authenticity_assessment",
    "ready_for_approval_scope_validation",
    "ready_for_approval_expiration_validation",
    "ready_for_approval_reviewer_identity_metadata",
    "ready_for_approval_patch_envelope_binding",
    "ready_for_approval_safety_report_binding",
    "ready_for_approval_review_packet_binding",
    "ready_for_approval_process_state_transition_gate",
    "ready_for_future_sandbox_workspace_isolation_input",
    "ready_for_future_sandbox_apply_precondition_input",
]

UNSAFE_FLAG_NAMES = [
    "ready_for_execution",
    "ready_for_general_execution",
    "ready_for_human_approval_capture",
    "ready_for_approval_grant",
    "ready_for_apply_permission",
    "ready_for_sandbox_repair_workspace_creation",
    "ready_for_sandbox_patch_materialization",
    "ready_for_sandbox_repair_apply",
    "ready_for_live_workspace_apply",
    "ready_for_live_workspace_write",
    "ready_for_source_file_write",
    "ready_for_sandbox_source_write",
    "ready_for_patch_file_write",
    "ready_for_file_edit",
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
    "allow_human_approval_capture",
    "allow_approval_grant",
    "allow_apply_permission",
    "allow_sandbox_workspace_creation",
    "allow_sandbox_patch_materialization",
    "allow_sandbox_repair_apply",
    "allow_live_workspace_apply",
    "allow_live_workspace_write",
    "allow_patch_file_write",
    "allow_file_edit",
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

UNSAFE_ARTIFACT_NAMES = [
    "approval_granted",
    "approval_captured_now",
    "apply_permission_granted",
    "sandbox_apply_allowed_now",
    "live_apply_allowed_now",
    "repair_execution_allowed_now",
]

UNSAFE_DECISION_NAMES = [
    "approval_granted_now",
    "approval_capture_allowed_now",
    "apply_permission_allowed_now",
    "sandbox_apply_allowed_now",
    "live_apply_allowed_now",
    "patch_materialization_allowed_now",
    "test_execution_allowed_now",
    "self_prompt_execution_allowed_now",
    "subagent_invocation_allowed_now",
    "model_provider_invocation_allowed_now",
    "external_agent_allowed_now",
    "repair_execution_allowed_now",
    "production_certified",
]

UNSAFE_REPORT_NAMES = [
    "approval_granted_now",
    "approval_capture_enabled",
    "apply_permission_enabled",
    "sandbox_workspace_creation_enabled",
    "patch_materialization_enabled",
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


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0391_VERSION not in version:
        raise ValueError("version must include v0.39.1")


def _validate_list(name: str, value: list[Any]) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{name} must be a list")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a dict")


def _validate_false(instance: Any, names: list[str]) -> None:
    for name in names:
        if getattr(instance, name):
            raise ValueError(f"{name} must remain false in v0.39.1")


def _validate_non_negative(name: str, value: int) -> None:
    if value < 0:
        raise ValueError(f"{name} must be >= 0")


def _with_overrides(defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    merged.update(overrides)
    return merged


def _text_digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class RepairApprovalArtifactFlagSet:
    flag_set_id: str
    version: str = V0391_VERSION
    approval_artifact_layer_constructed: bool = True
    approval_artifact_intake_available: bool = True
    approval_schema_validation_available: bool = True
    approval_authenticity_gate_available: bool = True
    approval_scope_validation_available: bool = True
    approval_expiration_validation_available: bool = True
    approval_reviewer_identity_metadata_available: bool = True
    approval_patch_envelope_binding_available: bool = True
    approval_safety_report_binding_available: bool = True
    approval_review_packet_binding_available: bool = True
    approval_process_state_transition_gate_available: bool = True
    ready_for_v0392_sandbox_workspace_isolation: bool = True
    ready_for_v0393_human_approved_patch_materialization_sandbox_apply: bool = True
    ready_for_approval_artifact_intake: bool = True
    ready_for_approval_artifact_schema_validation: bool = True
    ready_for_approval_authenticity_assessment: bool = True
    ready_for_approval_scope_validation: bool = True
    ready_for_approval_expiration_validation: bool = True
    ready_for_approval_reviewer_identity_metadata: bool = True
    ready_for_approval_patch_envelope_binding: bool = True
    ready_for_approval_safety_report_binding: bool = True
    ready_for_approval_review_packet_binding: bool = True
    ready_for_approval_process_state_transition_gate: bool = True
    ready_for_future_sandbox_workspace_isolation_input: bool = True
    ready_for_future_sandbox_apply_precondition_input: bool = True
    ready_for_execution: bool = False
    ready_for_general_execution: bool = False
    ready_for_human_approval_capture: bool = False
    ready_for_approval_grant: bool = False
    ready_for_apply_permission: bool = False
    ready_for_sandbox_repair_workspace_creation: bool = False
    ready_for_sandbox_patch_materialization: bool = False
    ready_for_sandbox_repair_apply: bool = False
    ready_for_live_workspace_apply: bool = False
    ready_for_live_workspace_write: bool = False
    ready_for_source_file_write: bool = False
    ready_for_sandbox_source_write: bool = False
    ready_for_patch_file_write: bool = False
    ready_for_file_edit: bool = False
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
        _validate_false(self, UNSAFE_FLAG_NAMES)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairApprovalArtifactSourceRef:
    source_ref_id: str
    source_kind: RepairApprovalArtifactSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairApprovalArtifactPolicy:
    policy_id: str
    version: str
    allowed_modes: list[RepairApprovalArtifactMode | str]
    allowed_artifact_kinds: list[RepairApprovalArtifactKind | str]
    allowed_scope_kinds: list[RepairApprovalScopeKind | str]
    required_authenticity_signals: list[RepairApprovalAuthenticitySignalKind | str]
    max_artifact_text_chars: int = 4096
    max_scope_refs: int = 128
    default_expiration_minutes: int = 1440
    require_reviewer_id: bool = True
    require_reviewer_role: bool = True
    require_approval_phrase: bool = True
    require_approval_timestamp: bool = True
    require_patch_envelope_binding: bool = True
    require_review_packet_binding: bool = True
    require_safety_report_binding: bool = True
    require_sandbox_only_scope: bool = True
    reject_live_apply_scope: bool = True
    reject_expired_artifact: bool = True
    reject_missing_patch_binding: bool = True
    reject_missing_safety_binding: bool = True
    reject_missing_review_binding: bool = True
    allow_approval_artifact_intake: bool = True
    allow_schema_validation: bool = True
    allow_authenticity_assessment: bool = True
    allow_scope_validation: bool = True
    allow_expiration_validation: bool = True
    allow_reviewer_identity_metadata: bool = True
    allow_patch_envelope_binding: bool = True
    allow_safety_report_binding: bool = True
    allow_review_packet_binding: bool = True
    allow_process_state_transition_gate: bool = True
    allow_future_workspace_isolation_input: bool = True
    allow_future_sandbox_apply_precondition_input: bool = True
    allow_human_approval_capture: bool = False
    allow_approval_grant: bool = False
    allow_apply_permission: bool = False
    allow_sandbox_workspace_creation: bool = False
    allow_sandbox_patch_materialization: bool = False
    allow_sandbox_repair_apply: bool = False
    allow_live_workspace_apply: bool = False
    allow_live_workspace_write: bool = False
    allow_patch_file_write: bool = False
    allow_file_edit: bool = False
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
        for name in ("allowed_modes", "allowed_artifact_kinds", "allowed_scope_kinds", "required_authenticity_signals"):
            _validate_list(name, getattr(self, name))
        for name in ("max_artifact_text_chars", "max_scope_refs", "default_expiration_minutes"):
            _validate_non_negative(name, getattr(self, name))
        _validate_false(self, UNSAFE_POLICY_ALLOW_NAMES)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairApprovalArtifactInput:
    approval_input_id: str
    version: str
    artifact_kind: RepairApprovalArtifactKind | str
    raw_approval_text: str
    reviewer_id: str | None
    reviewer_role: str | None
    approval_phrase: str | None
    approval_timestamp: str | None
    expiration_timestamp: str | None
    approval_nonce: str | None
    approval_scope_summary: str
    proposed_patch_envelope_id: str | None
    safety_report_id: str | None
    human_review_packet_id: str | None
    approval_request_contract_id: str | None
    source_refs: list[RepairApprovalArtifactSourceRef]
    prohibited_runtime_actions: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("approval_input_id", self.approval_input_id)
        _validate_version(self.version)
        _require_non_blank("approval_scope_summary", self.approval_scope_summary)
        _validate_list("source_refs", self.source_refs)
        _validate_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        missing = [item for item in PROHIBITED_RUNTIME_ACTIONS if item not in self.prohibited_runtime_actions]
        if missing:
            raise ValueError(f"prohibited_runtime_actions missing required entries: {missing}")
        if len(self.raw_approval_text) > 4096:
            raise ValueError("raw_approval_text must be bounded")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairApprovalArtifact:
    approval_artifact_id: str
    version: str
    artifact_kind: RepairApprovalArtifactKind | str
    status: RepairApprovalArtifactStatus | str
    disposition: RepairApprovalDisposition | str
    raw_approval_text_preview: str
    normalized_approval_summary: str
    reviewer_id: str | None
    reviewer_role: str | None
    approval_phrase_present: bool
    approval_timestamp: str | None
    expiration_timestamp: str | None
    approval_nonce: str | None
    artifact_digest: str | None
    bounded: bool
    redacted: bool
    source_refs: list[RepairApprovalArtifactSourceRef]
    human_approval_artifact_present: bool = True
    approval_artifact_received: bool = True
    approval_granted: bool = False
    approval_captured_now: bool = False
    apply_permission_granted: bool = False
    sandbox_apply_allowed_now: bool = False
    live_apply_allowed_now: bool = False
    repair_execution_allowed_now: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("approval_artifact_id", self.approval_artifact_id)
        _validate_version(self.version)
        _require_non_blank("normalized_approval_summary", self.normalized_approval_summary)
        if len(self.raw_approval_text_preview) > 512:
            raise ValueError("raw_approval_text_preview must be bounded")
        if not self.bounded or not self.redacted:
            raise ValueError("raw_approval_text_preview must be bounded/redacted")
        _validate_list("source_refs", self.source_refs)
        _validate_false(self, UNSAFE_ARTIFACT_NAMES)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairApprovalScopeBinding:
    scope_binding_id: str
    version: str
    approval_artifact_id: str
    scope_kind: RepairApprovalScopeKind | str
    proposed_patch_envelope_id: str | None
    safety_report_id: str | None
    human_review_packet_id: str | None
    approved_file_scope_refs: list[str]
    approved_hunk_scope_refs: list[str]
    denied_scope_refs: list[str]
    sandbox_only_scope: bool
    live_apply_scope_requested: bool
    scope_valid: bool
    scope_summary: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("scope_binding_id", self.scope_binding_id)
        _validate_version(self.version)
        _require_non_blank("approval_artifact_id", self.approval_artifact_id)
        _require_non_blank("scope_summary", self.scope_summary)
        for name in ("approved_file_scope_refs", "approved_hunk_scope_refs", "denied_scope_refs", "evidence_refs"):
            _validate_list(name, getattr(self, name))
        if self.live_apply_scope_requested and self.scope_valid:
            raise ValueError("live apply scope must force scope_valid false")
        if self.scope_valid and not self.sandbox_only_scope:
            raise ValueError("sandbox_only_scope must be true for future apply eligibility")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairApprovalAuthenticityAssessment:
    authenticity_assessment_id: str
    version: str
    approval_artifact_id: str
    authenticity_signals: list[RepairApprovalAuthenticitySignalKind | str]
    missing_signals: list[RepairApprovalAuthenticitySignalKind | str]
    authenticity_summary: str
    reviewer_id_present: bool
    reviewer_role_present: bool
    approval_phrase_present: bool
    timestamp_present: bool
    nonce_present: bool
    digest_present: bool
    authenticity_confidence: RepairApprovalConfidenceLevel | str
    authenticity_sufficient_for_future_gate: bool
    external_identity_verified: bool = False
    cryptographic_signature_verified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("authenticity_assessment_id", self.authenticity_assessment_id)
        _validate_version(self.version)
        _require_non_blank("approval_artifact_id", self.approval_artifact_id)
        _require_non_blank("authenticity_summary", self.authenticity_summary)
        _validate_list("authenticity_signals", self.authenticity_signals)
        _validate_list("missing_signals", self.missing_signals)
        _validate_false(self, ["external_identity_verified"])
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairApprovalExpirationAssessment:
    expiration_assessment_id: str
    version: str
    approval_artifact_id: str
    expiration_status: RepairApprovalExpirationStatus | str
    approval_timestamp: str | None
    expiration_timestamp: str | None
    evaluated_at: str | None
    expiration_summary: str
    fresh_for_future_gate: bool
    expired: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("expiration_assessment_id", self.expiration_assessment_id)
        _validate_version(self.version)
        _require_non_blank("approval_artifact_id", self.approval_artifact_id)
        _require_non_blank("expiration_summary", self.expiration_summary)
        if self.expired and self.fresh_for_future_gate:
            raise ValueError("expired approval cannot be fresh_for_future_gate")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairApprovalPatchBindingAssessment:
    patch_binding_assessment_id: str
    version: str
    approval_artifact_id: str
    proposed_patch_envelope_id: str | None
    safety_report_id: str | None
    human_review_packet_id: str | None
    approval_request_contract_id: str | None
    patch_binding_present: bool
    safety_binding_present: bool
    review_packet_binding_present: bool
    binding_consistent: bool
    binding_summary: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("patch_binding_assessment_id", self.patch_binding_assessment_id)
        _validate_version(self.version)
        _require_non_blank("approval_artifact_id", self.approval_artifact_id)
        _require_non_blank("binding_summary", self.binding_summary)
        _validate_list("evidence_refs", self.evidence_refs)
        if self.binding_consistent and not (self.patch_binding_present and self.safety_binding_present and self.review_packet_binding_present):
            raise ValueError("binding_consistent must be false when required bindings are missing")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairApprovalProcessStateGate:
    process_state_gate_id: str
    version: str
    approval_artifact_id: str
    prior_state: str
    candidate_next_state: str
    transition_summary: str
    gate_satisfied: bool
    future_workspace_isolation_eligible: bool
    future_sandbox_apply_precondition_satisfied: bool
    process_state_authority_granted: bool = False
    runtime_authority_granted: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("process_state_gate_id", "version", "approval_artifact_id", "prior_state", "candidate_next_state", "transition_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_false(self, ["process_state_authority_granted", "runtime_authority_granted"])
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairApprovalRiskAssessment:
    risk_assessment_id: str
    version: str
    approval_artifact_id: str
    risk_kinds: list[RepairApprovalArtifactRiskKind | str]
    risk_summary: str
    severity: str
    blocks_future_workspace_isolation: bool
    blocks_future_sandbox_apply_precondition: bool
    requires_human_review: bool
    do_nothing_recommended: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("risk_assessment_id", "version", "approval_artifact_id", "risk_summary", "severity"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("risk_kinds", self.risk_kinds)
        _validate_list("evidence_refs", self.evidence_refs)
        high_risks = {
            RepairApprovalArtifactRiskKind.APPLY_PERMISSION_CONFUSION_RISK.value,
            RepairApprovalArtifactRiskKind.APPROVAL_GRANT_CONFUSION_RISK.value,
            RepairApprovalArtifactRiskKind.APPROVAL_FOR_LIVE_APPLY_RISK.value,
        }
        risk_values = {str(item) for item in self.risk_kinds}
        if risk_values.intersection(high_risks) and not (self.blocks_future_sandbox_apply_precondition or self.requires_human_review):
            raise ValueError("high-risk approval confusion should block or require review")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairApprovalArtifactDecision:
    approval_decision_id: str
    version: str
    approval_artifact_id: str | None
    decision_kind: RepairApprovalArtifactDecisionKind | str
    status: RepairApprovalArtifactStatus | str
    disposition: RepairApprovalDisposition | str
    readiness_level: RepairApprovalArtifactReadinessLevel | str
    decision_summary: str
    rationale_summary: str
    confidence: RepairApprovalConfidenceLevel | str
    evidence_refs: list[str]
    ready_for_future_workspace_isolation_input: bool
    ready_for_future_sandbox_apply_precondition_input: bool
    approval_artifact_valid_for_future_gate: bool
    approval_granted_now: bool = False
    approval_capture_allowed_now: bool = False
    apply_permission_allowed_now: bool = False
    sandbox_apply_allowed_now: bool = False
    live_apply_allowed_now: bool = False
    patch_materialization_allowed_now: bool = False
    test_execution_allowed_now: bool = False
    self_prompt_execution_allowed_now: bool = False
    subagent_invocation_allowed_now: bool = False
    model_provider_invocation_allowed_now: bool = False
    external_agent_allowed_now: bool = False
    repair_execution_allowed_now: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("approval_decision_id", "version", "decision_summary", "rationale_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_false(self, UNSAFE_DECISION_NAMES)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairApprovalArtifactValidationFinding:
    finding_id: str
    finding_summary: str
    risk_kind: RepairApprovalArtifactRiskKind | str
    blocked: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("finding_summary", self.finding_summary)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairApprovalArtifactValidationReport:
    validation_report_id: str
    version: str
    validation_summary: str
    findings: list[RepairApprovalArtifactValidationFinding]
    artifact_intake_confirmed: bool = True
    schema_validation_confirmed: bool = True
    authenticity_assessment_confirmed: bool = True
    scope_validation_confirmed: bool = True
    freshness_validation_confirmed: bool = True
    no_approval_grant_confirmed: bool = True
    no_apply_confirmed: bool = True
    no_sandbox_workspace_creation_confirmed: bool = True
    no_patch_materialization_confirmed: bool = True
    no_patch_application_confirmed: bool = True
    no_test_execution_confirmed: bool = True
    no_self_prompt_execution_confirmed: bool = True
    no_subagent_invocation_confirmed: bool = True
    no_model_provider_confirmed: bool = True
    no_external_agent_confirmed: bool = True
    no_dominion_confirmed: bool = True
    no_production_certification_confirmed: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version(self.version)
        _require_non_blank("validation_summary", self.validation_summary)
        _validate_list("findings", self.findings)
        for name, value in self.__dict__.items():
            if name.endswith("_confirmed") and value is not True:
                raise ValueError(f"{name} must be true")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairApprovalArtifactRunPreview:
    run_preview_id: str
    version: str
    preview_summary: str
    preview_steps: list[str]
    preview_only: bool = True
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        _validate_version(self.version)
        _require_non_blank("preview_summary", self.preview_summary)
        _validate_list("preview_steps", self.preview_steps)
        if not self.preview_only or self.ready_for_execution:
            raise ValueError("run preview must remain preview-only and not execution-ready")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairApprovalArtifactNoApplyGuarantee:
    guarantee_id: str
    version: str
    guarantee_summary: str
    no_approval_grant: bool = True
    no_apply_permission: bool = True
    no_sandbox_workspace_creation: bool = True
    no_patch_materialization: bool = True
    no_sandbox_apply: bool = True
    no_live_apply: bool = True
    no_patch_file_write: bool = True
    no_patch_application: bool = True
    no_apply_patch: bool = True
    no_git_apply: bool = True
    no_test_execution: bool = True
    no_self_prompt_execution: bool = True
    no_next_action_execution: bool = True
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
        for name, value in self.__dict__.items():
            if name.startswith("no_") and value is not True:
                raise ValueError(f"{name} must be true")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class V0391ReadinessReport:
    report_id: str
    version: str
    release_name: str
    track_name: str
    approval_artifact: RepairApprovalArtifact | None
    scope_binding: RepairApprovalScopeBinding | None
    authenticity_assessment: RepairApprovalAuthenticityAssessment | None
    expiration_assessment: RepairApprovalExpirationAssessment | None
    patch_binding_assessment: RepairApprovalPatchBindingAssessment | None
    process_state_gate: RepairApprovalProcessStateGate | None
    risk_assessment: RepairApprovalRiskAssessment | None
    decision: RepairApprovalArtifactDecision
    flags: RepairApprovalArtifactFlagSet
    source_refs: list[RepairApprovalArtifactSourceRef]
    report_summary: str
    ready_for_v0392_sandbox_workspace_isolation: bool = True
    ready_for_v0393_human_approved_patch_materialization_sandbox_apply: bool = True
    ready_for_approval_artifact_intake: bool = True
    ready_for_approval_artifact_schema_validation: bool = True
    ready_for_approval_authenticity_assessment: bool = True
    ready_for_approval_scope_validation: bool = True
    ready_for_approval_expiration_validation: bool = True
    ready_for_approval_process_state_transition_gate: bool = True
    approval_artifact_received: bool = True
    approval_artifact_valid_for_future_gate: bool = True
    future_sandbox_apply_precondition_satisfied: bool = True
    approval_granted_now: bool = False
    approval_capture_enabled: bool = False
    apply_permission_enabled: bool = False
    sandbox_workspace_creation_enabled: bool = False
    patch_materialization_enabled: bool = False
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
        for name in ("report_id", "version", "release_name", "track_name", "report_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("source_refs", self.source_refs)
        _validate_false(self, UNSAFE_REPORT_NAMES)
        if not repair_approval_artifact_flags_preserve_no_apply(self.flags):
            raise ValueError("flags must preserve no apply")
        _validate_dict("metadata", self.metadata)


def build_repair_approval_artifact_flags(**overrides: Any) -> RepairApprovalArtifactFlagSet:
    return RepairApprovalArtifactFlagSet(flag_set_id="v0391-approval-artifact-flags", **overrides)


def build_repair_approval_artifact_source_ref(**overrides: Any) -> RepairApprovalArtifactSourceRef:
    defaults = {
        "source_ref_id": "v0391-source-ref",
        "source_kind": RepairApprovalArtifactSourceKind.V0390_REPAIR_APPLY_BOUNDARY,
        "source_id": "v0390-readiness-report",
        "source_summary": "v0.39.0 boundary metadata consumed by v0.39.1 approval artifact gate.",
        "evidence_refs": ["v0.39.0 boundary report"],
    }
    return RepairApprovalArtifactSourceRef(**_with_overrides(defaults, overrides))


def build_repair_approval_artifact_policy(**overrides: Any) -> RepairApprovalArtifactPolicy:
    defaults = {
        "policy_id": "v0391-approval-artifact-policy",
        "version": V0391_VERSION,
        "allowed_modes": [item.value for item in RepairApprovalArtifactMode if item is not RepairApprovalArtifactMode.UNKNOWN],
        "allowed_artifact_kinds": [item.value for item in RepairApprovalArtifactKind if item is not RepairApprovalArtifactKind.UNKNOWN],
        "allowed_scope_kinds": [
            RepairApprovalScopeKind.PROPOSED_PATCH_ENVELOPE_SCOPE.value,
            RepairApprovalScopeKind.PROPOSED_FILE_CHANGE_SCOPE.value,
            RepairApprovalScopeKind.PROPOSED_HUNK_SCOPE.value,
            RepairApprovalScopeKind.SAFETY_VALIDATED_PATCH_SCOPE.value,
            RepairApprovalScopeKind.HUMAN_REVIEW_PACKET_SCOPE.value,
            RepairApprovalScopeKind.SANDBOX_APPLY_FUTURE_SCOPE.value,
        ],
        "required_authenticity_signals": [
            RepairApprovalAuthenticitySignalKind.REVIEWER_ID_PRESENT.value,
            RepairApprovalAuthenticitySignalKind.APPROVAL_PHRASE_PRESENT.value,
            RepairApprovalAuthenticitySignalKind.APPROVAL_TIMESTAMP_PRESENT.value,
            RepairApprovalAuthenticitySignalKind.PATCH_ENVELOPE_REF_PRESENT.value,
        ],
    }
    return RepairApprovalArtifactPolicy(**_with_overrides(defaults, overrides))


def default_repair_approval_artifact_policy(**overrides: Any) -> RepairApprovalArtifactPolicy:
    return build_repair_approval_artifact_policy(**overrides)


def build_repair_approval_artifact_input(**overrides: Any) -> RepairApprovalArtifactInput:
    defaults = {
        "approval_input_id": "v0391-approval-input",
        "version": V0391_VERSION,
        "artifact_kind": RepairApprovalArtifactKind.EXPLICIT_HUMAN_APPROVAL_TEXT,
        "raw_approval_text": "Approved for future sandbox-only repair apply precondition metadata.",
        "reviewer_id": "reviewer-1",
        "reviewer_role": "human_reviewer",
        "approval_phrase": "Approved for sandbox-only repair",
        "approval_timestamp": "2026-06-09T00:00:00Z",
        "expiration_timestamp": "2026-06-10T00:00:00Z",
        "approval_nonce": "nonce-v0391",
        "approval_scope_summary": "Approval is scoped to proposed patch envelope metadata for future sandbox-only apply.",
        "proposed_patch_envelope_id": "patch-envelope-1",
        "safety_report_id": "safety-report-1",
        "human_review_packet_id": "review-packet-1",
        "approval_request_contract_id": "approval-contract-1",
        "source_refs": [build_repair_approval_artifact_source_ref()],
        "prohibited_runtime_actions": list(PROHIBITED_RUNTIME_ACTIONS),
    }
    return RepairApprovalArtifactInput(**_with_overrides(defaults, overrides))


def normalize_repair_approval_artifact_input(
    approval_input: RepairApprovalArtifactInput,
    policy: RepairApprovalArtifactPolicy | None = None,
) -> RepairApprovalArtifact:
    policy = policy or default_repair_approval_artifact_policy()
    preview = approval_input.raw_approval_text[: min(policy.max_artifact_text_chars, 160)]
    digest = _text_digest(approval_input.raw_approval_text)
    return build_repair_approval_artifact(
        raw_approval_text_preview=preview,
        normalized_approval_summary=approval_input.approval_scope_summary,
        artifact_kind=approval_input.artifact_kind,
        reviewer_id=approval_input.reviewer_id,
        reviewer_role=approval_input.reviewer_role,
        approval_phrase_present=bool(approval_input.approval_phrase),
        approval_timestamp=approval_input.approval_timestamp,
        expiration_timestamp=approval_input.expiration_timestamp,
        approval_nonce=approval_input.approval_nonce,
        artifact_digest=digest,
        source_refs=approval_input.source_refs,
    )


def build_repair_approval_artifact(**overrides: Any) -> RepairApprovalArtifact:
    defaults = {
        "approval_artifact_id": "v0391-approval-artifact",
        "version": V0391_VERSION,
        "artifact_kind": RepairApprovalArtifactKind.EXPLICIT_HUMAN_APPROVAL_TEXT,
        "status": RepairApprovalArtifactStatus.RECEIVED,
        "disposition": RepairApprovalDisposition.ACCEPTED_FOR_FUTURE_GATE,
        "raw_approval_text_preview": "Approved for future sandbox-only repair apply precondition metadata.",
        "normalized_approval_summary": "Approval artifact received for future sandbox-only apply precondition metadata.",
        "reviewer_id": "reviewer-1",
        "reviewer_role": "human_reviewer",
        "approval_phrase_present": True,
        "approval_timestamp": "2026-06-09T00:00:00Z",
        "expiration_timestamp": "2026-06-10T00:00:00Z",
        "approval_nonce": "nonce-v0391",
        "artifact_digest": _text_digest("Approved for future sandbox-only repair apply precondition metadata."),
        "bounded": True,
        "redacted": True,
        "source_refs": [build_repair_approval_artifact_source_ref()],
    }
    return RepairApprovalArtifact(**_with_overrides(defaults, overrides))


def build_repair_approval_scope_binding(**overrides: Any) -> RepairApprovalScopeBinding:
    defaults = {
        "scope_binding_id": "v0391-scope-binding",
        "version": V0391_VERSION,
        "approval_artifact_id": "v0391-approval-artifact",
        "scope_kind": RepairApprovalScopeKind.SANDBOX_APPLY_FUTURE_SCOPE,
        "proposed_patch_envelope_id": "patch-envelope-1",
        "safety_report_id": "safety-report-1",
        "human_review_packet_id": "review-packet-1",
        "approved_file_scope_refs": ["file-scope-1"],
        "approved_hunk_scope_refs": ["hunk-scope-1"],
        "denied_scope_refs": [],
        "sandbox_only_scope": True,
        "live_apply_scope_requested": False,
        "scope_valid": True,
        "scope_summary": "Approval scope is sandbox-only and bound to proposed patch envelope metadata.",
        "evidence_refs": ["patch-envelope-1", "review-packet-1"],
    }
    return RepairApprovalScopeBinding(**_with_overrides(defaults, overrides))


def bind_repair_approval_scope(
    approval_artifact: RepairApprovalArtifact,
    proposed_patch_envelope_id: str | None = "patch-envelope-1",
    safety_report_id: str | None = "safety-report-1",
    human_review_packet_id: str | None = "review-packet-1",
    live_apply_scope_requested: bool = False,
) -> RepairApprovalScopeBinding:
    return build_repair_approval_scope_binding(
        approval_artifact_id=approval_artifact.approval_artifact_id,
        proposed_patch_envelope_id=proposed_patch_envelope_id,
        safety_report_id=safety_report_id,
        human_review_packet_id=human_review_packet_id,
        live_apply_scope_requested=live_apply_scope_requested,
        scope_valid=not live_apply_scope_requested,
        sandbox_only_scope=not live_apply_scope_requested,
    )


def build_repair_approval_authenticity_assessment(**overrides: Any) -> RepairApprovalAuthenticityAssessment:
    defaults = {
        "authenticity_assessment_id": "v0391-authenticity-assessment",
        "version": V0391_VERSION,
        "approval_artifact_id": "v0391-approval-artifact",
        "authenticity_signals": [
            RepairApprovalAuthenticitySignalKind.REVIEWER_ID_PRESENT,
            RepairApprovalAuthenticitySignalKind.REVIEWER_ROLE_PRESENT,
            RepairApprovalAuthenticitySignalKind.APPROVAL_PHRASE_PRESENT,
            RepairApprovalAuthenticitySignalKind.APPROVAL_TIMESTAMP_PRESENT,
            RepairApprovalAuthenticitySignalKind.APPROVAL_NONCE_PRESENT,
            RepairApprovalAuthenticitySignalKind.APPROVAL_ARTIFACT_DIGEST_PRESENT,
            RepairApprovalAuthenticitySignalKind.APPROVAL_SCOPE_PRESENT,
            RepairApprovalAuthenticitySignalKind.PATCH_ENVELOPE_REF_PRESENT,
            RepairApprovalAuthenticitySignalKind.REVIEW_PACKET_REF_PRESENT,
            RepairApprovalAuthenticitySignalKind.SAFETY_REPORT_REF_PRESENT,
        ],
        "missing_signals": [],
        "authenticity_summary": "Approval artifact contains required supplied metadata signals; no external identity verification performed.",
        "reviewer_id_present": True,
        "reviewer_role_present": True,
        "approval_phrase_present": True,
        "timestamp_present": True,
        "nonce_present": True,
        "digest_present": True,
        "authenticity_confidence": RepairApprovalConfidenceLevel.HIGH,
        "authenticity_sufficient_for_future_gate": True,
    }
    return RepairApprovalAuthenticityAssessment(**_with_overrides(defaults, overrides))


def assess_repair_approval_authenticity(approval_artifact: RepairApprovalArtifact) -> RepairApprovalAuthenticityAssessment:
    missing: list[RepairApprovalAuthenticitySignalKind] = []
    signals: list[RepairApprovalAuthenticitySignalKind] = []
    if approval_artifact.reviewer_id:
        signals.append(RepairApprovalAuthenticitySignalKind.REVIEWER_ID_PRESENT)
    else:
        missing.append(RepairApprovalAuthenticitySignalKind.MISSING_REVIEWER_ID)
    if approval_artifact.approval_phrase_present:
        signals.append(RepairApprovalAuthenticitySignalKind.APPROVAL_PHRASE_PRESENT)
    else:
        missing.append(RepairApprovalAuthenticitySignalKind.MISSING_APPROVAL_PHRASE)
    if approval_artifact.approval_timestamp:
        signals.append(RepairApprovalAuthenticitySignalKind.APPROVAL_TIMESTAMP_PRESENT)
    else:
        missing.append(RepairApprovalAuthenticitySignalKind.MISSING_TIMESTAMP)
    if approval_artifact.artifact_digest:
        signals.append(RepairApprovalAuthenticitySignalKind.APPROVAL_ARTIFACT_DIGEST_PRESENT)
    confidence = RepairApprovalConfidenceLevel.HIGH if not missing else RepairApprovalConfidenceLevel.LOW
    return build_repair_approval_authenticity_assessment(
        approval_artifact_id=approval_artifact.approval_artifact_id,
        authenticity_signals=signals,
        missing_signals=missing,
        authenticity_confidence=confidence,
        authenticity_sufficient_for_future_gate=not missing,
    )


def build_repair_approval_expiration_assessment(**overrides: Any) -> RepairApprovalExpirationAssessment:
    defaults = {
        "expiration_assessment_id": "v0391-expiration-assessment",
        "version": V0391_VERSION,
        "approval_artifact_id": "v0391-approval-artifact",
        "expiration_status": RepairApprovalExpirationStatus.FRESH,
        "approval_timestamp": "2026-06-09T00:00:00Z",
        "expiration_timestamp": "2026-06-10T00:00:00Z",
        "evaluated_at": "2026-06-09T00:00:00Z",
        "expiration_summary": "Approval artifact is fresh for future gate metadata.",
        "fresh_for_future_gate": True,
        "expired": False,
    }
    return RepairApprovalExpirationAssessment(**_with_overrides(defaults, overrides))


def assess_repair_approval_expiration(
    approval_artifact: RepairApprovalArtifact,
    expired: bool = False,
) -> RepairApprovalExpirationAssessment:
    return build_repair_approval_expiration_assessment(
        approval_artifact_id=approval_artifact.approval_artifact_id,
        approval_timestamp=approval_artifact.approval_timestamp,
        expiration_timestamp=approval_artifact.expiration_timestamp,
        expiration_status=RepairApprovalExpirationStatus.EXPIRED if expired else RepairApprovalExpirationStatus.FRESH,
        expiration_summary="Approval artifact is expired." if expired else "Approval artifact is fresh for future gate metadata.",
        fresh_for_future_gate=not expired,
        expired=expired,
    )


def build_repair_approval_patch_binding_assessment(**overrides: Any) -> RepairApprovalPatchBindingAssessment:
    defaults = {
        "patch_binding_assessment_id": "v0391-patch-binding-assessment",
        "version": V0391_VERSION,
        "approval_artifact_id": "v0391-approval-artifact",
        "proposed_patch_envelope_id": "patch-envelope-1",
        "safety_report_id": "safety-report-1",
        "human_review_packet_id": "review-packet-1",
        "approval_request_contract_id": "approval-contract-1",
        "patch_binding_present": True,
        "safety_binding_present": True,
        "review_packet_binding_present": True,
        "binding_consistent": True,
        "binding_summary": "Approval artifact is bound to patch envelope, safety report, and review packet metadata.",
        "evidence_refs": ["patch-envelope-1", "safety-report-1", "review-packet-1"],
    }
    return RepairApprovalPatchBindingAssessment(**_with_overrides(defaults, overrides))


def assess_repair_approval_patch_binding(
    approval_artifact: RepairApprovalArtifact,
    proposed_patch_envelope_id: str | None = "patch-envelope-1",
    safety_report_id: str | None = "safety-report-1",
    human_review_packet_id: str | None = "review-packet-1",
) -> RepairApprovalPatchBindingAssessment:
    binding_present = bool(proposed_patch_envelope_id and safety_report_id and human_review_packet_id)
    return build_repair_approval_patch_binding_assessment(
        approval_artifact_id=approval_artifact.approval_artifact_id,
        proposed_patch_envelope_id=proposed_patch_envelope_id,
        safety_report_id=safety_report_id,
        human_review_packet_id=human_review_packet_id,
        patch_binding_present=bool(proposed_patch_envelope_id),
        safety_binding_present=bool(safety_report_id),
        review_packet_binding_present=bool(human_review_packet_id),
        binding_consistent=binding_present,
    )


def build_repair_approval_process_state_gate(**overrides: Any) -> RepairApprovalProcessStateGate:
    defaults = {
        "process_state_gate_id": "v0391-process-state-gate",
        "version": V0391_VERSION,
        "approval_artifact_id": "v0391-approval-artifact",
        "prior_state": "approval_artifact_received",
        "candidate_next_state": "future_sandbox_workspace_isolation_eligible",
        "transition_summary": "Approval artifact metadata satisfies future workspace isolation and sandbox apply precondition gates.",
        "gate_satisfied": True,
        "future_workspace_isolation_eligible": True,
        "future_sandbox_apply_precondition_satisfied": True,
    }
    return RepairApprovalProcessStateGate(**_with_overrides(defaults, overrides))


def create_repair_approval_process_state_gate(
    approval_artifact: RepairApprovalArtifact,
    authenticity: RepairApprovalAuthenticityAssessment,
    expiration: RepairApprovalExpirationAssessment,
    patch_binding: RepairApprovalPatchBindingAssessment,
    scope_binding: RepairApprovalScopeBinding,
) -> RepairApprovalProcessStateGate:
    gate = (
        authenticity.authenticity_sufficient_for_future_gate
        and expiration.fresh_for_future_gate
        and patch_binding.binding_consistent
        and scope_binding.scope_valid
    )
    return build_repair_approval_process_state_gate(
        approval_artifact_id=approval_artifact.approval_artifact_id,
        gate_satisfied=gate,
        future_workspace_isolation_eligible=gate,
        future_sandbox_apply_precondition_satisfied=gate,
    )


def build_repair_approval_risk_assessment(**overrides: Any) -> RepairApprovalRiskAssessment:
    defaults = {
        "risk_assessment_id": "v0391-risk-assessment",
        "version": V0391_VERSION,
        "approval_artifact_id": "v0391-approval-artifact",
        "risk_kinds": [],
        "risk_summary": "No blocking approval artifact risk identified for future gate metadata.",
        "severity": "low",
        "blocks_future_workspace_isolation": False,
        "blocks_future_sandbox_apply_precondition": False,
        "requires_human_review": False,
        "do_nothing_recommended": False,
        "evidence_refs": [],
    }
    return RepairApprovalRiskAssessment(**_with_overrides(defaults, overrides))


def assess_repair_approval_risk(
    approval_artifact: RepairApprovalArtifact,
    authenticity: RepairApprovalAuthenticityAssessment,
    scope_binding: RepairApprovalScopeBinding,
    expiration: RepairApprovalExpirationAssessment,
    patch_binding: RepairApprovalPatchBindingAssessment,
) -> RepairApprovalRiskAssessment:
    risks: list[RepairApprovalArtifactRiskKind] = []
    if not authenticity.authenticity_sufficient_for_future_gate:
        risks.append(RepairApprovalArtifactRiskKind.APPROVAL_AUTHENTICITY_UNCERTAIN_RISK)
    if not scope_binding.scope_valid:
        risks.append(RepairApprovalArtifactRiskKind.APPROVAL_SCOPE_MISMATCH_RISK)
    if expiration.expired:
        risks.append(RepairApprovalArtifactRiskKind.APPROVAL_EXPIRED_RISK)
    if not patch_binding.binding_consistent:
        risks.append(RepairApprovalArtifactRiskKind.PATCH_ENVELOPE_BINDING_MISSING_RISK)
    blocking = bool(risks)
    return build_repair_approval_risk_assessment(
        approval_artifact_id=approval_artifact.approval_artifact_id,
        risk_kinds=risks,
        risk_summary="Approval artifact has blocking risk." if blocking else "No blocking approval artifact risk identified for future gate metadata.",
        severity="high" if blocking else "low",
        blocks_future_workspace_isolation=blocking,
        blocks_future_sandbox_apply_precondition=blocking,
        requires_human_review=blocking,
        do_nothing_recommended=blocking,
    )


def build_repair_approval_artifact_decision(**overrides: Any) -> RepairApprovalArtifactDecision:
    defaults = {
        "approval_decision_id": "v0391-approval-decision",
        "version": V0391_VERSION,
        "approval_artifact_id": "v0391-approval-artifact",
        "decision_kind": RepairApprovalArtifactDecisionKind.ALLOW_FUTURE_WORKSPACE_ISOLATION_INPUT,
        "status": RepairApprovalArtifactStatus.READY_FOR_FUTURE_WORKSPACE_ISOLATION,
        "disposition": RepairApprovalDisposition.ACCEPTED_FOR_FUTURE_GATE,
        "readiness_level": RepairApprovalArtifactReadinessLevel.FUTURE_WORKSPACE_ISOLATION_INPUT_READY,
        "decision_summary": "Approval artifact is valid for future workspace isolation input metadata only.",
        "rationale_summary": "Supplied metadata has required scope, freshness, and binding signals; no apply permission is granted.",
        "confidence": RepairApprovalConfidenceLevel.HIGH,
        "evidence_refs": ["v0391-approval-artifact", "v0391-process-state-gate"],
        "ready_for_future_workspace_isolation_input": True,
        "ready_for_future_sandbox_apply_precondition_input": True,
        "approval_artifact_valid_for_future_gate": True,
    }
    return RepairApprovalArtifactDecision(**_with_overrides(defaults, overrides))


def decide_repair_approval_artifact(
    approval_artifact: RepairApprovalArtifact,
    process_state_gate: RepairApprovalProcessStateGate,
    risk_assessment: RepairApprovalRiskAssessment,
) -> RepairApprovalArtifactDecision:
    allowed = process_state_gate.gate_satisfied and not risk_assessment.blocks_future_sandbox_apply_precondition
    return build_repair_approval_artifact_decision(
        approval_artifact_id=approval_artifact.approval_artifact_id,
        decision_kind=RepairApprovalArtifactDecisionKind.ALLOW_FUTURE_WORKSPACE_ISOLATION_INPUT if allowed else RepairApprovalArtifactDecisionKind.REQUIRE_REVIEW,
        status=RepairApprovalArtifactStatus.READY_FOR_FUTURE_WORKSPACE_ISOLATION if allowed else RepairApprovalArtifactStatus.REVIEW_REQUIRED,
        disposition=RepairApprovalDisposition.ACCEPTED_FOR_FUTURE_GATE if allowed else RepairApprovalDisposition.REVIEW_REQUIRED,
        ready_for_future_workspace_isolation_input=allowed,
        ready_for_future_sandbox_apply_precondition_input=allowed,
        approval_artifact_valid_for_future_gate=allowed,
        confidence=RepairApprovalConfidenceLevel.HIGH if allowed else RepairApprovalConfidenceLevel.LOW,
    )


def build_repair_approval_artifact_validation_finding(**overrides: Any) -> RepairApprovalArtifactValidationFinding:
    defaults = {
        "finding_id": "v0391-validation-finding",
        "finding_summary": "Approval artifact gate remains metadata-only and grants no apply permission.",
        "risk_kind": RepairApprovalArtifactRiskKind.APPLY_PERMISSION_CONFUSION_RISK,
        "blocked": True,
    }
    return RepairApprovalArtifactValidationFinding(**_with_overrides(defaults, overrides))


def build_repair_approval_artifact_validation_report(**overrides: Any) -> RepairApprovalArtifactValidationReport:
    defaults = {
        "validation_report_id": "v0391-validation-report",
        "version": V0391_VERSION,
        "validation_summary": "Validation confirms approval artifact intake/schema/authenticity/scope/freshness behavior and no apply.",
        "findings": [build_repair_approval_artifact_validation_finding()],
    }
    return RepairApprovalArtifactValidationReport(**_with_overrides(defaults, overrides))


def build_repair_approval_artifact_run_preview(**overrides: Any) -> RepairApprovalArtifactRunPreview:
    defaults = {
        "run_preview_id": "v0391-run-preview",
        "version": V0391_VERSION,
        "preview_summary": "Preview approval artifact intake gate without runtime authority.",
        "preview_steps": [
            "ApprovalArtifactInput",
            "ApprovalArtifact",
            "AuthenticityAssessment",
            "ScopeBinding",
            "ExpirationAssessment",
            "PatchBindingAssessment",
            "ApprovalProcessStateGate",
            "ApprovalDecision",
        ],
    }
    return RepairApprovalArtifactRunPreview(**_with_overrides(defaults, overrides))


def build_repair_approval_artifact_no_apply_guarantee(**overrides: Any) -> RepairApprovalArtifactNoApplyGuarantee:
    defaults = {
        "guarantee_id": "v0391-no-apply-guarantee",
        "version": V0391_VERSION,
        "guarantee_summary": "v0.39.1 approval artifact gate does not grant approval or apply permission.",
    }
    return RepairApprovalArtifactNoApplyGuarantee(**_with_overrides(defaults, overrides))


def build_v0391_readiness_report(**overrides: Any) -> V0391ReadinessReport:
    approval_input = overrides.pop("approval_input", build_repair_approval_artifact_input())
    artifact = normalize_repair_approval_artifact_input(approval_input)
    scope = bind_repair_approval_scope(artifact)
    authenticity = assess_repair_approval_authenticity(artifact)
    expiration = assess_repair_approval_expiration(artifact)
    patch_binding = assess_repair_approval_patch_binding(artifact)
    gate = create_repair_approval_process_state_gate(artifact, authenticity, expiration, patch_binding, scope)
    risk = assess_repair_approval_risk(artifact, authenticity, scope, expiration, patch_binding)
    decision = decide_repair_approval_artifact(artifact, gate, risk)
    defaults = {
        "report_id": "v0391-readiness-report",
        "version": V0391_VERSION,
        "release_name": V0391_RELEASE_NAME,
        "track_name": V039_TRACK_NAME,
        "approval_artifact": artifact,
        "scope_binding": scope,
        "authenticity_assessment": authenticity,
        "expiration_assessment": expiration,
        "patch_binding_assessment": patch_binding,
        "process_state_gate": gate,
        "risk_assessment": risk,
        "decision": decision,
        "flags": build_repair_approval_artifact_flags(),
        "source_refs": [build_repair_approval_artifact_source_ref()],
        "report_summary": "v0.39.1 approval artifact gate is ready as future workspace isolation/apply precondition metadata only.",
    }
    return V0391ReadinessReport(**_with_overrides(defaults, overrides))


def repair_approval_artifact_flags_preserve_no_apply(flags: RepairApprovalArtifactFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_FLAG_NAMES)


def repair_approval_policy_blocks_apply_and_execution(policy: RepairApprovalArtifactPolicy) -> bool:
    return all(getattr(policy, name) is False for name in UNSAFE_POLICY_ALLOW_NAMES)


def repair_approval_artifact_is_not_apply_permission(artifact: RepairApprovalArtifact) -> bool:
    return all(getattr(artifact, name) is False for name in UNSAFE_ARTIFACT_NAMES)


def repair_approval_process_state_gate_is_not_runtime_authority(gate: RepairApprovalProcessStateGate) -> bool:
    return not gate.process_state_authority_granted and not gate.runtime_authority_granted


def repair_approval_decision_is_not_apply_permission(decision: RepairApprovalArtifactDecision) -> bool:
    return all(getattr(decision, name) is False for name in UNSAFE_DECISION_NAMES)


def v0391_readiness_report_is_not_execution_ready(report: V0391ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_REPORT_NAMES) and repair_approval_artifact_flags_preserve_no_apply(report.flags)
