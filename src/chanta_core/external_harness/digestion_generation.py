from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .manifest_extraction import ExternalManifestCandidateBase, ExternalManifestCandidateKind
from .profiles import _metadata_flag_true, _require_non_blank, _validate_object_list, _validate_string_list
from .risk_classification import (
    ExternalCapabilityRiskClass,
    ExternalCapabilityRiskClassification,
    ExternalCapabilityRiskRoute,
)


V0326_VERSION = "v0.32.6"
V0326_RELEASE_NAME = "v0.32.6 Digestion Candidate Generator"

DEFAULT_DIGESTION_PROHIBITED_RUNTIME_ACTIONS = [
    "runtime execution",
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
    "internal candidate creation",
    "internal candidate emission",
    "internalization",
    "registry mutation",
    "memory mutation",
    "dominion target creation",
    "dominion decision creation",
    "OCEL emission",
]


class ExternalDigestionCandidateKind(StrEnum):
    SKILL_PATTERN_CANDIDATE = "skill_pattern_candidate"
    TOOL_CONTRACT_PATTERN_CANDIDATE = "tool_contract_pattern_candidate"
    PLUGIN_PATTERN_CANDIDATE = "plugin_pattern_candidate"
    MISSION_PATTERN_CANDIDATE = "mission_pattern_candidate"
    GATEWAY_CONTRACT_PATTERN_CANDIDATE = "gateway_contract_pattern_candidate"
    PROVIDER_ADAPTER_PATTERN_CANDIDATE = "provider_adapter_pattern_candidate"
    PROFILE_PATTERN_CANDIDATE = "profile_pattern_candidate"
    MEMORY_SCHEMA_PATTERN_CANDIDATE = "memory_schema_pattern_candidate"
    APPROVAL_POLICY_PATTERN_CANDIDATE = "approval_policy_pattern_candidate"
    AUDIT_POLICY_PATTERN_CANDIDATE = "audit_policy_pattern_candidate"
    RESULT_ENVELOPE_PATTERN_CANDIDATE = "result_envelope_pattern_candidate"
    OCEL_TRACE_PATTERN_CANDIDATE = "ocel_trace_pattern_candidate"
    PROMPT_PATTERN_CANDIDATE = "prompt_pattern_candidate"
    DELEGATION_PACKET_PATTERN_CANDIDATE = "delegation_packet_pattern_candidate"
    UNKNOWN = "unknown"


class ExternalDigestionPatternKind(StrEnum):
    CONTRACT_PATTERN = "contract_pattern"
    SCHEMA_PATTERN = "schema_pattern"
    MANIFEST_PATTERN = "manifest_pattern"
    WORKFLOW_PATTERN = "workflow_pattern"
    APPROVAL_BOUNDARY_PATTERN = "approval_boundary_pattern"
    AUDIT_BOUNDARY_PATTERN = "audit_boundary_pattern"
    RESULT_BOUNDARY_PATTERN = "result_boundary_pattern"
    OCEL_TRACE_PATTERN = "ocel_trace_pattern"
    PROMPT_PATTERN = "prompt_pattern"
    ADAPTER_PATTERN = "adapter_pattern"
    ROUTING_PATTERN = "routing_pattern"
    NO_OP_PATTERN = "no_op_pattern"
    FUTURE_TRACK_PATTERN = "future_track_pattern"
    UNKNOWN = "unknown"


class ExternalDigestionRoute(StrEnum):
    SEND_TO_V0327_INTERNAL_CANDIDATE_EMITTER = "send_to_v0327_internal_candidate_emitter"
    SEND_TO_V0328_DOMINION_CANDIDATE_EMITTER = "send_to_v0328_dominion_candidate_emitter"
    REQUIRE_REVIEW = "require_review"
    DEFER = "defer"
    REJECT = "reject"
    BLOCK = "block"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class ExternalDigestibilityPosture(StrEnum):
    UNKNOWN = "unknown"
    NOT_DIGESTIBLE = "not_digestible"
    WEAK = "weak"
    PARTIAL = "partial"
    DIGESTIBLE = "digestible"
    DIGESTIBLE_WITH_GAPS = "digestible_with_gaps"
    REQUIRES_REVIEW = "requires_review"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class ExternalDigestionEvidenceQuality(StrEnum):
    UNKNOWN = "unknown"
    NONE = "none"
    WEAK = "weak"
    PARTIAL = "partial"
    SUFFICIENT_FOR_DIGESTION_CANDIDATE = "sufficient_for_digestion_candidate"
    SUFFICIENT_FOR_V0327_REVIEW = "sufficient_for_v0327_review"
    CONFLICTING = "conflicting"
    BLOCKED = "blocked"


class ExternalDigestionBlockerKind(StrEnum):
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    CONFLICTING_EVIDENCE = "conflicting_evidence"
    MISSING_MANIFEST_CANDIDATE = "missing_manifest_candidate"
    MISSING_RISK_CLASSIFICATION = "missing_risk_classification"
    BLOCKED_RISK_ROUTE = "blocked_risk_route"
    DOMINION_REQUIRED_ROUTE = "dominion_required_route"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNSAFE_RUNTIME_SURFACE = "unsafe_runtime_surface"
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
    INCOMPATIBLE_WITH_INTERNAL_TRIAD = "incompatible_with_internal_triad"
    UNKNOWN = "unknown"


class ExternalDigestionSourceKind(StrEnum):
    EXTERNAL_CAPABILITY_RISK_CLASSIFICATION = "external_capability_risk_classification"
    EXTERNAL_CAPABILITY_RISK_MAP = "external_capability_risk_map"
    EXTERNAL_CAPABILITY_BOUNDARY_MAP = "external_capability_boundary_map"
    EXTERNAL_MANIFEST_CANDIDATE = "external_manifest_candidate"
    EXTERNAL_MANIFEST_CANDIDATE_SET = "external_manifest_candidate_set"
    EXTERNAL_MANIFEST_EXTRACTION_REPORT = "external_manifest_extraction_report"
    OPENCODE_OBSERVATION_OUTPUT = "opencode_observation_output"
    OPENCLAW_OBSERVATION_OUTPUT = "openclaw_observation_output"
    HERMES_OBSERVATION_OUTPUT = "hermes_observation_output"
    REFERENCE_FILE_INVENTORY = "reference_file_inventory"
    REFERENCE_CORPUS_SNAPSHOT = "reference_corpus_snapshot"
    MANUAL_DIGESTION_REVIEW = "manual_digestion_review"
    UNKNOWN = "unknown"


def _validate_version_includes_v0326(version: str) -> None:
    _require_non_blank("version", version)
    if V0326_VERSION not in version:
        raise ValueError("version must include v0.32.6")


def _validate_kind_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.32.6")


def _validate_default_prohibitions(name: str, values: list[str]) -> None:
    _validate_string_list(name, values)
    missing = set(DEFAULT_DIGESTION_PROHIBITED_RUNTIME_ACTIONS) - set(values)
    if missing:
        raise ValueError(f"{name} missing v0.32.6 prohibitions: {sorted(missing)}")


@dataclass(frozen=True)
class ExternalDigestionSourceRef:
    source_ref_id: str
    source_kind: ExternalDigestionSourceKind | str
    source_id: str
    manifest_candidate_id: str | None = None
    risk_classification_id: str | None = None
    harness_kind: str | None = None
    reference_entry_ids: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        ExternalDigestionSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _validate_string_list("reference_entry_ids", self.reference_entry_ids)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"source_fetch", "execution", "live_scan"}):
            raise ValueError("ExternalDigestionSourceRef is not source fetch or execution")

    @property
    def source_fetch(self) -> bool:
        return False

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDigestionPatternSignal:
    pattern_signal_id: str
    source_ref_ids: list[str]
    candidate_kind: ExternalDigestionCandidateKind | str
    pattern_kind: ExternalDigestionPatternKind | str
    title: str
    summary: str
    extracted_pattern_summary: str
    suggested_internal_artifact_kind: str | None = None
    evidence_quality: ExternalDigestionEvidenceQuality | str = ExternalDigestionEvidenceQuality.UNKNOWN
    evidence_refs: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("pattern_signal_id", self.pattern_signal_id)
        _validate_string_list("source_ref_ids", self.source_ref_ids)
        ExternalDigestionCandidateKind(self.candidate_kind)
        ExternalDigestionPatternKind(self.pattern_kind)
        _require_non_blank("title", self.title)
        _require_non_blank("summary", self.summary)
        _require_non_blank("extracted_pattern_summary", self.extracted_pattern_summary)
        ExternalDigestionEvidenceQuality(self.evidence_quality)
        for name in ("evidence_refs", "assumptions", "limitations"):
            _validate_string_list(name, getattr(self, name))
        if _metadata_flag_true(self.metadata, {"generated_code", "artifact_creation"}):
            raise ValueError("ExternalDigestionPatternSignal is not generated code")

    @property
    def generated_code(self) -> bool:
        return False

    @property
    def suggested_artifact_creation(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDigestibilityAssessment:
    assessment_id: str
    pattern_signal_ids: list[str] = field(default_factory=list)
    target_manifest_candidate_id: str | None = None
    target_risk_classification_id: str | None = None
    digestibility_posture: ExternalDigestibilityPosture | str = ExternalDigestibilityPosture.UNKNOWN
    route: ExternalDigestionRoute | str = ExternalDigestionRoute.UNKNOWN
    summary: str = "Static digestibility assessment only."
    evidence_quality: ExternalDigestionEvidenceQuality | str = ExternalDigestionEvidenceQuality.UNKNOWN
    blocker_ids: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    ready_for_v0327_internal_candidate_emitter: bool = False
    ready_for_v0328_dominion_candidate_emitter: bool = False
    ready_for_internal_candidate_creation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("assessment_id", self.assessment_id)
        posture = ExternalDigestibilityPosture(self.digestibility_posture)
        route = ExternalDigestionRoute(self.route)
        _require_non_blank("summary", self.summary)
        ExternalDigestionEvidenceQuality(self.evidence_quality)
        for name in ("pattern_signal_ids", "blocker_ids", "gaps", "evidence_refs"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, ("ready_for_internal_candidate_creation", "ready_for_execution"))
        if self.ready_for_v0327_internal_candidate_emitter:
            if posture not in {ExternalDigestibilityPosture.DIGESTIBLE, ExternalDigestibilityPosture.DIGESTIBLE_WITH_GAPS}:
                raise ValueError("v0.32.7 handoff requires digestible posture")
            if route != ExternalDigestionRoute.SEND_TO_V0327_INTERNAL_CANDIDATE_EMITTER:
                raise ValueError("v0.32.7 handoff requires send_to_v0327 route")
            if self.blocker_ids:
                raise ValueError("v0.32.7 handoff is not allowed with blockers")
        if self.ready_for_v0328_dominion_candidate_emitter:
            allowed = route in {
                ExternalDigestionRoute.SEND_TO_V0328_DOMINION_CANDIDATE_EMITTER,
                ExternalDigestionRoute.REQUIRE_REVIEW,
                ExternalDigestionRoute.DEFER,
                ExternalDigestionRoute.BLOCK,
                ExternalDigestionRoute.FUTURE_TRACK,
            }
            if not allowed:
                raise ValueError("v0.32.8 handoff requires dominion or conservative route")
        if _metadata_flag_true(self.metadata, {"approval", "internalization"}):
            raise ValueError("ExternalDigestibilityAssessment is not approval or internalization")

    @property
    def approval(self) -> bool:
        return False

    @property
    def internalization(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDigestionBlocker:
    blocker_id: str
    blocker_kind: ExternalDigestionBlockerKind | str
    source_ref_ids: list[str] = field(default_factory=list)
    target_manifest_candidate_id: str | None = None
    target_risk_classification_id: str | None = None
    reason: str = "Static digestion blocker."
    blocks_v0327: bool = True
    routes_to_v0328: bool = False
    routes_to_future_gate: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("blocker_id", self.blocker_id)
        ExternalDigestionBlockerKind(self.blocker_kind)
        _validate_string_list("source_ref_ids", self.source_ref_ids)
        _require_non_blank("reason", self.reason)
        for name in ("blocks_v0327", "routes_to_v0328", "routes_to_future_gate"):
            if not isinstance(getattr(self, name), bool):
                raise TypeError(f"{name} must be bool")
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"remediation", "execution"}):
            raise ValueError("ExternalDigestionBlocker does not execute remediation")

    @property
    def remediation_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalToInternalPatternMap:
    pattern_map_id: str
    source_pattern_signal_ids: list[str] = field(default_factory=list)
    source_manifest_candidate_ids: list[str] = field(default_factory=list)
    source_risk_classification_ids: list[str] = field(default_factory=list)
    suggested_internal_candidate_kind: str = "external_pattern_candidate"
    suggested_internal_contract_summary: str = "Static suggested contract summary only."
    suggested_input_contract_summary: str = "Static input contract summary only."
    suggested_output_contract_summary: str = "Static output contract summary only."
    suggested_validation_summary: str = "Static validation summary only."
    suggested_test_summary: str = "Static test summary only."
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_DIGESTION_PROHIBITED_RUNTIME_ACTIONS))
    evidence_refs: list[str] = field(default_factory=list)
    ready_for_internal_candidate_emission: bool = False
    ready_for_internalization: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("pattern_map_id", self.pattern_map_id)
        for name in ("source_pattern_signal_ids", "source_manifest_candidate_ids", "source_risk_classification_ids", "evidence_refs"):
            _validate_string_list(name, getattr(self, name))
        for name in (
            "suggested_internal_candidate_kind",
            "suggested_internal_contract_summary",
            "suggested_input_contract_summary",
            "suggested_output_contract_summary",
            "suggested_validation_summary",
            "suggested_test_summary",
        ):
            _require_non_blank(name, getattr(self, name))
        _validate_default_prohibitions("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_false(self, ("ready_for_internal_candidate_emission", "ready_for_internalization", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"internal_skill_candidate", "internalization_plan", "artifact_creation"}):
            raise ValueError("ExternalToInternalPatternMap is not an internal artifact or internalization plan")

    @property
    def internal_skill_candidate(self) -> bool:
        return False

    @property
    def internalization_plan(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalHarnessDigestionCandidate:
    digestion_candidate_id: str
    candidate_kind: ExternalDigestionCandidateKind | str
    source_refs: list[ExternalDigestionSourceRef]
    pattern_signals: list[ExternalDigestionPatternSignal]
    digestibility_assessment: ExternalDigestibilityAssessment
    external_to_internal_pattern_map: ExternalToInternalPatternMap | None = None
    title: str = "External harness digestion candidate"
    summary: str = "Design-stage external digestion candidate only."
    source_harness_kinds: list[str] = field(default_factory=list)
    source_manifest_candidate_ids: list[str] = field(default_factory=list)
    source_risk_classification_ids: list[str] = field(default_factory=list)
    evidence_quality: ExternalDigestionEvidenceQuality | str = ExternalDigestionEvidenceQuality.UNKNOWN
    evidence_refs: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    blockers: list[ExternalDigestionBlocker] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    status: ExternalDigestibilityPosture | str = ExternalDigestibilityPosture.UNKNOWN
    route: ExternalDigestionRoute | str = ExternalDigestionRoute.UNKNOWN
    ready_for_v0327_internal_candidate_emitter: bool = False
    ready_for_v0328_dominion_candidate_emitter: bool = False
    ready_for_internal_candidate_creation: bool = False
    ready_for_internalization: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("digestion_candidate_id", self.digestion_candidate_id)
        ExternalDigestionCandidateKind(self.candidate_kind)
        _validate_object_list("source_refs", self.source_refs, ExternalDigestionSourceRef)
        _validate_object_list("pattern_signals", self.pattern_signals, ExternalDigestionPatternSignal)
        if not isinstance(self.digestibility_assessment, ExternalDigestibilityAssessment):
            raise TypeError("digestibility_assessment must be ExternalDigestibilityAssessment")
        if self.external_to_internal_pattern_map is not None and not isinstance(self.external_to_internal_pattern_map, ExternalToInternalPatternMap):
            raise TypeError("external_to_internal_pattern_map must be ExternalToInternalPatternMap or None")
        _require_non_blank("title", self.title)
        _require_non_blank("summary", self.summary)
        for name in (
            "source_harness_kinds",
            "source_manifest_candidate_ids",
            "source_risk_classification_ids",
            "evidence_refs",
            "assumptions",
            "limitations",
            "gaps",
        ):
            _validate_string_list(name, getattr(self, name))
        ExternalDigestionEvidenceQuality(self.evidence_quality)
        _validate_object_list("blockers", self.blockers, ExternalDigestionBlocker)
        ExternalDigestibilityPosture(self.status)
        ExternalDigestionRoute(self.route)
        _validate_false(self, ("ready_for_internal_candidate_creation", "ready_for_internalization", "ready_for_execution"))
        if self.ready_for_v0327_internal_candidate_emitter:
            if not self.digestibility_assessment.ready_for_v0327_internal_candidate_emitter:
                raise ValueError("candidate v0.32.7 handoff requires assessment handoff")
            if any(blocker.blocks_v0327 for blocker in self.blockers):
                raise ValueError("candidate v0.32.7 handoff is not allowed with blocking blockers")
        if _metadata_flag_true(self.metadata, {"internal_skill_candidate", "active_internalization"}):
            raise ValueError("ExternalHarnessDigestionCandidate is not internal candidate or active internalization")

    @property
    def internal_skill_candidate(self) -> bool:
        return False

    @property
    def active_internalization(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDigestionCandidateSet:
    candidate_set_id: str
    version: str = V0326_VERSION
    source_classification_report_id: str | None = None
    candidates: list[ExternalHarnessDigestionCandidate] = field(default_factory=list)
    accepted_candidate_ids: list[str] = field(default_factory=list)
    deferred_candidate_ids: list[str] = field(default_factory=list)
    rejected_candidate_ids: list[str] = field(default_factory=list)
    blocked_candidate_ids: list[str] = field(default_factory=list)
    dominion_required_candidate_ids: list[str] = field(default_factory=list)
    future_track_candidate_ids: list[str] = field(default_factory=list)
    no_op_candidate_ids: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    ready_for_v0327_internal_candidate_emitter: bool = False
    ready_for_v0328_dominion_candidate_emitter: bool = False
    ready_for_internal_candidate_creation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("candidate_set_id", self.candidate_set_id)
        _validate_version_includes_v0326(self.version)
        _validate_object_list("candidates", self.candidates, ExternalHarnessDigestionCandidate)
        for name in (
            "accepted_candidate_ids",
            "deferred_candidate_ids",
            "rejected_candidate_ids",
            "blocked_candidate_ids",
            "dominion_required_candidate_ids",
            "future_track_candidate_ids",
            "no_op_candidate_ids",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, ("ready_for_internal_candidate_creation", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"registry", "internal_candidate_emission"}):
            raise ValueError("ExternalDigestionCandidateSet is not registry and does not emit internal candidates")

    @property
    def registry(self) -> bool:
        return False

    @property
    def internal_candidate_emission(self) -> bool:
        return False


@dataclass(frozen=True)
class HarnessPatternDigestibilityReport:
    digestibility_report_id: str
    version: str
    candidate_set_id: str | None = None
    pattern_signal_count: int = 0
    candidate_count: int = 0
    digestible_count: int = 0
    blocked_count: int = 0
    dominion_required_count: int = 0
    future_track_count: int = 0
    no_op_count: int = 0
    summary: str = "Harness pattern digestibility report for static candidates."
    key_patterns: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0327_internal_candidate_emitter: bool = False
    ready_for_v0328_dominion_candidate_emitter: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("digestibility_report_id", self.digestibility_report_id)
        _validate_version_includes_v0326(self.version)
        for name in (
            "pattern_signal_count",
            "candidate_count",
            "digestible_count",
            "blocked_count",
            "dominion_required_count",
            "future_track_count",
            "no_op_count",
        ):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        _require_non_blank("summary", self.summary)
        for name in ("key_patterns", "blockers", "gaps", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, ("ready_for_execution",))
        if _metadata_flag_true(self.metadata, {"runtime_certification", "internal_candidate_emission"}):
            raise ValueError("HarnessPatternDigestibilityReport is not runtime certification or internal candidate emission")

    @property
    def runtime_certification(self) -> bool:
        return False

    @property
    def internal_candidate_emission(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDigestionCandidateGenerationInput:
    generation_input_id: str
    source_version: str = V0326_VERSION
    risk_classification_report_ids: list[str] = field(default_factory=list)
    risk_map_ids: list[str] = field(default_factory=list)
    boundary_map_ids: list[str] = field(default_factory=list)
    manifest_candidate_set_ids: list[str] = field(default_factory=list)
    opencode_output_ids: list[str] = field(default_factory=list)
    openclaw_output_ids: list[str] = field(default_factory=list)
    hermes_output_ids: list[str] = field(default_factory=list)
    reference_inventory_ids: list[str] = field(default_factory=list)
    reference_corpus_snapshot_ids: list[str] = field(default_factory=list)
    source_refs: list[ExternalDigestionSourceRef] = field(default_factory=list)
    requested_candidate_kinds: list[ExternalDigestionCandidateKind | str] = field(default_factory=list)
    task_summary: str = "Generate external digestion candidates from static contract metadata."
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_DIGESTION_PROHIBITED_RUNTIME_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("generation_input_id", self.generation_input_id)
        _require_non_blank("source_version", self.source_version)
        for name in (
            "risk_classification_report_ids",
            "risk_map_ids",
            "boundary_map_ids",
            "manifest_candidate_set_ids",
            "opencode_output_ids",
            "openclaw_output_ids",
            "hermes_output_ids",
            "reference_inventory_ids",
            "reference_corpus_snapshot_ids",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_object_list("source_refs", self.source_refs, ExternalDigestionSourceRef)
        _validate_kind_list("requested_candidate_kinds", self.requested_candidate_kinds, ExternalDigestionCandidateKind)
        _require_non_blank("task_summary", self.task_summary)
        _validate_default_prohibitions("prohibited_runtime_actions", self.prohibited_runtime_actions)
        if _metadata_flag_true(self.metadata, {"execution_request", "internalization_request"}):
            raise ValueError("ExternalDigestionCandidateGenerationInput is not execution request")

    @property
    def execution_request(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDigestionCandidateGenerationFinding:
    finding_id: str
    generation_input_id: str
    source_ref_ids: list[str]
    target_manifest_candidate_id: str | None
    target_risk_classification_id: str | None
    candidate_kind: ExternalDigestionCandidateKind | str
    route: ExternalDigestionRoute | str
    digestibility_posture: ExternalDigestibilityPosture | str
    summary: str
    pattern_signal_ids: list[str] = field(default_factory=list)
    blocker_ids: list[str] = field(default_factory=list)
    evidence_quality: ExternalDigestionEvidenceQuality | str = ExternalDigestionEvidenceQuality.UNKNOWN
    evidence_refs: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("generation_input_id", self.generation_input_id)
        _validate_string_list("source_ref_ids", self.source_ref_ids)
        ExternalDigestionCandidateKind(self.candidate_kind)
        ExternalDigestionRoute(self.route)
        ExternalDigestibilityPosture(self.digestibility_posture)
        _require_non_blank("summary", self.summary)
        for name in ("pattern_signal_ids", "blocker_ids", "evidence_refs", "assumptions", "limitations"):
            _validate_string_list(name, getattr(self, name))
        ExternalDigestionEvidenceQuality(self.evidence_quality)
        if _metadata_flag_true(self.metadata, {"internal_skill_candidate", "certification"}):
            raise ValueError("ExternalDigestionCandidateGenerationFinding is not internal candidate or certification")

    @property
    def internal_skill_candidate(self) -> bool:
        return False

    @property
    def certification(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDigestionCandidateGenerationReport:
    report_id: str
    version: str
    generation_input_id: str
    candidate_set_id: str | None = None
    digestibility_report_id: str | None = None
    findings: list[ExternalDigestionCandidateGenerationFinding] = field(default_factory=list)
    summary: str = "External digestion candidate generation report."
    generated_candidate_count: int = 0
    blocked_items: list[str] = field(default_factory=list)
    deferred_items: list[str] = field(default_factory=list)
    dominion_required_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0327_internal_candidate_emitter: bool = False
    ready_for_v0328_dominion_candidate_emitter: bool = False
    ready_for_internal_candidate_creation: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0326(self.version)
        _require_non_blank("generation_input_id", self.generation_input_id)
        _validate_object_list("findings", self.findings, ExternalDigestionCandidateGenerationFinding)
        _require_non_blank("summary", self.summary)
        if self.generated_candidate_count < 0:
            raise ValueError("generated_candidate_count must be >= 0")
        for name in (
            "blocked_items",
            "deferred_items",
            "dominion_required_items",
            "future_track_items",
            "gaps",
            "evidence_refs",
            "withdrawal_conditions",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, ("ready_for_internal_candidate_creation", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"internal_candidate_emission", "runtime_generation"}):
            raise ValueError("ExternalDigestionCandidateGenerationReport is not internal candidate emission or runtime generation")

    @property
    def internal_candidate_emission(self) -> bool:
        return False

    @property
    def runtime_generation(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDigestionCandidateRunPreview:
    run_preview_id: str
    generation_input_id: str | None = None
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
    no_internal_candidate_creation_guarantee: bool = True
    no_internalization_guarantee: bool = True
    no_dominion_target_creation_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must always be True in v0.32.6")
        if _metadata_flag_true(self.metadata, {"execution"}):
            raise ValueError("ExternalDigestionCandidateRunPreview is not execution")

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDigestionCandidateNoRuntimeGuarantee:
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
    no_internal_candidate_creation: bool = True
    no_internalization: bool = True
    no_dominion_target_creation: bool = True
    no_dominion_decision_creation: bool = True
    no_registry_mutation: bool = True
    no_memory_mutation: bool = True
    no_ocel_emission: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version_includes_v0326(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must always be True in v0.32.6")
        _validate_string_list("evidence_refs", self.evidence_refs)


@dataclass(frozen=True)
class V0326ReadinessReport:
    report_id: str
    version: str
    generation_report_id: str | None = None
    candidate_set_id: str | None = None
    digestibility_report_id: str | None = None
    summary: str = "v0.32.6 readiness is limited to design-stage handoff."
    ready_for_v0327_internal_skill_candidate_emitter: bool = False
    ready_for_v0328_external_dominion_candidate_emitter: bool = False
    ready_for_execution: bool = False
    ready_for_internal_candidate_emission: bool = False
    ready_for_internal_skill_candidate_creation: bool = False
    ready_for_internal_tool_candidate_creation: bool = False
    ready_for_internalization: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_plugin_loading: bool = False
    ready_for_tool_registration: bool = False
    ready_for_tool_invocation: bool = False
    ready_for_mission_installation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_gateway_connection: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    dominion_required_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_DIGESTION_PROHIBITED_RUNTIME_ACTIONS))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0326(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(
            self,
            (
                "ready_for_execution",
                "ready_for_internal_candidate_emission",
                "ready_for_internal_skill_candidate_creation",
                "ready_for_internal_tool_candidate_creation",
                "ready_for_internalization",
                "ready_for_registry_mutation",
                "ready_for_memory_mutation",
                "ready_for_plugin_loading",
                "ready_for_tool_registration",
                "ready_for_tool_invocation",
                "ready_for_mission_installation",
                "ready_for_provider_invocation",
                "ready_for_gateway_connection",
                "ready_for_network_access",
                "ready_for_credential_access",
                "ready_for_command_execution",
            ),
        )
        for name in (
            "completed_items",
            "blocked_items",
            "dominion_required_items",
            "future_track_items",
            "evidence_refs",
            "withdrawal_conditions",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_default_prohibitions("prohibited_until_later_gate", self.prohibited_until_later_gate)
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "internalization", "internal_candidate_creation"}):
            raise ValueError("V0326ReadinessReport is not runtime enablement")


def build_external_digestion_source_ref(
    source_ref_id: str,
    source_kind: ExternalDigestionSourceKind | str,
    source_id: str,
    **kwargs: Any,
) -> ExternalDigestionSourceRef:
    return ExternalDigestionSourceRef(source_ref_id=source_ref_id, source_kind=source_kind, source_id=source_id, **kwargs)


def build_external_digestion_pattern_signal(
    pattern_signal_id: str,
    source_ref_ids: list[str],
    candidate_kind: ExternalDigestionCandidateKind | str,
    pattern_kind: ExternalDigestionPatternKind | str,
    title: str,
    summary: str,
    extracted_pattern_summary: str,
    **kwargs: Any,
) -> ExternalDigestionPatternSignal:
    return ExternalDigestionPatternSignal(
        pattern_signal_id=pattern_signal_id,
        source_ref_ids=list(source_ref_ids),
        candidate_kind=candidate_kind,
        pattern_kind=pattern_kind,
        title=title,
        summary=summary,
        extracted_pattern_summary=extracted_pattern_summary,
        **kwargs,
    )


def build_external_digestibility_assessment(assessment_id: str, **kwargs: Any) -> ExternalDigestibilityAssessment:
    return ExternalDigestibilityAssessment(assessment_id=assessment_id, **kwargs)


def build_external_digestion_blocker(
    blocker_id: str,
    blocker_kind: ExternalDigestionBlockerKind | str,
    **kwargs: Any,
) -> ExternalDigestionBlocker:
    return ExternalDigestionBlocker(blocker_id=blocker_id, blocker_kind=blocker_kind, **kwargs)


def build_external_to_internal_pattern_map(pattern_map_id: str, **kwargs: Any) -> ExternalToInternalPatternMap:
    return ExternalToInternalPatternMap(pattern_map_id=pattern_map_id, **kwargs)


def build_external_harness_digestion_candidate(
    digestion_candidate_id: str,
    candidate_kind: ExternalDigestionCandidateKind | str,
    source_refs: list[ExternalDigestionSourceRef],
    pattern_signals: list[ExternalDigestionPatternSignal],
    digestibility_assessment: ExternalDigestibilityAssessment,
    **kwargs: Any,
) -> ExternalHarnessDigestionCandidate:
    return ExternalHarnessDigestionCandidate(
        digestion_candidate_id=digestion_candidate_id,
        candidate_kind=candidate_kind,
        source_refs=list(source_refs),
        pattern_signals=list(pattern_signals),
        digestibility_assessment=digestibility_assessment,
        **kwargs,
    )


def build_external_digestion_candidate_set(candidate_set_id: str, **kwargs: Any) -> ExternalDigestionCandidateSet:
    return ExternalDigestionCandidateSet(candidate_set_id=candidate_set_id, version=V0326_VERSION, **kwargs)


def build_harness_pattern_digestibility_report(
    digestibility_report_id: str,
    **kwargs: Any,
) -> HarnessPatternDigestibilityReport:
    return HarnessPatternDigestibilityReport(digestibility_report_id=digestibility_report_id, version=V0326_VERSION, **kwargs)


def build_external_digestion_candidate_generation_input(
    generation_input_id: str,
    **kwargs: Any,
) -> ExternalDigestionCandidateGenerationInput:
    return ExternalDigestionCandidateGenerationInput(generation_input_id=generation_input_id, **kwargs)


def build_external_digestion_candidate_generation_finding(
    finding_id: str,
    generation_input_id: str,
    source_ref_ids: list[str],
    target_manifest_candidate_id: str | None,
    target_risk_classification_id: str | None,
    candidate_kind: ExternalDigestionCandidateKind | str,
    route: ExternalDigestionRoute | str,
    digestibility_posture: ExternalDigestibilityPosture | str,
    summary: str,
    **kwargs: Any,
) -> ExternalDigestionCandidateGenerationFinding:
    return ExternalDigestionCandidateGenerationFinding(
        finding_id=finding_id,
        generation_input_id=generation_input_id,
        source_ref_ids=list(source_ref_ids),
        target_manifest_candidate_id=target_manifest_candidate_id,
        target_risk_classification_id=target_risk_classification_id,
        candidate_kind=candidate_kind,
        route=route,
        digestibility_posture=digestibility_posture,
        summary=summary,
        **kwargs,
    )


def build_external_digestion_candidate_generation_report(
    report_id: str,
    generation_input_id: str,
    **kwargs: Any,
) -> ExternalDigestionCandidateGenerationReport:
    return ExternalDigestionCandidateGenerationReport(
        report_id=report_id,
        version=V0326_VERSION,
        generation_input_id=generation_input_id,
        **kwargs,
    )


def build_external_digestion_candidate_run_preview(
    run_preview_id: str = "external_digestion_candidate_run_preview:v0.32.6",
    **kwargs: Any,
) -> ExternalDigestionCandidateRunPreview:
    return ExternalDigestionCandidateRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_external_digestion_candidate_no_runtime_guarantee(
    guarantee_id: str = "external_digestion_candidate_no_runtime_guarantee:v0.32.6",
    evidence_refs: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ExternalDigestionCandidateNoRuntimeGuarantee:
    return ExternalDigestionCandidateNoRuntimeGuarantee(
        guarantee_id=guarantee_id,
        version=V0326_VERSION,
        evidence_refs=list(evidence_refs or []),
        metadata=dict(metadata or {}),
    )


def build_v0326_readiness_report(
    report_id: str = "v0326_readiness_report",
    generation_report_id: str | None = None,
    candidate_set_id: str | None = None,
    digestibility_report_id: str | None = None,
    **kwargs: Any,
) -> V0326ReadinessReport:
    return V0326ReadinessReport(
        report_id=report_id,
        version=V0326_VERSION,
        generation_report_id=generation_report_id,
        candidate_set_id=candidate_set_id,
        digestibility_report_id=digestibility_report_id,
        **kwargs,
    )


def infer_external_digestion_candidate_kind_from_manifest_candidate(
    candidate: ExternalManifestCandidateBase,
) -> ExternalDigestionCandidateKind:
    kind = ExternalManifestCandidateKind(candidate.candidate_kind)
    return {
        ExternalManifestCandidateKind.SKILL_MANIFEST: ExternalDigestionCandidateKind.SKILL_PATTERN_CANDIDATE,
        ExternalManifestCandidateKind.TOOL_MANIFEST: ExternalDigestionCandidateKind.TOOL_CONTRACT_PATTERN_CANDIDATE,
        ExternalManifestCandidateKind.PLUGIN_MANIFEST: ExternalDigestionCandidateKind.PLUGIN_PATTERN_CANDIDATE,
        ExternalManifestCandidateKind.EXTERNAL_PLUGIN_MANIFEST: ExternalDigestionCandidateKind.PLUGIN_PATTERN_CANDIDATE,
        ExternalManifestCandidateKind.MISSION_MANIFEST: ExternalDigestionCandidateKind.MISSION_PATTERN_CANDIDATE,
        ExternalManifestCandidateKind.GATEWAY_MANIFEST: ExternalDigestionCandidateKind.GATEWAY_CONTRACT_PATTERN_CANDIDATE,
        ExternalManifestCandidateKind.CHANNEL_MANIFEST: ExternalDigestionCandidateKind.GATEWAY_CONTRACT_PATTERN_CANDIDATE,
        ExternalManifestCandidateKind.PROVIDER_MANIFEST: ExternalDigestionCandidateKind.PROVIDER_ADAPTER_PATTERN_CANDIDATE,
        ExternalManifestCandidateKind.PROFILE_MANIFEST: ExternalDigestionCandidateKind.PROFILE_PATTERN_CANDIDATE,
        ExternalManifestCandidateKind.MEMORY_SCHEMA_MANIFEST: ExternalDigestionCandidateKind.MEMORY_SCHEMA_PATTERN_CANDIDATE,
        ExternalManifestCandidateKind.APPROVAL_POLICY_MANIFEST: ExternalDigestionCandidateKind.APPROVAL_POLICY_PATTERN_CANDIDATE,
        ExternalManifestCandidateKind.AUDIT_POLICY_MANIFEST: ExternalDigestionCandidateKind.AUDIT_POLICY_PATTERN_CANDIDATE,
        ExternalManifestCandidateKind.RESULT_ENVELOPE_MANIFEST: ExternalDigestionCandidateKind.RESULT_ENVELOPE_PATTERN_CANDIDATE,
        ExternalManifestCandidateKind.OCEL_TRACE_MANIFEST: ExternalDigestionCandidateKind.OCEL_TRACE_PATTERN_CANDIDATE,
    }.get(kind, ExternalDigestionCandidateKind.UNKNOWN)


def infer_external_digestion_pattern_kind_from_candidate_kind(
    candidate_kind: ExternalDigestionCandidateKind | str,
) -> ExternalDigestionPatternKind:
    kind = ExternalDigestionCandidateKind(candidate_kind)
    return {
        ExternalDigestionCandidateKind.SKILL_PATTERN_CANDIDATE: ExternalDigestionPatternKind.CONTRACT_PATTERN,
        ExternalDigestionCandidateKind.TOOL_CONTRACT_PATTERN_CANDIDATE: ExternalDigestionPatternKind.SCHEMA_PATTERN,
        ExternalDigestionCandidateKind.PLUGIN_PATTERN_CANDIDATE: ExternalDigestionPatternKind.MANIFEST_PATTERN,
        ExternalDigestionCandidateKind.MISSION_PATTERN_CANDIDATE: ExternalDigestionPatternKind.WORKFLOW_PATTERN,
        ExternalDigestionCandidateKind.GATEWAY_CONTRACT_PATTERN_CANDIDATE: ExternalDigestionPatternKind.ADAPTER_PATTERN,
        ExternalDigestionCandidateKind.PROVIDER_ADAPTER_PATTERN_CANDIDATE: ExternalDigestionPatternKind.ROUTING_PATTERN,
        ExternalDigestionCandidateKind.PROFILE_PATTERN_CANDIDATE: ExternalDigestionPatternKind.MANIFEST_PATTERN,
        ExternalDigestionCandidateKind.MEMORY_SCHEMA_PATTERN_CANDIDATE: ExternalDigestionPatternKind.SCHEMA_PATTERN,
        ExternalDigestionCandidateKind.APPROVAL_POLICY_PATTERN_CANDIDATE: ExternalDigestionPatternKind.APPROVAL_BOUNDARY_PATTERN,
        ExternalDigestionCandidateKind.AUDIT_POLICY_PATTERN_CANDIDATE: ExternalDigestionPatternKind.AUDIT_BOUNDARY_PATTERN,
        ExternalDigestionCandidateKind.RESULT_ENVELOPE_PATTERN_CANDIDATE: ExternalDigestionPatternKind.RESULT_BOUNDARY_PATTERN,
        ExternalDigestionCandidateKind.OCEL_TRACE_PATTERN_CANDIDATE: ExternalDigestionPatternKind.OCEL_TRACE_PATTERN,
        ExternalDigestionCandidateKind.PROMPT_PATTERN_CANDIDATE: ExternalDigestionPatternKind.PROMPT_PATTERN,
        ExternalDigestionCandidateKind.DELEGATION_PACKET_PATTERN_CANDIDATE: ExternalDigestionPatternKind.ROUTING_PATTERN,
    }.get(kind, ExternalDigestionPatternKind.UNKNOWN)


def infer_external_digestion_route_from_risk_classification(
    classification: ExternalCapabilityRiskClassification,
) -> ExternalDigestionRoute:
    risk_class = ExternalCapabilityRiskClass(classification.risk_class)
    route = ExternalCapabilityRiskRoute(classification.route)
    if risk_class == ExternalCapabilityRiskClass.DIGESTIBLE_PATTERN and route == ExternalCapabilityRiskRoute.SEND_TO_V0326_DIGESTION_GENERATOR:
        return ExternalDigestionRoute.SEND_TO_V0327_INTERNAL_CANDIDATE_EMITTER
    if route == ExternalCapabilityRiskRoute.SEND_TO_V0328_DOMINION_EMITTER:
        return ExternalDigestionRoute.SEND_TO_V0328_DOMINION_CANDIDATE_EMITTER
    if route == ExternalCapabilityRiskRoute.BLOCK:
        return ExternalDigestionRoute.BLOCK
    if route == ExternalCapabilityRiskRoute.REQUIRE_FUTURE_GATE:
        return ExternalDigestionRoute.FUTURE_TRACK
    if route == ExternalCapabilityRiskRoute.NO_OP:
        return ExternalDigestionRoute.NO_OP
    if route == ExternalCapabilityRiskRoute.REJECT:
        return ExternalDigestionRoute.REJECT
    if route == ExternalCapabilityRiskRoute.REQUIRE_REVIEW:
        return ExternalDigestionRoute.REQUIRE_REVIEW
    return ExternalDigestionRoute.UNKNOWN


def infer_external_digestion_blockers_from_risk_classification(
    classification: ExternalCapabilityRiskClassification,
) -> list[ExternalDigestionBlockerKind]:
    risk_class = ExternalCapabilityRiskClass(classification.risk_class)
    route = ExternalCapabilityRiskRoute(classification.route)
    blockers: list[ExternalDigestionBlockerKind] = []
    if route == ExternalCapabilityRiskRoute.BLOCK or risk_class == ExternalCapabilityRiskClass.BLOCKED:
        blockers.append(ExternalDigestionBlockerKind.BLOCKED_RISK_ROUTE)
    if route == ExternalCapabilityRiskRoute.SEND_TO_V0328_DOMINION_EMITTER or risk_class == ExternalCapabilityRiskClass.DOMINION_REQUIRED:
        blockers.append(ExternalDigestionBlockerKind.DOMINION_REQUIRED_ROUTE)
    if route == ExternalCapabilityRiskRoute.REQUIRE_FUTURE_GATE or risk_class == ExternalCapabilityRiskClass.FUTURE_TRACK:
        blockers.append(ExternalDigestionBlockerKind.FUTURE_GATE_REQUIRED)
    for factor in classification.risk_factors:
        surface = factor.risk_surface
        mapped = {
            "plugin_loading": ExternalDigestionBlockerKind.PLUGIN_LOADING_SURFACE,
            "external_plugin_loading": ExternalDigestionBlockerKind.PLUGIN_LOADING_SURFACE,
            "tool_invocation": ExternalDigestionBlockerKind.TOOL_INVOCATION_SURFACE,
            "mission_execution": ExternalDigestionBlockerKind.MISSION_EXECUTION_SURFACE,
            "provider_invocation": ExternalDigestionBlockerKind.PROVIDER_INVOCATION_SURFACE,
            "gateway_connection": ExternalDigestionBlockerKind.GATEWAY_CONNECTION_SURFACE,
            "credential_access": ExternalDigestionBlockerKind.CREDENTIAL_ACCESS_SURFACE,
            "network_access": ExternalDigestionBlockerKind.NETWORK_ACCESS_SURFACE,
            "command_execution": ExternalDigestionBlockerKind.COMMAND_EXECUTION_SURFACE,
            "memory_mutation": ExternalDigestionBlockerKind.MEMORY_MUTATION_SURFACE,
            "registry_mutation": ExternalDigestionBlockerKind.REGISTRY_MUTATION_SURFACE,
        }.get(str(surface))
        if mapped is not None and mapped not in blockers:
            blockers.append(mapped)
    return blockers


def external_digestion_candidate_is_not_internal_candidate(candidate: ExternalHarnessDigestionCandidate) -> bool:
    return (
        candidate.ready_for_internal_candidate_creation is False
        and candidate.ready_for_internalization is False
        and candidate.ready_for_execution is False
        and candidate.internal_skill_candidate is False
        and candidate.active_internalization is False
    )


def external_pattern_map_is_not_internalization_plan(pattern_map: ExternalToInternalPatternMap) -> bool:
    return (
        pattern_map.ready_for_internal_candidate_emission is False
        and pattern_map.ready_for_internalization is False
        and pattern_map.ready_for_execution is False
        and pattern_map.internal_skill_candidate is False
        and pattern_map.internalization_plan is False
    )


def external_digestion_candidate_set_is_not_registry(candidate_set: ExternalDigestionCandidateSet) -> bool:
    return (
        candidate_set.ready_for_internal_candidate_creation is False
        and candidate_set.ready_for_execution is False
        and candidate_set.registry is False
        and candidate_set.internal_candidate_emission is False
    )


def v0326_readiness_report_is_not_runtime_ready(report: V0326ReadinessReport) -> bool:
    return (
        report.ready_for_execution is False
        and report.ready_for_internal_candidate_emission is False
        and report.ready_for_internal_skill_candidate_creation is False
        and report.ready_for_internal_tool_candidate_creation is False
        and report.ready_for_internalization is False
        and report.ready_for_registry_mutation is False
        and report.ready_for_memory_mutation is False
        and report.ready_for_plugin_loading is False
        and report.ready_for_tool_registration is False
        and report.ready_for_tool_invocation is False
        and report.ready_for_mission_installation is False
        and report.ready_for_provider_invocation is False
        and report.ready_for_gateway_connection is False
        and report.ready_for_network_access is False
        and report.ready_for_credential_access is False
        and report.ready_for_command_execution is False
    )
