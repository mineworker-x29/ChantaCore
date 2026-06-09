from dataclasses import fields
import inspect

import pytest

from chanta_core.agent_runtime import (
    DoNothingAlternativeBoundaryPolicy,
    DoNothingAlternativePosture,
    SandboxTestAllowedSurface,
    SandboxTestCommandBoundaryPolicy,
    SandboxTestCommandPosture,
    SandboxTestDeniedAction,
    SandboxTestExecutionPosture,
    SandboxTestGateEvaluation,
    SandboxTestNoExecutionGuarantee,
    SandboxTestOutputBoundaryPolicy,
    SandboxTestOutputPosture,
    SandboxTestPermissionDecision,
    SandboxTestPermissionRequest,
    SandboxTestProhibitedSurface,
    SandboxTestRunnerBoundary,
    SandboxTestRunnerBoundaryPolicy,
    SandboxTestRunnerCapabilityKind,
    SandboxTestRunnerDecisionKind,
    SandboxTestRunnerFlagSet,
    SandboxTestRunnerReadinessLevel,
    SandboxTestRunnerRiskKind,
    SandboxTestRunnerRiskRegister,
    SandboxTestRunnerSourceKind,
    SandboxTestRunnerSourceRef,
    SandboxTestRunnerStatus,
    SandboxTestRunnerSurfaceKind,
    SandboxTestRunnerTrackKind,
    V0370ReadinessReport,
    V037RoadmapOverview,
    VeraCodexEvaluationBoundaryPolicy,
    VeraCodexEvaluationPosture,
    build_do_nothing_alternative_boundary_policy,
    build_sandbox_test_allowed_surface,
    build_sandbox_test_command_boundary_policy,
    build_sandbox_test_denied_action,
    build_sandbox_test_gate_evaluation,
    build_sandbox_test_no_execution_guarantee,
    build_sandbox_test_output_boundary_policy,
    build_sandbox_test_permission_decision,
    build_sandbox_test_permission_request,
    build_sandbox_test_prohibited_surface,
    build_sandbox_test_runner_boundary,
    build_sandbox_test_runner_boundary_policy,
    build_sandbox_test_runner_flags,
    build_sandbox_test_runner_risk_register,
    build_sandbox_test_runner_source_ref,
    build_v0370_readiness_report,
    build_v037_roadmap_overview,
    build_vera_codex_evaluation_boundary_policy,
    do_nothing_policy_requires_baseline,
    sandbox_test_command_policy_blocks_shell,
    sandbox_test_output_policy_blocks_unbounded_output,
    sandbox_test_permission_decision_is_not_execution,
    sandbox_test_runner_boundary_is_not_execution,
    sandbox_test_runner_flags_preserve_no_execution,
    sandbox_test_runner_policy_blocks_test_execution,
    v0370_readiness_report_is_not_execution_ready,
    vera_codex_evaluation_policy_blocks_trial_execution,
)


SAFE_FLAG_NAMES = {
    "ready_for_v0371_allowlisted_test_command_policy",
    "ready_for_v0372_sandbox_test_execution_engine",
    "ready_for_v0376_vera_codex_one_shot_agent_trial",
    "ready_for_v0377_cold_agent_performance_evaluation",
    "ready_for_sandbox_test_runner_boundary",
    "ready_for_allowlisted_test_policy_boundary",
    "ready_for_test_output_boundary",
    "ready_for_vera_codex_evaluation_boundary",
    "ready_for_do_nothing_alternative_boundary",
}


def _unsafe_flag_names(cls):
    return [field.name for field in fields(cls) if field.name.startswith("ready_for_") and field.name not in SAFE_FLAG_NAMES]


def test_v0370_taxonomies_have_required_values():
    assert {item.value for item in SandboxTestRunnerTrackKind} == {
        "boundary_foundation",
        "allowlisted_test_command_policy",
        "sandbox_test_execution_engine",
        "test_result_envelope",
        "test_feedback_failure_diagnosis",
        "repair_suggestion_metadata",
        "vera_codex_one_shot_agent_trial",
        "cold_agent_performance_evaluation",
        "cli_test_runner_agent_evaluation_surface",
        "consolidation",
        "unknown",
    }
    assert "arbitrary_shell" in {item.value for item in SandboxTestRunnerSurfaceKind}
    assert "run_pytest" in {item.value for item in SandboxTestRunnerCapabilityKind}
    assert "do_nothing_omission_risk" in {item.value for item in SandboxTestRunnerRiskKind}
    assert "allow_boundary_definition" in {item.value for item in SandboxTestRunnerDecisionKind}
    assert "boundary_ready" in {item.value for item in SandboxTestRunnerStatus}
    assert "sandbox_test_runner_boundary_ready" in {item.value for item in SandboxTestRunnerReadinessLevel}
    assert "no_test_command_execution" in {item.value for item in SandboxTestCommandPosture}
    assert "no_test_execution" in {item.value for item in SandboxTestExecutionPosture}
    assert "no_output_capture" in {item.value for item in SandboxTestOutputPosture}
    assert "no_vera_codex_trial_execution" in {item.value for item in VeraCodexEvaluationPosture}
    assert "do_nothing_boundary_defined" in {item.value for item in DoNothingAlternativePosture}
    assert "v0369_handoff_packet" in {item.value for item in SandboxTestRunnerSourceKind}


def test_required_models_are_exported():
    for model in (
        SandboxTestRunnerFlagSet,
        SandboxTestRunnerSourceRef,
        SandboxTestRunnerBoundaryPolicy,
        SandboxTestCommandBoundaryPolicy,
        SandboxTestOutputBoundaryPolicy,
        VeraCodexEvaluationBoundaryPolicy,
        DoNothingAlternativeBoundaryPolicy,
        SandboxTestAllowedSurface,
        SandboxTestProhibitedSurface,
        SandboxTestRunnerBoundary,
        SandboxTestPermissionRequest,
        SandboxTestPermissionDecision,
        SandboxTestDeniedAction,
        SandboxTestGateEvaluation,
        SandboxTestRunnerRiskRegister,
        SandboxTestNoExecutionGuarantee,
        V037RoadmapOverview,
        V0370ReadinessReport,
    ):
        assert model is not None


def test_flags_allow_boundary_readiness_and_preserve_no_execution():
    flags = build_sandbox_test_runner_flags()
    assert flags.sandbox_test_runner_boundary_constructed
    assert flags.sandbox_test_runner_policy_defined
    assert flags.allowlisted_test_policy_boundary_defined
    assert flags.test_output_boundary_defined
    assert flags.vera_codex_evaluation_boundary_defined
    assert flags.do_nothing_alternative_boundary_defined
    assert flags.sandbox_test_runner_risk_register_defined
    assert flags.ready_for_v0371_allowlisted_test_command_policy
    assert flags.ready_for_v0372_sandbox_test_execution_engine
    assert flags.ready_for_v0376_vera_codex_one_shot_agent_trial
    assert flags.ready_for_v0377_cold_agent_performance_evaluation
    assert flags.ready_for_sandbox_test_runner_boundary
    assert flags.ready_for_allowlisted_test_policy_boundary
    assert flags.ready_for_test_output_boundary
    assert flags.ready_for_vera_codex_evaluation_boundary
    assert flags.ready_for_do_nothing_alternative_boundary
    assert sandbox_test_runner_flags_preserve_no_execution(flags)
    for name in _unsafe_flag_names(SandboxTestRunnerFlagSet) + ["production_certified"]:
        assert getattr(flags, name) is False


@pytest.mark.parametrize(
    "field_name",
    _unsafe_flag_names(SandboxTestRunnerFlagSet) + ["production_certified"],
)
def test_flags_reject_unsafe_true(field_name):
    with pytest.raises(ValueError):
        build_sandbox_test_runner_flags(**{field_name: True})


def test_source_ref_is_not_execution():
    source = build_sandbox_test_runner_source_ref()
    assert source.source_kind == SandboxTestRunnerSourceKind.V0369_HANDOFF_PACKET
    assert source.evidence_refs


def test_runner_boundary_policy_allows_future_gates_but_blocks_execution():
    policy = build_sandbox_test_runner_boundary_policy()
    assert policy.allow_boundary_definition
    assert policy.allow_allowlisted_policy_future_gate
    assert policy.allow_controlled_test_subprocess_future_gate
    assert policy.allow_bounded_output_future_gate
    assert policy.allow_vera_codex_evaluation_future_gate
    assert policy.allow_do_nothing_comparison_future_gate
    assert sandbox_test_runner_policy_blocks_test_execution(policy)
    for name in (
        "allow_test_execution",
        "allow_controlled_test_subprocess",
        "allow_pytest_execution",
        "allow_npm_test_execution",
        "allow_unittest_execution",
        "allow_shell",
        "allow_arbitrary_command",
        "allow_dependency_install",
        "allow_network_access",
        "allow_live_workspace_write",
        "allow_patch_application",
        "allow_automatic_repair",
        "allow_multi_cycle_loop",
        "allow_vera_codex_trial_execution",
        "allow_external_agent_execution",
        "allow_dominion_runtime",
    ):
        assert getattr(policy, name) is False
        with pytest.raises(ValueError):
            build_sandbox_test_runner_boundary_policy(**{name: True})


def test_command_output_vera_and_do_nothing_policies():
    command = build_sandbox_test_command_boundary_policy()
    output = build_sandbox_test_output_boundary_policy()
    vera = build_vera_codex_evaluation_boundary_policy()
    do_nothing = build_do_nothing_alternative_boundary_policy()
    assert command.require_allowlist
    assert command.require_no_shell
    assert command.require_sandbox_cwd
    assert command.require_timeout
    assert command.require_no_network
    assert command.reject_dependency_install
    assert sandbox_test_command_policy_blocks_shell(command)
    assert output.require_redaction
    assert output.block_raw_secret_output
    assert output.block_unbounded_output
    assert sandbox_test_output_policy_blocks_unbounded_output(output)
    assert vera.require_test_result_evidence
    assert vera.require_validation_report_evidence
    assert vera.require_do_nothing_comparison
    assert vera.require_human_handoff
    assert vera_codex_evaluation_policy_blocks_trial_execution(vera)
    assert do_nothing.require_do_nothing_baseline
    assert do_nothing.require_before_after_comparison
    assert do_nothing.require_risk_delta_comparison
    assert do_nothing.require_test_delta_comparison
    assert do_nothing_policy_requires_baseline(do_nothing)
    with pytest.raises(ValueError):
        build_sandbox_test_command_boundary_policy(allow_arbitrary_shell=True)
    with pytest.raises(ValueError):
        build_sandbox_test_output_boundary_policy(allow_output_capture=True)
    with pytest.raises(ValueError):
        build_vera_codex_evaluation_boundary_policy(allow_model_provider_invocation=True)
    with pytest.raises(ValueError):
        build_do_nothing_alternative_boundary_policy(allow_scoring_execution=True)


def test_allowed_and_prohibited_surfaces():
    allowed = build_sandbox_test_allowed_surface()
    assert allowed.allowed_only_for_design_stage
    assert allowed.executable_in_v0370 is False
    assert allowed.runs_tests is False
    assert allowed.runs_shell is False
    assert allowed.installs_dependency is False
    assert allowed.accesses_network is False
    assert allowed.invokes_model is False
    assert allowed.invokes_external_agent is False
    with pytest.raises(ValueError):
        build_sandbox_test_allowed_surface(runs_tests=True)
    prohibited = build_sandbox_test_prohibited_surface()
    assert prohibited.blocks_test_execution
    assert prohibited.blocks_runtime_readiness
    assert "shell_execution" in prohibited.prohibited_runtime_actions


def test_boundary_is_not_test_execution():
    boundary = build_sandbox_test_runner_boundary()
    assert sandbox_test_runner_boundary_is_not_execution(boundary)
    assert boundary.ready_for_v0371_allowlisted_test_command_policy
    assert boundary.ready_for_v0372_sandbox_test_execution_engine
    assert boundary.ready_for_v0376_vera_codex_one_shot_agent_trial
    assert boundary.ready_for_v0377_cold_agent_performance_evaluation
    assert boundary.ready_for_test_execution is False
    assert boundary.ready_for_controlled_test_subprocess is False
    assert boundary.ready_for_shell_execution is False
    assert boundary.ready_for_dependency_install is False
    assert boundary.ready_for_network_access is False
    assert boundary.ready_for_vera_codex_trial_execution is False
    with pytest.raises(ValueError):
        build_sandbox_test_runner_boundary(ready_for_test_execution=True)


def test_permission_decision_denies_runtime_execution():
    request = build_sandbox_test_permission_request()
    decision = build_sandbox_test_permission_decision(request_id=request.request_id)
    denied = build_sandbox_test_denied_action()
    gate = build_sandbox_test_gate_evaluation(request=request, decision=decision, denied_action=denied)
    assert sandbox_test_permission_decision_is_not_execution(decision)
    assert gate.ready_for_execution is False
    for name in (
        "test_execution_allowed",
        "controlled_test_subprocess_allowed",
        "shell_execution_allowed",
        "subprocess_allowed",
        "command_execution_allowed",
        "dependency_install_allowed",
        "network_access_allowed",
        "automatic_repair_allowed",
        "vera_codex_trial_execution_allowed",
        "external_agent_execution_allowed",
        "dominion_runtime_allowed",
    ):
        assert getattr(decision, name) is False
        with pytest.raises(ValueError):
            build_sandbox_test_permission_decision(**{name: True})


def test_risk_register_no_execution_guarantee_roadmap_and_readiness():
    risk = build_sandbox_test_runner_risk_register()
    guarantee = build_sandbox_test_no_execution_guarantee()
    roadmap = build_v037_roadmap_overview()
    report = build_v0370_readiness_report()
    required_risks = {
        SandboxTestRunnerRiskKind.ARBITRARY_SHELL_RISK,
        SandboxTestRunnerRiskKind.UNCONTROLLED_SUBPROCESS_RISK,
        SandboxTestRunnerRiskKind.DEPENDENCY_INSTALL_RISK,
        SandboxTestRunnerRiskKind.NETWORK_ACCESS_RISK,
        SandboxTestRunnerRiskKind.UNBOUNDED_OUTPUT_RISK,
        SandboxTestRunnerRiskKind.FAILED_TEST_MISREPORTED_AS_SUCCESS_RISK,
        SandboxTestRunnerRiskKind.AUTOMATIC_REPAIR_RISK,
        SandboxTestRunnerRiskKind.MULTI_CYCLE_LOOP_RISK,
        SandboxTestRunnerRiskKind.MODEL_SELF_PRAISE_RISK,
        SandboxTestRunnerRiskKind.DO_NOTHING_OMISSION_RISK,
        SandboxTestRunnerRiskKind.EXTERNAL_AGENT_EXECUTION_RISK,
        SandboxTestRunnerRiskKind.DOMINION_RUNTIME_RISK,
    }
    assert required_risks.issubset({SandboxTestRunnerRiskKind(item) for item in risk.risk_kinds})
    for field in fields(SandboxTestNoExecutionGuarantee):
        if field.name.startswith("no_"):
            assert getattr(guarantee, field.name) is True
    assert "v0.37.1 allowlisted test command policy" in roadmap.roadmap_items
    assert report.ready_for_v0371_allowlisted_test_command_policy
    assert report.ready_for_v0372_sandbox_test_execution_engine
    assert report.ready_for_v0376_vera_codex_one_shot_agent_trial
    assert report.ready_for_v0377_cold_agent_performance_evaluation
    assert v0370_readiness_report_is_not_execution_ready(report)
    for name in (
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
        "ready_for_cold_agent_performance_evaluation",
        "ready_for_external_agent_execution",
        "ready_for_dominion_runtime",
        "production_certified",
    ):
        assert getattr(report, name) is False
        with pytest.raises(ValueError):
            build_v0370_readiness_report(**{name: True})


def test_helpers_do_not_contain_runtime_execution_patterns():
    import chanta_core.agent_runtime.sandbox_test_boundary as module

    source = inspect.getsource(module)
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
    ]
    for pattern in forbidden:
        assert pattern not in source
