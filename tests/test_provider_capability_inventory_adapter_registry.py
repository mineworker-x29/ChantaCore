from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.provider_capability_inventory_adapter_registry import (
    AdapterAvailabilityStatus,
    AdapterCapabilityDeclaration,
    AdapterCredentialNeedDeclaration,
    AdapterDependencyBoundaryReport,
    AdapterDisabledReason,
    AdapterNetworkNeedDeclaration,
    AdapterOCELVisibilityDeclaration,
    AdapterPermissionScopeRequirement,
    AdapterReadinessStatus,
    AdapterRegistry,
    AdapterRegistryEntry,
    AdapterRegistryGate,
    AdapterRegistryPolicy,
    AdapterRegistryReport,
    AdapterRegistryReportService,
    AdapterRiskProfile,
    AdapterSafetyScopeRequirement,
    ProviderCapabilityInventory,
    ProviderCapabilityInventoryPolicy,
    ProviderCapabilityRecord,
    ProviderKindCatalog,
    ProviderKindRecord,
    REQUIRED_OCEL_EVENTS,
    RISK_DIMENSIONS,
    V0291_EFFECT_TYPES,
    V0291_FORBIDDEN_EFFECT_TYPES,
)


def _report() -> AdapterRegistryReport:
    return AdapterRegistryReportService().build_report()


def test_v0291_registry_models_build() -> None:
    report = _report()

    assert isinstance(report.inventory_policy, ProviderCapabilityInventoryPolicy)
    assert isinstance(report.registry_policy, AdapterRegistryPolicy)
    assert isinstance(report.provider_kind_catalog, ProviderKindCatalog)
    assert all(isinstance(item, ProviderKindRecord) for item in report.provider_kind_catalog.provider_kinds)
    assert isinstance(report.provider_capability_inventory, ProviderCapabilityInventory)
    assert all(isinstance(item, ProviderCapabilityRecord) for item in report.provider_capability_inventory.capability_records)
    assert isinstance(report.adapter_registry, AdapterRegistry)
    assert all(isinstance(item, AdapterRegistryEntry) for item in report.adapter_registry.entries)
    assert all(isinstance(item, AdapterCapabilityDeclaration) for item in report.capability_declarations)
    assert all(isinstance(item, AdapterAvailabilityStatus) for item in report.availability_statuses)
    assert all(isinstance(item, AdapterReadinessStatus) for item in report.readiness_statuses)
    assert all(isinstance(item, AdapterDisabledReason) for item in report.disabled_reasons)
    assert all(isinstance(item, AdapterDependencyBoundaryReport) for item in report.dependency_boundary_reports)
    assert all(isinstance(item, AdapterRiskProfile) for item in report.risk_profiles)
    assert all(isinstance(item, AdapterPermissionScopeRequirement) for item in report.permission_scope_requirements)
    assert all(isinstance(item, AdapterSafetyScopeRequirement) for item in report.safety_scope_requirements)
    assert all(isinstance(item, AdapterCredentialNeedDeclaration) for item in report.credential_need_declarations)
    assert all(isinstance(item, AdapterNetworkNeedDeclaration) for item in report.network_need_declarations)
    assert all(isinstance(item, AdapterOCELVisibilityDeclaration) for item in report.ocel_visibility_declarations)
    assert isinstance(report.registry_gate, AdapterRegistryGate)


def test_v0291_inventory_and_registry_policies_preserve_boundaries() -> None:
    report = _report()
    inventory_policy = report.inventory_policy
    registry_policy = report.registry_policy

    assert report.version == "v0.29.1"
    assert inventory_policy.layer == "external_provider_adapter"
    assert inventory_policy.inventory_enabled is True
    assert inventory_policy.registry_enabled is True
    assert inventory_policy.inventory_is_not_implementation is True
    assert inventory_policy.registry_is_not_execution is True
    assert inventory_policy.registry_entry_is_not_provider_registration is True
    assert inventory_policy.capability_declaration_is_not_permission is True
    assert inventory_policy.provider_availability_is_not_invocation_readiness is True
    assert inventory_policy.unknown_status_is_not_available is True
    assert inventory_policy.blocked_status_must_remain_blocked is True
    assert inventory_policy.adapter_implementation_enabled_now is False
    assert inventory_policy.provider_registration_enabled_now is False
    assert inventory_policy.provider_invocation_enabled_now is False
    assert inventory_policy.network_access_enabled_now is False
    assert inventory_policy.credential_storage_enabled_now is False
    assert inventory_policy.command_execution_expansion_enabled_now is False
    assert inventory_policy.rpa_adapter_enabled_now is False
    assert inventory_policy.external_agent_dominion_enabled_now is False
    assert inventory_policy.schumpeter_private_runtime_enabled_now is False
    assert inventory_policy.mock_no_network_required_before_live is True
    assert inventory_policy.permission_gate_required_before_invocation is True
    assert inventory_policy.safety_gate_required_before_invocation is True
    assert inventory_policy.credential_boundary_required_before_invocation is True
    assert inventory_policy.network_boundary_required_before_invocation is True
    assert inventory_policy.audit_required_before_invocation is True
    assert inventory_policy.rollback_or_noop_required_before_invocation is True
    assert inventory_policy.ocel_visibility_required_before_invocation is True

    assert registry_policy.registry_entries_allowed is True
    assert registry_policy.registry_entries_are_metadata_only is True
    assert registry_policy.real_provider_registration_forbidden_now is True
    assert registry_policy.adapter_runtime_binding_forbidden_now is True
    assert registry_policy.registry_entry_requires_contract_ref is True
    assert registry_policy.registry_entry_requires_provider_kind is True
    assert registry_policy.registry_entry_requires_capability_declarations is True
    assert registry_policy.registry_entry_requires_availability_status is True
    assert registry_policy.registry_entry_requires_readiness_status is True
    assert registry_policy.registry_entry_requires_risk_profile is True
    assert registry_policy.registry_entry_requires_permission_scope_requirements is True
    assert registry_policy.registry_entry_requires_safety_scope_requirements is True
    assert registry_policy.registry_entry_requires_credential_need_declaration is True
    assert registry_policy.registry_entry_requires_network_need_declaration is True
    assert registry_policy.registry_entry_requires_ocel_visibility_declaration is True
    assert registry_policy.provider_registration_enabled_now is False
    assert registry_policy.provider_invocation_enabled_now is False


def test_v0291_provider_kind_catalog_and_inventory_are_metadata_only() -> None:
    report = _report()
    kinds = {item.provider_kind: item for item in report.provider_kind_catalog.provider_kinds}

    assert {"llm_provider", "search_provider", "storage_provider", "calendar_provider", "email_provider", "workflow_provider", "rpa_provider", "internal_mock_provider", "local_file_provider", "unknown"} <= set(kinds)
    assert all(item.implementation_allowed_now is False for item in kinds.values())
    assert all(item.invocation_allowed_now is False for item in kinds.values())
    assert kinds["llm_provider"].network_required_later is True
    assert kinds["llm_provider"].credential_required_later is True
    assert kinds["rpa_provider"].future_track is True
    assert kinds["rpa_provider"].required_future_gate == "v0.29.7"

    inventory = report.provider_capability_inventory
    assert inventory.capability_count == len(inventory.capability_records)
    assert inventory.available_count >= 1
    assert inventory.gated_count >= 1
    assert inventory.future_track_count >= 1
    assert inventory.blocked_count >= 1
    assert inventory.unknown_count >= 1
    assert inventory.provider_invocation_enabled is False
    assert inventory.provider_registration_enabled is False

    unknown = next(record for record in inventory.capability_records if record.capability_status == "unknown")
    assert unknown.public_safe is False
    assert unknown.capability_declaration_is_permission is False
    assert unknown.capability_declaration_is_invocation is False
    assert all(record.capability_declaration_is_permission is False for record in inventory.capability_records)
    assert all(record.capability_declaration_is_invocation is False for record in inventory.capability_records)
    assert all(record.requires_provider_invocation is False or record.required_future_gate for record in inventory.capability_records)


def test_v0291_adapter_registry_entries_and_declarations_are_not_registration_or_invocation() -> None:
    report = _report()
    registry = report.adapter_registry

    assert registry.entry_count == len(registry.entries)
    assert registry.available_entry_count >= 1
    assert registry.gated_entry_count >= 1
    assert registry.future_track_entry_count >= 1
    assert registry.blocked_entry_count >= 1
    assert registry.provider_registered_now is False
    assert registry.provider_invoked_now is False
    assert registry.adapter_implemented_now is False

    for entry in registry.entries:
        assert entry.contract_ref is not None
        assert entry.capability_declaration_refs
        assert entry.availability_status_ref is not None
        assert entry.readiness_status_ref is not None
        assert entry.disabled_reason_ref is not None
        assert entry.risk_profile_ref is not None
        assert entry.dependency_boundary_report_ref is not None
        assert entry.permission_scope_requirement_ref is not None
        assert entry.safety_scope_requirement_ref is not None
        assert entry.credential_need_declaration_ref is not None
        assert entry.network_need_declaration_ref is not None
        assert entry.ocel_visibility_declaration_ref is not None
        assert entry.registry_entry_is_provider_registration is False
        assert entry.adapter_implemented_now is False
        assert entry.provider_registered_now is False
        assert entry.provider_invoked_now is False

    for declaration in report.capability_declarations:
        assert declaration.input_schema_ref is not None
        assert declaration.output_schema_ref is not None
        assert declaration.effect_boundary_ref is not None
        assert declaration.risk_level in {"low", "high"}
        assert declaration.required_audit_boundary is True
        assert declaration.required_rollback_boundary is True
        assert declaration.required_ocel_visibility is True
        assert declaration.declaration_status in {"declared", "warning"}
        assert declaration.declaration_is_permission is False
        assert declaration.declaration_is_invocation is False


def test_v0291_status_dependency_risk_and_requirement_declarations() -> None:
    report = _report()

    assert all(status.available_for_implementation is False for status in report.availability_statuses)
    assert all(status.available_for_invocation is False for status in report.availability_statuses)
    assert all(status.available_for_network is False for status in report.availability_statuses)
    assert all(status.ready_for_implementation is False for status in report.readiness_statuses)
    assert all(status.ready_for_provider_registration is False for status in report.readiness_statuses)
    assert all(status.ready_for_provider_invocation is False for status in report.readiness_statuses)
    assert all(status.mock_ready is False for status in report.readiness_statuses)
    assert all(status.permission_gate_ready is False for status in report.readiness_statuses)
    assert all(status.safety_gate_ready is False for status in report.readiness_statuses)
    assert all(status.credential_boundary_ready is False for status in report.readiness_statuses)
    assert all(status.network_boundary_ready is False for status in report.readiness_statuses)
    assert all(status.audit_rollback_ready is False for status in report.readiness_statuses)
    assert all(status.certification_ready is False for status in report.readiness_statuses)
    assert all(status.invocation_preview_ready is False for status in report.readiness_statuses)

    assert all(report.provider_sdk_required_now is False for report in report.dependency_boundary_reports)
    assert all(report.provider_sdk_runtime_dependency_added_now is False for report in report.dependency_boundary_reports)
    assert all(report.private_sdk_detected is False for report in report.dependency_boundary_reports)
    assert all(set(RISK_DIMENSIONS) <= set(profile.risk_dimensions) for profile in report.risk_profiles)
    assert all(profile.blocks_implementation is True for profile in report.risk_profiles)
    assert all(profile.blocks_invocation is True for profile in report.risk_profiles)

    assert all(requirement.permission_granted_now is False for requirement in report.permission_scope_requirements)
    assert all(requirement.permission_gate_future_version == "v0.29.3" for requirement in report.permission_scope_requirements)
    assert all(requirement.safety_gate_passed_now is False for requirement in report.safety_scope_requirements)
    assert all(requirement.safety_gate_future_version == "v0.29.3" for requirement in report.safety_scope_requirements)
    assert all(declaration.credential_value_stored_now is False for declaration in report.credential_need_declarations)
    assert all(declaration.credential_value_logged_now is False for declaration in report.credential_need_declarations)
    assert all(declaration.env_file_created_now is False for declaration in report.credential_need_declarations)
    assert all(declaration.credential_boundary_future_version == "v0.29.4" for declaration in report.credential_need_declarations)
    assert all(declaration.network_access_enabled_now is False for declaration in report.network_need_declarations)
    assert all(declaration.network_called_now is False for declaration in report.network_need_declarations)
    assert all(declaration.network_boundary_future_version == "v0.29.4" for declaration in report.network_need_declarations)
    assert all(set(REQUIRED_OCEL_EVENTS) <= set(declaration.declared_events) for declaration in report.ocel_visibility_declarations)
    assert all(not declaration.missing_required_events for declaration in report.ocel_visibility_declarations)


def test_v0291_registry_gate_report_pig_ocpx_and_cli() -> None:
    service = AdapterRegistryReportService()
    report = service.build_report()
    gate = report.registry_gate
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert gate.capability_declarations_complete is True
    assert gate.availability_statuses_complete is True
    assert gate.readiness_statuses_complete is True
    assert gate.risk_profiles_complete is True
    assert gate.permission_requirements_complete is True
    assert gate.safety_requirements_complete is True
    assert gate.credential_need_declarations_complete is True
    assert gate.network_need_declarations_complete is True
    assert gate.ocel_visibility_declarations_complete is True
    assert gate.no_provider_registration is True
    assert gate.no_provider_invocation is True
    assert gate.no_network_call is True
    assert gate.no_credential_storage is True
    assert gate.no_command_execution is True
    assert gate.ready_for_v0_29_2 is True
    assert gate.ready_for_adapter_implementation is False
    assert gate.ready_for_provider_registration is False
    assert gate.ready_for_provider_invocation is False

    assert report.report_status == "warning"
    assert report.ready_for_v0_29_2 is True
    assert report.ready_for_mock_harness is True
    assert report.ready_for_adapter_implementation is False
    assert report.ready_for_provider_registration is False
    assert report.ready_for_provider_invocation is False
    assert report.ready_for_network_access is False
    assert report.ready_for_command_execution is False
    assert report.next_required_step == "v0.29.2 Mock Adapter Harness / No-Network Default"

    assert pig["version"] == "v0.29.1"
    assert pig["layer"] == "external_provider_adapter"
    assert pig["subject"] == "provider_capability_inventory_adapter_registry"
    assert ocpx["state"] == "provider_capability_inventory_adapter_registry_created"
    assert "provider_capability_inventory_created" in V0291_EFFECT_TYPES
    assert "adapter_registry_created" in V0291_EFFECT_TYPES
    assert "adapter_registry_entry_created" in V0291_EFFECT_TYPES
    assert "adapter_capability_declaration_created" in V0291_EFFECT_TYPES
    assert "adapter_status_recorded" in V0291_EFFECT_TYPES
    assert "adapter_registry_gate_evaluated" in V0291_EFFECT_TYPES
    assert "provider_invoked" in V0291_FORBIDDEN_EFFECT_TYPES
    assert "network_called" in V0291_FORBIDDEN_EFFECT_TYPES
    assert "ProviderCapabilityInventoryState" in ocpx["target_read_models"]
    assert "AdapterRegistryState" in ocpx["target_read_models"]
    assert "AdapterRegistryGateState" in ocpx["target_read_models"]
    assert "V029ReadinessState" in ocpx["target_read_models"]

    commands = [
        "policy",
        "provider-kinds",
        "inventory",
        "capabilities",
        "entries",
        "declarations",
        "availability",
        "readiness",
        "disabled-reasons",
        "dependencies",
        "risks",
        "permission-requirements",
        "safety-requirements",
        "credential-needs",
        "network-needs",
        "ocel-visibility",
        "gate",
        "report",
    ]
    for command in commands:
        assert main(["adapter", "registry", command]) == 0
