from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace_agent_workbench.view_state import WorkbenchViewStateReportService


WORKBENCH_RUN_DASHBOARD_VERSION = "v0.26.6"
WORKBENCH_RUN_DASHBOARD_VERSION_NAME = "Run Dashboard / Session Monitor"
WORKBENCH_RUN_DASHBOARD_KOREAN_NAME = "Run Dashboard.Session Monitor"
WORKBENCH_RUN_DASHBOARD_LAYER = "workspace_agent_workbench"
WORKBENCH_RUN_DASHBOARD_TRACK = "Workspace Agent Workbench"
WORKBENCH_RUN_DASHBOARD_NEXT_STEP = "v0.26.7 Workbench Command Surface"

WORKBENCH_RUN_DASHBOARD_IMPLEMENTED_SKILL_IDS = [
    "skill:workbench_run_dashboard_view",
    "skill:workbench_session_monitor_view",
]
WORKBENCH_RUN_DASHBOARD_FUTURE_SKILL_IDS = [
    "skill:workbench_command_surface_use",
    "skill:workbench_snapshot_create",
    "skill:workbench_ocel_export_create",
    "skill:workbench_consolidation_view",
]

WORKBENCH_RUN_DASHBOARD_OBJECT_TYPES = [
    "workbench_run_dashboard_policy",
    "workbench_run_dashboard_request",
    "workbench_run_dashboard_source_view",
    "workbench_run_dashboard_view",
    "workbench_run_card",
    "workbench_pipeline_status_view",
    "workbench_stage_status_summary",
    "workbench_provider_status_summary",
    "workbench_response_status_summary",
    "workbench_safety_status_summary",
    "workbench_approval_status_summary",
    "workbench_failure_summary",
    "workbench_warning_summary",
    "workbench_session_monitor_policy",
    "workbench_session_monitor_view",
    "workbench_session_card",
    "workbench_session_trace_summary",
    "workbench_session_pig_guidance_summary",
    "workbench_session_decision_pattern_view",
    "workbench_session_route_pattern_view",
    "workbench_session_provider_pattern_view",
    "workbench_session_safety_pattern_view",
    "workbench_session_failure_pattern_view",
    "workbench_session_context_ref_view",
    "workbench_run_dashboard_metric_set",
    "workbench_run_dashboard_finding",
    "workbench_run_dashboard_report",
    "workbench_approval_console_report",
    "workbench_evidence_inspector_report",
    "workbench_provider_browser_report",
    "agent_ask_repl_report",
    "agent_trace_telemetry_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

WORKBENCH_RUN_DASHBOARD_EVENT_TYPES = [
    "workbench_run_dashboard_requested",
    "workbench_run_dashboard_policy_created",
    "workbench_run_dashboard_source_view_created",
    "workbench_run_dashboard_view_created",
    "workbench_run_card_created",
    "workbench_pipeline_status_view_created",
    "workbench_stage_status_summary_created",
    "workbench_provider_status_summary_created",
    "workbench_response_status_summary_created",
    "workbench_safety_status_summary_created",
    "workbench_approval_status_summary_created",
    "workbench_failure_summary_created",
    "workbench_warning_summary_created",
    "workbench_session_monitor_policy_created",
    "workbench_session_monitor_view_created",
    "workbench_session_card_created",
    "workbench_session_trace_summary_created",
    "workbench_session_pig_guidance_summary_created",
    "workbench_session_decision_pattern_view_created",
    "workbench_session_route_pattern_view_created",
    "workbench_session_provider_pattern_view_created",
    "workbench_session_safety_pattern_view_created",
    "workbench_session_failure_pattern_view_created",
    "workbench_session_context_ref_view_created",
    "workbench_run_dashboard_metric_set_created",
    "workbench_run_dashboard_report_created",
    "workbench_run_dashboard_warning_created",
    "workbench_run_dashboard_blocked",
]

WORKBENCH_RUN_DASHBOARD_RELATION_TYPES = [
    "uses_workbench_view_state",
    "uses_run_dashboard_panel",
    "uses_session_monitor_panel",
    "uses_ask_repl_report",
    "uses_pipeline_run_ref",
    "uses_trace_telemetry_report",
    "uses_approval_console_report",
    "uses_evidence_inspector_report",
    "uses_provider_browser_report",
    "uses_pig_guidance_ref",
    "creates_run_dashboard_view",
    "creates_run_card",
    "creates_pipeline_status_view",
    "creates_status_summary",
    "creates_session_monitor_view",
    "creates_session_summary",
    "creates_session_pattern_view",
    "creates_run_dashboard_metric_set",
    "defers_command_surface_to_v0_26_7",
    "defers_snapshot_export_to_v0_26_8",
    "defers_memory_continuity_to_v0_27",
    "not_background_monitor_started",
    "not_continuous_watcher_started",
    "not_rerun_performed",
    "not_command_executed",
    "not_provider_invoked",
    "not_pig_memory_promoted",
    "not_pig_policy_mutated",
    "not_pig_executed",
    "blocks_raw_provider_output_inline",
    "blocks_raw_transcript_persistence",
    "recorded_in_envelope",
]

WORKBENCH_RUN_DASHBOARD_EFFECT_TYPES = [
    "read_only_observation",
    "workbench_run_dashboard_created",
    "workbench_run_card_created",
    "workbench_pipeline_status_view_created",
    "workbench_status_summary_created",
    "workbench_session_monitor_created",
    "workbench_session_summary_created",
    "workbench_session_pattern_view_created",
    "workbench_run_dashboard_metric_created",
    "state_candidate_created",
]

WORKBENCH_RUN_DASHBOARD_FORBIDDEN_EFFECT_TYPES = [
    "background_monitor_started",
    "continuous_watcher_started",
    "auto_refresh_execution_started",
    "rerun_performed",
    "automatic_retry_performed",
    "automatic_repair_performed",
    "autonomous_optimization_performed",
    "command_executed",
    "approval_executed",
    "provider_invoked",
    "internal_provider_invoked",
    "provider_test_run_performed",
    "route_rerun_performed",
    "stage_rerun_performed",
    "agent_ask_executed",
    "agent_repl_started",
    "final_response_emitted",
    "local_command_executed",
    "bounded_local_command_executed",
    "command_rerun_performed",
    "direct_file_access_performed",
    "direct_subprocess_called",
    "memory_continuity_enabled",
    "memory_promoted",
    "persistent_memory_written",
    "persona_mutated",
    "external_provider_called",
    "external_agent_runtime_touched",
    "external_provider_adapter_implemented",
    "external_agent_adapter_implemented",
    "vendor_adapter_implemented",
    "pig_memory_promoted",
    "pig_policy_mutated",
    "pig_executed",
    "file_written",
    "file_edited",
    "file_deleted",
    "credential_exposed",
    "raw_secret_output",
    "raw_provider_output_inline",
    "raw_transcript_persisted",
    "schumpeter_split_introduced",
]


def _safe_id(value: str | None) -> str:
    text = value or "unknown"
    return "".join(char if char.isalnum() else "_" for char in text).strip("_").lower() or "unknown"


def _ref(ref_type: str, ref_id: str, version: str = WORKBENCH_RUN_DASHBOARD_VERSION) -> dict[str, Any]:
    return {"type": ref_type, "id": ref_id, "version": version}


def _panel_ref(panel_type: str, available: bool) -> dict[str, Any] | None:
    if not available:
        return None
    return _ref("workbench_panel", f"workbench_panel:{panel_type}", "v0.26.1")


def _model_ref(ref_type: str, model: Any, id_attr: str) -> dict[str, Any]:
    return _ref(ref_type, getattr(model, id_attr), getattr(model, "version", WORKBENCH_RUN_DASHBOARD_VERSION))


def _status_from_counts(warnings: int = 0, failures: int = 0, blocked: int = 0, total: int = 1) -> str:
    if blocked:
        return "blocked"
    if failures:
        return "failed"
    if warnings:
        return "warning"
    if total <= 0:
        return "missing"
    return "completed"


class _Model:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class WorkbenchRunDashboardPolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    layer: str = WORKBENCH_RUN_DASHBOARD_LAYER
    run_dashboard_enabled: bool = True
    session_monitor_enabled: bool = True
    run_status_summary_enabled: bool = True
    session_summary_enabled: bool = True
    pig_guidance_summary_enabled: bool = True
    repeated_pattern_view_enabled: bool = True
    failure_pattern_view_enabled: bool = True
    actual_ui_rendering_enabled: bool = False
    panel_rendering_enabled: bool = False
    background_monitor_enabled: bool = False
    continuous_watcher_enabled: bool = False
    auto_refresh_execution_enabled: bool = False
    rerun_enabled: bool = False
    automatic_retry_enabled: bool = False
    automatic_repair_enabled: bool = False
    autonomous_optimization_enabled: bool = False
    command_execution_enabled: bool = False
    approval_execution_enabled: bool = False
    provider_invocation_enabled: bool = False
    ask_execution_enabled: bool = False
    response_emission_enabled: bool = False
    local_runtime_execution_enabled: bool = False
    memory_continuity_enabled: bool = False
    memory_promotion_enabled: bool = False
    persistent_memory_write_enabled: bool = False
    persona_mutation_enabled: bool = False
    external_adapter_enabled: bool = False
    refs_only_by_default: bool = True
    raw_provider_output_inline_forbidden: bool = True
    raw_transcript_inline_forbidden: bool = True
    raw_secret_inline_forbidden: bool = True
    credential_inline_forbidden: bool = True
    private_path_sanitization_required: bool = True
    pig_guidance_is_not_memory: bool = True
    pig_guidance_is_not_policy_mutation: bool = True
    pig_guidance_is_not_execution: bool = True
    ocel_visible: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchRunDashboardRequest(_Model):
    request_id: str
    view_state_report_id: str | None
    view_state_id: str | None
    run_dashboard_panel_id: str | None
    session_monitor_panel_id: str | None
    ask_repl_report_ids: list[str]
    pipeline_run_ids: list[str]
    repl_session_ids: list[str]
    trace_telemetry_report_ids: list[str]
    approval_console_report_ids: list[str]
    evidence_inspector_report_ids: list[str]
    provider_browser_report_ids: list[str]
    focus_run_ref: dict[str, Any] | None
    focus_session_ref: dict[str, Any] | None
    pig_guidance_refs: list[dict[str, Any]]
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"


@dataclass
class WorkbenchRunDashboardSourceView(_Model):
    source_view_id: str
    ask_repl_report_refs: list[dict[str, Any]]
    pipeline_run_refs: list[dict[str, Any]]
    pipeline_result_refs: list[dict[str, Any]]
    surface_emission_refs: list[dict[str, Any]]
    repl_session_refs: list[dict[str, Any]]
    repl_turn_refs: list[dict[str, Any]]
    trace_report_refs: list[dict[str, Any]]
    approval_report_refs: list[dict[str, Any]]
    evidence_report_refs: list[dict[str, Any]]
    provider_report_refs: list[dict[str, Any]]
    pig_guidance_refs: list[dict[str, Any]]
    source_status: str
    run_count: int
    session_count: int
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    raw_provider_output_included: bool = False
    raw_transcript_included: bool = False
    raw_secret_included: bool = False
    private_full_path_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchStageStatusSummary(_Model):
    stage_status_summary_id: str
    stage_status_rows: list[dict[str, Any]]
    total_stage_count: int
    completed_count: int
    warning_count: int
    failed_count: int
    blocked_count: int
    skipped_count: int
    missing_count: int
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchPipelineStatusView(_Model):
    pipeline_status_view_id: str
    pipeline_run_ref: dict[str, Any]
    stage_status_summary: WorkbenchStageStatusSummary
    pipeline_status: str
    completed_stage_count: int
    warning_stage_count: int
    failed_stage_count: int
    blocked_stage_count: int
    skipped_stage_count: int
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    rerun_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchRunCard(_Model):
    run_card_id: str
    run_ref: dict[str, Any]
    run_type: str
    title: str
    status: str
    stage_summary_refs: list[dict[str, Any]]
    decision_summary_refs: list[dict[str, Any]]
    provider_summary_refs: list[dict[str, Any]]
    evidence_summary_refs: list[dict[str, Any]]
    safety_summary_refs: list[dict[str, Any]]
    approval_summary_refs: list[dict[str, Any]]
    failure_summary_refs: list[dict[str, Any]]
    pig_guidance_refs: list[dict[str, Any]]
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    rerun_enabled: bool = False
    command_enabled: bool = False
    provider_invocation_enabled: bool = False
    raw_transcript_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchProviderStatusSummary(_Model):
    provider_status_summary_id: str
    provider_invocation_count: int
    provider_warning_count: int
    provider_failed_count: int
    provider_blocked_count: int
    provider_boundary_warning_count: int
    provider_summary_refs: list[dict[str, Any]]
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    direct_provider_invocation_count: int = 0
    provider_invocation_enabled_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchResponseStatusSummary(_Model):
    response_status_summary_id: str
    response_assembly_count: int
    final_response_emission_count: int
    unsupported_claim_count: int
    uncertainty_note_count: int
    limitation_note_count: int
    response_failed_count: int
    response_blocked_count: int
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    response_rewrite_performed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSafetyStatusSummary(_Model):
    safety_status_summary_id: str
    safety_gate_count: int
    allow_route_count: int
    no_action_count: int
    clarification_count: int
    needs_more_input_count: int
    blocked_count: int
    deferred_count: int
    safety_warning_count: int
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    safety_policy_mutation_count: int = 0
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchApprovalStatusSummary(_Model):
    approval_status_summary_id: str
    approval_candidate_count: int
    approval_decision_count: int
    rejection_decision_count: int
    deferral_decision_count: int
    manual_review_count: int
    expired_approval_count: int
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    approval_executed_count: int = 0
    auto_approval_count: int = 0
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSessionFailurePatternView(_Model):
    failure_pattern_view_id: str
    session_ref: dict[str, Any] | None
    failure_category: str
    occurrence_count: int
    affected_run_refs: list[dict[str, Any]]
    recovery_guidance_refs: list[dict[str, Any]]
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    auto_retry_enabled: bool = False
    automatic_repair_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchFailureSummary(_Model):
    failure_summary_id: str
    failure_count: int
    failure_rows: list[dict[str, Any]]
    repeated_failure_patterns: list[WorkbenchSessionFailurePatternView]
    recovery_guidance_refs: list[dict[str, Any]]
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    automatic_repair_enabled: bool = False
    auto_retry_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchWarningSummary(_Model):
    warning_summary_id: str
    warning_count: int
    warning_rows: list[dict[str, Any]]
    repeated_warning_patterns: list[dict[str, Any]]
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchRunDashboardMetricSet(_Model):
    metric_set_id: str
    run_count: int
    session_count: int
    completed_run_count: int
    warning_run_count: int
    failed_run_count: int
    blocked_run_count: int
    approval_candidate_count: int
    approval_decision_count: int
    provider_invocation_count: int
    provider_failed_count: int
    safety_block_count: int
    unsupported_claim_count: int
    uncertainty_count: int
    limitation_count: int
    repeated_route_pattern_count: int
    repeated_provider_pattern_count: int
    repeated_safety_pattern_count: int
    repeated_failure_pattern_count: int
    metric_status: str
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    direct_bypass_count: int = 0
    command_rerun_count: int = 0
    automatic_repair_count: int = 0
    autonomous_loop_count: int = 0
    background_execution_count: int = 0
    memory_promotion_count: int = 0
    raw_transcript_persistence_count: int = 0
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchRunDashboardView(_Model):
    run_dashboard_view_id: str
    panel_id: str | None
    source_view: WorkbenchRunDashboardSourceView
    run_cards: list[WorkbenchRunCard]
    pipeline_status_views: list[WorkbenchPipelineStatusView]
    provider_status_summary: WorkbenchProviderStatusSummary | None
    response_status_summary: WorkbenchResponseStatusSummary | None
    safety_status_summary: WorkbenchSafetyStatusSummary | None
    approval_status_summary: WorkbenchApprovalStatusSummary | None
    failure_summary: WorkbenchFailureSummary | None
    warning_summary: WorkbenchWarningSummary | None
    metric_set: WorkbenchRunDashboardMetricSet | None
    view_status: str
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    renders_ui_now: bool = False
    background_monitor_started: bool = False
    auto_refresh_execution_started: bool = False
    rerun_performed: bool = False
    automatic_repair_performed: bool = False
    command_executed: bool = False
    provider_invoked: bool = False
    memory_promoted: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSessionMonitorPolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    session_monitor_enabled: bool = True
    session_summary_enabled: bool = True
    session_trace_summary_enabled: bool = True
    session_pig_guidance_summary_enabled: bool = True
    decision_pattern_view_enabled: bool = True
    route_pattern_view_enabled: bool = True
    provider_pattern_view_enabled: bool = True
    safety_pattern_view_enabled: bool = True
    failure_pattern_view_enabled: bool = True
    session_view_is_not_memory_continuity: bool = True
    raw_transcript_storage_forbidden: bool = True
    persistent_memory_write_forbidden: bool = True
    memory_promotion_forbidden: bool = True
    autonomous_optimization_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSessionCard(_Model):
    session_card_id: str
    session_ref: dict[str, Any]
    session_type: str
    turn_count: int
    run_count: int
    status: str
    summary_refs: list[dict[str, Any]]
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    raw_transcript_included: bool = False
    memory_continuity_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSessionTraceSummary(_Model):
    session_trace_summary_id: str
    session_ref: dict[str, Any]
    trace_refs: list[dict[str, Any]]
    stage_summary_refs: list[dict[str, Any]]
    decision_summary_refs: list[dict[str, Any]]
    route_summary_refs: list[dict[str, Any]]
    provider_summary_refs: list[dict[str, Any]]
    response_summary_refs: list[dict[str, Any]]
    summary_status: str
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    raw_transcript_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSessionPIGGuidanceSummary(_Model):
    session_pig_guidance_summary_id: str
    session_ref: dict[str, Any]
    pig_guidance_refs: list[dict[str, Any]]
    recommendation_count: int
    warning_count: int
    candidate_count: int
    rationale_count: int
    pattern_summary_count: int
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    pig_guidance_is_memory: bool = False
    pig_guidance_mutates_policy: bool = False
    pig_guidance_executes: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSessionDecisionPatternView(_Model):
    decision_pattern_view_id: str
    session_ref: dict[str, Any]
    decision_type: str
    occurrence_count: int
    outcome_distribution: dict[str, int]
    source_refs: list[dict[str, Any]]
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    autonomous_optimization_performed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSessionRoutePatternView(_Model):
    route_pattern_view_id: str
    session_ref: dict[str, Any]
    route_kind: str
    occurrence_count: int
    success_count: int
    warning_count: int
    failed_count: int
    blocked_count: int
    source_refs: list[dict[str, Any]]
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    route_rerun_triggered: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSessionProviderPatternView(_Model):
    provider_pattern_view_id: str
    session_ref: dict[str, Any]
    provider_id: str | None
    capability_id: str | None
    occurrence_count: int
    warning_count: int
    failed_count: int
    boundary_warning_count: int
    source_refs: list[dict[str, Any]]
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    provider_invoked_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSessionSafetyPatternView(_Model):
    safety_pattern_view_id: str
    session_ref: dict[str, Any]
    safety_outcome: str
    occurrence_count: int
    repeated_warning: bool
    repeated_block: bool
    source_refs: list[dict[str, Any]]
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    safety_policy_mutated_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSessionContextRefView(_Model):
    context_ref_view_id: str
    session_ref: dict[str, Any]
    context_kind: str
    context_refs: list[dict[str, Any]]
    context_summary: str
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    refs_only: bool = True
    raw_transcript_included: bool = False
    memory_promoted: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSessionMonitorView(_Model):
    session_monitor_view_id: str
    panel_id: str | None
    session_cards: list[WorkbenchSessionCard]
    session_trace_summaries: list[WorkbenchSessionTraceSummary]
    pig_guidance_summaries: list[WorkbenchSessionPIGGuidanceSummary]
    decision_pattern_views: list[WorkbenchSessionDecisionPatternView]
    route_pattern_views: list[WorkbenchSessionRoutePatternView]
    provider_pattern_views: list[WorkbenchSessionProviderPatternView]
    safety_pattern_views: list[WorkbenchSessionSafetyPatternView]
    failure_pattern_views: list[WorkbenchSessionFailurePatternView]
    context_ref_views: list[WorkbenchSessionContextRefView]
    monitor_status: str
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    renders_ui_now: bool = False
    background_monitor_started: bool = False
    memory_continuity_enabled: bool = False
    memory_promoted: bool = False
    raw_transcript_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchRunDashboardFinding(_Model):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION


@dataclass
class WorkbenchRunDashboardReport(_Model):
    report_id: str
    created_at: str
    dashboard_policy: WorkbenchRunDashboardPolicy
    request: WorkbenchRunDashboardRequest
    source_view: WorkbenchRunDashboardSourceView
    run_dashboard_view: WorkbenchRunDashboardView
    session_monitor_policy: WorkbenchSessionMonitorPolicy
    session_monitor_view: WorkbenchSessionMonitorView
    metric_set: WorkbenchRunDashboardMetricSet
    findings: list[WorkbenchRunDashboardFinding]
    report_status: str
    ready_for_v0_26_7: bool
    run_dashboard_view_created: bool
    session_monitor_view_created: bool
    run_cards_created: bool
    pipeline_status_views_created: bool
    provider_status_summary_created: bool
    response_status_summary_created: bool
    safety_status_summary_created: bool
    approval_status_summary_created: bool
    failure_summary_created: bool
    warning_summary_created: bool
    session_trace_summaries_created: bool
    session_pig_guidance_summaries_created: bool
    repeated_pattern_views_created: bool
    session_context_ref_views_created: bool
    metric_set_created: bool
    version: str = WORKBENCH_RUN_DASHBOARD_VERSION
    ready_for_v0_27: bool = False
    actual_ui_rendered: bool = False
    panel_rendered: bool = False
    background_monitor_started: bool = False
    continuous_watcher_started: bool = False
    auto_refresh_execution_started: bool = False
    rerun_performed: bool = False
    automatic_retry_performed: bool = False
    automatic_repair_performed: bool = False
    autonomous_optimization_performed: bool = False
    command_executed: bool = False
    approval_executed: bool = False
    provider_invoked: bool = False
    ask_executed: bool = False
    final_response_emitted: bool = False
    local_command_executed: bool = False
    direct_file_access_performed: bool = False
    direct_subprocess_performed: bool = False
    memory_continuity_enabled: bool = False
    memory_promoted: bool = False
    persistent_memory_written: bool = False
    persona_mutated: bool = False
    external_provider_adapter_implemented: bool = False
    external_agent_adapter_implemented: bool = False
    vendor_adapter_implemented: bool = False
    pig_memory_promoted: bool = False
    pig_policy_mutated: bool = False
    pig_executed: bool = False
    schumpeter_split_introduced: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    raw_provider_output_inline: bool = False
    raw_transcript_persisted: bool = False
    llm_judge_used: bool = False
    next_required_step: str = WORKBENCH_RUN_DASHBOARD_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = (
        "Valid until v0.26.7 Workbench Command Surface begins or run dashboard/session monitor policy changes."
    )


class WorkbenchRunDashboardPrerequisiteSourceService:
    def __init__(
        self,
        *,
        view_state_available: bool = True,
        run_dashboard_panel_available: bool = True,
        session_monitor_panel_available: bool = True,
        ask_repl_available: bool = True,
        trace_telemetry_available: bool = True,
        approval_console_available: bool = True,
        evidence_inspector_available: bool = True,
        provider_browser_available: bool = True,
        pig_guidance_available: bool = True,
    ) -> None:
        self.view_state_available = view_state_available
        self.run_dashboard_panel_available = run_dashboard_panel_available
        self.session_monitor_panel_available = session_monitor_panel_available
        self.ask_repl_available = ask_repl_available
        self.trace_telemetry_available = trace_telemetry_available
        self.approval_console_available = approval_console_available
        self.evidence_inspector_available = evidence_inspector_available
        self.provider_browser_available = provider_browser_available
        self.pig_guidance_available = pig_guidance_available

    def load_workbench_view_state(self) -> dict[str, Any]:
        if not self.view_state_available:
            return {"available": False, "source_id": None, "report": None, "view_state": None}
        parts = WorkbenchViewStateReportService().build_all_parts()
        return {
            "available": True,
            "source_id": parts["report"].report_id,
            "report": parts["report"],
            "view_state": parts["view_state"],
        }

    def load_run_dashboard_panel_model(self) -> dict[str, Any]:
        return {
            "available": self.run_dashboard_panel_available,
            "source_id": "workbench_panel:run_dashboard" if self.run_dashboard_panel_available else None,
            "ref": _panel_ref("run_dashboard", self.run_dashboard_panel_available),
        }

    def load_session_monitor_panel_model(self) -> dict[str, Any]:
        return {
            "available": self.session_monitor_panel_available,
            "source_id": "workbench_panel:session_monitor" if self.session_monitor_panel_available else None,
            "ref": _panel_ref("session_monitor", self.session_monitor_panel_available),
        }

    def load_ask_repl_reports_if_available(self) -> list[dict[str, Any]]:
        if not self.ask_repl_available:
            return []
        return [_ref("agent_ask_repl_report", "agent_ask_repl_report:v0.25.7:existing", "v0.25.7")]

    def load_pipeline_runs_if_available(self) -> list[dict[str, Any]]:
        if not self.ask_repl_available:
            return []
        return [_ref("agent_ask_pipeline_run", "agent_ask_pipeline_run:v0.25.7:existing", "v0.25.7")]

    def load_pipeline_results_if_available(self) -> list[dict[str, Any]]:
        if not self.ask_repl_available:
            return []
        return [_ref("agent_ask_pipeline_result", "agent_ask_pipeline_result:v0.25.7:existing", "v0.25.7")]

    def load_surface_emissions_if_available(self) -> list[dict[str, Any]]:
        if not self.ask_repl_available:
            return []
        return [_ref("agent_surface_emission", "agent_surface_emission:v0.25.7:existing", "v0.25.7")]

    def load_repl_sessions_if_available(self) -> list[dict[str, Any]]:
        if not self.ask_repl_available:
            return []
        return [_ref("agent_repl_session", "agent_repl_session:v0.25.7:existing", "v0.25.7")]

    def load_repl_turns_if_available(self) -> list[dict[str, Any]]:
        if not self.ask_repl_available:
            return []
        return [_ref("agent_repl_turn_result", "agent_repl_turn_result:v0.25.7:existing", "v0.25.7")]

    def load_trace_telemetry_reports_if_available(self) -> list[dict[str, Any]]:
        if not self.trace_telemetry_available:
            return []
        return [_ref("agent_trace_telemetry_report", "agent_trace_telemetry_report:v0.25.8:existing", "v0.25.8")]

    def load_approval_console_reports_if_available(self) -> list[dict[str, Any]]:
        if not self.approval_console_available:
            return []
        return [_ref("workbench_approval_console_report", "workbench_approval_console_report:v0.26.5:existing", "v0.26.5")]

    def load_evidence_inspector_reports_if_available(self) -> list[dict[str, Any]]:
        if not self.evidence_inspector_available:
            return []
        return [_ref("workbench_evidence_inspector_report", "workbench_evidence_inspector_report:v0.26.4:existing", "v0.26.4")]

    def load_provider_browser_reports_if_available(self) -> list[dict[str, Any]]:
        if not self.provider_browser_available:
            return []
        return [_ref("workbench_provider_browser_report", "workbench_provider_browser_report:v0.26.3:existing", "v0.26.3")]

    def load_pig_guidance_refs_if_available(self) -> list[dict[str, Any]]:
        if not self.pig_guidance_available:
            return []
        return [
            _ref("pig_guidance_ref", "pig_guidance:run-dashboard-session-monitor:recommendation", "v0.26.6"),
            _ref("pig_guidance_ref", "pig_guidance:run-dashboard-session-monitor:pattern-summary", "v0.26.6"),
        ]


class WorkbenchRunDashboardPolicyService:
    def build_policy(self) -> WorkbenchRunDashboardPolicy:
        return WorkbenchRunDashboardPolicy(
            policy_id="workbench_run_dashboard_policy:v0.26.6",
            evidence_refs=[_ref("workbench_policy_boundary", "run_dashboard_session_monitor_view_only")],
        )


class WorkbenchRunDashboardRequestService:
    def __init__(self, source_service: WorkbenchRunDashboardPrerequisiteSourceService | None = None) -> None:
        self.source_service = source_service or WorkbenchRunDashboardPrerequisiteSourceService()

    def build_request(self, strictness: str = "standard") -> WorkbenchRunDashboardRequest:
        view_state = self.source_service.load_workbench_view_state()
        run_panel = self.source_service.load_run_dashboard_panel_model()
        session_panel = self.source_service.load_session_monitor_panel_model()
        ask_refs = self.source_service.load_ask_repl_reports_if_available()
        pipeline_refs = self.source_service.load_pipeline_runs_if_available()
        session_refs = self.source_service.load_repl_sessions_if_available()
        trace_refs = self.source_service.load_trace_telemetry_reports_if_available()
        approval_refs = self.source_service.load_approval_console_reports_if_available()
        evidence_refs = self.source_service.load_evidence_inspector_reports_if_available()
        provider_refs = self.source_service.load_provider_browser_reports_if_available()
        pig_refs = self.source_service.load_pig_guidance_refs_if_available()
        source_refs = [
            ref
            for ref in [
                run_panel.get("ref"),
                session_panel.get("ref"),
                *ask_refs,
                *trace_refs,
                *approval_refs,
                *evidence_refs,
                *provider_refs,
            ]
            if ref is not None
        ]
        return WorkbenchRunDashboardRequest(
            request_id="workbench_run_dashboard_request:v0.26.6",
            view_state_report_id=view_state["source_id"],
            view_state_id=(view_state["view_state"].view_state_id if view_state.get("view_state") else None),
            run_dashboard_panel_id=run_panel["source_id"],
            session_monitor_panel_id=session_panel["source_id"],
            ask_repl_report_ids=[ref["id"] for ref in ask_refs],
            pipeline_run_ids=[ref["id"] for ref in pipeline_refs],
            repl_session_ids=[ref["id"] for ref in session_refs],
            trace_telemetry_report_ids=[ref["id"] for ref in trace_refs],
            approval_console_report_ids=[ref["id"] for ref in approval_refs],
            evidence_inspector_report_ids=[ref["id"] for ref in evidence_refs],
            provider_browser_report_ids=[ref["id"] for ref in provider_refs],
            focus_run_ref=pipeline_refs[0] if pipeline_refs else None,
            focus_session_ref=session_refs[0] if session_refs else None,
            pig_guidance_refs=pig_refs,
            source_refs=source_refs,
            strictness=strictness,
        )


class WorkbenchRunDashboardSourceViewService:
    def __init__(self, source_service: WorkbenchRunDashboardPrerequisiteSourceService | None = None) -> None:
        self.source_service = source_service or WorkbenchRunDashboardPrerequisiteSourceService()

    def build_source_view(self) -> WorkbenchRunDashboardSourceView:
        ask_refs = self.source_service.load_ask_repl_reports_if_available()
        pipeline_refs = self.source_service.load_pipeline_runs_if_available()
        result_refs = self.source_service.load_pipeline_results_if_available()
        emission_refs = self.source_service.load_surface_emissions_if_available()
        session_refs = self.source_service.load_repl_sessions_if_available()
        turn_refs = self.source_service.load_repl_turns_if_available()
        trace_refs = self.source_service.load_trace_telemetry_reports_if_available()
        approval_refs = self.source_service.load_approval_console_reports_if_available()
        evidence_refs = self.source_service.load_evidence_inspector_reports_if_available()
        provider_refs = self.source_service.load_provider_browser_reports_if_available()
        pig_refs = self.source_service.load_pig_guidance_refs_if_available()
        any_source = any([ask_refs, pipeline_refs, trace_refs, approval_refs, evidence_refs, provider_refs])
        core_available = (
            self.source_service.view_state_available
            and self.source_service.run_dashboard_panel_available
            and self.source_service.session_monitor_panel_available
        )
        source_status = "complete" if core_available and any_source else "partial" if any_source else "missing"
        run_count = len(ask_refs) + len(pipeline_refs) + len(trace_refs) + len(approval_refs)
        return WorkbenchRunDashboardSourceView(
            source_view_id="workbench_run_dashboard_source_view:v0.26.6",
            ask_repl_report_refs=ask_refs,
            pipeline_run_refs=pipeline_refs,
            pipeline_result_refs=result_refs,
            surface_emission_refs=emission_refs,
            repl_session_refs=session_refs,
            repl_turn_refs=turn_refs,
            trace_report_refs=trace_refs,
            approval_report_refs=approval_refs,
            evidence_report_refs=evidence_refs,
            provider_report_refs=provider_refs,
            pig_guidance_refs=pig_refs,
            source_status=source_status,
            run_count=run_count,
            session_count=len(session_refs),
            evidence_refs=ask_refs + pipeline_refs + trace_refs + approval_refs + evidence_refs + provider_refs,
        )


class WorkbenchStageStatusSummaryService:
    def build_stage_status_summary(self, source_view: WorkbenchRunDashboardSourceView) -> WorkbenchStageStatusSummary:
        stage_names = [
            "intent_classification",
            "safety_gate",
            "route_selection",
            "provider_selection",
            "response_assembly",
            "approval_console",
            "trace_telemetry",
        ]
        rows = [
            {
                "stage_id": f"stage:{stage_name}",
                "stage_name": stage_name,
                "status": "completed" if source_view.source_status in {"complete", "partial"} else "missing",
                "source_refs": source_view.evidence_refs[:2],
            }
            for stage_name in stage_names
        ]
        completed_count = sum(1 for row in rows if row["status"] == "completed")
        missing_count = sum(1 for row in rows if row["status"] == "missing")
        return WorkbenchStageStatusSummary(
            stage_status_summary_id="workbench_stage_status_summary:v0.26.6",
            stage_status_rows=rows,
            total_stage_count=len(rows),
            completed_count=completed_count,
            warning_count=0 if source_view.source_status == "complete" else 1,
            failed_count=0,
            blocked_count=0,
            skipped_count=0,
            missing_count=missing_count,
            evidence_refs=source_view.evidence_refs,
        )


class WorkbenchPipelineStatusViewService:
    def build_pipeline_status_views(
        self, source_view: WorkbenchRunDashboardSourceView, stage_summary: WorkbenchStageStatusSummary
    ) -> list[WorkbenchPipelineStatusView]:
        refs = source_view.pipeline_run_refs or [_ref("agent_ask_pipeline_run", "agent_ask_pipeline_run:v0.25.7:placeholder", "v0.25.7")]
        return [
            WorkbenchPipelineStatusView(
                pipeline_status_view_id=f"workbench_pipeline_status_view:{_safe_id(ref['id'])}",
                pipeline_run_ref=ref,
                stage_status_summary=stage_summary,
                pipeline_status=_status_from_counts(
                    stage_summary.warning_count,
                    stage_summary.failed_count,
                    stage_summary.blocked_count,
                    stage_summary.total_stage_count,
                ),
                completed_stage_count=stage_summary.completed_count,
                warning_stage_count=stage_summary.warning_count,
                failed_stage_count=stage_summary.failed_count,
                blocked_stage_count=stage_summary.blocked_count,
                skipped_stage_count=stage_summary.skipped_count,
                evidence_refs=[ref],
            )
            for ref in refs
        ]


class WorkbenchRunCardService:
    def build_run_cards(
        self, source_view: WorkbenchRunDashboardSourceView, pipeline_views: list[WorkbenchPipelineStatusView]
    ) -> list[WorkbenchRunCard]:
        card_specs = [
            ("ask", "Ask surface report", source_view.ask_repl_report_refs),
            ("pipeline_run", "Pipeline run", source_view.pipeline_run_refs),
            ("approval_console", "Approval console report", source_view.approval_report_refs),
            ("trace_telemetry", "Trace telemetry report", source_view.trace_report_refs),
        ]
        cards: list[WorkbenchRunCard] = []
        stage_ref = [_model_ref("workbench_pipeline_status_view", pipeline_views[0], "pipeline_status_view_id")] if pipeline_views else []
        for run_type, title, refs in card_specs:
            for ref in refs:
                cards.append(
                    WorkbenchRunCard(
                        run_card_id=f"workbench_run_card:{run_type}:{_safe_id(ref['id'])}",
                        run_ref=ref,
                        run_type=run_type,
                        title=title,
                        status="completed" if source_view.source_status in {"complete", "partial"} else "missing",
                        stage_summary_refs=stage_ref,
                        decision_summary_refs=[ref] if run_type in {"ask", "approval_console"} else [],
                        provider_summary_refs=source_view.provider_report_refs,
                        evidence_summary_refs=source_view.evidence_report_refs,
                        safety_summary_refs=source_view.approval_report_refs,
                        approval_summary_refs=source_view.approval_report_refs,
                        failure_summary_refs=[],
                        pig_guidance_refs=source_view.pig_guidance_refs,
                        evidence_refs=[ref],
                    )
                )
        if not cards:
            placeholder = _ref("workbench_run", "workbench_run:missing")
            cards.append(
                WorkbenchRunCard(
                    run_card_id="workbench_run_card:missing",
                    run_ref=placeholder,
                    run_type="unknown",
                    title="Missing run source",
                    status="missing",
                    stage_summary_refs=stage_ref,
                    decision_summary_refs=[],
                    provider_summary_refs=[],
                    evidence_summary_refs=[],
                    safety_summary_refs=[],
                    approval_summary_refs=[],
                    failure_summary_refs=[],
                    pig_guidance_refs=[],
                    evidence_refs=[],
                )
            )
        return cards


class WorkbenchProviderStatusSummaryService:
    def build_provider_status_summary(self, source_view: WorkbenchRunDashboardSourceView) -> WorkbenchProviderStatusSummary:
        return WorkbenchProviderStatusSummary(
            provider_status_summary_id="workbench_provider_status_summary:v0.26.6",
            provider_invocation_count=len(source_view.provider_report_refs),
            provider_warning_count=0,
            provider_failed_count=0,
            provider_blocked_count=0,
            provider_boundary_warning_count=0,
            provider_summary_refs=source_view.provider_report_refs,
            evidence_refs=source_view.provider_report_refs,
        )


class WorkbenchResponseStatusSummaryService:
    def build_response_status_summary(self, source_view: WorkbenchRunDashboardSourceView) -> WorkbenchResponseStatusSummary:
        return WorkbenchResponseStatusSummary(
            response_status_summary_id="workbench_response_status_summary:v0.26.6",
            response_assembly_count=len(source_view.evidence_report_refs),
            final_response_emission_count=len(source_view.surface_emission_refs),
            unsupported_claim_count=1 if source_view.evidence_report_refs else 0,
            uncertainty_note_count=1 if source_view.evidence_report_refs else 0,
            limitation_note_count=1 if source_view.evidence_report_refs else 0,
            response_failed_count=0,
            response_blocked_count=0,
            evidence_refs=source_view.evidence_report_refs + source_view.surface_emission_refs,
        )


class WorkbenchSafetyStatusSummaryService:
    def build_safety_status_summary(self, source_view: WorkbenchRunDashboardSourceView) -> WorkbenchSafetyStatusSummary:
        has_approval = bool(source_view.approval_report_refs)
        return WorkbenchSafetyStatusSummary(
            safety_status_summary_id="workbench_safety_status_summary:v0.26.6",
            safety_gate_count=1 if has_approval else 0,
            allow_route_count=1 if has_approval else 0,
            no_action_count=0,
            clarification_count=0,
            needs_more_input_count=0,
            blocked_count=0,
            deferred_count=0,
            safety_warning_count=0 if has_approval else 1,
            evidence_refs=source_view.approval_report_refs,
        )


class WorkbenchApprovalStatusSummaryService:
    def build_approval_status_summary(self, source_view: WorkbenchRunDashboardSourceView) -> WorkbenchApprovalStatusSummary:
        count = len(source_view.approval_report_refs)
        return WorkbenchApprovalStatusSummary(
            approval_status_summary_id="workbench_approval_status_summary:v0.26.6",
            approval_candidate_count=count,
            approval_decision_count=count,
            rejection_decision_count=count,
            deferral_decision_count=count,
            manual_review_count=count,
            expired_approval_count=0,
            evidence_refs=source_view.approval_report_refs,
        )


class WorkbenchFailureSummaryService:
    def build_failure_summary(
        self, source_view: WorkbenchRunDashboardSourceView, session_ref: dict[str, Any] | None = None
    ) -> WorkbenchFailureSummary:
        rows = []
        if source_view.source_status != "complete":
            rows.append(
                {
                    "failure_category": "missing_source",
                    "occurrence_count": 1,
                    "source_refs": source_view.evidence_refs,
                }
            )
        patterns = [
            WorkbenchSessionFailurePatternView(
                failure_pattern_view_id="workbench_session_failure_pattern_view:missing_source",
                session_ref=session_ref,
                failure_category="missing_source" if rows else "none",
                occurrence_count=len(rows),
                affected_run_refs=source_view.pipeline_run_refs,
                recovery_guidance_refs=[],
                evidence_refs=source_view.evidence_refs,
            )
        ]
        return WorkbenchFailureSummary(
            failure_summary_id="workbench_failure_summary:v0.26.6",
            failure_count=len(rows),
            failure_rows=rows,
            repeated_failure_patterns=patterns,
            recovery_guidance_refs=[],
            evidence_refs=source_view.evidence_refs,
        )


class WorkbenchWarningSummaryService:
    def build_warning_summary(self, source_view: WorkbenchRunDashboardSourceView) -> WorkbenchWarningSummary:
        rows = []
        if source_view.source_status != "complete":
            rows.append({"warning_type": "partial_source", "message": "Dashboard source view is partial.", "source_refs": source_view.evidence_refs})
        return WorkbenchWarningSummary(
            warning_summary_id="workbench_warning_summary:v0.26.6",
            warning_count=len(rows),
            warning_rows=rows,
            repeated_warning_patterns=rows,
            evidence_refs=source_view.evidence_refs,
        )


class WorkbenchSessionMonitorPolicyService:
    def build_policy(self) -> WorkbenchSessionMonitorPolicy:
        return WorkbenchSessionMonitorPolicy(
            policy_id="workbench_session_monitor_policy:v0.26.6",
            evidence_refs=[_ref("workbench_policy_boundary", "session_monitor_view_only")],
        )


class WorkbenchSessionCardService:
    def build_session_cards(self, source_view: WorkbenchRunDashboardSourceView) -> list[WorkbenchSessionCard]:
        refs = source_view.repl_session_refs or [_ref("workbench_session", "workbench_session:v0.26.6:synthetic-summary")]
        return [
            WorkbenchSessionCard(
                session_card_id=f"workbench_session_card:{_safe_id(ref['id'])}",
                session_ref=ref,
                session_type="repl_session" if ref["type"] == "agent_repl_session" else "workbench_session",
                turn_count=len(source_view.repl_turn_refs),
                run_count=source_view.run_count,
                status="active" if source_view.source_status in {"complete", "partial"} else "unknown",
                summary_refs=source_view.evidence_refs,
                evidence_refs=[ref],
            )
            for ref in refs
        ]


class WorkbenchSessionTraceSummaryService:
    def build_trace_summaries(
        self, session_cards: list[WorkbenchSessionCard], source_view: WorkbenchRunDashboardSourceView
    ) -> list[WorkbenchSessionTraceSummary]:
        return [
            WorkbenchSessionTraceSummary(
                session_trace_summary_id=f"workbench_session_trace_summary:{_safe_id(card.session_card_id)}",
                session_ref=card.session_ref,
                trace_refs=source_view.trace_report_refs,
                stage_summary_refs=source_view.pipeline_run_refs,
                decision_summary_refs=source_view.approval_report_refs,
                route_summary_refs=source_view.pipeline_run_refs,
                provider_summary_refs=source_view.provider_report_refs,
                response_summary_refs=source_view.evidence_report_refs,
                summary_status="ready" if source_view.trace_report_refs else "partial",
                evidence_refs=source_view.trace_report_refs,
            )
            for card in session_cards
        ]


class WorkbenchSessionPIGGuidanceSummaryService:
    def build_pig_guidance_summaries(
        self, session_cards: list[WorkbenchSessionCard], source_view: WorkbenchRunDashboardSourceView
    ) -> list[WorkbenchSessionPIGGuidanceSummary]:
        return [
            WorkbenchSessionPIGGuidanceSummary(
                session_pig_guidance_summary_id=f"workbench_session_pig_guidance_summary:{_safe_id(card.session_card_id)}",
                session_ref=card.session_ref,
                pig_guidance_refs=source_view.pig_guidance_refs,
                recommendation_count=1 if source_view.pig_guidance_refs else 0,
                warning_count=0,
                candidate_count=0,
                rationale_count=0,
                pattern_summary_count=1 if len(source_view.pig_guidance_refs) > 1 else 0,
                evidence_refs=source_view.pig_guidance_refs,
            )
            for card in session_cards
        ]


class WorkbenchSessionPatternViewService:
    def build_decision_pattern_views(
        self, session_cards: list[WorkbenchSessionCard], source_view: WorkbenchRunDashboardSourceView
    ) -> list[WorkbenchSessionDecisionPatternView]:
        return [
            WorkbenchSessionDecisionPatternView(
                decision_pattern_view_id=f"workbench_session_decision_pattern_view:{_safe_id(card.session_card_id)}",
                session_ref=card.session_ref,
                decision_type="approval_status",
                occurrence_count=len(source_view.approval_report_refs),
                outcome_distribution={"recorded": len(source_view.approval_report_refs)},
                source_refs=source_view.approval_report_refs,
                evidence_refs=source_view.approval_report_refs,
            )
            for card in session_cards
        ]

    def build_route_pattern_views(
        self, session_cards: list[WorkbenchSessionCard], source_view: WorkbenchRunDashboardSourceView
    ) -> list[WorkbenchSessionRoutePatternView]:
        return [
            WorkbenchSessionRoutePatternView(
                route_pattern_view_id=f"workbench_session_route_pattern_view:{_safe_id(card.session_card_id)}",
                session_ref=card.session_ref,
                route_kind="workspace_agent_surface",
                occurrence_count=len(source_view.pipeline_run_refs),
                success_count=len(source_view.pipeline_run_refs),
                warning_count=0,
                failed_count=0,
                blocked_count=0,
                source_refs=source_view.pipeline_run_refs,
                evidence_refs=source_view.pipeline_run_refs,
            )
            for card in session_cards
        ]

    def build_provider_pattern_views(
        self, session_cards: list[WorkbenchSessionCard], source_view: WorkbenchRunDashboardSourceView
    ) -> list[WorkbenchSessionProviderPatternView]:
        return [
            WorkbenchSessionProviderPatternView(
                provider_pattern_view_id=f"workbench_session_provider_pattern_view:{_safe_id(card.session_card_id)}",
                session_ref=card.session_ref,
                provider_id="internal_provider_registry" if source_view.provider_report_refs else None,
                capability_id=None,
                occurrence_count=len(source_view.provider_report_refs),
                warning_count=0,
                failed_count=0,
                boundary_warning_count=0,
                source_refs=source_view.provider_report_refs,
                evidence_refs=source_view.provider_report_refs,
            )
            for card in session_cards
        ]

    def build_safety_pattern_views(
        self, session_cards: list[WorkbenchSessionCard], source_view: WorkbenchRunDashboardSourceView
    ) -> list[WorkbenchSessionSafetyPatternView]:
        return [
            WorkbenchSessionSafetyPatternView(
                safety_pattern_view_id=f"workbench_session_safety_pattern_view:{_safe_id(card.session_card_id)}",
                session_ref=card.session_ref,
                safety_outcome="allow_route" if source_view.approval_report_refs else "unknown",
                occurrence_count=len(source_view.approval_report_refs),
                repeated_warning=False,
                repeated_block=False,
                source_refs=source_view.approval_report_refs,
                evidence_refs=source_view.approval_report_refs,
            )
            for card in session_cards
        ]

    def build_failure_pattern_views(
        self, session_cards: list[WorkbenchSessionCard], failure_summary: WorkbenchFailureSummary
    ) -> list[WorkbenchSessionFailurePatternView]:
        if not session_cards:
            return failure_summary.repeated_failure_patterns
        return [
            WorkbenchSessionFailurePatternView(
                failure_pattern_view_id=f"workbench_session_failure_pattern_view:{_safe_id(card.session_card_id)}",
                session_ref=card.session_ref,
                failure_category=failure_summary.failure_rows[0]["failure_category"] if failure_summary.failure_rows else "none",
                occurrence_count=failure_summary.failure_count,
                affected_run_refs=card.summary_refs,
                recovery_guidance_refs=failure_summary.recovery_guidance_refs,
                evidence_refs=failure_summary.evidence_refs,
            )
            for card in session_cards
        ]


class WorkbenchSessionContextRefViewService:
    def build_context_ref_views(
        self, session_cards: list[WorkbenchSessionCard], source_view: WorkbenchRunDashboardSourceView
    ) -> list[WorkbenchSessionContextRefView]:
        return [
            WorkbenchSessionContextRefView(
                context_ref_view_id=f"workbench_session_context_ref_view:{_safe_id(card.session_card_id)}",
                session_ref=card.session_ref,
                context_kind="long_task_context_ref",
                context_refs=source_view.evidence_refs + source_view.pig_guidance_refs,
                context_summary="Refs-only long-task context summary for dashboard inspection.",
                evidence_refs=source_view.evidence_refs,
            )
            for card in session_cards
        ]


class WorkbenchSessionMonitorViewService:
    def build_session_monitor_view(
        self,
        panel_id: str | None,
        session_cards: list[WorkbenchSessionCard],
        trace_summaries: list[WorkbenchSessionTraceSummary],
        pig_summaries: list[WorkbenchSessionPIGGuidanceSummary],
        decision_patterns: list[WorkbenchSessionDecisionPatternView],
        route_patterns: list[WorkbenchSessionRoutePatternView],
        provider_patterns: list[WorkbenchSessionProviderPatternView],
        safety_patterns: list[WorkbenchSessionSafetyPatternView],
        failure_patterns: list[WorkbenchSessionFailurePatternView],
        context_views: list[WorkbenchSessionContextRefView],
    ) -> WorkbenchSessionMonitorView:
        status = "ready" if session_cards and trace_summaries and context_views else "partial"
        return WorkbenchSessionMonitorView(
            session_monitor_view_id="workbench_session_monitor_view:v0.26.6",
            panel_id=panel_id,
            session_cards=session_cards,
            session_trace_summaries=trace_summaries,
            pig_guidance_summaries=pig_summaries,
            decision_pattern_views=decision_patterns,
            route_pattern_views=route_patterns,
            provider_pattern_views=provider_patterns,
            safety_pattern_views=safety_patterns,
            failure_pattern_views=failure_patterns,
            context_ref_views=context_views,
            monitor_status=status,
            evidence_refs=[_model_ref("workbench_session_card", card, "session_card_id") for card in session_cards],
        )


class WorkbenchRunDashboardMetricSetService:
    def build_metric_set(
        self,
        source_view: WorkbenchRunDashboardSourceView,
        run_cards: list[WorkbenchRunCard],
        approval_summary: WorkbenchApprovalStatusSummary,
        provider_summary: WorkbenchProviderStatusSummary,
        response_summary: WorkbenchResponseStatusSummary,
        safety_summary: WorkbenchSafetyStatusSummary,
        route_patterns: list[WorkbenchSessionRoutePatternView],
        provider_patterns: list[WorkbenchSessionProviderPatternView],
        safety_patterns: list[WorkbenchSessionSafetyPatternView],
        failure_patterns: list[WorkbenchSessionFailurePatternView],
    ) -> WorkbenchRunDashboardMetricSet:
        return WorkbenchRunDashboardMetricSet(
            metric_set_id="workbench_run_dashboard_metric_set:v0.26.6",
            run_count=source_view.run_count,
            session_count=source_view.session_count,
            completed_run_count=sum(1 for card in run_cards if card.status == "completed"),
            warning_run_count=sum(1 for card in run_cards if card.status == "warning"),
            failed_run_count=sum(1 for card in run_cards if card.status == "failed"),
            blocked_run_count=sum(1 for card in run_cards if card.status == "blocked"),
            approval_candidate_count=approval_summary.approval_candidate_count,
            approval_decision_count=approval_summary.approval_decision_count,
            provider_invocation_count=provider_summary.provider_invocation_count,
            provider_failed_count=provider_summary.provider_failed_count,
            safety_block_count=safety_summary.blocked_count,
            unsupported_claim_count=response_summary.unsupported_claim_count,
            uncertainty_count=response_summary.uncertainty_note_count,
            limitation_count=response_summary.limitation_note_count,
            repeated_route_pattern_count=len(route_patterns),
            repeated_provider_pattern_count=len(provider_patterns),
            repeated_safety_pattern_count=len(safety_patterns),
            repeated_failure_pattern_count=len(failure_patterns),
            metric_status="ready" if run_cards else "partial",
            evidence_refs=source_view.evidence_refs,
        )


class WorkbenchRunDashboardViewService:
    def build_run_dashboard_view(
        self,
        panel_id: str | None,
        source_view: WorkbenchRunDashboardSourceView,
        run_cards: list[WorkbenchRunCard],
        pipeline_views: list[WorkbenchPipelineStatusView],
        provider_summary: WorkbenchProviderStatusSummary,
        response_summary: WorkbenchResponseStatusSummary,
        safety_summary: WorkbenchSafetyStatusSummary,
        approval_summary: WorkbenchApprovalStatusSummary,
        failure_summary: WorkbenchFailureSummary,
        warning_summary: WorkbenchWarningSummary,
        metric_set: WorkbenchRunDashboardMetricSet,
    ) -> WorkbenchRunDashboardView:
        status = "ready" if source_view.source_status == "complete" else "warning" if source_view.source_status == "partial" else "failed"
        return WorkbenchRunDashboardView(
            run_dashboard_view_id="workbench_run_dashboard_view:v0.26.6",
            panel_id=panel_id,
            source_view=source_view,
            run_cards=run_cards,
            pipeline_status_views=pipeline_views,
            provider_status_summary=provider_summary,
            response_status_summary=response_summary,
            safety_status_summary=safety_summary,
            approval_status_summary=approval_summary,
            failure_summary=failure_summary,
            warning_summary=warning_summary,
            metric_set=metric_set,
            view_status=status,
            evidence_refs=[_model_ref("workbench_run_card", card, "run_card_id") for card in run_cards],
        )


class WorkbenchRunDashboardFindingService:
    BLOCKED_FINDINGS = {
        "background_monitor_attempted",
        "continuous_watcher_attempted",
        "auto_refresh_execution_attempted",
        "rerun_attempted",
        "automatic_retry_attempted",
        "automatic_repair_attempted",
        "autonomous_optimization_attempted",
        "command_execution_attempted",
        "approval_execution_attempted",
        "provider_invocation_attempted",
        "ask_execution_attempted",
        "final_response_emission_attempted",
        "local_command_execution_attempted",
        "direct_file_access_attempted",
        "direct_subprocess_attempted",
        "memory_continuity_attempted",
        "memory_promotion_attempted",
        "persistent_memory_write_attempted",
        "persona_mutation_attempted",
        "pig_guidance_as_memory_detected",
        "pig_policy_mutation_detected",
        "pig_execution_detected",
        "external_adapter_detected",
        "vendor_adapter_detected",
        "schumpeter_split_detected",
        "credential_exposure_detected",
        "raw_secret_output_detected",
        "raw_provider_output_detected",
        "raw_transcript_persistence_detected",
        "llm_judge_detected",
    }

    def _finding(self, finding_type: str, severity: str, message: str, subject_ref: dict[str, Any] | None = None) -> WorkbenchRunDashboardFinding:
        return WorkbenchRunDashboardFinding(
            finding_id=f"workbench_run_dashboard_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            subject_ref=subject_ref,
            evidence_refs=[subject_ref] if subject_ref else [],
            withdrawal_condition="Withdraw if the source report, policy boundary, or dashboard/session monitor artifact changes.",
        )

    def build_findings(
        self,
        source_service: WorkbenchRunDashboardPrerequisiteSourceService,
        source_view: WorkbenchRunDashboardSourceView,
        run_cards: list[WorkbenchRunCard],
        pipeline_views: list[WorkbenchPipelineStatusView],
        session_view: WorkbenchSessionMonitorView,
        metric_set: WorkbenchRunDashboardMetricSet,
        strictness: str = "standard",
        attempt_flags: dict[str, bool] | None = None,
        extra_findings: list[str] | None = None,
    ) -> list[WorkbenchRunDashboardFinding]:
        findings: list[WorkbenchRunDashboardFinding] = []
        missing_sources = [
            ("missing_workbench_view_state", not source_service.view_state_available),
            ("missing_run_dashboard_panel", not source_service.run_dashboard_panel_available),
            ("missing_session_monitor_panel", not source_service.session_monitor_panel_available),
            ("missing_ask_repl_report", not source_view.ask_repl_report_refs),
            ("missing_pipeline_run", not source_view.pipeline_run_refs),
            ("missing_trace_telemetry_report", not source_view.trace_report_refs),
            ("missing_session_refs", not source_view.repl_session_refs),
        ]
        for finding_type, missing in missing_sources:
            if missing:
                severity = "error" if strictness == "strict" and finding_type in {"missing_workbench_view_state", "missing_run_dashboard_panel", "missing_session_monitor_panel"} else "warning"
                findings.append(self._finding(finding_type, severity, f"{finding_type} detected."))
        created = [
            ("run_dashboard_view_created", True),
            ("run_card_created", bool(run_cards)),
            ("pipeline_status_view_created", bool(pipeline_views)),
            ("provider_status_summary_created", True),
            ("response_status_summary_created", True),
            ("safety_status_summary_created", True),
            ("approval_status_summary_created", True),
            ("failure_summary_created", True),
            ("warning_summary_created", True),
            ("session_monitor_view_created", True),
            ("session_card_created", bool(session_view.session_cards)),
            ("session_trace_summary_created", bool(session_view.session_trace_summaries)),
            ("session_pig_guidance_summary_created", bool(session_view.pig_guidance_summaries)),
            ("decision_pattern_view_created", bool(session_view.decision_pattern_views)),
            ("route_pattern_view_created", bool(session_view.route_pattern_views)),
            ("provider_pattern_view_created", bool(session_view.provider_pattern_views)),
            ("safety_pattern_view_created", bool(session_view.safety_pattern_views)),
            ("failure_pattern_view_created", bool(session_view.failure_pattern_views)),
            ("session_context_ref_view_created", bool(session_view.context_ref_views)),
            ("run_dashboard_metric_set_created", metric_set.metric_status in {"ready", "partial"}),
        ]
        for finding_type, did_create in created:
            if did_create:
                findings.append(self._finding(finding_type, "info", f"{finding_type} completed."))
        for finding_type, attempted in (attempt_flags or {}).items():
            if attempted:
                severity = "critical" if finding_type in self.BLOCKED_FINDINGS else "warning"
                findings.append(self._finding(finding_type, severity, f"{finding_type} detected."))
        for finding_type in extra_findings or []:
            severity = "critical" if finding_type in self.BLOCKED_FINDINGS else "warning"
            findings.append(self._finding(finding_type, severity, f"{finding_type} detected."))
        if not findings:
            findings.append(self._finding("ok", "info", "Run dashboard/session monitor report is ready."))
        return findings


class WorkbenchRunDashboardReportService:
    def build_all_parts(
        self,
        *,
        report_id: str | None = None,
        strictness: str = "standard",
        attempt_flags: dict[str, bool] | None = None,
        extra_findings: list[str] | None = None,
        view_state_available: bool = True,
        run_dashboard_panel_available: bool = True,
        session_monitor_panel_available: bool = True,
        ask_repl_available: bool = True,
        trace_telemetry_available: bool = True,
        approval_console_available: bool = True,
        evidence_inspector_available: bool = True,
        provider_browser_available: bool = True,
        pig_guidance_available: bool = True,
    ) -> dict[str, Any]:
        source_service = WorkbenchRunDashboardPrerequisiteSourceService(
            view_state_available=view_state_available,
            run_dashboard_panel_available=run_dashboard_panel_available,
            session_monitor_panel_available=session_monitor_panel_available,
            ask_repl_available=ask_repl_available,
            trace_telemetry_available=trace_telemetry_available,
            approval_console_available=approval_console_available,
            evidence_inspector_available=evidence_inspector_available,
            provider_browser_available=provider_browser_available,
            pig_guidance_available=pig_guidance_available,
        )
        policy = WorkbenchRunDashboardPolicyService().build_policy()
        request = WorkbenchRunDashboardRequestService(source_service).build_request(strictness=strictness)
        source_view = WorkbenchRunDashboardSourceViewService(source_service).build_source_view()
        stage_summary = WorkbenchStageStatusSummaryService().build_stage_status_summary(source_view)
        pipeline_views = WorkbenchPipelineStatusViewService().build_pipeline_status_views(source_view, stage_summary)
        run_cards = WorkbenchRunCardService().build_run_cards(source_view, pipeline_views)
        provider_summary = WorkbenchProviderStatusSummaryService().build_provider_status_summary(source_view)
        response_summary = WorkbenchResponseStatusSummaryService().build_response_status_summary(source_view)
        safety_summary = WorkbenchSafetyStatusSummaryService().build_safety_status_summary(source_view)
        approval_summary = WorkbenchApprovalStatusSummaryService().build_approval_status_summary(source_view)
        session_cards = WorkbenchSessionCardService().build_session_cards(source_view)
        session_ref = session_cards[0].session_ref if session_cards else None
        failure_summary = WorkbenchFailureSummaryService().build_failure_summary(source_view, session_ref)
        warning_summary = WorkbenchWarningSummaryService().build_warning_summary(source_view)
        trace_summaries = WorkbenchSessionTraceSummaryService().build_trace_summaries(session_cards, source_view)
        pig_summaries = WorkbenchSessionPIGGuidanceSummaryService().build_pig_guidance_summaries(session_cards, source_view)
        pattern_service = WorkbenchSessionPatternViewService()
        decision_patterns = pattern_service.build_decision_pattern_views(session_cards, source_view)
        route_patterns = pattern_service.build_route_pattern_views(session_cards, source_view)
        provider_patterns = pattern_service.build_provider_pattern_views(session_cards, source_view)
        safety_patterns = pattern_service.build_safety_pattern_views(session_cards, source_view)
        failure_patterns = pattern_service.build_failure_pattern_views(session_cards, failure_summary)
        context_views = WorkbenchSessionContextRefViewService().build_context_ref_views(session_cards, source_view)
        metric_set = WorkbenchRunDashboardMetricSetService().build_metric_set(
            source_view,
            run_cards,
            approval_summary,
            provider_summary,
            response_summary,
            safety_summary,
            route_patterns,
            provider_patterns,
            safety_patterns,
            failure_patterns,
        )
        dashboard_view = WorkbenchRunDashboardViewService().build_run_dashboard_view(
            request.run_dashboard_panel_id,
            source_view,
            run_cards,
            pipeline_views,
            provider_summary,
            response_summary,
            safety_summary,
            approval_summary,
            failure_summary,
            warning_summary,
            metric_set,
        )
        session_policy = WorkbenchSessionMonitorPolicyService().build_policy()
        session_view = WorkbenchSessionMonitorViewService().build_session_monitor_view(
            request.session_monitor_panel_id,
            session_cards,
            trace_summaries,
            pig_summaries,
            decision_patterns,
            route_patterns,
            provider_patterns,
            safety_patterns,
            failure_patterns,
            context_views,
        )
        findings = WorkbenchRunDashboardFindingService().build_findings(
            source_service,
            source_view,
            run_cards,
            pipeline_views,
            session_view,
            metric_set,
            strictness=strictness,
            attempt_flags=attempt_flags,
            extra_findings=extra_findings,
        )
        status = self._report_status(findings)
        report = WorkbenchRunDashboardReport(
            report_id=report_id or "workbench_run_dashboard_report:v0.26.6",
            created_at=utc_now_iso(),
            dashboard_policy=policy,
            request=request,
            source_view=source_view,
            run_dashboard_view=dashboard_view,
            session_monitor_policy=session_policy,
            session_monitor_view=session_view,
            metric_set=metric_set,
            findings=findings,
            report_status=status,
            ready_for_v0_26_7=status in {"passed", "warning"},
            run_dashboard_view_created=dashboard_view.view_status in {"ready", "warning"},
            session_monitor_view_created=session_view.monitor_status in {"ready", "partial"},
            run_cards_created=bool(run_cards),
            pipeline_status_views_created=bool(pipeline_views),
            provider_status_summary_created=provider_summary is not None,
            response_status_summary_created=response_summary is not None,
            safety_status_summary_created=safety_summary is not None,
            approval_status_summary_created=approval_summary is not None,
            failure_summary_created=failure_summary is not None,
            warning_summary_created=warning_summary is not None,
            session_trace_summaries_created=bool(trace_summaries),
            session_pig_guidance_summaries_created=bool(pig_summaries),
            repeated_pattern_views_created=any([decision_patterns, route_patterns, provider_patterns, safety_patterns, failure_patterns]),
            session_context_ref_views_created=bool(context_views),
            metric_set_created=metric_set.metric_status in {"ready", "partial"},
            limitations=[
                "v0.26.6 creates refs-only dashboard and session monitor read models; it does not render a UI.",
                "Repeated pattern views are descriptive and do not trigger optimization, retry, or repair.",
            ],
            withdrawal_conditions=[
                "Withdraw if dashboard/session monitor starts background work, executes commands, invokes providers, reruns runs, repairs failures, promotes memory, persists raw transcripts, or uses an LLM judge.",
            ],
        )
        return {
            "report": report,
            "policy": policy,
            "request": request,
            "source_view": source_view,
            "run_dashboard_view": dashboard_view,
            "run_cards": run_cards,
            "pipeline_status_views": pipeline_views,
            "stage_status_summary": stage_summary,
            "provider_status_summary": provider_summary,
            "response_status_summary": response_summary,
            "safety_status_summary": safety_summary,
            "approval_status_summary": approval_summary,
            "failure_summary": failure_summary,
            "warning_summary": warning_summary,
            "session_monitor_policy": session_policy,
            "session_monitor_view": session_view,
            "session_cards": session_cards,
            "session_trace_summaries": trace_summaries,
            "pig_guidance_summaries": pig_summaries,
            "decision_pattern_views": decision_patterns,
            "route_pattern_views": route_patterns,
            "provider_pattern_views": provider_patterns,
            "safety_pattern_views": safety_patterns,
            "failure_pattern_views": failure_patterns,
            "context_ref_views": context_views,
            "metric_set": metric_set,
            "findings": findings,
        }

    def _report_status(self, findings: list[WorkbenchRunDashboardFinding]) -> str:
        severities = {finding.severity for finding in findings}
        if "critical" in severities:
            return "blocked"
        if "error" in severities:
            return "failed"
        if "warning" in severities:
            return "warning"
        return "passed"

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": WORKBENCH_RUN_DASHBOARD_VERSION,
            "layer": WORKBENCH_RUN_DASHBOARD_LAYER,
            "subject": "run_dashboard_session_monitor",
            "principles": [
                "Run Dashboard is not background execution",
                "Session Monitor is not memory continuity",
                "Session summary is not raw transcript storage",
                "Repeated pattern view is not autonomous optimization",
                "Failure summary is not automatic repair",
                "Run status card is not rerun button",
                "Approval status card is not approval execution",
                "Provider status card is not provider invocation",
                "PIG guidance summary is not memory or policy mutation",
                "Long-task context refs are not persistent memory",
            ],
            "safety_boundary": {
                "run_dashboard_view_created": "conditional",
                "session_monitor_view_created": "conditional",
                "run_cards_created": "conditional",
                "pipeline_status_views_created": "conditional",
                "status_summaries_created": "conditional",
                "session_pattern_views_created": "conditional",
                "actual_ui_rendered": False,
                "panel_rendered": False,
                "background_monitor_started": False,
                "continuous_watcher_started": False,
                "auto_refresh_execution_started": False,
                "rerun_performed": False,
                "automatic_retry_performed": False,
                "automatic_repair_performed": False,
                "autonomous_optimization_performed": False,
                "command_executed": False,
                "approval_executed": False,
                "provider_invoked": False,
                "ask_executed": False,
                "final_response_emitted": False,
                "local_command_executed": False,
                "memory_continuity_enabled": False,
                "memory_promoted": False,
                "persistent_memory_written": False,
                "persona_mutated": False,
                "external_provider_adapter_implemented": False,
                "vendor_adapter_implemented": False,
                "pig_memory_promoted": False,
                "pig_policy_mutated": False,
                "pig_executed": False,
                "schumpeter_split_introduced": False,
                "credential_exposed": False,
                "raw_secret_output": False,
                "raw_provider_output_inline": False,
                "raw_transcript_persisted": False,
                "llm_judge_enabled": False,
            },
            "future_direction": [
                "v0.26.7 workbench command surface",
                "v0.26.8 snapshot / OCEL export",
                "v0.26.9 workbench consolidation",
                "v0.27 memory candidate and continuity",
            ],
            "next_step": WORKBENCH_RUN_DASHBOARD_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "workbench_run_dashboard_session_monitor_created",
            "version": WORKBENCH_RUN_DASHBOARD_VERSION,
            "source_read_models": [
                "WorkbenchViewStateState",
                "WorkbenchApprovalConsoleViewState",
                "WorkbenchEvidenceInspectorViewState",
                "WorkbenchProviderBrowserViewState",
                "WorkbenchTraceExplorerViewState",
                "AgentAskReplReportState",
                "AgentPipelineRunState",
                "AgentTraceTelemetryState",
                "PigGuidanceState",
            ],
            "target_read_models": [
                "WorkbenchRunDashboardViewState",
                "WorkbenchRunCardState",
                "WorkbenchPipelineStatusViewState",
                "WorkbenchStatusSummaryState",
                "WorkbenchSessionMonitorViewState",
                "WorkbenchSessionTraceSummaryState",
                "WorkbenchSessionPatternViewState",
                "WorkbenchRunDashboardMetricState",
                "V026ReadinessState",
            ],
            "effect_types": WORKBENCH_RUN_DASHBOARD_EFFECT_TYPES,
        }


def _bool_text(value: bool) -> str:
    return str(value).lower()


def render_workbench_run_dashboard_cli(parts: dict[str, Any], section: str = "view") -> str:
    report: WorkbenchRunDashboardReport = parts["report"]
    common = [
        "Workbench Run Dashboard / Session Monitor",
        f"version={report.version}",
        f"layer={WORKBENCH_RUN_DASHBOARD_LAYER}",
        f"run_dashboard_view_created={_bool_text(report.run_dashboard_view_created)}",
        f"session_monitor_view_created={_bool_text(report.session_monitor_view_created)}",
        f"run_cards_created={_bool_text(report.run_cards_created)}",
        f"pipeline_status_views_created={_bool_text(report.pipeline_status_views_created)}",
        f"provider_status_summary_created={_bool_text(report.provider_status_summary_created)}",
        f"response_status_summary_created={_bool_text(report.response_status_summary_created)}",
        f"safety_status_summary_created={_bool_text(report.safety_status_summary_created)}",
        f"approval_status_summary_created={_bool_text(report.approval_status_summary_created)}",
        f"failure_summary_created={_bool_text(report.failure_summary_created)}",
        f"warning_summary_created={_bool_text(report.warning_summary_created)}",
        f"session_trace_summaries_created={_bool_text(report.session_trace_summaries_created)}",
        f"session_pig_guidance_summaries_created={_bool_text(report.session_pig_guidance_summaries_created)}",
        f"repeated_pattern_views_created={_bool_text(report.repeated_pattern_views_created)}",
        f"session_context_ref_views_created={_bool_text(report.session_context_ref_views_created)}",
        f"metric_set_created={_bool_text(report.metric_set_created)}",
        f"ready_for_v0_26_7={_bool_text(report.ready_for_v0_26_7)}",
        f"ready_for_v0_27={_bool_text(report.ready_for_v0_27)}",
        f"actual_ui_rendered={_bool_text(report.actual_ui_rendered)}",
        f"panel_rendered={_bool_text(report.panel_rendered)}",
        f"background_monitor_started={_bool_text(report.background_monitor_started)}",
        f"continuous_watcher_started={_bool_text(report.continuous_watcher_started)}",
        f"auto_refresh_execution_started={_bool_text(report.auto_refresh_execution_started)}",
        f"rerun_performed={_bool_text(report.rerun_performed)}",
        f"automatic_retry_performed={_bool_text(report.automatic_retry_performed)}",
        f"automatic_repair_performed={_bool_text(report.automatic_repair_performed)}",
        f"autonomous_optimization_performed={_bool_text(report.autonomous_optimization_performed)}",
        f"command_executed={_bool_text(report.command_executed)}",
        f"approval_executed={_bool_text(report.approval_executed)}",
        f"provider_invoked={_bool_text(report.provider_invoked)}",
        f"ask_executed={_bool_text(report.ask_executed)}",
        f"final_response_emitted={_bool_text(report.final_response_emitted)}",
        f"local_command_executed={_bool_text(report.local_command_executed)}",
        f"memory_continuity_enabled={_bool_text(report.memory_continuity_enabled)}",
        f"memory_promoted={_bool_text(report.memory_promoted)}",
        f"persistent_memory_written={_bool_text(report.persistent_memory_written)}",
        f"persona_mutated={_bool_text(report.persona_mutated)}",
        f"external_provider_adapter_implemented={_bool_text(report.external_provider_adapter_implemented)}",
        f"vendor_adapter_implemented={_bool_text(report.vendor_adapter_implemented)}",
        f"pig_memory_promoted={_bool_text(report.pig_memory_promoted)}",
        f"pig_policy_mutated={_bool_text(report.pig_policy_mutated)}",
        f"pig_executed={_bool_text(report.pig_executed)}",
        f"schumpeter_split_introduced={_bool_text(report.schumpeter_split_introduced)}",
        f"credential_exposed={_bool_text(report.credential_exposed)}",
        f"raw_secret_output={_bool_text(report.raw_secret_output)}",
        f"raw_provider_output_inline={_bool_text(report.raw_provider_output_inline)}",
        f"raw_transcript_persisted={_bool_text(report.raw_transcript_persisted)}",
        f"llm_judge_used={_bool_text(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    if section == "view":
        view: WorkbenchRunDashboardView = parts["run_dashboard_view"]
        common.extend([f"view_status={view.view_status}", f"run_card_count={len(view.run_cards)}"])
    elif section == "runs":
        common.append(f"run_card_count={len(parts['run_cards'])}")
    elif section == "pipeline-status":
        common.append(f"pipeline_status_view_count={len(parts['pipeline_status_views'])}")
    elif section == "providers":
        summary: WorkbenchProviderStatusSummary = parts["provider_status_summary"]
        common.extend(
            [
                f"provider_invocation_count={summary.provider_invocation_count}",
                f"direct_provider_invocation_count={summary.direct_provider_invocation_count}",
                f"provider_invocation_enabled_now={_bool_text(summary.provider_invocation_enabled_now)}",
            ]
        )
    elif section == "responses":
        summary = parts["response_status_summary"]
        common.extend(
            [
                f"response_assembly_count={summary.response_assembly_count}",
                f"response_rewrite_performed={_bool_text(summary.response_rewrite_performed)}",
            ]
        )
    elif section == "safety":
        summary = parts["safety_status_summary"]
        common.extend(
            [
                f"safety_gate_count={summary.safety_gate_count}",
                f"safety_policy_mutation_count={summary.safety_policy_mutation_count}",
            ]
        )
    elif section == "approvals":
        summary = parts["approval_status_summary"]
        common.extend(
            [
                f"approval_candidate_count={summary.approval_candidate_count}",
                f"approval_executed_count={summary.approval_executed_count}",
                f"auto_approval_count={summary.auto_approval_count}",
            ]
        )
    elif section == "failures":
        summary = parts["failure_summary"]
        common.extend(
            [
                f"failure_count={summary.failure_count}",
                f"automatic_repair_enabled={_bool_text(summary.automatic_repair_enabled)}",
                f"auto_retry_enabled={_bool_text(summary.auto_retry_enabled)}",
            ]
        )
    elif section == "warnings":
        common.append(f"warning_count={parts['warning_summary'].warning_count}")
    elif section == "metrics":
        metric: WorkbenchRunDashboardMetricSet = parts["metric_set"]
        common.extend(
            [
                f"run_count={metric.run_count}",
                f"session_count={metric.session_count}",
                f"metric_status={metric.metric_status}",
                f"direct_bypass_count={metric.direct_bypass_count}",
                f"command_rerun_count={metric.command_rerun_count}",
                f"automatic_repair_count={metric.automatic_repair_count}",
                f"autonomous_loop_count={metric.autonomous_loop_count}",
                f"memory_promotion_count={metric.memory_promotion_count}",
                f"raw_transcript_persistence_count={metric.raw_transcript_persistence_count}",
            ]
        )
    elif section == "report":
        common.extend([f"report_id={report.report_id}", f"report_status={report.report_status}", f"finding_count={len(report.findings)}"])
    elif section == "monitor":
        view: WorkbenchSessionMonitorView = parts["session_monitor_view"]
        common.extend([f"monitor_status={view.monitor_status}", f"session_card_count={len(view.session_cards)}"])
    elif section == "cards":
        common.append(f"session_card_count={len(parts['session_cards'])}")
    elif section == "trace-summary":
        common.append(f"session_trace_summary_count={len(parts['session_trace_summaries'])}")
    elif section == "pig-guidance":
        common.append(f"pig_guidance_summary_count={len(parts['pig_guidance_summaries'])}")
    elif section == "patterns":
        pattern_count = (
            len(parts["decision_pattern_views"])
            + len(parts["route_pattern_views"])
            + len(parts["provider_pattern_views"])
            + len(parts["safety_pattern_views"])
            + len(parts["failure_pattern_views"])
        )
        common.append(f"repeated_pattern_count={pattern_count}")
    elif section == "context-refs":
        common.append(f"context_ref_count={len(parts['context_ref_views'])}")
    return "\n".join(common)
