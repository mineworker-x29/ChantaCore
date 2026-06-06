from __future__ import annotations

import contextlib
import io

from chanta_core.cli.main import main
from chanta_core.external_skill_packaging_certification_matrix import (
    AdapterPackagingCertificationFindingService,
    AdapterPackagingCertificationReportService,
    V0297_EFFECT_TYPES,
    V0297_FORBIDDEN_EFFECT_TYPES,
    V0297_OBJECT_TYPES,
)


def _report():
    return AdapterPackagingCertificationReportService().build_report()


def test_packaging_certification_policy_request_and_source_view_build() -> None:
    report = _report()
    policy = report.policy
    source = report.source_view

    assert report.version == "v0.29.7"
    assert policy.layer == "external_provider_adapter"
    assert policy.packaging_enabled is True
    assert policy.certification_matrix_enabled is True
    assert policy.manifest_required is True
    assert policy.dependency_boundary_required is True
    assert policy.exposure_report_required is True
    assert policy.certification_cases_required is True
    assert policy.mock_mode_certification_required is True
    assert policy.no_network_certification_required is True
    assert policy.no_credential_certification_required is True
    assert policy.no_command_certification_required is True
    assert policy.permission_safety_certification_required is True
    assert policy.credential_network_boundary_certification_required is True
    assert policy.dry_run_certification_required is True
    assert policy.approval_audit_rollback_certification_required is True
    assert policy.ocel_visibility_certification_required is True
    assert policy.result_boundary_certification_required is True
    assert policy.failure_rollback_noop_certification_required is True
    assert policy.package_publish_enabled_now is False
    assert policy.release_tag_creation_enabled_now is False
    assert policy.live_provider_certification_enabled_now is False
    assert policy.provider_invocation_enabled_now is False
    assert policy.network_access_enabled_now is False
    assert policy.credential_access_enabled_now is False
    assert policy.command_execution_expansion_enabled_now is False
    assert policy.live_adapter_implementation_enabled_now is False
    assert policy.rpa_adapter_enabled_now is False
    assert policy.external_agent_dominion_enabled_now is False
    assert policy.certification_pass_is_not_invocation_preview is True
    assert policy.certified_mock_is_not_certified_live_adapter is True
    assert policy.llm_judge_as_sole_certification_authority_forbidden is True

    assert report.request.approval_audit_rollback_report_id
    assert report.request.invocation_candidate_report_id
    assert report.request.credential_network_boundary_report_id
    assert report.request.permission_safety_report_id
    assert report.request.mock_harness_report_id
    assert report.request.adapter_registry_report_id
    assert source.approval_audit_rollback_report_ref is not None
    assert source.approval_audit_rollback_gate_ref is not None
    assert source.approval_decision_record_refs
    assert source.audit_trail_refs
    assert source.ocel_trace_plan_refs
    assert source.result_boundary_refs
    assert source.failure_classification_refs
    assert source.rollback_plan_refs
    assert source.noop_boundary_refs
    assert source.invocation_candidate_report_ref is not None
    assert source.dry_run_report_refs
    assert source.credential_network_boundary_report_ref is not None
    assert source.permission_safety_report_ref is not None
    assert source.mock_harness_report_ref is not None
    assert source.adapter_registry_report_ref is not None
    assert source.external_adapter_contract_report_ref is not None
    assert source.provider_invocation_prohibition_ref is not None
    assert source.command_execution_prohibition_ref is not None
    assert source.ready_for_certification_matrix is True
    assert source.provider_invocation_detected is False
    assert source.network_call_detected is False
    assert source.credential_access_detected is False
    assert source.command_execution_detected is False
    assert source.live_adapter_detected is False
    assert source.package_publish_detected is False
    assert source.release_tag_detected is False
    assert source.private_data_detected is False
    assert source.raw_provider_output_detected is False


def test_skill_manifest_package_dependency_and_exposure_are_not_publish() -> None:
    report = _report()

    package_policy = report.external_skill_package_policy
    assert package_policy.external_skill_manifest_required is True
    assert package_policy.package_manifest_required is True
    assert package_policy.manifest_is_not_runtime_enablement is True
    assert package_policy.package_manifest_is_not_package_publish is True
    assert package_policy.package_publish_forbidden_now is True
    assert package_policy.release_tag_forbidden_now is True
    assert package_policy.runtime_binding_forbidden_now is True
    assert package_policy.provider_registration_forbidden_now is True
    assert package_policy.provider_invocation_forbidden_now is True

    manifest = report.external_skill_manifest
    assert manifest.entries
    assert manifest.entry_count == len(manifest.entries)
    assert manifest.manifest_is_runtime_enablement is False
    assert manifest.package_published is False
    for entry in manifest.entries:
        assert entry.skill_name
        assert entry.adapter_name
        assert entry.provider_kind
        assert entry.capability_refs
        assert entry.registry_entry_ref is not None
        assert entry.contract_ref is not None
        assert entry.mock_harness_ref is not None
        assert entry.certification_matrix_ref is not None
        assert entry.runtime_enabled_now is False
        assert entry.provider_invocation_enabled_now is False

    for package_manifest in report.adapter_package_manifests:
        assert package_manifest.package_publish_ready is False
        assert package_manifest.package_published_now is False
        assert package_manifest.release_tag_created_now is False
        assert package_manifest.runtime_dependency_added_now is False

    for dependency in report.dependency_profiles:
        assert dependency.provider_sdk_required_now is False
        assert dependency.provider_sdk_optional_later is True
        assert dependency.provider_sdk_runtime_dependency_added_now is False
        assert dependency.external_runtime_dependency_added_now is False
        assert dependency.private_dependency_detected is False

    for exposure in report.package_exposure_reports:
        assert exposure.private_data_exposed is False
        assert exposure.credential_exposed is False
        assert exposure.secret_exposed is False
        assert exposure.raw_provider_output_exposed is False
        assert exposure.raw_payload_exposed is False
        assert exposure.provider_sdk_runtime_dependency_exposed is False


def test_certification_matrix_cases_and_results_are_boundary_only() -> None:
    report = _report()
    expected_case_names = {
        "manifest_completeness",
        "dependency_boundary",
        "package_exposure",
        "mock_mode",
        "no_network",
        "no_credential",
        "no_command",
        "permission_safety",
        "credential_network_boundary",
        "invocation_dry_run",
        "approval_audit_rollback",
        "ocel_visibility",
        "result_boundary",
        "failure_rollback_noop",
        "rpa_future_track",
        "external_dominion_exclusion",
    }

    assert report.certification_policy.certification_matrix_required is True
    assert report.certification_policy.certification_cases_required is True
    assert report.certification_policy.boundary_tests_required is True
    assert report.certification_policy.live_provider_certification_forbidden_now is True
    assert report.certification_policy.certification_pass_is_not_provider_invocation is True

    for matrix in report.certification_matrices:
        case_names = {case.case_name for case in matrix.certification_cases}
        assert expected_case_names <= case_names
        assert matrix.total_case_count == len(matrix.certification_cases)
        assert matrix.passed_case_count >= 1
        assert matrix.warning_case_count >= 1
        assert matrix.failed_case_count == 0
        assert matrix.blocked_case_count == 0
        assert matrix.unknown_case_count == 0
        assert matrix.live_certified is False
        assert matrix.preview_gate_ready is True
        for case in matrix.certification_cases:
            assert case.live_provider_required is False
            assert case.network_required is False
            assert case.credential_value_required is False
            assert case.command_execution_required is False

    for result in report.certification_case_results:
        assert result.provider_invoked is False
        assert result.network_called is False
        assert result.credential_accessed is False
        assert result.command_executed is False
        assert result.live_adapter_used is False


def test_boundary_certifications_rpa_and_dominion_exclusion() -> None:
    report = _report()

    assert all(item.mock_mode_passed and item.deterministic_fixture_passed and not item.live_adapter_used for item in report.mock_mode_certifications)
    assert all(item.no_network_passed and not item.network_called and not item.outbound_request_sent for item in report.no_network_certifications)
    assert all(item.no_credential_passed and not item.credential_accessed and not item.credential_stored and not item.credential_logged and not item.secret_retrieved for item in report.no_credential_certifications)
    assert all(item.command_execution_forbidden and not item.command_executed and not item.shell_true_detected and not item.unbounded_subprocess_detected for item in report.no_command_certifications)
    assert all(item.deny_first_passed and item.no_permission_granted and item.no_approval_granted for item in report.permission_safety_certifications)
    assert all(item.credential_boundary_passed and item.network_boundary_passed and not item.ready_for_live_access for item in report.credential_network_boundary_certifications)
    assert all(item.dry_run_passed_or_safely_deferred and not item.provider_invoked and not item.network_called and not item.credential_accessed for item in report.dry_run_certifications)
    assert all(item.approval_boundary_passed and item.audit_boundary_passed and item.rollback_noop_boundary_passed and not item.approval_granted and not item.rollback_executed for item in report.approval_audit_rollback_certifications)
    assert all(item.required_events_present and item.provider_invocation_event_absent_now for item in report.ocel_visibility_certifications)
    assert all(item.raw_provider_output_persistence_forbidden and not item.raw_provider_output_persisted for item in report.result_boundary_certifications)
    assert all(item.failure_classification_ready and item.noop_available and not item.automatic_retry_performed for item in report.failure_rollback_noop_certifications)
    assert all(item.rpa_deferred and not item.rpa_implemented_now and not item.A360_related and not item.Brity_related and not item.UiPath_related for item in report.rpa_future_track_notes)
    assert all(item.excluded_from_v029 and not item.external_dominion_implemented_now and item.future_track == "v0.30+" for item in report.external_dominion_exclusion_certifications)


def test_gate_report_pig_ocpx_and_cli_build() -> None:
    service = AdapterPackagingCertificationReportService()
    report = service.build_report()
    gate = report.certification_readiness_gate

    assert gate.manifest_complete is True
    assert gate.package_boundary_passed is True
    assert gate.dependency_boundary_passed is True
    assert gate.exposure_boundary_passed is True
    assert gate.certification_matrix_complete is True
    assert gate.required_cases_passed_or_warned is True
    assert gate.mock_certified is True
    assert gate.no_network_certified is True
    assert gate.no_credential_certified is True
    assert gate.no_command_certified is True
    assert gate.permission_safety_certified is True
    assert gate.credential_network_boundary_certified is True
    assert gate.dry_run_certified is True
    assert gate.approval_audit_rollback_certified is True
    assert gate.ocel_visibility_certified is True
    assert gate.result_boundary_certified is True
    assert gate.failure_rollback_noop_certified is True
    assert gate.no_package_publish is True
    assert gate.no_release_tag is True
    assert gate.no_live_certification is True
    assert gate.no_provider_invocation is True
    assert gate.no_network_call is True
    assert gate.no_credential_access is True
    assert gate.no_command_execution is True
    assert gate.ready_for_v0_29_8 is True
    assert gate.ready_for_limited_invocation_preview_gate is True
    assert gate.ready_for_provider_invocation is False
    assert gate.ready_for_network_access is False
    assert gate.ready_for_credential_access is False
    assert gate.ready_for_command_execution is False

    assert report.audit_trail.raw_content_included is False
    assert report.audit_trail.credential_value_included is False
    assert report.audit_trail.raw_payload_included is False
    assert report.audit_trail.raw_provider_output_included is False
    assert report.report_status == "warning"
    assert report.ready_for_v0_29_8 is True
    assert report.ready_for_limited_invocation_preview_gate is True

    pig = service.build_pig_report()
    assert pig["version"] == "v0.29.7"
    assert pig["subject"] == "external_skill_packaging_certification_matrix"
    assert pig["safety_boundary"]["package_published"] is False
    assert pig["safety_boundary"]["live_provider_certified"] is False
    assert pig["safety_boundary"]["provider_invoked"] is False

    ocpx = service.build_ocpx_projection()
    assert ocpx["state"] == "external_skill_packaging_certification_matrix_created"
    assert "ExternalSkillManifestState" in ocpx["target_read_models"]
    assert "AdapterCertificationReadinessGateState" in ocpx["target_read_models"]
    assert "adapter_certification_readiness_gate_evaluated" in ocpx["effect_types"]

    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exit_code = main(["adapter", "certify", "report"])
    output = stdout.getvalue()
    assert exit_code == 0
    assert "version=v0.29.7" in output
    assert "ready_for_v0_29_8=true" in output
    assert "ready_for_limited_invocation_preview_gate=true" in output
    assert "ready_for_provider_invocation=false" in output
    assert "package_published=false" in output
    assert "release_tag_created=false" in output
    assert "live_provider_certified=false" in output


def test_report_forbidden_flags_and_mappings_remain_false() -> None:
    report = _report()

    assert report.ready_for_provider_invocation is False
    assert report.ready_for_network_access is False
    assert report.ready_for_credential_access is False
    assert report.ready_for_command_execution is False
    assert report.package_published is False
    assert report.release_tag_created is False
    assert report.live_provider_certified is False
    assert report.provider_registered is False
    assert report.provider_invoked is False
    assert report.provider_sdk_invoked is False
    assert report.network_called is False
    assert report.outbound_request_sent is False
    assert report.credential_accessed is False
    assert report.credential_stored is False
    assert report.credential_logged is False
    assert report.secret_retrieved is False
    assert report.secret_materialized is False
    assert report.command_executed is False
    assert report.external_side_effect_performed is False
    assert report.file_mutated is False
    assert report.rollback_executed is False
    assert report.automatic_retry_performed is False
    assert report.live_adapter_implemented is False
    assert report.RPA_adapter_implemented is False
    assert report.A360_adapter_implemented is False
    assert report.Brity_adapter_implemented is False
    assert report.UiPath_adapter_implemented is False
    assert report.external_dominion_implemented is False
    assert report.schumpeter_private_runtime_used is False
    assert report.actual_user_data_used is False
    assert report.actual_company_data_used is False
    assert report.private_material_exposed is False
    assert report.raw_provider_output_persisted is False
    assert report.raw_payload_logged is False
    assert report.references_runtime_dependency_added is False
    assert report.references_code_copied is False
    assert report.PIG_execution_authority_enabled is False
    assert report.llm_judge_used is False

    assert "external_skill_manifest" in V0297_OBJECT_TYPES
    assert "adapter_packaging_certification_report" in V0297_OBJECT_TYPES
    assert "external_skill_manifest_created" in V0297_EFFECT_TYPES
    assert "adapter_certification_matrix_created" in V0297_EFFECT_TYPES
    assert "state_candidate_created" in V0297_EFFECT_TYPES
    assert "package_published" in V0297_FORBIDDEN_EFFECT_TYPES
    assert "live_provider_certified" in V0297_FORBIDDEN_EFFECT_TYPES
    assert "provider_invoked" in V0297_FORBIDDEN_EFFECT_TYPES

    finding_types = {finding.finding_type for finding in report.findings}
    assert "packaging_certification_policy_created" in finding_types
    assert "certification_matrix_created" in finding_types
    assert "certification_gate_created" in finding_types
    assert "package_publish_attempted" in AdapterPackagingCertificationFindingService.BLOCKED_FINDINGS
    assert "llm_judge_detected" in AdapterPackagingCertificationFindingService.BLOCKED_FINDINGS
