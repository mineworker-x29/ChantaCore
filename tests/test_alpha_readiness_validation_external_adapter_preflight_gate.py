from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.public_alpha_schumpeter_preparation import (
    AdapterCertificationPreflight,
    AlphaBoundaryTestMatrix,
    AlphaBoundaryTestMatrixRow,
    AlphaReadinessGate,
    AlphaReadinessValidationPolicy,
    AlphaReadinessValidationReport,
    AlphaReadinessValidationReportService,
    AlphaReadinessValidationRequest,
    AlphaReadinessValidationSourceView,
    AlphaRegressionTestMatrix,
    AlphaRegressionTestMatrixRow,
    AlphaValidationHandoffPacket,
    AuditRollbackOCELPreflight,
    CLISmokeValidationReport,
    CommandExecutionReopenCriteria,
    CredentialBoundaryPreflight,
    DocumentationValidationReport,
    ExamplePackValidationReport,
    ExternalAdapterPreflightPolicy,
    ExternalAdapterPreflightReport,
    ExternalAdapterPreflightRequest,
    ExternalAdapterPreflightSourceView,
    ExternalAdapterRiskAssessment,
    ForbiddenPatternScanPlan,
    ForbiddenPatternScanReport,
    ImportSmokeValidationReport,
    NetworkBoundaryPreflight,
    PackageBuildValidationReport,
    PackagingValidationReport,
    PermissionBoundaryPreflight,
    ProviderInvocationReopenCriteria,
    PublicPrivateValidationReport,
    ReleaseHygieneValidationReport,
    SafetyBoundaryValidationReport,
    SafetyGatePreflight,
    SchumpeterPreparationValidationReport,
    SmokeDemoValidationReport,
    V0288_EFFECT_TYPES,
    V0288_FORBIDDEN_EFFECT_TYPES,
    V028ValidationCoverageMatrix,
    V028ValidationCoverageRow,
)


def _report() -> AlphaReadinessValidationReport:
    return AlphaReadinessValidationReportService().build_report()


def test_v0288_validation_models_build() -> None:
    report = _report()

    assert isinstance(report.validation_policy, AlphaReadinessValidationPolicy)
    assert isinstance(report.request, AlphaReadinessValidationRequest)
    assert isinstance(report.source_view, AlphaReadinessValidationSourceView)
    assert isinstance(report.coverage_matrix, V028ValidationCoverageMatrix)
    assert all(isinstance(item, V028ValidationCoverageRow) for item in report.coverage_matrix.rows)
    assert isinstance(report.regression_test_matrix, AlphaRegressionTestMatrix)
    assert all(isinstance(item, AlphaRegressionTestMatrixRow) for item in report.regression_test_matrix.rows)
    assert isinstance(report.boundary_test_matrix, AlphaBoundaryTestMatrix)
    assert all(isinstance(item, AlphaBoundaryTestMatrixRow) for item in report.boundary_test_matrix.rows)
    assert isinstance(report.forbidden_pattern_scan_plan, ForbiddenPatternScanPlan)
    assert isinstance(report.forbidden_pattern_scan_report, ForbiddenPatternScanReport)
    assert isinstance(report.release_hygiene_validation_report, ReleaseHygieneValidationReport)
    assert isinstance(report.packaging_validation_report, PackagingValidationReport)
    assert isinstance(report.package_build_validation_report, PackageBuildValidationReport)
    assert isinstance(report.import_smoke_validation_report, ImportSmokeValidationReport)
    assert isinstance(report.cli_smoke_validation_report, CLISmokeValidationReport)
    assert isinstance(report.public_private_validation_report, PublicPrivateValidationReport)
    assert isinstance(report.documentation_validation_report, DocumentationValidationReport)
    assert isinstance(report.example_pack_validation_report, ExamplePackValidationReport)
    assert isinstance(report.smoke_demo_validation_report, SmokeDemoValidationReport)
    assert isinstance(report.safety_boundary_validation_report, SafetyBoundaryValidationReport)
    assert isinstance(report.schumpeter_preparation_validation_report, SchumpeterPreparationValidationReport)
    assert isinstance(report.external_adapter_preflight_report, ExternalAdapterPreflightReport)
    assert isinstance(report.alpha_readiness_gate, AlphaReadinessGate)
    assert isinstance(report.handoff_packet, AlphaValidationHandoffPacket)


def test_v0288_policy_source_coverage_regression_and_boundary_matrices() -> None:
    report = _report()
    policy = report.validation_policy

    assert policy.version == "v0.28.8"
    assert policy.validation_enabled is True
    assert policy.external_adapter_preflight_enabled is True
    assert policy.validation_is_not_release is True
    assert policy.preflight_is_not_adapter_implementation is True
    assert policy.unknown_is_not_passed is True
    assert policy.no_release_is_valid_outcome is True
    assert policy.no_adapter_is_valid_outcome is True
    assert policy.regression_validation_required is True
    assert policy.boundary_validation_required is True
    assert policy.forbidden_pattern_scan_required is True
    assert policy.external_adapter_preflight_required_before_v029 is True
    assert policy.package_publish_enabled_now is False
    assert policy.release_tag_creation_enabled_now is False
    assert policy.public_alpha_release_enabled_now is False
    assert policy.provider_invocation_enabled_now is False
    assert policy.network_call_enabled_now is False
    assert policy.command_execution_expansion_enabled_now is False
    assert policy.external_adapter_implementation_enabled_now is False
    assert policy.external_agent_dominion_enabled_now is False
    assert policy.rpa_adapter_enabled_now is False
    assert policy.schumpeter_private_runtime_enabled_now is False
    assert policy.runtime_continuity_injection_enabled_now is False
    assert policy.autonomous_memory_execution_enabled_now is False
    assert policy.llm_judge_as_sole_readiness_authority_forbidden is True

    source = report.source_view
    assert source.v0280_contract_report_ref is not None
    assert source.v0281_hygiene_report_ref is not None
    assert source.v0282_packaging_report_ref is not None
    assert source.v0283_public_private_report_ref is not None
    assert source.v0284_schumpeter_decision_report_ref is not None
    assert source.v0285_schumpeter_preparation_report_ref is not None
    assert source.v0286_runtime_profile_report_ref is not None
    assert source.v0287_documentation_report_ref is not None
    assert source.v0279_memory_consolidation_report_ref is not None
    assert source.v0269_workbench_consolidation_report_ref is not None
    assert source.test_metadata_refs
    assert source.ci_metadata_refs
    assert source.package_metadata_refs
    assert source.docs_metadata_refs
    assert source.forbidden_scan_metadata_refs
    assert source.private_material_detected is False
    assert source.credential_detected is False
    assert source.raw_trace_detected is False
    assert source.raw_transcript_detected is False
    assert source.raw_provider_output_detected is False
    assert source.provider_invocation_detected is False
    assert source.command_execution_detected is False

    coverage_versions = {row.version_number for row in report.coverage_matrix.rows}
    assert {f"v0.28.{idx}" for idx in range(8)} <= coverage_versions
    assert all(row.report_available and row.tests_available and row.boundary_tests_available for row in report.coverage_matrix.rows)
    assert all(row.safety_boundary_validated and row.public_private_validated for row in report.coverage_matrix.rows)
    assert report.coverage_matrix.unknown_count == 0

    scopes = {row.test_scope for row in report.regression_test_matrix.rows}
    assert {"v0.28.x", "v0.27.x", "v0.26.x", "v0.25.x", "v0.24.x", "v0.23.x", "v0.22_to_v0.20"} <= scopes
    assert all(row.command_execution_expansion_added is False for row in report.regression_test_matrix.rows)

    boundaries = {row.boundary_name for row in report.boundary_test_matrix.rows}
    assert {"no_package_publish", "no_release_tag_creation", "no_provider_invocation", "no_command_execution_expansion", "no_network_calls", "no_runtime_continuity_injection", "no_autonomous_memory_execution", "no_external_adapter_implementation", "no_RPA_adapter_implementation", "no_Schumpeter_private_runtime", "no_private_data", "no_credentials", "no_raw_traces", "no_raw_transcripts", "no_raw_provider_outputs", "no_references_runtime_dependency", "no_references_code_copy", "no_PIG_execution_authority", "no_LLM_judge_sole_authority"} <= boundaries
    assert report.boundary_test_matrix.blocked_boundary_count == 0


def test_v0288_validation_reports_and_scan_are_release_separated() -> None:
    report = _report()

    assert report.forbidden_pattern_scan_plan.raw_content_output_forbidden is True
    assert report.forbidden_pattern_scan_report.raw_content_output is False
    assert report.forbidden_pattern_scan_report.matched_pattern_count == 0
    assert report.forbidden_pattern_scan_report.blocking_match_count == 0
    assert report.release_hygiene_validation_report.blocks_public_alpha_release_claim is True
    assert report.release_hygiene_validation_report.repository_release_ready is False
    assert report.packaging_validation_report.package_distribution_ready is True
    assert report.package_build_validation_report.artifact_published is False
    assert report.package_build_validation_report.release_artifact_created is False
    assert report.import_smoke_validation_report.provider_invoked is False
    assert report.import_smoke_validation_report.command_executed is False
    assert report.cli_smoke_validation_report.provider_invoked is False
    assert report.cli_smoke_validation_report.command_executed is False
    assert report.public_private_validation_report.no_private_material_exposure is True
    assert report.public_private_validation_report.no_credential_exposure is True
    assert report.public_private_validation_report.no_raw_trace_exposure is True
    assert report.documentation_validation_report.no_overclaim_validated is True
    assert report.example_pack_validation_report.no_actual_user_data is True
    assert report.example_pack_validation_report.no_actual_company_data is True
    assert report.example_pack_validation_report.no_credentials is True
    assert report.example_pack_validation_report.no_raw_artifacts is True
    assert report.smoke_demo_validation_report.provider_invoked is False
    assert report.smoke_demo_validation_report.command_executed is False
    assert report.smoke_demo_validation_report.network_called is False
    assert report.smoke_demo_validation_report.file_mutated is False
    assert report.safety_boundary_validation_report.safety_boundaries_passed is True
    assert report.schumpeter_preparation_validation_report.actual_split_implemented is False
    assert report.schumpeter_preparation_validation_report.company_wrapper_implemented is False
    assert report.schumpeter_preparation_validation_report.private_config_created is False
    assert report.schumpeter_preparation_validation_report.provider_adapter_created is False
    assert report.schumpeter_preparation_validation_report.RPA_adapter_created is False


def test_v0288_external_adapter_preflight_and_reopen_criteria() -> None:
    preflight = _report().external_adapter_preflight_report

    assert isinstance(preflight.preflight_policy, ExternalAdapterPreflightPolicy)
    assert isinstance(preflight.request, ExternalAdapterPreflightRequest)
    assert isinstance(preflight.source_view, ExternalAdapterPreflightSourceView)
    assert isinstance(preflight.risk_assessment, ExternalAdapterRiskAssessment)
    assert isinstance(preflight.provider_invocation_reopen_criteria, ProviderInvocationReopenCriteria)
    assert isinstance(preflight.command_execution_reopen_criteria, CommandExecutionReopenCriteria)
    assert isinstance(preflight.credential_boundary_preflight, CredentialBoundaryPreflight)
    assert isinstance(preflight.network_boundary_preflight, NetworkBoundaryPreflight)
    assert isinstance(preflight.permission_boundary_preflight, PermissionBoundaryPreflight)
    assert isinstance(preflight.safety_gate_preflight, SafetyGatePreflight)
    assert isinstance(preflight.audit_rollback_ocel_preflight, AuditRollbackOCELPreflight)
    assert isinstance(preflight.adapter_certification_preflight, AdapterCertificationPreflight)

    policy = preflight.preflight_policy
    assert policy.adapter_implementation_enabled_now is False
    assert policy.provider_registration_enabled_now is False
    assert policy.provider_invocation_enabled_now is False
    assert policy.network_access_enabled_now is False
    assert policy.command_execution_enabled_now is False
    assert policy.credential_storage_enabled_now is False
    assert policy.external_agent_dominion_enabled_now is False
    assert policy.rpa_adapter_enabled_now is False
    assert policy.provider_adapter_contract_required_for_v029 is True
    assert policy.capability_declaration_is_not_permission is True
    assert policy.adapter_registration_is_not_execution is True
    assert policy.provider_invocation_requires_permission_gate is True
    assert policy.provider_invocation_requires_safety_gate is True
    assert policy.provider_invocation_requires_credential_boundary is True
    assert policy.provider_invocation_requires_network_boundary is True
    assert policy.provider_invocation_requires_audit is True
    assert policy.provider_invocation_requires_rollback_boundary is True
    assert policy.provider_invocation_requires_OCEL_visibility is True

    dimensions = set(preflight.risk_assessment.risk_dimensions)
    assert {"credential_exposure", "network_access", "provider_invocation", "command_execution", "permission_bypass", "safety_bypass", "audit_gap", "rollback_gap", "OCEL_visibility_gap", "external_dependency_risk", "private_data_exposure", "RPA_scope_creep", "external_agent_dominion_creep"} <= dimensions
    assert preflight.provider_invocation_reopen_criteria.provider_invocation_reopen_allowed_now is False
    assert preflight.provider_invocation_reopen_criteria.requires_v029_contract is True
    assert preflight.provider_invocation_reopen_criteria.requires_permission_gate is True
    assert preflight.provider_invocation_reopen_criteria.requires_OCEL_visibility is True
    assert preflight.command_execution_reopen_criteria.command_execution_reopen_allowed_now is False
    assert preflight.command_execution_reopen_criteria.requires_command_allowlist is True
    assert preflight.command_execution_reopen_criteria.requires_no_shell_true is True
    assert preflight.command_execution_reopen_criteria.requires_no_unbounded_subprocess is True
    assert preflight.credential_boundary_preflight.credential_storage_enabled_now is False
    assert preflight.network_boundary_preflight.network_access_enabled_now is False
    assert preflight.permission_boundary_preflight.provider_invocation_permission_required is True
    assert preflight.safety_gate_preflight.provider_safety_gate_required is True
    assert preflight.audit_rollback_ocel_preflight.OCEL_visibility_ready_for_v029 is True
    assert preflight.adapter_certification_preflight.adapter_mock_mode_required is True
    assert preflight.adapter_certification_preflight.adapter_no_network_default_required is True
    assert preflight.adapter_certification_preflight.adapter_no_credential_default_required is True
    assert preflight.ready_for_v0_29_contract is True
    assert preflight.ready_for_provider_invocation is False
    assert preflight.ready_for_command_execution is False
    assert preflight.adapter_implemented_now is False
    assert preflight.provider_invoked_now is False
    assert preflight.command_executed_now is False
    assert preflight.network_called_now is False
    assert preflight.credentials_created_now is False


def test_v0288_gate_report_mappings_and_cli_commands() -> None:
    service = AlphaReadinessValidationReportService()
    report = service.build_report()

    assert report.ready_for_v0_28_9 is True
    assert report.ready_for_public_alpha_release is False
    assert report.ready_for_public_alpha_release_claim is False
    assert report.ready_for_v0_29_contract is True
    assert report.ready_for_provider_invocation is False
    assert report.ready_for_command_execution is False
    assert report.alpha_readiness_gate.public_alpha_release_claim_allowed is False
    assert report.handoff_packet.target_version == "v0.28.9"
    assert report.handoff_packet.refs_only is True
    assert report.handoff_packet.implementation_performed_now is False
    assert {"public_alpha_release", "package_publish", "release_tag_creation", "external_provider_adapter", "provider_invocation", "command_execution_expansion", "RPA_adapter", "A360_adapter", "Brity_adapter", "UiPath_adapter", "external_agent_dominion_bridge", "runtime_continuity_injection", "autonomous_memory_execution", "Schumpeter_private_runtime"} <= set(report.handoff_packet.not_implemented_now)

    for flag in [
        "public_alpha_release_implemented",
        "package_published",
        "release_tag_created",
        "official_release_artifact_created",
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
        "schumpeter_private_runtime_used",
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

    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()
    assert pig["version"] == "v0.28.8"
    assert pig["subject"] == "alpha_readiness_validation_external_adapter_preflight_gate"
    assert ocpx["state"] == "alpha_readiness_validation_external_adapter_preflight_gate_evaluated"
    assert "alpha_readiness_validation_created" in V0288_EFFECT_TYPES
    assert "external_adapter_preflight_created" in V0288_EFFECT_TYPES
    assert "state_candidate_created" in V0288_EFFECT_TYPES
    assert "provider_invoked" in V0288_FORBIDDEN_EFFECT_TYPES
    assert "V029PreflightState" in ocpx["target_read_models"]

    validate_commands = ["policy", "source-view", "coverage", "regression", "boundaries", "forbidden-scan", "hygiene", "packaging", "build", "import-smoke", "cli-smoke", "public-private", "docs", "examples", "smoke", "safety", "schumpeter", "gate", "handoff", "report"]
    for command in validate_commands:
        assert main(["alpha", "validate", command]) == 0
    preflight_commands = ["adapter-policy", "adapter-risk", "provider-reopen", "command-reopen", "credentials", "network", "permission", "safety", "audit-ocel", "certification", "report"]
    for command in preflight_commands:
        assert main(["alpha", "preflight", command]) == 0
