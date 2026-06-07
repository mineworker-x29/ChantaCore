from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Callable

from .boundary import (
    _metadata_flag_true,
    _require_non_blank,
    _validate_object_list,
    _validate_string_list,
)
from .model_request import (
    DEFAULT_MAX_PROMPT_PREVIEW_CHARS,
    ModelRequestEnvelope,
    model_request_envelope_is_not_invocation,
    validate_model_request_envelope,
)
from .model_response import (
    DEFAULT_MAX_RAW_RESPONSE_PREVIEW_CHARS,
    ModelResponseEnvelope,
    build_model_response_envelope_from_supplied_text,
)


V0344_VERSION = "v0.34.4"
V0344_RELEASE_NAME = "v0.34.4 Existing Provider Boundary Adapter"
BoundaryCallable = Callable[[Any], Any]

DEFAULT_ADAPTER_PROHIBITED_RUNTIME_ACTIONS = [
    "direct provider SDK",
    "direct provider invocation",
    "direct network",
    "credential access",
    "secret read",
    "env read",
    "endpoint construction",
    "general agent execution",
    "autonomous loop",
    "general tool execution",
    "tool calls",
    "function calls",
    "action execution",
    "shell execution",
    "subprocess execution",
    "command execution",
    "workspace write",
    "code edit",
    "patch application",
    "raw prompt persistence",
    "raw response persistence",
    "reference code execution",
    "reference import",
    "dependency install",
    "persistent trace write",
    "external trace sink",
    "UI runtime",
    "external control",
    "authority grant",
]

DEFAULT_ADAPTER_WITHDRAWAL_CONDITIONS = [
    "Any direct provider SDK, direct network, endpoint construction, credential, secret, or env-read path is introduced.",
    "Any new provider SDK adapter, credential loader, or network adapter is introduced.",
    "Any provider output, action, tool, shell, patch, command, reference, or harness execution path is introduced.",
    "Any raw prompt/response persistence path or unsafe readiness flag is introduced.",
]

DIRECT_ACCESS_FALSE_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_direct_provider_invocation",
    "ready_for_provider_sdk_invocation",
    "ready_for_direct_network_access",
    "ready_for_network_access",
    "ready_for_credential_access",
    "ready_for_secret_read",
    "ready_for_agent_step_execution",
    "ready_for_general_agent_execution",
    "ready_for_autonomous_agent_runtime",
    "ready_for_general_tool_execution",
    "ready_for_tool_calls",
    "ready_for_function_calls",
    "ready_for_action_execution",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_patch_application",
    "ready_for_registry_mutation",
    "ready_for_memory_mutation",
    "ready_for_raw_prompt_persistence",
    "ready_for_raw_response_persistence",
    "ready_for_raw_model_output_persistence",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
)

CONTROLLED_EXISTING_BOUNDARY_MODES = {
    "injected_existing_boundary",
    "project_local_existing_boundary",
}

ALLOW_EXISTING_BOUNDARY_DECISIONS = {
    "allow_injected_existing_boundary_call",
    "allow_project_local_existing_boundary_call",
}


class ExistingProviderBoundaryAdapterKind(StrEnum):
    INJECTED_CALLABLE_ADAPTER = "injected_callable_adapter"
    EXISTING_CHAT_SERVICE_BOUNDARY_ADAPTER = "existing_chat_service_boundary_adapter"
    EXISTING_PROVIDER_BOUNDARY_ADAPTER = "existing_provider_boundary_adapter"
    MOCK_BOUNDARY_ADAPTER = "mock_boundary_adapter"
    SUPPLIED_OUTPUT_ADAPTER = "supplied_output_adapter"
    DISABLED_ADAPTER = "disabled_adapter"
    FUTURE_GATE_ADAPTER = "future_gate_adapter"
    BLOCKED_ADAPTER = "blocked_adapter"
    UNKNOWN = "unknown"


class ExistingProviderInvocationMode(StrEnum):
    NO_INVOCATION = "no_invocation"
    DRY_RUN = "dry_run"
    MOCK_ONLY = "mock_only"
    SUPPLIED_OUTPUT_ONLY = "supplied_output_only"
    INJECTED_EXISTING_BOUNDARY = "injected_existing_boundary"
    PROJECT_LOCAL_EXISTING_BOUNDARY = "project_local_existing_boundary"
    BLOCKED = "blocked"
    FUTURE_GATE = "future_gate"
    UNKNOWN = "unknown"


class ExistingProviderBoundaryAdapterStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    ADAPTER_READY = "adapter_ready"
    ADAPTER_READY_WITH_GAPS = "adapter_ready_with_gaps"
    INVOCATION_ALLOWED = "invocation_allowed"
    INVOCATION_BLOCKED = "invocation_blocked"
    INVOCATION_COMPLETED = "invocation_completed"
    INVOCATION_FAILED_SAFE = "invocation_failed_safe"
    DISABLED = "disabled"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class ExistingProviderBoundaryReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    ADAPTER_CONTRACT_READY = "adapter_contract_ready"
    ADAPTER_VALIDATION_READY = "adapter_validation_ready"
    CONTROLLED_EXISTING_BOUNDARY_INVOCATION_READY = "controlled_existing_boundary_invocation_ready"
    DESIGN_HANDOFF_READY_FOR_V0345 = "design_handoff_ready_for_v0345"
    DESIGN_HANDOFF_READY_FOR_V0346 = "design_handoff_ready_for_v0346"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class ExistingProviderBoundaryDecisionKind(StrEnum):
    ALLOW_MOCK_RESPONSE = "allow_mock_response"
    ALLOW_SUPPLIED_RESPONSE = "allow_supplied_response"
    ALLOW_INJECTED_EXISTING_BOUNDARY_CALL = "allow_injected_existing_boundary_call"
    ALLOW_PROJECT_LOCAL_EXISTING_BOUNDARY_CALL = "allow_project_local_existing_boundary_call"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class ExistingProviderBoundaryOutcomeKind(StrEnum):
    MOCK_RESPONSE_RETURNED = "mock_response_returned"
    SUPPLIED_RESPONSE_RETURNED = "supplied_response_returned"
    EXISTING_BOUNDARY_RESPONSE_RETURNED = "existing_boundary_response_returned"
    RESPONSE_ENVELOPE_CREATED = "response_envelope_created"
    BLOCKED_RESULT = "blocked_result"
    NO_OP_RESULT = "no_op_result"
    SAFE_FAIL_RESULT = "safe_fail_result"
    UNKNOWN = "unknown"


class ExistingProviderBoundaryRiskKind(StrEnum):
    DIRECT_PROVIDER_SDK_RISK = "direct_provider_sdk_risk"
    ARBITRARY_NETWORK_RISK = "arbitrary_network_risk"
    CREDENTIAL_EXPOSURE_RISK = "credential_exposure_risk"
    SECRET_READ_RISK = "secret_read_risk"
    ENDPOINT_CONSTRUCTION_RISK = "endpoint_construction_risk"
    EXISTING_BOUNDARY_BYPASS_RISK = "existing_boundary_bypass_risk"
    RAW_PROMPT_PERSISTENCE_RISK = "raw_prompt_persistence_risk"
    RAW_RESPONSE_PERSISTENCE_RISK = "raw_response_persistence_risk"
    UNBOUNDED_PROMPT_RISK = "unbounded_prompt_risk"
    UNBOUNDED_RESPONSE_RISK = "unbounded_response_risk"
    PROVIDER_OUTPUT_ACTION_RISK = "provider_output_action_risk"
    RECURSIVE_MODEL_CALL_RISK = "recursive_model_call_risk"
    AUTONOMOUS_LOOP_RISK = "autonomous_loop_risk"
    TOOL_CALL_RISK = "tool_call_risk"
    FUNCTION_CALL_RISK = "function_call_risk"
    COMMAND_EXECUTION_RISK = "command_execution_risk"
    WORKSPACE_WRITE_RISK = "workspace_write_risk"
    REFERENCE_EXECUTION_RISK = "reference_execution_risk"
    EXTERNAL_HARNESS_EXECUTION_RISK = "external_harness_execution_risk"
    UNKNOWN = "unknown"


class ExistingProviderBoundarySourceKind(StrEnum):
    V0343_MODEL_RESPONSE_ENVELOPE = "v0343_model_response_envelope"
    V0342_MODEL_REQUEST_ENVELOPE = "v0342_model_request_envelope"
    V0341_PROVIDER_PROFILE = "v0341_provider_profile"
    V0340_MODEL_INVOCATION_BOUNDARY = "v0340_model_invocation_boundary"
    V0339_HANDOFF_PACKET = "v0339_handoff_packet"
    EXISTING_CHAT_SERVICE_BOUNDARY_REF = "existing_chat_service_boundary_ref"
    EXISTING_PROVIDER_BOUNDARY_REF = "existing_provider_boundary_ref"
    INJECTED_CALLABLE_REF = "injected_callable_ref"
    MOCK_CALLABLE_REF = "mock_callable_ref"
    SUPPLIED_OUTPUT_REF = "supplied_output_ref"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class ExistingProviderBoundaryCallPosture(StrEnum):
    NO_CALL = "no_call"
    MOCK_CALL_ONLY = "mock_call_only"
    SUPPLIED_OUTPUT_ONLY = "supplied_output_only"
    INJECTED_BOUNDARY_CALL_ALLOWED = "injected_boundary_call_allowed"
    PROJECT_LOCAL_BOUNDARY_CALL_ALLOWED = "project_local_boundary_call_allowed"
    DIRECT_SDK_BLOCKED = "direct_sdk_blocked"
    DIRECT_NETWORK_BLOCKED = "direct_network_blocked"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


def _validate_version_includes_v0344(version: str) -> None:
    _require_non_blank("version", version)
    if V0344_VERSION not in version:
        raise ValueError("version must include v0.34.4")


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.34.4")


def _validate_true(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not True:
            raise ValueError(f"{name} must always be True in v0.34.4")


def _validate_dict(name: str, value: dict[str, Any] | None) -> None:
    if value is not None and (not isinstance(value, dict) or not all(isinstance(key, str) for key in value)):
        raise TypeError(f"{name} must be dict[str, Any] or None")


def _validate_non_negative(name: str, value: int) -> None:
    if value < 0:
        raise ValueError(f"{name} must be >= 0")


def _validate_enum_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _validate_metadata_no_direct_access(metadata: dict[str, Any]) -> None:
    _validate_dict("metadata", metadata)
    if _metadata_flag_true(
        metadata,
        {
            "direct_provider_invocation",
            "provider_sdk_import",
            "provider_sdk_invocation",
            "direct_network",
            "network_call",
            "credential_access",
            "secret_read",
            "env_read",
            "endpoint_construction",
            "action_execution",
            "tool_call_execution",
            "function_call_execution",
            "shell_execution",
            "command_execution",
            "workspace_write",
            "patch_application",
            "raw_prompt_persistence",
            "raw_response_persistence",
            "persistent_trace_write",
        },
    ):
        raise ValueError("v0.34.4 metadata cannot imply direct access, execution, or raw persistence")


def _validate_contains_terms(name: str, values: list[str], terms: list[str]) -> None:
    _validate_string_list(name, values)
    lowered = " | ".join(values).lower()
    missing = [term for term in terms if term.lower() not in lowered]
    if missing:
        raise ValueError(f"{name} missing required terms: {missing}")


def _bounded(value: str, limit: int) -> tuple[str, bool]:
    if len(value) <= limit:
        return value, False
    return value[:limit], True


def _mode_allows_existing_boundary_call(mode: ExistingProviderInvocationMode | str | None) -> bool:
    return mode is not None and ExistingProviderInvocationMode(mode).value in CONTROLLED_EXISTING_BOUNDARY_MODES


def _decision_allows_existing_boundary_call(decision_kind: ExistingProviderBoundaryDecisionKind | str) -> bool:
    return ExistingProviderBoundaryDecisionKind(decision_kind).value in ALLOW_EXISTING_BOUNDARY_DECISIONS


def _coerce_response_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in ("response_text", "text", "content", "message"):
            candidate = value.get(key)
            if isinstance(candidate, str):
                return candidate
        return "structured boundary response returned without executable handling"
    if value is None:
        return ""
    return str(value)


@dataclass(frozen=True)
class ExistingProviderBoundaryAdapterFlagSet:
    flag_set_id: str
    version: str = V0344_VERSION
    existing_provider_boundary_adapter_constructed: bool = False
    adapter_validation_available: bool = False
    controlled_existing_boundary_call_available: bool = False
    response_envelope_bridge_available: bool = False
    ready_for_v0345_model_output_action_quarantine: bool = False
    ready_for_v0346_agent_step_runner_model_integration: bool = False
    ready_for_execution: bool = False
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
    ready_for_agent_step_execution: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_tool_calls: bool = False
    ready_for_function_calls: bool = False
    ready_for_action_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_application: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_raw_prompt_persistence: bool = False
    ready_for_raw_response_persistence: bool = False
    ready_for_raw_model_output_persistence: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version_includes_v0344(self.version)
        _validate_false(self, DIRECT_ACCESS_FALSE_FLAG_NAMES)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False in v0.34.4")
        _validate_metadata_no_direct_access(self.metadata)


@dataclass(frozen=True)
class ExistingProviderBoundarySourceRef:
    source_ref_id: str
    source_kind: ExistingProviderBoundarySourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        ExistingProviderBoundarySourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_direct_access(self.metadata)

    @property
    def sdk_access(self) -> bool:
        return False

    @property
    def network_access(self) -> bool:
        return False

    @property
    def credential_access(self) -> bool:
        return False


@dataclass(frozen=True)
class ExistingProviderBoundaryCallableRef:
    callable_ref_id: str
    callable_name: str
    callable_kind: ExistingProviderBoundaryAdapterKind | str
    callable_summary: str
    source_refs: list[ExistingProviderBoundarySourceRef] = field(default_factory=list)
    direct_sdk: bool = False
    direct_network: bool = False
    credential_reader: bool = False
    secret_reader: bool = False
    shell_based: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("callable_ref_id", self.callable_ref_id)
        _require_non_blank("callable_name", self.callable_name)
        ExistingProviderBoundaryAdapterKind(self.callable_kind)
        _require_non_blank("callable_summary", self.callable_summary)
        _validate_object_list("source_refs", self.source_refs, ExistingProviderBoundarySourceRef)
        _validate_false(self, ("direct_sdk", "direct_network", "credential_reader", "secret_reader", "shell_based"))
        _validate_metadata_no_direct_access(self.metadata)

    @property
    def credential_access(self) -> bool:
        return False


@dataclass(frozen=True)
class ExistingProviderBoundaryAdapterPolicy:
    adapter_policy_id: str
    allowed_adapter_kinds: list[ExistingProviderBoundaryAdapterKind | str] = field(default_factory=list)
    allowed_invocation_modes: list[ExistingProviderInvocationMode | str] = field(default_factory=list)
    blocked_adapter_kinds: list[ExistingProviderBoundaryAdapterKind | str] = field(default_factory=list)
    prohibited_risks: list[ExistingProviderBoundaryRiskKind | str] = field(default_factory=list)
    allow_mock_call: bool = True
    allow_supplied_output: bool = True
    allow_injected_existing_boundary_call: bool = True
    allow_project_local_existing_boundary_call: bool = False
    allow_direct_provider_sdk: bool = False
    allow_direct_network: bool = False
    allow_credential_read: bool = False
    allow_secret_read: bool = False
    allow_endpoint_construction: bool = False
    allow_recursive_call: bool = False
    allow_tool_calls: bool = False
    allow_function_calls: bool = False
    allow_action_execution: bool = False
    allow_raw_prompt_persistence: bool = False
    allow_raw_response_persistence: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("adapter_policy_id", self.adapter_policy_id)
        _validate_enum_list("allowed_adapter_kinds", self.allowed_adapter_kinds, ExistingProviderBoundaryAdapterKind)
        _validate_enum_list("allowed_invocation_modes", self.allowed_invocation_modes, ExistingProviderInvocationMode)
        _validate_enum_list("blocked_adapter_kinds", self.blocked_adapter_kinds, ExistingProviderBoundaryAdapterKind)
        _validate_enum_list("prohibited_risks", self.prohibited_risks, ExistingProviderBoundaryRiskKind)
        _validate_false(
            self,
            (
                "allow_direct_provider_sdk",
                "allow_direct_network",
                "allow_credential_read",
                "allow_secret_read",
                "allow_endpoint_construction",
                "allow_recursive_call",
                "allow_tool_calls",
                "allow_function_calls",
                "allow_action_execution",
                "allow_raw_prompt_persistence",
                "allow_raw_response_persistence",
            ),
        )
        _validate_metadata_no_direct_access(self.metadata)

    @property
    def invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class ExistingProviderBoundaryAdapterDescriptor:
    adapter_id: str
    version: str
    adapter_kind: ExistingProviderBoundaryAdapterKind | str
    invocation_mode: ExistingProviderInvocationMode | str
    call_posture: ExistingProviderBoundaryCallPosture | str
    callable_ref: ExistingProviderBoundaryCallableRef | None
    adapter_policy: ExistingProviderBoundaryAdapterPolicy
    flags: ExistingProviderBoundaryAdapterFlagSet
    source_refs: list[ExistingProviderBoundarySourceRef]
    status: ExistingProviderBoundaryAdapterStatus | str
    readiness_level: ExistingProviderBoundaryReadinessLevel | str
    summary: str
    enabled: bool = True
    future_gated: bool = False
    ready_for_controlled_invocation: bool = False
    ready_for_direct_provider_invocation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("adapter_id", self.adapter_id)
        _validate_version_includes_v0344(self.version)
        ExistingProviderBoundaryAdapterKind(self.adapter_kind)
        mode = ExistingProviderInvocationMode(self.invocation_mode)
        ExistingProviderBoundaryCallPosture(self.call_posture)
        if self.callable_ref is not None and not isinstance(self.callable_ref, ExistingProviderBoundaryCallableRef):
            raise TypeError("callable_ref must be ExistingProviderBoundaryCallableRef or None")
        if not isinstance(self.adapter_policy, ExistingProviderBoundaryAdapterPolicy):
            raise TypeError("adapter_policy must be ExistingProviderBoundaryAdapterPolicy")
        if not isinstance(self.flags, ExistingProviderBoundaryAdapterFlagSet):
            raise TypeError("flags must be ExistingProviderBoundaryAdapterFlagSet")
        if not existing_provider_boundary_flags_preserve_direct_access_false(self.flags):
            raise ValueError("flags must preserve direct access and execution false")
        _validate_object_list("source_refs", self.source_refs, ExistingProviderBoundarySourceRef)
        ExistingProviderBoundaryAdapterStatus(self.status)
        ExistingProviderBoundaryReadinessLevel(self.readiness_level)
        _require_non_blank("summary", self.summary)
        if self.ready_for_controlled_invocation and not _mode_allows_existing_boundary_call(mode):
            raise ValueError("ready_for_controlled_invocation requires allowed existing boundary mode")
        _validate_false(self, ("ready_for_direct_provider_invocation", "ready_for_execution"))
        _validate_metadata_no_direct_access(self.metadata)

    @property
    def new_provider_sdk_adapter(self) -> bool:
        return False


@dataclass(frozen=True)
class ExistingProviderBoundaryInvocationInput:
    invocation_input_id: str
    source_version: str
    request_envelope_id: str
    provider_profile_id: str | None
    adapter_id: str | None
    invocation_mode: ExistingProviderInvocationMode | str
    prompt_payload_preview: str
    bounded_prompt_payload: dict[str, Any]
    task_summary: str
    source_refs: list[ExistingProviderBoundarySourceRef] = field(default_factory=list)
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_ADAPTER_PROHIBITED_RUNTIME_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("invocation_input_id", self.invocation_input_id)
        _validate_version_includes_v0344(self.source_version)
        _require_non_blank("request_envelope_id", self.request_envelope_id)
        ExistingProviderInvocationMode(self.invocation_mode)
        if len(self.prompt_payload_preview) > DEFAULT_MAX_PROMPT_PREVIEW_CHARS:
            raise ValueError("prompt_payload_preview must be bounded")
        _validate_dict("bounded_prompt_payload", self.bounded_prompt_payload)
        _require_non_blank("task_summary", self.task_summary)
        _validate_object_list("source_refs", self.source_refs, ExistingProviderBoundarySourceRef)
        _validate_contains_terms(
            "prohibited_runtime_actions",
            self.prohibited_runtime_actions,
            ["direct provider SDK", "direct network", "credential access", "secret read", "endpoint construction", "tool calls", "function calls", "action execution", "shell", "command", "write", "edit", "patch", "reference code execution"],
        )
        _validate_metadata_no_direct_access(self.metadata)

    @property
    def direct_sdk_network_request(self) -> bool:
        return False


@dataclass(frozen=True)
class ExistingProviderBoundaryInvocationDecision:
    decision_id: str
    invocation_input_id: str
    decision_kind: ExistingProviderBoundaryDecisionKind | str
    reason: str
    allowed_invocation_mode: ExistingProviderInvocationMode | str | None = None
    risk_kinds: list[ExistingProviderBoundaryRiskKind | str] = field(default_factory=list)
    controlled_existing_boundary_invocation_allowed: bool = False
    direct_provider_invocation_allowed: bool = False
    provider_sdk_allowed: bool = False
    direct_network_allowed: bool = False
    credential_access_allowed: bool = False
    secret_read_allowed: bool = False
    tool_calls_allowed: bool = False
    function_calls_allowed: bool = False
    action_execution_allowed: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("decision_id", self.decision_id)
        _require_non_blank("invocation_input_id", self.invocation_input_id)
        decision_kind = ExistingProviderBoundaryDecisionKind(self.decision_kind)
        _require_non_blank("reason", self.reason)
        if self.allowed_invocation_mode is not None:
            ExistingProviderInvocationMode(self.allowed_invocation_mode)
        _validate_enum_list("risk_kinds", self.risk_kinds, ExistingProviderBoundaryRiskKind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.controlled_existing_boundary_invocation_allowed and not _decision_allows_existing_boundary_call(decision_kind):
            raise ValueError("controlled existing boundary invocation requires allow existing-boundary decision")
        if self.controlled_existing_boundary_invocation_allowed and not _mode_allows_existing_boundary_call(self.allowed_invocation_mode):
            raise ValueError("controlled existing boundary invocation requires allowed existing-boundary mode")
        _validate_false(
            self,
            (
                "direct_provider_invocation_allowed",
                "provider_sdk_allowed",
                "direct_network_allowed",
                "credential_access_allowed",
                "secret_read_allowed",
                "tool_calls_allowed",
                "function_calls_allowed",
                "action_execution_allowed",
            ),
        )
        _validate_metadata_no_direct_access(self.metadata)


@dataclass(frozen=True)
class ExistingProviderBoundaryCallRecord:
    call_record_id: str
    invocation_input_id: str
    decision_id: str
    adapter_id: str | None
    invocation_mode: ExistingProviderInvocationMode | str
    call_started: bool
    call_completed: bool
    call_failed_safe: bool
    used_injected_callable: bool
    used_project_local_boundary: bool
    used_direct_provider_sdk: bool
    used_direct_network_client: bool
    read_credentials: bool
    read_secrets: bool
    executed_shell: bool
    executed_tools: bool
    wrote_workspace: bool
    raw_prompt_persisted: bool
    raw_response_persisted: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("call_record_id", self.call_record_id)
        _require_non_blank("invocation_input_id", self.invocation_input_id)
        _require_non_blank("decision_id", self.decision_id)
        ExistingProviderInvocationMode(self.invocation_mode)
        _validate_false(
            self,
            (
                "used_direct_provider_sdk",
                "used_direct_network_client",
                "read_credentials",
                "read_secrets",
                "executed_shell",
                "executed_tools",
                "wrote_workspace",
                "raw_prompt_persisted",
                "raw_response_persisted",
            ),
        )
        _require_non_blank("summary", self.summary)
        _validate_metadata_no_direct_access(self.metadata)

    @property
    def persistent_log(self) -> bool:
        return False


@dataclass(frozen=True)
class ExistingProviderBoundaryInvocationResult:
    invocation_result_id: str
    invocation_input_id: str
    decision_id: str
    call_record_id: str | None
    outcome_kind: ExistingProviderBoundaryOutcomeKind | str
    response_text_preview: str | None
    response_char_count: int
    response_envelope_id: str | None
    sanitization_report_id: str | None
    validation_report_id: str | None
    blocked_reason: str | None
    safe_fail_reason: str | None
    redacted: bool
    truncated: bool
    summary: str
    ready_for_v0345_model_output_action_quarantine: bool = False
    ready_for_action_execution: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("invocation_result_id", self.invocation_result_id)
        _require_non_blank("invocation_input_id", self.invocation_input_id)
        _require_non_blank("decision_id", self.decision_id)
        ExistingProviderBoundaryOutcomeKind(self.outcome_kind)
        if self.response_text_preview is not None and len(self.response_text_preview) > DEFAULT_MAX_RAW_RESPONSE_PREVIEW_CHARS:
            raise ValueError("response_text_preview must be bounded")
        _validate_non_negative("response_char_count", self.response_char_count)
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_action_execution", "ready_for_execution"))
        _validate_metadata_no_direct_access(self.metadata)

    @property
    def action(self) -> bool:
        return False

    @property
    def persistence(self) -> bool:
        return False


@dataclass(frozen=True)
class ExistingProviderBoundaryAdapterValidationFinding:
    finding_id: str
    adapter_id: str | None
    decision_kind: ExistingProviderBoundaryDecisionKind | str
    risk_kinds: list[ExistingProviderBoundaryRiskKind | str]
    summary: str
    blocked: bool = False
    future_gated: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        ExistingProviderBoundaryDecisionKind(self.decision_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, ExistingProviderBoundaryRiskKind)
        _require_non_blank("summary", self.summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_direct_access(self.metadata)

    @property
    def invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class ExistingProviderBoundaryAdapterValidationReport:
    validation_report_id: str
    version: str
    adapter_id: str | None
    findings: list[ExistingProviderBoundaryAdapterValidationFinding]
    validation_passed: bool
    blocked_reasons: list[str]
    warning_items: list[str]
    direct_sdk_blocked: bool
    direct_network_blocked: bool
    credential_access_blocked: bool
    secret_read_blocked: bool
    raw_persistence_blocked: bool
    summary: str
    ready_for_controlled_existing_boundary_invocation: bool = False
    ready_for_direct_provider_invocation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version_includes_v0344(self.version)
        _validate_object_list("findings", self.findings, ExistingProviderBoundaryAdapterValidationFinding)
        _validate_string_list("blocked_reasons", self.blocked_reasons)
        _validate_string_list("warning_items", self.warning_items)
        if self.validation_passed and self.blocked_reasons:
            raise ValueError("validation_passed cannot be True if blocked_reasons is non-empty")
        _validate_true(self, ("direct_sdk_blocked", "direct_network_blocked", "credential_access_blocked", "secret_read_blocked", "raw_persistence_blocked"))
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_direct_provider_invocation", "ready_for_execution"))
        _validate_metadata_no_direct_access(self.metadata)

    @property
    def certification(self) -> bool:
        return False


@dataclass(frozen=True)
class ExistingProviderBoundaryInvocationReport:
    report_id: str
    version: str
    adapter_id: str | None
    invocation_input_id: str | None
    invocation_result_id: str | None
    validation_report_id: str | None
    status: ExistingProviderBoundaryAdapterStatus | str
    readiness_level: ExistingProviderBoundaryReadinessLevel | str
    summary: str
    call_count: int = 0
    completed_call_count: int = 0
    blocked_call_count: int = 0
    safe_fail_count: int = 0
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0345_model_output_action_quarantine: bool = False
    ready_for_v0346_agent_step_runner_model_integration: bool = False
    ready_for_controlled_existing_boundary_invocation: bool = False
    ready_for_direct_provider_invocation: bool = False
    ready_for_action_execution: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=lambda: list(DEFAULT_ADAPTER_WITHDRAWAL_CONDITIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0344(self.version)
        ExistingProviderBoundaryAdapterStatus(self.status)
        ExistingProviderBoundaryReadinessLevel(self.readiness_level)
        _require_non_blank("summary", self.summary)
        for name in ("call_count", "completed_call_count", "blocked_call_count", "safe_fail_count"):
            _validate_non_negative(name, getattr(self, name))
        for name in ("completed_items", "blocked_items", "future_track_items", "gaps", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, ("ready_for_direct_provider_invocation", "ready_for_action_execution", "ready_for_execution"))
        _validate_metadata_no_direct_access(self.metadata)

    @property
    def runtime_expansion(self) -> bool:
        return False


@dataclass(frozen=True)
class ExistingProviderBoundaryRunPreview:
    run_preview_id: str
    adapter_id: str | None = None
    planned_steps: list[str] = field(default_factory=lambda: ["validate adapter policy", "decide controlled existing-boundary invocation", "bridge untrusted provider output into response sanitizer"])
    expected_artifacts: list[str] = field(default_factory=lambda: ["ExistingProviderBoundaryInvocationDecision", "ExistingProviderBoundaryCallRecord", "ModelResponseEnvelope", "ExistingProviderBoundaryInvocationResult"])
    explicitly_not_performed: list[str] = field(default_factory=lambda: list(DEFAULT_ADAPTER_PROHIBITED_RUNTIME_ACTIONS))
    no_direct_provider_sdk_guarantee: bool = True
    no_direct_network_access_guarantee: bool = True
    no_credential_access_guarantee: bool = True
    no_secret_read_guarantee: bool = True
    no_endpoint_construction_guarantee: bool = True
    no_agent_step_execution_guarantee: bool = True
    no_tool_execution_guarantee: bool = True
    no_action_execution_guarantee: bool = True
    no_shell_execution_guarantee: bool = True
    no_subprocess_guarantee: bool = True
    no_command_execution_guarantee: bool = True
    no_workspace_write_guarantee: bool = True
    no_code_edit_guarantee: bool = True
    no_patch_application_guarantee: bool = True
    no_raw_prompt_persistence_guarantee: bool = True
    no_raw_response_persistence_guarantee: bool = True
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
                raise ValueError(f"{name} must be True in v0.34.4")
        _validate_metadata_no_direct_access(self.metadata)

    @property
    def direct_provider_invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class ExistingProviderBoundaryNoDirectAccessGuarantee:
    guarantee_id: str
    version: str = V0344_VERSION
    no_direct_provider_invocation: bool = True
    no_provider_sdk_invocation: bool = True
    no_direct_network_access: bool = True
    no_credential_access: bool = True
    no_secret_read: bool = True
    no_env_read: bool = True
    no_endpoint_construction: bool = True
    no_agent_step_execution: bool = True
    no_general_agent_execution: bool = True
    no_autonomous_agent_runtime: bool = True
    no_general_tool_execution: bool = True
    no_tool_call_execution: bool = True
    no_function_call_execution: bool = True
    no_action_execution: bool = True
    no_shell_execution: bool = True
    no_subprocess: bool = True
    no_command_execution: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_patch_application: bool = True
    no_raw_prompt_persistence: bool = True
    no_raw_response_persistence: bool = True
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
        _validate_version_includes_v0344(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.34.4")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_direct_access(self.metadata)


@dataclass(frozen=True)
class V0344ReadinessReport:
    report_id: str
    version: str
    adapter_id: str | None
    invocation_report_id: str | None
    invocation_result_id: str | None
    validation_report_id: str | None
    summary: str
    ready_for_v0345_model_output_action_quarantine: bool = False
    ready_for_v0346_agent_step_runner_model_integration: bool = False
    ready_for_execution: bool = False
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
    ready_for_agent_step_execution: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_tool_calls: bool = False
    ready_for_function_calls: bool = False
    ready_for_action_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_application: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_raw_prompt_persistence: bool = False
    ready_for_raw_response_persistence: bool = False
    ready_for_raw_model_output_persistence: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_ADAPTER_PROHIBITED_RUNTIME_ACTIONS))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=lambda: list(DEFAULT_ADAPTER_WITHDRAWAL_CONDITIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0344(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(self, DIRECT_ACCESS_FALSE_FLAG_NAMES)
        for name in ("completed_items", "blocked_items", "future_track_items", "prohibited_until_later_gate", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_contains_terms(
            "prohibited_until_later_gate",
            self.prohibited_until_later_gate,
            ["direct provider SDK", "direct network", "credential access", "secret read", "endpoint construction", "general agent execution", "autonomous loop", "general tool execution", "tool calls", "function calls", "action execution", "shell", "subprocess", "command", "workspace write", "code edit", "patch application", "raw prompt persistence", "raw response persistence", "reference code execution", "reference import", "dependency install", "persistent trace write", "external trace sink", "UI runtime", "external control", "authority grant"],
        )
        _validate_metadata_no_direct_access(self.metadata)

    @property
    def general_execution_ready(self) -> bool:
        return False


def build_existing_provider_boundary_adapter_flags(
    flag_set_id: str = "existing_provider_boundary_adapter_flags:v0.34.4",
    **kwargs: Any,
) -> ExistingProviderBoundaryAdapterFlagSet:
    return ExistingProviderBoundaryAdapterFlagSet(
        flag_set_id=flag_set_id,
        version=kwargs.pop("version", V0344_VERSION),
        existing_provider_boundary_adapter_constructed=kwargs.pop("existing_provider_boundary_adapter_constructed", True),
        adapter_validation_available=kwargs.pop("adapter_validation_available", True),
        controlled_existing_boundary_call_available=kwargs.pop("controlled_existing_boundary_call_available", True),
        response_envelope_bridge_available=kwargs.pop("response_envelope_bridge_available", True),
        ready_for_v0345_model_output_action_quarantine=kwargs.pop("ready_for_v0345_model_output_action_quarantine", True),
        ready_for_v0346_agent_step_runner_model_integration=kwargs.pop("ready_for_v0346_agent_step_runner_model_integration", True),
        ready_for_controlled_model_invocation=kwargs.pop("ready_for_controlled_model_invocation", True),
        ready_for_existing_boundary_invocation=kwargs.pop("ready_for_existing_boundary_invocation", True),
        ready_for_real_model_invocation=kwargs.pop("ready_for_real_model_invocation", True),
        ready_for_model_invocation=kwargs.pop("ready_for_model_invocation", True),
        **kwargs,
    )


def build_existing_provider_boundary_source_ref(
    source_ref_id: str,
    source_kind: ExistingProviderBoundarySourceKind | str = ExistingProviderBoundarySourceKind.INJECTED_CALLABLE_REF,
    source_id: str = "existing_provider_boundary_source",
    source_summary: str = "Existing provider boundary source ref only; no SDK/network/credential access.",
    **kwargs: Any,
) -> ExistingProviderBoundarySourceRef:
    return ExistingProviderBoundarySourceRef(
        source_ref_id=source_ref_id,
        source_kind=source_kind,
        source_id=source_id,
        source_summary=source_summary,
        **kwargs,
    )


def build_existing_provider_boundary_callable_ref(
    callable_ref_id: str = "existing_provider_boundary_callable_ref:v0.34.4",
    **kwargs: Any,
) -> ExistingProviderBoundaryCallableRef:
    return ExistingProviderBoundaryCallableRef(
        callable_ref_id=callable_ref_id,
        callable_name=kwargs.pop("callable_name", "injected_existing_boundary_callable"),
        callable_kind=kwargs.pop("callable_kind", ExistingProviderBoundaryAdapterKind.INJECTED_CALLABLE_ADAPTER),
        callable_summary=kwargs.pop("callable_summary", "Injected existing boundary callable metadata only."),
        **kwargs,
    )


def build_existing_provider_boundary_adapter_policy(
    adapter_policy_id: str = "existing_provider_boundary_adapter_policy:v0.34.4",
    **kwargs: Any,
) -> ExistingProviderBoundaryAdapterPolicy:
    return ExistingProviderBoundaryAdapterPolicy(
        adapter_policy_id=adapter_policy_id,
        allowed_adapter_kinds=kwargs.pop("allowed_adapter_kinds", [ExistingProviderBoundaryAdapterKind.INJECTED_CALLABLE_ADAPTER, ExistingProviderBoundaryAdapterKind.MOCK_BOUNDARY_ADAPTER, ExistingProviderBoundaryAdapterKind.SUPPLIED_OUTPUT_ADAPTER]),
        allowed_invocation_modes=kwargs.pop("allowed_invocation_modes", [ExistingProviderInvocationMode.INJECTED_EXISTING_BOUNDARY, ExistingProviderInvocationMode.MOCK_ONLY, ExistingProviderInvocationMode.SUPPLIED_OUTPUT_ONLY]),
        blocked_adapter_kinds=kwargs.pop("blocked_adapter_kinds", [ExistingProviderBoundaryAdapterKind.BLOCKED_ADAPTER, ExistingProviderBoundaryAdapterKind.DISABLED_ADAPTER, ExistingProviderBoundaryAdapterKind.UNKNOWN]),
        prohibited_risks=kwargs.pop("prohibited_risks", [ExistingProviderBoundaryRiskKind.DIRECT_PROVIDER_SDK_RISK, ExistingProviderBoundaryRiskKind.ARBITRARY_NETWORK_RISK, ExistingProviderBoundaryRiskKind.CREDENTIAL_EXPOSURE_RISK, ExistingProviderBoundaryRiskKind.SECRET_READ_RISK, ExistingProviderBoundaryRiskKind.COMMAND_EXECUTION_RISK, ExistingProviderBoundaryRiskKind.WORKSPACE_WRITE_RISK]),
        **kwargs,
    )


def default_existing_provider_boundary_adapter_policy(**kwargs: Any) -> ExistingProviderBoundaryAdapterPolicy:
    return build_existing_provider_boundary_adapter_policy(**kwargs)


def build_existing_provider_boundary_adapter_descriptor(
    adapter_id: str = "existing_provider_boundary_adapter:v0.34.4",
    **kwargs: Any,
) -> ExistingProviderBoundaryAdapterDescriptor:
    return ExistingProviderBoundaryAdapterDescriptor(
        adapter_id=adapter_id,
        version=kwargs.pop("version", V0344_VERSION),
        adapter_kind=kwargs.pop("adapter_kind", ExistingProviderBoundaryAdapterKind.INJECTED_CALLABLE_ADAPTER),
        invocation_mode=kwargs.pop("invocation_mode", ExistingProviderInvocationMode.INJECTED_EXISTING_BOUNDARY),
        call_posture=kwargs.pop("call_posture", ExistingProviderBoundaryCallPosture.INJECTED_BOUNDARY_CALL_ALLOWED),
        callable_ref=kwargs.pop("callable_ref", build_existing_provider_boundary_callable_ref()),
        adapter_policy=kwargs.pop("adapter_policy", default_existing_provider_boundary_adapter_policy()),
        flags=kwargs.pop("flags", build_existing_provider_boundary_adapter_flags()),
        source_refs=kwargs.pop("source_refs", []),
        status=kwargs.pop("status", ExistingProviderBoundaryAdapterStatus.ADAPTER_READY),
        readiness_level=kwargs.pop("readiness_level", ExistingProviderBoundaryReadinessLevel.CONTROLLED_EXISTING_BOUNDARY_INVOCATION_READY),
        summary=kwargs.pop("summary", "Existing provider boundary adapter using injected callable only; no direct SDK/network access."),
        ready_for_controlled_invocation=kwargs.pop("ready_for_controlled_invocation", True),
        **kwargs,
    )


def build_existing_provider_boundary_invocation_input(
    invocation_input_id: str = "existing_provider_boundary_invocation_input:v0.34.4",
    **kwargs: Any,
) -> ExistingProviderBoundaryInvocationInput:
    return ExistingProviderBoundaryInvocationInput(
        invocation_input_id=invocation_input_id,
        source_version=kwargs.pop("source_version", V0344_VERSION),
        request_envelope_id=kwargs.pop("request_envelope_id", "model_request_envelope:v0.34.2"),
        provider_profile_id=kwargs.pop("provider_profile_id", None),
        adapter_id=kwargs.pop("adapter_id", "existing_provider_boundary_adapter:v0.34.4"),
        invocation_mode=kwargs.pop("invocation_mode", ExistingProviderInvocationMode.INJECTED_EXISTING_BOUNDARY),
        prompt_payload_preview=kwargs.pop("prompt_payload_preview", "bounded prompt preview for existing boundary"),
        bounded_prompt_payload=kwargs.pop("bounded_prompt_payload", {"prompt_preview": "bounded prompt preview for existing boundary"}),
        task_summary=kwargs.pop("task_summary", "Controlled existing provider boundary invocation input."),
        **kwargs,
    )


def build_existing_provider_boundary_invocation_decision(
    decision_id: str = "existing_provider_boundary_invocation_decision:v0.34.4",
    **kwargs: Any,
) -> ExistingProviderBoundaryInvocationDecision:
    return ExistingProviderBoundaryInvocationDecision(
        decision_id=decision_id,
        invocation_input_id=kwargs.pop("invocation_input_id", "existing_provider_boundary_invocation_input:v0.34.4"),
        decision_kind=kwargs.pop("decision_kind", ExistingProviderBoundaryDecisionKind.ALLOW_INJECTED_EXISTING_BOUNDARY_CALL),
        reason=kwargs.pop("reason", "Policy allows injected existing boundary callable; direct SDK/network remains blocked."),
        allowed_invocation_mode=kwargs.pop("allowed_invocation_mode", ExistingProviderInvocationMode.INJECTED_EXISTING_BOUNDARY),
        controlled_existing_boundary_invocation_allowed=kwargs.pop("controlled_existing_boundary_invocation_allowed", True),
        **kwargs,
    )


def build_existing_provider_boundary_call_record(
    call_record_id: str = "existing_provider_boundary_call_record:v0.34.4",
    **kwargs: Any,
) -> ExistingProviderBoundaryCallRecord:
    return ExistingProviderBoundaryCallRecord(
        call_record_id=call_record_id,
        invocation_input_id=kwargs.pop("invocation_input_id", "existing_provider_boundary_invocation_input:v0.34.4"),
        decision_id=kwargs.pop("decision_id", "existing_provider_boundary_invocation_decision:v0.34.4"),
        adapter_id=kwargs.pop("adapter_id", "existing_provider_boundary_adapter:v0.34.4"),
        invocation_mode=kwargs.pop("invocation_mode", ExistingProviderInvocationMode.INJECTED_EXISTING_BOUNDARY),
        call_started=kwargs.pop("call_started", False),
        call_completed=kwargs.pop("call_completed", False),
        call_failed_safe=kwargs.pop("call_failed_safe", False),
        used_injected_callable=kwargs.pop("used_injected_callable", False),
        used_project_local_boundary=kwargs.pop("used_project_local_boundary", False),
        used_direct_provider_sdk=kwargs.pop("used_direct_provider_sdk", False),
        used_direct_network_client=kwargs.pop("used_direct_network_client", False),
        read_credentials=kwargs.pop("read_credentials", False),
        read_secrets=kwargs.pop("read_secrets", False),
        executed_shell=kwargs.pop("executed_shell", False),
        executed_tools=kwargs.pop("executed_tools", False),
        wrote_workspace=kwargs.pop("wrote_workspace", False),
        raw_prompt_persisted=kwargs.pop("raw_prompt_persisted", False),
        raw_response_persisted=kwargs.pop("raw_response_persisted", False),
        summary=kwargs.pop("summary", "Existing boundary call record metadata only; not persistent log."),
        **kwargs,
    )


def build_existing_provider_boundary_invocation_result(
    invocation_result_id: str = "existing_provider_boundary_invocation_result:v0.34.4",
    **kwargs: Any,
) -> ExistingProviderBoundaryInvocationResult:
    return ExistingProviderBoundaryInvocationResult(
        invocation_result_id=invocation_result_id,
        invocation_input_id=kwargs.pop("invocation_input_id", "existing_provider_boundary_invocation_input:v0.34.4"),
        decision_id=kwargs.pop("decision_id", "existing_provider_boundary_invocation_decision:v0.34.4"),
        call_record_id=kwargs.pop("call_record_id", None),
        outcome_kind=kwargs.pop("outcome_kind", ExistingProviderBoundaryOutcomeKind.BLOCKED_RESULT),
        response_text_preview=kwargs.pop("response_text_preview", None),
        response_char_count=kwargs.pop("response_char_count", 0),
        response_envelope_id=kwargs.pop("response_envelope_id", None),
        sanitization_report_id=kwargs.pop("sanitization_report_id", None),
        validation_report_id=kwargs.pop("validation_report_id", None),
        blocked_reason=kwargs.pop("blocked_reason", "No controlled existing boundary call was performed."),
        safe_fail_reason=kwargs.pop("safe_fail_reason", None),
        redacted=kwargs.pop("redacted", True),
        truncated=kwargs.pop("truncated", False),
        summary=kwargs.pop("summary", "Existing boundary invocation result; no action execution."),
        ready_for_v0345_model_output_action_quarantine=kwargs.pop("ready_for_v0345_model_output_action_quarantine", False),
        **kwargs,
    )


def build_existing_provider_boundary_adapter_validation_finding(
    finding_id: str,
    **kwargs: Any,
) -> ExistingProviderBoundaryAdapterValidationFinding:
    return ExistingProviderBoundaryAdapterValidationFinding(
        finding_id=finding_id,
        adapter_id=kwargs.pop("adapter_id", None),
        decision_kind=kwargs.pop("decision_kind", ExistingProviderBoundaryDecisionKind.ALLOW_INJECTED_EXISTING_BOUNDARY_CALL),
        risk_kinds=kwargs.pop("risk_kinds", []),
        summary=kwargs.pop("summary", "Existing provider boundary adapter validation finding; no direct access."),
        **kwargs,
    )


def build_existing_provider_boundary_adapter_validation_report(
    validation_report_id: str = "existing_provider_boundary_adapter_validation_report:v0.34.4",
    **kwargs: Any,
) -> ExistingProviderBoundaryAdapterValidationReport:
    return ExistingProviderBoundaryAdapterValidationReport(
        validation_report_id=validation_report_id,
        version=kwargs.pop("version", V0344_VERSION),
        adapter_id=kwargs.pop("adapter_id", None),
        findings=kwargs.pop("findings", []),
        validation_passed=kwargs.pop("validation_passed", True),
        blocked_reasons=kwargs.pop("blocked_reasons", []),
        warning_items=kwargs.pop("warning_items", []),
        direct_sdk_blocked=kwargs.pop("direct_sdk_blocked", True),
        direct_network_blocked=kwargs.pop("direct_network_blocked", True),
        credential_access_blocked=kwargs.pop("credential_access_blocked", True),
        secret_read_blocked=kwargs.pop("secret_read_blocked", True),
        raw_persistence_blocked=kwargs.pop("raw_persistence_blocked", True),
        summary=kwargs.pop("summary", "Existing provider boundary adapter validation report; not certification."),
        **kwargs,
    )


def build_existing_provider_boundary_invocation_report(
    report_id: str = "existing_provider_boundary_invocation_report:v0.34.4",
    **kwargs: Any,
) -> ExistingProviderBoundaryInvocationReport:
    return ExistingProviderBoundaryInvocationReport(
        report_id=report_id,
        version=kwargs.pop("version", V0344_VERSION),
        adapter_id=kwargs.pop("adapter_id", "existing_provider_boundary_adapter:v0.34.4"),
        invocation_input_id=kwargs.pop("invocation_input_id", None),
        invocation_result_id=kwargs.pop("invocation_result_id", None),
        validation_report_id=kwargs.pop("validation_report_id", "existing_provider_boundary_adapter_validation_report:v0.34.4"),
        status=kwargs.pop("status", ExistingProviderBoundaryAdapterStatus.ADAPTER_READY),
        readiness_level=kwargs.pop("readiness_level", ExistingProviderBoundaryReadinessLevel.CONTROLLED_EXISTING_BOUNDARY_INVOCATION_READY),
        summary=kwargs.pop("summary", "Existing provider boundary invocation report; no runtime expansion."),
        completed_items=kwargs.pop("completed_items", ["adapter policy", "invocation decision", "response envelope bridge"]),
        future_track_items=kwargs.pop("future_track_items", ["model output action quarantine", "agent step runner model integration"]),
        ready_for_v0345_model_output_action_quarantine=kwargs.pop("ready_for_v0345_model_output_action_quarantine", True),
        ready_for_v0346_agent_step_runner_model_integration=kwargs.pop("ready_for_v0346_agent_step_runner_model_integration", True),
        ready_for_controlled_existing_boundary_invocation=kwargs.pop("ready_for_controlled_existing_boundary_invocation", True),
        **kwargs,
    )


def build_existing_provider_boundary_run_preview(
    run_preview_id: str = "existing_provider_boundary_run_preview:v0.34.4",
    **kwargs: Any,
) -> ExistingProviderBoundaryRunPreview:
    return ExistingProviderBoundaryRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_existing_provider_boundary_no_direct_access_guarantee(
    guarantee_id: str = "existing_provider_boundary_no_direct_access_guarantee:v0.34.4",
    **kwargs: Any,
) -> ExistingProviderBoundaryNoDirectAccessGuarantee:
    return ExistingProviderBoundaryNoDirectAccessGuarantee(guarantee_id=guarantee_id, version=kwargs.pop("version", V0344_VERSION), **kwargs)


def build_v0344_readiness_report(report_id: str = "v0344_readiness_report", **kwargs: Any) -> V0344ReadinessReport:
    return V0344ReadinessReport(
        report_id=report_id,
        version=kwargs.pop("version", V0344_VERSION),
        adapter_id=kwargs.pop("adapter_id", "existing_provider_boundary_adapter:v0.34.4"),
        invocation_report_id=kwargs.pop("invocation_report_id", "existing_provider_boundary_invocation_report:v0.34.4"),
        invocation_result_id=kwargs.pop("invocation_result_id", None),
        validation_report_id=kwargs.pop("validation_report_id", "existing_provider_boundary_adapter_validation_report:v0.34.4"),
        summary=kwargs.pop("summary", "v0.34.4 defines controlled existing provider boundary adapter only."),
        ready_for_v0345_model_output_action_quarantine=kwargs.pop("ready_for_v0345_model_output_action_quarantine", True),
        ready_for_v0346_agent_step_runner_model_integration=kwargs.pop("ready_for_v0346_agent_step_runner_model_integration", True),
        ready_for_controlled_model_invocation=kwargs.pop("ready_for_controlled_model_invocation", True),
        ready_for_existing_boundary_invocation=kwargs.pop("ready_for_existing_boundary_invocation", True),
        ready_for_real_model_invocation=kwargs.pop("ready_for_real_model_invocation", True),
        ready_for_model_invocation=kwargs.pop("ready_for_model_invocation", True),
        completed_items=kwargs.pop("completed_items", ["adapter contract", "policy gate", "call record", "response envelope bridge"]),
        future_track_items=kwargs.pop("future_track_items", ["model output action quarantine", "agent step runner model integration"]),
        **kwargs,
    )


def validate_existing_provider_boundary_adapter_descriptor(
    adapter: ExistingProviderBoundaryAdapterDescriptor,
) -> ExistingProviderBoundaryAdapterValidationReport:
    if not isinstance(adapter, ExistingProviderBoundaryAdapterDescriptor):
        raise TypeError("adapter must be ExistingProviderBoundaryAdapterDescriptor")
    blocked_reasons: list[str] = []
    findings: list[ExistingProviderBoundaryAdapterValidationFinding] = []
    if not existing_provider_boundary_adapter_blocks_direct_access(adapter):
        blocked_reasons.append("Adapter failed direct access blocking.")
    if adapter.adapter_kind in adapter.adapter_policy.blocked_adapter_kinds:
        blocked_reasons.append("Adapter kind is blocked by policy.")
    if adapter.invocation_mode not in adapter.adapter_policy.allowed_invocation_modes:
        blocked_reasons.append("Invocation mode is not allowed by policy.")
    if adapter.callable_ref is None and _mode_allows_existing_boundary_call(adapter.invocation_mode):
        findings.append(
            build_existing_provider_boundary_adapter_validation_finding(
                "finding:callable_missing_future_gate",
                adapter_id=adapter.adapter_id,
                decision_kind=ExistingProviderBoundaryDecisionKind.FUTURE_GATE_REQUIRED,
                risk_kinds=[ExistingProviderBoundaryRiskKind.EXISTING_BOUNDARY_BYPASS_RISK],
                summary="Callable ref metadata is absent; runtime callable must still be injected explicitly.",
                future_gated=True,
            )
        )
    return build_existing_provider_boundary_adapter_validation_report(
        adapter_id=adapter.adapter_id,
        findings=findings,
        validation_passed=not blocked_reasons,
        blocked_reasons=blocked_reasons,
        ready_for_controlled_existing_boundary_invocation=not blocked_reasons and _mode_allows_existing_boundary_call(adapter.invocation_mode),
        summary="Existing provider boundary adapter validates direct-access blocks.",
    )


def decide_existing_provider_boundary_invocation(
    invocation_input: ExistingProviderBoundaryInvocationInput,
    adapter: ExistingProviderBoundaryAdapterDescriptor,
    request_envelope: ModelRequestEnvelope | None = None,
) -> ExistingProviderBoundaryInvocationDecision:
    if not isinstance(invocation_input, ExistingProviderBoundaryInvocationInput):
        raise TypeError("invocation_input must be ExistingProviderBoundaryInvocationInput")
    if not isinstance(adapter, ExistingProviderBoundaryAdapterDescriptor):
        raise TypeError("adapter must be ExistingProviderBoundaryAdapterDescriptor")
    if request_envelope is not None:
        if not isinstance(request_envelope, ModelRequestEnvelope):
            raise TypeError("request_envelope must be ModelRequestEnvelope or None")
        validate_model_request_envelope(request_envelope)
        if not model_request_envelope_is_not_invocation(request_envelope):
            return build_existing_provider_boundary_invocation_decision(
                invocation_input_id=invocation_input.invocation_input_id,
                decision_kind=ExistingProviderBoundaryDecisionKind.BLOCK,
                reason="Request envelope failed no-direct-invocation validation.",
                allowed_invocation_mode=ExistingProviderInvocationMode.BLOCKED,
                controlled_existing_boundary_invocation_allowed=False,
                risk_kinds=[ExistingProviderBoundaryRiskKind.EXISTING_BOUNDARY_BYPASS_RISK],
            )
    validation = validate_existing_provider_boundary_adapter_descriptor(adapter)
    if not validation.validation_passed:
        return build_existing_provider_boundary_invocation_decision(
            invocation_input_id=invocation_input.invocation_input_id,
            decision_kind=ExistingProviderBoundaryDecisionKind.BLOCK,
            reason="Adapter validation blocked invocation.",
            allowed_invocation_mode=ExistingProviderInvocationMode.BLOCKED,
            controlled_existing_boundary_invocation_allowed=False,
            risk_kinds=[ExistingProviderBoundaryRiskKind.EXISTING_BOUNDARY_BYPASS_RISK],
        )
    mode = ExistingProviderInvocationMode(invocation_input.invocation_mode)
    if mode == ExistingProviderInvocationMode.INJECTED_EXISTING_BOUNDARY and adapter.adapter_policy.allow_injected_existing_boundary_call:
        return build_existing_provider_boundary_invocation_decision(invocation_input_id=invocation_input.invocation_input_id)
    if mode == ExistingProviderInvocationMode.PROJECT_LOCAL_EXISTING_BOUNDARY and adapter.adapter_policy.allow_project_local_existing_boundary_call:
        return build_existing_provider_boundary_invocation_decision(
            invocation_input_id=invocation_input.invocation_input_id,
            decision_kind=ExistingProviderBoundaryDecisionKind.ALLOW_PROJECT_LOCAL_EXISTING_BOUNDARY_CALL,
            allowed_invocation_mode=ExistingProviderInvocationMode.PROJECT_LOCAL_EXISTING_BOUNDARY,
            reason="Policy allows project-local existing boundary call; direct SDK/network remains blocked.",
        )
    if mode == ExistingProviderInvocationMode.MOCK_ONLY and adapter.adapter_policy.allow_mock_call:
        return build_existing_provider_boundary_invocation_decision(
            invocation_input_id=invocation_input.invocation_input_id,
            decision_kind=ExistingProviderBoundaryDecisionKind.ALLOW_MOCK_RESPONSE,
            allowed_invocation_mode=ExistingProviderInvocationMode.MOCK_ONLY,
            controlled_existing_boundary_invocation_allowed=False,
            reason="Policy allows mock response only.",
        )
    if mode == ExistingProviderInvocationMode.SUPPLIED_OUTPUT_ONLY and adapter.adapter_policy.allow_supplied_output:
        return build_existing_provider_boundary_invocation_decision(
            invocation_input_id=invocation_input.invocation_input_id,
            decision_kind=ExistingProviderBoundaryDecisionKind.ALLOW_SUPPLIED_RESPONSE,
            allowed_invocation_mode=ExistingProviderInvocationMode.SUPPLIED_OUTPUT_ONLY,
            controlled_existing_boundary_invocation_allowed=False,
            reason="Policy allows supplied output only.",
        )
    return build_existing_provider_boundary_invocation_decision(
        invocation_input_id=invocation_input.invocation_input_id,
        decision_kind=ExistingProviderBoundaryDecisionKind.BLOCK,
        allowed_invocation_mode=ExistingProviderInvocationMode.BLOCKED,
        controlled_existing_boundary_invocation_allowed=False,
        reason="Invocation mode is not allowed by adapter policy.",
        risk_kinds=[ExistingProviderBoundaryRiskKind.EXISTING_BOUNDARY_BYPASS_RISK],
    )


def build_model_response_envelope_from_boundary_result(
    response_text: str,
    response_envelope_id: str = "model_response_envelope:existing_boundary:v0.34.4",
    **kwargs: Any,
) -> ModelResponseEnvelope:
    return build_model_response_envelope_from_supplied_text(response_text, response_envelope_id=response_envelope_id, **kwargs)


def invoke_existing_provider_boundary_adapter(
    invocation_input: ExistingProviderBoundaryInvocationInput,
    adapter: ExistingProviderBoundaryAdapterDescriptor,
    request_envelope: ModelRequestEnvelope | None = None,
    boundary_callable: BoundaryCallable | None = None,
) -> ExistingProviderBoundaryInvocationResult:
    decision = decide_existing_provider_boundary_invocation(invocation_input, adapter, request_envelope)
    if not decision.controlled_existing_boundary_invocation_allowed:
        record = build_existing_provider_boundary_call_record(
            invocation_input_id=invocation_input.invocation_input_id,
            decision_id=decision.decision_id,
            adapter_id=adapter.adapter_id,
            invocation_mode=ExistingProviderInvocationMode.BLOCKED,
            summary="Policy decision blocked existing boundary call before invocation.",
        )
        return build_existing_provider_boundary_invocation_result(
            invocation_input_id=invocation_input.invocation_input_id,
            decision_id=decision.decision_id,
            call_record_id=record.call_record_id,
            outcome_kind=ExistingProviderBoundaryOutcomeKind.BLOCKED_RESULT,
            blocked_reason=decision.reason,
            summary="Existing boundary call blocked safely before callable invocation.",
        )
    if boundary_callable is None:
        record = build_existing_provider_boundary_call_record(
            invocation_input_id=invocation_input.invocation_input_id,
            decision_id=decision.decision_id,
            adapter_id=adapter.adapter_id,
            invocation_mode=decision.allowed_invocation_mode or ExistingProviderInvocationMode.FUTURE_GATE,
            summary="No injected callable was provided; no existing boundary call performed.",
        )
        return build_existing_provider_boundary_invocation_result(
            invocation_input_id=invocation_input.invocation_input_id,
            decision_id=decision.decision_id,
            call_record_id=record.call_record_id,
            outcome_kind=ExistingProviderBoundaryOutcomeKind.NO_OP_RESULT,
            blocked_reason="No injected existing boundary callable was provided.",
            summary="Existing boundary adapter returned no-op safely.",
        )
    try:
        raw_response = boundary_callable(invocation_input)
    except Exception as exc:
        record = build_existing_provider_boundary_call_record(
            invocation_input_id=invocation_input.invocation_input_id,
            decision_id=decision.decision_id,
            adapter_id=adapter.adapter_id,
            invocation_mode=decision.allowed_invocation_mode or ExistingProviderInvocationMode.INJECTED_EXISTING_BOUNDARY,
            call_started=True,
            call_failed_safe=True,
            used_injected_callable=decision.allowed_invocation_mode == ExistingProviderInvocationMode.INJECTED_EXISTING_BOUNDARY,
            used_project_local_boundary=decision.allowed_invocation_mode == ExistingProviderInvocationMode.PROJECT_LOCAL_EXISTING_BOUNDARY,
            summary="Injected existing boundary callable raised; adapter safe-failed.",
        )
        return build_existing_provider_boundary_invocation_result(
            invocation_input_id=invocation_input.invocation_input_id,
            decision_id=decision.decision_id,
            call_record_id=record.call_record_id,
            outcome_kind=ExistingProviderBoundaryOutcomeKind.SAFE_FAIL_RESULT,
            safe_fail_reason=str(exc),
            summary="Existing boundary callable failed safely; no retry or unsafe operation performed.",
        )
    response_text = _coerce_response_text(raw_response)
    response_envelope = build_model_response_envelope_from_boundary_result(response_text)
    if response_envelope.raw_response_ref is not None:
        preview = response_envelope.raw_response_ref.raw_response_preview
        truncated = response_envelope.raw_response_ref.truncated
    else:
        preview, truncated = _bounded(response_text, DEFAULT_MAX_RAW_RESPONSE_PREVIEW_CHARS)
    record = build_existing_provider_boundary_call_record(
        invocation_input_id=invocation_input.invocation_input_id,
        decision_id=decision.decision_id,
        adapter_id=adapter.adapter_id,
        invocation_mode=decision.allowed_invocation_mode or ExistingProviderInvocationMode.INJECTED_EXISTING_BOUNDARY,
        call_started=True,
        call_completed=True,
        used_injected_callable=decision.allowed_invocation_mode == ExistingProviderInvocationMode.INJECTED_EXISTING_BOUNDARY,
        used_project_local_boundary=decision.allowed_invocation_mode == ExistingProviderInvocationMode.PROJECT_LOCAL_EXISTING_BOUNDARY,
        summary="Controlled existing boundary callable completed; output remains untrusted.",
    )
    return build_existing_provider_boundary_invocation_result(
        invocation_input_id=invocation_input.invocation_input_id,
        decision_id=decision.decision_id,
        call_record_id=record.call_record_id,
        outcome_kind=ExistingProviderBoundaryOutcomeKind.EXISTING_BOUNDARY_RESPONSE_RETURNED,
        response_text_preview=preview,
        response_char_count=len(response_text),
        response_envelope_id=response_envelope.response_envelope_id,
        sanitization_report_id=response_envelope.sanitization_policy_id,
        validation_report_id=response_envelope.validation_report_id,
        blocked_reason=None,
        redacted=response_envelope.sanitized_payload.redacted,
        truncated=truncated or response_envelope.sanitized_payload.truncated,
        ready_for_v0345_model_output_action_quarantine=True,
        summary="Existing boundary response bridged into v0.34.3 sanitizer artifact; no action execution.",
    )


def existing_provider_boundary_flags_preserve_direct_access_false(flags: ExistingProviderBoundaryAdapterFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in DIRECT_ACCESS_FALSE_FLAG_NAMES) and flags.production_certified is False


def existing_provider_boundary_adapter_blocks_direct_access(adapter: ExistingProviderBoundaryAdapterDescriptor) -> bool:
    policy = adapter.adapter_policy
    return (
        existing_provider_boundary_flags_preserve_direct_access_false(adapter.flags)
        and adapter.ready_for_direct_provider_invocation is False
        and adapter.ready_for_execution is False
        and adapter.new_provider_sdk_adapter is False
        and policy.allow_direct_provider_sdk is False
        and policy.allow_direct_network is False
        and policy.allow_credential_read is False
        and policy.allow_secret_read is False
        and policy.allow_action_execution is False
        and (adapter.callable_ref is None or adapter.callable_ref.direct_sdk is False)
    )


def existing_provider_boundary_decision_blocks_unsafe_access(decision: ExistingProviderBoundaryInvocationDecision) -> bool:
    return (
        decision.direct_provider_invocation_allowed is False
        and decision.provider_sdk_allowed is False
        and decision.direct_network_allowed is False
        and decision.credential_access_allowed is False
        and decision.secret_read_allowed is False
        and decision.tool_calls_allowed is False
        and decision.function_calls_allowed is False
        and decision.action_execution_allowed is False
    )


def existing_provider_boundary_result_is_not_action(result: ExistingProviderBoundaryInvocationResult) -> bool:
    return result.action is False and result.persistence is False and result.ready_for_action_execution is False and result.ready_for_execution is False


def v0344_readiness_report_is_not_general_execution_ready(report: V0344ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in DIRECT_ACCESS_FALSE_FLAG_NAMES) and report.general_execution_ready is False
