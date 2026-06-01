from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace_agent_workbench.view_state import WorkbenchViewStateReportService


WORKBENCH_COMMAND_SURFACE_VERSION = "v0.26.7"
WORKBENCH_COMMAND_SURFACE_VERSION_NAME = "Workbench Command Surface"
WORKBENCH_COMMAND_SURFACE_KOREAN_NAME = "Workbench Command Surface"
WORKBENCH_COMMAND_SURFACE_LAYER = "workspace_agent_workbench"
WORKBENCH_COMMAND_SURFACE_TRACK = "Workspace Agent Workbench"
WORKBENCH_COMMAND_SURFACE_NEXT_STEP = "v0.26.8 Workbench Snapshot / OCEL Export"

WORKBENCH_COMMAND_SURFACE_IMPLEMENTED_SKILL_IDS = [
    "skill:workbench_command_surface_use",
]
WORKBENCH_COMMAND_SURFACE_FUTURE_SKILL_IDS = [
    "skill:workbench_snapshot_create",
    "skill:workbench_ocel_export_create",
    "skill:workbench_consolidation_view",
]

WORKBENCH_COMMAND_SURFACE_OBJECT_TYPES = [
    "workbench_command_surface_policy",
    "workbench_command_surface_request",
    "workbench_command_source_view",
    "workbench_command_surface_view",
    "workbench_command_type_policy",
    "workbench_command_request",
    "workbench_command_candidate",
    "workbench_do_nothing_candidate",
    "workbench_skill_candidate",
    "workbench_action_candidate",
    "workbench_route_candidate",
    "workbench_provider_candidate_ref",
    "workbench_file_edit_candidate",
    "workbench_ask_pipeline_candidate",
    "workbench_snapshot_request_candidate",
    "workbench_command_candidate_rationale",
    "workbench_command_evidence_bundle",
    "workbench_command_risk_summary",
    "workbench_command_pig_guidance_view",
    "workbench_command_safety_finding_view",
    "workbench_command_approval_requirement",
    "workbench_command_boundary_trace",
    "workbench_command_decision",
    "workbench_command_decision_record",
    "workbench_command_execution_envelope",
    "workbench_command_result",
    "workbench_command_history_entry",
    "workbench_command_audit_trail",
    "workbench_command_surface_finding",
    "workbench_command_surface_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

WORKBENCH_COMMAND_SURFACE_EVENT_TYPES = [
    "workbench_command_surface_requested",
    "workbench_command_surface_policy_created",
    "workbench_command_source_view_created",
    "workbench_command_type_policy_created",
    "workbench_command_surface_view_created",
    "workbench_command_request_created",
    "workbench_command_candidate_created",
    "workbench_do_nothing_candidate_created",
    "workbench_skill_candidate_created",
    "workbench_action_candidate_created",
    "workbench_route_candidate_created",
    "workbench_provider_candidate_ref_created",
    "workbench_file_edit_candidate_created",
    "workbench_ask_pipeline_candidate_created",
    "workbench_snapshot_request_candidate_created",
    "workbench_command_rationale_created",
    "workbench_command_evidence_bundle_created",
    "workbench_command_risk_summary_created",
    "workbench_command_pig_guidance_attached",
    "workbench_command_safety_finding_attached",
    "workbench_command_approval_requirement_created",
    "workbench_command_boundary_trace_created",
    "workbench_command_decision_recorded",
    "workbench_command_execution_envelope_created",
    "workbench_command_result_created",
    "workbench_command_history_recorded",
    "workbench_command_audit_trail_created",
    "workbench_command_surface_report_created",
    "workbench_command_surface_warning_created",
    "workbench_command_surface_blocked",
]

WORKBENCH_COMMAND_SURFACE_RELATION_TYPES = [
    "uses_workbench_view_state",
    "uses_command_surface_panel",
    "uses_run_dashboard_report",
    "uses_approval_console_report",
    "uses_evidence_inspector_report",
    "uses_provider_browser_report",
    "uses_trace_explorer_report",
    "uses_skill_registry_ref",
    "uses_provider_registry_ref",
    "uses_pig_guidance_ref",
    "creates_command_surface_view",
    "creates_command_candidate",
    "creates_do_nothing_candidate",
    "creates_skill_candidate",
    "creates_action_candidate",
    "creates_route_candidate",
    "creates_provider_candidate_ref",
    "creates_command_boundary_trace",
    "creates_command_decision_record",
    "creates_command_history_entry",
    "creates_command_audit_trail",
    "defers_snapshot_export_to_v0_26_8",
    "defers_memory_continuity_to_v0_27",
    "not_direct_command_executed",
    "not_provider_invoked",
    "not_file_mutated",
    "not_ask_executed",
    "not_pig_memory_promoted",
    "not_pig_policy_mutated",
    "not_pig_executed",
    "blocks_raw_provider_output_inline",
    "blocks_raw_transcript_persistence",
    "recorded_in_envelope",
]

WORKBENCH_COMMAND_SURFACE_EFFECT_TYPES = [
    "read_only_observation",
    "workbench_command_surface_created",
    "workbench_command_candidate_created",
    "workbench_do_nothing_candidate_created",
    "workbench_skill_candidate_created",
    "workbench_action_candidate_created",
    "workbench_route_candidate_created",
    "workbench_command_boundary_trace_created",
    "workbench_command_decision_recorded",
    "workbench_command_history_recorded",
    "workbench_command_audit_trail_created",
    "state_candidate_created",
]

WORKBENCH_COMMAND_SURFACE_FORBIDDEN_EFFECT_TYPES = [
    "direct_command_executed",
    "command_dispatched",
    "provider_invoked",
    "internal_provider_invoked",
    "provider_test_run_performed",
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
    "approval_executed",
    "approval_token_executed",
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

ALLOWED_COMMAND_DECISIONS = [
    "approve_candidate",
    "reject_candidate",
    "defer_candidate",
    "request_more_evidence",
    "request_clarification",
    "choose_do_nothing",
    "mark_inspection_only",
    "unknown",
]


def _safe_id(value: str | None) -> str:
    text = value or "unknown"
    return "".join(char if char.isalnum() else "_" for char in text).strip("_").lower() or "unknown"


def _ref(ref_type: str, ref_id: str, version: str = WORKBENCH_COMMAND_SURFACE_VERSION) -> dict[str, Any]:
    return {"type": ref_type, "id": ref_id, "version": version}


def _model_ref(ref_type: str, model: Any, id_attr: str) -> dict[str, Any]:
    return _ref(ref_type, getattr(model, id_attr), getattr(model, "version", WORKBENCH_COMMAND_SURFACE_VERSION))


class _ModelMixin:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class WorkbenchCommandSurfacePolicy(_ModelMixin):
    policy_id: str
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    layer: str = WORKBENCH_COMMAND_SURFACE_LAYER
    command_surface_enabled: bool = True
    command_candidate_enabled: bool = True
    skill_candidate_enabled: bool = True
    action_candidate_enabled: bool = True
    route_candidate_enabled: bool = True
    provider_candidate_enabled: bool = True
    ask_pipeline_candidate_enabled: bool = True
    file_edit_candidate_enabled: bool = True
    snapshot_request_candidate_enabled: bool = True
    do_nothing_candidate_enabled: bool = True
    command_decision_record_enabled: bool = True
    command_history_enabled: bool = True
    command_audit_trail_enabled: bool = True
    actual_ui_rendering_enabled: bool = False
    panel_rendering_enabled: bool = False
    direct_command_execution_enabled: bool = False
    provider_invocation_enabled: bool = False
    local_runtime_execution_enabled: bool = False
    file_mutation_enabled: bool = False
    patch_application_enabled: bool = False
    ask_execution_enabled: bool = False
    response_emission_enabled: bool = False
    route_rerun_enabled: bool = False
    stage_rerun_enabled: bool = False
    automatic_retry_enabled: bool = False
    automatic_repair_enabled: bool = False
    autonomous_loop_enabled: bool = False
    approval_execution_enabled: bool = False
    memory_promotion_enabled: bool = False
    persistent_memory_write_enabled: bool = False
    persona_mutation_enabled: bool = False
    external_adapter_enabled: bool = False
    command_requires_evidence_refs: bool = True
    command_requires_risk_summary: bool = True
    command_requires_boundary_trace: bool = True
    risky_command_requires_approval_requirement: bool = True
    do_nothing_alternative_required: bool = True
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
class WorkbenchCommandSurfaceRequest(_ModelMixin):
    request_id: str
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    view_state_report_id: str | None = None
    view_state_id: str | None = None
    command_surface_panel_id: str | None = None
    dashboard_report_id: str | None = None
    approval_console_report_id: str | None = None
    evidence_inspector_report_id: str | None = None
    provider_browser_report_id: str | None = None
    trace_explorer_report_id: str | None = None
    user_intent_ref: dict[str, Any] | None = None
    requested_command_type: str | None = None
    requested_subject_refs: list[dict[str, Any]] = field(default_factory=list)
    pig_guidance_refs: list[dict[str, Any]] = field(default_factory=list)
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"


@dataclass
class WorkbenchCommandSourceView(_ModelMixin):
    source_view_id: str
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    dashboard_report_refs: list[dict[str, Any]] = field(default_factory=list)
    approval_report_refs: list[dict[str, Any]] = field(default_factory=list)
    evidence_report_refs: list[dict[str, Any]] = field(default_factory=list)
    provider_report_refs: list[dict[str, Any]] = field(default_factory=list)
    trace_report_refs: list[dict[str, Any]] = field(default_factory=list)
    skill_registry_refs: list[dict[str, Any]] = field(default_factory=list)
    provider_registry_refs: list[dict[str, Any]] = field(default_factory=list)
    approval_candidate_refs: list[dict[str, Any]] = field(default_factory=list)
    pig_guidance_refs: list[dict[str, Any]] = field(default_factory=list)
    user_intent_refs: list[dict[str, Any]] = field(default_factory=list)
    source_status: str = "complete"
    raw_provider_output_included: bool = False
    raw_transcript_included: bool = False
    raw_secret_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchCommandTypePolicy(_ModelMixin):
    policy_id: str
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    allowed_candidate_types: list[str] = field(default_factory=lambda: [
        "inspect_trace",
        "inspect_provider",
        "inspect_evidence",
        "inspect_safety",
        "inspect_dashboard",
        "create_approval_candidate",
        "create_snapshot_request_candidate",
        "propose_skill_action",
        "ask_pipeline_candidate",
        "provider_invocation_candidate",
        "local_runtime_candidate",
        "file_edit_candidate",
        "do_nothing",
    ])
    forbidden_executable_types: list[str] = field(default_factory=lambda: [
        "direct_command_execution",
        "provider_invocation",
        "local_runtime_execution",
        "file_mutation",
        "ask_execution",
        "snapshot_export",
    ])
    default_to_candidate_only: bool = True
    do_nothing_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchCommandRequest(_ModelMixin):
    command_request_id: str
    command_type: str
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    user_intent_ref: dict[str, Any] | None = None
    subject_refs: list[dict[str, Any]] = field(default_factory=list)
    requested_by: str = "user"
    request_status: str = "accepted_for_candidate"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSkillCandidate(_ModelMixin):
    skill_candidate_id: str
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    skill_id: str | None = None
    skill_name: str | None = None
    candidate_reason: str = ""
    source_skill_registry_ref: dict[str, Any] | None = None
    task_frame_refs: list[dict[str, Any]] = field(default_factory=list)
    pig_guidance_refs: list[dict[str, Any]] = field(default_factory=list)
    safety_finding_refs: list[dict[str, Any]] = field(default_factory=list)
    selected: bool = False
    rejected: bool = False
    deferred: bool = False
    skill_executed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchActionCandidate(_ModelMixin):
    action_candidate_id: str
    action_type: str
    action_summary: str
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    rationale_refs: list[dict[str, Any]] = field(default_factory=list)
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    risk_refs: list[dict[str, Any]] = field(default_factory=list)
    approval_requirement_refs: list[dict[str, Any]] = field(default_factory=list)
    action_executed_now: bool = False
    file_mutated_now: bool = False
    provider_invoked_now: bool = False


@dataclass
class WorkbenchRouteCandidate(_ModelMixin):
    route_candidate_id: str
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    route_kind: str | None = None
    route_summary: str = ""
    route_context_refs: list[dict[str, Any]] = field(default_factory=list)
    provider_candidate_refs: list[dict[str, Any]] = field(default_factory=list)
    route_compatibility_refs: list[dict[str, Any]] = field(default_factory=list)
    safety_refs: list[dict[str, Any]] = field(default_factory=list)
    route_executed_now: bool = False
    route_rerun_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchProviderCandidateRef(_ModelMixin):
    provider_candidate_ref_id: str
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    provider_id: str | None = None
    capability_id: str | None = None
    provider_browser_ref: dict[str, Any] | None = None
    provider_selection_rationale_refs: list[dict[str, Any]] = field(default_factory=list)
    boundary_risk_refs: list[dict[str, Any]] = field(default_factory=list)
    readiness_refs: list[dict[str, Any]] = field(default_factory=list)
    provider_invoked_now: bool = False
    provider_test_run_performed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchFileEditCandidate(_ModelMixin):
    file_edit_candidate_id: str
    edit_summary: str
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    target_file_ref: dict[str, Any] | None = None
    patch_proposal_ref: dict[str, Any] | None = None
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    approval_required: bool = True
    file_mutated_now: bool = False
    patch_applied_now: bool = False


@dataclass
class WorkbenchAskPipelineCandidate(_ModelMixin):
    ask_pipeline_candidate_id: str
    ask_request_summary: str
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    target_surface: str = "v0.25.7 ask surface"
    required_boundary_refs: list[dict[str, Any]] = field(default_factory=list)
    execution_deferred_to_boundary: bool = True
    ask_executed_now: bool = False
    final_response_emitted_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSnapshotRequestCandidate(_ModelMixin):
    snapshot_request_candidate_id: str
    snapshot_summary: str
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    target_version: str = "v0.26.8"
    selected_ref_candidates: list[dict[str, Any]] = field(default_factory=list)
    snapshot_created_now: bool = False
    ocel_export_created_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchCommandCandidateRationale(_ModelMixin):
    rationale_id: str
    summary: str
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    reason_refs: list[dict[str, Any]] = field(default_factory=list)
    decision_evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    skill_selection_refs: list[dict[str, Any]] = field(default_factory=list)
    route_selection_refs: list[dict[str, Any]] = field(default_factory=list)
    provider_selection_refs: list[dict[str, Any]] = field(default_factory=list)
    pig_guidance_refs: list[dict[str, Any]] = field(default_factory=list)
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchCommandEvidenceBundle(_ModelMixin):
    command_evidence_bundle_id: str
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    claim_refs: list[dict[str, Any]] = field(default_factory=list)
    safety_refs: list[dict[str, Any]] = field(default_factory=list)
    provider_refs: list[dict[str, Any]] = field(default_factory=list)
    approval_refs: list[dict[str, Any]] = field(default_factory=list)
    pig_guidance_refs: list[dict[str, Any]] = field(default_factory=list)
    evidence_count: int = 0
    evidence_status: str = "partial"
    raw_provider_output_included: bool = False
    raw_transcript_included: bool = False
    raw_secret_included: bool = False


@dataclass
class WorkbenchCommandRiskSummary(_ModelMixin):
    command_risk_summary_id: str
    risk_level: str
    risk_categories: list[str]
    risk_summary: str
    approval_required: bool
    do_nothing_preferred: bool
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    mitigation_refs: list[dict[str, Any]] = field(default_factory=list)
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchCommandPIGGuidanceView(_ModelMixin):
    command_pig_guidance_view_id: str
    guidance_summary: str
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    pig_guidance_refs: list[dict[str, Any]] = field(default_factory=list)
    pig_guidance_is_memory: bool = False
    pig_guidance_mutates_policy: bool = False
    pig_guidance_executes: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchCommandSafetyFindingView(_ModelMixin):
    command_safety_finding_view_id: str
    safety_summary: str
    blocked: bool
    requires_approval: bool
    requires_clarification: bool
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    safety_finding_refs: list[dict[str, Any]] = field(default_factory=list)
    safety_policy_mutated_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchCommandApprovalRequirement(_ModelMixin):
    command_approval_requirement_id: str
    approval_required: bool
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    approval_candidate_refs: list[dict[str, Any]] = field(default_factory=list)
    approval_scope_refs: list[dict[str, Any]] = field(default_factory=list)
    approval_expiry_refs: list[dict[str, Any]] = field(default_factory=list)
    missing_approval_reason: str | None = None
    approval_execution_performed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchCommandBoundaryTrace(_ModelMixin):
    command_boundary_trace_id: str
    command_candidate_id: str
    required_boundaries: list[str]
    boundary_summary: str
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    allowed_boundary_refs: list[dict[str, Any]] = field(default_factory=list)
    forbidden_boundary_refs: list[dict[str, Any]] = field(default_factory=list)
    boundary_bypassed: bool = False
    execution_performed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchCommandCandidate(_ModelMixin):
    command_candidate_id: str
    command_type: str
    title: str
    summary: str
    rationale: WorkbenchCommandCandidateRationale
    evidence_bundle: WorkbenchCommandEvidenceBundle
    risk_summary: WorkbenchCommandRiskSummary
    boundary_trace: WorkbenchCommandBoundaryTrace
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    user_intent_refs: list[dict[str, Any]] = field(default_factory=list)
    subject_refs: list[dict[str, Any]] = field(default_factory=list)
    skill_candidate_refs: list[dict[str, Any]] = field(default_factory=list)
    action_candidate_refs: list[dict[str, Any]] = field(default_factory=list)
    route_candidate_refs: list[dict[str, Any]] = field(default_factory=list)
    provider_candidate_refs: list[dict[str, Any]] = field(default_factory=list)
    file_edit_candidate_refs: list[dict[str, Any]] = field(default_factory=list)
    ask_pipeline_candidate_ref: dict[str, Any] | None = None
    snapshot_request_candidate_ref: dict[str, Any] | None = None
    pig_guidance_view: WorkbenchCommandPIGGuidanceView | None = None
    safety_finding_view: WorkbenchCommandSafetyFindingView | None = None
    approval_requirement: WorkbenchCommandApprovalRequirement | None = None
    candidate_status: str = "ready_for_review"
    executable_now: bool = False
    executed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchDoNothingCandidate(_ModelMixin):
    do_nothing_candidate_id: str
    reason: str
    when_preferred: str
    risk_reduction_summary: str
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    alternative_to_candidate_refs: list[dict[str, Any]] = field(default_factory=list)
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    selected_now: bool = False
    execution_triggered: bool = False


@dataclass
class WorkbenchCommandDecision(_ModelMixin):
    command_decision_id: str
    command_candidate_id: str
    decision_type: str
    decision_reason: str
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    decided_by: str = "system_test_fixture"
    creates_execution: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchCommandDecisionRecord(_ModelMixin):
    command_decision_record_id: str
    decision: WorkbenchCommandDecision
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    record_status: str = "recorded"
    ocel_visible: bool = True
    execution_triggered: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchCommandExecutionEnvelope(_ModelMixin):
    command_execution_envelope_id: str
    command_candidate_id: str
    boundary_trace_id: str
    envelope_status: str
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    dispatch_target: str | None = None
    dispatch_deferred: bool = True
    dispatch_performed_now: bool = False
    provider_invoked_now: bool = False
    local_command_executed_now: bool = False
    file_mutated_now: bool = False
    ask_executed_now: bool = False
    final_response_emitted_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchCommandResult(_ModelMixin):
    command_result_id: str
    command_candidate_id: str
    result_type: str
    result_summary: str
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    result_refs: list[dict[str, Any]] = field(default_factory=list)
    external_execution_result: bool = False
    provider_invocation_result: bool = False
    local_command_result: bool = False
    file_mutation_result: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchCommandHistoryEntry(_ModelMixin):
    command_history_entry_id: str
    command_candidate_ref: dict[str, Any]
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    decision_record_ref: dict[str, Any] | None = None
    result_ref: dict[str, Any] | None = None
    timestamp: str | None = None
    sanitized: bool = True
    raw_secret_included: bool = False
    raw_provider_output_included: bool = False
    raw_transcript_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchCommandAuditTrail(_ModelMixin):
    command_audit_trail_id: str
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    command_candidate_refs: list[dict[str, Any]] = field(default_factory=list)
    command_decision_record_refs: list[dict[str, Any]] = field(default_factory=list)
    command_result_refs: list[dict[str, Any]] = field(default_factory=list)
    do_nothing_candidate_refs: list[dict[str, Any]] = field(default_factory=list)
    boundary_trace_refs: list[dict[str, Any]] = field(default_factory=list)
    audit_event_count: int = 0
    audit_status: str = "ready"
    raw_secret_included: bool = False
    raw_provider_output_included: bool = False
    raw_transcript_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchCommandSurfaceView(_ModelMixin):
    command_surface_view_id: str
    source_view: WorkbenchCommandSourceView
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    panel_id: str | None = None
    command_candidates: list[WorkbenchCommandCandidate] = field(default_factory=list)
    do_nothing_candidates: list[WorkbenchDoNothingCandidate] = field(default_factory=list)
    skill_candidates: list[WorkbenchSkillCandidate] = field(default_factory=list)
    action_candidates: list[WorkbenchActionCandidate] = field(default_factory=list)
    route_candidates: list[WorkbenchRouteCandidate] = field(default_factory=list)
    provider_candidate_refs: list[WorkbenchProviderCandidateRef] = field(default_factory=list)
    command_decisions: list[WorkbenchCommandDecision] = field(default_factory=list)
    command_results: list[WorkbenchCommandResult] = field(default_factory=list)
    command_history: list[WorkbenchCommandHistoryEntry] = field(default_factory=list)
    audit_trail: WorkbenchCommandAuditTrail | None = None
    view_status: str = "ready"
    renders_ui_now: bool = False
    direct_command_executed: bool = False
    provider_invoked: bool = False
    local_command_executed: bool = False
    file_mutated: bool = False
    ask_executed: bool = False
    final_response_emitted: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchCommandSurfaceFinding(_ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None = None
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    withdrawal_condition: str | None = None


@dataclass
class WorkbenchCommandSurfaceReport(_ModelMixin):
    report_id: str
    created_at: str
    command_surface_policy: WorkbenchCommandSurfacePolicy
    request: WorkbenchCommandSurfaceRequest
    source_view: WorkbenchCommandSourceView
    command_surface_view: WorkbenchCommandSurfaceView
    command_type_policy: WorkbenchCommandTypePolicy
    audit_trail: WorkbenchCommandAuditTrail
    findings: list[WorkbenchCommandSurfaceFinding]
    report_status: str
    ready_for_v0_26_8: bool
    command_surface_view_created: bool
    command_candidates_created: bool
    do_nothing_candidates_created: bool
    skill_candidates_created: bool
    action_candidates_created: bool
    route_candidates_created: bool
    provider_candidate_refs_created: bool
    file_edit_candidates_created: bool
    ask_pipeline_candidates_created: bool
    snapshot_request_candidates_created: bool
    command_decisions_recorded: bool
    command_history_created: bool
    audit_trail_created: bool
    version: str = WORKBENCH_COMMAND_SURFACE_VERSION
    ready_for_v0_27: bool = False
    actual_ui_rendered: bool = False
    panel_rendered: bool = False
    direct_command_executed: bool = False
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
    approval_executed: bool = False
    approval_token_executed: bool = False
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
    next_required_step: str = WORKBENCH_COMMAND_SURFACE_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = (
        "Valid until v0.26.8 Workbench Snapshot / OCEL Export begins or command surface policy changes."
    )


class WorkbenchCommandSurfacePrerequisiteSourceService:
    def __init__(
        self,
        *,
        view_state_available: bool = True,
        command_surface_panel_available: bool = True,
        dashboard_report_available: bool = True,
        approval_console_available: bool = True,
        evidence_inspector_available: bool = True,
        provider_browser_available: bool = True,
        trace_explorer_available: bool = True,
        skill_registry_available: bool = True,
        provider_registry_available: bool = True,
        pig_guidance_available: bool = True,
        user_intent_available: bool = True,
    ) -> None:
        self.view_state_available = view_state_available
        self.command_surface_panel_available = command_surface_panel_available
        self.dashboard_report_available = dashboard_report_available
        self.approval_console_available = approval_console_available
        self.evidence_inspector_available = evidence_inspector_available
        self.provider_browser_available = provider_browser_available
        self.trace_explorer_available = trace_explorer_available
        self.skill_registry_available = skill_registry_available
        self.provider_registry_available = provider_registry_available
        self.pig_guidance_available = pig_guidance_available
        self.user_intent_available = user_intent_available

    def load_workbench_view_state(self) -> dict[str, Any] | None:
        if not self.view_state_available:
            return None
        parts = WorkbenchViewStateReportService().build_all_parts()
        return {
            "view_state_report": _model_ref("workbench_view_state_report", parts["report"], "report_id"),
            "view_state": _model_ref("workbench_view_state", parts["view_state"], "view_state_id"),
        }

    def load_command_surface_panel_model(self) -> dict[str, Any] | None:
        if not self.command_surface_panel_available:
            return None
        return _ref("workbench_panel", "workbench_panel:command_surface", "v0.26.1")

    def load_dashboard_report_if_available(self) -> list[dict[str, Any]]:
        if not self.dashboard_report_available:
            return []
        return [_ref("workbench_run_dashboard_report", "workbench_run_dashboard_report:v0.26.6:existing", "v0.26.6")]

    def load_approval_console_report_if_available(self) -> list[dict[str, Any]]:
        if not self.approval_console_available:
            return []
        return [_ref("workbench_approval_console_report", "workbench_approval_console_report:v0.26.5:existing", "v0.26.5")]

    def load_evidence_inspector_report_if_available(self) -> list[dict[str, Any]]:
        if not self.evidence_inspector_available:
            return []
        return [_ref("workbench_evidence_inspector_report", "workbench_evidence_inspector_report:v0.26.4:existing", "v0.26.4")]

    def load_provider_browser_report_if_available(self) -> list[dict[str, Any]]:
        if not self.provider_browser_available:
            return []
        return [_ref("workbench_provider_browser_report", "workbench_provider_browser_report:v0.26.3:existing", "v0.26.3")]

    def load_trace_explorer_report_if_available(self) -> list[dict[str, Any]]:
        if not self.trace_explorer_available:
            return []
        return [_ref("workbench_trace_explorer_report", "workbench_trace_explorer_report:v0.26.2:existing", "v0.26.2")]

    def load_skill_registry_if_available(self) -> list[dict[str, Any]]:
        if not self.skill_registry_available:
            return []
        return [_ref("skill_registry", "skill_registry:workbench_command_surface:read_only")]

    def load_provider_registry_if_available(self) -> list[dict[str, Any]]:
        if not self.provider_registry_available:
            return []
        return [_ref("internal_provider_registry", "internal_provider_registry:v0.24.9", "v0.24.9")]

    def load_pig_guidance_refs_if_available(self) -> list[dict[str, Any]]:
        if not self.pig_guidance_available:
            return []
        return [
            _ref("pig_guidance", "pig_guidance:workbench_command_candidate_boundary"),
            _ref("pig_guidance", "pig_guidance:do_nothing_safe_alternative"),
        ]

    def load_user_intent_refs_if_available(self) -> list[dict[str, Any]]:
        if not self.user_intent_available:
            return []
        return [_ref("agent_task_frame", "agent_task_frame:v0.25.2:existing", "v0.25.2")]


class WorkbenchCommandSurfacePolicyService:
    def build_policy(self) -> WorkbenchCommandSurfacePolicy:
        return WorkbenchCommandSurfacePolicy(policy_id="workbench_command_surface_policy:v0.26.7")


class WorkbenchCommandSurfaceRequestService:
    def build_request(
        self,
        *,
        source_service: WorkbenchCommandSurfacePrerequisiteSourceService,
        report_id: str | None = None,
        requested_command_type: str | None = None,
        strictness: str = "standard",
    ) -> WorkbenchCommandSurfaceRequest:
        view_state = source_service.load_workbench_view_state() or {}
        panel = source_service.load_command_surface_panel_model()
        dashboard_refs = source_service.load_dashboard_report_if_available()
        approval_refs = source_service.load_approval_console_report_if_available()
        evidence_refs = source_service.load_evidence_inspector_report_if_available()
        provider_refs = source_service.load_provider_browser_report_if_available()
        trace_refs = source_service.load_trace_explorer_report_if_available()
        user_intent_refs = source_service.load_user_intent_refs_if_available()
        pig_refs = source_service.load_pig_guidance_refs_if_available()
        request_id = report_id or "workbench_command_surface_request:v0.26.7"
        source_refs = [
            *(dashboard_refs + approval_refs + evidence_refs + provider_refs + trace_refs),
            *pig_refs,
            *user_intent_refs,
        ]
        return WorkbenchCommandSurfaceRequest(
            request_id=request_id,
            view_state_report_id=(view_state.get("view_state_report") or {}).get("id"),
            view_state_id=(view_state.get("view_state") or {}).get("id"),
            command_surface_panel_id=(panel or {}).get("id"),
            dashboard_report_id=(dashboard_refs[0]["id"] if dashboard_refs else None),
            approval_console_report_id=(approval_refs[0]["id"] if approval_refs else None),
            evidence_inspector_report_id=(evidence_refs[0]["id"] if evidence_refs else None),
            provider_browser_report_id=(provider_refs[0]["id"] if provider_refs else None),
            trace_explorer_report_id=(trace_refs[0]["id"] if trace_refs else None),
            user_intent_ref=(user_intent_refs[0] if user_intent_refs else None),
            requested_command_type=requested_command_type or "inspect_dashboard",
            requested_subject_refs=source_refs[:3],
            pig_guidance_refs=pig_refs,
            source_refs=source_refs,
            strictness=strictness,
        )


class WorkbenchCommandSourceViewService:
    def build_source_view(
        self,
        source_service: WorkbenchCommandSurfacePrerequisiteSourceService,
        request: WorkbenchCommandSurfaceRequest,
    ) -> WorkbenchCommandSourceView:
        dashboard_refs = source_service.load_dashboard_report_if_available()
        approval_refs = source_service.load_approval_console_report_if_available()
        evidence_refs = source_service.load_evidence_inspector_report_if_available()
        provider_refs = source_service.load_provider_browser_report_if_available()
        trace_refs = source_service.load_trace_explorer_report_if_available()
        skill_refs = source_service.load_skill_registry_if_available()
        registry_refs = source_service.load_provider_registry_if_available()
        pig_refs = source_service.load_pig_guidance_refs_if_available()
        user_intent_refs = source_service.load_user_intent_refs_if_available()
        approval_candidate_refs = [
            _ref("workbench_approval_candidate", "workbench_approval_candidate:v0.26.5:existing", "v0.26.5")
        ] if approval_refs else []
        mandatory_present = bool(source_service.load_workbench_view_state()) and bool(
            source_service.load_command_surface_panel_model()
        )
        refs_present = any([dashboard_refs, approval_refs, evidence_refs, provider_refs, trace_refs])
        source_status = "complete" if mandatory_present and refs_present else "partial"
        if request.strictness == "strict" and not mandatory_present:
            source_status = "missing"
        return WorkbenchCommandSourceView(
            source_view_id="workbench_command_source_view:v0.26.7",
            dashboard_report_refs=dashboard_refs,
            approval_report_refs=approval_refs,
            evidence_report_refs=evidence_refs,
            provider_report_refs=provider_refs,
            trace_report_refs=trace_refs,
            skill_registry_refs=skill_refs,
            provider_registry_refs=registry_refs,
            approval_candidate_refs=approval_candidate_refs,
            pig_guidance_refs=pig_refs,
            user_intent_refs=user_intent_refs,
            source_status=source_status,
            evidence_refs=request.source_refs,
        )


class WorkbenchCommandTypePolicyService:
    def build_policy(self) -> WorkbenchCommandTypePolicy:
        return WorkbenchCommandTypePolicy(policy_id="workbench_command_type_policy:v0.26.7")


class WorkbenchSkillCandidateService:
    def build_skill_candidates(self, source_view: WorkbenchCommandSourceView) -> list[WorkbenchSkillCandidate]:
        if not source_view.skill_registry_refs:
            return []
        return [
            WorkbenchSkillCandidate(
                skill_candidate_id="workbench_skill_candidate:workbench_command_surface_use",
                skill_id="skill:workbench_command_surface_use",
                skill_name="workbench_command_surface_use",
                candidate_reason="Represent command-surface candidate creation without executing the skill.",
                source_skill_registry_ref=source_view.skill_registry_refs[0],
                task_frame_refs=source_view.user_intent_refs,
                pig_guidance_refs=source_view.pig_guidance_refs,
                evidence_refs=source_view.evidence_refs,
            )
        ]


class WorkbenchActionCandidateService:
    def build_action_candidates(self, source_view: WorkbenchCommandSourceView) -> list[WorkbenchActionCandidate]:
        evidence_refs = source_view.evidence_refs or [_ref("workbench_command_surface_policy", "refs_only_default")]
        return [
            WorkbenchActionCandidate(
                action_candidate_id="workbench_action_candidate:inspect_dashboard",
                action_type="inspect",
                action_summary="Inspect dashboard/session/approval refs through a command candidate only.",
                rationale_refs=source_view.dashboard_report_refs,
                evidence_refs=evidence_refs,
                risk_refs=[_ref("workbench_command_risk_summary", "workbench_command_risk_summary:inspect_dashboard")],
            ),
            WorkbenchActionCandidate(
                action_candidate_id="workbench_action_candidate:create_snapshot_request_candidate",
                action_type="snapshot_request",
                action_summary="Create a future snapshot request candidate without exporting now.",
                rationale_refs=source_view.trace_report_refs,
                evidence_refs=evidence_refs,
                risk_refs=[_ref("workbench_command_risk_summary", "workbench_command_risk_summary:snapshot_request")],
            ),
        ]


class WorkbenchRouteCandidateService:
    def build_route_candidates(self, source_view: WorkbenchCommandSourceView) -> list[WorkbenchRouteCandidate]:
        return [
            WorkbenchRouteCandidate(
                route_candidate_id="workbench_route_candidate:inspection_only",
                route_kind="inspection_only",
                route_summary="Route candidate remains a workbench inspection route and is not executed.",
                route_context_refs=source_view.trace_report_refs,
                provider_candidate_refs=[],
                route_compatibility_refs=source_view.provider_report_refs,
                safety_refs=source_view.approval_report_refs,
                evidence_refs=source_view.evidence_refs,
            )
        ]


class WorkbenchProviderCandidateRefService:
    def build_provider_candidate_refs(self, source_view: WorkbenchCommandSourceView) -> list[WorkbenchProviderCandidateRef]:
        return [
            WorkbenchProviderCandidateRef(
                provider_candidate_ref_id="workbench_provider_candidate_ref:inspection_provider",
                provider_id="provider_ref_only",
                capability_id="capability_ref_only",
                provider_browser_ref=(source_view.provider_report_refs[0] if source_view.provider_report_refs else None),
                provider_selection_rationale_refs=source_view.provider_report_refs,
                boundary_risk_refs=[_ref("risk", "provider_boundary_ref_only")],
                readiness_refs=source_view.provider_registry_refs,
                evidence_refs=source_view.evidence_refs,
            )
        ] if source_view.provider_report_refs or source_view.provider_registry_refs else []


class WorkbenchFileEditCandidateService:
    def build_file_edit_candidates(self, source_view: WorkbenchCommandSourceView) -> list[WorkbenchFileEditCandidate]:
        return [
            WorkbenchFileEditCandidate(
                file_edit_candidate_id="workbench_file_edit_candidate:proposal_only",
                edit_summary="File edit candidate is represented only as a proposed ref; no file is mutated.",
                target_file_ref=_ref("file_ref", "sanitized_target_file_ref"),
                patch_proposal_ref=_ref("patch_proposal_ref", "patch_proposal_ref:candidate_only"),
                evidence_refs=source_view.evidence_refs,
            )
        ]


class WorkbenchAskPipelineCandidateService:
    def build_ask_pipeline_candidates(self, source_view: WorkbenchCommandSourceView) -> list[WorkbenchAskPipelineCandidate]:
        return [
            WorkbenchAskPipelineCandidate(
                ask_pipeline_candidate_id="workbench_ask_pipeline_candidate:v0.25.7_boundary",
                ask_request_summary="Ask pipeline candidate is deferred to the v0.25.7 ask surface boundary.",
                required_boundary_refs=[_ref("agent_ask_repl_report", "agent_ask_repl_report:v0.25.7:boundary", "v0.25.7")],
                evidence_refs=source_view.evidence_refs,
            )
        ]


class WorkbenchSnapshotRequestCandidateService:
    def build_snapshot_request_candidates(
        self, source_view: WorkbenchCommandSourceView
    ) -> list[WorkbenchSnapshotRequestCandidate]:
        return [
            WorkbenchSnapshotRequestCandidate(
                snapshot_request_candidate_id="workbench_snapshot_request_candidate:v0.26.8_future",
                snapshot_summary="Snapshot request candidate is deferred to v0.26.8 and does not export now.",
                selected_ref_candidates=source_view.dashboard_report_refs + source_view.approval_report_refs,
                evidence_refs=source_view.evidence_refs,
            )
        ]


class WorkbenchDoNothingCandidateService:
    def build_do_nothing_candidates(self, command_candidate_refs: list[dict[str, Any]]) -> list[WorkbenchDoNothingCandidate]:
        return [
            WorkbenchDoNothingCandidate(
                do_nothing_candidate_id="workbench_do_nothing_candidate:safe_alternative",
                reason="No execution is required to preserve the workbench command surface boundary.",
                when_preferred="Prefer when evidence is incomplete, risk is unclear, or human approval is absent.",
                risk_reduction_summary="Avoids provider invocation, local runtime execution, file mutation, and ask/repl execution.",
                alternative_to_candidate_refs=command_candidate_refs,
                evidence_refs=command_candidate_refs,
            )
        ]


class WorkbenchCommandCandidateRationaleService:
    def build_rationale(self, source_view: WorkbenchCommandSourceView) -> WorkbenchCommandCandidateRationale:
        return WorkbenchCommandCandidateRationale(
            rationale_id="workbench_command_candidate_rationale:inspect_dashboard",
            summary="Use a command candidate to inspect prior workbench refs while preserving non-execution boundaries.",
            reason_refs=source_view.dashboard_report_refs + source_view.approval_report_refs,
            decision_evidence_refs=source_view.evidence_report_refs,
            skill_selection_refs=source_view.skill_registry_refs,
            route_selection_refs=source_view.trace_report_refs,
            provider_selection_refs=source_view.provider_report_refs,
            pig_guidance_refs=source_view.pig_guidance_refs,
            evidence_refs=source_view.evidence_refs,
        )


class WorkbenchCommandEvidenceBundleService:
    def build_evidence_bundle(self, source_view: WorkbenchCommandSourceView) -> WorkbenchCommandEvidenceBundle:
        refs = source_view.evidence_refs
        return WorkbenchCommandEvidenceBundle(
            command_evidence_bundle_id="workbench_command_evidence_bundle:inspect_dashboard",
            evidence_refs=refs,
            claim_refs=source_view.evidence_report_refs,
            safety_refs=source_view.approval_report_refs,
            provider_refs=source_view.provider_report_refs,
            approval_refs=source_view.approval_candidate_refs,
            pig_guidance_refs=source_view.pig_guidance_refs,
            evidence_count=len(refs),
            evidence_status="complete" if refs else "missing",
        )


class WorkbenchCommandRiskSummaryService:
    def build_risk_summary(self, source_view: WorkbenchCommandSourceView) -> WorkbenchCommandRiskSummary:
        risk_categories = ["provider_boundary", "file_mutation", "local_runtime_execution", "unknown"]
        return WorkbenchCommandRiskSummary(
            command_risk_summary_id="workbench_command_risk_summary:inspect_dashboard",
            risk_level="medium" if source_view.source_status == "complete" else "unknown",
            risk_categories=risk_categories,
            risk_summary="Command candidates may describe risky future actions, so approval and do-nothing alternatives remain required.",
            mitigation_refs=source_view.approval_report_refs + source_view.pig_guidance_refs,
            approval_required=True,
            do_nothing_preferred=source_view.source_status != "complete",
            evidence_refs=source_view.evidence_refs,
        )


class WorkbenchCommandPIGGuidanceViewService:
    def build_pig_guidance_view(self, source_view: WorkbenchCommandSourceView) -> WorkbenchCommandPIGGuidanceView:
        return WorkbenchCommandPIGGuidanceView(
            command_pig_guidance_view_id="workbench_command_pig_guidance_view:v0.26.7",
            pig_guidance_refs=source_view.pig_guidance_refs,
            guidance_summary="PIG guidance may inform candidates but cannot mutate memory, persona, policy, or execution authority.",
            evidence_refs=source_view.pig_guidance_refs,
        )


class WorkbenchCommandSafetyFindingViewService:
    def build_safety_finding_view(self, source_view: WorkbenchCommandSourceView) -> WorkbenchCommandSafetyFindingView:
        requires_clarification = not source_view.user_intent_refs
        return WorkbenchCommandSafetyFindingView(
            command_safety_finding_view_id="workbench_command_safety_finding_view:v0.26.7",
            safety_finding_refs=source_view.approval_report_refs,
            safety_summary="Command surface is candidate-only and blocks execution, mutation, rerun, repair, and provider invocation.",
            blocked=source_view.source_status == "blocked",
            requires_approval=True,
            requires_clarification=requires_clarification,
            evidence_refs=source_view.evidence_refs,
        )


class WorkbenchCommandApprovalRequirementService:
    def build_approval_requirement(self, source_view: WorkbenchCommandSourceView) -> WorkbenchCommandApprovalRequirement:
        missing_reason = None if source_view.approval_candidate_refs else "approval_candidate_ref_missing"
        return WorkbenchCommandApprovalRequirement(
            command_approval_requirement_id="workbench_command_approval_requirement:inspect_dashboard",
            approval_required=True,
            approval_candidate_refs=source_view.approval_candidate_refs,
            approval_scope_refs=[_ref("workbench_approval_scope", "workbench_approval_scope:v0.26.5:existing", "v0.26.5")]
            if source_view.approval_report_refs
            else [],
            approval_expiry_refs=[_ref("workbench_approval_expiry", "workbench_approval_expiry:v0.26.5:existing", "v0.26.5")]
            if source_view.approval_report_refs
            else [],
            missing_approval_reason=missing_reason,
            evidence_refs=source_view.approval_report_refs,
        )


class WorkbenchCommandBoundaryTraceService:
    def build_boundary_trace(
        self, command_candidate_id: str, source_view: WorkbenchCommandSourceView
    ) -> WorkbenchCommandBoundaryTrace:
        return WorkbenchCommandBoundaryTrace(
            command_boundary_trace_id="workbench_command_boundary_trace:inspect_dashboard",
            command_candidate_id=command_candidate_id,
            required_boundaries=[
                "v0.25.7_ask_surface",
                "v0.25.5_provider_invocation_orchestrator",
                "v0.24.7_gated_local_runtime",
                "v0.26_workbench_view_only",
                "v0.26.8_snapshot_export_future",
            ],
            allowed_boundary_refs=[
                _ref("workbench_view_only_boundary", "v0.26_workbench_view_only"),
                _ref("snapshot_export_future_boundary", "v0.26.8_snapshot_export_future", "v0.26.8"),
            ],
            forbidden_boundary_refs=[_ref("forbidden_effect", item) for item in WORKBENCH_COMMAND_SURFACE_FORBIDDEN_EFFECT_TYPES],
            boundary_summary="Execution-capable boundaries are referenced only; no dispatch is performed in v0.26.7.",
            evidence_refs=source_view.evidence_refs,
        )


class WorkbenchCommandCandidateService:
    def build_command_candidates(
        self,
        *,
        source_view: WorkbenchCommandSourceView,
        skill_candidates: list[WorkbenchSkillCandidate],
        action_candidates: list[WorkbenchActionCandidate],
        route_candidates: list[WorkbenchRouteCandidate],
        provider_candidate_refs: list[WorkbenchProviderCandidateRef],
        file_edit_candidates: list[WorkbenchFileEditCandidate],
        ask_pipeline_candidates: list[WorkbenchAskPipelineCandidate],
        snapshot_request_candidates: list[WorkbenchSnapshotRequestCandidate],
    ) -> list[WorkbenchCommandCandidate]:
        candidate_id = "workbench_command_candidate:inspect_dashboard"
        rationale = WorkbenchCommandCandidateRationaleService().build_rationale(source_view)
        evidence_bundle = WorkbenchCommandEvidenceBundleService().build_evidence_bundle(source_view)
        risk_summary = WorkbenchCommandRiskSummaryService().build_risk_summary(source_view)
        boundary_trace = WorkbenchCommandBoundaryTraceService().build_boundary_trace(candidate_id, source_view)
        pig_view = WorkbenchCommandPIGGuidanceViewService().build_pig_guidance_view(source_view)
        safety_view = WorkbenchCommandSafetyFindingViewService().build_safety_finding_view(source_view)
        approval_requirement = WorkbenchCommandApprovalRequirementService().build_approval_requirement(source_view)
        status = "ready_for_review" if evidence_bundle.evidence_refs and boundary_trace else "incomplete"
        return [
            WorkbenchCommandCandidate(
                command_candidate_id=candidate_id,
                command_type="inspect_dashboard",
                title="Inspect Workbench Run and Approval Context",
                summary="Candidate-only inspection of v0.26.6 dashboard and v0.26.5 approval refs.",
                user_intent_refs=source_view.user_intent_refs,
                subject_refs=source_view.dashboard_report_refs + source_view.approval_report_refs,
                skill_candidate_refs=[_model_ref("workbench_skill_candidate", item, "skill_candidate_id") for item in skill_candidates],
                action_candidate_refs=[_model_ref("workbench_action_candidate", item, "action_candidate_id") for item in action_candidates],
                route_candidate_refs=[_model_ref("workbench_route_candidate", item, "route_candidate_id") for item in route_candidates],
                provider_candidate_refs=[
                    _model_ref("workbench_provider_candidate_ref", item, "provider_candidate_ref_id")
                    for item in provider_candidate_refs
                ],
                file_edit_candidate_refs=[
                    _model_ref("workbench_file_edit_candidate", item, "file_edit_candidate_id")
                    for item in file_edit_candidates
                ],
                ask_pipeline_candidate_ref=(
                    _model_ref("workbench_ask_pipeline_candidate", ask_pipeline_candidates[0], "ask_pipeline_candidate_id")
                    if ask_pipeline_candidates
                    else None
                ),
                snapshot_request_candidate_ref=(
                    _model_ref(
                        "workbench_snapshot_request_candidate",
                        snapshot_request_candidates[0],
                        "snapshot_request_candidate_id",
                    )
                    if snapshot_request_candidates
                    else None
                ),
                rationale=rationale,
                evidence_bundle=evidence_bundle,
                risk_summary=risk_summary,
                pig_guidance_view=pig_view,
                safety_finding_view=safety_view,
                approval_requirement=approval_requirement,
                boundary_trace=boundary_trace,
                candidate_status=status,
                evidence_refs=evidence_bundle.evidence_refs,
            )
        ]


class WorkbenchCommandDecisionService:
    def build_decision(
        self,
        command_candidate_id: str,
        *,
        requested_decision: str | None = None,
        evidence_refs: list[dict[str, Any]] | None = None,
    ) -> WorkbenchCommandDecision:
        decision_type = requested_decision or "choose_do_nothing"
        if decision_type not in ALLOWED_COMMAND_DECISIONS:
            decision_type = "unknown"
        return WorkbenchCommandDecision(
            command_decision_id=f"workbench_command_decision:{_safe_id(command_candidate_id)}:{decision_type}",
            command_candidate_id=command_candidate_id,
            decision_type=decision_type,
            decision_reason="Record the command-surface decision without creating execution.",
            creates_execution=False,
            evidence_refs=evidence_refs or [],
        )


class WorkbenchCommandDecisionRecordService:
    def build_decision_record(self, decision: WorkbenchCommandDecision) -> WorkbenchCommandDecisionRecord:
        return WorkbenchCommandDecisionRecord(
            command_decision_record_id=f"workbench_command_decision_record:{_safe_id(decision.command_decision_id)}",
            decision=decision,
            evidence_refs=decision.evidence_refs,
        )


class WorkbenchCommandExecutionEnvelopeService:
    def build_non_executing_envelope(
        self, candidate: WorkbenchCommandCandidate, decision: WorkbenchCommandDecision | None = None
    ) -> WorkbenchCommandExecutionEnvelope:
        status = "inspection_only" if candidate.command_type.startswith("inspect") else "candidate_only"
        if decision and decision.decision_type == "approve_candidate":
            status = "approved_ref_only"
        if decision and decision.decision_type == "reject_candidate":
            status = "rejected"
        if decision and decision.decision_type == "defer_candidate":
            status = "deferred"
        return WorkbenchCommandExecutionEnvelope(
            command_execution_envelope_id=f"workbench_command_execution_envelope:{_safe_id(candidate.command_candidate_id)}",
            command_candidate_id=candidate.command_candidate_id,
            boundary_trace_id=candidate.boundary_trace.command_boundary_trace_id,
            envelope_status=status,
            dispatch_target=None,
            dispatch_deferred=True,
            dispatch_performed_now=False,
            evidence_refs=candidate.evidence_refs,
        )


class WorkbenchCommandResultService:
    def build_candidate_result(
        self, candidate: WorkbenchCommandCandidate, decision_record: WorkbenchCommandDecisionRecord | None = None
    ) -> WorkbenchCommandResult:
        result_type = "decision_recorded" if decision_record else "candidate_created"
        result_refs = [_model_ref("workbench_command_candidate", candidate, "command_candidate_id")]
        if decision_record:
            result_refs.append(_model_ref("workbench_command_decision_record", decision_record, "command_decision_record_id"))
        return WorkbenchCommandResult(
            command_result_id=f"workbench_command_result:{_safe_id(candidate.command_candidate_id)}",
            command_candidate_id=candidate.command_candidate_id,
            result_type=result_type,
            result_summary="Workbench command surface materialized records only; no external action result exists.",
            result_refs=result_refs,
            evidence_refs=candidate.evidence_refs,
        )


class WorkbenchCommandHistoryService:
    def build_history_entries(
        self,
        candidates: list[WorkbenchCommandCandidate],
        decision_records: list[WorkbenchCommandDecisionRecord],
        results: list[WorkbenchCommandResult],
    ) -> list[WorkbenchCommandHistoryEntry]:
        entries: list[WorkbenchCommandHistoryEntry] = []
        decision_ref = _model_ref("workbench_command_decision_record", decision_records[0], "command_decision_record_id") if decision_records else None
        result_ref = _model_ref("workbench_command_result", results[0], "command_result_id") if results else None
        for candidate in candidates:
            entries.append(
                WorkbenchCommandHistoryEntry(
                    command_history_entry_id=f"workbench_command_history_entry:{_safe_id(candidate.command_candidate_id)}",
                    command_candidate_ref=_model_ref("workbench_command_candidate", candidate, "command_candidate_id"),
                    decision_record_ref=decision_ref,
                    result_ref=result_ref,
                    timestamp=utc_now_iso(),
                    evidence_refs=candidate.evidence_refs,
                )
            )
        return entries


class WorkbenchCommandAuditTrailService:
    def build_audit_trail(
        self,
        candidates: list[WorkbenchCommandCandidate],
        do_nothing_candidates: list[WorkbenchDoNothingCandidate],
        decision_records: list[WorkbenchCommandDecisionRecord],
        results: list[WorkbenchCommandResult],
    ) -> WorkbenchCommandAuditTrail:
        boundary_refs = [
            _model_ref("workbench_command_boundary_trace", item.boundary_trace, "command_boundary_trace_id")
            for item in candidates
        ]
        event_count = len(candidates) + len(do_nothing_candidates) + len(decision_records) + len(results) + len(boundary_refs)
        return WorkbenchCommandAuditTrail(
            command_audit_trail_id="workbench_command_audit_trail:v0.26.7",
            command_candidate_refs=[_model_ref("workbench_command_candidate", item, "command_candidate_id") for item in candidates],
            command_decision_record_refs=[
                _model_ref("workbench_command_decision_record", item, "command_decision_record_id")
                for item in decision_records
            ],
            command_result_refs=[_model_ref("workbench_command_result", item, "command_result_id") for item in results],
            do_nothing_candidate_refs=[
                _model_ref("workbench_do_nothing_candidate", item, "do_nothing_candidate_id")
                for item in do_nothing_candidates
            ],
            boundary_trace_refs=boundary_refs,
            audit_event_count=event_count,
            audit_status="ready" if event_count else "partial",
            evidence_refs=[ref for item in candidates for ref in item.evidence_refs],
        )


class WorkbenchCommandSurfaceViewService:
    def build_surface_view(
        self,
        *,
        source_view: WorkbenchCommandSourceView,
        command_candidates: list[WorkbenchCommandCandidate],
        do_nothing_candidates: list[WorkbenchDoNothingCandidate],
        skill_candidates: list[WorkbenchSkillCandidate],
        action_candidates: list[WorkbenchActionCandidate],
        route_candidates: list[WorkbenchRouteCandidate],
        provider_candidate_refs: list[WorkbenchProviderCandidateRef],
        command_decisions: list[WorkbenchCommandDecision],
        command_results: list[WorkbenchCommandResult],
        command_history: list[WorkbenchCommandHistoryEntry],
        audit_trail: WorkbenchCommandAuditTrail,
    ) -> WorkbenchCommandSurfaceView:
        status = "ready" if command_candidates and do_nothing_candidates else "partial"
        if source_view.source_status == "missing":
            status = "failed"
        return WorkbenchCommandSurfaceView(
            command_surface_view_id="workbench_command_surface_view:v0.26.7",
            panel_id="workbench_panel:command_surface",
            source_view=source_view,
            command_candidates=command_candidates,
            do_nothing_candidates=do_nothing_candidates,
            skill_candidates=skill_candidates,
            action_candidates=action_candidates,
            route_candidates=route_candidates,
            provider_candidate_refs=provider_candidate_refs,
            command_decisions=command_decisions,
            command_results=command_results,
            command_history=command_history,
            audit_trail=audit_trail,
            view_status=status,
            evidence_refs=source_view.evidence_refs,
        )


class WorkbenchCommandSurfaceFindingService:
    BLOCKED_FINDINGS = {
        "direct_command_execution_attempted",
        "provider_invocation_attempted",
        "local_command_execution_attempted",
        "file_mutation_attempted",
        "patch_application_attempted",
        "ask_execution_attempted",
        "final_response_emission_attempted",
        "route_rerun_attempted",
        "stage_rerun_attempted",
        "automatic_retry_attempted",
        "automatic_repair_attempted",
        "autonomous_loop_attempted",
        "approval_execution_attempted",
        "approval_token_execution_attempted",
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

    CREATED_FINDINGS = [
        "command_surface_view_created",
        "command_candidate_created",
        "do_nothing_candidate_created",
        "skill_candidate_created",
        "action_candidate_created",
        "route_candidate_created",
        "provider_candidate_ref_created",
        "file_edit_candidate_created",
        "ask_pipeline_candidate_created",
        "snapshot_request_candidate_created",
        "command_rationale_created",
        "command_evidence_bundle_created",
        "command_risk_summary_created",
        "command_pig_guidance_attached",
        "command_safety_finding_attached",
        "command_approval_requirement_created",
        "command_boundary_trace_created",
        "command_decision_recorded",
        "command_execution_envelope_created",
        "command_result_created",
        "command_history_recorded",
        "command_audit_trail_created",
    ]

    def build_findings(
        self,
        *,
        source_service: WorkbenchCommandSurfacePrerequisiteSourceService,
        source_view: WorkbenchCommandSourceView,
        command_candidates: list[WorkbenchCommandCandidate],
        do_nothing_candidates: list[WorkbenchDoNothingCandidate],
        strictness: str = "standard",
        extra_findings: list[str] | None = None,
    ) -> list[WorkbenchCommandSurfaceFinding]:
        findings: list[WorkbenchCommandSurfaceFinding] = []
        if not source_service.view_state_available:
            findings.append(self._finding("warning", "missing_workbench_view_state", "Workbench view state is missing."))
        if not source_service.command_surface_panel_available:
            severity = "error" if strictness == "strict" else "warning"
            findings.append(self._finding(severity, "missing_command_surface_panel", "Command surface panel model is missing."))
        if not source_view.user_intent_refs:
            findings.append(self._finding("warning", "missing_user_intent_ref", "User intent ref is missing."))
        if not any(candidate.evidence_bundle.evidence_refs for candidate in command_candidates):
            findings.append(self._finding("error", "missing_evidence_refs", "Command candidate evidence refs are missing."))
        if not all(candidate.risk_summary for candidate in command_candidates):
            findings.append(self._finding("error", "missing_risk_summary", "Command candidate risk summary is missing."))
        if not all(candidate.boundary_trace for candidate in command_candidates):
            findings.append(self._finding("error", "missing_boundary_trace", "Command candidate boundary trace is missing."))
        if not do_nothing_candidates:
            findings.append(self._finding("error", "missing_do_nothing_candidate", "Do-nothing candidate is missing."))
        for finding_type in self.CREATED_FINDINGS:
            findings.append(self._finding("info", finding_type, f"{finding_type}"))
        for finding_type in extra_findings or []:
            severity = "critical" if finding_type in self.BLOCKED_FINDINGS else "warning"
            findings.append(self._finding(severity, finding_type, f"{finding_type}"))
        if not findings:
            findings.append(self._finding("info", "ok", "Workbench command surface report is complete."))
        return findings

    def _finding(self, severity: str, finding_type: str, message: str) -> WorkbenchCommandSurfaceFinding:
        return WorkbenchCommandSurfaceFinding(
            finding_id=f"workbench_command_surface_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            withdrawal_condition="Withdraw if command surface policy or source evidence changes.",
        )


class WorkbenchCommandSurfaceReportService:
    def build_all_parts(
        self,
        *,
        report_id: str | None = None,
        candidate_id: str | None = None,
        requested_decision: str | None = None,
        strictness: str = "standard",
        extra_findings: list[str] | None = None,
        view_state_available: bool = True,
        command_surface_panel_available: bool = True,
        dashboard_report_available: bool = True,
        approval_console_available: bool = True,
        evidence_inspector_available: bool = True,
        provider_browser_available: bool = True,
        trace_explorer_available: bool = True,
        skill_registry_available: bool = True,
        provider_registry_available: bool = True,
        pig_guidance_available: bool = True,
        user_intent_available: bool = True,
    ) -> dict[str, Any]:
        source_service = WorkbenchCommandSurfacePrerequisiteSourceService(
            view_state_available=view_state_available,
            command_surface_panel_available=command_surface_panel_available,
            dashboard_report_available=dashboard_report_available,
            approval_console_available=approval_console_available,
            evidence_inspector_available=evidence_inspector_available,
            provider_browser_available=provider_browser_available,
            trace_explorer_available=trace_explorer_available,
            skill_registry_available=skill_registry_available,
            provider_registry_available=provider_registry_available,
            pig_guidance_available=pig_guidance_available,
            user_intent_available=user_intent_available,
        )
        policy = WorkbenchCommandSurfacePolicyService().build_policy()
        request = WorkbenchCommandSurfaceRequestService().build_request(
            source_service=source_service,
            report_id=report_id,
            requested_command_type=None,
            strictness=strictness,
        )
        source_view = WorkbenchCommandSourceViewService().build_source_view(source_service, request)
        command_type_policy = WorkbenchCommandTypePolicyService().build_policy()
        skill_candidates = WorkbenchSkillCandidateService().build_skill_candidates(source_view)
        action_candidates = WorkbenchActionCandidateService().build_action_candidates(source_view)
        route_candidates = WorkbenchRouteCandidateService().build_route_candidates(source_view)
        provider_candidate_refs = WorkbenchProviderCandidateRefService().build_provider_candidate_refs(source_view)
        file_edit_candidates = WorkbenchFileEditCandidateService().build_file_edit_candidates(source_view)
        ask_pipeline_candidates = WorkbenchAskPipelineCandidateService().build_ask_pipeline_candidates(source_view)
        snapshot_request_candidates = WorkbenchSnapshotRequestCandidateService().build_snapshot_request_candidates(source_view)
        command_candidates = WorkbenchCommandCandidateService().build_command_candidates(
            source_view=source_view,
            skill_candidates=skill_candidates,
            action_candidates=action_candidates,
            route_candidates=route_candidates,
            provider_candidate_refs=provider_candidate_refs,
            file_edit_candidates=file_edit_candidates,
            ask_pipeline_candidates=ask_pipeline_candidates,
            snapshot_request_candidates=snapshot_request_candidates,
        )
        selected_candidate = command_candidates[0]
        if candidate_id:
            selected_candidate.command_candidate_id = candidate_id
            selected_candidate.boundary_trace.command_candidate_id = candidate_id
        command_refs = [_model_ref("workbench_command_candidate", item, "command_candidate_id") for item in command_candidates]
        do_nothing_candidates = WorkbenchDoNothingCandidateService().build_do_nothing_candidates(command_refs)
        command_requests = [
            WorkbenchCommandRequest(
                command_request_id="workbench_command_request:inspect_dashboard",
                command_type=selected_candidate.command_type,
                user_intent_ref=request.user_intent_ref,
                subject_refs=selected_candidate.subject_refs,
                evidence_refs=source_view.evidence_refs,
            )
        ]
        decision = WorkbenchCommandDecisionService().build_decision(
            selected_candidate.command_candidate_id,
            requested_decision=requested_decision,
            evidence_refs=selected_candidate.evidence_refs,
        )
        decision_record = WorkbenchCommandDecisionRecordService().build_decision_record(decision)
        execution_envelope = WorkbenchCommandExecutionEnvelopeService().build_non_executing_envelope(selected_candidate, decision)
        result = WorkbenchCommandResultService().build_candidate_result(selected_candidate, decision_record)
        command_history = WorkbenchCommandHistoryService().build_history_entries(command_candidates, [decision_record], [result])
        audit_trail = WorkbenchCommandAuditTrailService().build_audit_trail(
            command_candidates,
            do_nothing_candidates,
            [decision_record],
            [result],
        )
        surface_view = WorkbenchCommandSurfaceViewService().build_surface_view(
            source_view=source_view,
            command_candidates=command_candidates,
            do_nothing_candidates=do_nothing_candidates,
            skill_candidates=skill_candidates,
            action_candidates=action_candidates,
            route_candidates=route_candidates,
            provider_candidate_refs=provider_candidate_refs,
            command_decisions=[decision],
            command_results=[result],
            command_history=command_history,
            audit_trail=audit_trail,
        )
        findings = WorkbenchCommandSurfaceFindingService().build_findings(
            source_service=source_service,
            source_view=source_view,
            command_candidates=command_candidates,
            do_nothing_candidates=do_nothing_candidates,
            strictness=strictness,
            extra_findings=extra_findings,
        )
        report_status = self._report_status(findings, strictness)
        if strictness == "strict" and source_view.source_status == "missing":
            report_status = "failed"
        ready_for_v0_26_8 = report_status in {"passed", "warning"} and bool(command_candidates and do_nothing_candidates)
        report = WorkbenchCommandSurfaceReport(
            report_id=report_id or "workbench_command_surface_report:v0.26.7",
            created_at=utc_now_iso(),
            command_surface_policy=policy,
            request=request,
            source_view=source_view,
            command_surface_view=surface_view,
            command_type_policy=command_type_policy,
            audit_trail=audit_trail,
            findings=findings,
            report_status=report_status,
            ready_for_v0_26_8=ready_for_v0_26_8,
            command_surface_view_created=True,
            command_candidates_created=bool(command_candidates),
            do_nothing_candidates_created=bool(do_nothing_candidates),
            skill_candidates_created=bool(skill_candidates),
            action_candidates_created=bool(action_candidates),
            route_candidates_created=bool(route_candidates),
            provider_candidate_refs_created=bool(provider_candidate_refs),
            file_edit_candidates_created=bool(file_edit_candidates),
            ask_pipeline_candidates_created=bool(ask_pipeline_candidates),
            snapshot_request_candidates_created=bool(snapshot_request_candidates),
            command_decisions_recorded=True,
            command_history_created=bool(command_history),
            audit_trail_created=True,
            limitations=[
                "v0.26.7 creates command candidates and decision records only.",
                "Snapshot and OCEL export remain deferred to v0.26.8.",
                "Execution-capable boundaries remain references only.",
            ],
            withdrawal_conditions=[
                "Withdraw readiness if command dispatch, provider invocation, local execution, file mutation, ask/repl execution, or memory promotion is added.",
                "Withdraw readiness if raw transcript, raw provider output, raw secret, or credential values are persisted or printed.",
            ],
        )
        return {
            "policy": policy,
            "request": request,
            "source_view": source_view,
            "command_surface_view": surface_view,
            "command_type_policy": command_type_policy,
            "command_requests": command_requests,
            "command_candidates": command_candidates,
            "do_nothing_candidates": do_nothing_candidates,
            "skill_candidates": skill_candidates,
            "action_candidates": action_candidates,
            "route_candidates": route_candidates,
            "provider_candidate_refs": provider_candidate_refs,
            "file_edit_candidates": file_edit_candidates,
            "ask_pipeline_candidates": ask_pipeline_candidates,
            "snapshot_request_candidates": snapshot_request_candidates,
            "rationale": selected_candidate.rationale,
            "evidence_bundle": selected_candidate.evidence_bundle,
            "risk_summary": selected_candidate.risk_summary,
            "pig_guidance_view": selected_candidate.pig_guidance_view,
            "safety_finding_view": selected_candidate.safety_finding_view,
            "approval_requirement": selected_candidate.approval_requirement,
            "boundary_trace": selected_candidate.boundary_trace,
            "command_decisions": [decision],
            "command_decision_records": [decision_record],
            "execution_envelope": execution_envelope,
            "command_results": [result],
            "command_history": command_history,
            "audit_trail": audit_trail,
            "findings": findings,
            "report": report,
        }

    def _report_status(self, findings: list[WorkbenchCommandSurfaceFinding], strictness: str) -> str:
        if any(finding.finding_type in WorkbenchCommandSurfaceFindingService.BLOCKED_FINDINGS for finding in findings):
            return "blocked"
        if any(finding.severity == "critical" for finding in findings):
            return "blocked"
        if strictness == "strict" and any(finding.severity == "error" for finding in findings):
            return "failed"
        if any(finding.severity in {"warning", "error"} for finding in findings):
            return "warning"
        return "passed"

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": WORKBENCH_COMMAND_SURFACE_VERSION,
            "layer": WORKBENCH_COMMAND_SURFACE_LAYER,
            "subject": "workbench_command_surface",
            "principles": [
                "Workbench command is not direct execution",
                "Command candidate is not command execution",
                "Skill candidate is not skill execution",
                "Action candidate is not action execution",
                "Route candidate is not route execution",
                "Provider candidate is not provider invocation",
                "File edit candidate is not file mutation",
                "Ask pipeline candidate is not ask execution",
                "Snapshot request candidate is not snapshot export",
                "Do-nothing candidate is a first-class safe alternative",
                "PIG guidance is not memory, policy mutation, or execution",
            ],
            "safety_boundary": {
                "command_surface_view_created": "conditional",
                "command_candidates_created": "conditional",
                "do_nothing_candidates_created": "conditional",
                "skill_candidates_created": "conditional",
                "action_candidates_created": "conditional",
                "direct_command_executed": False,
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
                "approval_executed": False,
                "approval_token_executed": False,
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
                "v0.26.8 snapshot / OCEL export",
                "v0.26.9 workbench consolidation",
                "v0.27 memory candidate and continuity",
            ],
            "next_step": WORKBENCH_COMMAND_SURFACE_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "workbench_command_surface_created",
            "version": WORKBENCH_COMMAND_SURFACE_VERSION,
            "source_read_models": [
                "WorkbenchRunDashboardViewState",
                "WorkbenchApprovalConsoleViewState",
                "WorkbenchEvidenceInspectorViewState",
                "WorkbenchProviderBrowserViewState",
                "WorkbenchTraceExplorerViewState",
                "SkillRegistryState",
                "ProviderRegistryState",
                "PigGuidanceState",
            ],
            "target_read_models": [
                "WorkbenchCommandSurfaceViewState",
                "WorkbenchCommandCandidateState",
                "WorkbenchSkillCandidateState",
                "WorkbenchActionCandidateState",
                "WorkbenchCommandBoundaryTraceState",
                "WorkbenchCommandDecisionRecordState",
                "WorkbenchCommandAuditTrailState",
                "V026ReadinessState",
            ],
            "effect_types": WORKBENCH_COMMAND_SURFACE_EFFECT_TYPES,
        }


def _bool(value: bool) -> str:
    return "true" if value else "false"


def render_workbench_command_surface_cli(parts: dict[str, Any], section: str = "surface") -> str:
    report: WorkbenchCommandSurfaceReport = parts["report"]
    common = [
        f"version={report.version}",
        f"layer={WORKBENCH_COMMAND_SURFACE_LAYER}",
        f"command_surface_view_created={_bool(report.command_surface_view_created)}",
        f"command_candidates_created={_bool(report.command_candidates_created)}",
        f"do_nothing_candidates_created={_bool(report.do_nothing_candidates_created)}",
        f"skill_candidates_created={_bool(report.skill_candidates_created)}",
        f"action_candidates_created={_bool(report.action_candidates_created)}",
        f"route_candidates_created={_bool(report.route_candidates_created)}",
        f"provider_candidate_refs_created={_bool(report.provider_candidate_refs_created)}",
        f"file_edit_candidates_created={_bool(report.file_edit_candidates_created)}",
        f"ask_pipeline_candidates_created={_bool(report.ask_pipeline_candidates_created)}",
        f"snapshot_request_candidates_created={_bool(report.snapshot_request_candidates_created)}",
        f"command_decisions_recorded={_bool(report.command_decisions_recorded)}",
        f"command_history_created={_bool(report.command_history_created)}",
        f"audit_trail_created={_bool(report.audit_trail_created)}",
        f"ready_for_v0_26_8={_bool(report.ready_for_v0_26_8)}",
        f"ready_for_v0_27={_bool(report.ready_for_v0_27)}",
        f"direct_command_executed={_bool(report.direct_command_executed)}",
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
        f"approval_executed={_bool(report.approval_executed)}",
        f"approval_token_executed={_bool(report.approval_token_executed)}",
        f"memory_promoted={_bool(report.memory_promoted)}",
        f"persistent_memory_written={_bool(report.persistent_memory_written)}",
        f"persona_mutated={_bool(report.persona_mutated)}",
        f"external_provider_adapter_implemented={_bool(report.external_provider_adapter_implemented)}",
        f"vendor_adapter_implemented={_bool(report.vendor_adapter_implemented)}",
        f"pig_memory_promoted={_bool(report.pig_memory_promoted)}",
        f"pig_policy_mutated={_bool(report.pig_policy_mutated)}",
        f"pig_executed={_bool(report.pig_executed)}",
        f"schumpeter_split_introduced={_bool(report.schumpeter_split_introduced)}",
        f"credential_exposed={_bool(report.credential_exposed)}",
        f"raw_secret_output={_bool(report.raw_secret_output)}",
        f"raw_provider_output_inline={_bool(report.raw_provider_output_inline)}",
        f"raw_transcript_persisted={_bool(report.raw_transcript_persisted)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    lines = [f"Workbench Command Surface {section}", *common]
    if section == "surface":
        lines.extend([
            f"view_status={parts['command_surface_view'].view_status}",
            f"command_candidate_count={len(parts['command_candidates'])}",
        ])
    elif section == "candidates":
        lines.append(f"command_candidate_count={len(parts['command_candidates'])}")
    elif section == "do-nothing":
        lines.append(f"do_nothing_candidate_count={len(parts['do_nothing_candidates'])}")
    elif section == "skills":
        lines.append(f"skill_candidate_count={len(parts['skill_candidates'])}")
    elif section == "actions":
        lines.append(f"action_candidate_count={len(parts['action_candidates'])}")
    elif section == "routes":
        lines.append(f"route_candidate_count={len(parts['route_candidates'])}")
    elif section == "providers":
        lines.append(f"provider_candidate_ref_count={len(parts['provider_candidate_refs'])}")
    elif section == "file-edit-candidates":
        lines.append(f"file_edit_candidate_count={len(parts['file_edit_candidates'])}")
    elif section == "ask-candidates":
        lines.append(f"ask_pipeline_candidate_count={len(parts['ask_pipeline_candidates'])}")
    elif section == "snapshot-candidates":
        lines.append(f"snapshot_request_candidate_count={len(parts['snapshot_request_candidates'])}")
    elif section == "rationale":
        lines.append(f"rationale_id={parts['rationale'].rationale_id}")
    elif section == "risk":
        risk = parts["risk_summary"]
        lines.extend([
            f"risk_level={risk.risk_level}",
            f"approval_required={_bool(risk.approval_required)}",
            f"do_nothing_preferred={_bool(risk.do_nothing_preferred)}",
        ])
    elif section == "pig-guidance":
        pig = parts["pig_guidance_view"]
        lines.extend([
            f"pig_guidance_is_memory={_bool(pig.pig_guidance_is_memory)}",
            f"pig_guidance_mutates_policy={_bool(pig.pig_guidance_mutates_policy)}",
            f"pig_guidance_executes={_bool(pig.pig_guidance_executes)}",
        ])
    elif section == "safety":
        safety = parts["safety_finding_view"]
        lines.extend([
            f"blocked={_bool(safety.blocked)}",
            f"requires_approval={_bool(safety.requires_approval)}",
            f"safety_policy_mutated_now={_bool(safety.safety_policy_mutated_now)}",
        ])
    elif section == "approval-requirements":
        approval = parts["approval_requirement"]
        lines.extend([
            f"approval_required={_bool(approval.approval_required)}",
            f"approval_execution_performed={_bool(approval.approval_execution_performed)}",
        ])
    elif section == "boundary-trace":
        boundary = parts["boundary_trace"]
        lines.extend([
            f"boundary_bypassed={_bool(boundary.boundary_bypassed)}",
            f"execution_performed_now={_bool(boundary.execution_performed_now)}",
        ])
    elif section == "decide":
        decision = parts["command_decisions"][0]
        record = parts["command_decision_records"][0]
        lines.extend([
            f"decision_type={decision.decision_type}",
            f"decision_record_created={_bool(True)}",
            f"creates_execution={_bool(decision.creates_execution)}",
            f"execution_triggered={_bool(record.execution_triggered)}",
        ])
    elif section == "history":
        lines.append(f"command_history_count={len(parts['command_history'])}")
    elif section == "audit":
        audit = parts["audit_trail"]
        lines.extend([
            f"audit_event_count={audit.audit_event_count}",
            f"raw_secret_included={_bool(audit.raw_secret_included)}",
            f"raw_provider_output_included={_bool(audit.raw_provider_output_included)}",
            f"raw_transcript_included={_bool(audit.raw_transcript_included)}",
        ])
    elif section == "report":
        lines.extend([
            f"report_id={report.report_id}",
            f"report_status={report.report_status}",
            f"finding_count={len(report.findings)}",
        ])
    return "\n".join(lines)
