from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.workspace_agent_workbench.consolidation import (
    WORKBENCH_CONSOLIDATION_EFFECT_TYPES,
    WORKBENCH_CONSOLIDATION_EVENT_TYPES,
    WORKBENCH_CONSOLIDATION_FORBIDDEN_EFFECT_TYPES,
    WORKBENCH_CONSOLIDATION_IMPLEMENTED_SKILL_IDS,
    WORKBENCH_CONSOLIDATION_INCLUDED_VERSIONS,
    WORKBENCH_CONSOLIDATION_OBJECT_TYPES,
    WORKBENCH_CONSOLIDATION_PREVIOUS_SKILL_IDS,
    WORKBENCH_CONSOLIDATION_RELATION_TYPES,
    WORKBENCH_CONSOLIDATION_RELEASE_NAME,
    WORKBENCH_CONSOLIDATION_REQUIRED_GAPS,
    WORKBENCH_CONSOLIDATION_VERSION,
    WORKBENCH_MEMORY_CANDIDATE_READY_INPUTS,
    WorkbenchCapabilityMap,
    WorkbenchCapabilityMapEntry,
    WorkbenchConsolidationFinding,
    WorkbenchConsolidationReport,
    WorkbenchConsolidationReportService,
    WorkbenchCoverageMatrix,
    WorkbenchCoverageMatrixRow,
    WorkbenchDefaultAgentUsabilityGap,
    WorkbenchDefaultAgentUsabilityGapRegister,
    WorkbenchEventQualityConsolidationReport,
    WorkbenchFoundationSnapshot,
    WorkbenchFoundationSubjectComponent,
    WorkbenchInteractionBoundaryReport,
    WorkbenchMemoryCandidateHandoffPacket,
    WorkbenchProcessIntelligenceFeedbackLoopReport,
    WorkbenchReleaseManifest,
    WorkbenchSafetyBoundaryReport,
    WorkbenchTraceCoverageConsolidationReport,
    WorkbenchUsabilityReadinessReport,
    WorkbenchV027ReadinessReport,
)


def _parts() -> dict:
    return WorkbenchConsolidationReportService().build_all_parts()


def test_consolidation_models_build() -> None:
    parts = _parts()

    assert isinstance(parts["foundation_snapshot"], WorkbenchFoundationSnapshot)
    assert isinstance(parts["subject_components"][0], WorkbenchFoundationSubjectComponent)
    assert isinstance(parts["capability_map"], WorkbenchCapabilityMap)
    assert isinstance(parts["capability_map"].entries[0], WorkbenchCapabilityMapEntry)
    assert isinstance(parts["coverage_matrix"], WorkbenchCoverageMatrix)
    assert isinstance(parts["coverage_matrix"].rows[0], WorkbenchCoverageMatrixRow)
    assert isinstance(parts["safety_boundary_report"], WorkbenchSafetyBoundaryReport)
    assert isinstance(parts["interaction_boundary_report"], WorkbenchInteractionBoundaryReport)
    assert isinstance(parts["event_quality_consolidation_report"], WorkbenchEventQualityConsolidationReport)
    assert isinstance(parts["trace_coverage_consolidation_report"], WorkbenchTraceCoverageConsolidationReport)
    assert isinstance(parts["usability_readiness_report"], WorkbenchUsabilityReadinessReport)
    assert isinstance(parts["process_intelligence_feedback_loop_report"], WorkbenchProcessIntelligenceFeedbackLoopReport)
    assert isinstance(parts["gap_register"].gaps[0], WorkbenchDefaultAgentUsabilityGap)
    assert isinstance(parts["gap_register"], WorkbenchDefaultAgentUsabilityGapRegister)
    assert isinstance(parts["v027_readiness_report"], WorkbenchV027ReadinessReport)
    assert isinstance(parts["memory_candidate_handoff_packet"], WorkbenchMemoryCandidateHandoffPacket)
    assert isinstance(parts["release_manifest"], WorkbenchReleaseManifest)
    assert isinstance(parts["findings"][0], WorkbenchConsolidationFinding)
    assert isinstance(parts["report"], WorkbenchConsolidationReport)


def test_foundation_snapshot_subjects_and_skills() -> None:
    parts = _parts()
    snapshot = parts["foundation_snapshot"]
    components = parts["subject_components"]
    component_types = {component.component_type for component in components}

    assert WORKBENCH_CONSOLIDATION_VERSION == "v0.26.9"
    assert WORKBENCH_CONSOLIDATION_RELEASE_NAME == "Workspace Agent Workbench Foundation v1"
    assert WORKBENCH_CONSOLIDATION_IMPLEMENTED_SKILL_IDS == ["skill:workbench_consolidation_view"]
    assert "skill:workbench_snapshot_create" in WORKBENCH_CONSOLIDATION_PREVIOUS_SKILL_IDS
    assert "skill:workbench_ocel_export_create" in WORKBENCH_CONSOLIDATION_PREVIOUS_SKILL_IDS
    assert snapshot.release_name == WORKBENCH_CONSOLIDATION_RELEASE_NAME
    assert snapshot.included_versions == WORKBENCH_CONSOLIDATION_INCLUDED_VERSIONS
    assert "v0.26.0" in snapshot.included_versions
    assert "v0.26.9" in snapshot.included_versions
    assert snapshot.previous_release_ref is not None
    assert snapshot.previous_release_ref["version"] == "v0.25.9"
    assert {
        "contract",
        "view_state_panel_model",
        "trace_explorer",
        "provider_browser",
        "evidence_inspector",
        "approval_console",
        "run_dashboard_session_monitor",
        "command_surface",
        "snapshot_export",
        "consolidation",
    }.issubset(component_types)
    for component in components:
        assert component.ocel_visible is True
        assert component.memory_capable is False
        assert component.external_adapter is False
        assert component.execution_surface is False


def test_capability_map_and_coverage_matrix() -> None:
    parts = _parts()
    capability_map = parts["capability_map"]
    coverage = parts["coverage_matrix"]
    categories = {entry.capability_category for entry in capability_map.entries}
    coverage_versions = {row.version_introduced for row in coverage.rows}

    assert {
        "contract",
        "view_state",
        "trace_inspection",
        "provider_inspection",
        "evidence_inspection",
        "approval_record",
        "dashboard_monitor",
        "command_candidate",
        "snapshot_export",
        "consolidation",
    }.issubset(categories)
    assert capability_map.memory_capability_count == 0
    assert capability_map.external_adapter_count == 0
    assert capability_map.execution_surface_count == 0
    for entry in capability_map.entries:
        assert entry.allowed_effect_types
        assert entry.forbidden_effect_types
        assert entry.mutating is False
        assert entry.executing is False
        assert entry.memory_capable is False
        assert entry.external_adapter is False
    assert {f"v0.26.{index}" for index in range(0, 9)}.issubset(coverage_versions)
    assert coverage.coverage_status == "complete"
    assert coverage.missing_required_coverage_count == 0
    for row in coverage.rows:
        assert row.has_model is True
        assert row.has_service is True
        assert row.has_cli is True
        assert row.has_tests is True
        assert row.has_boundary_tests is True
        assert row.has_docs is True
        assert row.has_ocel_mapping is True
        assert row.has_pig_projection is True
        assert row.has_ocpx_projection is True
        assert row.has_safety_boundary is True


def test_safety_interaction_quality_trace_usability_feedback() -> None:
    parts = _parts()
    safety = parts["safety_boundary_report"]
    interaction = parts["interaction_boundary_report"]
    quality = parts["event_quality_consolidation_report"]
    trace = parts["trace_coverage_consolidation_report"]
    usability = parts["usability_readiness_report"]
    feedback = parts["process_intelligence_feedback_loop_report"]

    for key, value in safety.to_dict().items():
        if key.endswith("_count"):
            assert value == 0
    assert safety.status == "passed"
    assert interaction.trace_view_available is True
    assert interaction.provider_browser_available is True
    assert interaction.evidence_inspector_available is True
    assert interaction.approval_console_available is True
    assert interaction.run_dashboard_available is True
    assert interaction.session_monitor_available is True
    assert interaction.command_candidate_surface_available is True
    assert interaction.snapshot_export_available is True
    assert interaction.do_nothing_candidate_available is True
    assert interaction.approval_rejection_deferral_visible is True
    assert interaction.human_intervention_points_visible is True
    assert interaction.execution_boundary_preserved is True
    assert quality.decision_point_coverage is not None
    assert quality.skill_candidate_coverage is not None
    assert quality.action_candidate_coverage is not None
    assert quality.pig_guidance_coverage is not None
    assert quality.automatic_optimization_performed is False
    assert trace.trace_explorer_coverage is True
    assert trace.provider_browser_coverage is True
    assert trace.evidence_inspector_coverage is True
    assert trace.approval_console_coverage is True
    assert trace.dashboard_coverage is True
    assert trace.command_surface_coverage is True
    assert trace.snapshot_export_coverage is True
    assert usability.skill_candidate_visible is True
    assert usability.action_candidate_visible is True
    assert usability.provider_capability_visible is True
    assert usability.evidence_visible is True
    assert usability.safety_rationale_visible is True
    assert usability.approval_flow_visible is True
    assert usability.command_candidate_visible is True
    assert usability.session_context_refs_visible is True
    assert usability.pig_guidance_visible is True
    assert usability.do_nothing_visible is True
    assert feedback.ocel_event_quality_ready is True
    assert feedback.ocpx_view_readiness_ready is True
    assert feedback.pig_guidance_visibility_ready is True
    assert feedback.workbench_inspection_ready is True
    assert feedback.approval_record_ready is True
    assert feedback.command_candidate_ready is True
    assert feedback.snapshot_export_ready is True
    assert feedback.v027_memory_candidate_input_ready is True


def test_gap_register_v027_handoff_release_and_report() -> None:
    parts = _parts()
    gaps = parts["gap_register"]
    v027 = parts["v027_readiness_report"]
    handoff = parts["memory_candidate_handoff_packet"]
    manifest = parts["release_manifest"]
    report = parts["report"]
    gap_ids = {gap.gap_id.removeprefix("workbench_gap:") for gap in gaps.gaps}

    assert set(WORKBENCH_CONSOLIDATION_REQUIRED_GAPS).issubset(gap_ids)
    assert gaps.blocker_count == 0
    assert gaps.future_track_count == len(gaps.gaps)
    assert v027.target_track == "v0.27.x Memory Candidate & Continuity"
    assert v027.recommended_next_version == "v0.27.0 Memory Candidate & Continuity Contract"
    assert v027.ready_for_v0_27 is True
    assert v027.memory_not_implemented_yet is True
    assert v027.memory_candidate_not_extracted_yet is True
    assert v027.workbench_snapshot_available is True
    assert v027.ocel_export_available is True
    assert v027.session_context_refs_available is True
    assert v027.trace_summary_refs_available is True
    assert v027.evidence_summary_refs_available is True
    assert v027.pig_guidance_refs_available is True
    assert v027.approval_decision_refs_available is True
    assert v027.command_candidate_refs_available is True
    assert v027.failure_cause_refs_available is True
    assert v027.human_intervention_refs_available is True
    assert handoff.target_version == "v0.27.0"
    assert handoff.refs_only is True
    assert handoff.memory_created_now is False
    assert set(WORKBENCH_MEMORY_CANDIDATE_READY_INPUTS).issubset(set(handoff.memory_candidate_ready_inputs))
    assert "memory candidate extraction" in handoff.not_implemented_in_v0269
    assert "memory scoring" in handoff.not_implemented_in_v0269
    assert "memory promotion gate" in handoff.not_implemented_in_v0269
    assert "durable memory write" in handoff.not_implemented_in_v0269
    assert "persona mutation" in handoff.not_implemented_in_v0269
    assert "session continuity engine" in handoff.not_implemented_in_v0269
    assert manifest.release_version == "v0.26.9"
    assert manifest.release_name == WORKBENCH_CONSOLIDATION_RELEASE_NAME
    assert manifest.included_versions == WORKBENCH_CONSOLIDATION_INCLUDED_VERSIONS
    assert "Memory Candidate Extraction" in manifest.excluded_capabilities
    assert "Memory Promotion" in manifest.excluded_capabilities
    assert "Persistent Memory Write" in manifest.excluded_capabilities
    assert "Persona Mutation" in manifest.excluded_capabilities
    assert "Session Continuity Engine" in manifest.excluded_capabilities
    assert "External Provider Adapter" in manifest.excluded_capabilities
    assert "Schumpeter Split / Company Wrapper" in manifest.excluded_capabilities
    assert "pm4py/ocpa runtime adapter" in manifest.excluded_capabilities
    assert "Autonomous Multi-Step Execution Loop" in manifest.excluded_capabilities
    assert "Automatic Retry / Repair" in manifest.excluded_capabilities
    assert "Direct Command Execution" in manifest.excluded_capabilities
    assert "Raw Transcript Persistence / Export" in manifest.excluded_capabilities
    assert manifest.release_status in {"releasable", "releasable_with_warnings"}
    assert report.readiness_status == "ready"
    assert report.release_status == "releasable"
    assert report.ready_for_v0_27 is True
    assert report.ready_for_v0_28 is False


def test_forbidden_flags_ocel_pig_ocpx_and_cli(capsys) -> None:
    service = WorkbenchConsolidationReportService()
    parts = _parts()
    report = parts["report"]
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert report.memory_candidate_created is False
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.persona_mutated is False
    assert report.command_executed is False
    assert report.provider_invoked is False
    assert report.local_command_executed is False
    assert report.file_mutated is False
    assert report.patch_applied is False
    assert report.ask_executed is False
    assert report.final_response_emitted is False
    assert report.route_rerun_performed is False
    assert report.stage_rerun_performed is False
    assert report.automatic_retry_performed is False
    assert report.automatic_repair_performed is False
    assert report.autonomous_loop_started is False
    assert report.external_provider_adapter_implemented is False
    assert report.vendor_adapter_implemented is False
    assert report.pm4py_runtime_dependency_added is False
    assert report.ocpa_runtime_dependency_added is False
    assert report.pig_memory_promoted is False
    assert report.pig_policy_mutated is False
    assert report.pig_executed is False
    assert report.schumpeter_split_introduced is False
    assert report.raw_transcript_persisted is False
    assert report.raw_provider_output_inline is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False
    assert report.next_required_step == "v0.27.0 Memory Candidate & Continuity Contract"
    assert "workbench_foundation_snapshot" in WORKBENCH_CONSOLIDATION_OBJECT_TYPES
    assert "workbench_consolidation_report_created" in WORKBENCH_CONSOLIDATION_EVENT_TYPES
    assert "consolidates_workspace_agent_workbench_foundation" in WORKBENCH_CONSOLIDATION_RELATION_TYPES
    assert "workbench_consolidation_created" in WORKBENCH_CONSOLIDATION_EFFECT_TYPES
    assert "memory_candidate_created" in WORKBENCH_CONSOLIDATION_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.26.9"
    assert pig["subject"] == "workspace_agent_workbench_consolidation"
    assert pig["safety_boundary"]["memory_candidate_created"] is False
    assert ocpx["state"] == "workspace_agent_workbench_foundation_v1_consolidated"
    assert "WorkbenchFoundationSnapshotState" in ocpx["target_read_models"]
    assert "WorkbenchV027ReadinessState" in ocpx["target_read_models"]
    assert "WorkbenchMemoryCandidateHandoffState" in ocpx["target_read_models"]

    assert main(["workbench", "consolidate"]) == 0
    output = capsys.readouterr().out
    assert "version=v0.26.9" in output
    assert "release_name=Workspace Agent Workbench Foundation v1" in output
    assert "ready_for_v0_27=true" in output
    assert "ready_for_v0_28=false" in output
    assert "memory_candidate_created=false" in output
    assert "memory_promoted=false" in output
    assert "command_executed=false" in output
    assert "provider_invoked=false" in output
    assert "pm4py_runtime_dependency_added=false" in output
    assert "ocpa_runtime_dependency_added=false" in output
    assert "raw_transcript_persisted=false" in output
    assert "llm_judge_used=false" in output
