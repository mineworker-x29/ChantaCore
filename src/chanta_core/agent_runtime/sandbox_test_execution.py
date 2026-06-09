from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
import subprocess
import time
from typing import Any

from .boundary import _require_non_blank, _validate_string_list
from .sandbox_test_command_policy import (
    BLOCKED_ARGUMENT_PATTERNS,
    BLOCKED_COMMAND_NAMES,
    SandboxTestAllowedExecutable,
    SandboxTestAllowedModule,
    SandboxTestCommandDecisionKind,
    SandboxTestCommandDenylist,
    SandboxTestCommandKind,
    SandboxTestCommandSpec,
    SandboxTestCwdKind,
    SandboxTestDependencyPosture,
    SandboxTestEnvironmentMode,
    SandboxTestExecutableKind,
    SandboxTestInvocationContract,
    SandboxTestInvocationDecision,
    SandboxTestNetworkPosture,
    SandboxTestOutputCaptureMode,
    SandboxTestTimeoutKind,
    build_sandbox_test_allowed_executable,
    build_sandbox_test_allowed_module,
    build_sandbox_test_command_spec,
    default_sandbox_test_command_denylist,
    sandbox_test_invocation_contract_is_not_execution,
    sandbox_test_invocation_decision_is_not_execution,
)


V0372_VERSION = "v0.37.2"
V0372_RELEASE_NAME = "v0.37.2 Sandbox Test Execution Engine"


UNSAFE_EXECUTION_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_arbitrary_shell",
    "ready_for_uncontrolled_subprocess",
    "ready_for_shell_execution",
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
    "allow_arbitrary_shell",
    "allow_uncontrolled_subprocess",
    "allow_shell",
    "allow_command_execution",
    "allow_dependency_install",
    "allow_network_access",
    "allow_live_workspace_write",
    "allow_patch_application",
    "allow_automatic_repair",
    "allow_external_agent_execution",
    "allow_dominion_runtime",
)

UNSAFE_SUBPROCESS_POLICY_ALLOW_NAMES = (
    "allow_shell_true",
    "allow_command_string",
    "allow_package_manager",
    "allow_external_agent",
    "allow_network_access",
)

UNSAFE_DECISION_ALLOW_NAMES = (
    "arbitrary_shell_allowed",
    "uncontrolled_subprocess_allowed",
    "dependency_install_allowed",
    "network_access_allowed",
    "live_workspace_write_allowed",
    "automatic_repair_allowed",
    "external_agent_allowed",
    "dominion_runtime_allowed",
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
    if V0372_VERSION not in version:
        raise ValueError("version must include v0.37.2")


def _validate_false(name: str, value: bool) -> None:
    if value is not False:
        raise ValueError(f"{name} must remain False in v0.37.2")


def _validate_true(name: str, value: bool) -> None:
    if value is not True:
        raise ValueError(f"{name} must be True")


def _validate_non_negative(name: str, value: int | None) -> None:
    if value is not None and value < 0:
        raise ValueError(f"{name} must be None or >= 0")


def _validate_positive(name: str, value: int) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be > 0")


def _validate_metadata(value: dict[str, Any]) -> None:
    _validate_dict("metadata", value)


def _enum_value(value: Any) -> str:
    return value.value if isinstance(value, StrEnum) else str(value)


def _contains_blocked_token(tokens: list[str], denylist: SandboxTestCommandDenylist | None = None) -> bool:
    denylist = denylist or default_sandbox_test_command_denylist()
    lowered = [token.lower() for token in tokens]
    joined = " ".join(lowered)
    blocked_names = {item.lower() for item in denylist.blocked_command_names}
    blocked_patterns = [item.lower() for item in denylist.blocked_argument_patterns]
    return any(token in blocked_names for token in lowered) or any(pattern in joined for pattern in blocked_patterns)


def _limit_output(text: str, limit: int) -> tuple[str, bool]:
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


class SandboxTestExecutionMode(StrEnum):
    ALLOWLISTED_PYTHON_MODULE_EXECUTION = "allowlisted_python_module_execution"
    ALLOWLISTED_PYTEST_EXECUTION = "allowlisted_pytest_execution"
    ALLOWLISTED_UNITTEST_EXECUTION = "allowlisted_unittest_execution"
    METADATA_ONLY = "metadata_only"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class SandboxTestExecutionSourceKind(StrEnum):
    V0371_TEST_INVOCATION_CONTRACT = "v0371_test_invocation_contract"
    V0371_TEST_INVOCATION_DECISION = "v0371_test_invocation_decision"
    V0371_TEST_COMMAND_SPEC = "v0371_test_command_spec"
    V0371_TEST_COMMAND_ALLOWLIST = "v0371_test_command_allowlist"
    V0370_SANDBOX_TEST_RUNNER_BOUNDARY = "v0370_sandbox_test_runner_boundary"
    V0369_PATCH_APPLY_SANDBOX_CONSOLIDATION = "v0369_patch_apply_sandbox_consolidation"
    MANUAL_OPERATOR_INPUT = "manual_operator_input"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class SandboxTestExecutionStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    INPUT_VALIDATED = "input_validated"
    COMMAND_ALLOWED = "command_allowed"
    EXECUTION_STARTED = "execution_started"
    EXECUTION_COMPLETED = "execution_completed"
    EXECUTION_COMPLETED_WITH_NONZERO_EXIT = "execution_completed_with_nonzero_exit"
    EXECUTION_TIMED_OUT = "execution_timed_out"
    EXECUTION_BLOCKED = "execution_blocked"
    EXECUTION_FAILED_SAFE = "execution_failed_safe"
    NO_OP = "no_op"


class SandboxTestExecutionReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    EXECUTION_CONTRACT_READY = "execution_contract_ready"
    CONTROLLED_SUBPROCESS_READY = "controlled_subprocess_ready"
    ALLOWLISTED_TEST_EXECUTION_READY = "allowlisted_test_execution_ready"
    BOUNDED_OUTPUT_CAPTURE_READY = "bounded_output_capture_ready"
    RESULT_METADATA_READY = "result_metadata_ready"
    DESIGN_HANDOFF_READY_FOR_V0373 = "design_handoff_ready_for_v0373"
    DESIGN_HANDOFF_READY_FOR_V0374 = "design_handoff_ready_for_v0374"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class SandboxTestExecutionDecisionKind(StrEnum):
    ALLOW_CONTROLLED_SANDBOX_TEST_EXECUTION = "allow_controlled_sandbox_test_execution"
    ALLOW_CONTROLLED_SUBPROCESS = "allow_controlled_subprocess"
    ALLOW_BOUNDED_OUTPUT_CAPTURE = "allow_bounded_output_capture"
    ALLOW_FUTURE_TEST_RESULT_ENVELOPE_INPUT = "allow_future_test_result_envelope_input"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class SandboxTestExecutionRiskKind(StrEnum):
    UNALLOWLISTED_COMMAND_RISK = "unallowlisted_command_risk"
    ARBITRARY_SHELL_RISK = "arbitrary_shell_risk"
    SHELL_TRUE_RISK = "shell_true_risk"
    UNCONTROLLED_SUBPROCESS_RISK = "uncontrolled_subprocess_risk"
    COMMAND_INJECTION_RISK = "command_injection_risk"
    SHELL_METACHARACTER_RISK = "shell_metacharacter_risk"
    LIVE_WORKSPACE_CWD_RISK = "live_workspace_cwd_risk"
    OUTSIDE_SANDBOX_CWD_RISK = "outside_sandbox_cwd_risk"
    REFERENCES_CWD_RISK = "references_cwd_risk"
    DEPENDENCY_INSTALL_RISK = "dependency_install_risk"
    NETWORK_ACCESS_RISK = "network_access_risk"
    NETWORK_HARD_ISOLATION_UNCERTIFIED_RISK = "network_hard_isolation_uncertified_risk"
    UNBOUNDED_OUTPUT_RISK = "unbounded_output_risk"
    TIMEOUT_MISSING_RISK = "timeout_missing_risk"
    PROCESS_TIMEOUT_RISK = "process_timeout_risk"
    NONZERO_EXIT_RISK = "nonzero_exit_risk"
    MISSING_DEPENDENCY_RISK = "missing_dependency_risk"
    CREDENTIAL_EXPOSURE_RISK = "credential_exposure_risk"
    SECRET_EXPOSURE_RISK = "secret_exposure_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    AUTOMATIC_REPAIR_RISK = "automatic_repair_risk"
    MULTI_CYCLE_LOOP_RISK = "multi_cycle_loop_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    UNKNOWN = "unknown"


class ControlledTestSubprocessKind(StrEnum):
    PYTHON_MODULE_SUBPROCESS = "python_module_subprocess"
    PYTHON_PYTEST_MODULE_SUBPROCESS = "python_pytest_module_subprocess"
    PYTHON_UNITTEST_MODULE_SUBPROCESS = "python_unittest_module_subprocess"
    BLOCKED_SHELL_SUBPROCESS = "blocked_shell_subprocess"
    BLOCKED_PACKAGE_MANAGER_SUBPROCESS = "blocked_package_manager_subprocess"
    BLOCKED_EXTERNAL_AGENT_SUBPROCESS = "blocked_external_agent_subprocess"
    NO_SUBPROCESS = "no_subprocess"
    UNKNOWN = "unknown"


class ControlledTestSubprocessStatus(StrEnum):
    UNKNOWN = "unknown"
    NOT_STARTED = "not_started"
    VALIDATED = "validated"
    STARTED = "started"
    COMPLETED = "completed"
    COMPLETED_NONZERO = "completed_nonzero"
    TIMED_OUT = "timed_out"
    BLOCKED = "blocked"
    FAILED_SAFE = "failed_safe"
    NO_OP = "no_op"


class SandboxTestProcessExitKind(StrEnum):
    NOT_EXECUTED = "not_executed"
    EXIT_ZERO = "exit_zero"
    EXIT_NONZERO = "exit_nonzero"
    TIMEOUT = "timeout"
    BLOCKED_BEFORE_EXECUTION = "blocked_before_execution"
    FAILED_TO_START_SAFE = "failed_to_start_safe"
    UNKNOWN = "unknown"


class SandboxTestOutputStreamKind(StrEnum):
    STDOUT = "stdout"
    STDERR = "stderr"
    COMBINED = "combined"
    NO_OUTPUT = "no_output"
    UNKNOWN = "unknown"


class SandboxTestOutputCaptureStatus(StrEnum):
    NOT_CAPTURED = "not_captured"
    CAPTURED = "captured"
    CAPTURED_TRUNCATED = "captured_truncated"
    CAPTURED_REDACTED = "captured_redacted"
    BLOCKED_UNBOUNDED = "blocked_unbounded"
    BLOCKED_SECRET_LIKE = "blocked_secret_like"
    UNKNOWN = "unknown"


class SandboxTestTimeoutStatus(StrEnum):
    NO_TIMEOUT_CONFIGURED = "no_timeout_configured"
    TIMEOUT_CONFIGURED = "timeout_configured"
    COMPLETED_BEFORE_TIMEOUT = "completed_before_timeout"
    TIMED_OUT = "timed_out"
    TIMEOUT_BLOCKED = "timeout_blocked"
    UNKNOWN = "unknown"


class SandboxTestEnvironmentStatus(StrEnum):
    MINIMAL_ENV_PREPARED = "minimal_env_prepared"
    INHERITED_ENV_BLOCKED = "inherited_env_blocked"
    CREDENTIAL_ENV_BLOCKED = "credential_env_blocked"
    UNSAFE_ENV_BLOCKED = "unsafe_env_blocked"
    UNKNOWN = "unknown"


class SandboxTestNetworkIsolationStatus(StrEnum):
    NETWORK_POLICY_BLOCKED = "network_policy_blocked"
    NETWORK_HARD_ISOLATION_CERTIFIED = "network_hard_isolation_certified"
    NETWORK_HARD_ISOLATION_NOT_CERTIFIED = "network_hard_isolation_not_certified"
    NETWORK_STATUS_UNKNOWN = "network_status_unknown"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class SandboxTestExecutionFlagSet:
    flag_set_id: str
    version: str
    sandbox_test_execution_engine_constructed: bool
    controlled_subprocess_runner_available: bool
    allowlisted_test_execution_available: bool
    bounded_output_capture_available: bool
    timeout_enforcement_available: bool
    minimal_environment_available: bool
    ready_for_v0373_test_result_envelope: bool
    ready_for_v0374_test_feedback_failure_diagnosis: bool
    ready_for_v0376_vera_codex_one_shot_agent_trial: bool
    ready_for_sandbox_test_execution_engine: bool
    ready_for_controlled_test_subprocess: bool
    ready_for_allowlisted_test_execution: bool
    ready_for_pytest_module_execution: bool
    ready_for_unittest_module_execution: bool
    ready_for_bounded_test_output_capture: bool
    ready_for_test_timeout_enforcement: bool
    ready_for_minimal_test_environment: bool
    ready_for_future_test_result_envelope_input: bool
    ready_for_execution: bool
    ready_for_arbitrary_shell: bool
    ready_for_uncontrolled_subprocess: bool
    ready_for_shell_execution: bool
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
        for name in UNSAFE_EXECUTION_FLAG_NAMES:
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestExecutionSourceRef:
    source_ref_id: str
    source_kind: SandboxTestExecutionSourceKind | str
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
class SandboxTestExecutionPolicy:
    execution_policy_id: str
    version: str
    allowed_modes: list[SandboxTestExecutionMode | str]
    blocked_modes: list[SandboxTestExecutionMode | str]
    require_invocation_contract: bool
    require_allowlisted_command: bool
    require_sandbox_cwd: bool
    require_timeout: bool
    require_bounded_output: bool
    require_minimal_env: bool
    require_shell_false: bool
    require_no_dependency_install: bool
    require_no_network_policy: bool
    max_stdout_chars: int
    max_stderr_chars: int
    max_total_output_chars: int
    max_timeout_seconds: int
    allow_controlled_subprocess: bool
    allow_allowlisted_test_execution: bool
    allow_pytest_module_execution: bool
    allow_unittest_module_execution: bool
    allow_arbitrary_shell: bool
    allow_uncontrolled_subprocess: bool
    allow_shell: bool
    allow_command_execution: bool
    allow_dependency_install: bool
    allow_network_access: bool
    allow_live_workspace_write: bool
    allow_patch_application: bool
    allow_automatic_repair: bool
    allow_external_agent_execution: bool
    allow_dominion_runtime: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("execution_policy_id", self.execution_policy_id)
        _validate_version(self.version)
        _validate_list("allowed_modes", self.allowed_modes)
        _validate_list("blocked_modes", self.blocked_modes)
        for name in (
            "require_invocation_contract",
            "require_allowlisted_command",
            "require_sandbox_cwd",
            "require_timeout",
            "require_bounded_output",
            "require_minimal_env",
            "require_shell_false",
            "require_no_dependency_install",
            "require_no_network_policy",
        ):
            _validate_true(name, getattr(self, name))
        for name in ("max_stdout_chars", "max_stderr_chars", "max_total_output_chars", "max_timeout_seconds"):
            _validate_non_negative(name, getattr(self, name))
        for name in UNSAFE_POLICY_ALLOW_NAMES:
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class ControlledTestSubprocessPolicy:
    subprocess_policy_id: str
    version: str
    allowed_subprocess_kinds: list[ControlledTestSubprocessKind | str]
    blocked_subprocess_kinds: list[ControlledTestSubprocessKind | str]
    require_structured_argv: bool
    require_shell_false: bool
    require_timeout: bool
    require_sandbox_cwd: bool
    require_minimal_env: bool
    require_bounded_output: bool
    allow_subprocess_run: bool
    allow_shell_true: bool
    allow_command_string: bool
    allow_package_manager: bool
    allow_external_agent: bool
    allow_network_access: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("subprocess_policy_id", self.subprocess_policy_id)
        _validate_version(self.version)
        _validate_list("allowed_subprocess_kinds", self.allowed_subprocess_kinds)
        _validate_list("blocked_subprocess_kinds", self.blocked_subprocess_kinds)
        for name in (
            "require_structured_argv",
            "require_shell_false",
            "require_timeout",
            "require_sandbox_cwd",
            "require_minimal_env",
            "require_bounded_output",
        ):
            _validate_true(name, getattr(self, name))
        for name in UNSAFE_SUBPROCESS_POLICY_ALLOW_NAMES:
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestExecutionInput:
    execution_input_id: str
    version: str
    invocation_contract_id: str | None
    invocation_decision_id: str | None
    command_spec_id: str | None
    requested_mode: SandboxTestExecutionMode | str
    sandbox_cwd_ref: str
    timeout_seconds: int
    source_refs: list[SandboxTestExecutionSourceRef]
    prohibited_runtime_actions: list[str]
    task_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("execution_input_id", self.execution_input_id)
        _validate_version(self.version)
        _require_non_blank("sandbox_cwd_ref", self.sandbox_cwd_ref)
        _require_non_blank("task_summary", self.task_summary)
        _validate_positive("timeout_seconds", self.timeout_seconds)
        _validate_list("source_refs", self.source_refs)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        required = {"shell", "unallowlisted_command", "install", "network", "live_write", "external_agent", "Dominion", "repair"}
        if not required.issubset(set(self.prohibited_runtime_actions)):
            raise ValueError("prohibited_runtime_actions must include unsafe test execution actions")
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class ControlledTestCommandLine:
    command_line_id: str
    executable_name: str
    argv: list[str]
    command_summary: str
    structured_argv: bool
    shell: bool
    allowlisted: bool
    contains_blocked_arg: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("command_line_id", self.command_line_id)
        _require_non_blank("executable_name", self.executable_name)
        _require_non_blank("command_summary", self.command_summary)
        _validate_string_list("argv", self.argv)
        if not self.argv:
            raise ValueError("argv must be non-empty")
        _validate_true("structured_argv", self.structured_argv)
        _validate_false("shell", self.shell)
        _validate_true("allowlisted", self.allowlisted)
        _validate_false("contains_blocked_arg", self.contains_blocked_arg)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class ControlledTestEnvironment:
    environment_id: str
    environment_status: SandboxTestEnvironmentStatus | str
    env_preview_keys: list[str]
    blocked_env_keys: list[str]
    minimal_env: bool
    inherited_env: bool
    credential_env_present: bool
    network_env_present: bool
    env: dict[str, str] = field(default_factory=dict, repr=False)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("environment_id", self.environment_id)
        _validate_string_list("env_preview_keys", self.env_preview_keys)
        _validate_string_list("blocked_env_keys", self.blocked_env_keys)
        _validate_true("minimal_env", self.minimal_env)
        _validate_false("inherited_env", self.inherited_env)
        _validate_false("credential_env_present", self.credential_env_present)
        _validate_false("network_env_present", self.network_env_present)
        _validate_dict("env", self.env)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class ControlledTestCwdValidation:
    cwd_validation_id: str
    sandbox_cwd_ref: str
    normalized_cwd_ref: str
    cwd_kind: str
    valid_sandbox_cwd: bool
    live_workspace_cwd: bool
    reference_cwd: bool
    outside_sandbox_cwd: bool
    validation_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("cwd_validation_id", self.cwd_validation_id)
        _require_non_blank("sandbox_cwd_ref", self.sandbox_cwd_ref)
        _require_non_blank("normalized_cwd_ref", self.normalized_cwd_ref)
        _require_non_blank("validation_summary", self.validation_summary)
        if self.valid_sandbox_cwd:
            _validate_false("live_workspace_cwd", self.live_workspace_cwd)
            _validate_false("reference_cwd", self.reference_cwd)
            _validate_false("outside_sandbox_cwd", self.outside_sandbox_cwd)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class ControlledTestSubprocessInvocation:
    subprocess_invocation_id: str
    version: str
    execution_input_id: str
    subprocess_kind: ControlledTestSubprocessKind | str
    command_line: ControlledTestCommandLine
    cwd_validation: ControlledTestCwdValidation
    environment: ControlledTestEnvironment
    timeout_seconds: int
    output_limit_chars: int
    shell: bool
    executable_now: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("subprocess_invocation_id", self.subprocess_invocation_id)
        _validate_version(self.version)
        _require_non_blank("execution_input_id", self.execution_input_id)
        _validate_positive("timeout_seconds", self.timeout_seconds)
        _validate_positive("output_limit_chars", self.output_limit_chars)
        _validate_false("shell", self.shell)
        if self.executable_now and not self.cwd_validation.valid_sandbox_cwd:
            raise ValueError("executable_now requires valid sandbox cwd")
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class ControlledTestSubprocessResult:
    subprocess_result_id: str
    version: str
    subprocess_invocation_id: str
    subprocess_status: ControlledTestSubprocessStatus | str
    exit_kind: SandboxTestProcessExitKind | str
    return_code: int | None
    timed_out: bool
    duration_ms: int | None
    stdout_text: str
    stderr_text: str
    stdout_truncated: bool
    stderr_truncated: bool
    output_redacted: bool
    shell_used: bool
    dependency_install_attempted: bool
    network_access_allowed: bool
    live_workspace_write_allowed: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("subprocess_result_id", self.subprocess_result_id)
        _validate_version(self.version)
        _require_non_blank("subprocess_invocation_id", self.subprocess_invocation_id)
        _validate_non_negative("duration_ms", self.duration_ms)
        _validate_false("shell_used", self.shell_used)
        _validate_false("dependency_install_attempted", self.dependency_install_attempted)
        _validate_false("network_access_allowed", self.network_access_allowed)
        _validate_false("live_workspace_write_allowed", self.live_workspace_write_allowed)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestOutputCapture:
    output_capture_id: str
    version: str
    subprocess_result_id: str | None
    stream_kind: SandboxTestOutputStreamKind | str
    capture_status: SandboxTestOutputCaptureStatus | str
    captured_text: str
    original_char_count: int
    captured_char_count: int
    truncated: bool
    redacted: bool
    secret_like_content_detected: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("output_capture_id", self.output_capture_id)
        _validate_version(self.version)
        _validate_non_negative("original_char_count", self.original_char_count)
        _validate_non_negative("captured_char_count", self.captured_char_count)
        if self.captured_char_count != len(self.captured_text):
            raise ValueError("captured_char_count must match captured_text length")
        if self.secret_like_content_detected and not self.redacted:
            raise ValueError("secret-like output must be redacted")
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestExecutionResult:
    execution_result_id: str
    version: str
    execution_input_id: str
    execution_status: SandboxTestExecutionStatus | str
    readiness_level: SandboxTestExecutionReadinessLevel | str
    subprocess_invocation: ControlledTestSubprocessInvocation | None
    subprocess_result: ControlledTestSubprocessResult | None
    output_captures: list[SandboxTestOutputCapture]
    source_refs: list[SandboxTestExecutionSourceRef]
    summary: str
    test_process_completed: bool
    return_code: int | None
    timed_out: bool
    eligible_for_v0373_result_envelope: bool
    ready_for_v0373_test_result_envelope: bool
    ready_for_v0374_test_feedback_failure_diagnosis: bool
    ready_for_v0376_vera_codex_one_shot_agent_trial: bool
    ready_for_execution: bool
    ready_for_arbitrary_shell: bool
    ready_for_dependency_install: bool
    ready_for_network_access: bool
    ready_for_live_workspace_write: bool
    ready_for_automatic_repair: bool
    production_certified: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("execution_result_id", self.execution_result_id)
        _validate_version(self.version)
        _require_non_blank("execution_input_id", self.execution_input_id)
        _require_non_blank("summary", self.summary)
        _validate_list("output_captures", self.output_captures)
        _validate_list("source_refs", self.source_refs)
        for name in (
            "ready_for_execution",
            "ready_for_arbitrary_shell",
            "ready_for_dependency_install",
            "ready_for_network_access",
            "ready_for_live_workspace_write",
            "ready_for_automatic_repair",
            "production_certified",
        ):
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestExecutionDecision:
    execution_decision_id: str
    execution_input_id: str
    decision_kind: SandboxTestExecutionDecisionKind | str
    execution_status: SandboxTestExecutionStatus | str
    risk_kinds: list[SandboxTestExecutionRiskKind | str]
    decision_summary: str
    controlled_subprocess_allowed: bool
    allowlisted_test_execution_allowed: bool
    bounded_output_capture_allowed: bool
    future_result_envelope_input_allowed: bool
    arbitrary_shell_allowed: bool
    uncontrolled_subprocess_allowed: bool
    dependency_install_allowed: bool
    network_access_allowed: bool
    live_workspace_write_allowed: bool
    automatic_repair_allowed: bool
    external_agent_allowed: bool
    dominion_runtime_allowed: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("execution_decision_id", self.execution_decision_id)
        _require_non_blank("execution_input_id", self.execution_input_id)
        _require_non_blank("decision_summary", self.decision_summary)
        _validate_list("risk_kinds", self.risk_kinds)
        for name in UNSAFE_DECISION_ALLOW_NAMES:
            _validate_false(name, getattr(self, name))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestExecutionValidationFinding:
    finding_id: str
    risk_kind: SandboxTestExecutionRiskKind | str
    severity: str
    message: str
    blocks_execution: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("severity", self.severity)
        _require_non_blank("message", self.message)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestExecutionValidationReport:
    validation_report_id: str
    version: str
    execution_input_id: str
    findings: list[SandboxTestExecutionValidationFinding]
    decision: SandboxTestExecutionDecision
    allowlist_confirmed: bool
    sandbox_cwd_confirmed: bool
    shell_false_confirmed: bool
    timeout_confirmed: bool
    bounded_output_confirmed: bool
    minimal_env_confirmed: bool
    network_policy_blocked: bool
    network_hard_isolation_certified: bool
    summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version(self.version)
        _require_non_blank("execution_input_id", self.execution_input_id)
        _require_non_blank("summary", self.summary)
        _validate_list("findings", self.findings)
        _validate_true("network_policy_blocked", self.network_policy_blocked)
        _validate_false("network_hard_isolation_certified", self.network_hard_isolation_certified)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestExecutionReport:
    execution_report_id: str
    version: str
    execution_result: SandboxTestExecutionResult
    validation_report: SandboxTestExecutionValidationReport | None
    process_completed: bool
    report_summary: str
    production_certified: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("execution_report_id", self.execution_report_id)
        _validate_version(self.version)
        _require_non_blank("report_summary", self.report_summary)
        _validate_false("production_certified", self.production_certified)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestExecutionRunPreview:
    run_preview_id: str
    version: str
    execution_input_id: str
    command_line: ControlledTestCommandLine | None
    cwd_validation: ControlledTestCwdValidation | None
    ready_to_run_controlled_subprocess: bool
    ready_for_arbitrary_shell: bool
    ready_for_dependency_install: bool
    ready_for_network_access: bool
    preview_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        _validate_version(self.version)
        _require_non_blank("execution_input_id", self.execution_input_id)
        _require_non_blank("preview_summary", self.preview_summary)
        _validate_false("ready_for_arbitrary_shell", self.ready_for_arbitrary_shell)
        _validate_false("ready_for_dependency_install", self.ready_for_dependency_install)
        _validate_false("ready_for_network_access", self.ready_for_network_access)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestExecutionNoUnsafeCommandGuarantee:
    guarantee_id: str
    version: str
    no_arbitrary_shell: bool
    no_shell_true: bool
    no_uncontrolled_subprocess: bool
    no_unallowlisted_command: bool
    no_dependency_install: bool
    no_network_permission: bool
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
class V0372ReadinessReport:
    readiness_report_id: str
    version: str
    readiness_level: SandboxTestExecutionReadinessLevel | str
    status: SandboxTestExecutionStatus | str
    summary: str
    ready_for_v0373_test_result_envelope: bool
    ready_for_v0374_test_feedback_failure_diagnosis: bool
    ready_for_v0376_vera_codex_one_shot_agent_trial: bool
    ready_for_sandbox_test_execution_engine: bool
    ready_for_controlled_test_subprocess: bool
    ready_for_allowlisted_test_execution: bool
    ready_for_pytest_module_execution: bool
    ready_for_unittest_module_execution: bool
    ready_for_bounded_test_output_capture: bool
    ready_for_test_timeout_enforcement: bool
    ready_for_minimal_test_environment: bool
    ready_for_future_test_result_envelope_input: bool
    ready_for_execution: bool
    ready_for_arbitrary_shell: bool
    ready_for_uncontrolled_subprocess: bool
    ready_for_dependency_install: bool
    ready_for_network_access: bool
    ready_for_live_workspace_write: bool
    ready_for_patch_application: bool
    ready_for_automatic_repair: bool
    ready_for_repair_loop: bool
    ready_for_retry_loop: bool
    ready_for_multi_cycle_agentic_loop: bool
    ready_for_vera_codex_trial_execution: bool
    ready_for_cold_agent_performance_evaluation: bool
    ready_for_external_agent_execution: bool
    ready_for_dominion_runtime: bool
    production_certified: bool
    network_policy_blocked: bool
    network_hard_isolation_certified: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("readiness_report_id", self.readiness_report_id)
        _validate_version(self.version)
        _require_non_blank("summary", self.summary)
        for name in (
            "ready_for_execution",
            "ready_for_arbitrary_shell",
            "ready_for_uncontrolled_subprocess",
            "ready_for_dependency_install",
            "ready_for_network_access",
            "ready_for_live_workspace_write",
            "ready_for_patch_application",
            "ready_for_automatic_repair",
            "ready_for_repair_loop",
            "ready_for_retry_loop",
            "ready_for_multi_cycle_agentic_loop",
            "ready_for_vera_codex_trial_execution",
            "ready_for_cold_agent_performance_evaluation",
            "ready_for_external_agent_execution",
            "ready_for_dominion_runtime",
            "production_certified",
            "network_hard_isolation_certified",
        ):
            _validate_false(name, getattr(self, name))
        _validate_true("network_policy_blocked", self.network_policy_blocked)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


def build_sandbox_test_execution_flags(**kwargs: Any) -> SandboxTestExecutionFlagSet:
    return SandboxTestExecutionFlagSet(
        flag_set_id=kwargs.pop("flag_set_id", "sandbox_test_execution_flags:v0.37.2"),
        version=kwargs.pop("version", V0372_VERSION),
        sandbox_test_execution_engine_constructed=kwargs.pop("sandbox_test_execution_engine_constructed", True),
        controlled_subprocess_runner_available=kwargs.pop("controlled_subprocess_runner_available", True),
        allowlisted_test_execution_available=kwargs.pop("allowlisted_test_execution_available", True),
        bounded_output_capture_available=kwargs.pop("bounded_output_capture_available", True),
        timeout_enforcement_available=kwargs.pop("timeout_enforcement_available", True),
        minimal_environment_available=kwargs.pop("minimal_environment_available", True),
        ready_for_v0373_test_result_envelope=kwargs.pop("ready_for_v0373_test_result_envelope", True),
        ready_for_v0374_test_feedback_failure_diagnosis=kwargs.pop("ready_for_v0374_test_feedback_failure_diagnosis", True),
        ready_for_v0376_vera_codex_one_shot_agent_trial=kwargs.pop("ready_for_v0376_vera_codex_one_shot_agent_trial", True),
        ready_for_sandbox_test_execution_engine=kwargs.pop("ready_for_sandbox_test_execution_engine", True),
        ready_for_controlled_test_subprocess=kwargs.pop("ready_for_controlled_test_subprocess", True),
        ready_for_allowlisted_test_execution=kwargs.pop("ready_for_allowlisted_test_execution", True),
        ready_for_pytest_module_execution=kwargs.pop("ready_for_pytest_module_execution", True),
        ready_for_unittest_module_execution=kwargs.pop("ready_for_unittest_module_execution", True),
        ready_for_bounded_test_output_capture=kwargs.pop("ready_for_bounded_test_output_capture", True),
        ready_for_test_timeout_enforcement=kwargs.pop("ready_for_test_timeout_enforcement", True),
        ready_for_minimal_test_environment=kwargs.pop("ready_for_minimal_test_environment", True),
        ready_for_future_test_result_envelope_input=kwargs.pop("ready_for_future_test_result_envelope_input", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_EXECUTION_FLAG_NAMES},
    )


def build_sandbox_test_execution_source_ref(**kwargs: Any) -> SandboxTestExecutionSourceRef:
    return SandboxTestExecutionSourceRef(
        source_ref_id=kwargs.pop("source_ref_id", "sandbox_test_execution_source_ref:v0.37.2"),
        source_kind=kwargs.pop("source_kind", SandboxTestExecutionSourceKind.V0371_TEST_INVOCATION_CONTRACT),
        source_id=kwargs.pop("source_id", "v0.37.1"),
        source_summary=kwargs.pop("source_summary", "v0.37.1 invocation contract metadata"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.1 contract"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_execution_policy(**kwargs: Any) -> SandboxTestExecutionPolicy:
    return SandboxTestExecutionPolicy(
        execution_policy_id=kwargs.pop("execution_policy_id", "sandbox_test_execution_policy:v0.37.2"),
        version=kwargs.pop("version", V0372_VERSION),
        allowed_modes=kwargs.pop("allowed_modes", [
            SandboxTestExecutionMode.ALLOWLISTED_PYTHON_MODULE_EXECUTION,
            SandboxTestExecutionMode.ALLOWLISTED_PYTEST_EXECUTION,
            SandboxTestExecutionMode.ALLOWLISTED_UNITTEST_EXECUTION,
        ]),
        blocked_modes=kwargs.pop("blocked_modes", [SandboxTestExecutionMode.BLOCKED, SandboxTestExecutionMode.UNKNOWN]),
        require_invocation_contract=kwargs.pop("require_invocation_contract", True),
        require_allowlisted_command=kwargs.pop("require_allowlisted_command", True),
        require_sandbox_cwd=kwargs.pop("require_sandbox_cwd", True),
        require_timeout=kwargs.pop("require_timeout", True),
        require_bounded_output=kwargs.pop("require_bounded_output", True),
        require_minimal_env=kwargs.pop("require_minimal_env", True),
        require_shell_false=kwargs.pop("require_shell_false", True),
        require_no_dependency_install=kwargs.pop("require_no_dependency_install", True),
        require_no_network_policy=kwargs.pop("require_no_network_policy", True),
        max_stdout_chars=kwargs.pop("max_stdout_chars", 10000),
        max_stderr_chars=kwargs.pop("max_stderr_chars", 10000),
        max_total_output_chars=kwargs.pop("max_total_output_chars", 20000),
        max_timeout_seconds=kwargs.pop("max_timeout_seconds", 300),
        allow_controlled_subprocess=kwargs.pop("allow_controlled_subprocess", True),
        allow_allowlisted_test_execution=kwargs.pop("allow_allowlisted_test_execution", True),
        allow_pytest_module_execution=kwargs.pop("allow_pytest_module_execution", True),
        allow_unittest_module_execution=kwargs.pop("allow_unittest_module_execution", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_POLICY_ALLOW_NAMES},
    )


def build_controlled_test_subprocess_policy(**kwargs: Any) -> ControlledTestSubprocessPolicy:
    return ControlledTestSubprocessPolicy(
        subprocess_policy_id=kwargs.pop("subprocess_policy_id", "controlled_test_subprocess_policy:v0.37.2"),
        version=kwargs.pop("version", V0372_VERSION),
        allowed_subprocess_kinds=kwargs.pop("allowed_subprocess_kinds", [
            ControlledTestSubprocessKind.PYTHON_MODULE_SUBPROCESS,
            ControlledTestSubprocessKind.PYTHON_PYTEST_MODULE_SUBPROCESS,
            ControlledTestSubprocessKind.PYTHON_UNITTEST_MODULE_SUBPROCESS,
        ]),
        blocked_subprocess_kinds=kwargs.pop("blocked_subprocess_kinds", [
            ControlledTestSubprocessKind.BLOCKED_SHELL_SUBPROCESS,
            ControlledTestSubprocessKind.BLOCKED_PACKAGE_MANAGER_SUBPROCESS,
            ControlledTestSubprocessKind.BLOCKED_EXTERNAL_AGENT_SUBPROCESS,
            ControlledTestSubprocessKind.UNKNOWN,
        ]),
        require_structured_argv=kwargs.pop("require_structured_argv", True),
        require_shell_false=kwargs.pop("require_shell_false", True),
        require_timeout=kwargs.pop("require_timeout", True),
        require_sandbox_cwd=kwargs.pop("require_sandbox_cwd", True),
        require_minimal_env=kwargs.pop("require_minimal_env", True),
        require_bounded_output=kwargs.pop("require_bounded_output", True),
        allow_subprocess_run=kwargs.pop("allow_subprocess_run", True),
        allow_shell_true=kwargs.pop("allow_shell_true", False),
        allow_command_string=kwargs.pop("allow_command_string", False),
        allow_package_manager=kwargs.pop("allow_package_manager", False),
        allow_external_agent=kwargs.pop("allow_external_agent", False),
        allow_network_access=kwargs.pop("allow_network_access", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_execution_input(**kwargs: Any) -> SandboxTestExecutionInput:
    return SandboxTestExecutionInput(
        execution_input_id=kwargs.pop("execution_input_id", "sandbox_test_execution_input:v0.37.2"),
        version=kwargs.pop("version", V0372_VERSION),
        invocation_contract_id=kwargs.pop("invocation_contract_id", "sandbox_test_invocation_contract:v0.37.1"),
        invocation_decision_id=kwargs.pop("invocation_decision_id", "sandbox_test_invocation_decision:v0.37.1"),
        command_spec_id=kwargs.pop("command_spec_id", "sandbox_test_command_spec:pytest_module:v0.37.1"),
        requested_mode=kwargs.pop("requested_mode", SandboxTestExecutionMode.ALLOWLISTED_PYTEST_EXECUTION),
        sandbox_cwd_ref=kwargs.pop("sandbox_cwd_ref", "."),
        timeout_seconds=kwargs.pop("timeout_seconds", 60),
        source_refs=kwargs.pop("source_refs", [build_sandbox_test_execution_source_ref()]),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", ["shell", "unallowlisted_command", "install", "network", "live_write", "external_agent", "Dominion", "repair"]),
        task_summary=kwargs.pop("task_summary", "controlled sandbox test execution request"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_controlled_test_command_line(**kwargs: Any) -> ControlledTestCommandLine:
    argv = kwargs.pop("argv", ["python", "-m", "pytest", "--version"])
    return ControlledTestCommandLine(
        command_line_id=kwargs.pop("command_line_id", "controlled_test_command_line:v0.37.2"),
        executable_name=kwargs.pop("executable_name", argv[0]),
        argv=argv,
        command_summary=kwargs.pop("command_summary", "structured allowlisted argv"),
        structured_argv=kwargs.pop("structured_argv", True),
        shell=kwargs.pop("shell", False),
        allowlisted=kwargs.pop("allowlisted", True),
        contains_blocked_arg=kwargs.pop("contains_blocked_arg", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_controlled_test_environment(**kwargs: Any) -> ControlledTestEnvironment:
    env = kwargs.pop("env", {"PYTHONNOUSERSITE": "1", "PYTHONDONTWRITEBYTECODE": "1"})
    return ControlledTestEnvironment(
        environment_id=kwargs.pop("environment_id", "controlled_test_environment:v0.37.2"),
        environment_status=kwargs.pop("environment_status", SandboxTestEnvironmentStatus.MINIMAL_ENV_PREPARED),
        env_preview_keys=kwargs.pop("env_preview_keys", sorted(env.keys())),
        blocked_env_keys=kwargs.pop("blocked_env_keys", list(SECRET_MARKERS)),
        minimal_env=kwargs.pop("minimal_env", True),
        inherited_env=kwargs.pop("inherited_env", False),
        credential_env_present=kwargs.pop("credential_env_present", False),
        network_env_present=kwargs.pop("network_env_present", False),
        env=env,
        metadata=kwargs.pop("metadata", {}),
    )


def build_controlled_test_cwd_validation(**kwargs: Any) -> ControlledTestCwdValidation:
    sandbox_cwd_ref = kwargs.pop("sandbox_cwd_ref", ".")
    normalized = kwargs.pop("normalized_cwd_ref", str(Path(sandbox_cwd_ref).resolve()))
    return ControlledTestCwdValidation(
        cwd_validation_id=kwargs.pop("cwd_validation_id", "controlled_test_cwd_validation:v0.37.2"),
        sandbox_cwd_ref=sandbox_cwd_ref,
        normalized_cwd_ref=normalized,
        cwd_kind=kwargs.pop("cwd_kind", "sandbox_root"),
        valid_sandbox_cwd=kwargs.pop("valid_sandbox_cwd", True),
        live_workspace_cwd=kwargs.pop("live_workspace_cwd", False),
        reference_cwd=kwargs.pop("reference_cwd", False),
        outside_sandbox_cwd=kwargs.pop("outside_sandbox_cwd", False),
        validation_summary=kwargs.pop("validation_summary", "sandbox cwd validated"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_controlled_test_subprocess_invocation(**kwargs: Any) -> ControlledTestSubprocessInvocation:
    execution_input = kwargs.pop("execution_input", build_sandbox_test_execution_input())
    return ControlledTestSubprocessInvocation(
        subprocess_invocation_id=kwargs.pop("subprocess_invocation_id", "controlled_test_subprocess_invocation:v0.37.2"),
        version=kwargs.pop("version", V0372_VERSION),
        execution_input_id=kwargs.pop("execution_input_id", execution_input.execution_input_id),
        subprocess_kind=kwargs.pop("subprocess_kind", ControlledTestSubprocessKind.PYTHON_PYTEST_MODULE_SUBPROCESS),
        command_line=kwargs.pop("command_line", build_controlled_test_command_line()),
        cwd_validation=kwargs.pop("cwd_validation", build_controlled_test_cwd_validation(sandbox_cwd_ref=execution_input.sandbox_cwd_ref)),
        environment=kwargs.pop("environment", build_controlled_test_environment()),
        timeout_seconds=kwargs.pop("timeout_seconds", execution_input.timeout_seconds),
        output_limit_chars=kwargs.pop("output_limit_chars", 20000),
        shell=kwargs.pop("shell", False),
        executable_now=kwargs.pop("executable_now", True),
        metadata=kwargs.pop("metadata", {}),
    )


def build_controlled_test_subprocess_result(**kwargs: Any) -> ControlledTestSubprocessResult:
    return ControlledTestSubprocessResult(
        subprocess_result_id=kwargs.pop("subprocess_result_id", "controlled_test_subprocess_result:v0.37.2"),
        version=kwargs.pop("version", V0372_VERSION),
        subprocess_invocation_id=kwargs.pop("subprocess_invocation_id", "controlled_test_subprocess_invocation:v0.37.2"),
        subprocess_status=kwargs.pop("subprocess_status", ControlledTestSubprocessStatus.NOT_STARTED),
        exit_kind=kwargs.pop("exit_kind", SandboxTestProcessExitKind.NOT_EXECUTED),
        return_code=kwargs.pop("return_code", None),
        timed_out=kwargs.pop("timed_out", False),
        duration_ms=kwargs.pop("duration_ms", None),
        stdout_text=kwargs.pop("stdout_text", ""),
        stderr_text=kwargs.pop("stderr_text", ""),
        stdout_truncated=kwargs.pop("stdout_truncated", False),
        stderr_truncated=kwargs.pop("stderr_truncated", False),
        output_redacted=kwargs.pop("output_redacted", False),
        shell_used=kwargs.pop("shell_used", False),
        dependency_install_attempted=kwargs.pop("dependency_install_attempted", False),
        network_access_allowed=kwargs.pop("network_access_allowed", False),
        live_workspace_write_allowed=kwargs.pop("live_workspace_write_allowed", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_output_capture(**kwargs: Any) -> SandboxTestOutputCapture:
    captured_text = kwargs.pop("captured_text", "")
    return SandboxTestOutputCapture(
        output_capture_id=kwargs.pop("output_capture_id", "sandbox_test_output_capture:v0.37.2"),
        version=kwargs.pop("version", V0372_VERSION),
        subprocess_result_id=kwargs.pop("subprocess_result_id", None),
        stream_kind=kwargs.pop("stream_kind", SandboxTestOutputStreamKind.STDOUT),
        capture_status=kwargs.pop("capture_status", SandboxTestOutputCaptureStatus.CAPTURED if captured_text else SandboxTestOutputCaptureStatus.NOT_CAPTURED),
        captured_text=captured_text,
        original_char_count=kwargs.pop("original_char_count", len(captured_text)),
        captured_char_count=kwargs.pop("captured_char_count", len(captured_text)),
        truncated=kwargs.pop("truncated", False),
        redacted=kwargs.pop("redacted", False),
        secret_like_content_detected=kwargs.pop("secret_like_content_detected", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_execution_result(**kwargs: Any) -> SandboxTestExecutionResult:
    return SandboxTestExecutionResult(
        execution_result_id=kwargs.pop("execution_result_id", "sandbox_test_execution_result:v0.37.2"),
        version=kwargs.pop("version", V0372_VERSION),
        execution_input_id=kwargs.pop("execution_input_id", "sandbox_test_execution_input:v0.37.2"),
        execution_status=kwargs.pop("execution_status", SandboxTestExecutionStatus.EXECUTION_COMPLETED),
        readiness_level=kwargs.pop("readiness_level", SandboxTestExecutionReadinessLevel.RESULT_METADATA_READY),
        subprocess_invocation=kwargs.pop("subprocess_invocation", None),
        subprocess_result=kwargs.pop("subprocess_result", None),
        output_captures=kwargs.pop("output_captures", []),
        source_refs=kwargs.pop("source_refs", [build_sandbox_test_execution_source_ref()]),
        summary=kwargs.pop("summary", "sandbox test execution result metadata"),
        test_process_completed=kwargs.pop("test_process_completed", True),
        return_code=kwargs.pop("return_code", 0),
        timed_out=kwargs.pop("timed_out", False),
        eligible_for_v0373_result_envelope=kwargs.pop("eligible_for_v0373_result_envelope", True),
        ready_for_v0373_test_result_envelope=kwargs.pop("ready_for_v0373_test_result_envelope", True),
        ready_for_v0374_test_feedback_failure_diagnosis=kwargs.pop("ready_for_v0374_test_feedback_failure_diagnosis", True),
        ready_for_v0376_vera_codex_one_shot_agent_trial=kwargs.pop("ready_for_v0376_vera_codex_one_shot_agent_trial", True),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        ready_for_arbitrary_shell=kwargs.pop("ready_for_arbitrary_shell", False),
        ready_for_dependency_install=kwargs.pop("ready_for_dependency_install", False),
        ready_for_network_access=kwargs.pop("ready_for_network_access", False),
        ready_for_live_workspace_write=kwargs.pop("ready_for_live_workspace_write", False),
        ready_for_automatic_repair=kwargs.pop("ready_for_automatic_repair", False),
        production_certified=kwargs.pop("production_certified", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_execution_decision(**kwargs: Any) -> SandboxTestExecutionDecision:
    return SandboxTestExecutionDecision(
        execution_decision_id=kwargs.pop("execution_decision_id", "sandbox_test_execution_decision:v0.37.2"),
        execution_input_id=kwargs.pop("execution_input_id", "sandbox_test_execution_input:v0.37.2"),
        decision_kind=kwargs.pop("decision_kind", SandboxTestExecutionDecisionKind.ALLOW_CONTROLLED_SANDBOX_TEST_EXECUTION),
        execution_status=kwargs.pop("execution_status", SandboxTestExecutionStatus.COMMAND_ALLOWED),
        risk_kinds=kwargs.pop("risk_kinds", [SandboxTestExecutionRiskKind.NETWORK_HARD_ISOLATION_UNCERTIFIED_RISK]),
        decision_summary=kwargs.pop("decision_summary", "controlled sandbox test execution allowed only through bounded helper"),
        controlled_subprocess_allowed=kwargs.pop("controlled_subprocess_allowed", True),
        allowlisted_test_execution_allowed=kwargs.pop("allowlisted_test_execution_allowed", True),
        bounded_output_capture_allowed=kwargs.pop("bounded_output_capture_allowed", True),
        future_result_envelope_input_allowed=kwargs.pop("future_result_envelope_input_allowed", True),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.2 controlled execution policy"]),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_DECISION_ALLOW_NAMES},
    )


def build_sandbox_test_execution_validation_finding(**kwargs: Any) -> SandboxTestExecutionValidationFinding:
    return SandboxTestExecutionValidationFinding(
        finding_id=kwargs.pop("finding_id", "sandbox_test_execution_finding:v0.37.2"),
        risk_kind=kwargs.pop("risk_kind", SandboxTestExecutionRiskKind.UNKNOWN),
        severity=kwargs.pop("severity", "info"),
        message=kwargs.pop("message", "execution validation finding"),
        blocks_execution=kwargs.pop("blocks_execution", False),
        evidence_refs=kwargs.pop("evidence_refs", []),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_execution_validation_report(**kwargs: Any) -> SandboxTestExecutionValidationReport:
    decision = kwargs.pop("decision", build_sandbox_test_execution_decision())
    return SandboxTestExecutionValidationReport(
        validation_report_id=kwargs.pop("validation_report_id", "sandbox_test_execution_validation_report:v0.37.2"),
        version=kwargs.pop("version", V0372_VERSION),
        execution_input_id=kwargs.pop("execution_input_id", decision.execution_input_id),
        findings=kwargs.pop("findings", []),
        decision=decision,
        allowlist_confirmed=kwargs.pop("allowlist_confirmed", True),
        sandbox_cwd_confirmed=kwargs.pop("sandbox_cwd_confirmed", True),
        shell_false_confirmed=kwargs.pop("shell_false_confirmed", True),
        timeout_confirmed=kwargs.pop("timeout_confirmed", True),
        bounded_output_confirmed=kwargs.pop("bounded_output_confirmed", True),
        minimal_env_confirmed=kwargs.pop("minimal_env_confirmed", True),
        network_policy_blocked=kwargs.pop("network_policy_blocked", True),
        network_hard_isolation_certified=kwargs.pop("network_hard_isolation_certified", False),
        summary=kwargs.pop("summary", "controlled execution gates validated"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.2 validation"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_execution_report(**kwargs: Any) -> SandboxTestExecutionReport:
    result = kwargs.pop("execution_result", build_sandbox_test_execution_result())
    return SandboxTestExecutionReport(
        execution_report_id=kwargs.pop("execution_report_id", "sandbox_test_execution_report:v0.37.2"),
        version=kwargs.pop("version", V0372_VERSION),
        execution_result=result,
        validation_report=kwargs.pop("validation_report", None),
        process_completed=kwargs.pop("process_completed", result.test_process_completed),
        report_summary=kwargs.pop("report_summary", "sandbox process report; not production certification"),
        production_certified=kwargs.pop("production_certified", False),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.2 execution result"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_execution_run_preview(**kwargs: Any) -> SandboxTestExecutionRunPreview:
    return SandboxTestExecutionRunPreview(
        run_preview_id=kwargs.pop("run_preview_id", "sandbox_test_execution_run_preview:v0.37.2"),
        version=kwargs.pop("version", V0372_VERSION),
        execution_input_id=kwargs.pop("execution_input_id", "sandbox_test_execution_input:v0.37.2"),
        command_line=kwargs.pop("command_line", build_controlled_test_command_line()),
        cwd_validation=kwargs.pop("cwd_validation", build_controlled_test_cwd_validation()),
        ready_to_run_controlled_subprocess=kwargs.pop("ready_to_run_controlled_subprocess", True),
        ready_for_arbitrary_shell=kwargs.pop("ready_for_arbitrary_shell", False),
        ready_for_dependency_install=kwargs.pop("ready_for_dependency_install", False),
        ready_for_network_access=kwargs.pop("ready_for_network_access", False),
        preview_summary=kwargs.pop("preview_summary", "controlled run preview only"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.2 preview"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_execution_no_unsafe_command_guarantee(**kwargs: Any) -> SandboxTestExecutionNoUnsafeCommandGuarantee:
    no_names = tuple(name for name in SandboxTestExecutionNoUnsafeCommandGuarantee.__dataclass_fields__ if name.startswith("no_"))
    return SandboxTestExecutionNoUnsafeCommandGuarantee(
        guarantee_id=kwargs.pop("guarantee_id", "sandbox_test_execution_no_unsafe_command_guarantee:v0.37.2"),
        version=kwargs.pop("version", V0372_VERSION),
        summary=kwargs.pop("summary", "v0.37.2 controlled subprocess is narrow and blocks unsafe runtime authority"),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, True) for name in no_names},
    )


def build_v0372_readiness_report(**kwargs: Any) -> V0372ReadinessReport:
    return V0372ReadinessReport(
        readiness_report_id=kwargs.pop("readiness_report_id", "v0372_readiness_report"),
        version=kwargs.pop("version", V0372_VERSION),
        readiness_level=kwargs.pop("readiness_level", SandboxTestExecutionReadinessLevel.DESIGN_HANDOFF_READY_FOR_V0373),
        status=kwargs.pop("status", SandboxTestExecutionStatus.COMMAND_ALLOWED),
        summary=kwargs.pop("summary", "v0.37.2 controlled sandbox test execution ready; general execution remains false"),
        ready_for_v0373_test_result_envelope=kwargs.pop("ready_for_v0373_test_result_envelope", True),
        ready_for_v0374_test_feedback_failure_diagnosis=kwargs.pop("ready_for_v0374_test_feedback_failure_diagnosis", True),
        ready_for_v0376_vera_codex_one_shot_agent_trial=kwargs.pop("ready_for_v0376_vera_codex_one_shot_agent_trial", True),
        ready_for_sandbox_test_execution_engine=kwargs.pop("ready_for_sandbox_test_execution_engine", True),
        ready_for_controlled_test_subprocess=kwargs.pop("ready_for_controlled_test_subprocess", True),
        ready_for_allowlisted_test_execution=kwargs.pop("ready_for_allowlisted_test_execution", True),
        ready_for_pytest_module_execution=kwargs.pop("ready_for_pytest_module_execution", True),
        ready_for_unittest_module_execution=kwargs.pop("ready_for_unittest_module_execution", True),
        ready_for_bounded_test_output_capture=kwargs.pop("ready_for_bounded_test_output_capture", True),
        ready_for_test_timeout_enforcement=kwargs.pop("ready_for_test_timeout_enforcement", True),
        ready_for_minimal_test_environment=kwargs.pop("ready_for_minimal_test_environment", True),
        ready_for_future_test_result_envelope_input=kwargs.pop("ready_for_future_test_result_envelope_input", True),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        ready_for_arbitrary_shell=kwargs.pop("ready_for_arbitrary_shell", False),
        ready_for_uncontrolled_subprocess=kwargs.pop("ready_for_uncontrolled_subprocess", False),
        ready_for_dependency_install=kwargs.pop("ready_for_dependency_install", False),
        ready_for_network_access=kwargs.pop("ready_for_network_access", False),
        ready_for_live_workspace_write=kwargs.pop("ready_for_live_workspace_write", False),
        ready_for_patch_application=kwargs.pop("ready_for_patch_application", False),
        ready_for_automatic_repair=kwargs.pop("ready_for_automatic_repair", False),
        ready_for_repair_loop=kwargs.pop("ready_for_repair_loop", False),
        ready_for_retry_loop=kwargs.pop("ready_for_retry_loop", False),
        ready_for_multi_cycle_agentic_loop=kwargs.pop("ready_for_multi_cycle_agentic_loop", False),
        ready_for_vera_codex_trial_execution=kwargs.pop("ready_for_vera_codex_trial_execution", False),
        ready_for_cold_agent_performance_evaluation=kwargs.pop("ready_for_cold_agent_performance_evaluation", False),
        ready_for_external_agent_execution=kwargs.pop("ready_for_external_agent_execution", False),
        ready_for_dominion_runtime=kwargs.pop("ready_for_dominion_runtime", False),
        production_certified=kwargs.pop("production_certified", False),
        network_policy_blocked=kwargs.pop("network_policy_blocked", True),
        network_hard_isolation_certified=kwargs.pop("network_hard_isolation_certified", False),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.2 execution engine"]),
        metadata=kwargs.pop("metadata", {}),
    )


def default_sandbox_test_execution_policy(**kwargs: Any) -> SandboxTestExecutionPolicy:
    return build_sandbox_test_execution_policy(**kwargs)


def default_controlled_test_subprocess_policy(**kwargs: Any) -> ControlledTestSubprocessPolicy:
    return build_controlled_test_subprocess_policy(**kwargs)


def build_sandbox_test_execution_input_from_invocation_contract(
    contract: SandboxTestInvocationContract,
    decision: SandboxTestInvocationDecision | None = None,
    sandbox_cwd_ref: str = ".",
    **kwargs: Any,
) -> SandboxTestExecutionInput:
    if not sandbox_test_invocation_contract_is_not_execution(contract):
        raise ValueError("contract must preserve v0.37.1 no-execution boundaries")
    if decision is not None and not sandbox_test_invocation_decision_is_not_execution(decision):
        raise ValueError("decision must preserve v0.37.1 no-execution boundaries")
    return build_sandbox_test_execution_input(
        invocation_contract_id=contract.invocation_contract_id,
        invocation_decision_id=decision.invocation_decision_id if decision else None,
        command_spec_id=contract.command_spec.command_spec_id,
        requested_mode=SandboxTestExecutionMode.ALLOWLISTED_PYTEST_EXECUTION,
        sandbox_cwd_ref=sandbox_cwd_ref,
        timeout_seconds=min(contract.timeout_policy.max_timeout_seconds, kwargs.pop("timeout_seconds", contract.timeout_policy.default_timeout_seconds)),
        **kwargs,
    )


def validate_controlled_test_cwd(
    sandbox_cwd_ref: str,
    sandbox_root_ref: str | None = None,
    live_workspace_ref: str | None = None,
) -> ControlledTestCwdValidation:
    _require_non_blank("sandbox_cwd_ref", sandbox_cwd_ref)
    cwd = Path(sandbox_cwd_ref).resolve()
    root = Path(sandbox_root_ref).resolve() if sandbox_root_ref else cwd
    live_root = Path(live_workspace_ref).resolve() if live_workspace_ref else None
    refs = {part.lower() for part in cwd.parts}
    reference_cwd = "references" in refs
    live_workspace_cwd = live_root is not None and cwd == live_root
    try:
        outside_sandbox_cwd = cwd != root and root not in cwd.parents
    except RuntimeError:
        outside_sandbox_cwd = True
    valid = not reference_cwd and not live_workspace_cwd and not outside_sandbox_cwd
    return build_controlled_test_cwd_validation(
        sandbox_cwd_ref=sandbox_cwd_ref,
        normalized_cwd_ref=str(cwd),
        cwd_kind="sandbox_root" if valid else "blocked",
        valid_sandbox_cwd=valid,
        live_workspace_cwd=live_workspace_cwd,
        reference_cwd=reference_cwd,
        outside_sandbox_cwd=outside_sandbox_cwd,
        validation_summary="sandbox cwd validated" if valid else "sandbox cwd blocked",
    )


def build_controlled_test_command_line_from_contract(
    contract: SandboxTestInvocationContract,
    extra_args: list[str] | None = None,
    denylist: SandboxTestCommandDenylist | None = None,
) -> ControlledTestCommandLine:
    if not sandbox_test_invocation_contract_is_not_execution(contract):
        raise ValueError("contract must preserve no-execution boundaries before command line construction")
    spec = contract.command_spec
    executable = spec.executable.executable_name
    module = spec.module.module_name if spec.module else None
    argv = [executable]
    if module:
        argv.extend(["-m", module])
    argv.extend(extra_args or ["--version"])
    contains_blocked = _contains_blocked_token(argv, denylist)
    if contains_blocked:
        raise ValueError("controlled test command line contains blocked token")
    return build_controlled_test_command_line(
        executable_name=executable,
        argv=argv,
        allowlisted=True,
        contains_blocked_arg=False,
        command_summary="command line built from v0.37.1 invocation contract",
    )


def build_minimal_test_environment(**kwargs: Any) -> ControlledTestEnvironment:
    return build_controlled_test_environment(**kwargs)


def validate_controlled_test_subprocess_invocation(
    invocation: ControlledTestSubprocessInvocation,
    subprocess_policy: ControlledTestSubprocessPolicy | None = None,
) -> SandboxTestExecutionValidationReport:
    subprocess_policy = subprocess_policy or default_controlled_test_subprocess_policy()
    findings: list[SandboxTestExecutionValidationFinding] = []
    if _enum_value(invocation.subprocess_kind) not in {_enum_value(item) for item in subprocess_policy.allowed_subprocess_kinds}:
        findings.append(build_sandbox_test_execution_validation_finding(risk_kind=SandboxTestExecutionRiskKind.UNALLOWLISTED_COMMAND_RISK, severity="block", message="subprocess kind is not allowlisted", blocks_execution=True))
    if invocation.shell:
        findings.append(build_sandbox_test_execution_validation_finding(risk_kind=SandboxTestExecutionRiskKind.SHELL_TRUE_RISK, severity="block", message="shell must be False", blocks_execution=True))
    if not invocation.cwd_validation.valid_sandbox_cwd:
        findings.append(build_sandbox_test_execution_validation_finding(risk_kind=SandboxTestExecutionRiskKind.OUTSIDE_SANDBOX_CWD_RISK, severity="block", message="cwd is not valid sandbox cwd", blocks_execution=True))
    if _contains_blocked_token(invocation.command_line.argv):
        findings.append(build_sandbox_test_execution_validation_finding(risk_kind=SandboxTestExecutionRiskKind.COMMAND_INJECTION_RISK, severity="block", message="argv contains blocked token", blocks_execution=True))
    blocked = bool(findings)
    decision = build_sandbox_test_execution_decision(
        execution_input_id=invocation.execution_input_id,
        decision_kind=SandboxTestExecutionDecisionKind.BLOCK if blocked else SandboxTestExecutionDecisionKind.ALLOW_CONTROLLED_SANDBOX_TEST_EXECUTION,
        execution_status=SandboxTestExecutionStatus.EXECUTION_BLOCKED if blocked else SandboxTestExecutionStatus.COMMAND_ALLOWED,
        risk_kinds=[finding.risk_kind for finding in findings] + ([SandboxTestExecutionRiskKind.NETWORK_HARD_ISOLATION_UNCERTIFIED_RISK] if not blocked else []),
        controlled_subprocess_allowed=not blocked,
        allowlisted_test_execution_allowed=not blocked,
        bounded_output_capture_allowed=not blocked,
        future_result_envelope_input_allowed=not blocked,
        decision_summary="controlled subprocess validation blocked" if blocked else "controlled subprocess validation passed",
    )
    return build_sandbox_test_execution_validation_report(
        execution_input_id=invocation.execution_input_id,
        findings=findings,
        decision=decision,
        allowlist_confirmed=not blocked,
        sandbox_cwd_confirmed=invocation.cwd_validation.valid_sandbox_cwd,
        shell_false_confirmed=not invocation.shell,
        timeout_confirmed=invocation.timeout_seconds > 0,
        bounded_output_confirmed=invocation.output_limit_chars > 0,
        minimal_env_confirmed=invocation.environment.minimal_env,
        summary="controlled subprocess validation report",
    )


def bound_and_redact_test_output(
    text: str,
    limit: int,
    stream_kind: SandboxTestOutputStreamKind | str = SandboxTestOutputStreamKind.STDOUT,
    subprocess_result_id: str | None = None,
) -> SandboxTestOutputCapture:
    original_count = len(text)
    limited, truncated = _limit_output(text, limit)
    redacted_text, redacted = _redact_secret_like(limited)
    status = SandboxTestOutputCaptureStatus.CAPTURED
    if redacted:
        status = SandboxTestOutputCaptureStatus.CAPTURED_REDACTED
    if truncated:
        status = SandboxTestOutputCaptureStatus.CAPTURED_TRUNCATED
    return build_sandbox_test_output_capture(
        subprocess_result_id=subprocess_result_id,
        stream_kind=stream_kind,
        capture_status=status,
        captured_text=redacted_text,
        original_char_count=original_count,
        captured_char_count=len(redacted_text),
        truncated=truncated,
        redacted=redacted,
        secret_like_content_detected=redacted,
    )


def run_controlled_sandbox_test_subprocess(
    invocation: ControlledTestSubprocessInvocation,
    subprocess_policy: ControlledTestSubprocessPolicy | None = None,
) -> ControlledTestSubprocessResult:
    validation = validate_controlled_test_subprocess_invocation(invocation, subprocess_policy)
    if validation.findings:
        return build_controlled_test_subprocess_result(
            subprocess_invocation_id=invocation.subprocess_invocation_id,
            subprocess_status=ControlledTestSubprocessStatus.BLOCKED,
            exit_kind=SandboxTestProcessExitKind.BLOCKED_BEFORE_EXECUTION,
            metadata={"blocked": True, "findings": [finding.message for finding in validation.findings]},
        )
    start = time.perf_counter()
    try:
        completed = subprocess.run(
            invocation.command_line.argv,
            cwd=invocation.cwd_validation.normalized_cwd_ref,
            env=invocation.environment.env,
            shell=False,
            timeout=invocation.timeout_seconds,
            capture_output=True,
            text=True,
        )
    except subprocess.TimeoutExpired as exc:
        duration = int((time.perf_counter() - start) * 1000)
        stdout, stdout_truncated = _limit_output(exc.stdout or "", invocation.output_limit_chars)
        stderr, stderr_truncated = _limit_output(exc.stderr or "", invocation.output_limit_chars)
        stdout, stdout_redacted = _redact_secret_like(stdout)
        stderr, stderr_redacted = _redact_secret_like(stderr)
        return build_controlled_test_subprocess_result(
            subprocess_invocation_id=invocation.subprocess_invocation_id,
            subprocess_status=ControlledTestSubprocessStatus.TIMED_OUT,
            exit_kind=SandboxTestProcessExitKind.TIMEOUT,
            return_code=None,
            timed_out=True,
            duration_ms=duration,
            stdout_text=stdout,
            stderr_text=stderr,
            stdout_truncated=stdout_truncated,
            stderr_truncated=stderr_truncated,
            output_redacted=stdout_redacted or stderr_redacted,
        )
    except OSError as exc:
        duration = int((time.perf_counter() - start) * 1000)
        stderr, stderr_truncated = _limit_output(str(exc), invocation.output_limit_chars)
        stderr, stderr_redacted = _redact_secret_like(stderr)
        return build_controlled_test_subprocess_result(
            subprocess_invocation_id=invocation.subprocess_invocation_id,
            subprocess_status=ControlledTestSubprocessStatus.FAILED_SAFE,
            exit_kind=SandboxTestProcessExitKind.FAILED_TO_START_SAFE,
            return_code=None,
            timed_out=False,
            duration_ms=duration,
            stderr_text=stderr,
            stderr_truncated=stderr_truncated,
            output_redacted=stderr_redacted,
        )
    duration = int((time.perf_counter() - start) * 1000)
    stdout, stdout_truncated = _limit_output(completed.stdout or "", invocation.output_limit_chars)
    stderr, stderr_truncated = _limit_output(completed.stderr or "", invocation.output_limit_chars)
    stdout, stdout_redacted = _redact_secret_like(stdout)
    stderr, stderr_redacted = _redact_secret_like(stderr)
    return build_controlled_test_subprocess_result(
        subprocess_invocation_id=invocation.subprocess_invocation_id,
        subprocess_status=ControlledTestSubprocessStatus.COMPLETED if completed.returncode == 0 else ControlledTestSubprocessStatus.COMPLETED_NONZERO,
        exit_kind=SandboxTestProcessExitKind.EXIT_ZERO if completed.returncode == 0 else SandboxTestProcessExitKind.EXIT_NONZERO,
        return_code=completed.returncode,
        timed_out=False,
        duration_ms=duration,
        stdout_text=stdout,
        stderr_text=stderr,
        stdout_truncated=stdout_truncated,
        stderr_truncated=stderr_truncated,
        output_redacted=stdout_redacted or stderr_redacted,
    )


def run_sandbox_test_execution_engine(
    invocation: ControlledTestSubprocessInvocation,
    subprocess_policy: ControlledTestSubprocessPolicy | None = None,
) -> SandboxTestExecutionResult:
    result = run_controlled_sandbox_test_subprocess(invocation, subprocess_policy)
    stdout_capture = bound_and_redact_test_output(result.stdout_text, invocation.output_limit_chars, SandboxTestOutputStreamKind.STDOUT, result.subprocess_result_id)
    stderr_capture = bound_and_redact_test_output(result.stderr_text, invocation.output_limit_chars, SandboxTestOutputStreamKind.STDERR, result.subprocess_result_id)
    if result.timed_out:
        status = SandboxTestExecutionStatus.EXECUTION_TIMED_OUT
    elif result.return_code == 0:
        status = SandboxTestExecutionStatus.EXECUTION_COMPLETED
    elif result.return_code is None:
        status = SandboxTestExecutionStatus.EXECUTION_FAILED_SAFE
    else:
        status = SandboxTestExecutionStatus.EXECUTION_COMPLETED_WITH_NONZERO_EXIT
    return build_sandbox_test_execution_result(
        execution_input_id=invocation.execution_input_id,
        execution_status=status,
        subprocess_invocation=invocation,
        subprocess_result=result,
        output_captures=[stdout_capture, stderr_capture],
        test_process_completed=result.return_code is not None and not result.timed_out,
        return_code=result.return_code,
        timed_out=result.timed_out,
        summary="controlled sandbox test subprocess completed with process-level result",
    )


def validate_sandbox_test_execution_result(result: SandboxTestExecutionResult) -> SandboxTestExecutionValidationReport:
    findings: list[SandboxTestExecutionValidationFinding] = []
    if result.subprocess_result and result.subprocess_result.return_code not in (0, None):
        findings.append(build_sandbox_test_execution_validation_finding(risk_kind=SandboxTestExecutionRiskKind.NONZERO_EXIT_RISK, severity="info", message="process exited nonzero", blocks_execution=False))
    if result.timed_out:
        findings.append(build_sandbox_test_execution_validation_finding(risk_kind=SandboxTestExecutionRiskKind.PROCESS_TIMEOUT_RISK, severity="info", message="process timed out", blocks_execution=False))
    return build_sandbox_test_execution_validation_report(
        execution_input_id=result.execution_input_id,
        findings=findings,
        decision=build_sandbox_test_execution_decision(execution_input_id=result.execution_input_id),
        summary="execution result validation is process metadata only",
    )


def sandbox_test_execution_flags_preserve_no_unsafe_execution(flags: SandboxTestExecutionFlagSet) -> bool:
    return isinstance(flags, SandboxTestExecutionFlagSet) and all(getattr(flags, name) is False for name in UNSAFE_EXECUTION_FLAG_NAMES)


def sandbox_test_execution_policy_blocks_arbitrary_shell(policy: SandboxTestExecutionPolicy) -> bool:
    return isinstance(policy, SandboxTestExecutionPolicy) and all(getattr(policy, name) is False for name in UNSAFE_POLICY_ALLOW_NAMES)


def controlled_test_subprocess_invocation_is_shell_false(invocation: ControlledTestSubprocessInvocation) -> bool:
    return isinstance(invocation, ControlledTestSubprocessInvocation) and invocation.shell is False and invocation.command_line.shell is False


def sandbox_test_execution_result_is_not_production_certification(result: SandboxTestExecutionResult) -> bool:
    return isinstance(result, SandboxTestExecutionResult) and result.production_certified is False and result.ready_for_execution is False


def v0372_readiness_report_is_not_general_execution_ready(report: V0372ReadinessReport) -> bool:
    if not isinstance(report, V0372ReadinessReport):
        return False
    return (
        report.ready_for_execution is False
        and report.ready_for_arbitrary_shell is False
        and report.ready_for_uncontrolled_subprocess is False
        and report.ready_for_dependency_install is False
        and report.ready_for_network_access is False
        and report.ready_for_automatic_repair is False
        and report.ready_for_vera_codex_trial_execution is False
        and report.ready_for_external_agent_execution is False
        and report.ready_for_dominion_runtime is False
        and report.production_certified is False
        and report.network_policy_blocked is True
        and report.network_hard_isolation_certified is False
    )
