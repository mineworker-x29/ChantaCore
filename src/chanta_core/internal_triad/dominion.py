from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from chanta_core.internal_triad.boundaries import _require_non_blank, _validate_string_list
from chanta_core.internal_triad.internalization import (
    InternalCandidateSet,
    InternalizationNoOpDecision,
    InternalizationPlan,
    V0314ReadinessReport,
    V0314_REQUIRED_PROHIBITED_RUNTIME_ACTIONS,
)
from chanta_core.internal_triad.skill_kinds import V0310_TRACK


V0315_VERSION = "v0.31.5"
V0315_RELEASE_NAME = "v0.31.5 Dominion Skill Foundation"
V0315_TRACK = V0310_TRACK

V0315_REQUIRED_PROHIBITED_RUNTIME_ACTIONS = [
    *V0314_REQUIRED_PROHIBITED_RUNTIME_ACTIONS,
    "external_control",
    "authority_grant",
    "dominion_target_creation",
    "dominion_decision_creation",
    "dominion_runtime",
    "external_execution",
]

V0315_PROHIBITED_UNTIL_LATER_GATE = [
    "external_control",
    "authority_grant",
    "dominion_target_creation",
    "dominion_decision_creation",
    "external_execution",
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
]


class DominionSkillSourceKind(StrEnum):
    INTERNAL_CANDIDATE_SET = "internal_candidate_set"
    INTERNALIZATION_PLAN = "internalization_plan"
    INTERNALIZATION_NO_OP_DECISION = "internalization_no_op_decision"
    V0314_READINESS_REPORT = "v0314_readiness_report"
    DIGESTION_SKILL_OUTPUT = "digestion_skill_output"
    DIGESTION_ROUTE_DECISION = "digestion_route_decision"
    DIGESTIBLE_PATTERN_SIGNAL = "digestible_pattern_signal"
    OBSERVATION_RISK_MAP = "observation_risk_map"
    OBSERVATION_GAP_REGISTER = "observation_gap_register"
    CAPABILITY_MAP_ENTRY = "capability_map_entry"
    EXTERNAL_DOMINION_AUTHORITY_DECISION = "external_dominion_authority_decision"
    EXTERNAL_CERTIFICATION_REPORT = "external_certification_report"
    EXTERNAL_PREVIEW_GATE_REPORT = "external_preview_gate_report"
    MANUAL_DOMINION_REVIEW = "manual_dominion_review"
    UNKNOWN = "unknown"


class DominionFocusKind(StrEnum):
    EXTERNAL_RUNTIME_BOUNDARY = "external_runtime_boundary"
    PROVIDER_BOUNDARY = "provider_boundary"
    NETWORK_BOUNDARY = "network_boundary"
    CREDENTIAL_BOUNDARY = "credential_boundary"
    COMMAND_BOUNDARY = "command_boundary"
    BROWSER_BOUNDARY = "browser_boundary"
    RPA_BOUNDARY = "rpa_boundary"
    GATEWAY_BOUNDARY = "gateway_boundary"
    DELEGATION_BOUNDARY = "delegation_boundary"
    MEMORY_BOUNDARY = "memory_boundary"
    RAW_OUTPUT_BOUNDARY = "raw_output_boundary"
    REGISTRY_BOUNDARY = "registry_boundary"
    POLICY_BOUNDARY = "policy_boundary"
    APPROVAL_BOUNDARY = "approval_boundary"
    AUDIT_BOUNDARY = "audit_boundary"
    ROLLBACK_NO_OP_BOUNDARY = "rollback_no_op_boundary"
    FUTURE_GATE_BOUNDARY = "future_gate_boundary"
    OCEL_TRACE_BOUNDARY = "ocel_trace_boundary"
    UNKNOWN = "unknown"


class DominionSignalKind(StrEnum):
    DOMINION_REQUIRED = "dominion_required"
    EXTERNAL_CONTROL_RISK_DETECTED = "external_control_risk_detected"
    RUNTIME_BOUNDARY_NEEDED = "runtime_boundary_needed"
    AUTHORITY_BOUNDARY_NEEDED = "authority_boundary_needed"
    APPROVAL_BOUNDARY_NEEDED = "approval_boundary_needed"
    AUDIT_BOUNDARY_NEEDED = "audit_boundary_needed"
    RESULT_BOUNDARY_NEEDED = "result_boundary_needed"
    ROLLBACK_NO_OP_NEEDED = "rollback_no_op_needed"
    FUTURE_GATE_NEEDED = "future_gate_needed"
    NO_OP_RECOMMENDED = "no_op_recommended"
    BLOCKED_BY_POLICY = "blocked_by_policy"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    UNSAFE_TO_CONTROL = "unsafe_to_control"
    INCOMPATIBLE_WITH_OCEL_SPINE = "incompatible_with_ocel_spine"
    UNKNOWN = "unknown"


class DominionRoute(StrEnum):
    DOMINION_TARGET_SIGNAL = "dominion_target_signal"
    DOMINION_DECISION_SIGNAL = "dominion_decision_signal"
    FUTURE_GATE_SIGNAL = "future_gate_signal"
    REVIEW_REQUIRED = "review_required"
    DEFER = "defer"
    REJECT = "reject"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class DominionFeasibilityPosture(StrEnum):
    UNKNOWN = "unknown"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class DominionBoundaryPosture(StrEnum):
    UNKNOWN = "unknown"
    DESCRIPTIVE_ONLY = "descriptive_only"
    OBSERVATION_ONLY = "observation_only"
    PLAN_ONLY = "plan_only"
    SIMULATE_ONLY = "simulate_only"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class DominionRiskPosture(StrEnum):
    UNKNOWN = "unknown"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class DominionBlockerKind(StrEnum):
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    MISSING_INTERNALIZATION_CONTEXT = "missing_internalization_context"
    MISSING_BOUNDARY_CLASSIFICATION = "missing_boundary_classification"
    MISSING_RISK_MAP = "missing_risk_map"
    MISSING_APPROVAL_BOUNDARY = "missing_approval_boundary"
    MISSING_AUDIT_BOUNDARY = "missing_audit_boundary"
    MISSING_RESULT_BOUNDARY = "missing_result_boundary"
    MISSING_ROLLBACK_NO_OP = "missing_rollback_no_op"
    UNSAFE_NETWORK_SURFACE = "unsafe_network_surface"
    UNSAFE_CREDENTIAL_SURFACE = "unsafe_credential_surface"
    UNSAFE_COMMAND_SURFACE = "unsafe_command_surface"
    UNSAFE_PROVIDER_SURFACE = "unsafe_provider_surface"
    UNSAFE_BROWSER_SURFACE = "unsafe_browser_surface"
    UNSAFE_RPA_SURFACE = "unsafe_rpa_surface"
    UNSAFE_GATEWAY_SURFACE = "unsafe_gateway_surface"
    UNSAFE_DELEGATION_SURFACE = "unsafe_delegation_surface"
    MEMORY_CONTAMINATION_RISK = "memory_contamination_risk"
    RAW_OUTPUT_PERSISTENCE_RISK = "raw_output_persistence_risk"
    REGISTRY_MUTATION_RISK = "registry_mutation_risk"
    POLICY_ACTIVATION_RISK = "policy_activation_risk"
    REQUIRES_FUTURE_GATE = "requires_future_gate"
    INCOMPATIBLE_WITH_OCEL_SPINE = "incompatible_with_ocel_spine"
    UNKNOWN = "unknown"


def _metadata_flag_true(metadata: dict[str, Any], names: set[str]) -> bool:
    return isinstance(metadata, dict) and any(metadata.get(name) is True for name in names)


def _validate_object_list(name: str, values: list[Any], expected_type: type) -> None:
    if not isinstance(values, list) or not all(isinstance(item, expected_type) for item in values):
        raise TypeError(f"{name} must be list[{expected_type.__name__}]")


def _validate_version_includes_v0315(version: str) -> None:
    _require_non_blank("version", version)
    if V0315_VERSION not in version:
        raise ValueError("version must include v0.31.5")


def _validate_prohibited_actions(actions: list[str]) -> None:
    _validate_string_list("prohibited_runtime_actions", actions)
    missing = set(V0315_REQUIRED_PROHIBITED_RUNTIME_ACTIONS) - set(actions)
    if missing:
        raise ValueError(f"prohibited_runtime_actions missing v0.31.5 prohibitions: {sorted(missing)}")


def normalize_dominion_source_kind(value: DominionSkillSourceKind | str) -> DominionSkillSourceKind:
    if isinstance(value, DominionSkillSourceKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("dominion source kind must not be blank")
        return DominionSkillSourceKind(stripped)
    raise TypeError(f"unsupported dominion source kind: {value!r}")


def normalize_dominion_focus_kind(value: DominionFocusKind | str) -> DominionFocusKind:
    if isinstance(value, DominionFocusKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("dominion focus kind must not be blank")
        return DominionFocusKind(stripped)
    raise TypeError(f"unsupported dominion focus kind: {value!r}")


def normalize_dominion_signal_kind(value: DominionSignalKind | str) -> DominionSignalKind:
    if isinstance(value, DominionSignalKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("dominion signal kind must not be blank")
        return DominionSignalKind(stripped)
    raise TypeError(f"unsupported dominion signal kind: {value!r}")


def normalize_dominion_route(value: DominionRoute | str) -> DominionRoute:
    if isinstance(value, DominionRoute):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("dominion route must not be blank")
        return DominionRoute(stripped)
    raise TypeError(f"unsupported dominion route: {value!r}")


def normalize_dominion_feasibility_posture(value: DominionFeasibilityPosture | str) -> DominionFeasibilityPosture:
    if isinstance(value, DominionFeasibilityPosture):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("dominion feasibility posture must not be blank")
        return DominionFeasibilityPosture(stripped)
    raise TypeError(f"unsupported dominion feasibility posture: {value!r}")


def normalize_dominion_boundary_posture(value: DominionBoundaryPosture | str) -> DominionBoundaryPosture:
    if isinstance(value, DominionBoundaryPosture):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("dominion boundary posture must not be blank")
        return DominionBoundaryPosture(stripped)
    raise TypeError(f"unsupported dominion boundary posture: {value!r}")


def normalize_dominion_risk_posture(value: DominionRiskPosture | str) -> DominionRiskPosture:
    if isinstance(value, DominionRiskPosture):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("dominion risk posture must not be blank")
        return DominionRiskPosture(stripped)
    raise TypeError(f"unsupported dominion risk posture: {value!r}")


def normalize_dominion_blocker_kind(value: DominionBlockerKind | str) -> DominionBlockerKind:
    if isinstance(value, DominionBlockerKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("dominion blocker kind must not be blank")
        return DominionBlockerKind(stripped)
    raise TypeError(f"unsupported dominion blocker kind: {value!r}")


def dominion_source_kind_fetches(_: DominionSkillSourceKind | str) -> bool:
    normalize_dominion_source_kind(_)
    return False


def dominion_focus_kind_creates_target(_: DominionFocusKind | str) -> bool:
    normalize_dominion_focus_kind(_)
    return False


@dataclass(frozen=True)
class DominionSkillSourceRef:
    source_ref_id: str
    source_kind: DominionSkillSourceKind | str
    source_id: str
    target_id: str | None = None
    candidate_id: str | None = None
    capability_entry_id: str | None = None
    internal_candidate_id: str | None = None
    evidence_ref_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        normalize_dominion_source_kind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _validate_string_list("evidence_ref_ids", self.evidence_ref_ids)
        if _metadata_flag_true(self.metadata, {"source_fetch", "source_ref_fetch", "url_fetch"}):
            raise ValueError("DominionSkillSourceRef must not imply source fetch")

    @property
    def fetches_source(self) -> bool:
        return False


@dataclass(frozen=True)
class DominionSkillInput:
    dominion_input_id: str
    triad_input_id: str | None
    source_refs: list[DominionSkillSourceRef]
    internal_candidate_set_refs: list[str]
    internalization_plan_refs: list[str]
    digestion_output_refs: list[str]
    route_decision_refs: list[str]
    risk_map_refs: list[str]
    gap_register_refs: list[str]
    requested_focus: list[DominionFocusKind | str]
    task_summary: str
    source_version: str
    evidence_refs: list[str]
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(V0315_REQUIRED_PROHIBITED_RUNTIME_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("dominion_input_id", self.dominion_input_id)
        _validate_object_list("source_refs", self.source_refs, DominionSkillSourceRef)
        for name in (
            "internal_candidate_set_refs",
            "internalization_plan_refs",
            "digestion_output_refs",
            "route_decision_refs",
            "risk_map_refs",
            "gap_register_refs",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        if not isinstance(self.requested_focus, list):
            raise TypeError("requested_focus must be list[DominionFocusKind | str]")
        for focus in self.requested_focus:
            normalize_dominion_focus_kind(focus)
        _require_non_blank("task_summary", self.task_summary)
        _require_non_blank("source_version", self.source_version)
        _validate_prohibited_actions(self.prohibited_runtime_actions)
        if _metadata_flag_true(
            self.metadata,
            {"execution_request", "external_control", "authority_grant", "read_only_tool_execution", "dominion_runtime"},
        ):
            raise ValueError("DominionSkillInput must not imply execution, external control, authority grant, or runtime")

    @property
    def is_execution_request(self) -> bool:
        return False


@dataclass(frozen=True)
class DominionControlBoundarySignal:
    signal_id: str
    source_ref_id: str | None
    target_id: str | None
    candidate_id: str | None
    focus_kind: DominionFocusKind | str
    signal_kind: DominionSignalKind | str
    proposed_route: DominionRoute | str
    title: str
    summary: str
    boundary_summary: str | None = None
    risk_posture: DominionRiskPosture | str = DominionRiskPosture.UNKNOWN
    boundary_posture: DominionBoundaryPosture | str = DominionBoundaryPosture.UNKNOWN
    feasibility_posture: DominionFeasibilityPosture | str = DominionFeasibilityPosture.UNKNOWN
    evidence_ref_ids: list[str] = field(default_factory=list)
    blocker_ids: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("signal_id", self.signal_id)
        normalize_dominion_focus_kind(self.focus_kind)
        normalize_dominion_signal_kind(self.signal_kind)
        route = normalize_dominion_route(self.proposed_route)
        _require_non_blank("title", self.title)
        _require_non_blank("summary", self.summary)
        risk = normalize_dominion_risk_posture(self.risk_posture)
        normalize_dominion_boundary_posture(self.boundary_posture)
        normalize_dominion_feasibility_posture(self.feasibility_posture)
        for name in ("evidence_ref_ids", "blocker_ids", "assumptions", "limitations"):
            _validate_string_list(name, getattr(self, name))
        if risk in {DominionRiskPosture.HIGH, DominionRiskPosture.CRITICAL, DominionRiskPosture.BLOCKED}:
            if not self.blocker_ids and not self.limitations and route not in {
                DominionRoute.FUTURE_GATE_SIGNAL,
                DominionRoute.REVIEW_REQUIRED,
                DominionRoute.BLOCKED,
                DominionRoute.NO_OP,
            }:
                raise ValueError("high, critical, or blocked risk requires blocker_ids, limitations, or conservative route")
        if _metadata_flag_true(self.metadata, {"dominion_target_creation", "dominion_decision_creation", "authority_grant"}):
            raise ValueError("DominionControlBoundarySignal must remain signal-only")

    @property
    def creates_dominion_target(self) -> bool:
        return False

    @property
    def creates_dominion_decision(self) -> bool:
        return False

    @property
    def grants_authority(self) -> bool:
        return False


@dataclass(frozen=True)
class DominionGovernanceFinding:
    finding_id: str
    dominion_input_id: str
    signal_ids: list[str]
    route: DominionRoute | str
    summary: str
    risk_posture: DominionRiskPosture | str
    boundary_posture: DominionBoundaryPosture | str
    feasibility_posture: DominionFeasibilityPosture | str
    evidence_ref_ids: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    recommended_next_stage: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("dominion_input_id", self.dominion_input_id)
        _validate_string_list("signal_ids", self.signal_ids)
        normalize_dominion_route(self.route)
        _require_non_blank("summary", self.summary)
        normalize_dominion_risk_posture(self.risk_posture)
        normalize_dominion_boundary_posture(self.boundary_posture)
        normalize_dominion_feasibility_posture(self.feasibility_posture)
        _validate_string_list("evidence_ref_ids", self.evidence_ref_ids)
        _validate_string_list("blocked_reasons", self.blocked_reasons)
        if _metadata_flag_true(self.metadata, {"v0316_artifact_creation", "dominion_decision_creation", "authority_grant"}):
            raise ValueError("DominionGovernanceFinding must not create later-stage artifacts or grant authority")

    @property
    def creates_v0316_artifact(self) -> bool:
        return False

    @property
    def grants_authority(self) -> bool:
        return False


@dataclass(frozen=True)
class DominionBlocker:
    blocker_id: str
    blocker_kind: DominionBlockerKind | str
    source_ref_id: str | None
    target_id: str | None
    candidate_id: str | None
    description: str
    blocks_v0316: bool
    routes_to_future_gate: bool
    routes_to_no_op: bool
    evidence_ref_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("blocker_id", self.blocker_id)
        normalize_dominion_blocker_kind(self.blocker_kind)
        _require_non_blank("description", self.description)
        for name in ("blocks_v0316", "routes_to_future_gate", "routes_to_no_op"):
            if not isinstance(getattr(self, name), bool):
                raise TypeError(f"{name} must be bool")
        _validate_string_list("evidence_ref_ids", self.evidence_ref_ids)
        if _metadata_flag_true(self.metadata, {"remediation_execution", "automatic_remediation"}):
            raise ValueError("DominionBlocker must not execute remediation")

    @property
    def executes_remediation(self) -> bool:
        return False


@dataclass(frozen=True)
class DominionRouteDecision:
    route_decision_id: str
    dominion_input_id: str
    route: DominionRoute | str
    signal_ids: list[str]
    blocker_ids: list[str]
    reason: str
    evidence_ref_ids: list[str] = field(default_factory=list)
    ready_for_v0316_dominion_target_decision: bool = False
    ready_for_execution: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    ready_for_dominion_target_creation: bool = False
    ready_for_dominion_decision_creation: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("route_decision_id", self.route_decision_id)
        _require_non_blank("dominion_input_id", self.dominion_input_id)
        route = normalize_dominion_route(self.route)
        for name in ("signal_ids", "blocker_ids", "evidence_ref_ids"):
            _validate_string_list(name, getattr(self, name))
        _require_non_blank("reason", self.reason)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.5")
        if self.ready_for_external_control is not False:
            raise ValueError("ready_for_external_control must always be False in v0.31.5")
        if self.ready_for_authority_grant is not False:
            raise ValueError("ready_for_authority_grant must always be False in v0.31.5")
        if self.ready_for_dominion_target_creation is not False:
            raise ValueError("ready_for_dominion_target_creation must always be False in v0.31.5")
        if self.ready_for_dominion_decision_creation is not False:
            raise ValueError("ready_for_dominion_decision_creation must always be False in v0.31.5")
        if self.ready_for_v0316_dominion_target_decision and (
            route not in {DominionRoute.DOMINION_TARGET_SIGNAL, DominionRoute.DOMINION_DECISION_SIGNAL} or self.blocker_ids
        ):
            raise ValueError("v0.31.6 readiness requires target/decision signal route with no blocking blockers")
        if _metadata_flag_true(self.metadata, {"implementation", "authority_grant", "external_control"}):
            raise ValueError("DominionRouteDecision must not imply implementation, external control, or authority grant")

    @property
    def is_implementation(self) -> bool:
        return False

    @property
    def grants_authority(self) -> bool:
        return False


@dataclass(frozen=True)
class DominionSkillOutput:
    dominion_output_id: str
    dominion_input_id: str
    skill_contract_id: str | None
    status: str
    boundary_signals: list[DominionControlBoundarySignal]
    findings: list[DominionGovernanceFinding]
    blockers: list[DominionBlocker]
    route_decisions: list[DominionRouteDecision]
    dominion_target_signal_ids: list[str]
    dominion_decision_signal_ids: list[str]
    future_gate_signal_ids: list[str]
    review_required_signal_ids: list[str]
    blocked_signal_ids: list[str]
    no_op_signal_ids: list[str]
    evidence_ref_ids: list[str]
    ready_for_v0316_dominion_target_decision: bool = False
    ready_for_execution: bool = False
    ready_for_skill_activation: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    ready_for_dominion_runtime: bool = False
    blocked_reasons: list[str] = field(default_factory=list)
    no_op_reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("dominion_output_id", self.dominion_output_id)
        _require_non_blank("dominion_input_id", self.dominion_input_id)
        _require_non_blank("status", self.status)
        _validate_object_list("boundary_signals", self.boundary_signals, DominionControlBoundarySignal)
        _validate_object_list("findings", self.findings, DominionGovernanceFinding)
        _validate_object_list("blockers", self.blockers, DominionBlocker)
        _validate_object_list("route_decisions", self.route_decisions, DominionRouteDecision)
        for name in (
            "dominion_target_signal_ids",
            "dominion_decision_signal_ids",
            "future_gate_signal_ids",
            "review_required_signal_ids",
            "blocked_signal_ids",
            "no_op_signal_ids",
            "evidence_ref_ids",
            "blocked_reasons",
        ):
            _validate_string_list(name, getattr(self, name))
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.5")
        if self.ready_for_skill_activation is not False:
            raise ValueError("ready_for_skill_activation must always be False in v0.31.5")
        if self.ready_for_external_control is not False:
            raise ValueError("ready_for_external_control must always be False in v0.31.5")
        if self.ready_for_authority_grant is not False:
            raise ValueError("ready_for_authority_grant must always be False in v0.31.5")
        if self.ready_for_dominion_runtime is not False:
            raise ValueError("ready_for_dominion_runtime must always be False in v0.31.5")
        if self.ready_for_v0316_dominion_target_decision and (
            not (self.dominion_target_signal_ids or self.dominion_decision_signal_ids) or self.blocked_reasons
        ):
            raise ValueError("v0.31.6 readiness requires target/decision signal ids and no blocked reasons")
        if _metadata_flag_true(
            self.metadata,
            {
                "dominion_target_creation",
                "dominion_decision_creation",
                "authority_grant",
                "external_control",
                "active_artifact_registration",
            },
        ):
            raise ValueError("DominionSkillOutput must remain foundation artifact only")

    @property
    def creates_dominion_target(self) -> bool:
        return False

    @property
    def creates_dominion_decision(self) -> bool:
        return False

    @property
    def grants_authority(self) -> bool:
        return False

    @property
    def active_artifact_registration(self) -> bool:
        return False


@dataclass(frozen=True)
class DominionSkillNoOpDecision:
    no_op_id: str
    dominion_input_id: str
    reason: str
    blocked_reasons: list[str] = field(default_factory=list)
    safe_alternatives: list[str] = field(default_factory=list)
    evidence_ref_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("no_op_id", self.no_op_id)
        _require_non_blank("dominion_input_id", self.dominion_input_id)
        _require_non_blank("reason", self.reason)
        _validate_string_list("blocked_reasons", self.blocked_reasons)
        _validate_string_list("safe_alternatives", self.safe_alternatives)
        _validate_string_list("evidence_ref_ids", self.evidence_ref_ids)
        if _metadata_flag_true(self.metadata, {"execution", "failure"}):
            raise ValueError("DominionSkillNoOpDecision must not imply execution or failure")

    @property
    def is_failure(self) -> bool:
        return False

    @property
    def executes_anything(self) -> bool:
        return False


@dataclass(frozen=True)
class DominionSkillRunPreview:
    run_preview_id: str
    dominion_input_id: str | None = None
    planned_steps: list[str] = field(default_factory=list)
    expected_artifacts: list[str] = field(default_factory=list)
    explicitly_not_performed: list[str] = field(default_factory=list)
    no_execution_guarantee: bool = True
    no_external_control_guarantee: bool = True
    no_authority_grant_guarantee: bool = True
    no_dominion_target_creation_guarantee: bool = True
    no_dominion_decision_creation_guarantee: bool = True
    no_registry_mutation_guarantee: bool = True
    no_memory_mutation_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        for name in (
            "no_execution_guarantee",
            "no_external_control_guarantee",
            "no_authority_grant_guarantee",
            "no_dominion_target_creation_guarantee",
            "no_dominion_decision_creation_guarantee",
            "no_registry_mutation_guarantee",
            "no_memory_mutation_guarantee",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.31.5")
        if _metadata_flag_true(self.metadata, {"execution", "external_control", "authority_grant"}):
            raise ValueError("DominionSkillRunPreview must not imply execution, external control, or authority grant")

    @property
    def executes_run(self) -> bool:
        return False


@dataclass(frozen=True)
class DominionSkillFoundationReport:
    foundation_report_id: str
    version: str
    dominion_contract_ref: str | None
    supported_source_kinds: list[DominionSkillSourceKind | str]
    supported_focus_kinds: list[DominionFocusKind | str]
    supported_routes: list[DominionRoute | str]
    supported_output_artifact_kinds: list[str]
    prohibited_runtime_actions: list[str]
    ready_for_v0316_dominion_target_decision: bool
    ready_for_execution: bool
    ready_for_skill_activation: bool
    ready_for_external_control: bool
    ready_for_authority_grant: bool
    summary: str
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("foundation_report_id", self.foundation_report_id)
        _validate_version_includes_v0315(self.version)
        if not isinstance(self.supported_source_kinds, list):
            raise TypeError("supported_source_kinds must be list[DominionSkillSourceKind | str]")
        for kind in self.supported_source_kinds:
            normalize_dominion_source_kind(kind)
        if not isinstance(self.supported_focus_kinds, list):
            raise TypeError("supported_focus_kinds must be list[DominionFocusKind | str]")
        for kind in self.supported_focus_kinds:
            normalize_dominion_focus_kind(kind)
        if not isinstance(self.supported_routes, list):
            raise TypeError("supported_routes must be list[DominionRoute | str]")
        for route in self.supported_routes:
            normalize_dominion_route(route)
        _validate_string_list("supported_output_artifact_kinds", self.supported_output_artifact_kinds)
        _validate_prohibited_actions(self.prohibited_runtime_actions)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.5")
        if self.ready_for_skill_activation is not False:
            raise ValueError("ready_for_skill_activation must always be False in v0.31.5")
        if self.ready_for_external_control is not False:
            raise ValueError("ready_for_external_control must always be False in v0.31.5")
        if self.ready_for_authority_grant is not False:
            raise ValueError("ready_for_authority_grant must always be False in v0.31.5")
        _require_non_blank("summary", self.summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("withdrawal_conditions", self.withdrawal_conditions)
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "external_control", "authority_grant"}):
            raise ValueError("DominionSkillFoundationReport must not imply runtime enablement")

    @property
    def runtime_enablement(self) -> bool:
        return False


@dataclass(frozen=True)
class V0315ReadinessReport:
    report_id: str
    version: str
    dominion_foundation_report_id: str
    summary: str
    ready_for_v0316_dominion_target_decision: bool
    ready_for_execution: bool = False
    ready_for_skill_activation: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    ready_for_dominion_runtime: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(V0315_PROHIBITED_UNTIL_LATER_GATE))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0315(self.version)
        _require_non_blank("dominion_foundation_report_id", self.dominion_foundation_report_id)
        _require_non_blank("summary", self.summary)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.5")
        if self.ready_for_skill_activation is not False:
            raise ValueError("ready_for_skill_activation must always be False in v0.31.5")
        if self.ready_for_external_control is not False:
            raise ValueError("ready_for_external_control must always be False in v0.31.5")
        if self.ready_for_authority_grant is not False:
            raise ValueError("ready_for_authority_grant must always be False in v0.31.5")
        if self.ready_for_dominion_runtime is not False:
            raise ValueError("ready_for_dominion_runtime must always be False in v0.31.5")
        for name in (
            "completed_items",
            "blocked_items",
            "future_track_items",
            "prohibited_until_later_gate",
            "evidence_refs",
            "withdrawal_conditions",
        ):
            _validate_string_list(name, getattr(self, name))
        missing = set(V0315_PROHIBITED_UNTIL_LATER_GATE) - set(self.prohibited_until_later_gate)
        if missing:
            raise ValueError(f"prohibited_until_later_gate missing v0.31.5 prohibitions: {sorted(missing)}")
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "external_control", "authority_grant"}):
            raise ValueError("V0315ReadinessReport must not imply runtime enablement")

    @property
    def runtime_enablement(self) -> bool:
        return False


def build_dominion_source_ref(
    source_ref_id: str,
    source_kind: DominionSkillSourceKind | str,
    source_id: str,
    target_id: str | None = None,
    candidate_id: str | None = None,
    capability_entry_id: str | None = None,
    internal_candidate_id: str | None = None,
    evidence_ref_ids: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> DominionSkillSourceRef:
    return DominionSkillSourceRef(
        source_ref_id=source_ref_id,
        source_kind=source_kind,
        source_id=source_id,
        target_id=target_id,
        candidate_id=candidate_id,
        capability_entry_id=capability_entry_id,
        internal_candidate_id=internal_candidate_id,
        evidence_ref_ids=list(evidence_ref_ids or []),
        metadata=dict(metadata or {}),
    )


def build_dominion_skill_input(
    dominion_input_id: str,
    task_summary: str,
    source_version: str,
    triad_input_id: str | None = None,
    source_refs: list[DominionSkillSourceRef] | None = None,
    internal_candidate_set_refs: list[str] | None = None,
    internalization_plan_refs: list[str] | None = None,
    digestion_output_refs: list[str] | None = None,
    route_decision_refs: list[str] | None = None,
    risk_map_refs: list[str] | None = None,
    gap_register_refs: list[str] | None = None,
    requested_focus: list[DominionFocusKind | str] | None = None,
    evidence_refs: list[str] | None = None,
    candidate_set: InternalCandidateSet | None = None,
    internalization_plan: InternalizationPlan | None = None,
    no_op_decision: InternalizationNoOpDecision | None = None,
    readiness_report: V0314ReadinessReport | None = None,
    metadata: dict[str, Any] | None = None,
) -> DominionSkillInput:
    resolved_source_refs = list(source_refs or [])
    resolved_candidate_set_refs = list(internal_candidate_set_refs or [])
    resolved_plan_refs = list(internalization_plan_refs or [])
    resolved_evidence_refs = list(evidence_refs or [])
    if candidate_set is not None:
        resolved_candidate_set_refs.append(candidate_set.candidate_set_id)
        resolved_evidence_refs.extend(ref.evidence_ref_id for ref in candidate_set.evidence_refs)
        resolved_source_refs.append(
            build_dominion_source_ref(
                f"dominion_source_ref:{candidate_set.candidate_set_id}",
                DominionSkillSourceKind.INTERNAL_CANDIDATE_SET,
                candidate_set.candidate_set_id,
                evidence_ref_ids=[ref.evidence_ref_id for ref in candidate_set.evidence_refs],
            )
        )
    if internalization_plan is not None:
        resolved_plan_refs.append(internalization_plan.plan_id)
        resolved_evidence_refs.extend(ref.evidence_ref_id for ref in internalization_plan.evidence_refs)
        resolved_source_refs.append(
            build_dominion_source_ref(
                f"dominion_source_ref:{internalization_plan.plan_id}",
                DominionSkillSourceKind.INTERNALIZATION_PLAN,
                internalization_plan.plan_id,
                evidence_ref_ids=[ref.evidence_ref_id for ref in internalization_plan.evidence_refs],
            )
        )
    if no_op_decision is not None:
        resolved_source_refs.append(
            build_dominion_source_ref(
                f"dominion_source_ref:{no_op_decision.no_op_id}",
                DominionSkillSourceKind.INTERNALIZATION_NO_OP_DECISION,
                no_op_decision.no_op_id,
                evidence_ref_ids=[ref.evidence_ref_id for ref in no_op_decision.evidence_refs],
            )
        )
    if readiness_report is not None:
        resolved_source_refs.append(
            build_dominion_source_ref(
                f"dominion_source_ref:{readiness_report.report_id}",
                DominionSkillSourceKind.V0314_READINESS_REPORT,
                readiness_report.report_id,
                evidence_ref_ids=[ref.evidence_ref_id for ref in readiness_report.evidence_refs],
            )
        )
        resolved_evidence_refs.extend(ref.evidence_ref_id for ref in readiness_report.evidence_refs)
    return DominionSkillInput(
        dominion_input_id=dominion_input_id,
        triad_input_id=triad_input_id,
        source_refs=resolved_source_refs,
        internal_candidate_set_refs=resolved_candidate_set_refs,
        internalization_plan_refs=resolved_plan_refs,
        digestion_output_refs=list(digestion_output_refs or []),
        route_decision_refs=list(route_decision_refs or []),
        risk_map_refs=list(risk_map_refs or []),
        gap_register_refs=list(gap_register_refs or []),
        requested_focus=list(requested_focus or []),
        task_summary=task_summary,
        source_version=source_version,
        evidence_refs=resolved_evidence_refs,
        prohibited_runtime_actions=list(V0315_REQUIRED_PROHIBITED_RUNTIME_ACTIONS),
        metadata=dict(metadata or {}),
    )


def classify_dominion_focus_from_source(source: Any) -> DominionFocusKind:
    text = " ".join(
        str(part)
        for part in (
            getattr(source, "source_kind", ""),
            getattr(source, "source_id", ""),
            getattr(source, "target_id", ""),
            getattr(source, "candidate_id", ""),
            getattr(source, "metadata", ""),
        )
    ).lower()
    for token, focus in (
        ("provider", DominionFocusKind.PROVIDER_BOUNDARY),
        ("network", DominionFocusKind.NETWORK_BOUNDARY),
        ("credential", DominionFocusKind.CREDENTIAL_BOUNDARY),
        ("command", DominionFocusKind.COMMAND_BOUNDARY),
        ("browser", DominionFocusKind.BROWSER_BOUNDARY),
        ("rpa", DominionFocusKind.RPA_BOUNDARY),
        ("gateway", DominionFocusKind.GATEWAY_BOUNDARY),
        ("delegation", DominionFocusKind.DELEGATION_BOUNDARY),
        ("memory", DominionFocusKind.MEMORY_BOUNDARY),
        ("raw_output", DominionFocusKind.RAW_OUTPUT_BOUNDARY),
        ("registry", DominionFocusKind.REGISTRY_BOUNDARY),
        ("policy", DominionFocusKind.POLICY_BOUNDARY),
        ("approval", DominionFocusKind.APPROVAL_BOUNDARY),
        ("audit", DominionFocusKind.AUDIT_BOUNDARY),
        ("rollback", DominionFocusKind.ROLLBACK_NO_OP_BOUNDARY),
        ("future", DominionFocusKind.FUTURE_GATE_BOUNDARY),
        ("ocel", DominionFocusKind.OCEL_TRACE_BOUNDARY),
        ("runtime", DominionFocusKind.EXTERNAL_RUNTIME_BOUNDARY),
    ):
        if token in text:
            return focus
    return DominionFocusKind.UNKNOWN


def infer_dominion_route_from_source_or_signal(source_or_signal: Any) -> DominionRoute:
    if isinstance(source_or_signal, DominionControlBoundarySignal):
        return normalize_dominion_route(source_or_signal.proposed_route)
    text = " ".join(
        str(part)
        for part in (
            getattr(source_or_signal, "route", ""),
            getattr(source_or_signal, "source_kind", ""),
            getattr(source_or_signal, "source_id", ""),
            getattr(source_or_signal, "status", ""),
            getattr(source_or_signal, "metadata", ""),
        )
    ).lower()
    if "dominion_target" in text:
        return DominionRoute.DOMINION_TARGET_SIGNAL
    if "dominion_decision" in text or "authority" in text:
        return DominionRoute.DOMINION_DECISION_SIGNAL
    if "future" in text:
        return DominionRoute.FUTURE_GATE_SIGNAL
    if "review" in text:
        return DominionRoute.REVIEW_REQUIRED
    if "blocked" in text:
        return DominionRoute.BLOCKED
    if "reject" in text:
        return DominionRoute.REJECT
    if "defer" in text:
        return DominionRoute.DEFER
    if "no_op" in text:
        return DominionRoute.NO_OP
    return DominionRoute.UNKNOWN


def build_dominion_control_boundary_signal(
    signal_id: str,
    focus_kind: DominionFocusKind | str,
    signal_kind: DominionSignalKind | str,
    proposed_route: DominionRoute | str,
    title: str,
    summary: str,
    source_ref_id: str | None = None,
    target_id: str | None = None,
    candidate_id: str | None = None,
    boundary_summary: str | None = None,
    risk_posture: DominionRiskPosture | str = DominionRiskPosture.UNKNOWN,
    boundary_posture: DominionBoundaryPosture | str = DominionBoundaryPosture.UNKNOWN,
    feasibility_posture: DominionFeasibilityPosture | str = DominionFeasibilityPosture.UNKNOWN,
    evidence_ref_ids: list[str] | None = None,
    blocker_ids: list[str] | None = None,
    assumptions: list[str] | None = None,
    limitations: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> DominionControlBoundarySignal:
    return DominionControlBoundarySignal(
        signal_id=signal_id,
        source_ref_id=source_ref_id,
        target_id=target_id,
        candidate_id=candidate_id,
        focus_kind=focus_kind,
        signal_kind=signal_kind,
        proposed_route=proposed_route,
        title=title,
        summary=summary,
        boundary_summary=boundary_summary,
        risk_posture=risk_posture,
        boundary_posture=boundary_posture,
        feasibility_posture=feasibility_posture,
        evidence_ref_ids=list(evidence_ref_ids or []),
        blocker_ids=list(blocker_ids or []),
        assumptions=list(assumptions or []),
        limitations=list(limitations or []),
        metadata=dict(metadata or {}),
    )


def build_dominion_governance_finding(
    finding_id: str,
    dominion_input_id: str,
    route: DominionRoute | str,
    summary: str,
    signal_ids: list[str] | None = None,
    risk_posture: DominionRiskPosture | str = DominionRiskPosture.UNKNOWN,
    boundary_posture: DominionBoundaryPosture | str = DominionBoundaryPosture.UNKNOWN,
    feasibility_posture: DominionFeasibilityPosture | str = DominionFeasibilityPosture.UNKNOWN,
    evidence_ref_ids: list[str] | None = None,
    blocked_reasons: list[str] | None = None,
    recommended_next_stage: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> DominionGovernanceFinding:
    return DominionGovernanceFinding(
        finding_id=finding_id,
        dominion_input_id=dominion_input_id,
        signal_ids=list(signal_ids or []),
        route=route,
        summary=summary,
        risk_posture=risk_posture,
        boundary_posture=boundary_posture,
        feasibility_posture=feasibility_posture,
        evidence_ref_ids=list(evidence_ref_ids or []),
        blocked_reasons=list(blocked_reasons or []),
        recommended_next_stage=recommended_next_stage,
        metadata=dict(metadata or {}),
    )


def build_dominion_blocker(
    blocker_id: str,
    blocker_kind: DominionBlockerKind | str,
    description: str,
    source_ref_id: str | None = None,
    target_id: str | None = None,
    candidate_id: str | None = None,
    blocks_v0316: bool = False,
    routes_to_future_gate: bool = False,
    routes_to_no_op: bool = False,
    evidence_ref_ids: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> DominionBlocker:
    return DominionBlocker(
        blocker_id=blocker_id,
        blocker_kind=blocker_kind,
        source_ref_id=source_ref_id,
        target_id=target_id,
        candidate_id=candidate_id,
        description=description,
        blocks_v0316=blocks_v0316,
        routes_to_future_gate=routes_to_future_gate,
        routes_to_no_op=routes_to_no_op,
        evidence_ref_ids=list(evidence_ref_ids or []),
        metadata=dict(metadata or {}),
    )


def build_dominion_route_decision(
    route_decision_id: str,
    dominion_input_id: str,
    route: DominionRoute | str,
    reason: str,
    signal_ids: list[str] | None = None,
    blocker_ids: list[str] | None = None,
    evidence_ref_ids: list[str] | None = None,
    ready_for_v0316_dominion_target_decision: bool = False,
    metadata: dict[str, Any] | None = None,
) -> DominionRouteDecision:
    return DominionRouteDecision(
        route_decision_id=route_decision_id,
        dominion_input_id=dominion_input_id,
        route=route,
        signal_ids=list(signal_ids or []),
        blocker_ids=list(blocker_ids or []),
        reason=reason,
        evidence_ref_ids=list(evidence_ref_ids or []),
        ready_for_v0316_dominion_target_decision=ready_for_v0316_dominion_target_decision,
        ready_for_execution=False,
        ready_for_external_control=False,
        ready_for_authority_grant=False,
        ready_for_dominion_target_creation=False,
        ready_for_dominion_decision_creation=False,
        metadata=dict(metadata or {}),
    )


def build_dominion_skill_output(
    dominion_output_id: str,
    dominion_input_id: str,
    status: str,
    boundary_signals: list[DominionControlBoundarySignal] | None = None,
    findings: list[DominionGovernanceFinding] | None = None,
    blockers: list[DominionBlocker] | None = None,
    route_decisions: list[DominionRouteDecision] | None = None,
    dominion_target_signal_ids: list[str] | None = None,
    dominion_decision_signal_ids: list[str] | None = None,
    future_gate_signal_ids: list[str] | None = None,
    review_required_signal_ids: list[str] | None = None,
    blocked_signal_ids: list[str] | None = None,
    no_op_signal_ids: list[str] | None = None,
    evidence_ref_ids: list[str] | None = None,
    ready_for_v0316_dominion_target_decision: bool = False,
    skill_contract_id: str | None = None,
    blocked_reasons: list[str] | None = None,
    no_op_reason: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> DominionSkillOutput:
    return DominionSkillOutput(
        dominion_output_id=dominion_output_id,
        dominion_input_id=dominion_input_id,
        skill_contract_id=skill_contract_id,
        status=status,
        boundary_signals=list(boundary_signals or []),
        findings=list(findings or []),
        blockers=list(blockers or []),
        route_decisions=list(route_decisions or []),
        dominion_target_signal_ids=list(dominion_target_signal_ids or []),
        dominion_decision_signal_ids=list(dominion_decision_signal_ids or []),
        future_gate_signal_ids=list(future_gate_signal_ids or []),
        review_required_signal_ids=list(review_required_signal_ids or []),
        blocked_signal_ids=list(blocked_signal_ids or []),
        no_op_signal_ids=list(no_op_signal_ids or []),
        evidence_ref_ids=list(evidence_ref_ids or []),
        ready_for_v0316_dominion_target_decision=ready_for_v0316_dominion_target_decision,
        ready_for_execution=False,
        ready_for_skill_activation=False,
        ready_for_external_control=False,
        ready_for_authority_grant=False,
        ready_for_dominion_runtime=False,
        blocked_reasons=list(blocked_reasons or []),
        no_op_reason=no_op_reason,
        metadata=dict(metadata or {}),
    )


def build_dominion_no_op_decision(
    no_op_id: str,
    dominion_input_id: str,
    reason: str,
    blocked_reasons: list[str] | None = None,
    safe_alternatives: list[str] | None = None,
    evidence_ref_ids: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> DominionSkillNoOpDecision:
    return DominionSkillNoOpDecision(
        no_op_id=no_op_id,
        dominion_input_id=dominion_input_id,
        reason=reason,
        blocked_reasons=list(blocked_reasons or []),
        safe_alternatives=list(safe_alternatives or []),
        evidence_ref_ids=list(evidence_ref_ids or []),
        metadata=dict(metadata or {}),
    )


def build_dominion_run_preview(
    run_preview_id: str,
    dominion_input_id: str | None = None,
    planned_steps: list[str] | None = None,
    expected_artifacts: list[str] | None = None,
    explicitly_not_performed: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> DominionSkillRunPreview:
    return DominionSkillRunPreview(
        run_preview_id=run_preview_id,
        dominion_input_id=dominion_input_id,
        planned_steps=list(planned_steps or ["read available dominion source refs", "produce boundary signals"]),
        expected_artifacts=list(
            expected_artifacts
            or [
                "DominionSkillInput",
                "DominionControlBoundarySignal",
                "DominionGovernanceFinding",
                "DominionBlocker",
                "DominionRouteDecision",
                "DominionSkillOutput",
            ]
        ),
        explicitly_not_performed=list(
            explicitly_not_performed
            or [
                "execution",
                "external_control",
                "authority_grant",
                "dominion_target_creation",
                "dominion_decision_creation",
                "registry_mutation",
                "memory_mutation",
            ]
        ),
        metadata=dict(metadata or {}),
    )


def build_dominion_skill_foundation_report(
    dominion_contract_ref: str | None = "internal_triad_skill_contract:dominion:v0.31.0",
    ready_for_v0316_dominion_target_decision: bool = True,
) -> DominionSkillFoundationReport:
    return DominionSkillFoundationReport(
        foundation_report_id="dominion_skill_foundation_report:v0.31.5",
        version=V0315_VERSION,
        dominion_contract_ref=dominion_contract_ref,
        supported_source_kinds=[kind for kind in DominionSkillSourceKind],
        supported_focus_kinds=[kind for kind in DominionFocusKind],
        supported_routes=[route for route in DominionRoute],
        supported_output_artifact_kinds=[
            "dominion_skill_input",
            "dominion_control_boundary_signal",
            "dominion_governance_finding",
            "dominion_blocker",
            "dominion_route_decision",
            "dominion_skill_output",
            "dominion_run_preview",
            "dominion_no_op_decision",
        ],
        prohibited_runtime_actions=list(V0315_REQUIRED_PROHIBITED_RUNTIME_ACTIONS),
        ready_for_v0316_dominion_target_decision=ready_for_v0316_dominion_target_decision,
        ready_for_execution=False,
        ready_for_skill_activation=False,
        ready_for_external_control=False,
        ready_for_authority_grant=False,
        summary="Dominion Skill Foundation defines boundary and governance signals for later design stages only; no control or authority is enabled.",
        evidence_refs=["v0.31.4 InternalCandidateSet", "v0.31.0 DominionSkillContract"],
        withdrawal_conditions=[
            "dominion route signals are treated as active targets or decisions",
            "route decisions grant authority",
            "external control or runtime execution is introduced",
            "ready_for_execution, ready_for_external_control, or ready_for_authority_grant becomes true",
        ],
        metadata={"foundation_is_runtime_enablement": False},
    )


def build_v0315_readiness_report(foundation_report: DominionSkillFoundationReport) -> V0315ReadinessReport:
    return V0315ReadinessReport(
        report_id="v0315_readiness_report:dominion_skill_foundation",
        version=V0315_VERSION,
        dominion_foundation_report_id=foundation_report.foundation_report_id,
        summary="v0.31.5 is ready for v0.31.6 design-stage dominion target/decision modeling only; not execution or control.",
        ready_for_v0316_dominion_target_decision=foundation_report.ready_for_v0316_dominion_target_decision,
        ready_for_execution=False,
        ready_for_skill_activation=False,
        ready_for_external_control=False,
        ready_for_authority_grant=False,
        ready_for_dominion_runtime=False,
        completed_items=[
            "dominion source taxonomy",
            "dominion focus taxonomy",
            "dominion route taxonomy",
            "dominion input/source ref models",
            "control boundary signal and route decision models",
            foundation_report.foundation_report_id,
        ],
        blocked_items=[],
        future_track_items=[
            "external control",
            "authority grant",
            "dominion target creation",
            "dominion decision creation",
            "provider/network/credential/runtime control",
        ],
        evidence_refs=list(foundation_report.evidence_refs),
        withdrawal_conditions=list(foundation_report.withdrawal_conditions),
        metadata={"readiness_report_is_runtime_enablement": False},
    )


def dominion_input_preserves_no_execution(dominion_input: DominionSkillInput) -> bool:
    return (
        dominion_input.is_execution_request is False
        and not (set(V0315_REQUIRED_PROHIBITED_RUNTIME_ACTIONS) - set(dominion_input.prohibited_runtime_actions))
    )


def dominion_output_preserves_no_execution(output: DominionSkillOutput) -> bool:
    return (
        output.ready_for_execution is False
        and output.ready_for_skill_activation is False
        and output.ready_for_external_control is False
        and output.ready_for_authority_grant is False
        and output.ready_for_dominion_runtime is False
        and output.active_artifact_registration is False
    )


def dominion_output_is_not_target_or_decision(output: DominionSkillOutput) -> bool:
    return output.creates_dominion_target is False and output.creates_dominion_decision is False


def dominion_output_grants_no_authority(output: DominionSkillOutput) -> bool:
    return output.grants_authority is False and output.ready_for_authority_grant is False


def dominion_run_preview_preserves_no_execution(preview: DominionSkillRunPreview) -> bool:
    return (
        preview.no_execution_guarantee is True
        and preview.no_external_control_guarantee is True
        and preview.no_authority_grant_guarantee is True
        and preview.no_dominion_target_creation_guarantee is True
        and preview.no_dominion_decision_creation_guarantee is True
        and preview.no_registry_mutation_guarantee is True
        and preview.no_memory_mutation_guarantee is True
        and preview.executes_run is False
    )


def dominion_foundation_is_not_runtime_ready(report: DominionSkillFoundationReport | V0315ReadinessReport) -> bool:
    base = (
        report.ready_for_execution is False
        and report.ready_for_skill_activation is False
        and report.ready_for_external_control is False
        and report.ready_for_authority_grant is False
        and report.runtime_enablement is False
    )
    if isinstance(report, V0315ReadinessReport):
        return base and report.ready_for_dominion_runtime is False
    return base
