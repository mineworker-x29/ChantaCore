from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from chanta_core.external_dominion.digestion import (
    AssimilationDecision,
    AssimilationDecisionType,
    DigestionCandidate,
)
from chanta_core.external_dominion.dominion_levels import (
    DominionLevel,
    normalize_dominion_level,
)
from chanta_core.external_dominion.observation import ExternalEffectSurface
from chanta_core.external_dominion.trust import ExternalBoundarySurface


class DominionAuthorityRequestStatus(StrEnum):
    UNKNOWN = "unknown"
    REQUESTED = "requested"
    EVIDENCE_LINKED = "evidence_linked"
    REVIEW_REQUIRED = "review_required"
    DENIED = "denied"
    DEFERRED = "deferred"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class DominionAuthorityDecisionType(StrEnum):
    DENY = "deny"
    DEFER = "defer"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    OBSERVE_ONLY = "observe_only"
    DESCRIBE_ONLY = "describe_only"
    PLAN_ONLY = "plan_only"
    SIMULATE_ONLY = "simulate_only"
    FUTURE_TRACK = "future_track"
    BLOCKED = "blocked"


class DominionAuthorityScopeKind(StrEnum):
    TARGET_SCOPE = "target_scope"
    CAPABILITY_SCOPE = "capability_scope"
    CANDIDATE_SCOPE = "candidate_scope"
    REPORT_SCOPE = "report_scope"
    PROFILE_SCOPE = "profile_scope"
    MISSION_SCOPE = "mission_scope"
    DELEGATION_SCOPE = "delegation_scope"
    GATEWAY_SCOPE = "gateway_scope"
    PROVIDER_SCOPE = "provider_scope"
    RPA_SCOPE = "rpa_scope"
    UNKNOWN = "unknown"


V0304_MAX_GRANTABLE_LEVEL = DominionLevel.D3_SIMULATE

DANGEROUS_AUTHORITY_BOUNDARY_SURFACES = frozenset(
    {
        ExternalBoundarySurface.CREDENTIAL_BOUNDARY,
        ExternalBoundarySurface.NETWORK_BOUNDARY,
        ExternalBoundarySurface.COMMAND_BOUNDARY,
        ExternalBoundarySurface.BROWSER_BOUNDARY,
        ExternalBoundarySurface.RPA_BOUNDARY,
        ExternalBoundarySurface.GATEWAY_BOUNDARY,
        ExternalBoundarySurface.DELEGATION_BOUNDARY,
        ExternalBoundarySurface.PROVIDER_BOUNDARY,
    }
)

DANGEROUS_AUTHORITY_EFFECT_SURFACES = frozenset(
    {
        ExternalEffectSurface.WRITE_POSSIBLE,
        ExternalEffectSurface.COMMAND_POSSIBLE,
        ExternalEffectSurface.NETWORK_POSSIBLE,
        ExternalEffectSurface.CREDENTIAL_REQUIRED,
        ExternalEffectSurface.PROVIDER_INVOCATION_POSSIBLE,
        ExternalEffectSurface.BROWSER_AUTOMATION_POSSIBLE,
        ExternalEffectSurface.RPA_CONTROL_POSSIBLE,
        ExternalEffectSurface.GATEWAY_MESSAGE_POSSIBLE,
        ExternalEffectSurface.MEMORY_MUTATION_POSSIBLE,
        ExternalEffectSurface.DELEGATION_POSSIBLE,
        ExternalEffectSurface.EXTERNAL_SIDE_EFFECT_POSSIBLE,
        ExternalEffectSurface.UNKNOWN,
    }
)

CONSERVATIVE_SCOPE_KINDS = frozenset(
    {
        DominionAuthorityScopeKind.DELEGATION_SCOPE,
        DominionAuthorityScopeKind.GATEWAY_SCOPE,
        DominionAuthorityScopeKind.PROVIDER_SCOPE,
        DominionAuthorityScopeKind.RPA_SCOPE,
        DominionAuthorityScopeKind.UNKNOWN,
    }
)


def _unique(values: list[Any]) -> list[Any]:
    result: list[Any] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result


def _require_non_blank(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must not be blank")


def _validate_string_list(name: str, values: list[str]) -> None:
    if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
        raise TypeError(f"{name} must be list[str]")


def normalize_authority_request_status(
    value: DominionAuthorityRequestStatus | str,
) -> DominionAuthorityRequestStatus:
    if isinstance(value, DominionAuthorityRequestStatus):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("request_status must not be blank")
        return DominionAuthorityRequestStatus(stripped)
    raise TypeError(f"unsupported request status: {value!r}")


def normalize_authority_decision_type(
    value: DominionAuthorityDecisionType | str,
) -> DominionAuthorityDecisionType:
    if isinstance(value, DominionAuthorityDecisionType):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("decision must not be blank")
        return DominionAuthorityDecisionType(stripped)
    raise TypeError(f"unsupported authority decision: {value!r}")


def normalize_authority_scope_kind(value: DominionAuthorityScopeKind | str) -> DominionAuthorityScopeKind:
    if isinstance(value, DominionAuthorityScopeKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("scope_kind must not be blank")
        return DominionAuthorityScopeKind(stripped)
    raise TypeError(f"unsupported authority scope kind: {value!r}")


def _normalize_boundary(value: ExternalBoundarySurface | str) -> ExternalBoundarySurface:
    if isinstance(value, ExternalBoundarySurface):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("boundary surface must not be blank")
        return ExternalBoundarySurface(stripped)
    raise TypeError(f"unsupported boundary surface: {value!r}")


def _normalize_effect(value: ExternalEffectSurface | str) -> ExternalEffectSurface:
    if isinstance(value, ExternalEffectSurface):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("effect surface must not be blank")
        return ExternalEffectSurface(stripped)
    raise TypeError(f"unsupported effect surface: {value!r}")


def dominion_level_rank(level: DominionLevel | int | str) -> int:
    return int(normalize_dominion_level(level))


def compare_dominion_levels(a: DominionLevel | int | str, b: DominionLevel | int | str) -> int:
    rank_a = dominion_level_rank(a)
    rank_b = dominion_level_rank(b)
    if rank_a < rank_b:
        return -1
    if rank_a > rank_b:
        return 1
    return 0


def is_v0304_grantable_level(level: DominionLevel | int | str) -> bool:
    return normalize_dominion_level(level) <= V0304_MAX_GRANTABLE_LEVEL


def clamp_v0304_grant_level(level: DominionLevel | int | str) -> DominionLevel | None:
    normalized = normalize_dominion_level(level)
    if normalized > V0304_MAX_GRANTABLE_LEVEL:
        return None
    return normalized


def _default_prohibited_boundaries() -> list[str]:
    return [surface.value for surface in sorted(DANGEROUS_AUTHORITY_BOUNDARY_SURFACES, key=lambda item: item.value)]


def _default_prohibited_effects() -> list[str]:
    return [surface.value for surface in sorted(DANGEROUS_AUTHORITY_EFFECT_SURFACES, key=lambda item: item.value)]


@dataclass(frozen=True)
class DominionAuthorityScope:
    scope_id: str
    scope_kind: DominionAuthorityScopeKind | str
    target_id: str
    capability_ids: list[str] = field(default_factory=list)
    candidate_ids: list[str] = field(default_factory=list)
    report_ids: list[str] = field(default_factory=list)
    allowed_boundary_surfaces: list[str] = field(default_factory=list)
    prohibited_boundary_surfaces: list[str] = field(default_factory=_default_prohibited_boundaries)
    allowed_effect_surfaces: list[str] = field(default_factory=lambda: [ExternalEffectSurface.READ_ONLY.value])
    prohibited_effect_surfaces: list[str] = field(default_factory=_default_prohibited_effects)
    max_level: DominionLevel | int | str = DominionLevel.D1_DESCRIBE
    expires_at: str | None = None
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("scope_id", self.scope_id)
        _require_non_blank("target_id", self.target_id)
        scope_kind = normalize_authority_scope_kind(self.scope_kind)
        _validate_string_list("capability_ids", self.capability_ids)
        _validate_string_list("candidate_ids", self.candidate_ids)
        _validate_string_list("report_ids", self.report_ids)
        _validate_string_list("allowed_boundary_surfaces", self.allowed_boundary_surfaces)
        _validate_string_list("prohibited_boundary_surfaces", self.prohibited_boundary_surfaces)
        _validate_string_list("allowed_effect_surfaces", self.allowed_effect_surfaces)
        _validate_string_list("prohibited_effect_surfaces", self.prohibited_effect_surfaces)
        _validate_string_list("evidence_refs", self.evidence_refs)
        max_level = normalize_dominion_level(self.max_level)
        if max_level > V0304_MAX_GRANTABLE_LEVEL:
            raise ValueError("v0.30.4 authority scope max_level cannot exceed D3_SIMULATE")
        allowed_boundaries = {_normalize_boundary(surface) for surface in self.allowed_boundary_surfaces}
        prohibited_boundaries = {_normalize_boundary(surface) for surface in self.prohibited_boundary_surfaces}
        allowed_effects = {_normalize_effect(surface) for surface in self.allowed_effect_surfaces}
        prohibited_effects = {_normalize_effect(surface) for surface in self.prohibited_effect_surfaces}
        if allowed_boundaries & DANGEROUS_AUTHORITY_BOUNDARY_SURFACES:
            raise ValueError("dangerous boundary surfaces cannot be allowed by v0.30.4 authority scope")
        if allowed_effects & DANGEROUS_AUTHORITY_EFFECT_SURFACES:
            raise ValueError("dangerous effect surfaces cannot be allowed by v0.30.4 authority scope")
        missing_boundaries = DANGEROUS_AUTHORITY_BOUNDARY_SURFACES - prohibited_boundaries
        if missing_boundaries:
            raise ValueError("prohibited dangerous boundary surfaces must be preserved")
        missing_effects = DANGEROUS_AUTHORITY_EFFECT_SURFACES - prohibited_effects
        if missing_effects:
            raise ValueError("prohibited dangerous effect surfaces must be preserved")
        if scope_kind in CONSERVATIVE_SCOPE_KINDS and max_level > DominionLevel.D1_DESCRIBE:
            raise ValueError("gateway/provider/rpa/delegation/unknown scopes are conservative in v0.30.4")

    @property
    def grants_execution(self) -> bool:
        return False

    @property
    def grants_permission(self) -> bool:
        return False


def make_default_authority_scope(
    target_id: str,
    scope_kind: DominionAuthorityScopeKind | str = DominionAuthorityScopeKind.TARGET_SCOPE,
    scope_id: str | None = None,
    max_level: DominionLevel | int | str = DominionLevel.D1_DESCRIBE,
    capability_ids: list[str] | None = None,
    candidate_ids: list[str] | None = None,
    report_ids: list[str] | None = None,
    evidence_refs: list[str] | None = None,
) -> DominionAuthorityScope:
    _require_non_blank("target_id", target_id)
    return DominionAuthorityScope(
        scope_id or f"dominion_authority_scope:{target_id}",
        scope_kind,
        target_id,
        capability_ids=list(capability_ids or []),
        candidate_ids=list(candidate_ids or []),
        report_ids=list(report_ids or []),
        max_level=max_level,
        evidence_refs=list(evidence_refs or []),
    )


@dataclass(frozen=True)
class DominionAuthorityRequest:
    request_id: str
    target_id: str
    requested_level: DominionLevel | int | str
    requested_scope: DominionAuthorityScope | None = None
    requested_capabilities: list[str] = field(default_factory=list)
    source_kind: str | None = None
    source_ref: str | None = None
    source_candidate_ids: list[str] = field(default_factory=list)
    source_report_ids: list[str] = field(default_factory=list)
    rationale: str = ""
    evidence_refs: list[str] = field(default_factory=list)
    request_status: DominionAuthorityRequestStatus | str = DominionAuthorityRequestStatus.REQUESTED
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("request_id", self.request_id)
        _require_non_blank("target_id", self.target_id)
        normalize_dominion_level(self.requested_level)
        scope = self.effective_scope
        if scope.target_id != self.target_id:
            raise ValueError("requested_scope.target_id must match request target_id")
        _validate_string_list("requested_capabilities", self.requested_capabilities)
        _validate_string_list("source_candidate_ids", self.source_candidate_ids)
        _validate_string_list("source_report_ids", self.source_report_ids)
        _validate_string_list("evidence_refs", self.evidence_refs)
        status = normalize_authority_request_status(self.request_status)
        if status is DominionAuthorityRequestStatus.EVIDENCE_LINKED and not self.evidence_refs:
            raise ValueError("evidence_linked authority request requires evidence_refs")

    @property
    def effective_scope(self) -> DominionAuthorityScope:
        if self.requested_scope is not None:
            return self.requested_scope
        return make_default_authority_scope(
            self.target_id,
            max_level=min(normalize_dominion_level(self.requested_level), DominionLevel.D1_DESCRIBE),
            evidence_refs=self.evidence_refs,
        )

    @property
    def source_ref_fetched(self) -> bool:
        return False

    @property
    def grants_authority(self) -> bool:
        return False

    @property
    def grants_permission(self) -> bool:
        return False


@dataclass(frozen=True)
class DominionAuthorityEvaluation:
    evaluation_id: str
    request_id: str
    target_id: str
    requested_level: DominionLevel | int | str
    max_allowed_level: DominionLevel | int | str
    dangerous_boundary_surfaces: list[str]
    dangerous_effect_surfaces: list[str]
    risk_signals: list[str]
    recommended_decision: DominionAuthorityDecisionType | str
    recommended_granted_level: DominionLevel | int | str | None
    rationale: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("evaluation_id", self.evaluation_id)
        _require_non_blank("request_id", self.request_id)
        _require_non_blank("target_id", self.target_id)
        _require_non_blank("rationale", self.rationale)
        normalize_dominion_level(self.requested_level)
        max_allowed = normalize_dominion_level(self.max_allowed_level)
        if max_allowed > V0304_MAX_GRANTABLE_LEVEL:
            raise ValueError("max_allowed_level cannot exceed D3_SIMULATE")
        if self.recommended_granted_level is not None:
            granted = normalize_dominion_level(self.recommended_granted_level)
            if granted > V0304_MAX_GRANTABLE_LEVEL:
                raise ValueError("recommended_granted_level cannot exceed D3_SIMULATE")
        _validate_string_list("dangerous_boundary_surfaces", self.dangerous_boundary_surfaces)
        _validate_string_list("dangerous_effect_surfaces", self.dangerous_effect_surfaces)
        _validate_string_list("risk_signals", self.risk_signals)
        _validate_string_list("evidence_refs", self.evidence_refs)
        decision = normalize_authority_decision_type(self.recommended_decision)
        if (self.dangerous_boundary_surfaces or self.dangerous_effect_surfaces) and decision in {
            DominionAuthorityDecisionType.OBSERVE_ONLY,
            DominionAuthorityDecisionType.DESCRIBE_ONLY,
            DominionAuthorityDecisionType.PLAN_ONLY,
            DominionAuthorityDecisionType.SIMULATE_ONLY,
        }:
            raise ValueError("dangerous surfaces must not produce allow-style authority recommendations")

    @property
    def grants_authority(self) -> bool:
        return False

    @property
    def mutates_runtime_state(self) -> bool:
        return False


@dataclass(frozen=True)
class DominionAuthorityDecision:
    decision_id: str
    request_id: str
    target_id: str
    requested_level: DominionLevel | int | str
    granted_level: DominionLevel | int | str | None
    decision: DominionAuthorityDecisionType | str
    granted_scope: DominionAuthorityScope | None
    reason: str
    evidence_refs: list[str] = field(default_factory=list)
    required_reviews: list[str] = field(default_factory=list)
    approval_required: bool = False
    approval_granted: bool = False
    human_review_required: bool = False
    future_gate_required: bool = False
    blocked_reasons: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("decision_id", self.decision_id)
        _require_non_blank("request_id", self.request_id)
        _require_non_blank("target_id", self.target_id)
        _require_non_blank("reason", self.reason)
        requested = normalize_dominion_level(self.requested_level)
        decision = normalize_authority_decision_type(self.decision)
        granted = normalize_dominion_level(self.granted_level) if self.granted_level is not None else None
        if granted is not None:
            if granted > V0304_MAX_GRANTABLE_LEVEL:
                raise ValueError("v0.30.4 authority decisions cannot grant D4+")
            if granted > requested:
                raise ValueError("granted_level must not exceed requested_level")
        if requested > V0304_MAX_GRANTABLE_LEVEL:
            if decision not in {
                DominionAuthorityDecisionType.DENY,
                DominionAuthorityDecisionType.DEFER,
                DominionAuthorityDecisionType.NO_OP,
                DominionAuthorityDecisionType.REQUIRE_REVIEW,
                DominionAuthorityDecisionType.FUTURE_TRACK,
                DominionAuthorityDecisionType.BLOCKED,
            }:
                raise ValueError("D4-D9 requests must remain deny/defer/review/future_track/blocked/no_op in v0.30.4")
        if decision is DominionAuthorityDecisionType.OBSERVE_ONLY and granted is not None and granted > DominionLevel.D0_OBSERVE:
            raise ValueError("observe_only grants at most D0_OBSERVE")
        if decision is DominionAuthorityDecisionType.DESCRIBE_ONLY and granted is not None and granted > DominionLevel.D1_DESCRIBE:
            raise ValueError("describe_only grants at most D1_DESCRIBE")
        if decision is DominionAuthorityDecisionType.PLAN_ONLY and granted is not None and granted > DominionLevel.D2_PLAN:
            raise ValueError("plan_only grants at most D2_PLAN")
        if decision is DominionAuthorityDecisionType.SIMULATE_ONLY and granted is not None and granted > DominionLevel.D3_SIMULATE:
            raise ValueError("simulate_only grants at most D3_SIMULATE")
        if decision is DominionAuthorityDecisionType.BLOCKED and not self.blocked_reasons:
            raise ValueError("blocked authority decision requires blocked_reasons")
        if decision is DominionAuthorityDecisionType.FUTURE_TRACK and not self.future_gate_required:
            raise ValueError("future_track authority decision requires future_gate_required=True")
        if self.approval_granted is True:
            raise ValueError("approval_granted must remain False in v0.30.4")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("required_reviews", self.required_reviews)
        _validate_string_list("blocked_reasons", self.blocked_reasons)
        _validate_string_list("withdrawal_conditions", self.withdrawal_conditions)
        if self.granted_scope is not None:
            if self.granted_scope.target_id != self.target_id:
                raise ValueError("granted_scope.target_id must match decision target_id")
            if granted is not None and normalize_dominion_level(self.granted_scope.max_level) < granted:
                raise ValueError("granted_scope.max_level must cover granted_level")

    @property
    def executes(self) -> bool:
        return False

    @property
    def grants_d4_plus(self) -> bool:
        return False

    @property
    def grants_permission(self) -> bool:
        return False

    @property
    def grants_dominion_authority(self) -> bool:
        return False


@dataclass(frozen=True)
class DominionAuthorityReviewRequirement:
    review_id: str
    request_id: str
    target_id: str
    requested_level: DominionLevel | int | str
    review_reasons: list[str]
    required_reviewers: list[str]
    evidence_refs: list[str] = field(default_factory=list)
    future_gate_required: bool = False
    blocked_until_review: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("review_id", self.review_id)
        _require_non_blank("request_id", self.request_id)
        _require_non_blank("target_id", self.target_id)
        normalize_dominion_level(self.requested_level)
        _validate_string_list("review_reasons", self.review_reasons)
        _validate_string_list("required_reviewers", self.required_reviewers)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if any("@" in reviewer or "\\" in reviewer or "/" in reviewer for reviewer in self.required_reviewers):
            raise ValueError("required_reviewers must be symbolic strings only")

    @property
    def approval_granted(self) -> bool:
        return False

    @property
    def grants_authority(self) -> bool:
        return False


def is_high_risk_authority_scope(scope: DominionAuthorityScope) -> bool:
    scope_kind = normalize_authority_scope_kind(scope.scope_kind)
    if scope_kind in CONSERVATIVE_SCOPE_KINDS:
        return True
    allowed_boundaries = {_normalize_boundary(surface) for surface in scope.allowed_boundary_surfaces}
    allowed_effects = {_normalize_effect(surface) for surface in scope.allowed_effect_surfaces}
    return bool(
        allowed_boundaries & DANGEROUS_AUTHORITY_BOUNDARY_SURFACES
        or allowed_effects & DANGEROUS_AUTHORITY_EFFECT_SURFACES
    )


def request_requires_future_gate(request: DominionAuthorityRequest) -> bool:
    requested = normalize_dominion_level(request.requested_level)
    return requested > V0304_MAX_GRANTABLE_LEVEL or is_high_risk_authority_scope(request.effective_scope)


def evaluate_dominion_authority_request(request: DominionAuthorityRequest) -> DominionAuthorityEvaluation:
    requested = normalize_dominion_level(request.requested_level)
    scope = request.effective_scope
    allowed_boundaries = {_normalize_boundary(surface) for surface in scope.allowed_boundary_surfaces}
    allowed_effects = {_normalize_effect(surface) for surface in scope.allowed_effect_surfaces}
    dangerous_boundaries = sorted(
        (surface.value for surface in allowed_boundaries & DANGEROUS_AUTHORITY_BOUNDARY_SURFACES),
    )
    dangerous_effects = sorted(
        (surface.value for surface in allowed_effects & DANGEROUS_AUTHORITY_EFFECT_SURFACES),
    )
    high_risk = is_high_risk_authority_scope(scope)
    future_gate = request_requires_future_gate(request)
    if normalize_authority_request_status(request.request_status) is DominionAuthorityRequestStatus.BLOCKED:
        recommended_decision = DominionAuthorityDecisionType.BLOCKED
        recommended_level = None
        rationale = "Authority request status is blocked."
    elif future_gate and requested > V0304_MAX_GRANTABLE_LEVEL:
        recommended_decision = DominionAuthorityDecisionType.FUTURE_TRACK
        recommended_level = None
        rationale = "D4-D9 authority requests remain future-track in v0.30.4."
    elif high_risk:
        recommended_decision = DominionAuthorityDecisionType.REQUIRE_REVIEW
        recommended_level = None
        rationale = "Authority scope is high risk and requires review without grant."
    elif requested == DominionLevel.D0_OBSERVE:
        recommended_decision = DominionAuthorityDecisionType.OBSERVE_ONLY
        recommended_level = DominionLevel.D0_OBSERVE
        rationale = "Observation-only authority is within v0.30.4 descriptive boundary."
    elif requested == DominionLevel.D1_DESCRIBE:
        recommended_decision = DominionAuthorityDecisionType.DESCRIBE_ONLY
        recommended_level = DominionLevel.D1_DESCRIBE
        rationale = "Description-only authority is within v0.30.4 boundary."
    elif requested == DominionLevel.D2_PLAN:
        recommended_decision = DominionAuthorityDecisionType.PLAN_ONLY
        recommended_level = DominionLevel.D2_PLAN
        rationale = "Planning-only authority is within v0.30.4 boundary."
    elif requested == DominionLevel.D3_SIMULATE:
        recommended_decision = DominionAuthorityDecisionType.SIMULATE_ONLY
        recommended_level = DominionLevel.D3_SIMULATE
        rationale = "Simulation-only authority is within v0.30.4 boundary."
    else:
        recommended_decision = DominionAuthorityDecisionType.DEFER
        recommended_level = None
        rationale = "Authority request cannot be evaluated into a grant."
    return DominionAuthorityEvaluation(
        evaluation_id=f"dominion_authority_evaluation:{request.request_id}",
        request_id=request.request_id,
        target_id=request.target_id,
        requested_level=requested,
        max_allowed_level=V0304_MAX_GRANTABLE_LEVEL,
        dangerous_boundary_surfaces=dangerous_boundaries,
        dangerous_effect_surfaces=dangerous_effects,
        risk_signals=list(request.metadata.get("risk_signals", [])),
        recommended_decision=recommended_decision,
        recommended_granted_level=recommended_level,
        rationale=rationale,
        evidence_refs=list(request.evidence_refs),
        metadata={"v0304_contract_only": True},
    )


def make_dominion_authority_decision(
    request: DominionAuthorityRequest,
    evaluation: DominionAuthorityEvaluation | None = None,
) -> DominionAuthorityDecision:
    evaluation = evaluation or evaluate_dominion_authority_request(request)
    decision_type = normalize_authority_decision_type(evaluation.recommended_decision)
    granted_level = (
        clamp_v0304_grant_level(evaluation.recommended_granted_level)
        if evaluation.recommended_granted_level is not None
        else None
    )
    granted_scope = request.effective_scope if granted_level is not None else None
    blocked_reasons: list[str] = []
    if decision_type is DominionAuthorityDecisionType.BLOCKED:
        blocked_reasons.append("authority request is blocked")
    if evaluation.dangerous_boundary_surfaces:
        blocked_reasons.extend(f"dangerous boundary: {surface}" for surface in evaluation.dangerous_boundary_surfaces)
    if evaluation.dangerous_effect_surfaces:
        blocked_reasons.extend(f"dangerous effect: {surface}" for surface in evaluation.dangerous_effect_surfaces)
    return DominionAuthorityDecision(
        decision_id=f"dominion_authority_decision:{request.request_id}",
        request_id=request.request_id,
        target_id=request.target_id,
        requested_level=normalize_dominion_level(request.requested_level),
        granted_level=granted_level,
        decision=decision_type,
        granted_scope=granted_scope,
        reason=evaluation.rationale,
        evidence_refs=list(evaluation.evidence_refs),
        required_reviews=(
            ["human_review", "authority_boundary_review"]
            if decision_type in {DominionAuthorityDecisionType.REQUIRE_REVIEW, DominionAuthorityDecisionType.FUTURE_TRACK}
            else []
        ),
        approval_required=decision_type
        in {DominionAuthorityDecisionType.REQUIRE_REVIEW, DominionAuthorityDecisionType.FUTURE_TRACK},
        approval_granted=False,
        human_review_required=decision_type is DominionAuthorityDecisionType.REQUIRE_REVIEW,
        future_gate_required=decision_type is DominionAuthorityDecisionType.FUTURE_TRACK,
        blocked_reasons=_unique(blocked_reasons),
        withdrawal_conditions=[
            "authority decision is treated as execution, runtime control, permission, approval, or D4+ grant",
            "approval_required or human_review_required is treated as approval_granted",
        ],
        validity_horizon="v0.30.4 contract only; expires if v0.30 authority gates change.",
        metadata={"v0304_contract_only": True},
    )


def make_review_requirement_from_request(
    request: DominionAuthorityRequest,
    reasons: list[str] | None = None,
) -> DominionAuthorityReviewRequirement:
    review_reasons = list(reasons or [])
    if not review_reasons:
        if request_requires_future_gate(request):
            review_reasons.append("future gate required")
        else:
            review_reasons.append("authority review required")
    return DominionAuthorityReviewRequirement(
        review_id=f"dominion_authority_review:{request.request_id}",
        request_id=request.request_id,
        target_id=request.target_id,
        requested_level=normalize_dominion_level(request.requested_level),
        review_reasons=review_reasons,
        required_reviewers=["human_authority_reviewer"],
        evidence_refs=list(request.evidence_refs),
        future_gate_required=request_requires_future_gate(request),
        blocked_until_review=True,
        metadata={"v0304_contract_only": True},
    )


def decision_preserves_v0304_boundary(decision: DominionAuthorityDecision) -> bool:
    if decision.approval_granted is True:
        return False
    if decision.granted_level is not None and not is_v0304_grantable_level(decision.granted_level):
        return False
    return decision.executes is False and decision.grants_permission is False and decision.grants_dominion_authority is False


def make_authority_request_from_assimilation_decision(
    decision: AssimilationDecision,
    requested_level: DominionLevel | int | str = DominionLevel.D3_SIMULATE,
) -> DominionAuthorityRequest:
    decision_type = AssimilationDecisionType(decision.decision)
    status = (
        DominionAuthorityRequestStatus.REVIEW_REQUIRED
        if decision_type is AssimilationDecisionType.DOMINION_REQUIRED
        else DominionAuthorityRequestStatus.REQUESTED
    )
    scope = make_default_authority_scope(
        decision.target_id,
        scope_kind=DominionAuthorityScopeKind.CANDIDATE_SCOPE,
        scope_id=f"dominion_authority_scope:{decision.candidate_id}",
        max_level=DominionLevel.D1_DESCRIBE if decision_type is AssimilationDecisionType.DOMINION_REQUIRED else DominionLevel.D2_PLAN,
        candidate_ids=[decision.candidate_id],
        report_ids=[decision.source_report_id],
        evidence_refs=decision.evidence_refs,
    )
    return DominionAuthorityRequest(
        request_id=f"dominion_authority_request:{decision.candidate_id}",
        target_id=decision.target_id,
        requested_level=requested_level,
        requested_scope=scope,
        requested_capabilities=[],
        source_kind="assimilation_decision",
        source_candidate_ids=[decision.candidate_id],
        source_report_ids=[decision.source_report_id],
        rationale="Authority review request derived from assimilation decision; not a grant.",
        evidence_refs=list(decision.evidence_refs),
        request_status=status,
        metadata={"dominion_review_required": decision.dominion_review_required, "v0304_contract_only": True},
    )


def make_authority_request_from_digestion_candidate(
    candidate: DigestionCandidate,
    requested_level: DominionLevel | int | str = DominionLevel.D2_PLAN,
) -> DominionAuthorityRequest:
    scope = make_default_authority_scope(
        candidate.target_id,
        scope_kind=DominionAuthorityScopeKind.CANDIDATE_SCOPE,
        scope_id=f"dominion_authority_scope:{candidate.candidate_id}",
        max_level=DominionLevel.D2_PLAN,
        capability_ids=list(candidate.source_capability_ids),
        candidate_ids=[candidate.candidate_id],
        report_ids=[candidate.source_report_id],
        evidence_refs=list(candidate.supporting_evidence_refs),
    )
    return DominionAuthorityRequest(
        request_id=f"dominion_authority_request:{candidate.candidate_id}",
        target_id=candidate.target_id,
        requested_level=requested_level,
        requested_scope=scope,
        requested_capabilities=list(candidate.source_capability_ids),
        source_kind="digestion_candidate",
        source_candidate_ids=[candidate.candidate_id],
        source_report_ids=[candidate.source_report_id],
        rationale="Authority request derived from digestion candidate; not a grant.",
        evidence_refs=list(candidate.supporting_evidence_refs),
        request_status=DominionAuthorityRequestStatus.EVIDENCE_LINKED
        if candidate.supporting_evidence_refs
        else DominionAuthorityRequestStatus.REVIEW_REQUIRED,
        metadata={"v0304_contract_only": True},
    )
