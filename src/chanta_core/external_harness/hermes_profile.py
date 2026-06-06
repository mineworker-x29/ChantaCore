from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .profiles import _metadata_flag_true, _require_non_blank, _validate_object_list, _validate_string_list
from .reference_corpus import ReferenceFileInventoryEntry


V0323_VERSION = "v0.32.3"
V0323_RELEASE_NAME = "v0.32.3 Hermes-style Runtime Observation Profile"

DEFAULT_HERMES_PROHIBITED_RUNTIME_ACTIONS = [
    "Hermes execution",
    "Hermes runtime start",
    "reference code execution",
    "install",
    "import runtime",
    "profile activation",
    "memory access",
    "memory write",
    "mission installation",
    "mission execution",
    "skill registration",
    "skill execution",
    "tool registration",
    "tool invocation",
    "delegation execution",
    "provider routing",
    "provider invocation",
    "container runtime",
    "approval execution",
    "network",
    "credential",
    "secret file read",
    "command",
    "registry mutation",
    "OCEL emission",
]

HIGH_RISK_CAPABILITIES = {
    "activate_profile",
    "read_memory",
    "write_memory",
    "install_mission",
    "execute_mission",
    "register_skill",
    "execute_skill",
    "register_tool",
    "invoke_tool",
    "delegate_agent",
    "route_provider",
    "invoke_provider",
    "start_runtime",
    "start_container",
    "grant_approval",
    "emit_ocel_trace",
    "access_private_data",
    "use_credential",
    "access_network",
    "execute_command",
}


class HermesHarnessSurfaceKind(StrEnum):
    PROFILE_SURFACE = "profile_surface"
    MEMORY_SURFACE = "memory_surface"
    MISSION_SURFACE = "mission_surface"
    SKILL_SURFACE = "skill_surface"
    TOOL_SURFACE = "tool_surface"
    DELEGATION_SURFACE = "delegation_surface"
    PROVIDER_ROUTING_SURFACE = "provider_routing_surface"
    RUNTIME_SURFACE = "runtime_surface"
    CONTAINER_ISOLATION_SURFACE = "container_isolation_surface"
    AUTHORIZATION_SURFACE = "authorization_surface"
    APPROVAL_BOUNDARY_SURFACE = "approval_boundary_surface"
    AUDIT_BOUNDARY_SURFACE = "audit_boundary_surface"
    CONFIGURATION_MANIFEST_SURFACE = "configuration_manifest_surface"
    DEPENDENCY_MANIFEST_SURFACE = "dependency_manifest_surface"
    RESULT_ENVELOPE_SURFACE = "result_envelope_surface"
    OCEL_TRACE_SURFACE = "ocel_trace_surface"
    PRIVATE_DATA_SURFACE = "private_data_surface"
    CREDENTIAL_SURFACE = "credential_surface"
    NETWORK_SURFACE = "network_surface"
    COMMAND_EXECUTION_SURFACE = "command_execution_surface"
    GATEWAY_SURFACE = "gateway_surface"
    UNKNOWN = "unknown"


class HermesObservationFocusKind(StrEnum):
    PROFILE_MODEL = "profile_model"
    MEMORY_MODEL = "memory_model"
    MISSION_MODEL = "mission_model"
    SKILL_MODEL = "skill_model"
    TOOL_MODEL = "tool_model"
    DELEGATION_MODEL = "delegation_model"
    PROVIDER_ROUTING_MODEL = "provider_routing_model"
    RUNTIME_MODEL = "runtime_model"
    CONTAINER_ISOLATION_BOUNDARY = "container_isolation_boundary"
    AUTHORIZATION_BOUNDARY = "authorization_boundary"
    APPROVAL_BOUNDARY = "approval_boundary"
    AUDIT_BOUNDARY = "audit_boundary"
    CONFIGURATION_MANIFEST = "configuration_manifest"
    DEPENDENCY_MANIFEST = "dependency_manifest"
    RESULT_ENVELOPE = "result_envelope"
    OCEL_TRACE_RELEVANCE = "ocel_trace_relevance"
    PRIVATE_DATA_BOUNDARY = "private_data_boundary"
    CREDENTIAL_BOUNDARY = "credential_boundary"
    NETWORK_BOUNDARY = "network_boundary"
    COMMAND_BOUNDARY = "command_boundary"
    GATEWAY_BOUNDARY = "gateway_boundary"
    DIGESTION_RELEVANCE = "digestion_relevance"
    DOMINION_RELEVANCE = "dominion_relevance"
    UNKNOWN = "unknown"


class HermesCapabilityKind(StrEnum):
    DEFINE_PROFILE = "define_profile"
    ACTIVATE_PROFILE = "activate_profile"
    READ_MEMORY = "read_memory"
    WRITE_MEMORY = "write_memory"
    DEFINE_MISSION = "define_mission"
    INSTALL_MISSION = "install_mission"
    EXECUTE_MISSION = "execute_mission"
    DEFINE_SKILL = "define_skill"
    REGISTER_SKILL = "register_skill"
    EXECUTE_SKILL = "execute_skill"
    DEFINE_TOOL = "define_tool"
    REGISTER_TOOL = "register_tool"
    INVOKE_TOOL = "invoke_tool"
    DELEGATE_AGENT = "delegate_agent"
    ROUTE_PROVIDER = "route_provider"
    INVOKE_PROVIDER = "invoke_provider"
    START_RUNTIME = "start_runtime"
    START_CONTAINER = "start_container"
    ENFORCE_AUTHORIZATION = "enforce_authorization"
    REQUEST_APPROVAL = "request_approval"
    GRANT_APPROVAL = "grant_approval"
    RECORD_AUDIT = "record_audit"
    EMIT_RESULT_ENVELOPE = "emit_result_envelope"
    EMIT_OCEL_TRACE = "emit_ocel_trace"
    ACCESS_PRIVATE_DATA = "access_private_data"
    USE_CREDENTIAL = "use_credential"
    ACCESS_NETWORK = "access_network"
    EXECUTE_COMMAND = "execute_command"
    UNKNOWN = "unknown"


class HermesRiskSignalKind(StrEnum):
    PROFILE_ACTIVATION_RISK = "profile_activation_risk"
    MEMORY_ACCESS_RISK = "memory_access_risk"
    MEMORY_MUTATION_RISK = "memory_mutation_risk"
    MISSION_INSTALLATION_RISK = "mission_installation_risk"
    MISSION_EXECUTION_RISK = "mission_execution_risk"
    SKILL_REGISTRATION_RISK = "skill_registration_risk"
    SKILL_EXECUTION_RISK = "skill_execution_risk"
    TOOL_REGISTRATION_RISK = "tool_registration_risk"
    TOOL_INVOCATION_RISK = "tool_invocation_risk"
    DELEGATION_EXECUTION_RISK = "delegation_execution_risk"
    PROVIDER_ROUTING_RISK = "provider_routing_risk"
    PROVIDER_INVOCATION_RISK = "provider_invocation_risk"
    RUNTIME_START_RISK = "runtime_start_risk"
    CONTAINER_RUNTIME_RISK = "container_runtime_risk"
    AUTHORIZATION_BYPASS_RISK = "authorization_bypass_risk"
    APPROVAL_BYPASS_RISK = "approval_bypass_risk"
    AUDIT_GAP_RISK = "audit_gap_risk"
    PRIVATE_DATA_EXPOSURE_RISK = "private_data_exposure_risk"
    CREDENTIAL_ACCESS_RISK = "credential_access_risk"
    NETWORK_ACCESS_RISK = "network_access_risk"
    COMMAND_EXECUTION_RISK = "command_execution_risk"
    GATEWAY_CONTROL_RISK = "gateway_control_risk"
    RAW_OUTPUT_PERSISTENCE_RISK = "raw_output_persistence_risk"
    OCEL_EMISSION_RISK = "ocel_emission_risk"
    UNKNOWN = "unknown"


class HermesObservationStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    OBSERVED = "observed"
    OBSERVED_WITH_GAPS = "observed_with_gaps"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class HermesEvidenceQuality(StrEnum):
    UNKNOWN = "unknown"
    NONE = "none"
    WEAK = "weak"
    PARTIAL = "partial"
    SUFFICIENT_FOR_STATIC_OBSERVATION = "sufficient_for_static_observation"
    SUFFICIENT_FOR_PROFILE = "sufficient_for_profile"
    SUFFICIENT_FOR_MANIFEST_EXTRACTION_REVIEW = "sufficient_for_manifest_extraction_review"
    CONFLICTING = "conflicting"
    BLOCKED = "blocked"


def _validate_version_includes_v0323(version: str) -> None:
    _require_non_blank("version", version)
    if V0323_VERSION not in version:
        raise ValueError("version must include v0.32.3")


def _validate_kind_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _validate_default_prohibitions(name: str, values: list[str]) -> None:
    _validate_string_list(name, values)
    missing = set(DEFAULT_HERMES_PROHIBITED_RUNTIME_ACTIONS) - set(values)
    if missing:
        raise ValueError(f"{name} missing v0.32.3 prohibitions: {sorted(missing)}")


def _capability_is_high_risk(value: HermesCapabilityKind | str) -> bool:
    return HermesCapabilityKind(value).value in HIGH_RISK_CAPABILITIES


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.32.3")


@dataclass(frozen=True)
class HermesReferenceSourceRef:
    source_ref_id: str
    reference_source_id: str | None = None
    reference_inventory_id: str | None = None
    reference_entry_ids: list[str] = field(default_factory=list)
    local_path_ref: str | None = None
    source_label: str = "Hermes-style static reference"
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        _require_non_blank("source_label", self.source_label)
        _validate_string_list("reference_entry_ids", self.reference_entry_ids)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"source_fetch", "execution"}):
            raise ValueError("HermesReferenceSourceRef is not source fetch or execution")

    @property
    def source_fetch(self) -> bool:
        return False

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class HermesSurfaceObservation:
    observation_id: str
    surface_kind: HermesHarnessSurfaceKind | str
    focus_kind: HermesObservationFocusKind | str
    capability_kind: HermesCapabilityKind | str
    title: str
    summary: str
    source_refs: list[HermesReferenceSourceRef] = field(default_factory=list)
    evidence_quality: HermesEvidenceQuality | str = HermesEvidenceQuality.UNKNOWN
    risk_signal_kinds: list[HermesRiskSignalKind | str] = field(default_factory=list)
    boundary_notes: list[str] = field(default_factory=list)
    prohibited_runtime_actions: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("observation_id", self.observation_id)
        HermesHarnessSurfaceKind(self.surface_kind)
        HermesObservationFocusKind(self.focus_kind)
        capability = HermesCapabilityKind(self.capability_kind)
        _require_non_blank("title", self.title)
        _require_non_blank("summary", self.summary)
        _validate_object_list("source_refs", self.source_refs, HermesReferenceSourceRef)
        HermesEvidenceQuality(self.evidence_quality)
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, HermesRiskSignalKind)
        for name in ("boundary_notes", "prohibited_runtime_actions", "assumptions", "limitations"):
            _validate_string_list(name, getattr(self, name))
        if capability.value in HIGH_RISK_CAPABILITIES and not self.prohibited_runtime_actions:
            raise ValueError("high-risk capabilities require prohibited_runtime_actions")
        if _metadata_flag_true(self.metadata, {"permission", "runtime_surface"}):
            raise ValueError("HermesSurfaceObservation is not permission")

    @property
    def permission(self) -> bool:
        return False


@dataclass(frozen=True)
class HermesProfileSurfaceObservation:
    profile_observation_id: str
    source_refs: list[HermesReferenceSourceRef] = field(default_factory=list)
    possible_profile_paths: list[str] = field(default_factory=list)
    possible_profile_config_paths: list[str] = field(default_factory=list)
    declared_profile_names: list[str] = field(default_factory=list)
    profile_activation_risk_detected: bool = False
    private_data_risk_detected: bool = False
    risk_signal_kinds: list[HermesRiskSignalKind | str] = field(default_factory=list)
    ready_for_profile_activation: bool = False
    ready_for_private_data_access: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("profile_observation_id", self.profile_observation_id)
        _validate_object_list("source_refs", self.source_refs, HermesReferenceSourceRef)
        for name in ("possible_profile_paths", "possible_profile_config_paths", "declared_profile_names"):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, HermesRiskSignalKind)
        _validate_false(self, ("ready_for_profile_activation", "ready_for_private_data_access", "ready_for_execution"))

    @property
    def profile_activation(self) -> bool:
        return False


@dataclass(frozen=True)
class HermesMemorySurfaceObservation:
    memory_observation_id: str
    source_refs: list[HermesReferenceSourceRef] = field(default_factory=list)
    possible_memory_schema_paths: list[str] = field(default_factory=list)
    possible_memory_store_paths: list[str] = field(default_factory=list)
    possible_memory_writer_paths: list[str] = field(default_factory=list)
    declared_memory_names: list[str] = field(default_factory=list)
    memory_access_risk_detected: bool = False
    memory_mutation_risk_detected: bool = False
    private_data_risk_detected: bool = False
    risk_signal_kinds: list[HermesRiskSignalKind | str] = field(default_factory=list)
    ready_for_memory_access: bool = False
    ready_for_memory_write: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("memory_observation_id", self.memory_observation_id)
        _validate_object_list("source_refs", self.source_refs, HermesReferenceSourceRef)
        for name in ("possible_memory_schema_paths", "possible_memory_store_paths", "possible_memory_writer_paths", "declared_memory_names"):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, HermesRiskSignalKind)
        _validate_false(self, ("ready_for_memory_access", "ready_for_memory_write", "ready_for_memory_mutation", "ready_for_execution"))

    @property
    def memory_access_or_mutation(self) -> bool:
        return False


@dataclass(frozen=True)
class HermesMissionSurfaceObservation:
    mission_observation_id: str
    source_refs: list[HermesReferenceSourceRef] = field(default_factory=list)
    possible_mission_manifest_paths: list[str] = field(default_factory=list)
    possible_mission_runtime_paths: list[str] = field(default_factory=list)
    possible_scheduler_paths: list[str] = field(default_factory=list)
    declared_mission_names: list[str] = field(default_factory=list)
    mission_installation_risk_detected: bool = False
    mission_execution_risk_detected: bool = False
    schedule_trigger_risk_detected: bool = False
    risk_signal_kinds: list[HermesRiskSignalKind | str] = field(default_factory=list)
    ready_for_mission_installation: bool = False
    ready_for_mission_execution: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("mission_observation_id", self.mission_observation_id)
        _validate_object_list("source_refs", self.source_refs, HermesReferenceSourceRef)
        for name in ("possible_mission_manifest_paths", "possible_mission_runtime_paths", "possible_scheduler_paths", "declared_mission_names"):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, HermesRiskSignalKind)
        _validate_false(self, ("ready_for_mission_installation", "ready_for_mission_execution", "ready_for_execution"))

    @property
    def mission_install_or_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class HermesSkillSurfaceObservation:
    skill_observation_id: str
    source_refs: list[HermesReferenceSourceRef] = field(default_factory=list)
    possible_skill_manifest_paths: list[str] = field(default_factory=list)
    possible_skill_registry_paths: list[str] = field(default_factory=list)
    possible_skill_runtime_paths: list[str] = field(default_factory=list)
    declared_skill_names: list[str] = field(default_factory=list)
    skill_registration_risk_detected: bool = False
    skill_execution_risk_detected: bool = False
    risk_signal_kinds: list[HermesRiskSignalKind | str] = field(default_factory=list)
    ready_for_skill_registration: bool = False
    ready_for_skill_execution: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("skill_observation_id", self.skill_observation_id)
        _validate_object_list("source_refs", self.source_refs, HermesReferenceSourceRef)
        for name in ("possible_skill_manifest_paths", "possible_skill_registry_paths", "possible_skill_runtime_paths", "declared_skill_names"):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, HermesRiskSignalKind)
        _validate_false(self, ("ready_for_skill_registration", "ready_for_skill_execution", "ready_for_execution"))

    @property
    def skill_registration_or_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class HermesToolSurfaceObservation:
    tool_observation_id: str
    source_refs: list[HermesReferenceSourceRef] = field(default_factory=list)
    possible_tool_manifest_paths: list[str] = field(default_factory=list)
    possible_tool_registry_paths: list[str] = field(default_factory=list)
    possible_tool_runtime_paths: list[str] = field(default_factory=list)
    declared_tool_names: list[str] = field(default_factory=list)
    tool_registration_risk_detected: bool = False
    tool_invocation_risk_detected: bool = False
    command_execution_risk_detected: bool = False
    risk_signal_kinds: list[HermesRiskSignalKind | str] = field(default_factory=list)
    ready_for_tool_registration: bool = False
    ready_for_tool_invocation: bool = False
    ready_for_command_execution: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("tool_observation_id", self.tool_observation_id)
        _validate_object_list("source_refs", self.source_refs, HermesReferenceSourceRef)
        for name in ("possible_tool_manifest_paths", "possible_tool_registry_paths", "possible_tool_runtime_paths", "declared_tool_names"):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, HermesRiskSignalKind)
        _validate_false(self, ("ready_for_tool_registration", "ready_for_tool_invocation", "ready_for_command_execution", "ready_for_execution"))

    @property
    def tool_registration_or_invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class HermesDelegationBoundaryObservation:
    delegation_boundary_id: str
    source_refs: list[HermesReferenceSourceRef] = field(default_factory=list)
    possible_delegation_manifest_paths: list[str] = field(default_factory=list)
    possible_delegation_runtime_paths: list[str] = field(default_factory=list)
    possible_agent_route_paths: list[str] = field(default_factory=list)
    declared_delegation_names: list[str] = field(default_factory=list)
    delegation_execution_risk_detected: bool = False
    external_agent_risk_detected: bool = False
    risk_signal_kinds: list[HermesRiskSignalKind | str] = field(default_factory=list)
    ready_for_delegation_execution: bool = False
    ready_for_external_agent_runtime: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("delegation_boundary_id", self.delegation_boundary_id)
        _validate_object_list("source_refs", self.source_refs, HermesReferenceSourceRef)
        for name in ("possible_delegation_manifest_paths", "possible_delegation_runtime_paths", "possible_agent_route_paths", "declared_delegation_names"):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, HermesRiskSignalKind)
        _validate_false(self, ("ready_for_delegation_execution", "ready_for_external_agent_runtime", "ready_for_execution"))

    @property
    def delegation_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class HermesProviderRoutingBoundaryObservation:
    provider_routing_boundary_id: str
    source_refs: list[HermesReferenceSourceRef] = field(default_factory=list)
    possible_provider_config_paths: list[str] = field(default_factory=list)
    possible_provider_router_paths: list[str] = field(default_factory=list)
    declared_provider_names: list[str] = field(default_factory=list)
    provider_routing_risk_detected: bool = False
    provider_invocation_risk_detected: bool = False
    network_risk_detected: bool = False
    credential_risk_detected: bool = False
    risk_signal_kinds: list[HermesRiskSignalKind | str] = field(default_factory=list)
    ready_for_provider_routing: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("provider_routing_boundary_id", self.provider_routing_boundary_id)
        _validate_object_list("source_refs", self.source_refs, HermesReferenceSourceRef)
        for name in ("possible_provider_config_paths", "possible_provider_router_paths", "declared_provider_names"):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, HermesRiskSignalKind)
        _validate_false(self, ("ready_for_provider_routing", "ready_for_provider_invocation", "ready_for_network_access", "ready_for_credential_access", "ready_for_execution"))

    @property
    def provider_invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class HermesRuntimeIsolationBoundaryObservation:
    runtime_isolation_boundary_id: str
    source_refs: list[HermesReferenceSourceRef] = field(default_factory=list)
    possible_runtime_paths: list[str] = field(default_factory=list)
    possible_container_paths: list[str] = field(default_factory=list)
    possible_isolation_config_paths: list[str] = field(default_factory=list)
    runtime_start_risk_detected: bool = False
    container_runtime_risk_detected: bool = False
    command_execution_risk_detected: bool = False
    risk_signal_kinds: list[HermesRiskSignalKind | str] = field(default_factory=list)
    ready_for_hermes_runtime: bool = False
    ready_for_container_runtime: bool = False
    ready_for_command_execution: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("runtime_isolation_boundary_id", self.runtime_isolation_boundary_id)
        _validate_object_list("source_refs", self.source_refs, HermesReferenceSourceRef)
        for name in ("possible_runtime_paths", "possible_container_paths", "possible_isolation_config_paths"):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, HermesRiskSignalKind)
        _validate_false(self, ("ready_for_hermes_runtime", "ready_for_container_runtime", "ready_for_command_execution", "ready_for_execution"))

    @property
    def runtime_or_container_start(self) -> bool:
        return False


@dataclass(frozen=True)
class HermesApprovalAuditBoundaryRequirement:
    approval_audit_boundary_id: str
    source_refs: list[HermesReferenceSourceRef] = field(default_factory=list)
    possible_approval_paths: list[str] = field(default_factory=list)
    possible_authorization_paths: list[str] = field(default_factory=list)
    possible_audit_paths: list[str] = field(default_factory=list)
    approval_required_for_surfaces: list[HermesHarnessSurfaceKind | str] = field(default_factory=list)
    audit_required_for_surfaces: list[HermesHarnessSurfaceKind | str] = field(default_factory=list)
    authorization_gap_detected: bool = False
    approval_gap_detected: bool = False
    audit_gap_detected: bool = False
    risk_signal_kinds: list[HermesRiskSignalKind | str] = field(default_factory=list)
    approval_granted: bool = False
    ready_for_approval_execution: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("approval_audit_boundary_id", self.approval_audit_boundary_id)
        _validate_object_list("source_refs", self.source_refs, HermesReferenceSourceRef)
        for name in ("possible_approval_paths", "possible_authorization_paths", "possible_audit_paths"):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("approval_required_for_surfaces", self.approval_required_for_surfaces, HermesHarnessSurfaceKind)
        _validate_kind_list("audit_required_for_surfaces", self.audit_required_for_surfaces, HermesHarnessSurfaceKind)
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, HermesRiskSignalKind)
        _validate_false(self, ("approval_granted", "ready_for_approval_execution", "ready_for_execution"))

    @property
    def approval_or_audit_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class HermesConfigManifestObservation:
    config_manifest_observation_id: str
    source_refs: list[HermesReferenceSourceRef] = field(default_factory=list)
    possible_package_manifest_paths: list[str] = field(default_factory=list)
    possible_config_paths: list[str] = field(default_factory=list)
    possible_profile_manifest_paths: list[str] = field(default_factory=list)
    possible_memory_manifest_paths: list[str] = field(default_factory=list)
    possible_mission_manifest_paths: list[str] = field(default_factory=list)
    possible_skill_manifest_paths: list[str] = field(default_factory=list)
    possible_tool_manifest_paths: list[str] = field(default_factory=list)
    possible_script_entries: list[str] = field(default_factory=list)
    possible_dependency_entries: list[str] = field(default_factory=list)
    risk_signal_kinds: list[HermesRiskSignalKind | str] = field(default_factory=list)
    ready_for_dependency_install: bool = False
    ready_for_script_execution: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("config_manifest_observation_id", self.config_manifest_observation_id)
        _validate_object_list("source_refs", self.source_refs, HermesReferenceSourceRef)
        for name in (
            "possible_package_manifest_paths",
            "possible_config_paths",
            "possible_profile_manifest_paths",
            "possible_memory_manifest_paths",
            "possible_mission_manifest_paths",
            "possible_skill_manifest_paths",
            "possible_tool_manifest_paths",
            "possible_script_entries",
            "possible_dependency_entries",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, HermesRiskSignalKind)
        _validate_false(self, ("ready_for_dependency_install", "ready_for_script_execution", "ready_for_execution"))

    @property
    def dependency_install(self) -> bool:
        return False


@dataclass(frozen=True)
class HermesStaticObservationInput:
    hermes_input_id: str
    external_harness_profile_id: str | None = None
    reference_corpus_snapshot_id: str | None = None
    reference_inventory_ids: list[str] = field(default_factory=list)
    reference_source_refs: list[HermesReferenceSourceRef] = field(default_factory=list)
    requested_focus: list[HermesObservationFocusKind | str] = field(default_factory=list)
    task_summary: str = "Hermes-style static observation contract input."
    source_version: str = V0323_VERSION
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_HERMES_PROHIBITED_RUNTIME_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("hermes_input_id", self.hermes_input_id)
        _validate_string_list("reference_inventory_ids", self.reference_inventory_ids)
        _validate_object_list("reference_source_refs", self.reference_source_refs, HermesReferenceSourceRef)
        _validate_kind_list("requested_focus", self.requested_focus, HermesObservationFocusKind)
        _require_non_blank("task_summary", self.task_summary)
        _require_non_blank("source_version", self.source_version)
        _validate_default_prohibitions("prohibited_runtime_actions", self.prohibited_runtime_actions)
        if _metadata_flag_true(self.metadata, {"execution_request", "runtime_input"}):
            raise ValueError("HermesStaticObservationInput is not execution request")

    @property
    def execution_request(self) -> bool:
        return False


@dataclass(frozen=True)
class HermesObservationFinding:
    finding_id: str
    hermes_input_id: str
    surface_kind: HermesHarnessSurfaceKind | str
    capability_kind: HermesCapabilityKind | str
    summary: str
    source_ref_ids: list[str] = field(default_factory=list)
    risk_signal_kinds: list[HermesRiskSignalKind | str] = field(default_factory=list)
    evidence_quality: HermesEvidenceQuality | str = HermesEvidenceQuality.UNKNOWN
    digestion_relevance: bool = False
    dominion_relevance: bool = False
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("hermes_input_id", self.hermes_input_id)
        HermesHarnessSurfaceKind(self.surface_kind)
        HermesCapabilityKind(self.capability_kind)
        _require_non_blank("summary", self.summary)
        _validate_string_list("source_ref_ids", self.source_ref_ids)
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, HermesRiskSignalKind)
        HermesEvidenceQuality(self.evidence_quality)
        _validate_string_list("assumptions", self.assumptions)
        _validate_string_list("limitations", self.limitations)
        if _metadata_flag_true(self.metadata, {"permission", "internal_skill_candidate", "dominion_target"}):
            raise ValueError("HermesObservationFinding is not permission, InternalSkillCandidate, or DominionTarget")

    @property
    def digestion_candidate(self) -> bool:
        return False

    @property
    def dominion_target(self) -> bool:
        return False


@dataclass(frozen=True)
class HermesRiskSignal:
    risk_signal_id: str
    finding_id: str | None
    signal_kind: HermesRiskSignalKind | str
    severity: str
    summary: str
    source_ref_ids: list[str] = field(default_factory=list)
    recommended_boundary: str | None = None
    routes_to_dominion_hint: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_signal_id", self.risk_signal_id)
        HermesRiskSignalKind(self.signal_kind)
        _require_non_blank("severity", self.severity)
        _require_non_blank("summary", self.summary)
        _validate_string_list("source_ref_ids", self.source_ref_ids)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.severity.lower() in {"high", "critical"} and not self.recommended_boundary and not self.routes_to_dominion_hint:
            raise ValueError("high or critical severity requires recommended_boundary or routes_to_dominion_hint")
        if _metadata_flag_true(self.metadata, {"authority_grant", "permission"}):
            raise ValueError("HermesRiskSignal does not grant authority")

    @property
    def authority_grant(self) -> bool:
        return False


@dataclass(frozen=True)
class HermesDigestionHint:
    digestion_hint_id: str
    finding_ids: list[str]
    candidate_focus: HermesObservationFocusKind | str
    suggested_internal_candidate_kind: str | None
    summary: str
    evidence_refs: list[str] = field(default_factory=list)
    ready_for_v0324_manifest_extraction: bool = True
    ready_for_v0326_digestion_candidate_generation: bool = True
    ready_for_internal_candidate_creation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("digestion_hint_id", self.digestion_hint_id)
        _validate_string_list("finding_ids", self.finding_ids)
        HermesObservationFocusKind(self.candidate_focus)
        _require_non_blank("summary", self.summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, ("ready_for_internal_candidate_creation", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"internal_skill_candidate", "execution_ready"}):
            raise ValueError("HermesDigestionHint is not InternalSkillCandidate")

    @property
    def internal_skill_candidate(self) -> bool:
        return False


@dataclass(frozen=True)
class HermesDominionHint:
    dominion_hint_id: str
    finding_ids: list[str]
    risk_signal_ids: list[str]
    suggested_boundary: str
    summary: str
    evidence_refs: list[str] = field(default_factory=list)
    ready_for_v0328_dominion_candidate_emitter: bool = True
    ready_for_dominion_target_creation: bool = False
    ready_for_external_control: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("dominion_hint_id", self.dominion_hint_id)
        _validate_string_list("finding_ids", self.finding_ids)
        _validate_string_list("risk_signal_ids", self.risk_signal_ids)
        _require_non_blank("suggested_boundary", self.suggested_boundary)
        _require_non_blank("summary", self.summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, ("ready_for_dominion_target_creation", "ready_for_external_control", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"dominion_target", "external_control"}):
            raise ValueError("HermesDominionHint is not DominionTarget")

    @property
    def dominion_target(self) -> bool:
        return False


@dataclass(frozen=True)
class HermesStyleObservationProfile:
    hermes_profile_id: str
    base_harness_profile_id: str | None
    display_name: str
    description: str
    source_refs: list[HermesReferenceSourceRef] = field(default_factory=list)
    observed_surfaces: list[HermesSurfaceObservation] = field(default_factory=list)
    profile_surface: HermesProfileSurfaceObservation | None = None
    memory_surface: HermesMemorySurfaceObservation | None = None
    mission_surface: HermesMissionSurfaceObservation | None = None
    skill_surface: HermesSkillSurfaceObservation | None = None
    tool_surface: HermesToolSurfaceObservation | None = None
    delegation_boundary: HermesDelegationBoundaryObservation | None = None
    provider_routing_boundary: HermesProviderRoutingBoundaryObservation | None = None
    runtime_isolation_boundary: HermesRuntimeIsolationBoundaryObservation | None = None
    approval_audit_boundary: HermesApprovalAuditBoundaryRequirement | None = None
    config_manifest_observation: HermesConfigManifestObservation | None = None
    status: HermesObservationStatus | str = HermesObservationStatus.OBSERVED_WITH_GAPS
    gaps: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    ready_for_v0324_manifest_extraction: bool = True
    ready_for_execution: bool = False
    ready_for_hermes_execution: bool = False
    ready_for_hermes_runtime: bool = False
    ready_for_reference_code_execution: bool = False
    ready_for_profile_activation: bool = False
    ready_for_memory_access: bool = False
    ready_for_memory_write: bool = False
    ready_for_mission_execution: bool = False
    ready_for_skill_execution: bool = False
    ready_for_tool_invocation: bool = False
    ready_for_delegation_execution: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("hermes_profile_id", self.hermes_profile_id)
        _require_non_blank("display_name", self.display_name)
        _require_non_blank("description", self.description)
        _validate_object_list("source_refs", self.source_refs, HermesReferenceSourceRef)
        _validate_object_list("observed_surfaces", self.observed_surfaces, HermesSurfaceObservation)
        HermesObservationStatus(self.status)
        _validate_string_list("gaps", self.gaps)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(
            self,
            (
                "ready_for_execution",
                "ready_for_hermes_execution",
                "ready_for_hermes_runtime",
                "ready_for_reference_code_execution",
                "ready_for_profile_activation",
                "ready_for_memory_access",
                "ready_for_memory_write",
                "ready_for_mission_execution",
                "ready_for_skill_execution",
                "ready_for_tool_invocation",
                "ready_for_delegation_execution",
                "ready_for_provider_invocation",
                "ready_for_network_access",
                "ready_for_credential_access",
            ),
        )
        if _metadata_flag_true(self.metadata, {"hermes_runtime", "execution_ready"}):
            raise ValueError("HermesStyleObservationProfile is not Hermes runtime")

    @property
    def hermes_runtime(self) -> bool:
        return False


@dataclass(frozen=True)
class HermesObservationOutput:
    hermes_output_id: str
    hermes_input_id: str
    hermes_profile: HermesStyleObservationProfile
    findings: list[HermesObservationFinding] = field(default_factory=list)
    risk_signals: list[HermesRiskSignal] = field(default_factory=list)
    digestion_hints: list[HermesDigestionHint] = field(default_factory=list)
    dominion_hints: list[HermesDominionHint] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    ready_for_v0324_manifest_extraction: bool = True
    ready_for_v0325_risk_classification: bool = True
    ready_for_execution: bool = False
    ready_for_hermes_execution: bool = False
    ready_for_hermes_runtime: bool = False
    ready_for_memory_access: bool = False
    ready_for_mission_execution: bool = False
    ready_for_skill_execution: bool = False
    ready_for_delegation_execution: bool = False
    ready_for_provider_invocation: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("hermes_output_id", self.hermes_output_id)
        _require_non_blank("hermes_input_id", self.hermes_input_id)
        if not isinstance(self.hermes_profile, HermesStyleObservationProfile):
            raise TypeError("hermes_profile must be HermesStyleObservationProfile")
        _validate_object_list("findings", self.findings, HermesObservationFinding)
        _validate_object_list("risk_signals", self.risk_signals, HermesRiskSignal)
        _validate_object_list("digestion_hints", self.digestion_hints, HermesDigestionHint)
        _validate_object_list("dominion_hints", self.dominion_hints, HermesDominionHint)
        _validate_string_list("gaps", self.gaps)
        _validate_string_list("blocked_reasons", self.blocked_reasons)
        _validate_false(self, ("ready_for_execution", "ready_for_hermes_execution", "ready_for_hermes_runtime", "ready_for_memory_access", "ready_for_mission_execution", "ready_for_skill_execution", "ready_for_delegation_execution", "ready_for_provider_invocation"))
        if _metadata_flag_true(self.metadata, {"manifest_extraction_execution", "digestion_candidate", "dominion_target"}):
            raise ValueError("HermesObservationOutput is not runtime, digestion candidate, or dominion target")


@dataclass(frozen=True)
class HermesObservationRunPreview:
    run_preview_id: str
    hermes_input_id: str | None = None
    planned_steps: list[str] = field(default_factory=list)
    expected_artifacts: list[str] = field(default_factory=list)
    explicitly_not_performed: list[str] = field(default_factory=list)
    no_hermes_execution_guarantee: bool = True
    no_hermes_runtime_start_guarantee: bool = True
    no_reference_code_execution_guarantee: bool = True
    no_install_guarantee: bool = True
    no_import_runtime_guarantee: bool = True
    no_profile_activation_guarantee: bool = True
    no_memory_access_guarantee: bool = True
    no_memory_write_guarantee: bool = True
    no_mission_execution_guarantee: bool = True
    no_skill_execution_guarantee: bool = True
    no_tool_invocation_guarantee: bool = True
    no_delegation_execution_guarantee: bool = True
    no_provider_invocation_guarantee: bool = True
    no_network_access_guarantee: bool = True
    no_credential_access_guarantee: bool = True
    no_command_execution_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        for name in (
            "no_hermes_execution_guarantee",
            "no_hermes_runtime_start_guarantee",
            "no_reference_code_execution_guarantee",
            "no_install_guarantee",
            "no_import_runtime_guarantee",
            "no_profile_activation_guarantee",
            "no_memory_access_guarantee",
            "no_memory_write_guarantee",
            "no_mission_execution_guarantee",
            "no_skill_execution_guarantee",
            "no_tool_invocation_guarantee",
            "no_delegation_execution_guarantee",
            "no_provider_invocation_guarantee",
            "no_network_access_guarantee",
            "no_credential_access_guarantee",
            "no_command_execution_guarantee",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.32.3")


@dataclass(frozen=True)
class HermesNoExecutionGuarantee:
    guarantee_id: str
    version: str
    no_hermes_execution: bool = True
    no_hermes_runtime_start: bool = True
    no_reference_code_execution: bool = True
    no_dependency_install: bool = True
    no_import_runtime: bool = True
    no_profile_activation: bool = True
    no_memory_access: bool = True
    no_memory_write: bool = True
    no_memory_mutation: bool = True
    no_mission_installation: bool = True
    no_mission_execution: bool = True
    no_skill_registration: bool = True
    no_skill_execution: bool = True
    no_tool_registration: bool = True
    no_tool_invocation: bool = True
    no_delegation_execution: bool = True
    no_provider_routing: bool = True
    no_provider_invocation: bool = True
    no_container_runtime: bool = True
    no_approval_execution: bool = True
    no_network_access: bool = True
    no_credential_access: bool = True
    no_secret_file_read: bool = True
    no_command_execution: bool = True
    no_registry_mutation: bool = True
    no_ocel_emission: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version_includes_v0323(self.version)
        for name in (
            "no_hermes_execution",
            "no_hermes_runtime_start",
            "no_reference_code_execution",
            "no_dependency_install",
            "no_import_runtime",
            "no_profile_activation",
            "no_memory_access",
            "no_memory_write",
            "no_memory_mutation",
            "no_mission_installation",
            "no_mission_execution",
            "no_skill_registration",
            "no_skill_execution",
            "no_tool_registration",
            "no_tool_invocation",
            "no_delegation_execution",
            "no_provider_routing",
            "no_provider_invocation",
            "no_container_runtime",
            "no_approval_execution",
            "no_network_access",
            "no_credential_access",
            "no_secret_file_read",
            "no_command_execution",
            "no_registry_mutation",
            "no_ocel_emission",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.32.3")
        _validate_string_list("evidence_refs", self.evidence_refs)


@dataclass(frozen=True)
class V0323ReadinessReport:
    report_id: str
    version: str
    hermes_profile_id: str | None
    hermes_output_id: str | None
    summary: str
    ready_for_v0324_manifest_extraction: bool = True
    ready_for_v0325_risk_classification: bool = True
    ready_for_execution: bool = False
    ready_for_hermes_execution: bool = False
    ready_for_hermes_runtime: bool = False
    ready_for_reference_code_execution: bool = False
    ready_for_profile_activation: bool = False
    ready_for_memory_access: bool = False
    ready_for_memory_write: bool = False
    ready_for_mission_execution: bool = False
    ready_for_skill_execution: bool = False
    ready_for_tool_invocation: bool = False
    ready_for_delegation_execution: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_HERMES_PROHIBITED_RUNTIME_ACTIONS))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0323(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(
            self,
            (
                "ready_for_execution",
                "ready_for_hermes_execution",
                "ready_for_hermes_runtime",
                "ready_for_reference_code_execution",
                "ready_for_profile_activation",
                "ready_for_memory_access",
                "ready_for_memory_write",
                "ready_for_mission_execution",
                "ready_for_skill_execution",
                "ready_for_tool_invocation",
                "ready_for_delegation_execution",
                "ready_for_provider_invocation",
                "ready_for_network_access",
                "ready_for_credential_access",
            ),
        )
        for name in ("completed_items", "blocked_items", "future_track_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_default_prohibitions("prohibited_until_later_gate", self.prohibited_until_later_gate)
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "execution_ready"}):
            raise ValueError("V0323ReadinessReport is not runtime enablement")


def build_hermes_reference_source_ref(source_ref_id: str, reference_source_id: str | None = None, reference_inventory_id: str | None = None, reference_entry_ids: list[str] | None = None, local_path_ref: str | None = None, source_label: str = "Hermes-style static reference", evidence_refs: list[str] | None = None, metadata: dict[str, Any] | None = None) -> HermesReferenceSourceRef:
    return HermesReferenceSourceRef(source_ref_id, reference_source_id, reference_inventory_id, list(reference_entry_ids or []), local_path_ref, source_label, list(evidence_refs or []), dict(metadata or {}))


def build_hermes_surface_observation(observation_id: str, surface_kind: HermesHarnessSurfaceKind | str, focus_kind: HermesObservationFocusKind | str, capability_kind: HermesCapabilityKind | str, title: str, summary: str, source_refs: list[HermesReferenceSourceRef] | None = None, evidence_quality: HermesEvidenceQuality | str = HermesEvidenceQuality.UNKNOWN, risk_signal_kinds: list[HermesRiskSignalKind | str] | None = None, boundary_notes: list[str] | None = None, prohibited_runtime_actions: list[str] | None = None, assumptions: list[str] | None = None, limitations: list[str] | None = None, metadata: dict[str, Any] | None = None) -> HermesSurfaceObservation:
    return HermesSurfaceObservation(
        observation_id=observation_id,
        surface_kind=surface_kind,
        focus_kind=focus_kind,
        capability_kind=capability_kind,
        title=title,
        summary=summary,
        source_refs=list(source_refs or []),
        evidence_quality=evidence_quality,
        risk_signal_kinds=list(risk_signal_kinds or []),
        boundary_notes=list(boundary_notes or []),
        prohibited_runtime_actions=list(prohibited_runtime_actions or (DEFAULT_HERMES_PROHIBITED_RUNTIME_ACTIONS if _capability_is_high_risk(capability_kind) else [])),
        assumptions=list(assumptions or []),
        limitations=list(limitations or []),
        metadata=dict(metadata or {}),
    )


def build_hermes_profile_surface_observation(profile_observation_id: str, source_refs: list[HermesReferenceSourceRef] | None = None, **kwargs: Any) -> HermesProfileSurfaceObservation:
    return HermesProfileSurfaceObservation(profile_observation_id=profile_observation_id, source_refs=list(source_refs or []), **kwargs)


def build_hermes_memory_surface_observation(memory_observation_id: str, source_refs: list[HermesReferenceSourceRef] | None = None, **kwargs: Any) -> HermesMemorySurfaceObservation:
    return HermesMemorySurfaceObservation(memory_observation_id=memory_observation_id, source_refs=list(source_refs or []), **kwargs)


def build_hermes_mission_surface_observation(mission_observation_id: str, source_refs: list[HermesReferenceSourceRef] | None = None, **kwargs: Any) -> HermesMissionSurfaceObservation:
    return HermesMissionSurfaceObservation(mission_observation_id=mission_observation_id, source_refs=list(source_refs or []), **kwargs)


def build_hermes_skill_surface_observation(skill_observation_id: str, source_refs: list[HermesReferenceSourceRef] | None = None, **kwargs: Any) -> HermesSkillSurfaceObservation:
    return HermesSkillSurfaceObservation(skill_observation_id=skill_observation_id, source_refs=list(source_refs or []), **kwargs)


def build_hermes_tool_surface_observation(tool_observation_id: str, source_refs: list[HermesReferenceSourceRef] | None = None, **kwargs: Any) -> HermesToolSurfaceObservation:
    return HermesToolSurfaceObservation(tool_observation_id=tool_observation_id, source_refs=list(source_refs or []), **kwargs)


def build_hermes_delegation_boundary_observation(delegation_boundary_id: str, source_refs: list[HermesReferenceSourceRef] | None = None, **kwargs: Any) -> HermesDelegationBoundaryObservation:
    return HermesDelegationBoundaryObservation(delegation_boundary_id=delegation_boundary_id, source_refs=list(source_refs or []), **kwargs)


def build_hermes_provider_routing_boundary_observation(provider_routing_boundary_id: str, source_refs: list[HermesReferenceSourceRef] | None = None, **kwargs: Any) -> HermesProviderRoutingBoundaryObservation:
    return HermesProviderRoutingBoundaryObservation(provider_routing_boundary_id=provider_routing_boundary_id, source_refs=list(source_refs or []), **kwargs)


def build_hermes_runtime_isolation_boundary_observation(runtime_isolation_boundary_id: str, source_refs: list[HermesReferenceSourceRef] | None = None, **kwargs: Any) -> HermesRuntimeIsolationBoundaryObservation:
    return HermesRuntimeIsolationBoundaryObservation(runtime_isolation_boundary_id=runtime_isolation_boundary_id, source_refs=list(source_refs or []), **kwargs)


def build_hermes_approval_audit_boundary_requirement(approval_audit_boundary_id: str, source_refs: list[HermesReferenceSourceRef] | None = None, **kwargs: Any) -> HermesApprovalAuditBoundaryRequirement:
    return HermesApprovalAuditBoundaryRequirement(approval_audit_boundary_id=approval_audit_boundary_id, source_refs=list(source_refs or []), **kwargs)


def build_hermes_config_manifest_observation(config_manifest_observation_id: str, source_refs: list[HermesReferenceSourceRef] | None = None, **kwargs: Any) -> HermesConfigManifestObservation:
    return HermesConfigManifestObservation(config_manifest_observation_id=config_manifest_observation_id, source_refs=list(source_refs or []), **kwargs)


def build_hermes_static_observation_input(hermes_input_id: str, **kwargs: Any) -> HermesStaticObservationInput:
    return HermesStaticObservationInput(hermes_input_id=hermes_input_id, **kwargs)


def build_hermes_observation_finding(finding_id: str, hermes_input_id: str, surface_kind: HermesHarnessSurfaceKind | str, capability_kind: HermesCapabilityKind | str, summary: str, **kwargs: Any) -> HermesObservationFinding:
    return HermesObservationFinding(finding_id=finding_id, hermes_input_id=hermes_input_id, surface_kind=surface_kind, capability_kind=capability_kind, summary=summary, **kwargs)


def build_hermes_risk_signal(risk_signal_id: str, signal_kind: HermesRiskSignalKind | str, severity: str, summary: str, finding_id: str | None = None, **kwargs: Any) -> HermesRiskSignal:
    return HermesRiskSignal(risk_signal_id=risk_signal_id, finding_id=finding_id, signal_kind=signal_kind, severity=severity, summary=summary, **kwargs)


def build_hermes_digestion_hint(digestion_hint_id: str, finding_ids: list[str], candidate_focus: HermesObservationFocusKind | str, summary: str, suggested_internal_candidate_kind: str | None = None, **kwargs: Any) -> HermesDigestionHint:
    return HermesDigestionHint(digestion_hint_id=digestion_hint_id, finding_ids=list(finding_ids), candidate_focus=candidate_focus, suggested_internal_candidate_kind=suggested_internal_candidate_kind, summary=summary, **kwargs)


def build_hermes_dominion_hint(dominion_hint_id: str, finding_ids: list[str], risk_signal_ids: list[str], suggested_boundary: str, summary: str, **kwargs: Any) -> HermesDominionHint:
    return HermesDominionHint(dominion_hint_id=dominion_hint_id, finding_ids=list(finding_ids), risk_signal_ids=list(risk_signal_ids), suggested_boundary=suggested_boundary, summary=summary, **kwargs)


def build_hermes_style_observation_profile(hermes_profile_id: str, display_name: str, description: str, base_harness_profile_id: str | None = None, **kwargs: Any) -> HermesStyleObservationProfile:
    return HermesStyleObservationProfile(hermes_profile_id=hermes_profile_id, base_harness_profile_id=base_harness_profile_id, display_name=display_name, description=description, **kwargs)


def build_hermes_observation_output(hermes_output_id: str, hermes_input_id: str, hermes_profile: HermesStyleObservationProfile, **kwargs: Any) -> HermesObservationOutput:
    return HermesObservationOutput(hermes_output_id=hermes_output_id, hermes_input_id=hermes_input_id, hermes_profile=hermes_profile, **kwargs)


def build_hermes_observation_run_preview(run_preview_id: str = "hermes_observation_run_preview:v0.32.3", **kwargs: Any) -> HermesObservationRunPreview:
    return HermesObservationRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_hermes_no_execution_guarantee(guarantee_id: str = "hermes_no_execution_guarantee:v0.32.3", evidence_refs: list[str] | None = None, metadata: dict[str, Any] | None = None) -> HermesNoExecutionGuarantee:
    return HermesNoExecutionGuarantee(guarantee_id=guarantee_id, version=V0323_VERSION, evidence_refs=list(evidence_refs or []), metadata=dict(metadata or {}))


def build_v0323_readiness_report(report_id: str = "v0323_readiness_report", hermes_profile_id: str | None = None, hermes_output_id: str | None = None, summary: str = "v0.32.3 is ready for manifest extraction and risk classification design-stage handoff only, not execution.", **kwargs: Any) -> V0323ReadinessReport:
    return V0323ReadinessReport(report_id=report_id, version=V0323_VERSION, hermes_profile_id=hermes_profile_id, hermes_output_id=hermes_output_id, summary=summary, **kwargs)


def classify_inventory_entry_as_hermes_surface(entry: ReferenceFileInventoryEntry) -> HermesHarnessSurfaceKind:
    name = entry.file_name.lower()
    path = entry.relative_path.lower()
    detected = (entry.detected_kind or "").lower()
    extension = entry.file_extension or ""
    if "profile" in path or "profile" in name:
        return HermesHarnessSurfaceKind.PROFILE_SURFACE
    if "memory" in path or "memory" in name:
        return HermesHarnessSurfaceKind.MEMORY_SURFACE
    if "mission" in path or "mission" in name:
        return HermesHarnessSurfaceKind.MISSION_SURFACE
    if "skill" in path or "skill" in name:
        return HermesHarnessSurfaceKind.SKILL_SURFACE
    if "tool" in path or "tool" in name:
        return HermesHarnessSurfaceKind.TOOL_SURFACE
    if "delegat" in path or "agent" in path:
        return HermesHarnessSurfaceKind.DELEGATION_SURFACE
    if "provider" in path or "model" in path or "router" in path or "route" in path:
        return HermesHarnessSurfaceKind.PROVIDER_ROUTING_SURFACE
    if "container" in path or "docker" in path or "isolation" in path:
        return HermesHarnessSurfaceKind.CONTAINER_ISOLATION_SURFACE
    if "runtime" in path:
        return HermesHarnessSurfaceKind.RUNTIME_SURFACE
    if "authorization" in path or "auth" in path:
        return HermesHarnessSurfaceKind.AUTHORIZATION_SURFACE
    if "approval" in path:
        return HermesHarnessSurfaceKind.APPROVAL_BOUNDARY_SURFACE
    if "audit" in path:
        return HermesHarnessSurfaceKind.AUDIT_BOUNDARY_SURFACE
    if "credential" in path or "secret" in path or "token" in path or "key" in name:
        return HermesHarnessSurfaceKind.CREDENTIAL_SURFACE
    if "network" in path or "http" in path or "api" in path:
        return HermesHarnessSurfaceKind.NETWORK_SURFACE
    if "command" in path or "shell" in path or "exec" in path:
        return HermesHarnessSurfaceKind.COMMAND_EXECUTION_SURFACE
    if "gateway" in path:
        return HermesHarnessSurfaceKind.GATEWAY_SURFACE
    if "package" in name or "lock" in name or "dependency" in detected:
        return HermesHarnessSurfaceKind.DEPENDENCY_MANIFEST_SURFACE
    if "config" in path or extension in {".json", ".toml", ".yaml", ".yml"}:
        return HermesHarnessSurfaceKind.CONFIGURATION_MANIFEST_SURFACE
    return HermesHarnessSurfaceKind.UNKNOWN


def infer_hermes_capability_from_surface(surface_kind: HermesHarnessSurfaceKind | str) -> HermesCapabilityKind:
    surface = HermesHarnessSurfaceKind(surface_kind)
    return {
        HermesHarnessSurfaceKind.PROFILE_SURFACE: HermesCapabilityKind.DEFINE_PROFILE,
        HermesHarnessSurfaceKind.MEMORY_SURFACE: HermesCapabilityKind.READ_MEMORY,
        HermesHarnessSurfaceKind.MISSION_SURFACE: HermesCapabilityKind.DEFINE_MISSION,
        HermesHarnessSurfaceKind.SKILL_SURFACE: HermesCapabilityKind.DEFINE_SKILL,
        HermesHarnessSurfaceKind.TOOL_SURFACE: HermesCapabilityKind.DEFINE_TOOL,
        HermesHarnessSurfaceKind.DELEGATION_SURFACE: HermesCapabilityKind.DELEGATE_AGENT,
        HermesHarnessSurfaceKind.PROVIDER_ROUTING_SURFACE: HermesCapabilityKind.ROUTE_PROVIDER,
        HermesHarnessSurfaceKind.RUNTIME_SURFACE: HermesCapabilityKind.START_RUNTIME,
        HermesHarnessSurfaceKind.CONTAINER_ISOLATION_SURFACE: HermesCapabilityKind.START_CONTAINER,
        HermesHarnessSurfaceKind.AUTHORIZATION_SURFACE: HermesCapabilityKind.ENFORCE_AUTHORIZATION,
        HermesHarnessSurfaceKind.APPROVAL_BOUNDARY_SURFACE: HermesCapabilityKind.REQUEST_APPROVAL,
        HermesHarnessSurfaceKind.AUDIT_BOUNDARY_SURFACE: HermesCapabilityKind.RECORD_AUDIT,
        HermesHarnessSurfaceKind.CONFIGURATION_MANIFEST_SURFACE: HermesCapabilityKind.DEFINE_PROFILE,
        HermesHarnessSurfaceKind.DEPENDENCY_MANIFEST_SURFACE: HermesCapabilityKind.START_RUNTIME,
        HermesHarnessSurfaceKind.RESULT_ENVELOPE_SURFACE: HermesCapabilityKind.EMIT_RESULT_ENVELOPE,
        HermesHarnessSurfaceKind.OCEL_TRACE_SURFACE: HermesCapabilityKind.EMIT_OCEL_TRACE,
        HermesHarnessSurfaceKind.PRIVATE_DATA_SURFACE: HermesCapabilityKind.ACCESS_PRIVATE_DATA,
        HermesHarnessSurfaceKind.CREDENTIAL_SURFACE: HermesCapabilityKind.USE_CREDENTIAL,
        HermesHarnessSurfaceKind.NETWORK_SURFACE: HermesCapabilityKind.ACCESS_NETWORK,
        HermesHarnessSurfaceKind.COMMAND_EXECUTION_SURFACE: HermesCapabilityKind.EXECUTE_COMMAND,
        HermesHarnessSurfaceKind.GATEWAY_SURFACE: HermesCapabilityKind.ACCESS_NETWORK,
    }.get(surface, HermesCapabilityKind.UNKNOWN)


def infer_hermes_risk_signals_from_inventory_entry(entry: ReferenceFileInventoryEntry) -> list[HermesRiskSignalKind]:
    surface = classify_inventory_entry_as_hermes_surface(entry)
    capability = infer_hermes_capability_from_surface(surface)
    risks: list[HermesRiskSignalKind] = []
    if surface == HermesHarnessSurfaceKind.PROFILE_SURFACE:
        risks.append(HermesRiskSignalKind.PROFILE_ACTIVATION_RISK)
    if capability == HermesCapabilityKind.READ_MEMORY:
        risks.extend([HermesRiskSignalKind.MEMORY_ACCESS_RISK, HermesRiskSignalKind.PRIVATE_DATA_EXPOSURE_RISK])
    if surface == HermesHarnessSurfaceKind.MISSION_SURFACE:
        risks.extend([HermesRiskSignalKind.MISSION_INSTALLATION_RISK, HermesRiskSignalKind.MISSION_EXECUTION_RISK])
    if surface == HermesHarnessSurfaceKind.SKILL_SURFACE:
        risks.extend([HermesRiskSignalKind.SKILL_REGISTRATION_RISK, HermesRiskSignalKind.SKILL_EXECUTION_RISK])
    if surface == HermesHarnessSurfaceKind.TOOL_SURFACE:
        risks.extend([HermesRiskSignalKind.TOOL_REGISTRATION_RISK, HermesRiskSignalKind.TOOL_INVOCATION_RISK])
    if capability == HermesCapabilityKind.DELEGATE_AGENT:
        risks.append(HermesRiskSignalKind.DELEGATION_EXECUTION_RISK)
    if capability == HermesCapabilityKind.ROUTE_PROVIDER:
        risks.extend([HermesRiskSignalKind.PROVIDER_ROUTING_RISK, HermesRiskSignalKind.PROVIDER_INVOCATION_RISK, HermesRiskSignalKind.NETWORK_ACCESS_RISK, HermesRiskSignalKind.CREDENTIAL_ACCESS_RISK])
    if capability == HermesCapabilityKind.START_RUNTIME:
        risks.append(HermesRiskSignalKind.RUNTIME_START_RISK)
    if capability == HermesCapabilityKind.START_CONTAINER:
        risks.append(HermesRiskSignalKind.CONTAINER_RUNTIME_RISK)
    if capability == HermesCapabilityKind.USE_CREDENTIAL:
        risks.append(HermesRiskSignalKind.CREDENTIAL_ACCESS_RISK)
    if capability == HermesCapabilityKind.ACCESS_NETWORK:
        risks.append(HermesRiskSignalKind.NETWORK_ACCESS_RISK)
    if capability == HermesCapabilityKind.EXECUTE_COMMAND:
        risks.append(HermesRiskSignalKind.COMMAND_EXECUTION_RISK)
    if surface == HermesHarnessSurfaceKind.GATEWAY_SURFACE:
        risks.append(HermesRiskSignalKind.GATEWAY_CONTROL_RISK)
    if surface == HermesHarnessSurfaceKind.OCEL_TRACE_SURFACE:
        risks.append(HermesRiskSignalKind.OCEL_EMISSION_RISK)
    return risks or [HermesRiskSignalKind.UNKNOWN]


def hermes_profile_preserves_no_execution(profile: HermesStyleObservationProfile) -> bool:
    return (
        profile.ready_for_execution is False
        and profile.ready_for_hermes_execution is False
        and profile.ready_for_hermes_runtime is False
        and profile.ready_for_reference_code_execution is False
        and profile.ready_for_profile_activation is False
        and profile.ready_for_memory_access is False
        and profile.ready_for_memory_write is False
        and profile.ready_for_mission_execution is False
        and profile.ready_for_skill_execution is False
        and profile.ready_for_tool_invocation is False
        and profile.ready_for_delegation_execution is False
        and profile.ready_for_provider_invocation is False
        and profile.ready_for_network_access is False
        and profile.ready_for_credential_access is False
        and profile.hermes_runtime is False
    )


def hermes_output_is_not_manifest_or_digestive_runtime(output: HermesObservationOutput) -> bool:
    return (
        output.ready_for_execution is False
        and output.ready_for_hermes_execution is False
        and output.ready_for_hermes_runtime is False
        and output.ready_for_memory_access is False
        and output.ready_for_mission_execution is False
        and output.ready_for_skill_execution is False
        and output.ready_for_delegation_execution is False
        and output.ready_for_provider_invocation is False
    )


def hermes_run_preview_preserves_no_execution(preview: HermesObservationRunPreview) -> bool:
    return (
        preview.no_hermes_execution_guarantee
        and preview.no_hermes_runtime_start_guarantee
        and preview.no_reference_code_execution_guarantee
        and preview.no_profile_activation_guarantee
        and preview.no_memory_access_guarantee
        and preview.no_memory_write_guarantee
        and preview.no_mission_execution_guarantee
        and preview.no_skill_execution_guarantee
        and preview.no_tool_invocation_guarantee
        and preview.no_delegation_execution_guarantee
        and preview.no_provider_invocation_guarantee
        and preview.no_network_access_guarantee
        and preview.no_credential_access_guarantee
    )


def v0323_readiness_report_is_not_runtime_ready(report: V0323ReadinessReport) -> bool:
    return (
        report.ready_for_execution is False
        and report.ready_for_hermes_execution is False
        and report.ready_for_hermes_runtime is False
        and report.ready_for_reference_code_execution is False
        and report.ready_for_profile_activation is False
        and report.ready_for_memory_access is False
        and report.ready_for_memory_write is False
        and report.ready_for_mission_execution is False
        and report.ready_for_skill_execution is False
        and report.ready_for_tool_invocation is False
        and report.ready_for_delegation_execution is False
        and report.ready_for_provider_invocation is False
        and report.ready_for_network_access is False
        and report.ready_for_credential_access is False
    )
