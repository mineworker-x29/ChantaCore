from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from chanta_core.external_dominion.dominion_levels import DominionLevel, FUTURE_TRACK_LEVELS, normalize_dominion_level
from chanta_core.internal_triad.boundaries import _require_non_blank, _validate_string_list
from chanta_core.internal_triad.skill_kinds import V0310_TRACK


V0319_VERSION = "v0.31.9"
V0319_RELEASE_NAME = "v0.31.9 Internal Triad Skill Foundation Consolidation"
V0319_FOUNDATION_RELEASE_NAME = "Internal Triad Skill Foundation v1"
V0319_TRACK = V0310_TRACK

V0319_INCLUDED_VERSIONS = [
    "v0.31.0",
    "v0.31.1",
    "v0.31.2",
    "v0.31.3",
    "v0.31.4",
    "v0.31.5",
    "v0.31.6",
    "v0.31.7",
    "v0.31.8",
]

V0319_PROHIBITED_RUNTIME_SURFACES = [
    "external_scan",
    "source_ref_fetch",
    "read_only_tool_execution",
    "skill_activation",
    "registry_mutation",
    "memory_mutation",
    "ocel_emission",
    "runtime_trace_persistence",
    "ui_runtime",
    "action_execution",
    "provider_invocation",
    "network",
    "credential",
    "command",
    "browser",
    "rpa",
    "gateway",
    "packet_send",
    "rollback_execution",
    "retry_execution",
]

V0319_PROHIBITED_UNTIL_LATER_GATE = [
    "runtime_execution",
    "external_scan",
    "provider_invocation",
    "network",
    "credential",
    "command",
    "browser",
    "rpa",
    "gateway",
    "packet_send",
    "registry_mutation",
    "memory_mutation",
    "ocel_emission",
    "ui_runtime",
    "action_execution",
    "rollback",
    "retry",
]


class InternalTriadConsolidationStatus(StrEnum):
    UNKNOWN = "unknown"
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    CONSOLIDATED = "consolidated"
    CONSOLIDATED_WITH_GAPS = "consolidated_with_gaps"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class InternalTriadReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    CONTRACT_READY = "contract_ready"
    FOUNDATION_READY = "foundation_ready"
    HANDOFF_READY_FOR_V032 = "handoff_ready_for_v032"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


def _metadata_flag_true(metadata: dict[str, Any], names: set[str]) -> bool:
    return isinstance(metadata, dict) and any(metadata.get(name) is True for name in names)


def _validate_version_includes_v0319(version: str) -> None:
    _require_non_blank("version", version)
    if V0319_VERSION not in version:
        raise ValueError("version must include v0.31.9")


def _validate_included_versions(included_versions: list[str]) -> None:
    _validate_string_list("included_versions", included_versions)
    missing = set(V0319_INCLUDED_VERSIONS) - set(included_versions)
    if missing:
        raise ValueError(f"included_versions missing v0.31.x releases: {sorted(missing)}")


def _validate_object_list(name: str, values: list[Any], expected_type: type) -> None:
    if not isinstance(values, list) or not all(isinstance(item, expected_type) for item in values):
        raise TypeError(f"{name} must be list[{expected_type.__name__}]")


def normalize_internal_triad_consolidation_status(value: InternalTriadConsolidationStatus | str) -> InternalTriadConsolidationStatus:
    if isinstance(value, InternalTriadConsolidationStatus):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("internal triad consolidation status must not be blank")
        return InternalTriadConsolidationStatus(stripped)
    raise TypeError(f"unsupported internal triad consolidation status: {value!r}")


def normalize_internal_triad_readiness_level(value: InternalTriadReadinessLevel | str) -> InternalTriadReadinessLevel:
    if isinstance(value, InternalTriadReadinessLevel):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("internal triad readiness level must not be blank")
        return InternalTriadReadinessLevel(stripped)
    raise TypeError(f"unsupported internal triad readiness level: {value!r}")


@dataclass(frozen=True)
class InternalTriadReleaseFlagSet:
    flag_set_id: str
    version: str
    internal_triad_skill_foundation_ready: bool
    ready_for_v032_external_harness_observation_pipeline: bool
    ready_for_execution: bool = False
    ready_for_skill_activation: bool = False
    ready_for_external_scan: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    ready_for_read_only_tool_execution: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_ocel_emission: bool = False
    ready_for_runtime_trace_persistence: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_action_execution: bool = False
    ready_for_approval_execution: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    ready_for_rpa_runtime_control: bool = False
    ready_for_browser_runtime_control: bool = False
    ready_for_gateway_control: bool = False
    production_certified: bool = False
    live_adapter_certified: bool = False
    max_grantable_level: DominionLevel | str | None = DominionLevel.D3_SIMULATE
    future_track_levels: list[DominionLevel | str] = field(default_factory=lambda: list(FUTURE_TRACK_LEVELS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version_includes_v0319(self.version)
        false_flags = [
            "ready_for_execution",
            "ready_for_skill_activation",
            "ready_for_external_scan",
            "ready_for_external_control",
            "ready_for_authority_grant",
            "ready_for_read_only_tool_execution",
            "ready_for_registry_mutation",
            "ready_for_memory_mutation",
            "ready_for_ocel_emission",
            "ready_for_runtime_trace_persistence",
            "ready_for_ui_runtime",
            "ready_for_action_execution",
            "ready_for_approval_execution",
            "ready_for_provider_invocation",
            "ready_for_network_access",
            "ready_for_credential_access",
            "ready_for_command_execution",
            "ready_for_rpa_runtime_control",
            "ready_for_browser_runtime_control",
            "ready_for_gateway_control",
            "production_certified",
            "live_adapter_certified",
        ]
        for name in false_flags:
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False in v0.31.9")
        if self.max_grantable_level is not None and normalize_dominion_level(self.max_grantable_level) > DominionLevel.D3_SIMULATE:
            raise ValueError("max_grantable_level must be None or <= D3_SIMULATE in v0.31.9")
        if not isinstance(self.future_track_levels, list):
            raise TypeError("future_track_levels must be list[DominionLevel | str]")
        resolved_future_levels = {normalize_dominion_level(level) for level in self.future_track_levels}
        missing = set(FUTURE_TRACK_LEVELS) - resolved_future_levels
        if missing:
            raise ValueError(f"future_track_levels missing D4-D9 levels: {sorted(level.name for level in missing)}")
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "production_release", "live_adapter_ready"}):
            raise ValueError("InternalTriadReleaseFlagSet must not imply runtime enablement")

    @property
    def runtime_ready(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalTriadFoundationSnapshot:
    snapshot_id: str
    version: str
    release_name: str
    included_versions: list[str]
    included_artifact_groups: list[str]
    release_flags: InternalTriadReleaseFlagSet
    consolidation_status: InternalTriadConsolidationStatus | str
    readiness_level: InternalTriadReadinessLevel | str
    summary: str
    evidence_refs: list[str] = field(default_factory=list)
    known_gaps: list[str] = field(default_factory=list)
    known_risks: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("snapshot_id", self.snapshot_id)
        _validate_version_includes_v0319(self.version)
        _require_non_blank("release_name", self.release_name)
        _validate_included_versions(self.included_versions)
        _validate_string_list("included_artifact_groups", self.included_artifact_groups)
        if not isinstance(self.release_flags, InternalTriadReleaseFlagSet):
            raise TypeError("release_flags must be InternalTriadReleaseFlagSet")
        if not internal_triad_release_flags_preserve_runtime_false(self.release_flags):
            raise ValueError("release_flags must preserve no-runtime readiness")
        normalize_internal_triad_consolidation_status(self.consolidation_status)
        normalize_internal_triad_readiness_level(self.readiness_level)
        _require_non_blank("summary", self.summary)
        for name in ("evidence_refs", "known_gaps", "known_risks", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "execution_readiness"}):
            raise ValueError("InternalTriadFoundationSnapshot must not imply runtime enablement")

    @property
    def runtime_enablement(self) -> bool:
        return False


@dataclass(frozen=True)
class _TriadCoverageBase:
    coverage_id: str
    covered_artifact_refs: list[str] = field(default_factory=list)
    missing_artifact_refs: list[str] = field(default_factory=list)
    coverage_notes: list[str] = field(default_factory=list)
    coverage_complete: bool = False
    blocking_gaps: list[str] = field(default_factory=list)
    non_blocking_gaps: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("coverage_id", self.coverage_id)
        for name in (
            "covered_artifact_refs",
            "missing_artifact_refs",
            "coverage_notes",
            "blocking_gaps",
            "non_blocking_gaps",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        if self.coverage_complete and self.blocking_gaps:
            raise ValueError("coverage_complete cannot be true when blocking_gaps exist")
        if _metadata_flag_true(self.metadata, {"runtime_readiness", "certification"}):
            raise ValueError("coverage matrix must not imply runtime readiness or certification")

    @property
    def runtime_readiness(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadSkillContractCoverage(_TriadCoverageBase):
    pass


@dataclass(frozen=True)
class ObservationSkillCoverage(_TriadCoverageBase):
    pass


@dataclass(frozen=True)
class ObservationReportCoverage(_TriadCoverageBase):
    pass


@dataclass(frozen=True)
class DigestionSkillCoverage(_TriadCoverageBase):
    pass


@dataclass(frozen=True)
class InternalizationCoverage(_TriadCoverageBase):
    pass


@dataclass(frozen=True)
class DominionSkillCoverage(_TriadCoverageBase):
    pass


@dataclass(frozen=True)
class DominionTargetDecisionCoverage(_TriadCoverageBase):
    pass


@dataclass(frozen=True)
class TriadOCELTraceCoverageSummary(_TriadCoverageBase):
    pass


@dataclass(frozen=True)
class TriadWorkbenchCoverage(_TriadCoverageBase):
    pass


@dataclass(frozen=True)
class InternalTriadGapRegister:
    gap_register_id: str
    version: str
    blocking_gaps: list[str] = field(default_factory=list)
    non_blocking_gaps: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    recommended_v032_items: list[str] = field(default_factory=list)
    recommended_later_items: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("gap_register_id", self.gap_register_id)
        _validate_version_includes_v0319(self.version)
        for name in (
            "blocking_gaps",
            "non_blocking_gaps",
            "future_track_items",
            "recommended_v032_items",
            "recommended_later_items",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        if _metadata_flag_true(self.metadata, {"failure", "runtime_enablement"}):
            raise ValueError("InternalTriadGapRegister must not imply failure or runtime enablement")

    @property
    def blocks_v032(self) -> bool:
        return bool(self.blocking_gaps)


@dataclass(frozen=True)
class InternalTriadRiskRegister:
    risk_register_id: str
    version: str
    known_risks: list[str] = field(default_factory=list)
    high_risk_surfaces: list[str] = field(default_factory=list)
    prohibited_runtime_surfaces: list[str] = field(default_factory=lambda: list(V0319_PROHIBITED_RUNTIME_SURFACES))
    mitigations: list[str] = field(default_factory=list)
    unresolved_risks: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_register_id", self.risk_register_id)
        _validate_version_includes_v0319(self.version)
        for name in (
            "known_risks",
            "high_risk_surfaces",
            "prohibited_runtime_surfaces",
            "mitigations",
            "unresolved_risks",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        missing = set(V0319_PROHIBITED_RUNTIME_SURFACES) - set(self.prohibited_runtime_surfaces)
        if missing:
            raise ValueError(f"prohibited_runtime_surfaces missing v0.31.9 prohibitions: {sorted(missing)}")
        if _metadata_flag_true(self.metadata, {"exploitability_proof", "mitigation_permission"}):
            raise ValueError("InternalTriadRiskRegister must not imply exploitability proof or permission")

    @property
    def proves_exploitability(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalTriadV032HandoffPacket:
    handoff_id: str
    source_version: str
    target_version_track: str
    source_snapshot_id: str
    release_manifest_id: str | None
    recommended_next_track: str
    recommended_next_release: str
    external_harness_pipeline_focus: list[str]
    observation_profile_handoff_items: list[str] = field(default_factory=list)
    digestion_pipeline_handoff_items: list[str] = field(default_factory=list)
    dominion_pipeline_handoff_items: list[str] = field(default_factory=list)
    reusable_contract_refs: list[str] = field(default_factory=list)
    reusable_observation_refs: list[str] = field(default_factory=list)
    reusable_capability_map_refs: list[str] = field(default_factory=list)
    reusable_internal_candidate_refs: list[str] = field(default_factory=list)
    reusable_dominion_refs: list[str] = field(default_factory=list)
    reusable_ocel_trace_refs: list[str] = field(default_factory=list)
    reusable_workbench_refs: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(V0319_PROHIBITED_UNTIL_LATER_GATE))
    future_track_items: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    readiness_level: InternalTriadReadinessLevel | str = InternalTriadReadinessLevel.HANDOFF_READY_FOR_V032
    ready_for_v032: bool = True
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("handoff_id", self.handoff_id)
        _validate_version_includes_v0319(self.source_version)
        _require_non_blank("target_version_track", self.target_version_track)
        if "v0.32" not in self.target_version_track:
            raise ValueError("target_version_track must refer to v0.32")
        _require_non_blank("source_snapshot_id", self.source_snapshot_id)
        _require_non_blank("recommended_next_track", self.recommended_next_track)
        _require_non_blank("recommended_next_release", self.recommended_next_release)
        for name in (
            "external_harness_pipeline_focus",
            "observation_profile_handoff_items",
            "digestion_pipeline_handoff_items",
            "dominion_pipeline_handoff_items",
            "reusable_contract_refs",
            "reusable_observation_refs",
            "reusable_capability_map_refs",
            "reusable_internal_candidate_refs",
            "reusable_dominion_refs",
            "reusable_ocel_trace_refs",
            "reusable_workbench_refs",
            "prohibited_until_later_gate",
            "future_track_items",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        if not any("external harness" in item.lower() or "opencode" in item.lower() or "openclaw" in item.lower() or "hermes" in item.lower() for item in self.external_harness_pipeline_focus):
            raise ValueError("external_harness_pipeline_focus must mention external harness observation/digestion focus")
        missing = set(V0319_PROHIBITED_UNTIL_LATER_GATE) - set(self.prohibited_until_later_gate)
        if missing:
            raise ValueError(f"prohibited_until_later_gate missing v0.31.9 prohibitions: {sorted(missing)}")
        readiness = normalize_internal_triad_readiness_level(self.readiness_level)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.9")
        if self.ready_for_v032 and readiness not in {
            InternalTriadReadinessLevel.FOUNDATION_READY,
            InternalTriadReadinessLevel.HANDOFF_READY_FOR_V032,
        }:
            raise ValueError("ready_for_v032 requires foundation or v0.32 handoff readiness")
        if self.ready_for_v032 and _metadata_flag_true(self.metadata, {"blocking_gaps"}):
            raise ValueError("ready_for_v032 requires no blocking gaps")
        if _metadata_flag_true(self.metadata, {"implementation", "external_harness_execution"}):
            raise ValueError("InternalTriadV032HandoffPacket must not imply implementation")

    @property
    def implementation(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalTriadReleaseManifest:
    release_manifest_id: str
    version: str
    release_name: str
    snapshot_id: str
    included_versions: list[str]
    included_docs: list[str]
    included_modules: list[str]
    included_tests: list[str]
    release_flags: InternalTriadReleaseFlagSet
    test_command: str
    known_gaps: list[str] = field(default_factory=list)
    known_risks: list[str] = field(default_factory=list)
    next_handoff_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("release_manifest_id", self.release_manifest_id)
        _validate_version_includes_v0319(self.version)
        _require_non_blank("release_name", self.release_name)
        _require_non_blank("snapshot_id", self.snapshot_id)
        _validate_included_versions(self.included_versions)
        for name in ("included_docs", "included_modules", "included_tests", "known_gaps", "known_risks"):
            _validate_string_list(name, getattr(self, name))
        if not isinstance(self.release_flags, InternalTriadReleaseFlagSet):
            raise TypeError("release_flags must be InternalTriadReleaseFlagSet")
        if not internal_triad_release_flags_preserve_runtime_false(self.release_flags):
            raise ValueError("release_flags must preserve no-runtime readiness")
        _require_non_blank("test_command", self.test_command)
        if _metadata_flag_true(self.metadata, {"production_release", "runtime_readiness"}):
            raise ValueError("InternalTriadReleaseManifest must not imply production release or runtime readiness")

    @property
    def production_release(self) -> bool:
        return False


@dataclass(frozen=True)
class V031ConsolidationAuditTrail:
    audit_trail_id: str
    version: str
    reviewed_artifact_refs: list[str] = field(default_factory=list)
    reviewed_test_refs: list[str] = field(default_factory=list)
    reviewed_doc_refs: list[str] = field(default_factory=list)
    boundary_checks: list[str] = field(default_factory=list)
    negative_runtime_checks: list[str] = field(default_factory=list)
    no_execution_confirmed: bool = True
    no_external_scan_confirmed: bool = True
    no_tool_execution_confirmed: bool = True
    no_registry_mutation_confirmed: bool = True
    no_memory_mutation_confirmed: bool = True
    no_ocel_emission_confirmed: bool = True
    no_ui_runtime_confirmed: bool = True
    runtime_readiness_flags_false_confirmed: bool = True
    d4_d9_future_track_confirmed: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("audit_trail_id", self.audit_trail_id)
        _validate_version_includes_v0319(self.version)
        for name in (
            "reviewed_artifact_refs",
            "reviewed_test_refs",
            "reviewed_doc_refs",
            "boundary_checks",
            "negative_runtime_checks",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        for name in (
            "no_execution_confirmed",
            "no_external_scan_confirmed",
            "no_tool_execution_confirmed",
            "no_registry_mutation_confirmed",
            "no_memory_mutation_confirmed",
            "no_ocel_emission_confirmed",
            "no_ui_runtime_confirmed",
            "runtime_readiness_flags_false_confirmed",
            "d4_d9_future_track_confirmed",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True for v0.31.9 consolidation")
        if _metadata_flag_true(self.metadata, {"runtime_audit_execution"}):
            raise ValueError("V031ConsolidationAuditTrail is metadata, not runtime audit execution")

    @property
    def runtime_audit_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class V031ConsolidationReport:
    report_id: str
    version: str
    release_name: str
    snapshot_id: str
    release_manifest_id: str
    handoff_id: str | None
    consolidation_status: InternalTriadConsolidationStatus | str
    readiness_level: InternalTriadReadinessLevel | str
    summary: str
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    runtime_not_ready_items: list[str] = field(default_factory=list)
    v032_handoff_summary: str = "v0.32 External Harness Observation & Digestion Pipeline handoff only."
    ready_for_v032: bool = True
    ready_for_execution: bool = False
    ready_for_skill_activation: bool = False
    ready_for_external_scan: bool = False
    ready_for_ocel_emission: bool = False
    ready_for_ui_runtime: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0319(self.version)
        _require_non_blank("release_name", self.release_name)
        _require_non_blank("snapshot_id", self.snapshot_id)
        _require_non_blank("release_manifest_id", self.release_manifest_id)
        status = normalize_internal_triad_consolidation_status(self.consolidation_status)
        readiness = normalize_internal_triad_readiness_level(self.readiness_level)
        _require_non_blank("summary", self.summary)
        for name in ("completed_items", "blocked_items", "future_track_items", "runtime_not_ready_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _require_non_blank("v032_handoff_summary", self.v032_handoff_summary)
        for name in (
            "ready_for_execution",
            "ready_for_skill_activation",
            "ready_for_external_scan",
            "ready_for_ocel_emission",
            "ready_for_ui_runtime",
        ):
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False in v0.31.9")
        if self.ready_for_v032 and (self.blocked_items or status is InternalTriadConsolidationStatus.BLOCKED):
            raise ValueError("ready_for_v032 requires no blocking gaps")
        if self.ready_for_v032 and readiness not in {
            InternalTriadReadinessLevel.FOUNDATION_READY,
            InternalTriadReadinessLevel.HANDOFF_READY_FOR_V032,
        }:
            raise ValueError("ready_for_v032 requires foundation or handoff readiness")
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "production_certification"}):
            raise ValueError("V031ConsolidationReport must not imply runtime enablement or production certification")

    @property
    def runtime_enablement(self) -> bool:
        return False


def build_v0319_release_flags(
    internal_triad_skill_foundation_ready: bool = True,
    ready_for_v032_external_harness_observation_pipeline: bool = True,
    metadata: dict[str, Any] | None = None,
) -> InternalTriadReleaseFlagSet:
    return InternalTriadReleaseFlagSet(
        flag_set_id="v0319_release_flags:internal_triad_foundation_v1",
        version=V0319_VERSION,
        internal_triad_skill_foundation_ready=internal_triad_skill_foundation_ready,
        ready_for_v032_external_harness_observation_pipeline=ready_for_v032_external_harness_observation_pipeline,
        ready_for_execution=False,
        ready_for_skill_activation=False,
        ready_for_external_scan=False,
        ready_for_external_control=False,
        ready_for_authority_grant=False,
        ready_for_read_only_tool_execution=False,
        ready_for_registry_mutation=False,
        ready_for_memory_mutation=False,
        ready_for_ocel_emission=False,
        ready_for_runtime_trace_persistence=False,
        ready_for_ui_runtime=False,
        ready_for_action_execution=False,
        ready_for_approval_execution=False,
        ready_for_provider_invocation=False,
        ready_for_network_access=False,
        ready_for_credential_access=False,
        ready_for_command_execution=False,
        ready_for_rpa_runtime_control=False,
        ready_for_browser_runtime_control=False,
        ready_for_gateway_control=False,
        production_certified=False,
        live_adapter_certified=False,
        max_grantable_level=DominionLevel.D3_SIMULATE,
        future_track_levels=list(FUTURE_TRACK_LEVELS),
        metadata=dict(metadata or {}),
    )


def build_internal_triad_foundation_snapshot(
    snapshot_id: str = "internal_triad_foundation_snapshot:v0.31.9",
    release_flags: InternalTriadReleaseFlagSet | None = None,
    known_gaps: list[str] | None = None,
    known_risks: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> InternalTriadFoundationSnapshot:
    return InternalTriadFoundationSnapshot(
        snapshot_id=snapshot_id,
        version=V0319_VERSION,
        release_name=V0319_FOUNDATION_RELEASE_NAME,
        included_versions=list(V0319_INCLUDED_VERSIONS),
        included_artifact_groups=[
            "triad skill contracts",
            "observation foundation and reports",
            "digestion and internalization",
            "dominion governance",
            "OCEL trace contracts",
            "Workbench surface contracts",
        ],
        release_flags=release_flags or build_v0319_release_flags(),
        consolidation_status=InternalTriadConsolidationStatus.CONSOLIDATED_WITH_GAPS,
        readiness_level=InternalTriadReadinessLevel.HANDOFF_READY_FOR_V032,
        summary="v0.31.x is consolidated as Internal Triad Skill Foundation v1 without runtime enablement.",
        evidence_refs=["v0.31.0-v0.31.8 focused tests"],
        known_gaps=list(known_gaps or []),
        known_risks=list(known_risks or []),
        withdrawal_conditions=[
            "runtime readiness flag becomes true",
            "D4-D9 becomes grantable",
            "external scan, read-only tool execution, OCEL emission, or UI runtime is introduced",
        ],
        metadata=dict(metadata or {}),
    )


def build_triad_coverage_matrix(
    coverage_cls: type[_TriadCoverageBase],
    coverage_id: str,
    covered_artifact_refs: list[str] | None = None,
    missing_artifact_refs: list[str] | None = None,
    coverage_notes: list[str] | None = None,
    coverage_complete: bool = True,
    blocking_gaps: list[str] | None = None,
    non_blocking_gaps: list[str] | None = None,
    evidence_refs: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> _TriadCoverageBase:
    if not issubclass(coverage_cls, _TriadCoverageBase):
        raise TypeError("coverage_cls must be a triad coverage class")
    return coverage_cls(
        coverage_id=coverage_id,
        covered_artifact_refs=list(covered_artifact_refs or []),
        missing_artifact_refs=list(missing_artifact_refs or []),
        coverage_notes=list(coverage_notes or []),
        coverage_complete=coverage_complete,
        blocking_gaps=list(blocking_gaps or []),
        non_blocking_gaps=list(non_blocking_gaps or []),
        evidence_refs=list(evidence_refs or []),
        metadata=dict(metadata or {}),
    )


def build_internal_triad_gap_register(
    blocking_gaps: list[str] | None = None,
    non_blocking_gaps: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> InternalTriadGapRegister:
    return InternalTriadGapRegister(
        gap_register_id="internal_triad_gap_register:v0.31.9",
        version=V0319_VERSION,
        blocking_gaps=list(blocking_gaps or []),
        non_blocking_gaps=list(non_blocking_gaps or ["runtime surfaces remain later-gated"]),
        future_track_items=["D4-D9", "runtime execution", "read-only tool execution", "OCEL emission", "UI runtime"],
        recommended_v032_items=["external harness observation profile", "external harness digestion pipeline"],
        recommended_later_items=["runtime execution gates", "provider invocation gates", "UI runtime gates"],
        evidence_refs=["v0.31.9 consolidation review"],
        metadata=dict(metadata or {}),
    )


def build_internal_triad_risk_register(metadata: dict[str, Any] | None = None) -> InternalTriadRiskRegister:
    return InternalTriadRiskRegister(
        risk_register_id="internal_triad_risk_register:v0.31.9",
        version=V0319_VERSION,
        known_risks=["contract artifacts may be mistaken for runtime readiness"],
        high_risk_surfaces=["external harness", "provider", "network", "credential", "command", "browser", "rpa", "gateway"],
        prohibited_runtime_surfaces=list(V0319_PROHIBITED_RUNTIME_SURFACES),
        mitigations=["keep readiness flags false", "preserve D4-D9 future-track", "require later gates"],
        unresolved_risks=["v0.32 external harness pipeline remains design-stage"],
        evidence_refs=["v0.31.0-v0.31.8 boundary tests"],
        metadata=dict(metadata or {}),
    )


def build_v032_handoff_packet(
    snapshot: InternalTriadFoundationSnapshot,
    release_manifest_id: str | None = None,
    gap_register: InternalTriadGapRegister | None = None,
    metadata: dict[str, Any] | None = None,
) -> InternalTriadV032HandoffPacket:
    if not isinstance(snapshot, InternalTriadFoundationSnapshot):
        raise TypeError("snapshot must be InternalTriadFoundationSnapshot")
    resolved_blocking = list(gap_register.blocking_gaps if gap_register is not None else [])
    return InternalTriadV032HandoffPacket(
        handoff_id="internal_triad_v032_handoff_packet:v0.31.9",
        source_version=V0319_VERSION,
        target_version_track="v0.32 External Harness Observation & Digestion Pipeline",
        source_snapshot_id=snapshot.snapshot_id,
        release_manifest_id=release_manifest_id,
        recommended_next_track="External Harness Observation & Digestion Pipeline",
        recommended_next_release="v0.32.0",
        external_harness_pipeline_focus=[
            "generic external harness observation",
            "OpenCode/OpenClaw/Hermes-style observation profile",
            "external harness digestion and dominion signal pipeline",
        ],
        observation_profile_handoff_items=["observation report and capability-map refs"],
        digestion_pipeline_handoff_items=["digestion route and internal candidate refs"],
        dominion_pipeline_handoff_items=["dominion target and decision governance refs"],
        reusable_contract_refs=["v0.31.0 contracts"],
        reusable_observation_refs=["v0.31.1 observation output", "v0.31.2 observation report"],
        reusable_capability_map_refs=["v0.31.2 capability map"],
        reusable_internal_candidate_refs=["v0.31.4 internal candidate set"],
        reusable_dominion_refs=["v0.31.6 dominion target decision set"],
        reusable_ocel_trace_refs=["v0.31.7 trace plan"],
        reusable_workbench_refs=["v0.31.8 workbench snapshot"],
        prohibited_until_later_gate=list(V0319_PROHIBITED_UNTIL_LATER_GATE),
        future_track_items=["D4-D9", "external execution", "read-only tool execution", "OCEL emission", "UI runtime"],
        evidence_refs=list(snapshot.evidence_refs),
        readiness_level=InternalTriadReadinessLevel.HANDOFF_READY_FOR_V032 if not resolved_blocking else InternalTriadReadinessLevel.BLOCKED,
        ready_for_v032=not resolved_blocking,
        ready_for_execution=False,
        metadata={**dict(metadata or {}), **({"blocking_gaps": True} if resolved_blocking else {})},
    )


def build_internal_triad_release_manifest(
    snapshot: InternalTriadFoundationSnapshot,
    next_handoff_id: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> InternalTriadReleaseManifest:
    if not isinstance(snapshot, InternalTriadFoundationSnapshot):
        raise TypeError("snapshot must be InternalTriadFoundationSnapshot")
    return InternalTriadReleaseManifest(
        release_manifest_id="internal_triad_release_manifest:v0.31.9",
        version=V0319_VERSION,
        release_name=V0319_RELEASE_NAME,
        snapshot_id=snapshot.snapshot_id,
        included_versions=list(V0319_INCLUDED_VERSIONS),
        included_docs=[f"docs/versions/v0.31/v{version[1:]}_*.md" for version in V0319_INCLUDED_VERSIONS],
        included_modules=[
            "chanta_core.internal_triad.contracts",
            "chanta_core.internal_triad.observation",
            "chanta_core.internal_triad.observation_reports",
            "chanta_core.internal_triad.digestion",
            "chanta_core.internal_triad.internalization",
            "chanta_core.internal_triad.dominion",
            "chanta_core.internal_triad.dominion_decisions",
            "chanta_core.internal_triad.ocel_trace",
            "chanta_core.internal_triad.workbench",
            "chanta_core.internal_triad.consolidation",
        ],
        included_tests=[f"tests/test_v031{index}_*.py" for index in range(0, 10)],
        release_flags=snapshot.release_flags,
        test_command="py -m pytest tests/test_v0310_internal_triad_skill_contract.py tests/test_v0311_observation_skill_foundation.py tests/test_v0312_observation_report_capability_map.py tests/test_v0313_digestion_skill_foundation.py tests/test_v0314_digestion_candidate_internalization_plan.py tests/test_v0315_dominion_skill_foundation.py tests/test_v0316_dominion_target_decision.py tests/test_v0317_triad_skill_ocel_trace_integration.py tests/test_v0318_triad_skill_workbench_surface.py tests/test_v0319_internal_triad_foundation_consolidation.py",
        known_gaps=list(snapshot.known_gaps),
        known_risks=list(snapshot.known_risks),
        next_handoff_id=next_handoff_id,
        metadata=dict(metadata or {}),
    )


def build_v031_consolidation_audit_trail(metadata: dict[str, Any] | None = None) -> V031ConsolidationAuditTrail:
    return V031ConsolidationAuditTrail(
        audit_trail_id="v031_consolidation_audit_trail:v0.31.9",
        version=V0319_VERSION,
        reviewed_artifact_refs=list(V0319_INCLUDED_VERSIONS),
        reviewed_test_refs=[f"tests/test_v031{index}_*.py" for index in range(0, 10)],
        reviewed_doc_refs=[f"docs/versions/v0.31/v0.31.{index}_*.md" for index in range(0, 10)],
        boundary_checks=["no execution", "no external scan", "no tool execution", "no OCEL emission", "no UI runtime"],
        negative_runtime_checks=list(V0319_PROHIBITED_RUNTIME_SURFACES),
        evidence_refs=["focused v0.31.x tests"],
        metadata=dict(metadata or {}),
    )


def build_v031_consolidation_report(
    snapshot: InternalTriadFoundationSnapshot,
    manifest: InternalTriadReleaseManifest,
    handoff_packet: InternalTriadV032HandoffPacket | None = None,
    gap_register: InternalTriadGapRegister | None = None,
    metadata: dict[str, Any] | None = None,
) -> V031ConsolidationReport:
    if not isinstance(snapshot, InternalTriadFoundationSnapshot):
        raise TypeError("snapshot must be InternalTriadFoundationSnapshot")
    if not isinstance(manifest, InternalTriadReleaseManifest):
        raise TypeError("manifest must be InternalTriadReleaseManifest")
    blocking = list(gap_register.blocking_gaps if gap_register is not None else [])
    return V031ConsolidationReport(
        report_id="v031_consolidation_report:internal_triad_foundation_v1",
        version=V0319_VERSION,
        release_name=V0319_RELEASE_NAME,
        snapshot_id=snapshot.snapshot_id,
        release_manifest_id=manifest.release_manifest_id,
        handoff_id=handoff_packet.handoff_id if handoff_packet is not None else None,
        consolidation_status=InternalTriadConsolidationStatus.CONSOLIDATED_WITH_GAPS if not blocking else InternalTriadConsolidationStatus.BLOCKED,
        readiness_level=InternalTriadReadinessLevel.HANDOFF_READY_FOR_V032 if not blocking else InternalTriadReadinessLevel.BLOCKED,
        summary="v0.31.x is consolidated into Internal Triad Skill Foundation v1 without runtime enablement.",
        completed_items=list(V0319_INCLUDED_VERSIONS),
        blocked_items=blocking,
        future_track_items=["D4-D9", "runtime execution", "external scan", "read-only tool execution", "OCEL emission", "UI runtime"],
        runtime_not_ready_items=list(V0319_PROHIBITED_RUNTIME_SURFACES),
        v032_handoff_summary="Ready for v0.32 design-stage External Harness Observation & Digestion Pipeline handoff only.",
        ready_for_v032=not blocking,
        ready_for_execution=False,
        ready_for_skill_activation=False,
        ready_for_external_scan=False,
        ready_for_ocel_emission=False,
        ready_for_ui_runtime=False,
        evidence_refs=list(snapshot.evidence_refs),
        withdrawal_conditions=list(snapshot.withdrawal_conditions),
        metadata=dict(metadata or {}),
    )


def internal_triad_release_flags_preserve_runtime_false(flags: InternalTriadReleaseFlagSet) -> bool:
    return (
        flags.ready_for_execution is False
        and flags.ready_for_skill_activation is False
        and flags.ready_for_external_scan is False
        and flags.ready_for_external_control is False
        and flags.ready_for_authority_grant is False
        and flags.ready_for_read_only_tool_execution is False
        and flags.ready_for_registry_mutation is False
        and flags.ready_for_memory_mutation is False
        and flags.ready_for_ocel_emission is False
        and flags.ready_for_runtime_trace_persistence is False
        and flags.ready_for_ui_runtime is False
        and flags.ready_for_action_execution is False
        and flags.ready_for_approval_execution is False
        and flags.ready_for_provider_invocation is False
        and flags.ready_for_network_access is False
        and flags.ready_for_credential_access is False
        and flags.ready_for_command_execution is False
        and flags.ready_for_rpa_runtime_control is False
        and flags.ready_for_browser_runtime_control is False
        and flags.ready_for_gateway_control is False
        and flags.production_certified is False
        and flags.live_adapter_certified is False
        and flags.runtime_ready is False
        and (flags.max_grantable_level is None or normalize_dominion_level(flags.max_grantable_level) <= DominionLevel.D3_SIMULATE)
    )


def internal_triad_consolidation_preserves_no_execution(obj: Any) -> bool:
    return all(getattr(obj, name, False) is False for name in ("ready_for_execution", "ready_for_skill_activation", "ready_for_external_scan"))


def v032_handoff_packet_is_design_stage_only(packet: InternalTriadV032HandoffPacket) -> bool:
    return packet.ready_for_execution is False and packet.implementation is False and "v0.32" in packet.target_version_track


def v031_consolidation_report_is_not_runtime_ready(report: V031ConsolidationReport) -> bool:
    return (
        report.ready_for_execution is False
        and report.ready_for_skill_activation is False
        and report.ready_for_external_scan is False
        and report.ready_for_ocel_emission is False
        and report.ready_for_ui_runtime is False
        and report.runtime_enablement is False
    )
