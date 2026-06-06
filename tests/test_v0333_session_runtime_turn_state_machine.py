import pytest

from chanta_core.agent_runtime import (
    AgentRuntimeFailureKind,
    AgentRuntimeFailureRecord,
    AgentRuntimeNoSideEffectGuarantee,
    AgentRuntimeReadinessLevel,
    AgentRuntimeRunPreview,
    AgentRuntimeSession,
    AgentRuntimeSessionBoundaryView,
    AgentRuntimeSessionFlagSet,
    AgentRuntimeSessionReport,
    AgentRuntimeSessionSnapshot,
    AgentRuntimeSessionState,
    AgentRuntimeSourceKind,
    AgentRuntimeSourceRef,
    AgentRuntimeStateMachine,
    AgentRuntimeStateTransition,
    AgentRuntimeStep,
    AgentRuntimeStepKind,
    AgentRuntimeTerminalOutcomeKind,
    AgentRuntimeTransitionDecision,
    AgentRuntimeTransitionDecisionKind,
    AgentRuntimeTransitionKind,
    AgentRuntimeTransitionRequest,
    AgentRuntimeTurn,
    AgentRuntimeTurnState,
    V0333ReadinessReport,
    agent_runtime_flags_preserve_runtime_false,
    agent_runtime_session_is_not_execution,
    agent_runtime_snapshot_is_not_persistence,
    agent_runtime_transition_is_not_side_effect,
    build_agent_runtime_failure_record,
    build_agent_runtime_no_side_effect_guarantee,
    build_agent_runtime_run_preview,
    build_agent_runtime_session,
    build_agent_runtime_session_boundary_view,
    build_agent_runtime_session_flags,
    build_agent_runtime_session_report,
    build_agent_runtime_session_snapshot,
    build_agent_runtime_source_ref,
    build_agent_runtime_state_machine,
    build_agent_runtime_step,
    build_agent_runtime_transition_request,
    build_agent_runtime_turn,
    build_v0333_readiness_report,
    default_agent_runtime_transition_matrix,
    derive_agent_runtime_state_transition,
    v0333_readiness_report_is_not_runtime_ready,
    validate_agent_runtime_transition_request,
)
from chanta_core.agent_runtime.session_runtime import (
    DEFAULT_SESSION_PROHIBITED_RUNTIME_ACTIONS,
    RUNTIME_FLAG_NAMES,
)


def test_session_runtime_taxonomies_and_flags_are_non_runtime():
    assert "awaiting_model_step" in {item.value for item in AgentRuntimeSessionState}
    assert "safe_failed" in {item.value for item in AgentRuntimeSessionState}
    assert "model_step_planned" in {item.value for item in AgentRuntimeTurnState}
    assert "tool_call_planned" in {item.value for item in AgentRuntimeTurnState}
    assert "model_step_plan" in {item.value for item in AgentRuntimeStepKind}
    assert "plan_model_step" in {item.value for item in AgentRuntimeTransitionKind}
    assert "allowed_state_transition" in {item.value for item in AgentRuntimeTransitionDecisionKind}
    assert "response_ready" in {item.value for item in AgentRuntimeTerminalOutcomeKind}
    assert "ocel_emission_blocked" in {item.value for item in AgentRuntimeFailureKind}
    assert "opencode_reference_context_ref" in {item.value for item in AgentRuntimeSourceKind}
    assert "hermes_reference_context_ref" in {item.value for item in AgentRuntimeSourceKind}
    assert "state_transition_ready" in {item.value for item in AgentRuntimeReadinessLevel}

    flags = build_agent_runtime_session_flags(
        state_machine_constructed=True,
        transition_validation_available=True,
        ready_for_v0334_readonly_tool_registry=True,
        ready_for_v0336_agent_step_runner=True,
        ready_for_v0337_runtime_ocel_trace_emitter=True,
    )

    assert flags.state_machine_constructed is True
    assert flags.transition_validation_available is True
    assert flags.ready_for_v0334_readonly_tool_registry is True
    assert flags.ready_for_v0336_agent_step_runner is True
    assert flags.ready_for_v0337_runtime_ocel_trace_emitter is True
    assert agent_runtime_flags_preserve_runtime_false(flags)

    for flag_name in RUNTIME_FLAG_NAMES:
        with pytest.raises(ValueError):
            AgentRuntimeSessionFlagSet(
                flag_set_id=f"flags:bad:{flag_name}",
                version="v0.33.3",
                **{flag_name: True},
            )


def test_source_boundary_session_turn_and_step_are_state_artifacts_only():
    source_ref = build_agent_runtime_source_ref(
        "source:prompt",
        AgentRuntimeSourceKind.V0332_PROMPT_ASSEMBLY_OUTPUT,
        "prompt-output:1",
        "In-memory PromptAssemblyOutput metadata.",
    )
    reference_ref = build_agent_runtime_source_ref(
        "source:reference",
        AgentRuntimeSourceKind.OPENCODE_REFERENCE_CONTEXT_REF,
        "references/OpenCode",
        "Path-ref label only.",
    )
    boundary = build_agent_runtime_session_boundary_view(
        "boundary:view",
        runtime_boundary_id="boundary:1",
        runtime_profile_id="profile:1",
        prompt_output_id="prompt-output:1",
        source_refs=[source_ref, reference_ref],
    )
    session = build_agent_runtime_session(
        "session:1",
        boundary,
        runtime_profile_id="profile:1",
        prompt_output_id="prompt-output:1",
        source_refs=[source_ref, reference_ref],
    )
    turn = build_agent_runtime_turn(
        "turn:1",
        session.session_id,
        prompt_output_id=session.prompt_output_id,
        source_refs=[source_ref],
    )
    step = build_agent_runtime_step(
        "step:1",
        session.session_id,
        turn_id=turn.turn_id,
        step_kind=AgentRuntimeStepKind.PROMPT_ATTACH,
        proposed_next_transition=AgentRuntimeTransitionKind.OPEN_TURN,
        source_refs=[source_ref],
    )

    assert source_ref.fetch is False
    assert source_ref.file_read is False
    assert source_ref.execution is False
    assert set(DEFAULT_SESSION_PROHIBITED_RUNTIME_ACTIONS).issubset(set(boundary.prohibited_runtime_actions))
    assert boundary.ready_for_execution is False
    assert boundary.runtime_enforcement is False
    assert agent_runtime_session_is_not_execution(session)
    assert turn.ready_for_model_invocation is False
    assert turn.ready_for_tool_execution is False
    assert turn.model_or_tool_execution is False
    assert step.ready_for_execution is False
    assert step.step_execution is False

    with pytest.raises(ValueError):
        AgentRuntimeSourceRef(
            source_ref_id="source:bad",
            source_kind=AgentRuntimeSourceKind.REFERENCE_CONTEXT_REF,
            source_id="references/Hermes",
            source_summary="bad",
            metadata={"file_read": True},
        )
    with pytest.raises(ValueError):
        AgentRuntimeSessionBoundaryView(
            boundary_view_id="boundary:bad",
            ready_for_execution=True,
        )
    with pytest.raises(ValueError):
        AgentRuntimeSession(
            session_id="session:bad",
            state=AgentRuntimeSessionState.CREATED,
            boundary_view=boundary,
            ready_for_execution=True,
        )
    with pytest.raises(ValueError):
        AgentRuntimeTurn(
            turn_id="turn:bad",
            session_id=session.session_id,
            state=AgentRuntimeTurnState.CREATED,
            ready_for_model_invocation=True,
        )
    with pytest.raises(ValueError):
        AgentRuntimeTurn(
            turn_id="turn:bad:tool",
            session_id=session.session_id,
            state=AgentRuntimeTurnState.CREATED,
            ready_for_tool_execution=True,
        )
    with pytest.raises(ValueError):
        AgentRuntimeStep(
            step_id="step:bad",
            session_id=session.session_id,
            turn_id=None,
            step_kind=AgentRuntimeStepKind.MODEL_STEP_PLAN,
            title="bad",
            summary="bad",
            ready_for_execution=True,
        )


def test_transition_validation_derivation_and_blocked_runtime_surfaces_are_safe():
    state_machine = build_agent_runtime_state_machine("state-machine:1")
    assert state_machine.ready_for_transition_validation is True
    assert state_machine.ready_for_execution is False
    assert state_machine.runtime_execution is False
    assert AgentRuntimeTransitionKind.PLAN_MODEL_STEP in state_machine.prohibited_runtime_transitions
    assert "attach_boundary" in default_agent_runtime_transition_matrix()["created"]

    allowed_request = build_agent_runtime_transition_request(
        "transition-request:allowed",
        "session:1",
        AgentRuntimeTransitionKind.ATTACH_BOUNDARY,
        current_session_state=AgentRuntimeSessionState.CREATED,
    )
    allowed_decision = validate_agent_runtime_transition_request(state_machine, allowed_request)
    allowed_transition = derive_agent_runtime_state_transition(allowed_request, allowed_decision)

    assert allowed_decision.decision_kind == AgentRuntimeTransitionDecisionKind.ALLOWED_STATE_TRANSITION
    assert allowed_decision.ready_for_execution is False
    assert allowed_decision.side_effect_execution is False
    assert allowed_transition.to_session_state == AgentRuntimeSessionState.BOUNDARY_ATTACHED
    assert agent_runtime_transition_is_not_side_effect(allowed_transition)

    invalid_request = build_agent_runtime_transition_request(
        "transition-request:invalid",
        "session:1",
        AgentRuntimeTransitionKind.ATTACH_PROMPT,
        current_session_state=AgentRuntimeSessionState.CREATED,
    )
    invalid_decision = validate_agent_runtime_transition_request(state_machine, invalid_request)
    assert invalid_decision.decision_kind == AgentRuntimeTransitionDecisionKind.DENIED_INVALID_TRANSITION
    assert invalid_decision.denied_failure_kind == AgentRuntimeFailureKind.INVALID_TRANSITION

    model_request = build_agent_runtime_transition_request(
        "transition-request:model",
        "session:1",
        AgentRuntimeTransitionKind.PLAN_MODEL_STEP,
        current_session_state=AgentRuntimeSessionState.TURN_OPEN,
        current_turn_state=AgentRuntimeTurnState.PROMPT_CONTEXT_ATTACHED,
    )
    model_decision = validate_agent_runtime_transition_request(state_machine, model_request)
    model_transition = derive_agent_runtime_state_transition(model_request, model_decision)
    assert model_decision.decision_kind == AgentRuntimeTransitionDecisionKind.BLOCKED_BY_RUNTIME_PROHIBITION
    assert model_decision.denied_failure_kind == AgentRuntimeFailureKind.MODEL_INVOCATION_BLOCKED
    assert model_transition.terminal_outcome == AgentRuntimeTerminalOutcomeKind.BLOCKED

    tool_request = build_agent_runtime_transition_request(
        "transition-request:tool",
        "session:1",
        AgentRuntimeTransitionKind.PLAN_TOOL_CALL,
        current_session_state=AgentRuntimeSessionState.TURN_OPEN,
        current_turn_state=AgentRuntimeTurnState.PROMPT_CONTEXT_ATTACHED,
    )
    tool_decision = validate_agent_runtime_transition_request(state_machine, tool_request)
    assert tool_decision.denied_failure_kind == AgentRuntimeFailureKind.TOOL_EXECUTION_BLOCKED

    with pytest.raises(ValueError):
        AgentRuntimeTransitionDecision(
            transition_decision_id="decision:bad",
            transition_request_id=allowed_request.transition_request_id,
            decision_kind=AgentRuntimeTransitionDecisionKind.ALLOWED_STATE_TRANSITION,
            reason="bad",
            ready_for_execution=True,
        )
    with pytest.raises(ValueError):
        AgentRuntimeStateTransition(
            transition_id="transition:bad",
            transition_request_id=allowed_request.transition_request_id,
            transition_decision_id=allowed_decision.transition_decision_id,
            session_id="session:1",
            turn_id=None,
            transition_kind=AgentRuntimeTransitionKind.ATTACH_BOUNDARY,
            from_session_state=AgentRuntimeSessionState.CREATED,
            to_session_state=AgentRuntimeSessionState.BOUNDARY_ATTACHED,
            from_turn_state=None,
            to_turn_state=None,
            terminal_outcome=None,
            summary="bad",
            ready_for_execution=True,
        )
    with pytest.raises(ValueError):
        AgentRuntimeStateMachine(
            state_machine_id="state-machine:bad",
            version="v0.33.3",
            ready_for_execution=True,
        )


def test_failure_snapshot_report_preview_guarantee_and_readiness_are_non_runtime():
    boundary = build_agent_runtime_session_boundary_view("boundary:snapshot")
    session = build_agent_runtime_session("session:snapshot", boundary)
    turn = build_agent_runtime_turn("turn:snapshot", session.session_id)
    step = build_agent_runtime_step("step:snapshot", session.session_id, turn_id=turn.turn_id)
    request = build_agent_runtime_transition_request(
        "transition-request:snapshot",
        session.session_id,
        AgentRuntimeTransitionKind.NO_OP,
        current_session_state=AgentRuntimeSessionState.CREATED,
    )
    decision = validate_agent_runtime_transition_request(build_agent_runtime_state_machine(), request)
    transition = derive_agent_runtime_state_transition(request, decision)
    failure = build_agent_runtime_failure_record(
        "failure:1",
        session.session_id,
        failure_kind=AgentRuntimeFailureKind.PERMISSION_DENIED,
        safe_outcome=AgentRuntimeTerminalOutcomeKind.BLOCKED,
    )
    snapshot = build_agent_runtime_session_snapshot(
        "snapshot:1",
        session,
        turns=[turn],
        steps=[step],
        transitions=[transition],
        failures=[failure],
    )
    report = build_agent_runtime_session_report(
        "report:1",
        session.session_id,
        snapshot_id=snapshot.snapshot_id,
        state_machine_id="state-machine:1",
        transition_count=1,
        failure_count=1,
        active_turn_count=1,
        ready_for_v0334_readonly_tool_registry=True,
        ready_for_v0336_agent_step_runner=True,
        ready_for_v0337_runtime_ocel_trace_emitter=True,
    )
    preview = build_agent_runtime_run_preview("preview:1", session_id=session.session_id)
    guarantee = build_agent_runtime_no_side_effect_guarantee("guarantee:1")
    readiness = build_v0333_readiness_report(
        "readiness:1",
        session_report_id=report.report_id,
        session_snapshot_id=snapshot.snapshot_id,
        state_machine_id="state-machine:1",
        ready_for_v0334_readonly_tool_registry=True,
        ready_for_v0336_agent_step_runner=True,
        ready_for_v0337_runtime_ocel_trace_emitter=True,
        completed_items=["session state-machine contract"],
    )

    assert failure.ready_for_retry is False
    assert failure.ready_for_execution is False
    assert failure.safe_diagnostic_metadata is True
    assert agent_runtime_snapshot_is_not_persistence(snapshot)
    assert report.ready_for_execution is False
    assert report.runtime_execution is False
    assert all(getattr(preview, name) is True for name in preview.__dataclass_fields__ if name.startswith("no_"))
    assert preview.execution is False
    assert all(getattr(guarantee, name) is True for name in guarantee.__dataclass_fields__ if name.startswith("no_"))
    assert v0333_readiness_report_is_not_runtime_ready(readiness)
    assert set(DEFAULT_SESSION_PROHIBITED_RUNTIME_ACTIONS).issubset(set(readiness.prohibited_until_later_gate))

    with pytest.raises(ValueError):
        AgentRuntimeFailureRecord(
            failure_record_id="failure:bad",
            session_id=session.session_id,
            turn_id=None,
            failure_kind=AgentRuntimeFailureKind.INVALID_TRANSITION,
            summary="bad",
            safe_outcome=AgentRuntimeTerminalOutcomeKind.BLOCKED,
            ready_for_retry=True,
        )
    with pytest.raises(ValueError):
        AgentRuntimeSessionSnapshot(
            snapshot_id="snapshot:bad",
            version="v0.33.3",
            session=session,
            metadata={"persistence": True},
        )
    with pytest.raises(ValueError):
        AgentRuntimeSessionReport(
            report_id="report:bad",
            version="v0.33.3",
            session_id=session.session_id,
            snapshot_id=None,
            state_machine_id=None,
            status=AgentRuntimeSessionState.BLOCKED,
            readiness_level=AgentRuntimeReadinessLevel.BLOCKED,
            summary="bad",
            ready_for_v0336_agent_step_runner=True,
            blocked_items=["blocked"],
        )
    with pytest.raises(ValueError):
        AgentRuntimeRunPreview(
            run_preview_id="preview:bad",
            no_ocel_emission_guarantee=False,
        )
    with pytest.raises(ValueError):
        AgentRuntimeNoSideEffectGuarantee(
            guarantee_id="guarantee:bad",
            version="v0.33.3",
            no_runtime_trace_persistence=False,
        )
    for flag_name in RUNTIME_FLAG_NAMES:
        with pytest.raises(ValueError):
            V0333ReadinessReport(
                report_id=f"readiness:bad:{flag_name}",
                version="v0.33.3",
                **{flag_name: True},
            )
