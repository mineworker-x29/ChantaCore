"""v0.39.7 self-prompting next-action draft metadata.

This module creates bounded draft metadata only. It does not submit prompts to
models, invoke providers, execute prompts or next actions, invoke subagents,
call tools, run tests, apply patches, persist traces, execute repair, run loops,
start Dominion runtime, or certify production readiness.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank


V0397_VERSION = "v0.39.7"
V0397_RELEASE_NAME = "v0.39.7 Self-Prompting Next-Action Draft & Subagent Prompt Contract"
V039_TRACK_NAME = "Human-approved Sandbox Repair Apply & Re-test Loop with PI-native Self-Prompting Mission Loop Boundary"

PROHIBITED_RUNTIME_ACTIONS = [
    "prompt_submission",
    "model_provider_invocation",
    "prompt_execution",
    "next_action_execution",
    "subagent_invocation",
    "external_agent",
    "autonomous_loop",
    "retry_loop",
    "multi_cycle_loop",
    "repair_execution",
    "test_execution",
    "patch_application",
    "pig_execution",
    "trace_persistence",
    "Dominion",
]


class RepairSelfPromptingMode(StrEnum):
    SELF_PROMPTING_NEXT_ACTION_DRAFT = "self_prompting_next_action_draft"
    PROCESS_STATE_DRIVEN_NEXT_ACTION_CANDIDATE = "process_state_driven_next_action_candidate"
    PROCESS_STATE_DRIVEN_NEXT_ACTION_DECISION = "process_state_driven_next_action_decision"
    SELF_PROMPT_DRAFT_GENERATION = "self_prompt_draft_generation"
    AGENT_TO_SUBAGENT_PROMPT_DRAFT = "agent_to_subagent_prompt_draft"
    SUBAGENT_VERIFICATION_REQUEST_DRAFT = "subagent_verification_request_draft"
    PROMPT_SAFETY_ASSESSMENT = "prompt_safety_assessment"
    HUMAN_HANDOFF_PROMPT = "human_handoff_prompt"
    FUTURE_CLI_LOOP_STATE_SURFACE_INPUT = "future_cli_loop_state_surface_input"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairSelfPromptingSourceKind(StrEnum):
    V0396_PROCESS_STATE_RECONSTRUCTION_REPORT = "v0396_process_state_reconstruction_report"
    V0396_MISSION_STATE_PROJECTION = "v0396_mission_state_projection"
    V0396_PIG_DIAGNOSTIC_INPUT_CONTEXT = "v0396_pig_diagnostic_input_context"
    V0396_OCPX_STATE_PROJECTION = "v0396_ocpx_state_projection"
    V0396_PROCESS_STATE_DECISION = "v0396_process_state_decision"
    V0395_OUTCOME_COMPARISON_REPORT = "v0395_outcome_comparison_report"
    V0395_EFFECTIVENESS_ASSESSMENT = "v0395_effectiveness_assessment"
    V0395_REGRESSION_SIGNAL = "v0395_regression_signal"
    V0395_DO_NOTHING_COMPARISON = "v0395_do_nothing_comparison"
    V0394_POST_APPLY_RETEST_RESULT = "v0394_post_apply_retest_result"
    V0393_SANDBOX_APPLY_RESULT = "v0393_sandbox_apply_result"
    V0392_WORKSPACE_ISOLATION_DECISION = "v0392_workspace_isolation_decision"
    V0391_APPROVAL_PROCESS_STATE_GATE = "v0391_approval_process_state_gate"
    MANUAL_OPERATOR_NOTE = "manual_operator_note"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class RepairSelfPromptingStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    INPUT_VALIDATED = "input_validated"
    LOOP_CONTEXT_CREATED = "loop_context_created"
    NEXT_ACTION_CANDIDATES_CREATED = "next_action_candidates_created"
    NEXT_ACTION_DECISION_CREATED = "next_action_decision_created"
    SELF_PROMPT_DRAFT_CREATED = "self_prompt_draft_created"
    AGENT_TO_SUBAGENT_PROMPT_DRAFT_CREATED = "agent_to_subagent_prompt_draft_created"
    SUBAGENT_VERIFICATION_REQUEST_DRAFT_CREATED = "subagent_verification_request_draft_created"
    PROMPT_SAFETY_ASSESSED = "prompt_safety_assessed"
    HUMAN_HANDOFF_PROMPT_CREATED = "human_handoff_prompt_created"
    DRAFT_PACKET_CREATED = "draft_packet_created"
    READY_FOR_FUTURE_CLI_LOOP_STATE_SURFACE = "ready_for_future_cli_loop_state_surface"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    REVIEW_REQUIRED = "review_required"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class RepairSelfPromptingReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    LOOP_CONTEXT_READY = "loop_context_ready"
    NEXT_ACTION_CANDIDATE_READY = "next_action_candidate_ready"
    NEXT_ACTION_DECISION_READY = "next_action_decision_ready"
    SELF_PROMPT_DRAFT_READY = "self_prompt_draft_ready"
    AGENT_TO_SUBAGENT_PROMPT_DRAFT_READY = "agent_to_subagent_prompt_draft_ready"
    SUBAGENT_VERIFICATION_REQUEST_DRAFT_READY = "subagent_verification_request_draft_ready"
    PROMPT_SAFETY_READY = "prompt_safety_ready"
    HUMAN_HANDOFF_PROMPT_READY = "human_handoff_prompt_ready"
    FUTURE_CLI_LOOP_STATE_SURFACE_INPUT_READY = "future_cli_loop_state_surface_input_ready"
    DESIGN_HANDOFF_READY_FOR_V0398 = "design_handoff_ready_for_v0398"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class RepairSelfPromptingDecisionKind(StrEnum):
    ALLOW_LOOP_CONTEXT = "allow_loop_context"
    ALLOW_NEXT_ACTION_CANDIDATE_GENERATION = "allow_next_action_candidate_generation"
    ALLOW_NEXT_ACTION_DECISION = "allow_next_action_decision"
    ALLOW_SELF_PROMPT_DRAFT = "allow_self_prompt_draft"
    ALLOW_AGENT_TO_SUBAGENT_PROMPT_DRAFT = "allow_agent_to_subagent_prompt_draft"
    ALLOW_SUBAGENT_VERIFICATION_REQUEST_DRAFT = "allow_subagent_verification_request_draft"
    ALLOW_PROMPT_SAFETY_ASSESSMENT = "allow_prompt_safety_assessment"
    ALLOW_HUMAN_HANDOFF_PROMPT = "allow_human_handoff_prompt"
    ALLOW_FUTURE_CLI_LOOP_STATE_SURFACE_INPUT = "allow_future_cli_loop_state_surface_input"
    CHOOSE_HUMAN_REVIEW_REQUIRED = "choose_human_review_required"
    CHOOSE_DO_NOTHING = "choose_do_nothing"
    CHOOSE_STOP_AFTER_DRAFT = "choose_stop_after_draft"
    CHOOSE_EFFECTIVE_REPAIR_HANDOFF = "choose_effective_repair_handoff"
    CHOOSE_REGRESSIVE_REPAIR_HANDOFF = "choose_regressive_repair_handoff"
    CHOOSE_INCONCLUSIVE_HANDOFF = "choose_inconclusive_handoff"
    DENY = "deny"
    BLOCK = "block"
    REJECT_MISSING_PROCESS_STATE = "reject_missing_process_state"
    REJECT_MISSING_PIG_CONTEXT = "reject_missing_pig_context"
    REJECT_PROMPT_EXECUTION_REQUEST = "reject_prompt_execution_request"
    REJECT_SUBAGENT_INVOCATION_REQUEST = "reject_subagent_invocation_request"
    REJECT_MODEL_PROVIDER_REQUEST = "reject_model_provider_request"
    REJECT_AUTONOMOUS_CONTINUATION_REQUEST = "reject_autonomous_continuation_request"
    REJECT_RETRY_LOOP_REQUEST = "reject_retry_loop_request"
    REJECT_MULTI_CYCLE_LOOP_REQUEST = "reject_multi_cycle_loop_request"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class RepairSelfPromptingRiskKind(StrEnum):
    MISSING_PROCESS_STATE_RISK = "missing_process_state_risk"
    MISSING_MISSION_STATE_RISK = "missing_mission_state_risk"
    MISSING_PIG_CONTEXT_RISK = "missing_pig_context_risk"
    AMBIGUOUS_NEXT_ACTION_RISK = "ambiguous_next_action_risk"
    PROMPT_OVERREACH_RISK = "prompt_overreach_risk"
    PROMPT_INJECTION_RISK = "prompt_injection_risk"
    PROMPT_POLICY_VIOLATION_RISK = "prompt_policy_violation_risk"
    SECRET_EXPOSURE_RISK = "secret_exposure_risk"
    TOOL_EXECUTION_CONFUSION_RISK = "tool_execution_confusion_risk"
    MODEL_PROVIDER_INVOCATION_CONFUSION_RISK = "model_provider_invocation_confusion_risk"
    SELF_PROMPT_EXECUTION_CONFUSION_RISK = "self_prompt_execution_confusion_risk"
    NEXT_ACTION_EXECUTION_CONFUSION_RISK = "next_action_execution_confusion_risk"
    SUBAGENT_INVOCATION_CONFUSION_RISK = "subagent_invocation_confusion_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    AUTONOMOUS_LOOP_RUNTIME_RISK = "autonomous_loop_runtime_risk"
    RETRY_LOOP_RISK = "retry_loop_risk"
    MULTI_CYCLE_LOOP_RISK = "multi_cycle_loop_risk"
    AUTOMATIC_REPAIR_RISK = "automatic_repair_risk"
    COGNITIVE_SURRENDER_RISK = "cognitive_surrender_risk"
    TOKEN_COST_LOOP_EXPLOSION_RISK = "token_cost_loop_explosion_risk"
    CORRECTNESS_OVERCLAIM_RISK = "correctness_overclaim_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    UNKNOWN = "unknown"


class RepairNextActionKind(StrEnum):
    HUMAN_REVIEW = "human_review"
    ACCEPT_SANDBOX_REPAIR_CANDIDATE = "accept_sandbox_repair_candidate"
    REJECT_SANDBOX_REPAIR_CANDIDATE = "reject_sandbox_repair_candidate"
    REQUEST_MORE_EVIDENCE = "request_more_evidence"
    REQUEST_MANUAL_REVIEW = "request_manual_review"
    REQUEST_FOLLOWUP_PATCH_PROPOSAL = "request_followup_patch_proposal"
    REQUEST_TARGETED_RETEST = "request_targeted_retest"
    REQUEST_REGRESSION_INVESTIGATION = "request_regression_investigation"
    REQUEST_DO_NOTHING = "request_do_nothing"
    REQUEST_ROLLBACK_REVIEW = "request_rollback_review"
    PREPARE_V0398_CLI_SURFACE = "prepare_v0398_cli_surface"
    STOP_AFTER_DRAFT = "stop_after_draft"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairSelfPromptDraftKind(StrEnum):
    MISSION_CONTINUATION_PROMPT_DRAFT = "mission_continuation_prompt_draft"
    HUMAN_HANDOFF_PROMPT_DRAFT = "human_handoff_prompt_draft"
    REPAIR_REVIEW_PROMPT_DRAFT = "repair_review_prompt_draft"
    RETEST_ANALYSIS_PROMPT_DRAFT = "retest_analysis_prompt_draft"
    REGRESSION_INVESTIGATION_PROMPT_DRAFT = "regression_investigation_prompt_draft"
    EVIDENCE_GAP_PROMPT_DRAFT = "evidence_gap_prompt_draft"
    DO_NOTHING_REVIEW_PROMPT_DRAFT = "do_nothing_review_prompt_draft"
    CLI_SURFACE_PROMPT_DRAFT = "cli_surface_prompt_draft"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairSubagentPromptDraftKind(StrEnum):
    VERIFIER_SUBAGENT_PROMPT_DRAFT = "verifier_subagent_prompt_draft"
    SAFETY_REVIEWER_SUBAGENT_PROMPT_DRAFT = "safety_reviewer_subagent_prompt_draft"
    REGRESSION_REVIEWER_SUBAGENT_PROMPT_DRAFT = "regression_reviewer_subagent_prompt_draft"
    EVIDENCE_REVIEWER_SUBAGENT_PROMPT_DRAFT = "evidence_reviewer_subagent_prompt_draft"
    PROCESS_STATE_REVIEWER_SUBAGENT_PROMPT_DRAFT = "process_state_reviewer_subagent_prompt_draft"
    NO_SUBAGENT_NEEDED = "no_subagent_needed"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class RepairPromptDraftDisposition(StrEnum):
    DRAFT_CREATED = "draft_created"
    DRAFT_CREATED_WITH_WARNINGS = "draft_created_with_warnings"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    REVIEW_REQUIRED = "review_required"
    HUMAN_HANDOFF_REQUIRED = "human_handoff_required"
    DO_NOTHING_PREFERRED = "do_nothing_preferred"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairPromptDraftConfidenceLevel(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INCONCLUSIVE = "inconclusive"
    UNKNOWN = "unknown"


UNSAFE_FLAG_NAMES = [
    "ready_for_execution",
    "ready_for_general_execution",
    "ready_for_model_provider_invocation",
    "ready_for_prompt_submission_to_model",
    "ready_for_self_prompt_runtime_generation",
    "ready_for_self_prompt_execution",
    "ready_for_self_prompt_auto_execution",
    "ready_for_next_action_execution",
    "ready_for_next_action_auto_execution",
    "ready_for_agent_to_subagent_prompt_runtime_generation",
    "ready_for_subagent_invocation",
    "ready_for_subagent_auto_invocation",
    "ready_for_external_agent_execution",
    "ready_for_claude_code_invocation",
    "ready_for_codex_cli_invocation",
    "ready_for_opencode_invocation",
    "ready_for_hermes_invocation",
    "ready_for_openclaw_invocation",
    "ready_for_autonomous_loop_runtime",
    "ready_for_automatic_repair",
    "ready_for_retry_loop",
    "ready_for_multi_cycle_loop",
    "ready_for_repair_execution",
    "ready_for_test_execution",
    "ready_for_controlled_retest_execution",
    "ready_for_controlled_test_subprocess",
    "ready_for_arbitrary_command_execution",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_dependency_install",
    "ready_for_network_access",
    "ready_for_tool_execution",
    "ready_for_patch_application",
    "ready_for_apply_patch",
    "ready_for_git_apply",
    "ready_for_rollback_execution",
    "ready_for_ocel_event_write",
    "ready_for_ocel_file_write",
    "ready_for_ocpx_state_persistence",
    "ready_for_pig_recommendation_execution",
    "ready_for_pig_runtime_authority",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ui_runtime",
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
    "ready_for_external_control",
    "ready_for_authority_grant",
    "production_certified",
]

UNSAFE_POLICY_NAMES = [
    "allow_prompt_submission_to_model",
    "allow_model_provider_invocation",
    "allow_self_prompt_execution",
    "allow_self_prompt_auto_execution",
    "allow_next_action_execution",
    "allow_next_action_auto_execution",
    "allow_agent_to_subagent_prompt_runtime_generation",
    "allow_subagent_invocation",
    "allow_subagent_auto_invocation",
    "allow_external_agent_execution",
    "allow_claude_code_invocation",
    "allow_codex_cli_invocation",
    "allow_autonomous_loop_runtime",
    "allow_retry_loop",
    "allow_multi_cycle_loop",
    "allow_automatic_repair",
    "allow_repair_execution",
    "allow_test_execution",
    "allow_patch_application",
    "allow_rollback_execution",
    "allow_ocel_event_write",
    "allow_ocpx_state_persistence",
    "allow_pig_recommendation_execution",
    "allow_pig_runtime_authority",
    "allow_trace_persistence",
    "allow_subprocess",
    "allow_shell",
    "allow_dependency_install",
    "allow_network_access",
    "allow_dominion_runtime",
]

UNSAFE_DECISION_NAMES = [
    "prompt_execution_allowed_now",
    "next_action_execution_allowed_now",
    "model_provider_invocation_allowed_now",
    "subagent_invocation_allowed_now",
    "external_agent_allowed_now",
    "autonomous_loop_allowed_now",
    "retry_loop_allowed_now",
    "multi_cycle_loop_allowed_now",
    "repair_execution_allowed_now",
    "test_execution_allowed_now",
    "patch_application_allowed_now",
    "trace_persistence_allowed_now",
    "dominion_runtime_allowed_now",
    "production_certified",
]

UNSAFE_PACKET_NAMES = [
    "submitted_to_model",
    "prompt_executed",
    "next_action_executed",
    "subagent_invoked",
    "external_agent_invoked",
    "model_invoked",
    "autonomous_loop_continued",
    "retry_loop_started",
    "multi_cycle_loop_started",
    "repair_executed",
    "tests_run",
    "patch_applied",
    "trace_persisted",
    "dominion_runtime_invoked",
    "production_certified",
    "ready_for_execution",
]

UNSAFE_REPORT_NAMES = [
    "prompt_submitted_to_model",
    "prompt_executed",
    "next_action_executed",
    "subagent_invoked",
    "model_invoked",
    "external_agent_invoked",
    "autonomous_loop_continued",
    "repair_executed",
    "tests_run",
    "patch_applied",
    "trace_persisted",
    "dominion_runtime_invoked",
    "production_certified",
    "ready_for_execution",
]

UNSAFE_READINESS_NAMES = [
    "prompt_submission_enabled",
    "prompt_execution_enabled",
    "next_action_execution_enabled",
    "model_invocation_enabled",
    "subagent_invocation_enabled",
    "external_agent_enabled",
    "autonomous_loop_enabled",
    "retry_loop_enabled",
    "multi_cycle_loop_enabled",
    "repair_execution_enabled",
    "test_execution_enabled",
    "patch_application_enabled",
    "trace_persistence_enabled",
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
    if V0397_VERSION not in version:
        raise ValueError("version must include v0.39.7")


def _validate_list(name: str, value: Any) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be a list")


def _validate_dict(name: str, value: Any) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be a dict")


def _validate_false(instance: object, names: list[str]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must remain False in v0.39.7")


def _validate_true(instance: object, names: list[str]) -> None:
    for name in names:
        if getattr(instance, name) is not True:
            raise ValueError(f"{name} must be True")


def _bounded(text: str, limit: int = 4000) -> str:
    if len(text) <= limit:
        return text
    suffix = "...[truncated]"
    if limit <= len(suffix):
        return text[:limit]
    return text[: limit - len(suffix)] + suffix


@dataclass(frozen=True)
class RepairSelfPromptingFlagSet:
    flag_set_id: str
    version: str
    self_prompting_layer_constructed: bool = True
    self_prompting_mission_loop_context_available: bool = True
    process_state_driven_next_action_candidate_available: bool = True
    process_state_driven_next_action_decision_available: bool = True
    self_prompt_draft_available: bool = True
    agent_to_subagent_prompt_draft_available: bool = True
    subagent_verification_request_draft_available: bool = True
    prompt_safety_assessment_available: bool = True
    human_handoff_prompt_available: bool = True
    future_cli_loop_state_surface_input_available: bool = True
    ready_for_v0398_cli_sandbox_repair_apply_retest_loop_state_surface: bool = True
    ready_for_self_prompting_next_action_draft_contract: bool = True
    ready_for_self_prompting_mission_loop_context: bool = True
    ready_for_process_state_driven_next_action_candidate: bool = True
    ready_for_process_state_driven_next_action_decision: bool = True
    ready_for_self_prompt_draft_generation: bool = True
    ready_for_agent_to_subagent_prompt_draft_generation: bool = True
    ready_for_subagent_verification_request_draft_generation: bool = True
    ready_for_prompt_safety_assessment: bool = True
    ready_for_human_handoff_prompt: bool = True
    ready_for_future_cli_loop_state_surface_input: bool = True
    ready_for_execution: bool = False
    ready_for_general_execution: bool = False
    ready_for_model_provider_invocation: bool = False
    ready_for_prompt_submission_to_model: bool = False
    ready_for_self_prompt_runtime_generation: bool = False
    ready_for_self_prompt_execution: bool = False
    ready_for_self_prompt_auto_execution: bool = False
    ready_for_next_action_execution: bool = False
    ready_for_next_action_auto_execution: bool = False
    ready_for_agent_to_subagent_prompt_runtime_generation: bool = False
    ready_for_subagent_invocation: bool = False
    ready_for_subagent_auto_invocation: bool = False
    ready_for_external_agent_execution: bool = False
    ready_for_claude_code_invocation: bool = False
    ready_for_codex_cli_invocation: bool = False
    ready_for_opencode_invocation: bool = False
    ready_for_hermes_invocation: bool = False
    ready_for_openclaw_invocation: bool = False
    ready_for_autonomous_loop_runtime: bool = False
    ready_for_automatic_repair: bool = False
    ready_for_retry_loop: bool = False
    ready_for_multi_cycle_loop: bool = False
    ready_for_repair_execution: bool = False
    ready_for_test_execution: bool = False
    ready_for_controlled_retest_execution: bool = False
    ready_for_controlled_test_subprocess: bool = False
    ready_for_arbitrary_command_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_dependency_install: bool = False
    ready_for_network_access: bool = False
    ready_for_tool_execution: bool = False
    ready_for_patch_application: bool = False
    ready_for_apply_patch: bool = False
    ready_for_git_apply: bool = False
    ready_for_rollback_execution: bool = False
    ready_for_ocel_event_write: bool = False
    ready_for_ocel_file_write: bool = False
    ready_for_ocpx_state_persistence: bool = False
    ready_for_pig_recommendation_execution: bool = False
    ready_for_pig_runtime_authority: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
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
class RepairSelfPromptingSourceRef:
    source_ref_id: str
    source_kind: RepairSelfPromptingSourceKind | str
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
class RepairSelfPromptingPolicy:
    policy_id: str
    version: str
    allowed_modes: list[RepairSelfPromptingMode | str]
    allowed_next_action_kinds: list[RepairNextActionKind | str]
    allowed_prompt_draft_kinds: list[RepairSelfPromptDraftKind | str]
    allowed_subagent_prompt_draft_kinds: list[RepairSubagentPromptDraftKind | str]
    prohibited_prompt_fragments: list[str]
    max_prompt_chars: int = 4000
    max_next_action_candidates: int = 5
    require_process_state_reconstruction_report: bool = True
    require_mission_state_projection: bool = True
    require_pig_diagnostic_input_context: bool = True
    require_human_handoff: bool = True
    require_prompt_safety_assessment: bool = True
    require_draft_only: bool = True
    allow_loop_context: bool = True
    allow_next_action_candidate_generation: bool = True
    allow_next_action_decision: bool = True
    allow_self_prompt_draft_generation: bool = True
    allow_agent_to_subagent_prompt_draft_generation: bool = True
    allow_subagent_verification_request_draft_generation: bool = True
    allow_prompt_safety_assessment: bool = True
    allow_human_handoff_prompt: bool = True
    allow_future_cli_loop_state_surface_input: bool = True
    allow_prompt_submission_to_model: bool = False
    allow_model_provider_invocation: bool = False
    allow_self_prompt_execution: bool = False
    allow_self_prompt_auto_execution: bool = False
    allow_next_action_execution: bool = False
    allow_next_action_auto_execution: bool = False
    allow_agent_to_subagent_prompt_runtime_generation: bool = False
    allow_subagent_invocation: bool = False
    allow_subagent_auto_invocation: bool = False
    allow_external_agent_execution: bool = False
    allow_claude_code_invocation: bool = False
    allow_codex_cli_invocation: bool = False
    allow_autonomous_loop_runtime: bool = False
    allow_retry_loop: bool = False
    allow_multi_cycle_loop: bool = False
    allow_automatic_repair: bool = False
    allow_repair_execution: bool = False
    allow_test_execution: bool = False
    allow_patch_application: bool = False
    allow_rollback_execution: bool = False
    allow_ocel_event_write: bool = False
    allow_ocpx_state_persistence: bool = False
    allow_pig_recommendation_execution: bool = False
    allow_pig_runtime_authority: bool = False
    allow_trace_persistence: bool = False
    allow_subprocess: bool = False
    allow_shell: bool = False
    allow_dependency_install: bool = False
    allow_network_access: bool = False
    allow_dominion_runtime: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_id", self.policy_id)
        _validate_version(self.version)
        for name in ["allowed_modes", "allowed_next_action_kinds", "allowed_prompt_draft_kinds", "allowed_subagent_prompt_draft_kinds", "prohibited_prompt_fragments"]:
            _validate_list(name, getattr(self, name))
        if self.max_prompt_chars <= 0 or self.max_next_action_candidates <= 0:
            raise ValueError("numeric limits must be > 0")
        _validate_false(self, UNSAFE_POLICY_NAMES)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairSelfPromptingInput:
    self_prompting_input_id: str
    version: str
    process_state_reconstruction_report_id: str | None
    mission_state_id: str | None
    pig_input_context_id: str | None
    state_projection_id: str | None
    outcome_comparison_report_id: str | None
    effectiveness_assessment_id: str | None
    regression_signal_id: str | None
    requested_mode: RepairSelfPromptingMode | str
    source_refs: list[RepairSelfPromptingSourceRef]
    prohibited_runtime_actions: list[str]
    task_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("self_prompting_input_id", self.self_prompting_input_id)
        _validate_version(self.version)
        _require_non_blank("task_summary", self.task_summary)
        _validate_list("source_refs", self.source_refs)
        _validate_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        for action in PROHIBITED_RUNTIME_ACTIONS:
            if action not in self.prohibited_runtime_actions:
                raise ValueError(f"prohibited_runtime_actions must include {action}")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairSelfPromptingLoopContext:
    loop_context_id: str
    version: str
    canonical_name: str
    mission_objective_ref: str | None
    process_state_reconstruction_report_id: str | None
    mission_state_id: str | None
    pig_input_context_id: str | None
    current_state_summary: str
    diagnostic_summary: str
    human_handoff_required: bool
    max_iteration_count: int
    current_iteration_index: int
    autonomous_continuation_allowed: bool
    retry_loop_allowed: bool
    multi_cycle_loop_allowed: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["loop_context_id", "version", "canonical_name", "current_state_summary", "diagnostic_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        if self.canonical_name != "Self-Prompting Mission Loop":
            raise ValueError("canonical_name must be Self-Prompting Mission Loop")
        if self.human_handoff_required is not True:
            raise ValueError("human_handoff_required must be True")
        if self.max_iteration_count != 1 or self.current_iteration_index != 0:
            raise ValueError("loop context is single-iteration draft metadata only")
        _validate_false(self, ["autonomous_continuation_allowed", "retry_loop_allowed", "multi_cycle_loop_allowed"])
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairNextActionCandidate:
    candidate_id: str
    version: str
    next_action_kind: RepairNextActionKind | str
    candidate_summary: str
    rationale_summary: str
    supporting_signal_refs: list[str]
    blocking_signal_refs: list[str]
    requires_human_review: bool
    draft_only: bool
    executable_now: bool = False
    runtime_authority_granted: bool = False
    confidence: RepairPromptDraftConfidenceLevel | str = RepairPromptDraftConfidenceLevel.MEDIUM
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["candidate_id", "version", "candidate_summary", "rationale_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("supporting_signal_refs", self.supporting_signal_refs)
        _validate_list("blocking_signal_refs", self.blocking_signal_refs)
        _validate_true(self, ["requires_human_review", "draft_only"])
        _validate_false(self, ["executable_now", "runtime_authority_granted"])
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairNextActionDecision:
    next_action_decision_id: str
    version: str
    selected_candidate_id: str | None
    decision_kind: RepairSelfPromptingDecisionKind | str
    selected_next_action_kind: RepairNextActionKind | str
    decision_summary: str
    rationale_summary: str
    confidence: RepairPromptDraftConfidenceLevel | str
    human_handoff_required: bool
    do_nothing_considered: bool
    execution_allowed: bool = False
    auto_continue_allowed: bool = False
    subagent_invocation_allowed: bool = False
    model_invocation_allowed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["next_action_decision_id", "version", "decision_summary", "rationale_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_true(self, ["human_handoff_required", "do_nothing_considered"])
        _validate_false(self, ["execution_allowed", "auto_continue_allowed", "subagent_invocation_allowed", "model_invocation_allowed"])
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairNextActionDraft:
    next_action_draft_id: str
    version: str
    next_action_kind: RepairNextActionKind | str
    next_action_title: str
    next_action_summary: str
    action_request_text: str
    bounded: bool
    redacted: bool
    draft_only: bool
    execution_allowed: bool = False
    sent_to_model: bool = False
    sent_to_tool: bool = False
    sent_to_subagent: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["next_action_draft_id", "version", "next_action_title", "next_action_summary", "action_request_text"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_true(self, ["bounded", "redacted", "draft_only"])
        _validate_false(self, ["execution_allowed", "sent_to_model", "sent_to_tool", "sent_to_subagent"])
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairSelfPromptDraft:
    self_prompt_draft_id: str
    version: str
    prompt_draft_kind: RepairSelfPromptDraftKind | str
    prompt_title: str
    prompt_text: str
    prompt_summary: str
    source_state_summary: str
    expected_output_contract: str
    safety_instructions: list[str]
    prohibited_actions: list[str]
    bounded: bool
    redacted: bool
    draft_only: bool
    submitted_to_model: bool = False
    executed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["self_prompt_draft_id", "version", "prompt_title", "prompt_text", "prompt_summary", "source_state_summary", "expected_output_contract"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("safety_instructions", self.safety_instructions)
        _validate_list("prohibited_actions", self.prohibited_actions)
        _validate_true(self, ["bounded", "redacted", "draft_only"])
        _validate_false(self, ["submitted_to_model", "executed"])
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairAgentToSubagentPromptDraft:
    subagent_prompt_draft_id: str
    version: str
    subagent_prompt_kind: RepairSubagentPromptDraftKind | str
    intended_subagent_role: str
    prompt_title: str
    prompt_text: str
    verification_focus: list[str]
    expected_output_contract: str
    safety_instructions: list[str]
    prohibited_actions: list[str]
    bounded: bool
    redacted: bool
    draft_only: bool
    subagent_invoked: bool = False
    external_agent_invoked: bool = False
    model_invoked: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["subagent_prompt_draft_id", "version", "intended_subagent_role", "prompt_title", "prompt_text", "expected_output_contract"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ["verification_focus", "safety_instructions", "prohibited_actions"]:
            _validate_list(name, getattr(self, name))
        _validate_true(self, ["bounded", "redacted", "draft_only"])
        _validate_false(self, ["subagent_invoked", "external_agent_invoked", "model_invoked"])
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairSubagentVerificationRequestDraft:
    verification_request_draft_id: str
    version: str
    request_title: str
    request_summary: str
    verifier_role: str
    verification_questions: list[str]
    acceptance_criteria: list[str]
    rejection_criteria: list[str]
    evidence_refs: list[str]
    bounded: bool
    draft_only: bool
    subagent_invocation_allowed: bool = False
    sent_to_subagent: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["verification_request_draft_id", "version", "request_title", "request_summary", "verifier_role"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ["verification_questions", "acceptance_criteria", "rejection_criteria", "evidence_refs"]:
            _validate_list(name, getattr(self, name))
        _validate_true(self, ["bounded", "draft_only"])
        _validate_false(self, ["subagent_invocation_allowed", "sent_to_subagent"])
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairPromptSafetyAssessment:
    prompt_safety_assessment_id: str
    version: str
    assessed_draft_ids: list[str]
    risk_kinds: list[RepairSelfPromptingRiskKind | str]
    safety_summary: str
    blocks_prompt_execution: bool
    blocks_model_invocation: bool
    blocks_subagent_invocation: bool
    blocks_auto_continue: bool
    requires_human_review: bool
    safe_as_draft: bool
    safe_to_execute: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("prompt_safety_assessment_id", self.prompt_safety_assessment_id)
        _validate_version(self.version)
        _require_non_blank("safety_summary", self.safety_summary)
        _validate_list("assessed_draft_ids", self.assessed_draft_ids)
        _validate_list("risk_kinds", self.risk_kinds)
        _validate_true(self, ["blocks_prompt_execution", "blocks_model_invocation", "blocks_subagent_invocation", "blocks_auto_continue", "requires_human_review"])
        _validate_false(self, ["safe_to_execute"])
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairHumanHandoffPrompt:
    human_handoff_prompt_id: str
    version: str
    handoff_title: str
    handoff_text: str
    handoff_summary: str
    recommended_human_decision_points: list[str]
    blocked_runtime_actions: list[str]
    draft_refs: list[str]
    bounded: bool
    redacted: bool
    human_action_required: bool
    auto_continue_allowed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["human_handoff_prompt_id", "version", "handoff_title", "handoff_text", "handoff_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ["recommended_human_decision_points", "blocked_runtime_actions", "draft_refs"]:
            _validate_list(name, getattr(self, name))
        _validate_true(self, ["bounded", "redacted", "human_action_required"])
        _validate_false(self, ["auto_continue_allowed"])
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairSelfPromptingDraftPacket:
    draft_packet_id: str
    version: str
    loop_context: RepairSelfPromptingLoopContext
    next_action_candidates: list[RepairNextActionCandidate]
    next_action_decision: RepairNextActionDecision
    next_action_draft: RepairNextActionDraft | None
    self_prompt_draft: RepairSelfPromptDraft | None
    subagent_prompt_draft: RepairAgentToSubagentPromptDraft | None
    verification_request_draft: RepairSubagentVerificationRequestDraft | None
    prompt_safety_assessment: RepairPromptSafetyAssessment
    human_handoff_prompt: RepairHumanHandoffPrompt
    packet_summary: str
    ready_for_future_cli_loop_state_surface_input: bool
    draft_only: bool
    submitted_to_model: bool = False
    prompt_executed: bool = False
    next_action_executed: bool = False
    subagent_invoked: bool = False
    external_agent_invoked: bool = False
    model_invoked: bool = False
    autonomous_loop_continued: bool = False
    retry_loop_started: bool = False
    multi_cycle_loop_started: bool = False
    repair_executed: bool = False
    tests_run: bool = False
    patch_applied: bool = False
    trace_persisted: bool = False
    dominion_runtime_invoked: bool = False
    production_certified: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("draft_packet_id", self.draft_packet_id)
        _validate_version(self.version)
        _require_non_blank("packet_summary", self.packet_summary)
        _validate_list("next_action_candidates", self.next_action_candidates)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_true(self, ["draft_only"])
        _validate_false(self, UNSAFE_PACKET_NAMES)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairSelfPromptingDecision:
    self_prompting_decision_id: str
    version: str
    decision_kind: RepairSelfPromptingDecisionKind | str
    status: RepairSelfPromptingStatus | str
    readiness_level: RepairSelfPromptingReadinessLevel | str
    disposition: RepairPromptDraftDisposition | str
    decision_summary: str
    rationale_summary: str
    confidence: RepairPromptDraftConfidenceLevel | str
    evidence_refs: list[str]
    ready_for_future_cli_loop_state_surface_input: bool
    draft_generation_allowed_now: bool
    prompt_execution_allowed_now: bool = False
    next_action_execution_allowed_now: bool = False
    model_provider_invocation_allowed_now: bool = False
    subagent_invocation_allowed_now: bool = False
    external_agent_allowed_now: bool = False
    autonomous_loop_allowed_now: bool = False
    retry_loop_allowed_now: bool = False
    multi_cycle_loop_allowed_now: bool = False
    repair_execution_allowed_now: bool = False
    test_execution_allowed_now: bool = False
    patch_application_allowed_now: bool = False
    trace_persistence_allowed_now: bool = False
    dominion_runtime_allowed_now: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["self_prompting_decision_id", "version", "decision_summary", "rationale_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_false(self, UNSAFE_DECISION_NAMES)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairSelfPromptingReport:
    self_prompting_report_id: str
    version: str
    self_prompting_input_id: str
    draft_packet: RepairSelfPromptingDraftPacket
    decision: RepairSelfPromptingDecision
    report_summary: str
    ready_for_future_cli_loop_state_surface_input: bool
    draft_generation_completed: bool
    prompt_submitted_to_model: bool = False
    prompt_executed: bool = False
    next_action_executed: bool = False
    subagent_invoked: bool = False
    model_invoked: bool = False
    external_agent_invoked: bool = False
    autonomous_loop_continued: bool = False
    repair_executed: bool = False
    tests_run: bool = False
    patch_applied: bool = False
    trace_persisted: bool = False
    dominion_runtime_invoked: bool = False
    production_certified: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["self_prompting_report_id", "version", "self_prompting_input_id", "report_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_false(self, UNSAFE_REPORT_NAMES)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class V0397ReadinessReport:
    report_id: str
    version: str
    release_name: str
    track_name: str
    self_prompting_report: RepairSelfPromptingReport | None
    decision: RepairSelfPromptingDecision
    flags: RepairSelfPromptingFlagSet
    source_refs: list[RepairSelfPromptingSourceRef]
    report_summary: str
    ready_for_v0398_cli_sandbox_repair_apply_retest_loop_state_surface: bool
    ready_for_self_prompting_next_action_draft_contract: bool
    ready_for_process_state_driven_next_action_candidate: bool
    ready_for_process_state_driven_next_action_decision: bool
    ready_for_self_prompt_draft_generation: bool
    ready_for_agent_to_subagent_prompt_draft_generation: bool
    ready_for_subagent_verification_request_draft_generation: bool
    ready_for_prompt_safety_assessment: bool
    ready_for_human_handoff_prompt: bool
    ready_for_future_cli_loop_state_surface_input: bool
    draft_generation_completed: bool
    prompt_submission_enabled: bool = False
    prompt_execution_enabled: bool = False
    next_action_execution_enabled: bool = False
    model_invocation_enabled: bool = False
    subagent_invocation_enabled: bool = False
    external_agent_enabled: bool = False
    autonomous_loop_enabled: bool = False
    retry_loop_enabled: bool = False
    multi_cycle_loop_enabled: bool = False
    repair_execution_enabled: bool = False
    test_execution_enabled: bool = False
    patch_application_enabled: bool = False
    trace_persistence_enabled: bool = False
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
class RepairSelfPromptingValidationFinding:
    finding_id: str
    finding_summary: str
    risk_kind: RepairSelfPromptingRiskKind | str
    blocked: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("finding_summary", self.finding_summary)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairSelfPromptingValidationReport:
    validation_report_id: str
    version: str
    validation_summary: str
    findings: list[RepairSelfPromptingValidationFinding]
    draft_only_confirmed: bool
    no_model_invocation_confirmed: bool
    no_prompt_submission_confirmed: bool
    no_prompt_execution_confirmed: bool
    no_next_action_execution_confirmed: bool
    no_subagent_invocation_confirmed: bool
    no_external_agent_confirmed: bool
    no_autonomous_loop_confirmed: bool
    no_retry_loop_confirmed: bool
    no_multi_cycle_loop_confirmed: bool
    no_repair_execution_confirmed: bool
    no_test_execution_confirmed: bool
    no_patch_application_confirmed: bool
    no_trace_persistence_confirmed: bool
    no_pig_execution_confirmed: bool
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
                "draft_only_confirmed",
                "no_model_invocation_confirmed",
                "no_prompt_submission_confirmed",
                "no_prompt_execution_confirmed",
                "no_next_action_execution_confirmed",
                "no_subagent_invocation_confirmed",
                "no_external_agent_confirmed",
                "no_autonomous_loop_confirmed",
                "no_retry_loop_confirmed",
                "no_multi_cycle_loop_confirmed",
                "no_repair_execution_confirmed",
                "no_test_execution_confirmed",
                "no_patch_application_confirmed",
                "no_trace_persistence_confirmed",
                "no_pig_execution_confirmed",
                "no_dominion_runtime_confirmed",
                "no_production_certification_confirmed",
            ],
        )
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairSelfPromptingRunPreview:
    preview_id: str
    version: str
    preview_summary: str
    planned_draft_steps: list[str]
    draft_only: bool = True
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("preview_id", self.preview_id)
        _validate_version(self.version)
        _require_non_blank("preview_summary", self.preview_summary)
        _validate_list("planned_draft_steps", self.planned_draft_steps)
        if not self.draft_only or self.ready_for_execution:
            raise ValueError("preview must remain draft-only and not execution-ready")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairSelfPromptingDraftOnlyGuarantee:
    guarantee_id: str
    version: str
    guarantee_summary: str
    no_prompt_submission_to_model: bool = True
    no_model_invocation: bool = True
    no_prompt_execution: bool = True
    no_self_prompt_auto_execution: bool = True
    no_next_action_execution: bool = True
    no_subagent_invocation: bool = True
    no_external_agent: bool = True
    no_tool_execution: bool = True
    no_autonomous_loop: bool = True
    no_retry_loop: bool = True
    no_multi_cycle_loop: bool = True
    no_repair_execution: bool = True
    no_test_execution: bool = True
    no_patch_application: bool = True
    no_trace_persistence: bool = True
    no_pig_execution: bool = True
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
                "no_prompt_submission_to_model",
                "no_model_invocation",
                "no_prompt_execution",
                "no_self_prompt_auto_execution",
                "no_next_action_execution",
                "no_subagent_invocation",
                "no_external_agent",
                "no_tool_execution",
                "no_autonomous_loop",
                "no_retry_loop",
                "no_multi_cycle_loop",
                "no_repair_execution",
                "no_test_execution",
                "no_patch_application",
                "no_trace_persistence",
                "no_pig_execution",
                "no_dominion_runtime",
                "no_production_certification",
            ],
        )
        _validate_dict("metadata", self.metadata)


def build_repair_self_prompting_flags(**overrides: Any) -> RepairSelfPromptingFlagSet:
    return RepairSelfPromptingFlagSet(**_with_overrides({"flag_set_id": "v0397-self-prompting-flags", "version": V0397_VERSION}, overrides))


def build_repair_self_prompting_source_ref(**overrides: Any) -> RepairSelfPromptingSourceRef:
    defaults = {
        "source_ref_id": "v0397-source-ref",
        "source_kind": RepairSelfPromptingSourceKind.V0396_PROCESS_STATE_RECONSTRUCTION_REPORT,
        "source_id": "v0396-reconstruction-report",
        "source_summary": "Supplied process-state reconstruction metadata for draft generation.",
        "evidence_refs": ["v0396-reconstruction-report"],
    }
    return RepairSelfPromptingSourceRef(**_with_overrides(defaults, overrides))


def default_repair_self_prompting_policy(**overrides: Any) -> RepairSelfPromptingPolicy:
    defaults = {
        "policy_id": "v0397-self-prompting-policy",
        "version": V0397_VERSION,
        "allowed_modes": [item for item in RepairSelfPromptingMode],
        "allowed_next_action_kinds": [item for item in RepairNextActionKind],
        "allowed_prompt_draft_kinds": [item for item in RepairSelfPromptDraftKind],
        "allowed_subagent_prompt_draft_kinds": [item for item in RepairSubagentPromptDraftKind],
        "prohibited_prompt_fragments": ["execute-now", "call-model", "invoke-subagent", "auto-continue"],
    }
    return RepairSelfPromptingPolicy(**_with_overrides(defaults, overrides))


def build_repair_self_prompting_policy(**overrides: Any) -> RepairSelfPromptingPolicy:
    return default_repair_self_prompting_policy(**overrides)


def build_repair_self_prompting_input(**overrides: Any) -> RepairSelfPromptingInput:
    defaults = {
        "self_prompting_input_id": "v0397-self-prompting-input",
        "version": V0397_VERSION,
        "process_state_reconstruction_report_id": "v0396-reconstruction-report",
        "mission_state_id": "v0396-mission-state",
        "pig_input_context_id": "v0396-pig-input",
        "state_projection_id": "v0396-state-projection",
        "outcome_comparison_report_id": "v0395-comparison-report",
        "effectiveness_assessment_id": "v0395-effectiveness",
        "regression_signal_id": "v0395-regression",
        "requested_mode": RepairSelfPromptingMode.SELF_PROMPTING_NEXT_ACTION_DRAFT,
        "source_refs": [build_repair_self_prompting_source_ref()],
        "prohibited_runtime_actions": PROHIBITED_RUNTIME_ACTIONS.copy(),
        "task_summary": "Create bounded draft-only next-action and prompt metadata.",
    }
    return RepairSelfPromptingInput(**_with_overrides(defaults, overrides))


def build_repair_self_prompting_loop_context(**overrides: Any) -> RepairSelfPromptingLoopContext:
    defaults = {
        "loop_context_id": "v0397-loop-context",
        "version": V0397_VERSION,
        "canonical_name": "Self-Prompting Mission Loop",
        "mission_objective_ref": "repair-mission",
        "process_state_reconstruction_report_id": "v0396-reconstruction-report",
        "mission_state_id": "v0396-mission-state",
        "pig_input_context_id": "v0396-pig-input",
        "current_state_summary": "Process state reconstructed and human handoff remains required.",
        "diagnostic_summary": "Draft-only next action context prepared for review.",
        "human_handoff_required": True,
        "max_iteration_count": 1,
        "current_iteration_index": 0,
        "autonomous_continuation_allowed": False,
        "retry_loop_allowed": False,
        "multi_cycle_loop_allowed": False,
    }
    return RepairSelfPromptingLoopContext(**_with_overrides(defaults, overrides))


def create_repair_self_prompting_loop_context(self_prompting_input: RepairSelfPromptingInput) -> RepairSelfPromptingLoopContext:
    return build_repair_self_prompting_loop_context(
        process_state_reconstruction_report_id=self_prompting_input.process_state_reconstruction_report_id,
        mission_state_id=self_prompting_input.mission_state_id,
        pig_input_context_id=self_prompting_input.pig_input_context_id,
    )


def build_repair_next_action_candidate(**overrides: Any) -> RepairNextActionCandidate:
    defaults = {
        "candidate_id": "candidate-human-review",
        "version": V0397_VERSION,
        "next_action_kind": RepairNextActionKind.HUMAN_REVIEW,
        "candidate_summary": "Human review remains the required next action.",
        "rationale_summary": "v0.39.7 creates drafts only and grants no execution authority.",
        "supporting_signal_refs": ["human_handoff_required"],
        "blocking_signal_refs": ["no_autonomous_continuation"],
        "requires_human_review": True,
        "draft_only": True,
        "confidence": RepairPromptDraftConfidenceLevel.MEDIUM,
    }
    return RepairNextActionCandidate(**_with_overrides(defaults, overrides))


def create_repair_next_action_candidates(loop_context: RepairSelfPromptingLoopContext) -> list[RepairNextActionCandidate]:
    return [
        build_repair_next_action_candidate(),
        build_repair_next_action_candidate(
            candidate_id="candidate-v0398-cli-surface",
            next_action_kind=RepairNextActionKind.PREPARE_V0398_CLI_SURFACE,
            candidate_summary="Prepare future CLI loop-state surface input as draft metadata.",
            supporting_signal_refs=[loop_context.loop_context_id],
        ),
        build_repair_next_action_candidate(
            candidate_id="candidate-stop-after-draft",
            next_action_kind=RepairNextActionKind.STOP_AFTER_DRAFT,
            candidate_summary="Stop after draft packet and wait for human handoff.",
        ),
    ]


def build_repair_next_action_decision(**overrides: Any) -> RepairNextActionDecision:
    defaults = {
        "next_action_decision_id": "v0397-next-action-decision",
        "version": V0397_VERSION,
        "selected_candidate_id": "candidate-human-review",
        "decision_kind": RepairSelfPromptingDecisionKind.CHOOSE_HUMAN_REVIEW_REQUIRED,
        "selected_next_action_kind": RepairNextActionKind.HUMAN_REVIEW,
        "decision_summary": "Select human review as draft next action.",
        "rationale_summary": "Human handoff is mandatory; no next action executes.",
        "confidence": RepairPromptDraftConfidenceLevel.MEDIUM,
        "human_handoff_required": True,
        "do_nothing_considered": True,
    }
    return RepairNextActionDecision(**_with_overrides(defaults, overrides))


def decide_repair_next_action(candidates: list[RepairNextActionCandidate]) -> RepairNextActionDecision:
    selected = candidates[0] if candidates else None
    return build_repair_next_action_decision(
        selected_candidate_id=selected.candidate_id if selected else None,
        selected_next_action_kind=selected.next_action_kind if selected else RepairNextActionKind.NO_OP,
    )


def build_repair_next_action_draft(**overrides: Any) -> RepairNextActionDraft:
    defaults = {
        "next_action_draft_id": "v0397-next-action-draft",
        "version": V0397_VERSION,
        "next_action_kind": RepairNextActionKind.HUMAN_REVIEW,
        "next_action_title": "Human review required",
        "next_action_summary": "Draft next action for human handoff only.",
        "action_request_text": "Review the sandbox repair evidence and decide whether to continue to v0.39.8. Do not execute this draft automatically.",
        "bounded": True,
        "redacted": True,
        "draft_only": True,
    }
    return RepairNextActionDraft(**_with_overrides(defaults, overrides))


def draft_repair_next_action(decision: RepairNextActionDecision, *, max_chars: int = 4000) -> RepairNextActionDraft:
    return build_repair_next_action_draft(
        next_action_kind=decision.selected_next_action_kind,
        action_request_text=_bounded(f"{decision.decision_summary} {decision.rationale_summary}", max_chars),
    )


def build_repair_self_prompt_draft(**overrides: Any) -> RepairSelfPromptDraft:
    defaults = {
        "self_prompt_draft_id": "v0397-self-prompt-draft",
        "version": V0397_VERSION,
        "prompt_draft_kind": RepairSelfPromptDraftKind.MISSION_CONTINUATION_PROMPT_DRAFT,
        "prompt_title": "Draft mission continuation prompt",
        "prompt_text": "Draft only: summarize process state, preserve human handoff, and do not execute tools, prompts, subagents, tests, patches, or repair.",
        "prompt_summary": "Bounded self-prompt draft metadata only.",
        "source_state_summary": "v0.39.6 process-state reconstruction indicates future CLI input readiness.",
        "expected_output_contract": "Return a human-reviewable draft; do not execute it.",
        "safety_instructions": ["Do not submit to a model.", "Do not execute next actions.", "Do not invoke subagents."],
        "prohibited_actions": PROHIBITED_RUNTIME_ACTIONS.copy(),
        "bounded": True,
        "redacted": True,
        "draft_only": True,
    }
    return RepairSelfPromptDraft(**_with_overrides(defaults, overrides))


def draft_repair_self_prompt(loop_context: RepairSelfPromptingLoopContext, *, max_chars: int = 4000) -> RepairSelfPromptDraft:
    text = _bounded(
        f"Draft only for {loop_context.canonical_name}: {loop_context.current_state_summary} {loop_context.diagnostic_summary}",
        max_chars,
    )
    return build_repair_self_prompt_draft(prompt_text=text, source_state_summary=loop_context.current_state_summary)


def build_repair_agent_to_subagent_prompt_draft(**overrides: Any) -> RepairAgentToSubagentPromptDraft:
    defaults = {
        "subagent_prompt_draft_id": "v0397-subagent-prompt-draft",
        "version": V0397_VERSION,
        "subagent_prompt_kind": RepairSubagentPromptDraftKind.VERIFIER_SUBAGENT_PROMPT_DRAFT,
        "intended_subagent_role": "verifier",
        "prompt_title": "Verifier subagent prompt draft",
        "prompt_text": "Draft only: verify the repair evidence if a human later authorizes a subagent. Do not invoke a subagent from this draft.",
        "verification_focus": ["process-state consistency", "no runtime authority", "human handoff"],
        "expected_output_contract": "Return verification notes only if explicitly invoked by a future approved stage.",
        "safety_instructions": ["Do not invoke subagents.", "Do not call models.", "Do not execute tools."],
        "prohibited_actions": PROHIBITED_RUNTIME_ACTIONS.copy(),
        "bounded": True,
        "redacted": True,
        "draft_only": True,
    }
    return RepairAgentToSubagentPromptDraft(**_with_overrides(defaults, overrides))


def draft_repair_agent_to_subagent_prompt(loop_context: RepairSelfPromptingLoopContext, *, max_chars: int = 4000) -> RepairAgentToSubagentPromptDraft:
    return build_repair_agent_to_subagent_prompt_draft(
        prompt_text=_bounded(f"Draft-only verifier prompt for {loop_context.loop_context_id}; human authorization required before use.", max_chars)
    )


def build_repair_subagent_verification_request_draft(**overrides: Any) -> RepairSubagentVerificationRequestDraft:
    defaults = {
        "verification_request_draft_id": "v0397-verification-request-draft",
        "version": V0397_VERSION,
        "request_title": "Subagent verification request draft",
        "request_summary": "Draft verification request, not sent to a subagent.",
        "verifier_role": "repair-process verifier",
        "verification_questions": ["Does the draft preserve human handoff?", "Are all execution surfaces blocked?"],
        "acceptance_criteria": ["Draft-only metadata", "No model or subagent invocation"],
        "rejection_criteria": ["Any request to execute prompts or invoke agents"],
        "evidence_refs": ["v0397-draft-packet"],
        "bounded": True,
        "draft_only": True,
    }
    return RepairSubagentVerificationRequestDraft(**_with_overrides(defaults, overrides))


def draft_repair_subagent_verification_request(subagent_prompt: RepairAgentToSubagentPromptDraft) -> RepairSubagentVerificationRequestDraft:
    return build_repair_subagent_verification_request_draft(evidence_refs=[subagent_prompt.subagent_prompt_draft_id])


def build_repair_prompt_safety_assessment(**overrides: Any) -> RepairPromptSafetyAssessment:
    defaults = {
        "prompt_safety_assessment_id": "v0397-prompt-safety",
        "version": V0397_VERSION,
        "assessed_draft_ids": ["v0397-self-prompt-draft", "v0397-subagent-prompt-draft"],
        "risk_kinds": [RepairSelfPromptingRiskKind.SELF_PROMPT_EXECUTION_CONFUSION_RISK],
        "safety_summary": "Drafts are safe as drafts only; execution and invocation remain blocked.",
        "blocks_prompt_execution": True,
        "blocks_model_invocation": True,
        "blocks_subagent_invocation": True,
        "blocks_auto_continue": True,
        "requires_human_review": True,
        "safe_as_draft": True,
    }
    return RepairPromptSafetyAssessment(**_with_overrides(defaults, overrides))


def assess_repair_prompt_safety(draft_ids: list[str]) -> RepairPromptSafetyAssessment:
    return build_repair_prompt_safety_assessment(assessed_draft_ids=draft_ids)


def build_repair_human_handoff_prompt(**overrides: Any) -> RepairHumanHandoffPrompt:
    defaults = {
        "human_handoff_prompt_id": "v0397-human-handoff",
        "version": V0397_VERSION,
        "handoff_title": "Human handoff required",
        "handoff_text": "Review the draft packet. No prompt, next action, model, subagent, tool, repair, test, or patch action has been executed.",
        "handoff_summary": "Human handoff prompt metadata.",
        "recommended_human_decision_points": ["Approve future CLI surface preparation?", "Request more evidence?", "Stop after draft?"],
        "blocked_runtime_actions": PROHIBITED_RUNTIME_ACTIONS.copy(),
        "draft_refs": ["v0397-self-prompt-draft", "v0397-next-action-draft"],
        "bounded": True,
        "redacted": True,
        "human_action_required": True,
    }
    return RepairHumanHandoffPrompt(**_with_overrides(defaults, overrides))


def create_repair_human_handoff_prompt(packet_refs: list[str]) -> RepairHumanHandoffPrompt:
    return build_repair_human_handoff_prompt(draft_refs=packet_refs)


def build_repair_self_prompting_draft_packet(**overrides: Any) -> RepairSelfPromptingDraftPacket:
    loop_context = overrides.pop("loop_context", build_repair_self_prompting_loop_context())
    candidates = overrides.pop("next_action_candidates", create_repair_next_action_candidates(loop_context))
    decision = overrides.pop("next_action_decision", decide_repair_next_action(candidates))
    next_action_draft = overrides.pop("next_action_draft", draft_repair_next_action(decision))
    self_prompt = overrides.pop("self_prompt_draft", draft_repair_self_prompt(loop_context))
    subagent_prompt = overrides.pop("subagent_prompt_draft", draft_repair_agent_to_subagent_prompt(loop_context))
    verification = overrides.pop("verification_request_draft", draft_repair_subagent_verification_request(subagent_prompt))
    safety = overrides.pop("prompt_safety_assessment", assess_repair_prompt_safety([self_prompt.self_prompt_draft_id, subagent_prompt.subagent_prompt_draft_id]))
    handoff = overrides.pop("human_handoff_prompt", create_repair_human_handoff_prompt([next_action_draft.next_action_draft_id, self_prompt.self_prompt_draft_id]))
    defaults = {
        "draft_packet_id": "v0397-draft-packet",
        "version": V0397_VERSION,
        "loop_context": loop_context,
        "next_action_candidates": candidates,
        "next_action_decision": decision,
        "next_action_draft": next_action_draft,
        "self_prompt_draft": self_prompt,
        "subagent_prompt_draft": subagent_prompt,
        "verification_request_draft": verification,
        "prompt_safety_assessment": safety,
        "human_handoff_prompt": handoff,
        "packet_summary": "Draft-only self-prompting packet created for human handoff.",
        "ready_for_future_cli_loop_state_surface_input": True,
        "draft_only": True,
        "evidence_refs": ["v0396-reconstruction-report"],
    }
    return RepairSelfPromptingDraftPacket(**_with_overrides(defaults, overrides))


def create_repair_self_prompting_draft_packet(self_prompting_input: RepairSelfPromptingInput) -> RepairSelfPromptingDraftPacket:
    loop_context = create_repair_self_prompting_loop_context(self_prompting_input)
    return build_repair_self_prompting_draft_packet(loop_context=loop_context)


def build_repair_self_prompting_decision(**overrides: Any) -> RepairSelfPromptingDecision:
    defaults = {
        "self_prompting_decision_id": "v0397-self-prompting-decision",
        "version": V0397_VERSION,
        "decision_kind": RepairSelfPromptingDecisionKind.ALLOW_FUTURE_CLI_LOOP_STATE_SURFACE_INPUT,
        "status": RepairSelfPromptingStatus.READY_FOR_FUTURE_CLI_LOOP_STATE_SURFACE,
        "readiness_level": RepairSelfPromptingReadinessLevel.FUTURE_CLI_LOOP_STATE_SURFACE_INPUT_READY,
        "disposition": RepairPromptDraftDisposition.HUMAN_HANDOFF_REQUIRED,
        "decision_summary": "Draft packet may feed future v0.39.8 CLI loop-state surface input.",
        "rationale_summary": "Draft generation is complete; no prompt or action execution is allowed.",
        "confidence": RepairPromptDraftConfidenceLevel.MEDIUM,
        "evidence_refs": ["v0397-draft-packet"],
        "ready_for_future_cli_loop_state_surface_input": True,
        "draft_generation_allowed_now": True,
    }
    return RepairSelfPromptingDecision(**_with_overrides(defaults, overrides))


def decide_repair_self_prompting(packet: RepairSelfPromptingDraftPacket) -> RepairSelfPromptingDecision:
    return build_repair_self_prompting_decision(ready_for_future_cli_loop_state_surface_input=packet.ready_for_future_cli_loop_state_surface_input)


def build_repair_self_prompting_report(**overrides: Any) -> RepairSelfPromptingReport:
    self_prompting_input = overrides.pop("self_prompting_input", build_repair_self_prompting_input())
    packet = overrides.pop("draft_packet", create_repair_self_prompting_draft_packet(self_prompting_input))
    decision = overrides.pop("decision", decide_repair_self_prompting(packet))
    defaults = {
        "self_prompting_report_id": "v0397-self-prompting-report",
        "version": V0397_VERSION,
        "self_prompting_input_id": self_prompting_input.self_prompting_input_id,
        "draft_packet": packet,
        "decision": decision,
        "report_summary": "v0.39.7 draft packet created without model, prompt, action, or agent execution.",
        "ready_for_future_cli_loop_state_surface_input": True,
        "draft_generation_completed": True,
        "evidence_refs": ["v0397-draft-packet"],
    }
    return RepairSelfPromptingReport(**_with_overrides(defaults, overrides))


def create_repair_self_prompting_report(self_prompting_input: RepairSelfPromptingInput) -> RepairSelfPromptingReport:
    return build_repair_self_prompting_report(self_prompting_input=self_prompting_input)


def build_repair_self_prompting_validation_finding(**overrides: Any) -> RepairSelfPromptingValidationFinding:
    defaults = {
        "finding_id": "v0397-validation-finding",
        "finding_summary": "Draft-only contract preserves no execution.",
        "risk_kind": RepairSelfPromptingRiskKind.SELF_PROMPT_EXECUTION_CONFUSION_RISK,
        "blocked": False,
    }
    return RepairSelfPromptingValidationFinding(**_with_overrides(defaults, overrides))


def build_repair_self_prompting_validation_report(**overrides: Any) -> RepairSelfPromptingValidationReport:
    defaults = {
        "validation_report_id": "v0397-validation-report",
        "version": V0397_VERSION,
        "validation_summary": "Validation confirms draft-only behavior and no runtime invocation.",
        "findings": [build_repair_self_prompting_validation_finding()],
        "draft_only_confirmed": True,
        "no_model_invocation_confirmed": True,
        "no_prompt_submission_confirmed": True,
        "no_prompt_execution_confirmed": True,
        "no_next_action_execution_confirmed": True,
        "no_subagent_invocation_confirmed": True,
        "no_external_agent_confirmed": True,
        "no_autonomous_loop_confirmed": True,
        "no_retry_loop_confirmed": True,
        "no_multi_cycle_loop_confirmed": True,
        "no_repair_execution_confirmed": True,
        "no_test_execution_confirmed": True,
        "no_patch_application_confirmed": True,
        "no_trace_persistence_confirmed": True,
        "no_pig_execution_confirmed": True,
        "no_dominion_runtime_confirmed": True,
        "no_production_certification_confirmed": True,
    }
    return RepairSelfPromptingValidationReport(**_with_overrides(defaults, overrides))


def build_repair_self_prompting_run_preview(**overrides: Any) -> RepairSelfPromptingRunPreview:
    defaults = {
        "preview_id": "v0397-run-preview",
        "version": V0397_VERSION,
        "preview_summary": "Preview lists draft metadata steps only.",
        "planned_draft_steps": ["LoopContext", "NextActionCandidates", "SelfPromptDraft", "SubagentPromptDraft", "HumanHandoffPrompt"],
    }
    return RepairSelfPromptingRunPreview(**_with_overrides(defaults, overrides))


def build_repair_self_prompting_draft_only_guarantee(**overrides: Any) -> RepairSelfPromptingDraftOnlyGuarantee:
    defaults = {
        "guarantee_id": "v0397-draft-only-guarantee",
        "version": V0397_VERSION,
        "guarantee_summary": "v0.39.7 creates draft metadata only and blocks execution.",
    }
    return RepairSelfPromptingDraftOnlyGuarantee(**_with_overrides(defaults, overrides))


def build_v0397_readiness_report(**overrides: Any) -> V0397ReadinessReport:
    report = overrides.pop("self_prompting_report", build_repair_self_prompting_report())
    defaults = {
        "report_id": "v0397-readiness-report",
        "version": V0397_VERSION,
        "release_name": V0397_RELEASE_NAME,
        "track_name": V039_TRACK_NAME,
        "self_prompting_report": report,
        "decision": report.decision,
        "flags": build_repair_self_prompting_flags(),
        "source_refs": [build_repair_self_prompting_source_ref()],
        "report_summary": "v0.39.7 draft metadata is ready for v0.39.8 design-stage handoff only.",
        "ready_for_v0398_cli_sandbox_repair_apply_retest_loop_state_surface": True,
        "ready_for_self_prompting_next_action_draft_contract": True,
        "ready_for_process_state_driven_next_action_candidate": True,
        "ready_for_process_state_driven_next_action_decision": True,
        "ready_for_self_prompt_draft_generation": True,
        "ready_for_agent_to_subagent_prompt_draft_generation": True,
        "ready_for_subagent_verification_request_draft_generation": True,
        "ready_for_prompt_safety_assessment": True,
        "ready_for_human_handoff_prompt": True,
        "ready_for_future_cli_loop_state_surface_input": True,
        "draft_generation_completed": True,
    }
    return V0397ReadinessReport(**_with_overrides(defaults, overrides))


def repair_self_prompting_flags_preserve_no_execution(flags: RepairSelfPromptingFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_FLAG_NAMES)


def repair_self_prompting_policy_blocks_execution(policy: RepairSelfPromptingPolicy) -> bool:
    return all(getattr(policy, name) is False for name in UNSAFE_POLICY_NAMES)


def repair_self_prompt_draft_is_not_execution(draft: RepairSelfPromptDraft) -> bool:
    return draft.submitted_to_model is False and draft.executed is False and draft.draft_only is True


def repair_subagent_prompt_draft_is_not_invocation(draft: RepairAgentToSubagentPromptDraft) -> bool:
    return draft.subagent_invoked is False and draft.external_agent_invoked is False and draft.model_invoked is False and draft.draft_only is True


def repair_self_prompting_packet_is_draft_only(packet: RepairSelfPromptingDraftPacket) -> bool:
    return packet.draft_only is True and all(getattr(packet, name) is False for name in UNSAFE_PACKET_NAMES)


def v0397_readiness_report_is_not_execution_ready(report: V0397ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_READINESS_NAMES) and repair_self_prompting_flags_preserve_no_execution(report.flags)
