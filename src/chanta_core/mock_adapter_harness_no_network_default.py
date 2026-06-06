from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.external_provider_adapter_contract import ModelMixin, _bool, _ref
from chanta_core.provider_capability_inventory_adapter_registry import (
    AdapterRegistryReport,
    AdapterRegistryReportService,
)
from chanta_core.utility.time import utc_now_iso


V0292_VERSION = "v0.29.2"
V0292_LAYER = "external_provider_adapter"
V0292_TRACK = "External Skill / External Provider Adapter Development"
V0292_NAME = "Mock Adapter Harness / No-Network Default"
V0292_KOREAN_NAME = "Mock Adapter Harness·No-Network 기본값"
V0292_NEXT_STEP = "v0.29.3 Permission / Safety / Scope Gate for External Adapters"

V0292_OBJECT_TYPES = [
    "mock_adapter_harness_policy",
    "mock_adapter_harness_request",
    "mock_adapter_harness_source_view",
    "mock_provider_adapter_contract",
    "mock_adapter_fixture_catalog",
    "deterministic_adapter_fixture",
    "mock_adapter_input_bundle",
    "mock_adapter_response_schema",
    "mock_adapter_response_fixture",
    "mock_input_schema_validation_report",
    "mock_output_schema_validation_report",
    "mock_effect_boundary_validation_report",
    "no_network_adapter_policy",
    "no_network_boundary_report",
    "provider_sdk_isolation_report",
    "mock_credential_boundary_report",
    "mock_adapter_lifecycle_validation_report",
    "mock_adapter_ocel_trace_plan",
    "mock_adapter_ocel_trace_report",
    "mock_adapter_run_plan",
    "mock_adapter_run_report",
    "mock_adapter_harness_gate",
    "mock_adapter_harness_finding",
    "mock_adapter_harness_report",
    "adapter_registry_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

V0292_EVENT_TYPES = [
    "mock_adapter_harness_requested",
    "mock_adapter_harness_prerequisites_loaded",
    "mock_adapter_harness_policy_created",
    "mock_provider_adapter_contract_created",
    "mock_adapter_fixture_catalog_created",
    "deterministic_adapter_fixture_created",
    "mock_adapter_input_bundle_created",
    "mock_adapter_response_schema_created",
    "mock_adapter_response_fixture_created",
    "mock_input_schema_validation_report_created",
    "mock_output_schema_validation_report_created",
    "mock_effect_boundary_validation_report_created",
    "no_network_adapter_policy_created",
    "no_network_boundary_report_created",
    "provider_sdk_isolation_report_created",
    "mock_credential_boundary_report_created",
    "mock_adapter_lifecycle_validation_report_created",
    "mock_adapter_ocel_trace_plan_created",
    "mock_adapter_ocel_trace_report_created",
    "mock_adapter_run_plan_created",
    "mock_adapter_run_report_created",
    "mock_adapter_harness_gate_evaluated",
    "mock_adapter_harness_report_created",
    "mock_adapter_harness_warning_created",
    "mock_adapter_harness_blocked",
]

V0292_EFFECT_TYPES = [
    "read_only_observation",
    "mock_adapter_harness_created",
    "mock_provider_adapter_contract_created",
    "mock_fixture_created",
    "mock_schema_validation_report_created",
    "no_network_boundary_report_created",
    "provider_sdk_isolation_report_created",
    "mock_credential_boundary_report_created",
    "mock_adapter_run_report_created",
    "mock_adapter_ocel_trace_created",
    "mock_adapter_harness_gate_evaluated",
    "state_candidate_created",
]

V0292_FORBIDDEN_EFFECT_TYPES = [
    "live_adapter_implemented",
    "external_provider_adapter_implemented",
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

MOCK_REQUIRED_EVENT_TYPES = [
    "mock_adapter_declared",
    "mock_fixture_loaded",
    "mock_input_validated",
    "mock_response_generated",
    "mock_output_validated",
    "mock_effect_boundary_checked",
    "mock_run_completed",
]

MOCK_REQUIRED_OBJECT_TYPES = [
    "mock_adapter",
    "adapter_fixture",
    "mock_input",
    "mock_response",
    "adapter_registry_entry",
    "adapter_capability",
]


def _now() -> str:
    return utc_now_iso()


def _adapter_names(report: AdapterRegistryReport) -> list[str]:
    return [entry.adapter_name for entry in report.adapter_registry.entries]


def _entry_refs(report: AdapterRegistryReport) -> list[dict[str, Any]]:
    return [_ref("adapter_registry_entry", entry.registry_entry_id, "v0.29.1") for entry in report.adapter_registry.entries]


@dataclass
class MockAdapterHarnessPolicy(ModelMixin):
    policy_id: str
    mock_harness_enabled: bool = True
    no_network_default_required: bool = True
    deterministic_fixture_required: bool = True
    mock_response_schema_required: bool = True
    provider_sdk_isolation_required: bool = True
    credential_free_mock_required: bool = True
    ocel_visible_mock_required: bool = True
    mock_run_is_not_provider_invocation: bool = True
    mock_success_is_not_live_readiness: bool = True
    live_adapter_implementation_enabled_now: bool = False
    provider_registration_enabled_now: bool = False
    provider_invocation_enabled_now: bool = False
    network_access_enabled_now: bool = False
    credential_storage_enabled_now: bool = False
    provider_sdk_invocation_enabled_now: bool = False
    command_execution_expansion_enabled_now: bool = False
    rpa_adapter_enabled_now: bool = False
    external_agent_dominion_enabled_now: bool = False
    schumpeter_private_runtime_enabled_now: bool = False
    actual_user_data_forbidden: bool = True
    actual_company_data_forbidden: bool = True
    raw_provider_output_persistence_forbidden: bool = True
    llm_judge_as_sole_mock_authority_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0292_VERSION
    layer: str = V0292_LAYER


@dataclass
class MockAdapterHarnessRequest(ModelMixin):
    request_id: str
    adapter_registry_report_id: str | None
    adapter_registry_id: str | None
    provider_capability_inventory_id: str | None
    requested_mock_scope: str = "full_mock_harness"
    strictness: str = "standard"
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0292_VERSION


@dataclass
class MockAdapterHarnessSourceView(ModelMixin):
    source_view_id: str
    adapter_registry_report_ref: dict[str, Any] | None
    adapter_registry_ref: dict[str, Any] | None
    provider_capability_inventory_ref: dict[str, Any] | None
    adapter_capability_declaration_refs: list[dict[str, Any]]
    adapter_readiness_status_refs: list[dict[str, Any]]
    adapter_dependency_boundary_refs: list[dict[str, Any]]
    adapter_risk_profile_refs: list[dict[str, Any]]
    adapter_credential_need_refs: list[dict[str, Any]]
    adapter_network_need_refs: list[dict[str, Any]]
    adapter_ocel_visibility_refs: list[dict[str, Any]]
    mock_no_network_contract_ref: dict[str, Any] | None
    input_schema_contract_ref: dict[str, Any] | None
    output_schema_contract_ref: dict[str, Any] | None
    effect_boundary_contract_ref: dict[str, Any] | None
    provider_invocation_prohibition_ref: dict[str, Any] | None
    command_execution_prohibition_ref: dict[str, Any] | None
    source_status: str
    registry_ready_for_mock: bool | None
    live_adapter_detected: bool = False
    provider_invocation_detected: bool = False
    network_call_detected: bool = False
    credential_value_detected: bool = False
    command_execution_detected: bool = False
    raw_provider_output_detected: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0292_VERSION


@dataclass
class MockProviderAdapterContract(ModelMixin):
    contract_id: str
    mock_adapter_name: str
    adapter_registry_entry_ref: dict[str, Any] | None
    provider_kind: str
    capability_refs: list[dict[str, Any]]
    mock_interface_required: bool = True
    deterministic_response_required: bool = True
    no_network_required: bool = True
    no_credentials_required: bool = True
    no_provider_sdk_required: bool = True
    input_schema_validation_required: bool = True
    output_schema_validation_required: bool = True
    effect_boundary_validation_required: bool = True
    ocel_trace_required: bool = True
    live_adapter_implemented_now: bool = False
    provider_invoked_now: bool = False
    network_called_now: bool = False
    credential_used_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0292_VERSION


@dataclass
class DeterministicAdapterFixture(ModelMixin):
    fixture_id: str
    fixture_name: str
    adapter_name: str
    provider_kind: str
    capability_name: str
    input_fixture_ref: dict[str, Any] | None
    output_fixture_ref: dict[str, Any] | None
    deterministic: bool = True
    synthetic_only: bool = True
    contains_actual_user_data: bool = False
    contains_actual_company_data: bool = False
    contains_credentials: bool = False
    contains_raw_provider_output: bool = False
    requires_network: bool = False
    requires_provider_sdk: bool = False
    fixture_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0292_VERSION


@dataclass
class MockAdapterFixtureCatalog(ModelMixin):
    catalog_id: str
    fixtures: list[DeterministicAdapterFixture]
    fixture_count: int
    deterministic_fixture_count: int
    missing_fixture_count: int
    blocked_fixture_count: int
    catalog_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0292_VERSION


@dataclass
class MockAdapterInputBundle(ModelMixin):
    bundle_id: str
    adapter_name: str
    input_refs: list[dict[str, Any]]
    synthetic_input_refs: list[dict[str, Any]]
    schema_ref: dict[str, Any] | None
    input_bundle_status: str
    synthetic_only: bool = True
    contains_private_data: bool = False
    contains_credentials: bool = False
    contains_raw_secret: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0292_VERSION


@dataclass
class MockAdapterResponseSchema(ModelMixin):
    schema_id: str
    adapter_name: str
    capability_name: str
    schema_version: str
    required_fields: list[str]
    optional_fields: list[str]
    error_fields: list[str]
    redaction_boundary_required: bool = True
    raw_provider_output_forbidden: bool = True
    schema_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0292_VERSION


@dataclass
class MockAdapterResponseFixture(ModelMixin):
    response_fixture_id: str
    adapter_name: str
    capability_name: str
    response_schema_ref: dict[str, Any] | None
    fixture_ref: dict[str, Any] | None
    deterministic: bool = True
    synthetic_only: bool = True
    mock_response_is_live_provider_output: bool = False
    contains_raw_provider_output: bool = False
    contains_credentials: bool = False
    response_fixture_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0292_VERSION


@dataclass
class MockInputSchemaValidationReport(ModelMixin):
    report_id: str
    adapter_name: str
    input_bundle_ref: dict[str, Any] | None
    input_schema_contract_ref: dict[str, Any] | None
    input_schema_validated: bool | None
    private_data_boundary_validated: bool | None
    credential_reference_boundary_validated: bool | None
    raw_secret_input_detected: bool = False
    raw_private_payload_detected: bool = False
    validation_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0292_VERSION


@dataclass
class MockOutputSchemaValidationReport(ModelMixin):
    report_id: str
    adapter_name: str
    response_schema_ref: dict[str, Any] | None
    response_fixture_ref: dict[str, Any] | None
    output_schema_validated: bool | None
    output_redaction_boundary_validated: bool | None
    output_error_schema_validated: bool | None
    raw_provider_output_detected: bool = False
    credential_output_detected: bool = False
    validation_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0292_VERSION


@dataclass
class MockEffectBoundaryValidationReport(ModelMixin):
    report_id: str
    adapter_name: str
    effect_boundary_contract_ref: dict[str, Any] | None
    allowed_effects_validated: bool | None
    forbidden_effects_absent: bool
    provider_invoked: bool = False
    network_called: bool = False
    command_executed: bool = False
    credential_stored: bool = False
    external_side_effect_performed: bool = False
    file_mutated_by_adapter: bool = False
    private_data_exfiltrated: bool = False
    validation_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0292_VERSION


@dataclass
class NoNetworkAdapterPolicy(ModelMixin):
    policy_id: str
    no_network_default_required: bool = True
    live_network_disabled_now: bool = True
    outbound_network_forbidden_now: bool = True
    provider_sdk_network_forbidden_now: bool = True
    webhook_forbidden_now: bool = True
    websocket_forbidden_now: bool = True
    internal_network_forbidden_now: bool = True
    network_boundary_future_version: str = "v0.29.4"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0292_VERSION


@dataclass
class NoNetworkBoundaryReport(ModelMixin):
    report_id: str
    adapter_name: str
    no_network_policy_ref: dict[str, Any]
    network_need_declaration_ref: dict[str, Any] | None
    network_access_enabled: bool = False
    network_called: bool = False
    provider_sdk_network_called: bool = False
    outbound_domain_used: bool = False
    no_network_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0292_VERSION


@dataclass
class ProviderSDKIsolationReport(ModelMixin):
    report_id: str
    adapter_name: str
    provider_sdk_required_now: bool = False
    provider_sdk_imported_now: bool = False
    provider_sdk_invoked_now: bool = False
    provider_sdk_runtime_dependency_added_now: bool = False
    provider_sdk_optional_dependency_only_later: bool = True
    sdk_isolation_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0292_VERSION


@dataclass
class MockCredentialBoundaryReport(ModelMixin):
    report_id: str
    adapter_name: str
    credential_need_declaration_ref: dict[str, Any] | None
    credential_required_for_mock: bool = False
    credential_value_stored: bool = False
    credential_value_logged: bool = False
    env_file_created: bool = False
    committed_secret_detected: bool = False
    secret_reference_used_as_value: bool = False
    credential_boundary_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0292_VERSION


@dataclass
class MockAdapterLifecycleValidationReport(ModelMixin):
    report_id: str
    adapter_name: str
    lifecycle_contract_ref: dict[str, Any] | None
    declared_state_validated: bool | None
    mocked_state_validated: bool | None
    certified_mock_state_not_claimed_as_live: bool
    live_preview_state_not_enabled: bool
    lifecycle_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0292_VERSION


@dataclass
class MockAdapterOCELTracePlan(ModelMixin):
    plan_id: str
    adapter_name: str
    required_event_types: list[str]
    required_object_types: list[str]
    ocel_trace_plan_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0292_VERSION


@dataclass
class MockAdapterOCELTraceReport(ModelMixin):
    report_id: str
    adapter_name: str
    trace_plan_ref: dict[str, Any]
    required_events_present: bool | None
    required_objects_present: bool | None
    provider_invocation_event_absent: bool
    network_call_event_absent: bool
    command_execution_event_absent: bool
    ocel_trace_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0292_VERSION


@dataclass
class MockAdapterRunPlan(ModelMixin):
    plan_id: str
    adapter_name: str
    fixture_ref: dict[str, Any] | None
    input_bundle_ref: dict[str, Any] | None
    response_fixture_ref: dict[str, Any] | None
    run_mode: str
    run_allowed_now: bool
    live_provider_allowed: bool = False
    network_allowed: bool = False
    credentials_allowed: bool = False
    command_execution_allowed: bool = False
    file_mutation_allowed: bool = False
    plan_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0292_VERSION


@dataclass
class MockAdapterRunReport(ModelMixin):
    report_id: str
    plan_ref: dict[str, Any]
    adapter_name: str
    run_executed: bool
    run_mode: str
    fixture_loaded: bool | None
    input_validated: bool | None
    mock_response_generated: bool | None
    output_validated: bool | None
    effect_boundary_checked: bool | None
    ocel_trace_created: bool | None
    run_status: str
    live_provider_used: bool = False
    provider_invoked: bool = False
    network_called: bool = False
    credentials_used: bool = False
    command_executed: bool = False
    file_mutated: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0292_VERSION


@dataclass
class MockAdapterHarnessGate(ModelMixin):
    gate_id: str
    registry_report_ref: dict[str, Any] | None
    fixture_catalog_ref: dict[str, Any]
    no_network_boundary_refs: list[dict[str, Any]]
    sdk_isolation_refs: list[dict[str, Any]]
    credential_boundary_refs: list[dict[str, Any]]
    input_validation_refs: list[dict[str, Any]]
    output_validation_refs: list[dict[str, Any]]
    effect_boundary_validation_refs: list[dict[str, Any]]
    ocel_trace_report_refs: list[dict[str, Any]]
    mock_run_report_refs: list[dict[str, Any]]
    deterministic_fixtures_ready: bool
    no_network_boundary_passed: bool
    provider_sdk_isolation_passed: bool
    credential_free_mock_passed: bool
    input_output_schema_passed: bool
    effect_boundary_passed: bool
    ocel_visibility_passed: bool
    mock_run_passed_or_safely_deferred: bool
    gate_status: str
    ready_for_v0_29_3: bool
    ready_for_permission_safety_gate: bool
    ready_for_live_adapter_implementation: bool = False
    ready_for_provider_registration: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_command_execution: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0292_VERSION


@dataclass
class MockAdapterHarnessFinding(ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class MockAdapterHarnessReport(ModelMixin):
    report_id: str
    created_at: str
    policy: MockAdapterHarnessPolicy
    request: MockAdapterHarnessRequest
    source_view: MockAdapterHarnessSourceView
    mock_provider_adapter_contracts: list[MockProviderAdapterContract]
    fixture_catalog: MockAdapterFixtureCatalog
    input_bundles: list[MockAdapterInputBundle]
    response_schemas: list[MockAdapterResponseSchema]
    response_fixtures: list[MockAdapterResponseFixture]
    input_validation_reports: list[MockInputSchemaValidationReport]
    output_validation_reports: list[MockOutputSchemaValidationReport]
    effect_boundary_validation_reports: list[MockEffectBoundaryValidationReport]
    no_network_policy: NoNetworkAdapterPolicy
    no_network_boundary_reports: list[NoNetworkBoundaryReport]
    provider_sdk_isolation_reports: list[ProviderSDKIsolationReport]
    mock_credential_boundary_reports: list[MockCredentialBoundaryReport]
    lifecycle_validation_reports: list[MockAdapterLifecycleValidationReport]
    ocel_trace_plans: list[MockAdapterOCELTracePlan]
    ocel_trace_reports: list[MockAdapterOCELTraceReport]
    mock_run_plans: list[MockAdapterRunPlan]
    mock_run_reports: list[MockAdapterRunReport]
    mock_harness_gate: MockAdapterHarnessGate
    findings: list[MockAdapterHarnessFinding]
    report_status: str
    ready_for_v0_29_3: bool
    ready_for_permission_safety_gate: bool
    ready_for_live_adapter_implementation: bool = False
    ready_for_provider_registration: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_command_execution: bool = False
    live_adapter_implemented: bool = False
    provider_registered: bool = False
    provider_invoked: bool = False
    provider_sdk_invoked: bool = False
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
    next_required_step: str = V0292_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.29.3 Permission / Safety / Scope Gate for External Adapters begins or Mock Adapter Harness policy changes."
    version: str = V0292_VERSION


class MockAdapterHarnessPrerequisiteSourceService:
    def registry_report(self) -> AdapterRegistryReport:
        return AdapterRegistryReportService().build_report()

    def load_v0291_adapter_registry_report(self) -> dict[str, Any] | None:
        return _ref("adapter_registry_report", "adapter_registry_report:v0.29.1", "v0.29.1")

    def load_adapter_registry(self) -> dict[str, Any] | None:
        return _ref("adapter_registry", "adapter_registry:v0.29.1", "v0.29.1")

    def load_provider_capability_inventory(self) -> dict[str, Any] | None:
        return _ref("provider_capability_inventory", "provider_capability_inventory:v0.29.1", "v0.29.1")

    def load_adapter_capability_declarations(self) -> list[dict[str, Any]]:
        return [_ref("adapter_capability_declaration", item.declaration_id, "v0.29.1") for item in self.registry_report().capability_declarations]

    def load_adapter_readiness_statuses(self) -> list[dict[str, Any]]:
        return [_ref("adapter_readiness_status", item.status_id, "v0.29.1") for item in self.registry_report().readiness_statuses]

    def load_adapter_dependency_boundary_reports(self) -> list[dict[str, Any]]:
        return [_ref("adapter_dependency_boundary_report", item.report_id, "v0.29.1") for item in self.registry_report().dependency_boundary_reports]

    def load_adapter_risk_profiles(self) -> list[dict[str, Any]]:
        return [_ref("adapter_risk_profile", item.risk_profile_id, "v0.29.1") for item in self.registry_report().risk_profiles]

    def load_adapter_credential_need_declarations(self) -> list[dict[str, Any]]:
        return [_ref("adapter_credential_need_declaration", item.declaration_id, "v0.29.1") for item in self.registry_report().credential_need_declarations]

    def load_adapter_network_need_declarations(self) -> list[dict[str, Any]]:
        return [_ref("adapter_network_need_declaration", item.declaration_id, "v0.29.1") for item in self.registry_report().network_need_declarations]

    def load_adapter_ocel_visibility_declarations(self) -> list[dict[str, Any]]:
        return [_ref("adapter_ocel_visibility_declaration", item.declaration_id, "v0.29.1") for item in self.registry_report().ocel_visibility_declarations]

    def load_v0290_mock_no_network_requirement_contract(self) -> dict[str, Any] | None:
        return _ref("adapter_mock_no_network_requirement_contract", "adapter_mock_no_network_requirement_contract:v0.29.0", "v0.29.0")

    def load_v0290_input_output_schema_contracts(self) -> list[dict[str, Any]]:
        return [
            _ref("adapter_input_schema_contract", "adapter_input_schema_contract:v0.29.0", "v0.29.0"),
            _ref("adapter_output_schema_contract", "adapter_output_schema_contract:v0.29.0", "v0.29.0"),
        ]

    def load_v0290_effect_boundary_contract(self) -> dict[str, Any] | None:
        return _ref("adapter_effect_boundary_contract", "adapter_effect_boundary_contract:v0.29.0", "v0.29.0")

    def load_v0290_provider_invocation_prohibition_contract(self) -> dict[str, Any] | None:
        return _ref("provider_invocation_prohibition_contract", "provider_invocation_prohibition_contract:v0.29.0", "v0.29.0")

    def load_v0290_command_execution_prohibition_contract(self) -> dict[str, Any] | None:
        return _ref("command_execution_prohibition_contract", "command_execution_prohibition_contract:v0.29.0", "v0.29.0")


class MockAdapterHarnessPolicyService:
    def build_policy(self) -> MockAdapterHarnessPolicy:
        return MockAdapterHarnessPolicy("mock_adapter_harness_policy:v0.29.2")


class MockAdapterHarnessSourceViewService:
    def build_source_view(self) -> MockAdapterHarnessSourceView:
        source = MockAdapterHarnessPrerequisiteSourceService()
        schemas = source.load_v0290_input_output_schema_contracts()
        return MockAdapterHarnessSourceView(
            "mock_adapter_harness_source_view:v0.29.2",
            source.load_v0291_adapter_registry_report(),
            source.load_adapter_registry(),
            source.load_provider_capability_inventory(),
            source.load_adapter_capability_declarations(),
            source.load_adapter_readiness_statuses(),
            source.load_adapter_dependency_boundary_reports(),
            source.load_adapter_risk_profiles(),
            source.load_adapter_credential_need_declarations(),
            source.load_adapter_network_need_declarations(),
            source.load_adapter_ocel_visibility_declarations(),
            source.load_v0290_mock_no_network_requirement_contract(),
            schemas[0],
            schemas[1],
            source.load_v0290_effect_boundary_contract(),
            source.load_v0290_provider_invocation_prohibition_contract(),
            source.load_v0290_command_execution_prohibition_contract(),
            "complete",
            True,
        )


class MockAdapterHarnessRequestService:
    def build_request(self, source_view: MockAdapterHarnessSourceView) -> MockAdapterHarnessRequest:
        return MockAdapterHarnessRequest(
            "mock_adapter_harness_request:v0.29.2",
            source_view.adapter_registry_report_ref["object_id"] if source_view.adapter_registry_report_ref else None,
            source_view.adapter_registry_ref["object_id"] if source_view.adapter_registry_ref else None,
            source_view.provider_capability_inventory_ref["object_id"] if source_view.provider_capability_inventory_ref else None,
            source_refs=[ref for ref in [source_view.adapter_registry_report_ref, source_view.adapter_registry_ref, source_view.provider_capability_inventory_ref] if ref],
        )


class MockProviderAdapterContractService:
    def build_contracts_from_registry(self, registry_report: AdapterRegistryReport) -> list[MockProviderAdapterContract]:
        return [
            MockProviderAdapterContract(
                f"mock_provider_adapter_contract:{entry.adapter_name}:v0.29.2",
                entry.adapter_name,
                _ref("adapter_registry_entry", entry.registry_entry_id, "v0.29.1"),
                entry.provider_kind,
                entry.capability_declaration_refs,
            )
            for entry in registry_report.adapter_registry.entries
        ]


class DeterministicAdapterFixtureService:
    def build_fixtures(self, contracts: list[MockProviderAdapterContract]) -> list[DeterministicAdapterFixture]:
        fixtures = []
        for contract in contracts:
            fixtures.append(
                DeterministicAdapterFixture(
                    f"deterministic_adapter_fixture:{contract.mock_adapter_name}:v0.29.2",
                    f"{contract.mock_adapter_name}_synthetic_fixture",
                    contract.mock_adapter_name,
                    contract.provider_kind,
                    f"{contract.mock_adapter_name}_capability",
                    _ref("mock_adapter_input_bundle", f"mock_adapter_input_bundle:{contract.mock_adapter_name}:v0.29.2", V0292_VERSION),
                    _ref("mock_adapter_response_fixture", f"mock_adapter_response_fixture:{contract.mock_adapter_name}:v0.29.2", V0292_VERSION),
                )
            )
        return fixtures


class MockAdapterFixtureCatalogService:
    def build_catalog(self, fixtures: list[DeterministicAdapterFixture]) -> MockAdapterFixtureCatalog:
        missing = sum(1 for fixture in fixtures if fixture.fixture_status == "unknown")
        blocked = sum(1 for fixture in fixtures if fixture.fixture_status == "blocked")
        deterministic = sum(1 for fixture in fixtures if fixture.deterministic)
        status = "ready" if missing == 0 and blocked == 0 else "warning"
        return MockAdapterFixtureCatalog("mock_adapter_fixture_catalog:v0.29.2", fixtures, len(fixtures), deterministic, missing, blocked, status)


class MockAdapterInputBundleService:
    def build_bundles(self, contracts: list[MockProviderAdapterContract]) -> list[MockAdapterInputBundle]:
        return [
            MockAdapterInputBundle(
                f"mock_adapter_input_bundle:{contract.mock_adapter_name}:v0.29.2",
                contract.mock_adapter_name,
                [_ref("synthetic_mock_input", f"synthetic_mock_input:{contract.mock_adapter_name}:v0.29.2", V0292_VERSION)],
                [_ref("synthetic_mock_input", f"synthetic_mock_input:{contract.mock_adapter_name}:v0.29.2", V0292_VERSION)],
                _ref("adapter_input_schema_contract", "adapter_input_schema_contract:v0.29.0", "v0.29.0"),
                "ready",
            )
            for contract in contracts
        ]


class MockAdapterResponseSchemaService:
    def build_schemas(self, contracts: list[MockProviderAdapterContract]) -> list[MockAdapterResponseSchema]:
        return [
            MockAdapterResponseSchema(
                f"mock_adapter_response_schema:{contract.mock_adapter_name}:v0.29.2",
                contract.mock_adapter_name,
                f"{contract.mock_adapter_name}_capability",
                "mock-schema-v1",
                ["fixture_id", "adapter_name", "result_summary", "status"],
                ["warnings", "redacted_fields"],
                ["error_code", "error_message"],
            )
            for contract in contracts
        ]


class MockAdapterResponseFixtureService:
    def build_fixtures(self, schemas: list[MockAdapterResponseSchema]) -> list[MockAdapterResponseFixture]:
        return [
            MockAdapterResponseFixture(
                f"mock_adapter_response_fixture:{schema.adapter_name}:v0.29.2",
                schema.adapter_name,
                schema.capability_name,
                _ref("mock_adapter_response_schema", schema.schema_id, V0292_VERSION),
                _ref("deterministic_adapter_fixture", f"deterministic_adapter_fixture:{schema.adapter_name}:v0.29.2", V0292_VERSION),
            )
            for schema in schemas
        ]


class MockSchemaValidationService:
    def build_input_validation_reports(self, bundles: list[MockAdapterInputBundle], source_view: MockAdapterHarnessSourceView) -> list[MockInputSchemaValidationReport]:
        return [
            MockInputSchemaValidationReport(
                f"mock_input_schema_validation_report:{bundle.adapter_name}:v0.29.2",
                bundle.adapter_name,
                _ref("mock_adapter_input_bundle", bundle.bundle_id, V0292_VERSION),
                source_view.input_schema_contract_ref,
                True,
                True,
                True,
            )
            for bundle in bundles
        ]

    def build_output_validation_reports(self, schemas: list[MockAdapterResponseSchema], fixtures: list[MockAdapterResponseFixture]) -> list[MockOutputSchemaValidationReport]:
        by_name = {fixture.adapter_name: fixture for fixture in fixtures}
        return [
            MockOutputSchemaValidationReport(
                f"mock_output_schema_validation_report:{schema.adapter_name}:v0.29.2",
                schema.adapter_name,
                _ref("mock_adapter_response_schema", schema.schema_id, V0292_VERSION),
                _ref("mock_adapter_response_fixture", by_name[schema.adapter_name].response_fixture_id, V0292_VERSION),
                True,
                True,
                True,
            )
            for schema in schemas
        ]


class MockEffectBoundaryValidationService:
    def build_reports(self, contracts: list[MockProviderAdapterContract], source_view: MockAdapterHarnessSourceView) -> list[MockEffectBoundaryValidationReport]:
        return [
            MockEffectBoundaryValidationReport(
                f"mock_effect_boundary_validation_report:{contract.mock_adapter_name}:v0.29.2",
                contract.mock_adapter_name,
                source_view.effect_boundary_contract_ref,
                True,
                True,
            )
            for contract in contracts
        ]


class NoNetworkAdapterPolicyService:
    def build_policy(self) -> NoNetworkAdapterPolicy:
        return NoNetworkAdapterPolicy("no_network_adapter_policy:v0.29.2")


class NoNetworkBoundaryReportService:
    def build_reports(self, contracts: list[MockProviderAdapterContract], policy: NoNetworkAdapterPolicy, source_view: MockAdapterHarnessSourceView) -> list[NoNetworkBoundaryReport]:
        network_refs = {ref["object_id"].split(":")[1]: ref for ref in source_view.adapter_network_need_refs if len(ref["object_id"].split(":")) > 1}
        return [
            NoNetworkBoundaryReport(
                f"no_network_boundary_report:{contract.mock_adapter_name}:v0.29.2",
                contract.mock_adapter_name,
                _ref("no_network_adapter_policy", policy.policy_id, V0292_VERSION),
                network_refs.get(contract.mock_adapter_name),
            )
            for contract in contracts
        ]


class ProviderSDKIsolationReportService:
    def build_reports(self, contracts: list[MockProviderAdapterContract]) -> list[ProviderSDKIsolationReport]:
        return [ProviderSDKIsolationReport(f"provider_sdk_isolation_report:{contract.mock_adapter_name}:v0.29.2", contract.mock_adapter_name) for contract in contracts]


class MockCredentialBoundaryReportService:
    def build_reports(self, contracts: list[MockProviderAdapterContract], source_view: MockAdapterHarnessSourceView) -> list[MockCredentialBoundaryReport]:
        credential_refs = {ref["object_id"].split(":")[1]: ref for ref in source_view.adapter_credential_need_refs if len(ref["object_id"].split(":")) > 1}
        return [
            MockCredentialBoundaryReport(
                f"mock_credential_boundary_report:{contract.mock_adapter_name}:v0.29.2",
                contract.mock_adapter_name,
                credential_refs.get(contract.mock_adapter_name),
            )
            for contract in contracts
        ]


class MockAdapterLifecycleValidationReportService:
    def build_reports(self, contracts: list[MockProviderAdapterContract]) -> list[MockAdapterLifecycleValidationReport]:
        lifecycle_ref = _ref("adapter_lifecycle_contract", "adapter_lifecycle_contract:v0.29.0", "v0.29.0")
        return [
            MockAdapterLifecycleValidationReport(
                f"mock_adapter_lifecycle_validation_report:{contract.mock_adapter_name}:v0.29.2",
                contract.mock_adapter_name,
                lifecycle_ref,
                True,
                True,
                True,
                True,
                "passed",
            )
            for contract in contracts
        ]


class MockAdapterOCELTraceService:
    def build_trace_plans(self, contracts: list[MockProviderAdapterContract]) -> list[MockAdapterOCELTracePlan]:
        return [
            MockAdapterOCELTracePlan(
                f"mock_adapter_ocel_trace_plan:{contract.mock_adapter_name}:v0.29.2",
                contract.mock_adapter_name,
                list(MOCK_REQUIRED_EVENT_TYPES),
                list(MOCK_REQUIRED_OBJECT_TYPES),
                "ready",
            )
            for contract in contracts
        ]

    def build_trace_reports(self, plans: list[MockAdapterOCELTracePlan]) -> list[MockAdapterOCELTraceReport]:
        return [
            MockAdapterOCELTraceReport(
                f"mock_adapter_ocel_trace_report:{plan.adapter_name}:v0.29.2",
                plan.adapter_name,
                _ref("mock_adapter_ocel_trace_plan", plan.plan_id, V0292_VERSION),
                True,
                True,
                True,
                True,
                True,
                "passed",
            )
            for plan in plans
        ]


class MockAdapterRunService:
    def build_run_plans(
        self,
        fixtures: list[DeterministicAdapterFixture],
        bundles: list[MockAdapterInputBundle],
        responses: list[MockAdapterResponseFixture],
    ) -> list[MockAdapterRunPlan]:
        by_bundle = {bundle.adapter_name: bundle for bundle in bundles}
        by_response = {response.adapter_name: response for response in responses}
        return [
            MockAdapterRunPlan(
                f"mock_adapter_run_plan:{fixture.adapter_name}:v0.29.2",
                fixture.adapter_name,
                _ref("deterministic_adapter_fixture", fixture.fixture_id, V0292_VERSION),
                _ref("mock_adapter_input_bundle", by_bundle[fixture.adapter_name].bundle_id, V0292_VERSION),
                _ref("mock_adapter_response_fixture", by_response[fixture.adapter_name].response_fixture_id, V0292_VERSION),
                "metadata_only",
                True,
            )
            for fixture in fixtures
        ]

    def build_run_reports(self, plans: list[MockAdapterRunPlan]) -> list[MockAdapterRunReport]:
        return [
            MockAdapterRunReport(
                f"mock_adapter_run_report:{plan.adapter_name}:v0.29.2",
                _ref("mock_adapter_run_plan", plan.plan_id, V0292_VERSION),
                plan.adapter_name,
                True,
                plan.run_mode,
                True,
                True,
                True,
                True,
                True,
                True,
                "passed",
            )
            for plan in plans
        ]


class MockAdapterHarnessGateService:
    def evaluate_gate(
        self,
        registry_report_ref: dict[str, Any] | None,
        fixture_catalog: MockAdapterFixtureCatalog,
        no_network_reports: list[NoNetworkBoundaryReport],
        sdk_reports: list[ProviderSDKIsolationReport],
        credential_reports: list[MockCredentialBoundaryReport],
        input_reports: list[MockInputSchemaValidationReport],
        output_reports: list[MockOutputSchemaValidationReport],
        effect_reports: list[MockEffectBoundaryValidationReport],
        ocel_reports: list[MockAdapterOCELTraceReport],
        run_reports: list[MockAdapterRunReport],
    ) -> MockAdapterHarnessGate:
        deterministic = fixture_catalog.fixture_count > 0 and fixture_catalog.missing_fixture_count == 0 and fixture_catalog.blocked_fixture_count == 0
        no_network = all(not report.network_called and report.no_network_status in {"passed", "warning"} for report in no_network_reports)
        sdk = all(not report.provider_sdk_imported_now and not report.provider_sdk_invoked_now and not report.provider_sdk_runtime_dependency_added_now for report in sdk_reports)
        credential = all(not report.credential_value_stored and not report.credential_value_logged and not report.env_file_created for report in credential_reports)
        schemas = all(report.validation_status in {"passed", "warning"} for report in input_reports + output_reports)
        effects = all(report.forbidden_effects_absent and report.validation_status in {"passed", "warning"} for report in effect_reports)
        ocel = all(report.provider_invocation_event_absent and report.network_call_event_absent and report.command_execution_event_absent for report in ocel_reports)
        runs = all(not report.provider_invoked and not report.network_called and not report.credentials_used and not report.command_executed and not report.file_mutated for report in run_reports)
        ready = deterministic and no_network and sdk and credential and schemas and effects and ocel and runs
        return MockAdapterHarnessGate(
            "mock_adapter_harness_gate:v0.29.2",
            registry_report_ref,
            _ref("mock_adapter_fixture_catalog", fixture_catalog.catalog_id, V0292_VERSION),
            [_ref("no_network_boundary_report", report.report_id, V0292_VERSION) for report in no_network_reports],
            [_ref("provider_sdk_isolation_report", report.report_id, V0292_VERSION) for report in sdk_reports],
            [_ref("mock_credential_boundary_report", report.report_id, V0292_VERSION) for report in credential_reports],
            [_ref("mock_input_schema_validation_report", report.report_id, V0292_VERSION) for report in input_reports],
            [_ref("mock_output_schema_validation_report", report.report_id, V0292_VERSION) for report in output_reports],
            [_ref("mock_effect_boundary_validation_report", report.report_id, V0292_VERSION) for report in effect_reports],
            [_ref("mock_adapter_ocel_trace_report", report.report_id, V0292_VERSION) for report in ocel_reports],
            [_ref("mock_adapter_run_report", report.report_id, V0292_VERSION) for report in run_reports],
            deterministic,
            no_network,
            sdk,
            credential,
            schemas,
            effects,
            ocel,
            runs,
            "warning",
            ready,
            ready,
        )


class MockAdapterHarnessFindingService:
    BLOCKED_FINDINGS = {
        "live_adapter_implementation_attempted",
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

    def build_findings(self) -> list[MockAdapterHarnessFinding]:
        return [
            MockAdapterHarnessFinding("mock_adapter_harness_finding:policy_created:v0.29.2", "info", "mock_harness_policy_created", "Mock adapter harness policy created with no-network default.", _ref("mock_adapter_harness_policy", "mock_adapter_harness_policy:v0.29.2", V0292_VERSION), [], None),
            MockAdapterHarnessFinding("mock_adapter_harness_finding:fixture_catalog_created:v0.29.2", "info", "fixture_catalog_created", "Deterministic synthetic fixture catalog created without live provider output.", _ref("mock_adapter_fixture_catalog", "mock_adapter_fixture_catalog:v0.29.2", V0292_VERSION), [], "Withdraw if fixture data contains actual user/company data or raw provider output."),
            MockAdapterHarnessFinding("mock_adapter_harness_finding:gate_created:v0.29.2", "warning", "mock_harness_gate_created", "Mock harness gate is ready for v0.29.3 only; live adapter/provider/network readiness remains false.", _ref("mock_adapter_harness_gate", "mock_adapter_harness_gate:v0.29.2", V0292_VERSION), [], "Withdraw if ready_for_provider_invocation or ready_for_network_access becomes true."),
        ]


class MockAdapterHarnessReportService:
    def build_report(self, report_id: str | None = None) -> MockAdapterHarnessReport:
        source = MockAdapterHarnessPrerequisiteSourceService()
        registry_report = source.registry_report()
        policy = MockAdapterHarnessPolicyService().build_policy()
        source_view = MockAdapterHarnessSourceViewService().build_source_view()
        request = MockAdapterHarnessRequestService().build_request(source_view)
        contracts = MockProviderAdapterContractService().build_contracts_from_registry(registry_report)
        fixtures = DeterministicAdapterFixtureService().build_fixtures(contracts)
        fixture_catalog = MockAdapterFixtureCatalogService().build_catalog(fixtures)
        input_bundles = MockAdapterInputBundleService().build_bundles(contracts)
        response_schemas = MockAdapterResponseSchemaService().build_schemas(contracts)
        response_fixtures = MockAdapterResponseFixtureService().build_fixtures(response_schemas)
        validation_service = MockSchemaValidationService()
        input_validation_reports = validation_service.build_input_validation_reports(input_bundles, source_view)
        output_validation_reports = validation_service.build_output_validation_reports(response_schemas, response_fixtures)
        effect_boundary_validation_reports = MockEffectBoundaryValidationService().build_reports(contracts, source_view)
        no_network_policy = NoNetworkAdapterPolicyService().build_policy()
        no_network_boundary_reports = NoNetworkBoundaryReportService().build_reports(contracts, no_network_policy, source_view)
        provider_sdk_isolation_reports = ProviderSDKIsolationReportService().build_reports(contracts)
        mock_credential_boundary_reports = MockCredentialBoundaryReportService().build_reports(contracts, source_view)
        lifecycle_validation_reports = MockAdapterLifecycleValidationReportService().build_reports(contracts)
        ocel_service = MockAdapterOCELTraceService()
        ocel_trace_plans = ocel_service.build_trace_plans(contracts)
        ocel_trace_reports = ocel_service.build_trace_reports(ocel_trace_plans)
        run_service = MockAdapterRunService()
        mock_run_plans = run_service.build_run_plans(fixtures, input_bundles, response_fixtures)
        mock_run_reports = run_service.build_run_reports(mock_run_plans)
        gate = MockAdapterHarnessGateService().evaluate_gate(
            source_view.adapter_registry_report_ref,
            fixture_catalog,
            no_network_boundary_reports,
            provider_sdk_isolation_reports,
            mock_credential_boundary_reports,
            input_validation_reports,
            output_validation_reports,
            effect_boundary_validation_reports,
            ocel_trace_reports,
            mock_run_reports,
        )
        findings = MockAdapterHarnessFindingService().build_findings()
        return MockAdapterHarnessReport(
            report_id or "mock_adapter_harness_report:v0.29.2",
            _now(),
            policy,
            request,
            source_view,
            contracts,
            fixture_catalog,
            input_bundles,
            response_schemas,
            response_fixtures,
            input_validation_reports,
            output_validation_reports,
            effect_boundary_validation_reports,
            no_network_policy,
            no_network_boundary_reports,
            provider_sdk_isolation_reports,
            mock_credential_boundary_reports,
            lifecycle_validation_reports,
            ocel_trace_plans,
            ocel_trace_reports,
            mock_run_plans,
            mock_run_reports,
            gate,
            findings,
            "warning",
            gate.ready_for_v0_29_3,
            gate.ready_for_permission_safety_gate,
            limitations=["v0.29.2 validates mock/no-network metadata only. Permission, safety, credential, network, dry-run, approval, certification, and live invocation gates remain future work."],
            withdrawal_conditions=["Withdraw if live adapters, provider registration/invocation, provider SDK calls, network calls, credentials, command execution, private/raw data, or LLM-judge-only authority appear."],
        )

    def build_all_parts(self, report_id: str | None = None) -> dict[str, Any]:
        report = self.build_report(report_id=report_id)
        return {
            "policy": report.policy,
            "request": report.request,
            "source-view": report.source_view,
            "contracts": report.mock_provider_adapter_contracts,
            "fixtures": report.fixture_catalog,
            "inputs": report.input_bundles,
            "response-schema": report.response_schemas,
            "response-fixtures": report.response_fixtures,
            "validate-inputs": report.input_validation_reports,
            "validate-outputs": report.output_validation_reports,
            "validate-effects": report.effect_boundary_validation_reports,
            "no-network": report.no_network_boundary_reports,
            "sdk-isolation": report.provider_sdk_isolation_reports,
            "credentials": report.mock_credential_boundary_reports,
            "lifecycle": report.lifecycle_validation_reports,
            "ocel-plan": report.ocel_trace_plans,
            "ocel-report": report.ocel_trace_reports,
            "run-plan": report.mock_run_plans,
            "run-report": report.mock_run_reports,
            "gate": report.mock_harness_gate,
            "findings": report.findings,
            "report": report,
        }

    def build_pig_report(self) -> dict[str, Any]:
        report = self.build_report()
        return {
            "version": V0292_VERSION,
            "layer": V0292_LAYER,
            "subject": "mock_adapter_harness_no_network_default",
            "principles": [
                "Mock adapter is not real provider",
                "Mock harness is not provider runtime",
                "No-network default is mandatory",
                "Fixture response is not live provider output",
                "Mock response schema validation is not provider invocation",
                "Provider SDK isolation is not provider SDK readiness",
                "Mock run is not external action",
                "Mock OCEL trace is not provider action trace",
                "Credential-free mock is not credential boundary completion",
                "Mock success is not live adapter readiness",
            ],
            "safety_boundary": {
                "live_adapter_implemented": report.live_adapter_implemented,
                "provider_registered": report.provider_registered,
                "provider_invoked": report.provider_invoked,
                "provider_sdk_invoked": report.provider_sdk_invoked,
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
                "v0.29.3 Permission / Safety / Scope Gate for External Adapters",
                "v0.29.4 Credential / Secret / Network Boundary",
                "v0.29.5 Adapter Invocation Candidate / Dry-Run Plan",
                "v0.29.6 Provider Invocation Approval / Audit / Rollback Boundary",
                "v0.29.7 External Skill Packaging / Certification Matrix",
                "v0.29.8 Limited Provider Invocation Preview Gate",
                "v0.29.9 External Provider Adapter Foundation Consolidation",
            ],
            "next_step": V0292_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "mock_adapter_harness_no_network_default_created",
            "version": V0292_VERSION,
            "source_read_models": [
                "AdapterRegistryState",
                "ProviderCapabilityInventoryState",
                "AdapterCapabilityDeclarationState",
                "AdapterReadinessStatusState",
                "AdapterRiskProfileState",
                "AdapterCredentialNeedDeclarationState",
                "AdapterNetworkNeedDeclarationState",
                "AdapterOCELVisibilityDeclarationState",
                "AdapterMockNoNetworkRequirementState",
                "AdapterInputSchemaContractState",
                "AdapterOutputSchemaContractState",
                "AdapterEffectBoundaryContractState",
                "ProviderInvocationProhibitionState",
                "CommandExecutionProhibitionState",
                "PigGuidanceState",
                "OCPXProjectionState",
            ],
            "target_read_models": [
                "MockAdapterHarnessState",
                "MockProviderAdapterContractState",
                "MockAdapterFixtureCatalogState",
                "DeterministicAdapterFixtureState",
                "MockSchemaValidationState",
                "NoNetworkBoundaryState",
                "ProviderSDKIsolationState",
                "MockCredentialBoundaryState",
                "MockAdapterRunState",
                "MockAdapterOCELTraceState",
                "MockAdapterHarnessGateState",
                "V029ReadinessState",
            ],
            "effect_types": V0292_EFFECT_TYPES,
            "forbidden_effect_types": V0292_FORBIDDEN_EFFECT_TYPES,
        }


def render_mock_adapter_harness_cli(parts: dict[str, Any], section: str = "report") -> str:
    report: MockAdapterHarnessReport = parts["report"]
    lines = [
        f"Mock Adapter Harness / No-Network Default {section}",
        f"version={report.version}",
        f"layer={report.policy.layer}",
        f"report_status={report.report_status}",
        f"ready_for_v0_29_3={_bool(report.ready_for_v0_29_3)}",
        f"ready_for_permission_safety_gate={_bool(report.ready_for_permission_safety_gate)}",
        f"ready_for_live_adapter_implementation={_bool(report.ready_for_live_adapter_implementation)}",
        f"ready_for_provider_registration={_bool(report.ready_for_provider_registration)}",
        f"ready_for_provider_invocation={_bool(report.ready_for_provider_invocation)}",
        f"ready_for_network_access={_bool(report.ready_for_network_access)}",
        f"ready_for_command_execution={_bool(report.ready_for_command_execution)}",
        f"live_adapter_implemented={_bool(report.live_adapter_implemented)}",
        f"provider_registered={_bool(report.provider_registered)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"provider_sdk_invoked={_bool(report.provider_sdk_invoked)}",
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
