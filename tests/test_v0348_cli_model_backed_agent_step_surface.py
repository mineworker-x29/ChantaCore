import inspect

import pytest

from chanta_core.agent_runtime import (
    CLIModelBackedArgumentSpec,
    CLIModelBackedCommandKind,
    CLIModelBackedCommandMode,
    CLIModelBackedCommandResult,
    CLIModelBackedCommandSpec,
    CLIModelBackedDecisionKind,
    CLIModelBackedFlagSet,
    CLIModelBackedInputSourceKind,
    CLIModelBackedInvocationDecision,
    CLIModelBackedNoExternalSideEffectGuarantee,
    CLIModelBackedOutputFormat,
    CLIModelBackedReadinessLevel,
    CLIModelBackedRiskKind,
    CLIModelBackedRunPreview,
    CLIModelBackedRuntimeContext,
    CLIModelBackedSourceRef,
    CLIModelBackedSurfacePolicy,
    CLIModelBackedSurfaceStatus,
    V0348ReadinessReport,
    build_agent_step_runner_mvp,
    build_cli_model_backed_argument_spec,
    build_cli_model_backed_command_result,
    build_cli_model_backed_command_spec,
    build_cli_model_backed_flags,
    build_cli_model_backed_invocation_decision,
    build_cli_model_backed_no_external_side_effect_guarantee,
    build_cli_model_backed_run_output,
    build_cli_model_backed_run_preview,
    build_cli_model_backed_run_report,
    build_cli_model_backed_runtime_context,
    build_cli_model_backed_source_ref,
    build_default_cli_model_backed_surface,
    build_existing_provider_boundary_adapter_descriptor,
    build_model_backed_step_execution_record,
    build_model_backed_step_output,
    build_v0348_readiness_report,
    cli_model_backed_decision_blocks_direct_provider,
    cli_model_backed_flags_preserve_unsafe_false,
    cli_model_backed_invocation_is_not_shell,
    cli_model_backed_surface_is_not_shell,
    default_cli_model_backed_command_specs,
    default_cli_model_backed_surface_policy,
    evaluate_cli_model_backed_invocation,
    parse_cli_model_backed_invocation,
    render_cli_model_backed_output,
    run_cli_model_backed_command,
    v0348_readiness_report_is_not_general_execution_ready,
)
from chanta_core.agent_runtime import model_cli_surface
from chanta_core.agent_runtime.model_backed_step import ModelBackedStepOutcomeKind, ModelBackedStepStatus
from chanta_core.agent_runtime.model_cli_surface import (
    DEFAULT_V0348_PROHIBITED_UNTIL_LATER_GATE,
    UNSAFE_CLI_MODEL_BACKED_FLAG_NAMES,
)


def _fake_step_output():
    record = build_model_backed_step_execution_record(
        "record:trace:v0348",
        step_input_id="step_input:trace:v0348",
        decision_id="decision:trace:v0348",
        status=ModelBackedStepStatus.BOUNDED_STEP_COMPLETED,
        executed_bounded_model_backed_step=True,
    )
    return build_model_backed_step_output(
        "output:trace:v0348",
        step_input_id="step_input:trace:v0348",
        status=ModelBackedStepStatus.BOUNDED_STEP_COMPLETED,
        outcome_kind=ModelBackedStepOutcomeKind.FINAL_RESPONSE_OUTPUT,
        final_response_text="trace response not persisted",
        execution_record=record,
        quarantine_packet_ref="packet:trace:v0348",
    )


def test_cli_model_backed_taxonomies_and_flags_are_conservative():
    assert "model_help" in {item.value for item in CLIModelBackedCommandKind}
    assert "controlled_model_step" in {item.value for item in CLIModelBackedCommandMode}
    assert "runtime_context" in {item.value for item in CLIModelBackedInputSourceKind}
    assert "future_gated" in {item.value for item in CLIModelBackedSurfaceStatus}
    assert "allow_controlled_model_step_via_existing_boundary" in {item.value for item in CLIModelBackedDecisionKind}
    assert "structured_artifact" in {item.value for item in CLIModelBackedOutputFormat}
    assert "provider_sdk_bypass_risk" in {item.value for item in CLIModelBackedRiskKind}
    assert "bounded_model_backed_command_dispatch_ready" in {item.value for item in CLIModelBackedReadinessLevel}

    flags = build_cli_model_backed_flags(
        cli_model_backed_surface_constructed=True,
        cli_argument_parsing_enabled=True,
        bounded_model_command_dispatch_enabled=True,
        ready_for_v0349_consolidation=True,
        ready_for_bounded_cli_model_backed_step=True,
        ready_for_cli_model_backed_surface=True,
        ready_for_bounded_model_backed_step_execution=True,
        ready_for_agent_step_runner_model_integration=True,
        ready_for_controlled_model_invocation=True,
        ready_for_existing_boundary_invocation=True,
        ready_for_model_invocation=True,
        ready_for_model_invocation_trace_packet_creation=True,
        ready_for_bounded_model_invocation_ocel_trace_emission=True,
    )

    assert flags.ready_for_bounded_cli_model_backed_step is True
    assert flags.ready_for_cli_model_backed_surface is True
    assert flags.ready_for_bounded_model_backed_step_execution is True
    assert flags.ready_for_controlled_model_invocation is True
    assert flags.ready_for_model_invocation_trace_packet_creation is True
    assert flags.ready_for_execution is False
    assert flags.ready_for_shell_execution is False
    assert flags.ready_for_direct_provider_invocation is False
    assert flags.ready_for_provider_sdk_invocation is False
    assert flags.ready_for_general_tool_execution is False
    assert flags.ready_for_persistent_trace_write is False
    assert cli_model_backed_flags_preserve_unsafe_false(flags)

    for flag_name in UNSAFE_CLI_MODEL_BACKED_FLAG_NAMES:
        with pytest.raises(ValueError):
            CLIModelBackedFlagSet(flag_set_id=f"flags:bad:{flag_name}", version="v0.34.8", **{flag_name: True})


def test_source_specs_policy_and_surface_are_not_shell_or_provider():
    source = build_cli_model_backed_source_ref(
        "source:argv:v0348",
        source_kind=CLIModelBackedInputSourceKind.ARGV_LIST,
        source_id="argv",
        source_summary="argv fixture",
    )
    arg_spec = build_cli_model_backed_argument_spec(
        "arg:prompt",
        "--prompt",
        allow_prompt_text=True,
        description="Bounded prompt arg.",
    )
    command_spec = build_cli_model_backed_command_spec(
        "command:request",
        CLIModelBackedCommandKind.REQUEST_ENVELOPE_PREVIEW,
        "request-envelope",
        argument_specs=[arg_spec],
    )
    policy = default_cli_model_backed_surface_policy()
    surface = build_default_cli_model_backed_surface()

    assert isinstance(source, CLIModelBackedSourceRef)
    assert source.shell_command is False
    assert source.provider_call is False
    assert source.file_read is False
    assert source.execution is False
    assert isinstance(arg_spec, CLIModelBackedArgumentSpec)
    assert isinstance(command_spec, CLIModelBackedCommandSpec)
    assert command_spec.os_command is False
    assert policy.allow_shell is False
    assert policy.allow_subprocess is False
    assert policy.allow_command_execution is False
    assert policy.allow_direct_provider_invocation is False
    assert policy.allow_provider_sdk_invocation is False
    assert policy.allow_direct_network_access is False
    assert policy.allow_credential_access is False
    assert policy.allow_secret_read is False
    assert policy.allow_bounded_model_backed_step is True
    assert policy.allow_controlled_model_step_via_existing_boundary is True
    assert policy.allow_general_agent_execution is False
    assert policy.allow_general_tool_execution is False
    assert policy.allow_workspace_write is False
    assert policy.allow_patch_proposal is False
    assert policy.allow_patch_application is False
    assert policy.allow_model_invocation_trace_preview is True
    assert policy.allow_persistent_trace_write is False
    assert cli_model_backed_surface_is_not_shell(surface)

    with pytest.raises(ValueError):
        build_cli_model_backed_source_ref("source:bad", metadata={"shell_execution": True})
    with pytest.raises(ValueError):
        CLIModelBackedSurfacePolicy(policy_id="policy:bad:shell", allow_shell=True)
    with pytest.raises(ValueError):
        CLIModelBackedSurfacePolicy(policy_id="policy:bad:provider", allow_direct_provider_invocation=True)
    with pytest.raises(ValueError):
        CLIModelBackedSurfacePolicy(policy_id="policy:bad:persistent", allow_persistent_trace_write=True)
    with pytest.raises(ValueError):
        build_cli_model_backed_command_spec("command:bad", CLIModelBackedCommandKind.UNKNOWN, "unknown", enabled=True)


def test_parse_and_evaluate_safe_and_unsafe_commands():
    surface = build_default_cli_model_backed_surface()
    cases = {
        "help": parse_cli_model_backed_invocation(["agent", "model-help"], surface),
        "status": parse_cli_model_backed_invocation(["agent", "model-status", "--format", "json"], surface),
        "dry": parse_cli_model_backed_invocation(["agent", "model-dry-run"], surface),
        "request": parse_cli_model_backed_invocation(["agent", "request-envelope", "--prompt", "hello"], surface),
        "sanitize": parse_cli_model_backed_invocation(["agent", "sanitize-response", "--response", "final answer"], surface),
        "quarantine": parse_cli_model_backed_invocation(["agent", "quarantine-response", "--response", "final answer"], surface),
        "ask_mock": parse_cli_model_backed_invocation(["agent", "ask", "--prompt", "q", "--mock-response", "mock answer"], surface),
        "ask_supplied": parse_cli_model_backed_invocation(["agent", "ask", "--prompt", "q", "--supplied-response", "supplied answer"], surface),
        "step_mock": parse_cli_model_backed_invocation(["agent", "step", "--model-backed", "--mock-response", "mock step"], surface),
        "step_supplied": parse_cli_model_backed_invocation(["agent", "step", "--model-backed", "--supplied-response", "supplied step"], surface),
        "controlled": parse_cli_model_backed_invocation(["agent", "step", "--controlled-model"], surface),
        "trace": parse_cli_model_backed_invocation(["agent", "trace-preview", "--from-model-step-output"], surface),
        "noop": parse_cli_model_backed_invocation(["agent", "no-op"], surface),
    }

    assert cases["help"].command_kind == CLIModelBackedCommandKind.MODEL_HELP
    assert cases["status"].requested_output_format == CLIModelBackedOutputFormat.JSON
    assert cases["request"].command_kind == CLIModelBackedCommandKind.REQUEST_ENVELOPE_PREVIEW
    assert cases["step_mock"].command_kind == CLIModelBackedCommandKind.MODEL_BACKED_STEP_WITH_MOCK_RESPONSE
    assert cases["controlled"].command_kind == CLIModelBackedCommandKind.MODEL_BACKED_STEP_WITH_CONTROLLED_MODEL
    assert cli_model_backed_invocation_is_not_shell(cases["help"])

    assert evaluate_cli_model_backed_invocation(cases["help"], surface).decision_kind == CLIModelBackedDecisionKind.ALLOW_HELP
    assert evaluate_cli_model_backed_invocation(cases["request"], surface).decision_kind == CLIModelBackedDecisionKind.ALLOW_REQUEST_ENVELOPE_PREVIEW
    assert evaluate_cli_model_backed_invocation(cases["sanitize"], surface).decision_kind == CLIModelBackedDecisionKind.ALLOW_RESPONSE_SANITIZE_PREVIEW
    assert evaluate_cli_model_backed_invocation(cases["quarantine"], surface).decision_kind == CLIModelBackedDecisionKind.ALLOW_RESPONSE_QUARANTINE_PREVIEW
    assert evaluate_cli_model_backed_invocation(cases["step_mock"], surface).bounded_model_backed_step_allowed is True
    assert evaluate_cli_model_backed_invocation(cases["trace"], surface).model_invocation_trace_preview_allowed is True
    assert evaluate_cli_model_backed_invocation(cases["noop"], surface).decision_kind == CLIModelBackedDecisionKind.NO_OP

    no_context = evaluate_cli_model_backed_invocation(cases["controlled"], surface)
    assert no_context.decision_kind == CLIModelBackedDecisionKind.FUTURE_GATE_REQUIRED

    runtime_context = build_cli_model_backed_runtime_context(
        has_model_backed_step_runner=True,
        has_existing_provider_boundary_adapter=True,
        has_provider_boundary_callable=True,
        allows_controlled_model_step=True,
        metadata={
            "provider_adapter": build_existing_provider_boundary_adapter_descriptor(),
            "provider_boundary_callable": lambda _input: "controlled model response",
            "agent_step_runner": build_agent_step_runner_mvp(),
        },
    )
    controlled_decision = evaluate_cli_model_backed_invocation(cases["controlled"], surface, runtime_context)
    assert controlled_decision.decision_kind == CLIModelBackedDecisionKind.ALLOW_CONTROLLED_MODEL_STEP_VIA_EXISTING_BOUNDARY
    assert controlled_decision.controlled_model_step_via_existing_boundary_allowed is True

    unsafe_invocations = [
        parse_cli_model_backed_invocation(["agent", "unknown"], surface),
        parse_cli_model_backed_invocation(["agent", "model-status;whoami"], surface),
        parse_cli_model_backed_invocation(["agent", "run", "OpenCode"], surface),
        parse_cli_model_backed_invocation(["agent", "install", "Hermes"], surface),
        parse_cli_model_backed_invocation(["agent", "write", "--path", "x"], surface),
        parse_cli_model_backed_invocation(["agent", "patch", "--file", "x"], surface),
        parse_cli_model_backed_invocation(["agent", "provider", "openai"], surface),
    ]
    for invocation in unsafe_invocations:
        decision = evaluate_cli_model_backed_invocation(invocation, surface)
        assert decision.decision_kind == CLIModelBackedDecisionKind.BLOCK
        assert cli_model_backed_decision_blocks_direct_provider(decision)


def test_run_cli_handlers_dispatch_to_bounded_v034_helpers_only():
    surface = build_default_cli_model_backed_surface()
    request_output = run_cli_model_backed_command(
        parse_cli_model_backed_invocation(["agent", "request-envelope", "--prompt", "bounded prompt"], surface),
        surface,
    )
    sanitize_output = run_cli_model_backed_command(
        parse_cli_model_backed_invocation(["agent", "sanitize-response", "--response", "final response"], surface),
        surface,
    )
    quarantine_output = run_cli_model_backed_command(
        parse_cli_model_backed_invocation(["agent", "quarantine-response", "--response", "final response"], surface),
        surface,
    )
    step_output = run_cli_model_backed_command(
        parse_cli_model_backed_invocation(["agent", "step", "--model-backed", "--mock-response", "mock final response"], surface),
        surface,
    )
    ask_output = run_cli_model_backed_command(
        parse_cli_model_backed_invocation(["agent", "ask", "--prompt", "q", "--supplied-response", "supplied final response"], surface),
        surface,
    )

    assert request_output.command_result is not None
    assert request_output.command_result.request_envelope_ref is not None
    assert sanitize_output.command_result is not None
    assert sanitize_output.command_result.response_envelope_ref is not None
    assert quarantine_output.command_result is not None
    assert quarantine_output.command_result.quarantine_packet_ref is not None
    assert step_output.command_result is not None
    assert step_output.command_result.model_backed_step_output_ref is not None
    assert ask_output.command_result is not None
    assert ask_output.command_result.model_backed_step_output_ref is not None
    assert "mock final response" not in step_output.rendered_output
    assert step_output.ready_for_execution is False

    blocked = run_cli_model_backed_command(parse_cli_model_backed_invocation(["agent", "model-status|whoami"], surface), surface)
    assert blocked.denied_command is not None
    assert blocked.status == CLIModelBackedSurfaceStatus.BLOCKED


def test_controlled_model_and_trace_preview_use_v0346_v0344_and_v0347_only():
    surface = build_default_cli_model_backed_surface()
    runtime_context = build_cli_model_backed_runtime_context(
        has_model_backed_step_runner=True,
        has_existing_provider_boundary_adapter=True,
        has_provider_boundary_callable=True,
        has_model_invocation_trace_emitter=True,
        allows_controlled_model_step=True,
        metadata={
            "provider_adapter": build_existing_provider_boundary_adapter_descriptor(),
            "provider_boundary_callable": lambda _input: "controlled response from safe boundary",
            "agent_step_runner": build_agent_step_runner_mvp(),
            "trace_emitter": None,
        },
    )
    controlled_output = run_cli_model_backed_command(
        parse_cli_model_backed_invocation(["agent", "step", "--controlled-model"], surface),
        surface,
        runtime_context,
    )
    trace_context = build_cli_model_backed_runtime_context(
        has_model_invocation_trace_emitter=True,
        metadata={"model_backed_step_output": _fake_step_output()},
    )
    trace_output = run_cli_model_backed_command(
        parse_cli_model_backed_invocation(["agent", "trace-preview", "--from-model-step-output"], surface),
        surface,
        trace_context,
    )
    trace_empty = run_cli_model_backed_command(
        parse_cli_model_backed_invocation(["agent", "trace-preview", "--from-model-step-output"], surface),
        surface,
    )

    assert controlled_output.command_result is not None
    assert controlled_output.command_result.model_backed_step_output_ref is not None
    assert controlled_output.command_result.structured_result["provider_boundary_result_ref"] is not None
    assert controlled_output.ready_for_execution is False
    assert trace_output.command_result is not None
    assert trace_output.command_result.trace_packet_ref is not None
    assert trace_output.command_result.structured_result["ready_for_persistent_write"] is False
    assert trace_empty.command_result is not None
    assert trace_empty.command_result.trace_packet_ref is not None


def test_reports_preview_guarantee_readiness_and_rendering_are_bounded():
    surface = build_default_cli_model_backed_surface()
    invocation = parse_cli_model_backed_invocation(["agent", "model-status", "--format", "json"], surface)
    decision = evaluate_cli_model_backed_invocation(invocation, surface)
    result = build_cli_model_backed_command_result(
        "result:manual:v0348",
        invocation.invocation_id,
        decision.decision_id,
        invocation.command_kind,
        CLIModelBackedSurfaceStatus.COMPLETED,
        structured_result={"summary": "ok"},
        text_summary="manual result",
    )
    output = build_cli_model_backed_run_output(
        "output:manual:v0348",
        invocation.invocation_id,
        "manual result",
        CLIModelBackedSurfaceStatus.COMPLETED,
        command_result=result,
        denied_command=None,
        output_format=CLIModelBackedOutputFormat.JSON,
        summary="manual output",
    )
    report = build_cli_model_backed_run_report(
        "report:manual:v0348",
        invocation_id=invocation.invocation_id,
        run_output_id=output.run_output_id,
        command_count=1,
        allowed_count=1,
        bounded_model_step_count=1,
        trace_preview_count=1,
        ready_for_v0349_consolidation=True,
        ready_for_bounded_cli_model_backed_step=True,
    )
    preview = build_cli_model_backed_run_preview(cli_surface_id=surface.cli_surface_id)
    guarantee = build_cli_model_backed_no_external_side_effect_guarantee()
    readiness = build_v0348_readiness_report(
        cli_surface_id=surface.cli_surface_id,
        cli_run_report_id=report.report_id,
        run_output_id=output.run_output_id,
        ready_for_v0349_consolidation=True,
    )

    assert isinstance(result, CLIModelBackedCommandResult)
    assert output.ready_for_execution is False
    assert render_cli_model_backed_output(output, CLIModelBackedOutputFormat.JSON).startswith("{")
    assert report.ready_for_bounded_cli_model_backed_step is True
    assert report.ready_for_execution is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_direct_provider_invocation is False
    assert report.ready_for_provider_sdk_invocation is False
    assert report.ready_for_general_tool_execution is False
    assert report.ready_for_persistent_trace_write is False
    assert all(getattr(preview, name) is True for name in preview.__dataclass_fields__ if name.startswith("no_"))
    assert isinstance(preview, CLIModelBackedRunPreview)
    assert all(getattr(guarantee, name) is True for name in guarantee.__dataclass_fields__ if name.startswith("no_"))
    assert isinstance(guarantee, CLIModelBackedNoExternalSideEffectGuarantee)
    assert readiness.ready_for_bounded_cli_model_backed_step is True
    assert readiness.ready_for_cli_model_backed_surface is True
    assert readiness.ready_for_v0349_consolidation is True
    assert readiness.ready_for_execution is False
    assert readiness.ready_for_shell_execution is False
    assert readiness.ready_for_direct_provider_invocation is False
    assert readiness.ready_for_provider_sdk_invocation is False
    assert readiness.ready_for_general_agent_execution is False
    assert readiness.ready_for_general_tool_execution is False
    assert readiness.ready_for_persistent_trace_write is False
    assert v0348_readiness_report_is_not_general_execution_ready(readiness)
    assert set(DEFAULT_V0348_PROHIBITED_UNTIL_LATER_GATE).issubset(set(readiness.prohibited_until_later_gate))

    for flag_name in UNSAFE_CLI_MODEL_BACKED_FLAG_NAMES:
        with pytest.raises(ValueError):
            V0348ReadinessReport(report_id=f"readiness:bad:{flag_name}", version="v0.34.8", **{flag_name: True})
    with pytest.raises(ValueError):
        CLIModelBackedInvocationDecision(
            decision_id="decision:bad:shell",
            invocation_id=invocation.invocation_id,
            decision_kind=CLIModelBackedDecisionKind.ALLOW_HELP,
            reason="bad",
            shell_execution_allowed=True,
        )
    with pytest.raises(ValueError):
        build_cli_model_backed_run_output(
            "output:bad:v0348",
            invocation.invocation_id,
            "x" * 20,
            CLIModelBackedSurfaceStatus.COMPLETED,
            command_result=result,
            denied_command=None,
            output_format=CLIModelBackedOutputFormat.TEXT,
            summary="bad",
            metadata={"max_rendered_output_chars": 4},
        )


def test_default_specs_and_static_negative_patterns():
    specs = default_cli_model_backed_command_specs()
    assert {spec.command_kind for spec in specs} >= {
        CLIModelBackedCommandKind.MODEL_HELP,
        CLIModelBackedCommandKind.MODEL_STATUS,
        CLIModelBackedCommandKind.REQUEST_ENVELOPE_PREVIEW,
        CLIModelBackedCommandKind.MODEL_BACKED_STEP_WITH_CONTROLLED_MODEL,
        CLIModelBackedCommandKind.MODEL_INVOCATION_TRACE_PREVIEW,
    }
    source = inspect.getsource(model_cli_surface)
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
        "rmdir(",
        "mkdir(",
        "rename(",
        "replace(",
        "chmod(",
        "chown(",
        "shutil.",
        "sqlite",
        "logging.",
        "os.environ",
        "dotenv",
    ]
    unsafe_true_fragments = [
        "ready_for_execution=True",
        "ready_for_shell_execution=True",
        "ready_for_subprocess_execution=True",
        "ready_for_command_execution=True",
        "ready_for_direct_provider_invocation=True",
        "ready_for_provider_sdk_invocation=True",
        "ready_for_direct_network_access=True",
        "ready_for_credential_access=True",
        "ready_for_general_agent_execution=True",
        "ready_for_general_tool_execution=True",
        "ready_for_workspace_write=True",
        "ready_for_code_edit=True",
        "ready_for_patch_proposal=True",
        "ready_for_patch_application=True",
        "ready_for_persistent_trace_write=True",
        "production_certified=True",
    ]
    assert not any(fragment in source for fragment in forbidden_fragments)
    assert not any(fragment in source for fragment in unsafe_true_fragments)
