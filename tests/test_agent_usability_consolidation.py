from __future__ import annotations

from chanta_core.agent_surface import (
    AGENT_USABILITY_CONSOLIDATION_VERSION,
    AGENT_USABILITY_EFFECT_TYPES,
    AGENT_USABILITY_EVENT_TYPES,
    AGENT_USABILITY_OBJECT_TYPES,
    AGENT_USABILITY_RELEASE_NAME,
    AgentSurfaceCapabilityMap,
    AgentSurfaceCapabilityMapEntry,
    AgentSurfaceCoverageMatrix,
    AgentSurfaceCoverageMatrixRow,
    AgentSurfaceGap,
    AgentSurfaceGapRegister,
    AgentSurfacePipelineBoundaryReport,
    AgentSurfaceReleaseManifest,
    AgentSurfaceRoadmapBoundaryReport,
    AgentSurfaceSafetyBoundaryReport,
    AgentSurfaceTraceTelemetryCoverageReport,
    AgentUsabilityConsolidationFinding,
    AgentUsabilityConsolidationReport,
    AgentUsabilityConsolidationReportService,
    AgentUsabilityConsolidationSourceService,
    AgentUsabilityFoundationSnapshot,
    AgentUsabilitySubjectComponent,
    AgentV026ReadinessReport,
    AgentWorkbenchHandoffPacket,
)
from chanta_core.cli.main import main


def _parts() -> dict:
    return AgentUsabilityConsolidationReportService().build_all_parts()


def test_usability_consolidation_models_build() -> None:
    parts = _parts()

    assert isinstance(parts["foundation_snapshot"], AgentUsabilityFoundationSnapshot)
    assert isinstance(parts["subject_components"][0], AgentUsabilitySubjectComponent)
    assert isinstance(parts["capability_map"], AgentSurfaceCapabilityMap)
    assert isinstance(parts["capability_map"].entries[0], AgentSurfaceCapabilityMapEntry)
    assert isinstance(parts["coverage_matrix"], AgentSurfaceCoverageMatrix)
    assert isinstance(parts["coverage_matrix"].rows[0], AgentSurfaceCoverageMatrixRow)
    assert isinstance(parts["pipeline_boundary_report"], AgentSurfacePipelineBoundaryReport)
    assert isinstance(parts["safety_boundary_report"], AgentSurfaceSafetyBoundaryReport)
    assert isinstance(parts["trace_telemetry_coverage_report"], AgentSurfaceTraceTelemetryCoverageReport)
    assert isinstance(parts["roadmap_boundary_report"], AgentSurfaceRoadmapBoundaryReport)
    assert isinstance(parts["gap_register"], AgentSurfaceGapRegister)
    assert isinstance(parts["gap_register"].gaps[0], AgentSurfaceGap)
    assert isinstance(parts["release_manifest"], AgentSurfaceReleaseManifest)
    assert isinstance(parts["v026_readiness_report"], AgentV026ReadinessReport)
    assert isinstance(parts["findings"][0], AgentUsabilityConsolidationFinding)
    assert isinstance(parts["report"], AgentUsabilityConsolidationReport)
    assert isinstance(parts["workbench_handoff_packet"], AgentWorkbenchHandoffPacket)


def test_subject_components_and_capability_map_cover_v025_foundation() -> None:
    parts = _parts()
    components = {item.component_type: item for item in parts["subject_components"]}
    capability_map = parts["capability_map"]

    assert AGENT_USABILITY_CONSOLIDATION_VERSION == "v0.25.9"
    assert AGENT_USABILITY_RELEASE_NAME == "Bounded General Agent Surface Foundation v1"
    assert set(components) == {
        "contract",
        "turn_context",
        "intent_task",
        "safety_gate",
        "routing",
        "provider_invocation",
        "response_assembly",
        "ask_repl_surface",
        "trace_telemetry",
        "consolidation",
    }
    assert components["ask_repl_surface"].user_facing is True
    assert components["provider_invocation"].provider_invocation_capable is True
    assert components["trace_telemetry"].trace_capable is True
    assert all(component.external_adapter is False for component in components.values())
    assert all(component.memory_capable is False for component in components.values())
    assert all(component.workbench_ui is False for component in components.values())
    assert capability_map.implemented_count == 10
    assert capability_map.user_facing_count >= 1
    assert capability_map.provider_invocation_capability_count == 1
    assert capability_map.response_emission_capability_count == 1
    assert capability_map.trace_capability_count == 1
    assert capability_map.external_adapter_count == 0
    assert capability_map.memory_capability_count == 0
    assert capability_map.workbench_ui_count == 0
    skill_ids = {skill for entry in capability_map.entries for skill in entry.skill_ids}
    assert "skill:agent_usability_consolidation_view" in skill_ids
    assert "skill:agent_ask" in skill_ids
    assert "skill:agent_trace_record" in skill_ids


def test_coverage_pipeline_safety_and_trace_reports_are_ready() -> None:
    parts = _parts()
    coverage = parts["coverage_matrix"]
    pipeline = parts["pipeline_boundary_report"]
    safety = parts["safety_boundary_report"]
    trace = parts["trace_telemetry_coverage_report"]

    assert coverage.coverage_status == "complete"
    assert coverage.missing_required_coverage_count == 0
    assert len(coverage.rows) == 10
    assert all(row.has_model and row.has_service and row.has_tests and row.has_boundary_tests for row in coverage.rows)
    assert all(row.has_docs and row.has_ocel_mapping and row.has_pig_projection and row.has_ocpx_projection for row in coverage.rows)
    assert pipeline.required_stage_order == [
        "v0.25.1_turn_envelope",
        "v0.25.2_intent_task",
        "v0.25.3_safety_gate",
        "v0.25.4_route_plan_if_allow_route",
        "v0.25.5_provider_invocation_if_required",
        "v0.25.6_response_assembly",
        "v0.25.7_surface_emission",
    ]
    assert pipeline.stage_boundary_passed is True
    assert pipeline.ask_pipeline_available is True
    assert pipeline.repl_surface_available is True
    assert pipeline.response_emission_available is True
    assert pipeline.provider_invocation_via_v0255_only is True
    assert pipeline.local_runtime_via_v024_only is True
    assert pipeline.trace_telemetry_available is True
    assert pipeline.no_direct_bypass is True
    assert pipeline.pipeline_boundary_status == "ready"
    assert safety.status == "passed"
    assert safety.ask_count >= 1
    assert safety.final_response_emission_count >= 1
    assert safety.provider_invocation_count >= 1
    assert safety.trace_record_count >= 1
    assert safety.direct_provider_invocation_count == 0
    assert safety.direct_file_access_count == 0
    assert safety.direct_subprocess_count == 0
    assert safety.command_rerun_count == 0
    assert safety.workspace_workbench_count == 0
    assert safety.memory_promotion_count == 0
    assert safety.raw_transcript_persistence_count == 0
    assert safety.llm_judge_count == 0
    assert trace.coverage_status == "ready"
    assert trace.trace_available is True
    assert trace.ocel_projection_available is True
    assert trace.metric_set_available is True
    assert trace.telemetry_report_available is True
    assert all(trace.stage_trace_coverage.values())
    assert all(trace.decision_trace_coverage.values())
    assert trace.raw_trace_privacy_passed is True


def test_roadmap_gaps_manifest_readiness_and_handoff() -> None:
    parts = _parts()
    roadmap = parts["roadmap_boundary_report"]
    gaps = parts["gap_register"]
    manifest = parts["release_manifest"]
    readiness = parts["v026_readiness_report"]
    handoff = parts["workbench_handoff_packet"]

    assert roadmap.current_track == "v0.25.x Bounded General Agent Surface & Internal Tool Routing"
    assert roadmap.next_track == "v0.26.x Workspace Agent Workbench"
    assert roadmap.next_version == "v0.26.0 Workspace Agent Workbench Contract"
    assert roadmap.v027_memory_continuity_deferred is True
    assert roadmap.v028_public_alpha_schumpeter_split_deferred is True
    assert roadmap.v029_external_provider_adapters_deferred is True
    assert roadmap.v030_external_agent_dominion_deferred is True
    assert roadmap.growthkernel_bridge_deferred is True
    assert roadmap.roadmap_status == "aligned"
    gap_ids = {gap.gap_id.removeprefix("agent_surface_gap:") for gap in gaps.gaps}
    assert {
        "workspace_agent_workbench_not_started",
        "trace_explorer_not_started",
        "provider_browser_not_started",
        "manual_approval_ui_not_started",
        "memory_candidate_continuity_not_started",
        "public_alpha_schumpeter_split_not_started",
        "external_provider_adapters_not_started",
        "external_agent_dominion_bridge_not_started",
        "growthkernel_bridge_not_started",
    } <= gap_ids
    assert gaps.future_track_count == 9
    assert manifest.release_version == "v0.25.9"
    assert manifest.release_name == AGENT_USABILITY_RELEASE_NAME
    assert manifest.included_versions == [f"v0.25.{i}" for i in range(10)]
    for excluded in [
        "Workspace Agent Workbench UI",
        "Memory Candidate & Continuity",
        "External Provider Adapter",
        "External Agent Dominion Bridge",
        "Schumpeter split / company wrapper",
        "GrowthKernel runtime dependency",
        "autonomous loop",
        "background execution",
        "direct provider bypass",
        "direct subprocess",
    ]:
        assert excluded in manifest.excluded_capabilities
    assert manifest.release_status == "releasable"
    assert readiness.target_track == "v0.26.x Workspace Agent Workbench"
    assert readiness.recommended_next_version == "v0.26.0 Workspace Agent Workbench Contract"
    assert readiness.ready_for_v0_26 is True
    assert readiness.substrate_requirements_met is True
    assert readiness.workbench_not_implemented_yet is True
    assert handoff.target_version == "v0.26.0"
    assert "agent_surface_contract" in handoff.workbench_ready_inputs
    assert "agent_pipeline_stage_traces" in handoff.workbench_ready_inputs
    assert "provider_invocation_trace_views" in handoff.workbench_ready_inputs
    assert "safety_boundary_report" in handoff.workbench_ready_inputs
    assert "visual trace explorer" in handoff.not_implemented_in_v0259
    assert "dashboard" in handoff.not_implemented_in_v0259
    assert handoff.handoff_status == "ready"


def test_consolidation_report_flags_and_ocel_pig_ocpx() -> None:
    service = AgentUsabilityConsolidationReportService()
    parts = service.build_all_parts()
    report = parts["report"]
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert report.version == "v0.25.9"
    assert report.release_name == AGENT_USABILITY_RELEASE_NAME
    assert report.readiness_status == "ready"
    assert report.release_status == "releasable"
    assert report.ready_for_v0_26 is True
    assert report.ready_for_v0_27 is False
    assert report.new_ask_executed is False
    assert report.new_repl_turn_executed is False
    assert report.new_final_response_emitted is False
    assert report.new_provider_invocation_performed is False
    assert report.new_local_command_executed is False
    assert report.direct_provider_invocation is False
    assert report.direct_file_access_performed is False
    assert report.direct_subprocess_performed is False
    assert report.command_rerun_performed is False
    assert report.autonomous_loop_started is False
    assert report.background_execution_started is False
    assert report.workspace_workbench_implemented is False
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
    assert report.next_required_step == "v0.26.0 Workspace Agent Workbench Contract"
    assert "agent_usability_foundation_snapshot" in AGENT_USABILITY_OBJECT_TYPES
    assert "agent_usability_consolidation_requested" in AGENT_USABILITY_EVENT_TYPES
    assert "agent_usability_consolidation_created" in AGENT_USABILITY_EFFECT_TYPES
    assert pig["version"] == "v0.25.9"
    assert pig["layer"] == "agent_surface"
    assert pig["subject"] == "general_agent_usability_consolidation"
    assert pig["release_name"] == AGENT_USABILITY_RELEASE_NAME
    assert pig["safety_boundary"]["workspace_workbench_implemented"] is False
    assert pig["next_step"] == "v0.26.0 Workspace Agent Workbench Contract"
    assert ocpx["state"] == "bounded_general_agent_surface_foundation_v1_consolidated"
    assert "AgentUsabilityReleaseState" in ocpx["target_read_models"]
    assert "AgentWorkbenchHandoffState" in ocpx["target_read_models"]


def test_sources_are_read_only_and_do_not_load_raw_material() -> None:
    sources = AgentUsabilityConsolidationSourceService().load_all_sources()

    assert set(sources) >= {
        "contract",
        "turn_context",
        "intent_task",
        "safety_gate",
        "routing",
        "provider_invocation",
        "response_assembly",
        "ask_repl_surface",
        "trace_telemetry",
        "internal_provider_release",
    }
    assert all(source["read_only"] is True for source in sources.values())
    assert all(source["raw_transcript_loaded"] is False for source in sources.values())
    assert all(source["raw_provider_output_loaded"] is False for source in sources.values())
    assert all(source["raw_secret_loaded"] is False for source in sources.values())


def test_cli_usability_commands_render_sanitized_status(capsys) -> None:
    commands = [
        ["agent", "usability", "consolidate"],
        ["agent", "usability", "release-manifest"],
        ["agent", "usability", "readiness", "--target", "v0.26"],
        ["agent", "usability", "safety-boundary"],
        ["agent", "usability", "pipeline-boundary"],
        ["agent", "usability", "trace-coverage"],
        ["agent", "usability", "gaps"],
        ["agent", "usability", "handoff", "--target", "v0.26"],
        ["agent", "usability", "report", "--report-id", "report:test"],
    ]
    for argv in commands:
        assert main(argv) == 0
        output = capsys.readouterr().out
        assert "version=v0.25.9" in output
        assert "release_name=Bounded General Agent Surface Foundation v1" in output
        assert "ready_for_v0_26=true" in output
        assert "ready_for_v0_27=false" in output
        assert "new_ask_executed=false" in output
        assert "new_final_response_emitted=false" in output
        assert "new_provider_invocation_performed=false" in output
        assert "new_local_command_executed=false" in output
        assert "direct_provider_invocation=false" in output
        assert "direct_file_access_performed=false" in output
        assert "direct_subprocess_performed=false" in output
        assert "command_rerun_performed=false" in output
        assert "autonomous_loop_started=false" in output
        assert "workspace_workbench_implemented=false" in output
        assert "memory_promoted=false" in output
        assert "persistent_memory_written=false" in output
        assert "persona_mutated=false" in output
        assert "external_provider_adapter_implemented=false" in output
        assert "schumpeter_split_introduced=false" in output
        assert "credential_exposed=false" in output
        assert "raw_secret_output=false" in output
        assert "raw_provider_output_inline=false" in output
        assert "raw_transcript_persisted=false" in output
        assert "llm_judge_used=false" in output
        assert "next_required_step=v0.26.0 Workspace Agent Workbench Contract" in output
