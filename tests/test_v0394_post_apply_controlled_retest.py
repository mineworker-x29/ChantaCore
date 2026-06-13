from __future__ import annotations

import pytest

from chanta_core.agent_runtime.repair_post_apply_retest import (
    RepairControlledTestCommandSpec,
    RepairControlledTestRunnerInvocation,
    RepairPostApplyRetestControlledOnlyGuarantee,
    RepairPostApplyRetestDecision,
    RepairPostApplyRetestDecisionKind,
    RepairPostApplyRetestDisposition,
    RepairPostApplyRetestFlagSet,
    RepairPostApplyRetestInput,
    RepairPostApplyRetestMode,
    RepairPostApplyRetestPolicy,
    RepairPostApplyRetestReadinessLevel,
    RepairPostApplyRetestResult,
    RepairPostApplyRetestRiskKind,
    RepairPostApplyRetestRunRecord,
    RepairPostApplyRetestSourceKind,
    RepairPostApplyRetestStatus,
    RepairPostApplyTestCommandKind,
    RepairPostApplyTestOutputCapture,
    RepairPostApplyTestOutcomeKind,
    RepairPostApplyTestScopeKind,
    V0394ReadinessReport,
    audit_post_apply_controlled_retest,
    build_repair_controlled_test_command_spec,
    build_repair_controlled_test_runner_invocation,
    build_repair_post_apply_retest_controlled_only_guarantee,
    build_repair_post_apply_retest_flags,
    build_repair_post_apply_retest_input,
    build_repair_post_apply_retest_policy,
    build_repair_post_apply_retest_result,
    build_repair_post_apply_retest_run_record,
    build_repair_post_apply_test_output_capture,
    build_repair_post_apply_test_selection_plan,
    build_v0394_readiness_report,
    capture_repair_post_apply_test_output,
    create_repair_controlled_runner_invocation,
    create_repair_controlled_test_command_spec,
    create_repair_post_apply_test_selection_plan,
    default_repair_post_apply_retest_policy,
    repair_controlled_runner_invocation_is_not_raw_subprocess,
    repair_controlled_test_command_spec_is_shell_free,
    repair_post_apply_retest_flags_preserve_no_arbitrary_execution,
    repair_post_apply_retest_policy_blocks_arbitrary_runtime,
    repair_post_apply_retest_result_is_not_repair_correctness_proof,
    run_post_apply_controlled_retest,
    v0394_readiness_report_is_not_general_execution_ready,
)


def test_v0394_enum_values() -> None:
    assert [item.value for item in RepairPostApplyRetestMode] == [
        "post_apply_controlled_retest",
        "controlled_test_selection",
        "controlled_test_command_spec",
        "controlled_runner_invocation",
        "bounded_test_output_capture",
        "post_apply_test_result_envelope",
        "post_apply_retest_audit",
        "future_before_after_comparison_input",
        "blocked",
        "no_op",
        "unknown",
    ]
    assert [item.value for item in RepairPostApplyRetestSourceKind] == [
        "v0393_sandbox_apply_result",
        "v0393_sandbox_apply_transaction",
        "v0393_sandbox_apply_audit",
        "v0393_readiness_report",
        "v0392_workspace_descriptor",
        "v0392_workspace_isolation_decision",
        "v0392_live_boundary_check",
        "v0391_approval_artifact_decision",
        "v0391_approval_process_state_gate",
        "v0379_controlled_sandbox_test_runner",
        "v0373_sandbox_test_result_envelope",
        "v0374_sandbox_test_feedback_report",
        "supplied_test_command_spec",
        "supplied_test_runner_adapter",
        "test_fixture",
        "unknown",
    ]
    assert "controlled_retest_completed" in {item.value for item in RepairPostApplyRetestStatus}
    assert "future_before_after_comparison_input_ready" in {item.value for item in RepairPostApplyRetestReadinessLevel}
    assert "reject_shell_command" in {item.value for item in RepairPostApplyRetestDecisionKind}
    assert "arbitrary_command_execution_risk" in {item.value for item in RepairPostApplyRetestRiskKind}
    assert "bounded_pytest_selection" in {item.value for item in RepairPostApplyTestCommandKind}
    assert "unbounded_scope_rejected" in {item.value for item in RepairPostApplyTestScopeKind}
    assert [item.value for item in RepairPostApplyTestOutcomeKind] == [
        "passed",
        "failed",
        "error",
        "timed_out",
        "skipped",
        "blocked",
        "runner_unavailable",
        "inconclusive",
        "no_op",
        "unknown",
    ]
    assert "retest_completed" in {item.value for item in RepairPostApplyRetestDisposition}


def test_flags_allow_controlled_retest_only() -> None:
    flags = build_repair_post_apply_retest_flags()

    assert isinstance(flags, RepairPostApplyRetestFlagSet)
    assert flags.ready_for_post_apply_controlled_retest is True
    assert flags.ready_for_controlled_runner_invocation is True
    assert flags.ready_for_controlled_retest_execution is True
    assert flags.ready_for_controlled_test_subprocess is True
    assert flags.ready_for_bounded_test_output_capture is True
    assert flags.ready_for_future_before_after_comparison_input is True
    assert repair_post_apply_retest_flags_preserve_no_arbitrary_execution(flags)

    assert flags.ready_for_execution is False
    assert flags.ready_for_arbitrary_command_execution is False
    assert flags.ready_for_unbounded_test_execution is False
    assert flags.ready_for_shell_execution is False
    assert flags.ready_for_subprocess_execution is False
    assert flags.ready_for_command_execution is False
    assert flags.ready_for_dependency_install is False
    assert flags.ready_for_network_access is False
    assert flags.ready_for_patch_application is False
    assert flags.ready_for_apply_patch is False
    assert flags.ready_for_git_apply is False
    assert flags.ready_for_before_after_repair_comparison is False
    assert flags.ready_for_repair_execution is False
    assert flags.production_certified is False


@pytest.mark.parametrize(
    "field_name",
    [
        "ready_for_execution",
        "ready_for_arbitrary_command_execution",
        "ready_for_unbounded_test_execution",
        "ready_for_shell_execution",
        "ready_for_subprocess_execution",
        "ready_for_command_execution",
        "ready_for_dependency_install",
        "ready_for_network_access",
        "ready_for_live_workspace_read",
        "ready_for_live_workspace_apply",
        "ready_for_patch_application",
        "ready_for_apply_patch",
        "ready_for_git_apply",
        "ready_for_before_after_repair_comparison",
        "ready_for_repair_effectiveness_assessment",
        "ready_for_repair_process_state_projection",
        "ready_for_self_prompt_generation",
        "ready_for_self_prompt_auto_execution",
        "ready_for_agent_to_subagent_prompt_generation",
        "ready_for_subagent_auto_invocation",
        "ready_for_external_agent_execution",
        "ready_for_model_provider_invocation",
        "ready_for_autonomous_loop_runtime",
        "ready_for_retry_loop",
        "ready_for_multi_cycle_loop",
        "ready_for_repair_execution",
        "ready_for_dominion_runtime",
        "production_certified",
    ],
)
def test_flags_reject_unsafe_true(field_name: str) -> None:
    with pytest.raises(ValueError):
        build_repair_post_apply_retest_flags(**{field_name: True})


def test_policy_allows_controlled_boundary_and_blocks_runtime() -> None:
    policy = default_repair_post_apply_retest_policy()

    assert isinstance(policy, RepairPostApplyRetestPolicy)
    assert policy.allow_controlled_test_selection is True
    assert policy.allow_controlled_test_command_spec is True
    assert policy.allow_controlled_runner_invocation is True
    assert policy.allow_controlled_test_subprocess_via_runner is True
    assert policy.allow_bounded_test_output_capture is True
    assert policy.allow_post_apply_test_result_envelope is True
    assert policy.allow_future_before_after_comparison_input is True
    assert policy.require_successful_sandbox_apply_result is True
    assert policy.require_sandbox_apply_audit is True
    assert policy.require_workspace_isolation is True
    assert policy.require_controlled_runner is True
    assert policy.require_shell_false is True
    assert policy.require_timeout is True
    assert policy.require_bounded_output_capture is True
    assert policy.require_sandbox_cwd is True
    assert repair_post_apply_retest_policy_blocks_arbitrary_runtime(policy)

    assert policy.allow_arbitrary_command_execution is False
    assert policy.allow_shell is False
    assert policy.allow_raw_subprocess is False
    assert policy.allow_dependency_install is False
    assert policy.allow_network_access is False
    assert policy.allow_live_workspace_test is False
    assert policy.allow_unbounded_test_scope is False
    assert policy.allow_patch_application is False
    assert policy.allow_apply_patch is False
    assert policy.allow_git_apply is False
    assert policy.allow_before_after_comparison is False
    assert policy.allow_repair_execution is False
    assert policy.allow_dominion_runtime is False


@pytest.mark.parametrize(
    "field_name",
    [
        "allow_arbitrary_command_execution",
        "allow_shell",
        "allow_raw_subprocess",
        "allow_dependency_install",
        "allow_network_access",
        "allow_live_workspace_test",
        "allow_unbounded_test_scope",
        "allow_patch_application",
        "allow_apply_patch",
        "allow_git_apply",
        "allow_before_after_comparison",
        "allow_repair_execution",
        "allow_self_prompt_generation",
        "allow_self_prompt_auto_execution",
        "allow_subagent_auto_invocation",
        "allow_external_agent_execution",
        "allow_model_provider_invocation",
        "allow_dominion_runtime",
    ],
)
def test_policy_rejects_unsafe_allow_true(field_name: str) -> None:
    with pytest.raises(ValueError):
        build_repair_post_apply_retest_policy(**{field_name: True})


def test_retest_input_is_controlled_request_not_arbitrary_command() -> None:
    retest_input = build_repair_post_apply_retest_input()

    assert isinstance(retest_input, RepairPostApplyRetestInput)
    assert retest_input.sandbox_root_ref
    for action in [
        "shell",
        "raw_subprocess",
        "arbitrary_command",
        "install",
        "network",
        "live_workspace_test",
        "patch_apply",
        "apply_patch",
        "git_apply",
        "self_prompt_execution",
        "subagent_invocation",
        "model_provider",
        "external_agent",
        "Dominion",
    ]:
        assert action in retest_input.prohibited_runtime_actions


def test_selection_plan_rejects_unbounded_scope() -> None:
    with pytest.raises(ValueError):
        build_repair_post_apply_test_selection_plan(
            scope_kind=RepairPostApplyTestScopeKind.UNBOUNDED_SCOPE_REJECTED,
            unbounded_scope_requested=True,
            approved_by_policy=True,
        )

    plan = create_repair_post_apply_test_selection_plan(build_repair_post_apply_retest_input())
    assert plan.bounded is True
    assert plan.approved_by_policy is True
    assert plan.unbounded_scope_requested is False


def test_command_spec_is_shell_free_and_runner_bound() -> None:
    selection = create_repair_post_apply_test_selection_plan(build_repair_post_apply_retest_input())
    spec = create_repair_controlled_test_command_spec(selection)

    assert isinstance(spec, RepairControlledTestCommandSpec)
    assert spec.shell is False
    assert spec.uses_runner_adapter is True
    assert spec.install_command is False
    assert spec.network_command is False
    assert spec.arbitrary_command is False
    assert spec.approved_by_policy is True
    assert repair_controlled_test_command_spec_is_shell_free(spec)


@pytest.mark.parametrize(
    "field_name",
    ["shell", "install_command", "network_command", "arbitrary_command"],
)
def test_command_spec_rejects_unsafe_shape(field_name: str) -> None:
    with pytest.raises(ValueError):
        build_repair_controlled_test_command_spec(**{field_name: True})


def test_invocation_runner_unavailable_without_runner() -> None:
    invocation = create_repair_controlled_runner_invocation(
        build_repair_post_apply_retest_input(),
        build_repair_controlled_test_command_spec(),
        runner=None,
    )

    assert isinstance(invocation, RepairControlledTestRunnerInvocation)
    assert invocation.runner_supplied is False
    assert invocation.runner_invoked is False
    assert invocation.raw_subprocess_used_by_v0394 is False
    assert invocation.shell_used is False
    assert invocation.arbitrary_command_executed is False
    assert repair_controlled_runner_invocation_is_not_raw_subprocess(invocation)


def test_invocation_rejects_raw_subprocess_marker() -> None:
    with pytest.raises(ValueError):
        build_repair_controlled_test_runner_invocation(raw_subprocess_used_by_v0394=True)


def test_run_post_apply_controlled_retest_uses_fake_runner_only_when_gates_pass() -> None:
    calls: list[tuple[list[str], str, int, dict[str, str]]] = []

    def fake_runner(argv: list[str], cwd_ref: str, timeout_seconds: int, env_overrides: dict[str, str]) -> dict[str, object]:
        calls.append((argv, cwd_ref, timeout_seconds, env_overrides))
        return {
            "stdout": "1 passed",
            "stderr": "",
            "exit_code": 0,
            "timed_out": False,
            "duration_ms": 12,
        }

    invocation, record, capture, result = run_post_apply_controlled_retest(
        build_repair_post_apply_retest_input(),
        build_repair_controlled_test_command_spec(),
        runner=fake_runner,
    )

    assert len(calls) == 1
    assert invocation.runner_invoked is True
    assert record.controlled_runner_used is True
    assert record.raw_subprocess_used_by_v0394 is False
    assert record.shell_used is False
    assert record.network_used is False
    assert record.install_performed is False
    assert record.patch_applied is False
    assert record.repair_executed is False
    assert capture.stdout_preview == "1 passed"
    assert result.outcome_kind == RepairPostApplyTestOutcomeKind.PASSED
    assert result.ready_for_future_before_after_comparison_input is True
    assert result.tests_run_under_controlled_boundary is True
    assert result.ready_for_execution is False
    assert repair_post_apply_retest_result_is_not_repair_correctness_proof(result)


def test_run_post_apply_controlled_retest_blocks_when_gates_fail() -> None:
    calls = 0

    def fake_runner(argv: list[str], cwd_ref: str, timeout_seconds: int, env_overrides: dict[str, str]) -> dict[str, object]:
        nonlocal calls
        calls += 1
        return {"stdout": "should not run", "stderr": "", "exit_code": 0}

    _, record, _, result = run_post_apply_controlled_retest(
        build_repair_post_apply_retest_input(sandbox_apply_result_id=None),
        build_repair_controlled_test_command_spec(),
        runner=fake_runner,
    )

    assert calls == 0
    assert record.status == RepairPostApplyRetestStatus.CONTROLLED_RETEST_BLOCKED
    assert result.outcome_kind == RepairPostApplyTestOutcomeKind.BLOCKED
    assert result.ready_for_future_before_after_comparison_input is False


def test_run_post_apply_controlled_retest_returns_runner_unavailable_without_runner() -> None:
    _, record, _, result = run_post_apply_controlled_retest(
        build_repair_post_apply_retest_input(),
        build_repair_controlled_test_command_spec(),
        runner=None,
    )

    assert record.runner_unavailable is True
    assert record.controlled_runner_used is False
    assert result.outcome_kind == RepairPostApplyTestOutcomeKind.RUNNER_UNAVAILABLE
    assert result.ready_for_future_before_after_comparison_input is False


def test_output_capture_bounds_and_redacts() -> None:
    invocation = build_repair_controlled_test_runner_invocation()
    policy = default_repair_post_apply_retest_policy(max_stdout_chars=5, max_stderr_chars=4)
    capture = capture_repair_post_apply_test_output(invocation, "abcdef", "vwxyz", policy)

    assert isinstance(capture, RepairPostApplyTestOutputCapture)
    assert capture.stdout_preview == "abcde...[truncated]"
    assert capture.stderr_preview == "vwxy...[truncated]"
    assert capture.stdout_truncated is True
    assert capture.stderr_truncated is True
    assert capture.redacted is True
    assert capture.combined_output_digest is not None


def test_retest_result_outcomes_and_boundaries() -> None:
    for outcome in [
        RepairPostApplyTestOutcomeKind.PASSED,
        RepairPostApplyTestOutcomeKind.FAILED,
        RepairPostApplyTestOutcomeKind.ERROR,
        RepairPostApplyTestOutcomeKind.TIMED_OUT,
    ]:
        result = build_repair_post_apply_retest_result(outcome_kind=outcome)
        assert isinstance(result, RepairPostApplyRetestResult)
        assert result.ready_for_execution is False
        assert result.production_certified is False
        assert result.repair_executed is False
        assert result.self_prompt_generated is False
        assert result.self_prompt_executed is False
        assert result.subagent_invoked is False
        assert result.model_invoked is False
        assert result.external_agent_invoked is False
        assert result.dominion_runtime_invoked is False


@pytest.mark.parametrize(
    "field_name",
    ["repair_executed", "production_certified", "ready_for_execution", "patch_applied"],
)
def test_retest_result_rejects_unsafe_true(field_name: str) -> None:
    with pytest.raises(ValueError):
        build_repair_post_apply_retest_result(**{field_name: True})


def test_audit_confirms_no_unsafe_surfaces() -> None:
    retest_input = build_repair_post_apply_retest_input()
    record = build_repair_post_apply_retest_run_record(controlled_runner_used=True)
    result = build_repair_post_apply_retest_result()
    audit = audit_post_apply_controlled_retest(retest_input, record, result)

    assert audit.controlled_runner_confirmed is True
    assert audit.shell_false_confirmed is True
    assert audit.no_arbitrary_command_confirmed is True
    assert audit.no_dependency_install_confirmed is True
    assert audit.no_network_access_confirmed is True
    assert audit.no_live_workspace_touch_confirmed is True
    assert audit.no_patch_application_confirmed is True
    assert audit.no_apply_patch_confirmed is True
    assert audit.no_git_apply_confirmed is True
    assert audit.no_repair_execution_confirmed is True
    assert audit.no_self_prompt_execution_confirmed is True
    assert audit.no_subagent_invocation_confirmed is True
    assert audit.no_model_invocation_confirmed is True
    assert audit.no_external_agent_confirmed is True
    assert audit.no_dominion_runtime_confirmed is True
    assert audit.no_production_certification_confirmed is True


def test_decision_allows_controlled_runner_only() -> None:
    report = build_v0394_readiness_report()
    decision = report.decision

    assert isinstance(decision, RepairPostApplyRetestDecision)
    assert decision.ready_for_future_before_after_comparison_input is True
    assert decision.controlled_retest_allowed_now is True
    assert decision.controlled_runner_invocation_allowed_now is True
    assert decision.controlled_test_subprocess_allowed_now is True
    assert decision.arbitrary_command_allowed_now is False
    assert decision.shell_allowed_now is False
    assert decision.raw_subprocess_allowed_now is False
    assert decision.dependency_install_allowed_now is False
    assert decision.network_allowed_now is False
    assert decision.patch_apply_allowed_now is False
    assert decision.before_after_comparison_allowed_now is False
    assert decision.repair_execution_allowed_now is False
    assert decision.self_prompt_generation_allowed_now is False
    assert decision.self_prompt_execution_allowed_now is False
    assert decision.subagent_invocation_allowed_now is False
    assert decision.model_provider_invocation_allowed_now is False
    assert decision.external_agent_allowed_now is False
    assert decision.dominion_runtime_allowed_now is False
    assert decision.production_certified is False


def test_v0394_readiness_report_future_input_only() -> None:
    report = build_v0394_readiness_report()

    assert isinstance(report, V0394ReadinessReport)
    assert report.ready_for_v0395_before_after_repair_outcome_comparison is True
    assert report.ready_for_controlled_test_selection is True
    assert report.ready_for_controlled_test_command_spec is True
    assert report.ready_for_controlled_runner_invocation is True
    assert report.ready_for_controlled_retest_execution is True
    assert report.ready_for_bounded_test_output_capture is True
    assert report.ready_for_post_apply_test_result_envelope is True
    assert report.ready_for_future_before_after_comparison_input is True
    assert report.controlled_runner_invocation_enabled is True
    assert report.controlled_test_subprocess_enabled is True
    assert report.arbitrary_command_enabled is False
    assert report.shell_enabled is False
    assert report.raw_subprocess_enabled is False
    assert report.dependency_install_enabled is False
    assert report.network_enabled is False
    assert report.patch_apply_enabled is False
    assert report.apply_patch_enabled is False
    assert report.git_apply_enabled is False
    assert report.before_after_comparison_enabled is False
    assert report.repair_execution_enabled is False
    assert report.production_certified is False
    assert report.ready_for_execution is False
    assert v0394_readiness_report_is_not_general_execution_ready(report)


@pytest.mark.parametrize(
    "field_name",
    ["before_after_comparison_enabled", "ready_for_execution", "shell_enabled", "raw_subprocess_enabled"],
)
def test_readiness_report_rejects_unsafe_true(field_name: str) -> None:
    with pytest.raises(ValueError):
        build_v0394_readiness_report(**{field_name: True})


def test_controlled_only_guarantee_all_required_no_flags_true() -> None:
    guarantee = build_repair_post_apply_retest_controlled_only_guarantee()

    assert isinstance(guarantee, RepairPostApplyRetestControlledOnlyGuarantee)
    assert guarantee.no_arbitrary_command is True
    assert guarantee.no_shell is True
    assert guarantee.no_raw_subprocess is True
    assert guarantee.no_dependency_install is True
    assert guarantee.no_network_access is True
    assert guarantee.no_live_workspace_touch is True
    assert guarantee.no_patch_application is True
    assert guarantee.no_apply_patch is True
    assert guarantee.no_git_apply is True
    assert guarantee.no_before_after_comparison is True
    assert guarantee.no_repair_execution is True
    assert guarantee.no_self_prompt_execution is True
    assert guarantee.no_subagent_invocation is True
    assert guarantee.no_model_invocation is True
    assert guarantee.no_external_agent is True
    assert guarantee.no_autonomous_loop is True
    assert guarantee.no_retry_loop is True
    assert guarantee.no_multi_cycle_loop is True
    assert guarantee.no_dominion_runtime is True
    assert guarantee.no_production_certification is True


def test_run_record_rejects_unsafe_runtime_markers() -> None:
    for field_name in [
        "raw_subprocess_used_by_v0394",
        "shell_used",
        "network_used",
        "install_performed",
        "patch_applied",
        "repair_executed",
        "self_prompt_executed",
        "subagent_invoked",
        "model_invoked",
        "external_agent_invoked",
        "dominion_runtime_invoked",
    ]:
        with pytest.raises(ValueError):
            build_repair_post_apply_retest_run_record(**{field_name: True})
