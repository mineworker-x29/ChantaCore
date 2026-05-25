from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.workspace_agent_workbench import (
    WORKBENCH_CONTRACT_EFFECT_TYPES,
    WORKBENCH_CONTRACT_EVENT_TYPES,
    WORKBENCH_CONTRACT_OBJECT_TYPES,
    WORKBENCH_CONTRACT_FUTURE_SKILL_IDS,
    WORKBENCH_CONTRACT_IMPLEMENTED_SKILL_IDS,
    WORKBENCH_CONTRACT_RELATION_TYPES,
    WORKBENCH_CONTRACT_VERSION,
    WorkbenchActionBoundaryPolicy,
    WorkbenchApprovalPolicy,
    WorkbenchCommandBoundaryPolicy,
    WorkbenchContractFinding,
    WorkbenchContractPrerequisiteSourceService,
    WorkbenchContractReport,
    WorkbenchContractReportService,
    WorkbenchOCELVisibilityContract,
    WorkbenchPanelCategoryPolicy,
    WorkbenchPanelContract,
    WorkbenchReadOnlyInspectionPolicy,
    WorkbenchRoadmapBoundary,
    WorkbenchSnapshotPolicy,
    WorkbenchSurfaceMode,
    WorkbenchTracePrivacyPolicy,
    WorkbenchViewPermissionPolicy,
    WorkspaceAgentWorkbenchContract,
)


def _parts() -> dict:
    return WorkbenchContractReportService().build_all_parts()


def test_workbench_contract_models_build() -> None:
    parts = _parts()

    assert isinstance(parts["contract"], WorkspaceAgentWorkbenchContract)
    assert isinstance(parts["surface_modes"][0], WorkbenchSurfaceMode)
    assert isinstance(parts["panel_contracts"][0], WorkbenchPanelContract)
    assert isinstance(parts["panel_category_policy"], WorkbenchPanelCategoryPolicy)
    assert isinstance(parts["view_permission_policy"], WorkbenchViewPermissionPolicy)
    assert isinstance(parts["action_boundary_policy"], WorkbenchActionBoundaryPolicy)
    assert isinstance(parts["read_only_inspection_policy"], WorkbenchReadOnlyInspectionPolicy)
    assert isinstance(parts["approval_policy"], WorkbenchApprovalPolicy)
    assert isinstance(parts["command_boundary_policy"], WorkbenchCommandBoundaryPolicy)
    assert isinstance(parts["snapshot_policy"], WorkbenchSnapshotPolicy)
    assert isinstance(parts["trace_privacy_policy"], WorkbenchTracePrivacyPolicy)
    assert isinstance(parts["ocel_visibility_contract"], WorkbenchOCELVisibilityContract)
    assert isinstance(parts["roadmap_boundary"], WorkbenchRoadmapBoundary)
    assert isinstance(parts["findings"][0], WorkbenchContractFinding)
    assert isinstance(parts["report"], WorkbenchContractReport)


def test_contract_identity_and_source_loading() -> None:
    parts = _parts()
    contract = parts["contract"]
    sources = WorkbenchContractPrerequisiteSourceService().load_sources()

    assert WORKBENCH_CONTRACT_VERSION == "v0.26.0"
    assert contract.version == "v0.26.0"
    assert contract.layer == "workspace_agent_workbench"
    assert contract.release_track == "Workspace Agent Workbench"
    assert contract.status == "contract_only"
    assert WORKBENCH_CONTRACT_IMPLEMENTED_SKILL_IDS == ["skill:workspace_agent_workbench_contract_view"]
    assert "skill:workbench_view_state_create" in WORKBENCH_CONTRACT_FUTURE_SKILL_IDS
    assert "skill:workbench_trace_explorer_view" in WORKBENCH_CONTRACT_FUTURE_SKILL_IDS
    assert "skill:workbench_ocel_export_create" in WORKBENCH_CONTRACT_FUTURE_SKILL_IDS
    assert contract.source_release_ref is not None
    assert contract.source_release_ref["version"] == "v0.25.9"
    assert set(sources) >= {
        "consolidation_report",
        "release_manifest",
        "v026_readiness",
        "workbench_handoff",
        "agent_surface_contract",
        "trace_telemetry_report",
        "skill_registry",
        "provider_registry",
    }
    assert all(source["read_only"] is True for source in sources.values())
    assert all(source["raw_transcript_loaded"] is False for source in sources.values())
    assert all(source["raw_provider_output_loaded"] is False for source in sources.values())
    assert all(source["raw_secret_loaded"] is False for source in sources.values())


def test_surface_modes_are_contract_only_or_future_track() -> None:
    modes = {mode.mode_name: mode for mode in _parts()["surface_modes"]}

    assert set(modes) == {
        "contract_view",
        "trace_explorer_future",
        "pipeline_timeline_future",
        "provider_browser_future",
        "evidence_inspector_future",
        "safety_gate_view_future",
        "approval_console_future",
        "run_dashboard_future",
        "session_monitor_future",
        "command_surface_future",
        "snapshot_export_future",
        "blocked",
        "unknown",
    }
    assert modes["contract_view"].implementation_status == "contract_only"
    assert modes["trace_explorer_future"].activation_version == "v0.26.2"
    assert modes["provider_browser_future"].activation_version == "v0.26.3"
    assert modes["evidence_inspector_future"].activation_version == "v0.26.4"
    assert modes["approval_console_future"].activation_version == "v0.26.5"
    assert modes["run_dashboard_future"].activation_version == "v0.26.6"
    assert modes["command_surface_future"].activation_version == "v0.26.7"
    assert modes["snapshot_export_future"].activation_version == "v0.26.8"
    for mode_name, mode in modes.items():
        assert mode.implementation_status in {"contract_only", "future_track", "disabled", "blocked"}
        if mode_name.endswith("_future"):
            assert mode.execution_capable_future is False
            assert mode.memory_capable_future is False
            assert mode.external_adapter_capable_future is False


def test_panel_contracts_cover_required_future_panels() -> None:
    panels = {panel.panel_type: panel for panel in _parts()["panel_contracts"]}

    assert set(panels) == {
        "trace_explorer",
        "pipeline_timeline",
        "provider_browser",
        "evidence_inspector",
        "safety_gate_view",
        "approval_console",
        "run_dashboard",
        "session_monitor",
        "command_surface",
        "snapshot_export",
        "ocel_projection",
        "telemetry_metrics",
    }
    assert panels["trace_explorer"].activation_version == "v0.26.2"
    assert panels["provider_browser"].activation_version == "v0.26.3"
    assert panels["command_surface"].activation_version == "v0.26.7"
    assert panels["snapshot_export"].activation_version == "v0.26.8"
    for panel in panels.values():
        assert panel.implementation_status == "future_track"
        assert panel.raw_data_dump_forbidden is True
        assert panel.raw_transcript_forbidden is True
        assert panel.raw_provider_output_forbidden is True
        assert panel.raw_secret_output_forbidden is True
        assert panel.provider_invocation_allowed is False
        assert panel.direct_execution_allowed is False
        assert panel.memory_promotion_allowed is False
        assert panel.external_adapter_allowed is False
        assert panel.ocel_visible is True


def test_permission_action_inspection_approval_command_snapshot_privacy_policies() -> None:
    parts = _parts()
    category = parts["panel_category_policy"]
    permission = parts["view_permission_policy"]
    action = parts["action_boundary_policy"]
    inspection = parts["read_only_inspection_policy"]
    approval = parts["approval_policy"]
    command = parts["command_boundary_policy"]
    snapshot = parts["snapshot_policy"]
    privacy = parts["trace_privacy_policy"]
    ocel = parts["ocel_visibility_contract"]

    assert category.raw_data_dump_panels_forbidden is True
    assert category.direct_execution_panels_forbidden is True
    assert category.memory_panels_deferred is True
    assert category.external_adapter_panels_deferred is True
    assert permission.deny_by_default is True
    assert permission.read_only_inspection_allowed is True
    assert permission.trace_view_allowed is True
    assert permission.provider_capability_view_allowed is True
    assert permission.evidence_view_allowed is True
    assert permission.safety_gate_view_allowed is True
    assert permission.raw_transcript_view_forbidden is True
    assert permission.raw_provider_output_view_forbidden is True
    assert permission.raw_secret_view_forbidden is True
    assert permission.credential_view_forbidden is True
    assert permission.private_path_sanitization_required is True
    assert action.direct_provider_invocation_forbidden is True
    assert action.direct_file_access_forbidden is True
    assert action.direct_subprocess_forbidden is True
    assert action.direct_local_command_execution_forbidden is True
    assert action.command_rerun_forbidden is True
    assert action.automatic_repair_forbidden is True
    assert action.autonomous_loop_forbidden is True
    assert action.background_execution_forbidden is True
    assert action.workbench_command_must_use_v025_surface is True
    assert action.provider_invocation_must_use_v0255 is True
    assert action.local_runtime_must_use_v0247_gate is True
    assert action.approval_is_not_execution is True
    assert inspection.inspection_allowed is True
    assert inspection.inspect_trace_refs is True
    assert inspection.inspect_pipeline_refs is True
    assert inspection.inspect_provider_refs is True
    assert inspection.inspect_evidence_refs is True
    assert inspection.inspect_safety_refs is True
    assert inspection.inspect_telemetry_refs is True
    assert inspection.mutate_inspected_artifacts is False
    assert inspection.raw_transcript_dump_forbidden is True
    assert inspection.raw_provider_output_dump_forbidden is True
    assert inspection.raw_secret_dump_forbidden is True
    assert approval.approval_candidate_allowed_future is True
    assert approval.manual_approval_allowed_future is True
    assert approval.approval_token_allowed_future is True
    assert approval.approval_is_execution is False
    assert approval.approval_immediate_execution_forbidden is True
    assert approval.auto_approval_forbidden is True
    assert approval.approval_requires_ocel_visibility is True
    assert approval.approval_requires_policy_ref is True
    assert approval.approval_requires_user_intent_ref is True
    assert approval.approval_requires_expiry_or_scope is True
    assert command.workbench_command_surface_deferred_to == "v0.26.7"
    assert command.command_candidates_allowed_future is True
    assert command.command_execution_allowed_only_through_existing_surface is True
    assert command.ask_command_must_use_v0257 is True
    assert command.provider_command_must_use_v0255 is True
    assert command.local_runtime_command_must_use_v0247 is True
    assert command.direct_command_execution_forbidden is True
    assert command.command_rerun_loop_forbidden is True
    assert command.automatic_repair_loop_forbidden is True
    assert snapshot.snapshot_deferred_to == "v0.26.8"
    assert snapshot.snapshot_is_memory_promotion is False
    assert snapshot.persistent_memory_write_forbidden is True
    assert snapshot.raw_transcript_export_forbidden is True
    assert snapshot.raw_provider_output_export_forbidden is True
    assert snapshot.raw_secret_export_forbidden is True
    assert snapshot.private_company_material_export_forbidden is True
    assert privacy.trace_view_allowed_future is True
    assert privacy.raw_transcript_storage_forbidden is True
    assert privacy.raw_provider_output_storage_forbidden is True
    assert privacy.raw_secret_storage_forbidden is True
    assert privacy.credential_storage_forbidden is True
    assert privacy.trace_refs_only_by_default is True
    assert ocel.workbench_interactions_ocel_visible is True
    assert ocel.panel_view_ocel_visible is True
    assert ocel.selection_ocel_visible_future is True
    assert ocel.filter_ocel_visible_future is True
    assert ocel.approval_decision_ocel_visible_future is True
    assert ocel.command_candidate_ocel_visible_future is True
    assert ocel.snapshot_ocel_visible_future is True
    assert ocel.no_raw_secret_in_ocel is True
    assert ocel.no_raw_provider_output_in_ocel is True
    assert ocel.no_raw_transcript_in_ocel is True


def test_roadmap_report_ocel_pig_ocpx_and_cli(capsys) -> None:
    service = WorkbenchContractReportService()
    parts = service.build_all_parts()
    roadmap = parts["roadmap_boundary"]
    report = parts["report"]
    pig = parts["pig_report"]
    ocpx = parts["ocpx_projection"]

    assert roadmap.current_track == "v0.26.x Workspace Agent Workbench"
    assert roadmap.current_version_scope == "v0.26.0 contract_only"
    assert roadmap.next_version == "v0.26.1 Workbench View State & Panel Model"
    assert roadmap.trace_explorer_deferred_to == "v0.26.2"
    assert roadmap.provider_browser_deferred_to == "v0.26.3"
    assert roadmap.evidence_inspector_deferred_to == "v0.26.4"
    assert roadmap.approval_console_deferred_to == "v0.26.5"
    assert roadmap.run_dashboard_deferred_to == "v0.26.6"
    assert roadmap.command_surface_deferred_to == "v0.26.7"
    assert roadmap.snapshot_export_deferred_to == "v0.26.8"
    assert roadmap.memory_continuity_deferred_to == "v0.27.x"
    assert roadmap.public_alpha_schumpeter_split_deferred_to == "v0.28.x"
    assert roadmap.external_provider_adapters_deferred_to == "v0.29.x+"
    assert roadmap.external_agent_dominion_deferred_to == "v0.30.x+"
    assert roadmap.growthkernel_bridge_deferred is True
    assert report.report_status == "passed"
    assert report.ready_for_v0_26_1 is True
    assert report.ready_for_v0_27 is False
    assert report.workbench_contract_created is True
    assert report.actual_ui_implemented is False
    assert report.trace_explorer_implemented is False
    assert report.provider_browser_implemented is False
    assert report.evidence_inspector_implemented is False
    assert report.approval_console_implemented is False
    assert report.run_dashboard_implemented is False
    assert report.command_surface_implemented is False
    assert report.snapshot_export_implemented is False
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
    assert report.next_required_step == "v0.26.1 Workbench View State & Panel Model"
    assert "workspace_agent_workbench_contract" in WORKBENCH_CONTRACT_OBJECT_TYPES
    assert "workbench_contract_requested" in WORKBENCH_CONTRACT_EVENT_TYPES
    assert "declares_workbench_contract" in WORKBENCH_CONTRACT_RELATION_TYPES
    assert "workbench_contract_declared" in WORKBENCH_CONTRACT_EFFECT_TYPES
    assert pig["version"] == "v0.26.0"
    assert pig["layer"] == "workspace_agent_workbench"
    assert pig["subject"] == "workspace_agent_workbench_contract"
    assert pig["safety_boundary"]["actual_ui_implemented"] is False
    assert pig["next_step"] == "v0.26.1 Workbench View State & Panel Model"
    assert ocpx["state"] == "workspace_agent_workbench_contract_declared"
    assert "WorkspaceAgentWorkbenchContractState" in ocpx["target_read_models"]
    assert "WorkbenchRoadmapBoundaryState" in ocpx["target_read_models"]

    commands = [
        ["workbench", "contract"],
        ["workbench", "modes"],
        ["workbench", "panels"],
        ["workbench", "permissions"],
        ["workbench", "action-boundary"],
        ["workbench", "approval-policy"],
        ["workbench", "snapshot-policy"],
        ["workbench", "roadmap-boundary"],
        ["workbench", "contract-report"],
    ]
    for argv in commands:
        assert main(argv) == 0
        output = capsys.readouterr().out
        assert "version=v0.26.0" in output
        assert "layer=workspace_agent_workbench" in output
        assert "status=contract_only" in output
        assert "ready_for_v0_26_1=true" in output
        assert "ready_for_v0_27=false" in output
        assert "actual_ui_implemented=false" in output
        assert "trace_explorer_implemented=false" in output
        assert "provider_browser_implemented=false" in output
        assert "approval_console_implemented=false" in output
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
        assert "schumpeter_split_introduced=false" in output
        assert "credential_exposed=false" in output
        assert "raw_secret_output=false" in output
        assert "raw_provider_output_inline=false" in output
        assert "raw_transcript_persisted=false" in output
        assert "llm_judge_used=false" in output
        assert "next_required_step=v0.26.1 Workbench View State & Panel Model" in output
