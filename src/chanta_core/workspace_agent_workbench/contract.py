from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from chanta_core.agent_surface.usability_consolidation import (
    AGENT_USABILITY_RELEASE_NAME,
    AgentUsabilityConsolidationReportService,
)
from chanta_core.utility.time import utc_now_iso


WORKBENCH_CONTRACT_VERSION = "v0.26.0"
WORKBENCH_CONTRACT_VERSION_NAME = "Workspace Agent Workbench Contract"
WORKBENCH_CONTRACT_KOREAN_NAME = "Workspace Agent Workbench Contract"
WORKBENCH_CONTRACT_LAYER = "workspace_agent_workbench"
WORKBENCH_CONTRACT_TRACK = "Workspace Agent Workbench"
WORKBENCH_CONTRACT_NEXT_STEP = "v0.26.1 Workbench View State & Panel Model"

WORKBENCH_CONTRACT_OBJECT_TYPES = [
    "workspace_agent_workbench_contract",
    "workbench_surface_mode",
    "workbench_panel_contract",
    "workbench_panel_category_policy",
    "workbench_view_permission_policy",
    "workbench_action_boundary_policy",
    "workbench_read_only_inspection_policy",
    "workbench_approval_policy",
    "workbench_command_boundary_policy",
    "workbench_snapshot_policy",
    "workbench_trace_privacy_policy",
    "workbench_ocel_visibility_contract",
    "workbench_roadmap_boundary",
    "workbench_contract_finding",
    "workbench_contract_report",
    "agent_usability_consolidation_report",
    "agent_workbench_handoff_packet",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

WORKBENCH_CONTRACT_EVENT_TYPES = [
    "workbench_contract_requested",
    "workbench_prerequisites_loaded",
    "workbench_surface_modes_declared",
    "workbench_panel_contracts_declared",
    "workbench_panel_category_policy_created",
    "workbench_view_permission_policy_created",
    "workbench_action_boundary_policy_created",
    "workbench_read_only_inspection_policy_created",
    "workbench_approval_policy_created",
    "workbench_command_boundary_policy_created",
    "workbench_snapshot_policy_created",
    "workbench_trace_privacy_policy_created",
    "workbench_ocel_visibility_contract_created",
    "workbench_roadmap_boundary_created",
    "workbench_contract_report_created",
    "workbench_contract_warning_created",
    "workbench_contract_blocked",
]

WORKBENCH_CONTRACT_RELATION_TYPES = [
    "uses_agent_usability_consolidation",
    "uses_workbench_handoff_packet",
    "declares_workbench_contract",
    "declares_workbench_surface_mode",
    "declares_workbench_panel_contract",
    "declares_workbench_view_permission_policy",
    "declares_workbench_action_boundary_policy",
    "declares_workbench_read_only_inspection_policy",
    "declares_workbench_approval_policy",
    "declares_workbench_command_boundary_policy",
    "declares_workbench_snapshot_policy",
    "declares_workbench_trace_privacy_policy",
    "declares_workbench_ocel_visibility_contract",
    "prepares_workbench_view_state",
    "defers_view_state_to_v0_26_1",
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
    "not_workbench_ui_implemented",
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

WORKBENCH_CONTRACT_EFFECT_TYPES = [
    "read_only_observation",
    "workbench_contract_declared",
    "workbench_panel_contract_declared",
    "workbench_policy_declared",
    "state_candidate_created",
]

WORKBENCH_CONTRACT_FORBIDDEN_EFFECT_TYPES = [
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

WORKBENCH_CONTRACT_IMPLEMENTED_SKILL_IDS = [
    "skill:workspace_agent_workbench_contract_view",
]

WORKBENCH_CONTRACT_FUTURE_SKILL_IDS = [
    "skill:workbench_view_state_create",
    "skill:workbench_panel_model_view",
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

REQUIRED_WORKBENCH_PANEL_SPECS = [
    ("trace_explorer", "v0.26.2"),
    ("pipeline_timeline", "v0.26.2"),
    ("provider_browser", "v0.26.3"),
    ("evidence_inspector", "v0.26.4"),
    ("safety_gate_view", "v0.26.5"),
    ("approval_console", "v0.26.5"),
    ("run_dashboard", "v0.26.6"),
    ("session_monitor", "v0.26.6"),
    ("command_surface", "v0.26.7"),
    ("snapshot_export", "v0.26.8"),
    ("ocel_projection", "v0.26.8"),
    ("telemetry_metrics", "v0.26.6"),
]

REQUIRED_WORKBENCH_SURFACE_MODES = [
    ("contract_view", "v0.26.0", "contract_only"),
    ("trace_explorer_future", "v0.26.2", "future_track"),
    ("pipeline_timeline_future", "v0.26.2", "future_track"),
    ("provider_browser_future", "v0.26.3", "future_track"),
    ("evidence_inspector_future", "v0.26.4", "future_track"),
    ("safety_gate_view_future", "v0.26.5", "future_track"),
    ("approval_console_future", "v0.26.5", "future_track"),
    ("run_dashboard_future", "v0.26.6", "future_track"),
    ("session_monitor_future", "v0.26.6", "future_track"),
    ("command_surface_future", "v0.26.7", "future_track"),
    ("snapshot_export_future", "v0.26.8", "future_track"),
    ("blocked", None, "blocked"),
    ("unknown", None, "disabled"),
]


def _ref(ref_type: str, ref_id: str, version: str = WORKBENCH_CONTRACT_VERSION) -> dict[str, Any]:
    return {"type": ref_type, "id": ref_id, "version": version}


@dataclass
class _Model:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class WorkbenchSurfaceMode(_Model):
    mode_id: str
    mode_name: str
    description: str
    user_facing: bool
    inspection_capable_future: bool
    approval_capable_future: bool
    command_capable_future: bool
    snapshot_capable_future: bool
    allowed_outcomes: list[str]
    forbidden_effect_types: list[str]
    introduced_in: str = WORKBENCH_CONTRACT_VERSION
    activation_version: str | None = None
    implementation_status: str = "contract_only"
    execution_capable_future: bool = False
    memory_capable_future: bool = False
    external_adapter_capable_future: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchPanelContract(_Model):
    panel_contract_id: str
    panel_type: str
    activation_version: str
    implementation_status: str
    allowed_source_refs: list[str]
    allowed_read_models: list[str]
    allowed_actions: list[str]
    forbidden_actions: list[str]
    raw_data_dump_forbidden: bool = True
    raw_transcript_forbidden: bool = True
    raw_provider_output_forbidden: bool = True
    raw_secret_output_forbidden: bool = True
    provider_invocation_allowed: bool = False
    direct_execution_allowed: bool = False
    memory_promotion_allowed: bool = False
    external_adapter_allowed: bool = False
    ocel_visible: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchPanelCategoryPolicy(_Model):
    policy_id: str
    allowed_panel_categories: list[str]
    disabled_panel_categories: list[str]
    future_panel_categories: list[str]
    version: str = WORKBENCH_CONTRACT_VERSION
    raw_data_dump_panels_forbidden: bool = True
    direct_execution_panels_forbidden: bool = True
    memory_panels_deferred: bool = True
    external_adapter_panels_deferred: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchViewPermissionPolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_CONTRACT_VERSION
    deny_by_default: bool = True
    read_only_inspection_allowed: bool = True
    trace_view_allowed: bool = True
    provider_capability_view_allowed: bool = True
    evidence_view_allowed: bool = True
    safety_gate_view_allowed: bool = True
    approval_candidate_view_allowed: bool = True
    run_dashboard_view_allowed: bool = True
    snapshot_view_allowed: bool = True
    raw_transcript_view_forbidden: bool = True
    raw_provider_output_view_forbidden: bool = True
    raw_secret_view_forbidden: bool = True
    credential_view_forbidden: bool = True
    private_path_sanitization_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchActionBoundaryPolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_CONTRACT_VERSION
    workbench_action_enabled_future: bool = True
    direct_provider_invocation_forbidden: bool = True
    direct_file_access_forbidden: bool = True
    direct_subprocess_forbidden: bool = True
    direct_local_command_execution_forbidden: bool = True
    command_rerun_forbidden: bool = True
    automatic_repair_forbidden: bool = True
    autonomous_loop_forbidden: bool = True
    background_execution_forbidden: bool = True
    workbench_command_must_use_v025_surface: bool = True
    provider_invocation_must_use_v0255: bool = True
    local_runtime_must_use_v0247_gate: bool = True
    approval_is_not_execution: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchReadOnlyInspectionPolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_CONTRACT_VERSION
    inspection_allowed: bool = True
    inspect_trace_refs: bool = True
    inspect_pipeline_refs: bool = True
    inspect_provider_refs: bool = True
    inspect_evidence_refs: bool = True
    inspect_safety_refs: bool = True
    inspect_telemetry_refs: bool = True
    mutate_inspected_artifacts: bool = False
    raw_transcript_dump_forbidden: bool = True
    raw_provider_output_dump_forbidden: bool = True
    raw_secret_dump_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchApprovalPolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_CONTRACT_VERSION
    approval_candidate_allowed_future: bool = True
    manual_approval_allowed_future: bool = True
    approval_token_allowed_future: bool = True
    approval_is_execution: bool = False
    approval_immediate_execution_forbidden: bool = True
    auto_approval_forbidden: bool = True
    approval_requires_ocel_visibility: bool = True
    approval_requires_policy_ref: bool = True
    approval_requires_user_intent_ref: bool = True
    approval_requires_expiry_or_scope: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchCommandBoundaryPolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_CONTRACT_VERSION
    workbench_command_surface_deferred_to: str = "v0.26.7"
    command_candidates_allowed_future: bool = True
    command_execution_allowed_only_through_existing_surface: bool = True
    ask_command_must_use_v0257: bool = True
    provider_command_must_use_v0255: bool = True
    local_runtime_command_must_use_v0247: bool = True
    direct_command_execution_forbidden: bool = True
    command_rerun_loop_forbidden: bool = True
    automatic_repair_loop_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSnapshotPolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_CONTRACT_VERSION
    snapshot_deferred_to: str = "v0.26.8"
    snapshot_allowed_future: bool = True
    ocel_export_allowed_future: bool = True
    snapshot_is_memory_promotion: bool = False
    persistent_memory_write_forbidden: bool = True
    raw_transcript_export_forbidden: bool = True
    raw_provider_output_export_forbidden: bool = True
    raw_secret_export_forbidden: bool = True
    private_company_material_export_forbidden: bool = True
    reproducibility_metadata_allowed: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchTracePrivacyPolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_CONTRACT_VERSION
    trace_view_allowed_future: bool = True
    raw_transcript_storage_forbidden: bool = True
    raw_provider_output_storage_forbidden: bool = True
    raw_secret_storage_forbidden: bool = True
    credential_storage_forbidden: bool = True
    private_path_sanitization_required: bool = True
    trace_refs_only_by_default: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchOCELVisibilityContract(_Model):
    contract_id: str
    version: str = WORKBENCH_CONTRACT_VERSION
    workbench_interactions_ocel_visible: bool = True
    panel_view_ocel_visible: bool = True
    selection_ocel_visible_future: bool = True
    filter_ocel_visible_future: bool = True
    approval_decision_ocel_visible_future: bool = True
    command_candidate_ocel_visible_future: bool = True
    snapshot_ocel_visible_future: bool = True
    no_raw_secret_in_ocel: bool = True
    no_raw_provider_output_in_ocel: bool = True
    no_raw_transcript_in_ocel: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchRoadmapBoundary(_Model):
    boundary_id: str
    version: str = WORKBENCH_CONTRACT_VERSION
    current_track: str = "v0.26.x Workspace Agent Workbench"
    current_version_scope: str = "v0.26.0 contract_only"
    next_version: str = WORKBENCH_CONTRACT_NEXT_STEP
    trace_explorer_deferred_to: str = "v0.26.2"
    provider_browser_deferred_to: str = "v0.26.3"
    evidence_inspector_deferred_to: str = "v0.26.4"
    approval_console_deferred_to: str = "v0.26.5"
    run_dashboard_deferred_to: str = "v0.26.6"
    command_surface_deferred_to: str = "v0.26.7"
    snapshot_export_deferred_to: str = "v0.26.8"
    memory_continuity_deferred_to: str = "v0.27.x"
    public_alpha_schumpeter_split_deferred_to: str = "v0.28.x"
    external_provider_adapters_deferred_to: str = "v0.29.x+"
    external_agent_dominion_deferred_to: str = "v0.30.x+"
    growthkernel_bridge_deferred: bool = True
    roadmap_status: str = "aligned"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkspaceAgentWorkbenchContract(_Model):
    contract_id: str
    definition: str
    source_release_ref: dict[str, Any] | None
    surface_modes: list[WorkbenchSurfaceMode]
    panel_contracts: list[WorkbenchPanelContract]
    panel_category_policy: WorkbenchPanelCategoryPolicy
    view_permission_policy: WorkbenchViewPermissionPolicy
    action_boundary_policy: WorkbenchActionBoundaryPolicy
    read_only_inspection_policy: WorkbenchReadOnlyInspectionPolicy
    approval_policy: WorkbenchApprovalPolicy
    command_boundary_policy: WorkbenchCommandBoundaryPolicy
    snapshot_policy: WorkbenchSnapshotPolicy
    trace_privacy_policy: WorkbenchTracePrivacyPolicy
    ocel_visibility_contract: WorkbenchOCELVisibilityContract
    roadmap_boundary: WorkbenchRoadmapBoundary
    version: str = WORKBENCH_CONTRACT_VERSION
    layer: str = WORKBENCH_CONTRACT_LAYER
    release_track: str = WORKBENCH_CONTRACT_TRACK
    status: str = "contract_only"
    notes: list[str] = field(default_factory=list)


@dataclass
class WorkbenchContractFinding(_Model):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class WorkbenchContractReport(_Model):
    report_id: str
    created_at: str
    contract: WorkspaceAgentWorkbenchContract
    findings: list[WorkbenchContractFinding]
    report_status: str
    ready_for_v0_26_1: bool
    workbench_contract_created: bool
    version: str = WORKBENCH_CONTRACT_VERSION
    ready_for_v0_27: bool = False
    actual_ui_implemented: bool = False
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
    next_required_step: str = WORKBENCH_CONTRACT_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.26.1 view state and panel model begins or workbench policy changes."


class WorkbenchContractPrerequisiteSourceService:
    def __init__(self, v0259_available: bool = True) -> None:
        self.v0259_available = v0259_available

    def _source(self, source_id: str, version: str, subject: str, available: bool = True) -> dict[str, Any]:
        return {
            "source_id": source_id,
            "version": version,
            "subject": subject,
            "implemented_skill_ids": WORKBENCH_CONTRACT_IMPLEMENTED_SKILL_IDS,
            "future_skill_ids": WORKBENCH_CONTRACT_FUTURE_SKILL_IDS,
            "available": available,
            "read_only": True,
            "raw_transcript_loaded": False,
            "raw_provider_output_loaded": False,
            "raw_secret_loaded": False,
            "private_full_path_loaded": False,
        }

    def _v0259_parts(self) -> dict[str, Any] | None:
        if not self.v0259_available:
            return None
        return AgentUsabilityConsolidationReportService().build_all_parts()

    def load_v0259_consolidation_report(self) -> dict[str, Any]:
        parts = self._v0259_parts()
        if parts is None:
            return self._source("agent_usability_consolidation_report:v0.25.9", "v0.25.9", "consolidation_report", False)
        report = parts["report"]
        return self._source(report.report_id, report.version, "consolidation_report", True)

    def load_v0259_release_manifest(self) -> dict[str, Any]:
        parts = self._v0259_parts()
        if parts is None:
            return self._source("agent_surface_release_manifest:v0.25.9", "v0.25.9", "release_manifest", False)
        manifest = parts["release_manifest"]
        return self._source(manifest.manifest_id, manifest.release_version, "release_manifest", True)

    def load_v026_readiness_report(self) -> dict[str, Any]:
        parts = self._v0259_parts()
        if parts is None:
            return self._source("agent_v026_readiness_report:v0.25.9", "v0.25.9", "v026_readiness", False)
        readiness = parts["v026_readiness_report"]
        return self._source(readiness.report_id, readiness.version, "v026_readiness", True)

    def load_workbench_handoff_packet(self) -> dict[str, Any]:
        parts = self._v0259_parts()
        if parts is None:
            return self._source("agent_workbench_handoff_packet:v0.25.9", "v0.25.9", "workbench_handoff", False)
        handoff = parts["workbench_handoff_packet"]
        return self._source(handoff.handoff_packet_id, handoff.version, "workbench_handoff", True)

    def load_agent_surface_contract_if_available(self) -> dict[str, Any]:
        return self._source("agent_surface_contract:v0.25.0", "v0.25.0", "agent_surface_contract", True)

    def load_trace_telemetry_report_if_available(self) -> dict[str, Any]:
        return self._source("agent_trace_telemetry_report:v0.25.8", "v0.25.8", "trace_telemetry_report", True)

    def load_skill_registry_if_available(self) -> dict[str, Any]:
        return self._source("skill_registry:agent_surface_v0.25", "v0.25.9", "skill_registry", True)

    def load_provider_registry_if_available(self) -> dict[str, Any]:
        return self._source("provider_registry:internal_provider_v0.24", "v0.24.9", "provider_registry", True)

    def load_sources(self) -> dict[str, dict[str, Any]]:
        return {
            "consolidation_report": self.load_v0259_consolidation_report(),
            "release_manifest": self.load_v0259_release_manifest(),
            "v026_readiness": self.load_v026_readiness_report(),
            "workbench_handoff": self.load_workbench_handoff_packet(),
            "agent_surface_contract": self.load_agent_surface_contract_if_available(),
            "trace_telemetry_report": self.load_trace_telemetry_report_if_available(),
            "skill_registry": self.load_skill_registry_if_available(),
            "provider_registry": self.load_provider_registry_if_available(),
        }


class WorkbenchSurfaceModeService:
    def build_surface_modes(self) -> list[WorkbenchSurfaceMode]:
        modes: list[WorkbenchSurfaceMode] = []
        for mode_name, activation_version, status in REQUIRED_WORKBENCH_SURFACE_MODES:
            approval_future = mode_name == "approval_console_future"
            command_future = mode_name == "command_surface_future"
            snapshot_future = mode_name == "snapshot_export_future"
            inspection_future = mode_name not in {"blocked", "unknown"}
            modes.append(
                WorkbenchSurfaceMode(
                    mode_id=f"workbench_surface_mode:{mode_name}",
                    mode_name=mode_name,
                    description=f"{mode_name} is declared as a v0.26 contract surface, not an implementation.",
                    activation_version=activation_version,
                    implementation_status=status,
                    user_facing=mode_name != "unknown",
                    inspection_capable_future=inspection_future,
                    approval_capable_future=approval_future,
                    command_capable_future=command_future,
                    snapshot_capable_future=snapshot_future,
                    allowed_outcomes=["read_only_observation", "state_candidate_created"],
                    forbidden_effect_types=WORKBENCH_CONTRACT_FORBIDDEN_EFFECT_TYPES,
                    evidence_refs=[_ref("roadmap_boundary", "workbench_roadmap_boundary:v0.26.0")],
                )
            )
        return modes


class WorkbenchPanelContractService:
    def build_panel_contracts(self) -> list[WorkbenchPanelContract]:
        panels: list[WorkbenchPanelContract] = []
        for panel_type, activation_version in REQUIRED_WORKBENCH_PANEL_SPECS:
            allowed_actions = ["view_ref", "select_ref", "filter_ref"]
            if panel_type == "command_surface":
                allowed_actions = ["create_command_candidate_future", "view_command_candidate_ref"]
            if panel_type == "snapshot_export":
                allowed_actions = ["view_snapshot_candidate_future"]
            panels.append(
                WorkbenchPanelContract(
                    panel_contract_id=f"workbench_panel_contract:{panel_type}",
                    panel_type=panel_type,
                    activation_version=activation_version,
                    implementation_status="future_track",
                    allowed_source_refs=[
                        "AgentUsabilityReleaseState",
                        "AgentV026ReadinessState",
                        "AgentWorkbenchHandoffState",
                        "AgentSurfaceTraceState",
                        "AgentUsabilityTelemetryReportState",
                    ],
                    allowed_read_models=[
                        "WorkspaceAgentWorkbenchContractState",
                        "WorkbenchSurfaceModeState",
                        "WorkbenchPanelContractState",
                        "WorkbenchPermissionPolicyState",
                    ],
                    allowed_actions=allowed_actions,
                    forbidden_actions=[
                        "render_actual_panel",
                        "dump_raw_transcript",
                        "dump_raw_provider_output",
                        "invoke_provider",
                        "execute_local_command",
                        "promote_memory",
                        "call_external_adapter",
                    ],
                    evidence_refs=[_ref("workbench_panel_spec", panel_type)],
                )
            )
        return panels


class WorkbenchPanelCategoryPolicyService:
    def build_policy(self) -> WorkbenchPanelCategoryPolicy:
        return WorkbenchPanelCategoryPolicy(
            policy_id="workbench_panel_category_policy:v0.26.0",
            allowed_panel_categories=["contract", "read_only_inspection", "policy", "roadmap"],
            disabled_panel_categories=["raw_data_dump", "direct_execution", "memory", "external_adapter"],
            future_panel_categories=[panel_type for panel_type, _ in REQUIRED_WORKBENCH_PANEL_SPECS],
        )


class WorkbenchViewPermissionPolicyService:
    def build_policy(self) -> WorkbenchViewPermissionPolicy:
        return WorkbenchViewPermissionPolicy(policy_id="workbench_view_permission_policy:v0.26.0")


class WorkbenchActionBoundaryPolicyService:
    def build_policy(self) -> WorkbenchActionBoundaryPolicy:
        return WorkbenchActionBoundaryPolicy(policy_id="workbench_action_boundary_policy:v0.26.0")


class WorkbenchReadOnlyInspectionPolicyService:
    def build_policy(self) -> WorkbenchReadOnlyInspectionPolicy:
        return WorkbenchReadOnlyInspectionPolicy(policy_id="workbench_read_only_inspection_policy:v0.26.0")


class WorkbenchApprovalPolicyService:
    def build_policy(self) -> WorkbenchApprovalPolicy:
        return WorkbenchApprovalPolicy(policy_id="workbench_approval_policy:v0.26.0")


class WorkbenchCommandBoundaryPolicyService:
    def build_policy(self) -> WorkbenchCommandBoundaryPolicy:
        return WorkbenchCommandBoundaryPolicy(policy_id="workbench_command_boundary_policy:v0.26.0")


class WorkbenchSnapshotPolicyService:
    def build_policy(self) -> WorkbenchSnapshotPolicy:
        return WorkbenchSnapshotPolicy(policy_id="workbench_snapshot_policy:v0.26.0")


class WorkbenchTracePrivacyPolicyService:
    def build_policy(self) -> WorkbenchTracePrivacyPolicy:
        return WorkbenchTracePrivacyPolicy(policy_id="workbench_trace_privacy_policy:v0.26.0")


class WorkbenchOCELVisibilityContractService:
    def build_contract(self) -> WorkbenchOCELVisibilityContract:
        return WorkbenchOCELVisibilityContract(contract_id="workbench_ocel_visibility_contract:v0.26.0")


class WorkbenchRoadmapBoundaryService:
    def build_boundary(self) -> WorkbenchRoadmapBoundary:
        return WorkbenchRoadmapBoundary(boundary_id="workbench_roadmap_boundary:v0.26.0")


class WorkbenchContractService:
    def __init__(self, source_service: WorkbenchContractPrerequisiteSourceService | None = None) -> None:
        self.source_service = source_service or WorkbenchContractPrerequisiteSourceService()

    def build_contract(self) -> WorkspaceAgentWorkbenchContract:
        sources = self.source_service.load_sources()
        return WorkspaceAgentWorkbenchContract(
            contract_id="workspace_agent_workbench_contract:v0.26.0",
            definition=(
                "v0.26.0 declares the contract-only Workspace Agent Workbench layer "
                "for read-only inspection, approval candidates, and future bounded command surfaces."
            ),
            source_release_ref=sources["release_manifest"],
            surface_modes=WorkbenchSurfaceModeService().build_surface_modes(),
            panel_contracts=WorkbenchPanelContractService().build_panel_contracts(),
            panel_category_policy=WorkbenchPanelCategoryPolicyService().build_policy(),
            view_permission_policy=WorkbenchViewPermissionPolicyService().build_policy(),
            action_boundary_policy=WorkbenchActionBoundaryPolicyService().build_policy(),
            read_only_inspection_policy=WorkbenchReadOnlyInspectionPolicyService().build_policy(),
            approval_policy=WorkbenchApprovalPolicyService().build_policy(),
            command_boundary_policy=WorkbenchCommandBoundaryPolicyService().build_policy(),
            snapshot_policy=WorkbenchSnapshotPolicyService().build_policy(),
            trace_privacy_policy=WorkbenchTracePrivacyPolicyService().build_policy(),
            ocel_visibility_contract=WorkbenchOCELVisibilityContractService().build_contract(),
            roadmap_boundary=WorkbenchRoadmapBoundaryService().build_boundary(),
            notes=[
                "Workbench contract is not UI implementation.",
                "Workbench approval is not execution.",
                "Workbench snapshot is not memory promotion.",
            ],
        )

    def view_contract(self) -> WorkspaceAgentWorkbenchContract:
        return self.build_contract()


class WorkbenchContractFindingService:
    BLOCKED_FINDINGS = {
        "workbench_ui_implemented_too_early",
        "trace_explorer_implemented_too_early",
        "provider_browser_implemented_too_early",
        "evidence_inspector_implemented_too_early",
        "approval_console_implemented_too_early",
        "run_dashboard_implemented_too_early",
        "command_surface_implemented_too_early",
        "snapshot_export_implemented_too_early",
        "ask_execution_attempted",
        "provider_invocation_attempted",
        "direct_execution_attempted",
        "memory_promotion_attempted",
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
        contract: WorkspaceAgentWorkbenchContract | None,
        sources: dict[str, dict[str, Any]],
        attempt_flags: dict[str, bool] | None = None,
    ) -> list[WorkbenchContractFinding]:
        findings: list[WorkbenchContractFinding] = []
        if not sources.get("release_manifest", {}).get("available", False):
            findings.append(
                self._finding(
                    "warning",
                    "missing_v0259_release",
                    "v0.25.9 release manifest is unavailable; contract remains report-derived with warning status.",
                )
            )
        if contract is None:
            findings.append(self._finding("error", "missing_workbench_contract", "Workbench contract is missing."))
            return findings
        section_checks = {
            "missing_panel_contract": bool(contract.panel_contracts),
            "missing_view_permission_policy": contract.view_permission_policy is not None,
            "missing_action_boundary_policy": contract.action_boundary_policy is not None,
            "missing_read_only_inspection_policy": contract.read_only_inspection_policy is not None,
            "missing_approval_policy": contract.approval_policy is not None,
            "missing_snapshot_policy": contract.snapshot_policy is not None,
            "missing_ocel_visibility_contract": contract.ocel_visibility_contract is not None,
        }
        for finding_type, present in section_checks.items():
            if not present:
                findings.append(self._finding("error", finding_type, f"{finding_type} is missing."))
        for finding_type, detected in (attempt_flags or {}).items():
            if detected:
                normalized = finding_type if finding_type in self.BLOCKED_FINDINGS else f"{finding_type}_detected"
                findings.append(self._finding("critical", normalized, f"{normalized} was detected."))
        if not findings:
            findings.append(self._finding("info", "ok", "Workbench contract is contract-only and policy-complete."))
        return findings

    def _finding(self, severity: str, finding_type: str, message: str) -> WorkbenchContractFinding:
        return WorkbenchContractFinding(
            finding_id=f"workbench_contract_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            subject_ref={"id": "workspace_agent_workbench_contract"},
            evidence_refs=[],
            withdrawal_condition="Withdraw if the v0.26.0 workbench contract policy, v0.25.9 release source, or implementation boundary changes.",
        )


class WorkbenchContractReportService:
    def build_report(
        self,
        v0259_available: bool = True,
        attempt_flags: dict[str, bool] | None = None,
    ) -> WorkbenchContractReport:
        source_service = WorkbenchContractPrerequisiteSourceService(v0259_available=v0259_available)
        sources = source_service.load_sources()
        contract = WorkbenchContractService(source_service=source_service).build_contract()
        findings = WorkbenchContractFindingService().build_findings(contract, sources, attempt_flags)
        report_status = self._report_status(findings)
        return WorkbenchContractReport(
            report_id="workbench_contract_report:v0.26.0",
            created_at=utc_now_iso(),
            contract=contract,
            findings=findings,
            report_status=report_status,
            ready_for_v0_26_1=report_status in {"passed", "warning"},
            workbench_contract_created=True,
            limitations=[
                "v0.26.0 declares the workbench contract only; actual panel state and rendering begin in later v0.26 releases.",
                "v0.25.9 sources are consumed as sanitized report references, not raw transcripts or provider outputs.",
            ],
            withdrawal_conditions=[
                "Withdraw if v0.26.0 renders actual UI, executes ask/repl, emits responses, invokes providers, runs commands, promotes memory, implements external adapters, persists raw data, or uses an LLM judge.",
            ],
        )

    def build_all_parts(self, **kwargs: Any) -> dict[str, Any]:
        source_service = WorkbenchContractPrerequisiteSourceService(v0259_available=kwargs.get("v0259_available", True))
        sources = source_service.load_sources()
        contract = WorkbenchContractService(source_service=source_service).build_contract()
        findings = WorkbenchContractFindingService().build_findings(contract, sources, kwargs.get("attempt_flags"))
        report_status = self._report_status(findings)
        report = WorkbenchContractReport(
            report_id="workbench_contract_report:v0.26.0",
            created_at=utc_now_iso(),
            contract=contract,
            findings=findings,
            report_status=report_status,
            ready_for_v0_26_1=report_status in {"passed", "warning"},
            workbench_contract_created=True,
            limitations=[
                "v0.26.0 declares the workbench contract only; actual panel state and rendering begin in later v0.26 releases.",
                "v0.25.9 sources are consumed as sanitized report references, not raw transcripts or provider outputs.",
            ],
            withdrawal_conditions=[
                "Withdraw if v0.26.0 renders actual UI, executes ask/repl, emits responses, invokes providers, runs commands, promotes memory, implements external adapters, persists raw data, or uses an LLM judge.",
            ],
        )
        return {
            "sources": sources,
            "contract": contract,
            "surface_modes": contract.surface_modes,
            "panel_contracts": contract.panel_contracts,
            "panel_category_policy": contract.panel_category_policy,
            "view_permission_policy": contract.view_permission_policy,
            "action_boundary_policy": contract.action_boundary_policy,
            "read_only_inspection_policy": contract.read_only_inspection_policy,
            "approval_policy": contract.approval_policy,
            "command_boundary_policy": contract.command_boundary_policy,
            "snapshot_policy": contract.snapshot_policy,
            "trace_privacy_policy": contract.trace_privacy_policy,
            "ocel_visibility_contract": contract.ocel_visibility_contract,
            "roadmap_boundary": contract.roadmap_boundary,
            "findings": findings,
            "report": report,
            "pig_report": self.build_pig_report(),
            "ocpx_projection": self.build_ocpx_projection(),
        }

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": WORKBENCH_CONTRACT_VERSION,
            "layer": WORKBENCH_CONTRACT_LAYER,
            "subject": "workspace_agent_workbench_contract",
            "principles": [
                "workbench contract is not UI implementation",
                "workbench surface is not autonomous execution",
                "workbench panel contract is not panel rendering",
                "workbench approval is not execution",
                "workbench command is not direct tool call",
                "workbench snapshot is not memory promotion",
                "workbench OCEL visibility is not raw transcript export",
                "workbench must increase human control, not create bypass paths",
            ],
            "safety_boundary": {
                "actual_ui_implemented": False,
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
                "v0.26.1": "view state and panel model",
                "v0.26.2": "trace explorer",
                "v0.26.3": "provider browser",
                "v0.26.4": "evidence inspector",
                "v0.26.5": "approval console",
                "v0.26.6": "run dashboard",
                "v0.26.7": "command surface",
                "v0.26.8": "snapshot / OCEL export",
                "v0.27": "memory candidate and continuity",
                "v0.29+": "external provider/agent adapters",
                "v0.30+": "external agent dominion bridge",
            },
            "next_step": WORKBENCH_CONTRACT_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "workspace_agent_workbench_contract_declared",
            "version": WORKBENCH_CONTRACT_VERSION,
            "source_read_models": [
                "AgentUsabilityReleaseState",
                "AgentV026ReadinessState",
                "AgentWorkbenchHandoffState",
                "AgentSurfaceTraceState",
                "AgentUsabilityTelemetryReportState",
            ],
            "target_read_models": [
                "WorkspaceAgentWorkbenchContractState",
                "WorkbenchSurfaceModeState",
                "WorkbenchPanelContractState",
                "WorkbenchPermissionPolicyState",
                "WorkbenchActionBoundaryState",
                "WorkbenchApprovalPolicyState",
                "WorkbenchSnapshotPolicyState",
                "WorkbenchRoadmapBoundaryState",
                "V026ReadinessState",
            ],
            "effect_types": WORKBENCH_CONTRACT_EFFECT_TYPES,
        }

    def _report_status(self, findings: list[WorkbenchContractFinding]) -> str:
        if any(finding.severity == "critical" for finding in findings):
            return "blocked"
        if any(finding.severity == "error" for finding in findings):
            return "failed"
        if any(finding.severity == "warning" for finding in findings):
            return "warning"
        return "passed"


def render_workbench_contract_cli(parts: dict[str, Any], section: str = "contract") -> str:
    report: WorkbenchContractReport = parts["report"]
    contract = report.contract
    lines = [
        f"version={report.version}",
        f"layer={contract.layer}",
        f"status={contract.status}",
        f"ready_for_v0_26_1={str(report.ready_for_v0_26_1).lower()}",
        f"ready_for_v0_27={str(report.ready_for_v0_27).lower()}",
        f"actual_ui_implemented={str(report.actual_ui_implemented).lower()}",
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
    if section in {"contract", "contract-report"}:
        lines.append(f"report_status={report.report_status}")
        lines.append(f"contract_id={contract.contract_id}")
        lines.append(f"release_track={contract.release_track}")
        lines.append(f"source_release={AGENT_USABILITY_RELEASE_NAME}")
    elif section == "modes":
        for mode in parts["surface_modes"]:
            lines.append(f"- {mode.mode_name}: {mode.implementation_status} activation={mode.activation_version or 'none'}")
    elif section == "panels":
        for panel in parts["panel_contracts"]:
            lines.append(f"- {panel.panel_type}: {panel.implementation_status} activation={panel.activation_version}")
    elif section == "permissions":
        policy: WorkbenchViewPermissionPolicy = parts["view_permission_policy"]
        lines.append(f"deny_by_default={str(policy.deny_by_default).lower()}")
        lines.append(f"read_only_inspection_allowed={str(policy.read_only_inspection_allowed).lower()}")
        lines.append(f"raw_transcript_view_forbidden={str(policy.raw_transcript_view_forbidden).lower()}")
    elif section == "action-boundary":
        policy: WorkbenchActionBoundaryPolicy = parts["action_boundary_policy"]
        lines.append(f"workbench_command_must_use_v025_surface={str(policy.workbench_command_must_use_v025_surface).lower()}")
        lines.append(f"provider_invocation_must_use_v0255={str(policy.provider_invocation_must_use_v0255).lower()}")
        lines.append(f"local_runtime_must_use_v0247_gate={str(policy.local_runtime_must_use_v0247_gate).lower()}")
    elif section == "approval-policy":
        policy: WorkbenchApprovalPolicy = parts["approval_policy"]
        lines.append(f"approval_is_execution={str(policy.approval_is_execution).lower()}")
        lines.append(f"approval_immediate_execution_forbidden={str(policy.approval_immediate_execution_forbidden).lower()}")
        lines.append(f"approval_requires_ocel_visibility={str(policy.approval_requires_ocel_visibility).lower()}")
    elif section == "snapshot-policy":
        policy: WorkbenchSnapshotPolicy = parts["snapshot_policy"]
        lines.append(f"snapshot_deferred_to={policy.snapshot_deferred_to}")
        lines.append(f"snapshot_is_memory_promotion={str(policy.snapshot_is_memory_promotion).lower()}")
        lines.append(f"raw_transcript_export_forbidden={str(policy.raw_transcript_export_forbidden).lower()}")
    elif section == "roadmap-boundary":
        boundary: WorkbenchRoadmapBoundary = parts["roadmap_boundary"]
        lines.append(f"roadmap_status={boundary.roadmap_status}")
        lines.append(f"current_track={boundary.current_track}")
        lines.append(f"next_version={boundary.next_version}")
    return "\n".join(lines)
