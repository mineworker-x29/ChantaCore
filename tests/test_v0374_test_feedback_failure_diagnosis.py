from __future__ import annotations

from dataclasses import fields
import inspect

import pytest

import chanta_core.agent_runtime.sandbox_test_feedback as feedback_module
from chanta_core.agent_runtime import (
    SandboxDoNothingSignalKind,
    SandboxEvidenceStrength,
    SandboxFailureDiagnosisKind,
    SandboxFeedbackConfidenceLevel,
    SandboxFeedbackSeverity,
    SandboxRootCauseHypothesisKind,
    SandboxSuggestedNextActionKind,
    SandboxTestFeedbackDecisionKind,
    SandboxTestFeedbackMode,
    SandboxTestFeedbackReadinessLevel,
    SandboxTestFeedbackRiskKind,
    SandboxTestFeedbackSourceKind,
    SandboxTestFeedbackStatus,
    SandboxTestFailureClassKind,
    SandboxTestOutcomeKind,
    build_sandbox_evidence_assessment,
    build_sandbox_feedback_decision,
    build_sandbox_feedback_no_repair_guarantee,
    build_sandbox_root_cause_hypothesis,
    build_sandbox_suggested_next_action,
    build_sandbox_do_nothing_alternative_signal,
    build_sandbox_test_evidence_snippet,
    build_sandbox_test_failure_classification,
    build_sandbox_test_feedback_flags,
    build_sandbox_test_feedback_input,
    build_sandbox_test_feedback_policy,
    build_sandbox_test_feedback_report,
    build_sandbox_test_feedback_source_ref,
    build_sandbox_test_outcome_classification,
    build_sandbox_test_result_envelope,
    build_v0374_readiness_report,
    create_sandbox_test_feedback_report,
    default_sandbox_test_feedback_policy,
    generate_suggested_next_actions,
    sandbox_do_nothing_signal_is_not_scorecard,
    sandbox_feedback_flags_preserve_no_execution,
    sandbox_feedback_policy_blocks_repair_execution,
    sandbox_feedback_report_is_not_execution,
    sandbox_root_cause_hypothesis_is_not_proof,
    sandbox_suggested_next_action_is_not_execution,
    v0374_readiness_report_is_not_execution_ready,
)


SAFE_FLAG_NAMES = (
    "ready_for_v0375_repair_suggestion_metadata",
    "ready_for_v0376_vera_codex_one_shot_agent_trial",
    "ready_for_v0377_cold_agent_performance_evaluation",
    "ready_for_test_feedback_report",
    "ready_for_failure_diagnosis_report",
    "ready_for_root_cause_hypothesis_metadata",
    "ready_for_evidence_strength_assessment",
    "ready_for_suggested_next_action_metadata",
    "ready_for_do_nothing_alternative_signal",
    "ready_for_future_repair_suggestion_input",
    "ready_for_future_vera_codex_trial_input",
    "ready_for_future_cold_evaluation_input",
)

UNSAFE_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_test_execution",
    "ready_for_controlled_test_subprocess",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_dependency_install",
    "ready_for_network_access",
    "ready_for_repair_patch_proposal",
    "ready_for_automatic_repair",
    "ready_for_vera_codex_trial_execution",
    "ready_for_cold_agent_performance_evaluation",
    "ready_for_external_agent_execution",
    "ready_for_dominion_runtime",
)

UNSAFE_POLICY_NAMES = (
    "allow_test_execution",
    "allow_subprocess",
    "allow_shell",
    "allow_dependency_install",
    "allow_network_access",
    "allow_repair_patch_proposal",
    "allow_automatic_repair",
    "allow_vera_codex_trial_execution",
    "allow_cold_performance_evaluation",
    "allow_external_agent_execution",
    "allow_dominion_runtime",
)


def _values(enum_cls):
    return [item.value for item in enum_cls]


def _envelope(
    outcome_kind,
    failure_kind,
    *,
    passed: bool = False,
    failed: bool = True,
    inconclusive: bool = False,
    snippet_count: int = 2,
):
    snippets = [
        build_sandbox_test_evidence_snippet(
            evidence_snippet_id=f"snippet:{index}",
            snippet_text=f"evidence {index}",
            snippet_summary=f"evidence {index}",
        )
        for index in range(snippet_count)
    ]
    failure = build_sandbox_test_failure_classification(
        failure_class_kind=failure_kind,
        evidence_snippet_ids=[snippet.evidence_snippet_id for snippet in snippets],
        confidence="high" if snippet_count >= 2 else "low",
    )
    outcome = build_sandbox_test_outcome_classification(
        outcome_kind=outcome_kind,
        outcome_summary=f"{outcome_kind} outcome metadata",
        failure_classification_id=failure.failure_classification_id,
        evidence_snippet_ids=[snippet.evidence_snippet_id for snippet in snippets],
        confidence="high" if snippet_count >= 2 else "inconclusive",
        passed=passed,
        failed=failed,
        inconclusive=inconclusive,
    )
    return build_sandbox_test_result_envelope(
        outcome_classification=outcome,
        failure_classification=failure,
        evidence_snippets=snippets,
    )


def test_v0374_enum_values_are_complete():
    assert _values(SandboxTestFeedbackMode) == [
        "evidence_feedback_report",
        "failure_diagnosis_report",
        "root_cause_hypothesis_report",
        "do_nothing_signal_report",
        "future_repair_input_report",
        "blocked",
        "no_op",
        "unknown",
    ]
    assert _values(SandboxTestFeedbackSourceKind) == [
        "v0373_test_result_envelope",
        "v0373_outcome_classification",
        "v0373_failure_classification",
        "v0373_evidence_snippet",
        "v0372_sandbox_test_execution_result",
        "v0371_test_invocation_contract",
        "v0369_patch_apply_sandbox_consolidation",
        "manual_operator_input",
        "test_fixture",
        "unknown",
    ]
    assert "diagnosis_created_with_warnings" in _values(SandboxTestFeedbackStatus)
    assert "future_repair_input_ready" in _values(SandboxTestFeedbackReadinessLevel)
    assert "allow_future_repair_suggestion_input" in _values(SandboxTestFeedbackDecisionKind)
    assert "repair_permission_confusion_risk" in _values(SandboxTestFeedbackRiskKind)
    assert "missing_dependency_diagnosis" in _values(SandboxFailureDiagnosisKind)
    assert "implementation_bug_likely" in _values(SandboxRootCauseHypothesisKind)
    assert _values(SandboxEvidenceStrength) == ["strong", "moderate", "weak", "insufficient", "contradictory", "unknown"]
    assert _values(SandboxFeedbackSeverity) == ["info", "low", "medium", "high", "critical", "blocked", "unknown"]
    assert "inspect_missing_dependency_without_install" in _values(SandboxSuggestedNextActionKind)
    assert "do_nothing_required_due_to_insufficient_evidence" in _values(SandboxDoNothingSignalKind)
    assert _values(SandboxFeedbackConfidenceLevel) == ["high", "medium", "low", "inconclusive", "unknown"]


def test_feedback_flags_allow_metadata_readiness_but_preserve_no_execution():
    flags = build_sandbox_test_feedback_flags()
    for name in SAFE_FLAG_NAMES:
        assert getattr(flags, name) is True
    assert sandbox_feedback_flags_preserve_no_execution(flags)
    for name in UNSAFE_FLAG_NAMES:
        assert getattr(flags, name) is False
        with pytest.raises(ValueError):
            build_sandbox_test_feedback_flags(**{name: True})


def test_source_ref_policy_and_input_are_metadata_only():
    source = build_sandbox_test_feedback_source_ref()
    assert source.source_kind == SandboxTestFeedbackSourceKind.V0373_TEST_RESULT_ENVELOPE
    policy = default_sandbox_test_feedback_policy()
    assert policy.allow_feedback_report is True
    assert policy.allow_failure_diagnosis is True
    assert policy.allow_root_cause_hypothesis is True
    assert policy.allow_suggested_next_action_metadata is True
    assert policy.allow_do_nothing_signal is True
    assert policy.allow_future_repair_suggestion_input is True
    assert policy.allow_future_vera_codex_trial_input is True
    assert sandbox_feedback_policy_blocks_repair_execution(policy)
    for name in UNSAFE_POLICY_NAMES:
        assert getattr(policy, name) is False
        with pytest.raises(ValueError):
            build_sandbox_test_feedback_policy(**{name: True})
    request = build_sandbox_test_feedback_input()
    for action in ("test execution", "subprocess", "shell", "install", "network", "repair", "external agent", "Dominion", "evaluation execution"):
        assert action in request.prohibited_runtime_actions
    with pytest.raises(ValueError):
        build_sandbox_test_feedback_input(prohibited_runtime_actions=["repair"])


def test_evidence_assessment_strength_and_low_evidence_confidence_rule():
    for strength in SandboxEvidenceStrength:
        assessment = build_sandbox_evidence_assessment(
            evidence_strength=strength,
            confidence=SandboxFeedbackConfidenceLevel.LOW if strength in (SandboxEvidenceStrength.WEAK, SandboxEvidenceStrength.UNKNOWN) else SandboxFeedbackConfidenceLevel.INCONCLUSIVE,
        )
        assert assessment.evidence_strength == strength
    with pytest.raises(ValueError):
        build_sandbox_evidence_assessment(
            evidence_strength=SandboxEvidenceStrength.INSUFFICIENT,
            confidence=SandboxFeedbackConfidenceLevel.HIGH,
        )
    with pytest.raises(ValueError):
        build_sandbox_root_cause_hypothesis(
            evidence_strength=SandboxEvidenceStrength.WEAK,
            confidence=SandboxFeedbackConfidenceLevel.HIGH,
        )


def test_root_cause_action_and_do_nothing_models_never_execute_or_score():
    hypothesis = build_sandbox_root_cause_hypothesis()
    assert sandbox_root_cause_hypothesis_is_not_proof(hypothesis)
    with pytest.raises(ValueError):
        build_sandbox_root_cause_hypothesis(repair_allowed=True)
    action = build_sandbox_suggested_next_action()
    assert sandbox_suggested_next_action_is_not_execution(action)
    for name in ("executes_now", "repair_allowed", "test_rerun_allowed", "dependency_install_allowed"):
        with pytest.raises(ValueError):
            build_sandbox_suggested_next_action(**{name: True})
    signal = build_sandbox_do_nothing_alternative_signal()
    assert sandbox_do_nothing_signal_is_not_scorecard(signal)
    with pytest.raises(ValueError):
        build_sandbox_do_nothing_alternative_signal(scoring_performed=True)


def test_feedback_report_from_assertion_failure_is_future_input_only():
    envelope = _envelope(SandboxTestOutcomeKind.FAILED_ASSERTION, SandboxTestFailureClassKind.ASSERTION_FAILURE)
    report = create_sandbox_test_feedback_report(envelope)
    assert report.eligible_for_future_repair_suggestion is True
    assert report.eligible_for_future_vera_codex_trial is True
    assert report.eligible_for_future_cold_evaluation is True
    assert sandbox_feedback_report_is_not_execution(report)
    assert report.production_certified is False
    assert report.diagnosis_report.repair_allowed is False
    assert report.diagnosis_report.retry_allowed is False
    assert report.diagnosis_report.dependency_install_allowed is False
    assert report.diagnosis_report.observations[0].diagnosis_kind == SandboxFailureDiagnosisKind.ASSERTION_FAILURE_DIAGNOSIS
    assert report.diagnosis_report.hypotheses[0].hypothesis_kind == SandboxRootCauseHypothesisKind.IMPLEMENTATION_BUG_LIKELY
    assert report.diagnosis_report.hypotheses[0].proven is False
    assert any(action.action_kind == SandboxSuggestedNextActionKind.CREATE_REPAIR_SUGGESTION_FUTURE_GATE for action in report.suggested_actions)
    assert all(sandbox_suggested_next_action_is_not_execution(action) for action in report.suggested_actions)


def test_failed_inconclusive_missing_dependency_and_timeout_do_not_grant_success_repair_retry_or_install():
    inconclusive = _envelope(
        SandboxTestOutcomeKind.INCONCLUSIVE,
        SandboxTestFailureClassKind.INCONCLUSIVE_FAILURE,
        failed=False,
        inconclusive=True,
        snippet_count=0,
    )
    inconclusive_report = create_sandbox_test_feedback_report(inconclusive)
    assert inconclusive_report.diagnosis_report.inconclusive is True
    assert inconclusive_report.do_nothing_signal.signal_kind == SandboxDoNothingSignalKind.DO_NOTHING_REQUIRED_DUE_TO_INSUFFICIENT_EVIDENCE
    assert not any(action.action_kind == SandboxSuggestedNextActionKind.CREATE_REPAIR_SUGGESTION_FUTURE_GATE for action in inconclusive_report.suggested_actions)

    missing = _envelope(SandboxTestOutcomeKind.MISSING_DEPENDENCY, SandboxTestFailureClassKind.MISSING_DEPENDENCY_FAILURE)
    missing_report = create_sandbox_test_feedback_report(missing)
    assert any(action.action_kind == SandboxSuggestedNextActionKind.INSPECT_MISSING_DEPENDENCY_WITHOUT_INSTALL for action in missing_report.suggested_actions)
    assert missing_report.dependency_install_allowed is False

    timeout = _envelope(SandboxTestOutcomeKind.TIMEOUT, SandboxTestFailureClassKind.TIMEOUT_FAILURE)
    timeout_report = create_sandbox_test_feedback_report(timeout)
    assert any(action.action_kind == SandboxSuggestedNextActionKind.RERUN_TEST_FUTURE_GATE for action in timeout_report.suggested_actions)
    assert timeout_report.retry_allowed is False

    for report in (inconclusive_report, missing_report, timeout_report):
        assert report.production_certified is False
        assert report.repair_allowed is False
        assert report.repair_performed is False
        assert report.ready_for_execution is False


def test_negative_report_decision_and_guarantee_boundaries():
    with pytest.raises(ValueError):
        build_sandbox_test_feedback_report(production_certified=True)
    with pytest.raises(ValueError):
        build_sandbox_test_feedback_report(repair_performed=True)
    with pytest.raises(ValueError):
        build_sandbox_test_feedback_report(ready_for_execution=True)
    for name in (
        "test_execution_allowed",
        "subprocess_allowed",
        "shell_allowed",
        "dependency_install_allowed",
        "network_allowed",
        "repair_patch_proposal_allowed",
        "automatic_repair_allowed",
        "vera_codex_trial_execution_allowed",
        "cold_evaluation_execution_allowed",
        "external_agent_allowed",
        "dominion_runtime_allowed",
    ):
        with pytest.raises(ValueError):
            build_sandbox_feedback_decision(**{name: True})

    guarantee = build_sandbox_feedback_no_repair_guarantee()
    for field in fields(guarantee):
        if field.name.startswith("no_"):
            assert getattr(guarantee, field.name) is True


def test_v0374_readiness_report_preserves_unsafe_false():
    report = build_v0374_readiness_report()
    assert v0374_readiness_report_is_not_execution_ready(report)
    for name in SAFE_FLAG_NAMES:
        assert getattr(report, name) is True
    for name in (
        "ready_for_execution",
        "ready_for_test_execution",
        "ready_for_controlled_test_subprocess",
        "ready_for_shell_execution",
        "ready_for_subprocess_execution",
        "ready_for_command_execution",
        "ready_for_dependency_install",
        "ready_for_network_access",
        "ready_for_repair_patch_proposal",
        "ready_for_automatic_repair",
        "ready_for_multi_cycle_agentic_loop",
        "ready_for_vera_codex_trial_execution",
        "ready_for_cold_agent_performance_evaluation",
        "ready_for_external_agent_execution",
        "ready_for_dominion_runtime",
        "production_certified",
    ):
        assert getattr(report, name) is False
        with pytest.raises(ValueError):
            build_v0374_readiness_report(**{name: True})


def test_v0374_helpers_do_not_include_runtime_execution_calls():
    source = inspect.getsource(feedback_module)
    forbidden = (
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
    )
    for pattern in forbidden:
        assert pattern not in source
