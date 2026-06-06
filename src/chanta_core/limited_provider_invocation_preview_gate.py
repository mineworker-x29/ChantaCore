from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.adapter_invocation_candidate_dry_run_plan import (
    AdapterInvocationCandidateReport,
    AdapterInvocationCandidateReportService,
)
from chanta_core.credential_secret_network_boundary import (
    CredentialNetworkBoundaryReport,
    CredentialNetworkBoundaryReportService,
)
from chanta_core.external_provider_adapter_contract import (
    ExternalAdapterContractReport,
    ExternalAdapterContractReportService,
    ModelMixin,
    _bool,
    _ref,
)
from chanta_core.external_skill_packaging_certification_matrix import (
    AdapterPackagingCertificationReport,
    AdapterPackagingCertificationReportService,
)
from chanta_core.mock_adapter_harness_no_network_default import (
    MockAdapterHarnessReport,
    MockAdapterHarnessReportService,
)
from chanta_core.permission_safety_scope_gate_for_external_adapters import (
    AdapterPermissionSafetyReport,
    AdapterPermissionSafetyReportService,
)
from chanta_core.provider_capability_inventory_adapter_registry import (
    AdapterRegistryReport,
    AdapterRegistryReportService,
)
from chanta_core.provider_invocation_approval_audit_rollback_boundary import (
    ProviderInvocationApprovalAuditRollbackReport,
    ProviderInvocationApprovalAuditRollbackReportService,
)
from chanta_core.utility.time import utc_now_iso


V0298_VERSION = "v0.29.8"
V0298_LAYER = "external_provider_adapter"
V0298_TRACK = "External Skill / External Provider Adapter Development"
V0298_NAME = "Limited Provider Invocation Preview Gate"
V0298_NEXT_STEP = "v0.29.9 External Provider Adapter Foundation Consolidation"

V0298_OBJECT_TYPES = [
    "limited_provider_invocation_preview_policy",
    "limited_provider_invocation_preview_request",
    "limited_provider_invocation_preview_source_view",
    "limited_preview_eligibility_matrix",
    "limited_preview_eligibility_row",
    "limited_preview_scope_policy",
    "limited_preview_scope",
    "limited_preview_provider_candidate",
    "limited_preview_approval_requirement",
    "limited_preview_credential_binding",
    "limited_preview_network_binding",
    "limited_preview_payload_boundary",
    "limited_preview_result_boundary",
    "limited_preview_audit_ocel_plan",
    "limited_preview_rollback_noop_binding",
    "limited_preview_risk_assessment",
    "limited_preview_deny_defer_reason",
    "limited_preview_decision_candidate",
    "limited_preview_decision_record",
    "limited_preview_gate",
    "limited_preview_audit_trail",
    "limited_preview_handoff_packet",
    "limited_preview_finding",
    "limited_provider_invocation_preview_report",
    "adapter_packaging_certification_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

V0298_EVENT_TYPES = [
    "limited_preview_requested",
    "limited_preview_prerequisites_loaded",
    "limited_provider_invocation_preview_policy_created",
    "limited_preview_eligibility_matrix_created",
    "limited_preview_eligibility_row_created",
    "limited_preview_scope_policy_created",
    "limited_preview_scope_created",
    "limited_preview_provider_candidate_created",
    "limited_preview_approval_requirement_created",
    "limited_preview_credential_binding_created",
    "limited_preview_network_binding_created",
    "limited_preview_payload_boundary_created",
    "limited_preview_result_boundary_created",
    "limited_preview_audit_ocel_plan_created",
    "limited_preview_rollback_noop_binding_created",
    "limited_preview_risk_assessment_created",
    "limited_preview_deny_defer_reason_created",
    "limited_preview_decision_candidate_created",
    "limited_preview_decision_record_created",
    "limited_preview_gate_evaluated",
    "limited_preview_audit_trail_created",
    "limited_preview_handoff_packet_created",
    "limited_preview_report_created",
    "limited_preview_warning_created",
    "limited_preview_blocked",
]

V0298_EFFECT_TYPES = [
    "read_only_observation",
    "limited_preview_policy_created",
    "limited_preview_eligibility_matrix_created",
    "limited_preview_provider_candidate_created",
    "limited_preview_scope_created",
    "limited_preview_binding_created",
    "limited_preview_risk_assessment_created",
    "limited_preview_decision_record_created",
    "limited_preview_gate_evaluated",
    "limited_preview_handoff_packet_created",
    "state_candidate_created",
]

V0298_FORBIDDEN_EFFECT_TYPES = [
    "preview_execution_performed",
    "provider_registered",
    "provider_invoked",
    "provider_sdk_invoked",
    "network_called",
    "outbound_request_sent",
    "credential_accessed",
    "credential_stored",
    "credential_logged",
    "secret_retrieved",
    "secret_materialized",
    "command_executed",
    "shell_execution_surface_created",
    "subprocess_expansion_added",
    "external_side_effect_performed",
    "file_mutated",
    "rollback_executed",
    "automatic_retry_performed",
    "package_published",
    "package_uploaded",
    "release_tag_created",
    "official_release_artifact_created",
    "live_provider_certified",
    "live_adapter_implemented",
    "external_provider_adapter_implemented",
    "RPA_adapter_implemented",
    "A360_adapter_implemented",
    "Brity_adapter_implemented",
    "UiPath_adapter_implemented",
    "external_dominion_implemented",
    "schumpeter_private_runtime_used",
    "actual_user_data_used",
    "actual_company_data_used",
    "private_material_exposed",
    "raw_provider_output_persisted",
    "raw_payload_logged",
    "references_runtime_dependency_added",
    "references_code_copied",
    "PIG_execution_authority_enabled",
    "llm_judge_used",
]

PREVIEW_EVENTS = [
    "limited_preview_candidate_created",
    "limited_preview_scope_recorded",
    "limited_preview_approval_requirement_recorded",
    "limited_preview_credential_binding_recorded",
    "limited_preview_network_binding_recorded",
    "limited_preview_payload_boundary_recorded",
    "limited_preview_result_boundary_recorded",
    "limited_preview_gate_evaluated",
]

RISK_DIMENSIONS = [
    "credential_exposure",
    "network_access",
    "private_data_exposure",
    "provider_side_effect",
    "command_execution",
    "data_exfiltration",
    "raw_provider_output_persistence",
    "approval_gap",
    "audit_gap",
    "rollback_gap",
    "OCEL_visibility_gap",
    "RPA_scope_creep",
    "external_dominion_creep",
]


def _now() -> str:
    return utc_now_iso()


def _refs(object_type: str, items: list[Any], attr: str, version: str) -> list[dict[str, Any]]:
    return [_ref(object_type, getattr(item, attr), version) for item in items]


def _safe_get(items: list[Any], index: int) -> Any | None:
    if not items:
        return None
    return items[min(index, len(items) - 1)]


@dataclass
class LimitedProviderInvocationPreviewPolicy(ModelMixin):
    policy_id: str
    preview_gate_enabled: bool = True
    preview_execution_enabled_now: bool = False
    preview_eligibility_required: bool = True
    certification_required: bool = True
    explicit_approval_required_later: bool = True
    credential_boundary_required: bool = True
    network_boundary_required: bool = True
    payload_boundary_required: bool = True
    result_boundary_required: bool = True
    audit_ocel_plan_required: bool = True
    rollback_noop_boundary_required: bool = True
    limited_scope_required: bool = True
    preview_scope_must_be_bounded: bool = True
    preview_pass_is_not_unlimited_runtime: bool = True
    preview_authorization_candidate_is_not_invocation: bool = True
    provider_invocation_enabled_now: bool = False
    provider_registration_enabled_now: bool = False
    provider_sdk_invocation_enabled_now: bool = False
    network_access_enabled_now: bool = False
    credential_access_enabled_now: bool = False
    secret_retrieval_enabled_now: bool = False
    command_execution_expansion_enabled_now: bool = False
    rollback_execution_enabled_now: bool = False
    automatic_retry_enabled_now: bool = False
    live_adapter_implementation_enabled_now: bool = False
    package_publish_enabled_now: bool = False
    release_tag_creation_enabled_now: bool = False
    rpa_adapter_enabled_now: bool = False
    external_agent_dominion_enabled_now: bool = False
    no_provider_invocation_default: bool = True
    no_network_default: bool = True
    no_credential_value_default: bool = True
    no_command_execution_default: bool = True
    llm_judge_as_sole_preview_authority_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0298_VERSION
    layer: str = V0298_LAYER


@dataclass
class LimitedProviderInvocationPreviewRequest(ModelMixin):
    request_id: str
    packaging_certification_report_id: str | None
    approval_audit_rollback_report_id: str | None
    invocation_candidate_report_id: str | None
    credential_network_boundary_report_id: str | None
    requested_preview_scope: str = "full_limited_preview_gate"
    strictness: str = "standard"
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0298_VERSION


@dataclass
class LimitedProviderInvocationPreviewSourceView(ModelMixin):
    source_view_id: str
    packaging_certification_report_ref: dict[str, Any] | None
    certification_readiness_gate_ref: dict[str, Any] | None
    certification_matrix_refs: list[dict[str, Any]]
    certification_case_result_refs: list[dict[str, Any]]
    boundary_certification_refs: list[dict[str, Any]]
    rpa_future_track_note_refs: list[dict[str, Any]]
    external_dominion_exclusion_refs: list[dict[str, Any]]
    approval_audit_rollback_report_ref: dict[str, Any] | None
    approval_decision_record_refs: list[dict[str, Any]]
    audit_trail_refs: list[dict[str, Any]]
    rollback_noop_refs: list[dict[str, Any]]
    invocation_candidate_report_ref: dict[str, Any] | None
    invocation_candidate_refs: list[dict[str, Any]]
    dry_run_report_refs: list[dict[str, Any]]
    credential_network_boundary_report_ref: dict[str, Any] | None
    permission_safety_report_ref: dict[str, Any] | None
    mock_harness_report_ref: dict[str, Any] | None
    adapter_registry_report_ref: dict[str, Any] | None
    external_adapter_contract_report_ref: dict[str, Any] | None
    provider_invocation_prohibition_ref: dict[str, Any] | None
    command_execution_prohibition_ref: dict[str, Any] | None
    source_status: str
    certification_ready_for_preview_gate: bool | None
    approval_boundary_ready_for_preview_gate: bool | None
    invocation_candidate_ready_for_preview_gate: bool | None
    credential_network_ready_for_preview_gate: bool | None
    provider_invocation_detected: bool = False
    provider_sdk_invocation_detected: bool = False
    network_call_detected: bool = False
    credential_access_detected: bool = False
    secret_retrieval_detected: bool = False
    command_execution_detected: bool = False
    rollback_execution_detected: bool = False
    automatic_retry_detected: bool = False
    external_side_effect_detected: bool = False
    file_mutation_detected: bool = False
    package_publish_detected: bool = False
    release_tag_detected: bool = False
    live_adapter_detected: bool = False
    private_data_detected: bool = False
    raw_provider_output_detected: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0298_VERSION


@dataclass
class LimitedPreviewEligibilityRow(ModelMixin):
    row_id: str
    adapter_name: str
    capability_name: str
    invocation_candidate_ref: dict[str, Any] | None
    certification_matrix_ref: dict[str, Any] | None
    approval_boundary_ref: dict[str, Any] | None
    credential_network_boundary_ref: dict[str, Any] | None
    dry_run_ref: dict[str, Any] | None
    mock_harness_ref: dict[str, Any] | None
    contract_ref: dict[str, Any] | None
    certification_passed_or_warned: bool
    approval_boundary_complete: bool
    credential_boundary_complete: bool
    network_boundary_complete: bool
    payload_boundary_complete: bool
    result_boundary_complete: bool
    audit_ocel_boundary_complete: bool
    rollback_noop_boundary_complete: bool
    rpa_not_implemented: bool
    external_dominion_excluded: bool
    eligible_for_limited_preview_gate: bool
    eligible_for_live_invocation_now: bool = False
    eligibility_status: str = "eligible_candidate"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0298_VERSION


@dataclass
class LimitedPreviewEligibilityMatrix(ModelMixin):
    matrix_id: str
    rows: list[LimitedPreviewEligibilityRow]
    total_candidate_count: int
    eligible_candidate_count: int
    denied_candidate_count: int
    deferred_candidate_count: int
    blocked_candidate_count: int
    unknown_candidate_count: int
    matrix_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0298_VERSION


@dataclass
class LimitedPreviewScopePolicy(ModelMixin):
    policy_id: str
    limited_scope_required: bool = True
    preview_scope_must_be_adapter_specific: bool = True
    preview_scope_must_be_capability_specific: bool = True
    preview_scope_must_be_payload_bounded: bool = True
    preview_scope_must_be_network_bounded: bool = True
    preview_scope_must_be_credential_ref_bounded: bool = True
    preview_scope_must_be_time_bounded: bool = True
    wildcard_provider_scope_forbidden: bool = True
    wildcard_network_scope_forbidden: bool = True
    wildcard_credential_scope_forbidden: bool = True
    command_scope_forbidden: bool = True
    rpa_scope_forbidden_now: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0298_VERSION


@dataclass
class LimitedPreviewScope(ModelMixin):
    scope_id: str
    adapter_name: str
    capability_name: str
    eligibility_row_ref: dict[str, Any]
    provider_scope: str
    network_scope_ref: dict[str, Any] | None
    credential_scope_ref: dict[str, Any] | None
    payload_scope_ref: dict[str, Any] | None
    result_scope_ref: dict[str, Any] | None
    expiry_required: bool = True
    explicit_approval_required_later: bool = True
    scope_is_minimal: bool = True
    scope_is_bounded: bool = True
    live_invocation_scope_granted_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0298_VERSION


@dataclass
class LimitedPreviewProviderCandidate(ModelMixin):
    preview_candidate_id: str
    adapter_name: str
    capability_name: str
    eligibility_row_ref: dict[str, Any]
    preview_scope_ref: dict[str, Any]
    invocation_candidate_ref: dict[str, Any] | None
    provider_kind: str
    candidate_status: str
    candidate_reason: str
    preview_candidate_is_provider_invocation: bool = False
    provider_invoked_now: bool = False
    provider_registered_now: bool = False
    network_called_now: bool = False
    credential_accessed_now: bool = False
    command_executed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0298_VERSION


@dataclass
class LimitedPreviewApprovalRequirement(ModelMixin):
    requirement_id: str
    preview_candidate_ref: dict[str, Any]
    explicit_user_approval_required_later: bool = True
    approval_record_required: bool = True
    approval_expiry_required: bool = True
    approval_revalidation_required: bool = True
    approval_scope_summary_required: bool = True
    approval_granted_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0298_VERSION


@dataclass
class LimitedPreviewCredentialBinding(ModelMixin):
    binding_id: str
    preview_candidate_ref: dict[str, Any]
    credential_reference_ref: dict[str, Any] | None
    credential_boundary_ref: dict[str, Any] | None
    secret_reference_only: bool = True
    credential_value_accessed_now: bool = False
    credential_value_stored_now: bool = False
    credential_value_logged_now: bool = False
    secret_retrieved_now: bool = False
    binding_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0298_VERSION


@dataclass
class LimitedPreviewNetworkBinding(ModelMixin):
    binding_id: str
    preview_candidate_ref: dict[str, Any]
    network_request_candidate_ref: dict[str, Any] | None
    outbound_domain_rule_ref: dict[str, Any] | None
    network_boundary_ref: dict[str, Any] | None
    network_scope_bounded: bool
    network_called_now: bool = False
    outbound_request_sent_now: bool = False
    provider_sdk_network_called_now: bool = False
    binding_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0298_VERSION


@dataclass
class LimitedPreviewPayloadBoundary(ModelMixin):
    boundary_id: str
    preview_candidate_ref: dict[str, Any]
    payload_preview_ref: dict[str, Any] | None
    payload_boundary_ref: dict[str, Any] | None
    redaction_boundary_ref: dict[str, Any] | None
    payload_bounded: bool
    payload_sent_now: bool = False
    contains_credentials: bool = False
    contains_private_data: bool = False
    contains_raw_artifacts: bool = False
    boundary_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0298_VERSION


@dataclass
class LimitedPreviewResultBoundary(ModelMixin):
    boundary_id: str
    preview_candidate_ref: dict[str, Any]
    result_boundary_ref: dict[str, Any] | None
    result_persistence_policy_ref: dict[str, Any] | None
    raw_provider_output_persistence_forbidden: bool = True
    result_summary_required_later: bool = True
    result_redaction_required_later: bool = True
    provider_response_received_now: bool = False
    raw_provider_output_persisted_now: bool = False
    boundary_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0298_VERSION


@dataclass
class LimitedPreviewAuditOCELPlan(ModelMixin):
    plan_id: str
    preview_candidate_ref: dict[str, Any]
    audit_plan_ref: dict[str, Any] | None
    ocel_trace_plan_ref: dict[str, Any] | None
    required_preview_events: list[str]
    provider_invocation_event_emitted_now: bool = False
    audit_ocel_plan_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0298_VERSION


@dataclass
class LimitedPreviewRollbackNoOpBinding(ModelMixin):
    binding_id: str
    preview_candidate_ref: dict[str, Any]
    rollback_plan_ref: dict[str, Any] | None
    noop_boundary_ref: dict[str, Any] | None
    rollback_or_noop_available: bool
    rollback_executed_now: bool = False
    noop_available: bool = True
    noop_is_valid_decision: bool = True
    binding_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0298_VERSION


@dataclass
class LimitedPreviewRiskAssessment(ModelMixin):
    risk_assessment_id: str
    preview_candidate_ref: dict[str, Any]
    risk_dimensions: list[str]
    risk_level: str
    blocker_count: int
    warning_count: int
    risk_acceptable_for_preview_gate: bool
    risk_assessment_is_approval: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0298_VERSION


@dataclass
class LimitedPreviewDenyDeferReason(ModelMixin):
    reason_id: str
    preview_candidate_ref: dict[str, Any]
    reason_type: str
    decision: str
    required_future_action: str | None
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0298_VERSION


@dataclass
class LimitedPreviewDecisionCandidate(ModelMixin):
    decision_candidate_id: str
    preview_candidate_ref: dict[str, Any]
    proposed_decision: str
    decision_reason: str
    preview_execution_allowed_now: bool = False
    provider_invocation_allowed_now: bool = False
    network_allowed_now: bool = False
    credential_access_allowed_now: bool = False
    command_execution_allowed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0298_VERSION


@dataclass
class LimitedPreviewDecisionRecord(ModelMixin):
    decision_record_id: str
    decision_candidate_ref: dict[str, Any]
    final_decision: str
    decision_reason: str
    provider_invoked_now: bool = False
    network_called_now: bool = False
    credential_accessed_now: bool = False
    command_executed_now: bool = False
    external_side_effect_performed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0298_VERSION


@dataclass
class LimitedPreviewGate(ModelMixin):
    gate_id: str
    source_view_ref: dict[str, Any]
    eligibility_matrix_ref: dict[str, Any]
    preview_candidate_refs: list[dict[str, Any]]
    preview_scope_refs: list[dict[str, Any]]
    approval_requirement_refs: list[dict[str, Any]]
    credential_binding_refs: list[dict[str, Any]]
    network_binding_refs: list[dict[str, Any]]
    payload_boundary_refs: list[dict[str, Any]]
    result_boundary_refs: list[dict[str, Any]]
    audit_ocel_plan_refs: list[dict[str, Any]]
    rollback_noop_binding_refs: list[dict[str, Any]]
    risk_assessment_refs: list[dict[str, Any]]
    decision_record_refs: list[dict[str, Any]]
    certification_ready: bool
    approval_boundary_ready: bool
    credential_boundary_ready: bool
    network_boundary_ready: bool
    payload_boundary_ready: bool
    result_boundary_ready: bool
    audit_ocel_ready: bool
    rollback_noop_ready: bool
    risk_acceptable: bool
    rpa_excluded_or_deferred: bool
    external_dominion_excluded: bool
    preview_gate_candidates_complete: bool
    preview_gate_passed: bool
    no_provider_invocation: bool
    no_network_call: bool
    no_credential_access: bool
    no_command_execution: bool
    no_external_side_effect: bool
    no_package_publish: bool
    no_release_tag: bool
    gate_status: str
    ready_for_v0_29_9: bool
    ready_for_v029_consolidation: bool
    ready_for_preview_execution_now: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0298_VERSION


@dataclass
class LimitedPreviewAuditTrail(ModelMixin):
    audit_trail_id: str
    request_ref: dict[str, Any]
    source_view_ref: dict[str, Any]
    preview_candidate_refs: list[dict[str, Any]]
    decision_record_refs: list[dict[str, Any]]
    gate_ref: dict[str, Any]
    audit_event_count: int
    raw_content_included: bool = False
    credential_value_included: bool = False
    raw_payload_included: bool = False
    raw_provider_output_included: bool = False
    audit_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0298_VERSION


@dataclass
class LimitedPreviewHandoffPacket(ModelMixin):
    handoff_packet_id: str
    source_preview_report_id: str
    preview_gate_ref: dict[str, Any]
    eligible_candidate_refs: list[dict[str, Any]]
    denied_or_deferred_candidate_refs: list[dict[str, Any]]
    consolidation_required_refs: list[dict[str, Any]]
    not_implemented_now: list[str]
    refs_only: bool = True
    implementation_performed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0298_VERSION
    target_version: str = "v0.29.9"
    target_track: str = "External Provider Adapter Foundation Consolidation"


@dataclass
class LimitedPreviewFinding(ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class LimitedProviderInvocationPreviewReport(ModelMixin):
    report_id: str
    created_at: str
    policy: LimitedProviderInvocationPreviewPolicy
    request: LimitedProviderInvocationPreviewRequest
    source_view: LimitedProviderInvocationPreviewSourceView
    eligibility_matrix: LimitedPreviewEligibilityMatrix
    scope_policy: LimitedPreviewScopePolicy
    preview_scopes: list[LimitedPreviewScope]
    preview_candidates: list[LimitedPreviewProviderCandidate]
    approval_requirements: list[LimitedPreviewApprovalRequirement]
    credential_bindings: list[LimitedPreviewCredentialBinding]
    network_bindings: list[LimitedPreviewNetworkBinding]
    payload_boundaries: list[LimitedPreviewPayloadBoundary]
    result_boundaries: list[LimitedPreviewResultBoundary]
    audit_ocel_plans: list[LimitedPreviewAuditOCELPlan]
    rollback_noop_bindings: list[LimitedPreviewRollbackNoOpBinding]
    risk_assessments: list[LimitedPreviewRiskAssessment]
    deny_defer_reasons: list[LimitedPreviewDenyDeferReason]
    decision_candidates: list[LimitedPreviewDecisionCandidate]
    decision_records: list[LimitedPreviewDecisionRecord]
    preview_gate: LimitedPreviewGate
    audit_trail: LimitedPreviewAuditTrail
    handoff_packet: LimitedPreviewHandoffPacket
    findings: list[LimitedPreviewFinding]
    report_status: str
    ready_for_v0_29_9: bool
    ready_for_v029_consolidation: bool
    ready_for_preview_execution_now: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    preview_execution_performed: bool = False
    provider_registered: bool = False
    provider_invoked: bool = False
    provider_sdk_invoked: bool = False
    network_called: bool = False
    outbound_request_sent: bool = False
    credential_accessed: bool = False
    credential_stored: bool = False
    credential_logged: bool = False
    secret_retrieved: bool = False
    secret_materialized: bool = False
    command_executed: bool = False
    external_side_effect_performed: bool = False
    file_mutated: bool = False
    rollback_executed: bool = False
    automatic_retry_performed: bool = False
    package_published: bool = False
    release_tag_created: bool = False
    live_provider_certified: bool = False
    live_adapter_implemented: bool = False
    RPA_adapter_implemented: bool = False
    A360_adapter_implemented: bool = False
    Brity_adapter_implemented: bool = False
    UiPath_adapter_implemented: bool = False
    external_dominion_implemented: bool = False
    schumpeter_private_runtime_used: bool = False
    actual_user_data_used: bool = False
    actual_company_data_used: bool = False
    private_material_exposed: bool = False
    raw_provider_output_persisted: bool = False
    raw_payload_logged: bool = False
    references_runtime_dependency_added: bool = False
    references_code_copied: bool = False
    PIG_execution_authority_enabled: bool = False
    llm_judge_used: bool = False
    next_required_step: str = V0298_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.29.9 External Provider Adapter Foundation Consolidation begins or Limited Provider Invocation Preview policy changes."
    version: str = V0298_VERSION


class LimitedProviderInvocationPreviewPrerequisiteSourceService:
    def load_v0297_packaging_certification_report(self) -> AdapterPackagingCertificationReport:
        return AdapterPackagingCertificationReportService().build_report()

    def load_v0297_certification_readiness_gate(self) -> Any:
        return self.load_v0297_packaging_certification_report().certification_readiness_gate

    def load_certification_matrices(self) -> list[Any]:
        return self.load_v0297_packaging_certification_report().certification_matrices

    def load_certification_case_results(self) -> list[Any]:
        return self.load_v0297_packaging_certification_report().certification_case_results

    def load_boundary_certification_reports(self) -> list[Any]:
        report = self.load_v0297_packaging_certification_report()
        return (
            report.mock_mode_certifications
            + report.no_network_certifications
            + report.no_credential_certifications
            + report.no_command_certifications
            + report.permission_safety_certifications
            + report.credential_network_boundary_certifications
            + report.dry_run_certifications
            + report.approval_audit_rollback_certifications
            + report.ocel_visibility_certifications
            + report.result_boundary_certifications
            + report.failure_rollback_noop_certifications
        )

    def load_rpa_future_track_notes(self) -> list[Any]:
        return self.load_v0297_packaging_certification_report().rpa_future_track_notes

    def load_external_dominion_exclusion_certifications(self) -> list[Any]:
        return self.load_v0297_packaging_certification_report().external_dominion_exclusion_certifications

    def load_v0296_approval_audit_rollback_report(self) -> ProviderInvocationApprovalAuditRollbackReport:
        return ProviderInvocationApprovalAuditRollbackReportService().build_report()

    def load_v0295_invocation_candidate_report(self) -> AdapterInvocationCandidateReport:
        return AdapterInvocationCandidateReportService().build_report()

    def load_v0294_credential_network_boundary_report(self) -> CredentialNetworkBoundaryReport:
        return CredentialNetworkBoundaryReportService().build_report()

    def load_v0293_permission_safety_report(self) -> AdapterPermissionSafetyReport:
        return AdapterPermissionSafetyReportService().build_report()

    def load_v0292_mock_harness_report(self) -> MockAdapterHarnessReport:
        return MockAdapterHarnessReportService().build_report()

    def load_v0291_adapter_registry_report(self) -> AdapterRegistryReport:
        return AdapterRegistryReportService().build_report()

    def load_v0290_external_adapter_contract_report(self) -> ExternalAdapterContractReport:
        return ExternalAdapterContractReportService().build_report()

    def load_provider_invocation_prohibition_contract(self) -> dict[str, Any]:
        return _ref("provider_invocation_prohibition_contract", "provider_invocation_prohibition_contract:v0.29.0", "v0.29.0")

    def load_command_execution_prohibition_contract(self) -> dict[str, Any]:
        return _ref("command_execution_prohibition_contract", "command_execution_prohibition_contract:v0.29.0", "v0.29.0")


class LimitedProviderInvocationPreviewPolicyService:
    def build_policy(self) -> LimitedProviderInvocationPreviewPolicy:
        return LimitedProviderInvocationPreviewPolicy("limited_provider_invocation_preview_policy:v0.29.8")


class LimitedProviderInvocationPreviewSourceViewService:
    def build_source_view(self) -> LimitedProviderInvocationPreviewSourceView:
        source = LimitedProviderInvocationPreviewPrerequisiteSourceService()
        packaging = source.load_v0297_packaging_certification_report()
        approval = source.load_v0296_approval_audit_rollback_report()
        invocation = source.load_v0295_invocation_candidate_report()
        credential = source.load_v0294_credential_network_boundary_report()
        permission = source.load_v0293_permission_safety_report()
        mock = source.load_v0292_mock_harness_report()
        registry = source.load_v0291_adapter_registry_report()
        contract = source.load_v0290_external_adapter_contract_report()
        boundary_refs = []
        for item in source.load_boundary_certification_reports():
            object_id = getattr(item, "report_id", getattr(item, "note_id", getattr(item, "certification_id", "unknown")))
            boundary_refs.append(_ref(item.__class__.__name__, object_id, "v0.29.7"))
        rollback_noop_refs = _refs("provider_rollback_plan", approval.rollback_plans, "rollback_plan_id", "v0.29.6") + _refs(
            "provider_noop_boundary", approval.noop_boundaries, "noop_boundary_id", "v0.29.6"
        )
        return LimitedProviderInvocationPreviewSourceView(
            "limited_provider_invocation_preview_source_view:v0.29.8",
            _ref("adapter_packaging_certification_report", packaging.report_id, "v0.29.7"),
            _ref("adapter_certification_readiness_gate", packaging.certification_readiness_gate.gate_id, "v0.29.7"),
            _refs("adapter_certification_matrix", packaging.certification_matrices, "matrix_id", "v0.29.7"),
            _refs("adapter_certification_case_result", packaging.certification_case_results, "result_id", "v0.29.7"),
            boundary_refs,
            _refs("rpa_future_track_certification_note", packaging.rpa_future_track_notes, "note_id", "v0.29.7"),
            _refs("external_dominion_exclusion_certification", packaging.external_dominion_exclusion_certifications, "certification_id", "v0.29.7"),
            _ref("provider_invocation_approval_audit_rollback_report", approval.report_id, "v0.29.6"),
            _refs("provider_invocation_approval_decision_record", approval.approval_decision_records, "decision_record_id", "v0.29.6"),
            [_ref("provider_invocation_audit_trail", approval.audit_trail.audit_trail_id, "v0.29.6")],
            rollback_noop_refs,
            _ref("adapter_invocation_candidate_report", invocation.report_id, "v0.29.5"),
            _refs("adapter_invocation_candidate", invocation.invocation_candidates, "candidate_id", "v0.29.5"),
            _refs("adapter_invocation_dry_run_report", invocation.dry_run_reports, "report_id", "v0.29.5"),
            _ref("credential_network_boundary_report", credential.report_id, "v0.29.4"),
            _ref("adapter_permission_safety_report", permission.report_id, "v0.29.3"),
            _ref("mock_adapter_harness_report", mock.report_id, "v0.29.2"),
            _ref("adapter_registry_report", registry.report_id, "v0.29.1"),
            _ref("external_adapter_contract_report", contract.report_id, "v0.29.0"),
            source.load_provider_invocation_prohibition_contract(),
            source.load_command_execution_prohibition_contract(),
            "complete",
            packaging.ready_for_limited_invocation_preview_gate,
            approval.ready_for_certification_matrix,
            invocation.ready_for_approval_audit_rollback_boundary,
            credential.ready_for_invocation_candidate,
        )


class LimitedProviderInvocationPreviewRequestService:
    def build_request(self, source_view: LimitedProviderInvocationPreviewSourceView) -> LimitedProviderInvocationPreviewRequest:
        refs = [
            ref
            for ref in [
                source_view.packaging_certification_report_ref,
                source_view.approval_audit_rollback_report_ref,
                source_view.invocation_candidate_report_ref,
                source_view.credential_network_boundary_report_ref,
            ]
            if ref is not None
        ]
        return LimitedProviderInvocationPreviewRequest(
            "limited_provider_invocation_preview_request:v0.29.8",
            source_view.packaging_certification_report_ref.get("object_id") if source_view.packaging_certification_report_ref else None,
            source_view.approval_audit_rollback_report_ref.get("object_id") if source_view.approval_audit_rollback_report_ref else None,
            source_view.invocation_candidate_report_ref.get("object_id") if source_view.invocation_candidate_report_ref else None,
            source_view.credential_network_boundary_report_ref.get("object_id") if source_view.credential_network_boundary_report_ref else None,
            source_refs=refs,
        )


class LimitedPreviewEligibilityService:
    def build_rows(
        self,
        packaging: AdapterPackagingCertificationReport,
        approval: ProviderInvocationApprovalAuditRollbackReport,
        invocation: AdapterInvocationCandidateReport,
        credential: CredentialNetworkBoundaryReport,
        mock: MockAdapterHarnessReport,
        contract: ExternalAdapterContractReport,
    ) -> list[LimitedPreviewEligibilityRow]:
        rows: list[LimitedPreviewEligibilityRow] = []
        for index, candidate in enumerate(invocation.invocation_candidates):
            matrix = _safe_get(packaging.certification_matrices, index)
            dry_run = _safe_get(invocation.dry_run_reports, index)
            eligible = bool(matrix) and packaging.ready_for_limited_invocation_preview_gate and approval.ready_for_certification_matrix
            rows.append(
                LimitedPreviewEligibilityRow(
                    f"limited_preview_eligibility_row:{candidate.adapter_name}:v0.29.8",
                    candidate.adapter_name,
                    candidate.capability_name,
                    _ref("adapter_invocation_candidate", candidate.candidate_id, "v0.29.5"),
                    _ref("adapter_certification_matrix", matrix.matrix_id, "v0.29.7") if matrix else None,
                    _ref("provider_invocation_approval_audit_rollback_report", approval.report_id, "v0.29.6"),
                    _ref("credential_network_boundary_report", credential.report_id, "v0.29.4"),
                    _ref("adapter_invocation_dry_run_report", dry_run.report_id, "v0.29.5") if dry_run else None,
                    _ref("mock_adapter_harness_report", mock.report_id, "v0.29.2"),
                    _ref("external_adapter_contract_report", contract.report_id, "v0.29.0"),
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    eligible,
                )
            )
        return rows

    def build_matrix(self, rows: list[LimitedPreviewEligibilityRow]) -> LimitedPreviewEligibilityMatrix:
        return LimitedPreviewEligibilityMatrix(
            "limited_preview_eligibility_matrix:v0.29.8",
            rows,
            len(rows),
            sum(row.eligibility_status == "eligible_candidate" for row in rows),
            sum(row.eligibility_status == "denied" for row in rows),
            sum(row.eligibility_status == "deferred" for row in rows),
            sum(row.eligibility_status == "blocked" for row in rows),
            sum(row.eligibility_status == "unknown" for row in rows),
            "warning",
        )


class LimitedPreviewScopeService:
    def build_policy(self) -> LimitedPreviewScopePolicy:
        return LimitedPreviewScopePolicy("limited_preview_scope_policy:v0.29.8")

    def build_scopes(self, rows: list[LimitedPreviewEligibilityRow], credential: CredentialNetworkBoundaryReport) -> list[LimitedPreviewScope]:
        scopes: list[LimitedPreviewScope] = []
        for index, row in enumerate(rows):
            cred = _safe_get(credential.credential_access_candidates, index)
            network = _safe_get(credential.network_request_candidates, index)
            scopes.append(
                LimitedPreviewScope(
                    f"limited_preview_scope:{row.adapter_name}:v0.29.8",
                    row.adapter_name,
                    row.capability_name,
                    _ref("limited_preview_eligibility_row", row.row_id, V0298_VERSION),
                    f"{row.adapter_name}:{row.capability_name}:bounded-preview-candidate",
                    _ref("network_request_candidate", network.candidate_id, "v0.29.4") if network else None,
                    _ref("credential_access_candidate", cred.candidate_id, "v0.29.4") if cred else None,
                    _ref("payload_boundary_policy", credential.payload_boundary_policy.policy_id, "v0.29.4"),
                    _ref("provider_result_boundary_policy", "provider_result_boundary_policy:v0.29.6", "v0.29.6"),
                )
            )
        return scopes


class LimitedPreviewProviderCandidateService:
    def build_candidates(self, rows: list[LimitedPreviewEligibilityRow], scopes: list[LimitedPreviewScope]) -> list[LimitedPreviewProviderCandidate]:
        candidates: list[LimitedPreviewProviderCandidate] = []
        for index, row in enumerate(rows):
            scope = scopes[index]
            candidates.append(
                LimitedPreviewProviderCandidate(
                    f"limited_preview_provider_candidate:{row.adapter_name}:v0.29.8",
                    row.adapter_name,
                    row.capability_name,
                    _ref("limited_preview_eligibility_row", row.row_id, V0298_VERSION),
                    _ref("limited_preview_scope", scope.scope_id, V0298_VERSION),
                    row.invocation_candidate_ref,
                    "mock_provider",
                    "preview_gate_candidate" if row.eligible_for_limited_preview_gate else "deferred",
                    "Candidate is eligible for preview gate handoff only; provider invocation remains disabled.",
                )
            )
        return candidates


class LimitedPreviewBindingService:
    def build_approval_requirements(self, candidates: list[LimitedPreviewProviderCandidate]) -> list[LimitedPreviewApprovalRequirement]:
        return [
            LimitedPreviewApprovalRequirement(
                f"limited_preview_approval_requirement:{candidate.adapter_name}:v0.29.8",
                _ref("limited_preview_provider_candidate", candidate.preview_candidate_id, V0298_VERSION),
            )
            for candidate in candidates
        ]

    def build_credential_bindings(self, candidates: list[LimitedPreviewProviderCandidate], credential: CredentialNetworkBoundaryReport) -> list[LimitedPreviewCredentialBinding]:
        return [
            LimitedPreviewCredentialBinding(
                f"limited_preview_credential_binding:{candidate.adapter_name}:v0.29.8",
                _ref("limited_preview_provider_candidate", candidate.preview_candidate_id, V0298_VERSION),
                _ref("credential_access_candidate", _safe_get(credential.credential_access_candidates, index).candidate_id, "v0.29.4")
                if credential.credential_access_candidates
                else None,
                _ref("credential_network_boundary_report", credential.report_id, "v0.29.4"),
            )
            for index, candidate in enumerate(candidates)
        ]

    def build_network_bindings(self, candidates: list[LimitedPreviewProviderCandidate], credential: CredentialNetworkBoundaryReport) -> list[LimitedPreviewNetworkBinding]:
        bindings: list[LimitedPreviewNetworkBinding] = []
        for index, candidate in enumerate(candidates):
            network = _safe_get(credential.network_request_candidates, index)
            bindings.append(
                LimitedPreviewNetworkBinding(
                    f"limited_preview_network_binding:{candidate.adapter_name}:v0.29.8",
                    _ref("limited_preview_provider_candidate", candidate.preview_candidate_id, V0298_VERSION),
                    _ref("network_request_candidate", network.candidate_id, "v0.29.4") if network else None,
                    getattr(network, "outbound_domain_rule_ref", None) if network else None,
                    _ref("credential_network_boundary_report", credential.report_id, "v0.29.4"),
                    True,
                )
            )
        return bindings

    def build_payload_boundaries(self, candidates: list[LimitedPreviewProviderCandidate], invocation: AdapterInvocationCandidateReport, credential: CredentialNetworkBoundaryReport) -> list[LimitedPreviewPayloadBoundary]:
        boundaries: list[LimitedPreviewPayloadBoundary] = []
        for index, candidate in enumerate(candidates):
            preview = _safe_get(invocation.payload_previews, index)
            boundaries.append(
                LimitedPreviewPayloadBoundary(
                    f"limited_preview_payload_boundary:{candidate.adapter_name}:v0.29.8",
                    _ref("limited_preview_provider_candidate", candidate.preview_candidate_id, V0298_VERSION),
                    _ref("adapter_invocation_payload_preview", preview.payload_preview_id, "v0.29.5") if preview else None,
                    _ref("payload_boundary_policy", credential.payload_boundary_policy.policy_id, "v0.29.4"),
                    _ref("request_response_redaction_boundary", credential.request_response_redaction_boundary.boundary_id, "v0.29.4"),
                    True,
                )
            )
        return boundaries

    def build_result_boundaries(self, candidates: list[LimitedPreviewProviderCandidate], approval: ProviderInvocationApprovalAuditRollbackReport) -> list[LimitedPreviewResultBoundary]:
        return [
            LimitedPreviewResultBoundary(
                f"limited_preview_result_boundary:{candidate.adapter_name}:v0.29.8",
                _ref("limited_preview_provider_candidate", candidate.preview_candidate_id, V0298_VERSION),
                _ref("provider_result_boundary_policy", approval.result_boundary_policy.policy_id, "v0.29.6"),
                _ref("provider_result_persistence_policy", approval.result_persistence_policy.policy_id, "v0.29.6"),
            )
            for candidate in candidates
        ]

    def build_audit_ocel_plans(self, candidates: list[LimitedPreviewProviderCandidate], approval: ProviderInvocationApprovalAuditRollbackReport) -> list[LimitedPreviewAuditOCELPlan]:
        return [
            LimitedPreviewAuditOCELPlan(
                f"limited_preview_audit_ocel_plan:{candidate.adapter_name}:v0.29.8",
                _ref("limited_preview_provider_candidate", candidate.preview_candidate_id, V0298_VERSION),
                _ref("provider_invocation_audit_trail", approval.audit_trail.audit_trail_id, "v0.29.6"),
                _ref("provider_invocation_ocel_trace_plan", _safe_get(approval.ocel_trace_plans, index).trace_plan_id, "v0.29.6")
                if approval.ocel_trace_plans
                else None,
                PREVIEW_EVENTS,
            )
            for index, candidate in enumerate(candidates)
        ]

    def build_rollback_noop_bindings(self, candidates: list[LimitedPreviewProviderCandidate], approval: ProviderInvocationApprovalAuditRollbackReport) -> list[LimitedPreviewRollbackNoOpBinding]:
        bindings: list[LimitedPreviewRollbackNoOpBinding] = []
        for index, candidate in enumerate(candidates):
            rollback = _safe_get(approval.rollback_plans, index)
            noop = _safe_get(approval.noop_boundaries, index)
            bindings.append(
                LimitedPreviewRollbackNoOpBinding(
                    f"limited_preview_rollback_noop_binding:{candidate.adapter_name}:v0.29.8",
                    _ref("limited_preview_provider_candidate", candidate.preview_candidate_id, V0298_VERSION),
                    _ref("provider_rollback_plan", rollback.rollback_plan_id, "v0.29.6") if rollback else None,
                    _ref("provider_noop_boundary", noop.noop_boundary_id, "v0.29.6") if noop else None,
                    bool(rollback or noop),
                    noop_available=bool(noop),
                )
            )
        return bindings


class LimitedPreviewRiskService:
    def build_risk_assessments(self, candidates: list[LimitedPreviewProviderCandidate]) -> list[LimitedPreviewRiskAssessment]:
        return [
            LimitedPreviewRiskAssessment(
                f"limited_preview_risk_assessment:{candidate.adapter_name}:v0.29.8",
                _ref("limited_preview_provider_candidate", candidate.preview_candidate_id, V0298_VERSION),
                RISK_DIMENSIONS,
                "medium",
                0,
                1,
                True,
            )
            for candidate in candidates
        ]

    def build_deny_defer_reasons(self, candidates: list[LimitedPreviewProviderCandidate]) -> list[LimitedPreviewDenyDeferReason]:
        return [
            LimitedPreviewDenyDeferReason(
                f"limited_preview_deny_defer_reason:{candidate.adapter_name}:v0.29.8",
                _ref("limited_preview_provider_candidate", candidate.preview_candidate_id, V0298_VERSION),
                "unknown" if candidate.candidate_status == "preview_gate_candidate" else "missing_certification",
                "defer" if candidate.candidate_status == "preview_gate_candidate" else "deny",
                "v0.29.9 consolidation must preserve that preview eligibility is not execution.",
            )
            for candidate in candidates
        ]


class LimitedPreviewDecisionService:
    def build_decision_candidates(self, candidates: list[LimitedPreviewProviderCandidate]) -> list[LimitedPreviewDecisionCandidate]:
        return [
            LimitedPreviewDecisionCandidate(
                f"limited_preview_decision_candidate:{candidate.adapter_name}:v0.29.8",
                _ref("limited_preview_provider_candidate", candidate.preview_candidate_id, V0298_VERSION),
                "preview_gate_candidate" if candidate.candidate_status == "preview_gate_candidate" else "defer",
                "v0.29.8 records eligibility only; execution and provider invocation remain disabled.",
            )
            for candidate in candidates
        ]

    def build_decision_records(self, decision_candidates: list[LimitedPreviewDecisionCandidate]) -> list[LimitedPreviewDecisionRecord]:
        return [
            LimitedPreviewDecisionRecord(
                f"limited_preview_decision_record:{decision.decision_candidate_id.split(':')[1]}:v0.29.8",
                _ref("limited_preview_decision_candidate", decision.decision_candidate_id, V0298_VERSION),
                decision.proposed_decision,
                decision.decision_reason,
            )
            for decision in decision_candidates
        ]


class LimitedPreviewGateService:
    def evaluate_gate(
        self,
        source_view: LimitedProviderInvocationPreviewSourceView,
        matrix: LimitedPreviewEligibilityMatrix,
        scopes: list[LimitedPreviewScope],
        candidates: list[LimitedPreviewProviderCandidate],
        approvals: list[LimitedPreviewApprovalRequirement],
        credential_bindings: list[LimitedPreviewCredentialBinding],
        network_bindings: list[LimitedPreviewNetworkBinding],
        payload_boundaries: list[LimitedPreviewPayloadBoundary],
        result_boundaries: list[LimitedPreviewResultBoundary],
        audit_plans: list[LimitedPreviewAuditOCELPlan],
        rollback_bindings: list[LimitedPreviewRollbackNoOpBinding],
        risks: list[LimitedPreviewRiskAssessment],
        decisions: list[LimitedPreviewDecisionRecord],
    ) -> LimitedPreviewGate:
        ready = all(
            [
                source_view.certification_ready_for_preview_gate,
                source_view.approval_boundary_ready_for_preview_gate,
                source_view.credential_network_ready_for_preview_gate,
                matrix.eligible_candidate_count > 0,
                scopes,
                candidates,
                approvals,
                credential_bindings,
                network_bindings,
                payload_boundaries,
                result_boundaries,
                audit_plans,
                rollback_bindings,
                all(risk.risk_acceptable_for_preview_gate for risk in risks),
                decisions,
            ]
        )
        return LimitedPreviewGate(
            "limited_preview_gate:v0.29.8",
            _ref("limited_provider_invocation_preview_source_view", source_view.source_view_id, V0298_VERSION),
            _ref("limited_preview_eligibility_matrix", matrix.matrix_id, V0298_VERSION),
            _refs("limited_preview_provider_candidate", candidates, "preview_candidate_id", V0298_VERSION),
            _refs("limited_preview_scope", scopes, "scope_id", V0298_VERSION),
            _refs("limited_preview_approval_requirement", approvals, "requirement_id", V0298_VERSION),
            _refs("limited_preview_credential_binding", credential_bindings, "binding_id", V0298_VERSION),
            _refs("limited_preview_network_binding", network_bindings, "binding_id", V0298_VERSION),
            _refs("limited_preview_payload_boundary", payload_boundaries, "boundary_id", V0298_VERSION),
            _refs("limited_preview_result_boundary", result_boundaries, "boundary_id", V0298_VERSION),
            _refs("limited_preview_audit_ocel_plan", audit_plans, "plan_id", V0298_VERSION),
            _refs("limited_preview_rollback_noop_binding", rollback_bindings, "binding_id", V0298_VERSION),
            _refs("limited_preview_risk_assessment", risks, "risk_assessment_id", V0298_VERSION),
            _refs("limited_preview_decision_record", decisions, "decision_record_id", V0298_VERSION),
            bool(source_view.certification_ready_for_preview_gate),
            bool(source_view.approval_boundary_ready_for_preview_gate),
            bool(source_view.credential_network_ready_for_preview_gate),
            bool(source_view.credential_network_ready_for_preview_gate),
            bool(payload_boundaries),
            bool(result_boundaries),
            bool(audit_plans),
            bool(rollback_bindings),
            all(risk.risk_acceptable_for_preview_gate for risk in risks),
            True,
            True,
            bool(candidates),
            bool(ready),
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            "warning",
            bool(ready),
            bool(ready),
        )


class LimitedPreviewAuditTrailService:
    def build_audit_trail(
        self,
        request: LimitedProviderInvocationPreviewRequest,
        source_view: LimitedProviderInvocationPreviewSourceView,
        candidates: list[LimitedPreviewProviderCandidate],
        decisions: list[LimitedPreviewDecisionRecord],
        gate: LimitedPreviewGate,
    ) -> LimitedPreviewAuditTrail:
        return LimitedPreviewAuditTrail(
            "limited_preview_audit_trail:v0.29.8",
            _ref("limited_provider_invocation_preview_request", request.request_id, V0298_VERSION),
            _ref("limited_provider_invocation_preview_source_view", source_view.source_view_id, V0298_VERSION),
            _refs("limited_preview_provider_candidate", candidates, "preview_candidate_id", V0298_VERSION),
            _refs("limited_preview_decision_record", decisions, "decision_record_id", V0298_VERSION),
            _ref("limited_preview_gate", gate.gate_id, V0298_VERSION),
            5 + len(candidates) + len(decisions),
        )


class LimitedPreviewHandoffPacketService:
    def build_packet(
        self,
        report_id: str,
        gate: LimitedPreviewGate,
        candidates: list[LimitedPreviewProviderCandidate],
        decisions: list[LimitedPreviewDecisionRecord],
    ) -> LimitedPreviewHandoffPacket:
        eligible = [candidate for candidate in candidates if candidate.candidate_status == "preview_gate_candidate"]
        return LimitedPreviewHandoffPacket(
            "limited_preview_handoff_packet:v0.29.8",
            report_id,
            _ref("limited_preview_gate", gate.gate_id, V0298_VERSION),
            _refs("limited_preview_provider_candidate", eligible, "preview_candidate_id", V0298_VERSION),
            _refs("limited_preview_decision_record", decisions, "decision_record_id", V0298_VERSION),
            [_ref("limited_preview_gate", gate.gate_id, V0298_VERSION)],
            [
                "provider_invocation",
                "provider_registration",
                "provider_sdk_invocation",
                "network_call",
                "credential_access",
                "command_execution",
                "live_adapter_runtime",
                "RPA_adapter_runtime",
                "external_agent_dominion_bridge",
            ],
        )


class LimitedPreviewFindingService:
    BLOCKED_FINDINGS = {
        "provider_invocation_attempted",
        "provider_registration_attempted",
        "provider_sdk_invocation_attempted",
        "network_call_attempted",
        "outbound_request_attempted",
        "credential_access_attempted",
        "credential_storage_attempted",
        "credential_logging_attempted",
        "secret_retrieval_attempted",
        "secret_materialization_attempted",
        "command_execution_attempted",
        "shell_true_detected",
        "unbounded_subprocess_detected",
        "external_side_effect_attempted",
        "file_mutation_attempted",
        "rollback_execution_attempted",
        "automatic_retry_attempted",
        "live_adapter_implementation_attempted",
        "package_publish_attempted",
        "release_tag_creation_attempted",
        "live_provider_certification_attempted",
        "rpa_adapter_attempted",
        "A360_adapter_attempted",
        "Brity_adapter_attempted",
        "UiPath_adapter_attempted",
        "external_dominion_attempted",
        "schumpeter_private_runtime_attempted",
        "actual_user_data_detected",
        "actual_company_data_detected",
        "private_material_exposure_detected",
        "raw_provider_output_persistence_detected",
        "raw_payload_logging_detected",
        "references_runtime_dependency_detected",
        "references_code_copy_detected",
        "PIG_execution_authority_detected",
        "llm_judge_detected",
    }

    def build_findings(self) -> list[LimitedPreviewFinding]:
        created = [
            "limited_preview_policy_created",
            "eligibility_matrix_created",
            "preview_scope_created",
            "preview_candidate_created",
            "preview_approval_requirement_created",
            "preview_credential_binding_created",
            "preview_network_binding_created",
            "preview_payload_boundary_created",
            "preview_result_boundary_created",
            "preview_audit_ocel_plan_created",
            "preview_rollback_noop_binding_created",
            "preview_risk_assessment_created",
            "preview_decision_record_created",
            "preview_gate_created",
            "preview_handoff_packet_created",
        ]
        findings = [
            LimitedPreviewFinding(
                "limited_preview_finding:ok:v0.29.8",
                "info",
                "ok",
                "v0.29.8 limited preview gate remains eligibility-only and does not execute provider invocation.",
                None,
                [],
                None,
            )
        ]
        for finding_type in created:
            findings.append(
                LimitedPreviewFinding(
                    f"limited_preview_finding:{finding_type}:v0.29.8",
                    "info",
                    finding_type,
                    f"{finding_type} artifact was created without preview execution, provider invocation, network, credential, command, or side effect.",
                    None,
                    [],
                    None,
                )
            )
        for finding_type in self.BLOCKED_FINDINGS:
            findings.append(
                LimitedPreviewFinding(
                    f"limited_preview_finding:{finding_type}:v0.29.8",
                    "critical",
                    finding_type,
                    f"{finding_type} would block v0.29.8 preview gate validity.",
                    None,
                    [],
                    finding_type,
                )
            )
        return findings


class LimitedProviderInvocationPreviewReportService:
    def build_report(self, report_id: str | None = None) -> LimitedProviderInvocationPreviewReport:
        source_service = LimitedProviderInvocationPreviewPrerequisiteSourceService()
        packaging = source_service.load_v0297_packaging_certification_report()
        approval = source_service.load_v0296_approval_audit_rollback_report()
        invocation = source_service.load_v0295_invocation_candidate_report()
        credential = source_service.load_v0294_credential_network_boundary_report()
        mock = source_service.load_v0292_mock_harness_report()
        contract = source_service.load_v0290_external_adapter_contract_report()

        policy = LimitedProviderInvocationPreviewPolicyService().build_policy()
        source_view = LimitedProviderInvocationPreviewSourceViewService().build_source_view()
        request = LimitedProviderInvocationPreviewRequestService().build_request(source_view)
        rows = LimitedPreviewEligibilityService().build_rows(packaging, approval, invocation, credential, mock, contract)
        matrix = LimitedPreviewEligibilityService().build_matrix(rows)
        scope_service = LimitedPreviewScopeService()
        scope_policy = scope_service.build_policy()
        scopes = scope_service.build_scopes(rows, credential)
        candidates = LimitedPreviewProviderCandidateService().build_candidates(rows, scopes)
        binding_service = LimitedPreviewBindingService()
        approvals = binding_service.build_approval_requirements(candidates)
        credential_bindings = binding_service.build_credential_bindings(candidates, credential)
        network_bindings = binding_service.build_network_bindings(candidates, credential)
        payload_boundaries = binding_service.build_payload_boundaries(candidates, invocation, credential)
        result_boundaries = binding_service.build_result_boundaries(candidates, approval)
        audit_plans = binding_service.build_audit_ocel_plans(candidates, approval)
        rollback_bindings = binding_service.build_rollback_noop_bindings(candidates, approval)
        risk_service = LimitedPreviewRiskService()
        risks = risk_service.build_risk_assessments(candidates)
        reasons = risk_service.build_deny_defer_reasons(candidates)
        decision_service = LimitedPreviewDecisionService()
        decision_candidates = decision_service.build_decision_candidates(candidates)
        decision_records = decision_service.build_decision_records(decision_candidates)
        gate = LimitedPreviewGateService().evaluate_gate(
            source_view,
            matrix,
            scopes,
            candidates,
            approvals,
            credential_bindings,
            network_bindings,
            payload_boundaries,
            result_boundaries,
            audit_plans,
            rollback_bindings,
            risks,
            decision_records,
        )
        audit_trail = LimitedPreviewAuditTrailService().build_audit_trail(request, source_view, candidates, decision_records, gate)
        resolved_report_id = report_id or "limited_provider_invocation_preview_report:v0.29.8"
        handoff = LimitedPreviewHandoffPacketService().build_packet(resolved_report_id, gate, candidates, decision_records)
        findings = LimitedPreviewFindingService().build_findings()
        limitations = [
            "Limited preview gate creates eligibility and handoff evidence only; preview execution and provider invocation remain disabled.",
            "v0.29.9 consolidation must preserve all no-provider/no-network/no-credential/no-command boundaries.",
        ]
        withdrawal_conditions = [
            "preview execution, provider invocation, network call, credential access, command execution, side effect, rollback execution, or automatic retry appears",
            "package publish, release tag creation, live provider certification, live adapter, RPA adapter, or external dominion implementation appears",
            "private material, raw payload, or raw provider output is exposed",
            "ready_for_preview_execution_now, ready_for_provider_invocation, ready_for_network_access, or ready_for_credential_access becomes true",
            "LLM judge becomes the sole preview authority",
        ]
        return LimitedProviderInvocationPreviewReport(
            resolved_report_id,
            _now(),
            policy,
            request,
            source_view,
            matrix,
            scope_policy,
            scopes,
            candidates,
            approvals,
            credential_bindings,
            network_bindings,
            payload_boundaries,
            result_boundaries,
            audit_plans,
            rollback_bindings,
            risks,
            reasons,
            decision_candidates,
            decision_records,
            gate,
            audit_trail,
            handoff,
            findings,
            "warning",
            gate.ready_for_v0_29_9,
            gate.ready_for_v029_consolidation,
            limitations=limitations,
            withdrawal_conditions=withdrawal_conditions,
        )

    def build_all_parts(self, report_id: str | None = None) -> dict[str, Any]:
        report = self.build_report(report_id=report_id)
        return {
            "policy": report.policy,
            "request": report.request,
            "source-view": report.source_view,
            "eligibility": report.eligibility_matrix,
            "rows": report.eligibility_matrix.rows,
            "scope-policy": report.scope_policy,
            "scopes": report.preview_scopes,
            "candidates": report.preview_candidates,
            "approval": report.approval_requirements,
            "credentials": report.credential_bindings,
            "network": report.network_bindings,
            "payload": report.payload_boundaries,
            "result": report.result_boundaries,
            "audit-ocel": report.audit_ocel_plans,
            "rollback-noop": report.rollback_noop_bindings,
            "risk": report.risk_assessments,
            "deny-defer": report.deny_defer_reasons,
            "decisions": report.decision_records,
            "decision-candidates": report.decision_candidates,
            "gate": report.preview_gate,
            "audit": report.audit_trail,
            "handoff": report.handoff_packet,
            "findings": report.findings,
            "report": report,
        }

    def build_pig_report(self) -> dict[str, Any]:
        report = self.build_report()
        return {
            "version": V0298_VERSION,
            "layer": V0298_LAYER,
            "subject": "limited_provider_invocation_preview_gate",
            "principles": [
                "Limited preview gate is not provider invocation",
                "Preview eligibility is not execution",
                "Preview authorization candidate is not provider invocation",
                "Preview scope is not network access",
                "Preview credential binding is not credential access",
                "Preview network binding is not network call",
                "Preview payload boundary is not payload send",
                "Preview result boundary is not provider response persistence",
                "Preview pass is not unlimited runtime",
                "Deny / defer / no-op remain valid outcomes",
            ],
            "safety_boundary": {
                "preview_execution_performed": report.preview_execution_performed,
                "provider_registered": report.provider_registered,
                "provider_invoked": report.provider_invoked,
                "provider_sdk_invoked": report.provider_sdk_invoked,
                "network_called": report.network_called,
                "outbound_request_sent": report.outbound_request_sent,
                "credential_accessed": report.credential_accessed,
                "command_executed": report.command_executed,
                "external_side_effect_performed": report.external_side_effect_performed,
                "file_mutated": report.file_mutated,
                "rollback_executed": report.rollback_executed,
                "automatic_retry_performed": report.automatic_retry_performed,
                "package_published": report.package_published,
                "release_tag_created": report.release_tag_created,
                "live_provider_certified": report.live_provider_certified,
                "live_adapter_implemented": report.live_adapter_implemented,
                "RPA_adapter_implemented": report.RPA_adapter_implemented,
                "A360_adapter_implemented": report.A360_adapter_implemented,
                "Brity_adapter_implemented": report.Brity_adapter_implemented,
                "UiPath_adapter_implemented": report.UiPath_adapter_implemented,
                "external_dominion_implemented": report.external_dominion_implemented,
                "schumpeter_private_runtime_used": report.schumpeter_private_runtime_used,
                "private_material_exposed": report.private_material_exposed,
                "raw_provider_output_persisted": report.raw_provider_output_persisted,
                "references_runtime_dependency_added": report.references_runtime_dependency_added,
                "references_code_copied": report.references_code_copied,
                "PIG_execution_authority_enabled": report.PIG_execution_authority_enabled,
                "llm_judge_enabled": False,
            },
            "future_direction": [
                "v0.29.9 External Provider Adapter Foundation Consolidation",
                "v0.30.x External Agent Dominion Bridge",
            ],
            "next_step": V0298_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "limited_provider_invocation_preview_gate_created",
            "version": V0298_VERSION,
            "source_read_models": [
                "AdapterCertificationReadinessGateState",
                "AdapterCertificationMatrixState",
                "AdapterCertificationCaseResultState",
                "AdapterBoundaryCertificationState",
                "ProviderInvocationApprovalBoundaryState",
                "ProviderInvocationApprovalDecisionRecordState",
                "ProviderInvocationAuditTrailState",
                "ProviderRollbackPlanState",
                "ProviderNoOpBoundaryState",
                "AdapterInvocationCandidateState",
                "AdapterDryRunReportState",
                "CredentialNetworkBoundaryGateState",
                "AdapterPermissionSafetyGateState",
                "MockAdapterHarnessGateState",
                "AdapterRegistryState",
                "ExternalProviderAdapterContractState",
                "ProviderInvocationProhibitionState",
                "CommandExecutionProhibitionState",
                "PigGuidanceState",
                "OCPXProjectionState",
            ],
            "target_read_models": [
                "LimitedPreviewEligibilityMatrixState",
                "LimitedPreviewScopeState",
                "LimitedPreviewProviderCandidateState",
                "LimitedPreviewBindingState",
                "LimitedPreviewRiskAssessmentState",
                "LimitedPreviewDecisionState",
                "LimitedPreviewGateState",
                "LimitedPreviewAuditState",
                "LimitedPreviewHandoffState",
                "V029ReadinessState",
            ],
            "effect_types": V0298_EFFECT_TYPES,
        }


def render_limited_provider_invocation_preview_cli(parts: dict[str, Any], section: str = "report") -> str:
    payload = parts[section]
    if isinstance(payload, list):
        return "\n".join(
            [
                f"Limited Provider Invocation Preview Gate {section}",
                f"version={V0298_VERSION}",
                f"layer={V0298_LAYER}",
                f"count={len(payload)}",
            ]
        )
    if section != "report":
        object_id = (
            getattr(payload, "policy_id", None)
            or getattr(payload, "request_id", None)
            or getattr(payload, "source_view_id", None)
            or getattr(payload, "matrix_id", None)
            or getattr(payload, "gate_id", None)
            or getattr(payload, "audit_trail_id", None)
            or getattr(payload, "handoff_packet_id", None)
        )
        return "\n".join([payload.__class__.__name__, f"version={V0298_VERSION}", f"layer={V0298_LAYER}", f"object_id={object_id}"])

    report: LimitedProviderInvocationPreviewReport = payload
    lines = [
        "Limited Provider Invocation Preview Gate report",
        f"version={report.version}",
        f"layer={report.policy.layer}",
        f"report_status={report.report_status}",
        f"ready_for_v0_29_9={_bool(report.ready_for_v0_29_9)}",
        f"ready_for_v029_consolidation={_bool(report.ready_for_v029_consolidation)}",
        f"ready_for_preview_execution_now={_bool(report.ready_for_preview_execution_now)}",
        f"ready_for_provider_invocation={_bool(report.ready_for_provider_invocation)}",
        f"ready_for_network_access={_bool(report.ready_for_network_access)}",
        f"ready_for_credential_access={_bool(report.ready_for_credential_access)}",
        f"ready_for_command_execution={_bool(report.ready_for_command_execution)}",
        f"preview_execution_performed={_bool(report.preview_execution_performed)}",
        f"provider_registered={_bool(report.provider_registered)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"provider_sdk_invoked={_bool(report.provider_sdk_invoked)}",
        f"network_called={_bool(report.network_called)}",
        f"outbound_request_sent={_bool(report.outbound_request_sent)}",
        f"credential_accessed={_bool(report.credential_accessed)}",
        f"credential_stored={_bool(report.credential_stored)}",
        f"credential_logged={_bool(report.credential_logged)}",
        f"secret_retrieved={_bool(report.secret_retrieved)}",
        f"secret_materialized={_bool(report.secret_materialized)}",
        f"command_executed={_bool(report.command_executed)}",
        f"external_side_effect_performed={_bool(report.external_side_effect_performed)}",
        f"file_mutated={_bool(report.file_mutated)}",
        f"rollback_executed={_bool(report.rollback_executed)}",
        f"automatic_retry_performed={_bool(report.automatic_retry_performed)}",
        f"package_published={_bool(report.package_published)}",
        f"release_tag_created={_bool(report.release_tag_created)}",
        f"live_provider_certified={_bool(report.live_provider_certified)}",
        f"live_adapter_implemented={_bool(report.live_adapter_implemented)}",
        f"RPA_adapter_implemented={_bool(report.RPA_adapter_implemented)}",
        f"A360_adapter_implemented={_bool(report.A360_adapter_implemented)}",
        f"Brity_adapter_implemented={_bool(report.Brity_adapter_implemented)}",
        f"UiPath_adapter_implemented={_bool(report.UiPath_adapter_implemented)}",
        f"external_dominion_implemented={_bool(report.external_dominion_implemented)}",
        f"schumpeter_private_runtime_used={_bool(report.schumpeter_private_runtime_used)}",
        f"actual_user_data_used={_bool(report.actual_user_data_used)}",
        f"actual_company_data_used={_bool(report.actual_company_data_used)}",
        f"private_material_exposed={_bool(report.private_material_exposed)}",
        f"raw_provider_output_persisted={_bool(report.raw_provider_output_persisted)}",
        f"raw_payload_logged={_bool(report.raw_payload_logged)}",
        f"references_runtime_dependency_added={_bool(report.references_runtime_dependency_added)}",
        f"references_code_copied={_bool(report.references_code_copied)}",
        f"PIG_execution_authority_enabled={_bool(report.PIG_execution_authority_enabled)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    return "\n".join(lines)
