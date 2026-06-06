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


V0334_VERSION = "v0.33.4"
V0334_RELEASE_NAME = "v0.33.4 Safe Read-only Tool Registry"

DEFAULT_PROHIBITED_FILE_PATTERNS = [
    ".env",
    "*secret*",
    "*key*",
    "*token*",
    "*credential*",
    "*.pem",
    "id_rsa",
    "*id_rsa*",
]

DEFAULT_TOOL_PROHIBITED_ACTIONS = [
    "tool_execution",
    "tool execution",
    "read_only_tool_execution",
    "read-only tool execution",
    "workspace_inspection_execution",
    "workspace inspection execution",
    "file_read",
    "file read",
    "reference_file_access",
    "reference file access",
    "reference_code_execution",
    "reference code execution",
    "reference_import",
    "reference import",
    "dependency_install",
    "dependency install",
    "secret_file_read",
    "secret file read",
    "model_invocation",
    "model invocation",
    "provider_invocation",
    "provider invocation",
    "agent_step_execution",
    "agent step execution",
    "model_step_execution",
    "model step execution",
    "network_access",
    "network access",
    "credential_access",
    "credential access",
    "command_execution",
    "command execution",
    "workspace_write",
    "workspace write",
    "code_edit",
    "code edit",
    "patch_application",
    "patch application",
    "registry_mutation",
    "registry mutation",
    "memory_mutation",
    "memory mutation",
    "ocel_emission",
    "OCEL emission",
    "runtime_trace_persistence",
    "runtime trace persistence",
    "ui_runtime",
    "UI runtime",
    "external_control",
    "external control",
    "authority_grant",
    "authority grant",
]


class ReadOnlyToolKind(StrEnum):
    INSPECT_PROJECT_TREE_READONLY = "inspect_project_tree_readonly"
    INSPECT_FILE_METADATA_READONLY = "inspect_file_metadata_readonly"
    READ_TEXT_FILE_SAFE = "read_text_file_safe"
    SEARCH_TEXT_IN_WORKSPACE_READONLY = "search_text_in_workspace_readonly"
    SUMMARIZE_REFERENCE_INVENTORY = "summarize_reference_inventory"
    INSPECT_RECENT_OCEL_EVENTS_READONLY = "inspect_recent_ocel_events_readonly"
    INSPECT_AGENT_RUNTIME_STATE_READONLY = "inspect_agent_runtime_state_readonly"
    INSPECT_PROMPT_ASSEMBLY_OUTPUT_READONLY = "inspect_prompt_assembly_output_readonly"
    INSPECT_PROFILE_RUNTIME_READONLY = "inspect_profile_runtime_readonly"
    TEST_READONLY_TOOL = "test_readonly_tool"
    UNKNOWN = "unknown"


class ReadOnlyToolCapabilityKind(StrEnum):
    DESCRIBE_REGISTRY = "describe_registry"
    INSPECT_METADATA = "inspect_metadata"
    INSPECT_TREE = "inspect_tree"
    READ_SAFE_TEXT = "read_safe_text"
    SEARCH_SAFE_TEXT = "search_safe_text"
    SUMMARIZE_SAFE_METADATA = "summarize_safe_metadata"
    INSPECT_RUNTIME_STATE = "inspect_runtime_state"
    INSPECT_OCEL_TRACE_SUMMARY = "inspect_ocel_trace_summary"
    NO_OP = "no_op"
    BLOCK = "block"
    UNKNOWN = "unknown"


class ReadOnlyToolSurfaceKind(StrEnum):
    REGISTRY_METADATA = "registry_metadata"
    PROJECT_TREE_METADATA = "project_tree_metadata"
    FILE_METADATA = "file_metadata"
    SAFE_TEXT_FILE = "safe_text_file"
    WORKSPACE_SEARCH_INDEX = "workspace_search_index"
    REFERENCE_INVENTORY_METADATA = "reference_inventory_metadata"
    OCEL_EVENT_SUMMARY = "ocel_event_summary"
    AGENT_RUNTIME_STATE = "agent_runtime_state"
    PROMPT_ASSEMBLY_ARTIFACT = "prompt_assembly_artifact"
    PROFILE_RUNTIME_ARTIFACT = "profile_runtime_artifact"
    PROHIBITED_SECRET_FILE = "prohibited_secret_file"
    PROHIBITED_BINARY_FILE = "prohibited_binary_file"
    PROHIBITED_WORKSPACE_WRITE = "prohibited_workspace_write"
    PROHIBITED_COMMAND = "prohibited_command"
    PROHIBITED_NETWORK = "prohibited_network"
    PROHIBITED_CREDENTIAL = "prohibited_credential"
    UNKNOWN = "unknown"


class ReadOnlyToolSafetyLevel(StrEnum):
    SAFE_METADATA_ONLY = "safe_metadata_only"
    SAFE_READONLY_FUTURE_GATE = "safe_readonly_future_gate"
    REQUIRES_V0335_WORKSPACE_INSPECTION = "requires_v0335_workspace_inspection"
    REQUIRES_V0336_AGENT_STEP_RUNNER = "requires_v0336_agent_step_runner"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class ReadOnlyToolRegistryStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    REGISTRY_READY = "registry_ready"
    REGISTRY_READY_WITH_GAPS = "registry_ready_with_gaps"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class ReadOnlyToolPermissionDecisionKind(StrEnum):
    ALLOW_FUTURE_READONLY_EXECUTION = "allow_future_readonly_execution"
    ALLOW_REGISTRY_METADATA_ONLY = "allow_registry_metadata_only"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    DEFER = "defer"
    ASK_USER_REQUIRED = "ask_user_required"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class ReadOnlyToolBlockReasonKind(StrEnum):
    UNKNOWN_TOOL = "unknown_tool"
    TOOL_NOT_REGISTERED = "tool_not_registered"
    DESCRIPTOR_INVALID = "descriptor_invalid"
    NOT_READONLY = "not_readonly"
    HAS_SIDE_EFFECT_RISK = "has_side_effect_risk"
    WORKSPACE_WRITE_RISK = "workspace_write_risk"
    COMMAND_EXECUTION_RISK = "command_execution_risk"
    NETWORK_ACCESS_RISK = "network_access_risk"
    CREDENTIAL_ACCESS_RISK = "credential_access_risk"
    SECRET_FILE_RISK = "secret_file_risk"
    BINARY_FILE_RISK = "binary_file_risk"
    REFERENCE_FILE_ACCESS_NOT_ENABLED = "reference_file_access_not_enabled"
    WORKSPACE_INSPECTION_NOT_ENABLED = "workspace_inspection_not_enabled"
    AGENT_STEP_NOT_ENABLED = "agent_step_not_enabled"
    PROVIDER_INVOCATION_RISK = "provider_invocation_risk"
    REGISTRY_MUTATION_RISK = "registry_mutation_risk"
    MEMORY_MUTATION_RISK = "memory_mutation_risk"
    OCEL_EMISSION_RISK = "ocel_emission_risk"
    EXTERNAL_CONTROL_RISK = "external_control_risk"
    AUTHORITY_GRANT_RISK = "authority_grant_risk"
    UNKNOWN = "unknown"


class ReadOnlyToolSourceKind(StrEnum):
    V0330_RUNTIME_BOUNDARY = "v0330_runtime_boundary"
    V0333_SESSION_RUNTIME = "v0333_session_runtime"
    V0332_PROMPT_ASSEMBLY = "v0332_prompt_assembly"
    V0331_PROFILE_RUNTIME = "v0331_profile_runtime"
    V0329_HANDOFF_PACKET = "v0329_handoff_packet"
    REFERENCE_CONTEXT_REF = "reference_context_ref"
    OPENCODE_REFERENCE_CONTEXT_REF = "opencode_reference_context_ref"
    HERMES_REFERENCE_CONTEXT_REF = "hermes_reference_context_ref"
    OPENCLAW_REFERENCE_CONTEXT_REF = "openclaw_reference_context_ref"
    MANUAL_TOOL_DESCRIPTOR = "manual_tool_descriptor"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class ReadOnlyToolExecutionPosture(StrEnum):
    NO_EXECUTION = "no_execution"
    METADATA_ONLY = "metadata_only"
    FUTURE_READONLY_EXECUTION = "future_readonly_execution"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


RUNTIME_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_tool_execution",
    "ready_for_read_only_tool_execution",
    "ready_for_workspace_inspection_execution",
    "ready_for_file_read",
    "ready_for_reference_file_access",
    "ready_for_model_invocation",
    "ready_for_provider_invocation",
    "ready_for_agent_step_execution",
    "ready_for_model_step_execution",
    "ready_for_network_access",
    "ready_for_credential_access",
    "ready_for_command_execution",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_patch_application",
    "ready_for_registry_mutation",
    "ready_for_memory_mutation",
    "ready_for_ocel_emission",
    "ready_for_runtime_trace_persistence",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
)

PROHIBITED_SURFACES = {
    ReadOnlyToolSurfaceKind.PROHIBITED_SECRET_FILE,
    ReadOnlyToolSurfaceKind.PROHIBITED_BINARY_FILE,
    ReadOnlyToolSurfaceKind.PROHIBITED_WORKSPACE_WRITE,
    ReadOnlyToolSurfaceKind.PROHIBITED_COMMAND,
    ReadOnlyToolSurfaceKind.PROHIBITED_NETWORK,
    ReadOnlyToolSurfaceKind.PROHIBITED_CREDENTIAL,
}

SURFACE_BLOCK_REASONS = {
    ReadOnlyToolSurfaceKind.PROHIBITED_SECRET_FILE: ReadOnlyToolBlockReasonKind.SECRET_FILE_RISK,
    ReadOnlyToolSurfaceKind.PROHIBITED_BINARY_FILE: ReadOnlyToolBlockReasonKind.BINARY_FILE_RISK,
    ReadOnlyToolSurfaceKind.PROHIBITED_WORKSPACE_WRITE: ReadOnlyToolBlockReasonKind.WORKSPACE_WRITE_RISK,
    ReadOnlyToolSurfaceKind.PROHIBITED_COMMAND: ReadOnlyToolBlockReasonKind.COMMAND_EXECUTION_RISK,
    ReadOnlyToolSurfaceKind.PROHIBITED_NETWORK: ReadOnlyToolBlockReasonKind.NETWORK_ACCESS_RISK,
    ReadOnlyToolSurfaceKind.PROHIBITED_CREDENTIAL: ReadOnlyToolBlockReasonKind.CREDENTIAL_ACCESS_RISK,
}


def _validate_version_includes_v0334(version: str) -> None:
    _require_non_blank("version", version)
    if V0334_VERSION not in version:
        raise ValueError("version must include v0.33.4")


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.33.4")


def _validate_enum_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _validate_source_ref_list(values: list["ReadOnlyToolSourceRef"]) -> None:
    _validate_object_list("source_refs", values, ReadOnlyToolSourceRef)


def _validate_non_negative_int(name: str, value: int | None) -> None:
    if value is not None and (not isinstance(value, int) or value < 0):
        raise ValueError(f"{name} must be None or >= 0")


def _validate_secret_patterns(values: list[str]) -> None:
    _validate_string_list("prohibited_patterns", values)
    lowered = [value.lower() for value in values]
    for required in (".env", "secret", "key", "token", "credential", "pem", "id_rsa"):
        if not any(required in value for value in lowered):
            raise ValueError("prohibited_patterns must include secret-like defaults")


def _validate_prohibited_actions(values: list[str]) -> None:
    _validate_string_list("prohibited_actions", values)
    missing = set(DEFAULT_TOOL_PROHIBITED_ACTIONS) - set(values)
    if missing:
        raise ValueError(f"prohibited_actions missing v0.33.4 prohibitions: {sorted(missing)}")


@dataclass(frozen=True)
class ReadOnlyToolRegistryFlagSet:
    flag_set_id: str
    version: str = V0334_VERSION
    registry_metadata_constructed: bool = False
    descriptor_validation_available: bool = False
    call_proposal_validation_available: bool = False
    ready_for_v0335_workspace_inspection: bool = False
    ready_for_v0336_agent_step_runner: bool = False
    ready_for_execution: bool = False
    ready_for_tool_execution: bool = False
    ready_for_read_only_tool_execution: bool = False
    ready_for_workspace_inspection_execution: bool = False
    ready_for_file_read: bool = False
    ready_for_reference_file_access: bool = False
    ready_for_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_agent_step_execution: bool = False
    ready_for_model_step_execution: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_application: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_ocel_emission: bool = False
    ready_for_runtime_trace_persistence: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version_includes_v0334(self.version)
        _validate_false(self, RUNTIME_FLAG_NAMES)
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "tool_execution", "file_read"}):
            raise ValueError("ReadOnlyToolRegistryFlagSet is not runtime/tool/file readiness")


@dataclass(frozen=True)
class ReadOnlyToolSourceRef:
    source_ref_id: str
    source_kind: ReadOnlyToolSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        ReadOnlyToolSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"fetch", "file_read", "execution"}):
            raise ValueError("ReadOnlyToolSourceRef is not fetch, file read, or execution")

    @property
    def fetch(self) -> bool:
        return False

    @property
    def file_read(self) -> bool:
        return False

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ReadOnlyToolInputSchema:
    input_schema_id: str
    tool_kind: ReadOnlyToolKind | str
    required_fields: list[str] = field(default_factory=list)
    optional_fields: list[str] = field(default_factory=list)
    prohibited_fields: list[str] = field(default_factory=list)
    prohibited_patterns: list[str] = field(default_factory=lambda: list(DEFAULT_PROHIBITED_FILE_PATTERNS))
    max_path_depth: int | None = None
    max_result_items: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("input_schema_id", self.input_schema_id)
        ReadOnlyToolKind(self.tool_kind)
        for name in ("required_fields", "optional_fields", "prohibited_fields"):
            _validate_string_list(name, getattr(self, name))
        _validate_secret_patterns(self.prohibited_patterns)
        _validate_non_negative_int("max_path_depth", self.max_path_depth)
        _validate_non_negative_int("max_result_items", self.max_result_items)
        if _metadata_flag_true(self.metadata, {"input_execution", "file_read"}):
            raise ValueError("ReadOnlyToolInputSchema is not input execution")

    @property
    def input_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ReadOnlyToolOutputSchema:
    output_schema_id: str
    tool_kind: ReadOnlyToolKind | str
    output_fields: list[str] = field(default_factory=list)
    redacted_fields: list[str] = field(default_factory=list)
    forbidden_fields: list[str] = field(default_factory=list)
    max_output_chars: int | None = None
    raw_output_allowed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("output_schema_id", self.output_schema_id)
        ReadOnlyToolKind(self.tool_kind)
        for name in ("output_fields", "redacted_fields", "forbidden_fields"):
            _validate_string_list(name, getattr(self, name))
        _validate_non_negative_int("max_output_chars", self.max_output_chars)
        if self.raw_output_allowed is not False:
            raise ValueError("raw_output_allowed must default False")
        if _metadata_flag_true(self.metadata, {"output_persistence", "raw_output_persistence"}):
            raise ValueError("ReadOnlyToolOutputSchema is not output persistence")

    @property
    def output_persistence(self) -> bool:
        return False


@dataclass(frozen=True)
class ReadOnlyToolSafetyPolicy:
    safety_policy_id: str
    tool_kind: ReadOnlyToolKind | str
    safety_level: ReadOnlyToolSafetyLevel | str = ReadOnlyToolSafetyLevel.SAFE_METADATA_ONLY
    allowed_surfaces: list[ReadOnlyToolSurfaceKind | str] = field(default_factory=lambda: [ReadOnlyToolSurfaceKind.REGISTRY_METADATA])
    prohibited_surfaces: list[ReadOnlyToolSurfaceKind | str] = field(default_factory=lambda: list(PROHIBITED_SURFACES))
    prohibited_actions: list[str] = field(default_factory=lambda: list(DEFAULT_TOOL_PROHIBITED_ACTIONS))
    prohibited_file_patterns: list[str] = field(default_factory=lambda: list(DEFAULT_PROHIBITED_FILE_PATTERNS))
    allow_workspace_read: bool = False
    allow_reference_read: bool = False
    allow_secret_read: bool = False
    allow_binary_read: bool = False
    allow_network: bool = False
    allow_command: bool = False
    allow_write: bool = False
    allow_registry_mutation: bool = False
    allow_memory_mutation: bool = False
    requires_permission_gate: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("safety_policy_id", self.safety_policy_id)
        ReadOnlyToolKind(self.tool_kind)
        ReadOnlyToolSafetyLevel(self.safety_level)
        _validate_enum_list("allowed_surfaces", self.allowed_surfaces, ReadOnlyToolSurfaceKind)
        _validate_enum_list("prohibited_surfaces", self.prohibited_surfaces, ReadOnlyToolSurfaceKind)
        _validate_prohibited_actions(self.prohibited_actions)
        _validate_secret_patterns(self.prohibited_file_patterns)
        _validate_false(
            self,
            (
                "allow_workspace_read",
                "allow_reference_read",
                "allow_secret_read",
                "allow_binary_read",
                "allow_network",
                "allow_command",
                "allow_write",
                "allow_registry_mutation",
                "allow_memory_mutation",
            ),
        )
        if self.requires_permission_gate is not True:
            raise ValueError("requires_permission_gate should default True")
        if _metadata_flag_true(self.metadata, {"execution", "runtime_enforcement"}):
            raise ValueError("ReadOnlyToolSafetyPolicy is not execution")

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ReadOnlyToolDescriptor:
    tool_descriptor_id: str
    tool_name: str
    tool_kind: ReadOnlyToolKind | str
    capability_kinds: list[ReadOnlyToolCapabilityKind | str]
    surface_kinds: list[ReadOnlyToolSurfaceKind | str]
    input_schema: ReadOnlyToolInputSchema
    output_schema: ReadOnlyToolOutputSchema
    safety_policy: ReadOnlyToolSafetyPolicy
    source_refs: list[ReadOnlyToolSourceRef] = field(default_factory=list)
    description: str = "Read-only tool descriptor metadata only."
    execution_posture: ReadOnlyToolExecutionPosture | str = ReadOnlyToolExecutionPosture.NO_EXECUTION
    enabled_in_registry: bool = False
    executable_in_v0334: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("tool_descriptor_id", "tool_name", "description"):
            _require_non_blank(name, getattr(self, name))
        ReadOnlyToolKind(self.tool_kind)
        _validate_enum_list("capability_kinds", self.capability_kinds, ReadOnlyToolCapabilityKind)
        _validate_enum_list("surface_kinds", self.surface_kinds, ReadOnlyToolSurfaceKind)
        if not isinstance(self.input_schema, ReadOnlyToolInputSchema):
            raise TypeError("input_schema must be ReadOnlyToolInputSchema")
        if not isinstance(self.output_schema, ReadOnlyToolOutputSchema):
            raise TypeError("output_schema must be ReadOnlyToolOutputSchema")
        if not isinstance(self.safety_policy, ReadOnlyToolSafetyPolicy):
            raise TypeError("safety_policy must be ReadOnlyToolSafetyPolicy")
        _validate_source_ref_list(self.source_refs)
        ReadOnlyToolExecutionPosture(self.execution_posture)
        if self.executable_in_v0334 is not False:
            raise ValueError("executable_in_v0334 must always be False")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        prohibited = set(ReadOnlyToolSurfaceKind(value) for value in self.safety_policy.prohibited_surfaces)
        if set(ReadOnlyToolSurfaceKind(value) for value in self.surface_kinds) & prohibited:
            raise ValueError("descriptor must block prohibited surfaces")
        if _metadata_flag_true(self.metadata, {"executable_tool", "tool_execution"}):
            raise ValueError("ReadOnlyToolDescriptor is not executable tool")

    @property
    def executable_tool(self) -> bool:
        return False


@dataclass(frozen=True)
class ReadOnlyToolRegistry:
    registry_id: str
    version: str
    status: ReadOnlyToolRegistryStatus | str
    descriptors: list[ReadOnlyToolDescriptor] = field(default_factory=list)
    descriptor_ids: list[str] = field(default_factory=list)
    enabled_tool_names: list[str] = field(default_factory=list)
    disabled_tool_names: list[str] = field(default_factory=list)
    blocked_tool_names: list[str] = field(default_factory=list)
    source_refs: list[ReadOnlyToolSourceRef] = field(default_factory=list)
    registry_flags: ReadOnlyToolRegistryFlagSet = field(default_factory=lambda: ReadOnlyToolRegistryFlagSet(flag_set_id="readonly_tool_registry_flags:v0.33.4"))
    summary: str = "Safe read-only tool registry metadata only."
    gaps: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    ready_for_v0335_workspace_inspection: bool = False
    ready_for_v0336_agent_step_runner: bool = False
    ready_for_tool_execution: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("registry_id", self.registry_id)
        _validate_version_includes_v0334(self.version)
        ReadOnlyToolRegistryStatus(self.status)
        _validate_object_list("descriptors", self.descriptors, ReadOnlyToolDescriptor)
        for name in ("descriptor_ids", "enabled_tool_names", "disabled_tool_names", "blocked_tool_names", "gaps", "blocked_reasons"):
            _validate_string_list(name, getattr(self, name))
        _validate_source_ref_list(self.source_refs)
        if not isinstance(self.registry_flags, ReadOnlyToolRegistryFlagSet):
            raise TypeError("registry_flags must be ReadOnlyToolRegistryFlagSet")
        if not readonly_tool_registry_flags_preserve_runtime_false(self.registry_flags):
            raise ValueError("registry_flags must preserve runtime/tool false")
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_tool_execution", "ready_for_execution"))
        if (self.ready_for_v0335_workspace_inspection or self.ready_for_v0336_agent_step_runner) and self.blocked_reasons:
            raise ValueError("design-stage handoff readiness is not allowed with blocked_reasons")
        if _metadata_flag_true(self.metadata, {"runtime_registry", "tool_execution"}):
            raise ValueError("ReadOnlyToolRegistry is not executable runtime registry")

    @property
    def executable_runtime_registry(self) -> bool:
        return False


@dataclass(frozen=True)
class ReadOnlyToolCallProposal:
    proposal_id: str
    requested_tool_name: str
    requested_tool_kind: ReadOnlyToolKind | str
    requested_capability: ReadOnlyToolCapabilityKind | str
    requested_surface: ReadOnlyToolSurfaceKind | str
    input_preview: dict[str, Any] = field(default_factory=dict)
    request_summary: str = "Tool call proposal metadata only."
    source_refs: list[ReadOnlyToolSourceRef] = field(default_factory=list)
    ready_for_tool_execution: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("proposal_id", "requested_tool_name", "request_summary"):
            _require_non_blank(name, getattr(self, name))
        ReadOnlyToolKind(self.requested_tool_kind)
        ReadOnlyToolCapabilityKind(self.requested_capability)
        ReadOnlyToolSurfaceKind(self.requested_surface)
        if not isinstance(self.input_preview, dict):
            raise TypeError("input_preview must be dict")
        _validate_source_ref_list(self.source_refs)
        _validate_false(self, ("ready_for_tool_execution", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"invocation", "tool_execution"}):
            raise ValueError("ReadOnlyToolCallProposal is not invocation")

    @property
    def invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class ReadOnlyToolPermissionDecision:
    decision_id: str
    proposal_id: str
    requested_tool_name: str
    decision_kind: ReadOnlyToolPermissionDecisionKind | str
    reason: str
    safety_level: ReadOnlyToolSafetyLevel | str = ReadOnlyToolSafetyLevel.UNKNOWN
    block_reasons: list[ReadOnlyToolBlockReasonKind | str] = field(default_factory=list)
    allowed_only_for_future_stage: bool = False
    allowed_only_for_registry_metadata: bool = False
    execution_allowed: bool = False
    runtime_side_effect_allowed: bool = False
    ready_for_tool_execution: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("decision_id", "proposal_id", "requested_tool_name", "reason"):
            _require_non_blank(name, getattr(self, name))
        ReadOnlyToolPermissionDecisionKind(self.decision_kind)
        ReadOnlyToolSafetyLevel(self.safety_level)
        _validate_enum_list("block_reasons", self.block_reasons, ReadOnlyToolBlockReasonKind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(
            self,
            (
                "execution_allowed",
                "runtime_side_effect_allowed",
                "ready_for_tool_execution",
                "ready_for_execution",
            ),
        )
        if _metadata_flag_true(self.metadata, {"invocation", "execution_permission"}):
            raise ValueError("ReadOnlyToolPermissionDecision is not invocation")

    @property
    def invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class ReadOnlyToolBlockedAction:
    blocked_action_id: str
    proposal_id: str | None = None
    decision_id: str | None = None
    tool_name: str | None = None
    block_reasons: list[ReadOnlyToolBlockReasonKind | str] = field(default_factory=list)
    risk_surfaces: list[ReadOnlyToolSurfaceKind | str] = field(default_factory=list)
    reason: str = "Blocked read-only tool action."
    safe_alternatives: list[str] = field(default_factory=lambda: ["no-op", "defer", "ask user", "future v0.33.5 handoff"])
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("blocked_action_id", self.blocked_action_id)
        _validate_enum_list("block_reasons", self.block_reasons, ReadOnlyToolBlockReasonKind)
        _validate_enum_list("risk_surfaces", self.risk_surfaces, ReadOnlyToolSurfaceKind)
        _require_non_blank("reason", self.reason)
        _validate_string_list("safe_alternatives", self.safe_alternatives)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"remediation_execution", "tool_execution"}):
            raise ValueError("ReadOnlyToolBlockedAction does not remediate by execution")

    @property
    def safe_outcome(self) -> bool:
        return True


@dataclass(frozen=True)
class ReadOnlyToolRegistryValidationReport:
    validation_report_id: str
    registry_id: str | None = None
    descriptor_ids_checked: list[str] = field(default_factory=list)
    valid_descriptor_ids: list[str] = field(default_factory=list)
    invalid_descriptor_ids: list[str] = field(default_factory=list)
    blocked_descriptor_ids: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    blocked_actions: list[ReadOnlyToolBlockedAction] = field(default_factory=list)
    validation_passed: bool = False
    summary: str = "Read-only tool registry validation report only."
    ready_for_tool_execution: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        for name in ("descriptor_ids_checked", "valid_descriptor_ids", "invalid_descriptor_ids", "blocked_descriptor_ids", "warnings"):
            _validate_string_list(name, getattr(self, name))
        _validate_object_list("blocked_actions", self.blocked_actions, ReadOnlyToolBlockedAction)
        _require_non_blank("summary", self.summary)
        if self.validation_passed and (self.invalid_descriptor_ids or self.blocked_descriptor_ids):
            raise ValueError("validation_passed cannot be True with invalid or blocked descriptors")
        _validate_false(self, ("ready_for_tool_execution", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"runtime_certification", "tool_execution"}):
            raise ValueError("ReadOnlyToolRegistryValidationReport is not runtime certification")

    @property
    def runtime_certification(self) -> bool:
        return False


@dataclass(frozen=True)
class ReadOnlyToolRegistryReport:
    report_id: str
    version: str
    registry_id: str | None
    validation_report_id: str | None
    status: ReadOnlyToolRegistryStatus | str
    summary: str
    descriptor_count: int = 0
    enabled_descriptor_count: int = 0
    blocked_descriptor_count: int = 0
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0335_workspace_inspection: bool = False
    ready_for_v0336_agent_step_runner: bool = False
    ready_for_tool_execution: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("report_id", "version", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version_includes_v0334(self.version)
        ReadOnlyToolRegistryStatus(self.status)
        for name in ("descriptor_count", "enabled_descriptor_count", "blocked_descriptor_count"):
            _validate_non_negative_int(name, getattr(self, name))
        for name in ("completed_items", "blocked_items", "future_track_items", "gaps", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, ("ready_for_tool_execution", "ready_for_execution"))
        if (self.ready_for_v0335_workspace_inspection or self.ready_for_v0336_agent_step_runner) and self.blocked_items:
            raise ValueError("design-stage handoff readiness is not allowed with blocked_items")
        if _metadata_flag_true(self.metadata, {"tool_execution", "runtime_execution"}):
            raise ValueError("ReadOnlyToolRegistryReport is not tool execution")

    @property
    def tool_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ReadOnlyToolRegistryRunPreview:
    run_preview_id: str
    registry_id: str | None = None
    planned_steps: list[str] = field(default_factory=lambda: ["construct tool descriptors", "validate metadata"])
    expected_artifacts: list[str] = field(default_factory=lambda: ["ReadOnlyToolRegistry", "ReadOnlyToolRegistryReport"])
    explicitly_not_performed: list[str] = field(default_factory=lambda: ["tool execution", "file read", "workspace inspection", "provider invocation"])
    no_tool_execution_guarantee: bool = True
    no_read_only_tool_execution_guarantee: bool = True
    no_workspace_inspection_execution_guarantee: bool = True
    no_file_read_guarantee: bool = True
    no_reference_file_access_guarantee: bool = True
    no_model_invocation_guarantee: bool = True
    no_provider_invocation_guarantee: bool = True
    no_agent_step_execution_guarantee: bool = True
    no_network_access_guarantee: bool = True
    no_credential_access_guarantee: bool = True
    no_command_execution_guarantee: bool = True
    no_workspace_write_guarantee: bool = True
    no_code_edit_guarantee: bool = True
    no_patch_application_guarantee: bool = True
    no_registry_mutation_guarantee: bool = True
    no_memory_mutation_guarantee: bool = True
    no_ocel_emission_guarantee: bool = True
    no_runtime_trace_persistence_guarantee: bool = True
    no_ui_runtime_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.33.4")

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ReadOnlyToolRegistryNoExecutionGuarantee:
    guarantee_id: str
    version: str = V0334_VERSION
    no_tool_execution: bool = True
    no_read_only_tool_execution: bool = True
    no_workspace_inspection_execution: bool = True
    no_file_read: bool = True
    no_reference_file_access: bool = True
    no_reference_code_execution: bool = True
    no_reference_import: bool = True
    no_reference_dependency_install: bool = True
    no_secret_file_read: bool = True
    no_model_invocation: bool = True
    no_provider_invocation: bool = True
    no_agent_step_execution: bool = True
    no_network_access: bool = True
    no_credential_access: bool = True
    no_command_execution: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_patch_application: bool = True
    no_registry_mutation: bool = True
    no_memory_mutation: bool = True
    no_ocel_emission: bool = True
    no_runtime_trace_persistence: bool = True
    no_ui_runtime: bool = True
    no_external_control: bool = True
    no_authority_grant: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version_includes_v0334(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.33.4")
        _validate_string_list("evidence_refs", self.evidence_refs)


@dataclass(frozen=True)
class V0334ReadinessReport:
    report_id: str
    version: str = V0334_VERSION
    registry_id: str | None = None
    registry_report_id: str | None = None
    validation_report_id: str | None = None
    summary: str = "v0.33.4 constructs safe read-only tool registry metadata only."
    ready_for_v0335_workspace_inspection: bool = False
    ready_for_v0336_agent_step_runner: bool = False
    ready_for_execution: bool = False
    ready_for_tool_execution: bool = False
    ready_for_read_only_tool_execution: bool = False
    ready_for_workspace_inspection_execution: bool = False
    ready_for_file_read: bool = False
    ready_for_reference_file_access: bool = False
    ready_for_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_agent_step_execution: bool = False
    ready_for_model_step_execution: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_application: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_ocel_emission: bool = False
    ready_for_runtime_trace_persistence: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_TOOL_PROHIBITED_ACTIONS))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0334(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(self, RUNTIME_FLAG_NAMES)
        for name in ("completed_items", "blocked_items", "future_track_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_prohibited_actions(self.prohibited_until_later_gate)
        if (self.ready_for_v0335_workspace_inspection or self.ready_for_v0336_agent_step_runner) and self.blocked_items:
            raise ValueError("design-stage readiness is not allowed with blocked_items")
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "tool_execution", "file_read"}):
            raise ValueError("V0334ReadinessReport is not runtime enablement")

    @property
    def runtime_enablement(self) -> bool:
        return False


def build_readonly_tool_registry_flags(flag_set_id: str = "readonly_tool_registry_flags:v0.33.4", **kwargs: Any) -> ReadOnlyToolRegistryFlagSet:
    return ReadOnlyToolRegistryFlagSet(flag_set_id=flag_set_id, version=V0334_VERSION, **kwargs)


def build_readonly_tool_source_ref(source_ref_id: str, source_kind: ReadOnlyToolSourceKind | str = ReadOnlyToolSourceKind.MANUAL_TOOL_DESCRIPTOR, source_id: str = "manual_tool_descriptor", source_summary: str = "Provided in-memory tool registry metadata.", **kwargs: Any) -> ReadOnlyToolSourceRef:
    return ReadOnlyToolSourceRef(source_ref_id=source_ref_id, source_kind=source_kind, source_id=source_id, source_summary=source_summary, **kwargs)


def build_readonly_tool_input_schema(input_schema_id: str, tool_kind: ReadOnlyToolKind | str = ReadOnlyToolKind.TEST_READONLY_TOOL, **kwargs: Any) -> ReadOnlyToolInputSchema:
    return ReadOnlyToolInputSchema(input_schema_id=input_schema_id, tool_kind=tool_kind, **kwargs)


def build_readonly_tool_output_schema(output_schema_id: str, tool_kind: ReadOnlyToolKind | str = ReadOnlyToolKind.TEST_READONLY_TOOL, **kwargs: Any) -> ReadOnlyToolOutputSchema:
    return ReadOnlyToolOutputSchema(output_schema_id=output_schema_id, tool_kind=tool_kind, **kwargs)


def build_readonly_tool_safety_policy(safety_policy_id: str, tool_kind: ReadOnlyToolKind | str = ReadOnlyToolKind.TEST_READONLY_TOOL, **kwargs: Any) -> ReadOnlyToolSafetyPolicy:
    return ReadOnlyToolSafetyPolicy(safety_policy_id=safety_policy_id, tool_kind=tool_kind, **kwargs)


def build_readonly_tool_descriptor(tool_descriptor_id: str, tool_name: str, tool_kind: ReadOnlyToolKind | str = ReadOnlyToolKind.TEST_READONLY_TOOL, **kwargs: Any) -> ReadOnlyToolDescriptor:
    input_schema = kwargs.pop("input_schema", build_readonly_tool_input_schema(f"{tool_descriptor_id}:input", tool_kind))
    output_schema = kwargs.pop("output_schema", build_readonly_tool_output_schema(f"{tool_descriptor_id}:output", tool_kind))
    safety_policy = kwargs.pop("safety_policy", build_readonly_tool_safety_policy(f"{tool_descriptor_id}:policy", tool_kind))
    return ReadOnlyToolDescriptor(
        tool_descriptor_id=tool_descriptor_id,
        tool_name=tool_name,
        tool_kind=tool_kind,
        capability_kinds=kwargs.pop("capability_kinds", [ReadOnlyToolCapabilityKind.INSPECT_METADATA]),
        surface_kinds=kwargs.pop("surface_kinds", [ReadOnlyToolSurfaceKind.REGISTRY_METADATA]),
        input_schema=input_schema,
        output_schema=output_schema,
        safety_policy=safety_policy,
        **kwargs,
    )


def build_readonly_tool_registry(registry_id: str = "readonly_tool_registry:v0.33.4", **kwargs: Any) -> ReadOnlyToolRegistry:
    descriptors = kwargs.pop("descriptors", [])
    return ReadOnlyToolRegistry(
        registry_id=registry_id,
        version=V0334_VERSION,
        status=kwargs.pop("status", ReadOnlyToolRegistryStatus.REGISTRY_READY_WITH_GAPS),
        descriptors=descriptors,
        descriptor_ids=kwargs.pop("descriptor_ids", [descriptor.tool_descriptor_id for descriptor in descriptors]),
        enabled_tool_names=kwargs.pop("enabled_tool_names", [descriptor.tool_name for descriptor in descriptors if descriptor.enabled_in_registry]),
        disabled_tool_names=kwargs.pop("disabled_tool_names", [descriptor.tool_name for descriptor in descriptors if not descriptor.enabled_in_registry]),
        registry_flags=kwargs.pop("registry_flags", build_readonly_tool_registry_flags(registry_metadata_constructed=True, descriptor_validation_available=True, call_proposal_validation_available=True)),
        **kwargs,
    )


def build_readonly_tool_call_proposal(proposal_id: str, requested_tool_name: str, **kwargs: Any) -> ReadOnlyToolCallProposal:
    return ReadOnlyToolCallProposal(
        proposal_id=proposal_id,
        requested_tool_name=requested_tool_name,
        requested_tool_kind=kwargs.pop("requested_tool_kind", ReadOnlyToolKind.TEST_READONLY_TOOL),
        requested_capability=kwargs.pop("requested_capability", ReadOnlyToolCapabilityKind.INSPECT_METADATA),
        requested_surface=kwargs.pop("requested_surface", ReadOnlyToolSurfaceKind.REGISTRY_METADATA),
        **kwargs,
    )


def build_readonly_tool_permission_decision(decision_id: str, proposal_id: str, requested_tool_name: str, **kwargs: Any) -> ReadOnlyToolPermissionDecision:
    return ReadOnlyToolPermissionDecision(
        decision_id=decision_id,
        proposal_id=proposal_id,
        requested_tool_name=requested_tool_name,
        decision_kind=kwargs.pop("decision_kind", ReadOnlyToolPermissionDecisionKind.ALLOW_REGISTRY_METADATA_ONLY),
        reason=kwargs.pop("reason", "Allowed for registry metadata only; no execution."),
        **kwargs,
    )


def build_readonly_tool_blocked_action(blocked_action_id: str, **kwargs: Any) -> ReadOnlyToolBlockedAction:
    return ReadOnlyToolBlockedAction(blocked_action_id=blocked_action_id, **kwargs)


def build_readonly_tool_registry_validation_report(validation_report_id: str, **kwargs: Any) -> ReadOnlyToolRegistryValidationReport:
    return ReadOnlyToolRegistryValidationReport(validation_report_id=validation_report_id, **kwargs)


def build_readonly_tool_registry_report(report_id: str, **kwargs: Any) -> ReadOnlyToolRegistryReport:
    return ReadOnlyToolRegistryReport(
        report_id=report_id,
        version=V0334_VERSION,
        registry_id=kwargs.pop("registry_id", None),
        validation_report_id=kwargs.pop("validation_report_id", None),
        status=kwargs.pop("status", ReadOnlyToolRegistryStatus.REGISTRY_READY_WITH_GAPS),
        summary=kwargs.pop("summary", "Read-only tool registry report is not tool execution."),
        **kwargs,
    )


def build_readonly_tool_registry_run_preview(run_preview_id: str, **kwargs: Any) -> ReadOnlyToolRegistryRunPreview:
    return ReadOnlyToolRegistryRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_readonly_tool_registry_no_execution_guarantee(guarantee_id: str = "readonly_tool_registry_no_execution:v0.33.4", **kwargs: Any) -> ReadOnlyToolRegistryNoExecutionGuarantee:
    return ReadOnlyToolRegistryNoExecutionGuarantee(guarantee_id=guarantee_id, version=V0334_VERSION, **kwargs)


def build_v0334_readiness_report(report_id: str = "v0334_readiness_report", **kwargs: Any) -> V0334ReadinessReport:
    return V0334ReadinessReport(report_id=report_id, version=V0334_VERSION, **kwargs)


def default_safe_readonly_tool_descriptors() -> list[ReadOnlyToolDescriptor]:
    return [
        build_readonly_tool_descriptor(
            "descriptor:registry",
            "describe_registry",
            ReadOnlyToolKind.TEST_READONLY_TOOL,
            capability_kinds=[ReadOnlyToolCapabilityKind.DESCRIBE_REGISTRY],
            surface_kinds=[ReadOnlyToolSurfaceKind.REGISTRY_METADATA],
            execution_posture=ReadOnlyToolExecutionPosture.METADATA_ONLY,
            enabled_in_registry=True,
        ),
        build_readonly_tool_descriptor(
            "descriptor:runtime_state",
            "inspect_agent_runtime_state_readonly",
            ReadOnlyToolKind.INSPECT_AGENT_RUNTIME_STATE_READONLY,
            capability_kinds=[ReadOnlyToolCapabilityKind.INSPECT_RUNTIME_STATE],
            surface_kinds=[ReadOnlyToolSurfaceKind.AGENT_RUNTIME_STATE],
            execution_posture=ReadOnlyToolExecutionPosture.METADATA_ONLY,
            enabled_in_registry=True,
        ),
        build_readonly_tool_descriptor(
            "descriptor:prompt_output",
            "inspect_prompt_assembly_output_readonly",
            ReadOnlyToolKind.INSPECT_PROMPT_ASSEMBLY_OUTPUT_READONLY,
            capability_kinds=[ReadOnlyToolCapabilityKind.INSPECT_METADATA],
            surface_kinds=[ReadOnlyToolSurfaceKind.PROMPT_ASSEMBLY_ARTIFACT],
            execution_posture=ReadOnlyToolExecutionPosture.METADATA_ONLY,
            enabled_in_registry=True,
        ),
    ]


def validate_readonly_tool_descriptor(descriptor: ReadOnlyToolDescriptor) -> ReadOnlyToolRegistryValidationReport:
    if not isinstance(descriptor, ReadOnlyToolDescriptor):
        raise TypeError("descriptor must be ReadOnlyToolDescriptor")
    blocked: list[ReadOnlyToolBlockedAction] = []
    invalid_ids: list[str] = []
    blocked_ids: list[str] = []
    if descriptor.executable_in_v0334 or descriptor.ready_for_execution or descriptor.executable_tool:
        invalid_ids.append(descriptor.tool_descriptor_id)
    surfaces = set(ReadOnlyToolSurfaceKind(value) for value in descriptor.surface_kinds)
    if surfaces & PROHIBITED_SURFACES:
        blocked_ids.append(descriptor.tool_descriptor_id)
        blocked.append(
            build_readonly_tool_blocked_action(
                f"{descriptor.tool_descriptor_id}:blocked",
                tool_name=descriptor.tool_name,
                block_reasons=[SURFACE_BLOCK_REASONS[next(iter(surfaces & PROHIBITED_SURFACES))]],
                risk_surfaces=list(surfaces & PROHIBITED_SURFACES),
                reason="Descriptor includes prohibited surface.",
            )
        )
    return build_readonly_tool_registry_validation_report(
        f"{descriptor.tool_descriptor_id}:validation",
        descriptor_ids_checked=[descriptor.tool_descriptor_id],
        valid_descriptor_ids=[] if invalid_ids or blocked_ids else [descriptor.tool_descriptor_id],
        invalid_descriptor_ids=invalid_ids,
        blocked_descriptor_ids=blocked_ids,
        blocked_actions=blocked,
        validation_passed=not invalid_ids and not blocked_ids,
        ready_for_tool_execution=False,
        ready_for_execution=False,
    )


def validate_readonly_tool_registry(registry: ReadOnlyToolRegistry) -> ReadOnlyToolRegistryValidationReport:
    if not isinstance(registry, ReadOnlyToolRegistry):
        raise TypeError("registry must be ReadOnlyToolRegistry")
    checked: list[str] = []
    valid: list[str] = []
    invalid: list[str] = []
    blocked: list[str] = []
    actions: list[ReadOnlyToolBlockedAction] = []
    for descriptor in registry.descriptors:
        report = validate_readonly_tool_descriptor(descriptor)
        checked.extend(report.descriptor_ids_checked)
        valid.extend(report.valid_descriptor_ids)
        invalid.extend(report.invalid_descriptor_ids)
        blocked.extend(report.blocked_descriptor_ids)
        actions.extend(report.blocked_actions)
    return build_readonly_tool_registry_validation_report(
        f"{registry.registry_id}:validation",
        registry_id=registry.registry_id,
        descriptor_ids_checked=checked,
        valid_descriptor_ids=valid,
        invalid_descriptor_ids=invalid,
        blocked_descriptor_ids=blocked,
        blocked_actions=actions,
        validation_passed=not invalid and not blocked,
        summary="Registry validation is metadata validation only, not runtime certification.",
    )


def evaluate_readonly_tool_call_proposal(registry: ReadOnlyToolRegistry, proposal: ReadOnlyToolCallProposal) -> ReadOnlyToolPermissionDecision:
    if not isinstance(registry, ReadOnlyToolRegistry):
        raise TypeError("registry must be ReadOnlyToolRegistry")
    if not isinstance(proposal, ReadOnlyToolCallProposal):
        raise TypeError("proposal must be ReadOnlyToolCallProposal")
    descriptors = {descriptor.tool_name: descriptor for descriptor in registry.descriptors}
    descriptor = descriptors.get(proposal.requested_tool_name)
    if descriptor is None:
        return build_readonly_tool_permission_decision(
            f"{proposal.proposal_id}:decision",
            proposal.proposal_id,
            proposal.requested_tool_name,
            decision_kind=ReadOnlyToolPermissionDecisionKind.BLOCK,
            reason="Tool is not registered in v0.33.4 registry metadata.",
            safety_level=ReadOnlyToolSafetyLevel.BLOCKED,
            block_reasons=[ReadOnlyToolBlockReasonKind.TOOL_NOT_REGISTERED],
        )
    if ReadOnlyToolSurfaceKind(proposal.requested_surface) in PROHIBITED_SURFACES:
        return build_readonly_tool_permission_decision(
            f"{proposal.proposal_id}:decision",
            proposal.proposal_id,
            proposal.requested_tool_name,
            decision_kind=ReadOnlyToolPermissionDecisionKind.BLOCK,
            reason="Requested surface is prohibited and remains non-executable.",
            safety_level=ReadOnlyToolSafetyLevel.BLOCKED,
            block_reasons=[SURFACE_BLOCK_REASONS[ReadOnlyToolSurfaceKind(proposal.requested_surface)]],
        )
    if not descriptor.enabled_in_registry:
        return build_readonly_tool_permission_decision(
            f"{proposal.proposal_id}:decision",
            proposal.proposal_id,
            proposal.requested_tool_name,
            decision_kind=ReadOnlyToolPermissionDecisionKind.DENY,
            reason="Tool descriptor is metadata-only but disabled in registry.",
            safety_level=descriptor.safety_policy.safety_level,
            block_reasons=[ReadOnlyToolBlockReasonKind.TOOL_NOT_REGISTERED],
        )
    if descriptor.execution_posture == ReadOnlyToolExecutionPosture.METADATA_ONLY:
        return build_readonly_tool_permission_decision(
            f"{proposal.proposal_id}:decision",
            proposal.proposal_id,
            proposal.requested_tool_name,
            decision_kind=ReadOnlyToolPermissionDecisionKind.ALLOW_REGISTRY_METADATA_ONLY,
            reason="Allowed for registry metadata only; no tool execution in v0.33.4.",
            safety_level=descriptor.safety_policy.safety_level,
            allowed_only_for_registry_metadata=True,
        )
    return build_readonly_tool_permission_decision(
        f"{proposal.proposal_id}:decision",
        proposal.proposal_id,
        proposal.requested_tool_name,
        decision_kind=ReadOnlyToolPermissionDecisionKind.ALLOW_FUTURE_READONLY_EXECUTION,
        reason="Eligible only for future v0.33.5/v0.33.6 gate; no execution in v0.33.4.",
        safety_level=descriptor.safety_policy.safety_level,
        allowed_only_for_future_stage=True,
    )


def readonly_tool_registry_flags_preserve_runtime_false(flags: ReadOnlyToolRegistryFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in RUNTIME_FLAG_NAMES)


def readonly_tool_descriptor_is_not_executable(descriptor: ReadOnlyToolDescriptor) -> bool:
    return descriptor.executable_in_v0334 is False and descriptor.ready_for_execution is False and descriptor.executable_tool is False


def readonly_tool_decision_is_not_invocation(decision: ReadOnlyToolPermissionDecision) -> bool:
    return (
        decision.execution_allowed is False
        and decision.runtime_side_effect_allowed is False
        and decision.ready_for_tool_execution is False
        and decision.ready_for_execution is False
        and decision.invocation is False
    )


def readonly_tool_registry_is_not_runtime_registry(registry: ReadOnlyToolRegistry) -> bool:
    return registry.ready_for_tool_execution is False and registry.ready_for_execution is False and registry.executable_runtime_registry is False


def v0334_readiness_report_is_not_runtime_ready(report: V0334ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in RUNTIME_FLAG_NAMES) and report.runtime_enablement is False
