from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.credential_secret_network_boundary import (
    CredentialNetworkBoundaryReport,
    CredentialNetworkBoundaryReportService,
)
from chanta_core.external_provider_adapter_contract import ModelMixin, _bool, _ref
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
from chanta_core.utility.time import utc_now_iso


V0295_VERSION = "v0.29.5"
V0295_LAYER = "external_provider_adapter"
V0295_TRACK = "External Skill / External Provider Adapter Development"
V0295_NAME = "Adapter Invocation Candidate / Dry-Run Plan"
V0295_NEXT_STEP = "v0.29.6 Provider Invocation Approval / Audit / Rollback Boundary"

V0295_OBJECT_TYPES = [
    "adapter_invocation_candidate_policy",
    "adapter_invocation_candidate_request",
    "adapter_invocation_candidate_source_view",
    "adapter_invocation_intent",
    "adapter_invocation_candidate",
    "adapter_invocation_input_envelope",
    "adapter_invocation_payload_preview",
    "adapter_invocation_output_schema_preview",
    "adapter_invocation_credential_reference_check",
    "adapter_invocation_network_boundary_check",
    "adapter_invocation_permission_safety_check",
    "adapter_invocation_effect_preview",
    "adapter_invocation_risk_preview",
    "adapter_invocation_dry_run_plan",
    "adapter_invocation_dry_run_step",
    "adapter_invocation_dry_run_report",
    "adapter_invocation_dry_run_result",
    "adapter_invocation_noop_plan",
    "adapter_invocation_failure_mode_preview",
    "adapter_invocation_readiness_gate",
    "adapter_invocation_candidate_audit_trail",
    "adapter_invocation_candidate_finding",
    "adapter_invocation_candidate_report",
    "credential_network_boundary_report",
    "adapter_permission_safety_report",
    "mock_adapter_harness_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

V0295_EVENT_TYPES = [
    "adapter_invocation_candidate_requested",
    "adapter_invocation_candidate_prerequisites_loaded",
    "adapter_invocation_candidate_policy_created",
    "adapter_invocation_intent_created",
    "adapter_invocation_candidate_created",
    "adapter_invocation_input_envelope_created",
    "adapter_invocation_payload_preview_created",
    "adapter_invocation_output_schema_preview_created",
    "adapter_invocation_credential_reference_check_created",
    "adapter_invocation_network_boundary_check_created",
    "adapter_invocation_permission_safety_check_created",
    "adapter_invocation_effect_preview_created",
    "adapter_invocation_risk_preview_created",
    "adapter_invocation_dry_run_plan_created",
    "adapter_invocation_dry_run_step_created",
    "adapter_invocation_dry_run_report_created",
    "adapter_invocation_dry_run_result_created",
    "adapter_invocation_noop_plan_created",
    "adapter_invocation_failure_mode_preview_created",
    "adapter_invocation_readiness_gate_evaluated",
    "adapter_invocation_candidate_audit_trail_created",
    "adapter_invocation_candidate_report_created",
    "adapter_invocation_candidate_warning_created",
    "adapter_invocation_candidate_blocked",
]

V0295_EFFECT_TYPES = [
    "read_only_observation",
    "adapter_invocation_candidate_created",
    "adapter_payload_preview_created",
    "adapter_output_schema_preview_created",
    "adapter_effect_preview_created",
    "adapter_risk_preview_created",
    "adapter_dry_run_plan_created",
    "adapter_dry_run_report_created",
    "adapter_noop_plan_created",
    "adapter_invocation_readiness_gate_evaluated",
    "adapter_invocation_candidate_audit_trail_created",
    "state_candidate_created",
]

V0295_FORBIDDEN_EFFECT_TYPES = [
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

RISK_DIMENSIONS = [
    "credential_exposure",
    "network_access",
    "private_data_exposure",
    "provider_side_effect",
    "command_execution",
    "data_exfiltration",
    "raw_provider_output_persistence",
    "audit_gap",
    "rollback_gap",
    "OCEL_visibility_gap",
    "RPA_scope_creep",
    "external_dominion_creep",
]

DRY_RUN_STEP_NAMES = [
    "validate_input_envelope",
    "build_payload_preview",
    "check_credential_reference",
    "check_network_boundary",
    "check_permission_safety",
    "preview_effects",
    "preview_risks",
    "validate_output_schema",
    "produce_noop_plan",
    "record_ocel_trace_candidate",
]

FALLBACK_DECISIONS = [
    "deny",
    "defer",
    "mock_only",
    "dry_run_only",
    "require_v0296_approval",
    "require_v0298_preview_gate",
]

FAILURE_MODES = [
    "missing_permission",
    "missing_credential_boundary",
    "missing_network_boundary",
    "missing_approval",
    "schema_mismatch",
    "provider_error",
    "timeout",
    "auth_failure",
    "rate_limit",
    "unsafe_payload",
    "unknown",
]

INVOCATION_BLUEPRINTS = {
    "internal_mock_adapter": {
        "provider_kind": "internal_mock_provider",
        "action_kind": "mock_only",
        "candidate_status": "dry_run_ready",
        "run_mode": "mock_only",
        "risk_level": "none",
        "requires_provider": False,
        "requires_sdk": False,
        "requires_network": False,
        "requires_credentials": False,
        "requires_secret_reference": False,
        "requires_command": False,
        "requires_private_data": False,
        "requires_side_effect": False,
    },
    "generic_llm_adapter": {
        "provider_kind": "llm_provider",
        "action_kind": "external_read_candidate",
        "candidate_status": "approval_required_later",
        "run_mode": "metadata_only",
        "risk_level": "high",
        "requires_provider": True,
        "requires_sdk": True,
        "requires_network": True,
        "requires_credentials": True,
        "requires_secret_reference": True,
        "requires_command": False,
        "requires_private_data": False,
        "requires_side_effect": False,
    },
    "generic_search_adapter": {
        "provider_kind": "search_provider",
        "action_kind": "external_read_candidate",
        "candidate_status": "approval_required_later",
        "run_mode": "metadata_only",
        "risk_level": "medium",
        "requires_provider": True,
        "requires_sdk": True,
        "requires_network": True,
        "requires_credentials": False,
        "requires_secret_reference": False,
        "requires_command": False,
        "requires_private_data": False,
        "requires_side_effect": False,
    },
    "generic_workflow_adapter": {
        "provider_kind": "workflow_provider",
        "action_kind": "external_side_effect_candidate",
        "candidate_status": "approval_required_later",
        "run_mode": "metadata_only",
        "risk_level": "high",
        "requires_provider": True,
        "requires_sdk": True,
        "requires_network": True,
        "requires_credentials": True,
        "requires_secret_reference": True,
        "requires_command": False,
        "requires_private_data": False,
        "requires_side_effect": True,
    },
    "generic_rpa_adapter": {
        "provider_kind": "rpa_provider",
        "action_kind": "rpa_deferred",
        "candidate_status": "deferred",
        "run_mode": "not_run",
        "risk_level": "blocked",
        "requires_provider": True,
        "requires_sdk": False,
        "requires_network": True,
        "requires_credentials": True,
        "requires_secret_reference": True,
        "requires_command": True,
        "requires_private_data": False,
        "requires_side_effect": True,
    },
}


def _now() -> str:
    return utc_now_iso()


def _refs(object_type: str, items: list[Any], attr: str, version: str) -> list[dict[str, Any]]:
    return [_ref(object_type, getattr(item, attr), version) for item in items]


def _safe_get(items: list[Any], index: int) -> Any | None:
    if not items:
        return None
    return items[min(index, len(items) - 1)]


def _adapter_names(permission_report: AdapterPermissionSafetyReport) -> list[str]:
    names = [intent.adapter_name for intent in permission_report.action_intents]
    return names or list(INVOCATION_BLUEPRINTS)


def _spec(adapter_name: str) -> dict[str, Any]:
    return INVOCATION_BLUEPRINTS.get(
        adapter_name,
        {
            "provider_kind": "unknown",
            "action_kind": "unknown",
            "candidate_status": "unknown",
            "run_mode": "metadata_only",
            "risk_level": "unknown",
            "requires_provider": True,
            "requires_sdk": True,
            "requires_network": True,
            "requires_credentials": True,
            "requires_secret_reference": True,
            "requires_command": False,
            "requires_private_data": False,
            "requires_side_effect": False,
        },
    )


@dataclass
class AdapterInvocationCandidatePolicy(ModelMixin):
    policy_id: str
    invocation_candidate_enabled: bool = True
    dry_run_plan_enabled: bool = True
    dry_run_report_enabled: bool = True
    payload_preview_required: bool = True
    output_schema_preview_required: bool = True
    effect_preview_required: bool = True
    risk_preview_required: bool = True
    no_op_plan_required: bool = True
    credential_reference_check_required: bool = True
    network_boundary_check_required: bool = True
    permission_safety_check_required: bool = True
    provider_invocation_enabled_now: bool = False
    provider_sdk_invocation_enabled_now: bool = False
    network_access_enabled_now: bool = False
    credential_access_enabled_now: bool = False
    secret_retrieval_enabled_now: bool = False
    command_execution_expansion_enabled_now: bool = False
    live_adapter_implementation_enabled_now: bool = False
    rpa_adapter_enabled_now: bool = False
    external_agent_dominion_enabled_now: bool = False
    dry_run_is_not_provider_call: bool = True
    invocation_candidate_is_not_invocation: bool = True
    payload_preview_is_not_payload_send: bool = True
    effect_preview_is_not_side_effect: bool = True
    risk_preview_is_not_approval: bool = True
    no_provider_invocation_default: bool = True
    no_network_default: bool = True
    no_credential_value_default: bool = True
    llm_judge_as_sole_invocation_candidate_authority_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0295_VERSION
    layer: str = V0295_LAYER


@dataclass
class AdapterInvocationCandidateRequest(ModelMixin):
    request_id: str
    credential_network_boundary_report_id: str | None
    permission_safety_report_id: str | None
    mock_harness_report_id: str | None
    adapter_registry_report_id: str | None
    requested_candidate_scope: str = "full_invocation_candidate_pack"
    strictness: str = "standard"
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0295_VERSION


@dataclass
class AdapterInvocationCandidateSourceView(ModelMixin):
    source_view_id: str
    credential_network_boundary_report_ref: dict[str, Any] | None
    credential_network_gate_ref: dict[str, Any] | None
    credential_access_candidate_refs: list[dict[str, Any]]
    network_request_candidate_refs: list[dict[str, Any]]
    payload_boundary_policy_ref: dict[str, Any] | None
    request_response_redaction_boundary_ref: dict[str, Any] | None
    data_exfiltration_boundary_policy_ref: dict[str, Any] | None
    provider_sdk_boundary_report_refs: list[dict[str, Any]]
    permission_safety_report_ref: dict[str, Any] | None
    permission_decision_record_refs: list[dict[str, Any]]
    safety_classification_refs: list[dict[str, Any]]
    action_intent_refs: list[dict[str, Any]]
    action_scope_refs: list[dict[str, Any]]
    mock_harness_report_ref: dict[str, Any] | None
    mock_run_report_refs: list[dict[str, Any]]
    adapter_registry_report_ref: dict[str, Any] | None
    adapter_capability_declaration_refs: list[dict[str, Any]]
    effect_boundary_contract_ref: dict[str, Any] | None
    input_schema_contract_ref: dict[str, Any] | None
    output_schema_contract_ref: dict[str, Any] | None
    provider_invocation_prohibition_ref: dict[str, Any] | None
    command_execution_prohibition_ref: dict[str, Any] | None
    source_status: str
    credential_network_ready_for_candidate: bool | None
    permission_safety_ready_for_candidate: bool | None
    mock_ready_for_candidate: bool | None
    provider_invocation_detected: bool = False
    provider_sdk_invocation_detected: bool = False
    network_call_detected: bool = False
    credential_access_detected: bool = False
    secret_retrieval_detected: bool = False
    command_execution_detected: bool = False
    live_adapter_detected: bool = False
    private_data_detected: bool = False
    raw_provider_output_detected: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0295_VERSION


@dataclass
class AdapterInvocationIntent(ModelMixin):
    intent_id: str
    adapter_name: str
    provider_kind: str
    capability_name: str
    action_kind: str
    intent_summary: str
    intended_provider_action: str | None
    requires_provider_invocation: bool
    requires_provider_sdk: bool
    requires_network: bool
    requires_credentials: bool
    requires_secret_reference: bool
    requires_command_execution: bool
    requires_private_data: bool
    requires_external_side_effect: bool
    intent_allowed_as_candidate: bool
    intent_allowed_as_live_invocation: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0295_VERSION


@dataclass
class AdapterInvocationCandidate(ModelMixin):
    candidate_id: str
    adapter_name: str
    capability_name: str
    intent_ref: dict[str, Any]
    permission_decision_ref: dict[str, Any] | None
    safety_classification_ref: dict[str, Any] | None
    credential_access_candidate_ref: dict[str, Any] | None
    network_request_candidate_ref: dict[str, Any] | None
    candidate_status: str
    candidate_reason: str
    provider_invocation_candidate_is_invocation: bool = False
    provider_invoked_now: bool = False
    provider_sdk_invoked_now: bool = False
    network_called_now: bool = False
    credential_accessed_now: bool = False
    command_executed_now: bool = False
    required_next_gate: str = V0295_NEXT_STEP
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0295_VERSION


@dataclass
class AdapterInvocationInputEnvelope(ModelMixin):
    envelope_id: str
    candidate_ref: dict[str, Any]
    adapter_name: str
    capability_name: str
    input_schema_ref: dict[str, Any] | None
    input_refs: list[dict[str, Any]]
    synthetic_or_metadata_only: bool = True
    contains_actual_user_data: bool = False
    contains_actual_company_data: bool = False
    contains_private_data: bool = False
    contains_credentials: bool = False
    contains_raw_trace: bool = False
    contains_raw_transcript: bool = False
    contains_raw_provider_output: bool = False
    envelope_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0295_VERSION


@dataclass
class AdapterInvocationPayloadPreview(ModelMixin):
    payload_preview_id: str
    candidate_ref: dict[str, Any]
    input_envelope_ref: dict[str, Any]
    payload_boundary_ref: dict[str, Any] | None
    redaction_boundary_ref: dict[str, Any] | None
    payload_summary: str
    payload_preview_allowed: bool = True
    payload_preview_is_payload_send: bool = False
    outbound_payload_sent_now: bool = False
    contains_credentials: bool = False
    contains_private_data: bool = False
    contains_raw_artifacts: bool = False
    payload_preview_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0295_VERSION


@dataclass
class AdapterInvocationOutputSchemaPreview(ModelMixin):
    output_preview_id: str
    candidate_ref: dict[str, Any]
    output_schema_ref: dict[str, Any] | None
    expected_fields: list[str]
    expected_error_fields: list[str]
    redaction_required: bool = True
    raw_provider_output_persistence_forbidden: bool = True
    output_schema_preview_is_provider_response: bool = False
    provider_response_received_now: bool = False
    preview_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0295_VERSION


@dataclass
class AdapterInvocationCredentialReferenceCheck(ModelMixin):
    check_id: str
    candidate_ref: dict[str, Any]
    credential_access_candidate_ref: dict[str, Any] | None
    secret_reference_ref: dict[str, Any] | None
    credential_reference_present: bool
    credential_value_required: bool
    credential_value_accessed_now: bool = False
    credential_value_stored_now: bool = False
    credential_value_logged_now: bool = False
    secret_retrieved_now: bool = False
    check_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0295_VERSION


@dataclass
class AdapterInvocationNetworkBoundaryCheck(ModelMixin):
    check_id: str
    candidate_ref: dict[str, Any]
    network_request_candidate_ref: dict[str, Any] | None
    outbound_domain_rule_ref: dict[str, Any] | None
    network_boundary_present: bool
    network_required_for_live: bool
    network_called_now: bool = False
    outbound_request_sent_now: bool = False
    provider_sdk_network_called_now: bool = False
    check_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0295_VERSION


@dataclass
class AdapterInvocationPermissionSafetyCheck(ModelMixin):
    check_id: str
    candidate_ref: dict[str, Any]
    permission_decision_ref: dict[str, Any] | None
    safety_classification_ref: dict[str, Any] | None
    approval_required_later: bool
    unsafe_for_candidate: bool
    permission_granted_now: bool = False
    approval_granted_now: bool = False
    check_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0295_VERSION


@dataclass
class AdapterInvocationEffectPreview(ModelMixin):
    effect_preview_id: str
    candidate_ref: dict[str, Any]
    effect_boundary_contract_ref: dict[str, Any] | None
    predicted_effect_types: list[str]
    forbidden_effect_types_detected: list[str]
    external_side_effect_possible: bool
    external_side_effect_performed_now: bool = False
    file_mutated_now: bool = False
    provider_invoked_now: bool = False
    network_called_now: bool = False
    command_executed_now: bool = False
    effect_preview_is_side_effect: bool = False
    preview_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0295_VERSION


@dataclass
class AdapterInvocationRiskPreview(ModelMixin):
    risk_preview_id: str
    candidate_ref: dict[str, Any]
    risk_dimensions: list[str]
    risk_level: str
    blocker_count: int
    warning_count: int
    blocks_dry_run: bool
    requires_v0296_approval_audit_rollback: bool
    risk_preview_is_approval: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0295_VERSION


@dataclass
class AdapterInvocationDryRunStep(ModelMixin):
    step_id: str
    step_order: int
    step_name: str
    step_summary: str
    step_is_live_call: bool = False
    step_invokes_provider: bool = False
    step_calls_network: bool = False
    step_accesses_credentials: bool = False
    step_executes_command: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0295_VERSION


@dataclass
class AdapterInvocationDryRunPlan(ModelMixin):
    plan_id: str
    candidate_ref: dict[str, Any]
    input_envelope_ref: dict[str, Any]
    payload_preview_ref: dict[str, Any]
    output_schema_preview_ref: dict[str, Any]
    credential_check_ref: dict[str, Any]
    network_check_ref: dict[str, Any]
    permission_safety_check_ref: dict[str, Any]
    effect_preview_ref: dict[str, Any]
    risk_preview_ref: dict[str, Any]
    dry_run_steps: list[AdapterInvocationDryRunStep]
    run_mode: str
    dry_run_allowed_now: bool
    live_provider_allowed: bool = False
    network_allowed: bool = False
    credential_access_allowed: bool = False
    command_execution_allowed: bool = False
    external_side_effect_allowed: bool = False
    plan_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0295_VERSION


@dataclass
class AdapterInvocationDryRunResult(ModelMixin):
    result_id: str
    step_ref: dict[str, Any]
    result_status: str
    result_summary: str
    provider_invoked: bool = False
    network_called: bool = False
    credential_accessed: bool = False
    command_executed: bool = False
    side_effect_performed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0295_VERSION


@dataclass
class AdapterInvocationDryRunReport(ModelMixin):
    report_id: str
    plan_ref: dict[str, Any]
    candidate_ref: dict[str, Any]
    dry_run_results: list[AdapterInvocationDryRunResult]
    dry_run_executed: bool
    dry_run_mode: str
    dry_run_status: str
    provider_invoked: bool = False
    provider_sdk_invoked: bool = False
    network_called: bool = False
    credential_accessed: bool = False
    credential_stored: bool = False
    credential_logged: bool = False
    command_executed: bool = False
    external_side_effect_performed: bool = False
    raw_provider_output_persisted: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0295_VERSION


@dataclass
class AdapterInvocationNoOpPlan(ModelMixin):
    noop_plan_id: str
    candidate_ref: dict[str, Any]
    noop_reason: str
    fallback_decisions: list[str]
    noop_available: bool = True
    noop_is_execution: bool = False
    side_effect_performed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0295_VERSION


@dataclass
class AdapterInvocationFailureModePreview(ModelMixin):
    failure_preview_id: str
    candidate_ref: dict[str, Any]
    possible_failure_modes: list[str]
    failure_classification_required_later: bool = True
    rollback_or_noop_required_later: bool = True
    preview_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0295_VERSION


@dataclass
class AdapterInvocationReadinessGate(ModelMixin):
    gate_id: str
    source_view_ref: dict[str, Any]
    candidate_refs: list[dict[str, Any]]
    payload_preview_refs: list[dict[str, Any]]
    output_schema_preview_refs: list[dict[str, Any]]
    credential_check_refs: list[dict[str, Any]]
    network_check_refs: list[dict[str, Any]]
    permission_safety_check_refs: list[dict[str, Any]]
    effect_preview_refs: list[dict[str, Any]]
    risk_preview_refs: list[dict[str, Any]]
    dry_run_plan_refs: list[dict[str, Any]]
    dry_run_report_refs: list[dict[str, Any]]
    noop_plan_refs: list[dict[str, Any]]
    candidate_generation_complete: bool
    payload_previews_complete: bool
    output_schema_previews_complete: bool
    credential_checks_passed_or_deferred: bool
    network_checks_passed_or_deferred: bool
    permission_safety_checks_passed_or_deferred: bool
    effect_previews_complete: bool
    risk_previews_complete: bool
    dry_run_plans_complete: bool
    dry_run_reports_complete_or_safely_deferred: bool
    noop_plans_available: bool
    no_provider_invocation: bool
    no_network_call: bool
    no_credential_access: bool
    no_command_execution: bool
    no_external_side_effect: bool
    gate_status: str
    ready_for_v0_29_6: bool
    ready_for_approval_audit_rollback_boundary: bool
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0295_VERSION


@dataclass
class AdapterInvocationCandidateAuditTrail(ModelMixin):
    audit_trail_id: str
    request_ref: dict[str, Any]
    source_view_ref: dict[str, Any]
    candidate_refs: list[dict[str, Any]]
    dry_run_plan_refs: list[dict[str, Any]]
    dry_run_report_refs: list[dict[str, Any]]
    gate_ref: dict[str, Any]
    audit_event_count: int
    raw_content_included: bool = False
    credential_value_included: bool = False
    raw_payload_included: bool = False
    raw_provider_output_included: bool = False
    audit_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0295_VERSION


@dataclass
class AdapterInvocationCandidateFinding(ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class AdapterInvocationCandidateReport(ModelMixin):
    report_id: str
    created_at: str
    policy: AdapterInvocationCandidatePolicy
    request: AdapterInvocationCandidateRequest
    source_view: AdapterInvocationCandidateSourceView
    invocation_intents: list[AdapterInvocationIntent]
    invocation_candidates: list[AdapterInvocationCandidate]
    input_envelopes: list[AdapterInvocationInputEnvelope]
    payload_previews: list[AdapterInvocationPayloadPreview]
    output_schema_previews: list[AdapterInvocationOutputSchemaPreview]
    credential_reference_checks: list[AdapterInvocationCredentialReferenceCheck]
    network_boundary_checks: list[AdapterInvocationNetworkBoundaryCheck]
    permission_safety_checks: list[AdapterInvocationPermissionSafetyCheck]
    effect_previews: list[AdapterInvocationEffectPreview]
    risk_previews: list[AdapterInvocationRiskPreview]
    dry_run_plans: list[AdapterInvocationDryRunPlan]
    dry_run_reports: list[AdapterInvocationDryRunReport]
    noop_plans: list[AdapterInvocationNoOpPlan]
    failure_mode_previews: list[AdapterInvocationFailureModePreview]
    readiness_gate: AdapterInvocationReadinessGate
    audit_trail: AdapterInvocationCandidateAuditTrail
    findings: list[AdapterInvocationCandidateFinding]
    report_status: str
    ready_for_v0_29_6: bool
    ready_for_approval_audit_rollback_boundary: bool
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
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
    next_required_step: str = V0295_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.29.6 Provider Invocation Approval / Audit / Rollback Boundary begins or Adapter Invocation Candidate policy changes."
    version: str = V0295_VERSION


class AdapterInvocationCandidatePrerequisiteSourceService:
    def load_v0294_credential_network_boundary_report(self) -> CredentialNetworkBoundaryReport:
        return CredentialNetworkBoundaryReportService().build_report()

    def load_v0294_credential_network_gate(self) -> Any:
        return self.load_v0294_credential_network_boundary_report().credential_network_gate

    def load_credential_access_candidates(self) -> list[Any]:
        return self.load_v0294_credential_network_boundary_report().credential_access_candidates

    def load_network_request_candidates(self) -> list[Any]:
        return self.load_v0294_credential_network_boundary_report().network_request_candidates

    def load_payload_boundary_policy(self) -> Any:
        return self.load_v0294_credential_network_boundary_report().payload_boundary_policy

    def load_request_response_redaction_boundary(self) -> Any:
        return self.load_v0294_credential_network_boundary_report().request_response_redaction_boundary

    def load_data_exfiltration_boundary_policy(self) -> Any:
        return self.load_v0294_credential_network_boundary_report().data_exfiltration_boundary_policy

    def load_provider_sdk_boundary_reports(self) -> list[Any]:
        return self.load_v0294_credential_network_boundary_report().provider_sdk_boundary_reports

    def load_v0293_permission_safety_report(self) -> AdapterPermissionSafetyReport:
        return AdapterPermissionSafetyReportService().build_report()

    def load_permission_decision_records(self) -> list[Any]:
        return self.load_v0293_permission_safety_report().decision_records

    def load_safety_classifications(self) -> list[Any]:
        return self.load_v0293_permission_safety_report().safety_classifications

    def load_action_intents(self) -> list[Any]:
        return self.load_v0293_permission_safety_report().action_intents

    def load_action_scopes(self) -> list[Any]:
        return self.load_v0293_permission_safety_report().action_scopes

    def load_v0292_mock_harness_report(self) -> MockAdapterHarnessReport:
        return MockAdapterHarnessReportService().build_report()

    def load_mock_run_reports(self) -> list[Any]:
        return self.load_v0292_mock_harness_report().mock_run_reports

    def load_v0291_adapter_registry_report(self) -> AdapterRegistryReport:
        return AdapterRegistryReportService().build_report()

    def load_adapter_capability_declarations(self) -> list[Any]:
        return self.load_v0291_adapter_registry_report().capability_declarations

    def load_v0290_schema_and_effect_contracts(self) -> dict[str, dict[str, Any]]:
        return {
            "effect": _ref("adapter_effect_boundary_contract", "adapter_effect_boundary_contract:v0.29.0", "v0.29.0"),
            "input": _ref("adapter_input_schema_contract", "adapter_input_schema_contract:v0.29.0", "v0.29.0"),
            "output": _ref("adapter_output_schema_contract", "adapter_output_schema_contract:v0.29.0", "v0.29.0"),
        }

    def load_provider_invocation_prohibition_contract(self) -> dict[str, Any]:
        return _ref("provider_invocation_prohibition_contract", "provider_invocation_prohibition_contract:v0.29.0", "v0.29.0")

    def load_command_execution_prohibition_contract(self) -> dict[str, Any]:
        return _ref("command_execution_prohibition_contract", "command_execution_prohibition_contract:v0.29.0", "v0.29.0")


class AdapterInvocationCandidatePolicyService:
    def build_policy(self) -> AdapterInvocationCandidatePolicy:
        return AdapterInvocationCandidatePolicy("adapter_invocation_candidate_policy:v0.29.5")


class AdapterInvocationCandidateRequestService:
    def build_request(self, source_view: AdapterInvocationCandidateSourceView) -> AdapterInvocationCandidateRequest:
        refs = [
            ref
            for ref in [
                source_view.credential_network_boundary_report_ref,
                source_view.permission_safety_report_ref,
                source_view.mock_harness_report_ref,
                source_view.adapter_registry_report_ref,
            ]
            if ref is not None
        ]
        return AdapterInvocationCandidateRequest(
            "adapter_invocation_candidate_request:v0.29.5",
            source_view.credential_network_boundary_report_ref.get("id") if source_view.credential_network_boundary_report_ref else None,
            source_view.permission_safety_report_ref.get("id") if source_view.permission_safety_report_ref else None,
            source_view.mock_harness_report_ref.get("id") if source_view.mock_harness_report_ref else None,
            source_view.adapter_registry_report_ref.get("id") if source_view.adapter_registry_report_ref else None,
            source_refs=refs,
        )


class AdapterInvocationCandidateSourceViewService:
    def build_source_view(self) -> AdapterInvocationCandidateSourceView:
        source = AdapterInvocationCandidatePrerequisiteSourceService()
        boundary_report = source.load_v0294_credential_network_boundary_report()
        permission_report = source.load_v0293_permission_safety_report()
        mock_report = source.load_v0292_mock_harness_report()
        registry_report = source.load_v0291_adapter_registry_report()
        contracts = source.load_v0290_schema_and_effect_contracts()
        return AdapterInvocationCandidateSourceView(
            "adapter_invocation_candidate_source_view:v0.29.5",
            _ref("credential_network_boundary_report", boundary_report.report_id, "v0.29.4"),
            _ref("credential_network_boundary_gate", boundary_report.credential_network_gate.gate_id, "v0.29.4"),
            _refs("credential_access_candidate", boundary_report.credential_access_candidates, "candidate_id", "v0.29.4"),
            _refs("network_request_candidate", boundary_report.network_request_candidates, "candidate_id", "v0.29.4"),
            _ref("payload_boundary_policy", boundary_report.payload_boundary_policy.policy_id, "v0.29.4"),
            _ref("request_response_redaction_boundary", boundary_report.request_response_redaction_boundary.boundary_id, "v0.29.4"),
            _ref("data_exfiltration_boundary_policy", boundary_report.data_exfiltration_boundary_policy.policy_id, "v0.29.4"),
            _refs("provider_sdk_boundary_report", boundary_report.provider_sdk_boundary_reports, "report_id", "v0.29.4"),
            _ref("adapter_permission_safety_report", permission_report.report_id, "v0.29.3"),
            _refs("adapter_permission_decision_record", permission_report.decision_records, "decision_record_id", "v0.29.3"),
            _refs("adapter_safety_classification", permission_report.safety_classifications, "classification_id", "v0.29.3"),
            _refs("adapter_action_intent", permission_report.action_intents, "intent_id", "v0.29.3"),
            _refs("adapter_action_scope", permission_report.action_scopes, "scope_id", "v0.29.3"),
            _ref("mock_adapter_harness_report", mock_report.report_id, "v0.29.2"),
            _refs("mock_adapter_run_report", mock_report.mock_run_reports, "report_id", "v0.29.2"),
            _ref("adapter_registry_report", registry_report.report_id, "v0.29.1"),
            _refs("adapter_capability_declaration", registry_report.capability_declarations, "declaration_id", "v0.29.1"),
            contracts["effect"],
            contracts["input"],
            contracts["output"],
            source.load_provider_invocation_prohibition_contract(),
            source.load_command_execution_prohibition_contract(),
            "complete",
            boundary_report.ready_for_invocation_candidate and boundary_report.ready_for_dry_run_plan,
            permission_report.ready_for_v0_29_4,
            mock_report.ready_for_v0_29_3,
        )


class AdapterInvocationIntentService:
    def build_intents(self, permission_report: AdapterPermissionSafetyReport) -> list[AdapterInvocationIntent]:
        intents: list[AdapterInvocationIntent] = []
        for adapter_name in _adapter_names(permission_report):
            spec = _spec(adapter_name)
            capability_name = "adapter_invocation_candidate"
            intents.append(
                AdapterInvocationIntent(
                    f"adapter_invocation_intent:{adapter_name}:v0.29.5",
                    adapter_name,
                    spec["provider_kind"],
                    capability_name,
                    spec["action_kind"],
                    f"{adapter_name} is represented as a v0.29.5 invocation candidate only.",
                    f"{adapter_name}.candidate_action",
                    spec["requires_provider"],
                    spec["requires_sdk"],
                    spec["requires_network"],
                    spec["requires_credentials"],
                    spec["requires_secret_reference"],
                    spec["requires_command"],
                    spec["requires_private_data"],
                    spec["requires_side_effect"],
                    spec["action_kind"] not in {"command_like_blocked"},
                )
            )
        return intents


class AdapterInvocationCandidateService:
    def build_candidates(
        self,
        intents: list[AdapterInvocationIntent],
        permission_report: AdapterPermissionSafetyReport,
        boundary_report: CredentialNetworkBoundaryReport,
    ) -> list[AdapterInvocationCandidate]:
        candidates: list[AdapterInvocationCandidate] = []
        for index, intent in enumerate(intents):
            spec = _spec(intent.adapter_name)
            decision = _safe_get(permission_report.decision_records, index)
            safety = _safe_get(permission_report.safety_classifications, index)
            credential_candidate = _safe_get(boundary_report.credential_access_candidates, index)
            network_candidate = _safe_get(boundary_report.network_request_candidates, index)
            candidates.append(
                AdapterInvocationCandidate(
                    f"adapter_invocation_candidate:{intent.adapter_name}:v0.29.5",
                    intent.adapter_name,
                    intent.capability_name,
                    _ref("adapter_invocation_intent", intent.intent_id, V0295_VERSION),
                    _ref("adapter_permission_decision_record", decision.decision_record_id, "v0.29.3") if decision else None,
                    _ref("adapter_safety_classification", safety.classification_id, "v0.29.3") if safety else None,
                    _ref("credential_access_candidate", credential_candidate.candidate_id, "v0.29.4") if credential_candidate else None,
                    _ref("network_request_candidate", network_candidate.candidate_id, "v0.29.4") if network_candidate else None,
                    spec["candidate_status"],
                    "Candidate created for v0.29.6 approval/audit/rollback input preparation only.",
                )
            )
        return candidates


class AdapterInvocationInputEnvelopeService:
    def build_envelopes(self, candidates: list[AdapterInvocationCandidate], source_view: AdapterInvocationCandidateSourceView) -> list[AdapterInvocationInputEnvelope]:
        return [
            AdapterInvocationInputEnvelope(
                f"adapter_invocation_input_envelope:{candidate.adapter_name}:v0.29.5",
                _ref("adapter_invocation_candidate", candidate.candidate_id, V0295_VERSION),
                candidate.adapter_name,
                candidate.capability_name,
                source_view.input_schema_contract_ref,
                [_ref("adapter_invocation_candidate", candidate.candidate_id, V0295_VERSION)],
            )
            for candidate in candidates
        ]


class AdapterInvocationPayloadPreviewService:
    def build_previews(
        self,
        candidates: list[AdapterInvocationCandidate],
        envelopes: list[AdapterInvocationInputEnvelope],
        source_view: AdapterInvocationCandidateSourceView,
    ) -> list[AdapterInvocationPayloadPreview]:
        previews: list[AdapterInvocationPayloadPreview] = []
        for candidate, envelope in zip(candidates, envelopes):
            previews.append(
                AdapterInvocationPayloadPreview(
                    f"adapter_invocation_payload_preview:{candidate.adapter_name}:v0.29.5",
                    _ref("adapter_invocation_candidate", candidate.candidate_id, V0295_VERSION),
                    _ref("adapter_invocation_input_envelope", envelope.envelope_id, V0295_VERSION),
                    source_view.payload_boundary_policy_ref,
                    source_view.request_response_redaction_boundary_ref,
                    "Metadata-only payload preview; no payload is sent and no raw/private/credential material is included.",
                )
            )
        return previews


class AdapterInvocationOutputSchemaPreviewService:
    def build_previews(self, candidates: list[AdapterInvocationCandidate], source_view: AdapterInvocationCandidateSourceView) -> list[AdapterInvocationOutputSchemaPreview]:
        return [
            AdapterInvocationOutputSchemaPreview(
                f"adapter_invocation_output_schema_preview:{candidate.adapter_name}:v0.29.5",
                _ref("adapter_invocation_candidate", candidate.candidate_id, V0295_VERSION),
                source_view.output_schema_contract_ref,
                ["status", "result_summary", "error"],
                ["error_code", "error_message"],
            )
            for candidate in candidates
        ]


class AdapterInvocationCheckService:
    def build_credential_reference_checks(
        self,
        candidates: list[AdapterInvocationCandidate],
        intents: list[AdapterInvocationIntent],
    ) -> list[AdapterInvocationCredentialReferenceCheck]:
        checks: list[AdapterInvocationCredentialReferenceCheck] = []
        for candidate, intent in zip(candidates, intents):
            checks.append(
                AdapterInvocationCredentialReferenceCheck(
                    f"adapter_invocation_credential_reference_check:{candidate.adapter_name}:v0.29.5",
                    _ref("adapter_invocation_candidate", candidate.candidate_id, V0295_VERSION),
                    candidate.credential_access_candidate_ref,
                    candidate.credential_access_candidate_ref,
                    intent.requires_secret_reference,
                    intent.requires_credentials,
                    check_status="warning" if intent.requires_credentials else "passed",
                )
            )
        return checks

    def build_network_boundary_checks(
        self,
        candidates: list[AdapterInvocationCandidate],
        intents: list[AdapterInvocationIntent],
    ) -> list[AdapterInvocationNetworkBoundaryCheck]:
        checks: list[AdapterInvocationNetworkBoundaryCheck] = []
        for candidate, intent in zip(candidates, intents):
            checks.append(
                AdapterInvocationNetworkBoundaryCheck(
                    f"adapter_invocation_network_boundary_check:{candidate.adapter_name}:v0.29.5",
                    _ref("adapter_invocation_candidate", candidate.candidate_id, V0295_VERSION),
                    candidate.network_request_candidate_ref,
                    candidate.network_request_candidate_ref,
                    candidate.network_request_candidate_ref is not None,
                    intent.requires_network,
                    check_status="warning" if intent.requires_network else "passed",
                )
            )
        return checks

    def build_permission_safety_checks(
        self,
        candidates: list[AdapterInvocationCandidate],
        intents: list[AdapterInvocationIntent],
    ) -> list[AdapterInvocationPermissionSafetyCheck]:
        checks: list[AdapterInvocationPermissionSafetyCheck] = []
        for candidate, intent in zip(candidates, intents):
            unsafe = intent.action_kind in {"command_like_blocked", "rpa_deferred"}
            checks.append(
                AdapterInvocationPermissionSafetyCheck(
                    f"adapter_invocation_permission_safety_check:{candidate.adapter_name}:v0.29.5",
                    _ref("adapter_invocation_candidate", candidate.candidate_id, V0295_VERSION),
                    candidate.permission_decision_ref,
                    candidate.safety_classification_ref,
                    candidate.candidate_status in {"approval_required_later", "deferred"},
                    unsafe,
                    check_status="warning" if candidate.candidate_status != "dry_run_ready" else "passed",
                )
            )
        return checks


class AdapterInvocationEffectPreviewService:
    def build_previews(
        self,
        candidates: list[AdapterInvocationCandidate],
        intents: list[AdapterInvocationIntent],
        source_view: AdapterInvocationCandidateSourceView,
    ) -> list[AdapterInvocationEffectPreview]:
        previews: list[AdapterInvocationEffectPreview] = []
        for candidate, intent in zip(candidates, intents):
            predicted = ["read_only_observation", "adapter_dry_run_plan_created"]
            if intent.requires_external_side_effect:
                predicted.append("future_external_side_effect_candidate")
            previews.append(
                AdapterInvocationEffectPreview(
                    f"adapter_invocation_effect_preview:{candidate.adapter_name}:v0.29.5",
                    _ref("adapter_invocation_candidate", candidate.candidate_id, V0295_VERSION),
                    source_view.effect_boundary_contract_ref,
                    predicted,
                    [],
                    intent.requires_external_side_effect,
                    preview_status="warning" if intent.requires_external_side_effect else "ready",
                )
            )
        return previews


class AdapterInvocationRiskPreviewService:
    def build_previews(self, candidates: list[AdapterInvocationCandidate], intents: list[AdapterInvocationIntent]) -> list[AdapterInvocationRiskPreview]:
        previews: list[AdapterInvocationRiskPreview] = []
        for candidate, intent in zip(candidates, intents):
            spec = _spec(intent.adapter_name)
            warning_count = sum(
                [
                    intent.requires_credentials,
                    intent.requires_network,
                    intent.requires_provider_invocation,
                    intent.requires_external_side_effect,
                    intent.requires_command_execution,
                ]
            )
            previews.append(
                AdapterInvocationRiskPreview(
                    f"adapter_invocation_risk_preview:{candidate.adapter_name}:v0.29.5",
                    _ref("adapter_invocation_candidate", candidate.candidate_id, V0295_VERSION),
                    RISK_DIMENSIONS,
                    spec["risk_level"],
                    0,
                    warning_count,
                    False,
                    candidate.candidate_status != "dry_run_ready",
                )
            )
        return previews


class AdapterInvocationDryRunPlanService:
    def build_steps(self, candidate: AdapterInvocationCandidate) -> list[AdapterInvocationDryRunStep]:
        return [
            AdapterInvocationDryRunStep(
                f"adapter_invocation_dry_run_step:{candidate.adapter_name}:{index}:v0.29.5",
                index,
                name,
                f"{name} is evaluated as a metadata/mock dry-run step only.",
            )
            for index, name in enumerate(DRY_RUN_STEP_NAMES, start=1)
        ]

    def build_plans(
        self,
        candidates: list[AdapterInvocationCandidate],
        envelopes: list[AdapterInvocationInputEnvelope],
        payload_previews: list[AdapterInvocationPayloadPreview],
        output_previews: list[AdapterInvocationOutputSchemaPreview],
        credential_checks: list[AdapterInvocationCredentialReferenceCheck],
        network_checks: list[AdapterInvocationNetworkBoundaryCheck],
        permission_checks: list[AdapterInvocationPermissionSafetyCheck],
        effect_previews: list[AdapterInvocationEffectPreview],
        risk_previews: list[AdapterInvocationRiskPreview],
    ) -> list[AdapterInvocationDryRunPlan]:
        plans: list[AdapterInvocationDryRunPlan] = []
        for index, candidate in enumerate(candidates):
            spec = _spec(candidate.adapter_name)
            plans.append(
                AdapterInvocationDryRunPlan(
                    f"adapter_invocation_dry_run_plan:{candidate.adapter_name}:v0.29.5",
                    _ref("adapter_invocation_candidate", candidate.candidate_id, V0295_VERSION),
                    _ref("adapter_invocation_input_envelope", envelopes[index].envelope_id, V0295_VERSION),
                    _ref("adapter_invocation_payload_preview", payload_previews[index].payload_preview_id, V0295_VERSION),
                    _ref("adapter_invocation_output_schema_preview", output_previews[index].output_preview_id, V0295_VERSION),
                    _ref("adapter_invocation_credential_reference_check", credential_checks[index].check_id, V0295_VERSION),
                    _ref("adapter_invocation_network_boundary_check", network_checks[index].check_id, V0295_VERSION),
                    _ref("adapter_invocation_permission_safety_check", permission_checks[index].check_id, V0295_VERSION),
                    _ref("adapter_invocation_effect_preview", effect_previews[index].effect_preview_id, V0295_VERSION),
                    _ref("adapter_invocation_risk_preview", risk_previews[index].risk_preview_id, V0295_VERSION),
                    self.build_steps(candidate),
                    spec["run_mode"],
                    True,
                    plan_status="warning" if spec["run_mode"] == "not_run" else "ready",
                )
            )
        return plans


class AdapterInvocationDryRunReportService:
    def build_results(self, plan: AdapterInvocationDryRunPlan) -> list[AdapterInvocationDryRunResult]:
        return [
            AdapterInvocationDryRunResult(
                f"adapter_invocation_dry_run_result:{step.step_id}",
                _ref("adapter_invocation_dry_run_step", step.step_id, V0295_VERSION),
                "passed" if plan.run_mode != "not_run" else "warning",
                f"{step.step_name} completed as metadata/mock dry-run validation only.",
            )
            for step in plan.dry_run_steps
        ]

    def build_reports(self, plans: list[AdapterInvocationDryRunPlan]) -> list[AdapterInvocationDryRunReport]:
        reports: list[AdapterInvocationDryRunReport] = []
        for plan in plans:
            adapter_name = plan.plan_id.split(":")[1]
            reports.append(
                AdapterInvocationDryRunReport(
                    f"adapter_invocation_dry_run_report:{adapter_name}:v0.29.5",
                    _ref("adapter_invocation_dry_run_plan", plan.plan_id, V0295_VERSION),
                    plan.candidate_ref,
                    self.build_results(plan),
                    plan.run_mode != "not_run",
                    plan.run_mode,
                    "passed" if plan.run_mode != "not_run" else "warning",
                )
            )
        return reports


class AdapterInvocationNoOpPlanService:
    def build_plans(self, candidates: list[AdapterInvocationCandidate]) -> list[AdapterInvocationNoOpPlan]:
        return [
            AdapterInvocationNoOpPlan(
                f"adapter_invocation_noop_plan:{candidate.adapter_name}:v0.29.5",
                _ref("adapter_invocation_candidate", candidate.candidate_id, V0295_VERSION),
                "No-op is available whenever provider, network, credential, approval, or side-effect gates are missing.",
                FALLBACK_DECISIONS,
            )
            for candidate in candidates
        ]


class AdapterInvocationFailureModePreviewService:
    def build_previews(self, candidates: list[AdapterInvocationCandidate]) -> list[AdapterInvocationFailureModePreview]:
        return [
            AdapterInvocationFailureModePreview(
                f"adapter_invocation_failure_mode_preview:{candidate.adapter_name}:v0.29.5",
                _ref("adapter_invocation_candidate", candidate.candidate_id, V0295_VERSION),
                FAILURE_MODES,
            )
            for candidate in candidates
        ]


class AdapterInvocationReadinessGateService:
    def evaluate_gate(
        self,
        source_view: AdapterInvocationCandidateSourceView,
        candidates: list[AdapterInvocationCandidate],
        payload_previews: list[AdapterInvocationPayloadPreview],
        output_previews: list[AdapterInvocationOutputSchemaPreview],
        credential_checks: list[AdapterInvocationCredentialReferenceCheck],
        network_checks: list[AdapterInvocationNetworkBoundaryCheck],
        permission_checks: list[AdapterInvocationPermissionSafetyCheck],
        effect_previews: list[AdapterInvocationEffectPreview],
        risk_previews: list[AdapterInvocationRiskPreview],
        dry_run_plans: list[AdapterInvocationDryRunPlan],
        dry_run_reports: list[AdapterInvocationDryRunReport],
        noop_plans: list[AdapterInvocationNoOpPlan],
    ) -> AdapterInvocationReadinessGate:
        all_present = all(
            [
                candidates,
                payload_previews,
                output_previews,
                credential_checks,
                network_checks,
                permission_checks,
                effect_previews,
                risk_previews,
                dry_run_plans,
                dry_run_reports,
                noop_plans,
            ]
        )
        no_provider = all(not candidate.provider_invoked_now and not candidate.provider_sdk_invoked_now for candidate in candidates)
        no_network = all(not check.network_called_now and not check.outbound_request_sent_now for check in network_checks)
        no_credentials = all(not check.credential_value_accessed_now for check in credential_checks)
        no_command = all(not candidate.command_executed_now for candidate in candidates)
        no_side_effect = all(not preview.external_side_effect_performed_now and not preview.file_mutated_now for preview in effect_previews)
        ready = all_present and no_provider and no_network and no_credentials and no_command and no_side_effect
        return AdapterInvocationReadinessGate(
            "adapter_invocation_readiness_gate:v0.29.5",
            _ref("adapter_invocation_candidate_source_view", source_view.source_view_id, V0295_VERSION),
            _refs("adapter_invocation_candidate", candidates, "candidate_id", V0295_VERSION),
            _refs("adapter_invocation_payload_preview", payload_previews, "payload_preview_id", V0295_VERSION),
            _refs("adapter_invocation_output_schema_preview", output_previews, "output_preview_id", V0295_VERSION),
            _refs("adapter_invocation_credential_reference_check", credential_checks, "check_id", V0295_VERSION),
            _refs("adapter_invocation_network_boundary_check", network_checks, "check_id", V0295_VERSION),
            _refs("adapter_invocation_permission_safety_check", permission_checks, "check_id", V0295_VERSION),
            _refs("adapter_invocation_effect_preview", effect_previews, "effect_preview_id", V0295_VERSION),
            _refs("adapter_invocation_risk_preview", risk_previews, "risk_preview_id", V0295_VERSION),
            _refs("adapter_invocation_dry_run_plan", dry_run_plans, "plan_id", V0295_VERSION),
            _refs("adapter_invocation_dry_run_report", dry_run_reports, "report_id", V0295_VERSION),
            _refs("adapter_invocation_noop_plan", noop_plans, "noop_plan_id", V0295_VERSION),
            bool(candidates),
            bool(payload_previews),
            bool(output_previews),
            all(check.check_status in {"passed", "warning"} for check in credential_checks),
            all(check.check_status in {"passed", "warning"} for check in network_checks),
            all(check.check_status in {"passed", "warning"} for check in permission_checks),
            bool(effect_previews),
            bool(risk_previews),
            bool(dry_run_plans),
            all(report.dry_run_status in {"passed", "warning"} for report in dry_run_reports),
            all(plan.noop_available for plan in noop_plans),
            no_provider,
            no_network,
            no_credentials,
            no_command,
            no_side_effect,
            "warning",
            ready,
            ready,
        )


class AdapterInvocationCandidateAuditTrailService:
    def build_audit_trail(
        self,
        request: AdapterInvocationCandidateRequest,
        source_view: AdapterInvocationCandidateSourceView,
        candidates: list[AdapterInvocationCandidate],
        dry_run_plans: list[AdapterInvocationDryRunPlan],
        dry_run_reports: list[AdapterInvocationDryRunReport],
        gate: AdapterInvocationReadinessGate,
    ) -> AdapterInvocationCandidateAuditTrail:
        return AdapterInvocationCandidateAuditTrail(
            "adapter_invocation_candidate_audit_trail:v0.29.5",
            _ref("adapter_invocation_candidate_request", request.request_id, V0295_VERSION),
            _ref("adapter_invocation_candidate_source_view", source_view.source_view_id, V0295_VERSION),
            _refs("adapter_invocation_candidate", candidates, "candidate_id", V0295_VERSION),
            _refs("adapter_invocation_dry_run_plan", dry_run_plans, "plan_id", V0295_VERSION),
            _refs("adapter_invocation_dry_run_report", dry_run_reports, "report_id", V0295_VERSION),
            _ref("adapter_invocation_readiness_gate", gate.gate_id, V0295_VERSION),
            5 + len(candidates) + len(dry_run_plans) + len(dry_run_reports),
        )


class AdapterInvocationCandidateFindingService:
    BLOCKED_FINDINGS = {
        "provider_invocation_attempted",
        "provider_sdk_invocation_attempted",
        "provider_registration_attempted",
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

    def build_findings(self) -> list[AdapterInvocationCandidateFinding]:
        return [
            AdapterInvocationCandidateFinding(
                "adapter_invocation_candidate_finding:policy:v0.29.5",
                "info",
                "invocation_candidate_policy_created",
                "Invocation candidate policy created with provider, network, credential, command, and side-effect execution disabled.",
                _ref("adapter_invocation_candidate_policy", "adapter_invocation_candidate_policy:v0.29.5", V0295_VERSION),
                [],
                None,
            ),
            AdapterInvocationCandidateFinding(
                "adapter_invocation_candidate_finding:dry-run:v0.29.5",
                "info",
                "dry_run_plan_created",
                "Dry-run plans and reports are metadata/mock-only and are not provider calls or live results.",
                _ref("adapter_invocation_dry_run_plan", "adapter_invocation_dry_run_plan:internal_mock_adapter:v0.29.5", V0295_VERSION),
                [],
                "Withdraw if any dry-run step invokes providers, calls network, accesses credentials, executes commands, mutates files, or performs side effects.",
            ),
            AdapterInvocationCandidateFinding(
                "adapter_invocation_candidate_finding:gate:v0.29.5",
                "warning",
                "readiness_gate_created",
                "Readiness is for v0.29.6 approval/audit/rollback boundary only; provider, network, credential, and command readiness remain false.",
                _ref("adapter_invocation_readiness_gate", "adapter_invocation_readiness_gate:v0.29.5", V0295_VERSION),
                [],
                "Withdraw if provider, network, credential, command, side-effect, or live adapter readiness becomes true.",
            ),
        ]


class AdapterInvocationCandidateReportService:
    def build_report(self, report_id: str | None = None) -> AdapterInvocationCandidateReport:
        source_service = AdapterInvocationCandidatePrerequisiteSourceService()
        boundary_report = source_service.load_v0294_credential_network_boundary_report()
        permission_report = source_service.load_v0293_permission_safety_report()
        source_view = AdapterInvocationCandidateSourceViewService().build_source_view()
        policy = AdapterInvocationCandidatePolicyService().build_policy()
        request = AdapterInvocationCandidateRequestService().build_request(source_view)
        intents = AdapterInvocationIntentService().build_intents(permission_report)
        candidates = AdapterInvocationCandidateService().build_candidates(intents, permission_report, boundary_report)
        envelopes = AdapterInvocationInputEnvelopeService().build_envelopes(candidates, source_view)
        payload_previews = AdapterInvocationPayloadPreviewService().build_previews(candidates, envelopes, source_view)
        output_previews = AdapterInvocationOutputSchemaPreviewService().build_previews(candidates, source_view)
        check_service = AdapterInvocationCheckService()
        credential_checks = check_service.build_credential_reference_checks(candidates, intents)
        network_checks = check_service.build_network_boundary_checks(candidates, intents)
        permission_checks = check_service.build_permission_safety_checks(candidates, intents)
        effect_previews = AdapterInvocationEffectPreviewService().build_previews(candidates, intents, source_view)
        risk_previews = AdapterInvocationRiskPreviewService().build_previews(candidates, intents)
        dry_run_plans = AdapterInvocationDryRunPlanService().build_plans(
            candidates,
            envelopes,
            payload_previews,
            output_previews,
            credential_checks,
            network_checks,
            permission_checks,
            effect_previews,
            risk_previews,
        )
        dry_run_reports = AdapterInvocationDryRunReportService().build_reports(dry_run_plans)
        noop_plans = AdapterInvocationNoOpPlanService().build_plans(candidates)
        failure_previews = AdapterInvocationFailureModePreviewService().build_previews(candidates)
        gate = AdapterInvocationReadinessGateService().evaluate_gate(
            source_view,
            candidates,
            payload_previews,
            output_previews,
            credential_checks,
            network_checks,
            permission_checks,
            effect_previews,
            risk_previews,
            dry_run_plans,
            dry_run_reports,
            noop_plans,
        )
        audit_trail = AdapterInvocationCandidateAuditTrailService().build_audit_trail(
            request, source_view, candidates, dry_run_plans, dry_run_reports, gate
        )
        findings = AdapterInvocationCandidateFindingService().build_findings()
        return AdapterInvocationCandidateReport(
            report_id or "adapter_invocation_candidate_report:v0.29.5",
            _now(),
            policy,
            request,
            source_view,
            intents,
            candidates,
            envelopes,
            payload_previews,
            output_previews,
            credential_checks,
            network_checks,
            permission_checks,
            effect_previews,
            risk_previews,
            dry_run_plans,
            dry_run_reports,
            noop_plans,
            failure_previews,
            gate,
            audit_trail,
            findings,
            "warning",
            gate.ready_for_v0_29_6,
            gate.ready_for_approval_audit_rollback_boundary,
            limitations=["v0.29.5 creates invocation candidates and dry-run artifacts only. Approval/audit/rollback, certification, and limited invocation remain future work."],
            withdrawal_conditions=["Withdraw if providers, provider SDKs, network, credentials, secrets, commands, side effects, file mutation, live adapters, private/raw data, or LLM-judge-only authority appear."],
        )

    def build_all_parts(self, report_id: str | None = None) -> dict[str, Any]:
        report = self.build_report(report_id=report_id)
        return {
            "policy": report.policy,
            "request": report.request,
            "source-view": report.source_view,
            "intents": report.invocation_intents,
            "candidates": report.invocation_candidates,
            "input-envelope": report.input_envelopes,
            "payload-preview": report.payload_previews,
            "output-preview": report.output_schema_previews,
            "credential-check": report.credential_reference_checks,
            "network-check": report.network_boundary_checks,
            "permission-safety-check": report.permission_safety_checks,
            "effect-preview": report.effect_previews,
            "risk-preview": report.risk_previews,
            "dry-run-plan": report.dry_run_plans,
            "dry-run-report": report.dry_run_reports,
            "noop": report.noop_plans,
            "failure-preview": report.failure_mode_previews,
            "gate": report.readiness_gate,
            "audit": report.audit_trail,
            "findings": report.findings,
            "report": report,
        }

    def build_pig_report(self) -> dict[str, Any]:
        report = self.build_report()
        return {
            "version": V0295_VERSION,
            "layer": V0295_LAYER,
            "subject": "adapter_invocation_candidate_dry_run_plan",
            "principles": [
                "Invocation candidate is not invocation",
                "Dry-run plan is not provider call",
                "Dry-run report is not live result",
                "Payload preview is not payload send",
                "Output schema preview is not provider response",
                "Credential reference binding is not credential access",
                "Network request candidate is not network request",
                "Effect preview is not side effect",
                "Risk preview is not approval",
                "No-op / deny / defer are valid outcomes",
            ],
            "safety_boundary": {
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
                "v0.29.6 Provider Invocation Approval / Audit / Rollback Boundary",
                "v0.29.7 External Skill Packaging / Certification Matrix",
                "v0.29.8 Limited Provider Invocation Preview Gate",
                "v0.29.9 External Provider Adapter Foundation Consolidation",
            ],
            "next_step": V0295_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "adapter_invocation_candidate_dry_run_plan_created",
            "version": V0295_VERSION,
            "source_read_models": [
                "CredentialNetworkBoundaryGateState",
                "CredentialAccessCandidateState",
                "NetworkRequestCandidateState",
                "PayloadBoundaryState",
                "RequestResponseRedactionBoundaryState",
                "DataExfiltrationBoundaryState",
                "ProviderSDKBoundaryState",
                "AdapterPermissionSafetyGateState",
                "AdapterPermissionDecisionRecordState",
                "AdapterSafetyClassificationState",
                "AdapterActionIntentState",
                "AdapterActionScopeState",
                "MockAdapterHarnessState",
                "MockAdapterRunState",
                "AdapterRegistryState",
                "AdapterCapabilityDeclarationState",
                "AdapterEffectBoundaryContractState",
                "AdapterSchemaContractState",
                "ProviderInvocationProhibitionState",
                "CommandExecutionProhibitionState",
                "PigGuidanceState",
                "OCPXProjectionState",
            ],
            "target_read_models": [
                "AdapterInvocationCandidateState",
                "AdapterInvocationIntentState",
                "AdapterInvocationInputEnvelopeState",
                "AdapterPayloadPreviewState",
                "AdapterOutputSchemaPreviewState",
                "AdapterInvocationCheckState",
                "AdapterEffectPreviewState",
                "AdapterRiskPreviewState",
                "AdapterDryRunPlanState",
                "AdapterDryRunReportState",
                "AdapterNoOpPlanState",
                "AdapterInvocationReadinessGateState",
                "AdapterInvocationAuditState",
                "V029ReadinessState",
            ],
            "effect_types": V0295_EFFECT_TYPES,
            "forbidden_effect_types": V0295_FORBIDDEN_EFFECT_TYPES,
        }


def render_adapter_invocation_candidate_cli(parts: dict[str, Any], section: str = "report") -> str:
    report: AdapterInvocationCandidateReport = parts["report"]
    lines = [
        f"Adapter Invocation Candidate / Dry-Run Plan {section}",
        f"version={report.version}",
        f"layer={report.policy.layer}",
        f"report_status={report.report_status}",
        f"ready_for_v0_29_6={_bool(report.ready_for_v0_29_6)}",
        f"ready_for_approval_audit_rollback_boundary={_bool(report.ready_for_approval_audit_rollback_boundary)}",
        f"ready_for_provider_invocation={_bool(report.ready_for_provider_invocation)}",
        f"ready_for_network_access={_bool(report.ready_for_network_access)}",
        f"ready_for_credential_access={_bool(report.ready_for_credential_access)}",
        f"ready_for_command_execution={_bool(report.ready_for_command_execution)}",
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
