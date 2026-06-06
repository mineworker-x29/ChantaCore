from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.external_provider_adapter_contract import ModelMixin, _bool, _ref
from chanta_core.permission_safety_scope_gate_for_external_adapters import (
    AdapterPermissionSafetyReport,
    AdapterPermissionSafetyReportService,
)
from chanta_core.provider_capability_inventory_adapter_registry import (
    AdapterRegistryReport,
    AdapterRegistryReportService,
)
from chanta_core.utility.time import utc_now_iso


V0294_VERSION = "v0.29.4"
V0294_LAYER = "external_provider_adapter"
V0294_TRACK = "External Skill / External Provider Adapter Development"
V0294_NAME = "Credential / Secret / Network Boundary"
V0294_NEXT_STEP = "v0.29.5 Adapter Invocation Candidate / Dry-Run Plan"

V0294_OBJECT_TYPES = [
    "credential_secret_network_boundary_policy",
    "credential_network_boundary_request",
    "credential_network_boundary_source_view",
    "credential_boundary_policy",
    "credential_material_classification",
    "secret_reference_policy",
    "secret_reference_descriptor",
    "external_secret_store_contract",
    "credential_redaction_policy",
    "credential_audit_policy",
    "credential_scope_binding",
    "credential_access_candidate",
    "credential_boundary_report",
    "network_boundary_policy",
    "outbound_domain_policy",
    "outbound_domain_rule",
    "network_request_policy",
    "network_request_candidate",
    "network_timeout_retry_policy",
    "provider_sdk_boundary_policy",
    "provider_sdk_boundary_report",
    "data_exfiltration_boundary_policy",
    "payload_boundary_policy",
    "request_response_redaction_boundary",
    "network_audit_boundary",
    "credential_network_boundary_gate",
    "credential_network_boundary_audit_trail",
    "credential_network_boundary_finding",
    "credential_network_boundary_report",
    "adapter_permission_safety_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

V0294_EVENT_TYPES = [
    "credential_network_boundary_requested",
    "credential_network_boundary_prerequisites_loaded",
    "credential_secret_network_boundary_policy_created",
    "credential_boundary_policy_created",
    "credential_material_classification_created",
    "secret_reference_policy_created",
    "secret_reference_descriptor_created",
    "external_secret_store_contract_created",
    "credential_redaction_policy_created",
    "credential_audit_policy_created",
    "credential_scope_binding_created",
    "credential_access_candidate_created",
    "credential_boundary_report_created",
    "network_boundary_policy_created",
    "outbound_domain_policy_created",
    "outbound_domain_rule_created",
    "network_request_policy_created",
    "network_request_candidate_created",
    "network_timeout_retry_policy_created",
    "provider_sdk_boundary_policy_created",
    "provider_sdk_boundary_report_created",
    "data_exfiltration_boundary_policy_created",
    "payload_boundary_policy_created",
    "request_response_redaction_boundary_created",
    "network_audit_boundary_created",
    "credential_network_boundary_gate_evaluated",
    "credential_network_boundary_audit_trail_created",
    "credential_network_boundary_report_created",
    "credential_network_boundary_warning_created",
    "credential_network_boundary_blocked",
]

V0294_EFFECT_TYPES = [
    "read_only_observation",
    "credential_boundary_policy_created",
    "secret_reference_boundary_created",
    "credential_access_candidate_created",
    "network_boundary_policy_created",
    "outbound_domain_policy_created",
    "network_request_candidate_created",
    "provider_sdk_boundary_report_created",
    "data_exfiltration_boundary_created",
    "credential_network_boundary_gate_evaluated",
    "credential_network_boundary_audit_trail_created",
    "state_candidate_created",
]

V0294_FORBIDDEN_EFFECT_TYPES = [
    "credential_value_stored",
    "credential_value_logged",
    "env_file_created",
    "secret_retrieved",
    "secret_materialized",
    "provider_sdk_invoked",
    "provider_invoked",
    "network_called",
    "outbound_request_sent",
    "webhook_called",
    "websocket_connected",
    "command_executed",
    "shell_execution_surface_created",
    "subprocess_expansion_added",
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

SUPPORTED_FUTURE_STORE_KINDS = [
    "environment_secret_store",
    "OS_keychain",
    "enterprise_secret_manager",
    "CI_secret_store",
    "unknown",
]

BOUNDARY_BLUEPRINTS = {
    "internal_mock_adapter": ("internal_mock_provider", "none", False, False, "none", "ready"),
    "generic_llm_adapter": ("llm_provider", "api_key", True, True, "high", "warning"),
    "generic_search_adapter": ("search_provider", "none", False, True, "medium", "warning"),
    "generic_workflow_adapter": ("workflow_provider", "service_account", True, True, "high", "warning"),
    "generic_rpa_adapter": ("rpa_provider", "enterprise_secret_ref", True, True, "blocked", "warning"),
}


def _now() -> str:
    return utc_now_iso()


def _refs(object_type: str, items: list[Any], attr: str, version: str) -> list[dict[str, Any]]:
    return [_ref(object_type, getattr(item, attr), version) for item in items]


def _adapter_names(report: AdapterPermissionSafetyReport) -> list[str]:
    return [intent.adapter_name for intent in report.action_intents] or list(BOUNDARY_BLUEPRINTS)


def _spec(adapter_name: str) -> tuple[str, str, bool, bool, str, str]:
    return BOUNDARY_BLUEPRINTS.get(adapter_name, ("unknown", "unknown", True, True, "unknown", "unknown"))


@dataclass
class CredentialSecretNetworkBoundaryPolicy(ModelMixin):
    policy_id: str
    boundary_enabled: bool = True
    credential_boundary_required: bool = True
    secret_reference_required: bool = True
    external_secret_store_contract_required: bool = True
    credential_redaction_required: bool = True
    credential_audit_required: bool = True
    network_boundary_required: bool = True
    outbound_domain_policy_required: bool = True
    timeout_retry_policy_required: bool = True
    data_exfiltration_boundary_required: bool = True
    provider_sdk_boundary_required: bool = True
    credential_storage_enabled_now: bool = False
    credential_logging_enabled_now: bool = False
    env_file_creation_enabled_now: bool = False
    secret_retrieval_enabled_now: bool = False
    network_access_enabled_now: bool = False
    provider_sdk_invocation_enabled_now: bool = False
    provider_invocation_enabled_now: bool = False
    command_execution_expansion_enabled_now: bool = False
    live_adapter_implementation_enabled_now: bool = False
    rpa_adapter_enabled_now: bool = False
    external_agent_dominion_enabled_now: bool = False
    no_credential_value_default: bool = True
    no_network_default: bool = True
    no_provider_invocation_default: bool = True
    llm_judge_as_sole_boundary_authority_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION
    layer: str = V0294_LAYER


@dataclass
class CredentialNetworkBoundaryRequest(ModelMixin):
    request_id: str
    permission_safety_report_id: str | None
    mock_harness_report_id: str | None
    adapter_registry_report_id: str | None
    requested_boundary_scope: str = "full_credential_secret_network_boundary"
    strictness: str = "standard"
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class CredentialNetworkBoundarySourceView(ModelMixin):
    source_view_id: str
    permission_safety_report_ref: dict[str, Any] | None
    permission_safety_gate_ref: dict[str, Any] | None
    credential_safety_check_refs: list[dict[str, Any]]
    network_safety_check_refs: list[dict[str, Any]]
    permission_decision_record_refs: list[dict[str, Any]]
    safety_classification_refs: list[dict[str, Any]]
    action_intent_refs: list[dict[str, Any]]
    action_scope_refs: list[dict[str, Any]]
    no_network_boundary_refs: list[dict[str, Any]]
    provider_sdk_isolation_refs: list[dict[str, Any]]
    mock_credential_boundary_refs: list[dict[str, Any]]
    credential_need_declaration_refs: list[dict[str, Any]]
    network_need_declaration_refs: list[dict[str, Any]]
    adapter_risk_profile_refs: list[dict[str, Any]]
    credential_requirement_contract_ref: dict[str, Any] | None
    network_requirement_contract_ref: dict[str, Any] | None
    audit_requirement_contract_ref: dict[str, Any] | None
    provider_invocation_prohibition_ref: dict[str, Any] | None
    command_execution_prohibition_ref: dict[str, Any] | None
    source_status: str
    credential_sensitivity_present: bool
    network_sensitivity_present: bool
    credential_value_detected: bool = False
    credential_storage_detected: bool = False
    credential_logging_detected: bool = False
    env_file_detected: bool = False
    network_call_detected: bool = False
    provider_sdk_invocation_detected: bool = False
    provider_invocation_detected: bool = False
    command_execution_detected: bool = False
    private_data_detected: bool = False
    raw_provider_output_detected: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class CredentialBoundaryPolicy(ModelMixin):
    policy_id: str
    credential_boundary_required: bool = True
    credential_values_forbidden_now: bool = True
    credential_storage_forbidden_now: bool = True
    credential_logging_forbidden_now: bool = True
    env_file_creation_forbidden_now: bool = True
    committed_credentials_forbidden: bool = True
    secret_reference_only_required: bool = True
    credential_materialization_forbidden_now: bool = True
    credential_access_requires_future_approval_gate: bool = True
    credential_access_candidate_allowed: bool = True
    credential_access_candidate_is_not_access: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class CredentialMaterialClassification(ModelMixin):
    classification_id: str
    adapter_name: str
    capability_name: str
    credential_kind: str
    sensitivity_level: str
    credential_required_later: bool
    secret_reference_required: bool
    classification_status: str
    credential_value_present_now: bool = False
    credential_storage_allowed_now: bool = False
    credential_logging_allowed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class SecretReferencePolicy(ModelMixin):
    policy_id: str
    secret_reference_required: bool = True
    secret_reference_is_not_secret_value: bool = True
    secret_reference_must_be_opaque: bool = True
    secret_reference_must_not_include_value: bool = True
    secret_reference_must_not_be_logged_as_value: bool = True
    secret_reference_scope_required: bool = True
    secret_reference_expiry_required_later: bool = True
    secret_reference_audit_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class SecretReferenceDescriptor(ModelMixin):
    descriptor_id: str
    adapter_name: str
    capability_name: str
    secret_ref_name: str
    secret_ref_kind: str
    secret_ref_scope: str | None
    secret_ref_purpose: str
    secret_ref_status: str
    secret_value_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class ExternalSecretStoreContract(ModelMixin):
    contract_id: str
    supported_future_store_kinds: list[str]
    contract_status: str
    external_secret_store_required_later: bool = True
    secret_store_integration_enabled_now: bool = False
    secret_retrieval_enabled_now: bool = False
    secret_write_enabled_now: bool = False
    secret_rotation_required_later: bool = True
    secret_access_audit_required: bool = True
    secret_redaction_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class CredentialRedactionPolicy(ModelMixin):
    policy_id: str
    credential_redaction_required: bool = True
    redact_secret_like_values: bool = True
    redact_tokens: bool = True
    redact_api_keys: bool = True
    redact_session_cookies: bool = True
    redact_private_endpoints_when_sensitive: bool = True
    raw_credential_output_forbidden: bool = True
    redaction_is_not_access_permission: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class CredentialAuditPolicy(ModelMixin):
    policy_id: str
    credential_audit_required: bool = True
    audit_secret_reference_only: bool = True
    audit_credential_value_forbidden: bool = True
    audit_access_candidate_required: bool = True
    audit_access_decision_required_later: bool = True
    audit_redaction_required: bool = True
    audit_ocel_event_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class CredentialScopeBinding(ModelMixin):
    binding_id: str
    adapter_name: str
    capability_name: str
    permission_scope_ref: dict[str, Any] | None
    credential_classification_ref: dict[str, Any] | None
    secret_reference_ref: dict[str, Any] | None
    scope_bound_to_credential_ref: bool
    scope_minimal: bool
    scope_expiry_required: bool
    credential_access_allowed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class CredentialAccessCandidate(ModelMixin):
    candidate_id: str
    adapter_name: str
    capability_name: str
    credential_scope_binding_ref: dict[str, Any]
    secret_reference_ref: dict[str, Any] | None
    candidate_reason: str
    candidate_status: str
    credential_access_candidate_is_access: bool = False
    credential_value_accessed_now: bool = False
    credential_value_stored_now: bool = False
    credential_value_logged_now: bool = False
    required_future_gate: str = "v0.29.6 Provider Invocation Approval / Audit / Rollback Boundary"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class CredentialBoundaryReport(ModelMixin):
    report_id: str
    credential_policy_ref: dict[str, Any]
    material_classification_refs: list[dict[str, Any]]
    secret_reference_policy_ref: dict[str, Any]
    secret_reference_descriptor_refs: list[dict[str, Any]]
    external_secret_store_contract_ref: dict[str, Any]
    redaction_policy_ref: dict[str, Any]
    audit_policy_ref: dict[str, Any]
    scope_binding_refs: list[dict[str, Any]]
    access_candidate_refs: list[dict[str, Any]]
    credential_boundary_status: str
    credential_values_present: bool = False
    credential_stored: bool = False
    credential_logged: bool = False
    env_file_created: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class NetworkBoundaryPolicy(ModelMixin):
    policy_id: str
    network_boundary_required: bool = True
    no_network_default: bool = True
    network_access_enabled_now: bool = False
    outbound_network_forbidden_now: bool = True
    provider_sdk_network_forbidden_now: bool = True
    network_request_candidate_allowed: bool = True
    network_request_candidate_is_not_request: bool = True
    outbound_domain_policy_required: bool = True
    timeout_retry_policy_required: bool = True
    request_audit_required: bool = True
    data_exfiltration_boundary_required: bool = True
    future_network_reopen_version: str = "v0.29.8 Limited Provider Invocation Preview Gate"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class OutboundDomainPolicy(ModelMixin):
    policy_id: str
    outbound_domain_policy_required: bool = True
    allowlist_required_later: bool = True
    wildcard_domain_forbidden: bool = True
    unknown_domain_forbidden: bool = True
    private_network_forbidden_now: bool = True
    internal_network_forbidden_now: bool = True
    domain_policy_is_not_network_access: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class OutboundDomainRule(ModelMixin):
    rule_id: str
    adapter_name: str
    provider_kind: str
    domain_pattern: str | None
    domain_rule_kind: str
    rule_status: str
    wildcard: bool = False
    internal_domain: bool = False
    private_network: bool = False
    network_access_allowed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class NetworkRequestPolicy(ModelMixin):
    policy_id: str
    network_request_policy_required: bool = True
    network_request_candidate_allowed: bool = True
    real_network_request_forbidden_now: bool = True
    request_method_declaration_required: bool = True
    endpoint_declaration_required: bool = True
    payload_boundary_required: bool = True
    response_boundary_required: bool = True
    request_audit_required: bool = True
    timeout_required: bool = True
    retry_policy_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class NetworkRequestCandidate(ModelMixin):
    candidate_id: str
    adapter_name: str
    capability_name: str
    provider_kind: str
    method_candidate: str | None
    endpoint_ref: dict[str, Any] | None
    outbound_domain_rule_ref: dict[str, Any] | None
    payload_boundary_ref: dict[str, Any] | None
    timeout_retry_policy_ref: dict[str, Any] | None
    candidate_reason: str
    candidate_status: str
    network_request_candidate_is_request: bool = False
    network_called_now: bool = False
    provider_invoked_now: bool = False
    required_future_gate: str = "v0.29.8 Limited Provider Invocation Preview Gate"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class NetworkTimeoutRetryPolicy(ModelMixin):
    policy_id: str
    timeout_policy_required: bool = True
    retry_policy_required: bool = True
    bounded_timeout_required: bool = True
    bounded_retry_required: bool = True
    exponential_backoff_required_later: bool = True
    infinite_retry_forbidden: bool = True
    retry_on_auth_failure_forbidden: bool = True
    timeout_retry_policy_is_not_network_execution: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class ProviderSDKBoundaryPolicy(ModelMixin):
    policy_id: str
    provider_sdk_boundary_required: bool = True
    provider_sdk_runtime_dependency_forbidden_now: bool = True
    provider_sdk_import_forbidden_now: bool = True
    provider_sdk_invocation_forbidden_now: bool = True
    provider_sdk_optional_dependency_group_allowed_later: bool = True
    provider_sdk_mock_substitution_required: bool = True
    provider_sdk_boundary_is_not_sdk_readiness: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class ProviderSDKBoundaryReport(ModelMixin):
    report_id: str
    provider_sdk_policy_ref: dict[str, Any]
    adapter_name: str
    optional_dependency_group_defined_later: bool | None
    sdk_boundary_status: str
    provider_sdk_runtime_dependency_added: bool = False
    provider_sdk_imported: bool = False
    provider_sdk_invoked: bool = False
    provider_sdk_network_called: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class DataExfiltrationBoundaryPolicy(ModelMixin):
    policy_id: str
    data_exfiltration_boundary_required: bool = True
    private_data_exfiltration_forbidden: bool = True
    credential_exfiltration_forbidden: bool = True
    raw_provider_output_exfiltration_forbidden: bool = True
    outbound_payload_minimization_required: bool = True
    outbound_payload_redaction_required: bool = True
    response_redaction_required: bool = True
    payload_audit_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class PayloadBoundaryPolicy(ModelMixin):
    policy_id: str
    payload_boundary_required: bool = True
    outbound_payload_must_be_minimal: bool = True
    outbound_payload_must_exclude_credentials: bool = True
    outbound_payload_must_exclude_private_data_by_default: bool = True
    outbound_payload_must_exclude_raw_traces: bool = True
    outbound_payload_must_exclude_raw_transcripts: bool = True
    outbound_payload_must_exclude_raw_provider_outputs: bool = True
    payload_preview_allowed: bool = True
    payload_preview_is_not_payload_send: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class RequestResponseRedactionBoundary(ModelMixin):
    boundary_id: str
    redaction_boundary_status: str
    request_redaction_required: bool = True
    response_redaction_required: bool = True
    redact_credentials: bool = True
    redact_private_identifiers: bool = True
    redact_raw_provider_outputs: bool = True
    raw_request_logging_forbidden: bool = True
    raw_response_logging_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class NetworkAuditBoundary(ModelMixin):
    boundary_id: str
    network_audit_required: bool = True
    request_candidate_audit_required: bool = True
    domain_decision_audit_required: bool = True
    payload_boundary_audit_required: bool = True
    timeout_retry_audit_required: bool = True
    network_call_audit_required_later: bool = True
    audit_must_not_include_credentials: bool = True
    audit_must_not_include_raw_payloads: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class CredentialNetworkBoundaryGate(ModelMixin):
    gate_id: str
    source_view_ref: dict[str, Any]
    credential_boundary_report_ref: dict[str, Any]
    network_boundary_policy_ref: dict[str, Any]
    outbound_domain_policy_ref: dict[str, Any]
    network_request_policy_ref: dict[str, Any]
    provider_sdk_boundary_report_refs: list[dict[str, Any]]
    data_exfiltration_policy_ref: dict[str, Any]
    payload_boundary_policy_ref: dict[str, Any]
    request_response_redaction_boundary_ref: dict[str, Any]
    network_audit_boundary_ref: dict[str, Any]
    credential_boundary_passed: bool
    secret_reference_boundary_passed: bool
    no_credential_value_present: bool
    no_credential_storage: bool
    no_credential_logging: bool
    no_env_file_created: bool
    network_boundary_passed: bool
    no_network_call: bool
    provider_sdk_boundary_passed: bool
    no_provider_sdk_invocation: bool
    outbound_domain_policy_complete: bool
    payload_boundary_complete: bool
    data_exfiltration_boundary_complete: bool
    audit_boundary_complete: bool
    gate_status: str
    ready_for_v0_29_5: bool
    ready_for_invocation_candidate: bool
    ready_for_dry_run_plan: bool
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class CredentialNetworkBoundaryAuditTrail(ModelMixin):
    audit_trail_id: str
    request_ref: dict[str, Any]
    source_view_ref: dict[str, Any]
    credential_boundary_report_ref: dict[str, Any]
    network_boundary_refs: list[dict[str, Any]]
    gate_ref: dict[str, Any]
    audit_event_count: int
    raw_content_included: bool = False
    credential_value_included: bool = False
    raw_payload_included: bool = False
    audit_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0294_VERSION


@dataclass
class CredentialNetworkBoundaryFinding(ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class CredentialNetworkBoundaryReport(ModelMixin):
    report_id: str
    created_at: str
    policy: CredentialSecretNetworkBoundaryPolicy
    request: CredentialNetworkBoundaryRequest
    source_view: CredentialNetworkBoundarySourceView
    credential_boundary_policy: CredentialBoundaryPolicy
    credential_material_classifications: list[CredentialMaterialClassification]
    secret_reference_policy: SecretReferencePolicy
    secret_reference_descriptors: list[SecretReferenceDescriptor]
    external_secret_store_contract: ExternalSecretStoreContract
    credential_redaction_policy: CredentialRedactionPolicy
    credential_audit_policy: CredentialAuditPolicy
    credential_scope_bindings: list[CredentialScopeBinding]
    credential_access_candidates: list[CredentialAccessCandidate]
    credential_boundary_report: CredentialBoundaryReport
    network_boundary_policy: NetworkBoundaryPolicy
    outbound_domain_policy: OutboundDomainPolicy
    outbound_domain_rules: list[OutboundDomainRule]
    network_request_policy: NetworkRequestPolicy
    network_request_candidates: list[NetworkRequestCandidate]
    timeout_retry_policy: NetworkTimeoutRetryPolicy
    provider_sdk_boundary_policy: ProviderSDKBoundaryPolicy
    provider_sdk_boundary_reports: list[ProviderSDKBoundaryReport]
    data_exfiltration_boundary_policy: DataExfiltrationBoundaryPolicy
    payload_boundary_policy: PayloadBoundaryPolicy
    request_response_redaction_boundary: RequestResponseRedactionBoundary
    network_audit_boundary: NetworkAuditBoundary
    credential_network_gate: CredentialNetworkBoundaryGate
    audit_trail: CredentialNetworkBoundaryAuditTrail
    findings: list[CredentialNetworkBoundaryFinding]
    report_status: str
    ready_for_v0_29_5: bool
    ready_for_invocation_candidate: bool
    ready_for_dry_run_plan: bool
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    credential_value_present: bool = False
    credential_stored: bool = False
    credential_logged: bool = False
    env_file_created: bool = False
    secret_retrieved: bool = False
    secret_materialized: bool = False
    provider_sdk_invoked: bool = False
    provider_invoked: bool = False
    network_called: bool = False
    outbound_request_sent: bool = False
    command_executed: bool = False
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
    next_required_step: str = V0294_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.29.5 Adapter Invocation Candidate / Dry-Run Plan begins or Credential / Secret / Network Boundary policy changes."
    version: str = V0294_VERSION


class CredentialNetworkBoundaryPrerequisiteSourceService:
    def __init__(self) -> None:
        self._permission_report: AdapterPermissionSafetyReport | None = None
        self._registry_report: AdapterRegistryReport | None = None

    def load_v0293_permission_safety_report(self) -> AdapterPermissionSafetyReport:
        if self._permission_report is None:
            self._permission_report = AdapterPermissionSafetyReportService().build_report()
        return self._permission_report

    def load_v0293_permission_safety_gate(self) -> Any:
        return self.load_v0293_permission_safety_report().permission_safety_gate

    def load_credential_reference_safety_checks(self) -> list[Any]:
        return self.load_v0293_permission_safety_report().credential_safety_checks

    def load_network_need_safety_checks(self) -> list[Any]:
        return self.load_v0293_permission_safety_report().network_safety_checks

    def load_permission_decision_records(self) -> list[Any]:
        return self.load_v0293_permission_safety_report().decision_records

    def load_safety_classifications(self) -> list[Any]:
        return self.load_v0293_permission_safety_report().safety_classifications

    def load_action_intents(self) -> list[Any]:
        return self.load_v0293_permission_safety_report().action_intents

    def load_action_scopes(self) -> list[Any]:
        return self.load_v0293_permission_safety_report().action_scopes

    def _registry(self) -> AdapterRegistryReport:
        if self._registry_report is None:
            self._registry_report = AdapterRegistryReportService().build_report()
        return self._registry_report

    def load_v0292_no_network_boundary_reports(self) -> list[dict[str, Any]]:
        report = self.load_v0293_permission_safety_report()
        return report.source_view.no_network_boundary_report_refs

    def load_v0292_provider_sdk_isolation_reports(self) -> list[dict[str, Any]]:
        report = self.load_v0293_permission_safety_report()
        return report.source_view.provider_sdk_isolation_report_refs

    def load_v0292_mock_credential_boundary_reports(self) -> list[dict[str, Any]]:
        report = self.load_v0293_permission_safety_report()
        return report.source_view.mock_credential_boundary_report_refs

    def load_v0291_credential_need_declarations(self) -> list[Any]:
        return self._registry().credential_need_declarations

    def load_v0291_network_need_declarations(self) -> list[Any]:
        return self._registry().network_need_declarations

    def load_v0291_adapter_risk_profiles(self) -> list[Any]:
        return self._registry().risk_profiles

    def load_v0290_credential_network_audit_contracts(self) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        return (
            _ref("adapter_credential_requirement_contract", "adapter_credential_requirement_contract:v0.29.0", "v0.29.0"),
            _ref("adapter_network_requirement_contract", "adapter_network_requirement_contract:v0.29.0", "v0.29.0"),
            _ref("adapter_audit_requirement_contract", "adapter_audit_requirement_contract:v0.29.0", "v0.29.0"),
        )

    def load_provider_invocation_prohibition_contract(self) -> dict[str, Any]:
        return _ref("provider_invocation_prohibition_contract", "provider_invocation_prohibition_contract:v0.29.0", "v0.29.0")

    def load_command_execution_prohibition_contract(self) -> dict[str, Any]:
        return _ref("command_execution_prohibition_contract", "command_execution_prohibition_contract:v0.29.0", "v0.29.0")


class CredentialSecretNetworkBoundaryPolicyService:
    def build_policy(self) -> CredentialSecretNetworkBoundaryPolicy:
        return CredentialSecretNetworkBoundaryPolicy("credential_secret_network_boundary_policy:v0.29.4")


class CredentialNetworkBoundarySourceViewService:
    def build_source_view(self) -> CredentialNetworkBoundarySourceView:
        source = CredentialNetworkBoundaryPrerequisiteSourceService()
        permission_report = source.load_v0293_permission_safety_report()
        registry_report = source._registry()
        credential_contract, network_contract, audit_contract = source.load_v0290_credential_network_audit_contracts()
        credential_checks = source.load_credential_reference_safety_checks()
        network_checks = source.load_network_need_safety_checks()
        return CredentialNetworkBoundarySourceView(
            "credential_network_boundary_source_view:v0.29.4",
            _ref("adapter_permission_safety_report", permission_report.report_id, "v0.29.3"),
            _ref("adapter_permission_safety_gate", permission_report.permission_safety_gate.gate_id, "v0.29.3"),
            _refs("credential_reference_safety_check", credential_checks, "check_id", "v0.29.3"),
            _refs("network_need_safety_check", network_checks, "check_id", "v0.29.3"),
            _refs("adapter_permission_decision_record", permission_report.decision_records, "decision_record_id", "v0.29.3"),
            _refs("adapter_safety_classification", permission_report.safety_classifications, "classification_id", "v0.29.3"),
            _refs("adapter_action_intent", permission_report.action_intents, "intent_id", "v0.29.3"),
            _refs("adapter_action_scope", permission_report.action_scopes, "scope_id", "v0.29.3"),
            source.load_v0292_no_network_boundary_reports(),
            source.load_v0292_provider_sdk_isolation_reports(),
            source.load_v0292_mock_credential_boundary_reports(),
            _refs("adapter_credential_need_declaration", registry_report.credential_need_declarations, "declaration_id", "v0.29.1"),
            _refs("adapter_network_need_declaration", registry_report.network_need_declarations, "declaration_id", "v0.29.1"),
            _refs("adapter_risk_profile", registry_report.risk_profiles, "risk_profile_id", "v0.29.1"),
            credential_contract,
            network_contract,
            audit_contract,
            source.load_provider_invocation_prohibition_contract(),
            source.load_command_execution_prohibition_contract(),
            "complete",
            any(check.credentials_required_later for check in credential_checks),
            any(check.network_required_later for check in network_checks),
        )


class CredentialNetworkBoundaryRequestService:
    def build_request(self, source_view: CredentialNetworkBoundarySourceView) -> CredentialNetworkBoundaryRequest:
        return CredentialNetworkBoundaryRequest(
            "credential_network_boundary_request:v0.29.4",
            source_view.permission_safety_report_ref["object_id"] if source_view.permission_safety_report_ref else None,
            "mock_adapter_harness_report:v0.29.2",
            "adapter_registry_report:v0.29.1",
            source_refs=[
                ref
                for ref in [
                    source_view.permission_safety_report_ref,
                    source_view.permission_safety_gate_ref,
                    source_view.credential_requirement_contract_ref,
                    source_view.network_requirement_contract_ref,
                ]
                if ref
            ],
        )


class CredentialBoundaryService:
    def build_credential_boundary_policy(self) -> CredentialBoundaryPolicy:
        return CredentialBoundaryPolicy("credential_boundary_policy:v0.29.4")

    def build_material_classifications(self, permission_report: AdapterPermissionSafetyReport) -> list[CredentialMaterialClassification]:
        classifications = []
        for intent in permission_report.action_intents:
            _provider_kind, credential_kind, credential_required, _network_required, sensitivity, status = _spec(intent.adapter_name)
            classifications.append(
                CredentialMaterialClassification(
                    f"credential_material_classification:{intent.adapter_name}:v0.29.4",
                    intent.adapter_name,
                    intent.capability_name,
                    credential_kind,
                    sensitivity,
                    credential_required,
                    credential_required,
                    status,
                )
            )
        return classifications

    def build_secret_reference_policy(self) -> SecretReferencePolicy:
        return SecretReferencePolicy("secret_reference_policy:v0.29.4")

    def build_secret_reference_descriptors(self, classifications: list[CredentialMaterialClassification]) -> list[SecretReferenceDescriptor]:
        descriptors = []
        for classification in classifications:
            status = "ready" if classification.secret_reference_required else "warning"
            descriptors.append(
                SecretReferenceDescriptor(
                    f"secret_reference_descriptor:{classification.adapter_name}:v0.29.4",
                    classification.adapter_name,
                    classification.capability_name,
                    f"{classification.adapter_name}:secret-ref-placeholder",
                    "enterprise_secret_ref" if classification.secret_reference_required else "placeholder",
                    classification.credential_kind if classification.secret_reference_required else None,
                    "Opaque future secret reference only; no credential value is present.",
                    status,
                )
            )
        return descriptors

    def build_external_secret_store_contract(self) -> ExternalSecretStoreContract:
        return ExternalSecretStoreContract("external_secret_store_contract:v0.29.4", list(SUPPORTED_FUTURE_STORE_KINDS), "warning")

    def build_credential_redaction_policy(self) -> CredentialRedactionPolicy:
        return CredentialRedactionPolicy("credential_redaction_policy:v0.29.4")

    def build_credential_audit_policy(self) -> CredentialAuditPolicy:
        return CredentialAuditPolicy("credential_audit_policy:v0.29.4")

    def build_credential_scope_bindings(
        self,
        permission_report: AdapterPermissionSafetyReport,
        classifications: list[CredentialMaterialClassification],
        descriptors: list[SecretReferenceDescriptor],
    ) -> list[CredentialScopeBinding]:
        scopes = {scope.adapter_name: scope for scope in permission_report.action_scopes}
        descriptors_by_adapter = {descriptor.adapter_name: descriptor for descriptor in descriptors}
        bindings = []
        for classification in classifications:
            scope = scopes.get(classification.adapter_name)
            descriptor = descriptors_by_adapter[classification.adapter_name]
            bindings.append(
                CredentialScopeBinding(
                    f"credential_scope_binding:{classification.adapter_name}:v0.29.4",
                    classification.adapter_name,
                    classification.capability_name,
                    _ref("adapter_action_scope", scope.scope_id, "v0.29.3") if scope else None,
                    _ref("credential_material_classification", classification.classification_id, V0294_VERSION),
                    _ref("secret_reference_descriptor", descriptor.descriptor_id, V0294_VERSION),
                    classification.secret_reference_required,
                    True,
                    True,
                )
            )
        return bindings

    def build_credential_access_candidates(
        self,
        bindings: list[CredentialScopeBinding],
        descriptors: list[SecretReferenceDescriptor],
    ) -> list[CredentialAccessCandidate]:
        descriptors_by_adapter = {descriptor.adapter_name: descriptor for descriptor in descriptors}
        candidates = []
        for binding in bindings:
            descriptor = descriptors_by_adapter[binding.adapter_name]
            candidates.append(
                CredentialAccessCandidate(
                    f"credential_access_candidate:{binding.adapter_name}:v0.29.4",
                    binding.adapter_name,
                    binding.capability_name,
                    _ref("credential_scope_binding", binding.binding_id, V0294_VERSION),
                    _ref("secret_reference_descriptor", descriptor.descriptor_id, V0294_VERSION),
                    "Credential access candidate is recorded for future approval only.",
                    "deferred" if binding.scope_bound_to_credential_ref else "denied",
                )
            )
        return candidates

    def build_credential_boundary_report(
        self,
        policy: CredentialBoundaryPolicy,
        classifications: list[CredentialMaterialClassification],
        secret_policy: SecretReferencePolicy,
        descriptors: list[SecretReferenceDescriptor],
        contract: ExternalSecretStoreContract,
        redaction: CredentialRedactionPolicy,
        audit: CredentialAuditPolicy,
        bindings: list[CredentialScopeBinding],
        candidates: list[CredentialAccessCandidate],
    ) -> CredentialBoundaryReport:
        return CredentialBoundaryReport(
            "credential_boundary_report:v0.29.4",
            _ref("credential_boundary_policy", policy.policy_id, V0294_VERSION),
            _refs("credential_material_classification", classifications, "classification_id", V0294_VERSION),
            _ref("secret_reference_policy", secret_policy.policy_id, V0294_VERSION),
            _refs("secret_reference_descriptor", descriptors, "descriptor_id", V0294_VERSION),
            _ref("external_secret_store_contract", contract.contract_id, V0294_VERSION),
            _ref("credential_redaction_policy", redaction.policy_id, V0294_VERSION),
            _ref("credential_audit_policy", audit.policy_id, V0294_VERSION),
            _refs("credential_scope_binding", bindings, "binding_id", V0294_VERSION),
            _refs("credential_access_candidate", candidates, "candidate_id", V0294_VERSION),
            "warning",
        )


class NetworkBoundaryService:
    def build_network_boundary_policy(self) -> NetworkBoundaryPolicy:
        return NetworkBoundaryPolicy("network_boundary_policy:v0.29.4")

    def build_outbound_domain_policy(self) -> OutboundDomainPolicy:
        return OutboundDomainPolicy("outbound_domain_policy:v0.29.4")

    def build_outbound_domain_rules(self, permission_report: AdapterPermissionSafetyReport) -> list[OutboundDomainRule]:
        rules = []
        for intent in permission_report.action_intents:
            provider_kind, _credential_kind, _credential_required, network_required, _sensitivity, status = _spec(intent.adapter_name)
            rules.append(
                OutboundDomainRule(
                    f"outbound_domain_rule:{intent.adapter_name}:v0.29.4",
                    intent.adapter_name,
                    provider_kind,
                    None,
                    "future_review" if network_required else "deny",
                    "warning" if network_required else status,
                )
            )
        return rules

    def build_network_request_policy(self) -> NetworkRequestPolicy:
        return NetworkRequestPolicy("network_request_policy:v0.29.4")

    def build_network_request_candidates(
        self,
        permission_report: AdapterPermissionSafetyReport,
        rules: list[OutboundDomainRule],
        payload_policy: "PayloadBoundaryPolicy",
        timeout_policy: "NetworkTimeoutRetryPolicy",
    ) -> list[NetworkRequestCandidate]:
        rules_by_adapter = {rule.adapter_name: rule for rule in rules}
        candidates = []
        for intent in permission_report.action_intents:
            provider_kind, _credential_kind, _credential_required, network_required, _sensitivity, _status = _spec(intent.adapter_name)
            rule = rules_by_adapter[intent.adapter_name]
            candidates.append(
                NetworkRequestCandidate(
                    f"network_request_candidate:{intent.adapter_name}:v0.29.4",
                    intent.adapter_name,
                    intent.capability_name,
                    provider_kind,
                    "POST" if network_required else None,
                    _ref("endpoint_candidate", f"endpoint_candidate:{intent.adapter_name}:v0.29.4", V0294_VERSION) if network_required else None,
                    _ref("outbound_domain_rule", rule.rule_id, V0294_VERSION),
                    _ref("payload_boundary_policy", payload_policy.policy_id, V0294_VERSION),
                    _ref("network_timeout_retry_policy", timeout_policy.policy_id, V0294_VERSION),
                    "Network request candidate is recorded without sending a request.",
                    "deferred" if network_required else "denied",
                )
            )
        return candidates

    def build_timeout_retry_policy(self) -> NetworkTimeoutRetryPolicy:
        return NetworkTimeoutRetryPolicy("network_timeout_retry_policy:v0.29.4")


class ProviderSDKBoundaryService:
    def build_policy(self) -> ProviderSDKBoundaryPolicy:
        return ProviderSDKBoundaryPolicy("provider_sdk_boundary_policy:v0.29.4")

    def build_reports(self, policy: ProviderSDKBoundaryPolicy, permission_report: AdapterPermissionSafetyReport) -> list[ProviderSDKBoundaryReport]:
        return [
            ProviderSDKBoundaryReport(
                f"provider_sdk_boundary_report:{intent.adapter_name}:v0.29.4",
                _ref("provider_sdk_boundary_policy", policy.policy_id, V0294_VERSION),
                intent.adapter_name,
                True,
                "passed",
            )
            for intent in permission_report.action_intents
        ]


class DataExfiltrationBoundaryService:
    def build_policy(self) -> DataExfiltrationBoundaryPolicy:
        return DataExfiltrationBoundaryPolicy("data_exfiltration_boundary_policy:v0.29.4")

    def build_payload_boundary_policy(self) -> PayloadBoundaryPolicy:
        return PayloadBoundaryPolicy("payload_boundary_policy:v0.29.4")

    def build_request_response_redaction_boundary(self) -> RequestResponseRedactionBoundary:
        return RequestResponseRedactionBoundary("request_response_redaction_boundary:v0.29.4", "ready")

    def build_network_audit_boundary(self) -> NetworkAuditBoundary:
        return NetworkAuditBoundary("network_audit_boundary:v0.29.4")


class CredentialNetworkBoundaryGateService:
    def evaluate_gate(
        self,
        source_view: CredentialNetworkBoundarySourceView,
        credential_report: CredentialBoundaryReport,
        network_policy: NetworkBoundaryPolicy,
        outbound_policy: OutboundDomainPolicy,
        request_policy: NetworkRequestPolicy,
        sdk_reports: list[ProviderSDKBoundaryReport],
        data_policy: DataExfiltrationBoundaryPolicy,
        payload_policy: PayloadBoundaryPolicy,
        redaction_boundary: RequestResponseRedactionBoundary,
        audit_boundary: NetworkAuditBoundary,
    ) -> CredentialNetworkBoundaryGate:
        no_sdk = all(not report.provider_sdk_imported and not report.provider_sdk_invoked and not report.provider_sdk_network_called for report in sdk_reports)
        ready = (
            not credential_report.credential_values_present
            and not credential_report.credential_stored
            and not credential_report.credential_logged
            and not credential_report.env_file_created
            and network_policy.no_network_default
            and no_sdk
            and payload_policy.outbound_payload_must_exclude_credentials
            and audit_boundary.audit_must_not_include_credentials
        )
        return CredentialNetworkBoundaryGate(
            "credential_network_boundary_gate:v0.29.4",
            _ref("credential_network_boundary_source_view", source_view.source_view_id, V0294_VERSION),
            _ref("credential_boundary_report", credential_report.report_id, V0294_VERSION),
            _ref("network_boundary_policy", network_policy.policy_id, V0294_VERSION),
            _ref("outbound_domain_policy", outbound_policy.policy_id, V0294_VERSION),
            _ref("network_request_policy", request_policy.policy_id, V0294_VERSION),
            _refs("provider_sdk_boundary_report", sdk_reports, "report_id", V0294_VERSION),
            _ref("data_exfiltration_boundary_policy", data_policy.policy_id, V0294_VERSION),
            _ref("payload_boundary_policy", payload_policy.policy_id, V0294_VERSION),
            _ref("request_response_redaction_boundary", redaction_boundary.boundary_id, V0294_VERSION),
            _ref("network_audit_boundary", audit_boundary.boundary_id, V0294_VERSION),
            True,
            True,
            not credential_report.credential_values_present,
            not credential_report.credential_stored,
            not credential_report.credential_logged,
            not credential_report.env_file_created,
            network_policy.no_network_default,
            True,
            no_sdk,
            no_sdk,
            outbound_policy.outbound_domain_policy_required,
            payload_policy.payload_boundary_required,
            data_policy.data_exfiltration_boundary_required,
            audit_boundary.network_audit_required,
            "warning",
            ready,
            ready,
            ready,
        )


class CredentialNetworkBoundaryAuditTrailService:
    def build_audit_trail(
        self,
        request: CredentialNetworkBoundaryRequest,
        source_view: CredentialNetworkBoundarySourceView,
        credential_report: CredentialBoundaryReport,
        gate: CredentialNetworkBoundaryGate,
        network_refs: list[dict[str, Any]],
    ) -> CredentialNetworkBoundaryAuditTrail:
        return CredentialNetworkBoundaryAuditTrail(
            "credential_network_boundary_audit_trail:v0.29.4",
            _ref("credential_network_boundary_request", request.request_id, V0294_VERSION),
            _ref("credential_network_boundary_source_view", source_view.source_view_id, V0294_VERSION),
            _ref("credential_boundary_report", credential_report.report_id, V0294_VERSION),
            network_refs,
            _ref("credential_network_boundary_gate", gate.gate_id, V0294_VERSION),
            5 + len(network_refs),
        )


class CredentialNetworkBoundaryFindingService:
    BLOCKED_FINDINGS = {
        "credential_value_detected",
        "credential_storage_attempted",
        "credential_logging_attempted",
        "env_file_creation_attempted",
        "secret_retrieval_attempted",
        "secret_materialization_attempted",
        "network_call_attempted",
        "provider_sdk_invocation_attempted",
        "provider_invocation_attempted",
        "outbound_request_attempted",
        "webhook_attempted",
        "websocket_attempted",
        "command_execution_attempted",
        "shell_true_detected",
        "unbounded_subprocess_detected",
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

    def build_findings(self) -> list[CredentialNetworkBoundaryFinding]:
        return [
            CredentialNetworkBoundaryFinding("credential_network_boundary_finding:policy:v0.29.4", "info", "credential_secret_network_policy_created", "Credential/secret/network boundary policy created without value access or network calls.", _ref("credential_secret_network_boundary_policy", "credential_secret_network_boundary_policy:v0.29.4", V0294_VERSION), [], None),
            CredentialNetworkBoundaryFinding("credential_network_boundary_finding:credential:v0.29.4", "info", "credential_boundary_report_created", "Credential boundary report created with no credential value present.", _ref("credential_boundary_report", "credential_boundary_report:v0.29.4", V0294_VERSION), [], "Withdraw if credential values are stored, logged, or materialized."),
            CredentialNetworkBoundaryFinding("credential_network_boundary_finding:gate:v0.29.4", "warning", "credential_network_gate_created", "Boundary gate is ready for v0.29.5 dry-run candidates only; provider/network/credential access remains false.", _ref("credential_network_boundary_gate", "credential_network_boundary_gate:v0.29.4", V0294_VERSION), [], "Withdraw if provider, network, credential, or command readiness becomes true."),
        ]


class CredentialNetworkBoundaryReportService:
    def build_report(self, report_id: str | None = None) -> CredentialNetworkBoundaryReport:
        source_service = CredentialNetworkBoundaryPrerequisiteSourceService()
        permission_report = source_service.load_v0293_permission_safety_report()
        policy = CredentialSecretNetworkBoundaryPolicyService().build_policy()
        source_view = CredentialNetworkBoundarySourceViewService().build_source_view()
        request = CredentialNetworkBoundaryRequestService().build_request(source_view)
        credential_service = CredentialBoundaryService()
        credential_policy = credential_service.build_credential_boundary_policy()
        classifications = credential_service.build_material_classifications(permission_report)
        secret_policy = credential_service.build_secret_reference_policy()
        descriptors = credential_service.build_secret_reference_descriptors(classifications)
        secret_store_contract = credential_service.build_external_secret_store_contract()
        redaction_policy = credential_service.build_credential_redaction_policy()
        credential_audit_policy = credential_service.build_credential_audit_policy()
        bindings = credential_service.build_credential_scope_bindings(permission_report, classifications, descriptors)
        credential_candidates = credential_service.build_credential_access_candidates(bindings, descriptors)
        credential_report = credential_service.build_credential_boundary_report(credential_policy, classifications, secret_policy, descriptors, secret_store_contract, redaction_policy, credential_audit_policy, bindings, credential_candidates)
        data_service = DataExfiltrationBoundaryService()
        data_policy = data_service.build_policy()
        payload_policy = data_service.build_payload_boundary_policy()
        request_response_redaction = data_service.build_request_response_redaction_boundary()
        network_audit = data_service.build_network_audit_boundary()
        network_service = NetworkBoundaryService()
        network_policy = network_service.build_network_boundary_policy()
        outbound_policy = network_service.build_outbound_domain_policy()
        outbound_rules = network_service.build_outbound_domain_rules(permission_report)
        request_policy = network_service.build_network_request_policy()
        timeout_policy = network_service.build_timeout_retry_policy()
        network_candidates = network_service.build_network_request_candidates(permission_report, outbound_rules, payload_policy, timeout_policy)
        sdk_service = ProviderSDKBoundaryService()
        sdk_policy = sdk_service.build_policy()
        sdk_reports = sdk_service.build_reports(sdk_policy, permission_report)
        gate = CredentialNetworkBoundaryGateService().evaluate_gate(source_view, credential_report, network_policy, outbound_policy, request_policy, sdk_reports, data_policy, payload_policy, request_response_redaction, network_audit)
        network_refs = [
            _ref("network_boundary_policy", network_policy.policy_id, V0294_VERSION),
            _ref("outbound_domain_policy", outbound_policy.policy_id, V0294_VERSION),
            _ref("network_request_policy", request_policy.policy_id, V0294_VERSION),
            _ref("network_timeout_retry_policy", timeout_policy.policy_id, V0294_VERSION),
        ]
        audit_trail = CredentialNetworkBoundaryAuditTrailService().build_audit_trail(request, source_view, credential_report, gate, network_refs)
        findings = CredentialNetworkBoundaryFindingService().build_findings()
        return CredentialNetworkBoundaryReport(
            report_id or "credential_network_boundary_report:v0.29.4",
            _now(),
            policy,
            request,
            source_view,
            credential_policy,
            classifications,
            secret_policy,
            descriptors,
            secret_store_contract,
            redaction_policy,
            credential_audit_policy,
            bindings,
            credential_candidates,
            credential_report,
            network_policy,
            outbound_policy,
            outbound_rules,
            request_policy,
            network_candidates,
            timeout_policy,
            sdk_policy,
            sdk_reports,
            data_policy,
            payload_policy,
            request_response_redaction,
            network_audit,
            gate,
            audit_trail,
            findings,
            "warning",
            gate.ready_for_v0_29_5,
            gate.ready_for_invocation_candidate,
            gate.ready_for_dry_run_plan,
            limitations=["v0.29.4 defines credential, secret, and network boundaries only. Dry-run plans, approval/audit/rollback, certification, and limited invocation remain future work."],
            withdrawal_conditions=["Withdraw if credential values, secret retrieval, network calls, provider SDK/provider invocation, command execution, live adapters, private/raw data, or LLM-judge-only authority appear."],
        )

    def build_all_parts(self, report_id: str | None = None) -> dict[str, Any]:
        report = self.build_report(report_id=report_id)
        return {
            "policy": report.policy,
            "request": report.request,
            "source-view": report.source_view,
            "credentials": report.credential_boundary_report,
            "credential-classification": report.credential_material_classifications,
            "secret-policy": report.secret_reference_policy,
            "secret-refs": report.secret_reference_descriptors,
            "secret-store-contract": report.external_secret_store_contract,
            "credential-redaction": report.credential_redaction_policy,
            "credential-audit": report.credential_audit_policy,
            "credential-scope": report.credential_scope_bindings,
            "credential-candidates": report.credential_access_candidates,
            "network": report.network_boundary_policy,
            "outbound-domains": report.outbound_domain_rules,
            "network-requests": report.network_request_candidates,
            "timeout-retry": report.timeout_retry_policy,
            "provider-sdk": report.provider_sdk_boundary_reports,
            "exfiltration": report.data_exfiltration_boundary_policy,
            "payload": report.payload_boundary_policy,
            "redaction": report.request_response_redaction_boundary,
            "network-audit": report.network_audit_boundary,
            "gate": report.credential_network_gate,
            "audit": report.audit_trail,
            "findings": report.findings,
            "report": report,
        }

    def build_pig_report(self) -> dict[str, Any]:
        report = self.build_report()
        return {
            "version": V0294_VERSION,
            "layer": V0294_LAYER,
            "subject": "credential_secret_network_boundary",
            "principles": [
                "Credential boundary is not credential storage",
                "Secret reference is not secret value",
                "Credential access candidate is not credential access",
                "External secret store contract is not secret-store integration",
                "Network boundary is not network access",
                "Outbound domain policy is not network call",
                "Network request candidate is not network request",
                "Timeout/retry policy is not network execution",
                "Data exfiltration boundary is not data exfiltration",
                "No-network remains the default",
                "No-credential-value remains the default",
            ],
            "safety_boundary": {
                "credential_value_present": report.credential_value_present,
                "credential_stored": report.credential_stored,
                "credential_logged": report.credential_logged,
                "env_file_created": report.env_file_created,
                "secret_retrieved": report.secret_retrieved,
                "secret_materialized": report.secret_materialized,
                "provider_sdk_invoked": report.provider_sdk_invoked,
                "provider_invoked": report.provider_invoked,
                "network_called": report.network_called,
                "outbound_request_sent": report.outbound_request_sent,
                "command_executed": report.command_executed,
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
                "v0.29.5 Adapter Invocation Candidate / Dry-Run Plan",
                "v0.29.6 Provider Invocation Approval / Audit / Rollback Boundary",
                "v0.29.7 External Skill Packaging / Certification Matrix",
                "v0.29.8 Limited Provider Invocation Preview Gate",
                "v0.29.9 External Provider Adapter Foundation Consolidation",
            ],
            "next_step": V0294_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "credential_secret_network_boundary_created",
            "version": V0294_VERSION,
            "source_read_models": [
                "AdapterPermissionSafetyGateState",
                "AdapterScopeMatrixState",
                "AdapterPermissionDecisionRecordState",
                "AdapterSafetyClassificationState",
                "CredentialReferenceSafetyCheckState",
                "NetworkNeedSafetyCheckState",
                "MockCredentialBoundaryState",
                "NoNetworkBoundaryState",
                "ProviderSDKIsolationState",
                "AdapterCredentialNeedDeclarationState",
                "AdapterNetworkNeedDeclarationState",
                "AdapterRiskProfileState",
                "AdapterCredentialRequirementContractState",
                "AdapterNetworkRequirementContractState",
                "AdapterAuditRequirementContractState",
                "ProviderInvocationProhibitionState",
                "CommandExecutionProhibitionState",
                "PigGuidanceState",
                "OCPXProjectionState",
            ],
            "target_read_models": [
                "CredentialBoundaryState",
                "SecretReferenceBoundaryState",
                "ExternalSecretStoreContractState",
                "CredentialRedactionPolicyState",
                "CredentialAuditPolicyState",
                "CredentialAccessCandidateState",
                "NetworkBoundaryState",
                "OutboundDomainPolicyState",
                "NetworkRequestCandidateState",
                "ProviderSDKBoundaryState",
                "DataExfiltrationBoundaryState",
                "PayloadBoundaryState",
                "CredentialNetworkBoundaryGateState",
                "V029ReadinessState",
            ],
            "effect_types": V0294_EFFECT_TYPES,
            "forbidden_effect_types": V0294_FORBIDDEN_EFFECT_TYPES,
        }


def render_credential_network_boundary_cli(parts: dict[str, Any], section: str = "report") -> str:
    report: CredentialNetworkBoundaryReport = parts["report"]
    lines = [
        f"Credential / Secret / Network Boundary {section}",
        f"version={report.version}",
        f"layer={report.policy.layer}",
        f"report_status={report.report_status}",
        f"ready_for_v0_29_5={_bool(report.ready_for_v0_29_5)}",
        f"ready_for_invocation_candidate={_bool(report.ready_for_invocation_candidate)}",
        f"ready_for_dry_run_plan={_bool(report.ready_for_dry_run_plan)}",
        f"ready_for_provider_invocation={_bool(report.ready_for_provider_invocation)}",
        f"ready_for_network_access={_bool(report.ready_for_network_access)}",
        f"ready_for_credential_access={_bool(report.ready_for_credential_access)}",
        f"ready_for_command_execution={_bool(report.ready_for_command_execution)}",
        f"credential_value_present={_bool(report.credential_value_present)}",
        f"credential_stored={_bool(report.credential_stored)}",
        f"credential_logged={_bool(report.credential_logged)}",
        f"env_file_created={_bool(report.env_file_created)}",
        f"secret_retrieved={_bool(report.secret_retrieved)}",
        f"secret_materialized={_bool(report.secret_materialized)}",
        f"provider_sdk_invoked={_bool(report.provider_sdk_invoked)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"network_called={_bool(report.network_called)}",
        f"outbound_request_sent={_bool(report.outbound_request_sent)}",
        f"command_executed={_bool(report.command_executed)}",
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
