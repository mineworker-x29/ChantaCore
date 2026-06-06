from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .digestion_generation import (
    ExternalDigestionCandidateKind,
    ExternalHarnessDigestionCandidate,
    ExternalToInternalPatternMap,
)
from .profiles import _metadata_flag_true, _require_non_blank, _validate_object_list, _validate_string_list


V0327_VERSION = "v0.32.7"
V0327_RELEASE_NAME = "v0.32.7 Internal Skill Candidate Emitter"

DEFAULT_EMISSION_PROHIBITED_RUNTIME_ACTIONS = [
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
    "candidate activation",
    "skill activation",
    "policy activation",
    "registry mutation",
    "memory mutation",
    "internalization",
    "implementation creation",
    "dominion target creation",
    "dominion decision creation",
    "OCEL emission",
]


class InternalCandidateEmissionKind(StrEnum):
    EMITTED_INTERNAL_SKILL_CANDIDATE = "emitted_internal_skill_candidate"
    EMITTED_INTERNAL_TOOL_CONTRACT_CANDIDATE = "emitted_internal_tool_contract_candidate"
    EMITTED_INTERNAL_MISSION_CANDIDATE = "emitted_internal_mission_candidate"
    EMITTED_INTERNAL_POLICY_CANDIDATE = "emitted_internal_policy_candidate"
    EMITTED_INTERNAL_MEMORY_SCHEMA_CANDIDATE = "emitted_internal_memory_schema_candidate"
    EMITTED_INTERNAL_PROMPT_PATTERN_CANDIDATE = "emitted_internal_prompt_pattern_candidate"
    EMITTED_INTERNAL_TRACE_EVENT_PATTERN_CANDIDATE = "emitted_internal_trace_event_pattern_candidate"
    EMITTED_INTERNAL_RESULT_ENVELOPE_CANDIDATE = "emitted_internal_result_envelope_candidate"
    EMITTED_INTERNAL_APPROVAL_BOUNDARY_CANDIDATE = "emitted_internal_approval_boundary_candidate"
    EMITTED_INTERNAL_PROFILE_PATTERN_CANDIDATE = "emitted_internal_profile_pattern_candidate"
    NO_OP_CANDIDATE = "no_op_candidate"
    FUTURE_TRACK_CANDIDATE = "future_track_candidate"
    UNKNOWN = "unknown"


class InternalCandidateEmissionStatus(StrEnum):
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


class InternalCandidateEmissionRoute(StrEnum):
    EMIT_FOR_V0329_CONSOLIDATION = "emit_for_v0329_consolidation"
    SEND_TO_V0328_DOMINION_EMITTER = "send_to_v0328_dominion_emitter"
    REQUIRE_REVIEW = "require_review"
    DEFER = "defer"
    REJECT = "reject"
    BLOCK = "block"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class InternalCandidateEmissionSourceKind(StrEnum):
    EXTERNAL_HARNESS_DIGESTION_CANDIDATE = "external_harness_digestion_candidate"
    EXTERNAL_TO_INTERNAL_PATTERN_MAP = "external_to_internal_pattern_map"
    EXTERNAL_DIGESTION_CANDIDATE_SET = "external_digestion_candidate_set"
    EXTERNAL_DIGESTION_GENERATION_REPORT = "external_digestion_generation_report"
    HARNESS_PATTERN_DIGESTIBILITY_REPORT = "harness_pattern_digestibility_report"
    EXTERNAL_MANIFEST_CANDIDATE = "external_manifest_candidate"
    EXTERNAL_CAPABILITY_RISK_CLASSIFICATION = "external_capability_risk_classification"
    OPENCODE_OBSERVATION_OUTPUT = "opencode_observation_output"
    OPENCLAW_OBSERVATION_OUTPUT = "openclaw_observation_output"
    HERMES_OBSERVATION_OUTPUT = "hermes_observation_output"
    REFERENCE_FILE_INVENTORY = "reference_file_inventory"
    REFERENCE_CORPUS_SNAPSHOT = "reference_corpus_snapshot"
    MANUAL_CANDIDATE_EMISSION_REVIEW = "manual_candidate_emission_review"
    UNKNOWN = "unknown"


class InternalCandidateEmissionEvidenceQuality(StrEnum):
    UNKNOWN = "unknown"
    NONE = "none"
    WEAK = "weak"
    PARTIAL = "partial"
    SUFFICIENT_FOR_CANDIDATE_EMISSION = "sufficient_for_candidate_emission"
    SUFFICIENT_FOR_V0329_REVIEW = "sufficient_for_v0329_review"
    CONFLICTING = "conflicting"
    BLOCKED = "blocked"


class InternalCandidateEmissionReviewRequirementKind(StrEnum):
    EVIDENCE_REVIEW = "evidence_review"
    CONTRACT_REVIEW = "contract_review"
    SCHEMA_REVIEW = "schema_review"
    VALIDATION_REVIEW = "validation_review"
    TEST_REVIEW = "test_review"
    DOCUMENTATION_REVIEW = "documentation_review"
    SAFETY_REVIEW = "safety_review"
    BOUNDARY_REVIEW = "boundary_review"
    OCEL_TRACE_REVIEW = "ocel_trace_review"
    HUMAN_REVIEW = "human_review"
    FUTURE_GATE_REVIEW = "future_gate_review"
    UNKNOWN = "unknown"


class InternalCandidateEmissionBlockerKind(StrEnum):
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    CONFLICTING_EVIDENCE = "conflicting_evidence"
    MISSING_EXTERNAL_DIGESTION_CANDIDATE = "missing_external_digestion_candidate"
    MISSING_PATTERN_MAP = "missing_pattern_map"
    BLOCKED_DIGESTIBILITY_ASSESSMENT = "blocked_digestibility_assessment"
    DOMINION_REQUIRED_ROUTE = "dominion_required_route"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNSAFE_RUNTIME_SURFACE = "unsafe_runtime_surface"
    MISSING_CONTRACT_SUMMARY = "missing_contract_summary"
    MISSING_INPUT_CONTRACT = "missing_input_contract"
    MISSING_OUTPUT_CONTRACT = "missing_output_contract"
    MISSING_VALIDATION_SUMMARY = "missing_validation_summary"
    INCOMPATIBLE_WITH_INTERNAL_TRIAD = "incompatible_with_internal_triad"
    DUPLICATE_CANDIDATE_RISK = "duplicate_candidate_risk"
    UNKNOWN = "unknown"


def _validate_version_includes_v0327(version: str) -> None:
    _require_non_blank("version", version)
    if V0327_VERSION not in version:
        raise ValueError("version must include v0.32.7")


def _validate_kind_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.32.7")


def _validate_default_prohibitions(name: str, values: list[str]) -> None:
    _validate_string_list(name, values)
    missing = set(DEFAULT_EMISSION_PROHIBITED_RUNTIME_ACTIONS) - set(values)
    if missing:
        raise ValueError(f"{name} missing v0.32.7 prohibitions: {sorted(missing)}")


@dataclass(frozen=True)
class InternalCandidateEmissionSourceRef:
    source_ref_id: str
    source_kind: InternalCandidateEmissionSourceKind | str
    source_id: str
    external_digestion_candidate_id: str | None = None
    pattern_map_id: str | None = None
    manifest_candidate_id: str | None = None
    risk_classification_id: str | None = None
    harness_kind: str | None = None
    reference_entry_ids: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        InternalCandidateEmissionSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _validate_string_list("reference_entry_ids", self.reference_entry_ids)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"source_fetch", "execution", "live_scan"}):
            raise ValueError("InternalCandidateEmissionSourceRef is not source fetch or execution")

    @property
    def source_fetch(self) -> bool:
        return False

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalCandidateEmissionEvidenceRef:
    evidence_ref_id: str
    source_evidence_ref_id: str | None = None
    evidence_kind: str = "static_contract_evidence"
    evidence_summary: str = "Static evidence reference only."
    quality: InternalCandidateEmissionEvidenceQuality | str = InternalCandidateEmissionEvidenceQuality.UNKNOWN
    limitations: list[str] = field(default_factory=list)
    conflict_notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("evidence_ref_id", self.evidence_ref_id)
        _require_non_blank("evidence_kind", self.evidence_kind)
        _require_non_blank("evidence_summary", self.evidence_summary)
        InternalCandidateEmissionEvidenceQuality(self.quality)
        _validate_string_list("limitations", self.limitations)
        _validate_string_list("conflict_notes", self.conflict_notes)
        if _metadata_flag_true(self.metadata, {"runtime_trust", "activation_evidence"}):
            raise ValueError("InternalCandidateEmissionEvidenceRef is not runtime trust")

    @property
    def runtime_trust(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalCandidateEmissionBlocker:
    blocker_id: str
    blocker_kind: InternalCandidateEmissionBlockerKind | str
    source_ref_ids: list[str] = field(default_factory=list)
    target_candidate_id: str | None = None
    reason: str = "Static candidate emission blocker."
    blocks_v0329: bool = True
    routes_to_v0328: bool = False
    routes_to_future_gate: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("blocker_id", self.blocker_id)
        InternalCandidateEmissionBlockerKind(self.blocker_kind)
        _validate_string_list("source_ref_ids", self.source_ref_ids)
        _require_non_blank("reason", self.reason)
        for name in ("blocks_v0329", "routes_to_v0328", "routes_to_future_gate"):
            if not isinstance(getattr(self, name), bool):
                raise TypeError(f"{name} must be bool")
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"remediation", "execution"}):
            raise ValueError("InternalCandidateEmissionBlocker does not execute remediation")

    @property
    def remediation_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalCandidateEmissionReviewRequirement:
    review_requirement_id: str
    requirement_kind: InternalCandidateEmissionReviewRequirementKind | str
    target_candidate_ids: list[str] = field(default_factory=list)
    reason: str = "Static candidate review required."
    required_evidence_refs: list[str] = field(default_factory=list)
    required_reviewer_refs: list[str] = field(default_factory=list)
    approval_granted: bool = False
    blocks_activation: bool = True
    blocks_registry_mutation: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("review_requirement_id", self.review_requirement_id)
        InternalCandidateEmissionReviewRequirementKind(self.requirement_kind)
        _require_non_blank("reason", self.reason)
        for name in ("target_candidate_ids", "required_evidence_refs", "required_reviewer_refs"):
            _validate_string_list(name, getattr(self, name))
        if self.approval_granted is not False:
            raise ValueError("approval_granted must always be False in v0.32.7")
        if self.blocks_activation is not True:
            raise ValueError("blocks_activation must default True in v0.32.7")
        if self.blocks_registry_mutation is not True:
            raise ValueError("blocks_registry_mutation must default True in v0.32.7")
        if _metadata_flag_true(self.metadata, {"approval", "approval_granted"}):
            raise ValueError("InternalCandidateEmissionReviewRequirement is not approval")

    @property
    def approval(self) -> bool:
        return False


@dataclass(frozen=True)
class EmittedInternalCandidateBase:
    emitted_candidate_id: str
    emission_kind: InternalCandidateEmissionKind | str
    status: InternalCandidateEmissionStatus | str
    title: str
    purpose: str
    source_refs: list[InternalCandidateEmissionSourceRef] = field(default_factory=list)
    evidence_refs: list[InternalCandidateEmissionEvidenceRef] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    review_requirements: list[InternalCandidateEmissionReviewRequirement] = field(default_factory=list)
    blockers: list[InternalCandidateEmissionBlocker] = field(default_factory=list)
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_EMISSION_PROHIBITED_RUNTIME_ACTIONS))
    ready_for_activation: bool = False
    ready_for_skill_activation: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_internalization: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("emitted_candidate_id", self.emitted_candidate_id)
        InternalCandidateEmissionKind(self.emission_kind)
        InternalCandidateEmissionStatus(self.status)
        _require_non_blank("title", self.title)
        _require_non_blank("purpose", self.purpose)
        _validate_object_list("source_refs", self.source_refs, InternalCandidateEmissionSourceRef)
        _validate_object_list("evidence_refs", self.evidence_refs, InternalCandidateEmissionEvidenceRef)
        for name in ("assumptions", "limitations", "gaps"):
            _validate_string_list(name, getattr(self, name))
        _validate_object_list("review_requirements", self.review_requirements, InternalCandidateEmissionReviewRequirement)
        _validate_object_list("blockers", self.blockers, InternalCandidateEmissionBlocker)
        _validate_default_prohibitions("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_false(
            self,
            (
                "ready_for_activation",
                "ready_for_skill_activation",
                "ready_for_registry_mutation",
                "ready_for_memory_mutation",
                "ready_for_internalization",
                "ready_for_execution",
            ),
        )
        if _metadata_flag_true(self.metadata, {"active_artifact", "implementation", "runtime"}):
            raise ValueError("emitted internal candidate is not active artifact")

    @property
    def active_artifact(self) -> bool:
        return False


@dataclass(frozen=True)
class EmittedInternalSkillCandidate(EmittedInternalCandidateBase):
    proposed_skill_name: str = ""
    proposed_skill_kind: str = "external_derived_skill_pattern"
    source_pattern_map_ids: list[str] = field(default_factory=list)
    input_contract_summary: str = "Static input contract summary only."
    output_contract_summary: str = "Static output contract summary only."
    validation_summary: str = "Static validation summary only."
    required_tests: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__post_init__()
        _require_non_blank("proposed_skill_name", self.proposed_skill_name)
        for name in ("input_contract_summary", "output_contract_summary", "validation_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_string_list("source_pattern_map_ids", self.source_pattern_map_ids)
        _validate_string_list("required_tests", self.required_tests)

    @property
    def active_skill(self) -> bool:
        return False

    @property
    def registered_skill(self) -> bool:
        return False


@dataclass(frozen=True)
class EmittedInternalToolContractCandidate(EmittedInternalCandidateBase):
    proposed_tool_name: str = ""
    tool_contract_summary: str = "Static tool contract summary only."
    input_schema_summary: str = "Static input schema summary only."
    output_schema_summary: str = "Static output schema summary only."
    side_effect_policy_summary: str = "No side effect is authorized."
    source_pattern_map_ids: list[str] = field(default_factory=list)
    required_tests: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__post_init__()
        _require_non_blank("proposed_tool_name", self.proposed_tool_name)
        for name in ("tool_contract_summary", "input_schema_summary", "output_schema_summary", "side_effect_policy_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_string_list("source_pattern_map_ids", self.source_pattern_map_ids)
        _validate_string_list("required_tests", self.required_tests)

    @property
    def registered_tool(self) -> bool:
        return False

    @property
    def tool_invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class EmittedInternalMissionCandidate(EmittedInternalCandidateBase):
    proposed_mission_name: str = ""
    mission_scope_summary: str = "Static mission scope summary only."
    trigger_policy_summary: str = "No trigger execution is authorized."
    schedule_policy_summary: str = "No scheduler runtime is authorized."
    source_pattern_map_ids: list[str] = field(default_factory=list)
    required_tests: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__post_init__()
        _require_non_blank("proposed_mission_name", self.proposed_mission_name)
        _validate_string_list("source_pattern_map_ids", self.source_pattern_map_ids)
        _validate_string_list("required_tests", self.required_tests)

    @property
    def installed_mission(self) -> bool:
        return False

    @property
    def mission_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class EmittedInternalPolicyCandidate(EmittedInternalCandidateBase):
    proposed_policy_name: str = ""
    policy_scope_summary: str = "Static policy scope summary only."
    default_decision: str = "deny"
    enforcement_summary: str = "No enforcement execution is authorized."
    source_pattern_map_ids: list[str] = field(default_factory=list)
    required_tests: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__post_init__()
        _require_non_blank("proposed_policy_name", self.proposed_policy_name)
        _require_non_blank("enforcement_summary", self.enforcement_summary)
        _validate_string_list("source_pattern_map_ids", self.source_pattern_map_ids)
        _validate_string_list("required_tests", self.required_tests)

    @property
    def active_policy(self) -> bool:
        return False

    @property
    def enforcement_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class EmittedInternalMemorySchemaCandidate(EmittedInternalCandidateBase):
    proposed_schema_name: str = ""
    memory_scope_summary: str = "Static memory schema summary only."
    allowed_fields: list[str] = field(default_factory=list)
    prohibited_fields: list[str] = field(default_factory=list)
    persistence_policy_summary: str = "No memory persistence is authorized."
    source_pattern_map_ids: list[str] = field(default_factory=list)
    required_tests: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__post_init__()
        _require_non_blank("proposed_schema_name", self.proposed_schema_name)
        for name in ("allowed_fields", "prohibited_fields", "source_pattern_map_ids", "required_tests"):
            _validate_string_list(name, getattr(self, name))

    @property
    def memory_writer(self) -> bool:
        return False

    @property
    def memory_persistence(self) -> bool:
        return False


@dataclass(frozen=True)
class EmittedInternalPromptPatternCandidate(EmittedInternalCandidateBase):
    proposed_pattern_name: str = ""
    prompt_scope_summary: str = "Static prompt pattern summary only."
    insertion_policy_summary: str = "No prompt insertion is authorized."
    context_budget_notes: list[str] = field(default_factory=list)
    source_pattern_map_ids: list[str] = field(default_factory=list)
    required_tests: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__post_init__()
        _require_non_blank("proposed_pattern_name", self.proposed_pattern_name)
        for name in ("context_budget_notes", "source_pattern_map_ids", "required_tests"):
            _validate_string_list(name, getattr(self, name))

    @property
    def prompt_injection(self) -> bool:
        return False


@dataclass(frozen=True)
class EmittedInternalTraceEventPatternCandidate(EmittedInternalCandidateBase):
    proposed_event_type: str = ""
    proposed_object_types: list[str] = field(default_factory=list)
    proposed_relation_types: list[str] = field(default_factory=list)
    ocel_visibility_summary: str = "Static OCEL visibility summary only."
    source_pattern_map_ids: list[str] = field(default_factory=list)
    required_tests: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__post_init__()
        _require_non_blank("proposed_event_type", self.proposed_event_type)
        for name in ("proposed_object_types", "proposed_relation_types", "source_pattern_map_ids", "required_tests"):
            _validate_string_list(name, getattr(self, name))

    @property
    def ocel_event_emission(self) -> bool:
        return False


@dataclass(frozen=True)
class EmittedInternalResultEnvelopeCandidate(EmittedInternalCandidateBase):
    proposed_envelope_name: str = ""
    required_fields: list[str] = field(default_factory=list)
    optional_fields: list[str] = field(default_factory=list)
    forbidden_fields: list[str] = field(default_factory=list)
    raw_output_allowed: bool = False
    memory_persistence_allowed: bool = False
    source_pattern_map_ids: list[str] = field(default_factory=list)
    required_tests: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__post_init__()
        _require_non_blank("proposed_envelope_name", self.proposed_envelope_name)
        for name in ("required_fields", "optional_fields", "forbidden_fields", "source_pattern_map_ids", "required_tests"):
            _validate_string_list(name, getattr(self, name))
        if self.raw_output_allowed is not False:
            raise ValueError("raw_output_allowed must default False in v0.32.7")
        if self.memory_persistence_allowed is not False:
            raise ValueError("memory_persistence_allowed must default False in v0.32.7")

    @property
    def result_ingestion(self) -> bool:
        return False


@dataclass(frozen=True)
class EmittedInternalApprovalBoundaryCandidate(EmittedInternalCandidateBase):
    proposed_boundary_name: str = ""
    approval_scope_summary: str = "Static approval boundary summary only."
    required_review_kinds: list[InternalCandidateEmissionReviewRequirementKind | str] = field(default_factory=list)
    default_decision: str = "deny"
    source_pattern_map_ids: list[str] = field(default_factory=list)
    required_tests: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__post_init__()
        _require_non_blank("proposed_boundary_name", self.proposed_boundary_name)
        _validate_kind_list("required_review_kinds", self.required_review_kinds, InternalCandidateEmissionReviewRequirementKind)
        _validate_string_list("source_pattern_map_ids", self.source_pattern_map_ids)
        _validate_string_list("required_tests", self.required_tests)

    @property
    def approval_granted(self) -> bool:
        return False

    @property
    def approval_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class EmittedInternalProfilePatternCandidate(EmittedInternalCandidateBase):
    proposed_profile_pattern_name: str = ""
    profile_scope_summary: str = "Static profile pattern summary only."
    memory_scope_summary: str | None = None
    private_data_boundary_summary: str | None = None
    source_pattern_map_ids: list[str] = field(default_factory=list)
    required_tests: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__post_init__()
        _require_non_blank("proposed_profile_pattern_name", self.proposed_profile_pattern_name)
        _validate_string_list("source_pattern_map_ids", self.source_pattern_map_ids)
        _validate_string_list("required_tests", self.required_tests)

    @property
    def profile_activation(self) -> bool:
        return False

    @property
    def memory_or_private_data_access(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalHarnessInternalCandidateSet:
    candidate_set_id: str
    version: str = V0327_VERSION
    source_digestion_candidate_set_id: str | None = None
    skill_candidates: list[EmittedInternalSkillCandidate] = field(default_factory=list)
    tool_contract_candidates: list[EmittedInternalToolContractCandidate] = field(default_factory=list)
    mission_candidates: list[EmittedInternalMissionCandidate] = field(default_factory=list)
    policy_candidates: list[EmittedInternalPolicyCandidate] = field(default_factory=list)
    memory_schema_candidates: list[EmittedInternalMemorySchemaCandidate] = field(default_factory=list)
    prompt_pattern_candidates: list[EmittedInternalPromptPatternCandidate] = field(default_factory=list)
    trace_event_pattern_candidates: list[EmittedInternalTraceEventPatternCandidate] = field(default_factory=list)
    result_envelope_candidates: list[EmittedInternalResultEnvelopeCandidate] = field(default_factory=list)
    approval_boundary_candidates: list[EmittedInternalApprovalBoundaryCandidate] = field(default_factory=list)
    profile_pattern_candidates: list[EmittedInternalProfilePatternCandidate] = field(default_factory=list)
    emitted_candidate_ids: list[str] = field(default_factory=list)
    deferred_source_refs: list[str] = field(default_factory=list)
    rejected_source_refs: list[str] = field(default_factory=list)
    blocked_source_refs: list[str] = field(default_factory=list)
    dominion_required_source_refs: list[str] = field(default_factory=list)
    future_track_source_refs: list[str] = field(default_factory=list)
    no_op_source_refs: list[str] = field(default_factory=list)
    evidence_refs: list[InternalCandidateEmissionEvidenceRef] = field(default_factory=list)
    ready_for_v0329_consolidation: bool = False
    ready_for_candidate_activation: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_internalization: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("candidate_set_id", self.candidate_set_id)
        _validate_version_includes_v0327(self.version)
        _validate_object_list("skill_candidates", self.skill_candidates, EmittedInternalSkillCandidate)
        _validate_object_list("tool_contract_candidates", self.tool_contract_candidates, EmittedInternalToolContractCandidate)
        _validate_object_list("mission_candidates", self.mission_candidates, EmittedInternalMissionCandidate)
        _validate_object_list("policy_candidates", self.policy_candidates, EmittedInternalPolicyCandidate)
        _validate_object_list("memory_schema_candidates", self.memory_schema_candidates, EmittedInternalMemorySchemaCandidate)
        _validate_object_list("prompt_pattern_candidates", self.prompt_pattern_candidates, EmittedInternalPromptPatternCandidate)
        _validate_object_list("trace_event_pattern_candidates", self.trace_event_pattern_candidates, EmittedInternalTraceEventPatternCandidate)
        _validate_object_list("result_envelope_candidates", self.result_envelope_candidates, EmittedInternalResultEnvelopeCandidate)
        _validate_object_list("approval_boundary_candidates", self.approval_boundary_candidates, EmittedInternalApprovalBoundaryCandidate)
        _validate_object_list("profile_pattern_candidates", self.profile_pattern_candidates, EmittedInternalProfilePatternCandidate)
        for name in (
            "emitted_candidate_ids",
            "deferred_source_refs",
            "rejected_source_refs",
            "blocked_source_refs",
            "dominion_required_source_refs",
            "future_track_source_refs",
            "no_op_source_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_object_list("evidence_refs", self.evidence_refs, InternalCandidateEmissionEvidenceRef)
        _validate_false(self, ("ready_for_candidate_activation", "ready_for_registry_mutation", "ready_for_internalization", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"registry", "active_set"}):
            raise ValueError("ExternalHarnessInternalCandidateSet is not registry")

    @property
    def registry(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalCandidateEmissionInput:
    emission_input_id: str
    source_version: str = V0327_VERSION
    external_digestion_candidate_ids: list[str] = field(default_factory=list)
    external_digestion_candidate_set_ids: list[str] = field(default_factory=list)
    pattern_map_ids: list[str] = field(default_factory=list)
    digestion_generation_report_ids: list[str] = field(default_factory=list)
    digestibility_report_ids: list[str] = field(default_factory=list)
    source_refs: list[InternalCandidateEmissionSourceRef] = field(default_factory=list)
    requested_emission_kinds: list[InternalCandidateEmissionKind | str] = field(default_factory=list)
    task_summary: str = "Emit external-derived internal candidate design artifacts."
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_EMISSION_PROHIBITED_RUNTIME_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("emission_input_id", self.emission_input_id)
        _require_non_blank("source_version", self.source_version)
        for name in (
            "external_digestion_candidate_ids",
            "external_digestion_candidate_set_ids",
            "pattern_map_ids",
            "digestion_generation_report_ids",
            "digestibility_report_ids",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_object_list("source_refs", self.source_refs, InternalCandidateEmissionSourceRef)
        _validate_kind_list("requested_emission_kinds", self.requested_emission_kinds, InternalCandidateEmissionKind)
        _require_non_blank("task_summary", self.task_summary)
        _validate_default_prohibitions("prohibited_runtime_actions", self.prohibited_runtime_actions)
        if _metadata_flag_true(self.metadata, {"execution_request", "activation_request"}):
            raise ValueError("InternalCandidateEmissionInput is not execution request")

    @property
    def execution_request(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalCandidateEmissionFinding:
    finding_id: str
    emission_input_id: str
    source_ref_ids: list[str]
    target_emitted_candidate_id: str | None
    emission_kind: InternalCandidateEmissionKind | str
    route: InternalCandidateEmissionRoute | str
    status: InternalCandidateEmissionStatus | str
    summary: str
    evidence_quality: InternalCandidateEmissionEvidenceQuality | str = InternalCandidateEmissionEvidenceQuality.UNKNOWN
    blocker_ids: list[str] = field(default_factory=list)
    review_requirement_ids: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("emission_input_id", self.emission_input_id)
        _validate_string_list("source_ref_ids", self.source_ref_ids)
        InternalCandidateEmissionKind(self.emission_kind)
        InternalCandidateEmissionRoute(self.route)
        InternalCandidateEmissionStatus(self.status)
        _require_non_blank("summary", self.summary)
        InternalCandidateEmissionEvidenceQuality(self.evidence_quality)
        for name in ("blocker_ids", "review_requirement_ids", "evidence_refs", "assumptions", "limitations"):
            _validate_string_list(name, getattr(self, name))
        if _metadata_flag_true(self.metadata, {"active_candidate", "activation"}):
            raise ValueError("InternalCandidateEmissionFinding is not active candidate or activation")

    @property
    def active_candidate(self) -> bool:
        return False

    @property
    def activation(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalCandidateEmissionReport:
    report_id: str
    version: str
    emission_input_id: str
    candidate_set_id: str | None = None
    findings: list[InternalCandidateEmissionFinding] = field(default_factory=list)
    summary: str = "Internal candidate emission report for design artifacts."
    emitted_candidate_count: int = 0
    blocked_items: list[str] = field(default_factory=list)
    deferred_items: list[str] = field(default_factory=list)
    dominion_required_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0329_consolidation: bool = False
    ready_for_candidate_activation: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_internalization: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0327(self.version)
        _require_non_blank("emission_input_id", self.emission_input_id)
        _validate_object_list("findings", self.findings, InternalCandidateEmissionFinding)
        _require_non_blank("summary", self.summary)
        if self.emitted_candidate_count < 0:
            raise ValueError("emitted_candidate_count must be >= 0")
        for name in ("blocked_items", "deferred_items", "dominion_required_items", "future_track_items", "gaps", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, ("ready_for_candidate_activation", "ready_for_registry_mutation", "ready_for_internalization", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"runtime_result", "implementation"}):
            raise ValueError("InternalCandidateEmissionReport is not runtime result or implementation")

    @property
    def runtime_result(self) -> bool:
        return False

    @property
    def implementation(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalCandidateEmissionRunPreview:
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
    no_candidate_activation_guarantee: bool = True
    no_skill_activation_guarantee: bool = True
    no_registry_mutation_guarantee: bool = True
    no_memory_mutation_guarantee: bool = True
    no_internalization_guarantee: bool = True
    no_implementation_creation_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must always be True in v0.32.7")
        if _metadata_flag_true(self.metadata, {"execution"}):
            raise ValueError("InternalCandidateEmissionRunPreview is not execution")

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalCandidateEmissionNoRuntimeGuarantee:
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
    no_candidate_activation: bool = True
    no_skill_activation: bool = True
    no_tool_activation: bool = True
    no_policy_activation: bool = True
    no_memory_mutation: bool = True
    no_registry_mutation: bool = True
    no_internalization: bool = True
    no_implementation_creation: bool = True
    no_dominion_target_creation: bool = True
    no_dominion_decision_creation: bool = True
    no_ocel_emission: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version_includes_v0327(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must always be True in v0.32.7")
        _validate_string_list("evidence_refs", self.evidence_refs)


@dataclass(frozen=True)
class V0327ReadinessReport:
    report_id: str
    version: str
    emission_report_id: str | None = None
    candidate_set_id: str | None = None
    summary: str = "v0.32.7 readiness is limited to design-stage handoff."
    ready_for_v0328_external_dominion_candidate_emitter: bool = False
    ready_for_v0329_external_observation_digestion_consolidation: bool = False
    ready_for_execution: bool = False
    ready_for_candidate_activation: bool = False
    ready_for_skill_activation: bool = False
    ready_for_tool_registration: bool = False
    ready_for_tool_invocation: bool = False
    ready_for_mission_installation: bool = False
    ready_for_policy_activation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_internalization: bool = False
    ready_for_implementation: bool = False
    ready_for_plugin_loading: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_gateway_connection: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    dominion_required_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_EMISSION_PROHIBITED_RUNTIME_ACTIONS))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0327(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(
            self,
            (
                "ready_for_execution",
                "ready_for_candidate_activation",
                "ready_for_skill_activation",
                "ready_for_tool_registration",
                "ready_for_tool_invocation",
                "ready_for_mission_installation",
                "ready_for_policy_activation",
                "ready_for_memory_mutation",
                "ready_for_registry_mutation",
                "ready_for_internalization",
                "ready_for_implementation",
                "ready_for_plugin_loading",
                "ready_for_provider_invocation",
                "ready_for_gateway_connection",
                "ready_for_network_access",
                "ready_for_credential_access",
                "ready_for_command_execution",
            ),
        )
        for name in ("completed_items", "blocked_items", "dominion_required_items", "future_track_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_default_prohibitions("prohibited_until_later_gate", self.prohibited_until_later_gate)
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "activation", "internalization"}):
            raise ValueError("V0327ReadinessReport is not runtime enablement")


def build_internal_candidate_emission_source_ref(source_ref_id: str, source_kind: InternalCandidateEmissionSourceKind | str, source_id: str, **kwargs: Any) -> InternalCandidateEmissionSourceRef:
    return InternalCandidateEmissionSourceRef(source_ref_id=source_ref_id, source_kind=source_kind, source_id=source_id, **kwargs)


def build_internal_candidate_emission_evidence_ref(evidence_ref_id: str, **kwargs: Any) -> InternalCandidateEmissionEvidenceRef:
    return InternalCandidateEmissionEvidenceRef(evidence_ref_id=evidence_ref_id, **kwargs)


def build_internal_candidate_emission_blocker(blocker_id: str, blocker_kind: InternalCandidateEmissionBlockerKind | str, **kwargs: Any) -> InternalCandidateEmissionBlocker:
    return InternalCandidateEmissionBlocker(blocker_id=blocker_id, blocker_kind=blocker_kind, **kwargs)


def build_internal_candidate_emission_review_requirement(review_requirement_id: str, requirement_kind: InternalCandidateEmissionReviewRequirementKind | str, **kwargs: Any) -> InternalCandidateEmissionReviewRequirement:
    return InternalCandidateEmissionReviewRequirement(review_requirement_id=review_requirement_id, requirement_kind=requirement_kind, **kwargs)


def _candidate_defaults(emission_kind: InternalCandidateEmissionKind | str, declared_name: str, kwargs: dict[str, Any]) -> dict[str, Any]:
    merged = {
        "emission_kind": InternalCandidateEmissionKind(emission_kind),
        "status": InternalCandidateEmissionStatus.EMITTED_WITH_GAPS,
        "title": declared_name,
        "purpose": "External-derived internal candidate design artifact.",
    }
    merged.update(kwargs)
    return merged


def build_emitted_internal_skill_candidate(emitted_candidate_id: str, proposed_skill_name: str, **kwargs: Any) -> EmittedInternalSkillCandidate:
    return EmittedInternalSkillCandidate(emitted_candidate_id=emitted_candidate_id, proposed_skill_name=proposed_skill_name, **_candidate_defaults(InternalCandidateEmissionKind.EMITTED_INTERNAL_SKILL_CANDIDATE, proposed_skill_name, kwargs))


def build_emitted_internal_tool_contract_candidate(emitted_candidate_id: str, proposed_tool_name: str, **kwargs: Any) -> EmittedInternalToolContractCandidate:
    return EmittedInternalToolContractCandidate(emitted_candidate_id=emitted_candidate_id, proposed_tool_name=proposed_tool_name, **_candidate_defaults(InternalCandidateEmissionKind.EMITTED_INTERNAL_TOOL_CONTRACT_CANDIDATE, proposed_tool_name, kwargs))


def build_emitted_internal_mission_candidate(emitted_candidate_id: str, proposed_mission_name: str, **kwargs: Any) -> EmittedInternalMissionCandidate:
    return EmittedInternalMissionCandidate(emitted_candidate_id=emitted_candidate_id, proposed_mission_name=proposed_mission_name, **_candidate_defaults(InternalCandidateEmissionKind.EMITTED_INTERNAL_MISSION_CANDIDATE, proposed_mission_name, kwargs))


def build_emitted_internal_policy_candidate(emitted_candidate_id: str, proposed_policy_name: str, **kwargs: Any) -> EmittedInternalPolicyCandidate:
    return EmittedInternalPolicyCandidate(emitted_candidate_id=emitted_candidate_id, proposed_policy_name=proposed_policy_name, **_candidate_defaults(InternalCandidateEmissionKind.EMITTED_INTERNAL_POLICY_CANDIDATE, proposed_policy_name, kwargs))


def build_emitted_internal_memory_schema_candidate(emitted_candidate_id: str, proposed_schema_name: str, **kwargs: Any) -> EmittedInternalMemorySchemaCandidate:
    return EmittedInternalMemorySchemaCandidate(emitted_candidate_id=emitted_candidate_id, proposed_schema_name=proposed_schema_name, **_candidate_defaults(InternalCandidateEmissionKind.EMITTED_INTERNAL_MEMORY_SCHEMA_CANDIDATE, proposed_schema_name, kwargs))


def build_emitted_internal_prompt_pattern_candidate(emitted_candidate_id: str, proposed_pattern_name: str, **kwargs: Any) -> EmittedInternalPromptPatternCandidate:
    return EmittedInternalPromptPatternCandidate(emitted_candidate_id=emitted_candidate_id, proposed_pattern_name=proposed_pattern_name, **_candidate_defaults(InternalCandidateEmissionKind.EMITTED_INTERNAL_PROMPT_PATTERN_CANDIDATE, proposed_pattern_name, kwargs))


def build_emitted_internal_trace_event_pattern_candidate(emitted_candidate_id: str, proposed_event_type: str, **kwargs: Any) -> EmittedInternalTraceEventPatternCandidate:
    return EmittedInternalTraceEventPatternCandidate(emitted_candidate_id=emitted_candidate_id, proposed_event_type=proposed_event_type, **_candidate_defaults(InternalCandidateEmissionKind.EMITTED_INTERNAL_TRACE_EVENT_PATTERN_CANDIDATE, proposed_event_type, kwargs))


def build_emitted_internal_result_envelope_candidate(emitted_candidate_id: str, proposed_envelope_name: str, **kwargs: Any) -> EmittedInternalResultEnvelopeCandidate:
    return EmittedInternalResultEnvelopeCandidate(emitted_candidate_id=emitted_candidate_id, proposed_envelope_name=proposed_envelope_name, **_candidate_defaults(InternalCandidateEmissionKind.EMITTED_INTERNAL_RESULT_ENVELOPE_CANDIDATE, proposed_envelope_name, kwargs))


def build_emitted_internal_approval_boundary_candidate(emitted_candidate_id: str, proposed_boundary_name: str, **kwargs: Any) -> EmittedInternalApprovalBoundaryCandidate:
    return EmittedInternalApprovalBoundaryCandidate(emitted_candidate_id=emitted_candidate_id, proposed_boundary_name=proposed_boundary_name, **_candidate_defaults(InternalCandidateEmissionKind.EMITTED_INTERNAL_APPROVAL_BOUNDARY_CANDIDATE, proposed_boundary_name, kwargs))


def build_emitted_internal_profile_pattern_candidate(emitted_candidate_id: str, proposed_profile_pattern_name: str, **kwargs: Any) -> EmittedInternalProfilePatternCandidate:
    return EmittedInternalProfilePatternCandidate(emitted_candidate_id=emitted_candidate_id, proposed_profile_pattern_name=proposed_profile_pattern_name, **_candidate_defaults(InternalCandidateEmissionKind.EMITTED_INTERNAL_PROFILE_PATTERN_CANDIDATE, proposed_profile_pattern_name, kwargs))


def build_external_harness_internal_candidate_set(candidate_set_id: str, **kwargs: Any) -> ExternalHarnessInternalCandidateSet:
    return ExternalHarnessInternalCandidateSet(candidate_set_id=candidate_set_id, version=V0327_VERSION, **kwargs)


def build_internal_candidate_emission_input(emission_input_id: str, **kwargs: Any) -> InternalCandidateEmissionInput:
    return InternalCandidateEmissionInput(emission_input_id=emission_input_id, **kwargs)


def build_internal_candidate_emission_finding(finding_id: str, emission_input_id: str, source_ref_ids: list[str], target_emitted_candidate_id: str | None, emission_kind: InternalCandidateEmissionKind | str, route: InternalCandidateEmissionRoute | str, status: InternalCandidateEmissionStatus | str, summary: str, **kwargs: Any) -> InternalCandidateEmissionFinding:
    return InternalCandidateEmissionFinding(finding_id=finding_id, emission_input_id=emission_input_id, source_ref_ids=list(source_ref_ids), target_emitted_candidate_id=target_emitted_candidate_id, emission_kind=emission_kind, route=route, status=status, summary=summary, **kwargs)


def build_internal_candidate_emission_report(report_id: str, emission_input_id: str, **kwargs: Any) -> InternalCandidateEmissionReport:
    return InternalCandidateEmissionReport(report_id=report_id, version=V0327_VERSION, emission_input_id=emission_input_id, **kwargs)


def build_internal_candidate_emission_run_preview(run_preview_id: str = "internal_candidate_emission_run_preview:v0.32.7", **kwargs: Any) -> InternalCandidateEmissionRunPreview:
    return InternalCandidateEmissionRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_internal_candidate_emission_no_runtime_guarantee(guarantee_id: str = "internal_candidate_emission_no_runtime_guarantee:v0.32.7", evidence_refs: list[str] | None = None, metadata: dict[str, Any] | None = None) -> InternalCandidateEmissionNoRuntimeGuarantee:
    return InternalCandidateEmissionNoRuntimeGuarantee(guarantee_id=guarantee_id, version=V0327_VERSION, evidence_refs=list(evidence_refs or []), metadata=dict(metadata or {}))


def build_v0327_readiness_report(report_id: str = "v0327_readiness_report", emission_report_id: str | None = None, candidate_set_id: str | None = None, **kwargs: Any) -> V0327ReadinessReport:
    return V0327ReadinessReport(report_id=report_id, version=V0327_VERSION, emission_report_id=emission_report_id, candidate_set_id=candidate_set_id, **kwargs)


def infer_emission_kind_from_external_digestion_candidate(candidate: ExternalHarnessDigestionCandidate) -> InternalCandidateEmissionKind:
    kind = ExternalDigestionCandidateKind(candidate.candidate_kind)
    return {
        ExternalDigestionCandidateKind.SKILL_PATTERN_CANDIDATE: InternalCandidateEmissionKind.EMITTED_INTERNAL_SKILL_CANDIDATE,
        ExternalDigestionCandidateKind.TOOL_CONTRACT_PATTERN_CANDIDATE: InternalCandidateEmissionKind.EMITTED_INTERNAL_TOOL_CONTRACT_CANDIDATE,
        ExternalDigestionCandidateKind.MISSION_PATTERN_CANDIDATE: InternalCandidateEmissionKind.EMITTED_INTERNAL_MISSION_CANDIDATE,
        ExternalDigestionCandidateKind.MEMORY_SCHEMA_PATTERN_CANDIDATE: InternalCandidateEmissionKind.EMITTED_INTERNAL_MEMORY_SCHEMA_CANDIDATE,
        ExternalDigestionCandidateKind.PROMPT_PATTERN_CANDIDATE: InternalCandidateEmissionKind.EMITTED_INTERNAL_PROMPT_PATTERN_CANDIDATE,
        ExternalDigestionCandidateKind.OCEL_TRACE_PATTERN_CANDIDATE: InternalCandidateEmissionKind.EMITTED_INTERNAL_TRACE_EVENT_PATTERN_CANDIDATE,
        ExternalDigestionCandidateKind.RESULT_ENVELOPE_PATTERN_CANDIDATE: InternalCandidateEmissionKind.EMITTED_INTERNAL_RESULT_ENVELOPE_CANDIDATE,
        ExternalDigestionCandidateKind.APPROVAL_POLICY_PATTERN_CANDIDATE: InternalCandidateEmissionKind.EMITTED_INTERNAL_APPROVAL_BOUNDARY_CANDIDATE,
        ExternalDigestionCandidateKind.PROFILE_PATTERN_CANDIDATE: InternalCandidateEmissionKind.EMITTED_INTERNAL_PROFILE_PATTERN_CANDIDATE,
    }.get(kind, InternalCandidateEmissionKind.UNKNOWN)


def infer_review_requirements_from_pattern_map(pattern_map: ExternalToInternalPatternMap) -> list[InternalCandidateEmissionReviewRequirementKind]:
    reviews = [
        InternalCandidateEmissionReviewRequirementKind.CONTRACT_REVIEW,
        InternalCandidateEmissionReviewRequirementKind.VALIDATION_REVIEW,
        InternalCandidateEmissionReviewRequirementKind.TEST_REVIEW,
    ]
    if "schema" in pattern_map.suggested_internal_candidate_kind:
        reviews.append(InternalCandidateEmissionReviewRequirementKind.SCHEMA_REVIEW)
    if pattern_map.evidence_refs:
        reviews.append(InternalCandidateEmissionReviewRequirementKind.EVIDENCE_REVIEW)
    return reviews


def infer_emission_blockers_from_digestion_candidate(candidate: ExternalHarnessDigestionCandidate) -> list[InternalCandidateEmissionBlockerKind]:
    blockers: list[InternalCandidateEmissionBlockerKind] = []
    if candidate.blockers:
        blockers.append(InternalCandidateEmissionBlockerKind.BLOCKED_DIGESTIBILITY_ASSESSMENT)
    if candidate.ready_for_v0328_dominion_candidate_emitter:
        blockers.append(InternalCandidateEmissionBlockerKind.DOMINION_REQUIRED_ROUTE)
    if candidate.external_to_internal_pattern_map is None:
        blockers.append(InternalCandidateEmissionBlockerKind.MISSING_PATTERN_MAP)
    if not candidate.summary:
        blockers.append(InternalCandidateEmissionBlockerKind.MISSING_CONTRACT_SUMMARY)
    return blockers


def emitted_candidate_preserves_no_activation(candidate: EmittedInternalCandidateBase) -> bool:
    return (
        candidate.ready_for_activation is False
        and candidate.ready_for_skill_activation is False
        and candidate.ready_for_registry_mutation is False
        and candidate.ready_for_memory_mutation is False
        and candidate.ready_for_internalization is False
        and candidate.ready_for_execution is False
        and candidate.active_artifact is False
    )


def external_harness_internal_candidate_set_is_not_registry(candidate_set: ExternalHarnessInternalCandidateSet) -> bool:
    return (
        candidate_set.ready_for_candidate_activation is False
        and candidate_set.ready_for_registry_mutation is False
        and candidate_set.ready_for_internalization is False
        and candidate_set.ready_for_execution is False
        and candidate_set.registry is False
    )


def emission_report_is_not_runtime(report: InternalCandidateEmissionReport) -> bool:
    return (
        report.ready_for_candidate_activation is False
        and report.ready_for_registry_mutation is False
        and report.ready_for_internalization is False
        and report.ready_for_execution is False
        and report.runtime_result is False
        and report.implementation is False
    )


def v0327_readiness_report_is_not_runtime_ready(report: V0327ReadinessReport) -> bool:
    return (
        report.ready_for_execution is False
        and report.ready_for_candidate_activation is False
        and report.ready_for_skill_activation is False
        and report.ready_for_tool_registration is False
        and report.ready_for_tool_invocation is False
        and report.ready_for_mission_installation is False
        and report.ready_for_policy_activation is False
        and report.ready_for_memory_mutation is False
        and report.ready_for_registry_mutation is False
        and report.ready_for_internalization is False
        and report.ready_for_implementation is False
        and report.ready_for_plugin_loading is False
        and report.ready_for_provider_invocation is False
        and report.ready_for_gateway_connection is False
        and report.ready_for_network_access is False
        and report.ready_for_credential_access is False
        and report.ready_for_command_execution is False
    )
