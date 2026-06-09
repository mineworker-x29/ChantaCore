from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list
from .sandbox_test_result import (
    SandboxTestEvidenceSnippet,
    SandboxTestFailureClassKind,
    SandboxTestFailureClassification,
    SandboxTestOutcomeClassification,
    SandboxTestOutcomeKind,
    SandboxTestResultEnvelope,
)


V0374_VERSION = "v0.37.4"
V0374_RELEASE_NAME = "v0.37.4 Test Feedback Report & Failure Diagnosis"


UNSAFE_FEEDBACK_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_test_execution",
    "ready_for_controlled_test_subprocess",
    "ready_for_pytest_execution",
    "ready_for_npm_test_execution",
    "ready_for_unittest_execution",
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
    "ready_for_automatic_repair",
    "ready_for_repair_loop",
    "ready_for_retry_loop",
    "ready_for_multi_cycle_agentic_loop",
    "ready_for_vera_codex_trial_execution",
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

UNSAFE_FEEDBACK_POLICY_ALLOW_NAMES = (
    "allow_test_execution",
    "allow_subprocess",
    "allow_shell",
    "allow_dependency_install",
    "allow_network_access",
    "allow_repair_patch_proposal",
    "allow_automatic_repair",
    "allow_vera_codex_trial_execution",
    "allow_cold_performance_evaluation",
    "allow_external_agent_execution",
    "allow_dominion_runtime",
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
    if V0374_VERSION not in version:
        raise ValueError("version must include v0.37.4")


def _validate_false(name: str, value: bool) -> None:
    if value is not False:
        raise ValueError(f"{name} must remain False in v0.37.4")


def _validate_true(name: str, value: bool) -> None:
    if value is not True:
        raise ValueError(f"{name} must be True")


def _validate_non_negative(name: str, value: int) -> None:
    if value < 0:
        raise ValueError(f"{name} must be >= 0")


def _enum_value(value: Any) -> str:
    return value.value if isinstance(value, StrEnum) else str(value)


def _limit_text(text: str, limit: int) -> str:
    _validate_non_negative("limit", limit)
    return text[:limit]


class SandboxTestFeedbackMode(StrEnum):
    EVIDENCE_FEEDBACK_REPORT = "evidence_feedback_report"
    FAILURE_DIAGNOSIS_REPORT = "failure_diagnosis_report"
    ROOT_CAUSE_HYPOTHESIS_REPORT = "root_cause_hypothesis_report"
    DO_NOTHING_SIGNAL_REPORT = "do_nothing_signal_report"
    FUTURE_REPAIR_INPUT_REPORT = "future_repair_input_report"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class SandboxTestFeedbackSourceKind(StrEnum):
    V0373_TEST_RESULT_ENVELOPE = "v0373_test_result_envelope"
    V0373_OUTCOME_CLASSIFICATION = "v0373_outcome_classification"
    V0373_FAILURE_CLASSIFICATION = "v0373_failure_classification"
    V0373_EVIDENCE_SNIPPET = "v0373_evidence_snippet"
    V0372_SANDBOX_TEST_EXECUTION_RESULT = "v0372_sandbox_test_execution_result"
    V0371_TEST_INVOCATION_CONTRACT = "v0371_test_invocation_contract"
    V0369_PATCH_APPLY_SANDBOX_CONSOLIDATION = "v0369_patch_apply_sandbox_consolidation"
    MANUAL_OPERATOR_INPUT = "manual_operator_input"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class SandboxTestFeedbackStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    INPUT_VALIDATED = "input_validated"
    FEEDBACK_CREATED = "feedback_created"
    DIAGNOSIS_CREATED = "diagnosis_created"
    DIAGNOSIS_CREATED_WITH_WARNINGS = "diagnosis_created_with_warnings"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATED = "future_gated"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class SandboxTestFeedbackReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    FEEDBACK_CONTRACT_READY = "feedback_contract_ready"
    EVIDENCE_ASSESSMENT_READY = "evidence_assessment_ready"
    FAILURE_DIAGNOSIS_READY = "failure_diagnosis_ready"
    ROOT_CAUSE_HYPOTHESIS_READY = "root_cause_hypothesis_ready"
    DO_NOTHING_SIGNAL_READY = "do_nothing_signal_ready"
    FUTURE_REPAIR_INPUT_READY = "future_repair_input_ready"
    DESIGN_HANDOFF_READY_FOR_V0375 = "design_handoff_ready_for_v0375"
    DESIGN_HANDOFF_READY_FOR_V0376 = "design_handoff_ready_for_v0376"
    DESIGN_HANDOFF_READY_FOR_V0377 = "design_handoff_ready_for_v0377"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class SandboxTestFeedbackDecisionKind(StrEnum):
    ALLOW_FEEDBACK_REPORT = "allow_feedback_report"
    ALLOW_FAILURE_DIAGNOSIS = "allow_failure_diagnosis"
    ALLOW_ROOT_CAUSE_HYPOTHESIS = "allow_root_cause_hypothesis"
    ALLOW_SUGGESTED_NEXT_ACTION_METADATA = "allow_suggested_next_action_metadata"
    ALLOW_DO_NOTHING_SIGNAL = "allow_do_nothing_signal"
    ALLOW_FUTURE_REPAIR_SUGGESTION_INPUT = "allow_future_repair_suggestion_input"
    ALLOW_FUTURE_VERA_CODEX_TRIAL_INPUT = "allow_future_vera_codex_trial_input"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class SandboxTestFeedbackRiskKind(StrEnum):
    MISSING_RESULT_ENVELOPE_RISK = "missing_result_envelope_risk"
    INSUFFICIENT_EVIDENCE_RISK = "insufficient_evidence_risk"
    OVERCONFIDENT_DIAGNOSIS_RISK = "overconfident_diagnosis_risk"
    FAILED_TEST_REPORTED_AS_SUCCESS_RISK = "failed_test_reported_as_success_risk"
    INCONCLUSIVE_REPORTED_AS_SUCCESS_RISK = "inconclusive_reported_as_success_risk"
    ROOT_CAUSE_OVERCLAIM_RISK = "root_cause_overclaim_risk"
    REPAIR_PERMISSION_CONFUSION_RISK = "repair_permission_confusion_risk"
    RETRY_PERMISSION_CONFUSION_RISK = "retry_permission_confusion_risk"
    DEPENDENCY_INSTALL_CONFUSION_RISK = "dependency_install_confusion_risk"
    DO_NOTHING_OMISSION_RISK = "do_nothing_omission_risk"
    VERA_CODEX_OVERCLAIM_RISK = "vera_codex_overclaim_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    AUTOMATIC_REPAIR_RISK = "automatic_repair_risk"
    MULTI_CYCLE_LOOP_RISK = "multi_cycle_loop_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    UNKNOWN = "unknown"


class SandboxFailureDiagnosisKind(StrEnum):
    NO_FAILURE_DETECTED = "no_failure_detected"
    ASSERTION_FAILURE_DIAGNOSIS = "assertion_failure_diagnosis"
    IMPORT_FAILURE_DIAGNOSIS = "import_failure_diagnosis"
    SYNTAX_FAILURE_DIAGNOSIS = "syntax_failure_diagnosis"
    MISSING_DEPENDENCY_DIAGNOSIS = "missing_dependency_diagnosis"
    TIMEOUT_DIAGNOSIS = "timeout_diagnosis"
    COLLECTION_FAILURE_DIAGNOSIS = "collection_failure_diagnosis"
    RUNTIME_ERROR_DIAGNOSIS = "runtime_error_diagnosis"
    COMMAND_BLOCKED_DIAGNOSIS = "command_blocked_diagnosis"
    UNSAFE_OUTPUT_DIAGNOSIS = "unsafe_output_diagnosis"
    INCONCLUSIVE_DIAGNOSIS = "inconclusive_diagnosis"
    UNKNOWN_DIAGNOSIS = "unknown_diagnosis"


class SandboxRootCauseHypothesisKind(StrEnum):
    TEST_EXPECTATION_MISMATCH = "test_expectation_mismatch"
    IMPLEMENTATION_BUG_LIKELY = "implementation_bug_likely"
    IMPORT_PATH_ISSUE_LIKELY = "import_path_issue_likely"
    SYNTAX_ISSUE_LIKELY = "syntax_issue_likely"
    MISSING_DEPENDENCY_LIKELY = "missing_dependency_likely"
    STALE_TEST_OR_CONTEXT_LIKELY = "stale_test_or_context_likely"
    SANDBOX_ENVIRONMENT_ISSUE_LIKELY = "sandbox_environment_issue_likely"
    COMMAND_POLICY_BLOCK_LIKELY = "command_policy_block_likely"
    TIMEOUT_OR_PERFORMANCE_ISSUE_LIKELY = "timeout_or_performance_issue_likely"
    UNSAFE_OUTPUT_OR_SECRET_RISK_LIKELY = "unsafe_output_or_secret_risk_likely"
    NO_ROOT_CAUSE_IDENTIFIED = "no_root_cause_identified"
    INCONCLUSIVE = "inconclusive"
    UNKNOWN = "unknown"


class SandboxEvidenceStrength(StrEnum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    INSUFFICIENT = "insufficient"
    CONTRADICTORY = "contradictory"
    UNKNOWN = "unknown"


class SandboxFeedbackSeverity(StrEnum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class SandboxSuggestedNextActionKind(StrEnum):
    DO_NOTHING = "do_nothing"
    REQUEST_HUMAN_REVIEW = "request_human_review"
    CREATE_REPAIR_SUGGESTION_FUTURE_GATE = "create_repair_suggestion_future_gate"
    REVISE_TEST_OR_CONTEXT_FUTURE_GATE = "revise_test_or_context_future_gate"
    RERUN_TEST_FUTURE_GATE = "rerun_test_future_gate"
    INSPECT_MISSING_DEPENDENCY_WITHOUT_INSTALL = "inspect_missing_dependency_without_install"
    UPDATE_ALLOWLIST_FUTURE_GATE = "update_allowlist_future_gate"
    BLOCK_AND_INVESTIGATE = "block_and_investigate"
    PROCEED_TO_VERA_CODEX_TRIAL_FUTURE_GATE = "proceed_to_vera_codex_trial_future_gate"
    PROCEED_TO_COLD_EVALUATION_FUTURE_GATE = "proceed_to_cold_evaluation_future_gate"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class SandboxDoNothingSignalKind(StrEnum):
    DO_NOTHING_PREFERRED = "do_nothing_preferred"
    DO_NOTHING_COMPETITIVE = "do_nothing_competitive"
    DO_NOTHING_INFERIOR = "do_nothing_inferior"
    DO_NOTHING_REQUIRED_DUE_TO_INSUFFICIENT_EVIDENCE = "do_nothing_required_due_to_insufficient_evidence"
    DO_NOTHING_REQUIRED_DUE_TO_RISK_INCREASE = "do_nothing_required_due_to_risk_increase"
    DO_NOTHING_NOT_EVALUABLE_YET = "do_nothing_not_evaluable_yet"
    UNKNOWN = "unknown"


class SandboxFeedbackConfidenceLevel(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INCONCLUSIVE = "inconclusive"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class SandboxTestFeedbackFlagSet:
    flag_set_id: str
    version: str
    test_feedback_layer_constructed: bool
    feedback_report_available: bool
    failure_diagnosis_available: bool
    root_cause_hypothesis_available: bool
    evidence_strength_assessment_available: bool
    suggested_next_action_available: bool
    do_nothing_signal_available: bool
    ready_for_v0375_repair_suggestion_metadata: bool
    ready_for_v0376_vera_codex_one_shot_agent_trial: bool
    ready_for_v0377_cold_agent_performance_evaluation: bool
    ready_for_test_feedback_report: bool
    ready_for_failure_diagnosis_report: bool
    ready_for_root_cause_hypothesis_metadata: bool
    ready_for_evidence_strength_assessment: bool
    ready_for_suggested_next_action_metadata: bool
    ready_for_do_nothing_alternative_signal: bool
    ready_for_future_repair_suggestion_input: bool
    ready_for_future_vera_codex_trial_input: bool
    ready_for_future_cold_evaluation_input: bool
    ready_for_execution: bool
    ready_for_test_execution: bool
    ready_for_controlled_test_subprocess: bool
    ready_for_pytest_execution: bool
    ready_for_npm_test_execution: bool
    ready_for_unittest_execution: bool
    ready_for_shell_execution: bool
    ready_for_subprocess_execution: bool
    ready_for_command_execution: bool
    ready_for_dependency_install: bool
    ready_for_network_access: bool
    ready_for_live_workspace_write: bool
    ready_for_patch_application: bool
    ready_for_workspace_write: bool
    ready_for_code_edit: bool
    ready_for_apply_patch: bool
    ready_for_git_apply: bool
    ready_for_repair_patch_proposal: bool
    ready_for_automatic_repair: bool
    ready_for_repair_loop: bool
    ready_for_retry_loop: bool
    ready_for_multi_cycle_agentic_loop: bool
    ready_for_vera_codex_trial_execution: bool
    ready_for_cold_agent_performance_evaluation: bool
    ready_for_external_agent_execution: bool
    ready_for_claude_code_invocation: bool
    ready_for_codex_cli_invocation: bool
    ready_for_dominion_runtime: bool
    ready_for_infinite_agent_loop: bool
    ready_for_provider_invocation: bool
    ready_for_direct_network_access: bool
    ready_for_credential_access: bool
    ready_for_secret_read: bool
    ready_for_general_agent_execution: bool
    ready_for_autonomous_agent_runtime: bool
    ready_for_independent_agent_runtime: bool
    ready_for_general_tool_execution: bool
    ready_for_unquarantined_action_execution: bool
    ready_for_persistent_trace_write: bool
    ready_for_external_trace_sink: bool
    ready_for_ui_runtime: bool
    ready_for_external_control: bool
    ready_for_authority_grant: bool
    production_certified: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version(self.version)
        for name in UNSAFE_FEEDBACK_FLAG_NAMES:
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestFeedbackSourceRef:
    source_ref_id: str
    source_kind: SandboxTestFeedbackSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestFeedbackPolicy:
    feedback_policy_id: str
    version: str
    allowed_modes: list[SandboxTestFeedbackMode | str]
    max_observations: int
    max_hypotheses: int
    max_evidence_chars: int
    require_result_envelope: bool
    require_evidence_strength: bool
    require_confidence_level: bool
    require_do_nothing_signal: bool
    require_no_overclaim: bool
    allow_feedback_report: bool
    allow_failure_diagnosis: bool
    allow_root_cause_hypothesis: bool
    allow_suggested_next_action_metadata: bool
    allow_do_nothing_signal: bool
    allow_future_repair_suggestion_input: bool
    allow_future_vera_codex_trial_input: bool
    allow_test_execution: bool
    allow_subprocess: bool
    allow_shell: bool
    allow_dependency_install: bool
    allow_network_access: bool
    allow_repair_patch_proposal: bool
    allow_automatic_repair: bool
    allow_vera_codex_trial_execution: bool
    allow_cold_performance_evaluation: bool
    allow_external_agent_execution: bool
    allow_dominion_runtime: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("feedback_policy_id", self.feedback_policy_id)
        _validate_version(self.version)
        _validate_list("allowed_modes", self.allowed_modes)
        for name in ("max_observations", "max_hypotheses", "max_evidence_chars"):
            _validate_non_negative(name, getattr(self, name))
        for name in (
            "require_result_envelope",
            "require_evidence_strength",
            "require_confidence_level",
            "require_do_nothing_signal",
            "require_no_overclaim",
        ):
            _validate_true(name, getattr(self, name))
        for name in UNSAFE_FEEDBACK_POLICY_ALLOW_NAMES:
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestFeedbackInput:
    feedback_input_id: str
    version: str
    result_envelope_id: str | None
    outcome_classification_id: str | None
    failure_classification_id: str | None
    execution_result_id: str | None
    invocation_contract_id: str | None
    requested_mode: SandboxTestFeedbackMode | str
    source_refs: list[SandboxTestFeedbackSourceRef]
    prohibited_runtime_actions: list[str]
    task_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("feedback_input_id", self.feedback_input_id)
        _validate_version(self.version)
        _require_non_blank("task_summary", self.task_summary)
        _validate_list("source_refs", self.source_refs)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        required = {"test execution", "subprocess", "shell", "install", "network", "repair", "external agent", "Dominion", "evaluation execution"}
        if not required.issubset(set(self.prohibited_runtime_actions)):
            raise ValueError("prohibited_runtime_actions must include v0.37.4 unsafe actions")
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxFailureObservation:
    observation_id: str
    diagnosis_kind: SandboxFailureDiagnosisKind | str
    observation_summary: str
    evidence_refs: list[str]
    severity: SandboxFeedbackSeverity | str
    confidence: SandboxFeedbackConfidenceLevel | str
    blocked: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("observation_id", self.observation_id)
        _require_non_blank("observation_summary", self.observation_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxEvidenceAssessment:
    evidence_assessment_id: str
    evidence_strength: SandboxEvidenceStrength | str
    confidence: SandboxFeedbackConfidenceLevel | str
    evidence_summary: str
    supporting_evidence_refs: list[str]
    contradictory_evidence_refs: list[str]
    insufficient_evidence: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("evidence_assessment_id", self.evidence_assessment_id)
        _require_non_blank("evidence_summary", self.evidence_summary)
        _validate_string_list("supporting_evidence_refs", self.supporting_evidence_refs)
        _validate_string_list("contradictory_evidence_refs", self.contradictory_evidence_refs)
        if _enum_value(self.evidence_strength) in (SandboxEvidenceStrength.INSUFFICIENT.value, SandboxEvidenceStrength.CONTRADICTORY.value):
            if _enum_value(self.confidence) == SandboxFeedbackConfidenceLevel.HIGH.value:
                raise ValueError("insufficient or contradictory evidence cannot have high confidence")
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxRootCauseHypothesis:
    hypothesis_id: str
    hypothesis_kind: SandboxRootCauseHypothesisKind | str
    hypothesis_summary: str
    evidence_assessment: SandboxEvidenceAssessment
    confidence: SandboxFeedbackConfidenceLevel | str
    evidence_strength: SandboxEvidenceStrength | str
    proven: bool
    repair_allowed: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("hypothesis_id", self.hypothesis_id)
        _require_non_blank("hypothesis_summary", self.hypothesis_summary)
        _validate_false("repair_allowed", self.repair_allowed)
        if self.proven and _enum_value(self.evidence_strength) not in (SandboxEvidenceStrength.STRONG.value,):
            raise ValueError("proven hypothesis requires direct strong evidence")
        if _enum_value(self.evidence_strength) in (SandboxEvidenceStrength.WEAK.value, SandboxEvidenceStrength.INSUFFICIENT.value, SandboxEvidenceStrength.CONTRADICTORY.value):
            if _enum_value(self.confidence) == SandboxFeedbackConfidenceLevel.HIGH.value:
                raise ValueError("weak or insufficient evidence cannot have high confidence")
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxSuggestedNextAction:
    suggested_action_id: str
    action_kind: SandboxSuggestedNextActionKind | str
    action_summary: str
    rationale: str
    evidence_refs: list[str]
    future_gated: bool
    executes_now: bool
    repair_allowed: bool
    test_rerun_allowed: bool
    dependency_install_allowed: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("suggested_action_id", self.suggested_action_id)
        _require_non_blank("action_summary", self.action_summary)
        _require_non_blank("rationale", self.rationale)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false("executes_now", self.executes_now)
        _validate_false("repair_allowed", self.repair_allowed)
        _validate_false("test_rerun_allowed", self.test_rerun_allowed)
        _validate_false("dependency_install_allowed", self.dependency_install_allowed)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxDoNothingAlternativeSignal:
    do_nothing_signal_id: str
    signal_kind: SandboxDoNothingSignalKind | str
    signal_summary: str
    evidence_refs: list[str]
    risk_delta_summary: str
    test_delta_summary: str
    do_nothing_remains_valid: bool
    scoring_performed: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("do_nothing_signal_id", self.do_nothing_signal_id)
        _require_non_blank("signal_summary", self.signal_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _require_non_blank("risk_delta_summary", self.risk_delta_summary)
        _require_non_blank("test_delta_summary", self.test_delta_summary)
        _validate_false("scoring_performed", self.scoring_performed)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxFailureDiagnosisReport:
    diagnosis_report_id: str
    version: str
    feedback_input_id: str
    observations: list[SandboxFailureObservation]
    hypotheses: list[SandboxRootCauseHypothesis]
    evidence_assessments: list[SandboxEvidenceAssessment]
    diagnosis_summary: str
    primary_hypothesis_id: str | None
    inconclusive: bool
    repair_allowed: bool
    retry_allowed: bool
    dependency_install_allowed: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("diagnosis_report_id", self.diagnosis_report_id)
        _validate_version(self.version)
        _require_non_blank("feedback_input_id", self.feedback_input_id)
        _require_non_blank("diagnosis_summary", self.diagnosis_summary)
        _validate_list("observations", self.observations)
        _validate_list("hypotheses", self.hypotheses)
        _validate_list("evidence_assessments", self.evidence_assessments)
        _validate_false("repair_allowed", self.repair_allowed)
        _validate_false("retry_allowed", self.retry_allowed)
        _validate_false("dependency_install_allowed", self.dependency_install_allowed)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestFeedbackReport:
    feedback_report_id: str
    version: str
    feedback_input_id: str
    status: SandboxTestFeedbackStatus | str
    readiness_level: SandboxTestFeedbackReadinessLevel | str
    diagnosis_report: SandboxFailureDiagnosisReport
    suggested_actions: list[SandboxSuggestedNextAction]
    do_nothing_signal: SandboxDoNothingAlternativeSignal
    source_refs: list[SandboxTestFeedbackSourceRef]
    summary: str
    eligible_for_future_repair_suggestion: bool
    eligible_for_future_vera_codex_trial: bool
    eligible_for_future_cold_evaluation: bool
    test_execution_performed: bool
    subprocess_executed_by_v0374: bool
    repair_performed: bool
    repair_allowed: bool
    retry_allowed: bool
    dependency_install_allowed: bool
    production_certified: bool
    ready_for_execution: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("feedback_report_id", self.feedback_report_id)
        _validate_version(self.version)
        _require_non_blank("feedback_input_id", self.feedback_input_id)
        _require_non_blank("summary", self.summary)
        _validate_list("suggested_actions", self.suggested_actions)
        _validate_list("source_refs", self.source_refs)
        for name in (
            "test_execution_performed",
            "subprocess_executed_by_v0374",
            "repair_performed",
            "repair_allowed",
            "retry_allowed",
            "dependency_install_allowed",
            "production_certified",
            "ready_for_execution",
        ):
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxFeedbackDecision:
    decision_id: str
    feedback_input_id: str
    decision_kind: SandboxTestFeedbackDecisionKind | str
    status: SandboxTestFeedbackStatus | str
    risk_kinds: list[SandboxTestFeedbackRiskKind | str]
    decision_summary: str
    feedback_report_allowed: bool
    failure_diagnosis_allowed: bool
    root_cause_hypothesis_allowed: bool
    suggested_action_metadata_allowed: bool
    do_nothing_signal_allowed: bool
    future_repair_suggestion_input_allowed: bool
    future_vera_codex_trial_input_allowed: bool
    test_execution_allowed: bool
    subprocess_allowed: bool
    shell_allowed: bool
    dependency_install_allowed: bool
    network_allowed: bool
    repair_patch_proposal_allowed: bool
    automatic_repair_allowed: bool
    vera_codex_trial_execution_allowed: bool
    cold_evaluation_execution_allowed: bool
    external_agent_allowed: bool
    dominion_runtime_allowed: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("decision_id", self.decision_id)
        _require_non_blank("feedback_input_id", self.feedback_input_id)
        _require_non_blank("decision_summary", self.decision_summary)
        _validate_list("risk_kinds", self.risk_kinds)
        for name in (
            "test_execution_allowed",
            "subprocess_allowed",
            "shell_allowed",
            "dependency_install_allowed",
            "network_allowed",
            "repair_patch_proposal_allowed",
            "automatic_repair_allowed",
            "vera_codex_trial_execution_allowed",
            "cold_evaluation_execution_allowed",
            "external_agent_allowed",
            "dominion_runtime_allowed",
        ):
            _validate_false(name, getattr(self, name))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxFeedbackValidationFinding:
    finding_id: str
    risk_kind: SandboxTestFeedbackRiskKind | str
    severity: SandboxFeedbackSeverity | str
    message: str
    blocks_feedback: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("message", self.message)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxFeedbackValidationReport:
    validation_report_id: str
    version: str
    feedback_report_id: str
    findings: list[SandboxFeedbackValidationFinding]
    evidence_strength_confirmed: bool
    no_overclaim_confirmed: bool
    no_production_certification_confirmed: bool
    no_repair_confirmed: bool
    summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version(self.version)
        _require_non_blank("feedback_report_id", self.feedback_report_id)
        _require_non_blank("summary", self.summary)
        _validate_list("findings", self.findings)
        _validate_true("evidence_strength_confirmed", self.evidence_strength_confirmed)
        _validate_true("no_overclaim_confirmed", self.no_overclaim_confirmed)
        _validate_true("no_production_certification_confirmed", self.no_production_certification_confirmed)
        _validate_true("no_repair_confirmed", self.no_repair_confirmed)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxFeedbackRunPreview:
    run_preview_id: str
    version: str
    feedback_input_id: str
    preview_summary: str
    ready_for_feedback_report: bool
    ready_for_repair_patch_proposal: bool
    ready_for_test_execution: bool
    ready_for_vera_codex_trial_execution: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        _validate_version(self.version)
        _require_non_blank("feedback_input_id", self.feedback_input_id)
        _require_non_blank("preview_summary", self.preview_summary)
        _validate_false("ready_for_repair_patch_proposal", self.ready_for_repair_patch_proposal)
        _validate_false("ready_for_test_execution", self.ready_for_test_execution)
        _validate_false("ready_for_vera_codex_trial_execution", self.ready_for_vera_codex_trial_execution)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxFeedbackNoRepairGuarantee:
    guarantee_id: str
    version: str
    no_test_execution: bool
    no_controlled_test_subprocess: bool
    no_pytest_execution: bool
    no_unittest_execution: bool
    no_npm_test_execution: bool
    no_shell_execution: bool
    no_subprocess_execution: bool
    no_command_execution: bool
    no_dependency_install: bool
    no_network_access: bool
    no_live_workspace_write: bool
    no_patch_application: bool
    no_repair_patch_proposal: bool
    no_automatic_repair: bool
    no_repair_loop: bool
    no_retry_loop: bool
    no_multi_cycle_loop: bool
    no_vera_codex_trial_execution: bool
    no_cold_performance_evaluation_execution: bool
    no_provider_invocation: bool
    no_external_agent_execution: bool
    no_dominion_runtime: bool
    no_persistent_trace_write: bool
    no_ui_runtime: bool
    no_authority_grant: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version(self.version)
        _require_non_blank("summary", self.summary)
        for name in self.__dataclass_fields__:
            if name.startswith("no_"):
                _validate_true(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class V0374ReadinessReport:
    readiness_report_id: str
    version: str
    readiness_level: SandboxTestFeedbackReadinessLevel | str
    status: SandboxTestFeedbackStatus | str
    summary: str
    ready_for_v0375_repair_suggestion_metadata: bool
    ready_for_v0376_vera_codex_one_shot_agent_trial: bool
    ready_for_v0377_cold_agent_performance_evaluation: bool
    ready_for_test_feedback_report: bool
    ready_for_failure_diagnosis_report: bool
    ready_for_root_cause_hypothesis_metadata: bool
    ready_for_evidence_strength_assessment: bool
    ready_for_suggested_next_action_metadata: bool
    ready_for_do_nothing_alternative_signal: bool
    ready_for_future_repair_suggestion_input: bool
    ready_for_future_vera_codex_trial_input: bool
    ready_for_future_cold_evaluation_input: bool
    ready_for_execution: bool
    ready_for_test_execution: bool
    ready_for_controlled_test_subprocess: bool
    ready_for_shell_execution: bool
    ready_for_subprocess_execution: bool
    ready_for_command_execution: bool
    ready_for_dependency_install: bool
    ready_for_network_access: bool
    ready_for_repair_patch_proposal: bool
    ready_for_automatic_repair: bool
    ready_for_multi_cycle_agentic_loop: bool
    ready_for_vera_codex_trial_execution: bool
    ready_for_cold_agent_performance_evaluation: bool
    ready_for_external_agent_execution: bool
    ready_for_dominion_runtime: bool
    production_certified: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("readiness_report_id", self.readiness_report_id)
        _validate_version(self.version)
        _require_non_blank("summary", self.summary)
        for name in (
            "ready_for_execution",
            "ready_for_test_execution",
            "ready_for_controlled_test_subprocess",
            "ready_for_shell_execution",
            "ready_for_subprocess_execution",
            "ready_for_command_execution",
            "ready_for_dependency_install",
            "ready_for_network_access",
            "ready_for_repair_patch_proposal",
            "ready_for_automatic_repair",
            "ready_for_multi_cycle_agentic_loop",
            "ready_for_vera_codex_trial_execution",
            "ready_for_cold_agent_performance_evaluation",
            "ready_for_external_agent_execution",
            "ready_for_dominion_runtime",
            "production_certified",
        ):
            _validate_false(name, getattr(self, name))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


def build_sandbox_test_feedback_flags(**kwargs: Any) -> SandboxTestFeedbackFlagSet:
    return SandboxTestFeedbackFlagSet(
        flag_set_id=kwargs.pop("flag_set_id", "sandbox_test_feedback_flags:v0.37.4"),
        version=kwargs.pop("version", V0374_VERSION),
        test_feedback_layer_constructed=kwargs.pop("test_feedback_layer_constructed", True),
        feedback_report_available=kwargs.pop("feedback_report_available", True),
        failure_diagnosis_available=kwargs.pop("failure_diagnosis_available", True),
        root_cause_hypothesis_available=kwargs.pop("root_cause_hypothesis_available", True),
        evidence_strength_assessment_available=kwargs.pop("evidence_strength_assessment_available", True),
        suggested_next_action_available=kwargs.pop("suggested_next_action_available", True),
        do_nothing_signal_available=kwargs.pop("do_nothing_signal_available", True),
        ready_for_v0375_repair_suggestion_metadata=kwargs.pop("ready_for_v0375_repair_suggestion_metadata", True),
        ready_for_v0376_vera_codex_one_shot_agent_trial=kwargs.pop("ready_for_v0376_vera_codex_one_shot_agent_trial", True),
        ready_for_v0377_cold_agent_performance_evaluation=kwargs.pop("ready_for_v0377_cold_agent_performance_evaluation", True),
        ready_for_test_feedback_report=kwargs.pop("ready_for_test_feedback_report", True),
        ready_for_failure_diagnosis_report=kwargs.pop("ready_for_failure_diagnosis_report", True),
        ready_for_root_cause_hypothesis_metadata=kwargs.pop("ready_for_root_cause_hypothesis_metadata", True),
        ready_for_evidence_strength_assessment=kwargs.pop("ready_for_evidence_strength_assessment", True),
        ready_for_suggested_next_action_metadata=kwargs.pop("ready_for_suggested_next_action_metadata", True),
        ready_for_do_nothing_alternative_signal=kwargs.pop("ready_for_do_nothing_alternative_signal", True),
        ready_for_future_repair_suggestion_input=kwargs.pop("ready_for_future_repair_suggestion_input", True),
        ready_for_future_vera_codex_trial_input=kwargs.pop("ready_for_future_vera_codex_trial_input", True),
        ready_for_future_cold_evaluation_input=kwargs.pop("ready_for_future_cold_evaluation_input", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_FEEDBACK_FLAG_NAMES},
    )


def build_sandbox_test_feedback_source_ref(**kwargs: Any) -> SandboxTestFeedbackSourceRef:
    return SandboxTestFeedbackSourceRef(
        source_ref_id=kwargs.pop("source_ref_id", "sandbox_test_feedback_source:v0.37.4"),
        source_kind=kwargs.pop("source_kind", SandboxTestFeedbackSourceKind.V0373_TEST_RESULT_ENVELOPE),
        source_id=kwargs.pop("source_id", "sandbox_test_result_envelope:v0.37.3"),
        source_summary=kwargs.pop("source_summary", "supplied result envelope metadata"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.3 result envelope"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_feedback_policy(**kwargs: Any) -> SandboxTestFeedbackPolicy:
    return SandboxTestFeedbackPolicy(
        feedback_policy_id=kwargs.pop("feedback_policy_id", "sandbox_test_feedback_policy:v0.37.4"),
        version=kwargs.pop("version", V0374_VERSION),
        allowed_modes=kwargs.pop("allowed_modes", [
            SandboxTestFeedbackMode.EVIDENCE_FEEDBACK_REPORT,
            SandboxTestFeedbackMode.FAILURE_DIAGNOSIS_REPORT,
            SandboxTestFeedbackMode.ROOT_CAUSE_HYPOTHESIS_REPORT,
            SandboxTestFeedbackMode.DO_NOTHING_SIGNAL_REPORT,
            SandboxTestFeedbackMode.FUTURE_REPAIR_INPUT_REPORT,
        ]),
        max_observations=kwargs.pop("max_observations", 20),
        max_hypotheses=kwargs.pop("max_hypotheses", 10),
        max_evidence_chars=kwargs.pop("max_evidence_chars", 1000),
        require_result_envelope=kwargs.pop("require_result_envelope", True),
        require_evidence_strength=kwargs.pop("require_evidence_strength", True),
        require_confidence_level=kwargs.pop("require_confidence_level", True),
        require_do_nothing_signal=kwargs.pop("require_do_nothing_signal", True),
        require_no_overclaim=kwargs.pop("require_no_overclaim", True),
        allow_feedback_report=kwargs.pop("allow_feedback_report", True),
        allow_failure_diagnosis=kwargs.pop("allow_failure_diagnosis", True),
        allow_root_cause_hypothesis=kwargs.pop("allow_root_cause_hypothesis", True),
        allow_suggested_next_action_metadata=kwargs.pop("allow_suggested_next_action_metadata", True),
        allow_do_nothing_signal=kwargs.pop("allow_do_nothing_signal", True),
        allow_future_repair_suggestion_input=kwargs.pop("allow_future_repair_suggestion_input", True),
        allow_future_vera_codex_trial_input=kwargs.pop("allow_future_vera_codex_trial_input", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_FEEDBACK_POLICY_ALLOW_NAMES},
    )


def build_sandbox_test_feedback_input(**kwargs: Any) -> SandboxTestFeedbackInput:
    return SandboxTestFeedbackInput(
        feedback_input_id=kwargs.pop("feedback_input_id", "sandbox_test_feedback_input:v0.37.4"),
        version=kwargs.pop("version", V0374_VERSION),
        result_envelope_id=kwargs.pop("result_envelope_id", "sandbox_test_result_envelope:v0.37.3"),
        outcome_classification_id=kwargs.pop("outcome_classification_id", "sandbox_test_outcome_classification:v0.37.3"),
        failure_classification_id=kwargs.pop("failure_classification_id", "sandbox_test_failure_classification:v0.37.3"),
        execution_result_id=kwargs.pop("execution_result_id", None),
        invocation_contract_id=kwargs.pop("invocation_contract_id", None),
        requested_mode=kwargs.pop("requested_mode", SandboxTestFeedbackMode.FAILURE_DIAGNOSIS_REPORT),
        source_refs=kwargs.pop("source_refs", [build_sandbox_test_feedback_source_ref()]),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", ["test execution", "subprocess", "shell", "install", "network", "repair", "external agent", "Dominion", "evaluation execution"]),
        task_summary=kwargs.pop("task_summary", "feedback request from supplied result metadata"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_failure_observation(**kwargs: Any) -> SandboxFailureObservation:
    return SandboxFailureObservation(
        observation_id=kwargs.pop("observation_id", "sandbox_failure_observation:v0.37.4"),
        diagnosis_kind=kwargs.pop("diagnosis_kind", SandboxFailureDiagnosisKind.INCONCLUSIVE_DIAGNOSIS),
        observation_summary=kwargs.pop("observation_summary", "failure observation metadata"),
        evidence_refs=kwargs.pop("evidence_refs", []),
        severity=kwargs.pop("severity", SandboxFeedbackSeverity.INFO),
        confidence=kwargs.pop("confidence", SandboxFeedbackConfidenceLevel.INCONCLUSIVE),
        blocked=kwargs.pop("blocked", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_evidence_assessment(**kwargs: Any) -> SandboxEvidenceAssessment:
    return SandboxEvidenceAssessment(
        evidence_assessment_id=kwargs.pop("evidence_assessment_id", "sandbox_evidence_assessment:v0.37.4"),
        evidence_strength=kwargs.pop("evidence_strength", SandboxEvidenceStrength.INSUFFICIENT),
        confidence=kwargs.pop("confidence", SandboxFeedbackConfidenceLevel.INCONCLUSIVE),
        evidence_summary=kwargs.pop("evidence_summary", "evidence strength assessment"),
        supporting_evidence_refs=kwargs.pop("supporting_evidence_refs", []),
        contradictory_evidence_refs=kwargs.pop("contradictory_evidence_refs", []),
        insufficient_evidence=kwargs.pop("insufficient_evidence", True),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_root_cause_hypothesis(**kwargs: Any) -> SandboxRootCauseHypothesis:
    assessment = kwargs.pop("evidence_assessment", build_sandbox_evidence_assessment())
    return SandboxRootCauseHypothesis(
        hypothesis_id=kwargs.pop("hypothesis_id", "sandbox_root_cause_hypothesis:v0.37.4"),
        hypothesis_kind=kwargs.pop("hypothesis_kind", SandboxRootCauseHypothesisKind.INCONCLUSIVE),
        hypothesis_summary=kwargs.pop("hypothesis_summary", "root-cause hypothesis metadata; not proof"),
        evidence_assessment=assessment,
        confidence=kwargs.pop("confidence", assessment.confidence),
        evidence_strength=kwargs.pop("evidence_strength", assessment.evidence_strength),
        proven=kwargs.pop("proven", False),
        repair_allowed=kwargs.pop("repair_allowed", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_suggested_next_action(**kwargs: Any) -> SandboxSuggestedNextAction:
    return SandboxSuggestedNextAction(
        suggested_action_id=kwargs.pop("suggested_action_id", "sandbox_suggested_next_action:v0.37.4"),
        action_kind=kwargs.pop("action_kind", SandboxSuggestedNextActionKind.REQUEST_HUMAN_REVIEW),
        action_summary=kwargs.pop("action_summary", "suggested next action metadata only"),
        rationale=kwargs.pop("rationale", "action remains non-executing and future-gated if needed"),
        evidence_refs=kwargs.pop("evidence_refs", []),
        future_gated=kwargs.pop("future_gated", True),
        executes_now=kwargs.pop("executes_now", False),
        repair_allowed=kwargs.pop("repair_allowed", False),
        test_rerun_allowed=kwargs.pop("test_rerun_allowed", False),
        dependency_install_allowed=kwargs.pop("dependency_install_allowed", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_do_nothing_alternative_signal(**kwargs: Any) -> SandboxDoNothingAlternativeSignal:
    return SandboxDoNothingAlternativeSignal(
        do_nothing_signal_id=kwargs.pop("do_nothing_signal_id", "sandbox_do_nothing_signal:v0.37.4"),
        signal_kind=kwargs.pop("signal_kind", SandboxDoNothingSignalKind.DO_NOTHING_NOT_EVALUABLE_YET),
        signal_summary=kwargs.pop("signal_summary", "do-nothing alternative remains represented"),
        evidence_refs=kwargs.pop("evidence_refs", []),
        risk_delta_summary=kwargs.pop("risk_delta_summary", "risk delta is not scored in v0.37.4"),
        test_delta_summary=kwargs.pop("test_delta_summary", "test delta is not scored in v0.37.4"),
        do_nothing_remains_valid=kwargs.pop("do_nothing_remains_valid", True),
        scoring_performed=kwargs.pop("scoring_performed", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_failure_diagnosis_report(**kwargs: Any) -> SandboxFailureDiagnosisReport:
    return SandboxFailureDiagnosisReport(
        diagnosis_report_id=kwargs.pop("diagnosis_report_id", "sandbox_failure_diagnosis_report:v0.37.4"),
        version=kwargs.pop("version", V0374_VERSION),
        feedback_input_id=kwargs.pop("feedback_input_id", "sandbox_test_feedback_input:v0.37.4"),
        observations=kwargs.pop("observations", []),
        hypotheses=kwargs.pop("hypotheses", []),
        evidence_assessments=kwargs.pop("evidence_assessments", []),
        diagnosis_summary=kwargs.pop("diagnosis_summary", "failure diagnosis metadata only"),
        primary_hypothesis_id=kwargs.pop("primary_hypothesis_id", None),
        inconclusive=kwargs.pop("inconclusive", True),
        repair_allowed=kwargs.pop("repair_allowed", False),
        retry_allowed=kwargs.pop("retry_allowed", False),
        dependency_install_allowed=kwargs.pop("dependency_install_allowed", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_feedback_report(**kwargs: Any) -> SandboxTestFeedbackReport:
    diagnosis = kwargs.pop("diagnosis_report", build_sandbox_failure_diagnosis_report())
    return SandboxTestFeedbackReport(
        feedback_report_id=kwargs.pop("feedback_report_id", "sandbox_test_feedback_report:v0.37.4"),
        version=kwargs.pop("version", V0374_VERSION),
        feedback_input_id=kwargs.pop("feedback_input_id", diagnosis.feedback_input_id),
        status=kwargs.pop("status", SandboxTestFeedbackStatus.FEEDBACK_CREATED),
        readiness_level=kwargs.pop("readiness_level", SandboxTestFeedbackReadinessLevel.FUTURE_REPAIR_INPUT_READY),
        diagnosis_report=diagnosis,
        suggested_actions=kwargs.pop("suggested_actions", []),
        do_nothing_signal=kwargs.pop("do_nothing_signal", build_sandbox_do_nothing_alternative_signal()),
        source_refs=kwargs.pop("source_refs", [build_sandbox_test_feedback_source_ref()]),
        summary=kwargs.pop("summary", "feedback report metadata only"),
        eligible_for_future_repair_suggestion=kwargs.pop("eligible_for_future_repair_suggestion", True),
        eligible_for_future_vera_codex_trial=kwargs.pop("eligible_for_future_vera_codex_trial", True),
        eligible_for_future_cold_evaluation=kwargs.pop("eligible_for_future_cold_evaluation", True),
        test_execution_performed=kwargs.pop("test_execution_performed", False),
        subprocess_executed_by_v0374=kwargs.pop("subprocess_executed_by_v0374", False),
        repair_performed=kwargs.pop("repair_performed", False),
        repair_allowed=kwargs.pop("repair_allowed", False),
        retry_allowed=kwargs.pop("retry_allowed", False),
        dependency_install_allowed=kwargs.pop("dependency_install_allowed", False),
        production_certified=kwargs.pop("production_certified", False),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_feedback_decision(**kwargs: Any) -> SandboxFeedbackDecision:
    return SandboxFeedbackDecision(
        decision_id=kwargs.pop("decision_id", "sandbox_feedback_decision:v0.37.4"),
        feedback_input_id=kwargs.pop("feedback_input_id", "sandbox_test_feedback_input:v0.37.4"),
        decision_kind=kwargs.pop("decision_kind", SandboxTestFeedbackDecisionKind.ALLOW_FEEDBACK_REPORT),
        status=kwargs.pop("status", SandboxTestFeedbackStatus.FEEDBACK_CREATED),
        risk_kinds=kwargs.pop("risk_kinds", [SandboxTestFeedbackRiskKind.ROOT_CAUSE_OVERCLAIM_RISK]),
        decision_summary=kwargs.pop("decision_summary", "feedback metadata allowed; execution remains blocked"),
        feedback_report_allowed=kwargs.pop("feedback_report_allowed", True),
        failure_diagnosis_allowed=kwargs.pop("failure_diagnosis_allowed", True),
        root_cause_hypothesis_allowed=kwargs.pop("root_cause_hypothesis_allowed", True),
        suggested_action_metadata_allowed=kwargs.pop("suggested_action_metadata_allowed", True),
        do_nothing_signal_allowed=kwargs.pop("do_nothing_signal_allowed", True),
        future_repair_suggestion_input_allowed=kwargs.pop("future_repair_suggestion_input_allowed", True),
        future_vera_codex_trial_input_allowed=kwargs.pop("future_vera_codex_trial_input_allowed", True),
        test_execution_allowed=kwargs.pop("test_execution_allowed", False),
        subprocess_allowed=kwargs.pop("subprocess_allowed", False),
        shell_allowed=kwargs.pop("shell_allowed", False),
        dependency_install_allowed=kwargs.pop("dependency_install_allowed", False),
        network_allowed=kwargs.pop("network_allowed", False),
        repair_patch_proposal_allowed=kwargs.pop("repair_patch_proposal_allowed", False),
        automatic_repair_allowed=kwargs.pop("automatic_repair_allowed", False),
        vera_codex_trial_execution_allowed=kwargs.pop("vera_codex_trial_execution_allowed", False),
        cold_evaluation_execution_allowed=kwargs.pop("cold_evaluation_execution_allowed", False),
        external_agent_allowed=kwargs.pop("external_agent_allowed", False),
        dominion_runtime_allowed=kwargs.pop("dominion_runtime_allowed", False),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.4 feedback decision"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_feedback_validation_finding(**kwargs: Any) -> SandboxFeedbackValidationFinding:
    return SandboxFeedbackValidationFinding(
        finding_id=kwargs.pop("finding_id", "sandbox_feedback_validation_finding:v0.37.4"),
        risk_kind=kwargs.pop("risk_kind", SandboxTestFeedbackRiskKind.UNKNOWN),
        severity=kwargs.pop("severity", SandboxFeedbackSeverity.INFO),
        message=kwargs.pop("message", "feedback validation finding"),
        blocks_feedback=kwargs.pop("blocks_feedback", False),
        evidence_refs=kwargs.pop("evidence_refs", []),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_feedback_validation_report(**kwargs: Any) -> SandboxFeedbackValidationReport:
    return SandboxFeedbackValidationReport(
        validation_report_id=kwargs.pop("validation_report_id", "sandbox_feedback_validation_report:v0.37.4"),
        version=kwargs.pop("version", V0374_VERSION),
        feedback_report_id=kwargs.pop("feedback_report_id", "sandbox_test_feedback_report:v0.37.4"),
        findings=kwargs.pop("findings", []),
        evidence_strength_confirmed=kwargs.pop("evidence_strength_confirmed", True),
        no_overclaim_confirmed=kwargs.pop("no_overclaim_confirmed", True),
        no_production_certification_confirmed=kwargs.pop("no_production_certification_confirmed", True),
        no_repair_confirmed=kwargs.pop("no_repair_confirmed", True),
        summary=kwargs.pop("summary", "feedback validation confirms no repair or overclaim"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.4 validation"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_feedback_run_preview(**kwargs: Any) -> SandboxFeedbackRunPreview:
    return SandboxFeedbackRunPreview(
        run_preview_id=kwargs.pop("run_preview_id", "sandbox_feedback_run_preview:v0.37.4"),
        version=kwargs.pop("version", V0374_VERSION),
        feedback_input_id=kwargs.pop("feedback_input_id", "sandbox_test_feedback_input:v0.37.4"),
        preview_summary=kwargs.pop("preview_summary", "feedback preview only"),
        ready_for_feedback_report=kwargs.pop("ready_for_feedback_report", True),
        ready_for_repair_patch_proposal=kwargs.pop("ready_for_repair_patch_proposal", False),
        ready_for_test_execution=kwargs.pop("ready_for_test_execution", False),
        ready_for_vera_codex_trial_execution=kwargs.pop("ready_for_vera_codex_trial_execution", False),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.4 preview"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_feedback_no_repair_guarantee(**kwargs: Any) -> SandboxFeedbackNoRepairGuarantee:
    no_names = tuple(name for name in SandboxFeedbackNoRepairGuarantee.__dataclass_fields__ if name.startswith("no_"))
    return SandboxFeedbackNoRepairGuarantee(
        guarantee_id=kwargs.pop("guarantee_id", "sandbox_feedback_no_repair_guarantee:v0.37.4"),
        version=kwargs.pop("version", V0374_VERSION),
        summary=kwargs.pop("summary", "v0.37.4 emits feedback only and performs no repair"),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, True) for name in no_names},
    )


def build_v0374_readiness_report(**kwargs: Any) -> V0374ReadinessReport:
    return V0374ReadinessReport(
        readiness_report_id=kwargs.pop("readiness_report_id", "v0374_readiness_report"),
        version=kwargs.pop("version", V0374_VERSION),
        readiness_level=kwargs.pop("readiness_level", SandboxTestFeedbackReadinessLevel.DESIGN_HANDOFF_READY_FOR_V0375),
        status=kwargs.pop("status", SandboxTestFeedbackStatus.FEEDBACK_CREATED),
        summary=kwargs.pop("summary", "v0.37.4 feedback ready; execution and repair remain false"),
        ready_for_v0375_repair_suggestion_metadata=kwargs.pop("ready_for_v0375_repair_suggestion_metadata", True),
        ready_for_v0376_vera_codex_one_shot_agent_trial=kwargs.pop("ready_for_v0376_vera_codex_one_shot_agent_trial", True),
        ready_for_v0377_cold_agent_performance_evaluation=kwargs.pop("ready_for_v0377_cold_agent_performance_evaluation", True),
        ready_for_test_feedback_report=kwargs.pop("ready_for_test_feedback_report", True),
        ready_for_failure_diagnosis_report=kwargs.pop("ready_for_failure_diagnosis_report", True),
        ready_for_root_cause_hypothesis_metadata=kwargs.pop("ready_for_root_cause_hypothesis_metadata", True),
        ready_for_evidence_strength_assessment=kwargs.pop("ready_for_evidence_strength_assessment", True),
        ready_for_suggested_next_action_metadata=kwargs.pop("ready_for_suggested_next_action_metadata", True),
        ready_for_do_nothing_alternative_signal=kwargs.pop("ready_for_do_nothing_alternative_signal", True),
        ready_for_future_repair_suggestion_input=kwargs.pop("ready_for_future_repair_suggestion_input", True),
        ready_for_future_vera_codex_trial_input=kwargs.pop("ready_for_future_vera_codex_trial_input", True),
        ready_for_future_cold_evaluation_input=kwargs.pop("ready_for_future_cold_evaluation_input", True),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        ready_for_test_execution=kwargs.pop("ready_for_test_execution", False),
        ready_for_controlled_test_subprocess=kwargs.pop("ready_for_controlled_test_subprocess", False),
        ready_for_shell_execution=kwargs.pop("ready_for_shell_execution", False),
        ready_for_subprocess_execution=kwargs.pop("ready_for_subprocess_execution", False),
        ready_for_command_execution=kwargs.pop("ready_for_command_execution", False),
        ready_for_dependency_install=kwargs.pop("ready_for_dependency_install", False),
        ready_for_network_access=kwargs.pop("ready_for_network_access", False),
        ready_for_repair_patch_proposal=kwargs.pop("ready_for_repair_patch_proposal", False),
        ready_for_automatic_repair=kwargs.pop("ready_for_automatic_repair", False),
        ready_for_multi_cycle_agentic_loop=kwargs.pop("ready_for_multi_cycle_agentic_loop", False),
        ready_for_vera_codex_trial_execution=kwargs.pop("ready_for_vera_codex_trial_execution", False),
        ready_for_cold_agent_performance_evaluation=kwargs.pop("ready_for_cold_agent_performance_evaluation", False),
        ready_for_external_agent_execution=kwargs.pop("ready_for_external_agent_execution", False),
        ready_for_dominion_runtime=kwargs.pop("ready_for_dominion_runtime", False),
        production_certified=kwargs.pop("production_certified", False),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.4 feedback"]),
        metadata=kwargs.pop("metadata", {}),
    )


def default_sandbox_test_feedback_policy(**kwargs: Any) -> SandboxTestFeedbackPolicy:
    return build_sandbox_test_feedback_policy(**kwargs)


def build_test_feedback_input_from_result_envelope(
    result_envelope: SandboxTestResultEnvelope,
    **kwargs: Any,
) -> SandboxTestFeedbackInput:
    return build_sandbox_test_feedback_input(
        result_envelope_id=result_envelope.result_envelope_id,
        outcome_classification_id=result_envelope.outcome_classification.outcome_classification_id,
        failure_classification_id=result_envelope.failure_classification.failure_classification_id if result_envelope.failure_classification else None,
        source_refs=[build_sandbox_test_feedback_source_ref(
            source_id=result_envelope.result_envelope_id,
            evidence_refs=[result_envelope.result_envelope_id],
        )],
        **kwargs,
    )


def _diagnosis_from_failure(failure: SandboxTestFailureClassification | None, outcome: SandboxTestOutcomeClassification) -> SandboxFailureDiagnosisKind:
    failure_kind = _enum_value(failure.failure_class_kind) if failure else ""
    outcome_kind = _enum_value(outcome.outcome_kind)
    mapping = {
        SandboxTestFailureClassKind.NO_FAILURE_DETECTED.value: SandboxFailureDiagnosisKind.NO_FAILURE_DETECTED,
        SandboxTestFailureClassKind.ASSERTION_FAILURE.value: SandboxFailureDiagnosisKind.ASSERTION_FAILURE_DIAGNOSIS,
        SandboxTestFailureClassKind.IMPORT_FAILURE.value: SandboxFailureDiagnosisKind.IMPORT_FAILURE_DIAGNOSIS,
        SandboxTestFailureClassKind.SYNTAX_FAILURE.value: SandboxFailureDiagnosisKind.SYNTAX_FAILURE_DIAGNOSIS,
        SandboxTestFailureClassKind.MISSING_DEPENDENCY_FAILURE.value: SandboxFailureDiagnosisKind.MISSING_DEPENDENCY_DIAGNOSIS,
        SandboxTestFailureClassKind.TIMEOUT_FAILURE.value: SandboxFailureDiagnosisKind.TIMEOUT_DIAGNOSIS,
        SandboxTestFailureClassKind.COLLECTION_FAILURE.value: SandboxFailureDiagnosisKind.COLLECTION_FAILURE_DIAGNOSIS,
        SandboxTestFailureClassKind.RUNTIME_ERROR_FAILURE.value: SandboxFailureDiagnosisKind.RUNTIME_ERROR_DIAGNOSIS,
        SandboxTestFailureClassKind.COMMAND_BLOCKED_FAILURE.value: SandboxFailureDiagnosisKind.COMMAND_BLOCKED_DIAGNOSIS,
        SandboxTestFailureClassKind.UNSAFE_OUTPUT_FAILURE.value: SandboxFailureDiagnosisKind.UNSAFE_OUTPUT_DIAGNOSIS,
        SandboxTestFailureClassKind.INCONCLUSIVE_FAILURE.value: SandboxFailureDiagnosisKind.INCONCLUSIVE_DIAGNOSIS,
    }
    if failure_kind in mapping:
        return mapping[failure_kind]
    if outcome_kind == SandboxTestOutcomeKind.INCONCLUSIVE.value:
        return SandboxFailureDiagnosisKind.INCONCLUSIVE_DIAGNOSIS
    return SandboxFailureDiagnosisKind.UNKNOWN_DIAGNOSIS


def create_failure_observations_from_result_envelope(
    result_envelope: SandboxTestResultEnvelope,
    policy: SandboxTestFeedbackPolicy | None = None,
) -> list[SandboxFailureObservation]:
    policy = policy or default_sandbox_test_feedback_policy()
    outcome = result_envelope.outcome_classification
    failure = result_envelope.failure_classification
    diagnosis = _diagnosis_from_failure(failure, outcome)
    evidence_refs = [snippet.evidence_snippet_id for snippet in result_envelope.evidence_snippets[: policy.max_observations]]
    outcome_kind = _enum_value(outcome.outcome_kind)
    severity = SandboxFeedbackSeverity.INFO
    if outcome_kind in (SandboxTestOutcomeKind.FAILED.value, SandboxTestOutcomeKind.FAILED_ASSERTION.value, SandboxTestOutcomeKind.IMPORT_ERROR.value, SandboxTestOutcomeKind.SYNTAX_ERROR.value):
        severity = SandboxFeedbackSeverity.HIGH
    elif outcome_kind in (SandboxTestOutcomeKind.MISSING_DEPENDENCY.value, SandboxTestOutcomeKind.TIMEOUT.value, SandboxTestOutcomeKind.COMMAND_BLOCKED.value, SandboxTestOutcomeKind.UNSAFE_OUTPUT.value):
        severity = SandboxFeedbackSeverity.MEDIUM
    elif outcome_kind == SandboxTestOutcomeKind.INCONCLUSIVE.value:
        severity = SandboxFeedbackSeverity.LOW
    summary = f"{diagnosis.value}; outcome {outcome_kind}; feedback is not success certification"
    return [build_sandbox_failure_observation(
        diagnosis_kind=diagnosis,
        observation_summary=_limit_text(summary, policy.max_evidence_chars),
        evidence_refs=evidence_refs,
        severity=severity,
        confidence=SandboxFeedbackConfidenceLevel.LOW if outcome.inconclusive else SandboxFeedbackConfidenceLevel.MEDIUM,
        blocked=diagnosis in (SandboxFailureDiagnosisKind.UNSAFE_OUTPUT_DIAGNOSIS, SandboxFailureDiagnosisKind.COMMAND_BLOCKED_DIAGNOSIS),
    )]


def assess_evidence_strength_for_feedback(
    result_envelope: SandboxTestResultEnvelope,
    observations: list[SandboxFailureObservation] | None = None,
) -> SandboxEvidenceAssessment:
    observations = observations or create_failure_observations_from_result_envelope(result_envelope)
    supporting = [ref for observation in observations for ref in observation.evidence_refs]
    outcome = result_envelope.outcome_classification
    if outcome.inconclusive or not supporting:
        return build_sandbox_evidence_assessment(
            evidence_strength=SandboxEvidenceStrength.INSUFFICIENT,
            confidence=SandboxFeedbackConfidenceLevel.INCONCLUSIVE,
            evidence_summary="insufficient evidence; do-nothing or human review remains appropriate",
            supporting_evidence_refs=supporting,
            insufficient_evidence=True,
        )
    if result_envelope.evidence_snippets and len(result_envelope.evidence_snippets) >= 2:
        return build_sandbox_evidence_assessment(
            evidence_strength=SandboxEvidenceStrength.STRONG,
            confidence=SandboxFeedbackConfidenceLevel.HIGH,
            evidence_summary="multiple bounded evidence snippets support diagnosis; not proof",
            supporting_evidence_refs=supporting,
            insufficient_evidence=False,
        )
    return build_sandbox_evidence_assessment(
        evidence_strength=SandboxEvidenceStrength.MODERATE,
        confidence=SandboxFeedbackConfidenceLevel.MEDIUM,
        evidence_summary="bounded result evidence supports diagnosis; not proof",
        supporting_evidence_refs=supporting,
        insufficient_evidence=False,
    )


def _hypothesis_kind_for_observation(observation: SandboxFailureObservation) -> SandboxRootCauseHypothesisKind:
    diagnosis = _enum_value(observation.diagnosis_kind)
    mapping = {
        SandboxFailureDiagnosisKind.ASSERTION_FAILURE_DIAGNOSIS.value: SandboxRootCauseHypothesisKind.IMPLEMENTATION_BUG_LIKELY,
        SandboxFailureDiagnosisKind.IMPORT_FAILURE_DIAGNOSIS.value: SandboxRootCauseHypothesisKind.IMPORT_PATH_ISSUE_LIKELY,
        SandboxFailureDiagnosisKind.SYNTAX_FAILURE_DIAGNOSIS.value: SandboxRootCauseHypothesisKind.SYNTAX_ISSUE_LIKELY,
        SandboxFailureDiagnosisKind.MISSING_DEPENDENCY_DIAGNOSIS.value: SandboxRootCauseHypothesisKind.MISSING_DEPENDENCY_LIKELY,
        SandboxFailureDiagnosisKind.TIMEOUT_DIAGNOSIS.value: SandboxRootCauseHypothesisKind.TIMEOUT_OR_PERFORMANCE_ISSUE_LIKELY,
        SandboxFailureDiagnosisKind.COLLECTION_FAILURE_DIAGNOSIS.value: SandboxRootCauseHypothesisKind.STALE_TEST_OR_CONTEXT_LIKELY,
        SandboxFailureDiagnosisKind.COMMAND_BLOCKED_DIAGNOSIS.value: SandboxRootCauseHypothesisKind.COMMAND_POLICY_BLOCK_LIKELY,
        SandboxFailureDiagnosisKind.UNSAFE_OUTPUT_DIAGNOSIS.value: SandboxRootCauseHypothesisKind.UNSAFE_OUTPUT_OR_SECRET_RISK_LIKELY,
        SandboxFailureDiagnosisKind.NO_FAILURE_DETECTED.value: SandboxRootCauseHypothesisKind.NO_ROOT_CAUSE_IDENTIFIED,
        SandboxFailureDiagnosisKind.INCONCLUSIVE_DIAGNOSIS.value: SandboxRootCauseHypothesisKind.INCONCLUSIVE,
    }
    return mapping.get(diagnosis, SandboxRootCauseHypothesisKind.UNKNOWN)


def generate_root_cause_hypotheses(
    observations: list[SandboxFailureObservation],
    evidence_assessment: SandboxEvidenceAssessment,
    policy: SandboxTestFeedbackPolicy | None = None,
) -> list[SandboxRootCauseHypothesis]:
    policy = policy or default_sandbox_test_feedback_policy()
    hypotheses: list[SandboxRootCauseHypothesis] = []
    confidence = evidence_assessment.confidence
    if _enum_value(evidence_assessment.evidence_strength) in (SandboxEvidenceStrength.INSUFFICIENT.value, SandboxEvidenceStrength.CONTRADICTORY.value):
        confidence = SandboxFeedbackConfidenceLevel.INCONCLUSIVE
    for index, observation in enumerate(observations[: policy.max_hypotheses]):
        kind = _hypothesis_kind_for_observation(observation)
        hypotheses.append(build_sandbox_root_cause_hypothesis(
            hypothesis_id=f"sandbox_root_cause_hypothesis:{index}:v0.37.4",
            hypothesis_kind=kind,
            hypothesis_summary=f"{kind.value}; evidence-bounded hypothesis, not proof",
            evidence_assessment=evidence_assessment,
            confidence=confidence,
            evidence_strength=evidence_assessment.evidence_strength,
            proven=False,
            repair_allowed=False,
        ))
    return hypotheses or [build_sandbox_root_cause_hypothesis(evidence_assessment=evidence_assessment)]


def generate_suggested_next_actions(
    result_envelope: SandboxTestResultEnvelope,
    evidence_assessment: SandboxEvidenceAssessment,
    hypotheses: list[SandboxRootCauseHypothesis],
) -> list[SandboxSuggestedNextAction]:
    outcome = _enum_value(result_envelope.outcome_classification.outcome_kind)
    evidence_refs = [hypothesis.hypothesis_id for hypothesis in hypotheses]
    actions = [build_sandbox_suggested_next_action(
        suggested_action_id="sandbox_suggested_next_action:human_review:v0.37.4",
        action_kind=SandboxSuggestedNextActionKind.REQUEST_HUMAN_REVIEW,
        action_summary="request human review of bounded diagnosis metadata",
        rationale="failure diagnosis is not repair execution",
        evidence_refs=evidence_refs,
        future_gated=False,
    )]
    if _enum_value(evidence_assessment.evidence_strength) in (SandboxEvidenceStrength.INSUFFICIENT.value, SandboxEvidenceStrength.CONTRADICTORY.value):
        actions.insert(0, build_sandbox_suggested_next_action(
            suggested_action_id="sandbox_suggested_next_action:do_nothing:v0.37.4",
            action_kind=SandboxSuggestedNextActionKind.DO_NOTHING,
            action_summary="do nothing remains preferable until evidence improves",
            rationale="insufficient or contradictory evidence must not trigger repair",
            evidence_refs=evidence_refs,
            future_gated=False,
        ))
        return actions
    if outcome == SandboxTestOutcomeKind.MISSING_DEPENDENCY.value:
        actions.append(build_sandbox_suggested_next_action(
            suggested_action_id="sandbox_suggested_next_action:inspect_missing_dependency:v0.37.4",
            action_kind=SandboxSuggestedNextActionKind.INSPECT_MISSING_DEPENDENCY_WITHOUT_INSTALL,
            action_summary="inspect missing dependency metadata without installing dependencies",
            rationale="missing dependency classification does not grant install permission",
            evidence_refs=evidence_refs,
            future_gated=True,
        ))
    elif outcome == SandboxTestOutcomeKind.TIMEOUT.value:
        actions.append(build_sandbox_suggested_next_action(
            suggested_action_id="sandbox_suggested_next_action:future_rerun_gate:v0.37.4",
            action_kind=SandboxSuggestedNextActionKind.RERUN_TEST_FUTURE_GATE,
            action_summary="future-gated rerun consideration only",
            rationale="timeout classification does not grant retry permission",
            evidence_refs=evidence_refs,
            future_gated=True,
        ))
    elif result_envelope.outcome_classification.failed:
        actions.append(build_sandbox_suggested_next_action(
            suggested_action_id="sandbox_suggested_next_action:future_repair_input:v0.37.4",
            action_kind=SandboxSuggestedNextActionKind.CREATE_REPAIR_SUGGESTION_FUTURE_GATE,
            action_summary="prepare future repair suggestion input metadata",
            rationale="v0.37.4 does not create repair patch proposals",
            evidence_refs=evidence_refs,
            future_gated=True,
        ))
    else:
        actions.append(build_sandbox_suggested_next_action(
            suggested_action_id="sandbox_suggested_next_action:trial_future_gate:v0.37.4",
            action_kind=SandboxSuggestedNextActionKind.PROCEED_TO_VERA_CODEX_TRIAL_FUTURE_GATE,
            action_summary="prepare future Vera-Codex trial input metadata",
            rationale="trial execution remains future-gated",
            evidence_refs=evidence_refs,
            future_gated=True,
        ))
    return actions


def generate_do_nothing_alternative_signal(
    result_envelope: SandboxTestResultEnvelope,
    evidence_assessment: SandboxEvidenceAssessment,
) -> SandboxDoNothingAlternativeSignal:
    strength = _enum_value(evidence_assessment.evidence_strength)
    if strength in (SandboxEvidenceStrength.INSUFFICIENT.value, SandboxEvidenceStrength.CONTRADICTORY.value):
        return build_sandbox_do_nothing_alternative_signal(
            signal_kind=SandboxDoNothingSignalKind.DO_NOTHING_REQUIRED_DUE_TO_INSUFFICIENT_EVIDENCE,
            signal_summary="do nothing required because evidence is insufficient or contradictory",
            evidence_refs=evidence_assessment.supporting_evidence_refs,
            risk_delta_summary="acting now may increase repair or overclaim risk",
            test_delta_summary="no additional test delta is produced in v0.37.4",
        )
    if result_envelope.outcome_classification.failed:
        return build_sandbox_do_nothing_alternative_signal(
            signal_kind=SandboxDoNothingSignalKind.DO_NOTHING_COMPETITIVE,
            signal_summary="do nothing remains a comparator but appears inferior to future-gated review",
            evidence_refs=evidence_assessment.supporting_evidence_refs,
            risk_delta_summary="future-gated metadata action may reduce uncertainty without execution",
            test_delta_summary="failed outcome evidence is preserved but not rerun",
        )
    return build_sandbox_do_nothing_alternative_signal(
        signal_kind=SandboxDoNothingSignalKind.DO_NOTHING_NOT_EVALUABLE_YET,
        signal_summary="do-nothing baseline is represented but not scored",
        evidence_refs=evidence_assessment.supporting_evidence_refs,
    )


def create_sandbox_failure_diagnosis_report(
    result_envelope: SandboxTestResultEnvelope,
    feedback_input: SandboxTestFeedbackInput | None = None,
    policy: SandboxTestFeedbackPolicy | None = None,
) -> SandboxFailureDiagnosisReport:
    feedback_input = feedback_input or build_test_feedback_input_from_result_envelope(result_envelope)
    policy = policy or default_sandbox_test_feedback_policy()
    observations = create_failure_observations_from_result_envelope(result_envelope, policy)
    assessment = assess_evidence_strength_for_feedback(result_envelope, observations)
    hypotheses = generate_root_cause_hypotheses(observations, assessment, policy)
    primary = hypotheses[0].hypothesis_id if hypotheses else None
    inconclusive = _enum_value(assessment.evidence_strength) in (SandboxEvidenceStrength.INSUFFICIENT.value, SandboxEvidenceStrength.CONTRADICTORY.value)
    return build_sandbox_failure_diagnosis_report(
        feedback_input_id=feedback_input.feedback_input_id,
        observations=observations,
        hypotheses=hypotheses,
        evidence_assessments=[assessment],
        diagnosis_summary="failure diagnosis created from supplied result envelope metadata only",
        primary_hypothesis_id=primary,
        inconclusive=inconclusive,
    )


def create_sandbox_test_feedback_report(
    result_envelope: SandboxTestResultEnvelope,
    policy: SandboxTestFeedbackPolicy | None = None,
) -> SandboxTestFeedbackReport:
    policy = policy or default_sandbox_test_feedback_policy()
    feedback_input = build_test_feedback_input_from_result_envelope(result_envelope)
    diagnosis = create_sandbox_failure_diagnosis_report(result_envelope, feedback_input, policy)
    assessment = diagnosis.evidence_assessments[0] if diagnosis.evidence_assessments else build_sandbox_evidence_assessment()
    actions = generate_suggested_next_actions(result_envelope, assessment, diagnosis.hypotheses)
    do_nothing = generate_do_nothing_alternative_signal(result_envelope, assessment)
    return build_sandbox_test_feedback_report(
        feedback_input_id=feedback_input.feedback_input_id,
        diagnosis_report=diagnosis,
        suggested_actions=actions,
        do_nothing_signal=do_nothing,
        source_refs=feedback_input.source_refs,
        summary="feedback report created from supplied v0.37.3 result envelope only",
    )


def validate_sandbox_test_feedback_report(report: SandboxTestFeedbackReport) -> SandboxFeedbackValidationReport:
    findings: list[SandboxFeedbackValidationFinding] = []
    if report.production_certified:
        findings.append(build_sandbox_feedback_validation_finding(
            risk_kind=SandboxTestFeedbackRiskKind.PRODUCTION_CERTIFICATION_CONFUSION_RISK,
            severity=SandboxFeedbackSeverity.BLOCKED,
            message="production certification is not allowed",
            blocks_feedback=True,
        ))
    if report.repair_allowed or report.repair_performed:
        findings.append(build_sandbox_feedback_validation_finding(
            risk_kind=SandboxTestFeedbackRiskKind.REPAIR_PERMISSION_CONFUSION_RISK,
            severity=SandboxFeedbackSeverity.BLOCKED,
            message="repair is not allowed",
            blocks_feedback=True,
        ))
    if report.diagnosis_report.inconclusive and any(_enum_value(action.action_kind) == SandboxSuggestedNextActionKind.CREATE_REPAIR_SUGGESTION_FUTURE_GATE.value for action in report.suggested_actions):
        findings.append(build_sandbox_feedback_validation_finding(
            risk_kind=SandboxTestFeedbackRiskKind.INSUFFICIENT_EVIDENCE_RISK,
            severity=SandboxFeedbackSeverity.HIGH,
            message="inconclusive evidence should not proceed directly to repair suggestion input",
            blocks_feedback=True,
        ))
    return build_sandbox_feedback_validation_report(
        feedback_report_id=report.feedback_report_id,
        findings=findings,
        summary="feedback validation report",
    )


def sandbox_feedback_flags_preserve_no_execution(flags: SandboxTestFeedbackFlagSet) -> bool:
    return isinstance(flags, SandboxTestFeedbackFlagSet) and all(getattr(flags, name) is False for name in UNSAFE_FEEDBACK_FLAG_NAMES)


def sandbox_feedback_policy_blocks_repair_execution(policy: SandboxTestFeedbackPolicy) -> bool:
    return isinstance(policy, SandboxTestFeedbackPolicy) and all(getattr(policy, name) is False for name in UNSAFE_FEEDBACK_POLICY_ALLOW_NAMES)


def sandbox_root_cause_hypothesis_is_not_proof(hypothesis: SandboxRootCauseHypothesis) -> bool:
    return isinstance(hypothesis, SandboxRootCauseHypothesis) and hypothesis.proven is False and hypothesis.repair_allowed is False


def sandbox_suggested_next_action_is_not_execution(action: SandboxSuggestedNextAction) -> bool:
    return isinstance(action, SandboxSuggestedNextAction) and not action.executes_now and not action.repair_allowed and not action.test_rerun_allowed and not action.dependency_install_allowed


def sandbox_do_nothing_signal_is_not_scorecard(signal: SandboxDoNothingAlternativeSignal) -> bool:
    return isinstance(signal, SandboxDoNothingAlternativeSignal) and signal.scoring_performed is False


def sandbox_feedback_report_is_not_execution(report: SandboxTestFeedbackReport) -> bool:
    return (
        isinstance(report, SandboxTestFeedbackReport)
        and report.test_execution_performed is False
        and report.subprocess_executed_by_v0374 is False
        and report.repair_performed is False
        and report.ready_for_execution is False
    )


def v0374_readiness_report_is_not_execution_ready(report: V0374ReadinessReport) -> bool:
    if not isinstance(report, V0374ReadinessReport):
        return False
    return all(
        getattr(report, name) is False
        for name in (
            "ready_for_execution",
            "ready_for_test_execution",
            "ready_for_controlled_test_subprocess",
            "ready_for_shell_execution",
            "ready_for_subprocess_execution",
            "ready_for_command_execution",
            "ready_for_dependency_install",
            "ready_for_network_access",
            "ready_for_repair_patch_proposal",
            "ready_for_automatic_repair",
            "ready_for_multi_cycle_agentic_loop",
            "ready_for_vera_codex_trial_execution",
            "ready_for_cold_agent_performance_evaluation",
            "ready_for_external_agent_execution",
            "ready_for_dominion_runtime",
            "production_certified",
        )
    )
