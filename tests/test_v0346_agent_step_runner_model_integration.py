import inspect

import pytest

from chanta_core.agent_runtime import (
    ModelBackedStepDecision,
    ModelBackedStepDecisionKind,
    ModelBackedStepExecutionRecord,
    ModelBackedStepFlagSet,
    ModelBackedStepInput,
    ModelBackedStepIntegrationMode,
    ModelBackedStepIntegrationPolicy,
    ModelBackedStepNoExternalSideEffectGuarantee,
    ModelBackedStepOutcomeKind,
    ModelBackedStepOutput,
    ModelBackedStepPlan,
    ModelBackedStepQuarantineBridge,
    ModelBackedStepReadinessLevel,
    ModelBackedStepReport,
    ModelBackedStepRiskKind,
    ModelBackedStepRouteKind,
    ModelBackedStepRunPreview,
    ModelBackedStepRunnerBridge,
    ModelBackedStepSourceKind,
    ModelBackedStepSourceRef,
    ModelBackedStepStatus,
    V0346ReadinessReport,
    build_agent_step_input_from_model_quarantine,
    build_agent_step_runner_mvp,
    build_existing_provider_boundary_adapter_descriptor,
    build_model_backed_step_decision,
    build_model_backed_step_execution_record,
    build_model_backed_step_flags,
    build_model_backed_step_input,
    build_model_backed_step_integration_policy,
    build_model_backed_step_no_external_side_effect_guarantee,
    build_model_backed_step_output,
    build_model_backed_step_plan,
    build_model_backed_step_quarantine_bridge,
    build_model_backed_step_report,
    build_model_backed_step_run_preview,
    build_model_backed_step_runner_bridge,
    build_model_backed_step_source_ref,
    build_model_output_action_candidate,
    build_model_output_action_quarantine_packet_from_candidates,
    build_model_response_envelope_from_supplied_text,
    build_v0346_readiness_report,
    decide_model_backed_step,
    default_model_backed_step_integration_policy,
    default_workspace_inspection_path_policy,
    model_backed_step_decision_blocks_unsafe,
    model_backed_step_execution_record_confirms_no_unsafe_side_effect,
    model_backed_step_flags_preserve_unsafe_false,
    model_backed_step_output_is_not_persistence,
    plan_model_backed_step,
    run_model_backed_agent_step,
    v0346_readiness_report_is_not_general_execution_ready,
)
from chanta_core.agent_runtime.model_backed_step import UNSAFE_MODEL_BACKED_STEP_FLAG_NAMES
from chanta_core.agent_runtime.model_output_quarantine import ModelOutputActionCandidateKind


def _packet_for_candidate(kind, preview="bounded preview", **kwargs):
    candidate = build_model_output_action_candidate(
        candidate_id=f"candidate:{kind}",
        candidate_kind=kind,
        candidate_preview=preview,
        candidate_summary=f"{kind} candidate",
        **kwargs,
    )
    return build_model_output_action_quarantine_packet_from_candidates([candidate])


def test_model_backed_step_taxonomies_exist():
    assert "response_envelope_only" in {item.value for item in ModelBackedStepIntegrationMode}
    assert "bounded_step_completed" in {item.value for item in ModelBackedStepStatus}
    assert "v0345_quarantine_packet" in {item.value for item in ModelBackedStepSourceKind}
    assert "allow_safe_workspace_inspection_step" in {item.value for item in ModelBackedStepDecisionKind}
    assert "safe_workspace_inspection_step_route" in {item.value for item in ModelBackedStepRouteKind}
    assert "patch_proposal_risk" in {item.value for item in ModelBackedStepRiskKind}
    assert "safe_workspace_inspection_output" in {item.value for item in ModelBackedStepOutcomeKind}
    assert "bounded_model_backed_step_ready" in {item.value for item in ModelBackedStepReadinessLevel}


def test_flags_allow_bounded_integration_but_preserve_unsafe_false():
    flags = build_model_backed_step_flags(
        model_backed_step_integration_constructed=True,
        quarantine_bridge_available=True,
        step_runner_bridge_available=True,
        bounded_model_backed_step_execution_available=True,
        ready_for_v0347_model_invocation_ocel_trace_packet=True,
        ready_for_v0348_cli_model_backed_agent_step_surface=True,
        ready_for_bounded_model_backed_step_execution=True,
        ready_for_agent_step_runner_model_integration=True,
        ready_for_safe_workspace_inspection_execution=True,
    )

    assert flags.ready_for_bounded_model_backed_step_execution is True
    assert flags.ready_for_agent_step_runner_model_integration is True
    assert flags.ready_for_execution is False
    assert flags.ready_for_direct_provider_invocation is False
    assert flags.ready_for_provider_sdk_invocation is False
    assert flags.ready_for_general_tool_execution is False
    assert flags.ready_for_patch_proposal is False
    assert model_backed_step_flags_preserve_unsafe_false(flags)

    for flag_name in UNSAFE_MODEL_BACKED_STEP_FLAG_NAMES:
        with pytest.raises(ValueError):
            ModelBackedStepFlagSet(
                flag_set_id=f"flags:bad:{flag_name}",
                version="v0.34.6",
                **{flag_name: True},
            )


def test_source_policy_input_plan_and_decision_are_conservative():
    source = build_model_backed_step_source_ref(
        "source:quarantine",
        ModelBackedStepSourceKind.V0345_QUARANTINE_PACKET,
        "packet:1",
        "Quarantine packet source.",
    )
    policy = default_model_backed_step_integration_policy(allow_existing_boundary_adapter_call=True)
    step_input = build_model_backed_step_input(
        "step_input:model",
        quarantine_packet_id="packet:1",
        agent_step_runner_id="runner:1",
        source_refs=[source],
    )
    plan = plan_model_backed_step(step_input, policy)
    packet = _packet_for_candidate(ModelOutputActionCandidateKind.FINAL_RESPONSE_CANDIDATE, "Ready.")
    decision = decide_model_backed_step(step_input, packet, policy)

    assert source.execution is False
    assert source.provider_call is False
    assert source.file_read is False
    assert policy.allow_existing_boundary_adapter_call is True
    assert policy.allow_direct_provider_invocation is False
    assert policy.allow_provider_sdk_invocation is False
    assert policy.allow_direct_network_access is False
    assert policy.allow_workspace_write is False
    assert policy.allow_patch_proposal is False
    assert step_input.integration_mode == ModelBackedStepIntegrationMode.QUARANTINE_PACKET_ONLY
    assert plan.ready_for_bounded_step is True
    assert plan.ready_for_general_execution is False
    assert decision.bounded_step_allowed is True
    assert decision.direct_provider_invocation_allowed is False
    assert decision.provider_sdk_allowed is False
    assert decision.network_allowed is False
    assert decision.workspace_write_allowed is False
    assert decision.patch_application_allowed is False
    assert model_backed_step_decision_blocks_unsafe(decision)

    with pytest.raises(ValueError):
        ModelBackedStepIntegrationPolicy(
            integration_policy_id="policy:bad:provider",
            allow_direct_provider_invocation=True,
        )
    with pytest.raises(ValueError):
        ModelBackedStepDecision(
            decision_id="decision:bad:write",
            step_input_id="step_input:bad",
            decision_kind=ModelBackedStepDecisionKind.ALLOW_NON_MUTATING_FINAL_RESPONSE_STEP,
            route_kind=ModelBackedStepRouteKind.FINAL_RESPONSE_STEP_ROUTE,
            reason="bad",
            workspace_write_allowed=True,
        )


def test_bridges_execution_record_output_and_reports_are_bounded():
    bridge = build_model_backed_step_quarantine_bridge(
        quarantine_packet_id="packet:1",
        selected_safe_route_id="route:1",
        selected_candidate_id="candidate:1",
        selected_route_kind=ModelBackedStepRouteKind.FINAL_RESPONSE_STEP_ROUTE,
        safe_route_available=True,
    )
    runner_bridge = build_model_backed_step_runner_bridge(
        called_v0336_runner=True,
        produced_bounded_output=True,
    )
    record = build_model_backed_step_execution_record(
        status=ModelBackedStepStatus.BOUNDED_STEP_COMPLETED,
        executed_bounded_model_backed_step=True,
    )
    output = build_model_backed_step_output(
        execution_record=record,
        final_response_text="Ready.",
        ready_for_v0347_model_invocation_ocel_trace_packet=True,
        ready_for_v0348_cli_model_backed_agent_step_surface=True,
    )
    report = build_model_backed_step_report(
        bounded_step_count=1,
        ready_for_bounded_model_backed_step_execution=True,
    )

    assert bridge.execution is False
    assert runner_bridge.called_v0336_runner is True
    assert runner_bridge.called_general_tool is False
    assert runner_bridge.called_shell is False
    assert runner_bridge.wrote_workspace is False
    assert record.executed_bounded_model_backed_step is True
    assert model_backed_step_execution_record_confirms_no_unsafe_side_effect(record)
    assert output.ready_for_execution is False
    assert model_backed_step_output_is_not_persistence(output)
    assert report.ready_for_bounded_model_backed_step_execution is True
    assert report.ready_for_general_execution is False

    for flag_name in (
        "executed_direct_provider_call",
        "executed_provider_sdk",
        "used_direct_network",
        "read_credentials",
        "read_secrets",
        "executed_general_tool",
        "executed_unquarantined_action",
        "executed_shell",
        "wrote_workspace",
        "generated_patch_proposal",
        "applied_patch",
        "persisted_raw_prompt",
        "persisted_raw_response",
    ):
        with pytest.raises(ValueError):
            ModelBackedStepExecutionRecord(
                execution_record_id=f"record:bad:{flag_name}",
                step_input_id="step_input:bad",
                decision_id="decision:bad",
                status=ModelBackedStepStatus.BLOCKED,
                summary="bad",
                **{flag_name: True},
            )
    with pytest.raises(ValueError):
        ModelBackedStepOutput(
            step_output_id="output:bad",
            step_input_id="step_input:bad",
            status=ModelBackedStepStatus.COMPLETED,
            outcome_kind=ModelBackedStepOutcomeKind.FINAL_RESPONSE_OUTPUT,
            final_response_text="x",
            ask_user_message=None,
            no_op_reason=None,
            blocked_reason=None,
            safe_fail_reason=None,
            agent_step_output_ref=None,
            provider_boundary_result_ref=None,
            quarantine_packet_ref=None,
            execution_record=record,
            summary="bad",
            ready_for_execution=True,
        )


def test_preview_guarantee_and_readiness_keep_general_execution_false():
    preview = build_model_backed_step_run_preview()
    guarantee = build_model_backed_step_no_external_side_effect_guarantee()
    readiness = build_v0346_readiness_report(
        ready_for_safe_workspace_inspection_execution=True,
    )

    assert all(getattr(preview, name) is True for name in preview.__dataclass_fields__ if name.startswith("no_"))
    assert all(getattr(guarantee, name) is True for name in guarantee.__dataclass_fields__ if name.startswith("no_"))
    assert readiness.ready_for_bounded_model_backed_step_execution is True
    assert readiness.ready_for_agent_step_runner_model_integration is True
    assert readiness.ready_for_safe_workspace_inspection_execution is True
    assert readiness.ready_for_execution is False
    assert readiness.ready_for_general_agent_execution is False
    assert readiness.ready_for_direct_provider_invocation is False
    assert readiness.ready_for_provider_sdk_invocation is False
    assert readiness.ready_for_general_tool_execution is False
    assert readiness.ready_for_patch_proposal is False
    assert v0346_readiness_report_is_not_general_execution_ready(readiness)

    for flag_name in UNSAFE_MODEL_BACKED_STEP_FLAG_NAMES:
        with pytest.raises(ValueError):
            V0346ReadinessReport(
                report_id=f"readiness:bad:{flag_name}",
                version="v0.34.6",
                **{flag_name: True},
            )


def test_final_ask_and_no_op_routes_run_one_bounded_step():
    runner = build_agent_step_runner_mvp()

    final_output = run_model_backed_agent_step(
        build_model_backed_step_input("step_input:final", quarantine_packet_id="packet:final"),
        quarantine_packet=_packet_for_candidate(ModelOutputActionCandidateKind.FINAL_RESPONSE_CANDIDATE, "Final answer."),
        agent_step_runner=runner,
    )
    ask_output = run_model_backed_agent_step(
        build_model_backed_step_input("step_input:ask", quarantine_packet_id="packet:ask"),
        quarantine_packet=_packet_for_candidate(ModelOutputActionCandidateKind.ASK_USER_CANDIDATE, "Need clarification."),
        agent_step_runner=runner,
    )
    no_op_output = run_model_backed_agent_step(
        build_model_backed_step_input("step_input:noop", quarantine_packet_id="packet:noop"),
        quarantine_packet=_packet_for_candidate(ModelOutputActionCandidateKind.NO_OP_CANDIDATE, "Nothing to do."),
        agent_step_runner=runner,
    )

    assert final_output.outcome_kind == ModelBackedStepOutcomeKind.FINAL_RESPONSE_OUTPUT
    assert final_output.final_response_text == "Final answer."
    assert final_output.execution_record.executed_bounded_model_backed_step is True
    assert ask_output.outcome_kind == ModelBackedStepOutcomeKind.ASK_USER_OUTPUT
    assert ask_output.ask_user_message == "Need clarification."
    assert no_op_output.outcome_kind == ModelBackedStepOutcomeKind.NO_OP_OUTPUT
    assert no_op_output.no_op_reason is not None
    assert final_output.ready_for_execution is False


def test_safe_workspace_inspection_route_uses_v0336_and_v0335_path(tmp_path):
    safe_file = tmp_path / "safe.txt"
    safe_file.write_text("bounded safe read", encoding="utf-8")
    packet = _packet_for_candidate(
        ModelOutputActionCandidateKind.SAFE_WORKSPACE_INSPECTION_CANDIDATE,
        "read safe file",
        metadata={
            "tool_name": "read_text_file_safe",
            "tool_input": {"path_ref": str(safe_file)},
        },
    )
    step_input = build_model_backed_step_input("step_input:safe", quarantine_packet_id=packet.quarantine_packet_id)
    agent_input = build_agent_step_input_from_model_quarantine(step_input, packet)
    output = run_model_backed_agent_step(
        step_input,
        quarantine_packet=packet,
        agent_step_runner=build_agent_step_runner_mvp(),
        workspace_policy=default_workspace_inspection_path_policy(tmp_path),
    )

    assert agent_input.supplied_model_output is not None
    assert agent_input.supplied_model_output.structured_action["kind"] == "read_text_file_safe"
    assert output.outcome_kind == ModelBackedStepOutcomeKind.SAFE_WORKSPACE_INSPECTION_OUTPUT
    assert output.execution_record.executed_bounded_model_backed_step is True
    assert output.execution_record.executed_general_tool is False
    assert output.execution_record.wrote_workspace is False
    assert output.ready_for_execution is False


def test_unsafe_missing_quarantine_and_missing_runner_paths_block():
    unsafe_packet = _packet_for_candidate(ModelOutputActionCandidateKind.SHELL_COMMAND_CANDIDATE, "rm -rf no")
    unsafe_output = run_model_backed_agent_step(
        build_model_backed_step_input("step_input:unsafe", quarantine_packet_id=unsafe_packet.quarantine_packet_id),
        quarantine_packet=unsafe_packet,
        agent_step_runner=build_agent_step_runner_mvp(),
    )
    missing_quarantine_output = run_model_backed_agent_step(build_model_backed_step_input("step_input:missing"))
    missing_runner_output = run_model_backed_agent_step(
        build_model_backed_step_input("step_input:no_runner", quarantine_packet_id="packet:no_runner"),
        quarantine_packet=_packet_for_candidate(ModelOutputActionCandidateKind.FINAL_RESPONSE_CANDIDATE, "Ready."),
    )

    assert unsafe_output.outcome_kind == ModelBackedStepOutcomeKind.BLOCKED_OUTPUT
    assert unsafe_output.execution_record.executed_bounded_model_backed_step is False
    assert missing_quarantine_output.outcome_kind == ModelBackedStepOutcomeKind.BLOCKED_OUTPUT
    assert "quarantine" in (missing_quarantine_output.blocked_reason or "").lower()
    assert missing_runner_output.outcome_kind == ModelBackedStepOutcomeKind.FUTURE_GATED_OUTPUT
    assert missing_runner_output.execution_record.executed_bounded_model_backed_step is False


def test_response_envelope_and_fake_provider_adapter_paths_are_quarantined():
    response_envelope = build_model_response_envelope_from_supplied_text("Response from sanitized envelope.")
    response_output = run_model_backed_agent_step(
        build_model_backed_step_input("step_input:response", response_envelope_id=response_envelope.response_envelope_id),
        response_envelope=response_envelope,
        agent_step_runner=build_agent_step_runner_mvp(),
    )

    policy = default_model_backed_step_integration_policy(
        allowed_modes=[
            ModelBackedStepIntegrationMode.EXISTING_BOUNDARY_THEN_QUARANTINE,
            ModelBackedStepIntegrationMode.QUARANTINE_PACKET_ONLY,
        ],
        allow_existing_boundary_adapter_call=True,
    )
    provider_output = run_model_backed_agent_step(
        build_model_backed_step_input(
            "step_input:provider",
            integration_mode=ModelBackedStepIntegrationMode.EXISTING_BOUNDARY_THEN_QUARANTINE,
            request_envelope_id="request:1",
        ),
        policy=policy,
        provider_adapter=build_existing_provider_boundary_adapter_descriptor(),
        provider_boundary_callable=lambda _invocation_input: "Provider adapter response.",
        agent_step_runner=build_agent_step_runner_mvp(),
    )
    blocked_provider_output = run_model_backed_agent_step(
        build_model_backed_step_input(
            "step_input:provider_blocked",
            integration_mode=ModelBackedStepIntegrationMode.EXISTING_BOUNDARY_THEN_QUARANTINE,
            request_envelope_id="request:2",
        ),
        provider_adapter=build_existing_provider_boundary_adapter_descriptor(),
        provider_boundary_callable=lambda _invocation_input: "Should not be called.",
        agent_step_runner=build_agent_step_runner_mvp(),
    )

    assert response_output.outcome_kind == ModelBackedStepOutcomeKind.FINAL_RESPONSE_OUTPUT
    assert provider_output.outcome_kind == ModelBackedStepOutcomeKind.FINAL_RESPONSE_OUTPUT
    assert provider_output.provider_boundary_result_ref is not None
    assert provider_output.execution_record.executed_existing_boundary_adapter_call is True
    assert provider_output.execution_record.executed_direct_provider_call is False
    assert blocked_provider_output.outcome_kind == ModelBackedStepOutcomeKind.BLOCKED_OUTPUT
    assert blocked_provider_output.execution_record.executed_existing_boundary_adapter_call is False


def test_static_implementation_has_no_forbidden_runtime_patterns():
    from chanta_core.agent_runtime import model_backed_step

    source = inspect.getsource(model_backed_step)
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
        "os.environ",
        "dotenv",
    ]
    unsafe_true_fragments = [
        "ready_for_execution=True",
        "ready_for_general_agent_execution=True",
        "ready_for_autonomous_agent_runtime=True",
        "ready_for_direct_provider_invocation=True",
        "ready_for_provider_sdk_invocation=True",
        "ready_for_direct_network_access=True",
        "ready_for_credential_access=True",
        "ready_for_general_tool_execution=True",
        "ready_for_unquarantined_action_execution=True",
        "ready_for_workspace_write=True",
        "ready_for_code_edit=True",
        "ready_for_patch_proposal=True",
        "ready_for_patch_application=True",
    ]
    assert not any(fragment in source for fragment in forbidden_fragments)
    assert not any(fragment in source for fragment in unsafe_true_fragments)
