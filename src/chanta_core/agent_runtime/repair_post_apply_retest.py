"""v0.39.4 post-apply controlled re-test metadata and runner gate.

The only helper that may invoke test behavior is run_post_apply_controlled_retest,
and it only calls a supplied controlled runner callable after policy, command,
workspace, and sandbox-apply gates are satisfied. This module does not provide
raw process execution, shell execution, dependency installation, network access,
patch application, before/after comparison, repair execution, self-prompting,
subagent invocation, provider invocation, Dominion runtime, or production
certification.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Callable

from .boundary import _require_non_blank


V0394_VERSION = "v0.39.4"
V0394_RELEASE_NAME = "v0.39.4 Post-Apply Controlled Re-test"
V039_TRACK_NAME = "Human-approved Sandbox Repair Apply & Re-test Loop with PI-native Self-Prompting Mission Loop Boundary"

PROHIBITED_RUNTIME_ACTIONS = [
    "shell",
    "raw_subprocess",
    "arbitrary_command",
    "install",
    "network",
    "live_workspace_test",
    "patch_apply",
    "apply_patch",
    "git_apply",
    "self_prompt_execution",
    "subagent_invocation",
    "model_provider",
    "external_agent",
    "Dominion",
]


class RepairPostApplyRetestMode(StrEnum):
    POST_APPLY_CONTROLLED_RETEST = "post_apply_controlled_retest"
    CONTROLLED_TEST_SELECTION = "controlled_test_selection"
    CONTROLLED_TEST_COMMAND_SPEC = "controlled_test_command_spec"
    CONTROLLED_RUNNER_INVOCATION = "controlled_runner_invocation"
    BOUNDED_TEST_OUTPUT_CAPTURE = "bounded_test_output_capture"
    POST_APPLY_TEST_RESULT_ENVELOPE = "post_apply_test_result_envelope"
    POST_APPLY_RETEST_AUDIT = "post_apply_retest_audit"
    FUTURE_BEFORE_AFTER_COMPARISON_INPUT = "future_before_after_comparison_input"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairPostApplyRetestSourceKind(StrEnum):
    V0393_SANDBOX_APPLY_RESULT = "v0393_sandbox_apply_result"
    V0393_SANDBOX_APPLY_TRANSACTION = "v0393_sandbox_apply_transaction"
    V0393_SANDBOX_APPLY_AUDIT = "v0393_sandbox_apply_audit"
    V0393_READINESS_REPORT = "v0393_readiness_report"
    V0392_WORKSPACE_DESCRIPTOR = "v0392_workspace_descriptor"
    V0392_WORKSPACE_ISOLATION_DECISION = "v0392_workspace_isolation_decision"
    V0392_LIVE_BOUNDARY_CHECK = "v0392_live_boundary_check"
    V0391_APPROVAL_ARTIFACT_DECISION = "v0391_approval_artifact_decision"
    V0391_APPROVAL_PROCESS_STATE_GATE = "v0391_approval_process_state_gate"
    V0379_CONTROLLED_SANDBOX_TEST_RUNNER = "v0379_controlled_sandbox_test_runner"
    V0373_SANDBOX_TEST_RESULT_ENVELOPE = "v0373_sandbox_test_result_envelope"
    V0374_SANDBOX_TEST_FEEDBACK_REPORT = "v0374_sandbox_test_feedback_report"
    SUPPLIED_TEST_COMMAND_SPEC = "supplied_test_command_spec"
    SUPPLIED_TEST_RUNNER_ADAPTER = "supplied_test_runner_adapter"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class RepairPostApplyRetestStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    INPUT_VALIDATED = "input_validated"
    TEST_SELECTION_CREATED = "test_selection_created"
    COMMAND_SPEC_CREATED = "command_spec_created"
    RUNNER_INVOCATION_CREATED = "runner_invocation_created"
    CONTROLLED_RETEST_STARTED = "controlled_retest_started"
    CONTROLLED_RETEST_COMPLETED = "controlled_retest_completed"
    CONTROLLED_RETEST_COMPLETED_WITH_WARNINGS = "controlled_retest_completed_with_warnings"
    CONTROLLED_RETEST_FAILED = "controlled_retest_failed"
    CONTROLLED_RETEST_TIMED_OUT = "controlled_retest_timed_out"
    CONTROLLED_RETEST_BLOCKED = "controlled_retest_blocked"
    CONTROLLED_RUNNER_UNAVAILABLE = "controlled_runner_unavailable"
    OUTPUT_CAPTURED = "output_captured"
    READY_FOR_FUTURE_BEFORE_AFTER_COMPARISON = "ready_for_future_before_after_comparison"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    REVIEW_REQUIRED = "review_required"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class RepairPostApplyRetestReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    SANDBOX_APPLY_RESULT_READY = "sandbox_apply_result_ready"
    CONTROLLED_TEST_SELECTION_READY = "controlled_test_selection_ready"
    CONTROLLED_TEST_COMMAND_READY = "controlled_test_command_ready"
    CONTROLLED_RUNNER_INVOCATION_READY = "controlled_runner_invocation_ready"
    CONTROLLED_RETEST_RESULT_READY = "controlled_retest_result_ready"
    BOUNDED_OUTPUT_CAPTURE_READY = "bounded_output_capture_ready"
    FUTURE_BEFORE_AFTER_COMPARISON_INPUT_READY = "future_before_after_comparison_input_ready"
    DESIGN_HANDOFF_READY_FOR_V0395 = "design_handoff_ready_for_v0395"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class RepairPostApplyRetestDecisionKind(StrEnum):
    ALLOW_CONTROLLED_TEST_SELECTION = "allow_controlled_test_selection"
    ALLOW_CONTROLLED_TEST_COMMAND_SPEC = "allow_controlled_test_command_spec"
    ALLOW_CONTROLLED_RUNNER_INVOCATION = "allow_controlled_runner_invocation"
    ALLOW_BOUNDED_OUTPUT_CAPTURE = "allow_bounded_output_capture"
    ALLOW_POST_APPLY_TEST_RESULT_ENVELOPE = "allow_post_apply_test_result_envelope"
    ALLOW_FUTURE_BEFORE_AFTER_COMPARISON_INPUT = "allow_future_before_after_comparison_input"
    CHOOSE_DO_NOTHING = "choose_do_nothing"
    CHOOSE_HUMAN_REVIEW_REQUIRED = "choose_human_review_required"
    DENY = "deny"
    BLOCK = "block"
    REJECT_MISSING_SANDBOX_APPLY_RESULT = "reject_missing_sandbox_apply_result"
    REJECT_FAILED_SANDBOX_APPLY = "reject_failed_sandbox_apply"
    REJECT_INVALID_WORKSPACE = "reject_invalid_workspace"
    REJECT_LIVE_WORKSPACE_TARGET = "reject_live_workspace_target"
    REJECT_UNAPPROVED_TEST_COMMAND = "reject_unapproved_test_command"
    REJECT_SHELL_COMMAND = "reject_shell_command"
    REJECT_SUBPROCESS_WITHOUT_CONTROLLED_RUNNER = "reject_subprocess_without_controlled_runner"
    REJECT_DEPENDENCY_INSTALL = "reject_dependency_install"
    REJECT_NETWORK_ACCESS = "reject_network_access"
    REJECT_TIMEOUT_POLICY_MISSING = "reject_timeout_policy_missing"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class RepairPostApplyRetestRiskKind(StrEnum):
    MISSING_SANDBOX_APPLY_RESULT_RISK = "missing_sandbox_apply_result_risk"
    FAILED_SANDBOX_APPLY_RISK = "failed_sandbox_apply_risk"
    INVALID_WORKSPACE_RISK = "invalid_workspace_risk"
    LIVE_WORKSPACE_TEST_RISK = "live_workspace_test_risk"
    ARBITRARY_COMMAND_EXECUTION_RISK = "arbitrary_command_execution_risk"
    SHELL_EXECUTION_RISK = "shell_execution_risk"
    RAW_SUBPROCESS_EXECUTION_RISK = "raw_subprocess_execution_risk"
    DEPENDENCY_INSTALL_RISK = "dependency_install_risk"
    NETWORK_ACCESS_RISK = "network_access_risk"
    UNBOUNDED_TEST_SCOPE_RISK = "unbounded_test_scope_risk"
    MISSING_TIMEOUT_RISK = "missing_timeout_risk"
    EXCESSIVE_OUTPUT_RISK = "excessive_output_risk"
    TEST_OUTPUT_SECRET_LEAK_RISK = "test_output_secret_leak_risk"
    TEST_ARTIFACT_WRITE_CONFUSION_RISK = "test_artifact_write_confusion_risk"
    BEFORE_AFTER_COMPARISON_CONFUSION_RISK = "before_after_comparison_confusion_risk"
    REPAIR_CORRECTNESS_OVERCLAIM_RISK = "repair_correctness_overclaim_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    SELF_PROMPT_EXECUTION_CONFUSION_RISK = "self_prompt_execution_confusion_risk"
    SUBAGENT_INVOCATION_CONFUSION_RISK = "subagent_invocation_confusion_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    MODEL_PROVIDER_INVOCATION_RISK = "model_provider_invocation_risk"
    AUTONOMOUS_LOOP_RUNTIME_RISK = "autonomous_loop_runtime_risk"
    RETRY_LOOP_RISK = "retry_loop_risk"
    MULTI_CYCLE_LOOP_RISK = "multi_cycle_loop_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    UNKNOWN = "unknown"


class RepairPostApplyTestCommandKind(StrEnum):
    EXISTING_V037_RUNNER_COMMAND_REF = "existing_v037_runner_command_ref"
    BOUNDED_PYTEST_SELECTION = "bounded_pytest_selection"
    BOUNDED_UNITTEST_SELECTION = "bounded_unittest_selection"
    BOUNDED_PROJECT_TEST_SKILL_REF = "bounded_project_test_skill_ref"
    BOUNDED_SMOKE_TEST_SELECTION = "bounded_smoke_test_selection"
    NO_OP = "no_op"
    UNSUPPORTED = "unsupported"
    UNKNOWN = "unknown"


class RepairPostApplyTestScopeKind(StrEnum):
    CHANGED_TARGET_RELATED_TESTS = "changed_target_related_tests"
    APPROVED_TEST_SUBSET = "approved_test_subset"
    BOUNDED_SMOKE_TESTS = "bounded_smoke_tests"
    PREVIOUSLY_FAILING_TESTS = "previously_failing_tests"
    SAFETY_REQUIRED_TESTS = "safety_required_tests"
    FULL_SUITE_FUTURE_GATE = "full_suite_future_gate"
    UNBOUNDED_SCOPE_REJECTED = "unbounded_scope_rejected"
    NO_TESTS = "no_tests"
    UNKNOWN = "unknown"


class RepairPostApplyTestOutcomeKind(StrEnum):
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    TIMED_OUT = "timed_out"
    SKIPPED = "skipped"
    BLOCKED = "blocked"
    RUNNER_UNAVAILABLE = "runner_unavailable"
    INCONCLUSIVE = "inconclusive"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairPostApplyRetestDisposition(StrEnum):
    RETEST_COMPLETED = "retest_completed"
    RETEST_COMPLETED_WITH_WARNINGS = "retest_completed_with_warnings"
    RETEST_FAILED = "retest_failed"
    RETEST_TIMED_OUT = "retest_timed_out"
    RUNNER_UNAVAILABLE = "runner_unavailable"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    REVIEW_REQUIRED = "review_required"
    DO_NOTHING_PREFERRED = "do_nothing_preferred"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


UNSAFE_FLAG_NAMES = [
    "ready_for_execution",
    "ready_for_general_execution",
    "ready_for_arbitrary_command_execution",
    "ready_for_unbounded_test_execution",
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
    "allow_arbitrary_command_execution",
    "allow_shell",
    "allow_raw_subprocess",
    "allow_dependency_install",
    "allow_network_access",
    "allow_live_workspace_test",
    "allow_unbounded_test_scope",
    "allow_workspace_creation",
    "allow_git_worktree_creation",
    "allow_git_checkout",
    "allow_branch_creation",
    "allow_filesystem_scan",
    "allow_patch_materialization",
    "allow_patch_application",
    "allow_apply_patch",
    "allow_git_apply",
    "allow_before_after_comparison",
    "allow_repair_effectiveness_assessment",
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
    "allow_repair_execution",
    "allow_dominion_runtime",
]

UNSAFE_RUN_RECORD_NAMES = [
    "raw_subprocess_used_by_v0394",
    "shell_used",
    "network_used",
    "install_performed",
    "patch_applied",
    "repair_executed",
    "self_prompt_executed",
    "subagent_invoked",
    "model_invoked",
    "external_agent_invoked",
    "dominion_runtime_invoked",
]

UNSAFE_RESULT_NAMES = [
    "arbitrary_command_executed",
    "shell_used",
    "raw_subprocess_used_by_v0394",
    "live_workspace_touched",
    "patch_applied",
    "repair_executed",
    "self_prompt_generated",
    "self_prompt_executed",
    "next_action_generated",
    "next_action_executed",
    "subagent_invoked",
    "model_invoked",
    "external_agent_invoked",
    "dominion_runtime_invoked",
    "production_certified",
    "ready_for_execution",
]

UNSAFE_DECISION_NAMES = [
    "arbitrary_command_allowed_now",
    "shell_allowed_now",
    "raw_subprocess_allowed_now",
    "dependency_install_allowed_now",
    "network_allowed_now",
    "patch_apply_allowed_now",
    "apply_patch_allowed_now",
    "git_apply_allowed_now",
    "before_after_comparison_allowed_now",
    "repair_execution_allowed_now",
    "self_prompt_generation_allowed_now",
    "self_prompt_execution_allowed_now",
    "subagent_invocation_allowed_now",
    "model_provider_invocation_allowed_now",
    "external_agent_allowed_now",
    "dominion_runtime_allowed_now",
    "production_certified",
]

UNSAFE_REPORT_NAMES = [
    "arbitrary_command_enabled",
    "shell_enabled",
    "raw_subprocess_enabled",
    "dependency_install_enabled",
    "network_enabled",
    "patch_apply_enabled",
    "apply_patch_enabled",
    "git_apply_enabled",
    "before_after_comparison_enabled",
    "repair_execution_enabled",
    "self_prompt_generation_enabled",
    "self_prompt_execution_enabled",
    "subagent_invocation_enabled",
    "model_invocation_enabled",
    "external_agent_enabled",
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
    if V0394_VERSION not in version:
        raise ValueError("version must include v0.39.4")


def _validate_list(field_name: str, value: Any) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list")


def _validate_dict(field_name: str, value: Any) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{field_name} must be a dict")


def _validate_false(instance: object, names: list[str]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must remain False in v0.39.4")


def _validate_true(instance: object, names: list[str]) -> None:
    for name in names:
        if getattr(instance, name) is not True:
            raise ValueError(f"{name} must be True in v0.39.4")


def _digest_output(stdout: str, stderr: str) -> str:
    return hashlib.sha256((stdout + "\n" + stderr).encode("utf-8")).hexdigest()


def _bounded(text: str, limit: int) -> tuple[str, bool]:
    return (text[:limit] + "...[truncated]", True) if len(text) > limit else (text, False)


@dataclass(frozen=True)
class RepairPostApplyRetestFlagSet:
    flag_set_id: str
    version: str
    post_apply_retest_layer_constructed: bool = True
    controlled_test_selection_available: bool = True
    controlled_test_command_spec_available: bool = True
    controlled_runner_invocation_available: bool = True
    bounded_test_output_capture_available: bool = True
    post_apply_test_result_envelope_available: bool = True
    post_apply_retest_audit_available: bool = True
    future_before_after_comparison_input_available: bool = True
    ready_for_v0395_before_after_repair_outcome_comparison: bool = True
    ready_for_post_apply_controlled_retest: bool = True
    ready_for_controlled_test_selection: bool = True
    ready_for_controlled_test_command_spec: bool = True
    ready_for_controlled_runner_invocation: bool = True
    ready_for_controlled_retest_execution: bool = True
    ready_for_controlled_test_subprocess: bool = True
    ready_for_bounded_test_output_capture: bool = True
    ready_for_post_apply_test_result_envelope: bool = True
    ready_for_future_before_after_comparison_input: bool = True
    ready_for_execution: bool = False
    ready_for_general_execution: bool = False
    ready_for_arbitrary_command_execution: bool = False
    ready_for_unbounded_test_execution: bool = False
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
class RepairPostApplyRetestSourceRef:
    source_ref_id: str
    source_kind: RepairPostApplyRetestSourceKind | str
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
class RepairPostApplyRetestPolicy:
    policy_id: str
    version: str
    allowed_modes: list[RepairPostApplyRetestMode | str]
    allowed_command_kinds: list[RepairPostApplyTestCommandKind | str]
    allowed_scope_kinds: list[RepairPostApplyTestScopeKind | str]
    prohibited_command_fragments: list[str]
    max_argv_items: int = 8
    max_arg_chars: int = 200
    timeout_seconds: int = 30
    max_stdout_chars: int = 4000
    max_stderr_chars: int = 4000
    require_successful_sandbox_apply_result: bool = True
    require_sandbox_apply_audit: bool = True
    require_workspace_isolation: bool = True
    require_controlled_runner: bool = True
    require_shell_false: bool = True
    require_timeout: bool = True
    require_bounded_output_capture: bool = True
    require_sandbox_cwd: bool = True
    allow_controlled_test_selection: bool = True
    allow_controlled_test_command_spec: bool = True
    allow_controlled_runner_invocation: bool = True
    allow_controlled_test_subprocess_via_runner: bool = True
    allow_bounded_test_output_capture: bool = True
    allow_post_apply_test_result_envelope: bool = True
    allow_future_before_after_comparison_input: bool = True
    allow_arbitrary_command_execution: bool = False
    allow_shell: bool = False
    allow_raw_subprocess: bool = False
    allow_dependency_install: bool = False
    allow_network_access: bool = False
    allow_live_workspace_test: bool = False
    allow_unbounded_test_scope: bool = False
    allow_workspace_creation: bool = False
    allow_git_worktree_creation: bool = False
    allow_git_checkout: bool = False
    allow_branch_creation: bool = False
    allow_filesystem_scan: bool = False
    allow_patch_materialization: bool = False
    allow_patch_application: bool = False
    allow_apply_patch: bool = False
    allow_git_apply: bool = False
    allow_before_after_comparison: bool = False
    allow_repair_effectiveness_assessment: bool = False
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
    allow_repair_execution: bool = False
    allow_dominion_runtime: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_id", self.policy_id)
        _validate_version(self.version)
        for name in ["allowed_modes", "allowed_command_kinds", "allowed_scope_kinds", "prohibited_command_fragments"]:
            _validate_list(name, getattr(self, name))
        for name in ["max_argv_items", "max_arg_chars", "timeout_seconds", "max_stdout_chars", "max_stderr_chars"]:
            if getattr(self, name) <= 0:
                raise ValueError(f"{name} must be > 0")
        _validate_dict("metadata", self.metadata)
        _validate_false(self, UNSAFE_POLICY_ALLOW_NAMES)


@dataclass(frozen=True)
class RepairPostApplyRetestInput:
    retest_input_id: str
    version: str
    sandbox_apply_result_id: str | None
    sandbox_apply_transaction_id: str | None
    sandbox_apply_audit_id: str | None
    workspace_descriptor_id: str | None
    workspace_isolation_decision_id: str | None
    sandbox_root_ref: str
    requested_mode: RepairPostApplyRetestMode | str
    requested_test_scope: RepairPostApplyTestScopeKind | str
    source_refs: list[RepairPostApplyRetestSourceRef]
    prohibited_runtime_actions: list[str]
    task_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("retest_input_id", self.retest_input_id)
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
class RepairPostApplyTestSelectionPlan:
    selection_plan_id: str
    version: str
    retest_input_id: str
    scope_kind: RepairPostApplyTestScopeKind | str
    selected_test_refs: list[str]
    changed_target_refs: list[str]
    excluded_test_refs: list[str]
    selection_summary: str
    bounded: bool
    unbounded_scope_requested: bool
    full_suite_requested: bool
    approved_by_policy: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("selection_plan_id", self.selection_plan_id)
        _validate_version(self.version)
        _require_non_blank("retest_input_id", self.retest_input_id)
        _require_non_blank("selection_summary", self.selection_summary)
        for name in ["selected_test_refs", "changed_target_refs", "excluded_test_refs", "evidence_refs"]:
            _validate_list(name, getattr(self, name))
        _validate_dict("metadata", self.metadata)
        if self.bounded is not True:
            raise ValueError("selection plan must be bounded")
        if self.unbounded_scope_requested and self.approved_by_policy:
            raise ValueError("unbounded scope cannot be approved by policy")
        if self.full_suite_requested and self.approved_by_policy and self.scope_kind != RepairPostApplyTestScopeKind.FULL_SUITE_FUTURE_GATE:
            raise ValueError("full suite requires explicit future-gated scope metadata")


@dataclass(frozen=True)
class RepairControlledTestCommandSpec:
    command_spec_id: str
    version: str
    command_kind: RepairPostApplyTestCommandKind | str
    command_label: str
    argv: list[str]
    cwd_ref: str
    timeout_seconds: int
    env_overrides: dict[str, str]
    command_summary: str
    shell: bool
    uses_runner_adapter: bool
    install_command: bool
    network_command: bool
    arbitrary_command: bool
    approved_by_policy: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("command_spec_id", self.command_spec_id)
        _validate_version(self.version)
        _require_non_blank("command_label", self.command_label)
        _require_non_blank("cwd_ref", self.cwd_ref)
        _require_non_blank("command_summary", self.command_summary)
        _validate_list("argv", self.argv)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("env_overrides", self.env_overrides)
        _validate_dict("metadata", self.metadata)
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be > 0")
        if self.shell is not False:
            raise ValueError("shell must be False")
        if self.install_command or self.network_command or self.arbitrary_command:
            if self.approved_by_policy:
                raise ValueError("unsafe command spec cannot be approved")
        if self.approved_by_policy and not self.uses_runner_adapter:
            raise ValueError("approved execution requires runner adapter")


@dataclass(frozen=True)
class RepairControlledTestRunnerInvocation:
    invocation_id: str
    version: str
    retest_input_id: str
    command_spec_id: str
    runner_ref: str | None
    invocation_summary: str
    cwd_ref: str
    shell: bool
    timeout_seconds: int
    bounded_output_capture: bool
    runner_supplied: bool
    runner_invoked: bool
    raw_subprocess_used_by_v0394: bool
    shell_used: bool
    arbitrary_command_executed: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["invocation_id", "version", "retest_input_id", "command_spec_id", "cwd_ref", "invocation_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        if self.shell is not False:
            raise ValueError("shell must be False")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be > 0")
        if self.bounded_output_capture is not True:
            raise ValueError("bounded_output_capture must be True")
        if self.runner_invoked and not self.runner_supplied:
            raise ValueError("runner_invoked requires runner_supplied")
        _validate_false(self, ["raw_subprocess_used_by_v0394", "shell_used", "arbitrary_command_executed"])


@dataclass(frozen=True)
class RepairPostApplyTestOutputCapture:
    output_capture_id: str
    version: str
    invocation_id: str
    stdout_preview: str
    stderr_preview: str
    combined_output_digest: str | None
    stdout_truncated: bool
    stderr_truncated: bool
    redacted: bool
    max_stdout_chars: int
    max_stderr_chars: int
    output_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("output_capture_id", self.output_capture_id)
        _validate_version(self.version)
        _require_non_blank("invocation_id", self.invocation_id)
        _require_non_blank("output_summary", self.output_summary)
        if self.max_stdout_chars <= 0 or self.max_stderr_chars <= 0:
            raise ValueError("output capture limits must be > 0")
        if len(self.stdout_preview) > self.max_stdout_chars + 14:
            raise ValueError("stdout preview must be bounded")
        if len(self.stderr_preview) > self.max_stderr_chars + 14:
            raise ValueError("stderr preview must be bounded")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairPostApplyRetestRunRecord:
    run_record_id: str
    version: str
    invocation_id: str
    command_spec_id: str
    status: RepairPostApplyRetestStatus | str
    outcome_kind: RepairPostApplyTestOutcomeKind | str
    exit_code: int | None
    duration_ms: int | None
    timed_out: bool
    runner_unavailable: bool
    run_summary: str
    controlled_runner_used: bool
    raw_subprocess_used_by_v0394: bool = False
    shell_used: bool = False
    network_used: bool = False
    install_performed: bool = False
    patch_applied: bool = False
    repair_executed: bool = False
    self_prompt_executed: bool = False
    subagent_invoked: bool = False
    model_invoked: bool = False
    external_agent_invoked: bool = False
    dominion_runtime_invoked: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["run_record_id", "version", "invocation_id", "command_spec_id", "run_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        if self.duration_ms is not None and self.duration_ms < 0:
            raise ValueError("duration_ms must be None or >= 0")
        if self.runner_unavailable and self.controlled_runner_used:
            raise ValueError("runner unavailable cannot also be used")
        _validate_dict("metadata", self.metadata)
        _validate_false(self, UNSAFE_RUN_RECORD_NAMES)


@dataclass(frozen=True)
class RepairPostApplyRetestResult:
    retest_result_id: str
    version: str
    run_record_id: str
    output_capture_id: str | None
    status: RepairPostApplyRetestStatus | str
    outcome_kind: RepairPostApplyTestOutcomeKind | str
    disposition: RepairPostApplyRetestDisposition | str
    result_summary: str
    selected_test_refs: list[str]
    passed_test_refs: list[str]
    failed_test_refs: list[str]
    errored_test_refs: list[str]
    skipped_test_refs: list[str]
    ready_for_future_before_after_comparison_input: bool
    tests_run_under_controlled_boundary: bool
    arbitrary_command_executed: bool = False
    shell_used: bool = False
    raw_subprocess_used_by_v0394: bool = False
    live_workspace_touched: bool = False
    patch_applied: bool = False
    repair_executed: bool = False
    self_prompt_generated: bool = False
    self_prompt_executed: bool = False
    next_action_generated: bool = False
    next_action_executed: bool = False
    subagent_invoked: bool = False
    model_invoked: bool = False
    external_agent_invoked: bool = False
    dominion_runtime_invoked: bool = False
    production_certified: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["retest_result_id", "version", "run_record_id", "result_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ["selected_test_refs", "passed_test_refs", "failed_test_refs", "errored_test_refs", "skipped_test_refs", "evidence_refs"]:
            _validate_list(name, getattr(self, name))
        _validate_dict("metadata", self.metadata)
        _validate_false(self, UNSAFE_RESULT_NAMES)


@dataclass(frozen=True)
class RepairPostApplyRetestAudit:
    audit_id: str
    version: str
    retest_input_id: str
    run_record_id: str | None
    retest_result_id: str | None
    audit_summary: str
    sandbox_apply_result_confirmed: bool
    workspace_isolation_confirmed: bool
    sandbox_cwd_confirmed: bool
    controlled_runner_confirmed: bool
    shell_false_confirmed: bool
    timeout_confirmed: bool
    bounded_output_capture_confirmed: bool
    no_arbitrary_command_confirmed: bool
    no_dependency_install_confirmed: bool
    no_network_access_confirmed: bool
    no_live_workspace_touch_confirmed: bool
    no_patch_application_confirmed: bool
    no_apply_patch_confirmed: bool
    no_git_apply_confirmed: bool
    no_repair_execution_confirmed: bool
    no_self_prompt_execution_confirmed: bool
    no_subagent_invocation_confirmed: bool
    no_model_invocation_confirmed: bool
    no_external_agent_confirmed: bool
    no_dominion_runtime_confirmed: bool
    no_production_certification_confirmed: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["audit_id", "version", "retest_input_id", "audit_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        _validate_true(
            self,
            [
                "no_arbitrary_command_confirmed",
                "no_dependency_install_confirmed",
                "no_network_access_confirmed",
                "no_live_workspace_touch_confirmed",
                "no_patch_application_confirmed",
                "no_apply_patch_confirmed",
                "no_git_apply_confirmed",
                "no_repair_execution_confirmed",
                "no_self_prompt_execution_confirmed",
                "no_subagent_invocation_confirmed",
                "no_model_invocation_confirmed",
                "no_external_agent_confirmed",
                "no_dominion_runtime_confirmed",
                "no_production_certification_confirmed",
            ],
        )


@dataclass(frozen=True)
class RepairPostApplyRetestDecision:
    retest_decision_id: str
    version: str
    decision_kind: RepairPostApplyRetestDecisionKind | str
    status: RepairPostApplyRetestStatus | str
    readiness_level: RepairPostApplyRetestReadinessLevel | str
    disposition: RepairPostApplyRetestDisposition | str
    decision_summary: str
    rationale_summary: str
    confidence: str
    evidence_refs: list[str]
    ready_for_future_before_after_comparison_input: bool
    controlled_retest_allowed_now: bool
    controlled_runner_invocation_allowed_now: bool
    controlled_test_subprocess_allowed_now: bool
    arbitrary_command_allowed_now: bool = False
    shell_allowed_now: bool = False
    raw_subprocess_allowed_now: bool = False
    dependency_install_allowed_now: bool = False
    network_allowed_now: bool = False
    patch_apply_allowed_now: bool = False
    apply_patch_allowed_now: bool = False
    git_apply_allowed_now: bool = False
    before_after_comparison_allowed_now: bool = False
    repair_execution_allowed_now: bool = False
    self_prompt_generation_allowed_now: bool = False
    self_prompt_execution_allowed_now: bool = False
    subagent_invocation_allowed_now: bool = False
    model_provider_invocation_allowed_now: bool = False
    external_agent_allowed_now: bool = False
    dominion_runtime_allowed_now: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["retest_decision_id", "version", "decision_summary", "rationale_summary", "confidence"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        _validate_false(self, UNSAFE_DECISION_NAMES)


@dataclass(frozen=True)
class V0394ReadinessReport:
    report_id: str
    version: str
    release_name: str
    track_name: str
    selection_plan: RepairPostApplyTestSelectionPlan | None
    command_spec: RepairControlledTestCommandSpec | None
    invocation: RepairControlledTestRunnerInvocation | None
    output_capture: RepairPostApplyTestOutputCapture | None
    run_record: RepairPostApplyRetestRunRecord | None
    retest_result: RepairPostApplyRetestResult | None
    audit: RepairPostApplyRetestAudit | None
    decision: RepairPostApplyRetestDecision
    flags: RepairPostApplyRetestFlagSet
    source_refs: list[RepairPostApplyRetestSourceRef]
    report_summary: str
    ready_for_v0395_before_after_repair_outcome_comparison: bool
    ready_for_controlled_test_selection: bool
    ready_for_controlled_test_command_spec: bool
    ready_for_controlled_runner_invocation: bool
    ready_for_controlled_retest_execution: bool
    ready_for_bounded_test_output_capture: bool
    ready_for_post_apply_test_result_envelope: bool
    ready_for_future_before_after_comparison_input: bool
    controlled_retest_completed: bool
    controlled_runner_invocation_enabled: bool
    controlled_test_subprocess_enabled: bool
    arbitrary_command_enabled: bool = False
    shell_enabled: bool = False
    raw_subprocess_enabled: bool = False
    dependency_install_enabled: bool = False
    network_enabled: bool = False
    patch_apply_enabled: bool = False
    apply_patch_enabled: bool = False
    git_apply_enabled: bool = False
    before_after_comparison_enabled: bool = False
    repair_execution_enabled: bool = False
    self_prompt_generation_enabled: bool = False
    self_prompt_execution_enabled: bool = False
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
        _validate_false(self, UNSAFE_REPORT_NAMES)


@dataclass(frozen=True)
class RepairPostApplyRetestValidationFinding:
    finding_id: str
    finding_summary: str
    risk_kind: RepairPostApplyRetestRiskKind | str
    blocked: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("finding_summary", self.finding_summary)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairPostApplyRetestValidationReport:
    validation_report_id: str
    version: str
    validation_summary: str
    findings: list[RepairPostApplyRetestValidationFinding]
    confirms_successful_sandbox_apply_input: bool = True
    confirms_workspace_isolation: bool = True
    confirms_controlled_runner: bool = True
    confirms_shell_false: bool = True
    confirms_timeout: bool = True
    confirms_bounded_output_capture: bool = True
    confirms_no_arbitrary_command: bool = True
    confirms_no_shell: bool = True
    confirms_no_raw_subprocess: bool = True
    confirms_no_dependency_install: bool = True
    confirms_no_network: bool = True
    confirms_no_live_workspace_touch: bool = True
    confirms_no_patch_application: bool = True
    confirms_no_apply_patch: bool = True
    confirms_no_git_apply: bool = True
    confirms_no_before_after_comparison: bool = True
    confirms_no_repair_execution: bool = True
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
        _validate_true(self, [name for name in vars(self) if name.startswith("confirms_")])


@dataclass(frozen=True)
class RepairPostApplyRetestRunPreview:
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
class RepairPostApplyRetestControlledOnlyGuarantee:
    guarantee_id: str
    version: str
    guarantee_summary: str
    no_arbitrary_command: bool = True
    no_shell: bool = True
    no_raw_subprocess: bool = True
    no_dependency_install: bool = True
    no_network_access: bool = True
    no_live_workspace_touch: bool = True
    no_patch_application: bool = True
    no_apply_patch: bool = True
    no_git_apply: bool = True
    no_before_after_comparison: bool = True
    no_repair_execution: bool = True
    no_self_prompt_execution: bool = True
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
        _validate_true(self, [name for name in vars(self) if name.startswith("no_")])


ControlledRunner = Callable[[list[str], str, int, dict[str, str]], dict[str, Any]]


def build_repair_post_apply_retest_flags(**overrides: Any) -> RepairPostApplyRetestFlagSet:
    defaults = {"flag_set_id": "v0394-post-apply-retest-flags", "version": V0394_VERSION}
    return RepairPostApplyRetestFlagSet(**_with_overrides(defaults, overrides))


def build_repair_post_apply_retest_source_ref(**overrides: Any) -> RepairPostApplyRetestSourceRef:
    defaults = {
        "source_ref_id": "v0394-source-ref",
        "source_kind": RepairPostApplyRetestSourceKind.V0393_SANDBOX_APPLY_RESULT,
        "source_id": "v0393-apply-result",
        "source_summary": "v0.39.3 sandbox apply result supplies future post-apply controlled re-test input.",
        "evidence_refs": ["v0393-apply-result"],
    }
    return RepairPostApplyRetestSourceRef(**_with_overrides(defaults, overrides))


def default_repair_post_apply_retest_policy(**overrides: Any) -> RepairPostApplyRetestPolicy:
    defaults = {
        "policy_id": "v0394-post-apply-retest-policy",
        "version": V0394_VERSION,
        "allowed_modes": [
            RepairPostApplyRetestMode.POST_APPLY_CONTROLLED_RETEST,
            RepairPostApplyRetestMode.CONTROLLED_TEST_SELECTION,
            RepairPostApplyRetestMode.CONTROLLED_TEST_COMMAND_SPEC,
            RepairPostApplyRetestMode.CONTROLLED_RUNNER_INVOCATION,
            RepairPostApplyRetestMode.BOUNDED_TEST_OUTPUT_CAPTURE,
            RepairPostApplyRetestMode.POST_APPLY_TEST_RESULT_ENVELOPE,
            RepairPostApplyRetestMode.POST_APPLY_RETEST_AUDIT,
            RepairPostApplyRetestMode.FUTURE_BEFORE_AFTER_COMPARISON_INPUT,
        ],
        "allowed_command_kinds": [
            RepairPostApplyTestCommandKind.EXISTING_V037_RUNNER_COMMAND_REF,
            RepairPostApplyTestCommandKind.BOUNDED_PYTEST_SELECTION,
            RepairPostApplyTestCommandKind.BOUNDED_UNITTEST_SELECTION,
            RepairPostApplyTestCommandKind.BOUNDED_PROJECT_TEST_SKILL_REF,
            RepairPostApplyTestCommandKind.BOUNDED_SMOKE_TEST_SELECTION,
        ],
        "allowed_scope_kinds": [
            RepairPostApplyTestScopeKind.CHANGED_TARGET_RELATED_TESTS,
            RepairPostApplyTestScopeKind.APPROVED_TEST_SUBSET,
            RepairPostApplyTestScopeKind.BOUNDED_SMOKE_TESTS,
            RepairPostApplyTestScopeKind.PREVIOUSLY_FAILING_TESTS,
            RepairPostApplyTestScopeKind.SAFETY_REQUIRED_TESTS,
        ],
        "prohibited_command_fragments": [
            "shell-control",
            "package-manager",
            "network-fetch",
            "patch-application-tool",
            "git-apply-tool",
        ],
    }
    return RepairPostApplyRetestPolicy(**_with_overrides(defaults, overrides))


def build_repair_post_apply_retest_policy(**overrides: Any) -> RepairPostApplyRetestPolicy:
    return default_repair_post_apply_retest_policy(**overrides)


def build_repair_post_apply_retest_input(**overrides: Any) -> RepairPostApplyRetestInput:
    defaults = {
        "retest_input_id": "v0394-retest-input",
        "version": V0394_VERSION,
        "sandbox_apply_result_id": "v0393-apply-result",
        "sandbox_apply_transaction_id": "v0393-transaction",
        "sandbox_apply_audit_id": "v0393-audit",
        "workspace_descriptor_id": "v0392-workspace-descriptor",
        "workspace_isolation_decision_id": "v0392-workspace-decision",
        "sandbox_root_ref": "sandbox-root",
        "requested_mode": RepairPostApplyRetestMode.POST_APPLY_CONTROLLED_RETEST,
        "requested_test_scope": RepairPostApplyTestScopeKind.CHANGED_TARGET_RELATED_TESTS,
        "source_refs": [build_repair_post_apply_retest_source_ref()],
        "prohibited_runtime_actions": list(PROHIBITED_RUNTIME_ACTIONS),
        "task_summary": "Run a bounded post-apply re-test through an injected controlled runner boundary.",
    }
    return RepairPostApplyRetestInput(**_with_overrides(defaults, overrides))


def build_repair_post_apply_test_selection_plan(**overrides: Any) -> RepairPostApplyTestSelectionPlan:
    scope_kind = overrides.get("scope_kind", RepairPostApplyTestScopeKind.CHANGED_TARGET_RELATED_TESTS)
    unbounded = scope_kind == RepairPostApplyTestScopeKind.UNBOUNDED_SCOPE_REJECTED
    full_suite = scope_kind == RepairPostApplyTestScopeKind.FULL_SUITE_FUTURE_GATE
    defaults = {
        "selection_plan_id": "v0394-selection-plan",
        "version": V0394_VERSION,
        "retest_input_id": "v0394-retest-input",
        "scope_kind": scope_kind,
        "selected_test_refs": ["tests/test_changed_target.py::test_smoke"],
        "changed_target_refs": ["sandbox-root/example.py"],
        "excluded_test_refs": [],
        "selection_summary": "Bounded changed-target related post-apply test selection.",
        "bounded": True,
        "unbounded_scope_requested": unbounded,
        "full_suite_requested": full_suite,
        "approved_by_policy": not unbounded,
        "evidence_refs": ["v0393-apply-result"],
    }
    return RepairPostApplyTestSelectionPlan(**_with_overrides(defaults, overrides))


def create_repair_post_apply_test_selection_plan(retest_input: RepairPostApplyRetestInput) -> RepairPostApplyTestSelectionPlan:
    return build_repair_post_apply_test_selection_plan(
        retest_input_id=retest_input.retest_input_id,
        scope_kind=retest_input.requested_test_scope,
    )


def build_repair_controlled_test_command_spec(**overrides: Any) -> RepairControlledTestCommandSpec:
    defaults = {
        "command_spec_id": "v0394-command-spec",
        "version": V0394_VERSION,
        "command_kind": RepairPostApplyTestCommandKind.BOUNDED_PYTEST_SELECTION,
        "command_label": "bounded changed-target pytest selection",
        "argv": ["python", "-m", "pytest", "tests/test_changed_target.py::test_smoke"],
        "cwd_ref": "sandbox-root",
        "timeout_seconds": 30,
        "env_overrides": {},
        "command_summary": "Bounded argv for controlled runner adapter; not shell command execution.",
        "shell": False,
        "uses_runner_adapter": True,
        "install_command": False,
        "network_command": False,
        "arbitrary_command": False,
        "approved_by_policy": True,
        "evidence_refs": ["v0394-selection-plan"],
    }
    return RepairControlledTestCommandSpec(**_with_overrides(defaults, overrides))


def create_repair_controlled_test_command_spec(
    selection_plan: RepairPostApplyTestSelectionPlan,
    policy: RepairPostApplyRetestPolicy | None = None,
) -> RepairControlledTestCommandSpec:
    policy = policy or default_repair_post_apply_retest_policy()
    argv = ["python", "-m", "pytest", *selection_plan.selected_test_refs]
    unsafe_fragment = any(fragment in " ".join(argv) for fragment in policy.prohibited_command_fragments)
    return build_repair_controlled_test_command_spec(
        argv=argv[: policy.max_argv_items],
        timeout_seconds=policy.timeout_seconds,
        approved_by_policy=selection_plan.approved_by_policy and not unsafe_fragment,
    )


def build_repair_controlled_test_runner_invocation(**overrides: Any) -> RepairControlledTestRunnerInvocation:
    defaults = {
        "invocation_id": "v0394-runner-invocation",
        "version": V0394_VERSION,
        "retest_input_id": "v0394-retest-input",
        "command_spec_id": "v0394-command-spec",
        "runner_ref": "injected-controlled-runner",
        "invocation_summary": "Controlled runner invocation metadata with shell false and bounded output capture.",
        "cwd_ref": "sandbox-root",
        "shell": False,
        "timeout_seconds": 30,
        "bounded_output_capture": True,
        "runner_supplied": True,
        "runner_invoked": False,
        "raw_subprocess_used_by_v0394": False,
        "shell_used": False,
        "arbitrary_command_executed": False,
        "evidence_refs": ["v0394-command-spec"],
    }
    return RepairControlledTestRunnerInvocation(**_with_overrides(defaults, overrides))


def create_repair_controlled_runner_invocation(
    retest_input: RepairPostApplyRetestInput,
    command_spec: RepairControlledTestCommandSpec,
    runner: ControlledRunner | None = None,
) -> RepairControlledTestRunnerInvocation:
    return build_repair_controlled_test_runner_invocation(
        retest_input_id=retest_input.retest_input_id,
        command_spec_id=command_spec.command_spec_id,
        runner_ref="injected-controlled-runner" if runner else None,
        cwd_ref=command_spec.cwd_ref,
        timeout_seconds=command_spec.timeout_seconds,
        runner_supplied=runner is not None,
        runner_invoked=False,
    )


def build_repair_post_apply_test_output_capture(**overrides: Any) -> RepairPostApplyTestOutputCapture:
    stdout = overrides.pop("stdout", "1 passed")
    stderr = overrides.pop("stderr", "")
    max_stdout = overrides.get("max_stdout_chars", 4000)
    max_stderr = overrides.get("max_stderr_chars", 4000)
    stdout_preview, stdout_truncated = _bounded(stdout, max_stdout)
    stderr_preview, stderr_truncated = _bounded(stderr, max_stderr)
    defaults = {
        "output_capture_id": "v0394-output-capture",
        "version": V0394_VERSION,
        "invocation_id": "v0394-runner-invocation",
        "stdout_preview": stdout_preview,
        "stderr_preview": stderr_preview,
        "combined_output_digest": _digest_output(stdout, stderr),
        "stdout_truncated": stdout_truncated,
        "stderr_truncated": stderr_truncated,
        "redacted": True,
        "max_stdout_chars": max_stdout,
        "max_stderr_chars": max_stderr,
        "output_summary": "Bounded and redacted controlled test output capture.",
    }
    return RepairPostApplyTestOutputCapture(**_with_overrides(defaults, overrides))


def capture_repair_post_apply_test_output(
    invocation: RepairControlledTestRunnerInvocation,
    stdout: str,
    stderr: str,
    policy: RepairPostApplyRetestPolicy | None = None,
) -> RepairPostApplyTestOutputCapture:
    policy = policy or default_repair_post_apply_retest_policy()
    return build_repair_post_apply_test_output_capture(
        invocation_id=invocation.invocation_id,
        stdout=stdout,
        stderr=stderr,
        max_stdout_chars=policy.max_stdout_chars,
        max_stderr_chars=policy.max_stderr_chars,
    )


def build_repair_post_apply_retest_run_record(**overrides: Any) -> RepairPostApplyRetestRunRecord:
    defaults = {
        "run_record_id": "v0394-run-record",
        "version": V0394_VERSION,
        "invocation_id": "v0394-runner-invocation",
        "command_spec_id": "v0394-command-spec",
        "status": RepairPostApplyRetestStatus.CONTROLLED_RETEST_COMPLETED,
        "outcome_kind": RepairPostApplyTestOutcomeKind.PASSED,
        "exit_code": 0,
        "duration_ms": 10,
        "timed_out": False,
        "runner_unavailable": False,
        "run_summary": "Controlled post-apply re-test completed through supplied runner boundary.",
        "controlled_runner_used": True,
    }
    return RepairPostApplyRetestRunRecord(**_with_overrides(defaults, overrides))


def build_repair_post_apply_retest_result(**overrides: Any) -> RepairPostApplyRetestResult:
    defaults = {
        "retest_result_id": "v0394-retest-result",
        "version": V0394_VERSION,
        "run_record_id": "v0394-run-record",
        "output_capture_id": "v0394-output-capture",
        "status": RepairPostApplyRetestStatus.READY_FOR_FUTURE_BEFORE_AFTER_COMPARISON,
        "outcome_kind": RepairPostApplyTestOutcomeKind.PASSED,
        "disposition": RepairPostApplyRetestDisposition.RETEST_COMPLETED,
        "result_summary": "Controlled re-test result envelope; not repair correctness proof.",
        "selected_test_refs": ["tests/test_changed_target.py::test_smoke"],
        "passed_test_refs": ["tests/test_changed_target.py::test_smoke"],
        "failed_test_refs": [],
        "errored_test_refs": [],
        "skipped_test_refs": [],
        "ready_for_future_before_after_comparison_input": True,
        "tests_run_under_controlled_boundary": True,
        "evidence_refs": ["v0394-run-record", "v0394-output-capture"],
    }
    return RepairPostApplyRetestResult(**_with_overrides(defaults, overrides))


def build_repair_post_apply_retest_audit(**overrides: Any) -> RepairPostApplyRetestAudit:
    defaults = {
        "audit_id": "v0394-retest-audit",
        "version": V0394_VERSION,
        "retest_input_id": "v0394-retest-input",
        "run_record_id": "v0394-run-record",
        "retest_result_id": "v0394-retest-result",
        "audit_summary": "Audit confirms controlled runner re-test and blocked unsafe surfaces.",
        "sandbox_apply_result_confirmed": True,
        "workspace_isolation_confirmed": True,
        "sandbox_cwd_confirmed": True,
        "controlled_runner_confirmed": True,
        "shell_false_confirmed": True,
        "timeout_confirmed": True,
        "bounded_output_capture_confirmed": True,
        "no_arbitrary_command_confirmed": True,
        "no_dependency_install_confirmed": True,
        "no_network_access_confirmed": True,
        "no_live_workspace_touch_confirmed": True,
        "no_patch_application_confirmed": True,
        "no_apply_patch_confirmed": True,
        "no_git_apply_confirmed": True,
        "no_repair_execution_confirmed": True,
        "no_self_prompt_execution_confirmed": True,
        "no_subagent_invocation_confirmed": True,
        "no_model_invocation_confirmed": True,
        "no_external_agent_confirmed": True,
        "no_dominion_runtime_confirmed": True,
        "no_production_certification_confirmed": True,
        "evidence_refs": ["v0394-run-record", "v0394-retest-result"],
    }
    return RepairPostApplyRetestAudit(**_with_overrides(defaults, overrides))


def run_post_apply_controlled_retest(
    retest_input: RepairPostApplyRetestInput,
    command_spec: RepairControlledTestCommandSpec,
    runner: ControlledRunner | None = None,
    policy: RepairPostApplyRetestPolicy | None = None,
) -> tuple[RepairControlledTestRunnerInvocation, RepairPostApplyRetestRunRecord, RepairPostApplyTestOutputCapture, RepairPostApplyRetestResult]:
    policy = policy or default_repair_post_apply_retest_policy()
    invocation = create_repair_controlled_runner_invocation(retest_input, command_spec, runner)
    gates_pass = all(
        [
            retest_input.sandbox_apply_result_id,
            retest_input.sandbox_apply_audit_id,
            retest_input.workspace_isolation_decision_id,
            command_spec.approved_by_policy,
            command_spec.shell is False,
            command_spec.uses_runner_adapter,
            command_spec.timeout_seconds > 0,
        ]
    )
    if runner is None:
        record = build_repair_post_apply_retest_run_record(
            invocation_id=invocation.invocation_id,
            command_spec_id=command_spec.command_spec_id,
            status=RepairPostApplyRetestStatus.CONTROLLED_RUNNER_UNAVAILABLE,
            outcome_kind=RepairPostApplyTestOutcomeKind.RUNNER_UNAVAILABLE,
            exit_code=None,
            duration_ms=None,
            timed_out=False,
            runner_unavailable=True,
            run_summary="Controlled runner unavailable; no re-test execution performed.",
            controlled_runner_used=False,
        )
        capture = capture_repair_post_apply_test_output(invocation, "", "controlled runner unavailable", policy)
        result = build_repair_post_apply_retest_result(
            run_record_id=record.run_record_id,
            output_capture_id=capture.output_capture_id,
            status=RepairPostApplyRetestStatus.CONTROLLED_RUNNER_UNAVAILABLE,
            outcome_kind=RepairPostApplyTestOutcomeKind.RUNNER_UNAVAILABLE,
            disposition=RepairPostApplyRetestDisposition.RUNNER_UNAVAILABLE,
            result_summary="Runner unavailable; future comparison input is not ready.",
            passed_test_refs=[],
            ready_for_future_before_after_comparison_input=False,
            tests_run_under_controlled_boundary=False,
        )
        return invocation, record, capture, result
    if not gates_pass:
        record = build_repair_post_apply_retest_run_record(
            invocation_id=invocation.invocation_id,
            command_spec_id=command_spec.command_spec_id,
            status=RepairPostApplyRetestStatus.CONTROLLED_RETEST_BLOCKED,
            outcome_kind=RepairPostApplyTestOutcomeKind.BLOCKED,
            exit_code=None,
            duration_ms=None,
            timed_out=False,
            runner_unavailable=False,
            run_summary="Controlled re-test blocked by gate failure.",
            controlled_runner_used=False,
        )
        capture = capture_repair_post_apply_test_output(invocation, "", "controlled re-test blocked", policy)
        result = build_repair_post_apply_retest_result(
            run_record_id=record.run_record_id,
            output_capture_id=capture.output_capture_id,
            status=RepairPostApplyRetestStatus.CONTROLLED_RETEST_BLOCKED,
            outcome_kind=RepairPostApplyTestOutcomeKind.BLOCKED,
            disposition=RepairPostApplyRetestDisposition.BLOCKED,
            result_summary="Gate failure blocked controlled re-test.",
            passed_test_refs=[],
            ready_for_future_before_after_comparison_input=False,
            tests_run_under_controlled_boundary=False,
        )
        return invocation, record, capture, result

    invocation = build_repair_controlled_test_runner_invocation(
        retest_input_id=retest_input.retest_input_id,
        command_spec_id=command_spec.command_spec_id,
        cwd_ref=command_spec.cwd_ref,
        timeout_seconds=command_spec.timeout_seconds,
        runner_supplied=True,
        runner_invoked=True,
    )
    runner_result = runner(command_spec.argv, command_spec.cwd_ref, command_spec.timeout_seconds, command_spec.env_overrides)
    stdout = str(runner_result.get("stdout", ""))
    stderr = str(runner_result.get("stderr", ""))
    exit_code = runner_result.get("exit_code")
    timed_out = bool(runner_result.get("timed_out", False))
    duration_ms = runner_result.get("duration_ms", 0)
    if timed_out:
        status = RepairPostApplyRetestStatus.CONTROLLED_RETEST_TIMED_OUT
        outcome = RepairPostApplyTestOutcomeKind.TIMED_OUT
        disposition = RepairPostApplyRetestDisposition.RETEST_TIMED_OUT
    elif exit_code == 0:
        status = RepairPostApplyRetestStatus.CONTROLLED_RETEST_COMPLETED
        outcome = RepairPostApplyTestOutcomeKind.PASSED
        disposition = RepairPostApplyRetestDisposition.RETEST_COMPLETED
    else:
        status = RepairPostApplyRetestStatus.CONTROLLED_RETEST_FAILED
        outcome = RepairPostApplyTestOutcomeKind.FAILED
        disposition = RepairPostApplyRetestDisposition.RETEST_FAILED
    record = build_repair_post_apply_retest_run_record(
        invocation_id=invocation.invocation_id,
        command_spec_id=command_spec.command_spec_id,
        status=status,
        outcome_kind=outcome,
        exit_code=exit_code,
        duration_ms=duration_ms,
        timed_out=timed_out,
        runner_unavailable=False,
        controlled_runner_used=True,
    )
    capture = capture_repair_post_apply_test_output(invocation, stdout, stderr, policy)
    result = build_repair_post_apply_retest_result(
        run_record_id=record.run_record_id,
        output_capture_id=capture.output_capture_id,
        status=RepairPostApplyRetestStatus.READY_FOR_FUTURE_BEFORE_AFTER_COMPARISON,
        outcome_kind=outcome,
        disposition=disposition,
        passed_test_refs=["tests/test_changed_target.py::test_smoke"] if outcome == RepairPostApplyTestOutcomeKind.PASSED else [],
        failed_test_refs=["tests/test_changed_target.py::test_smoke"] if outcome == RepairPostApplyTestOutcomeKind.FAILED else [],
        errored_test_refs=[],
        ready_for_future_before_after_comparison_input=status in {
            RepairPostApplyRetestStatus.CONTROLLED_RETEST_COMPLETED,
            RepairPostApplyRetestStatus.CONTROLLED_RETEST_FAILED,
            RepairPostApplyRetestStatus.CONTROLLED_RETEST_TIMED_OUT,
        },
        tests_run_under_controlled_boundary=True,
    )
    return invocation, record, capture, result


def audit_post_apply_controlled_retest(
    retest_input: RepairPostApplyRetestInput,
    run_record: RepairPostApplyRetestRunRecord,
    result: RepairPostApplyRetestResult,
) -> RepairPostApplyRetestAudit:
    return build_repair_post_apply_retest_audit(
        retest_input_id=retest_input.retest_input_id,
        run_record_id=run_record.run_record_id,
        retest_result_id=result.retest_result_id,
        controlled_runner_confirmed=run_record.controlled_runner_used,
    )


def build_repair_post_apply_retest_decision(**overrides: Any) -> RepairPostApplyRetestDecision:
    defaults = {
        "retest_decision_id": "v0394-retest-decision",
        "version": V0394_VERSION,
        "decision_kind": RepairPostApplyRetestDecisionKind.ALLOW_FUTURE_BEFORE_AFTER_COMPARISON_INPUT,
        "status": RepairPostApplyRetestStatus.READY_FOR_FUTURE_BEFORE_AFTER_COMPARISON,
        "readiness_level": RepairPostApplyRetestReadinessLevel.FUTURE_BEFORE_AFTER_COMPARISON_INPUT_READY,
        "disposition": RepairPostApplyRetestDisposition.RETEST_COMPLETED,
        "decision_summary": "Controlled re-test completed and may feed future before/after comparison metadata.",
        "rationale_summary": "Re-test ran through supplied controlled runner boundary only; no correctness proof is claimed.",
        "confidence": "high",
        "evidence_refs": ["v0394-retest-result"],
        "ready_for_future_before_after_comparison_input": True,
        "controlled_retest_allowed_now": True,
        "controlled_runner_invocation_allowed_now": True,
        "controlled_test_subprocess_allowed_now": True,
    }
    return RepairPostApplyRetestDecision(**_with_overrides(defaults, overrides))


def decide_repair_post_apply_retest(result: RepairPostApplyRetestResult) -> RepairPostApplyRetestDecision:
    ready = result.ready_for_future_before_after_comparison_input and result.tests_run_under_controlled_boundary
    return build_repair_post_apply_retest_decision(
        decision_kind=RepairPostApplyRetestDecisionKind.ALLOW_FUTURE_BEFORE_AFTER_COMPARISON_INPUT if ready else RepairPostApplyRetestDecisionKind.REQUIRE_REVIEW,
        status=RepairPostApplyRetestStatus.READY_FOR_FUTURE_BEFORE_AFTER_COMPARISON if ready else RepairPostApplyRetestStatus.REVIEW_REQUIRED,
        readiness_level=RepairPostApplyRetestReadinessLevel.FUTURE_BEFORE_AFTER_COMPARISON_INPUT_READY if ready else RepairPostApplyRetestReadinessLevel.NOT_READY,
        disposition=RepairPostApplyRetestDisposition.RETEST_COMPLETED if ready else RepairPostApplyRetestDisposition.REVIEW_REQUIRED,
        ready_for_future_before_after_comparison_input=ready,
        controlled_retest_allowed_now=ready,
        controlled_runner_invocation_allowed_now=ready,
        controlled_test_subprocess_allowed_now=ready,
        confidence="high" if ready else "low",
    )


def build_repair_post_apply_retest_validation_finding(**overrides: Any) -> RepairPostApplyRetestValidationFinding:
    defaults = {
        "finding_id": "v0394-validation-finding",
        "finding_summary": "Controlled re-test is bounded to supplied runner and blocks arbitrary/runtime surfaces.",
        "risk_kind": RepairPostApplyRetestRiskKind.ARBITRARY_COMMAND_EXECUTION_RISK,
        "blocked": True,
    }
    return RepairPostApplyRetestValidationFinding(**_with_overrides(defaults, overrides))


def build_repair_post_apply_retest_validation_report(**overrides: Any) -> RepairPostApplyRetestValidationReport:
    defaults = {
        "validation_report_id": "v0394-validation-report",
        "version": V0394_VERSION,
        "validation_summary": "Validation confirms controlled runner, shell false, timeout, bounded output, and blocked runtime surfaces.",
        "findings": [build_repair_post_apply_retest_validation_finding()],
    }
    return RepairPostApplyRetestValidationReport(**_with_overrides(defaults, overrides))


def build_repair_post_apply_retest_run_preview(**overrides: Any) -> RepairPostApplyRetestRunPreview:
    defaults = {
        "run_preview_id": "v0394-run-preview",
        "version": V0394_VERSION,
        "preview_summary": "Preview controlled post-apply re-test through supplied runner boundary.",
        "preview_steps": [
            "RetestInput",
            "TestSelectionPlan",
            "ControlledTestCommandSpec",
            "ControlledRunnerInvocation",
            "ControlledRetestRunRecord",
            "OutputCapture",
            "PostApplyRetestResult",
            "RetestAudit",
        ],
    }
    return RepairPostApplyRetestRunPreview(**_with_overrides(defaults, overrides))


def build_repair_post_apply_retest_controlled_only_guarantee(**overrides: Any) -> RepairPostApplyRetestControlledOnlyGuarantee:
    defaults = {
        "guarantee_id": "v0394-controlled-only-guarantee",
        "version": V0394_VERSION,
        "guarantee_summary": "v0.39.4 uses only controlled runner boundary and blocks arbitrary/runtime surfaces.",
    }
    return RepairPostApplyRetestControlledOnlyGuarantee(**_with_overrides(defaults, overrides))


def build_v0394_readiness_report(**overrides: Any) -> V0394ReadinessReport:
    retest_input = overrides.pop("retest_input", build_repair_post_apply_retest_input())
    selection = create_repair_post_apply_test_selection_plan(retest_input)
    command = create_repair_controlled_test_command_spec(selection)
    invocation = build_repair_controlled_test_runner_invocation()
    capture = build_repair_post_apply_test_output_capture()
    record = build_repair_post_apply_retest_run_record()
    result = build_repair_post_apply_retest_result()
    audit = build_repair_post_apply_retest_audit()
    decision = decide_repair_post_apply_retest(result)
    defaults = {
        "report_id": "v0394-readiness-report",
        "version": V0394_VERSION,
        "release_name": V0394_RELEASE_NAME,
        "track_name": V039_TRACK_NAME,
        "selection_plan": selection,
        "command_spec": command,
        "invocation": invocation,
        "output_capture": capture,
        "run_record": record,
        "retest_result": result,
        "audit": audit,
        "decision": decision,
        "flags": build_repair_post_apply_retest_flags(),
        "source_refs": [build_repair_post_apply_retest_source_ref()],
        "report_summary": "v0.39.4 controlled re-test result is ready for future v0.39.5 comparison input only.",
        "ready_for_v0395_before_after_repair_outcome_comparison": True,
        "ready_for_controlled_test_selection": True,
        "ready_for_controlled_test_command_spec": True,
        "ready_for_controlled_runner_invocation": True,
        "ready_for_controlled_retest_execution": True,
        "ready_for_bounded_test_output_capture": True,
        "ready_for_post_apply_test_result_envelope": True,
        "ready_for_future_before_after_comparison_input": True,
        "controlled_retest_completed": True,
        "controlled_runner_invocation_enabled": True,
        "controlled_test_subprocess_enabled": True,
    }
    return V0394ReadinessReport(**_with_overrides(defaults, overrides))


def repair_post_apply_retest_flags_preserve_no_arbitrary_execution(flags: RepairPostApplyRetestFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_FLAG_NAMES)


def repair_post_apply_retest_policy_blocks_arbitrary_runtime(policy: RepairPostApplyRetestPolicy) -> bool:
    return all(getattr(policy, name) is False for name in UNSAFE_POLICY_ALLOW_NAMES)


def repair_controlled_test_command_spec_is_shell_free(spec: RepairControlledTestCommandSpec) -> bool:
    return spec.shell is False and not spec.install_command and not spec.network_command and not spec.arbitrary_command


def repair_controlled_runner_invocation_is_not_raw_subprocess(invocation: RepairControlledTestRunnerInvocation) -> bool:
    return not invocation.raw_subprocess_used_by_v0394 and not invocation.shell_used and not invocation.arbitrary_command_executed


def repair_post_apply_retest_result_is_not_repair_correctness_proof(result: RepairPostApplyRetestResult) -> bool:
    return all(getattr(result, name) is False for name in UNSAFE_RESULT_NAMES)


def v0394_readiness_report_is_not_general_execution_ready(report: V0394ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_REPORT_NAMES) and repair_post_apply_retest_flags_preserve_no_arbitrary_execution(report.flags)
