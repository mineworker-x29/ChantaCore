import os

import pytest

from chanta_core.agent_runtime import (
    AgentActionDecision,
    AgentActionDecisionKind,
    AgentActionProposalKind,
    AgentModelStepBoundary,
    AgentSafeToolExecutionRequest,
    AgentSafeToolExecutionResult,
    AgentStepExecutionMode,
    AgentStepExecutionRecord,
    AgentStepFlagSet,
    AgentStepNoExternalSideEffectGuarantee,
    AgentStepOutput,
    AgentStepPlan,
    AgentStepReport,
    AgentStepResultKind,
    AgentStepRiskKind,
    AgentStepRunPreview,
    AgentStepSourceKind,
    AgentStepStatus,
    AgentStepToolExecutionPosture,
    AgentSuppliedModelOutput,
    V0336ReadinessReport,
    agent_step_decision_preserves_no_external_side_effect,
    agent_step_flags_preserve_unsafe_runtime_false,
    agent_step_output_is_not_persistence,
    agent_step_runner_is_not_autonomous_runtime,
    build_agent_action_decision,
    build_agent_action_proposal,
    build_agent_model_step_boundary,
    build_agent_safe_tool_execution_request,
    build_agent_safe_tool_execution_result,
    build_agent_step_execution_record,
    build_agent_step_flags,
    build_agent_step_input,
    build_agent_step_no_external_side_effect_guarantee,
    build_agent_step_output,
    build_agent_step_plan,
    build_agent_step_report,
    build_agent_step_run_preview,
    build_agent_step_runner_mvp,
    build_agent_step_source_ref,
    build_agent_supplied_model_output,
    build_safe_workspace_inspection_request_from_action,
    build_v0336_readiness_report,
    default_workspace_inspection_path_policy,
    evaluate_agent_action_proposal,
    execute_safe_workspace_tool_from_decision,
    parse_agent_action_proposal_from_supplied_output,
    run_agent_step_mvp,
    v0336_readiness_report_is_not_general_runtime_ready,
)
from chanta_core.agent_runtime.step_runner import (
    DEFAULT_AGENT_STEP_PROHIBITED_ACTIONS,
    SAFE_WORKSPACE_TOOL_NAMES,
    UNSAFE_STEP_FLAG_NAMES,
)


def test_agent_step_taxonomies_and_flags_are_conservative():
    assert "supplied_model_output_only" in {item.value for item in AgentStepExecutionMode}
    assert "safe_tool_executed" in {item.value for item in AgentStepStatus}
    assert "supplied_model_output" in {item.value for item in AgentStepSourceKind}
    assert "read_text_file_safe" in {item.value for item in AgentActionProposalKind}
    assert "allow_safe_workspace_inspection" in {item.value for item in AgentActionDecisionKind}
    assert "provider_invocation_risk" in {item.value for item in AgentStepRiskKind}
    assert "safe_tool_result" in {item.value for item in AgentStepResultKind}
    assert "safe_workspace_inspection_only" in {item.value for item in AgentStepToolExecutionPosture}

    flags = build_agent_step_flags(
        agent_step_runner_constructed=True,
        bounded_agent_step_execution_enabled=True,
        supplied_model_output_processing_enabled=True,
        mock_model_output_processing_enabled=True,
        safe_workspace_tool_bridge_enabled=True,
        ready_for_v0337_runtime_ocel_trace_emitter=True,
        ready_for_v0338_cli_agent_run_surface=True,
        ready_for_safe_readonly_tool_execution=True,
        ready_for_safe_workspace_inspection_execution=True,
    )

    assert flags.bounded_agent_step_execution_enabled is True
    assert flags.supplied_model_output_processing_enabled is True
    assert flags.mock_model_output_processing_enabled is True
    assert flags.safe_workspace_tool_bridge_enabled is True
    assert flags.ready_for_execution is False
    assert flags.ready_for_general_agent_execution is False
    assert flags.ready_for_real_model_invocation is False
    assert flags.ready_for_provider_invocation is False
    assert flags.ready_for_general_tool_execution is False
    assert agent_step_flags_preserve_unsafe_runtime_false(flags)

    for flag_name in UNSAFE_STEP_FLAG_NAMES:
        with pytest.raises(ValueError):
            AgentStepFlagSet(
                flag_set_id=f"flags:bad:{flag_name}",
                version="v0.33.6",
                **{flag_name: True},
            )


def test_source_model_boundary_and_supplied_output_are_not_provider_invocation():
    source = build_agent_step_source_ref(
        "source:mock",
        AgentStepSourceKind.MOCK_MODEL_OUTPUT,
        "mock:1",
        "Mock model output fixture.",
    )
    boundary = build_agent_model_step_boundary(
        "boundary:model",
        allow_supplied_model_output=True,
        allow_mock_model_output=True,
    )
    output = build_agent_supplied_model_output(
        "model_output:1",
        source_kind=AgentStepSourceKind.SUPPLIED_MODEL_OUTPUT,
        raw_text="Final answer from supplied fixture.",
        output_summary="Supplied fixture output.",
    )

    assert source.fetch is False
    assert source.file_read is False
    assert source.execution is False
    assert boundary.allow_real_provider_invocation is False
    assert boundary.allow_raw_model_output_persistence is False
    assert output.trusted is False
    assert output.provider_invocation is False

    with pytest.raises(ValueError):
        build_agent_step_source_ref(
            "source:bad",
            AgentStepSourceKind.OPENCODE_REFERENCE_CONTEXT_REF,
            "references/OpenCode",
            "bad",
            metadata={"execution": True},
        )
    with pytest.raises(ValueError):
        AgentModelStepBoundary(
            model_boundary_id="boundary:bad:provider",
            allow_real_provider_invocation=True,
        )
    with pytest.raises(ValueError):
        AgentModelStepBoundary(
            model_boundary_id="boundary:bad:persist",
            allow_raw_model_output_persistence=True,
        )
    with pytest.raises(ValueError):
        AgentSuppliedModelOutput(
            model_output_id="model_output:bad",
            raw_text="x",
            trusted=True,
        )


def test_parse_evaluate_and_decide_actions_without_external_side_effects():
    runner = build_agent_step_runner_mvp()
    final_output = build_agent_supplied_model_output(
        "model_output:final",
        structured_action={"kind": "final_response", "final_response": "Done from supplied output."},
    )
    tool_output = build_agent_supplied_model_output(
        "model_output:tool",
        structured_action={
            "kind": "read_text_file_safe",
            "tool_input": {"path_ref": "safe.txt"},
        },
    )
    prohibited_output = build_agent_supplied_model_output(
        "model_output:command",
        structured_action={"kind": "prohibited_command", "tool_input": {"command": "echo no"}},
    )

    final_proposal = parse_agent_action_proposal_from_supplied_output(final_output)
    final_decision = evaluate_agent_action_proposal(final_proposal, runner)
    tool_proposal = parse_agent_action_proposal_from_supplied_output(tool_output)
    tool_decision = evaluate_agent_action_proposal(tool_proposal, runner)
    blocked_proposal = parse_agent_action_proposal_from_supplied_output(prohibited_output)
    blocked_decision = evaluate_agent_action_proposal(blocked_proposal, runner)

    assert final_proposal.proposal_kind == AgentActionProposalKind.FINAL_RESPONSE
    assert final_proposal.execution is False
    assert final_decision.decision_kind == AgentActionDecisionKind.ALLOW_FINAL_RESPONSE
    assert final_decision.provider_invocation_allowed is False
    assert agent_step_decision_preserves_no_external_side_effect(final_decision)
    assert tool_proposal.proposal_kind == AgentActionProposalKind.READ_TEXT_FILE_SAFE
    assert tool_decision.decision_kind == AgentActionDecisionKind.ALLOW_SAFE_WORKSPACE_INSPECTION
    assert tool_decision.execution_allowed is True
    assert tool_decision.allowed_only_for_safe_workspace_inspection is True
    assert tool_decision.allowed_tool_name == "read_text_file_safe"
    assert blocked_decision.decision_kind == AgentActionDecisionKind.BLOCK
    assert AgentStepRiskKind.COMMAND_EXECUTION_RISK in blocked_decision.risk_kinds

    with pytest.raises(ValueError):
        AgentActionDecision(
            decision_id="decision:bad:provider",
            proposal_id="proposal:bad",
            decision_kind=AgentActionDecisionKind.ALLOW_FINAL_RESPONSE,
            reason="bad",
            provider_invocation_allowed=True,
        )
    with pytest.raises(ValueError):
        AgentActionDecision(
            decision_id="decision:bad:write",
            proposal_id="proposal:bad",
            decision_kind=AgentActionDecisionKind.ALLOW_FINAL_RESPONSE,
            reason="bad",
            workspace_write_allowed=True,
        )


def test_safe_tool_request_result_and_bridge_to_v0335_policy(tmp_path):
    safe_file = tmp_path / "safe.txt"
    safe_file.write_text("hello safe bridge", encoding="utf-8")
    secret_file = tmp_path / "token.txt"
    secret_file.write_text("TOKEN=not-read", encoding="utf-8")
    policy = default_workspace_inspection_path_policy(tmp_path)
    runner = build_agent_step_runner_mvp()
    output = build_agent_supplied_model_output(
        "model_output:read",
        structured_action={
            "kind": "read_text_file_safe",
            "tool_input": {"path_ref": str(safe_file)},
        },
    )
    proposal = parse_agent_action_proposal_from_supplied_output(output)
    decision = evaluate_agent_action_proposal(proposal, runner)
    workspace_request = build_safe_workspace_inspection_request_from_action(proposal, decision)
    safe_request = build_agent_safe_tool_execution_request(
        "safe_request:1",
        proposal.proposal_id,
        decision.decision_id,
        "read_text_file_safe",
        tool_input=dict(proposal.proposed_tool_input),
        ready_for_safe_workspace_inspection=True,
    )
    safe_result = execute_safe_workspace_tool_from_decision(proposal, decision, policy)

    assert workspace_request.path_ref == str(safe_file)
    assert safe_request.ready_for_general_tool_execution is False
    assert safe_request.ready_for_execution is False
    assert safe_result.bounded_readonly is True
    assert safe_result.ready_for_execution is False
    assert safe_result.skipped_or_denied is False

    secret_output = build_agent_supplied_model_output(
        "model_output:secret",
        structured_action={
            "kind": "read_text_file_safe",
            "tool_input": {"path_ref": str(secret_file)},
        },
    )
    secret_proposal = parse_agent_action_proposal_from_supplied_output(secret_output)
    secret_decision = evaluate_agent_action_proposal(secret_proposal, runner)
    secret_result = execute_safe_workspace_tool_from_decision(secret_proposal, secret_decision, policy)
    assert secret_result.skipped_or_denied is True
    assert "TOKEN=not-read" not in str(secret_result)

    with pytest.raises(ValueError):
        AgentSafeToolExecutionRequest(
            safe_tool_request_id="safe_request:bad",
            proposal_id=proposal.proposal_id,
            decision_id=decision.decision_id,
            tool_name="unsupported_tool",
        )
    with pytest.raises(ValueError):
        AgentSafeToolExecutionResult(
            safe_tool_result_id="safe_result:bad",
            safe_tool_request_id=safe_request.safe_tool_request_id,
            tool_name="read_text_file_safe",
            workspace_inspection_result_ref=None,
            result_summary="bad",
            bounded_readonly=False,
        )


def test_step_input_plan_record_output_report_and_runner_are_bounded_only():
    output = build_agent_supplied_model_output(
        "model_output:final",
        structured_action={"kind": "final_response", "final_response": "Ready."},
    )
    step_input = build_agent_step_input(
        "step_input:1",
        supplied_model_output=output,
        task_summary="Use supplied output only.",
    )
    plan = build_agent_step_plan(
        "plan:1",
        step_input.step_input_id,
        planned_actions=[AgentActionProposalKind.FINAL_RESPONSE],
        allowed_tool_names=sorted(SAFE_WORKSPACE_TOOL_NAMES),
        ready_for_bounded_step=True,
    )
    record = build_agent_step_execution_record(
        "record:1",
        step_input.step_input_id,
        AgentStepStatus.RESPONSE_READY,
        executed_bounded_step=True,
    )
    step_output = build_agent_step_output(
        "step_output:1",
        step_input.step_input_id,
        AgentStepStatus.RESPONSE_READY,
        AgentStepResultKind.FINAL_RESPONSE_RESULT,
        record,
        final_response_text="Ready.",
        ready_for_v0337_runtime_ocel_trace_emitter=True,
        ready_for_v0338_cli_agent_run_surface=True,
    )
    report = build_agent_step_report(
        "report:1",
        step_input.step_input_id,
        step_output_id=step_output.step_output_id,
        proposal_count=1,
        allowed_action_count=1,
        ready_for_v0337_runtime_ocel_trace_emitter=True,
        ready_for_v0338_cli_agent_run_surface=True,
    )
    runner = build_agent_step_runner_mvp()

    assert step_input.supplied_model_output is output
    assert plan.ready_for_bounded_step is True
    assert plan.ready_for_real_model_invocation is False
    assert plan.ready_for_general_tool_execution is False
    assert plan.ready_for_execution is False
    assert record.executed_bounded_step is True
    assert record.executed_real_model_call is False
    assert record.executed_general_tool_call is False
    assert record.executed_command is False
    assert record.wrote_workspace is False
    assert record.emitted_ocel is False
    assert step_output.ready_for_execution is False
    assert agent_step_output_is_not_persistence(step_output)
    assert report.ready_for_execution is False
    assert report.ready_for_general_agent_execution is False
    assert report.ready_for_real_model_invocation is False
    assert report.ready_for_provider_invocation is False
    assert report.ready_for_general_tool_execution is False
    assert agent_step_runner_is_not_autonomous_runtime(runner)

    with pytest.raises(ValueError):
        build_agent_step_input("step_input:bad", task_summary="missing output")
    for flag_name in (
        "executed_real_model_call",
        "executed_general_tool_call",
        "executed_command",
        "wrote_workspace",
        "emitted_ocel",
    ):
        with pytest.raises(ValueError):
            AgentStepExecutionRecord(
                execution_record_id=f"record:bad:{flag_name}",
                step_input_id=step_input.step_input_id,
                status=AgentStepStatus.COMPLETED,
                **{flag_name: True},
            )


def test_run_agent_step_mvp_final_safe_tool_and_blocked_paths(tmp_path):
    safe_file = tmp_path / "safe.txt"
    safe_file.write_text("step runner safe read", encoding="utf-8")
    policy = default_workspace_inspection_path_policy(tmp_path)
    runner = build_agent_step_runner_mvp()

    final_input = build_agent_step_input(
        "step_input:final",
        supplied_model_output=build_agent_supplied_model_output(
            "model_output:final",
            structured_action={"kind": "final_response", "final_response": "Final from fixture."},
        ),
    )
    final_output = run_agent_step_mvp(final_input, runner)

    tool_input = build_agent_step_input(
        "step_input:tool",
        supplied_model_output=build_agent_supplied_model_output(
            "model_output:tool",
            structured_action={
                "kind": "read_text_file_safe",
                "tool_input": {"path_ref": str(safe_file)},
            },
        ),
    )
    tool_output = run_agent_step_mvp(tool_input, runner, workspace_policy=policy)

    command_input = build_agent_step_input(
        "step_input:command",
        supplied_model_output=build_agent_supplied_model_output(
            "model_output:command",
            structured_action={"kind": "prohibited_command", "tool_input": {"command": "echo no"}},
        ),
    )
    command_output = run_agent_step_mvp(command_input, runner, workspace_policy=policy)

    assert final_output.result_kind == AgentStepResultKind.FINAL_RESPONSE_RESULT
    assert final_output.final_response_text == "Final from fixture."
    assert final_output.ready_for_execution is False
    assert tool_output.result_kind == AgentStepResultKind.SAFE_TOOL_RESULT
    assert tool_output.safe_tool_result is not None
    assert tool_output.safe_tool_result.bounded_readonly is True
    assert command_output.result_kind == AgentStepResultKind.BLOCKED_ACTION_RESULT
    assert command_output.action_decision is not None
    assert command_output.action_decision.command_execution_allowed is False
    assert command_output.execution_record.executed_command is False


def test_preview_guarantee_readiness_and_static_negative_patterns():
    preview = build_agent_step_run_preview("preview:1", runner_id="runner:1")
    guarantee = build_agent_step_no_external_side_effect_guarantee("guarantee:1")
    readiness = build_v0336_readiness_report(
        "readiness:1",
        runner_id="runner:1",
        bounded_agent_step_execution_enabled=True,
        supplied_model_output_processing_enabled=True,
        safe_workspace_tool_bridge_enabled=True,
        ready_for_v0337_runtime_ocel_trace_emitter=True,
        ready_for_v0338_cli_agent_run_surface=True,
        ready_for_safe_readonly_tool_execution=True,
        ready_for_safe_workspace_inspection_execution=True,
    )

    assert all(getattr(preview, name) is True for name in preview.__dataclass_fields__ if name.startswith("no_"))
    assert all(getattr(guarantee, name) is True for name in guarantee.__dataclass_fields__ if name.startswith("no_"))
    assert readiness.bounded_agent_step_execution_enabled is True
    assert readiness.supplied_model_output_processing_enabled is True
    assert readiness.safe_workspace_tool_bridge_enabled is True
    assert readiness.ready_for_execution is False
    assert readiness.ready_for_general_agent_execution is False
    assert readiness.ready_for_real_model_invocation is False
    assert readiness.ready_for_provider_invocation is False
    assert readiness.ready_for_general_tool_execution is False
    assert v0336_readiness_report_is_not_general_runtime_ready(readiness)
    assert set(DEFAULT_AGENT_STEP_PROHIBITED_ACTIONS).issubset(set(readiness.prohibited_until_later_gate))

    for flag_name in UNSAFE_STEP_FLAG_NAMES:
        with pytest.raises(ValueError):
            V0336ReadinessReport(
                report_id=f"readiness:bad:{flag_name}",
                version="v0.33.6",
                **{flag_name: True},
            )
    with pytest.raises(ValueError):
        AgentStepNoExternalSideEffectGuarantee(
            guarantee_id="guarantee:bad",
            version="v0.33.6",
            no_provider_invocation=False,
        )

    source_path = os.path.join("src", "chanta_core", "agent_runtime", "step_runner.py")
    with open(source_path, "r", encoding="utf-8") as handle:
        source = handle.read()
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
        "unlink(",
        "rmdir(",
        "mkdir(",
        "rename(",
        "replace(",
        "chmod(",
        "chown(",
        "shutil.",
    ]
    assert not any(fragment in source for fragment in forbidden_fragments)
