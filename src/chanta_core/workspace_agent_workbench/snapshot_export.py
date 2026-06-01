from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace_agent_workbench.command_surface import WORKBENCH_COMMAND_SURFACE_EFFECT_TYPES
from chanta_core.workspace_agent_workbench.view_state import WorkbenchViewStateReportService


WORKBENCH_SNAPSHOT_EXPORT_VERSION = "v0.26.8"
WORKBENCH_SNAPSHOT_EXPORT_VERSION_NAME = "Workbench Snapshot / OCEL Export"
WORKBENCH_SNAPSHOT_EXPORT_KOREAN_NAME = "Workbench Snapshot.OCEL Export"
WORKBENCH_SNAPSHOT_EXPORT_LAYER = "workspace_agent_workbench"
WORKBENCH_SNAPSHOT_EXPORT_TRACK = "Workspace Agent Workbench"
WORKBENCH_SNAPSHOT_EXPORT_NEXT_STEP = "v0.26.9 Workspace Agent Workbench Consolidation"

WORKBENCH_SNAPSHOT_EXPORT_IMPLEMENTED_SKILL_IDS = [
    "skill:workbench_snapshot_create",
    "skill:workbench_ocel_export_create",
]
WORKBENCH_SNAPSHOT_EXPORT_FUTURE_SKILL_IDS = [
    "skill:workbench_consolidation_view",
]

WORKBENCH_SNAPSHOT_EXPORT_OBJECT_TYPES = [
    "workbench_snapshot_policy",
    "workbench_snapshot_request",
    "workbench_snapshot_source_view",
    "workbench_snapshot_selection_policy",
    "workbench_snapshot_selection",
    "workbench_snapshot",
    "workbench_snapshot_manifest",
    "workbench_snapshot_ref_bundle",
    "workbench_decision_point_export_ref",
    "workbench_skill_candidate_export_ref",
    "workbench_action_candidate_export_ref",
    "workbench_route_rationale_export_ref",
    "workbench_provider_rationale_export_ref",
    "workbench_safety_rationale_export_ref",
    "workbench_pig_guidance_export_ref",
    "workbench_human_intervention_export_ref",
    "workbench_approval_decision_export_ref",
    "workbench_failure_cause_export_ref",
    "workbench_command_candidate_export_ref",
    "workbench_ocel_export_policy",
    "workbench_ocel_export_package",
    "workbench_ocel_export_manifest",
    "workbench_event_quality_report",
    "workbench_trace_coverage_report",
    "workbench_snapshot_redaction_policy",
    "workbench_snapshot_redaction_report",
    "workbench_reproducibility_packet",
    "workbench_export_boundary_descriptor",
    "workbench_snapshot_export_finding",
    "workbench_snapshot_export_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

WORKBENCH_SNAPSHOT_EXPORT_EVENT_TYPES = [
    "workbench_snapshot_requested",
    "workbench_snapshot_policy_created",
    "workbench_snapshot_source_view_created",
    "workbench_snapshot_selection_created",
    "workbench_snapshot_created",
    "workbench_snapshot_manifest_created",
    "workbench_snapshot_ref_bundle_created",
    "workbench_decision_point_export_ref_created",
    "workbench_skill_candidate_export_ref_created",
    "workbench_action_candidate_export_ref_created",
    "workbench_route_rationale_export_ref_created",
    "workbench_provider_rationale_export_ref_created",
    "workbench_safety_rationale_export_ref_created",
    "workbench_pig_guidance_export_ref_created",
    "workbench_human_intervention_export_ref_created",
    "workbench_approval_decision_export_ref_created",
    "workbench_failure_cause_export_ref_created",
    "workbench_command_candidate_export_ref_created",
    "workbench_ocel_export_policy_created",
    "workbench_ocel_export_package_created",
    "workbench_ocel_export_manifest_created",
    "workbench_event_quality_report_created",
    "workbench_trace_coverage_report_created",
    "workbench_snapshot_redaction_policy_created",
    "workbench_snapshot_redaction_report_created",
    "workbench_reproducibility_packet_created",
    "workbench_export_boundary_descriptor_created",
    "workbench_snapshot_export_report_created",
    "workbench_snapshot_export_warning_created",
    "workbench_snapshot_export_blocked",
]

WORKBENCH_SNAPSHOT_EXPORT_RELATION_TYPES = [
    "uses_workbench_view_state",
    "uses_snapshot_export_panel",
    "uses_command_surface_report",
    "uses_run_dashboard_report",
    "uses_approval_console_report",
    "uses_evidence_inspector_report",
    "uses_provider_browser_report",
    "uses_trace_explorer_report",
    "uses_trace_telemetry_report",
    "uses_pig_guidance_ref",
    "creates_snapshot_selection",
    "creates_workbench_snapshot",
    "creates_snapshot_manifest",
    "creates_snapshot_ref_bundle",
    "creates_ocel_export_package",
    "creates_ocel_export_manifest",
    "creates_event_quality_report",
    "creates_trace_coverage_report",
    "creates_redaction_report",
    "creates_reproducibility_packet",
    "creates_export_boundary_descriptor",
    "defers_consolidation_to_v0_26_9",
    "defers_memory_continuity_to_v0_27",
    "not_memory_promoted",
    "not_raw_transcript_exported",
    "not_raw_provider_output_exported",
    "not_external_sync_performed",
    "not_command_executed",
    "not_provider_invoked",
    "not_pig_memory_promoted",
    "not_pig_policy_mutated",
    "not_pig_executed",
]

WORKBENCH_SNAPSHOT_EXPORT_EFFECT_TYPES = [
    "read_only_observation",
    "workbench_snapshot_created",
    "workbench_snapshot_manifest_created",
    "workbench_snapshot_ref_bundle_created",
    "workbench_ocel_export_created",
    "workbench_event_quality_report_created",
    "workbench_trace_coverage_report_created",
    "workbench_redaction_report_created",
    "workbench_reproducibility_packet_created",
    "workbench_export_boundary_descriptor_created",
    "state_candidate_created",
]

WORKBENCH_SNAPSHOT_EXPORT_FORBIDDEN_EFFECT_TYPES = [
    "memory_candidate_created",
    "memory_promoted",
    "persistent_memory_written",
    "persona_mutated",
    "raw_transcript_exported",
    "raw_provider_output_exported",
    "raw_secret_exported",
    "credential_exported",
    "private_full_path_exported",
    "external_sync_performed",
    "external_provider_adapter_implemented",
    "external_agent_adapter_implemented",
    "vendor_adapter_implemented",
    "pm4py_runtime_dependency_added",
    "ocpa_runtime_dependency_added",
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
    "pig_memory_promoted",
    "pig_policy_mutated",
    "pig_executed",
    "schumpeter_split_introduced",
    "llm_judge_used",
]

EXCLUDED_RAW_DATA_CATEGORIES = [
    "raw_transcripts",
    "raw_provider_outputs",
    "raw_secrets",
    "credentials",
    "private_full_paths",
]


def _safe_id(value: str | None) -> str:
    text = value or "unknown"
    return "".join(char if char.isalnum() else "_" for char in text).strip("_").lower() or "unknown"


def _ref(ref_type: str, ref_id: str, version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION) -> dict[str, Any]:
    return {"type": ref_type, "id": ref_id, "version": version}


def _model_ref(ref_type: str, model: Any, id_attr: str) -> dict[str, Any]:
    return _ref(ref_type, getattr(model, id_attr), getattr(model, "version", WORKBENCH_SNAPSHOT_EXPORT_VERSION))


class _ModelMixin:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class WorkbenchSnapshotPolicy(_ModelMixin):
    policy_id: str
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    layer: str = WORKBENCH_SNAPSHOT_EXPORT_LAYER
    snapshot_enabled: bool = True
    ocel_export_enabled: bool = True
    reproducibility_packet_enabled: bool = True
    event_quality_report_enabled: bool = True
    trace_coverage_report_enabled: bool = True
    redaction_report_enabled: bool = True
    memory_promotion_enabled: bool = False
    persistent_memory_write_enabled: bool = False
    memory_candidate_extraction_enabled: bool = False
    persona_mutation_enabled: bool = False
    external_sync_enabled: bool = False
    external_adapter_enabled: bool = False
    pm4py_runtime_dependency_enabled: bool = False
    ocpa_runtime_dependency_enabled: bool = False
    command_execution_enabled: bool = False
    provider_invocation_enabled: bool = False
    local_runtime_execution_enabled: bool = False
    file_mutation_enabled: bool = False
    ask_execution_enabled: bool = False
    response_emission_enabled: bool = False
    route_rerun_enabled: bool = False
    stage_rerun_enabled: bool = False
    automatic_retry_enabled: bool = False
    automatic_repair_enabled: bool = False
    autonomous_loop_enabled: bool = False
    refs_only_by_default: bool = True
    raw_transcript_export_forbidden: bool = True
    raw_provider_output_export_forbidden: bool = True
    raw_secret_export_forbidden: bool = True
    credential_export_forbidden: bool = True
    private_full_path_export_forbidden: bool = True
    pig_guidance_is_not_memory: bool = True
    pig_guidance_is_not_policy_mutation: bool = True
    pig_guidance_is_not_execution: bool = True
    ocel_visible: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSnapshotRequest(_ModelMixin):
    request_id: str
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    view_state_report_id: str | None = None
    view_state_id: str | None = None
    snapshot_export_panel_id: str | None = None
    command_surface_report_id: str | None = None
    dashboard_report_id: str | None = None
    approval_console_report_id: str | None = None
    evidence_inspector_report_id: str | None = None
    provider_browser_report_id: str | None = None
    trace_explorer_report_id: str | None = None
    trace_telemetry_report_id: str | None = None
    selected_ref_candidates: list[dict[str, Any]] = field(default_factory=list)
    requested_export_profile: str | None = None
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"


@dataclass
class WorkbenchSnapshotSourceView(_ModelMixin):
    source_view_id: str
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    workbench_report_refs: list[dict[str, Any]] = field(default_factory=list)
    command_candidate_refs: list[dict[str, Any]] = field(default_factory=list)
    decision_point_refs: list[dict[str, Any]] = field(default_factory=list)
    skill_candidate_refs: list[dict[str, Any]] = field(default_factory=list)
    action_candidate_refs: list[dict[str, Any]] = field(default_factory=list)
    route_rationale_refs: list[dict[str, Any]] = field(default_factory=list)
    provider_rationale_refs: list[dict[str, Any]] = field(default_factory=list)
    safety_rationale_refs: list[dict[str, Any]] = field(default_factory=list)
    pig_guidance_refs: list[dict[str, Any]] = field(default_factory=list)
    human_intervention_refs: list[dict[str, Any]] = field(default_factory=list)
    approval_decision_refs: list[dict[str, Any]] = field(default_factory=list)
    failure_cause_refs: list[dict[str, Any]] = field(default_factory=list)
    trace_refs: list[dict[str, Any]] = field(default_factory=list)
    ocel_projection_refs: list[dict[str, Any]] = field(default_factory=list)
    source_status: str = "complete"
    raw_provider_output_included: bool = False
    raw_transcript_included: bool = False
    raw_secret_included: bool = False
    private_full_path_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSnapshotSelectionPolicy(_ModelMixin):
    policy_id: str
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    selection_enabled: bool = True
    selection_is_not_memory_candidate: bool = True
    selection_is_not_memory_promotion: bool = True
    refs_only_selection_required: bool = True
    raw_content_selection_forbidden: bool = True
    sensitive_ref_redaction_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSnapshotSelection(_ModelMixin):
    selection_id: str
    selected_refs: list[dict[str, Any]]
    selected_ref_count: int
    selected_categories: list[str]
    omitted_refs: list[dict[str, Any]]
    omission_reasons: list[str]
    selection_status: str
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    memory_candidate_created: bool = False
    memory_promoted: bool = False
    raw_content_selected: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSnapshot(_ModelMixin):
    snapshot_id: str
    created_at: str
    snapshot_name: str
    source_view_id: str
    selection_id: str
    manifest_id: str
    ref_bundle_id: str
    redaction_report_id: str
    reproducibility_packet_id: str
    event_quality_report_id: str
    trace_coverage_report_id: str
    snapshot_status: str
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    refs_only: bool = True
    memory_promoted: bool = False
    persistent_memory_written: bool = False
    raw_transcript_included: bool = False
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False
    credential_included: bool = False
    private_full_path_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSnapshotManifest(_ModelMixin):
    manifest_id: str
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    snapshot_id: str | None = None
    included_report_refs: list[dict[str, Any]] = field(default_factory=list)
    included_trace_refs: list[dict[str, Any]] = field(default_factory=list)
    included_decision_point_refs: list[dict[str, Any]] = field(default_factory=list)
    included_candidate_refs: list[dict[str, Any]] = field(default_factory=list)
    included_approval_refs: list[dict[str, Any]] = field(default_factory=list)
    included_failure_refs: list[dict[str, Any]] = field(default_factory=list)
    included_pig_guidance_refs: list[dict[str, Any]] = field(default_factory=list)
    excluded_raw_data_categories: list[str] = field(default_factory=list)
    redaction_report_ref: dict[str, Any] | None = None
    manifest_status: str = "ready"
    is_memory_index: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchDecisionPointExportRef(_ModelMixin):
    export_ref_id: str
    decision_ref: dict[str, Any]
    decision_type: str
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    decision_outcome: str | None = None
    rationale_refs: list[dict[str, Any]] = field(default_factory=list)
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    raw_content_included: bool = False


@dataclass
class WorkbenchSkillCandidateExportRef(_ModelMixin):
    export_ref_id: str
    skill_candidate_ref: dict[str, Any]
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    skill_id: str | None = None
    skill_name: str | None = None
    selection_refs: list[dict[str, Any]] = field(default_factory=list)
    pig_guidance_refs: list[dict[str, Any]] = field(default_factory=list)
    skill_executed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchActionCandidateExportRef(_ModelMixin):
    export_ref_id: str
    action_candidate_ref: dict[str, Any]
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    action_type: str | None = None
    rationale_refs: list[dict[str, Any]] = field(default_factory=list)
    risk_refs: list[dict[str, Any]] = field(default_factory=list)
    approval_refs: list[dict[str, Any]] = field(default_factory=list)
    action_executed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchRouteRationaleExportRef(_ModelMixin):
    export_ref_id: str
    route_ref: dict[str, Any]
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    route_kind: str | None = None
    selection_rationale_refs: list[dict[str, Any]] = field(default_factory=list)
    compatibility_refs: list[dict[str, Any]] = field(default_factory=list)
    route_executed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchProviderRationaleExportRef(_ModelMixin):
    export_ref_id: str
    provider_ref: dict[str, Any]
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    provider_id: str | None = None
    capability_id: str | None = None
    rationale_refs: list[dict[str, Any]] = field(default_factory=list)
    boundary_risk_refs: list[dict[str, Any]] = field(default_factory=list)
    readiness_refs: list[dict[str, Any]] = field(default_factory=list)
    provider_invoked_now: bool = False
    raw_provider_output_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSafetyRationaleExportRef(_ModelMixin):
    export_ref_id: str
    safety_ref: dict[str, Any]
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    gate_outcome: str | None = None
    safety_rule_refs: list[dict[str, Any]] = field(default_factory=list)
    risk_refs: list[dict[str, Any]] = field(default_factory=list)
    safety_policy_mutated_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchPIGGuidanceExportRef(_ModelMixin):
    export_ref_id: str
    pig_guidance_ref: dict[str, Any]
    guidance_type: str
    guidance_summary: str
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    related_refs: list[dict[str, Any]] = field(default_factory=list)
    pig_guidance_is_memory: bool = False
    pig_guidance_mutates_policy: bool = False
    pig_guidance_executes: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchHumanInterventionExportRef(_ModelMixin):
    export_ref_id: str
    intervention_ref: dict[str, Any]
    intervention_type: str
    reason: str
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    approval_ref: dict[str, Any] | None = None
    execution_triggered_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchApprovalDecisionExportRef(_ModelMixin):
    export_ref_id: str
    approval_decision_ref: dict[str, Any]
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    decision_type: str = "unknown"
    decision_reason: str | None = None
    scope_refs: list[dict[str, Any]] = field(default_factory=list)
    expiry_refs: list[dict[str, Any]] = field(default_factory=list)
    execution_triggered: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchFailureCauseExportRef(_ModelMixin):
    export_ref_id: str
    failure_cause_ref: dict[str, Any]
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    failure_category: str | None = None
    failure_stage: str | None = None
    recovery_guidance_refs: list[dict[str, Any]] = field(default_factory=list)
    automatic_repair_enabled: bool = False
    auto_retry_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchCommandCandidateExportRef(_ModelMixin):
    export_ref_id: str
    command_candidate_ref: dict[str, Any]
    command_type: str
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    boundary_trace_refs: list[dict[str, Any]] = field(default_factory=list)
    decision_record_refs: list[dict[str, Any]] = field(default_factory=list)
    do_nothing_candidate_refs: list[dict[str, Any]] = field(default_factory=list)
    command_executed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSnapshotRefBundle(_ModelMixin):
    ref_bundle_id: str
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    decision_point_export_refs: list[WorkbenchDecisionPointExportRef] = field(default_factory=list)
    skill_candidate_export_refs: list[WorkbenchSkillCandidateExportRef] = field(default_factory=list)
    action_candidate_export_refs: list[WorkbenchActionCandidateExportRef] = field(default_factory=list)
    route_rationale_export_refs: list[WorkbenchRouteRationaleExportRef] = field(default_factory=list)
    provider_rationale_export_refs: list[WorkbenchProviderRationaleExportRef] = field(default_factory=list)
    safety_rationale_export_refs: list[WorkbenchSafetyRationaleExportRef] = field(default_factory=list)
    pig_guidance_export_refs: list[WorkbenchPIGGuidanceExportRef] = field(default_factory=list)
    human_intervention_export_refs: list[WorkbenchHumanInterventionExportRef] = field(default_factory=list)
    approval_decision_export_refs: list[WorkbenchApprovalDecisionExportRef] = field(default_factory=list)
    failure_cause_export_refs: list[WorkbenchFailureCauseExportRef] = field(default_factory=list)
    command_candidate_export_refs: list[WorkbenchCommandCandidateExportRef] = field(default_factory=list)
    ref_count: int = 0
    bundle_status: str = "ready"
    raw_content_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchOCELExportPolicy(_ModelMixin):
    policy_id: str
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    export_enabled: bool = True
    export_refs_only: bool = True
    mutate_original_artifacts: bool = False
    external_sync_enabled: bool = False
    external_adapter_enabled: bool = False
    raw_transcript_export_forbidden: bool = True
    raw_provider_output_export_forbidden: bool = True
    raw_secret_export_forbidden: bool = True
    credential_export_forbidden: bool = True
    private_full_path_export_forbidden: bool = True
    pm4py_runtime_dependency_enabled: bool = False
    ocpa_runtime_dependency_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchOCELExportPackage(_ModelMixin):
    export_package_id: str
    snapshot_id: str
    export_manifest_id: str
    object_type_refs: list[str]
    event_type_refs: list[str]
    relation_type_refs: list[str]
    effect_type_refs: list[str]
    exported_object_count: int
    exported_event_count: int
    exported_relation_count: int
    export_status: str
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    refs_only: bool = True
    external_sync_performed: bool = False
    raw_transcript_exported: bool = False
    raw_provider_output_exported: bool = False
    raw_secret_exported: bool = False
    credential_exported: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchOCELExportManifest(_ModelMixin):
    export_manifest_id: str
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    export_package_id: str | None = None
    snapshot_ref: dict[str, Any] | None = None
    included_object_types: list[str] = field(default_factory=list)
    included_event_types: list[str] = field(default_factory=list)
    included_relation_types: list[str] = field(default_factory=list)
    included_effect_types: list[str] = field(default_factory=list)
    excluded_raw_categories: list[str] = field(default_factory=list)
    export_boundary_descriptor_ref: dict[str, Any] | None = None
    manifest_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchEventQualityReport(_ModelMixin):
    event_quality_report_id: str
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    source_snapshot_id: str | None = None
    decision_point_coverage: float | None = None
    skill_candidate_coverage: float | None = None
    action_candidate_coverage: float | None = None
    route_rationale_coverage: float | None = None
    provider_rationale_coverage: float | None = None
    safety_rationale_coverage: float | None = None
    pig_guidance_coverage: float | None = None
    approval_decision_coverage: float | None = None
    failure_cause_coverage: float | None = None
    human_intervention_coverage: float | None = None
    missing_quality_dimensions: list[str] = field(default_factory=list)
    quality_status: str = "ready"
    automatic_optimization_performed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchTraceCoverageReport(_ModelMixin):
    trace_coverage_report_id: str
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    source_snapshot_id: str | None = None
    trace_ref_count: int = 0
    stage_trace_coverage: dict[str, bool] = field(default_factory=dict)
    decision_trace_coverage: dict[str, bool] = field(default_factory=dict)
    provider_trace_coverage: bool = False
    response_trace_coverage: bool = False
    approval_trace_coverage: bool = False
    command_trace_coverage: bool = False
    coverage_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSnapshotRedactionPolicy(_ModelMixin):
    policy_id: str
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    redaction_enabled: bool = True
    redact_raw_transcripts: bool = True
    redact_raw_provider_outputs: bool = True
    redact_raw_secrets: bool = True
    redact_credentials: bool = True
    redact_private_full_paths: bool = True
    preserve_refs: bool = True
    preserve_sanitized_summaries: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSnapshotRedactionReport(_ModelMixin):
    redaction_report_id: str
    redaction_policy_id: str
    redacted_raw_transcript_count: int
    redacted_raw_provider_output_count: int
    redacted_raw_secret_count: int
    redacted_credential_count: int
    redacted_private_path_count: int
    preserved_ref_count: int
    preserved_summary_count: int
    redaction_status: str
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchReproducibilityPacket(_ModelMixin):
    reproducibility_packet_id: str
    snapshot_id: str
    required_report_refs: list[dict[str, Any]]
    required_boundary_refs: list[dict[str, Any]]
    command_candidate_refs: list[dict[str, Any]]
    approval_decision_refs: list[dict[str, Any]]
    reproducibility_summary: str
    reproducibility_status: str
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    export_package_ref: dict[str, Any] | None = None
    rerun_permission_granted: bool = False
    rerun_performed: bool = False
    provider_invoked: bool = False
    command_executed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchExportBoundaryDescriptor(_ModelMixin):
    boundary_descriptor_id: str
    export_boundary_type: str
    boundary_summary: str
    allowed_targets: list[str]
    forbidden_targets: list[str]
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    external_adapter_invoked: bool = False
    pm4py_runtime_dependency_used: bool = False
    ocpa_runtime_dependency_used: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkbenchSnapshotExportFinding(_ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None = None
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    withdrawal_condition: str | None = None


@dataclass
class WorkbenchSnapshotExportReport(_ModelMixin):
    report_id: str
    created_at: str
    snapshot_policy: WorkbenchSnapshotPolicy
    request: WorkbenchSnapshotRequest
    source_view: WorkbenchSnapshotSourceView
    selection_policy: WorkbenchSnapshotSelectionPolicy
    selection: WorkbenchSnapshotSelection
    snapshot: WorkbenchSnapshot
    snapshot_manifest: WorkbenchSnapshotManifest
    ref_bundle: WorkbenchSnapshotRefBundle
    ocel_export_policy: WorkbenchOCELExportPolicy
    ocel_export_package: WorkbenchOCELExportPackage
    ocel_export_manifest: WorkbenchOCELExportManifest
    event_quality_report: WorkbenchEventQualityReport
    trace_coverage_report: WorkbenchTraceCoverageReport
    redaction_policy: WorkbenchSnapshotRedactionPolicy
    redaction_report: WorkbenchSnapshotRedactionReport
    reproducibility_packet: WorkbenchReproducibilityPacket
    export_boundary_descriptor: WorkbenchExportBoundaryDescriptor
    findings: list[WorkbenchSnapshotExportFinding]
    report_status: str
    ready_for_v0_26_9: bool
    snapshot_created: bool
    snapshot_manifest_created: bool
    ref_bundle_created: bool
    ocel_export_package_created: bool
    ocel_export_manifest_created: bool
    event_quality_report_created: bool
    trace_coverage_report_created: bool
    redaction_report_created: bool
    reproducibility_packet_created: bool
    export_boundary_descriptor_created: bool
    version: str = WORKBENCH_SNAPSHOT_EXPORT_VERSION
    ready_for_v0_27: bool = False
    actual_ui_rendered: bool = False
    panel_rendered: bool = False
    memory_candidate_created: bool = False
    memory_promoted: bool = False
    persistent_memory_written: bool = False
    persona_mutated: bool = False
    raw_transcript_exported: bool = False
    raw_provider_output_exported: bool = False
    raw_secret_exported: bool = False
    credential_exported: bool = False
    private_full_path_exported: bool = False
    external_sync_performed: bool = False
    external_provider_adapter_implemented: bool = False
    external_agent_adapter_implemented: bool = False
    vendor_adapter_implemented: bool = False
    pm4py_runtime_dependency_added: bool = False
    ocpa_runtime_dependency_added: bool = False
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
    pig_memory_promoted: bool = False
    pig_policy_mutated: bool = False
    pig_executed: bool = False
    schumpeter_split_introduced: bool = False
    llm_judge_used: bool = False
    next_required_step: str = WORKBENCH_SNAPSHOT_EXPORT_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = (
        "Valid until v0.26.9 Workspace Agent Workbench Consolidation begins or snapshot/export policy changes."
    )


class WorkbenchSnapshotPrerequisiteSourceService:
    def __init__(
        self,
        *,
        view_state_available: bool = True,
        snapshot_export_panel_available: bool = True,
        command_surface_available: bool = True,
        dashboard_available: bool = True,
        approval_console_available: bool = True,
        evidence_inspector_available: bool = True,
        provider_browser_available: bool = True,
        trace_explorer_available: bool = True,
        trace_telemetry_available: bool = True,
        pig_guidance_available: bool = True,
    ) -> None:
        self.view_state_available = view_state_available
        self.snapshot_export_panel_available = snapshot_export_panel_available
        self.command_surface_available = command_surface_available
        self.dashboard_available = dashboard_available
        self.approval_console_available = approval_console_available
        self.evidence_inspector_available = evidence_inspector_available
        self.provider_browser_available = provider_browser_available
        self.trace_explorer_available = trace_explorer_available
        self.trace_telemetry_available = trace_telemetry_available
        self.pig_guidance_available = pig_guidance_available

    def load_workbench_view_state(self) -> dict[str, Any] | None:
        if not self.view_state_available:
            return None
        parts = WorkbenchViewStateReportService().build_all_parts()
        return {
            "view_state_report": _ref("workbench_view_state_report", parts["report"].report_id, "v0.26.1"),
            "view_state": _ref("workbench_view_state", parts["view_state"].view_state_id, "v0.26.1"),
        }

    def load_snapshot_export_panel_model(self) -> dict[str, Any] | None:
        if not self.snapshot_export_panel_available:
            return None
        return _ref("workbench_panel", "workbench_panel:snapshot_export", "v0.26.1")

    def load_command_surface_report_if_available(self) -> list[dict[str, Any]]:
        return [_ref("workbench_command_surface_report", "workbench_command_surface_report:v0.26.7:existing", "v0.26.7")] if self.command_surface_available else []

    def load_dashboard_report_if_available(self) -> list[dict[str, Any]]:
        return [_ref("workbench_run_dashboard_report", "workbench_run_dashboard_report:v0.26.6:existing", "v0.26.6")] if self.dashboard_available else []

    def load_approval_console_report_if_available(self) -> list[dict[str, Any]]:
        return [_ref("workbench_approval_console_report", "workbench_approval_console_report:v0.26.5:existing", "v0.26.5")] if self.approval_console_available else []

    def load_evidence_inspector_report_if_available(self) -> list[dict[str, Any]]:
        return [_ref("workbench_evidence_inspector_report", "workbench_evidence_inspector_report:v0.26.4:existing", "v0.26.4")] if self.evidence_inspector_available else []

    def load_provider_browser_report_if_available(self) -> list[dict[str, Any]]:
        return [_ref("workbench_provider_browser_report", "workbench_provider_browser_report:v0.26.3:existing", "v0.26.3")] if self.provider_browser_available else []

    def load_trace_explorer_report_if_available(self) -> list[dict[str, Any]]:
        return [_ref("workbench_trace_explorer_report", "workbench_trace_explorer_report:v0.26.2:existing", "v0.26.2")] if self.trace_explorer_available else []

    def load_trace_telemetry_report_if_available(self) -> list[dict[str, Any]]:
        return [_ref("agent_trace_telemetry_report", "agent_trace_telemetry_report:v0.25.8:existing", "v0.25.8")] if self.trace_telemetry_available else []

    def load_pig_guidance_refs_if_available(self) -> list[dict[str, Any]]:
        if not self.pig_guidance_available:
            return []
        return [_ref("pig_guidance", "pig_guidance:snapshot_refs_only"), _ref("pig_guidance", "pig_guidance:export_redaction")]


class WorkbenchSnapshotPolicyService:
    def build_policy(self) -> WorkbenchSnapshotPolicy:
        return WorkbenchSnapshotPolicy(policy_id="workbench_snapshot_policy:v0.26.8")


class WorkbenchSnapshotRequestService:
    def build_request(
        self,
        source_service: WorkbenchSnapshotPrerequisiteSourceService,
        *,
        report_id: str | None = None,
        strictness: str = "standard",
    ) -> WorkbenchSnapshotRequest:
        view_state = source_service.load_workbench_view_state() or {}
        panel = source_service.load_snapshot_export_panel_model()
        command_refs = source_service.load_command_surface_report_if_available()
        dashboard_refs = source_service.load_dashboard_report_if_available()
        approval_refs = source_service.load_approval_console_report_if_available()
        evidence_refs = source_service.load_evidence_inspector_report_if_available()
        provider_refs = source_service.load_provider_browser_report_if_available()
        trace_refs = source_service.load_trace_explorer_report_if_available()
        telemetry_refs = source_service.load_trace_telemetry_report_if_available()
        pig_refs = source_service.load_pig_guidance_refs_if_available()
        source_refs = command_refs + dashboard_refs + approval_refs + evidence_refs + provider_refs + trace_refs + telemetry_refs + pig_refs
        return WorkbenchSnapshotRequest(
            request_id=report_id or "workbench_snapshot_request:v0.26.8",
            view_state_report_id=(view_state.get("view_state_report") or {}).get("id"),
            view_state_id=(view_state.get("view_state") or {}).get("id"),
            snapshot_export_panel_id=(panel or {}).get("id"),
            command_surface_report_id=(command_refs[0]["id"] if command_refs else None),
            dashboard_report_id=(dashboard_refs[0]["id"] if dashboard_refs else None),
            approval_console_report_id=(approval_refs[0]["id"] if approval_refs else None),
            evidence_inspector_report_id=(evidence_refs[0]["id"] if evidence_refs else None),
            provider_browser_report_id=(provider_refs[0]["id"] if provider_refs else None),
            trace_explorer_report_id=(trace_refs[0]["id"] if trace_refs else None),
            trace_telemetry_report_id=(telemetry_refs[0]["id"] if telemetry_refs else None),
            selected_ref_candidates=source_refs,
            requested_export_profile="refs_only",
            source_refs=source_refs,
            strictness=strictness,
        )


class WorkbenchSnapshotSourceViewService:
    def build_source_view(
        self,
        source_service: WorkbenchSnapshotPrerequisiteSourceService,
        request: WorkbenchSnapshotRequest,
    ) -> WorkbenchSnapshotSourceView:
        report_refs = [
            *source_service.load_command_surface_report_if_available(),
            *source_service.load_dashboard_report_if_available(),
            *source_service.load_approval_console_report_if_available(),
            *source_service.load_evidence_inspector_report_if_available(),
            *source_service.load_provider_browser_report_if_available(),
            *source_service.load_trace_explorer_report_if_available(),
        ]
        trace_refs = source_service.load_trace_explorer_report_if_available() + source_service.load_trace_telemetry_report_if_available()
        pig_refs = source_service.load_pig_guidance_refs_if_available()
        mandatory = bool(source_service.load_workbench_view_state()) and bool(source_service.load_snapshot_export_panel_model())
        source_status = "complete" if mandatory and report_refs else "partial"
        if request.strictness == "strict" and not mandatory:
            source_status = "missing"
        return WorkbenchSnapshotSourceView(
            source_view_id="workbench_snapshot_source_view:v0.26.8",
            workbench_report_refs=report_refs,
            command_candidate_refs=[_ref("workbench_command_candidate", "workbench_command_candidate:v0.26.7:existing", "v0.26.7")] if source_service.command_surface_available else [],
            decision_point_refs=[_ref("decision_point", "decision_point:command_surface:v0.26.7", "v0.26.7")],
            skill_candidate_refs=[_ref("workbench_skill_candidate", "workbench_skill_candidate:v0.26.7:existing", "v0.26.7")],
            action_candidate_refs=[_ref("workbench_action_candidate", "workbench_action_candidate:v0.26.7:existing", "v0.26.7")],
            route_rationale_refs=[_ref("workbench_route_rationale", "workbench_route_rationale:v0.25.4:existing", "v0.25.4")],
            provider_rationale_refs=[_ref("workbench_provider_rationale", "workbench_provider_rationale:v0.26.3:existing", "v0.26.3")],
            safety_rationale_refs=[_ref("workbench_safety_rationale", "workbench_safety_rationale:v0.26.5:existing", "v0.26.5")],
            pig_guidance_refs=pig_refs,
            human_intervention_refs=[_ref("human_intervention", "human_intervention:v0.26.5:existing", "v0.26.5")],
            approval_decision_refs=[_ref("workbench_approval_decision", "workbench_approval_decision:v0.26.5:existing", "v0.26.5")],
            failure_cause_refs=[_ref("failure_cause", "failure_cause:v0.26.6:existing", "v0.26.6")],
            trace_refs=trace_refs,
            ocel_projection_refs=[_ref("agent_turn_ocel_projection", "agent_turn_ocel_projection:v0.25.8:existing", "v0.25.8")],
            source_status=source_status,
            evidence_refs=request.source_refs,
        )


class WorkbenchSnapshotSelectionPolicyService:
    def build_policy(self) -> WorkbenchSnapshotSelectionPolicy:
        return WorkbenchSnapshotSelectionPolicy(policy_id="workbench_snapshot_selection_policy:v0.26.8")


class WorkbenchSnapshotSelectionService:
    def build_selection(self, source_view: WorkbenchSnapshotSourceView) -> WorkbenchSnapshotSelection:
        selected = (
            source_view.workbench_report_refs
            + source_view.command_candidate_refs
            + source_view.decision_point_refs
            + source_view.skill_candidate_refs
            + source_view.action_candidate_refs
            + source_view.route_rationale_refs
            + source_view.provider_rationale_refs
            + source_view.safety_rationale_refs
            + source_view.pig_guidance_refs
            + source_view.human_intervention_refs
            + source_view.approval_decision_refs
            + source_view.failure_cause_refs
            + source_view.trace_refs
        )
        categories = sorted({item["type"] for item in selected})
        return WorkbenchSnapshotSelection(
            selection_id="workbench_snapshot_selection:v0.26.8",
            selected_refs=selected,
            selected_ref_count=len(selected),
            selected_categories=categories,
            omitted_refs=[_ref("raw_data_category", item) for item in EXCLUDED_RAW_DATA_CATEGORIES],
            omission_reasons=[f"{item} excluded by redaction policy" for item in EXCLUDED_RAW_DATA_CATEGORIES],
            selection_status="ready" if selected else "partial",
            evidence_refs=selected,
        )


class WorkbenchSnapshotExportRefService:
    def build_decision_point_export_refs(self, source_view: WorkbenchSnapshotSourceView) -> list[WorkbenchDecisionPointExportRef]:
        return [
            WorkbenchDecisionPointExportRef(
                export_ref_id="workbench_decision_point_export_ref:command_surface",
                decision_ref=source_view.decision_point_refs[0],
                decision_type="command_surface_decision",
                decision_outcome="recorded_ref_only",
                rationale_refs=source_view.safety_rationale_refs,
                evidence_refs=source_view.evidence_refs,
            )
        ] if source_view.decision_point_refs else []

    def build_skill_candidate_export_refs(self, source_view: WorkbenchSnapshotSourceView) -> list[WorkbenchSkillCandidateExportRef]:
        return [
            WorkbenchSkillCandidateExportRef(
                export_ref_id="workbench_skill_candidate_export_ref:command_surface",
                skill_candidate_ref=source_view.skill_candidate_refs[0],
                skill_id="skill:workbench_command_surface_use",
                skill_name="workbench_command_surface_use",
                selection_refs=source_view.skill_candidate_refs,
                pig_guidance_refs=source_view.pig_guidance_refs,
                evidence_refs=source_view.evidence_refs,
            )
        ] if source_view.skill_candidate_refs else []

    def build_action_candidate_export_refs(self, source_view: WorkbenchSnapshotSourceView) -> list[WorkbenchActionCandidateExportRef]:
        return [
            WorkbenchActionCandidateExportRef(
                export_ref_id="workbench_action_candidate_export_ref:inspect",
                action_candidate_ref=source_view.action_candidate_refs[0],
                action_type="inspect",
                rationale_refs=source_view.decision_point_refs,
                risk_refs=source_view.safety_rationale_refs,
                approval_refs=source_view.approval_decision_refs,
                evidence_refs=source_view.evidence_refs,
            )
        ] if source_view.action_candidate_refs else []

    def build_route_rationale_export_refs(self, source_view: WorkbenchSnapshotSourceView) -> list[WorkbenchRouteRationaleExportRef]:
        return [
            WorkbenchRouteRationaleExportRef(
                export_ref_id="workbench_route_rationale_export_ref:route",
                route_ref=source_view.route_rationale_refs[0],
                route_kind="inspection_only",
                selection_rationale_refs=source_view.route_rationale_refs,
                compatibility_refs=source_view.provider_rationale_refs,
                evidence_refs=source_view.evidence_refs,
            )
        ] if source_view.route_rationale_refs else []

    def build_provider_rationale_export_refs(self, source_view: WorkbenchSnapshotSourceView) -> list[WorkbenchProviderRationaleExportRef]:
        return [
            WorkbenchProviderRationaleExportRef(
                export_ref_id="workbench_provider_rationale_export_ref:provider",
                provider_ref=source_view.provider_rationale_refs[0],
                provider_id="provider_ref_only",
                capability_id="capability_ref_only",
                rationale_refs=source_view.provider_rationale_refs,
                boundary_risk_refs=source_view.safety_rationale_refs,
                readiness_refs=source_view.workbench_report_refs,
                evidence_refs=source_view.evidence_refs,
            )
        ] if source_view.provider_rationale_refs else []

    def build_safety_rationale_export_refs(self, source_view: WorkbenchSnapshotSourceView) -> list[WorkbenchSafetyRationaleExportRef]:
        return [
            WorkbenchSafetyRationaleExportRef(
                export_ref_id="workbench_safety_rationale_export_ref:safety",
                safety_ref=source_view.safety_rationale_refs[0],
                gate_outcome="recorded_ref_only",
                safety_rule_refs=source_view.safety_rationale_refs,
                risk_refs=source_view.failure_cause_refs,
                evidence_refs=source_view.evidence_refs,
            )
        ] if source_view.safety_rationale_refs else []

    def build_pig_guidance_export_refs(self, source_view: WorkbenchSnapshotSourceView) -> list[WorkbenchPIGGuidanceExportRef]:
        return [
            WorkbenchPIGGuidanceExportRef(
                export_ref_id=f"workbench_pig_guidance_export_ref:{index}",
                pig_guidance_ref=ref,
                guidance_type="rationale",
                guidance_summary="PIG guidance is exported as a ref, not memory, policy, or execution authority.",
                related_refs=source_view.command_candidate_refs,
                evidence_refs=[ref],
            )
            for index, ref in enumerate(source_view.pig_guidance_refs, start=1)
        ]

    def build_human_intervention_export_refs(self, source_view: WorkbenchSnapshotSourceView) -> list[WorkbenchHumanInterventionExportRef]:
        return [
            WorkbenchHumanInterventionExportRef(
                export_ref_id="workbench_human_intervention_export_ref:approval",
                intervention_ref=source_view.human_intervention_refs[0],
                intervention_type="approval_required",
                reason="Human intervention ref is preserved for inspection only.",
                approval_ref=source_view.approval_decision_refs[0] if source_view.approval_decision_refs else None,
                evidence_refs=source_view.evidence_refs,
            )
        ] if source_view.human_intervention_refs else []

    def build_approval_decision_export_refs(self, source_view: WorkbenchSnapshotSourceView) -> list[WorkbenchApprovalDecisionExportRef]:
        return [
            WorkbenchApprovalDecisionExportRef(
                export_ref_id="workbench_approval_decision_export_ref:approval",
                approval_decision_ref=source_view.approval_decision_refs[0],
                decision_type="recorded_ref_only",
                decision_reason="Approval decision exported as refs only.",
                scope_refs=[_ref("workbench_approval_scope", "workbench_approval_scope:v0.26.5:existing", "v0.26.5")],
                expiry_refs=[_ref("workbench_approval_expiry", "workbench_approval_expiry:v0.26.5:existing", "v0.26.5")],
                evidence_refs=source_view.evidence_refs,
            )
        ] if source_view.approval_decision_refs else []

    def build_failure_cause_export_refs(self, source_view: WorkbenchSnapshotSourceView) -> list[WorkbenchFailureCauseExportRef]:
        return [
            WorkbenchFailureCauseExportRef(
                export_ref_id="workbench_failure_cause_export_ref:failure",
                failure_cause_ref=source_view.failure_cause_refs[0],
                failure_category="descriptive",
                failure_stage="workbench",
                recovery_guidance_refs=source_view.pig_guidance_refs,
                evidence_refs=source_view.evidence_refs,
            )
        ] if source_view.failure_cause_refs else []

    def build_command_candidate_export_refs(self, source_view: WorkbenchSnapshotSourceView) -> list[WorkbenchCommandCandidateExportRef]:
        return [
            WorkbenchCommandCandidateExportRef(
                export_ref_id="workbench_command_candidate_export_ref:command",
                command_candidate_ref=source_view.command_candidate_refs[0],
                command_type="inspect_dashboard",
                boundary_trace_refs=[_ref("workbench_command_boundary_trace", "workbench_command_boundary_trace:v0.26.7:existing", "v0.26.7")],
                decision_record_refs=[_ref("workbench_command_decision_record", "workbench_command_decision_record:v0.26.7:existing", "v0.26.7")],
                do_nothing_candidate_refs=[_ref("workbench_do_nothing_candidate", "workbench_do_nothing_candidate:v0.26.7:existing", "v0.26.7")],
                evidence_refs=source_view.evidence_refs,
            )
        ] if source_view.command_candidate_refs else []


class WorkbenchSnapshotRefBundleService:
    def build_ref_bundle(self, source_view: WorkbenchSnapshotSourceView) -> WorkbenchSnapshotRefBundle:
        ref_service = WorkbenchSnapshotExportRefService()
        decision_refs = ref_service.build_decision_point_export_refs(source_view)
        skill_refs = ref_service.build_skill_candidate_export_refs(source_view)
        action_refs = ref_service.build_action_candidate_export_refs(source_view)
        route_refs = ref_service.build_route_rationale_export_refs(source_view)
        provider_refs = ref_service.build_provider_rationale_export_refs(source_view)
        safety_refs = ref_service.build_safety_rationale_export_refs(source_view)
        pig_refs = ref_service.build_pig_guidance_export_refs(source_view)
        intervention_refs = ref_service.build_human_intervention_export_refs(source_view)
        approval_refs = ref_service.build_approval_decision_export_refs(source_view)
        failure_refs = ref_service.build_failure_cause_export_refs(source_view)
        command_refs = ref_service.build_command_candidate_export_refs(source_view)
        all_refs = decision_refs + skill_refs + action_refs + route_refs + provider_refs + safety_refs + pig_refs + intervention_refs + approval_refs + failure_refs + command_refs
        return WorkbenchSnapshotRefBundle(
            ref_bundle_id="workbench_snapshot_ref_bundle:v0.26.8",
            decision_point_export_refs=decision_refs,
            skill_candidate_export_refs=skill_refs,
            action_candidate_export_refs=action_refs,
            route_rationale_export_refs=route_refs,
            provider_rationale_export_refs=provider_refs,
            safety_rationale_export_refs=safety_refs,
            pig_guidance_export_refs=pig_refs,
            human_intervention_export_refs=intervention_refs,
            approval_decision_export_refs=approval_refs,
            failure_cause_export_refs=failure_refs,
            command_candidate_export_refs=command_refs,
            ref_count=len(all_refs),
            bundle_status="ready" if all_refs else "partial",
            evidence_refs=source_view.evidence_refs,
        )


class WorkbenchSnapshotRedactionPolicyService:
    def build_policy(self) -> WorkbenchSnapshotRedactionPolicy:
        return WorkbenchSnapshotRedactionPolicy(policy_id="workbench_snapshot_redaction_policy:v0.26.8")


class WorkbenchSnapshotRedactionReportService:
    def build_report(self, policy: WorkbenchSnapshotRedactionPolicy, preserved_ref_count: int) -> WorkbenchSnapshotRedactionReport:
        return WorkbenchSnapshotRedactionReport(
            redaction_report_id="workbench_snapshot_redaction_report:v0.26.8",
            redaction_policy_id=policy.policy_id,
            redacted_raw_transcript_count=1,
            redacted_raw_provider_output_count=1,
            redacted_raw_secret_count=1,
            redacted_credential_count=1,
            redacted_private_path_count=1,
            preserved_ref_count=preserved_ref_count,
            preserved_summary_count=preserved_ref_count,
            redaction_status="ready",
        )


class WorkbenchSnapshotManifestService:
    def build_manifest(
        self,
        source_view: WorkbenchSnapshotSourceView,
        ref_bundle: WorkbenchSnapshotRefBundle,
        redaction_report: WorkbenchSnapshotRedactionReport,
        *,
        snapshot_id: str | None = None,
    ) -> WorkbenchSnapshotManifest:
        return WorkbenchSnapshotManifest(
            manifest_id="workbench_snapshot_manifest:v0.26.8",
            snapshot_id=snapshot_id,
            included_report_refs=source_view.workbench_report_refs,
            included_trace_refs=source_view.trace_refs,
            included_decision_point_refs=source_view.decision_point_refs,
            included_candidate_refs=source_view.command_candidate_refs + source_view.skill_candidate_refs + source_view.action_candidate_refs,
            included_approval_refs=source_view.approval_decision_refs,
            included_failure_refs=source_view.failure_cause_refs,
            included_pig_guidance_refs=source_view.pig_guidance_refs,
            excluded_raw_data_categories=EXCLUDED_RAW_DATA_CATEGORIES,
            redaction_report_ref=_model_ref("workbench_snapshot_redaction_report", redaction_report, "redaction_report_id"),
            manifest_status="ready" if ref_bundle.ref_count else "partial",
            evidence_refs=source_view.evidence_refs,
        )


class WorkbenchEventQualityReportService:
    def build_report(self, source_view: WorkbenchSnapshotSourceView, *, snapshot_id: str | None = None) -> WorkbenchEventQualityReport:
        coverage = 1.0 if source_view.source_status == "complete" else 0.5
        missing = [] if coverage == 1.0 else ["partial_source_refs"]
        return WorkbenchEventQualityReport(
            event_quality_report_id="workbench_event_quality_report:v0.26.8",
            source_snapshot_id=snapshot_id,
            decision_point_coverage=coverage,
            skill_candidate_coverage=coverage,
            action_candidate_coverage=coverage,
            route_rationale_coverage=coverage,
            provider_rationale_coverage=coverage,
            safety_rationale_coverage=coverage,
            pig_guidance_coverage=coverage if source_view.pig_guidance_refs else 0.0,
            approval_decision_coverage=coverage,
            failure_cause_coverage=coverage,
            human_intervention_coverage=coverage,
            missing_quality_dimensions=missing,
            quality_status="ready" if not missing else "partial",
            evidence_refs=source_view.evidence_refs,
        )


class WorkbenchTraceCoverageReportService:
    def build_report(self, source_view: WorkbenchSnapshotSourceView, *, snapshot_id: str | None = None) -> WorkbenchTraceCoverageReport:
        trace_count = len(source_view.trace_refs)
        return WorkbenchTraceCoverageReport(
            trace_coverage_report_id="workbench_trace_coverage_report:v0.26.8",
            source_snapshot_id=snapshot_id,
            trace_ref_count=trace_count,
            stage_trace_coverage={"intent": True, "safety": True, "routing": True, "provider": True, "response": True},
            decision_trace_coverage={"approval": bool(source_view.approval_decision_refs), "command": bool(source_view.command_candidate_refs)},
            provider_trace_coverage=bool(source_view.provider_rationale_refs),
            response_trace_coverage=True,
            approval_trace_coverage=bool(source_view.approval_decision_refs),
            command_trace_coverage=bool(source_view.command_candidate_refs),
            coverage_status="ready" if trace_count else "partial",
            evidence_refs=source_view.trace_refs,
        )


class WorkbenchSnapshotService:
    def build_snapshot(
        self,
        source_view: WorkbenchSnapshotSourceView,
        selection: WorkbenchSnapshotSelection,
        manifest: WorkbenchSnapshotManifest,
        ref_bundle: WorkbenchSnapshotRefBundle,
        redaction_report: WorkbenchSnapshotRedactionReport,
        event_quality_report: WorkbenchEventQualityReport,
        trace_coverage_report: WorkbenchTraceCoverageReport,
    ) -> WorkbenchSnapshot:
        return WorkbenchSnapshot(
            snapshot_id="workbench_snapshot:v0.26.8",
            created_at=utc_now_iso(),
            snapshot_name="Workbench Snapshot / OCEL Export",
            source_view_id=source_view.source_view_id,
            selection_id=selection.selection_id,
            manifest_id=manifest.manifest_id,
            ref_bundle_id=ref_bundle.ref_bundle_id,
            redaction_report_id=redaction_report.redaction_report_id,
            reproducibility_packet_id="workbench_reproducibility_packet:v0.26.8",
            event_quality_report_id=event_quality_report.event_quality_report_id,
            trace_coverage_report_id=trace_coverage_report.trace_coverage_report_id,
            snapshot_status="ready" if selection.selected_refs and ref_bundle.ref_count else "partial",
            evidence_refs=selection.selected_refs,
        )


class WorkbenchOCELExportPolicyService:
    def build_policy(self) -> WorkbenchOCELExportPolicy:
        return WorkbenchOCELExportPolicy(policy_id="workbench_ocel_export_policy:v0.26.8")


class WorkbenchExportBoundaryDescriptorService:
    def build_descriptor(self) -> WorkbenchExportBoundaryDescriptor:
        return WorkbenchExportBoundaryDescriptor(
            boundary_descriptor_id="workbench_export_boundary_descriptor:v0.26.8",
            export_boundary_type="sanitized_ocel_package",
            boundary_summary="Exports internal refs-only OCEL package descriptors without external sync or runtime adapter calls.",
            allowed_targets=["internal_refs_only", "sanitized_ocel_package"],
            forbidden_targets=["external_sync", "external_adapter", "raw_transcript", "raw_provider_output", "memory_promotion"],
            evidence_refs=[_ref("workbench_snapshot_policy", "workbench_snapshot_policy:v0.26.8")],
        )


class WorkbenchOCELExportManifestService:
    def build_manifest(
        self,
        snapshot: WorkbenchSnapshot,
        boundary: WorkbenchExportBoundaryDescriptor,
        *,
        export_package_id: str | None = None,
    ) -> WorkbenchOCELExportManifest:
        return WorkbenchOCELExportManifest(
            export_manifest_id="workbench_ocel_export_manifest:v0.26.8",
            export_package_id=export_package_id,
            snapshot_ref=_model_ref("workbench_snapshot", snapshot, "snapshot_id"),
            included_object_types=WORKBENCH_SNAPSHOT_EXPORT_OBJECT_TYPES,
            included_event_types=WORKBENCH_SNAPSHOT_EXPORT_EVENT_TYPES,
            included_relation_types=WORKBENCH_SNAPSHOT_EXPORT_RELATION_TYPES,
            included_effect_types=WORKBENCH_SNAPSHOT_EXPORT_EFFECT_TYPES,
            excluded_raw_categories=EXCLUDED_RAW_DATA_CATEGORIES,
            export_boundary_descriptor_ref=_model_ref("workbench_export_boundary_descriptor", boundary, "boundary_descriptor_id"),
            manifest_status="ready",
            evidence_refs=snapshot.evidence_refs,
        )


class WorkbenchOCELExportPackageService:
    def build_package(self, snapshot: WorkbenchSnapshot, export_manifest: WorkbenchOCELExportManifest) -> WorkbenchOCELExportPackage:
        return WorkbenchOCELExportPackage(
            export_package_id="workbench_ocel_export_package:v0.26.8",
            snapshot_id=snapshot.snapshot_id,
            export_manifest_id=export_manifest.export_manifest_id,
            object_type_refs=export_manifest.included_object_types,
            event_type_refs=export_manifest.included_event_types,
            relation_type_refs=export_manifest.included_relation_types,
            effect_type_refs=export_manifest.included_effect_types,
            exported_object_count=len(export_manifest.included_object_types),
            exported_event_count=len(export_manifest.included_event_types),
            exported_relation_count=len(export_manifest.included_relation_types),
            export_status="ready",
            evidence_refs=snapshot.evidence_refs,
        )


class WorkbenchReproducibilityPacketService:
    def build_packet(
        self,
        snapshot: WorkbenchSnapshot,
        source_view: WorkbenchSnapshotSourceView,
        export_package: WorkbenchOCELExportPackage,
    ) -> WorkbenchReproducibilityPacket:
        return WorkbenchReproducibilityPacket(
            reproducibility_packet_id="workbench_reproducibility_packet:v0.26.8",
            snapshot_id=snapshot.snapshot_id,
            required_report_refs=source_view.workbench_report_refs,
            required_boundary_refs=[_ref("workbench_export_boundary_descriptor", "workbench_export_boundary_descriptor:v0.26.8")],
            command_candidate_refs=source_view.command_candidate_refs,
            approval_decision_refs=source_view.approval_decision_refs,
            export_package_ref=_model_ref("workbench_ocel_export_package", export_package, "export_package_id"),
            reproducibility_summary="Refs-only reproducibility packet; it grants no rerun permission.",
            reproducibility_status="ready" if source_view.workbench_report_refs else "partial",
            evidence_refs=snapshot.evidence_refs,
        )


class WorkbenchSnapshotExportFindingService:
    BLOCKED_FINDINGS = {
        "memory_candidate_extraction_attempted",
        "memory_promotion_attempted",
        "persistent_memory_write_attempted",
        "persona_mutation_attempted",
        "raw_transcript_export_attempted",
        "raw_provider_output_export_attempted",
        "raw_secret_export_attempted",
        "credential_export_attempted",
        "private_full_path_export_attempted",
        "external_sync_attempted",
        "external_adapter_detected",
        "pm4py_runtime_dependency_detected",
        "ocpa_runtime_dependency_detected",
        "command_execution_attempted",
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
        "pig_guidance_as_memory_detected",
        "pig_policy_mutation_detected",
        "pig_execution_detected",
        "schumpeter_split_detected",
        "opencode_runtime_dependency_detected",
        "openclaw_runtime_dependency_detected",
        "hermes_runtime_dependency_detected",
        "llm_judge_detected",
    }

    CREATED_FINDINGS = [
        "snapshot_created",
        "snapshot_manifest_created",
        "snapshot_ref_bundle_created",
        "decision_point_export_ref_created",
        "skill_candidate_export_ref_created",
        "action_candidate_export_ref_created",
        "route_rationale_export_ref_created",
        "provider_rationale_export_ref_created",
        "safety_rationale_export_ref_created",
        "pig_guidance_export_ref_created",
        "human_intervention_export_ref_created",
        "approval_decision_export_ref_created",
        "failure_cause_export_ref_created",
        "command_candidate_export_ref_created",
        "ocel_export_package_created",
        "event_quality_report_created",
        "trace_coverage_report_created",
        "redaction_report_created",
        "reproducibility_packet_created",
        "export_boundary_descriptor_created",
    ]

    def build_findings(
        self,
        *,
        source_service: WorkbenchSnapshotPrerequisiteSourceService,
        selection: WorkbenchSnapshotSelection,
        strictness: str = "standard",
        extra_findings: list[str] | None = None,
    ) -> list[WorkbenchSnapshotExportFinding]:
        findings: list[WorkbenchSnapshotExportFinding] = []
        if not source_service.view_state_available:
            findings.append(self._finding("warning", "missing_workbench_view_state", "Workbench view state is missing."))
        if not source_service.snapshot_export_panel_available:
            severity = "error" if strictness == "strict" else "warning"
            findings.append(self._finding(severity, "missing_snapshot_export_panel", "Snapshot export panel model is missing."))
        if not source_service.command_surface_available:
            findings.append(self._finding("warning", "missing_command_surface_report", "Command surface report is missing."))
        if not source_service.dashboard_available:
            findings.append(self._finding("warning", "missing_dashboard_report", "Dashboard report is missing."))
        if not source_service.trace_explorer_available:
            findings.append(self._finding("warning", "missing_trace_report", "Trace report is missing."))
        if not selection.selected_refs:
            findings.append(self._finding("error", "missing_selected_refs", "Selected refs are missing."))
        for finding_type in self.CREATED_FINDINGS:
            findings.append(self._finding("info", finding_type, finding_type))
        for finding_type in extra_findings or []:
            severity = "critical" if finding_type in self.BLOCKED_FINDINGS else "warning"
            findings.append(self._finding(severity, finding_type, finding_type))
        if not findings:
            findings.append(self._finding("info", "ok", "Workbench snapshot/export report is complete."))
        return findings

    def _finding(self, severity: str, finding_type: str, message: str) -> WorkbenchSnapshotExportFinding:
        return WorkbenchSnapshotExportFinding(
            finding_id=f"workbench_snapshot_export_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            withdrawal_condition="Withdraw if snapshot/export policy or source evidence changes.",
        )


class WorkbenchSnapshotExportReportService:
    def build_all_parts(
        self,
        *,
        report_id: str | None = None,
        strictness: str = "standard",
        extra_findings: list[str] | None = None,
        view_state_available: bool = True,
        snapshot_export_panel_available: bool = True,
        command_surface_available: bool = True,
        dashboard_available: bool = True,
        approval_console_available: bool = True,
        evidence_inspector_available: bool = True,
        provider_browser_available: bool = True,
        trace_explorer_available: bool = True,
        trace_telemetry_available: bool = True,
        pig_guidance_available: bool = True,
    ) -> dict[str, Any]:
        source_service = WorkbenchSnapshotPrerequisiteSourceService(
            view_state_available=view_state_available,
            snapshot_export_panel_available=snapshot_export_panel_available,
            command_surface_available=command_surface_available,
            dashboard_available=dashboard_available,
            approval_console_available=approval_console_available,
            evidence_inspector_available=evidence_inspector_available,
            provider_browser_available=provider_browser_available,
            trace_explorer_available=trace_explorer_available,
            trace_telemetry_available=trace_telemetry_available,
            pig_guidance_available=pig_guidance_available,
        )
        snapshot_policy = WorkbenchSnapshotPolicyService().build_policy()
        request = WorkbenchSnapshotRequestService().build_request(source_service, report_id=report_id, strictness=strictness)
        source_view = WorkbenchSnapshotSourceViewService().build_source_view(source_service, request)
        selection_policy = WorkbenchSnapshotSelectionPolicyService().build_policy()
        selection = WorkbenchSnapshotSelectionService().build_selection(source_view)
        ref_bundle = WorkbenchSnapshotRefBundleService().build_ref_bundle(source_view)
        redaction_policy = WorkbenchSnapshotRedactionPolicyService().build_policy()
        redaction_report = WorkbenchSnapshotRedactionReportService().build_report(redaction_policy, selection.selected_ref_count)
        event_quality = WorkbenchEventQualityReportService().build_report(source_view, snapshot_id="workbench_snapshot:v0.26.8")
        trace_coverage = WorkbenchTraceCoverageReportService().build_report(source_view, snapshot_id="workbench_snapshot:v0.26.8")
        manifest = WorkbenchSnapshotManifestService().build_manifest(
            source_view,
            ref_bundle,
            redaction_report,
            snapshot_id="workbench_snapshot:v0.26.8",
        )
        snapshot = WorkbenchSnapshotService().build_snapshot(
            source_view,
            selection,
            manifest,
            ref_bundle,
            redaction_report,
            event_quality,
            trace_coverage,
        )
        boundary = WorkbenchExportBoundaryDescriptorService().build_descriptor()
        ocel_policy = WorkbenchOCELExportPolicyService().build_policy()
        ocel_manifest = WorkbenchOCELExportManifestService().build_manifest(
            snapshot,
            boundary,
            export_package_id="workbench_ocel_export_package:v0.26.8",
        )
        ocel_package = WorkbenchOCELExportPackageService().build_package(snapshot, ocel_manifest)
        reproducibility = WorkbenchReproducibilityPacketService().build_packet(snapshot, source_view, ocel_package)
        findings = WorkbenchSnapshotExportFindingService().build_findings(
            source_service=source_service,
            selection=selection,
            strictness=strictness,
            extra_findings=extra_findings,
        )
        status = self._report_status(findings, strictness)
        if strictness == "strict" and (not source_service.view_state_available or not source_service.snapshot_export_panel_available):
            status = "failed"
        ready = status in {"passed", "warning"} and bool(selection.selected_refs and ref_bundle.ref_count)
        report = WorkbenchSnapshotExportReport(
            report_id=report_id or "workbench_snapshot_export_report:v0.26.8",
            created_at=utc_now_iso(),
            snapshot_policy=snapshot_policy,
            request=request,
            source_view=source_view,
            selection_policy=selection_policy,
            selection=selection,
            snapshot=snapshot,
            snapshot_manifest=manifest,
            ref_bundle=ref_bundle,
            ocel_export_policy=ocel_policy,
            ocel_export_package=ocel_package,
            ocel_export_manifest=ocel_manifest,
            event_quality_report=event_quality,
            trace_coverage_report=trace_coverage,
            redaction_policy=redaction_policy,
            redaction_report=redaction_report,
            reproducibility_packet=reproducibility,
            export_boundary_descriptor=boundary,
            findings=findings,
            report_status=status,
            ready_for_v0_26_9=ready,
            snapshot_created=True,
            snapshot_manifest_created=True,
            ref_bundle_created=True,
            ocel_export_package_created=True,
            ocel_export_manifest_created=True,
            event_quality_report_created=True,
            trace_coverage_report_created=True,
            redaction_report_created=True,
            reproducibility_packet_created=True,
            export_boundary_descriptor_created=True,
            limitations=[
                "v0.26.8 creates refs-only snapshot/export artifacts.",
                "No raw data export, memory promotion, external sync, or runtime adapter is implemented.",
            ],
            withdrawal_conditions=[
                "Withdraw readiness if raw transcript/provider/secret/credential/private path export is added.",
                "Withdraw readiness if memory promotion, external sync, process-mining runtime dependency, or execution is added.",
            ],
        )
        return {
            "snapshot_policy": snapshot_policy,
            "request": request,
            "source_view": source_view,
            "selection_policy": selection_policy,
            "selection": selection,
            "snapshot": snapshot,
            "snapshot_manifest": manifest,
            "ref_bundle": ref_bundle,
            "ocel_export_policy": ocel_policy,
            "ocel_export_package": ocel_package,
            "ocel_export_manifest": ocel_manifest,
            "event_quality_report": event_quality,
            "trace_coverage_report": trace_coverage,
            "redaction_policy": redaction_policy,
            "redaction_report": redaction_report,
            "reproducibility_packet": reproducibility,
            "export_boundary_descriptor": boundary,
            "findings": findings,
            "report": report,
        }

    def _report_status(self, findings: list[WorkbenchSnapshotExportFinding], strictness: str) -> str:
        if any(finding.finding_type in WorkbenchSnapshotExportFindingService.BLOCKED_FINDINGS for finding in findings):
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
            "version": WORKBENCH_SNAPSHOT_EXPORT_VERSION,
            "layer": WORKBENCH_SNAPSHOT_EXPORT_LAYER,
            "subject": "workbench_snapshot_ocel_export",
            "principles": [
                "Workbench Snapshot is not memory promotion",
                "Snapshot manifest is not memory index",
                "OCEL export package is not raw transcript export",
                "OCEL export package is not raw provider output export",
                "OCEL export package is not external sync",
                "Reproducibility packet is not rerun permission",
                "Event quality report is descriptive, not automatic optimization",
                "Redaction report documents exclusion, not source deletion",
                "Export boundary is not runtime adapter",
                "PIG guidance export ref is not PIG memory",
            ],
            "safety_boundary": {
                "snapshot_created": "conditional",
                "snapshot_manifest_created": "conditional",
                "ref_bundle_created": "conditional",
                "ocel_export_package_created": "conditional",
                "event_quality_report_created": "conditional",
                "trace_coverage_report_created": "conditional",
                "redaction_report_created": "conditional",
                "reproducibility_packet_created": "conditional",
                "memory_candidate_created": False,
                "memory_promoted": False,
                "persistent_memory_written": False,
                "persona_mutated": False,
                "raw_transcript_exported": False,
                "raw_provider_output_exported": False,
                "raw_secret_exported": False,
                "credential_exported": False,
                "private_full_path_exported": False,
                "external_sync_performed": False,
                "external_provider_adapter_implemented": False,
                "vendor_adapter_implemented": False,
                "pm4py_runtime_dependency_added": False,
                "ocpa_runtime_dependency_added": False,
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
                "pig_memory_promoted": False,
                "pig_policy_mutated": False,
                "pig_executed": False,
                "schumpeter_split_introduced": False,
                "llm_judge_enabled": False,
            },
            "future_direction": [
                "v0.26.9 workspace agent workbench consolidation",
                "v0.27 memory candidate and continuity",
                "v0.28 public alpha / Schumpeter split preparation",
                "v0.29+ external provider adapters",
                "v0.30+ external agent dominion bridge",
            ],
            "next_step": WORKBENCH_SNAPSHOT_EXPORT_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "workbench_snapshot_ocel_export_created",
            "version": WORKBENCH_SNAPSHOT_EXPORT_VERSION,
            "source_read_models": [
                "WorkbenchCommandSurfaceViewState",
                "WorkbenchRunDashboardViewState",
                "WorkbenchApprovalConsoleViewState",
                "WorkbenchEvidenceInspectorViewState",
                "WorkbenchProviderBrowserViewState",
                "WorkbenchTraceExplorerViewState",
                "AgentSurfaceTraceState",
                "AgentTurnOCELProjectionState",
                "PigGuidanceState",
            ],
            "target_read_models": [
                "WorkbenchSnapshotState",
                "WorkbenchSnapshotManifestState",
                "WorkbenchSnapshotRefBundleState",
                "WorkbenchOCELExportPackageState",
                "WorkbenchOCELExportManifestState",
                "WorkbenchEventQualityReportState",
                "WorkbenchTraceCoverageReportState",
                "WorkbenchRedactionReportState",
                "WorkbenchReproducibilityPacketState",
                "WorkbenchExportBoundaryDescriptorState",
                "V026ReadinessState",
            ],
            "effect_types": WORKBENCH_SNAPSHOT_EXPORT_EFFECT_TYPES,
            "compatibility_effect_refs": WORKBENCH_COMMAND_SURFACE_EFFECT_TYPES,
        }


def _bool(value: bool) -> str:
    return "true" if value else "false"


def render_workbench_snapshot_export_cli(parts: dict[str, Any], section: str = "create") -> str:
    report: WorkbenchSnapshotExportReport = parts["report"]
    lines = [
        f"Workbench Snapshot / OCEL Export {section}",
        f"version={report.version}",
        f"layer={WORKBENCH_SNAPSHOT_EXPORT_LAYER}",
        f"snapshot_created={_bool(report.snapshot_created)}",
        f"snapshot_manifest_created={_bool(report.snapshot_manifest_created)}",
        f"ref_bundle_created={_bool(report.ref_bundle_created)}",
        f"ocel_export_package_created={_bool(report.ocel_export_package_created)}",
        f"ocel_export_manifest_created={_bool(report.ocel_export_manifest_created)}",
        f"event_quality_report_created={_bool(report.event_quality_report_created)}",
        f"trace_coverage_report_created={_bool(report.trace_coverage_report_created)}",
        f"redaction_report_created={_bool(report.redaction_report_created)}",
        f"reproducibility_packet_created={_bool(report.reproducibility_packet_created)}",
        f"export_boundary_descriptor_created={_bool(report.export_boundary_descriptor_created)}",
        f"ready_for_v0_26_9={_bool(report.ready_for_v0_26_9)}",
        f"ready_for_v0_27={_bool(report.ready_for_v0_27)}",
        f"memory_candidate_created={_bool(report.memory_candidate_created)}",
        f"memory_promoted={_bool(report.memory_promoted)}",
        f"persistent_memory_written={_bool(report.persistent_memory_written)}",
        f"persona_mutated={_bool(report.persona_mutated)}",
        f"raw_transcript_exported={_bool(report.raw_transcript_exported)}",
        f"raw_provider_output_exported={_bool(report.raw_provider_output_exported)}",
        f"raw_secret_exported={_bool(report.raw_secret_exported)}",
        f"credential_exported={_bool(report.credential_exported)}",
        f"private_full_path_exported={_bool(report.private_full_path_exported)}",
        f"external_sync_performed={_bool(report.external_sync_performed)}",
        f"external_provider_adapter_implemented={_bool(report.external_provider_adapter_implemented)}",
        f"vendor_adapter_implemented={_bool(report.vendor_adapter_implemented)}",
        f"pm4py_runtime_dependency_added={_bool(report.pm4py_runtime_dependency_added)}",
        f"ocpa_runtime_dependency_added={_bool(report.ocpa_runtime_dependency_added)}",
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
        f"pig_memory_promoted={_bool(report.pig_memory_promoted)}",
        f"pig_policy_mutated={_bool(report.pig_policy_mutated)}",
        f"pig_executed={_bool(report.pig_executed)}",
        f"schumpeter_split_introduced={_bool(report.schumpeter_split_introduced)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    if section == "selection":
        lines.append(f"selected_ref_count={parts['selection'].selected_ref_count}")
    elif section == "manifest":
        lines.append(f"is_memory_index={_bool(parts['snapshot_manifest'].is_memory_index)}")
    elif section == "refs":
        lines.append(f"ref_count={parts['ref_bundle'].ref_count}")
        lines.append(f"raw_content_included={_bool(parts['ref_bundle'].raw_content_included)}")
    elif section == "redaction":
        redaction = parts["redaction_report"]
        lines.append(f"preserved_ref_count={redaction.preserved_ref_count}")
        lines.append(f"redacted_raw_transcript_count={redaction.redacted_raw_transcript_count}")
    elif section == "reproducibility":
        packet = parts["reproducibility_packet"]
        lines.append(f"rerun_permission_granted={_bool(packet.rerun_permission_granted)}")
        lines.append(f"rerun_performed={_bool(packet.rerun_performed)}")
    elif section == "ocel":
        package = parts["ocel_export_package"]
        lines.append(f"refs_only={_bool(package.refs_only)}")
        lines.append(f"exported_object_count={package.exported_object_count}")
    elif section == "export-manifest":
        manifest = parts["ocel_export_manifest"]
        lines.append(f"manifest_status={manifest.manifest_status}")
        lines.append(f"included_object_type_count={len(manifest.included_object_types)}")
    elif section == "quality":
        quality = parts["event_quality_report"]
        lines.append(f"automatic_optimization_performed={_bool(quality.automatic_optimization_performed)}")
    elif section == "trace-coverage":
        coverage = parts["trace_coverage_report"]
        lines.append(f"trace_ref_count={coverage.trace_ref_count}")
    elif section == "boundary":
        boundary = parts["export_boundary_descriptor"]
        lines.append(f"external_adapter_invoked={_bool(boundary.external_adapter_invoked)}")
        lines.append(f"pm4py_runtime_dependency_used={_bool(boundary.pm4py_runtime_dependency_used)}")
        lines.append(f"ocpa_runtime_dependency_used={_bool(boundary.ocpa_runtime_dependency_used)}")
    elif section == "report":
        lines.append(f"report_id={report.report_id}")
        lines.append(f"report_status={report.report_status}")
        lines.append(f"finding_count={len(report.findings)}")
    return "\n".join(lines)
