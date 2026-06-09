from __future__ import annotations

from dataclasses import fields
import inspect

import pytest

import chanta_core.agent_runtime.agent_performance_evaluation as eval_module
from chanta_core.agent_runtime import (
    ColdAgentBoundaryComplianceKind,
    ColdAgentDoNothingComparisonKind,
    ColdAgentEvaluationDecisionKind,
    ColdAgentEvaluationMode,
    ColdAgentEvaluationReadinessLevel,
    ColdAgentEvaluationRiskKind,
    ColdAgentEvaluationSourceKind,
    ColdAgentEvaluationStatus,
    ColdAgentEvidenceQualityKind,
    ColdAgentFailureConditionKind,
    ColdAgentScoreConfidenceLevel,
    ColdAgentScoreDimensionKind,
    ColdAgentScoreGrade,
    ColdAgentVerdictKind,
    SandboxDoNothingSignalKind,
    SandboxEvidenceStrength,
    SandboxFeedbackConfidenceLevel,
    SandboxRootCauseHypothesisKind,
    SandboxSuggestedNextActionKind,
    SandboxTestOutcomeKind,
    build_cold_agent_boundary_compliance_assessment,
    build_cold_agent_do_nothing_comparison,
    build_cold_agent_evidence_assessment,
    build_cold_agent_evaluation_flags,
    build_cold_agent_evaluation_input,
    build_cold_agent_evaluation_no_runtime_guarantee,
    build_cold_agent_evaluation_policy,
    build_cold_agent_evaluation_run_preview,
    build_cold_agent_failure_condition_assessment,
    build_cold_agent_performance_scorecard,
    build_cold_agent_score_dimension,
    build_cold_agent_verdict,
    build_sandbox_do_nothing_alternative_signal,
    build_sandbox_evidence_assessment,
    build_sandbox_failure_diagnosis_report,
    build_sandbox_root_cause_hypothesis,
    build_sandbox_suggested_next_action,
    build_sandbox_test_feedback_report,
    build_sandbox_test_outcome_classification,
    build_sandbox_test_result_envelope,
    build_v0377_readiness_report,
    cold_agent_evaluation_flags_preserve_no_runtime,
    cold_agent_evaluation_policy_blocks_runtime,
    cold_agent_scorecard_is_not_production_certification,
    cold_agent_verdict_is_not_execution_permission,
    create_cold_agent_evaluation_report,
    create_sandbox_repair_suggestion_envelope_from_feedback,
    default_cold_agent_evaluation_policy,
    run_vera_codex_one_shot_trial,
    v0377_readiness_report_is_not_execution_ready,
    validate_cold_agent_evaluation_report,
)


SAFE_FLAG_NAMES = (
    "ready_for_v0378_cli_test_runner_agent_evaluation_surface",
    "ready_for_v0379_controlled_sandbox_test_runner_consolidation",
    "ready_for_cold_agent_performance_evaluation",
    "ready_for_cold_agent_scorecard",
    "ready_for_evidence_grounding_assessment",
    "ready_for_boundary_compliance_assessment",
    "ready_for_do_nothing_comparison",
    "ready_for_failure_condition_assessment",
    "ready_for_future_cli_evaluation_surface_input",
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
    "allow_repair_execution",
    "allow_external_agent_execution",
    "allow_dominion_runtime",
)


def _values(enum_cls):
    return [item.value for item in enum_cls]


def _feedback_report(*, inconclusive=False):
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
    action = build_sandbox_suggested_next_action(action_kind=SandboxSuggestedNextActionKind.CREATE_REPAIR_SUGGESTION_FUTURE_GATE)
    do_nothing = build_sandbox_do_nothing_alternative_signal(
        signal_kind=SandboxDoNothingSignalKind.DO_NOTHING_COMPETITIVE if not inconclusive else SandboxDoNothingSignalKind.DO_NOTHING_REQUIRED_DUE_TO_INSUFFICIENT_EVIDENCE
    )
    return build_sandbox_test_feedback_report(
        diagnosis_report=diagnosis,
        suggested_actions=[action],
        do_nothing_signal=do_nothing,
    )


def _result_envelope(outcome_kind):
    outcome = build_sandbox_test_outcome_classification(
        outcome_kind=outcome_kind,
        passed=outcome_kind == SandboxTestOutcomeKind.PASSED,
        failed=outcome_kind not in (SandboxTestOutcomeKind.PASSED, SandboxTestOutcomeKind.INCONCLUSIVE, SandboxTestOutcomeKind.UNKNOWN),
        inconclusive=outcome_kind in (SandboxTestOutcomeKind.INCONCLUSIVE, SandboxTestOutcomeKind.UNKNOWN),
    )
    return build_sandbox_test_result_envelope(outcome_classification=outcome)


def _trial_bundle(*, outcome=SandboxTestOutcomeKind.PASSED, inconclusive=False):
    feedback = _feedback_report(inconclusive=inconclusive)
    repair = create_sandbox_repair_suggestion_envelope_from_feedback(feedback)
    result = _result_envelope(outcome)
    trial = run_vera_codex_one_shot_trial(repair_suggestion=repair, feedback_report=feedback, result_envelope=result)
    return trial, repair, feedback, result


def test_v0377_enum_values_are_complete():
    assert _values(ColdAgentEvaluationMode) == [
        "cold_scorecard",
        "evidence_grounded_evaluation",
        "do_nothing_comparison_evaluation",
        "boundary_compliance_evaluation",
        "failure_condition_evaluation",
        "future_cli_evaluation_input",
        "blocked",
        "no_op",
        "unknown",
    ]
    assert "v0376_vera_codex_one_shot_trial_packet" in _values(ColdAgentEvaluationSourceKind)
    assert "evaluation_completed_with_warnings" in _values(ColdAgentEvaluationStatus)
    assert "verdict_ready" in _values(ColdAgentEvaluationReadinessLevel)
    assert "allow_future_cli_evaluation_input" in _values(ColdAgentEvaluationDecisionKind)
    assert "score_without_evidence_risk" in _values(ColdAgentEvaluationRiskKind)
    assert "human_handoff_quality" in _values(ColdAgentScoreDimensionKind)
    assert _values(ColdAgentScoreGrade) == ["excellent", "good", "acceptable", "weak", "failed", "blocked", "inconclusive", "not_evaluable", "unknown"]
    assert _values(ColdAgentVerdictKind) == ["pass", "pass_with_warnings", "inconclusive", "fail", "blocked", "no_op", "unknown"]
    assert "model_provider_invocation_detected" in _values(ColdAgentFailureConditionKind)
    assert _values(ColdAgentEvidenceQualityKind) == ["strong", "adequate", "weak", "insufficient", "contradictory", "missing", "unknown"]
    assert "violation_detected" in _values(ColdAgentBoundaryComplianceKind)
    assert "do_nothing_required_due_to_insufficient_evidence" in _values(ColdAgentDoNothingComparisonKind)
    assert _values(ColdAgentScoreConfidenceLevel) == ["high", "medium", "low", "inconclusive", "unknown"]


def test_flags_policy_and_input_are_metadata_only():
    flags = build_cold_agent_evaluation_flags()
    for name in SAFE_FLAG_NAMES:
        assert getattr(flags, name) is True
    assert cold_agent_evaluation_flags_preserve_no_runtime(flags)
    for name in UNSAFE_FLAG_NAMES:
        assert getattr(flags, name) is False
        with pytest.raises(ValueError):
            build_cold_agent_evaluation_flags(**{name: True})

    policy = default_cold_agent_evaluation_policy()
    assert policy.require_test_result_evidence is True
    assert policy.require_vera_trial_packet is True
    assert policy.require_do_nothing_comparison is True
    assert policy.require_boundary_compliance_assessment is True
    assert policy.require_handoff_quality_assessment is True
    assert policy.reject_self_praise_without_evidence is True
    assert policy.reject_failed_test_as_success is True
    assert policy.reject_inconclusive_as_success is True
    assert policy.reject_production_certification is True
    assert cold_agent_evaluation_policy_blocks_runtime(policy)
    for name in UNSAFE_POLICY_NAMES:
        assert getattr(policy, name) is False
        with pytest.raises(ValueError):
            build_cold_agent_evaluation_policy(**{name: True})

    request = build_cold_agent_evaluation_input()
    for action in ("model invocation", "tool execution", "test execution", "subprocess", "shell", "install", "network", "repair", "external agent", "Dominion"):
        assert action in request.prohibited_runtime_actions
    with pytest.raises(ValueError):
        build_cold_agent_evaluation_input(prohibited_runtime_actions=["model invocation"])


def test_assessment_models_enforce_evidence_boundary_do_nothing_and_failure_rules():
    strong = build_cold_agent_evidence_assessment(
        evidence_quality=ColdAgentEvidenceQualityKind.STRONG,
        confidence=ColdAgentScoreConfidenceLevel.HIGH,
        supporting_evidence_refs=["trial"],
        sufficient_for_pass=True,
    )
    assert strong.sufficient_for_pass is True
    for quality in (ColdAgentEvidenceQualityKind.INSUFFICIENT, ColdAgentEvidenceQualityKind.MISSING, ColdAgentEvidenceQualityKind.CONTRADICTORY):
        with pytest.raises(ValueError):
            build_cold_agent_evidence_assessment(evidence_quality=quality, sufficient_for_pass=True)

    dimension = build_cold_agent_score_dimension(evidence_assessment=strong, score=0.8)
    assert dimension.score <= dimension.max_score
    with pytest.raises(ValueError):
        build_cold_agent_score_dimension(evidence_assessment=strong, score=2.0)
    weak = build_cold_agent_evidence_assessment(evidence_quality=ColdAgentEvidenceQualityKind.WEAK, sufficient_for_pass=True)
    with pytest.raises(ValueError):
        build_cold_agent_score_dimension(evidence_assessment=weak, score=0.9)

    boundary = build_cold_agent_boundary_compliance_assessment()
    assert boundary.pass_allowed is True
    with pytest.raises(ValueError):
        build_cold_agent_boundary_compliance_assessment(
            compliance_kind=ColdAgentBoundaryComplianceKind.VIOLATION_DETECTED,
            violated_boundaries=["tool_execution"],
            pass_allowed=True,
        )

    do_nothing = build_cold_agent_do_nothing_comparison(do_nothing_preferred=True, agent_outperforms_do_nothing=False)
    assert do_nothing.do_nothing_preferred is True
    with pytest.raises(ValueError):
        build_cold_agent_do_nothing_comparison(do_nothing_required=True, agent_outperforms_do_nothing=True)

    failure = build_cold_agent_failure_condition_assessment(
        triggered_conditions=[ColdAgentFailureConditionKind.MODEL_PROVIDER_INVOCATION_DETECTED],
        blocks_pass=True,
        forces_blocked=True,
    )
    assert failure.forces_blocked is True
    with pytest.raises(ValueError):
        build_cold_agent_failure_condition_assessment(
            triggered_conditions=[ColdAgentFailureConditionKind.MODEL_PROVIDER_INVOCATION_DETECTED],
            blocks_pass=False,
            forces_blocked=False,
        )


def test_cold_evaluation_from_sufficient_metadata_produces_non_certifying_scorecard():
    trial, repair, feedback, result = _trial_bundle()
    report = create_cold_agent_evaluation_report(trial, repair, feedback, result)
    assert report.eligible_for_future_cli_surface is True
    assert report.test_execution_performed is False
    assert report.model_invocation_performed is False
    assert report.tool_execution_performed is False
    assert report.repair_performed is False
    assert report.production_certified is False
    assert cold_agent_scorecard_is_not_production_certification(report.scorecard)
    assert cold_agent_verdict_is_not_execution_permission(report.verdict)
    assert report.scorecard.total_score <= report.scorecard.max_score
    assert report.scorecard.normalized_score <= 1.0
    assert report.scorecard.do_nothing_comparison is not None
    assert validate_cold_agent_evaluation_report(report).valid is True


def test_inconclusive_fail_and_blocked_outcomes_are_preserved():
    weak_trial, weak_repair, weak_feedback, weak_result = _trial_bundle(outcome=SandboxTestOutcomeKind.INCONCLUSIVE, inconclusive=True)
    weak_report = create_cold_agent_evaluation_report(weak_trial, weak_repair, weak_feedback, weak_result)
    assert weak_report.verdict.verdict_kind in (ColdAgentVerdictKind.INCONCLUSIVE, ColdAgentVerdictKind.FAIL, ColdAgentVerdictKind.BLOCKED)
    assert weak_report.verdict.pass_allowed is False
    assert weak_report.scorecard.do_nothing_comparison.do_nothing_preferred is True

    failed_trial, failed_repair, failed_feedback, failed_result = _trial_bundle(outcome=SandboxTestOutcomeKind.FAILED_ASSERTION)
    failed_report = create_cold_agent_evaluation_report(failed_trial, failed_repair, failed_feedback, failed_result)
    assert failed_report.verdict.verdict_kind != ColdAgentVerdictKind.PASS
    assert failed_report.verdict.pass_allowed is False

    blocked = build_cold_agent_boundary_compliance_assessment(
        compliance_kind=ColdAgentBoundaryComplianceKind.VIOLATION_DETECTED,
        violated_boundaries=["model_invocation_performed"],
        pass_allowed=False,
    )
    scorecard = failed_report.scorecard
    blocked_scorecard = build_cold_agent_performance_scorecard(
        evaluation_input_id=scorecard.evaluation_input_id,
        dimensions=scorecard.dimensions,
        boundary_assessment=blocked,
        do_nothing_comparison=scorecard.do_nothing_comparison,
        failure_assessment=build_cold_agent_failure_condition_assessment(
            triggered_conditions=[ColdAgentFailureConditionKind.MODEL_PROVIDER_INVOCATION_DETECTED],
            blocks_pass=True,
            forces_blocked=True,
        ),
        total_score=0.0,
        max_score=scorecard.max_score,
        normalized_score=0.0,
        overall_grade=ColdAgentScoreGrade.BLOCKED,
    )
    verdict = build_cold_agent_verdict(
        verdict_kind=ColdAgentVerdictKind.BLOCKED,
        scorecard_id=blocked_scorecard.scorecard_id,
        pass_allowed=False,
    )
    assert verdict.ready_for_execution is False
    assert verdict.production_certified is False


def test_no_runtime_guarantee_readiness_and_preview_preserve_boundaries():
    guarantee = build_cold_agent_evaluation_no_runtime_guarantee()
    for field in fields(guarantee):
        if field.name.startswith("no_"):
            assert getattr(guarantee, field.name) is True
    readiness = build_v0377_readiness_report()
    assert v0377_readiness_report_is_not_execution_ready(readiness)
    preview = build_cold_agent_evaluation_run_preview()
    assert preview.would_call_model_provider is False
    assert preview.would_execute_tools is False
    assert preview.would_run_tests is False
    assert preview.would_repair is False
    assert preview.would_certify_production is False


def test_helper_source_has_no_runtime_invocation_or_patch_generation_patterns():
    source = inspect.getsource(eval_module)
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
