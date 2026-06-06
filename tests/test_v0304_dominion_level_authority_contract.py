from __future__ import annotations

import pytest

from chanta_core.external_dominion import (
    AssimilationDecisionType,
    DigestionCandidateKind,
    DigestionFeasibilityStatus,
    DominionAuthorityDecision,
    DominionAuthorityDecisionType,
    DominionAuthorityEvaluation,
    DominionAuthorityRequest,
    DominionAuthorityRequestStatus,
    DominionAuthorityReviewRequirement,
    DominionAuthorityScope,
    DominionAuthorityScopeKind,
    DominionLevel,
    ExternalBoundarySurface,
    ExternalEffectSurface,
    InternalArtifactCandidateKind,
    clamp_v0304_grant_level,
    compare_dominion_levels,
    decision_preserves_v0304_boundary,
    dominion_level_rank,
    evaluate_dominion_authority_request,
    is_high_risk_authority_scope,
    is_v0304_grantable_level,
    make_assimilation_decision,
    make_authority_request_from_assimilation_decision,
    make_authority_request_from_digestion_candidate,
    make_default_authority_scope,
    make_dominion_authority_decision,
    make_review_requirement_from_request,
    request_requires_future_gate,
    DigestionCandidate,
)


def _scope(**overrides) -> DominionAuthorityScope:
    data = {
        "scope_id": "dominion_authority_scope:target:external",
        "scope_kind": DominionAuthorityScopeKind.TARGET_SCOPE,
        "target_id": "target:external",
        "capability_ids": ["capability:read"],
        "candidate_ids": [],
        "report_ids": [],
        "allowed_boundary_surfaces": [],
        "prohibited_boundary_surfaces": [
            ExternalBoundarySurface.CREDENTIAL_BOUNDARY,
            ExternalBoundarySurface.NETWORK_BOUNDARY,
            ExternalBoundarySurface.COMMAND_BOUNDARY,
            ExternalBoundarySurface.BROWSER_BOUNDARY,
            ExternalBoundarySurface.RPA_BOUNDARY,
            ExternalBoundarySurface.GATEWAY_BOUNDARY,
            ExternalBoundarySurface.DELEGATION_BOUNDARY,
            ExternalBoundarySurface.PROVIDER_BOUNDARY,
        ],
        "allowed_effect_surfaces": [ExternalEffectSurface.READ_ONLY],
        "prohibited_effect_surfaces": [
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
        ],
        "max_level": DominionLevel.D2_PLAN,
        "expires_at": None,
        "evidence_refs": ["evidence:scope"],
        "metadata": {},
    }
    data.update(overrides)
    return DominionAuthorityScope(**data)


def _request(**overrides) -> DominionAuthorityRequest:
    data = {
        "request_id": "dominion_authority_request:target:external",
        "target_id": "target:external",
        "requested_level": DominionLevel.D2_PLAN,
        "requested_scope": _scope(),
        "requested_capabilities": ["describe capability"],
        "source_kind": "test",
        "source_ref": "source:not-fetched",
        "source_candidate_ids": [],
        "source_report_ids": ["report:observation"],
        "rationale": "Plan-only authority request.",
        "evidence_refs": ["evidence:scope"],
        "request_status": DominionAuthorityRequestStatus.EVIDENCE_LINKED,
        "metadata": {},
    }
    data.update(overrides)
    return DominionAuthorityRequest(**data)


def _decision(**overrides) -> DominionAuthorityDecision:
    data = {
        "decision_id": "dominion_authority_decision:target:external",
        "request_id": "dominion_authority_request:target:external",
        "target_id": "target:external",
        "requested_level": DominionLevel.D2_PLAN,
        "granted_level": DominionLevel.D2_PLAN,
        "decision": DominionAuthorityDecisionType.PLAN_ONLY,
        "granted_scope": _scope(max_level=DominionLevel.D2_PLAN),
        "reason": "Plan-only grant within v0.30.4 contract boundary.",
        "evidence_refs": ["evidence:scope"],
        "required_reviews": [],
        "approval_required": False,
        "approval_granted": False,
        "human_review_required": False,
        "future_gate_required": False,
        "blocked_reasons": [],
        "withdrawal_conditions": ["decision is treated as execution"],
        "validity_horizon": "v0.30.4",
        "metadata": {},
    }
    data.update(overrides)
    return DominionAuthorityDecision(**data)


def _candidate(**overrides) -> DigestionCandidate:
    data = {
        "candidate_id": "digestion_candidate:capability:provider",
        "target_id": "target:external",
        "source_report_id": "capability_observation_report:target:external",
        "source_capability_ids": ["capability:provider"],
        "candidate_kind": DigestionCandidateKind.PROVIDER_ADAPTER_PATTERN,
        "proposed_internal_artifact_kind": InternalArtifactCandidateKind.NONE,
        "title": "Provider candidate",
        "summary": "Dominion-required provider candidate.",
        "extracted_pattern": {"kind": "provider"},
        "supporting_evidence_refs": ["evidence:provider"],
        "risk_signals": [],
        "effect_surfaces": [],
        "boundary_surfaces": [],
        "feasibility_status": DigestionFeasibilityStatus.REQUIRES_DOMINION_REVIEW,
        "blocked_reasons": [],
        "assumptions": [],
        "withdrawal_conditions": [],
        "metadata": {},
    }
    data.update(overrides)
    return DigestionCandidate(**data)


def test_valid_authority_scope_creation_is_non_executable() -> None:
    scope = _scope()

    assert scope.max_level == DominionLevel.D2_PLAN
    assert scope.grants_execution is False
    assert scope.grants_permission is False
    assert ExternalBoundarySurface.NETWORK_BOUNDARY in scope.prohibited_boundary_surfaces
    assert ExternalEffectSurface.NETWORK_POSSIBLE in scope.prohibited_effect_surfaces


def test_authority_scope_rejects_blank_ids_and_d4_plus_max_level() -> None:
    with pytest.raises(ValueError, match="scope_id"):
        _scope(scope_id="")
    with pytest.raises(ValueError, match="target_id"):
        _scope(target_id=" ")
    with pytest.raises(ValueError, match="D3_SIMULATE"):
        _scope(max_level=DominionLevel.D4_EXECUTE_READ)


def test_authority_scope_preserves_dangerous_surface_prohibitions() -> None:
    with pytest.raises(ValueError, match="dangerous boundary"):
        _scope(allowed_boundary_surfaces=[ExternalBoundarySurface.NETWORK_BOUNDARY])
    with pytest.raises(ValueError, match="dangerous effect"):
        _scope(allowed_effect_surfaces=[ExternalEffectSurface.COMMAND_POSSIBLE])
    with pytest.raises(ValueError, match="prohibited dangerous boundary"):
        _scope(prohibited_boundary_surfaces=[])
    with pytest.raises(ValueError, match="prohibited dangerous effect"):
        _scope(prohibited_effect_surfaces=[])


def test_gateway_provider_rpa_delegation_and_unknown_scopes_are_conservative() -> None:
    for kind in [
        DominionAuthorityScopeKind.GATEWAY_SCOPE,
        DominionAuthorityScopeKind.PROVIDER_SCOPE,
        DominionAuthorityScopeKind.RPA_SCOPE,
        DominionAuthorityScopeKind.DELEGATION_SCOPE,
        DominionAuthorityScopeKind.UNKNOWN,
    ]:
        scope = _scope(scope_kind=kind, max_level=DominionLevel.D1_DESCRIBE)
        assert is_high_risk_authority_scope(scope) is True
        with pytest.raises(ValueError, match="conservative"):
            _scope(scope_kind=kind, max_level=DominionLevel.D2_PLAN)


def test_valid_authority_request_creation_and_legacy_shape_grants_nothing() -> None:
    request = _request()

    assert request.effective_scope.target_id == request.target_id
    assert request.source_ref_fetched is False
    assert request.grants_authority is False
    assert request.grants_permission is False

    legacy = DominionAuthorityRequest(
        "dominion_authority_request:legacy",
        "target:legacy",
        DominionLevel.D8_DELEGATE_AGENT,
        requested_capabilities=["delegate task"],
    )
    assert legacy.requested_level == DominionLevel.D8_DELEGATE_AGENT
    assert legacy.effective_scope.target_id == "target:legacy"
    assert legacy.grants_authority is False


def test_authority_request_validates_scope_match_and_evidence_linked_status() -> None:
    with pytest.raises(ValueError, match="request_id"):
        _request(request_id="")
    with pytest.raises(ValueError, match="target_id"):
        _request(target_id="")
    with pytest.raises(ValueError, match="target_id"):
        _request(requested_scope=_scope(target_id="target:other"))
    with pytest.raises(ValueError, match="evidence_refs"):
        _request(evidence_refs=[], request_status=DominionAuthorityRequestStatus.EVIDENCE_LINKED)


def test_authority_decision_creation_and_decision_level_ceilings() -> None:
    decision = _decision()

    assert decision.executes is False
    assert decision.grants_d4_plus is False
    assert decision.grants_permission is False
    assert decision.grants_dominion_authority is False
    assert decision_preserves_v0304_boundary(decision) is True

    with pytest.raises(ValueError, match="D4"):
        _decision(requested_level=DominionLevel.D4_EXECUTE_READ, granted_level=DominionLevel.D4_EXECUTE_READ)
    with pytest.raises(ValueError, match="observe_only"):
        _decision(decision=DominionAuthorityDecisionType.OBSERVE_ONLY, granted_level=DominionLevel.D1_DESCRIBE)
    with pytest.raises(ValueError, match="describe_only"):
        _decision(decision=DominionAuthorityDecisionType.DESCRIBE_ONLY, granted_level=DominionLevel.D2_PLAN)
    with pytest.raises(ValueError, match="plan_only"):
        _decision(
            requested_level=DominionLevel.D3_SIMULATE,
            decision=DominionAuthorityDecisionType.PLAN_ONLY,
            granted_level=DominionLevel.D3_SIMULATE,
        )
    with pytest.raises(ValueError, match="blocked"):
        _decision(
            decision=DominionAuthorityDecisionType.BLOCKED,
            granted_level=None,
            granted_scope=None,
            blocked_reasons=[],
        )
    with pytest.raises(ValueError, match="future_gate_required"):
        _decision(
            decision=DominionAuthorityDecisionType.FUTURE_TRACK,
            requested_level=DominionLevel.D7_EXECUTE_NETWORK_PREVIEW,
            granted_level=None,
            granted_scope=None,
            future_gate_required=False,
        )
    with pytest.raises(ValueError, match="approval_granted"):
        _decision(approval_required=True, approval_granted=True)


def test_d4_to_d9_requests_cannot_receive_d4_plus_grants() -> None:
    for requested_level in [
        DominionLevel.D4_EXECUTE_READ,
        DominionLevel.D5_EXECUTE_WRITE_PROPOSAL,
        DominionLevel.D6_EXECUTE_SANDBOX,
        DominionLevel.D7_EXECUTE_NETWORK_PREVIEW,
        DominionLevel.D8_DELEGATE_AGENT,
        DominionLevel.D9_GATEWAY_CONTROL,
    ]:
        request = _request(requested_level=requested_level)
        evaluation = evaluate_dominion_authority_request(request)
        decision = make_dominion_authority_decision(request, evaluation)

        assert decision.decision in {
            DominionAuthorityDecisionType.FUTURE_TRACK,
            DominionAuthorityDecisionType.DEFER,
            DominionAuthorityDecisionType.DENY,
            DominionAuthorityDecisionType.REQUIRE_REVIEW,
            DominionAuthorityDecisionType.BLOCKED,
            DominionAuthorityDecisionType.NO_OP,
        }
        assert decision.granted_level is None or decision.granted_level <= DominionLevel.D3_SIMULATE
        assert decision.grants_d4_plus is False
        assert decision.future_gate_required is True
        assert request_requires_future_gate(request) is True


def test_observe_describe_plan_simulate_helper_outputs_preserve_ceilings() -> None:
    cases = [
        (DominionLevel.D0_OBSERVE, DominionAuthorityDecisionType.OBSERVE_ONLY),
        (DominionLevel.D1_DESCRIBE, DominionAuthorityDecisionType.DESCRIBE_ONLY),
        (DominionLevel.D2_PLAN, DominionAuthorityDecisionType.PLAN_ONLY),
        (DominionLevel.D3_SIMULATE, DominionAuthorityDecisionType.SIMULATE_ONLY),
    ]
    for level, decision_type in cases:
        scope = _scope(max_level=level)
        request = _request(requested_level=level, requested_scope=scope)
        decision = make_dominion_authority_decision(request)

        assert decision.decision == decision_type
        assert decision.granted_level == level
        assert decision.granted_level <= DominionLevel.D3_SIMULATE
        assert decision.executes is False


def test_review_requirement_and_evaluation_are_advisory_only() -> None:
    request = _request(requested_level=DominionLevel.D7_EXECUTE_NETWORK_PREVIEW)
    evaluation = evaluate_dominion_authority_request(request)
    review = make_review_requirement_from_request(request)

    assert evaluation.grants_authority is False
    assert evaluation.mutates_runtime_state is False
    assert evaluation.recommended_granted_level is None
    assert review.approval_granted is False
    assert review.grants_authority is False
    assert review.future_gate_required is True
    assert review.blocked_until_review is True

    with pytest.raises(ValueError, match="review_id"):
        DominionAuthorityReviewRequirement("", request.request_id, request.target_id, request.requested_level, [], [])
    with pytest.raises(ValueError, match="request_id"):
        DominionAuthorityReviewRequirement("review:bad", "", request.target_id, request.requested_level, [], [])
    with pytest.raises(ValueError, match="target_id"):
        DominionAuthorityReviewRequirement("review:bad", request.request_id, "", request.requested_level, [], [])
    with pytest.raises(ValueError, match="symbolic"):
        DominionAuthorityReviewRequirement(
            "review:bad",
            request.request_id,
            request.target_id,
            request.requested_level,
            [],
            ["person@example.com"],
        )

    with pytest.raises(ValueError, match="evaluation_id"):
        DominionAuthorityEvaluation(
            "",
            request.request_id,
            request.target_id,
            request.requested_level,
            DominionLevel.D3_SIMULATE,
            [],
            [],
            [],
            DominionAuthorityDecisionType.FUTURE_TRACK,
            None,
            "future-track",
        )
    with pytest.raises(ValueError, match="D3"):
        DominionAuthorityEvaluation(
            "evaluation:bad",
            request.request_id,
            request.target_id,
            request.requested_level,
            DominionLevel.D4_EXECUTE_READ,
            [],
            [],
            [],
            DominionAuthorityDecisionType.FUTURE_TRACK,
            None,
            "future-track",
        )
    with pytest.raises(ValueError, match="recommended_granted_level"):
        DominionAuthorityEvaluation(
            "evaluation:bad",
            request.request_id,
            request.target_id,
            request.requested_level,
            DominionLevel.D3_SIMULATE,
            [],
            [],
            [],
            DominionAuthorityDecisionType.FUTURE_TRACK,
            DominionLevel.D7_EXECUTE_NETWORK_PREVIEW,
            "future-track",
        )
    with pytest.raises(ValueError, match="dangerous surfaces"):
        DominionAuthorityEvaluation(
            "evaluation:bad",
            request.request_id,
            request.target_id,
            DominionLevel.D1_DESCRIBE,
            DominionLevel.D3_SIMULATE,
            [ExternalBoundarySurface.NETWORK_BOUNDARY],
            [],
            [],
            DominionAuthorityDecisionType.DESCRIBE_ONLY,
            DominionLevel.D1_DESCRIBE,
            "unsafe allow-style recommendation",
        )


@pytest.mark.parametrize(
    ("requested_level", "scope_kind"),
    [
        (DominionLevel.D7_EXECUTE_NETWORK_PREVIEW, DominionAuthorityScopeKind.PROVIDER_SCOPE),
        (DominionLevel.D9_GATEWAY_CONTROL, DominionAuthorityScopeKind.GATEWAY_SCOPE),
        (DominionLevel.D6_EXECUTE_SANDBOX, DominionAuthorityScopeKind.TARGET_SCOPE),
        (DominionLevel.D9_GATEWAY_CONTROL, DominionAuthorityScopeKind.RPA_SCOPE),
        (DominionLevel.D7_EXECUTE_NETWORK_PREVIEW, DominionAuthorityScopeKind.TARGET_SCOPE),
        (DominionLevel.D8_DELEGATE_AGENT, DominionAuthorityScopeKind.DELEGATION_SCOPE),
    ],
)
def test_negative_runtime_authority_requests_do_not_receive_runtime_grants(
    requested_level: DominionLevel,
    scope_kind: DominionAuthorityScopeKind,
) -> None:
    max_level = DominionLevel.D1_DESCRIBE if scope_kind in {
        DominionAuthorityScopeKind.PROVIDER_SCOPE,
        DominionAuthorityScopeKind.GATEWAY_SCOPE,
        DominionAuthorityScopeKind.RPA_SCOPE,
        DominionAuthorityScopeKind.DELEGATION_SCOPE,
    } else DominionLevel.D2_PLAN
    scope = _scope(scope_kind=scope_kind, max_level=max_level)
    request = _request(requested_level=requested_level, requested_scope=scope)
    decision = make_dominion_authority_decision(request)

    assert decision.granted_level is None or decision.granted_level <= DominionLevel.D3_SIMULATE
    assert decision.grants_d4_plus is False
    assert decision.executes is False
    assert decision.approval_granted is False
    assert decision.decision in {
        DominionAuthorityDecisionType.FUTURE_TRACK,
        DominionAuthorityDecisionType.REQUIRE_REVIEW,
        DominionAuthorityDecisionType.DEFER,
        DominionAuthorityDecisionType.DENY,
        DominionAuthorityDecisionType.NO_OP,
        DominionAuthorityDecisionType.BLOCKED,
    }


def test_interaction_with_v0303_dominion_required_decision_requests_review_only() -> None:
    candidate = _candidate()
    assimilation = make_assimilation_decision(candidate)

    assert assimilation.decision == AssimilationDecisionType.DOMINION_REQUIRED
    authority_request = make_authority_request_from_assimilation_decision(
        assimilation,
        requested_level=DominionLevel.D7_EXECUTE_NETWORK_PREVIEW,
    )
    decision = make_dominion_authority_decision(authority_request)

    assert authority_request.grants_authority is False
    assert decision.decision == DominionAuthorityDecisionType.FUTURE_TRACK
    assert decision.granted_level is None
    assert decision.grants_dominion_authority is False

    candidate_request = make_authority_request_from_digestion_candidate(
        candidate,
        requested_level=DominionLevel.D2_PLAN,
    )
    candidate_decision = make_dominion_authority_decision(candidate_request)
    assert candidate_request.grants_authority is False
    assert candidate_decision.granted_level is None or candidate_decision.granted_level <= DominionLevel.D3_SIMULATE


def test_level_helpers_are_conservative() -> None:
    assert dominion_level_rank(DominionLevel.D3_SIMULATE) == 3
    assert compare_dominion_levels(DominionLevel.D2_PLAN, DominionLevel.D3_SIMULATE) == -1
    assert compare_dominion_levels(DominionLevel.D3_SIMULATE, DominionLevel.D3_SIMULATE) == 0
    assert compare_dominion_levels(DominionLevel.D9_GATEWAY_CONTROL, DominionLevel.D3_SIMULATE) == 1
    assert is_v0304_grantable_level(DominionLevel.D3_SIMULATE) is True
    assert is_v0304_grantable_level(DominionLevel.D4_EXECUTE_READ) is False
    assert clamp_v0304_grant_level(DominionLevel.D2_PLAN) == DominionLevel.D2_PLAN
    assert clamp_v0304_grant_level(DominionLevel.D9_GATEWAY_CONTROL) is None
