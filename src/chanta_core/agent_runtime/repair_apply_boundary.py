"""v0.39.0 human-approved sandbox repair apply boundary metadata.

This module defines boundary and future-stage handoff metadata only. It does
not intake approval artifacts, create workspaces, materialize patches, apply
patches, run tests, generate prompts, invoke subagents, call providers, or
grant runtime authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank


V0390_VERSION = "v0.39.0"
V0390_RELEASE_NAME = "v0.39.0 Human-approved Sandbox Repair Apply Boundary + PI-native Self-Prompting Mission Loop Boundary"
V039_TRACK_NAME = "v0.39 Human-approved Sandbox Repair Apply & Re-test Loop with PI-native Self-Prompting Mission Loop Boundary"
SELF_PROMPTING_CANONICAL_NAME = "Self-Prompting Mission Loop"


class RepairApplyBoundaryMode(StrEnum):
    HUMAN_APPROVED_SANDBOX_REPAIR_APPLY_BOUNDARY = "human_approved_sandbox_repair_apply_boundary"
    APPROVAL_ARTIFACT_BOUNDARY = "approval_artifact_boundary"
    SANDBOX_WORKSPACE_ISOLATION_BOUNDARY = "sandbox_workspace_isolation_boundary"
    SANDBOX_PATCH_MATERIALIZATION_BOUNDARY = "sandbox_patch_materialization_boundary"
    SANDBOX_REPAIR_APPLY_BOUNDARY = "sandbox_repair_apply_boundary"
    POST_APPLY_CONTROLLED_RETEST_BOUNDARY = "post_apply_controlled_retest_boundary"
    BEFORE_AFTER_REPAIR_COMPARISON_BOUNDARY = "before_after_repair_comparison_boundary"
    PI_NATIVE_REPAIR_PROCESS_STATE_BOUNDARY = "pi_native_repair_process_state_boundary"
    SELF_PROMPTING_MISSION_LOOP_BOUNDARY = "self_prompting_mission_loop_boundary"
    PROCESS_STATE_DRIVEN_NEXT_ACTION_BOUNDARY = "process_state_driven_next_action_boundary"
    AGENT_TO_SUBAGENT_PROMPT_BOUNDARY = "agent_to_subagent_prompt_boundary"
    HUMAN_HANDOFF_PROMPT_BOUNDARY = "human_handoff_prompt_boundary"
    FUTURE_V039_STAGE_GATE = "future_v039_stage_gate"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairApplyBoundarySourceKind(StrEnum):
    V0389_CONSOLIDATION_REPORT = "v0389_consolidation_report"
    V0389_RELEASE_MANIFEST = "v0389_release_manifest"
    V0389_HANDOFF_PACKET = "v0389_handoff_packet"
    V0388_CLI_SURFACE_REPORT = "v0388_cli_surface_report"
    V0387_LOOP_PACKET = "v0387_loop_packet"
    V0386_HUMAN_REVIEW_PACKET = "v0386_human_review_packet"
    V0385_SAFETY_REPORT = "v0385_safety_report"
    V0384_PROPOSED_PATCH_ENVELOPE = "v0384_proposed_patch_envelope"
    V0383_SCOPE_PLAN = "v0383_scope_plan"
    V0382_SOURCE_CONTEXT_SNAPSHOT = "v0382_source_context_snapshot"
    V0381_EVIDENCE_BUNDLE = "v0381_evidence_bundle"
    V0380_BOUNDARY = "v0380_boundary"
    LOOP_ENGINEERING_NOTE = "loop_engineering_note"
    PI_NATIVE_DESIGN_NOTE = "pi_native_design_note"
    MANUAL_OPERATOR_NOTE = "manual_operator_note"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class RepairApplyBoundaryStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    BOUNDARY_DEFINED = "boundary_defined"
    BOUNDARY_DEFINED_WITH_WARNINGS = "boundary_defined_with_warnings"
    READY_FOR_V0391_APPROVAL_ARTIFACT_INTAKE = "ready_for_v0391_approval_artifact_intake"
    READY_FOR_V0392_SANDBOX_WORKSPACE_ISOLATION = "ready_for_v0392_sandbox_workspace_isolation"
    READY_FOR_V0393_SANDBOX_PATCH_MATERIALIZATION = "ready_for_v0393_sandbox_patch_materialization"
    READY_FOR_V0394_POST_APPLY_RETEST = "ready_for_v0394_post_apply_retest"
    READY_FOR_V0395_BEFORE_AFTER_COMPARISON = "ready_for_v0395_before_after_comparison"
    READY_FOR_V0396_PROCESS_STATE_RECONSTRUCTION = "ready_for_v0396_process_state_reconstruction"
    READY_FOR_V0397_SELF_PROMPTING_DRAFT = "ready_for_v0397_self_prompting_draft"
    READY_FOR_V0398_CLI_SURFACE = "ready_for_v0398_cli_surface"
    READY_FOR_V0399_CONSOLIDATION = "ready_for_v0399_consolidation"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class RepairApplyBoundaryReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    APPLY_BOUNDARY_READY = "apply_boundary_ready"
    APPROVAL_BOUNDARY_READY = "approval_boundary_ready"
    SANDBOX_ISOLATION_BOUNDARY_READY = "sandbox_isolation_boundary_ready"
    PATCH_MATERIALIZATION_BOUNDARY_READY = "patch_materialization_boundary_ready"
    SANDBOX_APPLY_BOUNDARY_READY = "sandbox_apply_boundary_ready"
    RETEST_BOUNDARY_READY = "retest_boundary_ready"
    OUTCOME_COMPARISON_BOUNDARY_READY = "outcome_comparison_boundary_ready"
    PI_PROCESS_STATE_BOUNDARY_READY = "pi_process_state_boundary_ready"
    SELF_PROMPTING_LOOP_BOUNDARY_READY = "self_prompting_loop_boundary_ready"
    NEXT_ACTION_DRAFT_BOUNDARY_READY = "next_action_draft_boundary_ready"
    SUBAGENT_PROMPT_BOUNDARY_READY = "subagent_prompt_boundary_ready"
    HUMAN_HANDOFF_BOUNDARY_READY = "human_handoff_boundary_ready"
    V039_TRACK_BOUNDARY_READY = "v039_track_boundary_ready"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class RepairApplyBoundaryDecisionKind(StrEnum):
    ALLOW_BOUNDARY_DEFINITION = "allow_boundary_definition"
    ALLOW_APPROVAL_ARTIFACT_BOUNDARY = "allow_approval_artifact_boundary"
    ALLOW_SANDBOX_WORKSPACE_ISOLATION_BOUNDARY = "allow_sandbox_workspace_isolation_boundary"
    ALLOW_SANDBOX_PATCH_MATERIALIZATION_BOUNDARY = "allow_sandbox_patch_materialization_boundary"
    ALLOW_SANDBOX_APPLY_BOUNDARY = "allow_sandbox_apply_boundary"
    ALLOW_POST_APPLY_RETEST_BOUNDARY = "allow_post_apply_retest_boundary"
    ALLOW_BEFORE_AFTER_COMPARISON_BOUNDARY = "allow_before_after_comparison_boundary"
    ALLOW_PI_PROCESS_STATE_BOUNDARY = "allow_pi_process_state_boundary"
    ALLOW_SELF_PROMPTING_LOOP_BOUNDARY = "allow_self_prompting_loop_boundary"
    ALLOW_NEXT_ACTION_DRAFT_BOUNDARY = "allow_next_action_draft_boundary"
    ALLOW_AGENT_TO_SUBAGENT_PROMPT_BOUNDARY = "allow_agent_to_subagent_prompt_boundary"
    ALLOW_HUMAN_HANDOFF_BOUNDARY = "allow_human_handoff_boundary"
    ALLOW_FUTURE_V039_STAGE_GATE = "allow_future_v039_stage_gate"
    CHOOSE_DO_NOTHING = "choose_do_nothing"
    CHOOSE_HUMAN_REVIEW_REQUIRED = "choose_human_review_required"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class RepairApplyBoundaryRiskKind(StrEnum):
    APPROVAL_CONFUSION_RISK = "approval_confusion_risk"
    APPLY_PERMISSION_CONFUSION_RISK = "apply_permission_confusion_risk"
    SANDBOX_LIVE_CONFUSION_RISK = "sandbox_live_confusion_risk"
    SELF_PROMPT_EXECUTION_CONFUSION_RISK = "self_prompt_execution_confusion_risk"
    NEXT_ACTION_AUTO_EXECUTION_RISK = "next_action_auto_execution_risk"
    SUBAGENT_AUTO_INVOCATION_RISK = "subagent_auto_invocation_risk"
    AUTONOMOUS_LOOP_RUNTIME_RISK = "autonomous_loop_runtime_risk"
    RETRY_LOOP_RISK = "retry_loop_risk"
    MULTI_CYCLE_LOOP_RISK = "multi_cycle_loop_risk"
    AUTOMATIC_REPAIR_RISK = "automatic_repair_risk"
    TEST_EXECUTION_CONFUSION_RISK = "test_execution_confusion_risk"
    PROCESS_STATE_CORRECTNESS_OVERCLAIM_RISK = "process_state_correctness_overclaim_risk"
    PIG_RECOMMENDATION_AUTHORITY_CONFUSION_RISK = "pig_recommendation_authority_confusion_risk"
    LIVE_WORKSPACE_APPLY_RISK = "live_workspace_apply_risk"
    LIVE_WORKSPACE_WRITE_RISK = "live_workspace_write_risk"
    PATCH_APPLICATION_RISK = "patch_application_risk"
    APPLY_PATCH_RISK = "apply_patch_risk"
    GIT_APPLY_RISK = "git_apply_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    MODEL_PROVIDER_INVOCATION_RISK = "model_provider_invocation_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    TOKEN_COST_LOOP_EXPLOSION_RISK = "token_cost_loop_explosion_risk"
    COGNITIVE_SURRENDER_RISK = "cognitive_surrender_risk"
    UNKNOWN = "unknown"


class RepairApplyBoundaryKind(StrEnum):
    HUMAN_APPROVED_SANDBOX_APPLY = "human_approved_sandbox_apply"
    APPROVAL_ARTIFACT_INTAKE = "approval_artifact_intake"
    APPROVAL_SCOPE_VALIDATION = "approval_scope_validation"
    SANDBOX_WORKSPACE_ISOLATION = "sandbox_workspace_isolation"
    SANDBOX_PATCH_MATERIALIZATION = "sandbox_patch_materialization"
    SANDBOX_REPAIR_APPLY = "sandbox_repair_apply"
    POST_APPLY_CONTROLLED_RETEST = "post_apply_controlled_retest"
    BEFORE_AFTER_REPAIR_OUTCOME_COMPARISON = "before_after_repair_outcome_comparison"
    REPAIR_EFFECTIVENESS_ASSESSMENT = "repair_effectiveness_assessment"
    REPAIR_PROCESS_STATE_PROJECTION = "repair_process_state_projection"
    OCEL_STYLE_REPAIR_EVENT_ENVELOPE = "ocel_style_repair_event_envelope"
    OCPX_STYLE_REPAIR_STATE_RECONSTRUCTION = "ocpx_style_repair_state_reconstruction"
    PIG_REPAIR_DIAGNOSTIC_RECOMMENDATION = "pig_repair_diagnostic_recommendation"
    SELF_PROMPTING_MISSION_LOOP = "self_prompting_mission_loop"
    PROCESS_STATE_DRIVEN_NEXT_ACTION_DRAFT = "process_state_driven_next_action_draft"
    AGENT_TO_SUBAGENT_PROMPT_DRAFT = "agent_to_subagent_prompt_draft"
    HUMAN_HANDOFF_PROMPT = "human_handoff_prompt"
    NO_AUTONOMOUS_CONTINUATION = "no_autonomous_continuation"
    NO_LIVE_APPLY = "no_live_apply"
    UNKNOWN = "unknown"


class SelfPromptingMissionLoopBoundaryKind(StrEnum):
    MISSION_OBJECTIVE_REF = "mission_objective_ref"
    PROCESS_STATE_PROJECTION = "process_state_projection"
    TRACE_HISTORY_REF = "trace_history_ref"
    VERIFICATION_CONTRACT_REF = "verification_contract_ref"
    POLICY_BOUNDARY_REF = "policy_boundary_ref"
    PIG_RECOMMENDATION_REF = "pig_recommendation_ref"
    NEXT_ACTION_DECISION_BOUNDARY = "next_action_decision_boundary"
    PROMPT_DRAFT_BOUNDARY = "prompt_draft_boundary"
    ACTION_REQUEST_DRAFT_BOUNDARY = "action_request_draft_boundary"
    SUBAGENT_VERIFICATION_PROMPT_DRAFT_BOUNDARY = "subagent_verification_prompt_draft_boundary"
    HUMAN_HANDOFF_BOUNDARY = "human_handoff_boundary"
    NO_SELF_EXECUTION_BOUNDARY = "no_self_execution_boundary"
    NO_SUBAGENT_INVOCATION_BOUNDARY = "no_subagent_invocation_boundary"
    NO_AUTONOMOUS_CONTINUATION_BOUNDARY = "no_autonomous_continuation_boundary"
    UNKNOWN = "unknown"


BOUNDARY_FLAG_NAMES = [
    "v039_boundary_layer_constructed",
    "human_approved_sandbox_repair_apply_boundary_available",
    "approval_artifact_boundary_available",
    "sandbox_workspace_isolation_boundary_available",
    "sandbox_patch_materialization_boundary_available",
    "sandbox_repair_apply_boundary_available",
    "post_apply_controlled_retest_boundary_available",
    "before_after_repair_comparison_boundary_available",
    "pi_native_process_state_boundary_available",
    "self_prompting_mission_loop_boundary_available",
    "process_state_driven_next_action_boundary_available",
    "agent_to_subagent_prompt_boundary_available",
    "human_handoff_prompt_boundary_available",
    "ready_for_v0391_approval_artifact_intake",
    "ready_for_v0392_sandbox_workspace_isolation",
    "ready_for_v0393_human_approved_patch_materialization_sandbox_apply",
    "ready_for_v0394_post_apply_controlled_retest",
    "ready_for_v0395_before_after_repair_outcome_comparison",
    "ready_for_v0396_pi_native_repair_process_state_reconstruction",
    "ready_for_v0397_self_prompting_next_action_draft",
    "ready_for_v0398_cli_sandbox_repair_apply_retest_loop_state_surface",
    "ready_for_v0399_consolidation",
    "ready_for_human_approved_sandbox_repair_apply_boundary",
    "ready_for_approval_artifact_intake_boundary",
    "ready_for_approval_scope_validation_boundary",
    "ready_for_sandbox_repair_workspace_isolation_boundary",
    "ready_for_sandbox_patch_materialization_boundary",
    "ready_for_sandbox_repair_apply_boundary",
    "ready_for_post_apply_controlled_retest_boundary",
    "ready_for_before_after_repair_comparison_boundary",
    "ready_for_repair_effectiveness_assessment_boundary",
    "ready_for_repair_process_state_projection_boundary",
    "ready_for_ocel_style_repair_event_envelope_boundary",
    "ready_for_ocpx_style_repair_state_reconstruction_boundary",
    "ready_for_pig_repair_diagnostic_recommendation_boundary",
    "ready_for_self_prompting_mission_loop_boundary",
    "ready_for_process_state_driven_next_action_draft_boundary",
    "ready_for_agent_to_subagent_prompt_draft_boundary",
    "ready_for_human_handoff_prompt_boundary",
]

UNSAFE_FLAG_NAMES = [
    "ready_for_execution",
    "ready_for_general_execution",
    "ready_for_approval_artifact_intake",
    "ready_for_approval_scope_validation",
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
    "allow_approval_artifact_intake",
    "allow_approval_capture",
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
    "allow_next_action_draft_generation",
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
    "approval_capture_allowed_now",
    "apply_allowed_now",
    "sandbox_apply_allowed_now",
    "live_apply_allowed_now",
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
    "approval_capture_enabled",
    "apply_enabled",
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
    if V0390_VERSION not in version:
        raise ValueError("version must include v0.39.0")


def _validate_list(name: str, value: list[Any]) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{name} must be a list")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a dict")


def _validate_false(instance: Any, names: list[str]) -> None:
    for name in names:
        if getattr(instance, name):
            raise ValueError(f"{name} must remain false in v0.39.0")


def _validate_true(instance: Any, names: list[str]) -> None:
    for name in names:
        if getattr(instance, name) is not True:
            raise ValueError(f"{name} must be true in v0.39.0 boundary metadata")


def _with_overrides(defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    merged.update(overrides)
    return merged


@dataclass(frozen=True)
class RepairApplyBoundaryFlagSet:
    flag_set_id: str
    version: str = V0390_VERSION
    v039_boundary_layer_constructed: bool = True
    human_approved_sandbox_repair_apply_boundary_available: bool = True
    approval_artifact_boundary_available: bool = True
    sandbox_workspace_isolation_boundary_available: bool = True
    sandbox_patch_materialization_boundary_available: bool = True
    sandbox_repair_apply_boundary_available: bool = True
    post_apply_controlled_retest_boundary_available: bool = True
    before_after_repair_comparison_boundary_available: bool = True
    pi_native_process_state_boundary_available: bool = True
    self_prompting_mission_loop_boundary_available: bool = True
    process_state_driven_next_action_boundary_available: bool = True
    agent_to_subagent_prompt_boundary_available: bool = True
    human_handoff_prompt_boundary_available: bool = True
    ready_for_v0391_approval_artifact_intake: bool = True
    ready_for_v0392_sandbox_workspace_isolation: bool = True
    ready_for_v0393_human_approved_patch_materialization_sandbox_apply: bool = True
    ready_for_v0394_post_apply_controlled_retest: bool = True
    ready_for_v0395_before_after_repair_outcome_comparison: bool = True
    ready_for_v0396_pi_native_repair_process_state_reconstruction: bool = True
    ready_for_v0397_self_prompting_next_action_draft: bool = True
    ready_for_v0398_cli_sandbox_repair_apply_retest_loop_state_surface: bool = True
    ready_for_v0399_consolidation: bool = True
    ready_for_human_approved_sandbox_repair_apply_boundary: bool = True
    ready_for_approval_artifact_intake_boundary: bool = True
    ready_for_approval_scope_validation_boundary: bool = True
    ready_for_sandbox_repair_workspace_isolation_boundary: bool = True
    ready_for_sandbox_patch_materialization_boundary: bool = True
    ready_for_sandbox_repair_apply_boundary: bool = True
    ready_for_post_apply_controlled_retest_boundary: bool = True
    ready_for_before_after_repair_comparison_boundary: bool = True
    ready_for_repair_effectiveness_assessment_boundary: bool = True
    ready_for_repair_process_state_projection_boundary: bool = True
    ready_for_ocel_style_repair_event_envelope_boundary: bool = True
    ready_for_ocpx_style_repair_state_reconstruction_boundary: bool = True
    ready_for_pig_repair_diagnostic_recommendation_boundary: bool = True
    ready_for_self_prompting_mission_loop_boundary: bool = True
    ready_for_process_state_driven_next_action_draft_boundary: bool = True
    ready_for_agent_to_subagent_prompt_draft_boundary: bool = True
    ready_for_human_handoff_prompt_boundary: bool = True
    ready_for_execution: bool = False
    ready_for_general_execution: bool = False
    ready_for_approval_artifact_intake: bool = False
    ready_for_approval_scope_validation: bool = False
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
class RepairApplyBoundarySourceRef:
    source_ref_id: str
    source_kind: RepairApplyBoundarySourceKind | str
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
class RepairApplyBoundaryPolicy:
    policy_id: str
    version: str
    allowed_modes: list[RepairApplyBoundaryMode | str]
    allowed_boundary_kinds: list[RepairApplyBoundaryKind | str]
    allowed_self_prompting_boundary_kinds: list[SelfPromptingMissionLoopBoundaryKind | str]
    required_prior_versions: list[str]
    required_future_stage_gates: list[str]
    require_human_approval_for_future_apply: bool = True
    require_sandbox_only_for_future_apply: bool = True
    require_no_live_apply: bool = True
    require_controlled_retest_boundary: bool = True
    require_before_after_comparison_boundary: bool = True
    require_pi_process_state_boundary: bool = True
    require_self_prompting_no_execution_boundary: bool = True
    require_subagent_no_invocation_boundary: bool = True
    require_human_handoff_boundary: bool = True
    allow_boundary_definition: bool = True
    allow_future_stage_gate_metadata: bool = True
    allow_approval_artifact_intake_boundary: bool = True
    allow_sandbox_workspace_isolation_boundary: bool = True
    allow_sandbox_patch_materialization_boundary: bool = True
    allow_sandbox_apply_boundary: bool = True
    allow_post_apply_retest_boundary: bool = True
    allow_before_after_comparison_boundary: bool = True
    allow_process_state_boundary: bool = True
    allow_self_prompting_boundary: bool = True
    allow_next_action_draft_boundary: bool = True
    allow_agent_to_subagent_prompt_boundary: bool = True
    allow_human_handoff_boundary: bool = True
    allow_approval_artifact_intake: bool = False
    allow_approval_capture: bool = False
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
    allow_next_action_draft_generation: bool = False
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
        for name in ("allowed_modes", "allowed_boundary_kinds", "allowed_self_prompting_boundary_kinds", "required_prior_versions", "required_future_stage_gates"):
            _validate_list(name, getattr(self, name))
        _validate_true(
            self,
            [
                "require_human_approval_for_future_apply",
                "require_sandbox_only_for_future_apply",
                "require_no_live_apply",
                "require_self_prompting_no_execution_boundary",
                "require_subagent_no_invocation_boundary",
                "require_human_handoff_boundary",
            ],
        )
        _validate_false(self, UNSAFE_POLICY_ALLOW_NAMES)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class HumanApprovedSandboxRepairApplyBoundary:
    boundary_id: str
    version: str
    policy: RepairApplyBoundaryPolicy
    source_refs: list[RepairApplyBoundarySourceRef]
    boundary_summary: str
    required_human_approval_future_gate: bool = True
    sandbox_only_future_gate: bool = True
    live_workspace_apply_blocked: bool = True
    approval_capture_blocked_in_v0390: bool = True
    apply_execution_blocked_in_v0390: bool = True
    test_execution_blocked_in_v0390: bool = True
    repair_execution_blocked_in_v0390: bool = True
    future_v0391_gate_open: bool = True
    future_v0392_gate_open: bool = True
    future_v0393_gate_open: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_id", self.boundary_id)
        _validate_version(self.version)
        _require_non_blank("boundary_summary", self.boundary_summary)
        _validate_list("source_refs", self.source_refs)
        _validate_true(
            self,
            [
                "required_human_approval_future_gate",
                "sandbox_only_future_gate",
                "live_workspace_apply_blocked",
                "approval_capture_blocked_in_v0390",
                "apply_execution_blocked_in_v0390",
                "test_execution_blocked_in_v0390",
                "repair_execution_blocked_in_v0390",
            ],
        )
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class SelfPromptingMissionLoopBoundary:
    self_prompting_boundary_id: str
    version: str
    loop_definition: str
    canonical_name: str
    rejected_external_terms: list[str]
    accepted_internal_terms: list[str]
    boundary_kinds: list[SelfPromptingMissionLoopBoundaryKind | str]
    process_state_required: bool = True
    mission_objective_required: bool = True
    verification_contract_required: bool = True
    policy_boundary_required: bool = True
    human_handoff_required: bool = True
    self_prompt_generation_blocked_in_v0390: bool = True
    self_prompt_auto_execution_blocked: bool = True
    next_action_auto_execution_blocked: bool = True
    subagent_prompt_generation_blocked_in_v0390: bool = True
    subagent_auto_invocation_blocked: bool = True
    autonomous_continuation_blocked: bool = True
    model_provider_invocation_blocked: bool = True
    external_agent_execution_blocked: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("self_prompting_boundary_id", "version", "loop_definition", "canonical_name"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        if self.canonical_name != SELF_PROMPTING_CANONICAL_NAME:
            raise ValueError("canonical_name should be Self-Prompting Mission Loop")
        for name in ("rejected_external_terms", "accepted_internal_terms", "boundary_kinds"):
            _validate_list(name, getattr(self, name))
        if "Loop Engineering as top-level ChantaCore concept" not in self.rejected_external_terms:
            raise ValueError("Loop Engineering must be rejected as top-level ChantaCore concept")
        for term in (
            "Self-Prompting Mission Loop",
            "PI-native Mission Execution Loop",
            "Process-State-Driven Self-Prompting",
            "Agent-to-Subagent Prompting Cycle",
        ):
            if term not in self.accepted_internal_terms:
                raise ValueError(f"accepted_internal_terms must include {term}")
        _validate_true(
            self,
            [
                "process_state_required",
                "mission_objective_required",
                "verification_contract_required",
                "policy_boundary_required",
                "human_handoff_required",
                "self_prompt_generation_blocked_in_v0390",
                "self_prompt_auto_execution_blocked",
                "next_action_auto_execution_blocked",
                "subagent_prompt_generation_blocked_in_v0390",
                "subagent_auto_invocation_blocked",
                "autonomous_continuation_blocked",
                "model_provider_invocation_blocked",
                "external_agent_execution_blocked",
            ],
        )
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class ProcessStateDrivenNextActionBoundary:
    next_action_boundary_id: str
    version: str
    boundary_summary: str
    required_inputs: list[str]
    future_output_artifacts: list[str]
    oc_el_style_event_envelope_future_gate: bool = True
    ocpx_state_reconstruction_future_gate: bool = True
    pig_recommendation_future_gate: bool = True
    next_action_draft_future_gate: bool = True
    execution_blocked: bool = True
    self_prompt_auto_execution_blocked: bool = True
    subagent_invocation_blocked: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("next_action_boundary_id", self.next_action_boundary_id)
        _validate_version(self.version)
        _require_non_blank("boundary_summary", self.boundary_summary)
        _validate_list("required_inputs", self.required_inputs)
        _validate_list("future_output_artifacts", self.future_output_artifacts)
        _validate_true(self, ["execution_blocked", "self_prompt_auto_execution_blocked", "subagent_invocation_blocked"])
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class AgentToSubagentPromptBoundary:
    subagent_prompt_boundary_id: str
    version: str
    boundary_summary: str
    future_prompt_draft_allowed: bool = True
    future_verification_prompt_draft_allowed: bool = True
    subagent_invocation_allowed_now: bool = False
    external_agent_invocation_allowed_now: bool = False
    model_provider_invocation_allowed_now: bool = False
    automatic_dispatch_allowed_now: bool = False
    human_handoff_required: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("subagent_prompt_boundary_id", self.subagent_prompt_boundary_id)
        _validate_version(self.version)
        _require_non_blank("boundary_summary", self.boundary_summary)
        _validate_false(
            self,
            [
                "subagent_invocation_allowed_now",
                "external_agent_invocation_allowed_now",
                "model_provider_invocation_allowed_now",
                "automatic_dispatch_allowed_now",
            ],
        )
        _validate_true(self, ["human_handoff_required"])
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairApplyBoundaryDecision:
    decision_id: str
    decision_kind: RepairApplyBoundaryDecisionKind | str
    status: RepairApplyBoundaryStatus | str
    readiness_level: RepairApplyBoundaryReadinessLevel | str
    decision_summary: str
    evidence_refs: list[str]
    ready_for_v0391: bool = True
    ready_for_v0392: bool = True
    ready_for_v0393: bool = True
    ready_for_v0394: bool = True
    ready_for_v0395: bool = True
    ready_for_v0396: bool = True
    ready_for_v0397: bool = True
    ready_for_v0398: bool = True
    ready_for_v0399: bool = True
    approval_capture_allowed_now: bool = False
    apply_allowed_now: bool = False
    sandbox_apply_allowed_now: bool = False
    live_apply_allowed_now: bool = False
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
        _require_non_blank("decision_id", self.decision_id)
        _require_non_blank("decision_summary", self.decision_summary)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_false(self, UNSAFE_DECISION_NAMES)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairApplyBoundaryValidationFinding:
    finding_id: str
    finding_summary: str
    risk_kind: RepairApplyBoundaryRiskKind | str
    blocked: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("finding_summary", self.finding_summary)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairApplyBoundaryValidationReport:
    validation_report_id: str
    version: str
    validation_summary: str
    findings: list[RepairApplyBoundaryValidationFinding]
    boundary_only_confirmed: bool = True
    no_approval_capture_confirmed: bool = True
    no_apply_confirmed: bool = True
    no_test_execution_confirmed: bool = True
    no_self_prompt_execution_confirmed: bool = True
    no_subagent_invocation_confirmed: bool = True
    no_external_agent_confirmed: bool = True
    no_model_provider_confirmed: bool = True
    no_repair_execution_confirmed: bool = True
    no_dominion_confirmed: bool = True
    no_production_certification_confirmed: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version(self.version)
        _require_non_blank("validation_summary", self.validation_summary)
        _validate_list("findings", self.findings)
        _validate_true(
            self,
            [
                "boundary_only_confirmed",
                "no_approval_capture_confirmed",
                "no_apply_confirmed",
                "no_test_execution_confirmed",
                "no_self_prompt_execution_confirmed",
                "no_subagent_invocation_confirmed",
                "no_external_agent_confirmed",
                "no_model_provider_confirmed",
                "no_repair_execution_confirmed",
                "no_dominion_confirmed",
                "no_production_certification_confirmed",
            ],
        )
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairApplyBoundaryRunPreview:
    run_preview_id: str
    version: str
    preview_summary: str
    boundary_modes: list[RepairApplyBoundaryMode | str]
    future_stage_gates: list[str]
    preview_only: bool = True
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        _validate_version(self.version)
        _require_non_blank("preview_summary", self.preview_summary)
        _validate_list("boundary_modes", self.boundary_modes)
        _validate_list("future_stage_gates", self.future_stage_gates)
        _validate_true(self, ["preview_only"])
        _validate_false(self, ["ready_for_execution"])
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairApplyBoundaryNoExecutionGuarantee:
    guarantee_id: str
    version: str
    guarantee_summary: str
    no_approval_capture: bool = True
    no_approval_grant: bool = True
    no_apply_permission: bool = True
    no_sandbox_apply: bool = True
    no_live_apply: bool = True
    no_patch_file_write: bool = True
    no_patch_application: bool = True
    no_apply_patch: bool = True
    no_git_apply: bool = True
    no_test_execution: bool = True
    no_self_prompt_generation: bool = True
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
class V0390ReadinessReport:
    report_id: str
    version: str
    release_name: str
    track_name: str
    boundary: HumanApprovedSandboxRepairApplyBoundary
    self_prompting_boundary: SelfPromptingMissionLoopBoundary
    next_action_boundary: ProcessStateDrivenNextActionBoundary
    subagent_prompt_boundary: AgentToSubagentPromptBoundary
    decision: RepairApplyBoundaryDecision
    flags: RepairApplyBoundaryFlagSet
    source_refs: list[RepairApplyBoundarySourceRef]
    report_summary: str
    ready_for_v039_track: bool = True
    ready_for_v0391_approval_artifact_intake: bool = True
    ready_for_v0392_sandbox_workspace_isolation: bool = True
    ready_for_v0393_sandbox_patch_materialization_apply: bool = True
    ready_for_v0394_post_apply_retest: bool = True
    ready_for_v0395_before_after_comparison: bool = True
    ready_for_v0396_pi_process_state_reconstruction: bool = True
    ready_for_v0397_self_prompting_next_action_draft: bool = True
    ready_for_v0398_cli_surface: bool = True
    ready_for_v0399_consolidation: bool = True
    approval_capture_enabled: bool = False
    apply_enabled: bool = False
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
        if "Human-approved Sandbox Repair Apply Boundary" not in self.release_name:
            raise ValueError("release_name should mention Human-approved Sandbox Repair Apply Boundary")
        if "Human-approved Sandbox Repair Apply & Re-test Loop" not in self.track_name:
            raise ValueError("track_name should mention Human-approved Sandbox Repair Apply & Re-test Loop")
        _validate_list("source_refs", self.source_refs)
        _validate_false(self, UNSAFE_REPORT_NAMES)
        if not repair_apply_boundary_flags_preserve_no_execution(self.flags):
            raise ValueError("flags must preserve no execution")
        _validate_dict("metadata", self.metadata)


def build_repair_apply_boundary_flags(**overrides: Any) -> RepairApplyBoundaryFlagSet:
    return RepairApplyBoundaryFlagSet(flag_set_id="v0390-repair-apply-boundary-flags", **overrides)


def build_repair_apply_boundary_source_ref(**overrides: Any) -> RepairApplyBoundarySourceRef:
    defaults = {
        "source_ref_id": "v0390-source-ref",
        "source_kind": RepairApplyBoundarySourceKind.V0389_HANDOFF_PACKET,
        "source_id": "v039-handoff-packet",
        "source_summary": "v0.38.9 future-track handoff metadata for v0.39 boundary foundation.",
        "evidence_refs": ["v0.38.9 consolidation report"],
    }
    return RepairApplyBoundarySourceRef(**_with_overrides(defaults, overrides))


def build_repair_apply_boundary_policy(**overrides: Any) -> RepairApplyBoundaryPolicy:
    defaults = {
        "policy_id": "v0390-repair-apply-boundary-policy",
        "version": V0390_VERSION,
        "allowed_modes": [item.value for item in RepairApplyBoundaryMode if item not in {RepairApplyBoundaryMode.UNKNOWN}],
        "allowed_boundary_kinds": [item.value for item in RepairApplyBoundaryKind if item is not RepairApplyBoundaryKind.UNKNOWN],
        "allowed_self_prompting_boundary_kinds": [
            item.value for item in SelfPromptingMissionLoopBoundaryKind if item is not SelfPromptingMissionLoopBoundaryKind.UNKNOWN
        ],
        "required_prior_versions": ["v0.36.9", "v0.37.9", "v0.38.9"],
        "required_future_stage_gates": [
            "v0.39.1",
            "v0.39.2",
            "v0.39.3",
            "v0.39.4",
            "v0.39.5",
            "v0.39.6",
            "v0.39.7",
            "v0.39.8",
            "v0.39.9",
        ],
    }
    return RepairApplyBoundaryPolicy(**_with_overrides(defaults, overrides))


def default_repair_apply_boundary_policy(**overrides: Any) -> RepairApplyBoundaryPolicy:
    return build_repair_apply_boundary_policy(**overrides)


def build_human_approved_sandbox_repair_apply_boundary(**overrides: Any) -> HumanApprovedSandboxRepairApplyBoundary:
    defaults = {
        "boundary_id": "v0390-human-approved-sandbox-repair-apply-boundary",
        "version": V0390_VERSION,
        "policy": default_repair_apply_boundary_policy(),
        "source_refs": [build_repair_apply_boundary_source_ref()],
        "boundary_summary": "Defines future human-approved sandbox repair apply boundaries without approval intake or apply execution.",
    }
    return HumanApprovedSandboxRepairApplyBoundary(**_with_overrides(defaults, overrides))


def build_self_prompting_mission_loop_boundary(**overrides: Any) -> SelfPromptingMissionLoopBoundary:
    defaults = {
        "self_prompting_boundary_id": "v0390-self-prompting-mission-loop-boundary",
        "version": V0390_VERSION,
        "loop_definition": (
            "PI-native mission execution structure using mission objective, process-state projection, trace history, "
            "verification contract, policy boundary, and PIG-style recommendation metadata to draft future prompt/action requests."
        ),
        "canonical_name": SELF_PROMPTING_CANONICAL_NAME,
        "rejected_external_terms": ["Loop Engineering as top-level ChantaCore concept"],
        "accepted_internal_terms": [
            "Self-Prompting Mission Loop",
            "PI-native Mission Execution Loop",
            "Process-State-Driven Self-Prompting",
            "Agent-to-Subagent Prompting Cycle",
        ],
        "boundary_kinds": [item.value for item in SelfPromptingMissionLoopBoundaryKind if item is not SelfPromptingMissionLoopBoundaryKind.UNKNOWN],
    }
    return SelfPromptingMissionLoopBoundary(**_with_overrides(defaults, overrides))


def build_process_state_driven_next_action_boundary(**overrides: Any) -> ProcessStateDrivenNextActionBoundary:
    defaults = {
        "next_action_boundary_id": "v0390-process-state-next-action-boundary",
        "version": V0390_VERSION,
        "boundary_summary": "Defines future process-state-driven next-action draft boundaries without generation or execution.",
        "required_inputs": [
            "mission objective",
            "process-state projection",
            "trace history reference",
            "verification contract",
            "policy boundary",
            "PIG recommendation metadata",
        ],
        "future_output_artifacts": [
            "OCEL-style event envelope metadata",
            "OCPX-style process-state reconstruction metadata",
            "PIG diagnostic recommendation metadata",
            "next-action draft metadata",
        ],
    }
    return ProcessStateDrivenNextActionBoundary(**_with_overrides(defaults, overrides))


def build_agent_to_subagent_prompt_boundary(**overrides: Any) -> AgentToSubagentPromptBoundary:
    defaults = {
        "subagent_prompt_boundary_id": "v0390-agent-to-subagent-prompt-boundary",
        "version": V0390_VERSION,
        "boundary_summary": "Defines future agent-to-subagent prompt draft boundaries without invocation or dispatch.",
    }
    return AgentToSubagentPromptBoundary(**_with_overrides(defaults, overrides))


def build_repair_apply_boundary_decision(**overrides: Any) -> RepairApplyBoundaryDecision:
    defaults = {
        "decision_id": "v0390-repair-apply-boundary-decision",
        "decision_kind": RepairApplyBoundaryDecisionKind.ALLOW_BOUNDARY_DEFINITION,
        "status": RepairApplyBoundaryStatus.BOUNDARY_DEFINED,
        "readiness_level": RepairApplyBoundaryReadinessLevel.V039_TRACK_BOUNDARY_READY,
        "decision_summary": "v0.39.0 boundary metadata may be created; runtime actions remain blocked.",
        "evidence_refs": ["v0.38.9 handoff packet", "v0.39.0 boundary policy"],
    }
    return RepairApplyBoundaryDecision(**_with_overrides(defaults, overrides))


def build_repair_apply_boundary_validation_finding(**overrides: Any) -> RepairApplyBoundaryValidationFinding:
    defaults = {
        "finding_id": "v0390-boundary-validation-finding",
        "finding_summary": "Runtime action remains blocked by v0.39.0 boundary policy.",
        "risk_kind": RepairApplyBoundaryRiskKind.APPLY_PERMISSION_CONFUSION_RISK,
        "blocked": True,
    }
    return RepairApplyBoundaryValidationFinding(**_with_overrides(defaults, overrides))


def build_repair_apply_boundary_validation_report(**overrides: Any) -> RepairApplyBoundaryValidationReport:
    defaults = {
        "validation_report_id": "v0390-boundary-validation-report",
        "version": V0390_VERSION,
        "validation_summary": "Validation confirms v0.39.0 boundary-only behavior.",
        "findings": [build_repair_apply_boundary_validation_finding()],
    }
    return RepairApplyBoundaryValidationReport(**_with_overrides(defaults, overrides))


def build_repair_apply_boundary_run_preview(**overrides: Any) -> RepairApplyBoundaryRunPreview:
    defaults = {
        "run_preview_id": "v0390-boundary-run-preview",
        "version": V0390_VERSION,
        "preview_summary": "Preview of boundary metadata only; no runtime action is started.",
        "boundary_modes": [RepairApplyBoundaryMode.HUMAN_APPROVED_SANDBOX_REPAIR_APPLY_BOUNDARY.value],
        "future_stage_gates": ["v0.39.1", "v0.39.2", "v0.39.3", "v0.39.4", "v0.39.5", "v0.39.6", "v0.39.7", "v0.39.8", "v0.39.9"],
    }
    return RepairApplyBoundaryRunPreview(**_with_overrides(defaults, overrides))


def build_repair_apply_boundary_no_execution_guarantee(**overrides: Any) -> RepairApplyBoundaryNoExecutionGuarantee:
    defaults = {
        "guarantee_id": "v0390-no-execution-guarantee",
        "version": V0390_VERSION,
        "guarantee_summary": "v0.39.0 boundary foundation does not execute approval, apply, test, self-prompt, subagent, repair, or Dominion runtime.",
    }
    return RepairApplyBoundaryNoExecutionGuarantee(**_with_overrides(defaults, overrides))


def build_v0390_readiness_report(**overrides: Any) -> V0390ReadinessReport:
    defaults = {
        "report_id": "v0390-readiness-report",
        "version": V0390_VERSION,
        "release_name": V0390_RELEASE_NAME,
        "track_name": V039_TRACK_NAME,
        "boundary": build_human_approved_sandbox_repair_apply_boundary(),
        "self_prompting_boundary": build_self_prompting_mission_loop_boundary(),
        "next_action_boundary": build_process_state_driven_next_action_boundary(),
        "subagent_prompt_boundary": build_agent_to_subagent_prompt_boundary(),
        "decision": build_repair_apply_boundary_decision(),
        "flags": build_repair_apply_boundary_flags(),
        "source_refs": [build_repair_apply_boundary_source_ref()],
        "report_summary": "v0.39.0 opens boundary readiness only for human-approved sandbox repair apply and PI-native self-prompting mission loop stages.",
    }
    return V0390ReadinessReport(**_with_overrides(defaults, overrides))


def repair_apply_boundary_flags_preserve_no_execution(flags: RepairApplyBoundaryFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_FLAG_NAMES)


def repair_apply_boundary_policy_blocks_apply_and_execution(policy: RepairApplyBoundaryPolicy) -> bool:
    return all(getattr(policy, name) is False for name in UNSAFE_POLICY_ALLOW_NAMES)


def self_prompting_boundary_is_not_self_execution(boundary: SelfPromptingMissionLoopBoundary) -> bool:
    return (
        boundary.self_prompt_generation_blocked_in_v0390
        and boundary.self_prompt_auto_execution_blocked
        and boundary.next_action_auto_execution_blocked
        and boundary.autonomous_continuation_blocked
    )


def next_action_boundary_is_not_next_action_execution(boundary: ProcessStateDrivenNextActionBoundary) -> bool:
    return boundary.execution_blocked and boundary.self_prompt_auto_execution_blocked and boundary.subagent_invocation_blocked


def subagent_prompt_boundary_is_not_invocation(boundary: AgentToSubagentPromptBoundary) -> bool:
    return (
        not boundary.subagent_invocation_allowed_now
        and not boundary.external_agent_invocation_allowed_now
        and not boundary.model_provider_invocation_allowed_now
        and not boundary.automatic_dispatch_allowed_now
        and boundary.human_handoff_required
    )


def v0390_readiness_report_is_not_execution_ready(report: V0390ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_REPORT_NAMES) and repair_apply_boundary_flags_preserve_no_execution(report.flags)

