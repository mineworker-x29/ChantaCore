from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from chanta_core.agent_surface.trace_telemetry import (
    AGENT_TRACE_STAGE_IDS,
    AGENT_TRACE_TELEMETRY_VERSION,
    AgentDecisionTrace,
    AgentPipelineStageTrace,
    AgentProviderInvocationTraceView,
    AgentResponseEmissionTrace,
    AgentRouteTrace,
    AgentSurfaceTrace,
    AgentTraceTelemetryReportService,
    AgentTurnOCELProjection,
)
from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace_agent_workbench.view_state import (
    WorkbenchPanel,
    WorkbenchViewState,
    WorkbenchViewStateReportService,
)


WORKBENCH_TRACE_EXPLORER_VERSION = "v0.26.2"
WORKBENCH_TRACE_EXPLORER_VERSION_NAME = "Trace Explorer & Pipeline Timeline"
WORKBENCH_TRACE_EXPLORER_LAYER = "workspace_agent_workbench"
WORKBENCH_TRACE_EXPLORER_TRACK = "Workspace Agent Workbench"
WORKBENCH_TRACE_EXPLORER_NEXT_STEP = "v0.26.3 Provider / Capability Browser"

WORKBENCH_TRACE_EXPLORER_IMPLEMENTED_SKILL_IDS = [
    "skill:workbench_trace_explorer_view",
    "skill:workbench_pipeline_timeline_view",
]

WORKBENCH_TRACE_EXPLORER_FUTURE_SKILL_IDS = [
    "skill:workbench_provider_browser_view",
    "skill:workbench_evidence_inspector_view",
    "skill:workbench_safety_gate_view",
    "skill:workbench_approval_console_view",
    "skill:workbench_run_dashboard_view",
    "skill:workbench_session_monitor_view",
    "skill:workbench_command_surface_use",
    "skill:workbench_snapshot_create",
    "skill:workbench_ocel_export_create",
    "skill:workbench_consolidation_view",
]

WORKBENCH_TRACE_EXPLORER_OBJECT_TYPES = [
    "workbench_trace_explorer_policy",
    "workbench_trace_explorer_request",
    "workbench_trace_source_view",
    "workbench_trace_explorer_view",
    "workbench_pipeline_timeline_policy",
    "workbench_pipeline_timeline",
    "workbench_timeline_node",
    "workbench_stage_node",
    "workbench_decision_node",
    "workbench_route_node",
    "workbench_provider_node",
    "workbench_response_node",
    "workbench_relation_edge",
    "workbench_trace_filter_policy",
    "workbench_trace_filter",
    "workbench_trace_filter_state",
    "workbench_trace_selection_view",
    "workbench_trace_inspection_policy",
    "workbench_trace_inspection_summary",
    "workbench_trace_inspection_report",
    "workbench_trace_explorer_finding",
    "workbench_trace_explorer_report",
    "workbench_view_state",
    "agent_surface_trace",
    "agent_turn_ocel_projection",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

WORKBENCH_TRACE_EXPLORER_EVENT_TYPES = [
    "workbench_trace_explorer_requested",
    "workbench_trace_explorer_policy_created",
    "workbench_trace_source_view_created",
    "workbench_trace_explorer_view_created",
    "workbench_pipeline_timeline_policy_created",
    "workbench_pipeline_timeline_created",
    "workbench_timeline_node_created",
    "workbench_stage_node_created",
    "workbench_decision_node_created",
    "workbench_route_node_created",
    "workbench_provider_node_created",
    "workbench_response_node_created",
    "workbench_relation_edge_created",
    "workbench_trace_filter_policy_created",
    "workbench_trace_filter_state_created",
    "workbench_trace_selection_view_created",
    "workbench_trace_inspection_policy_created",
    "workbench_trace_inspection_summary_created",
    "workbench_trace_inspection_report_created",
    "workbench_trace_explorer_report_created",
    "workbench_trace_explorer_warning_created",
    "workbench_trace_explorer_blocked",
]

WORKBENCH_TRACE_EXPLORER_RELATION_TYPES = [
    "uses_workbench_view_state",
    "uses_trace_explorer_panel",
    "uses_pipeline_timeline_panel",
    "uses_agent_surface_trace",
    "uses_agent_turn_ocel_projection",
    "creates_trace_source_view",
    "creates_trace_explorer_view",
    "creates_pipeline_timeline",
    "creates_stage_node",
    "creates_decision_node",
    "creates_route_node",
    "creates_provider_node",
    "creates_response_node",
    "creates_relation_edge",
    "applies_trace_filter",
    "creates_trace_selection_view",
    "creates_trace_inspection_summary",
    "creates_trace_inspection_report",
    "prepares_provider_browser",
    "defers_provider_browser_to_v0_26_3",
    "defers_evidence_inspector_to_v0_26_4",
    "defers_approval_console_to_v0_26_5",
    "defers_run_dashboard_to_v0_26_6",
    "defers_command_surface_to_v0_26_7",
    "defers_snapshot_export_to_v0_26_8",
    "defers_memory_continuity_to_v0_27",
    "defers_external_provider_adapters_to_v0_29_plus",
    "defers_external_agent_dominion_to_v0_30_plus",
    "not_ui_rendered",
    "not_trace_mutated",
    "not_stage_rerun",
    "not_agent_ask_executed",
    "not_provider_invoked",
    "not_local_command_executed",
    "not_memory_promoted",
    "not_external_adapter_implemented",
    "prevents_credential_exposure",
    "blocks_raw_provider_output_inline",
    "blocks_raw_secret_output",
    "recorded_in_envelope",
]

WORKBENCH_TRACE_EXPLORER_EFFECT_TYPES = [
    "read_only_observation",
    "workbench_trace_view_created",
    "workbench_pipeline_timeline_created",
    "workbench_timeline_node_created",
    "workbench_trace_filter_created",
    "workbench_trace_inspection_created",
    "state_candidate_created",
]

WORKBENCH_TRACE_EXPLORER_FORBIDDEN_EFFECT_TYPES = [
    "workbench_ui_implemented",
    "workbench_panel_rendered",
    "workbench_provider_browser_created",
    "workbench_evidence_inspector_created",
    "workbench_approval_candidate_created",
    "workbench_run_dashboard_created",
    "workbench_command_executed",
    "workbench_snapshot_created",
    "workbench_ocel_export_created",
    "stage_rerun_performed",
    "route_rerun_performed",
    "agent_ask_executed",
    "agent_repl_started",
    "final_response_emitted",
    "provider_invoked",
    "internal_provider_invoked",
    "local_command_executed",
    "bounded_local_command_executed",
    "command_rerun_performed",
    "direct_file_access_performed",
    "direct_subprocess_called",
    "background_execution_started",
    "autonomous_loop_started",
    "memory_promoted",
    "persistent_memory_written",
    "persona_mutated",
    "external_provider_called",
    "external_agent_runtime_touched",
    "file_written",
    "file_edited",
    "file_deleted",
    "credential_exposed",
    "raw_secret_output",
    "raw_provider_output_inline",
    "raw_transcript_persisted",
    "schumpeter_split_introduced",
]

VALID_TIMELINE_NODE_TYPES = {"stage", "decision", "route", "provider", "response", "telemetry", "unknown"}
VALID_RELATION_TYPES = {
    "stage_to_stage",
    "stage_to_decision",
    "decision_to_route",
    "route_to_provider",
    "provider_to_response",
    "response_to_emission",
    "trace_to_telemetry",
    "unknown",
}
VALID_TRACE_FILTER_TYPES = {
    "stage_status",
    "stage_type",
    "decision_type",
    "outcome",
    "provider_related",
    "response_related",
    "warning_only",
    "failed_or_blocked",
    "unknown",
}


def _ref(ref_type: str, ref_id: str | None, version: str = WORKBENCH_TRACE_EXPLORER_VERSION) -> dict[str, Any]:
    return {"type": ref_type, "id": ref_id or "missing", "version": version}


@dataclass
class _Model:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class WorkbenchTraceExplorerPolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_TRACE_EXPLORER_VERSION
    layer: str = WORKBENCH_TRACE_EXPLORER_LAYER
    trace_explorer_enabled: bool = True
    pipeline_timeline_enabled: bool = True
    actual_ui_rendering_enabled: bool = False
    panel_rendering_enabled: bool = False
    stage_rerun_enabled: bool = False
    provider_invocation_enabled: bool = False
    ask_execution_enabled: bool = False
    response_emission_enabled: bool = False
    local_runtime_execution_enabled: bool = False
    memory_promotion_enabled: bool = False
    persistent_memory_write_enabled: bool = False
    persona_mutation_enabled: bool = False
    external_provider_adapter_enabled: bool = False
    external_agent_adapter_enabled: bool = False
    refs_only_by_default: bool = True
    raw_transcript_inline_forbidden: bool = True
    raw_provider_output_inline_forbidden: bool = True
    raw_secret_inline_forbidden: bool = True
    credential_inline_forbidden: bool = True
    private_path_sanitization_required: bool = True
    ocel_visible: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchTraceExplorerRequest(_Model):
    request_id: str
    view_state_report_id: str | None
    view_state_id: str | None
    trace_telemetry_report_id: str | None
    surface_trace_id: str | None
    ocel_projection_id: str | None
    focus_trace_ref: dict[str, Any] | None
    filter_refs: list[dict[str, Any]]
    version: str = WORKBENCH_TRACE_EXPLORER_VERSION
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"


@dataclass
class WorkbenchTraceSourceView(_Model):
    source_view_id: str
    source_trace_ref: dict[str, Any] | None
    source_projection_ref: dict[str, Any] | None
    stage_trace_refs: list[dict[str, Any]]
    decision_trace_refs: list[dict[str, Any]]
    route_trace_ref: dict[str, Any] | None
    provider_trace_ref: dict[str, Any] | None
    response_emission_trace_ref: dict[str, Any] | None
    source_status: str
    version: str = WORKBENCH_TRACE_EXPLORER_VERSION
    raw_transcript_included: bool = False
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False
    private_full_path_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchTraceExplorerView(_Model):
    trace_explorer_view_id: str
    panel_id: str | None
    source_view: WorkbenchTraceSourceView
    timeline_id: str
    active_filter_state_id: str | None
    active_selection_view_id: str | None
    inspection_summary_id: str | None
    view_status: str
    version: str = WORKBENCH_TRACE_EXPLORER_VERSION
    renders_ui_now: bool = False
    stage_rerun_enabled: bool = False
    provider_invocation_enabled: bool = False
    raw_transcript_included: bool = False
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchPipelineTimelinePolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_TRACE_EXPLORER_VERSION
    timeline_enabled: bool = True
    node_model_only: bool = True
    edge_model_only: bool = True
    stage_execution_forbidden: bool = True
    route_execution_forbidden: bool = True
    provider_invocation_forbidden: bool = True
    raw_transcript_inline_forbidden: bool = True
    raw_provider_output_inline_forbidden: bool = True
    ocel_visible: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchTimelineNode(_Model):
    node_id: str
    node_type: str
    title: str
    subtitle: str | None
    source_ref: dict[str, Any] | None
    status: str
    order_index: int
    timestamp: str | None
    duration_ms: int | None
    sanitized_summary: str | None
    evidence_refs: list[dict[str, Any]]
    version: str = WORKBENCH_TRACE_EXPLORER_VERSION
    executable: bool = False
    raw_content_included: bool = False


@dataclass
class WorkbenchRelationEdge(_Model):
    edge_id: str
    source_node_id: str
    target_node_id: str
    relation_type: str
    source_relation_ref: dict[str, Any] | None
    edge_status: str
    version: str = WORKBENCH_TRACE_EXPLORER_VERSION
    mutates_relation_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchPipelineTimeline(_Model):
    timeline_id: str
    source_trace_id: str | None
    nodes: list[dict[str, Any]]
    edges: list[WorkbenchRelationEdge]
    stage_node_count: int
    decision_node_count: int
    route_node_count: int
    provider_node_count: int
    response_node_count: int
    timeline_status: str
    version: str = WORKBENCH_TRACE_EXPLORER_VERSION
    executes_now: bool = False
    rerun_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchStageNode(_Model):
    stage_node_id: str
    stage_id: str
    stage_name: str
    source_stage_trace_ref: dict[str, Any] | None
    stage_status: str
    input_refs: list[dict[str, Any]]
    output_refs: list[dict[str, Any]]
    duration_ms: int | None
    version: str = WORKBENCH_TRACE_EXPLORER_VERSION
    direct_bypass_detected: bool = False
    rerun_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchDecisionNode(_Model):
    decision_node_id: str
    decision_type: str
    decision_outcome: str
    source_decision_trace_ref: dict[str, Any] | None
    confidence: str | None
    version: str = WORKBENCH_TRACE_EXPLORER_VERSION
    deterministic: bool = True
    llm_judge_used: bool = False
    changes_decision_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchRouteNode(_Model):
    route_node_id: str
    route_kind: str | None
    source_route_trace_ref: dict[str, Any] | None
    selected_provider_refs: list[dict[str, Any]]
    route_step_refs: list[dict[str, Any]]
    route_status: str
    provider_invocation_required: bool
    provider_invoked_via_v0255: bool
    version: str = WORKBENCH_TRACE_EXPLORER_VERSION
    invokes_provider_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchProviderNode(_Model):
    provider_node_id: str
    provider_trace_ref: dict[str, Any] | None
    provider_result_refs: list[dict[str, Any]]
    provider_invoked_via_v0255: bool
    local_command_executed_via_v024: bool
    version: str = WORKBENCH_TRACE_EXPLORER_VERSION
    direct_provider_invocation: bool = False
    direct_local_command_executed: bool = False
    raw_provider_output_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchResponseNode(_Model):
    response_node_id: str
    response_emission_trace_ref: dict[str, Any] | None
    assembled_response_ref: dict[str, Any] | None
    surface_emission_ref: dict[str, Any] | None
    response_assembled_via_v0256: bool
    final_response_emitted_via_v0257: bool
    version: str = WORKBENCH_TRACE_EXPLORER_VERSION
    emits_response_now: bool = False
    raw_secret_output: bool = False
    raw_provider_output_inline: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchTraceFilterPolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_TRACE_EXPLORER_VERSION
    filtering_enabled: bool = True
    filter_is_not_data_deletion: bool = True
    filter_is_not_access_control: bool = True
    raw_data_filter_dump_forbidden: bool = True
    ocel_visible: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchTraceFilter(_Model):
    filter_id: str
    filter_type: str
    label: str
    predicate_summary: str
    active: bool
    version: str = WORKBENCH_TRACE_EXPLORER_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchTraceFilterState(_Model):
    filter_state_id: str
    filters: list[WorkbenchTraceFilter]
    active_filter_count: int
    affected_node_ids: list[str]
    hidden_node_ids: list[str]
    filter_status: str
    version: str = WORKBENCH_TRACE_EXPLORER_VERSION
    data_deleted: bool = False
    access_policy_mutated: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchTraceSelectionView(_Model):
    selection_view_id: str
    selected_node_ids: list[str]
    selected_edge_ids: list[str]
    selected_source_refs: list[dict[str, Any]]
    selection_summary: str | None
    version: str = WORKBENCH_TRACE_EXPLORER_VERSION
    selection_is_approval: bool = False
    selection_executes_now: bool = False
    raw_content_included: bool = False
    raw_secret_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchTraceInspectionPolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_TRACE_EXPLORER_VERSION
    inspection_enabled: bool = True
    inspection_is_read_only: bool = True
    summarize_refs_allowed: bool = True
    raw_transcript_inline_forbidden: bool = True
    raw_provider_output_inline_forbidden: bool = True
    raw_secret_inline_forbidden: bool = True
    stage_rerun_forbidden: bool = True
    provider_invocation_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchTraceInspectionSummary(_Model):
    inspection_summary_id: str
    trace_explorer_view_id: str
    stage_summary: list[dict[str, Any]]
    decision_summary: list[dict[str, Any]]
    route_summary: dict[str, Any] | None
    provider_summary: dict[str, Any] | None
    response_summary: dict[str, Any] | None
    warning_summary: list[dict[str, Any]]
    failure_summary: list[dict[str, Any]]
    summary_status: str
    version: str = WORKBENCH_TRACE_EXPLORER_VERSION
    raw_content_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchTraceInspectionReport(_Model):
    inspection_report_id: str
    created_at: str
    trace_explorer_view_id: str
    timeline_id: str
    inspection_summary: WorkbenchTraceInspectionSummary
    inspection_status: str
    version: str = WORKBENCH_TRACE_EXPLORER_VERSION
    trace_mutated: bool = False
    stage_rerun_performed: bool = False
    provider_invoked: bool = False
    local_command_executed: bool = False
    raw_transcript_included: bool = False
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchTraceExplorerFinding(_Model):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class WorkbenchTraceExplorerReport(_Model):
    report_id: str
    created_at: str
    trace_explorer_policy: WorkbenchTraceExplorerPolicy
    request: WorkbenchTraceExplorerRequest
    source_view: WorkbenchTraceSourceView
    trace_explorer_view: WorkbenchTraceExplorerView
    timeline_policy: WorkbenchPipelineTimelinePolicy
    timeline: WorkbenchPipelineTimeline
    filter_policy: WorkbenchTraceFilterPolicy
    filter_state: WorkbenchTraceFilterState
    selection_view: WorkbenchTraceSelectionView
    inspection_policy: WorkbenchTraceInspectionPolicy
    inspection_report: WorkbenchTraceInspectionReport
    findings: list[WorkbenchTraceExplorerFinding]
    report_status: str
    ready_for_v0_26_3: bool
    trace_explorer_view_created: bool
    pipeline_timeline_created: bool
    stage_nodes_created: bool
    decision_nodes_created: bool
    relation_edges_created: bool
    version: str = WORKBENCH_TRACE_EXPLORER_VERSION
    ready_for_v0_27: bool = False
    actual_ui_rendered: bool = False
    panel_rendered: bool = False
    trace_mutated: bool = False
    stage_rerun_performed: bool = False
    route_rerun_performed: bool = False
    ask_executed: bool = False
    final_response_emitted: bool = False
    provider_invoked: bool = False
    local_command_executed: bool = False
    direct_provider_invocation: bool = False
    direct_file_access_performed: bool = False
    direct_subprocess_performed: bool = False
    command_rerun_performed: bool = False
    autonomous_loop_started: bool = False
    background_execution_started: bool = False
    memory_promoted: bool = False
    persistent_memory_written: bool = False
    persona_mutated: bool = False
    external_provider_adapter_implemented: bool = False
    external_agent_adapter_implemented: bool = False
    schumpeter_split_introduced: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    raw_provider_output_inline: bool = False
    raw_transcript_persisted: bool = False
    llm_judge_used: bool = False
    next_required_step: str = WORKBENCH_TRACE_EXPLORER_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.26.3 Provider / Capability Browser begins or trace explorer policy changes."


class WorkbenchTraceExplorerPrerequisiteSourceService:
    def __init__(
        self,
        view_state_available: bool = True,
        trace_available: bool = True,
        route_trace_available: bool = True,
        provider_trace_available: bool = True,
        response_trace_available: bool = True,
        stage_traces_available: bool = True,
        decision_traces_available: bool = True,
        ask_report_id: str | None = None,
        trace_id: str | None = None,
        report_id: str | None = None,
    ) -> None:
        self.view_state_available = view_state_available
        self.trace_available = trace_available
        self.route_trace_available = route_trace_available
        self.provider_trace_available = provider_trace_available
        self.response_trace_available = response_trace_available
        self.stage_traces_available = stage_traces_available
        self.decision_traces_available = decision_traces_available
        self.ask_report_id = ask_report_id
        self.trace_id = trace_id
        self.report_id = report_id
        self._view_state_parts: dict[str, Any] | None = None
        self._trace_parts: dict[str, Any] | None = None

    def load_workbench_view_state(self) -> WorkbenchViewState | None:
        if not self.view_state_available:
            return None
        return self._load_view_state_parts()["view_state"]

    def load_trace_explorer_panel_model(self) -> WorkbenchPanel | None:
        return self._find_panel("trace_explorer")

    def load_pipeline_timeline_panel_model(self) -> WorkbenchPanel | None:
        return self._find_panel("pipeline_timeline")

    def load_agent_surface_trace(self) -> AgentSurfaceTrace | None:
        if not self.trace_available:
            return None
        return self._load_trace_parts()["surface_trace"]

    def load_agent_turn_ocel_projection(self) -> AgentTurnOCELProjection | None:
        if not self.trace_available:
            return None
        return self._load_trace_parts()["ocel_projection"]

    def load_pipeline_stage_traces(self) -> list[AgentPipelineStageTrace]:
        surface_trace = self.load_agent_surface_trace()
        if not surface_trace or not self.stage_traces_available:
            return []
        return surface_trace.stage_traces

    def load_decision_traces(self) -> list[AgentDecisionTrace]:
        surface_trace = self.load_agent_surface_trace()
        if not surface_trace or not self.decision_traces_available:
            return []
        return surface_trace.decision_traces

    def load_route_trace_if_available(self) -> AgentRouteTrace | None:
        surface_trace = self.load_agent_surface_trace()
        if not surface_trace or not self.route_trace_available:
            return None
        return surface_trace.route_trace

    def load_provider_trace_if_available(self) -> AgentProviderInvocationTraceView | None:
        surface_trace = self.load_agent_surface_trace()
        if not surface_trace or not self.provider_trace_available:
            return None
        return surface_trace.provider_trace_view

    def load_response_emission_trace_if_available(self) -> AgentResponseEmissionTrace | None:
        surface_trace = self.load_agent_surface_trace()
        if not surface_trace or not self.response_trace_available:
            return None
        return surface_trace.response_emission_trace

    def load_trace_telemetry_report_if_available(self) -> Any | None:
        if not self.trace_available:
            return None
        return self._load_trace_parts()["report"]

    def load_sources(self) -> dict[str, Any]:
        return {
            "workbench_view_state": self.load_workbench_view_state(),
            "trace_explorer_panel_model": self.load_trace_explorer_panel_model(),
            "pipeline_timeline_panel_model": self.load_pipeline_timeline_panel_model(),
            "surface_trace": self.load_agent_surface_trace(),
            "ocel_projection": self.load_agent_turn_ocel_projection(),
            "stage_traces": self.load_pipeline_stage_traces(),
            "decision_traces": self.load_decision_traces(),
            "route_trace": self.load_route_trace_if_available(),
            "provider_trace": self.load_provider_trace_if_available(),
            "response_trace": self.load_response_emission_trace_if_available(),
            "trace_telemetry_report": self.load_trace_telemetry_report_if_available(),
        }

    def _load_view_state_parts(self) -> dict[str, Any]:
        if self._view_state_parts is None:
            self._view_state_parts = WorkbenchViewStateReportService().build_all_parts()
        return self._view_state_parts

    def _load_trace_parts(self) -> dict[str, Any]:
        if self._trace_parts is None:
            self._trace_parts = AgentTraceTelemetryReportService().build_all_parts(
                ask_report_id=self.ask_report_id,
                trace_id=self.trace_id,
                report_id=self.report_id,
            )
        return self._trace_parts

    def _find_panel(self, panel_type: str) -> WorkbenchPanel | None:
        view_state = self.load_workbench_view_state()
        if not view_state:
            return None
        for panel in view_state.panel_registry_view.panels:
            if panel.panel_type == panel_type:
                return panel
        return None


class WorkbenchTraceExplorerPolicyService:
    def build_policy(self) -> WorkbenchTraceExplorerPolicy:
        return WorkbenchTraceExplorerPolicy(
            policy_id="workbench_trace_explorer_policy:v0.26.2",
            evidence_refs=[_ref("workspace_agent_workbench_contract", "v0.26.0")],
        )


class WorkbenchTraceExplorerRequestService:
    def build_request(self, sources: dict[str, Any], strictness: str = "standard") -> WorkbenchTraceExplorerRequest:
        view_state = sources.get("workbench_view_state")
        report = sources.get("trace_telemetry_report")
        surface_trace = sources.get("surface_trace")
        projection = sources.get("ocel_projection")
        return WorkbenchTraceExplorerRequest(
            request_id="workbench_trace_explorer_request:v0.26.2",
            view_state_report_id="workbench_view_state_report:v0.26.1" if view_state else None,
            view_state_id=view_state.view_state_id if view_state else None,
            trace_telemetry_report_id=report.report_id if report else None,
            surface_trace_id=surface_trace.surface_trace_id if surface_trace else None,
            ocel_projection_id=projection.projection_id if projection else None,
            focus_trace_ref=_ref("agent_surface_trace", surface_trace.surface_trace_id, AGENT_TRACE_TELEMETRY_VERSION) if surface_trace else None,
            filter_refs=[_ref("workbench_trace_filter", "warning_only"), _ref("workbench_trace_filter", "failed_or_blocked")],
            source_refs=self._source_refs(sources),
            strictness=strictness,
        )

    def _source_refs(self, sources: dict[str, Any]) -> list[dict[str, Any]]:
        refs: list[dict[str, Any]] = []
        if sources.get("workbench_view_state"):
            refs.append(_ref("workbench_view_state", sources["workbench_view_state"].view_state_id, "v0.26.1"))
        if sources.get("trace_explorer_panel_model"):
            refs.append(_ref("workbench_panel", sources["trace_explorer_panel_model"].panel_id, "v0.26.1"))
        if sources.get("pipeline_timeline_panel_model"):
            refs.append(_ref("workbench_panel", sources["pipeline_timeline_panel_model"].panel_id, "v0.26.1"))
        if sources.get("surface_trace"):
            refs.append(_ref("agent_surface_trace", sources["surface_trace"].surface_trace_id, AGENT_TRACE_TELEMETRY_VERSION))
        return refs


class WorkbenchTraceSourceViewService:
    def build_source_view(self, sources: dict[str, Any]) -> WorkbenchTraceSourceView:
        surface_trace: AgentSurfaceTrace | None = sources.get("surface_trace")
        projection: AgentTurnOCELProjection | None = sources.get("ocel_projection")
        stage_traces: list[AgentPipelineStageTrace] = sources.get("stage_traces", [])
        decision_traces: list[AgentDecisionTrace] = sources.get("decision_traces", [])
        route_trace: AgentRouteTrace | None = sources.get("route_trace")
        provider_trace: AgentProviderInvocationTraceView | None = sources.get("provider_trace")
        response_trace: AgentResponseEmissionTrace | None = sources.get("response_trace")
        if not surface_trace:
            status = "blocked"
        elif not stage_traces or not decision_traces:
            status = "missing"
        elif not projection or not route_trace or not provider_trace or not response_trace:
            status = "partial"
        else:
            status = "complete"
        return WorkbenchTraceSourceView(
            source_view_id="workbench_trace_source_view:v0.26.2",
            source_trace_ref=_ref("agent_surface_trace", surface_trace.surface_trace_id, AGENT_TRACE_TELEMETRY_VERSION) if surface_trace else None,
            source_projection_ref=_ref("agent_turn_ocel_projection", projection.projection_id, AGENT_TRACE_TELEMETRY_VERSION) if projection else None,
            stage_trace_refs=[_ref("agent_pipeline_stage_trace", stage.stage_trace_id, AGENT_TRACE_TELEMETRY_VERSION) for stage in stage_traces],
            decision_trace_refs=[_ref("agent_decision_trace", decision.decision_trace_id, AGENT_TRACE_TELEMETRY_VERSION) for decision in decision_traces],
            route_trace_ref=_ref("agent_route_trace", route_trace.route_trace_id, AGENT_TRACE_TELEMETRY_VERSION) if route_trace else None,
            provider_trace_ref=_ref("agent_provider_invocation_trace_view", provider_trace.provider_trace_view_id, AGENT_TRACE_TELEMETRY_VERSION) if provider_trace else None,
            response_emission_trace_ref=_ref("agent_response_emission_trace", response_trace.emission_trace_id, AGENT_TRACE_TELEMETRY_VERSION) if response_trace else None,
            source_status=status,
            evidence_refs=[_ref("agent_trace_telemetry_version", AGENT_TRACE_TELEMETRY_VERSION)],
        )


class WorkbenchTimelineNodeService:
    def build_stage_nodes(self, stage_traces: list[AgentPipelineStageTrace]) -> list[WorkbenchStageNode]:
        return [
            WorkbenchStageNode(
                stage_node_id=f"workbench_stage_node:{stage.stage_id}",
                stage_id=stage.stage_id,
                stage_name=stage.stage_name,
                source_stage_trace_ref=_ref("agent_pipeline_stage_trace", stage.stage_trace_id, AGENT_TRACE_TELEMETRY_VERSION),
                stage_status=stage.stage_status,
                input_refs=stage.input_refs,
                output_refs=stage.output_refs,
                duration_ms=stage.duration_ms,
                direct_bypass_detected=stage.direct_bypass_detected,
                evidence_refs=[_ref("agent_pipeline_stage_trace", stage.stage_trace_id, AGENT_TRACE_TELEMETRY_VERSION)],
            )
            for stage in stage_traces
        ]

    def build_decision_nodes(self, decision_traces: list[AgentDecisionTrace]) -> list[WorkbenchDecisionNode]:
        return [
            WorkbenchDecisionNode(
                decision_node_id=f"workbench_decision_node:{decision.decision_type}",
                decision_type=decision.decision_type,
                decision_outcome=decision.decision_outcome,
                source_decision_trace_ref=_ref("agent_decision_trace", decision.decision_trace_id, AGENT_TRACE_TELEMETRY_VERSION),
                confidence=decision.decision_confidence,
                deterministic=decision.deterministic,
                llm_judge_used=decision.llm_judge_used,
                evidence_refs=[_ref("agent_decision_trace", decision.decision_trace_id, AGENT_TRACE_TELEMETRY_VERSION)],
            )
            for decision in decision_traces
        ]

    def build_route_nodes(self, route_trace: AgentRouteTrace | None) -> list[WorkbenchRouteNode]:
        if not route_trace:
            return []
        return [
            WorkbenchRouteNode(
                route_node_id="workbench_route_node:route_trace",
                route_kind=route_trace.route_kind,
                source_route_trace_ref=_ref("agent_route_trace", route_trace.route_trace_id, AGENT_TRACE_TELEMETRY_VERSION),
                selected_provider_refs=route_trace.selected_provider_refs,
                route_step_refs=route_trace.route_step_refs,
                route_status=route_trace.route_status,
                provider_invocation_required=route_trace.provider_invocation_required,
                provider_invoked_via_v0255=route_trace.provider_invoked_via_v0255,
                evidence_refs=[_ref("agent_route_trace", route_trace.route_trace_id, AGENT_TRACE_TELEMETRY_VERSION)],
            )
        ]

    def build_provider_nodes(self, provider_trace: AgentProviderInvocationTraceView | None) -> list[WorkbenchProviderNode]:
        if not provider_trace:
            return []
        return [
            WorkbenchProviderNode(
                provider_node_id="workbench_provider_node:provider_trace",
                provider_trace_ref=_ref("agent_provider_invocation_trace_view", provider_trace.provider_trace_view_id, AGENT_TRACE_TELEMETRY_VERSION),
                provider_result_refs=provider_trace.provider_result_refs,
                provider_invoked_via_v0255=provider_trace.provider_invoked_via_v0255,
                local_command_executed_via_v024=provider_trace.local_command_executed_via_v024,
                direct_provider_invocation=provider_trace.direct_provider_invocation,
                direct_local_command_executed=provider_trace.direct_local_command_executed,
                raw_provider_output_included=False,
                evidence_refs=[_ref("agent_provider_invocation_trace_view", provider_trace.provider_trace_view_id, AGENT_TRACE_TELEMETRY_VERSION)],
            )
        ]

    def build_response_nodes(self, response_trace: AgentResponseEmissionTrace | None) -> list[WorkbenchResponseNode]:
        if not response_trace:
            return []
        return [
            WorkbenchResponseNode(
                response_node_id="workbench_response_node:response_trace",
                response_emission_trace_ref=_ref("agent_response_emission_trace", response_trace.emission_trace_id, AGENT_TRACE_TELEMETRY_VERSION),
                assembled_response_ref=response_trace.assembled_response_ref,
                surface_emission_ref=response_trace.surface_emission_ref,
                response_assembled_via_v0256=response_trace.response_assembled_via_v0256,
                final_response_emitted_via_v0257=response_trace.final_response_emitted_via_v0257,
                raw_secret_output=False,
                raw_provider_output_inline=False,
                evidence_refs=[_ref("agent_response_emission_trace", response_trace.emission_trace_id, AGENT_TRACE_TELEMETRY_VERSION)],
            )
        ]

    def build_timeline_nodes(
        self,
        stage_nodes: list[WorkbenchStageNode],
        decision_nodes: list[WorkbenchDecisionNode],
        route_nodes: list[WorkbenchRouteNode],
        provider_nodes: list[WorkbenchProviderNode],
        response_nodes: list[WorkbenchResponseNode],
    ) -> list[WorkbenchTimelineNode]:
        nodes: list[WorkbenchTimelineNode] = []
        order = 0
        for stage in stage_nodes:
            nodes.append(
                WorkbenchTimelineNode(
                    node_id=stage.stage_node_id,
                    node_type="stage",
                    title=stage.stage_name,
                    subtitle=stage.stage_id,
                    source_ref=stage.source_stage_trace_ref,
                    status=stage.stage_status,
                    order_index=order,
                    timestamp=None,
                    duration_ms=stage.duration_ms,
                    sanitized_summary=f"Stage {stage.stage_name} status={stage.stage_status}",
                    evidence_refs=stage.evidence_refs,
                )
            )
            order += 1
        for decision in decision_nodes:
            nodes.append(
                WorkbenchTimelineNode(
                    node_id=decision.decision_node_id,
                    node_type="decision",
                    title=decision.decision_type,
                    subtitle=decision.decision_outcome,
                    source_ref=decision.source_decision_trace_ref,
                    status="completed" if decision.decision_outcome != "missing" else "missing",
                    order_index=order,
                    timestamp=None,
                    duration_ms=None,
                    sanitized_summary=f"Decision {decision.decision_type} outcome={decision.decision_outcome}",
                    evidence_refs=decision.evidence_refs,
                )
            )
            order += 1
        for route in route_nodes:
            nodes.append(
                WorkbenchTimelineNode(
                    node_id=route.route_node_id,
                    node_type="route",
                    title="Route trace",
                    subtitle=route.route_kind,
                    source_ref=route.source_route_trace_ref,
                    status=route.route_status,
                    order_index=order,
                    timestamp=None,
                    duration_ms=None,
                    sanitized_summary=f"Route status={route.route_status}",
                    evidence_refs=route.evidence_refs,
                )
            )
            order += 1
        for provider in provider_nodes:
            nodes.append(
                WorkbenchTimelineNode(
                    node_id=provider.provider_node_id,
                    node_type="provider",
                    title="Provider trace view",
                    subtitle="prior v0.25.5 invocation trace" if provider.provider_invoked_via_v0255 else "no provider invocation trace",
                    source_ref=provider.provider_trace_ref,
                    status="completed" if provider.provider_invoked_via_v0255 else "skipped",
                    order_index=order,
                    timestamp=None,
                    duration_ms=None,
                    sanitized_summary="Provider node is refs-only and never invokes a provider.",
                    evidence_refs=provider.evidence_refs,
                )
            )
            order += 1
        for response in response_nodes:
            nodes.append(
                WorkbenchTimelineNode(
                    node_id=response.response_node_id,
                    node_type="response",
                    title="Response trace view",
                    subtitle="prior v0.25.6/v0.25.7 response artifact",
                    source_ref=response.response_emission_trace_ref,
                    status="completed" if response.final_response_emitted_via_v0257 else "missing",
                    order_index=order,
                    timestamp=None,
                    duration_ms=None,
                    sanitized_summary="Response node is a trace view and does not emit a response.",
                    evidence_refs=response.evidence_refs,
                )
            )
        return nodes


class WorkbenchRelationEdgeService:
    def build_edges(self, nodes: list[WorkbenchTimelineNode]) -> list[WorkbenchRelationEdge]:
        edges: list[WorkbenchRelationEdge] = []
        for index, (source, target) in enumerate(zip(nodes, nodes[1:]), start=1):
            relation_type = self._relation_type(source.node_type, target.node_type)
            edges.append(
                WorkbenchRelationEdge(
                    edge_id=f"workbench_relation_edge:{index}",
                    source_node_id=source.node_id,
                    target_node_id=target.node_id,
                    relation_type=relation_type,
                    source_relation_ref=None,
                    edge_status="inferred",
                    evidence_refs=[source.source_ref, target.source_ref],
                )
            )
        return edges

    def _relation_type(self, source_type: str, target_type: str) -> str:
        if source_type == "stage" and target_type == "stage":
            return "stage_to_stage"
        if source_type == "stage" and target_type == "decision":
            return "stage_to_decision"
        if source_type == "decision" and target_type == "route":
            return "decision_to_route"
        if source_type == "route" and target_type == "provider":
            return "route_to_provider"
        if source_type == "provider" and target_type == "response":
            return "provider_to_response"
        if target_type == "response":
            return "response_to_emission"
        return "unknown"


class WorkbenchPipelineTimelinePolicyService:
    def build_policy(self) -> WorkbenchPipelineTimelinePolicy:
        return WorkbenchPipelineTimelinePolicy(policy_id="workbench_pipeline_timeline_policy:v0.26.2")


class WorkbenchPipelineTimelineService:
    def build_timeline(
        self,
        source_view: WorkbenchTraceSourceView,
        nodes: list[WorkbenchTimelineNode],
        edges: list[WorkbenchRelationEdge],
    ) -> WorkbenchPipelineTimeline:
        stage_count = sum(1 for node in nodes if node.node_type == "stage")
        decision_count = sum(1 for node in nodes if node.node_type == "decision")
        if source_view.source_status == "blocked":
            status = "blocked"
        elif not nodes:
            status = "failed"
        elif stage_count == 0 or decision_count == 0:
            status = "warning"
        elif source_view.source_status in {"partial", "missing"}:
            status = "partial"
        else:
            status = "ready"
        return WorkbenchPipelineTimeline(
            timeline_id="workbench_pipeline_timeline:v0.26.2",
            source_trace_id=source_view.source_trace_ref["id"] if source_view.source_trace_ref else None,
            nodes=[node.to_dict() for node in nodes],
            edges=edges,
            stage_node_count=stage_count,
            decision_node_count=decision_count,
            route_node_count=sum(1 for node in nodes if node.node_type == "route"),
            provider_node_count=sum(1 for node in nodes if node.node_type == "provider"),
            response_node_count=sum(1 for node in nodes if node.node_type == "response"),
            timeline_status=status,
            evidence_refs=[_ref("workbench_trace_source_view", source_view.source_view_id)],
        )


class WorkbenchTraceFilterPolicyService:
    def build_policy(self) -> WorkbenchTraceFilterPolicy:
        return WorkbenchTraceFilterPolicy(policy_id="workbench_trace_filter_policy:v0.26.2")


class WorkbenchTraceFilterService:
    def build_default_filters(self) -> list[WorkbenchTraceFilter]:
        specs = [
            ("stage_status", "Stage status", "Match nodes by stage status.", False),
            ("stage_type", "Stage type", "Match nodes by pipeline stage type.", False),
            ("decision_type", "Decision type", "Match nodes by decision type.", False),
            ("outcome", "Outcome", "Match nodes by sanitized outcome labels.", False),
            ("provider_related", "Provider related", "Emphasize provider-related refs.", False),
            ("response_related", "Response related", "Emphasize response-related refs.", False),
            ("warning_only", "Warnings", "Emphasize warning nodes without deleting hidden data.", False),
            ("failed_or_blocked", "Failed or blocked", "Emphasize failed or blocked nodes without deleting hidden data.", False),
        ]
        return [
            WorkbenchTraceFilter(
                filter_id=f"workbench_trace_filter:{filter_type}",
                filter_type=filter_type,
                label=label,
                predicate_summary=predicate,
                active=active,
            )
            for filter_type, label, predicate, active in specs
        ]


class WorkbenchTraceFilterStateService:
    def build_filter_state(self, filters: list[WorkbenchTraceFilter], timeline: WorkbenchPipelineTimeline) -> WorkbenchTraceFilterState:
        active_filters = [item for item in filters if item.active]
        affected_node_ids = [node["node_id"] for node in timeline.nodes] if active_filters else []
        return WorkbenchTraceFilterState(
            filter_state_id="workbench_trace_filter_state:v0.26.2",
            filters=filters,
            active_filter_count=len(active_filters),
            affected_node_ids=affected_node_ids,
            hidden_node_ids=[],
            filter_status="ready" if filters else "empty",
            evidence_refs=[_ref("workbench_pipeline_timeline", timeline.timeline_id)],
        )


class WorkbenchTraceSelectionViewService:
    def build_selection_view(self, timeline: WorkbenchPipelineTimeline) -> WorkbenchTraceSelectionView:
        first_node = timeline.nodes[0] if timeline.nodes else None
        selected_node_ids = [first_node["node_id"]] if first_node else []
        selected_source_refs = [first_node["source_ref"]] if first_node and first_node.get("source_ref") else []
        return WorkbenchTraceSelectionView(
            selection_view_id="workbench_trace_selection_view:v0.26.2",
            selected_node_ids=selected_node_ids,
            selected_edge_ids=[],
            selected_source_refs=selected_source_refs,
            selection_summary="First timeline node selected by default." if first_node else None,
            evidence_refs=[_ref("workbench_pipeline_timeline", timeline.timeline_id)],
        )


class WorkbenchTraceInspectionPolicyService:
    def build_policy(self) -> WorkbenchTraceInspectionPolicy:
        return WorkbenchTraceInspectionPolicy(policy_id="workbench_trace_inspection_policy:v0.26.2")


class WorkbenchTraceInspectionSummaryService:
    def build_summary(
        self,
        trace_explorer_view_id: str,
        stage_nodes: list[WorkbenchStageNode],
        decision_nodes: list[WorkbenchDecisionNode],
        route_nodes: list[WorkbenchRouteNode],
        provider_nodes: list[WorkbenchProviderNode],
        response_nodes: list[WorkbenchResponseNode],
    ) -> WorkbenchTraceInspectionSummary:
        warning_summary = [
            {"node_ref": _ref("workbench_stage_node", stage.stage_node_id), "status": stage.stage_status}
            for stage in stage_nodes
            if stage.stage_status in {"warning", "missing", "blocked"}
        ]
        failure_summary = [
            {"node_ref": _ref("workbench_stage_node", stage.stage_node_id), "status": stage.stage_status}
            for stage in stage_nodes
            if stage.stage_status == "failed"
        ]
        status = "partial" if warning_summary else "ready"
        return WorkbenchTraceInspectionSummary(
            inspection_summary_id="workbench_trace_inspection_summary:v0.26.2",
            trace_explorer_view_id=trace_explorer_view_id,
            stage_summary=[
                {
                    "stage_node_ref": _ref("workbench_stage_node", stage.stage_node_id),
                    "stage_id": stage.stage_id,
                    "stage_status": stage.stage_status,
                }
                for stage in stage_nodes
            ],
            decision_summary=[
                {
                    "decision_node_ref": _ref("workbench_decision_node", decision.decision_node_id),
                    "decision_type": decision.decision_type,
                    "decision_outcome": decision.decision_outcome,
                }
                for decision in decision_nodes
            ],
            route_summary={"route_node_ref": _ref("workbench_route_node", route_nodes[0].route_node_id), "route_status": route_nodes[0].route_status} if route_nodes else None,
            provider_summary={"provider_node_ref": _ref("workbench_provider_node", provider_nodes[0].provider_node_id), "provider_invoked_via_v0255": provider_nodes[0].provider_invoked_via_v0255} if provider_nodes else None,
            response_summary={"response_node_ref": _ref("workbench_response_node", response_nodes[0].response_node_id), "final_response_emitted_via_v0257": response_nodes[0].final_response_emitted_via_v0257} if response_nodes else None,
            warning_summary=warning_summary,
            failure_summary=failure_summary,
            summary_status=status,
        )


class WorkbenchTraceInspectionReportService:
    def build_report(
        self,
        trace_explorer_view: WorkbenchTraceExplorerView,
        timeline: WorkbenchPipelineTimeline,
        inspection_summary: WorkbenchTraceInspectionSummary,
    ) -> WorkbenchTraceInspectionReport:
        if trace_explorer_view.view_status == "blocked":
            status = "blocked"
        elif inspection_summary.summary_status == "partial":
            status = "partial"
        else:
            status = "ready"
        return WorkbenchTraceInspectionReport(
            inspection_report_id="workbench_trace_inspection_report:v0.26.2",
            created_at=utc_now_iso(),
            trace_explorer_view_id=trace_explorer_view.trace_explorer_view_id,
            timeline_id=timeline.timeline_id,
            inspection_summary=inspection_summary,
            inspection_status=status,
            evidence_refs=[_ref("workbench_trace_explorer_view", trace_explorer_view.trace_explorer_view_id)],
        )


class WorkbenchTraceExplorerViewService:
    def build_view(
        self,
        panel: WorkbenchPanel | None,
        source_view: WorkbenchTraceSourceView,
        timeline: WorkbenchPipelineTimeline,
        filter_state: WorkbenchTraceFilterState,
        selection_view: WorkbenchTraceSelectionView,
    ) -> WorkbenchTraceExplorerView:
        if source_view.source_status == "blocked" or timeline.timeline_status == "blocked":
            status = "blocked"
        elif timeline.timeline_status == "failed":
            status = "failed"
        elif source_view.source_status in {"partial", "missing"} or timeline.timeline_status in {"partial", "warning"}:
            status = "partial"
        else:
            status = "ready"
        return WorkbenchTraceExplorerView(
            trace_explorer_view_id="workbench_trace_explorer_view:v0.26.2",
            panel_id=panel.panel_id if panel else None,
            source_view=source_view,
            timeline_id=timeline.timeline_id,
            active_filter_state_id=filter_state.filter_state_id,
            active_selection_view_id=selection_view.selection_view_id,
            inspection_summary_id="workbench_trace_inspection_summary:v0.26.2",
            view_status=status,
            evidence_refs=[_ref("workbench_panel", panel.panel_id, "v0.26.1")] if panel else [],
        )


class WorkbenchTraceExplorerFindingService:
    BLOCKED_FINDINGS = {
        "raw_transcript_inline_attempted",
        "raw_provider_output_inline_attempted",
        "raw_secret_inline_attempted",
        "trace_mutation_attempted",
        "stage_rerun_attempted",
        "route_rerun_attempted",
        "provider_invocation_attempted",
        "ask_execution_attempted",
        "final_response_emission_attempted",
        "local_command_execution_attempted",
        "direct_file_access_attempted",
        "direct_subprocess_attempted",
        "memory_promotion_attempted",
        "persona_mutation_attempted",
        "external_adapter_detected",
        "schumpeter_split_detected",
        "opencode_runtime_dependency_detected",
        "openclaw_runtime_dependency_detected",
        "hermes_runtime_dependency_detected",
        "credential_exposure_detected",
        "raw_secret_output_detected",
        "raw_provider_output_detected",
        "raw_transcript_persistence_detected",
        "llm_judge_detected",
    }

    def build_findings(
        self,
        sources: dict[str, Any],
        source_view: WorkbenchTraceSourceView,
        timeline: WorkbenchPipelineTimeline,
        inspection_report: WorkbenchTraceInspectionReport,
        attempt_flags: dict[str, bool] | None = None,
        extra_findings: list[str] | None = None,
    ) -> list[WorkbenchTraceExplorerFinding]:
        findings: list[WorkbenchTraceExplorerFinding] = []
        if not sources.get("workbench_view_state"):
            findings.append(self._finding("critical", "missing_workbench_view_state", "Workbench view state is unavailable."))
        if not sources.get("trace_explorer_panel_model"):
            findings.append(self._finding("critical", "missing_trace_explorer_panel", "Trace explorer panel model is unavailable."))
        if not sources.get("pipeline_timeline_panel_model"):
            findings.append(self._finding("critical", "missing_pipeline_timeline_panel", "Pipeline timeline panel model is unavailable."))
        if not sources.get("surface_trace"):
            findings.append(self._finding("critical", "missing_surface_trace", "Agent surface trace is unavailable."))
        if not sources.get("ocel_projection"):
            findings.append(self._finding("warning", "missing_ocel_projection", "Agent turn OCEL projection is unavailable."))
        if not sources.get("stage_traces"):
            findings.append(self._finding("critical", "missing_stage_trace", "Pipeline stage trace refs are unavailable."))
        if not sources.get("decision_traces"):
            findings.append(self._finding("critical", "missing_decision_trace", "Decision trace refs are unavailable."))
        if not sources.get("route_trace"):
            findings.append(self._finding("warning", "missing_route_trace", "Route trace is unavailable."))
        if not sources.get("provider_trace"):
            findings.append(self._finding("warning", "missing_provider_trace", "Provider trace view is unavailable."))
        if not sources.get("response_trace"):
            findings.append(self._finding("warning", "missing_response_trace", "Response emission trace is unavailable."))
        if source_view.source_status == "partial" or timeline.timeline_status == "partial" or inspection_report.inspection_status == "partial":
            findings.append(self._finding("warning", "partial_trace_source", "Trace source is partial and represented without fabricated data."))
        if timeline.stage_node_count > 0:
            findings.append(self._finding("info", "timeline_node_created", "Timeline node models were created."))
        if timeline.decision_node_count > 0:
            findings.append(self._finding("info", "pipeline_timeline_created", "Pipeline timeline was created."))
        if timeline.edges:
            findings.append(self._finding("info", "relation_edge_created", "Relation edge models were created."))
        findings.extend(
            [
                self._finding("info", "trace_explorer_view_created", "Trace explorer view artifact was created."),
                self._finding("info", "filter_state_created", "Trace filter state was created."),
                self._finding("info", "selection_view_created", "Trace selection view was created."),
                self._finding("info", "inspection_summary_created", "Trace inspection summary was created."),
            ]
        )
        for finding_type, active in (attempt_flags or {}).items():
            if active:
                normalized = finding_type if finding_type in self.BLOCKED_FINDINGS else f"{finding_type}_detected"
                findings.append(self._finding("critical", normalized, f"{normalized} was detected."))
        for finding_type in extra_findings or []:
            severity = "critical" if finding_type in self.BLOCKED_FINDINGS else "warning"
            findings.append(self._finding(severity, finding_type, f"{finding_type} was reported."))
        return findings

    def _finding(self, severity: str, finding_type: str, message: str) -> WorkbenchTraceExplorerFinding:
        return WorkbenchTraceExplorerFinding(
            finding_id=f"workbench_trace_explorer_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            subject_ref={"id": "workbench_trace_explorer"},
            evidence_refs=[],
            withdrawal_condition="Withdraw if v0.26.2 renders UI, mutates traces, reruns stages/routes, executes ask/repl, invokes providers, emits responses, executes commands, promotes memory, exposes raw data, or uses an LLM judge.",
        )


class WorkbenchTraceExplorerReportService:
    def build_report(self, **kwargs: Any) -> WorkbenchTraceExplorerReport:
        return self.build_all_parts(**kwargs)["report"]

    def build_all_parts(self, **kwargs: Any) -> dict[str, Any]:
        source_service = WorkbenchTraceExplorerPrerequisiteSourceService(
            view_state_available=kwargs.get("view_state_available", True),
            trace_available=kwargs.get("trace_available", True),
            route_trace_available=kwargs.get("route_trace_available", True),
            provider_trace_available=kwargs.get("provider_trace_available", True),
            response_trace_available=kwargs.get("response_trace_available", True),
            stage_traces_available=kwargs.get("stage_traces_available", True),
            decision_traces_available=kwargs.get("decision_traces_available", True),
            ask_report_id=kwargs.get("ask_report_id"),
            trace_id=kwargs.get("trace_id"),
            report_id=kwargs.get("report_id"),
        )
        sources = source_service.load_sources()
        policy = WorkbenchTraceExplorerPolicyService().build_policy()
        request = WorkbenchTraceExplorerRequestService().build_request(sources, kwargs.get("strictness", "standard"))
        source_view = WorkbenchTraceSourceViewService().build_source_view(sources)
        node_service = WorkbenchTimelineNodeService()
        stage_nodes = node_service.build_stage_nodes(sources["stage_traces"])
        decision_nodes = node_service.build_decision_nodes(sources["decision_traces"])
        route_nodes = node_service.build_route_nodes(sources["route_trace"])
        provider_nodes = node_service.build_provider_nodes(sources["provider_trace"])
        response_nodes = node_service.build_response_nodes(sources["response_trace"])
        timeline_nodes = node_service.build_timeline_nodes(stage_nodes, decision_nodes, route_nodes, provider_nodes, response_nodes)
        edges = WorkbenchRelationEdgeService().build_edges(timeline_nodes)
        timeline_policy = WorkbenchPipelineTimelinePolicyService().build_policy()
        timeline = WorkbenchPipelineTimelineService().build_timeline(source_view, timeline_nodes, edges)
        filter_policy = WorkbenchTraceFilterPolicyService().build_policy()
        filters = WorkbenchTraceFilterService().build_default_filters()
        filter_state = WorkbenchTraceFilterStateService().build_filter_state(filters, timeline)
        selection_view = WorkbenchTraceSelectionViewService().build_selection_view(timeline)
        trace_explorer_view = WorkbenchTraceExplorerViewService().build_view(
            sources["trace_explorer_panel_model"],
            source_view,
            timeline,
            filter_state,
            selection_view,
        )
        inspection_policy = WorkbenchTraceInspectionPolicyService().build_policy()
        inspection_summary = WorkbenchTraceInspectionSummaryService().build_summary(
            trace_explorer_view.trace_explorer_view_id,
            stage_nodes,
            decision_nodes,
            route_nodes,
            provider_nodes,
            response_nodes,
        )
        inspection_report = WorkbenchTraceInspectionReportService().build_report(trace_explorer_view, timeline, inspection_summary)
        findings = WorkbenchTraceExplorerFindingService().build_findings(
            sources,
            source_view,
            timeline,
            inspection_report,
            kwargs.get("attempt_flags"),
            kwargs.get("extra_findings"),
        )
        report_status = self._report_status(findings, trace_explorer_view, timeline, inspection_report)
        report = WorkbenchTraceExplorerReport(
            report_id="workbench_trace_explorer_report:v0.26.2",
            created_at=utc_now_iso(),
            trace_explorer_policy=policy,
            request=request,
            source_view=source_view,
            trace_explorer_view=trace_explorer_view,
            timeline_policy=timeline_policy,
            timeline=timeline,
            filter_policy=filter_policy,
            filter_state=filter_state,
            selection_view=selection_view,
            inspection_policy=inspection_policy,
            inspection_report=inspection_report,
            findings=findings,
            report_status=report_status,
            ready_for_v0_26_3=report_status in {"passed", "warning"},
            trace_explorer_view_created=trace_explorer_view.view_status in {"ready", "partial"},
            pipeline_timeline_created=timeline.timeline_status in {"ready", "partial", "warning"},
            stage_nodes_created=timeline.stage_node_count > 0,
            decision_nodes_created=timeline.decision_node_count > 0,
            relation_edges_created=bool(timeline.edges),
            limitations=[
                "v0.26.2 creates trace explorer and pipeline timeline view artifacts only; it does not render UI or rerun stages.",
                "Synthetic source loading represents existing v0.25.8 trace refs when no persistence layer is present.",
            ],
            withdrawal_conditions=[
                "Withdraw if v0.26.2 renders UI, mutates trace artifacts, reruns stages/routes, executes ask/repl, invokes providers, emits responses, executes commands, promotes memory, exposes raw data, adds external adapters, or uses an LLM judge.",
            ],
        )
        return {
            "report": report,
            "policy": policy,
            "request": request,
            "source_view": source_view,
            "trace_explorer_view": trace_explorer_view,
            "timeline_policy": timeline_policy,
            "timeline": timeline,
            "timeline_nodes": timeline_nodes,
            "stage_nodes": stage_nodes,
            "decision_nodes": decision_nodes,
            "route_nodes": route_nodes,
            "provider_nodes": provider_nodes,
            "response_nodes": response_nodes,
            "edges": edges,
            "filter_policy": filter_policy,
            "filters": filters,
            "filter_state": filter_state,
            "selection_view": selection_view,
            "inspection_policy": inspection_policy,
            "inspection_summary": inspection_summary,
            "inspection_report": inspection_report,
            "findings": findings,
            "pig_report": self.build_pig_report(),
            "ocpx_projection": self.build_ocpx_projection(),
            "sources": sources,
        }

    def _report_status(
        self,
        findings: list[WorkbenchTraceExplorerFinding],
        trace_explorer_view: WorkbenchTraceExplorerView,
        timeline: WorkbenchPipelineTimeline,
        inspection_report: WorkbenchTraceInspectionReport,
    ) -> str:
        if any(finding.severity == "critical" for finding in findings) or "blocked" in {trace_explorer_view.view_status, timeline.timeline_status, inspection_report.inspection_status}:
            return "blocked"
        if any(finding.severity == "error" for finding in findings) or timeline.timeline_status == "failed":
            return "failed"
        if any(finding.severity == "warning" for finding in findings) or "partial" in {trace_explorer_view.view_status, timeline.timeline_status, inspection_report.inspection_status}:
            return "warning"
        return "passed"

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": WORKBENCH_TRACE_EXPLORER_VERSION,
            "layer": WORKBENCH_TRACE_EXPLORER_LAYER,
            "subject": "trace_explorer_pipeline_timeline",
            "principles": [
                "Trace Explorer view is not UI rendering.",
                "Pipeline Timeline is not execution.",
                "Timeline node is not executable command.",
                "Stage node is a view of prior stage artifact.",
                "Decision node is a view of prior decision artifact.",
                "Provider node is a view of prior provider invocation trace, not provider invocation.",
                "Response node is a view of prior response assembly/emission, not response emission.",
                "Trace filter hides or emphasizes refs; it does not delete data.",
                "Trace inspection may summarize, but must not inline raw transcript/provider output/secrets.",
            ],
            "safety_boundary": {
                "trace_explorer_view_created": "conditional",
                "pipeline_timeline_created": "conditional",
                "stage_nodes_created": "conditional",
                "decision_nodes_created": "conditional",
                "actual_ui_rendered": False,
                "panel_rendered": False,
                "trace_mutated": False,
                "stage_rerun_performed": False,
                "route_rerun_performed": False,
                "ask_executed": False,
                "final_response_emitted": False,
                "provider_invoked": False,
                "local_command_executed": False,
                "direct_provider_invocation": False,
                "direct_file_access_performed": False,
                "direct_subprocess_performed": False,
                "command_rerun_performed": False,
                "autonomous_loop_started": False,
                "background_execution_started": False,
                "memory_promoted": False,
                "persistent_memory_written": False,
                "persona_mutated": False,
                "external_provider_adapter_implemented": False,
                "external_agent_adapter_implemented": False,
                "schumpeter_split_introduced": False,
                "credential_exposed": False,
                "raw_secret_output": False,
                "raw_provider_output_inline": False,
                "raw_transcript_persisted": False,
                "llm_judge_enabled": False,
            },
            "future_direction": [
                "v0.26.3 provider / capability browser",
                "v0.26.4 evidence / report inspector",
                "v0.26.5 safety gate / approval console",
                "v0.26.6 run dashboard / session monitor",
                "v0.26.7 command surface",
                "v0.26.8 snapshot / OCEL export",
                "v0.27 memory candidate and continuity",
            ],
            "next_step": WORKBENCH_TRACE_EXPLORER_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "workbench_trace_explorer_pipeline_timeline_created",
            "version": WORKBENCH_TRACE_EXPLORER_VERSION,
            "source_read_models": [
                "WorkbenchViewStateState",
                "WorkbenchPanelRegistryState",
                "AgentSurfaceTraceState",
                "AgentTurnOCELProjectionState",
                "AgentPipelineStageTraceState",
                "AgentDecisionTraceState",
                "AgentRouteTraceState",
                "AgentProviderInvocationTraceViewState",
                "AgentResponseEmissionTraceState",
            ],
            "target_read_models": [
                "WorkbenchTraceExplorerViewState",
                "WorkbenchPipelineTimelineState",
                "WorkbenchStageNodeState",
                "WorkbenchDecisionNodeState",
                "WorkbenchRelationEdgeState",
                "WorkbenchTraceInspectionState",
                "V026ReadinessState",
            ],
            "effect_types": WORKBENCH_TRACE_EXPLORER_EFFECT_TYPES,
        }


def render_workbench_trace_explorer_cli(parts: dict[str, Any], section: str = "view") -> str:
    report: WorkbenchTraceExplorerReport = parts["report"]
    lines = [
        f"version={report.version}",
        f"layer={WORKBENCH_TRACE_EXPLORER_LAYER}",
        f"trace_explorer_view_created={str(report.trace_explorer_view_created).lower()}",
        f"pipeline_timeline_created={str(report.pipeline_timeline_created).lower()}",
        f"stage_nodes_created={str(report.stage_nodes_created).lower()}",
        f"decision_nodes_created={str(report.decision_nodes_created).lower()}",
        f"relation_edges_created={str(report.relation_edges_created).lower()}",
        f"ready_for_v0_26_3={str(report.ready_for_v0_26_3).lower()}",
        f"ready_for_v0_27={str(report.ready_for_v0_27).lower()}",
        f"actual_ui_rendered={str(report.actual_ui_rendered).lower()}",
        f"panel_rendered={str(report.panel_rendered).lower()}",
        f"trace_mutated={str(report.trace_mutated).lower()}",
        f"stage_rerun_performed={str(report.stage_rerun_performed).lower()}",
        f"route_rerun_performed={str(report.route_rerun_performed).lower()}",
        f"ask_executed={str(report.ask_executed).lower()}",
        f"final_response_emitted={str(report.final_response_emitted).lower()}",
        f"provider_invoked={str(report.provider_invoked).lower()}",
        f"local_command_executed={str(report.local_command_executed).lower()}",
        f"direct_provider_invocation={str(report.direct_provider_invocation).lower()}",
        f"direct_file_access_performed={str(report.direct_file_access_performed).lower()}",
        f"direct_subprocess_performed={str(report.direct_subprocess_performed).lower()}",
        f"command_rerun_performed={str(report.command_rerun_performed).lower()}",
        f"autonomous_loop_started={str(report.autonomous_loop_started).lower()}",
        f"background_execution_started={str(report.background_execution_started).lower()}",
        f"memory_promoted={str(report.memory_promoted).lower()}",
        f"persistent_memory_written={str(report.persistent_memory_written).lower()}",
        f"persona_mutated={str(report.persona_mutated).lower()}",
        f"external_provider_adapter_implemented={str(report.external_provider_adapter_implemented).lower()}",
        f"external_agent_adapter_implemented={str(report.external_agent_adapter_implemented).lower()}",
        f"schumpeter_split_introduced={str(report.schumpeter_split_introduced).lower()}",
        f"credential_exposed={str(report.credential_exposed).lower()}",
        f"raw_secret_output={str(report.raw_secret_output).lower()}",
        f"raw_provider_output_inline={str(report.raw_provider_output_inline).lower()}",
        f"raw_transcript_persisted={str(report.raw_transcript_persisted).lower()}",
        f"llm_judge_used={str(report.llm_judge_used).lower()}",
        f"next_required_step={report.next_required_step}",
        f"report_status={report.report_status}",
    ]
    if section == "source":
        source_view = parts["source_view"]
        lines.extend(
            [
                f"source_status={source_view.source_status}",
                f"stage_trace_ref_count={len(source_view.stage_trace_refs)}",
                f"decision_trace_ref_count={len(source_view.decision_trace_refs)}",
                f"raw_transcript_included={str(source_view.raw_transcript_included).lower()}",
                f"raw_provider_output_included={str(source_view.raw_provider_output_included).lower()}",
                f"raw_secret_included={str(source_view.raw_secret_included).lower()}",
                f"private_full_path_included={str(source_view.private_full_path_included).lower()}",
            ]
        )
    elif section == "timeline":
        timeline = parts["timeline"]
        lines.extend(
            [
                f"timeline_status={timeline.timeline_status}",
                f"stage_node_count={timeline.stage_node_count}",
                f"decision_node_count={timeline.decision_node_count}",
                f"route_node_count={timeline.route_node_count}",
                f"provider_node_count={timeline.provider_node_count}",
                f"response_node_count={timeline.response_node_count}",
                f"executes_now={str(timeline.executes_now).lower()}",
                f"rerun_enabled={str(timeline.rerun_enabled).lower()}",
            ]
        )
    elif section == "stages":
        lines.extend([f"stage_node={node.stage_id}:{node.stage_status}:rerun_enabled={str(node.rerun_enabled).lower()}" for node in parts["stage_nodes"]])
    elif section == "decisions":
        lines.extend([f"decision_node={node.decision_type}:{node.decision_outcome}:llm_judge_used={str(node.llm_judge_used).lower()}" for node in parts["decision_nodes"]])
    elif section == "filters":
        filter_state = parts["filter_state"]
        lines.extend(
            [
                f"filter_status={filter_state.filter_status}",
                f"active_filter_count={filter_state.active_filter_count}",
                f"data_deleted={str(filter_state.data_deleted).lower()}",
                f"access_policy_mutated={str(filter_state.access_policy_mutated).lower()}",
            ]
        )
    elif section == "inspect":
        inspection = parts["inspection_report"]
        lines.extend(
            [
                f"inspection_status={inspection.inspection_status}",
                f"trace_mutated={str(inspection.trace_mutated).lower()}",
                f"stage_rerun_performed={str(inspection.stage_rerun_performed).lower()}",
                f"provider_invoked={str(inspection.provider_invoked).lower()}",
                f"local_command_executed={str(inspection.local_command_executed).lower()}",
                f"raw_transcript_included={str(inspection.raw_transcript_included).lower()}",
                f"raw_provider_output_included={str(inspection.raw_provider_output_included).lower()}",
                f"raw_secret_included={str(inspection.raw_secret_included).lower()}",
            ]
        )
    elif section == "report":
        lines.extend([f"finding={finding.severity}:{finding.finding_type}" for finding in report.findings])
    return "\n".join(lines)
