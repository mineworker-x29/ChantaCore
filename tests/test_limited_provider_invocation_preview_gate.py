from __future__ import annotations

import contextlib
import io

from chanta_core.cli.main import main
from chanta_core.limited_provider_invocation_preview_gate import (
    LimitedProviderInvocationPreviewReportService,
    LimitedPreviewFindingService,
    V0298_EFFECT_TYPES,
    V0298_FORBIDDEN_EFFECT_TYPES,
    V0298_OBJECT_TYPES,
)


def _report():
    return LimitedProviderInvocationPreviewReportService().build_report()


def test_preview_policy_request_and_source_view_build() -> None:
    report = _report()
    policy = report.policy
    source = report.source_view

    assert report.version == "v0.29.8"
    assert policy.layer == "external_provider_adapter"
    assert policy.preview_gate_enabled is True
    assert policy.preview_execution_enabled_now is False
    assert policy.preview_eligibility_required is True
    assert policy.certification_required is True
    assert policy.explicit_approval_required_later is True
    assert policy.credential_boundary_required is True
    assert policy.network_boundary_required is True
    assert policy.payload_boundary_required is True
    assert policy.result_boundary_required is True
    assert policy.audit_ocel_plan_required is True
    assert policy.rollback_noop_boundary_required is True
    assert policy.limited_scope_required is True
    assert policy.preview_scope_must_be_bounded is True
    assert policy.preview_pass_is_not_unlimited_runtime is True
    assert policy.preview_authorization_candidate_is_not_invocation is True
    assert policy.provider_invocation_enabled_now is False
    assert policy.provider_registration_enabled_now is False
    assert policy.provider_sdk_invocation_enabled_now is False
    assert policy.network_access_enabled_now is False
    assert policy.credential_access_enabled_now is False
    assert policy.secret_retrieval_enabled_now is False
    assert policy.command_execution_expansion_enabled_now is False
    assert policy.rollback_execution_enabled_now is False
    assert policy.automatic_retry_enabled_now is False
    assert policy.live_adapter_implementation_enabled_now is False
    assert policy.package_publish_enabled_now is False
    assert policy.release_tag_creation_enabled_now is False
    assert policy.rpa_adapter_enabled_now is False
    assert policy.external_agent_dominion_enabled_now is False
    assert policy.no_provider_invocation_default is True
    assert policy.no_network_default is True
    assert policy.no_credential_value_default is True
    assert policy.no_command_execution_default is True
    assert policy.llm_judge_as_sole_preview_authority_forbidden is True

    assert report.request.packaging_certification_report_id
    assert report.request.approval_audit_rollback_report_id
    assert report.request.invocation_candidate_report_id
    assert report.request.credential_network_boundary_report_id
    assert source.packaging_certification_report_ref is not None
    assert source.certification_readiness_gate_ref is not None
    assert source.certification_matrix_refs
    assert source.certification_case_result_refs
    assert source.boundary_certification_refs
    assert source.rpa_future_track_note_refs
    assert source.external_dominion_exclusion_refs
    assert source.approval_audit_rollback_report_ref is not None
    assert source.approval_decision_record_refs
    assert source.audit_trail_refs
    assert source.rollback_noop_refs
    assert source.invocation_candidate_report_ref is not None
    assert source.invocation_candidate_refs
    assert source.dry_run_report_refs
    assert source.credential_network_boundary_report_ref is not None
    assert source.permission_safety_report_ref is not None
    assert source.mock_harness_report_ref is not None
    assert source.adapter_registry_report_ref is not None
    assert source.external_adapter_contract_report_ref is not None
    assert source.provider_invocation_prohibition_ref is not None
    assert source.command_execution_prohibition_ref is not None
    assert source.certification_ready_for_preview_gate is True
    assert source.approval_boundary_ready_for_preview_gate is True
    assert source.invocation_candidate_ready_for_preview_gate is True
    assert source.credential_network_ready_for_preview_gate is True
    assert source.provider_invocation_detected is False
    assert source.provider_sdk_invocation_detected is False
    assert source.network_call_detected is False
    assert source.credential_access_detected is False
    assert source.secret_retrieval_detected is False
    assert source.command_execution_detected is False
    assert source.rollback_execution_detected is False
    assert source.automatic_retry_detected is False
    assert source.external_side_effect_detected is False
    assert source.file_mutation_detected is False
    assert source.package_publish_detected is False
    assert source.release_tag_detected is False
    assert source.live_adapter_detected is False
    assert source.private_data_detected is False
    assert source.raw_provider_output_detected is False


def test_eligibility_scope_and_preview_candidates_are_not_invocation() -> None:
    report = _report()
    matrix = report.eligibility_matrix

    assert matrix.rows
    assert matrix.total_candidate_count == len(matrix.rows)
    assert matrix.eligible_candidate_count >= 1
    assert matrix.denied_candidate_count == 0
    assert matrix.blocked_candidate_count == 0
    assert matrix.unknown_candidate_count == 0
    assert matrix.matrix_status in {"passed", "warning"}
    for row in matrix.rows:
        assert row.certification_passed_or_warned is True
        assert row.approval_boundary_complete is True
        assert row.credential_boundary_complete is True
        assert row.network_boundary_complete is True
        assert row.payload_boundary_complete is True
        assert row.result_boundary_complete is True
        assert row.audit_ocel_boundary_complete is True
        assert row.rollback_noop_boundary_complete is True
        assert row.rpa_not_implemented is True
        assert row.external_dominion_excluded is True
        assert row.eligible_for_limited_preview_gate is True
        assert row.eligible_for_live_invocation_now is False

    scope_policy = report.scope_policy
    assert scope_policy.limited_scope_required is True
    assert scope_policy.preview_scope_must_be_adapter_specific is True
    assert scope_policy.preview_scope_must_be_capability_specific is True
    assert scope_policy.preview_scope_must_be_payload_bounded is True
    assert scope_policy.preview_scope_must_be_network_bounded is True
    assert scope_policy.preview_scope_must_be_credential_ref_bounded is True
    assert scope_policy.preview_scope_must_be_time_bounded is True
    assert scope_policy.wildcard_provider_scope_forbidden is True
    assert scope_policy.wildcard_network_scope_forbidden is True
    assert scope_policy.wildcard_credential_scope_forbidden is True
    assert scope_policy.command_scope_forbidden is True
    assert scope_policy.rpa_scope_forbidden_now is True

    for scope in report.preview_scopes:
        assert scope.adapter_name
        assert scope.capability_name
        assert scope.provider_scope
        assert scope.network_scope_ref is not None
        assert scope.credential_scope_ref is not None
        assert scope.payload_scope_ref is not None
        assert scope.result_scope_ref is not None
        assert scope.expiry_required is True
        assert scope.explicit_approval_required_later is True
        assert scope.scope_is_minimal is True
        assert scope.scope_is_bounded is True
        assert scope.live_invocation_scope_granted_now is False

    for candidate in report.preview_candidates:
        assert candidate.preview_scope_ref
        assert candidate.invocation_candidate_ref is not None
        assert candidate.provider_kind
        assert candidate.candidate_status == "preview_gate_candidate"
        assert candidate.preview_candidate_is_provider_invocation is False
        assert candidate.provider_invoked_now is False
        assert candidate.provider_registered_now is False
        assert candidate.network_called_now is False
        assert candidate.credential_accessed_now is False
        assert candidate.command_executed_now is False


def test_preview_bindings_do_not_access_network_credentials_payload_or_results() -> None:
    report = _report()

    assert all(item.explicit_user_approval_required_later and item.approval_record_required for item in report.approval_requirements)
    assert all(item.approval_expiry_required and item.approval_revalidation_required for item in report.approval_requirements)
    assert all(item.approval_scope_summary_required and not item.approval_granted_now for item in report.approval_requirements)

    for binding in report.credential_bindings:
        assert binding.credential_reference_ref is not None
        assert binding.credential_boundary_ref is not None
        assert binding.secret_reference_only is True
        assert binding.credential_value_accessed_now is False
        assert binding.credential_value_stored_now is False
        assert binding.credential_value_logged_now is False
        assert binding.secret_retrieved_now is False

    for binding in report.network_bindings:
        assert binding.network_request_candidate_ref is not None
        assert binding.outbound_domain_rule_ref is not None
        assert binding.network_boundary_ref is not None
        assert binding.network_scope_bounded is True
        assert binding.network_called_now is False
        assert binding.outbound_request_sent_now is False
        assert binding.provider_sdk_network_called_now is False

    for boundary in report.payload_boundaries:
        assert boundary.payload_preview_ref is not None
        assert boundary.payload_boundary_ref is not None
        assert boundary.redaction_boundary_ref is not None
        assert boundary.payload_bounded is True
        assert boundary.payload_sent_now is False
        assert boundary.contains_credentials is False
        assert boundary.contains_private_data is False
        assert boundary.contains_raw_artifacts is False

    for boundary in report.result_boundaries:
        assert boundary.result_boundary_ref is not None
        assert boundary.result_persistence_policy_ref is not None
        assert boundary.raw_provider_output_persistence_forbidden is True
        assert boundary.result_summary_required_later is True
        assert boundary.result_redaction_required_later is True
        assert boundary.provider_response_received_now is False
        assert boundary.raw_provider_output_persisted_now is False


def test_audit_rollback_risk_and_decisions_are_boundary_only() -> None:
    report = _report()
    expected_events = {
        "limited_preview_candidate_created",
        "limited_preview_scope_recorded",
        "limited_preview_approval_requirement_recorded",
        "limited_preview_credential_binding_recorded",
        "limited_preview_network_binding_recorded",
        "limited_preview_payload_boundary_recorded",
        "limited_preview_result_boundary_recorded",
        "limited_preview_gate_evaluated",
    }

    assert all(expected_events <= set(plan.required_preview_events) for plan in report.audit_ocel_plans)
    assert all(not plan.provider_invocation_event_emitted_now for plan in report.audit_ocel_plans)
    assert all(item.rollback_or_noop_available and item.noop_available for item in report.rollback_noop_bindings)
    assert all(not item.rollback_executed_now and item.noop_is_valid_decision for item in report.rollback_noop_bindings)

    for risk in report.risk_assessments:
        assert "credential_exposure" in risk.risk_dimensions
        assert "network_access" in risk.risk_dimensions
        assert "external_dominion_creep" in risk.risk_dimensions
        assert risk.blocker_count == 0
        assert risk.warning_count >= 0
        assert risk.risk_acceptable_for_preview_gate is True
        assert risk.risk_assessment_is_approval is False

    assert report.deny_defer_reasons
    assert {reason.reason_type for reason in report.deny_defer_reasons} <= {
        "missing_certification",
        "high_risk",
        "private_data_risk",
        "credential_risk",
        "network_risk",
        "command_like_forbidden",
        "rpa_future_track",
        "external_dominion_future_track",
        "unknown",
    }
    assert {reason.decision for reason in report.deny_defer_reasons} <= {"deny", "defer", "block", "unknown"}

    for decision in report.decision_candidates:
        assert decision.proposed_decision == "preview_gate_candidate"
        assert decision.preview_execution_allowed_now is False
        assert decision.provider_invocation_allowed_now is False
        assert decision.network_allowed_now is False
        assert decision.credential_access_allowed_now is False
        assert decision.command_execution_allowed_now is False

    for record in report.decision_records:
        assert record.final_decision == "preview_gate_candidate"
        assert record.provider_invoked_now is False
        assert record.network_called_now is False
        assert record.credential_accessed_now is False
        assert record.command_executed_now is False
        assert record.external_side_effect_performed_now is False


def test_gate_audit_handoff_report_pig_ocpx_and_cli_build() -> None:
    service = LimitedProviderInvocationPreviewReportService()
    report = service.build_report()
    gate = report.preview_gate

    assert gate.certification_ready is True
    assert gate.approval_boundary_ready is True
    assert gate.credential_boundary_ready is True
    assert gate.network_boundary_ready is True
    assert gate.payload_boundary_ready is True
    assert gate.result_boundary_ready is True
    assert gate.audit_ocel_ready is True
    assert gate.rollback_noop_ready is True
    assert gate.risk_acceptable is True
    assert gate.rpa_excluded_or_deferred is True
    assert gate.external_dominion_excluded is True
    assert gate.preview_gate_candidates_complete is True
    assert gate.preview_gate_passed is True
    assert gate.no_provider_invocation is True
    assert gate.no_network_call is True
    assert gate.no_credential_access is True
    assert gate.no_command_execution is True
    assert gate.no_external_side_effect is True
    assert gate.no_package_publish is True
    assert gate.no_release_tag is True
    assert gate.ready_for_v0_29_9 is True
    assert gate.ready_for_v029_consolidation is True
    assert gate.ready_for_preview_execution_now is False
    assert gate.ready_for_provider_invocation is False
    assert gate.ready_for_network_access is False
    assert gate.ready_for_credential_access is False
    assert gate.ready_for_command_execution is False

    assert report.audit_trail.raw_content_included is False
    assert report.audit_trail.credential_value_included is False
    assert report.audit_trail.raw_payload_included is False
    assert report.audit_trail.raw_provider_output_included is False
    assert report.handoff_packet.target_version == "v0.29.9"
    assert report.handoff_packet.target_track == "External Provider Adapter Foundation Consolidation"
    assert report.handoff_packet.refs_only is True
    assert report.handoff_packet.implementation_performed_now is False
    assert {
        "provider_invocation",
        "provider_registration",
        "provider_sdk_invocation",
        "network_call",
        "credential_access",
        "command_execution",
        "live_adapter_runtime",
        "RPA_adapter_runtime",
        "external_agent_dominion_bridge",
    } <= set(report.handoff_packet.not_implemented_now)

    assert report.report_status == "warning"
    assert report.ready_for_v0_29_9 is True
    assert report.ready_for_v029_consolidation is True
    assert report.ready_for_preview_execution_now is False
    assert report.ready_for_provider_invocation is False
    assert report.ready_for_network_access is False
    assert report.ready_for_credential_access is False
    assert report.ready_for_command_execution is False

    pig = service.build_pig_report()
    assert pig["version"] == "v0.29.8"
    assert pig["subject"] == "limited_provider_invocation_preview_gate"
    assert pig["safety_boundary"]["preview_execution_performed"] is False
    assert pig["safety_boundary"]["provider_invoked"] is False
    assert pig["safety_boundary"]["network_called"] is False

    ocpx = service.build_ocpx_projection()
    assert ocpx["state"] == "limited_provider_invocation_preview_gate_created"
    assert "LimitedPreviewEligibilityMatrixState" in ocpx["target_read_models"]
    assert "LimitedPreviewHandoffState" in ocpx["target_read_models"]
    assert "limited_preview_gate_evaluated" in ocpx["effect_types"]

    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exit_code = main(["adapter", "preview", "report"])
    output = stdout.getvalue()
    assert exit_code == 0
    assert "version=v0.29.8" in output
    assert "ready_for_v0_29_9=true" in output
    assert "ready_for_v029_consolidation=true" in output
    assert "ready_for_preview_execution_now=false" in output
    assert "ready_for_provider_invocation=false" in output
    assert "provider_invoked=false" in output
    assert "network_called=false" in output
    assert "credential_accessed=false" in output
    assert "command_executed=false" in output


def test_report_forbidden_flags_and_mappings_remain_false() -> None:
    report = _report()

    forbidden_flags = [
        "preview_execution_performed",
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

    assert "limited_provider_invocation_preview_policy" in V0298_OBJECT_TYPES
    assert "limited_preview_gate" in V0298_OBJECT_TYPES
    assert "limited_provider_invocation_preview_report" in V0298_OBJECT_TYPES
    assert "limited_preview_policy_created" in V0298_EFFECT_TYPES
    assert "limited_preview_eligibility_matrix_created" in V0298_EFFECT_TYPES
    assert "limited_preview_handoff_packet_created" in V0298_EFFECT_TYPES
    assert "state_candidate_created" in V0298_EFFECT_TYPES
    assert "preview_execution_performed" in V0298_FORBIDDEN_EFFECT_TYPES
    assert "provider_invoked" in V0298_FORBIDDEN_EFFECT_TYPES
    assert "network_called" in V0298_FORBIDDEN_EFFECT_TYPES

    finding_types = {finding.finding_type for finding in report.findings}
    assert "limited_preview_policy_created" in finding_types
    assert "eligibility_matrix_created" in finding_types
    assert "preview_gate_created" in finding_types
    assert "provider_invocation_attempted" in LimitedPreviewFindingService.BLOCKED_FINDINGS
    assert "llm_judge_detected" in LimitedPreviewFindingService.BLOCKED_FINDINGS
