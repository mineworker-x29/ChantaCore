from __future__ import annotations

from dataclasses import fields
import inspect

import pytest

import chanta_core.agent_runtime.sandbox_test_result as result_module
from chanta_core.agent_runtime import (
    SandboxTestConfidenceLevel,
    SandboxTestEvidenceKind,
    SandboxTestFailureClassKind,
    SandboxTestOutcomeKind,
    SandboxTestOutputSignalKind,
    SandboxTestProcessClassificationKind,
    SandboxTestResultDecisionKind,
    SandboxTestResultEnvelopeMode,
    SandboxTestResultReadinessLevel,
    SandboxTestResultRiskKind,
    SandboxTestResultSourceKind,
    SandboxTestResultStatus,
    build_controlled_test_subprocess_result,
    build_sandbox_test_execution_result,
    build_sandbox_test_failure_classification,
    build_sandbox_test_outcome_classification,
    build_sandbox_test_result_envelope,
    build_sandbox_test_result_envelope_decision,
    build_sandbox_test_result_envelope_input,
    build_sandbox_test_result_flags,
    build_sandbox_test_result_no_execution_guarantee,
    build_sandbox_test_result_policy,
    build_sandbox_test_result_source_ref,
    build_v0373_readiness_report,
    classify_sandbox_test_failure,
    classify_sandbox_test_outcome,
    classify_sandbox_test_process_result,
    create_sandbox_test_result_envelope_from_execution_result,
    default_sandbox_test_result_policy,
    detect_sandbox_test_output_signals,
    extract_sandbox_test_evidence_snippets,
    sandbox_test_failure_classification_blocks_repair,
    sandbox_test_outcome_is_not_production_certification,
    sandbox_test_result_envelope_is_not_execution,
    sandbox_test_result_flags_preserve_no_execution,
    sandbox_test_result_policy_blocks_execution,
    v0373_readiness_report_is_not_execution_ready,
)


SAFE_FLAG_NAMES = (
    "ready_for_v0374_test_feedback_failure_diagnosis",
    "ready_for_v0375_repair_suggestion_metadata",
    "ready_for_v0376_vera_codex_one_shot_agent_trial",
    "ready_for_v0377_cold_agent_performance_evaluation",
    "ready_for_test_result_envelope",
    "ready_for_test_output_classifier",
    "ready_for_process_exit_classification",
    "ready_for_test_failure_classification",
    "ready_for_test_evidence_snippets",
    "ready_for_future_feedback_report_input",
    "ready_for_future_vera_codex_trial_evidence",
    "ready_for_future_cold_evaluation_evidence",
)

UNSAFE_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_test_execution",
    "ready_for_controlled_test_subprocess",
    "ready_for_pytest_execution",
    "ready_for_npm_test_execution",
    "ready_for_unittest_execution",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_dependency_install",
    "ready_for_network_access",
    "ready_for_automatic_repair",
    "ready_for_multi_cycle_agentic_loop",
    "ready_for_vera_codex_trial_execution",
    "ready_for_external_agent_execution",
    "ready_for_dominion_runtime",
)

UNSAFE_POLICY_NAMES = (
    "allow_test_execution",
    "allow_subprocess",
    "allow_shell",
    "allow_dependency_install",
    "allow_network_access",
    "allow_automatic_repair",
    "allow_vera_codex_trial_execution",
    "allow_cold_performance_evaluation",
    "allow_external_agent_execution",
    "allow_dominion_runtime",
)


def _values(enum_cls):
    return [item.value for item in enum_cls]


def _classify(stdout: str, stderr: str = "", return_code: int | None = 1, timed_out: bool = False):
    envelope_input = build_sandbox_test_result_envelope_input(
        stdout_text=stdout,
        stderr_text=stderr,
        return_code=return_code,
        timed_out=timed_out,
    )
    process = classify_sandbox_test_process_result(envelope_input)
    signals = detect_sandbox_test_output_signals(stdout, stderr)
    snippets = extract_sandbox_test_evidence_snippets(stdout, stderr, signals)
    failure = classify_sandbox_test_failure(process, signals, snippets)
    outcome = classify_sandbox_test_outcome(process, failure, signals, snippets)
    return process, signals, snippets, failure, outcome


def test_v0373_enum_values_are_complete():
    assert _values(SandboxTestResultEnvelopeMode) == [
        "process_result_envelope",
        "output_classifier_envelope",
        "combined_result_envelope",
        "evidence_only_envelope",
        "blocked",
        "no_op",
        "unknown",
    ]
    assert _values(SandboxTestResultSourceKind) == [
        "v0372_sandbox_test_execution_result",
        "v0372_controlled_subprocess_result",
        "v0372_output_capture",
        "v0371_invocation_contract",
        "v0371_command_spec",
        "v0370_test_runner_boundary",
        "manual_operator_input",
        "test_fixture",
        "unknown",
    ]
    assert _values(SandboxTestResultStatus) == [
        "unknown",
        "draft",
        "input_validated",
        "classified",
        "classified_with_warnings",
        "envelope_created",
        "blocked",
        "review_required",
        "future_gated",
        "no_op",
        "safe_failed",
    ]
    assert "output_classifier_ready" in _values(SandboxTestResultReadinessLevel)
    assert "allow_output_classification" in _values(SandboxTestResultDecisionKind)
    assert "failure_repair_confusion_risk" in _values(SandboxTestResultRiskKind)
    assert "process_exit_zero" in _values(SandboxTestProcessClassificationKind)
    assert "missing_dependency" in _values(SandboxTestOutcomeKind)
    assert "missing_dependency_failure" in _values(SandboxTestFailureClassKind)
    assert "missing_dependency_excerpt" in _values(SandboxTestEvidenceKind)
    assert _values(SandboxTestConfidenceLevel) == ["high", "medium", "low", "inconclusive", "unknown"]
    assert "secret_like_output_signal" in _values(SandboxTestOutputSignalKind)


def test_result_flags_allow_classifier_readiness_but_preserve_no_execution():
    flags = build_sandbox_test_result_flags()
    for name in SAFE_FLAG_NAMES:
        assert getattr(flags, name) is True
    assert sandbox_test_result_flags_preserve_no_execution(flags)
    for name in UNSAFE_FLAG_NAMES:
        assert getattr(flags, name) is False
        with pytest.raises(ValueError):
            build_sandbox_test_result_flags(**{name: True})


def test_source_ref_and_policy_are_metadata_only_and_block_execution():
    source = build_sandbox_test_result_source_ref()
    assert source.source_kind == SandboxTestResultSourceKind.V0372_SANDBOX_TEST_EXECUTION_RESULT
    policy = default_sandbox_test_result_policy()
    assert policy.allow_process_classification is True
    assert policy.allow_output_classification is True
    assert policy.allow_evidence_snippet_extraction is True
    assert policy.allow_future_feedback_input is True
    assert policy.allow_future_vera_codex_evidence is True
    assert sandbox_test_result_policy_blocks_execution(policy)
    for name in UNSAFE_POLICY_NAMES:
        assert getattr(policy, name) is False
        with pytest.raises(ValueError):
            build_sandbox_test_result_policy(**{name: True})


def test_envelope_input_is_classifier_request_not_execution_request():
    request = build_sandbox_test_result_envelope_input(stdout_text="1 passed in 0.01s", return_code=0)
    assert request.return_code == 0
    for action in ("test execution", "subprocess", "shell", "install", "network", "repair", "external agent", "Dominion"):
        assert action in request.prohibited_runtime_actions
    with pytest.raises(ValueError):
        build_sandbox_test_result_envelope_input(prohibited_runtime_actions=["shell"])


def test_process_classification_exit_zero_nonzero_timeout_and_missing():
    zero = classify_sandbox_test_process_result(build_sandbox_test_result_envelope_input(return_code=0, timed_out=False))
    assert zero.classification_kind == SandboxTestProcessClassificationKind.PROCESS_EXIT_ZERO
    assert zero.production_certified is False
    nonzero = classify_sandbox_test_process_result(build_sandbox_test_result_envelope_input(return_code=2, timed_out=False))
    assert nonzero.classification_kind == SandboxTestProcessClassificationKind.PROCESS_EXIT_NONZERO
    timeout = classify_sandbox_test_process_result(build_sandbox_test_result_envelope_input(return_code=None, timed_out=True))
    assert timeout.classification_kind == SandboxTestProcessClassificationKind.PROCESS_TIMEOUT
    missing = classify_sandbox_test_process_result(build_sandbox_test_result_envelope_input(return_code=None, timed_out=False))
    assert missing.classification_kind == SandboxTestProcessClassificationKind.NOT_EXECUTED


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("1 passed in 0.01s", SandboxTestOutputSignalKind.PYTEST_PASSED_SIGNAL),
        ("FAILED tests/test_sample.py::test_x\n1 failed", SandboxTestOutputSignalKind.PYTEST_FAILED_SIGNAL),
        ("Traceback (most recent call last):", SandboxTestOutputSignalKind.TRACEBACK_SIGNAL),
        ("ImportError: cannot import name x", SandboxTestOutputSignalKind.IMPORT_ERROR_SIGNAL),
        ("SyntaxError: invalid syntax", SandboxTestOutputSignalKind.SYNTAX_ERROR_SIGNAL),
        ("ModuleNotFoundError: No module named 'missing_dep'", SandboxTestOutputSignalKind.MISSING_MODULE_SIGNAL),
        ("collected 0 items\nno tests ran", SandboxTestOutputSignalKind.NO_TESTS_COLLECTED_SIGNAL),
        ("Ran 1 test in 0.001s\n\nOK", SandboxTestOutputSignalKind.UNITTEST_OK_SIGNAL),
        ("FAIL: test_x", SandboxTestOutputSignalKind.UNITTEST_FAILED_SIGNAL),
    ],
)
def test_output_signal_detection(text, expected):
    signals = detect_sandbox_test_output_signals(text, "")
    assert expected in {signal.signal_kind for signal in signals}


def test_evidence_snippets_are_bounded_and_redact_secret_like_output():
    policy = build_sandbox_test_result_policy(max_evidence_snippet_chars=16)
    signals = detect_sandbox_test_output_signals("api_key=abc SECRET", "")
    snippets = extract_sandbox_test_evidence_snippets("api_key=abc SECRET", "", signals, policy)
    assert snippets
    assert len(snippets[0].snippet_text) <= 16 or snippets[0].truncated is True
    assert any(snippet.redacted for snippet in snippets)
    assert any(snippet.secret_like_content_detected for snippet in snippets)


def test_failure_and_outcome_classification_blocks_repair_retry_and_install():
    _, _, _, failure, outcome = _classify("AssertionError: expected 1 == 2")
    assert failure.failure_class_kind == SandboxTestFailureClassKind.ASSERTION_FAILURE
    assert sandbox_test_failure_classification_blocks_repair(failure)
    assert outcome.outcome_kind == SandboxTestOutcomeKind.FAILED_ASSERTION
    assert sandbox_test_outcome_is_not_production_certification(outcome)

    _, _, _, failure, outcome = _classify("ImportError: cannot import x")
    assert failure.failure_class_kind == SandboxTestFailureClassKind.IMPORT_FAILURE
    assert outcome.outcome_kind == SandboxTestOutcomeKind.IMPORT_ERROR

    _, _, _, failure, outcome = _classify("SyntaxError: invalid syntax")
    assert failure.failure_class_kind == SandboxTestFailureClassKind.SYNTAX_FAILURE
    assert outcome.outcome_kind == SandboxTestOutcomeKind.SYNTAX_ERROR

    _, _, _, failure, outcome = _classify("ModuleNotFoundError: No module named 'not_here'")
    assert failure.failure_class_kind == SandboxTestFailureClassKind.MISSING_DEPENDENCY_FAILURE
    assert failure.dependency_install_allowed is False
    assert outcome.outcome_kind == SandboxTestOutcomeKind.MISSING_DEPENDENCY

    _, _, _, failure, outcome = _classify("process timed out", timed_out=True)
    assert failure.failure_class_kind == SandboxTestFailureClassKind.TIMEOUT_FAILURE
    assert failure.retry_allowed is False
    assert outcome.outcome_kind == SandboxTestOutcomeKind.TIMEOUT


def test_passed_and_inconclusive_outcomes_do_not_certify_production():
    _, _, _, failure, outcome = _classify("1 passed in 0.01s", return_code=0)
    assert failure.failure_class_kind == SandboxTestFailureClassKind.NO_FAILURE_DETECTED
    assert outcome.outcome_kind == SandboxTestOutcomeKind.PASSED
    assert outcome.production_certified is False

    _, _, _, failure, outcome = _classify("", return_code=None)
    assert failure.failure_class_kind == SandboxTestFailureClassKind.INCONCLUSIVE_FAILURE
    assert outcome.outcome_kind == SandboxTestOutcomeKind.INCONCLUSIVE
    assert outcome.inconclusive is True


def test_result_envelope_consumes_supplied_v0372_metadata_only():
    subprocess_result = build_controlled_test_subprocess_result(
        subprocess_result_id="subprocess-result:v0.37.2:test",
        return_code=0,
        stdout_text="1 passed in 0.01s",
    )
    execution_result = build_sandbox_test_execution_result(
        execution_result_id="execution-result:v0.37.2:test",
        subprocess_result=subprocess_result,
        return_code=0,
        timed_out=False,
    )
    envelope = create_sandbox_test_result_envelope_from_execution_result(execution_result)
    assert envelope.eligible_for_future_feedback_report is True
    assert envelope.eligible_for_future_vera_codex_trial is True
    assert envelope.eligible_for_future_cold_evaluation is True
    assert envelope.test_execution_performed is False
    assert envelope.subprocess_executed_by_v0373 is False
    assert envelope.repair_allowed is False
    assert envelope.retry_allowed is False
    assert envelope.dependency_install_allowed is False
    assert envelope.production_certified is False
    assert sandbox_test_result_envelope_is_not_execution(envelope)
    assert envelope.outcome_classification.outcome_kind == SandboxTestOutcomeKind.PASSED


def test_result_envelope_and_decision_reject_unsafe_authority_claims():
    with pytest.raises(ValueError):
        build_sandbox_test_result_envelope(subprocess_executed_by_v0373=True)
    with pytest.raises(ValueError):
        build_sandbox_test_result_envelope(production_certified=True)
    with pytest.raises(ValueError):
        build_sandbox_test_result_envelope(ready_for_execution=True)
    with pytest.raises(ValueError):
        build_sandbox_test_failure_classification(repair_allowed=True)
    with pytest.raises(ValueError):
        build_sandbox_test_failure_classification(retry_allowed=True)
    with pytest.raises(ValueError):
        build_sandbox_test_failure_classification(dependency_install_allowed=True)
    with pytest.raises(ValueError):
        build_sandbox_test_outcome_classification(production_certified=True)
    for name in (
        "test_execution_allowed",
        "subprocess_allowed",
        "shell_allowed",
        "dependency_install_allowed",
        "network_allowed",
        "repair_allowed",
        "vera_codex_trial_execution_allowed",
        "external_agent_allowed",
        "dominion_runtime_allowed",
    ):
        with pytest.raises(ValueError):
            build_sandbox_test_result_envelope_decision(**{name: True})


def test_no_execution_guarantee_and_readiness_report_preserve_boundary():
    guarantee = build_sandbox_test_result_no_execution_guarantee()
    for field in fields(guarantee):
        if field.name.startswith("no_"):
            assert getattr(guarantee, field.name) is True
    readiness = build_v0373_readiness_report()
    assert v0373_readiness_report_is_not_execution_ready(readiness)
    for name in SAFE_FLAG_NAMES:
        assert getattr(readiness, name) is True
    for name in (
        "ready_for_execution",
        "ready_for_test_execution",
        "ready_for_controlled_test_subprocess",
        "ready_for_shell_execution",
        "ready_for_subprocess_execution",
        "ready_for_command_execution",
        "ready_for_dependency_install",
        "ready_for_network_access",
        "ready_for_automatic_repair",
        "ready_for_multi_cycle_agentic_loop",
        "ready_for_vera_codex_trial_execution",
        "ready_for_cold_agent_performance_evaluation",
        "ready_for_external_agent_execution",
        "ready_for_dominion_runtime",
        "production_certified",
    ):
        assert getattr(readiness, name) is False
        with pytest.raises(ValueError):
            build_v0373_readiness_report(**{name: True})


def test_v0373_helpers_do_not_include_runtime_execution_calls():
    source = inspect.getsource(result_module)
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
