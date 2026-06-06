from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from chanta_core.internal_triad.boundaries import _require_non_blank, _validate_string_list
from chanta_core.internal_triad.skill_kinds import V0310_TRACK


V0317_VERSION = "v0.31.7"
V0317_RELEASE_NAME = "v0.31.7 Triad Skill OCEL Trace Integration"
V0317_TRACK = V0310_TRACK

V0317_PROHIBITED_UNTIL_LATER_GATE = [
    "ocel_event_emission",
    "ocel_object_persistence",
    "ocel_relation_persistence",
    "runtime_trace_write",
    "log_write",
    "database_write",
    "registry_mutation",
    "memory_mutation",
    "external_execution",
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
]


class TriadOCELTraceEventKind(StrEnum):
    TRIAD_SKILL_CONTRACT_CREATED = "triad_skill_contract_created"
    TRIAD_SKILL_INPUT_RECEIVED = "triad_skill_input_received"
    TRIAD_SKILL_RESULT_RECORDED = "triad_skill_result_recorded"
    OBSERVATION_SKILL_STARTED = "observation_skill_started"
    OBSERVATION_TARGET_REF_RECORDED = "observation_target_ref_recorded"
    OBSERVATION_ARTIFACT_REF_RECORDED = "observation_artifact_ref_recorded"
    OBSERVATION_EVIDENCE_REF_RECORDED = "observation_evidence_ref_recorded"
    OBSERVATION_FINDING_RECORDED = "observation_finding_recorded"
    OBSERVATION_GAP_RECORDED = "observation_gap_recorded"
    OBSERVATION_RISK_SIGNAL_RECORDED = "observation_risk_signal_recorded"
    OBSERVATION_REPORT_CREATED = "observation_report_created"
    CAPABILITY_MAP_CREATED = "capability_map_created"
    DIGESTION_SKILL_STARTED = "digestion_skill_started"
    DIGESTION_SOURCE_REF_RECORDED = "digestion_source_ref_recorded"
    DIGESTION_PATTERN_SIGNAL_RECORDED = "digestion_pattern_signal_recorded"
    DIGESTION_FINDING_RECORDED = "digestion_finding_recorded"
    DIGESTION_BLOCKER_RECORDED = "digestion_blocker_recorded"
    DIGESTION_ROUTE_DECISION_RECORDED = "digestion_route_decision_recorded"
    INTERNAL_CANDIDATE_CREATED = "internal_candidate_created"
    INTERNALIZATION_PLAN_CREATED = "internalization_plan_created"
    DOMINION_SKILL_STARTED = "dominion_skill_started"
    DOMINION_BOUNDARY_SIGNAL_RECORDED = "dominion_boundary_signal_recorded"
    DOMINION_GOVERNANCE_FINDING_RECORDED = "dominion_governance_finding_recorded"
    DOMINION_BLOCKER_RECORDED = "dominion_blocker_recorded"
    DOMINION_ROUTE_DECISION_RECORDED = "dominion_route_decision_recorded"
    DOMINION_TARGET_RECORDED = "dominion_target_recorded"
    DOMINION_DECISION_RECORDED = "dominion_decision_recorded"
    DOMINION_FUTURE_GATE_RECORDED = "dominion_future_gate_recorded"
    DOMINION_NO_OP_RECORDED = "dominion_no_op_recorded"
    TRIAD_NO_OP_RECORDED = "triad_no_op_recorded"
    TRIAD_SKILL_BLOCKED = "triad_skill_blocked"
    TRIAD_SKILL_COMPLETED = "triad_skill_completed"
    UNKNOWN = "unknown"


class TriadOCELObjectTypeKind(StrEnum):
    TRIAD_SKILL = "triad_skill"
    TRIAD_SKILL_CONTRACT = "triad_skill_contract"
    TRIAD_SKILL_RUN = "triad_skill_run"
    TRIAD_SKILL_INPUT = "triad_skill_input"
    TRIAD_SKILL_RESULT = "triad_skill_result"
    OBSERVATION_TARGET_REF = "observation_target_ref"
    OBSERVATION_ARTIFACT_REF = "observation_artifact_ref"
    OBSERVATION_EVIDENCE_REF = "observation_evidence_ref"
    OBSERVATION_FINDING = "observation_finding"
    OBSERVATION_GAP = "observation_gap"
    OBSERVATION_RISK_SIGNAL = "observation_risk_signal"
    OBSERVATION_REPORT = "observation_report"
    CAPABILITY_MAP = "capability_map"
    CAPABILITY_MAP_ENTRY = "capability_map_entry"
    DIGESTION_SOURCE_REF = "digestion_source_ref"
    DIGESTION_PATTERN_SIGNAL = "digestion_pattern_signal"
    DIGESTION_FINDING = "digestion_finding"
    DIGESTION_BLOCKER = "digestion_blocker"
    DIGESTION_ROUTE_DECISION = "digestion_route_decision"
    INTERNAL_CANDIDATE = "internal_candidate"
    INTERNAL_CANDIDATE_SET = "internal_candidate_set"
    INTERNALIZATION_PLAN = "internalization_plan"
    INTERNALIZATION_PLAN_STEP = "internalization_plan_step"
    DOMINION_SOURCE_REF = "dominion_source_ref"
    DOMINION_BOUNDARY_SIGNAL = "dominion_boundary_signal"
    DOMINION_GOVERNANCE_FINDING = "dominion_governance_finding"
    DOMINION_BLOCKER = "dominion_blocker"
    DOMINION_ROUTE_DECISION = "dominion_route_decision"
    DOMINION_TARGET = "dominion_target"
    DOMINION_CONTROL_BOUNDARY = "dominion_control_boundary"
    DOMINION_DECISION = "dominion_decision"
    DOMINION_FUTURE_GATE = "dominion_future_gate"
    DOMINION_NO_OP = "dominion_no_op"
    FUTURE_GATE_ITEM = "future_gate_item"
    NO_OP_DECISION = "no_op_decision"
    UNKNOWN = "unknown"


class TriadOCELRelationTypeKind(StrEnum):
    CONSUMES = "consumes"
    PRODUCES = "produces"
    REFERENCES = "references"
    DERIVES_FROM = "derives_from"
    MAPS_TO = "maps_to"
    CLASSIFIES = "classifies"
    BLOCKS = "blocks"
    ROUTES_TO = "routes_to"
    REQUIRES = "requires"
    PROHIBITS = "prohibits"
    SUPPORTS = "supports"
    EVIDENCES = "evidences"
    MITIGATES = "mitigates"
    SUPERSEDES = "supersedes"
    HANDS_OFF_TO = "hands_off_to"
    UNKNOWN = "unknown"


class TriadOCELArtifactKind(StrEnum):
    TRIAD_SKILL_CONTRACT = "triad_skill_contract"
    TRIAD_SKILL_INPUT_ENVELOPE = "triad_skill_input_envelope"
    TRIAD_SKILL_RESULT_ENVELOPE = "triad_skill_result_envelope"
    OBSERVATION_SKILL_INPUT = "observation_skill_input"
    OBSERVATION_SKILL_OUTPUT = "observation_skill_output"
    INTERNAL_OBSERVATION_REPORT = "internal_observation_report"
    INTERNAL_CAPABILITY_MAP = "internal_capability_map"
    OBSERVATION_GAP_REGISTER = "observation_gap_register"
    OBSERVATION_RISK_MAP = "observation_risk_map"
    OBSERVATION_EVIDENCE_TABLE = "observation_evidence_table"
    DIGESTION_SKILL_INPUT = "digestion_skill_input"
    DIGESTIBLE_PATTERN_SIGNAL = "digestible_pattern_signal"
    DIGESTION_FINDING = "digestion_finding"
    DIGESTION_BLOCKER = "digestion_blocker"
    DIGESTION_ROUTE_DECISION = "digestion_route_decision"
    DIGESTION_SKILL_OUTPUT = "digestion_skill_output"
    INTERNAL_CANDIDATE = "internal_candidate"
    INTERNAL_CANDIDATE_SET = "internal_candidate_set"
    INTERNALIZATION_PLAN = "internalization_plan"
    DOMINION_SKILL_INPUT = "dominion_skill_input"
    DOMINION_CONTROL_BOUNDARY_SIGNAL = "dominion_control_boundary_signal"
    DOMINION_GOVERNANCE_FINDING = "dominion_governance_finding"
    DOMINION_BLOCKER = "dominion_blocker"
    DOMINION_ROUTE_DECISION = "dominion_route_decision"
    DOMINION_SKILL_OUTPUT = "dominion_skill_output"
    INTERNAL_DOMINION_TARGET = "internal_dominion_target"
    INTERNAL_DOMINION_DECISION = "internal_dominion_decision"
    DOMINION_CONTROL_BOUNDARY = "dominion_control_boundary"
    DOMINION_FUTURE_GATE = "dominion_future_gate"
    DOMINION_NO_OP_DECISION = "dominion_no_op_decision"
    READINESS_REPORT = "readiness_report"
    UNKNOWN = "unknown"


class TriadOCELTracePlanStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    PLAN_READY = "plan_ready"
    PLAN_READY_WITH_GAPS = "plan_ready_with_gaps"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class TriadOCELTraceCoverageStatus(StrEnum):
    UNKNOWN = "unknown"
    NOT_STARTED = "not_started"
    PARTIAL = "partial"
    COVERED = "covered"
    COVERED_WITH_GAPS = "covered_with_gaps"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


def _metadata_flag_true(metadata: dict[str, Any], names: set[str]) -> bool:
    return isinstance(metadata, dict) and any(metadata.get(name) is True for name in names)


def _validate_version_includes_v0317(version: str) -> None:
    _require_non_blank("version", version)
    if V0317_VERSION not in version:
        raise ValueError("version must include v0.31.7")


def _validate_object_list(name: str, values: list[Any], expected_type: type) -> None:
    if not isinstance(values, list) or not all(isinstance(item, expected_type) for item in values):
        raise TypeError(f"{name} must be list[{expected_type.__name__}]")


def _validate_non_negative(name: str, value: int) -> None:
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be >= 0")


def _validate_enum_list(name: str, values: list[Any], normalizer: Any) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        normalizer(value)


def normalize_triad_ocel_event_kind(value: TriadOCELTraceEventKind | str) -> TriadOCELTraceEventKind:
    if isinstance(value, TriadOCELTraceEventKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("triad OCEL event kind must not be blank")
        return TriadOCELTraceEventKind(stripped)
    raise TypeError(f"unsupported triad OCEL event kind: {value!r}")


def normalize_triad_ocel_object_type(value: TriadOCELObjectTypeKind | str) -> TriadOCELObjectTypeKind:
    if isinstance(value, TriadOCELObjectTypeKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("triad OCEL object type must not be blank")
        return TriadOCELObjectTypeKind(stripped)
    raise TypeError(f"unsupported triad OCEL object type: {value!r}")


def normalize_triad_ocel_relation_type(value: TriadOCELRelationTypeKind | str) -> TriadOCELRelationTypeKind:
    if isinstance(value, TriadOCELRelationTypeKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("triad OCEL relation type must not be blank")
        return TriadOCELRelationTypeKind(stripped)
    raise TypeError(f"unsupported triad OCEL relation type: {value!r}")


def normalize_triad_ocel_artifact_kind(value: TriadOCELArtifactKind | str) -> TriadOCELArtifactKind:
    if isinstance(value, TriadOCELArtifactKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("triad OCEL artifact kind must not be blank")
        return TriadOCELArtifactKind(stripped)
    raise TypeError(f"unsupported triad OCEL artifact kind: {value!r}")


def normalize_triad_ocel_trace_plan_status(value: TriadOCELTracePlanStatus | str) -> TriadOCELTracePlanStatus:
    if isinstance(value, TriadOCELTracePlanStatus):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("triad OCEL trace plan status must not be blank")
        return TriadOCELTracePlanStatus(stripped)
    raise TypeError(f"unsupported triad OCEL trace plan status: {value!r}")


def normalize_triad_ocel_trace_coverage_status(value: TriadOCELTraceCoverageStatus | str) -> TriadOCELTraceCoverageStatus:
    if isinstance(value, TriadOCELTraceCoverageStatus):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("triad OCEL trace coverage status must not be blank")
        return TriadOCELTraceCoverageStatus(stripped)
    raise TypeError(f"unsupported triad OCEL trace coverage status: {value!r}")


def triad_ocel_event_kind_emits(_: TriadOCELTraceEventKind | str) -> bool:
    normalize_triad_ocel_event_kind(_)
    return False


def triad_ocel_object_type_persists(_: TriadOCELObjectTypeKind | str) -> bool:
    normalize_triad_ocel_object_type(_)
    return False


def triad_ocel_relation_type_persists(_: TriadOCELRelationTypeKind | str) -> bool:
    normalize_triad_ocel_relation_type(_)
    return False


@dataclass(frozen=True)
class TriadOCELObjectRef:
    object_ref_id: str
    object_type: TriadOCELObjectTypeKind | str
    object_id: str
    source_artifact_kind: TriadOCELArtifactKind | str
    source_artifact_id: str | None = None
    display_name: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("object_ref_id", self.object_ref_id)
        normalize_triad_ocel_object_type(self.object_type)
        _require_non_blank("object_id", self.object_id)
        normalize_triad_ocel_artifact_kind(self.source_artifact_kind)
        if _metadata_flag_true(self.metadata, {"persisted_object", "runtime_object_persistence"}):
            raise ValueError("TriadOCELObjectRef must not imply persisted object")

    @property
    def persisted_object(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadOCELArtifactRef:
    artifact_ref_id: str
    artifact_kind: TriadOCELArtifactKind | str
    artifact_id: str
    version: str | None = None
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("artifact_ref_id", self.artifact_ref_id)
        normalize_triad_ocel_artifact_kind(self.artifact_kind)
        _require_non_blank("artifact_id", self.artifact_id)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"artifact_mutation", "mutates_artifact", "source_ref_fetch"}):
            raise ValueError("TriadOCELArtifactRef must not imply artifact mutation or fetch")

    @property
    def mutates_artifact(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadOCELTraceEventSpec:
    event_spec_id: str
    event_kind: TriadOCELTraceEventKind | str
    event_type_name: str
    description: str
    required_object_types: list[TriadOCELObjectTypeKind | str] = field(default_factory=list)
    optional_object_types: list[TriadOCELObjectTypeKind | str] = field(default_factory=list)
    required_attributes: list[str] = field(default_factory=list)
    prohibited_attributes: list[str] = field(default_factory=list)
    source_artifact_kinds: list[TriadOCELArtifactKind | str] = field(default_factory=list)
    emits_runtime_event: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("event_spec_id", self.event_spec_id)
        normalize_triad_ocel_event_kind(self.event_kind)
        _require_non_blank("event_type_name", self.event_type_name)
        _require_non_blank("description", self.description)
        _validate_enum_list("required_object_types", self.required_object_types, normalize_triad_ocel_object_type)
        _validate_enum_list("optional_object_types", self.optional_object_types, normalize_triad_ocel_object_type)
        _validate_string_list("required_attributes", self.required_attributes)
        _validate_string_list("prohibited_attributes", self.prohibited_attributes)
        _validate_enum_list("source_artifact_kinds", self.source_artifact_kinds, normalize_triad_ocel_artifact_kind)
        if self.emits_runtime_event is not False:
            raise ValueError("emits_runtime_event must always be False in v0.31.7")
        if _metadata_flag_true(self.metadata, {"event_emission", "runtime_event", "ocel_emit"}):
            raise ValueError("TriadOCELTraceEventSpec must not imply event emission")

    @property
    def is_emitted_event(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadOCELTraceObjectSpec:
    object_spec_id: str
    object_type: TriadOCELObjectTypeKind | str
    object_type_name: str
    description: str
    required_attributes: list[str] = field(default_factory=list)
    prohibited_attributes: list[str] = field(default_factory=list)
    source_artifact_kinds: list[TriadOCELArtifactKind | str] = field(default_factory=list)
    persists_runtime_object: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("object_spec_id", self.object_spec_id)
        normalize_triad_ocel_object_type(self.object_type)
        _require_non_blank("object_type_name", self.object_type_name)
        _require_non_blank("description", self.description)
        _validate_string_list("required_attributes", self.required_attributes)
        _validate_string_list("prohibited_attributes", self.prohibited_attributes)
        _validate_enum_list("source_artifact_kinds", self.source_artifact_kinds, normalize_triad_ocel_artifact_kind)
        if self.persists_runtime_object is not False:
            raise ValueError("persists_runtime_object must always be False in v0.31.7")
        if _metadata_flag_true(self.metadata, {"object_persistence", "runtime_object_persistence"}):
            raise ValueError("TriadOCELTraceObjectSpec must not imply object persistence")

    @property
    def persisted_object(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadOCELTraceRelationSpec:
    relation_spec_id: str
    relation_type: TriadOCELRelationTypeKind | str
    source_object_type: TriadOCELObjectTypeKind | str
    target_object_type: TriadOCELObjectTypeKind | str
    description: str
    required_attributes: list[str] = field(default_factory=list)
    prohibited_attributes: list[str] = field(default_factory=list)
    persists_runtime_relation: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("relation_spec_id", self.relation_spec_id)
        normalize_triad_ocel_relation_type(self.relation_type)
        normalize_triad_ocel_object_type(self.source_object_type)
        normalize_triad_ocel_object_type(self.target_object_type)
        _require_non_blank("description", self.description)
        _validate_string_list("required_attributes", self.required_attributes)
        _validate_string_list("prohibited_attributes", self.prohibited_attributes)
        if self.persists_runtime_relation is not False:
            raise ValueError("persists_runtime_relation must always be False in v0.31.7")
        if _metadata_flag_true(self.metadata, {"relation_persistence", "runtime_relation_persistence"}):
            raise ValueError("TriadOCELTraceRelationSpec must not imply relation persistence")

    @property
    def persisted_relation(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadOCELArtifactMapping:
    mapping_id: str
    artifact_ref: TriadOCELArtifactRef
    object_refs: list[TriadOCELObjectRef] = field(default_factory=list)
    event_spec_ids: list[str] = field(default_factory=list)
    relation_spec_ids: list[str] = field(default_factory=list)
    mapping_notes: list[str] = field(default_factory=list)
    coverage_gaps: list[str] = field(default_factory=list)
    emits_runtime_events: bool = False
    persists_runtime_objects: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("mapping_id", self.mapping_id)
        if not isinstance(self.artifact_ref, TriadOCELArtifactRef):
            raise TypeError("artifact_ref must be TriadOCELArtifactRef")
        _validate_object_list("object_refs", self.object_refs, TriadOCELObjectRef)
        for name in ("event_spec_ids", "relation_spec_ids", "mapping_notes", "coverage_gaps"):
            _validate_string_list(name, getattr(self, name))
        if self.emits_runtime_events is not False:
            raise ValueError("emits_runtime_events must always be False in v0.31.7")
        if self.persists_runtime_objects is not False:
            raise ValueError("persists_runtime_objects must always be False in v0.31.7")
        if _metadata_flag_true(self.metadata, {"event_emission", "object_persistence", "artifact_mutation"}):
            raise ValueError("TriadOCELArtifactMapping must remain mapping contract only")

    @property
    def mutates_artifact(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadOCELTracePlan:
    trace_plan_id: str
    version: str
    source_artifact_refs: list[TriadOCELArtifactRef] = field(default_factory=list)
    object_specs: list[TriadOCELTraceObjectSpec] = field(default_factory=list)
    event_specs: list[TriadOCELTraceEventSpec] = field(default_factory=list)
    relation_specs: list[TriadOCELTraceRelationSpec] = field(default_factory=list)
    artifact_mappings: list[TriadOCELArtifactMapping] = field(default_factory=list)
    status: TriadOCELTracePlanStatus | str = TriadOCELTracePlanStatus.DRAFT
    planned_event_type_names: list[str] = field(default_factory=list)
    planned_object_type_names: list[str] = field(default_factory=list)
    planned_relation_type_names: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    ready_for_v0318_workbench_surface: bool = False
    ready_for_ocel_emission: bool = False
    ready_for_runtime_trace_persistence: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("trace_plan_id", self.trace_plan_id)
        _validate_version_includes_v0317(self.version)
        _validate_object_list("source_artifact_refs", self.source_artifact_refs, TriadOCELArtifactRef)
        _validate_object_list("object_specs", self.object_specs, TriadOCELTraceObjectSpec)
        _validate_object_list("event_specs", self.event_specs, TriadOCELTraceEventSpec)
        _validate_object_list("relation_specs", self.relation_specs, TriadOCELTraceRelationSpec)
        _validate_object_list("artifact_mappings", self.artifact_mappings, TriadOCELArtifactMapping)
        status = normalize_triad_ocel_trace_plan_status(self.status)
        for name in (
            "planned_event_type_names",
            "planned_object_type_names",
            "planned_relation_type_names",
            "gaps",
            "blocked_reasons",
        ):
            _validate_string_list(name, getattr(self, name))
        if self.ready_for_ocel_emission is not False:
            raise ValueError("ready_for_ocel_emission must always be False in v0.31.7")
        if self.ready_for_runtime_trace_persistence is not False:
            raise ValueError("ready_for_runtime_trace_persistence must always be False in v0.31.7")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.7")
        if self.ready_for_v0318_workbench_surface and (status is TriadOCELTracePlanStatus.BLOCKED or self.blocked_reasons):
            raise ValueError("ready_for_v0318_workbench_surface requires unblocked workbench design handoff")
        if _metadata_flag_true(self.metadata, {"event_emission", "runtime_trace_persistence", "execution"}):
            raise ValueError("TriadOCELTracePlan must not imply runtime trace emission or execution")

    @property
    def emits_ocel_events(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadOCELTraceCoverage:
    coverage_id: str
    trace_plan_id: str
    artifact_kinds_covered: list[TriadOCELArtifactKind | str] = field(default_factory=list)
    artifact_kinds_missing: list[TriadOCELArtifactKind | str] = field(default_factory=list)
    event_kinds_covered: list[TriadOCELTraceEventKind | str] = field(default_factory=list)
    event_kinds_missing: list[TriadOCELTraceEventKind | str] = field(default_factory=list)
    object_types_covered: list[TriadOCELObjectTypeKind | str] = field(default_factory=list)
    object_types_missing: list[TriadOCELObjectTypeKind | str] = field(default_factory=list)
    relation_types_covered: list[TriadOCELRelationTypeKind | str] = field(default_factory=list)
    relation_types_missing: list[TriadOCELRelationTypeKind | str] = field(default_factory=list)
    status: TriadOCELTraceCoverageStatus | str = TriadOCELTraceCoverageStatus.NOT_STARTED
    blocking_gaps: list[str] = field(default_factory=list)
    non_blocking_gaps: list[str] = field(default_factory=list)
    ready_for_v0318_workbench_surface: bool = False
    ready_for_ocel_emission: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("coverage_id", self.coverage_id)
        _require_non_blank("trace_plan_id", self.trace_plan_id)
        _validate_enum_list("artifact_kinds_covered", self.artifact_kinds_covered, normalize_triad_ocel_artifact_kind)
        _validate_enum_list("artifact_kinds_missing", self.artifact_kinds_missing, normalize_triad_ocel_artifact_kind)
        _validate_enum_list("event_kinds_covered", self.event_kinds_covered, normalize_triad_ocel_event_kind)
        _validate_enum_list("event_kinds_missing", self.event_kinds_missing, normalize_triad_ocel_event_kind)
        _validate_enum_list("object_types_covered", self.object_types_covered, normalize_triad_ocel_object_type)
        _validate_enum_list("object_types_missing", self.object_types_missing, normalize_triad_ocel_object_type)
        _validate_enum_list("relation_types_covered", self.relation_types_covered, normalize_triad_ocel_relation_type)
        _validate_enum_list("relation_types_missing", self.relation_types_missing, normalize_triad_ocel_relation_type)
        normalize_triad_ocel_trace_coverage_status(self.status)
        _validate_string_list("blocking_gaps", self.blocking_gaps)
        _validate_string_list("non_blocking_gaps", self.non_blocking_gaps)
        if self.ready_for_ocel_emission is not False:
            raise ValueError("ready_for_ocel_emission must always be False in v0.31.7")
        if self.ready_for_v0318_workbench_surface and self.blocking_gaps:
            raise ValueError("ready_for_v0318_workbench_surface requires no blocking gaps")
        if _metadata_flag_true(self.metadata, {"runtime_proof", "event_emission"}):
            raise ValueError("TriadOCELTraceCoverage must not imply runtime proof or emission")

    @property
    def runtime_completeness_proof(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadOCELTraceEmissionPreview:
    emission_preview_id: str
    trace_plan_id: str
    planned_steps: list[str] = field(default_factory=list)
    expected_artifacts: list[str] = field(default_factory=list)
    explicitly_not_performed: list[str] = field(default_factory=list)
    no_ocel_event_emission_guarantee: bool = True
    no_runtime_persistence_guarantee: bool = True
    no_log_write_guarantee: bool = True
    no_registry_mutation_guarantee: bool = True
    no_memory_mutation_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("emission_preview_id", self.emission_preview_id)
        _require_non_blank("trace_plan_id", self.trace_plan_id)
        _validate_string_list("planned_steps", self.planned_steps)
        _validate_string_list("expected_artifacts", self.expected_artifacts)
        _validate_string_list("explicitly_not_performed", self.explicitly_not_performed)
        for name in (
            "no_ocel_event_emission_guarantee",
            "no_runtime_persistence_guarantee",
            "no_log_write_guarantee",
            "no_registry_mutation_guarantee",
            "no_memory_mutation_guarantee",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.31.7")
        if _metadata_flag_true(self.metadata, {"event_emission", "log_write", "runtime_persistence"}):
            raise ValueError("TriadOCELTraceEmissionPreview must not imply emission")

    @property
    def emits_preview(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadOCELNoEmissionGuarantee:
    guarantee_id: str
    version: str
    no_ocel_event_emission: bool = True
    no_ocel_object_persistence: bool = True
    no_ocel_relation_persistence: bool = True
    no_runtime_trace_write: bool = True
    no_log_write: bool = True
    no_database_write: bool = True
    no_registry_mutation: bool = True
    no_memory_mutation: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version_includes_v0317(self.version)
        for name in (
            "no_ocel_event_emission",
            "no_ocel_object_persistence",
            "no_ocel_relation_persistence",
            "no_runtime_trace_write",
            "no_log_write",
            "no_database_write",
            "no_registry_mutation",
            "no_memory_mutation",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.31.7")
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"runtime_enforcement", "event_emission", "database_write"}):
            raise ValueError("TriadOCELNoEmissionGuarantee is contract metadata only")

    @property
    def runtime_enforcement(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadOCELTraceIntegrationReport:
    report_id: str
    version: str
    trace_plan_id: str
    coverage_id: str | None
    summary: str
    status: TriadOCELTracePlanStatus | str
    mapped_artifact_count: int
    planned_event_count: int
    planned_object_count: int
    planned_relation_count: int
    gaps: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    ready_for_v0318_workbench_surface: bool = False
    ready_for_ocel_emission: bool = False
    ready_for_runtime_trace_persistence: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0317(self.version)
        _require_non_blank("trace_plan_id", self.trace_plan_id)
        _require_non_blank("summary", self.summary)
        status = normalize_triad_ocel_trace_plan_status(self.status)
        for name in ("mapped_artifact_count", "planned_event_count", "planned_object_count", "planned_relation_count"):
            _validate_non_negative(name, getattr(self, name))
        for name in ("gaps", "blocked_reasons", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        if self.ready_for_ocel_emission is not False:
            raise ValueError("ready_for_ocel_emission must always be False in v0.31.7")
        if self.ready_for_runtime_trace_persistence is not False:
            raise ValueError("ready_for_runtime_trace_persistence must always be False in v0.31.7")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.7")
        if self.ready_for_v0318_workbench_surface and (status is TriadOCELTracePlanStatus.BLOCKED or self.blocked_reasons):
            raise ValueError("ready_for_v0318_workbench_surface requires unblocked workbench design handoff")
        if _metadata_flag_true(self.metadata, {"runtime_trace_integration", "runtime_enablement", "event_emission"}):
            raise ValueError("TriadOCELTraceIntegrationReport must not imply runtime trace integration")

    @property
    def runtime_trace_integration(self) -> bool:
        return False


@dataclass(frozen=True)
class V0317ReadinessReport:
    report_id: str
    version: str
    trace_integration_report_id: str
    summary: str
    ready_for_v0318_triad_skill_workbench_surface: bool
    ready_for_ocel_emission: bool = False
    ready_for_runtime_trace_persistence: bool = False
    ready_for_execution: bool = False
    ready_for_skill_activation: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(V0317_PROHIBITED_UNTIL_LATER_GATE))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0317(self.version)
        _require_non_blank("trace_integration_report_id", self.trace_integration_report_id)
        _require_non_blank("summary", self.summary)
        if self.ready_for_ocel_emission is not False:
            raise ValueError("ready_for_ocel_emission must always be False in v0.31.7")
        if self.ready_for_runtime_trace_persistence is not False:
            raise ValueError("ready_for_runtime_trace_persistence must always be False in v0.31.7")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.7")
        if self.ready_for_skill_activation is not False:
            raise ValueError("ready_for_skill_activation must always be False in v0.31.7")
        for name in (
            "completed_items",
            "blocked_items",
            "future_track_items",
            "prohibited_until_later_gate",
            "evidence_refs",
            "withdrawal_conditions",
        ):
            _validate_string_list(name, getattr(self, name))
        missing = set(V0317_PROHIBITED_UNTIL_LATER_GATE) - set(self.prohibited_until_later_gate)
        if missing:
            raise ValueError(f"prohibited_until_later_gate missing v0.31.7 prohibitions: {sorted(missing)}")
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "event_emission", "skill_activation"}):
            raise ValueError("V0317ReadinessReport must not imply runtime enablement")

    @property
    def runtime_enablement(self) -> bool:
        return False


def build_triad_ocel_object_ref(
    object_ref_id: str,
    object_type: TriadOCELObjectTypeKind | str,
    object_id: str,
    source_artifact_kind: TriadOCELArtifactKind | str,
    source_artifact_id: str | None = None,
    display_name: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> TriadOCELObjectRef:
    return TriadOCELObjectRef(
        object_ref_id=object_ref_id,
        object_type=object_type,
        object_id=object_id,
        source_artifact_kind=source_artifact_kind,
        source_artifact_id=source_artifact_id,
        display_name=display_name,
        metadata=dict(metadata or {}),
    )


def build_triad_ocel_artifact_ref(
    artifact_ref_id: str,
    artifact_kind: TriadOCELArtifactKind | str,
    artifact_id: str,
    version: str | None = None,
    evidence_refs: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> TriadOCELArtifactRef:
    return TriadOCELArtifactRef(
        artifact_ref_id=artifact_ref_id,
        artifact_kind=artifact_kind,
        artifact_id=artifact_id,
        version=version,
        evidence_refs=list(evidence_refs or []),
        metadata=dict(metadata or {}),
    )


def build_triad_ocel_event_spec(
    event_spec_id: str,
    event_kind: TriadOCELTraceEventKind | str,
    event_type_name: str,
    description: str,
    required_object_types: list[TriadOCELObjectTypeKind | str] | None = None,
    optional_object_types: list[TriadOCELObjectTypeKind | str] | None = None,
    required_attributes: list[str] | None = None,
    prohibited_attributes: list[str] | None = None,
    source_artifact_kinds: list[TriadOCELArtifactKind | str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> TriadOCELTraceEventSpec:
    return TriadOCELTraceEventSpec(
        event_spec_id=event_spec_id,
        event_kind=event_kind,
        event_type_name=event_type_name,
        description=description,
        required_object_types=list(required_object_types or []),
        optional_object_types=list(optional_object_types or []),
        required_attributes=list(required_attributes or []),
        prohibited_attributes=list(prohibited_attributes or []),
        source_artifact_kinds=list(source_artifact_kinds or []),
        emits_runtime_event=False,
        metadata=dict(metadata or {}),
    )


def build_triad_ocel_object_spec(
    object_spec_id: str,
    object_type: TriadOCELObjectTypeKind | str,
    object_type_name: str,
    description: str,
    required_attributes: list[str] | None = None,
    prohibited_attributes: list[str] | None = None,
    source_artifact_kinds: list[TriadOCELArtifactKind | str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> TriadOCELTraceObjectSpec:
    return TriadOCELTraceObjectSpec(
        object_spec_id=object_spec_id,
        object_type=object_type,
        object_type_name=object_type_name,
        description=description,
        required_attributes=list(required_attributes or []),
        prohibited_attributes=list(prohibited_attributes or []),
        source_artifact_kinds=list(source_artifact_kinds or []),
        persists_runtime_object=False,
        metadata=dict(metadata or {}),
    )


def build_triad_ocel_relation_spec(
    relation_spec_id: str,
    relation_type: TriadOCELRelationTypeKind | str,
    source_object_type: TriadOCELObjectTypeKind | str,
    target_object_type: TriadOCELObjectTypeKind | str,
    description: str,
    required_attributes: list[str] | None = None,
    prohibited_attributes: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> TriadOCELTraceRelationSpec:
    return TriadOCELTraceRelationSpec(
        relation_spec_id=relation_spec_id,
        relation_type=relation_type,
        source_object_type=source_object_type,
        target_object_type=target_object_type,
        description=description,
        required_attributes=list(required_attributes or []),
        prohibited_attributes=list(prohibited_attributes or []),
        persists_runtime_relation=False,
        metadata=dict(metadata or {}),
    )


def build_triad_ocel_artifact_mapping(
    mapping_id: str,
    artifact_ref: TriadOCELArtifactRef,
    object_refs: list[TriadOCELObjectRef] | None = None,
    event_spec_ids: list[str] | None = None,
    relation_spec_ids: list[str] | None = None,
    mapping_notes: list[str] | None = None,
    coverage_gaps: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> TriadOCELArtifactMapping:
    return TriadOCELArtifactMapping(
        mapping_id=mapping_id,
        artifact_ref=artifact_ref,
        object_refs=list(object_refs or []),
        event_spec_ids=list(event_spec_ids or []),
        relation_spec_ids=list(relation_spec_ids or []),
        mapping_notes=list(mapping_notes or []),
        coverage_gaps=list(coverage_gaps or []),
        emits_runtime_events=False,
        persists_runtime_objects=False,
        metadata=dict(metadata or {}),
    )


def build_default_triad_ocel_event_specs() -> list[TriadOCELTraceEventSpec]:
    specs: list[TriadOCELTraceEventSpec] = []
    for event_kind in TriadOCELTraceEventKind:
        if event_kind is TriadOCELTraceEventKind.UNKNOWN:
            continue
        specs.append(
            build_triad_ocel_event_spec(
                event_spec_id=f"triad_ocel_event_spec:{event_kind.value}:v0.31.7",
                event_kind=event_kind,
                event_type_name=event_kind.value,
                description=f"Contract-only OCEL event type for {event_kind.value}.",
                required_object_types=[TriadOCELObjectTypeKind.TRIAD_SKILL_RUN],
                optional_object_types=[TriadOCELObjectTypeKind.UNKNOWN],
                required_attributes=["event_spec_id", "source_artifact_ref"],
                prohibited_attributes=["runtime_emission", "database_write", "log_write"],
                source_artifact_kinds=[TriadOCELArtifactKind.UNKNOWN],
            )
        )
    return specs


def build_default_triad_ocel_object_specs() -> list[TriadOCELTraceObjectSpec]:
    specs: list[TriadOCELTraceObjectSpec] = []
    for object_type in TriadOCELObjectTypeKind:
        if object_type is TriadOCELObjectTypeKind.UNKNOWN:
            continue
        specs.append(
            build_triad_ocel_object_spec(
                object_spec_id=f"triad_ocel_object_spec:{object_type.value}:v0.31.7",
                object_type=object_type,
                object_type_name=object_type.value,
                description=f"Contract-only OCEL object type for {object_type.value}.",
                required_attributes=["object_ref_id", "source_artifact_ref"],
                prohibited_attributes=["runtime_persistence", "database_write"],
                source_artifact_kinds=[TriadOCELArtifactKind.UNKNOWN],
            )
        )
    return specs


def build_default_triad_ocel_relation_specs() -> list[TriadOCELTraceRelationSpec]:
    specs: list[TriadOCELTraceRelationSpec] = []
    for relation_type in TriadOCELRelationTypeKind:
        if relation_type is TriadOCELRelationTypeKind.UNKNOWN:
            continue
        specs.append(
            build_triad_ocel_relation_spec(
                relation_spec_id=f"triad_ocel_relation_spec:{relation_type.value}:v0.31.7",
                relation_type=relation_type,
                source_object_type=TriadOCELObjectTypeKind.UNKNOWN,
                target_object_type=TriadOCELObjectTypeKind.UNKNOWN,
                description=f"Contract-only OCEL relation type for {relation_type.value}.",
                required_attributes=["source_object_ref", "target_object_ref"],
                prohibited_attributes=["runtime_relation_persistence", "database_write"],
            )
        )
    return specs


def build_triad_ocel_trace_plan(
    trace_plan_id: str,
    source_artifact_refs: list[TriadOCELArtifactRef] | None = None,
    object_specs: list[TriadOCELTraceObjectSpec] | None = None,
    event_specs: list[TriadOCELTraceEventSpec] | None = None,
    relation_specs: list[TriadOCELTraceRelationSpec] | None = None,
    artifact_mappings: list[TriadOCELArtifactMapping] | None = None,
    status: TriadOCELTracePlanStatus | str = TriadOCELTracePlanStatus.PLAN_READY,
    gaps: list[str] | None = None,
    blocked_reasons: list[str] | None = None,
    ready_for_v0318_workbench_surface: bool = True,
    metadata: dict[str, Any] | None = None,
) -> TriadOCELTracePlan:
    resolved_event_specs = list(event_specs or build_default_triad_ocel_event_specs())
    resolved_object_specs = list(object_specs or build_default_triad_ocel_object_specs())
    resolved_relation_specs = list(relation_specs or build_default_triad_ocel_relation_specs())
    return TriadOCELTracePlan(
        trace_plan_id=trace_plan_id,
        version=V0317_VERSION,
        source_artifact_refs=list(source_artifact_refs or []),
        object_specs=resolved_object_specs,
        event_specs=resolved_event_specs,
        relation_specs=resolved_relation_specs,
        artifact_mappings=list(artifact_mappings or []),
        status=status,
        planned_event_type_names=[spec.event_type_name for spec in resolved_event_specs],
        planned_object_type_names=[spec.object_type_name for spec in resolved_object_specs],
        planned_relation_type_names=[normalize_triad_ocel_relation_type(spec.relation_type).value for spec in resolved_relation_specs],
        gaps=list(gaps or []),
        blocked_reasons=list(blocked_reasons or []),
        ready_for_v0318_workbench_surface=ready_for_v0318_workbench_surface,
        ready_for_ocel_emission=False,
        ready_for_runtime_trace_persistence=False,
        ready_for_execution=False,
        metadata=dict(metadata or {}),
    )


def build_triad_ocel_trace_coverage(
    coverage_id: str,
    trace_plan_id: str,
    artifact_kinds_covered: list[TriadOCELArtifactKind | str] | None = None,
    artifact_kinds_missing: list[TriadOCELArtifactKind | str] | None = None,
    event_kinds_covered: list[TriadOCELTraceEventKind | str] | None = None,
    event_kinds_missing: list[TriadOCELTraceEventKind | str] | None = None,
    object_types_covered: list[TriadOCELObjectTypeKind | str] | None = None,
    object_types_missing: list[TriadOCELObjectTypeKind | str] | None = None,
    relation_types_covered: list[TriadOCELRelationTypeKind | str] | None = None,
    relation_types_missing: list[TriadOCELRelationTypeKind | str] | None = None,
    status: TriadOCELTraceCoverageStatus | str = TriadOCELTraceCoverageStatus.COVERED_WITH_GAPS,
    blocking_gaps: list[str] | None = None,
    non_blocking_gaps: list[str] | None = None,
    ready_for_v0318_workbench_surface: bool = True,
    metadata: dict[str, Any] | None = None,
) -> TriadOCELTraceCoverage:
    return TriadOCELTraceCoverage(
        coverage_id=coverage_id,
        trace_plan_id=trace_plan_id,
        artifact_kinds_covered=list(artifact_kinds_covered or [kind for kind in TriadOCELArtifactKind if kind is not TriadOCELArtifactKind.UNKNOWN]),
        artifact_kinds_missing=list(artifact_kinds_missing or []),
        event_kinds_covered=list(event_kinds_covered or [kind for kind in TriadOCELTraceEventKind if kind is not TriadOCELTraceEventKind.UNKNOWN]),
        event_kinds_missing=list(event_kinds_missing or []),
        object_types_covered=list(object_types_covered or [kind for kind in TriadOCELObjectTypeKind if kind is not TriadOCELObjectTypeKind.UNKNOWN]),
        object_types_missing=list(object_types_missing or []),
        relation_types_covered=list(relation_types_covered or [kind for kind in TriadOCELRelationTypeKind if kind is not TriadOCELRelationTypeKind.UNKNOWN]),
        relation_types_missing=list(relation_types_missing or []),
        status=status,
        blocking_gaps=list(blocking_gaps or []),
        non_blocking_gaps=list(non_blocking_gaps or []),
        ready_for_v0318_workbench_surface=ready_for_v0318_workbench_surface,
        ready_for_ocel_emission=False,
        metadata=dict(metadata or {}),
    )


def build_triad_ocel_trace_emission_preview(
    emission_preview_id: str,
    trace_plan_id: str,
    planned_steps: list[str] | None = None,
    expected_artifacts: list[str] | None = None,
    explicitly_not_performed: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> TriadOCELTraceEmissionPreview:
    return TriadOCELTraceEmissionPreview(
        emission_preview_id=emission_preview_id,
        trace_plan_id=trace_plan_id,
        planned_steps=list(planned_steps or ["derive trace specs", "derive artifact mappings", "review trace coverage"]),
        expected_artifacts=list(
            expected_artifacts
            or [
                "TriadOCELTraceEventSpec",
                "TriadOCELTraceObjectSpec",
                "TriadOCELTraceRelationSpec",
                "TriadOCELArtifactMapping",
                "TriadOCELTraceCoverage",
            ]
        ),
        explicitly_not_performed=list(
            explicitly_not_performed
            or [
                "OCEL event emission",
                "runtime trace persistence",
                "log write",
                "database write",
                "registry mutation",
                "memory mutation",
            ]
        ),
        metadata=dict(metadata or {}),
    )


def build_triad_ocel_no_emission_guarantee(
    guarantee_id: str,
    evidence_refs: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> TriadOCELNoEmissionGuarantee:
    return TriadOCELNoEmissionGuarantee(
        guarantee_id=guarantee_id,
        version=V0317_VERSION,
        evidence_refs=list(evidence_refs or []),
        metadata=dict(metadata or {}),
    )


def build_triad_ocel_trace_integration_report(
    report_id: str,
    trace_plan: TriadOCELTracePlan,
    coverage: TriadOCELTraceCoverage | None = None,
    summary: str = "v0.31.7 defines OCEL trace contract artifacts only; no event emission or persistence.",
    evidence_refs: list[str] | None = None,
    withdrawal_conditions: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> TriadOCELTraceIntegrationReport:
    if not isinstance(trace_plan, TriadOCELTracePlan):
        raise TypeError("trace_plan must be TriadOCELTracePlan")
    if coverage is not None and not isinstance(coverage, TriadOCELTraceCoverage):
        raise TypeError("coverage must be TriadOCELTraceCoverage")
    return TriadOCELTraceIntegrationReport(
        report_id=report_id,
        version=V0317_VERSION,
        trace_plan_id=trace_plan.trace_plan_id,
        coverage_id=coverage.coverage_id if coverage is not None else None,
        summary=summary,
        status=trace_plan.status,
        mapped_artifact_count=len(trace_plan.artifact_mappings),
        planned_event_count=len(trace_plan.event_specs),
        planned_object_count=len(trace_plan.object_specs),
        planned_relation_count=len(trace_plan.relation_specs),
        gaps=list(trace_plan.gaps),
        blocked_reasons=list(trace_plan.blocked_reasons),
        ready_for_v0318_workbench_surface=trace_plan.ready_for_v0318_workbench_surface
        and (coverage is None or coverage.ready_for_v0318_workbench_surface),
        ready_for_ocel_emission=False,
        ready_for_runtime_trace_persistence=False,
        ready_for_execution=False,
        evidence_refs=list(evidence_refs or []),
        withdrawal_conditions=list(
            withdrawal_conditions
            or [
                "OCEL event emission is introduced",
                "OCEL database persistence is introduced",
                "runtime trace or log write is introduced",
                "ready_for_ocel_emission, ready_for_runtime_trace_persistence, or ready_for_execution becomes true",
            ]
        ),
        metadata=dict(metadata or {}),
    )


def build_v0317_readiness_report(
    trace_integration_report: TriadOCELTraceIntegrationReport,
    metadata: dict[str, Any] | None = None,
) -> V0317ReadinessReport:
    if not isinstance(trace_integration_report, TriadOCELTraceIntegrationReport):
        raise TypeError("trace_integration_report must be TriadOCELTraceIntegrationReport")
    return V0317ReadinessReport(
        report_id="v0317_readiness_report:triad_skill_ocel_trace_integration",
        version=V0317_VERSION,
        trace_integration_report_id=trace_integration_report.report_id,
        summary="v0.31.7 is ready for v0.31.8 Triad Skill Workbench Surface design handoff only; not runtime trace emission.",
        ready_for_v0318_triad_skill_workbench_surface=trace_integration_report.ready_for_v0318_workbench_surface,
        ready_for_ocel_emission=False,
        ready_for_runtime_trace_persistence=False,
        ready_for_execution=False,
        ready_for_skill_activation=False,
        completed_items=[
            "OCEL trace event vocabulary",
            "OCEL object and relation vocabularies",
            "artifact-to-OCEL mapping contracts",
            "trace plan and coverage contracts",
            "no-emission guarantee",
        ],
        blocked_items=[],
        future_track_items=["OCEL event emission", "runtime trace persistence", "workbench surface runtime"],
        evidence_refs=list(trace_integration_report.evidence_refs),
        withdrawal_conditions=list(trace_integration_report.withdrawal_conditions),
        metadata=dict(metadata or {}),
    )


def ocel_event_spec_preserves_no_emission(spec: TriadOCELTraceEventSpec) -> bool:
    return spec.emits_runtime_event is False and spec.is_emitted_event is False


def ocel_object_spec_preserves_no_persistence(spec: TriadOCELTraceObjectSpec) -> bool:
    return spec.persists_runtime_object is False and spec.persisted_object is False


def ocel_relation_spec_preserves_no_persistence(spec: TriadOCELTraceRelationSpec) -> bool:
    return spec.persists_runtime_relation is False and spec.persisted_relation is False


def ocel_trace_plan_preserves_no_emission(plan: TriadOCELTracePlan) -> bool:
    return (
        plan.ready_for_ocel_emission is False
        and plan.ready_for_runtime_trace_persistence is False
        and plan.ready_for_execution is False
        and plan.emits_ocel_events is False
        and all(ocel_event_spec_preserves_no_emission(spec) for spec in plan.event_specs)
        and all(ocel_object_spec_preserves_no_persistence(spec) for spec in plan.object_specs)
        and all(ocel_relation_spec_preserves_no_persistence(spec) for spec in plan.relation_specs)
        and all(mapping.emits_runtime_events is False and mapping.persists_runtime_objects is False for mapping in plan.artifact_mappings)
    )


def ocel_trace_coverage_is_not_runtime_proof(coverage: TriadOCELTraceCoverage) -> bool:
    return coverage.ready_for_ocel_emission is False and coverage.runtime_completeness_proof is False


def ocel_trace_report_is_not_runtime_ready(report: TriadOCELTraceIntegrationReport) -> bool:
    return (
        report.ready_for_ocel_emission is False
        and report.ready_for_runtime_trace_persistence is False
        and report.ready_for_execution is False
        and report.runtime_trace_integration is False
    )
