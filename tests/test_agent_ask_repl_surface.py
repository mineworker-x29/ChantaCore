from __future__ import annotations

from chanta_core.agent_surface import (
    AGENT_ASK_REPL_EFFECT_TYPES,
    AGENT_ASK_REPL_EVENT_TYPES,
    AGENT_ASK_REPL_OBJECT_TYPES,
    AGENT_ASK_REPL_RELATION_TYPES,
    AGENT_ASK_REPL_VERSION,
    AgentAskPipelinePolicyService,
    AgentAskPolicyService,
    AgentAskReplReport,
    AgentAskReplReportService,
    AgentAskRequest,
    AgentReplPolicyService,
    AgentReplSessionService,
    AgentSurfaceCommandHistoryService,
    AgentSurfaceEmissionPolicyService,
    AgentSurfaceSessionStateService,
)
from chanta_core.agent_surface.ask_repl import (
    AgentAskPipelineResult,
    AgentAskPipelineRun,
    AgentAskPipelineStep,
    AgentReplTurnRequest,
    AgentReplTurnResult,
    AgentSurfaceEmission,
    AgentSurfaceOutputView,
)
from chanta_core.agent_surface.response_assembly import AgentResponseAssemblyReportService
from chanta_core.cli.main import main


def _service() -> AgentAskReplReportService:
    return AgentAskReplReportService()


def test_ask_policy_and_repl_policy_build_with_v0257_boundaries() -> None:
    ask_policy = AgentAskPolicyService().build_policy()
    repl_policy = AgentReplPolicyService().build_policy()
    pipeline_policy = AgentAskPipelinePolicyService().build_policy()
    emission_policy = AgentSurfaceEmissionPolicyService().build_policy()

    assert ask_policy.version == AGENT_ASK_REPL_VERSION
    assert ask_policy.layer == "agent_surface"
    assert ask_policy.ask_enabled is True
    assert ask_policy.repl_enabled is True
    assert ask_policy.synchronous_only is True
    assert ask_policy.autonomous_loop_enabled is False
    assert ask_policy.background_execution_enabled is False
    assert ask_policy.self_prompting_enabled is False
    assert ask_policy.direct_provider_invocation_enabled is False
    assert ask_policy.direct_file_access_enabled is False
    assert ask_policy.direct_subprocess_enabled is False
    assert ask_policy.direct_local_command_execution_enabled is False
    assert ask_policy.memory_promotion_enabled is False
    assert ask_policy.persistent_memory_write_enabled is False
    assert ask_policy.persona_mutation_enabled is False
    assert ask_policy.external_provider_adapter_enabled is False
    assert ask_policy.external_agent_adapter_enabled is False
    assert ask_policy.require_v025_pipeline is True
    assert ask_policy.require_v0256_assembled_response_for_emission is True
    assert ask_policy.raw_secret_output_forbidden is True
    assert ask_policy.raw_provider_output_inline_forbidden is True
    assert ask_policy.private_path_sanitization_required is True
    assert ask_policy.llm_judge_enabled is False
    assert repl_policy.user_driven_turns_only is True
    assert repl_policy.one_pipeline_run_per_user_turn is True
    assert repl_policy.no_autonomous_loop is True
    assert repl_policy.no_background_execution is True
    assert repl_policy.no_self_prompting is True
    assert repl_policy.memory_promotion_enabled is False
    assert pipeline_policy.required_stage_order == [
        "v0.25.1_turn_envelope",
        "v0.25.2_intent_task",
        "v0.25.3_safety_gate",
        "v0.25.4_route_plan_if_allow_route",
        "v0.25.5_provider_invocation_if_required",
        "v0.25.6_response_assembly",
        "v0.25.7_surface_emission",
    ]
    assert pipeline_policy.max_pipeline_turns_per_ask == 1
    assert emission_policy.emit_only_assembled_response is True
    assert emission_policy.final_response_emission_enabled is True
    assert emission_policy.max_output_chars > 0


def test_ask_repl_models_build() -> None:
    request = AgentAskRequest(request_id="ask:test", user_text="Explain")
    step = AgentAskPipelineStep(
        pipeline_step_id="step:test",
        step_index=1,
        stage_id="v0.25.1_turn_envelope",
        stage_name="Turn",
        input_refs=[],
        output_refs=[],
        step_status="executed",
        executed_now=True,
    )
    run = AgentAskPipelineRun(pipeline_run_id="run:test", ask_request_id=request.request_id, steps=[step], started_at="now")
    result = AgentAskPipelineResult(
        pipeline_result_id="result:test",
        pipeline_run_id=run.pipeline_run_id,
        primary_outcome="answered",
        assembled_response_id="assembled:test",
        emission_id="emission:test",
        response_text="text",
        result_status="ready",
        evidence_bound=True,
        final_response_emitted=True,
        provider_invoked_via_v0255=False,
        local_command_executed_via_v024=False,
    )
    emission = AgentSurfaceEmission(
        emission_id="emission:test",
        assembled_response_id="assembled:test",
        response_text="text",
        output_view_id="view:test",
        emitted_at="now",
        emitted_to="test_fixture",
    )
    view = AgentSurfaceOutputView(output_view_id="view:test", response_text="text", display_format="plain_text")
    session = AgentReplSessionService().start_session("session:test")
    turn_request = AgentReplTurnRequest(repl_turn_request_id="turn:test", repl_session_id=session.repl_session_id, user_text="Explain", turn_index=1)
    turn_result = AgentReplTurnResult(
        repl_turn_result_id="turn-result:test",
        repl_session_id=session.repl_session_id,
        turn_index=1,
        ask_request_id=request.request_id,
        pipeline_result_id=result.pipeline_result_id,
        emission_id=emission.emission_id,
        turn_status="completed",
        final_response_emitted=True,
    )
    history = AgentSurfaceCommandHistoryService().record_history_entry("ask", {"id": request.request_id}, {"id": result.pipeline_result_id})
    state = AgentSurfaceSessionStateService().build_session_state(ask_count=1, emission_count=1)
    report = AgentAskReplReport(
        report_id="report:test",
        created_at="now",
        policy=AgentAskPolicyService().build_policy(),
        ask_request=request,
        pipeline_run=run,
        pipeline_result=result,
        emission=emission,
        repl_session=session,
        repl_turn_result=turn_result,
        session_state=state,
    )

    assert request.version == AGENT_ASK_REPL_VERSION
    assert run.autonomous_loop_started is False
    assert result.direct_provider_invocation is False
    assert emission.final_response_emitted is True
    assert emission.raw_secret_output is False
    assert view.bounded is True
    assert session.user_driven is True
    assert turn_request.run_full_pipeline is True
    assert turn_result.autonomous_followup_created is False
    assert history.sanitized is True
    assert state.autonomous_loop_count == 0
    assert report.ready_for_v0_26 is False


def test_single_ask_runs_one_bounded_pipeline_and_emits_response() -> None:
    report = _service().build_report("Explain the project structure")

    assert report.ask_executed is True
    assert report.repl_started is False
    assert report.repl_turn_executed is False
    assert report.final_response_emitted is True
    assert report.response_assembled_via_v0256 is True
    assert report.pipeline_run is not None
    assert len([step for step in report.pipeline_run.steps if step.executed_now]) <= 7
    assert report.pipeline_run.autonomous_loop_started is False
    assert report.pipeline_run.background_execution_started is False
    assert report.pipeline_run.self_prompt_loop_started is False
    assert report.pipeline_result.evidence_bound is True
    assert report.direct_provider_invocation is False
    assert report.direct_file_access_performed is False
    assert report.direct_subprocess_performed is False
    assert report.direct_local_command_executed is False
    assert report.command_rerun_performed is False
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.persona_mutated is False
    assert report.raw_secret_output is False
    assert report.raw_provider_output_inline is False
    assert report.llm_judge_used is False
    assert report.ready_for_v0_25_8 is True
    assert report.ready_for_v0_26 is False


def test_ask_can_emit_existing_v0256_assembled_response() -> None:
    response_report = AgentResponseAssemblyReportService().build_report("Explain the project structure")
    assembled_id = response_report.assembled_response.assembled_response_id
    report = _service().build_report(
        "Explain the project structure",
        assembled_response_id=assembled_id,
        run_full_pipeline=False,
    )

    assert report.final_response_emitted is True
    assert report.response_assembled_via_v0256 is True
    assert report.pipeline_result.assembled_response_id == assembled_id
    assert any(step.stage_id == "v0.25.6_response_assembly" for step in report.pipeline_run.steps)


def test_non_route_outcomes_emit_policy_responses() -> None:
    cases = [
        ("Do nothing and stop here", "no_action_response", "no_action_emitted"),
        ("unclear ambiguous target", "clarification_response", "clarification_emitted"),
        ("Print token=ghp_example and password=hunter2", "blocked_response", "blocked_emitted"),
        ("Promote this into persistent memory continuity", "deferred_response", "deferred_emitted"),
    ]
    for text, outcome, finding_type in cases:
        report = _service().build_report(text)
        finding_types = {finding.finding_type for finding in report.findings}

        assert report.pipeline_result.primary_outcome == outcome
        assert finding_type in finding_types
        assert report.final_response_emitted is True
        assert any(step.stage_id == "v0.25.4_route_plan_if_allow_route" and step.step_status == "skipped" for step in report.pipeline_run.steps)


def test_repl_session_and_explicit_user_turn_are_user_driven() -> None:
    session = AgentReplSessionService().start_session("session:test")
    turn_request, turn_result, report = AgentReplSessionService().run_user_turn(session, "Explain the project structure")
    closed = AgentReplSessionService().close_session(session)

    assert session.user_driven is True
    assert turn_request.turn_index == 1
    assert turn_result.final_response_emitted is True
    assert turn_result.autonomous_followup_created is False
    assert report.repl_started is True
    assert report.repl_turn_executed is True
    assert report.ask_executed is False
    assert report.pipeline_run.autonomous_loop_started is False
    assert len(report.pipeline_run.steps) <= 7
    assert closed.session_status == "closed"


def test_session_state_and_history_are_sanitized() -> None:
    state = AgentSurfaceSessionStateService().build_session_state(ask_count=2, repl_turn_count=1, emission_count=3, active_repl_sessions=1)
    history = AgentSurfaceCommandHistoryService().record_history_entry("ask", {"id": "request"}, {"id": "result"})

    assert state.total_ask_count == 2
    assert state.total_repl_turn_count == 1
    assert state.total_emission_count == 3
    assert state.autonomous_loop_count == 0
    assert state.background_execution_count == 0
    assert state.memory_promotion_count == 0
    assert state.external_adapter_count == 0
    assert history.sanitized is True
    assert history.raw_secret_included is False


def test_ocel_pig_ocpx_mapping_and_reports() -> None:
    service = _service()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert "agent_ask_policy" in AGENT_ASK_REPL_OBJECT_TYPES
    assert "agent_ask_requested" in AGENT_ASK_REPL_EVENT_TYPES
    assert "emits_assembled_response" in AGENT_ASK_REPL_RELATION_TYPES
    assert "agent_ask_executed" in AGENT_ASK_REPL_EFFECT_TYPES
    assert "final_response_emitted" in AGENT_ASK_REPL_EFFECT_TYPES
    assert pig["version"] == "v0.25.7"
    assert pig["layer"] == "agent_surface"
    assert pig["subject"] == "ask_repl_surface"
    assert pig["safety_boundary"]["final_response_emitted"] == "conditional"
    assert pig["safety_boundary"]["direct_provider_invocation"] is False
    assert pig["safety_boundary"]["autonomous_loop_started"] is False
    assert pig["safety_boundary"]["raw_provider_output_inline"] is False
    assert pig["safety_boundary"]["llm_judge_enabled"] is False
    assert ocpx["state"] == "agent_ask_repl_surface_enabled"
    assert "AgentAskPipelineRunState" in ocpx["target_read_models"]
    assert "AgentSurfaceEmissionState" in ocpx["target_read_models"]


def test_cli_agent_ask_repl_and_surface_views_render(capsys) -> None:
    emission_commands = [
        ["agent", "ask", "run", "--text", "Explain the project structure"],
        ["agent", "ask", "run", "--assembled-response-id", "assembled:test"],
        ["agent", "ask", "report", "--report-id", "demo"],
        ["agent", "ask", "history"],
        ["agent", "repl", "turn", "--session-id", "session:test", "--text", "Explain the project structure"],
        ["agent", "surface", "state"],
    ]

    for command in emission_commands:
        assert main(command) == 0
        output = capsys.readouterr().out
        assert "version=v0.25.7" in output
        assert "layer=agent_surface" in output
        assert "final_response_emitted=true" in output
        assert "response_assembled_via_v0256=true" in output
        assert "direct_provider_invocation=false" in output
        assert "direct_file_access_performed=false" in output
        assert "direct_subprocess_performed=false" in output
        assert "direct_local_command_executed=false" in output
        assert "command_rerun_performed=false" in output
        assert "autonomous_loop_started=false" in output
        assert "background_execution_started=false" in output
        assert "self_prompt_loop_started=false" in output
        assert "memory_promoted=false" in output
        assert "persistent_memory_written=false" in output
        assert "persona_mutated=false" in output
        assert "credential_exposed=false" in output
        assert "raw_secret_output=false" in output
        assert "raw_provider_output_inline=false" in output
        assert "llm_judge_used=false" in output
        assert "next_required_step=v0.25.8 Agent Trace / Usability Telemetry" in output

    for command in [
        ["agent", "repl", "start", "--session-id", "session:test"],
        ["agent", "repl", "session", "--session-id", "session:test"],
    ]:
        assert main(command) == 0
        output = capsys.readouterr().out
        assert "version=v0.25.7" in output
        assert "layer=agent_surface" in output
        assert "ask_executed=false" in output
        assert "repl_started=true" in output
        assert "repl_turn_executed=false" in output
        assert "final_response_emitted=false" in output
        assert "autonomous_loop_started=false" in output
        assert "background_execution_started=false" in output
        assert "self_prompt_loop_started=false" in output
        assert "raw_secret_output=false" in output
