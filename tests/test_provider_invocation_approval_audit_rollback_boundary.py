from __future__ import annotations

import contextlib
import io

from chanta_core.cli.main import main
from chanta_core.provider_invocation_approval_audit_rollback_boundary import (
    ProviderInvocationApprovalAuditRollbackFindingService,
    ProviderInvocationApprovalAuditRollbackReportService,
    V0296_EFFECT_TYPES,
    V0296_FORBIDDEN_EFFECT_TYPES,
    V0296_OBJECT_TYPES,
)


def _report():
    return ProviderInvocationApprovalAuditRollbackReportService().build_report()


def test_policy_request_and_source_view_build() -> None:
    report = _report()
    policy = report.policy
    source = report.source_view

    assert report.version == "v0.29.6"
    assert policy.layer == "external_provider_adapter"
    assert policy.approval_boundary_enabled is True
    assert policy.audit_boundary_enabled is True
    assert policy.rollback_boundary_enabled is True
    assert policy.approval_required_before_provider_invocation is True
    assert policy.audit_required_before_provider_invocation is True
    assert policy.rollback_or_noop_required_before_provider_invocation is True
    assert policy.approval_candidate_is_not_approval_grant is True
    assert policy.approval_record_is_not_provider_invocation is True
    assert policy.audit_policy_is_not_raw_result_persistence is True
    assert policy.rollback_plan_is_not_rollback_execution is True
    assert policy.no_op_boundary_required is True
    assert policy.failure_classification_required is True
    assert policy.result_boundary_required is True
    assert policy.ocel_trace_required is True
    assert policy.provider_invocation_enabled_now is False
    assert policy.provider_sdk_invocation_enabled_now is False
    assert policy.network_access_enabled_now is False
    assert policy.credential_access_enabled_now is False
    assert policy.command_execution_expansion_enabled_now is False
    assert policy.rollback_execution_enabled_now is False
    assert policy.automatic_retry_enabled_now is False
    assert policy.live_adapter_implementation_enabled_now is False
    assert policy.rpa_adapter_enabled_now is False
    assert policy.external_agent_dominion_enabled_now is False
    assert policy.no_provider_invocation_default is True
    assert policy.no_network_default is True
    assert policy.no_credential_value_default is True
    assert policy.no_command_execution_default is True
    assert policy.llm_judge_as_sole_approval_authority_forbidden is True

    assert report.request.invocation_candidate_report_id
    assert report.request.credential_network_boundary_report_id
    assert report.request.permission_safety_report_id
    assert source.invocation_candidate_report_ref is not None
    assert source.invocation_readiness_gate_ref is not None
    assert source.invocation_candidate_refs
    assert source.dry_run_report_refs
    assert source.risk_preview_refs
    assert source.effect_preview_refs
    assert source.noop_plan_refs
    assert source.failure_mode_preview_refs
    assert source.credential_network_boundary_report_ref is not None
    assert source.credential_access_candidate_refs
    assert source.network_request_candidate_refs
    assert source.permission_safety_report_ref is not None
    assert source.permission_decision_record_refs
    assert source.user_approval_requirement_refs
    assert source.mock_harness_report_ref is not None
    assert source.adapter_registry_report_ref is not None
    assert source.audit_requirement_contract_ref is not None
    assert source.rollback_noop_requirement_contract_ref is not None
    assert source.ocel_visibility_contract_ref is not None
    assert source.provider_invocation_prohibition_ref is not None
    assert source.command_execution_prohibition_ref is not None
    assert source.invocation_candidate_ready_for_approval_boundary is True
    assert source.credential_network_ready_for_approval_boundary is True
    assert source.permission_safety_ready_for_approval_boundary is True
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
    assert source.private_data_detected is False
    assert source.raw_provider_output_detected is False


def test_approval_requirements_candidates_and_decisions_are_not_grants() -> None:
    report = _report()

    assert report.approval_requirements
    for requirement in report.approval_requirements:
        assert requirement.approval_required is True
        assert requirement.approval_scope_summary_required is True
        assert requirement.approval_expiry_required is True
        assert requirement.approval_revalidation_required is True
        assert requirement.approval_record_required is True
        assert requirement.explicit_user_approval_required_later is True
        assert requirement.approval_requirement_is_approval_grant is False

    for candidate in report.approval_candidates:
        assert candidate.approval_requirement_ref
        assert candidate.risk_preview_ref
        assert candidate.effect_preview_ref
        assert candidate.approval_candidate_status in {"allowed_candidate", "deferred"}
        assert candidate.approval_candidate_is_approval_grant is False
        assert candidate.approval_candidate_is_execution is False
        assert candidate.provider_invoked_now is False

    allowed_decisions = {
        "deny",
        "defer",
        "require_user_approval",
        "require_certification",
        "require_limited_preview_gate",
        "mock_only",
        "dry_run_only",
        "no_op",
        "unknown",
    }
    assert report.approval_decision_candidates
    for decision in report.approval_decision_candidates:
        assert decision.proposed_decision in allowed_decisions
        assert decision.decision_reason
        assert decision.approval_granted_now is False
        assert decision.provider_invoked_now is False

    for record in report.approval_decision_records:
        assert record.final_decision in allowed_decisions
        assert record.approval_granted_now is False
        assert record.provider_invoked_now is False
        assert record.network_called_now is False
        assert record.credential_accessed_now is False
        assert record.command_executed_now is False
        assert record.rollback_executed_now is False


def test_scope_expiry_revalidation_audit_and_ocel_boundaries() -> None:
    report = _report()

    for summary in report.approval_scope_summaries:
        assert summary.adapter_name
        assert summary.capability_name
        assert summary.scope_summary
        assert summary.provider_scope
        assert summary.payload_scope_summary
        assert summary.result_scope_summary
        assert summary.scope_is_minimal is True
        assert summary.scope_is_expiring is True

    assert report.approval_expiry_policy.approval_expiry_required is True
    assert report.approval_expiry_policy.permanent_approval_forbidden is True
    assert report.approval_expiry_policy.approval_reuse_forbidden_without_revalidation is True
    assert report.approval_expiry_policy.expired_approval_requires_reapproval is True
    assert report.approval_expiry_policy.approval_scope_change_requires_reapproval is True

    revalidation = report.approval_revalidation_policy
    assert revalidation.revalidation_required_before_preview is True
    assert revalidation.revalidate_permission_scope is True
    assert revalidation.revalidate_safety_classification is True
    assert revalidation.revalidate_credential_boundary is True
    assert revalidation.revalidate_network_boundary is True
    assert revalidation.revalidate_payload_boundary is True
    assert revalidation.revalidate_result_boundary is True
    assert revalidation.revalidation_is_not_execution is True

    audit = report.audit_policy
    assert audit.audit_required is True
    assert audit.approval_audit_required is True
    assert audit.invocation_candidate_audit_required is True
    assert audit.credential_reference_audit_required is True
    assert audit.network_candidate_audit_required is True
    assert audit.payload_preview_audit_required is True
    assert audit.effect_preview_audit_required is True
    assert audit.risk_preview_audit_required is True
    assert audit.failure_classification_audit_required is True
    assert audit.rollback_plan_audit_required is True
    assert audit.future_provider_result_audit_required is True
    assert audit.raw_provider_output_audit_forbidden is True
    assert audit.credential_value_audit_forbidden is True
    assert audit.raw_payload_audit_forbidden is True

    for plan in report.audit_event_plans:
        assert "approval_requirement_recorded" in plan.required_audit_events
        assert "approval_candidate_recorded" in plan.required_audit_events
        assert "approval_decision_recorded" in plan.required_audit_events
        assert "rollback_plan_recorded" in plan.required_audit_events
        assert "noop_boundary_recorded" in plan.required_audit_events
        assert "ocel_trace_plan_recorded" in plan.required_audit_events

    assert report.audit_trail.raw_content_included is False
    assert report.audit_trail.credential_value_included is False
    assert report.audit_trail.raw_payload_included is False
    assert report.audit_trail.raw_provider_output_included is False

    assert report.ocel_trace_policy.ocel_trace_required is True
    assert report.ocel_trace_policy.provider_invocation_event_emitted_now is False
    for plan in report.ocel_trace_plans:
        assert "provider_approval_requirement_recorded" in plan.required_event_types
        assert "provider_approval_candidate_created" in plan.required_event_types
        assert "provider_invocation_boundary_gate_evaluated" in plan.required_event_types
        assert "adapter_invocation_candidate" in plan.required_object_types
        assert "provider_approval_decision_record" in plan.required_object_types
        assert plan.provider_invocation_event_forbidden_now is True


def test_result_failure_rollback_noop_and_retry_boundaries() -> None:
    report = _report()

    result = report.result_boundary_policy
    assert result.provider_result_boundary_required is True
    assert result.raw_provider_output_persistence_forbidden is True
    assert result.raw_provider_output_memory_write_forbidden is True
    assert result.result_summary_required_later is True
    assert result.result_schema_validation_required_later is True
    assert result.result_redaction_required_later is True
    assert result.result_audit_required_later is True
    assert result.result_boundary_is_not_provider_response is True

    persistence = report.result_persistence_policy
    assert persistence.raw_result_persistence_forbidden is True
    assert persistence.raw_result_logging_forbidden is True
    assert persistence.result_summary_only_by_default_later is True
    assert persistence.redacted_result_boundary_required_later is True
    assert persistence.provider_result_persisted_now is False

    for classification in report.failure_classifications:
        assert "missing_permission" in classification.possible_failure_modes
        assert "missing_approval" in classification.possible_failure_modes
        assert "missing_credential" in classification.possible_failure_modes
        assert "missing_network_boundary" in classification.possible_failure_modes
        assert "unsafe_result" in classification.possible_failure_modes
        assert "rollback_unavailable" in classification.possible_failure_modes
        assert classification.retry_allowed_now is False
        assert classification.automatic_retry_allowed_now is False
        assert classification.rollback_required_later is True
        assert classification.noop_fallback_available is True

    failure_policy = report.failure_handling_policy
    assert failure_policy.failure_handling_required is True
    assert failure_policy.automatic_retry_forbidden_now is True
    assert failure_policy.retry_requires_future_policy is True
    assert failure_policy.auth_failure_retry_forbidden is True
    assert failure_policy.rate_limit_retry_requires_future_policy is True
    assert failure_policy.timeout_handling_required_later is True
    assert failure_policy.failure_must_emit_ocel_later is True
    assert failure_policy.noop_on_uncertain_failure_allowed is True

    rollback_policy = report.rollback_boundary_policy
    assert rollback_policy.rollback_boundary_required is True
    assert rollback_policy.rollback_plan_required_before_side_effect is True
    assert rollback_policy.rollback_execution_enabled_now is False
    assert rollback_policy.rollback_without_audit_forbidden is True
    assert rollback_policy.rollback_without_original_action_ref_forbidden is True
    assert rollback_policy.rollback_must_be_scope_limited is True
    assert rollback_policy.noop_fallback_required is True

    for plan in report.rollback_plans:
        assert plan.rollback_strategy in {"no_op_only", "manual_review_required"}
        assert plan.rollback_requires_future_approval is True
        assert plan.rollback_executed_now is False
        assert plan.rollback_plan_is_rollback_execution is False

    for noop in report.noop_boundaries:
        assert noop.noop_available is True
        assert noop.noop_is_valid_decision is True
        assert noop.noop_is_execution is False
        assert noop.side_effect_performed is False

    retry = report.retry_deferral_policy
    assert retry.automatic_retry_enabled_now is False
    assert retry.retry_policy_deferred is True
    assert retry.retry_requires_future_boundary is True
    assert retry.retry_requires_audit is True
    assert retry.retry_requires_rate_limit_policy is True
    assert retry.retry_requires_user_or_policy_approval is True


def test_gate_report_pig_ocpx_and_cli_build() -> None:
    service = ProviderInvocationApprovalAuditRollbackReportService()
    report = service.build_report()
    gate = report.approval_audit_rollback_gate

    assert gate.approval_requirements_complete is True
    assert gate.approval_candidates_complete is True
    assert gate.approval_decisions_recorded is True
    assert gate.scope_summaries_complete is True
    assert gate.audit_boundary_complete is True
    assert gate.ocel_trace_boundary_complete is True
    assert gate.result_boundary_complete is True
    assert gate.failure_classification_complete is True
    assert gate.rollback_or_noop_boundary_complete is True
    assert gate.retry_deferred is True
    assert gate.no_approval_granted is True
    assert gate.no_provider_invocation is True
    assert gate.no_network_call is True
    assert gate.no_credential_access is True
    assert gate.no_command_execution is True
    assert gate.no_external_side_effect is True
    assert gate.no_rollback_execution is True
    assert gate.ready_for_v0_29_7 is True
    assert gate.ready_for_certification_matrix is True
    assert gate.ready_for_limited_invocation_preview is False
    assert gate.ready_for_provider_invocation is False
    assert gate.ready_for_network_access is False
    assert gate.ready_for_credential_access is False
    assert gate.ready_for_command_execution is False

    assert report.report_status == "warning"
    assert report.ready_for_v0_29_7 is True
    assert report.ready_for_certification_matrix is True
    assert report.ready_for_limited_invocation_preview is False
    assert report.approval_granted is False
    assert report.provider_invoked is False
    assert report.network_called is False
    assert report.credential_accessed is False
    assert report.rollback_executed is False
    assert report.automatic_retry_performed is False

    pig = service.build_pig_report()
    assert pig["version"] == "v0.29.6"
    assert pig["subject"] == "provider_invocation_approval_audit_rollback_boundary"
    assert pig["safety_boundary"]["approval_granted"] is False
    assert pig["safety_boundary"]["provider_invoked"] is False
    assert pig["safety_boundary"]["rollback_executed"] is False

    ocpx = service.build_ocpx_projection()
    assert ocpx["state"] == "provider_invocation_approval_audit_rollback_boundary_created"
    assert "ProviderInvocationApprovalBoundaryState" in ocpx["target_read_models"]
    assert "ProviderRollbackPlanState" in ocpx["target_read_models"]
    assert "provider_invocation_approval_audit_rollback_gate_evaluated" in ocpx["effect_types"]

    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exit_code = main(["adapter", "approval", "report"])
    output = stdout.getvalue()
    assert exit_code == 0
    assert "version=v0.29.6" in output
    assert "ready_for_v0_29_7=true" in output
    assert "ready_for_provider_invocation=false" in output
    assert "ready_for_network_access=false" in output
    assert "ready_for_credential_access=false" in output
    assert "approval_granted=false" in output
    assert "rollback_executed=false" in output


def test_report_forbidden_flags_and_mappings_remain_false() -> None:
    report = _report()

    assert report.ready_for_limited_invocation_preview is False
    assert report.ready_for_provider_invocation is False
    assert report.ready_for_network_access is False
    assert report.ready_for_credential_access is False
    assert report.ready_for_command_execution is False
    assert report.approval_granted is False
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

    assert "provider_invocation_approval_audit_rollback_policy" in V0296_OBJECT_TYPES
    assert "provider_invocation_approval_audit_rollback_report" in V0296_OBJECT_TYPES
    assert "provider_invocation_approval_candidate_created" in V0296_EFFECT_TYPES
    assert "provider_rollback_plan_created" in V0296_EFFECT_TYPES
    assert "state_candidate_created" in V0296_EFFECT_TYPES
    assert "approval_granted" in V0296_FORBIDDEN_EFFECT_TYPES
    assert "provider_invoked" in V0296_FORBIDDEN_EFFECT_TYPES
    assert "rollback_executed" in V0296_FORBIDDEN_EFFECT_TYPES

    finding_types = {finding.finding_type for finding in report.findings}
    assert "approval_audit_rollback_policy_created" in finding_types
    assert "approval_decision_record_created" in finding_types
    assert "approval_audit_rollback_gate_created" in finding_types
    assert "approval_grant_attempted" in ProviderInvocationApprovalAuditRollbackFindingService.BLOCKED_FINDINGS
    assert "llm_judge_detected" in ProviderInvocationApprovalAuditRollbackFindingService.BLOCKED_FINDINGS
