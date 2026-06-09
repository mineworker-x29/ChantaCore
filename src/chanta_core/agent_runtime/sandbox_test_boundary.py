from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list


V0370_VERSION = "v0.37.0"
V0370_RELEASE_NAME = "v0.37.0 Controlled Sandbox Test Runner Boundary Foundation"


UNSAFE_FLAG_NAMES = (
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
    "allow_controlled_test_subprocess",
    "allow_pytest_execution",
    "allow_npm_test_execution",
    "allow_unittest_execution",
    "allow_shell",
    "allow_arbitrary_command",
    "allow_dependency_install",
    "allow_network_access",
    "allow_live_workspace_write",
    "allow_patch_application",
    "allow_automatic_repair",
    "allow_multi_cycle_loop",
    "allow_vera_codex_trial_execution",
    "allow_external_agent_execution",
    "allow_dominion_runtime",
)

UNSAFE_DECISION_ALLOW_NAMES = (
    "test_execution_allowed",
    "controlled_test_subprocess_allowed",
    "shell_execution_allowed",
    "subprocess_allowed",
    "command_execution_allowed",
    "dependency_install_allowed",
    "network_access_allowed",
    "live_workspace_write_allowed",
    "patch_application_allowed",
    "automatic_repair_allowed",
    "multi_cycle_loop_allowed",
    "vera_codex_trial_execution_allowed",
    "external_agent_execution_allowed",
    "dominion_runtime_allowed",
)


class SandboxTestRunnerTrackKind(StrEnum):
    BOUNDARY_FOUNDATION = "boundary_foundation"
    ALLOWLISTED_TEST_COMMAND_POLICY = "allowlisted_test_command_policy"
    SANDBOX_TEST_EXECUTION_ENGINE = "sandbox_test_execution_engine"
    TEST_RESULT_ENVELOPE = "test_result_envelope"
    TEST_FEEDBACK_FAILURE_DIAGNOSIS = "test_feedback_failure_diagnosis"
    REPAIR_SUGGESTION_METADATA = "repair_suggestion_metadata"
    VERA_CODEX_ONE_SHOT_AGENT_TRIAL = "vera_codex_one_shot_agent_trial"
    COLD_AGENT_PERFORMANCE_EVALUATION = "cold_agent_performance_evaluation"
    CLI_TEST_RUNNER_AGENT_EVALUATION_SURFACE = "cli_test_runner_agent_evaluation_surface"
    CONSOLIDATION = "consolidation"
    UNKNOWN = "unknown"


class SandboxTestRunnerSurfaceKind(StrEnum):
    TEST_RUNNER_BOUNDARY = "test_runner_boundary"
    ALLOWLISTED_TEST_COMMAND_POLICY = "allowlisted_test_command_policy"
    TEST_INVOCATION_CONTRACT = "test_invocation_contract"
    CONTROLLED_SANDBOX_TEST_SUBPROCESS = "controlled_sandbox_test_subprocess"
    BOUNDED_TEST_OUTPUT_CAPTURE = "bounded_test_output_capture"
    TEST_RESULT_ENVELOPE = "test_result_envelope"
    FAILURE_DIAGNOSIS = "failure_diagnosis"
    REPAIR_SUGGESTION_METADATA = "repair_suggestion_metadata"
    VERA_CODEX_AGENT_TRIAL = "vera_codex_agent_trial"
    COLD_PERFORMANCE_EVALUATION = "cold_performance_evaluation"
    AGENT_SCORECARD = "agent_scorecard"
    DO_NOTHING_ALTERNATIVE_COMPARISON = "do_nothing_alternative_comparison"
    CLI_TEST_RUNNER_SURFACE = "cli_test_runner_surface"
    LIVE_WORKSPACE_TEST_EXECUTION = "live_workspace_test_execution"
    ARBITRARY_SHELL = "arbitrary_shell"
    DEPENDENCY_INSTALL = "dependency_install"
    NETWORK_ACCESS = "network_access"
    EXTERNAL_AGENT_EXECUTION = "external_agent_execution"
    DOMINION_RUNTIME = "dominion_runtime"
    AUTOMATIC_REPAIR = "automatic_repair"
    MULTI_CYCLE_LOOP = "multi_cycle_loop"
    UNKNOWN = "unknown"


class SandboxTestRunnerCapabilityKind(StrEnum):
    DEFINE_TEST_RUNNER_BOUNDARY = "define_test_runner_boundary"
    DEFINE_ALLOWLISTED_TEST_POLICY_BOUNDARY = "define_allowlisted_test_policy_boundary"
    DEFINE_TEST_OUTPUT_BOUNDARY = "define_test_output_boundary"
    DEFINE_VERA_CODEX_EVALUATION_BOUNDARY = "define_vera_codex_evaluation_boundary"
    DEFINE_DO_NOTHING_ALTERNATIVE_BOUNDARY = "define_do_nothing_alternative_boundary"
    CREATE_TEST_INVOCATION_CONTRACT_FUTURE_GATE = "create_test_invocation_contract_future_gate"
    CREATE_TEST_RESULT_ENVELOPE_FUTURE_GATE = "create_test_result_envelope_future_gate"
    CREATE_FEEDBACK_REPORT_FUTURE_GATE = "create_feedback_report_future_gate"
    CREATE_REPAIR_SUGGESTION_FUTURE_GATE = "create_repair_suggestion_future_gate"
    RUN_CONTROLLED_SANDBOX_TEST = "run_controlled_sandbox_test"
    RUN_PYTEST = "run_pytest"
    RUN_NPM_TEST = "run_npm_test"
    EXECUTE_ARBITRARY_SHELL = "execute_arbitrary_shell"
    INSTALL_DEPENDENCY = "install_dependency"
    ACCESS_NETWORK = "access_network"
    RUN_VERA_CODEX_TRIAL = "run_vera_codex_trial"
    RUN_COLD_PERFORMANCE_EVALUATION = "run_cold_performance_evaluation"
    RUN_AUTOMATIC_REPAIR = "run_automatic_repair"
    RUN_MULTI_CYCLE_LOOP = "run_multi_cycle_loop"
    EXECUTE_EXTERNAL_AGENT = "execute_external_agent"
    RUN_DOMINION_RUNTIME = "run_dominion_runtime"
    UNKNOWN = "unknown"


class SandboxTestRunnerRiskKind(StrEnum):
    ARBITRARY_SHELL_RISK = "arbitrary_shell_risk"
    UNCONTROLLED_SUBPROCESS_RISK = "uncontrolled_subprocess_risk"
    TEST_COMMAND_INJECTION_RISK = "test_command_injection_risk"
    LIVE_WORKSPACE_TEST_RISK = "live_workspace_test_risk"
    DEPENDENCY_INSTALL_RISK = "dependency_install_risk"
    NETWORK_ACCESS_RISK = "network_access_risk"
    UNBOUNDED_OUTPUT_RISK = "unbounded_output_risk"
    TIMEOUT_MISSING_RISK = "timeout_missing_risk"
    RESOURCE_EXHAUSTION_RISK = "resource_exhaustion_risk"
    MISSING_ALLOWLIST_RISK = "missing_allowlist_risk"
    TEST_RESULT_OVERCLAIM_RISK = "test_result_overclaim_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    FAILED_TEST_MISREPORTED_AS_SUCCESS_RISK = "failed_test_misreported_as_success_risk"
    AUTOMATIC_REPAIR_RISK = "automatic_repair_risk"
    MULTI_CYCLE_LOOP_RISK = "multi_cycle_loop_risk"
    MODEL_SELF_PRAISE_RISK = "model_self_praise_risk"
    VERA_CODEX_OVERCLAIM_RISK = "vera_codex_overclaim_risk"
    DO_NOTHING_OMISSION_RISK = "do_nothing_omission_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    CREDENTIAL_EXPOSURE_RISK = "credential_exposure_risk"
    SECRET_EXPOSURE_RISK = "secret_exposure_risk"
    UNKNOWN = "unknown"


class SandboxTestRunnerDecisionKind(StrEnum):
    ALLOW_BOUNDARY_DEFINITION = "allow_boundary_definition"
    ALLOW_ALLOWLISTED_POLICY_BOUNDARY_DEFINITION = "allow_allowlisted_policy_boundary_definition"
    ALLOW_TEST_OUTPUT_BOUNDARY_DEFINITION = "allow_test_output_boundary_definition"
    ALLOW_VERA_CODEX_EVALUATION_BOUNDARY_DEFINITION = "allow_vera_codex_evaluation_boundary_definition"
    ALLOW_DO_NOTHING_BOUNDARY_DEFINITION = "allow_do_nothing_boundary_definition"
    ALLOW_DESIGN_STAGE_HANDOFF = "allow_design_stage_handoff"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class SandboxTestRunnerStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    BOUNDARY_READY = "boundary_ready"
    BOUNDARY_READY_WITH_GAPS = "boundary_ready_with_gaps"
    ALLOWLIST_BOUNDARY_READY = "allowlist_boundary_ready"
    OUTPUT_BOUNDARY_READY = "output_boundary_ready"
    VERA_CODEX_EVALUATION_BOUNDARY_READY = "vera_codex_evaluation_boundary_ready"
    DO_NOTHING_BOUNDARY_READY = "do_nothing_boundary_ready"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class SandboxTestRunnerReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    BOUNDARY_CONTRACT_READY = "boundary_contract_ready"
    SANDBOX_TEST_RUNNER_BOUNDARY_READY = "sandbox_test_runner_boundary_ready"
    ALLOWLISTED_TEST_POLICY_BOUNDARY_READY = "allowlisted_test_policy_boundary_ready"
    TEST_OUTPUT_BOUNDARY_READY = "test_output_boundary_ready"
    VERA_CODEX_EVALUATION_BOUNDARY_READY = "vera_codex_evaluation_boundary_ready"
    DO_NOTHING_ALTERNATIVE_BOUNDARY_READY = "do_nothing_alternative_boundary_ready"
    DESIGN_HANDOFF_READY_FOR_V0371 = "design_handoff_ready_for_v0371"
    DESIGN_HANDOFF_READY_FOR_V0372 = "design_handoff_ready_for_v0372"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class SandboxTestCommandPosture(StrEnum):
    NO_TEST_COMMAND_EXECUTION = "no_test_command_execution"
    ALLOWLIST_POLICY_FUTURE_GATED = "allowlist_policy_future_gated"
    CONTROLLED_TEST_SUBPROCESS_FUTURE_GATED = "controlled_test_subprocess_future_gated"
    ARBITRARY_SHELL_BLOCKED = "arbitrary_shell_blocked"
    PACKAGE_SCRIPT_BLOCKED = "package_script_blocked"
    DEPENDENCY_INSTALL_BLOCKED = "dependency_install_blocked"
    UNKNOWN = "unknown"


class SandboxTestExecutionPosture(StrEnum):
    NO_TEST_EXECUTION = "no_test_execution"
    SANDBOX_ONLY_TEST_EXECUTION_FUTURE_GATED = "sandbox_only_test_execution_future_gated"
    LIVE_WORKSPACE_TEST_EXECUTION_BLOCKED = "live_workspace_test_execution_blocked"
    UNCONTROLLED_TEST_EXECUTION_BLOCKED = "uncontrolled_test_execution_blocked"
    UNKNOWN = "unknown"


class SandboxTestOutputPosture(StrEnum):
    NO_OUTPUT_CAPTURE = "no_output_capture"
    BOUNDED_OUTPUT_CAPTURE_FUTURE_GATED = "bounded_output_capture_future_gated"
    UNBOUNDED_OUTPUT_BLOCKED = "unbounded_output_blocked"
    RAW_SECRET_OUTPUT_BLOCKED = "raw_secret_output_blocked"
    UNKNOWN = "unknown"


class VeraCodexEvaluationPosture(StrEnum):
    NO_VERA_CODEX_TRIAL_EXECUTION = "no_vera_codex_trial_execution"
    ONE_SHOT_EVALUATION_FUTURE_GATED = "one_shot_evaluation_future_gated"
    COLD_EVALUATION_FUTURE_GATED = "cold_evaluation_future_gated"
    MODEL_SELF_PRAISE_BLOCKED = "model_self_praise_blocked"
    AUTONOMOUS_AGENT_EVALUATION_BLOCKED = "autonomous_agent_evaluation_blocked"
    EXTERNAL_AGENT_EVALUATION_BLOCKED = "external_agent_evaluation_blocked"
    UNKNOWN = "unknown"


class DoNothingAlternativePosture(StrEnum):
    DO_NOTHING_BOUNDARY_DEFINED = "do_nothing_boundary_defined"
    DO_NOTHING_COMPARISON_FUTURE_GATED = "do_nothing_comparison_future_gated"
    DO_NOTHING_REQUIRED_FOR_EVALUATION = "do_nothing_required_for_evaluation"
    DO_NOTHING_OMISSION_BLOCKED = "do_nothing_omission_blocked"
    UNKNOWN = "unknown"


class SandboxTestRunnerSourceKind(StrEnum):
    V0369_HANDOFF_PACKET = "v0369_handoff_packet"
    V0369_CONSOLIDATION_REPORT = "v0369_consolidation_report"
    V0368_CLI_SANDBOX_APPLY_SURFACE = "v0368_cli_sandbox_apply_surface"
    V0367_PATCH_APPLY_TRACE_PACKET = "v0367_patch_apply_trace_packet"
    V0366_AGENTIC_OPERATION_RUN_PACKET = "v0366_agentic_operation_run_packet"
    V0365_POST_APPLY_VALIDATION_REPORT = "v0365_post_apply_validation_report"
    MANUAL_DESIGN_NOTE = "manual_design_note"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


def _validate_list(name: str, value: list[Any]) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be list")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be dict")


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0370_VERSION not in version:
        raise ValueError("version must include v0.37.0")


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must always be False in v0.37.0")


def _validate_true(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not True:
            raise ValueError(f"{name} must be True in v0.37.0 boundary metadata")


def _validate_enum_list(name: str, value: list[Any], enum_cls: type[StrEnum]) -> None:
    _validate_list(name, value)
    for item in value:
        enum_cls(item)


def _validate_metadata(metadata: dict[str, Any]) -> None:
    _validate_dict("metadata", metadata)
    for key in metadata:
        lowered = str(key).lower()
        if any(token in lowered for token in ("secret_value", "credential_value", "api_key_value", "token_value")):
            raise ValueError("metadata keys must not carry credential or secret values")


@dataclass(frozen=True, kw_only=True)
class SandboxTestRunnerFlagSet:
    flag_set_id: str
    version: str
    sandbox_test_runner_boundary_constructed: bool
    sandbox_test_runner_policy_defined: bool
    allowlisted_test_policy_boundary_defined: bool
    test_output_boundary_defined: bool
    vera_codex_evaluation_boundary_defined: bool
    do_nothing_alternative_boundary_defined: bool
    sandbox_test_runner_risk_register_defined: bool
    ready_for_v0371_allowlisted_test_command_policy: bool
    ready_for_v0372_sandbox_test_execution_engine: bool
    ready_for_v0376_vera_codex_one_shot_agent_trial: bool
    ready_for_v0377_cold_agent_performance_evaluation: bool
    ready_for_sandbox_test_runner_boundary: bool
    ready_for_allowlisted_test_policy_boundary: bool
    ready_for_test_output_boundary: bool
    ready_for_vera_codex_evaluation_boundary: bool
    ready_for_do_nothing_alternative_boundary: bool
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
        _validate_false(self, UNSAFE_FLAG_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxTestRunnerSourceRef:
    source_ref_id: str
    source_kind: SandboxTestRunnerSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("source_ref_id", "source_id", "source_summary"):
            _require_non_blank(name, getattr(self, name))
        SandboxTestRunnerSourceKind(self.source_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxTestRunnerBoundaryPolicy:
    policy_id: str
    version: str
    test_command_posture: SandboxTestCommandPosture | str
    test_execution_posture: SandboxTestExecutionPosture | str
    output_posture: SandboxTestOutputPosture | str
    vera_codex_posture: VeraCodexEvaluationPosture | str
    do_nothing_posture: DoNothingAlternativePosture | str
    allowed_surfaces: list[SandboxTestRunnerSurfaceKind | str]
    prohibited_surfaces: list[SandboxTestRunnerSurfaceKind | str]
    prohibited_capabilities: list[SandboxTestRunnerCapabilityKind | str]
    prohibited_runtime_actions: list[str]
    allow_boundary_definition: bool
    allow_allowlisted_policy_future_gate: bool
    allow_controlled_test_subprocess_future_gate: bool
    allow_bounded_output_future_gate: bool
    allow_vera_codex_evaluation_future_gate: bool
    allow_do_nothing_comparison_future_gate: bool
    allow_test_execution: bool
    allow_controlled_test_subprocess: bool
    allow_pytest_execution: bool
    allow_npm_test_execution: bool
    allow_unittest_execution: bool
    allow_shell: bool
    allow_arbitrary_command: bool
    allow_dependency_install: bool
    allow_network_access: bool
    allow_live_workspace_write: bool
    allow_patch_application: bool
    allow_automatic_repair: bool
    allow_multi_cycle_loop: bool
    allow_vera_codex_trial_execution: bool
    allow_external_agent_execution: bool
    allow_dominion_runtime: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_id", self.policy_id)
        _validate_version(self.version)
        SandboxTestCommandPosture(self.test_command_posture)
        SandboxTestExecutionPosture(self.test_execution_posture)
        SandboxTestOutputPosture(self.output_posture)
        VeraCodexEvaluationPosture(self.vera_codex_posture)
        DoNothingAlternativePosture(self.do_nothing_posture)
        _validate_enum_list("allowed_surfaces", self.allowed_surfaces, SandboxTestRunnerSurfaceKind)
        _validate_enum_list("prohibited_surfaces", self.prohibited_surfaces, SandboxTestRunnerSurfaceKind)
        _validate_enum_list("prohibited_capabilities", self.prohibited_capabilities, SandboxTestRunnerCapabilityKind)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_false(self, UNSAFE_POLICY_ALLOW_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxTestCommandBoundaryPolicy:
    command_policy_id: str
    version: str
    posture: SandboxTestCommandPosture | str
    require_allowlist: bool
    require_structured_command_spec: bool
    require_no_shell: bool
    require_sandbox_cwd: bool
    require_timeout: bool
    require_no_network: bool
    reject_package_scripts_by_default: bool
    reject_dependency_install: bool
    allow_command_policy_future_gate: bool
    allow_test_command_execution: bool
    allow_arbitrary_shell: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("command_policy_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        SandboxTestCommandPosture(self.posture)
        _validate_true(self, ("require_allowlist", "require_structured_command_spec", "require_no_shell", "require_sandbox_cwd", "require_timeout", "require_no_network", "reject_package_scripts_by_default", "reject_dependency_install"))
        _validate_false(self, ("allow_test_command_execution", "allow_arbitrary_shell"))
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxTestOutputBoundaryPolicy:
    output_policy_id: str
    version: str
    posture: SandboxTestOutputPosture | str
    max_stdout_chars: int
    max_stderr_chars: int
    max_total_output_chars: int
    require_redaction: bool
    block_raw_secret_output: bool
    block_unbounded_output: bool
    allow_output_capture_future_gate: bool
    allow_output_capture: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("output_policy_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        SandboxTestOutputPosture(self.posture)
        for name in ("max_stdout_chars", "max_stderr_chars", "max_total_output_chars"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        _validate_true(self, ("require_redaction", "block_raw_secret_output", "block_unbounded_output"))
        _validate_false(self, ("allow_output_capture",))
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class VeraCodexEvaluationBoundaryPolicy:
    vera_policy_id: str
    version: str
    posture: VeraCodexEvaluationPosture | str
    require_test_result_evidence: bool
    require_validation_report_evidence: bool
    require_do_nothing_comparison: bool
    require_cold_evaluation: bool
    reject_self_praise_without_evidence: bool
    reject_test_failure_as_success: bool
    require_human_handoff: bool
    allow_one_shot_trial_future_gate: bool
    allow_cold_evaluation_future_gate: bool
    allow_vera_codex_trial_execution: bool
    allow_model_provider_invocation: bool
    allow_autonomous_agent_runtime: bool
    allow_external_agent_execution: bool
    allow_dominion_runtime: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("vera_policy_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        VeraCodexEvaluationPosture(self.posture)
        _validate_true(self, ("require_test_result_evidence", "require_validation_report_evidence", "require_do_nothing_comparison", "require_cold_evaluation", "reject_self_praise_without_evidence", "reject_test_failure_as_success", "require_human_handoff"))
        _validate_false(self, ("allow_vera_codex_trial_execution", "allow_model_provider_invocation", "allow_autonomous_agent_runtime", "allow_external_agent_execution", "allow_dominion_runtime"))
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class DoNothingAlternativeBoundaryPolicy:
    do_nothing_policy_id: str
    version: str
    posture: DoNothingAlternativePosture | str
    require_do_nothing_baseline: bool
    require_before_after_comparison: bool
    require_risk_delta_comparison: bool
    require_test_delta_comparison: bool
    reject_improvement_claim_without_evidence: bool
    allow_do_nothing_comparison_future_gate: bool
    allow_scoring_execution: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("do_nothing_policy_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        DoNothingAlternativePosture(self.posture)
        _validate_true(self, ("require_do_nothing_baseline", "require_before_after_comparison", "require_risk_delta_comparison", "require_test_delta_comparison", "reject_improvement_claim_without_evidence"))
        _validate_false(self, ("allow_scoring_execution",))
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxTestAllowedSurface:
    allowed_surface_id: str
    surface_kind: SandboxTestRunnerSurfaceKind | str
    capability_kind: SandboxTestRunnerCapabilityKind | str
    description: str
    allowed_only_for_design_stage: bool
    executable_in_v0370: bool
    runs_tests: bool
    runs_shell: bool
    installs_dependency: bool
    accesses_network: bool
    invokes_model: bool
    invokes_external_agent: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("allowed_surface_id", "description"):
            _require_non_blank(name, getattr(self, name))
        SandboxTestRunnerSurfaceKind(self.surface_kind)
        SandboxTestRunnerCapabilityKind(self.capability_kind)
        _validate_false(self, ("executable_in_v0370", "runs_tests", "runs_shell", "installs_dependency", "accesses_network", "invokes_model", "invokes_external_agent"))
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxTestProhibitedSurface:
    prohibited_surface_id: str
    surface_kind: SandboxTestRunnerSurfaceKind | str
    risk_kind: SandboxTestRunnerRiskKind | str
    capability_kind: SandboxTestRunnerCapabilityKind | str
    reason: str
    prohibited_runtime_actions: list[str]
    blocks_test_execution: bool
    blocks_runtime_readiness: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("prohibited_surface_id", "reason"):
            _require_non_blank(name, getattr(self, name))
        SandboxTestRunnerSurfaceKind(self.surface_kind)
        SandboxTestRunnerRiskKind(self.risk_kind)
        SandboxTestRunnerCapabilityKind(self.capability_kind)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_true(self, ("blocks_test_execution", "blocks_runtime_readiness"))
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxTestRunnerBoundary:
    boundary_id: str
    version: str
    release_name: str
    runner_policy: SandboxTestRunnerBoundaryPolicy
    command_policy: SandboxTestCommandBoundaryPolicy
    output_policy: SandboxTestOutputBoundaryPolicy
    vera_policy: VeraCodexEvaluationBoundaryPolicy
    do_nothing_policy: DoNothingAlternativeBoundaryPolicy
    allowed_surfaces: list[SandboxTestAllowedSurface]
    prohibited_surfaces: list[SandboxTestProhibitedSurface]
    flags: SandboxTestRunnerFlagSet
    status: SandboxTestRunnerStatus | str
    readiness_level: SandboxTestRunnerReadinessLevel | str
    summary: str
    gaps: list[str]
    blocked_reasons: list[str]
    evidence_refs: list[str]
    withdrawal_conditions: list[str]
    ready_for_v0371_allowlisted_test_command_policy: bool
    ready_for_v0372_sandbox_test_execution_engine: bool
    ready_for_v0376_vera_codex_one_shot_agent_trial: bool
    ready_for_v0377_cold_agent_performance_evaluation: bool
    ready_for_sandbox_test_runner_boundary: bool
    ready_for_allowlisted_test_policy_boundary: bool
    ready_for_vera_codex_evaluation_boundary: bool
    ready_for_do_nothing_alternative_boundary: bool
    ready_for_execution: bool
    ready_for_test_execution: bool
    ready_for_controlled_test_subprocess: bool
    ready_for_shell_execution: bool
    ready_for_dependency_install: bool
    ready_for_network_access: bool
    ready_for_vera_codex_trial_execution: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("boundary_id", "release_name", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ("allowed_surfaces", "prohibited_surfaces", "gaps", "blocked_reasons", "evidence_refs", "withdrawal_conditions"):
            _validate_list(name, getattr(self, name))
        if not sandbox_test_runner_flags_preserve_no_execution(self.flags):
            raise ValueError("flags must preserve no execution")
        SandboxTestRunnerStatus(self.status)
        SandboxTestRunnerReadinessLevel(self.readiness_level)
        _validate_false(self, ("ready_for_execution", "ready_for_test_execution", "ready_for_controlled_test_subprocess", "ready_for_shell_execution", "ready_for_dependency_install", "ready_for_network_access", "ready_for_vera_codex_trial_execution"))
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxTestPermissionRequest:
    request_id: str
    version: str
    requested_surface: SandboxTestRunnerSurfaceKind | str
    requested_capability: SandboxTestRunnerCapabilityKind | str
    request_summary: str
    source_refs: list[SandboxTestRunnerSourceRef]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("request_id", "request_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        SandboxTestRunnerSurfaceKind(self.requested_surface)
        SandboxTestRunnerCapabilityKind(self.requested_capability)
        _validate_list("source_refs", self.source_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxTestPermissionDecision:
    decision_id: str
    request_id: str
    decision_kind: SandboxTestRunnerDecisionKind | str
    reason: str
    risk_kinds: list[SandboxTestRunnerRiskKind | str]
    test_execution_allowed: bool
    controlled_test_subprocess_allowed: bool
    shell_execution_allowed: bool
    subprocess_allowed: bool
    command_execution_allowed: bool
    dependency_install_allowed: bool
    network_access_allowed: bool
    live_workspace_write_allowed: bool
    patch_application_allowed: bool
    automatic_repair_allowed: bool
    multi_cycle_loop_allowed: bool
    vera_codex_trial_execution_allowed: bool
    external_agent_execution_allowed: bool
    dominion_runtime_allowed: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("decision_id", "request_id", "reason"):
            _require_non_blank(name, getattr(self, name))
        SandboxTestRunnerDecisionKind(self.decision_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, SandboxTestRunnerRiskKind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, UNSAFE_DECISION_ALLOW_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxTestDeniedAction:
    denied_action_id: str
    request_id: str | None
    decision_id: str | None
    surface_kind: SandboxTestRunnerSurfaceKind | str
    capability_kind: SandboxTestRunnerCapabilityKind | str
    risk_kinds: list[SandboxTestRunnerRiskKind | str]
    reason: str
    safe_alternatives: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("denied_action_id", "reason"):
            _require_non_blank(name, getattr(self, name))
        SandboxTestRunnerSurfaceKind(self.surface_kind)
        SandboxTestRunnerCapabilityKind(self.capability_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, SandboxTestRunnerRiskKind)
        _validate_string_list("safe_alternatives", self.safe_alternatives)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxTestGateEvaluation:
    gate_evaluation_id: str
    version: str
    request: SandboxTestPermissionRequest
    decision: SandboxTestPermissionDecision
    denied_action: SandboxTestDeniedAction | None
    gate_summary: str
    passed: bool
    blocked: bool
    ready_for_execution: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("gate_evaluation_id", "gate_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must remain False")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxTestRunnerRiskRegister:
    risk_register_id: str
    version: str
    risk_kinds: list[SandboxTestRunnerRiskKind | str]
    high_risk_surfaces: list[SandboxTestRunnerSurfaceKind | str]
    mitigations: list[str]
    unresolved_risks: list[str]
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("risk_register_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_enum_list("risk_kinds", self.risk_kinds, SandboxTestRunnerRiskKind)
        _validate_enum_list("high_risk_surfaces", self.high_risk_surfaces, SandboxTestRunnerSurfaceKind)
        _validate_string_list("mitigations", self.mitigations)
        _validate_string_list("unresolved_risks", self.unresolved_risks)
        required = {
            SandboxTestRunnerRiskKind.ARBITRARY_SHELL_RISK,
            SandboxTestRunnerRiskKind.UNCONTROLLED_SUBPROCESS_RISK,
            SandboxTestRunnerRiskKind.DEPENDENCY_INSTALL_RISK,
            SandboxTestRunnerRiskKind.NETWORK_ACCESS_RISK,
            SandboxTestRunnerRiskKind.UNBOUNDED_OUTPUT_RISK,
            SandboxTestRunnerRiskKind.FAILED_TEST_MISREPORTED_AS_SUCCESS_RISK,
            SandboxTestRunnerRiskKind.AUTOMATIC_REPAIR_RISK,
            SandboxTestRunnerRiskKind.MULTI_CYCLE_LOOP_RISK,
            SandboxTestRunnerRiskKind.MODEL_SELF_PRAISE_RISK,
            SandboxTestRunnerRiskKind.DO_NOTHING_OMISSION_RISK,
            SandboxTestRunnerRiskKind.EXTERNAL_AGENT_EXECUTION_RISK,
            SandboxTestRunnerRiskKind.DOMINION_RUNTIME_RISK,
        }
        if not required.issubset({SandboxTestRunnerRiskKind(item) for item in self.risk_kinds}):
            raise ValueError("risk register missing required high-risk entries")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxTestNoExecutionGuarantee:
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
    no_multi_cycle_loop: bool
    no_vera_codex_trial_execution: bool
    no_cold_performance_evaluation_execution: bool
    no_model_invocation: bool
    no_external_agent_execution: bool
    no_dominion_runtime: bool
    no_authority_grant: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _require_non_blank("summary", self.summary)
        _validate_version(self.version)
        _validate_true(self, tuple(name for name in self.__dataclass_fields__ if name.startswith("no_")))
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class V037RoadmapOverview:
    roadmap_id: str
    version: str
    track_name: str
    roadmap_items: list[str]
    current_release: SandboxTestRunnerTrackKind | str
    next_release: SandboxTestRunnerTrackKind | str
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("roadmap_id", "track_name", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_string_list("roadmap_items", self.roadmap_items)
        SandboxTestRunnerTrackKind(self.current_release)
        SandboxTestRunnerTrackKind(self.next_release)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class V0370ReadinessReport:
    readiness_report_id: str
    version: str
    boundary_id: str
    readiness_level: SandboxTestRunnerReadinessLevel | str
    status: SandboxTestRunnerStatus | str
    summary: str
    ready_for_v0371_allowlisted_test_command_policy: bool
    ready_for_v0372_sandbox_test_execution_engine: bool
    ready_for_v0376_vera_codex_one_shot_agent_trial: bool
    ready_for_v0377_cold_agent_performance_evaluation: bool
    ready_for_sandbox_test_runner_boundary: bool
    ready_for_allowlisted_test_policy_boundary: bool
    ready_for_test_output_boundary: bool
    ready_for_vera_codex_evaluation_boundary: bool
    ready_for_do_nothing_alternative_boundary: bool
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
    ready_for_automatic_repair: bool
    ready_for_multi_cycle_agentic_loop: bool
    ready_for_vera_codex_trial_execution: bool
    ready_for_cold_agent_performance_evaluation: bool
    ready_for_external_agent_execution: bool
    ready_for_dominion_runtime: bool
    production_certified: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("readiness_report_id", "boundary_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        SandboxTestRunnerReadinessLevel(self.readiness_level)
        SandboxTestRunnerStatus(self.status)
        _validate_false(
            self,
            (
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
                "ready_for_automatic_repair",
                "ready_for_multi_cycle_agentic_loop",
                "ready_for_vera_codex_trial_execution",
                "ready_for_cold_agent_performance_evaluation",
                "ready_for_external_agent_execution",
                "ready_for_dominion_runtime",
                "production_certified",
            ),
        )
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


def build_sandbox_test_runner_flags(**kwargs: Any) -> SandboxTestRunnerFlagSet:
    return SandboxTestRunnerFlagSet(
        flag_set_id=kwargs.pop("flag_set_id", "sandbox_test_runner_flags:v0.37.0"),
        version=kwargs.pop("version", V0370_VERSION),
        sandbox_test_runner_boundary_constructed=kwargs.pop("sandbox_test_runner_boundary_constructed", True),
        sandbox_test_runner_policy_defined=kwargs.pop("sandbox_test_runner_policy_defined", True),
        allowlisted_test_policy_boundary_defined=kwargs.pop("allowlisted_test_policy_boundary_defined", True),
        test_output_boundary_defined=kwargs.pop("test_output_boundary_defined", True),
        vera_codex_evaluation_boundary_defined=kwargs.pop("vera_codex_evaluation_boundary_defined", True),
        do_nothing_alternative_boundary_defined=kwargs.pop("do_nothing_alternative_boundary_defined", True),
        sandbox_test_runner_risk_register_defined=kwargs.pop("sandbox_test_runner_risk_register_defined", True),
        ready_for_v0371_allowlisted_test_command_policy=kwargs.pop("ready_for_v0371_allowlisted_test_command_policy", True),
        ready_for_v0372_sandbox_test_execution_engine=kwargs.pop("ready_for_v0372_sandbox_test_execution_engine", True),
        ready_for_v0376_vera_codex_one_shot_agent_trial=kwargs.pop("ready_for_v0376_vera_codex_one_shot_agent_trial", True),
        ready_for_v0377_cold_agent_performance_evaluation=kwargs.pop("ready_for_v0377_cold_agent_performance_evaluation", True),
        ready_for_sandbox_test_runner_boundary=kwargs.pop("ready_for_sandbox_test_runner_boundary", True),
        ready_for_allowlisted_test_policy_boundary=kwargs.pop("ready_for_allowlisted_test_policy_boundary", True),
        ready_for_test_output_boundary=kwargs.pop("ready_for_test_output_boundary", True),
        ready_for_vera_codex_evaluation_boundary=kwargs.pop("ready_for_vera_codex_evaluation_boundary", True),
        ready_for_do_nothing_alternative_boundary=kwargs.pop("ready_for_do_nothing_alternative_boundary", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_FLAG_NAMES},
    )


def build_sandbox_test_runner_source_ref(**kwargs: Any) -> SandboxTestRunnerSourceRef:
    return SandboxTestRunnerSourceRef(
        source_ref_id=kwargs.pop("source_ref_id", "sandbox_test_runner_source_ref:v0.37.0"),
        source_kind=kwargs.pop("source_kind", SandboxTestRunnerSourceKind.V0369_HANDOFF_PACKET),
        source_id=kwargs.pop("source_id", "v037_handoff_packet:v0.36.9"),
        source_summary=kwargs.pop("source_summary", "v0.36.9 design-stage handoff metadata"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.36.9 consolidation report"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_runner_boundary_policy(**kwargs: Any) -> SandboxTestRunnerBoundaryPolicy:
    return SandboxTestRunnerBoundaryPolicy(
        policy_id=kwargs.pop("policy_id", "sandbox_test_runner_boundary_policy:v0.37.0"),
        version=kwargs.pop("version", V0370_VERSION),
        test_command_posture=kwargs.pop("test_command_posture", SandboxTestCommandPosture.NO_TEST_COMMAND_EXECUTION),
        test_execution_posture=kwargs.pop("test_execution_posture", SandboxTestExecutionPosture.NO_TEST_EXECUTION),
        output_posture=kwargs.pop("output_posture", SandboxTestOutputPosture.NO_OUTPUT_CAPTURE),
        vera_codex_posture=kwargs.pop("vera_codex_posture", VeraCodexEvaluationPosture.NO_VERA_CODEX_TRIAL_EXECUTION),
        do_nothing_posture=kwargs.pop("do_nothing_posture", DoNothingAlternativePosture.DO_NOTHING_BOUNDARY_DEFINED),
        allowed_surfaces=kwargs.pop("allowed_surfaces", [SandboxTestRunnerSurfaceKind.TEST_RUNNER_BOUNDARY, SandboxTestRunnerSurfaceKind.ALLOWLISTED_TEST_COMMAND_POLICY, SandboxTestRunnerSurfaceKind.BOUNDED_TEST_OUTPUT_CAPTURE, SandboxTestRunnerSurfaceKind.VERA_CODEX_AGENT_TRIAL, SandboxTestRunnerSurfaceKind.DO_NOTHING_ALTERNATIVE_COMPARISON]),
        prohibited_surfaces=kwargs.pop("prohibited_surfaces", [SandboxTestRunnerSurfaceKind.LIVE_WORKSPACE_TEST_EXECUTION, SandboxTestRunnerSurfaceKind.ARBITRARY_SHELL, SandboxTestRunnerSurfaceKind.DEPENDENCY_INSTALL, SandboxTestRunnerSurfaceKind.NETWORK_ACCESS, SandboxTestRunnerSurfaceKind.EXTERNAL_AGENT_EXECUTION, SandboxTestRunnerSurfaceKind.DOMINION_RUNTIME, SandboxTestRunnerSurfaceKind.AUTOMATIC_REPAIR, SandboxTestRunnerSurfaceKind.MULTI_CYCLE_LOOP]),
        prohibited_capabilities=kwargs.pop("prohibited_capabilities", [SandboxTestRunnerCapabilityKind.RUN_CONTROLLED_SANDBOX_TEST, SandboxTestRunnerCapabilityKind.RUN_PYTEST, SandboxTestRunnerCapabilityKind.RUN_NPM_TEST, SandboxTestRunnerCapabilityKind.EXECUTE_ARBITRARY_SHELL, SandboxTestRunnerCapabilityKind.INSTALL_DEPENDENCY, SandboxTestRunnerCapabilityKind.ACCESS_NETWORK, SandboxTestRunnerCapabilityKind.RUN_VERA_CODEX_TRIAL, SandboxTestRunnerCapabilityKind.RUN_COLD_PERFORMANCE_EVALUATION, SandboxTestRunnerCapabilityKind.RUN_AUTOMATIC_REPAIR, SandboxTestRunnerCapabilityKind.RUN_MULTI_CYCLE_LOOP, SandboxTestRunnerCapabilityKind.EXECUTE_EXTERNAL_AGENT, SandboxTestRunnerCapabilityKind.RUN_DOMINION_RUNTIME]),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", ["test_execution", "shell_execution", "dependency_install", "network_access", "automatic_repair", "external_agent_execution", "dominion_runtime"]),
        allow_boundary_definition=kwargs.pop("allow_boundary_definition", True),
        allow_allowlisted_policy_future_gate=kwargs.pop("allow_allowlisted_policy_future_gate", True),
        allow_controlled_test_subprocess_future_gate=kwargs.pop("allow_controlled_test_subprocess_future_gate", True),
        allow_bounded_output_future_gate=kwargs.pop("allow_bounded_output_future_gate", True),
        allow_vera_codex_evaluation_future_gate=kwargs.pop("allow_vera_codex_evaluation_future_gate", True),
        allow_do_nothing_comparison_future_gate=kwargs.pop("allow_do_nothing_comparison_future_gate", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_POLICY_ALLOW_NAMES},
    )


def build_sandbox_test_command_boundary_policy(**kwargs: Any) -> SandboxTestCommandBoundaryPolicy:
    return SandboxTestCommandBoundaryPolicy(
        command_policy_id=kwargs.pop("command_policy_id", "sandbox_test_command_boundary_policy:v0.37.0"),
        version=kwargs.pop("version", V0370_VERSION),
        posture=kwargs.pop("posture", SandboxTestCommandPosture.NO_TEST_COMMAND_EXECUTION),
        require_allowlist=kwargs.pop("require_allowlist", True),
        require_structured_command_spec=kwargs.pop("require_structured_command_spec", True),
        require_no_shell=kwargs.pop("require_no_shell", True),
        require_sandbox_cwd=kwargs.pop("require_sandbox_cwd", True),
        require_timeout=kwargs.pop("require_timeout", True),
        require_no_network=kwargs.pop("require_no_network", True),
        reject_package_scripts_by_default=kwargs.pop("reject_package_scripts_by_default", True),
        reject_dependency_install=kwargs.pop("reject_dependency_install", True),
        allow_command_policy_future_gate=kwargs.pop("allow_command_policy_future_gate", True),
        allow_test_command_execution=kwargs.pop("allow_test_command_execution", False),
        allow_arbitrary_shell=kwargs.pop("allow_arbitrary_shell", False),
        summary=kwargs.pop("summary", "future command policy must be allowlisted, sandbox cwd, no shell, timeout controlled"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_output_boundary_policy(**kwargs: Any) -> SandboxTestOutputBoundaryPolicy:
    return SandboxTestOutputBoundaryPolicy(
        output_policy_id=kwargs.pop("output_policy_id", "sandbox_test_output_boundary_policy:v0.37.0"),
        version=kwargs.pop("version", V0370_VERSION),
        posture=kwargs.pop("posture", SandboxTestOutputPosture.NO_OUTPUT_CAPTURE),
        max_stdout_chars=kwargs.pop("max_stdout_chars", 0),
        max_stderr_chars=kwargs.pop("max_stderr_chars", 0),
        max_total_output_chars=kwargs.pop("max_total_output_chars", 0),
        require_redaction=kwargs.pop("require_redaction", True),
        block_raw_secret_output=kwargs.pop("block_raw_secret_output", True),
        block_unbounded_output=kwargs.pop("block_unbounded_output", True),
        allow_output_capture_future_gate=kwargs.pop("allow_output_capture_future_gate", True),
        allow_output_capture=kwargs.pop("allow_output_capture", False),
        summary=kwargs.pop("summary", "bounded redacted output capture is future-gated and disabled in v0.37.0"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_vera_codex_evaluation_boundary_policy(**kwargs: Any) -> VeraCodexEvaluationBoundaryPolicy:
    return VeraCodexEvaluationBoundaryPolicy(
        vera_policy_id=kwargs.pop("vera_policy_id", "vera_codex_evaluation_boundary_policy:v0.37.0"),
        version=kwargs.pop("version", V0370_VERSION),
        posture=kwargs.pop("posture", VeraCodexEvaluationPosture.NO_VERA_CODEX_TRIAL_EXECUTION),
        require_test_result_evidence=kwargs.pop("require_test_result_evidence", True),
        require_validation_report_evidence=kwargs.pop("require_validation_report_evidence", True),
        require_do_nothing_comparison=kwargs.pop("require_do_nothing_comparison", True),
        require_cold_evaluation=kwargs.pop("require_cold_evaluation", True),
        reject_self_praise_without_evidence=kwargs.pop("reject_self_praise_without_evidence", True),
        reject_test_failure_as_success=kwargs.pop("reject_test_failure_as_success", True),
        require_human_handoff=kwargs.pop("require_human_handoff", True),
        allow_one_shot_trial_future_gate=kwargs.pop("allow_one_shot_trial_future_gate", True),
        allow_cold_evaluation_future_gate=kwargs.pop("allow_cold_evaluation_future_gate", True),
        allow_vera_codex_trial_execution=kwargs.pop("allow_vera_codex_trial_execution", False),
        allow_model_provider_invocation=kwargs.pop("allow_model_provider_invocation", False),
        allow_autonomous_agent_runtime=kwargs.pop("allow_autonomous_agent_runtime", False),
        allow_external_agent_execution=kwargs.pop("allow_external_agent_execution", False),
        allow_dominion_runtime=kwargs.pop("allow_dominion_runtime", False),
        summary=kwargs.pop("summary", "Vera-Codex evaluation is boundary metadata only in v0.37.0"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_do_nothing_alternative_boundary_policy(**kwargs: Any) -> DoNothingAlternativeBoundaryPolicy:
    return DoNothingAlternativeBoundaryPolicy(
        do_nothing_policy_id=kwargs.pop("do_nothing_policy_id", "do_nothing_alternative_boundary_policy:v0.37.0"),
        version=kwargs.pop("version", V0370_VERSION),
        posture=kwargs.pop("posture", DoNothingAlternativePosture.DO_NOTHING_BOUNDARY_DEFINED),
        require_do_nothing_baseline=kwargs.pop("require_do_nothing_baseline", True),
        require_before_after_comparison=kwargs.pop("require_before_after_comparison", True),
        require_risk_delta_comparison=kwargs.pop("require_risk_delta_comparison", True),
        require_test_delta_comparison=kwargs.pop("require_test_delta_comparison", True),
        reject_improvement_claim_without_evidence=kwargs.pop("reject_improvement_claim_without_evidence", True),
        allow_do_nothing_comparison_future_gate=kwargs.pop("allow_do_nothing_comparison_future_gate", True),
        allow_scoring_execution=kwargs.pop("allow_scoring_execution", False),
        summary=kwargs.pop("summary", "do-nothing alternative comparison is required evidence discipline and future-gated"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_allowed_surface(**kwargs: Any) -> SandboxTestAllowedSurface:
    return SandboxTestAllowedSurface(
        allowed_surface_id=kwargs.pop("allowed_surface_id", "sandbox_test_allowed_surface:v0.37.0"),
        surface_kind=kwargs.pop("surface_kind", SandboxTestRunnerSurfaceKind.TEST_RUNNER_BOUNDARY),
        capability_kind=kwargs.pop("capability_kind", SandboxTestRunnerCapabilityKind.DEFINE_TEST_RUNNER_BOUNDARY),
        description=kwargs.pop("description", "design-stage boundary definition surface only"),
        allowed_only_for_design_stage=kwargs.pop("allowed_only_for_design_stage", True),
        executable_in_v0370=kwargs.pop("executable_in_v0370", False),
        runs_tests=kwargs.pop("runs_tests", False),
        runs_shell=kwargs.pop("runs_shell", False),
        installs_dependency=kwargs.pop("installs_dependency", False),
        accesses_network=kwargs.pop("accesses_network", False),
        invokes_model=kwargs.pop("invokes_model", False),
        invokes_external_agent=kwargs.pop("invokes_external_agent", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_prohibited_surface(**kwargs: Any) -> SandboxTestProhibitedSurface:
    return SandboxTestProhibitedSurface(
        prohibited_surface_id=kwargs.pop("prohibited_surface_id", "sandbox_test_prohibited_surface:v0.37.0"),
        surface_kind=kwargs.pop("surface_kind", SandboxTestRunnerSurfaceKind.ARBITRARY_SHELL),
        risk_kind=kwargs.pop("risk_kind", SandboxTestRunnerRiskKind.ARBITRARY_SHELL_RISK),
        capability_kind=kwargs.pop("capability_kind", SandboxTestRunnerCapabilityKind.EXECUTE_ARBITRARY_SHELL),
        reason=kwargs.pop("reason", "unsafe runtime surface remains blocked"),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", ["test_execution", "shell_execution", "dependency_install", "network_access"]),
        blocks_test_execution=kwargs.pop("blocks_test_execution", True),
        blocks_runtime_readiness=kwargs.pop("blocks_runtime_readiness", True),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.0 boundary"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_runner_boundary(**kwargs: Any) -> SandboxTestRunnerBoundary:
    flags = kwargs.pop("flags", build_sandbox_test_runner_flags())
    return SandboxTestRunnerBoundary(
        boundary_id=kwargs.pop("boundary_id", "sandbox_test_runner_boundary:v0.37.0"),
        version=kwargs.pop("version", V0370_VERSION),
        release_name=kwargs.pop("release_name", V0370_RELEASE_NAME),
        runner_policy=kwargs.pop("runner_policy", build_sandbox_test_runner_boundary_policy()),
        command_policy=kwargs.pop("command_policy", build_sandbox_test_command_boundary_policy()),
        output_policy=kwargs.pop("output_policy", build_sandbox_test_output_boundary_policy()),
        vera_policy=kwargs.pop("vera_policy", build_vera_codex_evaluation_boundary_policy()),
        do_nothing_policy=kwargs.pop("do_nothing_policy", build_do_nothing_alternative_boundary_policy()),
        allowed_surfaces=kwargs.pop("allowed_surfaces", [build_sandbox_test_allowed_surface()]),
        prohibited_surfaces=kwargs.pop("prohibited_surfaces", [build_sandbox_test_prohibited_surface()]),
        flags=flags,
        status=kwargs.pop("status", SandboxTestRunnerStatus.BOUNDARY_READY),
        readiness_level=kwargs.pop("readiness_level", SandboxTestRunnerReadinessLevel.SANDBOX_TEST_RUNNER_BOUNDARY_READY),
        summary=kwargs.pop("summary", "controlled sandbox test runner boundary foundation only; no tests execute"),
        gaps=kwargs.pop("gaps", ["test command contract is v0.37.1", "execution engine is v0.37.2"]),
        blocked_reasons=kwargs.pop("blocked_reasons", ["test execution remains disabled"]),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.36.9 handoff"]),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", ["withdraw if any execution readiness becomes true"]),
        ready_for_v0371_allowlisted_test_command_policy=kwargs.pop("ready_for_v0371_allowlisted_test_command_policy", True),
        ready_for_v0372_sandbox_test_execution_engine=kwargs.pop("ready_for_v0372_sandbox_test_execution_engine", True),
        ready_for_v0376_vera_codex_one_shot_agent_trial=kwargs.pop("ready_for_v0376_vera_codex_one_shot_agent_trial", True),
        ready_for_v0377_cold_agent_performance_evaluation=kwargs.pop("ready_for_v0377_cold_agent_performance_evaluation", True),
        ready_for_sandbox_test_runner_boundary=kwargs.pop("ready_for_sandbox_test_runner_boundary", True),
        ready_for_allowlisted_test_policy_boundary=kwargs.pop("ready_for_allowlisted_test_policy_boundary", True),
        ready_for_vera_codex_evaluation_boundary=kwargs.pop("ready_for_vera_codex_evaluation_boundary", True),
        ready_for_do_nothing_alternative_boundary=kwargs.pop("ready_for_do_nothing_alternative_boundary", True),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        ready_for_test_execution=kwargs.pop("ready_for_test_execution", False),
        ready_for_controlled_test_subprocess=kwargs.pop("ready_for_controlled_test_subprocess", False),
        ready_for_shell_execution=kwargs.pop("ready_for_shell_execution", False),
        ready_for_dependency_install=kwargs.pop("ready_for_dependency_install", False),
        ready_for_network_access=kwargs.pop("ready_for_network_access", False),
        ready_for_vera_codex_trial_execution=kwargs.pop("ready_for_vera_codex_trial_execution", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_permission_request(**kwargs: Any) -> SandboxTestPermissionRequest:
    return SandboxTestPermissionRequest(
        request_id=kwargs.pop("request_id", "sandbox_test_permission_request:v0.37.0"),
        version=kwargs.pop("version", V0370_VERSION),
        requested_surface=kwargs.pop("requested_surface", SandboxTestRunnerSurfaceKind.TEST_RUNNER_BOUNDARY),
        requested_capability=kwargs.pop("requested_capability", SandboxTestRunnerCapabilityKind.DEFINE_TEST_RUNNER_BOUNDARY),
        request_summary=kwargs.pop("request_summary", "boundary definition request only"),
        source_refs=kwargs.pop("source_refs", [build_sandbox_test_runner_source_ref()]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_permission_decision(**kwargs: Any) -> SandboxTestPermissionDecision:
    return SandboxTestPermissionDecision(
        decision_id=kwargs.pop("decision_id", "sandbox_test_permission_decision:v0.37.0"),
        request_id=kwargs.pop("request_id", "sandbox_test_permission_request:v0.37.0"),
        decision_kind=kwargs.pop("decision_kind", SandboxTestRunnerDecisionKind.ALLOW_BOUNDARY_DEFINITION),
        reason=kwargs.pop("reason", "boundary definition allowed; execution remains blocked"),
        risk_kinds=kwargs.pop("risk_kinds", [SandboxTestRunnerRiskKind.TEST_RESULT_OVERCLAIM_RISK]),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.0 boundary"]),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_DECISION_ALLOW_NAMES},
    )


def build_sandbox_test_denied_action(**kwargs: Any) -> SandboxTestDeniedAction:
    return SandboxTestDeniedAction(
        denied_action_id=kwargs.pop("denied_action_id", "sandbox_test_denied_action:v0.37.0"),
        request_id=kwargs.pop("request_id", None),
        decision_id=kwargs.pop("decision_id", None),
        surface_kind=kwargs.pop("surface_kind", SandboxTestRunnerSurfaceKind.ARBITRARY_SHELL),
        capability_kind=kwargs.pop("capability_kind", SandboxTestRunnerCapabilityKind.EXECUTE_ARBITRARY_SHELL),
        risk_kinds=kwargs.pop("risk_kinds", [SandboxTestRunnerRiskKind.ARBITRARY_SHELL_RISK]),
        reason=kwargs.pop("reason", "unsafe test runner action denied"),
        safe_alternatives=kwargs.pop("safe_alternatives", ["define boundary", "future allowlist policy"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_gate_evaluation(**kwargs: Any) -> SandboxTestGateEvaluation:
    request = kwargs.pop("request", build_sandbox_test_permission_request())
    decision = kwargs.pop("decision", build_sandbox_test_permission_decision(request_id=request.request_id))
    return SandboxTestGateEvaluation(
        gate_evaluation_id=kwargs.pop("gate_evaluation_id", "sandbox_test_gate_evaluation:v0.37.0"),
        version=kwargs.pop("version", V0370_VERSION),
        request=request,
        decision=decision,
        denied_action=kwargs.pop("denied_action", None),
        gate_summary=kwargs.pop("gate_summary", "gate evaluation is metadata only"),
        passed=kwargs.pop("passed", True),
        blocked=kwargs.pop("blocked", False),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_runner_risk_register(**kwargs: Any) -> SandboxTestRunnerRiskRegister:
    return SandboxTestRunnerRiskRegister(
        risk_register_id=kwargs.pop("risk_register_id", "sandbox_test_runner_risk_register:v0.37.0"),
        version=kwargs.pop("version", V0370_VERSION),
        risk_kinds=kwargs.pop("risk_kinds", [
            SandboxTestRunnerRiskKind.ARBITRARY_SHELL_RISK,
            SandboxTestRunnerRiskKind.UNCONTROLLED_SUBPROCESS_RISK,
            SandboxTestRunnerRiskKind.DEPENDENCY_INSTALL_RISK,
            SandboxTestRunnerRiskKind.NETWORK_ACCESS_RISK,
            SandboxTestRunnerRiskKind.UNBOUNDED_OUTPUT_RISK,
            SandboxTestRunnerRiskKind.FAILED_TEST_MISREPORTED_AS_SUCCESS_RISK,
            SandboxTestRunnerRiskKind.AUTOMATIC_REPAIR_RISK,
            SandboxTestRunnerRiskKind.MULTI_CYCLE_LOOP_RISK,
            SandboxTestRunnerRiskKind.MODEL_SELF_PRAISE_RISK,
            SandboxTestRunnerRiskKind.DO_NOTHING_OMISSION_RISK,
            SandboxTestRunnerRiskKind.EXTERNAL_AGENT_EXECUTION_RISK,
            SandboxTestRunnerRiskKind.DOMINION_RUNTIME_RISK,
        ]),
        high_risk_surfaces=kwargs.pop("high_risk_surfaces", [SandboxTestRunnerSurfaceKind.ARBITRARY_SHELL, SandboxTestRunnerSurfaceKind.DEPENDENCY_INSTALL, SandboxTestRunnerSurfaceKind.NETWORK_ACCESS, SandboxTestRunnerSurfaceKind.EXTERNAL_AGENT_EXECUTION, SandboxTestRunnerSurfaceKind.DOMINION_RUNTIME]),
        mitigations=kwargs.pop("mitigations", ["future allowlist", "timeout", "bounded output", "human handoff"]),
        unresolved_risks=kwargs.pop("unresolved_risks", ["test execution remains future-gated"]),
        summary=kwargs.pop("summary", "risk register for future controlled sandbox test runner"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_no_execution_guarantee(**kwargs: Any) -> SandboxTestNoExecutionGuarantee:
    no_names = tuple(name for name in SandboxTestNoExecutionGuarantee.__dataclass_fields__ if name.startswith("no_"))
    return SandboxTestNoExecutionGuarantee(
        guarantee_id=kwargs.pop("guarantee_id", "sandbox_test_no_execution_guarantee:v0.37.0"),
        version=kwargs.pop("version", V0370_VERSION),
        summary=kwargs.pop("summary", "v0.37.0 defines boundaries only and executes nothing"),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, True) for name in no_names},
    )


def build_v037_roadmap_overview(**kwargs: Any) -> V037RoadmapOverview:
    return V037RoadmapOverview(
        roadmap_id=kwargs.pop("roadmap_id", "v037_roadmap_overview:v0.37.0"),
        version=kwargs.pop("version", V0370_VERSION),
        track_name=kwargs.pop("track_name", "Controlled Sandbox Test Runner & Vera-Codex Agent Evaluation"),
        roadmap_items=kwargs.pop("roadmap_items", [
            "v0.37.0 boundary foundation",
            "v0.37.1 allowlisted test command policy",
            "v0.37.2 sandbox test execution engine",
            "v0.37.3 test result envelope",
            "v0.37.4 feedback and diagnosis",
            "v0.37.5 repair suggestion metadata",
            "v0.37.6 Vera-Codex one-shot trial",
            "v0.37.7 cold scorecard",
            "v0.37.8 CLI surface",
            "v0.37.9 consolidation",
        ]),
        current_release=kwargs.pop("current_release", SandboxTestRunnerTrackKind.BOUNDARY_FOUNDATION),
        next_release=kwargs.pop("next_release", SandboxTestRunnerTrackKind.ALLOWLISTED_TEST_COMMAND_POLICY),
        summary=kwargs.pop("summary", "v0.37 roadmap overview; no execution in v0.37.0"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_v0370_readiness_report(**kwargs: Any) -> V0370ReadinessReport:
    return V0370ReadinessReport(
        readiness_report_id=kwargs.pop("readiness_report_id", "v0370_readiness_report"),
        version=kwargs.pop("version", V0370_VERSION),
        boundary_id=kwargs.pop("boundary_id", "sandbox_test_runner_boundary:v0.37.0"),
        readiness_level=kwargs.pop("readiness_level", SandboxTestRunnerReadinessLevel.DESIGN_HANDOFF_READY_FOR_V0371),
        status=kwargs.pop("status", SandboxTestRunnerStatus.BOUNDARY_READY),
        summary=kwargs.pop("summary", "v0.37.0 boundary ready; execution remains false"),
        ready_for_v0371_allowlisted_test_command_policy=kwargs.pop("ready_for_v0371_allowlisted_test_command_policy", True),
        ready_for_v0372_sandbox_test_execution_engine=kwargs.pop("ready_for_v0372_sandbox_test_execution_engine", True),
        ready_for_v0376_vera_codex_one_shot_agent_trial=kwargs.pop("ready_for_v0376_vera_codex_one_shot_agent_trial", True),
        ready_for_v0377_cold_agent_performance_evaluation=kwargs.pop("ready_for_v0377_cold_agent_performance_evaluation", True),
        ready_for_sandbox_test_runner_boundary=kwargs.pop("ready_for_sandbox_test_runner_boundary", True),
        ready_for_allowlisted_test_policy_boundary=kwargs.pop("ready_for_allowlisted_test_policy_boundary", True),
        ready_for_test_output_boundary=kwargs.pop("ready_for_test_output_boundary", True),
        ready_for_vera_codex_evaluation_boundary=kwargs.pop("ready_for_vera_codex_evaluation_boundary", True),
        ready_for_do_nothing_alternative_boundary=kwargs.pop("ready_for_do_nothing_alternative_boundary", True),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        ready_for_test_execution=kwargs.pop("ready_for_test_execution", False),
        ready_for_controlled_test_subprocess=kwargs.pop("ready_for_controlled_test_subprocess", False),
        ready_for_pytest_execution=kwargs.pop("ready_for_pytest_execution", False),
        ready_for_npm_test_execution=kwargs.pop("ready_for_npm_test_execution", False),
        ready_for_unittest_execution=kwargs.pop("ready_for_unittest_execution", False),
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
        evidence_refs=kwargs.pop("evidence_refs", ["v0.36.9 handoff"]),
        metadata=kwargs.pop("metadata", {}),
    )


def sandbox_test_runner_flags_preserve_no_execution(flags: SandboxTestRunnerFlagSet) -> bool:
    return isinstance(flags, SandboxTestRunnerFlagSet) and all(getattr(flags, name) is False for name in UNSAFE_FLAG_NAMES)


def sandbox_test_runner_policy_blocks_test_execution(policy: SandboxTestRunnerBoundaryPolicy) -> bool:
    return isinstance(policy, SandboxTestRunnerBoundaryPolicy) and all(getattr(policy, name) is False for name in UNSAFE_POLICY_ALLOW_NAMES)


def sandbox_test_command_policy_blocks_shell(policy: SandboxTestCommandBoundaryPolicy) -> bool:
    return isinstance(policy, SandboxTestCommandBoundaryPolicy) and policy.require_allowlist and policy.require_no_shell and not policy.allow_test_command_execution and not policy.allow_arbitrary_shell


def sandbox_test_output_policy_blocks_unbounded_output(policy: SandboxTestOutputBoundaryPolicy) -> bool:
    return isinstance(policy, SandboxTestOutputBoundaryPolicy) and policy.block_unbounded_output and policy.require_redaction and not policy.allow_output_capture


def vera_codex_evaluation_policy_blocks_trial_execution(policy: VeraCodexEvaluationBoundaryPolicy) -> bool:
    return isinstance(policy, VeraCodexEvaluationBoundaryPolicy) and policy.require_do_nothing_comparison and policy.require_human_handoff and not policy.allow_vera_codex_trial_execution and not policy.allow_model_provider_invocation and not policy.allow_autonomous_agent_runtime


def do_nothing_policy_requires_baseline(policy: DoNothingAlternativeBoundaryPolicy) -> bool:
    return isinstance(policy, DoNothingAlternativeBoundaryPolicy) and policy.require_do_nothing_baseline and policy.require_before_after_comparison and not policy.allow_scoring_execution


def sandbox_test_runner_boundary_is_not_execution(boundary: SandboxTestRunnerBoundary) -> bool:
    return (
        isinstance(boundary, SandboxTestRunnerBoundary)
        and sandbox_test_runner_flags_preserve_no_execution(boundary.flags)
        and not boundary.ready_for_execution
        and not boundary.ready_for_test_execution
        and not boundary.ready_for_controlled_test_subprocess
        and not boundary.ready_for_shell_execution
        and not boundary.ready_for_dependency_install
        and not boundary.ready_for_network_access
        and not boundary.ready_for_vera_codex_trial_execution
    )


def sandbox_test_permission_decision_is_not_execution(decision: SandboxTestPermissionDecision) -> bool:
    return isinstance(decision, SandboxTestPermissionDecision) and all(getattr(decision, name) is False for name in UNSAFE_DECISION_ALLOW_NAMES)


def v0370_readiness_report_is_not_execution_ready(report: V0370ReadinessReport) -> bool:
    if not isinstance(report, V0370ReadinessReport):
        return False
    unsafe = (
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
        "ready_for_automatic_repair",
        "ready_for_multi_cycle_agentic_loop",
        "ready_for_vera_codex_trial_execution",
        "ready_for_cold_agent_performance_evaluation",
        "ready_for_external_agent_execution",
        "ready_for_dominion_runtime",
        "production_certified",
    )
    return all(getattr(report, name) is False for name in unsafe)
