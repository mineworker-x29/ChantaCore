from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


V0320_VERSION = "v0.32.0"
V0320_RELEASE_NAME = "v0.32.0 External Harness Profile Contract + Reference Corpus Static Observation Contract"
V0320_TRACK = "External Harness Observation & Digestion Pipeline"

DEFAULT_HARNESS_PROHIBITED_RUNTIME_ACTIONS = [
    "execution",
    "install",
    "import_runtime",
    "network",
    "credential",
    "command",
    "provider",
    "browser",
    "rpa",
    "gateway",
    "packet_send",
    "registry_mutation",
    "memory_mutation",
]

DEFAULT_PROHIBITED_FILE_PATTERNS = [
    ".env",
    "*secret*",
    "*key*",
    "*token*",
    "*credential*",
]

ALLOWED_ACTIVE_OBSERVATION_MODES = {
    "contract_only",
    "manual_profile",
    "reference_static_observation",
    "manifest_only_observation",
    "documentation_only_observation",
    "unknown",
}


class ExternalHarnessProfileKind(StrEnum):
    OPENCODE_STYLE = "opencode_style"
    OPENCLAW_STYLE = "openclaw_style"
    HERMES_STYLE = "hermes_style"
    MCP_SERVER_STYLE = "mcp_server_style"
    PROVIDER_RUNTIME_STYLE = "provider_runtime_style"
    BROWSER_RUNTIME_STYLE = "browser_runtime_style"
    RPA_RUNTIME_STYLE = "rpa_runtime_style"
    GATEWAY_RUNTIME_STYLE = "gateway_runtime_style"
    GENERIC_AGENT_HARNESS = "generic_agent_harness"
    UNKNOWN = "unknown"


class ExternalHarnessSurfaceKind(StrEnum):
    FILE_WORKSPACE_SURFACE = "file_workspace_surface"
    TOOL_REGISTRY_SURFACE = "tool_registry_surface"
    PLUGIN_SURFACE = "plugin_surface"
    EXTERNAL_PLUGIN_SURFACE = "external_plugin_surface"
    PROVIDER_HOOK_SURFACE = "provider_hook_surface"
    COMMAND_EXECUTION_SURFACE = "command_execution_surface"
    CONFIGURATION_MANIFEST_SURFACE = "configuration_manifest_surface"
    PROFILE_SURFACE = "profile_surface"
    MEMORY_SURFACE = "memory_surface"
    MISSION_SURFACE = "mission_surface"
    SKILL_SURFACE = "skill_surface"
    DELEGATION_SURFACE = "delegation_surface"
    GATEWAY_SURFACE = "gateway_surface"
    CHANNEL_SURFACE = "channel_surface"
    APPROVAL_SURFACE = "approval_surface"
    AUDIT_SURFACE = "audit_surface"
    CREDENTIAL_SURFACE = "credential_surface"
    NETWORK_SURFACE = "network_surface"
    BROWSER_SURFACE = "browser_surface"
    RPA_SURFACE = "rpa_surface"
    RESULT_ENVELOPE_SURFACE = "result_envelope_surface"
    OCEL_TRACE_SURFACE = "ocel_trace_surface"
    PRIVATE_DATA_SURFACE = "private_data_surface"
    RAW_OUTPUT_SURFACE = "raw_output_surface"
    UNKNOWN = "unknown"


class ExternalHarnessProfileStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    PROFILE_READY = "profile_ready"
    PROFILE_READY_WITH_GAPS = "profile_ready_with_gaps"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class ExternalHarnessObservationMode(StrEnum):
    CONTRACT_ONLY = "contract_only"
    MANUAL_PROFILE = "manual_profile"
    REFERENCE_STATIC_OBSERVATION = "reference_static_observation"
    MANIFEST_ONLY_OBSERVATION = "manifest_only_observation"
    DOCUMENTATION_ONLY_OBSERVATION = "documentation_only_observation"
    FUTURE_LIVE_SCAN = "future_live_scan"
    FUTURE_RUNTIME = "future_runtime"
    UNKNOWN = "unknown"


class ExternalHarnessRiskPosture(StrEnum):
    UNKNOWN = "unknown"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class ExternalHarnessEvidenceQuality(StrEnum):
    UNKNOWN = "unknown"
    NONE = "none"
    WEAK = "weak"
    PARTIAL = "partial"
    SUFFICIENT_FOR_PROFILE = "sufficient_for_profile"
    SUFFICIENT_FOR_STATIC_OBSERVATION = "sufficient_for_static_observation"
    SUFFICIENT_FOR_NEXT_STAGE_REVIEW = "sufficient_for_next_stage_review"
    CONFLICTING = "conflicting"
    BLOCKED = "blocked"


def _require_non_blank(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must not be blank")


def _validate_string_list(name: str, values: list[str]) -> None:
    if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
        raise TypeError(f"{name} must be list[str]")


def _validate_object_list(name: str, values: list[Any], expected_type: type) -> None:
    if not isinstance(values, list) or not all(isinstance(item, expected_type) for item in values):
        raise TypeError(f"{name} must be list[{expected_type.__name__}]")


def _metadata_flag_true(metadata: dict[str, Any], names: set[str]) -> bool:
    return isinstance(metadata, dict) and any(metadata.get(name) is True for name in names)


def _validate_version_includes_v0320(version: str) -> None:
    _require_non_blank("version", version)
    if V0320_VERSION not in version:
        raise ValueError("version must include v0.32.0")


def _validate_enum_list(name: str, values: list[Any], normalizer: Any) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        normalizer(value)


def normalize_external_harness_profile_kind(value: ExternalHarnessProfileKind | str) -> ExternalHarnessProfileKind:
    if isinstance(value, ExternalHarnessProfileKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("external harness profile kind must not be blank")
        return ExternalHarnessProfileKind(stripped)
    raise TypeError(f"unsupported external harness profile kind: {value!r}")


def normalize_external_harness_surface_kind(value: ExternalHarnessSurfaceKind | str) -> ExternalHarnessSurfaceKind:
    if isinstance(value, ExternalHarnessSurfaceKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("external harness surface kind must not be blank")
        return ExternalHarnessSurfaceKind(stripped)
    raise TypeError(f"unsupported external harness surface kind: {value!r}")


def normalize_external_harness_profile_status(value: ExternalHarnessProfileStatus | str) -> ExternalHarnessProfileStatus:
    if isinstance(value, ExternalHarnessProfileStatus):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("external harness profile status must not be blank")
        return ExternalHarnessProfileStatus(stripped)
    raise TypeError(f"unsupported external harness profile status: {value!r}")


def normalize_external_harness_observation_mode(value: ExternalHarnessObservationMode | str) -> ExternalHarnessObservationMode:
    if isinstance(value, ExternalHarnessObservationMode):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("external harness observation mode must not be blank")
        return ExternalHarnessObservationMode(stripped)
    raise TypeError(f"unsupported external harness observation mode: {value!r}")


def normalize_external_harness_risk_posture(value: ExternalHarnessRiskPosture | str) -> ExternalHarnessRiskPosture:
    if isinstance(value, ExternalHarnessRiskPosture):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("external harness risk posture must not be blank")
        return ExternalHarnessRiskPosture(stripped)
    raise TypeError(f"unsupported external harness risk posture: {value!r}")


def normalize_external_harness_evidence_quality(value: ExternalHarnessEvidenceQuality | str) -> ExternalHarnessEvidenceQuality:
    if isinstance(value, ExternalHarnessEvidenceQuality):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("external harness evidence quality must not be blank")
        return ExternalHarnessEvidenceQuality(stripped)
    raise TypeError(f"unsupported external harness evidence quality: {value!r}")


def external_harness_profile_kind_executes(_: ExternalHarnessProfileKind | str) -> bool:
    normalize_external_harness_profile_kind(_)
    return False


def external_harness_surface_kind_is_permission(_: ExternalHarnessSurfaceKind | str) -> bool:
    normalize_external_harness_surface_kind(_)
    return False


@dataclass(frozen=True)
class ExternalHarnessRuntimeReadinessFlagSet:
    flag_set_id: str
    ready_for_execution: bool = False
    ready_for_external_harness_execution: bool = False
    ready_for_reference_code_execution: bool = False
    ready_for_live_scan: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_browser_runtime_control: bool = False
    ready_for_rpa_runtime_control: bool = False
    ready_for_gateway_control: bool = False
    ready_for_packet_send: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_ocel_emission: bool = False
    ready_for_ui_runtime: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        for name in (
            "ready_for_execution",
            "ready_for_external_harness_execution",
            "ready_for_reference_code_execution",
            "ready_for_live_scan",
            "ready_for_network_access",
            "ready_for_credential_access",
            "ready_for_command_execution",
            "ready_for_provider_invocation",
            "ready_for_browser_runtime_control",
            "ready_for_rpa_runtime_control",
            "ready_for_gateway_control",
            "ready_for_packet_send",
            "ready_for_registry_mutation",
            "ready_for_memory_mutation",
            "ready_for_ocel_emission",
            "ready_for_ui_runtime",
        ):
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False in v0.32.0")
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "harness_execution"}):
            raise ValueError("ExternalHarnessRuntimeReadinessFlagSet must not imply runtime enablement")

    @property
    def runtime_enablement(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalHarnessSurfaceDescriptor:
    surface_id: str
    surface_kind: ExternalHarnessSurfaceKind | str
    name: str
    description: str
    risk_posture: ExternalHarnessRiskPosture | str
    evidence_quality: ExternalHarnessEvidenceQuality | str
    evidence_refs: list[str] = field(default_factory=list)
    boundary_notes: list[str] = field(default_factory=list)
    prohibited_runtime_actions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("surface_id", self.surface_id)
        normalize_external_harness_surface_kind(self.surface_kind)
        _require_non_blank("name", self.name)
        _require_non_blank("description", self.description)
        risk = normalize_external_harness_risk_posture(self.risk_posture)
        normalize_external_harness_evidence_quality(self.evidence_quality)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("boundary_notes", self.boundary_notes)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        if risk in {ExternalHarnessRiskPosture.HIGH, ExternalHarnessRiskPosture.CRITICAL, ExternalHarnessRiskPosture.BLOCKED}:
            if not self.boundary_notes and not self.prohibited_runtime_actions:
                raise ValueError("high, critical, or blocked risk requires boundary notes or prohibited runtime actions")
        if _metadata_flag_true(self.metadata, {"permission", "runtime_permission"}):
            raise ValueError("ExternalHarnessSurfaceDescriptor must not imply permission")

    @property
    def is_permission(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalHarnessObservationBoundary:
    boundary_id: str
    profile_kind: ExternalHarnessProfileKind | str
    allowed_observation_modes: list[ExternalHarnessObservationMode | str] = field(default_factory=list)
    prohibited_observation_modes: list[ExternalHarnessObservationMode | str] = field(default_factory=list)
    allowed_static_operations: list[str] = field(default_factory=list)
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_HARNESS_PROHIBITED_RUNTIME_ACTIONS))
    prohibited_file_patterns: list[str] = field(default_factory=lambda: list(DEFAULT_PROHIBITED_FILE_PATTERNS))
    requires_read_only: bool = True
    requires_no_execution: bool = True
    requires_no_network: bool = True
    requires_no_credentials: bool = True
    requires_no_import_runtime: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_id", self.boundary_id)
        normalize_external_harness_profile_kind(self.profile_kind)
        _validate_enum_list("allowed_observation_modes", self.allowed_observation_modes, normalize_external_harness_observation_mode)
        _validate_enum_list("prohibited_observation_modes", self.prohibited_observation_modes, normalize_external_harness_observation_mode)
        _validate_string_list("allowed_static_operations", self.allowed_static_operations)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        missing = set(DEFAULT_HARNESS_PROHIBITED_RUNTIME_ACTIONS) - set(self.prohibited_runtime_actions)
        if missing:
            raise ValueError(f"prohibited_runtime_actions missing v0.32.0 prohibitions: {sorted(missing)}")
        _validate_string_list("prohibited_file_patterns", self.prohibited_file_patterns)
        for pattern in DEFAULT_PROHIBITED_FILE_PATTERNS:
            if pattern not in self.prohibited_file_patterns:
                raise ValueError("prohibited_file_patterns must include secret-like defaults")
        for name in (
            "requires_read_only",
            "requires_no_execution",
            "requires_no_network",
            "requires_no_credentials",
            "requires_no_import_runtime",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.32.0")
        if _metadata_flag_true(self.metadata, {"runtime_enforcement", "permission"}):
            raise ValueError("ExternalHarnessObservationBoundary is not runtime enforcement by itself")

    @property
    def runtime_enforcement(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalHarnessProfile:
    profile_id: str
    harness_kind: ExternalHarnessProfileKind | str
    display_name: str
    description: str
    source_ref: str | None
    observation_mode: ExternalHarnessObservationMode | str
    declared_surfaces: list[ExternalHarnessSurfaceDescriptor]
    observation_boundaries: list[ExternalHarnessObservationBoundary]
    runtime_readiness: ExternalHarnessRuntimeReadinessFlagSet
    evidence_refs: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    status: ExternalHarnessProfileStatus | str = ExternalHarnessProfileStatus.DRAFT
    ready_for_v0321_opencode_profile: bool = False
    ready_for_v0322_openclaw_profile: bool = False
    ready_for_v0323_hermes_profile: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("profile_id", self.profile_id)
        normalize_external_harness_profile_kind(self.harness_kind)
        _require_non_blank("display_name", self.display_name)
        _require_non_blank("description", self.description)
        mode = normalize_external_harness_observation_mode(self.observation_mode)
        if mode.value not in ALLOWED_ACTIVE_OBSERVATION_MODES:
            raise ValueError("observation_mode must not be future_live_scan or future_runtime in v0.32.0")
        _validate_object_list("declared_surfaces", self.declared_surfaces, ExternalHarnessSurfaceDescriptor)
        _validate_object_list("observation_boundaries", self.observation_boundaries, ExternalHarnessObservationBoundary)
        if not isinstance(self.runtime_readiness, ExternalHarnessRuntimeReadinessFlagSet):
            raise TypeError("runtime_readiness must be ExternalHarnessRuntimeReadinessFlagSet")
        if not external_harness_runtime_flags_preserve_false(self.runtime_readiness):
            raise ValueError("runtime_readiness flags must all be false")
        for name in ("evidence_refs", "assumptions", "limitations"):
            _validate_string_list(name, getattr(self, name))
        normalize_external_harness_profile_status(self.status)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.32.0")
        if _metadata_flag_true(self.metadata, {"harness_execution", "live_scan", "runtime_profile"}):
            raise ValueError("ExternalHarnessProfile must not imply harness execution")

    @property
    def harness_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalHarnessProfileSet:
    profile_set_id: str
    version: str
    profiles: list[ExternalHarnessProfile]
    default_boundary: ExternalHarnessObservationBoundary
    runtime_readiness: ExternalHarnessRuntimeReadinessFlagSet
    evidence_refs: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0321_opencode_profile: bool = True
    ready_for_v0322_openclaw_profile: bool = True
    ready_for_v0323_hermes_profile: bool = True
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("profile_set_id", self.profile_set_id)
        _validate_version_includes_v0320(self.version)
        _validate_object_list("profiles", self.profiles, ExternalHarnessProfile)
        if not isinstance(self.default_boundary, ExternalHarnessObservationBoundary):
            raise TypeError("default_boundary must be ExternalHarnessObservationBoundary")
        if not isinstance(self.runtime_readiness, ExternalHarnessRuntimeReadinessFlagSet):
            raise TypeError("runtime_readiness must be ExternalHarnessRuntimeReadinessFlagSet")
        if not external_harness_runtime_flags_preserve_false(self.runtime_readiness):
            raise ValueError("runtime_readiness flags must all be false")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("gaps", self.gaps)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.32.0")
        if _metadata_flag_true(self.metadata, {"runtime_registry", "active_profile_registry"}):
            raise ValueError("ExternalHarnessProfileSet must not imply runtime registry")

    @property
    def runtime_registry(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalHarnessProfileNoExecutionGuarantee:
    guarantee_id: str
    version: str
    no_harness_execution: bool = True
    no_reference_code_execution: bool = True
    no_live_scan: bool = True
    no_source_ref_fetch: bool = True
    no_install: bool = True
    no_import_runtime: bool = True
    no_network_access: bool = True
    no_credential_access: bool = True
    no_command_execution: bool = True
    no_provider_invocation: bool = True
    no_browser_automation: bool = True
    no_rpa_control: bool = True
    no_gateway_control: bool = True
    no_packet_send: bool = True
    no_registry_mutation: bool = True
    no_memory_mutation: bool = True
    no_ocel_emission: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version_includes_v0320(self.version)
        for name in (
            "no_harness_execution",
            "no_reference_code_execution",
            "no_live_scan",
            "no_source_ref_fetch",
            "no_install",
            "no_import_runtime",
            "no_network_access",
            "no_credential_access",
            "no_command_execution",
            "no_provider_invocation",
            "no_browser_automation",
            "no_rpa_control",
            "no_gateway_control",
            "no_packet_send",
            "no_registry_mutation",
            "no_memory_mutation",
            "no_ocel_emission",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.32.0")
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"runtime_enforcement", "harness_execution"}):
            raise ValueError("ExternalHarnessProfileNoExecutionGuarantee is contract metadata only")

    @property
    def runtime_enforcement(self) -> bool:
        return False


def build_external_harness_runtime_readiness_flags(
    flag_set_id: str = "external_harness_runtime_readiness_flags:v0.32.0",
    metadata: dict[str, Any] | None = None,
) -> ExternalHarnessRuntimeReadinessFlagSet:
    return ExternalHarnessRuntimeReadinessFlagSet(flag_set_id=flag_set_id, metadata=dict(metadata or {}))


def build_external_harness_surface_descriptor(
    surface_id: str,
    surface_kind: ExternalHarnessSurfaceKind | str,
    name: str,
    description: str,
    risk_posture: ExternalHarnessRiskPosture | str = ExternalHarnessRiskPosture.UNKNOWN,
    evidence_quality: ExternalHarnessEvidenceQuality | str = ExternalHarnessEvidenceQuality.UNKNOWN,
    evidence_refs: list[str] | None = None,
    boundary_notes: list[str] | None = None,
    prohibited_runtime_actions: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ExternalHarnessSurfaceDescriptor:
    return ExternalHarnessSurfaceDescriptor(
        surface_id=surface_id,
        surface_kind=surface_kind,
        name=name,
        description=description,
        risk_posture=risk_posture,
        evidence_quality=evidence_quality,
        evidence_refs=list(evidence_refs or []),
        boundary_notes=list(boundary_notes or []),
        prohibited_runtime_actions=list(prohibited_runtime_actions or []),
        metadata=dict(metadata or {}),
    )


def build_external_harness_observation_boundary(
    boundary_id: str,
    profile_kind: ExternalHarnessProfileKind | str = ExternalHarnessProfileKind.UNKNOWN,
    allowed_observation_modes: list[ExternalHarnessObservationMode | str] | None = None,
    prohibited_observation_modes: list[ExternalHarnessObservationMode | str] | None = None,
    allowed_static_operations: list[str] | None = None,
    prohibited_runtime_actions: list[str] | None = None,
    prohibited_file_patterns: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ExternalHarnessObservationBoundary:
    return ExternalHarnessObservationBoundary(
        boundary_id=boundary_id,
        profile_kind=profile_kind,
        allowed_observation_modes=list(
            allowed_observation_modes
            or [
                ExternalHarnessObservationMode.CONTRACT_ONLY,
                ExternalHarnessObservationMode.MANUAL_PROFILE,
                ExternalHarnessObservationMode.REFERENCE_STATIC_OBSERVATION,
                ExternalHarnessObservationMode.MANIFEST_ONLY_OBSERVATION,
                ExternalHarnessObservationMode.DOCUMENTATION_ONLY_OBSERVATION,
            ]
        ),
        prohibited_observation_modes=list(
            prohibited_observation_modes
            or [ExternalHarnessObservationMode.FUTURE_LIVE_SCAN, ExternalHarnessObservationMode.FUTURE_RUNTIME]
        ),
        allowed_static_operations=list(allowed_static_operations or ["path reference", "file inventory model", "manifest candidate model"]),
        prohibited_runtime_actions=list(prohibited_runtime_actions or DEFAULT_HARNESS_PROHIBITED_RUNTIME_ACTIONS),
        prohibited_file_patterns=list(prohibited_file_patterns or DEFAULT_PROHIBITED_FILE_PATTERNS),
        metadata=dict(metadata or {}),
    )


def build_external_harness_profile(
    profile_id: str,
    harness_kind: ExternalHarnessProfileKind | str,
    display_name: str,
    description: str,
    source_ref: str | None = None,
    observation_mode: ExternalHarnessObservationMode | str = ExternalHarnessObservationMode.CONTRACT_ONLY,
    declared_surfaces: list[ExternalHarnessSurfaceDescriptor] | None = None,
    observation_boundaries: list[ExternalHarnessObservationBoundary] | None = None,
    runtime_readiness: ExternalHarnessRuntimeReadinessFlagSet | None = None,
    evidence_refs: list[str] | None = None,
    assumptions: list[str] | None = None,
    limitations: list[str] | None = None,
    status: ExternalHarnessProfileStatus | str = ExternalHarnessProfileStatus.PROFILE_READY_WITH_GAPS,
    ready_for_v0321_opencode_profile: bool = False,
    ready_for_v0322_openclaw_profile: bool = False,
    ready_for_v0323_hermes_profile: bool = False,
    metadata: dict[str, Any] | None = None,
) -> ExternalHarnessProfile:
    return ExternalHarnessProfile(
        profile_id=profile_id,
        harness_kind=harness_kind,
        display_name=display_name,
        description=description,
        source_ref=source_ref,
        observation_mode=observation_mode,
        declared_surfaces=list(declared_surfaces or []),
        observation_boundaries=list(observation_boundaries or []),
        runtime_readiness=runtime_readiness or build_external_harness_runtime_readiness_flags(),
        evidence_refs=list(evidence_refs or []),
        assumptions=list(assumptions or []),
        limitations=list(limitations or []),
        status=status,
        ready_for_v0321_opencode_profile=ready_for_v0321_opencode_profile,
        ready_for_v0322_openclaw_profile=ready_for_v0322_openclaw_profile,
        ready_for_v0323_hermes_profile=ready_for_v0323_hermes_profile,
        ready_for_execution=False,
        metadata=dict(metadata or {}),
    )


def build_external_harness_profile_set(
    profile_set_id: str,
    profiles: list[ExternalHarnessProfile] | None = None,
    default_boundary: ExternalHarnessObservationBoundary | None = None,
    runtime_readiness: ExternalHarnessRuntimeReadinessFlagSet | None = None,
    evidence_refs: list[str] | None = None,
    gaps: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ExternalHarnessProfileSet:
    return ExternalHarnessProfileSet(
        profile_set_id=profile_set_id,
        version=V0320_VERSION,
        profiles=list(profiles or []),
        default_boundary=default_boundary or build_external_harness_observation_boundary("external_harness_observation_boundary:default:v0.32.0"),
        runtime_readiness=runtime_readiness or build_external_harness_runtime_readiness_flags(),
        evidence_refs=list(evidence_refs or []),
        gaps=list(gaps or []),
        ready_for_v0321_opencode_profile=True,
        ready_for_v0322_openclaw_profile=True,
        ready_for_v0323_hermes_profile=True,
        ready_for_execution=False,
        metadata=dict(metadata or {}),
    )


def build_external_harness_no_execution_guarantee(
    guarantee_id: str = "external_harness_no_execution_guarantee:v0.32.0",
    evidence_refs: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ExternalHarnessProfileNoExecutionGuarantee:
    return ExternalHarnessProfileNoExecutionGuarantee(
        guarantee_id=guarantee_id,
        version=V0320_VERSION,
        evidence_refs=list(evidence_refs or []),
        metadata=dict(metadata or {}),
    )


def external_harness_runtime_flags_preserve_false(flags: ExternalHarnessRuntimeReadinessFlagSet) -> bool:
    return (
        flags.ready_for_execution is False
        and flags.ready_for_external_harness_execution is False
        and flags.ready_for_reference_code_execution is False
        and flags.ready_for_live_scan is False
        and flags.ready_for_network_access is False
        and flags.ready_for_credential_access is False
        and flags.ready_for_command_execution is False
        and flags.ready_for_provider_invocation is False
        and flags.ready_for_browser_runtime_control is False
        and flags.ready_for_rpa_runtime_control is False
        and flags.ready_for_gateway_control is False
        and flags.ready_for_packet_send is False
        and flags.ready_for_registry_mutation is False
        and flags.ready_for_memory_mutation is False
        and flags.ready_for_ocel_emission is False
        and flags.ready_for_ui_runtime is False
        and flags.runtime_enablement is False
    )


def harness_profile_preserves_no_execution(profile: ExternalHarnessProfile) -> bool:
    return profile.ready_for_execution is False and profile.harness_execution is False and external_harness_runtime_flags_preserve_false(profile.runtime_readiness)
