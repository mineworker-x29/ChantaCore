from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.workspace_agent_workbench import (
    WORKBENCH_VIEW_STATE_EFFECT_TYPES,
    WORKBENCH_VIEW_STATE_EVENT_TYPES,
    WORKBENCH_VIEW_STATE_FORBIDDEN_EFFECT_TYPES,
    WORKBENCH_VIEW_STATE_FUTURE_SKILL_IDS,
    WORKBENCH_VIEW_STATE_IMPLEMENTED_SKILL_IDS,
    WORKBENCH_VIEW_STATE_OBJECT_TYPES,
    WORKBENCH_VIEW_STATE_RELATION_TYPES,
    WORKBENCH_VIEW_STATE_VERSION,
    WorkbenchFilterPolicy,
    WorkbenchFilterState,
    WorkbenchFocusPolicy,
    WorkbenchFocusState,
    WorkbenchNavigationPolicy,
    WorkbenchNavigationState,
    WorkbenchPanel,
    WorkbenchPanelLayout,
    WorkbenchPanelModelPolicy,
    WorkbenchPanelRegistryView,
    WorkbenchPanelSlot,
    WorkbenchSelectionPolicy,
    WorkbenchSelectionState,
    WorkbenchSessionView,
    WorkbenchSessionViewPolicy,
    WorkbenchViewState,
    WorkbenchViewStateFinding,
    WorkbenchViewStatePolicy,
    WorkbenchViewStatePrerequisiteSourceService,
    WorkbenchViewStateReport,
    WorkbenchViewStateReportService,
    WorkbenchViewStateRequest,
)


def _parts() -> dict:
    return WorkbenchViewStateReportService().build_all_parts()


def test_workbench_view_state_models_build() -> None:
    parts = _parts()

    assert isinstance(parts["view_state_policy"], WorkbenchViewStatePolicy)
    assert isinstance(parts["request"], WorkbenchViewStateRequest)
    assert isinstance(parts["panel_model_policy"], WorkbenchPanelModelPolicy)
    assert isinstance(parts["panels"][0], WorkbenchPanel)
    assert isinstance(parts["layout"].slots[0], WorkbenchPanelSlot)
    assert isinstance(parts["layout"], WorkbenchPanelLayout)
    assert isinstance(parts["panel_registry_view"], WorkbenchPanelRegistryView)
    assert isinstance(parts["selection_policy"], WorkbenchSelectionPolicy)
    assert isinstance(parts["selection_state"], WorkbenchSelectionState)
    assert isinstance(parts["filter_policy"], WorkbenchFilterPolicy)
    assert isinstance(parts["filter_state"], WorkbenchFilterState)
    assert isinstance(parts["focus_policy"], WorkbenchFocusPolicy)
    assert isinstance(parts["focus_state"], WorkbenchFocusState)
    assert isinstance(parts["navigation_policy"], WorkbenchNavigationPolicy)
    assert isinstance(parts["navigation_state"], WorkbenchNavigationState)
    assert isinstance(parts["session_view_policy"], WorkbenchSessionViewPolicy)
    assert isinstance(parts["session_view"], WorkbenchSessionView)
    assert isinstance(parts["view_state"], WorkbenchViewState)
    assert isinstance(parts["findings"][0], WorkbenchViewStateFinding)
    assert isinstance(parts["report"], WorkbenchViewStateReport)


def test_sources_skills_and_policies_are_view_state_only() -> None:
    parts = _parts()
    sources = WorkbenchViewStatePrerequisiteSourceService().load_sources()
    policy = parts["view_state_policy"]
    panel_policy = parts["panel_model_policy"]

    assert WORKBENCH_VIEW_STATE_VERSION == "v0.26.1"
    assert WORKBENCH_VIEW_STATE_IMPLEMENTED_SKILL_IDS == [
        "skill:workbench_view_state_create",
        "skill:workbench_panel_model_view",
    ]
    assert "skill:workbench_trace_explorer_view" in WORKBENCH_VIEW_STATE_FUTURE_SKILL_IDS
    assert "skill:workbench_provider_browser_view" in WORKBENCH_VIEW_STATE_FUTURE_SKILL_IDS
    assert "skill:workbench_snapshot_create" in WORKBENCH_VIEW_STATE_FUTURE_SKILL_IDS
    assert sources["workbench_contract"]["available"] is True
    assert len(sources["panel_contracts"]) == 12
    assert all(source.get("read_only", True) is True for key, source in sources.items() if isinstance(source, dict))
    assert policy.view_state_enabled is True
    assert policy.panel_model_enabled is True
    assert policy.actual_ui_rendering_enabled is False
    assert policy.browser_server_enabled is False
    assert policy.dashboard_rendering_enabled is False
    assert policy.panel_behavior_enabled is False
    assert policy.ask_execution_enabled is False
    assert policy.provider_invocation_enabled is False
    assert policy.local_runtime_execution_enabled is False
    assert policy.response_emission_enabled is False
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
    assert set(panel_policy.required_panel_types) == {
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
    assert panel_policy.panel_contract_required is True
    assert panel_policy.panel_behavior_deferred is True
    assert panel_policy.panel_rendering_deferred is True
    assert panel_policy.panel_source_refs_required is True
    assert panel_policy.raw_data_dump_forbidden is True
    assert panel_policy.provider_invocation_forbidden is True
    assert panel_policy.direct_execution_forbidden is True
    assert panel_policy.memory_promotion_forbidden is True
    assert panel_policy.external_adapter_forbidden is True


def test_required_panel_models_layout_and_registry_are_ready() -> None:
    parts = _parts()
    panels = {panel.panel_type: panel for panel in parts["panels"]}
    layout = parts["layout"]
    registry = parts["panel_registry_view"]

    assert set(panels) == set(parts["panel_model_policy"].required_panel_types)
    for panel in panels.values():
        assert panel.contract_ref is not None
        assert panel.implementation_status in {"model_only", "future_behavior", "disabled", "blocked"}
        assert panel.implementation_status == "model_only"
        assert panel.activation_version.startswith("v0.26.")
        assert panel.renders_ui_now is False
        assert panel.implements_behavior_now is False
        assert panel.provider_invocation_allowed_now is False
        assert panel.direct_execution_allowed_now is False
        assert panel.memory_promotion_allowed_now is False
        assert panel.external_adapter_allowed_now is False
        assert panel.raw_transcript_included is False
        assert panel.raw_provider_output_included is False
        assert panel.raw_secret_included is False
    assert panels["trace_explorer"].activation_version == "v0.26.2"
    assert panels["pipeline_timeline"].activation_version == "v0.26.2"
    assert panels["provider_browser"].activation_version == "v0.26.3"
    assert panels["evidence_inspector"].activation_version == "v0.26.4"
    assert panels["approval_console"].activation_version == "v0.26.5"
    assert panels["run_dashboard"].activation_version == "v0.26.6"
    assert panels["command_surface"].activation_version == "v0.26.7"
    assert panels["snapshot_export"].activation_version == "v0.26.8"
    assert len(layout.slots) == len(panels)
    assert all(slot.region in {"left", "right", "center", "bottom", "top", "overlay", "hidden", "unknown"} for slot in layout.slots)
    assert all(isinstance(slot.order_index, int) for slot in layout.slots)
    assert "workbench_panel:trace_explorer" in layout.active_panel_ids
    assert "workbench_panel:pipeline_timeline" in layout.active_panel_ids
    assert "workbench_panel:snapshot_export" in layout.hidden_panel_ids
    assert layout.layout_status == "ready"
    assert layout.renders_ui_now is False
    assert registry.panel_count == 12
    assert registry.model_only_count == 12
    assert registry.future_behavior_count == 0
    assert registry.disabled_count == 0
    assert registry.blocked_count == 0
    assert registry.registry_status == "ready"


def test_selection_filter_focus_navigation_and_session_view_are_non_executing() -> None:
    parts = _parts()
    selection_policy = parts["selection_policy"]
    selection = parts["selection_state"]
    filter_policy = parts["filter_policy"]
    filters = parts["filter_state"]
    focus_policy = parts["focus_policy"]
    focus = parts["focus_state"]
    navigation_policy = parts["navigation_policy"]
    navigation = parts["navigation_state"]
    session_policy = parts["session_view_policy"]
    session = parts["session_view"]

    assert selection_policy.selection_is_not_approval is True
    assert selection_policy.selection_is_not_execution is True
    assert selection_policy.selection_refs_only is True
    assert selection_policy.selected_raw_content_forbidden is True
    assert selection_policy.selected_secret_forbidden is True
    assert selection.selection_count == 1
    assert selection.selection_status == "ready"
    assert selection.approval_created is False
    assert selection.execution_triggered is False
    assert selection.raw_content_included is False
    assert selection.raw_secret_included is False
    assert filter_policy.filter_is_not_data_deletion is True
    assert filter_policy.filter_is_not_access_control is True
    assert filter_policy.hidden_data_not_deleted is True
    assert filters.filter_count == 1
    assert filters.data_deleted is False
    assert filters.access_policy_mutated is False
    assert focus_policy.focus_is_not_provider_invocation is True
    assert focus_policy.focus_is_not_execution is True
    assert focus_policy.focus_refs_only is True
    assert focus.focused_panel_id == "workbench_panel:trace_explorer"
    assert focus.provider_invoked is False
    assert focus.execution_triggered is False
    assert navigation_policy.navigation_is_not_background_routing is True
    assert navigation_policy.navigation_is_not_pipeline_execution is True
    assert navigation_policy.navigation_history_enabled is True
    assert navigation.pipeline_executed is False
    assert navigation.background_routing_started is False
    assert session_policy.session_view_is_not_memory_continuity is True
    assert session_policy.persistent_memory_write_forbidden is True
    assert session_policy.memory_promotion_forbidden is True
    assert session_policy.refs_only_by_default is True
    assert session_policy.raw_transcript_inline_forbidden is True
    assert session.visible_session_count == 1
    assert session.active_session_ref is not None
    assert session.memory_continuity_enabled is False
    assert session.persistent_memory_written is False
    assert session.raw_transcript_included is False


def test_view_state_report_ocel_pig_ocpx_and_cli(capsys) -> None:
    parts = _parts()
    view_state = parts["view_state"]
    report = parts["report"]
    pig = parts["pig_report"]
    ocpx = parts["ocpx_projection"]

    assert view_state.state_status == "ready"
    assert view_state.actual_ui_rendered is False
    assert view_state.panel_behavior_implemented is False
    assert view_state.ask_executed is False
    assert view_state.provider_invoked is False
    assert view_state.local_command_executed is False
    assert view_state.final_response_emitted is False
    assert view_state.memory_promoted is False
    assert view_state.persistent_memory_written is False
    assert view_state.persona_mutated is False
    assert view_state.external_adapter_implemented is False
    assert view_state.raw_transcript_included is False
    assert view_state.raw_provider_output_included is False
    assert view_state.raw_secret_included is False
    assert report.report_status == "passed"
    assert report.ready_for_v0_26_2 is True
    assert report.ready_for_v0_27 is False
    assert report.view_state_created is True
    assert report.panel_model_created is True
    assert report.panel_layout_created is True
    assert report.selection_state_created is True
    assert report.filter_state_created is True
    assert report.focus_state_created is True
    assert report.navigation_state_created is True
    assert report.session_view_created is True
    assert report.actual_ui_rendered is False
    assert report.panel_behavior_implemented is False
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
    assert report.next_required_step == "v0.26.2 Trace Explorer & Pipeline Timeline"
    assert "workbench_view_state_policy" in WORKBENCH_VIEW_STATE_OBJECT_TYPES
    assert "workbench_view_state_requested" in WORKBENCH_VIEW_STATE_EVENT_TYPES
    assert "creates_workbench_view_state" in WORKBENCH_VIEW_STATE_RELATION_TYPES
    assert "workbench_view_state_created" in WORKBENCH_VIEW_STATE_EFFECT_TYPES
    assert not set(WORKBENCH_VIEW_STATE_EFFECT_TYPES).intersection(WORKBENCH_VIEW_STATE_FORBIDDEN_EFFECT_TYPES)
    assert pig["version"] == "v0.26.1"
    assert pig["layer"] == "workspace_agent_workbench"
    assert pig["subject"] == "workbench_view_state_panel_model"
    assert pig["safety_boundary"]["actual_ui_rendered"] is False
    assert pig["safety_boundary"]["panel_behavior_implemented"] is False
    assert pig["next_step"] == "v0.26.2 Trace Explorer & Pipeline Timeline"
    assert ocpx["state"] == "workbench_view_state_panel_model_created"
    assert "WorkbenchViewStateState" in ocpx["target_read_models"]
    assert "WorkbenchSessionViewState" in ocpx["target_read_models"]

    commands = [
        ["workbench", "view-state"],
        ["workbench", "panels", "model"],
        ["workbench", "layout"],
        ["workbench", "selection"],
        ["workbench", "filters"],
        ["workbench", "focus"],
        ["workbench", "navigation"],
        ["workbench", "session-view"],
        ["workbench", "view-state-report"],
    ]
    for argv in commands:
        assert main(argv) == 0
        output = capsys.readouterr().out
        assert "version=v0.26.1" in output
        assert "layer=workspace_agent_workbench" in output
        assert "view_state_created=true" in output
        assert "panel_model_created=true" in output
        assert "panel_layout_created=true" in output
        assert "selection_state_created=true" in output
        assert "filter_state_created=true" in output
        assert "focus_state_created=true" in output
        assert "navigation_state_created=true" in output
        assert "session_view_created=true" in output
        assert "ready_for_v0_26_2=true" in output
        assert "ready_for_v0_27=false" in output
        assert "actual_ui_rendered=false" in output
        assert "panel_behavior_implemented=false" in output
        assert "trace_explorer_implemented=false" in output
        assert "provider_browser_implemented=false" in output
        assert "evidence_inspector_implemented=false" in output
        assert "approval_console_implemented=false" in output
        assert "run_dashboard_implemented=false" in output
        assert "command_surface_implemented=false" in output
        assert "snapshot_export_implemented=false" in output
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
        assert "raw_secret_output=false" in output
        assert "raw_provider_output_inline=false" in output
        assert "raw_transcript_persisted=false" in output
        assert "llm_judge_used=false" in output
        assert "next_required_step=v0.26.2 Trace Explorer & Pipeline Timeline" in output
