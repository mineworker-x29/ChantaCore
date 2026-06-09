from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list
from .sandbox_test_execution import (
    ControlledTestSubprocessResult,
    SandboxTestExecutionResult,
    SandboxTestExecutionStatus,
    SandboxTestOutputCapture,
    SandboxTestOutputStreamKind,
    SandboxTestProcessExitKind,
)


V0373_VERSION = "v0.37.3"
V0373_RELEASE_NAME = "v0.37.3 Test Result Envelope & Output Classifier"


UNSAFE_RESULT_FLAG_NAMES = (
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

UNSAFE_POLICY_ALLOW_NAMES = (
    "allow_test_execution",
    "allow_subprocess",
    "allow_shell",
    "allow_dependency_install",
    "allow_network_access",
    "allow_automatic_repair",
    "allow_vera_codex_trial_execution",
    "allow_cold_performance_evaluation",
    "allow_external_agent_execution",
    "allow_dominion_runtime",
)

SECRET_MARKERS = ("SECRET", "TOKEN", "KEY", "PASSWORD", "CREDENTIAL")


def _validate_list(name: str, value: Any) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{name} must be a list")


def _validate_dict(name: str, value: Any) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a dict")


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0373_VERSION not in version:
        raise ValueError("version must include v0.37.3")


def _validate_false(name: str, value: bool) -> None:
    if value is not False:
        raise ValueError(f"{name} must remain False in v0.37.3")


def _validate_true(name: str, value: bool) -> None:
    if value is not True:
        raise ValueError(f"{name} must be True")


def _validate_non_negative(name: str, value: int | None) -> None:
    if value is not None and value < 0:
        raise ValueError(f"{name} must be None or >= 0")


def _validate_metadata(value: dict[str, Any]) -> None:
    _validate_dict("metadata", value)


def _enum_value(value: Any) -> str:
    return value.value if isinstance(value, StrEnum) else str(value)


def _limit_text(text: str, limit: int) -> tuple[str, bool]:
    if limit < 0:
        raise ValueError("limit must be >= 0")
    if len(text) <= limit:
        return text, False
    return text[:limit], True


def _redact_secret_like(text: str) -> tuple[str, bool]:
    redacted = text
    changed = False
    for marker in SECRET_MARKERS:
        if marker.lower() in redacted.lower():
            redacted = redacted.replace(marker, "[REDACTED]")
            redacted = redacted.replace(marker.lower(), "[REDACTED]")
            changed = True
    return redacted, changed


def _combined_text(stdout_text: str, stderr_text: str) -> str:
    return "\n".join(part for part in (stdout_text, stderr_text) if part)


class SandboxTestResultEnvelopeMode(StrEnum):
    PROCESS_RESULT_ENVELOPE = "process_result_envelope"
    OUTPUT_CLASSIFIER_ENVELOPE = "output_classifier_envelope"
    COMBINED_RESULT_ENVELOPE = "combined_result_envelope"
    EVIDENCE_ONLY_ENVELOPE = "evidence_only_envelope"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class SandboxTestResultSourceKind(StrEnum):
    V0372_SANDBOX_TEST_EXECUTION_RESULT = "v0372_sandbox_test_execution_result"
    V0372_CONTROLLED_SUBPROCESS_RESULT = "v0372_controlled_subprocess_result"
    V0372_OUTPUT_CAPTURE = "v0372_output_capture"
    V0371_INVOCATION_CONTRACT = "v0371_invocation_contract"
    V0371_COMMAND_SPEC = "v0371_command_spec"
    V0370_TEST_RUNNER_BOUNDARY = "v0370_test_runner_boundary"
    MANUAL_OPERATOR_INPUT = "manual_operator_input"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class SandboxTestResultStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    INPUT_VALIDATED = "input_validated"
    CLASSIFIED = "classified"
    CLASSIFIED_WITH_WARNINGS = "classified_with_warnings"
    ENVELOPE_CREATED = "envelope_created"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATED = "future_gated"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class SandboxTestResultReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    RESULT_ENVELOPE_CONTRACT_READY = "result_envelope_contract_ready"
    PROCESS_CLASSIFICATION_READY = "process_classification_ready"
    OUTPUT_CLASSIFIER_READY = "output_classifier_ready"
    EVIDENCE_SNIPPET_READY = "evidence_snippet_ready"
    FUTURE_FEEDBACK_INPUT_READY = "future_feedback_input_ready"
    DESIGN_HANDOFF_READY_FOR_V0374 = "design_handoff_ready_for_v0374"
    DESIGN_HANDOFF_READY_FOR_V0376 = "design_handoff_ready_for_v0376"
    DESIGN_HANDOFF_READY_FOR_V0377 = "design_handoff_ready_for_v0377"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class SandboxTestResultDecisionKind(StrEnum):
    ALLOW_RESULT_ENVELOPE_CREATION = "allow_result_envelope_creation"
    ALLOW_PROCESS_CLASSIFICATION = "allow_process_classification"
    ALLOW_OUTPUT_CLASSIFICATION = "allow_output_classification"
    ALLOW_EVIDENCE_SNIPPET_EXTRACTION = "allow_evidence_snippet_extraction"
    ALLOW_FUTURE_FEEDBACK_INPUT = "allow_future_feedback_input"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class SandboxTestResultRiskKind(StrEnum):
    MISSING_EXECUTION_RESULT_RISK = "missing_execution_result_risk"
    MISSING_SUBPROCESS_RESULT_RISK = "missing_subprocess_result_risk"
    MISSING_OUTPUT_CAPTURE_RISK = "missing_output_capture_risk"
    UNBOUNDED_OUTPUT_RISK = "unbounded_output_risk"
    SECRET_LIKE_OUTPUT_RISK = "secret_like_output_risk"
    AMBIGUOUS_OUTPUT_RISK = "ambiguous_output_risk"
    FAILED_TEST_MISREPORTED_AS_SUCCESS_RISK = "failed_test_misreported_as_success_risk"
    PROCESS_EXIT_OVERCLAIM_RISK = "process_exit_overclaim_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    MISSING_DEPENDENCY_INSTALL_CONFUSION_RISK = "missing_dependency_install_confusion_risk"
    TIMEOUT_RETRY_CONFUSION_RISK = "timeout_retry_confusion_risk"
    FAILURE_REPAIR_CONFUSION_RISK = "failure_repair_confusion_risk"
    VERA_CODEX_OVERCLAIM_RISK = "vera_codex_overclaim_risk"
    DO_NOTHING_OMISSION_RISK = "do_nothing_omission_risk"
    UNKNOWN = "unknown"


class SandboxTestProcessClassificationKind(StrEnum):
    NOT_EXECUTED = "not_executed"
    PROCESS_EXIT_ZERO = "process_exit_zero"
    PROCESS_EXIT_NONZERO = "process_exit_nonzero"
    PROCESS_TIMEOUT = "process_timeout"
    BLOCKED_BEFORE_EXECUTION = "blocked_before_execution"
    FAILED_TO_START_SAFE = "failed_to_start_safe"
    PROCESS_RESULT_UNKNOWN = "process_result_unknown"
    UNKNOWN = "unknown"


class SandboxTestOutcomeKind(StrEnum):
    PASSED = "passed"
    FAILED = "failed"
    FAILED_ASSERTION = "failed_assertion"
    IMPORT_ERROR = "import_error"
    SYNTAX_ERROR = "syntax_error"
    MISSING_DEPENDENCY = "missing_dependency"
    TIMEOUT = "timeout"
    COMMAND_BLOCKED = "command_blocked"
    UNSAFE_OUTPUT = "unsafe_output"
    INCONCLUSIVE = "inconclusive"
    NO_TESTS_COLLECTED = "no_tests_collected"
    SAFE_FAILED = "safe_failed"
    UNKNOWN = "unknown"


class SandboxTestFailureClassKind(StrEnum):
    NO_FAILURE_DETECTED = "no_failure_detected"
    ASSERTION_FAILURE = "assertion_failure"
    IMPORT_FAILURE = "import_failure"
    SYNTAX_FAILURE = "syntax_failure"
    MISSING_DEPENDENCY_FAILURE = "missing_dependency_failure"
    TIMEOUT_FAILURE = "timeout_failure"
    COLLECTION_FAILURE = "collection_failure"
    RUNTIME_ERROR_FAILURE = "runtime_error_failure"
    COMMAND_BLOCKED_FAILURE = "command_blocked_failure"
    UNSAFE_OUTPUT_FAILURE = "unsafe_output_failure"
    UNKNOWN_FAILURE = "unknown_failure"
    INCONCLUSIVE_FAILURE = "inconclusive_failure"


class SandboxTestEvidenceKind(StrEnum):
    PROCESS_EXIT_CODE = "process_exit_code"
    TIMEOUT_STATUS = "timeout_status"
    STDOUT_EXCERPT = "stdout_excerpt"
    STDERR_EXCERPT = "stderr_excerpt"
    PYTEST_SUMMARY_LINE = "pytest_summary_line"
    UNITTEST_SUMMARY_LINE = "unittest_summary_line"
    TRACEBACK_EXCERPT = "traceback_excerpt"
    IMPORT_ERROR_EXCERPT = "import_error_excerpt"
    SYNTAX_ERROR_EXCERPT = "syntax_error_excerpt"
    ASSERTION_ERROR_EXCERPT = "assertion_error_excerpt"
    MISSING_DEPENDENCY_EXCERPT = "missing_dependency_excerpt"
    COMMAND_BLOCKED_EXCERPT = "command_blocked_excerpt"
    NO_TESTS_COLLECTED_EXCERPT = "no_tests_collected_excerpt"
    REDACTION_NOTICE = "redaction_notice"
    UNKNOWN = "unknown"


class SandboxTestConfidenceLevel(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INCONCLUSIVE = "inconclusive"
    UNKNOWN = "unknown"


class SandboxTestOutputSignalKind(StrEnum):
    PYTEST_PASSED_SIGNAL = "pytest_passed_signal"
    PYTEST_FAILED_SIGNAL = "pytest_failed_signal"
    PYTEST_ERROR_SIGNAL = "pytest_error_signal"
    UNITTEST_OK_SIGNAL = "unittest_ok_signal"
    UNITTEST_FAILED_SIGNAL = "unittest_failed_signal"
    TRACEBACK_SIGNAL = "traceback_signal"
    ASSERTION_ERROR_SIGNAL = "assertion_error_signal"
    IMPORT_ERROR_SIGNAL = "import_error_signal"
    SYNTAX_ERROR_SIGNAL = "syntax_error_signal"
    MISSING_MODULE_SIGNAL = "missing_module_signal"
    NO_TESTS_COLLECTED_SIGNAL = "no_tests_collected_signal"
    TIMEOUT_SIGNAL = "timeout_signal"
    COMMAND_BLOCKED_SIGNAL = "command_blocked_signal"
    SECRET_LIKE_OUTPUT_SIGNAL = "secret_like_output_signal"
    UNKNOWN_SIGNAL = "unknown_signal"


@dataclass(frozen=True)
class SandboxTestResultFlagSet:
    flag_set_id: str
    version: str
    test_result_envelope_layer_constructed: bool
    process_classification_available: bool
    output_classifier_available: bool
    failure_classification_available: bool
    evidence_snippet_extraction_available: bool
    ready_for_v0374_test_feedback_failure_diagnosis: bool
    ready_for_v0375_repair_suggestion_metadata: bool
    ready_for_v0376_vera_codex_one_shot_agent_trial: bool
    ready_for_v0377_cold_agent_performance_evaluation: bool
    ready_for_test_result_envelope: bool
    ready_for_test_output_classifier: bool
    ready_for_process_exit_classification: bool
    ready_for_test_failure_classification: bool
    ready_for_test_evidence_snippets: bool
    ready_for_future_feedback_report_input: bool
    ready_for_future_vera_codex_trial_evidence: bool
    ready_for_future_cold_evaluation_evidence: bool
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
        for name in UNSAFE_RESULT_FLAG_NAMES:
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestResultSourceRef:
    source_ref_id: str
    source_kind: SandboxTestResultSourceKind | str
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
class SandboxTestResultEnvelopePolicy:
    result_policy_id: str
    version: str
    allowed_modes: list[SandboxTestResultEnvelopeMode | str]
    max_stdout_chars: int
    max_stderr_chars: int
    max_evidence_snippet_chars: int
    max_evidence_snippets: int
    require_redaction: bool
    require_confidence_level: bool
    allow_process_classification: bool
    allow_output_classification: bool
    allow_evidence_snippet_extraction: bool
    allow_future_feedback_input: bool
    allow_future_vera_codex_evidence: bool
    allow_test_execution: bool
    allow_subprocess: bool
    allow_shell: bool
    allow_dependency_install: bool
    allow_network_access: bool
    allow_automatic_repair: bool
    allow_vera_codex_trial_execution: bool
    allow_cold_performance_evaluation: bool
    allow_external_agent_execution: bool
    allow_dominion_runtime: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("result_policy_id", self.result_policy_id)
        _validate_version(self.version)
        _validate_list("allowed_modes", self.allowed_modes)
        for name in ("max_stdout_chars", "max_stderr_chars", "max_evidence_snippet_chars", "max_evidence_snippets"):
            _validate_non_negative(name, getattr(self, name))
        _validate_true("require_redaction", self.require_redaction)
        _validate_true("require_confidence_level", self.require_confidence_level)
        for name in UNSAFE_POLICY_ALLOW_NAMES:
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestResultEnvelopeInput:
    envelope_input_id: str
    version: str
    execution_result_id: str | None
    subprocess_result_id: str | None
    command_spec_id: str | None
    invocation_contract_id: str | None
    requested_mode: SandboxTestResultEnvelopeMode | str
    stdout_text: str
    stderr_text: str
    return_code: int | None
    timed_out: bool
    source_refs: list[SandboxTestResultSourceRef]
    prohibited_runtime_actions: list[str]
    task_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("envelope_input_id", self.envelope_input_id)
        _validate_version(self.version)
        _require_non_blank("task_summary", self.task_summary)
        _validate_list("source_refs", self.source_refs)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        required = {"test execution", "subprocess", "shell", "install", "network", "repair", "external agent", "Dominion"}
        if not required.issubset(set(self.prohibited_runtime_actions)):
            raise ValueError("prohibited_runtime_actions must include result-envelope unsafe actions")
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestProcessClassification:
    process_classification_id: str
    classification_kind: SandboxTestProcessClassificationKind | str
    return_code: int | None
    timed_out: bool
    process_summary: str
    confidence: SandboxTestConfidenceLevel | str
    production_certified: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("process_classification_id", self.process_classification_id)
        _require_non_blank("process_summary", self.process_summary)
        _validate_false("production_certified", self.production_certified)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestOutputSignal:
    output_signal_id: str
    signal_kind: SandboxTestOutputSignalKind | str
    stream_kind: str
    signal_summary: str
    evidence_preview: str
    confidence: SandboxTestConfidenceLevel | str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("output_signal_id", self.output_signal_id)
        _require_non_blank("signal_summary", self.signal_summary)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestEvidenceSnippet:
    evidence_snippet_id: str
    evidence_kind: SandboxTestEvidenceKind | str
    stream_kind: str
    snippet_text: str
    snippet_summary: str
    redacted: bool
    truncated: bool
    secret_like_content_detected: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("evidence_snippet_id", self.evidence_snippet_id)
        _require_non_blank("snippet_summary", self.snippet_summary)
        if self.secret_like_content_detected and not self.redacted:
            raise ValueError("secret-like evidence must be redacted")
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestFailureClassification:
    failure_classification_id: str
    failure_class_kind: SandboxTestFailureClassKind | str
    failure_summary: str
    evidence_snippet_ids: list[str]
    confidence: SandboxTestConfidenceLevel | str
    repair_allowed: bool
    retry_allowed: bool
    dependency_install_allowed: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("failure_classification_id", self.failure_classification_id)
        _require_non_blank("failure_summary", self.failure_summary)
        _validate_string_list("evidence_snippet_ids", self.evidence_snippet_ids)
        _validate_false("repair_allowed", self.repair_allowed)
        _validate_false("retry_allowed", self.retry_allowed)
        _validate_false("dependency_install_allowed", self.dependency_install_allowed)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestOutcomeClassification:
    outcome_classification_id: str
    outcome_kind: SandboxTestOutcomeKind | str
    outcome_summary: str
    process_classification_id: str | None
    failure_classification_id: str | None
    output_signal_ids: list[str]
    evidence_snippet_ids: list[str]
    confidence: SandboxTestConfidenceLevel | str
    passed: bool
    failed: bool
    inconclusive: bool
    production_certified: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("outcome_classification_id", self.outcome_classification_id)
        _require_non_blank("outcome_summary", self.outcome_summary)
        _validate_string_list("output_signal_ids", self.output_signal_ids)
        _validate_string_list("evidence_snippet_ids", self.evidence_snippet_ids)
        _validate_false("production_certified", self.production_certified)
        if sum(bool(value) for value in (self.passed, self.failed, self.inconclusive)) > 1:
            raise ValueError("at most one outcome boolean may be True")
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestResultEnvelope:
    result_envelope_id: str
    version: str
    envelope_input_id: str
    mode: SandboxTestResultEnvelopeMode | str
    status: SandboxTestResultStatus | str
    readiness_level: SandboxTestResultReadinessLevel | str
    process_classification: SandboxTestProcessClassification
    outcome_classification: SandboxTestOutcomeClassification
    failure_classification: SandboxTestFailureClassification | None
    output_signals: list[SandboxTestOutputSignal]
    evidence_snippets: list[SandboxTestEvidenceSnippet]
    source_refs: list[SandboxTestResultSourceRef]
    summary: str
    eligible_for_future_feedback_report: bool
    eligible_for_future_vera_codex_trial: bool
    eligible_for_future_cold_evaluation: bool
    test_execution_performed: bool
    subprocess_executed_by_v0373: bool
    repair_allowed: bool
    retry_allowed: bool
    dependency_install_allowed: bool
    production_certified: bool
    ready_for_execution: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("result_envelope_id", self.result_envelope_id)
        _validate_version(self.version)
        _require_non_blank("envelope_input_id", self.envelope_input_id)
        _require_non_blank("summary", self.summary)
        _validate_list("output_signals", self.output_signals)
        _validate_list("evidence_snippets", self.evidence_snippets)
        _validate_list("source_refs", self.source_refs)
        for name in (
            "test_execution_performed",
            "subprocess_executed_by_v0373",
            "repair_allowed",
            "retry_allowed",
            "dependency_install_allowed",
            "production_certified",
            "ready_for_execution",
        ):
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestResultEnvelopeDecision:
    decision_id: str
    envelope_input_id: str
    decision_kind: SandboxTestResultDecisionKind | str
    status: SandboxTestResultStatus | str
    risk_kinds: list[SandboxTestResultRiskKind | str]
    decision_summary: str
    result_envelope_allowed: bool
    process_classification_allowed: bool
    output_classification_allowed: bool
    evidence_extraction_allowed: bool
    future_feedback_input_allowed: bool
    test_execution_allowed: bool
    subprocess_allowed: bool
    shell_allowed: bool
    dependency_install_allowed: bool
    network_allowed: bool
    repair_allowed: bool
    vera_codex_trial_execution_allowed: bool
    external_agent_allowed: bool
    dominion_runtime_allowed: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("decision_id", self.decision_id)
        _require_non_blank("envelope_input_id", self.envelope_input_id)
        _require_non_blank("decision_summary", self.decision_summary)
        _validate_list("risk_kinds", self.risk_kinds)
        for name in (
            "test_execution_allowed",
            "subprocess_allowed",
            "shell_allowed",
            "dependency_install_allowed",
            "network_allowed",
            "repair_allowed",
            "vera_codex_trial_execution_allowed",
            "external_agent_allowed",
            "dominion_runtime_allowed",
        ):
            _validate_false(name, getattr(self, name))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestResultValidationFinding:
    finding_id: str
    risk_kind: SandboxTestResultRiskKind | str
    severity: str
    message: str
    blocks_envelope: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("severity", self.severity)
        _require_non_blank("message", self.message)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestResultValidationReport:
    validation_report_id: str
    version: str
    result_envelope_id: str
    findings: list[SandboxTestResultValidationFinding]
    bounded_output_confirmed: bool
    redaction_confirmed: bool
    confidence_confirmed: bool
    no_production_certification_confirmed: bool
    summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version(self.version)
        _require_non_blank("result_envelope_id", self.result_envelope_id)
        _require_non_blank("summary", self.summary)
        _validate_list("findings", self.findings)
        _validate_true("bounded_output_confirmed", self.bounded_output_confirmed)
        _validate_true("redaction_confirmed", self.redaction_confirmed)
        _validate_true("confidence_confirmed", self.confidence_confirmed)
        _validate_true("no_production_certification_confirmed", self.no_production_certification_confirmed)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestResultClassifierReport:
    classifier_report_id: str
    version: str
    result_envelope_id: str
    classification_completed: bool
    report_summary: str
    production_certified: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("classifier_report_id", self.classifier_report_id)
        _validate_version(self.version)
        _require_non_blank("result_envelope_id", self.result_envelope_id)
        _require_non_blank("report_summary", self.report_summary)
        _validate_false("production_certified", self.production_certified)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestResultRunPreview:
    run_preview_id: str
    version: str
    envelope_input_id: str
    preview_summary: str
    ready_for_result_envelope: bool
    ready_for_test_execution: bool
    ready_for_repair: bool
    ready_for_vera_codex_trial_execution: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        _validate_version(self.version)
        _require_non_blank("envelope_input_id", self.envelope_input_id)
        _require_non_blank("preview_summary", self.preview_summary)
        _validate_false("ready_for_test_execution", self.ready_for_test_execution)
        _validate_false("ready_for_repair", self.ready_for_repair)
        _validate_false("ready_for_vera_codex_trial_execution", self.ready_for_vera_codex_trial_execution)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestResultNoExecutionGuarantee:
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
    no_automatic_repair: bool
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
class V0373ReadinessReport:
    readiness_report_id: str
    version: str
    readiness_level: SandboxTestResultReadinessLevel | str
    status: SandboxTestResultStatus | str
    summary: str
    ready_for_v0374_test_feedback_failure_diagnosis: bool
    ready_for_v0375_repair_suggestion_metadata: bool
    ready_for_v0376_vera_codex_one_shot_agent_trial: bool
    ready_for_v0377_cold_agent_performance_evaluation: bool
    ready_for_test_result_envelope: bool
    ready_for_test_output_classifier: bool
    ready_for_process_exit_classification: bool
    ready_for_test_failure_classification: bool
    ready_for_test_evidence_snippets: bool
    ready_for_future_feedback_report_input: bool
    ready_for_future_vera_codex_trial_evidence: bool
    ready_for_future_cold_evaluation_evidence: bool
    ready_for_execution: bool
    ready_for_test_execution: bool
    ready_for_controlled_test_subprocess: bool
    ready_for_shell_execution: bool
    ready_for_subprocess_execution: bool
    ready_for_command_execution: bool
    ready_for_dependency_install: bool
    ready_for_network_access: bool
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


def build_sandbox_test_result_flags(**kwargs: Any) -> SandboxTestResultFlagSet:
    return SandboxTestResultFlagSet(
        flag_set_id=kwargs.pop("flag_set_id", "sandbox_test_result_flags:v0.37.3"),
        version=kwargs.pop("version", V0373_VERSION),
        test_result_envelope_layer_constructed=kwargs.pop("test_result_envelope_layer_constructed", True),
        process_classification_available=kwargs.pop("process_classification_available", True),
        output_classifier_available=kwargs.pop("output_classifier_available", True),
        failure_classification_available=kwargs.pop("failure_classification_available", True),
        evidence_snippet_extraction_available=kwargs.pop("evidence_snippet_extraction_available", True),
        ready_for_v0374_test_feedback_failure_diagnosis=kwargs.pop("ready_for_v0374_test_feedback_failure_diagnosis", True),
        ready_for_v0375_repair_suggestion_metadata=kwargs.pop("ready_for_v0375_repair_suggestion_metadata", True),
        ready_for_v0376_vera_codex_one_shot_agent_trial=kwargs.pop("ready_for_v0376_vera_codex_one_shot_agent_trial", True),
        ready_for_v0377_cold_agent_performance_evaluation=kwargs.pop("ready_for_v0377_cold_agent_performance_evaluation", True),
        ready_for_test_result_envelope=kwargs.pop("ready_for_test_result_envelope", True),
        ready_for_test_output_classifier=kwargs.pop("ready_for_test_output_classifier", True),
        ready_for_process_exit_classification=kwargs.pop("ready_for_process_exit_classification", True),
        ready_for_test_failure_classification=kwargs.pop("ready_for_test_failure_classification", True),
        ready_for_test_evidence_snippets=kwargs.pop("ready_for_test_evidence_snippets", True),
        ready_for_future_feedback_report_input=kwargs.pop("ready_for_future_feedback_report_input", True),
        ready_for_future_vera_codex_trial_evidence=kwargs.pop("ready_for_future_vera_codex_trial_evidence", True),
        ready_for_future_cold_evaluation_evidence=kwargs.pop("ready_for_future_cold_evaluation_evidence", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_RESULT_FLAG_NAMES},
    )


def build_sandbox_test_result_source_ref(**kwargs: Any) -> SandboxTestResultSourceRef:
    return SandboxTestResultSourceRef(
        source_ref_id=kwargs.pop("source_ref_id", "sandbox_test_result_source_ref:v0.37.3"),
        source_kind=kwargs.pop("source_kind", SandboxTestResultSourceKind.V0372_SANDBOX_TEST_EXECUTION_RESULT),
        source_id=kwargs.pop("source_id", "v0.37.2"),
        source_summary=kwargs.pop("source_summary", "v0.37.2 supplied execution result metadata"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.2 execution result"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_result_policy(**kwargs: Any) -> SandboxTestResultEnvelopePolicy:
    return SandboxTestResultEnvelopePolicy(
        result_policy_id=kwargs.pop("result_policy_id", "sandbox_test_result_policy:v0.37.3"),
        version=kwargs.pop("version", V0373_VERSION),
        allowed_modes=kwargs.pop("allowed_modes", [
            SandboxTestResultEnvelopeMode.PROCESS_RESULT_ENVELOPE,
            SandboxTestResultEnvelopeMode.OUTPUT_CLASSIFIER_ENVELOPE,
            SandboxTestResultEnvelopeMode.COMBINED_RESULT_ENVELOPE,
            SandboxTestResultEnvelopeMode.EVIDENCE_ONLY_ENVELOPE,
        ]),
        max_stdout_chars=kwargs.pop("max_stdout_chars", 10000),
        max_stderr_chars=kwargs.pop("max_stderr_chars", 10000),
        max_evidence_snippet_chars=kwargs.pop("max_evidence_snippet_chars", 400),
        max_evidence_snippets=kwargs.pop("max_evidence_snippets", 8),
        require_redaction=kwargs.pop("require_redaction", True),
        require_confidence_level=kwargs.pop("require_confidence_level", True),
        allow_process_classification=kwargs.pop("allow_process_classification", True),
        allow_output_classification=kwargs.pop("allow_output_classification", True),
        allow_evidence_snippet_extraction=kwargs.pop("allow_evidence_snippet_extraction", True),
        allow_future_feedback_input=kwargs.pop("allow_future_feedback_input", True),
        allow_future_vera_codex_evidence=kwargs.pop("allow_future_vera_codex_evidence", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_POLICY_ALLOW_NAMES},
    )


def build_sandbox_test_result_envelope_input(**kwargs: Any) -> SandboxTestResultEnvelopeInput:
    return SandboxTestResultEnvelopeInput(
        envelope_input_id=kwargs.pop("envelope_input_id", "sandbox_test_result_envelope_input:v0.37.3"),
        version=kwargs.pop("version", V0373_VERSION),
        execution_result_id=kwargs.pop("execution_result_id", None),
        subprocess_result_id=kwargs.pop("subprocess_result_id", None),
        command_spec_id=kwargs.pop("command_spec_id", None),
        invocation_contract_id=kwargs.pop("invocation_contract_id", None),
        requested_mode=kwargs.pop("requested_mode", SandboxTestResultEnvelopeMode.COMBINED_RESULT_ENVELOPE),
        stdout_text=kwargs.pop("stdout_text", ""),
        stderr_text=kwargs.pop("stderr_text", ""),
        return_code=kwargs.pop("return_code", None),
        timed_out=kwargs.pop("timed_out", False),
        source_refs=kwargs.pop("source_refs", [build_sandbox_test_result_source_ref()]),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", ["test execution", "subprocess", "shell", "install", "network", "repair", "external agent", "Dominion"]),
        task_summary=kwargs.pop("task_summary", "classify supplied sandbox test result metadata"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_process_classification(**kwargs: Any) -> SandboxTestProcessClassification:
    return SandboxTestProcessClassification(
        process_classification_id=kwargs.pop("process_classification_id", "sandbox_test_process_classification:v0.37.3"),
        classification_kind=kwargs.pop("classification_kind", SandboxTestProcessClassificationKind.PROCESS_RESULT_UNKNOWN),
        return_code=kwargs.pop("return_code", None),
        timed_out=kwargs.pop("timed_out", False),
        process_summary=kwargs.pop("process_summary", "process-level classification only"),
        confidence=kwargs.pop("confidence", SandboxTestConfidenceLevel.INCONCLUSIVE),
        production_certified=kwargs.pop("production_certified", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_output_signal(**kwargs: Any) -> SandboxTestOutputSignal:
    return SandboxTestOutputSignal(
        output_signal_id=kwargs.pop("output_signal_id", "sandbox_test_output_signal:v0.37.3"),
        signal_kind=kwargs.pop("signal_kind", SandboxTestOutputSignalKind.UNKNOWN_SIGNAL),
        stream_kind=kwargs.pop("stream_kind", "combined"),
        signal_summary=kwargs.pop("signal_summary", "output signal metadata"),
        evidence_preview=kwargs.pop("evidence_preview", ""),
        confidence=kwargs.pop("confidence", SandboxTestConfidenceLevel.LOW),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_evidence_snippet(**kwargs: Any) -> SandboxTestEvidenceSnippet:
    return SandboxTestEvidenceSnippet(
        evidence_snippet_id=kwargs.pop("evidence_snippet_id", "sandbox_test_evidence_snippet:v0.37.3"),
        evidence_kind=kwargs.pop("evidence_kind", SandboxTestEvidenceKind.UNKNOWN),
        stream_kind=kwargs.pop("stream_kind", "combined"),
        snippet_text=kwargs.pop("snippet_text", ""),
        snippet_summary=kwargs.pop("snippet_summary", "bounded evidence snippet"),
        redacted=kwargs.pop("redacted", False),
        truncated=kwargs.pop("truncated", False),
        secret_like_content_detected=kwargs.pop("secret_like_content_detected", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_failure_classification(**kwargs: Any) -> SandboxTestFailureClassification:
    return SandboxTestFailureClassification(
        failure_classification_id=kwargs.pop("failure_classification_id", "sandbox_test_failure_classification:v0.37.3"),
        failure_class_kind=kwargs.pop("failure_class_kind", SandboxTestFailureClassKind.INCONCLUSIVE_FAILURE),
        failure_summary=kwargs.pop("failure_summary", "failure class is not root-cause certainty"),
        evidence_snippet_ids=kwargs.pop("evidence_snippet_ids", []),
        confidence=kwargs.pop("confidence", SandboxTestConfidenceLevel.INCONCLUSIVE),
        repair_allowed=kwargs.pop("repair_allowed", False),
        retry_allowed=kwargs.pop("retry_allowed", False),
        dependency_install_allowed=kwargs.pop("dependency_install_allowed", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_outcome_classification(**kwargs: Any) -> SandboxTestOutcomeClassification:
    return SandboxTestOutcomeClassification(
        outcome_classification_id=kwargs.pop("outcome_classification_id", "sandbox_test_outcome_classification:v0.37.3"),
        outcome_kind=kwargs.pop("outcome_kind", SandboxTestOutcomeKind.INCONCLUSIVE),
        outcome_summary=kwargs.pop("outcome_summary", "outcome classification is not production certification"),
        process_classification_id=kwargs.pop("process_classification_id", None),
        failure_classification_id=kwargs.pop("failure_classification_id", None),
        output_signal_ids=kwargs.pop("output_signal_ids", []),
        evidence_snippet_ids=kwargs.pop("evidence_snippet_ids", []),
        confidence=kwargs.pop("confidence", SandboxTestConfidenceLevel.INCONCLUSIVE),
        passed=kwargs.pop("passed", False),
        failed=kwargs.pop("failed", False),
        inconclusive=kwargs.pop("inconclusive", True),
        production_certified=kwargs.pop("production_certified", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_result_envelope(**kwargs: Any) -> SandboxTestResultEnvelope:
    process = kwargs.pop("process_classification", build_sandbox_test_process_classification())
    failure = kwargs.pop("failure_classification", build_sandbox_test_failure_classification())
    outcome = kwargs.pop("outcome_classification", build_sandbox_test_outcome_classification(
        process_classification_id=process.process_classification_id,
        failure_classification_id=failure.failure_classification_id,
    ))
    return SandboxTestResultEnvelope(
        result_envelope_id=kwargs.pop("result_envelope_id", "sandbox_test_result_envelope:v0.37.3"),
        version=kwargs.pop("version", V0373_VERSION),
        envelope_input_id=kwargs.pop("envelope_input_id", "sandbox_test_result_envelope_input:v0.37.3"),
        mode=kwargs.pop("mode", SandboxTestResultEnvelopeMode.COMBINED_RESULT_ENVELOPE),
        status=kwargs.pop("status", SandboxTestResultStatus.ENVELOPE_CREATED),
        readiness_level=kwargs.pop("readiness_level", SandboxTestResultReadinessLevel.FUTURE_FEEDBACK_INPUT_READY),
        process_classification=process,
        outcome_classification=outcome,
        failure_classification=failure,
        output_signals=kwargs.pop("output_signals", []),
        evidence_snippets=kwargs.pop("evidence_snippets", []),
        source_refs=kwargs.pop("source_refs", [build_sandbox_test_result_source_ref()]),
        summary=kwargs.pop("summary", "test result envelope created from supplied metadata"),
        eligible_for_future_feedback_report=kwargs.pop("eligible_for_future_feedback_report", True),
        eligible_for_future_vera_codex_trial=kwargs.pop("eligible_for_future_vera_codex_trial", True),
        eligible_for_future_cold_evaluation=kwargs.pop("eligible_for_future_cold_evaluation", True),
        test_execution_performed=kwargs.pop("test_execution_performed", False),
        subprocess_executed_by_v0373=kwargs.pop("subprocess_executed_by_v0373", False),
        repair_allowed=kwargs.pop("repair_allowed", False),
        retry_allowed=kwargs.pop("retry_allowed", False),
        dependency_install_allowed=kwargs.pop("dependency_install_allowed", False),
        production_certified=kwargs.pop("production_certified", False),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_result_envelope_decision(**kwargs: Any) -> SandboxTestResultEnvelopeDecision:
    return SandboxTestResultEnvelopeDecision(
        decision_id=kwargs.pop("decision_id", "sandbox_test_result_decision:v0.37.3"),
        envelope_input_id=kwargs.pop("envelope_input_id", "sandbox_test_result_envelope_input:v0.37.3"),
        decision_kind=kwargs.pop("decision_kind", SandboxTestResultDecisionKind.ALLOW_RESULT_ENVELOPE_CREATION),
        status=kwargs.pop("status", SandboxTestResultStatus.CLASSIFIED),
        risk_kinds=kwargs.pop("risk_kinds", [SandboxTestResultRiskKind.PROCESS_EXIT_OVERCLAIM_RISK]),
        decision_summary=kwargs.pop("decision_summary", "classification metadata allowed; execution remains blocked"),
        result_envelope_allowed=kwargs.pop("result_envelope_allowed", True),
        process_classification_allowed=kwargs.pop("process_classification_allowed", True),
        output_classification_allowed=kwargs.pop("output_classification_allowed", True),
        evidence_extraction_allowed=kwargs.pop("evidence_extraction_allowed", True),
        future_feedback_input_allowed=kwargs.pop("future_feedback_input_allowed", True),
        test_execution_allowed=kwargs.pop("test_execution_allowed", False),
        subprocess_allowed=kwargs.pop("subprocess_allowed", False),
        shell_allowed=kwargs.pop("shell_allowed", False),
        dependency_install_allowed=kwargs.pop("dependency_install_allowed", False),
        network_allowed=kwargs.pop("network_allowed", False),
        repair_allowed=kwargs.pop("repair_allowed", False),
        vera_codex_trial_execution_allowed=kwargs.pop("vera_codex_trial_execution_allowed", False),
        external_agent_allowed=kwargs.pop("external_agent_allowed", False),
        dominion_runtime_allowed=kwargs.pop("dominion_runtime_allowed", False),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.3 classifier"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_result_validation_finding(**kwargs: Any) -> SandboxTestResultValidationFinding:
    return SandboxTestResultValidationFinding(
        finding_id=kwargs.pop("finding_id", "sandbox_test_result_finding:v0.37.3"),
        risk_kind=kwargs.pop("risk_kind", SandboxTestResultRiskKind.UNKNOWN),
        severity=kwargs.pop("severity", "info"),
        message=kwargs.pop("message", "result validation finding"),
        blocks_envelope=kwargs.pop("blocks_envelope", False),
        evidence_refs=kwargs.pop("evidence_refs", []),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_result_validation_report(**kwargs: Any) -> SandboxTestResultValidationReport:
    return SandboxTestResultValidationReport(
        validation_report_id=kwargs.pop("validation_report_id", "sandbox_test_result_validation_report:v0.37.3"),
        version=kwargs.pop("version", V0373_VERSION),
        result_envelope_id=kwargs.pop("result_envelope_id", "sandbox_test_result_envelope:v0.37.3"),
        findings=kwargs.pop("findings", []),
        bounded_output_confirmed=kwargs.pop("bounded_output_confirmed", True),
        redaction_confirmed=kwargs.pop("redaction_confirmed", True),
        confidence_confirmed=kwargs.pop("confidence_confirmed", True),
        no_production_certification_confirmed=kwargs.pop("no_production_certification_confirmed", True),
        summary=kwargs.pop("summary", "result envelope validation confirms no execution or certification"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.3 validation"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_result_classifier_report(**kwargs: Any) -> SandboxTestResultClassifierReport:
    return SandboxTestResultClassifierReport(
        classifier_report_id=kwargs.pop("classifier_report_id", "sandbox_test_result_classifier_report:v0.37.3"),
        version=kwargs.pop("version", V0373_VERSION),
        result_envelope_id=kwargs.pop("result_envelope_id", "sandbox_test_result_envelope:v0.37.3"),
        classification_completed=kwargs.pop("classification_completed", True),
        report_summary=kwargs.pop("report_summary", "classification completed from supplied metadata only"),
        production_certified=kwargs.pop("production_certified", False),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.3 classifier"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_result_run_preview(**kwargs: Any) -> SandboxTestResultRunPreview:
    return SandboxTestResultRunPreview(
        run_preview_id=kwargs.pop("run_preview_id", "sandbox_test_result_run_preview:v0.37.3"),
        version=kwargs.pop("version", V0373_VERSION),
        envelope_input_id=kwargs.pop("envelope_input_id", "sandbox_test_result_envelope_input:v0.37.3"),
        preview_summary=kwargs.pop("preview_summary", "result classifier preview only"),
        ready_for_result_envelope=kwargs.pop("ready_for_result_envelope", True),
        ready_for_test_execution=kwargs.pop("ready_for_test_execution", False),
        ready_for_repair=kwargs.pop("ready_for_repair", False),
        ready_for_vera_codex_trial_execution=kwargs.pop("ready_for_vera_codex_trial_execution", False),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.3 preview"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_result_no_execution_guarantee(**kwargs: Any) -> SandboxTestResultNoExecutionGuarantee:
    no_names = tuple(name for name in SandboxTestResultNoExecutionGuarantee.__dataclass_fields__ if name.startswith("no_"))
    return SandboxTestResultNoExecutionGuarantee(
        guarantee_id=kwargs.pop("guarantee_id", "sandbox_test_result_no_execution_guarantee:v0.37.3"),
        version=kwargs.pop("version", V0373_VERSION),
        summary=kwargs.pop("summary", "v0.37.3 classifies supplied output only and executes nothing"),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, True) for name in no_names},
    )


def build_v0373_readiness_report(**kwargs: Any) -> V0373ReadinessReport:
    return V0373ReadinessReport(
        readiness_report_id=kwargs.pop("readiness_report_id", "v0373_readiness_report"),
        version=kwargs.pop("version", V0373_VERSION),
        readiness_level=kwargs.pop("readiness_level", SandboxTestResultReadinessLevel.DESIGN_HANDOFF_READY_FOR_V0374),
        status=kwargs.pop("status", SandboxTestResultStatus.ENVELOPE_CREATED),
        summary=kwargs.pop("summary", "v0.37.3 result envelope ready; execution remains false"),
        ready_for_v0374_test_feedback_failure_diagnosis=kwargs.pop("ready_for_v0374_test_feedback_failure_diagnosis", True),
        ready_for_v0375_repair_suggestion_metadata=kwargs.pop("ready_for_v0375_repair_suggestion_metadata", True),
        ready_for_v0376_vera_codex_one_shot_agent_trial=kwargs.pop("ready_for_v0376_vera_codex_one_shot_agent_trial", True),
        ready_for_v0377_cold_agent_performance_evaluation=kwargs.pop("ready_for_v0377_cold_agent_performance_evaluation", True),
        ready_for_test_result_envelope=kwargs.pop("ready_for_test_result_envelope", True),
        ready_for_test_output_classifier=kwargs.pop("ready_for_test_output_classifier", True),
        ready_for_process_exit_classification=kwargs.pop("ready_for_process_exit_classification", True),
        ready_for_test_failure_classification=kwargs.pop("ready_for_test_failure_classification", True),
        ready_for_test_evidence_snippets=kwargs.pop("ready_for_test_evidence_snippets", True),
        ready_for_future_feedback_report_input=kwargs.pop("ready_for_future_feedback_report_input", True),
        ready_for_future_vera_codex_trial_evidence=kwargs.pop("ready_for_future_vera_codex_trial_evidence", True),
        ready_for_future_cold_evaluation_evidence=kwargs.pop("ready_for_future_cold_evaluation_evidence", True),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        ready_for_test_execution=kwargs.pop("ready_for_test_execution", False),
        ready_for_controlled_test_subprocess=kwargs.pop("ready_for_controlled_test_subprocess", False),
        ready_for_shell_execution=kwargs.pop("ready_for_shell_execution", False),
        ready_for_subprocess_execution=kwargs.pop("ready_for_subprocess_execution", False),
        ready_for_command_execution=kwargs.pop("ready_for_command_execution", False),
        ready_for_dependency_install=kwargs.pop("ready_for_dependency_install", False),
        ready_for_network_access=kwargs.pop("ready_for_network_access", False),
        ready_for_automatic_repair=kwargs.pop("ready_for_automatic_repair", False),
        ready_for_multi_cycle_agentic_loop=kwargs.pop("ready_for_multi_cycle_agentic_loop", False),
        ready_for_vera_codex_trial_execution=kwargs.pop("ready_for_vera_codex_trial_execution", False),
        ready_for_cold_agent_performance_evaluation=kwargs.pop("ready_for_cold_agent_performance_evaluation", False),
        ready_for_external_agent_execution=kwargs.pop("ready_for_external_agent_execution", False),
        ready_for_dominion_runtime=kwargs.pop("ready_for_dominion_runtime", False),
        production_certified=kwargs.pop("production_certified", False),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.3 result envelope"]),
        metadata=kwargs.pop("metadata", {}),
    )


def default_sandbox_test_result_policy(**kwargs: Any) -> SandboxTestResultEnvelopePolicy:
    return build_sandbox_test_result_policy(**kwargs)


def bound_and_redact_result_text(text: str, limit: int) -> tuple[str, bool, bool]:
    limited, truncated = _limit_text(text, limit)
    redacted, redaction = _redact_secret_like(limited)
    return redacted, truncated, redaction


def build_test_result_envelope_input_from_execution_result(
    execution_result: SandboxTestExecutionResult,
    policy: SandboxTestResultEnvelopePolicy | None = None,
    **kwargs: Any,
) -> SandboxTestResultEnvelopeInput:
    policy = policy or default_sandbox_test_result_policy()
    subprocess_result = execution_result.subprocess_result
    stdout = subprocess_result.stdout_text if subprocess_result else ""
    stderr = subprocess_result.stderr_text if subprocess_result else ""
    stdout, _, _ = bound_and_redact_result_text(stdout, policy.max_stdout_chars)
    stderr, _, _ = bound_and_redact_result_text(stderr, policy.max_stderr_chars)
    return build_sandbox_test_result_envelope_input(
        execution_result_id=execution_result.execution_result_id,
        subprocess_result_id=subprocess_result.subprocess_result_id if subprocess_result else None,
        stdout_text=stdout,
        stderr_text=stderr,
        return_code=execution_result.return_code,
        timed_out=execution_result.timed_out,
        **kwargs,
    )


def classify_sandbox_test_process_result(envelope_input: SandboxTestResultEnvelopeInput) -> SandboxTestProcessClassification:
    if envelope_input.timed_out:
        return build_sandbox_test_process_classification(
            classification_kind=SandboxTestProcessClassificationKind.PROCESS_TIMEOUT,
            return_code=envelope_input.return_code,
            timed_out=True,
            process_summary="process timed out; retry is not allowed",
            confidence=SandboxTestConfidenceLevel.HIGH,
        )
    if envelope_input.return_code == 0:
        return build_sandbox_test_process_classification(
            classification_kind=SandboxTestProcessClassificationKind.PROCESS_EXIT_ZERO,
            return_code=0,
            process_summary="process exited zero; not production certification",
            confidence=SandboxTestConfidenceLevel.MEDIUM,
        )
    if envelope_input.return_code is None:
        return build_sandbox_test_process_classification(
            classification_kind=SandboxTestProcessClassificationKind.NOT_EXECUTED,
            return_code=None,
            process_summary="process was not executed or result missing",
            confidence=SandboxTestConfidenceLevel.LOW,
        )
    return build_sandbox_test_process_classification(
        classification_kind=SandboxTestProcessClassificationKind.PROCESS_EXIT_NONZERO,
        return_code=envelope_input.return_code,
        process_summary="process exited nonzero; repair is not allowed",
        confidence=SandboxTestConfidenceLevel.MEDIUM,
    )


def _signal(signal_kind: SandboxTestOutputSignalKind, stream_kind: str, evidence: str, confidence: SandboxTestConfidenceLevel) -> SandboxTestOutputSignal:
    preview, _, redacted = bound_and_redact_result_text(evidence, 240)
    return build_sandbox_test_output_signal(
        signal_kind=signal_kind,
        stream_kind=stream_kind,
        signal_summary=f"detected {signal_kind.value}",
        evidence_preview=preview if not redacted else preview,
        confidence=confidence,
    )


def detect_sandbox_test_output_signals(stdout_text: str, stderr_text: str) -> list[SandboxTestOutputSignal]:
    signals: list[SandboxTestOutputSignal] = []
    combined = _combined_text(stdout_text, stderr_text)
    lower = combined.lower()
    if " passed" in lower or " passed in " in lower:
        signals.append(_signal(SandboxTestOutputSignalKind.PYTEST_PASSED_SIGNAL, "stdout", combined, SandboxTestConfidenceLevel.MEDIUM))
    if lower.strip().endswith("ok") or "\nok" in lower:
        signals.append(_signal(SandboxTestOutputSignalKind.UNITTEST_OK_SIGNAL, "stdout", combined, SandboxTestConfidenceLevel.MEDIUM))
    if " failed" in lower or " failures" in lower:
        signals.append(_signal(SandboxTestOutputSignalKind.PYTEST_FAILED_SIGNAL, "combined", combined, SandboxTestConfidenceLevel.HIGH))
    if "fail:" in lower or "failed (" in lower:
        signals.append(_signal(SandboxTestOutputSignalKind.UNITTEST_FAILED_SIGNAL, "combined", combined, SandboxTestConfidenceLevel.HIGH))
    if " error" in lower or " errors" in lower:
        signals.append(_signal(SandboxTestOutputSignalKind.PYTEST_ERROR_SIGNAL, "combined", combined, SandboxTestConfidenceLevel.MEDIUM))
    if "traceback (most recent call last)" in lower:
        signals.append(_signal(SandboxTestOutputSignalKind.TRACEBACK_SIGNAL, "stderr", combined, SandboxTestConfidenceLevel.HIGH))
    if "assertionerror" in lower or "assert " in lower:
        signals.append(_signal(SandboxTestOutputSignalKind.ASSERTION_ERROR_SIGNAL, "combined", combined, SandboxTestConfidenceLevel.HIGH))
    if "importerror" in lower:
        signals.append(_signal(SandboxTestOutputSignalKind.IMPORT_ERROR_SIGNAL, "combined", combined, SandboxTestConfidenceLevel.HIGH))
    if "syntaxerror" in lower:
        signals.append(_signal(SandboxTestOutputSignalKind.SYNTAX_ERROR_SIGNAL, "combined", combined, SandboxTestConfidenceLevel.HIGH))
    if "modulenotfounderror" in lower or "no module named" in lower:
        signals.append(_signal(SandboxTestOutputSignalKind.MISSING_MODULE_SIGNAL, "combined", combined, SandboxTestConfidenceLevel.HIGH))
    if "no tests ran" in lower or "collected 0 items" in lower or "no tests collected" in lower:
        signals.append(_signal(SandboxTestOutputSignalKind.NO_TESTS_COLLECTED_SIGNAL, "combined", combined, SandboxTestConfidenceLevel.HIGH))
    if "timed out" in lower or "timeout" in lower:
        signals.append(_signal(SandboxTestOutputSignalKind.TIMEOUT_SIGNAL, "combined", combined, SandboxTestConfidenceLevel.HIGH))
    if "blocked" in lower and "command" in lower:
        signals.append(_signal(SandboxTestOutputSignalKind.COMMAND_BLOCKED_SIGNAL, "combined", combined, SandboxTestConfidenceLevel.HIGH))
    if any(marker.lower() in lower for marker in SECRET_MARKERS):
        signals.append(_signal(SandboxTestOutputSignalKind.SECRET_LIKE_OUTPUT_SIGNAL, "combined", combined, SandboxTestConfidenceLevel.HIGH))
    return signals or [_signal(SandboxTestOutputSignalKind.UNKNOWN_SIGNAL, "combined", combined, SandboxTestConfidenceLevel.INCONCLUSIVE)]


def _evidence_kind_for_signal(signal: SandboxTestOutputSignal) -> SandboxTestEvidenceKind:
    mapping = {
        SandboxTestOutputSignalKind.PYTEST_PASSED_SIGNAL.value: SandboxTestEvidenceKind.PYTEST_SUMMARY_LINE,
        SandboxTestOutputSignalKind.PYTEST_FAILED_SIGNAL.value: SandboxTestEvidenceKind.PYTEST_SUMMARY_LINE,
        SandboxTestOutputSignalKind.UNITTEST_OK_SIGNAL.value: SandboxTestEvidenceKind.UNITTEST_SUMMARY_LINE,
        SandboxTestOutputSignalKind.UNITTEST_FAILED_SIGNAL.value: SandboxTestEvidenceKind.UNITTEST_SUMMARY_LINE,
        SandboxTestOutputSignalKind.TRACEBACK_SIGNAL.value: SandboxTestEvidenceKind.TRACEBACK_EXCERPT,
        SandboxTestOutputSignalKind.IMPORT_ERROR_SIGNAL.value: SandboxTestEvidenceKind.IMPORT_ERROR_EXCERPT,
        SandboxTestOutputSignalKind.SYNTAX_ERROR_SIGNAL.value: SandboxTestEvidenceKind.SYNTAX_ERROR_EXCERPT,
        SandboxTestOutputSignalKind.ASSERTION_ERROR_SIGNAL.value: SandboxTestEvidenceKind.ASSERTION_ERROR_EXCERPT,
        SandboxTestOutputSignalKind.MISSING_MODULE_SIGNAL.value: SandboxTestEvidenceKind.MISSING_DEPENDENCY_EXCERPT,
        SandboxTestOutputSignalKind.COMMAND_BLOCKED_SIGNAL.value: SandboxTestEvidenceKind.COMMAND_BLOCKED_EXCERPT,
        SandboxTestOutputSignalKind.NO_TESTS_COLLECTED_SIGNAL.value: SandboxTestEvidenceKind.NO_TESTS_COLLECTED_EXCERPT,
        SandboxTestOutputSignalKind.SECRET_LIKE_OUTPUT_SIGNAL.value: SandboxTestEvidenceKind.REDACTION_NOTICE,
    }
    return mapping.get(_enum_value(signal.signal_kind), SandboxTestEvidenceKind.UNKNOWN)


def extract_sandbox_test_evidence_snippets(
    stdout_text: str,
    stderr_text: str,
    signals: list[SandboxTestOutputSignal] | None = None,
    policy: SandboxTestResultEnvelopePolicy | None = None,
) -> list[SandboxTestEvidenceSnippet]:
    policy = policy or default_sandbox_test_result_policy()
    signals = signals or detect_sandbox_test_output_signals(stdout_text, stderr_text)
    combined = _combined_text(stdout_text, stderr_text)
    snippets: list[SandboxTestEvidenceSnippet] = []
    for index, signal in enumerate(signals[: policy.max_evidence_snippets]):
        text, truncated, redacted = bound_and_redact_result_text(signal.evidence_preview or combined, policy.max_evidence_snippet_chars)
        redacted = redacted or "[REDACTED]" in text or _enum_value(signal.signal_kind) == SandboxTestOutputSignalKind.SECRET_LIKE_OUTPUT_SIGNAL.value
        snippets.append(build_sandbox_test_evidence_snippet(
            evidence_snippet_id=f"sandbox_test_evidence_snippet:{index}:v0.37.3",
            evidence_kind=_evidence_kind_for_signal(signal),
            stream_kind=signal.stream_kind,
            snippet_text=text,
            snippet_summary=f"bounded evidence for {signal.signal_kind}",
            redacted=redacted,
            truncated=truncated,
            secret_like_content_detected=redacted,
        ))
    return snippets


def classify_sandbox_test_failure(
    process_classification: SandboxTestProcessClassification,
    signals: list[SandboxTestOutputSignal],
    evidence_snippets: list[SandboxTestEvidenceSnippet],
) -> SandboxTestFailureClassification:
    kinds = {_enum_value(signal.signal_kind) for signal in signals}
    snippet_ids = [snippet.evidence_snippet_id for snippet in evidence_snippets]
    if SandboxTestProcessClassificationKind.PROCESS_TIMEOUT.value == _enum_value(process_classification.classification_kind) or SandboxTestOutputSignalKind.TIMEOUT_SIGNAL.value in kinds:
        return build_sandbox_test_failure_classification(failure_class_kind=SandboxTestFailureClassKind.TIMEOUT_FAILURE, failure_summary="timeout classified; retry not allowed", evidence_snippet_ids=snippet_ids, confidence=SandboxTestConfidenceLevel.HIGH)
    if SandboxTestOutputSignalKind.MISSING_MODULE_SIGNAL.value in kinds:
        return build_sandbox_test_failure_classification(failure_class_kind=SandboxTestFailureClassKind.MISSING_DEPENDENCY_FAILURE, failure_summary="missing dependency classified; install not allowed", evidence_snippet_ids=snippet_ids, confidence=SandboxTestConfidenceLevel.HIGH)
    if SandboxTestOutputSignalKind.IMPORT_ERROR_SIGNAL.value in kinds:
        return build_sandbox_test_failure_classification(failure_class_kind=SandboxTestFailureClassKind.IMPORT_FAILURE, failure_summary="import failure classified", evidence_snippet_ids=snippet_ids, confidence=SandboxTestConfidenceLevel.HIGH)
    if SandboxTestOutputSignalKind.SYNTAX_ERROR_SIGNAL.value in kinds:
        return build_sandbox_test_failure_classification(failure_class_kind=SandboxTestFailureClassKind.SYNTAX_FAILURE, failure_summary="syntax failure classified", evidence_snippet_ids=snippet_ids, confidence=SandboxTestConfidenceLevel.HIGH)
    if SandboxTestOutputSignalKind.ASSERTION_ERROR_SIGNAL.value in kinds or SandboxTestOutputSignalKind.PYTEST_FAILED_SIGNAL.value in kinds:
        return build_sandbox_test_failure_classification(failure_class_kind=SandboxTestFailureClassKind.ASSERTION_FAILURE, failure_summary="assertion/test failure classified; repair not allowed", evidence_snippet_ids=snippet_ids, confidence=SandboxTestConfidenceLevel.HIGH)
    if SandboxTestOutputSignalKind.COMMAND_BLOCKED_SIGNAL.value in kinds:
        return build_sandbox_test_failure_classification(failure_class_kind=SandboxTestFailureClassKind.COMMAND_BLOCKED_FAILURE, failure_summary="command blocked classified", evidence_snippet_ids=snippet_ids, confidence=SandboxTestConfidenceLevel.HIGH)
    if SandboxTestOutputSignalKind.SECRET_LIKE_OUTPUT_SIGNAL.value in kinds:
        return build_sandbox_test_failure_classification(failure_class_kind=SandboxTestFailureClassKind.UNSAFE_OUTPUT_FAILURE, failure_summary="secret-like output classified", evidence_snippet_ids=snippet_ids, confidence=SandboxTestConfidenceLevel.HIGH)
    if SandboxTestOutputSignalKind.NO_TESTS_COLLECTED_SIGNAL.value in kinds:
        return build_sandbox_test_failure_classification(failure_class_kind=SandboxTestFailureClassKind.COLLECTION_FAILURE, failure_summary="no tests collected classified", evidence_snippet_ids=snippet_ids, confidence=SandboxTestConfidenceLevel.HIGH)
    if SandboxTestProcessClassificationKind.PROCESS_EXIT_ZERO.value == _enum_value(process_classification.classification_kind):
        return build_sandbox_test_failure_classification(failure_class_kind=SandboxTestFailureClassKind.NO_FAILURE_DETECTED, failure_summary="no failure detected from supplied evidence", evidence_snippet_ids=snippet_ids, confidence=SandboxTestConfidenceLevel.MEDIUM)
    if SandboxTestProcessClassificationKind.PROCESS_EXIT_NONZERO.value == _enum_value(process_classification.classification_kind):
        return build_sandbox_test_failure_classification(failure_class_kind=SandboxTestFailureClassKind.RUNTIME_ERROR_FAILURE, failure_summary="nonzero process exit with limited evidence", evidence_snippet_ids=snippet_ids, confidence=SandboxTestConfidenceLevel.LOW)
    return build_sandbox_test_failure_classification(evidence_snippet_ids=snippet_ids)


def classify_sandbox_test_outcome(
    process_classification: SandboxTestProcessClassification,
    failure_classification: SandboxTestFailureClassification,
    signals: list[SandboxTestOutputSignal],
    evidence_snippets: list[SandboxTestEvidenceSnippet],
) -> SandboxTestOutcomeClassification:
    failure_kind = _enum_value(failure_classification.failure_class_kind)
    signal_values = {_enum_value(signal.signal_kind) for signal in signals}
    outcome = SandboxTestOutcomeKind.INCONCLUSIVE
    passed = failed = inconclusive = False
    confidence = failure_classification.confidence
    if failure_kind == SandboxTestFailureClassKind.NO_FAILURE_DETECTED.value and SandboxTestOutputSignalKind.PYTEST_PASSED_SIGNAL.value in signal_values:
        outcome, passed, confidence = SandboxTestOutcomeKind.PASSED, True, SandboxTestConfidenceLevel.MEDIUM
    elif failure_kind == SandboxTestFailureClassKind.ASSERTION_FAILURE.value:
        outcome, failed = SandboxTestOutcomeKind.FAILED_ASSERTION, True
    elif failure_kind == SandboxTestFailureClassKind.IMPORT_FAILURE.value:
        outcome, failed = SandboxTestOutcomeKind.IMPORT_ERROR, True
    elif failure_kind == SandboxTestFailureClassKind.SYNTAX_FAILURE.value:
        outcome, failed = SandboxTestOutcomeKind.SYNTAX_ERROR, True
    elif failure_kind == SandboxTestFailureClassKind.MISSING_DEPENDENCY_FAILURE.value:
        outcome, failed = SandboxTestOutcomeKind.MISSING_DEPENDENCY, True
    elif failure_kind == SandboxTestFailureClassKind.TIMEOUT_FAILURE.value:
        outcome, failed = SandboxTestOutcomeKind.TIMEOUT, True
    elif failure_kind == SandboxTestFailureClassKind.COMMAND_BLOCKED_FAILURE.value:
        outcome, failed = SandboxTestOutcomeKind.COMMAND_BLOCKED, True
    elif failure_kind == SandboxTestFailureClassKind.UNSAFE_OUTPUT_FAILURE.value:
        outcome, failed = SandboxTestOutcomeKind.UNSAFE_OUTPUT, True
    elif failure_kind == SandboxTestFailureClassKind.COLLECTION_FAILURE.value:
        outcome, failed = SandboxTestOutcomeKind.NO_TESTS_COLLECTED, True
    elif failure_kind == SandboxTestFailureClassKind.RUNTIME_ERROR_FAILURE.value:
        outcome, failed = SandboxTestOutcomeKind.FAILED, True
    else:
        inconclusive = True
        confidence = SandboxTestConfidenceLevel.INCONCLUSIVE
    return build_sandbox_test_outcome_classification(
        outcome_kind=outcome,
        outcome_summary=f"outcome classified as {outcome.value}; not production certification",
        process_classification_id=process_classification.process_classification_id,
        failure_classification_id=failure_classification.failure_classification_id,
        output_signal_ids=[signal.output_signal_id for signal in signals],
        evidence_snippet_ids=[snippet.evidence_snippet_id for snippet in evidence_snippets],
        confidence=confidence,
        passed=passed,
        failed=failed,
        inconclusive=inconclusive,
    )


def create_sandbox_test_result_envelope_from_execution_result(
    execution_result: SandboxTestExecutionResult,
    policy: SandboxTestResultEnvelopePolicy | None = None,
) -> SandboxTestResultEnvelope:
    envelope_input = build_test_result_envelope_input_from_execution_result(execution_result, policy)
    process = classify_sandbox_test_process_result(envelope_input)
    signals = detect_sandbox_test_output_signals(envelope_input.stdout_text, envelope_input.stderr_text)
    snippets = extract_sandbox_test_evidence_snippets(envelope_input.stdout_text, envelope_input.stderr_text, signals, policy)
    failure = classify_sandbox_test_failure(process, signals, snippets)
    outcome = classify_sandbox_test_outcome(process, failure, signals, snippets)
    return build_sandbox_test_result_envelope(
        envelope_input_id=envelope_input.envelope_input_id,
        process_classification=process,
        outcome_classification=outcome,
        failure_classification=failure,
        output_signals=signals,
        evidence_snippets=snippets,
        summary="result envelope created from supplied v0.37.2 metadata only",
    )


def validate_sandbox_test_result_envelope(envelope: SandboxTestResultEnvelope) -> SandboxTestResultValidationReport:
    findings: list[SandboxTestResultValidationFinding] = []
    if envelope.production_certified:
        findings.append(build_sandbox_test_result_validation_finding(risk_kind=SandboxTestResultRiskKind.PRODUCTION_CERTIFICATION_CONFUSION_RISK, severity="block", message="production certification is not allowed", blocks_envelope=True))
    if envelope.repair_allowed:
        findings.append(build_sandbox_test_result_validation_finding(risk_kind=SandboxTestResultRiskKind.FAILURE_REPAIR_CONFUSION_RISK, severity="block", message="repair is not allowed", blocks_envelope=True))
    return build_sandbox_test_result_validation_report(
        result_envelope_id=envelope.result_envelope_id,
        findings=findings,
        summary="result envelope validation report",
    )


def sandbox_test_result_flags_preserve_no_execution(flags: SandboxTestResultFlagSet) -> bool:
    return isinstance(flags, SandboxTestResultFlagSet) and all(getattr(flags, name) is False for name in UNSAFE_RESULT_FLAG_NAMES)


def sandbox_test_result_policy_blocks_execution(policy: SandboxTestResultEnvelopePolicy) -> bool:
    return isinstance(policy, SandboxTestResultEnvelopePolicy) and all(getattr(policy, name) is False for name in UNSAFE_POLICY_ALLOW_NAMES)


def sandbox_test_result_envelope_is_not_execution(envelope: SandboxTestResultEnvelope) -> bool:
    return (
        isinstance(envelope, SandboxTestResultEnvelope)
        and envelope.test_execution_performed is False
        and envelope.subprocess_executed_by_v0373 is False
        and envelope.ready_for_execution is False
    )


def sandbox_test_failure_classification_blocks_repair(classification: SandboxTestFailureClassification) -> bool:
    return isinstance(classification, SandboxTestFailureClassification) and not classification.repair_allowed and not classification.retry_allowed and not classification.dependency_install_allowed


def sandbox_test_outcome_is_not_production_certification(outcome: SandboxTestOutcomeClassification) -> bool:
    return isinstance(outcome, SandboxTestOutcomeClassification) and outcome.production_certified is False


def v0373_readiness_report_is_not_execution_ready(report: V0373ReadinessReport) -> bool:
    if not isinstance(report, V0373ReadinessReport):
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
            "ready_for_automatic_repair",
            "ready_for_multi_cycle_agentic_loop",
            "ready_for_vera_codex_trial_execution",
            "ready_for_cold_agent_performance_evaluation",
            "ready_for_external_agent_execution",
            "ready_for_dominion_runtime",
            "production_certified",
        )
    )
