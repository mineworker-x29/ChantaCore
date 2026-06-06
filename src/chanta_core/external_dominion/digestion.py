from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from chanta_core.external_dominion.dominion_levels import DominionLevel
from chanta_core.external_dominion.observation import (
    CapabilityObservationReport,
    ExternalCapabilityDescriptor,
    ExternalCapabilityKind,
    ExternalEffectSurface,
    ExternalRiskSignal,
    normalize_capability_kind,
    normalize_effect_surface,
    normalize_risk_signal,
)


class DigestionCandidateKind(StrEnum):
    TOOL_CONTRACT_PATTERN = "tool_contract_pattern"
    SKILL_MANIFEST_PATTERN = "skill_manifest_pattern"
    MISSION_MANIFEST_PATTERN = "mission_manifest_pattern"
    POLICY_RULE_PATTERN = "policy_rule_pattern"
    MEMORY_SCHEMA_PATTERN = "memory_schema_pattern"
    RESULT_ENVELOPE_PATTERN = "result_envelope_pattern"
    PROMPT_ASSEMBLY_PATTERN = "prompt_assembly_pattern"
    PROFILE_ISOLATION_PATTERN = "profile_isolation_pattern"
    GATEWAY_MANIFEST_PATTERN = "gateway_manifest_pattern"
    PROVIDER_ADAPTER_PATTERN = "provider_adapter_pattern"
    DELEGATION_PACKET_PATTERN = "delegation_packet_pattern"
    TRACE_EVENT_PATTERN = "trace_event_pattern"
    APPROVAL_BOUNDARY_PATTERN = "approval_boundary_pattern"
    UNKNOWN = "unknown"


class DigestionFeasibilityStatus(StrEnum):
    UNKNOWN = "unknown"
    DIGESTIBLE_PATTERN_ONLY = "digestible_pattern_only"
    SCHEMA_EXTRACTABLE = "schema_extractable"
    REQUIRES_INTERNAL_DESIGN = "requires_internal_design"
    REQUIRES_REVIEW = "requires_review"
    REQUIRES_DOMINION_REVIEW = "requires_dominion_review"
    NOT_DIGESTIBLE = "not_digestible"
    UNSAFE_TO_DIGEST = "unsafe_to_digest"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class AssimilationDecisionType(StrEnum):
    CANDIDATE = "candidate"
    DEFER = "defer"
    REJECT = "reject"
    DOMINION_REQUIRED = "dominion_required"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class InternalArtifactCandidateKind(StrEnum):
    INTERNAL_SKILL_CANDIDATE = "internal_skill_candidate"
    INTERNAL_TOOL_CONTRACT_CANDIDATE = "internal_tool_contract_candidate"
    INTERNAL_MISSION_MANIFEST_CANDIDATE = "internal_mission_manifest_candidate"
    INTERNAL_POLICY_RULE_CANDIDATE = "internal_policy_rule_candidate"
    INTERNAL_MEMORY_SCHEMA_CANDIDATE = "internal_memory_schema_candidate"
    INTERNAL_PROFILE_PATTERN_CANDIDATE = "internal_profile_pattern_candidate"
    INTERNAL_PROMPT_PATTERN_CANDIDATE = "internal_prompt_pattern_candidate"
    INTERNAL_TRACE_EVENT_PATTERN_CANDIDATE = "internal_trace_event_pattern_candidate"
    INTERNAL_GATEWAY_MANIFEST_CANDIDATE = "internal_gateway_manifest_candidate"
    INTERNAL_RESULT_ENVELOPE_CANDIDATE = "internal_result_envelope_candidate"
    NONE = "none"
    UNKNOWN = "unknown"


class DigestionBlockReason(StrEnum):
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    IDENTITY_UNTRUSTED = "identity_untrusted"
    TRUST_BOUNDARY_BLOCKED = "trust_boundary_blocked"
    DANGEROUS_NETWORK_SURFACE = "dangerous_network_surface"
    DANGEROUS_CREDENTIAL_SURFACE = "dangerous_credential_surface"
    DANGEROUS_COMMAND_SURFACE = "dangerous_command_surface"
    DANGEROUS_PROVIDER_SURFACE = "dangerous_provider_surface"
    DANGEROUS_BROWSER_SURFACE = "dangerous_browser_surface"
    DANGEROUS_RPA_SURFACE = "dangerous_rpa_surface"
    DANGEROUS_GATEWAY_SURFACE = "dangerous_gateway_surface"
    DELEGATION_SURFACE_UNCLEAR = "delegation_surface_unclear"
    MEMORY_CONTAMINATION_RISK = "memory_contamination_risk"
    RAW_OUTPUT_PERSISTENCE_RISK = "raw_output_persistence_risk"
    EXTERNAL_SIDE_EFFECT_RISK = "external_side_effect_risk"
    LICENSE_OR_SOURCE_UNCLEAR = "license_or_source_unclear"
    TOO_CONTEXT_HEAVY = "too_context_heavy"
    INCOMPATIBLE_WITH_OCEL_SPINE = "incompatible_with_ocel_spine"
    REQUIRES_FUTURE_GATE = "requires_future_gate"
    UNKNOWN = "unknown"


DIGESTIBLE_STATUSES = frozenset(
    {
        DigestionFeasibilityStatus.DIGESTIBLE_PATTERN_ONLY,
        DigestionFeasibilityStatus.SCHEMA_EXTRACTABLE,
    }
)

BLOCKED_OR_UNSAFE_STATUSES = frozenset(
    {
        DigestionFeasibilityStatus.BLOCKED,
        DigestionFeasibilityStatus.UNSAFE_TO_DIGEST,
    }
)

DEFERRED_STATUSES = frozenset(
    {
        DigestionFeasibilityStatus.UNKNOWN,
        DigestionFeasibilityStatus.REQUIRES_INTERNAL_DESIGN,
        DigestionFeasibilityStatus.REQUIRES_REVIEW,
        DigestionFeasibilityStatus.FUTURE_TRACK,
    }
)

REJECTED_STATUSES = frozenset(
    {
        DigestionFeasibilityStatus.NOT_DIGESTIBLE,
        DigestionFeasibilityStatus.UNSAFE_TO_DIGEST,
    }
)

EFFECT_TO_BLOCK_REASON = {
    ExternalEffectSurface.NETWORK_POSSIBLE: DigestionBlockReason.DANGEROUS_NETWORK_SURFACE,
    ExternalEffectSurface.CREDENTIAL_REQUIRED: DigestionBlockReason.DANGEROUS_CREDENTIAL_SURFACE,
    ExternalEffectSurface.COMMAND_POSSIBLE: DigestionBlockReason.DANGEROUS_COMMAND_SURFACE,
    ExternalEffectSurface.PROVIDER_INVOCATION_POSSIBLE: DigestionBlockReason.DANGEROUS_PROVIDER_SURFACE,
    ExternalEffectSurface.BROWSER_AUTOMATION_POSSIBLE: DigestionBlockReason.DANGEROUS_BROWSER_SURFACE,
    ExternalEffectSurface.RPA_CONTROL_POSSIBLE: DigestionBlockReason.DANGEROUS_RPA_SURFACE,
    ExternalEffectSurface.GATEWAY_MESSAGE_POSSIBLE: DigestionBlockReason.DANGEROUS_GATEWAY_SURFACE,
    ExternalEffectSurface.MEMORY_MUTATION_POSSIBLE: DigestionBlockReason.MEMORY_CONTAMINATION_RISK,
    ExternalEffectSurface.DELEGATION_POSSIBLE: DigestionBlockReason.DELEGATION_SURFACE_UNCLEAR,
    ExternalEffectSurface.EXTERNAL_SIDE_EFFECT_POSSIBLE: DigestionBlockReason.EXTERNAL_SIDE_EFFECT_RISK,
    ExternalEffectSurface.UNKNOWN: DigestionBlockReason.UNKNOWN,
}

RISK_TO_BLOCK_REASON = {
    ExternalRiskSignal.CREDENTIAL_ACCESS_POSSIBLE: DigestionBlockReason.DANGEROUS_CREDENTIAL_SURFACE,
    ExternalRiskSignal.NETWORK_ACCESS_POSSIBLE: DigestionBlockReason.DANGEROUS_NETWORK_SURFACE,
    ExternalRiskSignal.COMMAND_EXECUTION_POSSIBLE: DigestionBlockReason.DANGEROUS_COMMAND_SURFACE,
    ExternalRiskSignal.FILESYSTEM_WRITE_POSSIBLE: DigestionBlockReason.EXTERNAL_SIDE_EFFECT_RISK,
    ExternalRiskSignal.PROVIDER_INVOCATION_POSSIBLE: DigestionBlockReason.DANGEROUS_PROVIDER_SURFACE,
    ExternalRiskSignal.BROWSER_AUTOMATION_POSSIBLE: DigestionBlockReason.DANGEROUS_BROWSER_SURFACE,
    ExternalRiskSignal.RPA_CONTROL_POSSIBLE: DigestionBlockReason.DANGEROUS_RPA_SURFACE,
    ExternalRiskSignal.GATEWAY_SEND_POSSIBLE: DigestionBlockReason.DANGEROUS_GATEWAY_SURFACE,
    ExternalRiskSignal.MEMORY_CONTAMINATION_POSSIBLE: DigestionBlockReason.MEMORY_CONTAMINATION_RISK,
    ExternalRiskSignal.RAW_OUTPUT_PERSISTENCE_POSSIBLE: DigestionBlockReason.RAW_OUTPUT_PERSISTENCE_RISK,
    ExternalRiskSignal.AUTONOMOUS_LOOP_POSSIBLE: DigestionBlockReason.EXTERNAL_SIDE_EFFECT_RISK,
    ExternalRiskSignal.DELEGATED_AGENT_POSSIBLE: DigestionBlockReason.DELEGATION_SURFACE_UNCLEAR,
    ExternalRiskSignal.EXTERNAL_SIDE_EFFECT_POSSIBLE: DigestionBlockReason.EXTERNAL_SIDE_EFFECT_RISK,
    ExternalRiskSignal.HIGH_CONTEXT_BLOAT: DigestionBlockReason.TOO_CONTEXT_HEAVY,
    ExternalRiskSignal.IDENTITY_AMBIGUITY: DigestionBlockReason.IDENTITY_UNTRUSTED,
    ExternalRiskSignal.TRUST_BOUNDARY_UNCLEAR: DigestionBlockReason.TRUST_BOUNDARY_BLOCKED,
}


def _unique(values: list[Any]) -> list[Any]:
    result: list[Any] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result


def _require_non_blank(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must not be blank")


def normalize_candidate_kind(value: DigestionCandidateKind | str) -> DigestionCandidateKind:
    if isinstance(value, DigestionCandidateKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("candidate_kind must not be blank")
        return DigestionCandidateKind(stripped)
    raise TypeError(f"unsupported digestion candidate kind: {value!r}")


def normalize_feasibility_status(value: DigestionFeasibilityStatus | str) -> DigestionFeasibilityStatus:
    if isinstance(value, DigestionFeasibilityStatus):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("feasibility_status must not be blank")
        return DigestionFeasibilityStatus(stripped)
    raise TypeError(f"unsupported digestion feasibility status: {value!r}")


def normalize_decision_type(value: AssimilationDecisionType | str) -> AssimilationDecisionType:
    if isinstance(value, AssimilationDecisionType):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("decision must not be blank")
        return AssimilationDecisionType(stripped)
    raise TypeError(f"unsupported assimilation decision: {value!r}")


def normalize_internal_artifact_kind(value: InternalArtifactCandidateKind | str) -> InternalArtifactCandidateKind:
    if isinstance(value, InternalArtifactCandidateKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("proposed_internal_artifact_kind must not be blank")
        return InternalArtifactCandidateKind(stripped)
    raise TypeError(f"unsupported internal artifact candidate kind: {value!r}")


def normalize_block_reason(value: DigestionBlockReason | str) -> DigestionBlockReason:
    if isinstance(value, DigestionBlockReason):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("blocked reason must not be blank")
        return DigestionBlockReason(stripped)
    raise TypeError(f"unsupported digestion block reason: {value!r}")


def _normalize_block_reasons(values: list[DigestionBlockReason | str]) -> list[DigestionBlockReason]:
    if not isinstance(values, list):
        raise TypeError("blocked_reasons must be a list")
    return [normalize_block_reason(value) for value in values]


def _validate_string_list(name: str, values: list[str]) -> None:
    if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
        raise TypeError(f"{name} must be list[str]")


@dataclass(frozen=True)
class DigestionCandidate:
    candidate_id: str
    target_id: str
    source_report_id: str
    source_capability_ids: list[str]
    candidate_kind: DigestionCandidateKind | str
    proposed_internal_artifact_kind: InternalArtifactCandidateKind | str
    title: str
    summary: str | None = None
    extracted_pattern: dict[str, Any] = field(default_factory=dict)
    supporting_evidence_refs: list[str] = field(default_factory=list)
    risk_signals: list[str] = field(default_factory=list)
    effect_surfaces: list[str] = field(default_factory=list)
    boundary_surfaces: list[str] = field(default_factory=list)
    feasibility_status: DigestionFeasibilityStatus | str = DigestionFeasibilityStatus.UNKNOWN
    blocked_reasons: list[DigestionBlockReason | str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("candidate_id", self.candidate_id)
        _require_non_blank("target_id", self.target_id)
        _require_non_blank("source_report_id", self.source_report_id)
        _require_non_blank("title", self.title)
        _validate_string_list("source_capability_ids", self.source_capability_ids)
        _validate_string_list("supporting_evidence_refs", self.supporting_evidence_refs)
        _validate_string_list("risk_signals", self.risk_signals)
        _validate_string_list("effect_surfaces", self.effect_surfaces)
        _validate_string_list("boundary_surfaces", self.boundary_surfaces)
        _validate_string_list("assumptions", self.assumptions)
        _validate_string_list("withdrawal_conditions", self.withdrawal_conditions)
        if not isinstance(self.extracted_pattern, dict):
            raise TypeError("extracted_pattern must be a dict")
        normalize_candidate_kind(self.candidate_kind)
        normalize_internal_artifact_kind(self.proposed_internal_artifact_kind)
        status = normalize_feasibility_status(self.feasibility_status)
        reasons = _normalize_block_reasons(self.blocked_reasons)
        if status in BLOCKED_OR_UNSAFE_STATUSES and not reasons:
            raise ValueError("blocked or unsafe digestion candidates require blocked_reasons")
        if status in DIGESTIBLE_STATUSES and not self.supporting_evidence_refs:
            raise ValueError("digestible or schema-extractable candidates require supporting_evidence_refs")

    @property
    def creates_internal_artifact(self) -> bool:
        return False

    @property
    def creates_dominion_target(self) -> bool:
        return False

    @property
    def grants_permission(self) -> bool:
        return False

    @property
    def executes(self) -> bool:
        return False


@dataclass(frozen=True)
class DigestionFeasibilityReport:
    report_id: str
    target_id: str
    source_observation_report_id: str
    candidates: list[DigestionCandidate]
    digestible_count: int
    deferred_count: int
    rejected_count: int
    dominion_required_count: int
    blocked_count: int
    aggregate_block_reasons: list[DigestionBlockReason | str] = field(default_factory=list)
    aggregate_risk_signals: list[str] = field(default_factory=list)
    recommendation: str = "defer"
    confidence: str = "unknown"
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _require_non_blank("target_id", self.target_id)
        _require_non_blank("source_observation_report_id", self.source_observation_report_id)
        if not isinstance(self.candidates, list):
            raise TypeError("candidates must be a list")
        if any(candidate.target_id != self.target_id for candidate in self.candidates):
            raise ValueError("all candidate target_ids must match report target_id")
        _normalize_block_reasons(self.aggregate_block_reasons)
        _validate_string_list("aggregate_risk_signals", self.aggregate_risk_signals)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("withdrawal_conditions", self.withdrawal_conditions)
        expected = _count_candidate_statuses(self.candidates)
        actual = {
            "digestible_count": self.digestible_count,
            "deferred_count": self.deferred_count,
            "rejected_count": self.rejected_count,
            "dominion_required_count": self.dominion_required_count,
            "blocked_count": self.blocked_count,
        }
        if actual != expected:
            raise ValueError("digestion feasibility counts must match candidate statuses")
        lowered = self.recommendation.lower()
        if any(word in lowered for word in ("execute", "invoke", "register", "install", "grant authority")):
            raise ValueError("recommendation must not imply execution or runtime registration")

    @property
    def creates_internal_skill(self) -> bool:
        return False

    @property
    def creates_dominion_target(self) -> bool:
        return False

    @property
    def grants_permission(self) -> bool:
        return False


@dataclass(frozen=True)
class AssimilationDecision:
    decision_id: str
    candidate_id: str
    target_id: str
    source_report_id: str
    decision: AssimilationDecisionType | str
    proposed_internal_artifact_kind: InternalArtifactCandidateKind | str
    reason: str
    evidence_refs: list[str] = field(default_factory=list)
    required_reviews: list[str] = field(default_factory=list)
    blocked_reasons: list[DigestionBlockReason | str] = field(default_factory=list)
    dominion_review_required: bool = False
    future_gate_required: bool = False
    approval_required: bool = False
    validity_horizon: str | None = None
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("decision_id", self.decision_id)
        _require_non_blank("candidate_id", self.candidate_id)
        _require_non_blank("target_id", self.target_id)
        _require_non_blank("source_report_id", self.source_report_id)
        _require_non_blank("reason", self.reason)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("required_reviews", self.required_reviews)
        _validate_string_list("withdrawal_conditions", self.withdrawal_conditions)
        decision = normalize_decision_type(self.decision)
        normalize_internal_artifact_kind(self.proposed_internal_artifact_kind)
        reasons = _normalize_block_reasons(self.blocked_reasons)
        if decision is AssimilationDecisionType.CANDIDATE and not self.evidence_refs:
            raise ValueError("candidate assimilation decisions require evidence_refs")
        if decision in {AssimilationDecisionType.REJECT, AssimilationDecisionType.BLOCKED} and not (self.reason.strip() or reasons):
            raise ValueError("reject or blocked assimilation decisions require reason or blocked_reasons")
        if decision is AssimilationDecisionType.DOMINION_REQUIRED and not self.dominion_review_required:
            raise ValueError("dominion_required decisions must set dominion_review_required=True")
        if decision is AssimilationDecisionType.FUTURE_TRACK and not self.future_gate_required:
            raise ValueError("future_track decisions must set future_gate_required=True")

    @property
    def approval_granted(self) -> bool:
        return False

    @property
    def grants_permission(self) -> bool:
        return False

    @property
    def grants_dominion_authority(self) -> bool:
        return False

    @property
    def max_inferred_dominion_level(self) -> DominionLevel:
        return DominionLevel.D3_SIMULATE

    @property
    def creates_active_artifact(self) -> bool:
        return False


@dataclass(frozen=True)
class InternalizationPlan:
    plan_id: str
    decision_id: str
    candidate_id: str
    target_id: str
    proposed_internal_artifact_kind: InternalArtifactCandidateKind | str
    planned_steps: list[str]
    required_contracts: list[str]
    required_tests: list[str]
    required_reviews: list[str]
    explicitly_out_of_scope: list[str]
    no_execution_guarantee: bool
    no_runtime_registration_guarantee: bool
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("plan_id", self.plan_id)
        _require_non_blank("decision_id", self.decision_id)
        _require_non_blank("candidate_id", self.candidate_id)
        _require_non_blank("target_id", self.target_id)
        normalize_internal_artifact_kind(self.proposed_internal_artifact_kind)
        _validate_string_list("planned_steps", self.planned_steps)
        _validate_string_list("required_contracts", self.required_contracts)
        _validate_string_list("required_tests", self.required_tests)
        _validate_string_list("required_reviews", self.required_reviews)
        _validate_string_list("explicitly_out_of_scope", self.explicitly_out_of_scope)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("withdrawal_conditions", self.withdrawal_conditions)
        if self.no_execution_guarantee is not True:
            raise ValueError("no_execution_guarantee must be True")
        if self.no_runtime_registration_guarantee is not True:
            raise ValueError("no_runtime_registration_guarantee must be True")
        for step in self.planned_steps:
            lowered = step.lower()
            if any(f" {word} " in f" {lowered} " for word in ("execute", "run", "call", "send", "fetch", "invoke")):
                if "prohibited" not in lowered and "out of scope" not in lowered:
                    raise ValueError("planned_steps must not include execution verbs as actual operations")

    @property
    def creates_files(self) -> bool:
        return False

    @property
    def registers_runtime_artifact(self) -> bool:
        return False

    @property
    def executes(self) -> bool:
        return False


def _count_candidate_statuses(candidates: list[DigestionCandidate]) -> dict[str, int]:
    counts = {
        "digestible_count": 0,
        "deferred_count": 0,
        "rejected_count": 0,
        "dominion_required_count": 0,
        "blocked_count": 0,
    }
    for candidate in candidates:
        status = normalize_feasibility_status(candidate.feasibility_status)
        if status in DIGESTIBLE_STATUSES:
            counts["digestible_count"] += 1
        if status in DEFERRED_STATUSES:
            counts["deferred_count"] += 1
        if status in REJECTED_STATUSES:
            counts["rejected_count"] += 1
        if status is DigestionFeasibilityStatus.REQUIRES_DOMINION_REVIEW:
            counts["dominion_required_count"] += 1
        if status is DigestionFeasibilityStatus.BLOCKED:
            counts["blocked_count"] += 1
    return counts


def _text_for_descriptor(descriptor: ExternalCapabilityDescriptor) -> str:
    parts = [descriptor.name, descriptor.description or ""]
    parts.extend(str(value) for value in descriptor.declared_inputs)
    parts.extend(str(value) for value in descriptor.metadata.values())
    return " ".join(parts).lower()


def classify_digestion_candidate_from_capability(descriptor: ExternalCapabilityDescriptor) -> DigestionCandidateKind:
    kind = normalize_capability_kind(descriptor.kind)
    text = _text_for_descriptor(descriptor)
    if "approval" in text or "audit" in text or "rollback" in text:
        return DigestionCandidateKind.APPROVAL_BOUNDARY_PATTERN
    if "result" in text and "envelope" in text:
        return DigestionCandidateKind.RESULT_ENVELOPE_PATTERN
    if "trace" in text or "ocel" in text or "event" in text:
        return DigestionCandidateKind.TRACE_EVENT_PATTERN
    if "profile" in text or "isolation" in text:
        return DigestionCandidateKind.PROFILE_ISOLATION_PATTERN
    if "prompt" in text or "assembly" in text:
        return DigestionCandidateKind.PROMPT_ASSEMBLY_PATTERN
    if "policy" in text or "rule" in text:
        return DigestionCandidateKind.POLICY_RULE_PATTERN
    if "memory" in text or kind is ExternalCapabilityKind.MEMORY_SURFACE:
        return DigestionCandidateKind.MEMORY_SCHEMA_PATTERN
    if "gateway" in text or kind is ExternalCapabilityKind.GATEWAY_CHANNEL:
        return DigestionCandidateKind.GATEWAY_MANIFEST_PATTERN
    if "provider" in text or kind is ExternalCapabilityKind.PROVIDER:
        return DigestionCandidateKind.PROVIDER_ADAPTER_PATTERN
    if "delegate" in text or kind in {ExternalCapabilityKind.AGENT, ExternalCapabilityKind.DELEGATION_SURFACE}:
        return DigestionCandidateKind.DELEGATION_PACKET_PATTERN
    if "mission" in text or "scheduler" in text or kind is ExternalCapabilityKind.SCHEDULER:
        return DigestionCandidateKind.MISSION_MANIFEST_PATTERN
    if "skill" in text or kind in {ExternalCapabilityKind.SKILL, ExternalCapabilityKind.PLUGIN}:
        return DigestionCandidateKind.SKILL_MANIFEST_PATTERN
    if kind in {ExternalCapabilityKind.TOOL, ExternalCapabilityKind.MCP_TOOL}:
        return DigestionCandidateKind.TOOL_CONTRACT_PATTERN
    return DigestionCandidateKind.UNKNOWN


def infer_internal_artifact_candidate_kind(
    candidate_kind: DigestionCandidateKind | str,
) -> InternalArtifactCandidateKind:
    kind = normalize_candidate_kind(candidate_kind)
    return {
        DigestionCandidateKind.TOOL_CONTRACT_PATTERN: InternalArtifactCandidateKind.INTERNAL_TOOL_CONTRACT_CANDIDATE,
        DigestionCandidateKind.SKILL_MANIFEST_PATTERN: InternalArtifactCandidateKind.INTERNAL_SKILL_CANDIDATE,
        DigestionCandidateKind.MISSION_MANIFEST_PATTERN: InternalArtifactCandidateKind.INTERNAL_MISSION_MANIFEST_CANDIDATE,
        DigestionCandidateKind.POLICY_RULE_PATTERN: InternalArtifactCandidateKind.INTERNAL_POLICY_RULE_CANDIDATE,
        DigestionCandidateKind.MEMORY_SCHEMA_PATTERN: InternalArtifactCandidateKind.INTERNAL_MEMORY_SCHEMA_CANDIDATE,
        DigestionCandidateKind.RESULT_ENVELOPE_PATTERN: InternalArtifactCandidateKind.INTERNAL_RESULT_ENVELOPE_CANDIDATE,
        DigestionCandidateKind.PROMPT_ASSEMBLY_PATTERN: InternalArtifactCandidateKind.INTERNAL_PROMPT_PATTERN_CANDIDATE,
        DigestionCandidateKind.PROFILE_ISOLATION_PATTERN: InternalArtifactCandidateKind.INTERNAL_PROFILE_PATTERN_CANDIDATE,
        DigestionCandidateKind.GATEWAY_MANIFEST_PATTERN: InternalArtifactCandidateKind.INTERNAL_GATEWAY_MANIFEST_CANDIDATE,
        DigestionCandidateKind.PROVIDER_ADAPTER_PATTERN: InternalArtifactCandidateKind.NONE,
        DigestionCandidateKind.DELEGATION_PACKET_PATTERN: InternalArtifactCandidateKind.NONE,
        DigestionCandidateKind.TRACE_EVENT_PATTERN: InternalArtifactCandidateKind.INTERNAL_TRACE_EVENT_PATTERN_CANDIDATE,
        DigestionCandidateKind.APPROVAL_BOUNDARY_PATTERN: InternalArtifactCandidateKind.INTERNAL_POLICY_RULE_CANDIDATE,
        DigestionCandidateKind.UNKNOWN: InternalArtifactCandidateKind.UNKNOWN,
    }[kind]


def infer_digestion_block_reasons_from_observation(
    report_or_descriptor: CapabilityObservationReport | ExternalCapabilityDescriptor,
) -> list[DigestionBlockReason]:
    reasons: list[DigestionBlockReason] = []
    if isinstance(report_or_descriptor, CapabilityObservationReport):
        for blocked in report_or_descriptor.blocked_reasons:
            if blocked:
                reasons.append(DigestionBlockReason.TRUST_BOUNDARY_BLOCKED)
        effects = report_or_descriptor.aggregate_effect_surfaces
        risks = report_or_descriptor.aggregate_risk_signals
        if not report_or_descriptor.evidence_refs and not any(capability.evidence_refs for capability in report_or_descriptor.capabilities):
            reasons.append(DigestionBlockReason.INSUFFICIENT_EVIDENCE)
    else:
        effects = [normalize_effect_surface(effect) for effect in report_or_descriptor.effect_surfaces]
        risks = [normalize_risk_signal(risk) for risk in report_or_descriptor.risk_signals]
        if not report_or_descriptor.evidence_refs:
            reasons.append(DigestionBlockReason.INSUFFICIENT_EVIDENCE)
    reasons.extend(EFFECT_TO_BLOCK_REASON[effect] for effect in effects if effect in EFFECT_TO_BLOCK_REASON)
    reasons.extend(RISK_TO_BLOCK_REASON[risk] for risk in risks if risk in RISK_TO_BLOCK_REASON)
    return _unique(reasons)


def is_dangerous_for_digestion(report_or_candidate: CapabilityObservationReport | DigestionCandidate) -> bool:
    if isinstance(report_or_candidate, CapabilityObservationReport):
        return any(
            reason is not DigestionBlockReason.INSUFFICIENT_EVIDENCE
            for reason in infer_digestion_block_reasons_from_observation(report_or_candidate)
        )
    status = normalize_feasibility_status(report_or_candidate.feasibility_status)
    reasons = _normalize_block_reasons(report_or_candidate.blocked_reasons)
    return status in {
        DigestionFeasibilityStatus.REQUIRES_DOMINION_REVIEW,
        DigestionFeasibilityStatus.UNSAFE_TO_DIGEST,
        DigestionFeasibilityStatus.BLOCKED,
    } or any(reason is not DigestionBlockReason.INSUFFICIENT_EVIDENCE for reason in reasons)


def is_dangerous_for_digestestion(report_or_candidate: CapabilityObservationReport | DigestionCandidate) -> bool:
    return is_dangerous_for_digestion(report_or_candidate)


def can_create_digestion_candidate_from_report(report: CapabilityObservationReport) -> bool:
    if report.blocked_reasons:
        return False
    return bool(report.capabilities)


def _feasibility_for_descriptor(descriptor: ExternalCapabilityDescriptor) -> DigestionFeasibilityStatus:
    reasons = infer_digestion_block_reasons_from_observation(descriptor)
    dangerous_reasons = [reason for reason in reasons if reason is not DigestionBlockReason.INSUFFICIENT_EVIDENCE]
    if any(
        reason
        in {
            DigestionBlockReason.DANGEROUS_COMMAND_SURFACE,
            DigestionBlockReason.DANGEROUS_CREDENTIAL_SURFACE,
            DigestionBlockReason.DANGEROUS_RPA_SURFACE,
        }
        for reason in dangerous_reasons
    ):
        return DigestionFeasibilityStatus.REQUIRES_DOMINION_REVIEW
    if dangerous_reasons:
        return DigestionFeasibilityStatus.REQUIRES_DOMINION_REVIEW
    if DigestionBlockReason.INSUFFICIENT_EVIDENCE in reasons:
        return DigestionFeasibilityStatus.REQUIRES_REVIEW
    candidate_kind = classify_digestion_candidate_from_capability(descriptor)
    if candidate_kind in {
        DigestionCandidateKind.TOOL_CONTRACT_PATTERN,
        DigestionCandidateKind.SKILL_MANIFEST_PATTERN,
        DigestionCandidateKind.MISSION_MANIFEST_PATTERN,
        DigestionCandidateKind.RESULT_ENVELOPE_PATTERN,
        DigestionCandidateKind.TRACE_EVENT_PATTERN,
        DigestionCandidateKind.APPROVAL_BOUNDARY_PATTERN,
    }:
        return DigestionFeasibilityStatus.DIGESTIBLE_PATTERN_ONLY
    if candidate_kind in {
        DigestionCandidateKind.MEMORY_SCHEMA_PATTERN,
        DigestionCandidateKind.POLICY_RULE_PATTERN,
        DigestionCandidateKind.PROFILE_ISOLATION_PATTERN,
        DigestionCandidateKind.PROMPT_ASSEMBLY_PATTERN,
    }:
        return DigestionFeasibilityStatus.REQUIRES_INTERNAL_DESIGN
    if candidate_kind in {
        DigestionCandidateKind.PROVIDER_ADAPTER_PATTERN,
        DigestionCandidateKind.GATEWAY_MANIFEST_PATTERN,
        DigestionCandidateKind.DELEGATION_PACKET_PATTERN,
    }:
        return DigestionFeasibilityStatus.REQUIRES_DOMINION_REVIEW
    return DigestionFeasibilityStatus.REQUIRES_REVIEW


def build_digestion_candidates_from_observation_report(report: CapabilityObservationReport) -> list[DigestionCandidate]:
    if not can_create_digestion_candidate_from_report(report):
        return []
    candidates: list[DigestionCandidate] = []
    for descriptor in report.capabilities:
        candidate_kind = classify_digestion_candidate_from_capability(descriptor)
        internal_kind = infer_internal_artifact_candidate_kind(candidate_kind)
        status = _feasibility_for_descriptor(descriptor)
        reasons = infer_digestion_block_reasons_from_observation(descriptor)
        evidence_refs = list(descriptor.evidence_refs or report.evidence_refs)
        if status in DIGESTIBLE_STATUSES and not evidence_refs:
            status = DigestionFeasibilityStatus.REQUIRES_REVIEW
            reasons = _unique(reasons + [DigestionBlockReason.INSUFFICIENT_EVIDENCE])
        if status is DigestionFeasibilityStatus.REQUIRES_DOMINION_REVIEW and internal_kind not in {
            InternalArtifactCandidateKind.NONE,
            InternalArtifactCandidateKind.UNKNOWN,
        }:
            internal_kind = InternalArtifactCandidateKind.NONE
        candidates.append(
            DigestionCandidate(
                candidate_id=f"digestion_candidate:{descriptor.capability_id}",
                target_id=report.target_id,
                source_report_id=report.report_id,
                source_capability_ids=[descriptor.capability_id],
                candidate_kind=candidate_kind,
                proposed_internal_artifact_kind=internal_kind,
                title=f"Digestion review for {descriptor.name}",
                summary=descriptor.description,
                extracted_pattern={
                    "capability_kind": str(normalize_capability_kind(descriptor.kind)),
                    "declared_inputs": list(descriptor.declared_inputs),
                    "declared_outputs": list(descriptor.declared_outputs),
                    "source_ref_preserved_only": report.source_ref,
                },
                supporting_evidence_refs=evidence_refs,
                risk_signals=[str(risk) for risk in descriptor.risk_signals],
                effect_surfaces=[str(effect) for effect in descriptor.effect_surfaces],
                boundary_surfaces=[str(surface) for surface in descriptor.boundary_surfaces],
                feasibility_status=status,
                blocked_reasons=reasons,
                assumptions=[
                    "Observation artifacts are descriptive only.",
                    "Digestible pattern does not copy external code or create runtime artifacts.",
                ],
                withdrawal_conditions=[
                    "candidate is treated as an active internal skill, tool, mission, policy, memory writer, or runtime adapter",
                    "candidate creation fetches source_ref, invokes an external target, or grants permission",
                ],
                metadata={"v0303_contract_only": True},
            )
        )
    return candidates


def summarize_digestion_feasibility(
    candidates: list[DigestionCandidate],
    target_id: str,
    source_report_id: str,
) -> DigestionFeasibilityReport:
    _require_non_blank("target_id", target_id)
    _require_non_blank("source_report_id", source_report_id)
    aggregate_reasons: list[DigestionBlockReason] = []
    aggregate_risks: list[str] = []
    evidence_refs: list[str] = []
    for candidate in candidates:
        aggregate_reasons.extend(_normalize_block_reasons(candidate.blocked_reasons))
        aggregate_risks.extend(candidate.risk_signals)
        evidence_refs.extend(candidate.supporting_evidence_refs)
    counts = _count_candidate_statuses(candidates)
    if counts["blocked_count"]:
        recommendation = "blocked"
    elif counts["dominion_required_count"]:
        recommendation = "route_dominion_review_without_authority"
    elif counts["digestible_count"]:
        recommendation = "candidate_review_only"
    elif counts["deferred_count"]:
        recommendation = "defer_for_more_observation"
    else:
        recommendation = "no_op"
    return DigestionFeasibilityReport(
        report_id=f"digestion_feasibility_report:{target_id}",
        target_id=target_id,
        source_observation_report_id=source_report_id,
        candidates=list(candidates),
        digestible_count=counts["digestible_count"],
        deferred_count=counts["deferred_count"],
        rejected_count=counts["rejected_count"],
        dominion_required_count=counts["dominion_required_count"],
        blocked_count=counts["blocked_count"],
        aggregate_block_reasons=_unique(aggregate_reasons),
        aggregate_risk_signals=_unique(aggregate_risks),
        recommendation=recommendation,
        confidence="low" if evidence_refs else "unknown",
        evidence_refs=_unique(evidence_refs),
        withdrawal_conditions=[
            "feasibility report is treated as implementation, runtime registration, permission, or dominion authority",
            "v0.30.3 raises runtime readiness flags or grantability beyond D3_SIMULATE",
        ],
        metadata={"v0303_contract_only": True},
    )


def make_assimilation_decision(candidate: DigestionCandidate) -> AssimilationDecision:
    status = normalize_feasibility_status(candidate.feasibility_status)
    blocked_reasons = _normalize_block_reasons(candidate.blocked_reasons)
    if status in DIGESTIBLE_STATUSES:
        decision = AssimilationDecisionType.CANDIDATE
        reason = "Evidence-linked pattern may be reviewed as an internal artifact candidate only."
        dominion_required = False
        future_gate = False
    elif status is DigestionFeasibilityStatus.REQUIRES_DOMINION_REVIEW:
        decision = AssimilationDecisionType.DOMINION_REQUIRED
        reason = "Capability surfaces require later Dominion review without authority grant."
        dominion_required = True
        future_gate = False
    elif status is DigestionFeasibilityStatus.BLOCKED:
        decision = AssimilationDecisionType.BLOCKED
        reason = "Digestion progression is blocked by boundary reasons."
        dominion_required = False
        future_gate = False
    elif status is DigestionFeasibilityStatus.FUTURE_TRACK:
        decision = AssimilationDecisionType.FUTURE_TRACK
        reason = "Capability belongs to future-track gates and is not readiness."
        dominion_required = False
        future_gate = True
    elif status in REJECTED_STATUSES:
        decision = AssimilationDecisionType.REJECT
        reason = "Capability is not currently fit for safe digestion."
        dominion_required = False
        future_gate = status is DigestionFeasibilityStatus.UNSAFE_TO_DIGEST
    else:
        decision = AssimilationDecisionType.DEFER
        reason = "Evidence or internal design is insufficient for candidate promotion."
        dominion_required = False
        future_gate = False
    return AssimilationDecision(
        decision_id=f"assimilation_decision:{candidate.candidate_id}",
        candidate_id=candidate.candidate_id,
        target_id=candidate.target_id,
        source_report_id=candidate.source_report_id,
        decision=decision,
        proposed_internal_artifact_kind=(
            candidate.proposed_internal_artifact_kind
            if decision is AssimilationDecisionType.CANDIDATE
            else InternalArtifactCandidateKind.NONE
        ),
        reason=reason,
        evidence_refs=list(candidate.supporting_evidence_refs),
        required_reviews=["human_review", "privacy_boundary_review"] + (["dominion_review"] if dominion_required else []),
        blocked_reasons=blocked_reasons,
        dominion_review_required=dominion_required,
        future_gate_required=future_gate,
        approval_required=dominion_required or future_gate,
        validity_horizon="v0.30.3 contract only; expires when v0.30.4+ changes dominion routing.",
        withdrawal_conditions=[
            "decision is treated as permission, implementation, active artifact, or DominionAuthority",
            "decision grants D4+ or marks runtime readiness true",
        ],
        metadata={"v0303_contract_only": True, "max_inferred_dominion_level": str(DominionLevel.D3_SIMULATE)},
    )


def make_internalization_plan(decision: AssimilationDecision) -> InternalizationPlan | None:
    decision_type = normalize_decision_type(decision.decision)
    if decision_type is not AssimilationDecisionType.CANDIDATE:
        return None
    return InternalizationPlan(
        plan_id=f"internalization_plan:{decision.candidate_id}",
        decision_id=decision.decision_id,
        candidate_id=decision.candidate_id,
        target_id=decision.target_id,
        proposed_internal_artifact_kind=decision.proposed_internal_artifact_kind,
        planned_steps=[
            "Review extracted pattern against ChantaCore OCEL spine.",
            "Draft candidate contract shape for later implementation review.",
            "List tests required before any future runtime work.",
        ],
        required_contracts=["v0.30.3 assimilation decision", "future v0.31 internal triad contract"],
        required_tests=["candidate validation", "runtime boundary negative search"],
        required_reviews=list(decision.required_reviews),
        explicitly_out_of_scope=[
            "external execution prohibited",
            "runtime registration prohibited",
            "skill, tool, mission, policy, memory writer, provider, gateway, browser, RPA, or delegation activation prohibited",
        ],
        no_execution_guarantee=True,
        no_runtime_registration_guarantee=True,
        evidence_refs=list(decision.evidence_refs),
        withdrawal_conditions=[
            "plan is treated as implementation or runtime registration",
            "plan writes files, registers artifacts, invokes external systems, or grants authority",
        ],
        metadata={"v0303_contract_only": True},
    )
