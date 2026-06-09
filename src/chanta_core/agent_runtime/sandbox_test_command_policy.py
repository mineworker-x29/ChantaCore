from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list


V0371_VERSION = "v0.37.1"
V0371_RELEASE_NAME = "v0.37.1 Allowlisted Test Command Policy & Test Invocation Contract"


UNSAFE_COMMAND_FLAG_NAMES = (
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

UNSAFE_DECISION_NAMES = (
    "executable_now",
    "test_execution_allowed",
    "controlled_subprocess_allowed",
    "shell_allowed",
    "dependency_install_allowed",
    "network_allowed",
    "live_workspace_allowed",
    "external_agent_allowed",
    "dominion_runtime_allowed",
)

BLOCKED_COMMAND_NAMES = (
    "sh",
    "bash",
    "zsh",
    "fish",
    "powershell",
    "pwsh",
    "cmd",
    "npm",
    "pnpm",
    "yarn",
    "pip",
    "poetry",
    "cargo",
    "go",
    "make",
    "git",
    "curl",
    "wget",
    "run-claude-code",
    "run-codex",
    "run-opencode",
    "run-hermes",
    "run-openclaw",
    "dominion",
    "auto-repair",
    "repair-loop",
    "retry-loop",
    "multi-cycle",
)

BLOCKED_ARGUMENT_PATTERNS = (
    ";",
    "&&",
    "||",
    "|",
    ">",
    "<",
    "$(",
    "`",
    " install ",
    "--install",
    "http://",
    "https://",
    "run-claude-code",
    "run-codex",
    "run-opencode",
    "run-hermes",
    "run-openclaw",
    "dominion",
    "auto-repair",
    "multi-cycle",
)


def _validate_list(name: str, value: Any) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{name} must be a list")


def _validate_dict(name: str, value: Any) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a dict")


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0371_VERSION not in version:
        raise ValueError("version must include v0.37.1")


def _validate_false(name: str, value: bool) -> None:
    if value is not False:
        raise ValueError(f"{name} must remain False in v0.37.1")


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


def _tokens_for_request(request: "SandboxTestInvocationRequest") -> list[str]:
    tokens = [request.requested_executable_name]
    if request.requested_module_name:
        tokens.append(request.requested_module_name)
    tokens.extend(request.requested_args)
    return [token.lower() for token in tokens]


class SandboxTestCommandKind(StrEnum):
    PYTHON_PYTEST_MODULE = "python_pytest_module"
    PYTHON_PYTEST_FILE = "python_pytest_file"
    PYTHON_PYTEST_NODE = "python_pytest_node"
    PYTHON_UNITTEST_MODULE = "python_unittest_module"
    PYTHON_MODULE_INVOCATION = "python_module_invocation"
    METADATA_ONLY = "metadata_only"
    BLOCKED_SHELL_COMMAND = "blocked_shell_command"
    BLOCKED_PACKAGE_SCRIPT = "blocked_package_script"
    BLOCKED_DEPENDENCY_INSTALL = "blocked_dependency_install"
    BLOCKED_NETWORK_COMMAND = "blocked_network_command"
    BLOCKED_EXTERNAL_AGENT_COMMAND = "blocked_external_agent_command"
    BLOCKED_DOMINION_COMMAND = "blocked_dominion_command"
    BLOCKED_REPAIR_COMMAND = "blocked_repair_command"
    BLOCKED_MULTI_CYCLE_COMMAND = "blocked_multi_cycle_command"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class SandboxTestInvocationSourceKind(StrEnum):
    V0370_SANDBOX_TEST_RUNNER_BOUNDARY = "v0370_sandbox_test_runner_boundary"
    V0369_PATCH_APPLY_SANDBOX_CONSOLIDATION = "v0369_patch_apply_sandbox_consolidation"
    V0368_CLI_SANDBOX_APPLY_SURFACE = "v0368_cli_sandbox_apply_surface"
    V0367_PATCH_APPLY_TRACE_PACKET = "v0367_patch_apply_trace_packet"
    V0366_AGENTIC_OPERATION_RUN_PACKET = "v0366_agentic_operation_run_packet"
    V0365_POST_APPLY_VALIDATION_REPORT = "v0365_post_apply_validation_report"
    STRUCTURED_COMMAND_REQUEST = "structured_command_request"
    CLI_LIKE_ARGV = "cli_like_argv"
    MANUAL_OPERATOR_INPUT = "manual_operator_input"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class SandboxTestCommandStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    COMMAND_SPEC_CREATED = "command_spec_created"
    ALLOWLIST_CREATED = "allowlist_created"
    DENYLIST_CREATED = "denylist_created"
    INVOCATION_CONTRACT_CREATED = "invocation_contract_created"
    INVOCATION_VALIDATED = "invocation_validated"
    ELIGIBLE_FOR_FUTURE_SANDBOX_TEST_EXECUTION = "eligible_for_future_sandbox_test_execution"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATED = "future_gated"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class SandboxTestCommandReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    COMMAND_POLICY_CONTRACT_READY = "command_policy_contract_ready"
    STRUCTURED_COMMAND_SPEC_READY = "structured_command_spec_ready"
    ALLOWLIST_READY = "allowlist_ready"
    INVOCATION_CONTRACT_READY = "invocation_contract_ready"
    VALIDATION_REPORT_READY = "validation_report_ready"
    DESIGN_HANDOFF_READY_FOR_V0372 = "design_handoff_ready_for_v0372"
    DESIGN_HANDOFF_READY_FOR_V0373 = "design_handoff_ready_for_v0373"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class SandboxTestCommandDecisionKind(StrEnum):
    ALLOW_COMMAND_SPEC_METADATA = "allow_command_spec_metadata"
    ALLOW_ALLOWLIST_METADATA = "allow_allowlist_metadata"
    ALLOW_INVOCATION_CONTRACT_METADATA = "allow_invocation_contract_metadata"
    ALLOW_FUTURE_SANDBOX_TEST_EXECUTION_INPUT = "allow_future_sandbox_test_execution_input"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class SandboxTestCommandRiskKind(StrEnum):
    ARBITRARY_SHELL_RISK = "arbitrary_shell_risk"
    UNCONTROLLED_SUBPROCESS_RISK = "uncontrolled_subprocess_risk"
    COMMAND_INJECTION_RISK = "command_injection_risk"
    SHELL_METACHARACTER_RISK = "shell_metacharacter_risk"
    LIVE_WORKSPACE_CWD_RISK = "live_workspace_cwd_risk"
    OUTSIDE_SANDBOX_CWD_RISK = "outside_sandbox_cwd_risk"
    PACKAGE_SCRIPT_RISK = "package_script_risk"
    DEPENDENCY_INSTALL_RISK = "dependency_install_risk"
    NETWORK_ACCESS_RISK = "network_access_risk"
    UNBOUNDED_OUTPUT_RISK = "unbounded_output_risk"
    TIMEOUT_MISSING_RISK = "timeout_missing_risk"
    MISSING_ALLOWLIST_RISK = "missing_allowlist_risk"
    MALFORMED_COMMAND_SPEC_RISK = "malformed_command_spec_risk"
    UNSAFE_ARGUMENT_RISK = "unsafe_argument_risk"
    CREDENTIAL_EXPOSURE_RISK = "credential_exposure_risk"
    SECRET_EXPOSURE_RISK = "secret_exposure_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    AUTOMATIC_REPAIR_RISK = "automatic_repair_risk"
    MULTI_CYCLE_LOOP_RISK = "multi_cycle_loop_risk"
    UNKNOWN = "unknown"


class SandboxTestExecutableKind(StrEnum):
    PYTHON_EXECUTABLE = "python_executable"
    NODE_EXECUTABLE = "node_executable"
    NPM_EXECUTABLE = "npm_executable"
    SHELL_EXECUTABLE = "shell_executable"
    POWERSHELL_EXECUTABLE = "powershell_executable"
    CMD_EXECUTABLE = "cmd_executable"
    GIT_EXECUTABLE = "git_executable"
    PACKAGE_MANAGER_EXECUTABLE = "package_manager_executable"
    EXTERNAL_AGENT_EXECUTABLE = "external_agent_executable"
    UNKNOWN = "unknown"


class SandboxTestArgumentKind(StrEnum):
    MODULE_FLAG = "module_flag"
    MODULE_NAME = "module_name"
    TEST_PATH = "test_path"
    TEST_NODE_ID = "test_node_id"
    MARKER_EXPRESSION = "marker_expression"
    VERBOSITY_FLAG = "verbosity_flag"
    SAFE_PYTEST_FLAG = "safe_pytest_flag"
    OUTPUT_CONTROL_FLAG = "output_control_flag"
    UNSAFE_SHELL_FRAGMENT = "unsafe_shell_fragment"
    INSTALL_ARGUMENT = "install_argument"
    NETWORK_ARGUMENT = "network_argument"
    EXTERNAL_AGENT_ARGUMENT = "external_agent_argument"
    UNKNOWN = "unknown"


class SandboxTestCwdKind(StrEnum):
    SANDBOX_ROOT = "sandbox_root"
    SANDBOX_TESTS_DIR = "sandbox_tests_dir"
    SANDBOX_PACKAGE_ROOT = "sandbox_package_root"
    LIVE_WORKSPACE_ROOT = "live_workspace_root"
    REFERENCES_ROOT = "references_root"
    EXTERNAL_ROOT = "external_root"
    UNKNOWN = "unknown"


class SandboxTestTimeoutKind(StrEnum):
    DEFAULT_TIMEOUT = "default_timeout"
    EXPLICIT_TIMEOUT = "explicit_timeout"
    BOUNDED_TIMEOUT = "bounded_timeout"
    MISSING_TIMEOUT = "missing_timeout"
    UNBOUNDED_TIMEOUT = "unbounded_timeout"
    UNKNOWN = "unknown"


class SandboxTestResourceLimitKind(StrEnum):
    DEFAULT_LIMITS = "default_limits"
    EXPLICIT_LIMITS = "explicit_limits"
    MISSING_LIMITS = "missing_limits"
    EXCESSIVE_LIMITS = "excessive_limits"
    UNKNOWN = "unknown"


class SandboxTestOutputCaptureMode(StrEnum):
    NO_CAPTURE = "no_capture"
    BOUNDED_STDOUT_STDERR_FUTURE_GATED = "bounded_stdout_stderr_future_gated"
    BOUNDED_STRUCTURED_OUTPUT_FUTURE_GATED = "bounded_structured_output_future_gated"
    UNBOUNDED_CAPTURE_BLOCKED = "unbounded_capture_blocked"
    RAW_SECRET_OUTPUT_BLOCKED = "raw_secret_output_blocked"
    UNKNOWN = "unknown"


class SandboxTestEnvironmentMode(StrEnum):
    MINIMAL_SANDBOX_ENV = "minimal_sandbox_env"
    INHERITED_ENV_BLOCKED = "inherited_env_blocked"
    CREDENTIAL_ENV_BLOCKED = "credential_env_blocked"
    NETWORK_ENV_BLOCKED = "network_env_blocked"
    DEPENDENCY_INSTALL_ENV_BLOCKED = "dependency_install_env_blocked"
    UNKNOWN = "unknown"


class SandboxTestNetworkPosture(StrEnum):
    NETWORK_BLOCKED = "network_blocked"
    LOOPBACK_BLOCKED = "loopback_blocked"
    EXTERNAL_NETWORK_BLOCKED = "external_network_blocked"
    NETWORK_FUTURE_GATE_REQUIRED = "network_future_gate_required"
    UNKNOWN = "unknown"


class SandboxTestDependencyPosture(StrEnum):
    DEPENDENCY_INSTALL_BLOCKED = "dependency_install_blocked"
    DEPENDENCY_CHECK_METADATA_ONLY = "dependency_check_metadata_only"
    DEPENDENCY_INSTALL_FUTURE_GATE_REQUIRED = "dependency_install_future_gate_required"
    MISSING_DEPENDENCY_DOES_NOT_ALLOW_INSTALL = "missing_dependency_does_not_allow_install"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class SandboxTestCommandFlagSet:
    flag_set_id: str
    version: str
    allowlisted_test_command_policy_constructed: bool
    structured_command_spec_available: bool
    test_command_allowlist_available: bool
    test_command_denylist_available: bool
    test_invocation_contract_available: bool
    sandbox_cwd_policy_available: bool
    timeout_policy_available: bool
    output_capture_contract_available: bool
    environment_contract_available: bool
    ready_for_v0372_sandbox_test_execution_engine: bool
    ready_for_v0373_test_result_envelope: bool
    ready_for_v0376_vera_codex_one_shot_agent_trial: bool
    ready_for_allowlisted_test_command_policy: bool
    ready_for_structured_test_command_spec: bool
    ready_for_test_invocation_contract: bool
    ready_for_sandbox_cwd_policy: bool
    ready_for_test_timeout_policy: bool
    ready_for_test_output_capture_contract: bool
    ready_for_future_sandbox_test_execution_input: bool
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
        for name in UNSAFE_COMMAND_FLAG_NAMES:
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestCommandSourceRef:
    source_ref_id: str
    source_kind: SandboxTestInvocationSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestAllowedExecutable:
    allowed_executable_id: str
    executable_kind: SandboxTestExecutableKind | str
    executable_name: str
    executable_summary: str
    allowed_for_future_execution: bool
    executable_now: bool
    shell: bool
    package_manager: bool
    external_agent: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("allowed_executable_id", self.allowed_executable_id)
        _require_non_blank("executable_name", self.executable_name)
        _require_non_blank("executable_summary", self.executable_summary)
        if _enum_value(self.executable_kind) in {
            SandboxTestExecutableKind.SHELL_EXECUTABLE.value,
            SandboxTestExecutableKind.POWERSHELL_EXECUTABLE.value,
            SandboxTestExecutableKind.CMD_EXECUTABLE.value,
            SandboxTestExecutableKind.NPM_EXECUTABLE.value,
            SandboxTestExecutableKind.PACKAGE_MANAGER_EXECUTABLE.value,
            SandboxTestExecutableKind.EXTERNAL_AGENT_EXECUTABLE.value,
        }:
            raise ValueError("allowed executable cannot be shell, package manager, or external agent")
        _validate_false("executable_now", self.executable_now)
        _validate_false("shell", self.shell)
        _validate_false("package_manager", self.package_manager)
        _validate_false("external_agent", self.external_agent)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestAllowedModule:
    allowed_module_id: str
    module_name: str
    module_summary: str
    allowed_for_future_execution: bool
    executable_now: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("allowed_module_id", self.allowed_module_id)
        _require_non_blank("module_name", self.module_name)
        _require_non_blank("module_summary", self.module_summary)
        _validate_false("executable_now", self.executable_now)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestArgumentSpec:
    argument_spec_id: str
    argument_kind: SandboxTestArgumentKind | str
    argument_name: str
    allowed_values: list[str]
    blocked_values: list[str]
    allowed_patterns: list[str]
    blocked_patterns: list[str]
    required: bool
    max_chars: int
    description: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("argument_spec_id", self.argument_spec_id)
        _require_non_blank("argument_name", self.argument_name)
        _require_non_blank("description", self.description)
        _validate_string_list("allowed_values", self.allowed_values)
        _validate_string_list("blocked_values", self.blocked_values)
        _validate_string_list("allowed_patterns", self.allowed_patterns)
        _validate_string_list("blocked_patterns", self.blocked_patterns)
        _validate_non_negative("max_chars", self.max_chars)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestCommandSpec:
    command_spec_id: str
    version: str
    command_kind: SandboxTestCommandKind | str
    executable: SandboxTestAllowedExecutable
    module: SandboxTestAllowedModule | None
    argument_specs: list[SandboxTestArgumentSpec]
    cwd_kind: SandboxTestCwdKind | str
    timeout_kind: SandboxTestTimeoutKind | str
    output_capture_mode: SandboxTestOutputCaptureMode | str
    environment_mode: SandboxTestEnvironmentMode | str
    network_posture: SandboxTestNetworkPosture | str
    dependency_posture: SandboxTestDependencyPosture | str
    command_summary: str
    allowed_for_future_sandbox_execution: bool
    executable_now: bool
    shell_allowed: bool
    dependency_install_allowed: bool
    network_allowed: bool
    live_workspace_allowed: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("command_spec_id", self.command_spec_id)
        _validate_version(self.version)
        _require_non_blank("command_summary", self.command_summary)
        _validate_list("argument_specs", self.argument_specs)
        _validate_false("executable_now", self.executable_now)
        _validate_false("shell_allowed", self.shell_allowed)
        _validate_false("dependency_install_allowed", self.dependency_install_allowed)
        _validate_false("network_allowed", self.network_allowed)
        _validate_false("live_workspace_allowed", self.live_workspace_allowed)
        if _enum_value(self.cwd_kind) in {
            SandboxTestCwdKind.LIVE_WORKSPACE_ROOT.value,
            SandboxTestCwdKind.REFERENCES_ROOT.value,
            SandboxTestCwdKind.EXTERNAL_ROOT.value,
        }:
            raise ValueError("command spec cwd must not target live, reference, or external roots")
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestCommandAllowlist:
    allowlist_id: str
    version: str
    allowed_command_specs: list[SandboxTestCommandSpec]
    allowed_executables: list[SandboxTestAllowedExecutable]
    allowed_modules: list[SandboxTestAllowedModule]
    allowlist_summary: str
    future_execution_only: bool
    executable_now: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("allowlist_id", self.allowlist_id)
        _validate_version(self.version)
        _require_non_blank("allowlist_summary", self.allowlist_summary)
        _validate_list("allowed_command_specs", self.allowed_command_specs)
        _validate_list("allowed_executables", self.allowed_executables)
        _validate_list("allowed_modules", self.allowed_modules)
        _validate_true("future_execution_only", self.future_execution_only)
        _validate_false("executable_now", self.executable_now)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestCommandDenylist:
    denylist_id: str
    version: str
    blocked_command_kinds: list[SandboxTestCommandKind | str]
    blocked_executable_kinds: list[SandboxTestExecutableKind | str]
    blocked_argument_patterns: list[str]
    blocked_command_names: list[str]
    blocked_reason_summary: str
    blocks_shell: bool
    blocks_install: bool
    blocks_network: bool
    blocks_external_agent: bool
    blocks_dominion: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("denylist_id", self.denylist_id)
        _validate_version(self.version)
        _require_non_blank("blocked_reason_summary", self.blocked_reason_summary)
        _validate_list("blocked_command_kinds", self.blocked_command_kinds)
        _validate_list("blocked_executable_kinds", self.blocked_executable_kinds)
        _validate_string_list("blocked_argument_patterns", self.blocked_argument_patterns)
        _validate_string_list("blocked_command_names", self.blocked_command_names)
        _validate_true("blocks_shell", self.blocks_shell)
        _validate_true("blocks_install", self.blocks_install)
        _validate_true("blocks_network", self.blocks_network)
        _validate_true("blocks_external_agent", self.blocks_external_agent)
        _validate_true("blocks_dominion", self.blocks_dominion)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestSandboxCwdPolicy:
    cwd_policy_id: str
    version: str
    allowed_cwd_kinds: list[SandboxTestCwdKind | str]
    blocked_cwd_kinds: list[SandboxTestCwdKind | str]
    require_sandbox_root: bool
    require_no_live_workspace_cwd: bool
    require_no_reference_cwd: bool
    require_no_external_cwd: bool
    allow_cwd_validation_future_gate: bool
    allow_live_workspace_cwd: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("cwd_policy_id", self.cwd_policy_id)
        _validate_version(self.version)
        _require_non_blank("summary", self.summary)
        _validate_list("allowed_cwd_kinds", self.allowed_cwd_kinds)
        _validate_list("blocked_cwd_kinds", self.blocked_cwd_kinds)
        _validate_true("require_sandbox_root", self.require_sandbox_root)
        _validate_true("require_no_live_workspace_cwd", self.require_no_live_workspace_cwd)
        _validate_true("require_no_reference_cwd", self.require_no_reference_cwd)
        _validate_true("require_no_external_cwd", self.require_no_external_cwd)
        _validate_false("allow_live_workspace_cwd", self.allow_live_workspace_cwd)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestTimeoutPolicy:
    timeout_policy_id: str
    version: str
    timeout_kind: SandboxTestTimeoutKind | str
    default_timeout_seconds: int
    max_timeout_seconds: int
    require_timeout: bool
    allow_unbounded_timeout: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("timeout_policy_id", self.timeout_policy_id)
        _validate_version(self.version)
        _require_non_blank("summary", self.summary)
        _validate_non_negative("default_timeout_seconds", self.default_timeout_seconds)
        _validate_non_negative("max_timeout_seconds", self.max_timeout_seconds)
        _validate_true("require_timeout", self.require_timeout)
        _validate_false("allow_unbounded_timeout", self.allow_unbounded_timeout)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestResourceLimitPolicy:
    resource_policy_id: str
    version: str
    resource_limit_kind: SandboxTestResourceLimitKind | str
    max_process_count: int
    max_output_chars: int
    max_runtime_seconds: int
    require_resource_limits: bool
    allow_unbounded_resources: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("resource_policy_id", self.resource_policy_id)
        _validate_version(self.version)
        _require_non_blank("summary", self.summary)
        _validate_non_negative("max_process_count", self.max_process_count)
        _validate_non_negative("max_output_chars", self.max_output_chars)
        _validate_non_negative("max_runtime_seconds", self.max_runtime_seconds)
        _validate_true("require_resource_limits", self.require_resource_limits)
        _validate_false("allow_unbounded_resources", self.allow_unbounded_resources)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestOutputCaptureContract:
    output_contract_id: str
    version: str
    capture_mode: SandboxTestOutputCaptureMode | str
    max_stdout_chars: int
    max_stderr_chars: int
    max_total_output_chars: int
    redact_secrets: bool
    block_raw_secret_output: bool
    allow_output_capture_future_gate: bool
    allow_output_capture_now: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("output_contract_id", self.output_contract_id)
        _validate_version(self.version)
        _require_non_blank("summary", self.summary)
        _validate_non_negative("max_stdout_chars", self.max_stdout_chars)
        _validate_non_negative("max_stderr_chars", self.max_stderr_chars)
        _validate_non_negative("max_total_output_chars", self.max_total_output_chars)
        _validate_true("redact_secrets", self.redact_secrets)
        _validate_true("block_raw_secret_output", self.block_raw_secret_output)
        _validate_false("allow_output_capture_now", self.allow_output_capture_now)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestEnvironmentContract:
    environment_contract_id: str
    version: str
    environment_mode: SandboxTestEnvironmentMode | str
    allowed_env_keys: list[str]
    blocked_env_key_patterns: list[str]
    require_minimal_env: bool
    block_inherited_env: bool
    block_credential_env: bool
    block_network_env: bool
    allow_env_future_gate: bool
    allow_env_now: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("environment_contract_id", self.environment_contract_id)
        _validate_version(self.version)
        _require_non_blank("summary", self.summary)
        _validate_string_list("allowed_env_keys", self.allowed_env_keys)
        _validate_string_list("blocked_env_key_patterns", self.blocked_env_key_patterns)
        _validate_true("require_minimal_env", self.require_minimal_env)
        _validate_true("block_inherited_env", self.block_inherited_env)
        _validate_true("block_credential_env", self.block_credential_env)
        _validate_true("block_network_env", self.block_network_env)
        _validate_false("allow_env_now", self.allow_env_now)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestInvocationContract:
    invocation_contract_id: str
    version: str
    command_spec: SandboxTestCommandSpec
    allowlist_id: str | None
    denylist_id: str | None
    cwd_policy: SandboxTestSandboxCwdPolicy
    timeout_policy: SandboxTestTimeoutPolicy
    resource_policy: SandboxTestResourceLimitPolicy
    output_contract: SandboxTestOutputCaptureContract
    environment_contract: SandboxTestEnvironmentContract
    required_future_evidence_refs: list[str]
    do_nothing_baseline_required_for_future_evaluation: bool
    eligible_for_future_sandbox_test_execution: bool
    executable_now: bool
    test_execution_allowed: bool
    subprocess_allowed: bool
    shell_allowed: bool
    dependency_install_allowed: bool
    network_allowed: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("invocation_contract_id", self.invocation_contract_id)
        _validate_version(self.version)
        _require_non_blank("summary", self.summary)
        _validate_string_list("required_future_evidence_refs", self.required_future_evidence_refs)
        _validate_true("do_nothing_baseline_required_for_future_evaluation", self.do_nothing_baseline_required_for_future_evaluation)
        _validate_false("executable_now", self.executable_now)
        _validate_false("test_execution_allowed", self.test_execution_allowed)
        _validate_false("subprocess_allowed", self.subprocess_allowed)
        _validate_false("shell_allowed", self.shell_allowed)
        _validate_false("dependency_install_allowed", self.dependency_install_allowed)
        _validate_false("network_allowed", self.network_allowed)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestInvocationRequest:
    invocation_request_id: str
    version: str
    requested_command_kind: SandboxTestCommandKind | str
    requested_executable_name: str
    requested_module_name: str | None
    requested_args: list[str]
    requested_cwd_kind: SandboxTestCwdKind | str
    requested_timeout_seconds: int | None
    source_refs: list[SandboxTestCommandSourceRef]
    request_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("invocation_request_id", self.invocation_request_id)
        _validate_version(self.version)
        _require_non_blank("requested_executable_name", self.requested_executable_name)
        _require_non_blank("request_summary", self.request_summary)
        _validate_string_list("requested_args", self.requested_args)
        _validate_list("source_refs", self.source_refs)
        _validate_non_negative("requested_timeout_seconds", self.requested_timeout_seconds)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestInvocationDecision:
    invocation_decision_id: str
    invocation_request_id: str
    decision_kind: SandboxTestCommandDecisionKind | str
    command_status: SandboxTestCommandStatus | str
    risk_kinds: list[SandboxTestCommandRiskKind | str]
    decision_summary: str
    eligible_for_future_sandbox_test_execution: bool
    executable_now: bool
    test_execution_allowed: bool
    controlled_subprocess_allowed: bool
    shell_allowed: bool
    dependency_install_allowed: bool
    network_allowed: bool
    live_workspace_allowed: bool
    external_agent_allowed: bool
    dominion_runtime_allowed: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("invocation_decision_id", self.invocation_decision_id)
        _require_non_blank("invocation_request_id", self.invocation_request_id)
        _require_non_blank("decision_summary", self.decision_summary)
        _validate_list("risk_kinds", self.risk_kinds)
        _validate_string_list("evidence_refs", self.evidence_refs)
        for name in UNSAFE_DECISION_NAMES:
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestDeniedCommand:
    denied_command_id: str
    invocation_request_id: str | None
    decision_id: str | None
    command_kind: SandboxTestCommandKind | str
    risk_kinds: list[SandboxTestCommandRiskKind | str]
    reason: str
    safe_alternatives: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("denied_command_id", self.denied_command_id)
        _require_non_blank("reason", self.reason)
        _validate_list("risk_kinds", self.risk_kinds)
        _validate_string_list("safe_alternatives", self.safe_alternatives)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestInvocationValidationFinding:
    finding_id: str
    risk_kind: SandboxTestCommandRiskKind | str
    severity: str
    message: str
    blocks_future_execution_eligibility: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("severity", self.severity)
        _require_non_blank("message", self.message)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestInvocationValidationReport:
    validation_report_id: str
    version: str
    invocation_request_id: str
    findings: list[SandboxTestInvocationValidationFinding]
    decision: SandboxTestInvocationDecision
    eligible_for_future_sandbox_test_execution: bool
    certifies_test_execution: bool
    summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version(self.version)
        _require_non_blank("invocation_request_id", self.invocation_request_id)
        _require_non_blank("summary", self.summary)
        _validate_list("findings", self.findings)
        _validate_false("certifies_test_execution", self.certifies_test_execution)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestCommandPolicyReport:
    policy_report_id: str
    version: str
    allowlist_id: str
    denylist_id: str
    policy_ready: bool
    allowlist_ready: bool
    denylist_ready: bool
    ready_for_future_sandbox_test_execution_input: bool
    ready_for_test_execution: bool
    summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_report_id", self.policy_report_id)
        _validate_version(self.version)
        _require_non_blank("allowlist_id", self.allowlist_id)
        _require_non_blank("denylist_id", self.denylist_id)
        _require_non_blank("summary", self.summary)
        _validate_false("ready_for_test_execution", self.ready_for_test_execution)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestInvocationRunPreview:
    run_preview_id: str
    version: str
    invocation_contract_id: str
    invocation_request_id: str
    future_eligible: bool
    executable_now: bool
    test_execution_allowed: bool
    controlled_subprocess_allowed: bool
    preview_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        _validate_version(self.version)
        _require_non_blank("invocation_contract_id", self.invocation_contract_id)
        _require_non_blank("invocation_request_id", self.invocation_request_id)
        _require_non_blank("preview_summary", self.preview_summary)
        _validate_false("executable_now", self.executable_now)
        _validate_false("test_execution_allowed", self.test_execution_allowed)
        _validate_false("controlled_subprocess_allowed", self.controlled_subprocess_allowed)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxTestCommandNoExecutionGuarantee:
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
    no_live_code_edit: bool
    no_patch_application: bool
    no_automatic_repair: bool
    no_multi_cycle_loop: bool
    no_vera_codex_trial_execution: bool
    no_cold_performance_evaluation_execution: bool
    no_model_provider_invocation: bool
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
class V0371ReadinessReport:
    readiness_report_id: str
    version: str
    readiness_level: SandboxTestCommandReadinessLevel | str
    status: SandboxTestCommandStatus | str
    summary: str
    ready_for_v0372_sandbox_test_execution_engine: bool
    ready_for_v0373_test_result_envelope: bool
    ready_for_v0376_vera_codex_one_shot_agent_trial: bool
    ready_for_allowlisted_test_command_policy: bool
    ready_for_structured_test_command_spec: bool
    ready_for_test_invocation_contract: bool
    ready_for_sandbox_cwd_policy: bool
    ready_for_test_timeout_policy: bool
    ready_for_test_output_capture_contract: bool
    ready_for_future_sandbox_test_execution_input: bool
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
        ):
            _validate_false(name, getattr(self, name))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


def build_sandbox_test_command_flags(**kwargs: Any) -> SandboxTestCommandFlagSet:
    return SandboxTestCommandFlagSet(
        flag_set_id=kwargs.pop("flag_set_id", "sandbox_test_command_flags:v0.37.1"),
        version=kwargs.pop("version", V0371_VERSION),
        allowlisted_test_command_policy_constructed=kwargs.pop("allowlisted_test_command_policy_constructed", True),
        structured_command_spec_available=kwargs.pop("structured_command_spec_available", True),
        test_command_allowlist_available=kwargs.pop("test_command_allowlist_available", True),
        test_command_denylist_available=kwargs.pop("test_command_denylist_available", True),
        test_invocation_contract_available=kwargs.pop("test_invocation_contract_available", True),
        sandbox_cwd_policy_available=kwargs.pop("sandbox_cwd_policy_available", True),
        timeout_policy_available=kwargs.pop("timeout_policy_available", True),
        output_capture_contract_available=kwargs.pop("output_capture_contract_available", True),
        environment_contract_available=kwargs.pop("environment_contract_available", True),
        ready_for_v0372_sandbox_test_execution_engine=kwargs.pop("ready_for_v0372_sandbox_test_execution_engine", True),
        ready_for_v0373_test_result_envelope=kwargs.pop("ready_for_v0373_test_result_envelope", True),
        ready_for_v0376_vera_codex_one_shot_agent_trial=kwargs.pop("ready_for_v0376_vera_codex_one_shot_agent_trial", True),
        ready_for_allowlisted_test_command_policy=kwargs.pop("ready_for_allowlisted_test_command_policy", True),
        ready_for_structured_test_command_spec=kwargs.pop("ready_for_structured_test_command_spec", True),
        ready_for_test_invocation_contract=kwargs.pop("ready_for_test_invocation_contract", True),
        ready_for_sandbox_cwd_policy=kwargs.pop("ready_for_sandbox_cwd_policy", True),
        ready_for_test_timeout_policy=kwargs.pop("ready_for_test_timeout_policy", True),
        ready_for_test_output_capture_contract=kwargs.pop("ready_for_test_output_capture_contract", True),
        ready_for_future_sandbox_test_execution_input=kwargs.pop("ready_for_future_sandbox_test_execution_input", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_COMMAND_FLAG_NAMES},
    )


def build_sandbox_test_command_source_ref(**kwargs: Any) -> SandboxTestCommandSourceRef:
    return SandboxTestCommandSourceRef(
        source_ref_id=kwargs.pop("source_ref_id", "sandbox_test_command_source_ref:v0.37.1"),
        source_kind=kwargs.pop("source_kind", SandboxTestInvocationSourceKind.V0370_SANDBOX_TEST_RUNNER_BOUNDARY),
        source_id=kwargs.pop("source_id", "v0.37.0"),
        source_summary=kwargs.pop("source_summary", "v0.37.0 boundary handoff metadata"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.0 boundary"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_allowed_executable(**kwargs: Any) -> SandboxTestAllowedExecutable:
    return SandboxTestAllowedExecutable(
        allowed_executable_id=kwargs.pop("allowed_executable_id", "allowed_python_executable:v0.37.1"),
        executable_kind=kwargs.pop("executable_kind", SandboxTestExecutableKind.PYTHON_EXECUTABLE),
        executable_name=kwargs.pop("executable_name", "python"),
        executable_summary=kwargs.pop("executable_summary", "python executable metadata for future sandbox tests"),
        allowed_for_future_execution=kwargs.pop("allowed_for_future_execution", True),
        executable_now=kwargs.pop("executable_now", False),
        shell=kwargs.pop("shell", False),
        package_manager=kwargs.pop("package_manager", False),
        external_agent=kwargs.pop("external_agent", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_allowed_module(**kwargs: Any) -> SandboxTestAllowedModule:
    return SandboxTestAllowedModule(
        allowed_module_id=kwargs.pop("allowed_module_id", "allowed_pytest_module:v0.37.1"),
        module_name=kwargs.pop("module_name", "pytest"),
        module_summary=kwargs.pop("module_summary", "pytest module metadata for future sandbox tests"),
        allowed_for_future_execution=kwargs.pop("allowed_for_future_execution", True),
        executable_now=kwargs.pop("executable_now", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_argument_spec(**kwargs: Any) -> SandboxTestArgumentSpec:
    return SandboxTestArgumentSpec(
        argument_spec_id=kwargs.pop("argument_spec_id", "sandbox_test_argument_spec:v0.37.1"),
        argument_kind=kwargs.pop("argument_kind", SandboxTestArgumentKind.TEST_PATH),
        argument_name=kwargs.pop("argument_name", "test_path"),
        allowed_values=kwargs.pop("allowed_values", []),
        blocked_values=kwargs.pop("blocked_values", list(BLOCKED_COMMAND_NAMES)),
        allowed_patterns=kwargs.pop("allowed_patterns", ["tests/"]),
        blocked_patterns=kwargs.pop("blocked_patterns", list(BLOCKED_ARGUMENT_PATTERNS)),
        required=kwargs.pop("required", False),
        max_chars=kwargs.pop("max_chars", 240),
        description=kwargs.pop("description", "metadata-only argument rule for future sandbox test input"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_command_spec(**kwargs: Any) -> SandboxTestCommandSpec:
    return SandboxTestCommandSpec(
        command_spec_id=kwargs.pop("command_spec_id", "sandbox_test_command_spec:pytest_module:v0.37.1"),
        version=kwargs.pop("version", V0371_VERSION),
        command_kind=kwargs.pop("command_kind", SandboxTestCommandKind.PYTHON_PYTEST_MODULE),
        executable=kwargs.pop("executable", build_sandbox_test_allowed_executable()),
        module=kwargs.pop("module", build_sandbox_test_allowed_module()),
        argument_specs=kwargs.pop("argument_specs", [build_sandbox_test_argument_spec()]),
        cwd_kind=kwargs.pop("cwd_kind", SandboxTestCwdKind.SANDBOX_ROOT),
        timeout_kind=kwargs.pop("timeout_kind", SandboxTestTimeoutKind.BOUNDED_TIMEOUT),
        output_capture_mode=kwargs.pop("output_capture_mode", SandboxTestOutputCaptureMode.BOUNDED_STDOUT_STDERR_FUTURE_GATED),
        environment_mode=kwargs.pop("environment_mode", SandboxTestEnvironmentMode.MINIMAL_SANDBOX_ENV),
        network_posture=kwargs.pop("network_posture", SandboxTestNetworkPosture.NETWORK_BLOCKED),
        dependency_posture=kwargs.pop("dependency_posture", SandboxTestDependencyPosture.MISSING_DEPENDENCY_DOES_NOT_ALLOW_INSTALL),
        command_summary=kwargs.pop("command_summary", "structured pytest module metadata for future sandbox execution"),
        allowed_for_future_sandbox_execution=kwargs.pop("allowed_for_future_sandbox_execution", True),
        executable_now=kwargs.pop("executable_now", False),
        shell_allowed=kwargs.pop("shell_allowed", False),
        dependency_install_allowed=kwargs.pop("dependency_install_allowed", False),
        network_allowed=kwargs.pop("network_allowed", False),
        live_workspace_allowed=kwargs.pop("live_workspace_allowed", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_command_allowlist(**kwargs: Any) -> SandboxTestCommandAllowlist:
    spec = kwargs.pop("command_spec", build_sandbox_test_command_spec())
    return SandboxTestCommandAllowlist(
        allowlist_id=kwargs.pop("allowlist_id", "sandbox_test_command_allowlist:v0.37.1"),
        version=kwargs.pop("version", V0371_VERSION),
        allowed_command_specs=kwargs.pop("allowed_command_specs", [spec]),
        allowed_executables=kwargs.pop("allowed_executables", [spec.executable]),
        allowed_modules=kwargs.pop("allowed_modules", [spec.module] if spec.module is not None else []),
        allowlist_summary=kwargs.pop("allowlist_summary", "future-execution-only test command allowlist metadata"),
        future_execution_only=kwargs.pop("future_execution_only", True),
        executable_now=kwargs.pop("executable_now", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_command_denylist(**kwargs: Any) -> SandboxTestCommandDenylist:
    return SandboxTestCommandDenylist(
        denylist_id=kwargs.pop("denylist_id", "sandbox_test_command_denylist:v0.37.1"),
        version=kwargs.pop("version", V0371_VERSION),
        blocked_command_kinds=kwargs.pop("blocked_command_kinds", [
            SandboxTestCommandKind.BLOCKED_SHELL_COMMAND,
            SandboxTestCommandKind.BLOCKED_PACKAGE_SCRIPT,
            SandboxTestCommandKind.BLOCKED_DEPENDENCY_INSTALL,
            SandboxTestCommandKind.BLOCKED_NETWORK_COMMAND,
            SandboxTestCommandKind.BLOCKED_EXTERNAL_AGENT_COMMAND,
            SandboxTestCommandKind.BLOCKED_DOMINION_COMMAND,
            SandboxTestCommandKind.BLOCKED_REPAIR_COMMAND,
            SandboxTestCommandKind.BLOCKED_MULTI_CYCLE_COMMAND,
            SandboxTestCommandKind.UNKNOWN,
        ]),
        blocked_executable_kinds=kwargs.pop("blocked_executable_kinds", [
            SandboxTestExecutableKind.NODE_EXECUTABLE,
            SandboxTestExecutableKind.NPM_EXECUTABLE,
            SandboxTestExecutableKind.SHELL_EXECUTABLE,
            SandboxTestExecutableKind.POWERSHELL_EXECUTABLE,
            SandboxTestExecutableKind.CMD_EXECUTABLE,
            SandboxTestExecutableKind.GIT_EXECUTABLE,
            SandboxTestExecutableKind.PACKAGE_MANAGER_EXECUTABLE,
            SandboxTestExecutableKind.EXTERNAL_AGENT_EXECUTABLE,
            SandboxTestExecutableKind.UNKNOWN,
        ]),
        blocked_argument_patterns=kwargs.pop("blocked_argument_patterns", list(BLOCKED_ARGUMENT_PATTERNS)),
        blocked_command_names=kwargs.pop("blocked_command_names", list(BLOCKED_COMMAND_NAMES)),
        blocked_reason_summary=kwargs.pop("blocked_reason_summary", "blocks shell, install, network, external-agent, Dominion, repair, and loop commands"),
        blocks_shell=kwargs.pop("blocks_shell", True),
        blocks_install=kwargs.pop("blocks_install", True),
        blocks_network=kwargs.pop("blocks_network", True),
        blocks_external_agent=kwargs.pop("blocks_external_agent", True),
        blocks_dominion=kwargs.pop("blocks_dominion", True),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_sandbox_cwd_policy(**kwargs: Any) -> SandboxTestSandboxCwdPolicy:
    return SandboxTestSandboxCwdPolicy(
        cwd_policy_id=kwargs.pop("cwd_policy_id", "sandbox_test_cwd_policy:v0.37.1"),
        version=kwargs.pop("version", V0371_VERSION),
        allowed_cwd_kinds=kwargs.pop("allowed_cwd_kinds", [SandboxTestCwdKind.SANDBOX_ROOT, SandboxTestCwdKind.SANDBOX_TESTS_DIR, SandboxTestCwdKind.SANDBOX_PACKAGE_ROOT]),
        blocked_cwd_kinds=kwargs.pop("blocked_cwd_kinds", [SandboxTestCwdKind.LIVE_WORKSPACE_ROOT, SandboxTestCwdKind.REFERENCES_ROOT, SandboxTestCwdKind.EXTERNAL_ROOT, SandboxTestCwdKind.UNKNOWN]),
        require_sandbox_root=kwargs.pop("require_sandbox_root", True),
        require_no_live_workspace_cwd=kwargs.pop("require_no_live_workspace_cwd", True),
        require_no_reference_cwd=kwargs.pop("require_no_reference_cwd", True),
        require_no_external_cwd=kwargs.pop("require_no_external_cwd", True),
        allow_cwd_validation_future_gate=kwargs.pop("allow_cwd_validation_future_gate", True),
        allow_live_workspace_cwd=kwargs.pop("allow_live_workspace_cwd", False),
        summary=kwargs.pop("summary", "future test cwd must be sandbox-scoped"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_timeout_policy(**kwargs: Any) -> SandboxTestTimeoutPolicy:
    return SandboxTestTimeoutPolicy(
        timeout_policy_id=kwargs.pop("timeout_policy_id", "sandbox_test_timeout_policy:v0.37.1"),
        version=kwargs.pop("version", V0371_VERSION),
        timeout_kind=kwargs.pop("timeout_kind", SandboxTestTimeoutKind.BOUNDED_TIMEOUT),
        default_timeout_seconds=kwargs.pop("default_timeout_seconds", 60),
        max_timeout_seconds=kwargs.pop("max_timeout_seconds", 300),
        require_timeout=kwargs.pop("require_timeout", True),
        allow_unbounded_timeout=kwargs.pop("allow_unbounded_timeout", False),
        summary=kwargs.pop("summary", "future test input requires bounded timeout metadata"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_resource_limit_policy(**kwargs: Any) -> SandboxTestResourceLimitPolicy:
    return SandboxTestResourceLimitPolicy(
        resource_policy_id=kwargs.pop("resource_policy_id", "sandbox_test_resource_policy:v0.37.1"),
        version=kwargs.pop("version", V0371_VERSION),
        resource_limit_kind=kwargs.pop("resource_limit_kind", SandboxTestResourceLimitKind.DEFAULT_LIMITS),
        max_process_count=kwargs.pop("max_process_count", 1),
        max_output_chars=kwargs.pop("max_output_chars", 20000),
        max_runtime_seconds=kwargs.pop("max_runtime_seconds", 300),
        require_resource_limits=kwargs.pop("require_resource_limits", True),
        allow_unbounded_resources=kwargs.pop("allow_unbounded_resources", False),
        summary=kwargs.pop("summary", "future test input requires bounded resource metadata"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_output_capture_contract(**kwargs: Any) -> SandboxTestOutputCaptureContract:
    return SandboxTestOutputCaptureContract(
        output_contract_id=kwargs.pop("output_contract_id", "sandbox_test_output_contract:v0.37.1"),
        version=kwargs.pop("version", V0371_VERSION),
        capture_mode=kwargs.pop("capture_mode", SandboxTestOutputCaptureMode.BOUNDED_STDOUT_STDERR_FUTURE_GATED),
        max_stdout_chars=kwargs.pop("max_stdout_chars", 10000),
        max_stderr_chars=kwargs.pop("max_stderr_chars", 10000),
        max_total_output_chars=kwargs.pop("max_total_output_chars", 20000),
        redact_secrets=kwargs.pop("redact_secrets", True),
        block_raw_secret_output=kwargs.pop("block_raw_secret_output", True),
        allow_output_capture_future_gate=kwargs.pop("allow_output_capture_future_gate", True),
        allow_output_capture_now=kwargs.pop("allow_output_capture_now", False),
        summary=kwargs.pop("summary", "bounded output capture is future-gated metadata"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_environment_contract(**kwargs: Any) -> SandboxTestEnvironmentContract:
    return SandboxTestEnvironmentContract(
        environment_contract_id=kwargs.pop("environment_contract_id", "sandbox_test_environment_contract:v0.37.1"),
        version=kwargs.pop("version", V0371_VERSION),
        environment_mode=kwargs.pop("environment_mode", SandboxTestEnvironmentMode.MINIMAL_SANDBOX_ENV),
        allowed_env_keys=kwargs.pop("allowed_env_keys", ["PYTHONPATH"]),
        blocked_env_key_patterns=kwargs.pop("blocked_env_key_patterns", ["TOKEN", "SECRET", "KEY", "PASSWORD", "CREDENTIAL"]),
        require_minimal_env=kwargs.pop("require_minimal_env", True),
        block_inherited_env=kwargs.pop("block_inherited_env", True),
        block_credential_env=kwargs.pop("block_credential_env", True),
        block_network_env=kwargs.pop("block_network_env", True),
        allow_env_future_gate=kwargs.pop("allow_env_future_gate", True),
        allow_env_now=kwargs.pop("allow_env_now", False),
        summary=kwargs.pop("summary", "future test input requires minimal sandbox environment metadata"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_invocation_contract(**kwargs: Any) -> SandboxTestInvocationContract:
    return SandboxTestInvocationContract(
        invocation_contract_id=kwargs.pop("invocation_contract_id", "sandbox_test_invocation_contract:v0.37.1"),
        version=kwargs.pop("version", V0371_VERSION),
        command_spec=kwargs.pop("command_spec", build_sandbox_test_command_spec()),
        allowlist_id=kwargs.pop("allowlist_id", "sandbox_test_command_allowlist:v0.37.1"),
        denylist_id=kwargs.pop("denylist_id", "sandbox_test_command_denylist:v0.37.1"),
        cwd_policy=kwargs.pop("cwd_policy", build_sandbox_test_sandbox_cwd_policy()),
        timeout_policy=kwargs.pop("timeout_policy", build_sandbox_test_timeout_policy()),
        resource_policy=kwargs.pop("resource_policy", build_sandbox_test_resource_limit_policy()),
        output_contract=kwargs.pop("output_contract", build_sandbox_test_output_capture_contract()),
        environment_contract=kwargs.pop("environment_contract", build_sandbox_test_environment_contract()),
        required_future_evidence_refs=kwargs.pop("required_future_evidence_refs", ["sandbox validation report", "future test result envelope", "do-nothing baseline"]),
        do_nothing_baseline_required_for_future_evaluation=kwargs.pop("do_nothing_baseline_required_for_future_evaluation", True),
        eligible_for_future_sandbox_test_execution=kwargs.pop("eligible_for_future_sandbox_test_execution", True),
        executable_now=kwargs.pop("executable_now", False),
        test_execution_allowed=kwargs.pop("test_execution_allowed", False),
        subprocess_allowed=kwargs.pop("subprocess_allowed", False),
        shell_allowed=kwargs.pop("shell_allowed", False),
        dependency_install_allowed=kwargs.pop("dependency_install_allowed", False),
        network_allowed=kwargs.pop("network_allowed", False),
        summary=kwargs.pop("summary", "future-eligible invocation contract; no execution in v0.37.1"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_invocation_request(**kwargs: Any) -> SandboxTestInvocationRequest:
    return SandboxTestInvocationRequest(
        invocation_request_id=kwargs.pop("invocation_request_id", "sandbox_test_invocation_request:v0.37.1"),
        version=kwargs.pop("version", V0371_VERSION),
        requested_command_kind=kwargs.pop("requested_command_kind", SandboxTestCommandKind.PYTHON_PYTEST_MODULE),
        requested_executable_name=kwargs.pop("requested_executable_name", "python"),
        requested_module_name=kwargs.pop("requested_module_name", "pytest"),
        requested_args=kwargs.pop("requested_args", ["-m", "pytest", "tests/test_example.py"]),
        requested_cwd_kind=kwargs.pop("requested_cwd_kind", SandboxTestCwdKind.SANDBOX_ROOT),
        requested_timeout_seconds=kwargs.pop("requested_timeout_seconds", 60),
        source_refs=kwargs.pop("source_refs", [build_sandbox_test_command_source_ref()]),
        request_summary=kwargs.pop("request_summary", "metadata-only future sandbox test invocation request"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_invocation_decision(**kwargs: Any) -> SandboxTestInvocationDecision:
    return SandboxTestInvocationDecision(
        invocation_decision_id=kwargs.pop("invocation_decision_id", "sandbox_test_invocation_decision:v0.37.1"),
        invocation_request_id=kwargs.pop("invocation_request_id", "sandbox_test_invocation_request:v0.37.1"),
        decision_kind=kwargs.pop("decision_kind", SandboxTestCommandDecisionKind.ALLOW_FUTURE_SANDBOX_TEST_EXECUTION_INPUT),
        command_status=kwargs.pop("command_status", SandboxTestCommandStatus.ELIGIBLE_FOR_FUTURE_SANDBOX_TEST_EXECUTION),
        risk_kinds=kwargs.pop("risk_kinds", []),
        decision_summary=kwargs.pop("decision_summary", "eligible as future sandbox test execution input only"),
        eligible_for_future_sandbox_test_execution=kwargs.pop("eligible_for_future_sandbox_test_execution", True),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.1 policy metadata"]),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_DECISION_NAMES},
    )


def build_sandbox_test_denied_command(**kwargs: Any) -> SandboxTestDeniedCommand:
    return SandboxTestDeniedCommand(
        denied_command_id=kwargs.pop("denied_command_id", "sandbox_test_denied_command:v0.37.1"),
        invocation_request_id=kwargs.pop("invocation_request_id", None),
        decision_id=kwargs.pop("decision_id", None),
        command_kind=kwargs.pop("command_kind", SandboxTestCommandKind.BLOCKED_SHELL_COMMAND),
        risk_kinds=kwargs.pop("risk_kinds", [SandboxTestCommandRiskKind.ARBITRARY_SHELL_RISK]),
        reason=kwargs.pop("reason", "unsafe command denied as safe outcome"),
        safe_alternatives=kwargs.pop("safe_alternatives", ["structured python module metadata", "future sandbox-only allowlist"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_invocation_validation_finding(**kwargs: Any) -> SandboxTestInvocationValidationFinding:
    return SandboxTestInvocationValidationFinding(
        finding_id=kwargs.pop("finding_id", "sandbox_test_invocation_finding:v0.37.1"),
        risk_kind=kwargs.pop("risk_kind", SandboxTestCommandRiskKind.UNKNOWN),
        severity=kwargs.pop("severity", "info"),
        message=kwargs.pop("message", "metadata validation finding"),
        blocks_future_execution_eligibility=kwargs.pop("blocks_future_execution_eligibility", False),
        evidence_refs=kwargs.pop("evidence_refs", []),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_invocation_validation_report(**kwargs: Any) -> SandboxTestInvocationValidationReport:
    request = kwargs.pop("request", build_sandbox_test_invocation_request())
    decision = kwargs.pop("decision", decide_sandbox_test_invocation_eligibility(request))
    return SandboxTestInvocationValidationReport(
        validation_report_id=kwargs.pop("validation_report_id", "sandbox_test_invocation_validation_report:v0.37.1"),
        version=kwargs.pop("version", V0371_VERSION),
        invocation_request_id=kwargs.pop("invocation_request_id", request.invocation_request_id),
        findings=kwargs.pop("findings", []),
        decision=decision,
        eligible_for_future_sandbox_test_execution=kwargs.pop("eligible_for_future_sandbox_test_execution", decision.eligible_for_future_sandbox_test_execution),
        certifies_test_execution=kwargs.pop("certifies_test_execution", False),
        summary=kwargs.pop("summary", "validation report is metadata only and does not certify execution"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.1 validation"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_command_policy_report(**kwargs: Any) -> SandboxTestCommandPolicyReport:
    allowlist = kwargs.pop("allowlist", default_sandbox_test_command_allowlist())
    denylist = kwargs.pop("denylist", default_sandbox_test_command_denylist())
    return SandboxTestCommandPolicyReport(
        policy_report_id=kwargs.pop("policy_report_id", "sandbox_test_command_policy_report:v0.37.1"),
        version=kwargs.pop("version", V0371_VERSION),
        allowlist_id=kwargs.pop("allowlist_id", allowlist.allowlist_id),
        denylist_id=kwargs.pop("denylist_id", denylist.denylist_id),
        policy_ready=kwargs.pop("policy_ready", True),
        allowlist_ready=kwargs.pop("allowlist_ready", True),
        denylist_ready=kwargs.pop("denylist_ready", True),
        ready_for_future_sandbox_test_execution_input=kwargs.pop("ready_for_future_sandbox_test_execution_input", True),
        ready_for_test_execution=kwargs.pop("ready_for_test_execution", False),
        summary=kwargs.pop("summary", "allowlist and denylist metadata ready; execution remains false"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.1 command policy"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_invocation_run_preview(**kwargs: Any) -> SandboxTestInvocationRunPreview:
    contract = kwargs.pop("contract", default_sandbox_test_invocation_contract())
    request = kwargs.pop("request", build_sandbox_test_invocation_request())
    return SandboxTestInvocationRunPreview(
        run_preview_id=kwargs.pop("run_preview_id", "sandbox_test_invocation_run_preview:v0.37.1"),
        version=kwargs.pop("version", V0371_VERSION),
        invocation_contract_id=kwargs.pop("invocation_contract_id", contract.invocation_contract_id),
        invocation_request_id=kwargs.pop("invocation_request_id", request.invocation_request_id),
        future_eligible=kwargs.pop("future_eligible", True),
        executable_now=kwargs.pop("executable_now", False),
        test_execution_allowed=kwargs.pop("test_execution_allowed", False),
        controlled_subprocess_allowed=kwargs.pop("controlled_subprocess_allowed", False),
        preview_summary=kwargs.pop("preview_summary", "future eligibility preview only; no run is performed"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.1 preview"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_command_no_execution_guarantee(**kwargs: Any) -> SandboxTestCommandNoExecutionGuarantee:
    no_names = tuple(name for name in SandboxTestCommandNoExecutionGuarantee.__dataclass_fields__ if name.startswith("no_"))
    return SandboxTestCommandNoExecutionGuarantee(
        guarantee_id=kwargs.pop("guarantee_id", "sandbox_test_command_no_execution_guarantee:v0.37.1"),
        version=kwargs.pop("version", V0371_VERSION),
        summary=kwargs.pop("summary", "v0.37.1 defines command policy metadata only and executes nothing"),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, True) for name in no_names},
    )


def build_v0371_readiness_report(**kwargs: Any) -> V0371ReadinessReport:
    return V0371ReadinessReport(
        readiness_report_id=kwargs.pop("readiness_report_id", "v0371_readiness_report"),
        version=kwargs.pop("version", V0371_VERSION),
        readiness_level=kwargs.pop("readiness_level", SandboxTestCommandReadinessLevel.DESIGN_HANDOFF_READY_FOR_V0372),
        status=kwargs.pop("status", SandboxTestCommandStatus.ELIGIBLE_FOR_FUTURE_SANDBOX_TEST_EXECUTION),
        summary=kwargs.pop("summary", "v0.37.1 policy and contract metadata ready; execution remains false"),
        ready_for_v0372_sandbox_test_execution_engine=kwargs.pop("ready_for_v0372_sandbox_test_execution_engine", True),
        ready_for_v0373_test_result_envelope=kwargs.pop("ready_for_v0373_test_result_envelope", True),
        ready_for_v0376_vera_codex_one_shot_agent_trial=kwargs.pop("ready_for_v0376_vera_codex_one_shot_agent_trial", True),
        ready_for_allowlisted_test_command_policy=kwargs.pop("ready_for_allowlisted_test_command_policy", True),
        ready_for_structured_test_command_spec=kwargs.pop("ready_for_structured_test_command_spec", True),
        ready_for_test_invocation_contract=kwargs.pop("ready_for_test_invocation_contract", True),
        ready_for_sandbox_cwd_policy=kwargs.pop("ready_for_sandbox_cwd_policy", True),
        ready_for_test_timeout_policy=kwargs.pop("ready_for_test_timeout_policy", True),
        ready_for_test_output_capture_contract=kwargs.pop("ready_for_test_output_capture_contract", True),
        ready_for_future_sandbox_test_execution_input=kwargs.pop("ready_for_future_sandbox_test_execution_input", True),
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
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.1 command policy"]),
        metadata=kwargs.pop("metadata", {}),
    )


def default_sandbox_test_command_denylist(**kwargs: Any) -> SandboxTestCommandDenylist:
    return build_sandbox_test_command_denylist(**kwargs)


def default_sandbox_test_command_allowlist(**kwargs: Any) -> SandboxTestCommandAllowlist:
    return build_sandbox_test_command_allowlist(**kwargs)


def default_sandbox_test_invocation_contract(**kwargs: Any) -> SandboxTestInvocationContract:
    return build_sandbox_test_invocation_contract(**kwargs)


def validate_sandbox_test_command_spec(spec: SandboxTestCommandSpec) -> SandboxTestInvocationValidationReport:
    findings: list[SandboxTestInvocationValidationFinding] = []
    if not isinstance(spec, SandboxTestCommandSpec):
        raise ValueError("spec must be SandboxTestCommandSpec")
    if not sandbox_test_command_spec_is_not_execution(spec):
        findings.append(build_sandbox_test_invocation_validation_finding(
            risk_kind=SandboxTestCommandRiskKind.MALFORMED_COMMAND_SPEC_RISK,
            severity="block",
            message="command spec attempted execution authority",
            blocks_future_execution_eligibility=True,
        ))
    request = build_sandbox_test_invocation_request(
        requested_command_kind=spec.command_kind,
        requested_executable_name=spec.executable.executable_name,
        requested_module_name=spec.module.module_name if spec.module else None,
        requested_cwd_kind=spec.cwd_kind,
    )
    decision = decide_sandbox_test_invocation_eligibility(request)
    return build_sandbox_test_invocation_validation_report(
        request=request,
        decision=decision,
        findings=findings,
        eligible_for_future_sandbox_test_execution=decision.eligible_for_future_sandbox_test_execution and not findings,
    )


def validate_sandbox_test_invocation_request(request: SandboxTestInvocationRequest) -> SandboxTestInvocationValidationReport:
    decision = decide_sandbox_test_invocation_eligibility(request)
    findings: list[SandboxTestInvocationValidationFinding] = []
    if decision.risk_kinds:
        for index, risk in enumerate(decision.risk_kinds):
            findings.append(build_sandbox_test_invocation_validation_finding(
                finding_id=f"sandbox_test_invocation_finding:{index}:v0.37.1",
                risk_kind=risk,
                severity="block",
                message=f"request blocked for {risk}",
                blocks_future_execution_eligibility=True,
            ))
    return build_sandbox_test_invocation_validation_report(
        request=request,
        decision=decision,
        findings=findings,
        eligible_for_future_sandbox_test_execution=decision.eligible_for_future_sandbox_test_execution,
    )


def decide_sandbox_test_invocation_eligibility(
    request: SandboxTestInvocationRequest,
    allowlist: SandboxTestCommandAllowlist | None = None,
    denylist: SandboxTestCommandDenylist | None = None,
) -> SandboxTestInvocationDecision:
    if not isinstance(request, SandboxTestInvocationRequest):
        raise ValueError("request must be SandboxTestInvocationRequest")
    denylist = denylist or default_sandbox_test_command_denylist()
    allowlist = allowlist or default_sandbox_test_command_allowlist()
    tokens = _tokens_for_request(request)
    joined = " ".join(tokens)
    risk_kinds: list[SandboxTestCommandRiskKind] = []
    blocked_names = {item.lower() for item in denylist.blocked_command_names}
    blocked_patterns = [item.lower() for item in denylist.blocked_argument_patterns]
    if _enum_value(request.requested_command_kind) in {item.value for item in denylist.blocked_command_kinds if isinstance(item, SandboxTestCommandKind)}:
        risk_kinds.append(SandboxTestCommandRiskKind.MALFORMED_COMMAND_SPEC_RISK)
    if any(token in blocked_names for token in tokens):
        risk_kinds.append(SandboxTestCommandRiskKind.COMMAND_INJECTION_RISK)
    if any(pattern in joined for pattern in blocked_patterns):
        risk_kinds.append(SandboxTestCommandRiskKind.UNSAFE_ARGUMENT_RISK)
    if request.requested_executable_name.lower() in {"npm", "pnpm", "yarn"}:
        risk_kinds.append(SandboxTestCommandRiskKind.PACKAGE_SCRIPT_RISK)
    if request.requested_executable_name.lower() in {"pip", "poetry"} or "install" in tokens:
        risk_kinds.append(SandboxTestCommandRiskKind.DEPENDENCY_INSTALL_RISK)
    if "http://" in joined or "https://" in joined or request.requested_executable_name.lower() in {"curl", "wget"}:
        risk_kinds.append(SandboxTestCommandRiskKind.NETWORK_ACCESS_RISK)
    if any(token in {"run-claude-code", "run-codex", "run-opencode", "run-hermes", "run-openclaw"} for token in tokens):
        risk_kinds.append(SandboxTestCommandRiskKind.EXTERNAL_AGENT_EXECUTION_RISK)
    if "dominion" in tokens:
        risk_kinds.append(SandboxTestCommandRiskKind.DOMINION_RUNTIME_RISK)
    if "auto-repair" in tokens or "repair-loop" in tokens:
        risk_kinds.append(SandboxTestCommandRiskKind.AUTOMATIC_REPAIR_RISK)
    if "multi-cycle" in tokens or "retry-loop" in tokens:
        risk_kinds.append(SandboxTestCommandRiskKind.MULTI_CYCLE_LOOP_RISK)
    if _enum_value(request.requested_cwd_kind) in {
        SandboxTestCwdKind.LIVE_WORKSPACE_ROOT.value,
        SandboxTestCwdKind.REFERENCES_ROOT.value,
        SandboxTestCwdKind.EXTERNAL_ROOT.value,
        SandboxTestCwdKind.UNKNOWN.value,
    }:
        risk_kinds.append(SandboxTestCommandRiskKind.OUTSIDE_SANDBOX_CWD_RISK)
    if request.requested_timeout_seconds is None:
        risk_kinds.append(SandboxTestCommandRiskKind.TIMEOUT_MISSING_RISK)
    if not allowlist.allowed_command_specs:
        risk_kinds.append(SandboxTestCommandRiskKind.MISSING_ALLOWLIST_RISK)
    unique_risks = list(dict.fromkeys(risk_kinds))
    blocked = bool(unique_risks)
    return build_sandbox_test_invocation_decision(
        invocation_request_id=request.invocation_request_id,
        decision_kind=SandboxTestCommandDecisionKind.BLOCK if blocked else SandboxTestCommandDecisionKind.ALLOW_FUTURE_SANDBOX_TEST_EXECUTION_INPUT,
        command_status=SandboxTestCommandStatus.BLOCKED if blocked else SandboxTestCommandStatus.ELIGIBLE_FOR_FUTURE_SANDBOX_TEST_EXECUTION,
        risk_kinds=unique_risks,
        decision_summary="request blocked as unsafe metadata" if blocked else "request eligible as future sandbox test input only",
        eligible_for_future_sandbox_test_execution=not blocked,
    )


def sandbox_test_command_flags_preserve_no_execution(flags: SandboxTestCommandFlagSet) -> bool:
    return isinstance(flags, SandboxTestCommandFlagSet) and all(getattr(flags, name) is False for name in UNSAFE_COMMAND_FLAG_NAMES)


def sandbox_test_command_spec_is_not_execution(spec: SandboxTestCommandSpec) -> bool:
    return (
        isinstance(spec, SandboxTestCommandSpec)
        and spec.executable_now is False
        and spec.shell_allowed is False
        and spec.dependency_install_allowed is False
        and spec.network_allowed is False
        and spec.live_workspace_allowed is False
    )


def sandbox_test_invocation_contract_is_not_execution(contract: SandboxTestInvocationContract) -> bool:
    return (
        isinstance(contract, SandboxTestInvocationContract)
        and contract.executable_now is False
        and contract.test_execution_allowed is False
        and contract.subprocess_allowed is False
        and contract.shell_allowed is False
        and contract.dependency_install_allowed is False
        and contract.network_allowed is False
        and contract.do_nothing_baseline_required_for_future_evaluation is True
    )


def sandbox_test_invocation_decision_is_not_execution(decision: SandboxTestInvocationDecision) -> bool:
    return isinstance(decision, SandboxTestInvocationDecision) and all(getattr(decision, name) is False for name in UNSAFE_DECISION_NAMES)


def sandbox_test_denylist_blocks_shell_install_network(denylist: SandboxTestCommandDenylist) -> bool:
    return (
        isinstance(denylist, SandboxTestCommandDenylist)
        and denylist.blocks_shell
        and denylist.blocks_install
        and denylist.blocks_network
        and denylist.blocks_external_agent
        and denylist.blocks_dominion
    )


def v0371_readiness_report_is_not_execution_ready(report: V0371ReadinessReport) -> bool:
    if not isinstance(report, V0371ReadinessReport):
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
