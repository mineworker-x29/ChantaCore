from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import (
    DEFAULT_FUTURE_TRACK_LEVELS,
    _metadata_flag_true,
    _require_non_blank,
    _validate_string_list,
)


V0339_VERSION = "v0.33.9"
V0339_RELEASE_NAME = "v0.33.9 Internal General Agent Runtime MVP Consolidation"
FOUNDATION_RELEASE_NAME = "Internal General Agent Runtime MVP v1"

V033_INCLUDED_VERSIONS = [
    "v0.33.0",
    "v0.33.1",
    "v0.33.2",
    "v0.33.3",
    "v0.33.4",
    "v0.33.5",
    "v0.33.6",
    "v0.33.7",
    "v0.33.8",
]

DEFAULT_INCLUDED_MODULES = [
    "src/chanta_core/agent_runtime/boundary.py",
    "src/chanta_core/agent_runtime/profile_runtime.py",
    "src/chanta_core/agent_runtime/prompt_assembly.py",
    "src/chanta_core/agent_runtime/session_runtime.py",
    "src/chanta_core/agent_runtime/readonly_tools.py",
    "src/chanta_core/agent_runtime/workspace_inspection.py",
    "src/chanta_core/agent_runtime/step_runner.py",
    "src/chanta_core/agent_runtime/ocel_trace.py",
    "src/chanta_core/agent_runtime/cli_surface.py",
]

DEFAULT_INCLUDED_DOCS = [
    "docs/versions/v0.33/v0.33.0_internal_runtime_boundary_permission_gate.md",
    "docs/versions/v0.33/v0.33.1_agent_profile_runtime.md",
    "docs/versions/v0.33/v0.33.2_prompt_assembly_pipeline.md",
    "docs/versions/v0.33/v0.33.3_session_runtime_turn_state_machine.md",
    "docs/versions/v0.33/v0.33.4_safe_readonly_tool_registry.md",
    "docs/versions/v0.33/v0.33.5_safe_workspace_inspection_tool_pack.md",
    "docs/versions/v0.33/v0.33.6_agent_step_runner_mvp.md",
    "docs/versions/v0.33/v0.33.7_runtime_ocel_trace_emitter.md",
    "docs/versions/v0.33/v0.33.8_cli_agent_run_surface.md",
]

DEFAULT_INCLUDED_TESTS = [
    "tests/test_v0330_internal_runtime_boundary_permission_gate.py",
    "tests/test_v0331_agent_profile_runtime.py",
    "tests/test_v0332_prompt_assembly_pipeline.py",
    "tests/test_v0333_session_runtime_turn_state_machine.py",
    "tests/test_v0334_safe_readonly_tool_registry.py",
    "tests/test_v0335_safe_workspace_inspection_tool_pack.py",
    "tests/test_v0336_agent_step_runner_mvp.py",
    "tests/test_v0337_runtime_ocel_trace_emitter.py",
    "tests/test_v0338_cli_agent_run_surface.py",
]

DEFAULT_BOUNDED_CAPABILITIES = [
    "bounded internal runtime boundary and permission gate",
    "agent profile resolution",
    "prompt assembly output construction",
    "session turn step state-machine artifacts",
    "safe read-only tool registry metadata",
    "bounded safe workspace inspection through v0.33.5 policy",
    "bounded supplied/mock model output agent step runner",
    "bounded internal OCEL trace packet creation",
    "bounded CLI command surface",
]

DEFAULT_DESIGN_STAGE_CAPABILITIES = [
    "v0.34 Controlled Model Invocation Boundary handoff",
    "v0.34 Controlled Patch Proposal Layer handoff",
]

DEFAULT_PROHIBITED_CAPABILITIES = [
    "real provider invocation",
    "real model invocation",
    "autonomous general agent runtime",
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
    "reference test execution",
    "secret file read",
    "network access",
    "credential access",
    "persistent trace write",
    "external trace sink",
    "UI runtime",
    "external control",
    "authority grant",
    "D4-D9 authority grant",
]

DEFAULT_FUTURE_TRACK_ITEMS = [
    "Controlled Model Invocation Provider Boundary",
    "Controlled Patch Proposal Layer",
    "patch apply",
    "autonomous multi-step loop",
    "persistent trace store",
    "UI runtime",
    "external harness adapter",
]

DEFAULT_PROHIBITED_RUNTIME_SURFACES = [
    "real_model_invocation",
    "provider_invocation",
    "shell_execution",
    "subprocess_execution",
    "command_execution",
    "general_tool_execution",
    "workspace_write",
    "code_edit",
    "patch_application",
    "reference_code_execution",
    "reference_import",
    "dependency_install",
    "secret_file_read",
    "credential_access",
    "network_access",
    "persistent_trace_write",
    "external_trace_sink",
    "UI_runtime",
    "external_control",
    "authority_grant",
    "D4_D9_grant",
]

DEFAULT_PROHIBITED_BOUNDARIES = [
    "shell",
    "subprocess",
    "real provider",
    "general tool",
    "write/edit/patch",
    "reference execution",
    "credential access",
    "persistent trace",
    "UI runtime",
    "external control",
    "authority grant",
]

DEFAULT_WITHDRAWAL_CONDITIONS = [
    "Any provider/model invocation path is introduced.",
    "Any shell/subprocess/command execution path is introduced.",
    "Any workspace write/edit/patch path is introduced.",
    "Any general tool execution or autonomous multi-step runtime is introduced.",
    "Any persistent trace file, log, database, or external sink write is introduced.",
    "Any production_certified or ready_for_execution flag becomes true.",
]

DEFAULT_V034_OPTIONS = [
    "Controlled Model Invocation Boundary",
    "Controlled Patch Proposal Layer",
]

DEFAULT_PROHIBITED_UNTIL_LATER_GATE = [
    "real provider invocation",
    "real model invocation",
    "shell",
    "subprocess",
    "command execution",
    "general tool execution",
    "workspace write",
    "code edit",
    "patch application",
    "persistent trace write",
    "external trace sink",
    "UI runtime",
    "external control",
    "authority grant",
]

UNSAFE_MVP_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_general_agent_execution",
    "ready_for_autonomous_agent_runtime",
    "ready_for_real_model_invocation",
    "ready_for_model_invocation",
    "ready_for_provider_invocation",
    "ready_for_general_tool_execution",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_network_access",
    "ready_for_credential_access",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_patch_application",
    "ready_for_registry_mutation",
    "ready_for_memory_mutation",
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
    "ready_for_real_model_invocation",
    "ready_for_provider_invocation",
    "ready_for_general_tool_execution",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_patch_application",
    "ready_for_persistent_trace_write",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
)


class InternalAgentRuntimeMVPConsolidationStatus(StrEnum):
    UNKNOWN = "unknown"
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    CONSOLIDATED = "consolidated"
    CONSOLIDATED_WITH_GAPS = "consolidated_with_gaps"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class InternalAgentRuntimeMVPReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    CONTRACT_READY = "contract_ready"
    BOUNDED_RUNTIME_MVP_READY = "bounded_runtime_mvp_ready"
    BOUNDED_CLI_MVP_READY = "bounded_cli_mvp_ready"
    HANDOFF_READY_FOR_V034 = "handoff_ready_for_v034"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


def _validate_version_includes_v0339(version: str) -> None:
    _require_non_blank("version", version)
    if V0339_VERSION not in version:
        raise ValueError("version must include v0.33.9")


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.33.9")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise TypeError(f"{name} must be dict[str, Any]")


def _validate_non_negative_int(name: str, value: int) -> None:
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be >= 0")


def _validate_included_versions(values: list[str]) -> None:
    _validate_string_list("included_versions", values)
    missing = set(V033_INCLUDED_VERSIONS) - set(values)
    if missing:
        raise ValueError(f"included_versions must include v0.33.0 through v0.33.8: {sorted(missing)}")


def _validate_contains_all(name: str, values: list[str], required: list[str]) -> None:
    _validate_string_list(name, values)
    lowered = {value.lower() for value in values}
    missing = [item for item in required if item.lower() not in lowered]
    if missing:
        raise ValueError(f"{name} missing required values: {missing}")


def _validate_contains_terms(name: str, values: list[str], terms: list[str]) -> None:
    _validate_string_list(name, values)
    lowered = " | ".join(values).lower()
    missing = [term for term in terms if term.lower() not in lowered]
    if missing:
        raise ValueError(f"{name} missing required terms: {missing}")


def _validate_level_not_d4_d9(level: str | None) -> None:
    if level is None:
        return
    _require_non_blank("max_grantable_level", level)
    normalized = level.strip().upper()
    if any(normalized.startswith(value) for value in DEFAULT_FUTURE_TRACK_LEVELS):
        raise ValueError("D4-D9 must remain future-track in v0.33.9")


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
            "shell_execution",
            "workspace_write",
            "persistent_trace_write",
        },
    ):
        raise ValueError("v0.33.9 consolidation metadata cannot imply runtime expansion")


@dataclass(frozen=True)
class InternalAgentRuntimeMVPReleaseFlagSet:
    flag_set_id: str
    version: str = V0339_VERSION
    internal_general_agent_runtime_mvp_v1_ready: bool = False
    ready_for_v034_handoff: bool = False
    ready_for_bounded_internal_runtime_mvp: bool = False
    ready_for_bounded_cli_agent_run: bool = False
    ready_for_bounded_agent_step_execution: bool = False
    ready_for_supplied_model_output_processing: bool = False
    ready_for_mock_model_output_processing: bool = False
    ready_for_safe_workspace_inspection_execution: bool = False
    ready_for_safe_readonly_tool_execution: bool = False
    ready_for_bounded_internal_ocel_trace_emission: bool = False
    ready_for_trace_packet_creation: bool = False
    ready_for_execution: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_real_model_invocation: bool = False
    ready_for_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_application: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
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
        _validate_version_includes_v0339(self.version)
        _validate_false(self, UNSAFE_MVP_FLAG_NAMES)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False in v0.33.9")
        _validate_level_not_d4_d9(self.max_grantable_level)
        _validate_future_track_levels(self.future_track_levels)
        _validate_metadata_no_runtime_expansion(self.metadata)


@dataclass(frozen=True)
class InternalAgentRuntimeMVPSnapshot:
    snapshot_id: str
    version: str
    release_name: str
    included_versions: list[str]
    included_modules: list[str]
    included_artifact_groups: list[str]
    release_flags: InternalAgentRuntimeMVPReleaseFlagSet
    consolidation_status: InternalAgentRuntimeMVPConsolidationStatus | str
    readiness_level: InternalAgentRuntimeMVPReadinessLevel | str
    summary: str
    bounded_capabilities: list[str] = field(default_factory=list)
    prohibited_capabilities: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    known_gaps: list[str] = field(default_factory=list)
    known_risks: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("snapshot_id", self.snapshot_id)
        _validate_version_includes_v0339(self.version)
        _require_non_blank("release_name", self.release_name)
        _validate_included_versions(self.included_versions)
        for name in (
            "included_modules",
            "included_artifact_groups",
            "bounded_capabilities",
            "prohibited_capabilities",
            "evidence_refs",
            "known_gaps",
            "known_risks",
            "withdrawal_conditions",
        ):
            _validate_string_list(name, getattr(self, name))
        if not isinstance(self.release_flags, InternalAgentRuntimeMVPReleaseFlagSet):
            raise TypeError("release_flags must be InternalAgentRuntimeMVPReleaseFlagSet")
        if not internal_agent_runtime_mvp_flags_preserve_unsafe_false(self.release_flags):
            raise ValueError("release_flags must preserve unsafe readiness false")
        InternalAgentRuntimeMVPConsolidationStatus(self.consolidation_status)
        InternalAgentRuntimeMVPReadinessLevel(self.readiness_level)
        _require_non_blank("summary", self.summary)
        _validate_metadata_no_runtime_expansion(self.metadata)

    @property
    def runtime_expansion(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalRuntimeMVPCapabilityMatrix:
    capability_matrix_id: str
    version: str
    enabled_bounded_capabilities: list[str] = field(default_factory=list)
    design_stage_capabilities: list[str] = field(default_factory=list)
    prohibited_capabilities: list[str] = field(default_factory=list)
    future_track_capabilities: list[str] = field(default_factory=list)
    bounded_capability_to_version: dict[str, str] = field(default_factory=dict)
    prohibited_capability_to_reason: dict[str, str] = field(default_factory=dict)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("capability_matrix_id", self.capability_matrix_id)
        _validate_version_includes_v0339(self.version)
        for name in (
            "enabled_bounded_capabilities",
            "design_stage_capabilities",
            "prohibited_capabilities",
            "future_track_capabilities",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_dict("bounded_capability_to_version", self.bounded_capability_to_version)
        if not all(isinstance(value, str) for value in self.bounded_capability_to_version.values()):
            raise TypeError("bounded_capability_to_version must be dict[str, str]")
        _validate_dict("prohibited_capability_to_reason", self.prohibited_capability_to_reason)
        if not all(isinstance(value, str) for value in self.prohibited_capability_to_reason.values()):
            raise TypeError("prohibited_capability_to_reason must be dict[str, str]")
        _validate_contains_terms(
            "prohibited_capabilities",
            self.prohibited_capabilities,
            ["provider", "shell", "write", "general tool", "autonomous", "persistent trace", "UI"],
        )
        _validate_metadata_no_runtime_expansion(self.metadata)

    @property
    def permission_grant(self) -> bool:
        return False


@dataclass(frozen=True)
class _InternalRuntimeMVPCoverageBase:
    coverage_id: str
    version: str
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
        _validate_version_includes_v0339(self.version)
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
class InternalRuntimeBoundaryCoverage(_InternalRuntimeMVPCoverageBase):
    pass


@dataclass(frozen=True)
class AgentProfileRuntimeCoverage(_InternalRuntimeMVPCoverageBase):
    pass


@dataclass(frozen=True)
class PromptAssemblyCoverage(_InternalRuntimeMVPCoverageBase):
    pass


@dataclass(frozen=True)
class SessionRuntimeCoverage(_InternalRuntimeMVPCoverageBase):
    pass


@dataclass(frozen=True)
class ReadOnlyToolRegistryCoverage(_InternalRuntimeMVPCoverageBase):
    pass


@dataclass(frozen=True)
class WorkspaceInspectionCoverage(_InternalRuntimeMVPCoverageBase):
    pass


@dataclass(frozen=True)
class AgentStepRunnerCoverage(_InternalRuntimeMVPCoverageBase):
    pass


@dataclass(frozen=True)
class RuntimeOCELTraceCoverage(_InternalRuntimeMVPCoverageBase):
    pass


@dataclass(frozen=True)
class CLIAgentSurfaceCoverage(_InternalRuntimeMVPCoverageBase):
    pass


@dataclass(frozen=True)
class InternalRuntimeMVPBoundaryRegister:
    boundary_register_id: str
    version: str
    inherited_boundaries: list[str] = field(default_factory=list)
    active_bounded_boundaries: list[str] = field(default_factory=list)
    prohibited_boundaries: list[str] = field(default_factory=list)
    future_gate_boundaries: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_register_id", self.boundary_register_id)
        _validate_version_includes_v0339(self.version)
        for name in (
            "inherited_boundaries",
            "active_bounded_boundaries",
            "prohibited_boundaries",
            "future_gate_boundaries",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_contains_terms("prohibited_boundaries", self.prohibited_boundaries, DEFAULT_PROHIBITED_BOUNDARIES)
        _validate_metadata_no_runtime_expansion(self.metadata)

    @property
    def runtime_enforcement(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalRuntimeMVPRiskRegister:
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
        _validate_version_includes_v0339(self.version)
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
class InternalRuntimeMVPGapRegister:
    gap_register_id: str
    version: str
    blocking_gaps: list[str] = field(default_factory=list)
    non_blocking_gaps: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    recommended_v034_items: list[str] = field(default_factory=list)
    recommended_later_items: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("gap_register_id", self.gap_register_id)
        _validate_version_includes_v0339(self.version)
        for name in (
            "blocking_gaps",
            "non_blocking_gaps",
            "future_track_items",
            "recommended_v034_items",
            "recommended_later_items",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_contains_terms(
            "future_track_items",
            self.future_track_items,
            ["provider", "patch proposal", "autonomous", "persistent trace", "UI runtime", "external harness"],
        )
        _validate_metadata_no_runtime_expansion(self.metadata)


@dataclass(frozen=True)
class InternalRuntimeMVPReleaseManifest:
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
    release_flags: InternalAgentRuntimeMVPReleaseFlagSet
    known_gaps: list[str] = field(default_factory=list)
    known_risks: list[str] = field(default_factory=list)
    next_handoff_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("release_manifest_id", self.release_manifest_id)
        _validate_version_includes_v0339(self.version)
        _require_non_blank("release_name", self.release_name)
        _require_non_blank("snapshot_id", self.snapshot_id)
        _validate_included_versions(self.included_versions)
        for name in ("included_modules", "included_docs", "included_tests", "known_gaps", "known_risks"):
            _validate_string_list(name, getattr(self, name))
        _require_non_blank("focused_test_command", self.focused_test_command)
        _require_non_blank("full_track_test_command", self.full_track_test_command)
        if not isinstance(self.release_flags, InternalAgentRuntimeMVPReleaseFlagSet):
            raise TypeError("release_flags must be InternalAgentRuntimeMVPReleaseFlagSet")
        if not internal_agent_runtime_mvp_flags_preserve_unsafe_false(self.release_flags):
            raise ValueError("release_flags must preserve unsafe readiness false")
        _validate_metadata_no_runtime_expansion(self.metadata)

    @property
    def production_release(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalRuntimeMVPAuditTrail:
    audit_trail_id: str
    version: str
    reviewed_artifact_refs: list[str] = field(default_factory=list)
    reviewed_test_refs: list[str] = field(default_factory=list)
    reviewed_doc_refs: list[str] = field(default_factory=list)
    boundary_checks: list[str] = field(default_factory=list)
    negative_runtime_checks: list[str] = field(default_factory=list)
    bounded_capability_checks: list[str] = field(default_factory=list)
    no_real_model_invocation_confirmed: bool = True
    no_provider_invocation_confirmed: bool = True
    no_shell_execution_confirmed: bool = True
    no_subprocess_execution_confirmed: bool = True
    no_command_execution_confirmed: bool = True
    no_general_tool_execution_confirmed: bool = True
    no_workspace_write_confirmed: bool = True
    no_code_edit_confirmed: bool = True
    no_patch_application_confirmed: bool = True
    no_reference_code_execution_confirmed: bool = True
    no_reference_import_confirmed: bool = True
    no_dependency_install_confirmed: bool = True
    no_secret_file_read_confirmed: bool = True
    no_network_access_confirmed: bool = True
    no_credential_access_confirmed: bool = True
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
        _validate_version_includes_v0339(self.version)
        for name in (
            "reviewed_artifact_refs",
            "reviewed_test_refs",
            "reviewed_doc_refs",
            "boundary_checks",
            "negative_runtime_checks",
            "bounded_capability_checks",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True for successful v0.33.9 consolidation")
        if self.unsafe_readiness_flags_false_confirmed is not True:
            raise ValueError("unsafe_readiness_flags_false_confirmed must be True")
        _validate_metadata_no_runtime_expansion(self.metadata)

    @property
    def runtime_audit_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class V034HandoffPacket:
    handoff_id: str
    source_version: str
    target_version_track: str
    source_snapshot_id: str
    release_manifest_id: str | None
    recommended_next_track: str
    recommended_next_release: str
    recommended_v034_options: list[str] = field(default_factory=list)
    controlled_model_invocation_boundary_items: list[str] = field(default_factory=list)
    controlled_patch_proposal_items: list[str] = field(default_factory=list)
    bounded_runtime_reuse_items: list[str] = field(default_factory=list)
    safety_gate_reuse_items: list[str] = field(default_factory=list)
    reusable_boundary_refs: list[str] = field(default_factory=list)
    reusable_profile_refs: list[str] = field(default_factory=list)
    reusable_prompt_refs: list[str] = field(default_factory=list)
    reusable_session_refs: list[str] = field(default_factory=list)
    reusable_tool_registry_refs: list[str] = field(default_factory=list)
    reusable_workspace_inspection_refs: list[str] = field(default_factory=list)
    reusable_step_runner_refs: list[str] = field(default_factory=list)
    reusable_ocel_trace_refs: list[str] = field(default_factory=list)
    reusable_cli_surface_refs: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    readiness_level: InternalAgentRuntimeMVPReadinessLevel | str = InternalAgentRuntimeMVPReadinessLevel.HANDOFF_READY_FOR_V034
    ready_for_v034: bool = False
    ready_for_execution: bool = False
    ready_for_real_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_workspace_write: bool = False
    ready_for_patch_application: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("handoff_id", self.handoff_id)
        _validate_version_includes_v0339(self.source_version)
        _require_non_blank("target_version_track", self.target_version_track)
        if "v0.34" not in self.target_version_track:
            raise ValueError("target_version_track must refer to v0.34")
        _require_non_blank("source_snapshot_id", self.source_snapshot_id)
        _require_non_blank("recommended_next_track", self.recommended_next_track)
        _require_non_blank("recommended_next_release", self.recommended_next_release)
        for name in (
            "recommended_v034_options",
            "controlled_model_invocation_boundary_items",
            "controlled_patch_proposal_items",
            "bounded_runtime_reuse_items",
            "safety_gate_reuse_items",
            "reusable_boundary_refs",
            "reusable_profile_refs",
            "reusable_prompt_refs",
            "reusable_session_refs",
            "reusable_tool_registry_refs",
            "reusable_workspace_inspection_refs",
            "reusable_step_runner_refs",
            "reusable_ocel_trace_refs",
            "reusable_cli_surface_refs",
            "prohibited_until_later_gate",
            "future_track_items",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_contains_terms("recommended_v034_options", self.recommended_v034_options, ["Controlled Model Invocation Boundary", "Controlled Patch Proposal Layer"])
        _validate_contains_terms("prohibited_until_later_gate", self.prohibited_until_later_gate, DEFAULT_PROHIBITED_UNTIL_LATER_GATE)
        InternalAgentRuntimeMVPReadinessLevel(self.readiness_level)
        _validate_false(
            self,
            (
                "ready_for_execution",
                "ready_for_real_model_invocation",
                "ready_for_provider_invocation",
                "ready_for_workspace_write",
                "ready_for_patch_application",
            ),
        )
        _validate_metadata_no_runtime_expansion(self.metadata)

    @property
    def implementation(self) -> bool:
        return False


@dataclass(frozen=True)
class V033ConsolidationReport:
    report_id: str
    version: str
    release_name: str
    snapshot_id: str
    release_manifest_id: str
    handoff_id: str | None
    consolidation_status: InternalAgentRuntimeMVPConsolidationStatus | str
    readiness_level: InternalAgentRuntimeMVPReadinessLevel | str
    summary: str
    completed_items: list[str] = field(default_factory=list)
    bounded_enabled_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    runtime_not_ready_items: list[str] = field(default_factory=list)
    v034_handoff_summary: str = "v0.34 handoff is design-stage only."
    ready_for_v034: bool = False
    ready_for_bounded_internal_runtime_mvp: bool = False
    ready_for_bounded_cli_agent_run: bool = False
    ready_for_execution: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_real_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
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
        _validate_version_includes_v0339(self.version)
        _require_non_blank("release_name", self.release_name)
        _require_non_blank("snapshot_id", self.snapshot_id)
        _require_non_blank("release_manifest_id", self.release_manifest_id)
        InternalAgentRuntimeMVPConsolidationStatus(self.consolidation_status)
        InternalAgentRuntimeMVPReadinessLevel(self.readiness_level)
        _require_non_blank("summary", self.summary)
        _require_non_blank("v034_handoff_summary", self.v034_handoff_summary)
        for name in (
            "completed_items",
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
            raise ValueError("production_certified must always be False in v0.33.9")
        if self.ready_for_v034 and self.blocked_items:
            raise ValueError("ready_for_v034 design-stage handoff cannot be true with blocked_items")
        _validate_metadata_no_runtime_expansion(self.metadata)

    @property
    def runtime_expansion(self) -> bool:
        return False


def build_internal_agent_runtime_mvp_release_flags(
    flag_set_id: str = "internal_agent_runtime_mvp_release_flags:v0.33.9",
    **kwargs: Any,
) -> InternalAgentRuntimeMVPReleaseFlagSet:
    return InternalAgentRuntimeMVPReleaseFlagSet(
        flag_set_id=flag_set_id,
        version=kwargs.pop("version", V0339_VERSION),
        internal_general_agent_runtime_mvp_v1_ready=kwargs.pop("internal_general_agent_runtime_mvp_v1_ready", True),
        ready_for_v034_handoff=kwargs.pop("ready_for_v034_handoff", True),
        ready_for_bounded_internal_runtime_mvp=kwargs.pop("ready_for_bounded_internal_runtime_mvp", True),
        ready_for_bounded_cli_agent_run=kwargs.pop("ready_for_bounded_cli_agent_run", True),
        ready_for_bounded_agent_step_execution=kwargs.pop("ready_for_bounded_agent_step_execution", True),
        ready_for_supplied_model_output_processing=kwargs.pop("ready_for_supplied_model_output_processing", True),
        ready_for_mock_model_output_processing=kwargs.pop("ready_for_mock_model_output_processing", True),
        ready_for_safe_workspace_inspection_execution=kwargs.pop("ready_for_safe_workspace_inspection_execution", True),
        ready_for_safe_readonly_tool_execution=kwargs.pop("ready_for_safe_readonly_tool_execution", True),
        ready_for_bounded_internal_ocel_trace_emission=kwargs.pop("ready_for_bounded_internal_ocel_trace_emission", True),
        ready_for_trace_packet_creation=kwargs.pop("ready_for_trace_packet_creation", True),
        **kwargs,
    )


def build_internal_agent_runtime_mvp_snapshot(
    snapshot_id: str = "internal_agent_runtime_mvp_snapshot:v0.33.9",
    release_flags: InternalAgentRuntimeMVPReleaseFlagSet | None = None,
    **kwargs: Any,
) -> InternalAgentRuntimeMVPSnapshot:
    return InternalAgentRuntimeMVPSnapshot(
        snapshot_id=snapshot_id,
        version=kwargs.pop("version", V0339_VERSION),
        release_name=kwargs.pop("release_name", FOUNDATION_RELEASE_NAME),
        included_versions=kwargs.pop("included_versions", list(V033_INCLUDED_VERSIONS)),
        included_modules=kwargs.pop("included_modules", list(DEFAULT_INCLUDED_MODULES)),
        included_artifact_groups=kwargs.pop(
            "included_artifact_groups",
            ["boundary", "profile", "prompt", "session", "registry", "workspace_inspection", "step_runner", "trace", "cli"],
        ),
        release_flags=release_flags or build_internal_agent_runtime_mvp_release_flags(),
        consolidation_status=kwargs.pop("consolidation_status", InternalAgentRuntimeMVPConsolidationStatus.CONSOLIDATED_WITH_GAPS),
        readiness_level=kwargs.pop("readiness_level", InternalAgentRuntimeMVPReadinessLevel.HANDOFF_READY_FOR_V034),
        summary=kwargs.pop("summary", "v0.33.x is consolidated as a bounded internal general agent runtime MVP v1."),
        bounded_capabilities=kwargs.pop("bounded_capabilities", list(DEFAULT_BOUNDED_CAPABILITIES)),
        prohibited_capabilities=kwargs.pop("prohibited_capabilities", list(DEFAULT_PROHIBITED_CAPABILITIES)),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", list(DEFAULT_WITHDRAWAL_CONDITIONS)),
        **kwargs,
    )


def build_internal_runtime_mvp_capability_matrix(
    capability_matrix_id: str = "internal_runtime_mvp_capability_matrix:v0.33.9",
    **kwargs: Any,
) -> InternalRuntimeMVPCapabilityMatrix:
    bounded_to_version = {
        "runtime boundary and permission gate": "v0.33.0",
        "agent profile resolution": "v0.33.1",
        "prompt assembly output construction": "v0.33.2",
        "session turn state-machine artifacts": "v0.33.3",
        "safe read-only tool registry metadata": "v0.33.4",
        "safe workspace inspection": "v0.33.5",
        "bounded supplied/mock step runner": "v0.33.6",
        "bounded internal OCEL trace packet creation": "v0.33.7",
        "bounded CLI command surface": "v0.33.8",
    }
    prohibited_reasons = {item: "Prohibited until a later explicit gate; not opened by v0.33.9." for item in DEFAULT_PROHIBITED_CAPABILITIES}
    return InternalRuntimeMVPCapabilityMatrix(
        capability_matrix_id=capability_matrix_id,
        version=kwargs.pop("version", V0339_VERSION),
        enabled_bounded_capabilities=kwargs.pop("enabled_bounded_capabilities", list(DEFAULT_BOUNDED_CAPABILITIES)),
        design_stage_capabilities=kwargs.pop("design_stage_capabilities", list(DEFAULT_DESIGN_STAGE_CAPABILITIES)),
        prohibited_capabilities=kwargs.pop("prohibited_capabilities", list(DEFAULT_PROHIBITED_CAPABILITIES)),
        future_track_capabilities=kwargs.pop("future_track_capabilities", list(DEFAULT_FUTURE_TRACK_ITEMS)),
        bounded_capability_to_version=kwargs.pop("bounded_capability_to_version", bounded_to_version),
        prohibited_capability_to_reason=kwargs.pop("prohibited_capability_to_reason", prohibited_reasons),
        **kwargs,
    )


def build_internal_runtime_mvp_coverage(
    coverage_cls: type[_InternalRuntimeMVPCoverageBase],
    coverage_id: str,
    **kwargs: Any,
) -> _InternalRuntimeMVPCoverageBase:
    return coverage_cls(
        coverage_id=coverage_id,
        version=kwargs.pop("version", V0339_VERSION),
        covered_artifact_refs=kwargs.pop("covered_artifact_refs", []),
        covered_test_refs=kwargs.pop("covered_test_refs", []),
        covered_doc_refs=kwargs.pop("covered_doc_refs", []),
        coverage_notes=kwargs.pop("coverage_notes", ["Coverage is release-readiness metadata, not production certification."]),
        coverage_complete=kwargs.pop("coverage_complete", True),
        **kwargs,
    )


def build_internal_runtime_boundary_coverage(**kwargs: Any) -> InternalRuntimeBoundaryCoverage:
    return build_internal_runtime_mvp_coverage(
        InternalRuntimeBoundaryCoverage,
        kwargs.pop("coverage_id", "coverage:v0.33.0:boundary"),
        covered_artifact_refs=kwargs.pop("covered_artifact_refs", ["src/chanta_core/agent_runtime/boundary.py"]),
        covered_test_refs=kwargs.pop("covered_test_refs", ["tests/test_v0330_internal_runtime_boundary_permission_gate.py"]),
        covered_doc_refs=kwargs.pop("covered_doc_refs", [DEFAULT_INCLUDED_DOCS[0]]),
        **kwargs,
    )


def build_agent_profile_runtime_coverage(**kwargs: Any) -> AgentProfileRuntimeCoverage:
    return build_internal_runtime_mvp_coverage(
        AgentProfileRuntimeCoverage,
        kwargs.pop("coverage_id", "coverage:v0.33.1:profile"),
        covered_artifact_refs=kwargs.pop("covered_artifact_refs", ["src/chanta_core/agent_runtime/profile_runtime.py"]),
        covered_test_refs=kwargs.pop("covered_test_refs", ["tests/test_v0331_agent_profile_runtime.py"]),
        covered_doc_refs=kwargs.pop("covered_doc_refs", [DEFAULT_INCLUDED_DOCS[1]]),
        **kwargs,
    )


def build_prompt_assembly_coverage(**kwargs: Any) -> PromptAssemblyCoverage:
    return build_internal_runtime_mvp_coverage(
        PromptAssemblyCoverage,
        kwargs.pop("coverage_id", "coverage:v0.33.2:prompt"),
        covered_artifact_refs=kwargs.pop("covered_artifact_refs", ["src/chanta_core/agent_runtime/prompt_assembly.py"]),
        covered_test_refs=kwargs.pop("covered_test_refs", ["tests/test_v0332_prompt_assembly_pipeline.py"]),
        covered_doc_refs=kwargs.pop("covered_doc_refs", [DEFAULT_INCLUDED_DOCS[2]]),
        **kwargs,
    )


def build_session_runtime_coverage(**kwargs: Any) -> SessionRuntimeCoverage:
    return build_internal_runtime_mvp_coverage(
        SessionRuntimeCoverage,
        kwargs.pop("coverage_id", "coverage:v0.33.3:session"),
        covered_artifact_refs=kwargs.pop("covered_artifact_refs", ["src/chanta_core/agent_runtime/session_runtime.py"]),
        covered_test_refs=kwargs.pop("covered_test_refs", ["tests/test_v0333_session_runtime_turn_state_machine.py"]),
        covered_doc_refs=kwargs.pop("covered_doc_refs", [DEFAULT_INCLUDED_DOCS[3]]),
        **kwargs,
    )


def build_readonly_tool_registry_coverage(**kwargs: Any) -> ReadOnlyToolRegistryCoverage:
    return build_internal_runtime_mvp_coverage(
        ReadOnlyToolRegistryCoverage,
        kwargs.pop("coverage_id", "coverage:v0.33.4:readonly_tools"),
        covered_artifact_refs=kwargs.pop("covered_artifact_refs", ["src/chanta_core/agent_runtime/readonly_tools.py"]),
        covered_test_refs=kwargs.pop("covered_test_refs", ["tests/test_v0334_safe_readonly_tool_registry.py"]),
        covered_doc_refs=kwargs.pop("covered_doc_refs", [DEFAULT_INCLUDED_DOCS[4]]),
        **kwargs,
    )


def build_workspace_inspection_coverage(**kwargs: Any) -> WorkspaceInspectionCoverage:
    return build_internal_runtime_mvp_coverage(
        WorkspaceInspectionCoverage,
        kwargs.pop("coverage_id", "coverage:v0.33.5:workspace_inspection"),
        covered_artifact_refs=kwargs.pop("covered_artifact_refs", ["src/chanta_core/agent_runtime/workspace_inspection.py"]),
        covered_test_refs=kwargs.pop("covered_test_refs", ["tests/test_v0335_safe_workspace_inspection_tool_pack.py"]),
        covered_doc_refs=kwargs.pop("covered_doc_refs", [DEFAULT_INCLUDED_DOCS[5]]),
        **kwargs,
    )


def build_agent_step_runner_coverage(**kwargs: Any) -> AgentStepRunnerCoverage:
    return build_internal_runtime_mvp_coverage(
        AgentStepRunnerCoverage,
        kwargs.pop("coverage_id", "coverage:v0.33.6:step_runner"),
        covered_artifact_refs=kwargs.pop("covered_artifact_refs", ["src/chanta_core/agent_runtime/step_runner.py"]),
        covered_test_refs=kwargs.pop("covered_test_refs", ["tests/test_v0336_agent_step_runner_mvp.py"]),
        covered_doc_refs=kwargs.pop("covered_doc_refs", [DEFAULT_INCLUDED_DOCS[6]]),
        **kwargs,
    )


def build_runtime_ocel_trace_coverage(**kwargs: Any) -> RuntimeOCELTraceCoverage:
    return build_internal_runtime_mvp_coverage(
        RuntimeOCELTraceCoverage,
        kwargs.pop("coverage_id", "coverage:v0.33.7:ocel_trace"),
        covered_artifact_refs=kwargs.pop("covered_artifact_refs", ["src/chanta_core/agent_runtime/ocel_trace.py"]),
        covered_test_refs=kwargs.pop("covered_test_refs", ["tests/test_v0337_runtime_ocel_trace_emitter.py"]),
        covered_doc_refs=kwargs.pop("covered_doc_refs", [DEFAULT_INCLUDED_DOCS[7]]),
        **kwargs,
    )


def build_cli_agent_surface_coverage(**kwargs: Any) -> CLIAgentSurfaceCoverage:
    return build_internal_runtime_mvp_coverage(
        CLIAgentSurfaceCoverage,
        kwargs.pop("coverage_id", "coverage:v0.33.8:cli_surface"),
        covered_artifact_refs=kwargs.pop("covered_artifact_refs", ["src/chanta_core/agent_runtime/cli_surface.py"]),
        covered_test_refs=kwargs.pop("covered_test_refs", ["tests/test_v0338_cli_agent_run_surface.py"]),
        covered_doc_refs=kwargs.pop("covered_doc_refs", [DEFAULT_INCLUDED_DOCS[8]]),
        **kwargs,
    )


def build_internal_runtime_mvp_boundary_register(
    boundary_register_id: str = "internal_runtime_mvp_boundary_register:v0.33.9",
    **kwargs: Any,
) -> InternalRuntimeMVPBoundaryRegister:
    return InternalRuntimeMVPBoundaryRegister(
        boundary_register_id=boundary_register_id,
        version=kwargs.pop("version", V0339_VERSION),
        inherited_boundaries=kwargs.pop("inherited_boundaries", ["v0.30.9", "v0.31.9", "v0.32.9", *V033_INCLUDED_VERSIONS]),
        active_bounded_boundaries=kwargs.pop(
            "active_bounded_boundaries",
            ["permission gate", "safe workspace inspection policy", "supplied/mock step boundary", "returned trace packet boundary", "bounded CLI policy"],
        ),
        prohibited_boundaries=kwargs.pop("prohibited_boundaries", list(DEFAULT_PROHIBITED_BOUNDARIES)),
        future_gate_boundaries=kwargs.pop("future_gate_boundaries", list(DEFAULT_FUTURE_TRACK_ITEMS)),
        **kwargs,
    )


def build_internal_runtime_mvp_risk_register(
    risk_register_id: str = "internal_runtime_mvp_risk_register:v0.33.9",
    **kwargs: Any,
) -> InternalRuntimeMVPRiskRegister:
    return InternalRuntimeMVPRiskRegister(
        risk_register_id=risk_register_id,
        version=kwargs.pop("version", V0339_VERSION),
        known_risks=kwargs.pop("known_risks", ["model output injection", "path policy drift", "trace payload overreach", "CLI argument misuse"]),
        high_risk_surfaces=kwargs.pop("high_risk_surfaces", list(DEFAULT_PROHIBITED_RUNTIME_SURFACES)),
        prohibited_runtime_surfaces=kwargs.pop("prohibited_runtime_surfaces", list(DEFAULT_PROHIBITED_RUNTIME_SURFACES)),
        mitigations=kwargs.pop(
            "mitigations",
            ["permission-gated boundaries", "safe read-only path policy", "supplied/mock-only step runner", "returned trace packets", "bounded CLI denial defaults"],
        ),
        **kwargs,
    )


def build_internal_runtime_mvp_gap_register(
    gap_register_id: str = "internal_runtime_mvp_gap_register:v0.33.9",
    **kwargs: Any,
) -> InternalRuntimeMVPGapRegister:
    return InternalRuntimeMVPGapRegister(
        gap_register_id=gap_register_id,
        version=kwargs.pop("version", V0339_VERSION),
        blocking_gaps=kwargs.pop("blocking_gaps", []),
        non_blocking_gaps=kwargs.pop(
            "non_blocking_gaps",
            ["No real provider invocation boundary yet.", "No patch proposal artifacts yet.", "No production certification."],
        ),
        future_track_items=kwargs.pop("future_track_items", list(DEFAULT_FUTURE_TRACK_ITEMS)),
        recommended_v034_items=kwargs.pop("recommended_v034_items", list(DEFAULT_V034_OPTIONS)),
        recommended_later_items=kwargs.pop("recommended_later_items", ["patch apply", "autonomous loop", "persistent trace store", "UI runtime"]),
        **kwargs,
    )


def build_internal_runtime_mvp_release_manifest(
    release_manifest_id: str = "internal_runtime_mvp_release_manifest:v0.33.9",
    snapshot_id: str = "internal_agent_runtime_mvp_snapshot:v0.33.9",
    release_flags: InternalAgentRuntimeMVPReleaseFlagSet | None = None,
    **kwargs: Any,
) -> InternalRuntimeMVPReleaseManifest:
    return InternalRuntimeMVPReleaseManifest(
        release_manifest_id=release_manifest_id,
        version=kwargs.pop("version", V0339_VERSION),
        release_name=kwargs.pop("release_name", FOUNDATION_RELEASE_NAME),
        snapshot_id=snapshot_id,
        included_versions=kwargs.pop("included_versions", list(V033_INCLUDED_VERSIONS)),
        included_modules=kwargs.pop("included_modules", list(DEFAULT_INCLUDED_MODULES)),
        included_docs=kwargs.pop("included_docs", list(DEFAULT_INCLUDED_DOCS)),
        included_tests=kwargs.pop("included_tests", list(DEFAULT_INCLUDED_TESTS)),
        focused_test_command=kwargs.pop("focused_test_command", "python -m pytest tests/test_v0339_internal_general_agent_runtime_mvp_consolidation.py"),
        full_track_test_command=kwargs.pop(
            "full_track_test_command",
            "python -m pytest "
            + " ".join(
                [
                    *DEFAULT_INCLUDED_TESTS,
                    "tests/test_v0339_internal_general_agent_runtime_mvp_consolidation.py",
                ]
            ),
        ),
        release_flags=release_flags or build_internal_agent_runtime_mvp_release_flags(),
        known_gaps=kwargs.pop("known_gaps", ["v0.34 provider boundary and patch proposal remain future-stage."]),
        known_risks=kwargs.pop("known_risks", ["Unsafe runtime surfaces remain explicitly prohibited."]),
        **kwargs,
    )


def build_internal_runtime_mvp_audit_trail(
    audit_trail_id: str = "internal_runtime_mvp_audit_trail:v0.33.9",
    **kwargs: Any,
) -> InternalRuntimeMVPAuditTrail:
    return InternalRuntimeMVPAuditTrail(
        audit_trail_id=audit_trail_id,
        version=kwargs.pop("version", V0339_VERSION),
        reviewed_artifact_refs=kwargs.pop("reviewed_artifact_refs", list(DEFAULT_INCLUDED_MODULES)),
        reviewed_test_refs=kwargs.pop("reviewed_test_refs", list(DEFAULT_INCLUDED_TESTS)),
        reviewed_doc_refs=kwargs.pop("reviewed_doc_refs", list(DEFAULT_INCLUDED_DOCS)),
        boundary_checks=kwargs.pop("boundary_checks", ["v0.33.0-v0.33.8 unsafe readiness flags remain false."]),
        negative_runtime_checks=kwargs.pop("negative_runtime_checks", list(DEFAULT_PROHIBITED_CAPABILITIES)),
        bounded_capability_checks=kwargs.pop("bounded_capability_checks", list(DEFAULT_BOUNDED_CAPABILITIES)),
        **kwargs,
    )


def build_v034_handoff_packet(
    handoff_id: str = "v034_handoff_packet:v0.33.9",
    source_snapshot_id: str = "internal_agent_runtime_mvp_snapshot:v0.33.9",
    release_manifest_id: str | None = "internal_runtime_mvp_release_manifest:v0.33.9",
    **kwargs: Any,
) -> V034HandoffPacket:
    return V034HandoffPacket(
        handoff_id=handoff_id,
        source_version=kwargs.pop("source_version", V0339_VERSION),
        target_version_track=kwargs.pop("target_version_track", "v0.34"),
        source_snapshot_id=source_snapshot_id,
        release_manifest_id=release_manifest_id,
        recommended_next_track=kwargs.pop("recommended_next_track", "v0.34 Controlled Runtime Expansion Design"),
        recommended_next_release=kwargs.pop("recommended_next_release", "v0.34.0 Controlled Model Invocation Boundary"),
        recommended_v034_options=kwargs.pop("recommended_v034_options", list(DEFAULT_V034_OPTIONS)),
        controlled_model_invocation_boundary_items=kwargs.pop(
            "controlled_model_invocation_boundary_items",
            ["connect existing provider/chat_service boundary to v0.33.6 step runner", "strict provider gate", "no shell/write/edit/patch"],
        ),
        controlled_patch_proposal_items=kwargs.pop(
            "controlled_patch_proposal_items",
            ["patch proposals as artifacts only", "no patch application", "human approval gate before any future apply stage"],
        ),
        bounded_runtime_reuse_items=kwargs.pop("bounded_runtime_reuse_items", list(DEFAULT_BOUNDED_CAPABILITIES)),
        safety_gate_reuse_items=kwargs.pop("safety_gate_reuse_items", ["v0.33 permission gate", "v0.33.5 path policy", "v0.33.6 supplied/mock boundary"]),
        reusable_boundary_refs=kwargs.pop("reusable_boundary_refs", ["src/chanta_core/agent_runtime/boundary.py"]),
        reusable_profile_refs=kwargs.pop("reusable_profile_refs", ["src/chanta_core/agent_runtime/profile_runtime.py"]),
        reusable_prompt_refs=kwargs.pop("reusable_prompt_refs", ["src/chanta_core/agent_runtime/prompt_assembly.py"]),
        reusable_session_refs=kwargs.pop("reusable_session_refs", ["src/chanta_core/agent_runtime/session_runtime.py"]),
        reusable_tool_registry_refs=kwargs.pop("reusable_tool_registry_refs", ["src/chanta_core/agent_runtime/readonly_tools.py"]),
        reusable_workspace_inspection_refs=kwargs.pop("reusable_workspace_inspection_refs", ["src/chanta_core/agent_runtime/workspace_inspection.py"]),
        reusable_step_runner_refs=kwargs.pop("reusable_step_runner_refs", ["src/chanta_core/agent_runtime/step_runner.py"]),
        reusable_ocel_trace_refs=kwargs.pop("reusable_ocel_trace_refs", ["src/chanta_core/agent_runtime/ocel_trace.py"]),
        reusable_cli_surface_refs=kwargs.pop("reusable_cli_surface_refs", ["src/chanta_core/agent_runtime/cli_surface.py"]),
        prohibited_until_later_gate=kwargs.pop("prohibited_until_later_gate", list(DEFAULT_PROHIBITED_UNTIL_LATER_GATE)),
        future_track_items=kwargs.pop("future_track_items", list(DEFAULT_FUTURE_TRACK_ITEMS)),
        ready_for_v034=kwargs.pop("ready_for_v034", True),
        **kwargs,
    )


def build_v033_consolidation_report(
    report_id: str = "v033_consolidation_report:v0.33.9",
    snapshot_id: str = "internal_agent_runtime_mvp_snapshot:v0.33.9",
    release_manifest_id: str = "internal_runtime_mvp_release_manifest:v0.33.9",
    handoff_id: str | None = "v034_handoff_packet:v0.33.9",
    **kwargs: Any,
) -> V033ConsolidationReport:
    return V033ConsolidationReport(
        report_id=report_id,
        version=kwargs.pop("version", V0339_VERSION),
        release_name=kwargs.pop("release_name", FOUNDATION_RELEASE_NAME),
        snapshot_id=snapshot_id,
        release_manifest_id=release_manifest_id,
        handoff_id=handoff_id,
        consolidation_status=kwargs.pop("consolidation_status", InternalAgentRuntimeMVPConsolidationStatus.CONSOLIDATED_WITH_GAPS),
        readiness_level=kwargs.pop("readiness_level", InternalAgentRuntimeMVPReadinessLevel.HANDOFF_READY_FOR_V034),
        summary=kwargs.pop("summary", "v0.33.9 consolidates bounded Internal General Agent Runtime MVP v1 only."),
        completed_items=kwargs.pop("completed_items", list(DEFAULT_BOUNDED_CAPABILITIES)),
        bounded_enabled_items=kwargs.pop("bounded_enabled_items", list(DEFAULT_BOUNDED_CAPABILITIES)),
        blocked_items=kwargs.pop("blocked_items", []),
        future_track_items=kwargs.pop("future_track_items", list(DEFAULT_FUTURE_TRACK_ITEMS)),
        runtime_not_ready_items=kwargs.pop("runtime_not_ready_items", list(DEFAULT_PROHIBITED_CAPABILITIES)),
        v034_handoff_summary=kwargs.pop("v034_handoff_summary", "v0.34 handoff is design-stage only; no implementation authority is granted."),
        ready_for_v034=kwargs.pop("ready_for_v034", True),
        ready_for_bounded_internal_runtime_mvp=kwargs.pop("ready_for_bounded_internal_runtime_mvp", True),
        ready_for_bounded_cli_agent_run=kwargs.pop("ready_for_bounded_cli_agent_run", True),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", list(DEFAULT_WITHDRAWAL_CONDITIONS)),
        **kwargs,
    )


def internal_agent_runtime_mvp_flags_preserve_unsafe_false(flags: InternalAgentRuntimeMVPReleaseFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_MVP_FLAG_NAMES) and flags.production_certified is False


def internal_agent_runtime_mvp_snapshot_is_not_runtime_expansion(snapshot: InternalAgentRuntimeMVPSnapshot) -> bool:
    return snapshot.runtime_expansion is False and internal_agent_runtime_mvp_flags_preserve_unsafe_false(snapshot.release_flags)


def internal_runtime_mvp_capability_matrix_is_not_permission_grant(matrix: InternalRuntimeMVPCapabilityMatrix) -> bool:
    return matrix.permission_grant is False and "real provider invocation" in matrix.prohibited_capabilities


def internal_runtime_mvp_audit_confirms_no_unsafe_runtime(audit: InternalRuntimeMVPAuditTrail) -> bool:
    no_fields = [name for name in audit.__dataclass_fields__ if name.startswith("no_")]
    return all(getattr(audit, name) is True for name in no_fields) and audit.unsafe_readiness_flags_false_confirmed is True


def v034_handoff_packet_is_design_stage_only(packet: V034HandoffPacket) -> bool:
    return (
        packet.implementation is False
        and packet.ready_for_execution is False
        and packet.ready_for_real_model_invocation is False
        and packet.ready_for_provider_invocation is False
        and packet.ready_for_workspace_write is False
        and packet.ready_for_patch_application is False
    )


def v033_consolidation_report_is_not_general_runtime_ready(report: V033ConsolidationReport) -> bool:
    return (
        all(getattr(report, name) is False for name in REPORT_UNSAFE_FLAG_NAMES)
        and report.production_certified is False
        and report.runtime_expansion is False
    )
