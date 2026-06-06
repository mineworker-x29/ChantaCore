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


V0340_VERSION = "v0.34.0"
V0340_RELEASE_NAME = "v0.34.0 Controlled Model Invocation Boundary Foundation"
V034_TRACK_NAME = "Controlled Model Invocation Boundary"

DEFAULT_V034_STAGES = [
    "boundary_foundation",
    "provider_profile_policy",
    "model_request_envelope",
    "model_response_envelope_sanitizer",
    "existing_provider_boundary_adapter",
    "model_output_action_quarantine",
    "agent_step_runner_model_integration",
    "model_invocation_ocel_trace_packet",
    "cli_model_backed_agent_step_surface",
    "consolidation",
]

DEFAULT_PROVIDER_PROHIBITED_RUNTIME_ACTIONS = [
    "controlled model invocation",
    "real model invocation",
    "model invocation",
    "provider invocation",
    "provider SDK invocation",
    "network access",
    "credential access",
    "secret read",
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

DEFAULT_WITHDRAWAL_CONDITIONS = [
    "Any real model/provider invocation path is introduced.",
    "Any provider SDK import or network adapter is introduced.",
    "Any credential loader, secret reader, or endpoint construction path is introduced.",
    "Any agent step/tool/shell/write/edit/patch execution path is introduced.",
    "Any unsafe readiness flag or production_certified becomes true.",
]

UNSAFE_MODEL_INVOCATION_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_controlled_model_invocation",
    "ready_for_real_model_invocation",
    "ready_for_model_invocation",
    "ready_for_provider_invocation",
    "ready_for_provider_sdk_invocation",
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

DEFAULT_PROHIBITED_SURFACES = [
    "provider_sdk_direct",
    "provider_network_endpoint",
    "credential_store",
    "api_key_value",
    "workspace_write",
    "code_edit",
    "patch_application",
    "shell_command",
    "external_harness",
    "reference_code",
    "persistent_trace",
    "ui_runtime",
]

DEFAULT_PROHIBITED_CAPABILITIES = [
    "call_existing_provider_boundary",
    "call_provider_sdk_direct",
    "access_provider_network",
    "read_credential",
    "read_secret",
    "autonomous_loop",
    "execute_agent_step",
    "execute_tool",
    "write_workspace",
    "edit_code",
    "apply_patch",
    "execute_shell",
    "execute_external_harness",
    "execute_reference_code",
]


class ControlledModelInvocationTrackKind(StrEnum):
    BOUNDARY_FOUNDATION = "boundary_foundation"
    PROVIDER_PROFILE_POLICY = "provider_profile_policy"
    MODEL_REQUEST_ENVELOPE = "model_request_envelope"
    MODEL_RESPONSE_ENVELOPE_SANITIZER = "model_response_envelope_sanitizer"
    EXISTING_PROVIDER_BOUNDARY_ADAPTER = "existing_provider_boundary_adapter"
    MODEL_OUTPUT_ACTION_QUARANTINE = "model_output_action_quarantine"
    AGENT_STEP_RUNNER_MODEL_INTEGRATION = "agent_step_runner_model_integration"
    MODEL_INVOCATION_OCEL_TRACE_PACKET = "model_invocation_ocel_trace_packet"
    CLI_MODEL_BACKED_AGENT_STEP_SURFACE = "cli_model_backed_agent_step_surface"
    CONSOLIDATION = "consolidation"
    UNKNOWN = "unknown"


class ControlledModelInvocationSurfaceKind(StrEnum):
    PROMPT_PAYLOAD = "prompt_payload"
    MODEL_REQUEST_ENVELOPE = "model_request_envelope"
    MODEL_RESPONSE_ENVELOPE = "model_response_envelope"
    PROVIDER_PROFILE = "provider_profile"
    EXISTING_CHAT_SERVICE_BOUNDARY = "existing_chat_service_boundary"
    EXISTING_PROVIDER_BOUNDARY = "existing_provider_boundary"
    PROVIDER_SDK_DIRECT = "provider_sdk_direct"
    PROVIDER_NETWORK_ENDPOINT = "provider_network_endpoint"
    CREDENTIAL_STORE = "credential_store"
    API_KEY_VALUE = "api_key_value"
    MODEL_OUTPUT_ACTION = "model_output_action"
    SAFE_TOOL_BRIDGE = "safe_tool_bridge"
    WORKSPACE_WRITE = "workspace_write"
    CODE_EDIT = "code_edit"
    PATCH_APPLICATION = "patch_application"
    SHELL_COMMAND = "shell_command"
    EXTERNAL_HARNESS = "external_harness"
    REFERENCE_CODE = "reference_code"
    PERSISTENT_TRACE = "persistent_trace"
    UI_RUNTIME = "ui_runtime"
    UNKNOWN = "unknown"


class ControlledModelInvocationCapabilityKind(StrEnum):
    DEFINE_BOUNDARY = "define_boundary"
    DESCRIBE_EXISTING_PROVIDER_BOUNDARY_REF = "describe_existing_provider_boundary_ref"
    DEFINE_PROVIDER_PROFILE_POLICY = "define_provider_profile_policy"
    DEFINE_REQUEST_ENVELOPE_POLICY = "define_request_envelope_policy"
    DEFINE_RESPONSE_ENVELOPE_POLICY = "define_response_envelope_policy"
    DEFINE_OUTPUT_QUARANTINE_POLICY = "define_output_quarantine_policy"
    DEFINE_MODEL_TRACE_POLICY = "define_model_trace_policy"
    ALLOW_DESIGN_STAGE_HANDOFF = "allow_design_stage_handoff"
    BLOCK_INVOCATION = "block_invocation"
    NO_OP = "no_op"
    CALL_EXISTING_PROVIDER_BOUNDARY = "call_existing_provider_boundary"
    CALL_PROVIDER_SDK_DIRECT = "call_provider_sdk_direct"
    ACCESS_PROVIDER_NETWORK = "access_provider_network"
    READ_CREDENTIAL = "read_credential"
    READ_SECRET = "read_secret"
    EXECUTE_AGENT_STEP = "execute_agent_step"
    EXECUTE_TOOL = "execute_tool"
    WRITE_WORKSPACE = "write_workspace"
    EDIT_CODE = "edit_code"
    APPLY_PATCH = "apply_patch"
    EXECUTE_SHELL = "execute_shell"
    EXECUTE_EXTERNAL_HARNESS = "execute_external_harness"
    EXECUTE_REFERENCE_CODE = "execute_reference_code"
    UNKNOWN = "unknown"


class ControlledModelInvocationRiskKind(StrEnum):
    PROVIDER_INVOCATION_RISK = "provider_invocation_risk"
    ARBITRARY_NETWORK_ACCESS_RISK = "arbitrary_network_access_risk"
    CREDENTIAL_EXPOSURE_RISK = "credential_exposure_risk"
    SECRET_READ_RISK = "secret_read_risk"
    PROVIDER_SDK_BYPASS_RISK = "provider_sdk_bypass_risk"
    ENDPOINT_CONSTRUCTION_RISK = "endpoint_construction_risk"
    PROMPT_LEAK_RISK = "prompt_leak_risk"
    RAW_MODEL_OUTPUT_PERSISTENCE_RISK = "raw_model_output_persistence_risk"
    MODEL_OUTPUT_ACTION_AUTHORITY_RISK = "model_output_action_authority_risk"
    RECURSIVE_MODEL_CALL_RISK = "recursive_model_call_risk"
    AUTONOMOUS_LOOP_RISK = "autonomous_loop_risk"
    GENERAL_TOOL_EXECUTION_RISK = "general_tool_execution_risk"
    WORKSPACE_WRITE_RISK = "workspace_write_risk"
    COMMAND_EXECUTION_RISK = "command_execution_risk"
    REFERENCE_EXECUTION_RISK = "reference_execution_risk"
    EXTERNAL_HARNESS_EXECUTION_RISK = "external_harness_execution_risk"
    PERSISTENT_TRACE_WRITE_RISK = "persistent_trace_write_risk"
    EXTERNAL_CONTROL_RISK = "external_control_risk"
    AUTHORITY_GRANT_RISK = "authority_grant_risk"
    UNKNOWN = "unknown"


class ControlledModelInvocationDecisionKind(StrEnum):
    ALLOW_DESIGN_STAGE_BOUNDARY_DEFINITION = "allow_design_stage_boundary_definition"
    ALLOW_DESIGN_STAGE_HANDOFF = "allow_design_stage_handoff"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    ASK_USER_REQUIRED = "ask_user_required"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class ControlledModelInvocationBoundaryStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    BOUNDARY_READY = "boundary_ready"
    BOUNDARY_READY_WITH_GAPS = "boundary_ready_with_gaps"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class ControlledModelInvocationReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    BOUNDARY_CONTRACT_READY = "boundary_contract_ready"
    DESIGN_HANDOFF_READY_FOR_V0341 = "design_handoff_ready_for_v0341"
    DESIGN_HANDOFF_READY_FOR_V0342 = "design_handoff_ready_for_v0342"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class ControlledProviderBoundaryPosture(StrEnum):
    NO_PROVIDER_BOUNDARY = "no_provider_boundary"
    EXISTING_BOUNDARY_REF_ONLY = "existing_boundary_ref_only"
    EXISTING_BOUNDARY_FUTURE_GATE = "existing_boundary_future_gate"
    DIRECT_PROVIDER_BLOCKED = "direct_provider_blocked"
    PROVIDER_SDK_BLOCKED = "provider_sdk_blocked"
    NETWORK_ENDPOINT_BLOCKED = "network_endpoint_blocked"
    UNKNOWN = "unknown"


class ControlledCredentialPosture(StrEnum):
    NO_CREDENTIAL_ACCESS = "no_credential_access"
    CREDENTIAL_REF_ONLY = "credential_ref_only"
    EXISTING_BOUNDARY_MANAGED_FUTURE_GATE = "existing_boundary_managed_future_gate"
    DIRECT_SECRET_READ_BLOCKED = "direct_secret_read_blocked"
    DIRECT_ENV_READ_BLOCKED = "direct_env_read_blocked"
    UNKNOWN = "unknown"


class ControlledNetworkPosture(StrEnum):
    NO_NETWORK_ACCESS = "no_network_access"
    EXISTING_BOUNDARY_MANAGED_FUTURE_GATE = "existing_boundary_managed_future_gate"
    ARBITRARY_NETWORK_BLOCKED = "arbitrary_network_blocked"
    PROVIDER_ENDPOINT_BLOCKED = "provider_endpoint_blocked"
    UNKNOWN = "unknown"


class ControlledModelInvocationSourceKind(StrEnum):
    V0339_HANDOFF_PACKET = "v0339_handoff_packet"
    V0338_CLI_SURFACE = "v0338_cli_surface"
    V0337_OCEL_TRACE_EMITTER = "v0337_ocel_trace_emitter"
    V0336_AGENT_STEP_RUNNER = "v0336_agent_step_runner"
    V0332_PROMPT_ASSEMBLY = "v0332_prompt_assembly"
    EXISTING_CHAT_SERVICE_BOUNDARY_REF = "existing_chat_service_boundary_ref"
    EXISTING_PROVIDER_BOUNDARY_REF = "existing_provider_boundary_ref"
    PROVIDER_BOUNDARY_DESIGN_NOTE = "provider_boundary_design_note"
    REFERENCE_CONTEXT_REF = "reference_context_ref"
    OPENCODE_REFERENCE_CONTEXT_REF = "opencode_reference_context_ref"
    HERMES_REFERENCE_CONTEXT_REF = "hermes_reference_context_ref"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


def _validate_version_includes_v0340(version: str) -> None:
    _require_non_blank("version", version)
    if V0340_VERSION not in version:
        raise ValueError("version must include v0.34.0")


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.34.0")


def _validate_true(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not True:
            raise ValueError(f"{name} must always be True in v0.34.0")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise TypeError(f"{name} must be dict[str, Any]")


def _validate_enum_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _validate_source_ref_list(values: list["ControlledModelInvocationSourceRef"]) -> None:
    _validate_object_list("source_refs", values, ControlledModelInvocationSourceRef)


def _validate_metadata_no_invocation(metadata: dict[str, Any]) -> None:
    _validate_dict("metadata", metadata)
    if _metadata_flag_true(
        metadata,
        {
            "provider_call",
            "provider_invocation",
            "provider_sdk_import",
            "network_call",
            "credential_access",
            "secret_read",
            "endpoint_construction",
            "execution",
            "workspace_write",
            "adapter_created",
            "credential_loader_created",
            "network_adapter_created",
        },
    ):
        raise ValueError("v0.34.0 metadata cannot imply invocation or external access")


def _validate_v034_stages(values: list[ControlledModelInvocationTrackKind | str]) -> None:
    if not isinstance(values, list):
        raise TypeError("stages must be list")
    normalized = [ControlledModelInvocationTrackKind(value).value for value in values]
    missing = set(DEFAULT_V034_STAGES) - set(normalized)
    if missing:
        raise ValueError(f"stages must include v0.34.0-v0.34.9: {sorted(missing)}")


def _validate_contains_terms(name: str, values: list[str], terms: list[str]) -> None:
    _validate_string_list(name, values)
    lowered = " | ".join(values).lower()
    missing = [term for term in terms if term.lower() not in lowered]
    if missing:
        raise ValueError(f"{name} missing required terms: {missing}")


@dataclass(frozen=True)
class ControlledModelInvocationFlagSet:
    flag_set_id: str
    version: str = V0340_VERSION
    controlled_model_invocation_boundary_constructed: bool = False
    provider_surface_policy_defined: bool = False
    model_invocation_risk_register_defined: bool = False
    ready_for_v0341_provider_profile_policy: bool = False
    ready_for_v0342_model_request_envelope: bool = False
    ready_for_execution: bool = False
    ready_for_controlled_model_invocation: bool = False
    ready_for_real_model_invocation: bool = False
    ready_for_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_provider_sdk_invocation: bool = False
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
        _validate_version_includes_v0340(self.version)
        _validate_false(self, UNSAFE_MODEL_INVOCATION_FLAG_NAMES)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False in v0.34.0")
        _validate_metadata_no_invocation(self.metadata)


@dataclass(frozen=True)
class ControlledModelInvocationSourceRef:
    source_ref_id: str
    source_kind: ControlledModelInvocationSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        ControlledModelInvocationSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_invocation(self.metadata)

    @property
    def provider_call(self) -> bool:
        return False

    @property
    def credential_access(self) -> bool:
        return False

    @property
    def file_read(self) -> bool:
        return False


@dataclass(frozen=True)
class ExistingProviderBoundaryRef:
    provider_boundary_ref_id: str
    boundary_name: str
    boundary_kind: str
    boundary_summary: str
    allowed_use_in_v0340: str
    source_refs: list[ControlledModelInvocationSourceRef] = field(default_factory=list)
    direct_invocation_allowed: bool = False
    provider_sdk_import_allowed: bool = False
    credential_read_allowed: bool = False
    network_call_allowed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("provider_boundary_ref_id", "boundary_name", "boundary_kind", "boundary_summary", "allowed_use_in_v0340"):
            _require_non_blank(name, getattr(self, name))
        _validate_source_ref_list(self.source_refs)
        _validate_false(
            self,
            (
                "direct_invocation_allowed",
                "provider_sdk_import_allowed",
                "credential_read_allowed",
                "network_call_allowed",
            ),
        )
        _validate_metadata_no_invocation(self.metadata)

    @property
    def invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class ControlledProviderSurfacePolicy:
    policy_id: str
    provider_boundary_posture: ControlledProviderBoundaryPosture | str = ControlledProviderBoundaryPosture.EXISTING_BOUNDARY_REF_ONLY
    credential_posture: ControlledCredentialPosture | str = ControlledCredentialPosture.NO_CREDENTIAL_ACCESS
    network_posture: ControlledNetworkPosture | str = ControlledNetworkPosture.NO_NETWORK_ACCESS
    allowed_surfaces: list[ControlledModelInvocationSurfaceKind | str] = field(default_factory=list)
    prohibited_surfaces: list[ControlledModelInvocationSurfaceKind | str] = field(default_factory=list)
    prohibited_capabilities: list[ControlledModelInvocationCapabilityKind | str] = field(default_factory=list)
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_PROVIDER_PROHIBITED_RUNTIME_ACTIONS))
    allow_existing_boundary_ref: bool = True
    allow_existing_boundary_invocation: bool = False
    allow_direct_provider_sdk: bool = False
    allow_direct_network: bool = False
    allow_credential_read: bool = False
    allow_secret_read: bool = False
    allow_endpoint_construction: bool = False
    allow_recursive_model_call: bool = False
    allow_autonomous_loop: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_id", self.policy_id)
        ControlledProviderBoundaryPosture(self.provider_boundary_posture)
        ControlledCredentialPosture(self.credential_posture)
        ControlledNetworkPosture(self.network_posture)
        _validate_enum_list("allowed_surfaces", self.allowed_surfaces, ControlledModelInvocationSurfaceKind)
        _validate_enum_list("prohibited_surfaces", self.prohibited_surfaces, ControlledModelInvocationSurfaceKind)
        if not isinstance(self.prohibited_capabilities, list):
            raise TypeError("prohibited_capabilities must be list")
        for capability in self.prohibited_capabilities:
            if str(capability) != "autonomous_loop":
                ControlledModelInvocationCapabilityKind(capability)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_contains_terms(
            "prohibited_runtime_actions",
            self.prohibited_runtime_actions,
            DEFAULT_PROVIDER_PROHIBITED_RUNTIME_ACTIONS,
        )
        _validate_false(
            self,
            (
                "allow_existing_boundary_invocation",
                "allow_direct_provider_sdk",
                "allow_direct_network",
                "allow_credential_read",
                "allow_secret_read",
                "allow_endpoint_construction",
                "allow_recursive_model_call",
                "allow_autonomous_loop",
            ),
        )
        _validate_metadata_no_invocation(self.metadata)

    @property
    def invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class ControlledModelInvocationAllowedSurface:
    allowed_surface_id: str
    surface_kind: ControlledModelInvocationSurfaceKind | str
    capability_kind: ControlledModelInvocationCapabilityKind | str
    description: str
    allowed_only_for_design_stage: bool = True
    allowed_only_as_ref: bool = True
    executable_in_v0340: bool = False
    source_refs: list[ControlledModelInvocationSourceRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("allowed_surface_id", self.allowed_surface_id)
        ControlledModelInvocationSurfaceKind(self.surface_kind)
        ControlledModelInvocationCapabilityKind(self.capability_kind)
        _require_non_blank("description", self.description)
        if self.allowed_only_for_design_stage is not True:
            raise ValueError("allowed_only_for_design_stage must be True in v0.34.0")
        if self.executable_in_v0340 is not False:
            raise ValueError("executable_in_v0340 must always be False")
        _validate_source_ref_list(self.source_refs)
        _validate_metadata_no_invocation(self.metadata)

    @property
    def invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class ControlledModelInvocationProhibitedSurface:
    prohibited_surface_id: str
    surface_kind: ControlledModelInvocationSurfaceKind | str
    risk_kind: ControlledModelInvocationRiskKind | str
    capability_kind: ControlledModelInvocationCapabilityKind | str
    reason: str
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_PROVIDER_PROHIBITED_RUNTIME_ACTIONS))
    blocks_invocation: bool = True
    blocks_runtime_readiness: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("prohibited_surface_id", self.prohibited_surface_id)
        ControlledModelInvocationSurfaceKind(self.surface_kind)
        ControlledModelInvocationRiskKind(self.risk_kind)
        ControlledModelInvocationCapabilityKind(self.capability_kind)
        _require_non_blank("reason", self.reason)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        if self.blocks_invocation is not True:
            raise ValueError("blocks_invocation must be True in v0.34.0")
        if self.blocks_runtime_readiness is not True:
            raise ValueError("blocks_runtime_readiness must be True in v0.34.0")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_invocation(self.metadata)

    @property
    def boundary_metadata(self) -> bool:
        return True


@dataclass(frozen=True)
class ControlledModelInvocationBoundary:
    boundary_id: str
    version: str
    release_name: str
    provider_surface_policy: ControlledProviderSurfacePolicy
    existing_provider_boundary_refs: list[ExistingProviderBoundaryRef]
    allowed_surfaces: list[ControlledModelInvocationAllowedSurface]
    prohibited_surfaces: list[ControlledModelInvocationProhibitedSurface]
    flags: ControlledModelInvocationFlagSet
    status: ControlledModelInvocationBoundaryStatus | str
    readiness_level: ControlledModelInvocationReadinessLevel | str
    summary: str
    gaps: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    ready_for_v0341_provider_profile_policy: bool = False
    ready_for_v0342_model_request_envelope: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_id", self.boundary_id)
        _validate_version_includes_v0340(self.version)
        _require_non_blank("release_name", self.release_name)
        if not isinstance(self.provider_surface_policy, ControlledProviderSurfacePolicy):
            raise TypeError("provider_surface_policy must be ControlledProviderSurfacePolicy")
        _validate_object_list("existing_provider_boundary_refs", self.existing_provider_boundary_refs, ExistingProviderBoundaryRef)
        _validate_object_list("allowed_surfaces", self.allowed_surfaces, ControlledModelInvocationAllowedSurface)
        _validate_object_list("prohibited_surfaces", self.prohibited_surfaces, ControlledModelInvocationProhibitedSurface)
        if not isinstance(self.flags, ControlledModelInvocationFlagSet):
            raise TypeError("flags must be ControlledModelInvocationFlagSet")
        if not controlled_model_invocation_flags_preserve_invocation_false(self.flags):
            raise ValueError("flags must preserve invocation/runtime false")
        ControlledModelInvocationBoundaryStatus(self.status)
        ControlledModelInvocationReadinessLevel(self.readiness_level)
        _require_non_blank("summary", self.summary)
        for name in ("gaps", "blocked_reasons", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        if (self.ready_for_v0341_provider_profile_policy or self.ready_for_v0342_model_request_envelope) and self.blocked_reasons:
            raise ValueError("design-stage handoff readiness is not allowed with blocking reasons")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        _validate_metadata_no_invocation(self.metadata)

    @property
    def provider_invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class ControlledModelInvocationPermissionRequest:
    request_id: str
    requested_surface: ControlledModelInvocationSurfaceKind | str
    requested_capability: ControlledModelInvocationCapabilityKind | str
    request_summary: str
    source_refs: list[ControlledModelInvocationSourceRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("request_id", self.request_id)
        ControlledModelInvocationSurfaceKind(self.requested_surface)
        ControlledModelInvocationCapabilityKind(self.requested_capability)
        _require_non_blank("request_summary", self.request_summary)
        _validate_source_ref_list(self.source_refs)
        _validate_metadata_no_invocation(self.metadata)

    @property
    def invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class ControlledModelInvocationPermissionDecision:
    decision_id: str
    request_id: str
    decision_kind: ControlledModelInvocationDecisionKind | str
    reason: str
    allowed_only_for_design_stage: bool = True
    allowed_only_as_ref: bool = True
    invocation_allowed: bool = False
    provider_invocation_allowed: bool = False
    provider_sdk_allowed: bool = False
    network_allowed: bool = False
    credential_access_allowed: bool = False
    secret_read_allowed: bool = False
    agent_step_execution_allowed: bool = False
    required_reviews: list[str] = field(default_factory=list)
    denied_risk_kinds: list[ControlledModelInvocationRiskKind | str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("decision_id", self.decision_id)
        _require_non_blank("request_id", self.request_id)
        ControlledModelInvocationDecisionKind(self.decision_kind)
        _require_non_blank("reason", self.reason)
        _validate_false(
            self,
            (
                "invocation_allowed",
                "provider_invocation_allowed",
                "provider_sdk_allowed",
                "network_allowed",
                "credential_access_allowed",
                "secret_read_allowed",
                "agent_step_execution_allowed",
            ),
        )
        _validate_string_list("required_reviews", self.required_reviews)
        _validate_enum_list("denied_risk_kinds", self.denied_risk_kinds, ControlledModelInvocationRiskKind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_invocation(self.metadata)

    @property
    def invocation_permission(self) -> bool:
        return False


@dataclass(frozen=True)
class ControlledModelInvocationDeniedAction:
    denied_action_id: str
    request_id: str | None
    decision_id: str | None
    denied_surface: ControlledModelInvocationSurfaceKind | str
    denied_capability: ControlledModelInvocationCapabilityKind | str
    risk_kinds: list[ControlledModelInvocationRiskKind | str]
    reason: str
    safe_alternatives: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("denied_action_id", self.denied_action_id)
        ControlledModelInvocationSurfaceKind(self.denied_surface)
        ControlledModelInvocationCapabilityKind(self.denied_capability)
        _validate_enum_list("risk_kinds", self.risk_kinds, ControlledModelInvocationRiskKind)
        _require_non_blank("reason", self.reason)
        _validate_string_list("safe_alternatives", self.safe_alternatives)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_invocation(self.metadata)

    @property
    def safe_outcome(self) -> bool:
        return True


@dataclass(frozen=True)
class ControlledModelInvocationGateEvaluation:
    evaluation_id: str
    boundary_id: str
    request_id: str
    decision: ControlledModelInvocationPermissionDecision
    denied_actions: list[ControlledModelInvocationDeniedAction]
    allowed_design_stage_only: bool
    invocation_allowed: bool
    provider_invocation_allowed: bool
    network_allowed: bool
    credential_access_allowed: bool
    summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("evaluation_id", self.evaluation_id)
        _require_non_blank("boundary_id", self.boundary_id)
        _require_non_blank("request_id", self.request_id)
        if not isinstance(self.decision, ControlledModelInvocationPermissionDecision):
            raise TypeError("decision must be ControlledModelInvocationPermissionDecision")
        _validate_object_list("denied_actions", self.denied_actions, ControlledModelInvocationDeniedAction)
        _validate_false(self, ("invocation_allowed", "provider_invocation_allowed", "network_allowed", "credential_access_allowed"))
        _require_non_blank("summary", self.summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_invocation(self.metadata)

    @property
    def invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class ControlledModelInvocationRiskRegister:
    risk_register_id: str
    version: str
    known_risks: list[ControlledModelInvocationRiskKind | str] = field(default_factory=list)
    high_risk_surfaces: list[ControlledModelInvocationSurfaceKind | str] = field(default_factory=list)
    prohibited_capabilities: list[ControlledModelInvocationCapabilityKind | str] = field(default_factory=list)
    mitigations: list[str] = field(default_factory=list)
    unresolved_risks: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_register_id", self.risk_register_id)
        _validate_version_includes_v0340(self.version)
        _validate_enum_list("known_risks", self.known_risks, ControlledModelInvocationRiskKind)
        _validate_enum_list("high_risk_surfaces", self.high_risk_surfaces, ControlledModelInvocationSurfaceKind)
        if not isinstance(self.prohibited_capabilities, list):
            raise TypeError("prohibited_capabilities must be list")
        for capability in self.prohibited_capabilities:
            if str(capability) != "autonomous_loop":
                ControlledModelInvocationCapabilityKind(capability)
        _validate_contains_terms(
            "prohibited_capabilities",
            [str(value) for value in self.prohibited_capabilities],
            ["provider_sdk", "network", "credential", "secret", "autonomous", "shell", "write", "edit", "patch", "reference"],
        )
        _validate_string_list("mitigations", self.mitigations)
        _validate_string_list("unresolved_risks", self.unresolved_risks)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_invocation(self.metadata)

    @property
    def permission(self) -> bool:
        return False


@dataclass(frozen=True)
class ControlledModelInvocationNoExternalSideEffectGuarantee:
    guarantee_id: str
    version: str = V0340_VERSION
    no_real_model_invocation: bool = True
    no_model_invocation: bool = True
    no_provider_invocation: bool = True
    no_provider_sdk_invocation: bool = True
    no_network_access: bool = True
    no_credential_access: bool = True
    no_secret_read: bool = True
    no_endpoint_construction: bool = True
    no_agent_step_execution: bool = True
    no_general_agent_execution: bool = True
    no_autonomous_agent_runtime: bool = True
    no_general_tool_execution: bool = True
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
        _validate_version_includes_v0340(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.34.0")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_invocation(self.metadata)


@dataclass(frozen=True)
class V034RoadmapOverview:
    roadmap_id: str
    version: str
    release_name: str
    stages: list[ControlledModelInvocationTrackKind | str]
    stage_summaries: dict[str, str]
    boundary_summary: str
    existing_provider_boundary_role: str
    credential_policy_summary: str
    network_policy_summary: str
    response_quarantine_summary: str
    v035_handoff_preview: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("roadmap_id", self.roadmap_id)
        _validate_version_includes_v0340(self.version)
        _require_non_blank("release_name", self.release_name)
        _validate_v034_stages(self.stages)
        if not isinstance(self.stage_summaries, dict) or not all(isinstance(key, str) and isinstance(value, str) for key, value in self.stage_summaries.items()):
            raise TypeError("stage_summaries must be dict[str, str]")
        for name in (
            "boundary_summary",
            "existing_provider_boundary_role",
            "credential_policy_summary",
            "network_policy_summary",
            "response_quarantine_summary",
            "v035_handoff_preview",
        ):
            _require_non_blank(name, getattr(self, name))
        if "future-gated existing boundary ref only" not in self.existing_provider_boundary_role.lower():
            raise ValueError("existing_provider_boundary_role must say future-gated existing boundary ref only")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_invocation(self.metadata)

    @property
    def implementation(self) -> bool:
        return False


@dataclass(frozen=True)
class V0340ReadinessReport:
    report_id: str
    version: str = V0340_VERSION
    boundary_id: str | None = None
    roadmap_id: str | None = None
    risk_register_id: str | None = None
    summary: str = "v0.34.0 defines controlled model invocation boundary contracts only."
    ready_for_v0341_provider_profile_policy: bool = False
    ready_for_v0342_model_request_envelope: bool = False
    ready_for_execution: bool = False
    ready_for_controlled_model_invocation: bool = False
    ready_for_real_model_invocation: bool = False
    ready_for_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_provider_sdk_invocation: bool = False
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
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_PROVIDER_PROHIBITED_RUNTIME_ACTIONS))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0340(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(self, UNSAFE_MODEL_INVOCATION_FLAG_NAMES)
        for name in ("completed_items", "blocked_items", "future_track_items", "prohibited_until_later_gate", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_contains_terms("prohibited_until_later_gate", self.prohibited_until_later_gate, DEFAULT_PROVIDER_PROHIBITED_RUNTIME_ACTIONS)
        if (self.ready_for_v0341_provider_profile_policy or self.ready_for_v0342_model_request_envelope) and self.blocked_items:
            raise ValueError("design-stage handoff readiness is not allowed with blocked_items")
        _validate_metadata_no_invocation(self.metadata)

    @property
    def invocation_readiness(self) -> bool:
        return False


def build_controlled_model_invocation_flags(
    flag_set_id: str = "controlled_model_invocation_flags:v0.34.0",
    **kwargs: Any,
) -> ControlledModelInvocationFlagSet:
    return ControlledModelInvocationFlagSet(
        flag_set_id=flag_set_id,
        version=kwargs.pop("version", V0340_VERSION),
        controlled_model_invocation_boundary_constructed=kwargs.pop("controlled_model_invocation_boundary_constructed", True),
        provider_surface_policy_defined=kwargs.pop("provider_surface_policy_defined", True),
        model_invocation_risk_register_defined=kwargs.pop("model_invocation_risk_register_defined", True),
        ready_for_v0341_provider_profile_policy=kwargs.pop("ready_for_v0341_provider_profile_policy", True),
        ready_for_v0342_model_request_envelope=kwargs.pop("ready_for_v0342_model_request_envelope", True),
        **kwargs,
    )


def build_controlled_model_invocation_source_ref(
    source_ref_id: str,
    source_kind: ControlledModelInvocationSourceKind | str = ControlledModelInvocationSourceKind.PROVIDER_BOUNDARY_DESIGN_NOTE,
    source_id: str = "controlled_model_invocation_boundary_source",
    source_summary: str = "Design-stage source ref only; no fetch/read/execute.",
    **kwargs: Any,
) -> ControlledModelInvocationSourceRef:
    return ControlledModelInvocationSourceRef(
        source_ref_id=source_ref_id,
        source_kind=source_kind,
        source_id=source_id,
        source_summary=source_summary,
        **kwargs,
    )


def build_existing_provider_boundary_ref(
    provider_boundary_ref_id: str = "existing_provider_boundary_ref:v0.34.0",
    **kwargs: Any,
) -> ExistingProviderBoundaryRef:
    source_ref = build_controlled_model_invocation_source_ref(
        "source:existing_provider_boundary_ref:v0.34.0",
        ControlledModelInvocationSourceKind.EXISTING_PROVIDER_BOUNDARY_REF,
        "existing_provider_boundary",
        "Existing provider/chat_service boundary name ref only.",
    )
    return ExistingProviderBoundaryRef(
        provider_boundary_ref_id=provider_boundary_ref_id,
        boundary_name=kwargs.pop("boundary_name", "existing_provider_or_chat_service_boundary"),
        boundary_kind=kwargs.pop("boundary_kind", "future_gated_existing_boundary_ref"),
        boundary_summary=kwargs.pop("boundary_summary", "Existing provider/chat_service boundary is referenced only for future controlled integration."),
        allowed_use_in_v0340=kwargs.pop("allowed_use_in_v0340", "future-gated ref only; no invocation, SDK import, credential read, or network call."),
        source_refs=kwargs.pop("source_refs", [source_ref]),
        **kwargs,
    )


def build_controlled_provider_surface_policy(
    policy_id: str = "controlled_provider_surface_policy:v0.34.0",
    **kwargs: Any,
) -> ControlledProviderSurfacePolicy:
    return ControlledProviderSurfacePolicy(
        policy_id=policy_id,
        allowed_surfaces=kwargs.pop(
            "allowed_surfaces",
            [
                ControlledModelInvocationSurfaceKind.PROMPT_PAYLOAD,
                ControlledModelInvocationSurfaceKind.EXISTING_CHAT_SERVICE_BOUNDARY,
                ControlledModelInvocationSurfaceKind.EXISTING_PROVIDER_BOUNDARY,
            ],
        ),
        prohibited_surfaces=kwargs.pop(
            "prohibited_surfaces",
            [ControlledModelInvocationSurfaceKind(value) for value in DEFAULT_PROHIBITED_SURFACES],
        ),
        prohibited_capabilities=kwargs.pop("prohibited_capabilities", list(DEFAULT_PROHIBITED_CAPABILITIES)),
        **kwargs,
    )


def build_controlled_model_invocation_allowed_surface(
    allowed_surface_id: str,
    surface_kind: ControlledModelInvocationSurfaceKind | str = ControlledModelInvocationSurfaceKind.EXISTING_PROVIDER_BOUNDARY,
    capability_kind: ControlledModelInvocationCapabilityKind | str = ControlledModelInvocationCapabilityKind.DESCRIBE_EXISTING_PROVIDER_BOUNDARY_REF,
    description: str = "Allowed only as design-stage ref in v0.34.0.",
    **kwargs: Any,
) -> ControlledModelInvocationAllowedSurface:
    return ControlledModelInvocationAllowedSurface(
        allowed_surface_id=allowed_surface_id,
        surface_kind=surface_kind,
        capability_kind=capability_kind,
        description=description,
        **kwargs,
    )


def build_controlled_model_invocation_prohibited_surface(
    prohibited_surface_id: str,
    surface_kind: ControlledModelInvocationSurfaceKind | str = ControlledModelInvocationSurfaceKind.PROVIDER_SDK_DIRECT,
    risk_kind: ControlledModelInvocationRiskKind | str = ControlledModelInvocationRiskKind.PROVIDER_SDK_BYPASS_RISK,
    capability_kind: ControlledModelInvocationCapabilityKind | str = ControlledModelInvocationCapabilityKind.CALL_PROVIDER_SDK_DIRECT,
    reason: str = "Direct provider access is prohibited in v0.34.0.",
    **kwargs: Any,
) -> ControlledModelInvocationProhibitedSurface:
    return ControlledModelInvocationProhibitedSurface(
        prohibited_surface_id=prohibited_surface_id,
        surface_kind=surface_kind,
        risk_kind=risk_kind,
        capability_kind=capability_kind,
        reason=reason,
        **kwargs,
    )


def _default_prohibited_surfaces() -> list[ControlledModelInvocationProhibitedSurface]:
    return [
        build_controlled_model_invocation_prohibited_surface(
            f"prohibited:{surface.value}",
            surface,
            risk,
            capability,
        )
        for surface, risk, capability in [
            (ControlledModelInvocationSurfaceKind.PROVIDER_SDK_DIRECT, ControlledModelInvocationRiskKind.PROVIDER_SDK_BYPASS_RISK, ControlledModelInvocationCapabilityKind.CALL_PROVIDER_SDK_DIRECT),
            (ControlledModelInvocationSurfaceKind.PROVIDER_NETWORK_ENDPOINT, ControlledModelInvocationRiskKind.ARBITRARY_NETWORK_ACCESS_RISK, ControlledModelInvocationCapabilityKind.ACCESS_PROVIDER_NETWORK),
            (ControlledModelInvocationSurfaceKind.CREDENTIAL_STORE, ControlledModelInvocationRiskKind.CREDENTIAL_EXPOSURE_RISK, ControlledModelInvocationCapabilityKind.READ_CREDENTIAL),
            (ControlledModelInvocationSurfaceKind.API_KEY_VALUE, ControlledModelInvocationRiskKind.SECRET_READ_RISK, ControlledModelInvocationCapabilityKind.READ_SECRET),
            (ControlledModelInvocationSurfaceKind.SHELL_COMMAND, ControlledModelInvocationRiskKind.COMMAND_EXECUTION_RISK, ControlledModelInvocationCapabilityKind.EXECUTE_SHELL),
            (ControlledModelInvocationSurfaceKind.WORKSPACE_WRITE, ControlledModelInvocationRiskKind.WORKSPACE_WRITE_RISK, ControlledModelInvocationCapabilityKind.WRITE_WORKSPACE),
            (ControlledModelInvocationSurfaceKind.CODE_EDIT, ControlledModelInvocationRiskKind.WORKSPACE_WRITE_RISK, ControlledModelInvocationCapabilityKind.EDIT_CODE),
            (ControlledModelInvocationSurfaceKind.PATCH_APPLICATION, ControlledModelInvocationRiskKind.WORKSPACE_WRITE_RISK, ControlledModelInvocationCapabilityKind.APPLY_PATCH),
            (ControlledModelInvocationSurfaceKind.REFERENCE_CODE, ControlledModelInvocationRiskKind.REFERENCE_EXECUTION_RISK, ControlledModelInvocationCapabilityKind.EXECUTE_REFERENCE_CODE),
        ]
    ]


def build_controlled_model_invocation_boundary(
    boundary_id: str = "controlled_model_invocation_boundary:v0.34.0",
    **kwargs: Any,
) -> ControlledModelInvocationBoundary:
    return ControlledModelInvocationBoundary(
        boundary_id=boundary_id,
        version=kwargs.pop("version", V0340_VERSION),
        release_name=kwargs.pop("release_name", V0340_RELEASE_NAME),
        provider_surface_policy=kwargs.pop("provider_surface_policy", build_controlled_provider_surface_policy()),
        existing_provider_boundary_refs=kwargs.pop("existing_provider_boundary_refs", [build_existing_provider_boundary_ref()]),
        allowed_surfaces=kwargs.pop(
            "allowed_surfaces",
            [
                build_controlled_model_invocation_allowed_surface(
                    "allowed:existing_provider_boundary_ref",
                    ControlledModelInvocationSurfaceKind.EXISTING_PROVIDER_BOUNDARY,
                    ControlledModelInvocationCapabilityKind.DESCRIBE_EXISTING_PROVIDER_BOUNDARY_REF,
                )
            ],
        ),
        prohibited_surfaces=kwargs.pop("prohibited_surfaces", _default_prohibited_surfaces()),
        flags=kwargs.pop("flags", build_controlled_model_invocation_flags()),
        status=kwargs.pop("status", ControlledModelInvocationBoundaryStatus.BOUNDARY_READY_WITH_GAPS),
        readiness_level=kwargs.pop("readiness_level", ControlledModelInvocationReadinessLevel.BOUNDARY_CONTRACT_READY),
        summary=kwargs.pop("summary", "Controlled model invocation boundary foundation only; no provider call is allowed."),
        gaps=kwargs.pop("gaps", ["Actual provider policy, envelopes, adapter, sanitizer, quarantine, and integration remain future-stage."]),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", list(DEFAULT_WITHDRAWAL_CONDITIONS)),
        ready_for_v0341_provider_profile_policy=kwargs.pop("ready_for_v0341_provider_profile_policy", True),
        ready_for_v0342_model_request_envelope=kwargs.pop("ready_for_v0342_model_request_envelope", True),
        **kwargs,
    )


def build_controlled_model_invocation_permission_request(
    request_id: str,
    **kwargs: Any,
) -> ControlledModelInvocationPermissionRequest:
    return ControlledModelInvocationPermissionRequest(
        request_id=request_id,
        requested_surface=kwargs.pop("requested_surface", ControlledModelInvocationSurfaceKind.EXISTING_PROVIDER_BOUNDARY),
        requested_capability=kwargs.pop("requested_capability", ControlledModelInvocationCapabilityKind.DESCRIBE_EXISTING_PROVIDER_BOUNDARY_REF),
        request_summary=kwargs.pop("request_summary", "Design-stage boundary request only."),
        **kwargs,
    )


def build_controlled_model_invocation_permission_decision(
    decision_id: str,
    request_id: str,
    **kwargs: Any,
) -> ControlledModelInvocationPermissionDecision:
    return ControlledModelInvocationPermissionDecision(
        decision_id=decision_id,
        request_id=request_id,
        decision_kind=kwargs.pop("decision_kind", ControlledModelInvocationDecisionKind.ALLOW_DESIGN_STAGE_BOUNDARY_DEFINITION),
        reason=kwargs.pop("reason", "Allowed for boundary definition only; invocation remains prohibited."),
        **kwargs,
    )


def build_controlled_model_invocation_denied_action(
    denied_action_id: str,
    **kwargs: Any,
) -> ControlledModelInvocationDeniedAction:
    return ControlledModelInvocationDeniedAction(
        denied_action_id=denied_action_id,
        request_id=kwargs.pop("request_id", None),
        decision_id=kwargs.pop("decision_id", None),
        denied_surface=kwargs.pop("denied_surface", ControlledModelInvocationSurfaceKind.PROVIDER_SDK_DIRECT),
        denied_capability=kwargs.pop("denied_capability", ControlledModelInvocationCapabilityKind.CALL_PROVIDER_SDK_DIRECT),
        risk_kinds=kwargs.pop("risk_kinds", [ControlledModelInvocationRiskKind.PROVIDER_SDK_BYPASS_RISK]),
        reason=kwargs.pop("reason", "Provider invocation is denied in v0.34.0."),
        safe_alternatives=kwargs.pop("safe_alternatives", ["Use design-stage ExistingProviderBoundaryRef only."]),
        **kwargs,
    )


def build_controlled_model_invocation_gate_evaluation(
    evaluation_id: str,
    boundary_id: str,
    request_id: str,
    decision: ControlledModelInvocationPermissionDecision,
    **kwargs: Any,
) -> ControlledModelInvocationGateEvaluation:
    return ControlledModelInvocationGateEvaluation(
        evaluation_id=evaluation_id,
        boundary_id=boundary_id,
        request_id=request_id,
        decision=decision,
        denied_actions=kwargs.pop("denied_actions", []),
        allowed_design_stage_only=kwargs.pop("allowed_design_stage_only", True),
        invocation_allowed=kwargs.pop("invocation_allowed", False),
        provider_invocation_allowed=kwargs.pop("provider_invocation_allowed", False),
        network_allowed=kwargs.pop("network_allowed", False),
        credential_access_allowed=kwargs.pop("credential_access_allowed", False),
        summary=kwargs.pop("summary", "Gate evaluation preserves no model/provider invocation."),
        **kwargs,
    )


def build_controlled_model_invocation_risk_register(
    risk_register_id: str = "controlled_model_invocation_risk_register:v0.34.0",
    **kwargs: Any,
) -> ControlledModelInvocationRiskRegister:
    return ControlledModelInvocationRiskRegister(
        risk_register_id=risk_register_id,
        version=kwargs.pop("version", V0340_VERSION),
        known_risks=kwargs.pop(
            "known_risks",
            [
                ControlledModelInvocationRiskKind.PROVIDER_INVOCATION_RISK,
                ControlledModelInvocationRiskKind.ARBITRARY_NETWORK_ACCESS_RISK,
                ControlledModelInvocationRiskKind.CREDENTIAL_EXPOSURE_RISK,
                ControlledModelInvocationRiskKind.AUTONOMOUS_LOOP_RISK,
            ],
        ),
        high_risk_surfaces=kwargs.pop(
            "high_risk_surfaces",
            [
                ControlledModelInvocationSurfaceKind.PROVIDER_SDK_DIRECT,
                ControlledModelInvocationSurfaceKind.PROVIDER_NETWORK_ENDPOINT,
                ControlledModelInvocationSurfaceKind.CREDENTIAL_STORE,
                ControlledModelInvocationSurfaceKind.API_KEY_VALUE,
                ControlledModelInvocationSurfaceKind.SHELL_COMMAND,
                ControlledModelInvocationSurfaceKind.WORKSPACE_WRITE,
                ControlledModelInvocationSurfaceKind.REFERENCE_CODE,
            ],
        ),
        prohibited_capabilities=kwargs.pop("prohibited_capabilities", list(DEFAULT_PROHIBITED_CAPABILITIES)),
        mitigations=kwargs.pop(
            "mitigations",
            ["future-gated existing boundary refs", "no direct provider/network/credential access", "all invocation readiness flags false"],
        ),
        **kwargs,
    )


def build_controlled_model_invocation_no_external_side_effect_guarantee(
    guarantee_id: str = "controlled_model_invocation_no_external_side_effect:v0.34.0",
    **kwargs: Any,
) -> ControlledModelInvocationNoExternalSideEffectGuarantee:
    return ControlledModelInvocationNoExternalSideEffectGuarantee(guarantee_id=guarantee_id, version=kwargs.pop("version", V0340_VERSION), **kwargs)


def build_v034_roadmap_overview(
    roadmap_id: str = "v034_roadmap_overview:v0.34.0",
    **kwargs: Any,
) -> V034RoadmapOverview:
    return V034RoadmapOverview(
        roadmap_id=roadmap_id,
        version=kwargs.pop("version", V0340_VERSION),
        release_name=kwargs.pop("release_name", V0340_RELEASE_NAME),
        stages=kwargs.pop("stages", list(DEFAULT_V034_STAGES)),
        stage_summaries=kwargs.pop("stage_summaries", {stage: f"{stage} controlled model invocation track stage." for stage in DEFAULT_V034_STAGES}),
        boundary_summary=kwargs.pop("boundary_summary", "v0.34.0 defines the boundary foundation only; no invocation is opened."),
        existing_provider_boundary_role=kwargs.pop("existing_provider_boundary_role", "Existing provider/chat_service boundary is future-gated existing boundary ref only in v0.34.0."),
        credential_policy_summary=kwargs.pop("credential_policy_summary", "Credential posture records no credential access and no secret read."),
        network_policy_summary=kwargs.pop("network_policy_summary", "Network posture records no network access and provider endpoint blocked."),
        response_quarantine_summary=kwargs.pop("response_quarantine_summary", "Response quarantine is future-stage; v0.34.0 defines only its boundary slot."),
        v035_handoff_preview=kwargs.pop("v035_handoff_preview", "v0.35 remains outside this foundation and receives no invocation authority."),
        **kwargs,
    )


def build_v0340_readiness_report(
    report_id: str = "v0340_readiness_report",
    **kwargs: Any,
) -> V0340ReadinessReport:
    return V0340ReadinessReport(
        report_id=report_id,
        version=kwargs.pop("version", V0340_VERSION),
        boundary_id=kwargs.pop("boundary_id", "controlled_model_invocation_boundary:v0.34.0"),
        roadmap_id=kwargs.pop("roadmap_id", "v034_roadmap_overview:v0.34.0"),
        risk_register_id=kwargs.pop("risk_register_id", "controlled_model_invocation_risk_register:v0.34.0"),
        ready_for_v0341_provider_profile_policy=kwargs.pop("ready_for_v0341_provider_profile_policy", True),
        ready_for_v0342_model_request_envelope=kwargs.pop("ready_for_v0342_model_request_envelope", True),
        completed_items=kwargs.pop(
            "completed_items",
            ["boundary contract", "provider surface policy", "existing provider boundary ref", "risk register", "no external side effect guarantee", "roadmap overview"],
        ),
        future_track_items=kwargs.pop("future_track_items", list(DEFAULT_V034_STAGES[1:])),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", list(DEFAULT_WITHDRAWAL_CONDITIONS)),
        **kwargs,
    )


def controlled_model_invocation_flags_preserve_invocation_false(flags: ControlledModelInvocationFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_MODEL_INVOCATION_FLAG_NAMES) and flags.production_certified is False


def existing_provider_boundary_ref_is_not_invocation(ref: ExistingProviderBoundaryRef) -> bool:
    return (
        ref.invocation is False
        and ref.direct_invocation_allowed is False
        and ref.provider_sdk_import_allowed is False
        and ref.credential_read_allowed is False
        and ref.network_call_allowed is False
    )


def controlled_provider_surface_policy_blocks_direct_access(policy: ControlledProviderSurfacePolicy) -> bool:
    return (
        policy.invocation is False
        and policy.allow_existing_boundary_invocation is False
        and policy.allow_direct_provider_sdk is False
        and policy.allow_direct_network is False
        and policy.allow_credential_read is False
        and policy.allow_secret_read is False
        and policy.allow_endpoint_construction is False
        and policy.allow_recursive_model_call is False
        and policy.allow_autonomous_loop is False
    )


def controlled_model_invocation_boundary_is_not_invocation(boundary: ControlledModelInvocationBoundary) -> bool:
    return boundary.provider_invocation is False and boundary.ready_for_execution is False and controlled_model_invocation_flags_preserve_invocation_false(boundary.flags)


def controlled_model_invocation_decision_is_not_invocation(decision: ControlledModelInvocationPermissionDecision) -> bool:
    return (
        decision.invocation_permission is False
        and decision.invocation_allowed is False
        and decision.provider_invocation_allowed is False
        and decision.provider_sdk_allowed is False
        and decision.network_allowed is False
        and decision.credential_access_allowed is False
        and decision.secret_read_allowed is False
        and decision.agent_step_execution_allowed is False
    )


def v0340_readiness_report_is_not_invocation_ready(report: V0340ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_MODEL_INVOCATION_FLAG_NAMES) and report.invocation_readiness is False
