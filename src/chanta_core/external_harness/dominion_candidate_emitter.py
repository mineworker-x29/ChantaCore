from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .profiles import _metadata_flag_true, _require_non_blank, _validate_object_list, _validate_string_list
from .risk_classification import (
    ExternalCapabilityRiskClass,
    ExternalCapabilityRiskClassification,
    ExternalCapabilityRiskRoute,
)


V0328_VERSION = "v0.32.8"
V0328_RELEASE_NAME = "v0.32.8 External Dominion Candidate Emitter"

DEFAULT_DOMINION_PROHIBITED_RUNTIME_ACTIONS = [
    "harness execution",
    "reference code execution",
    "install",
    "import runtime",
    "plugin loading",
    "external plugin loading",
    "tool registration",
    "tool invocation",
    "mission installation",
    "mission execution",
    "gateway connection",
    "provider invocation",
    "network",
    "credential",
    "secret file read",
    "command",
    "browser",
    "RPA",
    "packet send",
    "active dominion target creation",
    "dominion decision creation",
    "authority grant",
    "external control",
    "D4-D9 grant",
    "registry mutation",
    "memory mutation",
    "OCEL emission",
]

_D4_D9_LEVELS = {"D4", "D5", "D6", "D7", "D8", "D9"}


class ExternalDominionCandidateKind(StrEnum):
    EXTERNAL_RUNTIME_CONTROL_CANDIDATE = "external_runtime_control_candidate"
    PROVIDER_INVOCATION_CANDIDATE = "provider_invocation_candidate"
    NETWORK_ACCESS_CANDIDATE = "network_access_candidate"
    CREDENTIAL_ACCESS_CANDIDATE = "credential_access_candidate"
    COMMAND_EXECUTION_CANDIDATE = "command_execution_candidate"
    BROWSER_RUNTIME_CANDIDATE = "browser_runtime_candidate"
    RPA_CONTROL_CANDIDATE = "rpa_control_candidate"
    GATEWAY_CONNECTION_CANDIDATE = "gateway_connection_candidate"
    CHANNEL_ACCESS_CANDIDATE = "channel_access_candidate"
    MESSAGE_SEND_CANDIDATE = "message_send_candidate"
    WEBHOOK_CALL_CANDIDATE = "webhook_call_candidate"
    PLUGIN_LOADING_CANDIDATE = "plugin_loading_candidate"
    EXTERNAL_PLUGIN_LOADING_CANDIDATE = "external_plugin_loading_candidate"
    TOOL_INVOCATION_CANDIDATE = "tool_invocation_candidate"
    TOOL_REGISTRATION_CANDIDATE = "tool_registration_candidate"
    MISSION_EXECUTION_CANDIDATE = "mission_execution_candidate"
    MISSION_INSTALLATION_CANDIDATE = "mission_installation_candidate"
    DELEGATION_EXECUTION_CANDIDATE = "delegation_execution_candidate"
    MEMORY_MUTATION_CANDIDATE = "memory_mutation_candidate"
    REGISTRY_MUTATION_CANDIDATE = "registry_mutation_candidate"
    PRIVATE_DATA_ACCESS_CANDIDATE = "private_data_access_candidate"
    RAW_OUTPUT_PERSISTENCE_CANDIDATE = "raw_output_persistence_candidate"
    OCEL_EMISSION_CANDIDATE = "ocel_emission_candidate"
    APPROVAL_BOUNDARY_CANDIDATE = "approval_boundary_candidate"
    AUDIT_BOUNDARY_CANDIDATE = "audit_boundary_candidate"
    FUTURE_TRACK_CANDIDATE = "future_track_candidate"
    NO_OP_CANDIDATE = "no_op_candidate"
    UNKNOWN = "unknown"


class ExternalDominionControlSurfaceKind(StrEnum):
    EXTERNAL_RUNTIME = "external_runtime"
    PROVIDER = "provider"
    NETWORK = "network"
    CREDENTIAL = "credential"
    COMMAND = "command"
    BROWSER = "browser"
    RPA = "rpa"
    GATEWAY = "gateway"
    CHANNEL = "channel"
    MESSAGE = "message"
    WEBHOOK = "webhook"
    PLUGIN = "plugin"
    EXTERNAL_PLUGIN = "external_plugin"
    TOOL = "tool"
    MISSION = "mission"
    DELEGATION = "delegation"
    MEMORY = "memory"
    REGISTRY = "registry"
    PRIVATE_DATA = "private_data"
    RAW_OUTPUT = "raw_output"
    OCEL_TRACE = "ocel_trace"
    APPROVAL = "approval"
    AUDIT = "audit"
    UNKNOWN = "unknown"


class ExternalDominionRiskSurfaceKind(StrEnum):
    EXTERNAL_SIDE_EFFECT = "external_side_effect"
    PRIVATE_DATA_EXPOSURE = "private_data_exposure"
    CREDENTIAL_EXPOSURE = "credential_exposure"
    NETWORK_SIDE_EFFECT = "network_side_effect"
    COMMAND_EXECUTION = "command_execution"
    PROVIDER_INVOCATION = "provider_invocation"
    BROWSER_AUTOMATION = "browser_automation"
    RPA_CONTROL = "rpa_control"
    GATEWAY_CONTROL = "gateway_control"
    CHANNEL_ACCESS = "channel_access"
    MESSAGE_SEND = "message_send"
    WEBHOOK_CALL = "webhook_call"
    PLUGIN_LOADING = "plugin_loading"
    EXTERNAL_PLUGIN_LOADING = "external_plugin_loading"
    TOOL_INVOCATION = "tool_invocation"
    TOOL_REGISTRATION = "tool_registration"
    MISSION_EXECUTION = "mission_execution"
    MISSION_INSTALLATION = "mission_installation"
    DELEGATION_EXECUTION = "delegation_execution"
    MEMORY_CONTAMINATION = "memory_contamination"
    RAW_OUTPUT_PERSISTENCE = "raw_output_persistence"
    REGISTRY_MUTATION = "registry_mutation"
    OCEL_SCHEMA_DRIFT = "ocel_schema_drift"
    OCEL_EMISSION = "ocel_emission"
    APPROVAL_BYPASS = "approval_bypass"
    AUDIT_GAP = "audit_gap"
    UNKNOWN = "unknown"


class ExternalDominionEmissionRoute(StrEnum):
    EMIT_FOR_V0329_CONSOLIDATION = "emit_for_v0329_consolidation"
    REQUIRE_REVIEW = "require_review"
    REQUIRE_FUTURE_GATE = "require_future_gate"
    DEFER = "defer"
    REJECT = "reject"
    BLOCK = "block"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class ExternalDominionCandidateStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    EMITTED = "emitted"
    EMITTED_WITH_GAPS = "emitted_with_gaps"
    REQUIRES_REVIEW = "requires_review"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    REJECTED = "rejected"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class ExternalDominionAuthorityPosture(StrEnum):
    NO_AUTHORITY = "no_authority"
    DESCRIPTIVE_ONLY = "descriptive_only"
    BOUNDARY_ONLY = "boundary_only"
    FUTURE_GATE_ONLY = "future_gate_only"
    NO_OP = "no_op"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"
    UNKNOWN = "unknown"


class ExternalDominionEvidenceQuality(StrEnum):
    UNKNOWN = "unknown"
    NONE = "none"
    WEAK = "weak"
    PARTIAL = "partial"
    SUFFICIENT_FOR_DOMINION_CANDIDATE = "sufficient_for_dominion_candidate"
    SUFFICIENT_FOR_V0329_REVIEW = "sufficient_for_v0329_review"
    CONFLICTING = "conflicting"
    BLOCKED = "blocked"


class ExternalDominionReviewRequirementKind(StrEnum):
    EVIDENCE_REVIEW = "evidence_review"
    BOUNDARY_REVIEW = "boundary_review"
    SAFETY_REVIEW = "safety_review"
    SECURITY_REVIEW = "security_review"
    PRIVACY_REVIEW = "privacy_review"
    CREDENTIAL_REVIEW = "credential_review"
    NETWORK_REVIEW = "network_review"
    COMMAND_REVIEW = "command_review"
    PROVIDER_REVIEW = "provider_review"
    PLUGIN_REVIEW = "plugin_review"
    GATEWAY_REVIEW = "gateway_review"
    MEMORY_REVIEW = "memory_review"
    REGISTRY_REVIEW = "registry_review"
    OCEL_TRACE_REVIEW = "ocel_trace_review"
    APPROVAL_REVIEW = "approval_review"
    AUDIT_REVIEW = "audit_review"
    HUMAN_REVIEW = "human_review"
    FUTURE_GATE_REVIEW = "future_gate_review"
    UNKNOWN = "unknown"


class ExternalDominionBlockerKind(StrEnum):
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    CONFLICTING_EVIDENCE = "conflicting_evidence"
    MISSING_RISK_CLASSIFICATION = "missing_risk_classification"
    MISSING_BOUNDARY_MAP = "missing_boundary_map"
    MISSING_DIGESTION_CANDIDATE = "missing_digestion_candidate"
    MISSING_INTERNAL_CANDIDATE_EMISSION_CONTEXT = "missing_internal_candidate_emission_context"
    UNSAFE_RUNTIME_SURFACE = "unsafe_runtime_surface"
    EXTERNAL_CONTROL_SURFACE = "external_control_surface"
    AUTHORITY_GRANT_REQUIRED = "authority_grant_required"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    PLUGIN_LOADING_SURFACE = "plugin_loading_surface"
    TOOL_INVOCATION_SURFACE = "tool_invocation_surface"
    MISSION_EXECUTION_SURFACE = "mission_execution_surface"
    PROVIDER_INVOCATION_SURFACE = "provider_invocation_surface"
    GATEWAY_CONNECTION_SURFACE = "gateway_connection_surface"
    CREDENTIAL_ACCESS_SURFACE = "credential_access_surface"
    NETWORK_ACCESS_SURFACE = "network_access_surface"
    COMMAND_EXECUTION_SURFACE = "command_execution_surface"
    MEMORY_MUTATION_SURFACE = "memory_mutation_surface"
    REGISTRY_MUTATION_SURFACE = "registry_mutation_surface"
    PRIVATE_DATA_SURFACE = "private_data_surface"
    INCOMPATIBLE_WITH_DOMINION_GOVERNANCE = "incompatible_with_dominion_governance"
    UNKNOWN = "unknown"


class ExternalDominionSourceKind(StrEnum):
    EXTERNAL_CAPABILITY_RISK_CLASSIFICATION = "external_capability_risk_classification"
    EXTERNAL_CAPABILITY_RISK_MAP = "external_capability_risk_map"
    EXTERNAL_CAPABILITY_BOUNDARY_MAP = "external_capability_boundary_map"
    EXTERNAL_DIGESTION_CANDIDATE = "external_digestion_candidate"
    EXTERNAL_DIGESTION_CANDIDATE_SET = "external_digestion_candidate_set"
    EXTERNAL_DIGESTION_GENERATION_REPORT = "external_digestion_generation_report"
    INTERNAL_CANDIDATE_EMISSION_REPORT = "internal_candidate_emission_report"
    EXTERNAL_HARNESS_INTERNAL_CANDIDATE_SET = "external_harness_internal_candidate_set"
    EXTERNAL_MANIFEST_CANDIDATE = "external_manifest_candidate"
    OPENCODE_OBSERVATION_OUTPUT = "opencode_observation_output"
    OPENCLAW_OBSERVATION_OUTPUT = "openclaw_observation_output"
    HERMES_OBSERVATION_OUTPUT = "hermes_observation_output"
    REFERENCE_FILE_INVENTORY = "reference_file_inventory"
    REFERENCE_CORPUS_SNAPSHOT = "reference_corpus_snapshot"
    MANUAL_DOMINION_REVIEW = "manual_dominion_review"
    UNKNOWN = "unknown"


def _validate_version_includes_v0328(version: str) -> None:
    _require_non_blank("version", version)
    if V0328_VERSION not in version:
        raise ValueError("version must include v0.32.8")


def _validate_kind_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.32.8")


def _validate_default_prohibitions(name: str, values: list[str]) -> None:
    _validate_string_list(name, values)
    missing = set(DEFAULT_DOMINION_PROHIBITED_RUNTIME_ACTIONS) - set(values)
    if missing:
        raise ValueError(f"{name} missing v0.32.8 prohibitions: {sorted(missing)}")


def _validate_level_not_d4_d9(level: str | None) -> None:
    if level is None:
        return
    _require_non_blank("max_allowed_level", level)
    normalized = level.strip().upper()
    if any(normalized.startswith(disallowed) for disallowed in _D4_D9_LEVELS):
        raise ValueError("D4-D9 must remain future-track and cannot be granted in v0.32.8")


@dataclass(frozen=True)
class ExternalDominionSourceRef:
    source_ref_id: str
    source_kind: ExternalDominionSourceKind | str
    source_id: str
    risk_classification_id: str | None = None
    digestion_candidate_id: str | None = None
    emitted_candidate_id: str | None = None
    manifest_candidate_id: str | None = None
    harness_kind: str | None = None
    reference_entry_ids: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        ExternalDominionSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _validate_string_list("reference_entry_ids", self.reference_entry_ids)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"source_fetch", "execution", "live_scan"}):
            raise ValueError("ExternalDominionSourceRef is not source fetch or execution")

    @property
    def source_fetch(self) -> bool:
        return False

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionEvidenceRef:
    evidence_ref_id: str
    source_evidence_ref_id: str | None = None
    evidence_kind: str = "static_dominion_evidence"
    evidence_summary: str = "Static dominion evidence reference only."
    quality: ExternalDominionEvidenceQuality | str = ExternalDominionEvidenceQuality.UNKNOWN
    limitations: list[str] = field(default_factory=list)
    conflict_notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("evidence_ref_id", self.evidence_ref_id)
        _require_non_blank("evidence_kind", self.evidence_kind)
        _require_non_blank("evidence_summary", self.evidence_summary)
        ExternalDominionEvidenceQuality(self.quality)
        _validate_string_list("limitations", self.limitations)
        _validate_string_list("conflict_notes", self.conflict_notes)
        if _metadata_flag_true(self.metadata, {"runtime_trust", "authority_grant"}):
            raise ValueError("ExternalDominionEvidenceRef is not runtime trust or authority grant")

    @property
    def runtime_trust(self) -> bool:
        return False

    @property
    def authority_grant(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionRiskSignal:
    risk_signal_id: str
    source_ref_ids: list[str]
    candidate_kind: ExternalDominionCandidateKind | str
    control_surfaces: list[ExternalDominionControlSurfaceKind | str] = field(default_factory=list)
    risk_surfaces: list[ExternalDominionRiskSurfaceKind | str] = field(default_factory=list)
    severity: str = "unknown"
    summary: str = "Static dominion risk signal."
    recommended_boundary_kinds: list[str] = field(default_factory=list)
    recommended_review_kinds: list[ExternalDominionReviewRequirementKind | str] = field(default_factory=list)
    evidence_refs: list[ExternalDominionEvidenceRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_signal_id", self.risk_signal_id)
        _validate_string_list("source_ref_ids", self.source_ref_ids)
        ExternalDominionCandidateKind(self.candidate_kind)
        _validate_kind_list("control_surfaces", self.control_surfaces, ExternalDominionControlSurfaceKind)
        _validate_kind_list("risk_surfaces", self.risk_surfaces, ExternalDominionRiskSurfaceKind)
        _require_non_blank("severity", self.severity)
        _require_non_blank("summary", self.summary)
        _validate_string_list("recommended_boundary_kinds", self.recommended_boundary_kinds)
        _validate_kind_list("recommended_review_kinds", self.recommended_review_kinds, ExternalDominionReviewRequirementKind)
        _validate_object_list("evidence_refs", self.evidence_refs, ExternalDominionEvidenceRef)
        if self.severity.lower() in {"high", "critical", "blocked"} and not self.recommended_boundary_kinds and not self.recommended_review_kinds:
            raise ValueError("high/critical/blocked severity requires boundary or review")
        if _metadata_flag_true(self.metadata, {"proof", "authority_grant"}):
            raise ValueError("ExternalDominionRiskSignal is not proof and does not grant authority")

    @property
    def proof(self) -> bool:
        return False

    @property
    def authority_grant(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionControlBoundaryCandidate:
    boundary_candidate_id: str
    boundary_name: str
    boundary_summary: str
    control_surfaces: list[ExternalDominionControlSurfaceKind | str] = field(default_factory=list)
    risk_surfaces: list[ExternalDominionRiskSurfaceKind | str] = field(default_factory=list)
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_DOMINION_PROHIBITED_RUNTIME_ACTIONS))
    required_reviews: list[ExternalDominionReviewRequirementKind | str] = field(default_factory=list)
    required_future_gates: list[str] = field(default_factory=list)
    blocks_execution: bool = True
    blocks_external_control: bool = True
    blocks_authority_grant: bool = True
    evidence_refs: list[ExternalDominionEvidenceRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_candidate_id", self.boundary_candidate_id)
        _require_non_blank("boundary_name", self.boundary_name)
        _require_non_blank("boundary_summary", self.boundary_summary)
        _validate_kind_list("control_surfaces", self.control_surfaces, ExternalDominionControlSurfaceKind)
        _validate_kind_list("risk_surfaces", self.risk_surfaces, ExternalDominionRiskSurfaceKind)
        _validate_default_prohibitions("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_kind_list("required_reviews", self.required_reviews, ExternalDominionReviewRequirementKind)
        _validate_string_list("required_future_gates", self.required_future_gates)
        if self.blocks_execution is not True:
            raise ValueError("blocks_execution must default True in v0.32.8")
        if self.blocks_external_control is not True:
            raise ValueError("blocks_external_control must default True in v0.32.8")
        if self.blocks_authority_grant is not True:
            raise ValueError("blocks_authority_grant must default True in v0.32.8")
        _validate_object_list("evidence_refs", self.evidence_refs, ExternalDominionEvidenceRef)
        if _metadata_flag_true(self.metadata, {"permission", "runtime_enforcement"}):
            raise ValueError("ExternalDominionControlBoundaryCandidate is not permission or runtime enforcement")

    @property
    def permission(self) -> bool:
        return False

    @property
    def runtime_enforcement(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionReviewRequirement:
    review_requirement_id: str
    requirement_kind: ExternalDominionReviewRequirementKind | str
    target_candidate_ids: list[str] = field(default_factory=list)
    reason: str = "Static dominion review required."
    required_evidence_refs: list[str] = field(default_factory=list)
    required_reviewer_refs: list[str] = field(default_factory=list)
    approval_granted: bool = False
    blocks_external_control: bool = True
    blocks_authority_grant: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("review_requirement_id", self.review_requirement_id)
        ExternalDominionReviewRequirementKind(self.requirement_kind)
        _require_non_blank("reason", self.reason)
        for name in ("target_candidate_ids", "required_evidence_refs", "required_reviewer_refs"):
            _validate_string_list(name, getattr(self, name))
        if self.approval_granted is not False:
            raise ValueError("approval_granted must always be False in v0.32.8")
        if self.blocks_external_control is not True:
            raise ValueError("blocks_external_control must default True in v0.32.8")
        if self.blocks_authority_grant is not True:
            raise ValueError("blocks_authority_grant must default True in v0.32.8")
        if _metadata_flag_true(self.metadata, {"approval", "approval_granted"}):
            raise ValueError("ExternalDominionReviewRequirement is not approval")

    @property
    def approval(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionBlocker:
    blocker_id: str
    blocker_kind: ExternalDominionBlockerKind | str
    source_ref_ids: list[str] = field(default_factory=list)
    target_candidate_id: str | None = None
    reason: str = "Static dominion blocker."
    blocks_v0329: bool = True
    routes_to_future_gate: bool = False
    routes_to_no_op: bool = False
    evidence_refs: list[ExternalDominionEvidenceRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("blocker_id", self.blocker_id)
        ExternalDominionBlockerKind(self.blocker_kind)
        _validate_string_list("source_ref_ids", self.source_ref_ids)
        _require_non_blank("reason", self.reason)
        for name in ("blocks_v0329", "routes_to_future_gate", "routes_to_no_op"):
            if not isinstance(getattr(self, name), bool):
                raise TypeError(f"{name} must be bool")
        _validate_object_list("evidence_refs", self.evidence_refs, ExternalDominionEvidenceRef)
        if _metadata_flag_true(self.metadata, {"remediation", "execution"}):
            raise ValueError("ExternalDominionBlocker does not execute remediation")

    @property
    def remediation_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class EmittedInternalDominionTargetCandidate:
    dominion_target_candidate_id: str
    candidate_kind: ExternalDominionCandidateKind | str
    status: ExternalDominionCandidateStatus | str
    title: str
    summary: str
    source_refs: list[ExternalDominionSourceRef] = field(default_factory=list)
    control_surfaces: list[ExternalDominionControlSurfaceKind | str] = field(default_factory=list)
    risk_surfaces: list[ExternalDominionRiskSurfaceKind | str] = field(default_factory=list)
    risk_signals: list[ExternalDominionRiskSignal] = field(default_factory=list)
    boundary_candidate_ids: list[str] = field(default_factory=list)
    future_gate_ids: list[str] = field(default_factory=list)
    no_op_decision_ids: list[str] = field(default_factory=list)
    authority_posture: ExternalDominionAuthorityPosture | str = ExternalDominionAuthorityPosture.NO_AUTHORITY
    max_allowed_level: str | None = None
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_DOMINION_PROHIBITED_RUNTIME_ACTIONS))
    evidence_refs: list[ExternalDominionEvidenceRef] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_active_dominion_target_creation: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("dominion_target_candidate_id", self.dominion_target_candidate_id)
        ExternalDominionCandidateKind(self.candidate_kind)
        ExternalDominionCandidateStatus(self.status)
        _require_non_blank("title", self.title)
        _require_non_blank("summary", self.summary)
        _validate_object_list("source_refs", self.source_refs, ExternalDominionSourceRef)
        _validate_kind_list("control_surfaces", self.control_surfaces, ExternalDominionControlSurfaceKind)
        _validate_kind_list("risk_surfaces", self.risk_surfaces, ExternalDominionRiskSurfaceKind)
        _validate_object_list("risk_signals", self.risk_signals, ExternalDominionRiskSignal)
        for name in ("boundary_candidate_ids", "future_gate_ids", "no_op_decision_ids", "assumptions", "limitations", "gaps"):
            _validate_string_list(name, getattr(self, name))
        ExternalDominionAuthorityPosture(self.authority_posture)
        _validate_level_not_d4_d9(self.max_allowed_level)
        _validate_default_prohibitions("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_object_list("evidence_refs", self.evidence_refs, ExternalDominionEvidenceRef)
        _validate_false(self, ("ready_for_active_dominion_target_creation", "ready_for_external_control", "ready_for_authority_grant", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"active_dominion_target", "external_control", "authority_grant", "d4_d9_grant"}):
            raise ValueError("EmittedInternalDominionTargetCandidate is not active target, external control, or authority grant")

    @property
    def active_internal_dominion_target(self) -> bool:
        return False

    @property
    def external_control(self) -> bool:
        return False

    @property
    def d4_d9_grant(self) -> bool:
        return False


@dataclass(frozen=True)
class EmittedDominionControlBoundaryCandidate:
    emitted_boundary_candidate_id: str
    target_candidate_id: str | None
    boundary_candidate: ExternalDominionControlBoundaryCandidate
    summary: str = "Static emitted dominion control boundary candidate."
    evidence_refs: list[ExternalDominionEvidenceRef] = field(default_factory=list)
    ready_for_runtime_enforcement: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("emitted_boundary_candidate_id", self.emitted_boundary_candidate_id)
        if not isinstance(self.boundary_candidate, ExternalDominionControlBoundaryCandidate):
            raise TypeError("boundary_candidate must be ExternalDominionControlBoundaryCandidate")
        _require_non_blank("summary", self.summary)
        _validate_object_list("evidence_refs", self.evidence_refs, ExternalDominionEvidenceRef)
        _validate_false(self, ("ready_for_runtime_enforcement", "ready_for_external_control", "ready_for_authority_grant", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"permission", "runtime_enforcement"}):
            raise ValueError("EmittedDominionControlBoundaryCandidate is not permission")

    @property
    def permission(self) -> bool:
        return False


@dataclass(frozen=True)
class EmittedDominionFutureGateItem:
    future_gate_id: str
    target_candidate_id: str | None = None
    gate_kind: str = "future_dominion_review_gate"
    reason: str = "Future gate required before any runtime consideration."
    required_artifacts: list[str] = field(default_factory=list)
    required_reviews: list[ExternalDominionReviewRequirementKind | str] = field(default_factory=list)
    prohibited_until_satisfied: list[str] = field(default_factory=lambda: list(DEFAULT_DOMINION_PROHIBITED_RUNTIME_ACTIONS))
    evidence_refs: list[ExternalDominionEvidenceRef] = field(default_factory=list)
    ready_now: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("future_gate_id", self.future_gate_id)
        _require_non_blank("gate_kind", self.gate_kind)
        _require_non_blank("reason", self.reason)
        _validate_string_list("required_artifacts", self.required_artifacts)
        _validate_kind_list("required_reviews", self.required_reviews, ExternalDominionReviewRequirementKind)
        _validate_default_prohibitions("prohibited_until_satisfied", self.prohibited_until_satisfied)
        _validate_object_list("evidence_refs", self.evidence_refs, ExternalDominionEvidenceRef)
        _validate_false(self, ("ready_now", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"readiness", "execution"}):
            raise ValueError("EmittedDominionFutureGateItem is not readiness")

    @property
    def readiness(self) -> bool:
        return False


@dataclass(frozen=True)
class EmittedDominionNoOpDecision:
    no_op_id: str
    target_candidate_id: str | None = None
    reason: str = "No dominion candidate action is recommended."
    safe_alternatives: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    evidence_refs: list[ExternalDominionEvidenceRef] = field(default_factory=list)
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("no_op_id", self.no_op_id)
        _require_non_blank("reason", self.reason)
        _validate_string_list("safe_alternatives", self.safe_alternatives)
        _validate_string_list("blocked_reasons", self.blocked_reasons)
        _validate_object_list("evidence_refs", self.evidence_refs, ExternalDominionEvidenceRef)
        _validate_false(self, ("ready_for_execution",))
        if _metadata_flag_true(self.metadata, {"failure", "execution"}):
            raise ValueError("EmittedDominionNoOpDecision is valid and not failure")

    @property
    def failure(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalHarnessDominionCandidate:
    dominion_candidate_id: str
    candidate_kind: ExternalDominionCandidateKind | str
    route: ExternalDominionEmissionRoute | str
    status: ExternalDominionCandidateStatus | str
    title: str
    summary: str
    source_refs: list[ExternalDominionSourceRef] = field(default_factory=list)
    target_candidate: EmittedInternalDominionTargetCandidate | None = None
    boundary_candidates: list[EmittedDominionControlBoundaryCandidate] = field(default_factory=list)
    future_gate_items: list[EmittedDominionFutureGateItem] = field(default_factory=list)
    no_op_decisions: list[EmittedDominionNoOpDecision] = field(default_factory=list)
    review_requirements: list[ExternalDominionReviewRequirement] = field(default_factory=list)
    blockers: list[ExternalDominionBlocker] = field(default_factory=list)
    authority_posture: ExternalDominionAuthorityPosture | str = ExternalDominionAuthorityPosture.NO_AUTHORITY
    evidence_quality: ExternalDominionEvidenceQuality | str = ExternalDominionEvidenceQuality.UNKNOWN
    evidence_refs: list[ExternalDominionEvidenceRef] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0329_consolidation: bool = False
    ready_for_active_dominion_target_creation: bool = False
    ready_for_dominion_decision_creation: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("dominion_candidate_id", self.dominion_candidate_id)
        ExternalDominionCandidateKind(self.candidate_kind)
        ExternalDominionEmissionRoute(self.route)
        ExternalDominionCandidateStatus(self.status)
        _require_non_blank("title", self.title)
        _require_non_blank("summary", self.summary)
        _validate_object_list("source_refs", self.source_refs, ExternalDominionSourceRef)
        if self.target_candidate is not None and not isinstance(self.target_candidate, EmittedInternalDominionTargetCandidate):
            raise TypeError("target_candidate must be EmittedInternalDominionTargetCandidate or None")
        _validate_object_list("boundary_candidates", self.boundary_candidates, EmittedDominionControlBoundaryCandidate)
        _validate_object_list("future_gate_items", self.future_gate_items, EmittedDominionFutureGateItem)
        _validate_object_list("no_op_decisions", self.no_op_decisions, EmittedDominionNoOpDecision)
        _validate_object_list("review_requirements", self.review_requirements, ExternalDominionReviewRequirement)
        _validate_object_list("blockers", self.blockers, ExternalDominionBlocker)
        ExternalDominionAuthorityPosture(self.authority_posture)
        ExternalDominionEvidenceQuality(self.evidence_quality)
        _validate_object_list("evidence_refs", self.evidence_refs, ExternalDominionEvidenceRef)
        for name in ("assumptions", "limitations", "gaps"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(
            self,
            (
                "ready_for_active_dominion_target_creation",
                "ready_for_dominion_decision_creation",
                "ready_for_external_control",
                "ready_for_authority_grant",
                "ready_for_execution",
            ),
        )
        if _metadata_flag_true(self.metadata, {"active_dominion_target", "dominion_decision", "authority_grant"}):
            raise ValueError("ExternalHarnessDominionCandidate is not active target, decision, or authority grant")

    @property
    def active_dominion_target(self) -> bool:
        return False

    @property
    def dominion_decision(self) -> bool:
        return False

    @property
    def authority_grant(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalHarnessDominionCandidateSet:
    candidate_set_id: str
    version: str = V0328_VERSION
    source_risk_classification_report_id: str | None = None
    source_digestion_candidate_set_id: str | None = None
    source_internal_candidate_set_id: str | None = None
    candidates: list[ExternalHarnessDominionCandidate] = field(default_factory=list)
    target_candidates: list[EmittedInternalDominionTargetCandidate] = field(default_factory=list)
    boundary_candidates: list[EmittedDominionControlBoundaryCandidate] = field(default_factory=list)
    future_gate_items: list[EmittedDominionFutureGateItem] = field(default_factory=list)
    no_op_decisions: list[EmittedDominionNoOpDecision] = field(default_factory=list)
    review_requirements: list[ExternalDominionReviewRequirement] = field(default_factory=list)
    blockers: list[ExternalDominionBlocker] = field(default_factory=list)
    emitted_candidate_ids: list[str] = field(default_factory=list)
    blocked_source_refs: list[str] = field(default_factory=list)
    deferred_source_refs: list[str] = field(default_factory=list)
    future_track_source_refs: list[str] = field(default_factory=list)
    no_op_source_refs: list[str] = field(default_factory=list)
    evidence_refs: list[ExternalDominionEvidenceRef] = field(default_factory=list)
    ready_for_v0329_consolidation: bool = False
    ready_for_active_dominion_target_creation: bool = False
    ready_for_dominion_decision_creation: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("candidate_set_id", self.candidate_set_id)
        _validate_version_includes_v0328(self.version)
        _validate_object_list("candidates", self.candidates, ExternalHarnessDominionCandidate)
        _validate_object_list("target_candidates", self.target_candidates, EmittedInternalDominionTargetCandidate)
        _validate_object_list("boundary_candidates", self.boundary_candidates, EmittedDominionControlBoundaryCandidate)
        _validate_object_list("future_gate_items", self.future_gate_items, EmittedDominionFutureGateItem)
        _validate_object_list("no_op_decisions", self.no_op_decisions, EmittedDominionNoOpDecision)
        _validate_object_list("review_requirements", self.review_requirements, ExternalDominionReviewRequirement)
        _validate_object_list("blockers", self.blockers, ExternalDominionBlocker)
        for name in ("emitted_candidate_ids", "blocked_source_refs", "deferred_source_refs", "future_track_source_refs", "no_op_source_refs"):
            _validate_string_list(name, getattr(self, name))
        _validate_object_list("evidence_refs", self.evidence_refs, ExternalDominionEvidenceRef)
        _validate_false(
            self,
            (
                "ready_for_active_dominion_target_creation",
                "ready_for_dominion_decision_creation",
                "ready_for_external_control",
                "ready_for_authority_grant",
                "ready_for_execution",
            ),
        )
        if _metadata_flag_true(self.metadata, {"runtime_registry", "registry"}):
            raise ValueError("ExternalHarnessDominionCandidateSet is not runtime registry")

    @property
    def runtime_registry(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionCandidateEmissionInput:
    emission_input_id: str
    source_version: str = V0328_VERSION
    risk_classification_ids: list[str] = field(default_factory=list)
    risk_classification_report_ids: list[str] = field(default_factory=list)
    risk_map_ids: list[str] = field(default_factory=list)
    boundary_map_ids: list[str] = field(default_factory=list)
    external_digestion_candidate_ids: list[str] = field(default_factory=list)
    external_digestion_candidate_set_ids: list[str] = field(default_factory=list)
    internal_candidate_emission_report_ids: list[str] = field(default_factory=list)
    external_harness_internal_candidate_set_ids: list[str] = field(default_factory=list)
    source_refs: list[ExternalDominionSourceRef] = field(default_factory=list)
    requested_candidate_kinds: list[ExternalDominionCandidateKind | str] = field(default_factory=list)
    task_summary: str = "Emit external dominion candidate design artifacts."
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_DOMINION_PROHIBITED_RUNTIME_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("emission_input_id", self.emission_input_id)
        _require_non_blank("source_version", self.source_version)
        for name in (
            "risk_classification_ids",
            "risk_classification_report_ids",
            "risk_map_ids",
            "boundary_map_ids",
            "external_digestion_candidate_ids",
            "external_digestion_candidate_set_ids",
            "internal_candidate_emission_report_ids",
            "external_harness_internal_candidate_set_ids",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_object_list("source_refs", self.source_refs, ExternalDominionSourceRef)
        _validate_kind_list("requested_candidate_kinds", self.requested_candidate_kinds, ExternalDominionCandidateKind)
        _require_non_blank("task_summary", self.task_summary)
        _validate_default_prohibitions("prohibited_runtime_actions", self.prohibited_runtime_actions)
        if _metadata_flag_true(self.metadata, {"execution_request", "external_control_request", "authority_request"}):
            raise ValueError("ExternalDominionCandidateEmissionInput is not execution request")

    @property
    def execution_request(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionCandidateEmissionFinding:
    finding_id: str
    emission_input_id: str
    source_ref_ids: list[str]
    target_candidate_id: str | None
    candidate_kind: ExternalDominionCandidateKind | str
    route: ExternalDominionEmissionRoute | str
    status: ExternalDominionCandidateStatus | str
    authority_posture: ExternalDominionAuthorityPosture | str
    summary: str
    risk_signal_ids: list[str] = field(default_factory=list)
    blocker_ids: list[str] = field(default_factory=list)
    review_requirement_ids: list[str] = field(default_factory=list)
    evidence_quality: ExternalDominionEvidenceQuality | str = ExternalDominionEvidenceQuality.UNKNOWN
    evidence_refs: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("emission_input_id", self.emission_input_id)
        _validate_string_list("source_ref_ids", self.source_ref_ids)
        ExternalDominionCandidateKind(self.candidate_kind)
        ExternalDominionEmissionRoute(self.route)
        ExternalDominionCandidateStatus(self.status)
        ExternalDominionAuthorityPosture(self.authority_posture)
        _require_non_blank("summary", self.summary)
        ExternalDominionEvidenceQuality(self.evidence_quality)
        for name in ("risk_signal_ids", "blocker_ids", "review_requirement_ids", "evidence_refs", "assumptions", "limitations"):
            _validate_string_list(name, getattr(self, name))
        if _metadata_flag_true(self.metadata, {"active_target", "authority_grant"}):
            raise ValueError("ExternalDominionCandidateEmissionFinding is not active target or authority grant")

    @property
    def active_target(self) -> bool:
        return False

    @property
    def authority_grant(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionCandidateEmissionReport:
    report_id: str
    version: str
    emission_input_id: str
    candidate_set_id: str | None = None
    findings: list[ExternalDominionCandidateEmissionFinding] = field(default_factory=list)
    summary: str = "External dominion candidate emission report for design artifacts."
    emitted_candidate_count: int = 0
    target_candidate_count: int = 0
    boundary_candidate_count: int = 0
    future_gate_count: int = 0
    no_op_count: int = 0
    blocked_items: list[str] = field(default_factory=list)
    deferred_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0329_consolidation: bool = False
    ready_for_active_dominion_target_creation: bool = False
    ready_for_dominion_decision_creation: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0328(self.version)
        _require_non_blank("emission_input_id", self.emission_input_id)
        _validate_object_list("findings", self.findings, ExternalDominionCandidateEmissionFinding)
        _require_non_blank("summary", self.summary)
        for name in ("emitted_candidate_count", "target_candidate_count", "boundary_candidate_count", "future_gate_count", "no_op_count"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        for name in ("blocked_items", "deferred_items", "future_track_items", "gaps", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(
            self,
            (
                "ready_for_active_dominion_target_creation",
                "ready_for_dominion_decision_creation",
                "ready_for_external_control",
                "ready_for_authority_grant",
                "ready_for_execution",
            ),
        )
        if _metadata_flag_true(self.metadata, {"runtime_result", "authority_grant"}):
            raise ValueError("ExternalDominionCandidateEmissionReport is not runtime result")

    @property
    def runtime_result(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionCandidateRunPreview:
    run_preview_id: str
    emission_input_id: str | None = None
    planned_steps: list[str] = field(default_factory=list)
    expected_artifacts: list[str] = field(default_factory=list)
    explicitly_not_performed: list[str] = field(default_factory=list)
    no_harness_execution_guarantee: bool = True
    no_reference_code_execution_guarantee: bool = True
    no_install_guarantee: bool = True
    no_import_runtime_guarantee: bool = True
    no_plugin_loading_guarantee: bool = True
    no_tool_registration_guarantee: bool = True
    no_tool_invocation_guarantee: bool = True
    no_mission_installation_guarantee: bool = True
    no_mission_execution_guarantee: bool = True
    no_provider_invocation_guarantee: bool = True
    no_gateway_connection_guarantee: bool = True
    no_network_access_guarantee: bool = True
    no_credential_access_guarantee: bool = True
    no_command_execution_guarantee: bool = True
    no_secret_file_read_guarantee: bool = True
    no_active_dominion_target_creation_guarantee: bool = True
    no_dominion_decision_creation_guarantee: bool = True
    no_authority_grant_guarantee: bool = True
    no_external_control_guarantee: bool = True
    no_registry_mutation_guarantee: bool = True
    no_memory_mutation_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must always be True in v0.32.8")
        if _metadata_flag_true(self.metadata, {"execution"}):
            raise ValueError("ExternalDominionCandidateRunPreview is not execution")

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionCandidateNoRuntimeGuarantee:
    guarantee_id: str
    version: str
    no_harness_execution: bool = True
    no_reference_code_execution: bool = True
    no_dependency_install: bool = True
    no_import_runtime: bool = True
    no_plugin_loading: bool = True
    no_external_plugin_loading: bool = True
    no_tool_registration: bool = True
    no_tool_invocation: bool = True
    no_mission_installation: bool = True
    no_mission_execution: bool = True
    no_gateway_connection: bool = True
    no_provider_invocation: bool = True
    no_network_access: bool = True
    no_credential_access: bool = True
    no_secret_file_read: bool = True
    no_command_execution: bool = True
    no_active_dominion_target_creation: bool = True
    no_dominion_decision_creation: bool = True
    no_authority_grant: bool = True
    no_external_control: bool = True
    no_d4_d9_grant: bool = True
    no_registry_mutation: bool = True
    no_memory_mutation: bool = True
    no_ocel_emission: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version_includes_v0328(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must always be True in v0.32.8")
        _validate_string_list("evidence_refs", self.evidence_refs)


@dataclass(frozen=True)
class V0328ReadinessReport:
    report_id: str
    version: str
    emission_report_id: str | None = None
    candidate_set_id: str | None = None
    summary: str = "v0.32.8 readiness is limited to design-stage handoff."
    ready_for_v0329_external_observation_digestion_consolidation: bool = False
    ready_for_execution: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    ready_for_active_dominion_target_creation: bool = False
    ready_for_dominion_decision_creation: bool = False
    ready_for_dominion_runtime: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_gateway_connection: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    ready_for_browser_runtime_control: bool = False
    ready_for_rpa_runtime_control: bool = False
    ready_for_packet_send: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_DOMINION_PROHIBITED_RUNTIME_ACTIONS))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0328(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(
            self,
            (
                "ready_for_execution",
                "ready_for_external_control",
                "ready_for_authority_grant",
                "ready_for_active_dominion_target_creation",
                "ready_for_dominion_decision_creation",
                "ready_for_dominion_runtime",
                "ready_for_provider_invocation",
                "ready_for_gateway_connection",
                "ready_for_network_access",
                "ready_for_credential_access",
                "ready_for_command_execution",
                "ready_for_browser_runtime_control",
                "ready_for_rpa_runtime_control",
                "ready_for_packet_send",
                "ready_for_registry_mutation",
                "ready_for_memory_mutation",
            ),
        )
        for name in ("completed_items", "blocked_items", "future_track_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_default_prohibitions("prohibited_until_later_gate", self.prohibited_until_later_gate)
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "external_control", "authority_grant"}):
            raise ValueError("V0328ReadinessReport is not runtime enablement")


def build_external_dominion_source_ref(
    source_ref_id: str,
    source_kind: ExternalDominionSourceKind | str,
    source_id: str,
    **kwargs: Any,
) -> ExternalDominionSourceRef:
    return ExternalDominionSourceRef(source_ref_id=source_ref_id, source_kind=source_kind, source_id=source_id, **kwargs)


def build_external_dominion_evidence_ref(evidence_ref_id: str, **kwargs: Any) -> ExternalDominionEvidenceRef:
    return ExternalDominionEvidenceRef(evidence_ref_id=evidence_ref_id, **kwargs)


def build_external_dominion_risk_signal(
    risk_signal_id: str,
    source_ref_ids: list[str],
    candidate_kind: ExternalDominionCandidateKind | str,
    **kwargs: Any,
) -> ExternalDominionRiskSignal:
    return ExternalDominionRiskSignal(
        risk_signal_id=risk_signal_id,
        source_ref_ids=list(source_ref_ids),
        candidate_kind=candidate_kind,
        **kwargs,
    )


def build_external_dominion_control_boundary_candidate(
    boundary_candidate_id: str,
    boundary_name: str,
    boundary_summary: str,
    **kwargs: Any,
) -> ExternalDominionControlBoundaryCandidate:
    return ExternalDominionControlBoundaryCandidate(
        boundary_candidate_id=boundary_candidate_id,
        boundary_name=boundary_name,
        boundary_summary=boundary_summary,
        **kwargs,
    )


def build_external_dominion_review_requirement(
    review_requirement_id: str,
    requirement_kind: ExternalDominionReviewRequirementKind | str,
    **kwargs: Any,
) -> ExternalDominionReviewRequirement:
    return ExternalDominionReviewRequirement(
        review_requirement_id=review_requirement_id,
        requirement_kind=requirement_kind,
        **kwargs,
    )


def build_external_dominion_blocker(
    blocker_id: str,
    blocker_kind: ExternalDominionBlockerKind | str,
    **kwargs: Any,
) -> ExternalDominionBlocker:
    return ExternalDominionBlocker(blocker_id=blocker_id, blocker_kind=blocker_kind, **kwargs)


def build_emitted_internal_dominion_target_candidate(
    dominion_target_candidate_id: str,
    candidate_kind: ExternalDominionCandidateKind | str,
    title: str,
    summary: str,
    **kwargs: Any,
) -> EmittedInternalDominionTargetCandidate:
    return EmittedInternalDominionTargetCandidate(
        dominion_target_candidate_id=dominion_target_candidate_id,
        candidate_kind=candidate_kind,
        status=kwargs.pop("status", ExternalDominionCandidateStatus.EMITTED_WITH_GAPS),
        title=title,
        summary=summary,
        **kwargs,
    )


def build_emitted_dominion_control_boundary_candidate(
    emitted_boundary_candidate_id: str,
    target_candidate_id: str | None,
    boundary_candidate: ExternalDominionControlBoundaryCandidate,
    **kwargs: Any,
) -> EmittedDominionControlBoundaryCandidate:
    return EmittedDominionControlBoundaryCandidate(
        emitted_boundary_candidate_id=emitted_boundary_candidate_id,
        target_candidate_id=target_candidate_id,
        boundary_candidate=boundary_candidate,
        **kwargs,
    )


def build_emitted_dominion_future_gate_item(future_gate_id: str, **kwargs: Any) -> EmittedDominionFutureGateItem:
    return EmittedDominionFutureGateItem(future_gate_id=future_gate_id, **kwargs)


def build_emitted_dominion_no_op_decision(no_op_id: str, **kwargs: Any) -> EmittedDominionNoOpDecision:
    return EmittedDominionNoOpDecision(no_op_id=no_op_id, **kwargs)


def build_external_harness_dominion_candidate(
    dominion_candidate_id: str,
    candidate_kind: ExternalDominionCandidateKind | str,
    route: ExternalDominionEmissionRoute | str,
    status: ExternalDominionCandidateStatus | str,
    title: str,
    summary: str,
    **kwargs: Any,
) -> ExternalHarnessDominionCandidate:
    return ExternalHarnessDominionCandidate(
        dominion_candidate_id=dominion_candidate_id,
        candidate_kind=candidate_kind,
        route=route,
        status=status,
        title=title,
        summary=summary,
        **kwargs,
    )


def build_external_harness_dominion_candidate_set(candidate_set_id: str, **kwargs: Any) -> ExternalHarnessDominionCandidateSet:
    return ExternalHarnessDominionCandidateSet(candidate_set_id=candidate_set_id, version=V0328_VERSION, **kwargs)


def build_external_dominion_candidate_emission_input(
    emission_input_id: str,
    **kwargs: Any,
) -> ExternalDominionCandidateEmissionInput:
    return ExternalDominionCandidateEmissionInput(emission_input_id=emission_input_id, **kwargs)


def build_external_dominion_candidate_emission_finding(
    finding_id: str,
    emission_input_id: str,
    source_ref_ids: list[str],
    target_candidate_id: str | None,
    candidate_kind: ExternalDominionCandidateKind | str,
    route: ExternalDominionEmissionRoute | str,
    status: ExternalDominionCandidateStatus | str,
    authority_posture: ExternalDominionAuthorityPosture | str,
    summary: str,
    **kwargs: Any,
) -> ExternalDominionCandidateEmissionFinding:
    return ExternalDominionCandidateEmissionFinding(
        finding_id=finding_id,
        emission_input_id=emission_input_id,
        source_ref_ids=list(source_ref_ids),
        target_candidate_id=target_candidate_id,
        candidate_kind=candidate_kind,
        route=route,
        status=status,
        authority_posture=authority_posture,
        summary=summary,
        **kwargs,
    )


def build_external_dominion_candidate_emission_report(
    report_id: str,
    emission_input_id: str,
    **kwargs: Any,
) -> ExternalDominionCandidateEmissionReport:
    return ExternalDominionCandidateEmissionReport(
        report_id=report_id,
        version=V0328_VERSION,
        emission_input_id=emission_input_id,
        **kwargs,
    )


def build_external_dominion_candidate_run_preview(
    run_preview_id: str = "external_dominion_candidate_run_preview:v0.32.8",
    **kwargs: Any,
) -> ExternalDominionCandidateRunPreview:
    return ExternalDominionCandidateRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_external_dominion_candidate_no_runtime_guarantee(
    guarantee_id: str = "external_dominion_candidate_no_runtime_guarantee:v0.32.8",
    evidence_refs: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ExternalDominionCandidateNoRuntimeGuarantee:
    return ExternalDominionCandidateNoRuntimeGuarantee(
        guarantee_id=guarantee_id,
        version=V0328_VERSION,
        evidence_refs=list(evidence_refs or []),
        metadata=dict(metadata or {}),
    )


def build_v0328_readiness_report(
    report_id: str = "v0328_readiness_report",
    emission_report_id: str | None = None,
    candidate_set_id: str | None = None,
    **kwargs: Any,
) -> V0328ReadinessReport:
    return V0328ReadinessReport(
        report_id=report_id,
        version=V0328_VERSION,
        emission_report_id=emission_report_id,
        candidate_set_id=candidate_set_id,
        **kwargs,
    )


def infer_external_dominion_candidate_kind_from_risk_classification(
    classification: ExternalCapabilityRiskClassification,
) -> ExternalDominionCandidateKind:
    route = ExternalCapabilityRiskRoute(classification.route)
    risk_class = ExternalCapabilityRiskClass(classification.risk_class)
    if route != ExternalCapabilityRiskRoute.SEND_TO_V0328_DOMINION_EMITTER and risk_class != ExternalCapabilityRiskClass.DOMINION_REQUIRED:
        if route == ExternalCapabilityRiskRoute.NO_OP:
            return ExternalDominionCandidateKind.NO_OP_CANDIDATE
        if route == ExternalCapabilityRiskRoute.REQUIRE_FUTURE_GATE:
            return ExternalDominionCandidateKind.FUTURE_TRACK_CANDIDATE
    surfaces = [factor.risk_surface for factor in classification.risk_factors]
    blockers = infer_external_dominion_blockers_from_risk_surfaces(surfaces)
    if ExternalDominionBlockerKind.COMMAND_EXECUTION_SURFACE in blockers:
        return ExternalDominionCandidateKind.COMMAND_EXECUTION_CANDIDATE
    if ExternalDominionBlockerKind.CREDENTIAL_ACCESS_SURFACE in blockers:
        return ExternalDominionCandidateKind.CREDENTIAL_ACCESS_CANDIDATE
    if ExternalDominionBlockerKind.NETWORK_ACCESS_SURFACE in blockers:
        return ExternalDominionCandidateKind.NETWORK_ACCESS_CANDIDATE
    if ExternalDominionBlockerKind.PROVIDER_INVOCATION_SURFACE in blockers:
        return ExternalDominionCandidateKind.PROVIDER_INVOCATION_CANDIDATE
    if ExternalDominionBlockerKind.GATEWAY_CONNECTION_SURFACE in blockers:
        return ExternalDominionCandidateKind.GATEWAY_CONNECTION_CANDIDATE
    if ExternalDominionBlockerKind.REGISTRY_MUTATION_SURFACE in blockers:
        return ExternalDominionCandidateKind.REGISTRY_MUTATION_CANDIDATE
    if ExternalDominionBlockerKind.MEMORY_MUTATION_SURFACE in blockers:
        return ExternalDominionCandidateKind.MEMORY_MUTATION_CANDIDATE
    return ExternalDominionCandidateKind.EXTERNAL_RUNTIME_CONTROL_CANDIDATE


def infer_external_dominion_control_surfaces_from_risk_surfaces(
    risk_surfaces: list[ExternalDominionRiskSurfaceKind | str] | list[str],
) -> list[ExternalDominionControlSurfaceKind]:
    mapped: list[ExternalDominionControlSurfaceKind] = []
    surface_map = {
        "external_side_effect": ExternalDominionControlSurfaceKind.EXTERNAL_RUNTIME,
        "private_data_exposure": ExternalDominionControlSurfaceKind.PRIVATE_DATA,
        "credential_exposure": ExternalDominionControlSurfaceKind.CREDENTIAL,
        "network_side_effect": ExternalDominionControlSurfaceKind.NETWORK,
        "command_execution": ExternalDominionControlSurfaceKind.COMMAND,
        "provider_invocation": ExternalDominionControlSurfaceKind.PROVIDER,
        "browser_automation": ExternalDominionControlSurfaceKind.BROWSER,
        "rpa_control": ExternalDominionControlSurfaceKind.RPA,
        "gateway_control": ExternalDominionControlSurfaceKind.GATEWAY,
        "channel_access": ExternalDominionControlSurfaceKind.CHANNEL,
        "message_send": ExternalDominionControlSurfaceKind.MESSAGE,
        "webhook_call": ExternalDominionControlSurfaceKind.WEBHOOK,
        "plugin_loading": ExternalDominionControlSurfaceKind.PLUGIN,
        "external_plugin_loading": ExternalDominionControlSurfaceKind.EXTERNAL_PLUGIN,
        "tool_invocation": ExternalDominionControlSurfaceKind.TOOL,
        "tool_registration": ExternalDominionControlSurfaceKind.TOOL,
        "mission_execution": ExternalDominionControlSurfaceKind.MISSION,
        "mission_installation": ExternalDominionControlSurfaceKind.MISSION,
        "delegation_execution": ExternalDominionControlSurfaceKind.DELEGATION,
        "memory_contamination": ExternalDominionControlSurfaceKind.MEMORY,
        "raw_output_persistence": ExternalDominionControlSurfaceKind.RAW_OUTPUT,
        "registry_mutation": ExternalDominionControlSurfaceKind.REGISTRY,
        "ocel_schema_drift": ExternalDominionControlSurfaceKind.OCEL_TRACE,
        "ocel_emission": ExternalDominionControlSurfaceKind.OCEL_TRACE,
        "approval_bypass": ExternalDominionControlSurfaceKind.APPROVAL,
        "audit_gap": ExternalDominionControlSurfaceKind.AUDIT,
    }
    for surface in risk_surfaces:
        value = surface.value if isinstance(surface, StrEnum) else str(surface)
        mapped_surface = surface_map.get(value, ExternalDominionControlSurfaceKind.UNKNOWN)
        if mapped_surface not in mapped:
            mapped.append(mapped_surface)
    return mapped


def infer_external_dominion_route_from_source(source_or_classification: Any) -> ExternalDominionEmissionRoute:
    route_value = getattr(source_or_classification, "route", None)
    if route_value is None:
        return ExternalDominionEmissionRoute.UNKNOWN
    route_text = route_value.value if isinstance(route_value, StrEnum) else str(route_value)
    if route_text in {"send_to_v0328_dominion_emitter", "send_to_v0328_dominion_candidate_emitter"}:
        return ExternalDominionEmissionRoute.EMIT_FOR_V0329_CONSOLIDATION
    if route_text in {"require_future_gate", "future_track"}:
        return ExternalDominionEmissionRoute.REQUIRE_FUTURE_GATE
    if route_text == "require_review":
        return ExternalDominionEmissionRoute.REQUIRE_REVIEW
    if route_text == "block":
        return ExternalDominionEmissionRoute.BLOCK
    if route_text == "reject":
        return ExternalDominionEmissionRoute.REJECT
    if route_text == "defer":
        return ExternalDominionEmissionRoute.DEFER
    if route_text == "no_op":
        return ExternalDominionEmissionRoute.NO_OP
    return ExternalDominionEmissionRoute.UNKNOWN


def infer_external_dominion_blockers_from_risk_surfaces(
    risk_surfaces: list[ExternalDominionRiskSurfaceKind | str] | list[str],
) -> list[ExternalDominionBlockerKind]:
    blockers: list[ExternalDominionBlockerKind] = []
    mapping = {
        "external_side_effect": ExternalDominionBlockerKind.EXTERNAL_CONTROL_SURFACE,
        "private_data_exposure": ExternalDominionBlockerKind.PRIVATE_DATA_SURFACE,
        "credential_exposure": ExternalDominionBlockerKind.CREDENTIAL_ACCESS_SURFACE,
        "network_side_effect": ExternalDominionBlockerKind.NETWORK_ACCESS_SURFACE,
        "command_execution": ExternalDominionBlockerKind.COMMAND_EXECUTION_SURFACE,
        "provider_invocation": ExternalDominionBlockerKind.PROVIDER_INVOCATION_SURFACE,
        "browser_automation": ExternalDominionBlockerKind.UNSAFE_RUNTIME_SURFACE,
        "rpa_control": ExternalDominionBlockerKind.UNSAFE_RUNTIME_SURFACE,
        "gateway_control": ExternalDominionBlockerKind.GATEWAY_CONNECTION_SURFACE,
        "channel_access": ExternalDominionBlockerKind.GATEWAY_CONNECTION_SURFACE,
        "message_send": ExternalDominionBlockerKind.GATEWAY_CONNECTION_SURFACE,
        "webhook_call": ExternalDominionBlockerKind.NETWORK_ACCESS_SURFACE,
        "plugin_loading": ExternalDominionBlockerKind.PLUGIN_LOADING_SURFACE,
        "external_plugin_loading": ExternalDominionBlockerKind.PLUGIN_LOADING_SURFACE,
        "tool_invocation": ExternalDominionBlockerKind.TOOL_INVOCATION_SURFACE,
        "tool_registration": ExternalDominionBlockerKind.REGISTRY_MUTATION_SURFACE,
        "mission_execution": ExternalDominionBlockerKind.MISSION_EXECUTION_SURFACE,
        "mission_installation": ExternalDominionBlockerKind.MISSION_EXECUTION_SURFACE,
        "delegation_execution": ExternalDominionBlockerKind.UNSAFE_RUNTIME_SURFACE,
        "memory_contamination": ExternalDominionBlockerKind.MEMORY_MUTATION_SURFACE,
        "raw_output_persistence": ExternalDominionBlockerKind.PRIVATE_DATA_SURFACE,
        "registry_mutation": ExternalDominionBlockerKind.REGISTRY_MUTATION_SURFACE,
        "ocel_emission": ExternalDominionBlockerKind.UNSAFE_RUNTIME_SURFACE,
        "approval_bypass": ExternalDominionBlockerKind.AUTHORITY_GRANT_REQUIRED,
        "audit_gap": ExternalDominionBlockerKind.INCOMPATIBLE_WITH_DOMINION_GOVERNANCE,
    }
    for surface in risk_surfaces:
        value = surface.value if isinstance(surface, StrEnum) else str(surface)
        blocker = mapping.get(value, ExternalDominionBlockerKind.UNKNOWN)
        if blocker not in blockers:
            blockers.append(blocker)
    return blockers


def dominion_candidate_preserves_no_external_control(candidate: ExternalHarnessDominionCandidate) -> bool:
    return (
        candidate.ready_for_active_dominion_target_creation is False
        and candidate.ready_for_dominion_decision_creation is False
        and candidate.ready_for_external_control is False
        and candidate.ready_for_authority_grant is False
        and candidate.ready_for_execution is False
        and candidate.active_dominion_target is False
        and candidate.dominion_decision is False
        and candidate.authority_grant is False
    )


def dominion_target_candidate_is_not_active_target(candidate: EmittedInternalDominionTargetCandidate) -> bool:
    return (
        candidate.ready_for_active_dominion_target_creation is False
        and candidate.ready_for_external_control is False
        and candidate.ready_for_authority_grant is False
        and candidate.ready_for_execution is False
        and candidate.active_internal_dominion_target is False
        and candidate.external_control is False
        and candidate.d4_d9_grant is False
    )


def dominion_candidate_set_is_not_runtime_registry(candidate_set: ExternalHarnessDominionCandidateSet) -> bool:
    return (
        candidate_set.ready_for_active_dominion_target_creation is False
        and candidate_set.ready_for_dominion_decision_creation is False
        and candidate_set.ready_for_external_control is False
        and candidate_set.ready_for_authority_grant is False
        and candidate_set.ready_for_execution is False
        and candidate_set.runtime_registry is False
    )


def v0328_readiness_report_is_not_runtime_ready(report: V0328ReadinessReport) -> bool:
    return (
        report.ready_for_execution is False
        and report.ready_for_external_control is False
        and report.ready_for_authority_grant is False
        and report.ready_for_active_dominion_target_creation is False
        and report.ready_for_dominion_decision_creation is False
        and report.ready_for_dominion_runtime is False
        and report.ready_for_provider_invocation is False
        and report.ready_for_gateway_connection is False
        and report.ready_for_network_access is False
        and report.ready_for_credential_access is False
        and report.ready_for_command_execution is False
        and report.ready_for_browser_runtime_control is False
        and report.ready_for_rpa_runtime_control is False
        and report.ready_for_packet_send is False
        and report.ready_for_registry_mutation is False
        and report.ready_for_memory_mutation is False
    )

