from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .profiles import (
    DEFAULT_PROHIBITED_FILE_PATTERNS,
    _metadata_flag_true,
    _require_non_blank,
    _validate_object_list,
    _validate_string_list,
)
from .reference_corpus import ReferenceFileInventoryEntry


V0324_VERSION = "v0.32.4"
V0324_RELEASE_NAME = "v0.32.4 External Skill Manifest Extraction"

DEFAULT_MANIFEST_PROHIBITED_RUNTIME_ACTIONS = [
    "manifest activation",
    "harness execution",
    "reference code execution",
    "install",
    "import runtime",
    "plugin loading",
    "external plugin loading",
    "tool registration",
    "tool invocation",
    "mission installation",
    "mission execution",
    "gateway connection",
    "provider invocation",
    "network",
    "credential",
    "secret file read",
    "command",
    "registry mutation",
    "memory mutation",
    "OCEL emission",
]


class ExternalManifestSourceKind(StrEnum):
    OPENCODE_OBSERVATION_OUTPUT = "opencode_observation_output"
    OPENCLAW_OBSERVATION_OUTPUT = "openclaw_observation_output"
    HERMES_OBSERVATION_OUTPUT = "hermes_observation_output"
    EXTERNAL_HARNESS_PROFILE = "external_harness_profile"
    REFERENCE_FILE_INVENTORY = "reference_file_inventory"
    REFERENCE_CORPUS_SNAPSHOT = "reference_corpus_snapshot"
    REFERENCE_MANIFEST_PATH = "reference_manifest_path"
    REFERENCE_DOCUMENTATION_PATH = "reference_documentation_path"
    REFERENCE_CONFIG_PATH = "reference_config_path"
    MANUAL_MANIFEST_REF = "manual_manifest_ref"
    SANITIZED_MANIFEST = "sanitized_manifest"
    UNKNOWN = "unknown"


class ExternalManifestCandidateKind(StrEnum):
    SKILL_MANIFEST = "skill_manifest"
    TOOL_MANIFEST = "tool_manifest"
    PLUGIN_MANIFEST = "plugin_manifest"
    EXTERNAL_PLUGIN_MANIFEST = "external_plugin_manifest"
    MISSION_MANIFEST = "mission_manifest"
    GATEWAY_MANIFEST = "gateway_manifest"
    CHANNEL_MANIFEST = "channel_manifest"
    PROVIDER_MANIFEST = "provider_manifest"
    PROFILE_MANIFEST = "profile_manifest"
    MEMORY_SCHEMA_MANIFEST = "memory_schema_manifest"
    APPROVAL_POLICY_MANIFEST = "approval_policy_manifest"
    AUDIT_POLICY_MANIFEST = "audit_policy_manifest"
    RESULT_ENVELOPE_MANIFEST = "result_envelope_manifest"
    OCEL_TRACE_MANIFEST = "ocel_trace_manifest"
    GENERIC_MANIFEST = "generic_manifest"
    UNKNOWN = "unknown"


class ExternalManifestExtractionStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    EXTRACTED = "extracted"
    EXTRACTED_WITH_GAPS = "extracted_with_gaps"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    REJECTED = "rejected"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class ExternalManifestCapabilityKind(StrEnum):
    DECLARE_SKILL = "declare_skill"
    DECLARE_TOOL = "declare_tool"
    DECLARE_PLUGIN = "declare_plugin"
    DECLARE_EXTERNAL_PLUGIN = "declare_external_plugin"
    DECLARE_MISSION = "declare_mission"
    DECLARE_GATEWAY = "declare_gateway"
    DECLARE_CHANNEL = "declare_channel"
    DECLARE_PROVIDER = "declare_provider"
    DECLARE_PROFILE = "declare_profile"
    DECLARE_MEMORY_SCHEMA = "declare_memory_schema"
    DECLARE_APPROVAL_POLICY = "declare_approval_policy"
    DECLARE_AUDIT_POLICY = "declare_audit_policy"
    DECLARE_RESULT_ENVELOPE = "declare_result_envelope"
    DECLARE_OCEL_TRACE = "declare_ocel_trace"
    UNKNOWN = "unknown"


class ExternalManifestEffectSurfaceKind(StrEnum):
    NO_EFFECT = "no_effect"
    FILE_WORKSPACE = "file_workspace"
    TOOL_REGISTRY = "tool_registry"
    PLUGIN_RUNTIME = "plugin_runtime"
    MISSION_RUNTIME = "mission_runtime"
    GATEWAY_RUNTIME = "gateway_runtime"
    CHANNEL_RUNTIME = "channel_runtime"
    PROVIDER_RUNTIME = "provider_runtime"
    NETWORK = "network"
    CREDENTIAL = "credential"
    COMMAND = "command"
    BROWSER = "browser"
    RPA = "rpa"
    DELEGATION = "delegation"
    MEMORY = "memory"
    REGISTRY = "registry"
    POLICY = "policy"
    PRIVATE_DATA = "private_data"
    RAW_OUTPUT = "raw_output"
    OCEL_TRACE = "ocel_trace"
    UNKNOWN = "unknown"


class ExternalManifestRiskSurfaceKind(StrEnum):
    REFERENCE_CODE_EXECUTION = "reference_code_execution"
    DEPENDENCY_INSTALL = "dependency_install"
    RUNTIME_IMPORT = "runtime_import"
    PLUGIN_LOADING = "plugin_loading"
    EXTERNAL_PLUGIN_LOADING = "external_plugin_loading"
    TOOL_REGISTRATION = "tool_registration"
    TOOL_INVOCATION = "tool_invocation"
    MISSION_INSTALLATION = "mission_installation"
    MISSION_EXECUTION = "mission_execution"
    PROVIDER_INVOCATION = "provider_invocation"
    GATEWAY_CONNECTION = "gateway_connection"
    CHANNEL_ACCESS = "channel_access"
    MESSAGE_SEND = "message_send"
    WEBHOOK_CALL = "webhook_call"
    NETWORK_ACCESS = "network_access"
    CREDENTIAL_ACCESS = "credential_access"
    SECRET_FILE_READ = "secret_file_read"
    COMMAND_EXECUTION = "command_execution"
    BROWSER_AUTOMATION = "browser_automation"
    RPA_CONTROL = "rpa_control"
    MEMORY_MUTATION = "memory_mutation"
    REGISTRY_MUTATION = "registry_mutation"
    PRIVATE_DATA_EXPOSURE = "private_data_exposure"
    RAW_OUTPUT_PERSISTENCE = "raw_output_persistence"
    OCEL_EMISSION = "ocel_emission"
    UNKNOWN = "unknown"


class ExternalManifestEvidenceQuality(StrEnum):
    UNKNOWN = "unknown"
    NONE = "none"
    WEAK = "weak"
    PARTIAL = "partial"
    SUFFICIENT_FOR_MANIFEST_CANDIDATE = "sufficient_for_manifest_candidate"
    SUFFICIENT_FOR_RISK_CLASSIFICATION_REVIEW = "sufficient_for_risk_classification_review"
    CONFLICTING = "conflicting"
    BLOCKED = "blocked"


def _validate_version_includes_v0324(version: str) -> None:
    _require_non_blank("version", version)
    if V0324_VERSION not in version:
        raise ValueError("version must include v0.32.4")


def _validate_kind_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _validate_default_prohibitions(name: str, values: list[str]) -> None:
    _validate_string_list(name, values)
    missing = set(DEFAULT_MANIFEST_PROHIBITED_RUNTIME_ACTIONS) - set(values)
    if missing:
        raise ValueError(f"{name} missing v0.32.4 prohibitions: {sorted(missing)}")


def _validate_secret_file_patterns(name: str, values: list[str]) -> None:
    _validate_string_list(name, values)
    missing = set(DEFAULT_PROHIBITED_FILE_PATTERNS) - set(values)
    if missing:
        raise ValueError(f"{name} missing secret-like prohibited patterns: {sorted(missing)}")


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.32.4")


@dataclass(frozen=True)
class ExternalManifestSourceRef:
    source_ref_id: str
    source_kind: ExternalManifestSourceKind | str
    source_id: str
    harness_kind: str | None = None
    reference_entry_ids: list[str] = field(default_factory=list)
    manifest_path_refs: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        ExternalManifestSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        for name in ("reference_entry_ids", "manifest_path_refs", "evidence_refs"):
            _validate_string_list(name, getattr(self, name))
        if _metadata_flag_true(self.metadata, {"source_fetch", "file_execution", "runtime_import", "execution"}):
            raise ValueError("ExternalManifestSourceRef is not source fetch, file execution, or runtime import")

    @property
    def source_fetch(self) -> bool:
        return False

    @property
    def file_execution_or_import(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalManifestFieldObservation:
    field_observation_id: str
    field_name: str
    field_summary: str
    observed_values: list[str] = field(default_factory=list)
    inferred_capability_kinds: list[ExternalManifestCapabilityKind | str] = field(default_factory=list)
    inferred_effect_surfaces: list[ExternalManifestEffectSurfaceKind | str] = field(default_factory=list)
    inferred_risk_surfaces: list[ExternalManifestRiskSurfaceKind | str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("field_observation_id", self.field_observation_id)
        _require_non_blank("field_name", self.field_name)
        _require_non_blank("field_summary", self.field_summary)
        for name in ("observed_values", "evidence_refs", "limitations"):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("inferred_capability_kinds", self.inferred_capability_kinds, ExternalManifestCapabilityKind)
        _validate_kind_list("inferred_effect_surfaces", self.inferred_effect_surfaces, ExternalManifestEffectSurfaceKind)
        _validate_kind_list("inferred_risk_surfaces", self.inferred_risk_surfaces, ExternalManifestRiskSurfaceKind)
        if _metadata_flag_true(self.metadata, {"manifest_activation", "runtime_effect"}):
            raise ValueError("ExternalManifestFieldObservation is not manifest activation")

    @property
    def manifest_activation(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalManifestExtractionRule:
    rule_id: str
    name: str
    description: str
    source_kinds: list[ExternalManifestSourceKind | str] = field(default_factory=list)
    candidate_kinds: list[ExternalManifestCandidateKind | str] = field(default_factory=list)
    path_patterns: list[str] = field(default_factory=list)
    file_extensions: list[str] = field(default_factory=list)
    detected_kinds: list[str] = field(default_factory=list)
    prohibited_file_patterns: list[str] = field(default_factory=lambda: list(DEFAULT_PROHIBITED_FILE_PATTERNS))
    produces_runtime_effects: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("rule_id", self.rule_id)
        _require_non_blank("name", self.name)
        _require_non_blank("description", self.description)
        _validate_kind_list("source_kinds", self.source_kinds, ExternalManifestSourceKind)
        _validate_kind_list("candidate_kinds", self.candidate_kinds, ExternalManifestCandidateKind)
        for name in ("path_patterns", "file_extensions", "detected_kinds"):
            _validate_string_list(name, getattr(self, name))
        _validate_secret_file_patterns("prohibited_file_patterns", self.prohibited_file_patterns)
        if self.produces_runtime_effects is not False:
            raise ValueError("produces_runtime_effects must always be False in v0.32.4")
        if _metadata_flag_true(self.metadata, {"scanner_runtime", "live_scan"}):
            raise ValueError("ExternalManifestExtractionRule is not scanner runtime")

    @property
    def scanner_runtime(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalManifestCandidateBase:
    manifest_candidate_id: str
    candidate_kind: ExternalManifestCandidateKind | str
    status: ExternalManifestExtractionStatus | str
    declared_name: str
    display_name: str | None = None
    source_refs: list[ExternalManifestSourceRef] = field(default_factory=list)
    field_observations: list[ExternalManifestFieldObservation] = field(default_factory=list)
    declared_capabilities: list[ExternalManifestCapabilityKind | str] = field(default_factory=list)
    effect_surfaces: list[ExternalManifestEffectSurfaceKind | str] = field(default_factory=list)
    risk_surfaces: list[ExternalManifestRiskSurfaceKind | str] = field(default_factory=list)
    evidence_quality: ExternalManifestEvidenceQuality | str = ExternalManifestEvidenceQuality.UNKNOWN
    evidence_refs: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_manifest_activation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("manifest_candidate_id", self.manifest_candidate_id)
        ExternalManifestCandidateKind(self.candidate_kind)
        ExternalManifestExtractionStatus(self.status)
        _require_non_blank("declared_name", self.declared_name)
        _validate_object_list("source_refs", self.source_refs, ExternalManifestSourceRef)
        _validate_object_list("field_observations", self.field_observations, ExternalManifestFieldObservation)
        _validate_kind_list("declared_capabilities", self.declared_capabilities, ExternalManifestCapabilityKind)
        _validate_kind_list("effect_surfaces", self.effect_surfaces, ExternalManifestEffectSurfaceKind)
        _validate_kind_list("risk_surfaces", self.risk_surfaces, ExternalManifestRiskSurfaceKind)
        ExternalManifestEvidenceQuality(self.evidence_quality)
        for name in ("evidence_refs", "assumptions", "limitations", "gaps"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, ("ready_for_manifest_activation", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"active_manifest", "manifest_activation", "execution_ready"}):
            raise ValueError("ExternalManifestCandidateBase is not active manifest")

    @property
    def active_manifest(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalSkillManifestCandidate(ExternalManifestCandidateBase):
    proposed_skill_name: str = ""
    skill_purpose_summary: str = "Static skill manifest candidate only."
    input_surface_summary: str = "Unknown input surface."
    output_surface_summary: str = "Unknown output surface."
    side_effect_summary: str = "No runtime side effect is authorized."
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_MANIFEST_PROHIBITED_RUNTIME_ACTIONS))

    def __post_init__(self) -> None:
        super().__post_init__()
        _require_non_blank("proposed_skill_name", self.proposed_skill_name)
        _validate_default_prohibitions("prohibited_runtime_actions", self.prohibited_runtime_actions)

    @property
    def active_skill(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalToolManifestCandidate(ExternalManifestCandidateBase):
    proposed_tool_name: str = ""
    tool_contract_summary: str = "Static tool manifest candidate only."
    input_schema_summary: str = "Unknown input schema."
    output_schema_summary: str = "Unknown output schema."
    side_effect_policy_summary: str = "No tool runtime is authorized."
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_MANIFEST_PROHIBITED_RUNTIME_ACTIONS))

    def __post_init__(self) -> None:
        super().__post_init__()
        _require_non_blank("proposed_tool_name", self.proposed_tool_name)
        _validate_default_prohibitions("prohibited_runtime_actions", self.prohibited_runtime_actions)

    @property
    def registered_tool(self) -> bool:
        return False

    @property
    def tool_invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalPluginManifestCandidate(ExternalManifestCandidateBase):
    proposed_plugin_name: str = ""
    plugin_scope_summary: str = "Static plugin manifest candidate only."
    external_plugin: bool = False
    plugin_runtime_summary: str = "No plugin runtime is authorized."
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_MANIFEST_PROHIBITED_RUNTIME_ACTIONS))

    def __post_init__(self) -> None:
        super().__post_init__()
        _require_non_blank("proposed_plugin_name", self.proposed_plugin_name)
        _validate_default_prohibitions("prohibited_runtime_actions", self.prohibited_runtime_actions)
        if self.external_plugin and ExternalManifestRiskSurfaceKind.EXTERNAL_PLUGIN_LOADING not in [ExternalManifestRiskSurfaceKind(value) for value in self.risk_surfaces] and "external plugin loading" not in self.prohibited_runtime_actions:
            raise ValueError("external_plugin candidates require external plugin risk surface or prohibition")

    @property
    def plugin_loading(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalMissionManifestCandidate(ExternalManifestCandidateBase):
    proposed_mission_name: str = ""
    mission_scope_summary: str = "Static mission manifest candidate only."
    trigger_summary: str = "No trigger execution is authorized."
    schedule_summary: str = "No scheduler runtime is authorized."
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_MANIFEST_PROHIBITED_RUNTIME_ACTIONS))

    def __post_init__(self) -> None:
        super().__post_init__()
        _require_non_blank("proposed_mission_name", self.proposed_mission_name)
        _validate_default_prohibitions("prohibited_runtime_actions", self.prohibited_runtime_actions)

    @property
    def mission_installation_or_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalGatewayManifestCandidate(ExternalManifestCandidateBase):
    proposed_gateway_name: str = ""
    gateway_scope_summary: str = "Static gateway manifest candidate only."
    channel_summary: str = "No channel access is authorized."
    action_summary: str = "No gateway action execution is authorized."
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_MANIFEST_PROHIBITED_RUNTIME_ACTIONS))

    def __post_init__(self) -> None:
        super().__post_init__()
        _require_non_blank("proposed_gateway_name", self.proposed_gateway_name)
        _validate_default_prohibitions("prohibited_runtime_actions", self.prohibited_runtime_actions)

    @property
    def gateway_connection_or_message_action(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalProviderManifestCandidate(ExternalManifestCandidateBase):
    proposed_provider_name: str = ""
    provider_scope_summary: str = "Static provider manifest candidate only."
    routing_summary: str = "No provider routing is authorized."
    network_requirement_summary: str = "No network access is authorized."
    credential_requirement_summary: str = "No credential access is authorized."
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_MANIFEST_PROHIBITED_RUNTIME_ACTIONS))

    def __post_init__(self) -> None:
        super().__post_init__()
        _require_non_blank("proposed_provider_name", self.proposed_provider_name)
        _validate_default_prohibitions("prohibited_runtime_actions", self.prohibited_runtime_actions)

    @property
    def provider_network_or_credential_access(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalProfileManifestCandidate(ExternalManifestCandidateBase):
    proposed_profile_name: str = ""
    profile_scope_summary: str = "Static profile manifest candidate only."
    memory_scope_summary: str | None = None
    private_data_summary: str | None = None
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_MANIFEST_PROHIBITED_RUNTIME_ACTIONS))

    def __post_init__(self) -> None:
        super().__post_init__()
        _require_non_blank("proposed_profile_name", self.proposed_profile_name)
        _validate_default_prohibitions("prohibited_runtime_actions", self.prohibited_runtime_actions)

    @property
    def profile_activation_or_memory_access(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalManifestCandidateSet:
    candidate_set_id: str
    version: str
    source_input_id: str | None = None
    skill_candidates: list[ExternalSkillManifestCandidate] = field(default_factory=list)
    tool_candidates: list[ExternalToolManifestCandidate] = field(default_factory=list)
    plugin_candidates: list[ExternalPluginManifestCandidate] = field(default_factory=list)
    mission_candidates: list[ExternalMissionManifestCandidate] = field(default_factory=list)
    gateway_candidates: list[ExternalGatewayManifestCandidate] = field(default_factory=list)
    provider_candidates: list[ExternalProviderManifestCandidate] = field(default_factory=list)
    profile_candidates: list[ExternalProfileManifestCandidate] = field(default_factory=list)
    generic_candidate_refs: list[str] = field(default_factory=list)
    rejected_source_refs: list[str] = field(default_factory=list)
    deferred_source_refs: list[str] = field(default_factory=list)
    blocked_source_refs: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    ready_for_v0325_risk_classification: bool = True
    ready_for_v0326_digestion_candidate_generation: bool = True
    ready_for_manifest_activation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("candidate_set_id", self.candidate_set_id)
        _validate_version_includes_v0324(self.version)
        _validate_object_list("skill_candidates", self.skill_candidates, ExternalSkillManifestCandidate)
        _validate_object_list("tool_candidates", self.tool_candidates, ExternalToolManifestCandidate)
        _validate_object_list("plugin_candidates", self.plugin_candidates, ExternalPluginManifestCandidate)
        _validate_object_list("mission_candidates", self.mission_candidates, ExternalMissionManifestCandidate)
        _validate_object_list("gateway_candidates", self.gateway_candidates, ExternalGatewayManifestCandidate)
        _validate_object_list("provider_candidates", self.provider_candidates, ExternalProviderManifestCandidate)
        _validate_object_list("profile_candidates", self.profile_candidates, ExternalProfileManifestCandidate)
        for name in ("generic_candidate_refs", "rejected_source_refs", "deferred_source_refs", "blocked_source_refs", "evidence_refs"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, ("ready_for_manifest_activation", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"registry", "runtime_registry", "active_manifest_set"}):
            raise ValueError("ExternalManifestCandidateSet is not registry")

    @property
    def registry(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalManifestExtractionInput:
    extraction_input_id: str
    source_version: str = V0324_VERSION
    external_harness_profile_ids: list[str] = field(default_factory=list)
    reference_inventory_ids: list[str] = field(default_factory=list)
    reference_corpus_snapshot_ids: list[str] = field(default_factory=list)
    opencode_output_ids: list[str] = field(default_factory=list)
    openclaw_output_ids: list[str] = field(default_factory=list)
    hermes_output_ids: list[str] = field(default_factory=list)
    source_refs: list[ExternalManifestSourceRef] = field(default_factory=list)
    requested_candidate_kinds: list[ExternalManifestCandidateKind | str] = field(default_factory=list)
    extraction_rules: list[ExternalManifestExtractionRule] = field(default_factory=list)
    task_summary: str = "External manifest extraction contract input."
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_MANIFEST_PROHIBITED_RUNTIME_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("extraction_input_id", self.extraction_input_id)
        _require_non_blank("source_version", self.source_version)
        for name in ("external_harness_profile_ids", "reference_inventory_ids", "reference_corpus_snapshot_ids", "opencode_output_ids", "openclaw_output_ids", "hermes_output_ids"):
            _validate_string_list(name, getattr(self, name))
        _validate_object_list("source_refs", self.source_refs, ExternalManifestSourceRef)
        _validate_kind_list("requested_candidate_kinds", self.requested_candidate_kinds, ExternalManifestCandidateKind)
        _validate_object_list("extraction_rules", self.extraction_rules, ExternalManifestExtractionRule)
        _require_non_blank("task_summary", self.task_summary)
        _validate_default_prohibitions("prohibited_runtime_actions", self.prohibited_runtime_actions)
        if _metadata_flag_true(self.metadata, {"execution_request", "runtime_input"}):
            raise ValueError("ExternalManifestExtractionInput is not execution request")

    @property
    def execution_request(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalManifestExtractionFinding:
    finding_id: str
    extraction_input_id: str
    source_ref_ids: list[str]
    candidate_kind: ExternalManifestCandidateKind | str
    summary: str
    inferred_capability_kinds: list[ExternalManifestCapabilityKind | str] = field(default_factory=list)
    inferred_effect_surfaces: list[ExternalManifestEffectSurfaceKind | str] = field(default_factory=list)
    inferred_risk_surfaces: list[ExternalManifestRiskSurfaceKind | str] = field(default_factory=list)
    evidence_quality: ExternalManifestEvidenceQuality | str = ExternalManifestEvidenceQuality.UNKNOWN
    evidence_refs: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("extraction_input_id", self.extraction_input_id)
        _validate_string_list("source_ref_ids", self.source_ref_ids)
        ExternalManifestCandidateKind(self.candidate_kind)
        _require_non_blank("summary", self.summary)
        _validate_kind_list("inferred_capability_kinds", self.inferred_capability_kinds, ExternalManifestCapabilityKind)
        _validate_kind_list("inferred_effect_surfaces", self.inferred_effect_surfaces, ExternalManifestEffectSurfaceKind)
        _validate_kind_list("inferred_risk_surfaces", self.inferred_risk_surfaces, ExternalManifestRiskSurfaceKind)
        ExternalManifestEvidenceQuality(self.evidence_quality)
        for name in ("evidence_refs", "assumptions", "limitations"):
            _validate_string_list(name, getattr(self, name))
        if _metadata_flag_true(self.metadata, {"certification", "manifest_activation"}):
            raise ValueError("ExternalManifestExtractionFinding is not certification or activation")

    @property
    def certification(self) -> bool:
        return False

    @property
    def manifest_activation(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalManifestExtractionReport:
    report_id: str
    version: str
    extraction_input_id: str
    candidate_set_id: str | None = None
    findings: list[ExternalManifestExtractionFinding] = field(default_factory=list)
    extraction_status: ExternalManifestExtractionStatus | str = ExternalManifestExtractionStatus.EXTRACTED_WITH_GAPS
    summary: str = "External manifest extraction report; no runtime extraction."
    extracted_candidate_count: int = 0
    blocked_items: list[str] = field(default_factory=list)
    deferred_items: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0325_risk_classification: bool = True
    ready_for_v0326_digestion_candidate_generation: bool = True
    ready_for_manifest_activation: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0324(self.version)
        _require_non_blank("extraction_input_id", self.extraction_input_id)
        _validate_object_list("findings", self.findings, ExternalManifestExtractionFinding)
        ExternalManifestExtractionStatus(self.extraction_status)
        _require_non_blank("summary", self.summary)
        if self.extracted_candidate_count < 0:
            raise ValueError("extracted_candidate_count must be >= 0")
        for name in ("blocked_items", "deferred_items", "gaps", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, ("ready_for_manifest_activation", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"runtime_extraction", "manifest_activation", "execution_ready"}):
            raise ValueError("ExternalManifestExtractionReport is not runtime extraction")

    @property
    def runtime_extraction(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalManifestExtractionRunPreview:
    run_preview_id: str
    extraction_input_id: str | None = None
    planned_steps: list[str] = field(default_factory=list)
    expected_artifacts: list[str] = field(default_factory=list)
    explicitly_not_performed: list[str] = field(default_factory=list)
    no_harness_execution_guarantee: bool = True
    no_reference_code_execution_guarantee: bool = True
    no_install_guarantee: bool = True
    no_import_runtime_guarantee: bool = True
    no_plugin_loading_guarantee: bool = True
    no_tool_registration_guarantee: bool = True
    no_tool_invocation_guarantee: bool = True
    no_mission_installation_guarantee: bool = True
    no_mission_execution_guarantee: bool = True
    no_provider_invocation_guarantee: bool = True
    no_gateway_connection_guarantee: bool = True
    no_network_access_guarantee: bool = True
    no_credential_access_guarantee: bool = True
    no_command_execution_guarantee: bool = True
    no_secret_file_read_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        for name in (
            "no_harness_execution_guarantee",
            "no_reference_code_execution_guarantee",
            "no_install_guarantee",
            "no_import_runtime_guarantee",
            "no_plugin_loading_guarantee",
            "no_tool_registration_guarantee",
            "no_tool_invocation_guarantee",
            "no_mission_installation_guarantee",
            "no_mission_execution_guarantee",
            "no_provider_invocation_guarantee",
            "no_gateway_connection_guarantee",
            "no_network_access_guarantee",
            "no_credential_access_guarantee",
            "no_command_execution_guarantee",
            "no_secret_file_read_guarantee",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.32.4")

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalManifestNoRuntimeGuarantee:
    guarantee_id: str
    version: str
    no_manifest_activation: bool = True
    no_harness_execution: bool = True
    no_reference_code_execution: bool = True
    no_dependency_install: bool = True
    no_import_runtime: bool = True
    no_plugin_loading: bool = True
    no_external_plugin_loading: bool = True
    no_tool_registration: bool = True
    no_tool_invocation: bool = True
    no_mission_installation: bool = True
    no_mission_execution: bool = True
    no_gateway_connection: bool = True
    no_provider_invocation: bool = True
    no_network_access: bool = True
    no_credential_access: bool = True
    no_secret_file_read: bool = True
    no_command_execution: bool = True
    no_registry_mutation: bool = True
    no_memory_mutation: bool = True
    no_ocel_emission: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version_includes_v0324(self.version)
        for name in (
            "no_manifest_activation",
            "no_harness_execution",
            "no_reference_code_execution",
            "no_dependency_install",
            "no_import_runtime",
            "no_plugin_loading",
            "no_external_plugin_loading",
            "no_tool_registration",
            "no_tool_invocation",
            "no_mission_installation",
            "no_mission_execution",
            "no_gateway_connection",
            "no_provider_invocation",
            "no_network_access",
            "no_credential_access",
            "no_secret_file_read",
            "no_command_execution",
            "no_registry_mutation",
            "no_memory_mutation",
            "no_ocel_emission",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.32.4")
        _validate_string_list("evidence_refs", self.evidence_refs)


@dataclass(frozen=True)
class V0324ReadinessReport:
    report_id: str
    version: str
    extraction_report_id: str | None = None
    candidate_set_id: str | None = None
    summary: str = "v0.32.4 is ready for risk classification and digestion candidate generation design-stage handoff only, not execution."
    ready_for_v0325_risk_classification: bool = True
    ready_for_v0326_digestion_candidate_generation: bool = True
    ready_for_manifest_activation: bool = False
    ready_for_execution: bool = False
    ready_for_harness_execution: bool = False
    ready_for_reference_code_execution: bool = False
    ready_for_plugin_loading: bool = False
    ready_for_tool_registration: bool = False
    ready_for_tool_invocation: bool = False
    ready_for_mission_installation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_gateway_connection: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_MANIFEST_PROHIBITED_RUNTIME_ACTIONS))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0324(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(
            self,
            (
                "ready_for_manifest_activation",
                "ready_for_execution",
                "ready_for_harness_execution",
                "ready_for_reference_code_execution",
                "ready_for_plugin_loading",
                "ready_for_tool_registration",
                "ready_for_tool_invocation",
                "ready_for_mission_installation",
                "ready_for_provider_invocation",
                "ready_for_gateway_connection",
                "ready_for_network_access",
                "ready_for_credential_access",
                "ready_for_command_execution",
            ),
        )
        for name in ("completed_items", "blocked_items", "future_track_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_default_prohibitions("prohibited_until_later_gate", self.prohibited_until_later_gate)
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "execution_ready"}):
            raise ValueError("V0324ReadinessReport is not runtime enablement")


def build_external_manifest_source_ref(source_ref_id: str, source_kind: ExternalManifestSourceKind | str, source_id: str, harness_kind: str | None = None, reference_entry_ids: list[str] | None = None, manifest_path_refs: list[str] | None = None, evidence_refs: list[str] | None = None, metadata: dict[str, Any] | None = None) -> ExternalManifestSourceRef:
    return ExternalManifestSourceRef(source_ref_id=source_ref_id, source_kind=source_kind, source_id=source_id, harness_kind=harness_kind, reference_entry_ids=list(reference_entry_ids or []), manifest_path_refs=list(manifest_path_refs or []), evidence_refs=list(evidence_refs or []), metadata=dict(metadata or {}))


def build_external_manifest_field_observation(field_observation_id: str, field_name: str, field_summary: str, **kwargs: Any) -> ExternalManifestFieldObservation:
    return ExternalManifestFieldObservation(field_observation_id=field_observation_id, field_name=field_name, field_summary=field_summary, **kwargs)


def build_external_manifest_extraction_rule(rule_id: str, name: str, description: str, **kwargs: Any) -> ExternalManifestExtractionRule:
    return ExternalManifestExtractionRule(rule_id=rule_id, name=name, description=description, **kwargs)


def _candidate_defaults(candidate_kind: ExternalManifestCandidateKind | str) -> dict[str, Any]:
    kind = ExternalManifestCandidateKind(candidate_kind)
    capabilities = {
        ExternalManifestCandidateKind.SKILL_MANIFEST: [ExternalManifestCapabilityKind.DECLARE_SKILL],
        ExternalManifestCandidateKind.TOOL_MANIFEST: [ExternalManifestCapabilityKind.DECLARE_TOOL],
        ExternalManifestCandidateKind.PLUGIN_MANIFEST: [ExternalManifestCapabilityKind.DECLARE_PLUGIN],
        ExternalManifestCandidateKind.EXTERNAL_PLUGIN_MANIFEST: [ExternalManifestCapabilityKind.DECLARE_EXTERNAL_PLUGIN],
        ExternalManifestCandidateKind.MISSION_MANIFEST: [ExternalManifestCapabilityKind.DECLARE_MISSION],
        ExternalManifestCandidateKind.GATEWAY_MANIFEST: [ExternalManifestCapabilityKind.DECLARE_GATEWAY],
        ExternalManifestCandidateKind.CHANNEL_MANIFEST: [ExternalManifestCapabilityKind.DECLARE_CHANNEL],
        ExternalManifestCandidateKind.PROVIDER_MANIFEST: [ExternalManifestCapabilityKind.DECLARE_PROVIDER],
        ExternalManifestCandidateKind.PROFILE_MANIFEST: [ExternalManifestCapabilityKind.DECLARE_PROFILE],
        ExternalManifestCandidateKind.MEMORY_SCHEMA_MANIFEST: [ExternalManifestCapabilityKind.DECLARE_MEMORY_SCHEMA],
        ExternalManifestCandidateKind.APPROVAL_POLICY_MANIFEST: [ExternalManifestCapabilityKind.DECLARE_APPROVAL_POLICY],
        ExternalManifestCandidateKind.AUDIT_POLICY_MANIFEST: [ExternalManifestCapabilityKind.DECLARE_AUDIT_POLICY],
        ExternalManifestCandidateKind.RESULT_ENVELOPE_MANIFEST: [ExternalManifestCapabilityKind.DECLARE_RESULT_ENVELOPE],
        ExternalManifestCandidateKind.OCEL_TRACE_MANIFEST: [ExternalManifestCapabilityKind.DECLARE_OCEL_TRACE],
    }.get(kind, [ExternalManifestCapabilityKind.UNKNOWN])
    return {
        "candidate_kind": kind,
        "status": ExternalManifestExtractionStatus.EXTRACTED_WITH_GAPS,
        "declared_capabilities": capabilities,
        "effect_surfaces": infer_manifest_effect_surfaces_from_candidate_kind(kind),
        "risk_surfaces": infer_manifest_risk_surfaces_from_candidate_kind(kind),
        "evidence_quality": ExternalManifestEvidenceQuality.SUFFICIENT_FOR_MANIFEST_CANDIDATE,
    }


def _merge_candidate_defaults(candidate_kind: ExternalManifestCandidateKind, kwargs: dict[str, Any]) -> dict[str, Any]:
    merged = _candidate_defaults(candidate_kind)
    merged.update(kwargs)
    return merged


def build_external_skill_manifest_candidate(manifest_candidate_id: str, declared_name: str, proposed_skill_name: str | None = None, **kwargs: Any) -> ExternalSkillManifestCandidate:
    return ExternalSkillManifestCandidate(manifest_candidate_id=manifest_candidate_id, declared_name=declared_name, proposed_skill_name=proposed_skill_name or declared_name, **_merge_candidate_defaults(ExternalManifestCandidateKind.SKILL_MANIFEST, kwargs))


def build_external_tool_manifest_candidate(manifest_candidate_id: str, declared_name: str, proposed_tool_name: str | None = None, **kwargs: Any) -> ExternalToolManifestCandidate:
    return ExternalToolManifestCandidate(manifest_candidate_id=manifest_candidate_id, declared_name=declared_name, proposed_tool_name=proposed_tool_name or declared_name, **_merge_candidate_defaults(ExternalManifestCandidateKind.TOOL_MANIFEST, kwargs))


def build_external_plugin_manifest_candidate(manifest_candidate_id: str, declared_name: str, proposed_plugin_name: str | None = None, external_plugin: bool = False, **kwargs: Any) -> ExternalPluginManifestCandidate:
    kind = ExternalManifestCandidateKind.EXTERNAL_PLUGIN_MANIFEST if external_plugin else ExternalManifestCandidateKind.PLUGIN_MANIFEST
    return ExternalPluginManifestCandidate(manifest_candidate_id=manifest_candidate_id, declared_name=declared_name, proposed_plugin_name=proposed_plugin_name or declared_name, external_plugin=external_plugin, **_merge_candidate_defaults(kind, kwargs))


def build_external_mission_manifest_candidate(manifest_candidate_id: str, declared_name: str, proposed_mission_name: str | None = None, **kwargs: Any) -> ExternalMissionManifestCandidate:
    return ExternalMissionManifestCandidate(manifest_candidate_id=manifest_candidate_id, declared_name=declared_name, proposed_mission_name=proposed_mission_name or declared_name, **_merge_candidate_defaults(ExternalManifestCandidateKind.MISSION_MANIFEST, kwargs))


def build_external_gateway_manifest_candidate(manifest_candidate_id: str, declared_name: str, proposed_gateway_name: str | None = None, **kwargs: Any) -> ExternalGatewayManifestCandidate:
    return ExternalGatewayManifestCandidate(manifest_candidate_id=manifest_candidate_id, declared_name=declared_name, proposed_gateway_name=proposed_gateway_name or declared_name, **_merge_candidate_defaults(ExternalManifestCandidateKind.GATEWAY_MANIFEST, kwargs))


def build_external_provider_manifest_candidate(manifest_candidate_id: str, declared_name: str, proposed_provider_name: str | None = None, **kwargs: Any) -> ExternalProviderManifestCandidate:
    return ExternalProviderManifestCandidate(manifest_candidate_id=manifest_candidate_id, declared_name=declared_name, proposed_provider_name=proposed_provider_name or declared_name, **_merge_candidate_defaults(ExternalManifestCandidateKind.PROVIDER_MANIFEST, kwargs))


def build_external_profile_manifest_candidate(manifest_candidate_id: str, declared_name: str, proposed_profile_name: str | None = None, **kwargs: Any) -> ExternalProfileManifestCandidate:
    return ExternalProfileManifestCandidate(manifest_candidate_id=manifest_candidate_id, declared_name=declared_name, proposed_profile_name=proposed_profile_name or declared_name, **_merge_candidate_defaults(ExternalManifestCandidateKind.PROFILE_MANIFEST, kwargs))


def build_external_manifest_candidate_set(candidate_set_id: str, **kwargs: Any) -> ExternalManifestCandidateSet:
    return ExternalManifestCandidateSet(candidate_set_id=candidate_set_id, version=V0324_VERSION, **kwargs)


def build_external_manifest_extraction_input(extraction_input_id: str, **kwargs: Any) -> ExternalManifestExtractionInput:
    return ExternalManifestExtractionInput(extraction_input_id=extraction_input_id, **kwargs)


def build_external_manifest_extraction_finding(finding_id: str, extraction_input_id: str, source_ref_ids: list[str], candidate_kind: ExternalManifestCandidateKind | str, summary: str, **kwargs: Any) -> ExternalManifestExtractionFinding:
    return ExternalManifestExtractionFinding(finding_id=finding_id, extraction_input_id=extraction_input_id, source_ref_ids=list(source_ref_ids), candidate_kind=candidate_kind, summary=summary, **kwargs)


def build_external_manifest_extraction_report(report_id: str, extraction_input_id: str, **kwargs: Any) -> ExternalManifestExtractionReport:
    return ExternalManifestExtractionReport(report_id=report_id, version=V0324_VERSION, extraction_input_id=extraction_input_id, **kwargs)


def build_external_manifest_extraction_run_preview(run_preview_id: str = "external_manifest_extraction_run_preview:v0.32.4", **kwargs: Any) -> ExternalManifestExtractionRunPreview:
    return ExternalManifestExtractionRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_external_manifest_no_runtime_guarantee(guarantee_id: str = "external_manifest_no_runtime_guarantee:v0.32.4", evidence_refs: list[str] | None = None, metadata: dict[str, Any] | None = None) -> ExternalManifestNoRuntimeGuarantee:
    return ExternalManifestNoRuntimeGuarantee(guarantee_id=guarantee_id, version=V0324_VERSION, evidence_refs=list(evidence_refs or []), metadata=dict(metadata or {}))


def build_v0324_readiness_report(report_id: str = "v0324_readiness_report", extraction_report_id: str | None = None, candidate_set_id: str | None = None, **kwargs: Any) -> V0324ReadinessReport:
    return V0324ReadinessReport(report_id=report_id, version=V0324_VERSION, extraction_report_id=extraction_report_id, candidate_set_id=candidate_set_id, **kwargs)


def infer_manifest_candidate_kind_from_inventory_entry(entry: ReferenceFileInventoryEntry) -> ExternalManifestCandidateKind:
    name = entry.file_name.lower()
    path = entry.relative_path.lower()
    detected = (entry.detected_kind or "").lower()
    extension = entry.file_extension or ""
    if any(pattern.strip("*").lower() in path for pattern in DEFAULT_PROHIBITED_FILE_PATTERNS):
        return ExternalManifestCandidateKind.UNKNOWN
    if "external" in path and "plugin" in path:
        return ExternalManifestCandidateKind.EXTERNAL_PLUGIN_MANIFEST
    if "plugin" in path or "plugin" in name:
        return ExternalManifestCandidateKind.PLUGIN_MANIFEST
    if "skill" in path or "skill" in name:
        return ExternalManifestCandidateKind.SKILL_MANIFEST
    if "tool" in path or "tool" in name:
        return ExternalManifestCandidateKind.TOOL_MANIFEST
    if "mission" in path or "mission" in name:
        return ExternalManifestCandidateKind.MISSION_MANIFEST
    if "gateway" in path or "gateway" in name:
        return ExternalManifestCandidateKind.GATEWAY_MANIFEST
    if "channel" in path or "channel" in name:
        return ExternalManifestCandidateKind.CHANNEL_MANIFEST
    if "provider" in path or "provider" in name or "model" in path:
        return ExternalManifestCandidateKind.PROVIDER_MANIFEST
    if "profile" in path or "profile" in name:
        return ExternalManifestCandidateKind.PROFILE_MANIFEST
    if "memory" in path:
        return ExternalManifestCandidateKind.MEMORY_SCHEMA_MANIFEST
    if "approval" in path or "policy" in path:
        return ExternalManifestCandidateKind.APPROVAL_POLICY_MANIFEST
    if "audit" in path:
        return ExternalManifestCandidateKind.AUDIT_POLICY_MANIFEST
    if "ocel" in path:
        return ExternalManifestCandidateKind.OCEL_TRACE_MANIFEST
    if "result" in path:
        return ExternalManifestCandidateKind.RESULT_ENVELOPE_MANIFEST
    if "manifest" in path or "manifest" in detected or "package" in name or "config" in path or extension in {".json", ".toml", ".yaml", ".yml"}:
        return ExternalManifestCandidateKind.GENERIC_MANIFEST
    return ExternalManifestCandidateKind.UNKNOWN


def infer_manifest_risk_surfaces_from_candidate_kind(candidate_kind: ExternalManifestCandidateKind | str) -> list[ExternalManifestRiskSurfaceKind]:
    kind = ExternalManifestCandidateKind(candidate_kind)
    return {
        ExternalManifestCandidateKind.SKILL_MANIFEST: [ExternalManifestRiskSurfaceKind.REGISTRY_MUTATION],
        ExternalManifestCandidateKind.TOOL_MANIFEST: [ExternalManifestRiskSurfaceKind.TOOL_REGISTRATION, ExternalManifestRiskSurfaceKind.TOOL_INVOCATION],
        ExternalManifestCandidateKind.PLUGIN_MANIFEST: [ExternalManifestRiskSurfaceKind.PLUGIN_LOADING],
        ExternalManifestCandidateKind.EXTERNAL_PLUGIN_MANIFEST: [ExternalManifestRiskSurfaceKind.EXTERNAL_PLUGIN_LOADING, ExternalManifestRiskSurfaceKind.RUNTIME_IMPORT],
        ExternalManifestCandidateKind.MISSION_MANIFEST: [ExternalManifestRiskSurfaceKind.MISSION_INSTALLATION, ExternalManifestRiskSurfaceKind.MISSION_EXECUTION],
        ExternalManifestCandidateKind.GATEWAY_MANIFEST: [ExternalManifestRiskSurfaceKind.GATEWAY_CONNECTION, ExternalManifestRiskSurfaceKind.MESSAGE_SEND],
        ExternalManifestCandidateKind.CHANNEL_MANIFEST: [ExternalManifestRiskSurfaceKind.CHANNEL_ACCESS, ExternalManifestRiskSurfaceKind.MESSAGE_SEND],
        ExternalManifestCandidateKind.PROVIDER_MANIFEST: [ExternalManifestRiskSurfaceKind.PROVIDER_INVOCATION, ExternalManifestRiskSurfaceKind.NETWORK_ACCESS, ExternalManifestRiskSurfaceKind.CREDENTIAL_ACCESS],
        ExternalManifestCandidateKind.PROFILE_MANIFEST: [ExternalManifestRiskSurfaceKind.PRIVATE_DATA_EXPOSURE, ExternalManifestRiskSurfaceKind.MEMORY_MUTATION],
        ExternalManifestCandidateKind.MEMORY_SCHEMA_MANIFEST: [ExternalManifestRiskSurfaceKind.MEMORY_MUTATION, ExternalManifestRiskSurfaceKind.PRIVATE_DATA_EXPOSURE],
        ExternalManifestCandidateKind.APPROVAL_POLICY_MANIFEST: [ExternalManifestRiskSurfaceKind.REGISTRY_MUTATION],
        ExternalManifestCandidateKind.AUDIT_POLICY_MANIFEST: [ExternalManifestRiskSurfaceKind.RAW_OUTPUT_PERSISTENCE],
        ExternalManifestCandidateKind.OCEL_TRACE_MANIFEST: [ExternalManifestRiskSurfaceKind.OCEL_EMISSION],
        ExternalManifestCandidateKind.RESULT_ENVELOPE_MANIFEST: [ExternalManifestRiskSurfaceKind.RAW_OUTPUT_PERSISTENCE],
        ExternalManifestCandidateKind.GENERIC_MANIFEST: [ExternalManifestRiskSurfaceKind.UNKNOWN],
    }.get(kind, [ExternalManifestRiskSurfaceKind.UNKNOWN])


def infer_manifest_effect_surfaces_from_candidate_kind(candidate_kind: ExternalManifestCandidateKind | str) -> list[ExternalManifestEffectSurfaceKind]:
    kind = ExternalManifestCandidateKind(candidate_kind)
    return {
        ExternalManifestCandidateKind.SKILL_MANIFEST: [ExternalManifestEffectSurfaceKind.REGISTRY],
        ExternalManifestCandidateKind.TOOL_MANIFEST: [ExternalManifestEffectSurfaceKind.TOOL_REGISTRY],
        ExternalManifestCandidateKind.PLUGIN_MANIFEST: [ExternalManifestEffectSurfaceKind.PLUGIN_RUNTIME],
        ExternalManifestCandidateKind.EXTERNAL_PLUGIN_MANIFEST: [ExternalManifestEffectSurfaceKind.PLUGIN_RUNTIME, ExternalManifestEffectSurfaceKind.NETWORK],
        ExternalManifestCandidateKind.MISSION_MANIFEST: [ExternalManifestEffectSurfaceKind.MISSION_RUNTIME],
        ExternalManifestCandidateKind.GATEWAY_MANIFEST: [ExternalManifestEffectSurfaceKind.GATEWAY_RUNTIME],
        ExternalManifestCandidateKind.CHANNEL_MANIFEST: [ExternalManifestEffectSurfaceKind.CHANNEL_RUNTIME],
        ExternalManifestCandidateKind.PROVIDER_MANIFEST: [ExternalManifestEffectSurfaceKind.PROVIDER_RUNTIME, ExternalManifestEffectSurfaceKind.NETWORK, ExternalManifestEffectSurfaceKind.CREDENTIAL],
        ExternalManifestCandidateKind.PROFILE_MANIFEST: [ExternalManifestEffectSurfaceKind.PRIVATE_DATA, ExternalManifestEffectSurfaceKind.MEMORY],
        ExternalManifestCandidateKind.MEMORY_SCHEMA_MANIFEST: [ExternalManifestEffectSurfaceKind.MEMORY],
        ExternalManifestCandidateKind.APPROVAL_POLICY_MANIFEST: [ExternalManifestEffectSurfaceKind.POLICY],
        ExternalManifestCandidateKind.AUDIT_POLICY_MANIFEST: [ExternalManifestEffectSurfaceKind.RAW_OUTPUT],
        ExternalManifestCandidateKind.OCEL_TRACE_MANIFEST: [ExternalManifestEffectSurfaceKind.OCEL_TRACE],
        ExternalManifestCandidateKind.RESULT_ENVELOPE_MANIFEST: [ExternalManifestEffectSurfaceKind.RAW_OUTPUT],
        ExternalManifestCandidateKind.GENERIC_MANIFEST: [ExternalManifestEffectSurfaceKind.NO_EFFECT],
    }.get(kind, [ExternalManifestEffectSurfaceKind.UNKNOWN])


def manifest_candidate_preserves_no_activation(candidate: ExternalManifestCandidateBase) -> bool:
    return candidate.ready_for_manifest_activation is False and candidate.ready_for_execution is False and candidate.active_manifest is False


def manifest_candidate_set_is_not_registry(candidate_set: ExternalManifestCandidateSet) -> bool:
    return candidate_set.ready_for_manifest_activation is False and candidate_set.ready_for_execution is False and candidate_set.registry is False


def manifest_extraction_report_is_not_runtime(report: ExternalManifestExtractionReport) -> bool:
    return report.ready_for_manifest_activation is False and report.ready_for_execution is False and report.runtime_extraction is False


def v0324_readiness_report_is_not_runtime_ready(report: V0324ReadinessReport) -> bool:
    return (
        report.ready_for_manifest_activation is False
        and report.ready_for_execution is False
        and report.ready_for_harness_execution is False
        and report.ready_for_reference_code_execution is False
        and report.ready_for_plugin_loading is False
        and report.ready_for_tool_registration is False
        and report.ready_for_tool_invocation is False
        and report.ready_for_mission_installation is False
        and report.ready_for_provider_invocation is False
        and report.ready_for_gateway_connection is False
        and report.ready_for_network_access is False
        and report.ready_for_credential_access is False
        and report.ready_for_command_execution is False
    )
