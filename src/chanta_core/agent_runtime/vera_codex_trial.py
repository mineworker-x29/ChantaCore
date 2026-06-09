from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list
from .sandbox_repair_suggestion import (
    SandboxRepairConfidenceLevel,
    SandboxRepairSuggestionEnvelope,
    SandboxRepairSuggestionKind,
    SandboxRepairSuggestionReport,
)
from .sandbox_test_feedback import SandboxTestFeedbackReport
from .sandbox_test_result import SandboxTestOutcomeKind, SandboxTestResultEnvelope


V0376_VERSION = "v0.37.6"
V0376_RELEASE_NAME = "v0.37.6 Vera-Codex One-shot Agent Operation Trial"


UNSAFE_VERA_CODEX_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_model_provider_invocation",
    "ready_for_tool_execution",
    "ready_for_test_execution",
    "ready_for_controlled_test_subprocess",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_dependency_install",
    "ready_for_network_access",
    "ready_for_live_workspace_write",
    "ready_for_patch_application",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_apply_patch",
    "ready_for_git_apply",
    "ready_for_repair_patch_proposal",
    "ready_for_repair_diff_generation",
    "ready_for_code_hunk_generation",
    "ready_for_automatic_repair",
    "ready_for_repair_execution",
    "ready_for_repair_loop",
    "ready_for_retry_loop",
    "ready_for_multi_cycle_agentic_loop",
    "ready_for_cold_agent_performance_evaluation",
    "ready_for_external_agent_execution",
    "ready_for_claude_code_invocation",
    "ready_for_codex_cli_invocation",
    "ready_for_dominion_runtime",
    "ready_for_infinite_agent_loop",
    "ready_for_provider_invocation",
    "ready_for_direct_network_access",
    "ready_for_credential_access",
    "ready_for_secret_read",
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
)

UNSAFE_VERA_CODEX_POLICY_ALLOW_NAMES = (
    "allow_model_provider_invocation",
    "allow_tool_execution",
    "allow_test_execution",
    "allow_subprocess",
    "allow_shell",
    "allow_dependency_install",
    "allow_network_access",
    "allow_repair_patch_proposal",
    "allow_repair_execution",
    "allow_automatic_repair",
    "allow_retry_loop",
    "allow_multi_cycle_loop",
    "allow_external_agent_execution",
    "allow_dominion_runtime",
)

PROHIBITED_TRIAL_ACTIONS = (
    "model invocation",
    "tool execution",
    "test execution",
    "subprocess",
    "shell",
    "install",
    "network",
    "repair",
    "external agent",
    "Dominion",
    "retry loop",
    "multi-cycle loop",
)


def _validate_list(name: str, value: Any) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{name} must be a list")


def _validate_dict(name: str, value: Any) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a dict")


def _validate_metadata(value: dict[str, Any]) -> None:
    _validate_dict("metadata", value)


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0376_VERSION not in version:
        raise ValueError("version must include v0.37.6")


def _validate_false(name: str, value: bool) -> None:
    if value is not False:
        raise ValueError(f"{name} must remain False in v0.37.6")


def _validate_true(name: str, value: bool) -> None:
    if value is not True:
        raise ValueError(f"{name} must be True")


def _validate_non_negative(name: str, value: int) -> None:
    if value < 0:
        raise ValueError(f"{name} must be >= 0")


def _validate_exactly_one(name: str, value: int) -> None:
    if value != 1:
        raise ValueError(f"{name} must be exactly 1 in v0.37.6")


def _enum_value(value: Any) -> str:
    return value.value if isinstance(value, StrEnum) else str(value)


def _limit_text(text: str, limit: int = 500) -> str:
    _validate_non_negative("limit", limit)
    return text[:limit]


class VeraCodexTrialMode(StrEnum):
    ONE_SHOT_OPERATOR_EVALUATION = "one_shot_operator_evaluation"
    EVIDENCE_ONLY_TRIAL = "evidence_only_trial"
    REPAIR_SUGGESTION_REVIEW_TRIAL = "repair_suggestion_review_trial"
    DO_NOTHING_COMPARISON_TRIAL = "do_nothing_comparison_trial"
    HUMAN_HANDOFF_TRIAL = "human_handoff_trial"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class VeraCodexTrialSourceKind(StrEnum):
    V0375_REPAIR_SUGGESTION_ENVELOPE = "v0375_repair_suggestion_envelope"
    V0375_REPAIR_SUGGESTION_REPORT = "v0375_repair_suggestion_report"
    V0374_TEST_FEEDBACK_REPORT = "v0374_test_feedback_report"
    V0374_FAILURE_DIAGNOSIS_REPORT = "v0374_failure_diagnosis_report"
    V0373_TEST_RESULT_ENVELOPE = "v0373_test_result_envelope"
    V0372_TEST_EXECUTION_RESULT = "v0372_test_execution_result"
    V0369_PATCH_APPLY_SANDBOX_CONSOLIDATION = "v0369_patch_apply_sandbox_consolidation"
    MANUAL_OPERATOR_TASK = "manual_operator_task"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class VeraCodexTrialStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    INPUT_VALIDATED = "input_validated"
    EVIDENCE_BUNDLE_CREATED = "evidence_bundle_created"
    TRIAL_PACKET_CREATED = "trial_packet_created"
    ONE_SHOT_TRIAL_COMPLETED = "one_shot_trial_completed"
    ONE_SHOT_TRIAL_COMPLETED_WITH_WARNINGS = "one_shot_trial_completed_with_warnings"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATED = "future_gated"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class VeraCodexTrialReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    TRIAL_CONTRACT_READY = "trial_contract_ready"
    EVIDENCE_BUNDLE_READY = "evidence_bundle_ready"
    ONE_SHOT_TRIAL_PACKET_READY = "one_shot_trial_packet_ready"
    DECISION_TRACE_READY = "decision_trace_ready"
    HANDOFF_MEMO_READY = "handoff_memo_ready"
    FUTURE_COLD_EVALUATION_INPUT_READY = "future_cold_evaluation_input_ready"
    DESIGN_HANDOFF_READY_FOR_V0377 = "design_handoff_ready_for_v0377"
    DESIGN_HANDOFF_READY_FOR_V0378 = "design_handoff_ready_for_v0378"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class VeraCodexTrialDecisionKind(StrEnum):
    ALLOW_ONE_SHOT_TRIAL_PACKET = "allow_one_shot_trial_packet"
    ALLOW_EVIDENCE_BUNDLE = "allow_evidence_bundle"
    ALLOW_DECISION_TRACE = "allow_decision_trace"
    ALLOW_TASK_HANDLING_REPORT = "allow_task_handling_report"
    ALLOW_HANDOFF_MEMO = "allow_handoff_memo"
    ALLOW_FUTURE_COLD_EVALUATION_INPUT = "allow_future_cold_evaluation_input"
    CHOOSE_DO_NOTHING = "choose_do_nothing"
    CHOOSE_HUMAN_REVIEW = "choose_human_review"
    CHOOSE_FUTURE_REPAIR_PROPOSAL_GATE = "choose_future_repair_proposal_gate"
    CHOOSE_BLOCK = "choose_block"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class VeraCodexTrialRiskKind(StrEnum):
    MISSING_EVIDENCE_BUNDLE_RISK = "missing_evidence_bundle_risk"
    INSUFFICIENT_TEST_EVIDENCE_RISK = "insufficient_test_evidence_risk"
    OVERCLAIM_RISK = "overclaim_risk"
    SELF_PRAISE_RISK = "self_praise_risk"
    FAILED_TEST_REPORTED_AS_SUCCESS_RISK = "failed_test_reported_as_success_risk"
    INCONCLUSIVE_REPORTED_AS_SUCCESS_RISK = "inconclusive_reported_as_success_risk"
    DO_NOTHING_OMISSION_RISK = "do_nothing_omission_risk"
    REPAIR_EXECUTION_CONFUSION_RISK = "repair_execution_confusion_risk"
    MODEL_PROVIDER_INVOCATION_RISK = "model_provider_invocation_risk"
    TOOL_EXECUTION_RISK = "tool_execution_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    CODEX_CLI_INVOCATION_RISK = "codex_cli_invocation_risk"
    CLAUDE_CODE_INVOCATION_RISK = "claude_code_invocation_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    AUTOMATIC_REPAIR_RISK = "automatic_repair_risk"
    RETRY_LOOP_RISK = "retry_loop_risk"
    MULTI_CYCLE_LOOP_RISK = "multi_cycle_loop_risk"
    CHAIN_OF_THOUGHT_LEAK_RISK = "chain_of_thought_leak_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    UNKNOWN = "unknown"


class VeraCodexOperatorRoleKind(StrEnum):
    BOUNDED_OPERATOR = "bounded_operator"
    EVIDENCE_EVALUATOR = "evidence_evaluator"
    REPAIR_SUGGESTION_REVIEWER = "repair_suggestion_reviewer"
    DO_NOTHING_COMPARATOR = "do_nothing_comparator"
    HUMAN_HANDOFF_WRITER = "human_handoff_writer"
    AUTONOMOUS_AGENT = "autonomous_agent"
    EXTERNAL_AGENT = "external_agent"
    DOMINION_OPERATOR = "dominion_operator"
    UNKNOWN = "unknown"


class VeraCodexEvidenceUseKind(StrEnum):
    USES_TEST_RESULT_ENVELOPE = "uses_test_result_envelope"
    USES_FEEDBACK_REPORT = "uses_feedback_report"
    USES_REPAIR_SUGGESTION = "uses_repair_suggestion"
    USES_DO_NOTHING_SIGNAL = "uses_do_nothing_signal"
    USES_SAFETY_BOUNDARY = "uses_safety_boundary"
    MISSING_REQUIRED_EVIDENCE = "missing_required_evidence"
    IGNORED_EVIDENCE = "ignored_evidence"
    UNKNOWN = "unknown"


class VeraCodexTaskHandlingOutcomeKind(StrEnum):
    EVIDENCE_SUPPORTS_CONTINUE_TO_COLD_EVALUATION = "evidence_supports_continue_to_cold_evaluation"
    EVIDENCE_SUPPORTS_HUMAN_REVIEW = "evidence_supports_human_review"
    EVIDENCE_SUPPORTS_DO_NOTHING = "evidence_supports_do_nothing"
    EVIDENCE_SUPPORTS_FUTURE_REPAIR_PROPOSAL_GATE = "evidence_supports_future_repair_proposal_gate"
    EVIDENCE_INSUFFICIENT = "evidence_insufficient"
    SAFETY_BOUNDARY_BLOCKS = "safety_boundary_blocks"
    NO_ACTION = "no_action"
    UNKNOWN = "unknown"


class VeraCodexStopReasonKind(StrEnum):
    COMPLETED_ONE_SHOT_TRIAL = "completed_one_shot_trial"
    COMPLETED_WITH_WARNINGS = "completed_with_warnings"
    STOPPED_FOR_HUMAN_HANDOFF = "stopped_for_human_handoff"
    BLOCKED_BY_INSUFFICIENT_EVIDENCE = "blocked_by_insufficient_evidence"
    BLOCKED_BY_SAFETY_BOUNDARY = "blocked_by_safety_boundary"
    BLOCKED_BY_FAILED_TEST = "blocked_by_failed_test"
    BLOCKED_BY_INCONCLUSIVE_RESULT = "blocked_by_inconclusive_result"
    STOPPED_NO_RETRY_ALLOWED = "stopped_no_retry_allowed"
    STOPPED_NO_REPAIR_ALLOWED = "stopped_no_repair_allowed"
    FUTURE_GATED = "future_gated"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class VeraCodexHandoffKind(StrEnum):
    HUMAN_REVIEW_HANDOFF = "human_review_handoff"
    COLD_EVALUATION_HANDOFF = "cold_evaluation_handoff"
    FUTURE_REPAIR_PROPOSAL_HANDOFF = "future_repair_proposal_handoff"
    DO_NOTHING_HANDOFF = "do_nothing_handoff"
    BLOCKED_HANDOFF = "blocked_handoff"
    NO_OP_HANDOFF = "no_op_handoff"
    UNKNOWN = "unknown"


class VeraCodexSafetyCheckKind(StrEnum):
    NO_MODEL_PROVIDER_INVOCATION_CHECK = "no_model_provider_invocation_check"
    NO_TOOL_EXECUTION_CHECK = "no_tool_execution_check"
    NO_TEST_EXECUTION_CHECK = "no_test_execution_check"
    NO_SUBPROCESS_EXECUTION_CHECK = "no_subprocess_execution_check"
    NO_SHELL_EXECUTION_CHECK = "no_shell_execution_check"
    NO_REPAIR_EXECUTION_CHECK = "no_repair_execution_check"
    NO_PATCH_GENERATION_CHECK = "no_patch_generation_check"
    NO_EXTERNAL_AGENT_CHECK = "no_external_agent_check"
    NO_DOMINION_RUNTIME_CHECK = "no_dominion_runtime_check"
    NO_RETRY_LOOP_CHECK = "no_retry_loop_check"
    NO_MULTI_CYCLE_LOOP_CHECK = "no_multi_cycle_loop_check"
    NO_CHAIN_OF_THOUGHT_OUTPUT_CHECK = "no_chain_of_thought_output_check"
    DO_NOTHING_CONSIDERED_CHECK = "do_nothing_considered_check"
    HUMAN_HANDOFF_REQUIRED_CHECK = "human_handoff_required_check"
    EVIDENCE_REQUIRED_CHECK = "evidence_required_check"
    UNKNOWN = "unknown"


class VeraCodexTrialConfidenceLevel(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INCONCLUSIVE = "inconclusive"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class VeraCodexTrialFlagSet:
    flag_set_id: str = "vera_codex_trial_flags:v0.37.6"
    version: str = V0376_VERSION
    vera_codex_trial_layer_constructed: bool = True
    vera_codex_operator_profile_available: bool = True
    vera_codex_trial_input_available: bool = True
    vera_codex_evidence_bundle_available: bool = True
    vera_codex_trial_packet_available: bool = True
    vera_codex_decision_trace_available: bool = True
    vera_codex_task_handling_report_available: bool = True
    vera_codex_handoff_memo_available: bool = True
    ready_for_v0377_cold_agent_performance_evaluation: bool = True
    ready_for_v0378_cli_test_runner_agent_evaluation_surface: bool = True
    ready_for_vera_codex_one_shot_agent_trial: bool = True
    ready_for_vera_codex_trial_packet: bool = True
    ready_for_vera_codex_evidence_bundle: bool = True
    ready_for_vera_codex_decision_trace: bool = True
    ready_for_vera_codex_task_handling_report: bool = True
    ready_for_vera_codex_handoff_memo: bool = True
    ready_for_future_cold_evaluation_input: bool = True
    ready_for_execution: bool = False
    ready_for_model_provider_invocation: bool = False
    ready_for_tool_execution: bool = False
    ready_for_test_execution: bool = False
    ready_for_controlled_test_subprocess: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_dependency_install: bool = False
    ready_for_network_access: bool = False
    ready_for_live_workspace_write: bool = False
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_apply_patch: bool = False
    ready_for_git_apply: bool = False
    ready_for_repair_patch_proposal: bool = False
    ready_for_repair_diff_generation: bool = False
    ready_for_code_hunk_generation: bool = False
    ready_for_automatic_repair: bool = False
    ready_for_repair_execution: bool = False
    ready_for_repair_loop: bool = False
    ready_for_retry_loop: bool = False
    ready_for_multi_cycle_agentic_loop: bool = False
    ready_for_cold_agent_performance_evaluation: bool = False
    ready_for_external_agent_execution: bool = False
    ready_for_claude_code_invocation: bool = False
    ready_for_codex_cli_invocation: bool = False
    ready_for_dominion_runtime: bool = False
    ready_for_infinite_agent_loop: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_direct_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_secret_read: bool = False
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
        _validate_metadata(self.metadata)
        for name in UNSAFE_VERA_CODEX_FLAG_NAMES:
            _validate_false(name, getattr(self, name))


@dataclass(frozen=True)
class VeraCodexTrialSourceRef:
    source_ref_id: str = "vera_codex_source_ref:v0.37.6"
    source_kind: VeraCodexTrialSourceKind | str = VeraCodexTrialSourceKind.V0375_REPAIR_SUGGESTION_ENVELOPE
    source_id: str = "source:v0.37.6"
    source_summary: str = "supplied Vera-Codex trial metadata source; no fetch/read/write/execute"
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class VeraCodexTrialPolicy:
    trial_policy_id: str = "vera_codex_trial_policy:v0.37.6"
    version: str = V0376_VERSION
    allowed_modes: list[VeraCodexTrialMode | str] = field(default_factory=lambda: [
        VeraCodexTrialMode.ONE_SHOT_OPERATOR_EVALUATION,
        VeraCodexTrialMode.EVIDENCE_ONLY_TRIAL,
        VeraCodexTrialMode.REPAIR_SUGGESTION_REVIEW_TRIAL,
        VeraCodexTrialMode.DO_NOTHING_COMPARISON_TRIAL,
        VeraCodexTrialMode.HUMAN_HANDOFF_TRIAL,
    ])
    allowed_operator_roles: list[VeraCodexOperatorRoleKind | str] = field(default_factory=lambda: [
        VeraCodexOperatorRoleKind.BOUNDED_OPERATOR,
        VeraCodexOperatorRoleKind.EVIDENCE_EVALUATOR,
        VeraCodexOperatorRoleKind.REPAIR_SUGGESTION_REVIEWER,
        VeraCodexOperatorRoleKind.DO_NOTHING_COMPARATOR,
        VeraCodexOperatorRoleKind.HUMAN_HANDOFF_WRITER,
    ])
    required_safety_checks: list[VeraCodexSafetyCheckKind | str] = field(default_factory=lambda: [
        VeraCodexSafetyCheckKind.NO_MODEL_PROVIDER_INVOCATION_CHECK,
        VeraCodexSafetyCheckKind.NO_TOOL_EXECUTION_CHECK,
        VeraCodexSafetyCheckKind.NO_TEST_EXECUTION_CHECK,
        VeraCodexSafetyCheckKind.NO_REPAIR_EXECUTION_CHECK,
        VeraCodexSafetyCheckKind.NO_CHAIN_OF_THOUGHT_OUTPUT_CHECK,
        VeraCodexSafetyCheckKind.DO_NOTHING_CONSIDERED_CHECK,
        VeraCodexSafetyCheckKind.HUMAN_HANDOFF_REQUIRED_CHECK,
        VeraCodexSafetyCheckKind.EVIDENCE_REQUIRED_CHECK,
    ])
    max_trial_count: int = 1
    max_cycle_count: int = 1
    max_decision_trace_steps: int = 5
    max_evidence_items: int = 8
    require_evidence_bundle: bool = True
    require_do_nothing_assessment: bool = True
    require_repair_suggestion_assessment: bool = True
    require_stop_reason: bool = True
    require_human_handoff: bool = True
    allow_one_shot_trial: bool = True
    allow_future_cold_evaluation_input: bool = True
    allow_model_provider_invocation: bool = False
    allow_tool_execution: bool = False
    allow_test_execution: bool = False
    allow_subprocess: bool = False
    allow_shell: bool = False
    allow_dependency_install: bool = False
    allow_network_access: bool = False
    allow_repair_patch_proposal: bool = False
    allow_repair_execution: bool = False
    allow_automatic_repair: bool = False
    allow_retry_loop: bool = False
    allow_multi_cycle_loop: bool = False
    allow_external_agent_execution: bool = False
    allow_dominion_runtime: bool = False
    metadata: dict[str, Any] = field(default_factory=lambda: {
        "digestion_first_policy_applied": True,
        "dominion_runtime_blocked": True,
        "external_agent_execution_blocked": True,
        "model_provider_invocation_blocked": True,
        "tool_execution_blocked": True,
        "bounded_vera_codex_evaluation_only": True,
        "mandatory_human_handoff_after_evaluation": True,
    })

    def __post_init__(self) -> None:
        _require_non_blank("trial_policy_id", self.trial_policy_id)
        _validate_version(self.version)
        _validate_list("allowed_modes", self.allowed_modes)
        _validate_list("allowed_operator_roles", self.allowed_operator_roles)
        _validate_list("required_safety_checks", self.required_safety_checks)
        _validate_exactly_one("max_trial_count", self.max_trial_count)
        _validate_exactly_one("max_cycle_count", self.max_cycle_count)
        if self.max_decision_trace_steps < 1:
            raise ValueError("max_decision_trace_steps must be >= 1")
        _validate_non_negative("max_evidence_items", self.max_evidence_items)
        for name in UNSAFE_VERA_CODEX_POLICY_ALLOW_NAMES:
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class VeraCodexOperatorProfile:
    operator_profile_id: str = "vera_codex_operator_profile:v0.37.6"
    version: str = V0376_VERSION
    role_kind: VeraCodexOperatorRoleKind | str = VeraCodexOperatorRoleKind.BOUNDED_OPERATOR
    profile_summary: str = "bounded evidence evaluator; no provider, tool, external agent, or Dominion authority"
    bounded_operator: bool = True
    evidence_evaluator: bool = True
    autonomous_agent: bool = False
    external_agent: bool = False
    dominion_operator: bool = False
    model_provider_invocation_allowed: bool = False
    tool_execution_allowed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("operator_profile_id", self.operator_profile_id)
        _validate_version(self.version)
        _require_non_blank("profile_summary", self.profile_summary)
        if _enum_value(self.role_kind) in (
            VeraCodexOperatorRoleKind.AUTONOMOUS_AGENT.value,
            VeraCodexOperatorRoleKind.EXTERNAL_AGENT.value,
            VeraCodexOperatorRoleKind.DOMINION_OPERATOR.value,
        ):
            raise ValueError("autonomous/external/Dominion operator roles are blocked in v0.37.6")
        _validate_false("autonomous_agent", self.autonomous_agent)
        _validate_false("external_agent", self.external_agent)
        _validate_false("dominion_operator", self.dominion_operator)
        _validate_false("model_provider_invocation_allowed", self.model_provider_invocation_allowed)
        _validate_false("tool_execution_allowed", self.tool_execution_allowed)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class VeraCodexTrialInput:
    trial_input_id: str = "vera_codex_trial_input:v0.37.6"
    version: str = V0376_VERSION
    requested_mode: VeraCodexTrialMode | str = VeraCodexTrialMode.ONE_SHOT_OPERATOR_EVALUATION
    task_summary: str = "one-shot evidence-bounded Vera-Codex metadata trial request"
    repair_suggestion_id: str | None = None
    feedback_report_id: str | None = None
    result_envelope_id: str | None = None
    execution_result_id: str | None = None
    operator_task_ref: str | None = None
    source_refs: list[VeraCodexTrialSourceRef] = field(default_factory=list)
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(PROHIBITED_TRIAL_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("trial_input_id", self.trial_input_id)
        _validate_version(self.version)
        _require_non_blank("task_summary", self.task_summary)
        _validate_list("source_refs", self.source_refs)
        _validate_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        missing = [action for action in PROHIBITED_TRIAL_ACTIONS if action not in self.prohibited_runtime_actions]
        if missing:
            raise ValueError(f"prohibited_runtime_actions missing required entries: {missing}")
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class VeraCodexEvidenceItem:
    evidence_item_id: str = "vera_codex_evidence_item:v0.37.6"
    evidence_use_kind: VeraCodexEvidenceUseKind | str = VeraCodexEvidenceUseKind.USES_REPAIR_SUGGESTION
    source_ref_id: str | None = None
    evidence_summary: str = "supplied evidence metadata item"
    evidence_strength: str = "moderate"
    confidence: VeraCodexTrialConfidenceLevel | str = VeraCodexTrialConfidenceLevel.MEDIUM
    required: bool = True
    present: bool = True
    redacted: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("evidence_item_id", self.evidence_item_id)
        _require_non_blank("evidence_summary", self.evidence_summary)
        _require_non_blank("evidence_strength", self.evidence_strength)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class VeraCodexEvidenceBundle:
    evidence_bundle_id: str = "vera_codex_evidence_bundle:v0.37.6"
    version: str = V0376_VERSION
    evidence_items: list[VeraCodexEvidenceItem] = field(default_factory=list)
    bundle_summary: str = "bounded evidence bundle for one-shot metadata trial"
    required_evidence_present: bool = True
    sufficient_for_one_shot_trial: bool = True
    sufficient_for_cold_evaluation_input: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("evidence_bundle_id", self.evidence_bundle_id)
        _validate_version(self.version)
        _validate_list("evidence_items", self.evidence_items)
        _require_non_blank("bundle_summary", self.bundle_summary)
        required_present = all((not item.required) or item.present for item in self.evidence_items)
        if self.required_evidence_present and not required_present:
            raise ValueError("required_evidence_present cannot be True when required evidence is missing")
        if self.sufficient_for_one_shot_trial and not self.required_evidence_present:
            raise ValueError("sufficient_for_one_shot_trial requires required evidence present")
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class VeraCodexTrialTask:
    trial_task_id: str = "vera_codex_trial_task:v0.37.6"
    task_summary: str = "evaluate supplied evidence once and create handoff metadata"
    expected_operator_output: str = "bounded metadata packet with stop reason and human handoff"
    non_goals: list[str] = field(default_factory=lambda: [
        "model provider invocation",
        "tool execution",
        "repair execution",
        "chain-of-thought output",
        "autonomous runtime",
    ])
    do_nothing_required: bool = True
    human_handoff_required: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("trial_task_id", self.trial_task_id)
        _require_non_blank("task_summary", self.task_summary)
        _require_non_blank("expected_operator_output", self.expected_operator_output)
        _validate_list("non_goals", self.non_goals)
        _validate_true("do_nothing_required", self.do_nothing_required)
        _validate_true("human_handoff_required", self.human_handoff_required)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class VeraCodexOperationConstraintSet:
    constraint_set_id: str = "vera_codex_constraints:v0.37.6"
    max_trial_count: int = 1
    max_cycle_count: int = 1
    automatic_retry_allowed: bool = False
    automatic_repair_allowed: bool = False
    model_provider_invocation_allowed: bool = False
    tool_execution_allowed: bool = False
    external_agent_execution_allowed: bool = False
    dominion_runtime_allowed: bool = False
    test_execution_allowed: bool = False
    patch_generation_allowed: bool = False
    file_write_allowed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("constraint_set_id", self.constraint_set_id)
        _validate_exactly_one("max_trial_count", self.max_trial_count)
        _validate_exactly_one("max_cycle_count", self.max_cycle_count)
        for name in (
            "automatic_retry_allowed",
            "automatic_repair_allowed",
            "model_provider_invocation_allowed",
            "tool_execution_allowed",
            "external_agent_execution_allowed",
            "dominion_runtime_allowed",
            "test_execution_allowed",
            "patch_generation_allowed",
            "file_write_allowed",
        ):
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class VeraCodexDecisionTraceStep:
    decision_trace_step_id: str = "vera_codex_trace_step:v0.37.6:0"
    step_index: int = 0
    step_summary: str = "bounded evidence summary step; no hidden reasoning"
    evidence_refs: list[str] = field(default_factory=list)
    risk_kinds: list[VeraCodexTrialRiskKind | str] = field(default_factory=list)
    decision_kind: VeraCodexTrialDecisionKind | str = VeraCodexTrialDecisionKind.ALLOW_DECISION_TRACE
    confidence: VeraCodexTrialConfidenceLevel | str = VeraCodexTrialConfidenceLevel.MEDIUM
    contains_chain_of_thought: bool = False
    executed_action: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("decision_trace_step_id", self.decision_trace_step_id)
        _require_non_blank("step_summary", self.step_summary)
        _validate_non_negative("step_index", self.step_index)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_list("risk_kinds", self.risk_kinds)
        _validate_false("contains_chain_of_thought", self.contains_chain_of_thought)
        _validate_false("executed_action", self.executed_action)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class VeraCodexDecisionTrace:
    decision_trace_id: str = "vera_codex_decision_trace:v0.37.6"
    version: str = V0376_VERSION
    trace_steps: list[VeraCodexDecisionTraceStep] = field(default_factory=list)
    trace_summary: str = "bounded decision trace metadata; not chain-of-thought"
    bounded_trace: bool = True
    contains_chain_of_thought: bool = False
    executed_actions: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("decision_trace_id", self.decision_trace_id)
        _validate_version(self.version)
        _validate_list("trace_steps", self.trace_steps)
        _require_non_blank("trace_summary", self.trace_summary)
        _validate_true("bounded_trace", self.bounded_trace)
        _validate_false("contains_chain_of_thought", self.contains_chain_of_thought)
        _validate_false("executed_actions", self.executed_actions)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class VeraCodexDoNothingAssessment:
    do_nothing_assessment_id: str = "vera_codex_do_nothing:v0.37.6"
    assessment_summary: str = "do-nothing alternative explicitly represented"
    do_nothing_valid: bool = True
    do_nothing_preferred: bool = False
    do_nothing_reason: str = "do nothing remains valid until human review or future gate"
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("do_nothing_assessment_id", self.do_nothing_assessment_id)
        _require_non_blank("assessment_summary", self.assessment_summary)
        _require_non_blank("do_nothing_reason", self.do_nothing_reason)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class VeraCodexRepairSuggestionAssessment:
    repair_assessment_id: str = "vera_codex_repair_assessment:v0.37.6"
    repair_suggestion_id: str | None = None
    assessment_summary: str = "repair suggestion reviewed as future-gated metadata only"
    supports_future_repair_proposal: bool = True
    supports_repair_now: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    confidence: VeraCodexTrialConfidenceLevel | str = VeraCodexTrialConfidenceLevel.MEDIUM
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("repair_assessment_id", self.repair_assessment_id)
        _require_non_blank("assessment_summary", self.assessment_summary)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_false("supports_repair_now", self.supports_repair_now)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class VeraCodexTaskHandlingAssessment:
    task_handling_assessment_id: str = "vera_codex_task_handling:v0.37.6"
    outcome_kind: VeraCodexTaskHandlingOutcomeKind | str = VeraCodexTaskHandlingOutcomeKind.EVIDENCE_SUPPORTS_HUMAN_REVIEW
    assessment_summary: str = "one-shot task handling metadata assessment"
    evidence_bundle_id: str = "vera_codex_evidence_bundle:v0.37.6"
    do_nothing_assessment: VeraCodexDoNothingAssessment = field(default_factory=VeraCodexDoNothingAssessment)
    repair_suggestion_assessment: VeraCodexRepairSuggestionAssessment = field(default_factory=VeraCodexRepairSuggestionAssessment)
    confidence: VeraCodexTrialConfidenceLevel | str = VeraCodexTrialConfidenceLevel.MEDIUM
    passed_as_success: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("task_handling_assessment_id", self.task_handling_assessment_id)
        _require_non_blank("assessment_summary", self.assessment_summary)
        _require_non_blank("evidence_bundle_id", self.evidence_bundle_id)
        if self.passed_as_success and _enum_value(self.outcome_kind) not in (VeraCodexTaskHandlingOutcomeKind.EVIDENCE_SUPPORTS_CONTINUE_TO_COLD_EVALUATION.value,):
            raise ValueError("passed_as_success requires strong non-blocking evidence and is not production certification")
        _validate_false("production_certified", self.production_certified)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class VeraCodexTrialDecision:
    trial_decision_id: str = "vera_codex_trial_decision:v0.37.6"
    decision_kind: VeraCodexTrialDecisionKind | str = VeraCodexTrialDecisionKind.CHOOSE_HUMAN_REVIEW
    decision_summary: str = "metadata-only one-shot trial decision"
    rationale_summary: str = "bounded rationale summary over supplied evidence only"
    confidence: VeraCodexTrialConfidenceLevel | str = VeraCodexTrialConfidenceLevel.MEDIUM
    evidence_refs: list[str] = field(default_factory=list)
    executes_now: bool = False
    repair_allowed: bool = False
    retry_allowed: bool = False
    model_invocation_allowed: bool = False
    tool_execution_allowed: bool = False
    external_agent_allowed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("trial_decision_id", self.trial_decision_id)
        _require_non_blank("decision_summary", self.decision_summary)
        _require_non_blank("rationale_summary", self.rationale_summary)
        _validate_list("evidence_refs", self.evidence_refs)
        for name in ("executes_now", "repair_allowed", "retry_allowed", "model_invocation_allowed", "tool_execution_allowed", "external_agent_allowed"):
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class VeraCodexStopReason:
    stop_reason_id: str = "vera_codex_stop_reason:v0.37.6"
    stop_reason_kind: VeraCodexStopReasonKind | str = VeraCodexStopReasonKind.STOPPED_FOR_HUMAN_HANDOFF
    stop_summary: str = "one-shot metadata trial stopped for mandatory human handoff"
    human_handoff_required: bool = True
    allows_continuation: bool = False
    allows_retry: bool = False
    allows_repair: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("stop_reason_id", self.stop_reason_id)
        _require_non_blank("stop_summary", self.stop_summary)
        _validate_true("human_handoff_required", self.human_handoff_required)
        _validate_false("allows_continuation", self.allows_continuation)
        _validate_false("allows_retry", self.allows_retry)
        _validate_false("allows_repair", self.allows_repair)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class VeraCodexHandoffMemo:
    handoff_memo_id: str = "vera_codex_handoff_memo:v0.37.6"
    handoff_kind: VeraCodexHandoffKind | str = VeraCodexHandoffKind.HUMAN_REVIEW_HANDOFF
    memo_summary: str = "mandatory human handoff memo; metadata only"
    key_evidence_refs: list[str] = field(default_factory=list)
    recommended_human_action: str = "review the one-shot metadata packet before any future gate"
    blocked_actions: list[str] = field(default_factory=lambda: list(PROHIBITED_TRIAL_ACTIONS))
    ready_for_cold_evaluation_input: bool = True
    executes_action: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("handoff_memo_id", self.handoff_memo_id)
        _require_non_blank("memo_summary", self.memo_summary)
        _require_non_blank("recommended_human_action", self.recommended_human_action)
        _validate_list("key_evidence_refs", self.key_evidence_refs)
        _validate_list("blocked_actions", self.blocked_actions)
        _validate_false("executes_action", self.executes_action)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class VeraCodexTrialSafetyFinding:
    safety_finding_id: str = "vera_codex_safety_finding:v0.37.6"
    check_kind: VeraCodexSafetyCheckKind | str = VeraCodexSafetyCheckKind.NO_MODEL_PROVIDER_INVOCATION_CHECK
    severity: str = "info"
    finding_summary: str = "safety check represented as metadata"
    evidence_preview: str = ""
    blocked: bool = False
    requires_review: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("safety_finding_id", self.safety_finding_id)
        _require_non_blank("severity", self.severity)
        _require_non_blank("finding_summary", self.finding_summary)
        object.__setattr__(self, "evidence_preview", _limit_text(self.evidence_preview, 500))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class VeraCodexTrialSafetyReport:
    safety_report_id: str = "vera_codex_safety_report:v0.37.6"
    version: str = V0376_VERSION
    safety_findings: list[VeraCodexTrialSafetyFinding] = field(default_factory=list)
    required_checks: list[VeraCodexSafetyCheckKind | str] = field(default_factory=list)
    passed_checks: list[VeraCodexSafetyCheckKind | str] = field(default_factory=list)
    failed_checks: list[VeraCodexSafetyCheckKind | str] = field(default_factory=list)
    blocked: bool = False
    requires_review: bool = False
    summary: str = "Vera-Codex one-shot trial safety report; no runtime permission"
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("safety_report_id", self.safety_report_id)
        _validate_version(self.version)
        for name in ("safety_findings", "required_checks", "passed_checks", "failed_checks"):
            _validate_list(name, getattr(self, name))
        _require_non_blank("summary", self.summary)
        _validate_false("ready_for_execution", self.ready_for_execution)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class VeraCodexOneShotTrialPacket:
    trial_packet_id: str = "vera_codex_one_shot_packet:v0.37.6"
    version: str = V0376_VERSION
    operator_profile: VeraCodexOperatorProfile = field(default_factory=VeraCodexOperatorProfile)
    trial_input: VeraCodexTrialInput = field(default_factory=VeraCodexTrialInput)
    trial_task: VeraCodexTrialTask = field(default_factory=VeraCodexTrialTask)
    constraint_set: VeraCodexOperationConstraintSet = field(default_factory=VeraCodexOperationConstraintSet)
    evidence_bundle: VeraCodexEvidenceBundle = field(default_factory=VeraCodexEvidenceBundle)
    decision_trace: VeraCodexDecisionTrace = field(default_factory=VeraCodexDecisionTrace)
    task_handling_assessment: VeraCodexTaskHandlingAssessment = field(default_factory=VeraCodexTaskHandlingAssessment)
    trial_decision: VeraCodexTrialDecision = field(default_factory=VeraCodexTrialDecision)
    safety_report: VeraCodexTrialSafetyReport = field(default_factory=VeraCodexTrialSafetyReport)
    stop_reason: VeraCodexStopReason = field(default_factory=VeraCodexStopReason)
    handoff_memo: VeraCodexHandoffMemo = field(default_factory=VeraCodexHandoffMemo)
    source_refs: list[VeraCodexTrialSourceRef] = field(default_factory=list)
    status: VeraCodexTrialStatus | str = VeraCodexTrialStatus.ONE_SHOT_TRIAL_COMPLETED
    readiness_level: VeraCodexTrialReadinessLevel | str = VeraCodexTrialReadinessLevel.ONE_SHOT_TRIAL_PACKET_READY
    trial_count: int = 1
    max_cycle_count: int = 1
    completed_one_shot: bool = True
    automatic_retry_allowed: bool = False
    automatic_repair_allowed: bool = False
    human_handoff_required: bool = True
    eligible_for_future_cold_evaluation: bool = True
    test_execution_performed: bool = False
    model_invocation_performed: bool = False
    tool_execution_performed: bool = False
    repair_performed: bool = False
    production_certified: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("trial_packet_id", self.trial_packet_id)
        _validate_version(self.version)
        _validate_list("source_refs", self.source_refs)
        _validate_exactly_one("trial_count", self.trial_count)
        _validate_exactly_one("max_cycle_count", self.max_cycle_count)
        _validate_false("automatic_retry_allowed", self.automatic_retry_allowed)
        _validate_false("automatic_repair_allowed", self.automatic_repair_allowed)
        _validate_true("human_handoff_required", self.human_handoff_required)
        for name in ("test_execution_performed", "model_invocation_performed", "tool_execution_performed", "repair_performed", "production_certified", "ready_for_execution"):
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class VeraCodexTrialValidationFinding:
    validation_finding_id: str = "vera_codex_validation_finding:v0.37.6"
    risk_kind: VeraCodexTrialRiskKind | str = VeraCodexTrialRiskKind.UNKNOWN
    severity: str = "info"
    message: str = "validation finding"
    blocks_trial: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_finding_id", self.validation_finding_id)
        _require_non_blank("severity", self.severity)
        _require_non_blank("message", self.message)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class VeraCodexTrialValidationReport:
    validation_report_id: str = "vera_codex_validation_report:v0.37.6"
    version: str = V0376_VERSION
    trial_packet_id: str | None = None
    findings: list[VeraCodexTrialValidationFinding] = field(default_factory=list)
    one_shot_confirmed: bool = True
    evidence_bundle_confirmed: bool = True
    no_runtime_execution_confirmed: bool = True
    no_chain_of_thought_confirmed: bool = True
    human_handoff_confirmed: bool = True
    stop_reason_confirmed: bool = True
    valid: bool = True
    summary: str = "Vera-Codex one-shot trial validation report"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version(self.version)
        _validate_list("findings", self.findings)
        _require_non_blank("summary", self.summary)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class VeraCodexTrialReport:
    trial_report_id: str = "vera_codex_trial_report:v0.37.6"
    version: str = V0376_VERSION
    trial_packet: VeraCodexOneShotTrialPacket = field(default_factory=VeraCodexOneShotTrialPacket)
    validation_report: VeraCodexTrialValidationReport = field(default_factory=VeraCodexTrialValidationReport)
    report_summary: str = "one-shot metadata trial report; not scorecard or certification"
    one_shot_completed: bool = True
    eligible_for_future_cold_evaluation: bool = True
    production_certified: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("trial_report_id", self.trial_report_id)
        _validate_version(self.version)
        _require_non_blank("report_summary", self.report_summary)
        _validate_false("production_certified", self.production_certified)
        _validate_false("ready_for_execution", self.ready_for_execution)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class VeraCodexTrialRunPreview:
    run_preview_id: str = "vera_codex_run_preview:v0.37.6"
    version: str = V0376_VERSION
    preview_summary: str = "preview only; does not invoke provider, tools, tests, repair, or agents"
    would_call_model_provider: bool = False
    would_execute_tools: bool = False
    would_run_tests: bool = False
    would_repair: bool = False
    would_use_external_agent: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        _validate_version(self.version)
        _require_non_blank("preview_summary", self.preview_summary)
        for name in ("would_call_model_provider", "would_execute_tools", "would_run_tests", "would_repair", "would_use_external_agent"):
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class VeraCodexNoAutonomyGuarantee:
    guarantee_id: str = "vera_codex_no_autonomy_guarantee:v0.37.6"
    version: str = V0376_VERSION
    no_model_provider_invocation: bool = True
    no_codex_cli_invocation: bool = True
    no_claude_code_invocation: bool = True
    no_external_agent_execution: bool = True
    no_tool_execution: bool = True
    no_test_execution: bool = True
    no_subprocess_execution: bool = True
    no_shell_execution: bool = True
    no_dependency_install: bool = True
    no_network_access: bool = True
    no_patch_generation: bool = True
    no_repair_execution: bool = True
    no_retry_loop: bool = True
    no_multi_cycle_loop: bool = True
    no_cold_evaluation_execution: bool = True
    no_dominion_runtime: bool = True
    no_chain_of_thought_output: bool = True
    no_production_certification: bool = True
    summary: str = "all v0.37.6 no-autonomy guarantees are true"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version(self.version)
        _require_non_blank("summary", self.summary)
        for name, value in self.__dict__.items():
            if name.startswith("no_"):
                _validate_true(name, value)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class V0376ReadinessReport:
    readiness_report_id: str = "v0376_readiness_report"
    version: str = V0376_VERSION
    release_name: str = V0376_RELEASE_NAME
    ready_for_v0377_cold_agent_performance_evaluation: bool = True
    ready_for_v0378_cli_test_runner_agent_evaluation_surface: bool = True
    ready_for_vera_codex_one_shot_agent_trial: bool = True
    ready_for_vera_codex_trial_packet: bool = True
    ready_for_vera_codex_evidence_bundle: bool = True
    ready_for_vera_codex_decision_trace: bool = True
    ready_for_vera_codex_task_handling_report: bool = True
    ready_for_vera_codex_handoff_memo: bool = True
    ready_for_future_cold_evaluation_input: bool = True
    ready_for_execution: bool = False
    ready_for_model_provider_invocation: bool = False
    ready_for_tool_execution: bool = False
    ready_for_test_execution: bool = False
    ready_for_controlled_test_subprocess: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_dependency_install: bool = False
    ready_for_network_access: bool = False
    ready_for_repair_patch_proposal: bool = False
    ready_for_repair_diff_generation: bool = False
    ready_for_code_hunk_generation: bool = False
    ready_for_automatic_repair: bool = False
    ready_for_repair_execution: bool = False
    ready_for_multi_cycle_agentic_loop: bool = False
    ready_for_cold_agent_performance_evaluation: bool = False
    ready_for_external_agent_execution: bool = False
    ready_for_dominion_runtime: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=lambda: {
        "digestion_first_policy_applied": True,
        "dominion_runtime_blocked": True,
        "external_agent_execution_blocked": True,
        "infinite_agent_loop_blocked": True,
        "recursive_self_invocation_blocked": True,
        "automatic_repair_loop_blocked": True,
        "repair_execution_blocked": True,
        "model_provider_invocation_blocked": True,
        "tool_execution_blocked": True,
        "bounded_vera_codex_evaluation_only": True,
        "no_independent_autonomous_agent_runtime": True,
        "mandatory_human_handoff_after_evaluation": True,
    })

    def __post_init__(self) -> None:
        _require_non_blank("readiness_report_id", self.readiness_report_id)
        _validate_version(self.version)
        _require_non_blank("release_name", self.release_name)
        for name in (
            "ready_for_execution",
            "ready_for_model_provider_invocation",
            "ready_for_tool_execution",
            "ready_for_test_execution",
            "ready_for_controlled_test_subprocess",
            "ready_for_shell_execution",
            "ready_for_subprocess_execution",
            "ready_for_command_execution",
            "ready_for_dependency_install",
            "ready_for_network_access",
            "ready_for_repair_patch_proposal",
            "ready_for_repair_diff_generation",
            "ready_for_code_hunk_generation",
            "ready_for_automatic_repair",
            "ready_for_repair_execution",
            "ready_for_multi_cycle_agentic_loop",
            "ready_for_cold_agent_performance_evaluation",
            "ready_for_external_agent_execution",
            "ready_for_dominion_runtime",
            "production_certified",
        ):
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


def build_vera_codex_trial_flags(**kwargs: Any) -> VeraCodexTrialFlagSet:
    return VeraCodexTrialFlagSet(**kwargs)


def build_vera_codex_trial_source_ref(**kwargs: Any) -> VeraCodexTrialSourceRef:
    return VeraCodexTrialSourceRef(**kwargs)


def build_vera_codex_trial_policy(**kwargs: Any) -> VeraCodexTrialPolicy:
    return VeraCodexTrialPolicy(**kwargs)


def build_vera_codex_operator_profile(**kwargs: Any) -> VeraCodexOperatorProfile:
    return VeraCodexOperatorProfile(**kwargs)


def build_vera_codex_trial_input(**kwargs: Any) -> VeraCodexTrialInput:
    return VeraCodexTrialInput(**kwargs)


def build_vera_codex_evidence_item(**kwargs: Any) -> VeraCodexEvidenceItem:
    return VeraCodexEvidenceItem(**kwargs)


def build_vera_codex_evidence_bundle(**kwargs: Any) -> VeraCodexEvidenceBundle:
    return VeraCodexEvidenceBundle(**kwargs)


def build_vera_codex_trial_task(**kwargs: Any) -> VeraCodexTrialTask:
    return VeraCodexTrialTask(**kwargs)


def build_vera_codex_operation_constraint_set(**kwargs: Any) -> VeraCodexOperationConstraintSet:
    return VeraCodexOperationConstraintSet(**kwargs)


def build_vera_codex_decision_trace_step(**kwargs: Any) -> VeraCodexDecisionTraceStep:
    return VeraCodexDecisionTraceStep(**kwargs)


def build_vera_codex_decision_trace(**kwargs: Any) -> VeraCodexDecisionTrace:
    return VeraCodexDecisionTrace(**kwargs)


def build_vera_codex_do_nothing_assessment(**kwargs: Any) -> VeraCodexDoNothingAssessment:
    return VeraCodexDoNothingAssessment(**kwargs)


def build_vera_codex_repair_suggestion_assessment(**kwargs: Any) -> VeraCodexRepairSuggestionAssessment:
    return VeraCodexRepairSuggestionAssessment(**kwargs)


def build_vera_codex_task_handling_assessment(**kwargs: Any) -> VeraCodexTaskHandlingAssessment:
    return VeraCodexTaskHandlingAssessment(**kwargs)


def build_vera_codex_trial_decision(**kwargs: Any) -> VeraCodexTrialDecision:
    return VeraCodexTrialDecision(**kwargs)


def build_vera_codex_stop_reason(**kwargs: Any) -> VeraCodexStopReason:
    return VeraCodexStopReason(**kwargs)


def build_vera_codex_handoff_memo(**kwargs: Any) -> VeraCodexHandoffMemo:
    return VeraCodexHandoffMemo(**kwargs)


def build_vera_codex_trial_safety_finding(**kwargs: Any) -> VeraCodexTrialSafetyFinding:
    return VeraCodexTrialSafetyFinding(**kwargs)


def build_vera_codex_trial_safety_report(**kwargs: Any) -> VeraCodexTrialSafetyReport:
    return VeraCodexTrialSafetyReport(**kwargs)


def build_vera_codex_one_shot_trial_packet(**kwargs: Any) -> VeraCodexOneShotTrialPacket:
    return VeraCodexOneShotTrialPacket(**kwargs)


def build_vera_codex_trial_validation_finding(**kwargs: Any) -> VeraCodexTrialValidationFinding:
    return VeraCodexTrialValidationFinding(**kwargs)


def build_vera_codex_trial_validation_report(**kwargs: Any) -> VeraCodexTrialValidationReport:
    return VeraCodexTrialValidationReport(**kwargs)


def build_vera_codex_trial_report(**kwargs: Any) -> VeraCodexTrialReport:
    return VeraCodexTrialReport(**kwargs)


def build_vera_codex_trial_run_preview(**kwargs: Any) -> VeraCodexTrialRunPreview:
    return VeraCodexTrialRunPreview(**kwargs)


def build_vera_codex_no_autonomy_guarantee(**kwargs: Any) -> VeraCodexNoAutonomyGuarantee:
    return VeraCodexNoAutonomyGuarantee(**kwargs)


def build_v0376_readiness_report(**kwargs: Any) -> V0376ReadinessReport:
    return V0376ReadinessReport(**kwargs)


def default_vera_codex_trial_policy(**kwargs: Any) -> VeraCodexTrialPolicy:
    return build_vera_codex_trial_policy(**kwargs)


def build_vera_codex_trial_input_from_repair_suggestion(
    repair_suggestion: SandboxRepairSuggestionEnvelope,
    **kwargs: Any,
) -> VeraCodexTrialInput:
    source = build_vera_codex_trial_source_ref(
        source_ref_id=f"vera_codex_source:{repair_suggestion.repair_suggestion_id}",
        source_kind=VeraCodexTrialSourceKind.V0375_REPAIR_SUGGESTION_ENVELOPE,
        source_id=repair_suggestion.repair_suggestion_id,
        source_summary="supplied v0.37.5 repair suggestion envelope; metadata only",
        evidence_refs=[e.repair_evidence_id for e in repair_suggestion.evidence_refs],
    )
    return build_vera_codex_trial_input(
        repair_suggestion_id=repair_suggestion.repair_suggestion_id,
        result_envelope_id=repair_suggestion.metadata.get("result_envelope_id"),
        task_summary="one-shot Vera-Codex metadata trial over supplied v0.37.5 repair suggestion",
        source_refs=[source],
        **kwargs,
    )


def _confidence_from_repair(confidence: Any) -> VeraCodexTrialConfidenceLevel:
    value = _enum_value(confidence)
    if value == SandboxRepairConfidenceLevel.HIGH.value:
        return VeraCodexTrialConfidenceLevel.HIGH
    if value == SandboxRepairConfidenceLevel.MEDIUM.value:
        return VeraCodexTrialConfidenceLevel.MEDIUM
    if value == SandboxRepairConfidenceLevel.LOW.value:
        return VeraCodexTrialConfidenceLevel.LOW
    if value == SandboxRepairConfidenceLevel.INCONCLUSIVE.value:
        return VeraCodexTrialConfidenceLevel.INCONCLUSIVE
    return VeraCodexTrialConfidenceLevel.UNKNOWN


def build_vera_codex_evidence_bundle_from_v037_artifacts(
    repair_suggestion: SandboxRepairSuggestionEnvelope | None = None,
    feedback_report: SandboxTestFeedbackReport | None = None,
    result_envelope: SandboxTestResultEnvelope | None = None,
    policy: VeraCodexTrialPolicy | None = None,
) -> VeraCodexEvidenceBundle:
    policy = policy or default_vera_codex_trial_policy()
    items: list[VeraCodexEvidenceItem] = []
    if result_envelope is not None:
        outcome = _enum_value(result_envelope.outcome_classification.outcome_kind)
        required_present = outcome not in (SandboxTestOutcomeKind.UNKNOWN.value,)
        items.append(build_vera_codex_evidence_item(
            evidence_item_id=f"vera_codex_evidence:result:{result_envelope.result_envelope_id}",
            evidence_use_kind=VeraCodexEvidenceUseKind.USES_TEST_RESULT_ENVELOPE,
            source_ref_id=result_envelope.result_envelope_id,
            evidence_summary=f"v0.37.3 result envelope outcome={outcome}; not certification",
            evidence_strength="strong" if required_present else "insufficient",
            confidence=VeraCodexTrialConfidenceLevel.MEDIUM if required_present else VeraCodexTrialConfidenceLevel.INCONCLUSIVE,
            required=True,
            present=required_present,
        ))
    if feedback_report is not None:
        items.append(build_vera_codex_evidence_item(
            evidence_item_id=f"vera_codex_evidence:feedback:{feedback_report.feedback_report_id}",
            evidence_use_kind=VeraCodexEvidenceUseKind.USES_FEEDBACK_REPORT,
            source_ref_id=feedback_report.feedback_report_id,
            evidence_summary="v0.37.4 feedback report supplied; diagnosis remains metadata",
            evidence_strength="moderate",
            confidence=VeraCodexTrialConfidenceLevel.MEDIUM,
            required=False,
            present=True,
        ))
    if repair_suggestion is not None:
        items.append(build_vera_codex_evidence_item(
            evidence_item_id=f"vera_codex_evidence:repair:{repair_suggestion.repair_suggestion_id}",
            evidence_use_kind=VeraCodexEvidenceUseKind.USES_REPAIR_SUGGESTION,
            source_ref_id=repair_suggestion.repair_suggestion_id,
            evidence_summary=f"v0.37.5 repair suggestion kind={_enum_value(repair_suggestion.suggestion_kind)}; no patch",
            evidence_strength="moderate" if not repair_suggestion.risk_assessment.blocks_future_repair_proposal else "insufficient",
            confidence=_confidence_from_repair(repair_suggestion.confidence),
            required=True,
            present=True,
        ))
        items.append(build_vera_codex_evidence_item(
            evidence_item_id=f"vera_codex_evidence:do_nothing:{repair_suggestion.repair_suggestion_id}",
            evidence_use_kind=VeraCodexEvidenceUseKind.USES_DO_NOTHING_SIGNAL,
            source_ref_id=repair_suggestion.do_nothing_comparison.do_nothing_comparison_id,
            evidence_summary="v0.37.5 do-nothing comparison supplied; remains valid comparator",
            evidence_strength="moderate",
            confidence=VeraCodexTrialConfidenceLevel.MEDIUM,
            required=True,
            present=repair_suggestion.do_nothing_comparison.do_nothing_remains_valid,
        ))
    items.append(build_vera_codex_evidence_item(
        evidence_item_id="vera_codex_evidence:safety:v0.37.6",
        evidence_use_kind=VeraCodexEvidenceUseKind.USES_SAFETY_BOUNDARY,
        evidence_summary="v0.37.6 safety boundary blocks provider/tool/test/repair/autonomy execution",
        evidence_strength="strong",
        confidence=VeraCodexTrialConfidenceLevel.HIGH,
        required=True,
        present=True,
    ))
    if len(items) > policy.max_evidence_items:
        items = items[:policy.max_evidence_items]
    required_present = all((not item.required) or item.present for item in items)
    insufficient_required_evidence = any(
        item.required
        and (
            item.evidence_strength in ("insufficient", "contradictory", "unknown")
            or _enum_value(item.confidence) in (VeraCodexTrialConfidenceLevel.INCONCLUSIVE.value, VeraCodexTrialConfidenceLevel.UNKNOWN.value)
        )
        for item in items
    )
    sufficient = bool(items) and required_present and not insufficient_required_evidence
    return build_vera_codex_evidence_bundle(
        evidence_items=items,
        required_evidence_present=required_present,
        sufficient_for_one_shot_trial=sufficient,
        sufficient_for_cold_evaluation_input=sufficient,
        bundle_summary="bounded v0.37 evidence bundle for deterministic one-shot metadata trial",
    )


def create_vera_codex_do_nothing_assessment(
    evidence_bundle: VeraCodexEvidenceBundle,
    repair_suggestion: SandboxRepairSuggestionEnvelope | None = None,
) -> VeraCodexDoNothingAssessment:
    evidence_refs = [item.evidence_item_id for item in evidence_bundle.evidence_items]
    preferred = not evidence_bundle.sufficient_for_one_shot_trial
    if repair_suggestion is not None:
        preferred = preferred or repair_suggestion.do_nothing_comparison.do_nothing_remains_valid
    return build_vera_codex_do_nothing_assessment(
        evidence_refs=evidence_refs,
        do_nothing_preferred=preferred,
        do_nothing_reason="do nothing is mandatory comparator and preferred when evidence is insufficient or risk remains high",
    )


def assess_vera_codex_repair_suggestion(
    evidence_bundle: VeraCodexEvidenceBundle,
    repair_suggestion: SandboxRepairSuggestionEnvelope | None = None,
) -> VeraCodexRepairSuggestionAssessment:
    evidence_refs = [item.evidence_item_id for item in evidence_bundle.evidence_items]
    supports_future = bool(
        repair_suggestion
        and repair_suggestion.eligible_for_future_repair_proposal
        and evidence_bundle.sufficient_for_one_shot_trial
    )
    confidence = _confidence_from_repair(repair_suggestion.confidence) if repair_suggestion else VeraCodexTrialConfidenceLevel.INCONCLUSIVE
    return build_vera_codex_repair_suggestion_assessment(
        repair_suggestion_id=repair_suggestion.repair_suggestion_id if repair_suggestion else None,
        supports_future_repair_proposal=supports_future,
        supports_repair_now=False,
        evidence_refs=evidence_refs,
        confidence=confidence,
        assessment_summary="repair suggestion assessed as future-gated metadata only",
    )


def create_vera_codex_decision_trace(
    evidence_bundle: VeraCodexEvidenceBundle,
    do_nothing: VeraCodexDoNothingAssessment,
    repair_assessment: VeraCodexRepairSuggestionAssessment,
    policy: VeraCodexTrialPolicy | None = None,
) -> VeraCodexDecisionTrace:
    policy = policy or default_vera_codex_trial_policy()
    risks = [
        VeraCodexTrialRiskKind.MODEL_PROVIDER_INVOCATION_RISK,
        VeraCodexTrialRiskKind.TOOL_EXECUTION_RISK,
        VeraCodexTrialRiskKind.CHAIN_OF_THOUGHT_LEAK_RISK,
    ]
    if not evidence_bundle.sufficient_for_one_shot_trial:
        risks.append(VeraCodexTrialRiskKind.INSUFFICIENT_TEST_EVIDENCE_RISK)
    steps = [
        build_vera_codex_decision_trace_step(
            decision_trace_step_id="vera_codex_trace_step:evidence:v0.37.6",
            step_index=0,
            step_summary="checked supplied evidence presence and sufficiency; no hidden reasoning stored",
            evidence_refs=[item.evidence_item_id for item in evidence_bundle.evidence_items],
            risk_kinds=risks,
            decision_kind=VeraCodexTrialDecisionKind.ALLOW_EVIDENCE_BUNDLE if evidence_bundle.required_evidence_present else VeraCodexTrialDecisionKind.REQUIRE_REVIEW,
        ),
        build_vera_codex_decision_trace_step(
            decision_trace_step_id="vera_codex_trace_step:do_nothing:v0.37.6",
            step_index=1,
            step_summary="recorded do-nothing assessment as mandatory comparator",
            evidence_refs=do_nothing.evidence_refs,
            risk_kinds=[VeraCodexTrialRiskKind.DO_NOTHING_OMISSION_RISK],
            decision_kind=VeraCodexTrialDecisionKind.CHOOSE_DO_NOTHING if do_nothing.do_nothing_preferred else VeraCodexTrialDecisionKind.ALLOW_TASK_HANDLING_REPORT,
        ),
        build_vera_codex_decision_trace_step(
            decision_trace_step_id="vera_codex_trace_step:repair_review:v0.37.6",
            step_index=2,
            step_summary="reviewed repair suggestion as future-gated metadata; no repair allowed",
            evidence_refs=repair_assessment.evidence_refs,
            risk_kinds=[VeraCodexTrialRiskKind.REPAIR_EXECUTION_CONFUSION_RISK],
            decision_kind=VeraCodexTrialDecisionKind.CHOOSE_FUTURE_REPAIR_PROPOSAL_GATE if repair_assessment.supports_future_repair_proposal else VeraCodexTrialDecisionKind.CHOOSE_HUMAN_REVIEW,
            confidence=repair_assessment.confidence,
        ),
    ][:policy.max_decision_trace_steps]
    return build_vera_codex_decision_trace(trace_steps=steps)


def decide_vera_codex_trial_outcome(
    evidence_bundle: VeraCodexEvidenceBundle,
    do_nothing: VeraCodexDoNothingAssessment,
    repair_assessment: VeraCodexRepairSuggestionAssessment,
    result_envelope: SandboxTestResultEnvelope | None = None,
) -> tuple[VeraCodexTaskHandlingAssessment, VeraCodexTrialDecision, VeraCodexStopReason]:
    evidence_refs = [item.evidence_item_id for item in evidence_bundle.evidence_items]
    outcome_value = _enum_value(result_envelope.outcome_classification.outcome_kind) if result_envelope else None
    failed_or_inconclusive = outcome_value in (
        SandboxTestOutcomeKind.FAILED.value,
        SandboxTestOutcomeKind.FAILED_ASSERTION.value,
        SandboxTestOutcomeKind.IMPORT_ERROR.value,
        SandboxTestOutcomeKind.SYNTAX_ERROR.value,
        SandboxTestOutcomeKind.MISSING_DEPENDENCY.value,
        SandboxTestOutcomeKind.TIMEOUT.value,
        SandboxTestOutcomeKind.INCONCLUSIVE.value,
        SandboxTestOutcomeKind.SAFE_FAILED.value,
        SandboxTestOutcomeKind.UNKNOWN.value,
    )
    if not evidence_bundle.sufficient_for_one_shot_trial:
        outcome = VeraCodexTaskHandlingOutcomeKind.EVIDENCE_INSUFFICIENT
        decision = VeraCodexTrialDecisionKind.CHOOSE_HUMAN_REVIEW
        stop = VeraCodexStopReasonKind.BLOCKED_BY_INSUFFICIENT_EVIDENCE
        confidence = VeraCodexTrialConfidenceLevel.INCONCLUSIVE
    elif failed_or_inconclusive:
        outcome = VeraCodexTaskHandlingOutcomeKind.EVIDENCE_SUPPORTS_HUMAN_REVIEW
        decision = VeraCodexTrialDecisionKind.CHOOSE_HUMAN_REVIEW
        stop = VeraCodexStopReasonKind.BLOCKED_BY_FAILED_TEST if outcome_value != SandboxTestOutcomeKind.INCONCLUSIVE.value else VeraCodexStopReasonKind.BLOCKED_BY_INCONCLUSIVE_RESULT
        confidence = VeraCodexTrialConfidenceLevel.MEDIUM
    elif repair_assessment.supports_future_repair_proposal:
        outcome = VeraCodexTaskHandlingOutcomeKind.EVIDENCE_SUPPORTS_FUTURE_REPAIR_PROPOSAL_GATE
        decision = VeraCodexTrialDecisionKind.CHOOSE_FUTURE_REPAIR_PROPOSAL_GATE
        stop = VeraCodexStopReasonKind.FUTURE_GATED
        confidence = repair_assessment.confidence
    else:
        outcome = VeraCodexTaskHandlingOutcomeKind.EVIDENCE_SUPPORTS_CONTINUE_TO_COLD_EVALUATION
        decision = VeraCodexTrialDecisionKind.ALLOW_FUTURE_COLD_EVALUATION_INPUT
        stop = VeraCodexStopReasonKind.COMPLETED_ONE_SHOT_TRIAL
        confidence = VeraCodexTrialConfidenceLevel.MEDIUM
    handling = build_vera_codex_task_handling_assessment(
        outcome_kind=outcome,
        evidence_bundle_id=evidence_bundle.evidence_bundle_id,
        do_nothing_assessment=do_nothing,
        repair_suggestion_assessment=repair_assessment,
        confidence=confidence,
        passed_as_success=False,
        assessment_summary="trial outcome is metadata only and not production success",
    )
    trial_decision = build_vera_codex_trial_decision(
        decision_kind=decision,
        evidence_refs=evidence_refs,
        confidence=confidence,
        decision_summary=f"{decision.value}; metadata only",
        rationale_summary="decision derived from supplied evidence sufficiency, do-nothing comparator, and repair suggestion metadata",
    )
    stop_reason = build_vera_codex_stop_reason(
        stop_reason_kind=stop,
        stop_summary=f"{stop.value}; mandatory human handoff follows",
    )
    return handling, trial_decision, stop_reason


def create_vera_codex_handoff_memo(
    trial_decision: VeraCodexTrialDecision,
    stop_reason: VeraCodexStopReason,
    evidence_refs: list[str],
) -> VeraCodexHandoffMemo:
    decision = _enum_value(trial_decision.decision_kind)
    if decision == VeraCodexTrialDecisionKind.ALLOW_FUTURE_COLD_EVALUATION_INPUT.value:
        kind = VeraCodexHandoffKind.COLD_EVALUATION_HANDOFF
    elif decision == VeraCodexTrialDecisionKind.CHOOSE_FUTURE_REPAIR_PROPOSAL_GATE.value:
        kind = VeraCodexHandoffKind.FUTURE_REPAIR_PROPOSAL_HANDOFF
    elif decision == VeraCodexTrialDecisionKind.CHOOSE_DO_NOTHING.value:
        kind = VeraCodexHandoffKind.DO_NOTHING_HANDOFF
    elif decision in (VeraCodexTrialDecisionKind.CHOOSE_BLOCK.value, VeraCodexTrialDecisionKind.BLOCK.value):
        kind = VeraCodexHandoffKind.BLOCKED_HANDOFF
    else:
        kind = VeraCodexHandoffKind.HUMAN_REVIEW_HANDOFF
    return build_vera_codex_handoff_memo(
        handoff_kind=kind,
        key_evidence_refs=evidence_refs,
        ready_for_cold_evaluation_input=decision == VeraCodexTrialDecisionKind.ALLOW_FUTURE_COLD_EVALUATION_INPUT.value,
        recommended_human_action=f"review {decision} after {stop_reason.stop_reason_kind}; no action executes automatically",
    )


def _create_safety_report(
    policy: VeraCodexTrialPolicy,
    evidence_bundle: VeraCodexEvidenceBundle,
) -> VeraCodexTrialSafetyReport:
    findings: list[VeraCodexTrialSafetyFinding] = []
    if not evidence_bundle.sufficient_for_one_shot_trial:
        findings.append(build_vera_codex_trial_safety_finding(
            safety_finding_id="vera_codex_safety_finding:evidence:v0.37.6",
            check_kind=VeraCodexSafetyCheckKind.EVIDENCE_REQUIRED_CHECK,
            severity="high",
            finding_summary="required evidence is missing or insufficient; review required",
            blocked=True,
            requires_review=True,
        ))
    passed = list(policy.required_safety_checks)
    failed: list[VeraCodexSafetyCheckKind | str] = []
    if findings:
        failed.append(VeraCodexSafetyCheckKind.EVIDENCE_REQUIRED_CHECK)
    return build_vera_codex_trial_safety_report(
        safety_findings=findings,
        required_checks=list(policy.required_safety_checks),
        passed_checks=passed,
        failed_checks=failed,
        blocked=any(f.blocked for f in findings),
        requires_review=any(f.requires_review for f in findings),
    )


def run_vera_codex_one_shot_trial(
    repair_suggestion: SandboxRepairSuggestionEnvelope | None = None,
    feedback_report: SandboxTestFeedbackReport | None = None,
    result_envelope: SandboxTestResultEnvelope | None = None,
    policy: VeraCodexTrialPolicy | None = None,
) -> VeraCodexOneShotTrialPacket:
    policy = policy or default_vera_codex_trial_policy()
    if repair_suggestion is not None:
        trial_input = build_vera_codex_trial_input_from_repair_suggestion(repair_suggestion)
    else:
        trial_input = build_vera_codex_trial_input(
            task_summary="one-shot Vera-Codex metadata trial with missing repair suggestion recorded",
            source_refs=[],
            metadata={"repair_suggestion_metadata_missing": True},
        )
    evidence_bundle = build_vera_codex_evidence_bundle_from_v037_artifacts(repair_suggestion, feedback_report, result_envelope, policy)
    do_nothing = create_vera_codex_do_nothing_assessment(evidence_bundle, repair_suggestion)
    repair_assessment = assess_vera_codex_repair_suggestion(evidence_bundle, repair_suggestion)
    decision_trace = create_vera_codex_decision_trace(evidence_bundle, do_nothing, repair_assessment, policy)
    handling, trial_decision, stop_reason = decide_vera_codex_trial_outcome(evidence_bundle, do_nothing, repair_assessment, result_envelope)
    handoff = create_vera_codex_handoff_memo(trial_decision, stop_reason, [item.evidence_item_id for item in evidence_bundle.evidence_items])
    safety = _create_safety_report(policy, evidence_bundle)
    status = VeraCodexTrialStatus.ONE_SHOT_TRIAL_COMPLETED_WITH_WARNINGS if safety.requires_review else VeraCodexTrialStatus.ONE_SHOT_TRIAL_COMPLETED
    return build_vera_codex_one_shot_trial_packet(
        trial_input=trial_input,
        evidence_bundle=evidence_bundle,
        decision_trace=decision_trace,
        task_handling_assessment=handling,
        trial_decision=trial_decision,
        safety_report=safety,
        stop_reason=stop_reason,
        handoff_memo=handoff,
        source_refs=trial_input.source_refs,
        status=status,
        eligible_for_future_cold_evaluation=handoff.ready_for_cold_evaluation_input,
        metadata={
            "digestion_first_policy_applied": True,
            "dominion_runtime_blocked": True,
            "external_agent_execution_blocked": True,
            "infinite_agent_loop_blocked": True,
            "recursive_self_invocation_blocked": True,
            "automatic_repair_loop_blocked": True,
            "repair_execution_blocked": True,
            "model_provider_invocation_blocked": True,
            "tool_execution_blocked": True,
            "bounded_vera_codex_evaluation_only": True,
            "no_independent_autonomous_agent_runtime": True,
            "mandatory_human_handoff_after_evaluation": True,
        },
    )


def validate_vera_codex_one_shot_trial_packet(packet: VeraCodexOneShotTrialPacket) -> VeraCodexTrialValidationReport:
    findings: list[VeraCodexTrialValidationFinding] = []
    if packet.trial_count != 1 or packet.max_cycle_count != 1:
        findings.append(build_vera_codex_trial_validation_finding(
            risk_kind=VeraCodexTrialRiskKind.MULTI_CYCLE_LOOP_RISK,
            severity="blocked",
            message="trial_count and max_cycle_count must be exactly 1",
            blocks_trial=True,
        ))
    if packet.model_invocation_performed or packet.tool_execution_performed or packet.test_execution_performed or packet.repair_performed:
        findings.append(build_vera_codex_trial_validation_finding(
            risk_kind=VeraCodexTrialRiskKind.MODEL_PROVIDER_INVOCATION_RISK,
            severity="blocked",
            message="runtime execution is not allowed",
            blocks_trial=True,
        ))
    if packet.decision_trace.contains_chain_of_thought:
        findings.append(build_vera_codex_trial_validation_finding(
            risk_kind=VeraCodexTrialRiskKind.CHAIN_OF_THOUGHT_LEAK_RISK,
            severity="blocked",
            message="decision trace must not contain chain-of-thought",
            blocks_trial=True,
        ))
    return build_vera_codex_trial_validation_report(
        trial_packet_id=packet.trial_packet_id,
        findings=findings,
        valid=not any(f.blocks_trial for f in findings),
    )


def vera_codex_trial_flags_preserve_no_autonomy(flags: VeraCodexTrialFlagSet) -> bool:
    return isinstance(flags, VeraCodexTrialFlagSet) and all(getattr(flags, name) is False for name in UNSAFE_VERA_CODEX_FLAG_NAMES)


def vera_codex_trial_policy_blocks_runtime_execution(policy: VeraCodexTrialPolicy) -> bool:
    return isinstance(policy, VeraCodexTrialPolicy) and all(getattr(policy, name) is False for name in UNSAFE_VERA_CODEX_POLICY_ALLOW_NAMES)


def vera_codex_trial_packet_is_single_shot(packet: VeraCodexOneShotTrialPacket) -> bool:
    return isinstance(packet, VeraCodexOneShotTrialPacket) and packet.trial_count == 1 and packet.max_cycle_count == 1 and not packet.automatic_retry_allowed and not packet.automatic_repair_allowed


def vera_codex_decision_trace_has_no_cot(trace: VeraCodexDecisionTrace) -> bool:
    return isinstance(trace, VeraCodexDecisionTrace) and trace.bounded_trace and not trace.contains_chain_of_thought and not trace.executed_actions and all(not step.contains_chain_of_thought and not step.executed_action for step in trace.trace_steps)


def vera_codex_trial_packet_is_not_production_certification(packet: VeraCodexOneShotTrialPacket) -> bool:
    return isinstance(packet, VeraCodexOneShotTrialPacket) and not packet.production_certified and not packet.ready_for_execution


def v0376_readiness_report_is_not_execution_ready(report: V0376ReadinessReport) -> bool:
    if not isinstance(report, V0376ReadinessReport):
        return False
    return all(
        getattr(report, name) is False
        for name in (
            "ready_for_execution",
            "ready_for_model_provider_invocation",
            "ready_for_tool_execution",
            "ready_for_test_execution",
            "ready_for_controlled_test_subprocess",
            "ready_for_shell_execution",
            "ready_for_subprocess_execution",
            "ready_for_command_execution",
            "ready_for_dependency_install",
            "ready_for_network_access",
            "ready_for_repair_patch_proposal",
            "ready_for_repair_diff_generation",
            "ready_for_code_hunk_generation",
            "ready_for_automatic_repair",
            "ready_for_repair_execution",
            "ready_for_multi_cycle_agentic_loop",
            "ready_for_cold_agent_performance_evaluation",
            "ready_for_external_agent_execution",
            "ready_for_dominion_runtime",
            "production_certified",
        )
    )
