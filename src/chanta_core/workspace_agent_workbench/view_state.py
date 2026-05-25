from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace_agent_workbench.contract import (
    REQUIRED_WORKBENCH_PANEL_SPECS,
    WorkbenchContractReportService,
    WorkbenchPanelContract,
)


WORKBENCH_VIEW_STATE_VERSION = "v0.26.1"
WORKBENCH_VIEW_STATE_VERSION_NAME = "Workbench View State & Panel Model"
WORKBENCH_VIEW_STATE_LAYER = "workspace_agent_workbench"
WORKBENCH_VIEW_STATE_TRACK = "Workspace Agent Workbench"
WORKBENCH_VIEW_STATE_NEXT_STEP = "v0.26.2 Trace Explorer & Pipeline Timeline"

WORKBENCH_VIEW_STATE_IMPLEMENTED_SKILL_IDS = [
    "skill:workbench_view_state_create",
    "skill:workbench_panel_model_view",
]

WORKBENCH_VIEW_STATE_FUTURE_SKILL_IDS = [
    "skill:workbench_trace_explorer_view",
    "skill:workbench_pipeline_timeline_view",
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

WORKBENCH_VIEW_STATE_OBJECT_TYPES = [
    "workbench_view_state_policy",
    "workbench_view_state_request",
    "workbench_panel_model_policy",
    "workbench_panel",
    "workbench_panel_slot",
    "workbench_panel_layout",
    "workbench_panel_registry_view",
    "workbench_selection_policy",
    "workbench_selection_state",
    "workbench_filter_policy",
    "workbench_filter_state",
    "workbench_focus_policy",
    "workbench_focus_state",
    "workbench_navigation_policy",
    "workbench_navigation_state",
    "workbench_session_view_policy",
    "workbench_session_view",
    "workbench_view_state",
    "workbench_view_state_finding",
    "workbench_view_state_report",
    "workspace_agent_workbench_contract",
    "workbench_panel_contract",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

WORKBENCH_VIEW_STATE_EVENT_TYPES = [
    "workbench_view_state_requested",
    "workbench_view_state_policy_created",
    "workbench_panel_model_policy_created",
    "workbench_panel_model_created",
    "workbench_panel_layout_created",
    "workbench_panel_registry_view_created",
    "workbench_selection_policy_created",
    "workbench_selection_state_created",
    "workbench_filter_policy_created",
    "workbench_filter_state_created",
    "workbench_focus_policy_created",
    "workbench_focus_state_created",
    "workbench_navigation_policy_created",
    "workbench_navigation_state_created",
    "workbench_session_view_policy_created",
    "workbench_session_view_created",
    "workbench_view_state_created",
    "workbench_view_state_report_created",
    "workbench_view_state_warning_created",
    "workbench_view_state_blocked",
]

WORKBENCH_VIEW_STATE_RELATION_TYPES = [
    "uses_workbench_contract",
    "uses_workbench_panel_contract",
    "creates_workbench_panel_model",
    "creates_workbench_panel_layout",
    "creates_workbench_panel_registry_view",
    "creates_workbench_selection_state",
    "creates_workbench_filter_state",
    "creates_workbench_focus_state",
    "creates_workbench_navigation_state",
    "creates_workbench_session_view",
    "creates_workbench_view_state",
    "prepares_trace_explorer",
    "defers_trace_explorer_to_v0_26_2",
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
    "not_panel_behavior_implemented",
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

WORKBENCH_VIEW_STATE_EFFECT_TYPES = [
    "read_only_observation",
    "workbench_view_state_created",
    "workbench_panel_model_created",
    "workbench_panel_layout_created",
    "workbench_selection_state_created",
    "workbench_filter_state_created",
    "workbench_focus_state_created",
    "workbench_navigation_state_created",
    "workbench_session_view_created",
    "state_candidate_created",
]

WORKBENCH_VIEW_STATE_FORBIDDEN_EFFECT_TYPES = [
    "workbench_ui_implemented",
    "workbench_panel_rendered",
    "workbench_trace_view_created",
    "workbench_provider_browser_created",
    "workbench_evidence_inspector_created",
    "workbench_approval_candidate_created",
    "workbench_run_dashboard_created",
    "workbench_command_executed",
    "workbench_snapshot_created",
    "workbench_ocel_export_created",
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

REQUIRED_WORKBENCH_VIEW_PANEL_TYPES = [panel_type for panel_type, _ in REQUIRED_WORKBENCH_PANEL_SPECS]
VALID_SLOT_REGIONS = {"left", "right", "center", "bottom", "top", "overlay", "hidden", "unknown"}


def _ref(ref_type: str, ref_id: str, version: str = WORKBENCH_VIEW_STATE_VERSION) -> dict[str, Any]:
    return {"type": ref_type, "id": ref_id, "version": version}


@dataclass
class _Model:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class WorkbenchViewStatePolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_VIEW_STATE_VERSION
    layer: str = WORKBENCH_VIEW_STATE_LAYER
    view_state_enabled: bool = True
    panel_model_enabled: bool = True
    actual_ui_rendering_enabled: bool = False
    browser_server_enabled: bool = False
    dashboard_rendering_enabled: bool = False
    panel_behavior_enabled: bool = False
    ask_execution_enabled: bool = False
    provider_invocation_enabled: bool = False
    local_runtime_execution_enabled: bool = False
    response_emission_enabled: bool = False
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
class WorkbenchViewStateRequest(_Model):
    request_id: str
    contract_report_id: str | None
    workbench_contract_id: str | None
    handoff_packet_id: str | None
    initial_panel_types: list[str]
    initial_selection_refs: list[dict[str, Any]]
    initial_filter_refs: list[dict[str, Any]]
    version: str = WORKBENCH_VIEW_STATE_VERSION
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"


@dataclass
class WorkbenchPanelModelPolicy(_Model):
    policy_id: str
    required_panel_types: list[str]
    version: str = WORKBENCH_VIEW_STATE_VERSION
    panel_contract_required: bool = True
    panel_behavior_deferred: bool = True
    panel_rendering_deferred: bool = True
    panel_source_refs_required: bool = True
    raw_data_dump_forbidden: bool = True
    provider_invocation_forbidden: bool = True
    direct_execution_forbidden: bool = True
    memory_promotion_forbidden: bool = True
    external_adapter_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchPanel(_Model):
    panel_id: str
    panel_type: str
    title: str
    contract_ref: dict[str, Any] | None
    implementation_status: str
    activation_version: str
    allowed_source_types: list[str]
    current_source_refs: list[dict[str, Any]]
    panel_state: str
    supports_selection: bool
    supports_filter: bool
    supports_focus: bool
    supports_navigation: bool
    version: str = WORKBENCH_VIEW_STATE_VERSION
    renders_ui_now: bool = False
    implements_behavior_now: bool = False
    provider_invocation_allowed_now: bool = False
    direct_execution_allowed_now: bool = False
    memory_promotion_allowed_now: bool = False
    external_adapter_allowed_now: bool = False
    raw_transcript_included: bool = False
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchPanelSlot(_Model):
    slot_id: str
    slot_name: str
    panel_id: str | None
    region: str
    order_index: int
    width_weight: float | None
    height_weight: float | None
    visible: bool
    version: str = WORKBENCH_VIEW_STATE_VERSION
    locked: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchPanelLayout(_Model):
    layout_id: str
    layout_name: str
    slots: list[WorkbenchPanelSlot]
    active_panel_ids: list[str]
    hidden_panel_ids: list[str]
    layout_status: str
    version: str = WORKBENCH_VIEW_STATE_VERSION
    renders_ui_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchPanelRegistryView(_Model):
    registry_view_id: str
    panels: list[WorkbenchPanel]
    panel_count: int
    model_only_count: int
    future_behavior_count: int
    disabled_count: int
    blocked_count: int
    registry_status: str
    version: str = WORKBENCH_VIEW_STATE_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSelectionPolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_VIEW_STATE_VERSION
    selection_enabled: bool = True
    selection_is_not_approval: bool = True
    selection_is_not_execution: bool = True
    selection_refs_only: bool = True
    selected_raw_content_forbidden: bool = True
    selected_secret_forbidden: bool = True
    ocel_visible: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSelectionState(_Model):
    selection_state_id: str
    selected_panel_id: str | None
    selected_object_refs: list[dict[str, Any]]
    selected_event_refs: list[dict[str, Any]]
    selected_relation_refs: list[dict[str, Any]]
    selected_evidence_refs: list[dict[str, Any]]
    selected_provider_refs: list[dict[str, Any]]
    selection_count: int
    selection_status: str
    version: str = WORKBENCH_VIEW_STATE_VERSION
    approval_created: bool = False
    execution_triggered: bool = False
    raw_content_included: bool = False
    raw_secret_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchFilterPolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_VIEW_STATE_VERSION
    filter_enabled: bool = True
    filter_is_not_data_deletion: bool = True
    filter_is_not_access_control: bool = True
    filter_refs_only: bool = True
    hidden_data_not_deleted: bool = True
    ocel_visible: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchFilterState(_Model):
    filter_state_id: str
    active_filters: list[dict[str, Any]]
    filter_count: int
    affected_panel_ids: list[str]
    filter_status: str
    version: str = WORKBENCH_VIEW_STATE_VERSION
    data_deleted: bool = False
    access_policy_mutated: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchFocusPolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_VIEW_STATE_VERSION
    focus_enabled: bool = True
    focus_is_not_provider_invocation: bool = True
    focus_is_not_execution: bool = True
    focus_refs_only: bool = True
    ocel_visible: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchFocusState(_Model):
    focus_state_id: str
    focused_panel_id: str | None
    focused_subject_ref: dict[str, Any] | None
    focus_reason: str | None
    focus_status: str
    version: str = WORKBENCH_VIEW_STATE_VERSION
    provider_invoked: bool = False
    execution_triggered: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchNavigationPolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_VIEW_STATE_VERSION
    navigation_enabled: bool = True
    navigation_is_not_background_routing: bool = True
    navigation_is_not_pipeline_execution: bool = True
    navigation_history_enabled: bool = True
    ocel_visible: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchNavigationState(_Model):
    navigation_state_id: str
    current_panel_id: str | None
    previous_panel_refs: list[dict[str, Any]]
    navigation_history: list[dict[str, Any]]
    navigation_status: str
    version: str = WORKBENCH_VIEW_STATE_VERSION
    pipeline_executed: bool = False
    background_routing_started: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSessionViewPolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_VIEW_STATE_VERSION
    session_view_enabled: bool = True
    session_view_is_not_memory_continuity: bool = True
    persistent_memory_write_forbidden: bool = True
    memory_promotion_forbidden: bool = True
    refs_only_by_default: bool = True
    raw_transcript_inline_forbidden: bool = True
    ocel_visible: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSessionView(_Model):
    session_view_id: str
    source_session_refs: list[dict[str, Any]]
    visible_session_count: int
    active_session_ref: dict[str, Any] | None
    session_summary_refs: list[dict[str, Any]]
    session_view_status: str
    version: str = WORKBENCH_VIEW_STATE_VERSION
    memory_continuity_enabled: bool = False
    persistent_memory_written: bool = False
    raw_transcript_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchViewState(_Model):
    view_state_id: str
    created_at: str
    policy: WorkbenchViewStatePolicy
    panel_registry_view: WorkbenchPanelRegistryView
    layout: WorkbenchPanelLayout
    selection_state: WorkbenchSelectionState
    filter_state: WorkbenchFilterState
    focus_state: WorkbenchFocusState
    navigation_state: WorkbenchNavigationState
    session_view: WorkbenchSessionView
    state_status: str
    version: str = WORKBENCH_VIEW_STATE_VERSION
    actual_ui_rendered: bool = False
    panel_behavior_implemented: bool = False
    ask_executed: bool = False
    provider_invoked: bool = False
    local_command_executed: bool = False
    final_response_emitted: bool = False
    memory_promoted: bool = False
    persistent_memory_written: bool = False
    persona_mutated: bool = False
    external_adapter_implemented: bool = False
    raw_transcript_included: bool = False
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchViewStateFinding(_Model):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class WorkbenchViewStateReport(_Model):
    report_id: str
    created_at: str
    view_state: WorkbenchViewState
    findings: list[WorkbenchViewStateFinding]
    report_status: str
    ready_for_v0_26_2: bool
    view_state_created: bool
    panel_model_created: bool
    panel_layout_created: bool
    selection_state_created: bool
    filter_state_created: bool
    focus_state_created: bool
    navigation_state_created: bool
    session_view_created: bool
    version: str = WORKBENCH_VIEW_STATE_VERSION
    ready_for_v0_27: bool = False
    actual_ui_rendered: bool = False
    panel_behavior_implemented: bool = False
    trace_explorer_implemented: bool = False
    provider_browser_implemented: bool = False
    evidence_inspector_implemented: bool = False
    approval_console_implemented: bool = False
    run_dashboard_implemented: bool = False
    command_surface_implemented: bool = False
    snapshot_export_implemented: bool = False
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
    next_required_step: str = WORKBENCH_VIEW_STATE_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.26.2 Trace Explorer & Pipeline Timeline begins or workbench view-state policy changes."


class WorkbenchViewStatePrerequisiteSourceService:
    def __init__(self, contract_available: bool = True, session_refs_available: bool = True) -> None:
        self.contract_available = contract_available
        self.session_refs_available = session_refs_available

    def _source(self, source_id: str, version: str, subject: str, available: bool = True) -> dict[str, Any]:
        return {
            "source_id": source_id,
            "version": version,
            "subject": subject,
            "available": available,
            "read_only": True,
            "refs_only": True,
            "raw_transcript_loaded": False,
            "raw_provider_output_loaded": False,
            "raw_secret_loaded": False,
            "private_full_path_loaded": False,
        }

    def _contract_parts(self) -> dict[str, Any] | None:
        if not self.contract_available:
            return None
        return WorkbenchContractReportService().build_all_parts()

    def load_workbench_contract(self) -> dict[str, Any]:
        parts = self._contract_parts()
        if parts is None:
            return self._source("workspace_agent_workbench_contract:v0.26.0", "v0.26.0", "workbench_contract", False)
        contract = parts["contract"]
        return self._source(contract.contract_id, contract.version, "workbench_contract", True)

    def load_panel_contracts(self) -> list[WorkbenchPanelContract]:
        parts = self._contract_parts()
        if parts is None:
            return []
        return list(parts["panel_contracts"])

    def load_workbench_handoff_packet_if_available(self) -> dict[str, Any]:
        return self._source("agent_workbench_handoff_packet:v0.25.9", "v0.25.9", "workbench_handoff", True)

    def load_agent_surface_trace_refs_if_available(self) -> list[dict[str, Any]]:
        return [_ref("agent_surface_trace", "agent_surface_trace:v0.25.8", "v0.25.8")]

    def load_session_refs_if_available(self) -> list[dict[str, Any]]:
        if not self.session_refs_available:
            return []
        return [_ref("agent_repl_session", "agent_repl_session:v0.25.7:latest", "v0.25.7")]

    def load_skill_registry_if_available(self) -> dict[str, Any]:
        return {
            **self._source("skill_registry:workbench_v0.26.1", WORKBENCH_VIEW_STATE_VERSION, "skill_registry", True),
            "implemented_skill_ids": WORKBENCH_VIEW_STATE_IMPLEMENTED_SKILL_IDS,
            "future_skill_ids": WORKBENCH_VIEW_STATE_FUTURE_SKILL_IDS,
        }

    def load_sources(self) -> dict[str, Any]:
        return {
            "workbench_contract": self.load_workbench_contract(),
            "panel_contracts": self.load_panel_contracts(),
            "workbench_handoff_packet": self.load_workbench_handoff_packet_if_available(),
            "agent_surface_trace_refs": self.load_agent_surface_trace_refs_if_available(),
            "session_refs": self.load_session_refs_if_available(),
            "skill_registry": self.load_skill_registry_if_available(),
        }


class WorkbenchViewStatePolicyService:
    def build_policy(self) -> WorkbenchViewStatePolicy:
        return WorkbenchViewStatePolicy(policy_id="workbench_view_state_policy:v0.26.1")


class WorkbenchPanelModelPolicyService:
    def build_policy(self) -> WorkbenchPanelModelPolicy:
        return WorkbenchPanelModelPolicy(
            policy_id="workbench_panel_model_policy:v0.26.1",
            required_panel_types=REQUIRED_WORKBENCH_VIEW_PANEL_TYPES.copy(),
        )


class WorkbenchPanelService:
    def build_panels_from_contracts(self, panel_contracts: list[WorkbenchPanelContract]) -> list[WorkbenchPanel]:
        by_type = {contract.panel_type: contract for contract in panel_contracts}
        panels: list[WorkbenchPanel] = []
        for panel_type in REQUIRED_WORKBENCH_VIEW_PANEL_TYPES:
            contract = by_type.get(panel_type)
            panel_id = f"workbench_panel:{panel_type}"
            panels.append(
                WorkbenchPanel(
                    panel_id=panel_id,
                    panel_type=panel_type,
                    title=panel_type.replace("_", " ").title(),
                    contract_ref=(
                        _ref("workbench_panel_contract", contract.panel_contract_id, contract.activation_version)
                        if contract is not None
                        else None
                    ),
                    implementation_status="model_only" if contract is not None else "blocked",
                    activation_version=contract.activation_version if contract is not None else "unknown",
                    allowed_source_types=[
                        "workbench_contract_ref",
                        "agent_surface_trace_ref",
                        "agent_telemetry_ref",
                        "agent_session_ref",
                    ],
                    current_source_refs=[_ref("workbench_panel_contract", panel_type, "v0.26.0")] if contract is not None else [],
                    panel_state="expanded" if panel_type in {"trace_explorer", "pipeline_timeline", "evidence_inspector"} else "collapsed",
                    supports_selection=True,
                    supports_filter=panel_type not in {"approval_console", "command_surface", "snapshot_export"},
                    supports_focus=True,
                    supports_navigation=True,
                    evidence_refs=[_ref("workbench_contract", "workspace_agent_workbench_contract:v0.26.0", "v0.26.0")],
                )
            )
        return panels


class WorkbenchPanelLayoutService:
    def build_default_layout(self, panels: list[WorkbenchPanel]) -> WorkbenchPanelLayout:
        region_by_type = {
            "trace_explorer": "center",
            "pipeline_timeline": "bottom",
            "provider_browser": "left",
            "evidence_inspector": "right",
            "safety_gate_view": "right",
            "approval_console": "bottom",
            "run_dashboard": "top",
            "session_monitor": "left",
            "command_surface": "bottom",
            "snapshot_export": "hidden",
            "ocel_projection": "hidden",
            "telemetry_metrics": "top",
        }
        slots: list[WorkbenchPanelSlot] = []
        for index, panel in enumerate(panels):
            region = region_by_type.get(panel.panel_type, "unknown")
            slots.append(
                WorkbenchPanelSlot(
                    slot_id=f"workbench_panel_slot:{panel.panel_type}",
                    slot_name=f"{panel.panel_type}_slot",
                    panel_id=panel.panel_id,
                    region=region,
                    order_index=index,
                    width_weight=1.0 if region in {"left", "center", "right"} else None,
                    height_weight=1.0 if region in {"top", "bottom"} else None,
                    visible=region != "hidden",
                    evidence_refs=[_ref("workbench_panel", panel.panel_id)],
                )
            )
        active = [slot.panel_id for slot in slots if slot.visible and slot.panel_id]
        hidden = [slot.panel_id for slot in slots if not slot.visible and slot.panel_id]
        invalid = [slot for slot in slots if slot.region not in VALID_SLOT_REGIONS]
        return WorkbenchPanelLayout(
            layout_id="workbench_panel_layout:default:v0.26.1",
            layout_name="default_workbench_model_layout",
            slots=slots,
            active_panel_ids=active,
            hidden_panel_ids=hidden,
            layout_status="failed" if invalid else "ready",
            evidence_refs=[_ref("workbench_panel_model_policy", "workbench_panel_model_policy:v0.26.1")],
        )


class WorkbenchPanelRegistryViewService:
    def build_registry_view(self, panels: list[WorkbenchPanel]) -> WorkbenchPanelRegistryView:
        return WorkbenchPanelRegistryView(
            registry_view_id="workbench_panel_registry_view:v0.26.1",
            panels=panels,
            panel_count=len(panels),
            model_only_count=sum(1 for panel in panels if panel.implementation_status == "model_only"),
            future_behavior_count=sum(1 for panel in panels if panel.implementation_status == "future_behavior"),
            disabled_count=sum(1 for panel in panels if panel.implementation_status == "disabled"),
            blocked_count=sum(1 for panel in panels if panel.implementation_status == "blocked"),
            registry_status="blocked" if any(panel.implementation_status == "blocked" for panel in panels) else "ready",
        )


class WorkbenchSelectionPolicyService:
    def build_policy(self) -> WorkbenchSelectionPolicy:
        return WorkbenchSelectionPolicy(policy_id="workbench_selection_policy:v0.26.1")


class WorkbenchSelectionStateService:
    def build_selection_state(
        self,
        request: WorkbenchViewStateRequest,
        panels: list[WorkbenchPanel],
    ) -> WorkbenchSelectionState:
        selected_panel_id = panels[0].panel_id if panels else None
        object_refs = list(request.initial_selection_refs)
        return WorkbenchSelectionState(
            selection_state_id="workbench_selection_state:v0.26.1",
            selected_panel_id=selected_panel_id,
            selected_object_refs=object_refs,
            selected_event_refs=[],
            selected_relation_refs=[],
            selected_evidence_refs=[],
            selected_provider_refs=[],
            selection_count=len(object_refs),
            selection_status="ready" if object_refs else "empty",
        )


class WorkbenchFilterPolicyService:
    def build_policy(self) -> WorkbenchFilterPolicy:
        return WorkbenchFilterPolicy(policy_id="workbench_filter_policy:v0.26.1")


class WorkbenchFilterStateService:
    def build_filter_state(self, request: WorkbenchViewStateRequest, panels: list[WorkbenchPanel]) -> WorkbenchFilterState:
        filters = list(request.initial_filter_refs)
        return WorkbenchFilterState(
            filter_state_id="workbench_filter_state:v0.26.1",
            active_filters=filters,
            filter_count=len(filters),
            affected_panel_ids=[panel.panel_id for panel in panels if panel.supports_filter],
            filter_status="ready" if filters else "empty",
        )


class WorkbenchFocusPolicyService:
    def build_policy(self) -> WorkbenchFocusPolicy:
        return WorkbenchFocusPolicy(policy_id="workbench_focus_policy:v0.26.1")


class WorkbenchFocusStateService:
    def build_focus_state(self, panels: list[WorkbenchPanel]) -> WorkbenchFocusState:
        focused = next((panel for panel in panels if panel.panel_type == "trace_explorer"), panels[0] if panels else None)
        return WorkbenchFocusState(
            focus_state_id="workbench_focus_state:v0.26.1",
            focused_panel_id=focused.panel_id if focused else None,
            focused_subject_ref=_ref("workbench_panel", focused.panel_id) if focused else None,
            focus_reason="default_model_focus" if focused else None,
            focus_status="ready" if focused else "empty",
        )


class WorkbenchNavigationPolicyService:
    def build_policy(self) -> WorkbenchNavigationPolicy:
        return WorkbenchNavigationPolicy(policy_id="workbench_navigation_policy:v0.26.1")


class WorkbenchNavigationStateService:
    def build_navigation_state(self, panels: list[WorkbenchPanel]) -> WorkbenchNavigationState:
        current = panels[0] if panels else None
        return WorkbenchNavigationState(
            navigation_state_id="workbench_navigation_state:v0.26.1",
            current_panel_id=current.panel_id if current else None,
            previous_panel_refs=[],
            navigation_history=[_ref("workbench_panel", current.panel_id)] if current else [],
            navigation_status="ready" if current else "empty",
        )


class WorkbenchSessionViewPolicyService:
    def build_policy(self) -> WorkbenchSessionViewPolicy:
        return WorkbenchSessionViewPolicy(policy_id="workbench_session_view_policy:v0.26.1")


class WorkbenchSessionViewService:
    def build_session_view(self, session_refs: list[dict[str, Any]]) -> WorkbenchSessionView:
        return WorkbenchSessionView(
            session_view_id="workbench_session_view:v0.26.1",
            source_session_refs=session_refs,
            visible_session_count=len(session_refs),
            active_session_ref=session_refs[0] if session_refs else None,
            session_summary_refs=[_ref("agent_session_summary", "agent_session_summary:v0.25.7:latest", "v0.25.7")]
            if session_refs
            else [],
            session_view_status="ready" if session_refs else "empty",
        )


class WorkbenchViewStateService:
    def __init__(self, source_service: WorkbenchViewStatePrerequisiteSourceService | None = None) -> None:
        self.source_service = source_service or WorkbenchViewStatePrerequisiteSourceService()

    def build_request(self) -> WorkbenchViewStateRequest:
        sources = self.source_service.load_sources()
        contract = sources["workbench_contract"]
        panel_types = [contract.panel_type for contract in sources["panel_contracts"]]
        return WorkbenchViewStateRequest(
            request_id="workbench_view_state_request:v0.26.1",
            contract_report_id="workbench_contract_report:v0.26.0" if contract.get("available") else None,
            workbench_contract_id=contract.get("source_id") if contract.get("available") else None,
            handoff_packet_id=sources["workbench_handoff_packet"]["source_id"],
            initial_panel_types=panel_types,
            initial_selection_refs=[_ref("agent_surface_trace", "agent_surface_trace:v0.25.8", "v0.25.8")],
            initial_filter_refs=[_ref("workbench_filter", "filter:all_statuses")],
            source_refs=[contract],
        )

    def build_view_state(self) -> WorkbenchViewState:
        sources = self.source_service.load_sources()
        request = self.build_request()
        panel_contracts = sources["panel_contracts"]
        panels = WorkbenchPanelService().build_panels_from_contracts(panel_contracts)
        registry = WorkbenchPanelRegistryViewService().build_registry_view(panels)
        layout = WorkbenchPanelLayoutService().build_default_layout(panels)
        selection = WorkbenchSelectionStateService().build_selection_state(request, panels)
        filters = WorkbenchFilterStateService().build_filter_state(request, panels)
        focus = WorkbenchFocusStateService().build_focus_state(panels)
        navigation = WorkbenchNavigationStateService().build_navigation_state(panels)
        session = WorkbenchSessionViewService().build_session_view(sources["session_refs"])
        blocked = registry.registry_status == "blocked" or layout.layout_status in {"failed", "blocked"}
        warning = session.session_view_status == "empty"
        return WorkbenchViewState(
            view_state_id="workbench_view_state:v0.26.1",
            created_at=utc_now_iso(),
            policy=WorkbenchViewStatePolicyService().build_policy(),
            panel_registry_view=registry,
            layout=layout,
            selection_state=selection,
            filter_state=filters,
            focus_state=focus,
            navigation_state=navigation,
            session_view=session,
            state_status="blocked" if blocked else "warning" if warning else "ready",
            evidence_refs=[_ref("workbench_contract", "workspace_agent_workbench_contract:v0.26.0", "v0.26.0")],
        )


class WorkbenchViewStateFindingService:
    BLOCKED_FINDINGS = {
        "raw_transcript_inline_attempted",
        "raw_provider_output_inline_attempted",
        "raw_secret_inline_attempted",
        "ui_rendering_attempted",
        "panel_behavior_implemented_too_early",
        "trace_explorer_behavior_attempted",
        "provider_browser_behavior_attempted",
        "evidence_inspector_behavior_attempted",
        "approval_console_behavior_attempted",
        "run_dashboard_behavior_attempted",
        "command_surface_behavior_attempted",
        "snapshot_export_behavior_attempted",
        "ask_execution_attempted",
        "final_response_emission_attempted",
        "provider_invocation_attempted",
        "local_command_execution_attempted",
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
        view_state: WorkbenchViewState | None,
        sources: dict[str, Any],
        attempt_flags: dict[str, bool] | None = None,
        extra_findings: list[str] | None = None,
    ) -> list[WorkbenchViewStateFinding]:
        findings: list[WorkbenchViewStateFinding] = []
        if not sources.get("workbench_contract", {}).get("available", False):
            findings.append(self._finding("warning", "missing_workbench_contract", "v0.26.0 workbench contract source is unavailable."))
        if not sources.get("panel_contracts"):
            findings.append(self._finding("warning", "missing_panel_contract", "No v0.26.0 panel contracts were available."))
        if view_state is None:
            findings.append(self._finding("error", "missing_panel_model", "Workbench view state was not created."))
            return findings
        if not view_state.panel_registry_view.panels:
            findings.append(self._finding("error", "missing_panel_model", "Required panel models are missing."))
        if not view_state.layout.slots:
            findings.append(self._finding("error", "missing_layout", "Workbench layout is missing."))
        if view_state.selection_state is None:
            findings.append(self._finding("error", "missing_selection_state", "Selection state is missing."))
        if view_state.filter_state is None:
            findings.append(self._finding("error", "missing_filter_state", "Filter state is missing."))
        if view_state.focus_state is None:
            findings.append(self._finding("error", "missing_focus_state", "Focus state is missing."))
        if view_state.navigation_state is None:
            findings.append(self._finding("error", "missing_navigation_state", "Navigation state is missing."))
        if view_state.session_view is None:
            findings.append(self._finding("error", "missing_session_view", "Session view is missing."))
        panel_ids = [panel.panel_id for panel in view_state.panel_registry_view.panels]
        if len(panel_ids) != len(set(panel_ids)):
            findings.append(self._finding("error", "duplicate_panel_id", "Duplicate panel ids are present."))
        for slot in view_state.layout.slots:
            if slot.region not in VALID_SLOT_REGIONS or (slot.panel_id and slot.panel_id not in panel_ids):
                findings.append(self._finding("error", "invalid_layout_slot", "Layout contains an invalid slot."))
        for finding_type in extra_findings or []:
            findings.append(self._finding("warning", finding_type, f"{finding_type} was detected."))
        for finding_type, detected in (attempt_flags or {}).items():
            if detected:
                normalized = finding_type if finding_type in self.BLOCKED_FINDINGS else f"{finding_type}_detected"
                findings.append(self._finding("critical", normalized, f"{normalized} was detected."))
        if not findings:
            findings.append(self._finding("info", "ok", "Workbench view state and panel models are ready."))
        return findings

    def _finding(self, severity: str, finding_type: str, message: str) -> WorkbenchViewStateFinding:
        return WorkbenchViewStateFinding(
            finding_id=f"workbench_view_state_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            subject_ref={"id": "workbench_view_state"},
            evidence_refs=[],
            withdrawal_condition="Withdraw if v0.26.1 renders UI, implements panel behavior, executes, mutates memory/persona, exposes raw data, or uses an LLM judge.",
        )


class WorkbenchViewStateReportService:
    def build_report(
        self,
        contract_available: bool = True,
        session_refs_available: bool = True,
        attempt_flags: dict[str, bool] | None = None,
        extra_findings: list[str] | None = None,
    ) -> WorkbenchViewStateReport:
        parts = self.build_all_parts(
            contract_available=contract_available,
            session_refs_available=session_refs_available,
            attempt_flags=attempt_flags,
            extra_findings=extra_findings,
        )
        return parts["report"]

    def build_all_parts(self, **kwargs: Any) -> dict[str, Any]:
        source_service = WorkbenchViewStatePrerequisiteSourceService(
            contract_available=kwargs.get("contract_available", True),
            session_refs_available=kwargs.get("session_refs_available", True),
        )
        sources = source_service.load_sources()
        request = WorkbenchViewStateService(source_service=source_service).build_request()
        view_state = WorkbenchViewStateService(source_service=source_service).build_view_state()
        findings = WorkbenchViewStateFindingService().build_findings(
            view_state,
            sources,
            kwargs.get("attempt_flags"),
            kwargs.get("extra_findings"),
        )
        report_status = self._report_status(findings, view_state)
        report = WorkbenchViewStateReport(
            report_id="workbench_view_state_report:v0.26.1",
            created_at=utc_now_iso(),
            view_state=view_state,
            findings=findings,
            report_status=report_status,
            ready_for_v0_26_2=report_status in {"passed", "warning"},
            view_state_created=True,
            panel_model_created=bool(view_state.panel_registry_view.panels),
            panel_layout_created=bool(view_state.layout.slots),
            selection_state_created=True,
            filter_state_created=True,
            focus_state_created=True,
            navigation_state_created=True,
            session_view_created=True,
            limitations=[
                "v0.26.1 creates view-state and panel-model records only; panel behavior begins in later v0.26 releases.",
                "Source artifacts are represented as sanitized references and raw transcript/provider/secret content is not inlined.",
            ],
            withdrawal_conditions=[
                "Withdraw if v0.26.1 renders UI, implements panel behavior, executes ask/repl, invokes providers, executes commands, promotes memory, mutates persona, implements adapters, persists raw data, or uses an LLM judge.",
            ],
        )
        return {
            "sources": sources,
            "request": request,
            "view_state_policy": view_state.policy,
            "panel_model_policy": WorkbenchPanelModelPolicyService().build_policy(),
            "panels": view_state.panel_registry_view.panels,
            "layout": view_state.layout,
            "panel_registry_view": view_state.panel_registry_view,
            "selection_policy": WorkbenchSelectionPolicyService().build_policy(),
            "selection_state": view_state.selection_state,
            "filter_policy": WorkbenchFilterPolicyService().build_policy(),
            "filter_state": view_state.filter_state,
            "focus_policy": WorkbenchFocusPolicyService().build_policy(),
            "focus_state": view_state.focus_state,
            "navigation_policy": WorkbenchNavigationPolicyService().build_policy(),
            "navigation_state": view_state.navigation_state,
            "session_view_policy": WorkbenchSessionViewPolicyService().build_policy(),
            "session_view": view_state.session_view,
            "view_state": view_state,
            "findings": findings,
            "report": report,
            "pig_report": self.build_pig_report(),
            "ocpx_projection": self.build_ocpx_projection(),
        }

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": WORKBENCH_VIEW_STATE_VERSION,
            "layer": WORKBENCH_VIEW_STATE_LAYER,
            "subject": "workbench_view_state_panel_model",
            "principles": [
                "workbench view model is not rendered UI",
                "panel registry is not panel implementation",
                "panel slot is not visual component",
                "selection state is not approval",
                "filter state is not data deletion",
                "focus state is not provider invocation",
                "navigation state is not background routing",
                "session view is not durable memory",
                "view state may reference artifacts but must not inline raw transcript/provider output/secrets",
            ],
            "safety_boundary": {
                "view_state_created": "conditional",
                "panel_model_created": "conditional",
                "panel_layout_created": "conditional",
                "actual_ui_rendered": False,
                "panel_behavior_implemented": False,
                "trace_explorer_implemented": False,
                "provider_browser_implemented": False,
                "evidence_inspector_implemented": False,
                "approval_console_implemented": False,
                "run_dashboard_implemented": False,
                "command_surface_implemented": False,
                "snapshot_export_implemented": False,
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
            "future_direction": {
                "v0.26.2": "trace explorer and pipeline timeline",
                "v0.26.3": "provider browser",
                "v0.26.4": "evidence inspector",
                "v0.26.5": "approval console",
                "v0.26.6": "run dashboard",
                "v0.26.7": "command surface",
                "v0.26.8": "snapshot / OCEL export",
                "v0.27": "memory candidate and continuity",
            },
            "next_step": WORKBENCH_VIEW_STATE_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "workbench_view_state_panel_model_created",
            "version": WORKBENCH_VIEW_STATE_VERSION,
            "source_read_models": [
                "WorkspaceAgentWorkbenchContractState",
                "WorkbenchPanelContractState",
                "WorkbenchRoadmapBoundaryState",
                "AgentWorkbenchHandoffState",
                "AgentSurfaceTraceState",
            ],
            "target_read_models": [
                "WorkbenchViewStateState",
                "WorkbenchPanelRegistryState",
                "WorkbenchPanelLayoutState",
                "WorkbenchSelectionStateState",
                "WorkbenchFilterStateState",
                "WorkbenchFocusStateState",
                "WorkbenchNavigationStateState",
                "WorkbenchSessionViewState",
                "V026ReadinessState",
            ],
            "effect_types": WORKBENCH_VIEW_STATE_EFFECT_TYPES,
        }

    def _report_status(self, findings: list[WorkbenchViewStateFinding], view_state: WorkbenchViewState) -> str:
        if any(finding.severity == "critical" for finding in findings) or view_state.state_status == "blocked":
            return "blocked"
        if any(finding.severity == "error" for finding in findings):
            return "failed"
        if any(finding.severity == "warning" for finding in findings) or view_state.state_status == "warning":
            return "warning"
        return "passed"


def render_workbench_view_state_cli(parts: dict[str, Any], section: str = "view-state") -> str:
    report: WorkbenchViewStateReport = parts["report"]
    view_state = report.view_state
    lines = [
        f"version={report.version}",
        f"layer={WORKBENCH_VIEW_STATE_LAYER}",
        f"view_state_created={str(report.view_state_created).lower()}",
        f"panel_model_created={str(report.panel_model_created).lower()}",
        f"panel_layout_created={str(report.panel_layout_created).lower()}",
        f"selection_state_created={str(report.selection_state_created).lower()}",
        f"filter_state_created={str(report.filter_state_created).lower()}",
        f"focus_state_created={str(report.focus_state_created).lower()}",
        f"navigation_state_created={str(report.navigation_state_created).lower()}",
        f"session_view_created={str(report.session_view_created).lower()}",
        f"ready_for_v0_26_2={str(report.ready_for_v0_26_2).lower()}",
        f"ready_for_v0_27={str(report.ready_for_v0_27).lower()}",
        f"actual_ui_rendered={str(report.actual_ui_rendered).lower()}",
        f"panel_behavior_implemented={str(report.panel_behavior_implemented).lower()}",
        f"trace_explorer_implemented={str(report.trace_explorer_implemented).lower()}",
        f"provider_browser_implemented={str(report.provider_browser_implemented).lower()}",
        f"evidence_inspector_implemented={str(report.evidence_inspector_implemented).lower()}",
        f"approval_console_implemented={str(report.approval_console_implemented).lower()}",
        f"run_dashboard_implemented={str(report.run_dashboard_implemented).lower()}",
        f"command_surface_implemented={str(report.command_surface_implemented).lower()}",
        f"snapshot_export_implemented={str(report.snapshot_export_implemented).lower()}",
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
    ]
    if section in {"view-state", "view-state-report"}:
        lines.append(f"report_status={report.report_status}")
        lines.append(f"state_status={view_state.state_status}")
        lines.append(f"view_state_id={view_state.view_state_id}")
    elif section == "panels-model":
        registry: WorkbenchPanelRegistryView = parts["panel_registry_view"]
        lines.append(f"panel_count={registry.panel_count}")
        lines.append(f"model_only_count={registry.model_only_count}")
        for panel in registry.panels:
            lines.append(f"- {panel.panel_type}: {panel.implementation_status} renders_ui_now={str(panel.renders_ui_now).lower()}")
    elif section == "layout":
        layout: WorkbenchPanelLayout = parts["layout"]
        lines.append(f"layout_status={layout.layout_status}")
        lines.append(f"active_panel_ids={','.join(layout.active_panel_ids)}")
        lines.append(f"hidden_panel_ids={','.join(layout.hidden_panel_ids)}")
    elif section == "selection":
        selection: WorkbenchSelectionState = parts["selection_state"]
        lines.append(f"selection_status={selection.selection_status}")
        lines.append(f"selection_count={selection.selection_count}")
        lines.append(f"approval_created={str(selection.approval_created).lower()}")
        lines.append(f"execution_triggered={str(selection.execution_triggered).lower()}")
    elif section == "filters":
        filters: WorkbenchFilterState = parts["filter_state"]
        lines.append(f"filter_status={filters.filter_status}")
        lines.append(f"filter_count={filters.filter_count}")
        lines.append(f"data_deleted={str(filters.data_deleted).lower()}")
        lines.append(f"access_policy_mutated={str(filters.access_policy_mutated).lower()}")
    elif section == "focus":
        focus: WorkbenchFocusState = parts["focus_state"]
        lines.append(f"focus_status={focus.focus_status}")
        lines.append(f"focused_panel_id={focus.focused_panel_id or ''}")
        lines.append(f"focus_provider_invoked={str(focus.provider_invoked).lower()}")
        lines.append(f"focus_execution_triggered={str(focus.execution_triggered).lower()}")
    elif section == "navigation":
        navigation: WorkbenchNavigationState = parts["navigation_state"]
        lines.append(f"navigation_status={navigation.navigation_status}")
        lines.append(f"current_panel_id={navigation.current_panel_id or ''}")
        lines.append(f"pipeline_executed={str(navigation.pipeline_executed).lower()}")
        lines.append(f"background_routing_started={str(navigation.background_routing_started).lower()}")
    elif section == "session-view":
        session: WorkbenchSessionView = parts["session_view"]
        lines.append(f"session_view_status={session.session_view_status}")
        lines.append(f"visible_session_count={session.visible_session_count}")
        lines.append(f"memory_continuity_enabled={str(session.memory_continuity_enabled).lower()}")
        lines.append(f"raw_transcript_included={str(session.raw_transcript_included).lower()}")
    return "\n".join(lines)
