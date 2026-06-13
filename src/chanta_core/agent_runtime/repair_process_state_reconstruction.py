"""v0.39.6 PI-native repair process-state reconstruction metadata.

This module reconstructs process-state from supplied metadata only. It does not
persist traces, write OCEL/JSONL/OCPX artifacts, execute PIG recommendations,
generate prompts, invoke agents/providers, run tests, apply patches, execute
repair, run loops, start Dominion runtime, or certify production readiness.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank


V0396_VERSION = "v0.39.6"
V0396_RELEASE_NAME = "v0.39.6 PI-native Repair Process-State Reconstruction"
V039_TRACK_NAME = "Human-approved Sandbox Repair Apply & Re-test Loop with PI-native Self-Prompting Mission Loop Boundary"

PROHIBITED_RUNTIME_ACTIONS = [
    "ocel_write",
    "ocpx_persistence",
    "pig_execution",
    "self_prompt_generation",
    "self_prompt_execution",
    "subagent_invocation",
    "model_provider",
    "external_agent",
    "test_execution",
    "patch_apply",
    "rollback",
    "repair_execution",
    "Dominion",
]


class RepairProcessStateMode(StrEnum):
    PI_NATIVE_REPAIR_PROCESS_STATE_RECONSTRUCTION = "pi_native_repair_process_state_reconstruction"
    OCEL_STYLE_REPAIR_EVENT_ENVELOPE = "ocel_style_repair_event_envelope"
    REPAIR_OBJECT_REFERENCE_MODEL = "repair_object_reference_model"
    REPAIR_OBJECT_RELATION_SNAPSHOT = "repair_object_relation_snapshot"
    REPAIR_TRACE_SEGMENT_RECONSTRUCTION = "repair_trace_segment_reconstruction"
    OCPX_STYLE_REPAIR_STATE_PROJECTION = "ocpx_style_repair_state_projection"
    REPAIR_PROCESS_STATE_TRANSITION = "repair_process_state_transition"
    REPAIR_MISSION_STATE_PROJECTION = "repair_mission_state_projection"
    PIG_DIAGNOSTIC_INPUT_CONTEXT = "pig_diagnostic_input_context"
    FUTURE_SELF_PROMPTING_NEXT_ACTION_INPUT = "future_self_prompting_next_action_input"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairProcessStateSourceKind(StrEnum):
    V0395_OUTCOME_COMPARISON_REPORT = "v0395_outcome_comparison_report"
    V0395_EFFECTIVENESS_ASSESSMENT = "v0395_effectiveness_assessment"
    V0395_REGRESSION_SIGNAL = "v0395_regression_signal"
    V0395_FAILURE_DELTA_ASSESSMENT = "v0395_failure_delta_assessment"
    V0395_DO_NOTHING_COMPARISON = "v0395_do_nothing_comparison"
    V0394_POST_APPLY_RETEST_RESULT = "v0394_post_apply_retest_result"
    V0394_POST_APPLY_RETEST_RUN_RECORD = "v0394_post_apply_retest_run_record"
    V0394_POST_APPLY_OUTPUT_CAPTURE = "v0394_post_apply_output_capture"
    V0394_POST_APPLY_RETEST_AUDIT = "v0394_post_apply_retest_audit"
    V0393_SANDBOX_APPLY_RESULT = "v0393_sandbox_apply_result"
    V0393_SANDBOX_APPLY_TRANSACTION = "v0393_sandbox_apply_transaction"
    V0393_SANDBOX_APPLY_AUDIT = "v0393_sandbox_apply_audit"
    V0392_WORKSPACE_DESCRIPTOR = "v0392_workspace_descriptor"
    V0392_WORKSPACE_ISOLATION_DECISION = "v0392_workspace_isolation_decision"
    V0392_TARGET_BINDING = "v0392_target_binding"
    V0391_APPROVAL_ARTIFACT_DECISION = "v0391_approval_artifact_decision"
    V0391_APPROVAL_PROCESS_STATE_GATE = "v0391_approval_process_state_gate"
    V0385_SAFETY_REPORT = "v0385_safety_report"
    V0384_PROPOSED_PATCH_ENVELOPE = "v0384_proposed_patch_envelope"
    V0384_PROPOSED_CODE_HUNK = "v0384_proposed_code_hunk"
    V037_BEFORE_TEST_RESULT = "v037_before_test_result"
    MANUAL_OPERATOR_NOTE = "manual_operator_note"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class RepairProcessStateStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    INPUT_VALIDATED = "input_validated"
    EVENT_ENVELOPES_CREATED = "event_envelopes_created"
    OBJECT_REFS_CREATED = "object_refs_created"
    OBJECT_RELATIONS_CREATED = "object_relations_created"
    TRACE_SEGMENTS_CREATED = "trace_segments_created"
    PROCESS_STATE_PROJECTED = "process_state_projected"
    PROCESS_STATE_TRANSITION_CREATED = "process_state_transition_created"
    MISSION_STATE_PROJECTED = "mission_state_projected"
    DIAGNOSTIC_CONTEXT_CREATED = "diagnostic_context_created"
    PIG_INPUT_CONTEXT_CREATED = "pig_input_context_created"
    RECONSTRUCTION_COMPLETED = "reconstruction_completed"
    RECONSTRUCTION_COMPLETED_WITH_WARNINGS = "reconstruction_completed_with_warnings"
    RECONSTRUCTION_INCONCLUSIVE = "reconstruction_inconclusive"
    READY_FOR_FUTURE_SELF_PROMPTING_NEXT_ACTION_DRAFT = "ready_for_future_self_prompting_next_action_draft"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    REVIEW_REQUIRED = "review_required"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class RepairProcessStateReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    EVENT_ENVELOPE_READY = "event_envelope_ready"
    OBJECT_REFERENCE_READY = "object_reference_ready"
    OBJECT_RELATION_READY = "object_relation_ready"
    TRACE_SEGMENT_READY = "trace_segment_ready"
    PROCESS_STATE_PROJECTION_READY = "process_state_projection_ready"
    PROCESS_STATE_TRANSITION_READY = "process_state_transition_ready"
    MISSION_STATE_PROJECTION_READY = "mission_state_projection_ready"
    DIAGNOSTIC_CONTEXT_READY = "diagnostic_context_ready"
    PIG_INPUT_CONTEXT_READY = "pig_input_context_ready"
    FUTURE_SELF_PROMPTING_INPUT_READY = "future_self_prompting_input_ready"
    DESIGN_HANDOFF_READY_FOR_V0397 = "design_handoff_ready_for_v0397"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class RepairProcessStateDecisionKind(StrEnum):
    ALLOW_EVENT_ENVELOPE_RECONSTRUCTION = "allow_event_envelope_reconstruction"
    ALLOW_OBJECT_REFERENCE_MODELING = "allow_object_reference_modeling"
    ALLOW_OBJECT_RELATION_SNAPSHOT = "allow_object_relation_snapshot"
    ALLOW_TRACE_SEGMENT_RECONSTRUCTION = "allow_trace_segment_reconstruction"
    ALLOW_PROCESS_STATE_PROJECTION = "allow_process_state_projection"
    ALLOW_PROCESS_STATE_TRANSITION = "allow_process_state_transition"
    ALLOW_MISSION_STATE_PROJECTION = "allow_mission_state_projection"
    ALLOW_DIAGNOSTIC_CONTEXT = "allow_diagnostic_context"
    ALLOW_PIG_INPUT_CONTEXT = "allow_pig_input_context"
    ALLOW_FUTURE_SELF_PROMPTING_NEXT_ACTION_INPUT = "allow_future_self_prompting_next_action_input"
    CHOOSE_EFFECTIVE_REPAIR_STATE = "choose_effective_repair_state"
    CHOOSE_REGRESSIVE_REPAIR_STATE = "choose_regressive_repair_state"
    CHOOSE_INCONCLUSIVE_REPAIR_STATE = "choose_inconclusive_repair_state"
    CHOOSE_DO_NOTHING = "choose_do_nothing"
    CHOOSE_HUMAN_REVIEW_REQUIRED = "choose_human_review_required"
    DENY = "deny"
    BLOCK = "block"
    REJECT_MISSING_OUTCOME_COMPARISON = "reject_missing_outcome_comparison"
    REJECT_MISSING_APPLY_RESULT = "reject_missing_apply_result"
    REJECT_MISSING_RETEST_RESULT = "reject_missing_retest_result"
    REJECT_INVALID_COMPARISON = "reject_invalid_comparison"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class RepairProcessStateRiskKind(StrEnum):
    MISSING_OUTCOME_COMPARISON_RISK = "missing_outcome_comparison_risk"
    MISSING_APPLY_RESULT_RISK = "missing_apply_result_risk"
    MISSING_RETEST_RESULT_RISK = "missing_retest_result_risk"
    INCOMPLETE_TRACE_RISK = "incomplete_trace_risk"
    INCONSISTENT_TRACE_RISK = "inconsistent_trace_risk"
    OBJECT_RELATION_GAP_RISK = "object_relation_gap_risk"
    INCOMPARABLE_STATE_RISK = "incomparable_state_risk"
    REGRESSION_UNDERREPRESENTED_RISK = "regression_underrepresented_risk"
    EFFECTIVENESS_OVERCLAIM_RISK = "effectiveness_overclaim_risk"
    CORRECTNESS_OVERCLAIM_RISK = "correctness_overclaim_risk"
    PROCESS_STATE_AUTHORITY_CONFUSION_RISK = "process_state_authority_confusion_risk"
    PIG_RECOMMENDATION_AUTHORITY_CONFUSION_RISK = "pig_recommendation_authority_confusion_risk"
    OCEL_PERSISTENCE_CONFUSION_RISK = "ocel_persistence_confusion_risk"
    OCPX_PERSISTENCE_CONFUSION_RISK = "ocpx_persistence_confusion_risk"
    TRACE_PERSISTENCE_CONFUSION_RISK = "trace_persistence_confusion_risk"
    SELF_PROMPT_GENERATION_CONFUSION_RISK = "self_prompt_generation_confusion_risk"
    SELF_PROMPT_EXECUTION_CONFUSION_RISK = "self_prompt_execution_confusion_risk"
    NEXT_ACTION_EXECUTION_CONFUSION_RISK = "next_action_execution_confusion_risk"
    SUBAGENT_INVOCATION_CONFUSION_RISK = "subagent_invocation_confusion_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    MODEL_PROVIDER_INVOCATION_RISK = "model_provider_invocation_risk"
    AUTONOMOUS_LOOP_RUNTIME_RISK = "autonomous_loop_runtime_risk"
    RETRY_LOOP_RISK = "retry_loop_risk"
    MULTI_CYCLE_LOOP_RISK = "multi_cycle_loop_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    UNKNOWN = "unknown"


class RepairProcessEventKind(StrEnum):
    APPROVAL_ARTIFACT_RECEIVED = "approval_artifact_received"
    APPROVAL_GATE_SATISFIED = "approval_gate_satisfied"
    WORKSPACE_ISOLATION_VALIDATED = "workspace_isolation_validated"
    PATCH_MATERIALIZED_IN_MEMORY = "patch_materialized_in_memory"
    SANDBOX_APPLY_STARTED = "sandbox_apply_started"
    SANDBOX_APPLY_COMPLETED = "sandbox_apply_completed"
    SANDBOX_APPLY_FAILED = "sandbox_apply_failed"
    CONTROLLED_RETEST_STARTED = "controlled_retest_started"
    CONTROLLED_RETEST_COMPLETED = "controlled_retest_completed"
    CONTROLLED_RETEST_FAILED = "controlled_retest_failed"
    OUTCOME_COMPARISON_COMPLETED = "outcome_comparison_completed"
    REGRESSION_SIGNAL_DETECTED = "regression_signal_detected"
    EFFECTIVENESS_ASSESSED = "effectiveness_assessed"
    DO_NOTHING_COMPARED = "do_nothing_compared"
    HUMAN_HANDOFF_REQUIRED = "human_handoff_required"
    UNKNOWN = "unknown"


class RepairProcessObjectKind(StrEnum):
    REPAIR_MISSION = "repair_mission"
    APPROVAL_ARTIFACT = "approval_artifact"
    APPROVAL_GATE = "approval_gate"
    SANDBOX_WORKSPACE = "sandbox_workspace"
    PROPOSED_PATCH_ENVELOPE = "proposed_patch_envelope"
    PROPOSED_CODE_HUNK = "proposed_code_hunk"
    SANDBOX_APPLY_TRANSACTION = "sandbox_apply_transaction"
    SANDBOX_APPLY_RESULT = "sandbox_apply_result"
    CONTROLLED_RETEST_RUN = "controlled_retest_run"
    CONTROLLED_RETEST_RESULT = "controlled_retest_result"
    BEFORE_TEST_RESULT = "before_test_result"
    AFTER_TEST_RESULT = "after_test_result"
    OUTCOME_COMPARISON = "outcome_comparison"
    EFFECTIVENESS_ASSESSMENT = "effectiveness_assessment"
    REGRESSION_SIGNAL = "regression_signal"
    DO_NOTHING_COMPARISON = "do_nothing_comparison"
    PROCESS_STATE_PROJECTION = "process_state_projection"
    HUMAN_HANDOFF = "human_handoff"
    UNKNOWN = "unknown"


class RepairProcessRelationKind(StrEnum):
    APPROVES = "approves"
    GATES = "gates"
    TARGETS = "targets"
    MATERIALIZES = "materializes"
    APPLIES_TO = "applies_to"
    MODIFIES = "modifies"
    PRODUCES = "produces"
    VERIFIES = "verifies"
    COMPARES = "compares"
    IMPROVES = "improves"
    REGRESSES = "regresses"
    LEAVES_RESIDUAL_FAILURE = "leaves_residual_failure"
    REQUIRES_HUMAN_REVIEW = "requires_human_review"
    FEEDS_FUTURE_STATE = "feeds_future_state"
    BLOCKS = "blocks"
    UNKNOWN = "unknown"


class RepairProcessStateKind(StrEnum):
    PROPOSAL_READY = "proposal_ready"
    APPROVAL_GATE_READY = "approval_gate_ready"
    WORKSPACE_ISOLATED = "workspace_isolated"
    SANDBOX_APPLY_COMPLETED = "sandbox_apply_completed"
    SANDBOX_APPLY_FAILED = "sandbox_apply_failed"
    RETEST_COMPLETED = "retest_completed"
    RETEST_FAILED = "retest_failed"
    COMPARISON_EFFECTIVE_CANDIDATE = "comparison_effective_candidate"
    COMPARISON_PARTIALLY_EFFECTIVE_CANDIDATE = "comparison_partially_effective_candidate"
    COMPARISON_INEFFECTIVE_CANDIDATE = "comparison_ineffective_candidate"
    COMPARISON_REGRESSIVE_CANDIDATE = "comparison_regressive_candidate"
    COMPARISON_INCONCLUSIVE = "comparison_inconclusive"
    HUMAN_REVIEW_REQUIRED = "human_review_required"
    FUTURE_SELF_PROMPTING_INPUT_READY = "future_self_prompting_input_ready"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class RepairDiagnosticSignalKind(StrEnum):
    REPAIR_EFFECTIVE_SIGNAL = "repair_effective_signal"
    REPAIR_PARTIALLY_EFFECTIVE_SIGNAL = "repair_partially_effective_signal"
    REPAIR_INEFFECTIVE_SIGNAL = "repair_ineffective_signal"
    REPAIR_REGRESSIVE_SIGNAL = "repair_regressive_signal"
    RESIDUAL_FAILURE_SIGNAL = "residual_failure_signal"
    NEW_FAILURE_SIGNAL = "new_failure_signal"
    NO_REGRESSION_SIGNAL = "no_regression_signal"
    LOW_COVERAGE_SIGNAL = "low_coverage_signal"
    INCONCLUSIVE_TEST_SIGNAL = "inconclusive_test_signal"
    DO_NOTHING_PREFERRED_SIGNAL = "do_nothing_preferred_signal"
    HUMAN_REVIEW_REQUIRED_SIGNAL = "human_review_required_signal"
    INSUFFICIENT_STATE_SIGNAL = "insufficient_state_signal"
    UNKNOWN = "unknown"


class RepairProcessStateDisposition(StrEnum):
    RECONSTRUCTED = "reconstructed"
    RECONSTRUCTED_WITH_WARNINGS = "reconstructed_with_warnings"
    INCONCLUSIVE = "inconclusive"
    EFFECTIVE_CANDIDATE_STATE = "effective_candidate_state"
    PARTIALLY_EFFECTIVE_CANDIDATE_STATE = "partially_effective_candidate_state"
    INEFFECTIVE_CANDIDATE_STATE = "ineffective_candidate_state"
    REGRESSIVE_CANDIDATE_STATE = "regressive_candidate_state"
    HUMAN_REVIEW_REQUIRED = "human_review_required"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairProcessStateConfidenceLevel(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INCONCLUSIVE = "inconclusive"
    UNKNOWN = "unknown"


UNSAFE_FLAG_NAMES = [
    "ready_for_execution",
    "ready_for_general_execution",
    "ready_for_test_execution",
    "ready_for_controlled_retest_execution",
    "ready_for_controlled_test_subprocess",
    "ready_for_arbitrary_command_execution",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_dependency_install",
    "ready_for_network_access",
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
    "ready_for_rollback_execution",
    "ready_for_ocel_event_write",
    "ready_for_ocel_file_write",
    "ready_for_ocpx_state_persistence",
    "ready_for_pig_recommendation_execution",
    "ready_for_pig_runtime_authority",
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

UNSAFE_POLICY_NAMES = [
    "allow_test_execution",
    "allow_controlled_retest_execution",
    "allow_patch_application",
    "allow_rollback_execution",
    "allow_repair_execution",
    "allow_ocel_event_write",
    "allow_ocel_file_write",
    "allow_ocpx_state_persistence",
    "allow_pig_recommendation_execution",
    "allow_pig_runtime_authority",
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
    "allow_subprocess",
    "allow_shell",
    "allow_dependency_install",
    "allow_network_access",
    "allow_dominion_runtime",
]

UNSAFE_DECISION_NAMES = [
    "ocel_event_write_allowed_now",
    "ocpx_state_persistence_allowed_now",
    "pig_recommendation_execution_allowed_now",
    "self_prompt_generation_allowed_now",
    "self_prompt_execution_allowed_now",
    "next_action_generation_allowed_now",
    "next_action_execution_allowed_now",
    "subagent_invocation_allowed_now",
    "model_provider_invocation_allowed_now",
    "external_agent_allowed_now",
    "patch_apply_allowed_now",
    "test_execution_allowed_now",
    "repair_execution_allowed_now",
    "dominion_runtime_allowed_now",
    "production_certified",
]

UNSAFE_REPORT_NAMES = [
    "persisted",
    "ocel_file_written",
    "jsonl_written",
    "ocpx_state_persisted",
    "pig_recommendation_executed",
    "self_prompt_generated",
    "self_prompt_executed",
    "next_action_generated",
    "next_action_executed",
    "subagent_invoked",
    "model_invoked",
    "external_agent_invoked",
    "patch_applied_by_v0396",
    "tests_run_by_v0396",
    "repair_executed_by_v0396",
    "dominion_runtime_invoked",
    "production_certified",
    "ready_for_execution",
]

UNSAFE_READINESS_NAMES = [
    "ocel_event_write_enabled",
    "ocel_file_write_enabled",
    "ocpx_state_persistence_enabled",
    "pig_recommendation_execution_enabled",
    "pig_runtime_authority_enabled",
    "self_prompt_generation_enabled",
    "self_prompt_execution_enabled",
    "next_action_generation_enabled",
    "next_action_execution_enabled",
    "subagent_invocation_enabled",
    "model_invocation_enabled",
    "external_agent_enabled",
    "patch_apply_enabled",
    "test_execution_enabled",
    "repair_execution_enabled",
    "dominion_runtime_enabled",
    "production_certified",
    "ready_for_execution",
]


def _with_overrides(defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged = defaults.copy()
    merged.update(overrides)
    return merged


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0396_VERSION not in version:
        raise ValueError("version must include v0.39.6")


def _validate_list(name: str, value: Any) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be a list")


def _validate_dict(name: str, value: Any) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be a dict")


def _validate_false(instance: object, names: list[str]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must remain False in v0.39.6")


def _validate_true(instance: object, names: list[str]) -> None:
    for name in names:
        if getattr(instance, name) is not True:
            raise ValueError(f"{name} must be True")


@dataclass(frozen=True)
class RepairProcessStateFlagSet:
    flag_set_id: str
    version: str
    process_state_reconstruction_layer_constructed: bool = True
    ocel_style_event_envelope_available: bool = True
    repair_object_reference_model_available: bool = True
    repair_object_relation_snapshot_available: bool = True
    repair_trace_segment_reconstruction_available: bool = True
    ocpx_style_state_projection_available: bool = True
    repair_process_state_transition_available: bool = True
    repair_mission_state_projection_available: bool = True
    pig_diagnostic_input_context_available: bool = True
    future_self_prompting_next_action_input_available: bool = True
    ready_for_v0397_self_prompting_next_action_draft: bool = True
    ready_for_pi_native_repair_process_state_reconstruction: bool = True
    ready_for_ocel_style_repair_event_envelope: bool = True
    ready_for_repair_object_reference_metadata: bool = True
    ready_for_repair_object_relation_metadata: bool = True
    ready_for_repair_trace_segment_metadata: bool = True
    ready_for_ocpx_style_repair_state_projection: bool = True
    ready_for_repair_process_state_transition_metadata: bool = True
    ready_for_repair_mission_state_projection: bool = True
    ready_for_pig_diagnostic_input_context: bool = True
    ready_for_future_self_prompting_next_action_input: bool = True
    ready_for_repair_process_state_projection: bool = True
    ready_for_execution: bool = False
    ready_for_general_execution: bool = False
    ready_for_test_execution: bool = False
    ready_for_controlled_retest_execution: bool = False
    ready_for_controlled_test_subprocess: bool = False
    ready_for_arbitrary_command_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_dependency_install: bool = False
    ready_for_network_access: bool = False
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
    ready_for_rollback_execution: bool = False
    ready_for_ocel_event_write: bool = False
    ready_for_ocel_file_write: bool = False
    ready_for_ocpx_state_persistence: bool = False
    ready_for_pig_recommendation_execution: bool = False
    ready_for_pig_runtime_authority: bool = False
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
class RepairProcessStateSourceRef:
    source_ref_id: str
    source_kind: RepairProcessStateSourceKind | str
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
class RepairProcessStatePolicy:
    policy_id: str
    version: str
    allowed_modes: list[RepairProcessStateMode | str]
    allowed_event_kinds: list[RepairProcessEventKind | str]
    allowed_object_kinds: list[RepairProcessObjectKind | str]
    allowed_relation_kinds: list[RepairProcessRelationKind | str]
    max_event_envelopes: int = 20
    max_object_refs: int = 40
    max_relations: int = 80
    max_trace_segments: int = 10
    require_outcome_comparison_report: bool = True
    require_sandbox_apply_result: bool = True
    require_post_apply_retest_result: bool = True
    require_do_nothing_comparison: bool = True
    require_human_handoff: bool = True
    allow_ocel_style_event_envelope: bool = True
    allow_object_reference_modeling: bool = True
    allow_object_relation_snapshot: bool = True
    allow_trace_segment_reconstruction: bool = True
    allow_ocpx_style_state_projection: bool = True
    allow_process_state_transition: bool = True
    allow_mission_state_projection: bool = True
    allow_pig_diagnostic_input_context: bool = True
    allow_future_self_prompting_next_action_input: bool = True
    allow_test_execution: bool = False
    allow_controlled_retest_execution: bool = False
    allow_patch_application: bool = False
    allow_rollback_execution: bool = False
    allow_repair_execution: bool = False
    allow_ocel_event_write: bool = False
    allow_ocel_file_write: bool = False
    allow_ocpx_state_persistence: bool = False
    allow_pig_recommendation_execution: bool = False
    allow_pig_runtime_authority: bool = False
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
    allow_subprocess: bool = False
    allow_shell: bool = False
    allow_dependency_install: bool = False
    allow_network_access: bool = False
    allow_dominion_runtime: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_id", self.policy_id)
        _validate_version(self.version)
        for name in ["allowed_modes", "allowed_event_kinds", "allowed_object_kinds", "allowed_relation_kinds"]:
            _validate_list(name, getattr(self, name))
        for name in ["max_event_envelopes", "max_object_refs", "max_relations", "max_trace_segments"]:
            if getattr(self, name) <= 0:
                raise ValueError(f"{name} must be > 0")
        _validate_dict("metadata", self.metadata)
        _validate_false(self, UNSAFE_POLICY_NAMES)


@dataclass(frozen=True)
class RepairProcessStateInput:
    process_state_input_id: str
    version: str
    outcome_comparison_report_id: str | None
    effectiveness_assessment_id: str | None
    regression_signal_id: str | None
    failure_delta_assessment_id: str | None
    post_apply_retest_result_id: str | None
    sandbox_apply_result_id: str | None
    approval_process_state_gate_id: str | None
    workspace_descriptor_id: str | None
    proposed_patch_envelope_id: str | None
    requested_mode: RepairProcessStateMode | str
    source_refs: list[RepairProcessStateSourceRef]
    prohibited_runtime_actions: list[str]
    task_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("process_state_input_id", self.process_state_input_id)
        _validate_version(self.version)
        _require_non_blank("task_summary", self.task_summary)
        _validate_list("source_refs", self.source_refs)
        _validate_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_dict("metadata", self.metadata)
        for action in PROHIBITED_RUNTIME_ACTIONS:
            if action not in self.prohibited_runtime_actions:
                raise ValueError(f"prohibited_runtime_actions must include {action}")


@dataclass(frozen=True)
class RepairProcessObjectRef:
    object_ref_id: str
    version: str
    object_kind: RepairProcessObjectKind | str
    source_id: str | None
    object_label: str
    object_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["object_ref_id", "version", "object_label", "object_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairProcessObjectRelation:
    relation_id: str
    version: str
    relation_kind: RepairProcessRelationKind | str
    source_object_ref_id: str
    target_object_ref_id: str
    relation_summary: str
    confidence: RepairProcessStateConfidenceLevel | str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["relation_id", "version", "source_object_ref_id", "target_object_ref_id", "relation_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairOCELStyleEventEnvelope:
    event_envelope_id: str
    version: str
    event_kind: RepairProcessEventKind | str
    event_label: str
    event_summary: str
    object_ref_ids: list[str]
    relation_ids: list[str]
    source_refs: list[RepairProcessStateSourceRef]
    sequence_index: int
    timestamp_ref: str | None
    bounded: bool
    persisted: bool = False
    written_to_ocel_file: bool = False
    written_to_jsonl: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["event_envelope_id", "version", "event_label", "event_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ["object_ref_ids", "relation_ids", "source_refs"]:
            _validate_list(name, getattr(self, name))
        if self.sequence_index < 0:
            raise ValueError("sequence_index must be >= 0")
        if self.bounded is not True:
            raise ValueError("event envelope must be bounded")
        _validate_false(self, ["persisted", "written_to_ocel_file", "written_to_jsonl"])
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairTraceSegment:
    trace_segment_id: str
    version: str
    segment_label: str
    segment_summary: str
    event_envelope_ids: list[str]
    object_ref_ids: list[str]
    relation_ids: list[str]
    start_state: RepairProcessStateKind | str
    end_state: RepairProcessStateKind | str
    complete: bool
    gaps: list[str]
    confidence: RepairProcessStateConfidenceLevel | str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["trace_segment_id", "version", "segment_label", "segment_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ["event_envelope_ids", "object_ref_ids", "relation_ids", "gaps"]:
            _validate_list(name, getattr(self, name))
        if self.gaps and self.complete:
            raise ValueError("complete must be False if gaps are non-empty")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairOCPXStateProjection:
    state_projection_id: str
    version: str
    projection_label: str
    projection_summary: str
    current_state: RepairProcessStateKind | str
    prior_state: RepairProcessStateKind | str | None
    event_envelope_ids: list[str]
    object_ref_ids: list[str]
    relation_ids: list[str]
    trace_segment_ids: list[str]
    diagnostic_signal_kinds: list[RepairDiagnosticSignalKind | str]
    human_review_required: bool
    do_nothing_still_valid: bool
    persisted: bool = False
    ocpx_state_written: bool = False
    runtime_authority_granted: bool = False
    confidence: RepairProcessStateConfidenceLevel | str = RepairProcessStateConfidenceLevel.MEDIUM
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["state_projection_id", "version", "projection_label", "projection_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ["event_envelope_ids", "object_ref_ids", "relation_ids", "trace_segment_ids", "diagnostic_signal_kinds"]:
            _validate_list(name, getattr(self, name))
        if self.human_review_required is not True:
            raise ValueError("human_review_required must be True")
        _validate_false(self, ["persisted", "ocpx_state_written", "runtime_authority_granted"])
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairProcessStateTransition:
    transition_id: str
    version: str
    prior_state: RepairProcessStateKind | str
    next_state: RepairProcessStateKind | str
    transition_summary: str
    trigger_event_ids: list[str]
    evidence_refs: list[str]
    transition_valid: bool
    human_review_required: bool
    runtime_authority_granted: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["transition_id", "version", "transition_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("trigger_event_ids", self.trigger_event_ids)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_false(self, ["runtime_authority_granted"])
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairMissionStateProjection:
    mission_state_id: str
    version: str
    mission_objective_ref: str | None
    mission_state_summary: str
    current_process_state: RepairProcessStateKind | str
    effectiveness_kind: str | None
    regression_detected: bool
    residual_failure_present: bool
    do_nothing_preferred: bool
    human_handoff_required: bool
    future_self_prompting_input_ready: bool
    next_action_generated: bool = False
    next_action_executed: bool = False
    self_prompt_generated: bool = False
    self_prompt_executed: bool = False
    subagent_invoked: bool = False
    runtime_authority_granted: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["mission_state_id", "version", "mission_state_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        if self.human_handoff_required is not True:
            raise ValueError("human_handoff_required must be True")
        _validate_false(
            self,
            [
                "next_action_generated",
                "next_action_executed",
                "self_prompt_generated",
                "self_prompt_executed",
                "subagent_invoked",
                "runtime_authority_granted",
            ],
        )
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairPIGDiagnosticInputContext:
    pig_input_context_id: str
    version: str
    state_projection_id: str
    mission_state_id: str
    diagnostic_signal_kinds: list[RepairDiagnosticSignalKind | str]
    diagnostic_context_summary: str
    recommended_attention_items: list[str]
    blocked_runtime_actions: list[str]
    human_review_required: bool
    pig_recommendation_executed: bool = False
    pig_runtime_authority_granted: bool = False
    next_action_draft_generated: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["pig_input_context_id", "version", "state_projection_id", "mission_state_id", "diagnostic_context_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ["diagnostic_signal_kinds", "recommended_attention_items", "blocked_runtime_actions"]:
            _validate_list(name, getattr(self, name))
        if self.human_review_required is not True:
            raise ValueError("human_review_required must be True")
        _validate_false(self, ["pig_recommendation_executed", "pig_runtime_authority_granted", "next_action_draft_generated"])
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairProcessStateDecision:
    process_state_decision_id: str
    version: str
    decision_kind: RepairProcessStateDecisionKind | str
    status: RepairProcessStateStatus | str
    readiness_level: RepairProcessStateReadinessLevel | str
    disposition: RepairProcessStateDisposition | str
    decision_summary: str
    rationale_summary: str
    confidence: RepairProcessStateConfidenceLevel | str
    evidence_refs: list[str]
    ready_for_future_self_prompting_next_action_input: bool
    process_state_reconstruction_allowed_now: bool
    ocel_event_write_allowed_now: bool = False
    ocpx_state_persistence_allowed_now: bool = False
    pig_recommendation_execution_allowed_now: bool = False
    self_prompt_generation_allowed_now: bool = False
    self_prompt_execution_allowed_now: bool = False
    next_action_generation_allowed_now: bool = False
    next_action_execution_allowed_now: bool = False
    subagent_invocation_allowed_now: bool = False
    model_provider_invocation_allowed_now: bool = False
    external_agent_allowed_now: bool = False
    patch_apply_allowed_now: bool = False
    test_execution_allowed_now: bool = False
    repair_execution_allowed_now: bool = False
    dominion_runtime_allowed_now: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["process_state_decision_id", "version", "decision_summary", "rationale_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_false(self, UNSAFE_DECISION_NAMES)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairProcessStateReconstructionReport:
    reconstruction_report_id: str
    version: str
    process_state_input_id: str
    object_refs: list[RepairProcessObjectRef]
    object_relations: list[RepairProcessObjectRelation]
    event_envelopes: list[RepairOCELStyleEventEnvelope]
    trace_segments: list[RepairTraceSegment]
    state_projection: RepairOCPXStateProjection
    process_state_transition: RepairProcessStateTransition
    mission_state: RepairMissionStateProjection
    pig_input_context: RepairPIGDiagnosticInputContext
    decision: RepairProcessStateDecision
    report_summary: str
    reconstruction_completed: bool
    ready_for_future_self_prompting_next_action_input: bool
    persisted: bool = False
    ocel_file_written: bool = False
    jsonl_written: bool = False
    ocpx_state_persisted: bool = False
    pig_recommendation_executed: bool = False
    self_prompt_generated: bool = False
    self_prompt_executed: bool = False
    next_action_generated: bool = False
    next_action_executed: bool = False
    subagent_invoked: bool = False
    model_invoked: bool = False
    external_agent_invoked: bool = False
    patch_applied_by_v0396: bool = False
    tests_run_by_v0396: bool = False
    repair_executed_by_v0396: bool = False
    dominion_runtime_invoked: bool = False
    production_certified: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["reconstruction_report_id", "version", "process_state_input_id", "report_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ["object_refs", "object_relations", "event_envelopes", "trace_segments", "evidence_refs"]:
            _validate_list(name, getattr(self, name))
        _validate_false(self, UNSAFE_REPORT_NAMES)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class V0396ReadinessReport:
    report_id: str
    version: str
    release_name: str
    track_name: str
    reconstruction_report: RepairProcessStateReconstructionReport | None
    decision: RepairProcessStateDecision
    flags: RepairProcessStateFlagSet
    source_refs: list[RepairProcessStateSourceRef]
    report_summary: str
    ready_for_v0397_self_prompting_next_action_draft: bool
    ready_for_pi_native_repair_process_state_reconstruction: bool
    ready_for_ocel_style_repair_event_envelope: bool
    ready_for_ocpx_style_repair_state_projection: bool
    ready_for_repair_mission_state_projection: bool
    ready_for_pig_diagnostic_input_context: bool
    ready_for_future_self_prompting_next_action_input: bool
    reconstruction_completed: bool
    ocel_event_write_enabled: bool = False
    ocel_file_write_enabled: bool = False
    ocpx_state_persistence_enabled: bool = False
    pig_recommendation_execution_enabled: bool = False
    pig_runtime_authority_enabled: bool = False
    self_prompt_generation_enabled: bool = False
    self_prompt_execution_enabled: bool = False
    next_action_generation_enabled: bool = False
    next_action_execution_enabled: bool = False
    subagent_invocation_enabled: bool = False
    model_invocation_enabled: bool = False
    external_agent_enabled: bool = False
    patch_apply_enabled: bool = False
    test_execution_enabled: bool = False
    repair_execution_enabled: bool = False
    dominion_runtime_enabled: bool = False
    production_certified: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["report_id", "version", "release_name", "track_name", "report_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("source_refs", self.source_refs)
        _validate_false(self, UNSAFE_READINESS_NAMES)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairProcessStateValidationFinding:
    finding_id: str
    finding_summary: str
    risk_kind: RepairProcessStateRiskKind | str
    blocked: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("finding_summary", self.finding_summary)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairProcessStateValidationReport:
    validation_report_id: str
    version: str
    validation_summary: str
    findings: list[RepairProcessStateValidationFinding]
    supplied_metadata_reconstruction_only_confirmed: bool
    no_ocel_file_write_confirmed: bool
    no_jsonl_write_confirmed: bool
    no_ocpx_persistence_confirmed: bool
    no_pig_execution_confirmed: bool
    no_self_prompt_generation_confirmed: bool
    no_self_prompt_execution_confirmed: bool
    no_next_action_generation_confirmed: bool
    no_next_action_execution_confirmed: bool
    no_subagent_invocation_confirmed: bool
    no_model_provider_confirmed: bool
    no_external_agent_confirmed: bool
    no_test_execution_confirmed: bool
    no_patch_application_confirmed: bool
    no_repair_execution_confirmed: bool
    no_dominion_runtime_confirmed: bool
    no_production_certification_confirmed: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version(self.version)
        _require_non_blank("validation_summary", self.validation_summary)
        _validate_list("findings", self.findings)
        _validate_true(
            self,
            [
                "supplied_metadata_reconstruction_only_confirmed",
                "no_ocel_file_write_confirmed",
                "no_jsonl_write_confirmed",
                "no_ocpx_persistence_confirmed",
                "no_pig_execution_confirmed",
                "no_self_prompt_generation_confirmed",
                "no_self_prompt_execution_confirmed",
                "no_next_action_generation_confirmed",
                "no_next_action_execution_confirmed",
                "no_subagent_invocation_confirmed",
                "no_model_provider_confirmed",
                "no_external_agent_confirmed",
                "no_test_execution_confirmed",
                "no_patch_application_confirmed",
                "no_repair_execution_confirmed",
                "no_dominion_runtime_confirmed",
                "no_production_certification_confirmed",
            ],
        )
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairProcessStateRunPreview:
    preview_id: str
    version: str
    preview_summary: str
    planned_metadata_steps: list[str]
    metadata_only: bool = True
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("preview_id", self.preview_id)
        _validate_version(self.version)
        _require_non_blank("preview_summary", self.preview_summary)
        _validate_list("planned_metadata_steps", self.planned_metadata_steps)
        if self.metadata_only is not True or self.ready_for_execution is not False:
            raise ValueError("preview must remain metadata-only and not execution-ready")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairProcessStateNoPersistenceNoExecutionGuarantee:
    guarantee_id: str
    version: str
    guarantee_summary: str
    no_ocel_file_write: bool = True
    no_jsonl_write: bool = True
    no_ocpx_persistence: bool = True
    no_trace_persistence: bool = True
    no_pig_execution: bool = True
    no_pig_runtime_authority: bool = True
    no_self_prompt_generation: bool = True
    no_self_prompt_execution: bool = True
    no_next_action_generation: bool = True
    no_next_action_execution: bool = True
    no_subagent_invocation: bool = True
    no_model_invocation: bool = True
    no_external_agent: bool = True
    no_test_execution: bool = True
    no_patch_application: bool = True
    no_rollback_execution: bool = True
    no_repair_execution: bool = True
    no_autonomous_loop: bool = True
    no_retry_loop: bool = True
    no_multi_cycle_loop: bool = True
    no_dominion_runtime: bool = True
    no_production_certification: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version(self.version)
        _require_non_blank("guarantee_summary", self.guarantee_summary)
        _validate_true(
            self,
            [
                "no_ocel_file_write",
                "no_jsonl_write",
                "no_ocpx_persistence",
                "no_trace_persistence",
                "no_pig_execution",
                "no_pig_runtime_authority",
                "no_self_prompt_generation",
                "no_self_prompt_execution",
                "no_next_action_generation",
                "no_next_action_execution",
                "no_subagent_invocation",
                "no_model_invocation",
                "no_external_agent",
                "no_test_execution",
                "no_patch_application",
                "no_rollback_execution",
                "no_repair_execution",
                "no_autonomous_loop",
                "no_retry_loop",
                "no_multi_cycle_loop",
                "no_dominion_runtime",
                "no_production_certification",
            ],
        )
        _validate_dict("metadata", self.metadata)


def build_repair_process_state_flags(**overrides: Any) -> RepairProcessStateFlagSet:
    return RepairProcessStateFlagSet(**_with_overrides({"flag_set_id": "v0396-process-state-flags", "version": V0396_VERSION}, overrides))


def build_repair_process_state_source_ref(**overrides: Any) -> RepairProcessStateSourceRef:
    defaults = {
        "source_ref_id": "v0396-source-ref",
        "source_kind": RepairProcessStateSourceKind.V0395_OUTCOME_COMPARISON_REPORT,
        "source_id": "v0395-comparison-report",
        "source_summary": "Supplied repair outcome comparison metadata for process-state reconstruction.",
        "evidence_refs": ["v0395-comparison-report"],
    }
    return RepairProcessStateSourceRef(**_with_overrides(defaults, overrides))


def default_repair_process_state_policy(**overrides: Any) -> RepairProcessStatePolicy:
    defaults = {
        "policy_id": "v0396-process-state-policy",
        "version": V0396_VERSION,
        "allowed_modes": [item for item in RepairProcessStateMode],
        "allowed_event_kinds": [item for item in RepairProcessEventKind],
        "allowed_object_kinds": [item for item in RepairProcessObjectKind],
        "allowed_relation_kinds": [item for item in RepairProcessRelationKind],
    }
    return RepairProcessStatePolicy(**_with_overrides(defaults, overrides))


def build_repair_process_state_policy(**overrides: Any) -> RepairProcessStatePolicy:
    return default_repair_process_state_policy(**overrides)


def build_repair_process_state_input(**overrides: Any) -> RepairProcessStateInput:
    defaults = {
        "process_state_input_id": "v0396-process-state-input",
        "version": V0396_VERSION,
        "outcome_comparison_report_id": "v0395-comparison-report",
        "effectiveness_assessment_id": "v0395-effectiveness",
        "regression_signal_id": "v0395-regression",
        "failure_delta_assessment_id": "v0395-failure-delta",
        "post_apply_retest_result_id": "v0394-retest-result",
        "sandbox_apply_result_id": "v0393-apply-result",
        "approval_process_state_gate_id": "v0391-approval-gate",
        "workspace_descriptor_id": "v0392-workspace-descriptor",
        "proposed_patch_envelope_id": "v0384-patch-envelope",
        "requested_mode": RepairProcessStateMode.PI_NATIVE_REPAIR_PROCESS_STATE_RECONSTRUCTION,
        "source_refs": [build_repair_process_state_source_ref()],
        "prohibited_runtime_actions": PROHIBITED_RUNTIME_ACTIONS.copy(),
        "task_summary": "Reconstruct PI-native repair process-state metadata without persistence or execution.",
    }
    return RepairProcessStateInput(**_with_overrides(defaults, overrides))


def build_repair_process_object_ref(**overrides: Any) -> RepairProcessObjectRef:
    defaults = {
        "object_ref_id": "obj-repair-mission",
        "version": V0396_VERSION,
        "object_kind": RepairProcessObjectKind.REPAIR_MISSION,
        "source_id": "repair-mission",
        "object_label": "Repair Mission",
        "object_summary": "Repair mission process object metadata.",
        "evidence_refs": ["v0396-process-state-input"],
    }
    return RepairProcessObjectRef(**_with_overrides(defaults, overrides))


def create_repair_process_object_refs(process_input: RepairProcessStateInput) -> list[RepairProcessObjectRef]:
    return [
        build_repair_process_object_ref(object_ref_id="obj-repair-mission", object_kind=RepairProcessObjectKind.REPAIR_MISSION, source_id=process_input.process_state_input_id, object_label="Repair Mission"),
        build_repair_process_object_ref(object_ref_id="obj-approval-gate", object_kind=RepairProcessObjectKind.APPROVAL_GATE, source_id=process_input.approval_process_state_gate_id, object_label="Approval Gate"),
        build_repair_process_object_ref(object_ref_id="obj-sandbox-apply", object_kind=RepairProcessObjectKind.SANDBOX_APPLY_RESULT, source_id=process_input.sandbox_apply_result_id, object_label="Sandbox Apply Result"),
        build_repair_process_object_ref(object_ref_id="obj-retest-result", object_kind=RepairProcessObjectKind.CONTROLLED_RETEST_RESULT, source_id=process_input.post_apply_retest_result_id, object_label="Controlled Retest Result"),
        build_repair_process_object_ref(object_ref_id="obj-outcome-comparison", object_kind=RepairProcessObjectKind.OUTCOME_COMPARISON, source_id=process_input.outcome_comparison_report_id, object_label="Outcome Comparison"),
        build_repair_process_object_ref(object_ref_id="obj-human-handoff", object_kind=RepairProcessObjectKind.HUMAN_HANDOFF, source_id="human-handoff-required", object_label="Human Handoff"),
    ]


def build_repair_process_object_relation(**overrides: Any) -> RepairProcessObjectRelation:
    defaults = {
        "relation_id": "rel-mission-produces-comparison",
        "version": V0396_VERSION,
        "relation_kind": RepairProcessRelationKind.PRODUCES,
        "source_object_ref_id": "obj-repair-mission",
        "target_object_ref_id": "obj-outcome-comparison",
        "relation_summary": "Repair mission produced outcome comparison metadata.",
        "confidence": RepairProcessStateConfidenceLevel.MEDIUM,
        "evidence_refs": ["v0395-comparison-report"],
    }
    return RepairProcessObjectRelation(**_with_overrides(defaults, overrides))


def create_repair_process_object_relations(object_refs: list[RepairProcessObjectRef]) -> list[RepairProcessObjectRelation]:
    ids = {obj.object_ref_id for obj in object_refs}
    relations = [
        ("rel-approval-gates-apply", RepairProcessRelationKind.GATES, "obj-approval-gate", "obj-sandbox-apply"),
        ("rel-apply-produces-retest", RepairProcessRelationKind.PRODUCES, "obj-sandbox-apply", "obj-retest-result"),
        ("rel-retest-feeds-comparison", RepairProcessRelationKind.FEEDS_FUTURE_STATE, "obj-retest-result", "obj-outcome-comparison"),
        ("rel-comparison-requires-handoff", RepairProcessRelationKind.REQUIRES_HUMAN_REVIEW, "obj-outcome-comparison", "obj-human-handoff"),
    ]
    return [
        build_repair_process_object_relation(
            relation_id=relation_id,
            relation_kind=kind,
            source_object_ref_id=source,
            target_object_ref_id=target,
            relation_summary=f"{source} {kind.value} {target}.",
        )
        for relation_id, kind, source, target in relations
        if source in ids and target in ids
    ]


def build_repair_ocel_style_event_envelope(**overrides: Any) -> RepairOCELStyleEventEnvelope:
    defaults = {
        "event_envelope_id": "evt-outcome-comparison-completed",
        "version": V0396_VERSION,
        "event_kind": RepairProcessEventKind.OUTCOME_COMPARISON_COMPLETED,
        "event_label": "Outcome Comparison Completed",
        "event_summary": "OCEL-style event envelope metadata; not persisted.",
        "object_ref_ids": ["obj-outcome-comparison"],
        "relation_ids": ["rel-comparison-requires-handoff"],
        "source_refs": [build_repair_process_state_source_ref()],
        "sequence_index": 0,
        "timestamp_ref": None,
        "bounded": True,
    }
    return RepairOCELStyleEventEnvelope(**_with_overrides(defaults, overrides))


def create_repair_ocel_style_event_envelopes(object_refs: list[RepairProcessObjectRef], relations: list[RepairProcessObjectRelation]) -> list[RepairOCELStyleEventEnvelope]:
    object_ids = [obj.object_ref_id for obj in object_refs]
    relation_ids = [rel.relation_id for rel in relations]
    event_kinds = [
        RepairProcessEventKind.APPROVAL_GATE_SATISFIED,
        RepairProcessEventKind.SANDBOX_APPLY_COMPLETED,
        RepairProcessEventKind.CONTROLLED_RETEST_COMPLETED,
        RepairProcessEventKind.OUTCOME_COMPARISON_COMPLETED,
        RepairProcessEventKind.HUMAN_HANDOFF_REQUIRED,
    ]
    return [
        build_repair_ocel_style_event_envelope(
            event_envelope_id=f"evt-{index}-{kind.value}",
            event_kind=kind,
            event_label=kind.value,
            object_ref_ids=object_ids,
            relation_ids=relation_ids,
            sequence_index=index,
        )
        for index, kind in enumerate(event_kinds)
    ]


def build_repair_trace_segment(**overrides: Any) -> RepairTraceSegment:
    defaults = {
        "trace_segment_id": "trace-v0396-repair",
        "version": V0396_VERSION,
        "segment_label": "Repair apply and comparison segment",
        "segment_summary": "Trace segment metadata reconstructed from supplied artifacts.",
        "event_envelope_ids": ["evt-outcome-comparison-completed"],
        "object_ref_ids": ["obj-repair-mission", "obj-outcome-comparison"],
        "relation_ids": ["rel-comparison-requires-handoff"],
        "start_state": RepairProcessStateKind.APPROVAL_GATE_READY,
        "end_state": RepairProcessStateKind.FUTURE_SELF_PROMPTING_INPUT_READY,
        "complete": True,
        "gaps": [],
        "confidence": RepairProcessStateConfidenceLevel.MEDIUM,
    }
    return RepairTraceSegment(**_with_overrides(defaults, overrides))


def reconstruct_repair_trace_segments(
    event_envelopes: list[RepairOCELStyleEventEnvelope],
    object_refs: list[RepairProcessObjectRef],
    relations: list[RepairProcessObjectRelation],
) -> list[RepairTraceSegment]:
    gaps = [] if event_envelopes and object_refs and relations else ["missing event/object/relation metadata"]
    return [
        build_repair_trace_segment(
            event_envelope_ids=[event.event_envelope_id for event in event_envelopes],
            object_ref_ids=[obj.object_ref_id for obj in object_refs],
            relation_ids=[rel.relation_id for rel in relations],
            complete=not gaps,
            gaps=gaps,
        )
    ]


def _state_from_metadata(metadata: dict[str, Any] | None = None) -> RepairProcessStateKind:
    data = metadata or {}
    if data.get("regressive_candidate") or data.get("regression_detected"):
        return RepairProcessStateKind.COMPARISON_REGRESSIVE_CANDIDATE
    if data.get("partially_effective_candidate"):
        return RepairProcessStateKind.COMPARISON_PARTIALLY_EFFECTIVE_CANDIDATE
    if data.get("ineffective_candidate"):
        return RepairProcessStateKind.COMPARISON_INEFFECTIVE_CANDIDATE
    if data.get("inconclusive_candidate"):
        return RepairProcessStateKind.COMPARISON_INCONCLUSIVE
    return RepairProcessStateKind.COMPARISON_EFFECTIVE_CANDIDATE


def _diagnostic_signals(metadata: dict[str, Any] | None = None) -> list[RepairDiagnosticSignalKind | str]:
    data = metadata or {}
    signals: list[RepairDiagnosticSignalKind | str] = []
    if data.get("regressive_candidate") or data.get("regression_detected"):
        signals.append(RepairDiagnosticSignalKind.REPAIR_REGRESSIVE_SIGNAL)
    elif data.get("partially_effective_candidate"):
        signals.append(RepairDiagnosticSignalKind.REPAIR_PARTIALLY_EFFECTIVE_SIGNAL)
    elif data.get("ineffective_candidate"):
        signals.append(RepairDiagnosticSignalKind.REPAIR_INEFFECTIVE_SIGNAL)
    else:
        signals.append(RepairDiagnosticSignalKind.REPAIR_EFFECTIVE_SIGNAL)
    if data.get("residual_failure_present"):
        signals.append(RepairDiagnosticSignalKind.RESIDUAL_FAILURE_SIGNAL)
    if data.get("do_nothing_preferred"):
        signals.append(RepairDiagnosticSignalKind.DO_NOTHING_PREFERRED_SIGNAL)
    signals.append(RepairDiagnosticSignalKind.HUMAN_REVIEW_REQUIRED_SIGNAL)
    return signals


def build_repair_ocpx_state_projection(**overrides: Any) -> RepairOCPXStateProjection:
    defaults = {
        "state_projection_id": "state-projection-v0396",
        "version": V0396_VERSION,
        "projection_label": "Repair process-state projection",
        "projection_summary": "OCPX-style projection metadata; not persisted.",
        "current_state": RepairProcessStateKind.COMPARISON_EFFECTIVE_CANDIDATE,
        "prior_state": RepairProcessStateKind.RETEST_COMPLETED,
        "event_envelope_ids": ["evt-outcome-comparison-completed"],
        "object_ref_ids": ["obj-repair-mission"],
        "relation_ids": ["rel-comparison-requires-handoff"],
        "trace_segment_ids": ["trace-v0396-repair"],
        "diagnostic_signal_kinds": [RepairDiagnosticSignalKind.REPAIR_EFFECTIVE_SIGNAL, RepairDiagnosticSignalKind.HUMAN_REVIEW_REQUIRED_SIGNAL],
        "human_review_required": True,
        "do_nothing_still_valid": True,
    }
    return RepairOCPXStateProjection(**_with_overrides(defaults, overrides))


def project_repair_ocpx_state(
    trace_segments: list[RepairTraceSegment],
    event_envelopes: list[RepairOCELStyleEventEnvelope],
    object_refs: list[RepairProcessObjectRef],
    relations: list[RepairProcessObjectRelation],
    *,
    metadata: dict[str, Any] | None = None,
) -> RepairOCPXStateProjection:
    return build_repair_ocpx_state_projection(
        current_state=_state_from_metadata(metadata),
        event_envelope_ids=[event.event_envelope_id for event in event_envelopes],
        object_ref_ids=[obj.object_ref_id for obj in object_refs],
        relation_ids=[rel.relation_id for rel in relations],
        trace_segment_ids=[segment.trace_segment_id for segment in trace_segments],
        diagnostic_signal_kinds=_diagnostic_signals(metadata),
        do_nothing_still_valid=True,
    )


def build_repair_process_state_transition(**overrides: Any) -> RepairProcessStateTransition:
    defaults = {
        "transition_id": "transition-v0396",
        "version": V0396_VERSION,
        "prior_state": RepairProcessStateKind.RETEST_COMPLETED,
        "next_state": RepairProcessStateKind.FUTURE_SELF_PROMPTING_INPUT_READY,
        "transition_summary": "Process-state transition metadata for v0.39.7 input.",
        "trigger_event_ids": ["evt-outcome-comparison-completed"],
        "evidence_refs": ["state-projection-v0396"],
        "transition_valid": True,
        "human_review_required": True,
    }
    return RepairProcessStateTransition(**_with_overrides(defaults, overrides))


def create_repair_process_state_transition(projection: RepairOCPXStateProjection) -> RepairProcessStateTransition:
    return build_repair_process_state_transition(
        prior_state=projection.prior_state or RepairProcessStateKind.RETEST_COMPLETED,
        next_state=RepairProcessStateKind.FUTURE_SELF_PROMPTING_INPUT_READY,
        trigger_event_ids=projection.event_envelope_ids,
    )


def build_repair_mission_state_projection(**overrides: Any) -> RepairMissionStateProjection:
    defaults = {
        "mission_state_id": "mission-state-v0396",
        "version": V0396_VERSION,
        "mission_objective_ref": "repair-mission",
        "mission_state_summary": "Repair mission state projected for human handoff and future v0.39.7 input.",
        "current_process_state": RepairProcessStateKind.FUTURE_SELF_PROMPTING_INPUT_READY,
        "effectiveness_kind": "effective_candidate",
        "regression_detected": False,
        "residual_failure_present": False,
        "do_nothing_preferred": False,
        "human_handoff_required": True,
        "future_self_prompting_input_ready": True,
    }
    return RepairMissionStateProjection(**_with_overrides(defaults, overrides))


def project_repair_mission_state(projection: RepairOCPXStateProjection, *, metadata: dict[str, Any] | None = None) -> RepairMissionStateProjection:
    data = metadata or {}
    return build_repair_mission_state_projection(
        current_process_state=projection.current_state,
        effectiveness_kind=data.get("effectiveness_kind", "effective_candidate"),
        regression_detected=bool(data.get("regression_detected", RepairDiagnosticSignalKind.REPAIR_REGRESSIVE_SIGNAL in projection.diagnostic_signal_kinds)),
        residual_failure_present=bool(data.get("residual_failure_present", False)),
        do_nothing_preferred=bool(data.get("do_nothing_preferred", False)),
    )


def build_repair_pig_diagnostic_input_context(**overrides: Any) -> RepairPIGDiagnosticInputContext:
    defaults = {
        "pig_input_context_id": "pig-input-v0396",
        "version": V0396_VERSION,
        "state_projection_id": "state-projection-v0396",
        "mission_state_id": "mission-state-v0396",
        "diagnostic_signal_kinds": [RepairDiagnosticSignalKind.REPAIR_EFFECTIVE_SIGNAL, RepairDiagnosticSignalKind.HUMAN_REVIEW_REQUIRED_SIGNAL],
        "diagnostic_context_summary": "PIG-style diagnostic input context only; no recommendation executed.",
        "recommended_attention_items": ["human-review-required", "verify-effectiveness-before-v0397"],
        "blocked_runtime_actions": PROHIBITED_RUNTIME_ACTIONS.copy(),
        "human_review_required": True,
    }
    return RepairPIGDiagnosticInputContext(**_with_overrides(defaults, overrides))


def create_pig_diagnostic_input_context(projection: RepairOCPXStateProjection, mission_state: RepairMissionStateProjection) -> RepairPIGDiagnosticInputContext:
    return build_repair_pig_diagnostic_input_context(
        state_projection_id=projection.state_projection_id,
        mission_state_id=mission_state.mission_state_id,
        diagnostic_signal_kinds=projection.diagnostic_signal_kinds,
    )


def build_repair_process_state_decision(**overrides: Any) -> RepairProcessStateDecision:
    defaults = {
        "process_state_decision_id": "decision-v0396",
        "version": V0396_VERSION,
        "decision_kind": RepairProcessStateDecisionKind.ALLOW_FUTURE_SELF_PROMPTING_NEXT_ACTION_INPUT,
        "status": RepairProcessStateStatus.READY_FOR_FUTURE_SELF_PROMPTING_NEXT_ACTION_DRAFT,
        "readiness_level": RepairProcessStateReadinessLevel.FUTURE_SELF_PROMPTING_INPUT_READY,
        "disposition": RepairProcessStateDisposition.RECONSTRUCTED,
        "decision_summary": "Process-state metadata can feed future v0.39.7 input only.",
        "rationale_summary": "Reconstruction is metadata-only and grants no persistence or runtime authority.",
        "confidence": RepairProcessStateConfidenceLevel.MEDIUM,
        "evidence_refs": ["state-projection-v0396"],
        "ready_for_future_self_prompting_next_action_input": True,
        "process_state_reconstruction_allowed_now": True,
    }
    return RepairProcessStateDecision(**_with_overrides(defaults, overrides))


def decide_repair_process_state(projection: RepairOCPXStateProjection | None = None) -> RepairProcessStateDecision:
    if projection and projection.current_state == RepairProcessStateKind.COMPARISON_REGRESSIVE_CANDIDATE:
        return build_repair_process_state_decision(
            decision_kind=RepairProcessStateDecisionKind.CHOOSE_REGRESSIVE_REPAIR_STATE,
            disposition=RepairProcessStateDisposition.REGRESSIVE_CANDIDATE_STATE,
        )
    return build_repair_process_state_decision()


def build_repair_process_state_reconstruction_report(**overrides: Any) -> RepairProcessStateReconstructionReport:
    process_input = overrides.pop("process_input", build_repair_process_state_input())
    object_refs = overrides.pop("object_refs", create_repair_process_object_refs(process_input))
    relations = overrides.pop("object_relations", create_repair_process_object_relations(object_refs))
    events = overrides.pop("event_envelopes", create_repair_ocel_style_event_envelopes(object_refs, relations))
    traces = overrides.pop("trace_segments", reconstruct_repair_trace_segments(events, object_refs, relations))
    projection = overrides.pop("state_projection", project_repair_ocpx_state(traces, events, object_refs, relations))
    transition = overrides.pop("process_state_transition", create_repair_process_state_transition(projection))
    mission = overrides.pop("mission_state", project_repair_mission_state(projection))
    pig_context = overrides.pop("pig_input_context", create_pig_diagnostic_input_context(projection, mission))
    decision = overrides.pop("decision", decide_repair_process_state(projection))
    defaults = {
        "reconstruction_report_id": "reconstruction-report-v0396",
        "version": V0396_VERSION,
        "process_state_input_id": process_input.process_state_input_id,
        "object_refs": object_refs,
        "object_relations": relations,
        "event_envelopes": events,
        "trace_segments": traces,
        "state_projection": projection,
        "process_state_transition": transition,
        "mission_state": mission,
        "pig_input_context": pig_context,
        "decision": decision,
        "report_summary": "PI-native repair process-state reconstructed as metadata only.",
        "reconstruction_completed": True,
        "ready_for_future_self_prompting_next_action_input": True,
        "evidence_refs": ["v0395-comparison-report", "v0394-retest-result", "v0393-apply-result"],
    }
    return RepairProcessStateReconstructionReport(**_with_overrides(defaults, overrides))


def create_repair_process_state_reconstruction_report(process_input: RepairProcessStateInput) -> RepairProcessStateReconstructionReport:
    return build_repair_process_state_reconstruction_report(process_input=process_input)


def build_repair_process_state_validation_finding(**overrides: Any) -> RepairProcessStateValidationFinding:
    defaults = {
        "finding_id": "v0396-validation-finding",
        "finding_summary": "No persistence or execution authority introduced.",
        "risk_kind": RepairProcessStateRiskKind.PROCESS_STATE_AUTHORITY_CONFUSION_RISK,
        "blocked": False,
    }
    return RepairProcessStateValidationFinding(**_with_overrides(defaults, overrides))


def build_repair_process_state_validation_report(**overrides: Any) -> RepairProcessStateValidationReport:
    defaults = {
        "validation_report_id": "v0396-validation-report",
        "version": V0396_VERSION,
        "validation_summary": "Validation confirms metadata reconstruction only.",
        "findings": [build_repair_process_state_validation_finding()],
        "supplied_metadata_reconstruction_only_confirmed": True,
        "no_ocel_file_write_confirmed": True,
        "no_jsonl_write_confirmed": True,
        "no_ocpx_persistence_confirmed": True,
        "no_pig_execution_confirmed": True,
        "no_self_prompt_generation_confirmed": True,
        "no_self_prompt_execution_confirmed": True,
        "no_next_action_generation_confirmed": True,
        "no_next_action_execution_confirmed": True,
        "no_subagent_invocation_confirmed": True,
        "no_model_provider_confirmed": True,
        "no_external_agent_confirmed": True,
        "no_test_execution_confirmed": True,
        "no_patch_application_confirmed": True,
        "no_repair_execution_confirmed": True,
        "no_dominion_runtime_confirmed": True,
        "no_production_certification_confirmed": True,
    }
    return RepairProcessStateValidationReport(**_with_overrides(defaults, overrides))


def build_repair_process_state_run_preview(**overrides: Any) -> RepairProcessStateRunPreview:
    defaults = {
        "preview_id": "v0396-run-preview",
        "version": V0396_VERSION,
        "preview_summary": "Preview lists process-state reconstruction metadata steps only.",
        "planned_metadata_steps": [
            "ObjectRefs",
            "ObjectRelations",
            "OCELStyleEventEnvelopes",
            "TraceSegments",
            "OCPXStateProjection",
            "MissionStateProjection",
            "PIGDiagnosticInputContext",
        ],
    }
    return RepairProcessStateRunPreview(**_with_overrides(defaults, overrides))


def build_repair_process_state_no_persistence_no_execution_guarantee(**overrides: Any) -> RepairProcessStateNoPersistenceNoExecutionGuarantee:
    defaults = {
        "guarantee_id": "v0396-no-persistence-no-execution",
        "version": V0396_VERSION,
        "guarantee_summary": "v0.39.6 does not persist traces or execute runtime actions.",
    }
    return RepairProcessStateNoPersistenceNoExecutionGuarantee(**_with_overrides(defaults, overrides))


def build_v0396_readiness_report(**overrides: Any) -> V0396ReadinessReport:
    reconstruction_report = overrides.pop("reconstruction_report", build_repair_process_state_reconstruction_report())
    defaults = {
        "report_id": "v0396-readiness-report",
        "version": V0396_VERSION,
        "release_name": V0396_RELEASE_NAME,
        "track_name": V039_TRACK_NAME,
        "reconstruction_report": reconstruction_report,
        "decision": reconstruction_report.decision,
        "flags": build_repair_process_state_flags(),
        "source_refs": [build_repair_process_state_source_ref()],
        "report_summary": "v0.39.6 reconstruction metadata is ready for v0.39.7 design-stage handoff only.",
        "ready_for_v0397_self_prompting_next_action_draft": True,
        "ready_for_pi_native_repair_process_state_reconstruction": True,
        "ready_for_ocel_style_repair_event_envelope": True,
        "ready_for_ocpx_style_repair_state_projection": True,
        "ready_for_repair_mission_state_projection": True,
        "ready_for_pig_diagnostic_input_context": True,
        "ready_for_future_self_prompting_next_action_input": True,
        "reconstruction_completed": True,
    }
    return V0396ReadinessReport(**_with_overrides(defaults, overrides))


def repair_process_state_flags_preserve_no_persistence_or_execution(flags: RepairProcessStateFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_FLAG_NAMES)


def repair_process_state_policy_blocks_persistence_and_runtime(policy: RepairProcessStatePolicy) -> bool:
    return all(getattr(policy, name) is False for name in UNSAFE_POLICY_NAMES)


def repair_ocel_event_envelope_is_not_persisted(envelope: RepairOCELStyleEventEnvelope) -> bool:
    return not envelope.persisted and not envelope.written_to_ocel_file and not envelope.written_to_jsonl


def repair_ocpx_state_projection_is_not_persisted(projection: RepairOCPXStateProjection) -> bool:
    return not projection.persisted and not projection.ocpx_state_written and not projection.runtime_authority_granted


def repair_pig_input_context_is_not_recommendation_execution(context: RepairPIGDiagnosticInputContext) -> bool:
    return not context.pig_recommendation_executed and not context.pig_runtime_authority_granted and not context.next_action_draft_generated


def repair_process_state_report_is_not_runtime_execution(report: RepairProcessStateReconstructionReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_REPORT_NAMES)


def v0396_readiness_report_is_not_execution_ready(report: V0396ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_READINESS_NAMES) and repair_process_state_flags_preserve_no_persistence_or_execution(report.flags)
