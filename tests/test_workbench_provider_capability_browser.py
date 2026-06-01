from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.workspace_agent_workbench import (
    WORKBENCH_PROVIDER_BROWSER_EFFECT_TYPES,
    WORKBENCH_PROVIDER_BROWSER_EVENT_TYPES,
    WORKBENCH_PROVIDER_BROWSER_FORBIDDEN_EFFECT_TYPES,
    WORKBENCH_PROVIDER_BROWSER_FUTURE_SKILL_IDS,
    WORKBENCH_PROVIDER_BROWSER_IMPLEMENTED_SKILL_IDS,
    WORKBENCH_PROVIDER_BROWSER_OBJECT_TYPES,
    WORKBENCH_PROVIDER_BROWSER_RELATION_TYPES,
    WORKBENCH_PROVIDER_BROWSER_VERSION,
    WorkbenchCapabilityCard,
    WorkbenchCapabilityReadinessView,
    WorkbenchHumanInterventionPointRef,
    WorkbenchProviderBoundaryRiskView,
    WorkbenchProviderBoundaryView,
    WorkbenchProviderBrowserFinding,
    WorkbenchProviderBrowserPolicy,
    WorkbenchProviderBrowserPrerequisiteSourceService,
    WorkbenchProviderBrowserReport,
    WorkbenchProviderBrowserReportService,
    WorkbenchProviderBrowserRequest,
    WorkbenchProviderBrowserView,
    WorkbenchProviderCard,
    WorkbenchProviderFailureModeView,
    WorkbenchProviderInspectionPolicy,
    WorkbenchProviderInspectionSummary,
    WorkbenchProviderPIGGuidanceView,
    WorkbenchProviderRouteCompatibilityRow,
    WorkbenchProviderSelectionRationaleView,
    WorkbenchProviderSourceView,
    WorkbenchRouteCompatibilityMatrix,
)


def _parts() -> dict:
    return WorkbenchProviderBrowserReportService().build_all_parts()


def test_provider_browser_models_build() -> None:
    parts = _parts()

    assert isinstance(parts["policy"], WorkbenchProviderBrowserPolicy)
    assert isinstance(parts["request"], WorkbenchProviderBrowserRequest)
    assert isinstance(parts["source_view"], WorkbenchProviderSourceView)
    assert isinstance(parts["provider_browser_view"], WorkbenchProviderBrowserView)
    assert isinstance(parts["provider_cards"][0], WorkbenchProviderCard)
    assert isinstance(parts["capability_cards"][0], WorkbenchCapabilityCard)
    assert isinstance(parts["boundary_views"][0], WorkbenchProviderBoundaryView)
    assert isinstance(parts["readiness_views"][0], WorkbenchCapabilityReadinessView)
    assert isinstance(parts["route_compatibility_matrix"], WorkbenchRouteCompatibilityMatrix)
    assert isinstance(parts["route_compatibility_matrix"].rows[0], WorkbenchProviderRouteCompatibilityRow)
    assert isinstance(parts["selection_rationale_views"][0], WorkbenchProviderSelectionRationaleView)
    assert isinstance(parts["boundary_risk_views"][0], WorkbenchProviderBoundaryRiskView)
    assert isinstance(parts["pig_guidance_views"][0], WorkbenchProviderPIGGuidanceView)
    assert isinstance(parts["failure_mode_views"][0], WorkbenchProviderFailureModeView)
    assert isinstance(parts["human_intervention_points"][0], WorkbenchHumanInterventionPointRef)
    assert isinstance(parts["inspection_policy"], WorkbenchProviderInspectionPolicy)
    assert isinstance(parts["inspection_summary"], WorkbenchProviderInspectionSummary)
    assert isinstance(parts["findings"][0], WorkbenchProviderBrowserFinding)
    assert isinstance(parts["report"], WorkbenchProviderBrowserReport)


def test_sources_skills_and_policy_are_provider_browser_view_only() -> None:
    parts = _parts()
    sources = WorkbenchProviderBrowserPrerequisiteSourceService().load_sources()
    policy = parts["policy"]

    assert WORKBENCH_PROVIDER_BROWSER_VERSION == "v0.26.3"
    assert WORKBENCH_PROVIDER_BROWSER_IMPLEMENTED_SKILL_IDS == ["skill:workbench_provider_browser_view"]
    assert "skill:workbench_evidence_inspector_view" in WORKBENCH_PROVIDER_BROWSER_FUTURE_SKILL_IDS
    assert "skill:workbench_approval_console_view" in WORKBENCH_PROVIDER_BROWSER_FUTURE_SKILL_IDS
    assert "skill:workbench_ocel_export_create" in WORKBENCH_PROVIDER_BROWSER_FUTURE_SKILL_IDS
    assert sources["workbench_view_state"] is not None
    assert sources["provider_browser_panel_model"].panel_type == "provider_browser"
    assert sources["provider_registry"] is not None
    assert sources["capability_surfaces"]
    assert sources["route_report"] is not None
    assert sources["provider_selection"] is not None
    assert sources["pig_guidance_refs"]
    assert policy.provider_browser_enabled is True
    assert policy.capability_browser_enabled is True
    assert policy.provider_selection_rationale_enabled is True
    assert policy.route_compatibility_view_enabled is True
    assert policy.boundary_risk_view_enabled is True
    assert policy.pig_guidance_view_enabled is True
    assert policy.human_intervention_point_view_enabled is True
    assert policy.actual_ui_rendering_enabled is False
    assert policy.panel_rendering_enabled is False
    assert policy.provider_invocation_enabled is False
    assert policy.provider_test_run_enabled is False
    assert policy.external_adapter_enabled is False
    assert policy.vendor_adapter_enabled is False
    assert policy.pm4py_runtime_dependency_enabled is False
    assert policy.ocpa_runtime_dependency_enabled is False
    assert policy.ask_execution_enabled is False
    assert policy.response_emission_enabled is False
    assert policy.local_runtime_execution_enabled is False
    assert policy.memory_promotion_enabled is False
    assert policy.persistent_memory_write_enabled is False
    assert policy.persona_mutation_enabled is False
    assert policy.refs_only_by_default is True
    assert policy.raw_provider_output_inline_forbidden is True
    assert policy.raw_transcript_inline_forbidden is True
    assert policy.raw_secret_inline_forbidden is True
    assert policy.credential_inline_forbidden is True
    assert policy.private_path_sanitization_required is True
    assert policy.pig_guidance_is_not_memory is True
    assert policy.pig_guidance_is_not_execution is True
    assert policy.pig_guidance_is_not_policy_mutation is True
    assert policy.ocel_visible is True


def test_source_view_cards_and_capabilities_are_refs_only() -> None:
    parts = _parts()
    source = parts["source_view"]
    provider_card = parts["provider_cards"][0]
    capability_card = parts["capability_cards"][0]

    assert source.provider_registry_ref is not None
    assert source.capability_surface_ref is not None
    assert source.provider_capability_refs
    assert source.provider_selection_refs
    assert source.route_plan_refs
    assert source.safety_gate_refs
    assert source.provider_count >= 9
    assert source.capability_count >= 20
    assert source.external_adapter_count == 0
    assert source.vendor_adapter_count == 0
    assert source.raw_provider_output_included is False
    assert source.raw_transcript_included is False
    assert source.raw_secret_included is False
    assert source.private_full_path_included is False
    assert provider_card.provider_type in {
        "workspace_read_provider",
        "repository_search_provider",
        "file_read_provider",
        "ocel_inspection_provider",
        "pig_inspection_provider",
        "ocpx_projection_provider",
        "local_runtime_provider",
        "diagnostic_provider",
        "candidate_generation_provider",
        "unknown",
    }
    assert provider_card.capability_count > 0
    assert provider_card.boundary_summary
    assert provider_card.readiness_summary
    assert provider_card.route_compatibility_summary
    assert provider_card.risk_summary
    assert provider_card.provider_invocation_allowed_now is False
    assert provider_card.provider_test_run_allowed_now is False
    assert provider_card.external_adapter is False
    assert provider_card.vendor_adapter is False
    assert provider_card.raw_provider_output_included is False
    assert capability_card.provider_id == provider_card.provider_id
    assert capability_card.read_only in {True, False}
    assert capability_card.requires_safety_gate in {True, False}
    assert capability_card.requires_v024_gate in {True, False}
    assert capability_card.allowed_for_route_plan is True
    assert capability_card.invocation_enabled_now is False
    assert capability_card.executable_now is False
    assert capability_card.external_adapter is False


def test_boundary_readiness_matrix_rationale_and_risk_views() -> None:
    parts = _parts()
    boundary = parts["boundary_views"][0]
    readiness = parts["readiness_views"][0]
    matrix = parts["route_compatibility_matrix"]
    row = matrix.rows[0]
    rationale = parts["selection_rationale_views"][0]
    risk = parts["boundary_risk_views"][0]

    assert boundary.boundary_type in {
        "read_only_boundary",
        "file_read_boundary",
        "process_inspection_boundary",
        "local_runtime_boundary",
        "safety_gate_boundary",
        "provider_policy_boundary",
        "evidence_boundary",
        "unknown",
    }
    assert boundary.required_policies
    assert "direct_provider_invocation" in boundary.forbidden_bypasses
    assert boundary.requires_v0255_invocation is True
    assert boundary.requires_v0247_gate in {True, False}
    assert boundary.direct_invocation_forbidden is True
    assert boundary.boundary_status == "ready"
    assert readiness.readiness_status in {
        "ready_for_route_plan",
        "ready_for_invocation_via_v0255",
        "requires_gate",
        "partial",
        "missing",
        "blocked",
        "future_track",
    }
    assert readiness.readiness_reason
    assert readiness.required_boundaries
    assert readiness.not_execution_ready_by_itself is True
    assert matrix.rows
    assert matrix.route_kind_count >= 1
    assert matrix.provider_count >= 1
    assert matrix.compatibility_status == "ready"
    assert row.provider_id
    assert row.route_kind
    assert row.compatibility_reason
    assert row.required_boundaries
    assert row.pig_guidance_refs
    assert row.human_intervention_required in {True, False}
    assert rationale.selected in {True, False}
    assert rationale.rejected in {True, False}
    assert rationale.deferred in {True, False}
    assert rationale.selection_reason
    assert rationale.ranking_basis
    assert rationale.route_context_refs
    assert rationale.safety_context_refs
    assert rationale.pig_guidance_refs
    assert risk.risk_level in {"none", "low", "medium", "high", "blocked", "unknown"}
    assert "provider_boundary" in risk.risk_categories
    assert risk.risk_summary
    assert risk.mitigation_boundary_refs
    assert risk.human_intervention_recommended in {True, False}


def test_pig_failure_intervention_inspection_and_report_are_non_executing() -> None:
    parts = _parts()
    pig = parts["pig_guidance_views"][0]
    failure = parts["failure_mode_views"][0]
    intervention = parts["human_intervention_points"][0]
    inspection_policy = parts["inspection_policy"]
    inspection = parts["inspection_summary"]
    report = parts["report"]

    assert pig.guidance_type in {"recommendation", "warning", "candidate", "rationale", "pattern_summary", "unknown"}
    assert pig.guidance_summary
    assert pig.related_decision_point_refs
    assert pig.pig_guidance_is_memory is False
    assert pig.pig_guidance_mutates_policy is False
    assert pig.pig_guidance_executes is False
    assert failure.known_failure_modes
    assert failure.last_failure_refs
    assert failure.failure_cause_refs
    assert failure.recovery_guidance_refs
    assert failure.auto_rerun_enabled is False
    assert failure.automatic_repair_enabled is False
    assert failure.provider_test_run_performed is False
    assert intervention.intervention_type in {
        "approval_required",
        "manual_review_recommended",
        "clarification_required",
        "risk_acceptance_required",
        "boundary_check_required",
        "failure_review_required",
        "unknown",
    }
    assert intervention.reason
    assert intervention.approval_created_now is False
    assert intervention.execution_triggered_now is False
    assert intervention.ocel_visible is True
    assert inspection_policy.inspection_is_read_only is True
    assert inspection_policy.provider_invocation_forbidden is True
    assert inspection_policy.provider_test_run_forbidden is True
    assert inspection_policy.external_adapter_forbidden is True
    assert inspection.summary_status == "ready"
    assert inspection.raw_provider_output_included is False
    assert inspection.raw_secret_included is False
    assert report.report_status == "passed"
    assert report.ready_for_v0_26_4 is True
    assert report.ready_for_v0_27 is False
    assert report.provider_browser_view_created is True
    assert report.provider_cards_created is True
    assert report.capability_cards_created is True
    assert report.boundary_views_created is True
    assert report.readiness_views_created is True
    assert report.route_compatibility_matrix_created is True
    assert report.selection_rationale_views_created is True
    assert report.boundary_risk_views_created is True
    assert report.pig_guidance_views_created is True
    assert report.human_intervention_points_created is True
    assert report.actual_ui_rendered is False
    assert report.panel_rendered is False
    assert report.provider_invoked is False
    assert report.provider_test_run_performed is False
    assert report.provider_boundary_bypassed is False
    assert report.external_provider_adapter_implemented is False
    assert report.external_agent_adapter_implemented is False
    assert report.vendor_adapter_implemented is False
    assert report.pm4py_runtime_dependency_added is False
    assert report.ocpa_runtime_dependency_added is False
    assert report.pig_memory_promoted is False
    assert report.pig_policy_mutated is False
    assert report.pig_executed is False
    assert report.ask_executed is False
    assert report.final_response_emitted is False
    assert report.local_command_executed is False
    assert report.direct_provider_invocation is False
    assert report.direct_file_access_performed is False
    assert report.direct_subprocess_performed is False
    assert report.command_rerun_performed is False
    assert report.automatic_repair_performed is False
    assert report.autonomous_loop_started is False
    assert report.background_execution_started is False
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.persona_mutated is False
    assert report.schumpeter_split_introduced is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.raw_provider_output_inline is False
    assert report.raw_transcript_persisted is False
    assert report.llm_judge_used is False
    assert report.next_required_step == "v0.26.4 Evidence / Report Inspector"


def test_ocel_pig_ocpx_and_cli_are_wired(capsys) -> None:
    parts = _parts()
    pig = parts["pig_report"]
    ocpx = parts["ocpx_projection"]

    assert "workbench_provider_browser_policy" in WORKBENCH_PROVIDER_BROWSER_OBJECT_TYPES
    assert "workbench_provider_browser_view_created" in WORKBENCH_PROVIDER_BROWSER_EVENT_TYPES
    assert "creates_provider_browser_view" in WORKBENCH_PROVIDER_BROWSER_RELATION_TYPES
    assert set(ocpx["effect_types"]) == set(WORKBENCH_PROVIDER_BROWSER_EFFECT_TYPES)
    assert not set(ocpx["effect_types"]).intersection(WORKBENCH_PROVIDER_BROWSER_FORBIDDEN_EFFECT_TYPES)
    assert pig["version"] == "v0.26.3"
    assert pig["layer"] == "workspace_agent_workbench"
    assert pig["subject"] == "provider_capability_browser"
    assert pig["safety_boundary"]["provider_invoked"] is False
    assert pig["safety_boundary"]["provider_test_run_performed"] is False
    assert pig["safety_boundary"]["pig_memory_promoted"] is False
    assert ocpx["state"] == "workbench_provider_capability_browser_created"
    assert "WorkbenchProviderBrowserViewState" in ocpx["target_read_models"]

    assert main(["workbench", "providers", "view"]) == 0
    output = capsys.readouterr().out
    assert "version=v0.26.3" in output
    assert "layer=workspace_agent_workbench" in output
    assert "provider_browser_view_created=true" in output
    assert "provider_invoked=false" in output
    assert "provider_test_run_performed=false" in output
    assert "pig_memory_promoted=false" in output
    assert "raw_provider_output_inline=false" in output
    assert "llm_judge_used=false" in output
    assert "next_required_step=v0.26.4 Evidence / Report Inspector" in output

    for command in [
        "cards",
        "capabilities",
        "boundaries",
        "readiness",
        "route-compatibility",
        "rationale",
        "pig-guidance",
        "intervention-points",
        "inspect",
        "report",
    ]:
        assert main(["workbench", "providers", command]) == 0
