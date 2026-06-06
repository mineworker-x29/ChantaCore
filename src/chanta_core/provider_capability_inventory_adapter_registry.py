from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.external_provider_adapter_contract import (
    ExternalAdapterContractReportService,
    ModelMixin,
    _bool,
    _ref,
)
from chanta_core.utility.time import utc_now_iso


V0291_VERSION = "v0.29.1"
V0291_LAYER = "external_provider_adapter"
V0291_TRACK = "External Skill / External Provider Adapter Development"
V0291_NAME = "Provider Capability Inventory / Adapter Registry"
V0291_KOREAN_NAME = "Provider Capability Inventory·Adapter Registry"
V0291_NEXT_STEP = "v0.29.2 Mock Adapter Harness / No-Network Default"

V0291_OBJECT_TYPES = [
    "provider_capability_inventory_policy",
    "adapter_registry_policy",
    "provider_kind_catalog",
    "provider_kind_record",
    "provider_capability_inventory",
    "provider_capability_record",
    "adapter_registry",
    "adapter_registry_entry",
    "adapter_capability_declaration",
    "adapter_availability_status",
    "adapter_readiness_status",
    "adapter_disabled_reason",
    "adapter_dependency_boundary_report",
    "adapter_risk_profile",
    "adapter_permission_scope_requirement",
    "adapter_safety_scope_requirement",
    "adapter_credential_need_declaration",
    "adapter_network_need_declaration",
    "adapter_ocel_visibility_declaration",
    "adapter_registry_gate",
    "adapter_registry_finding",
    "adapter_registry_report",
    "external_adapter_contract_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

V0291_EVENT_TYPES = [
    "adapter_registry_requested",
    "adapter_registry_prerequisites_loaded",
    "provider_capability_inventory_policy_created",
    "adapter_registry_policy_created",
    "provider_kind_catalog_created",
    "provider_kind_record_created",
    "provider_capability_inventory_created",
    "provider_capability_record_created",
    "adapter_registry_created",
    "adapter_registry_entry_created",
    "adapter_capability_declaration_created",
    "adapter_availability_status_created",
    "adapter_readiness_status_created",
    "adapter_disabled_reason_created",
    "adapter_dependency_boundary_report_created",
    "adapter_risk_profile_created",
    "adapter_permission_scope_requirement_created",
    "adapter_safety_scope_requirement_created",
    "adapter_credential_need_declaration_created",
    "adapter_network_need_declaration_created",
    "adapter_ocel_visibility_declaration_created",
    "adapter_registry_gate_evaluated",
    "adapter_registry_report_created",
    "adapter_registry_warning_created",
    "adapter_registry_blocked",
]

V0291_EFFECT_TYPES = [
    "read_only_observation",
    "provider_capability_inventory_created",
    "adapter_registry_created",
    "adapter_registry_entry_created",
    "adapter_capability_declaration_created",
    "adapter_status_recorded",
    "adapter_registry_gate_evaluated",
    "state_candidate_created",
]

V0291_FORBIDDEN_EFFECT_TYPES = [
    "external_provider_adapter_implemented",
    "external_skill_adapter_implemented",
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

REQUIRED_OCEL_EVENTS = [
    "adapter_declared",
    "capability_declared",
    "registry_entry_created",
    "availability_status_recorded",
    "readiness_status_recorded",
    "permission_scope_required",
    "safety_scope_required",
    "credential_need_declared",
    "network_need_declared",
]

RISK_DIMENSIONS = [
    "credential_exposure",
    "network_access",
    "private_data_exposure",
    "provider_side_effect",
    "command_execution",
    "data_exfiltration",
    "audit_gap",
    "rollback_gap",
    "OCEL_visibility_gap",
    "RPA_scope_creep",
    "external_dominion_creep",
]


def _now() -> str:
    return utc_now_iso()


@dataclass
class ProviderCapabilityInventoryPolicy(ModelMixin):
    policy_id: str
    version: str = V0291_VERSION
    layer: str = V0291_LAYER
    inventory_enabled: bool = True
    registry_enabled: bool = True
    inventory_is_not_implementation: bool = True
    registry_is_not_execution: bool = True
    registry_entry_is_not_provider_registration: bool = True
    capability_declaration_is_not_permission: bool = True
    provider_availability_is_not_invocation_readiness: bool = True
    unknown_status_is_not_available: bool = True
    blocked_status_must_remain_blocked: bool = True
    adapter_implementation_enabled_now: bool = False
    provider_registration_enabled_now: bool = False
    provider_invocation_enabled_now: bool = False
    network_access_enabled_now: bool = False
    credential_storage_enabled_now: bool = False
    command_execution_expansion_enabled_now: bool = False
    rpa_adapter_enabled_now: bool = False
    external_agent_dominion_enabled_now: bool = False
    schumpeter_private_runtime_enabled_now: bool = False
    mock_no_network_required_before_live: bool = True
    permission_gate_required_before_invocation: bool = True
    safety_gate_required_before_invocation: bool = True
    credential_boundary_required_before_invocation: bool = True
    network_boundary_required_before_invocation: bool = True
    audit_required_before_invocation: bool = True
    rollback_or_noop_required_before_invocation: bool = True
    ocel_visibility_required_before_invocation: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AdapterRegistryPolicy(ModelMixin):
    policy_id: str
    registry_entries_allowed: bool = True
    registry_entries_are_metadata_only: bool = True
    real_provider_registration_forbidden_now: bool = True
    adapter_runtime_binding_forbidden_now: bool = True
    registry_entry_requires_contract_ref: bool = True
    registry_entry_requires_provider_kind: bool = True
    registry_entry_requires_capability_declarations: bool = True
    registry_entry_requires_availability_status: bool = True
    registry_entry_requires_readiness_status: bool = True
    registry_entry_requires_disabled_reason_if_disabled: bool = True
    registry_entry_requires_risk_profile: bool = True
    registry_entry_requires_permission_scope_requirements: bool = True
    registry_entry_requires_safety_scope_requirements: bool = True
    registry_entry_requires_credential_need_declaration: bool = True
    registry_entry_requires_network_need_declaration: bool = True
    registry_entry_requires_ocel_visibility_declaration: bool = True
    provider_registration_enabled_now: bool = False
    provider_invocation_enabled_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0291_VERSION


@dataclass
class ProviderKindRecord(ModelMixin):
    provider_kind_id: str
    provider_kind: str
    provider_kind_summary: str
    allowed_now: bool
    network_required_later: bool
    credential_required_later: bool
    future_track: bool
    required_future_gate: str | None
    implementation_allowed_now: bool = False
    invocation_allowed_now: bool = False
    command_execution_required_later: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0291_VERSION


@dataclass
class ProviderKindCatalog(ModelMixin):
    catalog_id: str
    provider_kinds: list[ProviderKindRecord]
    provider_kind_count: int
    catalog_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0291_VERSION


@dataclass
class ProviderCapabilityRecord(ModelMixin):
    capability_record_id: str
    provider_kind: str
    capability_name: str
    capability_summary: str
    capability_category: str
    capability_status: str
    public_safe: bool
    requires_provider_registration: bool
    requires_provider_invocation: bool
    requires_network: bool
    requires_credentials: bool
    requires_command_execution: bool
    requires_private_data: bool
    requires_schumpeter_private_overlay: bool
    required_permission_scope: str | None
    required_safety_scope: str | None
    required_future_gate: str | None
    capability_declaration_is_permission: bool = False
    capability_declaration_is_invocation: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0291_VERSION


@dataclass
class ProviderCapabilityInventory(ModelMixin):
    inventory_id: str
    policy_ref: dict[str, Any]
    provider_kind_catalog_ref: dict[str, Any]
    capability_records: list[ProviderCapabilityRecord]
    capability_count: int
    available_count: int
    gated_count: int
    disabled_count: int
    future_track_count: int
    blocked_count: int
    unknown_count: int
    inventory_status: str
    provider_invocation_enabled: bool = False
    provider_registration_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0291_VERSION


@dataclass
class AdapterCapabilityDeclaration(ModelMixin):
    declaration_id: str
    adapter_name: str
    provider_kind: str
    capability_name: str
    capability_summary: str
    input_schema_ref: dict[str, Any] | None
    output_schema_ref: dict[str, Any] | None
    effect_boundary_ref: dict[str, Any] | None
    risk_level: str
    required_permission_scope: str | None
    required_safety_scope: str | None
    required_credential_boundary: bool
    required_network_boundary: bool
    required_audit_boundary: bool
    required_rollback_boundary: bool
    required_ocel_visibility: bool
    declaration_status: str
    declaration_is_permission: bool = False
    declaration_is_invocation: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0291_VERSION


@dataclass
class AdapterAvailabilityStatus(ModelMixin):
    status_id: str
    adapter_name: str
    availability: str
    availability_reason: str
    available_for_registry: bool
    available_for_implementation: bool = False
    available_for_invocation: bool = False
    available_for_network: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0291_VERSION


@dataclass
class AdapterReadinessStatus(ModelMixin):
    status_id: str
    adapter_name: str
    contract_ready: bool
    inventory_ready: bool
    registry_ready: bool
    readiness_status: str
    mock_ready: bool = False
    permission_gate_ready: bool = False
    safety_gate_ready: bool = False
    credential_boundary_ready: bool = False
    network_boundary_ready: bool = False
    audit_rollback_ready: bool = False
    certification_ready: bool = False
    invocation_preview_ready: bool = False
    ready_for_implementation: bool = False
    ready_for_provider_registration: bool = False
    ready_for_provider_invocation: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0291_VERSION


@dataclass
class AdapterDisabledReason(ModelMixin):
    reason_id: str
    adapter_name: str
    disabled: bool
    disabled_reason_type: str
    disabled_reason_summary: str
    required_followup_version: str | None
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0291_VERSION


@dataclass
class AdapterDependencyBoundaryReport(ModelMixin):
    report_id: str
    adapter_name: str
    provider_sdk_required_later: bool
    optional_dependency_group_required_later: bool
    dependency_boundary_status: str
    provider_sdk_required_now: bool = False
    provider_sdk_runtime_dependency_added_now: bool = False
    private_sdk_detected: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0291_VERSION


@dataclass
class AdapterRiskProfile(ModelMixin):
    risk_profile_id: str
    adapter_name: str
    risk_level: str
    risk_dimensions: list[str]
    blocker_count: int
    warning_count: int
    risk_summary: str
    blocks_registry: bool
    blocks_implementation: bool = True
    blocks_invocation: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0291_VERSION


@dataclass
class AdapterPermissionScopeRequirement(ModelMixin):
    requirement_id: str
    adapter_name: str
    permission_scope_required: bool
    scope_kind: str
    scope_limited_required: bool = True
    expiry_required: bool = True
    approval_record_required: bool = True
    permission_gate_future_version: str = "v0.29.3"
    permission_granted_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0291_VERSION


@dataclass
class AdapterSafetyScopeRequirement(ModelMixin):
    requirement_id: str
    adapter_name: str
    safety_scope_required: bool
    safety_scope_kind: str
    safety_gate_future_version: str = "v0.29.3"
    safety_gate_passed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0291_VERSION


@dataclass
class AdapterCredentialNeedDeclaration(ModelMixin):
    declaration_id: str
    adapter_name: str
    credentials_required_later: bool
    credential_kind: str
    secret_reference_required_later: bool
    credential_value_stored_now: bool = False
    credential_value_logged_now: bool = False
    env_file_created_now: bool = False
    credential_boundary_future_version: str = "v0.29.4"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0291_VERSION


@dataclass
class AdapterNetworkNeedDeclaration(ModelMixin):
    declaration_id: str
    adapter_name: str
    network_required_later: bool
    network_kind: str
    outbound_domain_policy_required_later: bool
    network_access_enabled_now: bool = False
    network_called_now: bool = False
    network_boundary_future_version: str = "v0.29.4"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0291_VERSION


@dataclass
class AdapterOCELVisibilityDeclaration(ModelMixin):
    declaration_id: str
    adapter_name: str
    declared_events: list[str]
    missing_required_events: list[str]
    ocel_visibility_status: str
    ocel_visibility_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0291_VERSION


@dataclass
class AdapterRegistryEntry(ModelMixin):
    registry_entry_id: str
    adapter_name: str
    adapter_kind: str
    provider_kind: str
    contract_ref: dict[str, Any] | None
    capability_declaration_refs: list[dict[str, Any]]
    availability_status_ref: dict[str, Any] | None
    readiness_status_ref: dict[str, Any] | None
    disabled_reason_ref: dict[str, Any] | None
    risk_profile_ref: dict[str, Any] | None
    dependency_boundary_report_ref: dict[str, Any] | None
    permission_scope_requirement_ref: dict[str, Any] | None
    safety_scope_requirement_ref: dict[str, Any] | None
    credential_need_declaration_ref: dict[str, Any] | None
    network_need_declaration_ref: dict[str, Any] | None
    ocel_visibility_declaration_ref: dict[str, Any] | None
    registry_status: str
    registry_entry_is_provider_registration: bool = False
    adapter_implemented_now: bool = False
    provider_registered_now: bool = False
    provider_invoked_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0291_VERSION


@dataclass
class AdapterRegistry(ModelMixin):
    registry_id: str
    policy_ref: dict[str, Any]
    entries: list[AdapterRegistryEntry]
    entry_count: int
    available_entry_count: int
    gated_entry_count: int
    disabled_entry_count: int
    future_track_entry_count: int
    blocked_entry_count: int
    unknown_entry_count: int
    registry_status: str
    provider_registered_now: bool = False
    provider_invoked_now: bool = False
    adapter_implemented_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0291_VERSION


@dataclass
class AdapterRegistryGate(ModelMixin):
    gate_id: str
    contract_report_ref: dict[str, Any] | None
    provider_capability_inventory_ref: dict[str, Any]
    adapter_registry_ref: dict[str, Any]
    capability_declarations_complete: bool
    availability_statuses_complete: bool
    readiness_statuses_complete: bool
    risk_profiles_complete: bool
    permission_requirements_complete: bool
    safety_requirements_complete: bool
    credential_need_declarations_complete: bool
    network_need_declarations_complete: bool
    ocel_visibility_declarations_complete: bool
    no_provider_registration: bool
    no_provider_invocation: bool
    no_network_call: bool
    no_credential_storage: bool
    no_command_execution: bool
    gate_status: str
    ready_for_v0_29_2: bool
    ready_for_adapter_implementation: bool = False
    ready_for_provider_registration: bool = False
    ready_for_provider_invocation: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0291_VERSION


@dataclass
class AdapterRegistryFinding(ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class AdapterRegistryReport(ModelMixin):
    report_id: str
    created_at: str
    inventory_policy: ProviderCapabilityInventoryPolicy
    registry_policy: AdapterRegistryPolicy
    provider_kind_catalog: ProviderKindCatalog
    provider_capability_inventory: ProviderCapabilityInventory
    adapter_registry: AdapterRegistry
    capability_declarations: list[AdapterCapabilityDeclaration]
    availability_statuses: list[AdapterAvailabilityStatus]
    readiness_statuses: list[AdapterReadinessStatus]
    disabled_reasons: list[AdapterDisabledReason]
    dependency_boundary_reports: list[AdapterDependencyBoundaryReport]
    risk_profiles: list[AdapterRiskProfile]
    permission_scope_requirements: list[AdapterPermissionScopeRequirement]
    safety_scope_requirements: list[AdapterSafetyScopeRequirement]
    credential_need_declarations: list[AdapterCredentialNeedDeclaration]
    network_need_declarations: list[AdapterNetworkNeedDeclaration]
    ocel_visibility_declarations: list[AdapterOCELVisibilityDeclaration]
    registry_gate: AdapterRegistryGate
    findings: list[AdapterRegistryFinding]
    report_status: str
    ready_for_v0_29_2: bool
    ready_for_mock_harness: bool
    ready_for_adapter_implementation: bool = False
    ready_for_provider_registration: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_command_execution: bool = False
    adapter_implemented: bool = False
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
    next_required_step: str = V0291_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.29.2 Mock Adapter Harness / No-Network Default begins or Adapter Registry policy changes."
    version: str = V0291_VERSION


class AdapterRegistryPrerequisiteSourceService:
    def _contract_parts(self) -> dict[str, Any]:
        return ExternalAdapterContractReportService().build_all_parts()

    def load_v0290_external_adapter_contract_report(self) -> dict[str, Any] | None:
        return _ref("external_adapter_contract_report", "external_adapter_contract_report:v0.29.0", "v0.29.0")

    def load_external_provider_adapter_contract(self) -> dict[str, Any] | None:
        return _ref("external_provider_adapter_contract", "external_provider_adapter_contract:v0.29.0", "v0.29.0")

    def load_external_skill_adapter_contract(self) -> dict[str, Any] | None:
        return _ref("external_skill_adapter_contract", "external_skill_adapter_contract:v0.29.0", "v0.29.0")

    def load_adapter_lifecycle_contract(self) -> dict[str, Any] | None:
        return _ref("adapter_lifecycle_contract", "adapter_lifecycle_contract:v0.29.0", "v0.29.0")

    def load_adapter_capability_contract(self) -> dict[str, Any] | None:
        return _ref("adapter_capability_contract", "adapter_capability_contract:v0.29.0", "v0.29.0")

    def load_adapter_schema_contracts(self) -> list[dict[str, Any]]:
        return [_ref("adapter_input_schema_contract", "adapter_input_schema_contract:v0.29.0", "v0.29.0"), _ref("adapter_output_schema_contract", "adapter_output_schema_contract:v0.29.0", "v0.29.0")]

    def load_adapter_effect_boundary_contract(self) -> dict[str, Any] | None:
        return _ref("adapter_effect_boundary_contract", "adapter_effect_boundary_contract:v0.29.0", "v0.29.0")

    def load_adapter_permission_safety_credential_network_audit_rollback_ocel_contracts(self) -> list[dict[str, Any]]:
        names = ["permission", "safety", "credential", "network", "audit", "rollback_noop", "ocel_visibility", "mock_no_network", "certification"]
        return [_ref(f"adapter_{name}_contract", f"adapter_{name}_contract:v0.29.0", "v0.29.0") for name in names]

    def load_provider_invocation_prohibition_contract(self) -> dict[str, Any] | None:
        return _ref("provider_invocation_prohibition_contract", "provider_invocation_prohibition_contract:v0.29.0", "v0.29.0")

    def load_command_execution_prohibition_contract(self) -> dict[str, Any] | None:
        return _ref("command_execution_prohibition_contract", "command_execution_prohibition_contract:v0.29.0", "v0.29.0")

    def load_v0289_handoff_packet_if_available(self) -> dict[str, Any] | None:
        return _ref("external_adapter_contract_handoff_packet", "external_adapter_contract_handoff_packet:v0.28.9", "v0.28.9")

    def load_ocel_pig_ocpx_metadata_if_available(self) -> list[dict[str, Any]]:
        return [_ref("pig_report", "external_provider_adapter_contract:pig:v0.29.0", "v0.29.0"), _ref("ocpx_projection", "external_provider_adapter_contract:ocpx:v0.29.0", "v0.29.0")]


class ProviderCapabilityInventoryPolicyService:
    def build_policy(self) -> ProviderCapabilityInventoryPolicy:
        return ProviderCapabilityInventoryPolicy("provider_capability_inventory_policy:v0.29.1")


class AdapterRegistryPolicyService:
    def build_policy(self) -> AdapterRegistryPolicy:
        return AdapterRegistryPolicy("adapter_registry_policy:v0.29.1")


class ProviderKindCatalogService:
    PROVIDER_KINDS = [
        ("llm_provider", "Generic LLM provider kind.", True, True, True, "v0.29.4"),
        ("search_provider", "Generic search provider kind.", True, False, True, "v0.29.4"),
        ("storage_provider", "Generic storage provider kind.", True, True, True, "v0.29.4"),
        ("calendar_provider", "Generic calendar provider kind.", True, True, True, "v0.29.4"),
        ("email_provider", "Generic email provider kind.", True, True, True, "v0.29.4"),
        ("workflow_provider", "Generic workflow provider kind.", True, True, True, "v0.29.5"),
        ("rpa_provider", "RPA provider kind deferred to future track.", True, True, True, "v0.29.7"),
        ("internal_mock_provider", "Internal mock provider kind for future no-network harness.", False, False, False, "v0.29.2"),
        ("local_file_provider", "Local file provider kind remains disabled for external adapter track.", False, False, True, "v0.29.3"),
        ("unknown", "Unknown provider kind is not available.", False, False, True, None),
    ]

    def build_catalog(self) -> ProviderKindCatalog:
        records = [
            ProviderKindRecord(f"provider_kind_record:{kind}:v0.29.1", kind, summary, kind == "internal_mock_provider", network, credential, future, gate)
            for kind, summary, network, credential, future, gate in self.PROVIDER_KINDS
        ]
        return ProviderKindCatalog("provider_kind_catalog:v0.29.1", records, len(records), "ready")


class ProviderCapabilityRecordService:
    def build_records(self) -> list[ProviderCapabilityRecord]:
        return [
            ProviderCapabilityRecord("provider_capability_record:internal_mock_response:v0.29.1", "internal_mock_provider", "mock_response", "Deterministic mock response capability for the future no-network harness.", "mock_response", "available", True, False, False, False, False, False, False, False, "none", "safe_read_only", "v0.29.2"),
            ProviderCapabilityRecord("provider_capability_record:llm_completion:v0.29.1", "llm_provider", "llm_completion", "Future LLM provider completion capability declaration.", "read", "gated", True, True, True, True, True, False, False, False, "read_only", "external_read", "v0.29.8"),
            ProviderCapabilityRecord("provider_capability_record:search_query:v0.29.1", "search_provider", "search_query", "Future search provider query capability declaration.", "search", "gated", True, True, True, True, False, False, False, False, "read_only", "external_read", "v0.29.8"),
            ProviderCapabilityRecord("provider_capability_record:workflow_action:v0.29.1", "workflow_provider", "workflow_action", "Future workflow action capability declaration.", "execute_workflow", "blocked", False, True, True, True, True, False, False, False, "external_side_effect", "external_side_effect", "v0.29.8"),
            ProviderCapabilityRecord("provider_capability_record:rpa_action:v0.29.1", "rpa_provider", "rpa_action", "RPA action declaration remains future-track and blocked.", "rpa_action", "future_track", False, True, True, True, True, True, False, False, "rpa_action", "rpa_sensitive", "v0.29.8"),
            ProviderCapabilityRecord("provider_capability_record:unknown:v0.29.1", "unknown", "unknown", "Unknown capability status is not available.", "unknown", "unknown", False, False, False, False, False, False, False, False, None, None, None),
        ]


class ProviderCapabilityInventoryService:
    def build_inventory(self, policy: ProviderCapabilityInventoryPolicy, catalog: ProviderKindCatalog) -> ProviderCapabilityInventory:
        records = ProviderCapabilityRecordService().build_records()
        counts = {status: sum(1 for record in records if record.capability_status == status) for status in ["available", "gated", "disabled", "future_track", "blocked", "unknown"]}
        return ProviderCapabilityInventory("provider_capability_inventory:v0.29.1", _ref("provider_capability_inventory_policy", policy.policy_id, V0291_VERSION), _ref("provider_kind_catalog", catalog.catalog_id, V0291_VERSION), records, len(records), counts["available"], counts["gated"], counts["disabled"], counts["future_track"], counts["blocked"], counts["unknown"], "warning")


ADAPTER_NAMES = ["internal_mock_adapter", "generic_llm_adapter", "generic_search_adapter", "generic_workflow_adapter", "generic_rpa_adapter"]
ADAPTER_PROVIDER_KIND = {
    "internal_mock_adapter": "internal_mock_provider",
    "generic_llm_adapter": "llm_provider",
    "generic_search_adapter": "search_provider",
    "generic_workflow_adapter": "workflow_provider",
    "generic_rpa_adapter": "rpa_provider",
}
ADAPTER_KIND = {
    "internal_mock_adapter": "internal_mock_adapter",
    "generic_llm_adapter": "generic_llm_adapter",
    "generic_search_adapter": "generic_search_adapter",
    "generic_workflow_adapter": "generic_workflow_adapter",
    "generic_rpa_adapter": "generic_rpa_adapter",
}
ADAPTER_STATUS = {
    "internal_mock_adapter": "available",
    "generic_llm_adapter": "gated",
    "generic_search_adapter": "gated",
    "generic_workflow_adapter": "blocked",
    "generic_rpa_adapter": "future_track",
}


class AdapterCapabilityDeclarationService:
    def build_declarations(self) -> list[AdapterCapabilityDeclaration]:
        source = AdapterRegistryPrerequisiteSourceService()
        schema_refs = source.load_adapter_schema_contracts()
        effect_ref = source.load_adapter_effect_boundary_contract()
        declarations: list[AdapterCapabilityDeclaration] = []
        for name in ADAPTER_NAMES:
            provider_kind = ADAPTER_PROVIDER_KIND[name]
            status = "declared" if name == "internal_mock_adapter" else "warning"
            declarations.append(AdapterCapabilityDeclaration(f"adapter_capability_declaration:{name}:v0.29.1", name, provider_kind, f"{name}_capability", f"{name} metadata-only capability declaration.", schema_refs[0], schema_refs[1], effect_ref, "low" if name == "internal_mock_adapter" else "high", "none" if name == "internal_mock_adapter" else "read_only", "safe_read_only" if name == "internal_mock_adapter" else "external_read", name != "internal_mock_adapter", name != "internal_mock_adapter", True, True, True, status))
        return declarations


class AdapterStatusService:
    def build_availability_statuses(self) -> list[AdapterAvailabilityStatus]:
        return [AdapterAvailabilityStatus(f"adapter_availability_status:{name}:v0.29.1", name, ADAPTER_STATUS[name], f"{name} is metadata-only; status does not grant implementation or invocation.", True) for name in ADAPTER_NAMES]

    def build_readiness_statuses(self) -> list[AdapterReadinessStatus]:
        return [AdapterReadinessStatus(f"adapter_readiness_status:{name}:v0.29.1", name, True, True, True, ADAPTER_STATUS[name]) for name in ADAPTER_NAMES]

    def build_disabled_reasons(self) -> list[AdapterDisabledReason]:
        reasons = {
            "internal_mock_adapter": ("none", "Internal mock metadata is available for registry only.", "v0.29.2", False),
            "generic_llm_adapter": ("missing_mock_harness", "Live LLM adapter requires mock harness and later gates.", "v0.29.2", True),
            "generic_search_adapter": ("missing_mock_harness", "Live search adapter requires mock harness and later gates.", "v0.29.2", True),
            "generic_workflow_adapter": ("missing_safety_gate", "Workflow side effects require safety and approval gates.", "v0.29.3", True),
            "generic_rpa_adapter": ("RPA_future_track", "RPA remains future-track and disabled.", "v0.29.7", True),
        }
        return [AdapterDisabledReason(f"adapter_disabled_reason:{name}:v0.29.1", name, disabled, reason_type, summary, followup) for name, (reason_type, summary, followup, disabled) in reasons.items()]


class AdapterDependencyBoundaryReportService:
    def build_reports(self) -> list[AdapterDependencyBoundaryReport]:
        return [AdapterDependencyBoundaryReport(f"adapter_dependency_boundary_report:{name}:v0.29.1", name, name != "internal_mock_adapter", name != "internal_mock_adapter", "passed" if name == "internal_mock_adapter" else "warning") for name in ADAPTER_NAMES]


class AdapterRiskProfileService:
    def build_profiles(self) -> list[AdapterRiskProfile]:
        profiles = []
        for name in ADAPTER_NAMES:
            risk_level = "low" if name == "internal_mock_adapter" else "high"
            blocker_count = 0 if name == "internal_mock_adapter" else 1
            warning_count = 0 if name == "internal_mock_adapter" else 2
            profiles.append(AdapterRiskProfile(f"adapter_risk_profile:{name}:v0.29.1", name, risk_level, list(RISK_DIMENSIONS), blocker_count, warning_count, f"{name} risk profile is metadata-only and blocks implementation/invocation.", False if name == "internal_mock_adapter" else True))
        return profiles


class AdapterRequirementDeclarationService:
    def build_permission_scope_requirements(self) -> list[AdapterPermissionScopeRequirement]:
        return [AdapterPermissionScopeRequirement(f"adapter_permission_scope_requirement:{name}:v0.29.1", name, name != "internal_mock_adapter", "none" if name == "internal_mock_adapter" else "read_only") for name in ADAPTER_NAMES]

    def build_safety_scope_requirements(self) -> list[AdapterSafetyScopeRequirement]:
        return [AdapterSafetyScopeRequirement(f"adapter_safety_scope_requirement:{name}:v0.29.1", name, name != "internal_mock_adapter", "safe_read_only" if name == "internal_mock_adapter" else "external_read") for name in ADAPTER_NAMES]

    def build_credential_need_declarations(self) -> list[AdapterCredentialNeedDeclaration]:
        return [AdapterCredentialNeedDeclaration(f"adapter_credential_need_declaration:{name}:v0.29.1", name, name not in {"internal_mock_adapter", "generic_search_adapter"}, "none" if name == "internal_mock_adapter" else "api_key", name != "internal_mock_adapter") for name in ADAPTER_NAMES]

    def build_network_need_declarations(self) -> list[AdapterNetworkNeedDeclaration]:
        return [AdapterNetworkNeedDeclaration(f"adapter_network_need_declaration:{name}:v0.29.1", name, name != "internal_mock_adapter", "none" if name == "internal_mock_adapter" else "outbound_https", name != "internal_mock_adapter") for name in ADAPTER_NAMES]

    def build_ocel_visibility_declarations(self) -> list[AdapterOCELVisibilityDeclaration]:
        return [AdapterOCELVisibilityDeclaration(f"adapter_ocel_visibility_declaration:{name}:v0.29.1", name, list(REQUIRED_OCEL_EVENTS), [], "passed") for name in ADAPTER_NAMES]


class AdapterRegistryEntryService:
    def build_entries(
        self,
        declarations: list[AdapterCapabilityDeclaration],
        availability: list[AdapterAvailabilityStatus],
        readiness: list[AdapterReadinessStatus],
        disabled: list[AdapterDisabledReason],
        dependencies: list[AdapterDependencyBoundaryReport],
        risks: list[AdapterRiskProfile],
        permissions: list[AdapterPermissionScopeRequirement],
        safety: list[AdapterSafetyScopeRequirement],
        credentials: list[AdapterCredentialNeedDeclaration],
        networks: list[AdapterNetworkNeedDeclaration],
        ocels: list[AdapterOCELVisibilityDeclaration],
    ) -> list[AdapterRegistryEntry]:
        by_name = lambda items, attr: {getattr(item, attr): item for item in items}
        decl = by_name(declarations, "adapter_name")
        av = by_name(availability, "adapter_name")
        ready = by_name(readiness, "adapter_name")
        dis = by_name(disabled, "adapter_name")
        dep = by_name(dependencies, "adapter_name")
        risk = by_name(risks, "adapter_name")
        perm = by_name(permissions, "adapter_name")
        safe = by_name(safety, "adapter_name")
        cred = by_name(credentials, "adapter_name")
        net = by_name(networks, "adapter_name")
        ocel = by_name(ocels, "adapter_name")
        contract_ref = AdapterRegistryPrerequisiteSourceService().load_external_provider_adapter_contract()
        return [
            AdapterRegistryEntry(
                f"adapter_registry_entry:{name}:v0.29.1",
                name,
                ADAPTER_KIND[name],
                ADAPTER_PROVIDER_KIND[name],
                contract_ref,
                [_ref("adapter_capability_declaration", decl[name].declaration_id, V0291_VERSION)],
                _ref("adapter_availability_status", av[name].status_id, V0291_VERSION),
                _ref("adapter_readiness_status", ready[name].status_id, V0291_VERSION),
                _ref("adapter_disabled_reason", dis[name].reason_id, V0291_VERSION),
                _ref("adapter_risk_profile", risk[name].risk_profile_id, V0291_VERSION),
                _ref("adapter_dependency_boundary_report", dep[name].report_id, V0291_VERSION),
                _ref("adapter_permission_scope_requirement", perm[name].requirement_id, V0291_VERSION),
                _ref("adapter_safety_scope_requirement", safe[name].requirement_id, V0291_VERSION),
                _ref("adapter_credential_need_declaration", cred[name].declaration_id, V0291_VERSION),
                _ref("adapter_network_need_declaration", net[name].declaration_id, V0291_VERSION),
                _ref("adapter_ocel_visibility_declaration", ocel[name].declaration_id, V0291_VERSION),
                ADAPTER_STATUS[name],
            )
            for name in ADAPTER_NAMES
        ]


class AdapterRegistryService:
    def build_registry(self, policy: AdapterRegistryPolicy, entries: list[AdapterRegistryEntry]) -> AdapterRegistry:
        counts = {status: sum(1 for entry in entries if entry.registry_status == status) for status in ["available", "gated", "disabled", "future_track", "blocked", "unknown"]}
        return AdapterRegistry("adapter_registry:v0.29.1", _ref("adapter_registry_policy", policy.policy_id, V0291_VERSION), entries, len(entries), counts["available"], counts["gated"], counts["disabled"], counts["future_track"], counts["blocked"], counts["unknown"], "warning")


class AdapterRegistryGateService:
    def evaluate_gate(self, inventory: ProviderCapabilityInventory, registry: AdapterRegistry, contract_ref: dict[str, Any] | None) -> AdapterRegistryGate:
        complete = registry.entry_count > 0 and inventory.capability_count > 0
        return AdapterRegistryGate(
            "adapter_registry_gate:v0.29.1",
            contract_ref,
            _ref("provider_capability_inventory", inventory.inventory_id, V0291_VERSION),
            _ref("adapter_registry", registry.registry_id, V0291_VERSION),
            complete,
            complete,
            complete,
            complete,
            complete,
            complete,
            complete,
            complete,
            complete,
            True,
            True,
            True,
            True,
            True,
            "warning",
            complete,
        )


class AdapterRegistryFindingService:
    BLOCKED_FINDINGS = {
        "adapter_implementation_attempted",
        "provider_registration_attempted",
        "provider_invocation_attempted",
        "provider_sdk_invocation_attempted",
        "network_call_attempted",
        "credential_storage_attempted",
        "credential_logging_attempted",
        "env_file_creation_attempted",
        "command_execution_attempted",
        "shell_execution_attempted",
        "shell_true_detected",
        "unbounded_subprocess_detected",
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

    def build_findings(self) -> list[AdapterRegistryFinding]:
        return [
            AdapterRegistryFinding("adapter_registry_finding:inventory_policy_created:v0.29.1", "info", "provider_capability_inventory_policy_created", "Provider capability inventory policy created as metadata only.", _ref("provider_capability_inventory_policy", "provider_capability_inventory_policy:v0.29.1", V0291_VERSION), [], None),
            AdapterRegistryFinding("adapter_registry_finding:registry_created:v0.29.1", "info", "adapter_registry_created", "Adapter registry created without provider registration or execution.", _ref("adapter_registry", "adapter_registry:v0.29.1", V0291_VERSION), [], "Withdraw if registry entries are treated as provider registration."),
            AdapterRegistryFinding("adapter_registry_finding:registry_gate_created:v0.29.1", "warning", "adapter_registry_gate_created", "Registry gate is evaluated for v0.29.2 mock harness readiness only; provider invocation remains false.", _ref("adapter_registry_gate", "adapter_registry_gate:v0.29.1", V0291_VERSION), [], "Withdraw if ready_for_provider_invocation becomes true."),
        ]


class AdapterRegistryReportService:
    def build_report(self, report_id: str | None = None) -> AdapterRegistryReport:
        source = AdapterRegistryPrerequisiteSourceService()
        inventory_policy = ProviderCapabilityInventoryPolicyService().build_policy()
        registry_policy = AdapterRegistryPolicyService().build_policy()
        catalog = ProviderKindCatalogService().build_catalog()
        inventory = ProviderCapabilityInventoryService().build_inventory(inventory_policy, catalog)
        declarations = AdapterCapabilityDeclarationService().build_declarations()
        status_service = AdapterStatusService()
        availability = status_service.build_availability_statuses()
        readiness = status_service.build_readiness_statuses()
        disabled = status_service.build_disabled_reasons()
        dependencies = AdapterDependencyBoundaryReportService().build_reports()
        risks = AdapterRiskProfileService().build_profiles()
        req_service = AdapterRequirementDeclarationService()
        permissions = req_service.build_permission_scope_requirements()
        safety = req_service.build_safety_scope_requirements()
        credentials = req_service.build_credential_need_declarations()
        networks = req_service.build_network_need_declarations()
        ocels = req_service.build_ocel_visibility_declarations()
        entries = AdapterRegistryEntryService().build_entries(declarations, availability, readiness, disabled, dependencies, risks, permissions, safety, credentials, networks, ocels)
        registry = AdapterRegistryService().build_registry(registry_policy, entries)
        gate = AdapterRegistryGateService().evaluate_gate(inventory, registry, source.load_v0290_external_adapter_contract_report())
        findings = AdapterRegistryFindingService().build_findings()
        return AdapterRegistryReport(
            report_id or "adapter_registry_report:v0.29.1",
            _now(),
            inventory_policy,
            registry_policy,
            catalog,
            inventory,
            registry,
            declarations,
            availability,
            readiness,
            disabled,
            dependencies,
            risks,
            permissions,
            safety,
            credentials,
            networks,
            ocels,
            gate,
            findings,
            "warning",
            gate.ready_for_v0_29_2,
            True,
            limitations=["v0.29.1 is inventory/registry-only; mock harness, permission/safety gates, credential/network boundaries, dry-run, approval, certification, and limited invocation remain future versions."],
            withdrawal_conditions=["Withdraw if registry entries become provider registration, capability declarations become permission/invocation, unknown statuses become available, provider SDK runtime dependencies are added, or adapter/provider/network/credential/command behavior appears."],
        )

    def build_all_parts(self, report_id: str | None = None) -> dict[str, Any]:
        report = self.build_report(report_id=report_id)
        return {
            "policy": report.inventory_policy,
            "registry-policy": report.registry_policy,
            "provider-kinds": report.provider_kind_catalog,
            "inventory": report.provider_capability_inventory,
            "capabilities": report.provider_capability_inventory.capability_records,
            "entries": report.adapter_registry,
            "declarations": report.capability_declarations,
            "availability": report.availability_statuses,
            "readiness": report.readiness_statuses,
            "disabled-reasons": report.disabled_reasons,
            "dependencies": report.dependency_boundary_reports,
            "risks": report.risk_profiles,
            "permission-requirements": report.permission_scope_requirements,
            "safety-requirements": report.safety_scope_requirements,
            "credential-needs": report.credential_need_declarations,
            "network-needs": report.network_need_declarations,
            "ocel-visibility": report.ocel_visibility_declarations,
            "gate": report.registry_gate,
            "findings": report.findings,
            "report": report,
        }

    def build_pig_report(self) -> dict[str, Any]:
        report = self.build_report()
        return {
            "version": V0291_VERSION,
            "layer": V0291_LAYER,
            "subject": "provider_capability_inventory_adapter_registry",
            "principles": [
                "Inventory is not implementation",
                "Registry is not execution",
                "Adapter registry entry is not provider registration",
                "Provider availability is not invocation readiness",
                "Capability declaration is not permission",
                "Capability status is not approval",
                "Provider kind catalog is not provider SDK dependency",
                "Adapter readiness is not network access",
                "Credential need declaration is not credential storage",
                "Network need declaration is not network access",
                "Unknown capability status is not available",
            ],
            "safety_boundary": {
                "adapter_implemented": report.adapter_implemented,
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
            "future_direction": ["v0.29.2 Mock Adapter Harness / No-Network Default", "v0.29.3 Permission / Safety / Scope Gate for External Adapters", "v0.29.4 Credential / Secret / Network Boundary", "v0.29.5 Adapter Invocation Candidate / Dry-Run Plan", "v0.29.6 Provider Invocation Approval / Audit / Rollback Boundary", "v0.29.7 External Skill Packaging / Certification Matrix", "v0.29.8 Limited Provider Invocation Preview Gate", "v0.29.9 External Provider Adapter Foundation Consolidation"],
            "next_step": V0291_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "provider_capability_inventory_adapter_registry_created",
            "version": V0291_VERSION,
            "source_read_models": ["ExternalProviderAdapterContractState", "ExternalSkillAdapterContractState", "AdapterLifecycleContractState", "AdapterCapabilityContractState", "AdapterSchemaContractState", "AdapterEffectBoundaryContractState", "AdapterPermissionRequirementContractState", "AdapterSafetyRequirementContractState", "AdapterCredentialRequirementContractState", "AdapterNetworkRequirementContractState", "AdapterAuditRequirementContractState", "AdapterRollbackNoOpRequirementContractState", "AdapterOCELVisibilityContractState", "AdapterMockNoNetworkRequirementState", "AdapterCertificationRequirementState", "ProviderInvocationProhibitionState", "PigGuidanceState", "OCPXProjectionState"],
            "target_read_models": ["ProviderCapabilityInventoryState", "ProviderCapabilityRecordState", "AdapterRegistryState", "AdapterRegistryEntryState", "AdapterCapabilityDeclarationState", "AdapterAvailabilityStatusState", "AdapterReadinessStatusState", "AdapterDependencyBoundaryState", "AdapterRiskProfileState", "AdapterRequirementDeclarationState", "AdapterRegistryGateState", "V029ReadinessState"],
            "effect_types": V0291_EFFECT_TYPES,
            "forbidden_effect_types": V0291_FORBIDDEN_EFFECT_TYPES,
        }


def render_adapter_registry_cli(parts: dict[str, Any], section: str = "report") -> str:
    report: AdapterRegistryReport = parts["report"]
    lines = [
        f"Provider Capability Inventory / Adapter Registry {section}",
        f"version={report.version}",
        f"layer={report.inventory_policy.layer}",
        f"report_status={report.report_status}",
        f"ready_for_v0_29_2={_bool(report.ready_for_v0_29_2)}",
        f"ready_for_mock_harness={_bool(report.ready_for_mock_harness)}",
        f"ready_for_adapter_implementation={_bool(report.ready_for_adapter_implementation)}",
        f"ready_for_provider_registration={_bool(report.ready_for_provider_registration)}",
        f"ready_for_provider_invocation={_bool(report.ready_for_provider_invocation)}",
        f"ready_for_network_access={_bool(report.ready_for_network_access)}",
        f"ready_for_command_execution={_bool(report.ready_for_command_execution)}",
        f"adapter_implemented={_bool(report.adapter_implemented)}",
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
