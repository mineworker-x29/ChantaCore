from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.public_alpha_schumpeter_preparation import (
    AlphaDocumentationExampleConsolidationReport,
    AlphaReadinessValidationConsolidationReport,
    AlphaRuntimeSmokeConsolidationReport,
    ExternalAdapterContractHandoffPacket,
    ExternalAdapterPreflightConsolidationReport,
    PackagingConsolidationReport,
    PublicAlphaCapabilityEntry,
    PublicAlphaCapabilityMap,
    PublicAlphaCoverageMatrix,
    PublicAlphaCoverageRow,
    PublicAlphaFoundationComponent,
    PublicAlphaFoundationSnapshot,
    PublicAlphaReleaseManifest,
    PublicAlphaReleaseReadinessReport,
    PublicPrivateBoundaryConsolidationReport,
    ReleaseHygieneConsolidationReport,
    SchumpeterDecisionConsolidationReport,
    SchumpeterPreparationConsolidationReport,
    V0289_EFFECT_TYPES,
    V0289_FORBIDDEN_EFFECT_TYPES,
    V028ConsolidationAuditTrail,
    V028ConsolidationReport,
    V028ConsolidationReportService,
    V029ReadinessReport,
)


def _report() -> V028ConsolidationReport:
    return V028ConsolidationReportService().build_report()


def test_v0289_consolidation_models_build() -> None:
    report = _report()

    assert isinstance(report.foundation_snapshot, PublicAlphaFoundationSnapshot)
    assert all(isinstance(item, PublicAlphaFoundationComponent) for item in report.foundation_snapshot.components)
    assert isinstance(report.capability_map, PublicAlphaCapabilityMap)
    assert all(isinstance(item, PublicAlphaCapabilityEntry) for item in report.capability_map.entries)
    assert isinstance(report.coverage_matrix, PublicAlphaCoverageMatrix)
    assert all(isinstance(item, PublicAlphaCoverageRow) for item in report.coverage_matrix.rows)
    assert isinstance(report.release_hygiene_consolidation, ReleaseHygieneConsolidationReport)
    assert isinstance(report.packaging_consolidation, PackagingConsolidationReport)
    assert isinstance(report.public_private_consolidation, PublicPrivateBoundaryConsolidationReport)
    assert isinstance(report.schumpeter_decision_consolidation, SchumpeterDecisionConsolidationReport)
    assert isinstance(report.schumpeter_preparation_consolidation, SchumpeterPreparationConsolidationReport)
    assert isinstance(report.runtime_smoke_consolidation, AlphaRuntimeSmokeConsolidationReport)
    assert isinstance(report.documentation_example_consolidation, AlphaDocumentationExampleConsolidationReport)
    assert isinstance(report.readiness_validation_consolidation, AlphaReadinessValidationConsolidationReport)
    assert isinstance(report.external_adapter_preflight_consolidation, ExternalAdapterPreflightConsolidationReport)
    assert isinstance(report.public_alpha_release_readiness, PublicAlphaReleaseReadinessReport)
    assert isinstance(report.v029_readiness_report, V029ReadinessReport)
    assert isinstance(report.external_adapter_contract_handoff_packet, ExternalAdapterContractHandoffPacket)
    assert isinstance(report.release_manifest, PublicAlphaReleaseManifest)
    assert isinstance(report.audit_trail, V028ConsolidationAuditTrail)


def test_v0289_foundation_snapshot_capabilities_and_coverage() -> None:
    report = _report()
    snapshot = report.foundation_snapshot

    assert report.version == "v0.28.9"
    assert report.release_name == "Public Alpha / Schumpeter Split Preparation Foundation v1"
    assert set(snapshot.included_versions) == {f"v0.28.{idx}" for idx in range(10)}
    assert {ref["version"] for ref in snapshot.previous_foundation_refs} >= {"v0.26.9", "v0.27.9"}
    assert snapshot.architecture_ready is True
    assert snapshot.repository_release_ready is False
    assert snapshot.package_distribution_ready is True
    assert snapshot.public_private_boundary_ready is True
    assert snapshot.documentation_ready is True
    assert snapshot.smoke_demo_ready is True
    assert snapshot.alpha_validation_ready is True
    assert snapshot.external_adapter_preflight_ready is True
    assert snapshot.public_alpha_release_ready is False
    assert snapshot.public_alpha_release_claim_allowed is False
    assert snapshot.public_alpha_release_implemented is False

    categories = {entry.category for entry in report.capability_map.entries}
    assert {"release_hygiene", "packaging", "public_private", "schumpeter_preparation", "runtime_smoke", "documentation", "validation", "external_adapter_preflight", "future_external_adapter", "future_external_dominion"} <= categories
    disabled = {entry.capability_name: entry for entry in report.capability_map.entries}
    assert disabled["provider_invocation"].alpha_status == "disabled"
    assert disabled["command_execution_expansion"].alpha_status == "disabled"
    assert disabled["future_external_adapter_contract"].future_track is True
    assert disabled["future_external_adapter_contract"].implemented_now is False
    assert disabled["future_external_dominion_bridge"].future_track is True
    assert disabled["future_external_dominion_bridge"].implemented_now is False

    subjects = {row.subject for row in report.coverage_matrix.rows}
    assert {"v028_contract", "release_hygiene", "packaging", "public_private_boundary", "schumpeter_decision", "schumpeter_preparation", "runtime_smoke", "documentation_examples", "readiness_validation", "external_adapter_preflight"} <= subjects
    assert all(row.report_available and row.docs_available and row.tests_available for row in report.coverage_matrix.rows)
    assert all(row.boundary_tests_available and row.cli_available and row.ocel_mapping_available for row in report.coverage_matrix.rows)
    assert all(row.pig_projection_available and row.ocpx_projection_available for row in report.coverage_matrix.rows)
    assert report.coverage_matrix.unknown_coverage_count == 0
    assert report.coverage_matrix.coverage_status == "warning"


def test_v0289_consolidation_reports_preserve_boundaries() -> None:
    report = _report()

    assert report.release_hygiene_consolidation.blocks_public_alpha_release is True
    assert report.release_hygiene_consolidation.repository_release_ready is False
    assert report.packaging_consolidation.package_distribution_ready is True
    assert report.packaging_consolidation.package_publish_blocked is True
    assert report.packaging_consolidation.package_published is False
    assert report.packaging_consolidation.release_tag_created is False
    assert report.public_private_consolidation.no_private_material_exposure is True
    assert report.public_private_consolidation.no_credential_exposure is True
    assert report.public_private_consolidation.no_raw_trace_exposure is True
    assert report.schumpeter_decision_consolidation.recommended_default == "keep_reference_only_and_prepare_private_overlay"
    assert report.schumpeter_decision_consolidation.actual_split_implemented is False
    assert report.schumpeter_decision_consolidation.references_runtime_dependency_added is False
    assert report.schumpeter_decision_consolidation.references_code_copied is False
    assert report.schumpeter_preparation_consolidation.actual_split_implemented is False
    assert report.schumpeter_preparation_consolidation.company_wrapper_implemented is False
    assert report.schumpeter_preparation_consolidation.private_config_created is False
    assert report.schumpeter_preparation_consolidation.provider_adapter_created is False
    assert report.schumpeter_preparation_consolidation.RPA_adapter_created is False
    assert report.runtime_smoke_consolidation.provider_invoked is False
    assert report.runtime_smoke_consolidation.command_executed is False
    assert report.runtime_smoke_consolidation.network_called is False
    assert report.runtime_smoke_consolidation.file_mutated is False
    assert report.documentation_example_consolidation.no_actual_user_data is True
    assert report.documentation_example_consolidation.no_actual_company_data is True
    assert report.documentation_example_consolidation.no_private_material_exposure is True
    assert report.documentation_example_consolidation.no_raw_artifact_exposure is True
    assert report.readiness_validation_consolidation.ready_for_provider_invocation is False
    assert report.readiness_validation_consolidation.ready_for_command_execution is False
    assert report.external_adapter_preflight_consolidation.ready_for_v0_29_contract is True
    assert report.external_adapter_preflight_consolidation.provider_invocation_reopen_ready is False
    assert report.external_adapter_preflight_consolidation.command_execution_reopen_ready is False
    assert report.external_adapter_preflight_consolidation.external_adapter_implemented is False
    assert report.external_adapter_preflight_consolidation.provider_registered is False
    assert report.external_adapter_preflight_consolidation.provider_invoked is False
    assert report.external_adapter_preflight_consolidation.network_called is False


def test_v0289_release_readiness_v029_handoff_manifest_and_report_flags() -> None:
    report = _report()
    release = report.public_alpha_release_readiness
    v029 = report.v029_readiness_report
    handoff = report.external_adapter_contract_handoff_packet
    manifest = report.release_manifest

    assert release.architecture_ready is True
    assert release.repository_release_ready is False
    assert release.package_distribution_ready is True
    assert release.public_alpha_release_ready is False
    assert release.public_alpha_release_claim_allowed is False
    assert release.no_release_decision_valid is True
    assert release.release_status == "blocked"
    assert release.blockers

    assert v029.target_version == "v0.29.0"
    assert v029.target_name == "External Provider Adapter Contract"
    assert v029.ready_for_v0_29_contract is True
    assert v029.ready_for_external_adapter_implementation is False
    assert v029.ready_for_provider_invocation is False
    assert v029.ready_for_command_execution is False
    assert v029.required_contract_first is True

    assert handoff.target_version == "v0.29.0"
    assert handoff.target_track == "External Provider Adapter Contract"
    assert {"define_external_provider_adapter_contract", "define_provider_capability_inventory", "define_permission_gate", "define_safety_gate", "define_credential_boundary", "define_network_boundary", "define_audit_OCEL_visibility", "define_mock_mode", "define_no_network_default", "define_no_credential_default"} <= set(handoff.required_first_steps)
    assert {"provider_invocation", "command_execution_expansion", "credential_storage", "network_access", "RPA_adapter_runtime", "external_agent_dominion_bridge"} <= set(handoff.not_allowed_at_v029_start)
    assert handoff.refs_only is True
    assert handoff.implementation_performed_now is False

    assert set(manifest.included_versions) == {f"v0.28.{idx}" for idx in range(10)}
    assert {"Public Alpha release implementation", "Package publish", "Release tag creation", "Production runtime", "Schumpeter private runtime", "External provider adapter implementation", "Provider invocation", "Command execution expansion", "Network calls", "RPA / A360 / Brity / UiPath adapters", "External Agent Dominion Bridge", "Runtime continuity injection", "Autonomous memory-driven execution"} <= set(manifest.excluded_capabilities)
    assert manifest.public_alpha_release_implemented is False
    assert manifest.package_published is False
    assert manifest.release_tag_created is False

    assert report.ready_for_v0_29 is True
    assert report.ready_for_v0_29_contract is True
    assert report.ready_for_external_adapter_implementation is False
    assert report.ready_for_provider_invocation is False
    assert report.ready_for_command_execution is False
    assert report.public_alpha_release_ready is False
    assert report.public_alpha_release_claim_allowed is False
    for flag in [
        "public_alpha_release_implemented",
        "package_published",
        "package_uploaded",
        "release_tag_created",
        "official_release_artifact_created",
        "production_runtime_implemented",
        "schumpeter_private_runtime_used",
        "company_wrapper_implemented",
        "external_adapter_implemented",
        "provider_registered",
        "provider_invoked",
        "network_called",
        "command_executed",
        "external_dominion_implemented",
        "RPA_adapter_implemented",
        "A360_adapter_implemented",
        "Brity_adapter_implemented",
        "UiPath_adapter_implemented",
        "credential_created",
        "credential_exposed",
        "secret_exposed",
        "private_material_exposed",
        "actual_user_data_used",
        "actual_company_data_used",
        "raw_trace_used",
        "raw_transcript_used",
        "raw_provider_output_used",
        "runtime_continuity_injected",
        "autonomous_memory_execution_enabled",
        "references_runtime_dependency_added",
        "references_code_copied",
        "PIG_execution_authority_enabled",
        "llm_judge_used",
    ]:
        assert getattr(report, flag) is False


def test_v0289_pig_ocpx_mappings_and_cli_commands() -> None:
    service = V028ConsolidationReportService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert pig["version"] == "v0.28.9"
    assert pig["subject"] == "public_alpha_schumpeter_split_preparation_consolidation"
    assert pig["release_name"] == "Public Alpha / Schumpeter Split Preparation Foundation v1"
    assert ocpx["state"] == "public_alpha_schumpeter_split_preparation_foundation_v1_consolidated"
    assert "public_alpha_foundation_snapshot_created" in V0289_EFFECT_TYPES
    assert "public_alpha_capability_map_created" in V0289_EFFECT_TYPES
    assert "public_alpha_release_manifest_created" in V0289_EFFECT_TYPES
    assert "external_adapter_contract_handoff_packet_created" in V0289_EFFECT_TYPES
    assert "state_candidate_created" in V0289_EFFECT_TYPES
    assert "provider_invoked" in V0289_FORBIDDEN_EFFECT_TYPES
    assert "PublicAlphaFoundationSnapshotState" in ocpx["target_read_models"]
    assert "V029ReadinessState" in ocpx["target_read_models"]
    assert "V028ConsolidationState" in ocpx["target_read_models"]

    commands = ["snapshot", "capabilities", "coverage", "hygiene", "packaging", "public-private", "schumpeter-decision", "schumpeter-prep", "runtime-smoke", "docs", "validation", "adapter-preflight", "release-readiness", "v029-readiness", "manifest", "handoff-v029", "report"]
    assert main(["alpha", "consolidate"]) == 0
    for command in commands:
        assert main(["alpha", "consolidate", command]) == 0
