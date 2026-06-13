from __future__ import annotations

import re
from pathlib import Path

import pytest

from chanta_core.agent_runtime.repair_mission_loop_negative_gates import (
    ALLOWED_SAFE_ALTERNATIVES,
    REQUIRED_NEGATIVE_ACTION_TYPES,
    NegativeRuntimeActionKind,
    RuntimeFalseClaimKind,
    RuntimeFalseClaimRequest,
    audit_production_certification_false_claims,
    audit_standalone_runtime_false_claims,
    build_denied_runtime_action_coverage_matrix,
    build_negative_runtime_gate_regression_suite,
    create_default_negative_runtime_gate_policy,
    create_negative_runtime_gate_readiness_report,
    create_negative_runtime_gate_safety_report,
    create_negative_runtime_request,
    create_v0404_human_checkpoint_hardening_handoff,
    create_v041_smoke_run_acceleration_safety_signal,
    denied_runtime_coverage_matrix_is_complete,
    detect_runtime_false_claim,
    evaluate_negative_runtime_request,
    negative_runtime_decision_preserves_no_authority,
    negative_runtime_evaluation_is_metadata_only,
    negative_runtime_readiness_preserves_no_unsafe_runtime,
    negative_runtime_suite_is_complete_and_blocked,
    v041_acceleration_safety_signal_is_not_runtime_start,
)


@pytest.mark.parametrize("action_type", REQUIRED_NEGATIVE_ACTION_TYPES)
def test_v0403_each_negative_action_is_blocked(action_type: str) -> None:
    evaluation = evaluate_negative_runtime_request(create_negative_runtime_request(action_type))

    assert evaluation.blocked is True
    assert evaluation.executed is False
    assert evaluation.decision.decision_kind in {"block", "stop"}
    assert negative_runtime_decision_preserves_no_authority(evaluation.decision)


def test_v0403_required_negative_action_kinds_are_declared() -> None:
    assert {item.value for item in NegativeRuntimeActionKind} == set(REQUIRED_NEGATIVE_ACTION_TYPES)
    assert {
        "model_provider_invocation",
        "prompt_submission",
        "subagent_invocation",
        "external_agent_execution",
        "automatic_repair",
        "retry_loop",
        "unbounded_multi_cycle_loop",
        "live_workspace_apply",
        "standalone_runtime_claim",
        "dominion_runtime",
        "production_certification",
        "shell_" + "sub" + "process_command",
        "dependency_install",
        "network_access",
        "credential_access",
    }.issubset(set(REQUIRED_NEGATIVE_ACTION_TYPES))


def test_v0403_negative_runtime_request_is_metadata_only() -> None:
    request = create_negative_runtime_request()

    assert request.metadata_only is True
    with pytest.raises(ValueError):
        create_negative_runtime_request(metadata_only=False)


def test_v0403_policy_is_deny_by_default_and_execution_disallowed() -> None:
    policy = create_default_negative_runtime_gate_policy()

    assert policy.deny_by_default is True
    assert policy.human_checkpoint_required_for_ambiguity is True
    assert policy.runtime_execution_allowed is False
    assert set(REQUIRED_NEGATIVE_ACTION_TYPES).issubset(policy.denied_action_types)
    with pytest.raises(ValueError):
        create_default_negative_runtime_gate_policy(runtime_execution_allowed=True)


def test_v0403_model_provider_invocation_is_blocked() -> None:
    assert evaluate_negative_runtime_request(create_negative_runtime_request("model_provider_invocation")).blocked


def test_v0403_prompt_submission_is_blocked() -> None:
    assert evaluate_negative_runtime_request(create_negative_runtime_request("prompt_submission")).blocked


def test_v0403_subagent_invocation_is_blocked() -> None:
    assert evaluate_negative_runtime_request(create_negative_runtime_request("subagent_invocation")).blocked


def test_v0403_external_agent_execution_is_blocked() -> None:
    assert evaluate_negative_runtime_request(create_negative_runtime_request("external_agent_execution")).blocked


def test_v0403_automatic_repair_is_blocked() -> None:
    assert evaluate_negative_runtime_request(create_negative_runtime_request("automatic_repair")).blocked


def test_v0403_retry_loop_is_blocked() -> None:
    assert evaluate_negative_runtime_request(create_negative_runtime_request("retry_loop")).blocked


def test_v0403_unbounded_multi_cycle_loop_is_blocked() -> None:
    assert evaluate_negative_runtime_request(create_negative_runtime_request("unbounded_multi_cycle_loop")).blocked


def test_v0403_live_workspace_apply_is_blocked() -> None:
    assert evaluate_negative_runtime_request(create_negative_runtime_request("live_workspace_apply")).blocked


def test_v0403_standalone_runtime_claim_is_blocked() -> None:
    evaluation = evaluate_negative_runtime_request(create_negative_runtime_request("standalone_runtime_claim"))

    assert evaluation.blocked is True
    assert evaluation.decision.decision_kind == "stop"


def test_v0403_dominion_runtime_is_blocked() -> None:
    assert evaluate_negative_runtime_request(create_negative_runtime_request("dominion_runtime")).blocked


def test_v0403_production_certification_is_blocked() -> None:
    assert evaluate_negative_runtime_request(create_negative_runtime_request("production_certification")).blocked


def test_v0403_shell_subprocess_command_is_blocked() -> None:
    action = "shell_" + "sub" + "process_command"
    assert evaluate_negative_runtime_request(create_negative_runtime_request(action)).blocked


def test_v0403_dependency_install_is_blocked() -> None:
    assert evaluate_negative_runtime_request(create_negative_runtime_request("dependency_install")).blocked


def test_v0403_network_access_is_blocked() -> None:
    assert evaluate_negative_runtime_request(create_negative_runtime_request("network_access")).blocked


def test_v0403_credential_access_is_blocked() -> None:
    assert evaluate_negative_runtime_request(create_negative_runtime_request("credential_access")).blocked


def test_v0403_decision_never_grants_runtime_authority() -> None:
    for action_type in REQUIRED_NEGATIVE_ACTION_TYPES:
        decision = evaluate_negative_runtime_request(create_negative_runtime_request(action_type)).decision
        assert decision.runtime_authority_granted is False


def test_v0403_decision_never_grants_model_prompt_subagent_or_live_authority() -> None:
    decision = evaluate_negative_runtime_request(create_negative_runtime_request("model_provider_invocation")).decision

    assert decision.live_workspace_authority_granted is False
    assert decision.model_invocation_authority_granted is False
    assert decision.prompt_submission_authority_granted is False
    assert decision.subagent_invocation_authority_granted is False
    with pytest.raises(ValueError):
        type(decision)(**{**decision.__dict__, "model_invocation_authority_granted": True})


def test_v0403_evaluation_records_denied_runtime_action_metadata() -> None:
    evaluation = evaluate_negative_runtime_request(create_negative_runtime_request("prompt_submission"))

    assert evaluation.denied_action_metadata_ref is not None
    assert negative_runtime_evaluation_is_metadata_only(evaluation)


def test_v0403_regression_suite_covers_all_required_cases() -> None:
    suite = build_negative_runtime_gate_regression_suite()

    assert negative_runtime_suite_is_complete_and_blocked(suite)
    assert {evaluation.request.requested_action_type for evaluation in suite.evaluations} == set(REQUIRED_NEGATIVE_ACTION_TYPES)


def test_v0403_coverage_matrix_complete_and_all_blocked() -> None:
    matrix = build_denied_runtime_action_coverage_matrix()

    assert denied_runtime_coverage_matrix_is_complete(matrix)
    assert matrix.unsafe_gap_count == 0


def test_v0403_false_standalone_runtime_claim_audit_blocks_claim() -> None:
    audit = audit_standalone_runtime_false_claims()

    assert audit.standalone_runtime_claim_detected is True
    assert audit.claim_allowed is False
    assert audit.chat_service_opened is False
    assert audit.agent_loop_opened is False
    assert audit.user_facing_cli_opened is False


def test_v0403_false_production_certification_audit_blocks_claim() -> None:
    audit = audit_production_certification_false_claims()

    assert audit.production_certification_claim_detected is True
    assert audit.claim_allowed is False
    assert audit.production_certified is False


def test_v0403_false_claim_detection_blocks_release_claim() -> None:
    claim = RuntimeFalseClaimRequest(
        claim_id="claim-standalone",
        claim_kind=RuntimeFalseClaimKind.STANDALONE_DEFAULT_PERSONAL_RUNTIME_READY.value,
        claim_text="Default Personal standalone runtime is ready.",
        source="test_fixture",
        evidence_refs=("v0403",),
    )
    detection = detect_runtime_false_claim(claim)

    assert detection.claim_detected is True
    assert detection.claim_allowed is False
    assert detection.must_block_release_claim is True


def test_v0403_safety_report_blocks_all_unsafe_readiness() -> None:
    report = create_negative_runtime_gate_safety_report()

    assert report.safe_for_v0403_negative_regression is True
    assert report.safe_for_model_invocation is False
    assert report.safe_for_prompt_submission is False
    assert report.safe_for_subagent_invocation is False
    assert report.safe_for_live_apply is False
    assert report.safe_for_autonomous_loop is False
    assert report.safe_for_standalone_default_personal_runtime is False
    assert report.safe_for_dominion_runtime is False
    assert report.production_certified is False


def test_v0403_readiness_report_keeps_unsafe_flags_false() -> None:
    report = create_negative_runtime_gate_readiness_report()

    assert report.negative_runtime_gate_regression_defined is True
    assert report.denied_runtime_action_coverage_ready is True
    assert report.false_standalone_runtime_claim_detection_ready is True
    assert report.false_production_certification_claim_detection_ready is True
    assert report.v0404_handoff_ready is True
    assert negative_runtime_readiness_preserves_no_unsafe_runtime(report)
    with pytest.raises(ValueError):
        create_negative_runtime_gate_readiness_report(ready_for_model_provider_invocation=True)
    with pytest.raises(ValueError):
        create_negative_runtime_gate_readiness_report(production_certified=True)


def test_v0403_v0404_handoff_targets_human_checkpoint_hardening() -> None:
    handoff = create_v0404_human_checkpoint_hardening_handoff()

    assert handoff.target_version == "v0.40.4"
    assert "Human Checkpoint Hardening" in handoff.target_track
    assert "scope_bound_checkpoint_decision" in handoff.recommended_focus
    assert "human_approval_does_not_grant_runtime_authority" in handoff.recommended_focus


def test_v0403_v041_acceleration_signal_is_non_authoritative() -> None:
    signal = create_v041_smoke_run_acceleration_safety_signal()

    assert signal.conservative_target == "v0.41.6"
    assert signal.earliest_candidate_target == "v0.41.6"
    assert signal.recommendation == "keep_conservative_target"
    assert signal.negative_gate_regression_passed is True
    assert v041_acceleration_safety_signal_is_not_runtime_start(signal)


def test_v0403_all_negative_requests_map_to_block_or_stop() -> None:
    suite = build_negative_runtime_gate_regression_suite()

    assert {evaluation.decision.decision_kind for evaluation in suite.evaluations}.issubset({"block", "stop"})


def test_v0403_safe_alternatives_are_from_allowed_set() -> None:
    suite = build_negative_runtime_gate_regression_suite()

    for evaluation in suite.evaluations:
        assert evaluation.decision.safe_alternative in ALLOWED_SAFE_ALTERNATIVES


def test_v0403_false_claims_do_not_modify_readiness_flags() -> None:
    detect_runtime_false_claim(
        RuntimeFalseClaimRequest(
            claim_id="claim-production",
            claim_kind=RuntimeFalseClaimKind.PRODUCTION_CERTIFIED.value,
            claim_text="Production certified.",
            source="test_fixture",
            evidence_refs=("v0403",),
        )
    )
    report = create_negative_runtime_gate_readiness_report()

    assert report.production_certified is False
    assert report.ready_for_standalone_default_personal_runtime is False


def test_v0403_negative_gate_regression_does_not_execute_anything() -> None:
    suite = build_negative_runtime_gate_regression_suite()

    for evaluation in suite.evaluations:
        assert evaluation.metadata_only is True
        assert evaluation.executed is False


def test_v0403_no_forbidden_runtime_call_patterns() -> None:
    implementation = Path("src/chanta_core/agent_runtime/repair_mission_loop_negative_gates.py")
    source = implementation.read_text(encoding="utf-8")
    lower_source = source.lower()
    forbidden_patterns = [
        "import subprocess",
        "subprocess.",
        "os.system",
        "eval(",
        "exec(",
        "import requests",
        "requests.",
        "import httpx",
        "httpx.",
        "import urllib",
        "urllib.",
        "import socket",
        "socket.",
        "import openai",
        "openai.",
        "import anthropic",
        "anthropic.",
        "import ollama",
        "ollama.",
        "import lmstudio",
        "lmstudio.",
        "apply_patch",
        "git apply",
        "git worktree",
    ]

    for pattern in forbidden_patterns:
        assert pattern not in lower_source
    assert re.search(r"(?<!no_)shell\s*=\s*True", source) is None
    assert "sub" + "process." not in lower_source
