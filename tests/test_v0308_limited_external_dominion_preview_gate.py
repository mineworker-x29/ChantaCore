from __future__ import annotations

import pytest

from chanta_core.external_dominion import (
    DominionLevel,
    ExternalDominionV0308PreviewGateHandoff,
    ExternalDominionV0309ConsolidationHandoff,
    LimitedExternalDominionPreviewAuditOCELPlan,
    LimitedExternalDominionPreviewCandidate,
    LimitedExternalDominionPreviewDecision,
    LimitedExternalDominionPreviewDecisionType,
    LimitedExternalDominionPreviewDenyDeferReason,
    LimitedExternalDominionPreviewEligibilityMatrix,
    LimitedExternalDominionPreviewGateReport,
    LimitedExternalDominionPreviewGateStatus,
    LimitedExternalDominionPreviewNoOpPlan,
    LimitedExternalDominionPreviewScope,
    LimitedExternalDominionPreviewScopeKind,
    build_limited_preview_candidate,
    build_preview_audit_ocel_plan,
    build_preview_eligibility_matrix_from_certification_handoff,
    build_preview_gate_report,
    build_preview_no_op_plan,
    build_preview_scope_from_eligibility,
    build_v0309_consolidation_handoff,
    make_limited_preview_decision,
    preview_decision_preserves_execution_false,
    preview_gate_allows_consolidation_only,
    preview_gate_preserves_no_execution,
    preview_scope_blocks_runtime_actions,
)


def _handoff(**overrides) -> ExternalDominionV0308PreviewGateHandoff:
    data = {
        "handoff_id": "v0308_handoff:1",
        "target_id": "target:external",
        "candidate_id": "candidate:1",
        "certification_matrix_id": "certification_matrix:1",
        "certification_report_id": "certification_report:1",
        "ready_for_v0308_limited_preview_gate_review": True,
        "ready_for_limited_preview_execution": False,
        "ready_for_execution": False,
        "production_certified": False,
        "live_adapter_certified": False,
        "unresolved_requirements": [],
        "limitations": [],
        "evidence_refs": ["evidence:certification"],
        "withdrawal_conditions": ["handoff is treated as execution"],
        "metadata": {},
    }
    data.update(overrides)
    return ExternalDominionV0308PreviewGateHandoff(**data)


def _eligibility(**overrides) -> LimitedExternalDominionPreviewEligibilityMatrix:
    data = {
        "eligibility_matrix_id": "preview_eligibility:1",
        "target_id": "target:external",
        "candidate_id": "candidate:1",
        "certification_matrix_id": "certification_matrix:1",
        "certification_report_id": "certification_report:1",
        "required_gate_conditions": ["certification matrix present"],
        "passed_gate_conditions": ["certification matrix present"],
        "failed_gate_conditions": [],
        "unresolved_gate_conditions": [],
        "deny_defer_reasons": [],
        "ready_for_gate_review": True,
        "ready_for_v0309_consolidation": True,
        "ready_for_limited_preview_execution": False,
        "ready_for_execution": False,
        "production_certified": False,
        "live_adapter_certified": False,
        "evidence_refs": ["evidence:certification"],
        "metadata": {},
    }
    data.update(overrides)
    return LimitedExternalDominionPreviewEligibilityMatrix(**data)


def _scope(**overrides) -> LimitedExternalDominionPreviewScope:
    data = {
        "preview_scope_id": "preview_scope:1",
        "target_id": "target:external",
        "candidate_id": "candidate:1",
        "scope_kind": LimitedExternalDominionPreviewScopeKind.CERTIFICATION_MATRIX_PREVIEW,
        "allowed_artifact_refs": ["certification_matrix:1"],
        "max_allowed_level": DominionLevel.D3_SIMULATE,
        "evidence_refs": ["evidence:certification"],
        "limitations": [],
        "metadata": {},
    }
    data.update(overrides)
    return LimitedExternalDominionPreviewScope(**data)


def _candidate(**overrides) -> LimitedExternalDominionPreviewCandidate:
    scope = _scope()
    data = {
        "preview_candidate_id": "preview_candidate:1",
        "target_id": "target:external",
        "candidate_id": "candidate:1",
        "eligibility_matrix_id": "preview_eligibility:1",
        "preview_scope": scope,
        "requested_preview_kind": LimitedExternalDominionPreviewScopeKind.CERTIFICATION_MATRIX_PREVIEW,
        "source_certification_report_id": "certification_report:1",
        "source_handoff_id": "v0308_handoff:1",
        "evidence_refs": ["evidence:certification"],
        "limitations": [],
        "unresolved_requirements": [],
        "requested_execution": False,
        "ready_for_execution": False,
        "metadata": {},
    }
    data.update(overrides)
    return LimitedExternalDominionPreviewCandidate(**data)


def _decision(**overrides) -> LimitedExternalDominionPreviewDecision:
    data = {
        "preview_decision_id": "preview_decision:1",
        "preview_candidate_id": "preview_candidate:1",
        "target_id": "target:external",
        "decision": LimitedExternalDominionPreviewDecisionType.PASS_FOR_V0309_CONSOLIDATION,
        "status": LimitedExternalDominionPreviewGateStatus.GATE_PASSED_FOR_CONSOLIDATION,
        "approved_for_v0309_consolidation": True,
        "approved_for_limited_preview_execution": False,
        "approved_for_execution": False,
        "reason": "Consolidation-only pass.",
        "limitations": [],
        "deny_defer_reasons": [],
        "required_followups": [],
        "future_gate_required": False,
        "evidence_refs": ["evidence:certification"],
        "withdrawal_conditions": ["decision is treated as execution"],
        "metadata": {},
    }
    data.update(overrides)
    return LimitedExternalDominionPreviewDecision(**data)


def test_preview_eligibility_matrix_validation_and_boundaries() -> None:
    matrix = _eligibility()

    assert matrix.ready_for_v0309_consolidation is True
    assert matrix.ready_for_limited_preview_execution is False
    assert matrix.ready_for_execution is False
    assert matrix.production_certified is False
    assert matrix.live_adapter_certified is False
    assert matrix.approves_execution is False
    assert preview_gate_preserves_no_execution(matrix) is True

    with pytest.raises(ValueError, match="eligibility_matrix_id"):
        _eligibility(eligibility_matrix_id="")
    with pytest.raises(ValueError, match="target_id"):
        _eligibility(target_id="")
    with pytest.raises(TypeError, match="required_gate_conditions"):
        _eligibility(required_gate_conditions="not-list")
    with pytest.raises(ValueError, match="ready_for_limited_preview_execution"):
        _eligibility(ready_for_limited_preview_execution=True)
    with pytest.raises(ValueError, match="ready_for_execution"):
        _eligibility(ready_for_execution=True)
    with pytest.raises(ValueError, match="production_certified"):
        _eligibility(production_certified=True)
    with pytest.raises(ValueError, match="live_adapter_certified"):
        _eligibility(live_adapter_certified=True)
    with pytest.raises(ValueError, match="passed gate review conditions"):
        _eligibility(failed_gate_conditions=["missing result boundary"], ready_for_v0309_consolidation=True)


def test_preview_scope_blocks_runtime_actions_and_d3_ceiling() -> None:
    scope = _scope()

    assert scope.max_allowed_level == DominionLevel.D3_SIMULATE
    assert scope.allows_execution is False
    assert preview_scope_blocks_runtime_actions(scope) is True
    for action in [
        "external execution",
        "network access",
        "credential access",
        "command execution",
        "provider invocation",
        "browser automation",
        "RPA control",
        "gateway control",
        "packet send",
        "rollback execution",
    ]:
        assert action in scope.prohibited_runtime_actions

    with pytest.raises(ValueError, match="preview_scope_id"):
        _scope(preview_scope_id="")
    with pytest.raises(ValueError, match="target_id"):
        _scope(target_id="")
    with pytest.raises(ValueError, match="D3_SIMULATE"):
        _scope(max_allowed_level=DominionLevel.D7_EXECUTE_NETWORK_PREVIEW)
    with pytest.raises(ValueError, match="runtime prohibitions"):
        _scope(prohibited_runtime_actions=["external execution"])


def test_preview_candidate_and_decision_are_non_executing() -> None:
    candidate = _candidate()
    decision = _decision()

    assert candidate.requested_execution is False
    assert candidate.ready_for_execution is False
    assert candidate.executes_preview is False
    assert decision.approved_for_v0309_consolidation is True
    assert decision.approved_for_limited_preview_execution is False
    assert decision.approved_for_execution is False
    assert decision.executes is False
    assert preview_decision_preserves_execution_false(decision) is True

    with pytest.raises(ValueError, match="preview_candidate_id"):
        _candidate(preview_candidate_id="")
    with pytest.raises(ValueError, match="preview_scope.target_id"):
        _candidate(preview_scope=_scope(target_id="target:other"))
    with pytest.raises(ValueError, match="requested_execution"):
        _candidate(requested_execution=True)
    with pytest.raises(ValueError, match="ready_for_execution"):
        _candidate(ready_for_execution=True)
    with pytest.raises(ValueError, match="approved_for_limited_preview_execution"):
        _decision(approved_for_limited_preview_execution=True)
    with pytest.raises(ValueError, match="approved_for_execution"):
        _decision(approved_for_execution=True)
    with pytest.raises(ValueError, match="pass_with_limitations"):
        _decision(
            decision=LimitedExternalDominionPreviewDecisionType.PASS_WITH_LIMITATIONS_FOR_V0309_CONSOLIDATION,
            status=LimitedExternalDominionPreviewGateStatus.PASSED_WITH_LIMITATIONS_FOR_CONSOLIDATION,
            limitations=[],
        )
    with pytest.raises(ValueError, match="deny_defer_reasons"):
        _decision(
            decision=LimitedExternalDominionPreviewDecisionType.DENY,
            status=LimitedExternalDominionPreviewGateStatus.DENIED,
            approved_for_v0309_consolidation=False,
            deny_defer_reasons=[],
        )


def test_preview_audit_noop_report_and_handoff_boundaries() -> None:
    candidate = _candidate()
    decision = _decision()
    audit = build_preview_audit_ocel_plan(candidate)
    no_op = build_preview_no_op_plan(
        candidate,
        "No preview gate action required.",
        [LimitedExternalDominionPreviewDenyDeferReason.INSUFFICIENT_CERTIFICATION],
    )
    report = build_preview_gate_report(_eligibility(), decision)
    handoff = build_v0309_consolidation_handoff(report, decision)

    assert audit.require_append_only is True
    assert audit.require_no_raw_payload_logging is True
    assert audit.require_no_secret_logging is True
    assert audit.require_result_boundary_refs is True
    assert audit.ocel_visibility_required is True
    assert audit.emits_events is False
    assert no_op.is_failure is False
    assert no_op.executes is False
    assert report.approved_for_v0309_consolidation is True
    assert report.approved_for_limited_preview_execution is False
    assert report.approved_for_execution is False
    assert report.executes_preview is False
    assert handoff.ready_for_v0309_consolidation is True
    assert handoff.ready_for_limited_preview_execution is False
    assert handoff.ready_for_execution is False
    assert handoff.approved_for_limited_preview_execution is False
    assert handoff.approved_for_execution is False
    assert handoff.executes is False
    assert preview_gate_allows_consolidation_only(handoff) is True

    with pytest.raises(ValueError, match="require_append_only"):
        LimitedExternalDominionPreviewAuditOCELPlan(
            "audit:bad",
            "target:external",
            None,
            None,
            [],
            [],
            [],
            [],
            require_append_only=False,
        )
    with pytest.raises(ValueError, match="approved_for_limited_preview_execution"):
        LimitedExternalDominionPreviewGateReport(
            "report:bad",
            "target:external",
            "candidate:1",
            "preview_eligibility:1",
            None,
            "summary",
            LimitedExternalDominionPreviewGateStatus.GATE_PASSED_FOR_CONSOLIDATION,
            LimitedExternalDominionPreviewDecisionType.PASS_FOR_V0309_CONSOLIDATION,
            True,
            True,
            False,
        )
    with pytest.raises(ValueError, match="ready_for_limited_preview_execution"):
        ExternalDominionV0309ConsolidationHandoff(
            "handoff:bad",
            "target:external",
            "candidate:1",
            "report:1",
            "decision:1",
            True,
            True,
            False,
            True,
            False,
            False,
        )


def test_helpers_consume_v0307_handoff_without_execution_readiness() -> None:
    handoff = _handoff()
    matrix = build_preview_eligibility_matrix_from_certification_handoff(handoff)
    scope = build_preview_scope_from_eligibility(matrix)
    candidate = build_limited_preview_candidate(matrix, scope, handoff)
    decision = make_limited_preview_decision(candidate)
    report = build_preview_gate_report(matrix, decision)
    consolidation = build_v0309_consolidation_handoff(report, decision)

    assert matrix.ready_for_gate_review is True
    assert matrix.ready_for_v0309_consolidation is True
    assert scope.allows_execution is False
    assert candidate.ready_for_execution is False
    assert decision.approved_for_v0309_consolidation is True
    assert decision.approved_for_limited_preview_execution is False
    assert report.approved_for_execution is False
    assert consolidation.ready_for_v0309_consolidation is True
    assert consolidation.ready_for_limited_preview_execution is False
    assert consolidation.ready_for_execution is False


def test_unresolved_or_missing_certification_conditions_defer_preview_gate() -> None:
    handoff = _handoff(unresolved_requirements=["missing result boundary"], limitations=["limited evidence"])
    matrix = build_preview_eligibility_matrix_from_certification_handoff(handoff)
    scope = build_preview_scope_from_eligibility(matrix)
    candidate = build_limited_preview_candidate(matrix, scope, handoff)
    decision = make_limited_preview_decision(candidate)

    assert matrix.ready_for_gate_review is False
    assert matrix.ready_for_v0309_consolidation is False
    assert LimitedExternalDominionPreviewDenyDeferReason.UNRESOLVED_BLOCKING_CASE in matrix.deny_defer_reasons
    assert decision.approved_for_v0309_consolidation is False
    assert decision.approved_for_limited_preview_execution is False
    assert decision.approved_for_execution is False

    missing_gate = _handoff(ready_for_v0308_limited_preview_gate_review=False)
    missing_matrix = build_preview_eligibility_matrix_from_certification_handoff(missing_gate)
    assert LimitedExternalDominionPreviewDenyDeferReason.INSUFFICIENT_CERTIFICATION in missing_matrix.deny_defer_reasons
