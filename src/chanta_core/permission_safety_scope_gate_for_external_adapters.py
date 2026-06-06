from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.external_provider_adapter_contract import ModelMixin, _bool, _ref
from chanta_core.mock_adapter_harness_no_network_default import (
    MockAdapterHarnessReport,
    MockAdapterHarnessReportService,
)
from chanta_core.provider_capability_inventory_adapter_registry import (
    AdapterRegistryReport,
    AdapterRegistryReportService,
)
from chanta_core.utility.time import utc_now_iso


V0293_VERSION = "v0.29.3"
V0293_LAYER = "external_provider_adapter"
V0293_TRACK = "External Skill / External Provider Adapter Development"
V0293_NAME = "Permission / Safety / Scope Gate for External Adapters"
V0293_KOREAN_NAME = "External Adapter 권한·안전·범위 게이트"
V0293_NEXT_STEP = "v0.29.4 Credential / Secret / Network Boundary"

V0293_OBJECT_TYPES = [
    "external_adapter_permission_safety_policy",
    "adapter_permission_safety_request",
    "adapter_permission_safety_source_view",
    "adapter_permission_policy",
    "adapter_safety_policy",
    "adapter_scope_policy",
    "adapter_deny_first_rule_set",
    "adapter_action_intent",
    "adapter_action_scope",
    "adapter_scope_matrix",
    "adapter_scope_matrix_row",
    "adapter_permission_scope_evaluation",
    "adapter_safety_classification",
    "adapter_safety_finding",
    "user_approval_requirement",
    "adapter_approval_candidate",
    "adapter_permission_decision_candidate",
    "adapter_permission_decision_record",
    "adapter_scope_expiry_policy",
    "private_data_safety_check",
    "credential_reference_safety_check",
    "network_need_safety_check",
    "command_like_action_safety_check",
    "external_side_effect_safety_check",
    "data_exfiltration_safety_check",
    "rpa_scope_deferral_check",
    "adapter_permission_safety_gate",
    "adapter_permission_safety_audit_trail",
    "adapter_permission_safety_finding",
    "adapter_permission_safety_report",
    "mock_adapter_harness_report",
    "adapter_registry_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

V0293_EVENT_TYPES = [
    "adapter_permission_safety_requested",
    "adapter_permission_safety_prerequisites_loaded",
    "external_adapter_permission_safety_policy_created",
    "adapter_permission_policy_created",
    "adapter_safety_policy_created",
    "adapter_scope_policy_created",
    "adapter_deny_first_rule_set_created",
    "adapter_action_intent_created",
    "adapter_action_scope_created",
    "adapter_scope_matrix_created",
    "adapter_permission_scope_evaluation_created",
    "adapter_safety_classification_created",
    "adapter_safety_finding_created",
    "user_approval_requirement_created",
    "adapter_approval_candidate_created",
    "adapter_permission_decision_candidate_created",
    "adapter_permission_decision_record_created",
    "adapter_scope_expiry_policy_created",
    "private_data_safety_check_created",
    "credential_reference_safety_check_created",
    "network_need_safety_check_created",
    "command_like_action_safety_check_created",
    "external_side_effect_safety_check_created",
    "data_exfiltration_safety_check_created",
    "rpa_scope_deferral_check_created",
    "adapter_permission_safety_gate_evaluated",
    "adapter_permission_safety_audit_trail_created",
    "adapter_permission_safety_report_created",
    "adapter_permission_safety_warning_created",
    "adapter_permission_safety_blocked",
]

V0293_EFFECT_TYPES = [
    "read_only_observation",
    "adapter_permission_safety_policy_created",
    "adapter_scope_matrix_created",
    "adapter_safety_classification_created",
    "adapter_permission_decision_record_created",
    "adapter_approval_candidate_created",
    "adapter_safety_check_created",
    "adapter_permission_safety_gate_evaluated",
    "adapter_permission_safety_audit_trail_created",
    "state_candidate_created",
]

V0293_FORBIDDEN_EFFECT_TYPES = [
    "real_permission_granted",
    "approval_granted",
    "provider_registered",
    "provider_invoked",
    "provider_sdk_invoked",
    "network_called",
    "credential_stored",
    "credential_logged",
    "env_file_created",
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
    "references_runtime_dependency_added",
    "references_code_copied",
    "PIG_execution_authority_enabled",
    "llm_judge_used",
]

ALLOWED_PERMISSION_DECISIONS = [
    "deny",
    "defer",
    "require_user_approval",
    "require_future_credential_boundary",
    "require_future_network_boundary",
    "mock_only",
    "dry_run_only",
    "no_op",
]

DENY_FIRST_RULES = [
    "deny_if_provider_invocation_required_now",
    "deny_if_network_required_now",
    "deny_if_credential_value_required_now",
    "deny_if_command_execution_required_now",
    "deny_if_private_data_required_now",
    "deny_if_raw_provider_output_persistence_required",
    "deny_if_rpa_action_required_now",
    "deny_if_external_dominion_required_now",
    "deny_if_missing_scope",
    "deny_if_missing_safety_classification",
]

ACTION_BLUEPRINTS = {
    "internal_mock_adapter": {
        "provider_kind": "internal_mock_provider",
        "capability_name": "internal_mock_adapter_capability",
        "action_kind": "mock_action",
        "scope_kind": "mock_only",
        "safety_class": "safe_mock_only",
        "risk_level": "none",
        "decision": "mock_only",
        "matrix_status": "mock_only",
        "approval_required": False,
        "action_allowed_now": True,
        "requires_provider_invocation": False,
        "requires_network": False,
        "requires_credentials": False,
        "requires_command_execution": False,
        "requires_private_data": False,
        "requires_raw_provider_output_persistence": False,
        "required_permission_scope": "none",
        "future_version": None,
    },
    "generic_llm_adapter": {
        "provider_kind": "llm_provider",
        "capability_name": "generic_llm_adapter_capability",
        "action_kind": "external_read",
        "scope_kind": "future_external_read",
        "safety_class": "blocked_credential_sensitive",
        "risk_level": "blocked",
        "decision": "require_future_credential_boundary",
        "matrix_status": "deferred",
        "approval_required": True,
        "action_allowed_now": False,
        "requires_provider_invocation": True,
        "requires_network": True,
        "requires_credentials": True,
        "requires_command_execution": False,
        "requires_private_data": False,
        "requires_raw_provider_output_persistence": False,
        "required_permission_scope": "read_only",
        "future_version": "v0.29.4",
    },
    "generic_search_adapter": {
        "provider_kind": "search_provider",
        "capability_name": "generic_search_adapter_capability",
        "action_kind": "external_read",
        "scope_kind": "future_external_read",
        "safety_class": "blocked_network_required",
        "risk_level": "blocked",
        "decision": "require_future_network_boundary",
        "matrix_status": "deferred",
        "approval_required": True,
        "action_allowed_now": False,
        "requires_provider_invocation": True,
        "requires_network": True,
        "requires_credentials": False,
        "requires_command_execution": False,
        "requires_private_data": False,
        "requires_raw_provider_output_persistence": False,
        "required_permission_scope": "read_only",
        "future_version": "v0.29.4",
    },
    "generic_workflow_adapter": {
        "provider_kind": "workflow_provider",
        "capability_name": "generic_workflow_adapter_capability",
        "action_kind": "external_side_effect",
        "scope_kind": "future_external_side_effect",
        "safety_class": "blocked_external_side_effect",
        "risk_level": "blocked",
        "decision": "defer",
        "matrix_status": "deferred",
        "approval_required": True,
        "action_allowed_now": False,
        "requires_provider_invocation": True,
        "requires_network": True,
        "requires_credentials": True,
        "requires_command_execution": False,
        "requires_private_data": False,
        "requires_raw_provider_output_persistence": False,
        "required_permission_scope": "external_side_effect",
        "future_version": "v0.29.6",
    },
    "generic_rpa_adapter": {
        "provider_kind": "rpa_provider",
        "capability_name": "generic_rpa_adapter_capability",
        "action_kind": "rpa_action",
        "scope_kind": "rpa_deferred",
        "safety_class": "blocked_rpa_future_track",
        "risk_level": "blocked",
        "decision": "defer",
        "matrix_status": "deferred",
        "approval_required": True,
        "action_allowed_now": False,
        "requires_provider_invocation": True,
        "requires_network": True,
        "requires_credentials": True,
        "requires_command_execution": True,
        "requires_private_data": False,
        "requires_raw_provider_output_persistence": False,
        "required_permission_scope": "rpa_action",
        "future_version": "v0.29.7_or_later_certification_and_v0.29.8_preview_gate",
    },
}


def _now() -> str:
    return utc_now_iso()


def _blueprint(adapter_name: str) -> dict[str, Any]:
    return ACTION_BLUEPRINTS.get(
        adapter_name,
        {
            "provider_kind": "unknown",
            "capability_name": f"{adapter_name}_capability",
            "action_kind": "unknown",
            "scope_kind": "unknown",
            "safety_class": "unknown",
            "risk_level": "unknown",
            "decision": "deny",
            "matrix_status": "unknown",
            "approval_required": True,
            "action_allowed_now": False,
            "requires_provider_invocation": True,
            "requires_network": True,
            "requires_credentials": True,
            "requires_command_execution": False,
            "requires_private_data": False,
            "requires_raw_provider_output_persistence": False,
            "required_permission_scope": "unknown",
            "future_version": None,
        },
    )


def _adapter_names(mock_report: MockAdapterHarnessReport) -> list[str]:
    names = [contract.mock_adapter_name for contract in mock_report.mock_provider_adapter_contracts]
    return names or list(ACTION_BLUEPRINTS)


def _refs(object_type: str, items: list[Any], attr: str, version: str) -> list[dict[str, Any]]:
    return [_ref(object_type, getattr(item, attr), version) for item in items]


@dataclass
class ExternalAdapterPermissionSafetyPolicy(ModelMixin):
    policy_id: str
    permission_safety_gate_enabled: bool = True
    deny_first_required: bool = True
    scoped_permission_required: bool = True
    permission_expiry_required: bool = True
    user_approval_requirement_enabled: bool = True
    permission_decision_record_required: bool = True
    safety_classification_required: bool = True
    private_data_check_required: bool = True
    credential_sensitivity_check_required: bool = True
    network_sensitivity_check_required: bool = True
    external_side_effect_check_required: bool = True
    data_exfiltration_check_required: bool = True
    command_like_action_forbidden_now: bool = True
    rpa_action_deferred: bool = True
    approval_candidate_is_not_execution: bool = True
    permission_gate_is_not_permission_grant: bool = True
    safety_gate_is_not_invocation: bool = True
    real_permission_grant_enabled_now: bool = False
    provider_registration_enabled_now: bool = False
    provider_invocation_enabled_now: bool = False
    network_access_enabled_now: bool = False
    credential_storage_enabled_now: bool = False
    command_execution_expansion_enabled_now: bool = False
    live_adapter_implementation_enabled_now: bool = False
    rpa_adapter_enabled_now: bool = False
    external_agent_dominion_enabled_now: bool = False
    schumpeter_private_runtime_enabled_now: bool = False
    PIG_execution_authority_forbidden: bool = True
    llm_judge_as_sole_permission_safety_authority_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION
    layer: str = V0293_LAYER


@dataclass
class AdapterPermissionSafetyRequest(ModelMixin):
    request_id: str
    mock_harness_report_id: str | None
    adapter_registry_report_id: str | None
    requested_gate_scope: str = "full_permission_safety_scope_gate"
    strictness: str = "standard"
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class AdapterPermissionSafetySourceView(ModelMixin):
    source_view_id: str
    mock_harness_report_ref: dict[str, Any] | None
    mock_harness_gate_ref: dict[str, Any] | None
    mock_run_report_refs: list[dict[str, Any]]
    mock_effect_boundary_validation_refs: list[dict[str, Any]]
    no_network_boundary_report_refs: list[dict[str, Any]]
    provider_sdk_isolation_report_refs: list[dict[str, Any]]
    mock_credential_boundary_report_refs: list[dict[str, Any]]
    mock_adapter_ocel_trace_report_refs: list[dict[str, Any]]
    adapter_registry_report_ref: dict[str, Any] | None
    adapter_registry_ref: dict[str, Any] | None
    adapter_capability_declaration_refs: list[dict[str, Any]]
    adapter_risk_profile_refs: list[dict[str, Any]]
    permission_scope_requirement_refs: list[dict[str, Any]]
    safety_scope_requirement_refs: list[dict[str, Any]]
    credential_need_declaration_refs: list[dict[str, Any]]
    network_need_declaration_refs: list[dict[str, Any]]
    provider_invocation_prohibition_ref: dict[str, Any] | None
    command_execution_prohibition_ref: dict[str, Any] | None
    source_status: str
    mock_harness_ready_for_permission_safety: bool | None
    provider_invocation_detected: bool = False
    network_call_detected: bool = False
    command_execution_detected: bool = False
    credential_value_detected: bool = False
    live_adapter_detected: bool = False
    private_data_detected: bool = False
    raw_provider_output_detected: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class AdapterPermissionPolicy(ModelMixin):
    policy_id: str
    deny_first_default: bool = True
    permission_required_for_external_action: bool = True
    permission_scope_required: bool = True
    permission_expiry_required: bool = True
    approval_record_required: bool = True
    permission_restoration_without_approval_forbidden: bool = True
    ambient_permission_forbidden: bool = True
    wildcard_permission_forbidden: bool = True
    permission_grant_enabled_now: bool = False
    permission_grant_candidate_enabled: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class AdapterSafetyPolicy(ModelMixin):
    policy_id: str
    safety_classification_required: bool = True
    safety_gate_required_for_external_action: bool = True
    private_data_safety_check_required: bool = True
    credential_safety_check_required: bool = True
    network_safety_check_required: bool = True
    external_side_effect_check_required: bool = True
    data_exfiltration_check_required: bool = True
    command_like_action_forbidden_now: bool = True
    rpa_action_future_track: bool = True
    unsafe_action_blocks_approval_candidate: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class AdapterScopePolicy(ModelMixin):
    policy_id: str
    scope_required: bool = True
    scope_must_be_minimal: bool = True
    scope_must_be_expiring: bool = True
    scope_must_be_action_specific: bool = True
    scope_must_reference_adapter_and_capability: bool = True
    broad_external_scope_forbidden: bool = True
    wildcard_scope_forbidden: bool = True
    private_data_scope_requires_future_boundary: bool = True
    credential_scope_requires_v0294: bool = True
    network_scope_requires_v0294: bool = True
    command_scope_forbidden_now: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class AdapterDenyFirstRuleSet(ModelMixin):
    rule_set_id: str
    deny_first_enabled: bool = True
    default_decision: str = "deny"
    allowed_decisions: list[str] = field(default_factory=lambda: list(ALLOWED_PERMISSION_DECISIONS))
    deny_rules: list[str] = field(default_factory=lambda: list(DENY_FIRST_RULES))
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class AdapterActionIntent(ModelMixin):
    intent_id: str
    adapter_name: str
    provider_kind: str
    capability_name: str
    intended_action: str
    intent_summary: str
    action_kind: str
    requires_provider_invocation: bool
    requires_network: bool
    requires_credentials: bool
    requires_command_execution: bool
    requires_private_data: bool
    requires_raw_provider_output_persistence: bool
    action_allowed_now: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class AdapterActionScope(ModelMixin):
    scope_id: str
    adapter_name: str
    capability_name: str
    action_intent_ref: dict[str, Any]
    scope_kind: str
    scope_summary: str
    scope_minimal: bool
    scope_expiring_required: bool
    scope_grant_allowed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class AdapterScopeMatrixRow(ModelMixin):
    row_id: str
    adapter_name: str
    capability_name: str
    action_scope_ref: dict[str, Any]
    permission_scope_required: bool
    safety_scope_required: bool
    approval_required: bool
    defer_to_v0294: bool
    defer_to_v0295: bool
    defer_to_v0296: bool
    defer_to_v0298: bool
    scope_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class AdapterScopeMatrix(ModelMixin):
    matrix_id: str
    rows: list[AdapterScopeMatrixRow]
    adapter_count: int
    safe_mock_only_count: int
    approval_required_count: int
    denied_count: int
    deferred_count: int
    unknown_count: int
    matrix_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class AdapterPermissionScopeEvaluation(ModelMixin):
    evaluation_id: str
    adapter_name: str
    capability_name: str
    action_scope_ref: dict[str, Any]
    required_permission_scope: str | None
    scope_is_minimal: bool | None
    scope_expiry_required: bool
    approval_record_required: bool
    permission_grant_candidate_allowed: bool
    real_permission_granted_now: bool = False
    evaluation_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class AdapterSafetyClassification(ModelMixin):
    classification_id: str
    adapter_name: str
    capability_name: str
    action_intent_ref: dict[str, Any]
    safety_class: str
    risk_level: str
    blocks_permission_candidate: bool
    requires_user_approval: bool
    requires_future_credential_boundary: bool
    requires_future_network_boundary: bool
    requires_future_audit_rollback: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class AdapterSafetyFinding(ModelMixin):
    safety_finding_id: str
    adapter_name: str
    capability_name: str
    finding_type: str
    severity: str
    blocks_gate: bool
    finding_summary: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class UserApprovalRequirement(ModelMixin):
    requirement_id: str
    adapter_name: str
    capability_name: str
    action_scope_ref: dict[str, Any]
    approval_required: bool
    approval_reason: str
    approval_surface_required: bool = True
    approval_record_required: bool = True
    approval_expiry_required: bool = True
    approval_scope_summary_required: bool = True
    approval_is_execution: bool = False
    approval_granted_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class AdapterApprovalCandidate(ModelMixin):
    approval_candidate_id: str
    adapter_name: str
    capability_name: str
    action_intent_ref: dict[str, Any]
    permission_scope_evaluation_ref: dict[str, Any]
    safety_classification_ref: dict[str, Any]
    approval_requirement_ref: dict[str, Any]
    candidate_status: str
    candidate_summary: str
    approval_candidate_is_permission_grant: bool = False
    approval_candidate_is_execution: bool = False
    provider_invoked_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class AdapterPermissionDecisionCandidate(ModelMixin):
    decision_candidate_id: str
    adapter_name: str
    capability_name: str
    proposed_decision: str
    decision_reason: str
    required_future_version: str | None
    candidate_ref: dict[str, Any] | None
    permission_granted_now: bool = False
    provider_invoked_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class AdapterPermissionDecisionRecord(ModelMixin):
    decision_record_id: str
    adapter_name: str
    capability_name: str
    decision_candidate_ref: dict[str, Any]
    final_decision: str
    decision_reason: str
    decision_recorded_at: str | None
    permission_granted_now: bool = False
    approval_granted_now: bool = False
    provider_invoked_now: bool = False
    network_called_now: bool = False
    command_executed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class AdapterScopeExpiryPolicy(ModelMixin):
    policy_id: str
    scope_expiry_required: bool = True
    default_expiry_required: bool = True
    permanent_permission_forbidden: bool = True
    silent_permission_restoration_forbidden: bool = True
    expired_permission_must_require_reapproval: bool = True
    expiry_policy_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class PrivateDataSafetyCheck(ModelMixin):
    check_id: str
    adapter_name: str
    capability_name: str
    private_data_required: bool
    private_data_detected: bool
    actual_user_data_detected: bool
    actual_company_data_detected: bool
    private_data_blocks_now: bool
    check_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class CredentialReferenceSafetyCheck(ModelMixin):
    check_id: str
    adapter_name: str
    capability_name: str
    credentials_required_later: bool
    credential_value_required_now: bool
    credential_value_detected: bool
    credential_storage_detected: bool
    credential_logging_detected: bool
    credential_boundary_future_version: str
    credential_sensitivity_blocks_now: bool
    check_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class NetworkNeedSafetyCheck(ModelMixin):
    check_id: str
    adapter_name: str
    capability_name: str
    network_required_later: bool
    network_required_now: bool
    network_called_now: bool
    provider_sdk_network_detected: bool
    network_boundary_future_version: str
    network_sensitivity_blocks_now: bool
    check_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class CommandLikeActionSafetyCheck(ModelMixin):
    check_id: str
    adapter_name: str
    capability_name: str
    command_like_action: bool
    command_execution_required: bool
    command_executed_now: bool
    shell_true_detected: bool
    unbounded_subprocess_detected: bool
    command_like_action_blocks_now: bool
    check_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class ExternalSideEffectSafetyCheck(ModelMixin):
    check_id: str
    adapter_name: str
    capability_name: str
    external_side_effect_possible: bool
    external_side_effect_performed_now: bool
    requires_future_approval_audit_rollback: bool
    future_gate_version: str
    side_effect_blocks_now: bool
    check_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class DataExfiltrationSafetyCheck(ModelMixin):
    check_id: str
    adapter_name: str
    capability_name: str
    data_exfiltration_risk: str
    private_data_exfiltrated_now: bool
    raw_provider_output_persisted_now: bool
    exfiltration_blocks_now: bool
    check_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class RPAScopeDeferralCheck(ModelMixin):
    check_id: str
    adapter_name: str
    capability_name: str
    rpa_action: bool
    A360_related: bool
    Brity_related: bool
    UiPath_related: bool
    rpa_adapter_implemented_now: bool
    rpa_action_deferred: bool
    required_future_gate: str
    check_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class AdapterPermissionSafetyGate(ModelMixin):
    gate_id: str
    source_view_ref: dict[str, Any]
    scope_matrix_ref: dict[str, Any]
    deny_first_rule_set_ref: dict[str, Any]
    permission_scope_evaluation_refs: list[dict[str, Any]]
    safety_classification_refs: list[dict[str, Any]]
    approval_candidate_refs: list[dict[str, Any]]
    decision_record_refs: list[dict[str, Any]]
    private_data_check_refs: list[dict[str, Any]]
    credential_safety_check_refs: list[dict[str, Any]]
    network_safety_check_refs: list[dict[str, Any]]
    command_like_check_refs: list[dict[str, Any]]
    external_side_effect_check_refs: list[dict[str, Any]]
    data_exfiltration_check_refs: list[dict[str, Any]]
    rpa_deferral_check_refs: list[dict[str, Any]]
    deny_first_passed: bool
    scope_evaluation_complete: bool
    safety_classification_complete: bool
    approval_requirements_complete: bool
    private_data_checks_passed: bool
    credential_checks_passed_or_deferred: bool
    network_checks_passed_or_deferred: bool
    command_like_actions_blocked: bool
    external_side_effects_deferred: bool
    rpa_actions_deferred: bool
    no_permission_granted: bool
    no_provider_invocation: bool
    no_network_call: bool
    no_credential_storage: bool
    no_command_execution: bool
    gate_status: str
    ready_for_v0_29_4: bool
    ready_for_credential_network_boundary: bool
    ready_for_invocation_candidate: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_command_execution: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class AdapterPermissionSafetyAuditTrail(ModelMixin):
    audit_trail_id: str
    request_ref: dict[str, Any]
    source_view_ref: dict[str, Any]
    gate_ref: dict[str, Any]
    policy_refs: list[dict[str, Any]]
    decision_record_refs: list[dict[str, Any]]
    safety_check_refs: list[dict[str, Any]]
    audit_event_count: int
    raw_content_included: bool = False
    audit_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0293_VERSION


@dataclass
class AdapterPermissionSafetyFinding(ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class AdapterPermissionSafetyReport(ModelMixin):
    report_id: str
    created_at: str
    policy: ExternalAdapterPermissionSafetyPolicy
    request: AdapterPermissionSafetyRequest
    source_view: AdapterPermissionSafetySourceView
    permission_policy: AdapterPermissionPolicy
    safety_policy: AdapterSafetyPolicy
    scope_policy: AdapterScopePolicy
    deny_first_rule_set: AdapterDenyFirstRuleSet
    action_intents: list[AdapterActionIntent]
    action_scopes: list[AdapterActionScope]
    scope_matrix: AdapterScopeMatrix
    permission_scope_evaluations: list[AdapterPermissionScopeEvaluation]
    safety_classifications: list[AdapterSafetyClassification]
    safety_findings: list[AdapterSafetyFinding]
    approval_requirements: list[UserApprovalRequirement]
    approval_candidates: list[AdapterApprovalCandidate]
    decision_candidates: list[AdapterPermissionDecisionCandidate]
    decision_records: list[AdapterPermissionDecisionRecord]
    scope_expiry_policy: AdapterScopeExpiryPolicy
    private_data_safety_checks: list[PrivateDataSafetyCheck]
    credential_safety_checks: list[CredentialReferenceSafetyCheck]
    network_safety_checks: list[NetworkNeedSafetyCheck]
    command_like_action_checks: list[CommandLikeActionSafetyCheck]
    external_side_effect_checks: list[ExternalSideEffectSafetyCheck]
    data_exfiltration_checks: list[DataExfiltrationSafetyCheck]
    rpa_deferral_checks: list[RPAScopeDeferralCheck]
    permission_safety_gate: AdapterPermissionSafetyGate
    audit_trail: AdapterPermissionSafetyAuditTrail
    findings: list[AdapterPermissionSafetyFinding]
    report_status: str
    ready_for_v0_29_4: bool
    ready_for_credential_network_boundary: bool
    ready_for_invocation_candidate: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_command_execution: bool = False
    real_permission_granted: bool = False
    approval_granted: bool = False
    live_adapter_implemented: bool = False
    provider_registered: bool = False
    provider_invoked: bool = False
    network_called: bool = False
    command_executed: bool = False
    credential_stored: bool = False
    credential_logged: bool = False
    env_file_created: bool = False
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
    references_runtime_dependency_added: bool = False
    references_code_copied: bool = False
    PIG_execution_authority_enabled: bool = False
    llm_judge_used: bool = False
    next_required_step: str = V0293_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.29.4 Credential / Secret / Network Boundary begins or Permission / Safety / Scope policy changes."
    version: str = V0293_VERSION


class AdapterPermissionSafetyPrerequisiteSourceService:
    def __init__(self) -> None:
        self._mock_report: MockAdapterHarnessReport | None = None
        self._registry_report: AdapterRegistryReport | None = None

    def load_v0292_mock_adapter_harness_report(self) -> MockAdapterHarnessReport:
        if self._mock_report is None:
            self._mock_report = MockAdapterHarnessReportService().build_report()
        return self._mock_report

    def load_v0292_mock_adapter_harness_gate(self) -> Any:
        return self.load_v0292_mock_adapter_harness_report().mock_harness_gate

    def load_mock_run_reports(self) -> list[Any]:
        return self.load_v0292_mock_adapter_harness_report().mock_run_reports

    def load_mock_effect_boundary_validation_reports(self) -> list[Any]:
        return self.load_v0292_mock_adapter_harness_report().effect_boundary_validation_reports

    def load_no_network_boundary_reports(self) -> list[Any]:
        return self.load_v0292_mock_adapter_harness_report().no_network_boundary_reports

    def load_provider_sdk_isolation_reports(self) -> list[Any]:
        return self.load_v0292_mock_adapter_harness_report().provider_sdk_isolation_reports

    def load_mock_credential_boundary_reports(self) -> list[Any]:
        return self.load_v0292_mock_adapter_harness_report().mock_credential_boundary_reports

    def load_mock_adapter_ocel_trace_reports(self) -> list[Any]:
        return self.load_v0292_mock_adapter_harness_report().ocel_trace_reports

    def load_v0291_adapter_registry_report(self) -> AdapterRegistryReport:
        if self._registry_report is None:
            self._registry_report = AdapterRegistryReportService().build_report()
        return self._registry_report

    def load_adapter_registry(self) -> Any:
        return self.load_v0291_adapter_registry_report().adapter_registry

    def load_adapter_capability_declarations(self) -> list[Any]:
        return self.load_v0291_adapter_registry_report().capability_declarations

    def load_adapter_risk_profiles(self) -> list[Any]:
        return self.load_v0291_adapter_registry_report().risk_profiles

    def load_permission_scope_requirements(self) -> list[Any]:
        return self.load_v0291_adapter_registry_report().permission_scope_requirements

    def load_safety_scope_requirements(self) -> list[Any]:
        return self.load_v0291_adapter_registry_report().safety_scope_requirements

    def load_credential_need_declarations(self) -> list[Any]:
        return self.load_v0291_adapter_registry_report().credential_need_declarations

    def load_network_need_declarations(self) -> list[Any]:
        return self.load_v0291_adapter_registry_report().network_need_declarations

    def load_provider_invocation_prohibition_contract(self) -> dict[str, Any]:
        return _ref("provider_invocation_prohibition_contract", "provider_invocation_prohibition_contract:v0.29.0", "v0.29.0")

    def load_command_execution_prohibition_contract(self) -> dict[str, Any]:
        return _ref("command_execution_prohibition_contract", "command_execution_prohibition_contract:v0.29.0", "v0.29.0")


class ExternalAdapterPermissionSafetyPolicyService:
    def build_policy(self) -> ExternalAdapterPermissionSafetyPolicy:
        return ExternalAdapterPermissionSafetyPolicy("external_adapter_permission_safety_policy:v0.29.3")


class AdapterPermissionSafetySourceViewService:
    def build_source_view(self) -> AdapterPermissionSafetySourceView:
        source = AdapterPermissionSafetyPrerequisiteSourceService()
        mock_report = source.load_v0292_mock_adapter_harness_report()
        registry_report = source.load_v0291_adapter_registry_report()
        return AdapterPermissionSafetySourceView(
            "adapter_permission_safety_source_view:v0.29.3",
            _ref("mock_adapter_harness_report", mock_report.report_id, "v0.29.2"),
            _ref("mock_adapter_harness_gate", mock_report.mock_harness_gate.gate_id, "v0.29.2"),
            _refs("mock_adapter_run_report", mock_report.mock_run_reports, "report_id", "v0.29.2"),
            _refs("mock_effect_boundary_validation_report", mock_report.effect_boundary_validation_reports, "report_id", "v0.29.2"),
            _refs("no_network_boundary_report", mock_report.no_network_boundary_reports, "report_id", "v0.29.2"),
            _refs("provider_sdk_isolation_report", mock_report.provider_sdk_isolation_reports, "report_id", "v0.29.2"),
            _refs("mock_credential_boundary_report", mock_report.mock_credential_boundary_reports, "report_id", "v0.29.2"),
            _refs("mock_adapter_ocel_trace_report", mock_report.ocel_trace_reports, "report_id", "v0.29.2"),
            _ref("adapter_registry_report", registry_report.report_id, "v0.29.1"),
            _ref("adapter_registry", registry_report.adapter_registry.registry_id, "v0.29.1"),
            _refs("adapter_capability_declaration", registry_report.capability_declarations, "declaration_id", "v0.29.1"),
            _refs("adapter_risk_profile", registry_report.risk_profiles, "risk_profile_id", "v0.29.1"),
            _refs("adapter_permission_scope_requirement", registry_report.permission_scope_requirements, "requirement_id", "v0.29.1"),
            _refs("adapter_safety_scope_requirement", registry_report.safety_scope_requirements, "requirement_id", "v0.29.1"),
            _refs("adapter_credential_need_declaration", registry_report.credential_need_declarations, "declaration_id", "v0.29.1"),
            _refs("adapter_network_need_declaration", registry_report.network_need_declarations, "declaration_id", "v0.29.1"),
            source.load_provider_invocation_prohibition_contract(),
            source.load_command_execution_prohibition_contract(),
            "complete" if mock_report.ready_for_permission_safety_gate and registry_report.ready_for_v0_29_2 else "partial",
            mock_report.ready_for_permission_safety_gate,
        )


class AdapterPermissionSafetyRequestService:
    def build_request(self, source_view: AdapterPermissionSafetySourceView) -> AdapterPermissionSafetyRequest:
        return AdapterPermissionSafetyRequest(
            "adapter_permission_safety_request:v0.29.3",
            source_view.mock_harness_report_ref["object_id"] if source_view.mock_harness_report_ref else None,
            source_view.adapter_registry_report_ref["object_id"] if source_view.adapter_registry_report_ref else None,
            source_refs=[ref for ref in [source_view.mock_harness_report_ref, source_view.adapter_registry_report_ref] if ref],
        )


class AdapterPermissionPolicyService:
    def build_policy(self) -> AdapterPermissionPolicy:
        return AdapterPermissionPolicy("adapter_permission_policy:v0.29.3")


class AdapterSafetyPolicyService:
    def build_policy(self) -> AdapterSafetyPolicy:
        return AdapterSafetyPolicy("adapter_safety_policy:v0.29.3")


class AdapterScopePolicyService:
    def build_policy(self) -> AdapterScopePolicy:
        return AdapterScopePolicy("adapter_scope_policy:v0.29.3")


class AdapterDenyFirstRuleSetService:
    def build_rule_set(self) -> AdapterDenyFirstRuleSet:
        return AdapterDenyFirstRuleSet("adapter_deny_first_rule_set:v0.29.3")


class AdapterActionIntentService:
    def build_intents(self, mock_report: MockAdapterHarnessReport) -> list[AdapterActionIntent]:
        intents: list[AdapterActionIntent] = []
        for adapter_name in _adapter_names(mock_report):
            spec = _blueprint(adapter_name)
            intents.append(
                AdapterActionIntent(
                    f"adapter_action_intent:{adapter_name}:v0.29.3",
                    adapter_name,
                    spec["provider_kind"],
                    spec["capability_name"],
                    spec["action_kind"],
                    f"{adapter_name} permission/safety intent is evaluated as metadata-only.",
                    spec["action_kind"],
                    spec["requires_provider_invocation"],
                    spec["requires_network"],
                    spec["requires_credentials"],
                    spec["requires_command_execution"],
                    spec["requires_private_data"],
                    spec["requires_raw_provider_output_persistence"],
                    spec["action_allowed_now"],
                )
            )
        return intents


class AdapterActionScopeService:
    def build_scopes(self, intents: list[AdapterActionIntent]) -> list[AdapterActionScope]:
        scopes = []
        for intent in intents:
            spec = _blueprint(intent.adapter_name)
            scopes.append(
                AdapterActionScope(
                    f"adapter_action_scope:{intent.adapter_name}:v0.29.3",
                    intent.adapter_name,
                    intent.capability_name,
                    _ref("adapter_action_intent", intent.intent_id, V0293_VERSION),
                    spec["scope_kind"],
                    f"{intent.adapter_name} scope is {spec['scope_kind']} and grants no runtime permission.",
                    True,
                    True,
                )
            )
        return scopes


class AdapterScopeMatrixService:
    def build_matrix(self, scopes: list[AdapterActionScope]) -> AdapterScopeMatrix:
        rows: list[AdapterScopeMatrixRow] = []
        for scope in scopes:
            spec = _blueprint(scope.adapter_name)
            rows.append(
                AdapterScopeMatrixRow(
                    f"adapter_scope_matrix_row:{scope.adapter_name}:v0.29.3",
                    scope.adapter_name,
                    scope.capability_name,
                    _ref("adapter_action_scope", scope.scope_id, V0293_VERSION),
                    spec["required_permission_scope"] != "none",
                    spec["safety_class"] != "safe_mock_only",
                    spec["approval_required"],
                    spec["future_version"] == "v0.29.4",
                    False,
                    spec["future_version"] == "v0.29.6",
                    spec["future_version"] is not None and "v0.29.8" in spec["future_version"],
                    spec["matrix_status"],
                )
            )
        return AdapterScopeMatrix(
            "adapter_scope_matrix:v0.29.3",
            rows,
            len(rows),
            sum(row.scope_status == "mock_only" for row in rows),
            sum(row.approval_required for row in rows),
            sum(row.scope_status == "denied" for row in rows),
            sum(row.scope_status == "deferred" for row in rows),
            sum(row.scope_status == "unknown" for row in rows),
            "warning",
        )


class AdapterPermissionScopeEvaluationService:
    def build_evaluations(self, scopes: list[AdapterActionScope], classifications: list[AdapterSafetyClassification] | None = None) -> list[AdapterPermissionScopeEvaluation]:
        blocked = {item.adapter_name: item.blocks_permission_candidate for item in classifications or []}
        return [
            AdapterPermissionScopeEvaluation(
                f"adapter_permission_scope_evaluation:{scope.adapter_name}:v0.29.3",
                scope.adapter_name,
                scope.capability_name,
                _ref("adapter_action_scope", scope.scope_id, V0293_VERSION),
                _blueprint(scope.adapter_name)["required_permission_scope"],
                scope.scope_minimal,
                True,
                True,
                not blocked.get(scope.adapter_name, False) and scope.scope_kind == "mock_only",
                False,
                "passed" if scope.scope_kind == "mock_only" else "warning",
            )
            for scope in scopes
        ]


class AdapterSafetyClassificationService:
    def build_classifications(self, intents: list[AdapterActionIntent]) -> list[AdapterSafetyClassification]:
        classifications = []
        for intent in intents:
            spec = _blueprint(intent.adapter_name)
            classifications.append(
                AdapterSafetyClassification(
                    f"adapter_safety_classification:{intent.adapter_name}:v0.29.3",
                    intent.adapter_name,
                    intent.capability_name,
                    _ref("adapter_action_intent", intent.intent_id, V0293_VERSION),
                    spec["safety_class"],
                    spec["risk_level"],
                    spec["safety_class"].startswith("blocked_"),
                    spec["approval_required"],
                    spec["requires_credentials"],
                    spec["requires_network"],
                    spec["action_kind"] == "external_side_effect",
                )
            )
        return classifications


class AdapterSafetyFindingService:
    def build_findings(self, classifications: list[AdapterSafetyClassification]) -> list[AdapterSafetyFinding]:
        findings = []
        for classification in classifications:
            finding_type = "safe_mock_only"
            if classification.requires_future_credential_boundary:
                finding_type = "credential_sensitive"
            elif classification.requires_future_network_boundary:
                finding_type = "network_sensitive"
            elif classification.requires_future_audit_rollback:
                finding_type = "external_side_effect_requires_future_gate"
            elif classification.safety_class == "blocked_rpa_future_track":
                finding_type = "rpa_future_track"
            findings.append(
                AdapterSafetyFinding(
                    f"adapter_safety_finding:{classification.adapter_name}:v0.29.3",
                    classification.adapter_name,
                    classification.capability_name,
                    finding_type,
                    "info" if finding_type == "safe_mock_only" else "warning",
                    False,
                    f"{classification.adapter_name} safety classification is {classification.safety_class}.",
                )
            )
        return findings


class UserApprovalRequirementService:
    def build_requirements(self, scopes: list[AdapterActionScope]) -> list[UserApprovalRequirement]:
        requirements = []
        for scope in scopes:
            spec = _blueprint(scope.adapter_name)
            requirements.append(
                UserApprovalRequirement(
                    f"user_approval_requirement:{scope.adapter_name}:v0.29.3",
                    scope.adapter_name,
                    scope.capability_name,
                    _ref("adapter_action_scope", scope.scope_id, V0293_VERSION),
                    spec["approval_required"],
                    "No approval required for mock-only metadata." if not spec["approval_required"] else "Future external action requires scoped user approval candidate only.",
                )
            )
        return requirements


class AdapterApprovalCandidateService:
    def build_candidates(
        self,
        intents: list[AdapterActionIntent],
        evaluations: list[AdapterPermissionScopeEvaluation],
        classifications: list[AdapterSafetyClassification],
        requirements: list[UserApprovalRequirement],
    ) -> list[AdapterApprovalCandidate]:
        evals = {item.adapter_name: item for item in evaluations}
        classes = {item.adapter_name: item for item in classifications}
        reqs = {item.adapter_name: item for item in requirements}
        candidates = []
        for intent in intents:
            spec = _blueprint(intent.adapter_name)
            status = "allowed_candidate" if spec["decision"] == "mock_only" else "deferred"
            candidates.append(
                AdapterApprovalCandidate(
                    f"adapter_approval_candidate:{intent.adapter_name}:v0.29.3",
                    intent.adapter_name,
                    intent.capability_name,
                    _ref("adapter_action_intent", intent.intent_id, V0293_VERSION),
                    _ref("adapter_permission_scope_evaluation", evals[intent.adapter_name].evaluation_id, V0293_VERSION),
                    _ref("adapter_safety_classification", classes[intent.adapter_name].classification_id, V0293_VERSION),
                    _ref("user_approval_requirement", reqs[intent.adapter_name].requirement_id, V0293_VERSION),
                    status,
                    f"{intent.adapter_name} candidate is metadata-only and grants no permission.",
                )
            )
        return candidates


class AdapterPermissionDecisionService:
    def build_candidates(self, approval_candidates: list[AdapterApprovalCandidate]) -> list[AdapterPermissionDecisionCandidate]:
        candidates = []
        for candidate in approval_candidates:
            spec = _blueprint(candidate.adapter_name)
            candidates.append(
                AdapterPermissionDecisionCandidate(
                    f"adapter_permission_decision_candidate:{candidate.adapter_name}:v0.29.3",
                    candidate.adapter_name,
                    candidate.capability_name,
                    spec["decision"],
                    f"Deny-first decision is {spec['decision']} with no runtime grant.",
                    spec["future_version"],
                    _ref("adapter_approval_candidate", candidate.approval_candidate_id, V0293_VERSION),
                )
            )
        return candidates

    def build_records(self, decision_candidates: list[AdapterPermissionDecisionCandidate]) -> list[AdapterPermissionDecisionRecord]:
        return [
            AdapterPermissionDecisionRecord(
                f"adapter_permission_decision_record:{candidate.adapter_name}:v0.29.3",
                candidate.adapter_name,
                candidate.capability_name,
                _ref("adapter_permission_decision_candidate", candidate.decision_candidate_id, V0293_VERSION),
                candidate.proposed_decision,
                candidate.decision_reason,
                _now(),
            )
            for candidate in decision_candidates
        ]


class AdapterScopeExpiryPolicyService:
    def build_policy(self) -> AdapterScopeExpiryPolicy:
        return AdapterScopeExpiryPolicy("adapter_scope_expiry_policy:v0.29.3")


class AdapterSafetyCheckService:
    def build_private_data_checks(self, intents: list[AdapterActionIntent]) -> list[PrivateDataSafetyCheck]:
        return [
            PrivateDataSafetyCheck(
                f"private_data_safety_check:{intent.adapter_name}:v0.29.3",
                intent.adapter_name,
                intent.capability_name,
                intent.requires_private_data,
                False,
                False,
                False,
                intent.requires_private_data,
                "blocked" if intent.requires_private_data else "passed",
            )
            for intent in intents
        ]

    def build_credential_reference_checks(self, intents: list[AdapterActionIntent]) -> list[CredentialReferenceSafetyCheck]:
        return [
            CredentialReferenceSafetyCheck(
                f"credential_reference_safety_check:{intent.adapter_name}:v0.29.3",
                intent.adapter_name,
                intent.capability_name,
                intent.requires_credentials,
                False,
                False,
                False,
                False,
                "v0.29.4",
                intent.requires_credentials,
                "warning" if intent.requires_credentials else "passed",
            )
            for intent in intents
        ]

    def build_network_need_checks(self, intents: list[AdapterActionIntent]) -> list[NetworkNeedSafetyCheck]:
        return [
            NetworkNeedSafetyCheck(
                f"network_need_safety_check:{intent.adapter_name}:v0.29.3",
                intent.adapter_name,
                intent.capability_name,
                intent.requires_network,
                False,
                False,
                False,
                "v0.29.4",
                intent.requires_network,
                "warning" if intent.requires_network else "passed",
            )
            for intent in intents
        ]

    def build_command_like_action_checks(self, intents: list[AdapterActionIntent]) -> list[CommandLikeActionSafetyCheck]:
        return [
            CommandLikeActionSafetyCheck(
                f"command_like_action_safety_check:{intent.adapter_name}:v0.29.3",
                intent.adapter_name,
                intent.capability_name,
                intent.action_kind == "command_like" or intent.requires_command_execution,
                intent.requires_command_execution,
                False,
                False,
                False,
                True,
                "blocked" if intent.requires_command_execution else "passed",
            )
            for intent in intents
        ]

    def build_external_side_effect_checks(self, intents: list[AdapterActionIntent]) -> list[ExternalSideEffectSafetyCheck]:
        return [
            ExternalSideEffectSafetyCheck(
                f"external_side_effect_safety_check:{intent.adapter_name}:v0.29.3",
                intent.adapter_name,
                intent.capability_name,
                intent.action_kind == "external_side_effect",
                False,
                True,
                "v0.29.6",
                intent.action_kind == "external_side_effect",
                "warning" if intent.action_kind == "external_side_effect" else "passed",
            )
            for intent in intents
        ]

    def build_data_exfiltration_checks(self, intents: list[AdapterActionIntent]) -> list[DataExfiltrationSafetyCheck]:
        return [
            DataExfiltrationSafetyCheck(
                f"data_exfiltration_safety_check:{intent.adapter_name}:v0.29.3",
                intent.adapter_name,
                intent.capability_name,
                "medium" if intent.requires_network else "none",
                False,
                False,
                intent.requires_raw_provider_output_persistence,
                "blocked" if intent.requires_raw_provider_output_persistence else "passed",
            )
            for intent in intents
        ]

    def build_rpa_deferral_checks(self, intents: list[AdapterActionIntent]) -> list[RPAScopeDeferralCheck]:
        return [
            RPAScopeDeferralCheck(
                f"rpa_scope_deferral_check:{intent.adapter_name}:v0.29.3",
                intent.adapter_name,
                intent.capability_name,
                intent.action_kind == "rpa_action",
                intent.action_kind == "rpa_action",
                intent.action_kind == "rpa_action",
                intent.action_kind == "rpa_action",
                False,
                True,
                "v0.29.7_or_later_certification_and_v0.29.8_preview_gate",
                "warning" if intent.action_kind == "rpa_action" else "passed",
            )
            for intent in intents
        ]


class AdapterPermissionSafetyGateService:
    def evaluate_gate(
        self,
        source_view: AdapterPermissionSafetySourceView,
        matrix: AdapterScopeMatrix,
        rule_set: AdapterDenyFirstRuleSet,
        evaluations: list[AdapterPermissionScopeEvaluation],
        classifications: list[AdapterSafetyClassification],
        approval_candidates: list[AdapterApprovalCandidate],
        decision_records: list[AdapterPermissionDecisionRecord],
        private_checks: list[PrivateDataSafetyCheck],
        credential_checks: list[CredentialReferenceSafetyCheck],
        network_checks: list[NetworkNeedSafetyCheck],
        command_checks: list[CommandLikeActionSafetyCheck],
        side_effect_checks: list[ExternalSideEffectSafetyCheck],
        exfiltration_checks: list[DataExfiltrationSafetyCheck],
        rpa_checks: list[RPAScopeDeferralCheck],
    ) -> AdapterPermissionSafetyGate:
        no_permission = all(not record.permission_granted_now and not record.approval_granted_now for record in decision_records)
        no_provider = all(not record.provider_invoked_now for record in decision_records)
        no_network = all(not report.network_called_now for report in network_checks)
        no_credential = all(not report.credential_storage_detected and not report.credential_logging_detected for report in credential_checks)
        no_command = all(not report.command_executed_now and report.command_like_action_blocks_now for report in command_checks)
        ready = no_permission and no_provider and no_network and no_credential and no_command
        return AdapterPermissionSafetyGate(
            "adapter_permission_safety_gate:v0.29.3",
            _ref("adapter_permission_safety_source_view", source_view.source_view_id, V0293_VERSION),
            _ref("adapter_scope_matrix", matrix.matrix_id, V0293_VERSION),
            _ref("adapter_deny_first_rule_set", rule_set.rule_set_id, V0293_VERSION),
            _refs("adapter_permission_scope_evaluation", evaluations, "evaluation_id", V0293_VERSION),
            _refs("adapter_safety_classification", classifications, "classification_id", V0293_VERSION),
            _refs("adapter_approval_candidate", approval_candidates, "approval_candidate_id", V0293_VERSION),
            _refs("adapter_permission_decision_record", decision_records, "decision_record_id", V0293_VERSION),
            _refs("private_data_safety_check", private_checks, "check_id", V0293_VERSION),
            _refs("credential_reference_safety_check", credential_checks, "check_id", V0293_VERSION),
            _refs("network_need_safety_check", network_checks, "check_id", V0293_VERSION),
            _refs("command_like_action_safety_check", command_checks, "check_id", V0293_VERSION),
            _refs("external_side_effect_safety_check", side_effect_checks, "check_id", V0293_VERSION),
            _refs("data_exfiltration_safety_check", exfiltration_checks, "check_id", V0293_VERSION),
            _refs("rpa_scope_deferral_check", rpa_checks, "check_id", V0293_VERSION),
            rule_set.deny_first_enabled and rule_set.default_decision == "deny",
            all(item.evaluation_status in {"passed", "warning"} for item in evaluations),
            bool(classifications),
            bool(approval_candidates),
            all(not item.private_data_detected and not item.actual_user_data_detected and not item.actual_company_data_detected for item in private_checks),
            all(not item.credential_value_detected and not item.credential_storage_detected and not item.credential_logging_detected for item in credential_checks),
            all(not item.network_called_now and not item.provider_sdk_network_detected for item in network_checks),
            no_command,
            all(not item.external_side_effect_performed_now for item in side_effect_checks),
            all(item.rpa_action_deferred and not item.rpa_adapter_implemented_now for item in rpa_checks),
            no_permission,
            no_provider,
            no_network,
            no_credential,
            no_command,
            "warning",
            ready,
            ready,
        )


class AdapterPermissionSafetyAuditTrailService:
    def build_audit_trail(
        self,
        request: AdapterPermissionSafetyRequest,
        source_view: AdapterPermissionSafetySourceView,
        gate: AdapterPermissionSafetyGate,
        policies: list[ModelMixin],
        decision_records: list[AdapterPermissionDecisionRecord],
        safety_checks: list[ModelMixin],
    ) -> AdapterPermissionSafetyAuditTrail:
        return AdapterPermissionSafetyAuditTrail(
            "adapter_permission_safety_audit_trail:v0.29.3",
            _ref("adapter_permission_safety_request", request.request_id, V0293_VERSION),
            _ref("adapter_permission_safety_source_view", source_view.source_view_id, V0293_VERSION),
            _ref("adapter_permission_safety_gate", gate.gate_id, V0293_VERSION),
            [{"object_type": policy.__class__.__name__, "object_id": getattr(policy, "policy_id", "unknown"), "version": V0293_VERSION} for policy in policies],
            _refs("adapter_permission_decision_record", decision_records, "decision_record_id", V0293_VERSION),
            [{"object_type": item.__class__.__name__, "object_id": getattr(item, "check_id", "unknown"), "version": V0293_VERSION} for item in safety_checks],
            len(decision_records) + len(safety_checks) + len(policies) + 3,
        )


class AdapterPermissionSafetyFindingService:
    BLOCKED_FINDINGS = {
        "permission_grant_attempted",
        "approval_grant_attempted",
        "provider_registration_attempted",
        "provider_invocation_attempted",
        "network_call_attempted",
        "credential_storage_attempted",
        "credential_logging_attempted",
        "env_file_creation_attempted",
        "command_execution_attempted",
        "shell_execution_attempted",
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
        "references_runtime_dependency_detected",
        "references_code_copy_detected",
        "PIG_execution_authority_detected",
        "llm_judge_detected",
    }

    def build_findings(self) -> list[AdapterPermissionSafetyFinding]:
        return [
            AdapterPermissionSafetyFinding("adapter_permission_safety_finding:policy_created:v0.29.3", "info", "permission_safety_policy_created", "Permission/safety/scope policy created with deny-first metadata-only behavior.", _ref("external_adapter_permission_safety_policy", "external_adapter_permission_safety_policy:v0.29.3", V0293_VERSION), [], None),
            AdapterPermissionSafetyFinding("adapter_permission_safety_finding:scope_matrix_created:v0.29.3", "info", "scope_matrix_created", "Scope matrix created without permission grants.", _ref("adapter_scope_matrix", "adapter_scope_matrix:v0.29.3", V0293_VERSION), [], "Withdraw if scope records grant runtime permission."),
            AdapterPermissionSafetyFinding("adapter_permission_safety_finding:gate_created:v0.29.3", "warning", "permission_safety_gate_created", "Gate is ready for v0.29.4 credential/network boundary only; invocation remains false.", _ref("adapter_permission_safety_gate", "adapter_permission_safety_gate:v0.29.3", V0293_VERSION), [], "Withdraw if ready_for_provider_invocation or ready_for_command_execution becomes true."),
        ]


class AdapterPermissionSafetyReportService:
    def build_report(self, report_id: str | None = None) -> AdapterPermissionSafetyReport:
        source_service = AdapterPermissionSafetyPrerequisiteSourceService()
        mock_report = source_service.load_v0292_mock_adapter_harness_report()
        policy = ExternalAdapterPermissionSafetyPolicyService().build_policy()
        source_view = AdapterPermissionSafetySourceViewService().build_source_view()
        request = AdapterPermissionSafetyRequestService().build_request(source_view)
        permission_policy = AdapterPermissionPolicyService().build_policy()
        safety_policy = AdapterSafetyPolicyService().build_policy()
        scope_policy = AdapterScopePolicyService().build_policy()
        deny_first_rule_set = AdapterDenyFirstRuleSetService().build_rule_set()
        action_intents = AdapterActionIntentService().build_intents(mock_report)
        action_scopes = AdapterActionScopeService().build_scopes(action_intents)
        classifications = AdapterSafetyClassificationService().build_classifications(action_intents)
        evaluations = AdapterPermissionScopeEvaluationService().build_evaluations(action_scopes, classifications)
        scope_matrix = AdapterScopeMatrixService().build_matrix(action_scopes)
        safety_findings = AdapterSafetyFindingService().build_findings(classifications)
        approval_requirements = UserApprovalRequirementService().build_requirements(action_scopes)
        approval_candidates = AdapterApprovalCandidateService().build_candidates(action_intents, evaluations, classifications, approval_requirements)
        decision_service = AdapterPermissionDecisionService()
        decision_candidates = decision_service.build_candidates(approval_candidates)
        decision_records = decision_service.build_records(decision_candidates)
        scope_expiry_policy = AdapterScopeExpiryPolicyService().build_policy()
        safety_check_service = AdapterSafetyCheckService()
        private_data_checks = safety_check_service.build_private_data_checks(action_intents)
        credential_checks = safety_check_service.build_credential_reference_checks(action_intents)
        network_checks = safety_check_service.build_network_need_checks(action_intents)
        command_checks = safety_check_service.build_command_like_action_checks(action_intents)
        side_effect_checks = safety_check_service.build_external_side_effect_checks(action_intents)
        exfiltration_checks = safety_check_service.build_data_exfiltration_checks(action_intents)
        rpa_checks = safety_check_service.build_rpa_deferral_checks(action_intents)
        gate = AdapterPermissionSafetyGateService().evaluate_gate(
            source_view,
            scope_matrix,
            deny_first_rule_set,
            evaluations,
            classifications,
            approval_candidates,
            decision_records,
            private_data_checks,
            credential_checks,
            network_checks,
            command_checks,
            side_effect_checks,
            exfiltration_checks,
            rpa_checks,
        )
        policies = [policy, permission_policy, safety_policy, scope_policy, scope_expiry_policy]
        safety_checks = private_data_checks + credential_checks + network_checks + command_checks + side_effect_checks + exfiltration_checks + rpa_checks
        audit_trail = AdapterPermissionSafetyAuditTrailService().build_audit_trail(request, source_view, gate, policies, decision_records, safety_checks)
        findings = AdapterPermissionSafetyFindingService().build_findings()
        return AdapterPermissionSafetyReport(
            report_id or "adapter_permission_safety_report:v0.29.3",
            _now(),
            policy,
            request,
            source_view,
            permission_policy,
            safety_policy,
            scope_policy,
            deny_first_rule_set,
            action_intents,
            action_scopes,
            scope_matrix,
            evaluations,
            classifications,
            safety_findings,
            approval_requirements,
            approval_candidates,
            decision_candidates,
            decision_records,
            scope_expiry_policy,
            private_data_checks,
            credential_checks,
            network_checks,
            command_checks,
            side_effect_checks,
            exfiltration_checks,
            rpa_checks,
            gate,
            audit_trail,
            findings,
            "warning",
            gate.ready_for_v0_29_4,
            gate.ready_for_credential_network_boundary,
            limitations=["v0.29.3 creates permission, safety, and scope decision records only. Credential, network, dry-run, approval/audit/rollback, certification, and live invocation remain future work."],
            withdrawal_conditions=["Withdraw if real permission grants, approval grants, provider invocation, network calls, credentials, command execution, live adapters, RPA integration, private/raw data, or LLM-judge-only authority appear."],
        )

    def build_all_parts(self, report_id: str | None = None) -> dict[str, Any]:
        report = self.build_report(report_id=report_id)
        return {
            "policy": report.policy,
            "request": report.request,
            "source-view": report.source_view,
            "permission-policy": report.permission_policy,
            "safety-policy": report.safety_policy,
            "scope-policy": report.scope_policy,
            "deny-first": report.deny_first_rule_set,
            "intents": report.action_intents,
            "scopes": report.action_scopes,
            "scope-matrix": report.scope_matrix,
            "permission-evaluation": report.permission_scope_evaluations,
            "safety-classification": report.safety_classifications,
            "approval-requirements": report.approval_requirements,
            "approval-candidates": report.approval_candidates,
            "decision-records": report.decision_records,
            "expiry": report.scope_expiry_policy,
            "private-data": report.private_data_safety_checks,
            "credentials": report.credential_safety_checks,
            "network": report.network_safety_checks,
            "command-like": report.command_like_action_checks,
            "side-effects": report.external_side_effect_checks,
            "exfiltration": report.data_exfiltration_checks,
            "rpa-deferral": report.rpa_deferral_checks,
            "evaluate": report.permission_safety_gate,
            "audit": report.audit_trail,
            "findings": report.findings,
            "report": report,
        }

    def build_pig_report(self) -> dict[str, Any]:
        report = self.build_report()
        return {
            "version": V0293_VERSION,
            "layer": V0293_LAYER,
            "subject": "permission_safety_scope_gate_for_external_adapters",
            "principles": [
                "Permission gate is not permission grant",
                "Safety gate is not provider invocation",
                "Scope declaration is not approval",
                "Approval requirement is not approval",
                "Approval candidate is not execution",
                "Deny-first rule precedes allow",
                "No-op / deny / defer are valid outcomes",
                "Permission must be scoped, expiring, auditable, and OCEL-visible",
                "Credential sensitivity requires future credential boundary",
                "Network sensitivity requires future network boundary",
                "No-provider-invocation remains the default outcome",
            ],
            "safety_boundary": {
                "real_permission_granted": report.real_permission_granted,
                "approval_granted": report.approval_granted,
                "live_adapter_implemented": report.live_adapter_implemented,
                "provider_registered": report.provider_registered,
                "provider_invoked": report.provider_invoked,
                "network_called": report.network_called,
                "command_executed": report.command_executed,
                "credential_stored": report.credential_stored,
                "credential_logged": report.credential_logged,
                "env_file_created": report.env_file_created,
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
                "references_runtime_dependency_added": report.references_runtime_dependency_added,
                "references_code_copied": report.references_code_copied,
                "PIG_execution_authority_enabled": report.PIG_execution_authority_enabled,
                "llm_judge_enabled": False,
            },
            "future_direction": [
                "v0.29.4 Credential / Secret / Network Boundary",
                "v0.29.5 Adapter Invocation Candidate / Dry-Run Plan",
                "v0.29.6 Provider Invocation Approval / Audit / Rollback Boundary",
                "v0.29.7 External Skill Packaging / Certification Matrix",
                "v0.29.8 Limited Provider Invocation Preview Gate",
                "v0.29.9 External Provider Adapter Foundation Consolidation",
            ],
            "next_step": V0293_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "adapter_permission_safety_scope_gate_created",
            "version": V0293_VERSION,
            "source_read_models": [
                "MockAdapterHarnessState",
                "MockAdapterHarnessGateState",
                "MockAdapterRunState",
                "MockEffectBoundaryValidationState",
                "NoNetworkBoundaryState",
                "ProviderSDKIsolationState",
                "MockCredentialBoundaryState",
                "AdapterRegistryState",
                "AdapterCapabilityDeclarationState",
                "AdapterRiskProfileState",
                "AdapterPermissionScopeRequirementState",
                "AdapterSafetyScopeRequirementState",
                "AdapterCredentialNeedDeclarationState",
                "AdapterNetworkNeedDeclarationState",
                "ProviderInvocationProhibitionState",
                "CommandExecutionProhibitionState",
                "PigGuidanceState",
                "OCPXProjectionState",
            ],
            "target_read_models": [
                "AdapterPermissionSafetyGateState",
                "AdapterScopeMatrixState",
                "AdapterActionIntentState",
                "AdapterPermissionScopeEvaluationState",
                "AdapterSafetyClassificationState",
                "AdapterApprovalCandidateState",
                "AdapterPermissionDecisionRecordState",
                "AdapterSafetyCheckState",
                "AdapterPermissionSafetyAuditState",
                "V029ReadinessState",
            ],
            "effect_types": V0293_EFFECT_TYPES,
            "forbidden_effect_types": V0293_FORBIDDEN_EFFECT_TYPES,
        }


def render_adapter_permission_safety_cli(parts: dict[str, Any], section: str = "report") -> str:
    report: AdapterPermissionSafetyReport = parts["report"]
    lines = [
        f"Permission / Safety / Scope Gate for External Adapters {section}",
        f"version={report.version}",
        f"layer={report.policy.layer}",
        f"report_status={report.report_status}",
        f"ready_for_v0_29_4={_bool(report.ready_for_v0_29_4)}",
        f"ready_for_credential_network_boundary={_bool(report.ready_for_credential_network_boundary)}",
        f"ready_for_invocation_candidate={_bool(report.ready_for_invocation_candidate)}",
        f"ready_for_provider_invocation={_bool(report.ready_for_provider_invocation)}",
        f"ready_for_command_execution={_bool(report.ready_for_command_execution)}",
        f"real_permission_granted={_bool(report.real_permission_granted)}",
        f"approval_granted={_bool(report.approval_granted)}",
        f"live_adapter_implemented={_bool(report.live_adapter_implemented)}",
        f"provider_registered={_bool(report.provider_registered)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"network_called={_bool(report.network_called)}",
        f"command_executed={_bool(report.command_executed)}",
        f"credential_stored={_bool(report.credential_stored)}",
        f"credential_logged={_bool(report.credential_logged)}",
        f"env_file_created={_bool(report.env_file_created)}",
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
