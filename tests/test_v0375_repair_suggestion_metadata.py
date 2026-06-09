from __future__ import annotations

from dataclasses import fields
import inspect

import pytest

import chanta_core.agent_runtime.sandbox_repair_suggestion as repair_module
from chanta_core.agent_runtime import (
    SandboxDoNothingSignalKind,
    SandboxEvidenceStrength,
    SandboxFeedbackConfidenceLevel,
    SandboxRepairActionKind,
    SandboxRepairConfidenceLevel,
    SandboxRepairDoNothingComparisonKind,
    SandboxRepairEvidenceKind,
    SandboxRepairReviewRequirementKind,
    SandboxRepairScopeKind,
    SandboxRepairSuggestionDecisionKind,
    SandboxRepairSuggestionKind,
    SandboxRepairSuggestionMode,
    SandboxRepairSuggestionReadinessLevel,
    SandboxRepairSuggestionRiskKind,
    SandboxRepairSuggestionSourceKind,
    SandboxRepairSuggestionStatus,
    SandboxRepairUrgency,
    SandboxRootCauseHypothesisKind,
    SandboxSuggestedNextActionKind,
    build_sandbox_do_nothing_alternative_signal,
    build_sandbox_evidence_assessment,
    build_sandbox_failure_diagnosis_report,
    build_sandbox_root_cause_hypothesis,
    build_sandbox_suggested_next_action,
    build_sandbox_test_feedback_report,
    build_sandbox_repair_do_nothing_comparison,
    build_sandbox_repair_human_review_requirement,
    build_sandbox_repair_risk_assessment,
    build_sandbox_repair_scope,
    build_sandbox_repair_suggested_action,
    build_sandbox_repair_suggestion_decision,
    build_sandbox_repair_suggestion_envelope,
    build_sandbox_repair_suggestion_flags,
    build_sandbox_repair_suggestion_input,
    build_sandbox_repair_suggestion_no_auto_repair_guarantee,
    build_sandbox_repair_suggestion_policy,
    build_sandbox_repair_suggestion_source_ref,
    build_v0375_readiness_report,
    create_sandbox_repair_suggestion_envelope_from_feedback,
    default_sandbox_repair_suggestion_policy,
    sandbox_repair_action_is_not_execution,
    sandbox_repair_envelope_is_not_patch_proposal,
    sandbox_repair_scope_is_not_edit_permission,
    sandbox_repair_suggestion_flags_preserve_no_repair,
    sandbox_repair_suggestion_policy_blocks_repair_execution,
    v0375_readiness_report_is_not_execution_ready,
)


SAFE_FLAG_NAMES = (
    "ready_for_v0376_vera_codex_one_shot_agent_trial",
    "ready_for_v0377_cold_agent_performance_evaluation",
    "ready_for_v0378_cli_test_runner_agent_evaluation_surface",
    "ready_for_v038_bounded_repair_proposal_loop",
    "ready_for_repair_suggestion_metadata",
    "ready_for_repair_scope_metadata",
    "ready_for_repair_risk_assessment",
    "ready_for_repair_human_review_requirement",
    "ready_for_do_nothing_repair_comparison",
    "ready_for_future_repair_proposal_input",
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
    "ready_for_repair_diff_generation",
    "ready_for_code_hunk_generation",
    "ready_for_automatic_repair",
    "ready_for_repair_execution",
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
    "allow_repair_diff_generation",
    "allow_code_hunk_generation",
    "allow_automatic_repair",
    "allow_repair_execution",
    "allow_vera_codex_trial_execution",
    "allow_cold_performance_evaluation",
    "allow_external_agent_execution",
    "allow_dominion_runtime",
)


def _values(enum_cls):
    return [item.value for item in enum_cls]


def _feedback_report(*, hypothesis_kind, evidence_strength, confidence, action_kind, do_nothing_kind, inconclusive=False):
    assessment = build_sandbox_evidence_assessment(
        evidence_strength=evidence_strength,
        confidence=confidence,
        supporting_evidence_refs=["evidence:1"] if evidence_strength != SandboxEvidenceStrength.INSUFFICIENT else [],
        insufficient_evidence=evidence_strength == SandboxEvidenceStrength.INSUFFICIENT,
    )
    hypothesis = build_sandbox_root_cause_hypothesis(
        hypothesis_kind=hypothesis_kind,
        evidence_assessment=assessment,
        evidence_strength=evidence_strength,
        confidence=confidence,
    )
    diagnosis = build_sandbox_failure_diagnosis_report(
        hypotheses=[hypothesis],
        evidence_assessments=[assessment],
        inconclusive=inconclusive,
    )
    action = build_sandbox_suggested_next_action(action_kind=action_kind)
    do_nothing = build_sandbox_do_nothing_alternative_signal(signal_kind=do_nothing_kind)
    return build_sandbox_test_feedback_report(
        diagnosis_report=diagnosis,
        suggested_actions=[action],
        do_nothing_signal=do_nothing,
    )


def test_v0375_enum_values_are_complete():
    assert _values(SandboxRepairSuggestionMode) == [
        "metadata_only_suggestion",
        "evidence_based_repair_hint",
        "scope_only_repair_hint",
        "human_review_repair_hint",
        "do_nothing_comparison_hint",
        "future_repair_proposal_input",
        "blocked",
        "no_op",
        "unknown",
    ]
    assert "v0374_test_feedback_report" in _values(SandboxRepairSuggestionSourceKind)
    assert "suggestion_created_with_warnings" in _values(SandboxRepairSuggestionStatus)
    assert "future_handoff_ready_for_v038" in _values(SandboxRepairSuggestionReadinessLevel)
    assert "allow_future_repair_proposal_input" in _values(SandboxRepairSuggestionDecisionKind)
    assert "repair_patch_confusion_risk" in _values(SandboxRepairSuggestionRiskKind)
    assert "inspect_missing_dependency_without_install" in _values(SandboxRepairSuggestionKind)
    assert "implementation_scope" in _values(SandboxRepairScopeKind)
    assert "inspect_timeout_without_retry" in _values(SandboxRepairActionKind)
    assert "root_cause_hypothesis_ref" in _values(SandboxRepairEvidenceKind)
    assert _values(SandboxRepairUrgency) == ["none", "low", "medium", "high", "blocked", "unknown"]
    assert _values(SandboxRepairConfidenceLevel) == ["high", "medium", "low", "inconclusive", "unknown"]
    assert "human_review_required_before_any_apply" in _values(SandboxRepairReviewRequirementKind)
    assert "do_nothing_required_due_to_insufficient_evidence" in _values(SandboxRepairDoNothingComparisonKind)


def test_repair_flags_allow_metadata_readiness_but_preserve_no_repair():
    flags = build_sandbox_repair_suggestion_flags()
    for name in SAFE_FLAG_NAMES:
        assert getattr(flags, name) is True
    assert sandbox_repair_suggestion_flags_preserve_no_repair(flags)
    for name in UNSAFE_FLAG_NAMES:
        assert getattr(flags, name) is False
        with pytest.raises(ValueError):
            build_sandbox_repair_suggestion_flags(**{name: True})


def test_source_policy_and_input_are_metadata_only():
    source = build_sandbox_repair_suggestion_source_ref()
    assert source.source_kind == SandboxRepairSuggestionSourceKind.V0374_TEST_FEEDBACK_REPORT
    policy = default_sandbox_repair_suggestion_policy()
    assert policy.allow_repair_suggestion_metadata is True
    assert policy.allow_scope_metadata is True
    assert policy.allow_risk_assessment is True
    assert policy.allow_human_review_requirement is True
    assert policy.allow_future_repair_proposal_input is True
    assert sandbox_repair_suggestion_policy_blocks_repair_execution(policy)
    for name in UNSAFE_POLICY_NAMES:
        assert getattr(policy, name) is False
        with pytest.raises(ValueError):
            build_sandbox_repair_suggestion_policy(**{name: True})
    request = build_sandbox_repair_suggestion_input()
    for action in ("patch proposal", "diff generation", "code edit", "apply", "test execution", "subprocess", "shell", "install", "network", "repair execution", "external agent", "Dominion"):
        assert action in request.prohibited_runtime_actions
    with pytest.raises(ValueError):
        build_sandbox_repair_suggestion_input(prohibited_runtime_actions=["repair execution"])


def test_scope_risk_do_nothing_review_and_action_boundaries():
    scope = build_sandbox_repair_scope()
    assert sandbox_repair_scope_is_not_edit_permission(scope)
    with pytest.raises(ValueError):
        build_sandbox_repair_scope(edit_allowed=True)
    with pytest.raises(ValueError):
        build_sandbox_repair_risk_assessment(severity="high", requires_human_review=False)
    high_risk = build_sandbox_repair_risk_assessment(severity="high", requires_human_review=True)
    assert high_risk.requires_human_review is True
    comparison = build_sandbox_repair_do_nothing_comparison()
    assert comparison.scoring_performed is False
    with pytest.raises(ValueError):
        build_sandbox_repair_do_nothing_comparison(scoring_performed=True)
    review = build_sandbox_repair_human_review_requirement()
    assert review.human_approval_present is False
    with pytest.raises(ValueError):
        build_sandbox_repair_human_review_requirement(human_approval_present=True)
    action = build_sandbox_repair_suggested_action()
    assert sandbox_repair_action_is_not_execution(action)
    for name in ("executes_now", "generates_patch", "edits_code", "applies_patch", "runs_tests", "installs_dependency"):
        with pytest.raises(ValueError):
            build_sandbox_repair_suggested_action(**{name: True})


def test_repair_suggestion_from_feedback_is_future_input_only():
    feedback = _feedback_report(
        hypothesis_kind=SandboxRootCauseHypothesisKind.IMPLEMENTATION_BUG_LIKELY,
        evidence_strength=SandboxEvidenceStrength.STRONG,
        confidence=SandboxFeedbackConfidenceLevel.HIGH,
        action_kind=SandboxSuggestedNextActionKind.CREATE_REPAIR_SUGGESTION_FUTURE_GATE,
        do_nothing_kind=SandboxDoNothingSignalKind.DO_NOTHING_COMPETITIVE,
    )
    envelope = create_sandbox_repair_suggestion_envelope_from_feedback(feedback)
    assert envelope.suggestion_kind == SandboxRepairSuggestionKind.REVISE_IMPLEMENTATION_FUTURE_GATE
    assert envelope.scope.scope_kind == SandboxRepairScopeKind.IMPLEMENTATION_SCOPE
    assert envelope.eligible_for_future_repair_proposal is True
    assert envelope.eligible_for_future_vera_codex_trial is True
    assert envelope.eligible_for_future_cold_evaluation is True
    assert sandbox_repair_envelope_is_not_patch_proposal(envelope)
    assert envelope.dependency_install_allowed is False
    assert envelope.production_certified is False
    assert envelope.human_review_requirement.human_approval_present is False
    assert envelope.do_nothing_comparison.scoring_performed is False
    assert all(sandbox_repair_action_is_not_execution(action) for action in envelope.suggested_actions)


def test_missing_dependency_timeout_and_weak_evidence_do_not_install_retry_or_repair_now():
    missing = _feedback_report(
        hypothesis_kind=SandboxRootCauseHypothesisKind.MISSING_DEPENDENCY_LIKELY,
        evidence_strength=SandboxEvidenceStrength.MODERATE,
        confidence=SandboxFeedbackConfidenceLevel.MEDIUM,
        action_kind=SandboxSuggestedNextActionKind.INSPECT_MISSING_DEPENDENCY_WITHOUT_INSTALL,
        do_nothing_kind=SandboxDoNothingSignalKind.DO_NOTHING_COMPETITIVE,
    )
    missing_envelope = create_sandbox_repair_suggestion_envelope_from_feedback(missing)
    assert missing_envelope.suggestion_kind == SandboxRepairSuggestionKind.INSPECT_MISSING_DEPENDENCY_WITHOUT_INSTALL
    assert any(action.action_kind == SandboxRepairActionKind.INSPECT_MISSING_DEPENDENCY_WITHOUT_INSTALL for action in missing_envelope.suggested_actions)
    assert missing_envelope.dependency_install_allowed is False

    timeout = _feedback_report(
        hypothesis_kind=SandboxRootCauseHypothesisKind.TIMEOUT_OR_PERFORMANCE_ISSUE_LIKELY,
        evidence_strength=SandboxEvidenceStrength.MODERATE,
        confidence=SandboxFeedbackConfidenceLevel.MEDIUM,
        action_kind=SandboxSuggestedNextActionKind.RERUN_TEST_FUTURE_GATE,
        do_nothing_kind=SandboxDoNothingSignalKind.DO_NOTHING_COMPETITIVE,
    )
    timeout_envelope = create_sandbox_repair_suggestion_envelope_from_feedback(timeout)
    assert timeout_envelope.suggestion_kind == SandboxRepairSuggestionKind.INSPECT_TIMEOUT_OR_PERFORMANCE_FUTURE_GATE
    assert any(action.action_kind == SandboxRepairActionKind.INSPECT_TIMEOUT_WITHOUT_RETRY for action in timeout_envelope.suggested_actions)
    assert timeout_envelope.tests_rerun is False

    weak = _feedback_report(
        hypothesis_kind=SandboxRootCauseHypothesisKind.INCONCLUSIVE,
        evidence_strength=SandboxEvidenceStrength.INSUFFICIENT,
        confidence=SandboxFeedbackConfidenceLevel.INCONCLUSIVE,
        action_kind=SandboxSuggestedNextActionKind.DO_NOTHING,
        do_nothing_kind=SandboxDoNothingSignalKind.DO_NOTHING_REQUIRED_DUE_TO_INSUFFICIENT_EVIDENCE,
        inconclusive=True,
    )
    weak_envelope = create_sandbox_repair_suggestion_envelope_from_feedback(weak)
    assert weak_envelope.suggestion_kind == SandboxRepairSuggestionKind.BLOCK_DUE_TO_INSUFFICIENT_EVIDENCE
    assert weak_envelope.eligible_for_future_repair_proposal is False
    assert weak_envelope.do_nothing_comparison.comparison_kind == SandboxRepairDoNothingComparisonKind.DO_NOTHING_REQUIRED_DUE_TO_INSUFFICIENT_EVIDENCE
    assert weak_envelope.do_nothing_comparison.do_nothing_remains_valid is True
    assert weak_envelope.risk_assessment.requires_human_review is True


def test_negative_envelope_decision_and_no_auto_repair_guarantee():
    for name in (
        "repair_patch_proposal_created",
        "repair_diff_generated",
        "code_hunk_generated",
        "repair_executed",
        "tests_rerun",
        "dependency_install_allowed",
        "production_certified",
        "ready_for_execution",
    ):
        with pytest.raises(ValueError):
            build_sandbox_repair_suggestion_envelope(**{name: True})
    for name in (
        "patch_proposal_allowed",
        "diff_generation_allowed",
        "code_hunk_generation_allowed",
        "file_edit_allowed",
        "patch_apply_allowed",
        "test_execution_allowed",
        "subprocess_allowed",
        "shell_allowed",
        "dependency_install_allowed",
        "network_allowed",
        "repair_execution_allowed",
        "vera_codex_trial_execution_allowed",
        "external_agent_allowed",
        "dominion_runtime_allowed",
    ):
        with pytest.raises(ValueError):
            build_sandbox_repair_suggestion_decision(**{name: True})
    guarantee = build_sandbox_repair_suggestion_no_auto_repair_guarantee()
    for field in fields(guarantee):
        if field.name.startswith("no_"):
            assert getattr(guarantee, field.name) is True


def test_v0375_readiness_report_preserves_unsafe_false():
    report = build_v0375_readiness_report()
    assert v0375_readiness_report_is_not_execution_ready(report)
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
        "ready_for_repair_diff_generation",
        "ready_for_code_hunk_generation",
        "ready_for_automatic_repair",
        "ready_for_repair_execution",
        "ready_for_multi_cycle_agentic_loop",
        "ready_for_vera_codex_trial_execution",
        "ready_for_cold_agent_performance_evaluation",
        "ready_for_external_agent_execution",
        "ready_for_dominion_runtime",
        "production_certified",
    ):
        assert getattr(report, name) is False
        with pytest.raises(ValueError):
            build_v0375_readiness_report(**{name: True})


def test_v0375_helpers_do_not_include_runtime_execution_or_patch_calls():
    source = inspect.getsource(repair_module)
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
