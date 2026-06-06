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
from chanta_core.external_provider_adapter_contract import ModelMixin, _bool, _ref
from chanta_core.mock_adapter_harness_no_network_default import MockAdapterHarnessReportService
from chanta_core.permission_safety_scope_gate_for_external_adapters import (
    AdapterPermissionSafetyReport,
    AdapterPermissionSafetyReportService,
)
from chanta_core.provider_capability_inventory_adapter_registry import AdapterRegistryReportService
from chanta_core.utility.time import utc_now_iso


V0296_VERSION = "v0.29.6"
V0296_LAYER = "external_provider_adapter"
V0296_TRACK = "External Skill / External Provider Adapter Development"
V0296_NAME = "Provider Invocation Approval / Audit / Rollback Boundary"
V0296_NEXT_STEP = "v0.29.7 External Skill Packaging / Certification Matrix"

V0296_OBJECT_TYPES = [
    "provider_invocation_approval_audit_rollback_policy",
    "provider_invocation_approval_audit_rollback_request",
    "provider_invocation_approval_audit_rollback_source_view",
    "provider_invocation_approval_requirement",
    "provider_invocation_approval_candidate",
    "provider_invocation_approval_decision_candidate",
    "provider_invocation_approval_decision_record",
    "provider_invocation_approval_scope_summary",
    "provider_invocation_approval_expiry_policy",
    "provider_invocation_approval_revalidation_policy",
    "provider_invocation_audit_policy",
    "provider_invocation_audit_event_plan",
    "provider_invocation_audit_trail",
    "provider_invocation_ocel_trace_policy",
    "provider_invocation_ocel_trace_plan",
    "provider_result_boundary_policy",
    "provider_result_persistence_policy",
    "provider_failure_classification",
    "provider_failure_handling_policy",
    "provider_rollback_boundary_policy",
    "provider_rollback_plan",
    "provider_noop_boundary",
    "provider_retry_deferral_policy",
    "provider_invocation_approval_audit_rollback_gate",
    "provider_invocation_approval_audit_rollback_finding",
    "provider_invocation_approval_audit_rollback_report",
    "adapter_invocation_candidate_report",
    "credential_network_boundary_report",
    "adapter_permission_safety_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

V0296_EVENT_TYPES = [
    "provider_invocation_approval_audit_rollback_requested",
    "provider_invocation_approval_audit_rollback_prerequisites_loaded",
    "provider_invocation_approval_audit_rollback_policy_created",
    "provider_invocation_approval_requirement_created",
    "provider_invocation_approval_candidate_created",
    "provider_invocation_approval_decision_candidate_created",
    "provider_invocation_approval_decision_record_created",
    "provider_invocation_approval_scope_summary_created",
    "provider_invocation_approval_expiry_policy_created",
    "provider_invocation_approval_revalidation_policy_created",
    "provider_invocation_audit_policy_created",
    "provider_invocation_audit_event_plan_created",
    "provider_invocation_audit_trail_created",
    "provider_invocation_ocel_trace_policy_created",
    "provider_invocation_ocel_trace_plan_created",
    "provider_result_boundary_policy_created",
    "provider_result_persistence_policy_created",
    "provider_failure_classification_created",
    "provider_failure_handling_policy_created",
    "provider_rollback_boundary_policy_created",
    "provider_rollback_plan_created",
    "provider_noop_boundary_created",
    "provider_retry_deferral_policy_created",
    "provider_invocation_approval_audit_rollback_gate_evaluated",
    "provider_invocation_approval_audit_rollback_report_created",
    "provider_invocation_approval_audit_rollback_warning_created",
    "provider_invocation_approval_audit_rollback_blocked",
]

V0296_EFFECT_TYPES = [
    "read_only_observation",
    "provider_invocation_approval_requirement_created",
    "provider_invocation_approval_candidate_created",
    "provider_invocation_approval_decision_record_created",
    "provider_invocation_audit_plan_created",
    "provider_invocation_ocel_trace_plan_created",
    "provider_result_boundary_created",
    "provider_failure_classification_created",
    "provider_rollback_plan_created",
    "provider_noop_boundary_created",
    "provider_invocation_approval_audit_rollback_gate_evaluated",
    "state_candidate_created",
]

V0296_FORBIDDEN_EFFECT_TYPES = [
    "approval_granted",
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

AUDIT_EVENT_NAMES = [
    "approval_requirement_recorded",
    "approval_candidate_recorded",
    "approval_decision_recorded",
    "scope_summary_recorded",
    "credential_reference_checked",
    "network_boundary_checked",
    "payload_boundary_checked",
    "effect_preview_recorded",
    "risk_preview_recorded",
    "failure_classification_recorded",
    "rollback_plan_recorded",
    "noop_boundary_recorded",
    "ocel_trace_plan_recorded",
]

TRACE_EVENT_TYPES = [
    "provider_approval_requirement_recorded",
    "provider_approval_candidate_created",
    "provider_approval_decision_recorded",
    "provider_audit_plan_created",
    "provider_failure_classification_created",
    "provider_rollback_plan_created",
    "provider_noop_boundary_created",
    "provider_invocation_boundary_gate_evaluated",
]

TRACE_OBJECT_TYPES = [
    "adapter_invocation_candidate",
    "provider_approval_candidate",
    "provider_approval_decision_record",
    "provider_audit_plan",
    "provider_rollback_plan",
    "provider_noop_boundary",
    "provider_failure_classification",
]

FAILURE_MODES = [
    "missing_permission",
    "missing_approval",
    "missing_credential",
    "missing_network_boundary",
    "schema_mismatch",
    "provider_error",
    "timeout",
    "auth_failure",
    "rate_limit",
    "unsafe_payload",
    "unsafe_result",
    "rollback_unavailable",
    "unknown",
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
class ProviderInvocationApprovalAuditRollbackPolicy(ModelMixin):
    policy_id: str
    approval_boundary_enabled: bool = True
    audit_boundary_enabled: bool = True
    rollback_boundary_enabled: bool = True
    approval_required_before_provider_invocation: bool = True
    audit_required_before_provider_invocation: bool = True
    rollback_or_noop_required_before_provider_invocation: bool = True
    approval_candidate_is_not_approval_grant: bool = True
    approval_record_is_not_provider_invocation: bool = True
    audit_policy_is_not_raw_result_persistence: bool = True
    rollback_plan_is_not_rollback_execution: bool = True
    no_op_boundary_required: bool = True
    failure_classification_required: bool = True
    result_boundary_required: bool = True
    ocel_trace_required: bool = True
    provider_invocation_enabled_now: bool = False
    provider_sdk_invocation_enabled_now: bool = False
    network_access_enabled_now: bool = False
    credential_access_enabled_now: bool = False
    command_execution_expansion_enabled_now: bool = False
    rollback_execution_enabled_now: bool = False
    automatic_retry_enabled_now: bool = False
    live_adapter_implementation_enabled_now: bool = False
    rpa_adapter_enabled_now: bool = False
    external_agent_dominion_enabled_now: bool = False
    no_provider_invocation_default: bool = True
    no_network_default: bool = True
    no_credential_value_default: bool = True
    no_command_execution_default: bool = True
    llm_judge_as_sole_approval_authority_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION
    layer: str = V0296_LAYER


@dataclass
class ProviderInvocationApprovalAuditRollbackRequest(ModelMixin):
    request_id: str
    invocation_candidate_report_id: str | None
    credential_network_boundary_report_id: str | None
    permission_safety_report_id: str | None
    requested_boundary_scope: str = "full_approval_audit_rollback_boundary"
    strictness: str = "standard"
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION


@dataclass
class ProviderInvocationApprovalAuditRollbackSourceView(ModelMixin):
    source_view_id: str
    invocation_candidate_report_ref: dict[str, Any] | None
    invocation_readiness_gate_ref: dict[str, Any] | None
    invocation_candidate_refs: list[dict[str, Any]]
    dry_run_report_refs: list[dict[str, Any]]
    risk_preview_refs: list[dict[str, Any]]
    effect_preview_refs: list[dict[str, Any]]
    noop_plan_refs: list[dict[str, Any]]
    failure_mode_preview_refs: list[dict[str, Any]]
    credential_network_boundary_report_ref: dict[str, Any] | None
    credential_access_candidate_refs: list[dict[str, Any]]
    network_request_candidate_refs: list[dict[str, Any]]
    permission_safety_report_ref: dict[str, Any] | None
    permission_decision_record_refs: list[dict[str, Any]]
    user_approval_requirement_refs: list[dict[str, Any]]
    mock_harness_report_ref: dict[str, Any] | None
    adapter_registry_report_ref: dict[str, Any] | None
    audit_requirement_contract_ref: dict[str, Any] | None
    rollback_noop_requirement_contract_ref: dict[str, Any] | None
    ocel_visibility_contract_ref: dict[str, Any] | None
    provider_invocation_prohibition_ref: dict[str, Any] | None
    command_execution_prohibition_ref: dict[str, Any] | None
    source_status: str
    invocation_candidate_ready_for_approval_boundary: bool | None
    credential_network_ready_for_approval_boundary: bool | None
    permission_safety_ready_for_approval_boundary: bool | None
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
    private_data_detected: bool = False
    raw_provider_output_detected: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION


@dataclass
class ProviderInvocationApprovalRequirement(ModelMixin):
    requirement_id: str
    candidate_ref: dict[str, Any]
    adapter_name: str
    capability_name: str
    approval_required: bool
    approval_reason: str
    approval_scope_summary_required: bool = True
    approval_expiry_required: bool = True
    approval_revalidation_required: bool = True
    approval_record_required: bool = True
    explicit_user_approval_required_later: bool = True
    approval_requirement_is_approval_grant: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION


@dataclass
class ProviderInvocationApprovalCandidate(ModelMixin):
    approval_candidate_id: str
    candidate_ref: dict[str, Any]
    approval_requirement_ref: dict[str, Any]
    permission_decision_ref: dict[str, Any] | None
    risk_preview_ref: dict[str, Any] | None
    effect_preview_ref: dict[str, Any] | None
    approval_candidate_status: str
    approval_candidate_summary: str
    approval_candidate_is_approval_grant: bool = False
    approval_candidate_is_execution: bool = False
    provider_invoked_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION


@dataclass
class ProviderInvocationApprovalDecisionCandidate(ModelMixin):
    decision_candidate_id: str
    approval_candidate_ref: dict[str, Any]
    proposed_decision: str
    decision_reason: str
    required_future_version: str | None
    approval_granted_now: bool = False
    provider_invoked_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION


@dataclass
class ProviderInvocationApprovalDecisionRecord(ModelMixin):
    decision_record_id: str
    decision_candidate_ref: dict[str, Any]
    final_decision: str
    decision_reason: str
    approval_granted_now: bool = False
    provider_invoked_now: bool = False
    network_called_now: bool = False
    credential_accessed_now: bool = False
    command_executed_now: bool = False
    rollback_executed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION


@dataclass
class ProviderInvocationApprovalScopeSummary(ModelMixin):
    scope_summary_id: str
    approval_candidate_ref: dict[str, Any]
    adapter_name: str
    capability_name: str
    scope_summary: str
    provider_scope: str | None
    credential_scope_ref: dict[str, Any] | None
    network_scope_ref: dict[str, Any] | None
    payload_scope_summary: str
    result_scope_summary: str
    scope_is_minimal: bool
    scope_is_expiring: bool
    scope_summary_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION


@dataclass
class ProviderInvocationApprovalExpiryPolicy(ModelMixin):
    policy_id: str
    approval_expiry_required: bool = True
    permanent_approval_forbidden: bool = True
    approval_reuse_forbidden_without_revalidation: bool = True
    expired_approval_requires_reapproval: bool = True
    approval_scope_change_requires_reapproval: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION


@dataclass
class ProviderInvocationApprovalRevalidationPolicy(ModelMixin):
    policy_id: str
    revalidation_required_before_preview: bool = True
    revalidate_permission_scope: bool = True
    revalidate_safety_classification: bool = True
    revalidate_credential_boundary: bool = True
    revalidate_network_boundary: bool = True
    revalidate_payload_boundary: bool = True
    revalidate_result_boundary: bool = True
    revalidation_is_not_execution: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION


@dataclass
class ProviderInvocationAuditPolicy(ModelMixin):
    policy_id: str
    audit_required: bool = True
    approval_audit_required: bool = True
    invocation_candidate_audit_required: bool = True
    credential_reference_audit_required: bool = True
    network_candidate_audit_required: bool = True
    payload_preview_audit_required: bool = True
    effect_preview_audit_required: bool = True
    risk_preview_audit_required: bool = True
    failure_classification_audit_required: bool = True
    rollback_plan_audit_required: bool = True
    future_provider_result_audit_required: bool = True
    raw_provider_output_audit_forbidden: bool = True
    credential_value_audit_forbidden: bool = True
    raw_payload_audit_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION


@dataclass
class ProviderInvocationAuditEventPlan(ModelMixin):
    audit_event_plan_id: str
    candidate_ref: dict[str, Any]
    required_audit_events: list[str]
    audit_plan_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION


@dataclass
class ProviderInvocationAuditTrail(ModelMixin):
    audit_trail_id: str
    request_ref: dict[str, Any]
    source_view_ref: dict[str, Any]
    approval_candidate_refs: list[dict[str, Any]]
    approval_decision_record_refs: list[dict[str, Any]]
    audit_event_plan_refs: list[dict[str, Any]]
    rollback_plan_refs: list[dict[str, Any]]
    noop_boundary_refs: list[dict[str, Any]]
    audit_event_count: int
    raw_content_included: bool = False
    credential_value_included: bool = False
    raw_payload_included: bool = False
    raw_provider_output_included: bool = False
    audit_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION


@dataclass
class ProviderInvocationOCELTracePolicy(ModelMixin):
    policy_id: str
    ocel_trace_required: bool = True
    approval_requirement_event_required: bool = True
    approval_candidate_event_required: bool = True
    approval_decision_event_required: bool = True
    audit_plan_event_required: bool = True
    rollback_plan_event_required: bool = True
    noop_boundary_event_required: bool = True
    failure_classification_event_required: bool = True
    future_provider_invocation_event_required: bool = True
    provider_invocation_event_emitted_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION


@dataclass
class ProviderInvocationOCELTracePlan(ModelMixin):
    trace_plan_id: str
    candidate_ref: dict[str, Any]
    required_event_types: list[str]
    required_object_types: list[str]
    provider_invocation_event_forbidden_now: bool = True
    trace_plan_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION


@dataclass
class ProviderResultBoundaryPolicy(ModelMixin):
    policy_id: str
    provider_result_boundary_required: bool = True
    raw_provider_output_persistence_forbidden: bool = True
    raw_provider_output_memory_write_forbidden: bool = True
    result_summary_required_later: bool = True
    result_schema_validation_required_later: bool = True
    result_redaction_required_later: bool = True
    result_audit_required_later: bool = True
    result_boundary_is_not_provider_response: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION


@dataclass
class ProviderResultPersistencePolicy(ModelMixin):
    policy_id: str
    raw_result_persistence_forbidden: bool = True
    raw_result_logging_forbidden: bool = True
    result_summary_only_by_default_later: bool = True
    redacted_result_boundary_required_later: bool = True
    provider_result_persisted_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION


@dataclass
class ProviderFailureClassification(ModelMixin):
    classification_id: str
    candidate_ref: dict[str, Any]
    possible_failure_modes: list[str]
    failure_severity: str
    rollback_required_later: bool
    noop_fallback_available: bool
    classification_status: str
    retry_allowed_now: bool = False
    automatic_retry_allowed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION


@dataclass
class ProviderFailureHandlingPolicy(ModelMixin):
    policy_id: str
    failure_handling_required: bool = True
    automatic_retry_forbidden_now: bool = True
    retry_requires_future_policy: bool = True
    auth_failure_retry_forbidden: bool = True
    rate_limit_retry_requires_future_policy: bool = True
    timeout_handling_required_later: bool = True
    failure_must_emit_ocel_later: bool = True
    noop_on_uncertain_failure_allowed: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION


@dataclass
class ProviderRollbackBoundaryPolicy(ModelMixin):
    policy_id: str
    rollback_boundary_required: bool = True
    rollback_plan_required_before_side_effect: bool = True
    rollback_execution_enabled_now: bool = False
    rollback_without_audit_forbidden: bool = True
    rollback_without_original_action_ref_forbidden: bool = True
    rollback_must_be_scope_limited: bool = True
    noop_fallback_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION


@dataclass
class ProviderRollbackPlan(ModelMixin):
    rollback_plan_id: str
    candidate_ref: dict[str, Any]
    effect_preview_ref: dict[str, Any] | None
    rollback_available: bool
    rollback_strategy: str
    rollback_scope_summary: str
    rollback_requires_future_approval: bool = True
    rollback_executed_now: bool = False
    rollback_plan_is_rollback_execution: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION


@dataclass
class ProviderNoOpBoundary(ModelMixin):
    noop_boundary_id: str
    candidate_ref: dict[str, Any]
    noop_reason: str
    noop_available: bool = True
    noop_is_valid_decision: bool = True
    noop_is_execution: bool = False
    side_effect_performed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION


@dataclass
class ProviderRetryDeferralPolicy(ModelMixin):
    policy_id: str
    automatic_retry_enabled_now: bool = False
    retry_policy_deferred: bool = True
    retry_requires_future_boundary: bool = True
    retry_requires_audit: bool = True
    retry_requires_rate_limit_policy: bool = True
    retry_requires_user_or_policy_approval: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION


@dataclass
class ProviderInvocationApprovalAuditRollbackGate(ModelMixin):
    gate_id: str
    source_view_ref: dict[str, Any]
    approval_requirement_refs: list[dict[str, Any]]
    approval_candidate_refs: list[dict[str, Any]]
    approval_decision_record_refs: list[dict[str, Any]]
    scope_summary_refs: list[dict[str, Any]]
    audit_policy_ref: dict[str, Any]
    audit_event_plan_refs: list[dict[str, Any]]
    ocel_trace_plan_refs: list[dict[str, Any]]
    result_boundary_policy_ref: dict[str, Any]
    result_persistence_policy_ref: dict[str, Any]
    failure_classification_refs: list[dict[str, Any]]
    failure_handling_policy_ref: dict[str, Any]
    rollback_boundary_policy_ref: dict[str, Any]
    rollback_plan_refs: list[dict[str, Any]]
    noop_boundary_refs: list[dict[str, Any]]
    retry_deferral_policy_ref: dict[str, Any]
    approval_requirements_complete: bool
    approval_candidates_complete: bool
    approval_decisions_recorded: bool
    scope_summaries_complete: bool
    audit_boundary_complete: bool
    ocel_trace_boundary_complete: bool
    result_boundary_complete: bool
    failure_classification_complete: bool
    rollback_or_noop_boundary_complete: bool
    retry_deferred: bool
    no_approval_granted: bool
    no_provider_invocation: bool
    no_network_call: bool
    no_credential_access: bool
    no_command_execution: bool
    no_external_side_effect: bool
    no_rollback_execution: bool
    gate_status: str
    ready_for_v0_29_7: bool
    ready_for_certification_matrix: bool
    ready_for_limited_invocation_preview: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0296_VERSION


@dataclass
class ProviderInvocationApprovalAuditRollbackFinding(ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class ProviderInvocationApprovalAuditRollbackReport(ModelMixin):
    report_id: str
    created_at: str
    policy: ProviderInvocationApprovalAuditRollbackPolicy
    request: ProviderInvocationApprovalAuditRollbackRequest
    source_view: ProviderInvocationApprovalAuditRollbackSourceView
    approval_requirements: list[ProviderInvocationApprovalRequirement]
    approval_candidates: list[ProviderInvocationApprovalCandidate]
    approval_decision_candidates: list[ProviderInvocationApprovalDecisionCandidate]
    approval_decision_records: list[ProviderInvocationApprovalDecisionRecord]
    approval_scope_summaries: list[ProviderInvocationApprovalScopeSummary]
    approval_expiry_policy: ProviderInvocationApprovalExpiryPolicy
    approval_revalidation_policy: ProviderInvocationApprovalRevalidationPolicy
    audit_policy: ProviderInvocationAuditPolicy
    audit_event_plans: list[ProviderInvocationAuditEventPlan]
    audit_trail: ProviderInvocationAuditTrail
    ocel_trace_policy: ProviderInvocationOCELTracePolicy
    ocel_trace_plans: list[ProviderInvocationOCELTracePlan]
    result_boundary_policy: ProviderResultBoundaryPolicy
    result_persistence_policy: ProviderResultPersistencePolicy
    failure_classifications: list[ProviderFailureClassification]
    failure_handling_policy: ProviderFailureHandlingPolicy
    rollback_boundary_policy: ProviderRollbackBoundaryPolicy
    rollback_plans: list[ProviderRollbackPlan]
    noop_boundaries: list[ProviderNoOpBoundary]
    retry_deferral_policy: ProviderRetryDeferralPolicy
    approval_audit_rollback_gate: ProviderInvocationApprovalAuditRollbackGate
    findings: list[ProviderInvocationApprovalAuditRollbackFinding]
    report_status: str
    ready_for_v0_29_7: bool
    ready_for_certification_matrix: bool
    ready_for_limited_invocation_preview: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    approval_granted: bool = False
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
    next_required_step: str = V0296_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.29.7 External Skill Packaging / Certification Matrix begins or Provider Invocation Approval / Audit / Rollback policy changes."
    version: str = V0296_VERSION


class ProviderInvocationApprovalAuditRollbackPrerequisiteSourceService:
    def load_v0295_invocation_candidate_report(self) -> AdapterInvocationCandidateReport:
        return AdapterInvocationCandidateReportService().build_report()

    def load_v0295_invocation_readiness_gate(self) -> Any:
        return self.load_v0295_invocation_candidate_report().readiness_gate

    def load_invocation_candidates(self) -> list[Any]:
        return self.load_v0295_invocation_candidate_report().invocation_candidates

    def load_dry_run_reports(self) -> list[Any]:
        return self.load_v0295_invocation_candidate_report().dry_run_reports

    def load_risk_previews(self) -> list[Any]:
        return self.load_v0295_invocation_candidate_report().risk_previews

    def load_effect_previews(self) -> list[Any]:
        return self.load_v0295_invocation_candidate_report().effect_previews

    def load_noop_plans(self) -> list[Any]:
        return self.load_v0295_invocation_candidate_report().noop_plans

    def load_failure_mode_previews(self) -> list[Any]:
        return self.load_v0295_invocation_candidate_report().failure_mode_previews

    def load_v0294_credential_network_boundary_report(self) -> CredentialNetworkBoundaryReport:
        return CredentialNetworkBoundaryReportService().build_report()

    def load_credential_access_candidates(self) -> list[Any]:
        return self.load_v0294_credential_network_boundary_report().credential_access_candidates

    def load_network_request_candidates(self) -> list[Any]:
        return self.load_v0294_credential_network_boundary_report().network_request_candidates

    def load_v0293_permission_safety_report(self) -> AdapterPermissionSafetyReport:
        return AdapterPermissionSafetyReportService().build_report()

    def load_permission_decision_records(self) -> list[Any]:
        return self.load_v0293_permission_safety_report().decision_records

    def load_user_approval_requirements(self) -> list[Any]:
        return self.load_v0293_permission_safety_report().approval_requirements

    def load_v0292_mock_harness_report(self) -> Any:
        return MockAdapterHarnessReportService().build_report()

    def load_v0291_adapter_registry_report(self) -> Any:
        return AdapterRegistryReportService().build_report()

    def load_v0290_audit_rollback_ocel_contracts(self) -> dict[str, dict[str, Any]]:
        return {
            "audit": _ref("adapter_audit_requirement_contract", "adapter_audit_requirement_contract:v0.29.0", "v0.29.0"),
            "rollback": _ref("adapter_rollback_noop_requirement_contract", "adapter_rollback_noop_requirement_contract:v0.29.0", "v0.29.0"),
            "ocel": _ref("adapter_ocel_visibility_contract", "adapter_ocel_visibility_contract:v0.29.0", "v0.29.0"),
        }

    def load_provider_invocation_prohibition_contract(self) -> dict[str, Any]:
        return _ref("provider_invocation_prohibition_contract", "provider_invocation_prohibition_contract:v0.29.0", "v0.29.0")

    def load_command_execution_prohibition_contract(self) -> dict[str, Any]:
        return _ref("command_execution_prohibition_contract", "command_execution_prohibition_contract:v0.29.0", "v0.29.0")


class ProviderInvocationApprovalAuditRollbackPolicyService:
    def build_policy(self) -> ProviderInvocationApprovalAuditRollbackPolicy:
        return ProviderInvocationApprovalAuditRollbackPolicy("provider_invocation_approval_audit_rollback_policy:v0.29.6")


class ProviderInvocationApprovalAuditRollbackSourceViewService:
    def build_source_view(self) -> ProviderInvocationApprovalAuditRollbackSourceView:
        source = ProviderInvocationApprovalAuditRollbackPrerequisiteSourceService()
        invocation_report = source.load_v0295_invocation_candidate_report()
        credential_report = source.load_v0294_credential_network_boundary_report()
        permission_report = source.load_v0293_permission_safety_report()
        mock_report = source.load_v0292_mock_harness_report()
        registry_report = source.load_v0291_adapter_registry_report()
        contracts = source.load_v0290_audit_rollback_ocel_contracts()
        return ProviderInvocationApprovalAuditRollbackSourceView(
            "provider_invocation_approval_audit_rollback_source_view:v0.29.6",
            _ref("adapter_invocation_candidate_report", invocation_report.report_id, "v0.29.5"),
            _ref("adapter_invocation_readiness_gate", invocation_report.readiness_gate.gate_id, "v0.29.5"),
            _refs("adapter_invocation_candidate", invocation_report.invocation_candidates, "candidate_id", "v0.29.5"),
            _refs("adapter_invocation_dry_run_report", invocation_report.dry_run_reports, "report_id", "v0.29.5"),
            _refs("adapter_invocation_risk_preview", invocation_report.risk_previews, "risk_preview_id", "v0.29.5"),
            _refs("adapter_invocation_effect_preview", invocation_report.effect_previews, "effect_preview_id", "v0.29.5"),
            _refs("adapter_invocation_noop_plan", invocation_report.noop_plans, "noop_plan_id", "v0.29.5"),
            _refs("adapter_invocation_failure_mode_preview", invocation_report.failure_mode_previews, "failure_preview_id", "v0.29.5"),
            _ref("credential_network_boundary_report", credential_report.report_id, "v0.29.4"),
            _refs("credential_access_candidate", credential_report.credential_access_candidates, "candidate_id", "v0.29.4"),
            _refs("network_request_candidate", credential_report.network_request_candidates, "candidate_id", "v0.29.4"),
            _ref("adapter_permission_safety_report", permission_report.report_id, "v0.29.3"),
            _refs("adapter_permission_decision_record", permission_report.decision_records, "decision_record_id", "v0.29.3"),
            _refs("user_approval_requirement", permission_report.approval_requirements, "requirement_id", "v0.29.3"),
            _ref("mock_adapter_harness_report", mock_report.report_id, "v0.29.2"),
            _ref("adapter_registry_report", registry_report.report_id, "v0.29.1"),
            contracts["audit"],
            contracts["rollback"],
            contracts["ocel"],
            source.load_provider_invocation_prohibition_contract(),
            source.load_command_execution_prohibition_contract(),
            "complete",
            invocation_report.ready_for_approval_audit_rollback_boundary,
            credential_report.ready_for_invocation_candidate,
            permission_report.ready_for_v0_29_4,
        )


class ProviderInvocationApprovalAuditRollbackRequestService:
    def build_request(self, source_view: ProviderInvocationApprovalAuditRollbackSourceView) -> ProviderInvocationApprovalAuditRollbackRequest:
        refs = [
            ref
            for ref in [
                source_view.invocation_candidate_report_ref,
                source_view.credential_network_boundary_report_ref,
                source_view.permission_safety_report_ref,
            ]
            if ref is not None
        ]
        return ProviderInvocationApprovalAuditRollbackRequest(
            "provider_invocation_approval_audit_rollback_request:v0.29.6",
            source_view.invocation_candidate_report_ref.get("object_id") if source_view.invocation_candidate_report_ref else None,
            source_view.credential_network_boundary_report_ref.get("object_id") if source_view.credential_network_boundary_report_ref else None,
            source_view.permission_safety_report_ref.get("object_id") if source_view.permission_safety_report_ref else None,
            source_refs=refs,
        )


class ProviderInvocationApprovalService:
    def build_requirements(self, invocation_report: AdapterInvocationCandidateReport) -> list[ProviderInvocationApprovalRequirement]:
        return [
            ProviderInvocationApprovalRequirement(
                f"provider_invocation_approval_requirement:{candidate.adapter_name}:v0.29.6",
                _ref("adapter_invocation_candidate", candidate.candidate_id, "v0.29.5"),
                candidate.adapter_name,
                candidate.capability_name,
                True,
                "Explicit user approval is required later before any provider invocation can be considered.",
            )
            for candidate in invocation_report.invocation_candidates
        ]

    def build_candidates(
        self,
        requirements: list[ProviderInvocationApprovalRequirement],
        invocation_report: AdapterInvocationCandidateReport,
        permission_report: AdapterPermissionSafetyReport,
    ) -> list[ProviderInvocationApprovalCandidate]:
        candidates: list[ProviderInvocationApprovalCandidate] = []
        for index, requirement in enumerate(requirements):
            invocation_candidate = invocation_report.invocation_candidates[index]
            decision = _safe_get(permission_report.decision_records, index)
            risk = _safe_get(invocation_report.risk_previews, index)
            effect = _safe_get(invocation_report.effect_previews, index)
            status = "deferred" if invocation_candidate.candidate_status in {"deferred", "blocked"} else "allowed_candidate"
            candidates.append(
                ProviderInvocationApprovalCandidate(
                    f"provider_invocation_approval_candidate:{invocation_candidate.adapter_name}:v0.29.6",
                    _ref("adapter_invocation_candidate", invocation_candidate.candidate_id, "v0.29.5"),
                    _ref("provider_invocation_approval_requirement", requirement.requirement_id, V0296_VERSION),
                    _ref("adapter_permission_decision_record", decision.decision_record_id, "v0.29.3") if decision else None,
                    _ref("adapter_invocation_risk_preview", risk.risk_preview_id, "v0.29.5") if risk else None,
                    _ref("adapter_invocation_effect_preview", effect.effect_preview_id, "v0.29.5") if effect else None,
                    status,
                    "Approval candidate is recorded for future human/policy decision only; it is not approval or execution.",
                )
            )
        return candidates

    def build_decision_candidates(self, approval_candidates: list[ProviderInvocationApprovalCandidate]) -> list[ProviderInvocationApprovalDecisionCandidate]:
        decisions: list[ProviderInvocationApprovalDecisionCandidate] = []
        for candidate in approval_candidates:
            proposed = "require_certification" if candidate.approval_candidate_status == "allowed_candidate" else "defer"
            future = "v0.29.7 External Skill Packaging / Certification Matrix" if proposed == "require_certification" else "v0.29.8 Limited Provider Invocation Preview Gate"
            decisions.append(
                ProviderInvocationApprovalDecisionCandidate(
                    f"provider_invocation_approval_decision_candidate:{candidate.approval_candidate_id.split(':')[1]}:v0.29.6",
                    _ref("provider_invocation_approval_candidate", candidate.approval_candidate_id, V0296_VERSION),
                    proposed,
                    "v0.29.6 records a decision candidate only; approval grant and provider invocation remain disabled.",
                    future,
                )
            )
        return decisions

    def build_decision_records(self, decision_candidates: list[ProviderInvocationApprovalDecisionCandidate]) -> list[ProviderInvocationApprovalDecisionRecord]:
        return [
            ProviderInvocationApprovalDecisionRecord(
                f"provider_invocation_approval_decision_record:{decision.decision_candidate_id.split(':')[1]}:v0.29.6",
                _ref("provider_invocation_approval_decision_candidate", decision.decision_candidate_id, V0296_VERSION),
                decision.proposed_decision,
                decision.decision_reason,
            )
            for decision in decision_candidates
        ]

    def build_scope_summaries(
        self,
        approval_candidates: list[ProviderInvocationApprovalCandidate],
        invocation_report: AdapterInvocationCandidateReport,
        credential_report: CredentialNetworkBoundaryReport,
    ) -> list[ProviderInvocationApprovalScopeSummary]:
        summaries: list[ProviderInvocationApprovalScopeSummary] = []
        for index, approval_candidate in enumerate(approval_candidates):
            invocation_candidate = invocation_report.invocation_candidates[index]
            credential = _safe_get(credential_report.credential_access_candidates, index)
            network = _safe_get(credential_report.network_request_candidates, index)
            summaries.append(
                ProviderInvocationApprovalScopeSummary(
                    f"provider_invocation_approval_scope_summary:{invocation_candidate.adapter_name}:v0.29.6",
                    _ref("provider_invocation_approval_candidate", approval_candidate.approval_candidate_id, V0296_VERSION),
                    invocation_candidate.adapter_name,
                    invocation_candidate.capability_name,
                    "Minimal, expiring approval scope summary for future certification and limited preview evaluation.",
                    invocation_candidate.capability_name,
                    _ref("credential_access_candidate", credential.candidate_id, "v0.29.4") if credential else None,
                    _ref("network_request_candidate", network.candidate_id, "v0.29.4") if network else None,
                    "Payload scope is metadata/mock preview only.",
                    "Result scope forbids raw provider output persistence.",
                    True,
                    True,
                    "ready",
                )
            )
        return summaries

    def build_expiry_policy(self) -> ProviderInvocationApprovalExpiryPolicy:
        return ProviderInvocationApprovalExpiryPolicy("provider_invocation_approval_expiry_policy:v0.29.6")

    def build_revalidation_policy(self) -> ProviderInvocationApprovalRevalidationPolicy:
        return ProviderInvocationApprovalRevalidationPolicy("provider_invocation_approval_revalidation_policy:v0.29.6")


class ProviderInvocationAuditService:
    def build_policy(self) -> ProviderInvocationAuditPolicy:
        return ProviderInvocationAuditPolicy("provider_invocation_audit_policy:v0.29.6")

    def build_event_plans(self, invocation_report: AdapterInvocationCandidateReport) -> list[ProviderInvocationAuditEventPlan]:
        return [
            ProviderInvocationAuditEventPlan(
                f"provider_invocation_audit_event_plan:{candidate.adapter_name}:v0.29.6",
                _ref("adapter_invocation_candidate", candidate.candidate_id, "v0.29.5"),
                AUDIT_EVENT_NAMES,
                "ready",
            )
            for candidate in invocation_report.invocation_candidates
        ]

    def build_audit_trail(
        self,
        request: ProviderInvocationApprovalAuditRollbackRequest,
        source_view: ProviderInvocationApprovalAuditRollbackSourceView,
        approval_candidates: list[ProviderInvocationApprovalCandidate],
        decision_records: list[ProviderInvocationApprovalDecisionRecord],
        audit_event_plans: list[ProviderInvocationAuditEventPlan],
        rollback_plans: list[ProviderRollbackPlan],
        noop_boundaries: list[ProviderNoOpBoundary],
    ) -> ProviderInvocationAuditTrail:
        return ProviderInvocationAuditTrail(
            "provider_invocation_audit_trail:v0.29.6",
            _ref("provider_invocation_approval_audit_rollback_request", request.request_id, V0296_VERSION),
            _ref("provider_invocation_approval_audit_rollback_source_view", source_view.source_view_id, V0296_VERSION),
            _refs("provider_invocation_approval_candidate", approval_candidates, "approval_candidate_id", V0296_VERSION),
            _refs("provider_invocation_approval_decision_record", decision_records, "decision_record_id", V0296_VERSION),
            _refs("provider_invocation_audit_event_plan", audit_event_plans, "audit_event_plan_id", V0296_VERSION),
            _refs("provider_rollback_plan", rollback_plans, "rollback_plan_id", V0296_VERSION),
            _refs("provider_noop_boundary", noop_boundaries, "noop_boundary_id", V0296_VERSION),
            5 + len(approval_candidates) + len(decision_records) + len(audit_event_plans),
        )


class ProviderInvocationOCELTraceService:
    def build_policy(self) -> ProviderInvocationOCELTracePolicy:
        return ProviderInvocationOCELTracePolicy("provider_invocation_ocel_trace_policy:v0.29.6")

    def build_trace_plans(self, invocation_report: AdapterInvocationCandidateReport) -> list[ProviderInvocationOCELTracePlan]:
        return [
            ProviderInvocationOCELTracePlan(
                f"provider_invocation_ocel_trace_plan:{candidate.adapter_name}:v0.29.6",
                _ref("adapter_invocation_candidate", candidate.candidate_id, "v0.29.5"),
                TRACE_EVENT_TYPES,
                TRACE_OBJECT_TYPES,
            )
            for candidate in invocation_report.invocation_candidates
        ]


class ProviderResultBoundaryService:
    def build_result_boundary_policy(self) -> ProviderResultBoundaryPolicy:
        return ProviderResultBoundaryPolicy("provider_result_boundary_policy:v0.29.6")

    def build_result_persistence_policy(self) -> ProviderResultPersistencePolicy:
        return ProviderResultPersistencePolicy("provider_result_persistence_policy:v0.29.6")


class ProviderFailureHandlingService:
    def build_failure_classifications(self, invocation_report: AdapterInvocationCandidateReport) -> list[ProviderFailureClassification]:
        classifications: list[ProviderFailureClassification] = []
        for candidate in invocation_report.invocation_candidates:
            severity = "high" if candidate.candidate_status in {"approval_required_later", "deferred"} else "low"
            classifications.append(
                ProviderFailureClassification(
                    f"provider_failure_classification:{candidate.adapter_name}:v0.29.6",
                    _ref("adapter_invocation_candidate", candidate.candidate_id, "v0.29.5"),
                    FAILURE_MODES,
                    severity,
                    True,
                    True,
                    "warning" if severity == "high" else "ready",
                )
            )
        return classifications

    def build_failure_handling_policy(self) -> ProviderFailureHandlingPolicy:
        return ProviderFailureHandlingPolicy("provider_failure_handling_policy:v0.29.6")


class ProviderRollbackService:
    def build_rollback_boundary_policy(self) -> ProviderRollbackBoundaryPolicy:
        return ProviderRollbackBoundaryPolicy("provider_rollback_boundary_policy:v0.29.6")

    def build_rollback_plans(
        self,
        invocation_report: AdapterInvocationCandidateReport,
    ) -> list[ProviderRollbackPlan]:
        plans: list[ProviderRollbackPlan] = []
        for index, candidate in enumerate(invocation_report.invocation_candidates):
            effect = _safe_get(invocation_report.effect_previews, index)
            side_effect_possible = bool(effect and effect.external_side_effect_possible)
            strategy = "manual_review_required" if side_effect_possible else "no_op_only"
            plans.append(
                ProviderRollbackPlan(
                    f"provider_rollback_plan:{candidate.adapter_name}:v0.29.6",
                    _ref("adapter_invocation_candidate", candidate.candidate_id, "v0.29.5"),
                    _ref("adapter_invocation_effect_preview", effect.effect_preview_id, "v0.29.5") if effect else None,
                    not side_effect_possible,
                    strategy,
                    "Rollback is a future reviewed boundary plan only; no rollback is executed now.",
                )
            )
        return plans

    def build_noop_boundaries(self, invocation_report: AdapterInvocationCandidateReport) -> list[ProviderNoOpBoundary]:
        return [
            ProviderNoOpBoundary(
                f"provider_noop_boundary:{candidate.adapter_name}:v0.29.6",
                _ref("adapter_invocation_candidate", candidate.candidate_id, "v0.29.5"),
                "No-op remains valid when approval, certification, preview, rollback, or result boundaries are incomplete.",
            )
            for candidate in invocation_report.invocation_candidates
        ]

    def build_retry_deferral_policy(self) -> ProviderRetryDeferralPolicy:
        return ProviderRetryDeferralPolicy("provider_retry_deferral_policy:v0.29.6")


class ProviderInvocationApprovalAuditRollbackGateService:
    def evaluate_gate(
        self,
        source_view: ProviderInvocationApprovalAuditRollbackSourceView,
        requirements: list[ProviderInvocationApprovalRequirement],
        approval_candidates: list[ProviderInvocationApprovalCandidate],
        decision_records: list[ProviderInvocationApprovalDecisionRecord],
        scope_summaries: list[ProviderInvocationApprovalScopeSummary],
        audit_policy: ProviderInvocationAuditPolicy,
        audit_event_plans: list[ProviderInvocationAuditEventPlan],
        ocel_trace_plans: list[ProviderInvocationOCELTracePlan],
        result_boundary_policy: ProviderResultBoundaryPolicy,
        result_persistence_policy: ProviderResultPersistencePolicy,
        failure_classifications: list[ProviderFailureClassification],
        failure_policy: ProviderFailureHandlingPolicy,
        rollback_policy: ProviderRollbackBoundaryPolicy,
        rollback_plans: list[ProviderRollbackPlan],
        noop_boundaries: list[ProviderNoOpBoundary],
        retry_policy: ProviderRetryDeferralPolicy,
    ) -> ProviderInvocationApprovalAuditRollbackGate:
        complete = all(
            [
                requirements,
                approval_candidates,
                decision_records,
                scope_summaries,
                audit_event_plans,
                ocel_trace_plans,
                failure_classifications,
                rollback_plans,
                noop_boundaries,
            ]
        )
        no_approval = all(not record.approval_granted_now for record in decision_records)
        no_provider = all(not record.provider_invoked_now for record in decision_records)
        no_network = all(not record.network_called_now for record in decision_records)
        no_credential = all(not record.credential_accessed_now for record in decision_records)
        no_command = all(not record.command_executed_now for record in decision_records)
        no_rollback = all(not record.rollback_executed_now for record in decision_records) and all(not plan.rollback_executed_now for plan in rollback_plans)
        ready = complete and no_approval and no_provider and no_network and no_credential and no_command and no_rollback
        return ProviderInvocationApprovalAuditRollbackGate(
            "provider_invocation_approval_audit_rollback_gate:v0.29.6",
            _ref("provider_invocation_approval_audit_rollback_source_view", source_view.source_view_id, V0296_VERSION),
            _refs("provider_invocation_approval_requirement", requirements, "requirement_id", V0296_VERSION),
            _refs("provider_invocation_approval_candidate", approval_candidates, "approval_candidate_id", V0296_VERSION),
            _refs("provider_invocation_approval_decision_record", decision_records, "decision_record_id", V0296_VERSION),
            _refs("provider_invocation_approval_scope_summary", scope_summaries, "scope_summary_id", V0296_VERSION),
            _ref("provider_invocation_audit_policy", audit_policy.policy_id, V0296_VERSION),
            _refs("provider_invocation_audit_event_plan", audit_event_plans, "audit_event_plan_id", V0296_VERSION),
            _refs("provider_invocation_ocel_trace_plan", ocel_trace_plans, "trace_plan_id", V0296_VERSION),
            _ref("provider_result_boundary_policy", result_boundary_policy.policy_id, V0296_VERSION),
            _ref("provider_result_persistence_policy", result_persistence_policy.policy_id, V0296_VERSION),
            _refs("provider_failure_classification", failure_classifications, "classification_id", V0296_VERSION),
            _ref("provider_failure_handling_policy", failure_policy.policy_id, V0296_VERSION),
            _ref("provider_rollback_boundary_policy", rollback_policy.policy_id, V0296_VERSION),
            _refs("provider_rollback_plan", rollback_plans, "rollback_plan_id", V0296_VERSION),
            _refs("provider_noop_boundary", noop_boundaries, "noop_boundary_id", V0296_VERSION),
            _ref("provider_retry_deferral_policy", retry_policy.policy_id, V0296_VERSION),
            bool(requirements),
            bool(approval_candidates),
            bool(decision_records),
            bool(scope_summaries),
            audit_policy.audit_required and bool(audit_event_plans),
            bool(ocel_trace_plans),
            result_boundary_policy.provider_result_boundary_required and result_persistence_policy.raw_result_persistence_forbidden,
            bool(failure_classifications),
            bool(rollback_plans) and all(noop.noop_available for noop in noop_boundaries),
            retry_policy.retry_policy_deferred,
            no_approval,
            no_provider,
            no_network,
            no_credential,
            no_command,
            True,
            no_rollback,
            "warning",
            ready,
            ready,
        )


class ProviderInvocationApprovalAuditRollbackFindingService:
    BLOCKED_FINDINGS = {
        "approval_grant_attempted",
        "provider_registration_attempted",
        "provider_invocation_attempted",
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

    def build_findings(self) -> list[ProviderInvocationApprovalAuditRollbackFinding]:
        return [
            ProviderInvocationApprovalAuditRollbackFinding(
                "provider_invocation_approval_audit_rollback_finding:policy:v0.29.6",
                "info",
                "approval_audit_rollback_policy_created",
                "Approval/audit/rollback boundary policy created without approval grant or provider execution.",
                _ref("provider_invocation_approval_audit_rollback_policy", "provider_invocation_approval_audit_rollback_policy:v0.29.6", V0296_VERSION),
                [],
                None,
            ),
            ProviderInvocationApprovalAuditRollbackFinding(
                "provider_invocation_approval_audit_rollback_finding:approval:v0.29.6",
                "info",
                "approval_decision_record_created",
                "Approval decision records are recorded as future-boundary inputs; approval_granted_now remains false.",
                _ref("provider_invocation_approval_decision_record", "provider_invocation_approval_decision_record:internal_mock_adapter:v0.29.6", V0296_VERSION),
                [],
                "Withdraw if approval is granted or treated as provider invocation.",
            ),
            ProviderInvocationApprovalAuditRollbackFinding(
                "provider_invocation_approval_audit_rollback_finding:gate:v0.29.6",
                "warning",
                "approval_audit_rollback_gate_created",
                "Gate readiness targets v0.29.7 certification only; limited preview and live provider readiness remain false.",
                _ref("provider_invocation_approval_audit_rollback_gate", "provider_invocation_approval_audit_rollback_gate:v0.29.6", V0296_VERSION),
                [],
                "Withdraw if provider, network, credential, command, rollback, retry, or limited preview readiness becomes true.",
            ),
        ]


class ProviderInvocationApprovalAuditRollbackReportService:
    def build_report(self, report_id: str | None = None) -> ProviderInvocationApprovalAuditRollbackReport:
        source_service = ProviderInvocationApprovalAuditRollbackPrerequisiteSourceService()
        invocation_report = source_service.load_v0295_invocation_candidate_report()
        credential_report = source_service.load_v0294_credential_network_boundary_report()
        permission_report = source_service.load_v0293_permission_safety_report()
        policy = ProviderInvocationApprovalAuditRollbackPolicyService().build_policy()
        source_view = ProviderInvocationApprovalAuditRollbackSourceViewService().build_source_view()
        request = ProviderInvocationApprovalAuditRollbackRequestService().build_request(source_view)
        approval_service = ProviderInvocationApprovalService()
        requirements = approval_service.build_requirements(invocation_report)
        approval_candidates = approval_service.build_candidates(requirements, invocation_report, permission_report)
        decision_candidates = approval_service.build_decision_candidates(approval_candidates)
        decision_records = approval_service.build_decision_records(decision_candidates)
        scope_summaries = approval_service.build_scope_summaries(approval_candidates, invocation_report, credential_report)
        expiry_policy = approval_service.build_expiry_policy()
        revalidation_policy = approval_service.build_revalidation_policy()
        audit_service = ProviderInvocationAuditService()
        audit_policy = audit_service.build_policy()
        audit_event_plans = audit_service.build_event_plans(invocation_report)
        ocel_service = ProviderInvocationOCELTraceService()
        ocel_policy = ocel_service.build_policy()
        ocel_plans = ocel_service.build_trace_plans(invocation_report)
        result_service = ProviderResultBoundaryService()
        result_policy = result_service.build_result_boundary_policy()
        result_persistence = result_service.build_result_persistence_policy()
        failure_service = ProviderFailureHandlingService()
        failure_classifications = failure_service.build_failure_classifications(invocation_report)
        failure_policy = failure_service.build_failure_handling_policy()
        rollback_service = ProviderRollbackService()
        rollback_policy = rollback_service.build_rollback_boundary_policy()
        rollback_plans = rollback_service.build_rollback_plans(invocation_report)
        noop_boundaries = rollback_service.build_noop_boundaries(invocation_report)
        retry_policy = rollback_service.build_retry_deferral_policy()
        gate = ProviderInvocationApprovalAuditRollbackGateService().evaluate_gate(
            source_view,
            requirements,
            approval_candidates,
            decision_records,
            scope_summaries,
            audit_policy,
            audit_event_plans,
            ocel_plans,
            result_policy,
            result_persistence,
            failure_classifications,
            failure_policy,
            rollback_policy,
            rollback_plans,
            noop_boundaries,
            retry_policy,
        )
        audit_trail = audit_service.build_audit_trail(
            request,
            source_view,
            approval_candidates,
            decision_records,
            audit_event_plans,
            rollback_plans,
            noop_boundaries,
        )
        findings = ProviderInvocationApprovalAuditRollbackFindingService().build_findings()
        return ProviderInvocationApprovalAuditRollbackReport(
            report_id or "provider_invocation_approval_audit_rollback_report:v0.29.6",
            _now(),
            policy,
            request,
            source_view,
            requirements,
            approval_candidates,
            decision_candidates,
            decision_records,
            scope_summaries,
            expiry_policy,
            revalidation_policy,
            audit_policy,
            audit_event_plans,
            audit_trail,
            ocel_policy,
            ocel_plans,
            result_policy,
            result_persistence,
            failure_classifications,
            failure_policy,
            rollback_policy,
            rollback_plans,
            noop_boundaries,
            retry_policy,
            gate,
            findings,
            "warning",
            gate.ready_for_v0_29_7,
            gate.ready_for_certification_matrix,
            limitations=["v0.29.6 creates approval/audit/rollback boundary artifacts only. Certification, limited preview, and provider invocation remain future work."],
            withdrawal_conditions=["Withdraw if approval grants, provider/network/credential/secret/command/side-effect/file/rollback/retry/live adapter/private/raw output behavior, or LLM-judge-only authority appears."],
        )

    def build_all_parts(self, report_id: str | None = None) -> dict[str, Any]:
        report = self.build_report(report_id=report_id)
        return {
            "policy": report.policy,
            "request": report.request,
            "source-view": report.source_view,
            "requirements": report.approval_requirements,
            "candidates": report.approval_candidates,
            "decisions": report.approval_decision_records,
            "decision-candidates": report.approval_decision_candidates,
            "scope-summary": report.approval_scope_summaries,
            "expiry": report.approval_expiry_policy,
            "revalidation": report.approval_revalidation_policy,
            "audit-policy": report.audit_policy,
            "audit-plan": report.audit_event_plans,
            "audit-trail": report.audit_trail,
            "ocel-policy": report.ocel_trace_policy,
            "ocel-plan": report.ocel_trace_plans,
            "result-boundary": report.result_boundary_policy,
            "result-persistence": report.result_persistence_policy,
            "failure": report.failure_classifications,
            "failure-policy": report.failure_handling_policy,
            "rollback": report.rollback_plans,
            "rollback-policy": report.rollback_boundary_policy,
            "noop": report.noop_boundaries,
            "retry-deferral": report.retry_deferral_policy,
            "gate": report.approval_audit_rollback_gate,
            "findings": report.findings,
            "report": report,
        }

    def build_pig_report(self) -> dict[str, Any]:
        report = self.build_report()
        return {
            "version": V0296_VERSION,
            "layer": V0296_LAYER,
            "subject": "provider_invocation_approval_audit_rollback_boundary",
            "principles": [
                "Approval requirement is not approval",
                "Approval candidate is not approval grant",
                "Approval record is not provider invocation",
                "Audit policy is not audit completion",
                "Audit trail is not raw provider output persistence",
                "Rollback plan is not rollback execution",
                "No-op boundary is a valid safety outcome",
                "Failure classification is not automatic retry",
                "Provider result boundary is not provider response persistence",
                "No-provider-invocation remains the default",
            ],
            "safety_boundary": {
                "approval_granted": report.approval_granted,
                "provider_registered": report.provider_registered,
                "provider_invoked": report.provider_invoked,
                "provider_sdk_invoked": report.provider_sdk_invoked,
                "network_called": report.network_called,
                "outbound_request_sent": report.outbound_request_sent,
                "credential_accessed": report.credential_accessed,
                "credential_stored": report.credential_stored,
                "credential_logged": report.credential_logged,
                "secret_retrieved": report.secret_retrieved,
                "secret_materialized": report.secret_materialized,
                "command_executed": report.command_executed,
                "external_side_effect_performed": report.external_side_effect_performed,
                "file_mutated": report.file_mutated,
                "rollback_executed": report.rollback_executed,
                "automatic_retry_performed": report.automatic_retry_performed,
                "live_adapter_implemented": report.live_adapter_implemented,
                "RPA_adapter_implemented": report.RPA_adapter_implemented,
                "A360_adapter_implemented": report.A360_adapter_implemented,
                "Brity_adapter_implemented": report.Brity_adapter_implemented,
                "UiPath_adapter_implemented": report.UiPath_adapter_implemented,
                "external_dominion_implemented": report.external_dominion_implemented,
                "schumpeter_private_runtime_used": report.schumpeter_private_runtime_used,
                "actual_user_data_used": report.actual_user_data_used,
                "actual_company_data_used": report.actual_company_data_used,
                "private_material_exposed": report.private_material_exposed,
                "raw_provider_output_persisted": report.raw_provider_output_persisted,
                "raw_payload_logged": report.raw_payload_logged,
                "references_runtime_dependency_added": report.references_runtime_dependency_added,
                "references_code_copied": report.references_code_copied,
                "PIG_execution_authority_enabled": report.PIG_execution_authority_enabled,
                "llm_judge_enabled": False,
            },
            "future_direction": [
                "v0.29.7 External Skill Packaging / Certification Matrix",
                "v0.29.8 Limited Provider Invocation Preview Gate",
                "v0.29.9 External Provider Adapter Foundation Consolidation",
            ],
            "next_step": V0296_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "provider_invocation_approval_audit_rollback_boundary_created",
            "version": V0296_VERSION,
            "source_read_models": [
                "AdapterInvocationCandidateState",
                "AdapterDryRunPlanState",
                "AdapterDryRunReportState",
                "AdapterEffectPreviewState",
                "AdapterRiskPreviewState",
                "AdapterNoOpPlanState",
                "AdapterFailureModePreviewState",
                "CredentialNetworkBoundaryGateState",
                "CredentialAccessCandidateState",
                "NetworkRequestCandidateState",
                "AdapterPermissionSafetyGateState",
                "AdapterPermissionDecisionRecordState",
                "MockAdapterHarnessState",
                "AdapterRegistryState",
                "AdapterAuditRequirementContractState",
                "AdapterRollbackNoOpRequirementContractState",
                "AdapterOCELVisibilityContractState",
                "ProviderInvocationProhibitionState",
                "CommandExecutionProhibitionState",
                "PigGuidanceState",
                "OCPXProjectionState",
            ],
            "target_read_models": [
                "ProviderInvocationApprovalBoundaryState",
                "ProviderInvocationApprovalCandidateState",
                "ProviderInvocationApprovalDecisionRecordState",
                "ProviderInvocationAuditPlanState",
                "ProviderInvocationAuditTrailState",
                "ProviderInvocationOCELTracePlanState",
                "ProviderResultBoundaryState",
                "ProviderFailureClassificationState",
                "ProviderRollbackPlanState",
                "ProviderNoOpBoundaryState",
                "ProviderInvocationApprovalAuditRollbackGateState",
                "V029ReadinessState",
            ],
            "effect_types": V0296_EFFECT_TYPES,
            "forbidden_effect_types": V0296_FORBIDDEN_EFFECT_TYPES,
        }


def render_provider_invocation_approval_cli(parts: dict[str, Any], section: str = "report") -> str:
    report: ProviderInvocationApprovalAuditRollbackReport = parts["report"]
    lines = [
        f"Provider Invocation Approval / Audit / Rollback Boundary {section}",
        f"version={report.version}",
        f"layer={report.policy.layer}",
        f"report_status={report.report_status}",
        f"ready_for_v0_29_7={_bool(report.ready_for_v0_29_7)}",
        f"ready_for_certification_matrix={_bool(report.ready_for_certification_matrix)}",
        f"ready_for_limited_invocation_preview={_bool(report.ready_for_limited_invocation_preview)}",
        f"ready_for_provider_invocation={_bool(report.ready_for_provider_invocation)}",
        f"ready_for_network_access={_bool(report.ready_for_network_access)}",
        f"ready_for_credential_access={_bool(report.ready_for_credential_access)}",
        f"ready_for_command_execution={_bool(report.ready_for_command_execution)}",
        f"approval_granted={_bool(report.approval_granted)}",
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
    payload = parts.get(section)
    if payload is not None and payload is not report:
        if isinstance(payload, list):
            lines.append(f"section_count={len(payload)}")
        else:
            lines.append(f"section_object={payload.__class__.__name__}")
    return "\n".join(lines)
