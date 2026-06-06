from __future__ import annotations

import pytest

from chanta_core.external_dominion import (
    DominionLevel,
    ExternalDelegationHandoffPreview,
    ExternalDominionApprovalCandidate,
    ExternalDominionApprovalDecisionRecord,
    ExternalDominionApprovalDecisionType,
    ExternalDominionApprovalRequirement,
    ExternalDominionApprovalRequirementStatus,
    ExternalDominionAuditEventKind,
    ExternalDominionAuditPolicy,
    ExternalDominionAuditTrailPlan,
    ExternalDominionFailureClass,
    ExternalDominionFailureClassification,
    ExternalDominionNoOpBoundary,
    ExternalDominionOCELTracePlan,
    ExternalDominionResultBoundaryAction,
    ExternalDominionResultBoundaryPolicy,
    ExternalDominionRetryDeferralPolicy,
    ExternalDominionRollbackPlan,
    ExternalDominionV0307CertificationHandoff,
    approval_boundary_preserves_v0306_no_execution,
    audit_policy_preserves_no_raw_secret_logging,
    build_audit_policy_for_candidate,
    build_audit_trail_plan,
    build_no_op_boundary,
    build_ocel_trace_plan_for_candidate,
    build_result_boundary_policy,
    build_retry_deferral_policy,
    build_rollback_plan,
    build_v0307_certification_handoff,
    classify_external_dominion_failure,
    high_risk_approval_decision_type,
    make_approval_candidate,
    make_approval_decision_record,
    make_approval_requirement_from_delegation_handoff,
    result_boundary_rejects_raw_memory_persistence,
    rollback_plan_preserves_no_execution,
)


def _handoff(**overrides) -> ExternalDelegationHandoffPreview:
    data = {
        "handoff_id": "external_delegation_handoff_preview:candidate:1",
        "candidate_id": "candidate:1",
        "target_id": "target:external",
        "dry_run_plan_id": "dry_run_plan:1",
        "dry_run_report_id": "dry_run_report:1",
        "no_op_plan_id": None,
        "next_stage": "v0.30.6 approval/audit/rollback boundary",
        "ready_for_v0306_approval_audit_boundary": True,
        "ready_for_execution": False,
        "evidence_refs": ["evidence:dry_run"],
        "withdrawal_conditions": ["handoff is treated as execution"],
        "metadata": {"requested_level": DominionLevel.D3_SIMULATE},
    }
    data.update(overrides)
    return ExternalDelegationHandoffPreview(**data)


def _requirement(**overrides) -> ExternalDominionApprovalRequirement:
    data = {
        "requirement_id": "approval_requirement:1",
        "target_id": "target:external",
        "candidate_id": "candidate:1",
        "dry_run_plan_id": "dry_run_plan:1",
        "dry_run_report_id": "dry_run_report:1",
        "requested_level": DominionLevel.D3_SIMULATE,
        "status": ExternalDominionApprovalRequirementStatus.REQUIRED,
        "required_evidence_refs": ["evidence:dry_run"],
        "required_reviews": ["human_review"],
        "required_boundary_checks": ["audit_policy", "result_boundary"],
        "required_result_boundary_actions": [
            ExternalDominionResultBoundaryAction.REJECT_RAW_OUTPUT,
            ExternalDominionResultBoundaryAction.REQUIRE_RESULT_ENVELOPE,
            ExternalDominionResultBoundaryAction.REQUIRE_NO_MEMORY_PERSISTENCE,
        ],
        "requires_human_review": True,
        "requires_future_gate": False,
        "reason": "Approval boundary requirement only.",
        "metadata": {},
    }
    data.update(overrides)
    return ExternalDominionApprovalRequirement(**data)


def _candidate(**overrides) -> ExternalDominionApprovalCandidate:
    data = {
        "approval_candidate_id": "approval_candidate:1",
        "requirement_id": "approval_requirement:1",
        "target_id": "target:external",
        "candidate_id": "candidate:1",
        "requested_decision": ExternalDominionApprovalDecisionType.REQUIRE_HUMAN_REVIEW,
        "requested_level": DominionLevel.D3_SIMULATE,
        "proposed_scope_refs": [],
        "evidence_refs": ["evidence:dry_run"],
        "unresolved_risks": [],
        "blocked_reasons": [],
        "ready_for_decision_record": True,
        "ready_for_execution": False,
        "metadata": {},
    }
    data.update(overrides)
    return ExternalDominionApprovalCandidate(**data)


def _decision(**overrides) -> ExternalDominionApprovalDecisionRecord:
    data = {
        "approval_decision_id": "approval_decision:1",
        "approval_candidate_id": "approval_candidate:1",
        "requirement_id": "approval_requirement:1",
        "target_id": "target:external",
        "decision": ExternalDominionApprovalDecisionType.REQUIRE_HUMAN_REVIEW,
        "approved_for_certification_review": False,
        "approved_for_execution": False,
        "reason": "Human review required; no execution approval.",
        "evidence_refs": ["evidence:dry_run"],
        "reviewer_refs": [],
        "required_next_stage": "v0.30.7 certification matrix",
        "future_gate_required": False,
        "blocked_reasons": [],
        "withdrawal_conditions": ["decision is treated as execution"],
        "metadata": {},
    }
    data.update(overrides)
    return ExternalDominionApprovalDecisionRecord(**data)


def test_approval_requirement_creation_and_future_gate_validation() -> None:
    requirement = _requirement()

    assert requirement.approval_granted is False
    assert requirement.approves_execution is False

    with pytest.raises(ValueError, match="requirement_id"):
        _requirement(requirement_id="")
    with pytest.raises(ValueError, match="target_id"):
        _requirement(target_id="")
    with pytest.raises(ValueError, match="reason"):
        _requirement(reason=" ")
    with pytest.raises(ValueError, match="future gate"):
        _requirement(requested_level=DominionLevel.D8_DELEGATE_AGENT, requires_future_gate=False)

    future = _requirement(requested_level=DominionLevel.D8_DELEGATE_AGENT, requires_future_gate=True)
    assert future.requires_future_gate is True


def test_approval_candidate_and_decision_never_approve_execution() -> None:
    candidate = _candidate()

    assert candidate.ready_for_execution is False
    assert candidate.approval_granted is False
    assert approval_boundary_preserves_v0306_no_execution(candidate) is True

    with pytest.raises(ValueError, match="ready_for_execution"):
        _candidate(ready_for_execution=True)
    with pytest.raises(ValueError, match="future gate"):
        _candidate(
            requested_decision=ExternalDominionApprovalDecisionType.ALLOW_CERTIFICATION_REVIEW,
            unresolved_risks=["provider network credential delegation risk"],
            metadata={},
        )

    cert_candidate = _candidate(
        requested_decision=ExternalDominionApprovalDecisionType.ALLOW_CERTIFICATION_REVIEW,
        unresolved_risks=["provider risk"],
        metadata={"future_gate_required": True},
    )
    assert cert_candidate.ready_for_execution is False

    decision = _decision(
        decision=ExternalDominionApprovalDecisionType.ALLOW_CERTIFICATION_REVIEW,
        approved_for_certification_review=True,
    )
    assert decision.approved_for_certification_review is True
    assert decision.approved_for_execution is False
    assert decision.executes is False
    assert approval_boundary_preserves_v0306_no_execution(decision) is True

    with pytest.raises(ValueError, match="approved_for_execution"):
        _decision(approved_for_execution=True)
    with pytest.raises(ValueError, match="approved_for_certification_review"):
        _decision(approved_for_certification_review=True)
    with pytest.raises(ValueError, match="blocked_reasons"):
        _decision(decision=ExternalDominionApprovalDecisionType.BLOCKED)
    with pytest.raises(ValueError, match="future_gate_required"):
        _decision(decision=ExternalDominionApprovalDecisionType.FUTURE_TRACK, future_gate_required=False)


def test_audit_policy_trail_and_ocel_trace_are_plans_only() -> None:
    policy = ExternalDominionAuditPolicy(
        "audit_policy:1",
        "target:external",
        "candidate:1",
        required_event_kinds=[ExternalDominionAuditEventKind.APPROVAL_REQUIREMENT_CREATED],
    )
    assert policy.require_ocel_visibility is True
    assert policy.require_append_only is True
    assert policy.prohibit_raw_payload_logging is True
    assert policy.prohibit_secret_logging is True
    assert policy.executes_audit is False
    assert audit_policy_preserves_no_raw_secret_logging(policy) is True

    with pytest.raises(ValueError, match="prohibit_raw_payload_logging"):
        ExternalDominionAuditPolicy("audit_policy:bad", "target:external", None, prohibit_raw_payload_logging=False)
    with pytest.raises(ValueError, match="prohibit_secret_logging"):
        ExternalDominionAuditPolicy("audit_policy:bad", "target:external", None, prohibit_secret_logging=False)

    trail = ExternalDominionAuditTrailPlan(
        "audit_trail_plan:1",
        policy.audit_policy_id,
        "target:external",
        "candidate:1",
        [ExternalDominionAuditEventKind.APPROVAL_DECISION_RECORDED],
        ["candidate:1"],
        ["evidence:dry_run"],
    )
    assert trail.no_raw_payload_guarantee is True
    assert trail.no_secret_logging_guarantee is True
    assert trail.emits_events is False

    trace = ExternalDominionOCELTracePlan(
        "ocel_trace_plan:1",
        "target:external",
        "candidate:1",
        "external_dominion_boundary",
        ["approval_decision_recorded"],
        ["external_target"],
        ["references"],
    )
    assert trace.ocel_visibility_required is True
    assert trace.emits_events is False


def test_result_boundary_defaults_reject_raw_output_and_memory_persistence() -> None:
    policy = ExternalDominionResultBoundaryPolicy("result_boundary:1", "target:external", "candidate:1")

    assert policy.raw_output_allowed is False
    assert policy.memory_persistence_allowed is False
    assert policy.result_envelope_required is True
    assert policy.evidence_required is True
    assert policy.ingests_result is False
    assert result_boundary_rejects_raw_memory_persistence(policy) is True

    with pytest.raises(ValueError, match="raw_output_allowed"):
        ExternalDominionResultBoundaryPolicy("result_boundary:bad", "target:external", None, raw_output_allowed=True)
    with pytest.raises(ValueError, match="memory_persistence_allowed"):
        ExternalDominionResultBoundaryPolicy("result_boundary:bad", "target:external", None, memory_persistence_allowed=True)
    with pytest.raises(ValueError, match="reject raw output"):
        ExternalDominionResultBoundaryPolicy(
            "result_boundary:bad",
            "target:external",
            None,
            required_actions=[ExternalDominionResultBoundaryAction.REQUIRE_RESULT_ENVELOPE],
        )


def test_rollback_noop_failure_retry_and_handoff_boundaries() -> None:
    rollback = ExternalDominionRollbackPlan("rollback:1", "target:external", "candidate:1")
    assert rollback.no_rollback_execution_guarantee is True
    assert rollback.fallback_no_op_required is True
    assert rollback.executes_rollback is False
    assert rollback_plan_preserves_no_execution(rollback) is True

    with pytest.raises(ValueError, match="no_rollback_execution_guarantee"):
        ExternalDominionRollbackPlan("rollback:bad", "target:external", None, no_rollback_execution_guarantee=False)
    with pytest.raises(ValueError, match="fallback_no_op_required"):
        ExternalDominionRollbackPlan(
            "rollback:bad",
            "target:external",
            None,
            rollback_available=False,
            fallback_no_op_required=False,
        )

    no_op = ExternalDominionNoOpBoundary("noop:1", "target:external", "candidate:1", "No safe approval path.")
    assert no_op.is_failure is False
    assert no_op.executes is False

    failure = ExternalDominionFailureClassification(
        "failure:1",
        "target:external",
        "candidate:1",
        ExternalDominionFailureClass.NETWORK_RISK,
        "Network risk remains future-gated.",
    )
    assert failure.retry_allowed is False
    assert failure.retry_deferred is True
    assert failure.retries is False

    retry = ExternalDominionRetryDeferralPolicy("retry:1", "target:external")
    assert retry.retry_allowed_now is False
    assert retry.max_retry_count == 0
    assert retry.retries is False

    with pytest.raises(ValueError, match="max_retry_count"):
        ExternalDominionRetryDeferralPolicy("retry:bad", "target:external", max_retry_count=1)

    with pytest.raises(ValueError, match="requires approval"):
        ExternalDominionV0307CertificationHandoff(
            "handoff:bad",
            "target:external",
            "candidate:1",
            None,
            None,
            None,
            None,
            None,
            True,
            False,
        )
    with pytest.raises(ValueError, match="ready_for_execution"):
        ExternalDominionV0307CertificationHandoff(
            "handoff:bad",
            "target:external",
            "candidate:1",
            None,
            None,
            None,
            None,
            None,
            False,
            True,
        )


def test_helpers_build_contract_artifacts_only() -> None:
    handoff = _handoff()
    requirement = make_approval_requirement_from_delegation_handoff(handoff)
    candidate = make_approval_candidate(requirement)
    decision = make_approval_decision_record(
        candidate,
        ExternalDominionApprovalDecisionType.REQUIRE_HUMAN_REVIEW,
        "Human review required before certification review.",
    )
    audit_policy = build_audit_policy_for_candidate(requirement)
    audit_trail = build_audit_trail_plan(audit_policy)
    trace_plan = build_ocel_trace_plan_for_candidate(requirement)
    result_boundary = build_result_boundary_policy(requirement)
    rollback_plan = build_rollback_plan(requirement)
    no_op = build_no_op_boundary(requirement, "No-op remains valid.")
    failure = classify_external_dominion_failure(
        "target:external",
        "candidate:1",
        ExternalDominionFailureClass.PROVIDER_RISK,
        "Provider risk cannot receive execution approval.",
    )
    retry = build_retry_deferral_policy("target:external", "candidate:1")
    certification = build_v0307_certification_handoff(
        "target:external",
        "candidate:1",
        approval_decision=decision,
        audit_policy=audit_policy,
        result_boundary_policy=result_boundary,
        rollback_plan=rollback_plan,
        evidence_refs=["evidence:dry_run"],
    )

    assert requirement.approval_granted is False
    assert candidate.ready_for_execution is False
    assert decision.approved_for_execution is False
    assert audit_trail.emits_events is False
    assert trace_plan.emits_events is False
    assert result_boundary.ingests_result is False
    assert rollback_plan.executes_rollback is False
    assert no_op.executes is False
    assert failure.retries is False
    assert retry.retries is False
    assert certification.ready_for_v0307_certification_matrix is True
    assert certification.ready_for_execution is False
    assert certification.is_certification is False


def test_high_risk_provider_network_credential_command_browser_rpa_gateway_delegation_gets_no_execution_approval() -> None:
    risk_terms = [
        "provider risk",
        "network risk",
        "credential risk",
        "command risk",
        "browser risk",
        "rpa risk",
        "gateway risk",
        "delegation risk",
    ]

    assert high_risk_approval_decision_type(risk_terms) is ExternalDominionApprovalDecisionType.REQUIRE_HUMAN_REVIEW
    candidate = _candidate(
        requested_decision=ExternalDominionApprovalDecisionType.REQUIRE_HUMAN_REVIEW,
        unresolved_risks=risk_terms,
        metadata={"future_gate_required": True},
    )
    decision = make_approval_decision_record(
        candidate,
        ExternalDominionApprovalDecisionType.REQUIRE_HUMAN_REVIEW,
        "High-risk surfaces require review only.",
    )

    assert candidate.ready_for_execution is False
    assert decision.approved_for_execution is False
    assert decision.approved_for_certification_review is False
