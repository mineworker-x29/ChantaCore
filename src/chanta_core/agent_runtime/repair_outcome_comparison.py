"""v0.39.5 before/after repair outcome comparison metadata.

This module compares supplied before/after test result metadata only. It does
not run tests, invoke a controlled runner, read or write files, apply patches,
roll back changes, execute repair, reconstruct process state, write traces,
generate prompts, invoke agents/providers, run loops, start Dominion runtime,
or certify production readiness.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank


V0395_VERSION = "v0.39.5"
V0395_RELEASE_NAME = "v0.39.5 Before / After Repair Outcome Comparison"
V039_TRACK_NAME = "Human-approved Sandbox Repair Apply & Re-test Loop with PI-native Self-Prompting Mission Loop Boundary"

PROHIBITED_RUNTIME_ACTIONS = [
    "test_execution",
    "controlled_runner_invocation",
    "shell",
    "subprocess",
    "command_execution",
    "apply_patch",
    "git_apply",
    "rollback_execution",
    "repair_execution",
    "self_prompt_execution",
    "subagent_invocation",
    "model_provider",
    "external_agent",
    "Dominion",
]


class RepairOutcomeComparisonMode(StrEnum):
    BEFORE_AFTER_REPAIR_OUTCOME_COMPARISON = "before_after_repair_outcome_comparison"
    BEFORE_AFTER_TEST_PAIRING = "before_after_test_pairing"
    TEST_OUTCOME_DELTA_ANALYSIS = "test_outcome_delta_analysis"
    FAILURE_DELTA_ASSESSMENT = "failure_delta_assessment"
    REGRESSION_SIGNAL_DETECTION = "regression_signal_detection"
    RESIDUAL_FAILURE_ASSESSMENT = "residual_failure_assessment"
    REPAIR_EFFECTIVENESS_ASSESSMENT = "repair_effectiveness_assessment"
    DO_NOTHING_AFTER_APPLY_COMPARISON = "do_nothing_after_apply_comparison"
    FUTURE_PROCESS_STATE_RECONSTRUCTION_INPUT = "future_process_state_reconstruction_input"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairOutcomeComparisonSourceKind(StrEnum):
    V0394_POST_APPLY_RETEST_RESULT = "v0394_post_apply_retest_result"
    V0394_POST_APPLY_RETEST_RUN_RECORD = "v0394_post_apply_retest_run_record"
    V0394_POST_APPLY_OUTPUT_CAPTURE = "v0394_post_apply_output_capture"
    V0394_POST_APPLY_RETEST_AUDIT = "v0394_post_apply_retest_audit"
    V0394_READINESS_REPORT = "v0394_readiness_report"
    V0393_SANDBOX_APPLY_RESULT = "v0393_sandbox_apply_result"
    V0393_SANDBOX_APPLY_TRANSACTION = "v0393_sandbox_apply_transaction"
    V0393_SANDBOX_APPLY_AUDIT = "v0393_sandbox_apply_audit"
    V0373_BEFORE_TEST_RESULT_ENVELOPE = "v0373_before_test_result_envelope"
    V0374_BEFORE_TEST_FEEDBACK_REPORT = "v0374_before_test_feedback_report"
    V0374_FAILURE_DIAGNOSIS_REPORT = "v0374_failure_diagnosis_report"
    V0381_REPAIR_EVIDENCE_BUNDLE = "v0381_repair_evidence_bundle"
    V0384_PROPOSED_PATCH_ENVELOPE = "v0384_proposed_patch_envelope"
    V0385_SAFETY_REPORT = "v0385_safety_report"
    SUPPLIED_BEFORE_TEST_RESULT = "supplied_before_test_result"
    SUPPLIED_AFTER_TEST_RESULT = "supplied_after_test_result"
    MANUAL_OPERATOR_NOTE = "manual_operator_note"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class RepairOutcomeComparisonStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    INPUT_VALIDATED = "input_validated"
    BEFORE_AFTER_PAIR_CREATED = "before_after_pair_created"
    OUTCOME_DELTA_CREATED = "outcome_delta_created"
    FAILURE_DELTA_ASSESSED = "failure_delta_assessed"
    REGRESSION_SIGNALS_DETECTED = "regression_signals_detected"
    RESIDUAL_FAILURES_ASSESSED = "residual_failures_assessed"
    EFFECTIVENESS_ASSESSED = "effectiveness_assessed"
    DO_NOTHING_COMPARED = "do_nothing_compared"
    COMPARISON_COMPLETED = "comparison_completed"
    COMPARISON_COMPLETED_WITH_WARNINGS = "comparison_completed_with_warnings"
    COMPARISON_INCONCLUSIVE = "comparison_inconclusive"
    READY_FOR_FUTURE_PROCESS_STATE_RECONSTRUCTION = "ready_for_future_process_state_reconstruction"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    REVIEW_REQUIRED = "review_required"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class RepairOutcomeComparisonReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    BEFORE_AFTER_PAIR_READY = "before_after_pair_ready"
    TEST_OUTCOME_DELTA_READY = "test_outcome_delta_ready"
    FAILURE_DELTA_READY = "failure_delta_ready"
    REGRESSION_SIGNAL_READY = "regression_signal_ready"
    RESIDUAL_FAILURE_ASSESSMENT_READY = "residual_failure_assessment_ready"
    REPAIR_EFFECTIVENESS_ASSESSMENT_READY = "repair_effectiveness_assessment_ready"
    DO_NOTHING_AFTER_APPLY_COMPARISON_READY = "do_nothing_after_apply_comparison_ready"
    FUTURE_PROCESS_STATE_RECONSTRUCTION_INPUT_READY = "future_process_state_reconstruction_input_ready"
    DESIGN_HANDOFF_READY_FOR_V0396 = "design_handoff_ready_for_v0396"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class RepairOutcomeComparisonDecisionKind(StrEnum):
    ALLOW_BEFORE_AFTER_PAIRING = "allow_before_after_pairing"
    ALLOW_TEST_OUTCOME_DELTA = "allow_test_outcome_delta"
    ALLOW_FAILURE_DELTA_ASSESSMENT = "allow_failure_delta_assessment"
    ALLOW_REGRESSION_SIGNAL_DETECTION = "allow_regression_signal_detection"
    ALLOW_RESIDUAL_FAILURE_ASSESSMENT = "allow_residual_failure_assessment"
    ALLOW_REPAIR_EFFECTIVENESS_ASSESSMENT = "allow_repair_effectiveness_assessment"
    ALLOW_DO_NOTHING_AFTER_APPLY_COMPARISON = "allow_do_nothing_after_apply_comparison"
    ALLOW_FUTURE_PROCESS_STATE_RECONSTRUCTION_INPUT = "allow_future_process_state_reconstruction_input"
    CHOOSE_EFFECTIVE_REPAIR_CANDIDATE = "choose_effective_repair_candidate"
    CHOOSE_PARTIALLY_EFFECTIVE_REPAIR_CANDIDATE = "choose_partially_effective_repair_candidate"
    CHOOSE_INEFFECTIVE_REPAIR_CANDIDATE = "choose_ineffective_repair_candidate"
    CHOOSE_REGRESSIVE_REPAIR_CANDIDATE = "choose_regressive_repair_candidate"
    CHOOSE_INCONCLUSIVE = "choose_inconclusive"
    CHOOSE_DO_NOTHING = "choose_do_nothing"
    CHOOSE_HUMAN_REVIEW_REQUIRED = "choose_human_review_required"
    DENY = "deny"
    BLOCK = "block"
    REJECT_MISSING_BEFORE_RESULT = "reject_missing_before_result"
    REJECT_MISSING_AFTER_RESULT = "reject_missing_after_result"
    REJECT_INVALID_AFTER_RESULT = "reject_invalid_after_result"
    REJECT_UNCONTROLLED_AFTER_RESULT = "reject_uncontrolled_after_result"
    REJECT_SANDBOX_APPLY_MISSING = "reject_sandbox_apply_missing"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class RepairOutcomeComparisonRiskKind(StrEnum):
    MISSING_BEFORE_RESULT_RISK = "missing_before_result_risk"
    MISSING_AFTER_RESULT_RISK = "missing_after_result_risk"
    UNCONTROLLED_AFTER_TEST_RISK = "uncontrolled_after_test_risk"
    FAILED_SANDBOX_APPLY_RISK = "failed_sandbox_apply_risk"
    INCOMPARABLE_TEST_SCOPE_RISK = "incomparable_test_scope_risk"
    CHANGED_TEST_SELECTION_RISK = "changed_test_selection_risk"
    INSUFFICIENT_TEST_COVERAGE_RISK = "insufficient_test_coverage_risk"
    FLAKY_TEST_RISK = "flaky_test_risk"
    TIMEOUT_INCONCLUSIVE_RISK = "timeout_inconclusive_risk"
    OUTPUT_TRUNCATION_RISK = "output_truncation_risk"
    FALSE_POSITIVE_PASS_RISK = "false_positive_pass_risk"
    FALSE_NEGATIVE_FAIL_RISK = "false_negative_fail_risk"
    REGRESSION_RISK = "regression_risk"
    NEW_FAILURE_RISK = "new_failure_risk"
    RESIDUAL_FAILURE_RISK = "residual_failure_risk"
    REPAIR_CORRECTNESS_OVERCLAIM_RISK = "repair_correctness_overclaim_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    AUTOMATIC_ROLLBACK_CONFUSION_RISK = "automatic_rollback_confusion_risk"
    AUTOMATIC_REPAIR_CONFUSION_RISK = "automatic_repair_confusion_risk"
    RETRY_LOOP_RISK = "retry_loop_risk"
    MULTI_CYCLE_LOOP_RISK = "multi_cycle_loop_risk"
    SELF_PROMPT_EXECUTION_CONFUSION_RISK = "self_prompt_execution_confusion_risk"
    SUBAGENT_INVOCATION_CONFUSION_RISK = "subagent_invocation_confusion_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    MODEL_PROVIDER_INVOCATION_RISK = "model_provider_invocation_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    UNKNOWN = "unknown"


class RepairTestOutcomeKind(StrEnum):
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    TIMED_OUT = "timed_out"
    SKIPPED = "skipped"
    BLOCKED = "blocked"
    RUNNER_UNAVAILABLE = "runner_unavailable"
    INCONCLUSIVE = "inconclusive"
    NO_RESULT = "no_result"
    UNKNOWN = "unknown"


class RepairTestOutcomeDeltaKind(StrEnum):
    FAIL_TO_PASS = "fail_to_pass"
    FAIL_TO_FAIL = "fail_to_fail"
    PASS_TO_PASS = "pass_to_pass"
    PASS_TO_FAIL = "pass_to_fail"
    ERROR_TO_PASS = "error_to_pass"
    ERROR_TO_FAIL = "error_to_fail"
    TIMEOUT_TO_PASS = "timeout_to_pass"
    TIMEOUT_TO_FAIL = "timeout_to_fail"
    TIMEOUT_TO_TIMEOUT = "timeout_to_timeout"
    NO_BEFORE_RESULT = "no_before_result"
    NO_AFTER_RESULT = "no_after_result"
    INCOMPARABLE = "incomparable"
    INCONCLUSIVE = "inconclusive"
    UNKNOWN = "unknown"


class RepairFailureDeltaKind(StrEnum):
    FAILURE_RESOLVED = "failure_resolved"
    FAILURE_REDUCED = "failure_reduced"
    FAILURE_UNCHANGED = "failure_unchanged"
    FAILURE_WORSENED = "failure_worsened"
    NEW_FAILURE_INTRODUCED = "new_failure_introduced"
    TIMEOUT_RESOLVED = "timeout_resolved"
    TIMEOUT_INTRODUCED = "timeout_introduced"
    ERROR_RESOLVED = "error_resolved"
    ERROR_INTRODUCED = "error_introduced"
    RESIDUAL_FAILURE_PRESENT = "residual_failure_present"
    NO_FAILURE_BEFORE = "no_failure_before"
    NO_FAILURE_AFTER = "no_failure_after"
    INCOMPARABLE = "incomparable"
    INCONCLUSIVE = "inconclusive"
    UNKNOWN = "unknown"


class RepairRegressionSignalKind(StrEnum):
    NO_REGRESSION_DETECTED = "no_regression_detected"
    NEW_FAILED_TEST = "new_failed_test"
    NEW_ERROR = "new_error"
    NEW_TIMEOUT = "new_timeout"
    INCREASED_FAILURE_COUNT = "increased_failure_count"
    DECREASED_PASS_COUNT = "decreased_pass_count"
    OUTPUT_REGRESSION_SIGNAL = "output_regression_signal"
    FLAKY_OR_INCONCLUSIVE_SIGNAL = "flaky_or_inconclusive_signal"
    SCOPE_CHANGED_SIGNAL = "scope_changed_signal"
    INSUFFICIENT_DATA = "insufficient_data"
    UNKNOWN = "unknown"


class RepairEffectivenessKind(StrEnum):
    EFFECTIVE_CANDIDATE = "effective_candidate"
    PARTIALLY_EFFECTIVE_CANDIDATE = "partially_effective_candidate"
    INEFFECTIVE_CANDIDATE = "ineffective_candidate"
    REGRESSIVE_CANDIDATE = "regressive_candidate"
    INCONCLUSIVE_CANDIDATE = "inconclusive_candidate"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairOutcomeComparisonDisposition(StrEnum):
    COMPARISON_COMPLETED = "comparison_completed"
    COMPARISON_COMPLETED_WITH_WARNINGS = "comparison_completed_with_warnings"
    EFFECTIVE_CANDIDATE = "effective_candidate"
    PARTIALLY_EFFECTIVE_CANDIDATE = "partially_effective_candidate"
    INEFFECTIVE_CANDIDATE = "ineffective_candidate"
    REGRESSIVE_CANDIDATE = "regressive_candidate"
    INCONCLUSIVE = "inconclusive"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    REVIEW_REQUIRED = "review_required"
    DO_NOTHING_PREFERRED = "do_nothing_preferred"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairOutcomeConfidenceLevel(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INCONCLUSIVE = "inconclusive"
    UNKNOWN = "unknown"


class RepairOutcomeDoNothingComparisonKind(StrEnum):
    REPAIR_OUTPERFORMS_DO_NOTHING = "repair_outperforms_do_nothing"
    REPAIR_PARTIALLY_OUTPERFORMS_DO_NOTHING = "repair_partially_outperforms_do_nothing"
    DO_NOTHING_PREFERRED_DUE_TO_REGRESSION = "do_nothing_preferred_due_to_regression"
    DO_NOTHING_PREFERRED_DUE_TO_INCONCLUSIVE_RESULT = "do_nothing_preferred_due_to_inconclusive_result"
    DO_NOTHING_COMPETITIVE_DUE_TO_LOW_COVERAGE = "do_nothing_competitive_due_to_low_coverage"
    DO_NOTHING_REQUIRED_DUE_TO_BLOCKING_ISSUE = "do_nothing_required_due_to_blocking_issue"
    DO_NOTHING_NOT_EVALUABLE_YET = "do_nothing_not_evaluable_yet"
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
    "allow_test_execution",
    "allow_controlled_retest_execution",
    "allow_arbitrary_command_execution",
    "allow_shell",
    "allow_raw_subprocess",
    "allow_dependency_install",
    "allow_network_access",
    "allow_patch_materialization",
    "allow_patch_application",
    "allow_apply_patch",
    "allow_git_apply",
    "allow_rollback_execution",
    "allow_repair_execution",
    "allow_process_state_reconstruction",
    "allow_ocel_event_write",
    "allow_ocpx_state_persistence",
    "allow_pig_recommendation_execution",
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
    "allow_dominion_runtime",
]

UNSAFE_DECISION_NAMES = [
    "test_execution_allowed_now",
    "controlled_retest_allowed_now",
    "arbitrary_command_allowed_now",
    "shell_allowed_now",
    "raw_subprocess_allowed_now",
    "patch_apply_allowed_now",
    "rollback_execution_allowed_now",
    "before_after_comparison_rerun_allowed_now",
    "repair_execution_allowed_now",
    "process_state_reconstruction_allowed_now",
    "ocel_event_write_allowed_now",
    "ocpx_state_persistence_allowed_now",
    "pig_recommendation_execution_allowed_now",
    "self_prompt_generation_allowed_now",
    "self_prompt_execution_allowed_now",
    "subagent_invocation_allowed_now",
    "model_provider_invocation_allowed_now",
    "external_agent_allowed_now",
    "dominion_runtime_allowed_now",
    "production_certified",
]

UNSAFE_REPORT_NAMES = [
    "correctness_proven",
    "production_certified",
    "tests_run_by_v0395",
    "patches_applied_by_v0395",
    "rollback_executed_by_v0395",
    "repair_executed_by_v0395",
    "self_prompt_generated",
    "self_prompt_executed",
    "next_action_generated",
    "next_action_executed",
    "subagent_invoked",
    "model_invoked",
    "external_agent_invoked",
    "dominion_runtime_invoked",
    "ready_for_execution",
]

UNSAFE_READINESS_REPORT_NAMES = [
    "tests_run_enabled",
    "controlled_retest_enabled",
    "patch_apply_enabled",
    "rollback_execution_enabled",
    "repair_execution_enabled",
    "process_state_reconstruction_enabled",
    "ocel_event_write_enabled",
    "ocpx_persistence_enabled",
    "pig_recommendation_execution_enabled",
    "self_prompt_generation_enabled",
    "self_prompt_execution_enabled",
    "next_action_generation_enabled",
    "next_action_execution_enabled",
    "subagent_invocation_enabled",
    "model_invocation_enabled",
    "external_agent_enabled",
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
    if V0395_VERSION not in version:
        raise ValueError("version must include v0.39.5")


def _validate_list(field_name: str, value: Any) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{field_name} must be a list")


def _validate_dict(field_name: str, value: Any) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{field_name} must be a dict")


def _validate_false(instance: object, names: list[str]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must remain False in v0.39.5")


def _validate_true(instance: object, names: list[str]) -> None:
    for name in names:
        if getattr(instance, name) is not True:
            raise ValueError(f"{name} must be True")


def _bounded(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "...[truncated]"


def _fail_refs(snapshot: "RepairTestOutcomeSnapshot") -> set[str]:
    return set(snapshot.failed_test_refs) | set(snapshot.errored_test_refs)


@dataclass(frozen=True)
class RepairOutcomeComparisonFlagSet:
    flag_set_id: str
    version: str
    outcome_comparison_layer_constructed: bool = True
    before_after_pairing_available: bool = True
    test_outcome_delta_available: bool = True
    failure_delta_assessment_available: bool = True
    regression_signal_detection_available: bool = True
    residual_failure_assessment_available: bool = True
    repair_effectiveness_assessment_available: bool = True
    do_nothing_after_apply_comparison_available: bool = True
    future_process_state_reconstruction_input_available: bool = True
    ready_for_v0396_pi_native_repair_process_state_reconstruction: bool = True
    ready_for_before_after_repair_comparison: bool = True
    ready_for_before_after_test_pairing: bool = True
    ready_for_test_outcome_delta_analysis: bool = True
    ready_for_failure_delta_assessment: bool = True
    ready_for_regression_signal_detection: bool = True
    ready_for_residual_failure_assessment: bool = True
    ready_for_repair_effectiveness_assessment: bool = True
    ready_for_do_nothing_after_apply_comparison: bool = True
    ready_for_future_process_state_reconstruction_input: bool = True
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
class RepairOutcomeComparisonSourceRef:
    source_ref_id: str
    source_kind: RepairOutcomeComparisonSourceKind | str
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
class RepairOutcomeComparisonPolicy:
    policy_id: str
    version: str
    allowed_modes: list[RepairOutcomeComparisonMode | str]
    allowed_outcome_kinds: list[RepairTestOutcomeKind | str]
    max_test_refs: int = 200
    max_output_preview_chars: int = 4000
    require_before_result: bool = True
    require_after_result: bool = True
    require_controlled_after_result: bool = True
    require_sandbox_apply_result: bool = True
    require_comparable_test_scope: bool = True
    require_do_nothing_comparison: bool = True
    allow_before_after_pairing: bool = True
    allow_test_outcome_delta_analysis: bool = True
    allow_failure_delta_assessment: bool = True
    allow_regression_signal_detection: bool = True
    allow_residual_failure_assessment: bool = True
    allow_repair_effectiveness_assessment: bool = True
    allow_do_nothing_after_apply_comparison: bool = True
    allow_future_process_state_reconstruction_input: bool = True
    allow_test_execution: bool = False
    allow_controlled_retest_execution: bool = False
    allow_arbitrary_command_execution: bool = False
    allow_shell: bool = False
    allow_raw_subprocess: bool = False
    allow_dependency_install: bool = False
    allow_network_access: bool = False
    allow_patch_materialization: bool = False
    allow_patch_application: bool = False
    allow_apply_patch: bool = False
    allow_git_apply: bool = False
    allow_rollback_execution: bool = False
    allow_repair_execution: bool = False
    allow_process_state_reconstruction: bool = False
    allow_ocel_event_write: bool = False
    allow_ocpx_state_persistence: bool = False
    allow_pig_recommendation_execution: bool = False
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
    allow_dominion_runtime: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_id", self.policy_id)
        _validate_version(self.version)
        _validate_list("allowed_modes", self.allowed_modes)
        _validate_list("allowed_outcome_kinds", self.allowed_outcome_kinds)
        if self.max_test_refs <= 0 or self.max_output_preview_chars <= 0:
            raise ValueError("numeric limits must be > 0")
        _validate_dict("metadata", self.metadata)
        _validate_false(self, UNSAFE_POLICY_ALLOW_NAMES)


@dataclass(frozen=True)
class RepairOutcomeComparisonInput:
    comparison_input_id: str
    version: str
    before_test_result_id: str | None
    after_retest_result_id: str | None
    sandbox_apply_result_id: str | None
    sandbox_apply_transaction_id: str | None
    before_feedback_report_id: str | None
    after_output_capture_id: str | None
    proposed_patch_envelope_id: str | None
    safety_report_id: str | None
    requested_mode: RepairOutcomeComparisonMode | str
    source_refs: list[RepairOutcomeComparisonSourceRef]
    prohibited_runtime_actions: list[str]
    task_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("comparison_input_id", self.comparison_input_id)
        _validate_version(self.version)
        _require_non_blank("task_summary", self.task_summary)
        _validate_list("source_refs", self.source_refs)
        _validate_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_dict("metadata", self.metadata)
        for action in PROHIBITED_RUNTIME_ACTIONS:
            if action not in self.prohibited_runtime_actions:
                raise ValueError(f"prohibited_runtime_actions must include {action}")


@dataclass(frozen=True)
class RepairTestOutcomeSnapshot:
    outcome_snapshot_id: str
    version: str
    source_result_id: str | None
    phase_label: str
    outcome_kind: RepairTestOutcomeKind | str
    selected_test_refs: list[str]
    passed_test_refs: list[str]
    failed_test_refs: list[str]
    errored_test_refs: list[str]
    skipped_test_refs: list[str]
    timed_out: bool
    runner_unavailable: bool
    output_digest: str | None
    output_preview: str
    bounded: bool
    redacted: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["outcome_snapshot_id", "version", "phase_label", "output_preview"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ["selected_test_refs", "passed_test_refs", "failed_test_refs", "errored_test_refs", "skipped_test_refs"]:
            _validate_list(name, getattr(self, name))
        _validate_dict("metadata", self.metadata)
        if not self.bounded or not self.redacted:
            raise ValueError("outcome snapshot must be bounded and redacted")


@dataclass(frozen=True)
class RepairBeforeAfterOutcomePair:
    outcome_pair_id: str
    version: str
    before_snapshot: RepairTestOutcomeSnapshot | None
    after_snapshot: RepairTestOutcomeSnapshot | None
    comparable_test_refs: list[str]
    before_only_test_refs: list[str]
    after_only_test_refs: list[str]
    scope_changed: bool
    pair_summary: str
    pair_complete: bool
    pair_comparable: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("outcome_pair_id", self.outcome_pair_id)
        _validate_version(self.version)
        _require_non_blank("pair_summary", self.pair_summary)
        for name in ["comparable_test_refs", "before_only_test_refs", "after_only_test_refs", "evidence_refs"]:
            _validate_list(name, getattr(self, name))
        _validate_dict("metadata", self.metadata)
        if self.pair_complete and (self.before_snapshot is None or self.after_snapshot is None):
            raise ValueError("pair_complete requires before and after snapshots")
        if self.pair_comparable and (not self.pair_complete or self.scope_changed or not self.comparable_test_refs):
            raise ValueError("pair_comparable requires complete comparable scope")


@dataclass(frozen=True)
class RepairTestOutcomeDelta:
    outcome_delta_id: str
    version: str
    outcome_pair_id: str
    delta_kind: RepairTestOutcomeDeltaKind | str
    before_outcome: RepairTestOutcomeKind | str
    after_outcome: RepairTestOutcomeKind | str
    passed_count_delta: int
    failed_count_delta: int
    error_count_delta: int
    skipped_count_delta: int
    delta_summary: str
    improved: bool
    worsened: bool
    inconclusive: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["outcome_delta_id", "version", "outcome_pair_id", "delta_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairFailureDeltaAssessment:
    failure_delta_id: str
    version: str
    outcome_pair_id: str
    failure_delta_kinds: list[RepairFailureDeltaKind | str]
    resolved_failure_refs: list[str]
    residual_failure_refs: list[str]
    new_failure_refs: list[str]
    worsened_failure_refs: list[str]
    failure_delta_summary: str
    residual_failures_present: bool
    new_failures_present: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["failure_delta_id", "version", "outcome_pair_id", "failure_delta_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ["failure_delta_kinds", "resolved_failure_refs", "residual_failure_refs", "new_failure_refs", "worsened_failure_refs", "evidence_refs"]:
            _validate_list(name, getattr(self, name))
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairRegressionSignal:
    regression_signal_id: str
    version: str
    outcome_pair_id: str
    signal_kinds: list[RepairRegressionSignalKind | str]
    signal_summary: str
    regression_detected: bool
    new_failure_detected: bool
    timeout_regression_detected: bool
    scope_change_detected: bool
    output_regression_detected: bool
    confidence: RepairOutcomeConfidenceLevel | str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["regression_signal_id", "version", "outcome_pair_id", "signal_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("signal_kinds", self.signal_kinds)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairEffectivenessAssessment:
    effectiveness_assessment_id: str
    version: str
    outcome_pair_id: str
    effectiveness_kind: RepairEffectivenessKind | str
    effectiveness_summary: str
    confidence: RepairOutcomeConfidenceLevel | str
    effective_candidate: bool
    partially_effective_candidate: bool
    ineffective_candidate: bool
    regressive_candidate: bool
    inconclusive_candidate: bool
    correctness_proven: bool = False
    production_certified: bool = False
    human_review_required: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["effectiveness_assessment_id", "version", "outcome_pair_id", "effectiveness_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        if self.correctness_proven or self.production_certified:
            raise ValueError("effectiveness assessment is not correctness proof or production certification")
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairOutcomeDoNothingComparison:
    do_nothing_comparison_id: str
    version: str
    comparison_kind: RepairOutcomeDoNothingComparisonKind | str
    comparison_summary: str
    do_nothing_remains_valid: bool
    do_nothing_preferred: bool
    do_nothing_required: bool
    repair_outperforms_do_nothing: bool
    confidence: RepairOutcomeConfidenceLevel | str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("do_nothing_comparison_id", self.do_nothing_comparison_id)
        _validate_version(self.version)
        _require_non_blank("comparison_summary", self.comparison_summary)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairOutcomeComparisonAudit:
    audit_id: str
    version: str
    comparison_input_id: str
    audit_summary: str
    before_result_present_confirmed: bool
    after_result_present_confirmed: bool
    controlled_after_result_confirmed: bool
    sandbox_apply_result_confirmed: bool
    no_test_execution_confirmed: bool
    no_controlled_runner_invocation_confirmed: bool
    no_shell_confirmed: bool
    no_subprocess_confirmed: bool
    no_patch_application_confirmed: bool
    no_apply_patch_confirmed: bool
    no_git_apply_confirmed: bool
    no_rollback_execution_confirmed: bool
    no_repair_execution_confirmed: bool
    no_process_state_reconstruction_confirmed: bool
    no_ocel_event_write_confirmed: bool
    no_ocpx_persistence_confirmed: bool
    no_pig_execution_confirmed: bool
    no_self_prompt_execution_confirmed: bool
    no_subagent_invocation_confirmed: bool
    no_model_invocation_confirmed: bool
    no_external_agent_confirmed: bool
    no_dominion_runtime_confirmed: bool
    no_production_certification_confirmed: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["audit_id", "version", "comparison_input_id", "audit_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        _validate_true(
            self,
            [
                "no_test_execution_confirmed",
                "no_controlled_runner_invocation_confirmed",
                "no_shell_confirmed",
                "no_subprocess_confirmed",
                "no_patch_application_confirmed",
                "no_apply_patch_confirmed",
                "no_git_apply_confirmed",
                "no_rollback_execution_confirmed",
                "no_repair_execution_confirmed",
                "no_process_state_reconstruction_confirmed",
                "no_ocel_event_write_confirmed",
                "no_ocpx_persistence_confirmed",
                "no_pig_execution_confirmed",
                "no_self_prompt_execution_confirmed",
                "no_subagent_invocation_confirmed",
                "no_model_invocation_confirmed",
                "no_external_agent_confirmed",
                "no_dominion_runtime_confirmed",
                "no_production_certification_confirmed",
            ],
        )


@dataclass(frozen=True)
class RepairOutcomeComparisonDecision:
    comparison_decision_id: str
    version: str
    decision_kind: RepairOutcomeComparisonDecisionKind | str
    status: RepairOutcomeComparisonStatus | str
    readiness_level: RepairOutcomeComparisonReadinessLevel | str
    disposition: RepairOutcomeComparisonDisposition | str
    decision_summary: str
    rationale_summary: str
    confidence: RepairOutcomeConfidenceLevel | str
    evidence_refs: list[str]
    ready_for_future_process_state_reconstruction_input: bool
    test_execution_allowed_now: bool = False
    controlled_retest_allowed_now: bool = False
    arbitrary_command_allowed_now: bool = False
    shell_allowed_now: bool = False
    raw_subprocess_allowed_now: bool = False
    patch_apply_allowed_now: bool = False
    rollback_execution_allowed_now: bool = False
    before_after_comparison_rerun_allowed_now: bool = False
    repair_execution_allowed_now: bool = False
    process_state_reconstruction_allowed_now: bool = False
    ocel_event_write_allowed_now: bool = False
    ocpx_state_persistence_allowed_now: bool = False
    pig_recommendation_execution_allowed_now: bool = False
    self_prompt_generation_allowed_now: bool = False
    self_prompt_execution_allowed_now: bool = False
    subagent_invocation_allowed_now: bool = False
    model_provider_invocation_allowed_now: bool = False
    external_agent_allowed_now: bool = False
    dominion_runtime_allowed_now: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["comparison_decision_id", "version", "decision_summary", "rationale_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        _validate_false(self, UNSAFE_DECISION_NAMES)


@dataclass(frozen=True)
class RepairOutcomeComparisonReport:
    comparison_report_id: str
    version: str
    comparison_input_id: str
    outcome_pair: RepairBeforeAfterOutcomePair
    outcome_delta: RepairTestOutcomeDelta
    failure_delta: RepairFailureDeltaAssessment
    regression_signal: RepairRegressionSignal
    effectiveness_assessment: RepairEffectivenessAssessment
    do_nothing_comparison: RepairOutcomeDoNothingComparison
    audit: RepairOutcomeComparisonAudit
    decision: RepairOutcomeComparisonDecision
    report_summary: str
    ready_for_future_process_state_reconstruction_input: bool
    comparison_completed: bool
    correctness_proven: bool = False
    production_certified: bool = False
    tests_run_by_v0395: bool = False
    patches_applied_by_v0395: bool = False
    rollback_executed_by_v0395: bool = False
    repair_executed_by_v0395: bool = False
    self_prompt_generated: bool = False
    self_prompt_executed: bool = False
    next_action_generated: bool = False
    next_action_executed: bool = False
    subagent_invoked: bool = False
    model_invoked: bool = False
    external_agent_invoked: bool = False
    dominion_runtime_invoked: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["comparison_report_id", "version", "comparison_input_id", "report_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        _validate_false(self, UNSAFE_REPORT_NAMES)


@dataclass(frozen=True)
class V0395ReadinessReport:
    report_id: str
    version: str
    release_name: str
    track_name: str
    comparison_report: RepairOutcomeComparisonReport | None
    decision: RepairOutcomeComparisonDecision
    flags: RepairOutcomeComparisonFlagSet
    source_refs: list[RepairOutcomeComparisonSourceRef]
    report_summary: str
    ready_for_v0396_pi_native_repair_process_state_reconstruction: bool
    ready_for_before_after_repair_comparison: bool
    ready_for_test_outcome_delta_analysis: bool
    ready_for_failure_delta_assessment: bool
    ready_for_regression_signal_detection: bool
    ready_for_repair_effectiveness_assessment: bool
    ready_for_future_process_state_reconstruction_input: bool
    comparison_completed: bool
    effective_candidate: bool
    regressive_candidate: bool
    inconclusive_candidate: bool
    tests_run_enabled: bool = False
    controlled_retest_enabled: bool = False
    patch_apply_enabled: bool = False
    rollback_execution_enabled: bool = False
    repair_execution_enabled: bool = False
    process_state_reconstruction_enabled: bool = False
    ocel_event_write_enabled: bool = False
    ocpx_persistence_enabled: bool = False
    pig_recommendation_execution_enabled: bool = False
    self_prompt_generation_enabled: bool = False
    self_prompt_execution_enabled: bool = False
    next_action_generation_enabled: bool = False
    next_action_execution_enabled: bool = False
    subagent_invocation_enabled: bool = False
    model_invocation_enabled: bool = False
    external_agent_enabled: bool = False
    dominion_runtime_enabled: bool = False
    production_certified: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["report_id", "version", "release_name", "track_name", "report_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("source_refs", self.source_refs)
        _validate_dict("metadata", self.metadata)
        _validate_false(self, UNSAFE_READINESS_REPORT_NAMES)


@dataclass(frozen=True)
class RepairOutcomeComparisonValidationFinding:
    finding_id: str
    finding_summary: str
    risk_kind: RepairOutcomeComparisonRiskKind | str
    blocked: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("finding_summary", self.finding_summary)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairOutcomeComparisonValidationReport:
    validation_report_id: str
    version: str
    validation_summary: str
    findings: list[RepairOutcomeComparisonValidationFinding]
    supplied_before_after_metadata_only_confirmed: bool
    no_test_execution_confirmed: bool
    no_controlled_runner_invocation_confirmed: bool
    no_patch_application_confirmed: bool
    no_rollback_execution_confirmed: bool
    no_repair_execution_confirmed: bool
    no_process_state_reconstruction_confirmed: bool
    no_ocel_write_confirmed: bool
    no_ocpx_persistence_confirmed: bool
    no_pig_execution_confirmed: bool
    no_self_prompt_execution_confirmed: bool
    no_subagent_invocation_confirmed: bool
    no_model_provider_confirmed: bool
    no_external_agent_confirmed: bool
    no_dominion_runtime_confirmed: bool
    no_production_certification_confirmed: bool
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
                "supplied_before_after_metadata_only_confirmed",
                "no_test_execution_confirmed",
                "no_controlled_runner_invocation_confirmed",
                "no_patch_application_confirmed",
                "no_rollback_execution_confirmed",
                "no_repair_execution_confirmed",
                "no_process_state_reconstruction_confirmed",
                "no_ocel_write_confirmed",
                "no_ocpx_persistence_confirmed",
                "no_pig_execution_confirmed",
                "no_self_prompt_execution_confirmed",
                "no_subagent_invocation_confirmed",
                "no_model_provider_confirmed",
                "no_external_agent_confirmed",
                "no_dominion_runtime_confirmed",
                "no_production_certification_confirmed",
            ],
        )


@dataclass(frozen=True)
class RepairOutcomeComparisonRunPreview:
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
        _validate_dict("metadata", self.metadata)
        if not self.metadata_only or self.ready_for_execution:
            raise ValueError("preview must remain metadata-only and not execution-ready")


@dataclass(frozen=True)
class RepairOutcomeComparisonNoExecutionGuarantee:
    guarantee_id: str
    version: str
    guarantee_summary: str
    no_test_execution: bool = True
    no_controlled_runner_invocation: bool = True
    no_arbitrary_command: bool = True
    no_shell: bool = True
    no_subprocess: bool = True
    no_patch_application: bool = True
    no_apply_patch: bool = True
    no_git_apply: bool = True
    no_rollback_execution: bool = True
    no_repair_execution: bool = True
    no_process_state_reconstruction: bool = True
    no_ocel_event_write: bool = True
    no_ocpx_persistence: bool = True
    no_pig_execution: bool = True
    no_self_prompt_generation: bool = True
    no_self_prompt_execution: bool = True
    no_next_action_execution: bool = True
    no_subagent_invocation: bool = True
    no_model_invocation: bool = True
    no_external_agent: bool = True
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
        _validate_dict("metadata", self.metadata)
        _validate_true(
            self,
            [
                "no_test_execution",
                "no_controlled_runner_invocation",
                "no_arbitrary_command",
                "no_shell",
                "no_subprocess",
                "no_patch_application",
                "no_apply_patch",
                "no_git_apply",
                "no_rollback_execution",
                "no_repair_execution",
                "no_process_state_reconstruction",
                "no_ocel_event_write",
                "no_ocpx_persistence",
                "no_pig_execution",
                "no_self_prompt_generation",
                "no_self_prompt_execution",
                "no_next_action_execution",
                "no_subagent_invocation",
                "no_model_invocation",
                "no_external_agent",
                "no_autonomous_loop",
                "no_retry_loop",
                "no_multi_cycle_loop",
                "no_dominion_runtime",
                "no_production_certification",
            ],
        )


def build_repair_outcome_comparison_flags(**overrides: Any) -> RepairOutcomeComparisonFlagSet:
    return RepairOutcomeComparisonFlagSet(**_with_overrides({"flag_set_id": "v0395-outcome-comparison-flags", "version": V0395_VERSION}, overrides))


def build_repair_outcome_comparison_source_ref(**overrides: Any) -> RepairOutcomeComparisonSourceRef:
    defaults = {
        "source_ref_id": "v0395-source-ref",
        "source_kind": RepairOutcomeComparisonSourceKind.SUPPLIED_AFTER_TEST_RESULT,
        "source_id": "after-retest-result",
        "source_summary": "Supplied before/after result metadata for v0.39.5 comparison.",
        "evidence_refs": ["v0394-retest-result"],
    }
    return RepairOutcomeComparisonSourceRef(**_with_overrides(defaults, overrides))


def default_repair_outcome_comparison_policy(**overrides: Any) -> RepairOutcomeComparisonPolicy:
    defaults = {
        "policy_id": "v0395-outcome-comparison-policy",
        "version": V0395_VERSION,
        "allowed_modes": [
            RepairOutcomeComparisonMode.BEFORE_AFTER_REPAIR_OUTCOME_COMPARISON,
            RepairOutcomeComparisonMode.TEST_OUTCOME_DELTA_ANALYSIS,
            RepairOutcomeComparisonMode.FAILURE_DELTA_ASSESSMENT,
            RepairOutcomeComparisonMode.REGRESSION_SIGNAL_DETECTION,
            RepairOutcomeComparisonMode.REPAIR_EFFECTIVENESS_ASSESSMENT,
            RepairOutcomeComparisonMode.DO_NOTHING_AFTER_APPLY_COMPARISON,
            RepairOutcomeComparisonMode.FUTURE_PROCESS_STATE_RECONSTRUCTION_INPUT,
        ],
        "allowed_outcome_kinds": [item for item in RepairTestOutcomeKind],
    }
    return RepairOutcomeComparisonPolicy(**_with_overrides(defaults, overrides))


def build_repair_outcome_comparison_policy(**overrides: Any) -> RepairOutcomeComparisonPolicy:
    return default_repair_outcome_comparison_policy(**overrides)


def build_repair_outcome_comparison_input(**overrides: Any) -> RepairOutcomeComparisonInput:
    defaults = {
        "comparison_input_id": "v0395-comparison-input",
        "version": V0395_VERSION,
        "before_test_result_id": "before-result",
        "after_retest_result_id": "after-result",
        "sandbox_apply_result_id": "sandbox-apply-result",
        "sandbox_apply_transaction_id": "sandbox-apply-transaction",
        "before_feedback_report_id": "before-feedback",
        "after_output_capture_id": "after-output-capture",
        "proposed_patch_envelope_id": "patch-envelope",
        "safety_report_id": "safety-report",
        "requested_mode": RepairOutcomeComparisonMode.BEFORE_AFTER_REPAIR_OUTCOME_COMPARISON,
        "source_refs": [build_repair_outcome_comparison_source_ref()],
        "prohibited_runtime_actions": PROHIBITED_RUNTIME_ACTIONS.copy(),
        "task_summary": "Compare supplied before/after repair outcome metadata without execution.",
    }
    return RepairOutcomeComparisonInput(**_with_overrides(defaults, overrides))


def build_repair_test_outcome_snapshot(**overrides: Any) -> RepairTestOutcomeSnapshot:
    defaults = {
        "outcome_snapshot_id": "v0395-outcome-snapshot",
        "version": V0395_VERSION,
        "source_result_id": "result",
        "phase_label": "after",
        "outcome_kind": RepairTestOutcomeKind.PASSED,
        "selected_test_refs": ["tests/test_target.py::test_case"],
        "passed_test_refs": ["tests/test_target.py::test_case"],
        "failed_test_refs": [],
        "errored_test_refs": [],
        "skipped_test_refs": [],
        "timed_out": False,
        "runner_unavailable": False,
        "output_digest": "digest",
        "output_preview": "bounded redacted output",
        "bounded": True,
        "redacted": True,
    }
    return RepairTestOutcomeSnapshot(**_with_overrides(defaults, overrides))


def create_repair_test_outcome_snapshot_from_result_metadata(
    result_metadata: dict[str, Any],
    *,
    phase_label: str,
    max_output_preview_chars: int = 4000,
) -> RepairTestOutcomeSnapshot:
    outcome = result_metadata.get("outcome_kind", RepairTestOutcomeKind.UNKNOWN)
    selected = list(result_metadata.get("selected_test_refs", []))
    return build_repair_test_outcome_snapshot(
        outcome_snapshot_id=f"v0395-{phase_label}-snapshot",
        source_result_id=result_metadata.get("result_id") or result_metadata.get("retest_result_id"),
        phase_label=phase_label,
        outcome_kind=outcome,
        selected_test_refs=selected,
        passed_test_refs=list(result_metadata.get("passed_test_refs", [])),
        failed_test_refs=list(result_metadata.get("failed_test_refs", [])),
        errored_test_refs=list(result_metadata.get("errored_test_refs", [])),
        skipped_test_refs=list(result_metadata.get("skipped_test_refs", [])),
        timed_out=bool(result_metadata.get("timed_out", outcome == RepairTestOutcomeKind.TIMED_OUT)),
        runner_unavailable=bool(result_metadata.get("runner_unavailable", outcome == RepairTestOutcomeKind.RUNNER_UNAVAILABLE)),
        output_digest=result_metadata.get("output_digest"),
        output_preview=_bounded(str(result_metadata.get("output_preview", "bounded redacted output")), max_output_preview_chars),
        bounded=True,
        redacted=True,
    )


def build_repair_before_after_outcome_pair(**overrides: Any) -> RepairBeforeAfterOutcomePair:
    before = overrides.pop("before_snapshot", build_repair_test_outcome_snapshot(phase_label="before", outcome_kind=RepairTestOutcomeKind.FAILED, passed_test_refs=[], failed_test_refs=["tests/test_target.py::test_case"]))
    after = overrides.pop("after_snapshot", build_repair_test_outcome_snapshot())
    before_refs = set(before.selected_test_refs) if before else set()
    after_refs = set(after.selected_test_refs) if after else set()
    comparable = sorted(before_refs & after_refs)
    defaults = {
        "outcome_pair_id": "v0395-outcome-pair",
        "version": V0395_VERSION,
        "before_snapshot": before,
        "after_snapshot": after,
        "comparable_test_refs": comparable,
        "before_only_test_refs": sorted(before_refs - after_refs),
        "after_only_test_refs": sorted(after_refs - before_refs),
        "scope_changed": before_refs != after_refs,
        "pair_summary": "Before/after outcome pair created from supplied metadata.",
        "pair_complete": before is not None and after is not None,
        "pair_comparable": before is not None and after is not None and before_refs == after_refs and bool(comparable),
        "evidence_refs": ["before-result", "after-result"],
    }
    return RepairBeforeAfterOutcomePair(**_with_overrides(defaults, overrides))


def pair_before_after_repair_outcomes(
    before_snapshot: RepairTestOutcomeSnapshot | None,
    after_snapshot: RepairTestOutcomeSnapshot | None,
) -> RepairBeforeAfterOutcomePair:
    return build_repair_before_after_outcome_pair(before_snapshot=before_snapshot, after_snapshot=after_snapshot)


def _delta_kind(before: RepairTestOutcomeKind | str, after: RepairTestOutcomeKind | str, comparable: bool = True) -> RepairTestOutcomeDeltaKind:
    if not comparable:
        return RepairTestOutcomeDeltaKind.INCOMPARABLE
    before_value = str(before)
    after_value = str(after)
    pairs = {
        ("failed", "passed"): RepairTestOutcomeDeltaKind.FAIL_TO_PASS,
        ("failed", "failed"): RepairTestOutcomeDeltaKind.FAIL_TO_FAIL,
        ("passed", "passed"): RepairTestOutcomeDeltaKind.PASS_TO_PASS,
        ("passed", "failed"): RepairTestOutcomeDeltaKind.PASS_TO_FAIL,
        ("error", "passed"): RepairTestOutcomeDeltaKind.ERROR_TO_PASS,
        ("error", "failed"): RepairTestOutcomeDeltaKind.ERROR_TO_FAIL,
        ("timed_out", "passed"): RepairTestOutcomeDeltaKind.TIMEOUT_TO_PASS,
        ("timed_out", "failed"): RepairTestOutcomeDeltaKind.TIMEOUT_TO_FAIL,
        ("timed_out", "timed_out"): RepairTestOutcomeDeltaKind.TIMEOUT_TO_TIMEOUT,
        ("no_result", "passed"): RepairTestOutcomeDeltaKind.NO_BEFORE_RESULT,
        ("failed", "no_result"): RepairTestOutcomeDeltaKind.NO_AFTER_RESULT,
    }
    return pairs.get((before_value, after_value), RepairTestOutcomeDeltaKind.INCONCLUSIVE)


def build_repair_test_outcome_delta(**overrides: Any) -> RepairTestOutcomeDelta:
    defaults = {
        "outcome_delta_id": "v0395-outcome-delta",
        "version": V0395_VERSION,
        "outcome_pair_id": "v0395-outcome-pair",
        "delta_kind": RepairTestOutcomeDeltaKind.FAIL_TO_PASS,
        "before_outcome": RepairTestOutcomeKind.FAILED,
        "after_outcome": RepairTestOutcomeKind.PASSED,
        "passed_count_delta": 1,
        "failed_count_delta": -1,
        "error_count_delta": 0,
        "skipped_count_delta": 0,
        "delta_summary": "Outcome improved from failing baseline to passing after-test candidate.",
        "improved": True,
        "worsened": False,
        "inconclusive": False,
        "evidence_refs": ["v0395-outcome-pair"],
    }
    return RepairTestOutcomeDelta(**_with_overrides(defaults, overrides))


def compare_repair_test_outcomes(pair: RepairBeforeAfterOutcomePair) -> RepairTestOutcomeDelta:
    before = pair.before_snapshot
    after = pair.after_snapshot
    before_kind = before.outcome_kind if before else RepairTestOutcomeKind.NO_RESULT
    after_kind = after.outcome_kind if after else RepairTestOutcomeKind.NO_RESULT
    kind = _delta_kind(before_kind, after_kind, pair.pair_comparable)
    before_passed = len(before.passed_test_refs) if before else 0
    after_passed = len(after.passed_test_refs) if after else 0
    before_failed = len(before.failed_test_refs) if before else 0
    after_failed = len(after.failed_test_refs) if after else 0
    before_errors = len(before.errored_test_refs) if before else 0
    after_errors = len(after.errored_test_refs) if after else 0
    before_skipped = len(before.skipped_test_refs) if before else 0
    after_skipped = len(after.skipped_test_refs) if after else 0
    improved = kind in {
        RepairTestOutcomeDeltaKind.FAIL_TO_PASS,
        RepairTestOutcomeDeltaKind.ERROR_TO_PASS,
        RepairTestOutcomeDeltaKind.TIMEOUT_TO_PASS,
    }
    worsened = kind in {
        RepairTestOutcomeDeltaKind.PASS_TO_FAIL,
        RepairTestOutcomeDeltaKind.ERROR_TO_FAIL,
        RepairTestOutcomeDeltaKind.TIMEOUT_TO_FAIL,
    }
    inconclusive = kind in {
        RepairTestOutcomeDeltaKind.INCOMPARABLE,
        RepairTestOutcomeDeltaKind.INCONCLUSIVE,
        RepairTestOutcomeDeltaKind.NO_BEFORE_RESULT,
        RepairTestOutcomeDeltaKind.NO_AFTER_RESULT,
    }
    return build_repair_test_outcome_delta(
        outcome_pair_id=pair.outcome_pair_id,
        delta_kind=kind,
        before_outcome=before_kind,
        after_outcome=after_kind,
        passed_count_delta=after_passed - before_passed,
        failed_count_delta=after_failed - before_failed,
        error_count_delta=after_errors - before_errors,
        skipped_count_delta=after_skipped - before_skipped,
        delta_summary=f"Outcome delta {kind.value} computed from supplied metadata.",
        improved=improved,
        worsened=worsened,
        inconclusive=inconclusive,
    )


def build_repair_failure_delta_assessment(**overrides: Any) -> RepairFailureDeltaAssessment:
    defaults = {
        "failure_delta_id": "v0395-failure-delta",
        "version": V0395_VERSION,
        "outcome_pair_id": "v0395-outcome-pair",
        "failure_delta_kinds": [RepairFailureDeltaKind.FAILURE_RESOLVED],
        "resolved_failure_refs": ["tests/test_target.py::test_case"],
        "residual_failure_refs": [],
        "new_failure_refs": [],
        "worsened_failure_refs": [],
        "failure_delta_summary": "Failure delta assessed from supplied before/after metadata.",
        "residual_failures_present": False,
        "new_failures_present": False,
        "evidence_refs": ["v0395-outcome-pair"],
    }
    return RepairFailureDeltaAssessment(**_with_overrides(defaults, overrides))


def assess_repair_failure_delta(pair: RepairBeforeAfterOutcomePair) -> RepairFailureDeltaAssessment:
    before_failures = _fail_refs(pair.before_snapshot) if pair.before_snapshot else set()
    after_failures = _fail_refs(pair.after_snapshot) if pair.after_snapshot else set()
    resolved = sorted(before_failures - after_failures)
    residual = sorted(before_failures & after_failures)
    new = sorted(after_failures - before_failures)
    kinds: list[RepairFailureDeltaKind | str] = []
    if resolved:
        kinds.append(RepairFailureDeltaKind.FAILURE_RESOLVED)
    if residual:
        kinds.append(RepairFailureDeltaKind.RESIDUAL_FAILURE_PRESENT)
    if new:
        kinds.append(RepairFailureDeltaKind.NEW_FAILURE_INTRODUCED)
    if not before_failures:
        kinds.append(RepairFailureDeltaKind.NO_FAILURE_BEFORE)
    if not after_failures:
        kinds.append(RepairFailureDeltaKind.NO_FAILURE_AFTER)
    if not kinds:
        kinds.append(RepairFailureDeltaKind.INCONCLUSIVE)
    return build_repair_failure_delta_assessment(
        outcome_pair_id=pair.outcome_pair_id,
        failure_delta_kinds=kinds,
        resolved_failure_refs=resolved,
        residual_failure_refs=residual,
        new_failure_refs=new,
        worsened_failure_refs=new,
        residual_failures_present=bool(residual),
        new_failures_present=bool(new),
    )


def build_repair_regression_signal(**overrides: Any) -> RepairRegressionSignal:
    defaults = {
        "regression_signal_id": "v0395-regression-signal",
        "version": V0395_VERSION,
        "outcome_pair_id": "v0395-outcome-pair",
        "signal_kinds": [RepairRegressionSignalKind.NO_REGRESSION_DETECTED],
        "signal_summary": "No regression detected from supplied comparison metadata; this is not certification.",
        "regression_detected": False,
        "new_failure_detected": False,
        "timeout_regression_detected": False,
        "scope_change_detected": False,
        "output_regression_detected": False,
        "confidence": RepairOutcomeConfidenceLevel.MEDIUM,
        "evidence_refs": ["v0395-outcome-pair"],
    }
    return RepairRegressionSignal(**_with_overrides(defaults, overrides))


def detect_repair_regression_signals(pair: RepairBeforeAfterOutcomePair, failure_delta: RepairFailureDeltaAssessment | None = None) -> RepairRegressionSignal:
    failure_delta = failure_delta or assess_repair_failure_delta(pair)
    signal_kinds: list[RepairRegressionSignalKind | str] = []
    new_failure = bool(failure_delta.new_failure_refs)
    timeout_regression = bool(pair.after_snapshot and pair.after_snapshot.timed_out and not (pair.before_snapshot and pair.before_snapshot.timed_out))
    if new_failure:
        signal_kinds.append(RepairRegressionSignalKind.NEW_FAILED_TEST)
    if timeout_regression:
        signal_kinds.append(RepairRegressionSignalKind.NEW_TIMEOUT)
    if pair.scope_changed:
        signal_kinds.append(RepairRegressionSignalKind.SCOPE_CHANGED_SIGNAL)
    if not signal_kinds:
        signal_kinds.append(RepairRegressionSignalKind.NO_REGRESSION_DETECTED if pair.pair_comparable else RepairRegressionSignalKind.INSUFFICIENT_DATA)
    regression_detected = any(item != RepairRegressionSignalKind.NO_REGRESSION_DETECTED for item in signal_kinds)
    return build_repair_regression_signal(
        outcome_pair_id=pair.outcome_pair_id,
        signal_kinds=signal_kinds,
        regression_detected=regression_detected,
        new_failure_detected=new_failure,
        timeout_regression_detected=timeout_regression,
        scope_change_detected=pair.scope_changed,
        confidence=RepairOutcomeConfidenceLevel.MEDIUM if pair.pair_comparable else RepairOutcomeConfidenceLevel.LOW,
    )


def build_repair_effectiveness_assessment(**overrides: Any) -> RepairEffectivenessAssessment:
    defaults = {
        "effectiveness_assessment_id": "v0395-effectiveness",
        "version": V0395_VERSION,
        "outcome_pair_id": "v0395-outcome-pair",
        "effectiveness_kind": RepairEffectivenessKind.EFFECTIVE_CANDIDATE,
        "effectiveness_summary": "Repair is an effective candidate based on metadata comparison, not a correctness proof.",
        "confidence": RepairOutcomeConfidenceLevel.MEDIUM,
        "effective_candidate": True,
        "partially_effective_candidate": False,
        "ineffective_candidate": False,
        "regressive_candidate": False,
        "inconclusive_candidate": False,
        "evidence_refs": ["v0395-outcome-delta"],
    }
    return RepairEffectivenessAssessment(**_with_overrides(defaults, overrides))


def assess_repair_effectiveness(
    outcome_delta: RepairTestOutcomeDelta,
    failure_delta: RepairFailureDeltaAssessment,
    regression_signal: RepairRegressionSignal,
) -> RepairEffectivenessAssessment:
    if regression_signal.regression_detected or outcome_delta.worsened:
        kind = RepairEffectivenessKind.REGRESSIVE_CANDIDATE
    elif outcome_delta.improved and not failure_delta.residual_failures_present:
        kind = RepairEffectivenessKind.EFFECTIVE_CANDIDATE
    elif outcome_delta.improved or failure_delta.resolved_failure_refs:
        kind = RepairEffectivenessKind.PARTIALLY_EFFECTIVE_CANDIDATE
    elif outcome_delta.inconclusive:
        kind = RepairEffectivenessKind.INCONCLUSIVE_CANDIDATE
    else:
        kind = RepairEffectivenessKind.INEFFECTIVE_CANDIDATE
    return build_repair_effectiveness_assessment(
        outcome_pair_id=outcome_delta.outcome_pair_id,
        effectiveness_kind=kind,
        effectiveness_summary=f"{kind.value} derived from supplied before/after metadata; not correctness proof.",
        confidence=RepairOutcomeConfidenceLevel.MEDIUM if not outcome_delta.inconclusive else RepairOutcomeConfidenceLevel.INCONCLUSIVE,
        effective_candidate=kind == RepairEffectivenessKind.EFFECTIVE_CANDIDATE,
        partially_effective_candidate=kind == RepairEffectivenessKind.PARTIALLY_EFFECTIVE_CANDIDATE,
        ineffective_candidate=kind == RepairEffectivenessKind.INEFFECTIVE_CANDIDATE,
        regressive_candidate=kind == RepairEffectivenessKind.REGRESSIVE_CANDIDATE,
        inconclusive_candidate=kind == RepairEffectivenessKind.INCONCLUSIVE_CANDIDATE,
    )


def build_repair_outcome_do_nothing_comparison(**overrides: Any) -> RepairOutcomeDoNothingComparison:
    defaults = {
        "do_nothing_comparison_id": "v0395-do-nothing-comparison",
        "version": V0395_VERSION,
        "comparison_kind": RepairOutcomeDoNothingComparisonKind.REPAIR_OUTPERFORMS_DO_NOTHING,
        "comparison_summary": "Do-nothing comparison represented for human review.",
        "do_nothing_remains_valid": True,
        "do_nothing_preferred": False,
        "do_nothing_required": False,
        "repair_outperforms_do_nothing": True,
        "confidence": RepairOutcomeConfidenceLevel.MEDIUM,
        "evidence_refs": ["v0395-effectiveness"],
    }
    return RepairOutcomeDoNothingComparison(**_with_overrides(defaults, overrides))


def compare_repair_outcome_to_do_nothing(effectiveness: RepairEffectivenessAssessment) -> RepairOutcomeDoNothingComparison:
    if effectiveness.regressive_candidate:
        kind = RepairOutcomeDoNothingComparisonKind.DO_NOTHING_PREFERRED_DUE_TO_REGRESSION
    elif effectiveness.inconclusive_candidate:
        kind = RepairOutcomeDoNothingComparisonKind.DO_NOTHING_PREFERRED_DUE_TO_INCONCLUSIVE_RESULT
    elif effectiveness.partially_effective_candidate:
        kind = RepairOutcomeDoNothingComparisonKind.REPAIR_PARTIALLY_OUTPERFORMS_DO_NOTHING
    elif effectiveness.effective_candidate:
        kind = RepairOutcomeDoNothingComparisonKind.REPAIR_OUTPERFORMS_DO_NOTHING
    else:
        kind = RepairOutcomeDoNothingComparisonKind.DO_NOTHING_COMPETITIVE_DUE_TO_LOW_COVERAGE
    return build_repair_outcome_do_nothing_comparison(
        comparison_kind=kind,
        do_nothing_preferred=kind
        in {
            RepairOutcomeDoNothingComparisonKind.DO_NOTHING_PREFERRED_DUE_TO_REGRESSION,
            RepairOutcomeDoNothingComparisonKind.DO_NOTHING_PREFERRED_DUE_TO_INCONCLUSIVE_RESULT,
        },
        repair_outperforms_do_nothing=kind
        in {
            RepairOutcomeDoNothingComparisonKind.REPAIR_OUTPERFORMS_DO_NOTHING,
            RepairOutcomeDoNothingComparisonKind.REPAIR_PARTIALLY_OUTPERFORMS_DO_NOTHING,
        },
    )


def build_repair_outcome_comparison_audit(**overrides: Any) -> RepairOutcomeComparisonAudit:
    defaults = {
        "audit_id": "v0395-comparison-audit",
        "version": V0395_VERSION,
        "comparison_input_id": "v0395-comparison-input",
        "audit_summary": "v0.39.5 compared supplied metadata only and introduced no execution.",
        "before_result_present_confirmed": True,
        "after_result_present_confirmed": True,
        "controlled_after_result_confirmed": True,
        "sandbox_apply_result_confirmed": True,
        "no_test_execution_confirmed": True,
        "no_controlled_runner_invocation_confirmed": True,
        "no_shell_confirmed": True,
        "no_subprocess_confirmed": True,
        "no_patch_application_confirmed": True,
        "no_apply_patch_confirmed": True,
        "no_git_apply_confirmed": True,
        "no_rollback_execution_confirmed": True,
        "no_repair_execution_confirmed": True,
        "no_process_state_reconstruction_confirmed": True,
        "no_ocel_event_write_confirmed": True,
        "no_ocpx_persistence_confirmed": True,
        "no_pig_execution_confirmed": True,
        "no_self_prompt_execution_confirmed": True,
        "no_subagent_invocation_confirmed": True,
        "no_model_invocation_confirmed": True,
        "no_external_agent_confirmed": True,
        "no_dominion_runtime_confirmed": True,
        "no_production_certification_confirmed": True,
        "evidence_refs": ["v0395-comparison-report"],
    }
    return RepairOutcomeComparisonAudit(**_with_overrides(defaults, overrides))


def audit_repair_outcome_comparison(comparison_input: RepairOutcomeComparisonInput) -> RepairOutcomeComparisonAudit:
    return build_repair_outcome_comparison_audit(
        comparison_input_id=comparison_input.comparison_input_id,
        before_result_present_confirmed=comparison_input.before_test_result_id is not None,
        after_result_present_confirmed=comparison_input.after_retest_result_id is not None,
        sandbox_apply_result_confirmed=comparison_input.sandbox_apply_result_id is not None,
    )


def build_repair_outcome_comparison_decision(**overrides: Any) -> RepairOutcomeComparisonDecision:
    defaults = {
        "comparison_decision_id": "v0395-comparison-decision",
        "version": V0395_VERSION,
        "decision_kind": RepairOutcomeComparisonDecisionKind.ALLOW_FUTURE_PROCESS_STATE_RECONSTRUCTION_INPUT,
        "status": RepairOutcomeComparisonStatus.READY_FOR_FUTURE_PROCESS_STATE_RECONSTRUCTION,
        "readiness_level": RepairOutcomeComparisonReadinessLevel.FUTURE_PROCESS_STATE_RECONSTRUCTION_INPUT_READY,
        "disposition": RepairOutcomeComparisonDisposition.COMPARISON_COMPLETED,
        "decision_summary": "Comparison metadata may feed future v0.39.6 process-state reconstruction input.",
        "rationale_summary": "Before/after supplied metadata was compared without execution or correctness proof.",
        "confidence": RepairOutcomeConfidenceLevel.MEDIUM,
        "evidence_refs": ["v0395-comparison-report"],
        "ready_for_future_process_state_reconstruction_input": True,
    }
    return RepairOutcomeComparisonDecision(**_with_overrides(defaults, overrides))


def decide_repair_outcome_comparison(report_or_assessment: RepairOutcomeComparisonReport | RepairEffectivenessAssessment) -> RepairOutcomeComparisonDecision:
    assessment = report_or_assessment.effectiveness_assessment if isinstance(report_or_assessment, RepairOutcomeComparisonReport) else report_or_assessment
    if assessment.regressive_candidate:
        kind = RepairOutcomeComparisonDecisionKind.CHOOSE_REGRESSIVE_REPAIR_CANDIDATE
        disposition = RepairOutcomeComparisonDisposition.REGRESSIVE_CANDIDATE
    elif assessment.effective_candidate:
        kind = RepairOutcomeComparisonDecisionKind.CHOOSE_EFFECTIVE_REPAIR_CANDIDATE
        disposition = RepairOutcomeComparisonDisposition.EFFECTIVE_CANDIDATE
    elif assessment.partially_effective_candidate:
        kind = RepairOutcomeComparisonDecisionKind.CHOOSE_PARTIALLY_EFFECTIVE_REPAIR_CANDIDATE
        disposition = RepairOutcomeComparisonDisposition.PARTIALLY_EFFECTIVE_CANDIDATE
    elif assessment.inconclusive_candidate:
        kind = RepairOutcomeComparisonDecisionKind.CHOOSE_INCONCLUSIVE
        disposition = RepairOutcomeComparisonDisposition.INCONCLUSIVE
    else:
        kind = RepairOutcomeComparisonDecisionKind.CHOOSE_INEFFECTIVE_REPAIR_CANDIDATE
        disposition = RepairOutcomeComparisonDisposition.INEFFECTIVE_CANDIDATE
    return build_repair_outcome_comparison_decision(decision_kind=kind, disposition=disposition, confidence=assessment.confidence)


def build_repair_outcome_comparison_report(**overrides: Any) -> RepairOutcomeComparisonReport:
    pair = overrides.pop("outcome_pair", build_repair_before_after_outcome_pair())
    delta = overrides.pop("outcome_delta", compare_repair_test_outcomes(pair))
    failure_delta = overrides.pop("failure_delta", assess_repair_failure_delta(pair))
    regression = overrides.pop("regression_signal", detect_repair_regression_signals(pair, failure_delta))
    effectiveness = overrides.pop("effectiveness_assessment", assess_repair_effectiveness(delta, failure_delta, regression))
    do_nothing = overrides.pop("do_nothing_comparison", compare_repair_outcome_to_do_nothing(effectiveness))
    decision = overrides.pop("decision", decide_repair_outcome_comparison(effectiveness))
    defaults = {
        "comparison_report_id": "v0395-comparison-report",
        "version": V0395_VERSION,
        "comparison_input_id": "v0395-comparison-input",
        "outcome_pair": pair,
        "outcome_delta": delta,
        "failure_delta": failure_delta,
        "regression_signal": regression,
        "effectiveness_assessment": effectiveness,
        "do_nothing_comparison": do_nothing,
        "audit": build_repair_outcome_comparison_audit(),
        "decision": decision,
        "report_summary": "Before/after repair outcome comparison completed from supplied metadata only.",
        "ready_for_future_process_state_reconstruction_input": True,
        "comparison_completed": True,
        "evidence_refs": ["v0395-outcome-pair", "v0395-outcome-delta"],
    }
    return RepairOutcomeComparisonReport(**_with_overrides(defaults, overrides))


def create_repair_outcome_comparison_report(
    comparison_input: RepairOutcomeComparisonInput,
    before_snapshot: RepairTestOutcomeSnapshot,
    after_snapshot: RepairTestOutcomeSnapshot,
) -> RepairOutcomeComparisonReport:
    pair = pair_before_after_repair_outcomes(before_snapshot, after_snapshot)
    report = build_repair_outcome_comparison_report(outcome_pair=pair, comparison_input_id=comparison_input.comparison_input_id)
    return report


def build_repair_outcome_comparison_validation_finding(**overrides: Any) -> RepairOutcomeComparisonValidationFinding:
    defaults = {
        "finding_id": "v0395-validation-finding",
        "finding_summary": "No runtime authority introduced.",
        "risk_kind": RepairOutcomeComparisonRiskKind.REPAIR_CORRECTNESS_OVERCLAIM_RISK,
        "blocked": False,
    }
    return RepairOutcomeComparisonValidationFinding(**_with_overrides(defaults, overrides))


def build_repair_outcome_comparison_validation_report(**overrides: Any) -> RepairOutcomeComparisonValidationReport:
    defaults = {
        "validation_report_id": "v0395-validation-report",
        "version": V0395_VERSION,
        "validation_summary": "Validation confirms supplied metadata comparison only and no execution.",
        "findings": [build_repair_outcome_comparison_validation_finding()],
        "supplied_before_after_metadata_only_confirmed": True,
        "no_test_execution_confirmed": True,
        "no_controlled_runner_invocation_confirmed": True,
        "no_patch_application_confirmed": True,
        "no_rollback_execution_confirmed": True,
        "no_repair_execution_confirmed": True,
        "no_process_state_reconstruction_confirmed": True,
        "no_ocel_write_confirmed": True,
        "no_ocpx_persistence_confirmed": True,
        "no_pig_execution_confirmed": True,
        "no_self_prompt_execution_confirmed": True,
        "no_subagent_invocation_confirmed": True,
        "no_model_provider_confirmed": True,
        "no_external_agent_confirmed": True,
        "no_dominion_runtime_confirmed": True,
        "no_production_certification_confirmed": True,
    }
    return RepairOutcomeComparisonValidationReport(**_with_overrides(defaults, overrides))


def build_repair_outcome_comparison_run_preview(**overrides: Any) -> RepairOutcomeComparisonRunPreview:
    defaults = {
        "preview_id": "v0395-run-preview",
        "version": V0395_VERSION,
        "preview_summary": "Preview lists metadata comparison steps only.",
        "planned_metadata_steps": [
            "OutcomeSnapshot",
            "BeforeAfterOutcomePair",
            "TestOutcomeDelta",
            "FailureDeltaAssessment",
            "RegressionSignal",
            "RepairEffectivenessAssessment",
            "DoNothingComparison",
        ],
    }
    return RepairOutcomeComparisonRunPreview(**_with_overrides(defaults, overrides))


def build_repair_outcome_comparison_no_execution_guarantee(**overrides: Any) -> RepairOutcomeComparisonNoExecutionGuarantee:
    defaults = {
        "guarantee_id": "v0395-no-execution-guarantee",
        "version": V0395_VERSION,
        "guarantee_summary": "v0.39.5 comparison is metadata-only and blocks all execution/runtime surfaces.",
    }
    return RepairOutcomeComparisonNoExecutionGuarantee(**_with_overrides(defaults, overrides))


def build_v0395_readiness_report(**overrides: Any) -> V0395ReadinessReport:
    comparison_report = overrides.pop("comparison_report", build_repair_outcome_comparison_report())
    decision = overrides.pop("decision", comparison_report.decision)
    effectiveness = comparison_report.effectiveness_assessment
    defaults = {
        "report_id": "v0395-readiness-report",
        "version": V0395_VERSION,
        "release_name": V0395_RELEASE_NAME,
        "track_name": V039_TRACK_NAME,
        "comparison_report": comparison_report,
        "decision": decision,
        "flags": build_repair_outcome_comparison_flags(),
        "source_refs": [build_repair_outcome_comparison_source_ref()],
        "report_summary": "v0.39.5 comparison metadata is ready for v0.39.6 design-stage handoff only.",
        "ready_for_v0396_pi_native_repair_process_state_reconstruction": True,
        "ready_for_before_after_repair_comparison": True,
        "ready_for_test_outcome_delta_analysis": True,
        "ready_for_failure_delta_assessment": True,
        "ready_for_regression_signal_detection": True,
        "ready_for_repair_effectiveness_assessment": True,
        "ready_for_future_process_state_reconstruction_input": True,
        "comparison_completed": True,
        "effective_candidate": effectiveness.effective_candidate,
        "regressive_candidate": effectiveness.regressive_candidate,
        "inconclusive_candidate": effectiveness.inconclusive_candidate,
    }
    return V0395ReadinessReport(**_with_overrides(defaults, overrides))


def repair_outcome_comparison_flags_preserve_no_execution(flags: RepairOutcomeComparisonFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_FLAG_NAMES)


def repair_outcome_comparison_policy_blocks_runtime(policy: RepairOutcomeComparisonPolicy) -> bool:
    return all(getattr(policy, name) is False for name in UNSAFE_POLICY_ALLOW_NAMES)


def repair_effectiveness_assessment_is_not_correctness_proof(assessment: RepairEffectivenessAssessment) -> bool:
    return assessment.correctness_proven is False and assessment.production_certified is False


def repair_outcome_comparison_report_is_not_execution(report: RepairOutcomeComparisonReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_REPORT_NAMES)


def v0395_readiness_report_is_not_execution_ready(report: V0395ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_READINESS_REPORT_NAMES) and repair_outcome_comparison_flags_preserve_no_execution(report.flags)
