from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from chanta_core.internal_triad.boundaries import _require_non_blank, _validate_string_list
from chanta_core.internal_triad.observation_reports import (
    CapabilityClassification,
    CapabilityMapEntry,
    InternalCapabilityMap,
    ObservationReportBundle,
    V0312_REQUIRED_PROHIBITED_RUNTIME_ACTIONS,
    normalize_capability_classification,
)
from chanta_core.internal_triad.skill_kinds import V0310_TRACK


V0313_VERSION = "v0.31.3"
V0313_RELEASE_NAME = "v0.31.3 Digestion Skill Foundation"
V0313_TRACK = V0310_TRACK

V0313_REQUIRED_PROHIBITED_RUNTIME_ACTIONS = [
    *V0312_REQUIRED_PROHIBITED_RUNTIME_ACTIONS,
    "active_internalization",
    "internal_tool_contract_candidate_creation",
    "internal_mission_candidate_creation",
    "internal_policy_candidate_creation",
    "internal_memory_schema_candidate_creation",
    "active_digestion_candidate_creation",
    "registry_mutation",
    "memory_mutation",
]

V0313_PROHIBITED_UNTIL_LATER_GATE = [
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
    "active_internalization",
    "internal_candidate_creation",
    "internal_skill_candidate_creation",
    "internal_tool_contract_candidate_creation",
    "internal_mission_candidate_creation",
    "internal_policy_candidate_creation",
    "internal_memory_schema_candidate_creation",
    "internalization_plan_creation",
    "dominion_target_creation",
    "dominion_decision_creation",
]


class DigestionSkillSourceKind(StrEnum):
    INTERNAL_OBSERVATION_REPORT = "internal_observation_report"
    INTERNAL_CAPABILITY_MAP = "internal_capability_map"
    OBSERVATION_REPORT_BUNDLE = "observation_report_bundle"
    CAPABILITY_MAP_ENTRY = "capability_map_entry"
    OBSERVATION_GAP_REGISTER = "observation_gap_register"
    OBSERVATION_RISK_MAP = "observation_risk_map"
    OBSERVATION_EVIDENCE_TABLE = "observation_evidence_table"
    MANUAL_DIGESTIVE_REVIEW = "manual_digestive_review"
    V0312_READINESS_REPORT = "v0312_readiness_report"
    UNKNOWN = "unknown"


class DigestionFocusKind(StrEnum):
    TOOL_CONTRACT_PATTERN = "tool_contract_pattern"
    SKILL_MANIFEST_PATTERN = "skill_manifest_pattern"
    MISSION_MANIFEST_PATTERN = "mission_manifest_pattern"
    POLICY_RULE_PATTERN = "policy_rule_pattern"
    MEMORY_SCHEMA_PATTERN = "memory_schema_pattern"
    PROMPT_PATTERN = "prompt_pattern"
    PROFILE_PATTERN = "profile_pattern"
    TRACE_EVENT_PATTERN = "trace_event_pattern"
    RESULT_ENVELOPE_PATTERN = "result_envelope_pattern"
    APPROVAL_BOUNDARY_PATTERN = "approval_boundary_pattern"
    OCEL_TRACE_PATTERN = "ocel_trace_pattern"
    GATEWAY_MANIFEST_PATTERN = "gateway_manifest_pattern"
    PROVIDER_ADAPTER_PATTERN = "provider_adapter_pattern"
    DELEGATION_PACKET_PATTERN = "delegation_packet_pattern"
    UNSAFE_RUNTIME_SURFACE = "unsafe_runtime_surface"
    UNKNOWN = "unknown"


class DigestionSignalKind(StrEnum):
    PATTERN_DETECTED = "pattern_detected"
    SCHEMA_EXTRACTABLE = "schema_extractable"
    INTERNALIZATION_POSSIBLE = "internalization_possible"
    REQUIRES_INTERNAL_DESIGN = "requires_internal_design"
    REQUIRES_REVIEW = "requires_review"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    UNSAFE_TO_DIGEST = "unsafe_to_digest"
    INCOMPATIBLE_WITH_OCEL_SPINE = "incompatible_with_ocel_spine"
    DOMINION_REQUIRED = "dominion_required"
    FUTURE_TRACK_REQUIRED = "future_track_required"
    BLOCKED = "blocked"
    NO_OP_RECOMMENDED = "no_op_recommended"
    UNKNOWN = "unknown"


class DigestionRoute(StrEnum):
    INTERNALIZATION_CANDIDATE_SIGNAL = "internalization_candidate_signal"
    DEFER = "defer"
    REJECT = "reject"
    DOMINION_REQUIRED_SIGNAL = "dominion_required_signal"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class DigestionFeasibilityPosture(StrEnum):
    UNKNOWN = "unknown"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class DigestionEvidencePosture(StrEnum):
    UNKNOWN = "unknown"
    NONE = "none"
    WEAK = "weak"
    PARTIAL = "partial"
    SUFFICIENT_FOR_ROUTE_SIGNAL = "sufficient_for_route_signal"
    SUFFICIENT_FOR_V0314_REVIEW = "sufficient_for_v0314_review"
    CONFLICTING = "conflicting"
    BLOCKED = "blocked"


class DigestionBlockerKind(StrEnum):
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    MISSING_CAPABILITY_MAP_ENTRY = "missing_capability_map_entry"
    MISSING_OBSERVATION_REPORT = "missing_observation_report"
    MISSING_EVIDENCE_TABLE = "missing_evidence_table"
    UNSAFE_NETWORK_SURFACE = "unsafe_network_surface"
    UNSAFE_CREDENTIAL_SURFACE = "unsafe_credential_surface"
    UNSAFE_COMMAND_SURFACE = "unsafe_command_surface"
    UNSAFE_PROVIDER_SURFACE = "unsafe_provider_surface"
    UNSAFE_BROWSER_SURFACE = "unsafe_browser_surface"
    UNSAFE_RPA_SURFACE = "unsafe_rpa_surface"
    UNSAFE_GATEWAY_SURFACE = "unsafe_gateway_surface"
    UNSAFE_DELEGATION_SURFACE = "unsafe_delegation_surface"
    RAW_OUTPUT_PERSISTENCE_RISK = "raw_output_persistence_risk"
    MEMORY_CONTAMINATION_RISK = "memory_contamination_risk"
    INCOMPATIBLE_WITH_OCEL_SPINE = "incompatible_with_ocel_spine"
    REQUIRES_DOMINION = "requires_dominion"
    REQUIRES_FUTURE_GATE = "requires_future_gate"
    UNKNOWN = "unknown"


def _metadata_flag_true(metadata: dict[str, Any], names: set[str]) -> bool:
    return isinstance(metadata, dict) and any(metadata.get(name) is True for name in names)


def _validate_object_list(name: str, values: list[Any], expected_type: type) -> None:
    if not isinstance(values, list) or not all(isinstance(item, expected_type) for item in values):
        raise TypeError(f"{name} must be list[{expected_type.__name__}]")


def _validate_version_includes_v0313(version: str) -> None:
    _require_non_blank("version", version)
    if V0313_VERSION not in version:
        raise ValueError("version must include v0.31.3")


def _validate_prohibited_actions(actions: list[str]) -> None:
    _validate_string_list("prohibited_runtime_actions", actions)
    missing = set(V0313_REQUIRED_PROHIBITED_RUNTIME_ACTIONS) - set(actions)
    if missing:
        raise ValueError(f"prohibited_runtime_actions missing v0.31.3 prohibitions: {sorted(missing)}")


def normalize_digestion_source_kind(value: DigestionSkillSourceKind | str) -> DigestionSkillSourceKind:
    if isinstance(value, DigestionSkillSourceKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("digestion source kind must not be blank")
        return DigestionSkillSourceKind(stripped)
    raise TypeError(f"unsupported digestion source kind: {value!r}")


def normalize_digestion_focus_kind(value: DigestionFocusKind | str) -> DigestionFocusKind:
    if isinstance(value, DigestionFocusKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("digestion focus kind must not be blank")
        return DigestionFocusKind(stripped)
    raise TypeError(f"unsupported digestion focus kind: {value!r}")


def normalize_digestion_signal_kind(value: DigestionSignalKind | str) -> DigestionSignalKind:
    if isinstance(value, DigestionSignalKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("digestion signal kind must not be blank")
        return DigestionSignalKind(stripped)
    raise TypeError(f"unsupported digestion signal kind: {value!r}")


def normalize_digestion_route(value: DigestionRoute | str) -> DigestionRoute:
    if isinstance(value, DigestionRoute):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("digestion route must not be blank")
        return DigestionRoute(stripped)
    raise TypeError(f"unsupported digestion route: {value!r}")


def normalize_digestion_feasibility_posture(value: DigestionFeasibilityPosture | str) -> DigestionFeasibilityPosture:
    if isinstance(value, DigestionFeasibilityPosture):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("digestion feasibility posture must not be blank")
        return DigestionFeasibilityPosture(stripped)
    raise TypeError(f"unsupported digestion feasibility posture: {value!r}")


def normalize_digestion_evidence_posture(value: DigestionEvidencePosture | str) -> DigestionEvidencePosture:
    if isinstance(value, DigestionEvidencePosture):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("digestion evidence posture must not be blank")
        return DigestionEvidencePosture(stripped)
    raise TypeError(f"unsupported digestion evidence posture: {value!r}")


def normalize_digestion_blocker_kind(value: DigestionBlockerKind | str) -> DigestionBlockerKind:
    if isinstance(value, DigestionBlockerKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("digestion blocker kind must not be blank")
        return DigestionBlockerKind(stripped)
    raise TypeError(f"unsupported digestion blocker kind: {value!r}")


def digestion_source_kind_fetches(_: DigestionSkillSourceKind | str) -> bool:
    normalize_digestion_source_kind(_)
    return False


def digestion_focus_kind_creates_internal_artifact(_: DigestionFocusKind | str) -> bool:
    normalize_digestion_focus_kind(_)
    return False


@dataclass(frozen=True)
class DigestionSourceRef:
    source_ref_id: str
    source_kind: DigestionSkillSourceKind | str
    source_id: str
    target_id: str | None = None
    capability_entry_id: str | None = None
    evidence_ref_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        normalize_digestion_source_kind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _validate_string_list("evidence_ref_ids", self.evidence_ref_ids)
        if _metadata_flag_true(self.metadata, {"source_fetch", "source_ref_fetch", "url_fetch"}):
            raise ValueError("DigestionSourceRef must not imply source fetch")

    @property
    def fetches_source(self) -> bool:
        return False


@dataclass(frozen=True)
class DigestionSkillInput:
    digestion_input_id: str
    triad_input_id: str | None
    source_refs: list[DigestionSourceRef]
    observation_report_refs: list[str]
    capability_map_refs: list[str]
    capability_entry_refs: list[str]
    requested_focus: list[DigestionFocusKind | str]
    task_summary: str
    source_version: str
    evidence_refs: list[str]
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(V0313_REQUIRED_PROHIBITED_RUNTIME_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("digestion_input_id", self.digestion_input_id)
        _validate_object_list("source_refs", self.source_refs, DigestionSourceRef)
        for name in ("observation_report_refs", "capability_map_refs", "capability_entry_refs", "evidence_refs"):
            _validate_string_list(name, getattr(self, name))
        if not isinstance(self.requested_focus, list):
            raise TypeError("requested_focus must be list[DigestionFocusKind | str]")
        for focus in self.requested_focus:
            normalize_digestion_focus_kind(focus)
        _require_non_blank("task_summary", self.task_summary)
        _require_non_blank("source_version", self.source_version)
        _validate_prohibited_actions(self.prohibited_runtime_actions)
        if _metadata_flag_true(
            self.metadata,
            {"execution_request", "active_internalization", "registry_mutation", "memory_mutation", "read_only_tool_execution"},
        ):
            raise ValueError("DigestionSkillInput must not imply execution, internalization, registry mutation, memory mutation, or tool execution")

    @property
    def is_execution_request(self) -> bool:
        return False


@dataclass(frozen=True)
class DigestiblePatternSignal:
    signal_id: str
    source_ref_id: str | None
    target_id: str | None
    capability_entry_id: str | None
    focus_kind: DigestionFocusKind | str
    signal_kind: DigestionSignalKind | str
    proposed_route: DigestionRoute | str
    title: str
    summary: str
    extracted_pattern_summary: str | None = None
    evidence_ref_ids: list[str] = field(default_factory=list)
    blocker_ids: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    feasibility_posture: DigestionFeasibilityPosture | str = DigestionFeasibilityPosture.UNKNOWN
    evidence_posture: DigestionEvidencePosture | str = DigestionEvidencePosture.UNKNOWN
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("signal_id", self.signal_id)
        normalize_digestion_focus_kind(self.focus_kind)
        normalize_digestion_signal_kind(self.signal_kind)
        route = normalize_digestion_route(self.proposed_route)
        _require_non_blank("title", self.title)
        _require_non_blank("summary", self.summary)
        for name in ("evidence_ref_ids", "blocker_ids", "assumptions", "limitations"):
            _validate_string_list(name, getattr(self, name))
        normalize_digestion_feasibility_posture(self.feasibility_posture)
        normalize_digestion_evidence_posture(self.evidence_posture)
        if route is DigestionRoute.BLOCKED and not (self.blocker_ids or self.limitations):
            raise ValueError("blocked route requires blocker_ids or limitations")
        if _metadata_flag_true(
            self.metadata,
            {
                "internal_skill_candidate_creation",
                "internalization_plan_creation",
                "dominion_target_creation",
                "internal_artifact_creation",
            },
        ):
            raise ValueError("DigestiblePatternSignal is not an internal artifact or dominion target")

    @property
    def creates_internal_skill_candidate(self) -> bool:
        return False

    @property
    def creates_internalization_plan(self) -> bool:
        return False

    @property
    def creates_dominion_target(self) -> bool:
        return False

    @property
    def is_internal_artifact(self) -> bool:
        return False


@dataclass(frozen=True)
class DigestionFinding:
    finding_id: str
    digestion_input_id: str
    signal_ids: list[str]
    route: DigestionRoute | str
    summary: str
    feasibility_posture: DigestionFeasibilityPosture | str
    evidence_posture: DigestionEvidencePosture | str
    evidence_ref_ids: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    recommended_next_stage: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("digestion_input_id", self.digestion_input_id)
        _validate_string_list("signal_ids", self.signal_ids)
        normalize_digestion_route(self.route)
        _require_non_blank("summary", self.summary)
        normalize_digestion_feasibility_posture(self.feasibility_posture)
        normalize_digestion_evidence_posture(self.evidence_posture)
        _validate_string_list("evidence_ref_ids", self.evidence_ref_ids)
        _validate_string_list("blocked_reasons", self.blocked_reasons)
        if _metadata_flag_true(self.metadata, {"v0314_artifact_creation", "internalization_plan_creation", "dominion_target_creation"}):
            raise ValueError("DigestionFinding must not create later-stage artifacts or dominion targets")

    @property
    def creates_v0314_artifact(self) -> bool:
        return False

    @property
    def creates_dominion_target(self) -> bool:
        return False


@dataclass(frozen=True)
class DigestionBlocker:
    blocker_id: str
    blocker_kind: DigestionBlockerKind | str
    source_ref_id: str | None
    capability_entry_id: str | None
    description: str
    blocks_v0314: bool
    routes_to_dominion: bool
    routes_to_future_gate: bool
    evidence_ref_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("blocker_id", self.blocker_id)
        normalize_digestion_blocker_kind(self.blocker_kind)
        _require_non_blank("description", self.description)
        for name in ("blocks_v0314", "routes_to_dominion", "routes_to_future_gate"):
            if not isinstance(getattr(self, name), bool):
                raise TypeError(f"{name} must be bool")
        _validate_string_list("evidence_ref_ids", self.evidence_ref_ids)
        if _metadata_flag_true(self.metadata, {"remediation_execution", "automatic_remediation"}):
            raise ValueError("DigestionBlocker must not execute remediation")

    @property
    def executes_remediation(self) -> bool:
        return False


@dataclass(frozen=True)
class DigestionRouteDecision:
    route_decision_id: str
    digestion_input_id: str
    route: DigestionRoute | str
    signal_ids: list[str]
    blocker_ids: list[str]
    reason: str
    evidence_ref_ids: list[str] = field(default_factory=list)
    ready_for_v0314_internalization_plan: bool = False
    ready_for_v0315_dominion_skill_foundation: bool = False
    ready_for_execution: bool = False
    ready_for_skill_activation: bool = False
    ready_for_internalization: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("route_decision_id", self.route_decision_id)
        _require_non_blank("digestion_input_id", self.digestion_input_id)
        route = normalize_digestion_route(self.route)
        for name in ("signal_ids", "blocker_ids", "evidence_ref_ids"):
            _validate_string_list(name, getattr(self, name))
        _require_non_blank("reason", self.reason)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.3")
        if self.ready_for_skill_activation is not False:
            raise ValueError("ready_for_skill_activation must always be False in v0.31.3")
        if self.ready_for_internalization is not False:
            raise ValueError("ready_for_internalization must always be False in v0.31.3")
        if self.ready_for_v0314_internalization_plan and (route is not DigestionRoute.INTERNALIZATION_CANDIDATE_SIGNAL or self.blocker_ids):
            raise ValueError("v0.31.4 readiness requires internalization_candidate_signal route with no blocking blockers")
        conservative_routing = _metadata_flag_true(self.metadata, {"conservative_dominion_routing"})
        if self.ready_for_v0315_dominion_skill_foundation and not (route is DigestionRoute.DOMINION_REQUIRED_SIGNAL or conservative_routing):
            raise ValueError("v0.31.5 readiness requires dominion_required_signal route or conservative routing")
        if _metadata_flag_true(self.metadata, {"implementation", "active_internalization"}):
            raise ValueError("DigestionRouteDecision is not implementation")

    @property
    def is_implementation(self) -> bool:
        return False


@dataclass(frozen=True)
class DigestionSkillOutput:
    digestion_output_id: str
    digestion_input_id: str
    skill_contract_id: str | None
    status: str
    pattern_signals: list[DigestiblePatternSignal]
    findings: list[DigestionFinding]
    blockers: list[DigestionBlocker]
    route_decisions: list[DigestionRouteDecision]
    internalization_signal_ids: list[str]
    deferred_signal_ids: list[str]
    rejected_signal_ids: list[str]
    dominion_required_signal_ids: list[str]
    blocked_signal_ids: list[str]
    future_track_signal_ids: list[str]
    evidence_ref_ids: list[str]
    ready_for_v0314_internalization_plan: bool
    ready_for_v0315_dominion_skill_foundation: bool
    ready_for_execution: bool = False
    ready_for_skill_activation: bool = False
    ready_for_internalization: bool = False
    ready_for_registry_mutation: bool = False
    blocked_reasons: list[str] = field(default_factory=list)
    no_op_reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("digestion_output_id", self.digestion_output_id)
        _require_non_blank("digestion_input_id", self.digestion_input_id)
        _require_non_blank("status", self.status)
        _validate_object_list("pattern_signals", self.pattern_signals, DigestiblePatternSignal)
        _validate_object_list("findings", self.findings, DigestionFinding)
        _validate_object_list("blockers", self.blockers, DigestionBlocker)
        _validate_object_list("route_decisions", self.route_decisions, DigestionRouteDecision)
        for name in (
            "internalization_signal_ids",
            "deferred_signal_ids",
            "rejected_signal_ids",
            "dominion_required_signal_ids",
            "blocked_signal_ids",
            "future_track_signal_ids",
            "evidence_ref_ids",
            "blocked_reasons",
        ):
            _validate_string_list(name, getattr(self, name))
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.3")
        if self.ready_for_skill_activation is not False:
            raise ValueError("ready_for_skill_activation must always be False in v0.31.3")
        if self.ready_for_internalization is not False:
            raise ValueError("ready_for_internalization must always be False in v0.31.3")
        if self.ready_for_registry_mutation is not False:
            raise ValueError("ready_for_registry_mutation must always be False in v0.31.3")
        if _metadata_flag_true(
            self.metadata,
            {
                "internal_skill_candidate_creation",
                "internalization_plan_creation",
                "dominion_target_creation",
                "active_artifact_registration",
                "registry_mutation",
            },
        ):
            raise ValueError("DigestionSkillOutput must not create internalization, dominion, registry, or active artifact state")

    @property
    def creates_internal_skill_candidate(self) -> bool:
        return False

    @property
    def creates_internalization_plan(self) -> bool:
        return False

    @property
    def creates_dominion_target(self) -> bool:
        return False

    @property
    def active_artifact_registration(self) -> bool:
        return False


@dataclass(frozen=True)
class DigestionSkillNoOpDecision:
    no_op_id: str
    digestion_input_id: str
    reason: str
    blocked_reasons: list[str] = field(default_factory=list)
    safe_alternatives: list[str] = field(default_factory=list)
    evidence_ref_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("no_op_id", self.no_op_id)
        _require_non_blank("digestion_input_id", self.digestion_input_id)
        _require_non_blank("reason", self.reason)
        for name in ("blocked_reasons", "safe_alternatives", "evidence_ref_ids"):
            _validate_string_list(name, getattr(self, name))

    @property
    def is_failure(self) -> bool:
        return False

    @property
    def executes_anything(self) -> bool:
        return False


@dataclass(frozen=True)
class DigestionSkillRunPreview:
    run_preview_id: str
    digestion_input_id: str | None
    planned_steps: list[str]
    expected_artifacts: list[str]
    explicitly_not_performed: list[str]
    no_execution_guarantee: bool = True
    no_external_scan_guarantee: bool = True
    no_tool_execution_guarantee: bool = True
    no_internalization_guarantee: bool = True
    no_candidate_creation_guarantee: bool = True
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
            "no_internalization_guarantee",
            "no_candidate_creation_guarantee",
            "no_registry_mutation_guarantee",
            "no_memory_mutation_guarantee",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.31.3")
        if _metadata_flag_true(self.metadata, {"executes_run", "active_internalization", "tool_execution"}):
            raise ValueError("DigestionSkillRunPreview must not imply execution")

    @property
    def executes_run(self) -> bool:
        return False


@dataclass(frozen=True)
class DigestionSkillFoundationReport:
    foundation_report_id: str
    version: str
    digestion_contract_ref: str | None
    supported_source_kinds: list[DigestionSkillSourceKind | str]
    supported_focus_kinds: list[DigestionFocusKind | str]
    supported_routes: list[DigestionRoute | str]
    supported_output_artifact_kinds: list[str]
    prohibited_runtime_actions: list[str]
    ready_for_v0314_digestion_candidate_internalization_plan: bool
    ready_for_v0315_dominion_skill_foundation: bool
    ready_for_execution: bool = False
    ready_for_skill_activation: bool = False
    ready_for_internalization: bool = False
    summary: str = ""
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("foundation_report_id", self.foundation_report_id)
        _validate_version_includes_v0313(self.version)
        for source_kind in self.supported_source_kinds:
            normalize_digestion_source_kind(source_kind)
        for focus_kind in self.supported_focus_kinds:
            normalize_digestion_focus_kind(focus_kind)
        for route in self.supported_routes:
            normalize_digestion_route(route)
        _validate_string_list("supported_output_artifact_kinds", self.supported_output_artifact_kinds)
        _validate_prohibited_actions(self.prohibited_runtime_actions)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.3")
        if self.ready_for_skill_activation is not False:
            raise ValueError("ready_for_skill_activation must always be False in v0.31.3")
        if self.ready_for_internalization is not False:
            raise ValueError("ready_for_internalization must always be False in v0.31.3")
        _require_non_blank("summary", self.summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("withdrawal_conditions", self.withdrawal_conditions)

    @property
    def runtime_enablement(self) -> bool:
        return False


@dataclass(frozen=True)
class V0313ReadinessReport:
    report_id: str
    version: str
    digestion_foundation_report_id: str
    summary: str
    ready_for_v0314_digestion_candidate_internalization_plan: bool
    ready_for_v0315_dominion_skill_foundation: bool
    ready_for_execution: bool = False
    ready_for_skill_activation: bool = False
    ready_for_internalization: bool = False
    ready_for_registry_mutation: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(V0313_PROHIBITED_UNTIL_LATER_GATE))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0313(self.version)
        _require_non_blank("digestion_foundation_report_id", self.digestion_foundation_report_id)
        _require_non_blank("summary", self.summary)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.3")
        if self.ready_for_skill_activation is not False:
            raise ValueError("ready_for_skill_activation must always be False in v0.31.3")
        if self.ready_for_internalization is not False:
            raise ValueError("ready_for_internalization must always be False in v0.31.3")
        if self.ready_for_registry_mutation is not False:
            raise ValueError("ready_for_registry_mutation must always be False in v0.31.3")
        for name in (
            "completed_items",
            "blocked_items",
            "future_track_items",
            "prohibited_until_later_gate",
            "evidence_refs",
            "withdrawal_conditions",
        ):
            _validate_string_list(name, getattr(self, name))
        missing = set(V0313_PROHIBITED_UNTIL_LATER_GATE) - set(self.prohibited_until_later_gate)
        if missing:
            raise ValueError(f"prohibited_until_later_gate missing required items: {sorted(missing)}")
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "execution_readiness", "active_internalization"}):
            raise ValueError("V0313ReadinessReport must not imply runtime readiness")

    @property
    def runtime_enablement(self) -> bool:
        return False


def build_digestion_source_ref(
    source_ref_id: str,
    source_kind: DigestionSkillSourceKind | str,
    source_id: str,
    target_id: str | None = None,
    capability_entry_id: str | None = None,
    evidence_ref_ids: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> DigestionSourceRef:
    return DigestionSourceRef(
        source_ref_id=source_ref_id,
        source_kind=source_kind,
        source_id=source_id,
        target_id=target_id,
        capability_entry_id=capability_entry_id,
        evidence_ref_ids=list(evidence_ref_ids or []),
        metadata=dict(metadata or {}),
    )


def build_digestion_skill_input(
    digestion_input_id: str,
    task_summary: str,
    source_version: str,
    source_refs: list[DigestionSourceRef] | None = None,
    observation_report_refs: list[str] | None = None,
    capability_map_refs: list[str] | None = None,
    capability_entry_refs: list[str] | None = None,
    requested_focus: list[DigestionFocusKind | str] | None = None,
    evidence_refs: list[str] | None = None,
    triad_input_id: str | None = None,
    capability_map: InternalCapabilityMap | None = None,
    bundle: ObservationReportBundle | None = None,
    metadata: dict[str, Any] | None = None,
) -> DigestionSkillInput:
    resolved_source_refs = list(source_refs or [])
    resolved_report_refs = list(observation_report_refs or [])
    resolved_map_refs = list(capability_map_refs or [])
    resolved_entry_refs = list(capability_entry_refs or [])
    resolved_evidence_refs = list(evidence_refs or [])
    if capability_map is not None:
        resolved_map_refs.append(capability_map.capability_map_id)
        resolved_report_refs.append(capability_map.observation_report_id)
        resolved_entry_refs.extend(entry.entry_id for entry in capability_map.entries)
        resolved_source_refs.append(
            build_digestion_source_ref(
                f"digestion_source_ref:{capability_map.capability_map_id}",
                DigestionSkillSourceKind.INTERNAL_CAPABILITY_MAP,
                capability_map.capability_map_id,
                target_id=capability_map.target_id,
                evidence_ref_ids=capability_map.evidence_ref_ids,
            )
        )
        resolved_evidence_refs.extend(capability_map.evidence_ref_ids)
    if bundle is not None:
        resolved_report_refs.append(bundle.observation_report.report_id)
        resolved_map_refs.append(bundle.capability_map.capability_map_id)
        resolved_entry_refs.extend(entry.entry_id for entry in bundle.capability_map.entries)
        resolved_source_refs.append(
            build_digestion_source_ref(
                f"digestion_source_ref:{bundle.bundle_id}",
                DigestionSkillSourceKind.OBSERVATION_REPORT_BUNDLE,
                bundle.bundle_id,
                evidence_ref_ids=bundle.evidence_refs,
            )
        )
        resolved_evidence_refs.extend(bundle.evidence_refs)
    return DigestionSkillInput(
        digestion_input_id=digestion_input_id,
        triad_input_id=triad_input_id,
        source_refs=resolved_source_refs,
        observation_report_refs=resolved_report_refs,
        capability_map_refs=resolved_map_refs,
        capability_entry_refs=resolved_entry_refs,
        requested_focus=list(requested_focus or []),
        task_summary=task_summary,
        source_version=source_version,
        evidence_refs=resolved_evidence_refs,
        prohibited_runtime_actions=list(V0313_REQUIRED_PROHIBITED_RUNTIME_ACTIONS),
        metadata=dict(metadata or {}),
    )


def classify_digestion_focus_from_capability_entry(entry: CapabilityMapEntry) -> DigestionFocusKind:
    if not isinstance(entry, CapabilityMapEntry):
        raise TypeError("entry must be CapabilityMapEntry")
    text = " ".join(
        [
            entry.capability_name,
            entry.capability_kind or "",
            " ".join(entry.boundary_surfaces),
            " ".join(entry.effect_surfaces),
        ]
    ).lower()
    unsafe_terms = {"network", "credential", "command", "provider", "browser", "rpa", "gateway", "delegation", "runtime"}
    if any(term in text for term in unsafe_terms) or normalize_capability_classification(entry.classification) is CapabilityClassification.BLOCKED:
        return DigestionFocusKind.UNSAFE_RUNTIME_SURFACE
    for token, focus in (
        ("tool", DigestionFocusKind.TOOL_CONTRACT_PATTERN),
        ("skill", DigestionFocusKind.SKILL_MANIFEST_PATTERN),
        ("mission", DigestionFocusKind.MISSION_MANIFEST_PATTERN),
        ("policy", DigestionFocusKind.POLICY_RULE_PATTERN),
        ("memory", DigestionFocusKind.MEMORY_SCHEMA_PATTERN),
        ("prompt", DigestionFocusKind.PROMPT_PATTERN),
        ("profile", DigestionFocusKind.PROFILE_PATTERN),
        ("trace", DigestionFocusKind.TRACE_EVENT_PATTERN),
        ("result", DigestionFocusKind.RESULT_ENVELOPE_PATTERN),
        ("approval", DigestionFocusKind.APPROVAL_BOUNDARY_PATTERN),
        ("ocel", DigestionFocusKind.OCEL_TRACE_PATTERN),
    ):
        if token in text:
            return focus
    return DigestionFocusKind.UNKNOWN


def infer_digestion_route_from_capability_classification(
    entry_or_classification: CapabilityMapEntry | CapabilityClassification | str,
) -> DigestionRoute:
    classification = (
        normalize_capability_classification(entry_or_classification.classification)
        if isinstance(entry_or_classification, CapabilityMapEntry)
        else normalize_capability_classification(entry_or_classification)
    )
    if classification is CapabilityClassification.DIGESTION_SIGNAL:
        return DigestionRoute.INTERNALIZATION_CANDIDATE_SIGNAL
    if classification is CapabilityClassification.DOMINION_SIGNAL:
        return DigestionRoute.DOMINION_REQUIRED_SIGNAL
    if classification is CapabilityClassification.BLOCKED:
        return DigestionRoute.BLOCKED
    if classification is CapabilityClassification.DEFERRED:
        return DigestionRoute.DEFER
    if classification is CapabilityClassification.FUTURE_TRACK:
        return DigestionRoute.FUTURE_TRACK
    if classification is CapabilityClassification.NO_OP:
        return DigestionRoute.NO_OP
    if classification in {CapabilityClassification.DESCRIPTIVE_ONLY, CapabilityClassification.SAFE_DESCRIPTIVE}:
        return DigestionRoute.DEFER
    return DigestionRoute.UNKNOWN


def build_digestible_pattern_signal(
    signal_id: str,
    focus_kind: DigestionFocusKind | str,
    signal_kind: DigestionSignalKind | str,
    proposed_route: DigestionRoute | str,
    title: str,
    summary: str,
    source_ref_id: str | None = None,
    target_id: str | None = None,
    capability_entry_id: str | None = None,
    extracted_pattern_summary: str | None = None,
    evidence_ref_ids: list[str] | None = None,
    blocker_ids: list[str] | None = None,
    assumptions: list[str] | None = None,
    limitations: list[str] | None = None,
    feasibility_posture: DigestionFeasibilityPosture | str = DigestionFeasibilityPosture.UNKNOWN,
    evidence_posture: DigestionEvidencePosture | str = DigestionEvidencePosture.UNKNOWN,
    metadata: dict[str, Any] | None = None,
) -> DigestiblePatternSignal:
    return DigestiblePatternSignal(
        signal_id=signal_id,
        source_ref_id=source_ref_id,
        target_id=target_id,
        capability_entry_id=capability_entry_id,
        focus_kind=focus_kind,
        signal_kind=signal_kind,
        proposed_route=proposed_route,
        title=title,
        summary=summary,
        extracted_pattern_summary=extracted_pattern_summary,
        evidence_ref_ids=list(evidence_ref_ids or []),
        blocker_ids=list(blocker_ids or []),
        assumptions=list(assumptions or []),
        limitations=list(limitations or []),
        feasibility_posture=feasibility_posture,
        evidence_posture=evidence_posture,
        metadata=dict(metadata or {}),
    )


def build_digestion_finding(
    finding_id: str,
    digestion_input_id: str,
    route: DigestionRoute | str,
    summary: str,
    signal_ids: list[str] | None = None,
    feasibility_posture: DigestionFeasibilityPosture | str = DigestionFeasibilityPosture.UNKNOWN,
    evidence_posture: DigestionEvidencePosture | str = DigestionEvidencePosture.UNKNOWN,
    evidence_ref_ids: list[str] | None = None,
    blocked_reasons: list[str] | None = None,
    recommended_next_stage: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> DigestionFinding:
    return DigestionFinding(
        finding_id=finding_id,
        digestion_input_id=digestion_input_id,
        signal_ids=list(signal_ids or []),
        route=route,
        summary=summary,
        feasibility_posture=feasibility_posture,
        evidence_posture=evidence_posture,
        evidence_ref_ids=list(evidence_ref_ids or []),
        blocked_reasons=list(blocked_reasons or []),
        recommended_next_stage=recommended_next_stage,
        metadata=dict(metadata or {}),
    )


def build_digestion_blocker(
    blocker_id: str,
    blocker_kind: DigestionBlockerKind | str,
    description: str,
    source_ref_id: str | None = None,
    capability_entry_id: str | None = None,
    blocks_v0314: bool = False,
    routes_to_dominion: bool = False,
    routes_to_future_gate: bool = False,
    evidence_ref_ids: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> DigestionBlocker:
    return DigestionBlocker(
        blocker_id=blocker_id,
        blocker_kind=blocker_kind,
        source_ref_id=source_ref_id,
        capability_entry_id=capability_entry_id,
        description=description,
        blocks_v0314=blocks_v0314,
        routes_to_dominion=routes_to_dominion,
        routes_to_future_gate=routes_to_future_gate,
        evidence_ref_ids=list(evidence_ref_ids or []),
        metadata=dict(metadata or {}),
    )


def build_digestion_route_decision(
    route_decision_id: str,
    digestion_input_id: str,
    route: DigestionRoute | str,
    reason: str,
    signal_ids: list[str] | None = None,
    blocker_ids: list[str] | None = None,
    evidence_ref_ids: list[str] | None = None,
    ready_for_v0314_internalization_plan: bool = False,
    ready_for_v0315_dominion_skill_foundation: bool = False,
    metadata: dict[str, Any] | None = None,
) -> DigestionRouteDecision:
    return DigestionRouteDecision(
        route_decision_id=route_decision_id,
        digestion_input_id=digestion_input_id,
        route=route,
        signal_ids=list(signal_ids or []),
        blocker_ids=list(blocker_ids or []),
        reason=reason,
        evidence_ref_ids=list(evidence_ref_ids or []),
        ready_for_v0314_internalization_plan=ready_for_v0314_internalization_plan,
        ready_for_v0315_dominion_skill_foundation=ready_for_v0315_dominion_skill_foundation,
        ready_for_execution=False,
        ready_for_skill_activation=False,
        ready_for_internalization=False,
        metadata=dict(metadata or {}),
    )


def build_digestion_skill_output(
    digestion_output_id: str,
    digestion_input_id: str,
    status: str,
    pattern_signals: list[DigestiblePatternSignal] | None = None,
    findings: list[DigestionFinding] | None = None,
    blockers: list[DigestionBlocker] | None = None,
    route_decisions: list[DigestionRouteDecision] | None = None,
    internalization_signal_ids: list[str] | None = None,
    deferred_signal_ids: list[str] | None = None,
    rejected_signal_ids: list[str] | None = None,
    dominion_required_signal_ids: list[str] | None = None,
    blocked_signal_ids: list[str] | None = None,
    future_track_signal_ids: list[str] | None = None,
    evidence_ref_ids: list[str] | None = None,
    ready_for_v0314_internalization_plan: bool = False,
    ready_for_v0315_dominion_skill_foundation: bool = False,
    skill_contract_id: str | None = None,
    blocked_reasons: list[str] | None = None,
    no_op_reason: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> DigestionSkillOutput:
    return DigestionSkillOutput(
        digestion_output_id=digestion_output_id,
        digestion_input_id=digestion_input_id,
        skill_contract_id=skill_contract_id,
        status=status,
        pattern_signals=list(pattern_signals or []),
        findings=list(findings or []),
        blockers=list(blockers or []),
        route_decisions=list(route_decisions or []),
        internalization_signal_ids=list(internalization_signal_ids or []),
        deferred_signal_ids=list(deferred_signal_ids or []),
        rejected_signal_ids=list(rejected_signal_ids or []),
        dominion_required_signal_ids=list(dominion_required_signal_ids or []),
        blocked_signal_ids=list(blocked_signal_ids or []),
        future_track_signal_ids=list(future_track_signal_ids or []),
        evidence_ref_ids=list(evidence_ref_ids or []),
        ready_for_v0314_internalization_plan=ready_for_v0314_internalization_plan,
        ready_for_v0315_dominion_skill_foundation=ready_for_v0315_dominion_skill_foundation,
        ready_for_execution=False,
        ready_for_skill_activation=False,
        ready_for_internalization=False,
        ready_for_registry_mutation=False,
        blocked_reasons=list(blocked_reasons or []),
        no_op_reason=no_op_reason,
        metadata=dict(metadata or {}),
    )


def build_digestion_no_op_decision(
    no_op_id: str,
    digestion_input_id: str,
    reason: str,
    blocked_reasons: list[str] | None = None,
    safe_alternatives: list[str] | None = None,
    evidence_ref_ids: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> DigestionSkillNoOpDecision:
    return DigestionSkillNoOpDecision(
        no_op_id=no_op_id,
        digestion_input_id=digestion_input_id,
        reason=reason,
        blocked_reasons=list(blocked_reasons or []),
        safe_alternatives=list(safe_alternatives or []),
        evidence_ref_ids=list(evidence_ref_ids or []),
        metadata=dict(metadata or {}),
    )


def build_digestion_run_preview(
    run_preview_id: str,
    digestion_input_id: str | None = None,
    planned_steps: list[str] | None = None,
    expected_artifacts: list[str] | None = None,
    explicitly_not_performed: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> DigestionSkillRunPreview:
    return DigestionSkillRunPreview(
        run_preview_id=run_preview_id,
        digestion_input_id=digestion_input_id,
        planned_steps=list(planned_steps or ["read available observation report refs", "produce route signals"]),
        expected_artifacts=list(
            expected_artifacts
            or [
                "DigestionSkillInput",
                "DigestiblePatternSignal",
                "DigestionFinding",
                "DigestionBlocker",
                "DigestionRouteDecision",
                "DigestionSkillOutput",
            ]
        ),
        explicitly_not_performed=list(
            explicitly_not_performed
            or [
                "execution",
                "external_scan",
                "read_only_tool_execution",
                "active_internalization",
                "candidate_creation",
                "registry_mutation",
                "memory_mutation",
            ]
        ),
        metadata=dict(metadata or {}),
    )


def build_digestion_skill_foundation_report(
    digestion_contract_ref: str | None = "internal_triad_skill_contract:digestion:v0.31.0",
    ready_for_v0314_digestion_candidate_internalization_plan: bool = True,
    ready_for_v0315_dominion_skill_foundation: bool = True,
) -> DigestionSkillFoundationReport:
    return DigestionSkillFoundationReport(
        foundation_report_id="digestion_skill_foundation_report:v0.31.3",
        version=V0313_VERSION,
        digestion_contract_ref=digestion_contract_ref,
        supported_source_kinds=[kind for kind in DigestionSkillSourceKind],
        supported_focus_kinds=[kind for kind in DigestionFocusKind],
        supported_routes=[route for route in DigestionRoute],
        supported_output_artifact_kinds=[
            "digestion_skill_input",
            "digestible_pattern_signal",
            "digestion_finding",
            "digestion_blocker",
            "digestion_route_decision",
            "digestion_skill_output",
            "digestion_run_preview",
            "digestion_no_op_decision",
        ],
        prohibited_runtime_actions=list(V0313_REQUIRED_PROHIBITED_RUNTIME_ACTIONS),
        ready_for_v0314_digestion_candidate_internalization_plan=ready_for_v0314_digestion_candidate_internalization_plan,
        ready_for_v0315_dominion_skill_foundation=ready_for_v0315_dominion_skill_foundation,
        ready_for_execution=False,
        ready_for_skill_activation=False,
        ready_for_internalization=False,
        summary="Digestion Skill Foundation defines route signals for later design stages only; no active internalization is enabled.",
        evidence_refs=["v0.31.2 ObservationReportBundle", "v0.31.0 DigestionSkillContract"],
        withdrawal_conditions=[
            "digestible pattern signals are treated as active candidates",
            "route decisions are treated as implementation",
            "registry or memory mutation is introduced",
            "ready_for_execution, ready_for_skill_activation, or ready_for_internalization becomes true",
        ],
        metadata={"foundation_is_runtime_enablement": False},
    )


def build_v0313_readiness_report(foundation_report: DigestionSkillFoundationReport) -> V0313ReadinessReport:
    return V0313ReadinessReport(
        report_id="v0313_readiness_report:digestion_skill_foundation",
        version=V0313_VERSION,
        digestion_foundation_report_id=foundation_report.foundation_report_id,
        summary="v0.31.3 is ready for v0.31.4 design-stage candidate/internalization-plan modeling only; not execution.",
        ready_for_v0314_digestion_candidate_internalization_plan=foundation_report.ready_for_v0314_digestion_candidate_internalization_plan,
        ready_for_v0315_dominion_skill_foundation=foundation_report.ready_for_v0315_dominion_skill_foundation,
        ready_for_execution=False,
        ready_for_skill_activation=False,
        ready_for_internalization=False,
        ready_for_registry_mutation=False,
        completed_items=[
            "digestion source taxonomy",
            "digestion focus taxonomy",
            "digestion route taxonomy",
            "digestion input/source ref models",
            "digestible pattern signal and route decision models",
            foundation_report.foundation_report_id,
        ],
        blocked_items=[],
        future_track_items=[
            "active internalization",
            "internal candidate creation",
            "internalization plan creation",
            "registry mutation",
            "read-only tool execution",
        ],
        evidence_refs=list(foundation_report.evidence_refs),
        withdrawal_conditions=list(foundation_report.withdrawal_conditions),
        metadata={"readiness_report_is_runtime_enablement": False},
    )


def digestion_input_preserves_no_execution(digestion_input: DigestionSkillInput) -> bool:
    return (
        digestion_input.is_execution_request is False
        and not (set(V0313_REQUIRED_PROHIBITED_RUNTIME_ACTIONS) - set(digestion_input.prohibited_runtime_actions))
    )


def digestion_output_preserves_no_execution(output: DigestionSkillOutput) -> bool:
    return (
        output.ready_for_execution is False
        and output.ready_for_skill_activation is False
        and output.ready_for_internalization is False
        and output.ready_for_registry_mutation is False
        and output.active_artifact_registration is False
    )


def digestion_output_is_not_internalization(output: DigestionSkillOutput) -> bool:
    return output.creates_internal_skill_candidate is False and output.creates_internalization_plan is False


def digestion_output_is_not_dominion(output: DigestionSkillOutput) -> bool:
    return output.creates_dominion_target is False


def digestion_run_preview_preserves_no_execution(preview: DigestionSkillRunPreview) -> bool:
    return (
        preview.no_execution_guarantee is True
        and preview.no_external_scan_guarantee is True
        and preview.no_tool_execution_guarantee is True
        and preview.no_internalization_guarantee is True
        and preview.no_candidate_creation_guarantee is True
        and preview.no_registry_mutation_guarantee is True
        and preview.no_memory_mutation_guarantee is True
        and preview.executes_run is False
    )


def digestion_foundation_is_not_runtime_ready(report: DigestionSkillFoundationReport | V0313ReadinessReport) -> bool:
    base = (
        report.ready_for_execution is False
        and report.ready_for_skill_activation is False
        and report.ready_for_internalization is False
        and report.runtime_enablement is False
    )
    if isinstance(report, V0313ReadinessReport):
        return base and report.ready_for_registry_mutation is False
    return base
