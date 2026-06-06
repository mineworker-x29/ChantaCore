from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .profiles import _metadata_flag_true, _require_non_blank, _validate_object_list, _validate_string_list


V0329_VERSION = "v0.32.9"
V0329_RELEASE_NAME = "v0.32.9 External Observation / Digestion Consolidation"
V0329_FOUNDATION_RELEASE_NAME = "External Harness Observation & Digestion Pipeline v1"

REQUIRED_V032_INCLUDED_VERSIONS = [
    "v0.32.0",
    "v0.32.1",
    "v0.32.2",
    "v0.32.3",
    "v0.32.4",
    "v0.32.5",
    "v0.32.6",
    "v0.32.7",
    "v0.32.8",
]

DEFAULT_FUTURE_TRACK_LEVELS = ["D4", "D5", "D6", "D7", "D8", "D9"]

DEFAULT_CONSOLIDATION_PROHIBITED_RUNTIME_SURFACES = [
    "external_harness_execution",
    "reference_code_execution",
    "live_scan",
    "source_ref_fetch",
    "read_only_tool_execution",
    "runtime_adapter_loading",
    "dependency_install",
    "runtime_import",
    "plugin_loading",
    "tool_registration",
    "tool_invocation",
    "mission_installation",
    "mission_execution",
    "provider_invocation",
    "network_access",
    "credential_access",
    "command_execution",
    "browser_runtime_control",
    "rpa_runtime_control",
    "gateway_control",
    "packet_send",
    "registry_mutation",
    "memory_mutation",
    "ocel_emission",
    "runtime_trace_persistence",
    "ui_runtime",
    "external_control",
    "authority_grant",
    "D4_D9_grant",
]

DEFAULT_V033_FOCUS_ITEMS = [
    "Internal General Agent Runtime MVP",
    "profile runtime",
    "prompt assembly",
    "session runtime",
    "safe read-only tool registry",
    "safe workspace inspection",
    "agent step runner",
    "runtime OCEL trace emitter",
    "CLI surface",
]


class ExternalPipelineConsolidationStatus(StrEnum):
    UNKNOWN = "unknown"
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    CONSOLIDATED = "consolidated"
    CONSOLIDATED_WITH_GAPS = "consolidated_with_gaps"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class ExternalPipelineReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    CONTRACT_READY = "contract_ready"
    PROFILE_READY = "profile_ready"
    STATIC_OBSERVATION_READY = "static_observation_ready"
    PIPELINE_FOUNDATION_READY = "pipeline_foundation_ready"
    HANDOFF_READY_FOR_V033 = "handoff_ready_for_v033"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


def _validate_version_includes_v0329(version: str) -> None:
    _require_non_blank("version", version)
    if V0329_VERSION not in version:
        raise ValueError("version must include v0.32.9")


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.32.9")


def _validate_required_versions(name: str, values: list[str]) -> None:
    _validate_string_list(name, values)
    missing = set(REQUIRED_V032_INCLUDED_VERSIONS) - set(values)
    if missing:
        raise ValueError(f"{name} must include v0.32.0 through v0.32.8: {sorted(missing)}")


def _validate_prohibited_surfaces(name: str, values: list[str]) -> None:
    _validate_string_list(name, values)
    missing = set(DEFAULT_CONSOLIDATION_PROHIBITED_RUNTIME_SURFACES) - set(values)
    if missing:
        raise ValueError(f"{name} missing v0.32.9 prohibited surfaces: {sorted(missing)}")


def _validate_level_not_d4_d9(level: str | None) -> None:
    if level is None:
        return
    _require_non_blank("max_grantable_level", level)
    normalized = level.strip().upper()
    if any(normalized.startswith(disallowed) for disallowed in DEFAULT_FUTURE_TRACK_LEVELS):
        raise ValueError("D4-D9 must remain future-track and cannot be max grantable in v0.32.9")


def _validate_future_track_levels(values: list[str]) -> None:
    _validate_string_list("future_track_levels", values)
    missing = set(DEFAULT_FUTURE_TRACK_LEVELS) - set(values)
    if missing:
        raise ValueError(f"future_track_levels must include D4-D9: {sorted(missing)}")


RUNTIME_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_external_harness_execution",
    "ready_for_reference_code_execution",
    "ready_for_live_scan",
    "ready_for_read_only_tool_execution",
    "ready_for_runtime_adapter_loading",
    "ready_for_candidate_activation",
    "ready_for_internalization",
    "ready_for_external_control",
    "ready_for_authority_grant",
    "ready_for_provider_invocation",
    "ready_for_network_access",
    "ready_for_credential_access",
    "ready_for_command_execution",
    "ready_for_browser_runtime_control",
    "ready_for_rpa_runtime_control",
    "ready_for_gateway_control",
    "ready_for_packet_send",
    "ready_for_plugin_loading",
    "ready_for_tool_registration",
    "ready_for_tool_invocation",
    "ready_for_mission_installation",
    "ready_for_mission_execution",
    "ready_for_registry_mutation",
    "ready_for_memory_mutation",
    "ready_for_ocel_emission",
    "ready_for_runtime_trace_persistence",
    "ready_for_ui_runtime",
)


@dataclass(frozen=True)
class ExternalPipelineReleaseFlagSet:
    flag_set_id: str
    version: str = V0329_VERSION
    external_harness_observation_digestion_pipeline_ready: bool = True
    ready_for_v033_internal_general_agent_runtime_mvp: bool = False
    ready_for_execution: bool = False
    ready_for_external_harness_execution: bool = False
    ready_for_reference_code_execution: bool = False
    ready_for_live_scan: bool = False
    ready_for_read_only_tool_execution: bool = False
    ready_for_runtime_adapter_loading: bool = False
    ready_for_candidate_activation: bool = False
    ready_for_internalization: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    ready_for_browser_runtime_control: bool = False
    ready_for_rpa_runtime_control: bool = False
    ready_for_gateway_control: bool = False
    ready_for_packet_send: bool = False
    ready_for_plugin_loading: bool = False
    ready_for_tool_registration: bool = False
    ready_for_tool_invocation: bool = False
    ready_for_mission_installation: bool = False
    ready_for_mission_execution: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_ocel_emission: bool = False
    ready_for_runtime_trace_persistence: bool = False
    ready_for_ui_runtime: bool = False
    production_certified: bool = False
    live_adapter_certified: bool = False
    max_grantable_level: str | None = None
    future_track_levels: list[str] = field(default_factory=lambda: list(DEFAULT_FUTURE_TRACK_LEVELS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version_includes_v0329(self.version)
        _validate_false(self, RUNTIME_FLAG_NAMES)
        _validate_false(self, ("production_certified", "live_adapter_certified"))
        _validate_level_not_d4_d9(self.max_grantable_level)
        _validate_future_track_levels(self.future_track_levels)
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "production_release", "live_adapter"}):
            raise ValueError("ExternalPipelineReleaseFlagSet is not runtime enablement")


@dataclass(frozen=True)
class ExternalHarnessPipelineSnapshot:
    snapshot_id: str
    version: str
    release_name: str
    included_versions: list[str]
    included_artifact_groups: list[str]
    release_flags: ExternalPipelineReleaseFlagSet
    consolidation_status: ExternalPipelineConsolidationStatus | str
    readiness_level: ExternalPipelineReadinessLevel | str
    summary: str
    evidence_refs: list[str] = field(default_factory=list)
    known_gaps: list[str] = field(default_factory=list)
    known_risks: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("snapshot_id", self.snapshot_id)
        _validate_version_includes_v0329(self.version)
        _require_non_blank("release_name", self.release_name)
        _validate_required_versions("included_versions", self.included_versions)
        _validate_string_list("included_artifact_groups", self.included_artifact_groups)
        if not isinstance(self.release_flags, ExternalPipelineReleaseFlagSet):
            raise TypeError("release_flags must be ExternalPipelineReleaseFlagSet")
        if not external_pipeline_release_flags_preserve_runtime_false(self.release_flags):
            raise ValueError("release_flags must preserve no-runtime readiness")
        ExternalPipelineConsolidationStatus(self.consolidation_status)
        ExternalPipelineReadinessLevel(self.readiness_level)
        _require_non_blank("summary", self.summary)
        for name in ("evidence_refs", "known_gaps", "known_risks", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "execution_readiness"}):
            raise ValueError("ExternalHarnessPipelineSnapshot is not runtime enablement")

    @property
    def runtime_enablement(self) -> bool:
        return False


@dataclass(frozen=True)
class _CoverageBase:
    coverage_id: str
    version: str = V0329_VERSION
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
        _validate_version_includes_v0329(self.version)
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
            raise ValueError("coverage_complete cannot be true with blocking_gaps")
        if _metadata_flag_true(self.metadata, {"certification", "runtime_readiness"}):
            raise ValueError("coverage is not certification or runtime readiness")

    @property
    def certification(self) -> bool:
        return False

    @property
    def runtime_readiness(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalHarnessProfileCoverage(_CoverageBase):
    pass


@dataclass(frozen=True)
class ReferenceCorpusCoverage(_CoverageBase):
    pass


@dataclass(frozen=True)
class OpenCodeObservationCoverage(_CoverageBase):
    pass


@dataclass(frozen=True)
class OpenClawObservationCoverage(_CoverageBase):
    pass


@dataclass(frozen=True)
class HermesObservationCoverage(_CoverageBase):
    pass


@dataclass(frozen=True)
class ManifestExtractionCoverage(_CoverageBase):
    pass


@dataclass(frozen=True)
class RiskClassificationCoverage(_CoverageBase):
    pass


@dataclass(frozen=True)
class DigestionCandidateCoverage(_CoverageBase):
    pass


@dataclass(frozen=True)
class InternalCandidateEmissionCoverage(_CoverageBase):
    pass


@dataclass(frozen=True)
class DominionCandidateEmissionCoverage(_CoverageBase):
    pass


@dataclass(frozen=True)
class ExternalPipelineGapRegister:
    gap_register_id: str
    version: str = V0329_VERSION
    blocking_gaps: list[str] = field(default_factory=list)
    non_blocking_gaps: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=lambda: ["runtime execution", "read-only tool execution", "runtime adapter loading"])
    recommended_v033_items: list[str] = field(default_factory=list)
    recommended_later_items: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("gap_register_id", self.gap_register_id)
        _validate_version_includes_v0329(self.version)
        for name in ("blocking_gaps", "non_blocking_gaps", "future_track_items", "recommended_v033_items", "recommended_later_items", "evidence_refs"):
            _validate_string_list(name, getattr(self, name))

    @property
    def blocks_handoff(self) -> bool:
        return bool(self.blocking_gaps)


@dataclass(frozen=True)
class ExternalPipelineRiskRegister:
    risk_register_id: str
    version: str = V0329_VERSION
    known_risks: list[str] = field(default_factory=list)
    high_risk_surfaces: list[str] = field(default_factory=list)
    prohibited_runtime_surfaces: list[str] = field(default_factory=lambda: list(DEFAULT_CONSOLIDATION_PROHIBITED_RUNTIME_SURFACES))
    mitigations: list[str] = field(default_factory=list)
    unresolved_risks: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_register_id", self.risk_register_id)
        _validate_version_includes_v0329(self.version)
        for name in ("known_risks", "high_risk_surfaces", "mitigations", "unresolved_risks", "evidence_refs"):
            _validate_string_list(name, getattr(self, name))
        _validate_prohibited_surfaces("prohibited_runtime_surfaces", self.prohibited_runtime_surfaces)
        if _metadata_flag_true(self.metadata, {"proof_of_exploitability", "permission"}):
            raise ValueError("ExternalPipelineRiskRegister is not proof and mitigations are not permissions")

    @property
    def proof_of_exploitability(self) -> bool:
        return False

    @property
    def mitigation_permission(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalPipelineReleaseManifest:
    release_manifest_id: str
    version: str
    release_name: str
    snapshot_id: str
    included_versions: list[str]
    included_modules: list[str]
    included_docs: list[str]
    included_tests: list[str]
    optional_integration_tests: list[str]
    release_flags: ExternalPipelineReleaseFlagSet
    focused_test_command: str
    full_track_test_command: str
    known_gaps: list[str] = field(default_factory=list)
    known_risks: list[str] = field(default_factory=list)
    next_handoff_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("release_manifest_id", self.release_manifest_id)
        _validate_version_includes_v0329(self.version)
        _require_non_blank("release_name", self.release_name)
        _require_non_blank("snapshot_id", self.snapshot_id)
        _validate_required_versions("included_versions", self.included_versions)
        for name in ("included_modules", "included_docs", "included_tests", "optional_integration_tests", "known_gaps", "known_risks"):
            _validate_string_list(name, getattr(self, name))
        if not isinstance(self.release_flags, ExternalPipelineReleaseFlagSet):
            raise TypeError("release_flags must be ExternalPipelineReleaseFlagSet")
        if not external_pipeline_release_flags_preserve_runtime_false(self.release_flags):
            raise ValueError("release_flags must preserve no-runtime readiness")
        _require_non_blank("focused_test_command", self.focused_test_command)
        _require_non_blank("full_track_test_command", self.full_track_test_command)
        for item in self.optional_integration_tests:
            if "disabled-by-default" not in item and "disabled_by_default" not in item:
                raise ValueError("optional integration tests must be represented as disabled-by-default")
        if _metadata_flag_true(self.metadata, {"production_release", "runtime_readiness"}):
            raise ValueError("ExternalPipelineReleaseManifest is not production release")

    @property
    def production_release(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalPipelineConsolidationAuditTrail:
    audit_trail_id: str
    version: str = V0329_VERSION
    reviewed_artifact_refs: list[str] = field(default_factory=list)
    reviewed_test_refs: list[str] = field(default_factory=list)
    reviewed_doc_refs: list[str] = field(default_factory=list)
    boundary_checks: list[str] = field(default_factory=list)
    negative_runtime_checks: list[str] = field(default_factory=list)
    no_execution_confirmed: bool = True
    no_external_harness_execution_confirmed: bool = True
    no_reference_code_execution_confirmed: bool = True
    no_live_scan_confirmed: bool = True
    no_source_ref_fetch_confirmed: bool = True
    no_read_only_tool_execution_confirmed: bool = True
    no_runtime_adapter_loading_confirmed: bool = True
    no_provider_invocation_confirmed: bool = True
    no_network_access_confirmed: bool = True
    no_credential_access_confirmed: bool = True
    no_command_execution_confirmed: bool = True
    no_gateway_control_confirmed: bool = True
    no_packet_send_confirmed: bool = True
    no_registry_mutation_confirmed: bool = True
    no_memory_mutation_confirmed: bool = True
    no_ocel_emission_confirmed: bool = True
    no_ui_runtime_confirmed: bool = True
    no_external_control_confirmed: bool = True
    no_authority_grant_confirmed: bool = True
    no_d4_d9_grant_confirmed: bool = True
    runtime_readiness_flags_false_confirmed: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("audit_trail_id", self.audit_trail_id)
        _validate_version_includes_v0329(self.version)
        for name in ("reviewed_artifact_refs", "reviewed_test_refs", "reviewed_doc_refs", "boundary_checks", "negative_runtime_checks", "evidence_refs"):
            _validate_string_list(name, getattr(self, name))
        for name in self.__dataclass_fields__:
            if name.endswith("_confirmed") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True for successful v0.32.9 consolidation")
        if _metadata_flag_true(self.metadata, {"runtime_audit_execution"}):
            raise ValueError("ExternalPipelineConsolidationAuditTrail is metadata, not runtime audit execution")


@dataclass(frozen=True)
class V033HandoffPacket:
    handoff_id: str
    source_version: str
    target_version_track: str
    source_snapshot_id: str
    release_manifest_id: str | None = None
    recommended_next_track: str = "v0.33 Internal General Agent Runtime MVP"
    recommended_next_release: str = "v0.33.0 Internal General Agent Runtime MVP"
    v033_focus_items: list[str] = field(default_factory=lambda: list(DEFAULT_V033_FOCUS_ITEMS))
    profile_runtime_handoff_items: list[str] = field(default_factory=list)
    prompt_assembly_handoff_items: list[str] = field(default_factory=list)
    session_runtime_handoff_items: list[str] = field(default_factory=list)
    read_only_tool_registry_handoff_items: list[str] = field(default_factory=list)
    safe_workspace_inspection_handoff_items: list[str] = field(default_factory=list)
    agent_step_runner_handoff_items: list[str] = field(default_factory=list)
    runtime_ocel_trace_handoff_items: list[str] = field(default_factory=list)
    cli_surface_handoff_items: list[str] = field(default_factory=list)
    reusable_profile_refs: list[str] = field(default_factory=list)
    reusable_reference_corpus_refs: list[str] = field(default_factory=list)
    reusable_manifest_refs: list[str] = field(default_factory=list)
    reusable_risk_classification_refs: list[str] = field(default_factory=list)
    reusable_digestion_candidate_refs: list[str] = field(default_factory=list)
    reusable_internal_candidate_refs: list[str] = field(default_factory=list)
    reusable_dominion_candidate_refs: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_CONSOLIDATION_PROHIBITED_RUNTIME_SURFACES))
    future_track_items: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    readiness_level: ExternalPipelineReadinessLevel | str = ExternalPipelineReadinessLevel.PIPELINE_FOUNDATION_READY
    ready_for_v033: bool = False
    ready_for_execution: bool = False
    ready_for_read_only_tool_execution: bool = False
    ready_for_runtime_adapter_loading: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("handoff_id", self.handoff_id)
        _validate_version_includes_v0329(self.source_version)
        _require_non_blank("target_version_track", self.target_version_track)
        if "v0.33" not in self.target_version_track:
            raise ValueError("target_version_track must refer to v0.33")
        _require_non_blank("source_snapshot_id", self.source_snapshot_id)
        _require_non_blank("recommended_next_track", self.recommended_next_track)
        _require_non_blank("recommended_next_release", self.recommended_next_release)
        for name in (
            "v033_focus_items",
            "profile_runtime_handoff_items",
            "prompt_assembly_handoff_items",
            "session_runtime_handoff_items",
            "read_only_tool_registry_handoff_items",
            "safe_workspace_inspection_handoff_items",
            "agent_step_runner_handoff_items",
            "runtime_ocel_trace_handoff_items",
            "cli_surface_handoff_items",
            "reusable_profile_refs",
            "reusable_reference_corpus_refs",
            "reusable_manifest_refs",
            "reusable_risk_classification_refs",
            "reusable_digestion_candidate_refs",
            "reusable_internal_candidate_refs",
            "reusable_dominion_candidate_refs",
            "future_track_items",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        if not set(DEFAULT_V033_FOCUS_ITEMS).issubset(set(self.v033_focus_items)):
            raise ValueError("v033_focus_items must include the v0.33 roadmap focus items")
        _validate_prohibited_surfaces("prohibited_until_later_gate", self.prohibited_until_later_gate)
        level = ExternalPipelineReadinessLevel(self.readiness_level)
        _validate_false(self, ("ready_for_execution", "ready_for_read_only_tool_execution", "ready_for_runtime_adapter_loading"))
        if self.ready_for_v033 and level not in {
            ExternalPipelineReadinessLevel.HANDOFF_READY_FOR_V033,
            ExternalPipelineReadinessLevel.PIPELINE_FOUNDATION_READY,
        }:
            raise ValueError("ready_for_v033 requires v0.33 handoff or pipeline foundation readiness")
        if self.ready_for_v033 and self.metadata.get("blocking_gaps"):
            raise ValueError("ready_for_v033 is not allowed with blocking gaps")
        if _metadata_flag_true(self.metadata, {"implementation", "runtime_enablement"}):
            raise ValueError("V033HandoffPacket is not implementation")


@dataclass(frozen=True)
class V032ConsolidationReport:
    report_id: str
    version: str
    release_name: str
    snapshot_id: str
    release_manifest_id: str
    handoff_id: str | None = None
    consolidation_status: ExternalPipelineConsolidationStatus | str = ExternalPipelineConsolidationStatus.CONSOLIDATED_WITH_GAPS
    readiness_level: ExternalPipelineReadinessLevel | str = ExternalPipelineReadinessLevel.PIPELINE_FOUNDATION_READY
    summary: str = "v0.32.x is consolidated as a design-stage external harness observation and digestion pipeline."
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    runtime_not_ready_items: list[str] = field(default_factory=list)
    v033_handoff_summary: str = "Ready for v0.33 design-stage handoff only."
    ready_for_v033: bool = False
    ready_for_execution: bool = False
    ready_for_external_harness_execution: bool = False
    ready_for_reference_code_execution: bool = False
    ready_for_live_scan: bool = False
    ready_for_read_only_tool_execution: bool = False
    ready_for_runtime_adapter_loading: bool = False
    ready_for_ocel_emission: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0329(self.version)
        _require_non_blank("release_name", self.release_name)
        _require_non_blank("snapshot_id", self.snapshot_id)
        _require_non_blank("release_manifest_id", self.release_manifest_id)
        ExternalPipelineConsolidationStatus(self.consolidation_status)
        ExternalPipelineReadinessLevel(self.readiness_level)
        _require_non_blank("summary", self.summary)
        for name in ("completed_items", "blocked_items", "future_track_items", "runtime_not_ready_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _require_non_blank("v033_handoff_summary", self.v033_handoff_summary)
        _validate_false(
            self,
            (
                "ready_for_execution",
                "ready_for_external_harness_execution",
                "ready_for_reference_code_execution",
                "ready_for_live_scan",
                "ready_for_read_only_tool_execution",
                "ready_for_runtime_adapter_loading",
                "ready_for_ocel_emission",
                "ready_for_ui_runtime",
                "ready_for_external_control",
                "ready_for_authority_grant",
            ),
        )
        if self.ready_for_v033 and self.blocked_items:
            raise ValueError("ready_for_v033 is not allowed with blocking gaps")
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "production_certification"}):
            raise ValueError("V032ConsolidationReport is not runtime enablement or production certification")

    @property
    def runtime_enablement(self) -> bool:
        return False

    @property
    def production_certification(self) -> bool:
        return False


def build_v0329_release_flags(flag_set_id: str = "v0329_release_flags", **kwargs: Any) -> ExternalPipelineReleaseFlagSet:
    return ExternalPipelineReleaseFlagSet(flag_set_id=flag_set_id, version=V0329_VERSION, **kwargs)


def build_external_harness_pipeline_snapshot(snapshot_id: str, release_flags: ExternalPipelineReleaseFlagSet, **kwargs: Any) -> ExternalHarnessPipelineSnapshot:
    return ExternalHarnessPipelineSnapshot(
        snapshot_id=snapshot_id,
        version=V0329_VERSION,
        release_name=kwargs.pop("release_name", V0329_FOUNDATION_RELEASE_NAME),
        included_versions=kwargs.pop("included_versions", list(REQUIRED_V032_INCLUDED_VERSIONS)),
        included_artifact_groups=kwargs.pop("included_artifact_groups", []),
        release_flags=release_flags,
        consolidation_status=kwargs.pop("consolidation_status", ExternalPipelineConsolidationStatus.CONSOLIDATED_WITH_GAPS),
        readiness_level=kwargs.pop("readiness_level", ExternalPipelineReadinessLevel.PIPELINE_FOUNDATION_READY),
        summary=kwargs.pop("summary", "External harness observation and digestion pipeline v1 snapshot."),
        **kwargs,
    )


def build_external_pipeline_coverage_matrix(coverage_id: str, coverage_cls: type[_CoverageBase] = ExternalHarnessProfileCoverage, **kwargs: Any) -> _CoverageBase:
    return coverage_cls(coverage_id=coverage_id, version=V0329_VERSION, **kwargs)


def build_external_pipeline_gap_register(gap_register_id: str = "v0329_gap_register", **kwargs: Any) -> ExternalPipelineGapRegister:
    return ExternalPipelineGapRegister(gap_register_id=gap_register_id, version=V0329_VERSION, **kwargs)


def build_external_pipeline_risk_register(risk_register_id: str = "v0329_risk_register", **kwargs: Any) -> ExternalPipelineRiskRegister:
    return ExternalPipelineRiskRegister(risk_register_id=risk_register_id, version=V0329_VERSION, **kwargs)


def build_external_pipeline_release_manifest(release_manifest_id: str, release_flags: ExternalPipelineReleaseFlagSet, **kwargs: Any) -> ExternalPipelineReleaseManifest:
    return ExternalPipelineReleaseManifest(
        release_manifest_id=release_manifest_id,
        version=V0329_VERSION,
        release_name=kwargs.pop("release_name", V0329_FOUNDATION_RELEASE_NAME),
        snapshot_id=kwargs.pop("snapshot_id", "v0329_pipeline_snapshot"),
        included_versions=kwargs.pop("included_versions", list(REQUIRED_V032_INCLUDED_VERSIONS)),
        included_modules=kwargs.pop("included_modules", []),
        included_docs=kwargs.pop("included_docs", []),
        included_tests=kwargs.pop("included_tests", []),
        optional_integration_tests=kwargs.pop("optional_integration_tests", []),
        release_flags=release_flags,
        focused_test_command=kwargs.pop("focused_test_command", "py -m pytest tests/test_v0328_external_dominion_candidate_emitter.py tests/test_v0329_external_observation_digestion_consolidation.py"),
        full_track_test_command=kwargs.pop("full_track_test_command", "py -m pytest tests/test_v0320_external_harness_profile_contract.py ... tests/test_v0329_external_observation_digestion_consolidation.py"),
        **kwargs,
    )


def build_external_pipeline_consolidation_audit_trail(audit_trail_id: str = "v0329_consolidation_audit_trail", **kwargs: Any) -> ExternalPipelineConsolidationAuditTrail:
    return ExternalPipelineConsolidationAuditTrail(audit_trail_id=audit_trail_id, version=V0329_VERSION, **kwargs)


def build_v033_handoff_packet(handoff_id: str, source_snapshot_id: str, **kwargs: Any) -> V033HandoffPacket:
    return V033HandoffPacket(
        handoff_id=handoff_id,
        source_version=V0329_VERSION,
        target_version_track=kwargs.pop("target_version_track", "v0.33 Internal General Agent Runtime MVP"),
        source_snapshot_id=source_snapshot_id,
        **kwargs,
    )


def build_v032_consolidation_report(report_id: str, snapshot_id: str, release_manifest_id: str, **kwargs: Any) -> V032ConsolidationReport:
    return V032ConsolidationReport(
        report_id=report_id,
        version=V0329_VERSION,
        release_name=kwargs.pop("release_name", V0329_FOUNDATION_RELEASE_NAME),
        snapshot_id=snapshot_id,
        release_manifest_id=release_manifest_id,
        **kwargs,
    )


def external_pipeline_release_flags_preserve_runtime_false(flags: ExternalPipelineReleaseFlagSet) -> bool:
    return (
        all(getattr(flags, name) is False for name in RUNTIME_FLAG_NAMES)
        and flags.production_certified is False
        and flags.live_adapter_certified is False
    )


def external_pipeline_snapshot_is_not_runtime_ready(snapshot: ExternalHarnessPipelineSnapshot) -> bool:
    return external_pipeline_release_flags_preserve_runtime_false(snapshot.release_flags) and snapshot.runtime_enablement is False


def external_pipeline_coverage_is_not_certification(coverage: _CoverageBase) -> bool:
    return coverage.certification is False and coverage.runtime_readiness is False


def v033_handoff_packet_is_design_stage_only(packet: V033HandoffPacket) -> bool:
    return (
        packet.ready_for_execution is False
        and packet.ready_for_read_only_tool_execution is False
        and packet.ready_for_runtime_adapter_loading is False
    )


def v032_consolidation_report_is_not_runtime_ready(report: V032ConsolidationReport) -> bool:
    return (
        report.ready_for_execution is False
        and report.ready_for_external_harness_execution is False
        and report.ready_for_reference_code_execution is False
        and report.ready_for_live_scan is False
        and report.ready_for_read_only_tool_execution is False
        and report.ready_for_runtime_adapter_loading is False
        and report.ready_for_ocel_emission is False
        and report.ready_for_ui_runtime is False
        and report.ready_for_external_control is False
        and report.ready_for_authority_grant is False
        and report.runtime_enablement is False
        and report.production_certification is False
    )
