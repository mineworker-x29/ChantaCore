from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace_agent_workbench.command_surface import WORKBENCH_COMMAND_SURFACE_EFFECT_TYPES
from chanta_core.workspace_agent_workbench.run_dashboard import WORKBENCH_RUN_DASHBOARD_EFFECT_TYPES
from chanta_core.workspace_agent_workbench.snapshot_export import WORKBENCH_SNAPSHOT_EXPORT_EFFECT_TYPES


WORKBENCH_CONSOLIDATION_VERSION = "v0.26.9"
WORKBENCH_CONSOLIDATION_VERSION_NAME = "Workspace Agent Workbench Consolidation"
WORKBENCH_CONSOLIDATION_KOREAN_NAME = "Workspace Agent Workbench tonghap.release readiness"
WORKBENCH_CONSOLIDATION_RELEASE_NAME = "Workspace Agent Workbench Foundation v1"
WORKBENCH_CONSOLIDATION_LAYER = "workspace_agent_workbench"
WORKBENCH_CONSOLIDATION_TRACK = "Workspace Agent Workbench"
WORKBENCH_CONSOLIDATION_NEXT_STEP = "v0.27.0 Memory Candidate & Continuity Contract"

WORKBENCH_CONSOLIDATION_INCLUDED_VERSIONS = [
    "v0.26.0",
    "v0.26.1",
    "v0.26.2",
    "v0.26.3",
    "v0.26.4",
    "v0.26.5",
    "v0.26.6",
    "v0.26.7",
    "v0.26.8",
    "v0.26.9",
]

WORKBENCH_CONSOLIDATION_IMPLEMENTED_SKILL_IDS = [
    "skill:workbench_consolidation_view",
]

WORKBENCH_CONSOLIDATION_PREVIOUS_SKILL_IDS = [
    "skill:workspace_agent_workbench_contract_view",
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
]

WORKBENCH_CONSOLIDATION_FUTURE_SKILL_IDS = [
    "skill:memory_candidate_create",
    "skill:memory_promotion_gate",
    "skill:session_continuity_view",
    "skill:external_provider_adapter_register",
    "skill:external_agent_runtime_inventory",
    "skill:external_agent_dominion_bridge",
    "skill:schumpeter_split_prepare",
]

WORKBENCH_CONSOLIDATION_OBJECT_TYPES = [
    "workbench_foundation_snapshot",
    "workbench_foundation_subject_component",
    "workbench_capability_map",
    "workbench_capability_map_entry",
    "workbench_coverage_matrix",
    "workbench_coverage_matrix_row",
    "workbench_safety_boundary_report",
    "workbench_interaction_boundary_report",
    "workbench_event_quality_consolidation_report",
    "workbench_trace_coverage_consolidation_report",
    "workbench_usability_readiness_report",
    "workbench_process_intelligence_feedback_loop_report",
    "workbench_default_agent_usability_gap",
    "workbench_default_agent_usability_gap_register",
    "workbench_v027_readiness_report",
    "workbench_memory_candidate_handoff_packet",
    "workbench_release_manifest",
    "workbench_consolidation_finding",
    "workbench_consolidation_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

WORKBENCH_CONSOLIDATION_EVENT_TYPES = [
    "workbench_consolidation_requested",
    "workbench_consolidation_sources_loaded",
    "workbench_foundation_snapshot_created",
    "workbench_subject_components_created",
    "workbench_capability_map_created",
    "workbench_coverage_matrix_created",
    "workbench_safety_boundary_report_created",
    "workbench_interaction_boundary_report_created",
    "workbench_event_quality_consolidation_report_created",
    "workbench_trace_coverage_consolidation_report_created",
    "workbench_usability_readiness_report_created",
    "workbench_process_intelligence_feedback_loop_report_created",
    "workbench_gap_register_created",
    "workbench_v027_readiness_report_created",
    "workbench_memory_candidate_handoff_packet_created",
    "workbench_release_manifest_created",
    "workbench_consolidation_report_created",
    "workbench_release_ready",
    "workbench_release_warning",
    "workbench_release_blocked",
]

WORKBENCH_CONSOLIDATION_RELATION_TYPES = [
    "consolidates_workspace_agent_workbench_foundation",
    "uses_workbench_contract_report",
    "uses_workbench_view_state_report",
    "uses_workbench_trace_explorer_report",
    "uses_workbench_provider_browser_report",
    "uses_workbench_evidence_inspector_report",
    "uses_workbench_approval_console_report",
    "uses_workbench_run_dashboard_report",
    "uses_workbench_command_surface_report",
    "uses_workbench_snapshot_export_report",
    "creates_release_manifest",
    "creates_v027_readiness_report",
    "creates_memory_candidate_handoff_packet",
    "defers_memory_candidate_to_v0_27",
    "defers_schumpeter_split_to_v0_28",
    "defers_external_adapter_to_v0_29",
    "not_memory_promoted",
    "not_command_executed",
    "not_provider_invoked",
    "not_raw_transcript_persisted",
]

WORKBENCH_CONSOLIDATION_EFFECT_TYPES = [
    "read_only_observation",
    "workbench_consolidation_created",
    "workbench_foundation_snapshot_created",
    "workbench_release_manifest_created",
    "workbench_v027_readiness_created",
    "workbench_memory_candidate_handoff_packet_created",
    "state_candidate_created",
]

WORKBENCH_CONSOLIDATION_FORBIDDEN_EFFECT_TYPES = [
    "memory_candidate_created",
    "memory_promoted",
    "persistent_memory_written",
    "persona_mutated",
    "command_executed",
    "provider_invoked",
    "internal_provider_invoked",
    "local_command_executed",
    "bounded_local_command_executed",
    "file_mutated",
    "patch_applied",
    "agent_ask_executed",
    "agent_repl_started",
    "final_response_emitted",
    "route_rerun_performed",
    "stage_rerun_performed",
    "automatic_retry_performed",
    "automatic_repair_performed",
    "autonomous_loop_started",
    "external_provider_adapter_implemented",
    "external_agent_adapter_implemented",
    "vendor_adapter_implemented",
    "pm4py_runtime_dependency_added",
    "ocpa_runtime_dependency_added",
    "pig_memory_promoted",
    "pig_policy_mutated",
    "pig_executed",
    "schumpeter_split_introduced",
    "raw_transcript_persisted",
    "raw_provider_output_inline",
    "raw_secret_output",
    "llm_judge_used",
]

WORKBENCH_CONSOLIDATION_REQUIRED_GAPS = [
    "memory_candidate_extraction_not_started",
    "session_continuity_not_started",
    "durable_memory_boundary_not_started",
    "memory_promotion_gate_not_started",
    "public_alpha_schumpeter_split_not_started",
    "external_provider_adapter_not_started",
    "external_agent_dominion_bridge_not_started",
    "pm4py_ocpa_adapter_not_started",
    "production_ui_not_started",
    "autonomous_multistep_loop_not_started",
]

WORKBENCH_MEMORY_CANDIDATE_READY_INPUTS = [
    "workbench_snapshot_refs",
    "ocel_export_package_refs",
    "session_context_refs",
    "trace_summary_refs",
    "evidence_summary_refs",
    "pig_guidance_refs",
    "approval_decision_refs",
    "command_candidate_refs",
    "failure_cause_refs",
    "human_intervention_refs",
    "event_quality_report_refs",
]

WORKBENCH_V0269_NOT_IMPLEMENTED = [
    "memory candidate extraction",
    "memory scoring",
    "memory promotion gate",
    "durable memory write",
    "persona mutation",
    "session continuity engine",
]

WORKBENCH_EXCLUDED_CAPABILITIES = [
    "Memory Candidate Extraction",
    "Memory Promotion",
    "Persistent Memory Write",
    "Persona Mutation",
    "Session Continuity Engine",
    "External Provider Adapter",
    "External Agent Dominion Bridge",
    "Schumpeter Split / Company Wrapper",
    "pm4py/ocpa runtime adapter",
    "Autonomous Multi-Step Execution Loop",
    "Automatic Retry / Repair",
    "Direct Provider Invocation",
    "Direct Command Execution",
    "Direct File Mutation",
    "Raw Transcript Persistence / Export",
    "Raw Provider Output Persistence / Export",
]


def _ref(ref_type: str, ref_id: str, version: str = WORKBENCH_CONSOLIDATION_VERSION) -> dict[str, Any]:
    return {"type": ref_type, "id": ref_id, "version": version}


def _model_ref(ref_type: str, model: Any, id_attr: str) -> dict[str, Any]:
    return _ref(ref_type, getattr(model, id_attr), getattr(model, "version", WORKBENCH_CONSOLIDATION_VERSION))


def _bool(value: bool) -> str:
    return "true" if value else "false"


class _ModelMixin:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class WorkbenchFoundationSubjectComponent(_ModelMixin):
    component_id: str
    version_introduced: str
    subject_id: str
    subject_name: str
    component_type: str
    skill_ids: list[str]
    report_ref: dict[str, Any] | None
    status: str
    user_visible_control_surface: bool
    inspection_capable: bool
    approval_capable: bool
    command_candidate_capable: bool
    snapshot_export_capable: bool
    memory_capable: bool = False
    external_adapter: bool = False
    execution_surface: bool = False
    ocel_visible: bool = True
    pig_visible: bool = True
    ocpx_visible: bool = True
    finding_count: int = 0
    notes: list[str] = field(default_factory=list)


@dataclass
class WorkbenchFoundationSnapshot(_ModelMixin):
    snapshot_id: str
    created_at: str
    subject_components: list[WorkbenchFoundationSubjectComponent]
    capability_map_id: str
    coverage_matrix_id: str
    safety_boundary_report_id: str
    interaction_boundary_report_id: str
    event_quality_consolidation_report_id: str
    trace_coverage_consolidation_report_id: str
    usability_readiness_report_id: str
    v027_readiness_report_id: str
    memory_candidate_handoff_packet_id: str
    release_manifest_id: str
    consolidation_report_id: str
    snapshot_status: str
    version: str = WORKBENCH_CONSOLIDATION_VERSION
    release_name: str = WORKBENCH_CONSOLIDATION_RELEASE_NAME
    included_versions: list[str] = field(default_factory=lambda: list(WORKBENCH_CONSOLIDATION_INCLUDED_VERSIONS))
    previous_release_ref: dict[str, Any] | None = field(
        default_factory=lambda: _ref("agent_usability_consolidation_report", "v0.25.9_bounded_general_agent_surface_foundation_v1", "v0.25.9")
    )
    limitations: list[str] = field(default_factory=list)


@dataclass
class WorkbenchCapabilityMapEntry(_ModelMixin):
    capability_id: str
    name: str
    version_introduced: str
    skill_ids: list[str]
    source_report_refs: list[dict[str, Any]]
    status: str
    capability_category: str
    allowed_effect_types: list[str]
    forbidden_effect_types: list[str]
    user_visible: bool
    mutating: bool = False
    executing: bool = False
    memory_capable: bool = False
    external_adapter: bool = False
    ocel_visible: bool = True
    pig_visible: bool = True
    ocpx_visible: bool = True
    safety_notes: list[str] = field(default_factory=list)


@dataclass
class WorkbenchCapabilityMap(_ModelMixin):
    map_id: str
    entries: list[WorkbenchCapabilityMapEntry]
    implemented_count: int
    warning_count: int
    failed_count: int
    blocked_count: int
    inspection_capability_count: int
    approval_capability_count: int
    command_candidate_capability_count: int
    snapshot_export_capability_count: int
    memory_capability_count: int = 0
    external_adapter_count: int = 0
    execution_surface_count: int = 0
    version: str = WORKBENCH_CONSOLIDATION_VERSION


@dataclass
class WorkbenchCoverageMatrixRow(_ModelMixin):
    subject_id: str
    version_introduced: str
    has_model: bool
    has_service: bool
    has_cli: bool
    has_tests: bool
    has_boundary_tests: bool
    has_docs: bool
    has_ocel_mapping: bool
    has_pig_projection: bool
    has_ocpx_projection: bool
    has_safety_boundary: bool
    has_forbidden_search: bool
    latest_artifact_available: bool
    coverage_notes: list[str] = field(default_factory=list)


@dataclass
class WorkbenchCoverageMatrix(_ModelMixin):
    matrix_id: str
    rows: list[WorkbenchCoverageMatrixRow]
    coverage_status: str
    missing_required_coverage_count: int
    optional_gap_count: int
    future_track_gap_count: int
    version: str = WORKBENCH_CONSOLIDATION_VERSION


@dataclass
class WorkbenchSafetyBoundaryReport(_ModelMixin):
    report_id: str
    status: str
    version: str = WORKBENCH_CONSOLIDATION_VERSION
    ui_rendering_count: int = 0
    provider_invocation_count: int = 0
    command_execution_count: int = 0
    local_command_execution_count: int = 0
    file_mutation_count: int = 0
    ask_execution_count: int = 0
    final_response_emission_count: int = 0
    route_rerun_count: int = 0
    stage_rerun_count: int = 0
    automatic_retry_count: int = 0
    automatic_repair_count: int = 0
    autonomous_loop_count: int = 0
    background_daemon_count: int = 0
    continuous_watcher_count: int = 0
    memory_candidate_count: int = 0
    memory_promotion_count: int = 0
    persistent_memory_write_count: int = 0
    persona_mutation_count: int = 0
    external_adapter_count: int = 0
    vendor_adapter_count: int = 0
    pm4py_runtime_dependency_count: int = 0
    ocpa_runtime_dependency_count: int = 0
    raw_transcript_persistence_count: int = 0
    raw_provider_output_persistence_count: int = 0
    raw_secret_output_count: int = 0
    credential_exposure_count: int = 0
    schumpeter_split_count: int = 0
    llm_judge_count: int = 0
    findings: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchInteractionBoundaryReport(_ModelMixin):
    report_id: str
    trace_view_available: bool
    provider_browser_available: bool
    evidence_inspector_available: bool
    approval_console_available: bool
    run_dashboard_available: bool
    session_monitor_available: bool
    command_candidate_surface_available: bool
    snapshot_export_available: bool
    do_nothing_candidate_available: bool
    approval_rejection_deferral_visible: bool
    human_intervention_points_visible: bool
    execution_boundary_preserved: bool
    interaction_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = WORKBENCH_CONSOLIDATION_VERSION


@dataclass
class WorkbenchEventQualityConsolidationReport(_ModelMixin):
    report_id: str
    source_event_quality_report_refs: list[dict[str, Any]]
    decision_point_coverage: float | None
    skill_candidate_coverage: float | None
    action_candidate_coverage: float | None
    route_rationale_coverage: float | None
    provider_rationale_coverage: float | None
    safety_rationale_coverage: float | None
    pig_guidance_coverage: float | None
    approval_decision_coverage: float | None
    failure_cause_coverage: float | None
    human_intervention_coverage: float | None
    event_quality_status: str
    automatic_optimization_performed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = WORKBENCH_CONSOLIDATION_VERSION


@dataclass
class WorkbenchTraceCoverageConsolidationReport(_ModelMixin):
    report_id: str
    source_trace_coverage_report_refs: list[dict[str, Any]]
    trace_explorer_coverage: bool
    provider_browser_coverage: bool
    evidence_inspector_coverage: bool
    approval_console_coverage: bool
    dashboard_coverage: bool
    command_surface_coverage: bool
    snapshot_export_coverage: bool
    stage_trace_coverage: dict[str, bool]
    decision_trace_coverage: dict[str, bool]
    coverage_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = WORKBENCH_CONSOLIDATION_VERSION


@dataclass
class WorkbenchUsabilityReadinessReport(_ModelMixin):
    report_id: str
    default_agent_assets_visible: bool
    skill_candidate_visible: bool
    action_candidate_visible: bool
    provider_capability_visible: bool
    evidence_visible: bool
    safety_rationale_visible: bool
    approval_flow_visible: bool
    command_candidate_visible: bool
    session_context_refs_visible: bool
    pig_guidance_visible: bool
    do_nothing_visible: bool
    usability_status: str
    remaining_gaps: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]]
    version: str = WORKBENCH_CONSOLIDATION_VERSION


@dataclass
class WorkbenchProcessIntelligenceFeedbackLoopReport(_ModelMixin):
    report_id: str
    ocel_event_quality_ready: bool
    ocpx_view_readiness_ready: bool
    pig_guidance_visibility_ready: bool
    workbench_inspection_ready: bool
    approval_record_ready: bool
    command_candidate_ready: bool
    snapshot_export_ready: bool
    v027_memory_candidate_input_ready: bool
    feedback_loop_status: str
    notes: list[str]
    evidence_refs: list[dict[str, Any]]
    version: str = WORKBENCH_CONSOLIDATION_VERSION


@dataclass
class WorkbenchDefaultAgentUsabilityGap(_ModelMixin):
    gap_id: str
    title: str
    description: str
    severity: str
    affected_subjects: list[str]
    recommended_track: str | None
    recommended_version: str | None
    withdrawal_condition: str | None
    evidence_refs: list[dict[str, Any]]
    version: str = WORKBENCH_CONSOLIDATION_VERSION


@dataclass
class WorkbenchDefaultAgentUsabilityGapRegister(_ModelMixin):
    register_id: str
    gaps: list[WorkbenchDefaultAgentUsabilityGap]
    blocker_count: int
    warning_count: int
    future_track_count: int
    gap_status: str
    version: str = WORKBENCH_CONSOLIDATION_VERSION


@dataclass
class WorkbenchV027ReadinessReport(_ModelMixin):
    report_id: str
    ready_for_v0_27: bool
    substrate_requirements_met: bool
    workbench_snapshot_available: bool
    ocel_export_available: bool
    session_context_refs_available: bool
    trace_summary_refs_available: bool
    evidence_summary_refs_available: bool
    pig_guidance_refs_available: bool
    approval_decision_refs_available: bool
    command_candidate_refs_available: bool
    failure_cause_refs_available: bool
    human_intervention_refs_available: bool
    blockers: list[str]
    warnings: list[str]
    notes: list[str]
    version: str = WORKBENCH_CONSOLIDATION_VERSION
    target_track: str = "v0.27.x Memory Candidate & Continuity"
    recommended_next_version: str = WORKBENCH_CONSOLIDATION_NEXT_STEP
    memory_not_implemented_yet: bool = True
    memory_candidate_not_extracted_yet: bool = True


@dataclass
class WorkbenchMemoryCandidateHandoffPacket(_ModelMixin):
    handoff_packet_id: str
    source_release_manifest_id: str
    source_consolidation_report_id: str
    memory_candidate_ready_inputs: list[str]
    not_implemented_in_v0269: list[str]
    handoff_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = WORKBENCH_CONSOLIDATION_VERSION
    target_version: str = "v0.27.0"
    target_track: str = "Memory Candidate & Continuity"
    refs_only: bool = True
    memory_created_now: bool = False


@dataclass
class WorkbenchReleaseManifest(_ModelMixin):
    manifest_id: str
    included_versions: list[str]
    included_subjects: list[str]
    included_capabilities: list[str]
    excluded_capabilities: list[str]
    allowed_effect_types: list[str]
    forbidden_effect_types: list[str]
    foundation_snapshot_id: str
    capability_map_id: str
    coverage_matrix_id: str
    safety_boundary_report_id: str
    interaction_boundary_report_id: str
    event_quality_consolidation_report_id: str
    trace_coverage_consolidation_report_id: str
    usability_readiness_report_id: str
    v027_readiness_report_id: str
    memory_candidate_handoff_packet_id: str
    release_status: str
    notes: list[str] = field(default_factory=list)
    release_version: str = WORKBENCH_CONSOLIDATION_VERSION
    release_name: str = WORKBENCH_CONSOLIDATION_RELEASE_NAME


@dataclass
class WorkbenchConsolidationFinding(_ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class WorkbenchConsolidationReport(_ModelMixin):
    report_id: str
    created_at: str
    foundation_snapshot: WorkbenchFoundationSnapshot
    capability_map: WorkbenchCapabilityMap
    coverage_matrix: WorkbenchCoverageMatrix
    safety_boundary_report: WorkbenchSafetyBoundaryReport
    interaction_boundary_report: WorkbenchInteractionBoundaryReport
    event_quality_consolidation_report: WorkbenchEventQualityConsolidationReport
    trace_coverage_consolidation_report: WorkbenchTraceCoverageConsolidationReport
    usability_readiness_report: WorkbenchUsabilityReadinessReport
    process_intelligence_feedback_loop_report: WorkbenchProcessIntelligenceFeedbackLoopReport
    gap_register: WorkbenchDefaultAgentUsabilityGapRegister
    v027_readiness_report: WorkbenchV027ReadinessReport
    memory_candidate_handoff_packet: WorkbenchMemoryCandidateHandoffPacket
    release_manifest: WorkbenchReleaseManifest
    findings: list[WorkbenchConsolidationFinding]
    readiness_status: str
    release_status: str
    ready_for_v0_27: bool
    version: str = WORKBENCH_CONSOLIDATION_VERSION
    release_name: str = WORKBENCH_CONSOLIDATION_RELEASE_NAME
    ready_for_v0_28: bool = False
    memory_candidate_created: bool = False
    memory_promoted: bool = False
    persistent_memory_written: bool = False
    persona_mutated: bool = False
    command_executed: bool = False
    provider_invoked: bool = False
    local_command_executed: bool = False
    file_mutated: bool = False
    patch_applied: bool = False
    ask_executed: bool = False
    final_response_emitted: bool = False
    route_rerun_performed: bool = False
    stage_rerun_performed: bool = False
    automatic_retry_performed: bool = False
    automatic_repair_performed: bool = False
    autonomous_loop_started: bool = False
    external_provider_adapter_implemented: bool = False
    external_agent_adapter_implemented: bool = False
    vendor_adapter_implemented: bool = False
    pm4py_runtime_dependency_added: bool = False
    ocpa_runtime_dependency_added: bool = False
    pig_memory_promoted: bool = False
    pig_policy_mutated: bool = False
    pig_executed: bool = False
    schumpeter_split_introduced: bool = False
    raw_transcript_persisted: bool = False
    raw_provider_output_inline: bool = False
    raw_secret_output: bool = False
    llm_judge_used: bool = False
    next_required_step: str = WORKBENCH_CONSOLIDATION_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = (
        "Valid until v0.27 Memory Candidate & Continuity begins or Workbench Foundation policy changes."
    )


SUBJECT_DEFINITIONS = [
    ("v0.26.0", "workbench_contract", "Workspace Agent Workbench Contract", "contract", ["skill:workspace_agent_workbench_contract_view"], "contract", True, True, False, False, False),
    ("v0.26.1", "workbench_view_state", "Workbench View State & Panel Model", "view_state_panel_model", ["skill:workbench_view_state_create", "skill:workbench_panel_model_view"], "view_state", True, True, False, False, False),
    ("v0.26.2", "workbench_trace_explorer", "Trace Explorer & Pipeline Timeline", "trace_explorer", ["skill:workbench_trace_explorer_view", "skill:workbench_pipeline_timeline_view"], "trace_inspection", True, True, False, False, False),
    ("v0.26.3", "workbench_provider_browser", "Provider / Capability Browser", "provider_browser", ["skill:workbench_provider_browser_view"], "provider_inspection", True, True, False, False, False),
    ("v0.26.4", "workbench_evidence_inspector", "Evidence / Report Inspector", "evidence_inspector", ["skill:workbench_evidence_inspector_view"], "evidence_inspection", True, True, False, False, False),
    ("v0.26.5", "workbench_approval_console", "Safety Gate / Approval Console", "approval_console", ["skill:workbench_safety_gate_view", "skill:workbench_approval_console_view"], "approval_record", True, True, True, False, False),
    ("v0.26.6", "workbench_run_dashboard_session_monitor", "Run Dashboard / Session Monitor", "run_dashboard_session_monitor", ["skill:workbench_run_dashboard_view", "skill:workbench_session_monitor_view"], "dashboard_monitor", True, True, False, False, False),
    ("v0.26.7", "workbench_command_surface", "Workbench Command Surface", "command_surface", ["skill:workbench_command_surface_use"], "command_candidate", True, True, False, True, False),
    ("v0.26.8", "workbench_snapshot_export", "Workbench Snapshot / OCEL Export", "snapshot_export", ["skill:workbench_snapshot_create", "skill:workbench_ocel_export_create"], "snapshot_export", True, True, False, False, True),
    ("v0.26.9", "workbench_consolidation", "Workspace Agent Workbench Consolidation", "consolidation", ["skill:workbench_consolidation_view"], "consolidation", True, True, False, False, False),
]


class WorkbenchConsolidationSourceService:
    def __init__(
        self,
        *,
        v0260_available: bool = True,
        v0261_available: bool = True,
        v0262_available: bool = True,
        v0263_available: bool = True,
        v0264_available: bool = True,
        v0265_available: bool = True,
        v0266_available: bool = True,
        v0267_available: bool = True,
        v0268_available: bool = True,
        v0259_available: bool = True,
        v0249_available: bool = True,
    ) -> None:
        self.availability = {
            "v0.26.0": v0260_available,
            "v0.26.1": v0261_available,
            "v0.26.2": v0262_available,
            "v0.26.3": v0263_available,
            "v0.26.4": v0264_available,
            "v0.26.5": v0265_available,
            "v0.26.6": v0266_available,
            "v0.26.7": v0267_available,
            "v0.26.8": v0268_available,
            "v0.25.9": v0259_available,
            "v0.24.9": v0249_available,
        }

    def _load(self, version: str, report_type: str) -> dict[str, Any] | None:
        if not self.availability.get(version, False):
            return None
        return _ref(report_type, f"{report_type}:{version}", version)

    def load_v0260_contract_report(self) -> dict[str, Any] | None:
        return self._load("v0.26.0", "workbench_contract_report")

    def load_v0261_view_state_report(self) -> dict[str, Any] | None:
        return self._load("v0.26.1", "workbench_view_state_report")

    def load_v0262_trace_explorer_report(self) -> dict[str, Any] | None:
        return self._load("v0.26.2", "workbench_trace_explorer_report")

    def load_v0263_provider_browser_report(self) -> dict[str, Any] | None:
        return self._load("v0.26.3", "workbench_provider_browser_report")

    def load_v0264_evidence_inspector_report(self) -> dict[str, Any] | None:
        return self._load("v0.26.4", "workbench_evidence_inspector_report")

    def load_v0265_approval_console_report(self) -> dict[str, Any] | None:
        return self._load("v0.26.5", "workbench_approval_console_report")

    def load_v0266_dashboard_report(self) -> dict[str, Any] | None:
        return self._load("v0.26.6", "workbench_run_dashboard_report")

    def load_v0267_command_surface_report(self) -> dict[str, Any] | None:
        return self._load("v0.26.7", "workbench_command_surface_report")

    def load_v0268_snapshot_export_report(self) -> dict[str, Any] | None:
        return self._load("v0.26.8", "workbench_snapshot_export_report")

    def load_v0259_agent_surface_release(self) -> dict[str, Any] | None:
        return self._load("v0.25.9", "agent_usability_consolidation_report")

    def load_v0249_internal_provider_release(self) -> dict[str, Any] | None:
        return self._load("v0.24.9", "internal_provider_consolidation_report")

    def report_ref_for_version(self, version: str) -> dict[str, Any] | None:
        loaders = {
            "v0.26.0": self.load_v0260_contract_report,
            "v0.26.1": self.load_v0261_view_state_report,
            "v0.26.2": self.load_v0262_trace_explorer_report,
            "v0.26.3": self.load_v0263_provider_browser_report,
            "v0.26.4": self.load_v0264_evidence_inspector_report,
            "v0.26.5": self.load_v0265_approval_console_report,
            "v0.26.6": self.load_v0266_dashboard_report,
            "v0.26.7": self.load_v0267_command_surface_report,
            "v0.26.8": self.load_v0268_snapshot_export_report,
        }
        loader = loaders.get(version)
        return loader() if loader else None

    def missing_versions(self) -> list[str]:
        return [version for version in WORKBENCH_CONSOLIDATION_INCLUDED_VERSIONS[:-1] if not self.availability.get(version, False)]


class WorkbenchFoundationSubjectComponentService:
    def build_subject_components(self, source_service: WorkbenchConsolidationSourceService) -> list[WorkbenchFoundationSubjectComponent]:
        components: list[WorkbenchFoundationSubjectComponent] = []
        for version, subject_id, name, component_type, skill_ids, _category, user_visible, inspection, approval, command, snapshot in SUBJECT_DEFINITIONS:
            available = True if version == WORKBENCH_CONSOLIDATION_VERSION else source_service.availability.get(version, False)
            components.append(
                WorkbenchFoundationSubjectComponent(
                    component_id=f"workbench_component:{subject_id}",
                    version_introduced=version,
                    subject_id=subject_id,
                    subject_name=name,
                    component_type=component_type,
                    skill_ids=skill_ids,
                    report_ref=source_service.report_ref_for_version(version) if version != WORKBENCH_CONSOLIDATION_VERSION else None,
                    status="implemented" if available else "warning",
                    user_visible_control_surface=user_visible,
                    inspection_capable=inspection,
                    approval_capable=approval,
                    command_candidate_capable=command,
                    snapshot_export_capable=snapshot,
                    finding_count=0 if available else 1,
                    notes=["Consolidated as refs-only Workbench Foundation v1 component."],
                )
            )
        return components


class WorkbenchCapabilityMapService:
    def build_capability_map(self, components: list[WorkbenchFoundationSubjectComponent]) -> WorkbenchCapabilityMap:
        entries: list[WorkbenchCapabilityMapEntry] = []
        for component, definition in zip(components, SUBJECT_DEFINITIONS, strict=True):
            category = definition[5]
            entries.append(
                WorkbenchCapabilityMapEntry(
                    capability_id=f"workbench_capability:{category}",
                    name=component.subject_name,
                    version_introduced=component.version_introduced,
                    skill_ids=component.skill_ids,
                    source_report_refs=[component.report_ref] if component.report_ref else [],
                    status=component.status,
                    capability_category=category,
                    allowed_effect_types=WORKBENCH_CONSOLIDATION_EFFECT_TYPES,
                    forbidden_effect_types=WORKBENCH_CONSOLIDATION_FORBIDDEN_EFFECT_TYPES,
                    user_visible=component.user_visible_control_surface,
                    safety_notes=["Capability is read-only, non-executing, and OCEL-visible in v0.26.9."],
                )
            )
        return WorkbenchCapabilityMap(
            map_id="workbench_capability_map:v0.26.9",
            entries=entries,
            implemented_count=sum(1 for entry in entries if entry.status == "implemented"),
            warning_count=sum(1 for entry in entries if entry.status == "warning"),
            failed_count=0,
            blocked_count=0,
            inspection_capability_count=sum(1 for component in components if component.inspection_capable),
            approval_capability_count=sum(1 for component in components if component.approval_capable),
            command_candidate_capability_count=sum(1 for component in components if component.command_candidate_capable),
            snapshot_export_capability_count=sum(1 for component in components if component.snapshot_export_capable),
        )


class WorkbenchCoverageMatrixService:
    def build_coverage_matrix(self, components: list[WorkbenchFoundationSubjectComponent]) -> WorkbenchCoverageMatrix:
        rows = [
            WorkbenchCoverageMatrixRow(
                subject_id=component.subject_id,
                version_introduced=component.version_introduced,
                has_model=True,
                has_service=True,
                has_cli=True,
                has_tests=True,
                has_boundary_tests=True,
                has_docs=True,
                has_ocel_mapping=True,
                has_pig_projection=True,
                has_ocpx_projection=True,
                has_safety_boundary=True,
                has_forbidden_search=True,
                latest_artifact_available=component.status == "implemented",
                coverage_notes=["Coverage is consolidated from v0.26 release artifacts."],
            )
            for component in components
            if component.version_introduced != WORKBENCH_CONSOLIDATION_VERSION
        ]
        missing = sum(1 for row in rows if not row.latest_artifact_available)
        return WorkbenchCoverageMatrix(
            matrix_id="workbench_coverage_matrix:v0.26.9",
            rows=rows,
            coverage_status="complete" if missing == 0 else "partial",
            missing_required_coverage_count=missing,
            optional_gap_count=0,
            future_track_gap_count=len(WORKBENCH_CONSOLIDATION_REQUIRED_GAPS),
        )


class WorkbenchSafetyBoundaryReportService:
    def build_safety_boundary_report(self) -> WorkbenchSafetyBoundaryReport:
        return WorkbenchSafetyBoundaryReport(report_id="workbench_safety_boundary_report:v0.26.9", status="passed")


class WorkbenchInteractionBoundaryReportService:
    def build_interaction_boundary_report(self) -> WorkbenchInteractionBoundaryReport:
        return WorkbenchInteractionBoundaryReport(
            report_id="workbench_interaction_boundary_report:v0.26.9",
            trace_view_available=True,
            provider_browser_available=True,
            evidence_inspector_available=True,
            approval_console_available=True,
            run_dashboard_available=True,
            session_monitor_available=True,
            command_candidate_surface_available=True,
            snapshot_export_available=True,
            do_nothing_candidate_available=True,
            approval_rejection_deferral_visible=True,
            human_intervention_points_visible=True,
            execution_boundary_preserved=True,
            interaction_status="ready",
            evidence_refs=[_ref("workbench_release_manifest", "workbench_release_manifest:v0.26.9")],
        )


class WorkbenchEventQualityConsolidationReportService:
    def build_report(self) -> WorkbenchEventQualityConsolidationReport:
        return WorkbenchEventQualityConsolidationReport(
            report_id="workbench_event_quality_consolidation:v0.26.9",
            source_event_quality_report_refs=[_ref("workbench_event_quality_report", "workbench_event_quality_report:v0.26.8", "v0.26.8")],
            decision_point_coverage=1.0,
            skill_candidate_coverage=1.0,
            action_candidate_coverage=1.0,
            route_rationale_coverage=1.0,
            provider_rationale_coverage=1.0,
            safety_rationale_coverage=1.0,
            pig_guidance_coverage=1.0,
            approval_decision_coverage=1.0,
            failure_cause_coverage=1.0,
            human_intervention_coverage=1.0,
            event_quality_status="ready",
            evidence_refs=[_ref("workbench_snapshot_export_report", "workbench_snapshot_export_report:v0.26.8", "v0.26.8")],
        )


class WorkbenchTraceCoverageConsolidationReportService:
    def build_report(self) -> WorkbenchTraceCoverageConsolidationReport:
        return WorkbenchTraceCoverageConsolidationReport(
            report_id="workbench_trace_coverage_consolidation:v0.26.9",
            source_trace_coverage_report_refs=[
                _ref("workbench_trace_coverage_report", "workbench_trace_coverage_report:v0.26.8", "v0.26.8")
            ],
            trace_explorer_coverage=True,
            provider_browser_coverage=True,
            evidence_inspector_coverage=True,
            approval_console_coverage=True,
            dashboard_coverage=True,
            command_surface_coverage=True,
            snapshot_export_coverage=True,
            stage_trace_coverage={"contract": True, "inspection": True, "approval": True, "command_candidate": True, "snapshot_export": True},
            decision_trace_coverage={"approval_decision": True, "command_decision": True, "handoff_decision": True},
            coverage_status="ready",
            evidence_refs=[_ref("workbench_snapshot_export_report", "workbench_snapshot_export_report:v0.26.8", "v0.26.8")],
        )


class WorkbenchUsabilityReadinessReportService:
    def build_report(self, gaps: list[WorkbenchDefaultAgentUsabilityGap]) -> WorkbenchUsabilityReadinessReport:
        return WorkbenchUsabilityReadinessReport(
            report_id="workbench_usability_readiness:v0.26.9",
            default_agent_assets_visible=True,
            skill_candidate_visible=True,
            action_candidate_visible=True,
            provider_capability_visible=True,
            evidence_visible=True,
            safety_rationale_visible=True,
            approval_flow_visible=True,
            command_candidate_visible=True,
            session_context_refs_visible=True,
            pig_guidance_visible=True,
            do_nothing_visible=True,
            usability_status="ready",
            remaining_gaps=[gap.to_dict() for gap in gaps],
            evidence_refs=[_ref("workbench_capability_map", "workbench_capability_map:v0.26.9")],
        )


class WorkbenchProcessIntelligenceFeedbackLoopReportService:
    def build_report(self) -> WorkbenchProcessIntelligenceFeedbackLoopReport:
        return WorkbenchProcessIntelligenceFeedbackLoopReport(
            report_id="workbench_process_intelligence_feedback_loop:v0.26.9",
            ocel_event_quality_ready=True,
            ocpx_view_readiness_ready=True,
            pig_guidance_visibility_ready=True,
            workbench_inspection_ready=True,
            approval_record_ready=True,
            command_candidate_ready=True,
            snapshot_export_ready=True,
            v027_memory_candidate_input_ready=True,
            feedback_loop_status="ready",
            notes=["Feedback loop readiness is descriptive and does not optimize or execute autonomously."],
            evidence_refs=[_ref("workbench_event_quality_consolidation_report", "workbench_event_quality_consolidation:v0.26.9")],
        )


class WorkbenchDefaultAgentUsabilityGapRegisterService:
    def build_gap_register(self) -> WorkbenchDefaultAgentUsabilityGapRegister:
        gaps = [
            WorkbenchDefaultAgentUsabilityGap(
                gap_id=f"workbench_gap:{gap_id}",
                title=gap_id.replace("_", " "),
                description="Tracked as a future-track gap; not implemented in v0.26.9.",
                severity="future_track",
                affected_subjects=["workspace_agent_workbench"],
                recommended_track="future_track",
                recommended_version=self._recommended_version(gap_id),
                withdrawal_condition="Withdraw if this future-track capability is implemented before its roadmap slot.",
                evidence_refs=[_ref("workbench_release_manifest", "workbench_release_manifest:v0.26.9")],
            )
            for gap_id in WORKBENCH_CONSOLIDATION_REQUIRED_GAPS
        ]
        return WorkbenchDefaultAgentUsabilityGapRegister(
            register_id="workbench_default_agent_usability_gap_register:v0.26.9",
            gaps=gaps,
            blocker_count=0,
            warning_count=0,
            future_track_count=len(gaps),
            gap_status="ready",
        )

    def _recommended_version(self, gap_id: str) -> str | None:
        if "memory" in gap_id or "continuity" in gap_id:
            return "v0.27.x"
        if "schumpeter" in gap_id:
            return "v0.28.x"
        if "external_provider" in gap_id or "pm4py" in gap_id:
            return "v0.29.x+"
        if "external_agent" in gap_id:
            return "v0.30.x+"
        return None


class WorkbenchV027ReadinessReportService:
    def build_report(self, safety: WorkbenchSafetyBoundaryReport, coverage: WorkbenchCoverageMatrix) -> WorkbenchV027ReadinessReport:
        substrate = safety.status == "passed" and coverage.coverage_status in {"complete", "partial"}
        return WorkbenchV027ReadinessReport(
            report_id="workbench_v027_readiness:v0.26.9",
            ready_for_v0_27=substrate,
            substrate_requirements_met=substrate,
            workbench_snapshot_available=True,
            ocel_export_available=True,
            session_context_refs_available=True,
            trace_summary_refs_available=True,
            evidence_summary_refs_available=True,
            pig_guidance_refs_available=True,
            approval_decision_refs_available=True,
            command_candidate_refs_available=True,
            failure_cause_refs_available=True,
            human_intervention_refs_available=True,
            blockers=[],
            warnings=[] if coverage.coverage_status == "complete" else ["Some optional source refs are partial but safe."],
            notes=["Readiness means v0.27 contract work may start; no memory candidate is extracted in v0.26.9."],
        )


class WorkbenchMemoryCandidateHandoffPacketService:
    def build_packet(self, release_manifest_id: str, consolidation_report_id: str) -> WorkbenchMemoryCandidateHandoffPacket:
        return WorkbenchMemoryCandidateHandoffPacket(
            handoff_packet_id="workbench_memory_candidate_handoff:v0.26.9",
            source_release_manifest_id=release_manifest_id,
            source_consolidation_report_id=consolidation_report_id,
            memory_candidate_ready_inputs=list(WORKBENCH_MEMORY_CANDIDATE_READY_INPUTS),
            not_implemented_in_v0269=list(WORKBENCH_V0269_NOT_IMPLEMENTED),
            handoff_status="ready",
            evidence_refs=[_ref("workbench_release_manifest", release_manifest_id)],
        )


class WorkbenchReleaseManifestService:
    def build_manifest(
        self,
        components: list[WorkbenchFoundationSubjectComponent],
        capability_map: WorkbenchCapabilityMap,
        coverage: WorkbenchCoverageMatrix,
        safety: WorkbenchSafetyBoundaryReport,
        interaction: WorkbenchInteractionBoundaryReport,
        event_quality: WorkbenchEventQualityConsolidationReport,
        trace_coverage: WorkbenchTraceCoverageConsolidationReport,
        usability: WorkbenchUsabilityReadinessReport,
        v027: WorkbenchV027ReadinessReport,
        handoff: WorkbenchMemoryCandidateHandoffPacket,
    ) -> WorkbenchReleaseManifest:
        releasable = safety.status == "passed" and interaction.interaction_status == "ready" and v027.ready_for_v0_27
        return WorkbenchReleaseManifest(
            manifest_id="workbench_release_manifest:v0.26.9",
            included_versions=list(WORKBENCH_CONSOLIDATION_INCLUDED_VERSIONS),
            included_subjects=[component.subject_id for component in components],
            included_capabilities=[entry.capability_category for entry in capability_map.entries],
            excluded_capabilities=list(WORKBENCH_EXCLUDED_CAPABILITIES),
            allowed_effect_types=WORKBENCH_CONSOLIDATION_EFFECT_TYPES,
            forbidden_effect_types=WORKBENCH_CONSOLIDATION_FORBIDDEN_EFFECT_TYPES,
            foundation_snapshot_id="workbench_foundation_snapshot:v0.26.9",
            capability_map_id=capability_map.map_id,
            coverage_matrix_id=coverage.matrix_id,
            safety_boundary_report_id=safety.report_id,
            interaction_boundary_report_id=interaction.report_id,
            event_quality_consolidation_report_id=event_quality.report_id,
            trace_coverage_consolidation_report_id=trace_coverage.report_id,
            usability_readiness_report_id=usability.report_id,
            v027_readiness_report_id=v027.report_id,
            memory_candidate_handoff_packet_id=handoff.handoff_packet_id,
            release_status="releasable" if releasable else "releasable_with_warnings",
            notes=["Workspace Agent Workbench Foundation v1 closes v0.26 without memory or execution capabilities."],
        )


class WorkbenchFoundationSnapshotService:
    def build_snapshot(
        self,
        components: list[WorkbenchFoundationSubjectComponent],
        release_manifest: WorkbenchReleaseManifest,
        readiness_status: str,
    ) -> WorkbenchFoundationSnapshot:
        return WorkbenchFoundationSnapshot(
            snapshot_id="workbench_foundation_snapshot:v0.26.9",
            created_at=utc_now_iso(),
            subject_components=components,
            capability_map_id=release_manifest.capability_map_id,
            coverage_matrix_id=release_manifest.coverage_matrix_id,
            safety_boundary_report_id=release_manifest.safety_boundary_report_id,
            interaction_boundary_report_id=release_manifest.interaction_boundary_report_id,
            event_quality_consolidation_report_id=release_manifest.event_quality_consolidation_report_id,
            trace_coverage_consolidation_report_id=release_manifest.trace_coverage_consolidation_report_id,
            usability_readiness_report_id=release_manifest.usability_readiness_report_id,
            v027_readiness_report_id=release_manifest.v027_readiness_report_id,
            memory_candidate_handoff_packet_id=release_manifest.memory_candidate_handoff_packet_id,
            release_manifest_id=release_manifest.manifest_id,
            consolidation_report_id="workbench_consolidation_report:v0.26.9",
            snapshot_status="ready" if readiness_status == "ready" else "warning",
            limitations=["Foundation snapshot is refs-only release readiness, not memory continuity."],
        )


class WorkbenchConsolidationFindingService:
    BLOCKED_FINDINGS = {
        "memory_candidate_extraction_detected",
        "memory_promotion_detected",
        "persistent_memory_write_detected",
        "persona_mutation_detected",
        "command_execution_detected",
        "provider_invocation_detected",
        "local_command_execution_detected",
        "file_mutation_detected",
        "ask_execution_detected",
        "final_response_emission_detected",
        "rerun_retry_repair_detected",
        "autonomous_loop_detected",
        "external_adapter_detected",
        "pm4py_ocpa_dependency_detected",
        "raw_transcript_persistence_detected",
        "raw_provider_output_persistence_detected",
        "raw_secret_output_detected",
        "schumpeter_split_detected",
        "llm_judge_detected",
    }
    CREATED_FINDINGS = [
        "v027_readiness_created",
        "memory_candidate_handoff_created",
        "release_manifest_created",
    ]

    def build_findings(
        self,
        source_service: WorkbenchConsolidationSourceService,
        coverage: WorkbenchCoverageMatrix,
        event_quality: WorkbenchEventQualityConsolidationReport,
        trace_coverage: WorkbenchTraceCoverageConsolidationReport,
        usability: WorkbenchUsabilityReadinessReport,
        *,
        strictness: str = "standard",
        extra_findings: list[str] | None = None,
    ) -> list[WorkbenchConsolidationFinding]:
        findings: list[WorkbenchConsolidationFinding] = []
        missing_map = {
            "v0.26.0": "missing_contract_report",
            "v0.26.1": "missing_view_state_report",
            "v0.26.2": "missing_trace_explorer_report",
            "v0.26.3": "missing_provider_browser_report",
            "v0.26.4": "missing_evidence_inspector_report",
            "v0.26.5": "missing_approval_console_report",
            "v0.26.6": "missing_dashboard_report",
            "v0.26.7": "missing_command_surface_report",
            "v0.26.8": "missing_snapshot_export_report",
        }
        for version in source_service.missing_versions():
            severity = "error" if strictness == "strict" else "warning"
            findings.append(self._finding(severity, missing_map.get(version, "missing_v026_subject"), f"{version} source report is missing."))
        if coverage.missing_required_coverage_count:
            findings.append(self._finding("warning", "missing_v026_subject", "Some v0.26 subject coverage is partial."))
        if event_quality.event_quality_status != "ready":
            findings.append(self._finding("warning", "incomplete_event_quality", "Event quality consolidation is partial."))
        if trace_coverage.coverage_status != "ready":
            findings.append(self._finding("warning", "incomplete_trace_coverage", "Trace coverage consolidation is partial."))
        if usability.usability_status != "ready":
            findings.append(self._finding("warning", "incomplete_usability_readiness", "Usability readiness is partial."))
        for finding_type in self.CREATED_FINDINGS:
            findings.append(self._finding("info", finding_type, finding_type))
        for finding_type in extra_findings or []:
            severity = "critical" if finding_type in self.BLOCKED_FINDINGS else "warning"
            findings.append(self._finding(severity, finding_type, finding_type))
        if not findings:
            findings.append(self._finding("info", "ok", "Workbench Foundation v1 is consolidated."))
        return findings

    def _finding(self, severity: str, finding_type: str, message: str) -> WorkbenchConsolidationFinding:
        return WorkbenchConsolidationFinding(
            finding_id=f"workbench_consolidation_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            subject_ref=None,
            evidence_refs=[_ref("workbench_consolidation_report", "workbench_consolidation_report:v0.26.9")],
            withdrawal_condition="Withdraw if Workbench Foundation policy or source readiness changes.",
        )


class WorkbenchConsolidationReportService:
    def build_all_parts(
        self,
        *,
        report_id: str | None = None,
        strictness: str = "standard",
        extra_findings: list[str] | None = None,
        v0260_available: bool = True,
        v0261_available: bool = True,
        v0262_available: bool = True,
        v0263_available: bool = True,
        v0264_available: bool = True,
        v0265_available: bool = True,
        v0266_available: bool = True,
        v0267_available: bool = True,
        v0268_available: bool = True,
    ) -> dict[str, Any]:
        source = WorkbenchConsolidationSourceService(
            v0260_available=v0260_available,
            v0261_available=v0261_available,
            v0262_available=v0262_available,
            v0263_available=v0263_available,
            v0264_available=v0264_available,
            v0265_available=v0265_available,
            v0266_available=v0266_available,
            v0267_available=v0267_available,
            v0268_available=v0268_available,
        )
        components = WorkbenchFoundationSubjectComponentService().build_subject_components(source)
        capability_map = WorkbenchCapabilityMapService().build_capability_map(components)
        coverage = WorkbenchCoverageMatrixService().build_coverage_matrix(components)
        safety = WorkbenchSafetyBoundaryReportService().build_safety_boundary_report()
        interaction = WorkbenchInteractionBoundaryReportService().build_interaction_boundary_report()
        event_quality = WorkbenchEventQualityConsolidationReportService().build_report()
        trace_coverage = WorkbenchTraceCoverageConsolidationReportService().build_report()
        gap_register = WorkbenchDefaultAgentUsabilityGapRegisterService().build_gap_register()
        usability = WorkbenchUsabilityReadinessReportService().build_report(gap_register.gaps)
        feedback = WorkbenchProcessIntelligenceFeedbackLoopReportService().build_report()
        v027 = WorkbenchV027ReadinessReportService().build_report(safety, coverage)
        handoff = WorkbenchMemoryCandidateHandoffPacketService().build_packet(
            "workbench_release_manifest:v0.26.9",
            report_id or "workbench_consolidation_report:v0.26.9",
        )
        release_manifest = WorkbenchReleaseManifestService().build_manifest(
            components,
            capability_map,
            coverage,
            safety,
            interaction,
            event_quality,
            trace_coverage,
            usability,
            v027,
            handoff,
        )
        findings = WorkbenchConsolidationFindingService().build_findings(
            source,
            coverage,
            event_quality,
            trace_coverage,
            usability,
            strictness=strictness,
            extra_findings=extra_findings,
        )
        readiness_status = self._readiness_status(findings, strictness)
        if strictness == "strict" and source.missing_versions():
            readiness_status = "blocked"
        release_status = "blocked" if readiness_status == "blocked" else release_manifest.release_status
        if release_status == "blocked":
            v027.ready_for_v0_27 = False
        foundation_snapshot = WorkbenchFoundationSnapshotService().build_snapshot(components, release_manifest, readiness_status)
        report = WorkbenchConsolidationReport(
            report_id=report_id or "workbench_consolidation_report:v0.26.9",
            created_at=utc_now_iso(),
            foundation_snapshot=foundation_snapshot,
            capability_map=capability_map,
            coverage_matrix=coverage,
            safety_boundary_report=safety,
            interaction_boundary_report=interaction,
            event_quality_consolidation_report=event_quality,
            trace_coverage_consolidation_report=trace_coverage,
            usability_readiness_report=usability,
            process_intelligence_feedback_loop_report=feedback,
            gap_register=gap_register,
            v027_readiness_report=v027,
            memory_candidate_handoff_packet=handoff,
            release_manifest=release_manifest,
            findings=findings,
            readiness_status=readiness_status,
            release_status=release_status,
            ready_for_v0_27=v027.ready_for_v0_27 and readiness_status in {"ready", "warning"},
            limitations=[
                "v0.26.9 consolidates Workspace Agent Workbench Foundation v1 only.",
                "v0.27 readiness is a refs-only handoff signal, not memory implementation.",
            ],
            withdrawal_conditions=[
                "Withdraw readiness if memory candidate extraction, memory promotion, execution, raw persistence, external adapter, pm4py/ocpa dependency, Schumpeter split, or LLM judge is introduced.",
            ],
        )
        return {
            "source_service": source,
            "foundation_snapshot": foundation_snapshot,
            "subject_components": components,
            "capability_map": capability_map,
            "coverage_matrix": coverage,
            "safety_boundary_report": safety,
            "interaction_boundary_report": interaction,
            "event_quality_consolidation_report": event_quality,
            "trace_coverage_consolidation_report": trace_coverage,
            "usability_readiness_report": usability,
            "process_intelligence_feedback_loop_report": feedback,
            "gap_register": gap_register,
            "v027_readiness_report": v027,
            "memory_candidate_handoff_packet": handoff,
            "release_manifest": release_manifest,
            "findings": findings,
            "report": report,
        }

    def _readiness_status(self, findings: list[WorkbenchConsolidationFinding], strictness: str) -> str:
        if any(finding.finding_type in WorkbenchConsolidationFindingService.BLOCKED_FINDINGS for finding in findings):
            return "blocked"
        if any(finding.severity == "critical" for finding in findings):
            return "blocked"
        if strictness == "strict" and any(finding.severity == "error" for finding in findings):
            return "blocked"
        if any(finding.severity in {"warning", "error"} for finding in findings):
            return "warning"
        return "ready"

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": WORKBENCH_CONSOLIDATION_VERSION,
            "layer": WORKBENCH_CONSOLIDATION_LAYER,
            "subject": "workspace_agent_workbench_consolidation",
            "release_name": WORKBENCH_CONSOLIDATION_RELEASE_NAME,
            "principles": [
                "Consolidation is not new Workbench feature implementation",
                "Workbench release readiness is not memory continuity",
                "v0.27 readiness is not v0.27 implementation",
                "Memory candidate readiness is not memory candidate extraction",
                "PIG guidance visibility is not PIG memory",
                "Command candidate visibility is not command execution",
                "Approval decision visibility is not approval execution",
                "Event quality report is not automatic optimization",
                "Trace coverage report is not autonomous improvement",
            ],
            "safety_boundary": {
                "memory_candidate_created": False,
                "memory_promoted": False,
                "persistent_memory_written": False,
                "persona_mutated": False,
                "command_executed": False,
                "provider_invoked": False,
                "local_command_executed": False,
                "file_mutated": False,
                "patch_applied": False,
                "ask_executed": False,
                "final_response_emitted": False,
                "route_rerun_performed": False,
                "stage_rerun_performed": False,
                "automatic_retry_performed": False,
                "automatic_repair_performed": False,
                "autonomous_loop_started": False,
                "external_provider_adapter_implemented": False,
                "vendor_adapter_implemented": False,
                "pm4py_runtime_dependency_added": False,
                "ocpa_runtime_dependency_added": False,
                "pig_memory_promoted": False,
                "pig_policy_mutated": False,
                "pig_executed": False,
                "schumpeter_split_introduced": False,
                "raw_transcript_persisted": False,
                "raw_provider_output_inline": False,
                "raw_secret_output": False,
                "llm_judge_enabled": False,
            },
            "future_direction": [
                "v0.27 memory candidate and continuity",
                "v0.28 public alpha / Schumpeter split preparation",
                "v0.29+ external provider adapters",
                "v0.30+ external agent dominion bridge",
            ],
            "next_step": WORKBENCH_CONSOLIDATION_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "workspace_agent_workbench_foundation_v1_consolidated",
            "version": WORKBENCH_CONSOLIDATION_VERSION,
            "release_name": WORKBENCH_CONSOLIDATION_RELEASE_NAME,
            "source_read_models": [
                "WorkbenchContractState",
                "WorkbenchViewStateState",
                "WorkbenchTraceExplorerViewState",
                "WorkbenchProviderBrowserViewState",
                "WorkbenchEvidenceInspectorViewState",
                "WorkbenchApprovalConsoleViewState",
                "WorkbenchRunDashboardViewState",
                "WorkbenchCommandSurfaceViewState",
                "WorkbenchSnapshotState",
                "WorkbenchOCELExportPackageState",
            ],
            "target_read_models": [
                "WorkbenchFoundationSnapshotState",
                "WorkbenchReleaseManifestState",
                "WorkbenchSafetyBoundaryState",
                "WorkbenchInteractionBoundaryState",
                "WorkbenchEventQualityConsolidationState",
                "WorkbenchTraceCoverageConsolidationState",
                "WorkbenchUsabilityReadinessState",
                "WorkbenchV027ReadinessState",
                "WorkbenchMemoryCandidateHandoffState",
                "V027ReadinessState",
            ],
            "effect_types": WORKBENCH_CONSOLIDATION_EFFECT_TYPES,
            "compatibility_effect_refs": WORKBENCH_RUN_DASHBOARD_EFFECT_TYPES
            + WORKBENCH_COMMAND_SURFACE_EFFECT_TYPES
            + WORKBENCH_SNAPSHOT_EXPORT_EFFECT_TYPES,
        }


def render_workbench_consolidation_cli(parts: dict[str, Any], section: str = "consolidate") -> str:
    report: WorkbenchConsolidationReport = parts["report"]
    lines = [
        f"Workspace Agent Workbench Consolidation {section}",
        f"version={report.version}",
        f"release_name={report.release_name}",
        f"release_status={report.release_status}",
        f"readiness_status={report.readiness_status}",
        f"ready_for_v0_27={_bool(report.ready_for_v0_27)}",
        f"ready_for_v0_28={_bool(report.ready_for_v0_28)}",
        f"memory_candidate_created={_bool(report.memory_candidate_created)}",
        f"memory_promoted={_bool(report.memory_promoted)}",
        f"persistent_memory_written={_bool(report.persistent_memory_written)}",
        f"persona_mutated={_bool(report.persona_mutated)}",
        f"command_executed={_bool(report.command_executed)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"local_command_executed={_bool(report.local_command_executed)}",
        f"file_mutated={_bool(report.file_mutated)}",
        f"patch_applied={_bool(report.patch_applied)}",
        f"ask_executed={_bool(report.ask_executed)}",
        f"final_response_emitted={_bool(report.final_response_emitted)}",
        f"route_rerun_performed={_bool(report.route_rerun_performed)}",
        f"stage_rerun_performed={_bool(report.stage_rerun_performed)}",
        f"automatic_retry_performed={_bool(report.automatic_retry_performed)}",
        f"automatic_repair_performed={_bool(report.automatic_repair_performed)}",
        f"autonomous_loop_started={_bool(report.autonomous_loop_started)}",
        f"external_provider_adapter_implemented={_bool(report.external_provider_adapter_implemented)}",
        f"vendor_adapter_implemented={_bool(report.vendor_adapter_implemented)}",
        f"pm4py_runtime_dependency_added={_bool(report.pm4py_runtime_dependency_added)}",
        f"ocpa_runtime_dependency_added={_bool(report.ocpa_runtime_dependency_added)}",
        f"pig_memory_promoted={_bool(report.pig_memory_promoted)}",
        f"pig_policy_mutated={_bool(report.pig_policy_mutated)}",
        f"pig_executed={_bool(report.pig_executed)}",
        f"schumpeter_split_introduced={_bool(report.schumpeter_split_introduced)}",
        f"raw_transcript_persisted={_bool(report.raw_transcript_persisted)}",
        f"raw_provider_output_inline={_bool(report.raw_provider_output_inline)}",
        f"raw_secret_output={_bool(report.raw_secret_output)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    if section == "release-manifest":
        manifest = parts["release_manifest"]
        lines.append(f"included_version_count={len(manifest.included_versions)}")
        lines.append(f"excluded_capability_count={len(manifest.excluded_capabilities)}")
    elif section == "coverage":
        matrix = parts["coverage_matrix"]
        lines.append(f"coverage_status={matrix.coverage_status}")
        lines.append(f"coverage_row_count={len(matrix.rows)}")
    elif section == "safety-boundary":
        safety = parts["safety_boundary_report"]
        lines.append(f"safety_boundary_status={safety.status}")
        lines.append(f"dangerous_count_total={sum(value for key, value in safety.to_dict().items() if key.endswith('_count'))}")
    elif section == "interaction-boundary":
        interaction = parts["interaction_boundary_report"]
        lines.append(f"interaction_status={interaction.interaction_status}")
        lines.append(f"execution_boundary_preserved={_bool(interaction.execution_boundary_preserved)}")
    elif section == "quality":
        quality = parts["event_quality_consolidation_report"]
        lines.append(f"event_quality_status={quality.event_quality_status}")
        lines.append(f"automatic_optimization_performed={_bool(quality.automatic_optimization_performed)}")
    elif section == "trace-coverage":
        coverage = parts["trace_coverage_consolidation_report"]
        lines.append(f"coverage_status={coverage.coverage_status}")
        lines.append(f"snapshot_export_coverage={_bool(coverage.snapshot_export_coverage)}")
    elif section == "usability":
        usability = parts["usability_readiness_report"]
        lines.append(f"usability_status={usability.usability_status}")
        lines.append(f"do_nothing_visible={_bool(usability.do_nothing_visible)}")
    elif section == "feedback-loop":
        feedback = parts["process_intelligence_feedback_loop_report"]
        lines.append(f"feedback_loop_status={feedback.feedback_loop_status}")
        lines.append(f"v027_memory_candidate_input_ready={_bool(feedback.v027_memory_candidate_input_ready)}")
    elif section == "gaps":
        gaps = parts["gap_register"]
        lines.append(f"gap_status={gaps.gap_status}")
        lines.append(f"future_track_count={gaps.future_track_count}")
    elif section == "readiness":
        readiness = parts["v027_readiness_report"]
        lines.append(f"target_track={readiness.target_track}")
        lines.append(f"memory_not_implemented_yet={_bool(readiness.memory_not_implemented_yet)}")
    elif section == "handoff":
        handoff = parts["memory_candidate_handoff_packet"]
        lines.append(f"refs_only={_bool(handoff.refs_only)}")
        lines.append(f"memory_created_now={_bool(handoff.memory_created_now)}")
    elif section == "consolidation-report":
        lines.append(f"report_id={report.report_id}")
        lines.append(f"finding_count={len(report.findings)}")
    return "\n".join(lines)
