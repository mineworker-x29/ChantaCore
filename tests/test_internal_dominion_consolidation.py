from chanta_core.internal_dominion import (
    DOMINION_EFFECT_TYPES,
    DOMINION_OCEL_EVENT_TYPES,
    DOMINION_OCEL_OBJECT_TYPES,
    DOMINION_OCEL_RELATION_TYPES,
    DOMINION_SEED_SKILL_IDS,
    InternalDominionConsolidationService,
    InternalDominionRoadmapBoundaryReportService,
    InternalDominionSafetyBoundaryReportService,
)


def test_internal_dominion_consolidation_report_can_be_created():
    report = InternalDominionConsolidationService().consolidate()

    assert report.version == "v0.23.9"
    assert report.release_name == "OCEL-native Internal Dominion Foundation v1"
    assert report.readiness_status == "ready"
    assert report.release_status == "releasable"
    assert report.ready_for_v0_24 is True
    assert report.ready_for_v0_25 is False
    assert report.safe_to_dispatch is False
    assert report.provider_api_call_performed is False
    assert report.external_runtime_touched is False
    assert report.dispatch_performed is False
    assert report.authorization_consumed is False
    assert report.live_status_tracking_started is False
    assert report.live_output_fetch_started is False
    assert report.real_external_outcome_recorded is False
    assert report.local_runtime_provider_implemented is False
    assert report.general_agent_usability_implemented is False
    assert report.workspace_agent_workbench_implemented is False
    assert report.memory_candidate_continuity_implemented is False
    assert report.external_provider_adapter_implemented is False
    assert report.schumpeter_split_introduced is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False
    assert report.next_track_recommendation == "v0.24.x Internal Provider / Local Runtime Provider"
    assert report.limitations
    assert report.withdrawal_conditions


def test_foundation_snapshot_includes_v0_23_0_through_v0_23_9_and_subjects():
    report = InternalDominionConsolidationService().consolidate()
    snapshot = report.foundation_snapshot

    assert snapshot is not None
    assert snapshot.included_versions == [
        "v0.23.0",
        "v0.23.1",
        "v0.23.2",
        "v0.23.3",
        "v0.23.4",
        "v0.23.5",
        "v0.23.6",
        "v0.23.7",
        "v0.23.8",
        "v0.23.9",
    ]
    component_types = {item.component_type for item in snapshot.subjects}
    assert {
        "contract",
        "inventory",
        "capability",
        "request_candidate",
        "plan_binding",
        "static_safety",
        "preflight",
        "gate",
        "dispatch_boundary",
        "workbench",
        "consolidation",
    } <= component_types
    for subject in snapshot.subjects:
        assert subject.provider_neutral is True
        assert subject.executing is False
        assert subject.dispatch_enabled is False
        assert subject.provider_api_call_enabled is False
        assert subject.external_runtime_touch_enabled is False
        assert subject.credential_materialization_enabled is False


def test_capability_map_includes_all_dominion_skills_and_no_live_execution():
    report = InternalDominionConsolidationService().consolidate()
    capability_map = report.capability_map

    assert capability_map is not None
    skill_ids = {entry.skill_ids[0] for entry in capability_map.entries}
    assert set(DOMINION_SEED_SKILL_IDS) <= skill_ids
    assert capability_map.implemented_count >= len(DOMINION_SEED_SKILL_IDS)
    for entry in capability_map.entries:
        assert entry.provider_neutral is True
        assert entry.executing is False
        assert "external_runtime_touched" in entry.forbidden_effect_types
        assert "authorization_consumed" in entry.forbidden_effect_types


def test_coverage_matrix_checks_required_columns():
    report = InternalDominionConsolidationService().consolidate()
    matrix = report.coverage_matrix

    assert matrix is not None
    assert matrix.coverage_status == "complete"
    assert matrix.missing_required_coverage_count == 0
    assert len(matrix.rows) >= 9
    for row in matrix.rows:
        assert row.has_model is True
        assert row.has_service is True
        assert row.has_cli is True
        assert row.has_tests is True
        assert row.has_boundary_tests is True
        assert row.has_ocel_mapping is True
        assert row.has_pig_projection is True
        assert row.has_ocpx_projection is True
        assert row.has_workbench_visibility is True
        assert row.has_docs is True


def test_safety_boundary_report_zero_counts_and_blocks_on_dangerous_count():
    service = InternalDominionSafetyBoundaryReportService()
    report = service.build_safety_boundary_report()

    assert report.provider_api_call_count == 0
    assert report.external_runtime_touch_count == 0
    assert report.external_dispatch_count == 0
    assert report.external_run_start_count == 0
    assert report.authorization_consumed_count == 0
    assert report.live_status_tracking_count == 0
    assert report.live_output_fetch_count == 0
    assert report.real_external_outcome_record_count == 0
    assert report.credential_exposure_count == 0
    assert report.raw_secret_output_count == 0
    assert report.local_command_execution_count == 0
    assert report.shell_execution_count == 0
    assert report.network_access_count == 0
    assert report.mcp_connection_count == 0
    assert report.plugin_loading_count == 0
    assert report.llm_judge_count == 0
    assert report.vendor_specific_core_logic_count == 0
    assert report.growthkernel_active_dependency_count == 0
    assert report.premature_local_runtime_provider_count == 0
    assert report.premature_general_agent_usability_count == 0
    assert report.premature_external_provider_adapter_count == 0
    assert report.premature_schumpeter_split_count == 0
    assert report.status == "passed"

    blocked = service.build_safety_boundary_report({"markers": ["provider_api_call"]})
    assert blocked.provider_api_call_count == 1
    assert blocked.status == "blocked"


def test_roadmap_boundary_and_gap_register_and_release_manifest():
    report = InternalDominionConsolidationService().consolidate()
    roadmap = report.roadmap_boundary_report
    gaps = report.gap_register
    manifest = report.release_manifest

    assert roadmap is not None
    assert roadmap.next_track == "v0.24.x Internal Provider / Local Runtime Provider"
    assert roadmap.local_runtime_provider_deferred is True
    assert roadmap.general_agent_usability_deferred is True
    assert roadmap.workspace_workbench_deferred is True
    assert roadmap.memory_continuity_deferred is True
    assert roadmap.public_alpha_schumpeter_split_deferred is True
    assert roadmap.external_provider_adapters_deferred is True
    assert roadmap.growthkernel_bridge_deferred is True
    assert roadmap.roadmap_status == "aligned"

    assert gaps is not None
    gap_ids = {item.gap_id for item in gaps.gaps}
    assert {
        "internal_provider_local_runtime_not_started",
        "general_agent_usability_not_started",
        "workspace_agent_workbench_not_started",
        "memory_candidate_continuity_not_started",
        "public_alpha_schumpeter_split_not_started",
        "external_provider_adapters_not_started",
        "live_provider_preflight_not_started",
        "actual_bounded_dispatch_not_started",
        "real_status_tracking_not_started",
        "real_external_outcome_recording_not_started",
        "growthkernel_bridge_not_started",
    } <= gap_ids
    assert gaps.future_track_count >= 11
    assert gaps.blocker_count == 0

    assert manifest is not None
    assert manifest.release_version == "v0.23.9"
    assert manifest.release_name == "OCEL-native Internal Dominion Foundation v1"
    assert "v0.23.0" in manifest.included_versions
    assert "v0.23.9" in manifest.included_versions
    assert "actual external dispatch" in manifest.excluded_capabilities
    assert "provider API execution" in manifest.excluded_capabilities
    assert "external runtime touch" in manifest.excluded_capabilities
    assert "authorization consumption" in manifest.excluded_capabilities
    assert "live status tracking" in manifest.excluded_capabilities
    assert "live output fetch" in manifest.excluded_capabilities
    assert "real external outcome record" in manifest.excluded_capabilities
    assert "Local Runtime Provider" in manifest.excluded_capabilities
    assert "General Agent Usability" in manifest.excluded_capabilities
    assert "Workspace Agent Workbench" in manifest.excluded_capabilities
    assert "Memory Candidate / Continuity" in manifest.excluded_capabilities
    assert "External Provider Adapter" in manifest.excluded_capabilities
    assert "Schumpeter split / company wrapper" in manifest.excluded_capabilities
    assert "GrowthKernel runtime dependency" in manifest.excluded_capabilities
    assert manifest.release_status == "releasable"


def test_report_blocks_when_dangerous_source_marker_is_present():
    report = InternalDominionConsolidationService().build_report({"markers": ["dispatch"]})

    assert report.readiness_status == "blocked"
    assert report.release_status == "blocked"
    assert report.ready_for_v0_24 is False
    assert any(item.finding_type == "dispatch_detected" for item in report.findings)


def test_workbench_snapshot_is_read_only():
    service = InternalDominionConsolidationService()
    snapshot = service.build_workbench_snapshot()

    assert snapshot.version == "v0.23.9"
    assert snapshot.read_only is True
    assert snapshot.mutation_performed is False
    assert snapshot.subject_summary
    assert snapshot.safety_summary
    assert snapshot.roadmap_summary
    assert snapshot.gap_summary
    assert snapshot.next_track_recommendation == "v0.24.x Internal Provider / Local Runtime Provider"


def test_ocel_mapping_exists_for_consolidation():
    assert "internal_dominion_foundation_snapshot" in DOMINION_OCEL_OBJECT_TYPES
    assert "internal_dominion_subject_component" in DOMINION_OCEL_OBJECT_TYPES
    assert "internal_dominion_capability_map" in DOMINION_OCEL_OBJECT_TYPES
    assert "internal_dominion_capability_map_entry" in DOMINION_OCEL_OBJECT_TYPES
    assert "internal_dominion_coverage_matrix" in DOMINION_OCEL_OBJECT_TYPES
    assert "internal_dominion_coverage_matrix_row" in DOMINION_OCEL_OBJECT_TYPES
    assert "internal_dominion_safety_boundary_report" in DOMINION_OCEL_OBJECT_TYPES
    assert "internal_dominion_roadmap_boundary_report" in DOMINION_OCEL_OBJECT_TYPES
    assert "internal_dominion_gap" in DOMINION_OCEL_OBJECT_TYPES
    assert "internal_dominion_gap_register" in DOMINION_OCEL_OBJECT_TYPES
    assert "internal_dominion_release_manifest" in DOMINION_OCEL_OBJECT_TYPES
    assert "internal_dominion_consolidation_finding" in DOMINION_OCEL_OBJECT_TYPES
    assert "internal_dominion_consolidation_report" in DOMINION_OCEL_OBJECT_TYPES
    assert "internal_dominion_workbench_snapshot" in DOMINION_OCEL_OBJECT_TYPES

    assert "internal_dominion_consolidation_requested" in DOMINION_OCEL_EVENT_TYPES
    assert "internal_dominion_sources_loaded" in DOMINION_OCEL_EVENT_TYPES
    assert "internal_dominion_subject_components_created" in DOMINION_OCEL_EVENT_TYPES
    assert "internal_dominion_capability_map_created" in DOMINION_OCEL_EVENT_TYPES
    assert "internal_dominion_coverage_matrix_created" in DOMINION_OCEL_EVENT_TYPES
    assert "internal_dominion_safety_boundary_report_created" in DOMINION_OCEL_EVENT_TYPES
    assert "internal_dominion_roadmap_boundary_report_created" in DOMINION_OCEL_EVENT_TYPES
    assert "internal_dominion_gap_register_created" in DOMINION_OCEL_EVENT_TYPES
    assert "internal_dominion_release_manifest_created" in DOMINION_OCEL_EVENT_TYPES
    assert "internal_dominion_consolidation_report_created" in DOMINION_OCEL_EVENT_TYPES
    assert "internal_dominion_workbench_snapshot_created" in DOMINION_OCEL_EVENT_TYPES
    assert "internal_dominion_release_ready" in DOMINION_OCEL_EVENT_TYPES
    assert "internal_dominion_release_warning" in DOMINION_OCEL_EVENT_TYPES
    assert "internal_dominion_release_blocked" in DOMINION_OCEL_EVENT_TYPES

    assert "consolidates_internal_dominion_foundation" in DOMINION_OCEL_RELATION_TYPES
    assert "summarizes_dominion_subject" in DOMINION_OCEL_RELATION_TYPES
    assert "maps_dominion_capability" in DOMINION_OCEL_RELATION_TYPES
    assert "checks_dominion_coverage" in DOMINION_OCEL_RELATION_TYPES
    assert "checks_dominion_safety_boundary" in DOMINION_OCEL_RELATION_TYPES
    assert "checks_dominion_roadmap_boundary" in DOMINION_OCEL_RELATION_TYPES
    assert "registers_dominion_gap" in DOMINION_OCEL_RELATION_TYPES
    assert "declares_internal_dominion_release_manifest" in DOMINION_OCEL_RELATION_TYPES
    assert "produces_internal_dominion_consolidation_report" in DOMINION_OCEL_RELATION_TYPES
    assert "produces_internal_dominion_workbench_snapshot" in DOMINION_OCEL_RELATION_TYPES
    assert "recommends_v0_24_internal_provider" in DOMINION_OCEL_RELATION_TYPES
    assert "defers_public_alpha_schumpeter_split_to_v0_28" in DOMINION_OCEL_RELATION_TYPES
    assert "defers_growthkernel_bridge_to_later_track" in DOMINION_OCEL_RELATION_TYPES
    assert "derived_from_v0_23_8_dispatch_boundary" in DOMINION_OCEL_RELATION_TYPES

    assert {"read_only_observation", "state_candidate_created"} <= set(DOMINION_EFFECT_TYPES)
    assert "consolidation_state_created" in DOMINION_EFFECT_TYPES
    assert "workbench_snapshot_created" in DOMINION_EFFECT_TYPES
    assert "external_runtime_touched" not in DOMINION_EFFECT_TYPES
    assert "authorization_consumed" not in DOMINION_EFFECT_TYPES


def test_pig_and_ocpx_projection_build_with_v0_23_9_coverage():
    service = InternalDominionConsolidationService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert pig["version"] == "v0.23.9"
    assert pig["layer"] == "internal_dominion"
    assert pig["subject"] == "internal_dominion_consolidation_release_readiness"
    assert pig["release_name"] == "OCEL-native Internal Dominion Foundation v1"
    assert "consolidation is not dispatch" in pig["principles"]
    assert "release readiness is not provider adapter implementation" in pig["principles"]
    assert pig["safety_boundary"]["safe_to_dispatch"] is False
    assert pig["safety_boundary"]["provider_api_call_performed"] is False
    assert pig["safety_boundary"]["external_runtime_touched"] is False
    assert pig["safety_boundary"]["dispatch_performed"] is False
    assert pig["safety_boundary"]["authorization_consumed"] is False
    assert pig["safety_boundary"]["live_status_tracking_started"] is False
    assert pig["safety_boundary"]["live_output_fetch_started"] is False
    assert pig["safety_boundary"]["real_external_outcome_recorded"] is False
    assert pig["safety_boundary"]["credential_exposed"] is False
    assert pig["safety_boundary"]["local_runtime_provider_implemented"] is False
    assert pig["safety_boundary"]["general_agent_usability_implemented"] is False
    assert pig["safety_boundary"]["workspace_agent_workbench_implemented"] is False
    assert pig["safety_boundary"]["memory_candidate_continuity_implemented"] is False
    assert pig["safety_boundary"]["external_provider_adapter_implemented"] is False
    assert pig["safety_boundary"]["schumpeter_split_introduced"] is False
    assert pig["safety_boundary"]["llm_judge_enabled"] is False
    assert pig["roadmap"]["v0.24"] == "Internal Provider / Local Runtime Provider"
    assert pig["roadmap"]["v0.25"] == "General Agent Usability & Tool Routing"
    assert pig["roadmap"]["v0.26"] == "Workspace Agent Workbench"
    assert pig["roadmap"]["v0.27"] == "Memory Candidate & Continuity"
    assert pig["roadmap"]["v0.28"] == "Public Alpha / Schumpeter Split Preparation"
    assert pig["roadmap"]["v0.29+"] == "External Skill / External Provider Adapters"

    assert ocpx["state"] == "internal_dominion_foundation_v1_consolidated"
    assert ocpx["version"] == "v0.23.9"
    assert "InternalDominionReleaseState" in ocpx["target_read_models"]
    assert "InternalDominionConsolidationState" in ocpx["target_read_models"]
    assert "InternalDominionWorkbenchState" in ocpx["target_read_models"]
    assert "InternalDominionReadinessState" in ocpx["target_read_models"]
    assert "DominionRoadmapBoundaryState" in ocpx["target_read_models"]
    assert "V024ReadinessState" in ocpx["target_read_models"]


def test_premature_roadmap_markers_block():
    report = InternalDominionRoadmapBoundaryReportService().build_roadmap_boundary_report(
        {"markers": ["premature_local_runtime_provider"]}
    )

    assert report.roadmap_status == "blocked"
    assert report.findings
