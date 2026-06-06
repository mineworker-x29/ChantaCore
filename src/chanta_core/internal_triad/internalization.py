from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from chanta_core.internal_triad.boundaries import _require_non_blank, _validate_string_list
from chanta_core.internal_triad.digestion import (
    DigestiblePatternSignal,
    DigestionRoute,
    DigestionRouteDecision,
    DigestionSkillOutput,
    V0313_REQUIRED_PROHIBITED_RUNTIME_ACTIONS,
)
from chanta_core.internal_triad.skill_kinds import V0310_TRACK


V0314_VERSION = "v0.31.4"
V0314_RELEASE_NAME = "v0.31.4 Digestion Candidate / Internalization Plan"
V0314_TRACK = V0310_TRACK

V0314_REQUIRED_PROHIBITED_RUNTIME_ACTIONS = [
    *V0313_REQUIRED_PROHIBITED_RUNTIME_ACTIONS,
    "runtime_execution",
    "skill_activation",
    "tool_registration",
    "mission_installation",
    "policy_activation",
    "memory_schema_activation",
    "prompt_pattern_activation",
    "trace_event_handler_activation",
    "runtime_handler_creation",
    "runtime_command_creation",
    "implementation_file_creation",
]

V0314_PROHIBITED_UNTIL_LATER_GATE = [
    "runtime_execution",
    "skill_activation",
    "registry_mutation",
    "tool_registration",
    "mission_installation",
    "policy_activation",
    "memory_mutation",
    "memory_schema_activation",
    "prompt_pattern_activation",
    "trace_event_handler_activation",
    "ocel_event_emission",
    "external_scan",
    "source_ref_fetch",
    "url_fetch",
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
    "dominion_target_creation",
    "dominion_decision_creation",
]


class InternalCandidateKind(StrEnum):
    INTERNAL_SKILL_CANDIDATE = "internal_skill_candidate"
    INTERNAL_TOOL_CONTRACT_CANDIDATE = "internal_tool_contract_candidate"
    INTERNAL_MISSION_CANDIDATE = "internal_mission_candidate"
    INTERNAL_POLICY_CANDIDATE = "internal_policy_candidate"
    INTERNAL_MEMORY_SCHEMA_CANDIDATE = "internal_memory_schema_candidate"
    INTERNAL_PROMPT_PATTERN_CANDIDATE = "internal_prompt_pattern_candidate"
    INTERNAL_TRACE_EVENT_PATTERN_CANDIDATE = "internal_trace_event_pattern_candidate"
    INTERNAL_RESULT_ENVELOPE_CANDIDATE = "internal_result_envelope_candidate"
    INTERNAL_PROFILE_PATTERN_CANDIDATE = "internal_profile_pattern_candidate"
    INTERNAL_APPROVAL_BOUNDARY_CANDIDATE = "internal_approval_boundary_candidate"
    UNKNOWN = "unknown"


class InternalCandidateStatus(StrEnum):
    UNKNOWN = "unknown"
    CANDIDATE = "candidate"
    REQUIRES_REVIEW = "requires_review"
    REQUIRES_MORE_EVIDENCE = "requires_more_evidence"
    DEFERRED = "deferred"
    REJECTED = "rejected"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class InternalizationPlanStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    PLAN_READY = "plan_ready"
    PLAN_READY_WITH_GAPS = "plan_ready_with_gaps"
    REQUIRES_REVIEW = "requires_review"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class InternalizationPlanStepKind(StrEnum):
    DEFINE_CONTRACT = "define_contract"
    DEFINE_SCHEMA = "define_schema"
    DEFINE_VALIDATION = "define_validation"
    DEFINE_TEST = "define_test"
    DEFINE_DOC = "define_doc"
    DEFINE_OCEL_TRACE_CONTRACT = "define_ocel_trace_contract"
    DEFINE_REVIEW_GATE = "define_review_gate"
    DEFINE_NO_OP_PATH = "define_no_op_path"
    DEFINE_FUTURE_GATE = "define_future_gate"
    UNKNOWN = "unknown"


class InternalizationReviewRequirementKind(StrEnum):
    EVIDENCE_REVIEW = "evidence_review"
    BOUNDARY_REVIEW = "boundary_review"
    SAFETY_REVIEW = "safety_review"
    OCEL_TRACE_REVIEW = "ocel_trace_review"
    TEST_REVIEW = "test_review"
    DOCUMENTATION_REVIEW = "documentation_review"
    HUMAN_REVIEW = "human_review"
    FUTURE_GATE_REVIEW = "future_gate_review"
    UNKNOWN = "unknown"


class InternalCandidateRiskKind(StrEnum):
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    UNSAFE_RUNTIME_SURFACE = "unsafe_runtime_surface"
    REGISTRY_MUTATION_RISK = "registry_mutation_risk"
    TOOL_EXECUTION_RISK = "tool_execution_risk"
    MEMORY_MUTATION_RISK = "memory_mutation_risk"
    POLICY_ACTIVATION_RISK = "policy_activation_risk"
    MISSION_INSTALLATION_RISK = "mission_installation_risk"
    PROMPT_INJECTION_RISK = "prompt_injection_risk"
    OCEL_SCHEMA_DRIFT_RISK = "ocel_schema_drift_risk"
    EXTERNAL_DEPENDENCY_RISK = "external_dependency_risk"
    PROVIDER_NETWORK_CREDENTIAL_RISK = "provider_network_credential_risk"
    COMMAND_BROWSER_RPA_GATEWAY_RISK = "command_browser_rpa_gateway_risk"
    INCOMPATIBLE_WITH_OCEL_SPINE = "incompatible_with_ocel_spine"
    UNKNOWN = "unknown"


def _metadata_flag_true(metadata: dict[str, Any], names: set[str]) -> bool:
    return isinstance(metadata, dict) and any(metadata.get(name) is True for name in names)


def _validate_object_list(name: str, values: list[Any], expected_type: type) -> None:
    if not isinstance(values, list) or not all(isinstance(item, expected_type) for item in values):
        raise TypeError(f"{name} must be list[{expected_type.__name__}]")


def _validate_version_includes_v0314(version: str) -> None:
    _require_non_blank("version", version)
    if V0314_VERSION not in version:
        raise ValueError("version must include v0.31.4")


def _validate_prohibited_actions(actions: list[str]) -> None:
    _validate_string_list("prohibited_runtime_actions", actions)
    missing = set(V0314_REQUIRED_PROHIBITED_RUNTIME_ACTIONS) - set(actions)
    if missing:
        raise ValueError(f"prohibited_runtime_actions missing v0.31.4 prohibitions: {sorted(missing)}")


def normalize_internal_candidate_kind(value: InternalCandidateKind | str) -> InternalCandidateKind:
    if isinstance(value, InternalCandidateKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("internal candidate kind must not be blank")
        return InternalCandidateKind(stripped)
    raise TypeError(f"unsupported internal candidate kind: {value!r}")


def normalize_internal_candidate_status(value: InternalCandidateStatus | str) -> InternalCandidateStatus:
    if isinstance(value, InternalCandidateStatus):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("internal candidate status must not be blank")
        return InternalCandidateStatus(stripped)
    raise TypeError(f"unsupported internal candidate status: {value!r}")


def normalize_internalization_plan_status(value: InternalizationPlanStatus | str) -> InternalizationPlanStatus:
    if isinstance(value, InternalizationPlanStatus):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("internalization plan status must not be blank")
        return InternalizationPlanStatus(stripped)
    raise TypeError(f"unsupported internalization plan status: {value!r}")


def normalize_internalization_plan_step_kind(value: InternalizationPlanStepKind | str) -> InternalizationPlanStepKind:
    if isinstance(value, InternalizationPlanStepKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("internalization plan step kind must not be blank")
        return InternalizationPlanStepKind(stripped)
    raise TypeError(f"unsupported internalization plan step kind: {value!r}")


def normalize_internalization_review_requirement_kind(
    value: InternalizationReviewRequirementKind | str,
) -> InternalizationReviewRequirementKind:
    if isinstance(value, InternalizationReviewRequirementKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("internalization review requirement kind must not be blank")
        return InternalizationReviewRequirementKind(stripped)
    raise TypeError(f"unsupported internalization review requirement kind: {value!r}")


def normalize_internal_candidate_risk_kind(value: InternalCandidateRiskKind | str) -> InternalCandidateRiskKind:
    if isinstance(value, InternalCandidateRiskKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("internal candidate risk kind must not be blank")
        return InternalCandidateRiskKind(stripped)
    raise TypeError(f"unsupported internal candidate risk kind: {value!r}")


def internal_candidate_kind_creates_active_artifact(_: InternalCandidateKind | str) -> bool:
    normalize_internal_candidate_kind(_)
    return False


@dataclass(frozen=True)
class InternalCandidateSourceRef:
    source_ref_id: str
    source_kind: str
    source_id: str
    target_id: str | None = None
    capability_entry_id: str | None = None
    digestion_signal_id: str | None = None
    route_decision_id: str | None = None
    evidence_ref_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        _require_non_blank("source_kind", self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _validate_string_list("evidence_ref_ids", self.evidence_ref_ids)
        if _metadata_flag_true(self.metadata, {"source_fetch", "source_ref_fetch", "url_fetch"}):
            raise ValueError("InternalCandidateSourceRef must not imply source fetch")

    @property
    def fetches_source(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalCandidateEvidenceRef:
    evidence_ref_id: str
    source_evidence_ref_id: str | None
    evidence_kind: str
    evidence_summary: str
    quality: str
    limitations: list[str] = field(default_factory=list)
    conflict_notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("evidence_ref_id", self.evidence_ref_id)
        _require_non_blank("evidence_kind", self.evidence_kind)
        _require_non_blank("evidence_summary", self.evidence_summary)
        _require_non_blank("quality", self.quality)
        _validate_string_list("limitations", self.limitations)
        _validate_string_list("conflict_notes", self.conflict_notes)
        if _metadata_flag_true(self.metadata, {"runtime_trust", "execution_evidence"}):
            raise ValueError("InternalCandidateEvidenceRef must not imply runtime trust")

    @property
    def runtime_trust(self) -> bool:
        return False


def _validate_candidate_base(candidate: Any, expected_kind: InternalCandidateKind) -> None:
    _require_non_blank("candidate_id", candidate.candidate_id)
    kind = normalize_internal_candidate_kind(candidate.candidate_kind)
    if kind is not expected_kind:
        raise ValueError(f"candidate_kind must be {expected_kind.value}")
    normalize_internal_candidate_status(candidate.status)
    _require_non_blank("title", candidate.title)
    _require_non_blank("purpose", candidate.purpose)
    _validate_object_list("source_refs", candidate.source_refs, InternalCandidateSourceRef)
    _validate_object_list("evidence_refs", candidate.evidence_refs, InternalCandidateEvidenceRef)
    _validate_string_list("assumptions", candidate.assumptions)
    _validate_string_list("limitations", candidate.limitations)
    if not isinstance(candidate.risk_kinds, list):
        raise TypeError("risk_kinds must be list[InternalCandidateRiskKind | str]")
    for risk_kind in candidate.risk_kinds:
        normalize_internal_candidate_risk_kind(risk_kind)
    if not isinstance(candidate.required_reviews, list):
        raise TypeError("required_reviews must be list[InternalizationReviewRequirementKind | str]")
    for review_kind in candidate.required_reviews:
        normalize_internalization_review_requirement_kind(review_kind)
    if candidate.ready_for_activation is not False:
        raise ValueError("ready_for_activation must always be False in v0.31.4")
    if candidate.ready_for_registry_mutation is not False:
        raise ValueError("ready_for_registry_mutation must always be False in v0.31.4")
    if candidate.ready_for_execution is not False:
        raise ValueError("ready_for_execution must always be False in v0.31.4")
    if _metadata_flag_true(candidate.metadata, {"active_artifact", "active_skill", "registry_mutation", "execution"}):
        raise ValueError("Internal candidate must not imply active artifact, registry mutation, or execution")


def _candidate_is_inactive(candidate: Any) -> bool:
    return (
        candidate.ready_for_activation is False
        and candidate.ready_for_registry_mutation is False
        and candidate.ready_for_execution is False
    )


@dataclass(frozen=True)
class InternalSkillCandidate:
    candidate_id: str
    candidate_kind: InternalCandidateKind | str
    status: InternalCandidateStatus | str
    title: str
    purpose: str
    source_refs: list[InternalCandidateSourceRef]
    evidence_refs: list[InternalCandidateEvidenceRef]
    assumptions: list[str]
    limitations: list[str]
    risk_kinds: list[InternalCandidateRiskKind | str]
    required_reviews: list[InternalizationReviewRequirementKind | str]
    ready_for_activation: bool
    ready_for_registry_mutation: bool
    ready_for_execution: bool
    proposed_skill_name: str
    proposed_skill_kind: str
    input_contract_summary: str
    output_contract_summary: str
    prohibited_runtime_actions: list[str]
    required_tests: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_candidate_base(self, InternalCandidateKind.INTERNAL_SKILL_CANDIDATE)
        _require_non_blank("proposed_skill_name", self.proposed_skill_name)
        _require_non_blank("proposed_skill_kind", self.proposed_skill_kind)
        _require_non_blank("input_contract_summary", self.input_contract_summary)
        _require_non_blank("output_contract_summary", self.output_contract_summary)
        _validate_prohibited_actions(self.prohibited_runtime_actions)
        _validate_string_list("required_tests", self.required_tests)

    @property
    def active_artifact(self) -> bool:
        return False

    @property
    def active_skill(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalToolContractCandidate:
    candidate_id: str
    candidate_kind: InternalCandidateKind | str
    status: InternalCandidateStatus | str
    title: str
    purpose: str
    source_refs: list[InternalCandidateSourceRef]
    evidence_refs: list[InternalCandidateEvidenceRef]
    assumptions: list[str]
    limitations: list[str]
    risk_kinds: list[InternalCandidateRiskKind | str]
    required_reviews: list[InternalizationReviewRequirementKind | str]
    ready_for_activation: bool
    ready_for_registry_mutation: bool
    ready_for_execution: bool
    proposed_tool_name: str
    tool_contract_summary: str
    input_schema_summary: str
    output_schema_summary: str
    side_effect_policy: str
    prohibited_runtime_actions: list[str]
    required_tests: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_candidate_base(self, InternalCandidateKind.INTERNAL_TOOL_CONTRACT_CANDIDATE)
        _require_non_blank("proposed_tool_name", self.proposed_tool_name)
        _require_non_blank("tool_contract_summary", self.tool_contract_summary)
        _require_non_blank("input_schema_summary", self.input_schema_summary)
        _require_non_blank("output_schema_summary", self.output_schema_summary)
        _require_non_blank("side_effect_policy", self.side_effect_policy)
        if any(term in self.side_effect_policy.lower() for term in ("execute", "run", "invoke", "call provider")):
            raise ValueError("side_effect_policy must not imply execution")
        _validate_prohibited_actions(self.prohibited_runtime_actions)
        _validate_string_list("required_tests", self.required_tests)

    @property
    def registered_tool(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalMissionCandidate:
    candidate_id: str
    candidate_kind: InternalCandidateKind | str
    status: InternalCandidateStatus | str
    title: str
    purpose: str
    source_refs: list[InternalCandidateSourceRef]
    evidence_refs: list[InternalCandidateEvidenceRef]
    assumptions: list[str]
    limitations: list[str]
    risk_kinds: list[InternalCandidateRiskKind | str]
    required_reviews: list[InternalizationReviewRequirementKind | str]
    ready_for_activation: bool
    ready_for_registry_mutation: bool
    ready_for_execution: bool
    proposed_mission_name: str
    schedule_policy_summary: str
    trigger_policy_summary: str
    fresh_session_required: bool
    prohibited_runtime_actions: list[str]
    required_tests: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_candidate_base(self, InternalCandidateKind.INTERNAL_MISSION_CANDIDATE)
        _require_non_blank("proposed_mission_name", self.proposed_mission_name)
        _require_non_blank("schedule_policy_summary", self.schedule_policy_summary)
        _require_non_blank("trigger_policy_summary", self.trigger_policy_summary)
        if not isinstance(self.fresh_session_required, bool):
            raise TypeError("fresh_session_required must be bool")
        _validate_prohibited_actions(self.prohibited_runtime_actions)
        _validate_string_list("required_tests", self.required_tests)

    @property
    def installed_mission(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalPolicyCandidate:
    candidate_id: str
    candidate_kind: InternalCandidateKind | str
    status: InternalCandidateStatus | str
    title: str
    purpose: str
    source_refs: list[InternalCandidateSourceRef]
    evidence_refs: list[InternalCandidateEvidenceRef]
    assumptions: list[str]
    limitations: list[str]
    risk_kinds: list[InternalCandidateRiskKind | str]
    required_reviews: list[InternalizationReviewRequirementKind | str]
    ready_for_activation: bool
    ready_for_registry_mutation: bool
    ready_for_execution: bool
    proposed_policy_name: str
    policy_scope_summary: str
    enforcement_summary: str
    default_decision: str
    prohibited_runtime_actions: list[str]
    required_tests: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_candidate_base(self, InternalCandidateKind.INTERNAL_POLICY_CANDIDATE)
        _require_non_blank("proposed_policy_name", self.proposed_policy_name)
        _require_non_blank("policy_scope_summary", self.policy_scope_summary)
        _require_non_blank("enforcement_summary", self.enforcement_summary)
        _require_non_blank("default_decision", self.default_decision)
        if _metadata_flag_true(self.metadata, {"policy_activation", "enforcement_execution"}):
            raise ValueError("InternalPolicyCandidate must not imply policy activation")
        _validate_prohibited_actions(self.prohibited_runtime_actions)
        _validate_string_list("required_tests", self.required_tests)

    @property
    def active_policy(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalMemorySchemaCandidate:
    candidate_id: str
    candidate_kind: InternalCandidateKind | str
    status: InternalCandidateStatus | str
    title: str
    purpose: str
    source_refs: list[InternalCandidateSourceRef]
    evidence_refs: list[InternalCandidateEvidenceRef]
    assumptions: list[str]
    limitations: list[str]
    risk_kinds: list[InternalCandidateRiskKind | str]
    required_reviews: list[InternalizationReviewRequirementKind | str]
    ready_for_activation: bool
    ready_for_registry_mutation: bool
    ready_for_execution: bool
    proposed_schema_name: str
    memory_scope_summary: str
    allowed_fields: list[str]
    prohibited_fields: list[str]
    persistence_policy_summary: str
    prohibited_runtime_actions: list[str]
    required_tests: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_candidate_base(self, InternalCandidateKind.INTERNAL_MEMORY_SCHEMA_CANDIDATE)
        _require_non_blank("proposed_schema_name", self.proposed_schema_name)
        _require_non_blank("memory_scope_summary", self.memory_scope_summary)
        _validate_string_list("allowed_fields", self.allowed_fields)
        _validate_string_list("prohibited_fields", self.prohibited_fields)
        _require_non_blank("persistence_policy_summary", self.persistence_policy_summary)
        if _metadata_flag_true(self.metadata, {"memory_writer", "memory_mutation", "persist_memory"}):
            raise ValueError("InternalMemorySchemaCandidate must not write or persist memory")
        _validate_prohibited_actions(self.prohibited_runtime_actions)
        _validate_string_list("required_tests", self.required_tests)

    @property
    def memory_writer(self) -> bool:
        return False

    @property
    def persists_memory(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalPromptPatternCandidate:
    candidate_id: str
    candidate_kind: InternalCandidateKind | str
    status: InternalCandidateStatus | str
    title: str
    purpose: str
    source_refs: list[InternalCandidateSourceRef]
    evidence_refs: list[InternalCandidateEvidenceRef]
    assumptions: list[str]
    limitations: list[str]
    risk_kinds: list[InternalCandidateRiskKind | str]
    required_reviews: list[InternalizationReviewRequirementKind | str]
    ready_for_activation: bool
    ready_for_registry_mutation: bool
    ready_for_execution: bool
    proposed_pattern_name: str
    prompt_scope_summary: str
    insertion_policy_summary: str
    context_budget_notes: list[str]
    prohibited_runtime_actions: list[str]
    required_tests: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_candidate_base(self, InternalCandidateKind.INTERNAL_PROMPT_PATTERN_CANDIDATE)
        _require_non_blank("proposed_pattern_name", self.proposed_pattern_name)
        _require_non_blank("prompt_scope_summary", self.prompt_scope_summary)
        _require_non_blank("insertion_policy_summary", self.insertion_policy_summary)
        _validate_string_list("context_budget_notes", self.context_budget_notes)
        if _metadata_flag_true(self.metadata, {"prompt_injection", "prompt_activation"}):
            raise ValueError("InternalPromptPatternCandidate must not imply prompt injection")
        _validate_prohibited_actions(self.prohibited_runtime_actions)
        _validate_string_list("required_tests", self.required_tests)

    @property
    def prompt_injection(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalTraceEventPatternCandidate:
    candidate_id: str
    candidate_kind: InternalCandidateKind | str
    status: InternalCandidateStatus | str
    title: str
    purpose: str
    source_refs: list[InternalCandidateSourceRef]
    evidence_refs: list[InternalCandidateEvidenceRef]
    assumptions: list[str]
    limitations: list[str]
    risk_kinds: list[InternalCandidateRiskKind | str]
    required_reviews: list[InternalizationReviewRequirementKind | str]
    ready_for_activation: bool
    ready_for_registry_mutation: bool
    ready_for_execution: bool
    proposed_event_type: str
    proposed_object_types: list[str]
    proposed_relation_types: list[str]
    ocel_visibility_summary: str
    prohibited_runtime_actions: list[str]
    required_tests: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_candidate_base(self, InternalCandidateKind.INTERNAL_TRACE_EVENT_PATTERN_CANDIDATE)
        _require_non_blank("proposed_event_type", self.proposed_event_type)
        _validate_string_list("proposed_object_types", self.proposed_object_types)
        _validate_string_list("proposed_relation_types", self.proposed_relation_types)
        _require_non_blank("ocel_visibility_summary", self.ocel_visibility_summary)
        if _metadata_flag_true(self.metadata, {"ocel_event_emission", "trace_handler_activation"}):
            raise ValueError("InternalTraceEventPatternCandidate must not emit OCEL events")
        _validate_prohibited_actions(self.prohibited_runtime_actions)
        _validate_string_list("required_tests", self.required_tests)

    @property
    def emits_ocel_event(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalResultEnvelopeCandidate:
    candidate_id: str
    candidate_kind: InternalCandidateKind | str
    status: InternalCandidateStatus | str
    title: str
    purpose: str
    source_refs: list[InternalCandidateSourceRef]
    evidence_refs: list[InternalCandidateEvidenceRef]
    assumptions: list[str]
    limitations: list[str]
    risk_kinds: list[InternalCandidateRiskKind | str]
    required_reviews: list[InternalizationReviewRequirementKind | str]
    ready_for_activation: bool
    ready_for_registry_mutation: bool
    ready_for_execution: bool
    proposed_envelope_name: str
    required_fields: list[str]
    optional_fields: list[str]
    forbidden_fields: list[str]
    raw_output_allowed: bool = False
    memory_persistence_allowed: bool = False
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(V0314_REQUIRED_PROHIBITED_RUNTIME_ACTIONS))
    required_tests: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_candidate_base(self, InternalCandidateKind.INTERNAL_RESULT_ENVELOPE_CANDIDATE)
        _require_non_blank("proposed_envelope_name", self.proposed_envelope_name)
        for name in ("required_fields", "optional_fields", "forbidden_fields"):
            _validate_string_list(name, getattr(self, name))
        if self.raw_output_allowed is not False:
            raise ValueError("raw_output_allowed must default to False in v0.31.4")
        if self.memory_persistence_allowed is not False:
            raise ValueError("memory_persistence_allowed must default to False in v0.31.4")
        _validate_prohibited_actions(self.prohibited_runtime_actions)
        _validate_string_list("required_tests", self.required_tests)

    @property
    def result_ingestion(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalCandidateSet:
    candidate_set_id: str
    source_digestion_output_id: str | None
    skill_candidates: list[InternalSkillCandidate]
    tool_contract_candidates: list[InternalToolContractCandidate]
    mission_candidates: list[InternalMissionCandidate]
    policy_candidates: list[InternalPolicyCandidate]
    memory_schema_candidates: list[InternalMemorySchemaCandidate]
    prompt_pattern_candidates: list[InternalPromptPatternCandidate]
    trace_event_pattern_candidates: list[InternalTraceEventPatternCandidate]
    result_envelope_candidates: list[InternalResultEnvelopeCandidate]
    rejected_source_refs: list[str]
    deferred_source_refs: list[str]
    dominion_required_source_refs: list[str]
    blocked_source_refs: list[str]
    evidence_refs: list[InternalCandidateEvidenceRef]
    ready_for_activation: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("candidate_set_id", self.candidate_set_id)
        for name, expected_type in (
            ("skill_candidates", InternalSkillCandidate),
            ("tool_contract_candidates", InternalToolContractCandidate),
            ("mission_candidates", InternalMissionCandidate),
            ("policy_candidates", InternalPolicyCandidate),
            ("memory_schema_candidates", InternalMemorySchemaCandidate),
            ("prompt_pattern_candidates", InternalPromptPatternCandidate),
            ("trace_event_pattern_candidates", InternalTraceEventPatternCandidate),
            ("result_envelope_candidates", InternalResultEnvelopeCandidate),
            ("evidence_refs", InternalCandidateEvidenceRef),
        ):
            _validate_object_list(name, getattr(self, name), expected_type)
        for name in ("rejected_source_refs", "deferred_source_refs", "dominion_required_source_refs", "blocked_source_refs"):
            _validate_string_list(name, getattr(self, name))
        if self.ready_for_activation is not False:
            raise ValueError("ready_for_activation must always be False in v0.31.4")
        if self.ready_for_registry_mutation is not False:
            raise ValueError("ready_for_registry_mutation must always be False in v0.31.4")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.4")
        if _metadata_flag_true(self.metadata, {"registry", "registry_mutation", "dominion_target_creation"}):
            raise ValueError("InternalCandidateSet is not registry and must not create dominion targets")

    @property
    def is_registry(self) -> bool:
        return False

    @property
    def creates_dominion_target(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalizationPlanStep:
    step_id: str
    step_kind: InternalizationPlanStepKind | str
    order: int
    title: str
    description: str
    target_candidate_ids: list[str]
    required_reviews: list[InternalizationReviewRequirementKind | str]
    expected_artifacts: list[str]
    explicitly_not_performed: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("step_id", self.step_id)
        normalize_internalization_plan_step_kind(self.step_kind)
        if not isinstance(self.order, int) or self.order < 0:
            raise ValueError("order must be >= 0")
        _require_non_blank("title", self.title)
        _require_non_blank("description", self.description)
        _validate_string_list("target_candidate_ids", self.target_candidate_ids)
        if not isinstance(self.required_reviews, list):
            raise TypeError("required_reviews must be list[InternalizationReviewRequirementKind | str]")
        for review_kind in self.required_reviews:
            normalize_internalization_review_requirement_kind(review_kind)
        _validate_string_list("expected_artifacts", self.expected_artifacts)
        _validate_string_list("explicitly_not_performed", self.explicitly_not_performed)
        if _metadata_flag_true(self.metadata, {"execution_step", "implementation_execution"}):
            raise ValueError("InternalizationPlanStep must not imply execution")

    @property
    def executes_step(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalizationReviewRequirement:
    review_requirement_id: str
    requirement_kind: InternalizationReviewRequirementKind | str
    target_candidate_ids: list[str]
    reason: str
    required_evidence_refs: list[str]
    required_reviewer_refs: list[str]
    blocks_activation: bool = True
    blocks_registry_mutation: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("review_requirement_id", self.review_requirement_id)
        normalize_internalization_review_requirement_kind(self.requirement_kind)
        _validate_string_list("target_candidate_ids", self.target_candidate_ids)
        _require_non_blank("reason", self.reason)
        _validate_string_list("required_evidence_refs", self.required_evidence_refs)
        _validate_string_list("required_reviewer_refs", self.required_reviewer_refs)
        if not isinstance(self.blocks_activation, bool):
            raise TypeError("blocks_activation must be bool")
        if not isinstance(self.blocks_registry_mutation, bool):
            raise TypeError("blocks_registry_mutation must be bool")
        if _metadata_flag_true(self.metadata, {"approval_granted", "activation_approved"}):
            raise ValueError("InternalizationReviewRequirement is not approval")

    @property
    def approval_granted(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalizationPlan:
    plan_id: str
    source_candidate_set_id: str
    status: InternalizationPlanStatus | str
    summary: str
    plan_steps: list[InternalizationPlanStep]
    review_requirements: list[InternalizationReviewRequirement]
    candidate_ids: list[str]
    blocked_candidate_ids: list[str]
    deferred_candidate_ids: list[str]
    future_track_candidate_ids: list[str]
    explicitly_out_of_scope: list[str]
    no_execution_guarantee: bool = True
    no_registry_mutation_guarantee: bool = True
    no_skill_activation_guarantee: bool = True
    no_tool_registration_guarantee: bool = True
    no_mission_installation_guarantee: bool = True
    no_policy_activation_guarantee: bool = True
    no_memory_mutation_guarantee: bool = True
    ready_for_activation: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[InternalCandidateEvidenceRef] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("plan_id", self.plan_id)
        _require_non_blank("source_candidate_set_id", self.source_candidate_set_id)
        status = normalize_internalization_plan_status(self.status)
        _require_non_blank("summary", self.summary)
        _validate_object_list("plan_steps", self.plan_steps, InternalizationPlanStep)
        _validate_object_list("review_requirements", self.review_requirements, InternalizationReviewRequirement)
        for name in ("candidate_ids", "blocked_candidate_ids", "deferred_candidate_ids", "future_track_candidate_ids", "explicitly_out_of_scope"):
            _validate_string_list(name, getattr(self, name))
        for name in (
            "no_execution_guarantee",
            "no_registry_mutation_guarantee",
            "no_skill_activation_guarantee",
            "no_tool_registration_guarantee",
            "no_mission_installation_guarantee",
            "no_policy_activation_guarantee",
            "no_memory_mutation_guarantee",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.31.4")
        if status is InternalizationPlanStatus.PLAN_READY_WITH_GAPS and not (self.blocked_candidate_ids or self.deferred_candidate_ids):
            raise ValueError("plan_ready_with_gaps requires explicit gaps")
        if self.ready_for_activation is not False:
            raise ValueError("ready_for_activation must always be False in v0.31.4")
        if self.ready_for_registry_mutation is not False:
            raise ValueError("ready_for_registry_mutation must always be False in v0.31.4")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.4")
        _validate_object_list("evidence_refs", self.evidence_refs, InternalCandidateEvidenceRef)
        _validate_string_list("withdrawal_conditions", self.withdrawal_conditions)
        if _metadata_flag_true(self.metadata, {"implementation", "implementation_execution", "runtime_integration"}):
            raise ValueError("InternalizationPlan must not imply implementation")

    @property
    def is_implementation(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalizationNoOpDecision:
    no_op_id: str
    source_candidate_set_id: str | None
    reason: str
    blocked_reasons: list[str] = field(default_factory=list)
    safe_alternatives: list[str] = field(default_factory=list)
    evidence_refs: list[InternalCandidateEvidenceRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("no_op_id", self.no_op_id)
        _require_non_blank("reason", self.reason)
        _validate_string_list("blocked_reasons", self.blocked_reasons)
        _validate_string_list("safe_alternatives", self.safe_alternatives)
        _validate_object_list("evidence_refs", self.evidence_refs, InternalCandidateEvidenceRef)

    @property
    def is_failure(self) -> bool:
        return False

    @property
    def executes_anything(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalizationRunPreview:
    run_preview_id: str
    source_candidate_set_id: str | None
    planned_steps: list[str]
    expected_artifacts: list[str]
    explicitly_not_performed: list[str]
    no_execution_guarantee: bool = True
    no_registry_mutation_guarantee: bool = True
    no_skill_activation_guarantee: bool = True
    no_tool_registration_guarantee: bool = True
    no_mission_installation_guarantee: bool = True
    no_policy_activation_guarantee: bool = True
    no_memory_mutation_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        _validate_string_list("planned_steps", self.planned_steps)
        _validate_string_list("expected_artifacts", self.expected_artifacts)
        _validate_string_list("explicitly_not_performed", self.explicitly_not_performed)
        for name in (
            "no_execution_guarantee",
            "no_registry_mutation_guarantee",
            "no_skill_activation_guarantee",
            "no_tool_registration_guarantee",
            "no_mission_installation_guarantee",
            "no_policy_activation_guarantee",
            "no_memory_mutation_guarantee",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.31.4")
        if _metadata_flag_true(self.metadata, {"executes_run", "implementation_execution"}):
            raise ValueError("InternalizationRunPreview must not imply execution")

    @property
    def executes_run(self) -> bool:
        return False


@dataclass(frozen=True)
class V0314ReadinessReport:
    report_id: str
    version: str
    candidate_set_id: str | None
    internalization_plan_id: str | None
    summary: str
    ready_for_v0315_dominion_skill_foundation: bool
    ready_for_v0316_dominion_target_decision: bool
    ready_for_activation: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_execution: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    deferred_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(V0314_PROHIBITED_UNTIL_LATER_GATE))
    evidence_refs: list[InternalCandidateEvidenceRef] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0314(self.version)
        _require_non_blank("summary", self.summary)
        if self.ready_for_activation is not False:
            raise ValueError("ready_for_activation must always be False in v0.31.4")
        if self.ready_for_registry_mutation is not False:
            raise ValueError("ready_for_registry_mutation must always be False in v0.31.4")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.4")
        for name in ("completed_items", "blocked_items", "deferred_items", "future_track_items", "prohibited_until_later_gate", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_object_list("evidence_refs", self.evidence_refs, InternalCandidateEvidenceRef)
        missing = set(V0314_PROHIBITED_UNTIL_LATER_GATE) - set(self.prohibited_until_later_gate)
        if missing:
            raise ValueError(f"prohibited_until_later_gate missing required items: {sorted(missing)}")
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "activation_readiness", "registry_mutation_readiness"}):
            raise ValueError("V0314ReadinessReport must not imply runtime enablement")

    @property
    def runtime_enablement(self) -> bool:
        return False


def build_internal_candidate_source_ref(
    source_ref_id: str,
    source_kind: str,
    source_id: str,
    target_id: str | None = None,
    capability_entry_id: str | None = None,
    digestion_signal_id: str | None = None,
    route_decision_id: str | None = None,
    evidence_ref_ids: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> InternalCandidateSourceRef:
    return InternalCandidateSourceRef(
        source_ref_id=source_ref_id,
        source_kind=source_kind,
        source_id=source_id,
        target_id=target_id,
        capability_entry_id=capability_entry_id,
        digestion_signal_id=digestion_signal_id,
        route_decision_id=route_decision_id,
        evidence_ref_ids=list(evidence_ref_ids or []),
        metadata=dict(metadata or {}),
    )


def build_internal_candidate_evidence_ref(
    evidence_ref_id: str,
    evidence_kind: str,
    evidence_summary: str,
    quality: str = "unknown",
    source_evidence_ref_id: str | None = None,
    limitations: list[str] | None = None,
    conflict_notes: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> InternalCandidateEvidenceRef:
    return InternalCandidateEvidenceRef(
        evidence_ref_id=evidence_ref_id,
        source_evidence_ref_id=source_evidence_ref_id,
        evidence_kind=evidence_kind,
        evidence_summary=evidence_summary,
        quality=quality,
        limitations=list(limitations or []),
        conflict_notes=list(conflict_notes or []),
        metadata=dict(metadata or {}),
    )


def _candidate_base_kwargs(
    candidate_id: str,
    candidate_kind: InternalCandidateKind,
    title: str,
    purpose: str,
    status: InternalCandidateStatus | str = InternalCandidateStatus.CANDIDATE,
    source_refs: list[InternalCandidateSourceRef] | None = None,
    evidence_refs: list[InternalCandidateEvidenceRef] | None = None,
    assumptions: list[str] | None = None,
    limitations: list[str] | None = None,
    risk_kinds: list[InternalCandidateRiskKind | str] | None = None,
    required_reviews: list[InternalizationReviewRequirementKind | str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "candidate_id": candidate_id,
        "candidate_kind": candidate_kind,
        "status": status,
        "title": title,
        "purpose": purpose,
        "source_refs": list(source_refs or []),
        "evidence_refs": list(evidence_refs or []),
        "assumptions": list(assumptions or []),
        "limitations": list(limitations or []),
        "risk_kinds": list(risk_kinds or []),
        "required_reviews": list(required_reviews or []),
        "ready_for_activation": False,
        "ready_for_registry_mutation": False,
        "ready_for_execution": False,
        "metadata": dict(metadata or {}),
    }


def build_internal_skill_candidate(
    candidate_id: str,
    title: str,
    purpose: str,
    proposed_skill_name: str,
    proposed_skill_kind: str = "contract_only",
    input_contract_summary: str = "candidate input contract only",
    output_contract_summary: str = "candidate output contract only",
    prohibited_runtime_actions: list[str] | None = None,
    required_tests: list[str] | None = None,
    **base_kwargs: Any,
) -> InternalSkillCandidate:
    return InternalSkillCandidate(
        **_candidate_base_kwargs(candidate_id, InternalCandidateKind.INTERNAL_SKILL_CANDIDATE, title, purpose, **base_kwargs),
        proposed_skill_name=proposed_skill_name,
        proposed_skill_kind=proposed_skill_kind,
        input_contract_summary=input_contract_summary,
        output_contract_summary=output_contract_summary,
        prohibited_runtime_actions=list(prohibited_runtime_actions or V0314_REQUIRED_PROHIBITED_RUNTIME_ACTIONS),
        required_tests=list(required_tests or []),
    )


def build_internal_tool_contract_candidate(
    candidate_id: str,
    title: str,
    purpose: str,
    proposed_tool_name: str,
    tool_contract_summary: str = "candidate tool contract only",
    input_schema_summary: str = "candidate input schema",
    output_schema_summary: str = "candidate output schema",
    side_effect_policy: str = "no side effects; design review only",
    prohibited_runtime_actions: list[str] | None = None,
    required_tests: list[str] | None = None,
    **base_kwargs: Any,
) -> InternalToolContractCandidate:
    return InternalToolContractCandidate(
        **_candidate_base_kwargs(candidate_id, InternalCandidateKind.INTERNAL_TOOL_CONTRACT_CANDIDATE, title, purpose, **base_kwargs),
        proposed_tool_name=proposed_tool_name,
        tool_contract_summary=tool_contract_summary,
        input_schema_summary=input_schema_summary,
        output_schema_summary=output_schema_summary,
        side_effect_policy=side_effect_policy,
        prohibited_runtime_actions=list(prohibited_runtime_actions or V0314_REQUIRED_PROHIBITED_RUNTIME_ACTIONS),
        required_tests=list(required_tests or []),
    )


def build_internal_mission_candidate(
    candidate_id: str,
    title: str,
    purpose: str,
    proposed_mission_name: str,
    schedule_policy_summary: str = "no installed schedule",
    trigger_policy_summary: str = "no active trigger",
    fresh_session_required: bool = True,
    prohibited_runtime_actions: list[str] | None = None,
    required_tests: list[str] | None = None,
    **base_kwargs: Any,
) -> InternalMissionCandidate:
    return InternalMissionCandidate(
        **_candidate_base_kwargs(candidate_id, InternalCandidateKind.INTERNAL_MISSION_CANDIDATE, title, purpose, **base_kwargs),
        proposed_mission_name=proposed_mission_name,
        schedule_policy_summary=schedule_policy_summary,
        trigger_policy_summary=trigger_policy_summary,
        fresh_session_required=fresh_session_required,
        prohibited_runtime_actions=list(prohibited_runtime_actions or V0314_REQUIRED_PROHIBITED_RUNTIME_ACTIONS),
        required_tests=list(required_tests or []),
    )


def build_internal_policy_candidate(
    candidate_id: str,
    title: str,
    purpose: str,
    proposed_policy_name: str,
    policy_scope_summary: str = "candidate policy scope",
    enforcement_summary: str = "descriptive enforcement contract only",
    default_decision: str = "deny",
    prohibited_runtime_actions: list[str] | None = None,
    required_tests: list[str] | None = None,
    **base_kwargs: Any,
) -> InternalPolicyCandidate:
    return InternalPolicyCandidate(
        **_candidate_base_kwargs(candidate_id, InternalCandidateKind.INTERNAL_POLICY_CANDIDATE, title, purpose, **base_kwargs),
        proposed_policy_name=proposed_policy_name,
        policy_scope_summary=policy_scope_summary,
        enforcement_summary=enforcement_summary,
        default_decision=default_decision,
        prohibited_runtime_actions=list(prohibited_runtime_actions or V0314_REQUIRED_PROHIBITED_RUNTIME_ACTIONS),
        required_tests=list(required_tests or []),
    )


def build_internal_memory_schema_candidate(
    candidate_id: str,
    title: str,
    purpose: str,
    proposed_schema_name: str,
    memory_scope_summary: str = "candidate memory schema only",
    allowed_fields: list[str] | None = None,
    prohibited_fields: list[str] | None = None,
    persistence_policy_summary: str = "no persistence in v0.31.4",
    prohibited_runtime_actions: list[str] | None = None,
    required_tests: list[str] | None = None,
    **base_kwargs: Any,
) -> InternalMemorySchemaCandidate:
    return InternalMemorySchemaCandidate(
        **_candidate_base_kwargs(candidate_id, InternalCandidateKind.INTERNAL_MEMORY_SCHEMA_CANDIDATE, title, purpose, **base_kwargs),
        proposed_schema_name=proposed_schema_name,
        memory_scope_summary=memory_scope_summary,
        allowed_fields=list(allowed_fields or []),
        prohibited_fields=list(prohibited_fields or []),
        persistence_policy_summary=persistence_policy_summary,
        prohibited_runtime_actions=list(prohibited_runtime_actions or V0314_REQUIRED_PROHIBITED_RUNTIME_ACTIONS),
        required_tests=list(required_tests or []),
    )


def build_internal_prompt_pattern_candidate(
    candidate_id: str,
    title: str,
    purpose: str,
    proposed_pattern_name: str,
    prompt_scope_summary: str = "candidate prompt pattern only",
    insertion_policy_summary: str = "no insertion or activation",
    context_budget_notes: list[str] | None = None,
    prohibited_runtime_actions: list[str] | None = None,
    required_tests: list[str] | None = None,
    **base_kwargs: Any,
) -> InternalPromptPatternCandidate:
    return InternalPromptPatternCandidate(
        **_candidate_base_kwargs(candidate_id, InternalCandidateKind.INTERNAL_PROMPT_PATTERN_CANDIDATE, title, purpose, **base_kwargs),
        proposed_pattern_name=proposed_pattern_name,
        prompt_scope_summary=prompt_scope_summary,
        insertion_policy_summary=insertion_policy_summary,
        context_budget_notes=list(context_budget_notes or []),
        prohibited_runtime_actions=list(prohibited_runtime_actions or V0314_REQUIRED_PROHIBITED_RUNTIME_ACTIONS),
        required_tests=list(required_tests or []),
    )


def build_internal_trace_event_pattern_candidate(
    candidate_id: str,
    title: str,
    purpose: str,
    proposed_event_type: str,
    proposed_object_types: list[str] | None = None,
    proposed_relation_types: list[str] | None = None,
    ocel_visibility_summary: str = "candidate OCEL trace contract only",
    prohibited_runtime_actions: list[str] | None = None,
    required_tests: list[str] | None = None,
    **base_kwargs: Any,
) -> InternalTraceEventPatternCandidate:
    return InternalTraceEventPatternCandidate(
        **_candidate_base_kwargs(candidate_id, InternalCandidateKind.INTERNAL_TRACE_EVENT_PATTERN_CANDIDATE, title, purpose, **base_kwargs),
        proposed_event_type=proposed_event_type,
        proposed_object_types=list(proposed_object_types or []),
        proposed_relation_types=list(proposed_relation_types or []),
        ocel_visibility_summary=ocel_visibility_summary,
        prohibited_runtime_actions=list(prohibited_runtime_actions or V0314_REQUIRED_PROHIBITED_RUNTIME_ACTIONS),
        required_tests=list(required_tests or []),
    )


def build_internal_result_envelope_candidate(
    candidate_id: str,
    title: str,
    purpose: str,
    proposed_envelope_name: str,
    required_fields: list[str] | None = None,
    optional_fields: list[str] | None = None,
    forbidden_fields: list[str] | None = None,
    prohibited_runtime_actions: list[str] | None = None,
    required_tests: list[str] | None = None,
    **base_kwargs: Any,
) -> InternalResultEnvelopeCandidate:
    return InternalResultEnvelopeCandidate(
        **_candidate_base_kwargs(candidate_id, InternalCandidateKind.INTERNAL_RESULT_ENVELOPE_CANDIDATE, title, purpose, **base_kwargs),
        proposed_envelope_name=proposed_envelope_name,
        required_fields=list(required_fields or []),
        optional_fields=list(optional_fields or []),
        forbidden_fields=list(forbidden_fields or []),
        raw_output_allowed=False,
        memory_persistence_allowed=False,
        prohibited_runtime_actions=list(prohibited_runtime_actions or V0314_REQUIRED_PROHIBITED_RUNTIME_ACTIONS),
        required_tests=list(required_tests or []),
    )


def build_internal_candidate_set(
    candidate_set_id: str,
    source_digestion_output_id: str | None = None,
    skill_candidates: list[InternalSkillCandidate] | None = None,
    tool_contract_candidates: list[InternalToolContractCandidate] | None = None,
    mission_candidates: list[InternalMissionCandidate] | None = None,
    policy_candidates: list[InternalPolicyCandidate] | None = None,
    memory_schema_candidates: list[InternalMemorySchemaCandidate] | None = None,
    prompt_pattern_candidates: list[InternalPromptPatternCandidate] | None = None,
    trace_event_pattern_candidates: list[InternalTraceEventPatternCandidate] | None = None,
    result_envelope_candidates: list[InternalResultEnvelopeCandidate] | None = None,
    rejected_source_refs: list[str] | None = None,
    deferred_source_refs: list[str] | None = None,
    dominion_required_source_refs: list[str] | None = None,
    blocked_source_refs: list[str] | None = None,
    evidence_refs: list[InternalCandidateEvidenceRef] | None = None,
    digestion_output: DigestionSkillOutput | None = None,
    metadata: dict[str, Any] | None = None,
) -> InternalCandidateSet:
    resolved_digestion_output_id = source_digestion_output_id
    resolved_dominion_refs = list(dominion_required_source_refs or [])
    resolved_blocked_refs = list(blocked_source_refs or [])
    if digestion_output is not None:
        resolved_digestion_output_id = digestion_output.digestion_output_id
        resolved_dominion_refs.extend(digestion_output.dominion_required_signal_ids)
        resolved_blocked_refs.extend(digestion_output.blocked_signal_ids)
    return InternalCandidateSet(
        candidate_set_id=candidate_set_id,
        source_digestion_output_id=resolved_digestion_output_id,
        skill_candidates=list(skill_candidates or []),
        tool_contract_candidates=list(tool_contract_candidates or []),
        mission_candidates=list(mission_candidates or []),
        policy_candidates=list(policy_candidates or []),
        memory_schema_candidates=list(memory_schema_candidates or []),
        prompt_pattern_candidates=list(prompt_pattern_candidates or []),
        trace_event_pattern_candidates=list(trace_event_pattern_candidates or []),
        result_envelope_candidates=list(result_envelope_candidates or []),
        rejected_source_refs=list(rejected_source_refs or []),
        deferred_source_refs=list(deferred_source_refs or []),
        dominion_required_source_refs=resolved_dominion_refs,
        blocked_source_refs=resolved_blocked_refs,
        evidence_refs=list(evidence_refs or []),
        ready_for_activation=False,
        ready_for_registry_mutation=False,
        ready_for_execution=False,
        metadata=dict(metadata or {}),
    )


def build_internalization_plan_step(
    step_id: str,
    step_kind: InternalizationPlanStepKind | str,
    order: int,
    title: str,
    description: str,
    target_candidate_ids: list[str] | None = None,
    required_reviews: list[InternalizationReviewRequirementKind | str] | None = None,
    expected_artifacts: list[str] | None = None,
    explicitly_not_performed: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> InternalizationPlanStep:
    return InternalizationPlanStep(
        step_id=step_id,
        step_kind=step_kind,
        order=order,
        title=title,
        description=description,
        target_candidate_ids=list(target_candidate_ids or []),
        required_reviews=list(required_reviews or []),
        expected_artifacts=list(expected_artifacts or []),
        explicitly_not_performed=list(explicitly_not_performed or ["execution", "registry_mutation", "activation"]),
        metadata=dict(metadata or {}),
    )


def build_internalization_review_requirement(
    review_requirement_id: str,
    requirement_kind: InternalizationReviewRequirementKind | str,
    reason: str,
    target_candidate_ids: list[str] | None = None,
    required_evidence_refs: list[str] | None = None,
    required_reviewer_refs: list[str] | None = None,
    blocks_activation: bool = True,
    blocks_registry_mutation: bool = True,
    metadata: dict[str, Any] | None = None,
) -> InternalizationReviewRequirement:
    return InternalizationReviewRequirement(
        review_requirement_id=review_requirement_id,
        requirement_kind=requirement_kind,
        target_candidate_ids=list(target_candidate_ids or []),
        reason=reason,
        required_evidence_refs=list(required_evidence_refs or []),
        required_reviewer_refs=list(required_reviewer_refs or []),
        blocks_activation=blocks_activation,
        blocks_registry_mutation=blocks_registry_mutation,
        metadata=dict(metadata or {}),
    )


def build_internalization_plan(
    plan_id: str,
    source_candidate_set_id: str,
    status: InternalizationPlanStatus | str,
    summary: str,
    plan_steps: list[InternalizationPlanStep] | None = None,
    review_requirements: list[InternalizationReviewRequirement] | None = None,
    candidate_ids: list[str] | None = None,
    blocked_candidate_ids: list[str] | None = None,
    deferred_candidate_ids: list[str] | None = None,
    future_track_candidate_ids: list[str] | None = None,
    explicitly_out_of_scope: list[str] | None = None,
    evidence_refs: list[InternalCandidateEvidenceRef] | None = None,
    withdrawal_conditions: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> InternalizationPlan:
    return InternalizationPlan(
        plan_id=plan_id,
        source_candidate_set_id=source_candidate_set_id,
        status=status,
        summary=summary,
        plan_steps=list(plan_steps or []),
        review_requirements=list(review_requirements or []),
        candidate_ids=list(candidate_ids or []),
        blocked_candidate_ids=list(blocked_candidate_ids or []),
        deferred_candidate_ids=list(deferred_candidate_ids or []),
        future_track_candidate_ids=list(future_track_candidate_ids or []),
        explicitly_out_of_scope=list(explicitly_out_of_scope or []),
        ready_for_activation=False,
        ready_for_registry_mutation=False,
        ready_for_execution=False,
        evidence_refs=list(evidence_refs or []),
        withdrawal_conditions=list(withdrawal_conditions or []),
        metadata=dict(metadata or {}),
    )


def build_internalization_no_op_decision(
    no_op_id: str,
    reason: str,
    source_candidate_set_id: str | None = None,
    blocked_reasons: list[str] | None = None,
    safe_alternatives: list[str] | None = None,
    evidence_refs: list[InternalCandidateEvidenceRef] | None = None,
    metadata: dict[str, Any] | None = None,
) -> InternalizationNoOpDecision:
    return InternalizationNoOpDecision(
        no_op_id=no_op_id,
        source_candidate_set_id=source_candidate_set_id,
        reason=reason,
        blocked_reasons=list(blocked_reasons or []),
        safe_alternatives=list(safe_alternatives or []),
        evidence_refs=list(evidence_refs or []),
        metadata=dict(metadata or {}),
    )


def build_internalization_run_preview(
    run_preview_id: str,
    source_candidate_set_id: str | None = None,
    planned_steps: list[str] | None = None,
    expected_artifacts: list[str] | None = None,
    explicitly_not_performed: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> InternalizationRunPreview:
    return InternalizationRunPreview(
        run_preview_id=run_preview_id,
        source_candidate_set_id=source_candidate_set_id,
        planned_steps=list(planned_steps or ["structure candidate set", "draft internalization plan"]),
        expected_artifacts=list(expected_artifacts or ["InternalCandidateSet", "InternalizationPlan"]),
        explicitly_not_performed=list(
            explicitly_not_performed
            or [
                "execution",
                "registry_mutation",
                "skill_activation",
                "tool_registration",
                "mission_installation",
                "policy_activation",
                "memory_mutation",
            ]
        ),
        metadata=dict(metadata or {}),
    )


def build_v0314_readiness_report(
    candidate_set: InternalCandidateSet | None = None,
    internalization_plan: InternalizationPlan | None = None,
    ready_for_v0315_dominion_skill_foundation: bool = True,
    ready_for_v0316_dominion_target_decision: bool = False,
) -> V0314ReadinessReport:
    return V0314ReadinessReport(
        report_id="v0314_readiness_report:digestion_candidate_internalization_plan",
        version=V0314_VERSION,
        candidate_set_id=candidate_set.candidate_set_id if candidate_set is not None else None,
        internalization_plan_id=internalization_plan.plan_id if internalization_plan is not None else None,
        summary="v0.31.4 creates reviewable internal candidate and plan artifacts only; no activation, registry mutation, or execution.",
        ready_for_v0315_dominion_skill_foundation=ready_for_v0315_dominion_skill_foundation,
        ready_for_v0316_dominion_target_decision=ready_for_v0316_dominion_target_decision,
        ready_for_activation=False,
        ready_for_registry_mutation=False,
        ready_for_execution=False,
        completed_items=[
            "internal candidate taxonomy",
            "internal candidate models",
            "candidate set model",
            "internalization plan model",
            "run preview and no-op models",
        ],
        blocked_items=[],
        deferred_items=[],
        future_track_items=["activation", "registry mutation", "runtime integration"],
        evidence_refs=list(candidate_set.evidence_refs if candidate_set is not None else []),
        withdrawal_conditions=[
            "candidate is treated as active artifact",
            "candidate set is treated as registry",
            "internalization plan is treated as implementation",
            "ready_for_activation, ready_for_registry_mutation, or ready_for_execution becomes true",
        ],
        metadata={"readiness_report_is_runtime_enablement": False},
    )


def candidate_preserves_no_activation(candidate: Any) -> bool:
    return _candidate_is_inactive(candidate) and getattr(candidate, "active_artifact", False) is False


def candidate_set_preserves_no_registry_mutation(candidate_set: InternalCandidateSet) -> bool:
    return (
        candidate_set.ready_for_activation is False
        and candidate_set.ready_for_registry_mutation is False
        and candidate_set.ready_for_execution is False
        and candidate_set.is_registry is False
        and candidate_set.creates_dominion_target is False
    )


def internalization_plan_preserves_no_execution(plan: InternalizationPlan) -> bool:
    return (
        plan.ready_for_activation is False
        and plan.ready_for_registry_mutation is False
        and plan.ready_for_execution is False
        and plan.no_execution_guarantee is True
        and plan.no_registry_mutation_guarantee is True
        and plan.no_skill_activation_guarantee is True
        and plan.no_tool_registration_guarantee is True
        and plan.no_mission_installation_guarantee is True
        and plan.no_policy_activation_guarantee is True
        and plan.no_memory_mutation_guarantee is True
    )


def internalization_plan_is_not_implementation(plan: InternalizationPlan) -> bool:
    return plan.is_implementation is False


def v0314_readiness_report_is_not_runtime_ready(report: V0314ReadinessReport) -> bool:
    return (
        report.ready_for_activation is False
        and report.ready_for_registry_mutation is False
        and report.ready_for_execution is False
        and report.runtime_enablement is False
    )
