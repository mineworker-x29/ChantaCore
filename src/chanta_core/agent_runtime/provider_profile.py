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


V0341_VERSION = "v0.34.1"
V0341_RELEASE_NAME = "v0.34.1 Provider Profile & Invocation Policy"

DEFAULT_SECRET_LIKE_PATTERNS = [
    ".env",
    "secret",
    "token",
    "key",
    "credential",
    "api_key",
    "password",
]

DEFAULT_PROVIDER_PROFILE_PROHIBITED_UNTIL_LATER_GATE = [
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
    "shell execution",
    "subprocess execution",
    "command execution",
    "workspace write",
    "code edit",
    "patch application",
    "reference code execution",
    "reference import",
    "dependency install",
    "persistent trace write",
    "external trace sink",
    "UI runtime",
    "external control",
    "authority grant",
]

DEFAULT_PROVIDER_PROFILE_WITHDRAWAL_CONDITIONS = [
    "Any provider profile starts invoking a real provider or existing provider boundary.",
    "Any provider SDK, network adapter, credential loader, secret reader, or env reader is introduced.",
    "Any endpoint value, credential value, or raw prompt/response persistence path is introduced.",
    "Any unsafe readiness flag or production_certified becomes true.",
]

UNSAFE_PROVIDER_PROFILE_FLAG_NAMES = (
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
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_patch_application",
    "ready_for_registry_mutation",
    "ready_for_memory_mutation",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
)

FUTURE_GATED_PROVIDER_KINDS = {
    "existing_chat_service_provider",
    "existing_provider_boundary",
    "local_openai_compatible_future_gate",
    "local_lm_studio_future_gate",
    "local_ollama_future_gate",
    "remote_openai_future_gate",
    "remote_claude_future_gate",
    "remote_provider_future_gate",
}


class ProviderProfileKind(StrEnum):
    MOCK_PROVIDER = "mock_provider"
    SUPPLIED_OUTPUT_PROVIDER = "supplied_output_provider"
    EXISTING_CHAT_SERVICE_PROVIDER = "existing_chat_service_provider"
    EXISTING_PROVIDER_BOUNDARY = "existing_provider_boundary"
    LOCAL_OPENAI_COMPATIBLE_FUTURE_GATE = "local_openai_compatible_future_gate"
    LOCAL_LM_STUDIO_FUTURE_GATE = "local_lm_studio_future_gate"
    LOCAL_OLLAMA_FUTURE_GATE = "local_ollama_future_gate"
    REMOTE_OPENAI_FUTURE_GATE = "remote_openai_future_gate"
    REMOTE_CLAUDE_FUTURE_GATE = "remote_claude_future_gate"
    REMOTE_PROVIDER_FUTURE_GATE = "remote_provider_future_gate"
    DISABLED_PROVIDER = "disabled_provider"
    UNKNOWN = "unknown"


class ProviderBoundaryKind(StrEnum):
    NO_BOUNDARY = "no_boundary"
    MOCK_BOUNDARY = "mock_boundary"
    SUPPLIED_OUTPUT_BOUNDARY = "supplied_output_boundary"
    EXISTING_CHAT_SERVICE_BOUNDARY_REF = "existing_chat_service_boundary_ref"
    EXISTING_PROVIDER_BOUNDARY_REF = "existing_provider_boundary_ref"
    FUTURE_LOCAL_PROVIDER_BOUNDARY = "future_local_provider_boundary"
    FUTURE_REMOTE_PROVIDER_BOUNDARY = "future_remote_provider_boundary"
    DIRECT_SDK_BOUNDARY_BLOCKED = "direct_sdk_boundary_blocked"
    DIRECT_NETWORK_BOUNDARY_BLOCKED = "direct_network_boundary_blocked"
    UNKNOWN = "unknown"


class ProviderInvocationModeKind(StrEnum):
    NO_INVOCATION = "no_invocation"
    MOCK_ONLY = "mock_only"
    SUPPLIED_OUTPUT_ONLY = "supplied_output_only"
    EXISTING_BOUNDARY_FUTURE_GATE = "existing_boundary_future_gate"
    CONTROLLED_INVOCATION_FUTURE_GATE = "controlled_invocation_future_gate"
    DIRECT_SDK_BLOCKED = "direct_sdk_blocked"
    DIRECT_NETWORK_BLOCKED = "direct_network_blocked"
    UNKNOWN = "unknown"


class ProviderProfileStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    VALID_METADATA = "valid_metadata"
    VALID_METADATA_WITH_GAPS = "valid_metadata_with_gaps"
    BLOCKED = "blocked"
    DISABLED = "disabled"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class ProviderProfileReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    PROFILE_CONTRACT_READY = "profile_contract_ready"
    METADATA_VALIDATION_READY = "metadata_validation_ready"
    DESIGN_HANDOFF_READY_FOR_V0342 = "design_handoff_ready_for_v0342"
    DESIGN_HANDOFF_READY_FOR_V0343 = "design_handoff_ready_for_v0343"
    DESIGN_HANDOFF_READY_FOR_V0344 = "design_handoff_ready_for_v0344"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class ProviderProfileSourceKind(StrEnum):
    V0340_BOUNDARY = "v0340_boundary"
    V0339_HANDOFF_PACKET = "v0339_handoff_packet"
    EXISTING_CHAT_SERVICE_BOUNDARY_REF = "existing_chat_service_boundary_ref"
    EXISTING_PROVIDER_BOUNDARY_REF = "existing_provider_boundary_ref"
    MANUAL_PROFILE_SPEC = "manual_profile_spec"
    TEST_FIXTURE = "test_fixture"
    REFERENCE_CONTEXT_REF = "reference_context_ref"
    OPENCODE_REFERENCE_CONTEXT_REF = "opencode_reference_context_ref"
    HERMES_REFERENCE_CONTEXT_REF = "hermes_reference_context_ref"
    UNKNOWN = "unknown"


class ProviderProfileTrustLevel(StrEnum):
    TRUSTED_INTERNAL_METADATA = "trusted_internal_metadata"
    BOUNDARY_REF_METADATA = "boundary_ref_metadata"
    MANUAL_SPEC_UNVERIFIED = "manual_spec_unverified"
    TEST_FIXTURE = "test_fixture"
    FUTURE_GATE = "future_gate"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class ProviderProfileRiskKind(StrEnum):
    PROVIDER_INVOCATION_RISK = "provider_invocation_risk"
    PROVIDER_SDK_BYPASS_RISK = "provider_sdk_bypass_risk"
    ARBITRARY_NETWORK_ACCESS_RISK = "arbitrary_network_access_risk"
    CREDENTIAL_EXPOSURE_RISK = "credential_exposure_risk"
    SECRET_READ_RISK = "secret_read_risk"
    ENV_READ_RISK = "env_read_risk"
    ENDPOINT_CONSTRUCTION_RISK = "endpoint_construction_risk"
    RECURSIVE_MODEL_CALL_RISK = "recursive_model_call_risk"
    AUTONOMOUS_LOOP_RISK = "autonomous_loop_risk"
    RAW_PROMPT_LEAK_RISK = "raw_prompt_leak_risk"
    RAW_RESPONSE_PERSISTENCE_RISK = "raw_response_persistence_risk"
    MODEL_OUTPUT_AUTHORITY_RISK = "model_output_authority_risk"
    GENERAL_TOOL_EXECUTION_RISK = "general_tool_execution_risk"
    COMMAND_EXECUTION_RISK = "command_execution_risk"
    WORKSPACE_WRITE_RISK = "workspace_write_risk"
    REFERENCE_EXECUTION_RISK = "reference_execution_risk"
    UNKNOWN = "unknown"


class ProviderProfileValidationDecisionKind(StrEnum):
    ACCEPT_METADATA_ONLY = "accept_metadata_only"
    ACCEPT_FUTURE_GATE_METADATA = "accept_future_gate_metadata"
    DENY = "deny"
    BLOCK = "block"
    DISABLE = "disable"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class ProviderCredentialPosture(StrEnum):
    NO_CREDENTIALS_REQUIRED = "no_credentials_required"
    CREDENTIAL_REF_ONLY = "credential_ref_only"
    EXISTING_BOUNDARY_MANAGED_FUTURE_GATE = "existing_boundary_managed_future_gate"
    DIRECT_ENV_READ_BLOCKED = "direct_env_read_blocked"
    DIRECT_SECRET_FILE_READ_BLOCKED = "direct_secret_file_read_blocked"
    INLINE_SECRET_BLOCKED = "inline_secret_blocked"
    UNKNOWN = "unknown"


class ProviderNetworkPosture(StrEnum):
    NO_NETWORK_REQUIRED = "no_network_required"
    EXISTING_BOUNDARY_MANAGED_FUTURE_GATE = "existing_boundary_managed_future_gate"
    LOCAL_ENDPOINT_FUTURE_GATE = "local_endpoint_future_gate"
    REMOTE_ENDPOINT_FUTURE_GATE = "remote_endpoint_future_gate"
    DIRECT_NETWORK_BLOCKED = "direct_network_blocked"
    ARBITRARY_NETWORK_BLOCKED = "arbitrary_network_blocked"
    UNKNOWN = "unknown"


def _validate_version_includes_v0341(version: str) -> None:
    _require_non_blank("version", version)
    if V0341_VERSION not in version:
        raise ValueError("version must include v0.34.1")


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.34.1")


def _validate_true(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not True:
            raise ValueError(f"{name} must always be True in v0.34.1")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise TypeError(f"{name} must be dict[str, Any]")


def _validate_enum_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _validate_metadata_no_invocation(metadata: dict[str, Any]) -> None:
    _validate_dict("metadata", metadata)
    if _metadata_flag_true(
        metadata,
        {
            "provider_call",
            "provider_invocation",
            "existing_boundary_invocation",
            "provider_sdk_import",
            "network_call",
            "credential_access",
            "secret_read",
            "env_read",
            "endpoint_construction",
            "execution",
            "workspace_write",
            "adapter_created",
            "credential_loader_created",
            "network_adapter_created",
        },
    ):
        raise ValueError("v0.34.1 metadata cannot imply invocation or external access")


def _validate_secret_like_patterns(values: list[str]) -> None:
    _validate_string_list("prohibited patterns", values)
    lowered = " | ".join(values).lower()
    missing = [term for term in DEFAULT_SECRET_LIKE_PATTERNS if term not in lowered]
    if missing:
        raise ValueError(f"patterns must include secret-like defaults: {missing}")


def _looks_like_secret_value(value: str | None) -> bool:
    if value is None:
        return False
    lowered = value.strip().lower()
    return lowered.startswith("sk-") or any(marker in lowered for marker in ("secret=", "token=", "key=", "credential=", "api_key=", "password="))


def _validate_no_secret_values(name: str, values: list[str | None]) -> None:
    for value in values:
        if _looks_like_secret_value(value):
            raise ValueError(f"{name} must not contain secret-like values")


def _validate_contains_terms(name: str, values: list[str], terms: list[str]) -> None:
    _validate_string_list(name, values)
    lowered = " | ".join(values).lower()
    missing = [term for term in terms if term.lower() not in lowered]
    if missing:
        raise ValueError(f"{name} missing required terms: {missing}")


@dataclass(frozen=True)
class ProviderProfileFlagSet:
    flag_set_id: str
    version: str = V0341_VERSION
    provider_profile_registry_constructed: bool = False
    provider_profile_validation_available: bool = False
    provider_invocation_policy_defined: bool = False
    ready_for_v0342_model_request_envelope: bool = False
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
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_application: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version_includes_v0341(self.version)
        _validate_false(self, UNSAFE_PROVIDER_PROFILE_FLAG_NAMES)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False in v0.34.1")
        _validate_metadata_no_invocation(self.metadata)


@dataclass(frozen=True)
class ProviderProfileSourceRef:
    source_ref_id: str
    source_kind: ProviderProfileSourceKind | str
    source_id: str
    source_summary: str
    trust_level: ProviderProfileTrustLevel | str = ProviderProfileTrustLevel.TRUSTED_INTERNAL_METADATA
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        ProviderProfileSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        ProviderProfileTrustLevel(self.trust_level)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_invocation(self.metadata)

    @property
    def provider_call(self) -> bool:
        return False

    @property
    def credential_access(self) -> bool:
        return False

    @property
    def network_access(self) -> bool:
        return False

    @property
    def file_read(self) -> bool:
        return False


@dataclass(frozen=True)
class ProviderCredentialPolicy:
    credential_policy_id: str
    credential_posture: ProviderCredentialPosture | str = ProviderCredentialPosture.NO_CREDENTIALS_REQUIRED
    credential_ref_name: str | None = None
    required_credential_refs: list[str] = field(default_factory=list)
    prohibited_credential_sources: list[str] = field(default_factory=lambda: [".env", "secret files", "inline secret values", "OS credential env"])
    allow_env_read: bool = False
    allow_secret_file_read: bool = False
    allow_inline_secret: bool = False
    allow_credential_value_storage: bool = False
    allow_credential_logging: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("credential_policy_id", self.credential_policy_id)
        ProviderCredentialPosture(self.credential_posture)
        _validate_string_list("required_credential_refs", self.required_credential_refs)
        _validate_string_list("prohibited_credential_sources", self.prohibited_credential_sources)
        _validate_false(
            self,
            (
                "allow_env_read",
                "allow_secret_file_read",
                "allow_inline_secret",
                "allow_credential_value_storage",
                "allow_credential_logging",
            ),
        )
        _validate_no_secret_values("credential refs", [self.credential_ref_name, *self.required_credential_refs])
        _validate_metadata_no_invocation(self.metadata)

    @property
    def contains_secret_values(self) -> bool:
        return False


@dataclass(frozen=True)
class ProviderNetworkPolicy:
    network_policy_id: str
    network_posture: ProviderNetworkPosture | str = ProviderNetworkPosture.NO_NETWORK_REQUIRED
    endpoint_ref_name: str | None = None
    endpoint_url_value: str | None = None
    allowed_endpoint_refs: list[str] = field(default_factory=list)
    prohibited_endpoint_patterns: list[str] = field(default_factory=lambda: ["direct URL values", "localhost direct calls", "remote direct calls", "arbitrary endpoints"])
    allow_direct_network: bool = False
    allow_endpoint_value_storage: bool = False
    allow_arbitrary_endpoint: bool = False
    allow_localhost_direct_call: bool = False
    allow_remote_direct_call: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("network_policy_id", self.network_policy_id)
        ProviderNetworkPosture(self.network_posture)
        _validate_string_list("allowed_endpoint_refs", self.allowed_endpoint_refs)
        _validate_string_list("prohibited_endpoint_patterns", self.prohibited_endpoint_patterns)
        if self.endpoint_url_value is not None:
            raise ValueError("endpoint_url_value must be None in v0.34.1")
        _validate_false(
            self,
            (
                "allow_direct_network",
                "allow_endpoint_value_storage",
                "allow_arbitrary_endpoint",
                "allow_localhost_direct_call",
                "allow_remote_direct_call",
            ),
        )
        _validate_metadata_no_invocation(self.metadata)

    @property
    def network_access(self) -> bool:
        return False


@dataclass(frozen=True)
class ProviderInvocationLimitPolicy:
    limit_policy_id: str
    max_prompt_chars: int = 12000
    max_response_chars: int = 12000
    max_tokens: int | None = None
    timeout_seconds: int | None = None
    max_retries: int = 0
    allow_retries: bool = False
    allow_streaming: bool = False
    allow_tool_calls: bool = False
    allow_function_calls: bool = False
    allow_recursive_calls: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("limit_policy_id", self.limit_policy_id)
        for name in ("max_prompt_chars", "max_response_chars", "max_tokens", "timeout_seconds", "max_retries"):
            value = getattr(self, name)
            if value is not None and value < 0:
                raise ValueError(f"{name} must be >= 0")
        if self.max_retries != 0:
            raise ValueError("max_retries must be 0 in v0.34.1")
        _validate_false(
            self,
            (
                "allow_retries",
                "allow_streaming",
                "allow_tool_calls",
                "allow_function_calls",
                "allow_recursive_calls",
            ),
        )
        _validate_metadata_no_invocation(self.metadata)

    @property
    def invocation_constraint_metadata_only(self) -> bool:
        return True


@dataclass(frozen=True)
class ProviderPromptDataPolicy:
    prompt_data_policy_id: str
    allow_raw_prompt_persistence: bool = False
    allow_secret_in_prompt: bool = False
    allow_credential_in_prompt: bool = False
    allow_file_content_in_prompt: bool = False
    allow_unbounded_prompt: bool = False
    redaction_required: bool = True
    max_prompt_preview_chars: int = 2000
    prohibited_prompt_patterns: list[str] = field(default_factory=lambda: list(DEFAULT_SECRET_LIKE_PATTERNS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("prompt_data_policy_id", self.prompt_data_policy_id)
        _validate_false(
            self,
            (
                "allow_raw_prompt_persistence",
                "allow_secret_in_prompt",
                "allow_credential_in_prompt",
                "allow_file_content_in_prompt",
                "allow_unbounded_prompt",
            ),
        )
        if self.redaction_required is not True:
            raise ValueError("redaction_required should remain True in v0.34.1")
        if self.max_prompt_preview_chars < 0:
            raise ValueError("max_prompt_preview_chars must be >= 0")
        _validate_secret_like_patterns(self.prohibited_prompt_patterns)
        _validate_metadata_no_invocation(self.metadata)


@dataclass(frozen=True)
class ProviderResponseDataPolicy:
    response_data_policy_id: str
    allow_raw_response_persistence: bool = False
    allow_untrusted_response_as_action: bool = False
    allow_response_tool_calls: bool = False
    allow_response_patch: bool = False
    allow_response_command: bool = False
    allow_unbounded_response: bool = False
    redaction_required: bool = True
    quarantine_required: bool = True
    max_response_preview_chars: int = 2000
    prohibited_response_patterns: list[str] = field(default_factory=lambda: list(DEFAULT_SECRET_LIKE_PATTERNS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("response_data_policy_id", self.response_data_policy_id)
        _validate_false(
            self,
            (
                "allow_raw_response_persistence",
                "allow_untrusted_response_as_action",
                "allow_response_tool_calls",
                "allow_response_patch",
                "allow_response_command",
                "allow_unbounded_response",
            ),
        )
        if self.redaction_required is not True:
            raise ValueError("redaction_required should remain True in v0.34.1")
        if self.quarantine_required is not True:
            raise ValueError("quarantine_required should remain True in v0.34.1")
        if self.max_response_preview_chars < 0:
            raise ValueError("max_response_preview_chars must be >= 0")
        _validate_secret_like_patterns(self.prohibited_response_patterns)
        _validate_metadata_no_invocation(self.metadata)


@dataclass(frozen=True)
class ProviderProfileDescriptor:
    provider_profile_id: str
    profile_name: str
    profile_kind: ProviderProfileKind | str
    boundary_kind: ProviderBoundaryKind | str
    invocation_mode: ProviderInvocationModeKind | str
    credential_policy: ProviderCredentialPolicy
    network_policy: ProviderNetworkPolicy
    limit_policy: ProviderInvocationLimitPolicy
    prompt_data_policy: ProviderPromptDataPolicy
    response_data_policy: ProviderResponseDataPolicy
    source_refs: list[ProviderProfileSourceRef] = field(default_factory=list)
    status: ProviderProfileStatus | str = ProviderProfileStatus.VALID_METADATA
    readiness_level: ProviderProfileReadinessLevel | str = ProviderProfileReadinessLevel.METADATA_VALIDATION_READY
    description: str = "Provider profile metadata only."
    enabled: bool = False
    future_gated: bool = False
    invocation_allowed: bool = False
    provider_sdk_allowed: bool = False
    network_allowed: bool = False
    credential_access_allowed: bool = False
    secret_read_allowed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("provider_profile_id", self.provider_profile_id)
        _require_non_blank("profile_name", self.profile_name)
        profile_kind = ProviderProfileKind(self.profile_kind)
        ProviderBoundaryKind(self.boundary_kind)
        ProviderInvocationModeKind(self.invocation_mode)
        if not isinstance(self.credential_policy, ProviderCredentialPolicy):
            raise TypeError("credential_policy must be ProviderCredentialPolicy")
        if not isinstance(self.network_policy, ProviderNetworkPolicy):
            raise TypeError("network_policy must be ProviderNetworkPolicy")
        if not isinstance(self.limit_policy, ProviderInvocationLimitPolicy):
            raise TypeError("limit_policy must be ProviderInvocationLimitPolicy")
        if not isinstance(self.prompt_data_policy, ProviderPromptDataPolicy):
            raise TypeError("prompt_data_policy must be ProviderPromptDataPolicy")
        if not isinstance(self.response_data_policy, ProviderResponseDataPolicy):
            raise TypeError("response_data_policy must be ProviderResponseDataPolicy")
        _validate_object_list("source_refs", self.source_refs, ProviderProfileSourceRef)
        ProviderProfileStatus(self.status)
        ProviderProfileReadinessLevel(self.readiness_level)
        _require_non_blank("description", self.description)
        _validate_false(
            self,
            (
                "invocation_allowed",
                "provider_sdk_allowed",
                "network_allowed",
                "credential_access_allowed",
                "secret_read_allowed",
            ),
        )
        if profile_kind.value in FUTURE_GATED_PROVIDER_KINDS and self.future_gated is not True:
            raise ValueError("existing/local/remote provider profiles must be future_gated metadata only in v0.34.1")
        _validate_metadata_no_invocation(self.metadata)

    @property
    def provider_runtime(self) -> bool:
        return False


@dataclass(frozen=True)
class ProviderProfileRegistry:
    registry_id: str
    version: str
    descriptors: list[ProviderProfileDescriptor]
    descriptor_ids: list[str]
    enabled_profile_names: list[str]
    disabled_profile_names: list[str]
    blocked_profile_names: list[str]
    future_gated_profile_names: list[str]
    flags: ProviderProfileFlagSet
    source_refs: list[ProviderProfileSourceRef]
    summary: str
    ready_for_v0342_model_request_envelope: bool = False
    ready_for_v0343_model_response_envelope: bool = False
    ready_for_v0344_existing_provider_boundary_adapter: bool = False
    ready_for_invocation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("registry_id", self.registry_id)
        _validate_version_includes_v0341(self.version)
        _validate_object_list("descriptors", self.descriptors, ProviderProfileDescriptor)
        for name in ("descriptor_ids", "enabled_profile_names", "disabled_profile_names", "blocked_profile_names", "future_gated_profile_names"):
            _validate_string_list(name, getattr(self, name))
        if not isinstance(self.flags, ProviderProfileFlagSet):
            raise TypeError("flags must be ProviderProfileFlagSet")
        if not provider_profile_flags_preserve_invocation_false(self.flags):
            raise ValueError("flags must preserve unsafe provider readiness false")
        _validate_object_list("source_refs", self.source_refs, ProviderProfileSourceRef)
        _require_non_blank("summary", self.summary)
        if (self.ready_for_v0342_model_request_envelope or self.ready_for_v0343_model_response_envelope or self.ready_for_v0344_existing_provider_boundary_adapter) and self.blocked_profile_names:
            raise ValueError("design-stage handoff readiness is not allowed with blocked profiles")
        _validate_false(self, ("ready_for_invocation", "ready_for_execution"))
        _validate_metadata_no_invocation(self.metadata)

    @property
    def provider_runtime(self) -> bool:
        return False


@dataclass(frozen=True)
class ProviderInvocationPolicy:
    invocation_policy_id: str
    version: str
    allowed_profile_kinds: list[ProviderProfileKind | str] = field(default_factory=list)
    blocked_profile_kinds: list[ProviderProfileKind | str] = field(default_factory=list)
    future_gated_profile_kinds: list[ProviderProfileKind | str] = field(default_factory=list)
    required_credential_postures: list[ProviderCredentialPosture | str] = field(default_factory=list)
    required_network_postures: list[ProviderNetworkPosture | str] = field(default_factory=list)
    prohibited_risks: list[ProviderProfileRiskKind | str] = field(default_factory=list)
    allow_mock_provider: bool = True
    allow_supplied_output_provider: bool = True
    allow_existing_boundary_ref: bool = True
    allow_existing_boundary_invocation: bool = False
    allow_local_provider_invocation: bool = False
    allow_remote_provider_invocation: bool = False
    allow_direct_provider_sdk: bool = False
    allow_direct_network: bool = False
    allow_credential_read: bool = False
    allow_secret_read: bool = False
    allow_tool_calls: bool = False
    allow_recursive_calls: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("invocation_policy_id", self.invocation_policy_id)
        _validate_version_includes_v0341(self.version)
        _validate_enum_list("allowed_profile_kinds", self.allowed_profile_kinds, ProviderProfileKind)
        _validate_enum_list("blocked_profile_kinds", self.blocked_profile_kinds, ProviderProfileKind)
        _validate_enum_list("future_gated_profile_kinds", self.future_gated_profile_kinds, ProviderProfileKind)
        _validate_enum_list("required_credential_postures", self.required_credential_postures, ProviderCredentialPosture)
        _validate_enum_list("required_network_postures", self.required_network_postures, ProviderNetworkPosture)
        _validate_enum_list("prohibited_risks", self.prohibited_risks, ProviderProfileRiskKind)
        _validate_false(
            self,
            (
                "allow_existing_boundary_invocation",
                "allow_local_provider_invocation",
                "allow_remote_provider_invocation",
                "allow_direct_provider_sdk",
                "allow_direct_network",
                "allow_credential_read",
                "allow_secret_read",
                "allow_tool_calls",
                "allow_recursive_calls",
            ),
        )
        _validate_metadata_no_invocation(self.metadata)

    @property
    def invocation_permission(self) -> bool:
        return False


@dataclass(frozen=True)
class ProviderProfileValidationFinding:
    finding_id: str
    provider_profile_id: str | None
    decision_kind: ProviderProfileValidationDecisionKind | str
    risk_kinds: list[ProviderProfileRiskKind | str]
    summary: str
    blocked: bool = False
    future_gated: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        ProviderProfileValidationDecisionKind(self.decision_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, ProviderProfileRiskKind)
        _require_non_blank("summary", self.summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_invocation(self.metadata)

    @property
    def invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class ProviderProfileValidationReport:
    validation_report_id: str
    version: str
    registry_id: str | None
    descriptor_ids_checked: list[str]
    valid_metadata_profile_ids: list[str]
    blocked_profile_ids: list[str]
    future_gated_profile_ids: list[str]
    findings: list[ProviderProfileValidationFinding]
    validation_passed: bool
    summary: str
    ready_for_invocation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version_includes_v0341(self.version)
        for name in ("descriptor_ids_checked", "valid_metadata_profile_ids", "blocked_profile_ids", "future_gated_profile_ids"):
            _validate_string_list(name, getattr(self, name))
        _validate_object_list("findings", self.findings, ProviderProfileValidationFinding)
        if self.validation_passed is True and self.blocked_profile_ids:
            raise ValueError("validation_passed cannot be True if blocked_profile_ids is non-empty")
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_invocation", "ready_for_execution"))
        _validate_metadata_no_invocation(self.metadata)

    @property
    def runtime_certification(self) -> bool:
        return False


@dataclass(frozen=True)
class ProviderProfileResolutionInput:
    resolution_input_id: str
    source_version: str
    requested_profile_name: str | None
    requested_profile_kind: ProviderProfileKind | str
    registry_id: str | None
    invocation_policy_id: str | None
    source_refs: list[ProviderProfileSourceRef]
    task_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("resolution_input_id", self.resolution_input_id)
        _validate_version_includes_v0341(self.source_version)
        ProviderProfileKind(self.requested_profile_kind)
        _validate_object_list("source_refs", self.source_refs, ProviderProfileSourceRef)
        _require_non_blank("task_summary", self.task_summary)
        _validate_metadata_no_invocation(self.metadata)

    @property
    def provider_invocation_request(self) -> bool:
        return False


@dataclass(frozen=True)
class ProviderProfileResolutionDecision:
    resolution_decision_id: str
    resolution_input_id: str
    selected_provider_profile_id: str | None
    selected_profile_kind: ProviderProfileKind | str | None
    decision_kind: ProviderProfileValidationDecisionKind | str
    reason: str
    invocation_allowed: bool = False
    provider_invocation_allowed: bool = False
    network_allowed: bool = False
    credential_access_allowed: bool = False
    secret_read_allowed: bool = False
    future_gated: bool = False
    risk_kinds: list[ProviderProfileRiskKind | str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("resolution_decision_id", self.resolution_decision_id)
        _require_non_blank("resolution_input_id", self.resolution_input_id)
        if self.selected_profile_kind is not None:
            ProviderProfileKind(self.selected_profile_kind)
        ProviderProfileValidationDecisionKind(self.decision_kind)
        _require_non_blank("reason", self.reason)
        _validate_false(
            self,
            (
                "invocation_allowed",
                "provider_invocation_allowed",
                "network_allowed",
                "credential_access_allowed",
                "secret_read_allowed",
            ),
        )
        _validate_enum_list("risk_kinds", self.risk_kinds, ProviderProfileRiskKind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_invocation(self.metadata)

    @property
    def provider_invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class ProviderProfileResolutionReport:
    report_id: str
    version: str
    resolution_input_id: str
    resolution_decision_id: str | None
    selected_provider_profile_id: str | None
    status: ProviderProfileStatus | str
    readiness_level: ProviderProfileReadinessLevel | str
    summary: str
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0342_model_request_envelope: bool = False
    ready_for_v0343_model_response_envelope: bool = False
    ready_for_v0344_existing_provider_boundary_adapter: bool = False
    ready_for_invocation: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0341(self.version)
        _require_non_blank("resolution_input_id", self.resolution_input_id)
        ProviderProfileStatus(self.status)
        ProviderProfileReadinessLevel(self.readiness_level)
        _require_non_blank("summary", self.summary)
        for name in ("completed_items", "blocked_items", "future_track_items", "gaps", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        if (self.ready_for_v0342_model_request_envelope or self.ready_for_v0343_model_response_envelope or self.ready_for_v0344_existing_provider_boundary_adapter) and self.blocked_items:
            raise ValueError("design-stage handoff readiness is not allowed with blocked_items")
        _validate_false(self, ("ready_for_invocation", "ready_for_execution"))
        _validate_metadata_no_invocation(self.metadata)

    @property
    def invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class ProviderProfileRunPreview:
    run_preview_id: str
    registry_id: str | None = None
    planned_steps: list[str] = field(default_factory=lambda: ["construct provider profile metadata", "validate metadata-only policies", "produce no-invocation readiness report"])
    expected_artifacts: list[str] = field(default_factory=lambda: ["ProviderProfileRegistry", "ProviderInvocationPolicy", "ProviderProfileValidationReport", "V0341ReadinessReport"])
    explicitly_not_performed: list[str] = field(default_factory=lambda: list(DEFAULT_PROVIDER_PROFILE_PROHIBITED_UNTIL_LATER_GATE))
    no_model_invocation_guarantee: bool = True
    no_provider_invocation_guarantee: bool = True
    no_provider_sdk_invocation_guarantee: bool = True
    no_network_access_guarantee: bool = True
    no_credential_access_guarantee: bool = True
    no_secret_read_guarantee: bool = True
    no_env_read_guarantee: bool = True
    no_agent_step_execution_guarantee: bool = True
    no_tool_execution_guarantee: bool = True
    no_command_execution_guarantee: bool = True
    no_workspace_write_guarantee: bool = True
    no_code_edit_guarantee: bool = True
    no_patch_application_guarantee: bool = True
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
                raise ValueError(f"{name} must be True in v0.34.1")
        _validate_metadata_no_invocation(self.metadata)

    @property
    def invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class ProviderProfileNoInvocationGuarantee:
    guarantee_id: str
    version: str = V0341_VERSION
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
    no_shell_execution: bool = True
    no_subprocess: bool = True
    no_command_execution: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_patch_application: bool = True
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
        _validate_version_includes_v0341(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.34.1")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_invocation(self.metadata)


@dataclass(frozen=True)
class V0341ReadinessReport:
    report_id: str
    version: str
    registry_id: str | None
    invocation_policy_id: str | None
    validation_report_id: str | None
    resolution_report_id: str | None
    summary: str
    ready_for_v0342_model_request_envelope: bool = False
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
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_application: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_PROVIDER_PROFILE_PROHIBITED_UNTIL_LATER_GATE))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=lambda: list(DEFAULT_PROVIDER_PROFILE_WITHDRAWAL_CONDITIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0341(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(self, UNSAFE_PROVIDER_PROFILE_FLAG_NAMES)
        for name in ("completed_items", "blocked_items", "future_track_items", "prohibited_until_later_gate", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_contains_terms(
            "prohibited_until_later_gate",
            self.prohibited_until_later_gate,
            [
                "controlled model invocation",
                "provider invocation",
                "existing boundary invocation",
                "network access",
                "credential access",
                "secret read",
                "env read",
                "endpoint construction",
                "agent step execution",
                "general tool execution",
                "shell",
                "workspace write",
                "reference code execution",
                "persistent trace write",
                "UI runtime",
                "authority grant",
            ],
        )
        if (self.ready_for_v0342_model_request_envelope or self.ready_for_v0343_model_response_envelope or self.ready_for_v0344_existing_provider_boundary_adapter) and self.blocked_items:
            raise ValueError("design-stage handoff readiness is not allowed with blocked_items")
        _validate_metadata_no_invocation(self.metadata)

    @property
    def invocation_readiness(self) -> bool:
        return False


def build_provider_profile_flags(
    flag_set_id: str = "provider_profile_flags:v0.34.1",
    **kwargs: Any,
) -> ProviderProfileFlagSet:
    return ProviderProfileFlagSet(
        flag_set_id=flag_set_id,
        version=kwargs.pop("version", V0341_VERSION),
        provider_profile_registry_constructed=kwargs.pop("provider_profile_registry_constructed", True),
        provider_profile_validation_available=kwargs.pop("provider_profile_validation_available", True),
        provider_invocation_policy_defined=kwargs.pop("provider_invocation_policy_defined", True),
        ready_for_v0342_model_request_envelope=kwargs.pop("ready_for_v0342_model_request_envelope", True),
        ready_for_v0343_model_response_envelope=kwargs.pop("ready_for_v0343_model_response_envelope", True),
        ready_for_v0344_existing_provider_boundary_adapter=kwargs.pop("ready_for_v0344_existing_provider_boundary_adapter", True),
        **kwargs,
    )


def build_provider_profile_source_ref(
    source_ref_id: str,
    source_kind: ProviderProfileSourceKind | str = ProviderProfileSourceKind.MANUAL_PROFILE_SPEC,
    source_id: str = "provider_profile_source",
    source_summary: str = "Provider profile source ref only; no fetch/read/execute.",
    **kwargs: Any,
) -> ProviderProfileSourceRef:
    return ProviderProfileSourceRef(
        source_ref_id=source_ref_id,
        source_kind=source_kind,
        source_id=source_id,
        source_summary=source_summary,
        **kwargs,
    )


def build_provider_credential_policy(
    credential_policy_id: str = "provider_credential_policy:v0.34.1",
    **kwargs: Any,
) -> ProviderCredentialPolicy:
    return ProviderCredentialPolicy(credential_policy_id=credential_policy_id, **kwargs)


def build_provider_network_policy(
    network_policy_id: str = "provider_network_policy:v0.34.1",
    **kwargs: Any,
) -> ProviderNetworkPolicy:
    return ProviderNetworkPolicy(network_policy_id=network_policy_id, **kwargs)


def build_provider_invocation_limit_policy(
    limit_policy_id: str = "provider_invocation_limit_policy:v0.34.1",
    **kwargs: Any,
) -> ProviderInvocationLimitPolicy:
    return ProviderInvocationLimitPolicy(limit_policy_id=limit_policy_id, **kwargs)


def build_provider_prompt_data_policy(
    prompt_data_policy_id: str = "provider_prompt_data_policy:v0.34.1",
    **kwargs: Any,
) -> ProviderPromptDataPolicy:
    return ProviderPromptDataPolicy(prompt_data_policy_id=prompt_data_policy_id, **kwargs)


def build_provider_response_data_policy(
    response_data_policy_id: str = "provider_response_data_policy:v0.34.1",
    **kwargs: Any,
) -> ProviderResponseDataPolicy:
    return ProviderResponseDataPolicy(response_data_policy_id=response_data_policy_id, **kwargs)


def build_provider_profile_descriptor(
    provider_profile_id: str,
    profile_name: str,
    profile_kind: ProviderProfileKind | str,
    **kwargs: Any,
) -> ProviderProfileDescriptor:
    profile_kind_value = ProviderProfileKind(profile_kind)
    is_mock = profile_kind_value == ProviderProfileKind.MOCK_PROVIDER
    is_supplied = profile_kind_value == ProviderProfileKind.SUPPLIED_OUTPUT_PROVIDER
    future_gated = profile_kind_value.value in FUTURE_GATED_PROVIDER_KINDS
    return ProviderProfileDescriptor(
        provider_profile_id=provider_profile_id,
        profile_name=profile_name,
        profile_kind=profile_kind_value,
        boundary_kind=kwargs.pop(
            "boundary_kind",
            ProviderBoundaryKind.MOCK_BOUNDARY if is_mock else ProviderBoundaryKind.SUPPLIED_OUTPUT_BOUNDARY if is_supplied else ProviderBoundaryKind.EXISTING_PROVIDER_BOUNDARY_REF,
        ),
        invocation_mode=kwargs.pop(
            "invocation_mode",
            ProviderInvocationModeKind.MOCK_ONLY if is_mock else ProviderInvocationModeKind.SUPPLIED_OUTPUT_ONLY if is_supplied else ProviderInvocationModeKind.EXISTING_BOUNDARY_FUTURE_GATE,
        ),
        credential_policy=kwargs.pop("credential_policy", build_provider_credential_policy()),
        network_policy=kwargs.pop("network_policy", build_provider_network_policy()),
        limit_policy=kwargs.pop("limit_policy", build_provider_invocation_limit_policy()),
        prompt_data_policy=kwargs.pop("prompt_data_policy", build_provider_prompt_data_policy()),
        response_data_policy=kwargs.pop("response_data_policy", build_provider_response_data_policy()),
        source_refs=kwargs.pop("source_refs", [build_provider_profile_source_ref(f"source:{provider_profile_id}", ProviderProfileSourceKind.MANUAL_PROFILE_SPEC, provider_profile_id, "Provider profile metadata source ref only.")]),
        status=kwargs.pop("status", ProviderProfileStatus.VALID_METADATA_WITH_GAPS if future_gated else ProviderProfileStatus.VALID_METADATA),
        readiness_level=kwargs.pop("readiness_level", ProviderProfileReadinessLevel.METADATA_VALIDATION_READY if not future_gated else ProviderProfileReadinessLevel.FUTURE_TRACK),
        description=kwargs.pop("description", "Provider profile descriptor metadata only; no invocation is allowed."),
        enabled=kwargs.pop("enabled", bool(is_mock or is_supplied)),
        future_gated=kwargs.pop("future_gated", future_gated),
        **kwargs,
    )


def default_mock_provider_profile_descriptor(**kwargs: Any) -> ProviderProfileDescriptor:
    return build_provider_profile_descriptor(
        kwargs.pop("provider_profile_id", "provider_profile:mock:v0.34.1"),
        kwargs.pop("profile_name", "mock_provider"),
        ProviderProfileKind.MOCK_PROVIDER,
        **kwargs,
    )


def default_supplied_output_provider_profile_descriptor(**kwargs: Any) -> ProviderProfileDescriptor:
    return build_provider_profile_descriptor(
        kwargs.pop("provider_profile_id", "provider_profile:supplied_output:v0.34.1"),
        kwargs.pop("profile_name", "supplied_output_provider"),
        ProviderProfileKind.SUPPLIED_OUTPUT_PROVIDER,
        **kwargs,
    )


def build_provider_profile_registry(
    registry_id: str = "provider_profile_registry:v0.34.1",
    **kwargs: Any,
) -> ProviderProfileRegistry:
    descriptors = kwargs.pop("descriptors", [default_mock_provider_profile_descriptor(), default_supplied_output_provider_profile_descriptor()])
    return ProviderProfileRegistry(
        registry_id=registry_id,
        version=kwargs.pop("version", V0341_VERSION),
        descriptors=descriptors,
        descriptor_ids=kwargs.pop("descriptor_ids", [descriptor.provider_profile_id for descriptor in descriptors]),
        enabled_profile_names=kwargs.pop("enabled_profile_names", [descriptor.profile_name for descriptor in descriptors if descriptor.enabled]),
        disabled_profile_names=kwargs.pop("disabled_profile_names", [descriptor.profile_name for descriptor in descriptors if ProviderProfileStatus(descriptor.status) == ProviderProfileStatus.DISABLED]),
        blocked_profile_names=kwargs.pop("blocked_profile_names", [descriptor.profile_name for descriptor in descriptors if ProviderProfileStatus(descriptor.status) == ProviderProfileStatus.BLOCKED]),
        future_gated_profile_names=kwargs.pop("future_gated_profile_names", [descriptor.profile_name for descriptor in descriptors if descriptor.future_gated]),
        flags=kwargs.pop("flags", build_provider_profile_flags()),
        source_refs=kwargs.pop("source_refs", []),
        summary=kwargs.pop("summary", "Provider profile registry metadata only; no provider runtime or invocation."),
        ready_for_v0342_model_request_envelope=kwargs.pop("ready_for_v0342_model_request_envelope", True),
        ready_for_v0343_model_response_envelope=kwargs.pop("ready_for_v0343_model_response_envelope", True),
        ready_for_v0344_existing_provider_boundary_adapter=kwargs.pop("ready_for_v0344_existing_provider_boundary_adapter", True),
        **kwargs,
    )


def default_provider_invocation_policy(**kwargs: Any) -> ProviderInvocationPolicy:
    return build_provider_invocation_policy(**kwargs)


def build_provider_invocation_policy(
    invocation_policy_id: str = "provider_invocation_policy:v0.34.1",
    **kwargs: Any,
) -> ProviderInvocationPolicy:
    return ProviderInvocationPolicy(
        invocation_policy_id=invocation_policy_id,
        version=kwargs.pop("version", V0341_VERSION),
        allowed_profile_kinds=kwargs.pop("allowed_profile_kinds", [ProviderProfileKind.MOCK_PROVIDER, ProviderProfileKind.SUPPLIED_OUTPUT_PROVIDER]),
        blocked_profile_kinds=kwargs.pop("blocked_profile_kinds", [ProviderProfileKind.DISABLED_PROVIDER, ProviderProfileKind.UNKNOWN]),
        future_gated_profile_kinds=kwargs.pop("future_gated_profile_kinds", [ProviderProfileKind(value) for value in FUTURE_GATED_PROVIDER_KINDS]),
        required_credential_postures=kwargs.pop(
            "required_credential_postures",
            [ProviderCredentialPosture.NO_CREDENTIALS_REQUIRED, ProviderCredentialPosture.CREDENTIAL_REF_ONLY, ProviderCredentialPosture.EXISTING_BOUNDARY_MANAGED_FUTURE_GATE],
        ),
        required_network_postures=kwargs.pop(
            "required_network_postures",
            [ProviderNetworkPosture.NO_NETWORK_REQUIRED, ProviderNetworkPosture.EXISTING_BOUNDARY_MANAGED_FUTURE_GATE, ProviderNetworkPosture.LOCAL_ENDPOINT_FUTURE_GATE, ProviderNetworkPosture.REMOTE_ENDPOINT_FUTURE_GATE],
        ),
        prohibited_risks=kwargs.pop(
            "prohibited_risks",
            [
                ProviderProfileRiskKind.PROVIDER_INVOCATION_RISK,
                ProviderProfileRiskKind.PROVIDER_SDK_BYPASS_RISK,
                ProviderProfileRiskKind.ARBITRARY_NETWORK_ACCESS_RISK,
                ProviderProfileRiskKind.CREDENTIAL_EXPOSURE_RISK,
                ProviderProfileRiskKind.SECRET_READ_RISK,
                ProviderProfileRiskKind.ENV_READ_RISK,
                ProviderProfileRiskKind.ENDPOINT_CONSTRUCTION_RISK,
                ProviderProfileRiskKind.RECURSIVE_MODEL_CALL_RISK,
                ProviderProfileRiskKind.AUTONOMOUS_LOOP_RISK,
            ],
        ),
        **kwargs,
    )


def build_provider_profile_validation_finding(
    finding_id: str,
    **kwargs: Any,
) -> ProviderProfileValidationFinding:
    return ProviderProfileValidationFinding(
        finding_id=finding_id,
        provider_profile_id=kwargs.pop("provider_profile_id", None),
        decision_kind=kwargs.pop("decision_kind", ProviderProfileValidationDecisionKind.ACCEPT_METADATA_ONLY),
        risk_kinds=kwargs.pop("risk_kinds", []),
        summary=kwargs.pop("summary", "Provider profile metadata accepted without invocation."),
        **kwargs,
    )


def validate_provider_profile_descriptor(
    descriptor: ProviderProfileDescriptor,
    policy: ProviderInvocationPolicy | None = None,
) -> ProviderProfileValidationFinding:
    if not isinstance(descriptor, ProviderProfileDescriptor):
        raise TypeError("descriptor must be ProviderProfileDescriptor")
    policy = policy or default_provider_invocation_policy()
    if not provider_invocation_policy_blocks_runtime_access(policy):
        return build_provider_profile_validation_finding(
            f"finding:{descriptor.provider_profile_id}:blocked_policy",
            provider_profile_id=descriptor.provider_profile_id,
            decision_kind=ProviderProfileValidationDecisionKind.BLOCK,
            risk_kinds=[ProviderProfileRiskKind.PROVIDER_INVOCATION_RISK],
            summary="Invocation policy attempted to permit runtime access.",
            blocked=True,
        )
    if not provider_profile_descriptor_is_not_invocation(descriptor):
        return build_provider_profile_validation_finding(
            f"finding:{descriptor.provider_profile_id}:blocked_descriptor",
            provider_profile_id=descriptor.provider_profile_id,
            decision_kind=ProviderProfileValidationDecisionKind.BLOCK,
            risk_kinds=[ProviderProfileRiskKind.PROVIDER_INVOCATION_RISK],
            summary="Descriptor attempted to permit provider invocation or external access.",
            blocked=True,
        )
    if ProviderProfileKind(descriptor.profile_kind) in {ProviderProfileKind.DISABLED_PROVIDER, ProviderProfileKind.UNKNOWN}:
        return build_provider_profile_validation_finding(
            f"finding:{descriptor.provider_profile_id}:disabled_or_unknown",
            provider_profile_id=descriptor.provider_profile_id,
            decision_kind=ProviderProfileValidationDecisionKind.DISABLE,
            risk_kinds=[ProviderProfileRiskKind.UNKNOWN],
            summary="Disabled or unknown provider profile is not accepted.",
            blocked=True,
        )
    if descriptor.future_gated:
        return build_provider_profile_validation_finding(
            f"finding:{descriptor.provider_profile_id}:future_gated",
            provider_profile_id=descriptor.provider_profile_id,
            decision_kind=ProviderProfileValidationDecisionKind.ACCEPT_FUTURE_GATE_METADATA,
            risk_kinds=[ProviderProfileRiskKind.PROVIDER_INVOCATION_RISK],
            summary="Future-gated provider metadata accepted as non-invocation ref only.",
            future_gated=True,
        )
    return build_provider_profile_validation_finding(
        f"finding:{descriptor.provider_profile_id}:metadata_only",
        provider_profile_id=descriptor.provider_profile_id,
        decision_kind=ProviderProfileValidationDecisionKind.ACCEPT_METADATA_ONLY,
        risk_kinds=[],
        summary="Mock/supplied provider profile metadata accepted without network, credential, or provider access.",
    )


def build_provider_profile_validation_report(
    validation_report_id: str = "provider_profile_validation_report:v0.34.1",
    **kwargs: Any,
) -> ProviderProfileValidationReport:
    findings = kwargs.pop("findings", [])
    return ProviderProfileValidationReport(
        validation_report_id=validation_report_id,
        version=kwargs.pop("version", V0341_VERSION),
        registry_id=kwargs.pop("registry_id", None),
        descriptor_ids_checked=kwargs.pop("descriptor_ids_checked", []),
        valid_metadata_profile_ids=kwargs.pop("valid_metadata_profile_ids", []),
        blocked_profile_ids=kwargs.pop("blocked_profile_ids", []),
        future_gated_profile_ids=kwargs.pop("future_gated_profile_ids", []),
        findings=findings,
        validation_passed=kwargs.pop("validation_passed", True),
        summary=kwargs.pop("summary", "Provider profile metadata validation report; no runtime certification."),
        **kwargs,
    )


def validate_provider_profile_registry(
    registry: ProviderProfileRegistry,
    policy: ProviderInvocationPolicy | None = None,
) -> ProviderProfileValidationReport:
    if not isinstance(registry, ProviderProfileRegistry):
        raise TypeError("registry must be ProviderProfileRegistry")
    policy = policy or default_provider_invocation_policy()
    findings = [validate_provider_profile_descriptor(descriptor, policy) for descriptor in registry.descriptors]
    blocked = [finding.provider_profile_id for finding in findings if finding.blocked and finding.provider_profile_id is not None]
    future_gated = [finding.provider_profile_id for finding in findings if finding.future_gated and finding.provider_profile_id is not None]
    valid = [finding.provider_profile_id for finding in findings if not finding.blocked and finding.provider_profile_id is not None]
    return build_provider_profile_validation_report(
        registry_id=registry.registry_id,
        descriptor_ids_checked=[descriptor.provider_profile_id for descriptor in registry.descriptors],
        valid_metadata_profile_ids=valid,
        blocked_profile_ids=blocked,
        future_gated_profile_ids=future_gated,
        findings=findings,
        validation_passed=not blocked,
        summary="Provider profile registry validation completed as metadata-only no-invocation report.",
    )


def build_provider_profile_resolution_input(
    resolution_input_id: str,
    **kwargs: Any,
) -> ProviderProfileResolutionInput:
    return ProviderProfileResolutionInput(
        resolution_input_id=resolution_input_id,
        source_version=kwargs.pop("source_version", V0341_VERSION),
        requested_profile_name=kwargs.pop("requested_profile_name", None),
        requested_profile_kind=kwargs.pop("requested_profile_kind", ProviderProfileKind.MOCK_PROVIDER),
        registry_id=kwargs.pop("registry_id", None),
        invocation_policy_id=kwargs.pop("invocation_policy_id", None),
        source_refs=kwargs.pop("source_refs", []),
        task_summary=kwargs.pop("task_summary", "Resolve provider profile metadata only."),
        **kwargs,
    )


def build_provider_profile_resolution_decision(
    resolution_decision_id: str,
    resolution_input_id: str,
    **kwargs: Any,
) -> ProviderProfileResolutionDecision:
    return ProviderProfileResolutionDecision(
        resolution_decision_id=resolution_decision_id,
        resolution_input_id=resolution_input_id,
        selected_provider_profile_id=kwargs.pop("selected_provider_profile_id", None),
        selected_profile_kind=kwargs.pop("selected_profile_kind", None),
        decision_kind=kwargs.pop("decision_kind", ProviderProfileValidationDecisionKind.ACCEPT_METADATA_ONLY),
        reason=kwargs.pop("reason", "Provider profile resolved as metadata only; invocation remains false."),
        **kwargs,
    )


def resolve_provider_profile_from_registry(
    input: ProviderProfileResolutionInput,
    registry: ProviderProfileRegistry,
    policy: ProviderInvocationPolicy,
) -> ProviderProfileResolutionDecision:
    if not isinstance(input, ProviderProfileResolutionInput):
        raise TypeError("input must be ProviderProfileResolutionInput")
    if not isinstance(registry, ProviderProfileRegistry):
        raise TypeError("registry must be ProviderProfileRegistry")
    if not isinstance(policy, ProviderInvocationPolicy):
        raise TypeError("policy must be ProviderInvocationPolicy")
    candidates = [
        descriptor
        for descriptor in registry.descriptors
        if (input.requested_profile_name is None or descriptor.profile_name == input.requested_profile_name)
        and ProviderProfileKind(descriptor.profile_kind) == ProviderProfileKind(input.requested_profile_kind)
    ]
    if not candidates:
        return build_provider_profile_resolution_decision(
            f"resolution_decision:{input.resolution_input_id}:not_found",
            input.resolution_input_id,
            decision_kind=ProviderProfileValidationDecisionKind.DENY,
            reason="Requested provider profile metadata was not found.",
            risk_kinds=[ProviderProfileRiskKind.UNKNOWN],
        )
    selected = candidates[0]
    finding = validate_provider_profile_descriptor(selected, policy)
    return build_provider_profile_resolution_decision(
        f"resolution_decision:{input.resolution_input_id}:{selected.provider_profile_id}",
        input.resolution_input_id,
        selected_provider_profile_id=selected.provider_profile_id,
        selected_profile_kind=selected.profile_kind,
        decision_kind=ProviderProfileValidationDecisionKind.FUTURE_GATE_REQUIRED if selected.future_gated else finding.decision_kind,
        reason="Provider profile resolved as future-gated metadata only." if selected.future_gated else "Provider profile resolved as non-network metadata only.",
        future_gated=selected.future_gated,
        risk_kinds=finding.risk_kinds,
    )


def build_provider_profile_resolution_report(
    report_id: str = "provider_profile_resolution_report:v0.34.1",
    **kwargs: Any,
) -> ProviderProfileResolutionReport:
    return ProviderProfileResolutionReport(
        report_id=report_id,
        version=kwargs.pop("version", V0341_VERSION),
        resolution_input_id=kwargs.pop("resolution_input_id", "provider_profile_resolution_input:v0.34.1"),
        resolution_decision_id=kwargs.pop("resolution_decision_id", None),
        selected_provider_profile_id=kwargs.pop("selected_provider_profile_id", None),
        status=kwargs.pop("status", ProviderProfileStatus.VALID_METADATA),
        readiness_level=kwargs.pop("readiness_level", ProviderProfileReadinessLevel.METADATA_VALIDATION_READY),
        summary=kwargs.pop("summary", "Provider profile resolution report; no invocation."),
        ready_for_v0342_model_request_envelope=kwargs.pop("ready_for_v0342_model_request_envelope", True),
        ready_for_v0343_model_response_envelope=kwargs.pop("ready_for_v0343_model_response_envelope", True),
        ready_for_v0344_existing_provider_boundary_adapter=kwargs.pop("ready_for_v0344_existing_provider_boundary_adapter", True),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", list(DEFAULT_PROVIDER_PROFILE_WITHDRAWAL_CONDITIONS)),
        **kwargs,
    )


def build_provider_profile_run_preview(
    run_preview_id: str = "provider_profile_run_preview:v0.34.1",
    **kwargs: Any,
) -> ProviderProfileRunPreview:
    return ProviderProfileRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_provider_profile_no_invocation_guarantee(
    guarantee_id: str = "provider_profile_no_invocation_guarantee:v0.34.1",
    **kwargs: Any,
) -> ProviderProfileNoInvocationGuarantee:
    return ProviderProfileNoInvocationGuarantee(guarantee_id=guarantee_id, version=kwargs.pop("version", V0341_VERSION), **kwargs)


def build_v0341_readiness_report(
    report_id: str = "v0341_readiness_report",
    **kwargs: Any,
) -> V0341ReadinessReport:
    return V0341ReadinessReport(
        report_id=report_id,
        version=kwargs.pop("version", V0341_VERSION),
        registry_id=kwargs.pop("registry_id", "provider_profile_registry:v0.34.1"),
        invocation_policy_id=kwargs.pop("invocation_policy_id", "provider_invocation_policy:v0.34.1"),
        validation_report_id=kwargs.pop("validation_report_id", "provider_profile_validation_report:v0.34.1"),
        resolution_report_id=kwargs.pop("resolution_report_id", "provider_profile_resolution_report:v0.34.1"),
        summary=kwargs.pop("summary", "v0.34.1 defines provider profile metadata and invocation policy only; no invocation readiness."),
        ready_for_v0342_model_request_envelope=kwargs.pop("ready_for_v0342_model_request_envelope", True),
        ready_for_v0343_model_response_envelope=kwargs.pop("ready_for_v0343_model_response_envelope", True),
        ready_for_v0344_existing_provider_boundary_adapter=kwargs.pop("ready_for_v0344_existing_provider_boundary_adapter", True),
        completed_items=kwargs.pop("completed_items", ["provider profile descriptors", "provider registry metadata", "credential policy", "network policy", "invocation policy", "validation and resolution reports"]),
        future_track_items=kwargs.pop("future_track_items", ["model request envelope", "model response envelope", "existing provider boundary adapter"]),
        **kwargs,
    )


def provider_profile_flags_preserve_invocation_false(flags: ProviderProfileFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_PROVIDER_PROFILE_FLAG_NAMES) and flags.production_certified is False


def provider_profile_descriptor_is_not_invocation(descriptor: ProviderProfileDescriptor) -> bool:
    return (
        descriptor.provider_runtime is False
        and descriptor.invocation_allowed is False
        and descriptor.provider_sdk_allowed is False
        and descriptor.network_allowed is False
        and descriptor.credential_access_allowed is False
        and descriptor.secret_read_allowed is False
    )


def provider_invocation_policy_blocks_runtime_access(policy: ProviderInvocationPolicy) -> bool:
    return (
        policy.invocation_permission is False
        and policy.allow_existing_boundary_invocation is False
        and policy.allow_local_provider_invocation is False
        and policy.allow_remote_provider_invocation is False
        and policy.allow_direct_provider_sdk is False
        and policy.allow_direct_network is False
        and policy.allow_credential_read is False
        and policy.allow_secret_read is False
        and policy.allow_tool_calls is False
        and policy.allow_recursive_calls is False
    )


def provider_profile_registry_is_not_runtime_registry(registry: ProviderProfileRegistry) -> bool:
    return (
        registry.provider_runtime is False
        and registry.ready_for_invocation is False
        and registry.ready_for_execution is False
        and provider_profile_flags_preserve_invocation_false(registry.flags)
        and all(provider_profile_descriptor_is_not_invocation(descriptor) for descriptor in registry.descriptors)
    )


def v0341_readiness_report_is_not_invocation_ready(report: V0341ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_PROVIDER_PROFILE_FLAG_NAMES) and report.invocation_readiness is False
