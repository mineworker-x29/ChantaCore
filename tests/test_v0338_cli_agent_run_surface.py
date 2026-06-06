import inspect

import pytest

from chanta_core.agent_runtime import (
    AgentActionProposalKind,
    AgentRuntimeSessionState,
    CLIAgentArgumentSpec,
    CLIAgentCommandKind,
    CLIAgentCommandMode,
    CLIAgentCommandSpec,
    CLIAgentDecisionKind,
    CLIAgentFlagSet,
    CLIAgentInputSourceKind,
    CLIAgentInvocationDecision,
    CLIAgentNoExternalSideEffectGuarantee,
    CLIAgentOutputFormat,
    CLIAgentReadinessLevel,
    CLIAgentRiskKind,
    CLIAgentRunPreview,
    CLIAgentSurfacePolicy,
    CLIAgentSurfaceStatus,
    V0338ReadinessReport,
    build_agent_action_decision,
    build_agent_action_proposal,
    build_agent_runtime_session,
    build_agent_runtime_session_snapshot,
    build_agent_step_execution_record,
    build_agent_step_output,
    build_cli_agent_argument_spec,
    build_cli_agent_command_result,
    build_cli_agent_command_spec,
    build_cli_agent_denied_command,
    build_cli_agent_flags,
    build_cli_agent_invocation,
    build_cli_agent_invocation_decision,
    build_cli_agent_no_external_side_effect_guarantee,
    build_cli_agent_run_output,
    build_cli_agent_run_preview,
    build_cli_agent_run_report,
    build_cli_agent_source_ref,
    build_cli_agent_surface,
    build_cli_agent_surface_policy,
    build_default_cli_agent_surface,
    build_v0338_readiness_report,
    cli_agent_flags_preserve_unsafe_runtime_false,
    cli_decision_preserves_no_external_side_effect,
    cli_invocation_is_not_shell_execution,
    cli_surface_is_not_shell,
    default_cli_agent_command_specs,
    default_cli_agent_surface_policy,
    default_workspace_inspection_path_policy,
    evaluate_cli_agent_invocation,
    parse_cli_agent_invocation,
    render_cli_agent_output,
    run_cli_agent_command,
    v0338_readiness_report_is_not_general_runtime_ready,
)
from chanta_core.agent_runtime import cli_surface
from chanta_core.agent_runtime.cli_surface import (
    DEFAULT_V0338_PROHIBITED_UNTIL_LATER_GATE,
    UNSAFE_CLI_FLAG_NAMES,
)
from chanta_core.agent_runtime.step_runner import AgentStepResultKind, AgentStepStatus


def _fake_step_output():
    proposal = build_agent_action_proposal(
        "proposal:trace",
        AgentActionProposalKind.FINAL_RESPONSE,
        model_output_id="model_output:trace",
        proposed_final_response="Trace preview response.",
    )
    decision = build_agent_action_decision(
        "decision:trace",
        proposal.proposal_id,
        "allow_final_response",
        reason="Final response from supplied/mock output only.",
    )
    record = build_agent_step_execution_record(
        "record:trace",
        "step_input:trace",
        AgentStepStatus.RESPONSE_READY,
        executed_bounded_step=True,
    )
    return build_agent_step_output(
        "step_output:trace",
        "step_input:trace",
        AgentStepStatus.RESPONSE_READY,
        AgentStepResultKind.FINAL_RESPONSE_RESULT,
        record,
        action_proposal=proposal,
        action_decision=decision,
        final_response_text="Trace preview response.",
    )


def test_cli_taxonomies_and_flags_are_conservative():
    assert "agent_help" in {item.value for item in CLIAgentCommandKind}
    assert "readonly_inspection" in {item.value for item in CLIAgentCommandMode}
    assert "argv_list" in {item.value for item in CLIAgentInputSourceKind}
    assert "completed_with_skips" in {item.value for item in CLIAgentSurfaceStatus}
    assert "allow_trace_preview" in {item.value for item in CLIAgentDecisionKind}
    assert "json" in {item.value for item in CLIAgentOutputFormat}
    assert "shell_injection_risk" in {item.value for item in CLIAgentRiskKind}
    assert "bounded_cli_command_dispatch_ready" in {item.value for item in CLIAgentReadinessLevel}

    flags = build_cli_agent_flags(
        cli_surface_constructed=True,
        cli_argument_parsing_enabled=True,
        bounded_cli_command_dispatch_enabled=True,
        ready_for_v0339_consolidation=True,
        ready_for_bounded_cli_agent_run=True,
        ready_for_bounded_agent_step_execution=True,
        ready_for_safe_readonly_tool_execution=True,
        ready_for_safe_workspace_inspection_execution=True,
        ready_for_bounded_internal_ocel_trace_emission=True,
    )

    assert flags.ready_for_bounded_cli_agent_run is True
    assert flags.ready_for_bounded_agent_step_execution is True
    assert flags.ready_for_safe_workspace_inspection_execution is True
    assert flags.ready_for_bounded_internal_ocel_trace_emission is True
    assert flags.ready_for_execution is False
    assert flags.ready_for_shell_execution is False
    assert flags.ready_for_subprocess_execution is False
    assert flags.ready_for_real_model_invocation is False
    assert flags.ready_for_provider_invocation is False
    assert flags.ready_for_general_agent_execution is False
    assert flags.ready_for_general_tool_execution is False
    assert flags.ready_for_persistent_trace_write is False
    assert cli_agent_flags_preserve_unsafe_runtime_false(flags)

    for flag_name in UNSAFE_CLI_FLAG_NAMES:
        with pytest.raises(ValueError):
            CLIAgentFlagSet(flag_set_id=f"flags:bad:{flag_name}", version="v0.33.8", **{flag_name: True})


def test_source_argument_command_policy_and_surface_contracts_are_safe():
    source = build_cli_agent_source_ref(
        "source:argv",
        CLIAgentInputSourceKind.ARGV_LIST,
        "argv",
        "CLI argv fixture.",
    )
    arg_spec = build_cli_agent_argument_spec(
        "arg:path",
        "--path",
        required=True,
        allow_path_value=True,
        description="Safe path reference.",
    )
    command_spec = build_cli_agent_command_spec(
        "command:read",
        CLIAgentCommandKind.AGENT_READ_TEXT_FILE_SAFE,
        "read-text",
        argument_specs=[arg_spec],
    )
    policy = default_cli_agent_surface_policy()
    surface = build_default_cli_agent_surface()

    assert source.shell_command is False
    assert source.provider_call is False
    assert source.file_read is False
    assert isinstance(arg_spec, CLIAgentArgumentSpec)
    assert isinstance(command_spec, CLIAgentCommandSpec)
    assert command_spec.os_command is False
    assert policy.allow_shell is False
    assert policy.allow_subprocess is False
    assert policy.allow_real_model_invocation is False
    assert policy.allow_provider_invocation is False
    assert policy.allow_general_tool_execution is False
    assert policy.allow_safe_workspace_inspection is True
    assert policy.allow_bounded_agent_step is True
    assert policy.allow_bounded_trace_preview is True
    assert policy.allow_workspace_write is False
    assert policy.allow_network_access is False
    assert policy.allow_credential_access is False
    assert policy.allow_persistent_trace_write is False
    assert cli_surface_is_not_shell(surface)

    with pytest.raises(ValueError):
        build_cli_agent_source_ref("source:bad", metadata={"shell": True})
    with pytest.raises(ValueError):
        CLIAgentSurfacePolicy(policy_id="policy:bad:shell", allow_shell=True)
    with pytest.raises(ValueError):
        CLIAgentSurfacePolicy(policy_id="policy:bad:provider", allow_provider_invocation=True)
    with pytest.raises(ValueError):
        build_cli_agent_command_spec("command:bad", CLIAgentCommandKind.UNKNOWN, "unknown", enabled=True)


def test_parse_and_evaluate_safe_and_unsafe_invocations():
    surface = build_default_cli_agent_surface()
    help_invocation = parse_cli_agent_invocation(["agent", "help"], surface)
    status_invocation = parse_cli_agent_invocation(["agent", "status", "--format", "json"], surface)
    inspect_invocation = parse_cli_agent_invocation(["agent", "inspect-path", "--path", "safe.txt"], surface)
    tree_invocation = parse_cli_agent_invocation(["agent", "inspect-tree", "--path", "."], surface)
    read_invocation = parse_cli_agent_invocation(["agent", "read-text", "--path", "safe.txt"], surface)
    search_invocation = parse_cli_agent_invocation(["agent", "search", "--path", ".", "--query", "needle"], surface)
    reference_invocation = parse_cli_agent_invocation(["agent", "reference-summary", "--path", "references/OpenCode"], surface)
    step_invocation = parse_cli_agent_invocation(["agent", "step", "--supplied-output", '{"kind":"final_response","final_response":"ok"}'], surface)
    mock_step_invocation = parse_cli_agent_invocation(["agent", "step", "--mock-output", '{"kind":"final_response","final_response":"ok"}'], surface)
    trace_invocation = parse_cli_agent_invocation(["agent", "trace-preview", "--from-step-output"], surface)
    no_op_invocation = parse_cli_agent_invocation(["agent", "no-op"], surface)
    unknown_invocation = parse_cli_agent_invocation(["agent", "does-not-exist"], surface)
    shell_invocation = parse_cli_agent_invocation(["agent", "status;whoami"], surface)
    provider_invocation = parse_cli_agent_invocation(["agent", "provider"], surface)
    write_invocation = parse_cli_agent_invocation(["agent", "write", "--path", "x"], surface)

    assert help_invocation.command_kind == CLIAgentCommandKind.AGENT_HELP
    assert status_invocation.requested_output_format == CLIAgentOutputFormat.JSON
    assert inspect_invocation.command_kind == CLIAgentCommandKind.AGENT_INSPECT_PATH_READONLY
    assert tree_invocation.command_kind == CLIAgentCommandKind.AGENT_INSPECT_TREE_READONLY
    assert read_invocation.command_kind == CLIAgentCommandKind.AGENT_READ_TEXT_FILE_SAFE
    assert search_invocation.command_kind == CLIAgentCommandKind.AGENT_SEARCH_WORKSPACE_READONLY
    assert reference_invocation.command_kind == CLIAgentCommandKind.AGENT_REFERENCE_SUMMARY_READONLY
    assert step_invocation.command_kind == CLIAgentCommandKind.AGENT_STEP_WITH_SUPPLIED_OUTPUT
    assert mock_step_invocation.command_kind == CLIAgentCommandKind.AGENT_STEP_WITH_MOCK_OUTPUT
    assert trace_invocation.command_kind == CLIAgentCommandKind.AGENT_TRACE_PREVIEW_FROM_STEP_OUTPUT
    assert no_op_invocation.command_kind == CLIAgentCommandKind.AGENT_NO_OP
    assert cli_invocation_is_not_shell_execution(help_invocation)

    assert evaluate_cli_agent_invocation(help_invocation, surface).decision_kind == CLIAgentDecisionKind.ALLOW_HELP
    assert evaluate_cli_agent_invocation(inspect_invocation, surface).safe_workspace_inspection_allowed is True
    assert evaluate_cli_agent_invocation(step_invocation, surface).bounded_agent_step_allowed is True
    assert evaluate_cli_agent_invocation(mock_step_invocation, surface).bounded_agent_step_allowed is True
    assert evaluate_cli_agent_invocation(trace_invocation, surface).trace_preview_allowed is True
    assert evaluate_cli_agent_invocation(no_op_invocation, surface).decision_kind == CLIAgentDecisionKind.NO_OP
    assert evaluate_cli_agent_invocation(unknown_invocation, surface).decision_kind == CLIAgentDecisionKind.BLOCK
    assert evaluate_cli_agent_invocation(shell_invocation, surface).decision_kind == CLIAgentDecisionKind.BLOCK
    assert evaluate_cli_agent_invocation(provider_invocation, surface).decision_kind == CLIAgentDecisionKind.BLOCK
    assert evaluate_cli_agent_invocation(write_invocation, surface).decision_kind == CLIAgentDecisionKind.BLOCK

    for invocation in (unknown_invocation, shell_invocation, provider_invocation, write_invocation):
        decision = evaluate_cli_agent_invocation(invocation, surface)
        assert cli_decision_preserves_no_external_side_effect(decision)
        assert decision.shell_execution_allowed is False
        assert decision.subprocess_allowed is False
        assert decision.provider_invocation_allowed is False
        assert decision.general_tool_execution_allowed is False
        assert decision.workspace_write_allowed is False
        assert decision.persistent_trace_write_allowed is False


def test_run_cli_safe_workspace_inspection_step_and_trace_preview(tmp_path):
    safe_file = tmp_path / "safe.txt"
    safe_file.write_text("needle from v0338 safe file", encoding="utf-8")
    secret_file = tmp_path / "token.txt"
    secret_file.write_text("TOKEN=not returned", encoding="utf-8")
    surface = build_default_cli_agent_surface()
    workspace_policy = default_workspace_inspection_path_policy(tmp_path)

    inspect_output = run_cli_agent_command(
        parse_cli_agent_invocation(["agent", "inspect-path", "--path", str(safe_file)], surface),
        surface,
        {"workspace_policy": workspace_policy},
    )
    tree_output = run_cli_agent_command(
        parse_cli_agent_invocation(["agent", "inspect-tree", "--path", str(tmp_path)], surface),
        surface,
        {"workspace_policy": workspace_policy},
    )
    read_output = run_cli_agent_command(
        parse_cli_agent_invocation(["agent", "read-text", "--path", str(safe_file)], surface),
        surface,
        {"workspace_policy": workspace_policy},
    )
    search_output = run_cli_agent_command(
        parse_cli_agent_invocation(["agent", "search", "--path", str(tmp_path), "--query", "needle"], surface),
        surface,
        {"workspace_policy": workspace_policy},
    )
    secret_output = run_cli_agent_command(
        parse_cli_agent_invocation(["agent", "read-text", "--path", str(secret_file)], surface),
        surface,
        {"workspace_policy": workspace_policy},
    )
    step_output = run_cli_agent_command(
        parse_cli_agent_invocation(["agent", "step", "--mock-output", '{"kind":"final_response","final_response":"mock ok"}'], surface),
        surface,
        {"workspace_policy": workspace_policy},
    )
    fake_step = _fake_step_output()
    trace_output = run_cli_agent_command(
        parse_cli_agent_invocation(["agent", "trace-preview", "--from-step-output"], surface),
        surface,
        {"step_output": fake_step},
    )

    assert inspect_output.command_result is not None
    assert inspect_output.command_result.workspace_inspection_result_ref is not None
    assert tree_output.command_result is not None
    assert read_output.command_result is not None
    assert search_output.command_result is not None
    assert secret_output.status in {CLIAgentSurfaceStatus.BLOCKED, CLIAgentSurfaceStatus.COMPLETED_WITH_SKIPS}
    assert "TOKEN=not returned" not in str(secret_output)
    assert step_output.command_result is not None
    assert step_output.command_result.agent_step_output_ref is not None
    assert "mock ok" not in step_output.rendered_output
    assert trace_output.command_result is not None
    assert trace_output.command_result.trace_packet_ref is not None
    assert "ready_for_persistent_write" in trace_output.rendered_output
    assert trace_output.ready_for_execution is False


def test_run_cli_denials_reports_preview_guarantee_and_readiness():
    surface = build_default_cli_agent_surface()
    missing_step = run_cli_agent_command(parse_cli_agent_invocation(["agent", "step"], surface), surface)
    unknown = run_cli_agent_command(parse_cli_agent_invocation(["agent", "unknown"], surface), surface)
    shell = run_cli_agent_command(parse_cli_agent_invocation(["agent", "status|whoami"], surface), surface)
    trace_without_artifact = run_cli_agent_command(parse_cli_agent_invocation(["agent", "trace-preview", "--from-step-output"], surface), surface)
    report = build_cli_agent_run_report(
        "report:1",
        invocation_id="invocation:1",
        run_output_id="output:1",
        command_count=1,
        allowed_count=1,
        ready_for_v0339_consolidation=True,
        ready_for_bounded_cli_agent_run=True,
    )
    preview = build_cli_agent_run_preview("preview:1", cli_surface_id=surface.cli_surface_id)
    guarantee = build_cli_agent_no_external_side_effect_guarantee("guarantee:1")
    readiness = build_v0338_readiness_report(
        "readiness:1",
        cli_surface_id=surface.cli_surface_id,
        cli_run_report_id=report.report_id,
        run_output_id="output:1",
        bounded_cli_surface_enabled=True,
        cli_argument_parsing_enabled=True,
        bounded_cli_command_dispatch_enabled=True,
        ready_for_v0339_consolidation=True,
        ready_for_bounded_cli_agent_run=True,
        ready_for_bounded_agent_step_execution=True,
        ready_for_safe_readonly_tool_execution=True,
        ready_for_safe_workspace_inspection_execution=True,
        ready_for_bounded_internal_ocel_trace_emission=True,
    )

    assert missing_step.denied_command is not None
    assert unknown.denied_command is not None
    assert shell.denied_command is not None
    assert trace_without_artifact.denied_command is not None
    assert report.ready_for_bounded_cli_agent_run is True
    assert report.ready_for_execution is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_subprocess_execution is False
    assert report.ready_for_real_model_invocation is False
    assert report.ready_for_provider_invocation is False
    assert report.ready_for_general_tool_execution is False
    assert report.ready_for_persistent_trace_write is False
    assert all(getattr(preview, name) is True for name in preview.__dataclass_fields__ if name.startswith("no_"))
    assert isinstance(preview, CLIAgentRunPreview)
    assert all(getattr(guarantee, name) is True for name in guarantee.__dataclass_fields__ if name.startswith("no_"))
    assert isinstance(guarantee, CLIAgentNoExternalSideEffectGuarantee)
    assert readiness.bounded_cli_surface_enabled is True
    assert readiness.cli_argument_parsing_enabled is True
    assert readiness.bounded_cli_command_dispatch_enabled is True
    assert readiness.ready_for_bounded_cli_agent_run is True
    assert readiness.ready_for_execution is False
    assert readiness.ready_for_shell_execution is False
    assert readiness.ready_for_subprocess_execution is False
    assert readiness.ready_for_real_model_invocation is False
    assert readiness.ready_for_provider_invocation is False
    assert readiness.ready_for_general_agent_execution is False
    assert readiness.ready_for_general_tool_execution is False
    assert readiness.ready_for_persistent_trace_write is False
    assert readiness.ready_for_ui_runtime is False
    assert v0338_readiness_report_is_not_general_runtime_ready(readiness)
    assert set(DEFAULT_V0338_PROHIBITED_UNTIL_LATER_GATE).issubset(set(readiness.prohibited_until_later_gate))

    for flag_name in UNSAFE_CLI_FLAG_NAMES:
        with pytest.raises(ValueError):
            V0338ReadinessReport(report_id=f"readiness:bad:{flag_name}", version="v0.33.8", **{flag_name: True})


def test_builder_helpers_and_rendering_are_bounded_artifacts():
    invocation = build_cli_agent_invocation(
        "invocation:manual",
        ["agent", "help"],
        CLIAgentCommandKind.AGENT_HELP,
        parsed_args={"command_token": "help"},
    )
    decision = build_cli_agent_invocation_decision(
        "decision:manual",
        invocation.invocation_id,
        CLIAgentDecisionKind.ALLOW_HELP,
        "manual help allowed",
        allowed_command_kind=CLIAgentCommandKind.AGENT_HELP,
    )
    denied = build_cli_agent_denied_command(
        "denied:manual",
        invocation_id=invocation.invocation_id,
        decision_id=decision.decision_id,
        command_kind=CLIAgentCommandKind.UNKNOWN,
    )
    result = build_cli_agent_command_result(
        "result:manual",
        invocation.invocation_id,
        decision.decision_id,
        CLIAgentCommandKind.AGENT_HELP,
        CLIAgentSurfaceStatus.COMPLETED,
        structured_result={"summary": "help"},
        text_summary="help summary",
    )
    output = build_cli_agent_run_output(
        "output:manual",
        invocation.invocation_id,
        "help summary",
        CLIAgentSurfaceStatus.COMPLETED,
        command_result=result,
        denied_command=None,
        output_format=CLIAgentOutputFormat.JSON,
        summary="manual output",
    )

    assert denied.reason
    assert result.ready_for_execution is False
    assert output.ready_for_execution is False
    assert render_cli_agent_output(output, CLIAgentOutputFormat.JSON).startswith("{")

    with pytest.raises(ValueError):
        build_cli_agent_run_output(
            "output:bad",
            invocation.invocation_id,
            "x" * 20,
            CLIAgentSurfaceStatus.COMPLETED,
            command_result=result,
            denied_command=None,
            output_format=CLIAgentOutputFormat.TEXT,
            summary="bad",
            metadata={"max_rendered_output_chars": 4},
        )
    with pytest.raises(ValueError):
        CLIAgentInvocationDecision(
            decision_id="decision:bad",
            invocation_id=invocation.invocation_id,
            decision_kind=CLIAgentDecisionKind.ALLOW_HELP,
            reason="bad",
            shell_execution_allowed=True,
        )


def test_runtime_static_negative_patterns_and_no_shell_provider_write_persistence():
    source = inspect.getsource(cli_surface)
    forbidden_fragments = [
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "requests.",
        "httpx.",
        "urllib.",
        "aiohttp.",
        "socket.",
        "eval(",
        "exec(",
        "importlib",
        "write_text(",
        "write_bytes(",
        "open(",
        "unlink(",
        ".rmdir(",
        ".mkdir(",
        ".rename(",
        "Path.replace(",
        ".chmod(",
        ".chown(",
        "shutil.",
        "sqlite",
        "logging.",
    ]
    assert not any(fragment in source for fragment in forbidden_fragments)

    readiness_true_fragments = [
        "ready_for_execution=True",
        "ready_for_shell_execution=True",
        "ready_for_subprocess_execution=True",
        "ready_for_real_model_invocation=True",
        "ready_for_provider_invocation=True",
        "ready_for_general_agent_execution=True",
        "ready_for_general_tool_execution=True",
        "ready_for_persistent_trace_write=True",
        "ready_for_ui_runtime=True",
    ]
    assert not any(fragment in source for fragment in readiness_true_fragments)
