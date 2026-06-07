from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import (
    _metadata_flag_true,
    _require_non_blank,
    _validate_object_list,
    _validate_string_list,
)
from .prompt_assembly import PromptAssemblyOutput
from .provider_profile import (
    ProviderInvocationPolicy,
    ProviderProfileDescriptor,
    provider_invocation_policy_blocks_runtime_access,
    provider_profile_descriptor_is_not_invocation,
)


V0342_VERSION = "v0.34.2"
V0342_RELEASE_NAME = "v0.34.2 Model Request Envelope"
DEFAULT_MAX_PROMPT_PREVIEW_CHARS = 2000

DEFAULT_SECRET_LIKE_PATTERNS = [
    ".env",
    "secret",
    "token",
    "key",
    "credential",
    "api_key",
    "password",
]

DEFAULT_MODEL_REQUEST_PROHIBITED_RUNTIME_ACTIONS = [
    "controlled model invocation",
    "real model invocation",
    "model invocation",
    "provider invocation",
    "provider SDK invocation",
    "existing boundary invocation",
    "network access",
    "credential access",
    "secret read",
    "env read",
    "endpoint construction",
    "agent step execution",
    "general agent execution",
    "autonomous loop",
    "general tool execution",
    "tool calls",
    "function calls",
    "recursive calls",
    "shell execution",
    "subprocess execution",
    "command execution",
    "workspace write",
    "code edit",
    "patch application",
    "raw prompt persistence",
    "external harness execution",
    "reference code execution",
    "reference import",
    "dependency install",
    "persistent trace write",
    "external trace sink",
    "UI runtime",
    "external control",
    "authority grant",
]

DEFAULT_MODEL_REQUEST_WITHDRAWAL_CONDITIONS = [
    "Any model/provider/existing-boundary invocation path is introduced.",
    "Any provider SDK, network, credential, secret, env, endpoint, tool-call, function-call, or recursive-call path is introduced.",
    "Any raw prompt persistence or raw request payload persistence path is introduced.",
    "Any unsafe readiness flag or production_certified becomes true.",
]

UNSAFE_MODEL_REQUEST_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_controlled_model_invocation",
    "ready_for_real_model_invocation",
    "ready_for_model_invocation",
    "ready_for_provider_invocation",
    "ready_for_provider_sdk_invocation",
    "ready_for_existing_boundary_invocation",
    "ready_for_network_access",
    "ready_for_credential_access",
    "ready_for_secret_read",
    "ready_for_agent_step_execution",
    "ready_for_general_agent_execution",
    "ready_for_autonomous_agent_runtime",
    "ready_for_general_tool_execution",
    "ready_for_tool_calls",
    "ready_for_function_calls",
    "ready_for_recursive_calls",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_patch_application",
    "ready_for_registry_mutation",
    "ready_for_memory_mutation",
    "ready_for_raw_prompt_persistence",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
)


class ModelRequestEnvelopeKind(StrEnum):
    PROMPT_ASSEMBLY_REQUEST = "prompt_assembly_request"
    BOUNDED_CHAT_REQUEST = "bounded_chat_request"
    SUPPLIED_OUTPUT_TEST_REQUEST = "supplied_output_test_request"
    MOCK_PROVIDER_TEST_REQUEST = "mock_provider_test_request"
    EXISTING_BOUNDARY_FUTURE_GATE_REQUEST = "existing_boundary_future_gate_request"
    BLOCKED_REQUEST = "blocked_request"
    NO_OP_REQUEST = "no_op_request"
    UNKNOWN = "unknown"


class ModelRequestPayloadFormat(StrEnum):
    MESSAGE_LIST = "message_list"
    PLAIN_TEXT_PROMPT = "plain_text_prompt"
    STRUCTURED_BLOCKS = "structured_blocks"
    PROMPT_REF_ONLY = "prompt_ref_only"
    REDACTED_PREVIEW_ONLY = "redacted_preview_only"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class ModelRequestSourceKind(StrEnum):
    V0341_PROVIDER_PROFILE = "v0341_provider_profile"
    V0340_MODEL_INVOCATION_BOUNDARY = "v0340_model_invocation_boundary"
    V0332_PROMPT_ASSEMBLY_OUTPUT = "v0332_prompt_assembly_output"
    V0333_SESSION_RUNTIME = "v0333_session_runtime"
    V0336_AGENT_STEP_RUNNER = "v0336_agent_step_runner"
    MANUAL_REQUEST_SPEC = "manual_request_spec"
    TEST_FIXTURE = "test_fixture"
    REFERENCE_CONTEXT_REF = "reference_context_ref"
    OPENCODE_REFERENCE_CONTEXT_REF = "opencode_reference_context_ref"
    HERMES_REFERENCE_CONTEXT_REF = "hermes_reference_context_ref"
    UNKNOWN = "unknown"


class ModelRequestStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    ENVELOPE_CONSTRUCTED = "envelope_constructed"
    VALIDATED = "validated"
    VALIDATED_WITH_GAPS = "validated_with_gaps"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class ModelRequestReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    REQUEST_CONTRACT_READY = "request_contract_ready"
    ENVELOPE_VALIDATION_READY = "envelope_validation_ready"
    DESIGN_HANDOFF_READY_FOR_V0343 = "design_handoff_ready_for_v0343"
    DESIGN_HANDOFF_READY_FOR_V0344 = "design_handoff_ready_for_v0344"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class ModelRequestValidationDecisionKind(StrEnum):
    ACCEPT_ENVELOPE_METADATA_ONLY = "accept_envelope_metadata_only"
    ACCEPT_FUTURE_GATE_ENVELOPE = "accept_future_gate_envelope"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class ModelRequestRiskKind(StrEnum):
    RAW_PROMPT_PERSISTENCE_RISK = "raw_prompt_persistence_risk"
    SECRET_IN_PROMPT_RISK = "secret_in_prompt_risk"
    CREDENTIAL_IN_PROMPT_RISK = "credential_in_prompt_risk"
    TOKEN_IN_PROMPT_RISK = "token_in_prompt_risk"
    UNBOUNDED_PROMPT_RISK = "unbounded_prompt_risk"
    UNBOUNDED_RESPONSE_RISK = "unbounded_response_risk"
    PROVIDER_INVOCATION_RISK = "provider_invocation_risk"
    NETWORK_ACCESS_RISK = "network_access_risk"
    CREDENTIAL_ACCESS_RISK = "credential_access_risk"
    TOOL_CALL_RISK = "tool_call_risk"
    FUNCTION_CALL_RISK = "function_call_risk"
    RECURSIVE_CALL_RISK = "recursive_call_risk"
    PROMPT_INJECTION_RISK = "prompt_injection_risk"
    BOUNDARY_OVERRIDE_RISK = "boundary_override_risk"
    REFERENCE_CONTENT_LEAK_RISK = "reference_content_leak_risk"
    ENDPOINT_CONSTRUCTION_RISK = "endpoint_construction_risk"
    UNKNOWN = "unknown"


class ModelRequestDataSensitivityKind(StrEnum):
    PUBLIC = "public"
    INTERNAL = "internal"
    USER_SUPPLIED = "user_supplied"
    REFERENCE_CONTEXT = "reference_context"
    UNTRUSTED_EXTERNAL_REFERENCE = "untrusted_external_reference"
    SECRET_LIKE = "secret_like"
    CREDENTIAL_LIKE = "credential_like"
    TOKEN_LIKE = "token_like"
    UNKNOWN = "unknown"


def _validate_version_includes_v0342(version: str) -> None:
    _require_non_blank("version", version)
    if V0342_VERSION not in version:
        raise ValueError("version must include v0.34.2")


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.34.2")


def _validate_true(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not True:
            raise ValueError(f"{name} must always be True in v0.34.2")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise TypeError(f"{name} must be dict[str, Any]")


def _validate_enum_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _validate_non_negative(name: str, value: int | None) -> None:
    if value is not None and value < 0:
        raise ValueError(f"{name} must be >= 0")


def _validate_metadata_no_invocation(metadata: dict[str, Any]) -> None:
    _validate_dict("metadata", metadata)
    if _metadata_flag_true(
        metadata,
        {
            "model_invocation",
            "provider_call",
            "provider_invocation",
            "existing_boundary_invocation",
            "provider_sdk_import",
            "network_call",
            "credential_access",
            "secret_read",
            "env_read",
            "endpoint_construction",
            "tool_call",
            "function_call",
            "recursive_call",
            "execution",
            "workspace_write",
            "raw_prompt_persistence",
            "persistent_trace_write",
        },
    ):
        raise ValueError("v0.34.2 metadata cannot imply invocation, external access, or raw prompt persistence")


def _validate_secret_like_patterns(name: str, values: list[str]) -> None:
    _validate_string_list(name, values)
    lowered = " | ".join(values).lower()
    missing = [term for term in DEFAULT_SECRET_LIKE_PATTERNS if term not in lowered]
    if missing:
        raise ValueError(f"{name} must include secret-like defaults: {missing}")


def _contains_secret_like_text(value: str) -> bool:
    lowered = value.lower()
    markers = ("secret=", "token=", "key=", "credential=", "api_key=", "password=", "sk-")
    return any(marker in lowered for marker in markers)


def _redacted_bounded_preview(value: str, max_chars: int = DEFAULT_MAX_PROMPT_PREVIEW_CHARS) -> tuple[str, bool, bool]:
    redacted = value
    was_redacted = False
    for marker in ("secret=", "token=", "key=", "credential=", "api_key=", "password=", "sk-"):
        if marker in redacted.lower():
            redacted = redacted.replace(marker, "[redacted]=")
            was_redacted = True
    truncated = len(redacted) > max_chars
    if truncated:
        redacted = redacted[:max_chars]
    return redacted, was_redacted, truncated


def _validate_contains_terms(name: str, values: list[str], terms: list[str]) -> None:
    _validate_string_list(name, values)
    lowered = " | ".join(values).lower()
    missing = [term for term in terms if term.lower() not in lowered]
    if missing:
        raise ValueError(f"{name} missing required terms: {missing}")


@dataclass(frozen=True)
class ModelRequestFlagSet:
    flag_set_id: str
    version: str = V0342_VERSION
    model_request_envelope_constructed: bool = False
    prompt_payload_ref_constructed: bool = False
    model_request_validation_available: bool = False
    ready_for_v0343_model_response_envelope: bool = False
    ready_for_v0344_existing_provider_boundary_adapter: bool = False
    ready_for_execution: bool = False
    ready_for_controlled_model_invocation: bool = False
    ready_for_real_model_invocation: bool = False
    ready_for_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_provider_sdk_invocation: bool = False
    ready_for_existing_boundary_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_secret_read: bool = False
    ready_for_agent_step_execution: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_tool_calls: bool = False
    ready_for_function_calls: bool = False
    ready_for_recursive_calls: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_application: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_raw_prompt_persistence: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version_includes_v0342(self.version)
        _validate_false(self, UNSAFE_MODEL_REQUEST_FLAG_NAMES)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False in v0.34.2")
        _validate_metadata_no_invocation(self.metadata)


@dataclass(frozen=True)
class ModelRequestSourceRef:
    source_ref_id: str
    source_kind: ModelRequestSourceKind | str
    source_id: str
    source_summary: str
    sensitivity: ModelRequestDataSensitivityKind | str = ModelRequestDataSensitivityKind.INTERNAL
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        ModelRequestSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        sensitivity = ModelRequestDataSensitivityKind(self.sensitivity)
        if sensitivity in {
            ModelRequestDataSensitivityKind.SECRET_LIKE,
            ModelRequestDataSensitivityKind.CREDENTIAL_LIKE,
            ModelRequestDataSensitivityKind.TOKEN_LIKE,
            ModelRequestDataSensitivityKind.UNKNOWN,
        }:
            raise ValueError("secret/credential/token-like or unknown request sources are blocked in v0.34.2")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_invocation(self.metadata)

    @property
    def provider_call(self) -> bool:
        return False

    @property
    def file_read(self) -> bool:
        return False

    @property
    def credential_access(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelPromptPayloadRef:
    prompt_payload_ref_id: str
    payload_format: ModelRequestPayloadFormat | str
    prompt_output_id: str | None
    prompt_summary: str
    prompt_preview: str
    message_count: int
    estimated_prompt_chars: int
    estimated_prompt_tokens: int | None
    redacted: bool
    truncated: bool
    contains_secret_like_content: bool
    contains_credential_like_content: bool
    contains_token_like_content: bool
    source_refs: list[ModelRequestSourceRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("prompt_payload_ref_id", self.prompt_payload_ref_id)
        ModelRequestPayloadFormat(self.payload_format)
        _require_non_blank("prompt_summary", self.prompt_summary)
        if len(self.prompt_preview) > DEFAULT_MAX_PROMPT_PREVIEW_CHARS:
            raise ValueError("prompt_preview must be bounded")
        for name in ("message_count", "estimated_prompt_chars"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        _validate_non_negative("estimated_prompt_tokens", self.estimated_prompt_tokens)
        _validate_false(
            self,
            (
                "contains_secret_like_content",
                "contains_credential_like_content",
                "contains_token_like_content",
            ),
        )
        if _contains_secret_like_text(self.prompt_preview):
            raise ValueError("prompt_preview must not contain secret-like content")
        _validate_object_list("source_refs", self.source_refs, ModelRequestSourceRef)
        _validate_metadata_no_invocation(self.metadata)

    @property
    def raw_prompt_persistence(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelRequestTokenBudget:
    token_budget_id: str
    max_prompt_chars: int = 12000
    max_prompt_tokens: int | None = None
    max_response_chars: int = 12000
    max_response_tokens: int | None = None
    max_total_tokens: int | None = None
    allow_unbounded_prompt: bool = False
    allow_unbounded_response: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("token_budget_id", self.token_budget_id)
        for name in ("max_prompt_chars", "max_prompt_tokens", "max_response_chars", "max_response_tokens", "max_total_tokens"):
            _validate_non_negative(name, getattr(self, name))
        _validate_false(self, ("allow_unbounded_prompt", "allow_unbounded_response"))
        _validate_metadata_no_invocation(self.metadata)


@dataclass(frozen=True)
class ModelRequestStopPolicy:
    stop_policy_id: str
    stop_sequences: list[str] = field(default_factory=list)
    prohibited_stop_sequences: list[str] = field(default_factory=list)
    max_stop_sequence_count: int = 4
    max_stop_sequence_chars: int = 120
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("stop_policy_id", self.stop_policy_id)
        _validate_string_list("stop_sequences", self.stop_sequences)
        _validate_string_list("prohibited_stop_sequences", self.prohibited_stop_sequences)
        _validate_non_negative("max_stop_sequence_count", self.max_stop_sequence_count)
        _validate_non_negative("max_stop_sequence_chars", self.max_stop_sequence_chars)
        if len(self.stop_sequences) > self.max_stop_sequence_count:
            raise ValueError("stop_sequences must be bounded")
        if any(len(value) > self.max_stop_sequence_chars for value in self.stop_sequences):
            raise ValueError("stop sequence length must be bounded")
        _validate_metadata_no_invocation(self.metadata)

    @property
    def provider_call(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelRequestTimeoutPolicy:
    timeout_policy_id: str
    timeout_seconds: int | None = None
    connect_timeout_seconds: int | None = None
    read_timeout_seconds: int | None = None
    allow_streaming: bool = False
    allow_retries: bool = False
    max_retries: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("timeout_policy_id", self.timeout_policy_id)
        for name in ("timeout_seconds", "connect_timeout_seconds", "read_timeout_seconds", "max_retries"):
            _validate_non_negative(name, getattr(self, name))
        if self.max_retries != 0:
            raise ValueError("max_retries must be 0 in v0.34.2")
        _validate_false(self, ("allow_streaming", "allow_retries"))
        _validate_metadata_no_invocation(self.metadata)

    @property
    def network_access(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelRequestOutputPolicy:
    output_policy_id: str
    max_output_chars: int = 12000
    max_output_tokens: int | None = None
    allow_raw_response_persistence: bool = False
    allow_tool_calls: bool = False
    allow_function_calls: bool = False
    allow_patch_output: bool = False
    allow_command_output: bool = False
    allow_untrusted_action: bool = False
    require_response_envelope: bool = True
    require_response_sanitizer: bool = True
    require_action_quarantine: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("output_policy_id", self.output_policy_id)
        _validate_non_negative("max_output_chars", self.max_output_chars)
        _validate_non_negative("max_output_tokens", self.max_output_tokens)
        _validate_false(
            self,
            (
                "allow_raw_response_persistence",
                "allow_tool_calls",
                "allow_function_calls",
                "allow_patch_output",
                "allow_command_output",
                "allow_untrusted_action",
            ),
        )
        _validate_true(self, ("require_response_envelope", "require_response_sanitizer", "require_action_quarantine"))
        _validate_metadata_no_invocation(self.metadata)


@dataclass(frozen=True)
class ModelRequestSafetyConstraints:
    safety_constraints_id: str
    prohibited_request_content: list[str] = field(default_factory=lambda: list(DEFAULT_SECRET_LIKE_PATTERNS))
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_MODEL_REQUEST_PROHIBITED_RUNTIME_ACTIONS))
    required_boundary_refs: list[str] = field(default_factory=lambda: ["v0.34.0 boundary", "v0.34.1 provider profile policy"])
    require_provider_profile_validation: bool = True
    require_prompt_redaction: bool = True
    require_token_budget: bool = True
    require_output_policy: bool = True
    require_no_tool_calls: bool = True
    require_no_function_calls: bool = True
    require_no_recursive_calls: bool = True
    require_no_raw_prompt_persistence: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("safety_constraints_id", self.safety_constraints_id)
        for name in ("prohibited_request_content", "prohibited_runtime_actions", "required_boundary_refs"):
            _validate_string_list(name, getattr(self, name))
        _validate_secret_like_patterns("prohibited_request_content", self.prohibited_request_content)
        _validate_contains_terms(
            "prohibited_runtime_actions",
            self.prohibited_runtime_actions,
            ["provider invocation", "network", "credential", "tool calls", "function calls", "recursive calls", "shell", "command", "write", "patch", "external harness"],
        )
        for name in self.__dataclass_fields__:
            if name.startswith("require_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.34.2")
        _validate_metadata_no_invocation(self.metadata)

    @property
    def runtime_enforcement(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelRequestProviderBinding:
    provider_binding_id: str
    provider_profile_id: str | None
    provider_profile_name: str | None
    provider_profile_kind: str | None
    provider_boundary_ref_id: str | None
    invocation_policy_id: str | None
    binding_summary: str
    future_gated: bool = False
    invocation_allowed: bool = False
    provider_invocation_allowed: bool = False
    network_allowed: bool = False
    credential_access_allowed: bool = False
    source_refs: list[ModelRequestSourceRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("provider_binding_id", self.provider_binding_id)
        _require_non_blank("binding_summary", self.binding_summary)
        _validate_false(self, ("invocation_allowed", "provider_invocation_allowed", "network_allowed", "credential_access_allowed"))
        _validate_object_list("source_refs", self.source_refs, ModelRequestSourceRef)
        _validate_metadata_no_invocation(self.metadata)

    @property
    def provider_call(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelRequestEnvelopeInput:
    envelope_input_id: str
    source_version: str
    prompt_output_id: str | None
    runtime_profile_id: str | None
    session_id: str | None
    turn_id: str | None
    provider_profile_id: str | None
    invocation_policy_id: str | None
    requested_payload_format: ModelRequestPayloadFormat | str
    task_summary: str
    source_refs: list[ModelRequestSourceRef] = field(default_factory=list)
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_MODEL_REQUEST_PROHIBITED_RUNTIME_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("envelope_input_id", self.envelope_input_id)
        _validate_version_includes_v0342(self.source_version)
        ModelRequestPayloadFormat(self.requested_payload_format)
        _require_non_blank("task_summary", self.task_summary)
        _validate_object_list("source_refs", self.source_refs, ModelRequestSourceRef)
        _validate_contains_terms(
            "prohibited_runtime_actions",
            self.prohibited_runtime_actions,
            ["model invocation", "provider invocation", "provider SDK", "network", "credential", "secret read", "tool calls", "function calls", "recursive calls", "shell", "command", "write", "edit", "patch", "external harness execution"],
        )
        _validate_metadata_no_invocation(self.metadata)

    @property
    def provider_invocation_request(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelRequestEnvelope:
    request_envelope_id: str
    version: str
    envelope_kind: ModelRequestEnvelopeKind | str
    status: ModelRequestStatus | str
    readiness_level: ModelRequestReadinessLevel | str
    payload_ref: ModelPromptPayloadRef
    provider_binding: ModelRequestProviderBinding
    token_budget: ModelRequestTokenBudget
    stop_policy: ModelRequestStopPolicy
    timeout_policy: ModelRequestTimeoutPolicy
    output_policy: ModelRequestOutputPolicy
    safety_constraints: ModelRequestSafetyConstraints
    source_refs: list[ModelRequestSourceRef]
    summary: str
    validation_report_id: str | None = None
    ready_for_v0343_model_response_envelope: bool = False
    ready_for_v0344_existing_provider_boundary_adapter: bool = False
    ready_for_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("request_envelope_id", self.request_envelope_id)
        _validate_version_includes_v0342(self.version)
        ModelRequestEnvelopeKind(self.envelope_kind)
        ModelRequestStatus(self.status)
        ModelRequestReadinessLevel(self.readiness_level)
        if not isinstance(self.payload_ref, ModelPromptPayloadRef):
            raise TypeError("payload_ref must be ModelPromptPayloadRef")
        if not isinstance(self.provider_binding, ModelRequestProviderBinding):
            raise TypeError("provider_binding must be ModelRequestProviderBinding")
        for name, expected in (
            ("token_budget", ModelRequestTokenBudget),
            ("stop_policy", ModelRequestStopPolicy),
            ("timeout_policy", ModelRequestTimeoutPolicy),
            ("output_policy", ModelRequestOutputPolicy),
            ("safety_constraints", ModelRequestSafetyConstraints),
        ):
            if not isinstance(getattr(self, name), expected):
                raise TypeError(f"{name} must be {expected.__name__}")
        _validate_object_list("source_refs", self.source_refs, ModelRequestSourceRef)
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_invocation", "ready_for_provider_invocation", "ready_for_execution"))
        _validate_metadata_no_invocation(self.metadata)

    @property
    def provider_call(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelRequestValidationFinding:
    finding_id: str
    request_envelope_id: str | None
    decision_kind: ModelRequestValidationDecisionKind | str
    risk_kinds: list[ModelRequestRiskKind | str]
    summary: str
    blocked: bool = False
    future_gated: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        ModelRequestValidationDecisionKind(self.decision_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, ModelRequestRiskKind)
        _require_non_blank("summary", self.summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_invocation(self.metadata)

    @property
    def invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelRequestValidationReport:
    validation_report_id: str
    version: str
    request_envelope_id: str | None
    findings: list[ModelRequestValidationFinding]
    validation_passed: bool
    blocked_reasons: list[str]
    warning_items: list[str]
    redaction_applied: bool
    prompt_budget_valid: bool
    output_policy_valid: bool
    provider_binding_valid: bool
    summary: str
    ready_for_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version_includes_v0342(self.version)
        _validate_object_list("findings", self.findings, ModelRequestValidationFinding)
        _validate_string_list("blocked_reasons", self.blocked_reasons)
        _validate_string_list("warning_items", self.warning_items)
        if self.validation_passed and self.blocked_reasons:
            raise ValueError("validation_passed cannot be True if blocked_reasons is non-empty")
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_invocation", "ready_for_provider_invocation", "ready_for_execution"))
        _validate_metadata_no_invocation(self.metadata)

    @property
    def invocation_certification(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelRequestEnvelopeReport:
    report_id: str
    version: str
    envelope_input_id: str
    request_envelope_id: str | None
    validation_report_id: str | None
    status: ModelRequestStatus | str
    readiness_level: ModelRequestReadinessLevel | str
    summary: str
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0343_model_response_envelope: bool = False
    ready_for_v0344_existing_provider_boundary_adapter: bool = False
    ready_for_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=lambda: list(DEFAULT_MODEL_REQUEST_WITHDRAWAL_CONDITIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0342(self.version)
        _require_non_blank("envelope_input_id", self.envelope_input_id)
        ModelRequestStatus(self.status)
        ModelRequestReadinessLevel(self.readiness_level)
        _require_non_blank("summary", self.summary)
        for name in ("completed_items", "blocked_items", "future_track_items", "gaps", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        if (self.ready_for_v0343_model_response_envelope or self.ready_for_v0344_existing_provider_boundary_adapter) and self.blocked_items:
            raise ValueError("design-stage handoff readiness is not allowed with blocked_items")
        _validate_false(self, ("ready_for_invocation", "ready_for_provider_invocation", "ready_for_execution"))
        _validate_metadata_no_invocation(self.metadata)

    @property
    def invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelRequestRunPreview:
    run_preview_id: str
    request_envelope_id: str | None = None
    planned_steps: list[str] = field(default_factory=lambda: ["construct bounded prompt payload ref", "bind provider profile metadata", "validate request envelope metadata"])
    expected_artifacts: list[str] = field(default_factory=lambda: ["ModelPromptPayloadRef", "ModelRequestEnvelope", "ModelRequestValidationReport", "V0342ReadinessReport"])
    explicitly_not_performed: list[str] = field(default_factory=lambda: list(DEFAULT_MODEL_REQUEST_PROHIBITED_RUNTIME_ACTIONS))
    no_model_invocation_guarantee: bool = True
    no_real_model_invocation_guarantee: bool = True
    no_provider_invocation_guarantee: bool = True
    no_provider_sdk_invocation_guarantee: bool = True
    no_existing_boundary_invocation_guarantee: bool = True
    no_network_access_guarantee: bool = True
    no_credential_access_guarantee: bool = True
    no_secret_read_guarantee: bool = True
    no_env_read_guarantee: bool = True
    no_agent_step_execution_guarantee: bool = True
    no_tool_execution_guarantee: bool = True
    no_tool_call_guarantee: bool = True
    no_function_call_guarantee: bool = True
    no_recursive_call_guarantee: bool = True
    no_command_execution_guarantee: bool = True
    no_workspace_write_guarantee: bool = True
    no_code_edit_guarantee: bool = True
    no_patch_application_guarantee: bool = True
    no_raw_prompt_persistence_guarantee: bool = True
    no_reference_code_execution_guarantee: bool = True
    no_reference_import_guarantee: bool = True
    no_dependency_install_guarantee: bool = True
    no_persistent_trace_write_guarantee: bool = True
    no_ui_runtime_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.34.2")
        _validate_metadata_no_invocation(self.metadata)

    @property
    def invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelRequestNoInvocationGuarantee:
    guarantee_id: str
    version: str = V0342_VERSION
    no_model_invocation: bool = True
    no_real_model_invocation: bool = True
    no_provider_invocation: bool = True
    no_provider_sdk_invocation: bool = True
    no_existing_boundary_invocation: bool = True
    no_network_access: bool = True
    no_credential_access: bool = True
    no_secret_read: bool = True
    no_env_read: bool = True
    no_endpoint_construction: bool = True
    no_agent_step_execution: bool = True
    no_tool_execution: bool = True
    no_tool_calls: bool = True
    no_function_calls: bool = True
    no_recursive_calls: bool = True
    no_shell_execution: bool = True
    no_subprocess: bool = True
    no_command_execution: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_patch_application: bool = True
    no_raw_prompt_persistence: bool = True
    no_reference_code_execution: bool = True
    no_reference_import: bool = True
    no_reference_dependency_install: bool = True
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
        _validate_version_includes_v0342(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.34.2")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_invocation(self.metadata)


@dataclass(frozen=True)
class V0342ReadinessReport:
    report_id: str
    version: str
    request_envelope_id: str | None
    envelope_report_id: str | None
    validation_report_id: str | None
    summary: str
    ready_for_v0343_model_response_envelope: bool = False
    ready_for_v0344_existing_provider_boundary_adapter: bool = False
    ready_for_execution: bool = False
    ready_for_controlled_model_invocation: bool = False
    ready_for_real_model_invocation: bool = False
    ready_for_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_provider_sdk_invocation: bool = False
    ready_for_existing_boundary_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_secret_read: bool = False
    ready_for_agent_step_execution: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_tool_calls: bool = False
    ready_for_function_calls: bool = False
    ready_for_recursive_calls: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_application: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_raw_prompt_persistence: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_MODEL_REQUEST_PROHIBITED_RUNTIME_ACTIONS))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=lambda: list(DEFAULT_MODEL_REQUEST_WITHDRAWAL_CONDITIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0342(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(self, UNSAFE_MODEL_REQUEST_FLAG_NAMES)
        for name in ("completed_items", "blocked_items", "future_track_items", "prohibited_until_later_gate", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_contains_terms(
            "prohibited_until_later_gate",
            self.prohibited_until_later_gate,
            ["controlled model invocation", "real model invocation", "model invocation", "provider invocation", "provider SDK invocation", "existing boundary invocation", "network access", "credential access", "secret read", "env read", "endpoint construction", "agent step execution", "autonomous loop", "general tool execution", "tool calls", "function calls", "recursive calls", "shell", "subprocess", "command", "workspace write", "code edit", "patch application", "raw prompt persistence", "reference code execution", "reference import", "dependency install", "persistent trace write", "UI runtime", "authority grant"],
        )
        if (self.ready_for_v0343_model_response_envelope or self.ready_for_v0344_existing_provider_boundary_adapter) and self.blocked_items:
            raise ValueError("design-stage handoff readiness is not allowed with blocked_items")
        _validate_metadata_no_invocation(self.metadata)

    @property
    def invocation_readiness(self) -> bool:
        return False


def build_model_request_flags(flag_set_id: str = "model_request_flags:v0.34.2", **kwargs: Any) -> ModelRequestFlagSet:
    return ModelRequestFlagSet(
        flag_set_id=flag_set_id,
        version=kwargs.pop("version", V0342_VERSION),
        model_request_envelope_constructed=kwargs.pop("model_request_envelope_constructed", True),
        prompt_payload_ref_constructed=kwargs.pop("prompt_payload_ref_constructed", True),
        model_request_validation_available=kwargs.pop("model_request_validation_available", True),
        ready_for_v0343_model_response_envelope=kwargs.pop("ready_for_v0343_model_response_envelope", True),
        ready_for_v0344_existing_provider_boundary_adapter=kwargs.pop("ready_for_v0344_existing_provider_boundary_adapter", True),
        **kwargs,
    )


def build_model_request_source_ref(
    source_ref_id: str,
    source_kind: ModelRequestSourceKind | str = ModelRequestSourceKind.MANUAL_REQUEST_SPEC,
    source_id: str = "model_request_source",
    source_summary: str = "Model request source ref only; no fetch/read/execute.",
    **kwargs: Any,
) -> ModelRequestSourceRef:
    return ModelRequestSourceRef(
        source_ref_id=source_ref_id,
        source_kind=source_kind,
        source_id=source_id,
        source_summary=source_summary,
        **kwargs,
    )


def build_model_prompt_payload_ref(
    prompt_payload_ref_id: str = "model_prompt_payload_ref:v0.34.2",
    **kwargs: Any,
) -> ModelPromptPayloadRef:
    return ModelPromptPayloadRef(
        prompt_payload_ref_id=prompt_payload_ref_id,
        payload_format=kwargs.pop("payload_format", ModelRequestPayloadFormat.REDACTED_PREVIEW_ONLY),
        prompt_output_id=kwargs.pop("prompt_output_id", None),
        prompt_summary=kwargs.pop("prompt_summary", "Bounded redacted prompt payload ref only."),
        prompt_preview=kwargs.pop("prompt_preview", "bounded redacted prompt preview"),
        message_count=kwargs.pop("message_count", 0),
        estimated_prompt_chars=kwargs.pop("estimated_prompt_chars", 0),
        estimated_prompt_tokens=kwargs.pop("estimated_prompt_tokens", None),
        redacted=kwargs.pop("redacted", True),
        truncated=kwargs.pop("truncated", False),
        contains_secret_like_content=kwargs.pop("contains_secret_like_content", False),
        contains_credential_like_content=kwargs.pop("contains_credential_like_content", False),
        contains_token_like_content=kwargs.pop("contains_token_like_content", False),
        **kwargs,
    )


def build_prompt_payload_ref_from_prompt_assembly_output(
    prompt_output: PromptAssemblyOutput,
    prompt_payload_ref_id: str | None = None,
    max_preview_chars: int = DEFAULT_MAX_PROMPT_PREVIEW_CHARS,
    **kwargs: Any,
) -> ModelPromptPayloadRef:
    if not isinstance(prompt_output, PromptAssemblyOutput):
        raise TypeError("prompt_output must be PromptAssemblyOutput")
    if prompt_output.assembled_prompt_text is not None:
        raw_preview = prompt_output.assembled_prompt_text
        payload_format = ModelRequestPayloadFormat.PLAIN_TEXT_PROMPT
    elif prompt_output.assembled_messages:
        raw_preview = "\n".join(f"{item.get('role', 'unknown')}: {item.get('content', '')}" for item in prompt_output.assembled_messages)
        payload_format = ModelRequestPayloadFormat.MESSAGE_LIST
    else:
        raw_preview = "prompt output ref only"
        payload_format = ModelRequestPayloadFormat.PROMPT_REF_ONLY
    preview, redacted, truncated = _redacted_bounded_preview(raw_preview, max_preview_chars)
    source_ref = build_model_request_source_ref(
        f"source:{prompt_output.prompt_output_id}",
        ModelRequestSourceKind.V0332_PROMPT_ASSEMBLY_OUTPUT,
        prompt_output.prompt_output_id,
        "PromptAssemblyOutput metadata source ref; no provider call or raw persistence.",
    )
    return build_model_prompt_payload_ref(
        prompt_payload_ref_id or f"model_prompt_payload_ref:{prompt_output.prompt_output_id}",
        payload_format=kwargs.pop("payload_format", payload_format),
        prompt_output_id=prompt_output.prompt_output_id,
        prompt_summary=kwargs.pop("prompt_summary", "Bounded prompt payload ref derived from PromptAssemblyOutput metadata."),
        prompt_preview=preview,
        message_count=len(prompt_output.assembled_messages),
        estimated_prompt_chars=len(raw_preview),
        estimated_prompt_tokens=prompt_output.token_budget_estimate,
        redacted=kwargs.pop("redacted", redacted or True),
        truncated=kwargs.pop("truncated", truncated),
        source_refs=kwargs.pop("source_refs", [source_ref]),
        **kwargs,
    )


def build_model_request_token_budget(token_budget_id: str = "model_request_token_budget:v0.34.2", **kwargs: Any) -> ModelRequestTokenBudget:
    return ModelRequestTokenBudget(token_budget_id=token_budget_id, **kwargs)


def default_model_request_token_budget(**kwargs: Any) -> ModelRequestTokenBudget:
    return build_model_request_token_budget(**kwargs)


def build_model_request_stop_policy(stop_policy_id: str = "model_request_stop_policy:v0.34.2", **kwargs: Any) -> ModelRequestStopPolicy:
    return ModelRequestStopPolicy(stop_policy_id=stop_policy_id, **kwargs)


def default_model_request_stop_policy(**kwargs: Any) -> ModelRequestStopPolicy:
    return build_model_request_stop_policy(**kwargs)


def build_model_request_timeout_policy(timeout_policy_id: str = "model_request_timeout_policy:v0.34.2", **kwargs: Any) -> ModelRequestTimeoutPolicy:
    return ModelRequestTimeoutPolicy(timeout_policy_id=timeout_policy_id, **kwargs)


def default_model_request_timeout_policy(**kwargs: Any) -> ModelRequestTimeoutPolicy:
    return build_model_request_timeout_policy(**kwargs)


def build_model_request_output_policy(output_policy_id: str = "model_request_output_policy:v0.34.2", **kwargs: Any) -> ModelRequestOutputPolicy:
    return ModelRequestOutputPolicy(output_policy_id=output_policy_id, **kwargs)


def default_model_request_output_policy(**kwargs: Any) -> ModelRequestOutputPolicy:
    return build_model_request_output_policy(**kwargs)


def build_model_request_safety_constraints(safety_constraints_id: str = "model_request_safety_constraints:v0.34.2", **kwargs: Any) -> ModelRequestSafetyConstraints:
    return ModelRequestSafetyConstraints(safety_constraints_id=safety_constraints_id, **kwargs)


def default_model_request_safety_constraints(**kwargs: Any) -> ModelRequestSafetyConstraints:
    return build_model_request_safety_constraints(**kwargs)


def build_model_request_provider_binding(
    provider_binding_id: str = "model_request_provider_binding:v0.34.2",
    provider_profile: ProviderProfileDescriptor | None = None,
    invocation_policy: ProviderInvocationPolicy | None = None,
    **kwargs: Any,
) -> ModelRequestProviderBinding:
    if provider_profile is not None and not provider_profile_descriptor_is_not_invocation(provider_profile):
        raise ValueError("provider_profile must preserve invocation false")
    if invocation_policy is not None and not provider_invocation_policy_blocks_runtime_access(invocation_policy):
        raise ValueError("invocation_policy must block runtime access")
    return ModelRequestProviderBinding(
        provider_binding_id=provider_binding_id,
        provider_profile_id=kwargs.pop("provider_profile_id", None if provider_profile is None else provider_profile.provider_profile_id),
        provider_profile_name=kwargs.pop("provider_profile_name", None if provider_profile is None else provider_profile.profile_name),
        provider_profile_kind=kwargs.pop("provider_profile_kind", None if provider_profile is None else str(provider_profile.profile_kind)),
        provider_boundary_ref_id=kwargs.pop("provider_boundary_ref_id", None),
        invocation_policy_id=kwargs.pop("invocation_policy_id", None if invocation_policy is None else invocation_policy.invocation_policy_id),
        binding_summary=kwargs.pop("binding_summary", "Provider profile binding metadata only; no provider call."),
        future_gated=kwargs.pop("future_gated", bool(provider_profile.future_gated) if provider_profile is not None else False),
        **kwargs,
    )


def build_model_request_envelope_input(
    envelope_input_id: str = "model_request_envelope_input:v0.34.2",
    **kwargs: Any,
) -> ModelRequestEnvelopeInput:
    return ModelRequestEnvelopeInput(
        envelope_input_id=envelope_input_id,
        source_version=kwargs.pop("source_version", V0342_VERSION),
        prompt_output_id=kwargs.pop("prompt_output_id", None),
        runtime_profile_id=kwargs.pop("runtime_profile_id", None),
        session_id=kwargs.pop("session_id", None),
        turn_id=kwargs.pop("turn_id", None),
        provider_profile_id=kwargs.pop("provider_profile_id", None),
        invocation_policy_id=kwargs.pop("invocation_policy_id", None),
        requested_payload_format=kwargs.pop("requested_payload_format", ModelRequestPayloadFormat.REDACTED_PREVIEW_ONLY),
        task_summary=kwargs.pop("task_summary", "Build bounded model request envelope metadata only."),
        **kwargs,
    )


def build_model_request_envelope(
    request_envelope_id: str = "model_request_envelope:v0.34.2",
    **kwargs: Any,
) -> ModelRequestEnvelope:
    return ModelRequestEnvelope(
        request_envelope_id=request_envelope_id,
        version=kwargs.pop("version", V0342_VERSION),
        envelope_kind=kwargs.pop("envelope_kind", ModelRequestEnvelopeKind.PROMPT_ASSEMBLY_REQUEST),
        status=kwargs.pop("status", ModelRequestStatus.VALIDATED_WITH_GAPS),
        readiness_level=kwargs.pop("readiness_level", ModelRequestReadinessLevel.ENVELOPE_VALIDATION_READY),
        payload_ref=kwargs.pop("payload_ref", build_model_prompt_payload_ref()),
        provider_binding=kwargs.pop("provider_binding", build_model_request_provider_binding()),
        token_budget=kwargs.pop("token_budget", default_model_request_token_budget()),
        stop_policy=kwargs.pop("stop_policy", default_model_request_stop_policy()),
        timeout_policy=kwargs.pop("timeout_policy", default_model_request_timeout_policy()),
        output_policy=kwargs.pop("output_policy", default_model_request_output_policy()),
        safety_constraints=kwargs.pop("safety_constraints", default_model_request_safety_constraints()),
        source_refs=kwargs.pop("source_refs", []),
        summary=kwargs.pop("summary", "Model request envelope metadata only; no model/provider invocation."),
        ready_for_v0343_model_response_envelope=kwargs.pop("ready_for_v0343_model_response_envelope", True),
        ready_for_v0344_existing_provider_boundary_adapter=kwargs.pop("ready_for_v0344_existing_provider_boundary_adapter", True),
        **kwargs,
    )


def build_model_request_validation_finding(
    finding_id: str,
    **kwargs: Any,
) -> ModelRequestValidationFinding:
    return ModelRequestValidationFinding(
        finding_id=finding_id,
        request_envelope_id=kwargs.pop("request_envelope_id", None),
        decision_kind=kwargs.pop("decision_kind", ModelRequestValidationDecisionKind.ACCEPT_ENVELOPE_METADATA_ONLY),
        risk_kinds=kwargs.pop("risk_kinds", []),
        summary=kwargs.pop("summary", "Model request envelope metadata accepted without invocation."),
        **kwargs,
    )


def validate_model_prompt_payload_ref(
    payload_ref: ModelPromptPayloadRef,
    constraints: ModelRequestSafetyConstraints | None = None,
) -> ModelRequestValidationFinding:
    if not isinstance(payload_ref, ModelPromptPayloadRef):
        raise TypeError("payload_ref must be ModelPromptPayloadRef")
    if constraints is not None and not isinstance(constraints, ModelRequestSafetyConstraints):
        raise TypeError("constraints must be ModelRequestSafetyConstraints")
    risks: list[ModelRequestRiskKind] = []
    if len(payload_ref.prompt_preview) > DEFAULT_MAX_PROMPT_PREVIEW_CHARS:
        risks.append(ModelRequestRiskKind.UNBOUNDED_PROMPT_RISK)
    if not model_prompt_payload_ref_is_not_raw_persistence(payload_ref):
        risks.append(ModelRequestRiskKind.RAW_PROMPT_PERSISTENCE_RISK)
    if risks:
        return build_model_request_validation_finding(
            f"finding:{payload_ref.prompt_payload_ref_id}:blocked_payload",
            decision_kind=ModelRequestValidationDecisionKind.BLOCK,
            risk_kinds=risks,
            summary="Prompt payload ref failed bounded/redacted metadata validation.",
            blocked=True,
        )
    return build_model_request_validation_finding(
        f"finding:{payload_ref.prompt_payload_ref_id}:payload_ok",
        summary="Prompt payload ref is bounded, redacted, and not raw prompt persistence.",
    )


def build_model_request_validation_report(
    validation_report_id: str = "model_request_validation_report:v0.34.2",
    **kwargs: Any,
) -> ModelRequestValidationReport:
    return ModelRequestValidationReport(
        validation_report_id=validation_report_id,
        version=kwargs.pop("version", V0342_VERSION),
        request_envelope_id=kwargs.pop("request_envelope_id", None),
        findings=kwargs.pop("findings", []),
        validation_passed=kwargs.pop("validation_passed", True),
        blocked_reasons=kwargs.pop("blocked_reasons", []),
        warning_items=kwargs.pop("warning_items", []),
        redaction_applied=kwargs.pop("redaction_applied", True),
        prompt_budget_valid=kwargs.pop("prompt_budget_valid", True),
        output_policy_valid=kwargs.pop("output_policy_valid", True),
        provider_binding_valid=kwargs.pop("provider_binding_valid", True),
        summary=kwargs.pop("summary", "Model request validation report; no invocation certification."),
        **kwargs,
    )


def validate_model_request_envelope(envelope: ModelRequestEnvelope) -> ModelRequestValidationReport:
    if not isinstance(envelope, ModelRequestEnvelope):
        raise TypeError("envelope must be ModelRequestEnvelope")
    findings = [validate_model_prompt_payload_ref(envelope.payload_ref, envelope.safety_constraints)]
    blocked_reasons = [finding.summary for finding in findings if finding.blocked]
    if not model_request_envelope_is_not_invocation(envelope):
        blocked_reasons.append("Envelope attempted to permit invocation or execution.")
    return build_model_request_validation_report(
        request_envelope_id=envelope.request_envelope_id,
        findings=findings,
        validation_passed=not blocked_reasons,
        blocked_reasons=blocked_reasons,
        redaction_applied=envelope.payload_ref.redacted,
        prompt_budget_valid=envelope.token_budget.allow_unbounded_prompt is False,
        output_policy_valid=envelope.output_policy.allow_tool_calls is False and envelope.output_policy.allow_function_calls is False,
        provider_binding_valid=envelope.provider_binding.provider_call is False,
        summary="Model request envelope validated as metadata-only no-invocation artifact.",
    )


def build_model_request_envelope_report(
    report_id: str = "model_request_envelope_report:v0.34.2",
    **kwargs: Any,
) -> ModelRequestEnvelopeReport:
    return ModelRequestEnvelopeReport(
        report_id=report_id,
        version=kwargs.pop("version", V0342_VERSION),
        envelope_input_id=kwargs.pop("envelope_input_id", "model_request_envelope_input:v0.34.2"),
        request_envelope_id=kwargs.pop("request_envelope_id", "model_request_envelope:v0.34.2"),
        validation_report_id=kwargs.pop("validation_report_id", "model_request_validation_report:v0.34.2"),
        status=kwargs.pop("status", ModelRequestStatus.VALIDATED_WITH_GAPS),
        readiness_level=kwargs.pop("readiness_level", ModelRequestReadinessLevel.ENVELOPE_VALIDATION_READY),
        summary=kwargs.pop("summary", "Model request envelope report; no invocation."),
        completed_items=kwargs.pop("completed_items", ["prompt payload ref", "provider binding", "token/stop/timeout/output/safety policies", "validation report"]),
        future_track_items=kwargs.pop("future_track_items", ["model response envelope", "existing provider boundary adapter"]),
        ready_for_v0343_model_response_envelope=kwargs.pop("ready_for_v0343_model_response_envelope", True),
        ready_for_v0344_existing_provider_boundary_adapter=kwargs.pop("ready_for_v0344_existing_provider_boundary_adapter", True),
        **kwargs,
    )


def build_model_request_run_preview(run_preview_id: str = "model_request_run_preview:v0.34.2", **kwargs: Any) -> ModelRequestRunPreview:
    return ModelRequestRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_model_request_no_invocation_guarantee(
    guarantee_id: str = "model_request_no_invocation_guarantee:v0.34.2",
    **kwargs: Any,
) -> ModelRequestNoInvocationGuarantee:
    return ModelRequestNoInvocationGuarantee(guarantee_id=guarantee_id, version=kwargs.pop("version", V0342_VERSION), **kwargs)


def build_v0342_readiness_report(report_id: str = "v0342_readiness_report", **kwargs: Any) -> V0342ReadinessReport:
    return V0342ReadinessReport(
        report_id=report_id,
        version=kwargs.pop("version", V0342_VERSION),
        request_envelope_id=kwargs.pop("request_envelope_id", "model_request_envelope:v0.34.2"),
        envelope_report_id=kwargs.pop("envelope_report_id", "model_request_envelope_report:v0.34.2"),
        validation_report_id=kwargs.pop("validation_report_id", "model_request_validation_report:v0.34.2"),
        summary=kwargs.pop("summary", "v0.34.2 defines Model Request Envelope metadata and validation only; no invocation readiness."),
        ready_for_v0343_model_response_envelope=kwargs.pop("ready_for_v0343_model_response_envelope", True),
        ready_for_v0344_existing_provider_boundary_adapter=kwargs.pop("ready_for_v0344_existing_provider_boundary_adapter", True),
        completed_items=kwargs.pop("completed_items", ["model request envelope", "prompt payload ref", "provider binding", "request policies", "validation report"]),
        future_track_items=kwargs.pop("future_track_items", ["model response envelope", "existing provider boundary adapter"]),
        **kwargs,
    )


def model_request_flags_preserve_invocation_false(flags: ModelRequestFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_MODEL_REQUEST_FLAG_NAMES) and flags.production_certified is False


def model_prompt_payload_ref_is_not_raw_persistence(payload_ref: ModelPromptPayloadRef) -> bool:
    return (
        payload_ref.raw_prompt_persistence is False
        and payload_ref.contains_secret_like_content is False
        and payload_ref.contains_credential_like_content is False
        and payload_ref.contains_token_like_content is False
        and len(payload_ref.prompt_preview) <= DEFAULT_MAX_PROMPT_PREVIEW_CHARS
    )


def model_request_envelope_is_not_invocation(envelope: ModelRequestEnvelope) -> bool:
    return (
        envelope.provider_call is False
        and envelope.ready_for_invocation is False
        and envelope.ready_for_provider_invocation is False
        and envelope.ready_for_execution is False
        and envelope.provider_binding.provider_call is False
        and model_prompt_payload_ref_is_not_raw_persistence(envelope.payload_ref)
    )


def model_request_validation_report_is_not_invocation(report: ModelRequestValidationReport) -> bool:
    return (
        report.invocation_certification is False
        and report.ready_for_invocation is False
        and report.ready_for_provider_invocation is False
        and report.ready_for_execution is False
    )


def v0342_readiness_report_is_not_invocation_ready(report: V0342ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_MODEL_REQUEST_FLAG_NAMES) and report.invocation_readiness is False
