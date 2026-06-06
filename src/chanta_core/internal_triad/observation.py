from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from chanta_core.internal_triad.boundaries import V0310_REQUIRED_PROHIBITED_RUNTIME_ACTIONS, _require_non_blank, _validate_string_list
from chanta_core.internal_triad.skill_kinds import V0310_TRACK


V0311_VERSION = "v0.31.1"
V0311_RELEASE_NAME = "v0.31.1 Observation Skill Foundation"
V0311_TRACK = V0310_TRACK

V0311_REQUIRED_PROHIBITED_RUNTIME_ACTIONS = [
    "external_scan",
    "source_ref_fetch",
    "url_fetch",
    "external_execution",
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
    "rollback",
    "retry",
    "active_registry_mutation",
    "active_memory_mutation",
    "skill_activation",
    "digestion_candidate_creation",
    "dominion_target_creation",
]

V0311_PROHIBITED_UNTIL_LATER_GATE = [
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
    "dominion_target_creation",
]


class ObservationSkillSourceKind(StrEnum):
    V030_HANDOFF_PACKET = "v030_handoff_packet"
    EXTERNAL_TARGET_RECORD = "external_target_record"
    EXTERNAL_CAPABILITY_OBSERVATION_REPORT = "external_capability_observation_report"
    DIGESTION_FEASIBILITY_REPORT = "digestion_feasibility_report"
    DOMINION_AUTHORITY_DECISION = "dominion_authority_decision"
    EXTERNAL_DELEGATION_DRY_RUN_REPORT = "external_delegation_dry_run_report"
    APPROVAL_AUDIT_BOUNDARY = "approval_audit_boundary"
    CERTIFICATION_REPORT = "certification_report"
    PREVIEW_GATE_REPORT = "preview_gate_report"
    CONSOLIDATION_REPORT = "consolidation_report"
    MANUAL_EVIDENCE_REF = "manual_evidence_ref"
    UNKNOWN = "unknown"


class ObservationFocusKind(StrEnum):
    TARGET_IDENTITY = "target_identity"
    TARGET_TRUST_BOUNDARY = "target_trust_boundary"
    CAPABILITY_SURFACE = "capability_surface"
    EVIDENCE_QUALITY = "evidence_quality"
    RISK_SURFACE = "risk_surface"
    EFFECT_SURFACE = "effect_surface"
    BOUNDARY_SURFACE = "boundary_surface"
    DIGESTION_RELEVANCE = "digestion_relevance"
    DOMINION_RELEVANCE = "dominion_relevance"
    CERTIFICATION_COVERAGE = "certification_coverage"
    PREVIEW_GATE_READINESS = "preview_gate_readiness"
    OCEL_TRACE_RELEVANCE = "ocel_trace_relevance"
    GAP_DETECTION = "gap_detection"
    UNKNOWN = "unknown"


class ObservationFindingKind(StrEnum):
    DESCRIPTIVE_SUMMARY = "descriptive_summary"
    CAPABILITY_DETECTED = "capability_detected"
    EVIDENCE_LINKED = "evidence_linked"
    EVIDENCE_MISSING = "evidence_missing"
    RISK_SIGNAL_DETECTED = "risk_signal_detected"
    BOUNDARY_SURFACE_DETECTED = "boundary_surface_detected"
    EFFECT_SURFACE_DETECTED = "effect_surface_detected"
    TRUST_GAP_DETECTED = "trust_gap_detected"
    DIGESTION_POSSIBLE_SIGNAL = "digestion_possible_signal"
    DOMINION_REQUIRED_SIGNAL = "dominion_required_signal"
    CERTIFICATION_GAP_SIGNAL = "certification_gap_signal"
    PREVIEW_GATE_GAP_SIGNAL = "preview_gate_gap_signal"
    OCEL_TRACE_NEED_DETECTED = "ocel_trace_need_detected"
    NO_OP_RECOMMENDED = "no_op_recommended"
    UNKNOWN = "unknown"


class ObservationGapKind(StrEnum):
    MISSING_TARGET_IDENTITY = "missing_target_identity"
    MISSING_TRUST_BOUNDARY = "missing_trust_boundary"
    MISSING_CAPABILITY_REPORT = "missing_capability_report"
    MISSING_EVIDENCE_REFS = "missing_evidence_refs"
    MISSING_RISK_CLASSIFICATION = "missing_risk_classification"
    MISSING_BOUNDARY_CLASSIFICATION = "missing_boundary_classification"
    MISSING_DIGESTION_DECISION = "missing_digestion_decision"
    MISSING_DOMINION_DECISION = "missing_dominion_decision"
    MISSING_APPROVAL_BOUNDARY = "missing_approval_boundary"
    MISSING_AUDIT_POLICY = "missing_audit_policy"
    MISSING_RESULT_BOUNDARY = "missing_result_boundary"
    MISSING_ROLLBACK_OR_NO_OP = "missing_rollback_or_no_op"
    MISSING_CERTIFICATION_CASE = "missing_certification_case"
    MISSING_PREVIEW_GATE_DECISION = "missing_preview_gate_decision"
    MISSING_OCEL_TRACE_PLAN = "missing_ocel_trace_plan"
    UNKNOWN = "unknown"


class ObservationRiskPosture(StrEnum):
    UNKNOWN = "unknown"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class ObservationEvidenceQuality(StrEnum):
    UNKNOWN = "unknown"
    NONE = "none"
    WEAK = "weak"
    PARTIAL = "partial"
    SUFFICIENT_FOR_OBSERVATION = "sufficient_for_observation"
    SUFFICIENT_FOR_NEXT_STAGE_REVIEW = "sufficient_for_next_stage_review"
    CONFLICTING = "conflicting"
    BLOCKED = "blocked"


def _validate_object_list(name: str, values: list[Any], expected_type: type) -> None:
    if not isinstance(values, list) or not all(isinstance(item, expected_type) for item in values):
        raise TypeError(f"{name} must be list[{expected_type.__name__}]")


def _metadata_flag_true(metadata: dict[str, Any], names: set[str]) -> bool:
    return any(metadata.get(name) is True for name in names)


def _validate_prohibited_actions(actions: list[str]) -> None:
    _validate_string_list("prohibited_runtime_actions", actions)
    missing = set(V0311_REQUIRED_PROHIBITED_RUNTIME_ACTIONS) - set(actions)
    if missing:
        raise ValueError(f"prohibited_runtime_actions missing v0.31.1 no-execution actions: {sorted(missing)}")


def _validate_version_includes_v0311(version: str) -> None:
    _require_non_blank("version", version)
    if V0311_VERSION not in version:
        raise ValueError("version must include v0.31.1")


def normalize_observation_source_kind(value: ObservationSkillSourceKind | str) -> ObservationSkillSourceKind:
    if isinstance(value, ObservationSkillSourceKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("observation source kind must not be blank")
        return ObservationSkillSourceKind(stripped)
    raise TypeError(f"unsupported observation source kind: {value!r}")


def normalize_observation_focus_kind(value: ObservationFocusKind | str) -> ObservationFocusKind:
    if isinstance(value, ObservationFocusKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("observation focus kind must not be blank")
        return ObservationFocusKind(stripped)
    raise TypeError(f"unsupported observation focus kind: {value!r}")


def normalize_observation_finding_kind(value: ObservationFindingKind | str) -> ObservationFindingKind:
    if isinstance(value, ObservationFindingKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("observation finding kind must not be blank")
        return ObservationFindingKind(stripped)
    raise TypeError(f"unsupported observation finding kind: {value!r}")


def normalize_observation_gap_kind(value: ObservationGapKind | str) -> ObservationGapKind:
    if isinstance(value, ObservationGapKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("observation gap kind must not be blank")
        return ObservationGapKind(stripped)
    raise TypeError(f"unsupported observation gap kind: {value!r}")


def normalize_observation_risk_posture(value: ObservationRiskPosture | str) -> ObservationRiskPosture:
    if isinstance(value, ObservationRiskPosture):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("observation risk posture must not be blank")
        return ObservationRiskPosture(stripped)
    raise TypeError(f"unsupported observation risk posture: {value!r}")


def normalize_observation_evidence_quality(value: ObservationEvidenceQuality | str) -> ObservationEvidenceQuality:
    if isinstance(value, ObservationEvidenceQuality):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("observation evidence quality must not be blank")
        return ObservationEvidenceQuality(stripped)
    raise TypeError(f"unsupported observation evidence quality: {value!r}")


def observation_source_kind_fetches(_: ObservationSkillSourceKind | str) -> bool:
    normalize_observation_source_kind(_)
    return False


def observation_focus_kind_creates_next_stage_artifact(_: ObservationFocusKind | str) -> bool:
    normalize_observation_focus_kind(_)
    return False


def observation_finding_kind_is_certification(_: ObservationFindingKind | str) -> bool:
    normalize_observation_finding_kind(_)
    return False


@dataclass(frozen=True)
class ObservationTargetRef:
    target_ref_id: str
    target_id: str
    target_kind: str | None
    source_kind: ObservationSkillSourceKind | str
    source_ref: str | None = None
    display_name: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("target_ref_id", self.target_ref_id)
        _require_non_blank("target_id", self.target_id)
        normalize_observation_source_kind(self.source_kind)
        if self.source_ref is not None and not isinstance(self.source_ref, str):
            raise TypeError("source_ref must be str | None")

    @property
    def accesses_target(self) -> bool:
        return False

    @property
    def fetches_source_ref(self) -> bool:
        return False


@dataclass(frozen=True)
class ObservationArtifactRef:
    artifact_ref_id: str
    artifact_kind: str
    artifact_id: str
    source_kind: ObservationSkillSourceKind | str
    source_version: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("artifact_ref_id", self.artifact_ref_id)
        _require_non_blank("artifact_kind", self.artifact_kind)
        _require_non_blank("artifact_id", self.artifact_id)
        normalize_observation_source_kind(self.source_kind)

    @property
    def fetches_artifact(self) -> bool:
        return False


@dataclass(frozen=True)
class ObservationEvidenceRef:
    evidence_ref_id: str
    evidence_kind: str
    evidence_id: str
    source_artifact_ref_id: str | None
    quality: ObservationEvidenceQuality | str
    conflict_notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("evidence_ref_id", self.evidence_ref_id)
        _require_non_blank("evidence_kind", self.evidence_kind)
        _require_non_blank("evidence_id", self.evidence_id)
        quality = normalize_observation_evidence_quality(self.quality)
        _validate_string_list("conflict_notes", self.conflict_notes)
        if quality is ObservationEvidenceQuality.CONFLICTING and not self.conflict_notes:
            raise ValueError("conflicting evidence quality requires conflict_notes")

    @property
    def runtime_trust(self) -> bool:
        return False


@dataclass(frozen=True)
class ObservationSkillInput:
    observation_input_id: str
    triad_input_id: str | None
    requested_focus: list[ObservationFocusKind | str]
    target_refs: list[ObservationTargetRef]
    artifact_refs: list[ObservationArtifactRef]
    evidence_refs: list[ObservationEvidenceRef]
    task_summary: str
    source_version: str
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(V0311_REQUIRED_PROHIBITED_RUNTIME_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("observation_input_id", self.observation_input_id)
        _require_non_blank("task_summary", self.task_summary)
        _require_non_blank("source_version", self.source_version)
        if not isinstance(self.requested_focus, list):
            raise TypeError("requested_focus must be list[ObservationFocusKind | str]")
        for focus in self.requested_focus:
            normalize_observation_focus_kind(focus)
        _validate_object_list("target_refs", self.target_refs, ObservationTargetRef)
        _validate_object_list("artifact_refs", self.artifact_refs, ObservationArtifactRef)
        _validate_object_list("evidence_refs", self.evidence_refs, ObservationEvidenceRef)
        _validate_prohibited_actions(self.prohibited_runtime_actions)
        if _metadata_flag_true(self.metadata, {"execution_request", "external_scan", "source_ref_fetch", "url_fetch", "read_only_tool_execution"}):
            raise ValueError("ObservationSkillInput must not imply execution request, external scan, source_ref fetch, or tool execution")

    @property
    def is_execution_request(self) -> bool:
        return False


@dataclass(frozen=True)
class ObservationFinding:
    finding_id: str
    finding_kind: ObservationFindingKind | str
    focus_kind: ObservationFocusKind | str
    target_id: str | None
    artifact_ref_ids: list[str]
    evidence_ref_ids: list[str]
    summary: str
    risk_posture: ObservationRiskPosture | str = ObservationRiskPosture.UNKNOWN
    evidence_quality: ObservationEvidenceQuality | str = ObservationEvidenceQuality.UNKNOWN
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        normalize_observation_finding_kind(self.finding_kind)
        normalize_observation_focus_kind(self.focus_kind)
        _validate_string_list("artifact_ref_ids", self.artifact_ref_ids)
        _validate_string_list("evidence_ref_ids", self.evidence_ref_ids)
        _require_non_blank("summary", self.summary)
        risk = normalize_observation_risk_posture(self.risk_posture)
        quality = normalize_observation_evidence_quality(self.evidence_quality)
        _validate_string_list("assumptions", self.assumptions)
        _validate_string_list("limitations", self.limitations)
        if not self.evidence_ref_ids:
            if quality not in {
                ObservationEvidenceQuality.UNKNOWN,
                ObservationEvidenceQuality.NONE,
                ObservationEvidenceQuality.WEAK,
                ObservationEvidenceQuality.BLOCKED,
            }:
                raise ValueError("evidence_quality must be conservative when evidence_ref_ids is empty")
            if risk in {ObservationRiskPosture.LOW, ObservationRiskPosture.MEDIUM, ObservationRiskPosture.HIGH, ObservationRiskPosture.CRITICAL}:
                raise ValueError("risk_posture must be conservative when evidence_ref_ids is empty")
        if _metadata_flag_true(self.metadata, {"certification", "permission", "digestion_candidate", "dominion_target", "dominion_authority"}):
            raise ValueError("ObservationFinding must not imply certification, permission, digestion candidate, or dominion target")

    @property
    def is_certification(self) -> bool:
        return False

    @property
    def grants_permission(self) -> bool:
        return False

    @property
    def creates_digestion_or_dominion_artifact(self) -> bool:
        return False


@dataclass(frozen=True)
class ObservationGap:
    gap_id: str
    gap_kind: ObservationGapKind | str
    target_id: str | None
    artifact_ref_ids: list[str]
    description: str
    blocks_v0312: bool
    recommended_followup: str | None = None
    evidence_ref_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("gap_id", self.gap_id)
        normalize_observation_gap_kind(self.gap_kind)
        _validate_string_list("artifact_ref_ids", self.artifact_ref_ids)
        _require_non_blank("description", self.description)
        if not isinstance(self.blocks_v0312, bool):
            raise TypeError("blocks_v0312 must be bool")
        _validate_string_list("evidence_ref_ids", self.evidence_ref_ids)

    @property
    def executes_remediation(self) -> bool:
        return False


@dataclass(frozen=True)
class ObservationRiskSignal:
    risk_signal_id: str
    target_id: str | None
    signal_name: str
    posture: ObservationRiskPosture | str
    related_finding_ids: list[str] = field(default_factory=list)
    related_gap_ids: list[str] = field(default_factory=list)
    evidence_ref_ids: list[str] = field(default_factory=list)
    recommended_boundary: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_signal_id", self.risk_signal_id)
        _require_non_blank("signal_name", self.signal_name)
        posture = normalize_observation_risk_posture(self.posture)
        _validate_string_list("related_finding_ids", self.related_finding_ids)
        _validate_string_list("related_gap_ids", self.related_gap_ids)
        _validate_string_list("evidence_ref_ids", self.evidence_ref_ids)
        if posture in {ObservationRiskPosture.HIGH, ObservationRiskPosture.CRITICAL, ObservationRiskPosture.BLOCKED} and not (
            self.recommended_boundary or self.evidence_ref_ids
        ):
            raise ValueError("high/critical/blocked risk posture requires recommended_boundary or evidence_ref_ids")

    @property
    def grants_authority(self) -> bool:
        return False


@dataclass(frozen=True)
class ObservationSkillOutput:
    observation_output_id: str
    observation_input_id: str
    skill_contract_id: str | None
    status: str
    findings: list[ObservationFinding]
    gaps: list[ObservationGap]
    risk_signals: list[ObservationRiskSignal]
    observed_target_ref_ids: list[str] = field(default_factory=list)
    observed_artifact_ref_ids: list[str] = field(default_factory=list)
    evidence_ref_ids: list[str] = field(default_factory=list)
    ready_for_v0312_observation_report: bool = False
    ready_for_execution: bool = False
    ready_for_skill_activation: bool = False
    ready_for_external_scan: bool = False
    blocked_reasons: list[str] = field(default_factory=list)
    no_op_reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("observation_output_id", self.observation_output_id)
        _require_non_blank("observation_input_id", self.observation_input_id)
        _require_non_blank("status", self.status)
        _validate_object_list("findings", self.findings, ObservationFinding)
        _validate_object_list("gaps", self.gaps, ObservationGap)
        _validate_object_list("risk_signals", self.risk_signals, ObservationRiskSignal)
        _validate_string_list("observed_target_ref_ids", self.observed_target_ref_ids)
        _validate_string_list("observed_artifact_ref_ids", self.observed_artifact_ref_ids)
        _validate_string_list("evidence_ref_ids", self.evidence_ref_ids)
        _validate_string_list("blocked_reasons", self.blocked_reasons)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.1")
        if self.ready_for_skill_activation is not False:
            raise ValueError("ready_for_skill_activation must always be False in v0.31.1")
        if self.ready_for_external_scan is not False:
            raise ValueError("ready_for_external_scan must always be False in v0.31.1")
        if self.ready_for_v0312_observation_report and any(gap.blocks_v0312 for gap in self.gaps):
            raise ValueError("ready_for_v0312_observation_report can be True only when no gaps block v0.31.2")
        if _metadata_flag_true(self.metadata, {"digestion_candidate", "dominion_target", "active_artifact_registration"}):
            raise ValueError("ObservationSkillOutput must not imply digestion candidate or dominion target creation")

    @property
    def creates_digestion_candidate(self) -> bool:
        return False

    @property
    def creates_dominion_target(self) -> bool:
        return False


@dataclass(frozen=True)
class ObservationSkillNoOpDecision:
    no_op_id: str
    observation_input_id: str
    reason: str
    blocked_reasons: list[str] = field(default_factory=list)
    safe_alternatives: list[str] = field(default_factory=list)
    evidence_ref_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("no_op_id", self.no_op_id)
        _require_non_blank("observation_input_id", self.observation_input_id)
        _require_non_blank("reason", self.reason)
        _validate_string_list("blocked_reasons", self.blocked_reasons)
        _validate_string_list("safe_alternatives", self.safe_alternatives)
        _validate_string_list("evidence_ref_ids", self.evidence_ref_ids)

    @property
    def is_failure(self) -> bool:
        return False

    @property
    def executes_anything(self) -> bool:
        return False


@dataclass(frozen=True)
class ObservationSkillRunPreview:
    run_preview_id: str
    observation_input_id: str
    planned_steps: list[str]
    expected_artifacts: list[str]
    explicitly_not_performed: list[str]
    no_execution_guarantee: bool = True
    no_external_scan_guarantee: bool = True
    no_tool_execution_guarantee: bool = True
    no_registry_mutation_guarantee: bool = True
    no_memory_mutation_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        _require_non_blank("observation_input_id", self.observation_input_id)
        _validate_string_list("planned_steps", self.planned_steps)
        _validate_string_list("expected_artifacts", self.expected_artifacts)
        _validate_string_list("explicitly_not_performed", self.explicitly_not_performed)
        for name in (
            "no_execution_guarantee",
            "no_external_scan_guarantee",
            "no_tool_execution_guarantee",
            "no_registry_mutation_guarantee",
            "no_memory_mutation_guarantee",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.31.1")
        if _metadata_flag_true(self.metadata, {"executes_run", "external_scan", "tool_execution"}):
            raise ValueError("ObservationSkillRunPreview must not imply execution")

    @property
    def executes_run(self) -> bool:
        return False


@dataclass(frozen=True)
class ObservationSkillFoundationReport:
    foundation_report_id: str
    version: str
    observation_contract_ref: str | None
    supported_source_kinds: list[ObservationSkillSourceKind | str]
    supported_focus_kinds: list[ObservationFocusKind | str]
    supported_output_artifact_kinds: list[str]
    prohibited_runtime_actions: list[str]
    ready_for_v0312_observation_report_capability_map: bool
    ready_for_execution: bool = False
    ready_for_skill_activation: bool = False
    ready_for_external_scan: bool = False
    summary: str = ""
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("foundation_report_id", self.foundation_report_id)
        _validate_version_includes_v0311(self.version)
        if not isinstance(self.supported_source_kinds, list):
            raise TypeError("supported_source_kinds must be list[ObservationSkillSourceKind | str]")
        if not isinstance(self.supported_focus_kinds, list):
            raise TypeError("supported_focus_kinds must be list[ObservationFocusKind | str]")
        for source_kind in self.supported_source_kinds:
            normalize_observation_source_kind(source_kind)
        for focus_kind in self.supported_focus_kinds:
            normalize_observation_focus_kind(focus_kind)
        _validate_string_list("supported_output_artifact_kinds", self.supported_output_artifact_kinds)
        _validate_prohibited_actions(self.prohibited_runtime_actions)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.1")
        if self.ready_for_skill_activation is not False:
            raise ValueError("ready_for_skill_activation must always be False in v0.31.1")
        if self.ready_for_external_scan is not False:
            raise ValueError("ready_for_external_scan must always be False in v0.31.1")
        _require_non_blank("summary", self.summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("withdrawal_conditions", self.withdrawal_conditions)

    @property
    def runtime_enablement(self) -> bool:
        return False


@dataclass(frozen=True)
class V0311ReadinessReport:
    report_id: str
    version: str
    observation_foundation_report_id: str
    summary: str
    ready_for_v0312_observation_report_capability_map: bool
    ready_for_execution: bool = False
    ready_for_skill_activation: bool = False
    ready_for_external_scan: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(V0311_PROHIBITED_UNTIL_LATER_GATE))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0311(self.version)
        _require_non_blank("observation_foundation_report_id", self.observation_foundation_report_id)
        _require_non_blank("summary", self.summary)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.1")
        if self.ready_for_skill_activation is not False:
            raise ValueError("ready_for_skill_activation must always be False in v0.31.1")
        if self.ready_for_external_scan is not False:
            raise ValueError("ready_for_external_scan must always be False in v0.31.1")
        for name in (
            "completed_items",
            "blocked_items",
            "future_track_items",
            "prohibited_until_later_gate",
            "evidence_refs",
            "withdrawal_conditions",
        ):
            _validate_string_list(name, getattr(self, name))
        missing = set(V0311_PROHIBITED_UNTIL_LATER_GATE) - set(self.prohibited_until_later_gate)
        if missing:
            raise ValueError(f"prohibited_until_later_gate missing required items: {sorted(missing)}")

    @property
    def runtime_enablement(self) -> bool:
        return False


def build_observation_target_ref(
    target_ref_id: str,
    target_id: str,
    source_kind: ObservationSkillSourceKind | str,
    target_kind: str | None = None,
    source_ref: str | None = None,
    display_name: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> ObservationTargetRef:
    return ObservationTargetRef(
        target_ref_id=target_ref_id,
        target_id=target_id,
        target_kind=target_kind,
        source_kind=source_kind,
        source_ref=source_ref,
        display_name=display_name,
        metadata=dict(metadata or {}),
    )


def build_observation_artifact_ref(
    artifact_ref_id: str,
    artifact_kind: str,
    artifact_id: str,
    source_kind: ObservationSkillSourceKind | str,
    source_version: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> ObservationArtifactRef:
    return ObservationArtifactRef(
        artifact_ref_id=artifact_ref_id,
        artifact_kind=artifact_kind,
        artifact_id=artifact_id,
        source_kind=source_kind,
        source_version=source_version,
        metadata=dict(metadata or {}),
    )


def build_observation_evidence_ref(
    evidence_ref_id: str,
    evidence_kind: str,
    evidence_id: str,
    quality: ObservationEvidenceQuality | str,
    source_artifact_ref_id: str | None = None,
    conflict_notes: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ObservationEvidenceRef:
    return ObservationEvidenceRef(
        evidence_ref_id=evidence_ref_id,
        evidence_kind=evidence_kind,
        evidence_id=evidence_id,
        source_artifact_ref_id=source_artifact_ref_id,
        quality=quality,
        conflict_notes=list(conflict_notes or []),
        metadata=dict(metadata or {}),
    )


def build_observation_skill_input(
    observation_input_id: str,
    task_summary: str,
    source_version: str,
    requested_focus: list[ObservationFocusKind | str] | None = None,
    target_refs: list[ObservationTargetRef] | None = None,
    artifact_refs: list[ObservationArtifactRef] | None = None,
    evidence_refs: list[ObservationEvidenceRef] | None = None,
    triad_input_id: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> ObservationSkillInput:
    return ObservationSkillInput(
        observation_input_id=observation_input_id,
        triad_input_id=triad_input_id,
        requested_focus=list(requested_focus or []),
        target_refs=list(target_refs or []),
        artifact_refs=list(artifact_refs or []),
        evidence_refs=list(evidence_refs or []),
        task_summary=task_summary,
        source_version=source_version,
        prohibited_runtime_actions=list(V0311_REQUIRED_PROHIBITED_RUNTIME_ACTIONS),
        metadata=dict(metadata or {}),
    )


def build_observation_finding(
    finding_id: str,
    finding_kind: ObservationFindingKind | str,
    focus_kind: ObservationFocusKind | str,
    summary: str,
    target_id: str | None = None,
    artifact_ref_ids: list[str] | None = None,
    evidence_ref_ids: list[str] | None = None,
    risk_posture: ObservationRiskPosture | str = ObservationRiskPosture.UNKNOWN,
    evidence_quality: ObservationEvidenceQuality | str = ObservationEvidenceQuality.UNKNOWN,
    assumptions: list[str] | None = None,
    limitations: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ObservationFinding:
    return ObservationFinding(
        finding_id=finding_id,
        finding_kind=finding_kind,
        focus_kind=focus_kind,
        target_id=target_id,
        artifact_ref_ids=list(artifact_ref_ids or []),
        evidence_ref_ids=list(evidence_ref_ids or []),
        summary=summary,
        risk_posture=risk_posture,
        evidence_quality=evidence_quality,
        assumptions=list(assumptions or []),
        limitations=list(limitations or []),
        metadata=dict(metadata or {}),
    )


def build_observation_gap(
    gap_id: str,
    gap_kind: ObservationGapKind | str,
    description: str,
    blocks_v0312: bool,
    target_id: str | None = None,
    artifact_ref_ids: list[str] | None = None,
    recommended_followup: str | None = None,
    evidence_ref_ids: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ObservationGap:
    return ObservationGap(
        gap_id=gap_id,
        gap_kind=gap_kind,
        target_id=target_id,
        artifact_ref_ids=list(artifact_ref_ids or []),
        description=description,
        blocks_v0312=blocks_v0312,
        recommended_followup=recommended_followup,
        evidence_ref_ids=list(evidence_ref_ids or []),
        metadata=dict(metadata or {}),
    )


def build_observation_risk_signal(
    risk_signal_id: str,
    signal_name: str,
    posture: ObservationRiskPosture | str,
    target_id: str | None = None,
    related_finding_ids: list[str] | None = None,
    related_gap_ids: list[str] | None = None,
    evidence_ref_ids: list[str] | None = None,
    recommended_boundary: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> ObservationRiskSignal:
    return ObservationRiskSignal(
        risk_signal_id=risk_signal_id,
        target_id=target_id,
        signal_name=signal_name,
        posture=posture,
        related_finding_ids=list(related_finding_ids or []),
        related_gap_ids=list(related_gap_ids or []),
        evidence_ref_ids=list(evidence_ref_ids or []),
        recommended_boundary=recommended_boundary,
        metadata=dict(metadata or {}),
    )


def build_observation_skill_output(
    observation_output_id: str,
    observation_input_id: str,
    status: str,
    findings: list[ObservationFinding] | None = None,
    gaps: list[ObservationGap] | None = None,
    risk_signals: list[ObservationRiskSignal] | None = None,
    skill_contract_id: str | None = None,
    observed_target_ref_ids: list[str] | None = None,
    observed_artifact_ref_ids: list[str] | None = None,
    evidence_ref_ids: list[str] | None = None,
    ready_for_v0312_observation_report: bool = False,
    blocked_reasons: list[str] | None = None,
    no_op_reason: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> ObservationSkillOutput:
    return ObservationSkillOutput(
        observation_output_id=observation_output_id,
        observation_input_id=observation_input_id,
        skill_contract_id=skill_contract_id,
        status=status,
        findings=list(findings or []),
        gaps=list(gaps or []),
        risk_signals=list(risk_signals or []),
        observed_target_ref_ids=list(observed_target_ref_ids or []),
        observed_artifact_ref_ids=list(observed_artifact_ref_ids or []),
        evidence_ref_ids=list(evidence_ref_ids or []),
        ready_for_v0312_observation_report=ready_for_v0312_observation_report,
        ready_for_execution=False,
        ready_for_skill_activation=False,
        ready_for_external_scan=False,
        blocked_reasons=list(blocked_reasons or []),
        no_op_reason=no_op_reason,
        metadata=dict(metadata or {}),
    )


def build_observation_no_op_decision(
    no_op_id: str,
    observation_input_id: str,
    reason: str,
    blocked_reasons: list[str] | None = None,
    safe_alternatives: list[str] | None = None,
    evidence_ref_ids: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ObservationSkillNoOpDecision:
    return ObservationSkillNoOpDecision(
        no_op_id=no_op_id,
        observation_input_id=observation_input_id,
        reason=reason,
        blocked_reasons=list(blocked_reasons or []),
        safe_alternatives=list(safe_alternatives or []),
        evidence_ref_ids=list(evidence_ref_ids or []),
        metadata=dict(metadata or {}),
    )


def build_observation_run_preview(
    run_preview_id: str,
    observation_input_id: str,
    planned_steps: list[str] | None = None,
    expected_artifacts: list[str] | None = None,
    explicitly_not_performed: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ObservationSkillRunPreview:
    return ObservationSkillRunPreview(
        run_preview_id=run_preview_id,
        observation_input_id=observation_input_id,
        planned_steps=list(planned_steps or ["validate available refs", "structure observation metadata"]),
        expected_artifacts=list(expected_artifacts or ["ObservationSkillOutput"]),
        explicitly_not_performed=list(
            explicitly_not_performed
            or [
                "external_scan",
                "source_ref_fetch",
                "url_fetch",
                "read_only_tool_execution",
                "skill_activation",
                "registry_mutation",
                "memory_mutation",
            ]
        ),
        metadata=dict(metadata or {}),
    )


def build_observation_skill_foundation_report(
    observation_contract_ref: str | None = "internal_triad_skill_contract:observation:v0.31.0",
    ready_for_v0312_observation_report_capability_map: bool = True,
) -> ObservationSkillFoundationReport:
    return ObservationSkillFoundationReport(
        foundation_report_id="observation_skill_foundation_report:v0.31.1",
        version=V0311_VERSION,
        observation_contract_ref=observation_contract_ref,
        supported_source_kinds=[kind for kind in ObservationSkillSourceKind],
        supported_focus_kinds=[kind for kind in ObservationFocusKind],
        supported_output_artifact_kinds=[
            "observation_input",
            "observation_finding",
            "observation_gap",
            "observation_risk_signal",
            "observation_skill_output",
            "observation_run_preview",
            "observation_no_op_decision",
        ],
        prohibited_runtime_actions=list(V0311_REQUIRED_PROHIBITED_RUNTIME_ACTIONS),
        ready_for_v0312_observation_report_capability_map=ready_for_v0312_observation_report_capability_map,
        ready_for_execution=False,
        ready_for_skill_activation=False,
        ready_for_external_scan=False,
        summary="Observation Skill Foundation model layer for next-stage report and capability-map design only.",
        evidence_refs=["v0.31.0 ObservationSkillContract", "v0.30.9 ExternalDominionV031HandoffPacket"],
        withdrawal_conditions=[
            "Observation Skill is treated as external scanning",
            "source_ref fetch or URL fetch is introduced",
            "ready_for_execution, ready_for_skill_activation, or ready_for_external_scan becomes true",
            "observation output is treated as digestion candidate or dominion target",
        ],
        metadata={"foundation_is_runtime_enablement": False},
    )


def build_v0311_readiness_report(
    foundation_report: ObservationSkillFoundationReport,
) -> V0311ReadinessReport:
    return V0311ReadinessReport(
        report_id="v0311_readiness_report:observation_skill_foundation",
        version=V0311_VERSION,
        observation_foundation_report_id=foundation_report.foundation_report_id,
        summary="v0.31.1 is ready for v0.31.2 Observation Report / Capability Map design only; not execution.",
        ready_for_v0312_observation_report_capability_map=foundation_report.ready_for_v0312_observation_report_capability_map,
        ready_for_execution=False,
        ready_for_skill_activation=False,
        ready_for_external_scan=False,
        completed_items=[
            "observation source taxonomy",
            "observation focus taxonomy",
            "observation finding/gap/risk/evidence models",
            "observation input/output/no-op/run-preview models",
            foundation_report.foundation_report_id,
        ],
        blocked_items=[],
        future_track_items=[
            "external scan",
            "source_ref fetch",
            "read-only tool execution",
            "digestion candidate creation",
            "dominion target creation",
        ],
        evidence_refs=list(foundation_report.evidence_refs),
        withdrawal_conditions=list(foundation_report.withdrawal_conditions),
        metadata={"readiness_report_is_runtime_enablement": False},
    )


def observation_input_preserves_no_execution(observation_input: ObservationSkillInput) -> bool:
    return (
        observation_input.is_execution_request is False
        and not (set(V0311_REQUIRED_PROHIBITED_RUNTIME_ACTIONS) - set(observation_input.prohibited_runtime_actions))
    )


def observation_output_preserves_no_execution(output: ObservationSkillOutput) -> bool:
    return (
        output.ready_for_execution is False
        and output.ready_for_skill_activation is False
        and output.ready_for_external_scan is False
        and output.creates_digestion_candidate is False
        and output.creates_dominion_target is False
    )


def observation_run_preview_preserves_no_execution(preview: ObservationSkillRunPreview) -> bool:
    return (
        preview.no_execution_guarantee is True
        and preview.no_external_scan_guarantee is True
        and preview.no_tool_execution_guarantee is True
        and preview.no_registry_mutation_guarantee is True
        and preview.no_memory_mutation_guarantee is True
        and preview.executes_run is False
    )


def observation_foundation_is_not_runtime_ready(report: ObservationSkillFoundationReport | V0311ReadinessReport) -> bool:
    return (
        report.ready_for_execution is False
        and report.ready_for_skill_activation is False
        and report.ready_for_external_scan is False
        and report.runtime_enablement is False
    )

