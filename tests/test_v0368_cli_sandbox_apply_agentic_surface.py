from dataclasses import fields
import inspect

import pytest

from chanta_core.agent_runtime import (
    CLISandboxApplyArgumentSpec,
    CLISandboxApplyCommandKind,
    CLISandboxApplyCommandMode,
    CLISandboxApplyCommandResult,
    CLISandboxApplyCommandSpec,
    CLISandboxApplyDecisionKind,
    CLISandboxApplyDeniedCommand,
    CLISandboxApplyFlagSet,
    CLISandboxApplyInputSourceKind,
    CLISandboxApplyInvocation,
    CLISandboxApplyInvocationDecision,
    CLISandboxApplyNoExternalSideEffectGuarantee,
    CLISandboxApplyOutputFormat,
    CLISandboxApplyReadinessLevel,
    CLISandboxApplyRiskKind,
    CLISandboxApplyRunOutput,
    CLISandboxApplyRunPreview,
    CLISandboxApplyRunReport,
    CLISandboxApplyRuntimeContext,
    CLISandboxApplySourceRef,
    CLISandboxApplySurface,
    CLISandboxApplySurfacePolicy,
    CLISandboxApplySurfaceStatus,
    V0368ReadinessReport,
    build_cli_sandbox_apply_argument_spec,
    build_cli_sandbox_apply_command_result,
    build_cli_sandbox_apply_command_spec,
    build_cli_sandbox_apply_denied_command,
    build_cli_sandbox_apply_flags,
    build_cli_sandbox_apply_invocation_decision,
    build_cli_sandbox_apply_no_external_side_effect_guarantee,
    build_cli_sandbox_apply_run_preview,
    build_cli_sandbox_apply_run_report,
    build_cli_sandbox_apply_runtime_context,
    build_cli_sandbox_apply_source_ref,
    build_cli_sandbox_apply_surface_policy,
    build_default_cli_sandbox_apply_surface,
    build_v0368_readiness_report,
    cli_sandbox_apply_decision_blocks_external_agent,
    cli_sandbox_apply_decision_blocks_live_apply,
    cli_sandbox_apply_flags_preserve_unsafe_false,
    cli_sandbox_apply_invocation_is_not_shell,
    cli_sandbox_apply_surface_is_not_shell,
    default_cli_sandbox_apply_command_specs,
    default_cli_sandbox_apply_surface_policy,
    evaluate_cli_sandbox_apply_invocation,
    parse_cli_sandbox_apply_invocation,
    run_cli_sandbox_apply_command,
    v0368_readiness_report_is_not_execution_ready,
)


def test_v0368_taxonomies_have_required_values():
    assert {item.value for item in CLISandboxApplyCommandKind} == {
        "sandbox_apply_help",
        "sandbox_apply_status",
        "sandbox_apply_dry_run_preview",
        "sandbox_apply_candidate_preview",
        "sandbox_approval_validate",
        "sandbox_workspace_preview",
        "sandbox_apply_preview",
        "sandbox_apply_run",
        "sandbox_validate",
        "sandbox_reconcile",
        "agentic_task_preview",
        "agentic_task_run_once",
        "sandbox_trace_preview",
        "sandbox_bundle_preview",
        "live_apply_denied",
        "live_write_denied",
        "live_edit_denied",
        "apply_patch_denied",
        "git_apply_denied",
        "test_execution_denied",
        "dependency_install_denied",
        "shell_command_denied",
        "reference_execution_denied",
        "external_agent_denied",
        "dominion_denied",
        "auto_repair_denied",
        "multi_cycle_denied",
        "no_op",
        "unknown",
    }
    assert {item.value for item in CLISandboxApplyCommandMode} == {
        "help",
        "status",
        "dry_run_preview",
        "candidate_preview",
        "approval_validate",
        "workspace_preview",
        "sandbox_apply_preview",
        "sandbox_apply_run",
        "validation",
        "reconciliation",
        "agentic_task_preview",
        "agentic_task_run_once",
        "trace_preview",
        "bundle_preview",
        "denied",
        "blocked",
        "no_op",
        "unknown",
    }
    assert "argv_list" in {item.value for item in CLISandboxApplyInputSourceKind}
    assert "completed" in {item.value for item in CLISandboxApplySurfaceStatus}
    assert "allow_sandbox_apply_run" in {item.value for item in CLISandboxApplyDecisionKind}
    assert "json" in {item.value for item in CLISandboxApplyOutputFormat}
    assert "external_agent_execution_risk" in {item.value for item in CLISandboxApplyRiskKind}
    assert "bounded_agentic_task_run_once_ready" in {item.value for item in CLISandboxApplyReadinessLevel}


def test_required_models_are_exported():
    for model in (
        CLISandboxApplyFlagSet,
        CLISandboxApplySourceRef,
        CLISandboxApplyArgumentSpec,
        CLISandboxApplyCommandSpec,
        CLISandboxApplySurfacePolicy,
        CLISandboxApplySurface,
        CLISandboxApplyInvocation,
        CLISandboxApplyInvocationDecision,
        CLISandboxApplyDeniedCommand,
        CLISandboxApplyRuntimeContext,
        CLISandboxApplyCommandResult,
        CLISandboxApplyRunOutput,
        CLISandboxApplyRunReport,
        CLISandboxApplyRunPreview,
        CLISandboxApplyNoExternalSideEffectGuarantee,
        V0368ReadinessReport,
    ):
        assert model is not None


def _unsafe_flag_names(cls):
    safe_ready = {
        "ready_for_v0369_patch_apply_sandbox_consolidation",
        "ready_for_cli_sandbox_apply_surface",
        "ready_for_bounded_cli_sandbox_apply_preview",
        "ready_for_cli_apply_candidate_preview",
        "ready_for_cli_dry_run_preview",
        "ready_for_cli_sandbox_workspace_preview",
        "ready_for_cli_sandbox_apply_run",
        "ready_for_cli_sandbox_post_apply_validation",
        "ready_for_cli_agentic_task_run_once",
        "ready_for_cli_trace_preview",
        "ready_for_sandbox_file_write",
        "ready_for_sandbox_patch_apply",
    }
    return [field.name for field in fields(cls) if field.name.startswith("ready_for_") and field.name not in safe_ready]


def test_flags_allow_cli_surface_and_preserve_unsafe_false():
    flags = build_cli_sandbox_apply_flags()
    assert flags.cli_sandbox_apply_surface_constructed
    assert flags.cli_argument_parsing_enabled
    assert flags.bounded_preview_command_dispatch_enabled
    assert flags.bounded_sandbox_apply_dispatch_enabled
    assert flags.bounded_agentic_task_dispatch_enabled
    assert flags.denied_unsafe_command_handling_enabled
    assert flags.ready_for_v0369_patch_apply_sandbox_consolidation
    assert flags.ready_for_cli_sandbox_apply_run
    assert flags.ready_for_sandbox_file_write
    assert flags.ready_for_sandbox_patch_apply
    assert cli_sandbox_apply_flags_preserve_unsafe_false(flags)
    for name in _unsafe_flag_names(CLISandboxApplyFlagSet) + ["production_certified"]:
        assert getattr(flags, name) is False


@pytest.mark.parametrize(
    "field_name",
    [
        "ready_for_execution",
        "ready_for_live_workspace_write",
        "ready_for_patch_application",
        "ready_for_workspace_write",
        "ready_for_code_edit",
        "ready_for_apply_patch",
        "ready_for_git_apply",
        "ready_for_test_execution",
        "ready_for_shell_execution",
        "ready_for_external_agent_execution",
        "ready_for_claude_code_invocation",
        "ready_for_codex_cli_invocation",
        "ready_for_dominion_runtime",
        "ready_for_infinite_agent_loop",
        "ready_for_automatic_repair",
        "ready_for_multi_cycle_agentic_loop",
    ],
)
def test_flags_reject_unsafe_true_values(field_name):
    with pytest.raises(ValueError):
        build_cli_sandbox_apply_flags(**{field_name: True})


def test_source_ref_argument_spec_and_command_spec_are_not_execution():
    source = build_cli_sandbox_apply_source_ref()
    arg = build_cli_sandbox_apply_argument_spec(max_value_chars=12)
    spec = build_cli_sandbox_apply_command_spec(command_kind=CLISandboxApplyCommandKind.SANDBOX_APPLY_RUN)
    assert source.source_kind == CLISandboxApplyInputSourceKind.TEST_FIXTURE
    assert arg.max_value_chars == 12
    assert isinstance(spec, CLISandboxApplyCommandSpec)
    assert spec.command_kind == CLISandboxApplyCommandKind.SANDBOX_APPLY_RUN


def test_surface_policy_allows_safe_dispatch_and_blocks_runtime():
    policy = default_cli_sandbox_apply_surface_policy()
    assert policy.allow_candidate_preview
    assert policy.allow_sandbox_apply_run
    assert policy.allow_sandbox_file_write
    assert policy.allow_sandbox_patch_apply
    for name in (
        "allow_live_workspace_write",
        "allow_patch_application",
        "allow_workspace_write",
        "allow_code_edit",
        "allow_apply_patch",
        "allow_git_apply",
        "allow_test_execution",
        "allow_shell",
        "allow_subprocess",
        "allow_command_execution",
        "allow_dependency_install",
        "allow_reference_execution",
        "allow_reference_import",
        "allow_external_agent_execution",
        "allow_claude_code_invocation",
        "allow_codex_cli_invocation",
        "allow_dominion_runtime",
        "allow_provider_invocation",
        "allow_network_access",
        "allow_credential_access",
        "allow_secret_read",
        "allow_persistent_trace_write",
        "allow_ui_runtime",
    ):
        assert getattr(policy, name) is False


@pytest.mark.parametrize(
    "field_name",
    [
        "allow_shell",
        "allow_subprocess",
        "allow_command_execution",
        "allow_live_workspace_write",
        "allow_patch_application",
        "allow_code_edit",
        "allow_apply_patch",
        "allow_git_apply",
        "allow_test_execution",
        "allow_dependency_install",
        "allow_reference_execution",
        "allow_external_agent_execution",
        "allow_dominion_runtime",
        "allow_provider_invocation",
        "allow_network_access",
        "allow_credential_access",
        "allow_persistent_trace_write",
        "allow_ui_runtime",
    ],
)
def test_surface_policy_rejects_unsafe_true_values(field_name):
    with pytest.raises(ValueError):
        build_cli_sandbox_apply_surface_policy(**{field_name: True})


def test_surface_is_not_shell():
    surface = build_default_cli_sandbox_apply_surface()
    assert isinstance(surface, CLISandboxApplySurface)
    assert cli_sandbox_apply_surface_is_not_shell(surface)
    assert surface.ready_for_execution is False
    assert len(default_cli_sandbox_apply_command_specs()) >= 20


@pytest.mark.parametrize(
    ("command", "kind"),
    [
        ("sandbox-apply-help", CLISandboxApplyCommandKind.SANDBOX_APPLY_HELP),
        ("sandbox-apply-status", CLISandboxApplyCommandKind.SANDBOX_APPLY_STATUS),
        ("no-op", CLISandboxApplyCommandKind.NO_OP),
        ("sandbox-apply-dry-run-preview", CLISandboxApplyCommandKind.SANDBOX_APPLY_DRY_RUN_PREVIEW),
        ("sandbox-apply-candidate-preview", CLISandboxApplyCommandKind.SANDBOX_APPLY_CANDIDATE_PREVIEW),
        ("sandbox-approval-validate", CLISandboxApplyCommandKind.SANDBOX_APPROVAL_VALIDATE),
        ("sandbox-workspace-preview", CLISandboxApplyCommandKind.SANDBOX_WORKSPACE_PREVIEW),
        ("sandbox-apply-preview", CLISandboxApplyCommandKind.SANDBOX_APPLY_PREVIEW),
        ("sandbox-apply-run", CLISandboxApplyCommandKind.SANDBOX_APPLY_RUN),
        ("sandbox-validate", CLISandboxApplyCommandKind.SANDBOX_VALIDATE),
        ("sandbox-reconcile", CLISandboxApplyCommandKind.SANDBOX_RECONCILE),
        ("agentic-task-preview", CLISandboxApplyCommandKind.AGENTIC_TASK_PREVIEW),
        ("agentic-task-run-once", CLISandboxApplyCommandKind.AGENTIC_TASK_RUN_ONCE),
        ("sandbox-trace-preview", CLISandboxApplyCommandKind.SANDBOX_TRACE_PREVIEW),
        ("sandbox-bundle-preview", CLISandboxApplyCommandKind.SANDBOX_BUNDLE_PREVIEW),
    ],
)
def test_parse_safe_commands(command, kind):
    invocation = parse_cli_sandbox_apply_invocation([command, "--format", "json"])
    assert invocation.command_kind == kind
    assert invocation.requested_output_format == CLISandboxApplyOutputFormat.JSON
    assert cli_sandbox_apply_invocation_is_not_shell(invocation)


@pytest.mark.parametrize(
    ("command", "kind"),
    [
        ("patch-apply-live", CLISandboxApplyCommandKind.LIVE_APPLY_DENIED),
        ("apply-live", CLISandboxApplyCommandKind.LIVE_APPLY_DENIED),
        ("write-live", CLISandboxApplyCommandKind.LIVE_WRITE_DENIED),
        ("edit-live", CLISandboxApplyCommandKind.LIVE_EDIT_DENIED),
        ("workspace-write", CLISandboxApplyCommandKind.LIVE_WRITE_DENIED),
        ("code-edit", CLISandboxApplyCommandKind.LIVE_EDIT_DENIED),
        ("git-apply", CLISandboxApplyCommandKind.GIT_APPLY_DENIED),
        ("apply-patch", CLISandboxApplyCommandKind.APPLY_PATCH_DENIED),
        ("test-run", CLISandboxApplyCommandKind.TEST_EXECUTION_DENIED),
        ("pytest", CLISandboxApplyCommandKind.TEST_EXECUTION_DENIED),
        ("npm-test", CLISandboxApplyCommandKind.TEST_EXECUTION_DENIED),
        ("install", CLISandboxApplyCommandKind.DEPENDENCY_INSTALL_DENIED),
        ("npm", CLISandboxApplyCommandKind.DEPENDENCY_INSTALL_DENIED),
        ("pip", CLISandboxApplyCommandKind.DEPENDENCY_INSTALL_DENIED),
        ("run-opencode", CLISandboxApplyCommandKind.REFERENCE_EXECUTION_DENIED),
        ("run-hermes", CLISandboxApplyCommandKind.REFERENCE_EXECUTION_DENIED),
        ("run-openclaw", CLISandboxApplyCommandKind.REFERENCE_EXECUTION_DENIED),
        ("run-claude-code", CLISandboxApplyCommandKind.EXTERNAL_AGENT_DENIED),
        ("run-codex", CLISandboxApplyCommandKind.EXTERNAL_AGENT_DENIED),
        ("dominion", CLISandboxApplyCommandKind.DOMINION_DENIED),
        ("external-agent-loop", CLISandboxApplyCommandKind.EXTERNAL_AGENT_DENIED),
        ("infinite-loop", CLISandboxApplyCommandKind.DOMINION_DENIED),
        ("recursive-agent", CLISandboxApplyCommandKind.EXTERNAL_AGENT_DENIED),
        ("auto-repair", CLISandboxApplyCommandKind.AUTO_REPAIR_DENIED),
        ("repair-loop", CLISandboxApplyCommandKind.AUTO_REPAIR_DENIED),
        ("retry-loop", CLISandboxApplyCommandKind.MULTI_CYCLE_DENIED),
        ("multi-cycle", CLISandboxApplyCommandKind.MULTI_CYCLE_DENIED),
    ],
)
def test_parse_denied_commands(command, kind):
    invocation = parse_cli_sandbox_apply_invocation([command])
    assert invocation.command_kind == kind
    output = run_cli_sandbox_apply_command(invocation, build_default_cli_sandbox_apply_surface())
    assert output.denied_command is not None
    assert output.command_result is None
    assert output.status == CLISandboxApplySurfaceStatus.BLOCKED


def test_unknown_and_shell_like_command_denied():
    surface = build_default_cli_sandbox_apply_surface()
    unknown = parse_cli_sandbox_apply_invocation(["unknown-command"])
    shell_like = parse_cli_sandbox_apply_invocation(["sandbox-apply-help", "&&", "pytest"])
    for invocation in (unknown, shell_like):
        decision = evaluate_cli_sandbox_apply_invocation(invocation, surface)
        assert decision.allowed_command_kind is None
        assert decision.bounded_preview_allowed is False
        assert cli_sandbox_apply_decision_blocks_live_apply(decision)
        assert cli_sandbox_apply_decision_blocks_external_agent(decision)


def test_evaluate_allows_safe_preview_only():
    surface = build_default_cli_sandbox_apply_surface()
    invocation = parse_cli_sandbox_apply_invocation(["sandbox-apply-dry-run-preview"])
    decision = evaluate_cli_sandbox_apply_invocation(invocation, surface)
    assert decision.decision_kind == CLISandboxApplyDecisionKind.ALLOW_DRY_RUN_PREVIEW
    assert decision.bounded_preview_allowed
    assert not decision.sandbox_apply_run_allowed
    assert cli_sandbox_apply_decision_blocks_live_apply(decision)


def test_sandbox_apply_run_requires_context():
    surface = build_default_cli_sandbox_apply_surface()
    invocation = parse_cli_sandbox_apply_invocation(["sandbox-apply-run"])
    denied = evaluate_cli_sandbox_apply_invocation(invocation, surface)
    assert denied.decision_kind == CLISandboxApplyDecisionKind.REQUIRE_REVIEW
    context = build_cli_sandbox_apply_runtime_context(sandbox_root_ref="sandbox-root")
    allowed = evaluate_cli_sandbox_apply_invocation(invocation, surface, context)
    assert allowed.decision_kind == CLISandboxApplyDecisionKind.ALLOW_SANDBOX_APPLY_RUN
    assert allowed.sandbox_apply_run_allowed
    assert allowed.sandbox_file_write_allowed
    assert allowed.sandbox_patch_apply_allowed


def test_sandbox_apply_run_writes_only_under_tmp_sandbox_root(tmp_path):
    surface = build_default_cli_sandbox_apply_surface()
    context = build_cli_sandbox_apply_runtime_context(sandbox_root_ref=str(tmp_path))
    invocation = parse_cli_sandbox_apply_invocation(["sandbox-apply-run"])
    output = run_cli_sandbox_apply_command(invocation, surface, context)
    assert output.command_result is not None
    assert output.command_result.command_kind == CLISandboxApplyCommandKind.SANDBOX_APPLY_RUN
    assert output.command_result.sandbox_write_performed is True
    assert output.command_result.live_write_performed is False
    assert output.ready_for_execution is False
    assert (tmp_path / "src" / "example.py").exists()


def test_agentic_task_run_once_is_single_cycle_metadata():
    surface = build_default_cli_sandbox_apply_surface()
    invocation = parse_cli_sandbox_apply_invocation(["agentic-task-run-once"])
    output = run_cli_sandbox_apply_command(invocation, surface)
    assert output.command_result is not None
    assert output.command_result.agentic_operation_run_packet_ref
    assert output.command_result.structured_result["single_cycle_only"] is True
    assert output.ready_for_execution is False


def test_trace_preview_is_v0367_returned_packet_only():
    surface = build_default_cli_sandbox_apply_surface()
    invocation = parse_cli_sandbox_apply_invocation(["sandbox-trace-preview"])
    output = run_cli_sandbox_apply_command(invocation, surface)
    assert output.command_result is not None
    assert output.command_result.trace_packet_ref
    assert output.command_result.structured_result["trace_persisted"] is False
    assert output.ready_for_execution is False


def test_run_output_bounded_redacted_and_not_file_write():
    surface = build_default_cli_sandbox_apply_surface()
    invocation = parse_cli_sandbox_apply_invocation(["sandbox-apply-help", "--task", "secret token " + "x" * 3000])
    output = run_cli_sandbox_apply_command(invocation, surface)
    assert "[redacted]" in output.rendered_output or output.denied_command is not None
    assert len(output.rendered_output) <= 1600
    assert output.ready_for_execution is False


def test_run_report_preview_guarantee_and_readiness():
    report = build_cli_sandbox_apply_run_report()
    preview = build_cli_sandbox_apply_run_preview()
    guarantee = build_cli_sandbox_apply_no_external_side_effect_guarantee()
    readiness = build_v0368_readiness_report()
    assert isinstance(report, CLISandboxApplyRunReport)
    assert isinstance(preview, CLISandboxApplyRunPreview)
    for field in fields(guarantee):
        if field.name.startswith("no_"):
            assert getattr(guarantee, field.name) is True
    assert isinstance(readiness, V0368ReadinessReport)
    assert readiness.ready_for_v0369_patch_apply_sandbox_consolidation
    assert readiness.ready_for_cli_sandbox_apply_surface
    assert v0368_readiness_report_is_not_execution_ready(readiness)


@pytest.mark.parametrize(
    "field_name",
    [
        "ready_for_execution",
        "ready_for_live_workspace_write",
        "ready_for_patch_application",
        "ready_for_workspace_write",
        "ready_for_code_edit",
        "ready_for_apply_patch",
        "ready_for_git_apply",
        "ready_for_test_execution",
        "ready_for_shell_execution",
        "ready_for_external_agent_execution",
        "ready_for_dominion_runtime",
        "ready_for_persistent_trace_write",
    ],
)
def test_readiness_report_rejects_unsafe_true_values(field_name):
    with pytest.raises(ValueError):
        build_v0368_readiness_report(**{field_name: True})


def test_negative_decision_allowed_flags_rejected():
    with pytest.raises(ValueError):
        build_cli_sandbox_apply_invocation_decision(live_workspace_write_allowed=True)
    with pytest.raises(ValueError):
        build_cli_sandbox_apply_invocation_decision(shell_execution_allowed=True)


def test_command_result_rejects_live_write_and_non_run_sandbox_write():
    with pytest.raises(ValueError):
        build_cli_sandbox_apply_command_result(live_write_performed=True)
    with pytest.raises(ValueError):
        build_cli_sandbox_apply_command_result(
            command_kind=CLISandboxApplyCommandKind.SANDBOX_APPLY_HELP,
            sandbox_write_performed=True,
        )


def test_helpers_do_not_contain_runtime_execution_patterns():
    import chanta_core.agent_runtime.patch_apply_cli_surface as module

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
    ]
    for pattern in forbidden:
        assert pattern not in source
    assert "apply_patch(" not in source
    assert "git apply" not in source
