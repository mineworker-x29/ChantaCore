from __future__ import annotations

import inspect

import pytest

from chanta_core.internal_triad import workbench
from chanta_core.internal_triad.workbench import (
    TriadWorkbenchActionKind,
    TriadWorkbenchActionSpec,
    TriadWorkbenchArtifactCard,
    TriadWorkbenchArtifactRef,
    TriadWorkbenchCardKind,
    TriadWorkbenchDataSourceKind,
    TriadWorkbenchDisplayFilter,
    TriadWorkbenchGapRiskEvidenceView,
    TriadWorkbenchPanelKind,
    TriadWorkbenchPanelSpec,
    TriadWorkbenchReadinessView,
    TriadWorkbenchReport,
    TriadWorkbenchRunPreview,
    TriadWorkbenchSeverity,
    TriadWorkbenchSnapshot,
    TriadWorkbenchStatus,
    TriadWorkbenchSurface,
    TriadWorkbenchSurfaceKind,
    TriadWorkbenchTracePreview,
    V0318ReadinessReport,
    build_triad_workbench_action_spec,
    build_triad_workbench_artifact_card,
    build_triad_workbench_artifact_ref,
    build_triad_workbench_display_filter,
    build_triad_workbench_gap_risk_evidence_view,
    build_triad_workbench_panel_spec,
    build_triad_workbench_readiness_view,
    build_triad_workbench_report,
    build_triad_workbench_run_preview,
    build_triad_workbench_snapshot,
    build_triad_workbench_surface,
    build_triad_workbench_trace_preview,
    build_v0318_readiness_report,
    workbench_action_spec_preserves_no_execution,
    workbench_readiness_report_is_not_runtime_ready,
    workbench_report_is_not_runtime_ready,
    workbench_snapshot_preserves_no_runtime,
    workbench_surface_is_not_ui_runtime,
)


def test_v0318_taxonomies_are_complete_and_display_only() -> None:
    assert {kind.value for kind in TriadWorkbenchSurfaceKind} == {
        "triad_overview",
        "observation_surface",
        "capability_map_surface",
        "digestion_surface",
        "internalization_surface",
        "dominion_surface",
        "ocel_trace_surface",
        "gap_risk_evidence_surface",
        "readiness_surface",
        "future_gate_surface",
        "no_op_surface",
        "unknown",
    }
    assert {kind.value for kind in TriadWorkbenchPanelKind} == {
        "overview_panel",
        "observation_report_panel",
        "capability_map_panel",
        "digestion_signal_panel",
        "internal_candidate_panel",
        "internalization_plan_panel",
        "dominion_target_panel",
        "dominion_decision_panel",
        "ocel_trace_plan_panel",
        "ocel_trace_coverage_panel",
        "gap_register_panel",
        "risk_map_panel",
        "evidence_table_panel",
        "future_gate_panel",
        "no_op_panel",
        "readiness_panel",
        "unknown",
    }
    assert {kind.value for kind in TriadWorkbenchCardKind} == {
        "artifact_card",
        "report_card",
        "candidate_card",
        "decision_card",
        "trace_card",
        "risk_card",
        "gap_card",
        "evidence_card",
        "future_gate_card",
        "no_op_card",
        "readiness_card",
        "unknown",
    }
    assert {kind.value for kind in TriadWorkbenchActionKind} == {
        "view_only",
        "inspect_artifact",
        "inspect_trace_plan",
        "inspect_gap",
        "inspect_risk",
        "inspect_evidence",
        "inspect_readiness",
        "export_preview",
        "approval_preview",
        "no_op_preview",
        "future_track_preview",
        "unknown",
    }
    assert {kind.value for kind in TriadWorkbenchDataSourceKind} == {
        "triad_contract",
        "observation_report",
        "capability_map",
        "digestion_output",
        "internal_candidate_set",
        "internalization_plan",
        "dominion_target_decision_set",
        "ocel_trace_plan",
        "ocel_trace_coverage",
        "readiness_report",
        "gap_register",
        "risk_map",
        "evidence_table",
        "manual_ref",
        "unknown",
    }
    assert {status.value for status in TriadWorkbenchStatus} == {
        "unknown",
        "draft",
        "surface_ready",
        "surface_ready_with_gaps",
        "blocked",
        "deferred",
        "future_track",
        "no_op",
    }
    assert {severity.value for severity in TriadWorkbenchSeverity} == {"info", "low", "medium", "high", "critical", "blocked"}
    assert workbench.triad_workbench_surface_kind_creates_ui_runtime(TriadWorkbenchSurfaceKind.TRIAD_OVERVIEW) is False
    assert workbench.triad_workbench_action_kind_executes(TriadWorkbenchActionKind.APPROVAL_PREVIEW) is False


def _artifact_ref() -> TriadWorkbenchArtifactRef:
    return build_triad_workbench_artifact_ref(
        "triad_workbench_artifact_ref:1",
        TriadWorkbenchDataSourceKind.OCEL_TRACE_PLAN,
        "triad_ocel_trace_plan:1",
        source_version="v0.31.7",
        evidence_refs=["evidence:1"],
    )


def test_workbench_refs_filters_actions_panels_cards_are_non_executable() -> None:
    artifact_ref = _artifact_ref()
    display_filter = build_triad_workbench_display_filter(
        "triad_workbench_filter:1",
        "Trace filters",
        target_surface_kinds=[TriadWorkbenchSurfaceKind.OCEL_TRACE_SURFACE],
        target_panel_kinds=[TriadWorkbenchPanelKind.OCEL_TRACE_PLAN_PANEL],
        target_card_kinds=[TriadWorkbenchCardKind.TRACE_CARD],
        include_statuses=[TriadWorkbenchStatus.SURFACE_READY],
        include_severities=[TriadWorkbenchSeverity.INFO],
        include_artifact_kinds=[TriadWorkbenchDataSourceKind.OCEL_TRACE_PLAN],
    )
    action = build_triad_workbench_action_spec(
        "triad_workbench_action_spec:1",
        TriadWorkbenchActionKind.INSPECT_TRACE_PLAN,
        "Inspect trace plan",
        "Display-only trace plan inspection.",
        target_artifact_refs=[artifact_ref],
    )
    panel = build_triad_workbench_panel_spec(
        "triad_workbench_panel:1",
        TriadWorkbenchPanelKind.OCEL_TRACE_PLAN_PANEL,
        "Trace plan",
        "Display-only trace plan panel.",
        artifact_refs=[artifact_ref],
        action_specs=[action],
        filters=[display_filter],
    )
    card = build_triad_workbench_artifact_card(
        "triad_workbench_card:1",
        TriadWorkbenchCardKind.TRACE_CARD,
        "Trace plan card",
        "Display-only trace card.",
        artifact_ref,
        tags=["trace"],
        evidence_refs=["evidence:1"],
        action_specs=[action],
    )

    assert artifact_ref.fetches_data is False
    assert artifact_ref.active_object is False
    assert isinstance(display_filter, TriadWorkbenchDisplayFilter)
    assert display_filter.executes_query is False
    assert isinstance(action, TriadWorkbenchActionSpec)
    assert action.execution_enabled is False
    assert action.approval_enabled is False
    assert action.mutation_enabled is False
    assert action.export_enabled is False
    assert action.executes_action is False
    assert workbench_action_spec_preserves_no_execution(action) is True
    assert isinstance(panel, TriadWorkbenchPanelSpec)
    assert panel.rendered_ui is False
    assert isinstance(card, TriadWorkbenchArtifactCard)
    assert card.active_artifact is False


def test_surface_snapshot_report_preview_and_readiness_are_not_runtime() -> None:
    artifact_ref = _artifact_ref()
    action = build_triad_workbench_action_spec("action:1", TriadWorkbenchActionKind.VIEW_ONLY, "View", "Display only.")
    panel = build_triad_workbench_panel_spec("panel:1", TriadWorkbenchPanelKind.READINESS_PANEL, "Readiness", "Display only.")
    card = build_triad_workbench_artifact_card("card:1", TriadWorkbenchCardKind.READINESS_CARD, "Readiness", "Display only.", artifact_ref)
    trace_preview = build_triad_workbench_trace_preview(
        "trace_preview:1",
        source_trace_plan_id="triad_ocel_trace_plan:1",
        planned_event_type_names=["triad_skill_completed"],
        coverage_summary="Trace preview is not emission.",
    )
    gre_view = build_triad_workbench_gap_risk_evidence_view(
        "gap_risk_evidence_view:1",
        evidence_artifact_refs=[artifact_ref],
        highest_severity=TriadWorkbenchSeverity.LOW,
        recommended_followups=["review v0.31.9 consolidation"],
    )
    readiness_view = build_triad_workbench_readiness_view("readiness_view:1", readiness_report_refs=[artifact_ref])
    surface = build_triad_workbench_surface(
        "surface:1",
        TriadWorkbenchSurfaceKind.TRIAD_OVERVIEW,
        "Triad overview",
        "Display-only overview.",
        panels=[panel],
        cards=[card],
        trace_preview=trace_preview,
        gap_risk_evidence_view=gre_view,
        readiness_view=readiness_view,
    )
    snapshot = build_triad_workbench_snapshot("snapshot:1", surfaces=[surface], artifact_refs=[artifact_ref], action_specs=[action])
    report = build_triad_workbench_report("report:1", snapshot)
    run_preview = build_triad_workbench_run_preview("run_preview:1")
    readiness = build_v0318_readiness_report(report)

    assert isinstance(trace_preview, TriadWorkbenchTracePreview)
    assert trace_preview.ready_for_ocel_emission is False
    assert trace_preview.ready_for_runtime_trace_persistence is False
    assert trace_preview.emits_ocel_events is False
    assert isinstance(gre_view, TriadWorkbenchGapRiskEvidenceView)
    assert gre_view.remediation_enabled is False
    assert gre_view.remediates is False
    assert isinstance(readiness_view, TriadWorkbenchReadinessView)
    assert readiness_view.ready_for_execution is False
    assert readiness_view.ready_for_skill_activation is False
    assert readiness_view.ready_for_ui_runtime is False
    assert readiness_view.ready_for_action_execution is False
    assert readiness_view.runtime_readiness is False
    assert isinstance(surface, TriadWorkbenchSurface)
    assert workbench_surface_is_not_ui_runtime(surface) is True
    assert isinstance(snapshot, TriadWorkbenchSnapshot)
    assert snapshot.ready_for_ui_runtime is False
    assert snapshot.ready_for_execution is False
    assert snapshot.persists_runtime_state is False
    assert workbench_snapshot_preserves_no_runtime(snapshot) is True
    assert isinstance(report, TriadWorkbenchReport)
    assert report.ready_for_ui_runtime is False
    assert report.ready_for_action_execution is False
    assert report.ready_for_execution is False
    assert workbench_report_is_not_runtime_ready(report) is True
    assert isinstance(run_preview, TriadWorkbenchRunPreview)
    assert run_preview.no_ui_runtime_guarantee is True
    assert run_preview.no_action_execution_guarantee is True
    assert run_preview.no_approval_execution_guarantee is True
    assert run_preview.no_ocel_emission_guarantee is True
    assert run_preview.no_runtime_persistence_guarantee is True
    assert run_preview.no_registry_mutation_guarantee is True
    assert run_preview.no_memory_mutation_guarantee is True
    assert run_preview.executes_run is False
    assert isinstance(readiness, V0318ReadinessReport)
    assert readiness.ready_for_ui_runtime is False
    assert readiness.ready_for_action_execution is False
    assert readiness.ready_for_approval_execution is False
    assert readiness.ready_for_ocel_emission is False
    assert readiness.ready_for_runtime_trace_persistence is False
    assert readiness.ready_for_execution is False
    assert workbench_readiness_report_is_not_runtime_ready(readiness) is True


def test_v0318_negative_runtime_flags_are_rejected() -> None:
    with pytest.raises(ValueError, match="execution_enabled"):
        TriadWorkbenchActionSpec("action:bad", TriadWorkbenchActionKind.VIEW_ONLY, "View", "description", execution_enabled=True)
    with pytest.raises(ValueError, match="approval_enabled"):
        TriadWorkbenchActionSpec("action:bad", TriadWorkbenchActionKind.APPROVAL_PREVIEW, "Approve", "description", approval_enabled=True)
    with pytest.raises(ValueError, match="mutation_enabled"):
        TriadWorkbenchActionSpec("action:bad", TriadWorkbenchActionKind.INSPECT_ARTIFACT, "Inspect", "description", mutation_enabled=True)
    with pytest.raises(ValueError, match="export_enabled"):
        TriadWorkbenchActionSpec("action:bad", TriadWorkbenchActionKind.EXPORT_PREVIEW, "Export", "description", export_enabled=True)
    with pytest.raises(ValueError, match="ready_for_ui_runtime"):
        TriadWorkbenchSurface("surface:bad", TriadWorkbenchSurfaceKind.TRIAD_OVERVIEW, "title", "description", ready_for_ui_runtime=True)
    with pytest.raises(ValueError, match="persistence"):
        build_triad_workbench_snapshot("snapshot:bad", metadata={"persistence": True})
    with pytest.raises(ValueError, match="ready_for_ocel_emission"):
        TriadWorkbenchTracePreview("trace_preview:bad", ready_for_ocel_emission=True)
    with pytest.raises(ValueError, match="ready_for_execution"):
        TriadWorkbenchReadinessView("readiness:bad", ready_for_execution=True)
    with pytest.raises(ValueError, match="ready_for_action_execution"):
        TriadWorkbenchReport("report:bad", "snapshot:bad", "v0.31.8", "summary", 0, 0, 0, 0, ready_for_action_execution=True)


def test_v0318_helpers_are_pure_conservative() -> None:
    helpers = [
        build_triad_workbench_artifact_ref,
        build_triad_workbench_display_filter,
        build_triad_workbench_action_spec,
        build_triad_workbench_panel_spec,
        build_triad_workbench_artifact_card,
        build_triad_workbench_trace_preview,
        build_triad_workbench_gap_risk_evidence_view,
        build_triad_workbench_readiness_view,
        build_triad_workbench_surface,
        build_triad_workbench_snapshot,
        build_triad_workbench_report,
        build_triad_workbench_run_preview,
        build_v0318_readiness_report,
        workbench_action_spec_preserves_no_execution,
        workbench_surface_is_not_ui_runtime,
        workbench_snapshot_preserves_no_runtime,
        workbench_report_is_not_runtime_ready,
        workbench_readiness_report_is_not_runtime_ready,
    ]
    for helper in helpers:
        source = inspect.getsource(helper)
        assert "ready_for_execution=True" not in source
        assert "ready_for_ui_runtime=True" not in source
        assert "ready_for_action_execution=True" not in source
        assert "ready_for_approval_execution=True" not in source
        assert "ready_for_ocel_emission=True" not in source
        assert "execution_enabled=True" not in source
        assert "approval_enabled=True" not in source
        assert "subprocess" not in source
        assert "os.system" not in source
        assert "shell=True" not in source
        assert "requests." not in source
        assert "httpx." not in source
        assert "socket." not in source
