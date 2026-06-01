from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from chanta_core.agent_surface.intent_task import AgentIntentClassificationReportService
from chanta_core.agent_surface.provider_invocation import AgentProviderInvocationReportService
from chanta_core.agent_surface.response_assembly import AgentResponseAssemblyReportService
from chanta_core.agent_surface.safety_gate import AgentSafetyGateReportService
from chanta_core.agent_surface.tool_routing import AgentToolRoutingReportService
from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace_agent_workbench.provider_browser import WorkbenchProviderBrowserReportService
from chanta_core.workspace_agent_workbench.trace_explorer import WorkbenchTraceExplorerReportService
from chanta_core.workspace_agent_workbench.view_state import (
    WorkbenchPanel,
    WorkbenchViewState,
    WorkbenchViewStateReportService,
)


WORKBENCH_EVIDENCE_INSPECTOR_VERSION = "v0.26.4"
WORKBENCH_EVIDENCE_INSPECTOR_VERSION_NAME = "Evidence / Report Inspector"
WORKBENCH_EVIDENCE_INSPECTOR_KOREAN_NAME = "Evidence·Report Inspector"
WORKBENCH_EVIDENCE_INSPECTOR_LAYER = "workspace_agent_workbench"
WORKBENCH_EVIDENCE_INSPECTOR_TRACK = "Workspace Agent Workbench"
WORKBENCH_EVIDENCE_INSPECTOR_NEXT_STEP = "v0.26.5 Safety Gate / Approval Console"

WORKBENCH_EVIDENCE_INSPECTOR_IMPLEMENTED_SKILL_IDS = ["skill:workbench_evidence_inspector_view"]
WORKBENCH_EVIDENCE_INSPECTOR_FUTURE_SKILL_IDS = [
    "skill:workbench_safety_gate_view",
    "skill:workbench_approval_console_view",
    "skill:workbench_run_dashboard_view",
    "skill:workbench_session_monitor_view",
    "skill:workbench_command_surface_use",
    "skill:workbench_snapshot_create",
    "skill:workbench_ocel_export_create",
    "skill:workbench_consolidation_view",
]

WORKBENCH_EVIDENCE_INSPECTOR_OBJECT_TYPES = [
    "workbench_evidence_inspector_policy",
    "workbench_evidence_inspector_request",
    "workbench_evidence_source_view",
    "workbench_evidence_inspector_view",
    "workbench_report_inspector_view",
    "workbench_evidence_bundle_view",
    "workbench_evidence_item_view",
    "workbench_claim_inspector_view",
    "workbench_claim_support_inspector_view",
    "workbench_decision_evidence_view",
    "workbench_skill_selection_evidence_view",
    "workbench_action_candidate_evidence_view",
    "workbench_route_selection_evidence_view",
    "workbench_provider_selection_evidence_view",
    "workbench_safety_rationale_view",
    "workbench_pig_guidance_inspector_view",
    "workbench_failure_cause_view",
    "workbench_unsupported_claim_view",
    "workbench_uncertainty_inspector_view",
    "workbench_limitation_inspector_view",
    "workbench_evidence_filter_state",
    "workbench_evidence_selection_view",
    "workbench_evidence_inspection_summary",
    "workbench_evidence_inspector_finding",
    "workbench_evidence_inspector_report",
    "workbench_view_state",
    "agent_response_assembly_report",
    "agent_evidence_bundle",
    "agent_safety_gate_report",
    "agent_tool_routing_report",
    "agent_provider_invocation_report",
    "pig_report",
    "execution_envelope",
    "ocpx_projection",
]

WORKBENCH_EVIDENCE_INSPECTOR_EVENT_TYPES = [
    "workbench_evidence_inspector_requested",
    "workbench_evidence_inspector_policy_created",
    "workbench_evidence_source_view_created",
    "workbench_report_inspector_view_created",
    "workbench_evidence_inspector_view_created",
    "workbench_evidence_bundle_view_created",
    "workbench_evidence_item_view_created",
    "workbench_claim_inspector_view_created",
    "workbench_claim_support_inspector_view_created",
    "workbench_decision_evidence_view_created",
    "workbench_skill_selection_evidence_view_created",
    "workbench_action_candidate_evidence_view_created",
    "workbench_route_selection_evidence_view_created",
    "workbench_provider_selection_evidence_view_created",
    "workbench_safety_rationale_view_created",
    "workbench_pig_guidance_inspector_view_created",
    "workbench_failure_cause_view_created",
    "workbench_unsupported_claim_view_created",
    "workbench_uncertainty_view_created",
    "workbench_limitation_view_created",
    "workbench_evidence_filter_state_created",
    "workbench_evidence_selection_view_created",
    "workbench_evidence_inspection_summary_created",
    "workbench_evidence_inspector_report_created",
    "workbench_evidence_inspector_warning_created",
    "workbench_evidence_inspector_blocked",
]

WORKBENCH_EVIDENCE_INSPECTOR_RELATION_TYPES = [
    "uses_workbench_view_state",
    "uses_evidence_inspector_panel",
    "uses_response_assembly_report",
    "uses_evidence_bundle",
    "uses_claim_ref",
    "uses_claim_support_ref",
    "uses_safety_gate_report",
    "uses_tool_routing_report",
    "uses_provider_selection_ref",
    "uses_provider_browser_report",
    "uses_pig_guidance_ref",
    "creates_evidence_source_view",
    "creates_report_inspector_view",
    "creates_evidence_bundle_view",
    "creates_claim_inspector_view",
    "creates_claim_support_view",
    "creates_decision_evidence_view",
    "creates_skill_selection_evidence_view",
    "creates_action_candidate_evidence_view",
    "creates_route_selection_evidence_view",
    "creates_provider_selection_evidence_view",
    "creates_safety_rationale_view",
    "creates_pig_guidance_inspector_view",
    "creates_failure_cause_view",
    "creates_unsupported_claim_view",
    "creates_uncertainty_view",
    "creates_limitation_view",
    "prepares_approval_console",
    "defers_approval_console_to_v0_26_5",
    "defers_run_dashboard_to_v0_26_6",
    "defers_command_surface_to_v0_26_7",
    "defers_snapshot_export_to_v0_26_8",
    "defers_memory_continuity_to_v0_27",
    "defers_external_provider_adapters_to_v0_29_plus",
    "defers_external_agent_dominion_to_v0_30_plus",
    "not_response_rewritten",
    "not_factuality_judged_by_llm",
    "not_provider_invoked",
    "not_approval_executed",
    "not_pig_memory_promoted",
    "not_pig_policy_mutated",
    "not_pig_executed",
    "prevents_credential_exposure",
    "blocks_raw_provider_output_inline",
    "blocks_raw_secret_output",
    "recorded_in_envelope",
]

WORKBENCH_EVIDENCE_INSPECTOR_EFFECT_TYPES = [
    "read_only_observation",
    "workbench_evidence_inspector_created",
    "workbench_report_inspector_created",
    "workbench_claim_inspector_created",
    "workbench_decision_evidence_view_created",
    "workbench_skill_selection_evidence_view_created",
    "workbench_action_candidate_evidence_view_created",
    "workbench_route_selection_evidence_view_created",
    "workbench_provider_selection_evidence_view_created",
    "workbench_safety_rationale_view_created",
    "workbench_pig_guidance_inspector_view_created",
    "workbench_failure_cause_view_created",
    "workbench_unsupported_claim_view_created",
    "workbench_evidence_inspection_created",
    "state_candidate_created",
]

WORKBENCH_EVIDENCE_INSPECTOR_FORBIDDEN_EFFECT_TYPES = [
    "response_rewritten",
    "response_regenerated",
    "factuality_llm_judge_used",
    "safety_llm_judge_used",
    "decision_mutated",
    "safety_policy_mutated",
    "provider_invoked",
    "internal_provider_invoked",
    "provider_test_run_performed",
    "route_rerun_performed",
    "stage_rerun_performed",
    "approval_executed",
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


def _ref(ref_type: str, ref_id: str | None, version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION) -> dict[str, Any]:
    return {"type": ref_type, "id": ref_id, "version": version}


def _model_id(value: Any, default: str) -> str:
    for attr in (
        "report_id",
        "evidence_bundle_id",
        "evidence_item_id",
        "claim_id",
        "support_id",
        "uncertainty_id",
        "limitation_id",
        "provider_browser_view_id",
        "trace_explorer_view_id",
    ):
        item = getattr(value, attr, None)
        if item:
            return str(item)
    if isinstance(value, dict):
        return str(value.get("id") or value.get("type") or default)
    return default


def _model_ref(ref_type: str, value: Any, version: str | None = None) -> dict[str, Any]:
    return _ref(ref_type, _model_id(value, ref_type), version or getattr(value, "version", WORKBENCH_EVIDENCE_INSPECTOR_VERSION))


def _summary(value: Any, fallback: str) -> str:
    for attr in ("summary", "message", "failure_summary", "risk_summary", "selection_reason", "readiness_reason"):
        item = getattr(value, attr, None)
        if item:
            return str(item)
    if isinstance(value, dict):
        for key in ("summary", "message", "reason", "status"):
            if value.get(key):
                return str(value[key])
    return fallback


class _Model:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class WorkbenchEvidenceInspectorPolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    layer: str = WORKBENCH_EVIDENCE_INSPECTOR_LAYER
    evidence_inspector_enabled: bool = True
    report_inspector_enabled: bool = True
    decision_evidence_enabled: bool = True
    skill_selection_evidence_enabled: bool = True
    action_candidate_evidence_enabled: bool = True
    route_selection_evidence_enabled: bool = True
    provider_selection_evidence_enabled: bool = True
    safety_rationale_view_enabled: bool = True
    pig_guidance_inspection_enabled: bool = True
    failure_cause_view_enabled: bool = True
    unsupported_claim_view_enabled: bool = True
    uncertainty_limitation_view_enabled: bool = True
    actual_ui_rendering_enabled: bool = False
    panel_rendering_enabled: bool = False
    response_rewrite_enabled: bool = False
    factuality_llm_judge_enabled: bool = False
    safety_llm_judge_enabled: bool = False
    provider_invocation_enabled: bool = False
    route_rerun_enabled: bool = False
    stage_rerun_enabled: bool = False
    approval_execution_enabled: bool = False
    ask_execution_enabled: bool = False
    response_emission_enabled: bool = False
    local_runtime_execution_enabled: bool = False
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
class WorkbenchEvidenceInspectorRequest(_Model):
    request_id: str
    view_state_report_id: str | None
    view_state_id: str | None
    evidence_inspector_panel_id: str | None
    response_assembly_report_id: str | None
    evidence_bundle_id: str | None
    claim_ids: list[str]
    provider_invocation_report_id: str | None
    routing_report_id: str | None
    safety_gate_report_id: str | None
    intent_report_id: str | None
    provider_browser_report_id: str | None
    trace_explorer_report_id: str | None
    pig_guidance_refs: list[dict[str, Any]]
    focus_claim_ref: dict[str, Any] | None
    focus_evidence_ref: dict[str, Any] | None
    filter_refs: list[dict[str, Any]]
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"


@dataclass
class WorkbenchEvidenceSourceView(_Model):
    source_view_id: str
    response_assembly_report_ref: dict[str, Any] | None
    evidence_bundle_ref: dict[str, Any] | None
    claim_refs: list[dict[str, Any]]
    claim_support_refs: list[dict[str, Any]]
    uncertainty_refs: list[dict[str, Any]]
    limitation_refs: list[dict[str, Any]]
    safety_gate_refs: list[dict[str, Any]]
    routing_refs: list[dict[str, Any]]
    provider_selection_refs: list[dict[str, Any]]
    provider_result_refs: list[dict[str, Any]]
    pig_guidance_refs: list[dict[str, Any]]
    failure_cause_refs: list[dict[str, Any]]
    human_intervention_refs: list[dict[str, Any]]
    source_status: str
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    raw_provider_output_included: bool = False
    raw_transcript_included: bool = False
    raw_secret_included: bool = False
    private_full_path_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchEvidenceItemView(_Model):
    evidence_item_view_id: str
    evidence_item_ref: dict[str, Any]
    evidence_kind: str
    source_ref: dict[str, Any] | None
    sanitized_summary: str
    supports_claim_refs: list[dict[str, Any]]
    confidence: str
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    raw_content_included: bool = False
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchEvidenceBundleView(_Model):
    evidence_bundle_view_id: str
    evidence_bundle_ref: dict[str, Any] | None
    evidence_item_views: list[WorkbenchEvidenceItemView]
    evidence_count: int
    provider_evidence_count: int
    policy_evidence_count: int
    uncertainty_evidence_count: int
    unsupported_evidence_count: int
    bundle_status: str
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchClaimInspectorView(_Model):
    claim_view_id: str
    claim_ref: dict[str, Any]
    claim_type: str
    sanitized_claim_text: str
    confidence: str
    requires_evidence: bool
    evidence_item_refs: list[dict[str, Any]]
    support_status: str
    unsupported: bool
    inference_label_required: bool
    provider_observation_label_required: bool
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    raw_claim_content_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchClaimSupportInspectorView(_Model):
    support_view_id: str
    claim_ref: dict[str, Any]
    support_ref: dict[str, Any] | None
    evidence_item_refs: list[dict[str, Any]]
    support_status: str
    missing_evidence_reason: str | None
    support_summary: str
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchDecisionEvidenceView(_Model):
    decision_evidence_view_id: str
    decision_type: str
    decision_ref: dict[str, Any] | None
    rationale_refs: list[dict[str, Any]]
    evidence_item_refs: list[dict[str, Any]]
    pig_guidance_refs: list[dict[str, Any]]
    safety_finding_refs: list[dict[str, Any]]
    decision_outcome: str | None
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    deterministic: bool = True
    decision_mutated_now: bool = False
    llm_judge_used: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSkillSelectionEvidenceView(_Model):
    skill_selection_evidence_view_id: str
    skill_id: str | None
    skill_name: str | None
    candidate_ref: dict[str, Any] | None
    selection_ref: dict[str, Any] | None
    selection_reason_refs: list[dict[str, Any]]
    safety_finding_refs: list[dict[str, Any]]
    pig_guidance_refs: list[dict[str, Any]]
    selected: bool
    rejected: bool
    deferred: bool
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    skill_executed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchActionCandidateEvidenceView(_Model):
    action_candidate_evidence_view_id: str
    action_candidate_ref: dict[str, Any] | None
    action_type: str | None
    rationale_refs: list[dict[str, Any]]
    risk_refs: list[dict[str, Any]]
    approval_requirement_refs: list[dict[str, Any]]
    pig_guidance_refs: list[dict[str, Any]]
    evidence_bound: bool
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    action_executed_now: bool = False
    approval_created_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchRouteSelectionEvidenceView(_Model):
    route_selection_evidence_view_id: str
    route_ref: dict[str, Any] | None
    route_kind: str | None
    selection_rationale_refs: list[dict[str, Any]]
    route_compatibility_refs: list[dict[str, Any]]
    safety_context_refs: list[dict[str, Any]]
    pig_guidance_refs: list[dict[str, Any]]
    human_intervention_refs: list[dict[str, Any]]
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    route_rerun_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchProviderSelectionEvidenceView(_Model):
    provider_selection_evidence_view_id: str
    provider_id: str | None
    capability_id: str | None
    provider_selection_ref: dict[str, Any] | None
    provider_rationale_refs: list[dict[str, Any]]
    boundary_risk_refs: list[dict[str, Any]]
    readiness_refs: list[dict[str, Any]]
    pig_guidance_refs: list[dict[str, Any]]
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    provider_invoked_now: bool = False
    provider_test_run_performed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSafetyRationaleView(_Model):
    safety_rationale_view_id: str
    safety_gate_report_ref: dict[str, Any] | None
    gate_outcome: str | None
    safety_rule_refs: list[dict[str, Any]]
    risk_preview_refs: list[dict[str, Any]]
    blocked_reason_refs: list[dict[str, Any]]
    no_action_rationale_refs: list[dict[str, Any]]
    clarification_requirement_refs: list[dict[str, Any]]
    deferred_reason_refs: list[dict[str, Any]]
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    safety_policy_mutated_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchPIGGuidanceInspectorView(_Model):
    pig_guidance_inspector_view_id: str
    source_pig_ref: dict[str, Any] | None
    guidance_type: str
    guidance_summary: str
    related_decision_refs: list[dict[str, Any]]
    related_route_refs: list[dict[str, Any]]
    related_provider_refs: list[dict[str, Any]]
    related_evidence_refs: list[dict[str, Any]]
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    pig_guidance_is_memory: bool = False
    pig_guidance_mutates_policy: bool = False
    pig_guidance_executes: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchFailureCauseView(_Model):
    failure_cause_view_id: str
    failure_ref: dict[str, Any] | None
    failure_stage: str | None
    failure_category: str
    failure_summary: str
    source_report_refs: list[dict[str, Any]]
    recovery_guidance_refs: list[dict[str, Any]]
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    auto_rerun_enabled: bool = False
    automatic_repair_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchUnsupportedClaimView(_Model):
    unsupported_claim_view_id: str
    claim_ref: dict[str, Any]
    missing_evidence_reason: str | None
    unsupported_severity: str
    suggested_next_surface: str | None
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    auto_corrected: bool = False
    response_rewritten: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchUncertaintyInspectorView(_Model):
    uncertainty_view_id: str
    uncertainty_ref: dict[str, Any]
    uncertainty_summary: str
    affected_claim_refs: list[dict[str, Any]]
    cause: str | None
    source_refs: list[dict[str, Any]]
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    converted_to_certainty_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchLimitationInspectorView(_Model):
    limitation_view_id: str
    limitation_ref: dict[str, Any]
    limitation_summary: str
    limitation_type: str | None
    source_refs: list[dict[str, Any]]
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    treated_as_failure: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchReportInspectorView(_Model):
    report_inspector_view_id: str
    inspected_report_refs: list[dict[str, Any]]
    report_count: int
    report_types: list[str]
    summary: str
    warning_refs: list[dict[str, Any]]
    failure_refs: list[dict[str, Any]]
    blocked_refs: list[dict[str, Any]]
    report_status: str
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    raw_report_content_included: bool = False
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchEvidenceInspectorView(_Model):
    evidence_inspector_view_id: str
    panel_id: str | None
    source_view: WorkbenchEvidenceSourceView
    evidence_bundle_view: WorkbenchEvidenceBundleView | None
    claim_views: list[WorkbenchClaimInspectorView]
    claim_support_views: list[WorkbenchClaimSupportInspectorView]
    decision_evidence_views: list[WorkbenchDecisionEvidenceView]
    skill_selection_evidence_views: list[WorkbenchSkillSelectionEvidenceView]
    action_candidate_evidence_views: list[WorkbenchActionCandidateEvidenceView]
    route_selection_evidence_views: list[WorkbenchRouteSelectionEvidenceView]
    provider_selection_evidence_views: list[WorkbenchProviderSelectionEvidenceView]
    safety_rationale_views: list[WorkbenchSafetyRationaleView]
    pig_guidance_views: list[WorkbenchPIGGuidanceInspectorView]
    failure_cause_views: list[WorkbenchFailureCauseView]
    unsupported_claim_views: list[WorkbenchUnsupportedClaimView]
    uncertainty_views: list[WorkbenchUncertaintyInspectorView]
    limitation_views: list[WorkbenchLimitationInspectorView]
    report_inspector_view: WorkbenchReportInspectorView
    view_status: str
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    renders_ui_now: bool = False
    response_rewritten: bool = False
    provider_invoked: bool = False
    approval_executed: bool = False
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchEvidenceFilterPolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    filtering_enabled: bool = True
    filter_is_not_data_deletion: bool = True
    filter_is_not_access_control: bool = True
    raw_data_filter_dump_forbidden: bool = True
    ocel_visible: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchEvidenceFilterState(_Model):
    filter_state_id: str
    active_filters: list[dict[str, Any]]
    active_filter_count: int
    affected_claim_refs: list[dict[str, Any]]
    affected_evidence_refs: list[dict[str, Any]]
    hidden_claim_refs: list[dict[str, Any]]
    hidden_evidence_refs: list[dict[str, Any]]
    filter_status: str
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    data_deleted: bool = False
    access_policy_mutated: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchEvidenceSelectionView(_Model):
    selection_view_id: str
    selected_claim_refs: list[dict[str, Any]]
    selected_evidence_refs: list[dict[str, Any]]
    selected_report_refs: list[dict[str, Any]]
    selected_pig_guidance_refs: list[dict[str, Any]]
    selection_summary: str | None
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    selection_is_approval: bool = False
    selection_executes_now: bool = False
    raw_content_included: bool = False
    raw_secret_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchEvidenceInspectionPolicy(_Model):
    policy_id: str
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    inspection_enabled: bool = True
    inspection_is_read_only: bool = True
    summarize_refs_allowed: bool = True
    response_rewrite_forbidden: bool = True
    factuality_llm_judge_forbidden: bool = True
    raw_provider_output_inline_forbidden: bool = True
    raw_transcript_inline_forbidden: bool = True
    raw_secret_inline_forbidden: bool = True
    provider_invocation_forbidden: bool = True
    approval_execution_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchEvidenceInspectionSummary(_Model):
    inspection_summary_id: str
    evidence_inspector_view_id: str
    evidence_summary: list[dict[str, Any]]
    claim_summary: list[dict[str, Any]]
    unsupported_claim_summary: list[dict[str, Any]]
    decision_evidence_summary: list[dict[str, Any]]
    route_provider_evidence_summary: list[dict[str, Any]]
    safety_rationale_summary: list[dict[str, Any]]
    pig_guidance_summary: list[dict[str, Any]]
    failure_cause_summary: list[dict[str, Any]]
    uncertainty_summary: list[dict[str, Any]]
    limitation_summary: list[dict[str, Any]]
    human_intervention_summary: list[dict[str, Any]]
    summary_status: str
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    raw_provider_output_included: bool = False
    raw_transcript_included: bool = False
    raw_secret_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchEvidenceInspectorFinding(_Model):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class WorkbenchEvidenceInspectorReport(_Model):
    report_id: str
    created_at: str
    evidence_inspector_policy: WorkbenchEvidenceInspectorPolicy
    request: WorkbenchEvidenceInspectorRequest
    source_view: WorkbenchEvidenceSourceView
    evidence_inspector_view: WorkbenchEvidenceInspectorView
    filter_policy: WorkbenchEvidenceFilterPolicy
    filter_state: WorkbenchEvidenceFilterState
    selection_view: WorkbenchEvidenceSelectionView
    inspection_policy: WorkbenchEvidenceInspectionPolicy
    inspection_summary: WorkbenchEvidenceInspectionSummary
    findings: list[WorkbenchEvidenceInspectorFinding]
    report_status: str
    ready_for_v0_26_5: bool
    evidence_inspector_view_created: bool
    report_inspector_view_created: bool
    evidence_bundle_view_created: bool
    claim_views_created: bool
    claim_support_views_created: bool
    decision_evidence_views_created: bool
    skill_selection_evidence_views_created: bool
    action_candidate_evidence_views_created: bool
    route_selection_evidence_views_created: bool
    provider_selection_evidence_views_created: bool
    safety_rationale_views_created: bool
    pig_guidance_views_created: bool
    failure_cause_views_created: bool
    unsupported_claim_views_created: bool
    uncertainty_views_created: bool
    limitation_views_created: bool
    version: str = WORKBENCH_EVIDENCE_INSPECTOR_VERSION
    ready_for_v0_27: bool = False
    actual_ui_rendered: bool = False
    panel_rendered: bool = False
    response_rewritten: bool = False
    factuality_llm_judge_used: bool = False
    decision_mutated: bool = False
    safety_policy_mutated: bool = False
    provider_invoked: bool = False
    provider_test_run_performed: bool = False
    route_rerun_performed: bool = False
    stage_rerun_performed: bool = False
    approval_executed: bool = False
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
    pm4py_runtime_dependency_added: bool = False
    ocpa_runtime_dependency_added: bool = False
    pig_memory_promoted: bool = False
    pig_policy_mutated: bool = False
    pig_executed: bool = False
    schumpeter_split_introduced: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    raw_provider_output_inline: bool = False
    raw_transcript_persisted: bool = False
    llm_judge_used: bool = False
    next_required_step: str = WORKBENCH_EVIDENCE_INSPECTOR_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.26.5 Safety Gate / Approval Console begins or evidence inspector policy changes."


class WorkbenchEvidenceInspectorPrerequisiteSourceService:
    def __init__(
        self,
        view_state_available: bool = True,
        evidence_inspector_panel_available: bool = True,
        response_assembly_available: bool = True,
        evidence_bundle_available: bool = True,
        claim_support_available: bool = True,
        safety_gate_available: bool = True,
        routing_available: bool = True,
        provider_invocation_available: bool = True,
        intent_available: bool = True,
        provider_browser_available: bool = True,
        trace_explorer_available: bool = True,
        pig_guidance_available: bool = True,
        failure_cause_available: bool = True,
    ) -> None:
        self.view_state_available = view_state_available
        self.evidence_inspector_panel_available = evidence_inspector_panel_available
        self.response_assembly_available = response_assembly_available
        self.evidence_bundle_available = evidence_bundle_available
        self.claim_support_available = claim_support_available
        self.safety_gate_available = safety_gate_available
        self.routing_available = routing_available
        self.provider_invocation_available = provider_invocation_available
        self.intent_available = intent_available
        self.provider_browser_available = provider_browser_available
        self.trace_explorer_available = trace_explorer_available
        self.pig_guidance_available = pig_guidance_available
        self.failure_cause_available = failure_cause_available

    def load_workbench_view_state(self) -> WorkbenchViewState | None:
        if not self.view_state_available:
            return None
        return WorkbenchViewStateReportService().build_all_parts()["view_state"]

    def load_evidence_inspector_panel_model(self) -> WorkbenchPanel | None:
        view_state = self.load_workbench_view_state()
        if not view_state or not self.evidence_inspector_panel_available:
            return None
        return next((panel for panel in view_state.panel_registry_view.panels if panel.panel_type == "evidence_inspector"), None)

    def load_response_assembly_report_if_available(self) -> dict[str, Any] | None:
        if not self.response_assembly_available:
            return None
        parts = AgentResponseAssemblyReportService().build_all_parts()
        if not self.evidence_bundle_available:
            parts["evidence_bundle"] = None
            parts["evidence_items"] = []
        if not self.claim_support_available and parts.get("answer_draft"):
            parts["answer_draft"].claim_supports = []
        return parts

    def load_safety_gate_report_if_available(self) -> dict[str, Any] | None:
        return AgentSafetyGateReportService().build_all_parts() if self.safety_gate_available else None

    def load_routing_report_if_available(self) -> dict[str, Any] | None:
        return AgentToolRoutingReportService().build_all_parts() if self.routing_available else None

    def load_provider_invocation_report_refs_if_available(self) -> dict[str, Any] | None:
        return AgentProviderInvocationReportService().build_all_parts() if self.provider_invocation_available else None

    def load_intent_report_if_available(self) -> dict[str, Any] | None:
        return AgentIntentClassificationReportService().build_all_parts() if self.intent_available else None

    def load_provider_browser_report_if_available(self) -> dict[str, Any] | None:
        return WorkbenchProviderBrowserReportService().build_all_parts() if self.provider_browser_available else None

    def load_trace_explorer_report_if_available(self) -> dict[str, Any] | None:
        return WorkbenchTraceExplorerReportService().build_all_parts() if self.trace_explorer_available else None

    def load_sources(self) -> dict[str, Any]:
        response = self.load_response_assembly_report_if_available()
        provider_browser = self.load_provider_browser_report_if_available()
        pig_refs: list[dict[str, Any]] = []
        failure_refs: list[dict[str, Any]] = []
        human_refs: list[dict[str, Any]] = []
        if provider_browser:
            pig_refs = [
                _model_ref("workbench_provider_pig_guidance_view", item)
                for item in provider_browser.get("pig_guidance_views", [])
            ] if self.pig_guidance_available else []
            failure_refs = [
                _model_ref("workbench_provider_failure_mode_view", item)
                for item in provider_browser.get("failure_mode_views", [])
            ] if self.failure_cause_available else []
            human_refs = [
                _model_ref("workbench_human_intervention_point_ref", item)
                for item in provider_browser.get("human_intervention_points", [])
            ]
        return {
            "view_state": self.load_workbench_view_state(),
            "panel": self.load_evidence_inspector_panel_model(),
            "response_assembly": response,
            "safety_gate": self.load_safety_gate_report_if_available(),
            "routing": self.load_routing_report_if_available(),
            "provider_invocation": self.load_provider_invocation_report_refs_if_available(),
            "intent": self.load_intent_report_if_available(),
            "provider_browser": provider_browser,
            "trace_explorer": self.load_trace_explorer_report_if_available(),
            "pig_guidance_refs": pig_refs,
            "failure_cause_refs": failure_refs,
            "human_intervention_refs": human_refs,
        }


class WorkbenchEvidenceInspectorPolicyService:
    def build_policy(self) -> WorkbenchEvidenceInspectorPolicy:
        return WorkbenchEvidenceInspectorPolicy(policy_id="workbench_evidence_inspector_policy:v0.26.4")


class WorkbenchEvidenceInspectorRequestService:
    def build_request(self, sources: dict[str, Any], strictness: str = "standard") -> WorkbenchEvidenceInspectorRequest:
        response = sources.get("response_assembly") or {}
        report = response.get("report")
        bundle = response.get("evidence_bundle")
        draft = response.get("answer_draft")
        claims = list(getattr(draft, "claims", []))
        view_state = sources.get("view_state")
        panel = sources.get("panel")
        provider_invocation = sources.get("provider_invocation") or {}
        routing = sources.get("routing") or {}
        safety = sources.get("safety_gate") or {}
        intent = sources.get("intent") or {}
        provider_browser = sources.get("provider_browser") or {}
        trace = sources.get("trace_explorer") or {}
        evidence_item = (response.get("evidence_items") or [None])[0]
        return WorkbenchEvidenceInspectorRequest(
            request_id="workbench_evidence_inspector_request:v0.26.4",
            view_state_report_id="workbench_view_state_report:v0.26.1" if view_state else None,
            view_state_id=getattr(view_state, "view_state_id", None),
            evidence_inspector_panel_id=getattr(panel, "panel_id", None),
            response_assembly_report_id=getattr(report, "report_id", None),
            evidence_bundle_id=getattr(bundle, "evidence_bundle_id", None),
            claim_ids=[claim.claim_id for claim in claims],
            provider_invocation_report_id=getattr(provider_invocation.get("report"), "report_id", None),
            routing_report_id=getattr(routing.get("report"), "report_id", None),
            safety_gate_report_id=getattr(safety.get("report"), "report_id", None),
            intent_report_id=getattr(intent.get("report"), "report_id", None),
            provider_browser_report_id=getattr(provider_browser.get("report"), "report_id", None),
            trace_explorer_report_id=getattr(trace.get("report"), "report_id", None),
            pig_guidance_refs=sources.get("pig_guidance_refs", []),
            focus_claim_ref=_model_ref("agent_claim", claims[0]) if claims else None,
            focus_evidence_ref=_model_ref("agent_evidence_item", evidence_item) if evidence_item else None,
            filter_refs=[_ref("workbench_evidence_filter", "filter:all_evidence")],
            source_refs=[
                _model_ref("agent_response_assembly_report", report) if report else _ref("agent_response_assembly_report", None),
                _model_ref("workbench_panel", panel) if panel else _ref("workbench_panel", None),
            ],
            strictness=strictness,
        )


class WorkbenchEvidenceSourceViewService:
    def build_source_view(self, sources: dict[str, Any]) -> WorkbenchEvidenceSourceView:
        response = sources.get("response_assembly") or {}
        report = response.get("report")
        bundle = response.get("evidence_bundle")
        draft = response.get("answer_draft")
        provider_invocation = sources.get("provider_invocation") or {}
        routing = sources.get("routing") or {}
        safety = sources.get("safety_gate") or {}
        claims = list(getattr(draft, "claims", []))
        supports = list(getattr(draft, "claim_supports", []))
        uncertainties = list(getattr(draft, "uncertainty_notes", []))
        limitations = list(getattr(draft, "limitation_notes", []))
        provider_result_refs = [
            _model_ref("agent_provider_result_ref", item)
            for item in getattr(provider_invocation.get("result_bundle"), "result_refs", [])
        ]
        provider_selection_refs = []
        if routing.get("selection"):
            provider_selection_refs.append(_model_ref("agent_provider_selection", routing["selection"]))
        source_status = "complete" if report and bundle and claims and supports else "partial" if any([report, bundle, claims, safety, routing]) else "missing"
        return WorkbenchEvidenceSourceView(
            source_view_id="workbench_evidence_source_view:v0.26.4",
            response_assembly_report_ref=_model_ref("agent_response_assembly_report", report) if report else None,
            evidence_bundle_ref=_model_ref("agent_evidence_bundle", bundle) if bundle else None,
            claim_refs=[_model_ref("agent_claim", claim) for claim in claims],
            claim_support_refs=[_model_ref("agent_claim_support", support) for support in supports],
            uncertainty_refs=[_model_ref("agent_uncertainty_note", item) for item in uncertainties],
            limitation_refs=[_model_ref("agent_limitation_note", item) for item in limitations],
            safety_gate_refs=[_model_ref("agent_safety_gate_report", safety.get("report"))] if safety.get("report") else [],
            routing_refs=[_model_ref("agent_tool_routing_report", routing.get("report"))] if routing.get("report") else [],
            provider_selection_refs=provider_selection_refs,
            provider_result_refs=provider_result_refs,
            pig_guidance_refs=sources.get("pig_guidance_refs", []),
            failure_cause_refs=sources.get("failure_cause_refs", []),
            human_intervention_refs=sources.get("human_intervention_refs", []),
            source_status=source_status,
            evidence_refs=[_ref("workbench_view_state", getattr(sources.get("view_state"), "view_state_id", None), "v0.26.1")],
        )


class WorkbenchEvidenceItemViewService:
    def build_evidence_item_views(self, evidence_items: list[Any], claims: list[Any] | None = None) -> list[WorkbenchEvidenceItemView]:
        views: list[WorkbenchEvidenceItemView] = []
        claims = claims or []
        for item in evidence_items:
            source_ref = item.source_ref.to_dict() if hasattr(item.source_ref, "to_dict") else asdict(item.source_ref)
            support_ids = item.supports_claim_ids or [
                claim.claim_id for claim in claims if item.evidence_item_id in getattr(claim, "evidence_item_ids", [])
            ] or [claim.claim_id for claim in claims if getattr(claim, "requires_evidence", False)]
            views.append(
                WorkbenchEvidenceItemView(
                    evidence_item_view_id=f"workbench_evidence_item_view:{item.evidence_item_id}",
                    evidence_item_ref=_model_ref("agent_evidence_item", item),
                    evidence_kind=item.evidence_kind,
                    source_ref=source_ref,
                    sanitized_summary=item.summary,
                    supports_claim_refs=[_ref("agent_claim", claim_id, "v0.25.6") for claim_id in support_ids],
                    confidence=item.confidence,
                    evidence_refs=[_model_ref("agent_evidence_item", item)],
                )
            )
        return views


class WorkbenchEvidenceBundleViewService:
    def build_evidence_bundle_view(self, bundle: Any | None, item_views: list[WorkbenchEvidenceItemView], unsupported_count: int) -> WorkbenchEvidenceBundleView | None:
        if bundle is None:
            return None
        return WorkbenchEvidenceBundleView(
            evidence_bundle_view_id=f"workbench_evidence_bundle_view:{bundle.evidence_bundle_id}",
            evidence_bundle_ref=_model_ref("agent_evidence_bundle", bundle),
            evidence_item_views=item_views,
            evidence_count=bundle.evidence_count,
            provider_evidence_count=bundle.provider_evidence_count,
            policy_evidence_count=bundle.policy_evidence_count,
            uncertainty_evidence_count=bundle.uncertainty_evidence_count,
            unsupported_evidence_count=unsupported_count,
            bundle_status=bundle.bundle_status,
            evidence_refs=[_model_ref("agent_evidence_bundle", bundle)],
        )


class WorkbenchClaimInspectorViewService:
    def build_claim_views(self, claims: list[Any], supports: list[Any]) -> list[WorkbenchClaimInspectorView]:
        support_by_claim = {support.claim_id: support for support in supports}
        views: list[WorkbenchClaimInspectorView] = []
        for claim in claims:
            support = support_by_claim.get(claim.claim_id)
            status = getattr(support, "support_status", "unknown")
            views.append(
                WorkbenchClaimInspectorView(
                    claim_view_id=f"workbench_claim_inspector_view:{claim.claim_id}",
                    claim_ref=_model_ref("agent_claim", claim),
                    claim_type=claim.claim_type,
                    sanitized_claim_text=claim.text,
                    confidence=claim.confidence,
                    requires_evidence=claim.requires_evidence,
                    evidence_item_refs=[_ref("agent_evidence_item", item_id, "v0.25.6") for item_id in claim.evidence_item_ids],
                    support_status=status,
                    unsupported=claim.unsupported or status == "unsupported",
                    inference_label_required=claim.claim_type in {"inference", "interpretation"},
                    provider_observation_label_required=claim.claim_type == "provider_observation",
                    evidence_refs=[_model_ref("agent_claim", claim)],
                )
            )
        return views


class WorkbenchClaimSupportInspectorViewService:
    def build_claim_support_views(self, supports: list[Any]) -> list[WorkbenchClaimSupportInspectorView]:
        return [
            WorkbenchClaimSupportInspectorView(
                support_view_id=f"workbench_claim_support_inspector_view:{support.support_id}",
                claim_ref=_ref("agent_claim", support.claim_id, "v0.25.6"),
                support_ref=_model_ref("agent_claim_support", support),
                evidence_item_refs=[_ref("agent_evidence_item", item_id, "v0.25.6") for item_id in support.evidence_item_ids],
                support_status=support.support_status,
                missing_evidence_reason=support.missing_evidence_reason,
                support_summary=f"Claim support is {support.support_status}; raw evidence content is not inlined.",
                evidence_refs=[_model_ref("agent_claim_support", support)],
            )
            for support in supports
        ]


class WorkbenchReportInspectorViewService:
    def build_report_inspector_view(self, sources: dict[str, Any]) -> WorkbenchReportInspectorView:
        pairs = [
            ("agent_response_assembly_report", (sources.get("response_assembly") or {}).get("report")),
            ("agent_provider_invocation_report", (sources.get("provider_invocation") or {}).get("report")),
            ("agent_tool_routing_report", (sources.get("routing") or {}).get("report")),
            ("agent_safety_gate_report", (sources.get("safety_gate") or {}).get("report")),
            ("workbench_provider_browser_report", (sources.get("provider_browser") or {}).get("report")),
            ("workbench_trace_explorer_report", (sources.get("trace_explorer") or {}).get("report")),
        ]
        refs = [_model_ref(kind, value) for kind, value in pairs if value]
        warning_refs = [_model_ref(kind, value) for kind, value in pairs if value and getattr(value, "report_status", None) == "warning"]
        failure_refs = [_model_ref(kind, value) for kind, value in pairs if value and getattr(value, "report_status", None) == "failed"]
        blocked_refs = [_model_ref(kind, value) for kind, value in pairs if value and getattr(value, "report_status", None) == "blocked"]
        status = "blocked" if blocked_refs else "failed" if failure_refs else "warning" if warning_refs else "ready" if refs else "partial"
        return WorkbenchReportInspectorView(
            report_inspector_view_id="workbench_report_inspector_view:v0.26.4",
            inspected_report_refs=refs,
            report_count=len(refs),
            report_types=[ref["type"] for ref in refs],
            summary="Refs-only report inspection view; raw report/provider/transcript content is not inlined.",
            warning_refs=warning_refs,
            failure_refs=failure_refs,
            blocked_refs=blocked_refs,
            report_status=status,
            evidence_refs=refs,
        )


class WorkbenchDecisionEvidenceViewService:
    def build_decision_evidence_views(self, sources: dict[str, Any], item_refs: list[dict[str, Any]]) -> list[WorkbenchDecisionEvidenceView]:
        safety = sources.get("safety_gate") or {}
        routing = sources.get("routing") or {}
        intent = sources.get("intent") or {}
        response = sources.get("response_assembly") or {}
        provider_browser = sources.get("provider_browser") or {}
        decision_specs = [
            ("intent_classification", intent.get("report"), getattr(intent.get("intent"), "intent_category", None)),
            ("safety_gate", safety.get("decision"), getattr(safety.get("decision"), "primary_outcome", None)),
            ("route_selection", routing.get("route_plan"), getattr(routing.get("route_plan"), "route_plan_status", None)),
            ("provider_selection", routing.get("selection"), getattr(routing.get("selection"), "selection_status", None)),
            ("response_assembly", response.get("report"), getattr(response.get("report"), "report_status", None)),
        ]
        views: list[WorkbenchDecisionEvidenceView] = []
        for decision_type, decision, outcome in decision_specs:
            if not decision:
                continue
            views.append(
                WorkbenchDecisionEvidenceView(
                    decision_evidence_view_id=f"workbench_decision_evidence_view:{decision_type}",
                    decision_type=decision_type,
                    decision_ref=_model_ref(decision_type, decision),
                    rationale_refs=[_model_ref("workbench_provider_browser_report", provider_browser.get("report"))] if provider_browser.get("report") else [],
                    evidence_item_refs=item_refs,
                    pig_guidance_refs=sources.get("pig_guidance_refs", []),
                    safety_finding_refs=[_model_ref("agent_safety_gate_finding", item) for item in safety.get("findings", [])],
                    decision_outcome=outcome,
                    evidence_refs=item_refs,
                )
            )
        return views


class WorkbenchSkillSelectionEvidenceViewService:
    def build_skill_selection_evidence_views(self, sources: dict[str, Any]) -> list[WorkbenchSkillSelectionEvidenceView]:
        return [
            WorkbenchSkillSelectionEvidenceView(
                skill_selection_evidence_view_id="workbench_skill_selection_evidence_view:workbench_evidence_inspector_view",
                skill_id="skill:workbench_evidence_inspector_view",
                skill_name="workbench_evidence_inspector_view",
                candidate_ref=_ref("workbench_skill_candidate", "skill:workbench_evidence_inspector_view"),
                selection_ref=_ref("workbench_skill_selection", "skill:workbench_evidence_inspector_view"),
                selection_reason_refs=[_ref("workbench_track", "workspace_agent_workbench:v0.26")],
                safety_finding_refs=[],
                pig_guidance_refs=sources.get("pig_guidance_refs", []),
                selected=True,
                rejected=False,
                deferred=False,
            )
        ]


class WorkbenchActionCandidateEvidenceViewService:
    def build_action_candidate_evidence_views(self, sources: dict[str, Any]) -> list[WorkbenchActionCandidateEvidenceView]:
        human_refs = sources.get("human_intervention_refs", [])
        return [
            WorkbenchActionCandidateEvidenceView(
                action_candidate_evidence_view_id="workbench_action_candidate_evidence_view:evidence_bound_inspection",
                action_candidate_ref=_ref("workbench_action_candidate", "evidence_bound_inspection_only"),
                action_type="inspection_only",
                rationale_refs=[_ref("workbench_policy", "evidence_report_inspector_view_only")],
                risk_refs=sources.get("failure_cause_refs", []),
                approval_requirement_refs=human_refs,
                pig_guidance_refs=sources.get("pig_guidance_refs", []),
                evidence_bound=True,
            )
        ]


class WorkbenchRouteSelectionEvidenceViewService:
    def build_route_selection_evidence_views(self, sources: dict[str, Any]) -> list[WorkbenchRouteSelectionEvidenceView]:
        routing = sources.get("routing") or {}
        route_plan = routing.get("route_plan")
        if not route_plan:
            return []
        return [
            WorkbenchRouteSelectionEvidenceView(
                route_selection_evidence_view_id="workbench_route_selection_evidence_view:route_plan",
                route_ref=_model_ref("agent_tool_route_plan", route_plan),
                route_kind=getattr(route_plan, "route_kind", getattr(route_plan, "recommended_route_kind", None)),
                selection_rationale_refs=[_model_ref("agent_tool_routing_report", routing.get("report"))],
                route_compatibility_refs=[_ref("workbench_route_compatibility_matrix", "workbench_route_compatibility_matrix:v0.26.3", "v0.26.3")],
                safety_context_refs=[_ref("agent_safety_gate_report", getattr(route_plan, "safety_gate_report_id", None), "v0.25.3")],
                pig_guidance_refs=sources.get("pig_guidance_refs", []),
                human_intervention_refs=sources.get("human_intervention_refs", []),
            )
        ]


class WorkbenchProviderSelectionEvidenceViewService:
    def build_provider_selection_evidence_views(self, sources: dict[str, Any]) -> list[WorkbenchProviderSelectionEvidenceView]:
        provider_browser = sources.get("provider_browser") or {}
        rationale_views = provider_browser.get("selection_rationale_views", [])
        readiness_views = provider_browser.get("readiness_views", [])
        risk_views = provider_browser.get("boundary_risk_views", [])
        if not rationale_views:
            return []
        views: list[WorkbenchProviderSelectionEvidenceView] = []
        for item in rationale_views:
            views.append(
                WorkbenchProviderSelectionEvidenceView(
                    provider_selection_evidence_view_id=f"workbench_provider_selection_evidence_view:{item.rationale_view_id}",
                    provider_id=item.provider_id,
                    capability_id=item.capability_id,
                    provider_selection_ref=item.source_selection_ref,
                    provider_rationale_refs=[_model_ref("workbench_provider_selection_rationale_view", item)],
                    boundary_risk_refs=[_model_ref("workbench_provider_boundary_risk_view", risk) for risk in risk_views if risk.provider_id == item.provider_id],
                    readiness_refs=[_model_ref("workbench_capability_readiness_view", ready) for ready in readiness_views if ready.provider_id == item.provider_id],
                    pig_guidance_refs=item.pig_guidance_refs,
                )
            )
        return views


class WorkbenchSafetyRationaleViewService:
    def build_safety_rationale_views(self, sources: dict[str, Any]) -> list[WorkbenchSafetyRationaleView]:
        safety = sources.get("safety_gate") or {}
        report = safety.get("report")
        decision = safety.get("decision")
        if not report:
            return []
        return [
            WorkbenchSafetyRationaleView(
                safety_rationale_view_id=f"workbench_safety_rationale_view:{report.report_id}",
                safety_gate_report_ref=_model_ref("agent_safety_gate_report", report),
                gate_outcome=getattr(decision, "primary_outcome", None),
                safety_rule_refs=[_model_ref("agent_safety_rule_result", item) for item in safety.get("rule_results", [])],
                risk_preview_refs=[_model_ref("agent_task_risk_preview", getattr(report, "request", None))],
                blocked_reason_refs=[_model_ref("agent_blocked_decision", safety.get("blocked"))] if safety.get("blocked") else [],
                no_action_rationale_refs=[_model_ref("agent_no_action_decision", safety.get("no_action"))] if safety.get("no_action") else [],
                clarification_requirement_refs=[_model_ref("agent_clarification_decision", safety.get("clarification"))] if safety.get("clarification") else [],
                deferred_reason_refs=[_model_ref("agent_deferred_decision", safety.get("deferred"))] if safety.get("deferred") else [],
                evidence_refs=[_model_ref("agent_safety_gate_report", report)],
            )
        ]


class WorkbenchPIGGuidanceInspectorViewService:
    def build_pig_guidance_views(self, sources: dict[str, Any]) -> list[WorkbenchPIGGuidanceInspectorView]:
        refs = sources.get("pig_guidance_refs", [])
        if not refs:
            return []
        return [
            WorkbenchPIGGuidanceInspectorView(
                pig_guidance_inspector_view_id=f"workbench_pig_guidance_inspector_view:{index}",
                source_pig_ref=ref,
                guidance_type="rationale",
                guidance_summary="PIG guidance is represented as an inspection reference only; it is not memory, policy mutation, or execution.",
                related_decision_refs=[],
                related_route_refs=[_ref("agent_tool_route_plan", "route_plan_ref:v0.25.4", "v0.25.4")],
                related_provider_refs=[_ref("workbench_provider_browser_report", "workbench_provider_browser_report:v0.26.3", "v0.26.3")],
                related_evidence_refs=[],
                evidence_refs=[ref],
            )
            for index, ref in enumerate(refs)
        ]


class WorkbenchFailureCauseViewService:
    def build_failure_cause_views(self, sources: dict[str, Any]) -> list[WorkbenchFailureCauseView]:
        refs = sources.get("failure_cause_refs", [])
        response = sources.get("response_assembly") or {}
        findings = response.get("findings", [])
        views = [
            WorkbenchFailureCauseView(
                failure_cause_view_id=f"workbench_failure_cause_view:{index}",
                failure_ref=ref,
                failure_stage="provider_browser",
                failure_category="provider_warning",
                failure_summary="Prior provider browser failure mode is visible as a refs-only inspection object.",
                source_report_refs=[_ref("workbench_provider_browser_report", "workbench_provider_browser_report:v0.26.3", "v0.26.3")],
                recovery_guidance_refs=[],
                evidence_refs=[ref],
            )
            for index, ref in enumerate(refs)
        ]
        for finding in findings:
            if getattr(finding, "severity", None) in {"warning", "error", "critical"}:
                views.append(
                    WorkbenchFailureCauseView(
                        failure_cause_view_id=f"workbench_failure_cause_view:{finding.finding_id}",
                        failure_ref=_model_ref("agent_response_assembly_finding", finding),
                        failure_stage="response_assembly",
                        failure_category="evidence_missing" if "evidence" in finding.finding_type else "unknown",
                        failure_summary=finding.message,
                        source_report_refs=[_model_ref("agent_response_assembly_report", response.get("report"))],
                        recovery_guidance_refs=[],
                        evidence_refs=[_model_ref("agent_response_assembly_finding", finding)],
                    )
                )
        return views


class WorkbenchUnsupportedClaimViewService:
    def build_unsupported_claim_views(
        self,
        claim_views: list[WorkbenchClaimInspectorView],
        support_views: list[WorkbenchClaimSupportInspectorView],
    ) -> list[WorkbenchUnsupportedClaimView]:
        reason_by_claim = {view.claim_ref["id"]: view.missing_evidence_reason for view in support_views}
        targets = [view for view in claim_views if view.unsupported or view.support_status in {"unsupported", "weakly_supported"}]
        if not targets and claim_views:
            targets = [claim_views[0]]
        return [
            WorkbenchUnsupportedClaimView(
                unsupported_claim_view_id=f"workbench_unsupported_claim_view:{view.claim_ref['id']}",
                claim_ref=view.claim_ref,
                missing_evidence_reason=reason_by_claim.get(view.claim_ref["id"]),
                unsupported_severity="warning" if view.unsupported else "info",
                suggested_next_surface="v0.26.5 approval console" if view.unsupported else "none",
                evidence_refs=view.evidence_item_refs,
            )
            for view in targets
        ]


class WorkbenchUncertaintyInspectorViewService:
    def build_uncertainty_views(self, uncertainties: list[Any]) -> list[WorkbenchUncertaintyInspectorView]:
        if not uncertainties:
            return [
                WorkbenchUncertaintyInspectorView(
                    uncertainty_view_id="workbench_uncertainty_inspector_view:no_explicit_uncertainty_ref",
                    uncertainty_ref=_ref("agent_uncertainty_note", "no_explicit_uncertainty_ref", "v0.25.6"),
                    uncertainty_summary="No explicit uncertainty note ref is available; the inspector does not convert this into certainty.",
                    affected_claim_refs=[],
                    cause="no_explicit_uncertainty_ref",
                    source_refs=[],
                )
            ]
        return [
            WorkbenchUncertaintyInspectorView(
                uncertainty_view_id=f"workbench_uncertainty_inspector_view:{item.uncertainty_id}",
                uncertainty_ref=_model_ref("agent_uncertainty_note", item),
                uncertainty_summary=item.message,
                affected_claim_refs=[_ref("agent_claim", claim_id, "v0.25.6") for claim_id in item.affected_claim_ids],
                cause=item.cause,
                source_refs=item.evidence_refs,
                evidence_refs=item.evidence_refs,
            )
            for item in uncertainties
        ]


class WorkbenchLimitationInspectorViewService:
    def build_limitation_views(self, limitations: list[Any]) -> list[WorkbenchLimitationInspectorView]:
        return [
            WorkbenchLimitationInspectorView(
                limitation_view_id=f"workbench_limitation_inspector_view:{item.limitation_id}",
                limitation_ref=_model_ref("agent_limitation_note", item),
                limitation_summary=item.message,
                limitation_type=item.limitation_type,
                source_refs=item.evidence_refs,
                evidence_refs=item.evidence_refs,
            )
            for item in limitations
        ]


class WorkbenchEvidenceFilterService:
    def build_policy(self) -> WorkbenchEvidenceFilterPolicy:
        return WorkbenchEvidenceFilterPolicy(policy_id="workbench_evidence_filter_policy:v0.26.4")

    def build_filter_state(self, request: WorkbenchEvidenceInspectorRequest) -> WorkbenchEvidenceFilterState:
        return WorkbenchEvidenceFilterState(
            filter_state_id="workbench_evidence_filter_state:v0.26.4",
            active_filters=request.filter_refs,
            active_filter_count=len(request.filter_refs),
            affected_claim_refs=[],
            affected_evidence_refs=[],
            hidden_claim_refs=[],
            hidden_evidence_refs=[],
            filter_status="ready" if request.filter_refs else "empty",
            evidence_refs=request.filter_refs,
        )


class WorkbenchEvidenceSelectionViewService:
    def build_selection_view(self, request: WorkbenchEvidenceInspectorRequest) -> WorkbenchEvidenceSelectionView:
        return WorkbenchEvidenceSelectionView(
            selection_view_id="workbench_evidence_selection_view:v0.26.4",
            selected_claim_refs=[request.focus_claim_ref] if request.focus_claim_ref else [],
            selected_evidence_refs=[request.focus_evidence_ref] if request.focus_evidence_ref else [],
            selected_report_refs=[
                _ref("agent_response_assembly_report", request.response_assembly_report_id, "v0.25.6")
            ] if request.response_assembly_report_id else [],
            selected_pig_guidance_refs=request.pig_guidance_refs,
            selection_summary="Selection is inspection-only and does not approve or execute.",
        )


class WorkbenchEvidenceInspectionSummaryService:
    def build_summary(self, view: WorkbenchEvidenceInspectorView) -> WorkbenchEvidenceInspectionSummary:
        bundle = view.evidence_bundle_view
        return WorkbenchEvidenceInspectionSummary(
            inspection_summary_id="workbench_evidence_inspection_summary:v0.26.4",
            evidence_inspector_view_id=view.evidence_inspector_view_id,
            evidence_summary=[{"evidence_count": bundle.evidence_count if bundle else 0, "bundle_status": bundle.bundle_status if bundle else "missing"}],
            claim_summary=[{"claim_ref": item.claim_ref, "support_status": item.support_status} for item in view.claim_views],
            unsupported_claim_summary=[{"claim_ref": item.claim_ref, "severity": item.unsupported_severity} for item in view.unsupported_claim_views],
            decision_evidence_summary=[{"decision_type": item.decision_type, "decision_outcome": item.decision_outcome} for item in view.decision_evidence_views],
            route_provider_evidence_summary=[
                {"route_ref": item.route_ref, "route_rerun_now": item.route_rerun_now} for item in view.route_selection_evidence_views
            ] + [
                {"provider_id": item.provider_id, "provider_invoked_now": item.provider_invoked_now}
                for item in view.provider_selection_evidence_views
            ],
            safety_rationale_summary=[{"gate_outcome": item.gate_outcome, "policy_mutated": item.safety_policy_mutated_now} for item in view.safety_rationale_views],
            pig_guidance_summary=[{"guidance_type": item.guidance_type, "executes": item.pig_guidance_executes} for item in view.pig_guidance_views],
            failure_cause_summary=[{"failure_category": item.failure_category, "auto_repair": item.automatic_repair_enabled} for item in view.failure_cause_views],
            uncertainty_summary=[{"cause": item.cause, "converted": item.converted_to_certainty_now} for item in view.uncertainty_views],
            limitation_summary=[{"limitation_type": item.limitation_type, "failure": item.treated_as_failure} for item in view.limitation_views],
            human_intervention_summary=[{"approval_executed": view.approval_executed}],
            summary_status=view.view_status,
            evidence_refs=view.evidence_refs,
        )


class WorkbenchEvidenceInspectionPolicyService:
    def build_policy(self) -> WorkbenchEvidenceInspectionPolicy:
        return WorkbenchEvidenceInspectionPolicy(policy_id="workbench_evidence_inspection_policy:v0.26.4")


class WorkbenchEvidenceInspectorViewService:
    def build_view(
        self,
        request: WorkbenchEvidenceInspectorRequest,
        source_view: WorkbenchEvidenceSourceView,
        report_view: WorkbenchReportInspectorView,
        evidence_bundle_view: WorkbenchEvidenceBundleView | None,
        claim_views: list[WorkbenchClaimInspectorView],
        claim_support_views: list[WorkbenchClaimSupportInspectorView],
        decision_evidence_views: list[WorkbenchDecisionEvidenceView],
        skill_selection_evidence_views: list[WorkbenchSkillSelectionEvidenceView],
        action_candidate_evidence_views: list[WorkbenchActionCandidateEvidenceView],
        route_selection_evidence_views: list[WorkbenchRouteSelectionEvidenceView],
        provider_selection_evidence_views: list[WorkbenchProviderSelectionEvidenceView],
        safety_rationale_views: list[WorkbenchSafetyRationaleView],
        pig_guidance_views: list[WorkbenchPIGGuidanceInspectorView],
        failure_cause_views: list[WorkbenchFailureCauseView],
        unsupported_claim_views: list[WorkbenchUnsupportedClaimView],
        uncertainty_views: list[WorkbenchUncertaintyInspectorView],
        limitation_views: list[WorkbenchLimitationInspectorView],
    ) -> WorkbenchEvidenceInspectorView:
        status = "ready" if source_view.source_status == "complete" else "partial"
        if report_view.report_status in {"failed", "blocked"}:
            status = report_view.report_status
        elif unsupported_claim_views or uncertainty_views or limitation_views:
            status = "warning"
        return WorkbenchEvidenceInspectorView(
            evidence_inspector_view_id="workbench_evidence_inspector_view:v0.26.4",
            panel_id=request.evidence_inspector_panel_id,
            source_view=source_view,
            evidence_bundle_view=evidence_bundle_view,
            claim_views=claim_views,
            claim_support_views=claim_support_views,
            decision_evidence_views=decision_evidence_views,
            skill_selection_evidence_views=skill_selection_evidence_views,
            action_candidate_evidence_views=action_candidate_evidence_views,
            route_selection_evidence_views=route_selection_evidence_views,
            provider_selection_evidence_views=provider_selection_evidence_views,
            safety_rationale_views=safety_rationale_views,
            pig_guidance_views=pig_guidance_views,
            failure_cause_views=failure_cause_views,
            unsupported_claim_views=unsupported_claim_views,
            uncertainty_views=uncertainty_views,
            limitation_views=limitation_views,
            report_inspector_view=report_view,
            view_status=status,
            evidence_refs=source_view.evidence_refs,
        )


class WorkbenchEvidenceInspectorFindingService:
    BLOCKED_FINDINGS = {
        "raw_provider_output_inline_attempted",
        "raw_transcript_inline_attempted",
        "raw_secret_inline_attempted",
        "response_rewrite_attempted",
        "factuality_llm_judge_detected",
        "safety_llm_judge_detected",
        "decision_mutation_attempted",
        "safety_policy_mutation_attempted",
        "pig_guidance_as_memory_detected",
        "pig_policy_mutation_detected",
        "pig_execution_detected",
        "provider_invocation_attempted",
        "route_rerun_attempted",
        "stage_rerun_attempted",
        "approval_execution_attempted",
        "ask_execution_attempted",
        "final_response_emission_attempted",
        "local_command_execution_attempted",
        "direct_file_access_attempted",
        "direct_subprocess_attempted",
        "command_rerun_attempted",
        "automatic_repair_attempted",
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

    def build_findings(
        self,
        sources: dict[str, Any],
        view: WorkbenchEvidenceInspectorView,
        strictness: str = "standard",
        attempt_flags: dict[str, bool] | None = None,
        extra_findings: list[str] | None = None,
    ) -> list[WorkbenchEvidenceInspectorFinding]:
        findings: list[WorkbenchEvidenceInspectorFinding] = []
        if not sources.get("view_state"):
            findings.append(self._finding("warning", "missing_workbench_view_state", "Workbench view state is unavailable."))
        if not sources.get("panel"):
            findings.append(self._finding("warning", "missing_evidence_inspector_panel", "Evidence inspector panel model is unavailable."))
        if not sources.get("response_assembly"):
            findings.append(self._finding("error" if strictness == "strict" else "warning", "missing_response_assembly_report", "Response assembly source is unavailable."))
        if view.evidence_bundle_view is None:
            findings.append(self._finding("error" if strictness == "strict" else "warning", "missing_evidence_bundle", "Evidence bundle source is unavailable."))
        if not view.claim_support_views:
            findings.append(self._finding("warning", "missing_claim_support", "Claim support source is unavailable."))
        if not sources.get("safety_gate"):
            findings.append(self._finding("warning", "missing_safety_gate_report", "Safety gate source is unavailable."))
        if not sources.get("routing"):
            findings.append(self._finding("warning", "missing_route_report", "Routing source is unavailable."))
        if not view.provider_selection_evidence_views:
            findings.append(self._finding("warning", "missing_provider_selection_report", "Provider selection source is unavailable."))
        if not sources.get("pig_guidance_refs"):
            findings.append(self._finding("warning", "missing_pig_guidance_refs", "PIG guidance refs are unavailable."))
        created = [
            "evidence_bundle_view_created",
            "claim_view_created",
            "claim_support_view_created",
            "decision_evidence_view_created",
            "skill_selection_evidence_view_created",
            "action_candidate_evidence_view_created",
            "route_selection_evidence_view_created",
            "provider_selection_evidence_view_created",
            "safety_rationale_view_created",
            "pig_guidance_inspector_view_created",
            "failure_cause_view_created",
            "unsupported_claim_view_created",
            "uncertainty_view_created",
            "limitation_view_created",
            "human_intervention_ref_attached",
        ]
        for finding_type in created:
            findings.append(self._finding("info", finding_type, f"{finding_type} was created or evaluated as a refs-only view artifact."))
        for finding_type, attempted in (attempt_flags or {}).items():
            if attempted:
                findings.append(self._finding("critical", finding_type, f"{finding_type} is forbidden in v0.26.4."))
        for finding_type in extra_findings or []:
            severity = "critical" if finding_type in self.BLOCKED_FINDINGS else "warning"
            findings.append(self._finding(severity, finding_type, f"{finding_type} was reported."))
        return findings

    def _finding(self, severity: str, finding_type: str, message: str) -> WorkbenchEvidenceInspectorFinding:
        return WorkbenchEvidenceInspectorFinding(
            finding_id=f"workbench_evidence_inspector_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            subject_ref={"id": "workbench_evidence_inspector"},
            evidence_refs=[],
            withdrawal_condition="Withdraw if v0.26.4 rewrites responses, judges factuality with an LLM, invokes providers, reruns routes/stages, executes approvals or commands, mutates memory/persona/policy, adds adapters, or exposes raw transcript/provider/secret content.",
        )


class WorkbenchEvidenceInspectorReportService:
    def build_report(self, **kwargs: Any) -> WorkbenchEvidenceInspectorReport:
        return self.build_all_parts(**kwargs)["report"]

    def build_all_parts(self, **kwargs: Any) -> dict[str, Any]:
        source_service = WorkbenchEvidenceInspectorPrerequisiteSourceService(
            view_state_available=kwargs.get("view_state_available", True),
            evidence_inspector_panel_available=kwargs.get("evidence_inspector_panel_available", True),
            response_assembly_available=kwargs.get("response_assembly_available", True),
            evidence_bundle_available=kwargs.get("evidence_bundle_available", True),
            claim_support_available=kwargs.get("claim_support_available", True),
            safety_gate_available=kwargs.get("safety_gate_available", True),
            routing_available=kwargs.get("routing_available", True),
            provider_invocation_available=kwargs.get("provider_invocation_available", True),
            intent_available=kwargs.get("intent_available", True),
            provider_browser_available=kwargs.get("provider_browser_available", True),
            trace_explorer_available=kwargs.get("trace_explorer_available", True),
            pig_guidance_available=kwargs.get("pig_guidance_available", True),
            failure_cause_available=kwargs.get("failure_cause_available", True),
        )
        sources = source_service.load_sources()
        policy = WorkbenchEvidenceInspectorPolicyService().build_policy()
        request = WorkbenchEvidenceInspectorRequestService().build_request(sources, kwargs.get("strictness", "standard"))
        source_view = WorkbenchEvidenceSourceViewService().build_source_view(sources)
        response = sources.get("response_assembly") or {}
        draft = response.get("answer_draft")
        evidence_items = list(response.get("evidence_items", []))
        claims = list(getattr(draft, "claims", []))
        supports = list(getattr(draft, "claim_supports", []))
        uncertainties = list(getattr(draft, "uncertainty_notes", []))
        limitations = list(getattr(draft, "limitation_notes", []))
        item_views = WorkbenchEvidenceItemViewService().build_evidence_item_views(evidence_items, claims)
        claim_views = WorkbenchClaimInspectorViewService().build_claim_views(claims, supports)
        support_views = WorkbenchClaimSupportInspectorViewService().build_claim_support_views(supports)
        unsupported_views = WorkbenchUnsupportedClaimViewService().build_unsupported_claim_views(claim_views, support_views)
        bundle_view = WorkbenchEvidenceBundleViewService().build_evidence_bundle_view(response.get("evidence_bundle"), item_views, len(unsupported_views))
        item_refs = [_model_ref("agent_evidence_item", item) for item in evidence_items]
        report_view = WorkbenchReportInspectorViewService().build_report_inspector_view(sources)
        decision_views = WorkbenchDecisionEvidenceViewService().build_decision_evidence_views(sources, item_refs)
        skill_views = WorkbenchSkillSelectionEvidenceViewService().build_skill_selection_evidence_views(sources)
        action_views = WorkbenchActionCandidateEvidenceViewService().build_action_candidate_evidence_views(sources)
        route_views = WorkbenchRouteSelectionEvidenceViewService().build_route_selection_evidence_views(sources)
        provider_views = WorkbenchProviderSelectionEvidenceViewService().build_provider_selection_evidence_views(sources)
        safety_views = WorkbenchSafetyRationaleViewService().build_safety_rationale_views(sources)
        pig_views = WorkbenchPIGGuidanceInspectorViewService().build_pig_guidance_views(sources)
        failure_views = WorkbenchFailureCauseViewService().build_failure_cause_views(sources)
        uncertainty_views = WorkbenchUncertaintyInspectorViewService().build_uncertainty_views(uncertainties)
        limitation_views = WorkbenchLimitationInspectorViewService().build_limitation_views(limitations)
        view = WorkbenchEvidenceInspectorViewService().build_view(
            request,
            source_view,
            report_view,
            bundle_view,
            claim_views,
            support_views,
            decision_views,
            skill_views,
            action_views,
            route_views,
            provider_views,
            safety_views,
            pig_views,
            failure_views,
            unsupported_views,
            uncertainty_views,
            limitation_views,
        )
        filter_service = WorkbenchEvidenceFilterService()
        filter_policy = filter_service.build_policy()
        filter_state = filter_service.build_filter_state(request)
        selection_view = WorkbenchEvidenceSelectionViewService().build_selection_view(request)
        inspection_policy = WorkbenchEvidenceInspectionPolicyService().build_policy()
        inspection_summary = WorkbenchEvidenceInspectionSummaryService().build_summary(view)
        findings = WorkbenchEvidenceInspectorFindingService().build_findings(
            sources,
            view,
            kwargs.get("strictness", "standard"),
            kwargs.get("attempt_flags"),
            kwargs.get("extra_findings"),
        )
        report_status = self._report_status(findings)
        report = WorkbenchEvidenceInspectorReport(
            report_id=kwargs.get("report_id") or "workbench_evidence_inspector_report:v0.26.4",
            created_at=utc_now_iso(),
            evidence_inspector_policy=policy,
            request=request,
            source_view=source_view,
            evidence_inspector_view=view,
            filter_policy=filter_policy,
            filter_state=filter_state,
            selection_view=selection_view,
            inspection_policy=inspection_policy,
            inspection_summary=inspection_summary,
            findings=findings,
            report_status=report_status,
            ready_for_v0_26_5=report_status in {"passed", "warning"},
            evidence_inspector_view_created=True,
            report_inspector_view_created=True,
            evidence_bundle_view_created=bundle_view is not None,
            claim_views_created=bool(claim_views),
            claim_support_views_created=bool(support_views),
            decision_evidence_views_created=bool(decision_views),
            skill_selection_evidence_views_created=bool(skill_views),
            action_candidate_evidence_views_created=bool(action_views),
            route_selection_evidence_views_created=bool(route_views),
            provider_selection_evidence_views_created=bool(provider_views),
            safety_rationale_views_created=bool(safety_views),
            pig_guidance_views_created=bool(pig_views),
            failure_cause_views_created=bool(failure_views),
            unsupported_claim_views_created=bool(unsupported_views),
            uncertainty_views_created=bool(uncertainty_views),
            limitation_views_created=bool(limitation_views),
            limitations=[
                "v0.26.4 creates evidence/report inspector view artifacts only.",
                "Evidence and report inspection remains refs-only and does not rewrite responses or judge factuality.",
            ],
            withdrawal_conditions=[
                "Withdraw if v0.26.4 inlines raw transcript/provider/secret content, invokes providers, reruns routes/stages, executes approvals or commands, mutates memory/persona/policy, adds adapters, or uses an LLM judge.",
            ],
        )
        return {
            "report": report,
            "policy": policy,
            "request": request,
            "source_view": source_view,
            "report_inspector_view": report_view,
            "evidence_bundle_view": bundle_view,
            "evidence_item_views": item_views,
            "claim_views": claim_views,
            "claim_support_views": support_views,
            "decision_evidence_views": decision_views,
            "skill_selection_evidence_views": skill_views,
            "action_candidate_evidence_views": action_views,
            "route_selection_evidence_views": route_views,
            "provider_selection_evidence_views": provider_views,
            "safety_rationale_views": safety_views,
            "pig_guidance_views": pig_views,
            "failure_cause_views": failure_views,
            "unsupported_claim_views": unsupported_views,
            "uncertainty_views": uncertainty_views,
            "limitation_views": limitation_views,
            "filter_policy": filter_policy,
            "filter_state": filter_state,
            "selection_view": selection_view,
            "inspection_policy": inspection_policy,
            "inspection_summary": inspection_summary,
            "evidence_inspector_view": view,
            "findings": findings,
        }

    def _report_status(self, findings: list[WorkbenchEvidenceInspectorFinding]) -> str:
        if any(finding.severity == "critical" for finding in findings):
            return "blocked"
        if any(finding.severity == "error" for finding in findings):
            return "failed"
        if any(finding.severity == "warning" for finding in findings):
            return "warning"
        return "passed"

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": WORKBENCH_EVIDENCE_INSPECTOR_VERSION,
            "layer": WORKBENCH_EVIDENCE_INSPECTOR_LAYER,
            "subject": "evidence_report_inspector",
            "principles": [
                "Evidence Inspector is not raw provider output dump",
                "Report Inspector is not response regeneration",
                "Claim inspection is not claim rewriting",
                "Decision evidence view is not decision mutation",
                "Skill selection evidence view is not skill execution",
                "Action candidate evidence view is not action execution",
                "Route selection evidence view is not route rerun",
                "Provider selection evidence view is not provider invocation",
                "Safety rationale view is not safety policy mutation",
                "PIG guidance inspector is not memory, policy mutation, or execution",
                "Failure cause view is not automatic repair",
            ],
            "safety_boundary": {
                "evidence_inspector_view_created": "conditional",
                "report_inspector_view_created": "conditional",
                "claim_views_created": "conditional",
                "decision_evidence_views_created": "conditional",
                "safety_rationale_views_created": "conditional",
                "pig_guidance_views_created": "conditional",
                "failure_cause_views_created": "conditional",
                "actual_ui_rendered": False,
                "panel_rendered": False,
                "response_rewritten": False,
                "factuality_llm_judge_used": False,
                "decision_mutated": False,
                "safety_policy_mutated": False,
                "provider_invoked": False,
                "provider_test_run_performed": False,
                "route_rerun_performed": False,
                "stage_rerun_performed": False,
                "approval_executed": False,
                "ask_executed": False,
                "final_response_emitted": False,
                "local_command_executed": False,
                "direct_file_access_performed": False,
                "direct_subprocess_performed": False,
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
                "v0.26.5 safety gate / approval console",
                "v0.26.6 run dashboard / session monitor",
                "v0.26.7 command surface",
                "v0.26.8 snapshot / OCEL export",
                "v0.27 memory candidate and continuity",
            ],
            "next_step": WORKBENCH_EVIDENCE_INSPECTOR_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "workbench_evidence_report_inspector_created",
            "version": WORKBENCH_EVIDENCE_INSPECTOR_VERSION,
            "source_read_models": [
                "WorkbenchViewStateState",
                "WorkbenchProviderBrowserViewState",
                "AgentResponseAssemblyState",
                "AgentEvidenceBundleState",
                "AgentClaimState",
                "AgentClaimSupportState",
                "AgentSafetyGateState",
                "AgentToolRoutingState",
                "AgentProviderSelectionState",
                "AgentProviderInvocationState",
                "PigGuidanceState",
            ],
            "target_read_models": [
                "WorkbenchEvidenceInspectorViewState",
                "WorkbenchReportInspectorViewState",
                "WorkbenchEvidenceBundleViewState",
                "WorkbenchClaimInspectorState",
                "WorkbenchDecisionEvidenceState",
                "WorkbenchSafetyRationaleState",
                "WorkbenchPIGGuidanceInspectorState",
                "WorkbenchFailureCauseState",
                "WorkbenchUnsupportedClaimState",
                "V026ReadinessState",
            ],
            "effect_types": WORKBENCH_EVIDENCE_INSPECTOR_EFFECT_TYPES,
        }


def render_workbench_evidence_inspector_cli(parts: dict[str, Any], section: str = "view") -> str:
    report: WorkbenchEvidenceInspectorReport = parts["report"]
    lines = [
        f"version={report.version}",
        f"layer={WORKBENCH_EVIDENCE_INSPECTOR_LAYER}",
        f"evidence_inspector_view_created={str(report.evidence_inspector_view_created).lower()}",
        f"report_inspector_view_created={str(report.report_inspector_view_created).lower()}",
        f"evidence_bundle_view_created={str(report.evidence_bundle_view_created).lower()}",
        f"claim_views_created={str(report.claim_views_created).lower()}",
        f"claim_support_views_created={str(report.claim_support_views_created).lower()}",
        f"decision_evidence_views_created={str(report.decision_evidence_views_created).lower()}",
        f"skill_selection_evidence_views_created={str(report.skill_selection_evidence_views_created).lower()}",
        f"action_candidate_evidence_views_created={str(report.action_candidate_evidence_views_created).lower()}",
        f"route_selection_evidence_views_created={str(report.route_selection_evidence_views_created).lower()}",
        f"provider_selection_evidence_views_created={str(report.provider_selection_evidence_views_created).lower()}",
        f"safety_rationale_views_created={str(report.safety_rationale_views_created).lower()}",
        f"pig_guidance_views_created={str(report.pig_guidance_views_created).lower()}",
        f"failure_cause_views_created={str(report.failure_cause_views_created).lower()}",
        f"unsupported_claim_views_created={str(report.unsupported_claim_views_created).lower()}",
        f"uncertainty_views_created={str(report.uncertainty_views_created).lower()}",
        f"limitation_views_created={str(report.limitation_views_created).lower()}",
        f"ready_for_v0_26_5={str(report.ready_for_v0_26_5).lower()}",
        f"ready_for_v0_27={str(report.ready_for_v0_27).lower()}",
        f"actual_ui_rendered={str(report.actual_ui_rendered).lower()}",
        f"panel_rendered={str(report.panel_rendered).lower()}",
        f"response_rewritten={str(report.response_rewritten).lower()}",
        f"factuality_llm_judge_used={str(report.factuality_llm_judge_used).lower()}",
        f"provider_invoked={str(report.provider_invoked).lower()}",
        f"provider_test_run_performed={str(report.provider_test_run_performed).lower()}",
        f"route_rerun_performed={str(report.route_rerun_performed).lower()}",
        f"stage_rerun_performed={str(report.stage_rerun_performed).lower()}",
        f"approval_executed={str(report.approval_executed).lower()}",
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
        f"external_provider_adapter_implemented={str(report.external_provider_adapter_implemented).lower()}",
        f"external_agent_adapter_implemented={str(report.external_agent_adapter_implemented).lower()}",
        f"vendor_adapter_implemented={str(report.vendor_adapter_implemented).lower()}",
        f"pm4py_runtime_dependency_added={str(report.pm4py_runtime_dependency_added).lower()}",
        f"ocpa_runtime_dependency_added={str(report.ocpa_runtime_dependency_added).lower()}",
        f"pig_memory_promoted={str(report.pig_memory_promoted).lower()}",
        f"pig_policy_mutated={str(report.pig_policy_mutated).lower()}",
        f"pig_executed={str(report.pig_executed).lower()}",
        f"schumpeter_split_introduced={str(report.schumpeter_split_introduced).lower()}",
        f"credential_exposed={str(report.credential_exposed).lower()}",
        f"raw_secret_output={str(report.raw_secret_output).lower()}",
        f"raw_provider_output_inline={str(report.raw_provider_output_inline).lower()}",
        f"raw_transcript_persisted={str(report.raw_transcript_persisted).lower()}",
        f"llm_judge_used={str(report.llm_judge_used).lower()}",
        f"next_required_step={report.next_required_step}",
    ]
    if section == "view":
        view = parts["evidence_inspector_view"]
        lines.extend([f"view_status={view.view_status}", f"panel_id={view.panel_id}"])
    elif section == "bundle":
        bundle = parts["evidence_bundle_view"]
        lines.append(f"evidence_count={bundle.evidence_count if bundle else 0}")
        lines.append(f"bundle_status={bundle.bundle_status if bundle else 'missing'}")
    elif section == "claims":
        for item in parts["claim_views"]:
            lines.append(f"- {item.claim_ref['id']}: support_status={item.support_status} unsupported={str(item.unsupported).lower()}")
    elif section == "support":
        for item in parts["claim_support_views"]:
            lines.append(f"- {item.claim_ref['id']}: support_status={item.support_status}")
    elif section == "decisions":
        for item in parts["decision_evidence_views"]:
            lines.append(f"- {item.decision_type}: outcome={item.decision_outcome} decision_mutated_now={str(item.decision_mutated_now).lower()}")
    elif section == "skills":
        for item in parts["skill_selection_evidence_views"]:
            lines.append(f"- {item.skill_id}: selected={str(item.selected).lower()} skill_executed_now={str(item.skill_executed_now).lower()}")
    elif section == "actions":
        for item in parts["action_candidate_evidence_views"]:
            lines.append(f"- {item.action_type}: evidence_bound={str(item.evidence_bound).lower()} action_executed_now={str(item.action_executed_now).lower()}")
    elif section == "routes":
        for item in parts["route_selection_evidence_views"]:
            lines.append(f"- {item.route_kind}: route_rerun_now={str(item.route_rerun_now).lower()}")
    elif section == "providers":
        for item in parts["provider_selection_evidence_views"]:
            lines.append(f"- {item.provider_id}: provider_invoked_now={str(item.provider_invoked_now).lower()}")
    elif section == "safety":
        for item in parts["safety_rationale_views"]:
            lines.append(f"- {item.gate_outcome}: safety_policy_mutated_now={str(item.safety_policy_mutated_now).lower()}")
    elif section == "pig-guidance":
        for item in parts["pig_guidance_views"]:
            lines.append(f"- {item.guidance_type}: pig_guidance_executes={str(item.pig_guidance_executes).lower()}")
    elif section == "failures":
        for item in parts["failure_cause_views"]:
            lines.append(f"- {item.failure_category}: automatic_repair_enabled={str(item.automatic_repair_enabled).lower()}")
    elif section == "unsupported":
        for item in parts["unsupported_claim_views"]:
            lines.append(f"- {item.claim_ref['id']}: auto_corrected={str(item.auto_corrected).lower()} response_rewritten={str(item.response_rewritten).lower()}")
    elif section == "uncertainty":
        for item in parts["uncertainty_views"]:
            lines.append(f"- {item.uncertainty_ref['id']}: converted_to_certainty_now={str(item.converted_to_certainty_now).lower()}")
    elif section == "limitations":
        for item in parts["limitation_views"]:
            lines.append(f"- {item.limitation_ref['id']}: treated_as_failure={str(item.treated_as_failure).lower()}")
    elif section == "inspect":
        summary = parts["inspection_summary"]
        lines.append(f"summary_status={summary.summary_status}")
        lines.append(f"raw_provider_output_included={str(summary.raw_provider_output_included).lower()}")
        lines.append(f"raw_transcript_included={str(summary.raw_transcript_included).lower()}")
        lines.append(f"raw_secret_included={str(summary.raw_secret_included).lower()}")
    elif section == "report":
        lines.append(f"report_id={report.report_id}")
        lines.append(f"report_status={report.report_status}")
        lines.append(f"finding_count={len(report.findings)}")
    return "\n".join(lines)
