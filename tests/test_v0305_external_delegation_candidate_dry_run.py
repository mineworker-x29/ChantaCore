from __future__ import annotations

import pytest

from chanta_core.external_dominion import (
    DominionAuthorityDecision,
    DominionAuthorityDecisionType,
    DominionAuthorityRequest,
    DominionAuthorityRequestStatus,
    DominionAuthorityScope,
    DominionAuthorityScopeKind,
    DominionLevel,
    ExternalBoundarySurface,
    ExternalDelegationCandidate,
    ExternalDelegationCandidateStatus,
    ExternalDelegationDryRunPlan,
    ExternalDelegationDryRunReport,
    ExternalDelegationDryRunStep,
    ExternalDelegationEffectPreview,
    ExternalDelegationExpectedOutputSchema,
    ExternalDelegationHandoffPreview,
    ExternalDelegationInputEnvelope,
    ExternalDelegationIntent,
    ExternalDelegationIntentKind,
    ExternalDelegationNoOpPlan,
    ExternalDelegationRiskPreview,
    ExternalEffectSurface,
    build_delegation_input_envelope,
    build_expected_output_schema,
    build_external_delegation_dry_run_plan,
    build_external_delegation_dry_run_report,
    build_external_delegation_handoff_preview,
    build_external_delegation_no_op_plan,
    delegation_candidate_preserves_v0305_boundary,
    dry_run_plan_preserves_no_execution,
    make_dominion_authority_decision,
    make_external_delegation_candidate,
    make_external_delegation_intent_from_authority_decision,
    preview_delegation_effects,
    preview_delegation_risks,
)


def _authority_scope(**overrides) -> DominionAuthorityScope:
    data = {
        "scope_id": "dominion_authority_scope:target:external",
        "scope_kind": DominionAuthorityScopeKind.TARGET_SCOPE,
        "target_id": "target:external",
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
        "max_level": DominionLevel.D3_SIMULATE,
        "evidence_refs": ["evidence:authority"],
    }
    data.update(overrides)
    return DominionAuthorityScope(**data)


def _authority_decision(**overrides) -> DominionAuthorityDecision:
    scope = _authority_scope()
    data = {
        "decision_id": "dominion_authority_decision:target:external",
        "request_id": "dominion_authority_request:target:external",
        "target_id": "target:external",
        "requested_level": DominionLevel.D3_SIMULATE,
        "granted_level": DominionLevel.D3_SIMULATE,
        "decision": DominionAuthorityDecisionType.SIMULATE_ONLY,
        "granted_scope": scope,
        "reason": "Simulation-only authority decision for planning artifacts.",
        "evidence_refs": ["evidence:authority"],
        "required_reviews": [],
        "approval_required": False,
        "approval_granted": False,
        "human_review_required": False,
        "future_gate_required": False,
        "blocked_reasons": [],
        "withdrawal_conditions": ["decision is treated as runtime execution"],
        "validity_horizon": "v0.30.4",
        "metadata": {},
    }
    data.update(overrides)
    return DominionAuthorityDecision(**data)


def _intent(**overrides) -> ExternalDelegationIntent:
    data = {
        "intent_id": "external_delegation_intent:target:external",
        "target_id": "target:external",
        "intent_kind": ExternalDelegationIntentKind.SIMULATE_EXTERNAL_RESPONSE,
        "goal_summary": "Model a possible external response.",
        "reason": "Plan only.",
        "source_decision_ids": ["dominion_authority_decision:target:external"],
        "source_candidate_ids": [],
        "source_report_ids": [],
        "requested_level": DominionLevel.D3_SIMULATE,
        "evidence_refs": ["evidence:authority"],
        "metadata": {},
    }
    data.update(overrides)
    return ExternalDelegationIntent(**data)


def _envelope(**overrides) -> ExternalDelegationInputEnvelope:
    data = {
        "envelope_id": "external_delegation_input_envelope:external_delegation_candidate:1",
        "candidate_id": "external_delegation_candidate:1",
        "target_id": "target:external",
        "context_summary": "Local planning envelope.",
        "structured_inputs": {"goal": "model only"},
        "allowed_capability_refs": [],
        "prohibited_capabilities": ["network access", "credential access", "provider invocation"],
        "object_refs": [],
        "evidence_refs": ["evidence:authority"],
        "data_boundary_notes": ["redact private data"],
        "redaction_required": True,
        "metadata": {},
    }
    data.update(overrides)
    return ExternalDelegationInputEnvelope(**data)


def _schema(**overrides) -> ExternalDelegationExpectedOutputSchema:
    data = {
        "schema_id": "external_delegation_expected_output_schema:external_delegation_candidate:1",
        "candidate_id": "external_delegation_candidate:1",
        "target_id": "target:external",
        "required_fields": ["summary", "evidence_refs"],
    }
    data.update(overrides)
    return ExternalDelegationExpectedOutputSchema(**data)


def _effect(**overrides) -> ExternalDelegationEffectPreview:
    data = {
        "preview_id": "external_delegation_effect_preview:external_delegation_candidate:1",
        "candidate_id": "external_delegation_candidate:1",
        "target_id": "target:external",
        "side_effect_free_expected": True,
    }
    data.update(overrides)
    return ExternalDelegationEffectPreview(**data)


def _risk(**overrides) -> ExternalDelegationRiskPreview:
    data = {
        "risk_preview_id": "external_delegation_risk_preview:external_delegation_candidate:1",
        "candidate_id": "external_delegation_candidate:1",
        "target_id": "target:external",
        "risk_signals": [],
        "blocked_reasons": [],
        "required_reviews": [],
        "future_gate_required": False,
        "human_approval_required": False,
        "no_op_recommended": False,
        "rationale": "Low-risk planning artifact.",
        "evidence_refs": ["evidence:authority"],
    }
    data.update(overrides)
    return ExternalDelegationRiskPreview(**data)


def _candidate(**overrides) -> ExternalDelegationCandidate:
    data = {
        "candidate_id": "external_delegation_candidate:1",
        "target_id": "target:external",
        "intent": _intent(),
        "input_envelope": _envelope(),
        "expected_output_schema": _schema(),
        "effect_preview": _effect(),
        "risk_preview": _risk(),
        "status": ExternalDelegationCandidateStatus.CANDIDATE,
        "requested_level": DominionLevel.D3_SIMULATE,
        "max_allowed_level": DominionLevel.D3_SIMULATE,
        "evidence_refs": ["evidence:authority"],
        "withdrawal_conditions": ["candidate is treated as runtime delegation"],
        "metadata": {},
    }
    data.update(overrides)
    return ExternalDelegationCandidate(**data)


def test_valid_external_delegation_intent_creation_is_non_runtime() -> None:
    intent = _intent()

    assert intent.creates_delegation_runtime is False
    assert intent.triggers_execution is False
    assert intent.grants_authority is False
    assert intent.requested_level == DominionLevel.D3_SIMULATE

    with pytest.raises(ValueError, match="intent_id"):
        _intent(intent_id="")
    with pytest.raises(ValueError, match="target_id"):
        _intent(target_id="")
    with pytest.raises(ValueError, match="goal_summary"):
        _intent(goal_summary=" ")
    with pytest.raises(ValueError, match="reason"):
        _intent(reason="")
    with pytest.raises(TypeError, match="source_decision_ids"):
        _intent(source_decision_ids="not-list")


def test_input_envelope_creation_and_redaction_boundary() -> None:
    envelope = _envelope()

    assert envelope.packet_sent is False
    assert envelope.submitted_to_external_runtime is False
    assert envelope.redaction_required is True

    with pytest.raises(ValueError, match="envelope_id"):
        _envelope(envelope_id="")
    with pytest.raises(ValueError, match="candidate_id"):
        _envelope(candidate_id="")
    with pytest.raises(ValueError, match="target_id"):
        _envelope(target_id="")
    with pytest.raises(ValueError, match="context_summary"):
        _envelope(context_summary=" ")
    with pytest.raises(TypeError, match="structured_inputs"):
        _envelope(structured_inputs=[])
    with pytest.raises(TypeError, match="allowed_capability_refs"):
        _envelope(allowed_capability_refs="not-list")
    with pytest.raises(TypeError, match="prohibited_capabilities"):
        _envelope(prohibited_capabilities="not-list")
    with pytest.raises(ValueError, match="redaction_required"):
        _envelope(redaction_required=False)


def test_expected_output_schema_defaults_and_validation() -> None:
    schema = ExternalDelegationExpectedOutputSchema(
        "schema:1",
        "candidate:1",
        "target:external",
        ["summary"],
    )

    assert schema.raw_output_allowed is False
    assert schema.result_envelope_required is True
    assert schema.evidence_required is True
    assert schema.is_external_output is False

    with pytest.raises(ValueError, match="schema_id"):
        _schema(schema_id="")
    with pytest.raises(ValueError, match="candidate_id"):
        _schema(candidate_id="")
    with pytest.raises(ValueError, match="target_id"):
        _schema(target_id="")
    with pytest.raises(TypeError, match="required_fields"):
        _schema(required_fields="not-list")
    with pytest.raises(TypeError, match="forbidden_fields"):
        _schema(forbidden_fields="not-list")
    with pytest.raises(ValueError, match="raw_output_allowed"):
        _schema(raw_output_allowed=True)
    with pytest.raises(ValueError, match="result_envelope_required"):
        _schema(result_envelope_required=False)
    with pytest.raises(ValueError, match="evidence_required"):
        _schema(evidence_required=False)


def test_effect_preview_and_risk_preview_validation() -> None:
    effect = _effect()
    assert effect.descriptive_only is True
    assert effect.any_dangerous_effect_possible is False

    with pytest.raises(ValueError, match="side_effect_free_expected"):
        _effect(network_effect_possible=True, side_effect_free_expected=True)
    dangerous_effect = _effect(network_effect_possible=True, side_effect_free_expected=False)
    assert dangerous_effect.any_dangerous_effect_possible is True

    risk = _risk()
    assert risk.approval_granted is False
    assert risk.executes is False
    assert risk.blocks_by_itself is False

    with pytest.raises(ValueError, match="risk_preview_id"):
        _risk(risk_preview_id="")
    with pytest.raises(ValueError, match="candidate_id"):
        _risk(candidate_id="")
    with pytest.raises(ValueError, match="target_id"):
        _risk(target_id="")
    with pytest.raises(ValueError, match="high-risk"):
        _risk(risk_signals=["network risk"], future_gate_required=False, human_approval_required=False)
    high_risk = _risk(risk_signals=["network risk"], future_gate_required=True)
    assert high_risk.approval_granted is False


def test_external_delegation_candidate_validation_and_boundaries() -> None:
    candidate = _candidate()

    assert candidate.grants_delegation_authority is False
    assert candidate.creates_runtime is False
    assert candidate.executes is False
    assert delegation_candidate_preserves_v0305_boundary(candidate) is True

    with pytest.raises(ValueError, match="candidate_id"):
        _candidate(candidate_id="")
    with pytest.raises(ValueError, match="target_id"):
        _candidate(target_id="")
    with pytest.raises(ValueError, match="intent target_id"):
        _candidate(intent=_intent(target_id="target:other"))
    with pytest.raises(ValueError, match="nested target_id"):
        _candidate(input_envelope=_envelope(target_id="target:other"))
    with pytest.raises(ValueError, match="nested candidate_id"):
        _candidate(expected_output_schema=_schema(candidate_id="candidate:other"))
    with pytest.raises(ValueError, match="D3_SIMULATE"):
        _candidate(requested_level=DominionLevel.D8_DELEGATE_AGENT, max_allowed_level=DominionLevel.D8_DELEGATE_AGENT)


def test_dry_run_step_plan_report_noop_and_handoff_validation() -> None:
    step = ExternalDelegationDryRunStep(
        "step:1",
        "external_delegation_candidate:1",
        0,
        "Validate envelope locally.",
        "simulate local envelope validation",
        "envelope checklist",
    )
    assert step.simulation_plan_only is True

    with pytest.raises(ValueError, match="step_id"):
        ExternalDelegationDryRunStep("", "candidate:1", 0, "desc", "simulate local review", "artifact")
    with pytest.raises(ValueError, match="candidate_id"):
        ExternalDelegationDryRunStep("step:bad", "", 0, "desc", "simulate local review", "artifact")
    with pytest.raises(ValueError, match="order"):
        ExternalDelegationDryRunStep("step:bad", "candidate:1", -1, "desc", "simulate local review", "artifact")
    with pytest.raises(ValueError, match="description"):
        ExternalDelegationDryRunStep("step:bad", "candidate:1", 0, "", "simulate local review", "artifact")
    with pytest.raises(ValueError, match="actual execution"):
        ExternalDelegationDryRunStep("step:bad", "candidate:1", 0, "desc", "execute external tool", "artifact")
    with pytest.raises(ValueError, match="uses_"):
        ExternalDelegationDryRunStep(
            "step:bad",
            "candidate:1",
            0,
            "desc",
            "simulate local review",
            "artifact",
            uses_external_runtime=True,
        )

    plan = ExternalDelegationDryRunPlan(
        "plan:1",
        "external_delegation_candidate:1",
        "target:external",
        [step],
        ["envelope checklist"],
        ["external contact"],
        True,
        True,
        True,
        True,
        True,
        evidence_refs=["evidence:authority"],
    )
    assert plan.executes is False
    assert dry_run_plan_preserves_no_execution(plan) is True

    for field_name in [
        "no_execution_guarantee",
        "no_external_contact_guarantee",
        "no_credential_use_guarantee",
        "no_network_use_guarantee",
        "no_command_use_guarantee",
    ]:
        kwargs = {
            "plan_id": "plan:bad",
            "candidate_id": "external_delegation_candidate:1",
            "target_id": "target:external",
            "steps": [step],
            "expected_artifacts": [],
            "explicitly_not_performed": [],
            "no_execution_guarantee": True,
            "no_external_contact_guarantee": True,
            "no_credential_use_guarantee": True,
            "no_network_use_guarantee": True,
            "no_command_use_guarantee": True,
        }
        kwargs[field_name] = False
        with pytest.raises(ValueError, match=field_name):
            ExternalDelegationDryRunPlan(**kwargs)

    report = ExternalDelegationDryRunReport(
        "report:1",
        "plan:1",
        "external_delegation_candidate:1",
        "target:external",
        ["step:1"],
        ["local only"],
        [],
        False,
        False,
        True,
    )
    assert report.derived_from_plan_only is True
    assert report.is_external_runtime_output is False
    assert report.approval_granted is False

    no_op = ExternalDelegationNoOpPlan(
        "noop:1",
        "external_delegation_candidate:1",
        "target:external",
        "No safe delegation path.",
    )
    assert no_op.is_failure is False
    assert no_op.executes is False

    handoff = ExternalDelegationHandoffPreview(
        "handoff:1",
        "external_delegation_candidate:1",
        "target:external",
        plan.plan_id,
        report.report_id,
        None,
        "v0.30.6 approval/audit/rollback boundary",
        True,
        False,
    )
    assert handoff.executes_handoff is False
    with pytest.raises(ValueError, match="ready_for_execution"):
        ExternalDelegationHandoffPreview("handoff:bad", "candidate:1", "target:external", None, None, None, "v0.30.6 approval/audit/rollback boundary", True, True)


def test_helpers_build_candidate_plan_report_and_handoff_without_execution() -> None:
    authority_decision = _authority_decision()
    intent = make_external_delegation_intent_from_authority_decision(authority_decision)
    assert intent is not None

    candidate = make_external_delegation_candidate(intent, authority_decision)
    plan = build_external_delegation_dry_run_plan(candidate)
    report = build_external_delegation_dry_run_report(plan)
    handoff = build_external_delegation_handoff_preview(candidate, plan, report)

    assert candidate.status == ExternalDelegationCandidateStatus.CANDIDATE
    assert delegation_candidate_preserves_v0305_boundary(candidate) is True
    assert dry_run_plan_preserves_no_execution(plan) is True
    assert report.is_external_runtime_output is False
    assert handoff.ready_for_execution is False
    assert handoff.ready_for_v0306_approval_audit_boundary is True


def test_d8_delegation_request_remains_future_track_and_non_runtime() -> None:
    request = DominionAuthorityRequest(
        "dominion_authority_request:d8",
        "target:external",
        DominionLevel.D8_DELEGATE_AGENT,
        requested_scope=_authority_scope(max_level=DominionLevel.D3_SIMULATE),
        request_status=DominionAuthorityRequestStatus.REQUESTED,
    )
    authority_decision = make_dominion_authority_decision(request)
    intent = make_external_delegation_intent_from_authority_decision(authority_decision)
    assert intent is not None
    candidate = make_external_delegation_candidate(intent, authority_decision)
    no_op = build_external_delegation_no_op_plan(candidate, "D8 remains future-track.")
    handoff = build_external_delegation_handoff_preview(candidate, no_op_plan=no_op)

    assert authority_decision.granted_level is None
    assert candidate.requested_level == DominionLevel.D8_DELEGATE_AGENT
    assert candidate.max_allowed_level <= DominionLevel.D3_SIMULATE
    assert candidate.grants_delegation_authority is False
    assert candidate.creates_runtime is False
    assert no_op.is_failure is False
    assert handoff.next_stage == "future_track"
    assert handoff.ready_for_execution is False


def test_denied_or_blocked_authority_decision_produces_noop_or_no_intent() -> None:
    denied = _authority_decision(
        decision=DominionAuthorityDecisionType.DENY,
        granted_level=None,
        granted_scope=None,
    )
    assert make_external_delegation_intent_from_authority_decision(denied) is None

    blocked = _authority_decision(
        decision=DominionAuthorityDecisionType.BLOCKED,
        granted_level=None,
        granted_scope=None,
        blocked_reasons=["blocked by authority boundary"],
    )
    intent = make_external_delegation_intent_from_authority_decision(blocked)
    assert intent is not None
    candidate = make_external_delegation_candidate(intent, blocked)
    no_op = build_external_delegation_no_op_plan(candidate, "Blocked authority decision.", blocked.blocked_reasons)
    assert candidate.status == ExternalDelegationCandidateStatus.BLOCKED
    assert no_op.is_failure is False
    assert no_op.executes is False


def test_high_risk_provider_gateway_rpa_browser_command_network_credential_stays_non_executable() -> None:
    intent = _intent(
        metadata={
            "future_gate_required": True,
            "approval_required": True,
            "risk_signals": [
                "provider risk",
                "gateway risk",
                "rpa risk",
                "browser risk",
                "command risk",
                "network risk",
                "credential risk",
            ],
        }
    )
    envelope = build_delegation_input_envelope(intent)
    schema = build_expected_output_schema(intent)
    effect = preview_delegation_effects(intent)
    risk = preview_delegation_risks(intent)

    assert envelope.packet_sent is False
    assert envelope.redaction_required is True
    assert schema.raw_output_allowed is False
    assert effect.delegation_effect_possible is True
    assert effect.side_effect_free_expected is False
    assert risk.future_gate_required is True
    assert risk.human_approval_required is True
    assert risk.approval_granted is False
