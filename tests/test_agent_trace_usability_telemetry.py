from __future__ import annotations

from chanta_core.agent_surface import (
    AGENT_TRACE_EFFECT_TYPES,
    AGENT_TRACE_EVENT_TYPES,
    AGENT_TRACE_OBJECT_TYPES,
    AGENT_TRACE_RELATION_TYPES,
    AGENT_TRACE_TELEMETRY_VERSION,
    AgentDecisionTrace,
    AgentPipelineStageTrace,
    AgentProviderInvocationTraceView,
    AgentResponseEmissionTrace,
    AgentRouteTrace,
    AgentSurfaceTrace,
    AgentTraceEvent,
    AgentTraceObjectRef,
    AgentTracePolicyService,
    AgentTraceRelationRef,
    AgentTraceRequest,
    AgentTraceSourceBundle,
    AgentTraceTelemetryReportService,
    AgentTurnOCELProjection,
    AgentTurnOCELProjectionPolicyService,
    AgentUsabilityMetricDefinition,
    AgentUsabilityMetricDefinitionService,
    AgentUsabilityMetricSet,
    AgentUsabilityMetricValue,
    AgentUsabilityTelemetryPolicyService,
    AgentUsabilityTelemetryReport,
)
from chanta_core.cli.main import main


def _service() -> AgentTraceTelemetryReportService:
    return AgentTraceTelemetryReportService()


def test_trace_policy_builds_with_v0258_boundaries() -> None:
    policy = AgentTracePolicyService().build_policy()
    telemetry_policy = AgentUsabilityTelemetryPolicyService().build_policy()
    projection_policy = AgentTurnOCELProjectionPolicyService().build_policy()

    assert policy.version == AGENT_TRACE_TELEMETRY_VERSION
    assert policy.layer == "agent_surface"
    assert policy.trace_recording_enabled is True
    assert policy.telemetry_enabled is True
    assert policy.report_derived_only is True
    assert policy.raw_transcript_persistence_enabled is False
    assert policy.raw_provider_output_persistence_enabled is False
    assert policy.raw_secret_persistence_enabled is False
    assert policy.ask_execution_enabled is False
    assert policy.repl_execution_enabled is False
    assert policy.provider_invocation_enabled is False
    assert policy.local_runtime_execution_enabled is False
    assert policy.background_daemon_enabled is False
    assert policy.continuous_watcher_enabled is False
    assert policy.autonomous_optimization_enabled is False
    assert policy.workspace_workbench_enabled is False
    assert policy.memory_promotion_enabled is False
    assert policy.persistent_memory_write_enabled is False
    assert policy.persona_mutation_enabled is False
    assert policy.external_provider_adapter_enabled is False
    assert policy.external_agent_adapter_enabled is False
    assert policy.ocel_projection_required is True
    assert policy.private_path_sanitization_required is True
    assert policy.credential_output_forbidden is True
    assert policy.raw_secret_output_forbidden is True
    assert policy.llm_judge_enabled is False
    assert telemetry_policy.descriptive_only is True
    assert telemetry_policy.background_collection_enabled is False
    assert telemetry_policy.raw_transcript_collection_enabled is False
    assert telemetry_policy.memory_promotion_enabled is False
    assert telemetry_policy.external_reporting_enabled is False
    assert projection_policy.projection_enabled is True
    assert projection_policy.mutate_original_artifacts is False
    assert projection_policy.raw_transcript_projection_forbidden is True


def test_trace_telemetry_models_build() -> None:
    request = AgentTraceRequest(request_id="trace-request:test", ask_repl_report_id="ask-report:test")
    source_bundle = AgentTraceSourceBundle(source_bundle_id="bundle:test", source_count=1, source_status="partial")
    event = AgentTraceEvent(
        trace_event_id="event:test",
        event_type="agent_trace_event_created",
        timestamp=None,
        stage_id="v0.25.1_turn_envelope",
        source_ref={"id": "source"},
        event_status="observed",
    )
    object_ref = AgentTraceObjectRef(
        object_ref_id="object:test",
        object_type="agent_ask_repl_report",
        object_id="ask-report:test",
        source_version="v0.25.7",
        stage_id=None,
        sanitized_label="ask-report:test",
    )
    relation = AgentTraceRelationRef(
        relation_ref_id="relation:test",
        relation_type="uses_agent_ask_repl_report",
        source_object_ref_id=object_ref.object_ref_id,
        target_object_ref_id=object_ref.object_ref_id,
        stage_id=None,
    )
    stage = AgentPipelineStageTrace(
        stage_trace_id="stage:test",
        stage_id="v0.25.1_turn_envelope",
        stage_name="Turn",
        stage_status="completed",
        input_refs=[],
        output_refs=[],
        started_at=None,
        ended_at=None,
        duration_ms=None,
        provider_invoked=False,
        local_command_executed=False,
    )
    decision = AgentDecisionTrace(
        decision_trace_id="decision:test",
        decision_type="safety_gate",
        decision_outcome="allow_route",
        decision_confidence="medium",
        source_ref=None,
    )
    route = AgentRouteTrace(
        route_trace_id="route:test",
        route_kind="provider_backed_route",
        selected_provider_refs=[],
        route_step_refs=[],
        route_status="invoked",
        provider_invocation_required=True,
        provider_invoked_via_v0255=True,
    )
    provider = AgentProviderInvocationTraceView(
        provider_trace_view_id="provider:test",
        provider_invocation_report_ref=None,
        provider_result_refs=[],
        provider_invoked_via_v0255=True,
        local_command_executed_via_v024=False,
    )
    response = AgentResponseEmissionTrace(
        emission_trace_id="response:test",
        assembled_response_ref=None,
        surface_emission_ref=None,
        response_assembled_via_v0256=True,
        final_response_emitted_via_v0257=True,
        response_status="emitted",
    )
    surface = AgentSurfaceTrace(
        surface_trace_id="surface:test",
        created_at="now",
        source_bundle_id=source_bundle.source_bundle_id,
        trace_events=[event],
        object_refs=[object_ref],
        relation_refs=[relation],
        stage_traces=[stage],
        decision_traces=[decision],
        route_trace=route,
        provider_trace_view=provider,
        response_emission_trace=response,
        trace_status="complete",
        ocel_projectable=True,
    )
    projection = AgentTurnOCELProjection(
        projection_id="projection:test",
        surface_trace_id=surface.surface_trace_id,
        object_types=[],
        event_types=[],
        relation_types=[],
        projected_object_count=1,
        projected_event_count=1,
        projected_relation_count=1,
        projection_status="ready",
    )
    definition = AgentUsabilityMetricDefinition(
        metric_id="agent_turn_count",
        metric_name="Agent Turn Count",
        metric_category="turn_volume",
        description="count",
        value_type="count",
    )
    value = AgentUsabilityMetricValue(
        metric_value_id="metric-value:test",
        metric_id=definition.metric_id,
        value=1,
        unit="count",
        source_refs=[],
    )
    metric_set = AgentUsabilityMetricSet(metric_set_id="metric-set:test", metric_values=[value], metric_count=1, metric_set_status="ready")
    telemetry = AgentUsabilityTelemetryReport(
        telemetry_report_id="telemetry:test",
        created_at="now",
        policy=AgentUsabilityTelemetryPolicyService().build_policy(),
        surface_trace_id=surface.surface_trace_id,
        metric_definitions=[definition],
        metric_set=metric_set,
        telemetry_status="ready",
    )

    assert request.version == AGENT_TRACE_TELEMETRY_VERSION
    assert source_bundle.raw_transcript_included is False
    assert event.sanitized is True
    assert object_ref.raw_content_included is False
    assert relation.source_object_ref_id == object_ref.object_ref_id
    assert stage.direct_bypass_detected is False
    assert decision.deterministic is True
    assert decision.llm_judge_used is False
    assert route.provider_invoked_via_v0255 is True
    assert provider.direct_provider_invocation is False
    assert response.raw_provider_output_inline is False
    assert surface.raw_transcript_included is False
    assert projection.original_artifacts_mutated is False
    assert projection.raw_transcript_projected is False
    assert telemetry.descriptive_only is True


def test_trace_report_builds_from_v0257_report_refs_only() -> None:
    report = _service().build_report(ask_report_id="ask-report:test")

    assert report.version == AGENT_TRACE_TELEMETRY_VERSION
    assert report.report_status == "passed"
    assert report.trace_recorded is True
    assert report.ocel_projected is True
    assert report.telemetry_created is True
    assert report.ready_for_v0_25_9 is True
    assert report.ready_for_v0_26 is False
    assert report.source_bundle.source_status == "complete"
    assert report.source_bundle.source_count >= 4
    assert report.source_bundle.raw_transcript_included is False
    assert report.source_bundle.raw_secret_included is False
    assert report.source_bundle.raw_provider_output_included is False
    assert report.surface_trace.trace_status == "complete"
    assert len(report.surface_trace.stage_traces) == 7
    assert {stage.stage_id for stage in report.surface_trace.stage_traces} >= {
        "v0.25.1_turn_envelope",
        "v0.25.2_intent_task",
        "v0.25.3_safety_gate",
        "v0.25.4_route_plan",
        "v0.25.5_provider_invocation",
        "v0.25.6_response_assembly",
        "v0.25.7_surface_emission",
    }
    assert report.surface_trace.route_trace is not None
    assert report.surface_trace.provider_trace_view is not None
    assert report.surface_trace.response_emission_trace is not None
    assert report.surface_trace.provider_trace_view.provider_invoked_via_v0255 is True
    assert report.surface_trace.provider_trace_view.direct_provider_invocation is False
    assert report.surface_trace.response_emission_trace.response_assembled_via_v0256 is True
    assert report.surface_trace.response_emission_trace.final_response_emitted_via_v0257 is True
    assert report.surface_trace.raw_transcript_included is False
    assert report.surface_trace.raw_provider_output_included is False
    assert report.ocel_projection.projection_status == "ready"
    assert report.ocel_projection.original_artifacts_mutated is False
    assert report.ocel_projection.raw_provider_output_projected is False
    assert report.telemetry_report.telemetry_status == "ready"
    assert report.telemetry_report.autonomous_optimization_performed is False
    assert report.telemetry_report.background_collection_started is False
    assert report.telemetry_report.memory_promoted is False
    assert report.telemetry_report.external_report_sent is False


def test_metric_definitions_and_values_are_report_derived() -> None:
    report = _service().build_report(ask_report_id="ask-report:test")
    definitions = AgentUsabilityMetricDefinitionService().build_metric_definitions()
    metric_ids = {definition.metric_id for definition in definitions}
    values = {value.metric_id: value for value in report.telemetry_report.metric_set.metric_values}

    for required in [
        "agent_turn_count",
        "ask_count",
        "repl_turn_count",
        "final_response_emission_count",
        "allow_route_count",
        "route_plan_count",
        "provider_invocation_count",
        "response_assembly_count",
        "pipeline_completed_count",
        "direct_bypass_count",
        "autonomous_loop_count",
        "background_execution_count",
        "memory_promotion_count",
        "credential_exposure_count",
        "raw_secret_output_count",
    ]:
        assert required in metric_ids
        assert required in values
        assert values[required].computed is True
        assert values[required].computation_method == "report_derived"
        assert values[required].source_refs
    assert values["agent_turn_count"].value == 1
    assert values["ask_count"].value == 1
    assert values["final_response_emission_count"].value == 1
    assert values["provider_invocation_count"].value == 1
    assert values["direct_bypass_count"].value == 0
    assert values["autonomous_loop_count"].value == 0
    assert values["background_execution_count"].value == 0
    assert values["memory_promotion_count"].value == 0
    assert values["credential_exposure_count"].value == 0
    assert values["raw_secret_output_count"].value == 0
    assert report.telemetry_report.metric_set.metric_count == len(values)


def test_trace_report_flags_are_v0258_non_execution_flags() -> None:
    report = _service().build_report(ask_report_id="ask-report:test")

    assert report.ask_executed is False
    assert report.repl_executed is False
    assert report.final_response_emitted is False
    assert report.provider_invoked is False
    assert report.local_command_executed is False
    assert report.direct_file_access_performed is False
    assert report.direct_subprocess_performed is False
    assert report.command_rerun_performed is False
    assert report.background_collection_started is False
    assert report.autonomous_optimization_performed is False
    assert report.workspace_workbench_implemented is False
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.persona_mutated is False
    assert report.external_provider_adapter_implemented is False
    assert report.external_agent_adapter_implemented is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.raw_provider_output_inline is False
    assert report.raw_transcript_persisted is False
    assert report.llm_judge_used is False
    assert report.next_required_step == "v0.25.9 General Agent Usability Consolidation"


def test_ocel_pig_ocpx_mapping_and_reports() -> None:
    service = _service()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert "agent_trace_policy" in AGENT_TRACE_OBJECT_TYPES
    assert "agent_surface_trace" in AGENT_TRACE_OBJECT_TYPES
    assert "agent_trace_requested" in AGENT_TRACE_EVENT_TYPES
    assert "agent_turn_ocel_projected" in AGENT_TRACE_EVENT_TYPES
    assert "projects_agent_turn_to_ocel" in AGENT_TRACE_RELATION_TYPES
    assert "agent_surface_trace_recorded" in AGENT_TRACE_EFFECT_TYPES
    assert "agent_usability_telemetry_created" in AGENT_TRACE_EFFECT_TYPES
    assert pig["version"] == "v0.25.8"
    assert pig["layer"] == "agent_surface"
    assert pig["subject"] == "agent_trace_usability_telemetry"
    assert pig["safety_boundary"]["trace_recorded"] == "conditional"
    assert pig["safety_boundary"]["ask_executed"] is False
    assert pig["safety_boundary"]["provider_invoked"] is False
    assert pig["safety_boundary"]["raw_transcript_persisted"] is False
    assert pig["safety_boundary"]["llm_judge_enabled"] is False
    assert ocpx["state"] == "agent_trace_usability_telemetry_created"
    assert "AgentSurfaceTraceState" in ocpx["target_read_models"]
    assert "AgentUsabilityTelemetryReportState" in ocpx["target_read_models"]


def test_cli_trace_and_telemetry_views_render(capsys) -> None:
    commands = [
        ["agent", "trace", "record", "--ask-report-id", "ask-report:test"],
        ["agent", "trace", "view", "--trace-id", "trace:test"],
        ["agent", "trace", "projection", "--trace-id", "trace:test"],
        ["agent", "trace", "source-bundle", "--ask-report-id", "ask-report:test"],
        ["agent", "telemetry", "report", "--ask-report-id", "ask-report:test"],
        ["agent", "telemetry", "metrics", "--report-id", "trace-report:test"],
        ["agent", "telemetry", "findings", "--report-id", "trace-report:test"],
    ]

    for command in commands:
        assert main(command) == 0
        output = capsys.readouterr().out
        assert "version=v0.25.8" in output
        assert "layer=agent_surface" in output
        assert "trace_recorded=true" in output
        assert "ocel_projected=true" in output
        assert "telemetry_created=true" in output
        assert "ready_for_v0_25_9=true" in output
        assert "ready_for_v0_26=false" in output
        assert "ask_executed=false" in output
        assert "repl_executed=false" in output
        assert "final_response_emitted=false" in output
        assert "provider_invoked=false" in output
        assert "local_command_executed=false" in output
        assert "direct_file_access_performed=false" in output
        assert "direct_subprocess_performed=false" in output
        assert "command_rerun_performed=false" in output
        assert "background_collection_started=false" in output
        assert "autonomous_optimization_performed=false" in output
        assert "workspace_workbench_implemented=false" in output
        assert "memory_promoted=false" in output
        assert "persistent_memory_written=false" in output
        assert "persona_mutated=false" in output
        assert "credential_exposed=false" in output
        assert "raw_secret_output=false" in output
        assert "raw_provider_output_inline=false" in output
        assert "raw_transcript_persisted=false" in output
        assert "llm_judge_used=false" in output
        assert "next_required_step=v0.25.9 General Agent Usability Consolidation" in output
