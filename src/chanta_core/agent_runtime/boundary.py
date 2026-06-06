from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


V0330_VERSION = "v0.33.0"
V0330_RELEASE_NAME = "v0.33.0 Internal Runtime Boundary & Permission Gate"
V0330_TRACK = "Internal General Agent Runtime MVP"

DEFAULT_FUTURE_TRACK_LEVELS = ["D4", "D5", "D6", "D7", "D8", "D9"]

DEFAULT_V033_STAGES = [
    "boundary_permission_gate",
    "agent_profile_runtime",
    "prompt_assembly_pipeline",
    "session_runtime_turn_state_machine",
    "safe_readonly_tool_registry",
    "safe_workspace_inspection",
    "agent_step_runner",
    "runtime_ocel_trace_emitter",
    "cli_agent_run_surface",
    "consolidation",
]

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

DEFAULT_V0330_PROHIBITED_RUNTIME_ACTIONS = [
    "external_harness_execution",
    "external harness execution",
    "OpenCode_execution",
    "OpenCode execution",
    "Hermes_execution",
    "Hermes execution",
    "OpenClaw_execution",
    "OpenClaw execution",
    "reference_code_execution",
    "reference code execution",
    "reference_import",
    "reference import",
    "dependency_install",
    "dependency install",
    "live_scan",
    "live scan",
    "source_ref_fetch",
    "source_ref fetch",
    "secret_file_read",
    "secret file read",
    "read_only_tool_execution",
    "read-only tool execution",
    "workspace_inspection_execution",
    "workspace inspection execution",
    "agent_step_execution",
    "agent step execution",
    "provider_invocation",
    "provider invocation",
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
    "browser_runtime_control",
    "browser",
    "rpa_runtime_control",
    "RPA",
    "gateway_control",
    "gateway",
    "packet_send",
    "packet send",
    "registry_mutation",
    "registry mutation",
    "memory_mutation",
    "memory mutation",
    "ocel_emission",
    "OCEL emission",
    "ui_runtime",
    "UI runtime",
    "external_control",
    "external control",
    "authority_grant",
    "authority grant",
    "D4_D9_grant",
    "D4-D9 grant",
]


class InternalRuntimeTrackKind(StrEnum):
    BOUNDARY_PERMISSION_GATE = "boundary_permission_gate"
    AGENT_PROFILE_RUNTIME = "agent_profile_runtime"
    PROMPT_ASSEMBLY_PIPELINE = "prompt_assembly_pipeline"
    SESSION_RUNTIME_TURN_STATE_MACHINE = "session_runtime_turn_state_machine"
    SAFE_READONLY_TOOL_REGISTRY = "safe_readonly_tool_registry"
    SAFE_WORKSPACE_INSPECTION = "safe_workspace_inspection"
    AGENT_STEP_RUNNER = "agent_step_runner"
    RUNTIME_OCEL_TRACE_EMITTER = "runtime_ocel_trace_emitter"
    CLI_AGENT_RUN_SURFACE = "cli_agent_run_surface"
    CONSOLIDATION = "consolidation"
    UNKNOWN = "unknown"


class InternalRuntimeSurfaceKind(StrEnum):
    INTERNAL_PROFILE_RESOLUTION = "internal_profile_resolution"
    PROMPT_ASSEMBLY = "prompt_assembly"
    SESSION_STATE_MACHINE = "session_state_machine"
    READ_ONLY_TOOL_REGISTRY = "read_only_tool_registry"
    SAFE_WORKSPACE_INSPECTION = "safe_workspace_inspection"
    MODEL_STEP_BOUNDARY = "model_step_boundary"
    AGENT_ACTION_PROPOSAL = "agent_action_proposal"
    PERMISSION_GATE = "permission_gate"
    INTERNAL_OCEL_TRACE = "internal_ocel_trace"
    CLI_SURFACE = "cli_surface"
    REFERENCE_CORPUS_CONTEXT = "reference_corpus_context"
    EXTERNAL_HARNESS_CONTEXT = "external_harness_context"
    PROVIDER_BOUNDARY = "provider_boundary"
    WORKSPACE_WRITE = "workspace_write"
    CODE_EDIT = "code_edit"
    PATCH_APPLICATION = "patch_application"
    SHELL_COMMAND = "shell_command"
    NETWORK = "network"
    CREDENTIAL = "credential"
    BROWSER = "browser"
    RPA = "rpa"
    GATEWAY = "gateway"
    EXTERNAL_CONTROL = "external_control"
    AUTHORITY_GRANT = "authority_grant"
    UNKNOWN = "unknown"


class InternalRuntimeCapabilityKind(StrEnum):
    RESOLVE_AGENT_PROFILE = "resolve_agent_profile"
    ASSEMBLE_PROMPT = "assemble_prompt"
    CREATE_SESSION = "create_session"
    TRANSITION_TURN_STATE = "transition_turn_state"
    PROPOSE_ACTION = "propose_action"
    EVALUATE_PERMISSION = "evaluate_permission"
    DENY_ACTION = "deny_action"
    BLOCK_ACTION = "block_action"
    NO_OP = "no_op"
    ASK_USER = "ask_user"
    INSPECT_TOOL_REGISTRY_READONLY = "inspect_tool_registry_readonly"
    INSPECT_WORKSPACE_READONLY = "inspect_workspace_readonly"
    READ_TEXT_FILE_SAFE = "read_text_file_safe"
    SEARCH_WORKSPACE_READONLY = "search_workspace_readonly"
    CALL_MODEL_VIA_EXISTING_BOUNDARY = "call_model_via_existing_boundary"
    EMIT_INTERNAL_OCEL_TRACE = "emit_internal_ocel_trace"
    RUN_CLI_AGENT_SURFACE = "run_cli_agent_surface"
    EXECUTE_EXTERNAL_HARNESS = "execute_external_harness"
    EXECUTE_REFERENCE_CODE = "execute_reference_code"
    RUN_SHELL_COMMAND = "run_shell_command"
    WRITE_WORKSPACE = "write_workspace"
    EDIT_CODE = "edit_code"
    APPLY_PATCH = "apply_patch"
    INSTALL_DEPENDENCY = "install_dependency"
    INVOKE_PROVIDER = "invoke_provider"
    ACCESS_NETWORK = "access_network"
    ACCESS_CREDENTIAL = "access_credential"
    CONTROL_BROWSER = "control_browser"
    CONTROL_RPA = "control_rpa"
    CONTROL_GATEWAY = "control_gateway"
    GRANT_AUTHORITY = "grant_authority"
    UNKNOWN = "unknown"


class InternalRuntimeActionKind(StrEnum):
    ALLOW_DESIGN_STAGE_HANDOFF = "allow_design_stage_handoff"
    ALLOW_INTERNAL_BOUNDARY_DEFINITION = "allow_internal_boundary_definition"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    DEFER = "defer"
    ASK_USER = "ask_user"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE = "future_gate"
    UNKNOWN = "unknown"


class InternalRuntimeRiskSurfaceKind(StrEnum):
    EXTERNAL_HARNESS_EXECUTION = "external_harness_execution"
    REFERENCE_CODE_EXECUTION = "reference_code_execution"
    LIVE_SCAN = "live_scan"
    SOURCE_REF_FETCH = "source_ref_fetch"
    SECRET_FILE_READ = "secret_file_read"
    DEPENDENCY_INSTALL = "dependency_install"
    RUNTIME_IMPORT = "runtime_import"
    SHELL_SUBPROCESS = "shell_subprocess"
    WORKSPACE_WRITE = "workspace_write"
    CODE_EDIT = "code_edit"
    PATCH_APPLICATION = "patch_application"
    PROVIDER_INVOCATION = "provider_invocation"
    NETWORK_ACCESS = "network_access"
    CREDENTIAL_ACCESS = "credential_access"
    BROWSER_RUNTIME_CONTROL = "browser_runtime_control"
    RPA_RUNTIME_CONTROL = "rpa_runtime_control"
    GATEWAY_CONTROL = "gateway_control"
    PACKET_SEND = "packet_send"
    REGISTRY_MUTATION = "registry_mutation"
    MEMORY_MUTATION = "memory_mutation"
    OCEL_EMISSION = "ocel_emission"
    RUNTIME_TRACE_PERSISTENCE = "runtime_trace_persistence"
    UI_RUNTIME = "ui_runtime"
    EXTERNAL_CONTROL = "external_control"
    AUTHORITY_GRANT = "authority_grant"
    D4_D9_GRANT = "d4_d9_grant"
    RAW_OUTPUT_PERSISTENCE = "raw_output_persistence"
    UNKNOWN = "unknown"


class InternalRuntimePermissionDecisionKind(StrEnum):
    ALLOWED_DESIGN_STAGE_ONLY = "allowed_design_stage_only"
    ALLOWED_BOUNDARY_DEFINITION_ONLY = "allowed_boundary_definition_only"
    DENIED = "denied"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    ASK_USER_REQUIRED = "ask_user_required"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class InternalRuntimeBoundaryStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    BOUNDARY_READY = "boundary_ready"
    BOUNDARY_READY_WITH_GAPS = "boundary_ready_with_gaps"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class InternalRuntimeReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    BOUNDARY_CONTRACT_READY = "boundary_contract_ready"
    DESIGN_HANDOFF_READY_FOR_V0331 = "design_handoff_ready_for_v0331"
    DESIGN_HANDOFF_READY_FOR_V0332 = "design_handoff_ready_for_v0332"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class InternalRuntimeReferenceCorpusPosture(StrEnum):
    NO_REFERENCE_CONTEXT = "no_reference_context"
    PATH_REFERENCE_ONLY = "path_reference_only"
    STATIC_METADATA_ONLY = "static_metadata_only"
    SAFE_INVENTORY_FUTURE_GATE = "safe_inventory_future_gate"
    READ_ONLY_INSPECTION_FUTURE_GATE = "read_only_inspection_future_gate"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


def _require_non_blank(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must not be blank")


def _validate_string_list(name: str, values: list[str]) -> None:
    if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
        raise TypeError(f"{name} must be list[str]")


def _validate_object_list(name: str, values: list[Any], expected_type: type) -> None:
    if not isinstance(values, list) or not all(isinstance(item, expected_type) for item in values):
        raise TypeError(f"{name} must be list[{expected_type.__name__}]")


def _validate_version_includes_v0330(version: str) -> None:
    _require_non_blank("version", version)
    if V0330_VERSION not in version:
        raise ValueError("version must include v0.33.0")


def _metadata_flag_true(metadata: dict[str, Any], names: set[str]) -> bool:
    return isinstance(metadata, dict) and any(metadata.get(name) is True for name in names)


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.33.0")


def _validate_true(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not True:
            raise ValueError(f"{name} must always be True in v0.33.0")


def _validate_level_not_d4_d9(level: str | None) -> None:
    if level is None:
        return
    _require_non_blank("max_grantable_level", level)
    normalized = level.strip().upper()
    if any(normalized.startswith(disallowed) for disallowed in DEFAULT_FUTURE_TRACK_LEVELS):
        raise ValueError("D4-D9 must remain future-track and cannot be max grantable in v0.33.0")


def _validate_future_track_levels(values: list[str]) -> None:
    _validate_string_list("future_track_levels", values)
    missing = set(DEFAULT_FUTURE_TRACK_LEVELS) - set(values)
    if missing:
        raise ValueError(f"future_track_levels must include D4-D9: {sorted(missing)}")


def _validate_prohibited_runtime_actions(name: str, values: list[str]) -> None:
    _validate_string_list(name, values)
    missing = set(DEFAULT_V0330_PROHIBITED_RUNTIME_ACTIONS) - set(values)
    if missing:
        raise ValueError(f"{name} missing v0.33.0 prohibitions: {sorted(missing)}")


def _validate_secret_patterns(values: list[str]) -> None:
    _validate_string_list("prohibited_file_patterns", values)
    lowered = [value.lower() for value in values]
    for required in (".env", "secret", "key", "token", "credential", "pem", "id_rsa"):
        if not any(required in value for value in lowered):
            raise ValueError("prohibited_file_patterns must include secret-like defaults")


def _validate_roadmap_stages(values: list[InternalRuntimeTrackKind | str]) -> None:
    if not isinstance(values, list):
        raise TypeError("stages must be list")
    normalized = [InternalRuntimeTrackKind(value).value for value in values]
    missing = set(DEFAULT_V033_STAGES) - set(normalized)
    if missing:
        raise ValueError(f"stages must include v0.33.0-v0.33.9 roadmap concepts: {sorted(missing)}")


RUNTIME_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_external_harness_execution",
    "ready_for_reference_code_execution",
    "ready_for_live_scan",
    "ready_for_read_only_tool_execution",
    "ready_for_workspace_inspection_execution",
    "ready_for_agent_step_execution",
    "ready_for_provider_invocation",
    "ready_for_network_access",
    "ready_for_credential_access",
    "ready_for_command_execution",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_patch_application",
    "ready_for_browser_runtime_control",
    "ready_for_rpa_runtime_control",
    "ready_for_gateway_control",
    "ready_for_packet_send",
    "ready_for_registry_mutation",
    "ready_for_memory_mutation",
    "ready_for_ocel_emission",
    "ready_for_runtime_trace_persistence",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
)

REFERENCE_RUNTIME_FLAG_NAMES = (
    "ready_for_reference_code_execution",
    "ready_for_reference_import",
    "ready_for_reference_dependency_install",
    "ready_for_reference_test_execution",
    "ready_for_reference_readonly_inspection",
)


@dataclass(frozen=True)
class InternalRuntimeCapabilityFlagSet:
    flag_set_id: str
    version: str = V0330_VERSION
    ready_for_v0331_agent_profile_runtime: bool = False
    ready_for_v0332_prompt_assembly: bool = False
    ready_for_execution: bool = False
    ready_for_external_harness_execution: bool = False
    ready_for_reference_code_execution: bool = False
    ready_for_live_scan: bool = False
    ready_for_read_only_tool_execution: bool = False
    ready_for_workspace_inspection_execution: bool = False
    ready_for_agent_step_execution: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_application: bool = False
    ready_for_browser_runtime_control: bool = False
    ready_for_rpa_runtime_control: bool = False
    ready_for_gateway_control: bool = False
    ready_for_packet_send: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_ocel_emission: bool = False
    ready_for_runtime_trace_persistence: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    live_adapter_certified: bool = False
    max_grantable_level: str | None = None
    future_track_levels: list[str] = field(default_factory=lambda: list(DEFAULT_FUTURE_TRACK_LEVELS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version_includes_v0330(self.version)
        _validate_false(self, RUNTIME_FLAG_NAMES)
        _validate_false(self, ("production_certified", "live_adapter_certified"))
        _validate_level_not_d4_d9(self.max_grantable_level)
        _validate_future_track_levels(self.future_track_levels)
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "production_release", "live_adapter"}):
            raise ValueError("InternalRuntimeCapabilityFlagSet is not runtime enablement")


@dataclass(frozen=True)
class InternalRuntimeAllowedSurface:
    allowed_surface_id: str
    surface_kind: InternalRuntimeSurfaceKind | str
    capability_kind: InternalRuntimeCapabilityKind | str
    description: str
    allowed_only_for_design_stage: bool = True
    allowed_only_for_boundary_definition: bool = True
    executable_in_v0330: bool = False
    requires_permission_gate: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("allowed_surface_id", self.allowed_surface_id)
        InternalRuntimeSurfaceKind(self.surface_kind)
        InternalRuntimeCapabilityKind(self.capability_kind)
        _require_non_blank("description", self.description)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.executable_in_v0330 is not False:
            raise ValueError("executable_in_v0330 must always be False")
        if _metadata_flag_true(self.metadata, {"runtime_execution", "executable_surface"}):
            raise ValueError("InternalRuntimeAllowedSurface is not runtime execution")

    @property
    def runtime_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalRuntimeProhibitedSurface:
    prohibited_surface_id: str
    surface_kind: InternalRuntimeSurfaceKind | str
    risk_surface: InternalRuntimeRiskSurfaceKind | str
    capability_kind: InternalRuntimeCapabilityKind | str
    reason: str
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_V0330_PROHIBITED_RUNTIME_ACTIONS))
    blocks_execution: bool = True
    blocks_runtime_readiness: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("prohibited_surface_id", self.prohibited_surface_id)
        InternalRuntimeSurfaceKind(self.surface_kind)
        InternalRuntimeRiskSurfaceKind(self.risk_surface)
        InternalRuntimeCapabilityKind(self.capability_kind)
        _require_non_blank("reason", self.reason)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.blocks_execution is not True:
            raise ValueError("blocks_execution must default True in v0.33.0")
        if self.blocks_runtime_readiness is not True:
            raise ValueError("blocks_runtime_readiness must default True in v0.33.0")
        if _metadata_flag_true(self.metadata, {"runtime_enforcement", "permission"}):
            raise ValueError("InternalRuntimeProhibitedSurface is gate metadata, not runtime enforcement")

    @property
    def runtime_enforcement(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalRuntimeReferenceCorpusBoundary:
    reference_boundary_id: str
    version: str = V0330_VERSION
    references_root_path_ref: str | None = "references/"
    known_reference_path_refs: list[str] = field(default_factory=lambda: ["references/OpenCode", "references/Hermes"])
    open_code_reference_path_ref: str | None = "references/OpenCode"
    hermes_reference_path_ref: str | None = "references/Hermes"
    openclaw_reference_path_ref: str | None = "references/OpenClaw"
    posture: InternalRuntimeReferenceCorpusPosture | str = InternalRuntimeReferenceCorpusPosture.PATH_REFERENCE_ONLY
    allowed_reference_uses: list[str] = field(default_factory=lambda: ["path refs", "prior v0.32 static metadata", "design-stage examples"])
    prohibited_reference_uses: list[str] = field(default_factory=lambda: ["execute", "import runtime", "install dependencies", "run tests", "read secrets"])
    prohibited_file_patterns: list[str] = field(default_factory=lambda: list(DEFAULT_PROHIBITED_FILE_PATTERNS))
    ready_for_reference_code_execution: bool = False
    ready_for_reference_import: bool = False
    ready_for_reference_dependency_install: bool = False
    ready_for_reference_test_execution: bool = False
    ready_for_reference_readonly_inspection: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("reference_boundary_id", self.reference_boundary_id)
        _validate_version_includes_v0330(self.version)
        _validate_string_list("known_reference_path_refs", self.known_reference_path_refs)
        for name in ("allowed_reference_uses", "prohibited_reference_uses", "prohibited_file_patterns"):
            _validate_string_list(name, getattr(self, name))
        InternalRuntimeReferenceCorpusPosture(self.posture)
        _validate_false(self, REFERENCE_RUNTIME_FLAG_NAMES)
        _validate_secret_patterns(self.prohibited_file_patterns)
        if _metadata_flag_true(self.metadata, {"file_access", "reference_execution", "reference_import"}):
            raise ValueError("InternalRuntimeReferenceCorpusBoundary is not file access")

    @property
    def file_access(self) -> bool:
        return False

    @property
    def path_refs_only(self) -> bool:
        return True


@dataclass(frozen=True)
class InternalRuntimeBoundary:
    boundary_id: str
    version: str
    release_name: str
    allowed_surfaces: list[InternalRuntimeAllowedSurface]
    prohibited_surfaces: list[InternalRuntimeProhibitedSurface]
    reference_corpus_boundary: InternalRuntimeReferenceCorpusBoundary | None
    capability_flags: InternalRuntimeCapabilityFlagSet
    status: InternalRuntimeBoundaryStatus | str
    readiness_level: InternalRuntimeReadinessLevel | str
    summary: str
    gaps: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    ready_for_v0331_agent_profile_runtime: bool = False
    ready_for_v0332_prompt_assembly: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_id", self.boundary_id)
        _validate_version_includes_v0330(self.version)
        _require_non_blank("release_name", self.release_name)
        _validate_object_list("allowed_surfaces", self.allowed_surfaces, InternalRuntimeAllowedSurface)
        _validate_object_list("prohibited_surfaces", self.prohibited_surfaces, InternalRuntimeProhibitedSurface)
        if self.reference_corpus_boundary is not None and not isinstance(self.reference_corpus_boundary, InternalRuntimeReferenceCorpusBoundary):
            raise TypeError("reference_corpus_boundary must be InternalRuntimeReferenceCorpusBoundary or None")
        if not isinstance(self.capability_flags, InternalRuntimeCapabilityFlagSet):
            raise TypeError("capability_flags must be InternalRuntimeCapabilityFlagSet")
        if not internal_runtime_flags_preserve_runtime_false(self.capability_flags):
            raise ValueError("capability_flags must preserve runtime false")
        status = InternalRuntimeBoundaryStatus(self.status)
        InternalRuntimeReadinessLevel(self.readiness_level)
        _require_non_blank("summary", self.summary)
        for name in ("gaps", "blocked_reasons", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        if (self.ready_for_v0331_agent_profile_runtime or self.ready_for_v0332_prompt_assembly) and self.blocked_reasons:
            raise ValueError("design-stage handoff readiness is not allowed with blocked_reasons")
        if (self.ready_for_v0331_agent_profile_runtime or self.ready_for_v0332_prompt_assembly) and status is InternalRuntimeBoundaryStatus.BLOCKED:
            raise ValueError("blocked boundary cannot be ready for next design-stage handoff")
        if _metadata_flag_true(self.metadata, {"runtime_execution", "runtime_enablement"}):
            raise ValueError("InternalRuntimeBoundary is not runtime execution")

    @property
    def runtime_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalRuntimePermissionRequest:
    request_id: str
    requested_surface: InternalRuntimeSurfaceKind | str
    requested_capability: InternalRuntimeCapabilityKind | str
    requested_action_summary: str
    source_track: InternalRuntimeTrackKind | str
    source_artifact_refs: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("request_id", self.request_id)
        InternalRuntimeSurfaceKind(self.requested_surface)
        InternalRuntimeCapabilityKind(self.requested_capability)
        _require_non_blank("requested_action_summary", self.requested_action_summary)
        InternalRuntimeTrackKind(self.source_track)
        _validate_string_list("source_artifact_refs", self.source_artifact_refs)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"permission_grant", "execution"}):
            raise ValueError("InternalRuntimePermissionRequest is not permission grant or execution")

    @property
    def permission_grant(self) -> bool:
        return False

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalRuntimePermissionDecision:
    decision_id: str
    request_id: str
    decision_kind: InternalRuntimePermissionDecisionKind | str
    reason: str
    allowed_only_for_design_stage: bool = False
    allowed_only_for_boundary_definition: bool = False
    execution_allowed: bool = False
    runtime_side_effect_allowed: bool = False
    requires_user_confirmation: bool = False
    required_reviews: list[str] = field(default_factory=list)
    denied_risk_surfaces: list[InternalRuntimeRiskSurfaceKind | str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("decision_id", self.decision_id)
        _require_non_blank("request_id", self.request_id)
        InternalRuntimePermissionDecisionKind(self.decision_kind)
        _require_non_blank("reason", self.reason)
        _validate_string_list("required_reviews", self.required_reviews)
        if not isinstance(self.denied_risk_surfaces, list):
            raise TypeError("denied_risk_surfaces must be list")
        for value in self.denied_risk_surfaces:
            InternalRuntimeRiskSurfaceKind(value)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.execution_allowed is not False:
            raise ValueError("execution_allowed must always be False in v0.33.0")
        if self.runtime_side_effect_allowed is not False:
            raise ValueError("runtime_side_effect_allowed must always be False in v0.33.0")
        if _metadata_flag_true(self.metadata, {"runtime_permission_grant", "execution_permission"}):
            raise ValueError("InternalRuntimePermissionDecision is not runtime permission grant")

    @property
    def runtime_permission_grant(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalRuntimeDeniedAction:
    denied_action_id: str
    request_id: str | None
    decision_id: str | None
    denied_surface: InternalRuntimeSurfaceKind | str
    denied_capability: InternalRuntimeCapabilityKind | str
    reason: str
    risk_surfaces: list[InternalRuntimeRiskSurfaceKind | str] = field(default_factory=list)
    safe_alternatives: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("denied_action_id", self.denied_action_id)
        InternalRuntimeSurfaceKind(self.denied_surface)
        InternalRuntimeCapabilityKind(self.denied_capability)
        _require_non_blank("reason", self.reason)
        if not isinstance(self.risk_surfaces, list):
            raise TypeError("risk_surfaces must be list")
        for value in self.risk_surfaces:
            InternalRuntimeRiskSurfaceKind(value)
        _validate_string_list("safe_alternatives", self.safe_alternatives)
        _validate_string_list("evidence_refs", self.evidence_refs)

    @property
    def safe_outcome(self) -> bool:
        return True


@dataclass(frozen=True)
class InternalRuntimeGateEvaluation:
    evaluation_id: str
    boundary_id: str
    request_id: str
    decision: InternalRuntimePermissionDecision
    denied_actions: list[InternalRuntimeDeniedAction]
    allowed_design_stage_only: bool
    execution_allowed: bool
    runtime_side_effect_allowed: bool
    summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("evaluation_id", self.evaluation_id)
        _require_non_blank("boundary_id", self.boundary_id)
        _require_non_blank("request_id", self.request_id)
        if not isinstance(self.decision, InternalRuntimePermissionDecision):
            raise TypeError("decision must be InternalRuntimePermissionDecision")
        _validate_object_list("denied_actions", self.denied_actions, InternalRuntimeDeniedAction)
        if self.execution_allowed is not False:
            raise ValueError("execution_allowed must always be False in v0.33.0")
        if self.runtime_side_effect_allowed is not False:
            raise ValueError("runtime_side_effect_allowed must always be False in v0.33.0")
        _require_non_blank("summary", self.summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"execution", "runtime_side_effect"}):
            raise ValueError("InternalRuntimeGateEvaluation is not execution")

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalRuntimeNoExternalSideEffectGuarantee:
    guarantee_id: str
    version: str = V0330_VERSION
    no_runtime_execution: bool = True
    no_external_harness_execution: bool = True
    no_reference_code_execution: bool = True
    no_reference_import: bool = True
    no_dependency_install: bool = True
    no_live_scan: bool = True
    no_source_ref_fetch: bool = True
    no_secret_file_read: bool = True
    no_read_only_tool_execution: bool = True
    no_workspace_inspection_execution: bool = True
    no_agent_step_execution: bool = True
    no_provider_invocation: bool = True
    no_network_access: bool = True
    no_credential_access: bool = True
    no_command_execution: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_patch_application: bool = True
    no_browser_runtime_control: bool = True
    no_rpa_runtime_control: bool = True
    no_gateway_control: bool = True
    no_packet_send: bool = True
    no_registry_mutation: bool = True
    no_memory_mutation: bool = True
    no_ocel_emission: bool = True
    no_ui_runtime: bool = True
    no_external_control: bool = True
    no_authority_grant: bool = True
    no_d4_d9_grant: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version_includes_v0330(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.33.0")
        _validate_string_list("evidence_refs", self.evidence_refs)


@dataclass(frozen=True)
class V033RoadmapOverview:
    roadmap_id: str
    version: str
    release_name: str
    stages: list[InternalRuntimeTrackKind | str]
    stage_summaries: dict[str, str]
    references_context_summary: str
    opencode_reference_role: str
    hermes_reference_role: str
    openclaw_reference_role: str | None
    runtime_boundary_summary: str
    prohibited_runtime_summary: str
    v034_handoff_preview: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("roadmap_id", self.roadmap_id)
        _validate_version_includes_v0330(self.version)
        _require_non_blank("release_name", self.release_name)
        _validate_roadmap_stages(self.stages)
        if not isinstance(self.stage_summaries, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in self.stage_summaries.items()):
            raise TypeError("stage_summaries must be dict[str, str]")
        for name in (
            "references_context_summary",
            "opencode_reference_role",
            "hermes_reference_role",
            "runtime_boundary_summary",
            "prohibited_runtime_summary",
            "v034_handoff_preview",
        ):
            _require_non_blank(name, getattr(self, name))
        required_phrase = "read-only design/reference corpus only"
        if required_phrase not in self.opencode_reference_role.lower():
            raise ValueError("opencode_reference_role must say read-only design/reference corpus only")
        if required_phrase not in self.hermes_reference_role.lower():
            raise ValueError("hermes_reference_role must say read-only design/reference corpus only")
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"implementation", "runtime_execution"}):
            raise ValueError("V033RoadmapOverview is not implementation")

    @property
    def implementation(self) -> bool:
        return False


@dataclass(frozen=True)
class V0330ReadinessReport:
    report_id: str
    version: str = V0330_VERSION
    boundary_id: str | None = None
    roadmap_id: str | None = None
    summary: str = "v0.33.0 defines the internal runtime boundary and permission gate only."
    ready_for_v0331_agent_profile_runtime: bool = False
    ready_for_v0332_prompt_assembly: bool = False
    ready_for_execution: bool = False
    ready_for_external_harness_execution: bool = False
    ready_for_reference_code_execution: bool = False
    ready_for_live_scan: bool = False
    ready_for_read_only_tool_execution: bool = False
    ready_for_workspace_inspection_execution: bool = False
    ready_for_agent_step_execution: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_application: bool = False
    ready_for_browser_runtime_control: bool = False
    ready_for_rpa_runtime_control: bool = False
    ready_for_gateway_control: bool = False
    ready_for_packet_send: bool = False
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
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_V0330_PROHIBITED_RUNTIME_ACTIONS))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0330(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(self, RUNTIME_FLAG_NAMES)
        for name in ("completed_items", "blocked_items", "future_track_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_prohibited_runtime_actions("prohibited_until_later_gate", self.prohibited_until_later_gate)
        if (self.ready_for_v0331_agent_profile_runtime or self.ready_for_v0332_prompt_assembly) and self.blocked_items:
            raise ValueError("design-stage handoff readiness is not allowed with blocked_items")
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "execution_readiness"}):
            raise ValueError("V0330ReadinessReport is not runtime enablement")

    @property
    def runtime_enablement(self) -> bool:
        return False


def build_internal_runtime_capability_flags(flag_set_id: str = "internal_runtime_capability_flags:v0.33.0", **kwargs: Any) -> InternalRuntimeCapabilityFlagSet:
    return InternalRuntimeCapabilityFlagSet(flag_set_id=flag_set_id, version=V0330_VERSION, **kwargs)


def build_internal_runtime_allowed_surface(
    allowed_surface_id: str,
    surface_kind: InternalRuntimeSurfaceKind | str,
    capability_kind: InternalRuntimeCapabilityKind | str,
    description: str,
    **kwargs: Any,
) -> InternalRuntimeAllowedSurface:
    return InternalRuntimeAllowedSurface(
        allowed_surface_id=allowed_surface_id,
        surface_kind=surface_kind,
        capability_kind=capability_kind,
        description=description,
        **kwargs,
    )


def build_internal_runtime_prohibited_surface(
    prohibited_surface_id: str,
    surface_kind: InternalRuntimeSurfaceKind | str,
    risk_surface: InternalRuntimeRiskSurfaceKind | str,
    capability_kind: InternalRuntimeCapabilityKind | str,
    reason: str,
    **kwargs: Any,
) -> InternalRuntimeProhibitedSurface:
    return InternalRuntimeProhibitedSurface(
        prohibited_surface_id=prohibited_surface_id,
        surface_kind=surface_kind,
        risk_surface=risk_surface,
        capability_kind=capability_kind,
        reason=reason,
        **kwargs,
    )


def build_internal_runtime_reference_corpus_boundary(reference_boundary_id: str = "reference_corpus_boundary:v0.33.0", **kwargs: Any) -> InternalRuntimeReferenceCorpusBoundary:
    return InternalRuntimeReferenceCorpusBoundary(reference_boundary_id=reference_boundary_id, version=V0330_VERSION, **kwargs)


def build_internal_runtime_boundary(boundary_id: str, capability_flags: InternalRuntimeCapabilityFlagSet | None = None, **kwargs: Any) -> InternalRuntimeBoundary:
    return InternalRuntimeBoundary(
        boundary_id=boundary_id,
        version=V0330_VERSION,
        release_name=kwargs.pop("release_name", V0330_RELEASE_NAME),
        allowed_surfaces=kwargs.pop("allowed_surfaces", []),
        prohibited_surfaces=kwargs.pop("prohibited_surfaces", []),
        reference_corpus_boundary=kwargs.pop("reference_corpus_boundary", build_internal_runtime_reference_corpus_boundary()),
        capability_flags=capability_flags or build_internal_runtime_capability_flags(),
        status=kwargs.pop("status", InternalRuntimeBoundaryStatus.BOUNDARY_READY_WITH_GAPS),
        readiness_level=kwargs.pop("readiness_level", InternalRuntimeReadinessLevel.BOUNDARY_CONTRACT_READY),
        summary=kwargs.pop("summary", "Internal runtime boundary and permission gate contract only."),
        **kwargs,
    )


def build_internal_runtime_permission_request(request_id: str, **kwargs: Any) -> InternalRuntimePermissionRequest:
    return InternalRuntimePermissionRequest(
        request_id=request_id,
        requested_surface=kwargs.pop("requested_surface", InternalRuntimeSurfaceKind.PERMISSION_GATE),
        requested_capability=kwargs.pop("requested_capability", InternalRuntimeCapabilityKind.EVALUATE_PERMISSION),
        requested_action_summary=kwargs.pop("requested_action_summary", "Evaluate design-stage permission request."),
        source_track=kwargs.pop("source_track", InternalRuntimeTrackKind.BOUNDARY_PERMISSION_GATE),
        **kwargs,
    )


def build_internal_runtime_permission_decision(decision_id: str, request_id: str, **kwargs: Any) -> InternalRuntimePermissionDecision:
    return InternalRuntimePermissionDecision(
        decision_id=decision_id,
        request_id=request_id,
        decision_kind=kwargs.pop("decision_kind", InternalRuntimePermissionDecisionKind.ALLOWED_BOUNDARY_DEFINITION_ONLY),
        reason=kwargs.pop("reason", "Allowed for boundary definition only; execution remains prohibited."),
        **kwargs,
    )


def build_internal_runtime_denied_action(denied_action_id: str, **kwargs: Any) -> InternalRuntimeDeniedAction:
    return InternalRuntimeDeniedAction(
        denied_action_id=denied_action_id,
        request_id=kwargs.pop("request_id", None),
        decision_id=kwargs.pop("decision_id", None),
        denied_surface=kwargs.pop("denied_surface", InternalRuntimeSurfaceKind.SHELL_COMMAND),
        denied_capability=kwargs.pop("denied_capability", InternalRuntimeCapabilityKind.RUN_SHELL_COMMAND),
        reason=kwargs.pop("reason", "Runtime action is denied in v0.33.0."),
        **kwargs,
    )


def build_internal_runtime_gate_evaluation(evaluation_id: str, boundary_id: str, request_id: str, decision: InternalRuntimePermissionDecision, **kwargs: Any) -> InternalRuntimeGateEvaluation:
    return InternalRuntimeGateEvaluation(
        evaluation_id=evaluation_id,
        boundary_id=boundary_id,
        request_id=request_id,
        decision=decision,
        denied_actions=kwargs.pop("denied_actions", []),
        allowed_design_stage_only=kwargs.pop("allowed_design_stage_only", True),
        execution_allowed=kwargs.pop("execution_allowed", False),
        runtime_side_effect_allowed=kwargs.pop("runtime_side_effect_allowed", False),
        summary=kwargs.pop("summary", "Gate evaluation preserves no runtime execution."),
        **kwargs,
    )


def build_internal_runtime_no_external_side_effect_guarantee(guarantee_id: str = "internal_runtime_no_external_side_effect:v0.33.0", **kwargs: Any) -> InternalRuntimeNoExternalSideEffectGuarantee:
    return InternalRuntimeNoExternalSideEffectGuarantee(guarantee_id=guarantee_id, version=V0330_VERSION, **kwargs)


def build_v033_roadmap_overview(roadmap_id: str = "v033_roadmap:v0.33.0", **kwargs: Any) -> V033RoadmapOverview:
    return V033RoadmapOverview(
        roadmap_id=roadmap_id,
        version=V0330_VERSION,
        release_name=kwargs.pop("release_name", V0330_RELEASE_NAME),
        stages=kwargs.pop("stages", list(DEFAULT_V033_STAGES)),
        stage_summaries=kwargs.pop("stage_summaries", {stage: f"{stage} design-stage track." for stage in DEFAULT_V033_STAGES}),
        references_context_summary=kwargs.pop("references_context_summary", "Reference corpus paths remain read-only design/reference corpus context only."),
        opencode_reference_role=kwargs.pop("opencode_reference_role", "references/OpenCode is read-only design/reference corpus only."),
        hermes_reference_role=kwargs.pop("hermes_reference_role", "references/Hermes is read-only design/reference corpus only."),
        openclaw_reference_role=kwargs.pop("openclaw_reference_role", "references/OpenClaw is optional read-only design/reference corpus only."),
        runtime_boundary_summary=kwargs.pop("runtime_boundary_summary", "v0.33.0 defines boundary and permission gate contracts only."),
        prohibited_runtime_summary=kwargs.pop("prohibited_runtime_summary", "Runtime execution and external side effects remain prohibited."),
        v034_handoff_preview=kwargs.pop("v034_handoff_preview", "v0.34 is outside this boundary and receives no runtime grant from v0.33.0."),
        **kwargs,
    )


def build_v0330_readiness_report(report_id: str = "v0330_readiness_report", **kwargs: Any) -> V0330ReadinessReport:
    return V0330ReadinessReport(report_id=report_id, version=V0330_VERSION, **kwargs)


def internal_runtime_flags_preserve_runtime_false(flags: InternalRuntimeCapabilityFlagSet) -> bool:
    return (
        all(getattr(flags, name) is False for name in RUNTIME_FLAG_NAMES)
        and flags.production_certified is False
        and flags.live_adapter_certified is False
    )


def internal_runtime_boundary_is_not_execution(boundary: InternalRuntimeBoundary) -> bool:
    return (
        boundary.ready_for_execution is False
        and boundary.runtime_execution is False
        and internal_runtime_flags_preserve_runtime_false(boundary.capability_flags)
    )


def permission_decision_preserves_no_execution(decision: InternalRuntimePermissionDecision) -> bool:
    return (
        decision.execution_allowed is False
        and decision.runtime_side_effect_allowed is False
        and decision.runtime_permission_grant is False
    )


def reference_corpus_boundary_preserves_no_reference_execution(boundary: InternalRuntimeReferenceCorpusBoundary) -> bool:
    return (
        all(getattr(boundary, name) is False for name in REFERENCE_RUNTIME_FLAG_NAMES)
        and boundary.file_access is False
        and boundary.path_refs_only is True
    )


def v0330_readiness_report_is_not_runtime_ready(report: V0330ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in RUNTIME_FLAG_NAMES) and report.runtime_enablement is False
