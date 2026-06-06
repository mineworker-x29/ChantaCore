from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from chanta_core.internal_triad.boundaries import _require_non_blank, _validate_string_list
from chanta_core.internal_triad.observation import (
    V0311_REQUIRED_PROHIBITED_RUNTIME_ACTIONS,
    ObservationEvidenceQuality,
    ObservationFinding,
    ObservationFindingKind,
    ObservationGap,
    ObservationRiskSignal,
    ObservationSkillOutput,
    normalize_observation_evidence_quality,
)
from chanta_core.internal_triad.skill_kinds import V0310_TRACK


V0312_VERSION = "v0.31.2"
V0312_RELEASE_NAME = "v0.31.2 Observation Report / Capability Map"
V0312_TRACK = V0310_TRACK

V0312_REQUIRED_PROHIBITED_RUNTIME_ACTIONS = [
    *V0311_REQUIRED_PROHIBITED_RUNTIME_ACTIONS,
    "internal_skill_candidate_creation",
    "internalization_plan_creation",
    "dominion_decision_creation",
]

V0312_PROHIBITED_UNTIL_LATER_GATE = [
    "external_scan",
    "source_ref_fetch",
    "url_fetch",
    "internal_tool_execution",
    "read_only_tool_execution",
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
    "rollback",
    "retry",
    "digestion_candidate_creation",
    "internal_skill_candidate_creation",
    "internalization_plan_creation",
    "dominion_target_creation",
    "dominion_decision_creation",
]


class ObservationReportStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    REPORT_READY = "report_ready"
    REPORT_READY_WITH_GAPS = "report_ready_with_gaps"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class CapabilityClassification(StrEnum):
    UNKNOWN = "unknown"
    DESCRIPTIVE_ONLY = "descriptive_only"
    SAFE_DESCRIPTIVE = "safe_descriptive"
    DIGESTION_SIGNAL = "digestion_signal"
    DOMINION_SIGNAL = "dominion_signal"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class CapabilityMapStatus(StrEnum):
    UNKNOWN = "unknown"
    MAP_READY = "map_ready"
    MAP_READY_WITH_GAPS = "map_ready_with_gaps"
    INCOMPLETE = "incomplete"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


def _validate_version_includes_v0312(version: str) -> None:
    _require_non_blank("version", version)
    if V0312_VERSION not in version:
        raise ValueError("version must include v0.31.2")


def _validate_any_list(name: str, values: list[Any]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")


def _validate_object_list(name: str, values: list[Any], expected_type: type) -> None:
    if not isinstance(values, list) or not all(isinstance(item, expected_type) for item in values):
        raise TypeError(f"{name} must be list[{expected_type.__name__}]")


def _metadata_flag_true(metadata: dict[str, Any], names: set[str]) -> bool:
    return isinstance(metadata, dict) and any(metadata.get(name) is True for name in names)


def _contains_dominion_signal(items: list[Any]) -> bool:
    for item in items:
        if isinstance(item, ObservationFinding):
            try:
                kind = normalize_observation_finding_kind_for_report(item.finding_kind)
            except ValueError:
                kind = None
            if kind is ObservationFindingKind.DOMINION_REQUIRED_SIGNAL:
                return True
        elif isinstance(item, dict):
            text = " ".join(str(value).lower() for value in item.values())
            if "dominion" in text:
                return True
        elif "dominion" in str(item).lower():
            return True
    return False


def normalize_observation_report_status(value: ObservationReportStatus | str) -> ObservationReportStatus:
    if isinstance(value, ObservationReportStatus):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("observation report status must not be blank")
        return ObservationReportStatus(stripped)
    raise TypeError(f"unsupported observation report status: {value!r}")


def normalize_capability_classification(value: CapabilityClassification | str) -> CapabilityClassification:
    if isinstance(value, CapabilityClassification):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("capability classification must not be blank")
        return CapabilityClassification(stripped)
    raise TypeError(f"unsupported capability classification: {value!r}")


def normalize_capability_map_status(value: CapabilityMapStatus | str) -> CapabilityMapStatus:
    if isinstance(value, CapabilityMapStatus):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("capability map status must not be blank")
        return CapabilityMapStatus(stripped)
    raise TypeError(f"unsupported capability map status: {value!r}")


def normalize_observation_finding_kind_for_report(value: ObservationFindingKind | str) -> ObservationFindingKind:
    if isinstance(value, ObservationFindingKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("observation finding kind must not be blank")
        return ObservationFindingKind(stripped)
    raise TypeError(f"unsupported observation finding kind: {value!r}")


@dataclass(frozen=True)
class CapabilityMapEntry:
    entry_id: str
    target_id: str | None
    capability_name: str
    capability_kind: str | None
    classification: CapabilityClassification | str
    source_finding_ids: list[str]
    source_risk_signal_ids: list[str]
    source_gap_ids: list[str]
    evidence_ref_ids: list[str]
    risk_posture: str
    evidence_quality: str
    boundary_surfaces: list[str]
    effect_surfaces: list[str]
    recommended_next_stage: str | None = None
    blocked_reasons: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("entry_id", self.entry_id)
        _require_non_blank("capability_name", self.capability_name)
        classification = normalize_capability_classification(self.classification)
        for name in (
            "source_finding_ids",
            "source_risk_signal_ids",
            "source_gap_ids",
            "evidence_ref_ids",
            "boundary_surfaces",
            "effect_surfaces",
            "blocked_reasons",
        ):
            _validate_string_list(name, getattr(self, name))
        _require_non_blank("risk_posture", self.risk_posture)
        _require_non_blank("evidence_quality", self.evidence_quality)
        if classification is CapabilityClassification.BLOCKED and not self.blocked_reasons:
            raise ValueError("blocked classification requires blocked_reasons")
        if _metadata_flag_true(
            self.metadata,
            {
                "permission_grant",
                "activate_capability",
                "digestion_candidate_creation",
                "dominion_target_creation",
            },
        ):
            raise ValueError("CapabilityMapEntry is not permission, activation, digestion, or dominion creation")

    @property
    def grants_permission(self) -> bool:
        return False

    @property
    def activates_capability(self) -> bool:
        return False

    @property
    def creates_digestion_candidate(self) -> bool:
        return False

    @property
    def creates_dominion_target(self) -> bool:
        return False


@dataclass(frozen=True)
class ObservedTargetSummary:
    target_summary_id: str
    target_id: str
    display_name: str | None
    source_target_ref_ids: list[str]
    observed_capability_entry_ids: list[str]
    gap_ids: list[str]
    risk_signal_ids: list[str]
    evidence_ref_ids: list[str]
    summary: str
    risk_posture: str
    evidence_quality: str
    ready_for_capability_map: bool
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("target_summary_id", self.target_summary_id)
        _require_non_blank("target_id", self.target_id)
        for name in (
            "source_target_ref_ids",
            "observed_capability_entry_ids",
            "gap_ids",
            "risk_signal_ids",
            "evidence_ref_ids",
        ):
            _validate_string_list(name, getattr(self, name))
        _require_non_blank("summary", self.summary)
        _require_non_blank("risk_posture", self.risk_posture)
        _require_non_blank("evidence_quality", self.evidence_quality)
        if not isinstance(self.ready_for_capability_map, bool):
            raise TypeError("ready_for_capability_map must be bool")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.2")
        if _metadata_flag_true(self.metadata, {"target_access", "external_scan"}):
            raise ValueError("ObservedTargetSummary must not imply target access or external scan")

    @property
    def accesses_target(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalObservationReport:
    report_id: str
    observation_output_id: str | None
    source_input_id: str | None
    target_summaries: list[ObservedTargetSummary]
    findings: list[Any]
    gaps: list[Any]
    risk_signals: list[Any]
    evidence_ref_ids: list[str]
    status: ObservationReportStatus | str
    summary: str
    report_gaps: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    ready_for_v0313_digestion_skill_foundation: bool = False
    ready_for_v0315_dominion_skill_foundation: bool = False
    ready_for_execution: bool = False
    ready_for_skill_activation: bool = False
    ready_for_external_scan: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_object_list("target_summaries", self.target_summaries, ObservedTargetSummary)
        for name in ("findings", "gaps", "risk_signals"):
            _validate_any_list(name, getattr(self, name))
        _validate_string_list("evidence_ref_ids", self.evidence_ref_ids)
        status = normalize_observation_report_status(self.status)
        _require_non_blank("summary", self.summary)
        _validate_string_list("report_gaps", self.report_gaps)
        _validate_string_list("blocked_reasons", self.blocked_reasons)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.2")
        if self.ready_for_skill_activation is not False:
            raise ValueError("ready_for_skill_activation must always be False in v0.31.2")
        if self.ready_for_external_scan is not False:
            raise ValueError("ready_for_external_scan must always be False in v0.31.2")
        if status is ObservationReportStatus.BLOCKED and self.ready_for_v0313_digestion_skill_foundation:
            raise ValueError("blocked observation report cannot be ready for v0.31.3")
        has_dominion_signal = _contains_dominion_signal(self.findings) or _contains_dominion_signal(self.risk_signals)
        conservative_routing = _metadata_flag_true(self.metadata, {"conservative_dominion_routing"})
        if self.ready_for_v0315_dominion_skill_foundation and not (has_dominion_signal or conservative_routing):
            raise ValueError("v0.31.5 readiness requires dominion signal or conservative routing metadata")
        if _metadata_flag_true(
            self.metadata,
            {
                "external_scan",
                "digestion_candidate_creation",
                "dominion_target_creation",
                "active_artifact_registration",
            },
        ):
            raise ValueError("InternalObservationReport must not imply scan, active registration, digestion, or dominion creation")

    @property
    def creates_digestion_candidate(self) -> bool:
        return False

    @property
    def creates_dominion_target(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalCapabilityMap:
    capability_map_id: str
    observation_report_id: str
    target_id: str | None
    entries: list[CapabilityMapEntry]
    safe_descriptive_capability_ids: list[str]
    digestion_signal_capability_ids: list[str]
    dominion_signal_capability_ids: list[str]
    blocked_capability_ids: list[str]
    deferred_capability_ids: list[str]
    unknown_capability_ids: list[str]
    status: CapabilityMapStatus | str
    evidence_ref_ids: list[str] = field(default_factory=list)
    map_gaps: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    ready_for_v0313_digestion_skill_foundation: bool = False
    ready_for_v0315_dominion_skill_foundation: bool = False
    ready_for_execution: bool = False
    ready_for_skill_activation: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("capability_map_id", self.capability_map_id)
        _require_non_blank("observation_report_id", self.observation_report_id)
        _validate_object_list("entries", self.entries, CapabilityMapEntry)
        for name in (
            "safe_descriptive_capability_ids",
            "digestion_signal_capability_ids",
            "dominion_signal_capability_ids",
            "blocked_capability_ids",
            "deferred_capability_ids",
            "unknown_capability_ids",
            "evidence_ref_ids",
            "map_gaps",
            "blocked_reasons",
        ):
            _validate_string_list(name, getattr(self, name))
        status = normalize_capability_map_status(self.status)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.2")
        if self.ready_for_skill_activation is not False:
            raise ValueError("ready_for_skill_activation must always be False in v0.31.2")
        entry_by_id = {entry.entry_id: entry for entry in self.entries}
        for entry_id in self.digestion_signal_capability_ids:
            if entry_id not in entry_by_id:
                raise ValueError("digestion_signal_capability_ids must refer to existing entries")
            if normalize_capability_classification(entry_by_id[entry_id].classification) is not CapabilityClassification.DIGESTION_SIGNAL:
                raise ValueError("digestion_signal_capability_ids must refer to digestion_signal entries")
        for entry_id in self.dominion_signal_capability_ids:
            if entry_id not in entry_by_id:
                raise ValueError("dominion_signal_capability_ids must refer to existing entries")
            if normalize_capability_classification(entry_by_id[entry_id].classification) is not CapabilityClassification.DOMINION_SIGNAL:
                raise ValueError("dominion_signal_capability_ids must refer to dominion_signal entries")
        if self.blocked_capability_ids and not self.blocked_reasons:
            raise ValueError("blocked_capability_ids require blocked_reasons")
        if status is CapabilityMapStatus.BLOCKED and self.ready_for_v0313_digestion_skill_foundation:
            raise ValueError("blocked capability map cannot be ready for v0.31.3")
        if _metadata_flag_true(self.metadata, {"permission_map", "activate_capabilities", "runtime_enablement"}):
            raise ValueError("InternalCapabilityMap is not a permission map and does not activate capabilities")

    @property
    def grants_permission(self) -> bool:
        return False

    @property
    def activates_capabilities(self) -> bool:
        return False


@dataclass(frozen=True)
class ObservationGapRegister:
    gap_register_id: str
    observation_report_id: str
    gap_ids: list[str]
    blocking_gap_ids: list[str]
    non_blocking_gap_ids: list[str]
    deferred_gap_ids: list[str]
    future_track_gap_ids: list[str]
    summary: str
    evidence_ref_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("gap_register_id", self.gap_register_id)
        _require_non_blank("observation_report_id", self.observation_report_id)
        for name in (
            "gap_ids",
            "blocking_gap_ids",
            "non_blocking_gap_ids",
            "deferred_gap_ids",
            "future_track_gap_ids",
            "evidence_ref_ids",
        ):
            _validate_string_list(name, getattr(self, name))
        _require_non_blank("summary", self.summary)
        if _metadata_flag_true(self.metadata, {"remediation_execution", "automatic_remediation"}):
            raise ValueError("ObservationGapRegister must not execute remediation")

    @property
    def executes_remediation(self) -> bool:
        return False

    @property
    def blocks_next_stage(self) -> bool:
        return bool(self.blocking_gap_ids)


@dataclass(frozen=True)
class ObservationRiskMap:
    risk_map_id: str
    observation_report_id: str
    risk_signal_ids: list[str]
    high_risk_signal_ids: list[str]
    critical_risk_signal_ids: list[str]
    blocked_risk_signal_ids: list[str]
    risk_surfaces: list[str]
    recommended_boundaries: list[str]
    summary: str
    evidence_ref_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_map_id", self.risk_map_id)
        _require_non_blank("observation_report_id", self.observation_report_id)
        for name in (
            "risk_signal_ids",
            "high_risk_signal_ids",
            "critical_risk_signal_ids",
            "blocked_risk_signal_ids",
            "risk_surfaces",
            "recommended_boundaries",
            "evidence_ref_ids",
        ):
            _validate_string_list(name, getattr(self, name))
        _require_non_blank("summary", self.summary)
        if _metadata_flag_true(self.metadata, {"authority_grant", "dominion_target_creation"}):
            raise ValueError("ObservationRiskMap must not grant authority or create dominion targets")

    @property
    def grants_authority(self) -> bool:
        return False

    @property
    def creates_dominion_target(self) -> bool:
        return False


@dataclass(frozen=True)
class ObservationEvidenceTable:
    evidence_table_id: str
    observation_report_id: str
    evidence_ref_ids: list[str]
    strong_evidence_ref_ids: list[str]
    weak_evidence_ref_ids: list[str]
    missing_evidence_items: list[str]
    conflicting_evidence_ref_ids: list[str]
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("evidence_table_id", self.evidence_table_id)
        _require_non_blank("observation_report_id", self.observation_report_id)
        for name in (
            "evidence_ref_ids",
            "strong_evidence_ref_ids",
            "weak_evidence_ref_ids",
            "missing_evidence_items",
            "conflicting_evidence_ref_ids",
        ):
            _validate_string_list(name, getattr(self, name))
        _require_non_blank("summary", self.summary)
        if _metadata_flag_true(self.metadata, {"runtime_trust", "execution_evidence"}):
            raise ValueError("ObservationEvidenceTable must not establish runtime trust")

    @property
    def runtime_trust(self) -> bool:
        return False


@dataclass(frozen=True)
class ObservationReportBundle:
    bundle_id: str
    observation_report: InternalObservationReport
    capability_map: InternalCapabilityMap
    gap_register: ObservationGapRegister
    risk_map: ObservationRiskMap
    evidence_table: ObservationEvidenceTable
    status: ObservationReportStatus | str
    ready_for_v0313_digestion_skill_foundation: bool = False
    ready_for_v0315_dominion_skill_foundation: bool = False
    ready_for_execution: bool = False
    ready_for_skill_activation: bool = False
    ready_for_external_scan: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("bundle_id", self.bundle_id)
        if not isinstance(self.observation_report, InternalObservationReport):
            raise TypeError("observation_report must be InternalObservationReport")
        if not isinstance(self.capability_map, InternalCapabilityMap):
            raise TypeError("capability_map must be InternalCapabilityMap")
        if not isinstance(self.gap_register, ObservationGapRegister):
            raise TypeError("gap_register must be ObservationGapRegister")
        if not isinstance(self.risk_map, ObservationRiskMap):
            raise TypeError("risk_map must be ObservationRiskMap")
        if not isinstance(self.evidence_table, ObservationEvidenceTable):
            raise TypeError("evidence_table must be ObservationEvidenceTable")
        normalize_observation_report_status(self.status)
        report_id = self.observation_report.report_id
        for name, nested_report_id in (
            ("capability_map", self.capability_map.observation_report_id),
            ("gap_register", self.gap_register.observation_report_id),
            ("risk_map", self.risk_map.observation_report_id),
            ("evidence_table", self.evidence_table.observation_report_id),
        ):
            if nested_report_id != report_id:
                raise ValueError(f"{name} observation_report_id must match observation_report.report_id")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.2")
        if self.ready_for_skill_activation is not False:
            raise ValueError("ready_for_skill_activation must always be False in v0.31.2")
        if self.ready_for_external_scan is not False:
            raise ValueError("ready_for_external_scan must always be False in v0.31.2")
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"active_artifact_registration", "runtime_enablement"}):
            raise ValueError("ObservationReportBundle must not imply active artifact registration")

    @property
    def active_artifact_registration(self) -> bool:
        return False


@dataclass(frozen=True)
class ObservationReportRunPreview:
    run_preview_id: str
    observation_output_id: str | None
    planned_steps: list[str]
    expected_artifacts: list[str]
    explicitly_not_performed: list[str]
    no_execution_guarantee: bool = True
    no_external_scan_guarantee: bool = True
    no_tool_execution_guarantee: bool = True
    no_digestion_candidate_creation_guarantee: bool = True
    no_dominion_target_creation_guarantee: bool = True
    no_registry_mutation_guarantee: bool = True
    no_memory_mutation_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        _validate_string_list("planned_steps", self.planned_steps)
        _validate_string_list("expected_artifacts", self.expected_artifacts)
        _validate_string_list("explicitly_not_performed", self.explicitly_not_performed)
        for name in (
            "no_execution_guarantee",
            "no_external_scan_guarantee",
            "no_tool_execution_guarantee",
            "no_digestion_candidate_creation_guarantee",
            "no_dominion_target_creation_guarantee",
            "no_registry_mutation_guarantee",
            "no_memory_mutation_guarantee",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.31.2")
        if _metadata_flag_true(self.metadata, {"executes_run", "external_scan", "tool_execution"}):
            raise ValueError("ObservationReportRunPreview must not imply execution")

    @property
    def executes_run(self) -> bool:
        return False


@dataclass(frozen=True)
class V0312ReadinessReport:
    report_id: str
    version: str
    observation_report_bundle_id: str | None
    summary: str
    ready_for_v0313_digestion_skill_foundation: bool
    ready_for_v0315_dominion_skill_foundation: bool
    ready_for_execution: bool = False
    ready_for_skill_activation: bool = False
    ready_for_external_scan: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(V0312_PROHIBITED_UNTIL_LATER_GATE))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0312(self.version)
        _require_non_blank("summary", self.summary)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.2")
        if self.ready_for_skill_activation is not False:
            raise ValueError("ready_for_skill_activation must always be False in v0.31.2")
        if self.ready_for_external_scan is not False:
            raise ValueError("ready_for_external_scan must always be False in v0.31.2")
        for name in (
            "completed_items",
            "blocked_items",
            "future_track_items",
            "prohibited_until_later_gate",
            "evidence_refs",
            "withdrawal_conditions",
        ):
            _validate_string_list(name, getattr(self, name))
        missing = set(V0312_PROHIBITED_UNTIL_LATER_GATE) - set(self.prohibited_until_later_gate)
        if missing:
            raise ValueError(f"prohibited_until_later_gate missing required items: {sorted(missing)}")
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "execution_readiness"}):
            raise ValueError("V0312ReadinessReport must not imply runtime readiness")

    @property
    def runtime_enablement(self) -> bool:
        return False


def classify_capability_from_observation_finding(finding: ObservationFinding) -> CapabilityClassification:
    if not isinstance(finding, ObservationFinding):
        raise TypeError("finding must be ObservationFinding")
    finding_kind = normalize_observation_finding_kind_for_report(finding.finding_kind)
    if finding_kind is ObservationFindingKind.DIGESTION_POSSIBLE_SIGNAL:
        return CapabilityClassification.DIGESTION_SIGNAL
    if finding_kind is ObservationFindingKind.DOMINION_REQUIRED_SIGNAL:
        return CapabilityClassification.DOMINION_SIGNAL
    if finding_kind is ObservationFindingKind.CAPABILITY_DETECTED:
        quality = normalize_observation_evidence_quality(finding.evidence_quality)
        if quality in {
            ObservationEvidenceQuality.SUFFICIENT_FOR_OBSERVATION,
            ObservationEvidenceQuality.SUFFICIENT_FOR_NEXT_STAGE_REVIEW,
        }:
            return CapabilityClassification.SAFE_DESCRIPTIVE
        return CapabilityClassification.DESCRIPTIVE_ONLY
    if finding_kind is ObservationFindingKind.NO_OP_RECOMMENDED:
        return CapabilityClassification.NO_OP
    if finding_kind in {
        ObservationFindingKind.EVIDENCE_MISSING,
        ObservationFindingKind.TRUST_GAP_DETECTED,
        ObservationFindingKind.CERTIFICATION_GAP_SIGNAL,
        ObservationFindingKind.PREVIEW_GATE_GAP_SIGNAL,
        ObservationFindingKind.OCEL_TRACE_NEED_DETECTED,
    }:
        return CapabilityClassification.DEFERRED
    if finding_kind is ObservationFindingKind.UNKNOWN:
        return CapabilityClassification.UNKNOWN
    return CapabilityClassification.DESCRIPTIVE_ONLY


def build_capability_map_entry(
    entry_id: str,
    capability_name: str,
    classification: CapabilityClassification | str,
    target_id: str | None = None,
    capability_kind: str | None = None,
    source_finding_ids: list[str] | None = None,
    source_risk_signal_ids: list[str] | None = None,
    source_gap_ids: list[str] | None = None,
    evidence_ref_ids: list[str] | None = None,
    risk_posture: str = "unknown",
    evidence_quality: str = "unknown",
    boundary_surfaces: list[str] | None = None,
    effect_surfaces: list[str] | None = None,
    recommended_next_stage: str | None = None,
    blocked_reasons: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> CapabilityMapEntry:
    return CapabilityMapEntry(
        entry_id=entry_id,
        target_id=target_id,
        capability_name=capability_name,
        capability_kind=capability_kind,
        classification=classification,
        source_finding_ids=list(source_finding_ids or []),
        source_risk_signal_ids=list(source_risk_signal_ids or []),
        source_gap_ids=list(source_gap_ids or []),
        evidence_ref_ids=list(evidence_ref_ids or []),
        risk_posture=risk_posture,
        evidence_quality=evidence_quality,
        boundary_surfaces=list(boundary_surfaces or []),
        effect_surfaces=list(effect_surfaces or []),
        recommended_next_stage=recommended_next_stage,
        blocked_reasons=list(blocked_reasons or []),
        metadata=dict(metadata or {}),
    )


def build_observed_target_summary(
    target_summary_id: str,
    target_id: str,
    summary: str,
    display_name: str | None = None,
    source_target_ref_ids: list[str] | None = None,
    observed_capability_entry_ids: list[str] | None = None,
    gap_ids: list[str] | None = None,
    risk_signal_ids: list[str] | None = None,
    evidence_ref_ids: list[str] | None = None,
    risk_posture: str = "unknown",
    evidence_quality: str = "unknown",
    ready_for_capability_map: bool = False,
    metadata: dict[str, Any] | None = None,
) -> ObservedTargetSummary:
    return ObservedTargetSummary(
        target_summary_id=target_summary_id,
        target_id=target_id,
        display_name=display_name,
        source_target_ref_ids=list(source_target_ref_ids or []),
        observed_capability_entry_ids=list(observed_capability_entry_ids or []),
        gap_ids=list(gap_ids or []),
        risk_signal_ids=list(risk_signal_ids or []),
        evidence_ref_ids=list(evidence_ref_ids or []),
        summary=summary,
        risk_posture=risk_posture,
        evidence_quality=evidence_quality,
        ready_for_capability_map=ready_for_capability_map,
        ready_for_execution=False,
        metadata=dict(metadata or {}),
    )


def build_internal_observation_report(
    report_id: str,
    summary: str,
    status: ObservationReportStatus | str,
    observation_output: ObservationSkillOutput | None = None,
    observation_output_id: str | None = None,
    source_input_id: str | None = None,
    target_summaries: list[ObservedTargetSummary] | None = None,
    findings: list[Any] | None = None,
    gaps: list[Any] | None = None,
    risk_signals: list[Any] | None = None,
    evidence_ref_ids: list[str] | None = None,
    report_gaps: list[str] | None = None,
    blocked_reasons: list[str] | None = None,
    ready_for_v0313_digestion_skill_foundation: bool = False,
    ready_for_v0315_dominion_skill_foundation: bool = False,
    metadata: dict[str, Any] | None = None,
) -> InternalObservationReport:
    if observation_output is not None:
        observation_output_id = observation_output.observation_output_id
        source_input_id = observation_output.observation_input_id
        findings = list(findings if findings is not None else observation_output.findings)
        gaps = list(gaps if gaps is not None else observation_output.gaps)
        risk_signals = list(risk_signals if risk_signals is not None else observation_output.risk_signals)
        evidence_ref_ids = list(evidence_ref_ids if evidence_ref_ids is not None else observation_output.evidence_ref_ids)
    return InternalObservationReport(
        report_id=report_id,
        observation_output_id=observation_output_id,
        source_input_id=source_input_id,
        target_summaries=list(target_summaries or []),
        findings=list(findings or []),
        gaps=list(gaps or []),
        risk_signals=list(risk_signals or []),
        evidence_ref_ids=list(evidence_ref_ids or []),
        status=status,
        summary=summary,
        report_gaps=list(report_gaps or []),
        blocked_reasons=list(blocked_reasons or []),
        ready_for_v0313_digestion_skill_foundation=ready_for_v0313_digestion_skill_foundation,
        ready_for_v0315_dominion_skill_foundation=ready_for_v0315_dominion_skill_foundation,
        ready_for_execution=False,
        ready_for_skill_activation=False,
        ready_for_external_scan=False,
        metadata=dict(metadata or {}),
    )


def build_internal_capability_map(
    capability_map_id: str,
    observation_report_id: str,
    entries: list[CapabilityMapEntry] | None = None,
    target_id: str | None = None,
    safe_descriptive_capability_ids: list[str] | None = None,
    digestion_signal_capability_ids: list[str] | None = None,
    dominion_signal_capability_ids: list[str] | None = None,
    blocked_capability_ids: list[str] | None = None,
    deferred_capability_ids: list[str] | None = None,
    unknown_capability_ids: list[str] | None = None,
    status: CapabilityMapStatus | str = CapabilityMapStatus.UNKNOWN,
    evidence_ref_ids: list[str] | None = None,
    map_gaps: list[str] | None = None,
    blocked_reasons: list[str] | None = None,
    ready_for_v0313_digestion_skill_foundation: bool = False,
    ready_for_v0315_dominion_skill_foundation: bool = False,
    metadata: dict[str, Any] | None = None,
) -> InternalCapabilityMap:
    return InternalCapabilityMap(
        capability_map_id=capability_map_id,
        observation_report_id=observation_report_id,
        target_id=target_id,
        entries=list(entries or []),
        safe_descriptive_capability_ids=list(safe_descriptive_capability_ids or []),
        digestion_signal_capability_ids=list(digestion_signal_capability_ids or []),
        dominion_signal_capability_ids=list(dominion_signal_capability_ids or []),
        blocked_capability_ids=list(blocked_capability_ids or []),
        deferred_capability_ids=list(deferred_capability_ids or []),
        unknown_capability_ids=list(unknown_capability_ids or []),
        status=status,
        evidence_ref_ids=list(evidence_ref_ids or []),
        map_gaps=list(map_gaps or []),
        blocked_reasons=list(blocked_reasons or []),
        ready_for_v0313_digestion_skill_foundation=ready_for_v0313_digestion_skill_foundation,
        ready_for_v0315_dominion_skill_foundation=ready_for_v0315_dominion_skill_foundation,
        ready_for_execution=False,
        ready_for_skill_activation=False,
        metadata=dict(metadata or {}),
    )


def build_observation_gap_register(
    gap_register_id: str,
    observation_report_id: str,
    summary: str,
    gap_ids: list[str] | None = None,
    blocking_gap_ids: list[str] | None = None,
    non_blocking_gap_ids: list[str] | None = None,
    deferred_gap_ids: list[str] | None = None,
    future_track_gap_ids: list[str] | None = None,
    evidence_ref_ids: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ObservationGapRegister:
    return ObservationGapRegister(
        gap_register_id=gap_register_id,
        observation_report_id=observation_report_id,
        gap_ids=list(gap_ids or []),
        blocking_gap_ids=list(blocking_gap_ids or []),
        non_blocking_gap_ids=list(non_blocking_gap_ids or []),
        deferred_gap_ids=list(deferred_gap_ids or []),
        future_track_gap_ids=list(future_track_gap_ids or []),
        summary=summary,
        evidence_ref_ids=list(evidence_ref_ids or []),
        metadata=dict(metadata or {}),
    )


def build_observation_risk_map(
    risk_map_id: str,
    observation_report_id: str,
    summary: str,
    risk_signal_ids: list[str] | None = None,
    high_risk_signal_ids: list[str] | None = None,
    critical_risk_signal_ids: list[str] | None = None,
    blocked_risk_signal_ids: list[str] | None = None,
    risk_surfaces: list[str] | None = None,
    recommended_boundaries: list[str] | None = None,
    evidence_ref_ids: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ObservationRiskMap:
    return ObservationRiskMap(
        risk_map_id=risk_map_id,
        observation_report_id=observation_report_id,
        risk_signal_ids=list(risk_signal_ids or []),
        high_risk_signal_ids=list(high_risk_signal_ids or []),
        critical_risk_signal_ids=list(critical_risk_signal_ids or []),
        blocked_risk_signal_ids=list(blocked_risk_signal_ids or []),
        risk_surfaces=list(risk_surfaces or []),
        recommended_boundaries=list(recommended_boundaries or []),
        summary=summary,
        evidence_ref_ids=list(evidence_ref_ids or []),
        metadata=dict(metadata or {}),
    )


def build_observation_evidence_table(
    evidence_table_id: str,
    observation_report_id: str,
    summary: str,
    evidence_ref_ids: list[str] | None = None,
    strong_evidence_ref_ids: list[str] | None = None,
    weak_evidence_ref_ids: list[str] | None = None,
    missing_evidence_items: list[str] | None = None,
    conflicting_evidence_ref_ids: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ObservationEvidenceTable:
    return ObservationEvidenceTable(
        evidence_table_id=evidence_table_id,
        observation_report_id=observation_report_id,
        evidence_ref_ids=list(evidence_ref_ids or []),
        strong_evidence_ref_ids=list(strong_evidence_ref_ids or []),
        weak_evidence_ref_ids=list(weak_evidence_ref_ids or []),
        missing_evidence_items=list(missing_evidence_items or []),
        conflicting_evidence_ref_ids=list(conflicting_evidence_ref_ids or []),
        summary=summary,
        metadata=dict(metadata or {}),
    )


def build_observation_report_bundle(
    bundle_id: str,
    observation_report: InternalObservationReport,
    capability_map: InternalCapabilityMap,
    gap_register: ObservationGapRegister,
    risk_map: ObservationRiskMap,
    evidence_table: ObservationEvidenceTable,
    status: ObservationReportStatus | str,
    ready_for_v0313_digestion_skill_foundation: bool = False,
    ready_for_v0315_dominion_skill_foundation: bool = False,
    evidence_refs: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ObservationReportBundle:
    return ObservationReportBundle(
        bundle_id=bundle_id,
        observation_report=observation_report,
        capability_map=capability_map,
        gap_register=gap_register,
        risk_map=risk_map,
        evidence_table=evidence_table,
        status=status,
        ready_for_v0313_digestion_skill_foundation=ready_for_v0313_digestion_skill_foundation,
        ready_for_v0315_dominion_skill_foundation=ready_for_v0315_dominion_skill_foundation,
        ready_for_execution=False,
        ready_for_skill_activation=False,
        ready_for_external_scan=False,
        evidence_refs=list(evidence_refs or []),
        metadata=dict(metadata or {}),
    )


def build_observation_report_run_preview(
    run_preview_id: str,
    observation_output_id: str | None = None,
    planned_steps: list[str] | None = None,
    expected_artifacts: list[str] | None = None,
    explicitly_not_performed: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ObservationReportRunPreview:
    return ObservationReportRunPreview(
        run_preview_id=run_preview_id,
        observation_output_id=observation_output_id,
        planned_steps=list(planned_steps or ["structure observation report", "derive descriptive capability map"]),
        expected_artifacts=list(
            expected_artifacts
            or [
                "InternalObservationReport",
                "InternalCapabilityMap",
                "ObservationGapRegister",
                "ObservationRiskMap",
                "ObservationEvidenceTable",
                "ObservationReportBundle",
            ]
        ),
        explicitly_not_performed=list(
            explicitly_not_performed
            or [
                "external_scan",
                "source_ref_fetch",
                "read_only_tool_execution",
                "digestion_candidate_creation",
                "dominion_target_creation",
                "registry_mutation",
                "memory_mutation",
            ]
        ),
        metadata=dict(metadata or {}),
    )


def build_v0312_readiness_report(
    bundle: ObservationReportBundle | None = None,
    ready_for_v0313_digestion_skill_foundation: bool | None = None,
    ready_for_v0315_dominion_skill_foundation: bool | None = None,
) -> V0312ReadinessReport:
    if bundle is not None:
        v0313_ready = bundle.ready_for_v0313_digestion_skill_foundation
        v0315_ready = bundle.ready_for_v0315_dominion_skill_foundation
        bundle_id = bundle.bundle_id
        evidence_refs = list(bundle.evidence_refs)
    else:
        v0313_ready = bool(ready_for_v0313_digestion_skill_foundation)
        v0315_ready = bool(ready_for_v0315_dominion_skill_foundation)
        bundle_id = None
        evidence_refs = []
    return V0312ReadinessReport(
        report_id="v0312_readiness_report:observation_report_capability_map",
        version=V0312_VERSION,
        observation_report_bundle_id=bundle_id,
        summary="v0.31.2 is ready for next design-stage digestion review only; no execution or scan readiness is enabled.",
        ready_for_v0313_digestion_skill_foundation=v0313_ready,
        ready_for_v0315_dominion_skill_foundation=v0315_ready,
        ready_for_execution=False,
        ready_for_skill_activation=False,
        ready_for_external_scan=False,
        completed_items=[
            "observation report status taxonomy",
            "capability classification taxonomy",
            "internal observation report model",
            "internal capability map model",
            "gap, risk, and evidence table models",
            "observation report bundle model",
        ],
        blocked_items=[],
        future_track_items=[
            "external scan",
            "read-only tool execution",
            "digestion candidate creation",
            "dominion target creation",
        ],
        evidence_refs=evidence_refs,
        withdrawal_conditions=[
            "capability map is treated as permission or activation",
            "digestion_signal is treated as active candidate creation",
            "dominion_signal is treated as target or authority creation",
            "ready_for_execution, ready_for_skill_activation, or ready_for_external_scan becomes true",
        ],
        metadata={"readiness_report_is_runtime_enablement": False},
    )


def observation_report_preserves_no_execution(report: InternalObservationReport) -> bool:
    return (
        report.ready_for_execution is False
        and report.ready_for_skill_activation is False
        and report.ready_for_external_scan is False
        and report.creates_digestion_candidate is False
        and report.creates_dominion_target is False
    )


def capability_map_preserves_no_activation(capability_map: InternalCapabilityMap) -> bool:
    return (
        capability_map.ready_for_execution is False
        and capability_map.ready_for_skill_activation is False
        and capability_map.grants_permission is False
        and capability_map.activates_capabilities is False
        and all(entry.grants_permission is False and entry.activates_capability is False for entry in capability_map.entries)
    )


def observation_bundle_preserves_no_runtime(bundle: ObservationReportBundle) -> bool:
    return (
        bundle.ready_for_execution is False
        and bundle.ready_for_skill_activation is False
        and bundle.ready_for_external_scan is False
        and bundle.active_artifact_registration is False
        and observation_report_preserves_no_execution(bundle.observation_report)
        and capability_map_preserves_no_activation(bundle.capability_map)
    )


def observation_report_is_not_digestion_or_dominion(bundle_or_report: ObservationReportBundle | InternalObservationReport) -> bool:
    if isinstance(bundle_or_report, ObservationReportBundle):
        report = bundle_or_report.observation_report
        entries = bundle_or_report.capability_map.entries
    elif isinstance(bundle_or_report, InternalObservationReport):
        report = bundle_or_report
        entries = []
    else:
        raise TypeError("expected ObservationReportBundle or InternalObservationReport")
    return (
        report.creates_digestion_candidate is False
        and report.creates_dominion_target is False
        and all(entry.creates_digestion_candidate is False and entry.creates_dominion_target is False for entry in entries)
    )
