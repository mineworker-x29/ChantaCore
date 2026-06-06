from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .profiles import _metadata_flag_true, _require_non_blank, _validate_object_list, _validate_string_list
from .reference_corpus import ReferenceFileInventoryEntry


V0321_VERSION = "v0.32.1"
V0321_RELEASE_NAME = "v0.32.1 OpenCode-style Harness Observation Profile"

DEFAULT_OPENCODE_PROHIBITED_RUNTIME_ACTIONS = [
    "OpenCode execution",
    "reference code execution",
    "install",
    "import runtime",
    "workspace write",
    "code edit",
    "patch application",
    "tool invocation",
    "tool registration",
    "plugin loading",
    "external plugin loading",
    "provider invocation",
    "command",
    "shell",
    "network",
    "credential",
    "secret file read",
    "registry mutation",
    "memory mutation",
    "OCEL emission",
]

HIGH_RISK_CAPABILITIES = {
    "write_file",
    "edit_code",
    "apply_patch",
    "invoke_tool",
    "register_tool",
    "load_plugin",
    "load_external_plugin",
    "invoke_provider",
    "execute_command",
    "execute_shell",
    "dependency_resolution",
}


class OpenCodeHarnessSurfaceKind(StrEnum):
    WORKSPACE_TREE_SURFACE = "workspace_tree_surface"
    FILE_READ_SURFACE = "file_read_surface"
    FILE_WRITE_SURFACE = "file_write_surface"
    CODE_EDIT_SURFACE = "code_edit_surface"
    PATCH_SURFACE = "patch_surface"
    SEARCH_SURFACE = "search_surface"
    TOOL_REGISTRY_SURFACE = "tool_registry_surface"
    TOOL_INVOCATION_SURFACE = "tool_invocation_surface"
    PLUGIN_MANIFEST_SURFACE = "plugin_manifest_surface"
    PLUGIN_RUNTIME_SURFACE = "plugin_runtime_surface"
    EXTERNAL_PLUGIN_SURFACE = "external_plugin_surface"
    PROVIDER_HOOK_SURFACE = "provider_hook_surface"
    COMMAND_EXECUTION_SURFACE = "command_execution_surface"
    SHELL_SURFACE = "shell_surface"
    LSP_EDITOR_SURFACE = "lsp_editor_surface"
    CONFIGURATION_MANIFEST_SURFACE = "configuration_manifest_surface"
    DEPENDENCY_MANIFEST_SURFACE = "dependency_manifest_surface"
    APPROVAL_BOUNDARY_SURFACE = "approval_boundary_surface"
    AUDIT_BOUNDARY_SURFACE = "audit_boundary_surface"
    RESULT_ENVELOPE_SURFACE = "result_envelope_surface"
    OCEL_TRACE_SURFACE = "ocel_trace_surface"
    UNKNOWN = "unknown"


class OpenCodeObservationFocusKind(StrEnum):
    WORKSPACE_STRUCTURE = "workspace_structure"
    FILE_OPERATION_MODEL = "file_operation_model"
    CODE_EDIT_MODEL = "code_edit_model"
    PATCH_MODEL = "patch_model"
    SEARCH_MODEL = "search_model"
    TOOL_REGISTRY_MODEL = "tool_registry_model"
    PLUGIN_MODEL = "plugin_model"
    EXTERNAL_PLUGIN_MODEL = "external_plugin_model"
    PROVIDER_HOOK_MODEL = "provider_hook_model"
    COMMAND_EXECUTION_BOUNDARY = "command_execution_boundary"
    SHELL_BOUNDARY = "shell_boundary"
    LSP_EDITOR_BOUNDARY = "lsp_editor_boundary"
    DEPENDENCY_MANIFEST = "dependency_manifest"
    CONFIGURATION_MANIFEST = "configuration_manifest"
    APPROVAL_BOUNDARY = "approval_boundary"
    AUDIT_BOUNDARY = "audit_boundary"
    RESULT_ENVELOPE = "result_envelope"
    OCEL_TRACE_RELEVANCE = "ocel_trace_relevance"
    DIGESTION_RELEVANCE = "digestion_relevance"
    DOMINION_RELEVANCE = "dominion_relevance"
    UNKNOWN = "unknown"


class OpenCodeCapabilityKind(StrEnum):
    READ_WORKSPACE = "read_workspace"
    READ_FILE = "read_file"
    WRITE_FILE = "write_file"
    EDIT_CODE = "edit_code"
    APPLY_PATCH = "apply_patch"
    SEARCH_WORKSPACE = "search_workspace"
    INVOKE_TOOL = "invoke_tool"
    REGISTER_TOOL = "register_tool"
    LOAD_PLUGIN = "load_plugin"
    LOAD_EXTERNAL_PLUGIN = "load_external_plugin"
    INVOKE_PROVIDER = "invoke_provider"
    EXECUTE_COMMAND = "execute_command"
    EXECUTE_SHELL = "execute_shell"
    EDITOR_INTEGRATION = "editor_integration"
    DEPENDENCY_RESOLUTION = "dependency_resolution"
    CONFIG_LOADING = "config_loading"
    APPROVAL_GATE = "approval_gate"
    AUDIT_TRACE = "audit_trace"
    RESULT_ENVELOPE = "result_envelope"
    UNKNOWN = "unknown"


class OpenCodeRiskSignalKind(StrEnum):
    WORKSPACE_WRITE_RISK = "workspace_write_risk"
    CODE_EDIT_RISK = "code_edit_risk"
    PATCH_APPLICATION_RISK = "patch_application_risk"
    COMMAND_EXECUTION_RISK = "command_execution_risk"
    SHELL_EXECUTION_RISK = "shell_execution_risk"
    PROVIDER_INVOCATION_RISK = "provider_invocation_risk"
    NETWORK_ACCESS_RISK = "network_access_risk"
    CREDENTIAL_ACCESS_RISK = "credential_access_risk"
    PLUGIN_LOADING_RISK = "plugin_loading_risk"
    EXTERNAL_PLUGIN_RISK = "external_plugin_risk"
    DEPENDENCY_INSTALL_RISK = "dependency_install_risk"
    TOOL_REGISTRY_MUTATION_RISK = "tool_registry_mutation_risk"
    TOOL_INVOCATION_RISK = "tool_invocation_risk"
    LSP_EDITOR_RUNTIME_RISK = "lsp_editor_runtime_risk"
    RAW_OUTPUT_PERSISTENCE_RISK = "raw_output_persistence_risk"
    SECRET_FILE_READ_RISK = "secret_file_read_risk"
    MEMORY_MUTATION_RISK = "memory_mutation_risk"
    REGISTRY_MUTATION_RISK = "registry_mutation_risk"
    OCEL_EMISSION_RISK = "ocel_emission_risk"
    UNKNOWN = "unknown"


class OpenCodeObservationStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    OBSERVED = "observed"
    OBSERVED_WITH_GAPS = "observed_with_gaps"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class OpenCodeEvidenceQuality(StrEnum):
    UNKNOWN = "unknown"
    NONE = "none"
    WEAK = "weak"
    PARTIAL = "partial"
    SUFFICIENT_FOR_STATIC_OBSERVATION = "sufficient_for_static_observation"
    SUFFICIENT_FOR_PROFILE = "sufficient_for_profile"
    SUFFICIENT_FOR_MANIFEST_EXTRACTION_REVIEW = "sufficient_for_manifest_extraction_review"
    CONFLICTING = "conflicting"
    BLOCKED = "blocked"


def _validate_version_includes_v0321(version: str) -> None:
    _require_non_blank("version", version)
    if V0321_VERSION not in version:
        raise ValueError("version must include v0.32.1")


def _validate_kind_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _validate_default_prohibitions(name: str, values: list[str]) -> None:
    _validate_string_list(name, values)
    missing = set(DEFAULT_OPENCODE_PROHIBITED_RUNTIME_ACTIONS) - set(values)
    if missing:
        raise ValueError(f"{name} missing v0.32.1 prohibitions: {sorted(missing)}")


def _capability_is_high_risk(value: OpenCodeCapabilityKind | str) -> bool:
    return OpenCodeCapabilityKind(value).value in HIGH_RISK_CAPABILITIES


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.32.1")


@dataclass(frozen=True)
class OpenCodeReferenceSourceRef:
    source_ref_id: str
    reference_source_id: str | None = None
    reference_inventory_id: str | None = None
    reference_entry_ids: list[str] = field(default_factory=list)
    local_path_ref: str | None = None
    source_label: str = "OpenCode-style static reference"
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        _require_non_blank("source_label", self.source_label)
        _validate_string_list("reference_entry_ids", self.reference_entry_ids)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"source_fetch", "execution"}):
            raise ValueError("OpenCodeReferenceSourceRef is not source fetch or execution")

    @property
    def source_fetch(self) -> bool:
        return False

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenCodeSurfaceObservation:
    observation_id: str
    surface_kind: OpenCodeHarnessSurfaceKind | str
    focus_kind: OpenCodeObservationFocusKind | str
    capability_kind: OpenCodeCapabilityKind | str
    title: str
    summary: str
    source_refs: list[OpenCodeReferenceSourceRef] = field(default_factory=list)
    evidence_quality: OpenCodeEvidenceQuality | str = OpenCodeEvidenceQuality.UNKNOWN
    risk_signal_kinds: list[OpenCodeRiskSignalKind | str] = field(default_factory=list)
    boundary_notes: list[str] = field(default_factory=list)
    prohibited_runtime_actions: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("observation_id", self.observation_id)
        OpenCodeHarnessSurfaceKind(self.surface_kind)
        OpenCodeObservationFocusKind(self.focus_kind)
        capability = OpenCodeCapabilityKind(self.capability_kind)
        _require_non_blank("title", self.title)
        _require_non_blank("summary", self.summary)
        _validate_object_list("source_refs", self.source_refs, OpenCodeReferenceSourceRef)
        OpenCodeEvidenceQuality(self.evidence_quality)
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, OpenCodeRiskSignalKind)
        for name in ("boundary_notes", "prohibited_runtime_actions", "assumptions", "limitations"):
            _validate_string_list(name, getattr(self, name))
        if capability.value in HIGH_RISK_CAPABILITIES and not self.prohibited_runtime_actions:
            raise ValueError("high-risk capabilities require prohibited_runtime_actions")
        if _metadata_flag_true(self.metadata, {"permission", "runtime_surface"}):
            raise ValueError("OpenCodeSurfaceObservation is not permission")

    @property
    def permission(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenCodeWorkspaceSurfaceObservation:
    workspace_observation_id: str
    source_refs: list[OpenCodeReferenceSourceRef] = field(default_factory=list)
    file_tree_summary: str = "Static workspace structure observation only."
    documentation_candidate_paths: list[str] = field(default_factory=list)
    manifest_candidate_paths: list[str] = field(default_factory=list)
    config_candidate_paths: list[str] = field(default_factory=list)
    risk_surface_candidate_paths: list[str] = field(default_factory=list)
    write_surface_detected: bool = False
    patch_surface_detected: bool = False
    command_surface_detected: bool = False
    ready_for_workspace_access: bool = False
    ready_for_workspace_write: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("workspace_observation_id", self.workspace_observation_id)
        _validate_object_list("source_refs", self.source_refs, OpenCodeReferenceSourceRef)
        _require_non_blank("file_tree_summary", self.file_tree_summary)
        for name in ("documentation_candidate_paths", "manifest_candidate_paths", "config_candidate_paths", "risk_surface_candidate_paths"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, ("ready_for_workspace_access", "ready_for_workspace_write", "ready_for_execution"))

    @property
    def workspace_access(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenCodeToolRegistrySurfaceObservation:
    tool_registry_observation_id: str
    source_refs: list[OpenCodeReferenceSourceRef] = field(default_factory=list)
    possible_tool_manifest_paths: list[str] = field(default_factory=list)
    possible_tool_registry_paths: list[str] = field(default_factory=list)
    possible_tool_invocation_paths: list[str] = field(default_factory=list)
    declared_tool_names: list[str] = field(default_factory=list)
    risk_signal_kinds: list[OpenCodeRiskSignalKind | str] = field(default_factory=list)
    ready_for_tool_registration: bool = False
    ready_for_tool_invocation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("tool_registry_observation_id", self.tool_registry_observation_id)
        _validate_object_list("source_refs", self.source_refs, OpenCodeReferenceSourceRef)
        for name in ("possible_tool_manifest_paths", "possible_tool_registry_paths", "possible_tool_invocation_paths", "declared_tool_names"):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, OpenCodeRiskSignalKind)
        _validate_false(self, ("ready_for_tool_registration", "ready_for_tool_invocation", "ready_for_execution"))

    @property
    def registry_mutation(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenCodePluginSurfaceObservation:
    plugin_observation_id: str
    source_refs: list[OpenCodeReferenceSourceRef] = field(default_factory=list)
    possible_plugin_manifest_paths: list[str] = field(default_factory=list)
    possible_plugin_runtime_paths: list[str] = field(default_factory=list)
    possible_external_plugin_paths: list[str] = field(default_factory=list)
    declared_plugin_names: list[str] = field(default_factory=list)
    external_plugin_risk_detected: bool = False
    risk_signal_kinds: list[OpenCodeRiskSignalKind | str] = field(default_factory=list)
    ready_for_plugin_loading: bool = False
    ready_for_external_plugin_loading: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("plugin_observation_id", self.plugin_observation_id)
        _validate_object_list("source_refs", self.source_refs, OpenCodeReferenceSourceRef)
        for name in ("possible_plugin_manifest_paths", "possible_plugin_runtime_paths", "possible_external_plugin_paths", "declared_plugin_names"):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, OpenCodeRiskSignalKind)
        _validate_false(self, ("ready_for_plugin_loading", "ready_for_external_plugin_loading", "ready_for_execution"))

    @property
    def plugin_loading(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenCodeProviderHookSurfaceObservation:
    provider_hook_observation_id: str
    source_refs: list[OpenCodeReferenceSourceRef] = field(default_factory=list)
    possible_provider_config_paths: list[str] = field(default_factory=list)
    possible_provider_hook_paths: list[str] = field(default_factory=list)
    declared_provider_names: list[str] = field(default_factory=list)
    network_risk_detected: bool = False
    credential_risk_detected: bool = False
    risk_signal_kinds: list[OpenCodeRiskSignalKind | str] = field(default_factory=list)
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("provider_hook_observation_id", self.provider_hook_observation_id)
        _validate_object_list("source_refs", self.source_refs, OpenCodeReferenceSourceRef)
        for name in ("possible_provider_config_paths", "possible_provider_hook_paths", "declared_provider_names"):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, OpenCodeRiskSignalKind)
        _validate_false(self, ("ready_for_provider_invocation", "ready_for_network_access", "ready_for_credential_access", "ready_for_execution"))

    @property
    def provider_invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenCodeCommandRiskBoundary:
    command_boundary_id: str
    source_refs: list[OpenCodeReferenceSourceRef] = field(default_factory=list)
    possible_command_paths: list[str] = field(default_factory=list)
    possible_shell_paths: list[str] = field(default_factory=list)
    command_keywords_detected: list[str] = field(default_factory=list)
    shell_keywords_detected: list[str] = field(default_factory=list)
    risk_signal_kinds: list[OpenCodeRiskSignalKind | str] = field(default_factory=list)
    required_boundaries: list[str] = field(default_factory=list)
    ready_for_command_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("command_boundary_id", self.command_boundary_id)
        _validate_object_list("source_refs", self.source_refs, OpenCodeReferenceSourceRef)
        for name in ("possible_command_paths", "possible_shell_paths", "command_keywords_detected", "shell_keywords_detected", "required_boundaries"):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, OpenCodeRiskSignalKind)
        _validate_false(self, ("ready_for_command_execution", "ready_for_shell_execution", "ready_for_execution"))

    @property
    def command_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenCodeConfigManifestObservation:
    config_manifest_observation_id: str
    source_refs: list[OpenCodeReferenceSourceRef] = field(default_factory=list)
    possible_package_manifest_paths: list[str] = field(default_factory=list)
    possible_config_paths: list[str] = field(default_factory=list)
    possible_lockfile_paths: list[str] = field(default_factory=list)
    possible_script_entries: list[str] = field(default_factory=list)
    possible_dependency_entries: list[str] = field(default_factory=list)
    risk_signal_kinds: list[OpenCodeRiskSignalKind | str] = field(default_factory=list)
    ready_for_dependency_install: bool = False
    ready_for_script_execution: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("config_manifest_observation_id", self.config_manifest_observation_id)
        _validate_object_list("source_refs", self.source_refs, OpenCodeReferenceSourceRef)
        for name in ("possible_package_manifest_paths", "possible_config_paths", "possible_lockfile_paths", "possible_script_entries", "possible_dependency_entries"):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, OpenCodeRiskSignalKind)
        _validate_false(self, ("ready_for_dependency_install", "ready_for_script_execution", "ready_for_execution"))

    @property
    def dependency_install(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenCodeStaticObservationInput:
    opencode_input_id: str
    external_harness_profile_id: str | None = None
    reference_corpus_snapshot_id: str | None = None
    reference_inventory_ids: list[str] = field(default_factory=list)
    reference_source_refs: list[OpenCodeReferenceSourceRef] = field(default_factory=list)
    requested_focus: list[OpenCodeObservationFocusKind | str] = field(default_factory=list)
    task_summary: str = "OpenCode-style static observation contract input."
    source_version: str = V0321_VERSION
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_OPENCODE_PROHIBITED_RUNTIME_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("opencode_input_id", self.opencode_input_id)
        _validate_string_list("reference_inventory_ids", self.reference_inventory_ids)
        _validate_object_list("reference_source_refs", self.reference_source_refs, OpenCodeReferenceSourceRef)
        _validate_kind_list("requested_focus", self.requested_focus, OpenCodeObservationFocusKind)
        _require_non_blank("task_summary", self.task_summary)
        _require_non_blank("source_version", self.source_version)
        _validate_default_prohibitions("prohibited_runtime_actions", self.prohibited_runtime_actions)
        if _metadata_flag_true(self.metadata, {"execution_request", "runtime_input"}):
            raise ValueError("OpenCodeStaticObservationInput is not execution request")

    @property
    def execution_request(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenCodeObservationFinding:
    finding_id: str
    opencode_input_id: str
    surface_kind: OpenCodeHarnessSurfaceKind | str
    capability_kind: OpenCodeCapabilityKind | str
    summary: str
    source_ref_ids: list[str] = field(default_factory=list)
    risk_signal_kinds: list[OpenCodeRiskSignalKind | str] = field(default_factory=list)
    evidence_quality: OpenCodeEvidenceQuality | str = OpenCodeEvidenceQuality.UNKNOWN
    digestion_relevance: bool = False
    dominion_relevance: bool = False
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("opencode_input_id", self.opencode_input_id)
        OpenCodeHarnessSurfaceKind(self.surface_kind)
        OpenCodeCapabilityKind(self.capability_kind)
        _require_non_blank("summary", self.summary)
        _validate_string_list("source_ref_ids", self.source_ref_ids)
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, OpenCodeRiskSignalKind)
        OpenCodeEvidenceQuality(self.evidence_quality)
        _validate_string_list("assumptions", self.assumptions)
        _validate_string_list("limitations", self.limitations)
        if _metadata_flag_true(self.metadata, {"permission", "internal_skill_candidate", "dominion_target"}):
            raise ValueError("OpenCodeObservationFinding is not permission, InternalSkillCandidate, or DominionTarget")

    @property
    def digestion_candidate(self) -> bool:
        return False

    @property
    def dominion_target(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenCodeRiskSignal:
    risk_signal_id: str
    finding_id: str | None
    signal_kind: OpenCodeRiskSignalKind | str
    severity: str
    summary: str
    source_ref_ids: list[str] = field(default_factory=list)
    recommended_boundary: str | None = None
    routes_to_dominion_hint: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_signal_id", self.risk_signal_id)
        OpenCodeRiskSignalKind(self.signal_kind)
        _require_non_blank("severity", self.severity)
        _require_non_blank("summary", self.summary)
        _validate_string_list("source_ref_ids", self.source_ref_ids)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.severity.lower() in {"high", "critical"} and not self.recommended_boundary and not self.routes_to_dominion_hint:
            raise ValueError("high or critical severity requires recommended_boundary or routes_to_dominion_hint")
        if _metadata_flag_true(self.metadata, {"authority_grant", "permission"}):
            raise ValueError("OpenCodeRiskSignal does not grant authority")

    @property
    def authority_grant(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenCodeDigestionHint:
    digestion_hint_id: str
    finding_ids: list[str]
    candidate_focus: OpenCodeObservationFocusKind | str
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
        OpenCodeObservationFocusKind(self.candidate_focus)
        _require_non_blank("summary", self.summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, ("ready_for_internal_candidate_creation", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"internal_skill_candidate", "execution_ready"}):
            raise ValueError("OpenCodeDigestionHint is not InternalSkillCandidate")

    @property
    def internal_skill_candidate(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenCodeDominionHint:
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
            raise ValueError("OpenCodeDominionHint is not DominionTarget")

    @property
    def dominion_target(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenCodeStyleObservationProfile:
    opencode_profile_id: str
    base_harness_profile_id: str | None
    display_name: str
    description: str
    source_refs: list[OpenCodeReferenceSourceRef] = field(default_factory=list)
    observed_surfaces: list[OpenCodeSurfaceObservation] = field(default_factory=list)
    workspace_surface: OpenCodeWorkspaceSurfaceObservation | None = None
    tool_registry_surface: OpenCodeToolRegistrySurfaceObservation | None = None
    plugin_surface: OpenCodePluginSurfaceObservation | None = None
    provider_hook_surface: OpenCodeProviderHookSurfaceObservation | None = None
    command_boundary: OpenCodeCommandRiskBoundary | None = None
    config_manifest_observation: OpenCodeConfigManifestObservation | None = None
    status: OpenCodeObservationStatus | str = OpenCodeObservationStatus.OBSERVED_WITH_GAPS
    gaps: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    ready_for_v0324_manifest_extraction: bool = True
    ready_for_execution: bool = False
    ready_for_opencode_execution: bool = False
    ready_for_reference_code_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_command_execution: bool = False
    ready_for_provider_invocation: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("opencode_profile_id", self.opencode_profile_id)
        _require_non_blank("display_name", self.display_name)
        _require_non_blank("description", self.description)
        _validate_object_list("source_refs", self.source_refs, OpenCodeReferenceSourceRef)
        _validate_object_list("observed_surfaces", self.observed_surfaces, OpenCodeSurfaceObservation)
        OpenCodeObservationStatus(self.status)
        _validate_string_list("gaps", self.gaps)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(
            self,
            (
                "ready_for_execution",
                "ready_for_opencode_execution",
                "ready_for_reference_code_execution",
                "ready_for_workspace_write",
                "ready_for_command_execution",
                "ready_for_provider_invocation",
            ),
        )
        if _metadata_flag_true(self.metadata, {"opencode_runtime", "execution_ready"}):
            raise ValueError("OpenCodeStyleObservationProfile is not OpenCode runtime")

    @property
    def opencode_runtime(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenCodeObservationOutput:
    opencode_output_id: str
    opencode_input_id: str
    opencode_profile: OpenCodeStyleObservationProfile
    findings: list[OpenCodeObservationFinding] = field(default_factory=list)
    risk_signals: list[OpenCodeRiskSignal] = field(default_factory=list)
    digestion_hints: list[OpenCodeDigestionHint] = field(default_factory=list)
    dominion_hints: list[OpenCodeDominionHint] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    ready_for_v0324_manifest_extraction: bool = True
    ready_for_v0325_risk_classification: bool = True
    ready_for_execution: bool = False
    ready_for_opencode_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_command_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("opencode_output_id", self.opencode_output_id)
        _require_non_blank("opencode_input_id", self.opencode_input_id)
        if not isinstance(self.opencode_profile, OpenCodeStyleObservationProfile):
            raise TypeError("opencode_profile must be OpenCodeStyleObservationProfile")
        _validate_object_list("findings", self.findings, OpenCodeObservationFinding)
        _validate_object_list("risk_signals", self.risk_signals, OpenCodeRiskSignal)
        _validate_object_list("digestion_hints", self.digestion_hints, OpenCodeDigestionHint)
        _validate_object_list("dominion_hints", self.dominion_hints, OpenCodeDominionHint)
        _validate_string_list("gaps", self.gaps)
        _validate_string_list("blocked_reasons", self.blocked_reasons)
        _validate_false(self, ("ready_for_execution", "ready_for_opencode_execution", "ready_for_workspace_write", "ready_for_command_execution"))
        if _metadata_flag_true(self.metadata, {"manifest_extraction_execution", "digestion_candidate", "dominion_target"}):
            raise ValueError("OpenCodeObservationOutput is not runtime, digestion candidate, or dominion target")


@dataclass(frozen=True)
class OpenCodeObservationRunPreview:
    run_preview_id: str
    opencode_input_id: str | None = None
    planned_steps: list[str] = field(default_factory=list)
    expected_artifacts: list[str] = field(default_factory=list)
    explicitly_not_performed: list[str] = field(default_factory=list)
    no_opencode_execution_guarantee: bool = True
    no_reference_code_execution_guarantee: bool = True
    no_install_guarantee: bool = True
    no_import_runtime_guarantee: bool = True
    no_workspace_write_guarantee: bool = True
    no_code_edit_guarantee: bool = True
    no_patch_application_guarantee: bool = True
    no_tool_invocation_guarantee: bool = True
    no_plugin_loading_guarantee: bool = True
    no_provider_invocation_guarantee: bool = True
    no_command_execution_guarantee: bool = True
    no_network_access_guarantee: bool = True
    no_credential_access_guarantee: bool = True
    no_secret_file_read_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        for name in (
            "no_opencode_execution_guarantee",
            "no_reference_code_execution_guarantee",
            "no_install_guarantee",
            "no_import_runtime_guarantee",
            "no_workspace_write_guarantee",
            "no_code_edit_guarantee",
            "no_patch_application_guarantee",
            "no_tool_invocation_guarantee",
            "no_plugin_loading_guarantee",
            "no_provider_invocation_guarantee",
            "no_command_execution_guarantee",
            "no_network_access_guarantee",
            "no_credential_access_guarantee",
            "no_secret_file_read_guarantee",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.32.1")


@dataclass(frozen=True)
class OpenCodeNoExecutionGuarantee:
    guarantee_id: str
    version: str
    no_opencode_execution: bool = True
    no_reference_code_execution: bool = True
    no_dependency_install: bool = True
    no_import_runtime: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_patch_application: bool = True
    no_tool_invocation: bool = True
    no_tool_registration: bool = True
    no_plugin_loading: bool = True
    no_external_plugin_loading: bool = True
    no_provider_invocation: bool = True
    no_command_execution: bool = True
    no_shell_execution: bool = True
    no_network_access: bool = True
    no_credential_access: bool = True
    no_secret_file_read: bool = True
    no_registry_mutation: bool = True
    no_memory_mutation: bool = True
    no_ocel_emission: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version_includes_v0321(self.version)
        for name in (
            "no_opencode_execution",
            "no_reference_code_execution",
            "no_dependency_install",
            "no_import_runtime",
            "no_workspace_write",
            "no_code_edit",
            "no_patch_application",
            "no_tool_invocation",
            "no_tool_registration",
            "no_plugin_loading",
            "no_external_plugin_loading",
            "no_provider_invocation",
            "no_command_execution",
            "no_shell_execution",
            "no_network_access",
            "no_credential_access",
            "no_secret_file_read",
            "no_registry_mutation",
            "no_memory_mutation",
            "no_ocel_emission",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.32.1")
        _validate_string_list("evidence_refs", self.evidence_refs)


@dataclass(frozen=True)
class V0321ReadinessReport:
    report_id: str
    version: str
    opencode_profile_id: str | None
    opencode_output_id: str | None
    summary: str
    ready_for_v0324_manifest_extraction: bool = True
    ready_for_v0325_risk_classification: bool = True
    ready_for_execution: bool = False
    ready_for_opencode_execution: bool = False
    ready_for_reference_code_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_command_execution: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_OPENCODE_PROHIBITED_RUNTIME_ACTIONS))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0321(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(
            self,
            (
                "ready_for_execution",
                "ready_for_opencode_execution",
                "ready_for_reference_code_execution",
                "ready_for_workspace_write",
                "ready_for_code_edit",
                "ready_for_command_execution",
                "ready_for_provider_invocation",
                "ready_for_network_access",
                "ready_for_credential_access",
            ),
        )
        for name in ("completed_items", "blocked_items", "future_track_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_default_prohibitions("prohibited_until_later_gate", self.prohibited_until_later_gate)
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "execution_ready"}):
            raise ValueError("V0321ReadinessReport is not runtime enablement")


def build_opencode_reference_source_ref(
    source_ref_id: str,
    reference_source_id: str | None = None,
    reference_inventory_id: str | None = None,
    reference_entry_ids: list[str] | None = None,
    local_path_ref: str | None = None,
    source_label: str = "OpenCode-style static reference",
    evidence_refs: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> OpenCodeReferenceSourceRef:
    return OpenCodeReferenceSourceRef(source_ref_id, reference_source_id, reference_inventory_id, list(reference_entry_ids or []), local_path_ref, source_label, list(evidence_refs or []), dict(metadata or {}))


def build_opencode_surface_observation(
    observation_id: str,
    surface_kind: OpenCodeHarnessSurfaceKind | str,
    focus_kind: OpenCodeObservationFocusKind | str,
    capability_kind: OpenCodeCapabilityKind | str,
    title: str,
    summary: str,
    source_refs: list[OpenCodeReferenceSourceRef] | None = None,
    evidence_quality: OpenCodeEvidenceQuality | str = OpenCodeEvidenceQuality.UNKNOWN,
    risk_signal_kinds: list[OpenCodeRiskSignalKind | str] | None = None,
    boundary_notes: list[str] | None = None,
    prohibited_runtime_actions: list[str] | None = None,
    assumptions: list[str] | None = None,
    limitations: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> OpenCodeSurfaceObservation:
    return OpenCodeSurfaceObservation(
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
        prohibited_runtime_actions=list(prohibited_runtime_actions or (DEFAULT_OPENCODE_PROHIBITED_RUNTIME_ACTIONS if _capability_is_high_risk(capability_kind) else [])),
        assumptions=list(assumptions or []),
        limitations=list(limitations or []),
        metadata=dict(metadata or {}),
    )


def build_opencode_workspace_surface_observation(workspace_observation_id: str, source_refs: list[OpenCodeReferenceSourceRef] | None = None, **kwargs: Any) -> OpenCodeWorkspaceSurfaceObservation:
    return OpenCodeWorkspaceSurfaceObservation(workspace_observation_id=workspace_observation_id, source_refs=list(source_refs or []), **kwargs)


def build_opencode_tool_registry_surface_observation(tool_registry_observation_id: str, source_refs: list[OpenCodeReferenceSourceRef] | None = None, **kwargs: Any) -> OpenCodeToolRegistrySurfaceObservation:
    return OpenCodeToolRegistrySurfaceObservation(tool_registry_observation_id=tool_registry_observation_id, source_refs=list(source_refs or []), **kwargs)


def build_opencode_plugin_surface_observation(plugin_observation_id: str, source_refs: list[OpenCodeReferenceSourceRef] | None = None, **kwargs: Any) -> OpenCodePluginSurfaceObservation:
    return OpenCodePluginSurfaceObservation(plugin_observation_id=plugin_observation_id, source_refs=list(source_refs or []), **kwargs)


def build_opencode_provider_hook_surface_observation(provider_hook_observation_id: str, source_refs: list[OpenCodeReferenceSourceRef] | None = None, **kwargs: Any) -> OpenCodeProviderHookSurfaceObservation:
    return OpenCodeProviderHookSurfaceObservation(provider_hook_observation_id=provider_hook_observation_id, source_refs=list(source_refs or []), **kwargs)


def build_opencode_command_risk_boundary(command_boundary_id: str, source_refs: list[OpenCodeReferenceSourceRef] | None = None, **kwargs: Any) -> OpenCodeCommandRiskBoundary:
    return OpenCodeCommandRiskBoundary(command_boundary_id=command_boundary_id, source_refs=list(source_refs or []), **kwargs)


def build_opencode_config_manifest_observation(config_manifest_observation_id: str, source_refs: list[OpenCodeReferenceSourceRef] | None = None, **kwargs: Any) -> OpenCodeConfigManifestObservation:
    return OpenCodeConfigManifestObservation(config_manifest_observation_id=config_manifest_observation_id, source_refs=list(source_refs or []), **kwargs)


def build_opencode_static_observation_input(opencode_input_id: str, **kwargs: Any) -> OpenCodeStaticObservationInput:
    return OpenCodeStaticObservationInput(opencode_input_id=opencode_input_id, **kwargs)


def build_opencode_observation_finding(finding_id: str, opencode_input_id: str, surface_kind: OpenCodeHarnessSurfaceKind | str, capability_kind: OpenCodeCapabilityKind | str, summary: str, **kwargs: Any) -> OpenCodeObservationFinding:
    return OpenCodeObservationFinding(finding_id=finding_id, opencode_input_id=opencode_input_id, surface_kind=surface_kind, capability_kind=capability_kind, summary=summary, **kwargs)


def build_opencode_risk_signal(risk_signal_id: str, signal_kind: OpenCodeRiskSignalKind | str, severity: str, summary: str, finding_id: str | None = None, **kwargs: Any) -> OpenCodeRiskSignal:
    return OpenCodeRiskSignal(risk_signal_id=risk_signal_id, finding_id=finding_id, signal_kind=signal_kind, severity=severity, summary=summary, **kwargs)


def build_opencode_digestion_hint(digestion_hint_id: str, finding_ids: list[str], candidate_focus: OpenCodeObservationFocusKind | str, summary: str, suggested_internal_candidate_kind: str | None = None, **kwargs: Any) -> OpenCodeDigestionHint:
    return OpenCodeDigestionHint(digestion_hint_id=digestion_hint_id, finding_ids=list(finding_ids), candidate_focus=candidate_focus, suggested_internal_candidate_kind=suggested_internal_candidate_kind, summary=summary, **kwargs)


def build_opencode_dominion_hint(dominion_hint_id: str, finding_ids: list[str], risk_signal_ids: list[str], suggested_boundary: str, summary: str, **kwargs: Any) -> OpenCodeDominionHint:
    return OpenCodeDominionHint(dominion_hint_id=dominion_hint_id, finding_ids=list(finding_ids), risk_signal_ids=list(risk_signal_ids), suggested_boundary=suggested_boundary, summary=summary, **kwargs)


def build_opencode_style_observation_profile(opencode_profile_id: str, display_name: str, description: str, base_harness_profile_id: str | None = None, **kwargs: Any) -> OpenCodeStyleObservationProfile:
    return OpenCodeStyleObservationProfile(opencode_profile_id=opencode_profile_id, base_harness_profile_id=base_harness_profile_id, display_name=display_name, description=description, **kwargs)


def build_opencode_observation_output(opencode_output_id: str, opencode_input_id: str, opencode_profile: OpenCodeStyleObservationProfile, **kwargs: Any) -> OpenCodeObservationOutput:
    return OpenCodeObservationOutput(opencode_output_id=opencode_output_id, opencode_input_id=opencode_input_id, opencode_profile=opencode_profile, **kwargs)


def build_opencode_observation_run_preview(run_preview_id: str = "opencode_observation_run_preview:v0.32.1", **kwargs: Any) -> OpenCodeObservationRunPreview:
    return OpenCodeObservationRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_opencode_no_execution_guarantee(guarantee_id: str = "opencode_no_execution_guarantee:v0.32.1", evidence_refs: list[str] | None = None, metadata: dict[str, Any] | None = None) -> OpenCodeNoExecutionGuarantee:
    return OpenCodeNoExecutionGuarantee(guarantee_id=guarantee_id, version=V0321_VERSION, evidence_refs=list(evidence_refs or []), metadata=dict(metadata or {}))


def build_v0321_readiness_report(report_id: str = "v0321_readiness_report", opencode_profile_id: str | None = None, opencode_output_id: str | None = None, summary: str = "v0.32.1 is ready for manifest extraction and risk classification design-stage handoff only, not execution.", **kwargs: Any) -> V0321ReadinessReport:
    return V0321ReadinessReport(report_id=report_id, version=V0321_VERSION, opencode_profile_id=opencode_profile_id, opencode_output_id=opencode_output_id, summary=summary, **kwargs)


def classify_inventory_entry_as_opencode_surface(entry: ReferenceFileInventoryEntry) -> OpenCodeHarnessSurfaceKind:
    name = entry.file_name.lower()
    path = entry.relative_path.lower()
    detected = (entry.detected_kind or "").lower()
    if "package" in name or "lock" in name or "dependency" in detected:
        return OpenCodeHarnessSurfaceKind.DEPENDENCY_MANIFEST_SURFACE
    if "plugin" in path:
        return OpenCodeHarnessSurfaceKind.PLUGIN_MANIFEST_SURFACE
    if "tool" in path:
        return OpenCodeHarnessSurfaceKind.TOOL_REGISTRY_SURFACE
    if "provider" in path or "model" in path:
        return OpenCodeHarnessSurfaceKind.PROVIDER_HOOK_SURFACE
    if "shell" in path or "command" in path or "exec" in path:
        return OpenCodeHarnessSurfaceKind.COMMAND_EXECUTION_SURFACE
    if entry.file_extension in {".md", ".txt"}:
        return OpenCodeHarnessSurfaceKind.FILE_READ_SURFACE
    if entry.file_extension in {".json", ".toml", ".yaml", ".yml"}:
        return OpenCodeHarnessSurfaceKind.CONFIGURATION_MANIFEST_SURFACE
    return OpenCodeHarnessSurfaceKind.WORKSPACE_TREE_SURFACE


def infer_opencode_capability_from_surface(surface_kind: OpenCodeHarnessSurfaceKind | str) -> OpenCodeCapabilityKind:
    surface = OpenCodeHarnessSurfaceKind(surface_kind)
    return {
        OpenCodeHarnessSurfaceKind.FILE_READ_SURFACE: OpenCodeCapabilityKind.READ_FILE,
        OpenCodeHarnessSurfaceKind.FILE_WRITE_SURFACE: OpenCodeCapabilityKind.WRITE_FILE,
        OpenCodeHarnessSurfaceKind.CODE_EDIT_SURFACE: OpenCodeCapabilityKind.EDIT_CODE,
        OpenCodeHarnessSurfaceKind.PATCH_SURFACE: OpenCodeCapabilityKind.APPLY_PATCH,
        OpenCodeHarnessSurfaceKind.SEARCH_SURFACE: OpenCodeCapabilityKind.SEARCH_WORKSPACE,
        OpenCodeHarnessSurfaceKind.TOOL_REGISTRY_SURFACE: OpenCodeCapabilityKind.REGISTER_TOOL,
        OpenCodeHarnessSurfaceKind.TOOL_INVOCATION_SURFACE: OpenCodeCapabilityKind.INVOKE_TOOL,
        OpenCodeHarnessSurfaceKind.PLUGIN_MANIFEST_SURFACE: OpenCodeCapabilityKind.LOAD_PLUGIN,
        OpenCodeHarnessSurfaceKind.PLUGIN_RUNTIME_SURFACE: OpenCodeCapabilityKind.LOAD_PLUGIN,
        OpenCodeHarnessSurfaceKind.EXTERNAL_PLUGIN_SURFACE: OpenCodeCapabilityKind.LOAD_EXTERNAL_PLUGIN,
        OpenCodeHarnessSurfaceKind.PROVIDER_HOOK_SURFACE: OpenCodeCapabilityKind.INVOKE_PROVIDER,
        OpenCodeHarnessSurfaceKind.COMMAND_EXECUTION_SURFACE: OpenCodeCapabilityKind.EXECUTE_COMMAND,
        OpenCodeHarnessSurfaceKind.SHELL_SURFACE: OpenCodeCapabilityKind.EXECUTE_SHELL,
        OpenCodeHarnessSurfaceKind.LSP_EDITOR_SURFACE: OpenCodeCapabilityKind.EDITOR_INTEGRATION,
        OpenCodeHarnessSurfaceKind.DEPENDENCY_MANIFEST_SURFACE: OpenCodeCapabilityKind.DEPENDENCY_RESOLUTION,
        OpenCodeHarnessSurfaceKind.CONFIGURATION_MANIFEST_SURFACE: OpenCodeCapabilityKind.CONFIG_LOADING,
        OpenCodeHarnessSurfaceKind.APPROVAL_BOUNDARY_SURFACE: OpenCodeCapabilityKind.APPROVAL_GATE,
        OpenCodeHarnessSurfaceKind.AUDIT_BOUNDARY_SURFACE: OpenCodeCapabilityKind.AUDIT_TRACE,
        OpenCodeHarnessSurfaceKind.RESULT_ENVELOPE_SURFACE: OpenCodeCapabilityKind.RESULT_ENVELOPE,
    }.get(surface, OpenCodeCapabilityKind.READ_WORKSPACE)


def infer_opencode_risk_signals_from_inventory_entry(entry: ReferenceFileInventoryEntry) -> list[OpenCodeRiskSignalKind]:
    surface = classify_inventory_entry_as_opencode_surface(entry)
    capability = infer_opencode_capability_from_surface(surface)
    risks: list[OpenCodeRiskSignalKind] = []
    if capability == OpenCodeCapabilityKind.WRITE_FILE:
        risks.append(OpenCodeRiskSignalKind.WORKSPACE_WRITE_RISK)
    if capability == OpenCodeCapabilityKind.EDIT_CODE:
        risks.append(OpenCodeRiskSignalKind.CODE_EDIT_RISK)
    if capability == OpenCodeCapabilityKind.APPLY_PATCH:
        risks.append(OpenCodeRiskSignalKind.PATCH_APPLICATION_RISK)
    if capability == OpenCodeCapabilityKind.EXECUTE_COMMAND:
        risks.append(OpenCodeRiskSignalKind.COMMAND_EXECUTION_RISK)
    if capability == OpenCodeCapabilityKind.EXECUTE_SHELL:
        risks.append(OpenCodeRiskSignalKind.SHELL_EXECUTION_RISK)
    if capability == OpenCodeCapabilityKind.INVOKE_PROVIDER:
        risks.extend([OpenCodeRiskSignalKind.PROVIDER_INVOCATION_RISK, OpenCodeRiskSignalKind.NETWORK_ACCESS_RISK, OpenCodeRiskSignalKind.CREDENTIAL_ACCESS_RISK])
    if capability == OpenCodeCapabilityKind.LOAD_PLUGIN:
        risks.append(OpenCodeRiskSignalKind.PLUGIN_LOADING_RISK)
    if capability == OpenCodeCapabilityKind.LOAD_EXTERNAL_PLUGIN:
        risks.append(OpenCodeRiskSignalKind.EXTERNAL_PLUGIN_RISK)
    if capability == OpenCodeCapabilityKind.DEPENDENCY_RESOLUTION:
        risks.append(OpenCodeRiskSignalKind.DEPENDENCY_INSTALL_RISK)
    if capability == OpenCodeCapabilityKind.REGISTER_TOOL:
        risks.append(OpenCodeRiskSignalKind.TOOL_REGISTRY_MUTATION_RISK)
    if capability == OpenCodeCapabilityKind.INVOKE_TOOL:
        risks.append(OpenCodeRiskSignalKind.TOOL_INVOCATION_RISK)
    return risks or [OpenCodeRiskSignalKind.UNKNOWN]


def opencode_profile_preserves_no_execution(profile: OpenCodeStyleObservationProfile) -> bool:
    return (
        profile.ready_for_execution is False
        and profile.ready_for_opencode_execution is False
        and profile.ready_for_reference_code_execution is False
        and profile.ready_for_workspace_write is False
        and profile.ready_for_command_execution is False
        and profile.ready_for_provider_invocation is False
        and profile.opencode_runtime is False
    )


def opencode_output_is_not_manifest_or_digestive_runtime(output: OpenCodeObservationOutput) -> bool:
    return (
        output.ready_for_execution is False
        and output.ready_for_opencode_execution is False
        and output.ready_for_workspace_write is False
        and output.ready_for_command_execution is False
    )


def opencode_run_preview_preserves_no_execution(preview: OpenCodeObservationRunPreview) -> bool:
    return (
        preview.no_opencode_execution_guarantee
        and preview.no_reference_code_execution_guarantee
        and preview.no_workspace_write_guarantee
        and preview.no_command_execution_guarantee
        and preview.no_provider_invocation_guarantee
    )


def v0321_readiness_report_is_not_runtime_ready(report: V0321ReadinessReport) -> bool:
    return (
        report.ready_for_execution is False
        and report.ready_for_opencode_execution is False
        and report.ready_for_reference_code_execution is False
        and report.ready_for_workspace_write is False
        and report.ready_for_code_edit is False
        and report.ready_for_command_execution is False
        and report.ready_for_provider_invocation is False
        and report.ready_for_network_access is False
        and report.ready_for_credential_access is False
    )
