from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from chanta_core.external_dominion.dominion_levels import DominionLevel, normalize_dominion_level
from chanta_core.internal_triad.boundaries import _require_non_blank, _validate_string_list
from chanta_core.internal_triad.dominion import (
    DominionControlBoundarySignal,
    DominionRoute,
    DominionRouteDecision,
    DominionSkillOutput,
    V0315_REQUIRED_PROHIBITED_RUNTIME_ACTIONS,
)
from chanta_core.internal_triad.skill_kinds import V0310_TRACK


V0316_VERSION = "v0.31.6"
V0316_RELEASE_NAME = "v0.31.6 Dominion Target / Dominion Decision"
V0316_TRACK = V0310_TRACK

V0316_REQUIRED_PROHIBITED_RUNTIME_ACTIONS = [
    *V0315_REQUIRED_PROHIBITED_RUNTIME_ACTIONS,
    "provider_invocation",
    "network_access",
    "credential_access",
    "command_execution",
    "browser_runtime_control",
    "rpa_runtime_control",
    "gateway_control",
    "delegation_runtime",
    "d4_d9_grant",
]

V0316_PROHIBITED_UNTIL_LATER_GATE = [
    "external_control",
    "authority_grant",
    "external_execution",
    "provider_invocation",
    "network",
    "credential",
    "command",
    "browser",
    "rpa",
    "gateway",
    "packet_send",
    "delegation_runtime",
    "registry_mutation",
    "memory_mutation",
    "rollback",
    "retry",
    "D4-D9",
]


class InternalDominionTargetKind(StrEnum):
    EXTERNAL_RUNTIME_TARGET = "external_runtime_target"
    EXTERNAL_AGENT_HARNESS_TARGET = "external_agent_harness_target"
    EXTERNAL_PROVIDER_TARGET = "external_provider_target"
    EXTERNAL_GATEWAY_TARGET = "external_gateway_target"
    EXTERNAL_RPA_TARGET = "external_rpa_target"
    BROWSER_RUNTIME_TARGET = "browser_runtime_target"
    COMMAND_RUNTIME_TARGET = "command_runtime_target"
    CREDENTIAL_BOUND_TARGET = "credential_bound_target"
    NETWORK_BOUND_TARGET = "network_bound_target"
    MEMORY_BOUNDARY_TARGET = "memory_boundary_target"
    REGISTRY_BOUNDARY_TARGET = "registry_boundary_target"
    POLICY_BOUNDARY_TARGET = "policy_boundary_target"
    DELEGATION_BOUNDARY_TARGET = "delegation_boundary_target"
    FUTURE_TRACK_TARGET = "future_track_target"
    UNKNOWN = "unknown"


class InternalDominionTargetStatus(StrEnum):
    UNKNOWN = "unknown"
    TARGET_CANDIDATE = "target_candidate"
    TARGET_RECORDED = "target_recorded"
    REQUIRES_REVIEW = "requires_review"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class InternalDominionDecisionType(StrEnum):
    DENY = "deny"
    DEFER = "defer"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    REQUIRE_FUTURE_GATE = "require_future_gate"
    RECORD_TARGET_ONLY = "record_target_only"
    PLAN_ONLY = "plan_only"
    SIMULATE_ONLY = "simulate_only"
    BLOCK = "block"
    FUTURE_TRACK = "future_track"


class DominionControlBoundaryKind(StrEnum):
    NO_EXTERNAL_CONTROL = "no_external_control"
    NO_PROVIDER_INVOCATION = "no_provider_invocation"
    NO_NETWORK_ACCESS = "no_network_access"
    NO_CREDENTIAL_ACCESS = "no_credential_access"
    NO_COMMAND_EXECUTION = "no_command_execution"
    NO_BROWSER_AUTOMATION = "no_browser_automation"
    NO_RPA_CONTROL = "no_rpa_control"
    NO_GATEWAY_CONTROL = "no_gateway_control"
    NO_PACKET_SEND = "no_packet_send"
    NO_RAW_OUTPUT_PERSISTENCE = "no_raw_output_persistence"
    NO_MEMORY_MUTATION = "no_memory_mutation"
    NO_REGISTRY_MUTATION = "no_registry_mutation"
    NO_POLICY_ACTIVATION = "no_policy_activation"
    APPROVAL_REQUIRED = "approval_required"
    AUDIT_REQUIRED = "audit_required"
    RESULT_BOUNDARY_REQUIRED = "result_boundary_required"
    ROLLBACK_NO_OP_REQUIRED = "rollback_no_op_required"
    OCEL_TRACE_REQUIRED = "ocel_trace_required"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class DominionFutureGateKind(StrEnum):
    EXTERNAL_EXECUTION_GATE = "external_execution_gate"
    PROVIDER_INVOCATION_GATE = "provider_invocation_gate"
    NETWORK_ACCESS_GATE = "network_access_gate"
    CREDENTIAL_ACCESS_GATE = "credential_access_gate"
    COMMAND_EXECUTION_GATE = "command_execution_gate"
    BROWSER_RUNTIME_GATE = "browser_runtime_gate"
    RPA_RUNTIME_GATE = "rpa_runtime_gate"
    GATEWAY_CONTROL_GATE = "gateway_control_gate"
    EXTERNAL_AGENT_DELEGATION_GATE = "external_agent_delegation_gate"
    REGISTRY_MUTATION_GATE = "registry_mutation_gate"
    MEMORY_MUTATION_GATE = "memory_mutation_gate"
    POLICY_ACTIVATION_GATE = "policy_activation_gate"
    TOOL_EXECUTION_GATE = "tool_execution_gate"
    MISSION_INSTALLATION_GATE = "mission_installation_gate"
    PRODUCTION_CERTIFICATION_GATE = "production_certification_gate"
    UNKNOWN = "unknown"


class DominionDecisionReasonKind(StrEnum):
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    HIGH_RISK_SURFACE = "high_risk_surface"
    MISSING_BOUNDARY = "missing_boundary"
    MISSING_AUDIT = "missing_audit"
    MISSING_APPROVAL = "missing_approval"
    MISSING_RESULT_BOUNDARY = "missing_result_boundary"
    MISSING_ROLLBACK_NO_OP = "missing_rollback_no_op"
    INCOMPATIBLE_WITH_OCEL_SPINE = "incompatible_with_ocel_spine"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    BLOCKED_BY_POLICY = "blocked_by_policy"
    NO_OP_PREFERRED = "no_op_preferred"
    DESCRIPTIVE_RECORD_ONLY = "descriptive_record_only"
    CONSERVATIVE_ROUTING = "conservative_routing"
    UNKNOWN = "unknown"


class DominionControlSurface(StrEnum):
    EXTERNAL_RUNTIME = "external_runtime"
    PROVIDER = "provider"
    NETWORK = "network"
    CREDENTIAL = "credential"
    COMMAND = "command"
    BROWSER = "browser"
    RPA = "rpa"
    GATEWAY = "gateway"
    PACKET = "packet"
    DELEGATION = "delegation"
    MEMORY = "memory"
    REGISTRY = "registry"
    POLICY = "policy"
    TOOL = "tool"
    MISSION = "mission"
    OCEL_TRACE = "ocel_trace"
    UNKNOWN = "unknown"


class DominionRiskSurface(StrEnum):
    PRIVATE_DATA = "private_data"
    CREDENTIAL_EXPOSURE = "credential_exposure"
    NETWORK_SIDE_EFFECT = "network_side_effect"
    COMMAND_EXECUTION = "command_execution"
    PROVIDER_INVOCATION = "provider_invocation"
    BROWSER_AUTOMATION = "browser_automation"
    RPA_CONTROL = "rpa_control"
    GATEWAY_SEND = "gateway_send"
    EXTERNAL_DELEGATION = "external_delegation"
    MEMORY_CONTAMINATION = "memory_contamination"
    RAW_OUTPUT_PERSISTENCE = "raw_output_persistence"
    REGISTRY_MUTATION = "registry_mutation"
    POLICY_ACTIVATION = "policy_activation"
    MISSION_INSTALLATION = "mission_installation"
    TOOL_EXECUTION = "tool_execution"
    OCEL_SCHEMA_DRIFT = "ocel_schema_drift"
    UNKNOWN = "unknown"


def _metadata_flag_true(metadata: dict[str, Any], names: set[str]) -> bool:
    return isinstance(metadata, dict) and any(metadata.get(name) is True for name in names)


def _validate_object_list(name: str, values: list[Any], expected_type: type) -> None:
    if not isinstance(values, list) or not all(isinstance(item, expected_type) for item in values):
        raise TypeError(f"{name} must be list[{expected_type.__name__}]")


def _validate_version_includes_v0316(version: str) -> None:
    _require_non_blank("version", version)
    if V0316_VERSION not in version:
        raise ValueError("version must include v0.31.6")


def _validate_level_at_or_below_d3(name: str, level: DominionLevel | int | str | None) -> None:
    if level is not None and normalize_dominion_level(level) > DominionLevel.D3_SIMULATE:
        raise ValueError(f"{name} must be None or <= D3_SIMULATE in v0.31.6")


def _validate_prohibited_actions(actions: list[str]) -> None:
    _validate_string_list("prohibited_runtime_actions", actions)
    missing = set(V0316_REQUIRED_PROHIBITED_RUNTIME_ACTIONS) - set(actions)
    if missing:
        raise ValueError(f"prohibited_runtime_actions missing v0.31.6 prohibitions: {sorted(missing)}")


def normalize_internal_dominion_target_kind(value: InternalDominionTargetKind | str) -> InternalDominionTargetKind:
    if isinstance(value, InternalDominionTargetKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("internal dominion target kind must not be blank")
        return InternalDominionTargetKind(stripped)
    raise TypeError(f"unsupported internal dominion target kind: {value!r}")


def normalize_internal_dominion_target_status(value: InternalDominionTargetStatus | str) -> InternalDominionTargetStatus:
    if isinstance(value, InternalDominionTargetStatus):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("internal dominion target status must not be blank")
        return InternalDominionTargetStatus(stripped)
    raise TypeError(f"unsupported internal dominion target status: {value!r}")


def normalize_internal_dominion_decision_type(value: InternalDominionDecisionType | str) -> InternalDominionDecisionType:
    if isinstance(value, InternalDominionDecisionType):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("internal dominion decision type must not be blank")
        return InternalDominionDecisionType(stripped)
    raise TypeError(f"unsupported internal dominion decision type: {value!r}")


def normalize_dominion_control_boundary_kind(value: DominionControlBoundaryKind | str) -> DominionControlBoundaryKind:
    if isinstance(value, DominionControlBoundaryKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("dominion control boundary kind must not be blank")
        return DominionControlBoundaryKind(stripped)
    raise TypeError(f"unsupported dominion control boundary kind: {value!r}")


def normalize_dominion_future_gate_kind(value: DominionFutureGateKind | str) -> DominionFutureGateKind:
    if isinstance(value, DominionFutureGateKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("dominion future gate kind must not be blank")
        return DominionFutureGateKind(stripped)
    raise TypeError(f"unsupported dominion future gate kind: {value!r}")


def normalize_dominion_decision_reason_kind(value: DominionDecisionReasonKind | str) -> DominionDecisionReasonKind:
    if isinstance(value, DominionDecisionReasonKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("dominion decision reason kind must not be blank")
        return DominionDecisionReasonKind(stripped)
    raise TypeError(f"unsupported dominion decision reason kind: {value!r}")


def normalize_dominion_control_surface(value: DominionControlSurface | str) -> DominionControlSurface:
    if isinstance(value, DominionControlSurface):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("dominion control surface must not be blank")
        return DominionControlSurface(stripped)
    raise TypeError(f"unsupported dominion control surface: {value!r}")


def normalize_dominion_risk_surface(value: DominionRiskSurface | str) -> DominionRiskSurface:
    if isinstance(value, DominionRiskSurface):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("dominion risk surface must not be blank")
        return DominionRiskSurface(stripped)
    raise TypeError(f"unsupported dominion risk surface: {value!r}")


def internal_dominion_target_kind_controls_runtime(_: InternalDominionTargetKind | str) -> bool:
    normalize_internal_dominion_target_kind(_)
    return False


def internal_dominion_decision_type_grants_execution(_: InternalDominionDecisionType | str) -> bool:
    normalize_internal_dominion_decision_type(_)
    return False


@dataclass(frozen=True)
class DominionTargetSourceRef:
    source_ref_id: str
    source_kind: str
    source_id: str
    target_id: str | None = None
    candidate_id: str | None = None
    signal_id: str | None = None
    finding_id: str | None = None
    route_decision_id: str | None = None
    evidence_ref_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        _require_non_blank("source_kind", self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _validate_string_list("evidence_ref_ids", self.evidence_ref_ids)
        if _metadata_flag_true(self.metadata, {"source_fetch", "source_ref_fetch", "url_fetch"}):
            raise ValueError("DominionTargetSourceRef must not imply source fetch")

    @property
    def fetches_source(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalDominionTarget:
    dominion_target_id: str
    source_external_target_id: str | None
    target_kind: InternalDominionTargetKind | str
    status: InternalDominionTargetStatus | str
    title: str
    summary: str
    source_refs: list[DominionTargetSourceRef]
    control_surfaces: list[DominionControlSurface | str]
    risk_surfaces: list[DominionRiskSurface | str]
    control_boundary_ids: list[str]
    future_gate_ids: list[str]
    evidence_ref_ids: list[str]
    max_allowed_level: DominionLevel | int | str | None = DominionLevel.D3_SIMULATE
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(V0316_REQUIRED_PROHIBITED_RUNTIME_ACTIONS))
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("dominion_target_id", self.dominion_target_id)
        normalize_internal_dominion_target_kind(self.target_kind)
        normalize_internal_dominion_target_status(self.status)
        _require_non_blank("title", self.title)
        _require_non_blank("summary", self.summary)
        _validate_object_list("source_refs", self.source_refs, DominionTargetSourceRef)
        if not isinstance(self.control_surfaces, list):
            raise TypeError("control_surfaces must be list[DominionControlSurface | str]")
        for surface in self.control_surfaces:
            normalize_dominion_control_surface(surface)
        if not isinstance(self.risk_surfaces, list):
            raise TypeError("risk_surfaces must be list[DominionRiskSurface | str]")
        for surface in self.risk_surfaces:
            normalize_dominion_risk_surface(surface)
        for name in ("control_boundary_ids", "future_gate_ids", "evidence_ref_ids", "assumptions", "limitations"):
            _validate_string_list(name, getattr(self, name))
        _validate_level_at_or_below_d3("max_allowed_level", self.max_allowed_level)
        _validate_prohibited_actions(self.prohibited_runtime_actions)
        if self.ready_for_external_control is not False:
            raise ValueError("ready_for_external_control must always be False in v0.31.6")
        if self.ready_for_authority_grant is not False:
            raise ValueError("ready_for_authority_grant must always be False in v0.31.6")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.6")
        if _metadata_flag_true(self.metadata, {"external_control", "authority_grant", "execution", "live_runtime_ready"}):
            raise ValueError("InternalDominionTarget must remain governance artifact only")

    @property
    def external_runtime_control(self) -> bool:
        return False

    @property
    def governance_artifact_only(self) -> bool:
        return True


@dataclass(frozen=True)
class DominionControlBoundary:
    boundary_id: str
    dominion_target_id: str
    boundary_kind: DominionControlBoundaryKind | str
    control_surfaces: list[DominionControlSurface | str] = field(default_factory=list)
    risk_surfaces: list[DominionRiskSurface | str] = field(default_factory=list)
    required_evidence_refs: list[str] = field(default_factory=list)
    required_reviews: list[str] = field(default_factory=list)
    required_future_gates: list[DominionFutureGateKind | str] = field(default_factory=list)
    description: str = "Boundary blocks execution, external control, and authority grant until later gates."
    blocks_execution: bool = True
    blocks_external_control: bool = True
    blocks_authority_grant: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_id", self.boundary_id)
        _require_non_blank("dominion_target_id", self.dominion_target_id)
        normalize_dominion_control_boundary_kind(self.boundary_kind)
        if not isinstance(self.control_surfaces, list):
            raise TypeError("control_surfaces must be list[DominionControlSurface | str]")
        for surface in self.control_surfaces:
            normalize_dominion_control_surface(surface)
        if not isinstance(self.risk_surfaces, list):
            raise TypeError("risk_surfaces must be list[DominionRiskSurface | str]")
        for surface in self.risk_surfaces:
            normalize_dominion_risk_surface(surface)
        _validate_string_list("required_evidence_refs", self.required_evidence_refs)
        _validate_string_list("required_reviews", self.required_reviews)
        if not isinstance(self.required_future_gates, list):
            raise TypeError("required_future_gates must be list[DominionFutureGateKind | str]")
        for gate in self.required_future_gates:
            normalize_dominion_future_gate_kind(gate)
        _require_non_blank("description", self.description)
        if self.blocks_execution is not True:
            raise ValueError("blocks_execution must be True in v0.31.6")
        if self.blocks_external_control is not True:
            raise ValueError("blocks_external_control must be True in v0.31.6")
        if self.blocks_authority_grant is not True:
            raise ValueError("blocks_authority_grant must be True in v0.31.6")
        if _metadata_flag_true(self.metadata, {"permission", "permits_execution", "permits_external_control"}):
            raise ValueError("DominionControlBoundary must not imply permission")

    @property
    def is_permission(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalDominionDecision:
    dominion_decision_id: str
    dominion_target_id: str
    decision_type: InternalDominionDecisionType | str
    reason_kind: DominionDecisionReasonKind | str
    reason: str
    granted_level: DominionLevel | int | str | None = None
    required_boundaries: list[DominionControlBoundaryKind | str] = field(default_factory=list)
    required_future_gates: list[DominionFutureGateKind | str] = field(default_factory=list)
    required_reviews: list[str] = field(default_factory=list)
    evidence_ref_ids: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    approved_for_execution: bool = False
    approved_for_external_control: bool = False
    authority_granted: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("dominion_decision_id", self.dominion_decision_id)
        _require_non_blank("dominion_target_id", self.dominion_target_id)
        normalize_internal_dominion_decision_type(self.decision_type)
        normalize_dominion_decision_reason_kind(self.reason_kind)
        _require_non_blank("reason", self.reason)
        _validate_level_at_or_below_d3("granted_level", self.granted_level)
        if not isinstance(self.required_boundaries, list):
            raise TypeError("required_boundaries must be list[DominionControlBoundaryKind | str]")
        for boundary in self.required_boundaries:
            normalize_dominion_control_boundary_kind(boundary)
        if not isinstance(self.required_future_gates, list):
            raise TypeError("required_future_gates must be list[DominionFutureGateKind | str]")
        for gate in self.required_future_gates:
            normalize_dominion_future_gate_kind(gate)
        for name in ("required_reviews", "evidence_ref_ids", "blocked_reasons", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        if self.approved_for_execution is not False:
            raise ValueError("approved_for_execution must always be False in v0.31.6")
        if self.approved_for_external_control is not False:
            raise ValueError("approved_for_external_control must always be False in v0.31.6")
        if self.authority_granted is not False:
            raise ValueError("authority_granted must always be False in v0.31.6")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.6")
        if _metadata_flag_true(self.metadata, {"execution", "external_control", "authority_grant", "d4_d9_grant"}):
            raise ValueError("InternalDominionDecision must not imply execution or authority grant")

    @property
    def is_execution(self) -> bool:
        return False

    @property
    def grants_authority(self) -> bool:
        return False


@dataclass(frozen=True)
class DominionFutureGateItem:
    future_gate_id: str
    dominion_target_id: str | None
    gate_kind: DominionFutureGateKind | str
    reason: str
    blocked_until: str | None = None
    required_artifacts: list[str] = field(default_factory=list)
    required_reviews: list[str] = field(default_factory=list)
    prohibited_until_satisfied: list[str] = field(default_factory=lambda: list(V0316_PROHIBITED_UNTIL_LATER_GATE))
    evidence_ref_ids: list[str] = field(default_factory=list)
    ready_now: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("future_gate_id", self.future_gate_id)
        normalize_dominion_future_gate_kind(self.gate_kind)
        _require_non_blank("reason", self.reason)
        for name in ("required_artifacts", "required_reviews", "prohibited_until_satisfied", "evidence_ref_ids"):
            _validate_string_list(name, getattr(self, name))
        if self.ready_now is not False:
            raise ValueError("ready_now must always be False in v0.31.6")
        if _metadata_flag_true(self.metadata, {"future_readiness", "approval", "implementation"}):
            raise ValueError("DominionFutureGateItem must not imply readiness, approval, or implementation")

    @property
    def is_readiness(self) -> bool:
        return False


@dataclass(frozen=True)
class DominionNoOpDecision:
    no_op_id: str
    dominion_target_id: str | None
    reason: str
    safe_alternatives: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    evidence_ref_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("no_op_id", self.no_op_id)
        _require_non_blank("reason", self.reason)
        _validate_string_list("safe_alternatives", self.safe_alternatives)
        _validate_string_list("blocked_reasons", self.blocked_reasons)
        _validate_string_list("evidence_ref_ids", self.evidence_ref_ids)
        if _metadata_flag_true(self.metadata, {"failure", "execution"}):
            raise ValueError("DominionNoOpDecision must not imply failure or execution")

    @property
    def is_failure(self) -> bool:
        return False

    @property
    def executes_anything(self) -> bool:
        return False


@dataclass(frozen=True)
class DominionTargetDecisionSet:
    decision_set_id: str
    source_dominion_output_id: str | None
    targets: list[InternalDominionTarget]
    boundaries: list[DominionControlBoundary]
    decisions: list[InternalDominionDecision]
    future_gates: list[DominionFutureGateItem]
    no_op_decisions: list[DominionNoOpDecision]
    evidence_ref_ids: list[str] = field(default_factory=list)
    ready_for_v0317_ocel_trace_integration: bool = False
    ready_for_execution: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("decision_set_id", self.decision_set_id)
        _validate_object_list("targets", self.targets, InternalDominionTarget)
        _validate_object_list("boundaries", self.boundaries, DominionControlBoundary)
        _validate_object_list("decisions", self.decisions, InternalDominionDecision)
        _validate_object_list("future_gates", self.future_gates, DominionFutureGateItem)
        _validate_object_list("no_op_decisions", self.no_op_decisions, DominionNoOpDecision)
        _validate_string_list("evidence_ref_ids", self.evidence_ref_ids)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.6")
        if self.ready_for_external_control is not False:
            raise ValueError("ready_for_external_control must always be False in v0.31.6")
        if self.ready_for_authority_grant is not False:
            raise ValueError("ready_for_authority_grant must always be False in v0.31.6")
        if _metadata_flag_true(self.metadata, {"runtime_registry", "external_control", "authority_grant", "execution"}):
            raise ValueError("DominionTargetDecisionSet must not imply runtime registry or runtime control")

    @property
    def runtime_registry(self) -> bool:
        return False


@dataclass(frozen=True)
class DominionDecisionRunPreview:
    run_preview_id: str
    decision_set_id: str | None = None
    planned_steps: list[str] = field(default_factory=list)
    expected_artifacts: list[str] = field(default_factory=list)
    explicitly_not_performed: list[str] = field(default_factory=list)
    no_execution_guarantee: bool = True
    no_external_control_guarantee: bool = True
    no_authority_grant_guarantee: bool = True
    no_provider_invocation_guarantee: bool = True
    no_network_access_guarantee: bool = True
    no_credential_access_guarantee: bool = True
    no_command_execution_guarantee: bool = True
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
            "no_provider_invocation_guarantee",
            "no_network_access_guarantee",
            "no_credential_access_guarantee",
            "no_command_execution_guarantee",
            "no_registry_mutation_guarantee",
            "no_memory_mutation_guarantee",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.31.6")
        if _metadata_flag_true(self.metadata, {"execution", "external_control", "authority_grant"}):
            raise ValueError("DominionDecisionRunPreview must not imply execution, external control, or authority grant")

    @property
    def executes_run(self) -> bool:
        return False


@dataclass(frozen=True)
class V0316ReadinessReport:
    report_id: str
    version: str
    decision_set_id: str | None
    summary: str
    ready_for_v0317_triad_skill_ocel_trace_integration: bool
    ready_for_execution: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    ready_for_dominion_runtime: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(V0316_PROHIBITED_UNTIL_LATER_GATE))
    evidence_ref_ids: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0316(self.version)
        _require_non_blank("summary", self.summary)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.6")
        if self.ready_for_external_control is not False:
            raise ValueError("ready_for_external_control must always be False in v0.31.6")
        if self.ready_for_authority_grant is not False:
            raise ValueError("ready_for_authority_grant must always be False in v0.31.6")
        if self.ready_for_dominion_runtime is not False:
            raise ValueError("ready_for_dominion_runtime must always be False in v0.31.6")
        for name in (
            "completed_items",
            "blocked_items",
            "future_track_items",
            "prohibited_until_later_gate",
            "evidence_ref_ids",
            "withdrawal_conditions",
        ):
            _validate_string_list(name, getattr(self, name))
        missing = set(V0316_PROHIBITED_UNTIL_LATER_GATE) - set(self.prohibited_until_later_gate)
        if missing:
            raise ValueError(f"prohibited_until_later_gate missing v0.31.6 prohibitions: {sorted(missing)}")
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "external_control", "authority_grant"}):
            raise ValueError("V0316ReadinessReport must not imply runtime enablement")

    @property
    def runtime_enablement(self) -> bool:
        return False


def build_dominion_target_source_ref(
    source_ref_id: str,
    source_kind: str,
    source_id: str,
    target_id: str | None = None,
    candidate_id: str | None = None,
    signal_id: str | None = None,
    finding_id: str | None = None,
    route_decision_id: str | None = None,
    evidence_ref_ids: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> DominionTargetSourceRef:
    return DominionTargetSourceRef(
        source_ref_id=source_ref_id,
        source_kind=source_kind,
        source_id=source_id,
        target_id=target_id,
        candidate_id=candidate_id,
        signal_id=signal_id,
        finding_id=finding_id,
        route_decision_id=route_decision_id,
        evidence_ref_ids=list(evidence_ref_ids or []),
        metadata=dict(metadata or {}),
    )


def _target_kind_from_signal(signal: DominionControlBoundarySignal | None) -> InternalDominionTargetKind:
    if signal is None:
        return InternalDominionTargetKind.UNKNOWN
    text = " ".join([str(signal.focus_kind), str(signal.title), str(signal.summary), str(signal.boundary_summary or "")]).lower()
    for token, kind in (
        ("provider", InternalDominionTargetKind.EXTERNAL_PROVIDER_TARGET),
        ("gateway", InternalDominionTargetKind.EXTERNAL_GATEWAY_TARGET),
        ("rpa", InternalDominionTargetKind.EXTERNAL_RPA_TARGET),
        ("browser", InternalDominionTargetKind.BROWSER_RUNTIME_TARGET),
        ("command", InternalDominionTargetKind.COMMAND_RUNTIME_TARGET),
        ("credential", InternalDominionTargetKind.CREDENTIAL_BOUND_TARGET),
        ("network", InternalDominionTargetKind.NETWORK_BOUND_TARGET),
        ("memory", InternalDominionTargetKind.MEMORY_BOUNDARY_TARGET),
        ("registry", InternalDominionTargetKind.REGISTRY_BOUNDARY_TARGET),
        ("policy", InternalDominionTargetKind.POLICY_BOUNDARY_TARGET),
        ("delegation", InternalDominionTargetKind.DELEGATION_BOUNDARY_TARGET),
        ("runtime", InternalDominionTargetKind.EXTERNAL_RUNTIME_TARGET),
    ):
        if token in text:
            return kind
    return InternalDominionTargetKind.UNKNOWN


def build_internal_dominion_target(
    dominion_target_id: str,
    title: str,
    summary: str,
    target_kind: InternalDominionTargetKind | str = InternalDominionTargetKind.UNKNOWN,
    status: InternalDominionTargetStatus | str = InternalDominionTargetStatus.TARGET_RECORDED,
    source_external_target_id: str | None = None,
    source_refs: list[DominionTargetSourceRef] | None = None,
    control_surfaces: list[DominionControlSurface | str] | None = None,
    risk_surfaces: list[DominionRiskSurface | str] | None = None,
    control_boundary_ids: list[str] | None = None,
    future_gate_ids: list[str] | None = None,
    evidence_ref_ids: list[str] | None = None,
    max_allowed_level: DominionLevel | int | str | None = DominionLevel.D3_SIMULATE,
    prohibited_runtime_actions: list[str] | None = None,
    assumptions: list[str] | None = None,
    limitations: list[str] | None = None,
    signal: DominionControlBoundarySignal | None = None,
    metadata: dict[str, Any] | None = None,
) -> InternalDominionTarget:
    resolved_kind = _target_kind_from_signal(signal) if target_kind == InternalDominionTargetKind.UNKNOWN and signal is not None else target_kind
    resolved_source_refs = list(source_refs or [])
    resolved_evidence_ref_ids = list(evidence_ref_ids or [])
    if signal is not None:
        resolved_evidence_ref_ids.extend(signal.evidence_ref_ids)
        resolved_source_refs.append(
            build_dominion_target_source_ref(
                f"dominion_target_source_ref:{signal.signal_id}",
                "dominion_control_boundary_signal",
                signal.signal_id,
                target_id=signal.target_id,
                candidate_id=signal.candidate_id,
                signal_id=signal.signal_id,
                evidence_ref_ids=signal.evidence_ref_ids,
            )
        )
    return InternalDominionTarget(
        dominion_target_id=dominion_target_id,
        source_external_target_id=source_external_target_id,
        target_kind=resolved_kind,
        status=status,
        title=title,
        summary=summary,
        source_refs=resolved_source_refs,
        control_surfaces=list(control_surfaces or []),
        risk_surfaces=list(risk_surfaces or []),
        control_boundary_ids=list(control_boundary_ids or []),
        future_gate_ids=list(future_gate_ids or []),
        evidence_ref_ids=resolved_evidence_ref_ids,
        max_allowed_level=max_allowed_level,
        prohibited_runtime_actions=list(prohibited_runtime_actions or V0316_REQUIRED_PROHIBITED_RUNTIME_ACTIONS),
        assumptions=list(assumptions or []),
        limitations=list(limitations or []),
        ready_for_external_control=False,
        ready_for_authority_grant=False,
        ready_for_execution=False,
        metadata=dict(metadata or {}),
    )


def build_dominion_control_boundary(
    boundary_id: str,
    dominion_target_id: str,
    boundary_kind: DominionControlBoundaryKind | str,
    description: str = "Boundary blocks execution, external control, and authority grant until later gates.",
    control_surfaces: list[DominionControlSurface | str] | None = None,
    risk_surfaces: list[DominionRiskSurface | str] | None = None,
    required_evidence_refs: list[str] | None = None,
    required_reviews: list[str] | None = None,
    required_future_gates: list[DominionFutureGateKind | str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> DominionControlBoundary:
    return DominionControlBoundary(
        boundary_id=boundary_id,
        dominion_target_id=dominion_target_id,
        boundary_kind=boundary_kind,
        control_surfaces=list(control_surfaces or []),
        risk_surfaces=list(risk_surfaces or []),
        required_evidence_refs=list(required_evidence_refs or []),
        required_reviews=list(required_reviews or []),
        required_future_gates=list(required_future_gates or []),
        description=description,
        blocks_execution=True,
        blocks_external_control=True,
        blocks_authority_grant=True,
        metadata=dict(metadata or {}),
    )


def build_internal_dominion_decision(
    dominion_decision_id: str,
    dominion_target_id: str,
    decision_type: InternalDominionDecisionType | str,
    reason_kind: DominionDecisionReasonKind | str,
    reason: str,
    granted_level: DominionLevel | int | str | None = None,
    required_boundaries: list[DominionControlBoundaryKind | str] | None = None,
    required_future_gates: list[DominionFutureGateKind | str] | None = None,
    required_reviews: list[str] | None = None,
    evidence_ref_ids: list[str] | None = None,
    blocked_reasons: list[str] | None = None,
    withdrawal_conditions: list[str] | None = None,
    route_decision: DominionRouteDecision | None = None,
    metadata: dict[str, Any] | None = None,
) -> InternalDominionDecision:
    resolved_evidence_refs = list(evidence_ref_ids or [])
    if route_decision is not None:
        resolved_evidence_refs.extend(route_decision.evidence_ref_ids)
    return InternalDominionDecision(
        dominion_decision_id=dominion_decision_id,
        dominion_target_id=dominion_target_id,
        decision_type=decision_type,
        reason_kind=reason_kind,
        reason=reason,
        granted_level=granted_level,
        required_boundaries=list(required_boundaries or []),
        required_future_gates=list(required_future_gates or []),
        required_reviews=list(required_reviews or []),
        evidence_ref_ids=resolved_evidence_refs,
        blocked_reasons=list(blocked_reasons or []),
        withdrawal_conditions=list(withdrawal_conditions or []),
        approved_for_execution=False,
        approved_for_external_control=False,
        authority_granted=False,
        ready_for_execution=False,
        metadata=dict(metadata or {}),
    )


def build_dominion_future_gate_item(
    future_gate_id: str,
    gate_kind: DominionFutureGateKind | str,
    reason: str,
    dominion_target_id: str | None = None,
    blocked_until: str | None = None,
    required_artifacts: list[str] | None = None,
    required_reviews: list[str] | None = None,
    prohibited_until_satisfied: list[str] | None = None,
    evidence_ref_ids: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> DominionFutureGateItem:
    return DominionFutureGateItem(
        future_gate_id=future_gate_id,
        dominion_target_id=dominion_target_id,
        gate_kind=gate_kind,
        reason=reason,
        blocked_until=blocked_until,
        required_artifacts=list(required_artifacts or []),
        required_reviews=list(required_reviews or []),
        prohibited_until_satisfied=list(prohibited_until_satisfied or V0316_PROHIBITED_UNTIL_LATER_GATE),
        evidence_ref_ids=list(evidence_ref_ids or []),
        ready_now=False,
        metadata=dict(metadata or {}),
    )


def build_dominion_no_op_decision(
    no_op_id: str,
    reason: str,
    dominion_target_id: str | None = None,
    safe_alternatives: list[str] | None = None,
    blocked_reasons: list[str] | None = None,
    evidence_ref_ids: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> DominionNoOpDecision:
    return DominionNoOpDecision(
        no_op_id=no_op_id,
        dominion_target_id=dominion_target_id,
        reason=reason,
        safe_alternatives=list(safe_alternatives or []),
        blocked_reasons=list(blocked_reasons or []),
        evidence_ref_ids=list(evidence_ref_ids or []),
        metadata=dict(metadata or {}),
    )


def build_dominion_target_decision_set(
    decision_set_id: str,
    source_dominion_output_id: str | None = None,
    targets: list[InternalDominionTarget] | None = None,
    boundaries: list[DominionControlBoundary] | None = None,
    decisions: list[InternalDominionDecision] | None = None,
    future_gates: list[DominionFutureGateItem] | None = None,
    no_op_decisions: list[DominionNoOpDecision] | None = None,
    evidence_ref_ids: list[str] | None = None,
    ready_for_v0317_ocel_trace_integration: bool = True,
    dominion_output: DominionSkillOutput | None = None,
    metadata: dict[str, Any] | None = None,
) -> DominionTargetDecisionSet:
    resolved_output_id = source_dominion_output_id
    resolved_evidence_refs = list(evidence_ref_ids or [])
    if dominion_output is not None:
        resolved_output_id = dominion_output.dominion_output_id
        resolved_evidence_refs.extend(dominion_output.evidence_ref_ids)
    return DominionTargetDecisionSet(
        decision_set_id=decision_set_id,
        source_dominion_output_id=resolved_output_id,
        targets=list(targets or []),
        boundaries=list(boundaries or []),
        decisions=list(decisions or []),
        future_gates=list(future_gates or []),
        no_op_decisions=list(no_op_decisions or []),
        evidence_ref_ids=resolved_evidence_refs,
        ready_for_v0317_ocel_trace_integration=ready_for_v0317_ocel_trace_integration,
        ready_for_execution=False,
        ready_for_external_control=False,
        ready_for_authority_grant=False,
        metadata=dict(metadata or {}),
    )


def build_dominion_decision_run_preview(
    run_preview_id: str,
    decision_set_id: str | None = None,
    planned_steps: list[str] | None = None,
    expected_artifacts: list[str] | None = None,
    explicitly_not_performed: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> DominionDecisionRunPreview:
    return DominionDecisionRunPreview(
        run_preview_id=run_preview_id,
        decision_set_id=decision_set_id,
        planned_steps=list(planned_steps or ["structure dominion target records", "structure dominion decision records"]),
        expected_artifacts=list(
            expected_artifacts
            or [
                "InternalDominionTarget",
                "DominionControlBoundary",
                "InternalDominionDecision",
                "DominionFutureGateItem",
                "DominionNoOpDecision",
                "DominionTargetDecisionSet",
            ]
        ),
        explicitly_not_performed=list(
            explicitly_not_performed
            or [
                "execution",
                "external_control",
                "authority_grant",
                "provider_invocation",
                "network_access",
                "credential_access",
                "command_execution",
                "registry_mutation",
                "memory_mutation",
            ]
        ),
        metadata=dict(metadata or {}),
    )


def build_v0316_readiness_report(decision_set: DominionTargetDecisionSet | None = None) -> V0316ReadinessReport:
    return V0316ReadinessReport(
        report_id="v0316_readiness_report:dominion_target_decision",
        version=V0316_VERSION,
        decision_set_id=decision_set.decision_set_id if decision_set is not None else None,
        summary="v0.31.6 creates internal dominion target and decision governance records only; no runtime control or authority grant.",
        ready_for_v0317_triad_skill_ocel_trace_integration=True,
        ready_for_execution=False,
        ready_for_external_control=False,
        ready_for_authority_grant=False,
        ready_for_dominion_runtime=False,
        completed_items=[
            "internal dominion target taxonomy",
            "internal dominion decision taxonomy",
            "control boundary and future gate taxonomies",
            "target/decision governance models",
            "decision set and run preview models",
        ],
        blocked_items=[],
        future_track_items=["D4-D9", "external control", "authority grant", "runtime integration"],
        evidence_ref_ids=list(decision_set.evidence_ref_ids if decision_set is not None else []),
        withdrawal_conditions=[
            "internal dominion target is treated as external runtime control",
            "internal dominion decision grants authority",
            "D4-D9 is granted",
            "ready_for_execution, ready_for_external_control, or ready_for_authority_grant becomes true",
        ],
        metadata={"readiness_report_is_runtime_enablement": False},
    )


def target_preserves_no_external_control(target: InternalDominionTarget) -> bool:
    return (
        target.ready_for_external_control is False
        and target.ready_for_authority_grant is False
        and target.ready_for_execution is False
        and target.external_runtime_control is False
        and (target.max_allowed_level is None or normalize_dominion_level(target.max_allowed_level) <= DominionLevel.D3_SIMULATE)
    )


def decision_grants_no_authority(decision: InternalDominionDecision) -> bool:
    return (
        decision.approved_for_execution is False
        and decision.approved_for_external_control is False
        and decision.authority_granted is False
        and decision.ready_for_execution is False
        and decision.grants_authority is False
        and (decision.granted_level is None or normalize_dominion_level(decision.granted_level) <= DominionLevel.D3_SIMULATE)
    )


def decision_set_preserves_no_runtime(decision_set: DominionTargetDecisionSet) -> bool:
    return (
        decision_set.ready_for_execution is False
        and decision_set.ready_for_external_control is False
        and decision_set.ready_for_authority_grant is False
        and decision_set.runtime_registry is False
        and all(target_preserves_no_external_control(target) for target in decision_set.targets)
        and all(decision_grants_no_authority(decision) for decision in decision_set.decisions)
    )


def future_gate_is_not_ready(gate: DominionFutureGateItem) -> bool:
    return gate.ready_now is False and gate.is_readiness is False


def dominion_decision_run_preview_preserves_no_execution(preview: DominionDecisionRunPreview) -> bool:
    return (
        preview.no_execution_guarantee is True
        and preview.no_external_control_guarantee is True
        and preview.no_authority_grant_guarantee is True
        and preview.no_provider_invocation_guarantee is True
        and preview.no_network_access_guarantee is True
        and preview.no_credential_access_guarantee is True
        and preview.no_command_execution_guarantee is True
        and preview.no_registry_mutation_guarantee is True
        and preview.no_memory_mutation_guarantee is True
        and preview.executes_run is False
    )


def v0316_readiness_report_is_not_runtime_ready(report: V0316ReadinessReport) -> bool:
    return (
        report.ready_for_execution is False
        and report.ready_for_external_control is False
        and report.ready_for_authority_grant is False
        and report.ready_for_dominion_runtime is False
        and report.runtime_enablement is False
    )
