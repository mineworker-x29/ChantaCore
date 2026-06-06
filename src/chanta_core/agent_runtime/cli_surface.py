from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any
import json

from .boundary import (
    _metadata_flag_true,
    _require_non_blank,
    _validate_object_list,
    _validate_string_list,
)
from .ocel_trace import (
    RuntimeOCELTracePacket,
    build_runtime_ocel_packet_from_agent_step_output,
    build_runtime_ocel_packet_from_session_snapshot,
    default_runtime_ocel_trace_policy,
    runtime_ocel_packet_is_not_persistence,
)
from .session_runtime import AgentRuntimeSessionSnapshot
from .step_runner import (
    AgentStepOutput,
    build_agent_step_input,
    build_agent_step_runner_mvp,
    build_agent_supplied_model_output,
    run_agent_step_mvp,
)
from .workspace_inspection import (
    WorkspaceInspectionPathPolicy,
    WorkspaceInspectionRequestKind,
    WorkspaceInspectionResultKind,
    WorkspaceInspectionToolKind,
    WorkspaceInspectionToolResult,
    build_workspace_inspection_request,
    inspect_file_metadata_readonly,
    inspect_project_tree_readonly,
    inspect_workspace_path_readonly,
    read_text_file_safe,
    search_text_in_workspace_readonly,
    summarize_reference_inventory_readonly,
)


V0338_VERSION = "v0.33.8"
V0338_RELEASE_NAME = "v0.33.8 CLI Agent Run Surface"

MAX_CLI_ARG_CHARS = 20_000
MAX_RENDERED_OUTPUT_CHARS = 12_000

DEFAULT_CLI_PROHIBITED_ARG_PATTERNS = [
    ";",
    "|",
    "&&",
    "||",
    "`",
    "$(",
    ">",
    "<",
    "secret",
    "token",
    "credential",
    ".env",
    "id_rsa",
    ".pem",
]

DEFAULT_V0338_PROHIBITED_UNTIL_LATER_GATE = [
    "shell execution",
    "subprocess",
    "real model invocation",
    "provider invocation",
    "general agent execution",
    "general tool execution",
    "command execution",
    "network access",
    "credential access",
    "workspace write",
    "code edit",
    "patch application",
    "reference code execution",
    "reference import",
    "dependency install",
    "secret file read",
    "persistent trace write",
    "external trace sink",
    "registry mutation",
    "memory mutation",
    "UI runtime",
    "external control",
    "authority grant",
]


class CLIAgentCommandKind(StrEnum):
    AGENT_HELP = "agent_help"
    AGENT_STATUS = "agent_status"
    AGENT_PROFILE_PREVIEW = "agent_profile_preview"
    AGENT_PROMPT_PREVIEW = "agent_prompt_preview"
    AGENT_SESSION_PREVIEW = "agent_session_preview"
    AGENT_INSPECT_PATH_READONLY = "agent_inspect_path_readonly"
    AGENT_INSPECT_TREE_READONLY = "agent_inspect_tree_readonly"
    AGENT_READ_TEXT_FILE_SAFE = "agent_read_text_file_safe"
    AGENT_SEARCH_WORKSPACE_READONLY = "agent_search_workspace_readonly"
    AGENT_REFERENCE_SUMMARY_READONLY = "agent_reference_summary_readonly"
    AGENT_STEP_WITH_SUPPLIED_OUTPUT = "agent_step_with_supplied_output"
    AGENT_STEP_WITH_MOCK_OUTPUT = "agent_step_with_mock_output"
    AGENT_TRACE_PREVIEW_FROM_STEP_OUTPUT = "agent_trace_preview_from_step_output"
    AGENT_TRACE_PREVIEW_FROM_SESSION_SNAPSHOT = "agent_trace_preview_from_session_snapshot"
    AGENT_NO_OP = "agent_no_op"
    UNKNOWN = "unknown"


class CLIAgentCommandMode(StrEnum):
    HELP = "help"
    STATUS = "status"
    PREVIEW = "preview"
    READONLY_INSPECTION = "readonly_inspection"
    BOUNDED_STEP = "bounded_step"
    TRACE_PREVIEW = "trace_preview"
    NO_OP = "no_op"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class CLIAgentInputSourceKind(StrEnum):
    ARGV_LIST = "argv_list"
    PARSED_ARGS = "parsed_args"
    IN_MEMORY_ARTIFACT = "in_memory_artifact"
    SUPPLIED_MODEL_OUTPUT = "supplied_model_output"
    MOCK_MODEL_OUTPUT = "mock_model_output"
    WORKSPACE_PATH_REF = "workspace_path_ref"
    REFERENCE_PATH_REF = "reference_path_ref"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class CLIAgentSurfaceStatus(StrEnum):
    UNKNOWN = "unknown"
    INITIALIZED = "initialized"
    PARSED = "parsed"
    DECISION_READY = "decision_ready"
    ALLOWED = "allowed"
    DENIED = "denied"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    COMPLETED_WITH_SKIPS = "completed_with_skips"
    SAFE_FAILED = "safe_failed"
    NO_OP = "no_op"


class CLIAgentDecisionKind(StrEnum):
    ALLOW_HELP = "allow_help"
    ALLOW_STATUS = "allow_status"
    ALLOW_PREVIEW = "allow_preview"
    ALLOW_SAFE_WORKSPACE_INSPECTION = "allow_safe_workspace_inspection"
    ALLOW_BOUNDED_STEP_WITH_SUPPLIED_OUTPUT = "allow_bounded_step_with_supplied_output"
    ALLOW_BOUNDED_STEP_WITH_MOCK_OUTPUT = "allow_bounded_step_with_mock_output"
    ALLOW_TRACE_PREVIEW = "allow_trace_preview"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    ASK_USER_REQUIRED = "ask_user_required"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class CLIAgentOutputFormat(StrEnum):
    TEXT = "text"
    MARKDOWN = "markdown"
    JSON = "json"
    STRUCTURED_ARTIFACT = "structured_artifact"
    DEBUG_SUMMARY = "debug_summary"
    NO_OUTPUT = "no_output"
    UNKNOWN = "unknown"


class CLIAgentRiskKind(StrEnum):
    SHELL_INJECTION_RISK = "shell_injection_risk"
    PATH_TRAVERSAL_RISK = "path_traversal_risk"
    SECRET_FILE_RISK = "secret_file_risk"
    PROVIDER_INVOCATION_RISK = "provider_invocation_risk"
    REAL_MODEL_INVOCATION_RISK = "real_model_invocation_risk"
    COMMAND_EXECUTION_RISK = "command_execution_risk"
    WORKSPACE_WRITE_RISK = "workspace_write_risk"
    NETWORK_ACCESS_RISK = "network_access_risk"
    CREDENTIAL_ACCESS_RISK = "credential_access_risk"
    REFERENCE_EXECUTION_RISK = "reference_execution_risk"
    GENERAL_TOOL_EXECUTION_RISK = "general_tool_execution_risk"
    RAW_OUTPUT_PERSISTENCE_RISK = "raw_output_persistence_risk"
    PERSISTENT_TRACE_WRITE_RISK = "persistent_trace_write_risk"
    EXTERNAL_TRACE_SINK_RISK = "external_trace_sink_risk"
    EXTERNAL_CONTROL_RISK = "external_control_risk"
    AUTHORITY_GRANT_RISK = "authority_grant_risk"
    UNKNOWN = "unknown"


class CLIAgentReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    CLI_CONTRACT_READY = "cli_contract_ready"
    BOUNDED_CLI_SURFACE_READY = "bounded_cli_surface_ready"
    BOUNDED_CLI_COMMAND_DISPATCH_READY = "bounded_cli_command_dispatch_ready"
    DESIGN_HANDOFF_READY_FOR_V0339 = "design_handoff_ready_for_v0339"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


UNSAFE_CLI_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_real_model_invocation",
    "ready_for_model_invocation",
    "ready_for_provider_invocation",
    "ready_for_general_agent_execution",
    "ready_for_general_tool_execution",
    "ready_for_general_ocel_emission",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_command_execution",
    "ready_for_network_access",
    "ready_for_credential_access",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_patch_application",
    "ready_for_registry_mutation",
    "ready_for_memory_mutation",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
)

INSPECTION_COMMAND_KINDS = {
    CLIAgentCommandKind.AGENT_INSPECT_PATH_READONLY,
    CLIAgentCommandKind.AGENT_INSPECT_TREE_READONLY,
    CLIAgentCommandKind.AGENT_READ_TEXT_FILE_SAFE,
    CLIAgentCommandKind.AGENT_SEARCH_WORKSPACE_READONLY,
    CLIAgentCommandKind.AGENT_REFERENCE_SUMMARY_READONLY,
}

STEP_COMMAND_KINDS = {
    CLIAgentCommandKind.AGENT_STEP_WITH_SUPPLIED_OUTPUT,
    CLIAgentCommandKind.AGENT_STEP_WITH_MOCK_OUTPUT,
}

TRACE_COMMAND_KINDS = {
    CLIAgentCommandKind.AGENT_TRACE_PREVIEW_FROM_STEP_OUTPUT,
    CLIAgentCommandKind.AGENT_TRACE_PREVIEW_FROM_SESSION_SNAPSHOT,
}

SAFE_COMMAND_ALIASES = {
    "help": CLIAgentCommandKind.AGENT_HELP,
    "--help": CLIAgentCommandKind.AGENT_HELP,
    "-h": CLIAgentCommandKind.AGENT_HELP,
    "status": CLIAgentCommandKind.AGENT_STATUS,
    "profile-preview": CLIAgentCommandKind.AGENT_PROFILE_PREVIEW,
    "prompt-preview": CLIAgentCommandKind.AGENT_PROMPT_PREVIEW,
    "session-preview": CLIAgentCommandKind.AGENT_SESSION_PREVIEW,
    "inspect-path": CLIAgentCommandKind.AGENT_INSPECT_PATH_READONLY,
    "inspect-tree": CLIAgentCommandKind.AGENT_INSPECT_TREE_READONLY,
    "read-text": CLIAgentCommandKind.AGENT_READ_TEXT_FILE_SAFE,
    "search": CLIAgentCommandKind.AGENT_SEARCH_WORKSPACE_READONLY,
    "reference-summary": CLIAgentCommandKind.AGENT_REFERENCE_SUMMARY_READONLY,
    "step": CLIAgentCommandKind.AGENT_STEP_WITH_SUPPLIED_OUTPUT,
    "trace-preview": CLIAgentCommandKind.AGENT_TRACE_PREVIEW_FROM_STEP_OUTPUT,
    "no-op": CLIAgentCommandKind.AGENT_NO_OP,
}


def _validate_version_includes_v0338(version: str) -> None:
    _require_non_blank("version", version)
    if V0338_VERSION not in version:
        raise ValueError("version must include v0.33.8")


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.33.8")


def _validate_enum_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _validate_non_negative_int(name: str, value: int) -> None:
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be >= 0")


def _validate_source_ref_list(values: list["CLIAgentSourceRef"]) -> None:
    _validate_object_list("source_refs", values, CLIAgentSourceRef)


def _has_prohibited_arg(value: str, patterns: list[str]) -> bool:
    lowered = value.lower()
    return any(pattern.lower() in lowered for pattern in patterns)


def _safe_preview(value: Any, max_chars: int = MAX_RENDERED_OUTPUT_CHARS) -> tuple[str, bool, bool]:
    if value is None:
        text = ""
    elif isinstance(value, dict):
        text = json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
    else:
        text = str(value)
    redacted = _has_prohibited_arg(text, ["secret=", "token=", "credential=", "id_rsa", "private key"])
    if redacted:
        text = "[redacted]"
    truncated = len(text) > max_chars
    if truncated:
        text = text[: max(max_chars - 14, 0)] + "...[truncated]"
    return text, redacted, truncated


def _command_mode_for_kind(command_kind: CLIAgentCommandKind | str) -> CLIAgentCommandMode:
    kind = CLIAgentCommandKind(command_kind)
    if kind == CLIAgentCommandKind.AGENT_HELP:
        return CLIAgentCommandMode.HELP
    if kind == CLIAgentCommandKind.AGENT_STATUS:
        return CLIAgentCommandMode.STATUS
    if kind in {
        CLIAgentCommandKind.AGENT_PROFILE_PREVIEW,
        CLIAgentCommandKind.AGENT_PROMPT_PREVIEW,
        CLIAgentCommandKind.AGENT_SESSION_PREVIEW,
    }:
        return CLIAgentCommandMode.PREVIEW
    if kind in INSPECTION_COMMAND_KINDS:
        return CLIAgentCommandMode.READONLY_INSPECTION
    if kind in STEP_COMMAND_KINDS:
        return CLIAgentCommandMode.BOUNDED_STEP
    if kind in TRACE_COMMAND_KINDS:
        return CLIAgentCommandMode.TRACE_PREVIEW
    if kind == CLIAgentCommandKind.AGENT_NO_OP:
        return CLIAgentCommandMode.NO_OP
    return CLIAgentCommandMode.UNKNOWN


@dataclass(frozen=True)
class CLIAgentFlagSet:
    flag_set_id: str
    version: str = V0338_VERSION
    cli_surface_constructed: bool = False
    cli_argument_parsing_enabled: bool = False
    bounded_cli_command_dispatch_enabled: bool = False
    ready_for_v0339_consolidation: bool = False
    ready_for_bounded_cli_agent_run: bool = False
    ready_for_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_real_model_invocation: bool = False
    ready_for_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_bounded_agent_step_execution: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_safe_readonly_tool_execution: bool = False
    ready_for_safe_workspace_inspection_execution: bool = False
    ready_for_bounded_internal_ocel_trace_emission: bool = False
    ready_for_general_ocel_emission: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_command_execution: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_application: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version_includes_v0338(self.version)
        _validate_false(self, UNSAFE_CLI_FLAG_NAMES)
        if _metadata_flag_true(self.metadata, {"shell", "subprocess", "provider_invocation", "persistent_trace_write"}):
            raise ValueError("CLIAgentFlagSet is not shell/provider/persistent runtime readiness")


@dataclass(frozen=True)
class CLIAgentSourceRef:
    source_ref_id: str
    source_kind: CLIAgentInputSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        CLIAgentInputSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"shell", "provider_call", "file_read"}):
            raise ValueError("CLIAgentSourceRef is not shell command, provider call, or file read")

    @property
    def shell_command(self) -> bool:
        return False

    @property
    def provider_call(self) -> bool:
        return False

    @property
    def file_read(self) -> bool:
        return False


@dataclass(frozen=True)
class CLIAgentArgumentSpec:
    argument_spec_id: str
    name: str
    required: bool = False
    allowed_values: list[str] = field(default_factory=list)
    prohibited_values: list[str] = field(default_factory=list)
    allow_path_value: bool = False
    allow_json_value: bool = False
    max_value_chars: int = MAX_CLI_ARG_CHARS
    description: str = "Bounded CLI argument."
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("argument_spec_id", self.argument_spec_id)
        _require_non_blank("name", self.name)
        _validate_string_list("allowed_values", self.allowed_values)
        _validate_string_list("prohibited_values", self.prohibited_values)
        _validate_non_negative_int("max_value_chars", self.max_value_chars)
        _require_non_blank("description", self.description)
        if _metadata_flag_true(self.metadata, {"execution"}):
            raise ValueError("CLIAgentArgumentSpec is not argument execution")


@dataclass(frozen=True)
class CLIAgentCommandSpec:
    command_spec_id: str
    command_kind: CLIAgentCommandKind | str
    command_mode: CLIAgentCommandMode | str
    command_name: str
    description: str
    argument_specs: list[CLIAgentArgumentSpec] = field(default_factory=list)
    allowed_output_formats: list[CLIAgentOutputFormat | str] = field(default_factory=lambda: [CLIAgentOutputFormat.TEXT, CLIAgentOutputFormat.JSON])
    allowed_decisions: list[CLIAgentDecisionKind | str] = field(default_factory=list)
    risk_kinds: list[CLIAgentRiskKind | str] = field(default_factory=list)
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("command_spec_id", self.command_spec_id)
        kind = CLIAgentCommandKind(self.command_kind)
        CLIAgentCommandMode(self.command_mode)
        _require_non_blank("command_name", self.command_name)
        _require_non_blank("description", self.description)
        _validate_object_list("argument_specs", self.argument_specs, CLIAgentArgumentSpec)
        _validate_enum_list("allowed_output_formats", self.allowed_output_formats, CLIAgentOutputFormat)
        _validate_enum_list("allowed_decisions", self.allowed_decisions, CLIAgentDecisionKind)
        _validate_enum_list("risk_kinds", self.risk_kinds, CLIAgentRiskKind)
        if self.enabled and kind == CLIAgentCommandKind.UNKNOWN:
            raise ValueError("unknown command spec cannot be enabled")
        if _metadata_flag_true(self.metadata, {"os_command", "shell"}):
            raise ValueError("CLIAgentCommandSpec is not OS command")

    @property
    def os_command(self) -> bool:
        return False


@dataclass(frozen=True)
class CLIAgentSurfacePolicy:
    policy_id: str
    allowed_command_kinds: list[CLIAgentCommandKind | str] = field(default_factory=list)
    blocked_command_kinds: list[CLIAgentCommandKind | str] = field(default_factory=lambda: [CLIAgentCommandKind.UNKNOWN])
    allowed_output_formats: list[CLIAgentOutputFormat | str] = field(default_factory=lambda: [CLIAgentOutputFormat.TEXT, CLIAgentOutputFormat.JSON, CLIAgentOutputFormat.MARKDOWN, CLIAgentOutputFormat.STRUCTURED_ARTIFACT])
    prohibited_arg_patterns: list[str] = field(default_factory=lambda: list(DEFAULT_CLI_PROHIBITED_ARG_PATTERNS))
    max_arg_chars: int = MAX_CLI_ARG_CHARS
    allow_shell: bool = False
    allow_subprocess: bool = False
    allow_real_model_invocation: bool = False
    allow_provider_invocation: bool = False
    allow_general_tool_execution: bool = False
    allow_safe_workspace_inspection: bool = True
    allow_bounded_agent_step: bool = True
    allow_bounded_trace_preview: bool = True
    allow_workspace_write: bool = False
    allow_network_access: bool = False
    allow_credential_access: bool = False
    allow_persistent_trace_write: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_id", self.policy_id)
        _validate_enum_list("allowed_command_kinds", self.allowed_command_kinds, CLIAgentCommandKind)
        _validate_enum_list("blocked_command_kinds", self.blocked_command_kinds, CLIAgentCommandKind)
        _validate_enum_list("allowed_output_formats", self.allowed_output_formats, CLIAgentOutputFormat)
        _validate_string_list("prohibited_arg_patterns", self.prohibited_arg_patterns)
        if not any(pattern in self.prohibited_arg_patterns for pattern in (";", "|", "&&", "||")):
            raise ValueError("prohibited_arg_patterns must include shell-like metacharacters")
        _validate_non_negative_int("max_arg_chars", self.max_arg_chars)
        _validate_false(
            self,
            (
                "allow_shell",
                "allow_subprocess",
                "allow_real_model_invocation",
                "allow_provider_invocation",
                "allow_general_tool_execution",
                "allow_workspace_write",
                "allow_network_access",
                "allow_credential_access",
                "allow_persistent_trace_write",
            ),
        )


@dataclass(frozen=True)
class CLIAgentSurface:
    cli_surface_id: str
    version: str
    command_specs: list[CLIAgentCommandSpec]
    policy: CLIAgentSurfacePolicy
    flags: CLIAgentFlagSet
    status: CLIAgentSurfaceStatus | str = CLIAgentSurfaceStatus.INITIALIZED
    readiness_level: CLIAgentReadinessLevel | str = CLIAgentReadinessLevel.BOUNDED_CLI_COMMAND_DISPATCH_READY
    summary: str = "Bounded CLI Agent Run Surface."
    ready_for_bounded_cli_agent_run: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("cli_surface_id", self.cli_surface_id)
        _validate_version_includes_v0338(self.version)
        _validate_object_list("command_specs", self.command_specs, CLIAgentCommandSpec)
        if not isinstance(self.policy, CLIAgentSurfacePolicy):
            raise TypeError("policy must be CLIAgentSurfacePolicy")
        if not isinstance(self.flags, CLIAgentFlagSet):
            raise TypeError("flags must be CLIAgentFlagSet")
        if not cli_agent_flags_preserve_unsafe_runtime_false(self.flags):
            raise ValueError("flags must preserve unsafe runtime false")
        CLIAgentSurfaceStatus(self.status)
        CLIAgentReadinessLevel(self.readiness_level)
        _require_non_blank("summary", self.summary)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        if _metadata_flag_true(self.metadata, {"shell"}):
            raise ValueError("CLIAgentSurface is not shell")


@dataclass(frozen=True)
class CLIAgentInvocation:
    invocation_id: str
    argv: list[str]
    command_kind: CLIAgentCommandKind | str
    command_mode: CLIAgentCommandMode | str
    parsed_args: dict[str, Any] = field(default_factory=dict)
    requested_output_format: CLIAgentOutputFormat | str = CLIAgentOutputFormat.TEXT
    source_refs: list[CLIAgentSourceRef] = field(default_factory=list)
    invocation_summary: str = "Parsed bounded CLI invocation artifact."
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("invocation_id", self.invocation_id)
        _validate_string_list("argv", self.argv)
        CLIAgentCommandKind(self.command_kind)
        CLIAgentCommandMode(self.command_mode)
        if not isinstance(self.parsed_args, dict):
            raise TypeError("parsed_args must be dict")
        CLIAgentOutputFormat(self.requested_output_format)
        _validate_source_ref_list(self.source_refs)
        _require_non_blank("invocation_summary", self.invocation_summary)
        if _metadata_flag_true(self.metadata, {"shell_execution", "subprocess"}):
            raise ValueError("CLIAgentInvocation is not shell execution")


@dataclass(frozen=True)
class CLIAgentInvocationDecision:
    decision_id: str
    invocation_id: str
    decision_kind: CLIAgentDecisionKind | str
    reason: str
    risk_kinds: list[CLIAgentRiskKind | str] = field(default_factory=list)
    allowed_command_kind: CLIAgentCommandKind | str | None = None
    safe_workspace_inspection_allowed: bool = False
    bounded_agent_step_allowed: bool = False
    trace_preview_allowed: bool = False
    shell_execution_allowed: bool = False
    subprocess_allowed: bool = False
    provider_invocation_allowed: bool = False
    general_tool_execution_allowed: bool = False
    workspace_write_allowed: bool = False
    network_access_allowed: bool = False
    credential_access_allowed: bool = False
    persistent_trace_write_allowed: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("decision_id", self.decision_id)
        _require_non_blank("invocation_id", self.invocation_id)
        kind = CLIAgentDecisionKind(self.decision_kind)
        _require_non_blank("reason", self.reason)
        _validate_enum_list("risk_kinds", self.risk_kinds, CLIAgentRiskKind)
        if self.allowed_command_kind is not None:
            allowed_kind = CLIAgentCommandKind(self.allowed_command_kind)
            if self.safe_workspace_inspection_allowed and allowed_kind not in INSPECTION_COMMAND_KINDS:
                raise ValueError("safe workspace inspection allowed only for v0.33.5 commands")
            if self.bounded_agent_step_allowed and allowed_kind not in STEP_COMMAND_KINDS:
                raise ValueError("bounded agent step allowed only for v0.33.6 supplied/mock commands")
            if self.trace_preview_allowed and allowed_kind not in TRACE_COMMAND_KINDS:
                raise ValueError("trace preview allowed only for v0.33.7 trace commands")
        _validate_false(
            self,
            (
                "shell_execution_allowed",
                "subprocess_allowed",
                "provider_invocation_allowed",
                "general_tool_execution_allowed",
                "workspace_write_allowed",
                "network_access_allowed",
                "credential_access_allowed",
                "persistent_trace_write_allowed",
            ),
        )
        _validate_string_list("evidence_refs", self.evidence_refs)
        if kind == CLIAgentDecisionKind.UNKNOWN:
            raise ValueError("unknown decision kind is not valid for a completed decision")


@dataclass(frozen=True)
class CLIAgentDeniedCommand:
    denied_command_id: str
    invocation_id: str | None
    decision_id: str | None
    command_kind: CLIAgentCommandKind | str = CLIAgentCommandKind.UNKNOWN
    risk_kinds: list[CLIAgentRiskKind | str] = field(default_factory=list)
    reason: str = "CLI command denied safely."
    safe_alternatives: list[str] = field(default_factory=lambda: ["agent help", "agent status", "agent no-op"])
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("denied_command_id", self.denied_command_id)
        CLIAgentCommandKind(self.command_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, CLIAgentRiskKind)
        _require_non_blank("reason", self.reason)
        _validate_string_list("safe_alternatives", self.safe_alternatives)


@dataclass(frozen=True)
class CLIAgentCommandResult:
    command_result_id: str
    invocation_id: str
    decision_id: str
    command_kind: CLIAgentCommandKind | str
    status: CLIAgentSurfaceStatus | str
    workspace_inspection_result_ref: str | None = None
    agent_step_output_ref: str | None = None
    trace_packet_ref: str | None = None
    structured_result: dict[str, Any] = field(default_factory=dict)
    text_summary: str = "CLI command completed as bounded internal artifact."
    redacted: bool = False
    truncated: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("command_result_id", self.command_result_id)
        _require_non_blank("invocation_id", self.invocation_id)
        _require_non_blank("decision_id", self.decision_id)
        CLIAgentCommandKind(self.command_kind)
        CLIAgentSurfaceStatus(self.status)
        if not isinstance(self.structured_result, dict):
            raise TypeError("structured_result must be dict")
        _require_non_blank("text_summary", self.text_summary)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")


@dataclass(frozen=True)
class CLIAgentRunOutput:
    run_output_id: str
    invocation_id: str
    command_result: CLIAgentCommandResult | None
    denied_command: CLIAgentDeniedCommand | None
    rendered_output: str
    output_format: CLIAgentOutputFormat | str
    status: CLIAgentSurfaceStatus | str
    summary: str
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_output_id", self.run_output_id)
        _require_non_blank("invocation_id", self.invocation_id)
        if self.command_result is not None and not isinstance(self.command_result, CLIAgentCommandResult):
            raise TypeError("command_result must be CLIAgentCommandResult or None")
        if self.denied_command is not None and not isinstance(self.denied_command, CLIAgentDeniedCommand):
            raise TypeError("denied_command must be CLIAgentDeniedCommand or None")
        _require_non_blank("rendered_output", self.rendered_output)
        if len(self.rendered_output) > int(self.metadata.get("max_rendered_output_chars", MAX_RENDERED_OUTPUT_CHARS)):
            raise ValueError("rendered_output must be bounded")
        CLIAgentOutputFormat(self.output_format)
        CLIAgentSurfaceStatus(self.status)
        _require_non_blank("summary", self.summary)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")


@dataclass(frozen=True)
class CLIAgentRunReport:
    report_id: str
    version: str
    invocation_id: str | None = None
    run_output_id: str | None = None
    status: CLIAgentSurfaceStatus | str = CLIAgentSurfaceStatus.COMPLETED
    readiness_level: CLIAgentReadinessLevel | str = CLIAgentReadinessLevel.BOUNDED_CLI_COMMAND_DISPATCH_READY
    summary: str = "Bounded CLI Agent Run Surface report."
    command_count: int = 0
    allowed_count: int = 0
    denied_count: int = 0
    blocked_count: int = 0
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0339_consolidation: bool = False
    ready_for_bounded_cli_agent_run: bool = False
    ready_for_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_real_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_persistent_trace_write: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0338(self.version)
        CLIAgentSurfaceStatus(self.status)
        CLIAgentReadinessLevel(self.readiness_level)
        _require_non_blank("summary", self.summary)
        for name in ("command_count", "allowed_count", "denied_count", "blocked_count"):
            _validate_non_negative_int(name, getattr(self, name))
        for name in ("completed_items", "blocked_items", "future_track_items", "gaps", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(
            self,
            (
                "ready_for_execution",
                "ready_for_shell_execution",
                "ready_for_subprocess_execution",
                "ready_for_real_model_invocation",
                "ready_for_provider_invocation",
                "ready_for_general_tool_execution",
                "ready_for_persistent_trace_write",
            ),
        )


@dataclass(frozen=True)
class CLIAgentRunPreview:
    run_preview_id: str
    cli_surface_id: str | None = None
    planned_steps: list[str] = field(default_factory=lambda: ["parse argv", "evaluate policy", "dispatch bounded command", "return output artifact"])
    expected_artifacts: list[str] = field(default_factory=lambda: ["CLIAgentInvocation", "CLIAgentInvocationDecision", "CLIAgentRunOutput"])
    explicitly_not_performed: list[str] = field(default_factory=lambda: list(DEFAULT_V0338_PROHIBITED_UNTIL_LATER_GATE))
    no_shell_execution_guarantee: bool = True
    no_subprocess_guarantee: bool = True
    no_real_model_invocation_guarantee: bool = True
    no_provider_invocation_guarantee: bool = True
    no_general_tool_execution_guarantee: bool = True
    no_command_execution_guarantee: bool = True
    no_network_access_guarantee: bool = True
    no_credential_access_guarantee: bool = True
    no_workspace_write_guarantee: bool = True
    no_code_edit_guarantee: bool = True
    no_patch_application_guarantee: bool = True
    no_reference_code_execution_guarantee: bool = True
    no_reference_import_guarantee: bool = True
    no_reference_dependency_install_guarantee: bool = True
    no_secret_file_read_guarantee: bool = True
    no_persistent_trace_write_guarantee: bool = True
    no_external_trace_sink_guarantee: bool = True
    no_ui_runtime_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True")


@dataclass(frozen=True)
class CLIAgentNoExternalSideEffectGuarantee:
    guarantee_id: str
    version: str
    no_shell_execution: bool = True
    no_subprocess: bool = True
    no_real_model_invocation: bool = True
    no_provider_invocation: bool = True
    no_general_tool_execution: bool = True
    no_command_execution: bool = True
    no_network_access: bool = True
    no_credential_access: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_patch_application: bool = True
    no_file_creation: bool = True
    no_file_deletion: bool = True
    no_file_rename: bool = True
    no_chmod_chown: bool = True
    no_reference_code_execution: bool = True
    no_reference_import: bool = True
    no_reference_dependency_install: bool = True
    no_secret_file_read: bool = True
    no_registry_mutation: bool = True
    no_memory_mutation: bool = True
    no_persistent_trace_write: bool = True
    no_external_trace_sink: bool = True
    no_ui_runtime: bool = True
    no_external_control: bool = True
    no_authority_grant: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version_includes_v0338(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True")
        _validate_string_list("evidence_refs", self.evidence_refs)


@dataclass(frozen=True)
class V0338ReadinessReport:
    report_id: str
    version: str
    cli_surface_id: str | None = None
    cli_run_report_id: str | None = None
    run_output_id: str | None = None
    summary: str = "v0.33.8 bounded CLI Agent Run Surface readiness report."
    bounded_cli_surface_enabled: bool = False
    cli_argument_parsing_enabled: bool = False
    bounded_cli_command_dispatch_enabled: bool = False
    ready_for_v0339_consolidation: bool = False
    ready_for_bounded_cli_agent_run: bool = False
    ready_for_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_real_model_invocation: bool = False
    ready_for_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_bounded_agent_step_execution: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_safe_readonly_tool_execution: bool = False
    ready_for_safe_workspace_inspection_execution: bool = False
    ready_for_bounded_internal_ocel_trace_emission: bool = False
    ready_for_general_ocel_emission: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_command_execution: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_application: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_V0338_PROHIBITED_UNTIL_LATER_GATE))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0338(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(self, UNSAFE_CLI_FLAG_NAMES)
        for name in ("completed_items", "blocked_items", "future_track_items", "prohibited_until_later_gate", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        lowered = [value.lower() for value in self.prohibited_until_later_gate]
        for required in DEFAULT_V0338_PROHIBITED_UNTIL_LATER_GATE:
            if required.lower() not in lowered:
                raise ValueError("prohibited_until_later_gate missing v0.33.8 prohibition")


def build_cli_agent_flags(flag_set_id: str = "cli_agent_flags:v0.33.8", **kwargs: Any) -> CLIAgentFlagSet:
    return CLIAgentFlagSet(flag_set_id=flag_set_id, version=V0338_VERSION, **kwargs)


def build_cli_agent_source_ref(
    source_ref_id: str,
    source_kind: CLIAgentInputSourceKind | str = CLIAgentInputSourceKind.TEST_FIXTURE,
    source_id: str = "test_fixture",
    source_summary: str = "Provided in-memory CLI source.",
    **kwargs: Any,
) -> CLIAgentSourceRef:
    return CLIAgentSourceRef(source_ref_id=source_ref_id, source_kind=source_kind, source_id=source_id, source_summary=source_summary, **kwargs)


def build_cli_agent_argument_spec(argument_spec_id: str, name: str, **kwargs: Any) -> CLIAgentArgumentSpec:
    return CLIAgentArgumentSpec(argument_spec_id=argument_spec_id, name=name, **kwargs)


def build_cli_agent_command_spec(
    command_spec_id: str,
    command_kind: CLIAgentCommandKind | str,
    command_name: str,
    **kwargs: Any,
) -> CLIAgentCommandSpec:
    kind = CLIAgentCommandKind(command_kind)
    return CLIAgentCommandSpec(
        command_spec_id=command_spec_id,
        command_kind=kind,
        command_mode=kwargs.pop("command_mode", _command_mode_for_kind(kind)),
        command_name=command_name,
        description=kwargs.pop("description", f"Bounded CLI command: {command_name}"),
        **kwargs,
    )


def default_cli_agent_command_specs() -> list[CLIAgentCommandSpec]:
    specs: list[CLIAgentCommandSpec] = []
    for alias, kind in SAFE_COMMAND_ALIASES.items():
        if alias in {"--help", "-h"}:
            continue
        specs.append(
            build_cli_agent_command_spec(
                f"cli_command_spec:{kind.value}",
                kind,
                alias,
                allowed_decisions=[
                    CLIAgentDecisionKind.ALLOW_HELP,
                    CLIAgentDecisionKind.ALLOW_STATUS,
                    CLIAgentDecisionKind.ALLOW_PREVIEW,
                    CLIAgentDecisionKind.ALLOW_SAFE_WORKSPACE_INSPECTION,
                    CLIAgentDecisionKind.ALLOW_BOUNDED_STEP_WITH_SUPPLIED_OUTPUT,
                    CLIAgentDecisionKind.ALLOW_BOUNDED_STEP_WITH_MOCK_OUTPUT,
                    CLIAgentDecisionKind.ALLOW_TRACE_PREVIEW,
                    CLIAgentDecisionKind.NO_OP,
                ],
            )
        )
    specs.append(
        build_cli_agent_command_spec(
            "cli_command_spec:agent_step_with_mock_output",
            CLIAgentCommandKind.AGENT_STEP_WITH_MOCK_OUTPUT,
            "step --mock-output",
            allowed_decisions=[CLIAgentDecisionKind.ALLOW_BOUNDED_STEP_WITH_MOCK_OUTPUT],
        )
    )
    specs.append(
        build_cli_agent_command_spec(
            "cli_command_spec:agent_trace_preview_from_session_snapshot",
            CLIAgentCommandKind.AGENT_TRACE_PREVIEW_FROM_SESSION_SNAPSHOT,
            "trace-preview --from-session-snapshot",
            allowed_decisions=[CLIAgentDecisionKind.ALLOW_TRACE_PREVIEW],
        )
    )
    return specs


def default_cli_agent_surface_policy() -> CLIAgentSurfacePolicy:
    return CLIAgentSurfacePolicy(
        policy_id="cli_agent_surface_policy:v0.33.8",
        allowed_command_kinds=[spec.command_kind for spec in default_cli_agent_command_specs()],
        blocked_command_kinds=[CLIAgentCommandKind.UNKNOWN],
    )


def build_cli_agent_surface_policy(policy_id: str = "cli_agent_surface_policy:v0.33.8", **kwargs: Any) -> CLIAgentSurfacePolicy:
    default_policy = default_cli_agent_surface_policy()
    return CLIAgentSurfacePolicy(
        policy_id=policy_id,
        allowed_command_kinds=kwargs.pop("allowed_command_kinds", list(default_policy.allowed_command_kinds)),
        blocked_command_kinds=kwargs.pop("blocked_command_kinds", list(default_policy.blocked_command_kinds)),
        **kwargs,
    )


def build_cli_agent_surface(cli_surface_id: str, **kwargs: Any) -> CLIAgentSurface:
    policy = kwargs.pop("policy", default_cli_agent_surface_policy())
    flags = kwargs.pop(
        "flags",
        build_cli_agent_flags(
            cli_surface_constructed=True,
            cli_argument_parsing_enabled=True,
            bounded_cli_command_dispatch_enabled=True,
            ready_for_v0339_consolidation=True,
            ready_for_bounded_cli_agent_run=True,
            ready_for_bounded_agent_step_execution=True,
            ready_for_safe_readonly_tool_execution=True,
            ready_for_safe_workspace_inspection_execution=True,
            ready_for_bounded_internal_ocel_trace_emission=True,
        ),
    )
    return CLIAgentSurface(
        cli_surface_id=cli_surface_id,
        version=V0338_VERSION,
        command_specs=kwargs.pop("command_specs", default_cli_agent_command_specs()),
        policy=policy,
        flags=flags,
        ready_for_bounded_cli_agent_run=kwargs.pop("ready_for_bounded_cli_agent_run", True),
        **kwargs,
    )


def build_default_cli_agent_surface() -> CLIAgentSurface:
    return build_cli_agent_surface("cli_agent_surface:v0.33.8")


def build_cli_agent_invocation(
    invocation_id: str,
    argv: list[str],
    command_kind: CLIAgentCommandKind | str,
    **kwargs: Any,
) -> CLIAgentInvocation:
    kind = CLIAgentCommandKind(command_kind)
    return CLIAgentInvocation(
        invocation_id=invocation_id,
        argv=argv,
        command_kind=kind,
        command_mode=kwargs.pop("command_mode", _command_mode_for_kind(kind)),
        **kwargs,
    )


def build_cli_agent_invocation_decision(
    decision_id: str,
    invocation_id: str,
    decision_kind: CLIAgentDecisionKind | str,
    reason: str,
    **kwargs: Any,
) -> CLIAgentInvocationDecision:
    return CLIAgentInvocationDecision(decision_id=decision_id, invocation_id=invocation_id, decision_kind=decision_kind, reason=reason, **kwargs)


def build_cli_agent_denied_command(denied_command_id: str, **kwargs: Any) -> CLIAgentDeniedCommand:
    return CLIAgentDeniedCommand(denied_command_id=denied_command_id, **kwargs)


def build_cli_agent_command_result(
    command_result_id: str,
    invocation_id: str,
    decision_id: str,
    command_kind: CLIAgentCommandKind | str,
    status: CLIAgentSurfaceStatus | str,
    **kwargs: Any,
) -> CLIAgentCommandResult:
    return CLIAgentCommandResult(
        command_result_id=command_result_id,
        invocation_id=invocation_id,
        decision_id=decision_id,
        command_kind=command_kind,
        status=status,
        **kwargs,
    )


def build_cli_agent_run_output(
    run_output_id: str,
    invocation_id: str,
    rendered_output: str,
    status: CLIAgentSurfaceStatus | str,
    **kwargs: Any,
) -> CLIAgentRunOutput:
    return CLIAgentRunOutput(run_output_id=run_output_id, invocation_id=invocation_id, rendered_output=rendered_output, status=status, **kwargs)


def build_cli_agent_run_report(report_id: str, **kwargs: Any) -> CLIAgentRunReport:
    return CLIAgentRunReport(report_id=report_id, version=V0338_VERSION, **kwargs)


def build_cli_agent_run_preview(run_preview_id: str, **kwargs: Any) -> CLIAgentRunPreview:
    return CLIAgentRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_cli_agent_no_external_side_effect_guarantee(
    guarantee_id: str = "cli_agent_no_external_side_effect:v0.33.8",
    **kwargs: Any,
) -> CLIAgentNoExternalSideEffectGuarantee:
    return CLIAgentNoExternalSideEffectGuarantee(guarantee_id=guarantee_id, version=V0338_VERSION, **kwargs)


def build_v0338_readiness_report(report_id: str = "v0338_readiness_report", **kwargs: Any) -> V0338ReadinessReport:
    return V0338ReadinessReport(report_id=report_id, version=V0338_VERSION, **kwargs)


def _parse_option_pairs(tokens: list[str]) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token.startswith("--"):
            key = "_".join(token[2:].split("-"))
            if index + 1 < len(tokens) and not tokens[index + 1].startswith("--"):
                parsed[key] = tokens[index + 1]
                index += 2
            else:
                parsed[key] = True
                index += 1
        else:
            parsed.setdefault("positional", []).append(token)
            index += 1
    return parsed


def _kind_from_argv(argv: list[str]) -> CLIAgentCommandKind:
    tokens = list(argv)
    if tokens and tokens[0] == "agent":
        tokens = tokens[1:]
    if not tokens:
        return CLIAgentCommandKind.AGENT_HELP
    first = tokens[0]
    if first == "step":
        parsed = _parse_option_pairs(tokens[1:])
        if "mock_output" in parsed:
            return CLIAgentCommandKind.AGENT_STEP_WITH_MOCK_OUTPUT
        return CLIAgentCommandKind.AGENT_STEP_WITH_SUPPLIED_OUTPUT
    if first == "trace-preview":
        parsed = _parse_option_pairs(tokens[1:])
        if "from_session_snapshot" in parsed:
            return CLIAgentCommandKind.AGENT_TRACE_PREVIEW_FROM_SESSION_SNAPSHOT
        return CLIAgentCommandKind.AGENT_TRACE_PREVIEW_FROM_STEP_OUTPUT
    return SAFE_COMMAND_ALIASES.get(first, CLIAgentCommandKind.UNKNOWN)


def parse_cli_agent_invocation(argv: list[str], surface: CLIAgentSurface | None = None) -> CLIAgentInvocation:
    if not isinstance(argv, list):
        raise TypeError("argv must be list")
    active_surface = surface or build_default_cli_agent_surface()
    safe_argv = [str(item)[: active_surface.policy.max_arg_chars] for item in argv]
    tokens = list(safe_argv)
    if tokens and tokens[0] == "agent":
        tokens = tokens[1:]
    command_token = tokens[0] if tokens else "help"
    option_tokens = tokens[1:] if tokens else []
    parsed_args = _parse_option_pairs(option_tokens)
    command_kind = _kind_from_argv(safe_argv)
    output_format_value = parsed_args.get("format", CLIAgentOutputFormat.TEXT)
    try:
        output_format = CLIAgentOutputFormat(output_format_value)
    except ValueError:
        output_format = CLIAgentOutputFormat.TEXT
    parsed_args["command_token"] = command_token
    return build_cli_agent_invocation(
        "cli_invocation:v0.33.8:" + ("_".join(command_token.split(":")) or "help"),
        safe_argv,
        command_kind,
        parsed_args=parsed_args,
        requested_output_format=output_format,
        source_refs=[
            build_cli_agent_source_ref(
                "cli_source:argv",
                CLIAgentInputSourceKind.ARGV_LIST,
                "argv",
                "CLI-style argv list supplied in memory.",
            )
        ],
    )


def evaluate_cli_agent_invocation(invocation: CLIAgentInvocation, surface: CLIAgentSurface) -> CLIAgentInvocationDecision:
    if not isinstance(invocation, CLIAgentInvocation):
        raise TypeError("invocation must be CLIAgentInvocation")
    if not isinstance(surface, CLIAgentSurface):
        raise TypeError("surface must be CLIAgentSurface")
    command_kind = CLIAgentCommandKind(invocation.command_kind)
    risks: list[CLIAgentRiskKind | str] = []

    for value in invocation.argv:
        if len(value) > surface.policy.max_arg_chars:
            risks.append(CLIAgentRiskKind.SHELL_INJECTION_RISK)
        if _has_prohibited_arg(value, surface.policy.prohibited_arg_patterns):
            risks.append(CLIAgentRiskKind.SHELL_INJECTION_RISK)
            if any(secret in value.lower() for secret in ("secret", "token", "credential", ".env", "id_rsa", ".pem")):
                risks.append(CLIAgentRiskKind.SECRET_FILE_RISK)

    command_token = str(invocation.parsed_args.get("command_token", "")).lower()
    explicit_unsafe = {
        "shell": CLIAgentRiskKind.SHELL_INJECTION_RISK,
        "run": CLIAgentRiskKind.COMMAND_EXECUTION_RISK,
        "exec": CLIAgentRiskKind.COMMAND_EXECUTION_RISK,
        "provider": CLIAgentRiskKind.PROVIDER_INVOCATION_RISK,
        "model": CLIAgentRiskKind.REAL_MODEL_INVOCATION_RISK,
        "write": CLIAgentRiskKind.WORKSPACE_WRITE_RISK,
        "edit": CLIAgentRiskKind.WORKSPACE_WRITE_RISK,
        "patch": CLIAgentRiskKind.WORKSPACE_WRITE_RISK,
        "install": CLIAgentRiskKind.REFERENCE_EXECUTION_RISK,
        "opencode": CLIAgentRiskKind.REFERENCE_EXECUTION_RISK,
        "hermes": CLIAgentRiskKind.REFERENCE_EXECUTION_RISK,
    }
    if command_token in explicit_unsafe:
        risks.append(explicit_unsafe[command_token])

    if command_kind == CLIAgentCommandKind.UNKNOWN or command_kind in surface.policy.blocked_command_kinds or risks:
        return build_cli_agent_invocation_decision(
            f"{invocation.invocation_id}:decision",
            invocation.invocation_id,
            CLIAgentDecisionKind.BLOCK,
            "Unknown, unsupported, shell-like, or unsafe CLI command was blocked.",
            risk_kinds=list(dict.fromkeys(risks or [CLIAgentRiskKind.UNKNOWN])),
            allowed_command_kind=None,
        )
    if command_kind not in surface.policy.allowed_command_kinds:
        return build_cli_agent_invocation_decision(
            f"{invocation.invocation_id}:decision",
            invocation.invocation_id,
            CLIAgentDecisionKind.DENY,
            "Command is not enabled by v0.33.8 CLI surface policy.",
            risk_kinds=[CLIAgentRiskKind.UNKNOWN],
        )
    if command_kind == CLIAgentCommandKind.AGENT_HELP:
        return build_cli_agent_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIAgentDecisionKind.ALLOW_HELP, "Help command is bounded output only.", allowed_command_kind=command_kind)
    if command_kind == CLIAgentCommandKind.AGENT_STATUS:
        return build_cli_agent_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIAgentDecisionKind.ALLOW_STATUS, "Status command is bounded output only.", allowed_command_kind=command_kind)
    if CLIAgentCommandMode(invocation.command_mode) == CLIAgentCommandMode.PREVIEW:
        return build_cli_agent_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIAgentDecisionKind.ALLOW_PREVIEW, "Preview command is bounded output only.", allowed_command_kind=command_kind)
    if command_kind in INSPECTION_COMMAND_KINDS:
        if not surface.policy.allow_safe_workspace_inspection:
            return build_cli_agent_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIAgentDecisionKind.DENY, "Safe workspace inspection is disabled by policy.", risk_kinds=[CLIAgentRiskKind.GENERAL_TOOL_EXECUTION_RISK])
        return build_cli_agent_invocation_decision(
            f"{invocation.invocation_id}:decision",
            invocation.invocation_id,
            CLIAgentDecisionKind.ALLOW_SAFE_WORKSPACE_INSPECTION,
            "Allowed only through v0.33.5 safe workspace inspection.",
            allowed_command_kind=command_kind,
            safe_workspace_inspection_allowed=True,
        )
    if command_kind in STEP_COMMAND_KINDS:
        output_key = "mock_output" if command_kind == CLIAgentCommandKind.AGENT_STEP_WITH_MOCK_OUTPUT else "supplied_output"
        if output_key not in invocation.parsed_args:
            return build_cli_agent_invocation_decision(
                f"{invocation.invocation_id}:decision",
                invocation.invocation_id,
                CLIAgentDecisionKind.DENY,
                "Bounded CLI step requires supplied/mock model output.",
                risk_kinds=[CLIAgentRiskKind.REAL_MODEL_INVOCATION_RISK],
            )
        decision_kind = CLIAgentDecisionKind.ALLOW_BOUNDED_STEP_WITH_MOCK_OUTPUT if command_kind == CLIAgentCommandKind.AGENT_STEP_WITH_MOCK_OUTPUT else CLIAgentDecisionKind.ALLOW_BOUNDED_STEP_WITH_SUPPLIED_OUTPUT
        return build_cli_agent_invocation_decision(
            f"{invocation.invocation_id}:decision",
            invocation.invocation_id,
            decision_kind,
            "Allowed only through v0.33.6 supplied/mock bounded step runner.",
            allowed_command_kind=command_kind,
            bounded_agent_step_allowed=True,
        )
    if command_kind in TRACE_COMMAND_KINDS:
        return build_cli_agent_invocation_decision(
            f"{invocation.invocation_id}:decision",
            invocation.invocation_id,
            CLIAgentDecisionKind.ALLOW_TRACE_PREVIEW,
            "Allowed only through v0.33.7 returned trace packet creation.",
            allowed_command_kind=command_kind,
            trace_preview_allowed=True,
        )
    if command_kind == CLIAgentCommandKind.AGENT_NO_OP:
        return build_cli_agent_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIAgentDecisionKind.NO_OP, "No-op command performs no action.", allowed_command_kind=command_kind)
    return build_cli_agent_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIAgentDecisionKind.BLOCK, "Unsupported command was blocked.", risk_kinds=[CLIAgentRiskKind.UNKNOWN])


def _workspace_request_for_invocation(invocation: CLIAgentInvocation) -> tuple[WorkspaceInspectionRequestKind, WorkspaceInspectionToolKind]:
    kind = CLIAgentCommandKind(invocation.command_kind)
    if kind == CLIAgentCommandKind.AGENT_INSPECT_PATH_READONLY:
        return WorkspaceInspectionRequestKind.INSPECT_PATH, WorkspaceInspectionToolKind.INSPECT_WORKSPACE_PATH_READONLY
    if kind == CLIAgentCommandKind.AGENT_INSPECT_TREE_READONLY:
        return WorkspaceInspectionRequestKind.INSPECT_TREE, WorkspaceInspectionToolKind.INSPECT_PROJECT_TREE_READONLY
    if kind == CLIAgentCommandKind.AGENT_READ_TEXT_FILE_SAFE:
        return WorkspaceInspectionRequestKind.READ_SAFE_TEXT, WorkspaceInspectionToolKind.READ_TEXT_FILE_SAFE
    if kind == CLIAgentCommandKind.AGENT_SEARCH_WORKSPACE_READONLY:
        return WorkspaceInspectionRequestKind.SEARCH_SAFE_TEXT, WorkspaceInspectionToolKind.SEARCH_TEXT_IN_WORKSPACE_READONLY
    if kind == CLIAgentCommandKind.AGENT_REFERENCE_SUMMARY_READONLY:
        return WorkspaceInspectionRequestKind.SUMMARIZE_REFERENCE_INVENTORY, WorkspaceInspectionToolKind.SUMMARIZE_REFERENCE_INVENTORY_READONLY
    return WorkspaceInspectionRequestKind.NO_OP, WorkspaceInspectionToolKind.UNKNOWN


def _run_workspace_command(invocation: CLIAgentInvocation, workspace_policy: WorkspaceInspectionPathPolicy) -> WorkspaceInspectionToolResult:
    request_kind, tool_kind = _workspace_request_for_invocation(invocation)
    request = build_workspace_inspection_request(
        f"{invocation.invocation_id}:workspace_request",
        request_kind,
        tool_kind,
        path_ref=invocation.parsed_args.get("path"),
        query=invocation.parsed_args.get("query"),
        request_summary="v0.33.8 CLI safe workspace inspection bridge.",
    )
    if tool_kind == WorkspaceInspectionToolKind.INSPECT_WORKSPACE_PATH_READONLY:
        return inspect_workspace_path_readonly(request, workspace_policy)
    if tool_kind == WorkspaceInspectionToolKind.INSPECT_PROJECT_TREE_READONLY:
        return inspect_project_tree_readonly(request, workspace_policy)
    if tool_kind == WorkspaceInspectionToolKind.READ_TEXT_FILE_SAFE:
        return read_text_file_safe(request, workspace_policy)
    if tool_kind == WorkspaceInspectionToolKind.SEARCH_TEXT_IN_WORKSPACE_READONLY:
        return search_text_in_workspace_readonly(request, workspace_policy)
    if tool_kind == WorkspaceInspectionToolKind.SUMMARIZE_REFERENCE_INVENTORY_READONLY:
        return summarize_reference_inventory_readonly(request, workspace_policy)
    return inspect_file_metadata_readonly(request, workspace_policy)


def _run_step_command(invocation: CLIAgentInvocation, workspace_policy: WorkspaceInspectionPathPolicy | None) -> AgentStepOutput:
    command_kind = CLIAgentCommandKind(invocation.command_kind)
    raw_output = invocation.parsed_args.get("mock_output" if command_kind == CLIAgentCommandKind.AGENT_STEP_WITH_MOCK_OUTPUT else "supplied_output", "")
    structured_action: dict[str, Any] | None = None
    if isinstance(raw_output, str) and raw_output.strip().startswith("{"):
        try:
            loaded = json.loads(raw_output)
        except json.JSONDecodeError:
            loaded = None
        if isinstance(loaded, dict):
            structured_action = loaded
    model_output = build_agent_supplied_model_output(
        f"{invocation.invocation_id}:model_output",
        raw_text=str(raw_output),
        structured_action=structured_action,
        output_summary="CLI supplied/mock model output artifact.",
    )
    step_input = build_agent_step_input(
        f"{invocation.invocation_id}:step_input",
        supplied_model_output=model_output,
        task_summary="v0.33.8 bounded CLI step command.",
    )
    return run_agent_step_mvp(step_input, build_agent_step_runner_mvp(), workspace_policy=workspace_policy)


def render_cli_agent_output(output: CLIAgentRunOutput, output_format: CLIAgentOutputFormat | str | None = None) -> str:
    if not isinstance(output, CLIAgentRunOutput):
        raise TypeError("output must be CLIAgentRunOutput")
    fmt = CLIAgentOutputFormat(output_format or output.output_format)
    if fmt == CLIAgentOutputFormat.NO_OUTPUT:
        return ""
    if fmt == CLIAgentOutputFormat.JSON:
        payload = {
            "run_output_id": output.run_output_id,
            "status": str(output.status),
            "summary": output.summary,
            "result": output.command_result.structured_result if output.command_result else None,
            "denied": output.denied_command.reason if output.denied_command else None,
        }
        rendered, _, _ = _safe_preview(payload)
        return rendered
    return output.rendered_output


def _run_output_from_result(invocation: CLIAgentInvocation, result: CLIAgentCommandResult) -> CLIAgentRunOutput:
    rendered, redacted, truncated = _safe_preview(result.structured_result or result.text_summary)
    if not rendered:
        rendered = result.text_summary
    result = CLIAgentCommandResult(
        **{
            **result.__dict__,
            "redacted": result.redacted or redacted,
            "truncated": result.truncated or truncated,
        }
    )
    return build_cli_agent_run_output(
        f"{invocation.invocation_id}:run_output",
        invocation.invocation_id,
        rendered,
        result.status,
        command_result=result,
        denied_command=None,
        output_format=invocation.requested_output_format,
        summary=result.text_summary,
        metadata={"max_rendered_output_chars": MAX_RENDERED_OUTPUT_CHARS},
    )


def _run_output_from_denial(invocation: CLIAgentInvocation, decision: CLIAgentInvocationDecision) -> CLIAgentRunOutput:
    denied = build_cli_agent_denied_command(
        f"{invocation.invocation_id}:denied",
        invocation_id=invocation.invocation_id,
        decision_id=decision.decision_id,
        command_kind=invocation.command_kind,
        risk_kinds=list(decision.risk_kinds),
        reason=decision.reason,
    )
    rendered, _, _ = _safe_preview({"denied": denied.reason, "safe_alternatives": denied.safe_alternatives})
    return build_cli_agent_run_output(
        f"{invocation.invocation_id}:run_output",
        invocation.invocation_id,
        rendered,
        CLIAgentSurfaceStatus.BLOCKED,
        command_result=None,
        denied_command=denied,
        output_format=invocation.requested_output_format,
        summary="CLI command was denied or blocked safely.",
    )


def run_cli_agent_command(
    invocation: CLIAgentInvocation,
    surface: CLIAgentSurface,
    runtime_context: dict[str, Any] | None = None,
) -> CLIAgentRunOutput:
    if not isinstance(invocation, CLIAgentInvocation):
        raise TypeError("invocation must be CLIAgentInvocation")
    if not isinstance(surface, CLIAgentSurface):
        raise TypeError("surface must be CLIAgentSurface")
    context = runtime_context or {}
    decision = evaluate_cli_agent_invocation(invocation, surface)
    decision_kind = CLIAgentDecisionKind(decision.decision_kind)
    command_kind = CLIAgentCommandKind(invocation.command_kind)
    if decision_kind in {CLIAgentDecisionKind.BLOCK, CLIAgentDecisionKind.DENY}:
        return _run_output_from_denial(invocation, decision)

    if decision_kind in {CLIAgentDecisionKind.ALLOW_HELP, CLIAgentDecisionKind.ALLOW_STATUS, CLIAgentDecisionKind.ALLOW_PREVIEW, CLIAgentDecisionKind.NO_OP}:
        payload = {
            "command": command_kind.value,
            "safe_commands": sorted(alias for alias in SAFE_COMMAND_ALIASES if not alias.startswith("-")),
            "ready_for_execution": False,
        }
        result = build_cli_agent_command_result(
            f"{invocation.invocation_id}:result",
            invocation.invocation_id,
            decision.decision_id,
            command_kind,
            CLIAgentSurfaceStatus.NO_OP if decision_kind == CLIAgentDecisionKind.NO_OP else CLIAgentSurfaceStatus.COMPLETED,
            structured_result=payload,
            text_summary="Bounded CLI metadata/help/status/preview output.",
        )
        return _run_output_from_result(invocation, result)

    if decision_kind == CLIAgentDecisionKind.ALLOW_SAFE_WORKSPACE_INSPECTION:
        workspace_policy = context.get("workspace_policy")
        if not isinstance(workspace_policy, WorkspaceInspectionPathPolicy):
            return _run_output_from_denial(
                invocation,
                build_cli_agent_invocation_decision(
                    f"{invocation.invocation_id}:decision:no_workspace_policy",
                    invocation.invocation_id,
                    CLIAgentDecisionKind.BLOCK,
                    "Workspace policy is required for v0.33.5 safe inspection.",
                    risk_kinds=[CLIAgentRiskKind.PATH_TRAVERSAL_RISK],
                ),
            )
        workspace_result = _run_workspace_command(invocation, workspace_policy)
        status = CLIAgentSurfaceStatus.COMPLETED_WITH_SKIPS if WorkspaceInspectionResultKind(workspace_result.result_kind) in {WorkspaceInspectionResultKind.SKIPPED_RESULT, WorkspaceInspectionResultKind.DENIED_RESULT} else CLIAgentSurfaceStatus.COMPLETED
        result = build_cli_agent_command_result(
            f"{invocation.invocation_id}:result",
            invocation.invocation_id,
            decision.decision_id,
            command_kind,
            status,
            workspace_inspection_result_ref=workspace_result.tool_result_id,
            structured_result={
                "workspace_result_id": workspace_result.tool_result_id,
                "result_kind": str(workspace_result.result_kind),
                "status": str(workspace_result.status),
                "summary": workspace_result.summary,
            },
            text_summary="CLI command completed through v0.33.5 safe workspace inspection.",
            redacted=status == CLIAgentSurfaceStatus.COMPLETED_WITH_SKIPS,
        )
        return _run_output_from_result(invocation, result)

    if decision_kind in {
        CLIAgentDecisionKind.ALLOW_BOUNDED_STEP_WITH_SUPPLIED_OUTPUT,
        CLIAgentDecisionKind.ALLOW_BOUNDED_STEP_WITH_MOCK_OUTPUT,
    }:
        step_output = _run_step_command(invocation, context.get("workspace_policy"))
        result = build_cli_agent_command_result(
            f"{invocation.invocation_id}:result",
            invocation.invocation_id,
            decision.decision_id,
            command_kind,
            CLIAgentSurfaceStatus.COMPLETED,
            agent_step_output_ref=step_output.step_output_id,
            structured_result={
                "step_output_id": step_output.step_output_id,
                "status": str(step_output.status),
                "result_kind": str(step_output.result_kind),
                "summary": step_output.summary,
                "final_response_present": step_output.final_response_text is not None,
            },
            text_summary="CLI command completed through v0.33.6 bounded supplied/mock step runner.",
        )
        return _run_output_from_result(invocation, result)

    if decision_kind == CLIAgentDecisionKind.ALLOW_TRACE_PREVIEW:
        packet: RuntimeOCELTracePacket | None = None
        if command_kind == CLIAgentCommandKind.AGENT_TRACE_PREVIEW_FROM_STEP_OUTPUT:
            step_output = context.get("step_output")
            if isinstance(step_output, AgentStepOutput):
                packet = build_runtime_ocel_packet_from_agent_step_output(step_output, default_runtime_ocel_trace_policy())
        elif command_kind == CLIAgentCommandKind.AGENT_TRACE_PREVIEW_FROM_SESSION_SNAPSHOT:
            snapshot = context.get("session_snapshot")
            if isinstance(snapshot, AgentRuntimeSessionSnapshot):
                packet = build_runtime_ocel_packet_from_session_snapshot(snapshot, default_runtime_ocel_trace_policy())
        if packet is None:
            return _run_output_from_denial(
                invocation,
                build_cli_agent_invocation_decision(
                    f"{invocation.invocation_id}:decision:no_trace_artifact",
                    invocation.invocation_id,
                    CLIAgentDecisionKind.BLOCK,
                    "Trace preview requires supplied in-memory step output or session snapshot.",
                    risk_kinds=[CLIAgentRiskKind.PERSISTENT_TRACE_WRITE_RISK],
                ),
            )
        result = build_cli_agent_command_result(
            f"{invocation.invocation_id}:result",
            invocation.invocation_id,
            decision.decision_id,
            command_kind,
            CLIAgentSurfaceStatus.COMPLETED,
            trace_packet_ref=packet.trace_packet_id,
            structured_result={
                "trace_packet_id": packet.trace_packet_id,
                "event_count": len(packet.events),
                "object_count": len(packet.objects),
                "relation_count": len(packet.relations),
                "ready_for_persistent_write": packet.ready_for_persistent_write,
                "ready_for_external_sink": packet.ready_for_external_sink,
            },
            text_summary="CLI command completed through v0.33.7 returned trace packet preview.",
        )
        if not runtime_ocel_packet_is_not_persistence(packet):
            return _run_output_from_denial(invocation, decision)
        return _run_output_from_result(invocation, result)

    return _run_output_from_denial(invocation, decision)


def cli_agent_flags_preserve_unsafe_runtime_false(flags: CLIAgentFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_CLI_FLAG_NAMES)


def cli_invocation_is_not_shell_execution(invocation: CLIAgentInvocation) -> bool:
    return _metadata_flag_true(invocation.metadata, {"shell_execution", "subprocess"}) is False


def cli_decision_preserves_no_external_side_effect(decision: CLIAgentInvocationDecision) -> bool:
    return (
        decision.shell_execution_allowed is False
        and decision.subprocess_allowed is False
        and decision.provider_invocation_allowed is False
        and decision.general_tool_execution_allowed is False
        and decision.workspace_write_allowed is False
        and decision.network_access_allowed is False
        and decision.credential_access_allowed is False
        and decision.persistent_trace_write_allowed is False
    )


def cli_surface_is_not_shell(surface: CLIAgentSurface) -> bool:
    return surface.ready_for_execution is False and surface.policy.allow_shell is False and surface.policy.allow_subprocess is False


def v0338_readiness_report_is_not_general_runtime_ready(report: V0338ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_CLI_FLAG_NAMES)
