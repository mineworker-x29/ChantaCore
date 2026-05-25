from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.workspace_agent_workbench import (
    WORKBENCH_TRACE_EXPLORER_EFFECT_TYPES,
    WORKBENCH_TRACE_EXPLORER_EVENT_TYPES,
    WORKBENCH_TRACE_EXPLORER_FORBIDDEN_EFFECT_TYPES,
    WORKBENCH_TRACE_EXPLORER_FUTURE_SKILL_IDS,
    WORKBENCH_TRACE_EXPLORER_IMPLEMENTED_SKILL_IDS,
    WORKBENCH_TRACE_EXPLORER_OBJECT_TYPES,
    WORKBENCH_TRACE_EXPLORER_RELATION_TYPES,
    WORKBENCH_TRACE_EXPLORER_VERSION,
    WorkbenchDecisionNode,
    WorkbenchPipelineTimeline,
    WorkbenchPipelineTimelinePolicy,
    WorkbenchProviderNode,
    WorkbenchRelationEdge,
    WorkbenchResponseNode,
    WorkbenchRouteNode,
    WorkbenchStageNode,
    WorkbenchTimelineNode,
    WorkbenchTraceExplorerFinding,
    WorkbenchTraceExplorerPolicy,
    WorkbenchTraceExplorerPrerequisiteSourceService,
    WorkbenchTraceExplorerReport,
    WorkbenchTraceExplorerReportService,
    WorkbenchTraceExplorerRequest,
    WorkbenchTraceExplorerView,
    WorkbenchTraceFilter,
    WorkbenchTraceFilterPolicy,
    WorkbenchTraceFilterState,
    WorkbenchTraceInspectionPolicy,
    WorkbenchTraceInspectionReport,
    WorkbenchTraceInspectionSummary,
    WorkbenchTraceSelectionView,
    WorkbenchTraceSourceView,
)


def _parts() -> dict:
    return WorkbenchTraceExplorerReportService().build_all_parts()


def test_trace_explorer_models_build() -> None:
    parts = _parts()

    assert isinstance(parts["policy"], WorkbenchTraceExplorerPolicy)
    assert isinstance(parts["request"], WorkbenchTraceExplorerRequest)
    assert isinstance(parts["source_view"], WorkbenchTraceSourceView)
    assert isinstance(parts["trace_explorer_view"], WorkbenchTraceExplorerView)
    assert isinstance(parts["timeline_policy"], WorkbenchPipelineTimelinePolicy)
    assert isinstance(parts["timeline"], WorkbenchPipelineTimeline)
    assert isinstance(parts["timeline_nodes"][0], WorkbenchTimelineNode)
    assert isinstance(parts["stage_nodes"][0], WorkbenchStageNode)
    assert isinstance(parts["decision_nodes"][0], WorkbenchDecisionNode)
    assert isinstance(parts["route_nodes"][0], WorkbenchRouteNode)
    assert isinstance(parts["provider_nodes"][0], WorkbenchProviderNode)
    assert isinstance(parts["response_nodes"][0], WorkbenchResponseNode)
    assert isinstance(parts["edges"][0], WorkbenchRelationEdge)
    assert isinstance(parts["filter_policy"], WorkbenchTraceFilterPolicy)
    assert isinstance(parts["filters"][0], WorkbenchTraceFilter)
    assert isinstance(parts["filter_state"], WorkbenchTraceFilterState)
    assert isinstance(parts["selection_view"], WorkbenchTraceSelectionView)
    assert isinstance(parts["inspection_policy"], WorkbenchTraceInspectionPolicy)
    assert isinstance(parts["inspection_summary"], WorkbenchTraceInspectionSummary)
    assert isinstance(parts["inspection_report"], WorkbenchTraceInspectionReport)
    assert isinstance(parts["findings"][0], WorkbenchTraceExplorerFinding)
    assert isinstance(parts["report"], WorkbenchTraceExplorerReport)


def test_sources_skills_and_policies_are_trace_view_only() -> None:
    parts = _parts()
    sources = WorkbenchTraceExplorerPrerequisiteSourceService().load_sources()
    policy = parts["policy"]

    assert WORKBENCH_TRACE_EXPLORER_VERSION == "v0.26.2"
    assert WORKBENCH_TRACE_EXPLORER_IMPLEMENTED_SKILL_IDS == [
        "skill:workbench_trace_explorer_view",
        "skill:workbench_pipeline_timeline_view",
    ]
    assert "skill:workbench_provider_browser_view" in WORKBENCH_TRACE_EXPLORER_FUTURE_SKILL_IDS
    assert "skill:workbench_evidence_inspector_view" in WORKBENCH_TRACE_EXPLORER_FUTURE_SKILL_IDS
    assert "skill:workbench_snapshot_create" in WORKBENCH_TRACE_EXPLORER_FUTURE_SKILL_IDS
    assert sources["workbench_view_state"] is not None
    assert sources["trace_explorer_panel_model"].panel_type == "trace_explorer"
    assert sources["pipeline_timeline_panel_model"].panel_type == "pipeline_timeline"
    assert sources["surface_trace"] is not None
    assert sources["ocel_projection"] is not None
    assert len(sources["stage_traces"]) >= 7
    assert len(sources["decision_traces"]) >= 7
    assert policy.trace_explorer_enabled is True
    assert policy.pipeline_timeline_enabled is True
    assert policy.actual_ui_rendering_enabled is False
    assert policy.panel_rendering_enabled is False
    assert policy.stage_rerun_enabled is False
    assert policy.provider_invocation_enabled is False
    assert policy.ask_execution_enabled is False
    assert policy.response_emission_enabled is False
    assert policy.local_runtime_execution_enabled is False
    assert policy.memory_promotion_enabled is False
    assert policy.persistent_memory_write_enabled is False
    assert policy.persona_mutation_enabled is False
    assert policy.external_provider_adapter_enabled is False
    assert policy.external_agent_adapter_enabled is False
    assert policy.refs_only_by_default is True
    assert policy.raw_transcript_inline_forbidden is True
    assert policy.raw_provider_output_inline_forbidden is True
    assert policy.raw_secret_inline_forbidden is True
    assert policy.credential_inline_forbidden is True
    assert policy.private_path_sanitization_required is True
    assert policy.ocel_visible is True


def test_source_view_trace_explorer_view_and_timeline_are_refs_only() -> None:
    parts = _parts()
    source_view = parts["source_view"]
    view = parts["trace_explorer_view"]
    timeline_policy = parts["timeline_policy"]
    timeline = parts["timeline"]

    assert source_view.source_trace_ref is not None
    assert source_view.source_projection_ref is not None
    assert len(source_view.stage_trace_refs) >= 7
    assert len(source_view.decision_trace_refs) >= 7
    assert source_view.raw_transcript_included is False
    assert source_view.raw_provider_output_included is False
    assert source_view.raw_secret_included is False
    assert source_view.private_full_path_included is False
    assert view.panel_id == "workbench_panel:trace_explorer"
    assert view.timeline_id == timeline.timeline_id
    assert view.renders_ui_now is False
    assert view.stage_rerun_enabled is False
    assert view.provider_invocation_enabled is False
    assert view.raw_transcript_included is False
    assert view.raw_provider_output_included is False
    assert view.raw_secret_included is False
    assert timeline_policy.node_model_only is True
    assert timeline_policy.edge_model_only is True
    assert timeline_policy.stage_execution_forbidden is True
    assert timeline_policy.route_execution_forbidden is True
    assert timeline_policy.provider_invocation_forbidden is True
    assert timeline.stage_node_count >= 7
    assert timeline.decision_node_count >= 7
    assert timeline.route_node_count == 1
    assert timeline.provider_node_count == 1
    assert timeline.response_node_count == 1
    assert timeline.executes_now is False
    assert timeline.rerun_enabled is False


def test_nodes_edges_filters_selection_and_inspection_are_non_executing() -> None:
    parts = _parts()
    stage = parts["stage_nodes"][0]
    decision = parts["decision_nodes"][0]
    route = parts["route_nodes"][0]
    provider = parts["provider_nodes"][0]
    response = parts["response_nodes"][0]
    edge = parts["edges"][0]
    filter_policy = parts["filter_policy"]
    filter_state = parts["filter_state"]
    selection = parts["selection_view"]
    inspection_policy = parts["inspection_policy"]
    inspection = parts["inspection_report"]

    assert stage.source_stage_trace_ref is not None
    assert stage.stage_id.startswith("v0.25.")
    assert stage.rerun_enabled is False
    assert decision.source_decision_trace_ref is not None
    assert decision.changes_decision_now is False
    assert decision.llm_judge_used is False
    assert route.source_route_trace_ref is not None
    assert route.invokes_provider_now is False
    assert provider.provider_trace_ref is not None
    assert provider.direct_provider_invocation is False
    assert provider.direct_local_command_executed is False
    assert provider.raw_provider_output_included is False
    assert response.response_emission_trace_ref is not None
    assert response.emits_response_now is False
    assert response.raw_secret_output is False
    assert response.raw_provider_output_inline is False
    assert edge.relation_type in {
        "stage_to_stage",
        "stage_to_decision",
        "decision_to_route",
        "route_to_provider",
        "provider_to_response",
        "response_to_emission",
        "trace_to_telemetry",
        "unknown",
    }
    assert edge.mutates_relation_now is False
    assert filter_policy.filter_is_not_data_deletion is True
    assert filter_policy.filter_is_not_access_control is True
    assert filter_state.data_deleted is False
    assert filter_state.access_policy_mutated is False
    assert selection.selection_is_approval is False
    assert selection.selection_executes_now is False
    assert selection.raw_content_included is False
    assert selection.raw_secret_included is False
    assert inspection_policy.inspection_is_read_only is True
    assert inspection_policy.stage_rerun_forbidden is True
    assert inspection_policy.provider_invocation_forbidden is True
    assert inspection.trace_mutated is False
    assert inspection.stage_rerun_performed is False
    assert inspection.provider_invoked is False
    assert inspection.local_command_executed is False
    assert inspection.raw_transcript_included is False
    assert inspection.raw_provider_output_included is False
    assert inspection.raw_secret_included is False


def test_report_ocel_pig_ocpx_and_cli_are_ready(capsys) -> None:
    parts = _parts()
    report = parts["report"]
    pig = parts["pig_report"]
    ocpx = parts["ocpx_projection"]

    assert report.report_status == "passed"
    assert report.ready_for_v0_26_3 is True
    assert report.ready_for_v0_27 is False
    assert report.trace_explorer_view_created is True
    assert report.pipeline_timeline_created is True
    assert report.stage_nodes_created is True
    assert report.decision_nodes_created is True
    assert report.relation_edges_created is True
    assert report.actual_ui_rendered is False
    assert report.panel_rendered is False
    assert report.trace_mutated is False
    assert report.stage_rerun_performed is False
    assert report.route_rerun_performed is False
    assert report.ask_executed is False
    assert report.final_response_emitted is False
    assert report.provider_invoked is False
    assert report.local_command_executed is False
    assert report.direct_provider_invocation is False
    assert report.direct_file_access_performed is False
    assert report.direct_subprocess_performed is False
    assert report.command_rerun_performed is False
    assert report.autonomous_loop_started is False
    assert report.background_execution_started is False
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.persona_mutated is False
    assert report.external_provider_adapter_implemented is False
    assert report.external_agent_adapter_implemented is False
    assert report.schumpeter_split_introduced is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.raw_provider_output_inline is False
    assert report.raw_transcript_persisted is False
    assert report.llm_judge_used is False
    assert report.next_required_step == "v0.26.3 Provider / Capability Browser"
    assert "workbench_trace_explorer_view" in WORKBENCH_TRACE_EXPLORER_OBJECT_TYPES
    assert "workbench_trace_explorer_view_created" in WORKBENCH_TRACE_EXPLORER_EVENT_TYPES
    assert "creates_pipeline_timeline" in WORKBENCH_TRACE_EXPLORER_RELATION_TYPES
    assert WORKBENCH_TRACE_EXPLORER_EFFECT_TYPES == [
        "read_only_observation",
        "workbench_trace_view_created",
        "workbench_pipeline_timeline_created",
        "workbench_timeline_node_created",
        "workbench_trace_filter_created",
        "workbench_trace_inspection_created",
        "state_candidate_created",
    ]
    assert "stage_rerun_performed" in WORKBENCH_TRACE_EXPLORER_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.26.2"
    assert pig["layer"] == "workspace_agent_workbench"
    assert pig["subject"] == "trace_explorer_pipeline_timeline"
    assert pig["safety_boundary"]["actual_ui_rendered"] is False
    assert pig["safety_boundary"]["provider_invoked"] is False
    assert ocpx["state"] == "workbench_trace_explorer_pipeline_timeline_created"
    assert "WorkbenchTraceExplorerViewState" in ocpx["target_read_models"]

    for command in ["view", "source", "timeline", "stages", "decisions", "filters", "inspect", "report"]:
        assert main(["workbench", "trace", command, "--trace-id", "agent_surface_trace:synthetic-existing"]) == 0
        output = capsys.readouterr().out
        assert "version=v0.26.2" in output
        assert "layer=workspace_agent_workbench" in output
        assert "trace_explorer_view_created=true" in output
        assert "pipeline_timeline_created=true" in output
        assert "stage_nodes_created=true" in output
        assert "decision_nodes_created=true" in output
        assert "relation_edges_created=true" in output
        assert "ready_for_v0_26_3=true" in output
        assert "ready_for_v0_27=false" in output
        assert "actual_ui_rendered=false" in output
        assert "panel_rendered=false" in output
        assert "trace_mutated=false" in output
        assert "stage_rerun_performed=false" in output
        assert "route_rerun_performed=false" in output
        assert "ask_executed=false" in output
        assert "final_response_emitted=false" in output
        assert "provider_invoked=false" in output
        assert "local_command_executed=false" in output
        assert "direct_provider_invocation=false" in output
        assert "direct_file_access_performed=false" in output
        assert "direct_subprocess_performed=false" in output
        assert "command_rerun_performed=false" in output
        assert "autonomous_loop_started=false" in output
        assert "background_execution_started=false" in output
        assert "memory_promoted=false" in output
        assert "persistent_memory_written=false" in output
        assert "persona_mutated=false" in output
        assert "external_provider_adapter_implemented=false" in output
        assert "external_agent_adapter_implemented=false" in output
        assert "schumpeter_split_introduced=false" in output
        assert "credential_exposed=false" in output
        assert "raw_secret_output=false" in output
        assert "raw_provider_output_inline=false" in output
        assert "raw_transcript_persisted=false" in output
        assert "llm_judge_used=false" in output
        assert "next_required_step=v0.26.3 Provider / Capability Browser" in output
