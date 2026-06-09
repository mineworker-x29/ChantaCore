import inspect

import pytest

from chanta_core.agent_runtime import (
    CLIPatchProposalArgumentSpec,
    CLIPatchProposalCommandKind,
    CLIPatchProposalCommandMode,
    CLIPatchProposalCommandResult,
    CLIPatchProposalCommandSpec,
    CLIPatchProposalDecisionKind,
    CLIPatchProposalDeniedCommand,
    CLIPatchProposalFlagSet,
    CLIPatchProposalInputSourceKind,
    CLIPatchProposalInvocation,
    CLIPatchProposalInvocationDecision,
    CLIPatchProposalNoExternalSideEffectGuarantee,
    CLIPatchProposalOutputFormat,
    CLIPatchProposalReadinessLevel,
    CLIPatchProposalRiskKind,
    CLIPatchProposalRunOutput,
    CLIPatchProposalRunPreview,
    CLIPatchProposalRunReport,
    CLIPatchProposalRuntimeContext,
    CLIPatchProposalSourceRef,
    CLIPatchProposalSurface,
    CLIPatchProposalSurfacePolicy,
    CLIPatchProposalSurfaceStatus,
    V0358ReadinessReport,
    build_cli_patch_proposal_argument_spec,
    build_cli_patch_proposal_command_result,
    build_cli_patch_proposal_command_spec,
    build_cli_patch_proposal_denied_command,
    build_cli_patch_proposal_flags,
    build_cli_patch_proposal_invocation,
    build_cli_patch_proposal_invocation_decision,
    build_cli_patch_proposal_no_external_side_effect_guarantee,
    build_cli_patch_proposal_run_output,
    build_cli_patch_proposal_run_preview,
    build_cli_patch_proposal_run_report,
    build_cli_patch_proposal_runtime_context,
    build_cli_patch_proposal_source_ref,
    build_cli_patch_proposal_surface,
    build_cli_patch_proposal_surface_policy,
    build_default_cli_patch_proposal_surface,
    build_v0358_readiness_report,
    cli_patch_proposal_decision_blocks_apply,
    cli_patch_proposal_decision_blocks_external_agent,
    cli_patch_proposal_flags_preserve_unsafe_false,
    cli_patch_proposal_invocation_is_not_shell,
    cli_patch_proposal_surface_is_not_shell,
    default_cli_patch_proposal_command_specs,
    default_cli_patch_proposal_surface_policy,
    evaluate_cli_patch_proposal_invocation,
    parse_cli_patch_proposal_invocation,
    render_cli_patch_proposal_output,
    run_cli_patch_proposal_command,
    v0358_readiness_report_is_not_execution_ready,
)
from chanta_core.agent_runtime import patch_cli_surface as cli_module


def test_v0358_taxonomies_have_required_values() -> None:
    assert {item.value for item in CLIPatchProposalCommandKind} == {
        "patch_help",
        "patch_status",
        "patch_dry_run",
        "patch_intent_preview",
        "patch_scope_preview",
        "patch_context_preview",
        "patch_plan_preview",
        "patch_diff_preview",
        "patch_risk",
        "patch_review",
        "patch_trace_preview",
        "patch_bundle_preview",
        "patch_apply_denied",
        "patch_write_denied",
        "patch_edit_denied",
        "patch_test_denied",
        "patch_install_denied",
        "external_agent_denied",
        "dominion_denied",
        "no_op",
        "unknown",
    }
    assert {item.value for item in CLIPatchProposalCommandMode} == {
        "help",
        "status",
        "dry_run",
        "intent_preview",
        "scope_preview",
        "context_preview",
        "plan_preview",
        "diff_preview",
        "risk_preview",
        "review_preview",
        "trace_preview",
        "bundle_preview",
        "denied",
        "blocked",
        "no_op",
        "unknown",
    }
    assert {item.value for item in CLIPatchProposalInputSourceKind} == {
        "argv_list",
        "parsed_args",
        "runtime_context",
        "intent_text_arg",
        "scope_arg",
        "task_arg",
        "patch_intent_ref",
        "patch_context_snapshot_ref",
        "patch_plan_ref",
        "diff_envelope_ref",
        "risk_report_ref",
        "review_packet_ref",
        "trace_packet_ref",
        "reference_digest_ref",
        "test_fixture",
        "unknown",
    }
    assert {item.value for item in CLIPatchProposalSurfaceStatus} == {
        "unknown",
        "initialized",
        "parsed",
        "decision_ready",
        "allowed",
        "denied",
        "blocked",
        "completed",
        "completed_with_warnings",
        "safe_failed",
        "no_op",
        "future_gated",
    }
    assert {item.value for item in CLIPatchProposalDecisionKind} == {
        "allow_help",
        "allow_status",
        "allow_dry_run",
        "allow_intent_preview",
        "allow_scope_preview",
        "allow_context_preview",
        "allow_plan_preview",
        "allow_diff_preview",
        "allow_risk_preview",
        "allow_review_preview",
        "allow_trace_preview",
        "allow_bundle_preview",
        "deny_patch_apply",
        "deny_write_edit",
        "deny_test_execution",
        "deny_dependency_install",
        "deny_shell_command",
        "deny_reference_execution",
        "deny_external_agent_execution",
        "deny_dominion_runtime",
        "deny",
        "block",
        "no_op",
        "require_review",
        "future_gate_required",
        "unknown",
    }
    assert {item.value for item in CLIPatchProposalOutputFormat} == {
        "text",
        "markdown",
        "json",
        "structured_artifact",
        "debug_summary",
        "no_output",
        "unknown",
    }
    assert {item.value for item in CLIPatchProposalRiskKind} == {
        "shell_injection_risk",
        "command_execution_risk",
        "patch_apply_risk",
        "workspace_write_risk",
        "code_edit_risk",
        "test_execution_risk",
        "dependency_install_risk",
        "reference_execution_risk",
        "reference_import_risk",
        "external_agent_execution_risk",
        "claude_code_invocation_risk",
        "codex_cli_invocation_risk",
        "dominion_runtime_risk",
        "infinite_agent_loop_risk",
        "direct_provider_invocation_risk",
        "direct_network_access_risk",
        "credential_access_risk",
        "secret_read_risk",
        "persistent_trace_write_risk",
        "ui_runtime_risk",
        "authority_grant_risk",
        "unknown",
    }
    assert {item.value for item in CLIPatchProposalReadinessLevel} == {
        "not_ready",
        "cli_contract_ready",
        "bounded_cli_patch_proposal_surface_ready",
        "bounded_preview_command_dispatch_ready",
        "design_handoff_ready_for_v0359",
        "blocked",
        "future_track",
    }


def test_required_models_are_exported() -> None:
    for model in (
        CLIPatchProposalFlagSet,
        CLIPatchProposalSourceRef,
        CLIPatchProposalArgumentSpec,
        CLIPatchProposalCommandSpec,
        CLIPatchProposalSurfacePolicy,
        CLIPatchProposalSurface,
        CLIPatchProposalInvocation,
        CLIPatchProposalInvocationDecision,
        CLIPatchProposalDeniedCommand,
        CLIPatchProposalRuntimeContext,
        CLIPatchProposalCommandResult,
        CLIPatchProposalRunOutput,
        CLIPatchProposalRunReport,
        CLIPatchProposalRunPreview,
        CLIPatchProposalNoExternalSideEffectGuarantee,
        V0358ReadinessReport,
    ):
        assert inspect.isclass(model)


def test_flags_allow_safe_preview_readiness_and_block_unsafe() -> None:
    flags = build_cli_patch_proposal_flags()
    assert flags.cli_patch_proposal_surface_constructed is True
    assert flags.cli_argument_parsing_enabled is True
    assert flags.bounded_preview_command_dispatch_enabled is True
    assert flags.denied_unsafe_command_handling_enabled is True
    assert flags.ready_for_v0359_consolidation is True
    assert flags.ready_for_cli_patch_proposal_surface is True
    assert flags.ready_for_bounded_cli_patch_proposal_preview is True
    assert flags.ready_for_cli_patch_intent_preview is True
    assert flags.ready_for_cli_patch_context_preview is True
    assert flags.ready_for_cli_patch_plan_preview is True
    assert flags.ready_for_cli_diff_proposal_preview is True
    assert flags.ready_for_cli_patch_risk_preview is True
    assert flags.ready_for_cli_patch_review_preview is True
    assert flags.ready_for_cli_patch_trace_preview is True
    assert cli_patch_proposal_flags_preserve_unsafe_false(flags) is True

    for field in (
        "ready_for_execution",
        "ready_for_patch_application",
        "ready_for_workspace_write",
        "ready_for_code_edit",
        "ready_for_apply_patch",
        "ready_for_git_apply",
        "ready_for_test_execution",
        "ready_for_shell_execution",
        "ready_for_subprocess_execution",
        "ready_for_command_execution",
        "ready_for_dependency_install",
        "ready_for_reference_execution",
        "ready_for_reference_import",
        "ready_for_external_agent_execution",
        "ready_for_claude_code_invocation",
        "ready_for_codex_cli_invocation",
        "ready_for_dominion_runtime",
        "ready_for_infinite_agent_loop",
        "ready_for_provider_invocation",
        "ready_for_direct_network_access",
        "ready_for_credential_access",
        "ready_for_secret_read",
        "ready_for_general_agent_execution",
        "ready_for_autonomous_agent_runtime",
        "ready_for_general_tool_execution",
        "ready_for_unquarantined_action_execution",
        "ready_for_persistent_trace_write",
        "ready_for_external_trace_sink",
        "ready_for_ui_runtime",
        "ready_for_external_control",
        "ready_for_authority_grant",
        "production_certified",
    ):
        with pytest.raises(ValueError):
            build_cli_patch_proposal_flags(**{field: True})


def test_source_argument_command_policy_and_surface_are_not_shell() -> None:
    source = build_cli_patch_proposal_source_ref(
        source_kind=CLIPatchProposalInputSourceKind.ARGV_LIST,
        source_id="argv",
        source_summary="argv metadata only",
    )
    arg = build_cli_patch_proposal_argument_spec(max_value_chars=32)
    command = build_cli_patch_proposal_command_spec(
        command_kind=CLIPatchProposalCommandKind.PATCH_DIFF_PREVIEW,
        command_name="patch-diff-preview",
    )
    policy = default_cli_patch_proposal_surface_policy()
    surface = build_default_cli_patch_proposal_surface()

    assert source.source_kind == CLIPatchProposalInputSourceKind.ARGV_LIST
    assert arg.max_value_chars == 32
    assert command.command_mode == CLIPatchProposalCommandMode.DIFF_PREVIEW
    assert policy.allow_patch_intent_preview is True
    assert policy.allow_patch_context_preview is True
    assert policy.allow_patch_plan_preview is True
    assert policy.allow_diff_proposal_preview is True
    assert policy.allow_patch_risk_preview is True
    assert policy.allow_patch_review_preview is True
    assert policy.allow_patch_trace_preview is True
    assert policy.allow_shell is False
    assert policy.allow_subprocess is False
    assert policy.allow_command_execution is False
    assert policy.allow_patch_application is False
    assert policy.allow_workspace_write is False
    assert policy.allow_code_edit is False
    assert policy.allow_apply_patch is False
    assert policy.allow_git_apply is False
    assert policy.allow_test_execution is False
    assert policy.allow_dependency_install is False
    assert policy.allow_reference_execution is False
    assert policy.allow_reference_import is False
    assert policy.allow_external_agent_execution is False
    assert policy.allow_claude_code_invocation is False
    assert policy.allow_codex_cli_invocation is False
    assert policy.allow_dominion_runtime is False
    assert policy.allow_infinite_agent_loop is False
    assert policy.allow_provider_invocation is False
    assert policy.allow_network_access is False
    assert policy.allow_credential_access is False
    assert policy.allow_secret_read is False
    assert policy.allow_persistent_trace_write is False
    assert policy.allow_ui_runtime is False
    assert cli_patch_proposal_surface_is_not_shell(surface) is True
    assert surface.ready_for_execution is False
    assert surface.ready_for_cli_patch_proposal_surface is True

    for field in (
        "allow_shell",
        "allow_subprocess",
        "allow_command_execution",
        "allow_patch_application",
        "allow_workspace_write",
        "allow_code_edit",
        "allow_apply_patch",
        "allow_git_apply",
        "allow_test_execution",
        "allow_dependency_install",
        "allow_reference_execution",
        "allow_reference_import",
        "allow_external_agent_execution",
        "allow_claude_code_invocation",
        "allow_codex_cli_invocation",
        "allow_dominion_runtime",
        "allow_infinite_agent_loop",
        "allow_provider_invocation",
        "allow_network_access",
        "allow_credential_access",
        "allow_secret_read",
        "allow_persistent_trace_write",
        "allow_ui_runtime",
    ):
        with pytest.raises(ValueError):
            build_cli_patch_proposal_surface_policy(**{field: True})

    with pytest.raises(ValueError):
        build_cli_patch_proposal_surface_policy(prohibited_arg_patterns=["secret"])


def test_default_command_specs_include_safe_and_denied_commands() -> None:
    specs = default_cli_patch_proposal_command_specs()
    names = {spec.command_name for spec in specs}
    for name in (
        "patch-help",
        "patch-status",
        "patch-dry-run",
        "patch-intent-preview",
        "patch-context-preview",
        "patch-plan-preview",
        "patch-diff-preview",
        "patch-risk",
        "patch-review",
        "patch-trace-preview",
        "patch-bundle-preview",
        "no-op",
        "patch-apply",
        "run-opencode",
        "run-claude-code",
        "dominion",
        "infinite-loop",
    ):
        assert name in names
    assert all(spec.command_name != "shell" for spec in specs)


def test_parse_safe_commands() -> None:
    surface = build_default_cli_patch_proposal_surface()
    cases = {
        "patch-help": CLIPatchProposalCommandKind.PATCH_HELP,
        "patch-status": CLIPatchProposalCommandKind.PATCH_STATUS,
        "patch-dry-run": CLIPatchProposalCommandKind.PATCH_DRY_RUN,
        "patch-intent-preview": CLIPatchProposalCommandKind.PATCH_INTENT_PREVIEW,
        "patch-scope-preview": CLIPatchProposalCommandKind.PATCH_SCOPE_PREVIEW,
        "patch-context-preview": CLIPatchProposalCommandKind.PATCH_CONTEXT_PREVIEW,
        "patch-plan-preview": CLIPatchProposalCommandKind.PATCH_PLAN_PREVIEW,
        "patch-diff-preview": CLIPatchProposalCommandKind.PATCH_DIFF_PREVIEW,
        "patch-risk": CLIPatchProposalCommandKind.PATCH_RISK,
        "patch-review": CLIPatchProposalCommandKind.PATCH_REVIEW,
        "patch-trace-preview": CLIPatchProposalCommandKind.PATCH_TRACE_PREVIEW,
        "patch-bundle-preview": CLIPatchProposalCommandKind.PATCH_BUNDLE_PREVIEW,
        "no-op": CLIPatchProposalCommandKind.NO_OP,
    }
    for command, kind in cases.items():
        invocation = parse_cli_patch_proposal_invocation(["patch", command, "--format", "json"], surface)
        assert invocation.command_kind == kind
        assert invocation.requested_output_format == CLIPatchProposalOutputFormat.JSON
        assert cli_patch_proposal_invocation_is_not_shell(invocation) is True


def test_evaluate_allows_bounded_preview_only_for_safe_commands() -> None:
    surface = build_default_cli_patch_proposal_surface()
    for command in (
        "patch-help",
        "patch-status",
        "patch-dry-run",
        "patch-intent-preview",
        "patch-scope-preview",
        "patch-context-preview",
        "patch-plan-preview",
        "patch-diff-preview",
        "patch-risk",
        "patch-review",
        "patch-trace-preview",
        "patch-bundle-preview",
    ):
        invocation = parse_cli_patch_proposal_invocation([command], surface)
        decision = evaluate_cli_patch_proposal_invocation(invocation, surface)
        assert decision.bounded_preview_allowed is True
        assert cli_patch_proposal_decision_blocks_apply(decision) is True
        assert cli_patch_proposal_decision_blocks_external_agent(decision) is True
    no_op = evaluate_cli_patch_proposal_invocation(parse_cli_patch_proposal_invocation(["no-op"], surface), surface)
    assert no_op.decision_kind == CLIPatchProposalDecisionKind.NO_OP
    assert no_op.bounded_preview_allowed is False


def test_unknown_shell_apply_write_test_install_external_agent_and_dominion_commands_are_denied() -> None:
    surface = build_default_cli_patch_proposal_surface()
    denied_cases = {
        "does-not-exist": CLIPatchProposalDecisionKind.BLOCK,
        "status;whoami": CLIPatchProposalDecisionKind.DENY_SHELL_COMMAND,
        "shell": CLIPatchProposalDecisionKind.DENY_SHELL_COMMAND,
        "patch-apply": CLIPatchProposalDecisionKind.DENY_PATCH_APPLY,
        "apply": CLIPatchProposalDecisionKind.DENY_PATCH_APPLY,
        "write": CLIPatchProposalDecisionKind.DENY_WRITE_EDIT,
        "edit": CLIPatchProposalDecisionKind.DENY_WRITE_EDIT,
        "git-apply": CLIPatchProposalDecisionKind.DENY_PATCH_APPLY,
        "apply-patch": CLIPatchProposalDecisionKind.DENY_PATCH_APPLY,
        "test-run": CLIPatchProposalDecisionKind.DENY_TEST_EXECUTION,
        "pytest": CLIPatchProposalDecisionKind.DENY_TEST_EXECUTION,
        "install": CLIPatchProposalDecisionKind.DENY_DEPENDENCY_INSTALL,
        "npm": CLIPatchProposalDecisionKind.DENY_DEPENDENCY_INSTALL,
        "pip": CLIPatchProposalDecisionKind.DENY_DEPENDENCY_INSTALL,
        "run-opencode": CLIPatchProposalDecisionKind.DENY_EXTERNAL_AGENT_EXECUTION,
        "run-hermes": CLIPatchProposalDecisionKind.DENY_EXTERNAL_AGENT_EXECUTION,
        "run-openclaw": CLIPatchProposalDecisionKind.DENY_EXTERNAL_AGENT_EXECUTION,
        "run-claude-code": CLIPatchProposalDecisionKind.DENY_EXTERNAL_AGENT_EXECUTION,
        "run-codex": CLIPatchProposalDecisionKind.DENY_EXTERNAL_AGENT_EXECUTION,
        "external-agent-loop": CLIPatchProposalDecisionKind.DENY_EXTERNAL_AGENT_EXECUTION,
        "recursive-agent": CLIPatchProposalDecisionKind.DENY_EXTERNAL_AGENT_EXECUTION,
        "agent-chain": CLIPatchProposalDecisionKind.DENY_EXTERNAL_AGENT_EXECUTION,
        "harness-execute": CLIPatchProposalDecisionKind.DENY_EXTERNAL_AGENT_EXECUTION,
        "dominion": CLIPatchProposalDecisionKind.DENY_DOMINION_RUNTIME,
        "infinite-loop": CLIPatchProposalDecisionKind.DENY_DOMINION_RUNTIME,
    }
    for command, expected_decision in denied_cases.items():
        invocation = parse_cli_patch_proposal_invocation([command], surface)
        decision = evaluate_cli_patch_proposal_invocation(invocation, surface)
        assert decision.decision_kind == expected_decision
        assert decision.bounded_preview_allowed is False
        assert cli_patch_proposal_decision_blocks_apply(decision) is True
        assert cli_patch_proposal_decision_blocks_external_agent(decision) is True


def test_unsafe_args_are_denied_even_on_safe_commands() -> None:
    surface = build_default_cli_patch_proposal_surface()
    for argv in (
        ["patch-dry-run", "--task", "hello; whoami"],
        ["patch-intent-preview", "--task", "token=abc"],
        ["patch-trace-preview", "--task", "run-claude-code"],
        ["patch-bundle-preview", "--task", "dominion infinite-loop"],
    ):
        invocation = parse_cli_patch_proposal_invocation(list(argv), surface)
        decision = evaluate_cli_patch_proposal_invocation(invocation, surface)
        assert decision.decision_kind == CLIPatchProposalDecisionKind.DENY_SHELL_COMMAND
        assert decision.bounded_preview_allowed is False


def test_run_cli_returns_bounded_in_memory_previews_and_trace_preview_is_not_persistence() -> None:
    surface = build_default_cli_patch_proposal_surface()
    context = build_cli_patch_proposal_runtime_context(
        has_patch_intent_artifacts=True,
        has_patch_context_snapshot=True,
        has_patch_plan=True,
        has_diff_envelope=True,
        has_risk_report=True,
        has_review_packet=True,
        has_trace_packet=True,
        has_reference_digest=True,
        metadata={
            "patch_intent_ref": "bundle:fixture:v0.35.1",
            "patch_context_snapshot_ref": "context_snapshot:fixture:v0.35.2",
            "patch_plan_ref": "patch_plan:fixture:v0.35.3",
            "diff_envelope_ref": "diff_envelope:fixture:v0.35.4",
            "risk_report_ref": "risk_report:fixture:v0.35.5",
            "review_packet_ref": "review_packet:fixture:v0.35.6",
            "trace_packet_ref": "trace_packet:fixture:v0.35.7",
        },
    )
    expected_refs = {
        "patch-intent-preview": "patch_intent_ref",
        "patch-context-preview": "patch_context_snapshot_ref",
        "patch-plan-preview": "patch_plan_ref",
        "patch-diff-preview": "diff_envelope_ref",
        "patch-risk": "risk_report_ref",
        "patch-review": "review_packet_ref",
        "patch-trace-preview": "trace_packet_ref",
    }
    for command, ref_field in expected_refs.items():
        invocation = parse_cli_patch_proposal_invocation([command, "--format", "json"], surface)
        output = run_cli_patch_proposal_command(invocation, surface, context)
        assert output.status == CLIPatchProposalSurfaceStatus.COMPLETED
        assert output.ready_for_execution is False
        assert output.denied_command is None
        assert output.command_result is not None
        assert getattr(output.command_result, ref_field) is not None
        assert output.command_result.ready_for_execution is False
        assert len(output.rendered_output) <= 1200
    trace_output = run_cli_patch_proposal_command(parse_cli_patch_proposal_invocation(["patch-trace-preview"], surface), surface, context)
    assert trace_output.command_result.trace_packet_ref == "trace_packet:fixture:v0.35.7"
    assert trace_output.command_result.structured_result["ready_for_execution"] is False
    assert trace_output.command_result.structured_result["patch_application_allowed"] is False


def test_run_denied_command_returns_denied_output_without_execution() -> None:
    surface = build_default_cli_patch_proposal_surface()
    output = run_cli_patch_proposal_command(parse_cli_patch_proposal_invocation(["patch-apply"], surface), surface)
    assert output.status == CLIPatchProposalSurfaceStatus.BLOCKED
    assert output.denied_command is not None
    assert output.command_result is None
    assert output.ready_for_execution is False
    assert CLIPatchProposalRiskKind.PATCH_APPLY_RISK in output.denied_command.risk_kinds


def test_output_report_preview_guarantee_and_readiness_are_safe() -> None:
    result = build_cli_patch_proposal_command_result()
    output = build_cli_patch_proposal_run_output(command_result=result, rendered_output="bounded output")
    assert render_cli_patch_proposal_output(output, CLIPatchProposalOutputFormat.JSON).startswith("{")
    assert output.ready_for_execution is False

    report = build_cli_patch_proposal_run_report()
    assert report.ready_for_execution is False
    assert report.ready_for_patch_application is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_external_agent_execution is False
    assert report.ready_for_dominion_runtime is False
    assert report.ready_for_persistent_trace_write is False

    preview = build_cli_patch_proposal_run_preview()
    guarantee = build_cli_patch_proposal_no_external_side_effect_guarantee()
    readiness = build_v0358_readiness_report()
    assert preview.no_shell_execution_guarantee is True
    assert all(value is True for key, value in guarantee.__dict__.items() if key.startswith("no_"))
    assert v0358_readiness_report_is_not_execution_ready(readiness) is True
    assert readiness.ready_for_v0359_consolidation is True
    assert readiness.ready_for_cli_patch_proposal_surface is True
    assert readiness.ready_for_execution is False

    with pytest.raises(ValueError):
        build_cli_patch_proposal_run_output(rendered_output="x" * 1300)
    with pytest.raises(ValueError):
        build_cli_patch_proposal_command_result(ready_for_execution=True)
    with pytest.raises(ValueError):
        build_cli_patch_proposal_run_output(ready_for_execution=True)


def test_negative_decision_context_report_and_readiness_flags() -> None:
    for field in (
        "patch_application_allowed",
        "workspace_write_allowed",
        "code_edit_allowed",
        "apply_patch_allowed",
        "git_apply_allowed",
        "shell_execution_allowed",
        "subprocess_allowed",
        "command_execution_allowed",
        "test_execution_allowed",
        "dependency_install_allowed",
        "reference_execution_allowed",
        "reference_import_allowed",
        "external_agent_execution_allowed",
        "claude_code_invocation_allowed",
        "codex_cli_invocation_allowed",
        "dominion_runtime_allowed",
        "infinite_agent_loop_allowed",
        "provider_invocation_allowed",
        "network_access_allowed",
        "credential_access_allowed",
        "secret_read_allowed",
        "persistent_trace_write_allowed",
        "ui_runtime_allowed",
    ):
        with pytest.raises(ValueError):
            build_cli_patch_proposal_invocation_decision(**{field: True})

    for field in (
        "allows_patch_application",
        "allows_workspace_write",
        "allows_code_edit",
        "allows_shell",
        "allows_external_agent_execution",
        "allows_dominion_runtime",
    ):
        with pytest.raises(ValueError):
            build_cli_patch_proposal_runtime_context(**{field: True})

    for field in (
        "ready_for_execution",
        "ready_for_patch_application",
        "ready_for_workspace_write",
        "ready_for_shell_execution",
        "ready_for_external_agent_execution",
        "ready_for_dominion_runtime",
        "ready_for_persistent_trace_write",
    ):
        with pytest.raises(ValueError):
            build_cli_patch_proposal_run_report(**{field: True})

    for field in (
        "ready_for_execution",
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
        "ready_for_persistent_trace_write",
        "production_certified",
    ):
        with pytest.raises(ValueError):
            build_v0358_readiness_report(**{field: True})


def test_helpers_do_not_use_runtime_side_effect_capabilities() -> None:
    source = inspect.getsource(cli_module)
    forbidden_tokens = (
        "import subprocess",
        "subprocess.",
        "os.system(",
        "shell=True",
        "from pathlib",
        "Path(",
        ".read_text(",
        ".read_bytes(",
        ".write_text(",
        ".write_bytes(",
        " open(",
        ".unlink(",
        ".rename(",
        ".chmod(",
        ".chown(",
        "import requests",
        "import httpx",
        "import urllib",
        "import aiohttp",
        "import socket",
        "os.environ",
        "eval(",
        "exec(",
        "importlib",
        "logging.",
        "json.dump(",
        "sqlite",
    )
    for token in forbidden_tokens:
        assert token not in source
