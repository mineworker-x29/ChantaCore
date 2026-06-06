from __future__ import annotations

import contextlib
import io

from chanta_core.cli.main import main
from chanta_core.external_provider_adapter_foundation_consolidation import (
    V0299_EFFECT_TYPES,
    V0299_FORBIDDEN_EFFECT_TYPES,
    V0299_INCLUDED_VERSIONS,
    V0299_OBJECT_TYPES,
    V029ConsolidationFindingService,
    V029ConsolidationReportService,
)


def _report():
    return V029ConsolidationReportService().build_report()


def test_foundation_snapshot_components_and_previous_foundations_build() -> None:
    report = _report()
    snapshot = report.foundation_snapshot

    assert report.version == "v0.29.9"
    assert report.release_name == "External Provider Adapter Foundation v1"
    assert snapshot.release_name == "External Provider Adapter Foundation v1"
    assert snapshot.included_versions == V0299_INCLUDED_VERSIONS
    assert {ref["version"] for ref in snapshot.previous_foundation_refs} == {"v0.26.9", "v0.27.9", "v0.28.9"}
    assert len(snapshot.components) == 10
    assert {component.component_type for component in snapshot.components} >= {
        "contract",
        "registry",
        "mock_harness",
        "permission_safety",
        "credential_network",
        "invocation_dry_run",
        "approval_audit_rollback",
        "packaging_certification",
        "limited_preview_gate",
        "consolidation",
    }
    assert all(component.ready_for_foundation for component in snapshot.components)
    assert all(component.runtime_blocker is False for component in snapshot.components)
    assert snapshot.contract_ready is True
    assert snapshot.registry_ready is True
    assert snapshot.mock_harness_ready is True
    assert snapshot.permission_safety_ready is True
    assert snapshot.credential_network_ready is True
    assert snapshot.invocation_dry_run_ready is True
    assert snapshot.approval_audit_rollback_ready is True
    assert snapshot.packaging_certification_ready is True
    assert snapshot.limited_preview_gate_ready is True
    assert snapshot.provider_invocation_runtime_ready is False
    assert snapshot.live_adapter_runtime_ready is False
    assert snapshot.v030_handoff_ready is True


def test_capability_map_distinguishes_readiness_from_runtime() -> None:
    report = _report()
    capability_map = report.capability_map

    assert capability_map.entries
    assert capability_map.contract_count >= 1
    assert capability_map.registry_count >= 1
    assert capability_map.mock_ready_count >= 1
    assert capability_map.boundary_ready_count >= 1
    assert capability_map.dry_run_ready_count >= 1
    assert capability_map.certified_count >= 1
    assert capability_map.preview_gate_candidate_count >= 1
    assert capability_map.runtime_enabled_count == 0
    assert capability_map.blocked_count == 0
    assert capability_map.unknown_count == 0
    assert capability_map.capability_map_status == "ready"
    for entry in capability_map.entries:
        assert entry.capability_status in {
            "contract_only",
            "registry_only",
            "mock_ready",
            "boundary_ready",
            "dry_run_ready",
            "certified_mock",
            "preview_gate_candidate",
            "runtime_disabled",
            "future_track",
            "blocked",
            "unknown",
        }
        assert entry.runtime_enabled_now is False
        assert entry.provider_invocation_enabled_now is False
        assert entry.network_enabled_now is False
        assert entry.credential_access_enabled_now is False
        assert entry.requires_command_execution is False
        assert entry.requires_rpa is False
        assert entry.requires_external_dominion is False


def test_coverage_matrix_represents_all_v029_subjects() -> None:
    report = _report()
    coverage = report.coverage_matrix
    expected_subjects = {
        "adapter_contract",
        "provider_capability_registry",
        "mock_harness_no_network",
        "permission_safety_scope_gate",
        "credential_secret_network_boundary",
        "invocation_candidate_dry_run",
        "approval_audit_rollback_boundary",
        "packaging_certification_matrix",
        "limited_preview_gate",
    }

    assert {row.subject for row in coverage.rows} == expected_subjects
    assert coverage.required_coverage_count == len(expected_subjects)
    assert coverage.passed_coverage_count == len(expected_subjects)
    assert coverage.warning_coverage_count == 0
    assert coverage.blocked_coverage_count == 0
    assert coverage.unknown_coverage_count == 0
    assert coverage.coverage_status == "passed"
    for row in coverage.rows:
        assert row.report_available is True
        assert row.docs_available is True
        assert row.tests_available is True
        assert row.boundary_tests_available is True
        assert row.cli_available is True
        assert row.ocel_mapping_available is True
        assert row.pig_projection_available is True
        assert row.ocpx_projection_available is True
        assert row.safety_boundary_available is True
        assert row.coverage_status == "passed"
        assert row.missing_items == []


def test_all_consolidation_reports_keep_runtime_forbidden() -> None:
    report = _report()

    assert report.contract_consolidation.contract_ready is True
    assert report.contract_consolidation.provider_invocation_forbidden is True
    assert report.contract_consolidation.command_execution_forbidden is True
    assert report.registry_consolidation.registry_ready is True
    assert report.registry_consolidation.metadata_only_registry is True
    assert report.registry_consolidation.provider_registered is False
    assert report.registry_consolidation.provider_invoked is False
    assert report.mock_harness_consolidation.mock_harness_ready is True
    assert report.mock_harness_consolidation.no_network_default_validated is True
    assert report.mock_harness_consolidation.deterministic_fixture_validated is True
    assert report.mock_harness_consolidation.live_adapter_used is False
    assert report.mock_harness_consolidation.provider_invoked is False
    assert report.mock_harness_consolidation.network_called is False
    assert report.permission_safety_consolidation.permission_safety_ready is True
    assert report.permission_safety_consolidation.deny_first_validated is True
    assert report.permission_safety_consolidation.no_permission_granted is True
    assert report.permission_safety_consolidation.no_approval_granted is True
    assert report.permission_safety_consolidation.provider_invoked is False
    assert report.credential_network_consolidation.credential_network_ready is True
    assert report.credential_network_consolidation.no_credential_access is True
    assert report.credential_network_consolidation.no_credential_storage is True
    assert report.credential_network_consolidation.no_network_call is True
    assert report.credential_network_consolidation.no_provider_sdk_invocation is True
    assert report.invocation_dry_run_consolidation.invocation_dry_run_ready is True
    assert report.invocation_dry_run_consolidation.no_provider_invocation is True
    assert report.invocation_dry_run_consolidation.no_network_call is True
    assert report.invocation_dry_run_consolidation.no_credential_access is True
    assert report.invocation_dry_run_consolidation.no_external_side_effect is True
    assert report.approval_audit_rollback_consolidation.approval_audit_rollback_ready is True
    assert report.approval_audit_rollback_consolidation.no_approval_granted is True
    assert report.approval_audit_rollback_consolidation.no_provider_invocation is True
    assert report.approval_audit_rollback_consolidation.no_rollback_execution is True
    assert report.approval_audit_rollback_consolidation.no_automatic_retry is True
    assert report.packaging_certification_consolidation.packaging_certification_ready is True
    assert report.packaging_certification_consolidation.no_package_publish is True
    assert report.packaging_certification_consolidation.no_release_tag is True
    assert report.packaging_certification_consolidation.no_live_provider_certification is True
    assert report.packaging_certification_consolidation.no_provider_invocation is True
    assert report.limited_preview_gate_consolidation.limited_preview_gate_ready is True
    assert report.limited_preview_gate_consolidation.preview_gate_candidates_exist is True
    assert report.limited_preview_gate_consolidation.no_preview_execution is True
    assert report.limited_preview_gate_consolidation.no_provider_invocation is True
    assert report.limited_preview_gate_consolidation.no_network_call is True
    assert report.limited_preview_gate_consolidation.no_credential_access is True


def test_readiness_v030_handoff_manifest_and_audit_are_boundary_only() -> None:
    report = _report()
    readiness = report.adapter_readiness_report
    v030 = report.v030_readiness_report
    handoff = report.external_agent_dominion_handoff_packet
    manifest = report.release_manifest

    assert readiness.external_provider_adapter_foundation_ready is True
    assert readiness.provider_invocation_runtime_ready is False
    assert readiness.limited_preview_execution_ready_now is False
    assert readiness.live_adapter_runtime_ready is False
    assert readiness.ready_for_v030_contract is True
    assert readiness.readiness_status == "ready"
    assert readiness.warnings

    assert v030.target_version == "v0.30.0"
    assert v030.target_name == "External Agent Dominion Bridge Contract"
    assert v030.ready_for_v030_contract is True
    assert v030.ready_for_external_agent_inventory is True
    assert v030.ready_for_external_agent_dominion_runtime is False
    assert v030.ready_for_external_agent_execution is False
    assert v030.required_contract_first is True
    assert {
        "external_agent_trust_boundary",
        "external_agent_identity_boundary",
        "external_agent_capability_registry",
        "delegation_permission_gate",
        "safety_gate",
        "isolation_boundary",
        "audit_ocel_visibility",
        "rollback_noop_boundary",
        "dominion_preview_gate",
    } <= set(v030.required_boundaries)

    assert handoff.target_version == "v0.30.0"
    assert handoff.target_track == "External Agent Dominion Bridge Contract"
    assert handoff.refs_only is True
    assert handoff.implementation_performed_now is False
    assert {
        "external_agent_execution",
        "autonomous_delegation",
        "external_agent_command_authority",
        "unbounded_tool_control",
        "RPA_runtime_control",
        "provider_invocation_bypass",
        "credential_access_bypass",
        "network_access_bypass",
    } <= set(handoff.not_allowed_at_v030_start)

    assert manifest.release_name == "External Provider Adapter Foundation v1"
    assert manifest.included_versions == V0299_INCLUDED_VERSIONS
    assert {
        "Provider invocation runtime",
        "Provider registration runtime",
        "Provider SDK invocation",
        "Network access",
        "Credential access",
        "Command execution expansion",
        "Live adapter runtime",
        "Package publish",
        "Release tag creation",
        "Live provider certification",
        "RPA / A360 / Brity / UiPath runtime",
        "External Agent Dominion Bridge runtime",
        "Schumpeter private runtime",
    } <= set(manifest.excluded_capabilities)
    assert manifest.provider_invocation_enabled is False
    assert manifest.network_access_enabled is False
    assert manifest.credential_access_enabled is False
    assert manifest.command_execution_enabled is False

    assert report.audit_trail.raw_content_included is False
    assert report.audit_trail.credential_value_included is False
    assert report.audit_trail.raw_payload_included is False
    assert report.audit_trail.raw_provider_output_included is False
    assert report.audit_trail.audit_event_count >= 1


def test_report_pig_ocpx_cli_and_forbidden_flags() -> None:
    service = V029ConsolidationReportService()
    report = service.build_report()

    assert report.report_status == "passed"
    assert report.external_provider_adapter_foundation_ready is True
    assert report.ready_for_v030 is True
    assert report.ready_for_v030_contract is True
    assert report.provider_invocation_runtime_ready is False
    assert report.limited_preview_execution_ready_now is False
    assert report.live_adapter_runtime_ready is False
    assert report.external_agent_dominion_runtime_ready is False

    forbidden_flags = [
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
        "external_side_effect_performed",
        "file_mutated",
        "rollback_executed",
        "automatic_retry_performed",
        "package_published",
        "release_tag_created",
        "live_provider_certified",
        "live_adapter_implemented",
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
    for flag in forbidden_flags:
        assert getattr(report, flag) is False

    assert "external_provider_adapter_foundation_snapshot" in V0299_OBJECT_TYPES
    assert "v029_consolidation_report" in V0299_OBJECT_TYPES
    assert "external_provider_adapter_foundation_snapshot_created" in V0299_EFFECT_TYPES
    assert "v029_consolidation_report_created" in V0299_EFFECT_TYPES
    assert "state_candidate_created" in V0299_EFFECT_TYPES
    assert "provider_invoked" in V0299_FORBIDDEN_EFFECT_TYPES
    assert "network_called" in V0299_FORBIDDEN_EFFECT_TYPES
    assert "credential_accessed" in V0299_FORBIDDEN_EFFECT_TYPES

    pig = service.build_pig_report()
    assert pig["version"] == "v0.29.9"
    assert pig["subject"] == "external_provider_adapter_foundation_consolidation"
    assert pig["release_name"] == "External Provider Adapter Foundation v1"
    assert pig["safety_boundary"]["provider_invoked"] is False
    assert pig["safety_boundary"]["external_dominion_implemented"] is False

    ocpx = service.build_ocpx_projection()
    assert ocpx["state"] == "external_provider_adapter_foundation_v1_consolidated"
    assert "ExternalProviderAdapterFoundationSnapshotState" in ocpx["target_read_models"]
    assert "V030ReadinessState" in ocpx["target_read_models"]
    assert "v029_consolidation_report_created" in ocpx["effect_types"]

    finding_types = {finding.finding_type for finding in report.findings}
    assert "foundation_snapshot_created" in finding_types
    assert "capability_map_created" in finding_types
    assert "release_manifest_created" in finding_types
    assert "provider_invocation_attempted" in V029ConsolidationFindingService.BLOCKED_FINDINGS
    assert "llm_judge_detected" in V029ConsolidationFindingService.BLOCKED_FINDINGS

    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exit_code = main(["adapter", "consolidate", "report"])
    output = stdout.getvalue()
    assert exit_code == 0
    assert "version=v0.29.9" in output
    assert "release_name=External Provider Adapter Foundation v1" in output
    assert "external_provider_adapter_foundation_ready=true" in output
    assert "ready_for_v030_contract=true" in output
    assert "provider_invocation_runtime_ready=false" in output
    assert "provider_invoked=false" in output
    assert "network_called=false" in output
    assert "credential_accessed=false" in output
    assert "command_executed=false" in output
