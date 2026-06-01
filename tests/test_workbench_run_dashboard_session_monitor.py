from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.workspace_agent_workbench import (
    WORKBENCH_RUN_DASHBOARD_EFFECT_TYPES,
    WORKBENCH_RUN_DASHBOARD_EVENT_TYPES,
    WORKBENCH_RUN_DASHBOARD_FORBIDDEN_EFFECT_TYPES,
    WORKBENCH_RUN_DASHBOARD_FUTURE_SKILL_IDS,
    WORKBENCH_RUN_DASHBOARD_IMPLEMENTED_SKILL_IDS,
    WORKBENCH_RUN_DASHBOARD_OBJECT_TYPES,
    WORKBENCH_RUN_DASHBOARD_RELATION_TYPES,
    WORKBENCH_RUN_DASHBOARD_VERSION,
    WorkbenchApprovalStatusSummary,
    WorkbenchFailureSummary,
    WorkbenchPipelineStatusView,
    WorkbenchProviderStatusSummary,
    WorkbenchResponseStatusSummary,
    WorkbenchRunCard,
    WorkbenchRunDashboardFinding,
    WorkbenchRunDashboardMetricSet,
    WorkbenchRunDashboardPolicy,
    WorkbenchRunDashboardReport,
    WorkbenchRunDashboardReportService,
    WorkbenchRunDashboardRequest,
    WorkbenchRunDashboardSourceView,
    WorkbenchRunDashboardView,
    WorkbenchSafetyStatusSummary,
    WorkbenchSessionCard,
    WorkbenchSessionContextRefView,
    WorkbenchSessionDecisionPatternView,
    WorkbenchSessionFailurePatternView,
    WorkbenchSessionMonitorPolicy,
    WorkbenchSessionMonitorView,
    WorkbenchSessionPIGGuidanceSummary,
    WorkbenchSessionProviderPatternView,
    WorkbenchSessionRoutePatternView,
    WorkbenchSessionSafetyPatternView,
    WorkbenchSessionTraceSummary,
    WorkbenchStageStatusSummary,
    WorkbenchWarningSummary,
)


def _parts() -> dict:
    return WorkbenchRunDashboardReportService().build_all_parts()


def test_run_dashboard_session_monitor_models_build() -> None:
    parts = _parts()

    assert isinstance(parts["policy"], WorkbenchRunDashboardPolicy)
    assert isinstance(parts["request"], WorkbenchRunDashboardRequest)
    assert isinstance(parts["source_view"], WorkbenchRunDashboardSourceView)
    assert isinstance(parts["run_dashboard_view"], WorkbenchRunDashboardView)
    assert isinstance(parts["run_cards"][0], WorkbenchRunCard)
    assert isinstance(parts["pipeline_status_views"][0], WorkbenchPipelineStatusView)
    assert isinstance(parts["stage_status_summary"], WorkbenchStageStatusSummary)
    assert isinstance(parts["provider_status_summary"], WorkbenchProviderStatusSummary)
    assert isinstance(parts["response_status_summary"], WorkbenchResponseStatusSummary)
    assert isinstance(parts["safety_status_summary"], WorkbenchSafetyStatusSummary)
    assert isinstance(parts["approval_status_summary"], WorkbenchApprovalStatusSummary)
    assert isinstance(parts["failure_summary"], WorkbenchFailureSummary)
    assert isinstance(parts["warning_summary"], WorkbenchWarningSummary)
    assert isinstance(parts["session_monitor_policy"], WorkbenchSessionMonitorPolicy)
    assert isinstance(parts["session_monitor_view"], WorkbenchSessionMonitorView)
    assert isinstance(parts["session_cards"][0], WorkbenchSessionCard)
    assert isinstance(parts["session_trace_summaries"][0], WorkbenchSessionTraceSummary)
    assert isinstance(parts["pig_guidance_summaries"][0], WorkbenchSessionPIGGuidanceSummary)
    assert isinstance(parts["decision_pattern_views"][0], WorkbenchSessionDecisionPatternView)
    assert isinstance(parts["route_pattern_views"][0], WorkbenchSessionRoutePatternView)
    assert isinstance(parts["provider_pattern_views"][0], WorkbenchSessionProviderPatternView)
    assert isinstance(parts["safety_pattern_views"][0], WorkbenchSessionSafetyPatternView)
    assert isinstance(parts["failure_pattern_views"][0], WorkbenchSessionFailurePatternView)
    assert isinstance(parts["context_ref_views"][0], WorkbenchSessionContextRefView)
    assert isinstance(parts["metric_set"], WorkbenchRunDashboardMetricSet)
    assert isinstance(parts["findings"][0], WorkbenchRunDashboardFinding)
    assert isinstance(parts["report"], WorkbenchRunDashboardReport)


def test_policy_skills_sources_and_refs_only_boundaries() -> None:
    parts = _parts()
    policy = parts["policy"]
    source = parts["source_view"]

    assert WORKBENCH_RUN_DASHBOARD_VERSION == "v0.26.6"
    assert WORKBENCH_RUN_DASHBOARD_IMPLEMENTED_SKILL_IDS == [
        "skill:workbench_run_dashboard_view",
        "skill:workbench_session_monitor_view",
    ]
    assert "skill:workbench_command_surface_use" in WORKBENCH_RUN_DASHBOARD_FUTURE_SKILL_IDS
    assert "skill:memory_candidate_create" not in WORKBENCH_RUN_DASHBOARD_FUTURE_SKILL_IDS
    assert policy.run_dashboard_enabled is True
    assert policy.session_monitor_enabled is True
    assert policy.run_status_summary_enabled is True
    assert policy.session_summary_enabled is True
    assert policy.pig_guidance_summary_enabled is True
    assert policy.repeated_pattern_view_enabled is True
    assert policy.failure_pattern_view_enabled is True
    assert policy.actual_ui_rendering_enabled is False
    assert policy.background_monitor_enabled is False
    assert policy.continuous_watcher_enabled is False
    assert policy.auto_refresh_execution_enabled is False
    assert policy.rerun_enabled is False
    assert policy.automatic_retry_enabled is False
    assert policy.automatic_repair_enabled is False
    assert policy.autonomous_optimization_enabled is False
    assert policy.command_execution_enabled is False
    assert policy.approval_execution_enabled is False
    assert policy.provider_invocation_enabled is False
    assert policy.ask_execution_enabled is False
    assert policy.response_emission_enabled is False
    assert policy.local_runtime_execution_enabled is False
    assert policy.memory_continuity_enabled is False
    assert policy.memory_promotion_enabled is False
    assert policy.persistent_memory_write_enabled is False
    assert policy.persona_mutation_enabled is False
    assert policy.external_adapter_enabled is False
    assert policy.refs_only_by_default is True
    assert policy.raw_provider_output_inline_forbidden is True
    assert policy.raw_transcript_inline_forbidden is True
    assert policy.raw_secret_inline_forbidden is True
    assert policy.pig_guidance_is_not_memory is True
    assert policy.pig_guidance_is_not_policy_mutation is True
    assert policy.pig_guidance_is_not_execution is True
    assert source.ask_repl_report_refs
    assert source.pipeline_run_refs
    assert source.trace_report_refs
    assert source.approval_report_refs
    assert source.evidence_report_refs
    assert source.provider_report_refs
    assert source.pig_guidance_refs
    assert source.raw_provider_output_included is False
    assert source.raw_transcript_included is False
    assert source.raw_secret_included is False
    assert source.private_full_path_included is False
    assert source.run_count >= 1
    assert source.session_count >= 1


def test_dashboard_cards_pipeline_status_and_summaries_are_non_executing() -> None:
    parts = _parts()
    card = parts["run_cards"][0]
    pipeline = parts["pipeline_status_views"][0]
    provider = parts["provider_status_summary"]
    response = parts["response_status_summary"]
    safety = parts["safety_status_summary"]
    approval = parts["approval_status_summary"]
    failure = parts["failure_summary"]

    assert card.status in {"completed", "warning", "failed", "blocked", "partial", "missing", "unknown"}
    assert card.rerun_enabled is False
    assert card.command_enabled is False
    assert card.provider_invocation_enabled is False
    assert card.raw_transcript_included is False
    assert pipeline.rerun_enabled is False
    assert provider.direct_provider_invocation_count == 0
    assert provider.provider_invocation_enabled_now is False
    assert response.response_rewrite_performed is False
    assert safety.safety_policy_mutation_count == 0
    assert approval.approval_executed_count == 0
    assert approval.auto_approval_count == 0
    assert failure.automatic_repair_enabled is False
    assert failure.auto_retry_enabled is False


def test_session_monitor_trace_pig_patterns_context_and_metrics_are_descriptive_only() -> None:
    parts = _parts()
    session_policy = parts["session_monitor_policy"]
    session_view = parts["session_monitor_view"]
    session_card = parts["session_cards"][0]
    trace = parts["session_trace_summaries"][0]
    pig = parts["pig_guidance_summaries"][0]
    decision_pattern = parts["decision_pattern_views"][0]
    route_pattern = parts["route_pattern_views"][0]
    provider_pattern = parts["provider_pattern_views"][0]
    safety_pattern = parts["safety_pattern_views"][0]
    failure_pattern = parts["failure_pattern_views"][0]
    context = parts["context_ref_views"][0]
    metric = parts["metric_set"]

    assert session_policy.session_view_is_not_memory_continuity is True
    assert session_policy.raw_transcript_storage_forbidden is True
    assert session_policy.persistent_memory_write_forbidden is True
    assert session_policy.memory_promotion_forbidden is True
    assert session_policy.autonomous_optimization_forbidden is True
    assert session_view.background_monitor_started is False
    assert session_view.memory_continuity_enabled is False
    assert session_view.memory_promoted is False
    assert session_view.raw_transcript_included is False
    assert session_card.raw_transcript_included is False
    assert session_card.memory_continuity_enabled is False
    assert trace.raw_transcript_included is False
    assert pig.pig_guidance_is_memory is False
    assert pig.pig_guidance_mutates_policy is False
    assert pig.pig_guidance_executes is False
    assert decision_pattern.autonomous_optimization_performed is False
    assert route_pattern.route_rerun_triggered is False
    assert provider_pattern.provider_invoked_now is False
    assert safety_pattern.safety_policy_mutated_now is False
    assert failure_pattern.auto_retry_enabled is False
    assert failure_pattern.automatic_repair_enabled is False
    assert context.refs_only is True
    assert context.raw_transcript_included is False
    assert context.memory_promoted is False
    assert metric.direct_bypass_count == 0
    assert metric.command_rerun_count == 0
    assert metric.automatic_repair_count == 0
    assert metric.autonomous_loop_count == 0
    assert metric.background_execution_count == 0
    assert metric.memory_promotion_count == 0
    assert metric.raw_transcript_persistence_count == 0


def test_report_flags_ocel_pig_ocpx_and_cli_outputs(capsys) -> None:
    service = WorkbenchRunDashboardReportService()
    parts = service.build_all_parts()
    report = parts["report"]
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert report.report_status in {"passed", "warning"}
    assert report.ready_for_v0_26_7 is True
    assert report.ready_for_v0_27 is False
    assert report.run_dashboard_view_created is True
    assert report.session_monitor_view_created is True
    assert report.run_cards_created is True
    assert report.pipeline_status_views_created is True
    assert report.provider_status_summary_created is True
    assert report.response_status_summary_created is True
    assert report.safety_status_summary_created is True
    assert report.approval_status_summary_created is True
    assert report.failure_summary_created is True
    assert report.warning_summary_created is True
    assert report.session_trace_summaries_created is True
    assert report.session_pig_guidance_summaries_created is True
    assert report.repeated_pattern_views_created is True
    assert report.session_context_ref_views_created is True
    assert report.metric_set_created is True
    assert report.actual_ui_rendered is False
    assert report.background_monitor_started is False
    assert report.continuous_watcher_started is False
    assert report.auto_refresh_execution_started is False
    assert report.rerun_performed is False
    assert report.automatic_retry_performed is False
    assert report.automatic_repair_performed is False
    assert report.autonomous_optimization_performed is False
    assert report.command_executed is False
    assert report.approval_executed is False
    assert report.provider_invoked is False
    assert report.ask_executed is False
    assert report.final_response_emitted is False
    assert report.local_command_executed is False
    assert report.memory_continuity_enabled is False
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.persona_mutated is False
    assert report.external_provider_adapter_implemented is False
    assert report.vendor_adapter_implemented is False
    assert report.pig_memory_promoted is False
    assert report.pig_policy_mutated is False
    assert report.pig_executed is False
    assert report.schumpeter_split_introduced is False
    assert report.raw_secret_output is False
    assert report.raw_provider_output_inline is False
    assert report.raw_transcript_persisted is False
    assert report.llm_judge_used is False
    assert report.next_required_step == "v0.26.7 Workbench Command Surface"
    assert "workbench_run_dashboard_policy" in WORKBENCH_RUN_DASHBOARD_OBJECT_TYPES
    assert "workbench_run_dashboard_report_created" in WORKBENCH_RUN_DASHBOARD_EVENT_TYPES
    assert "creates_run_dashboard_view" in WORKBENCH_RUN_DASHBOARD_RELATION_TYPES
    assert "workbench_run_dashboard_created" in WORKBENCH_RUN_DASHBOARD_EFFECT_TYPES
    assert "background_monitor_started" in WORKBENCH_RUN_DASHBOARD_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.26.6"
    assert pig["subject"] == "run_dashboard_session_monitor"
    assert ocpx["state"] == "workbench_run_dashboard_session_monitor_created"
    assert "WorkbenchRunDashboardViewState" in ocpx["target_read_models"]

    assert main(["workbench", "dashboard", "view"]) == 0
    output = capsys.readouterr().out
    assert "version=v0.26.6" in output
    assert "run_dashboard_view_created=true" in output
    assert "session_monitor_view_created=true" in output
    assert "ready_for_v0_26_7=true" in output
    assert "ready_for_v0_27=false" in output
    assert "background_monitor_started=false" in output
    assert "command_executed=false" in output
    assert "provider_invoked=false" in output
    assert "raw_transcript_persisted=false" in output

    assert main(["workbench", "sessions", "monitor"]) == 0
    output = capsys.readouterr().out
    assert "monitor_status=ready" in output
    assert "memory_continuity_enabled=false" in output
