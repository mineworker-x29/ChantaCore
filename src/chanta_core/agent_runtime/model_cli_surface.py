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
from .model_backed_step import (
    ModelBackedStepIntegrationMode,
    ModelBackedStepOutput,
    build_model_backed_step_input,
    default_model_backed_step_integration_policy,
    run_model_backed_agent_step,
)
from .model_invocation_trace import (
    ModelInvocationTracePacket,
    build_model_invocation_trace_emission_input,
    build_model_invocation_trace_emitter,
    build_model_invocation_trace_packet_from_model_backed_step_output,
    emit_model_invocation_trace_packet,
    model_invocation_trace_packet_is_not_persistence,
)
from .model_output_quarantine import (
    ModelOutputActionQuarantinePacket,
    build_model_output_action_quarantine_packet_from_candidates,
    extract_model_output_action_candidates_from_response_envelope,
    validate_model_output_action_quarantine_packet,
)
from .model_request import build_model_prompt_payload_ref, build_model_request_envelope
from .model_response import ModelResponseEnvelope, build_model_response_envelope_from_supplied_text
from .step_runner import build_agent_step_runner_mvp


V0348_VERSION = "v0.34.8"
V0348_RELEASE_NAME = "v0.34.8 CLI Model-backed Agent Step Surface"
MAX_CLI_MODEL_BACKED_ARG_CHARS = 12000
MAX_CLI_MODEL_BACKED_RENDERED_OUTPUT_CHARS = 12000

DEFAULT_CLI_MODEL_BACKED_PROHIBITED_ARG_PATTERNS = [
    ";",
    "|",
    "&&",
    "||",
    "`",
    "$(",
    ">",
    "<",
    " secret",
    "token",
    "credential",
    "api_key",
    ".env",
    "id_rsa",
    ".pem",
    "openai",
    "anthropic",
    "ollama",
    "lm studio",
    "opencode",
    "hermes",
    "openclaw",
    "install",
    "write",
    "patch",
]

DEFAULT_V0348_PROHIBITED_UNTIL_LATER_GATE = [
    "shell execution",
    "subprocess execution",
    "command execution",
    "direct provider invocation",
    "provider SDK invocation",
    "direct network access",
    "credential access",
    "secret read",
    "general agent execution",
    "autonomous loop",
    "general tool execution",
    "unquarantined action execution",
    "workspace write",
    "code edit",
    "patch proposal",
    "patch application",
    "reference code execution",
    "reference import",
    "dependency install",
    "raw prompt persistence",
    "raw response persistence",
    "raw model output persistence",
    "general OCEL emission",
    "persistent trace write",
    "external trace sink",
    "UI runtime",
    "external control",
    "authority grant",
]

DEFAULT_V0348_WITHDRAWAL_CONDITIONS = [
    "Any shell, subprocess, command, provider SDK, direct network, credential, secret, write, edit, patch, or persistent trace path is introduced.",
    "Any autonomous runtime, general tool execution, unquarantined action execution, reference execution/import/install, or unsafe readiness flag is introduced.",
    "Any CLI argument is passed to an OS command or used to construct provider endpoints or credential access.",
]


class CLIModelBackedCommandKind(StrEnum):
    MODEL_HELP = "model_help"
    MODEL_STATUS = "model_status"
    MODEL_DRY_RUN = "model_dry_run"
    REQUEST_ENVELOPE_PREVIEW = "request_envelope_preview"
    RESPONSE_SANITIZE_PREVIEW = "response_sanitize_preview"
    RESPONSE_QUARANTINE_PREVIEW = "response_quarantine_preview"
    MODEL_BACKED_ASK_WITH_MOCK_RESPONSE = "model_backed_ask_with_mock_response"
    MODEL_BACKED_ASK_WITH_SUPPLIED_RESPONSE = "model_backed_ask_with_supplied_response"
    MODEL_BACKED_STEP_WITH_MOCK_RESPONSE = "model_backed_step_with_mock_response"
    MODEL_BACKED_STEP_WITH_SUPPLIED_RESPONSE = "model_backed_step_with_supplied_response"
    MODEL_BACKED_STEP_WITH_CONTROLLED_MODEL = "model_backed_step_with_controlled_model"
    MODEL_INVOCATION_TRACE_PREVIEW = "model_invocation_trace_preview"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class CLIModelBackedCommandMode(StrEnum):
    HELP = "help"
    STATUS = "status"
    DRY_RUN = "dry_run"
    PREVIEW = "preview"
    RESPONSE_SANITIZATION = "response_sanitization"
    ACTION_QUARANTINE = "action_quarantine"
    BOUNDED_MODEL_BACKED_STEP = "bounded_model_backed_step"
    CONTROLLED_MODEL_STEP = "controlled_model_step"
    TRACE_PREVIEW = "trace_preview"
    NO_OP = "no_op"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class CLIModelBackedInputSourceKind(StrEnum):
    ARGV_LIST = "argv_list"
    PARSED_ARGS = "parsed_args"
    RUNTIME_CONTEXT = "runtime_context"
    PROMPT_TEXT_ARG = "prompt_text_arg"
    MOCK_RESPONSE_ARG = "mock_response_arg"
    SUPPLIED_RESPONSE_ARG = "supplied_response_arg"
    MODEL_REQUEST_ENVELOPE_REF = "model_request_envelope_ref"
    MODEL_RESPONSE_ENVELOPE_REF = "model_response_envelope_ref"
    QUARANTINE_PACKET_REF = "quarantine_packet_ref"
    MODEL_BACKED_STEP_OUTPUT_REF = "model_backed_step_output_ref"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class CLIModelBackedSurfaceStatus(StrEnum):
    UNKNOWN = "unknown"
    INITIALIZED = "initialized"
    PARSED = "parsed"
    DECISION_READY = "decision_ready"
    ALLOWED = "allowed"
    DENIED = "denied"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    COMPLETED_WITH_WARNINGS = "completed_with_warnings"
    SAFE_FAILED = "safe_failed"
    NO_OP = "no_op"
    FUTURE_GATED = "future_gated"


class CLIModelBackedDecisionKind(StrEnum):
    ALLOW_HELP = "allow_help"
    ALLOW_STATUS = "allow_status"
    ALLOW_DRY_RUN = "allow_dry_run"
    ALLOW_REQUEST_ENVELOPE_PREVIEW = "allow_request_envelope_preview"
    ALLOW_RESPONSE_SANITIZE_PREVIEW = "allow_response_sanitize_preview"
    ALLOW_RESPONSE_QUARANTINE_PREVIEW = "allow_response_quarantine_preview"
    ALLOW_BOUNDED_MODEL_BACKED_STEP_WITH_MOCK_RESPONSE = "allow_bounded_model_backed_step_with_mock_response"
    ALLOW_BOUNDED_MODEL_BACKED_STEP_WITH_SUPPLIED_RESPONSE = "allow_bounded_model_backed_step_with_supplied_response"
    ALLOW_CONTROLLED_MODEL_STEP_VIA_EXISTING_BOUNDARY = "allow_controlled_model_step_via_existing_boundary"
    ALLOW_MODEL_INVOCATION_TRACE_PREVIEW = "allow_model_invocation_trace_preview"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class CLIModelBackedOutputFormat(StrEnum):
    TEXT = "text"
    MARKDOWN = "markdown"
    JSON = "json"
    STRUCTURED_ARTIFACT = "structured_artifact"
    DEBUG_SUMMARY = "debug_summary"
    NO_OUTPUT = "no_output"
    UNKNOWN = "unknown"


class CLIModelBackedRiskKind(StrEnum):
    SHELL_INJECTION_RISK = "shell_injection_risk"
    COMMAND_EXECUTION_RISK = "command_execution_risk"
    DIRECT_PROVIDER_INVOCATION_RISK = "direct_provider_invocation_risk"
    PROVIDER_SDK_BYPASS_RISK = "provider_sdk_bypass_risk"
    DIRECT_NETWORK_ACCESS_RISK = "direct_network_access_risk"
    CREDENTIAL_ACCESS_RISK = "credential_access_risk"
    SECRET_READ_RISK = "secret_read_risk"
    UNBOUNDED_PROMPT_RISK = "unbounded_prompt_risk"
    UNBOUNDED_RESPONSE_RISK = "unbounded_response_risk"
    RAW_PROMPT_PERSISTENCE_RISK = "raw_prompt_persistence_risk"
    RAW_RESPONSE_PERSISTENCE_RISK = "raw_response_persistence_risk"
    UNQUARANTINED_ACTION_EXECUTION_RISK = "unquarantined_action_execution_risk"
    GENERAL_TOOL_EXECUTION_RISK = "general_tool_execution_risk"
    WORKSPACE_WRITE_RISK = "workspace_write_risk"
    CODE_EDIT_RISK = "code_edit_risk"
    PATCH_PROPOSAL_RISK = "patch_proposal_risk"
    PATCH_APPLICATION_RISK = "patch_application_risk"
    REFERENCE_EXECUTION_RISK = "reference_execution_risk"
    EXTERNAL_HARNESS_EXECUTION_RISK = "external_harness_execution_risk"
    PERSISTENT_TRACE_WRITE_RISK = "persistent_trace_write_risk"
    UI_RUNTIME_RISK = "ui_runtime_risk"
    AUTHORITY_GRANT_RISK = "authority_grant_risk"
    UNKNOWN = "unknown"


class CLIModelBackedReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    CLI_CONTRACT_READY = "cli_contract_ready"
    BOUNDED_CLI_MODEL_SURFACE_READY = "bounded_cli_model_surface_ready"
    BOUNDED_MODEL_BACKED_COMMAND_DISPATCH_READY = "bounded_model_backed_command_dispatch_ready"
    DESIGN_HANDOFF_READY_FOR_V0349 = "design_handoff_ready_for_v0349"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


UNSAFE_CLI_MODEL_BACKED_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_direct_provider_invocation",
    "ready_for_provider_invocation",
    "ready_for_provider_sdk_invocation",
    "ready_for_direct_network_access",
    "ready_for_network_access",
    "ready_for_credential_access",
    "ready_for_secret_read",
    "ready_for_general_agent_execution",
    "ready_for_autonomous_agent_runtime",
    "ready_for_general_tool_execution",
    "ready_for_unquarantined_action_execution",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_patch_proposal",
    "ready_for_patch_application",
    "ready_for_registry_mutation",
    "ready_for_memory_mutation",
    "ready_for_raw_prompt_persistence",
    "ready_for_raw_response_persistence",
    "ready_for_raw_model_output_persistence",
    "ready_for_general_ocel_emission",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
)

BOUNDED_STEP_COMMANDS = {
    CLIModelBackedCommandKind.MODEL_BACKED_ASK_WITH_MOCK_RESPONSE,
    CLIModelBackedCommandKind.MODEL_BACKED_ASK_WITH_SUPPLIED_RESPONSE,
    CLIModelBackedCommandKind.MODEL_BACKED_STEP_WITH_MOCK_RESPONSE,
    CLIModelBackedCommandKind.MODEL_BACKED_STEP_WITH_SUPPLIED_RESPONSE,
}


def _validate_version_includes_v0348(version: str) -> None:
    _require_non_blank("version", version)
    if V0348_VERSION not in version:
        raise ValueError("version must include v0.34.8")


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.34.8")


def _validate_true(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not True:
            raise ValueError(f"{name} must always be True in v0.34.8")


def _validate_non_negative(name: str, value: int) -> None:
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be >= 0")


def _validate_enum_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _has_prohibited_text(value: str, patterns: list[str]) -> bool:
    lowered = value.lower()
    return any(pattern.lower() in lowered for pattern in patterns)


def _validate_prohibited_patterns(values: list[str]) -> None:
    _validate_string_list("prohibited_arg_patterns", values)
    lowered = " | ".join(values).lower()
    for required in (";", "|", "&&", "||", "token", "credential", ".env"):
        if required not in lowered:
            raise ValueError("prohibited_arg_patterns missing shell or secret-like pattern")


def _validate_metadata_no_cli_side_effect(metadata: dict[str, Any]) -> None:
    if not isinstance(metadata, dict):
        raise TypeError("metadata must be dict")
    if _metadata_flag_true(
        metadata,
        {
            "shell_execution",
            "subprocess_execution",
            "command_execution",
            "direct_provider_invocation",
            "provider_sdk_invocation",
            "direct_network_access",
            "credential_access",
            "secret_read",
            "general_agent_execution",
            "autonomous_agent_runtime",
            "general_tool_execution",
            "unquarantined_action_execution",
            "workspace_write",
            "code_edit",
            "patch_proposal",
            "patch_application",
            "file_write",
            "persistent_trace_write",
            "external_trace_sink",
            "ui_runtime",
            "authority_grant",
        },
    ):
        raise ValueError("v0.34.8 metadata cannot imply shell, provider, write, persistence, or authority")
    for value in metadata.values():
        if isinstance(value, str) and _has_prohibited_text(value, ["api_key", "token=", "secret=", "credential=", ".env", "id_rsa"]):
            raise ValueError("runtime metadata must not contain credential-like content")


def _bounded_preview(value: Any, max_chars: int = MAX_CLI_MODEL_BACKED_RENDERED_OUTPUT_CHARS) -> tuple[str, bool, bool]:
    if value is None:
        text = ""
    elif isinstance(value, dict):
        text = json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
    else:
        text = str(value)
    redacted = _has_prohibited_text(text, ["api_key", "token=", "secret=", "credential=", "id_rsa", "private key"])
    if redacted:
        text = "[redacted]"
    truncated = len(text) > max_chars
    if truncated:
        text = text[: max(max_chars - 14, 0)] + "...[truncated]"
    return text, redacted, truncated


def _argument_value(argv: list[str], name: str) -> str | None:
    if name not in argv:
        return None
    index = argv.index(name)
    if index + 1 >= len(argv):
        return None
    return argv[index + 1]


def _command_mode_for_kind(command_kind: CLIModelBackedCommandKind | str) -> CLIModelBackedCommandMode:
    kind = CLIModelBackedCommandKind(command_kind)
    if kind == CLIModelBackedCommandKind.MODEL_HELP:
        return CLIModelBackedCommandMode.HELP
    if kind == CLIModelBackedCommandKind.MODEL_STATUS:
        return CLIModelBackedCommandMode.STATUS
    if kind == CLIModelBackedCommandKind.MODEL_DRY_RUN:
        return CLIModelBackedCommandMode.DRY_RUN
    if kind == CLIModelBackedCommandKind.REQUEST_ENVELOPE_PREVIEW:
        return CLIModelBackedCommandMode.PREVIEW
    if kind == CLIModelBackedCommandKind.RESPONSE_SANITIZE_PREVIEW:
        return CLIModelBackedCommandMode.RESPONSE_SANITIZATION
    if kind == CLIModelBackedCommandKind.RESPONSE_QUARANTINE_PREVIEW:
        return CLIModelBackedCommandMode.ACTION_QUARANTINE
    if kind in BOUNDED_STEP_COMMANDS:
        return CLIModelBackedCommandMode.BOUNDED_MODEL_BACKED_STEP
    if kind == CLIModelBackedCommandKind.MODEL_BACKED_STEP_WITH_CONTROLLED_MODEL:
        return CLIModelBackedCommandMode.CONTROLLED_MODEL_STEP
    if kind == CLIModelBackedCommandKind.MODEL_INVOCATION_TRACE_PREVIEW:
        return CLIModelBackedCommandMode.TRACE_PREVIEW
    if kind == CLIModelBackedCommandKind.NO_OP:
        return CLIModelBackedCommandMode.NO_OP
    return CLIModelBackedCommandMode.UNKNOWN


def _kind_from_argv(argv: list[str]) -> CLIModelBackedCommandKind:
    tokens = [str(arg) for arg in argv]
    command = tokens[1] if tokens and tokens[0] == "agent" and len(tokens) > 1 else (tokens[0] if tokens else "")
    if command in {"model-help", "help", "--help", "-h"}:
        return CLIModelBackedCommandKind.MODEL_HELP
    if command == "model-status":
        return CLIModelBackedCommandKind.MODEL_STATUS
    if command == "model-dry-run":
        return CLIModelBackedCommandKind.MODEL_DRY_RUN
    if command == "request-envelope":
        return CLIModelBackedCommandKind.REQUEST_ENVELOPE_PREVIEW
    if command == "sanitize-response":
        return CLIModelBackedCommandKind.RESPONSE_SANITIZE_PREVIEW
    if command == "quarantine-response":
        return CLIModelBackedCommandKind.RESPONSE_QUARANTINE_PREVIEW
    if command == "ask":
        if "--mock-response" in tokens:
            return CLIModelBackedCommandKind.MODEL_BACKED_ASK_WITH_MOCK_RESPONSE
        if "--supplied-response" in tokens:
            return CLIModelBackedCommandKind.MODEL_BACKED_ASK_WITH_SUPPLIED_RESPONSE
    if command == "step" and "--model-backed" in tokens:
        if "--mock-response" in tokens:
            return CLIModelBackedCommandKind.MODEL_BACKED_STEP_WITH_MOCK_RESPONSE
        if "--supplied-response" in tokens:
            return CLIModelBackedCommandKind.MODEL_BACKED_STEP_WITH_SUPPLIED_RESPONSE
    if command == "step" and "--controlled-model" in tokens:
        return CLIModelBackedCommandKind.MODEL_BACKED_STEP_WITH_CONTROLLED_MODEL
    if command == "trace-preview":
        return CLIModelBackedCommandKind.MODEL_INVOCATION_TRACE_PREVIEW
    if command == "no-op":
        return CLIModelBackedCommandKind.NO_OP
    return CLIModelBackedCommandKind.UNKNOWN


@dataclass(frozen=True)
class CLIModelBackedFlagSet:
    flag_set_id: str
    version: str = V0348_VERSION
    cli_model_backed_surface_constructed: bool = False
    cli_argument_parsing_enabled: bool = False
    bounded_model_command_dispatch_enabled: bool = False
    ready_for_v0349_consolidation: bool = False
    ready_for_bounded_cli_model_backed_step: bool = False
    ready_for_cli_model_backed_surface: bool = False
    ready_for_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_bounded_model_backed_step_execution: bool = False
    ready_for_agent_step_runner_model_integration: bool = False
    ready_for_controlled_model_invocation: bool = False
    ready_for_existing_boundary_invocation: bool = False
    ready_for_real_model_invocation: bool = False
    ready_for_model_invocation: bool = False
    ready_for_direct_provider_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_provider_sdk_invocation: bool = False
    ready_for_direct_network_access: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_secret_read: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_unquarantined_action_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_proposal: bool = False
    ready_for_patch_application: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_raw_prompt_persistence: bool = False
    ready_for_raw_response_persistence: bool = False
    ready_for_raw_model_output_persistence: bool = False
    ready_for_model_invocation_trace_packet_creation: bool = False
    ready_for_bounded_model_invocation_ocel_trace_emission: bool = False
    ready_for_general_ocel_emission: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version_includes_v0348(self.version)
        _validate_false(self, UNSAFE_CLI_MODEL_BACKED_FLAG_NAMES)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False in v0.34.8")
        _validate_metadata_no_cli_side_effect(self.metadata)


@dataclass(frozen=True)
class CLIModelBackedSourceRef:
    source_ref_id: str
    source_kind: CLIModelBackedInputSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        CLIModelBackedInputSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_cli_side_effect(self.metadata)

    @property
    def shell_command(self) -> bool:
        return False

    @property
    def provider_call(self) -> bool:
        return False

    @property
    def file_read(self) -> bool:
        return False

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class CLIModelBackedArgumentSpec:
    argument_spec_id: str
    name: str
    required: bool = False
    allowed_values: list[str] = field(default_factory=list)
    prohibited_values: list[str] = field(default_factory=list)
    allow_prompt_text: bool = False
    allow_response_text: bool = False
    allow_json_value: bool = False
    max_value_chars: int = MAX_CLI_MODEL_BACKED_ARG_CHARS
    description: str = "Bounded CLI model-backed argument."
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("argument_spec_id", self.argument_spec_id)
        _require_non_blank("name", self.name)
        _validate_string_list("allowed_values", self.allowed_values)
        _validate_string_list("prohibited_values", self.prohibited_values)
        _validate_non_negative("max_value_chars", self.max_value_chars)
        _require_non_blank("description", self.description)
        _validate_metadata_no_cli_side_effect(self.metadata)


@dataclass(frozen=True)
class CLIModelBackedCommandSpec:
    command_spec_id: str
    command_kind: CLIModelBackedCommandKind | str
    command_mode: CLIModelBackedCommandMode | str
    command_name: str
    description: str
    argument_specs: list[CLIModelBackedArgumentSpec] = field(default_factory=list)
    allowed_output_formats: list[CLIModelBackedOutputFormat | str] = field(default_factory=lambda: [CLIModelBackedOutputFormat.TEXT, CLIModelBackedOutputFormat.JSON, CLIModelBackedOutputFormat.STRUCTURED_ARTIFACT])
    allowed_decisions: list[CLIModelBackedDecisionKind | str] = field(default_factory=list)
    risk_kinds: list[CLIModelBackedRiskKind | str] = field(default_factory=list)
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("command_spec_id", self.command_spec_id)
        kind = CLIModelBackedCommandKind(self.command_kind)
        CLIModelBackedCommandMode(self.command_mode)
        _require_non_blank("command_name", self.command_name)
        _require_non_blank("description", self.description)
        _validate_object_list("argument_specs", self.argument_specs, CLIModelBackedArgumentSpec)
        _validate_enum_list("allowed_output_formats", self.allowed_output_formats, CLIModelBackedOutputFormat)
        _validate_enum_list("allowed_decisions", self.allowed_decisions, CLIModelBackedDecisionKind)
        _validate_enum_list("risk_kinds", self.risk_kinds, CLIModelBackedRiskKind)
        if self.enabled and kind == CLIModelBackedCommandKind.UNKNOWN:
            raise ValueError("unknown command spec cannot be enabled")
        _validate_metadata_no_cli_side_effect(self.metadata)

    @property
    def os_command(self) -> bool:
        return False


@dataclass(frozen=True)
class CLIModelBackedSurfacePolicy:
    policy_id: str
    allowed_command_kinds: list[CLIModelBackedCommandKind | str] = field(default_factory=list)
    blocked_command_kinds: list[CLIModelBackedCommandKind | str] = field(default_factory=lambda: [CLIModelBackedCommandKind.UNKNOWN])
    allowed_output_formats: list[CLIModelBackedOutputFormat | str] = field(default_factory=lambda: [CLIModelBackedOutputFormat.TEXT, CLIModelBackedOutputFormat.JSON, CLIModelBackedOutputFormat.MARKDOWN, CLIModelBackedOutputFormat.STRUCTURED_ARTIFACT])
    prohibited_arg_patterns: list[str] = field(default_factory=lambda: list(DEFAULT_CLI_MODEL_BACKED_PROHIBITED_ARG_PATTERNS))
    max_arg_chars: int = MAX_CLI_MODEL_BACKED_ARG_CHARS
    allow_shell: bool = False
    allow_subprocess: bool = False
    allow_command_execution: bool = False
    allow_direct_provider_invocation: bool = False
    allow_provider_sdk_invocation: bool = False
    allow_direct_network_access: bool = False
    allow_credential_access: bool = False
    allow_secret_read: bool = False
    allow_bounded_model_backed_step: bool = True
    allow_controlled_model_step_via_existing_boundary: bool = True
    allow_general_agent_execution: bool = False
    allow_autonomous_agent_runtime: bool = False
    allow_general_tool_execution: bool = False
    allow_unquarantined_action_execution: bool = False
    allow_workspace_write: bool = False
    allow_code_edit: bool = False
    allow_patch_proposal: bool = False
    allow_patch_application: bool = False
    allow_model_invocation_trace_preview: bool = True
    allow_persistent_trace_write: bool = False
    allow_ui_runtime: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_id", self.policy_id)
        _validate_enum_list("allowed_command_kinds", self.allowed_command_kinds, CLIModelBackedCommandKind)
        _validate_enum_list("blocked_command_kinds", self.blocked_command_kinds, CLIModelBackedCommandKind)
        _validate_enum_list("allowed_output_formats", self.allowed_output_formats, CLIModelBackedOutputFormat)
        _validate_prohibited_patterns(self.prohibited_arg_patterns)
        _validate_non_negative("max_arg_chars", self.max_arg_chars)
        _validate_false(
            self,
            (
                "allow_shell",
                "allow_subprocess",
                "allow_command_execution",
                "allow_direct_provider_invocation",
                "allow_provider_sdk_invocation",
                "allow_direct_network_access",
                "allow_credential_access",
                "allow_secret_read",
                "allow_general_agent_execution",
                "allow_autonomous_agent_runtime",
                "allow_general_tool_execution",
                "allow_unquarantined_action_execution",
                "allow_workspace_write",
                "allow_code_edit",
                "allow_patch_proposal",
                "allow_patch_application",
                "allow_persistent_trace_write",
                "allow_ui_runtime",
            ),
        )
        _validate_metadata_no_cli_side_effect(self.metadata)


@dataclass(frozen=True)
class CLIModelBackedSurface:
    cli_surface_id: str
    version: str
    command_specs: list[CLIModelBackedCommandSpec]
    policy: CLIModelBackedSurfacePolicy
    flags: CLIModelBackedFlagSet
    status: CLIModelBackedSurfaceStatus | str
    readiness_level: CLIModelBackedReadinessLevel | str
    summary: str
    ready_for_bounded_cli_model_backed_step: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("cli_surface_id", self.cli_surface_id)
        _validate_version_includes_v0348(self.version)
        _validate_object_list("command_specs", self.command_specs, CLIModelBackedCommandSpec)
        if not isinstance(self.policy, CLIModelBackedSurfacePolicy):
            raise TypeError("policy must be CLIModelBackedSurfacePolicy")
        if not isinstance(self.flags, CLIModelBackedFlagSet):
            raise TypeError("flags must be CLIModelBackedFlagSet")
        CLIModelBackedSurfaceStatus(self.status)
        CLIModelBackedReadinessLevel(self.readiness_level)
        _require_non_blank("summary", self.summary)
        if not cli_model_backed_flags_preserve_unsafe_false(self.flags):
            raise ValueError("flags must preserve unsafe readiness false")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.34.8")
        _validate_metadata_no_cli_side_effect(self.metadata)


@dataclass(frozen=True)
class CLIModelBackedInvocation:
    invocation_id: str
    argv: list[str]
    command_kind: CLIModelBackedCommandKind | str
    command_mode: CLIModelBackedCommandMode | str
    parsed_args: dict[str, Any]
    requested_output_format: CLIModelBackedOutputFormat | str
    source_refs: list[CLIModelBackedSourceRef]
    invocation_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("invocation_id", self.invocation_id)
        if not isinstance(self.argv, list) or not all(isinstance(item, str) for item in self.argv):
            raise TypeError("argv must be list[str]")
        CLIModelBackedCommandKind(self.command_kind)
        CLIModelBackedCommandMode(self.command_mode)
        if not isinstance(self.parsed_args, dict):
            raise TypeError("parsed_args must be dict")
        CLIModelBackedOutputFormat(self.requested_output_format)
        _validate_object_list("source_refs", self.source_refs, CLIModelBackedSourceRef)
        _require_non_blank("invocation_summary", self.invocation_summary)
        _validate_metadata_no_cli_side_effect(self.metadata)


@dataclass(frozen=True)
class CLIModelBackedInvocationDecision:
    decision_id: str
    invocation_id: str
    decision_kind: CLIModelBackedDecisionKind | str
    reason: str
    risk_kinds: list[CLIModelBackedRiskKind | str] = field(default_factory=list)
    allowed_command_kind: CLIModelBackedCommandKind | str | None = None
    bounded_model_backed_step_allowed: bool = False
    controlled_model_step_via_existing_boundary_allowed: bool = False
    model_invocation_trace_preview_allowed: bool = False
    shell_execution_allowed: bool = False
    subprocess_allowed: bool = False
    command_execution_allowed: bool = False
    direct_provider_invocation_allowed: bool = False
    provider_sdk_allowed: bool = False
    direct_network_allowed: bool = False
    credential_access_allowed: bool = False
    secret_read_allowed: bool = False
    general_tool_execution_allowed: bool = False
    unquarantined_action_execution_allowed: bool = False
    workspace_write_allowed: bool = False
    code_edit_allowed: bool = False
    patch_proposal_allowed: bool = False
    patch_application_allowed: bool = False
    persistent_trace_write_allowed: bool = False
    ui_runtime_allowed: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("decision_id", self.decision_id)
        _require_non_blank("invocation_id", self.invocation_id)
        CLIModelBackedDecisionKind(self.decision_kind)
        _require_non_blank("reason", self.reason)
        _validate_enum_list("risk_kinds", self.risk_kinds, CLIModelBackedRiskKind)
        if self.allowed_command_kind is not None:
            CLIModelBackedCommandKind(self.allowed_command_kind)
        _validate_false(
            self,
            (
                "shell_execution_allowed",
                "subprocess_allowed",
                "command_execution_allowed",
                "direct_provider_invocation_allowed",
                "provider_sdk_allowed",
                "direct_network_allowed",
                "credential_access_allowed",
                "secret_read_allowed",
                "general_tool_execution_allowed",
                "unquarantined_action_execution_allowed",
                "workspace_write_allowed",
                "code_edit_allowed",
                "patch_proposal_allowed",
                "patch_application_allowed",
                "persistent_trace_write_allowed",
                "ui_runtime_allowed",
            ),
        )
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_cli_side_effect(self.metadata)


@dataclass(frozen=True)
class CLIModelBackedDeniedCommand:
    denied_command_id: str
    invocation_id: str | None = None
    decision_id: str | None = None
    command_kind: CLIModelBackedCommandKind | str = CLIModelBackedCommandKind.UNKNOWN
    risk_kinds: list[CLIModelBackedRiskKind | str] = field(default_factory=list)
    reason: str = "CLI model-backed command denied safely."
    safe_alternatives: list[str] = field(default_factory=lambda: ["agent model-help", "agent model-status", "agent no-op"])
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("denied_command_id", self.denied_command_id)
        CLIModelBackedCommandKind(self.command_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, CLIModelBackedRiskKind)
        _require_non_blank("reason", self.reason)
        _validate_string_list("safe_alternatives", self.safe_alternatives)
        _validate_metadata_no_cli_side_effect(self.metadata)


@dataclass(frozen=True)
class CLIModelBackedRuntimeContext:
    runtime_context_id: str
    has_model_backed_step_runner: bool = False
    has_existing_provider_boundary_adapter: bool = False
    has_provider_boundary_callable: bool = False
    has_model_invocation_trace_emitter: bool = False
    has_workspace_policy: bool = False
    context_summary: str = "Bounded in-memory runtime context refs only."
    allows_controlled_model_step: bool = False
    allows_direct_provider: bool = False
    allows_shell: bool = False
    allows_write: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("runtime_context_id", self.runtime_context_id)
        _require_non_blank("context_summary", self.context_summary)
        if self.allows_controlled_model_step and not (
            self.has_model_backed_step_runner and self.has_existing_provider_boundary_adapter and self.has_provider_boundary_callable
        ):
            raise ValueError("controlled model step requires v0.34.6 runner and v0.34.4 adapter/callable refs")
        _validate_false(self, ("allows_direct_provider", "allows_shell", "allows_write"))
        _validate_metadata_no_cli_side_effect(self.metadata)


@dataclass(frozen=True)
class CLIModelBackedCommandResult:
    command_result_id: str
    invocation_id: str
    decision_id: str
    command_kind: CLIModelBackedCommandKind | str
    status: CLIModelBackedSurfaceStatus | str
    request_envelope_ref: str | None = None
    response_envelope_ref: str | None = None
    quarantine_packet_ref: str | None = None
    model_backed_step_output_ref: str | None = None
    trace_packet_ref: str | None = None
    structured_result: dict[str, Any] = field(default_factory=dict)
    text_summary: str = "CLI model-backed command result."
    redacted: bool = True
    truncated: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("command_result_id", "invocation_id", "decision_id", "text_summary"):
            _require_non_blank(name, getattr(self, name))
        CLIModelBackedCommandKind(self.command_kind)
        CLIModelBackedSurfaceStatus(self.status)
        if not isinstance(self.structured_result, dict):
            raise TypeError("structured_result must be dict")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.34.8")
        rendered, redacted, truncated = _bounded_preview(self.structured_result or self.text_summary)
        if rendered == "[redacted]" and not (self.redacted or redacted):
            raise ValueError("secret-like result must be redacted")
        if truncated and not self.truncated:
            raise ValueError("truncated result must be marked truncated")
        _validate_metadata_no_cli_side_effect(self.metadata)


@dataclass(frozen=True)
class CLIModelBackedRunOutput:
    run_output_id: str
    invocation_id: str
    command_result: CLIModelBackedCommandResult | None
    denied_command: CLIModelBackedDeniedCommand | None
    rendered_output: str
    output_format: CLIModelBackedOutputFormat | str
    status: CLIModelBackedSurfaceStatus | str
    summary: str
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("run_output_id", "invocation_id", "rendered_output", "summary"):
            _require_non_blank(name, getattr(self, name))
        if self.command_result is not None and not isinstance(self.command_result, CLIModelBackedCommandResult):
            raise TypeError("command_result must be CLIModelBackedCommandResult or None")
        if self.denied_command is not None and not isinstance(self.denied_command, CLIModelBackedDeniedCommand):
            raise TypeError("denied_command must be CLIModelBackedDeniedCommand or None")
        CLIModelBackedOutputFormat(self.output_format)
        CLIModelBackedSurfaceStatus(self.status)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.34.8")
        if len(self.rendered_output) > self.metadata.get("max_rendered_output_chars", MAX_CLI_MODEL_BACKED_RENDERED_OUTPUT_CHARS):
            raise ValueError("rendered_output must be bounded")
        _validate_metadata_no_cli_side_effect(self.metadata)


@dataclass(frozen=True)
class CLIModelBackedRunReport:
    report_id: str
    version: str
    invocation_id: str | None = None
    run_output_id: str | None = None
    status: CLIModelBackedSurfaceStatus | str = CLIModelBackedSurfaceStatus.COMPLETED
    readiness_level: CLIModelBackedReadinessLevel | str = CLIModelBackedReadinessLevel.BOUNDED_CLI_MODEL_SURFACE_READY
    summary: str = "v0.34.8 CLI model-backed run report; not persistent log."
    command_count: int = 0
    allowed_count: int = 0
    denied_count: int = 0
    blocked_count: int = 0
    bounded_model_step_count: int = 0
    trace_preview_count: int = 0
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0349_consolidation: bool = False
    ready_for_bounded_cli_model_backed_step: bool = False
    ready_for_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_direct_provider_invocation: bool = False
    ready_for_provider_sdk_invocation: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_persistent_trace_write: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=lambda: list(DEFAULT_V0348_WITHDRAWAL_CONDITIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0348(self.version)
        CLIModelBackedSurfaceStatus(self.status)
        CLIModelBackedReadinessLevel(self.readiness_level)
        _require_non_blank("summary", self.summary)
        for name in ("command_count", "allowed_count", "denied_count", "blocked_count", "bounded_model_step_count", "trace_preview_count"):
            _validate_non_negative(name, getattr(self, name))
        for name in ("completed_items", "blocked_items", "future_track_items", "gaps", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(
            self,
            (
                "ready_for_execution",
                "ready_for_shell_execution",
                "ready_for_direct_provider_invocation",
                "ready_for_provider_sdk_invocation",
                "ready_for_general_agent_execution",
                "ready_for_general_tool_execution",
                "ready_for_persistent_trace_write",
            ),
        )
        _validate_metadata_no_cli_side_effect(self.metadata)


@dataclass(frozen=True)
class CLIModelBackedRunPreview:
    run_preview_id: str
    cli_surface_id: str | None = None
    planned_steps: list[str] = field(default_factory=lambda: ["parse argv", "evaluate policy", "dispatch bounded helper only"])
    expected_artifacts: list[str] = field(default_factory=lambda: ["CLIModelBackedInvocation", "CLIModelBackedRunOutput"])
    explicitly_not_performed: list[str] = field(default_factory=lambda: list(DEFAULT_V0348_PROHIBITED_UNTIL_LATER_GATE))
    no_shell_execution_guarantee: bool = True
    no_subprocess_guarantee: bool = True
    no_command_execution_guarantee: bool = True
    no_direct_provider_invocation_guarantee: bool = True
    no_provider_sdk_invocation_guarantee: bool = True
    no_direct_network_access_guarantee: bool = True
    no_credential_access_guarantee: bool = True
    no_secret_read_guarantee: bool = True
    no_general_agent_execution_guarantee: bool = True
    no_autonomous_agent_runtime_guarantee: bool = True
    no_general_tool_execution_guarantee: bool = True
    no_unquarantined_action_execution_guarantee: bool = True
    no_workspace_write_guarantee: bool = True
    no_code_edit_guarantee: bool = True
    no_patch_proposal_guarantee: bool = True
    no_patch_application_guarantee: bool = True
    no_reference_code_execution_guarantee: bool = True
    no_reference_import_guarantee: bool = True
    no_reference_dependency_install_guarantee: bool = True
    no_raw_prompt_persistence_guarantee: bool = True
    no_raw_response_persistence_guarantee: bool = True
    no_persistent_trace_write_guarantee: bool = True
    no_ui_runtime_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        _validate_true(self, tuple(name for name in self.__dataclass_fields__ if name.startswith("no_")))
        _validate_metadata_no_cli_side_effect(self.metadata)


@dataclass(frozen=True)
class CLIModelBackedNoExternalSideEffectGuarantee:
    guarantee_id: str
    version: str
    no_shell_execution: bool = True
    no_subprocess: bool = True
    no_command_execution: bool = True
    no_direct_provider_invocation: bool = True
    no_provider_sdk_invocation: bool = True
    no_direct_network_access: bool = True
    no_credential_access: bool = True
    no_secret_read: bool = True
    no_general_agent_execution: bool = True
    no_autonomous_agent_runtime: bool = True
    no_general_tool_execution: bool = True
    no_unquarantined_action_execution: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_patch_proposal: bool = True
    no_patch_application: bool = True
    no_file_creation: bool = True
    no_file_deletion: bool = True
    no_file_rename: bool = True
    no_chmod_chown: bool = True
    no_reference_code_execution: bool = True
    no_reference_import: bool = True
    no_reference_dependency_install: bool = True
    no_registry_mutation: bool = True
    no_memory_mutation: bool = True
    no_raw_prompt_persistence: bool = True
    no_raw_response_persistence: bool = True
    no_persistent_trace_write: bool = True
    no_external_trace_sink: bool = True
    no_ui_runtime: bool = True
    no_external_control: bool = True
    no_authority_grant: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version_includes_v0348(self.version)
        _validate_true(self, tuple(name for name in self.__dataclass_fields__ if name.startswith("no_")))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_cli_side_effect(self.metadata)


@dataclass(frozen=True)
class V0348ReadinessReport:
    report_id: str
    version: str
    cli_surface_id: str | None = None
    cli_run_report_id: str | None = None
    run_output_id: str | None = None
    summary: str = "v0.34.8 CLI Model-backed Agent Step Surface readiness; not general execution."
    ready_for_v0349_consolidation: bool = False
    ready_for_bounded_cli_model_backed_step: bool = True
    ready_for_cli_model_backed_surface: bool = True
    ready_for_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_bounded_model_backed_step_execution: bool = True
    ready_for_agent_step_runner_model_integration: bool = True
    ready_for_controlled_model_invocation: bool = True
    ready_for_existing_boundary_invocation: bool = True
    ready_for_real_model_invocation: bool = True
    ready_for_model_invocation: bool = True
    ready_for_direct_provider_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_provider_sdk_invocation: bool = False
    ready_for_direct_network_access: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_secret_read: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_unquarantined_action_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_proposal: bool = False
    ready_for_patch_application: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_raw_prompt_persistence: bool = False
    ready_for_raw_response_persistence: bool = False
    ready_for_raw_model_output_persistence: bool = False
    ready_for_model_invocation_trace_packet_creation: bool = True
    ready_for_bounded_model_invocation_ocel_trace_emission: bool = True
    ready_for_general_ocel_emission: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    completed_items: list[str] = field(default_factory=lambda: ["CLI model-backed surface", "safe parser", "bounded dispatch"])
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=lambda: ["v0.34.9 consolidation"])
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_V0348_PROHIBITED_UNTIL_LATER_GATE))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=lambda: list(DEFAULT_V0348_WITHDRAWAL_CONDITIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0348(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(self, UNSAFE_CLI_MODEL_BACKED_FLAG_NAMES)
        for name in ("completed_items", "blocked_items", "future_track_items", "prohibited_until_later_gate", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_metadata_no_cli_side_effect(self.metadata)


def build_cli_model_backed_flags(flag_set_id: str = "cli_model_backed_flags:v0.34.8", **kwargs: Any) -> CLIModelBackedFlagSet:
    return CLIModelBackedFlagSet(flag_set_id=flag_set_id, version=kwargs.pop("version", V0348_VERSION), **kwargs)


def build_cli_model_backed_source_ref(source_ref_id: str = "cli_model_backed_source_ref:v0.34.8", **kwargs: Any) -> CLIModelBackedSourceRef:
    return CLIModelBackedSourceRef(
        source_ref_id=source_ref_id,
        source_kind=kwargs.pop("source_kind", CLIModelBackedInputSourceKind.TEST_FIXTURE),
        source_id=kwargs.pop("source_id", "test_fixture"),
        source_summary=kwargs.pop("source_summary", "CLI model-backed source ref metadata only."),
        **kwargs,
    )


def build_cli_model_backed_argument_spec(argument_spec_id: str, name: str, **kwargs: Any) -> CLIModelBackedArgumentSpec:
    return CLIModelBackedArgumentSpec(argument_spec_id=argument_spec_id, name=name, **kwargs)


def build_cli_model_backed_command_spec(command_spec_id: str, command_kind: CLIModelBackedCommandKind | str, command_name: str, **kwargs: Any) -> CLIModelBackedCommandSpec:
    return CLIModelBackedCommandSpec(
        command_spec_id=command_spec_id,
        command_kind=command_kind,
        command_mode=kwargs.pop("command_mode", _command_mode_for_kind(command_kind)),
        command_name=command_name,
        description=kwargs.pop("description", "Bounded CLI model-backed command."),
        **kwargs,
    )


def build_cli_model_backed_surface_policy(policy_id: str = "cli_model_backed_surface_policy:v0.34.8", **kwargs: Any) -> CLIModelBackedSurfacePolicy:
    return CLIModelBackedSurfacePolicy(policy_id=policy_id, **kwargs)


def default_cli_model_backed_surface_policy(**kwargs: Any) -> CLIModelBackedSurfacePolicy:
    return build_cli_model_backed_surface_policy(
        allowed_command_kinds=kwargs.pop("allowed_command_kinds", [kind for kind in CLIModelBackedCommandKind if kind != CLIModelBackedCommandKind.UNKNOWN]),
        **kwargs,
    )


def default_cli_model_backed_command_specs() -> list[CLIModelBackedCommandSpec]:
    return [
        build_cli_model_backed_command_spec(f"command:{kind.value}:v0.34.8", kind, kind.value)
        for kind in CLIModelBackedCommandKind
        if kind != CLIModelBackedCommandKind.UNKNOWN
    ]


def build_cli_model_backed_surface(cli_surface_id: str = "cli_model_backed_surface:v0.34.8", **kwargs: Any) -> CLIModelBackedSurface:
    return CLIModelBackedSurface(
        cli_surface_id=cli_surface_id,
        version=kwargs.pop("version", V0348_VERSION),
        command_specs=kwargs.pop("command_specs", default_cli_model_backed_command_specs()),
        policy=kwargs.pop("policy", default_cli_model_backed_surface_policy()),
        flags=kwargs.pop(
            "flags",
            build_cli_model_backed_flags(
                cli_model_backed_surface_constructed=True,
                cli_argument_parsing_enabled=True,
                bounded_model_command_dispatch_enabled=True,
                ready_for_bounded_cli_model_backed_step=True,
                ready_for_cli_model_backed_surface=True,
                ready_for_bounded_model_backed_step_execution=True,
                ready_for_agent_step_runner_model_integration=True,
                ready_for_model_invocation_trace_packet_creation=True,
                ready_for_bounded_model_invocation_ocel_trace_emission=True,
            ),
        ),
        status=kwargs.pop("status", CLIModelBackedSurfaceStatus.INITIALIZED),
        readiness_level=kwargs.pop("readiness_level", CLIModelBackedReadinessLevel.BOUNDED_CLI_MODEL_SURFACE_READY),
        summary=kwargs.pop("summary", "v0.34.8 bounded CLI model-backed surface; not shell."),
        ready_for_bounded_cli_model_backed_step=kwargs.pop("ready_for_bounded_cli_model_backed_step", True),
        **kwargs,
    )


def build_default_cli_model_backed_surface(**kwargs: Any) -> CLIModelBackedSurface:
    return build_cli_model_backed_surface(**kwargs)


def build_cli_model_backed_invocation(invocation_id: str, argv: list[str], command_kind: CLIModelBackedCommandKind | str, **kwargs: Any) -> CLIModelBackedInvocation:
    return CLIModelBackedInvocation(
        invocation_id=invocation_id,
        argv=argv,
        command_kind=command_kind,
        command_mode=kwargs.pop("command_mode", _command_mode_for_kind(command_kind)),
        parsed_args=kwargs.pop("parsed_args", {}),
        requested_output_format=kwargs.pop("requested_output_format", CLIModelBackedOutputFormat.TEXT),
        source_refs=kwargs.pop("source_refs", []),
        invocation_summary=kwargs.pop("invocation_summary", "Parsed CLI model-backed invocation; not shell."),
        **kwargs,
    )


def build_cli_model_backed_invocation_decision(decision_id: str, invocation_id: str, decision_kind: CLIModelBackedDecisionKind | str, reason: str, **kwargs: Any) -> CLIModelBackedInvocationDecision:
    return CLIModelBackedInvocationDecision(decision_id=decision_id, invocation_id=invocation_id, decision_kind=decision_kind, reason=reason, **kwargs)


def build_cli_model_backed_denied_command(denied_command_id: str, **kwargs: Any) -> CLIModelBackedDeniedCommand:
    return CLIModelBackedDeniedCommand(denied_command_id=denied_command_id, **kwargs)


def build_cli_model_backed_runtime_context(runtime_context_id: str = "cli_model_backed_runtime_context:v0.34.8", **kwargs: Any) -> CLIModelBackedRuntimeContext:
    return CLIModelBackedRuntimeContext(runtime_context_id=runtime_context_id, **kwargs)


def build_cli_model_backed_command_result(command_result_id: str, invocation_id: str, decision_id: str, command_kind: CLIModelBackedCommandKind | str, status: CLIModelBackedSurfaceStatus | str, **kwargs: Any) -> CLIModelBackedCommandResult:
    return CLIModelBackedCommandResult(command_result_id=command_result_id, invocation_id=invocation_id, decision_id=decision_id, command_kind=command_kind, status=status, **kwargs)


def build_cli_model_backed_run_output(run_output_id: str, invocation_id: str, rendered_output: str, status: CLIModelBackedSurfaceStatus | str, **kwargs: Any) -> CLIModelBackedRunOutput:
    return CLIModelBackedRunOutput(run_output_id=run_output_id, invocation_id=invocation_id, rendered_output=rendered_output, status=status, **kwargs)


def build_cli_model_backed_run_report(report_id: str = "cli_model_backed_run_report:v0.34.8", **kwargs: Any) -> CLIModelBackedRunReport:
    return CLIModelBackedRunReport(report_id=report_id, version=kwargs.pop("version", V0348_VERSION), **kwargs)


def build_cli_model_backed_run_preview(run_preview_id: str = "cli_model_backed_run_preview:v0.34.8", **kwargs: Any) -> CLIModelBackedRunPreview:
    return CLIModelBackedRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_cli_model_backed_no_external_side_effect_guarantee(guarantee_id: str = "cli_model_backed_no_external_side_effect_guarantee:v0.34.8", **kwargs: Any) -> CLIModelBackedNoExternalSideEffectGuarantee:
    return CLIModelBackedNoExternalSideEffectGuarantee(guarantee_id=guarantee_id, version=kwargs.pop("version", V0348_VERSION), **kwargs)


def build_v0348_readiness_report(report_id: str = "v0348_readiness_report", **kwargs: Any) -> V0348ReadinessReport:
    return V0348ReadinessReport(report_id=report_id, version=kwargs.pop("version", V0348_VERSION), **kwargs)


def parse_cli_model_backed_invocation(argv: list[str], surface: CLIModelBackedSurface | None = None) -> CLIModelBackedInvocation:
    if not isinstance(argv, list) or not all(isinstance(arg, str) for arg in argv):
        raise TypeError("argv must be list[str]")
    surface = surface or build_default_cli_model_backed_surface()
    kind = _kind_from_argv(argv)
    fmt = CLIModelBackedOutputFormat.JSON if _argument_value(argv, "--format") == "json" else CLIModelBackedOutputFormat.TEXT
    parsed: dict[str, Any] = {"argv_count": len(argv), "command_token": argv[1] if len(argv) > 1 and argv[0] == "agent" else (argv[0] if argv else "")}
    for arg_name, key in (
        ("--prompt", "prompt"),
        ("--response", "response"),
        ("--mock-response", "mock_response"),
        ("--supplied-response", "supplied_response"),
        ("--format", "format"),
    ):
        value = _argument_value(argv, arg_name)
        if value is not None:
            parsed[key] = value
    source_refs = [
        build_cli_model_backed_source_ref(
            "source:argv:v0.34.8",
            source_kind=CLIModelBackedInputSourceKind.ARGV_LIST,
            source_id="argv",
            source_summary="CLI argv list parsed in memory; not shell.",
        )
    ]
    return build_cli_model_backed_invocation(
        f"cli_model_backed_invocation:{abs(hash(tuple(argv))) % 1000000}",
        list(argv),
        kind,
        parsed_args=parsed,
        requested_output_format=fmt,
        source_refs=source_refs,
    )


def _unsafe_arg_risks(invocation: CLIModelBackedInvocation, surface: CLIModelBackedSurface) -> list[CLIModelBackedRiskKind]:
    risks: list[CLIModelBackedRiskKind] = []
    joined = " ".join(invocation.argv).lower()
    if _has_prohibited_text(joined, surface.policy.prohibited_arg_patterns):
        risks.append(CLIModelBackedRiskKind.SHELL_INJECTION_RISK)
    for value in invocation.parsed_args.values():
        if isinstance(value, str) and len(value) > surface.policy.max_arg_chars:
            if "prompt" in invocation.parsed_args and invocation.parsed_args.get("prompt") == value:
                risks.append(CLIModelBackedRiskKind.UNBOUNDED_PROMPT_RISK)
            else:
                risks.append(CLIModelBackedRiskKind.UNBOUNDED_RESPONSE_RISK)
    risk_words = {
        "provider": CLIModelBackedRiskKind.DIRECT_PROVIDER_INVOCATION_RISK,
        "sdk": CLIModelBackedRiskKind.PROVIDER_SDK_BYPASS_RISK,
        "network": CLIModelBackedRiskKind.DIRECT_NETWORK_ACCESS_RISK,
        "credential": CLIModelBackedRiskKind.CREDENTIAL_ACCESS_RISK,
        "secret": CLIModelBackedRiskKind.SECRET_READ_RISK,
        "tool": CLIModelBackedRiskKind.GENERAL_TOOL_EXECUTION_RISK,
        "write": CLIModelBackedRiskKind.WORKSPACE_WRITE_RISK,
        "edit": CLIModelBackedRiskKind.CODE_EDIT_RISK,
        "patch": CLIModelBackedRiskKind.PATCH_PROPOSAL_RISK,
        "install": CLIModelBackedRiskKind.REFERENCE_EXECUTION_RISK,
        "opencode": CLIModelBackedRiskKind.REFERENCE_EXECUTION_RISK,
        "hermes": CLIModelBackedRiskKind.REFERENCE_EXECUTION_RISK,
        "openclaw": CLIModelBackedRiskKind.REFERENCE_EXECUTION_RISK,
    }
    for word, risk in risk_words.items():
        if word in joined:
            risks.append(risk)
    return list(dict.fromkeys(risks))


def _context_get(runtime_context: CLIModelBackedRuntimeContext | dict[str, Any] | None, key: str) -> Any:
    if isinstance(runtime_context, CLIModelBackedRuntimeContext):
        return runtime_context.metadata.get(key)
    if isinstance(runtime_context, dict):
        return runtime_context.get(key)
    return None


def evaluate_cli_model_backed_invocation(
    invocation: CLIModelBackedInvocation,
    surface: CLIModelBackedSurface,
    runtime_context: CLIModelBackedRuntimeContext | dict[str, Any] | None = None,
) -> CLIModelBackedInvocationDecision:
    if not isinstance(invocation, CLIModelBackedInvocation):
        raise TypeError("invocation must be CLIModelBackedInvocation")
    if not isinstance(surface, CLIModelBackedSurface):
        raise TypeError("surface must be CLIModelBackedSurface")
    kind = CLIModelBackedCommandKind(invocation.command_kind)
    risks = _unsafe_arg_risks(invocation, surface)
    if kind == CLIModelBackedCommandKind.UNKNOWN or kind in surface.policy.blocked_command_kinds or risks:
        return build_cli_model_backed_invocation_decision(
            f"{invocation.invocation_id}:decision",
            invocation.invocation_id,
            CLIModelBackedDecisionKind.BLOCK,
            "Unknown, shell-like, provider-like, write-like, reference, or otherwise unsafe CLI model command was blocked.",
            risk_kinds=risks or [CLIModelBackedRiskKind.UNKNOWN],
            allowed_command_kind=None,
        )
    if kind not in surface.policy.allowed_command_kinds:
        return build_cli_model_backed_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIModelBackedDecisionKind.DENY, "Command is not enabled by v0.34.8 policy.", risk_kinds=[CLIModelBackedRiskKind.UNKNOWN])
    if kind == CLIModelBackedCommandKind.MODEL_HELP:
        return build_cli_model_backed_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIModelBackedDecisionKind.ALLOW_HELP, "Help output is bounded metadata only.", allowed_command_kind=kind)
    if kind == CLIModelBackedCommandKind.MODEL_STATUS:
        return build_cli_model_backed_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIModelBackedDecisionKind.ALLOW_STATUS, "Status output is bounded metadata only.", allowed_command_kind=kind)
    if kind == CLIModelBackedCommandKind.MODEL_DRY_RUN:
        return build_cli_model_backed_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIModelBackedDecisionKind.ALLOW_DRY_RUN, "Dry-run output is bounded metadata only.", allowed_command_kind=kind)
    if kind == CLIModelBackedCommandKind.REQUEST_ENVELOPE_PREVIEW:
        if "prompt" not in invocation.parsed_args:
            return build_cli_model_backed_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIModelBackedDecisionKind.DENY, "Request envelope preview requires --prompt.", risk_kinds=[CLIModelBackedRiskKind.UNBOUNDED_PROMPT_RISK])
        return build_cli_model_backed_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIModelBackedDecisionKind.ALLOW_REQUEST_ENVELOPE_PREVIEW, "Request envelope preview uses v0.34.2 metadata only.", allowed_command_kind=kind)
    if kind == CLIModelBackedCommandKind.RESPONSE_SANITIZE_PREVIEW:
        if "response" not in invocation.parsed_args:
            return build_cli_model_backed_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIModelBackedDecisionKind.DENY, "Response sanitize preview requires --response.", risk_kinds=[CLIModelBackedRiskKind.UNBOUNDED_RESPONSE_RISK])
        return build_cli_model_backed_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIModelBackedDecisionKind.ALLOW_RESPONSE_SANITIZE_PREVIEW, "Response sanitize preview uses v0.34.3.", allowed_command_kind=kind)
    if kind == CLIModelBackedCommandKind.RESPONSE_QUARANTINE_PREVIEW:
        if "response" not in invocation.parsed_args:
            return build_cli_model_backed_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIModelBackedDecisionKind.DENY, "Response quarantine preview requires --response.", risk_kinds=[CLIModelBackedRiskKind.UNQUARANTINED_ACTION_EXECUTION_RISK])
        return build_cli_model_backed_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIModelBackedDecisionKind.ALLOW_RESPONSE_QUARANTINE_PREVIEW, "Response quarantine preview uses v0.34.5 metadata.", allowed_command_kind=kind)
    if kind in BOUNDED_STEP_COMMANDS:
        if not surface.policy.allow_bounded_model_backed_step:
            return build_cli_model_backed_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIModelBackedDecisionKind.DENY, "Bounded model-backed step disabled by policy.", risk_kinds=[CLIModelBackedRiskKind.UNQUARANTINED_ACTION_EXECUTION_RISK])
        response_key = "mock_response" if "mock" in kind.value else "supplied_response"
        if response_key not in invocation.parsed_args:
            return build_cli_model_backed_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIModelBackedDecisionKind.DENY, "Bounded model-backed command requires supplied/mock response.", risk_kinds=[CLIModelBackedRiskKind.UNBOUNDED_RESPONSE_RISK])
        decision_kind = CLIModelBackedDecisionKind.ALLOW_BOUNDED_MODEL_BACKED_STEP_WITH_MOCK_RESPONSE if response_key == "mock_response" else CLIModelBackedDecisionKind.ALLOW_BOUNDED_MODEL_BACKED_STEP_WITH_SUPPLIED_RESPONSE
        return build_cli_model_backed_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, decision_kind, "Bounded model-backed step allowed only through v0.34.6.", allowed_command_kind=kind, bounded_model_backed_step_allowed=True)
    if kind == CLIModelBackedCommandKind.MODEL_BACKED_STEP_WITH_CONTROLLED_MODEL:
        context_ok = isinstance(runtime_context, CLIModelBackedRuntimeContext) and runtime_context.allows_controlled_model_step
        if not context_ok or not surface.policy.allow_controlled_model_step_via_existing_boundary:
            return build_cli_model_backed_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIModelBackedDecisionKind.FUTURE_GATE_REQUIRED, "Controlled model CLI step requires explicit runtime_context with v0.34.6/v0.34.4 route.", risk_kinds=[CLIModelBackedRiskKind.DIRECT_PROVIDER_INVOCATION_RISK])
        return build_cli_model_backed_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIModelBackedDecisionKind.ALLOW_CONTROLLED_MODEL_STEP_VIA_EXISTING_BOUNDARY, "Controlled model CLI step allowed only through v0.34.6 and v0.34.4 runtime_context.", allowed_command_kind=kind, bounded_model_backed_step_allowed=True, controlled_model_step_via_existing_boundary_allowed=True)
    if kind == CLIModelBackedCommandKind.MODEL_INVOCATION_TRACE_PREVIEW:
        if not surface.policy.allow_model_invocation_trace_preview:
            return build_cli_model_backed_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIModelBackedDecisionKind.DENY, "Trace preview disabled by policy.", risk_kinds=[CLIModelBackedRiskKind.PERSISTENT_TRACE_WRITE_RISK])
        return build_cli_model_backed_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIModelBackedDecisionKind.ALLOW_MODEL_INVOCATION_TRACE_PREVIEW, "Trace preview uses v0.34.7 returned packet only.", allowed_command_kind=kind, model_invocation_trace_preview_allowed=True)
    if kind == CLIModelBackedCommandKind.NO_OP:
        return build_cli_model_backed_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIModelBackedDecisionKind.NO_OP, "No-op performs no action.", allowed_command_kind=kind)
    return build_cli_model_backed_invocation_decision(f"{invocation.invocation_id}:decision", invocation.invocation_id, CLIModelBackedDecisionKind.BLOCK, "Unsupported command blocked.", risk_kinds=[CLIModelBackedRiskKind.UNKNOWN])


def _run_output_from_denial(invocation: CLIModelBackedInvocation, decision: CLIModelBackedInvocationDecision) -> CLIModelBackedRunOutput:
    denied = build_cli_model_backed_denied_command(
        f"{invocation.invocation_id}:denied",
        invocation_id=invocation.invocation_id,
        decision_id=decision.decision_id,
        command_kind=invocation.command_kind,
        risk_kinds=list(decision.risk_kinds),
        reason=decision.reason,
    )
    rendered, _, _ = _bounded_preview({"denied": denied.reason, "safe_alternatives": denied.safe_alternatives})
    return build_cli_model_backed_run_output(
        f"{invocation.invocation_id}:run_output",
        invocation.invocation_id,
        rendered,
        CLIModelBackedSurfaceStatus.BLOCKED,
        command_result=None,
        denied_command=denied,
        output_format=invocation.requested_output_format,
        summary="CLI model-backed command denied or blocked safely.",
    )


def _run_output_from_result(invocation: CLIModelBackedInvocation, result: CLIModelBackedCommandResult) -> CLIModelBackedRunOutput:
    rendered, redacted, truncated = _bounded_preview(result.structured_result or result.text_summary)
    safe_result = CLIModelBackedCommandResult(**{**result.__dict__, "redacted": result.redacted or redacted, "truncated": result.truncated or truncated})
    return build_cli_model_backed_run_output(
        f"{invocation.invocation_id}:run_output",
        invocation.invocation_id,
        rendered or result.text_summary,
        result.status,
        command_result=safe_result,
        denied_command=None,
        output_format=invocation.requested_output_format,
        summary=result.text_summary,
    )


def _response_packet(response_text: str, response_envelope_id: str) -> tuple[ModelResponseEnvelope, ModelOutputActionQuarantinePacket]:
    response_envelope = build_model_response_envelope_from_supplied_text(response_text, response_envelope_id=response_envelope_id)
    candidate_set = extract_model_output_action_candidates_from_response_envelope(response_envelope)
    packet = build_model_output_action_quarantine_packet_from_candidates(candidate_set.candidates, source_response_envelope_id=response_envelope.response_envelope_id)
    validate_model_output_action_quarantine_packet(packet)
    return response_envelope, packet


def _run_model_step_from_response(invocation: CLIModelBackedInvocation, decision: CLIModelBackedInvocationDecision, response_text: str) -> CLIModelBackedCommandResult:
    response_envelope, packet = _response_packet(response_text, f"{invocation.invocation_id}:response_envelope")
    step_input = build_model_backed_step_input(
        f"{invocation.invocation_id}:model_backed_step_input",
        integration_mode=ModelBackedStepIntegrationMode.QUARANTINE_PACKET_ONLY,
        response_envelope_id=response_envelope.response_envelope_id,
        quarantine_packet_id=packet.quarantine_packet_id,
        agent_step_runner_id="agent_step_runner_mvp:v0.33.6",
        task_summary="v0.34.8 bounded CLI model-backed step.",
    )
    output = run_model_backed_agent_step(
        step_input,
        quarantine_packet=packet,
        response_envelope=response_envelope,
        agent_step_runner=build_agent_step_runner_mvp(),
    )
    return build_cli_model_backed_command_result(
        f"{invocation.invocation_id}:result",
        invocation.invocation_id,
        decision.decision_id,
        invocation.command_kind,
        CLIModelBackedSurfaceStatus.COMPLETED,
        response_envelope_ref=response_envelope.response_envelope_id,
        quarantine_packet_ref=packet.quarantine_packet_id,
        model_backed_step_output_ref=output.step_output_id,
        structured_result={
            "model_backed_step_output_id": output.step_output_id,
            "status": str(output.status),
            "outcome_kind": str(output.outcome_kind),
            "ready_for_execution": output.ready_for_execution,
        },
        text_summary="CLI command completed through v0.34.6 bounded model-backed step.",
    )


def run_cli_model_backed_command(
    invocation: CLIModelBackedInvocation,
    surface: CLIModelBackedSurface,
    runtime_context: CLIModelBackedRuntimeContext | dict[str, Any] | None = None,
) -> CLIModelBackedRunOutput:
    if not isinstance(invocation, CLIModelBackedInvocation):
        raise TypeError("invocation must be CLIModelBackedInvocation")
    if not isinstance(surface, CLIModelBackedSurface):
        raise TypeError("surface must be CLIModelBackedSurface")
    decision = evaluate_cli_model_backed_invocation(invocation, surface, runtime_context)
    decision_kind = CLIModelBackedDecisionKind(decision.decision_kind)
    kind = CLIModelBackedCommandKind(invocation.command_kind)
    if decision_kind in {CLIModelBackedDecisionKind.BLOCK, CLIModelBackedDecisionKind.DENY, CLIModelBackedDecisionKind.FUTURE_GATE_REQUIRED}:
        return _run_output_from_denial(invocation, decision)
    if decision_kind in {CLIModelBackedDecisionKind.ALLOW_HELP, CLIModelBackedDecisionKind.ALLOW_STATUS, CLIModelBackedDecisionKind.ALLOW_DRY_RUN, CLIModelBackedDecisionKind.NO_OP}:
        result = build_cli_model_backed_command_result(
            f"{invocation.invocation_id}:result",
            invocation.invocation_id,
            decision.decision_id,
            kind,
            CLIModelBackedSurfaceStatus.NO_OP if decision_kind == CLIModelBackedDecisionKind.NO_OP else CLIModelBackedSurfaceStatus.COMPLETED,
            structured_result={"command": kind.value, "ready_for_execution": False, "safe_surface": True},
            text_summary="Bounded CLI model-backed help/status/dry-run/no-op output.",
        )
        return _run_output_from_result(invocation, result)
    if decision_kind == CLIModelBackedDecisionKind.ALLOW_REQUEST_ENVELOPE_PREVIEW:
        prompt = str(invocation.parsed_args.get("prompt", ""))
        preview, redacted, truncated = _bounded_preview(prompt, 500)
        payload_ref = build_model_prompt_payload_ref(
            f"{invocation.invocation_id}:prompt_payload_ref",
            prompt_preview=preview if not redacted else "[redacted]",
            estimated_prompt_chars=len(prompt),
            redacted=True,
            truncated=truncated,
        )
        envelope = build_model_request_envelope(f"{invocation.invocation_id}:request_envelope", payload_ref=payload_ref)
        result = build_cli_model_backed_command_result(
            f"{invocation.invocation_id}:result",
            invocation.invocation_id,
            decision.decision_id,
            kind,
            CLIModelBackedSurfaceStatus.COMPLETED,
            request_envelope_ref=envelope.request_envelope_id,
            structured_result={"request_envelope_id": envelope.request_envelope_id, "ready_for_execution": envelope.ready_for_execution},
            text_summary="CLI request envelope preview used v0.34.2 metadata only.",
        )
        return _run_output_from_result(invocation, result)
    if decision_kind == CLIModelBackedDecisionKind.ALLOW_RESPONSE_SANITIZE_PREVIEW:
        response_envelope = build_model_response_envelope_from_supplied_text(str(invocation.parsed_args.get("response", "")), response_envelope_id=f"{invocation.invocation_id}:response_envelope")
        result = build_cli_model_backed_command_result(
            f"{invocation.invocation_id}:result",
            invocation.invocation_id,
            decision.decision_id,
            kind,
            CLIModelBackedSurfaceStatus.COMPLETED,
            response_envelope_ref=response_envelope.response_envelope_id,
            structured_result={"response_envelope_id": response_envelope.response_envelope_id, "redacted": response_envelope.sanitized_payload.redacted, "truncated": response_envelope.sanitized_payload.truncated},
            text_summary="CLI sanitize-response preview used v0.34.3.",
        )
        return _run_output_from_result(invocation, result)
    if decision_kind == CLIModelBackedDecisionKind.ALLOW_RESPONSE_QUARANTINE_PREVIEW:
        response_envelope, packet = _response_packet(str(invocation.parsed_args.get("response", "")), f"{invocation.invocation_id}:response_envelope")
        result = build_cli_model_backed_command_result(
            f"{invocation.invocation_id}:result",
            invocation.invocation_id,
            decision.decision_id,
            kind,
            CLIModelBackedSurfaceStatus.COMPLETED,
            response_envelope_ref=response_envelope.response_envelope_id,
            quarantine_packet_ref=packet.quarantine_packet_id,
            structured_result={"quarantine_packet_id": packet.quarantine_packet_id, "candidate_count": packet.candidate_set.candidate_count, "ready_for_execution": packet.ready_for_execution},
            text_summary="CLI quarantine-response preview used v0.34.5.",
        )
        return _run_output_from_result(invocation, result)
    if decision_kind in {
        CLIModelBackedDecisionKind.ALLOW_BOUNDED_MODEL_BACKED_STEP_WITH_MOCK_RESPONSE,
        CLIModelBackedDecisionKind.ALLOW_BOUNDED_MODEL_BACKED_STEP_WITH_SUPPLIED_RESPONSE,
    }:
        response_key = "mock_response" if decision_kind == CLIModelBackedDecisionKind.ALLOW_BOUNDED_MODEL_BACKED_STEP_WITH_MOCK_RESPONSE else "supplied_response"
        return _run_output_from_result(invocation, _run_model_step_from_response(invocation, decision, str(invocation.parsed_args.get(response_key, ""))))
    if decision_kind == CLIModelBackedDecisionKind.ALLOW_CONTROLLED_MODEL_STEP_VIA_EXISTING_BOUNDARY:
        step_input = build_model_backed_step_input(
            f"{invocation.invocation_id}:controlled_step_input",
            integration_mode=ModelBackedStepIntegrationMode.EXISTING_BOUNDARY_THEN_QUARANTINE,
            request_envelope_id="request_envelope:cli_controlled:v0.34.8",
            agent_step_runner_id="agent_step_runner_mvp:v0.33.6",
            task_summary="v0.34.8 controlled model CLI route via v0.34.6/v0.34.4 only.",
        )
        policy = default_model_backed_step_integration_policy(
            allowed_modes=[ModelBackedStepIntegrationMode.EXISTING_BOUNDARY_THEN_QUARANTINE, ModelBackedStepIntegrationMode.QUARANTINE_PACKET_ONLY],
            allow_existing_boundary_adapter_call=True,
        )
        step_output = run_model_backed_agent_step(
            step_input,
            policy=policy,
            provider_adapter=_context_get(runtime_context, "provider_adapter"),
            provider_boundary_callable=_context_get(runtime_context, "provider_boundary_callable"),
            agent_step_runner=_context_get(runtime_context, "agent_step_runner") or build_agent_step_runner_mvp(),
        )
        result = build_cli_model_backed_command_result(
            f"{invocation.invocation_id}:result",
            invocation.invocation_id,
            decision.decision_id,
            kind,
            CLIModelBackedSurfaceStatus.COMPLETED,
            model_backed_step_output_ref=step_output.step_output_id,
            quarantine_packet_ref=step_output.quarantine_packet_ref,
            structured_result={"model_backed_step_output_id": step_output.step_output_id, "provider_boundary_result_ref": step_output.provider_boundary_result_ref, "ready_for_execution": step_output.ready_for_execution},
            text_summary="CLI controlled-model command completed only through v0.34.6/v0.34.4 route.",
        )
        return _run_output_from_result(invocation, result)
    if decision_kind == CLIModelBackedDecisionKind.ALLOW_MODEL_INVOCATION_TRACE_PREVIEW:
        step_output = _context_get(runtime_context, "model_backed_step_output")
        if isinstance(step_output, ModelBackedStepOutput):
            packet = build_model_invocation_trace_packet_from_model_backed_step_output(step_output)
        else:
            packet = emit_model_invocation_trace_packet(
                build_model_invocation_trace_emission_input(f"{invocation.invocation_id}:trace_input"),
                _context_get(runtime_context, "trace_emitter") or build_model_invocation_trace_emitter(),
            )
        if not isinstance(packet, ModelInvocationTracePacket) or not model_invocation_trace_packet_is_not_persistence(packet):
            return _run_output_from_denial(invocation, decision)
        result = build_cli_model_backed_command_result(
            f"{invocation.invocation_id}:result",
            invocation.invocation_id,
            decision.decision_id,
            kind,
            CLIModelBackedSurfaceStatus.COMPLETED,
            trace_packet_ref=packet.trace_packet_id,
            structured_result={"trace_packet_id": packet.trace_packet_id, "event_count": len(packet.events), "object_count": len(packet.objects), "ready_for_persistent_write": packet.ready_for_persistent_write},
            text_summary="CLI trace preview used v0.34.7 returned packet only.",
        )
        return _run_output_from_result(invocation, result)
    return _run_output_from_denial(invocation, decision)


def render_cli_model_backed_output(output: CLIModelBackedRunOutput, output_format: CLIModelBackedOutputFormat | str | None = None) -> str:
    if not isinstance(output, CLIModelBackedRunOutput):
        raise TypeError("output must be CLIModelBackedRunOutput")
    fmt = CLIModelBackedOutputFormat(output_format or output.output_format)
    if fmt == CLIModelBackedOutputFormat.NO_OUTPUT:
        return ""
    if fmt == CLIModelBackedOutputFormat.JSON:
        payload = {
            "run_output_id": output.run_output_id,
            "status": str(output.status),
            "summary": output.summary,
            "result": output.command_result.structured_result if output.command_result else None,
            "denied": output.denied_command.reason if output.denied_command else None,
        }
        rendered, _, _ = _bounded_preview(payload)
        return rendered
    return output.rendered_output


def cli_model_backed_flags_preserve_unsafe_false(flags: CLIModelBackedFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_CLI_MODEL_BACKED_FLAG_NAMES) and flags.production_certified is False


def cli_model_backed_invocation_is_not_shell(invocation: CLIModelBackedInvocation) -> bool:
    return _metadata_flag_true(invocation.metadata, {"shell_execution", "subprocess_execution", "command_execution"}) is False


def cli_model_backed_decision_blocks_direct_provider(decision: CLIModelBackedInvocationDecision) -> bool:
    return (
        decision.shell_execution_allowed is False
        and decision.subprocess_allowed is False
        and decision.command_execution_allowed is False
        and decision.direct_provider_invocation_allowed is False
        and decision.provider_sdk_allowed is False
        and decision.direct_network_allowed is False
        and decision.credential_access_allowed is False
        and decision.secret_read_allowed is False
        and decision.general_tool_execution_allowed is False
        and decision.workspace_write_allowed is False
        and decision.patch_proposal_allowed is False
        and decision.patch_application_allowed is False
        and decision.persistent_trace_write_allowed is False
    )


def cli_model_backed_surface_is_not_shell(surface: CLIModelBackedSurface) -> bool:
    return surface.ready_for_execution is False and surface.policy.allow_shell is False and surface.policy.allow_subprocess is False


def v0348_readiness_report_is_not_general_execution_ready(report: V0348ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_CLI_MODEL_BACKED_FLAG_NAMES)
