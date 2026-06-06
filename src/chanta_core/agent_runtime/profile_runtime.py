from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import (
    InternalRuntimeBoundary,
    InternalRuntimeCapabilityFlagSet,
    internal_runtime_flags_preserve_runtime_false,
    _metadata_flag_true,
    _require_non_blank,
    _validate_object_list,
    _validate_string_list,
)


V0331_VERSION = "v0.33.1"
V0331_RELEASE_NAME = "v0.33.1 Agent Profile Runtime"

DEFAULT_PROFILE_PROHIBITED_RUNTIME_ACTIONS = [
    "execution",
    "agent runtime execution",
    "agent_step_execution",
    "agent step execution",
    "prompt_assembly_execution",
    "prompt assembly execution",
    "session_runtime_execution",
    "session runtime execution",
    "read_only_tool_execution",
    "read-only tool execution",
    "tool_execution",
    "tool execution",
    "workspace_inspection_execution",
    "workspace inspection execution",
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
    "reference_code_execution",
    "reference code execution",
    "reference_import",
    "reference import",
    "dependency_install",
    "dependency install",
    "secret_file_read",
    "secret file read",
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
]


class AgentProfileKind(StrEnum):
    VERA = "vera"
    CHANTA_CORE = "chanta_core"
    CHANTA_RESEARCH_GROUP = "chanta_research_group"
    SCHUMPETER = "schumpeter"
    GENERIC_INTERNAL_AGENT = "generic_internal_agent"
    TEST_PROFILE = "test_profile"
    UNKNOWN = "unknown"


class AgentProfileModeKind(StrEnum):
    DEFAULT = "default"
    RESEARCH = "research"
    CODING_ASSISTANT = "coding_assistant"
    PROCESS_INTELLIGENCE = "process_intelligence"
    EXTERNAL_HARNESS_ANALYSIS = "external_harness_analysis"
    REFERENCE_CORPUS_REVIEW = "reference_corpus_review"
    SAFE_READONLY = "safe_readonly"
    BOUNDARY_REVIEW = "boundary_review"
    TEST = "test"
    UNKNOWN = "unknown"


class AgentProfileSourceKind(StrEnum):
    MANUAL_PROFILE_SPEC = "manual_profile_spec"
    V0330_BOUNDARY = "v0330_boundary"
    V0329_HANDOFF_PACKET = "v0329_handoff_packet"
    V032_REFERENCE_CONTEXT = "v032_reference_context"
    MEMORY_CONTEXT_REF = "memory_context_ref"
    PERSONA_CONTEXT_REF = "persona_context_ref"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class AgentProfileProjectionKind(StrEnum):
    PERSONA_PROJECTION = "persona_projection"
    ROLE_PROJECTION = "role_projection"
    MODE_PROJECTION = "mode_projection"
    POLICY_PROJECTION = "policy_projection"
    REFERENCE_CONTEXT_PROJECTION = "reference_context_projection"
    SAFETY_BOUNDARY_PROJECTION = "safety_boundary_projection"
    UNKNOWN = "unknown"


class AgentProfilePolicyOverlayKind(StrEnum):
    NO_EXTERNAL_SIDE_EFFECTS = "no_external_side_effects"
    NO_REFERENCE_EXECUTION = "no_reference_execution"
    NO_SECRET_ACCESS = "no_secret_access"
    NO_WORKSPACE_WRITE = "no_workspace_write"
    NO_COMMAND_EXECUTION = "no_command_execution"
    NO_PROVIDER_INVOCATION = "no_provider_invocation"
    NO_NETWORK_ACCESS = "no_network_access"
    NO_REGISTRY_MUTATION = "no_registry_mutation"
    NO_MEMORY_MUTATION = "no_memory_mutation"
    NO_EXTERNAL_CONTROL = "no_external_control"
    NO_AUTHORITY_GRANT = "no_authority_grant"
    REQUIRE_PERMISSION_GATE = "require_permission_gate"
    REQUIRE_EVIDENCE_REFS = "require_evidence_refs"
    REQUIRE_SAFE_FAIL = "require_safe_fail"
    UNKNOWN = "unknown"


class AgentProfileLoadoutKind(StrEnum):
    PROFILE_ONLY = "profile_only"
    PROFILE_WITH_BOUNDARY = "profile_with_boundary"
    PROFILE_WITH_REFERENCE_CONTEXT = "profile_with_reference_context"
    PROFILE_WITH_POLICY_OVERLAY = "profile_with_policy_overlay"
    PROFILE_WITH_TOOL_AVAILABILITY_VIEW = "profile_with_tool_availability_view"
    TEST_LOADOUT = "test_loadout"
    UNKNOWN = "unknown"


class AgentProfileContextRoleKind(StrEnum):
    PRIMARY_PERSONA = "primary_persona"
    ASSISTANT_ROLE = "assistant_role"
    RESEARCH_ROLE = "research_role"
    CODING_REFERENCE_ROLE = "coding_reference_role"
    PROCESS_INTELLIGENCE_ROLE = "process_intelligence_role"
    EXTERNAL_HARNESS_REFERENCE_ROLE = "external_harness_reference_role"
    OPENCODE_REFERENCE_ROLE = "opencode_reference_role"
    HERMES_REFERENCE_ROLE = "hermes_reference_role"
    OPENCLAW_REFERENCE_ROLE = "openclaw_reference_role"
    SAFETY_BOUNDARY_ROLE = "safety_boundary_role"
    UNKNOWN = "unknown"


class AgentProfileResolutionStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    RESOLVED = "resolved"
    RESOLVED_WITH_GAPS = "resolved_with_gaps"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class AgentProfileReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    PROFILE_CONTRACT_READY = "profile_contract_ready"
    PROFILE_RESOLUTION_READY = "profile_resolution_ready"
    DESIGN_HANDOFF_READY_FOR_V0332 = "design_handoff_ready_for_v0332"
    DESIGN_HANDOFF_READY_FOR_V0333 = "design_handoff_ready_for_v0333"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class AgentProfileEvidenceQuality(StrEnum):
    UNKNOWN = "unknown"
    NONE = "none"
    WEAK = "weak"
    PARTIAL = "partial"
    SUFFICIENT_FOR_PROFILE_RESOLUTION = "sufficient_for_profile_resolution"
    SUFFICIENT_FOR_V0332_REVIEW = "sufficient_for_v0332_review"
    CONFLICTING = "conflicting"
    BLOCKED = "blocked"


RUNTIME_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_agent_step_execution",
    "ready_for_prompt_assembly_execution",
    "ready_for_session_runtime_execution",
    "ready_for_read_only_tool_execution",
    "ready_for_workspace_inspection_execution",
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
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
)


def _validate_version_includes_v0331(version: str) -> None:
    _require_non_blank("version", version)
    if V0331_VERSION not in version:
        raise ValueError("version must include v0.33.1")


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.33.1")


def _validate_true(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not True:
            raise ValueError(f"{name} must always be True in v0.33.1")


def _validate_source_ref_list(values: list["AgentProfileSourceRef"]) -> None:
    _validate_object_list("source_refs", values, AgentProfileSourceRef)


def _validate_enum_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _validate_prohibited_runtime_actions(name: str, values: list[str]) -> None:
    _validate_string_list(name, values)
    missing = set(DEFAULT_PROFILE_PROHIBITED_RUNTIME_ACTIONS) - set(values)
    if missing:
        raise ValueError(f"{name} missing v0.33.1 prohibitions: {sorted(missing)}")


@dataclass(frozen=True)
class AgentProfileRuntimeFlagSet:
    flag_set_id: str
    version: str = V0331_VERSION
    ready_for_v0332_prompt_assembly: bool = False
    ready_for_v0333_session_runtime: bool = False
    ready_for_execution: bool = False
    ready_for_agent_step_execution: bool = False
    ready_for_prompt_assembly_execution: bool = False
    ready_for_session_runtime_execution: bool = False
    ready_for_read_only_tool_execution: bool = False
    ready_for_workspace_inspection_execution: bool = False
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
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version_includes_v0331(self.version)
        _validate_false(self, RUNTIME_FLAG_NAMES)
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "permission_grant", "active_session"}):
            raise ValueError("AgentProfileRuntimeFlagSet is not runtime enablement")


@dataclass(frozen=True)
class AgentProfileSourceRef:
    source_ref_id: str
    source_kind: AgentProfileSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        AgentProfileSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"fetch", "memory_read", "execution"}):
            raise ValueError("AgentProfileSourceRef is not fetch, memory read, or execution")

    @property
    def fetch(self) -> bool:
        return False

    @property
    def memory_read(self) -> bool:
        return False

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentProfilePersonaProjection:
    projection_id: str
    projection_kind: AgentProfileProjectionKind | str
    profile_kind: AgentProfileKind | str
    display_name: str
    role_summary: str
    behavior_summary: str
    constraints_summary: str
    source_refs: list[AgentProfileSourceRef] = field(default_factory=list)
    evidence_quality: AgentProfileEvidenceQuality | str = AgentProfileEvidenceQuality.UNKNOWN
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("projection_id", self.projection_id)
        AgentProfileProjectionKind(self.projection_kind)
        AgentProfileKind(self.profile_kind)
        for name in ("display_name", "role_summary", "behavior_summary", "constraints_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_source_ref_list(self.source_refs)
        AgentProfileEvidenceQuality(self.evidence_quality)
        if _metadata_flag_true(self.metadata, {"authority_grant", "autonomous_identity"}):
            raise ValueError("AgentProfilePersonaProjection is not authority grant")

    @property
    def authority_grant(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentProfileModeBinding:
    mode_binding_id: str
    mode_kind: AgentProfileModeKind | str
    title: str
    summary: str
    active_context_roles: list[AgentProfileContextRoleKind | str] = field(default_factory=list)
    prohibited_context_roles: list[AgentProfileContextRoleKind | str] = field(default_factory=list)
    source_refs: list[AgentProfileSourceRef] = field(default_factory=list)
    ready_for_tool_activation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("mode_binding_id", self.mode_binding_id)
        AgentProfileModeKind(self.mode_kind)
        _require_non_blank("title", self.title)
        _require_non_blank("summary", self.summary)
        _validate_enum_list("active_context_roles", self.active_context_roles, AgentProfileContextRoleKind)
        _validate_enum_list("prohibited_context_roles", self.prohibited_context_roles, AgentProfileContextRoleKind)
        _validate_source_ref_list(self.source_refs)
        _validate_false(self, ("ready_for_tool_activation", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"tool_activation", "runtime_execution"}):
            raise ValueError("AgentProfileModeBinding is not tool activation")

    @property
    def tool_activation(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentProfilePolicyOverlay:
    policy_overlay_id: str
    overlay_kinds: list[AgentProfilePolicyOverlayKind | str] = field(default_factory=lambda: [
        AgentProfilePolicyOverlayKind.NO_EXTERNAL_SIDE_EFFECTS,
        AgentProfilePolicyOverlayKind.REQUIRE_PERMISSION_GATE,
        AgentProfilePolicyOverlayKind.REQUIRE_SAFE_FAIL,
    ])
    summary: str = "Conservative profile policy overlay for v0.33.1 profile resolution only."
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_PROFILE_PROHIBITED_RUNTIME_ACTIONS))
    required_permission_gate: bool = True
    required_safe_fail: bool = True
    source_refs: list[AgentProfileSourceRef] = field(default_factory=list)
    ready_for_policy_activation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_overlay_id", self.policy_overlay_id)
        _validate_enum_list("overlay_kinds", self.overlay_kinds, AgentProfilePolicyOverlayKind)
        _require_non_blank("summary", self.summary)
        _validate_prohibited_runtime_actions("prohibited_runtime_actions", self.prohibited_runtime_actions)
        if self.required_permission_gate is not True:
            raise ValueError("required_permission_gate should default True")
        if self.required_safe_fail is not True:
            raise ValueError("required_safe_fail should default True")
        _validate_source_ref_list(self.source_refs)
        _validate_false(self, ("ready_for_policy_activation", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"active_policy_enforcement", "policy_activation"}):
            raise ValueError("AgentProfilePolicyOverlay is not active policy enforcement")

    @property
    def active_policy_enforcement(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentProfileReferenceContext:
    reference_context_id: str
    posture: str
    references_root_path_ref: str | None = "references/"
    opencode_reference_path_ref: str | None = "references/OpenCode"
    hermes_reference_path_ref: str | None = "references/Hermes"
    openclaw_reference_path_ref: str | None = "references/OpenClaw"
    context_roles: list[AgentProfileContextRoleKind | str] = field(default_factory=lambda: [
        AgentProfileContextRoleKind.OPENCODE_REFERENCE_ROLE,
        AgentProfileContextRoleKind.HERMES_REFERENCE_ROLE,
    ])
    allowed_reference_uses: list[str] = field(default_factory=lambda: ["path refs", "design notes", "prior v0.32 metadata"])
    prohibited_reference_uses: list[str] = field(default_factory=lambda: ["file access", "execute", "import runtime", "install dependencies", "read secrets"])
    source_refs: list[AgentProfileSourceRef] = field(default_factory=list)
    ready_for_reference_file_access: bool = False
    ready_for_reference_code_execution: bool = False
    ready_for_reference_import: bool = False
    ready_for_reference_dependency_install: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("reference_context_id", self.reference_context_id)
        _require_non_blank("posture", self.posture)
        _validate_enum_list("context_roles", self.context_roles, AgentProfileContextRoleKind)
        for name in ("allowed_reference_uses", "prohibited_reference_uses"):
            _validate_string_list(name, getattr(self, name))
        _validate_source_ref_list(self.source_refs)
        _validate_false(
            self,
            (
                "ready_for_reference_file_access",
                "ready_for_reference_code_execution",
                "ready_for_reference_import",
                "ready_for_reference_dependency_install",
            ),
        )
        if _metadata_flag_true(self.metadata, {"file_access", "reference_execution", "reference_import"}):
            raise ValueError("AgentProfileReferenceContext is not file access")

    @property
    def file_access(self) -> bool:
        return False

    @property
    def path_refs_only(self) -> bool:
        return True


@dataclass(frozen=True)
class AgentProfileToolAvailabilityView:
    tool_availability_view_id: str
    available_tool_names: list[str] = field(default_factory=list)
    unavailable_tool_names: list[str] = field(default_factory=list)
    future_tool_names: list[str] = field(default_factory=list)
    summary: str = "Tool availability view only; no registry access or execution."
    source_refs: list[AgentProfileSourceRef] = field(default_factory=list)
    ready_for_tool_registry_access: bool = False
    ready_for_tool_execution: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("tool_availability_view_id", self.tool_availability_view_id)
        for name in ("available_tool_names", "unavailable_tool_names", "future_tool_names"):
            _validate_string_list(name, getattr(self, name))
        _require_non_blank("summary", self.summary)
        _validate_source_ref_list(self.source_refs)
        _validate_false(self, ("ready_for_tool_registry_access", "ready_for_tool_execution", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"tool_registry_access", "tool_execution"}):
            raise ValueError("AgentProfileToolAvailabilityView is not tool registry access")

    @property
    def tool_registry_access(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentRuntimeLoadout:
    loadout_id: str
    loadout_kind: AgentProfileLoadoutKind | str
    persona_projection: AgentProfilePersonaProjection
    mode_binding: AgentProfileModeBinding
    policy_overlay: AgentProfilePolicyOverlay
    reference_context: AgentProfileReferenceContext | None
    tool_availability_view: AgentProfileToolAvailabilityView | None
    runtime_boundary_id: str | None
    summary: str
    gaps: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    source_refs: list[AgentProfileSourceRef] = field(default_factory=list)
    ready_for_prompt_assembly: bool = False
    ready_for_session_runtime: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("loadout_id", self.loadout_id)
        AgentProfileLoadoutKind(self.loadout_kind)
        if not isinstance(self.persona_projection, AgentProfilePersonaProjection):
            raise TypeError("persona_projection must be AgentProfilePersonaProjection")
        if not isinstance(self.mode_binding, AgentProfileModeBinding):
            raise TypeError("mode_binding must be AgentProfileModeBinding")
        if not isinstance(self.policy_overlay, AgentProfilePolicyOverlay):
            raise TypeError("policy_overlay must be AgentProfilePolicyOverlay")
        if self.reference_context is not None and not isinstance(self.reference_context, AgentProfileReferenceContext):
            raise TypeError("reference_context must be AgentProfileReferenceContext or None")
        if self.tool_availability_view is not None and not isinstance(self.tool_availability_view, AgentProfileToolAvailabilityView):
            raise TypeError("tool_availability_view must be AgentProfileToolAvailabilityView or None")
        _require_non_blank("summary", self.summary)
        for name in ("gaps", "blocked_reasons"):
            _validate_string_list(name, getattr(self, name))
        _validate_source_ref_list(self.source_refs)
        if (self.ready_for_prompt_assembly or self.ready_for_session_runtime) and self.blocked_reasons:
            raise ValueError("design-stage loadout handoff readiness is not allowed with blocked_reasons")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        if _metadata_flag_true(self.metadata, {"runtime_action", "tool_activation"}):
            raise ValueError("AgentRuntimeLoadout is not runtime action")

    @property
    def runtime_action(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentRuntimeProfile:
    runtime_profile_id: str
    profile_kind: AgentProfileKind | str
    mode_kind: AgentProfileModeKind | str
    display_name: str
    description: str
    loadout: AgentRuntimeLoadout
    runtime_flags: AgentProfileRuntimeFlagSet
    status: AgentProfileResolutionStatus | str
    readiness_level: AgentProfileReadinessLevel | str
    summary: str
    evidence_refs: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    ready_for_v0332_prompt_assembly: bool = False
    ready_for_v0333_session_runtime: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("runtime_profile_id", self.runtime_profile_id)
        AgentProfileKind(self.profile_kind)
        AgentProfileModeKind(self.mode_kind)
        for name in ("display_name", "description", "summary"):
            _require_non_blank(name, getattr(self, name))
        if not isinstance(self.loadout, AgentRuntimeLoadout):
            raise TypeError("loadout must be AgentRuntimeLoadout")
        if not isinstance(self.runtime_flags, AgentProfileRuntimeFlagSet):
            raise TypeError("runtime_flags must be AgentProfileRuntimeFlagSet")
        if not agent_profile_flags_preserve_runtime_false(self.runtime_flags):
            raise ValueError("runtime_flags must preserve runtime false")
        AgentProfileResolutionStatus(self.status)
        AgentProfileReadinessLevel(self.readiness_level)
        for name in ("evidence_refs", "assumptions", "limitations", "gaps", "blocked_reasons"):
            _validate_string_list(name, getattr(self, name))
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        if (self.ready_for_v0332_prompt_assembly or self.ready_for_v0333_session_runtime) and self.blocked_reasons:
            raise ValueError("design-stage profile handoff readiness is not allowed with blocked_reasons")
        if _metadata_flag_true(self.metadata, {"active_session", "runtime_execution"}):
            raise ValueError("AgentRuntimeProfile is not active session")

    @property
    def active_session(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentProfileResolutionInput:
    resolution_input_id: str
    source_version: str
    requested_profile_kind: AgentProfileKind | str
    requested_mode_kind: AgentProfileModeKind | str
    runtime_boundary_id: str | None = None
    boundary_status_ref: str | None = None
    source_refs: list[AgentProfileSourceRef] = field(default_factory=list)
    requested_context_roles: list[AgentProfileContextRoleKind | str] = field(default_factory=list)
    task_summary: str = "Resolve in-memory agent profile metadata."
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_PROFILE_PROHIBITED_RUNTIME_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("resolution_input_id", self.resolution_input_id)
        _require_non_blank("source_version", self.source_version)
        AgentProfileKind(self.requested_profile_kind)
        AgentProfileModeKind(self.requested_mode_kind)
        _validate_source_ref_list(self.source_refs)
        _validate_enum_list("requested_context_roles", self.requested_context_roles, AgentProfileContextRoleKind)
        _require_non_blank("task_summary", self.task_summary)
        _validate_prohibited_runtime_actions("prohibited_runtime_actions", self.prohibited_runtime_actions)
        if _metadata_flag_true(self.metadata, {"runtime_execution_request", "file_load"}):
            raise ValueError("AgentProfileResolutionInput is not runtime execution request")

    @property
    def runtime_execution_request(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentProfileResolutionDecision:
    resolution_decision_id: str
    resolution_input_id: str
    decision_kind: str
    summary: str
    selected_profile_kind: AgentProfileKind | str
    selected_mode_kind: AgentProfileModeKind | str
    selected_context_roles: list[AgentProfileContextRoleKind | str] = field(default_factory=list)
    blocked_context_roles: list[AgentProfileContextRoleKind | str] = field(default_factory=list)
    denied_runtime_surfaces: list[str] = field(default_factory=list)
    required_reviews: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    ready_for_profile_resolution: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("resolution_decision_id", self.resolution_decision_id)
        _require_non_blank("resolution_input_id", self.resolution_input_id)
        _require_non_blank("decision_kind", self.decision_kind)
        _require_non_blank("summary", self.summary)
        AgentProfileKind(self.selected_profile_kind)
        AgentProfileModeKind(self.selected_mode_kind)
        _validate_enum_list("selected_context_roles", self.selected_context_roles, AgentProfileContextRoleKind)
        _validate_enum_list("blocked_context_roles", self.blocked_context_roles, AgentProfileContextRoleKind)
        for name in ("denied_runtime_surfaces", "required_reviews", "evidence_refs"):
            _validate_string_list(name, getattr(self, name))
        if self.ready_for_profile_resolution and _metadata_flag_true(self.metadata, {"file_load", "runtime_execution"}):
            raise ValueError("ready_for_profile_resolution is only for in-memory profile resolution")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        if _metadata_flag_true(self.metadata, {"permission_grant", "execution_grant"}):
            raise ValueError("AgentProfileResolutionDecision is not permission grant")

    @property
    def permission_grant(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentProfileResolutionReport:
    report_id: str
    version: str
    resolution_input_id: str
    runtime_profile_id: str | None
    decision_id: str | None
    summary: str
    status: AgentProfileResolutionStatus | str
    readiness_level: AgentProfileReadinessLevel | str
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0332_prompt_assembly: bool = False
    ready_for_v0333_session_runtime: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0331(self.version)
        _require_non_blank("resolution_input_id", self.resolution_input_id)
        _require_non_blank("summary", self.summary)
        AgentProfileResolutionStatus(self.status)
        AgentProfileReadinessLevel(self.readiness_level)
        for name in ("completed_items", "blocked_items", "future_track_items", "gaps", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        if (self.ready_for_v0332_prompt_assembly or self.ready_for_v0333_session_runtime) and self.blocked_items:
            raise ValueError("design-stage report handoff readiness is not allowed with blocked_items")
        if _metadata_flag_true(self.metadata, {"runtime_execution", "active_session"}):
            raise ValueError("AgentProfileResolutionReport is not runtime execution")

    @property
    def runtime_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentProfileRuntimeRunPreview:
    run_preview_id: str
    resolution_input_id: str | None = None
    planned_steps: list[str] = field(default_factory=lambda: ["resolve provided in-memory profile metadata"])
    expected_artifacts: list[str] = field(default_factory=lambda: ["AgentRuntimeProfile", "AgentProfileResolutionReport"])
    explicitly_not_performed: list[str] = field(default_factory=lambda: ["agent execution", "prompt assembly execution", "tool execution"])
    no_agent_step_execution_guarantee: bool = True
    no_prompt_assembly_execution_guarantee: bool = True
    no_session_runtime_execution_guarantee: bool = True
    no_read_only_tool_execution_guarantee: bool = True
    no_workspace_inspection_execution_guarantee: bool = True
    no_provider_invocation_guarantee: bool = True
    no_network_access_guarantee: bool = True
    no_credential_access_guarantee: bool = True
    no_command_execution_guarantee: bool = True
    no_reference_code_execution_guarantee: bool = True
    no_reference_import_guarantee: bool = True
    no_reference_dependency_install_guarantee: bool = True
    no_ocel_emission_guarantee: bool = True
    no_ui_runtime_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.33.1")

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentProfileRuntimeNoExecutionGuarantee:
    guarantee_id: str
    version: str = V0331_VERSION
    no_agent_runtime_execution: bool = True
    no_agent_step_execution: bool = True
    no_prompt_assembly_execution: bool = True
    no_session_runtime_execution: bool = True
    no_read_only_tool_execution: bool = True
    no_workspace_inspection_execution: bool = True
    no_provider_invocation: bool = True
    no_network_access: bool = True
    no_credential_access: bool = True
    no_command_execution: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_patch_application: bool = True
    no_reference_code_execution: bool = True
    no_reference_import: bool = True
    no_reference_dependency_install: bool = True
    no_secret_file_read: bool = True
    no_registry_mutation: bool = True
    no_memory_mutation: bool = True
    no_ocel_emission: bool = True
    no_ui_runtime: bool = True
    no_external_control: bool = True
    no_authority_grant: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version_includes_v0331(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.33.1")
        _validate_string_list("evidence_refs", self.evidence_refs)


@dataclass(frozen=True)
class V0331ReadinessReport:
    report_id: str
    version: str = V0331_VERSION
    runtime_profile_id: str | None = None
    resolution_report_id: str | None = None
    summary: str = "v0.33.1 resolves agent runtime profile contracts only."
    ready_for_v0332_prompt_assembly: bool = False
    ready_for_v0333_session_runtime: bool = False
    ready_for_execution: bool = False
    ready_for_agent_step_execution: bool = False
    ready_for_prompt_assembly_execution: bool = False
    ready_for_session_runtime_execution: bool = False
    ready_for_read_only_tool_execution: bool = False
    ready_for_workspace_inspection_execution: bool = False
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
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_PROFILE_PROHIBITED_RUNTIME_ACTIONS))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0331(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(self, RUNTIME_FLAG_NAMES)
        for name in ("completed_items", "blocked_items", "future_track_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_prohibited_runtime_actions("prohibited_until_later_gate", self.prohibited_until_later_gate)
        if (self.ready_for_v0332_prompt_assembly or self.ready_for_v0333_session_runtime) and self.blocked_items:
            raise ValueError("design-stage readiness is not allowed with blocked_items")
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "active_session"}):
            raise ValueError("V0331ReadinessReport is not runtime enablement")

    @property
    def runtime_enablement(self) -> bool:
        return False


def build_agent_profile_runtime_flags(flag_set_id: str = "agent_profile_runtime_flags:v0.33.1", **kwargs: Any) -> AgentProfileRuntimeFlagSet:
    return AgentProfileRuntimeFlagSet(flag_set_id=flag_set_id, version=V0331_VERSION, **kwargs)


def build_agent_profile_source_ref(source_ref_id: str, source_kind: AgentProfileSourceKind | str = AgentProfileSourceKind.MANUAL_PROFILE_SPEC, source_id: str = "manual_profile_spec", source_summary: str = "Provided in-memory profile metadata.", **kwargs: Any) -> AgentProfileSourceRef:
    return AgentProfileSourceRef(source_ref_id=source_ref_id, source_kind=source_kind, source_id=source_id, source_summary=source_summary, **kwargs)


def build_agent_profile_persona_projection(projection_id: str, **kwargs: Any) -> AgentProfilePersonaProjection:
    return AgentProfilePersonaProjection(
        projection_id=projection_id,
        projection_kind=kwargs.pop("projection_kind", AgentProfileProjectionKind.PERSONA_PROJECTION),
        profile_kind=kwargs.pop("profile_kind", AgentProfileKind.VERA),
        display_name=kwargs.pop("display_name", "Vera"),
        role_summary=kwargs.pop("role_summary", "Internal ChantaCore assistant profile projection."),
        behavior_summary=kwargs.pop("behavior_summary", "Profile metadata only; no autonomous execution."),
        constraints_summary=kwargs.pop("constraints_summary", "Preserve v0.33.0 boundary and no runtime authority."),
        **kwargs,
    )


def build_agent_profile_mode_binding(mode_binding_id: str, **kwargs: Any) -> AgentProfileModeBinding:
    return AgentProfileModeBinding(
        mode_binding_id=mode_binding_id,
        mode_kind=kwargs.pop("mode_kind", AgentProfileModeKind.DEFAULT),
        title=kwargs.pop("title", "Default profile mode"),
        summary=kwargs.pop("summary", "Mode binding is descriptive and does not activate tools."),
        **kwargs,
    )


def build_agent_profile_policy_overlay(policy_overlay_id: str, **kwargs: Any) -> AgentProfilePolicyOverlay:
    return AgentProfilePolicyOverlay(policy_overlay_id=policy_overlay_id, **kwargs)


def build_agent_profile_reference_context(reference_context_id: str, **kwargs: Any) -> AgentProfileReferenceContext:
    return AgentProfileReferenceContext(reference_context_id=reference_context_id, posture=kwargs.pop("posture", "path_reference_only"), **kwargs)


def build_agent_profile_tool_availability_view(tool_availability_view_id: str, **kwargs: Any) -> AgentProfileToolAvailabilityView:
    return AgentProfileToolAvailabilityView(tool_availability_view_id=tool_availability_view_id, **kwargs)


def build_agent_runtime_loadout(loadout_id: str, persona_projection: AgentProfilePersonaProjection | None = None, mode_binding: AgentProfileModeBinding | None = None, policy_overlay: AgentProfilePolicyOverlay | None = None, **kwargs: Any) -> AgentRuntimeLoadout:
    return AgentRuntimeLoadout(
        loadout_id=loadout_id,
        loadout_kind=kwargs.pop("loadout_kind", AgentProfileLoadoutKind.PROFILE_WITH_BOUNDARY),
        persona_projection=persona_projection or build_agent_profile_persona_projection(f"{loadout_id}:persona"),
        mode_binding=mode_binding or build_agent_profile_mode_binding(f"{loadout_id}:mode"),
        policy_overlay=policy_overlay or build_agent_profile_policy_overlay(f"{loadout_id}:policy"),
        reference_context=kwargs.pop("reference_context", build_agent_profile_reference_context(f"{loadout_id}:reference")),
        tool_availability_view=kwargs.pop("tool_availability_view", build_agent_profile_tool_availability_view(f"{loadout_id}:tools")),
        runtime_boundary_id=kwargs.pop("runtime_boundary_id", None),
        summary=kwargs.pop("summary", "Agent runtime loadout contract only; no runtime action."),
        **kwargs,
    )


def build_agent_runtime_profile(runtime_profile_id: str, loadout: AgentRuntimeLoadout | None = None, runtime_flags: AgentProfileRuntimeFlagSet | None = None, **kwargs: Any) -> AgentRuntimeProfile:
    return AgentRuntimeProfile(
        runtime_profile_id=runtime_profile_id,
        profile_kind=kwargs.pop("profile_kind", AgentProfileKind.VERA),
        mode_kind=kwargs.pop("mode_kind", AgentProfileModeKind.DEFAULT),
        display_name=kwargs.pop("display_name", "Vera"),
        description=kwargs.pop("description", "Resolved in-memory agent runtime profile contract."),
        loadout=loadout or build_agent_runtime_loadout(f"{runtime_profile_id}:loadout"),
        runtime_flags=runtime_flags or build_agent_profile_runtime_flags(),
        status=kwargs.pop("status", AgentProfileResolutionStatus.RESOLVED_WITH_GAPS),
        readiness_level=kwargs.pop("readiness_level", AgentProfileReadinessLevel.PROFILE_RESOLUTION_READY),
        summary=kwargs.pop("summary", "AgentRuntimeProfile is resolved but not an active session."),
        **kwargs,
    )


def build_agent_profile_resolution_input(resolution_input_id: str, **kwargs: Any) -> AgentProfileResolutionInput:
    return AgentProfileResolutionInput(
        resolution_input_id=resolution_input_id,
        source_version=kwargs.pop("source_version", V0331_VERSION),
        requested_profile_kind=kwargs.pop("requested_profile_kind", AgentProfileKind.VERA),
        requested_mode_kind=kwargs.pop("requested_mode_kind", AgentProfileModeKind.DEFAULT),
        **kwargs,
    )


def build_agent_profile_resolution_decision(resolution_decision_id: str, resolution_input_id: str, **kwargs: Any) -> AgentProfileResolutionDecision:
    return AgentProfileResolutionDecision(
        resolution_decision_id=resolution_decision_id,
        resolution_input_id=resolution_input_id,
        decision_kind=kwargs.pop("decision_kind", "resolve_in_memory_profile"),
        summary=kwargs.pop("summary", "Resolve provided in-memory profile metadata only."),
        selected_profile_kind=kwargs.pop("selected_profile_kind", AgentProfileKind.VERA),
        selected_mode_kind=kwargs.pop("selected_mode_kind", AgentProfileModeKind.DEFAULT),
        **kwargs,
    )


def build_agent_profile_resolution_report(report_id: str, resolution_input_id: str, **kwargs: Any) -> AgentProfileResolutionReport:
    return AgentProfileResolutionReport(
        report_id=report_id,
        version=V0331_VERSION,
        resolution_input_id=resolution_input_id,
        runtime_profile_id=kwargs.pop("runtime_profile_id", None),
        decision_id=kwargs.pop("decision_id", None),
        summary=kwargs.pop("summary", "Agent profile resolution report is not runtime execution."),
        status=kwargs.pop("status", AgentProfileResolutionStatus.RESOLVED_WITH_GAPS),
        readiness_level=kwargs.pop("readiness_level", AgentProfileReadinessLevel.PROFILE_RESOLUTION_READY),
        **kwargs,
    )


def build_agent_profile_runtime_run_preview(run_preview_id: str, **kwargs: Any) -> AgentProfileRuntimeRunPreview:
    return AgentProfileRuntimeRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_agent_profile_runtime_no_execution_guarantee(guarantee_id: str = "agent_profile_no_execution:v0.33.1", **kwargs: Any) -> AgentProfileRuntimeNoExecutionGuarantee:
    return AgentProfileRuntimeNoExecutionGuarantee(guarantee_id=guarantee_id, version=V0331_VERSION, **kwargs)


def build_v0331_readiness_report(report_id: str = "v0331_readiness_report", **kwargs: Any) -> V0331ReadinessReport:
    return V0331ReadinessReport(report_id=report_id, version=V0331_VERSION, **kwargs)


def resolve_agent_runtime_profile_from_input(
    resolution_input: AgentProfileResolutionInput,
    runtime_boundary: InternalRuntimeBoundary | None = None,
    profile_metadata: dict[str, Any] | None = None,
) -> AgentRuntimeProfile:
    if not isinstance(resolution_input, AgentProfileResolutionInput):
        raise TypeError("resolution_input must be AgentProfileResolutionInput")
    if runtime_boundary is not None and not isinstance(runtime_boundary, InternalRuntimeBoundary):
        raise TypeError("runtime_boundary must be InternalRuntimeBoundary or None")
    metadata = dict(profile_metadata or {})
    if _metadata_flag_true(metadata, {"file_load", "runtime_execution", "provider_call", "workspace_inspection"}):
        raise ValueError("profile_metadata must be in-memory profile metadata only")

    profile_kind = metadata.get("profile_kind", resolution_input.requested_profile_kind)
    mode_kind = metadata.get("mode_kind", resolution_input.requested_mode_kind)
    display_name = metadata.get("display_name", "Vera")
    description = metadata.get("description", "Resolved in-memory agent runtime profile contract.")
    source_refs = list(resolution_input.source_refs)

    persona = build_agent_profile_persona_projection(
        f"{resolution_input.resolution_input_id}:persona",
        profile_kind=profile_kind,
        display_name=display_name,
        source_refs=source_refs,
    )
    mode = build_agent_profile_mode_binding(
        f"{resolution_input.resolution_input_id}:mode",
        mode_kind=mode_kind,
        active_context_roles=list(resolution_input.requested_context_roles),
        source_refs=source_refs,
    )
    policy = build_agent_profile_policy_overlay(
        f"{resolution_input.resolution_input_id}:policy",
        source_refs=source_refs,
    )
    reference_context = build_agent_profile_reference_context(
        f"{resolution_input.resolution_input_id}:reference",
        source_refs=source_refs,
    )
    tools = build_agent_profile_tool_availability_view(
        f"{resolution_input.resolution_input_id}:tools",
        future_tool_names=["safe_readonly_tool_registry:v0.33.4"],
        source_refs=source_refs,
    )
    loadout = build_agent_runtime_loadout(
        f"{resolution_input.resolution_input_id}:loadout",
        persona,
        mode,
        policy,
        reference_context=reference_context,
        tool_availability_view=tools,
        runtime_boundary_id=runtime_boundary.boundary_id if runtime_boundary else resolution_input.runtime_boundary_id,
        source_refs=source_refs,
        ready_for_prompt_assembly=True,
        ready_for_session_runtime=True,
    )
    flags = build_agent_profile_runtime_flags(
        ready_for_v0332_prompt_assembly=True,
        ready_for_v0333_session_runtime=True,
    )
    return build_agent_runtime_profile(
        f"{resolution_input.resolution_input_id}:runtime_profile",
        loadout,
        flags,
        profile_kind=profile_kind,
        mode_kind=mode_kind,
        display_name=display_name,
        description=description,
        ready_for_v0332_prompt_assembly=True,
        ready_for_v0333_session_runtime=True,
        evidence_refs=[],
    )


def agent_profile_flags_preserve_runtime_false(flags: AgentProfileRuntimeFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in RUNTIME_FLAG_NAMES)


def agent_runtime_profile_is_not_active_session(profile: AgentRuntimeProfile) -> bool:
    return (
        profile.ready_for_execution is False
        and profile.active_session is False
        and agent_profile_flags_preserve_runtime_false(profile.runtime_flags)
    )


def agent_reference_context_preserves_no_file_access(context: AgentProfileReferenceContext) -> bool:
    return (
        context.ready_for_reference_file_access is False
        and context.ready_for_reference_code_execution is False
        and context.ready_for_reference_import is False
        and context.ready_for_reference_dependency_install is False
        and context.file_access is False
        and context.path_refs_only is True
    )


def agent_profile_resolution_report_is_not_runtime(report: AgentProfileResolutionReport) -> bool:
    return report.ready_for_execution is False and report.runtime_execution is False


def v0331_readiness_report_is_not_runtime_ready(report: V0331ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in RUNTIME_FLAG_NAMES) and report.runtime_enablement is False
