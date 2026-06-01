from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from chanta_core.agent_surface.safety_gate import AgentSafetyGateReportService
from chanta_core.agent_surface.tool_routing import AgentToolRoutingReportService
from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace_agent_workbench.evidence_inspector import WorkbenchEvidenceInspectorReportService
from chanta_core.workspace_agent_workbench.provider_browser import WorkbenchProviderBrowserReportService
from chanta_core.workspace_agent_workbench.trace_explorer import WorkbenchTraceExplorerReportService
from chanta_core.workspace_agent_workbench.view_state import WorkbenchViewStateReportService


WORKBENCH_SAFETY_APPROVAL_VERSION = "v0.26.5"
WORKBENCH_SAFETY_APPROVAL_VERSION_NAME = "Safety Gate / Approval Console"
WORKBENCH_SAFETY_APPROVAL_KOREAN_NAME = "Safety Gate·Approval Console"
WORKBENCH_SAFETY_APPROVAL_LAYER = "workspace_agent_workbench"
WORKBENCH_SAFETY_APPROVAL_TRACK = "Workspace Agent Workbench"
WORKBENCH_SAFETY_APPROVAL_NEXT_STEP = "v0.26.6 Run Dashboard / Session Monitor"

WORKBENCH_SAFETY_APPROVAL_IMPLEMENTED_SKILL_IDS = [
    "skill:workbench_safety_gate_view",
    "skill:workbench_approval_console_view",
]
WORKBENCH_SAFETY_APPROVAL_FUTURE_SKILL_IDS = [
    "skill:workbench_run_dashboard_view",
    "skill:workbench_session_monitor_view",
    "skill:workbench_command_surface_use",
    "skill:workbench_snapshot_create",
    "skill:workbench_ocel_export_create",
    "skill:workbench_consolidation_view",
]

WORKBENCH_SAFETY_APPROVAL_OBJECT_TYPES = [
    "workbench_safety_approval_policy",
    "workbench_safety_approval_request",
    "workbench_safety_gate_source_view",
    "workbench_safety_gate_view",
    "workbench_safety_rationale_console_view",
    "workbench_approval_console_view",
    "workbench_approval_requirement",
    "workbench_approval_candidate",
    "workbench_approval_candidate_evidence_bundle",
    "workbench_action_risk_summary",
    "workbench_approval_scope",
    "workbench_approval_expiry",
    "workbench_approval_token",
    "workbench_approval_decision",
    "workbench_approval_decision_record",
    "workbench_rejection_decision_record",
    "workbench_deferral_decision_record",
    "workbench_manual_review_record",
    "workbench_pig_guidance_attachment",
    "workbench_approval_human_intervention_point",
    "workbench_approval_audit_trail",
    "workbench_approval_console_finding",
    "workbench_approval_console_report",
    "workbench_evidence_inspector_report",
    "agent_safety_gate_report",
    "agent_gate_outcome_envelope",
    "pig_report",
    "execution_envelope",
    "ocpx_projection",
]

WORKBENCH_SAFETY_APPROVAL_EVENT_TYPES = [
    "workbench_safety_approval_requested",
    "workbench_safety_approval_policy_created",
    "workbench_safety_gate_source_view_created",
    "workbench_safety_gate_view_created",
    "workbench_safety_rationale_console_created",
    "workbench_approval_console_view_created",
    "workbench_approval_requirement_created",
    "workbench_approval_candidate_created",
    "workbench_approval_candidate_evidence_bundle_created",
    "workbench_action_risk_summary_created",
    "workbench_approval_scope_created",
    "workbench_approval_expiry_created",
    "workbench_approval_token_created",
    "workbench_approval_decision_recorded",
    "workbench_rejection_decision_recorded",
    "workbench_deferral_decision_recorded",
    "workbench_manual_review_recorded",
    "workbench_pig_guidance_attached",
    "workbench_human_intervention_point_identified",
    "workbench_approval_audit_trail_created",
    "workbench_approval_console_report_created",
    "workbench_approval_console_warning_created",
    "workbench_approval_console_blocked",
]

WORKBENCH_SAFETY_APPROVAL_RELATION_TYPES = [
    "uses_workbench_view_state",
    "uses_safety_gate_panel",
    "uses_approval_console_panel",
    "uses_safety_gate_report",
    "uses_gate_outcome_envelope",
    "uses_evidence_inspector_report",
    "uses_provider_browser_report",
    "uses_pig_guidance_ref",
    "creates_safety_gate_view",
    "creates_safety_rationale_console",
    "creates_approval_requirement",
    "creates_approval_candidate",
    "creates_action_risk_summary",
    "creates_approval_scope",
    "creates_approval_expiry",
    "creates_non_executable_approval_token",
    "records_approval_decision",
    "records_rejection_decision",
    "records_deferral_decision",
    "records_manual_review",
    "attaches_pig_guidance_ref",
    "identifies_human_intervention_point",
    "creates_approval_audit_trail",
    "prepares_run_dashboard",
    "defers_run_dashboard_to_v0_26_6",
    "defers_command_surface_to_v0_26_7",
    "defers_snapshot_export_to_v0_26_8",
    "defers_memory_continuity_to_v0_27",
    "defers_external_provider_adapters_to_v0_29_plus",
    "defers_external_agent_dominion_to_v0_30_plus",
    "not_approval_executed",
    "not_command_executed",
    "not_provider_invoked",
    "not_pig_memory_promoted",
    "not_pig_policy_mutated",
    "not_pig_executed",
    "prevents_credential_exposure",
    "blocks_raw_provider_output_inline",
    "blocks_raw_secret_output",
    "recorded_in_envelope",
]

WORKBENCH_SAFETY_APPROVAL_EFFECT_TYPES = [
    "read_only_observation",
    "workbench_safety_gate_view_created",
    "workbench_safety_rationale_console_created",
    "workbench_approval_console_created",
    "workbench_approval_requirement_created",
    "workbench_approval_candidate_created",
    "workbench_approval_scope_created",
    "workbench_approval_expiry_created",
    "workbench_approval_token_created",
    "workbench_approval_decision_recorded",
    "workbench_rejection_decision_recorded",
    "workbench_deferral_decision_recorded",
    "workbench_manual_review_recorded",
    "workbench_pig_guidance_attached",
    "workbench_human_intervention_point_identified",
    "workbench_approval_audit_trail_created",
    "state_candidate_created",
]

WORKBENCH_SAFETY_APPROVAL_FORBIDDEN_EFFECT_TYPES = [
    "approval_executed",
    "approval_token_executed",
    "auto_approval_performed",
    "command_executed",
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
    "automatic_repair_performed",
    "direct_file_access_performed",
    "direct_subprocess_called",
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


class _Model:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _utc_now() -> str:
    return utc_now_iso()


def _model_id(prefix: str, seed: str | None = None) -> str:
    suffix = seed or "default"
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in suffix)
    return f"{prefix}_{WORKBENCH_SAFETY_APPROVAL_VERSION.replace('.', '_')}_{safe}"


def _ref(object_type: str, object_id: str | None, **extra: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {"object_type": object_type, "object_id": object_id or "unknown"}
    payload.update({key: value for key, value in extra.items() if value is not None})
    return payload


def _model_ref(object_type: str, model: Any, id_attr: str) -> dict[str, Any]:
    return _ref(object_type, getattr(model, id_attr, None), version=getattr(model, "version", None))


def _panel_by_type(view_state_parts: dict[str, Any] | None, panel_type: str) -> Any | None:
    if not view_state_parts:
        return None
    panels = view_state_parts.get("panels") or []
    for panel in panels:
        if getattr(panel, "panel_type", None) == panel_type:
            return panel
    return None


def _as_ref_list(values: list[Any], object_type: str, id_attr: str = "id") -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for index, value in enumerate(values):
        if isinstance(value, dict):
            refs.append(value)
            continue
        object_id = getattr(value, id_attr, None) or getattr(value, f"{id_attr}_id", None)
        refs.append(_ref(object_type, object_id or f"{object_type}_{index + 1}"))
    return refs


@dataclass(frozen=True)
class WorkbenchSafetyApprovalPolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_SAFETY_APPROVAL_VERSION
    layer: str = WORKBENCH_SAFETY_APPROVAL_LAYER
    safety_gate_view_enabled: bool = True
    approval_console_enabled: bool = True
    approval_candidate_enabled: bool = True
    approval_decision_record_enabled: bool = True
    rejection_decision_record_enabled: bool = True
    deferral_decision_record_enabled: bool = True
    manual_review_record_enabled: bool = True
    human_intervention_point_enabled: bool = True
    actual_ui_rendering_enabled: bool = False
    panel_rendering_enabled: bool = False
    approval_execution_enabled: bool = False
    approval_token_execution_enabled: bool = False
    auto_approval_enabled: bool = False
    command_execution_enabled: bool = False
    provider_invocation_enabled: bool = False
    route_rerun_enabled: bool = False
    stage_rerun_enabled: bool = False
    ask_execution_enabled: bool = False
    response_emission_enabled: bool = False
    local_runtime_execution_enabled: bool = False
    memory_promotion_enabled: bool = False
    persistent_memory_write_enabled: bool = False
    persona_mutation_enabled: bool = False
    external_adapter_enabled: bool = False
    approval_requires_user_intent_ref: bool = True
    approval_requires_policy_ref: bool = True
    approval_requires_evidence_refs: bool = True
    approval_requires_risk_summary: bool = True
    approval_requires_scope: bool = True
    approval_requires_expiry: bool = True
    approval_requires_ocel_visibility: bool = True
    pig_guidance_is_not_memory: bool = True
    pig_guidance_is_not_policy_mutation: bool = True
    pig_guidance_is_not_execution: bool = True
    refs_only_by_default: bool = True
    raw_provider_output_inline_forbidden: bool = True
    raw_transcript_inline_forbidden: bool = True
    raw_secret_inline_forbidden: bool = True
    credential_inline_forbidden: bool = True
    private_path_sanitization_required: bool = True
    ocel_visible: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class WorkbenchSafetyApprovalRequest(_Model):
    request_id: str
    version: str = WORKBENCH_SAFETY_APPROVAL_VERSION
    view_state_report_id: str | None = None
    view_state_id: str | None = None
    safety_gate_panel_id: str | None = None
    approval_console_panel_id: str | None = None
    safety_gate_report_id: str | None = None
    gate_outcome_envelope_id: str | None = None
    evidence_inspector_report_id: str | None = None
    provider_browser_report_id: str | None = None
    trace_explorer_report_id: str | None = None
    route_plan_id: str | None = None
    provider_selection_id: str | None = None
    action_candidate_refs: list[dict[str, Any]] = field(default_factory=list)
    pig_guidance_refs: list[dict[str, Any]] = field(default_factory=list)
    human_intervention_refs: list[dict[str, Any]] = field(default_factory=list)
    focus_approval_candidate_ref: dict[str, Any] | None = None
    requested_decision: str | None = None
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"


@dataclass(frozen=True)
class WorkbenchSafetyGateSourceView(_Model):
    source_view_id: str
    version: str = WORKBENCH_SAFETY_APPROVAL_VERSION
    safety_gate_report_ref: dict[str, Any] | None = None
    gate_outcome_ref: dict[str, Any] | None = None
    risk_refs: list[dict[str, Any]] = field(default_factory=list)
    policy_refs: list[dict[str, Any]] = field(default_factory=list)
    no_action_refs: list[dict[str, Any]] = field(default_factory=list)
    clarification_refs: list[dict[str, Any]] = field(default_factory=list)
    blocked_refs: list[dict[str, Any]] = field(default_factory=list)
    deferred_refs: list[dict[str, Any]] = field(default_factory=list)
    allow_route_refs: list[dict[str, Any]] = field(default_factory=list)
    evidence_refs_in_source: list[dict[str, Any]] = field(default_factory=list)
    pig_guidance_refs: list[dict[str, Any]] = field(default_factory=list)
    source_status: str = "complete"
    raw_provider_output_included: bool = False
    raw_transcript_included: bool = False
    raw_secret_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class WorkbenchSafetyGateView(_Model):
    safety_gate_view_id: str
    panel_id: str | None
    source_view: WorkbenchSafetyGateSourceView
    gate_outcome: str | None
    safety_summary: str
    rationale_refs: list[dict[str, Any]]
    risk_refs: list[dict[str, Any]]
    policy_refs: list[dict[str, Any]]
    user_intent_refs: list[dict[str, Any]]
    human_intervention_refs: list[dict[str, Any]]
    view_status: str
    version: str = WORKBENCH_SAFETY_APPROVAL_VERSION
    safety_policy_mutated_now: bool = False
    approval_created_now: bool = False
    execution_triggered_now: bool = False
    raw_secret_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class WorkbenchSafetyRationaleConsoleView(_Model):
    rationale_console_view_id: str
    safety_gate_view_id: str
    rationale_items: list[dict[str, Any]]
    policy_refs: list[dict[str, Any]]
    risk_refs: list[dict[str, Any]]
    pig_guidance_refs: list[dict[str, Any]]
    explanation_status: str
    version: str = WORKBENCH_SAFETY_APPROVAL_VERSION
    safety_policy_mutated_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class WorkbenchApprovalCandidateEvidenceBundle(_Model):
    approval_evidence_bundle_id: str
    evidence_refs: list[dict[str, Any]]
    claim_refs: list[dict[str, Any]]
    safety_refs: list[dict[str, Any]]
    route_refs: list[dict[str, Any]]
    provider_refs: list[dict[str, Any]]
    pig_guidance_refs: list[dict[str, Any]]
    failure_cause_refs: list[dict[str, Any]]
    evidence_count: int
    evidence_status: str
    version: str = WORKBENCH_SAFETY_APPROVAL_VERSION
    raw_provider_output_included: bool = False
    raw_transcript_included: bool = False
    raw_secret_included: bool = False


@dataclass(frozen=True)
class WorkbenchActionRiskSummary(_Model):
    risk_summary_id: str
    risk_level: str
    risk_categories: list[str]
    risk_summary: str
    mitigation_refs: list[dict[str, Any]]
    human_review_required: bool
    evidence_refs: list[dict[str, Any]]
    version: str = WORKBENCH_SAFETY_APPROVAL_VERSION


@dataclass(frozen=True)
class WorkbenchApprovalRequirement(_Model):
    requirement_id: str
    requirement_type: str
    description: str
    required: bool
    source_refs: list[dict[str, Any]]
    version: str = WORKBENCH_SAFETY_APPROVAL_VERSION
    satisfied_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class WorkbenchApprovalScope(_Model):
    scope_id: str
    scope_type: str
    scope_summary: str
    allowed_refs: list[dict[str, Any]]
    forbidden_refs: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]]
    version: str = WORKBENCH_SAFETY_APPROVAL_VERSION
    max_use_count: int = 1
    scope_status: str = "valid"
    scope_grants_execution_now: bool = False


@dataclass(frozen=True)
class WorkbenchApprovalExpiry(_Model):
    expiry_id: str
    expires_at: str | None
    expires_after_turn_count: int | None
    expires_after_use_count: int | None
    expiry_summary: str
    expired_now: bool
    evidence_refs: list[dict[str, Any]]
    version: str = WORKBENCH_SAFETY_APPROVAL_VERSION


@dataclass(frozen=True)
class WorkbenchPIGGuidanceAttachment(_Model):
    pig_guidance_attachment_id: str
    attached_to_ref: dict[str, Any]
    guidance_summary: str
    guidance_type: str
    source_pig_ref: dict[str, Any] | None = None
    version: str = WORKBENCH_SAFETY_APPROVAL_VERSION
    pig_guidance_is_memory: bool = False
    pig_guidance_mutates_policy: bool = False
    pig_guidance_executes: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class WorkbenchApprovalHumanInterventionPoint(_Model):
    intervention_point_id: str
    intervention_type: str
    reason: str
    source_refs: list[dict[str, Any]]
    approval_candidate_ref: dict[str, Any] | None
    approval_created_now: bool
    version: str = WORKBENCH_SAFETY_APPROVAL_VERSION
    execution_triggered_now: bool = False
    ocel_visible: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class WorkbenchApprovalCandidate(_Model):
    approval_candidate_id: str
    candidate_type: str
    title: str
    summary: str
    user_intent_refs: list[dict[str, Any]]
    policy_refs: list[dict[str, Any]]
    evidence_bundle: WorkbenchApprovalCandidateEvidenceBundle
    risk_summary: WorkbenchActionRiskSummary
    approval_requirements: list[WorkbenchApprovalRequirement]
    approval_scope: WorkbenchApprovalScope
    approval_expiry: WorkbenchApprovalExpiry
    pig_guidance_attachments: list[WorkbenchPIGGuidanceAttachment]
    human_intervention_points: list[WorkbenchApprovalHumanInterventionPoint]
    candidate_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = WORKBENCH_SAFETY_APPROVAL_VERSION
    executable_now: bool = False
    execution_triggered_now: bool = False
    approval_decision_required: bool = True


@dataclass(frozen=True)
class WorkbenchApprovalToken(_Model):
    approval_token_id: str
    approval_candidate_id: str
    scope_ref: dict[str, Any]
    expiry_ref: dict[str, Any]
    evidence_refs: list[dict[str, Any]]
    decision_record_id: str | None = None
    token_status: str = "proposed"
    version: str = WORKBENCH_SAFETY_APPROVAL_VERSION
    token_is_command: bool = False
    token_executes_now: bool = False
    token_grants_unbounded_execution: bool = False


@dataclass(frozen=True)
class WorkbenchApprovalDecision(_Model):
    approval_decision_id: str
    approval_candidate_id: str
    decision_type: str
    decision_reason: str
    decided_by: str
    decision_refs: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]]
    decided_at: str | None = None
    version: str = WORKBENCH_SAFETY_APPROVAL_VERSION
    creates_execution: bool = False
    provider_invoked_now: bool = False
    local_command_executed_now: bool = False


@dataclass(frozen=True)
class WorkbenchApprovalDecisionRecord(_Model):
    decision_record_id: str
    approval_decision: WorkbenchApprovalDecision
    approval_token: WorkbenchApprovalToken | None
    record_status: str
    version: str = WORKBENCH_SAFETY_APPROVAL_VERSION
    ocel_visible: bool = True
    execution_triggered: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class WorkbenchRejectionDecisionRecord(_Model):
    rejection_record_id: str
    approval_candidate_id: str
    rejection_reason: str
    rejected_refs: list[dict[str, Any]]
    alternative_refs: list[dict[str, Any]]
    record_status: str
    version: str = WORKBENCH_SAFETY_APPROVAL_VERSION
    execution_triggered: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class WorkbenchDeferralDecisionRecord(_Model):
    deferral_record_id: str
    approval_candidate_id: str
    deferral_reason: str
    deferred_until: str | None
    deferred_to_surface: str | None
    required_followup_refs: list[dict[str, Any]]
    record_status: str
    version: str = WORKBENCH_SAFETY_APPROVAL_VERSION
    execution_triggered: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class WorkbenchManualReviewRecord(_Model):
    manual_review_record_id: str
    review_subject_ref: dict[str, Any]
    review_reason: str
    reviewer_ref: dict[str, Any] | None
    review_status: str
    decision_ref: dict[str, Any] | None
    version: str = WORKBENCH_SAFETY_APPROVAL_VERSION
    execution_triggered: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class WorkbenchApprovalAuditTrail(_Model):
    audit_trail_id: str
    approval_candidate_refs: list[dict[str, Any]]
    decision_record_refs: list[dict[str, Any]]
    rejection_record_refs: list[dict[str, Any]]
    deferral_record_refs: list[dict[str, Any]]
    manual_review_record_refs: list[dict[str, Any]]
    audit_event_count: int
    audit_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = WORKBENCH_SAFETY_APPROVAL_VERSION
    raw_secret_included: bool = False
    raw_provider_output_included: bool = False


@dataclass(frozen=True)
class WorkbenchApprovalConsoleView(_Model):
    approval_console_view_id: str
    panel_id: str | None
    safety_gate_view_id: str | None
    approval_candidates: list[WorkbenchApprovalCandidate]
    approval_decisions: list[WorkbenchApprovalDecision]
    manual_review_records: list[WorkbenchManualReviewRecord]
    audit_trail: WorkbenchApprovalAuditTrail | None
    console_status: str
    version: str = WORKBENCH_SAFETY_APPROVAL_VERSION
    renders_ui_now: bool = False
    approval_executed: bool = False
    command_executed: bool = False
    provider_invoked: bool = False
    local_command_executed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class WorkbenchApprovalConsoleFinding(_Model):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass(frozen=True)
class WorkbenchApprovalConsoleReport(_Model):
    report_id: str
    created_at: str
    safety_approval_policy: WorkbenchSafetyApprovalPolicy
    request: WorkbenchSafetyApprovalRequest
    source_view: WorkbenchSafetyGateSourceView
    safety_gate_view: WorkbenchSafetyGateView
    safety_rationale_console_view: WorkbenchSafetyRationaleConsoleView
    approval_console_view: WorkbenchApprovalConsoleView
    approval_audit_trail: WorkbenchApprovalAuditTrail
    findings: list[WorkbenchApprovalConsoleFinding]
    report_status: str
    ready_for_v0_26_6: bool
    safety_gate_view_created: bool
    approval_console_view_created: bool
    approval_candidates_created: bool
    approval_decisions_recorded: bool
    rejection_decisions_recorded: bool
    deferral_decisions_recorded: bool
    manual_review_records_created: bool
    human_intervention_points_created: bool
    audit_trail_created: bool
    version: str = WORKBENCH_SAFETY_APPROVAL_VERSION
    ready_for_v0_27: bool = False
    actual_ui_rendered: bool = False
    panel_rendered: bool = False
    approval_executed: bool = False
    approval_token_executed: bool = False
    auto_approval_performed: bool = False
    command_executed: bool = False
    provider_invoked: bool = False
    route_rerun_performed: bool = False
    stage_rerun_performed: bool = False
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
    next_required_step: str = WORKBENCH_SAFETY_APPROVAL_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = (
        "Valid until v0.26.6 Run Dashboard / Session Monitor begins or approval console policy changes."
    )


class WorkbenchApprovalConsolePrerequisiteSourceService:
    def __init__(
        self,
        *,
        view_state_available: bool = True,
        safety_gate_panel_available: bool = True,
        approval_console_panel_available: bool = True,
        safety_gate_available: bool = True,
        evidence_inspector_available: bool = True,
        provider_browser_available: bool = True,
        trace_explorer_available: bool = True,
        routing_available: bool = True,
        action_candidate_available: bool = True,
        pig_guidance_available: bool = True,
        human_intervention_available: bool = True,
    ) -> None:
        self.view_state_available = view_state_available
        self.safety_gate_panel_available = safety_gate_panel_available
        self.approval_console_panel_available = approval_console_panel_available
        self.safety_gate_available = safety_gate_available
        self.evidence_inspector_available = evidence_inspector_available
        self.provider_browser_available = provider_browser_available
        self.trace_explorer_available = trace_explorer_available
        self.routing_available = routing_available
        self.action_candidate_available = action_candidate_available
        self.pig_guidance_available = pig_guidance_available
        self.human_intervention_available = human_intervention_available

    def load_workbench_view_state(self) -> dict[str, Any] | None:
        if not self.view_state_available:
            return None
        return WorkbenchViewStateReportService().build_all_parts()

    def load_safety_gate_panel_model(self, view_state: dict[str, Any] | None) -> Any | None:
        if not self.safety_gate_panel_available:
            return None
        return _panel_by_type(view_state, "safety_gate_view")

    def load_approval_console_panel_model(self, view_state: dict[str, Any] | None) -> Any | None:
        if not self.approval_console_panel_available:
            return None
        return _panel_by_type(view_state, "approval_console")

    def load_safety_gate_report_if_available(self) -> dict[str, Any] | None:
        if not self.safety_gate_available:
            return None
        return AgentSafetyGateReportService().build_all_parts()

    def load_gate_outcome_envelope_if_available(self, safety_gate: dict[str, Any] | None) -> Any | None:
        if not safety_gate:
            return None
        return safety_gate.get("outcome_envelope")

    def load_evidence_inspector_report_if_available(self) -> dict[str, Any] | None:
        if not self.evidence_inspector_available:
            return None
        return WorkbenchEvidenceInspectorReportService().build_all_parts()

    def load_provider_browser_report_if_available(self) -> dict[str, Any] | None:
        if not self.provider_browser_available:
            return None
        return WorkbenchProviderBrowserReportService().build_all_parts()

    def load_trace_explorer_report_if_available(self) -> dict[str, Any] | None:
        if not self.trace_explorer_available:
            return None
        return WorkbenchTraceExplorerReportService().build_all_parts()

    def load_route_plan_if_available(self) -> Any | None:
        if not self.routing_available:
            return None
        return AgentToolRoutingReportService().build_all_parts()

    def load_action_candidate_refs_if_available(self, evidence_inspector: dict[str, Any] | None) -> list[dict[str, Any]]:
        if not self.action_candidate_available or not evidence_inspector:
            return []
        views = evidence_inspector.get("action_candidate_evidence_views") or []
        return [
            _model_ref("workbench_action_candidate_evidence_view", view, "action_candidate_evidence_view_id")
            for view in views
        ]

    def load_pig_guidance_refs_if_available(
        self,
        evidence_inspector: dict[str, Any] | None,
        provider_browser: dict[str, Any] | None,
    ) -> list[dict[str, Any]]:
        if not self.pig_guidance_available:
            return []
        refs: list[dict[str, Any]] = []
        if evidence_inspector:
            refs.extend(
                _model_ref("workbench_pig_guidance_inspector_view", item, "pig_guidance_inspector_view_id")
                for item in evidence_inspector.get("pig_guidance_views", [])
            )
        if provider_browser:
            refs.extend(
                _model_ref("workbench_provider_pig_guidance_view", item, "pig_guidance_view_id")
                for item in provider_browser.get("pig_guidance_views", [])
            )
        return refs

    def load_human_intervention_refs_if_available(
        self,
        evidence_inspector: dict[str, Any] | None,
        provider_browser: dict[str, Any] | None,
    ) -> list[dict[str, Any]]:
        if not self.human_intervention_available:
            return []
        refs: list[dict[str, Any]] = []
        if evidence_inspector:
            refs.extend(evidence_inspector.get("source_view").human_intervention_refs)
        if provider_browser:
            refs.extend(
                _model_ref("workbench_human_intervention_point_ref", item, "human_intervention_point_id")
                for item in provider_browser.get("human_intervention_points", [])
            )
        return refs

    def load_sources(self) -> dict[str, Any]:
        view_state = self.load_workbench_view_state()
        safety_gate_panel = self.load_safety_gate_panel_model(view_state)
        approval_console_panel = self.load_approval_console_panel_model(view_state)
        safety_gate = self.load_safety_gate_report_if_available()
        gate_outcome = self.load_gate_outcome_envelope_if_available(safety_gate)
        evidence_inspector = self.load_evidence_inspector_report_if_available()
        provider_browser = self.load_provider_browser_report_if_available()
        trace_explorer = self.load_trace_explorer_report_if_available()
        routing = self.load_route_plan_if_available()
        return {
            "view_state": view_state,
            "safety_gate_panel": safety_gate_panel,
            "approval_console_panel": approval_console_panel,
            "safety_gate": safety_gate,
            "gate_outcome": gate_outcome,
            "evidence_inspector": evidence_inspector,
            "provider_browser": provider_browser,
            "trace_explorer": trace_explorer,
            "routing": routing,
            "action_candidate_refs": self.load_action_candidate_refs_if_available(evidence_inspector),
            "pig_guidance_refs": self.load_pig_guidance_refs_if_available(evidence_inspector, provider_browser),
            "human_intervention_refs": self.load_human_intervention_refs_if_available(
                evidence_inspector,
                provider_browser,
            ),
        }


class WorkbenchSafetyApprovalPolicyService:
    def build_policy(self) -> WorkbenchSafetyApprovalPolicy:
        return WorkbenchSafetyApprovalPolicy(
            policy_id=_model_id("workbench_safety_approval_policy"),
            evidence_refs=[_ref("roadmap_policy", WORKBENCH_SAFETY_APPROVAL_VERSION)],
        )


class WorkbenchSafetyApprovalRequestService:
    def build_request(
        self,
        sources: dict[str, Any],
        *,
        requested_decision: str | None = None,
        candidate_id: str | None = None,
        strictness: str = "standard",
    ) -> WorkbenchSafetyApprovalRequest:
        view_state = sources.get("view_state")
        view_state_model = view_state.get("view_state") if view_state else None
        view_state_report = view_state.get("report") if view_state else None
        safety_gate = sources.get("safety_gate")
        safety_report = safety_gate.get("report") if safety_gate else None
        gate_outcome = sources.get("gate_outcome")
        evidence_report = sources.get("evidence_inspector", {}).get("report") if sources.get("evidence_inspector") else None
        provider_report = sources.get("provider_browser", {}).get("report") if sources.get("provider_browser") else None
        trace_report = sources.get("trace_explorer", {}).get("report") if sources.get("trace_explorer") else None
        route_report = sources.get("routing", {}).get("report") if sources.get("routing") else None
        route_plan = sources.get("routing", {}).get("route_plan") if sources.get("routing") else None
        provider_selection = sources.get("routing", {}).get("provider_selection") if sources.get("routing") else None
        return WorkbenchSafetyApprovalRequest(
            request_id=_model_id("workbench_safety_approval_request", requested_decision or "default"),
            view_state_report_id=getattr(view_state_report, "report_id", None),
            view_state_id=getattr(view_state_model, "view_state_id", None),
            safety_gate_panel_id=getattr(sources.get("safety_gate_panel"), "panel_id", None),
            approval_console_panel_id=getattr(sources.get("approval_console_panel"), "panel_id", None),
            safety_gate_report_id=getattr(safety_report, "report_id", None),
            gate_outcome_envelope_id=getattr(gate_outcome, "outcome_envelope_id", None),
            evidence_inspector_report_id=getattr(evidence_report, "report_id", None),
            provider_browser_report_id=getattr(provider_report, "report_id", None),
            trace_explorer_report_id=getattr(trace_report, "report_id", None),
            route_plan_id=getattr(route_plan, "route_plan_id", None),
            provider_selection_id=getattr(provider_selection, "provider_selection_id", None),
            action_candidate_refs=sources.get("action_candidate_refs", []),
            pig_guidance_refs=sources.get("pig_guidance_refs", []),
            human_intervention_refs=sources.get("human_intervention_refs", []),
            focus_approval_candidate_ref=(
                _ref("workbench_approval_candidate", candidate_id) if candidate_id else None
            ),
            requested_decision=requested_decision,
            source_refs=[
                ref
                for ref in [
                    _ref("workbench_view_state", getattr(view_state_model, "view_state_id", None))
                    if view_state_model
                    else None,
                    _ref("agent_safety_gate_report", getattr(safety_report, "report_id", None))
                    if safety_report
                    else None,
                    _ref("workbench_evidence_inspector_report", getattr(evidence_report, "report_id", None))
                    if evidence_report
                    else None,
                ]
                if ref is not None
            ],
            strictness=strictness,
        )


class WorkbenchSafetyGateSourceViewService:
    def build_source_view(self, sources: dict[str, Any]) -> WorkbenchSafetyGateSourceView:
        safety_gate = sources.get("safety_gate")
        safety_report = safety_gate.get("report") if safety_gate else None
        gate_outcome = sources.get("gate_outcome")
        evidence_inspector = sources.get("evidence_inspector")
        evidence_summary = getattr(evidence_inspector.get("inspection_summary"), "evidence_summary", []) if evidence_inspector else []
        safety_rationale = evidence_inspector.get("safety_rationale_views", []) if evidence_inspector else []
        routing = sources.get("routing")
        route_report = routing.get("report") if routing else None
        status = "complete" if safety_report and evidence_inspector else "partial"
        if not safety_report and not evidence_inspector:
            status = "missing"
        return WorkbenchSafetyGateSourceView(
            source_view_id=_model_id("workbench_safety_gate_source_view"),
            safety_gate_report_ref=(
                _model_ref("agent_safety_gate_report", safety_report, "report_id") if safety_report else None
            ),
            gate_outcome_ref=(
                _model_ref("agent_gate_outcome_envelope", gate_outcome, "outcome_envelope_id")
                if gate_outcome
                else None
            ),
            risk_refs=[
                _ref("safety_risk_ref", "safety_gate_risk_summary"),
                *[
                    _model_ref("workbench_safety_rationale_view", item, "safety_rationale_view_id")
                    for item in safety_rationale
                ],
            ],
            policy_refs=[_ref("workbench_safety_approval_policy", WORKBENCH_SAFETY_APPROVAL_VERSION)],
            no_action_refs=[_ref("agent_gate_outcome", "no_action")]
            if getattr(gate_outcome, "no_action_decision", None)
            else [],
            clarification_refs=[_ref("agent_gate_outcome", "clarification")]
            if getattr(gate_outcome, "clarification_decision", None)
            else [],
            blocked_refs=[_ref("agent_gate_outcome", "blocked")] if getattr(gate_outcome, "blocked_decision", None) else [],
            deferred_refs=[_ref("agent_gate_outcome", "deferred")] if getattr(gate_outcome, "deferred_decision", None) else [],
            allow_route_refs=[_ref("agent_tool_routing_report", getattr(route_report, "report_id", None))]
            if route_report
            else [],
            evidence_refs_in_source=evidence_summary
            or [_ref("workbench_evidence_inspector_report", getattr(evidence_inspector.get("report"), "report_id", None))]
            if evidence_inspector
            else [],
            pig_guidance_refs=sources.get("pig_guidance_refs", []),
            source_status=status,
            evidence_refs=[_ref("source_view_rule", "refs_only_safety_approval")],
        )


class WorkbenchSafetyGateViewService:
    def build_safety_gate_view(
        self,
        request: WorkbenchSafetyApprovalRequest,
        source_view: WorkbenchSafetyGateSourceView,
        sources: dict[str, Any],
    ) -> WorkbenchSafetyGateView:
        safety_gate = sources.get("safety_gate") or {}
        decision = safety_gate.get("decision")
        gate_outcome = getattr(decision, "primary_outcome", None)
        status = "ready" if source_view.safety_gate_report_ref else "partial"
        return WorkbenchSafetyGateView(
            safety_gate_view_id=_model_id("workbench_safety_gate_view"),
            panel_id=request.safety_gate_panel_id,
            source_view=source_view,
            gate_outcome=gate_outcome,
            safety_summary=(
                "Safety gate outcome is represented as refs and rationale for approval review only."
            ),
            rationale_refs=[_ref("agent_safety_gate_decision", getattr(decision, "decision_id", None))]
            if decision
            else [],
            risk_refs=source_view.risk_refs,
            policy_refs=source_view.policy_refs,
            user_intent_refs=[_ref("agent_intent_classification_report", "intent_report_ref")],
            human_intervention_refs=sources.get("human_intervention_refs", []),
            view_status=status,
            evidence_refs=source_view.evidence_refs_in_source,
        )


class WorkbenchSafetyRationaleConsoleViewService:
    def build_rationale_console_view(
        self,
        safety_gate_view: WorkbenchSafetyGateView,
        source_view: WorkbenchSafetyGateSourceView,
    ) -> WorkbenchSafetyRationaleConsoleView:
        return WorkbenchSafetyRationaleConsoleView(
            rationale_console_view_id=_model_id("workbench_safety_rationale_console_view"),
            safety_gate_view_id=safety_gate_view.safety_gate_view_id,
            rationale_items=[
                {
                    "rationale_type": "safety_gate",
                    "summary": safety_gate_view.safety_summary,
                    "gate_outcome": safety_gate_view.gate_outcome,
                }
            ],
            policy_refs=source_view.policy_refs,
            risk_refs=source_view.risk_refs,
            pig_guidance_refs=source_view.pig_guidance_refs,
            explanation_status=safety_gate_view.view_status,
            evidence_refs=source_view.evidence_refs,
        )


class WorkbenchApprovalCandidateEvidenceBundleService:
    def build_evidence_bundle(self, source_view: WorkbenchSafetyGateSourceView) -> WorkbenchApprovalCandidateEvidenceBundle:
        evidence_refs = list(source_view.evidence_refs_in_source)
        return WorkbenchApprovalCandidateEvidenceBundle(
            approval_evidence_bundle_id=_model_id("workbench_approval_candidate_evidence_bundle"),
            evidence_refs=evidence_refs,
            claim_refs=[_ref("agent_claim", "claim_ref")],
            safety_refs=[source_view.safety_gate_report_ref] if source_view.safety_gate_report_ref else [],
            route_refs=source_view.allow_route_refs,
            provider_refs=[],
            pig_guidance_refs=source_view.pig_guidance_refs,
            failure_cause_refs=[],
            evidence_count=len(evidence_refs),
            evidence_status="complete" if evidence_refs else "partial",
        )


class WorkbenchActionRiskSummaryService:
    def build_risk_summary(self, source_view: WorkbenchSafetyGateSourceView) -> WorkbenchActionRiskSummary:
        risk_categories = ["provider_boundary"] if source_view.allow_route_refs else ["unknown"]
        risk_level = "medium" if source_view.allow_route_refs else "low"
        return WorkbenchActionRiskSummary(
            risk_summary_id=_model_id("workbench_action_risk_summary"),
            risk_level=risk_level,
            risk_categories=risk_categories,
            risk_summary="Risk is summarized from existing safety, route, provider, and evidence refs only.",
            mitigation_refs=source_view.policy_refs,
            human_review_required=True,
            evidence_refs=source_view.risk_refs,
        )


class WorkbenchApprovalRequirementService:
    def build_requirements(
        self,
        source_view: WorkbenchSafetyGateSourceView,
        risk_summary: WorkbenchActionRiskSummary,
    ) -> list[WorkbenchApprovalRequirement]:
        requirements = [
            ("user_confirmation", "Human user intent reference must be reviewed."),
            ("policy_acknowledgement", "Relevant safety and approval policy references must be reviewed."),
            ("risk_acceptance", "Risk summary must be acknowledged before any future command surface use."),
            ("scope_confirmation", "Approval scope must be bounded before decision recording."),
            ("expiry_confirmation", "Approval expiry must be bounded before decision recording."),
            ("manual_review", "Manual review is required for OCEL-visible approval decisions."),
        ]
        source_refs = source_view.policy_refs + source_view.evidence_refs_in_source + risk_summary.evidence_refs
        return [
            WorkbenchApprovalRequirement(
                requirement_id=_model_id("workbench_approval_requirement", requirement_type),
                requirement_type=requirement_type,
                description=description,
                required=True,
                source_refs=source_refs,
                evidence_refs=source_view.evidence_refs,
            )
            for requirement_type, description in requirements
        ]


class WorkbenchApprovalScopeService:
    def build_scope(self, source_view: WorkbenchSafetyGateSourceView) -> WorkbenchApprovalScope:
        scope_type = "single_route" if source_view.allow_route_refs else "inspection_only"
        return WorkbenchApprovalScope(
            scope_id=_model_id("workbench_approval_scope"),
            scope_type=scope_type,
            scope_summary="Approval scope is a single bounded reference and grants no execution in v0.26.5.",
            allowed_refs=source_view.allow_route_refs or source_view.evidence_refs_in_source,
            forbidden_refs=[
                _ref("forbidden_effect", effect_type) for effect_type in WORKBENCH_SAFETY_APPROVAL_FORBIDDEN_EFFECT_TYPES
            ],
            evidence_refs=source_view.evidence_refs,
            scope_status="valid" if source_view.evidence_refs_in_source else "incomplete",
        )


class WorkbenchApprovalExpiryService:
    def build_expiry(self) -> WorkbenchApprovalExpiry:
        return WorkbenchApprovalExpiry(
            expiry_id=_model_id("workbench_approval_expiry"),
            expires_at=None,
            expires_after_turn_count=1,
            expires_after_use_count=1,
            expiry_summary="Approval reference expires after one turn or one use and does not execute by itself.",
            expired_now=False,
            evidence_refs=[_ref("expiry_policy", "single_turn_single_use")],
        )


class WorkbenchPIGGuidanceAttachmentService:
    def attach_pig_guidance_refs(
        self,
        pig_guidance_refs: list[dict[str, Any]],
        attached_to_ref: dict[str, Any],
    ) -> list[WorkbenchPIGGuidanceAttachment]:
        refs = pig_guidance_refs or [_ref("pig_guidance_ref", "optional_missing")]
        return [
            WorkbenchPIGGuidanceAttachment(
                pig_guidance_attachment_id=_model_id("workbench_pig_guidance_attachment", str(index + 1)),
                source_pig_ref=source_pig_ref,
                attached_to_ref=attached_to_ref,
                guidance_summary="PIG guidance is attached as a non-executing approval rationale reference.",
                guidance_type="rationale",
                evidence_refs=[source_pig_ref],
            )
            for index, source_pig_ref in enumerate(refs)
        ]


class WorkbenchApprovalHumanInterventionPointService:
    def build_human_intervention_points(
        self,
        source_refs: list[dict[str, Any]],
        approval_candidate_ref: dict[str, Any] | None,
    ) -> list[WorkbenchApprovalHumanInterventionPoint]:
        return [
            WorkbenchApprovalHumanInterventionPoint(
                intervention_point_id=_model_id("workbench_approval_human_intervention_point", "approval_required"),
                intervention_type="approval_required",
                reason="Approval candidate requires a human decision record before any later surface may use it.",
                source_refs=source_refs,
                approval_candidate_ref=approval_candidate_ref,
                approval_created_now=approval_candidate_ref is not None,
                evidence_refs=source_refs,
            )
        ]


class WorkbenchApprovalCandidateService:
    def build_candidates(
        self,
        source_view: WorkbenchSafetyGateSourceView,
        safety_gate_view: WorkbenchSafetyGateView,
        evidence_bundle: WorkbenchApprovalCandidateEvidenceBundle,
        risk_summary: WorkbenchActionRiskSummary,
        requirements: list[WorkbenchApprovalRequirement],
        scope: WorkbenchApprovalScope,
        expiry: WorkbenchApprovalExpiry,
        pig_attachments: list[WorkbenchPIGGuidanceAttachment],
        human_intervention_points: list[WorkbenchApprovalHumanInterventionPoint],
    ) -> list[WorkbenchApprovalCandidate]:
        candidate_type = "route_approval" if source_view.allow_route_refs else "manual_review"
        status = "ready_for_review"
        if not safety_gate_view.user_intent_refs or not source_view.policy_refs or not evidence_bundle.evidence_refs:
            status = "incomplete"
        candidate_id = _model_id("workbench_approval_candidate", candidate_type)
        return [
            WorkbenchApprovalCandidate(
                approval_candidate_id=candidate_id,
                candidate_type=candidate_type,
                title="Safety gate approval review",
                summary="Approval candidate records a bounded decision surface without executing the candidate.",
                user_intent_refs=safety_gate_view.user_intent_refs,
                policy_refs=source_view.policy_refs,
                evidence_bundle=evidence_bundle,
                risk_summary=risk_summary,
                approval_requirements=requirements,
                approval_scope=scope,
                approval_expiry=expiry,
                pig_guidance_attachments=pig_attachments,
                human_intervention_points=human_intervention_points,
                candidate_status=status,
                evidence_refs=evidence_bundle.evidence_refs,
            )
        ]


class WorkbenchApprovalTokenService:
    def build_non_executable_token_ref(
        self,
        candidate: WorkbenchApprovalCandidate,
        *,
        decision_record_id: str | None = None,
        token_status: str = "proposed",
    ) -> WorkbenchApprovalToken:
        return WorkbenchApprovalToken(
            approval_token_id=_model_id("workbench_approval_token", token_status),
            approval_candidate_id=candidate.approval_candidate_id,
            decision_record_id=decision_record_id,
            token_status=token_status,
            scope_ref=_model_ref("workbench_approval_scope", candidate.approval_scope, "scope_id"),
            expiry_ref=_model_ref("workbench_approval_expiry", candidate.approval_expiry, "expiry_id"),
            evidence_refs=candidate.evidence_refs,
        )


class WorkbenchApprovalDecisionService:
    ALLOWED_DECISIONS = {
        "approve",
        "reject",
        "defer",
        "request_clarification",
        "request_more_evidence",
        "revoke",
        "expire",
        "unknown",
    }

    def build_decision(
        self,
        candidate: WorkbenchApprovalCandidate,
        *,
        decision_type: str = "approve",
    ) -> WorkbenchApprovalDecision:
        normalized = decision_type if decision_type in self.ALLOWED_DECISIONS else "unknown"
        return WorkbenchApprovalDecision(
            approval_decision_id=_model_id("workbench_approval_decision", normalized),
            approval_candidate_id=candidate.approval_candidate_id,
            decision_type=normalized,
            decision_reason=f"{normalized} decision recorded as OCEL-visible approval console record only.",
            decided_by="system_test_fixture",
            decided_at=_utc_now(),
            decision_refs=[_model_ref("workbench_approval_candidate", candidate, "approval_candidate_id")],
            evidence_refs=candidate.evidence_refs,
        )


class WorkbenchApprovalDecisionRecordService:
    def build_approval_decision_record(
        self,
        decision: WorkbenchApprovalDecision,
        token: WorkbenchApprovalToken,
    ) -> WorkbenchApprovalDecisionRecord:
        return WorkbenchApprovalDecisionRecord(
            decision_record_id=_model_id("workbench_approval_decision_record", decision.decision_type),
            approval_decision=decision,
            approval_token=token,
            record_status="recorded",
            evidence_refs=decision.evidence_refs,
        )

    def build_rejection_decision_record(
        self,
        candidate: WorkbenchApprovalCandidate,
    ) -> WorkbenchRejectionDecisionRecord:
        return WorkbenchRejectionDecisionRecord(
            rejection_record_id=_model_id("workbench_rejection_decision_record"),
            approval_candidate_id=candidate.approval_candidate_id,
            rejection_reason="Rejection is recorded as a first-class non-executing decision.",
            rejected_refs=[_model_ref("workbench_approval_candidate", candidate, "approval_candidate_id")],
            alternative_refs=[_ref("do_nothing_alternative", "available")],
            record_status="recorded",
            evidence_refs=candidate.evidence_refs,
        )

    def build_deferral_decision_record(
        self,
        candidate: WorkbenchApprovalCandidate,
    ) -> WorkbenchDeferralDecisionRecord:
        return WorkbenchDeferralDecisionRecord(
            deferral_record_id=_model_id("workbench_deferral_decision_record"),
            approval_candidate_id=candidate.approval_candidate_id,
            deferral_reason="Deferral keeps the candidate inspectable without executing it.",
            deferred_until=None,
            deferred_to_surface=WORKBENCH_SAFETY_APPROVAL_NEXT_STEP,
            required_followup_refs=[_ref("workbench_future_surface", WORKBENCH_SAFETY_APPROVAL_NEXT_STEP)],
            record_status="recorded",
            evidence_refs=candidate.evidence_refs,
        )


class WorkbenchManualReviewRecordService:
    def build_manual_review_record(self, candidate: WorkbenchApprovalCandidate) -> WorkbenchManualReviewRecord:
        return WorkbenchManualReviewRecord(
            manual_review_record_id=_model_id("workbench_manual_review_record"),
            review_subject_ref=_model_ref("workbench_approval_candidate", candidate, "approval_candidate_id"),
            review_reason="Manual review is required before any later execution-capable surface can consume approval refs.",
            reviewer_ref=_ref("reviewer", "system_test_fixture"),
            review_status="requested",
            decision_ref=None,
            evidence_refs=candidate.evidence_refs,
        )


class WorkbenchApprovalAuditTrailService:
    def build_audit_trail(
        self,
        candidates: list[WorkbenchApprovalCandidate],
        decision_records: list[WorkbenchApprovalDecisionRecord],
        rejection_records: list[WorkbenchRejectionDecisionRecord],
        deferral_records: list[WorkbenchDeferralDecisionRecord],
        manual_review_records: list[WorkbenchManualReviewRecord],
    ) -> WorkbenchApprovalAuditTrail:
        evidence_refs = [
            ref
            for candidate in candidates
            for ref in candidate.evidence_refs
        ]
        event_count = (
            len(candidates)
            + len(decision_records)
            + len(rejection_records)
            + len(deferral_records)
            + len(manual_review_records)
        )
        return WorkbenchApprovalAuditTrail(
            audit_trail_id=_model_id("workbench_approval_audit_trail"),
            approval_candidate_refs=[
                _model_ref("workbench_approval_candidate", item, "approval_candidate_id") for item in candidates
            ],
            decision_record_refs=[
                _model_ref("workbench_approval_decision_record", item, "decision_record_id")
                for item in decision_records
            ],
            rejection_record_refs=[
                _model_ref("workbench_rejection_decision_record", item, "rejection_record_id")
                for item in rejection_records
            ],
            deferral_record_refs=[
                _model_ref("workbench_deferral_decision_record", item, "deferral_record_id")
                for item in deferral_records
            ],
            manual_review_record_refs=[
                _model_ref("workbench_manual_review_record", item, "manual_review_record_id")
                for item in manual_review_records
            ],
            audit_event_count=event_count,
            audit_status="ready" if event_count else "partial",
            evidence_refs=evidence_refs,
        )


class WorkbenchApprovalConsoleViewService:
    def build_console_view(
        self,
        request: WorkbenchSafetyApprovalRequest,
        safety_gate_view: WorkbenchSafetyGateView,
        candidates: list[WorkbenchApprovalCandidate],
        decisions: list[WorkbenchApprovalDecision],
        manual_review_records: list[WorkbenchManualReviewRecord],
        audit_trail: WorkbenchApprovalAuditTrail,
    ) -> WorkbenchApprovalConsoleView:
        return WorkbenchApprovalConsoleView(
            approval_console_view_id=_model_id("workbench_approval_console_view"),
            panel_id=request.approval_console_panel_id,
            safety_gate_view_id=safety_gate_view.safety_gate_view_id,
            approval_candidates=candidates,
            approval_decisions=decisions,
            manual_review_records=manual_review_records,
            audit_trail=audit_trail,
            console_status="ready" if candidates else "partial",
            evidence_refs=safety_gate_view.evidence_refs,
        )


class WorkbenchApprovalConsoleFindingService:
    BLOCKED_FINDINGS = {
        "approval_execution_attempted",
        "approval_token_execution_attempted",
        "auto_approval_attempted",
        "command_execution_attempted",
        "provider_invocation_attempted",
        "route_rerun_attempted",
        "stage_rerun_attempted",
        "ask_execution_attempted",
        "final_response_emission_attempted",
        "local_command_execution_attempted",
        "direct_file_access_attempted",
        "direct_subprocess_attempted",
        "command_rerun_attempted",
        "automatic_repair_attempted",
        "pig_guidance_as_memory_detected",
        "pig_policy_mutation_detected",
        "pig_execution_detected",
        "memory_promotion_attempted",
        "persona_mutation_attempted",
        "external_adapter_detected",
        "vendor_adapter_detected",
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

    CREATED_FINDINGS = {
        "safety_gate_view_created",
        "safety_rationale_console_created",
        "approval_console_view_created",
        "approval_requirement_created",
        "approval_candidate_created",
        "approval_scope_created",
        "approval_expiry_created",
        "approval_token_created",
        "approval_decision_recorded",
        "rejection_decision_recorded",
        "deferral_decision_recorded",
        "manual_review_recorded",
        "pig_guidance_attached",
        "human_intervention_point_identified",
        "approval_audit_trail_created",
    }

    def _finding(self, finding_type: str, severity: str, message: str) -> WorkbenchApprovalConsoleFinding:
        return WorkbenchApprovalConsoleFinding(
            finding_id=_model_id("workbench_approval_console_finding", finding_type),
            severity=severity,
            finding_type=finding_type,
            message=message,
            subject_ref=_ref("workbench_approval_console", finding_type),
            evidence_refs=[_ref("finding_rule", finding_type)],
            withdrawal_condition=f"Withdraw if {finding_type} is disproven by source refs.",
        )

    def build_findings(
        self,
        sources: dict[str, Any],
        request: WorkbenchSafetyApprovalRequest,
        source_view: WorkbenchSafetyGateSourceView,
        candidates: list[WorkbenchApprovalCandidate],
        decision_records: list[WorkbenchApprovalDecisionRecord],
        rejection_records: list[WorkbenchRejectionDecisionRecord],
        deferral_records: list[WorkbenchDeferralDecisionRecord],
        manual_review_records: list[WorkbenchManualReviewRecord],
        audit_trail: WorkbenchApprovalAuditTrail,
        *,
        strictness: str = "standard",
        attempt_flags: dict[str, bool] | None = None,
        extra_findings: list[str] | None = None,
    ) -> list[WorkbenchApprovalConsoleFinding]:
        findings: list[WorkbenchApprovalConsoleFinding] = []
        missing = [
            ("missing_workbench_view_state", sources.get("view_state") is None),
            ("missing_safety_gate_panel", sources.get("safety_gate_panel") is None),
            ("missing_approval_console_panel", sources.get("approval_console_panel") is None),
            ("missing_safety_gate_report", sources.get("safety_gate") is None),
            ("missing_evidence_inspector_report", sources.get("evidence_inspector") is None),
            ("missing_user_intent_ref", not candidates or not candidates[0].user_intent_refs),
            ("missing_policy_ref", not source_view.policy_refs),
            ("missing_evidence_refs", not source_view.evidence_refs_in_source),
            ("missing_risk_summary", not candidates or not candidates[0].risk_summary),
            ("missing_approval_scope", not candidates or not candidates[0].approval_scope),
            ("missing_approval_expiry", not candidates or not candidates[0].approval_expiry),
        ]
        for finding_type, present in missing:
            if present:
                severity = "error" if strictness == "strict" and finding_type in {
                    "missing_safety_gate_report",
                    "missing_user_intent_ref",
                    "missing_policy_ref",
                    "missing_evidence_refs",
                    "missing_risk_summary",
                    "missing_approval_scope",
                    "missing_approval_expiry",
                } else "warning"
                findings.append(self._finding(finding_type, severity, f"{finding_type} is missing."))
        created = [
            ("safety_gate_view_created", True),
            ("safety_rationale_console_created", True),
            ("approval_console_view_created", True),
            ("approval_requirement_created", bool(candidates and candidates[0].approval_requirements)),
            ("approval_candidate_created", bool(candidates)),
            ("approval_scope_created", bool(candidates and candidates[0].approval_scope)),
            ("approval_expiry_created", bool(candidates and candidates[0].approval_expiry)),
            ("approval_token_created", bool(decision_records and decision_records[0].approval_token)),
            ("approval_decision_recorded", bool(decision_records)),
            ("rejection_decision_recorded", bool(rejection_records)),
            ("deferral_decision_recorded", bool(deferral_records)),
            ("manual_review_recorded", bool(manual_review_records)),
            ("pig_guidance_attached", bool(candidates and candidates[0].pig_guidance_attachments)),
            ("human_intervention_point_identified", bool(candidates and candidates[0].human_intervention_points)),
            ("approval_audit_trail_created", audit_trail.audit_event_count > 0),
        ]
        for finding_type, is_created in created:
            if is_created:
                findings.append(self._finding(finding_type, "info", f"{finding_type} completed."))
        for finding_type, attempted in (attempt_flags or {}).items():
            if attempted:
                severity = "critical" if finding_type in self.BLOCKED_FINDINGS else "warning"
                findings.append(self._finding(finding_type, severity, f"{finding_type} detected."))
        for finding_type in extra_findings or []:
            severity = "critical" if finding_type in self.BLOCKED_FINDINGS else "warning"
            findings.append(self._finding(finding_type, severity, f"{finding_type} detected."))
        if not findings:
            findings.append(self._finding("ok", "info", "Safety approval console report is ready."))
        return findings


class WorkbenchApprovalConsoleReportService:
    def build_all_parts(
        self,
        *,
        report_id: str | None = None,
        candidate_id: str | None = None,
        requested_decision: str | None = None,
        strictness: str = "standard",
        attempt_flags: dict[str, bool] | None = None,
        extra_findings: list[str] | None = None,
        view_state_available: bool = True,
        safety_gate_panel_available: bool = True,
        approval_console_panel_available: bool = True,
        safety_gate_available: bool = True,
        evidence_inspector_available: bool = True,
        provider_browser_available: bool = True,
        trace_explorer_available: bool = True,
        routing_available: bool = True,
        action_candidate_available: bool = True,
        pig_guidance_available: bool = True,
        human_intervention_available: bool = True,
    ) -> dict[str, Any]:
        source_service = WorkbenchApprovalConsolePrerequisiteSourceService(
            view_state_available=view_state_available,
            safety_gate_panel_available=safety_gate_panel_available,
            approval_console_panel_available=approval_console_panel_available,
            safety_gate_available=safety_gate_available,
            evidence_inspector_available=evidence_inspector_available,
            provider_browser_available=provider_browser_available,
            trace_explorer_available=trace_explorer_available,
            routing_available=routing_available,
            action_candidate_available=action_candidate_available,
            pig_guidance_available=pig_guidance_available,
            human_intervention_available=human_intervention_available,
        )
        sources = source_service.load_sources()
        policy = WorkbenchSafetyApprovalPolicyService().build_policy()
        request = WorkbenchSafetyApprovalRequestService().build_request(
            sources,
            requested_decision=requested_decision,
            candidate_id=candidate_id,
            strictness=strictness,
        )
        source_view = WorkbenchSafetyGateSourceViewService().build_source_view(sources)
        safety_gate_view = WorkbenchSafetyGateViewService().build_safety_gate_view(request, source_view, sources)
        rationale_console = WorkbenchSafetyRationaleConsoleViewService().build_rationale_console_view(
            safety_gate_view,
            source_view,
        )
        evidence_bundle = WorkbenchApprovalCandidateEvidenceBundleService().build_evidence_bundle(source_view)
        risk_summary = WorkbenchActionRiskSummaryService().build_risk_summary(source_view)
        requirements = WorkbenchApprovalRequirementService().build_requirements(source_view, risk_summary)
        scope = WorkbenchApprovalScopeService().build_scope(source_view)
        expiry = WorkbenchApprovalExpiryService().build_expiry()
        candidate_ref = _ref("workbench_approval_candidate", candidate_id or "route_approval")
        pig_attachments = WorkbenchPIGGuidanceAttachmentService().attach_pig_guidance_refs(
            source_view.pig_guidance_refs,
            candidate_ref,
        )
        human_intervention_points = WorkbenchApprovalHumanInterventionPointService().build_human_intervention_points(
            source_view.evidence_refs_in_source or source_view.policy_refs,
            candidate_ref,
        )
        candidates = WorkbenchApprovalCandidateService().build_candidates(
            source_view,
            safety_gate_view,
            evidence_bundle,
            risk_summary,
            requirements,
            scope,
            expiry,
            pig_attachments,
            human_intervention_points,
        )
        candidate = candidates[0]
        if candidate_id:
            candidate_ref = _model_ref("workbench_approval_candidate", candidate, "approval_candidate_id")
        token = WorkbenchApprovalTokenService().build_non_executable_token_ref(candidate)
        decision_type = requested_decision or "approve"
        decision = WorkbenchApprovalDecisionService().build_decision(candidate, decision_type=decision_type)
        approval_record = WorkbenchApprovalDecisionRecordService().build_approval_decision_record(decision, token)
        rejection_record = WorkbenchApprovalDecisionRecordService().build_rejection_decision_record(candidate)
        deferral_record = WorkbenchApprovalDecisionRecordService().build_deferral_decision_record(candidate)
        manual_review_record = WorkbenchManualReviewRecordService().build_manual_review_record(candidate)
        audit_trail = WorkbenchApprovalAuditTrailService().build_audit_trail(
            candidates,
            [approval_record],
            [rejection_record],
            [deferral_record],
            [manual_review_record],
        )
        console = WorkbenchApprovalConsoleViewService().build_console_view(
            request,
            safety_gate_view,
            candidates,
            [decision],
            [manual_review_record],
            audit_trail,
        )
        findings = WorkbenchApprovalConsoleFindingService().build_findings(
            sources,
            request,
            source_view,
            candidates,
            [approval_record],
            [rejection_record],
            [deferral_record],
            [manual_review_record],
            audit_trail,
            strictness=strictness,
            attempt_flags=attempt_flags,
            extra_findings=extra_findings,
        )
        report_status = self._report_status(findings)
        report = WorkbenchApprovalConsoleReport(
            report_id=report_id or _model_id("workbench_approval_console_report"),
            created_at=_utc_now(),
            safety_approval_policy=policy,
            request=request,
            source_view=source_view,
            safety_gate_view=safety_gate_view,
            safety_rationale_console_view=rationale_console,
            approval_console_view=console,
            approval_audit_trail=audit_trail,
            findings=findings,
            report_status=report_status,
            ready_for_v0_26_6=report_status in {"passed", "warning"},
            safety_gate_view_created=True,
            approval_console_view_created=True,
            approval_candidates_created=bool(candidates),
            approval_decisions_recorded=True,
            rejection_decisions_recorded=True,
            deferral_decisions_recorded=True,
            manual_review_records_created=True,
            human_intervention_points_created=True,
            audit_trail_created=True,
            limitations=[
                "v0.26.5 records approval decisions only; execution-capable command surfaces remain deferred."
            ],
            withdrawal_conditions=[
                "Withdraw readiness if an approval, command, provider, route, memory, or adapter execution path is added."
            ],
        )
        return {
            "report": report,
            "policy": policy,
            "request": request,
            "source_view": source_view,
            "safety_gate_view": safety_gate_view,
            "safety_rationale_console_view": rationale_console,
            "approval_console_view": console,
            "approval_requirements": requirements,
            "approval_candidates": candidates,
            "approval_evidence_bundle": evidence_bundle,
            "risk_summary": risk_summary,
            "approval_scope": scope,
            "approval_expiry": expiry,
            "approval_token": token,
            "approval_decisions": [decision],
            "approval_decision_records": [approval_record],
            "rejection_records": [rejection_record],
            "deferral_records": [deferral_record],
            "manual_review_records": [manual_review_record],
            "pig_guidance_attachments": pig_attachments,
            "human_intervention_points": human_intervention_points,
            "approval_audit_trail": audit_trail,
            "findings": findings,
        }

    def _report_status(self, findings: list[WorkbenchApprovalConsoleFinding]) -> str:
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
            "version": WORKBENCH_SAFETY_APPROVAL_VERSION,
            "layer": WORKBENCH_SAFETY_APPROVAL_LAYER,
            "subject": "safety_gate_approval_console",
            "principles": [
                "Approval Console is not execution",
                "Approval candidate is not command",
                "Approval token is not command token",
                "Approval decision is not provider invocation",
                "Approve / reject / defer must be OCEL-visible",
                "Approval scope is required",
                "Approval expiry is required",
                "User intent ref is required",
                "Policy ref is required",
                "Evidence refs are required",
                "PIG guidance is not memory, policy mutation, or execution",
                "Human intervention point is not approval by itself",
            ],
            "safety_boundary": {
                "safety_gate_view_created": "conditional",
                "approval_console_view_created": "conditional",
                "approval_candidates_created": "conditional",
                "approval_decisions_recorded": "conditional",
                "rejection_decisions_recorded": "conditional",
                "deferral_decisions_recorded": "conditional",
                "manual_review_records_created": "conditional",
                "approval_executed": False,
                "approval_token_executed": False,
                "auto_approval_performed": False,
                "command_executed": False,
                "provider_invoked": False,
                "route_rerun_performed": False,
                "stage_rerun_performed": False,
                "ask_executed": False,
                "final_response_emitted": False,
                "local_command_executed": False,
                "command_rerun_performed": False,
                "automatic_repair_performed": False,
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
                "v0.26.6 run dashboard / session monitor",
                "v0.26.7 command surface",
                "v0.26.8 snapshot / OCEL export",
                "v0.27 memory candidate and continuity",
            ],
            "next_step": WORKBENCH_SAFETY_APPROVAL_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "workbench_safety_gate_approval_console_created",
            "version": WORKBENCH_SAFETY_APPROVAL_VERSION,
            "source_read_models": [
                "WorkbenchViewStateState",
                "WorkbenchEvidenceInspectorViewState",
                "WorkbenchProviderBrowserViewState",
                "WorkbenchTraceExplorerViewState",
                "AgentSafetyGateState",
                "AgentGateOutcomeState",
                "AgentToolRoutingState",
                "AgentProviderSelectionState",
                "PigGuidanceState",
            ],
            "target_read_models": [
                "WorkbenchSafetyGateViewState",
                "WorkbenchSafetyRationaleConsoleState",
                "WorkbenchApprovalConsoleViewState",
                "WorkbenchApprovalCandidateState",
                "WorkbenchApprovalRequirementState",
                "WorkbenchApprovalScopeState",
                "WorkbenchApprovalDecisionRecordState",
                "WorkbenchManualReviewRecordState",
                "WorkbenchApprovalAuditTrailState",
                "V026ReadinessState",
            ],
            "effect_types": WORKBENCH_SAFETY_APPROVAL_EFFECT_TYPES,
        }


def _bool_text(value: bool) -> str:
    return str(value).lower()


def render_workbench_approval_console_cli(parts: dict[str, Any], section: str = "console") -> str:
    report: WorkbenchApprovalConsoleReport = parts["report"]
    common = [
        "Workbench Safety Gate / Approval Console",
        f"version={report.version}",
        f"layer={WORKBENCH_SAFETY_APPROVAL_LAYER}",
        f"safety_gate_view_created={_bool_text(report.safety_gate_view_created)}",
        f"approval_console_view_created={_bool_text(report.approval_console_view_created)}",
        f"approval_candidates_created={_bool_text(report.approval_candidates_created)}",
        f"approval_decisions_recorded={_bool_text(report.approval_decisions_recorded)}",
        f"rejection_decisions_recorded={_bool_text(report.rejection_decisions_recorded)}",
        f"deferral_decisions_recorded={_bool_text(report.deferral_decisions_recorded)}",
        f"manual_review_records_created={_bool_text(report.manual_review_records_created)}",
        f"human_intervention_points_created={_bool_text(report.human_intervention_points_created)}",
        f"audit_trail_created={_bool_text(report.audit_trail_created)}",
        f"ready_for_v0_26_6={_bool_text(report.ready_for_v0_26_6)}",
        f"ready_for_v0_27={_bool_text(report.ready_for_v0_27)}",
        f"approval_executed={_bool_text(report.approval_executed)}",
        f"approval_token_executed={_bool_text(report.approval_token_executed)}",
        f"auto_approval_performed={_bool_text(report.auto_approval_performed)}",
        f"command_executed={_bool_text(report.command_executed)}",
        f"provider_invoked={_bool_text(report.provider_invoked)}",
        f"route_rerun_performed={_bool_text(report.route_rerun_performed)}",
        f"stage_rerun_performed={_bool_text(report.stage_rerun_performed)}",
        f"ask_executed={_bool_text(report.ask_executed)}",
        f"final_response_emitted={_bool_text(report.final_response_emitted)}",
        f"local_command_executed={_bool_text(report.local_command_executed)}",
        f"command_rerun_performed={_bool_text(report.command_rerun_performed)}",
        f"automatic_repair_performed={_bool_text(report.automatic_repair_performed)}",
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
        f"section={section}",
    ]
    if section == "rationale":
        common.append(f"rationale_items={len(parts['safety_rationale_console_view'].rationale_items)}")
    elif section == "candidates":
        common.append(f"candidate_count={len(parts['approval_candidates'])}")
    elif section == "requirements":
        common.append(f"requirement_count={len(parts['approval_requirements'])}")
    elif section == "scope":
        common.append(f"scope_type={parts['approval_scope'].scope_type}")
    elif section == "expiry":
        common.append(f"expires_after_use_count={parts['approval_expiry'].expires_after_use_count}")
    elif section == "decide":
        common.append(f"decision_type={parts['approval_decisions'][0].decision_type}")
        common.append("decision_record_created=true")
        common.append("decision_creates_execution=false")
    elif section == "audit":
        common.append(f"audit_event_count={parts['approval_audit_trail'].audit_event_count}")
    elif section == "report":
        common.append(f"report_status={report.report_status}")
        common.append(f"finding_count={len(report.findings)}")
    else:
        common.append(f"console_status={parts['approval_console_view'].console_status}")
    return "\n".join(common)
