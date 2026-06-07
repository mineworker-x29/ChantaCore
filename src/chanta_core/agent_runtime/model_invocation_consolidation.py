from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import DEFAULT_FUTURE_TRACK_LEVELS, _metadata_flag_true, _require_non_blank, _validate_string_list


V0349_VERSION = "v0.34.9"
V0349_RELEASE_NAME = "v0.34.9 Controlled Model Invocation Boundary Consolidation"
CONTROLLED_MODEL_INVOCATION_BOUNDARY_V1 = "Controlled Model Invocation Boundary v1"

V034_INCLUDED_VERSIONS = [
    "v0.34.0",
    "v0.34.1",
    "v0.34.2",
    "v0.34.3",
    "v0.34.4",
    "v0.34.5",
    "v0.34.6",
    "v0.34.7",
    "v0.34.8",
]

DEFAULT_INCLUDED_MODULES = [
    "src/chanta_core/agent_runtime/model_invocation_boundary.py",
    "src/chanta_core/agent_runtime/provider_profile.py",
    "src/chanta_core/agent_runtime/model_request.py",
    "src/chanta_core/agent_runtime/model_response.py",
    "src/chanta_core/agent_runtime/provider_adapter.py",
    "src/chanta_core/agent_runtime/model_output_quarantine.py",
    "src/chanta_core/agent_runtime/model_backed_step.py",
    "src/chanta_core/agent_runtime/model_invocation_trace.py",
    "src/chanta_core/agent_runtime/model_cli_surface.py",
]

DEFAULT_INCLUDED_DOCS = [
    "docs/versions/v0.34/v0.34.0_controlled_model_invocation_boundary.md",
    "docs/versions/v0.34/v0.34.1_provider_profile_invocation_policy.md",
    "docs/versions/v0.34/v0.34.2_model_request_envelope.md",
    "docs/versions/v0.34/v0.34.3_model_response_envelope_sanitizer.md",
    "docs/versions/v0.34/v0.34.4_existing_provider_boundary_adapter.md",
    "docs/versions/v0.34/v0.34.5_model_output_action_quarantine.md",
    "docs/versions/v0.34/v0.34.6_agent_step_runner_model_integration.md",
    "docs/versions/v0.34/v0.34.7_model_invocation_ocel_trace_packet.md",
    "docs/versions/v0.34/v0.34.8_cli_model_backed_agent_step_surface.md",
]

DEFAULT_INCLUDED_TESTS = [
    "tests/test_v0340_controlled_model_invocation_boundary.py",
    "tests/test_v0341_provider_profile_invocation_policy.py",
    "tests/test_v0342_model_request_envelope.py",
    "tests/test_v0343_model_response_envelope_sanitizer.py",
    "tests/test_v0344_existing_provider_boundary_adapter.py",
    "tests/test_v0345_model_output_action_quarantine.py",
    "tests/test_v0346_agent_step_runner_model_integration.py",
    "tests/test_v0347_model_invocation_ocel_trace_packet.py",
    "tests/test_v0348_cli_model_backed_agent_step_surface.py",
]

DEFAULT_CONTROLLED_CAPABILITIES = [
    "controlled model invocation boundary definitions",
    "provider profile metadata and invocation policy",
    "model request envelope construction and validation",
    "model response envelope sanitizer and action-signal detection",
    "existing provider boundary adapter through injected project-local boundary only",
]

DEFAULT_BOUNDED_CAPABILITIES = [
    "model output action quarantine",
    "bounded model-backed step through v0.34.6",
    "model invocation trace packet creation through v0.34.7",
    "bounded CLI model-backed surface through v0.34.8",
]

DEFAULT_PROHIBITED_CAPABILITIES = [
    "direct provider SDK invocation",
    "direct provider invocation",
    "direct network access",
    "credential read",
    "secret read",
    "environment credential read",
    "new provider SDK adapter",
    "new credential loader",
    "new network adapter",
    "autonomous general agent runtime",
    "general tool execution",
    "unquarantined action execution",
    "shell execution",
    "subprocess execution",
    "command execution",
    "workspace write",
    "code edit",
    "patch proposal",
    "patch application",
    "external harness execution",
    "reference code execution",
    "reference import",
    "dependency install",
    "reference test execution",
    "persistent trace write",
    "database write",
    "runtime log write",
    "external trace sink",
    "UI runtime",
    "external control",
    "authority grant",
    "D4-D9 authority grant",
]

DEFAULT_FUTURE_TRACK_ITEMS = [
    "Controlled Patch Proposal Layer",
    "patch apply sandbox",
    "autonomous multi-step loop",
    "persistent trace store",
    "UI runtime",
    "external harness adapter",
    "direct provider adapter review if ever needed",
]

DEFAULT_RECOMMENDED_V035_ITEMS = [
    "controlled patch proposal artifacts only",
    "patch proposal redaction and bounding",
    "human review gate before any later patch application track",
]

DEFAULT_PROHIBITED_RUNTIME_SURFACES = [
    "direct_provider_invocation",
    "provider_sdk_invocation",
    "direct_network_access",
    "credential_access",
    "secret_read",
    "shell_execution",
    "subprocess_execution",
    "command_execution",
    "general_tool_execution",
    "unquarantined_action_execution",
    "workspace_write",
    "code_edit",
    "patch_proposal",
    "patch_application",
    "reference_code_execution",
    "reference_import",
    "dependency_install",
    "persistent_trace_write",
    "external_trace_sink",
    "UI_runtime",
    "external_control",
    "authority_grant",
    "D4_D9_grant",
]

DEFAULT_PROHIBITED_BOUNDARIES = [
    "direct provider SDK",
    "direct network",
    "credential read",
    "secret read",
    "shell",
    "subprocess",
    "command",
    "workspace write",
    "code edit",
    "patch proposal",
    "patch application",
    "reference execution",
    "general tool",
    "autonomous runtime",
    "persistent trace",
    "UI runtime",
    "external control",
    "authority grant",
]

DEFAULT_WITHDRAWAL_CONDITIONS = [
    "Any direct provider SDK, network, credential, shell, write, patch, or persistent trace path is introduced.",
    "Any autonomous runtime, general tool execution, reference execution, or authority grant is introduced.",
    "Any unsafe readiness flag or production_certified becomes true.",
]

DEFAULT_PROHIBITED_UNTIL_LATER_GATE = [
    "patch application",
    "workspace write",
    "code edit",
    "shell",
    "command",
    "direct provider",
    "direct network",
    "credential access",
    "autonomous loop",
    "general tool",
    "UI runtime",
    "authority grant",
]

UNSAFE_CONSOLIDATION_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_general_agent_execution",
    "ready_for_autonomous_agent_runtime",
    "ready_for_direct_provider_invocation",
    "ready_for_provider_invocation",
    "ready_for_provider_sdk_invocation",
    "ready_for_direct_network_access",
    "ready_for_network_access",
    "ready_for_credential_access",
    "ready_for_secret_read",
    "ready_for_general_tool_execution",
    "ready_for_unquarantined_action_execution",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_patch_proposal",
    "ready_for_patch_application",
    "ready_for_registry_mutation",
    "ready_for_memory_mutation",
    "ready_for_raw_prompt_persistence",
    "ready_for_raw_response_persistence",
    "ready_for_raw_model_output_persistence",
    "ready_for_general_ocel_emission",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
)

REPORT_UNSAFE_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_general_agent_execution",
    "ready_for_autonomous_agent_runtime",
    "ready_for_direct_provider_invocation",
    "ready_for_provider_sdk_invocation",
    "ready_for_direct_network_access",
    "ready_for_credential_access",
    "ready_for_secret_read",
    "ready_for_general_tool_execution",
    "ready_for_unquarantined_action_execution",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_patch_proposal",
    "ready_for_patch_application",
    "ready_for_persistent_trace_write",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
)


class ControlledModelInvocationConsolidationStatus(StrEnum):
    UNKNOWN = "unknown"
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    CONSOLIDATED = "consolidated"
    CONSOLIDATED_WITH_GAPS = "consolidated_with_gaps"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class ControlledModelInvocationConsolidationReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    CONTRACT_READY = "contract_ready"
    CONTROLLED_BOUNDARY_READY = "controlled_boundary_ready"
    BOUNDED_MODEL_INVOCATION_READY = "bounded_model_invocation_ready"
    CLI_MODEL_BACKED_SURFACE_READY = "cli_model_backed_surface_ready"
    HANDOFF_READY_FOR_V035 = "handoff_ready_for_v035"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


def _validate_version_includes_v0349(version: str) -> None:
    _require_non_blank("version", version)
    if V0349_VERSION not in version:
        raise ValueError("version must include v0.34.9")


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.34.9")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise TypeError(f"{name} must be dict[str, Any]")


def _validate_included_versions(values: list[str]) -> None:
    _validate_string_list("included_versions", values)
    missing = set(V034_INCLUDED_VERSIONS) - set(values)
    if missing:
        raise ValueError(f"included_versions must include v0.34.0 through v0.34.8: {sorted(missing)}")


def _validate_contains_terms(name: str, values: list[str], terms: list[str]) -> None:
    _validate_string_list(name, values)
    lowered = " | ".join(values).lower()
    missing = [term for term in terms if term.lower() not in lowered]
    if missing:
        raise ValueError(f"{name} missing required terms: {missing}")


def _validate_contains_all(name: str, values: list[str], required: list[str]) -> None:
    _validate_string_list(name, values)
    lowered = {value.lower() for value in values}
    missing = [item for item in required if item.lower() not in lowered]
    if missing:
        raise ValueError(f"{name} missing required values: {missing}")


def _validate_level_not_d4_d9(level: str | None) -> None:
    if level is None:
        return
    _require_non_blank("max_grantable_level", level)
    normalized = level.strip().upper()
    if any(normalized.startswith(value) for value in DEFAULT_FUTURE_TRACK_LEVELS):
        raise ValueError("D4-D9 must remain future-track in v0.34.9")


def _validate_future_track_levels(values: list[str]) -> None:
    _validate_string_list("future_track_levels", values)
    missing = set(DEFAULT_FUTURE_TRACK_LEVELS) - set(values)
    if missing:
        raise ValueError(f"future_track_levels must include D4-D9: {sorted(missing)}")


def _validate_metadata_no_runtime_expansion(metadata: dict[str, Any]) -> None:
    _validate_dict("metadata", metadata)
    if _metadata_flag_true(
        metadata,
        {
            "runtime_expansion",
            "permission_grant",
            "production_release",
            "implementation",
            "provider_invocation",
            "provider_sdk_invocation",
            "direct_network_access",
            "credential_access",
            "shell_execution",
            "workspace_write",
            "patch_proposal",
            "patch_application",
            "persistent_trace_write",
            "ui_runtime",
            "authority_grant",
        },
    ):
        raise ValueError("v0.34.9 consolidation metadata cannot imply runtime expansion")


@dataclass(frozen=True)
class ControlledModelInvocationReleaseFlagSet:
    flag_set_id: str
    version: str = V0349_VERSION
    controlled_model_invocation_boundary_v1_ready: bool = False
    ready_for_v035_handoff: bool = False
    ready_for_controlled_model_invocation_boundary: bool = False
    ready_for_controlled_existing_boundary_invocation: bool = False
    ready_for_bounded_model_backed_step_execution: bool = False
    ready_for_agent_step_runner_model_integration: bool = False
    ready_for_cli_model_backed_surface: bool = False
    ready_for_model_invocation_trace_packet_creation: bool = False
    ready_for_bounded_model_invocation_ocel_trace_emission: bool = False
    ready_for_execution: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_direct_provider_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_provider_sdk_invocation: bool = False
    ready_for_direct_network_access: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_secret_read: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_unquarantined_action_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_proposal: bool = False
    ready_for_patch_application: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_raw_prompt_persistence: bool = False
    ready_for_raw_response_persistence: bool = False
    ready_for_raw_model_output_persistence: bool = False
    ready_for_general_ocel_emission: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    max_grantable_level: str | None = None
    future_track_levels: list[str] = field(default_factory=lambda: list(DEFAULT_FUTURE_TRACK_LEVELS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version_includes_v0349(self.version)
        _validate_false(self, UNSAFE_CONSOLIDATION_FLAG_NAMES)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False in v0.34.9")
        _validate_level_not_d4_d9(self.max_grantable_level)
        _validate_future_track_levels(self.future_track_levels)
        _validate_metadata_no_runtime_expansion(self.metadata)


@dataclass(frozen=True)
class ControlledModelInvocationSnapshot:
    snapshot_id: str
    version: str
    release_name: str
    included_versions: list[str]
    included_modules: list[str]
    included_artifact_groups: list[str]
    release_flags: ControlledModelInvocationReleaseFlagSet
    consolidation_status: ControlledModelInvocationConsolidationStatus | str
    readiness_level: ControlledModelInvocationConsolidationReadinessLevel | str
    summary: str
    controlled_capabilities: list[str] = field(default_factory=list)
    prohibited_capabilities: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    known_gaps: list[str] = field(default_factory=list)
    known_risks: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("snapshot_id", self.snapshot_id)
        _validate_version_includes_v0349(self.version)
        _require_non_blank("release_name", self.release_name)
        if CONTROLLED_MODEL_INVOCATION_BOUNDARY_V1 not in self.release_name:
            raise ValueError("release_name should be Controlled Model Invocation Boundary v1")
        _validate_included_versions(self.included_versions)
        for name in (
            "included_modules",
            "included_artifact_groups",
            "controlled_capabilities",
            "prohibited_capabilities",
            "evidence_refs",
            "known_gaps",
            "known_risks",
            "withdrawal_conditions",
        ):
            _validate_string_list(name, getattr(self, name))
        if not isinstance(self.release_flags, ControlledModelInvocationReleaseFlagSet):
            raise TypeError("release_flags must be ControlledModelInvocationReleaseFlagSet")
        if not controlled_model_invocation_flags_preserve_unsafe_false(self.release_flags):
            raise ValueError("release_flags must preserve unsafe readiness false")
        ControlledModelInvocationConsolidationStatus(self.consolidation_status)
        ControlledModelInvocationConsolidationReadinessLevel(self.readiness_level)
        _require_non_blank("summary", self.summary)
        _validate_metadata_no_runtime_expansion(self.metadata)

    @property
    def runtime_expansion(self) -> bool:
        return False


@dataclass(frozen=True)
class ControlledModelInvocationCapabilityMatrix:
    capability_matrix_id: str
    version: str
    enabled_controlled_capabilities: list[str] = field(default_factory=list)
    enabled_bounded_capabilities: list[str] = field(default_factory=list)
    design_stage_capabilities: list[str] = field(default_factory=list)
    prohibited_capabilities: list[str] = field(default_factory=list)
    future_track_capabilities: list[str] = field(default_factory=list)
    capability_to_version: dict[str, str] = field(default_factory=dict)
    prohibited_capability_to_reason: dict[str, str] = field(default_factory=dict)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("capability_matrix_id", self.capability_matrix_id)
        _validate_version_includes_v0349(self.version)
        for name in (
            "enabled_controlled_capabilities",
            "enabled_bounded_capabilities",
            "design_stage_capabilities",
            "prohibited_capabilities",
            "future_track_capabilities",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_dict("capability_to_version", self.capability_to_version)
        _validate_dict("prohibited_capability_to_reason", self.prohibited_capability_to_reason)
        if not all(isinstance(value, str) for value in self.capability_to_version.values()):
            raise TypeError("capability_to_version must be dict[str, str]")
        if not all(isinstance(value, str) for value in self.prohibited_capability_to_reason.values()):
            raise TypeError("prohibited_capability_to_reason must be dict[str, str]")
        _validate_contains_terms(
            "prohibited_capabilities",
            self.prohibited_capabilities,
            ["direct provider SDK", "direct network", "credential", "shell", "write", "patch", "general tool", "autonomous", "persistent trace", "UI"],
        )
        _validate_metadata_no_runtime_expansion(self.metadata)

    @property
    def permission_grant(self) -> bool:
        return False


@dataclass(frozen=True)
class _ControlledModelInvocationCoverageBase:
    coverage_id: str
    version: str
    stage_version: str
    covered_artifact_refs: list[str] = field(default_factory=list)
    missing_artifact_refs: list[str] = field(default_factory=list)
    covered_test_refs: list[str] = field(default_factory=list)
    missing_test_refs: list[str] = field(default_factory=list)
    covered_doc_refs: list[str] = field(default_factory=list)
    missing_doc_refs: list[str] = field(default_factory=list)
    coverage_notes: list[str] = field(default_factory=list)
    coverage_complete: bool = False
    blocking_gaps: list[str] = field(default_factory=list)
    non_blocking_gaps: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("coverage_id", self.coverage_id)
        _validate_version_includes_v0349(self.version)
        _require_non_blank("stage_version", self.stage_version)
        for name in (
            "covered_artifact_refs",
            "missing_artifact_refs",
            "covered_test_refs",
            "missing_test_refs",
            "covered_doc_refs",
            "missing_doc_refs",
            "coverage_notes",
            "blocking_gaps",
            "non_blocking_gaps",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        if self.coverage_complete and self.blocking_gaps:
            raise ValueError("coverage_complete cannot be True when blocking_gaps is non-empty")
        _validate_metadata_no_runtime_expansion(self.metadata)

    @property
    def production_certification(self) -> bool:
        return False


@dataclass(frozen=True)
class ControlledModelInvocationBoundaryCoverage(_ControlledModelInvocationCoverageBase):
    pass


@dataclass(frozen=True)
class ProviderProfilePolicyCoverage(_ControlledModelInvocationCoverageBase):
    pass


@dataclass(frozen=True)
class ModelRequestEnvelopeCoverage(_ControlledModelInvocationCoverageBase):
    pass


@dataclass(frozen=True)
class ModelResponseEnvelopeCoverage(_ControlledModelInvocationCoverageBase):
    pass


@dataclass(frozen=True)
class ExistingProviderBoundaryAdapterCoverage(_ControlledModelInvocationCoverageBase):
    pass


@dataclass(frozen=True)
class ModelOutputActionQuarantineCoverage(_ControlledModelInvocationCoverageBase):
    pass


@dataclass(frozen=True)
class ModelBackedStepIntegrationCoverage(_ControlledModelInvocationCoverageBase):
    pass


@dataclass(frozen=True)
class ModelInvocationTraceCoverage(_ControlledModelInvocationCoverageBase):
    pass


@dataclass(frozen=True)
class CLIModelBackedSurfaceCoverage(_ControlledModelInvocationCoverageBase):
    pass


@dataclass(frozen=True)
class ControlledModelInvocationBoundaryRegister:
    boundary_register_id: str
    version: str
    inherited_boundaries: list[str] = field(default_factory=list)
    active_controlled_boundaries: list[str] = field(default_factory=list)
    active_bounded_boundaries: list[str] = field(default_factory=list)
    prohibited_boundaries: list[str] = field(default_factory=list)
    future_gate_boundaries: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_register_id", self.boundary_register_id)
        _validate_version_includes_v0349(self.version)
        for name in (
            "inherited_boundaries",
            "active_controlled_boundaries",
            "active_bounded_boundaries",
            "prohibited_boundaries",
            "future_gate_boundaries",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_contains_terms(
            "prohibited_boundaries",
            self.prohibited_boundaries,
            ["direct provider SDK", "direct network", "credential", "secret", "shell", "subprocess", "command", "workspace write", "code edit", "patch proposal", "patch application", "reference", "general tool", "autonomous", "persistent trace", "UI", "external control", "authority"],
        )
        _validate_metadata_no_runtime_expansion(self.metadata)

    @property
    def runtime_enforcement(self) -> bool:
        return False


@dataclass(frozen=True)
class ControlledModelInvocationRiskRegister:
    risk_register_id: str
    version: str
    known_risks: list[str] = field(default_factory=list)
    high_risk_surfaces: list[str] = field(default_factory=list)
    prohibited_runtime_surfaces: list[str] = field(default_factory=list)
    mitigations: list[str] = field(default_factory=list)
    unresolved_risks: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_register_id", self.risk_register_id)
        _validate_version_includes_v0349(self.version)
        for name in (
            "known_risks",
            "high_risk_surfaces",
            "prohibited_runtime_surfaces",
            "mitigations",
            "unresolved_risks",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_contains_all("prohibited_runtime_surfaces", self.prohibited_runtime_surfaces, DEFAULT_PROHIBITED_RUNTIME_SURFACES)
        _validate_metadata_no_runtime_expansion(self.metadata)

    @property
    def permission(self) -> bool:
        return False


@dataclass(frozen=True)
class ControlledModelInvocationGapRegister:
    gap_register_id: str
    version: str
    blocking_gaps: list[str] = field(default_factory=list)
    non_blocking_gaps: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    recommended_v035_items: list[str] = field(default_factory=list)
    recommended_later_items: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("gap_register_id", self.gap_register_id)
        _validate_version_includes_v0349(self.version)
        for name in (
            "blocking_gaps",
            "non_blocking_gaps",
            "future_track_items",
            "recommended_v035_items",
            "recommended_later_items",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_contains_terms(
            "future_track_items",
            self.future_track_items,
            ["Controlled Patch Proposal", "patch apply", "autonomous", "persistent trace", "UI", "external harness"],
        )
        _validate_metadata_no_runtime_expansion(self.metadata)


@dataclass(frozen=True)
class ControlledModelInvocationReleaseManifest:
    release_manifest_id: str
    version: str
    release_name: str
    snapshot_id: str
    included_versions: list[str]
    included_modules: list[str]
    included_docs: list[str]
    included_tests: list[str]
    focused_test_command: str
    full_track_test_command: str
    release_flags: ControlledModelInvocationReleaseFlagSet
    known_gaps: list[str] = field(default_factory=list)
    known_risks: list[str] = field(default_factory=list)
    next_handoff_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("release_manifest_id", self.release_manifest_id)
        _validate_version_includes_v0349(self.version)
        _require_non_blank("release_name", self.release_name)
        _require_non_blank("snapshot_id", self.snapshot_id)
        _validate_included_versions(self.included_versions)
        for name in ("included_modules", "included_docs", "included_tests", "known_gaps", "known_risks"):
            _validate_string_list(name, getattr(self, name))
        _require_non_blank("focused_test_command", self.focused_test_command)
        _require_non_blank("full_track_test_command", self.full_track_test_command)
        if not isinstance(self.release_flags, ControlledModelInvocationReleaseFlagSet):
            raise TypeError("release_flags must be ControlledModelInvocationReleaseFlagSet")
        if not controlled_model_invocation_flags_preserve_unsafe_false(self.release_flags):
            raise ValueError("release_flags must preserve unsafe readiness false")
        if self.next_handoff_id is not None:
            _require_non_blank("next_handoff_id", self.next_handoff_id)
        _validate_metadata_no_runtime_expansion(self.metadata)

    @property
    def production_release(self) -> bool:
        return False


@dataclass(frozen=True)
class ControlledModelInvocationAuditTrail:
    audit_trail_id: str
    version: str
    reviewed_artifact_refs: list[str] = field(default_factory=list)
    reviewed_test_refs: list[str] = field(default_factory=list)
    reviewed_doc_refs: list[str] = field(default_factory=list)
    boundary_checks: list[str] = field(default_factory=list)
    negative_runtime_checks: list[str] = field(default_factory=list)
    controlled_capability_checks: list[str] = field(default_factory=list)
    no_direct_provider_invocation_confirmed: bool = True
    no_provider_sdk_invocation_confirmed: bool = True
    no_direct_network_access_confirmed: bool = True
    no_credential_access_confirmed: bool = True
    no_secret_read_confirmed: bool = True
    no_shell_execution_confirmed: bool = True
    no_subprocess_execution_confirmed: bool = True
    no_command_execution_confirmed: bool = True
    no_general_agent_execution_confirmed: bool = True
    no_autonomous_agent_runtime_confirmed: bool = True
    no_general_tool_execution_confirmed: bool = True
    no_unquarantined_action_execution_confirmed: bool = True
    no_workspace_write_confirmed: bool = True
    no_code_edit_confirmed: bool = True
    no_patch_proposal_confirmed: bool = True
    no_patch_application_confirmed: bool = True
    no_reference_code_execution_confirmed: bool = True
    no_reference_import_confirmed: bool = True
    no_dependency_install_confirmed: bool = True
    no_raw_prompt_persistence_confirmed: bool = True
    no_raw_response_persistence_confirmed: bool = True
    no_raw_model_output_persistence_confirmed: bool = True
    no_persistent_trace_write_confirmed: bool = True
    no_external_trace_sink_confirmed: bool = True
    no_ui_runtime_confirmed: bool = True
    no_external_control_confirmed: bool = True
    no_authority_grant_confirmed: bool = True
    no_d4_d9_grant_confirmed: bool = True
    unsafe_readiness_flags_false_confirmed: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("audit_trail_id", self.audit_trail_id)
        _validate_version_includes_v0349(self.version)
        for name in (
            "reviewed_artifact_refs",
            "reviewed_test_refs",
            "reviewed_doc_refs",
            "boundary_checks",
            "negative_runtime_checks",
            "controlled_capability_checks",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True for successful v0.34.9 consolidation")
        if self.unsafe_readiness_flags_false_confirmed is not True:
            raise ValueError("unsafe_readiness_flags_false_confirmed must be True")
        _validate_metadata_no_runtime_expansion(self.metadata)

    @property
    def runtime_audit_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class V035HandoffPacket:
    handoff_id: str
    source_version: str
    target_version_track: str
    source_snapshot_id: str
    release_manifest_id: str | None
    recommended_next_track: str
    recommended_next_release: str
    controlled_patch_proposal_items: list[str] = field(default_factory=list)
    reusable_request_envelope_items: list[str] = field(default_factory=list)
    reusable_response_envelope_items: list[str] = field(default_factory=list)
    reusable_action_quarantine_items: list[str] = field(default_factory=list)
    reusable_model_backed_step_items: list[str] = field(default_factory=list)
    reusable_trace_items: list[str] = field(default_factory=list)
    reusable_cli_items: list[str] = field(default_factory=list)
    required_new_boundaries: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    readiness_level: ControlledModelInvocationConsolidationReadinessLevel | str = ControlledModelInvocationConsolidationReadinessLevel.HANDOFF_READY_FOR_V035
    ready_for_v035: bool = False
    ready_for_execution: bool = False
    ready_for_patch_proposal: bool = False
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_direct_provider_invocation: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("handoff_id", self.handoff_id)
        _validate_version_includes_v0349(self.source_version)
        _require_non_blank("target_version_track", self.target_version_track)
        if "v0.35" not in self.target_version_track:
            raise ValueError("target_version_track should refer to v0.35")
        _require_non_blank("source_snapshot_id", self.source_snapshot_id)
        if self.release_manifest_id is not None:
            _require_non_blank("release_manifest_id", self.release_manifest_id)
        _require_non_blank("recommended_next_track", self.recommended_next_track)
        if "Controlled Patch Proposal Layer" not in self.recommended_next_track:
            raise ValueError("recommended_next_track should mention Controlled Patch Proposal Layer")
        _require_non_blank("recommended_next_release", self.recommended_next_release)
        for name in (
            "controlled_patch_proposal_items",
            "reusable_request_envelope_items",
            "reusable_response_envelope_items",
            "reusable_action_quarantine_items",
            "reusable_model_backed_step_items",
            "reusable_trace_items",
            "reusable_cli_items",
            "required_new_boundaries",
            "prohibited_until_later_gate",
            "future_track_items",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        ControlledModelInvocationConsolidationReadinessLevel(self.readiness_level)
        if self.ready_for_execution or self.ready_for_patch_proposal or self.ready_for_patch_application or self.ready_for_workspace_write or self.ready_for_code_edit or self.ready_for_direct_provider_invocation:
            raise ValueError("v0.34.9 handoff cannot enable execution, patch proposal/application, write/edit, or direct provider readiness")
        _validate_contains_terms(
            "prohibited_until_later_gate",
            self.prohibited_until_later_gate,
            ["patch application", "workspace write", "code edit", "shell", "command", "direct provider", "direct network", "credential", "autonomous", "general tool", "UI", "authority"],
        )
        _validate_metadata_no_runtime_expansion(self.metadata)

    @property
    def implementation(self) -> bool:
        return False


@dataclass(frozen=True)
class V034ConsolidationReport:
    report_id: str
    version: str
    release_name: str
    snapshot_id: str
    release_manifest_id: str
    handoff_id: str | None
    consolidation_status: ControlledModelInvocationConsolidationStatus | str
    readiness_level: ControlledModelInvocationConsolidationReadinessLevel | str
    summary: str
    completed_items: list[str] = field(default_factory=list)
    controlled_enabled_items: list[str] = field(default_factory=list)
    bounded_enabled_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    runtime_not_ready_items: list[str] = field(default_factory=list)
    v035_handoff_summary: str = ""
    ready_for_v035: bool = False
    ready_for_controlled_model_invocation_boundary_v1: bool = False
    ready_for_controlled_existing_boundary_invocation: bool = False
    ready_for_bounded_model_backed_step_execution: bool = False
    ready_for_cli_model_backed_surface: bool = False
    ready_for_model_invocation_trace_packet_creation: bool = False
    ready_for_execution: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_direct_provider_invocation: bool = False
    ready_for_provider_sdk_invocation: bool = False
    ready_for_direct_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_secret_read: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_unquarantined_action_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_proposal: bool = False
    ready_for_patch_application: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0349(self.version)
        _require_non_blank("release_name", self.release_name)
        _require_non_blank("snapshot_id", self.snapshot_id)
        _require_non_blank("release_manifest_id", self.release_manifest_id)
        if self.handoff_id is not None:
            _require_non_blank("handoff_id", self.handoff_id)
        ControlledModelInvocationConsolidationStatus(self.consolidation_status)
        ControlledModelInvocationConsolidationReadinessLevel(self.readiness_level)
        _require_non_blank("summary", self.summary)
        _require_non_blank("v035_handoff_summary", self.v035_handoff_summary)
        for name in (
            "completed_items",
            "controlled_enabled_items",
            "bounded_enabled_items",
            "blocked_items",
            "future_track_items",
            "runtime_not_ready_items",
            "evidence_refs",
            "withdrawal_conditions",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, REPORT_UNSAFE_FLAG_NAMES)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False in v0.34.9")
        _validate_metadata_no_runtime_expansion(self.metadata)

    @property
    def runtime_expansion(self) -> bool:
        return False


def build_controlled_model_invocation_release_flags(
    flag_set_id: str = "controlled_model_invocation_release_flags:v0.34.9",
    **kwargs: Any,
) -> ControlledModelInvocationReleaseFlagSet:
    return ControlledModelInvocationReleaseFlagSet(
        flag_set_id=flag_set_id,
        version=kwargs.pop("version", V0349_VERSION),
        controlled_model_invocation_boundary_v1_ready=kwargs.pop("controlled_model_invocation_boundary_v1_ready", True),
        ready_for_v035_handoff=kwargs.pop("ready_for_v035_handoff", True),
        ready_for_controlled_model_invocation_boundary=kwargs.pop("ready_for_controlled_model_invocation_boundary", True),
        ready_for_controlled_existing_boundary_invocation=kwargs.pop("ready_for_controlled_existing_boundary_invocation", True),
        ready_for_bounded_model_backed_step_execution=kwargs.pop("ready_for_bounded_model_backed_step_execution", True),
        ready_for_agent_step_runner_model_integration=kwargs.pop("ready_for_agent_step_runner_model_integration", True),
        ready_for_cli_model_backed_surface=kwargs.pop("ready_for_cli_model_backed_surface", True),
        ready_for_model_invocation_trace_packet_creation=kwargs.pop("ready_for_model_invocation_trace_packet_creation", True),
        ready_for_bounded_model_invocation_ocel_trace_emission=kwargs.pop("ready_for_bounded_model_invocation_ocel_trace_emission", True),
        max_grantable_level=kwargs.pop("max_grantable_level", "D3_SIMULATE"),
        **kwargs,
    )


def build_controlled_model_invocation_snapshot(
    snapshot_id: str = "controlled_model_invocation_snapshot:v0.34.9",
    release_flags: ControlledModelInvocationReleaseFlagSet | None = None,
    **kwargs: Any,
) -> ControlledModelInvocationSnapshot:
    return ControlledModelInvocationSnapshot(
        snapshot_id=snapshot_id,
        version=kwargs.pop("version", V0349_VERSION),
        release_name=kwargs.pop("release_name", CONTROLLED_MODEL_INVOCATION_BOUNDARY_V1),
        included_versions=kwargs.pop("included_versions", list(V034_INCLUDED_VERSIONS)),
        included_modules=kwargs.pop("included_modules", list(DEFAULT_INCLUDED_MODULES)),
        included_artifact_groups=kwargs.pop("included_artifact_groups", ["controlled model invocation boundary", "provider policy", "request/response envelopes", "existing boundary adapter", "action quarantine", "model-backed step", "trace packet", "CLI surface"]),
        release_flags=release_flags or build_controlled_model_invocation_release_flags(),
        consolidation_status=kwargs.pop("consolidation_status", ControlledModelInvocationConsolidationStatus.CONSOLIDATED_WITH_GAPS),
        readiness_level=kwargs.pop("readiness_level", ControlledModelInvocationConsolidationReadinessLevel.HANDOFF_READY_FOR_V035),
        summary=kwargs.pop("summary", "v0.34.9 consolidates Controlled Model Invocation Boundary v1 as bounded foundation only."),
        controlled_capabilities=kwargs.pop("controlled_capabilities", [*DEFAULT_CONTROLLED_CAPABILITIES, *DEFAULT_BOUNDED_CAPABILITIES]),
        prohibited_capabilities=kwargs.pop("prohibited_capabilities", list(DEFAULT_PROHIBITED_CAPABILITIES)),
        known_gaps=kwargs.pop("known_gaps", ["v0.35 patch proposal remains future-track; patch application remains prohibited."]),
        known_risks=kwargs.pop("known_risks", ["Unsafe runtime surfaces remain explicitly prohibited."]),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", list(DEFAULT_WITHDRAWAL_CONDITIONS)),
        **kwargs,
    )


def build_controlled_model_invocation_capability_matrix(
    capability_matrix_id: str = "controlled_model_invocation_capability_matrix:v0.34.9",
    **kwargs: Any,
) -> ControlledModelInvocationCapabilityMatrix:
    capability_to_version = {
        "controlled model invocation boundary definitions": "v0.34.0",
        "provider profile metadata and invocation policy": "v0.34.1",
        "model request envelope construction and validation": "v0.34.2",
        "model response envelope sanitizer and action-signal detection": "v0.34.3",
        "existing provider boundary adapter through injected project-local boundary only": "v0.34.4",
        "model output action quarantine": "v0.34.5",
        "bounded model-backed step through v0.34.6": "v0.34.6",
        "model invocation trace packet creation through v0.34.7": "v0.34.7",
        "bounded CLI model-backed surface through v0.34.8": "v0.34.8",
    }
    prohibited_reasons = {item: "Prohibited until a later explicit gate; not opened by v0.34.9." for item in DEFAULT_PROHIBITED_CAPABILITIES}
    return ControlledModelInvocationCapabilityMatrix(
        capability_matrix_id=capability_matrix_id,
        version=kwargs.pop("version", V0349_VERSION),
        enabled_controlled_capabilities=kwargs.pop("enabled_controlled_capabilities", list(DEFAULT_CONTROLLED_CAPABILITIES)),
        enabled_bounded_capabilities=kwargs.pop("enabled_bounded_capabilities", list(DEFAULT_BOUNDED_CAPABILITIES)),
        design_stage_capabilities=kwargs.pop("design_stage_capabilities", ["v0.35 Controlled Patch Proposal Layer handoff"]),
        prohibited_capabilities=kwargs.pop("prohibited_capabilities", list(DEFAULT_PROHIBITED_CAPABILITIES)),
        future_track_capabilities=kwargs.pop("future_track_capabilities", list(DEFAULT_FUTURE_TRACK_ITEMS)),
        capability_to_version=kwargs.pop("capability_to_version", capability_to_version),
        prohibited_capability_to_reason=kwargs.pop("prohibited_capability_to_reason", prohibited_reasons),
        **kwargs,
    )


def build_controlled_model_invocation_coverage(
    coverage_cls: type[_ControlledModelInvocationCoverageBase],
    coverage_id: str,
    stage_version: str,
    **kwargs: Any,
) -> _ControlledModelInvocationCoverageBase:
    return coverage_cls(
        coverage_id=coverage_id,
        version=kwargs.pop("version", V0349_VERSION),
        stage_version=stage_version,
        covered_artifact_refs=kwargs.pop("covered_artifact_refs", []),
        covered_test_refs=kwargs.pop("covered_test_refs", []),
        covered_doc_refs=kwargs.pop("covered_doc_refs", []),
        coverage_notes=kwargs.pop("coverage_notes", ["Coverage is release-readiness metadata, not production certification."]),
        coverage_complete=kwargs.pop("coverage_complete", True),
        **kwargs,
    )


def build_controlled_model_invocation_boundary_coverage(**kwargs: Any) -> ControlledModelInvocationBoundaryCoverage:
    return build_controlled_model_invocation_coverage(ControlledModelInvocationBoundaryCoverage, kwargs.pop("coverage_id", "coverage:v0.34.0:boundary"), "v0.34.0", covered_artifact_refs=kwargs.pop("covered_artifact_refs", [DEFAULT_INCLUDED_MODULES[0]]), covered_test_refs=kwargs.pop("covered_test_refs", [DEFAULT_INCLUDED_TESTS[0]]), covered_doc_refs=kwargs.pop("covered_doc_refs", [DEFAULT_INCLUDED_DOCS[0]]), **kwargs)


def build_provider_profile_policy_coverage(**kwargs: Any) -> ProviderProfilePolicyCoverage:
    return build_controlled_model_invocation_coverage(ProviderProfilePolicyCoverage, kwargs.pop("coverage_id", "coverage:v0.34.1:provider_profile"), "v0.34.1", covered_artifact_refs=kwargs.pop("covered_artifact_refs", [DEFAULT_INCLUDED_MODULES[1]]), covered_test_refs=kwargs.pop("covered_test_refs", [DEFAULT_INCLUDED_TESTS[1]]), covered_doc_refs=kwargs.pop("covered_doc_refs", [DEFAULT_INCLUDED_DOCS[1]]), **kwargs)


def build_model_request_envelope_coverage(**kwargs: Any) -> ModelRequestEnvelopeCoverage:
    return build_controlled_model_invocation_coverage(ModelRequestEnvelopeCoverage, kwargs.pop("coverage_id", "coverage:v0.34.2:model_request"), "v0.34.2", covered_artifact_refs=kwargs.pop("covered_artifact_refs", [DEFAULT_INCLUDED_MODULES[2]]), covered_test_refs=kwargs.pop("covered_test_refs", [DEFAULT_INCLUDED_TESTS[2]]), covered_doc_refs=kwargs.pop("covered_doc_refs", [DEFAULT_INCLUDED_DOCS[2]]), **kwargs)


def build_model_response_envelope_coverage(**kwargs: Any) -> ModelResponseEnvelopeCoverage:
    return build_controlled_model_invocation_coverage(ModelResponseEnvelopeCoverage, kwargs.pop("coverage_id", "coverage:v0.34.3:model_response"), "v0.34.3", covered_artifact_refs=kwargs.pop("covered_artifact_refs", [DEFAULT_INCLUDED_MODULES[3]]), covered_test_refs=kwargs.pop("covered_test_refs", [DEFAULT_INCLUDED_TESTS[3]]), covered_doc_refs=kwargs.pop("covered_doc_refs", [DEFAULT_INCLUDED_DOCS[3]]), **kwargs)


def build_existing_provider_boundary_adapter_coverage(**kwargs: Any) -> ExistingProviderBoundaryAdapterCoverage:
    return build_controlled_model_invocation_coverage(ExistingProviderBoundaryAdapterCoverage, kwargs.pop("coverage_id", "coverage:v0.34.4:provider_adapter"), "v0.34.4", covered_artifact_refs=kwargs.pop("covered_artifact_refs", [DEFAULT_INCLUDED_MODULES[4]]), covered_test_refs=kwargs.pop("covered_test_refs", [DEFAULT_INCLUDED_TESTS[4]]), covered_doc_refs=kwargs.pop("covered_doc_refs", [DEFAULT_INCLUDED_DOCS[4]]), **kwargs)


def build_model_output_action_quarantine_coverage(**kwargs: Any) -> ModelOutputActionQuarantineCoverage:
    return build_controlled_model_invocation_coverage(ModelOutputActionQuarantineCoverage, kwargs.pop("coverage_id", "coverage:v0.34.5:quarantine"), "v0.34.5", covered_artifact_refs=kwargs.pop("covered_artifact_refs", [DEFAULT_INCLUDED_MODULES[5]]), covered_test_refs=kwargs.pop("covered_test_refs", [DEFAULT_INCLUDED_TESTS[5]]), covered_doc_refs=kwargs.pop("covered_doc_refs", [DEFAULT_INCLUDED_DOCS[5]]), **kwargs)


def build_model_backed_step_integration_coverage(**kwargs: Any) -> ModelBackedStepIntegrationCoverage:
    return build_controlled_model_invocation_coverage(ModelBackedStepIntegrationCoverage, kwargs.pop("coverage_id", "coverage:v0.34.6:model_backed_step"), "v0.34.6", covered_artifact_refs=kwargs.pop("covered_artifact_refs", [DEFAULT_INCLUDED_MODULES[6]]), covered_test_refs=kwargs.pop("covered_test_refs", [DEFAULT_INCLUDED_TESTS[6]]), covered_doc_refs=kwargs.pop("covered_doc_refs", [DEFAULT_INCLUDED_DOCS[6]]), **kwargs)


def build_model_invocation_trace_coverage(**kwargs: Any) -> ModelInvocationTraceCoverage:
    return build_controlled_model_invocation_coverage(ModelInvocationTraceCoverage, kwargs.pop("coverage_id", "coverage:v0.34.7:trace"), "v0.34.7", covered_artifact_refs=kwargs.pop("covered_artifact_refs", [DEFAULT_INCLUDED_MODULES[7]]), covered_test_refs=kwargs.pop("covered_test_refs", [DEFAULT_INCLUDED_TESTS[7]]), covered_doc_refs=kwargs.pop("covered_doc_refs", [DEFAULT_INCLUDED_DOCS[7]]), **kwargs)


def build_cli_model_backed_surface_coverage(**kwargs: Any) -> CLIModelBackedSurfaceCoverage:
    return build_controlled_model_invocation_coverage(CLIModelBackedSurfaceCoverage, kwargs.pop("coverage_id", "coverage:v0.34.8:model_cli_surface"), "v0.34.8", covered_artifact_refs=kwargs.pop("covered_artifact_refs", [DEFAULT_INCLUDED_MODULES[8]]), covered_test_refs=kwargs.pop("covered_test_refs", [DEFAULT_INCLUDED_TESTS[8]]), covered_doc_refs=kwargs.pop("covered_doc_refs", [DEFAULT_INCLUDED_DOCS[8]]), **kwargs)


def build_controlled_model_invocation_boundary_register(boundary_register_id: str = "controlled_model_invocation_boundary_register:v0.34.9", **kwargs: Any) -> ControlledModelInvocationBoundaryRegister:
    return ControlledModelInvocationBoundaryRegister(
        boundary_register_id=boundary_register_id,
        version=kwargs.pop("version", V0349_VERSION),
        inherited_boundaries=kwargs.pop("inherited_boundaries", ["v0.30.9", "v0.31.9", "v0.32.9", "v0.33.9", *V034_INCLUDED_VERSIONS]),
        active_controlled_boundaries=kwargs.pop("active_controlled_boundaries", list(DEFAULT_CONTROLLED_CAPABILITIES)),
        active_bounded_boundaries=kwargs.pop("active_bounded_boundaries", list(DEFAULT_BOUNDED_CAPABILITIES)),
        prohibited_boundaries=kwargs.pop("prohibited_boundaries", list(DEFAULT_PROHIBITED_BOUNDARIES)),
        future_gate_boundaries=kwargs.pop("future_gate_boundaries", list(DEFAULT_FUTURE_TRACK_ITEMS)),
        **kwargs,
    )


def build_controlled_model_invocation_risk_register(risk_register_id: str = "controlled_model_invocation_risk_register:v0.34.9", **kwargs: Any) -> ControlledModelInvocationRiskRegister:
    return ControlledModelInvocationRiskRegister(
        risk_register_id=risk_register_id,
        version=kwargs.pop("version", V0349_VERSION),
        known_risks=kwargs.pop("known_risks", ["provider-boundary confusion", "model-output authority confusion", "CLI-as-shell confusion", "trace-as-persistence confusion"]),
        high_risk_surfaces=kwargs.pop("high_risk_surfaces", list(DEFAULT_PROHIBITED_RUNTIME_SURFACES)),
        prohibited_runtime_surfaces=kwargs.pop("prohibited_runtime_surfaces", list(DEFAULT_PROHIBITED_RUNTIME_SURFACES)),
        mitigations=kwargs.pop("mitigations", ["v0.34.4 existing-boundary gate", "v0.34.5 quarantine", "v0.34.6 bounded step bridge", "v0.34.7 returned trace packets", "v0.34.8 deny-by-default CLI"]),
        **kwargs,
    )


def build_controlled_model_invocation_gap_register(gap_register_id: str = "controlled_model_invocation_gap_register:v0.34.9", **kwargs: Any) -> ControlledModelInvocationGapRegister:
    return ControlledModelInvocationGapRegister(
        gap_register_id=gap_register_id,
        version=kwargs.pop("version", V0349_VERSION),
        blocking_gaps=kwargs.pop("blocking_gaps", []),
        non_blocking_gaps=kwargs.pop("non_blocking_gaps", ["No patch proposal artifacts in v0.34.9.", "No production certification.", "No direct provider SDK or network path."]),
        future_track_items=kwargs.pop("future_track_items", list(DEFAULT_FUTURE_TRACK_ITEMS)),
        recommended_v035_items=kwargs.pop("recommended_v035_items", list(DEFAULT_RECOMMENDED_V035_ITEMS)),
        recommended_later_items=kwargs.pop("recommended_later_items", ["patch application sandbox", "persistent trace store", "UI runtime", "autonomous loop review"]),
        **kwargs,
    )


def build_controlled_model_invocation_release_manifest(
    release_manifest_id: str = "controlled_model_invocation_release_manifest:v0.34.9",
    snapshot_id: str = "controlled_model_invocation_snapshot:v0.34.9",
    release_flags: ControlledModelInvocationReleaseFlagSet | None = None,
    **kwargs: Any,
) -> ControlledModelInvocationReleaseManifest:
    return ControlledModelInvocationReleaseManifest(
        release_manifest_id=release_manifest_id,
        version=kwargs.pop("version", V0349_VERSION),
        release_name=kwargs.pop("release_name", CONTROLLED_MODEL_INVOCATION_BOUNDARY_V1),
        snapshot_id=snapshot_id,
        included_versions=kwargs.pop("included_versions", list(V034_INCLUDED_VERSIONS)),
        included_modules=kwargs.pop("included_modules", list(DEFAULT_INCLUDED_MODULES)),
        included_docs=kwargs.pop("included_docs", list(DEFAULT_INCLUDED_DOCS)),
        included_tests=kwargs.pop("included_tests", list(DEFAULT_INCLUDED_TESTS)),
        focused_test_command=kwargs.pop("focused_test_command", "python -m pytest tests/test_v0349_controlled_model_invocation_boundary_consolidation.py"),
        full_track_test_command=kwargs.pop("full_track_test_command", "python -m pytest " + " ".join([*DEFAULT_INCLUDED_TESTS, "tests/test_v0349_controlled_model_invocation_boundary_consolidation.py"])),
        release_flags=release_flags or build_controlled_model_invocation_release_flags(),
        known_gaps=kwargs.pop("known_gaps", ["v0.35 controlled patch proposal remains future-stage."]),
        known_risks=kwargs.pop("known_risks", ["Unsafe runtime surfaces remain prohibited."]),
        next_handoff_id=kwargs.pop("next_handoff_id", "v035_handoff_packet:v0.34.9"),
        **kwargs,
    )


def build_controlled_model_invocation_audit_trail(audit_trail_id: str = "controlled_model_invocation_audit_trail:v0.34.9", **kwargs: Any) -> ControlledModelInvocationAuditTrail:
    return ControlledModelInvocationAuditTrail(
        audit_trail_id=audit_trail_id,
        version=kwargs.pop("version", V0349_VERSION),
        reviewed_artifact_refs=kwargs.pop("reviewed_artifact_refs", list(DEFAULT_INCLUDED_MODULES)),
        reviewed_test_refs=kwargs.pop("reviewed_test_refs", list(DEFAULT_INCLUDED_TESTS)),
        reviewed_doc_refs=kwargs.pop("reviewed_doc_refs", list(DEFAULT_INCLUDED_DOCS)),
        boundary_checks=kwargs.pop("boundary_checks", ["v0.34.0-v0.34.8 gates remain inherited and unsafe readiness flags remain false."]),
        negative_runtime_checks=kwargs.pop("negative_runtime_checks", list(DEFAULT_PROHIBITED_CAPABILITIES)),
        controlled_capability_checks=kwargs.pop("controlled_capability_checks", [*DEFAULT_CONTROLLED_CAPABILITIES, *DEFAULT_BOUNDED_CAPABILITIES]),
        **kwargs,
    )


def build_v035_handoff_packet(
    handoff_id: str = "v035_handoff_packet:v0.34.9",
    source_snapshot_id: str = "controlled_model_invocation_snapshot:v0.34.9",
    release_manifest_id: str | None = "controlled_model_invocation_release_manifest:v0.34.9",
    **kwargs: Any,
) -> V035HandoffPacket:
    return V035HandoffPacket(
        handoff_id=handoff_id,
        source_version=kwargs.pop("source_version", V0349_VERSION),
        target_version_track=kwargs.pop("target_version_track", "v0.35"),
        source_snapshot_id=source_snapshot_id,
        release_manifest_id=release_manifest_id,
        recommended_next_track=kwargs.pop("recommended_next_track", "v0.35 Controlled Patch Proposal Layer"),
        recommended_next_release=kwargs.pop("recommended_next_release", "v0.35.0 Controlled Patch Proposal Layer Foundation"),
        controlled_patch_proposal_items=kwargs.pop("controlled_patch_proposal_items", list(DEFAULT_RECOMMENDED_V035_ITEMS)),
        reusable_request_envelope_items=kwargs.pop("reusable_request_envelope_items", ["v0.34.2 bounded request envelope refs"]),
        reusable_response_envelope_items=kwargs.pop("reusable_response_envelope_items", ["v0.34.3 sanitized response payloads"]),
        reusable_action_quarantine_items=kwargs.pop("reusable_action_quarantine_items", ["v0.34.5 quarantined safe route decisions"]),
        reusable_model_backed_step_items=kwargs.pop("reusable_model_backed_step_items", ["v0.34.6 bounded step output metadata"]),
        reusable_trace_items=kwargs.pop("reusable_trace_items", ["v0.34.7 returned trace packet metadata"]),
        reusable_cli_items=kwargs.pop("reusable_cli_items", ["v0.34.8 bounded CLI denial and preview patterns"]),
        required_new_boundaries=kwargs.pop("required_new_boundaries", ["patch proposal is artifact only", "patch application remains later human-approved sandbox track"]),
        prohibited_until_later_gate=kwargs.pop("prohibited_until_later_gate", list(DEFAULT_PROHIBITED_UNTIL_LATER_GATE)),
        future_track_items=kwargs.pop("future_track_items", list(DEFAULT_FUTURE_TRACK_ITEMS)),
        ready_for_v035=kwargs.pop("ready_for_v035", True),
        **kwargs,
    )


def build_v034_consolidation_report(
    report_id: str = "v034_consolidation_report:v0.34.9",
    snapshot_id: str = "controlled_model_invocation_snapshot:v0.34.9",
    release_manifest_id: str = "controlled_model_invocation_release_manifest:v0.34.9",
    handoff_id: str | None = "v035_handoff_packet:v0.34.9",
    **kwargs: Any,
) -> V034ConsolidationReport:
    return V034ConsolidationReport(
        report_id=report_id,
        version=kwargs.pop("version", V0349_VERSION),
        release_name=kwargs.pop("release_name", CONTROLLED_MODEL_INVOCATION_BOUNDARY_V1),
        snapshot_id=snapshot_id,
        release_manifest_id=release_manifest_id,
        handoff_id=handoff_id,
        consolidation_status=kwargs.pop("consolidation_status", ControlledModelInvocationConsolidationStatus.CONSOLIDATED_WITH_GAPS),
        readiness_level=kwargs.pop("readiness_level", ControlledModelInvocationConsolidationReadinessLevel.HANDOFF_READY_FOR_V035),
        summary=kwargs.pop("summary", "v0.34.9 consolidates Controlled Model Invocation Boundary v1 only."),
        completed_items=kwargs.pop("completed_items", [*DEFAULT_CONTROLLED_CAPABILITIES, *DEFAULT_BOUNDED_CAPABILITIES]),
        controlled_enabled_items=kwargs.pop("controlled_enabled_items", list(DEFAULT_CONTROLLED_CAPABILITIES)),
        bounded_enabled_items=kwargs.pop("bounded_enabled_items", list(DEFAULT_BOUNDED_CAPABILITIES)),
        blocked_items=kwargs.pop("blocked_items", []),
        future_track_items=kwargs.pop("future_track_items", list(DEFAULT_FUTURE_TRACK_ITEMS)),
        runtime_not_ready_items=kwargs.pop("runtime_not_ready_items", list(DEFAULT_PROHIBITED_CAPABILITIES)),
        v035_handoff_summary=kwargs.pop("v035_handoff_summary", "v0.35 handoff is design-stage only for controlled patch proposal artifacts; no patch application is enabled."),
        ready_for_v035=kwargs.pop("ready_for_v035", True),
        ready_for_controlled_model_invocation_boundary_v1=kwargs.pop("ready_for_controlled_model_invocation_boundary_v1", True),
        ready_for_controlled_existing_boundary_invocation=kwargs.pop("ready_for_controlled_existing_boundary_invocation", True),
        ready_for_bounded_model_backed_step_execution=kwargs.pop("ready_for_bounded_model_backed_step_execution", True),
        ready_for_cli_model_backed_surface=kwargs.pop("ready_for_cli_model_backed_surface", True),
        ready_for_model_invocation_trace_packet_creation=kwargs.pop("ready_for_model_invocation_trace_packet_creation", True),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", list(DEFAULT_WITHDRAWAL_CONDITIONS)),
        **kwargs,
    )


def controlled_model_invocation_flags_preserve_unsafe_false(flags: ControlledModelInvocationReleaseFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_CONSOLIDATION_FLAG_NAMES) and flags.production_certified is False


def controlled_model_invocation_snapshot_is_not_runtime_expansion(snapshot: ControlledModelInvocationSnapshot) -> bool:
    return snapshot.runtime_expansion is False and controlled_model_invocation_flags_preserve_unsafe_false(snapshot.release_flags)


def controlled_model_invocation_capability_matrix_is_not_permission_grant(matrix: ControlledModelInvocationCapabilityMatrix) -> bool:
    return matrix.permission_grant is False and "direct provider SDK invocation" in matrix.prohibited_capabilities


def controlled_model_invocation_audit_confirms_no_unsafe_runtime(audit: ControlledModelInvocationAuditTrail) -> bool:
    no_fields = [name for name in audit.__dataclass_fields__ if name.startswith("no_")]
    return all(getattr(audit, name) is True for name in no_fields) and audit.unsafe_readiness_flags_false_confirmed is True


def v035_handoff_packet_is_design_stage_only(packet: V035HandoffPacket) -> bool:
    return (
        packet.implementation is False
        and packet.ready_for_v035 is True
        and packet.ready_for_execution is False
        and packet.ready_for_patch_proposal is False
        and packet.ready_for_patch_application is False
        and packet.ready_for_workspace_write is False
        and packet.ready_for_code_edit is False
        and packet.ready_for_direct_provider_invocation is False
    )


def v034_consolidation_report_is_not_general_runtime_ready(report: V034ConsolidationReport) -> bool:
    return all(getattr(report, name) is False for name in REPORT_UNSAFE_FLAG_NAMES) and report.production_certified is False and report.runtime_expansion is False
