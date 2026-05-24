from __future__ import annotations

import subprocess
import sys

from chanta_core.internal_dominion import (
    DOMINION_OCEL_EVENT_TYPES,
    DOMINION_OCEL_OBJECT_TYPES,
    DOMINION_OCEL_RELATION_TYPES,
    RUNTIME_INVENTORY_NEXT_STEP,
    RUNTIME_INVENTORY_VERSION,
    CredentialBoundaryDescriptor,
    DominionInventorySourceService,
    DominionRuntimeInventoryRequest,
    EnvironmentBoundaryDescriptor,
    ExternalAgentRef,
    ExternalControlSurfaceRef,
    ExternalProviderRef,
    ExternalRuntimeRef,
    ExternalSystemRef,
    ExternalToolRef,
    InternalDominionRegistryService,
    RuntimeInventoryPolicyService,
    RuntimeInventoryReportService,
)


def _manifest(items: list[dict]) -> DominionRuntimeInventoryRequest:
    return DominionRuntimeInventoryRequest(source_refs=[{"items": items}])


def test_runtime_inventory_doc_records_v0_23_1_identity() -> None:
    text = open("docs/versions/v0.23.1_runtime_agent_system_inventory.md", encoding="utf-8").read()

    assert "Runtime / Agent / System Inventory" in text
    assert "Track: Internal Dominion Foundation" in text
    assert "Inventory is not dispatch" in text
    assert "Inventory is not provider API discovery" in text
    assert "Inventory is not runtime touch" in text
    assert "Inventory is not credential materialization" in text
    assert "v0.23.2 Capability Observation & Digestion for Dominion" in text


def test_runtime_inventory_report_builds_and_counts_declared_items() -> None:
    request = _manifest(
        [
            {"kind": "provider", "provider_ref_id": "provider:p1", "provider_name": "P1", "provider_type": "local_runtime"},
            {
                "kind": "runtime",
                "runtime_id": "runtime:r1",
                "runtime_type": "local_runtime",
                "provider_ref_id": "provider:p1",
                "environment": "production",
                "credential_boundary_ref": {"credential_boundary_id": "credential:c1"},
            },
            {"kind": "agent", "agent_id": "agent:a1", "agent_type": "coding_agent", "runtime_id": "runtime:r1"},
            {"kind": "tool", "tool_id": "tool:t1", "tool_type": "cli_tool", "runtime_id": "runtime:r1"},
            {"kind": "system", "system_id": "system:s1", "system_type": "erp", "environment": "production"},
            {
                "kind": "control_surface",
                "control_surface_id": "surface:manual",
                "surface_type": "manual_only",
                "runtime_id": "runtime:r1",
                "read_only_supported": True,
            },
            {"kind": "credential_boundary", "credential_boundary_id": "credential:c1", "credential_type": "vault_ref"},
        ]
    )

    report = RuntimeInventoryReportService().build_report(request)

    assert report.version == RUNTIME_INVENTORY_VERSION
    assert report.provider_count == 1
    assert report.runtime_count == 1
    assert report.agent_count == 1
    assert report.tool_count == 1
    assert report.system_count == 1
    assert report.control_surface_count == 1
    assert report.production_runtime_count == 1
    assert report.credential_sensitive_count == 1
    assert report.finding_count >= 1
    assert report.next_required_step == RUNTIME_INVENTORY_NEXT_STEP
    assert report.limitations
    assert report.withdrawal_conditions
    assert report.validity_horizon
    assert report.snapshot.dispatch_enabled is False
    assert report.snapshot.external_runtime_touched is False
    assert report.snapshot.provider_api_call_performed is False
    assert report.snapshot.raw_secret_output is False


def test_inventory_sources_are_sanitized_and_declarative_only() -> None:
    source = DominionInventorySourceService().load_sources(
        DominionRuntimeInventoryRequest(
            source_type="operator_input",
            source_refs=[{"credential_value": "hidden", "token": "hidden", "name": "declared"}],
        )
    )[0]

    assert source.source_type == "operator_input"
    assert source.raw_content_included is False
    assert source.credential_values_included is False
    assert source.private_full_paths_included is False
    assert "credential_value" not in source.source_ref
    assert "token" not in source.source_ref


def test_model_refs_support_required_types_and_default_safety_flags() -> None:
    provider_types = [
        "local_runtime",
        "rpa_runtime",
        "agent_runtime",
        "workflow_engine",
        "browser_automation",
        "enterprise_api",
        "database_or_etl",
        "custom_system",
    ]
    for provider_type in provider_types:
        provider = ExternalProviderRef(
            provider_ref_id=f"provider:{provider_type}",
            provider_name=provider_type,
            provider_type=provider_type,
        )
        assert provider.vendor_name is None
        assert provider.internal_core_dependency is False
        assert provider.provider_specific_logic_in_core is False

    runtime = ExternalRuntimeRef("runtime:r1", "Runtime", "local_runtime", environment="local")
    assert runtime.dispatch_enabled is False
    assert runtime.runtime_touched is False
    assert runtime.provider_api_call_performed is False

    for agent_type in ["coding_agent", "workflow_agent", "browser_agent", "chat_agent", "custom_agent"]:
        assert ExternalAgentRef(f"agent:{agent_type}", agent_type, agent_type).dispatch_enabled is False
    for tool_type in ["rpa_tool", "cli_tool", "api_tool", "browser_tool", "workflow_tool", "database_tool"]:
        assert ExternalToolRef(f"tool:{tool_type}", tool_type, tool_type).dispatch_enabled is False
    for system_type in ["business_app", "erp", "mes", "groupware", "ticketing", "document", "data_platform", "workflow"]:
        assert ExternalSystemRef(f"system:{system_type}", system_type, system_type).dispatch_enabled is False


def test_control_surface_and_boundaries_keep_dispatch_disabled() -> None:
    for surface_type in [
        "cli",
        "api",
        "sdk",
        "control_room",
        "queue",
        "scheduler",
        "agent_endpoint",
        "browser_session",
        "webhook",
        "database_connection",
        "workflow_console",
        "manual_only",
    ]:
        surface = ExternalControlSurfaceRef(
            control_surface_id=f"surface:{surface_type}",
            surface_type=surface_type,
            dispatch_supported=True,
        )
        assert surface.dispatch_supported is True
        assert surface.dispatch_enabled_v0_23_1 is False
        assert surface.provider_api_call_enabled_v0_23_1 is False

    credential = CredentialBoundaryDescriptor("credential:vault", credential_type="vault_ref")
    assert credential.credential_value_stored is False
    assert credential.credential_value_output is False
    assert credential.vault_or_secret_ref_only is True
    assert credential.redaction_required is True

    environment = EnvironmentBoundaryDescriptor(
        environment_boundary_id="environment:prod",
        runtime_id="runtime:prod",
        environment="production",
        production_impacting=True,
        requires_human_gate_for_dispatch=True,
        requires_strong_gate_for_mutation=True,
    )
    assert environment.production_impacting is True
    assert environment.requires_human_gate_for_dispatch is True
    assert environment.requires_strong_gate_for_mutation is True
    assert environment.dispatch_allowed_in_v0_23_1 is False


def test_policy_findings_cover_inventory_risks() -> None:
    service = RuntimeInventoryPolicyService()
    provider = ExternalProviderRef(
        "provider:bad",
        "requires GrowthKernel dependency",
        "unknown",
        vendor_name="FutureVendor",
        provider_specific_logic_in_core=True,
    )
    runtime = ExternalRuntimeRef(
        "runtime:bad",
        "Bad Runtime",
        "unknown",
        environment="unknown",
        dispatch_enabled=True,
        production_impacting=True,
    )
    surface = ExternalControlSurfaceRef(
        "surface:bad",
        "api",
        dispatch_enabled_v0_23_1=True,
        provider_api_call_enabled_v0_23_1=True,
    )
    findings = service.evaluate_policy(
        [provider],
        [runtime],
        [surface],
        [],
        [
            {"credential_value": "hidden"},
            {"note": "v0.23 self_execution legacy"},
            {"note": "requires GrowthKernel dependency"},
        ],
    )
    finding_types = {item.finding_type for item in findings}

    assert "unknown_runtime_type" in finding_types
    assert "unknown_environment" in finding_types
    assert "production_runtime_declared" in finding_types
    assert "credential_boundary_missing" in finding_types
    assert "credential_value_exposure_risk" in finding_types
    assert "provider_specific_logic_in_core" in finding_types
    assert "dispatch_enabled_too_early" in finding_types
    assert "provider_api_call_enabled_too_early" in finding_types
    assert "growthkernel_dependency_detected" in finding_types
    assert "self_execution_legacy_detected" in finding_types
    assert "vendor_hardcoding_detected" in finding_types


def test_registry_marks_runtime_inventory_skill_read_only_and_others_stubbed() -> None:
    contracts = InternalDominionRegistryService().list_skill_contracts()
    by_id = {item["skill_id"]: item for item in contracts}

    assert by_id["skill:dominion_runtime_inventory"]["status"] == "read_only"
    assert by_id["skill:dominion_runtime_inventory"]["declarative_inventory_only"] is True
    assert by_id["skill:dominion_runtime_inventory"]["external_dispatch_enabled"] is False
    assert by_id["skill:dominion_runtime_inventory"]["provider_api_call_enabled"] is False
    assert by_id["skill:dominion_bounded_dispatch"]["status"] == "boundary_only"
    assert by_id["skill:dominion_bounded_dispatch"]["stub"] is False


def test_ocel_pig_and_ocpx_inventory_views_exist() -> None:
    reports = RuntimeInventoryReportService()
    pig = reports.build_pig_report()
    ocpx = reports.build_ocpx_projection()

    for object_type in [
        "dominion_runtime_inventory_request",
        "dominion_inventory_source",
        "runtime_inventory_snapshot",
        "runtime_inventory_report",
        "external_provider_ref",
        "external_runtime_ref",
        "external_agent_ref",
        "external_tool_ref",
        "external_system_ref",
        "external_control_surface_ref",
        "credential_boundary_descriptor",
        "environment_boundary_descriptor",
        "runtime_inventory_finding",
    ]:
        assert object_type in DOMINION_OCEL_OBJECT_TYPES
    assert "dominion_runtime_inventory_requested" in DOMINION_OCEL_EVENT_TYPES
    assert "runtime_inventory_report_created" in DOMINION_OCEL_EVENT_TYPES
    assert "declares_external_runtime" in DOMINION_OCEL_RELATION_TYPES
    assert "not_provider_api_called" in DOMINION_OCEL_RELATION_TYPES

    assert pig["version"] == "v0.23.1"
    assert pig["subject"] == "runtime_agent_system_inventory"
    assert "inventory is not dispatch" in pig["principles"]
    assert pig["safety_boundary"]["dispatch_enabled"] is False
    assert pig["safety_boundary"]["external_runtime_touched"] is False
    assert pig["safety_boundary"]["provider_api_call_performed"] is False
    assert pig["safety_boundary"]["credential_exposed"] is False
    assert pig["safety_boundary"]["raw_secret_output"] is False
    assert ocpx["state"] == "dominion_runtime_inventory_declared"
    assert "DominionRuntimeInventoryState" in ocpx["target_read_models"]
    assert {"read_only_observation", "state_candidate_created"} <= set(ocpx["effect_types"])


def test_dominion_inventory_cli_views_are_sanitized() -> None:
    for args in [
        ["inventory"],
        ["inventory", "--source", "declared_manifest"],
        ["inventory", "report", "--report-id", "runtime_inventory_report:v0.23.1"],
        ["inventory", "providers"],
        ["inventory", "runtimes"],
        ["inventory", "systems"],
        ["inventory", "control-surfaces"],
        ["inventory", "findings"],
    ]:
        completed = subprocess.run(
            [sys.executable, "-m", "chantacore.cli", "dominion", *args],
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0
        assert "provider_count=" in completed.stdout
        assert "runtime_count=" in completed.stdout
        assert "agent_count=" in completed.stdout
        assert "tool_count=" in completed.stdout
        assert "system_count=" in completed.stdout
        assert "production_runtime_count=" in completed.stdout
        assert "credential_sensitive_count=" in completed.stdout
        assert "dispatch_enabled=false" in completed.stdout
        assert "external_runtime_touched=false" in completed.stdout
        assert "provider_api_call_performed=false" in completed.stdout
        assert "credential_exposed=false" in completed.stdout
        assert "next_required_step=v0.23.2 Capability Observation & Digestion for Dominion" in completed.stdout
        assert "raw_secrets_printed=False" in completed.stdout
        assert "private_full_paths_printed=False" in completed.stdout
