from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.mock_adapter_harness_no_network_default import (
    DeterministicAdapterFixture,
    MockAdapterFixtureCatalog,
    MockAdapterHarnessGate,
    MockAdapterHarnessPolicy,
    MockAdapterHarnessReport,
    MockAdapterHarnessReportService,
    MockAdapterHarnessRequest,
    MockAdapterHarnessSourceView,
    MockAdapterInputBundle,
    MockAdapterLifecycleValidationReport,
    MockAdapterOCELTracePlan,
    MockAdapterOCELTraceReport,
    MockAdapterResponseFixture,
    MockAdapterResponseSchema,
    MockAdapterRunPlan,
    MockAdapterRunReport,
    MockCredentialBoundaryReport,
    MockEffectBoundaryValidationReport,
    MockInputSchemaValidationReport,
    MockOutputSchemaValidationReport,
    MockProviderAdapterContract,
    NoNetworkAdapterPolicy,
    NoNetworkBoundaryReport,
    ProviderSDKIsolationReport,
    MOCK_REQUIRED_EVENT_TYPES,
    MOCK_REQUIRED_OBJECT_TYPES,
    V0292_EFFECT_TYPES,
    V0292_FORBIDDEN_EFFECT_TYPES,
)


def _report() -> MockAdapterHarnessReport:
    return MockAdapterHarnessReportService().build_report()


def test_v0292_mock_harness_models_build() -> None:
    report = _report()

    assert isinstance(report.policy, MockAdapterHarnessPolicy)
    assert isinstance(report.request, MockAdapterHarnessRequest)
    assert isinstance(report.source_view, MockAdapterHarnessSourceView)
    assert all(isinstance(item, MockProviderAdapterContract) for item in report.mock_provider_adapter_contracts)
    assert isinstance(report.fixture_catalog, MockAdapterFixtureCatalog)
    assert all(isinstance(item, DeterministicAdapterFixture) for item in report.fixture_catalog.fixtures)
    assert all(isinstance(item, MockAdapterInputBundle) for item in report.input_bundles)
    assert all(isinstance(item, MockAdapterResponseSchema) for item in report.response_schemas)
    assert all(isinstance(item, MockAdapterResponseFixture) for item in report.response_fixtures)
    assert all(isinstance(item, MockInputSchemaValidationReport) for item in report.input_validation_reports)
    assert all(isinstance(item, MockOutputSchemaValidationReport) for item in report.output_validation_reports)
    assert all(isinstance(item, MockEffectBoundaryValidationReport) for item in report.effect_boundary_validation_reports)
    assert isinstance(report.no_network_policy, NoNetworkAdapterPolicy)
    assert all(isinstance(item, NoNetworkBoundaryReport) for item in report.no_network_boundary_reports)
    assert all(isinstance(item, ProviderSDKIsolationReport) for item in report.provider_sdk_isolation_reports)
    assert all(isinstance(item, MockCredentialBoundaryReport) for item in report.mock_credential_boundary_reports)
    assert all(isinstance(item, MockAdapterLifecycleValidationReport) for item in report.lifecycle_validation_reports)
    assert all(isinstance(item, MockAdapterOCELTracePlan) for item in report.ocel_trace_plans)
    assert all(isinstance(item, MockAdapterOCELTraceReport) for item in report.ocel_trace_reports)
    assert all(isinstance(item, MockAdapterRunPlan) for item in report.mock_run_plans)
    assert all(isinstance(item, MockAdapterRunReport) for item in report.mock_run_reports)
    assert isinstance(report.mock_harness_gate, MockAdapterHarnessGate)


def test_v0292_policy_and_source_view_preserve_no_network_default() -> None:
    report = _report()
    policy = report.policy
    source = report.source_view

    assert report.version == "v0.29.2"
    assert policy.layer == "external_provider_adapter"
    assert policy.mock_harness_enabled is True
    assert policy.no_network_default_required is True
    assert policy.deterministic_fixture_required is True
    assert policy.mock_response_schema_required is True
    assert policy.provider_sdk_isolation_required is True
    assert policy.credential_free_mock_required is True
    assert policy.ocel_visible_mock_required is True
    assert policy.mock_run_is_not_provider_invocation is True
    assert policy.mock_success_is_not_live_readiness is True
    assert policy.live_adapter_implementation_enabled_now is False
    assert policy.provider_registration_enabled_now is False
    assert policy.provider_invocation_enabled_now is False
    assert policy.network_access_enabled_now is False
    assert policy.credential_storage_enabled_now is False
    assert policy.provider_sdk_invocation_enabled_now is False
    assert policy.command_execution_expansion_enabled_now is False
    assert policy.rpa_adapter_enabled_now is False
    assert policy.external_agent_dominion_enabled_now is False
    assert policy.schumpeter_private_runtime_enabled_now is False
    assert policy.actual_user_data_forbidden is True
    assert policy.actual_company_data_forbidden is True
    assert policy.raw_provider_output_persistence_forbidden is True
    assert policy.llm_judge_as_sole_mock_authority_forbidden is True

    assert source.adapter_registry_report_ref is not None
    assert source.adapter_registry_ref is not None
    assert source.provider_capability_inventory_ref is not None
    assert source.adapter_capability_declaration_refs
    assert source.adapter_readiness_status_refs
    assert source.adapter_dependency_boundary_refs
    assert source.adapter_risk_profile_refs
    assert source.adapter_credential_need_refs
    assert source.adapter_network_need_refs
    assert source.adapter_ocel_visibility_refs
    assert source.mock_no_network_contract_ref is not None
    assert source.input_schema_contract_ref is not None
    assert source.output_schema_contract_ref is not None
    assert source.effect_boundary_contract_ref is not None
    assert source.provider_invocation_prohibition_ref is not None
    assert source.command_execution_prohibition_ref is not None
    assert source.registry_ready_for_mock is True
    assert source.live_adapter_detected is False
    assert source.provider_invocation_detected is False
    assert source.network_call_detected is False
    assert source.credential_value_detected is False
    assert source.command_execution_detected is False
    assert source.raw_provider_output_detected is False


def test_v0292_mock_contracts_fixtures_inputs_and_responses_are_synthetic() -> None:
    report = _report()

    assert report.mock_provider_adapter_contracts
    for contract in report.mock_provider_adapter_contracts:
        assert contract.adapter_registry_entry_ref is not None
        assert contract.capability_refs
        assert contract.mock_interface_required is True
        assert contract.deterministic_response_required is True
        assert contract.no_network_required is True
        assert contract.no_credentials_required is True
        assert contract.no_provider_sdk_required is True
        assert contract.input_schema_validation_required is True
        assert contract.output_schema_validation_required is True
        assert contract.effect_boundary_validation_required is True
        assert contract.ocel_trace_required is True
        assert contract.live_adapter_implemented_now is False
        assert contract.provider_invoked_now is False
        assert contract.network_called_now is False
        assert contract.credential_used_now is False

    catalog = report.fixture_catalog
    assert catalog.fixture_count == len(catalog.fixtures)
    assert catalog.deterministic_fixture_count == catalog.fixture_count
    assert catalog.missing_fixture_count == 0
    assert catalog.blocked_fixture_count == 0
    assert catalog.catalog_status == "ready"
    for fixture in catalog.fixtures:
        assert fixture.deterministic is True
        assert fixture.synthetic_only is True
        assert fixture.contains_actual_user_data is False
        assert fixture.contains_actual_company_data is False
        assert fixture.contains_credentials is False
        assert fixture.contains_raw_provider_output is False
        assert fixture.requires_network is False
        assert fixture.requires_provider_sdk is False

    assert all(bundle.synthetic_only is True for bundle in report.input_bundles)
    assert all(bundle.contains_private_data is False for bundle in report.input_bundles)
    assert all(bundle.contains_credentials is False for bundle in report.input_bundles)
    assert all(bundle.contains_raw_secret is False for bundle in report.input_bundles)
    assert all(schema.redaction_boundary_required is True for schema in report.response_schemas)
    assert all(schema.raw_provider_output_forbidden is True for schema in report.response_schemas)
    assert all({"fixture_id", "adapter_name", "result_summary", "status"} <= set(schema.required_fields) for schema in report.response_schemas)
    assert all(fixture.mock_response_is_live_provider_output is False for fixture in report.response_fixtures)
    assert all(fixture.contains_raw_provider_output is False for fixture in report.response_fixtures)
    assert all(fixture.contains_credentials is False for fixture in report.response_fixtures)


def test_v0292_schema_effect_no_network_sdk_and_credential_boundaries() -> None:
    report = _report()

    assert all(item.input_schema_validated is True for item in report.input_validation_reports)
    assert all(item.private_data_boundary_validated is True for item in report.input_validation_reports)
    assert all(item.credential_reference_boundary_validated is True for item in report.input_validation_reports)
    assert all(item.raw_secret_input_detected is False for item in report.input_validation_reports)
    assert all(item.raw_private_payload_detected is False for item in report.input_validation_reports)
    assert all(item.output_schema_validated is True for item in report.output_validation_reports)
    assert all(item.output_redaction_boundary_validated is True for item in report.output_validation_reports)
    assert all(item.output_error_schema_validated is True for item in report.output_validation_reports)
    assert all(item.raw_provider_output_detected is False for item in report.output_validation_reports)
    assert all(item.credential_output_detected is False for item in report.output_validation_reports)

    for item in report.effect_boundary_validation_reports:
        assert item.allowed_effects_validated is True
        assert item.forbidden_effects_absent is True
        assert item.provider_invoked is False
        assert item.network_called is False
        assert item.command_executed is False
        assert item.credential_stored is False
        assert item.external_side_effect_performed is False
        assert item.file_mutated_by_adapter is False
        assert item.private_data_exfiltrated is False

    policy = report.no_network_policy
    assert policy.no_network_default_required is True
    assert policy.live_network_disabled_now is True
    assert policy.outbound_network_forbidden_now is True
    assert policy.provider_sdk_network_forbidden_now is True
    assert policy.webhook_forbidden_now is True
    assert policy.websocket_forbidden_now is True
    assert policy.internal_network_forbidden_now is True
    assert policy.network_boundary_future_version == "v0.29.4"
    assert all(item.network_access_enabled is False for item in report.no_network_boundary_reports)
    assert all(item.network_called is False for item in report.no_network_boundary_reports)
    assert all(item.provider_sdk_network_called is False for item in report.no_network_boundary_reports)
    assert all(item.outbound_domain_used is False for item in report.no_network_boundary_reports)
    assert all(item.provider_sdk_required_now is False for item in report.provider_sdk_isolation_reports)
    assert all(item.provider_sdk_imported_now is False for item in report.provider_sdk_isolation_reports)
    assert all(item.provider_sdk_invoked_now is False for item in report.provider_sdk_isolation_reports)
    assert all(item.provider_sdk_runtime_dependency_added_now is False for item in report.provider_sdk_isolation_reports)
    assert all(item.provider_sdk_optional_dependency_only_later is True for item in report.provider_sdk_isolation_reports)
    assert all(item.credential_required_for_mock is False for item in report.mock_credential_boundary_reports)
    assert all(item.credential_value_stored is False for item in report.mock_credential_boundary_reports)
    assert all(item.credential_value_logged is False for item in report.mock_credential_boundary_reports)
    assert all(item.env_file_created is False for item in report.mock_credential_boundary_reports)
    assert all(item.committed_secret_detected is False for item in report.mock_credential_boundary_reports)
    assert all(item.secret_reference_used_as_value is False for item in report.mock_credential_boundary_reports)


def test_v0292_lifecycle_ocel_and_mock_runs_are_not_external_actions() -> None:
    report = _report()

    assert all(item.declared_state_validated is True for item in report.lifecycle_validation_reports)
    assert all(item.mocked_state_validated is True for item in report.lifecycle_validation_reports)
    assert all(item.certified_mock_state_not_claimed_as_live is True for item in report.lifecycle_validation_reports)
    assert all(item.live_preview_state_not_enabled is True for item in report.lifecycle_validation_reports)

    for plan in report.ocel_trace_plans:
        assert set(MOCK_REQUIRED_EVENT_TYPES) <= set(plan.required_event_types)
        assert set(MOCK_REQUIRED_OBJECT_TYPES) <= set(plan.required_object_types)
    assert all(item.required_events_present is True for item in report.ocel_trace_reports)
    assert all(item.required_objects_present is True for item in report.ocel_trace_reports)
    assert all(item.provider_invocation_event_absent is True for item in report.ocel_trace_reports)
    assert all(item.network_call_event_absent is True for item in report.ocel_trace_reports)
    assert all(item.command_execution_event_absent is True for item in report.ocel_trace_reports)

    for plan in report.mock_run_plans:
        assert plan.run_mode == "metadata_only"
        assert plan.live_provider_allowed is False
        assert plan.network_allowed is False
        assert plan.credentials_allowed is False
        assert plan.command_execution_allowed is False
        assert plan.file_mutation_allowed is False
    for item in report.mock_run_reports:
        assert item.run_mode == "metadata_only"
        assert item.live_provider_used is False
        assert item.provider_invoked is False
        assert item.network_called is False
        assert item.credentials_used is False
        assert item.command_executed is False
        assert item.file_mutated is False


def test_v0292_gate_report_pig_ocpx_and_cli() -> None:
    service = MockAdapterHarnessReportService()
    report = service.build_report()
    gate = report.mock_harness_gate
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert gate.deterministic_fixtures_ready is True
    assert gate.no_network_boundary_passed is True
    assert gate.provider_sdk_isolation_passed is True
    assert gate.credential_free_mock_passed is True
    assert gate.input_output_schema_passed is True
    assert gate.effect_boundary_passed is True
    assert gate.ocel_visibility_passed is True
    assert gate.mock_run_passed_or_safely_deferred is True
    assert gate.ready_for_v0_29_3 is True
    assert gate.ready_for_permission_safety_gate is True
    assert gate.ready_for_live_adapter_implementation is False
    assert gate.ready_for_provider_registration is False
    assert gate.ready_for_provider_invocation is False
    assert gate.ready_for_network_access is False
    assert gate.ready_for_command_execution is False

    assert report.report_status == "warning"
    assert report.ready_for_v0_29_3 is True
    assert report.ready_for_permission_safety_gate is True
    assert report.ready_for_live_adapter_implementation is False
    assert report.ready_for_provider_registration is False
    assert report.ready_for_provider_invocation is False
    assert report.ready_for_network_access is False
    assert report.ready_for_command_execution is False
    assert report.next_required_step == "v0.29.3 Permission / Safety / Scope Gate for External Adapters"

    assert pig["version"] == "v0.29.2"
    assert pig["subject"] == "mock_adapter_harness_no_network_default"
    assert ocpx["state"] == "mock_adapter_harness_no_network_default_created"
    assert "mock_adapter_harness_created" in V0292_EFFECT_TYPES
    assert "mock_provider_adapter_contract_created" in V0292_EFFECT_TYPES
    assert "mock_fixture_created" in V0292_EFFECT_TYPES
    assert "mock_schema_validation_report_created" in V0292_EFFECT_TYPES
    assert "no_network_boundary_report_created" in V0292_EFFECT_TYPES
    assert "provider_sdk_isolation_report_created" in V0292_EFFECT_TYPES
    assert "mock_adapter_harness_gate_evaluated" in V0292_EFFECT_TYPES
    assert "provider_invoked" in V0292_FORBIDDEN_EFFECT_TYPES
    assert "network_called" in V0292_FORBIDDEN_EFFECT_TYPES
    assert "MockAdapterHarnessState" in ocpx["target_read_models"]
    assert "MockAdapterHarnessGateState" in ocpx["target_read_models"]
    assert "V029ReadinessState" in ocpx["target_read_models"]

    commands = [
        "policy",
        "source-view",
        "contracts",
        "fixtures",
        "inputs",
        "response-schema",
        "response-fixtures",
        "validate-inputs",
        "validate-outputs",
        "validate-effects",
        "no-network",
        "sdk-isolation",
        "credentials",
        "lifecycle",
        "ocel-plan",
        "ocel-report",
        "run-plan",
        "run-report",
        "gate",
        "report",
    ]
    for command in commands:
        assert main(["adapter", "mock", command]) == 0
