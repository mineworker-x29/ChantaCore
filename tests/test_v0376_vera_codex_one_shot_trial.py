from __future__ import annotations

from dataclasses import fields
import inspect

import pytest

import chanta_core.agent_runtime.vera_codex_trial as trial_module
from chanta_core.agent_runtime import (
    SandboxDoNothingSignalKind,
    SandboxEvidenceStrength,
    SandboxFeedbackConfidenceLevel,
    SandboxRepairSuggestionKind,
    SandboxRootCauseHypothesisKind,
    SandboxSuggestedNextActionKind,
    SandboxTestOutcomeKind,
    VeraCodexEvidenceUseKind,
    VeraCodexHandoffKind,
    VeraCodexOperatorRoleKind,
    VeraCodexSafetyCheckKind,
    VeraCodexStopReasonKind,
    VeraCodexTaskHandlingOutcomeKind,
    VeraCodexTrialConfidenceLevel,
    VeraCodexTrialDecisionKind,
    VeraCodexTrialMode,
    VeraCodexTrialReadinessLevel,
    VeraCodexTrialRiskKind,
    VeraCodexTrialSourceKind,
    VeraCodexTrialStatus,
    build_sandbox_do_nothing_alternative_signal,
    build_sandbox_evidence_assessment,
    build_sandbox_failure_diagnosis_report,
    build_sandbox_root_cause_hypothesis,
    build_sandbox_suggested_next_action,
    build_sandbox_test_feedback_report,
    build_sandbox_test_outcome_classification,
    build_sandbox_test_result_envelope,
    build_v0376_readiness_report,
    build_vera_codex_decision_trace,
    build_vera_codex_decision_trace_step,
    build_vera_codex_do_nothing_assessment,
    build_vera_codex_evidence_bundle,
    build_vera_codex_evidence_bundle_from_v037_artifacts,
    build_vera_codex_evidence_item,
    build_vera_codex_handoff_memo,
    build_vera_codex_no_autonomy_guarantee,
    build_vera_codex_one_shot_trial_packet,
    build_vera_codex_operation_constraint_set,
    build_vera_codex_operator_profile,
    build_vera_codex_repair_suggestion_assessment,
    build_vera_codex_stop_reason,
    build_vera_codex_task_handling_assessment,
    build_vera_codex_trial_decision,
    build_vera_codex_trial_flags,
    build_vera_codex_trial_input,
    build_vera_codex_trial_policy,
    build_vera_codex_trial_run_preview,
    build_vera_codex_trial_task,
    create_sandbox_repair_suggestion_envelope_from_feedback,
    default_vera_codex_trial_policy,
    run_vera_codex_one_shot_trial,
    v0376_readiness_report_is_not_execution_ready,
    validate_vera_codex_one_shot_trial_packet,
    vera_codex_decision_trace_has_no_cot,
    vera_codex_trial_flags_preserve_no_autonomy,
    vera_codex_trial_packet_is_not_production_certification,
    vera_codex_trial_packet_is_single_shot,
    vera_codex_trial_policy_blocks_runtime_execution,
)


SAFE_FLAG_NAMES = (
    "ready_for_v0377_cold_agent_performance_evaluation",
    "ready_for_v0378_cli_test_runner_agent_evaluation_surface",
    "ready_for_vera_codex_one_shot_agent_trial",
    "ready_for_vera_codex_trial_packet",
    "ready_for_vera_codex_evidence_bundle",
    "ready_for_vera_codex_decision_trace",
    "ready_for_vera_codex_task_handling_report",
    "ready_for_vera_codex_handoff_memo",
    "ready_for_future_cold_evaluation_input",
)

UNSAFE_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_model_provider_invocation",
    "ready_for_tool_execution",
    "ready_for_test_execution",
    "ready_for_controlled_test_subprocess",
    "ready_for_shell_execution",
    "ready_for_dependency_install",
    "ready_for_network_access",
    "ready_for_repair_patch_proposal",
    "ready_for_automatic_repair",
    "ready_for_repair_execution",
    "ready_for_cold_agent_performance_evaluation",
    "ready_for_external_agent_execution",
    "ready_for_dominion_runtime",
)

UNSAFE_POLICY_NAMES = (
    "allow_model_provider_invocation",
    "allow_tool_execution",
    "allow_test_execution",
    "allow_subprocess",
    "allow_shell",
    "allow_dependency_install",
    "allow_network_access",
    "allow_repair_patch_proposal",
    "allow_repair_execution",
    "allow_automatic_repair",
    "allow_retry_loop",
    "allow_multi_cycle_loop",
    "allow_external_agent_execution",
    "allow_dominion_runtime",
)


def _values(enum_cls):
    return [item.value for item in enum_cls]


def _feedback_report(*, inconclusive=False, action_kind=SandboxSuggestedNextActionKind.CREATE_REPAIR_SUGGESTION_FUTURE_GATE):
    assessment = build_sandbox_evidence_assessment(
        evidence_strength=SandboxEvidenceStrength.STRONG if not inconclusive else SandboxEvidenceStrength.INSUFFICIENT,
        confidence=SandboxFeedbackConfidenceLevel.HIGH if not inconclusive else SandboxFeedbackConfidenceLevel.INCONCLUSIVE,
        supporting_evidence_refs=["evidence:1"] if not inconclusive else [],
        insufficient_evidence=inconclusive,
    )
    hypothesis = build_sandbox_root_cause_hypothesis(
        hypothesis_kind=SandboxRootCauseHypothesisKind.IMPLEMENTATION_BUG_LIKELY if not inconclusive else SandboxRootCauseHypothesisKind.INCONCLUSIVE,
        evidence_assessment=assessment,
        evidence_strength=assessment.evidence_strength,
        confidence=assessment.confidence,
    )
    diagnosis = build_sandbox_failure_diagnosis_report(
        hypotheses=[hypothesis],
        evidence_assessments=[assessment],
        inconclusive=inconclusive,
    )
    action = build_sandbox_suggested_next_action(action_kind=action_kind)
    do_nothing = build_sandbox_do_nothing_alternative_signal(
        signal_kind=SandboxDoNothingSignalKind.DO_NOTHING_COMPETITIVE if not inconclusive else SandboxDoNothingSignalKind.DO_NOTHING_REQUIRED_DUE_TO_INSUFFICIENT_EVIDENCE
    )
    return build_sandbox_test_feedback_report(
        diagnosis_report=diagnosis,
        suggested_actions=[action],
        do_nothing_signal=do_nothing,
    )


def _repair_suggestion(*, inconclusive=False):
    return create_sandbox_repair_suggestion_envelope_from_feedback(_feedback_report(inconclusive=inconclusive))


def _result_envelope(outcome_kind):
    outcome = build_sandbox_test_outcome_classification(
        outcome_kind=outcome_kind,
        passed=outcome_kind == SandboxTestOutcomeKind.PASSED,
        failed=outcome_kind not in (SandboxTestOutcomeKind.PASSED, SandboxTestOutcomeKind.INCONCLUSIVE, SandboxTestOutcomeKind.UNKNOWN),
        inconclusive=outcome_kind in (SandboxTestOutcomeKind.INCONCLUSIVE, SandboxTestOutcomeKind.UNKNOWN),
    )
    return build_sandbox_test_result_envelope(outcome_classification=outcome)


def test_v0376_enum_values_are_complete():
    assert _values(VeraCodexTrialMode) == [
        "one_shot_operator_evaluation",
        "evidence_only_trial",
        "repair_suggestion_review_trial",
        "do_nothing_comparison_trial",
        "human_handoff_trial",
        "blocked",
        "no_op",
        "unknown",
    ]
    assert "v0375_repair_suggestion_envelope" in _values(VeraCodexTrialSourceKind)
    assert "one_shot_trial_completed_with_warnings" in _values(VeraCodexTrialStatus)
    assert "decision_trace_ready" in _values(VeraCodexTrialReadinessLevel)
    assert "choose_future_repair_proposal_gate" in _values(VeraCodexTrialDecisionKind)
    assert "chain_of_thought_leak_risk" in _values(VeraCodexTrialRiskKind)
    assert "bounded_operator" in _values(VeraCodexOperatorRoleKind)
    assert "uses_do_nothing_signal" in _values(VeraCodexEvidenceUseKind)
    assert "evidence_supports_continue_to_cold_evaluation" in _values(VeraCodexTaskHandlingOutcomeKind)
    assert "stopped_for_human_handoff" in _values(VeraCodexStopReasonKind)
    assert "cold_evaluation_handoff" in _values(VeraCodexHandoffKind)
    assert "no_chain_of_thought_output_check" in _values(VeraCodexSafetyCheckKind)
    assert _values(VeraCodexTrialConfidenceLevel) == ["high", "medium", "low", "inconclusive", "unknown"]


def test_flags_policy_profile_and_input_preserve_no_autonomy():
    flags = build_vera_codex_trial_flags()
    for name in SAFE_FLAG_NAMES:
        assert getattr(flags, name) is True
    assert vera_codex_trial_flags_preserve_no_autonomy(flags)
    for name in UNSAFE_FLAG_NAMES:
        assert getattr(flags, name) is False
        with pytest.raises(ValueError):
            build_vera_codex_trial_flags(**{name: True})

    policy = default_vera_codex_trial_policy()
    assert policy.max_trial_count == 1
    assert policy.max_cycle_count == 1
    assert policy.allow_one_shot_trial is True
    assert policy.allow_future_cold_evaluation_input is True
    assert vera_codex_trial_policy_blocks_runtime_execution(policy)
    with pytest.raises(ValueError):
        build_vera_codex_trial_policy(max_trial_count=2)
    with pytest.raises(ValueError):
        build_vera_codex_trial_policy(max_cycle_count=2)
    for name in UNSAFE_POLICY_NAMES:
        assert getattr(policy, name) is False
        with pytest.raises(ValueError):
            build_vera_codex_trial_policy(**{name: True})

    profile = build_vera_codex_operator_profile()
    assert profile.bounded_operator is True
    assert profile.evidence_evaluator is True
    assert profile.autonomous_agent is False
    assert profile.external_agent is False
    assert profile.dominion_operator is False
    with pytest.raises(ValueError):
        build_vera_codex_operator_profile(autonomous_agent=True)
    with pytest.raises(ValueError):
        build_vera_codex_operator_profile(role_kind=VeraCodexOperatorRoleKind.AUTONOMOUS_AGENT)

    trial_input = build_vera_codex_trial_input()
    for action in ("model invocation", "tool execution", "test execution", "subprocess", "shell", "install", "network", "repair", "external agent", "Dominion", "retry loop", "multi-cycle loop"):
        assert action in trial_input.prohibited_runtime_actions
    with pytest.raises(ValueError):
        build_vera_codex_trial_input(prohibited_runtime_actions=["model invocation"])


def test_evidence_task_constraints_trace_and_no_cot_boundaries():
    missing = build_vera_codex_evidence_item(
        evidence_item_id="missing:evidence",
        evidence_use_kind=VeraCodexEvidenceUseKind.MISSING_REQUIRED_EVIDENCE,
        evidence_summary="missing required evidence",
        evidence_strength="insufficient",
        required=True,
        present=False,
        confidence=VeraCodexTrialConfidenceLevel.INCONCLUSIVE,
    )
    bundle = build_vera_codex_evidence_bundle(
        evidence_items=[missing],
        required_evidence_present=False,
        sufficient_for_one_shot_trial=False,
        sufficient_for_cold_evaluation_input=False,
    )
    assert bundle.required_evidence_present is False
    with pytest.raises(ValueError):
        build_vera_codex_evidence_bundle(evidence_items=[missing], required_evidence_present=True)

    task = build_vera_codex_trial_task()
    assert task.do_nothing_required is True
    assert task.human_handoff_required is True
    with pytest.raises(ValueError):
        build_vera_codex_trial_task(do_nothing_required=False)

    constraints = build_vera_codex_operation_constraint_set()
    assert constraints.max_trial_count == 1
    assert constraints.max_cycle_count == 1
    for field in fields(constraints):
        if field.name.endswith("_allowed"):
            assert getattr(constraints, field.name) is False
    with pytest.raises(ValueError):
        build_vera_codex_operation_constraint_set(tool_execution_allowed=True)

    step = build_vera_codex_decision_trace_step()
    assert step.contains_chain_of_thought is False
    assert step.executed_action is False
    with pytest.raises(ValueError):
        build_vera_codex_decision_trace_step(contains_chain_of_thought=True)
    trace = build_vera_codex_decision_trace(trace_steps=[step])
    assert vera_codex_decision_trace_has_no_cot(trace)
    with pytest.raises(ValueError):
        build_vera_codex_decision_trace(contains_chain_of_thought=True)


def test_assessments_decision_stop_handoff_and_packet_boundaries():
    do_nothing = build_vera_codex_do_nothing_assessment()
    assert do_nothing.do_nothing_valid is True
    repair_assessment = build_vera_codex_repair_suggestion_assessment(supports_future_repair_proposal=True)
    assert repair_assessment.supports_repair_now is False
    with pytest.raises(ValueError):
        build_vera_codex_repair_suggestion_assessment(supports_repair_now=True)
    handling = build_vera_codex_task_handling_assessment(
        do_nothing_assessment=do_nothing,
        repair_suggestion_assessment=repair_assessment,
    )
    assert handling.production_certified is False
    decision = build_vera_codex_trial_decision()
    for name in ("executes_now", "repair_allowed", "retry_allowed", "model_invocation_allowed", "tool_execution_allowed", "external_agent_allowed"):
        assert getattr(decision, name) is False
        with pytest.raises(ValueError):
            build_vera_codex_trial_decision(**{name: True})
    stop = build_vera_codex_stop_reason()
    assert stop.human_handoff_required is True
    assert stop.allows_continuation is False
    assert stop.allows_retry is False
    assert stop.allows_repair is False
    with pytest.raises(ValueError):
        build_vera_codex_stop_reason(allows_retry=True)
    handoff = build_vera_codex_handoff_memo()
    assert handoff.executes_action is False
    with pytest.raises(ValueError):
        build_vera_codex_handoff_memo(executes_action=True)
    packet = build_vera_codex_one_shot_trial_packet(
        task_handling_assessment=handling,
        trial_decision=decision,
        stop_reason=stop,
        handoff_memo=handoff,
    )
    assert vera_codex_trial_packet_is_single_shot(packet)
    assert vera_codex_trial_packet_is_not_production_certification(packet)
    for name in ("test_execution_performed", "model_invocation_performed", "tool_execution_performed", "repair_performed", "production_certified", "ready_for_execution"):
        assert getattr(packet, name) is False
        with pytest.raises(ValueError):
            build_vera_codex_one_shot_trial_packet(**{name: True})
    with pytest.raises(ValueError):
        build_vera_codex_one_shot_trial_packet(trial_count=2)


def test_one_shot_trial_can_create_future_cold_input_from_sufficient_supplied_metadata():
    repair = _repair_suggestion()
    result = _result_envelope(SandboxTestOutcomeKind.PASSED)
    packet = run_vera_codex_one_shot_trial(repair_suggestion=repair, feedback_report=_feedback_report(), result_envelope=result)
    assert packet.trial_count == 1
    assert packet.max_cycle_count == 1
    assert packet.automatic_retry_allowed is False
    assert packet.automatic_repair_allowed is False
    assert packet.human_handoff_required is True
    assert packet.stop_reason.human_handoff_required is True
    assert packet.decision_trace.contains_chain_of_thought is False
    assert packet.handoff_memo.executes_action is False
    assert packet.eligible_for_future_cold_evaluation in (True, False)
    assert packet.model_invocation_performed is False
    assert packet.tool_execution_performed is False
    assert packet.repair_performed is False
    assert packet.production_certified is False
    assert validate_vera_codex_one_shot_trial_packet(packet).valid is True


def test_insufficient_failed_and_inconclusive_evidence_preserve_do_nothing_and_no_success():
    weak_repair = _repair_suggestion(inconclusive=True)
    inconclusive_result = _result_envelope(SandboxTestOutcomeKind.INCONCLUSIVE)
    packet = run_vera_codex_one_shot_trial(repair_suggestion=weak_repair, feedback_report=_feedback_report(inconclusive=True), result_envelope=inconclusive_result)
    assert packet.safety_report.requires_review is True
    assert packet.task_handling_assessment.outcome_kind in (
        VeraCodexTaskHandlingOutcomeKind.EVIDENCE_INSUFFICIENT,
        VeraCodexTaskHandlingOutcomeKind.EVIDENCE_SUPPORTS_HUMAN_REVIEW,
    )
    assert packet.task_handling_assessment.passed_as_success is False
    assert packet.task_handling_assessment.do_nothing_assessment.do_nothing_valid is True
    assert packet.trial_decision.executes_now is False
    assert packet.stop_reason.allows_retry is False
    assert packet.stop_reason.allows_repair is False

    failed_result = _result_envelope(SandboxTestOutcomeKind.FAILED_ASSERTION)
    failed_packet = run_vera_codex_one_shot_trial(repair_suggestion=_repair_suggestion(), feedback_report=_feedback_report(), result_envelope=failed_result)
    assert failed_packet.task_handling_assessment.passed_as_success is False
    assert failed_packet.trial_decision.decision_kind == VeraCodexTrialDecisionKind.CHOOSE_HUMAN_REVIEW


def test_reports_guarantee_readiness_and_run_preview_preserve_boundaries():
    guarantee = build_vera_codex_no_autonomy_guarantee()
    for field in fields(guarantee):
        if field.name.startswith("no_"):
            assert getattr(guarantee, field.name) is True
    readiness = build_v0376_readiness_report()
    assert v0376_readiness_report_is_not_execution_ready(readiness)
    preview = build_vera_codex_trial_run_preview()
    assert preview.would_call_model_provider is False
    assert preview.would_execute_tools is False
    assert preview.would_run_tests is False
    assert preview.would_repair is False
    assert preview.would_use_external_agent is False


def test_helper_source_has_no_runtime_invocation_or_patch_generation_patterns():
    source = inspect.getsource(trial_module)
    forbidden = [
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "Path.write_text",
        "Path.write_bytes",
        "open(",
        "import requests",
        "import httpx",
        "import urllib",
        "import aiohttp",
        "import socket",
        "eval(",
        "exec(",
        "apply_patch(",
        "git apply",
    ]
    for pattern in forbidden:
        assert pattern not in source
