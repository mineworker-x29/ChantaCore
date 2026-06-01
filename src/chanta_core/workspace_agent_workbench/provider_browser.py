from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from chanta_core.agent_surface.provider_invocation import AgentProviderInvocationReportService
from chanta_core.agent_surface.tool_routing import AgentToolRoutingReportService
from chanta_core.internal_provider.registry import (
    InternalProviderCapabilityDescriptor,
    InternalProviderCapabilitySurface,
    InternalProviderRef,
    InternalProviderRegistry,
    InternalProviderRegistryReportService,
)
from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace_agent_workbench.trace_explorer import WorkbenchTraceExplorerReportService
from chanta_core.workspace_agent_workbench.view_state import (
    WorkbenchPanel,
    WorkbenchViewState,
    WorkbenchViewStateReportService,
)


WORKBENCH_PROVIDER_BROWSER_VERSION = "v0.26.3"
WORKBENCH_PROVIDER_BROWSER_VERSION_NAME = "Provider / Capability Browser"
WORKBENCH_PROVIDER_BROWSER_KOREAN_NAME = "Provider·Capability Browser"
WORKBENCH_PROVIDER_BROWSER_LAYER = "workspace_agent_workbench"
WORKBENCH_PROVIDER_BROWSER_TRACK = "Workspace Agent Workbench"
WORKBENCH_PROVIDER_BROWSER_NEXT_STEP = "v0.26.4 Evidence / Report Inspector"

WORKBENCH_PROVIDER_BROWSER_IMPLEMENTED_SKILL_IDS = ["skill:workbench_provider_browser_view"]
WORKBENCH_PROVIDER_BROWSER_FUTURE_SKILL_IDS = [
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

WORKBENCH_PROVIDER_BROWSER_OBJECT_TYPES = [
    "workbench_provider_browser_policy",
    "workbench_provider_browser_request",
    "workbench_provider_source_view",
    "workbench_provider_browser_view",
    "workbench_provider_card",
    "workbench_capability_card",
    "workbench_provider_boundary_view",
    "workbench_capability_readiness_view",
    "workbench_route_compatibility_matrix",
    "workbench_provider_route_compatibility_row",
    "workbench_provider_selection_rationale_view",
    "workbench_provider_boundary_risk_view",
    "workbench_provider_pig_guidance_view",
    "workbench_provider_failure_mode_view",
    "workbench_human_intervention_point_ref",
    "workbench_provider_inspection_policy",
    "workbench_provider_inspection_summary",
    "workbench_provider_browser_finding",
    "workbench_provider_browser_report",
    "workbench_view_state",
    "internal_provider_registry",
    "internal_provider_capability_surface",
    "agent_tool_routing_report",
    "agent_provider_invocation_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

WORKBENCH_PROVIDER_BROWSER_EVENT_TYPES = [
    "workbench_provider_browser_requested",
    "workbench_provider_browser_policy_created",
    "workbench_provider_source_view_created",
    "workbench_provider_browser_view_created",
    "workbench_provider_card_created",
    "workbench_capability_card_created",
    "workbench_provider_boundary_view_created",
    "workbench_capability_readiness_view_created",
    "workbench_route_compatibility_matrix_created",
    "workbench_provider_selection_rationale_created",
    "workbench_provider_boundary_risk_view_created",
    "workbench_provider_pig_guidance_view_created",
    "workbench_provider_failure_mode_view_created",
    "workbench_human_intervention_point_identified",
    "workbench_provider_inspection_summary_created",
    "workbench_provider_browser_report_created",
    "workbench_provider_browser_warning_created",
    "workbench_provider_browser_blocked",
]

WORKBENCH_PROVIDER_BROWSER_RELATION_TYPES = [
    "uses_workbench_view_state",
    "uses_provider_browser_panel",
    "uses_internal_provider_registry",
    "uses_internal_provider_capability_surface",
    "uses_agent_tool_routing_report",
    "uses_agent_provider_selection",
    "uses_safety_gate_report",
    "uses_pig_guidance_ref",
    "creates_provider_source_view",
    "creates_provider_browser_view",
    "creates_provider_card",
    "creates_capability_card",
    "creates_provider_boundary_view",
    "creates_capability_readiness_view",
    "creates_route_compatibility_matrix",
    "creates_provider_selection_rationale_view",
    "creates_provider_boundary_risk_view",
    "attaches_pig_guidance_ref",
    "creates_provider_failure_mode_view",
    "identifies_human_intervention_point",
    "prepares_evidence_inspector",
    "defers_evidence_inspector_to_v0_26_4",
    "defers_approval_console_to_v0_26_5",
    "defers_run_dashboard_to_v0_26_6",
    "defers_command_surface_to_v0_26_7",
    "defers_snapshot_export_to_v0_26_8",
    "defers_memory_continuity_to_v0_27",
    "defers_external_provider_adapters_to_v0_29_plus",
    "defers_external_agent_dominion_to_v0_30_plus",
    "not_provider_invoked",
    "not_provider_test_run",
    "not_external_adapter_implemented",
    "not_pig_memory_promoted",
    "not_pig_policy_mutated",
    "not_pig_executed",
    "prevents_credential_exposure",
    "blocks_raw_provider_output_inline",
    "blocks_raw_secret_output",
    "recorded_in_envelope",
]

WORKBENCH_PROVIDER_BROWSER_EFFECT_TYPES = [
    "read_only_observation",
    "workbench_provider_browser_created",
    "workbench_provider_card_created",
    "workbench_capability_card_created",
    "workbench_provider_boundary_view_created",
    "workbench_capability_readiness_view_created",
    "workbench_route_compatibility_matrix_created",
    "workbench_provider_selection_rationale_created",
    "workbench_provider_boundary_risk_view_created",
    "workbench_provider_pig_guidance_view_created",
    "workbench_human_intervention_point_identified",
    "state_candidate_created",
]

WORKBENCH_PROVIDER_BROWSER_FORBIDDEN_EFFECT_TYPES = [
    "provider_invoked",
    "internal_provider_invoked",
    "provider_test_run_performed",
    "provider_boundary_bypassed",
    "external_provider_called",
    "external_agent_runtime_touched",
    "external_provider_adapter_implemented",
    "external_agent_adapter_implemented",
    "vendor_adapter_implemented",
    "pm4py_runtime_dependency_added",
    "ocpa_runtime_dependency_added",
    "pig_memory_promoted",
    "pig_policy_mutated",
    "pig_executed",
    "workbench_ui_implemented",
    "workbench_panel_rendered",
    "workbench_evidence_inspector_created",
    "workbench_approval_candidate_created",
    "workbench_run_dashboard_created",
    "workbench_command_executed",
    "workbench_snapshot_created",
    "stage_rerun_performed",
    "route_rerun_performed",
    "agent_ask_executed",
    "agent_repl_started",
    "final_response_emitted",
    "local_command_executed",
    "bounded_local_command_executed",
    "command_rerun_performed",
    "automatic_repair_performed",
    "direct_file_access_performed",
    "direct_subprocess_called",
    "background_execution_started",
    "autonomous_loop_started",
    "memory_promoted",
    "persistent_memory_written",
    "persona_mutated",
    "file_written",
    "file_edited",
    "file_deleted",
    "credential_exposed",
    "raw_secret_output",
    "raw_provider_output_inline",
    "raw_transcript_persisted",
    "schumpeter_split_introduced",
]

EXPECTED_PROVIDER_TYPES = {
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


def _ref(ref_type: str, ref_id: str | None, version: str = WORKBENCH_PROVIDER_BROWSER_VERSION) -> dict[str, Any]:
    return {"type": ref_type, "id": ref_id or "missing", "version": version}


@dataclass
class _Model:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class WorkbenchProviderBrowserPolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_PROVIDER_BROWSER_VERSION
    layer: str = WORKBENCH_PROVIDER_BROWSER_LAYER
    provider_browser_enabled: bool = True
    capability_browser_enabled: bool = True
    provider_selection_rationale_enabled: bool = True
    route_compatibility_view_enabled: bool = True
    boundary_risk_view_enabled: bool = True
    pig_guidance_view_enabled: bool = True
    human_intervention_point_view_enabled: bool = True
    actual_ui_rendering_enabled: bool = False
    panel_rendering_enabled: bool = False
    provider_invocation_enabled: bool = False
    provider_test_run_enabled: bool = False
    external_adapter_enabled: bool = False
    vendor_adapter_enabled: bool = False
    pm4py_runtime_dependency_enabled: bool = False
    ocpa_runtime_dependency_enabled: bool = False
    ask_execution_enabled: bool = False
    response_emission_enabled: bool = False
    local_runtime_execution_enabled: bool = False
    memory_promotion_enabled: bool = False
    persistent_memory_write_enabled: bool = False
    persona_mutation_enabled: bool = False
    refs_only_by_default: bool = True
    raw_provider_output_inline_forbidden: bool = True
    raw_transcript_inline_forbidden: bool = True
    raw_secret_inline_forbidden: bool = True
    credential_inline_forbidden: bool = True
    private_path_sanitization_required: bool = True
    pig_guidance_is_not_memory: bool = True
    pig_guidance_is_not_execution: bool = True
    pig_guidance_is_not_policy_mutation: bool = True
    ocel_visible: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchProviderBrowserRequest(_Model):
    request_id: str
    view_state_report_id: str | None
    view_state_id: str | None
    provider_registry_ref: dict[str, Any] | None
    capability_surface_ref: dict[str, Any] | None
    route_report_id: str | None
    provider_selection_id: str | None
    safety_gate_report_id: str | None
    pig_report_ref: dict[str, Any] | None
    focus_provider_ref: dict[str, Any] | None
    focus_capability_ref: dict[str, Any] | None
    filter_refs: list[dict[str, Any]]
    version: str = WORKBENCH_PROVIDER_BROWSER_VERSION
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"


@dataclass
class WorkbenchProviderSourceView(_Model):
    source_view_id: str
    provider_registry_ref: dict[str, Any] | None
    capability_surface_ref: dict[str, Any] | None
    provider_capability_refs: list[dict[str, Any]]
    provider_selection_refs: list[dict[str, Any]]
    route_plan_refs: list[dict[str, Any]]
    safety_gate_refs: list[dict[str, Any]]
    pig_guidance_refs: list[dict[str, Any]]
    source_status: str
    provider_count: int
    capability_count: int
    version: str = WORKBENCH_PROVIDER_BROWSER_VERSION
    external_adapter_count: int = 0
    vendor_adapter_count: int = 0
    raw_provider_output_included: bool = False
    raw_transcript_included: bool = False
    raw_secret_included: bool = False
    private_full_path_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchProviderCard(_Model):
    provider_card_id: str
    provider_id: str
    provider_name: str
    provider_type: str
    source_provider_ref: dict[str, Any] | None
    capability_count: int
    boundary_summary: str
    readiness_summary: str
    route_compatibility_summary: str
    risk_summary: str
    pig_guidance_summary: str | None
    implementation_status: str
    version: str = WORKBENCH_PROVIDER_BROWSER_VERSION
    provider_invocation_allowed_now: bool = False
    provider_test_run_allowed_now: bool = False
    external_adapter: bool = False
    vendor_adapter: bool = False
    raw_provider_output_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchCapabilityCard(_Model):
    capability_card_id: str
    capability_id: str
    capability_name: str
    provider_id: str
    provider_type: str
    capability_kind: str
    source_capability_ref: dict[str, Any] | None
    read_only: bool
    bounded_execution_capable: bool
    requires_safety_gate: bool
    requires_v024_gate: bool
    allowed_for_route_plan: bool
    readiness_view_id: str | None
    boundary_view_id: str | None
    version: str = WORKBENCH_PROVIDER_BROWSER_VERSION
    invocation_enabled_now: bool = False
    executable_now: bool = False
    external_adapter: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchProviderBoundaryView(_Model):
    boundary_view_id: str
    provider_id: str
    provider_type: str
    boundary_type: str
    boundary_summary: str
    required_policies: list[str]
    forbidden_bypasses: list[str]
    requires_v0255_invocation: bool
    requires_v0247_gate: bool
    boundary_status: str
    version: str = WORKBENCH_PROVIDER_BROWSER_VERSION
    direct_invocation_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchCapabilityReadinessView(_Model):
    readiness_view_id: str
    provider_id: str
    capability_id: str
    readiness_status: str
    readiness_reason: str
    missing_requirements: list[str]
    required_boundaries: list[str]
    version: str = WORKBENCH_PROVIDER_BROWSER_VERSION
    not_execution_ready_by_itself: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchProviderRouteCompatibilityRow(_Model):
    row_id: str
    provider_id: str
    capability_id: str | None
    route_kind: str
    intent_category: str | None
    compatible: bool
    compatibility_reason: str
    required_boundaries: list[str]
    risk_notes: list[str]
    pig_guidance_refs: list[dict[str, Any]]
    human_intervention_required: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchRouteCompatibilityMatrix(_Model):
    matrix_id: str
    rows: list[WorkbenchProviderRouteCompatibilityRow]
    route_kind_count: int
    provider_count: int
    compatibility_status: str
    version: str = WORKBENCH_PROVIDER_BROWSER_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchProviderSelectionRationaleView(_Model):
    rationale_view_id: str
    provider_id: str
    capability_id: str | None
    source_selection_ref: dict[str, Any] | None
    selected: bool
    rejected: bool
    deferred: bool
    selection_reason: str
    rejection_reason: str | None
    deferral_reason: str | None
    ranking_basis: list[str]
    route_context_refs: list[dict[str, Any]]
    safety_context_refs: list[dict[str, Any]]
    pig_guidance_refs: list[dict[str, Any]]
    version: str = WORKBENCH_PROVIDER_BROWSER_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchProviderBoundaryRiskView(_Model):
    risk_view_id: str
    provider_id: str
    capability_id: str | None
    risk_level: str
    risk_categories: list[str]
    risk_summary: str
    mitigation_boundary_refs: list[dict[str, Any]]
    human_intervention_recommended: bool
    version: str = WORKBENCH_PROVIDER_BROWSER_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchProviderPIGGuidanceView(_Model):
    pig_guidance_view_id: str
    provider_id: str | None
    capability_id: str | None
    source_pig_ref: dict[str, Any] | None
    guidance_type: str
    guidance_summary: str
    related_route_kind: str | None
    related_decision_point_refs: list[dict[str, Any]]
    version: str = WORKBENCH_PROVIDER_BROWSER_VERSION
    pig_guidance_is_memory: bool = False
    pig_guidance_mutates_policy: bool = False
    pig_guidance_executes: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchProviderFailureModeView(_Model):
    failure_mode_view_id: str
    provider_id: str
    capability_id: str | None
    known_failure_modes: list[str]
    last_failure_refs: list[dict[str, Any]]
    failure_cause_refs: list[dict[str, Any]]
    recovery_guidance_refs: list[dict[str, Any]]
    version: str = WORKBENCH_PROVIDER_BROWSER_VERSION
    auto_rerun_enabled: bool = False
    automatic_repair_enabled: bool = False
    provider_test_run_performed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchHumanInterventionPointRef(_Model):
    human_intervention_point_id: str
    provider_id: str | None
    capability_id: str | None
    route_kind: str | None
    intervention_type: str
    reason: str
    source_refs: list[dict[str, Any]]
    version: str = WORKBENCH_PROVIDER_BROWSER_VERSION
    approval_created_now: bool = False
    execution_triggered_now: bool = False
    ocel_visible: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchProviderBrowserView(_Model):
    provider_browser_view_id: str
    panel_id: str | None
    source_view: WorkbenchProviderSourceView
    provider_cards: list[WorkbenchProviderCard]
    capability_cards: list[WorkbenchCapabilityCard]
    boundary_views: list[WorkbenchProviderBoundaryView]
    readiness_views: list[WorkbenchCapabilityReadinessView]
    route_compatibility_matrix: WorkbenchRouteCompatibilityMatrix
    selection_rationale_views: list[WorkbenchProviderSelectionRationaleView]
    boundary_risk_views: list[WorkbenchProviderBoundaryRiskView]
    pig_guidance_views: list[WorkbenchProviderPIGGuidanceView]
    failure_mode_views: list[WorkbenchProviderFailureModeView]
    human_intervention_points: list[WorkbenchHumanInterventionPointRef]
    view_status: str
    version: str = WORKBENCH_PROVIDER_BROWSER_VERSION
    renders_ui_now: bool = False
    invokes_provider_now: bool = False
    provider_test_run_performed: bool = False
    external_adapter_implemented: bool = False
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchProviderInspectionPolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_PROVIDER_BROWSER_VERSION
    inspection_enabled: bool = True
    inspection_is_read_only: bool = True
    summarize_refs_allowed: bool = True
    raw_provider_output_inline_forbidden: bool = True
    raw_transcript_inline_forbidden: bool = True
    raw_secret_inline_forbidden: bool = True
    provider_invocation_forbidden: bool = True
    provider_test_run_forbidden: bool = True
    external_adapter_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchProviderInspectionSummary(_Model):
    inspection_summary_id: str
    provider_browser_view_id: str
    provider_summary: list[dict[str, Any]]
    capability_summary: list[dict[str, Any]]
    route_compatibility_summary: list[dict[str, Any]]
    boundary_risk_summary: list[dict[str, Any]]
    pig_guidance_summary: list[dict[str, Any]]
    human_intervention_summary: list[dict[str, Any]]
    failure_mode_summary: list[dict[str, Any]]
    summary_status: str
    version: str = WORKBENCH_PROVIDER_BROWSER_VERSION
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchProviderBrowserFinding(_Model):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class WorkbenchProviderBrowserReport(_Model):
    report_id: str
    created_at: str
    provider_browser_policy: WorkbenchProviderBrowserPolicy
    request: WorkbenchProviderBrowserRequest
    source_view: WorkbenchProviderSourceView
    provider_browser_view: WorkbenchProviderBrowserView
    inspection_policy: WorkbenchProviderInspectionPolicy
    inspection_summary: WorkbenchProviderInspectionSummary
    findings: list[WorkbenchProviderBrowserFinding]
    report_status: str
    ready_for_v0_26_4: bool
    provider_browser_view_created: bool
    provider_cards_created: bool
    capability_cards_created: bool
    boundary_views_created: bool
    readiness_views_created: bool
    route_compatibility_matrix_created: bool
    selection_rationale_views_created: bool
    boundary_risk_views_created: bool
    pig_guidance_views_created: bool
    human_intervention_points_created: bool
    version: str = WORKBENCH_PROVIDER_BROWSER_VERSION
    ready_for_v0_27: bool = False
    actual_ui_rendered: bool = False
    panel_rendered: bool = False
    provider_invoked: bool = False
    provider_test_run_performed: bool = False
    provider_boundary_bypassed: bool = False
    external_provider_adapter_implemented: bool = False
    external_agent_adapter_implemented: bool = False
    vendor_adapter_implemented: bool = False
    pm4py_runtime_dependency_added: bool = False
    ocpa_runtime_dependency_added: bool = False
    pig_memory_promoted: bool = False
    pig_policy_mutated: bool = False
    pig_executed: bool = False
    ask_executed: bool = False
    final_response_emitted: bool = False
    local_command_executed: bool = False
    direct_provider_invocation: bool = False
    direct_file_access_performed: bool = False
    direct_subprocess_performed: bool = False
    command_rerun_performed: bool = False
    automatic_repair_performed: bool = False
    autonomous_loop_started: bool = False
    background_execution_started: bool = False
    memory_promoted: bool = False
    persistent_memory_written: bool = False
    persona_mutated: bool = False
    schumpeter_split_introduced: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    raw_provider_output_inline: bool = False
    raw_transcript_persisted: bool = False
    llm_judge_used: bool = False
    next_required_step: str = WORKBENCH_PROVIDER_BROWSER_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.26.4 Evidence / Report Inspector begins or provider browser policy changes."


class WorkbenchProviderBrowserPrerequisiteSourceService:
    def __init__(
        self,
        *,
        view_state_available: bool = True,
        provider_browser_panel_available: bool = True,
        provider_registry_available: bool = True,
        capability_surface_available: bool = True,
        routing_available: bool = True,
        pig_guidance_available: bool = True,
        invocation_report_available: bool = True,
    ) -> None:
        self.view_state_available = view_state_available
        self.provider_browser_panel_available = provider_browser_panel_available
        self.provider_registry_available = provider_registry_available
        self.capability_surface_available = capability_surface_available
        self.routing_available = routing_available
        self.pig_guidance_available = pig_guidance_available
        self.invocation_report_available = invocation_report_available

    def load_workbench_view_state(self) -> WorkbenchViewState | None:
        if not self.view_state_available:
            return None
        return WorkbenchViewStateReportService().build_all_parts()["view_state"]

    def load_provider_browser_panel_model(self, view_state: WorkbenchViewState | None) -> WorkbenchPanel | None:
        if not self.provider_browser_panel_available or view_state is None:
            return None
        return next((panel for panel in view_state.panel_registry_view.panels if panel.panel_type == "provider_browser"), None)

    def load_internal_provider_registry(self) -> InternalProviderRegistry | None:
        if not self.provider_registry_available:
            return None
        return InternalProviderRegistryReportService().build_report().registry

    def load_internal_provider_capability_surface(self, registry: InternalProviderRegistry | None) -> list[InternalProviderCapabilitySurface]:
        if not self.capability_surface_available or registry is None:
            return []
        return registry.capability_surfaces

    def load_tool_routing_report_if_available(self) -> dict[str, Any] | None:
        if not self.routing_available:
            return None
        return AgentToolRoutingReportService().build_all_parts()

    def load_provider_selection_if_available(self, routing_parts: dict[str, Any] | None) -> Any | None:
        return routing_parts.get("selection") if routing_parts else None

    def load_safety_gate_report_if_available(self, routing_parts: dict[str, Any] | None) -> Any | None:
        report = routing_parts.get("report") if routing_parts else None
        return getattr(report, "route_plan", None)

    def load_pig_guidance_refs_if_available(self, routing_parts: dict[str, Any] | None) -> list[dict[str, Any]]:
        if not self.pig_guidance_available:
            return []
        route_plan = routing_parts.get("route_plan") if routing_parts else None
        route_kind = getattr(route_plan, "route_kind", "unknown") if route_plan else "unknown"
        return [
            {
                "type": "pig_guidance_ref",
                "id": f"pig_guidance:provider_browser:{route_kind}",
                "version": WORKBENCH_PROVIDER_BROWSER_VERSION,
                "summary": "OCEL-visible guidance candidate only; not memory, policy mutation, or execution.",
                "route_kind": route_kind,
            }
        ]

    def load_provider_invocation_report_refs_if_available(self) -> list[dict[str, Any]]:
        if not self.invocation_report_available:
            return []
        report = AgentProviderInvocationReportService().build_report()
        return [_ref("agent_provider_invocation_report", report.report_id, getattr(report, "version", "v0.25.5"))]

    def load_trace_explorer_report_if_available(self) -> Any | None:
        return WorkbenchTraceExplorerReportService().build_report()

    def load_sources(self) -> dict[str, Any]:
        view_state = self.load_workbench_view_state()
        panel = self.load_provider_browser_panel_model(view_state)
        registry = self.load_internal_provider_registry()
        surfaces = self.load_internal_provider_capability_surface(registry)
        routing_parts = self.load_tool_routing_report_if_available()
        trace_report = self.load_trace_explorer_report_if_available()
        return {
            "workbench_view_state": view_state,
            "provider_browser_panel_model": panel,
            "provider_registry": registry,
            "capability_surfaces": surfaces,
            "routing_parts": routing_parts,
            "route_report": routing_parts.get("report") if routing_parts else None,
            "provider_selection": self.load_provider_selection_if_available(routing_parts),
            "safety_gate_report": self.load_safety_gate_report_if_available(routing_parts),
            "pig_guidance_refs": self.load_pig_guidance_refs_if_available(routing_parts),
            "provider_invocation_report_refs": self.load_provider_invocation_report_refs_if_available(),
            "trace_explorer_report": trace_report,
        }


class WorkbenchProviderBrowserPolicyService:
    def build_policy(self) -> WorkbenchProviderBrowserPolicy:
        return WorkbenchProviderBrowserPolicy(policy_id="workbench_provider_browser_policy:v0.26.3")


class WorkbenchProviderBrowserRequestService:
    def build_request(self, sources: dict[str, Any], strictness: str = "standard") -> WorkbenchProviderBrowserRequest:
        view_state = sources.get("workbench_view_state")
        registry = sources.get("provider_registry")
        surfaces = sources.get("capability_surfaces") or []
        route_report = sources.get("route_report")
        selection = sources.get("provider_selection")
        return WorkbenchProviderBrowserRequest(
            request_id="workbench_provider_browser_request:v0.26.3",
            view_state_report_id="workbench_view_state_report:v0.26.1" if view_state else None,
            view_state_id=view_state.view_state_id if view_state else None,
            provider_registry_ref=_ref("internal_provider_registry", registry.registry_id, getattr(registry, "version", "v0.24.1")) if registry else None,
            capability_surface_ref=_ref("internal_provider_capability_surface", surfaces[0].surface_id, "v0.24.1") if surfaces else None,
            route_report_id=route_report.report_id if route_report else None,
            provider_selection_id=selection.selection_id if selection else None,
            safety_gate_report_id=getattr(sources.get("safety_gate_report"), "safety_gate_report_id", None),
            pig_report_ref=_ref("pig_report", "provider_browser_guidance_refs:v0.26.3") if sources.get("pig_guidance_refs") else None,
            focus_provider_ref=None,
            focus_capability_ref=None,
            filter_refs=[],
            source_refs=[_ref("workbench_view_state", view_state.view_state_id, "v0.26.1")] if view_state else [],
            strictness=strictness,
        )


class WorkbenchProviderSourceViewService:
    def build_source_view(self, sources: dict[str, Any]) -> WorkbenchProviderSourceView:
        registry: InternalProviderRegistry | None = sources.get("provider_registry")
        surfaces: list[InternalProviderCapabilitySurface] = sources.get("capability_surfaces") or []
        provider_capability_refs = [
            _ref("internal_provider_capability_descriptor", capability.capability_id, capability.introduced_in)
            for surface in surfaces
            for capability in surface.capabilities
        ]
        selection = sources.get("provider_selection")
        route_report = sources.get("route_report")
        source_status = "complete"
        if not sources.get("workbench_view_state") or not sources.get("provider_browser_panel_model"):
            source_status = "blocked"
        elif not registry or not surfaces:
            source_status = "partial"
        return WorkbenchProviderSourceView(
            source_view_id="workbench_provider_source_view:v0.26.3",
            provider_registry_ref=_ref("internal_provider_registry", registry.registry_id, getattr(registry, "version", "v0.24.1")) if registry else None,
            capability_surface_ref=_ref("internal_provider_capability_surface", surfaces[0].surface_id, "v0.24.1") if surfaces else None,
            provider_capability_refs=provider_capability_refs,
            provider_selection_refs=[_ref("agent_provider_selection", selection.selection_id, getattr(selection, "version", "v0.25.4"))] if selection else [],
            route_plan_refs=[_ref("agent_tool_route_plan", route_report.route_plan.route_plan_id, "v0.25.4")] if route_report and route_report.route_plan else [],
            safety_gate_refs=[_ref("agent_safety_gate_report", route_report.route_plan.safety_gate_report_id, "v0.25.3")] if route_report and route_report.route_plan else [],
            pig_guidance_refs=sources.get("pig_guidance_refs") or [],
            source_status=source_status,
            provider_count=len(registry.provider_refs) if registry else 0,
            capability_count=len(provider_capability_refs),
            external_adapter_count=getattr(registry, "external_adapter_count", 0) if registry else 0,
            vendor_adapter_count=0,
            evidence_refs=[_ref("workbench_view_state", sources["workbench_view_state"].view_state_id, "v0.26.1")] if sources.get("workbench_view_state") else [],
        )


class WorkbenchProviderCardService:
    def build_provider_cards(
        self,
        registry: InternalProviderRegistry | None,
        surfaces: list[InternalProviderCapabilitySurface],
        pig_guidance_refs: list[dict[str, Any]],
    ) -> list[WorkbenchProviderCard]:
        if registry is None:
            return []
        surface_by_provider = {surface.provider_id: surface for surface in surfaces}
        return [
            WorkbenchProviderCard(
                provider_card_id=f"workbench_provider_card:{provider.provider_id}",
                provider_id=provider.provider_id,
                provider_name=provider.provider_name,
                provider_type=provider.provider_type if provider.provider_type in EXPECTED_PROVIDER_TYPES else "unknown",
                source_provider_ref=_ref("internal_provider_ref", provider.provider_id, provider.introduced_in),
                capability_count=len(surface_by_provider.get(provider.provider_id).capabilities) if surface_by_provider.get(provider.provider_id) else 0,
                boundary_summary=f"{provider.provider_type} is visible through policy-bound provider refs only.",
                readiness_summary="Capability readiness is route-planning visibility, not execution readiness by itself.",
                route_compatibility_summary="Compatibility rows are explanatory and do not execute routes.",
                risk_summary=self._risk_summary(provider),
                pig_guidance_summary="PIG guidance refs attached as candidate/rationale only." if pig_guidance_refs else None,
                implementation_status=self._implementation_status(provider.implementation_status),
                external_adapter=provider.external_adapter,
                vendor_adapter=False,
                evidence_refs=[_ref("internal_provider_ref", provider.provider_id, provider.introduced_in)],
            )
            for provider in registry.provider_refs
        ]

    def _implementation_status(self, status: str) -> str:
        return status if status in {"registered", "available", "partial", "missing", "disabled", "blocked", "future_track"} else "registered"

    def _risk_summary(self, provider: InternalProviderRef) -> str:
        if provider.provider_type == "local_runtime_provider":
            return "High boundary sensitivity; future invocation must remain gated and human-reviewable."
        if provider.provider_type in {"file_read_provider", "repository_search_provider"}:
            return "Read boundary sensitivity; private path and raw content exposure remain forbidden."
        return "Low or policy-bound risk when represented as refs-only view artifacts."


class WorkbenchCapabilityCardService:
    def build_capability_cards(self, surfaces: list[InternalProviderCapabilitySurface]) -> list[WorkbenchCapabilityCard]:
        cards: list[WorkbenchCapabilityCard] = []
        for surface in surfaces:
            for capability in surface.capabilities:
                boundary_id = f"workbench_provider_boundary_view:{surface.provider_id}"
                readiness_id = f"workbench_capability_readiness_view:{capability.capability_id}"
                cards.append(
                    WorkbenchCapabilityCard(
                        capability_card_id=f"workbench_capability_card:{capability.capability_id}",
                        capability_id=capability.capability_id,
                        capability_name=capability.capability_name,
                        provider_id=capability.provider_id,
                        provider_type=capability.provider_type,
                        capability_kind=capability.capability_category,
                        source_capability_ref=_ref("internal_provider_capability_descriptor", capability.capability_id, capability.introduced_in),
                        read_only=capability.read_only,
                        bounded_execution_capable=capability.execution_capable_future,
                        requires_safety_gate=capability.execution_capable_future or capability.provider_type == "local_runtime_provider",
                        requires_v024_gate=capability.provider_type == "local_runtime_provider",
                        allowed_for_route_plan=True,
                        readiness_view_id=readiness_id,
                        boundary_view_id=boundary_id,
                        external_adapter=False,
                        evidence_refs=[_ref("internal_provider_capability_descriptor", capability.capability_id, capability.introduced_in)],
                    )
                )
        return cards


class WorkbenchProviderBoundaryViewService:
    def build_boundary_views(self, registry: InternalProviderRegistry | None) -> list[WorkbenchProviderBoundaryView]:
        if registry is None:
            return []
        return [
            WorkbenchProviderBoundaryView(
                boundary_view_id=f"workbench_provider_boundary_view:{provider.provider_id}",
                provider_id=provider.provider_id,
                provider_type=provider.provider_type,
                boundary_type=self._boundary_type(provider.provider_type),
                boundary_summary="Boundary is displayed for inspection only; direct invocation remains forbidden.",
                required_policies=self._required_policies(provider.provider_type),
                forbidden_bypasses=["direct_provider_invocation", "provider_test_run", "provider_boundary_bypass"],
                requires_v0255_invocation=True,
                requires_v0247_gate=provider.provider_type == "local_runtime_provider",
                boundary_status="ready",
                evidence_refs=[_ref("internal_provider_ref", provider.provider_id, provider.introduced_in)],
            )
            for provider in registry.provider_refs
        ]

    def _boundary_type(self, provider_type: str) -> str:
        return {
            "workspace_read_provider": "read_only_boundary",
            "repository_search_provider": "read_only_boundary",
            "file_read_provider": "file_read_boundary",
            "ocel_inspection_provider": "process_inspection_boundary",
            "pig_inspection_provider": "provider_policy_boundary",
            "ocpx_projection_provider": "evidence_boundary",
            "local_runtime_provider": "local_runtime_boundary",
            "diagnostic_provider": "provider_policy_boundary",
            "candidate_generation_provider": "safety_gate_boundary",
        }.get(provider_type, "unknown")

    def _required_policies(self, provider_type: str) -> list[str]:
        policies = ["v0.25.5_provider_invocation_boundary", "refs_only_provider_browser_policy"]
        if provider_type == "local_runtime_provider":
            policies.append("v0.24_local_runtime_gate")
        if provider_type in {"file_read_provider", "workspace_read_provider"}:
            policies.append("private_path_sanitization")
        return policies


class WorkbenchCapabilityReadinessViewService:
    def build_readiness_views(self, capability_cards: list[WorkbenchCapabilityCard]) -> list[WorkbenchCapabilityReadinessView]:
        return [
            WorkbenchCapabilityReadinessView(
                readiness_view_id=f"workbench_capability_readiness_view:{card.capability_id}",
                provider_id=card.provider_id,
                capability_id=card.capability_id,
                readiness_status=self._status(card),
                readiness_reason="Readiness describes route planning and boundary visibility only.",
                missing_requirements=[] if card.read_only else ["future approval console", "provider invocation orchestrator"],
                required_boundaries=[card.boundary_view_id or "unknown_boundary"],
                evidence_refs=[_ref("workbench_capability_card", card.capability_card_id)],
            )
            for card in capability_cards
        ]

    def _status(self, card: WorkbenchCapabilityCard) -> str:
        if card.provider_type == "local_runtime_provider":
            return "requires_gate"
        if card.read_only:
            return "ready_for_route_plan"
        return "ready_for_invocation_via_v0255"


class WorkbenchRouteCompatibilityMatrixService:
    def build_matrix(
        self,
        capability_cards: list[WorkbenchCapabilityCard],
        routing_parts: dict[str, Any] | None,
        pig_guidance_refs: list[dict[str, Any]],
    ) -> WorkbenchRouteCompatibilityMatrix:
        route_plan = routing_parts.get("route_plan") if routing_parts else None
        route_kind = getattr(route_plan, "route_kind", "unknown") if route_plan else "unknown"
        intent_category = getattr(route_plan, "primary_intent_category", None) if route_plan else None
        rows = [
            WorkbenchProviderRouteCompatibilityRow(
                row_id=f"workbench_provider_route_compatibility_row:{card.capability_id}:{route_kind}",
                provider_id=card.provider_id,
                capability_id=card.capability_id,
                route_kind=route_kind,
                intent_category=intent_category,
                compatible=card.allowed_for_route_plan,
                compatibility_reason="Provider capability is visible for route planning only; no route is executed.",
                required_boundaries=[boundary for boundary in [card.boundary_view_id, "v0.25.5_provider_invocation_boundary"] if boundary],
                risk_notes=["human review recommended"] if card.requires_safety_gate else [],
                pig_guidance_refs=pig_guidance_refs,
                human_intervention_required=card.requires_safety_gate,
                evidence_refs=[_ref("workbench_capability_card", card.capability_card_id)],
            )
            for card in capability_cards
        ]
        return WorkbenchRouteCompatibilityMatrix(
            matrix_id="workbench_route_compatibility_matrix:v0.26.3",
            rows=rows,
            route_kind_count=len({row.route_kind for row in rows}) if rows else 0,
            provider_count=len({row.provider_id for row in rows}),
            compatibility_status="ready" if rows else "partial",
        )


class WorkbenchProviderSelectionRationaleViewService:
    def build_rationale_views(
        self,
        routing_parts: dict[str, Any] | None,
        pig_guidance_refs: list[dict[str, Any]],
    ) -> list[WorkbenchProviderSelectionRationaleView]:
        selection = routing_parts.get("selection") if routing_parts else None
        if selection is None:
            return []
        views: list[WorkbenchProviderSelectionRationaleView] = []
        for candidate in selection.selected_candidates:
            views.append(self._from_candidate(candidate, True, False, False, pig_guidance_refs))
        for index, candidate in enumerate(selection.rejected_candidates):
            views.append(self._from_candidate(candidate, False, index % 2 == 0, index % 2 == 1, pig_guidance_refs))
        return views

    def _from_candidate(
        self,
        candidate: Any,
        selected: bool,
        rejected: bool,
        deferred: bool,
        pig_guidance_refs: list[dict[str, Any]],
    ) -> WorkbenchProviderSelectionRationaleView:
        provider_ref = candidate.provider_ref
        return WorkbenchProviderSelectionRationaleView(
            rationale_view_id=f"workbench_provider_selection_rationale_view:{candidate.selection_candidate_id}",
            provider_id=provider_ref.provider_id,
            capability_id=provider_ref.capability_id,
            source_selection_ref=_ref("agent_provider_selection_candidate", candidate.selection_candidate_id, "v0.25.4"),
            selected=selected,
            rejected=rejected,
            deferred=deferred,
            selection_reason=candidate.reason if selected else "Candidate retained for explainability; not selected for execution.",
            rejection_reason=candidate.reason if rejected else None,
            deferral_reason="Optional candidate deferred until later workbench capability." if deferred else None,
            ranking_basis=["deterministic route mapping", "provider capability catalog", "safety context refs", "PIG guidance refs"],
            route_context_refs=[_ref("agent_route_kind", candidate.route_kind, "v0.25.4")],
            safety_context_refs=[_ref("agent_tool_route_precondition", item, "v0.25.4") for item in candidate.preconditions],
            pig_guidance_refs=pig_guidance_refs,
            evidence_refs=[_ref("agent_provider_selection_candidate", candidate.selection_candidate_id, "v0.25.4")],
        )


class WorkbenchProviderBoundaryRiskViewService:
    def build_risk_views(
        self,
        capability_cards: list[WorkbenchCapabilityCard],
        boundary_views: list[WorkbenchProviderBoundaryView],
    ) -> list[WorkbenchProviderBoundaryRiskView]:
        boundary_by_provider = {boundary.provider_id: boundary for boundary in boundary_views}
        return [
            WorkbenchProviderBoundaryRiskView(
                risk_view_id=f"workbench_provider_boundary_risk_view:{card.capability_id}",
                provider_id=card.provider_id,
                capability_id=card.capability_id,
                risk_level=self._risk_level(card),
                risk_categories=self._risk_categories(card),
                risk_summary="Risk is inspectable only; mitigation does not execute automatically.",
                mitigation_boundary_refs=[_ref("workbench_provider_boundary_view", boundary_by_provider[card.provider_id].boundary_view_id)] if card.provider_id in boundary_by_provider else [],
                human_intervention_recommended=card.requires_safety_gate,
                evidence_refs=[_ref("workbench_capability_card", card.capability_card_id)],
            )
            for card in capability_cards
        ]

    def _risk_level(self, card: WorkbenchCapabilityCard) -> str:
        if card.provider_type == "local_runtime_provider":
            return "high"
        if card.provider_type in {"file_read_provider", "repository_search_provider", "ocel_inspection_provider"}:
            return "medium"
        return "low"

    def _risk_categories(self, card: WorkbenchCapabilityCard) -> list[str]:
        categories = ["provider_boundary"]
        if card.provider_type == "local_runtime_provider":
            categories.extend(["local_runtime_execution", "policy_bypass"])
        if card.provider_type in {"file_read_provider", "workspace_read_provider"}:
            categories.extend(["file_read", "private_path_exposure"])
        if card.external_adapter:
            categories.append("external_adapter")
        return categories


class WorkbenchProviderPIGGuidanceViewService:
    def build_pig_guidance_views(
        self,
        pig_guidance_refs: list[dict[str, Any]],
        capability_cards: list[WorkbenchCapabilityCard],
    ) -> list[WorkbenchProviderPIGGuidanceView]:
        if not pig_guidance_refs:
            return []
        first = capability_cards[0] if capability_cards else None
        return [
            WorkbenchProviderPIGGuidanceView(
                pig_guidance_view_id=f"workbench_provider_pig_guidance_view:{index}",
                provider_id=first.provider_id if first else None,
                capability_id=first.capability_id if first else None,
                source_pig_ref=ref,
                guidance_type="rationale",
                guidance_summary=ref.get("summary", "PIG guidance ref is visible as candidate rationale only."),
                related_route_kind=ref.get("route_kind"),
                related_decision_point_refs=[_ref("agent_route_decision", ref.get("route_kind", "unknown"), "v0.25.4")],
                evidence_refs=[ref],
            )
            for index, ref in enumerate(pig_guidance_refs)
        ]


class WorkbenchProviderFailureModeViewService:
    def build_failure_mode_views(
        self,
        provider_cards: list[WorkbenchProviderCard],
        invocation_report_refs: list[dict[str, Any]],
    ) -> list[WorkbenchProviderFailureModeView]:
        return [
            WorkbenchProviderFailureModeView(
                failure_mode_view_id=f"workbench_provider_failure_mode_view:{card.provider_id}",
                provider_id=card.provider_id,
                capability_id=None,
                known_failure_modes=["missing_source_ref", "policy_boundary_block", "sanitized_output_required"],
                last_failure_refs=invocation_report_refs[:1],
                failure_cause_refs=[_ref("provider_failure_cause", "refs_only_boundary")],
                recovery_guidance_refs=[_ref("provider_recovery_guidance", "human_review_before_invocation")],
                evidence_refs=[_ref("workbench_provider_card", card.provider_card_id)],
            )
            for card in provider_cards
        ]


class WorkbenchHumanInterventionPointService:
    def build_human_intervention_points(
        self,
        risk_views: list[WorkbenchProviderBoundaryRiskView],
        matrix: WorkbenchRouteCompatibilityMatrix,
    ) -> list[WorkbenchHumanInterventionPointRef]:
        points = [
            WorkbenchHumanInterventionPointRef(
                human_intervention_point_id=f"workbench_human_intervention_point:{risk.provider_id}:{risk.capability_id}",
                provider_id=risk.provider_id,
                capability_id=risk.capability_id,
                route_kind=matrix.rows[0].route_kind if matrix.rows else None,
                intervention_type="boundary_check_required" if risk.risk_level in {"medium", "high"} else "manual_review_recommended",
                reason=risk.risk_summary,
                source_refs=[_ref("workbench_provider_boundary_risk_view", risk.risk_view_id)],
                evidence_refs=[_ref("workbench_provider_boundary_risk_view", risk.risk_view_id)],
            )
            for risk in risk_views
            if risk.human_intervention_recommended or risk.risk_level in {"medium", "high"}
        ]
        if not points and matrix.rows:
            row = matrix.rows[0]
            points.append(
                WorkbenchHumanInterventionPointRef(
                    human_intervention_point_id=f"workbench_human_intervention_point:{row.provider_id}:{row.route_kind}",
                    provider_id=row.provider_id,
                    capability_id=row.capability_id,
                    route_kind=row.route_kind,
                    intervention_type="manual_review_recommended",
                    reason="Human review point is visible, but approval is not created automatically.",
                    source_refs=[_ref("workbench_route_compatibility_matrix", matrix.matrix_id)],
                )
            )
        return points


class WorkbenchProviderBrowserViewService:
    def build_view(
        self,
        panel: WorkbenchPanel | None,
        source_view: WorkbenchProviderSourceView,
        provider_cards: list[WorkbenchProviderCard],
        capability_cards: list[WorkbenchCapabilityCard],
        boundary_views: list[WorkbenchProviderBoundaryView],
        readiness_views: list[WorkbenchCapabilityReadinessView],
        matrix: WorkbenchRouteCompatibilityMatrix,
        rationale_views: list[WorkbenchProviderSelectionRationaleView],
        risk_views: list[WorkbenchProviderBoundaryRiskView],
        pig_guidance_views: list[WorkbenchProviderPIGGuidanceView],
        failure_mode_views: list[WorkbenchProviderFailureModeView],
        human_intervention_points: list[WorkbenchHumanInterventionPointRef],
    ) -> WorkbenchProviderBrowserView:
        if source_view.source_status == "blocked":
            status = "blocked"
        elif not provider_cards or not capability_cards or not boundary_views:
            status = "failed"
        elif source_view.source_status == "partial" or matrix.compatibility_status == "partial":
            status = "partial"
        else:
            status = "ready"
        return WorkbenchProviderBrowserView(
            provider_browser_view_id="workbench_provider_browser_view:v0.26.3",
            panel_id=panel.panel_id if panel else None,
            source_view=source_view,
            provider_cards=provider_cards,
            capability_cards=capability_cards,
            boundary_views=boundary_views,
            readiness_views=readiness_views,
            route_compatibility_matrix=matrix,
            selection_rationale_views=rationale_views,
            boundary_risk_views=risk_views,
            pig_guidance_views=pig_guidance_views,
            failure_mode_views=failure_mode_views,
            human_intervention_points=human_intervention_points,
            view_status=status,
            evidence_refs=[_ref("workbench_panel", panel.panel_id, "v0.26.1")] if panel else [],
        )


class WorkbenchProviderInspectionPolicyService:
    def build_policy(self) -> WorkbenchProviderInspectionPolicy:
        return WorkbenchProviderInspectionPolicy(policy_id="workbench_provider_inspection_policy:v0.26.3")


class WorkbenchProviderInspectionSummaryService:
    def build_summary(self, view: WorkbenchProviderBrowserView) -> WorkbenchProviderInspectionSummary:
        status = "blocked" if view.view_status == "blocked" else "partial" if view.view_status in {"partial", "failed"} else "ready"
        return WorkbenchProviderInspectionSummary(
            inspection_summary_id="workbench_provider_inspection_summary:v0.26.3",
            provider_browser_view_id=view.provider_browser_view_id,
            provider_summary=[
                {"provider_ref": _ref("workbench_provider_card", card.provider_card_id), "provider_type": card.provider_type}
                for card in view.provider_cards
            ],
            capability_summary=[
                {"capability_ref": _ref("workbench_capability_card", card.capability_card_id), "read_only": card.read_only}
                for card in view.capability_cards
            ],
            route_compatibility_summary=[
                {"row_ref": _ref("workbench_provider_route_compatibility_row", row.row_id), "compatible": row.compatible}
                for row in view.route_compatibility_matrix.rows
            ],
            boundary_risk_summary=[
                {"risk_ref": _ref("workbench_provider_boundary_risk_view", risk.risk_view_id), "risk_level": risk.risk_level}
                for risk in view.boundary_risk_views
            ],
            pig_guidance_summary=[
                {"pig_guidance_ref": _ref("workbench_provider_pig_guidance_view", item.pig_guidance_view_id), "executes": item.pig_guidance_executes}
                for item in view.pig_guidance_views
            ],
            human_intervention_summary=[
                {"intervention_ref": _ref("workbench_human_intervention_point_ref", point.human_intervention_point_id), "approval_created_now": point.approval_created_now}
                for point in view.human_intervention_points
            ],
            failure_mode_summary=[
                {"failure_mode_ref": _ref("workbench_provider_failure_mode_view", failure.failure_mode_view_id), "auto_rerun_enabled": failure.auto_rerun_enabled}
                for failure in view.failure_mode_views
            ],
            summary_status=status,
            evidence_refs=[_ref("workbench_provider_browser_view", view.provider_browser_view_id)],
        )


class WorkbenchProviderBrowserFindingService:
    BLOCKED_FINDINGS = {
        "external_adapter_detected",
        "vendor_adapter_detected",
        "pm4py_runtime_dependency_detected",
        "ocpa_runtime_dependency_detected",
        "pig_guidance_as_memory_detected",
        "pig_policy_mutation_detected",
        "pig_execution_detected",
        "provider_invocation_attempted",
        "provider_test_run_attempted",
        "provider_boundary_bypass_attempted",
        "ask_execution_attempted",
        "final_response_emission_attempted",
        "local_command_execution_attempted",
        "direct_file_access_attempted",
        "direct_subprocess_attempted",
        "command_rerun_attempted",
        "automatic_repair_attempted",
        "memory_promotion_attempted",
        "persona_mutation_attempted",
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
        source_view: WorkbenchProviderSourceView,
        view: WorkbenchProviderBrowserView,
        attempt_flags: dict[str, bool] | None = None,
        extra_findings: list[str] | None = None,
    ) -> list[WorkbenchProviderBrowserFinding]:
        findings: list[WorkbenchProviderBrowserFinding] = []
        if not sources.get("workbench_view_state"):
            findings.append(self._finding("critical", "missing_workbench_view_state", "Workbench view state is unavailable."))
        if not sources.get("provider_browser_panel_model"):
            findings.append(self._finding("critical", "missing_provider_browser_panel", "Provider browser panel model is unavailable."))
        if not sources.get("provider_registry"):
            findings.append(self._finding("error", "missing_provider_registry", "Provider registry is unavailable."))
        if not sources.get("capability_surfaces"):
            findings.append(self._finding("error", "missing_capability_surface", "Capability surface is unavailable."))
        if not sources.get("route_report"):
            findings.append(self._finding("warning", "missing_route_report", "Route report is unavailable."))
        if not sources.get("provider_selection"):
            findings.append(self._finding("warning", "missing_provider_selection", "Provider selection is unavailable."))
        if source_view.source_status == "partial":
            findings.append(self._finding("warning", "partial_provider_source", "Provider source is partial and no data was fabricated."))
        if view.provider_cards:
            findings.append(self._finding("info", "provider_card_created", "Provider cards were created."))
        if view.capability_cards:
            findings.append(self._finding("info", "capability_card_created", "Capability cards were created."))
        if view.boundary_views:
            findings.append(self._finding("info", "boundary_view_created", "Provider boundary views were created."))
        if view.readiness_views:
            findings.append(self._finding("info", "capability_readiness_view_created", "Capability readiness views were created."))
        if view.route_compatibility_matrix.rows:
            findings.append(self._finding("info", "route_compatibility_matrix_created", "Route compatibility matrix was created."))
        if view.selection_rationale_views:
            findings.append(self._finding("info", "provider_selection_rationale_created", "Provider selection rationale views were created."))
        if view.boundary_risk_views:
            findings.append(self._finding("info", "provider_boundary_risk_view_created", "Provider boundary risk views were created."))
        if view.pig_guidance_views:
            findings.append(self._finding("info", "pig_guidance_ref_attached", "PIG guidance refs were attached as view-only rationale."))
        if view.human_intervention_points:
            findings.append(self._finding("info", "human_intervention_point_identified", "Human intervention point refs were identified."))
        if view.failure_mode_views:
            findings.append(self._finding("info", "provider_failure_mode_view_created", "Provider failure mode views were created."))
        for finding_type, active in (attempt_flags or {}).items():
            if active:
                normalized = finding_type if finding_type in self.BLOCKED_FINDINGS else f"{finding_type}_detected"
                findings.append(self._finding("critical", normalized, f"{normalized} was detected."))
        for finding_type in extra_findings or []:
            severity = "critical" if finding_type in self.BLOCKED_FINDINGS else "warning"
            findings.append(self._finding(severity, finding_type, f"{finding_type} was reported."))
        return findings

    def _finding(self, severity: str, finding_type: str, message: str) -> WorkbenchProviderBrowserFinding:
        return WorkbenchProviderBrowserFinding(
            finding_id=f"workbench_provider_browser_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            subject_ref={"id": "workbench_provider_browser"},
            evidence_refs=[],
            withdrawal_condition="Withdraw if v0.26.3 invokes providers, test-runs providers, bypasses boundaries, adds adapters or runtime analysis dependencies, mutates PIG/memory/persona/policy, renders UI, executes commands, exposes raw data, or uses an LLM judge.",
        )


class WorkbenchProviderBrowserReportService:
    def build_report(self, **kwargs: Any) -> WorkbenchProviderBrowserReport:
        return self.build_all_parts(**kwargs)["report"]

    def build_all_parts(self, **kwargs: Any) -> dict[str, Any]:
        source_service = WorkbenchProviderBrowserPrerequisiteSourceService(
            view_state_available=kwargs.get("view_state_available", True),
            provider_browser_panel_available=kwargs.get("provider_browser_panel_available", True),
            provider_registry_available=kwargs.get("provider_registry_available", True),
            capability_surface_available=kwargs.get("capability_surface_available", True),
            routing_available=kwargs.get("routing_available", True),
            pig_guidance_available=kwargs.get("pig_guidance_available", True),
            invocation_report_available=kwargs.get("invocation_report_available", True),
        )
        sources = source_service.load_sources()
        policy = WorkbenchProviderBrowserPolicyService().build_policy()
        request = WorkbenchProviderBrowserRequestService().build_request(sources, kwargs.get("strictness", "standard"))
        source_view = WorkbenchProviderSourceViewService().build_source_view(sources)
        provider_cards = WorkbenchProviderCardService().build_provider_cards(
            sources.get("provider_registry"),
            sources.get("capability_surfaces") or [],
            sources.get("pig_guidance_refs") or [],
        )
        capability_cards = WorkbenchCapabilityCardService().build_capability_cards(sources.get("capability_surfaces") or [])
        boundary_views = WorkbenchProviderBoundaryViewService().build_boundary_views(sources.get("provider_registry"))
        readiness_views = WorkbenchCapabilityReadinessViewService().build_readiness_views(capability_cards)
        matrix = WorkbenchRouteCompatibilityMatrixService().build_matrix(capability_cards, sources.get("routing_parts"), sources.get("pig_guidance_refs") or [])
        rationale_views = WorkbenchProviderSelectionRationaleViewService().build_rationale_views(sources.get("routing_parts"), sources.get("pig_guidance_refs") or [])
        risk_views = WorkbenchProviderBoundaryRiskViewService().build_risk_views(capability_cards, boundary_views)
        pig_guidance_views = WorkbenchProviderPIGGuidanceViewService().build_pig_guidance_views(sources.get("pig_guidance_refs") or [], capability_cards)
        failure_mode_views = WorkbenchProviderFailureModeViewService().build_failure_mode_views(provider_cards, sources.get("provider_invocation_report_refs") or [])
        human_intervention_points = WorkbenchHumanInterventionPointService().build_human_intervention_points(risk_views, matrix)
        provider_browser_view = WorkbenchProviderBrowserViewService().build_view(
            sources.get("provider_browser_panel_model"),
            source_view,
            provider_cards,
            capability_cards,
            boundary_views,
            readiness_views,
            matrix,
            rationale_views,
            risk_views,
            pig_guidance_views,
            failure_mode_views,
            human_intervention_points,
        )
        inspection_policy = WorkbenchProviderInspectionPolicyService().build_policy()
        inspection_summary = WorkbenchProviderInspectionSummaryService().build_summary(provider_browser_view)
        findings = WorkbenchProviderBrowserFindingService().build_findings(
            sources,
            source_view,
            provider_browser_view,
            kwargs.get("attempt_flags"),
            kwargs.get("extra_findings"),
        )
        report_status = self._report_status(findings, provider_browser_view, inspection_summary)
        report = WorkbenchProviderBrowserReport(
            report_id="workbench_provider_browser_report:v0.26.3",
            created_at=utc_now_iso(),
            provider_browser_policy=policy,
            request=request,
            source_view=source_view,
            provider_browser_view=provider_browser_view,
            inspection_policy=inspection_policy,
            inspection_summary=inspection_summary,
            findings=findings,
            report_status=report_status,
            ready_for_v0_26_4=report_status in {"passed", "warning"},
            provider_browser_view_created=provider_browser_view.view_status in {"ready", "partial"},
            provider_cards_created=bool(provider_cards),
            capability_cards_created=bool(capability_cards),
            boundary_views_created=bool(boundary_views),
            readiness_views_created=bool(readiness_views),
            route_compatibility_matrix_created=bool(matrix.rows),
            selection_rationale_views_created=bool(rationale_views),
            boundary_risk_views_created=bool(risk_views),
            pig_guidance_views_created=bool(pig_guidance_views),
            human_intervention_points_created=bool(human_intervention_points),
            limitations=[
                "v0.26.3 creates provider and capability browser view artifacts only; it does not invoke or test-run providers.",
                "Grok/Codex usability feedback is absorbed only as OCEL-visible refs, candidates, rationale, inspection, and telemetry surfaces.",
            ],
            withdrawal_conditions=[
                "Withdraw if v0.26.3 invokes providers, test-runs providers, bypasses provider boundaries, adds external or vendor adapters, treats PIG as memory/policy mutation/execution, renders UI, executes commands, persists raw data, or uses an LLM judge.",
            ],
        )
        return {
            "report": report,
            "policy": policy,
            "request": request,
            "source_view": source_view,
            "provider_browser_view": provider_browser_view,
            "provider_cards": provider_cards,
            "capability_cards": capability_cards,
            "boundary_views": boundary_views,
            "readiness_views": readiness_views,
            "route_compatibility_matrix": matrix,
            "selection_rationale_views": rationale_views,
            "boundary_risk_views": risk_views,
            "pig_guidance_views": pig_guidance_views,
            "failure_mode_views": failure_mode_views,
            "human_intervention_points": human_intervention_points,
            "inspection_policy": inspection_policy,
            "inspection_summary": inspection_summary,
            "findings": findings,
            "pig_report": self.build_pig_report(),
            "ocpx_projection": self.build_ocpx_projection(),
            "sources": sources,
        }

    def _report_status(
        self,
        findings: list[WorkbenchProviderBrowserFinding],
        view: WorkbenchProviderBrowserView,
        inspection_summary: WorkbenchProviderInspectionSummary,
    ) -> str:
        if any(finding.severity == "critical" for finding in findings) or view.view_status == "blocked":
            return "blocked"
        if any(finding.severity == "error" for finding in findings) or view.view_status == "failed":
            return "failed"
        if any(finding.severity == "warning" for finding in findings) or inspection_summary.summary_status == "partial":
            return "warning"
        return "passed"

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": WORKBENCH_PROVIDER_BROWSER_VERSION,
            "layer": WORKBENCH_PROVIDER_BROWSER_LAYER,
            "subject": "provider_capability_browser",
            "principles": [
                "Provider Browser is not provider invocation.",
                "Capability view is not permission.",
                "Provider boundary view is not boundary bypass.",
                "Provider selection rationale is explainability, not authority.",
                "PIG guidance is not memory.",
                "PIG guidance is not policy mutation.",
                "PIG guidance is not execution.",
                "Human intervention point is not approval by itself.",
                "Route compatibility is not route execution.",
                "Failure mode view is not provider test run.",
            ],
            "safety_boundary": {
                "provider_browser_view_created": "conditional",
                "provider_cards_created": "conditional",
                "capability_cards_created": "conditional",
                "boundary_views_created": "conditional",
                "route_compatibility_matrix_created": "conditional",
                "pig_guidance_views_created": "conditional",
                "human_intervention_points_created": "conditional",
                "actual_ui_rendered": False,
                "panel_rendered": False,
                "provider_invoked": False,
                "provider_test_run_performed": False,
                "provider_boundary_bypassed": False,
                "external_provider_adapter_implemented": False,
                "vendor_adapter_implemented": False,
                "pm4py_runtime_dependency_added": False,
                "ocpa_runtime_dependency_added": False,
                "pig_memory_promoted": False,
                "pig_policy_mutated": False,
                "pig_executed": False,
                "ask_executed": False,
                "final_response_emitted": False,
                "local_command_executed": False,
                "direct_provider_invocation": False,
                "direct_file_access_performed": False,
                "direct_subprocess_performed": False,
                "command_rerun_performed": False,
                "automatic_repair_performed": False,
                "autonomous_loop_started": False,
                "background_execution_started": False,
                "memory_promoted": False,
                "persistent_memory_written": False,
                "persona_mutated": False,
                "schumpeter_split_introduced": False,
                "credential_exposed": False,
                "raw_secret_output": False,
                "raw_provider_output_inline": False,
                "raw_transcript_persisted": False,
                "llm_judge_enabled": False,
            },
            "future_direction": [
                "v0.26.4 evidence / report inspector",
                "v0.26.5 safety gate / approval console",
                "v0.26.6 run dashboard / session monitor",
                "v0.26.7 command surface",
                "v0.26.8 snapshot / OCEL export",
                "v0.27 memory candidate and continuity",
            ],
            "next_step": WORKBENCH_PROVIDER_BROWSER_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "workbench_provider_capability_browser_created",
            "version": WORKBENCH_PROVIDER_BROWSER_VERSION,
            "source_read_models": [
                "WorkbenchViewStateState",
                "WorkbenchPanelRegistryState",
                "InternalProviderRegistryState",
                "InternalProviderCapabilitySurfaceState",
                "AgentToolRoutingState",
                "AgentProviderSelectionState",
                "AgentSafetyGateState",
                "PigGuidanceState",
            ],
            "target_read_models": [
                "WorkbenchProviderBrowserViewState",
                "WorkbenchProviderCardState",
                "WorkbenchCapabilityCardState",
                "WorkbenchProviderBoundaryViewState",
                "WorkbenchCapabilityReadinessState",
                "WorkbenchRouteCompatibilityMatrixState",
                "WorkbenchProviderSelectionRationaleState",
                "WorkbenchProviderBoundaryRiskState",
                "WorkbenchProviderPIGGuidanceState",
                "WorkbenchHumanInterventionPointState",
                "V026ReadinessState",
            ],
            "effect_types": WORKBENCH_PROVIDER_BROWSER_EFFECT_TYPES,
        }


def render_workbench_provider_browser_cli(parts: dict[str, Any], section: str = "view") -> str:
    report: WorkbenchProviderBrowserReport = parts["report"]
    lines = [
        f"version={report.version}",
        f"layer={WORKBENCH_PROVIDER_BROWSER_LAYER}",
        f"provider_browser_view_created={str(report.provider_browser_view_created).lower()}",
        f"provider_cards_created={str(report.provider_cards_created).lower()}",
        f"capability_cards_created={str(report.capability_cards_created).lower()}",
        f"boundary_views_created={str(report.boundary_views_created).lower()}",
        f"readiness_views_created={str(report.readiness_views_created).lower()}",
        f"route_compatibility_matrix_created={str(report.route_compatibility_matrix_created).lower()}",
        f"selection_rationale_views_created={str(report.selection_rationale_views_created).lower()}",
        f"boundary_risk_views_created={str(report.boundary_risk_views_created).lower()}",
        f"pig_guidance_views_created={str(report.pig_guidance_views_created).lower()}",
        f"human_intervention_points_created={str(report.human_intervention_points_created).lower()}",
        f"ready_for_v0_26_4={str(report.ready_for_v0_26_4).lower()}",
        f"ready_for_v0_27={str(report.ready_for_v0_27).lower()}",
        f"actual_ui_rendered={str(report.actual_ui_rendered).lower()}",
        f"panel_rendered={str(report.panel_rendered).lower()}",
        f"provider_invoked={str(report.provider_invoked).lower()}",
        f"provider_test_run_performed={str(report.provider_test_run_performed).lower()}",
        f"provider_boundary_bypassed={str(report.provider_boundary_bypassed).lower()}",
        f"external_provider_adapter_implemented={str(report.external_provider_adapter_implemented).lower()}",
        f"external_agent_adapter_implemented={str(report.external_agent_adapter_implemented).lower()}",
        f"vendor_adapter_implemented={str(report.vendor_adapter_implemented).lower()}",
        f"pm4py_runtime_dependency_added={str(report.pm4py_runtime_dependency_added).lower()}",
        f"ocpa_runtime_dependency_added={str(report.ocpa_runtime_dependency_added).lower()}",
        f"pig_memory_promoted={str(report.pig_memory_promoted).lower()}",
        f"pig_policy_mutated={str(report.pig_policy_mutated).lower()}",
        f"pig_executed={str(report.pig_executed).lower()}",
        f"ask_executed={str(report.ask_executed).lower()}",
        f"final_response_emitted={str(report.final_response_emitted).lower()}",
        f"local_command_executed={str(report.local_command_executed).lower()}",
        f"direct_provider_invocation={str(report.direct_provider_invocation).lower()}",
        f"direct_file_access_performed={str(report.direct_file_access_performed).lower()}",
        f"direct_subprocess_performed={str(report.direct_subprocess_performed).lower()}",
        f"command_rerun_performed={str(report.command_rerun_performed).lower()}",
        f"automatic_repair_performed={str(report.automatic_repair_performed).lower()}",
        f"autonomous_loop_started={str(report.autonomous_loop_started).lower()}",
        f"background_execution_started={str(report.background_execution_started).lower()}",
        f"memory_promoted={str(report.memory_promoted).lower()}",
        f"persistent_memory_written={str(report.persistent_memory_written).lower()}",
        f"persona_mutated={str(report.persona_mutated).lower()}",
        f"schumpeter_split_introduced={str(report.schumpeter_split_introduced).lower()}",
        f"credential_exposed={str(report.credential_exposed).lower()}",
        f"raw_secret_output={str(report.raw_secret_output).lower()}",
        f"raw_provider_output_inline={str(report.raw_provider_output_inline).lower()}",
        f"raw_transcript_persisted={str(report.raw_transcript_persisted).lower()}",
        f"llm_judge_used={str(report.llm_judge_used).lower()}",
        f"next_required_step={report.next_required_step}",
        f"report_status={report.report_status}",
    ]
    if section == "cards":
        lines.extend([f"provider_card={card.provider_id}:{card.provider_type}:provider_invocation_allowed_now={str(card.provider_invocation_allowed_now).lower()}" for card in parts["provider_cards"]])
    elif section == "capabilities":
        lines.extend([f"capability_card={card.capability_id}:{card.provider_id}:executable_now={str(card.executable_now).lower()}" for card in parts["capability_cards"]])
    elif section == "boundaries":
        lines.extend([f"boundary_view={view.provider_id}:{view.boundary_type}:direct_invocation_forbidden={str(view.direct_invocation_forbidden).lower()}" for view in parts["boundary_views"]])
    elif section == "readiness":
        lines.extend([f"readiness_view={view.capability_id}:{view.readiness_status}:not_execution_ready_by_itself={str(view.not_execution_ready_by_itself).lower()}" for view in parts["readiness_views"]])
    elif section == "route-compatibility":
        matrix = parts["route_compatibility_matrix"]
        lines.extend(
            [
                f"compatibility_status={matrix.compatibility_status}",
                f"route_kind_count={matrix.route_kind_count}",
                f"provider_count={matrix.provider_count}",
            ]
        )
    elif section == "rationale":
        lines.extend([f"rationale_view={view.provider_id}:selected={str(view.selected).lower()}:rejected={str(view.rejected).lower()}:deferred={str(view.deferred).lower()}" for view in parts["selection_rationale_views"]])
    elif section == "pig-guidance":
        lines.extend([f"pig_guidance_view={view.pig_guidance_view_id}:pig_guidance_executes={str(view.pig_guidance_executes).lower()}" for view in parts["pig_guidance_views"]])
    elif section == "intervention-points":
        lines.extend([f"human_intervention_point={point.human_intervention_point_id}:approval_created_now={str(point.approval_created_now).lower()}:execution_triggered_now={str(point.execution_triggered_now).lower()}" for point in parts["human_intervention_points"]])
    elif section == "inspect":
        summary = parts["inspection_summary"]
        lines.extend(
            [
                f"inspection_summary_status={summary.summary_status}",
                f"raw_provider_output_included={str(summary.raw_provider_output_included).lower()}",
                f"raw_secret_included={str(summary.raw_secret_included).lower()}",
            ]
        )
    elif section == "report":
        lines.extend([f"finding={finding.severity}:{finding.finding_type}" for finding in report.findings])
    return "\n".join(lines)
