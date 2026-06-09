from __future__ import annotations

from dataclasses import fields
import inspect

import pytest

import chanta_core.agent_runtime.sandbox_test_cli_surface as cli_module
from chanta_core.agent_runtime import (
    CLITestRunnerCommandKind,
    CLITestRunnerCommandMode,
    CLITestRunnerDecisionKind,
    CLITestRunnerInputSourceKind,
    CLITestRunnerOutputFormat,
    CLITestRunnerReadinessLevel,
    CLITestRunnerRiskKind,
    CLITestRunnerSurfaceStatus,
    build_cli_test_runner_argument_spec,
    build_cli_test_runner_command_result,
    build_cli_test_runner_command_spec,
    build_cli_test_runner_flags,
    build_cli_test_runner_invocation_decision,
    build_cli_test_runner_no_unsafe_side_effect_guarantee,
    build_cli_test_runner_run_output,
    build_cli_test_runner_run_preview,
    build_cli_test_runner_run_report,
    build_cli_test_runner_runtime_context,
    build_cli_test_runner_source_ref,
    build_cli_test_runner_surface,
    build_cli_test_runner_surface_policy,
    build_default_cli_test_runner_surface,
    build_v0378_readiness_report,
    cli_test_runner_decision_blocks_external_agent,
    cli_test_runner_decision_blocks_shell_and_live_runtime,
    cli_test_runner_flags_preserve_unsafe_false,
    cli_test_runner_invocation_is_not_shell,
    cli_test_runner_surface_is_not_shell,
    default_cli_test_runner_command_specs,
    default_cli_test_runner_surface_policy,
    evaluate_cli_test_runner_invocation,
    parse_cli_test_runner_invocation,
    render_cli_test_runner_output,
    run_cli_test_runner_command,
    v0378_readiness_report_is_not_execution_ready,
)


SAFE_FLAG_NAMES = (
    "ready_for_v0379_controlled_sandbox_test_runner_consolidation",
    "ready_for_cli_test_runner_surface",
    "ready_for_cli_test_invocation_preview",
    "ready_for_cli_sandbox_test_run",
    "ready_for_cli_test_result_summary",
    "ready_for_cli_feedback_report",
    "ready_for_cli_repair_suggestion_preview",
    "ready_for_cli_vera_trial_preview",
    "ready_for_cli_vera_trial_run_once",
    "ready_for_cli_cold_scorecard",
    "ready_for_cli_evaluation_bundle_preview",
    "ready_for_cli_controlled_test_execution_dispatch",
)

UNSAFE_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_uncontrolled_subprocess",
    "ready_for_command_execution",
    "ready_for_dependency_install",
    "ready_for_network_access",
    "ready_for_live_workspace_write",
    "ready_for_patch_application",
    "ready_for_apply_patch",
    "ready_for_git_apply",
    "ready_for_repair_patch_proposal",
    "ready_for_automatic_repair",
    "ready_for_model_provider_invocation",
    "ready_for_tool_execution",
    "ready_for_external_agent_execution",
    "ready_for_claude_code_invocation",
    "ready_for_codex_cli_invocation",
    "ready_for_dominion_runtime",
    "ready_for_persistent_trace_write",
)

UNSAFE_POLICY_NAMES = (
    "allow_direct_subprocess",
    "allow_shell",
    "allow_arbitrary_command",
    "allow_dependency_install",
    "allow_network_access",
    "allow_live_workspace_write",
    "allow_patch_application",
    "allow_code_edit",
    "allow_apply_patch",
    "allow_git_apply",
    "allow_repair_patch_proposal",
    "allow_repair_execution",
    "allow_automatic_repair",
    "allow_model_provider_invocation",
    "allow_tool_execution",
    "allow_external_agent_execution",
    "allow_claude_code_invocation",
    "allow_codex_cli_invocation",
    "allow_dominion_runtime",
    "allow_persistent_trace_write",
    "allow_ui_runtime",
)


def _values(enum_cls):
    return [item.value for item in enum_cls]


def test_v0378_enum_values_are_complete():
    assert _values(CLITestRunnerCommandKind) == [
        "test_run_help",
        "test_run_status",
        "test_invocation_preview",
        "test_run_sandbox",
        "test_result_summary",
        "feedback_report",
        "repair_suggestion_preview",
        "vera_trial_preview",
        "vera_trial_run_once",
        "cold_scorecard",
        "evaluation_bundle_preview",
        "denied_shell",
        "denied_direct_pytest",
        "denied_direct_unittest",
        "denied_package_script",
        "denied_dependency_install",
        "denied_network_command",
        "denied_live_workspace_command",
        "denied_apply_patch",
        "denied_git_apply",
        "denied_repair_execution",
        "denied_external_agent",
        "denied_model_provider",
        "denied_dominion",
        "denied_multi_cycle",
        "no_op",
        "unknown",
    ]
    assert "sandbox_test_run" in _values(CLITestRunnerCommandMode)
    assert "runtime_context" in _values(CLITestRunnerInputSourceKind)
    assert "completed_with_warnings" in _values(CLITestRunnerSurfaceStatus)
    assert "allow_vera_trial_run_once" in _values(CLITestRunnerDecisionKind)
    assert "structured_artifact" in _values(CLITestRunnerOutputFormat)
    assert "codex_cli_invocation_risk" in _values(CLITestRunnerRiskKind)
    assert "bounded_agent_evaluation_dispatch_ready" in _values(CLITestRunnerReadinessLevel)


def test_flags_policy_surface_and_specs_preserve_runtime_false():
    flags = build_cli_test_runner_flags()
    for name in SAFE_FLAG_NAMES:
        assert getattr(flags, name) is True
    for name in UNSAFE_FLAG_NAMES:
        assert getattr(flags, name) is False
        with pytest.raises(ValueError):
            build_cli_test_runner_flags(**{name: True})
    assert cli_test_runner_flags_preserve_unsafe_false(flags)

    policy = default_cli_test_runner_surface_policy()
    assert policy.allow_help is True
    assert policy.allow_sandbox_test_run is True
    assert policy.allow_controlled_test_execution_dispatch is True
    assert "pytest" in policy.prohibited_arg_patterns
    for name in UNSAFE_POLICY_NAMES:
        assert getattr(policy, name) is False
        with pytest.raises(ValueError):
            build_cli_test_runner_surface_policy(**{name: True})

    source = build_cli_test_runner_source_ref()
    assert source.source_kind == CLITestRunnerInputSourceKind.ARGV_LIST
    arg = build_cli_test_runner_argument_spec(max_value_chars=20)
    assert arg.max_value_chars == 20
    assert "apply_patch" in arg.prohibited_patterns
    command = build_cli_test_runner_command_spec(argument_specs=[arg])
    assert command.dispatch_target is None
    specs = default_cli_test_runner_command_specs()
    assert any(spec.command_name == "test-run-sandbox" for spec in specs)
    assert any(spec.command_name == "run-codex" for spec in specs)

    surface = build_default_cli_test_runner_surface()
    assert cli_test_runner_surface_is_not_shell(surface)
    assert surface.ready_for_execution is False
    assert len(surface.command_specs) >= 20


def test_runtime_context_invocation_decision_result_report_models_are_bounded():
    context = build_cli_test_runner_runtime_context(
        has_invocation_contract=True,
        sandbox_root_ref="sandbox-root:fixture",
        allows_controlled_test_execution_dispatch=True,
        has_test_result_envelope=True,
        allows_result_summary=True,
    )
    assert context.allows_direct_subprocess is False
    with pytest.raises(ValueError):
        build_cli_test_runner_runtime_context(allows_shell=True)
    with pytest.raises(ValueError):
        build_cli_test_runner_runtime_context(allows_controlled_test_execution_dispatch=True)

    decision = build_cli_test_runner_invocation_decision()
    assert cli_test_runner_decision_blocks_shell_and_live_runtime(decision)
    assert cli_test_runner_decision_blocks_external_agent(decision)
    for field in fields(decision):
        if field.name.endswith("_allowed") and field.name not in {"bounded_preview_allowed"}:
            assert getattr(decision, field.name) is False
    with pytest.raises(ValueError):
        build_cli_test_runner_invocation_decision(shell_execution_allowed=True)

    result = build_cli_test_runner_command_result()
    assert result.ready_for_execution is False
    assert result.direct_subprocess_used is False
    with pytest.raises(ValueError):
        build_cli_test_runner_command_result(model_invocation_performed=True)

    output = build_cli_test_runner_run_output()
    assert output.ready_for_execution is False
    report = build_cli_test_runner_run_report(run_output=output)
    assert report.ready_for_execution is False
    preview = build_cli_test_runner_run_preview()
    assert preview.will_use_shell is False
    guarantee = build_cli_test_runner_no_unsafe_side_effect_guarantee()
    assert guarantee.no_shell_execution is True
    assert guarantee.no_controlled_test_dispatch is True

    readiness = build_v0378_readiness_report()
    assert v0378_readiness_report_is_not_execution_ready(readiness)
    for name in UNSAFE_FLAG_NAMES:
        assert getattr(readiness, name) is False


@pytest.mark.parametrize(
    ("argv", "kind"),
    [
        (["test-run-help"], CLITestRunnerCommandKind.TEST_RUN_HELP),
        (["test-run-status"], CLITestRunnerCommandKind.TEST_RUN_STATUS),
        (["test-invocation-preview", "--format", "json"], CLITestRunnerCommandKind.TEST_INVOCATION_PREVIEW),
        (["test-run-sandbox", "--contract", "contract:1"], CLITestRunnerCommandKind.TEST_RUN_SANDBOX),
        (["test-result-summary"], CLITestRunnerCommandKind.TEST_RESULT_SUMMARY),
        (["feedback-report"], CLITestRunnerCommandKind.FEEDBACK_REPORT),
        (["repair-suggestion-preview"], CLITestRunnerCommandKind.REPAIR_SUGGESTION_PREVIEW),
        (["vera-trial-preview"], CLITestRunnerCommandKind.VERA_TRIAL_PREVIEW),
        (["vera-trial-run-once"], CLITestRunnerCommandKind.VERA_TRIAL_RUN_ONCE),
        (["cold-scorecard"], CLITestRunnerCommandKind.COLD_SCORECARD),
        (["evaluation-bundle-preview"], CLITestRunnerCommandKind.EVALUATION_BUNDLE_PREVIEW),
        (["no-op"], CLITestRunnerCommandKind.NO_OP),
        ([], CLITestRunnerCommandKind.NO_OP),
    ],
)
def test_parse_safe_commands(argv, kind):
    invocation = parse_cli_test_runner_invocation(argv)
    assert invocation.command_kind == kind
    assert cli_test_runner_invocation_is_not_shell(invocation)
    assert invocation.metadata["argv_not_passed_to_subprocess"] is True


@pytest.mark.parametrize(
    "argv",
    [
        ["unknown-command"],
        ["shell"],
        ["bash"],
        ["powershell"],
        ["cmd"],
        ["python"],
        ["pytest"],
        ["unittest"],
        ["npm"],
        ["pip"],
        ["install"],
        ["curl"],
        ["wget"],
        ["git"],
        ["git-apply"],
        ["apply_patch"],
        ["apply-patch"],
        ["live-write"],
        ["edit-live"],
        ["workspace-write"],
        ["repair"],
        ["auto-repair"],
        ["retry-loop"],
        ["multi-cycle"],
        ["run-opencode"],
        ["run-hermes"],
        ["run-openclaw"],
        ["run-claude-code"],
        ["run-codex"],
        ["provider-call"],
        ["dominion"],
        ["external-agent-loop"],
        ["infinite-loop"],
        ["recursive-agent"],
        ["test-run-help", ";", "pytest"],
    ],
)
def test_unknown_and_unsafe_commands_are_denied(argv):
    surface = build_default_cli_test_runner_surface()
    invocation = parse_cli_test_runner_invocation(argv, surface)
    decision = evaluate_cli_test_runner_invocation(invocation, surface)
    assert decision.allowed_command_kind is None
    assert cli_test_runner_decision_blocks_shell_and_live_runtime(decision)
    output = run_cli_test_runner_command(invocation, surface)
    assert output.denied_command is not None
    assert output.command_result is None
    assert output.ready_for_execution is False


def test_evaluate_allows_safe_preview_but_not_runtime_permission():
    surface = build_default_cli_test_runner_surface()
    invocation = parse_cli_test_runner_invocation(["test-invocation-preview", "--target", "contract:1"], surface)
    decision = evaluate_cli_test_runner_invocation(invocation, surface)
    assert decision.bounded_preview_allowed is True
    assert decision.command_execution_allowed is False
    assert decision.shell_execution_allowed is False

    output = run_cli_test_runner_command(invocation, surface)
    assert output.command_result is not None
    assert output.command_result.ready_for_execution is False
    assert output.command_result.structured_result["argv_not_passed_to_shell"] is True
    assert "preview" in output.command_result.text_summary


def test_test_run_sandbox_requires_v0372_boundary_context():
    surface = build_default_cli_test_runner_surface()
    invocation = parse_cli_test_runner_invocation(["test-run-sandbox", "--contract", "contract:1"], surface)
    denied = evaluate_cli_test_runner_invocation(invocation, surface)
    assert denied.controlled_test_execution_dispatch_allowed is False

    context = build_cli_test_runner_runtime_context(
        has_invocation_contract=True,
        sandbox_root_ref="sandbox-root:fixture",
        allows_controlled_test_execution_dispatch=True,
        metadata={"invocation_contract_ref": "contract:1"},
    )
    decision = evaluate_cli_test_runner_invocation(invocation, surface, context)
    assert decision.controlled_test_execution_dispatch_allowed is True
    assert decision.direct_subprocess_allowed is False

    output = run_cli_test_runner_command(invocation, surface, context)
    assert output.command_result is not None
    assert output.command_result.controlled_test_execution_dispatched is True
    assert output.command_result.direct_subprocess_used is False
    assert output.command_result.shell_used is False
    assert output.command_result.structured_result["direct_subprocess_used_by_v0378"] is False
    guarantee = build_cli_test_runner_no_unsafe_side_effect_guarantee(no_controlled_test_dispatch=False)
    assert guarantee.no_controlled_test_dispatch is False


@pytest.mark.parametrize(
    ("argv", "expected_key"),
    [
        (["test-result-summary"], "summary_source"),
        (["feedback-report"], "summary_source"),
        (["repair-suggestion-preview"], "patch_generated"),
        (["vera-trial-preview"], "trial_count"),
        (["vera-trial-run-once"], "trial_packet_id"),
        (["cold-scorecard"], "cold_evaluation_report_id"),
        (["evaluation-bundle-preview"], "has_vera_trial_packet"),
    ],
)
def test_safe_dispatch_commands_return_bounded_metadata(argv, expected_key):
    surface = build_default_cli_test_runner_surface()
    context = build_cli_test_runner_runtime_context(
        has_test_result_envelope=True,
        has_feedback_report=True,
        has_repair_suggestion=True,
        has_vera_trial_packet=True,
        has_cold_evaluation_report=True,
        allows_result_summary=True,
        allows_feedback_report=True,
        allows_repair_suggestion_preview=True,
        allows_vera_trial_run_once=True,
        allows_cold_scorecard=True,
    )
    invocation = parse_cli_test_runner_invocation(argv, surface)
    output = run_cli_test_runner_command(invocation, surface, context)
    assert output.command_result is not None
    assert expected_key in output.command_result.structured_result
    assert output.command_result.repair_performed is False
    assert output.command_result.model_invocation_performed is False
    assert output.command_result.production_certified is False
    if argv[0] == "repair-suggestion-preview":
        assert output.command_result.structured_result["patch_generated"] is False
        assert output.command_result.structured_result["diff_generated"] is False
        assert output.command_result.structured_result["hunk_generated"] is False
    if argv[0] == "cold-scorecard":
        assert output.command_result.structured_result["production_certified"] is False


def test_output_rendering_is_in_memory_and_bounded():
    result = build_cli_test_runner_command_result(text_summary="short result")
    assert "short result" in render_cli_test_runner_output(result, CLITestRunnerOutputFormat.TEXT)
    assert "status" in render_cli_test_runner_output(result, CLITestRunnerOutputFormat.JSON)
    assert "**CLI Output**" in render_cli_test_runner_output(result, CLITestRunnerOutputFormat.MARKDOWN)


def test_static_module_does_not_use_forbidden_runtime_calls():
    source = inspect.getsource(cli_module)
    forbidden_patterns = (
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "requests.",
        "httpx.",
        "urllib.",
        "aiohttp.",
        "socket.",
        ".write_text(",
        ".write_bytes(",
        "eval(",
        "exec(",
    )
    for pattern in forbidden_patterns:
        assert pattern not in source
    assert "run_vera_codex_one_shot_trial" in source
    assert "create_cold_agent_evaluation_report" in source

