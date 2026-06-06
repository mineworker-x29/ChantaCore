from __future__ import annotations

import contextlib
import io

from chanta_core.adapter_invocation_candidate_dry_run_plan import (
    AdapterInvocationCandidateFindingService,
    AdapterInvocationCandidateReportService,
    V0295_EFFECT_TYPES,
    V0295_FORBIDDEN_EFFECT_TYPES,
    V0295_OBJECT_TYPES,
)
from chanta_core.cli.main import main


def _report():
    return AdapterInvocationCandidateReportService().build_report()


def test_adapter_invocation_candidate_policy_and_source_view_build() -> None:
    report = _report()

    assert report.version == "v0.29.5"
    assert report.policy.layer == "external_provider_adapter"
    assert report.policy.invocation_candidate_enabled is True
    assert report.policy.dry_run_plan_enabled is True
    assert report.policy.dry_run_report_enabled is True
    assert report.policy.payload_preview_required is True
    assert report.policy.output_schema_preview_required is True
    assert report.policy.effect_preview_required is True
    assert report.policy.risk_preview_required is True
    assert report.policy.no_op_plan_required is True
    assert report.policy.credential_reference_check_required is True
    assert report.policy.network_boundary_check_required is True
    assert report.policy.permission_safety_check_required is True
    assert report.policy.provider_invocation_enabled_now is False
    assert report.policy.provider_sdk_invocation_enabled_now is False
    assert report.policy.network_access_enabled_now is False
    assert report.policy.credential_access_enabled_now is False
    assert report.policy.secret_retrieval_enabled_now is False
    assert report.policy.command_execution_expansion_enabled_now is False
    assert report.policy.live_adapter_implementation_enabled_now is False
    assert report.policy.rpa_adapter_enabled_now is False
    assert report.policy.external_agent_dominion_enabled_now is False
    assert report.policy.dry_run_is_not_provider_call is True
    assert report.policy.invocation_candidate_is_not_invocation is True
    assert report.policy.payload_preview_is_not_payload_send is True
    assert report.policy.effect_preview_is_not_side_effect is True
    assert report.policy.risk_preview_is_not_approval is True
    assert report.policy.no_provider_invocation_default is True
    assert report.policy.no_network_default is True
    assert report.policy.no_credential_value_default is True
    assert report.policy.llm_judge_as_sole_invocation_candidate_authority_forbidden is True

    source = report.source_view
    assert source.credential_network_boundary_report_ref is not None
    assert source.credential_network_gate_ref is not None
    assert source.credential_access_candidate_refs
    assert source.network_request_candidate_refs
    assert source.payload_boundary_policy_ref is not None
    assert source.request_response_redaction_boundary_ref is not None
    assert source.data_exfiltration_boundary_policy_ref is not None
    assert source.provider_sdk_boundary_report_refs
    assert source.permission_safety_report_ref is not None
    assert source.permission_decision_record_refs
    assert source.safety_classification_refs
    assert source.action_intent_refs
    assert source.action_scope_refs
    assert source.mock_harness_report_ref is not None
    assert source.mock_run_report_refs
    assert source.adapter_registry_report_ref is not None
    assert source.adapter_capability_declaration_refs
    assert source.effect_boundary_contract_ref is not None
    assert source.input_schema_contract_ref is not None
    assert source.output_schema_contract_ref is not None
    assert source.provider_invocation_prohibition_ref is not None
    assert source.command_execution_prohibition_ref is not None
    assert source.credential_network_ready_for_candidate is True
    assert source.permission_safety_ready_for_candidate is True
    assert source.mock_ready_for_candidate is True
    assert source.provider_invocation_detected is False
    assert source.provider_sdk_invocation_detected is False
    assert source.network_call_detected is False
    assert source.credential_access_detected is False
    assert source.secret_retrieval_detected is False
    assert source.command_execution_detected is False
    assert source.live_adapter_detected is False
    assert source.private_data_detected is False
    assert source.raw_provider_output_detected is False


def test_intents_candidates_envelopes_and_previews_are_candidate_only() -> None:
    report = _report()

    assert report.invocation_intents
    assert {intent.action_kind for intent in report.invocation_intents} >= {
        "mock_only",
        "external_read_candidate",
        "external_side_effect_candidate",
        "rpa_deferred",
    }
    assert all(intent.intent_allowed_as_candidate for intent in report.invocation_intents)
    assert all(not intent.intent_allowed_as_live_invocation for intent in report.invocation_intents)

    assert report.invocation_candidates
    for candidate in report.invocation_candidates:
        assert candidate.intent_ref
        assert candidate.provider_invocation_candidate_is_invocation is False
        assert candidate.provider_invoked_now is False
        assert candidate.provider_sdk_invoked_now is False
        assert candidate.network_called_now is False
        assert candidate.credential_accessed_now is False
        assert candidate.command_executed_now is False
        assert candidate.required_next_gate == "v0.29.6 Provider Invocation Approval / Audit / Rollback Boundary"

    assert report.input_envelopes
    for envelope in report.input_envelopes:
        assert envelope.synthetic_or_metadata_only is True
        assert envelope.contains_actual_user_data is False
        assert envelope.contains_actual_company_data is False
        assert envelope.contains_private_data is False
        assert envelope.contains_credentials is False
        assert envelope.contains_raw_trace is False
        assert envelope.contains_raw_transcript is False
        assert envelope.contains_raw_provider_output is False

    for preview in report.payload_previews:
        assert preview.payload_preview_allowed is True
        assert preview.payload_preview_is_payload_send is False
        assert preview.outbound_payload_sent_now is False
        assert preview.contains_credentials is False
        assert preview.contains_private_data is False
        assert preview.contains_raw_artifacts is False

    for preview in report.output_schema_previews:
        assert preview.expected_fields
        assert preview.expected_error_fields
        assert preview.redaction_required is True
        assert preview.raw_provider_output_persistence_forbidden is True
        assert preview.output_schema_preview_is_provider_response is False
        assert preview.provider_response_received_now is False


def test_checks_effect_risk_and_dry_run_artifacts_are_no_live_execution() -> None:
    report = _report()

    for check in report.credential_reference_checks:
        assert check.credential_value_accessed_now is False
        assert check.credential_value_stored_now is False
        assert check.credential_value_logged_now is False
        assert check.secret_retrieved_now is False

    for check in report.network_boundary_checks:
        assert check.network_called_now is False
        assert check.outbound_request_sent_now is False
        assert check.provider_sdk_network_called_now is False

    for check in report.permission_safety_checks:
        assert check.permission_granted_now is False
        assert check.approval_granted_now is False

    for preview in report.effect_previews:
        assert preview.predicted_effect_types
        assert preview.forbidden_effect_types_detected == []
        assert preview.external_side_effect_performed_now is False
        assert preview.file_mutated_now is False
        assert preview.provider_invoked_now is False
        assert preview.network_called_now is False
        assert preview.command_executed_now is False
        assert preview.effect_preview_is_side_effect is False

    for preview in report.risk_previews:
        assert "credential_exposure" in preview.risk_dimensions
        assert "network_access" in preview.risk_dimensions
        assert "provider_side_effect" in preview.risk_dimensions
        assert "rollback_gap" in preview.risk_dimensions
        assert "RPA_scope_creep" in preview.risk_dimensions
        assert "external_dominion_creep" in preview.risk_dimensions
        assert preview.risk_preview_is_approval is False
        assert preview.blocks_dry_run is False

    for plan in report.dry_run_plans:
        assert plan.dry_run_steps
        assert plan.dry_run_allowed_now is True
        assert plan.live_provider_allowed is False
        assert plan.network_allowed is False
        assert plan.credential_access_allowed is False
        assert plan.command_execution_allowed is False
        assert plan.external_side_effect_allowed is False
        for step in plan.dry_run_steps:
            assert step.step_is_live_call is False
            assert step.step_invokes_provider is False
            assert step.step_calls_network is False
            assert step.step_accesses_credentials is False
            assert step.step_executes_command is False

    for dry_report in report.dry_run_reports:
        assert dry_report.provider_invoked is False
        assert dry_report.provider_sdk_invoked is False
        assert dry_report.network_called is False
        assert dry_report.credential_accessed is False
        assert dry_report.credential_stored is False
        assert dry_report.credential_logged is False
        assert dry_report.command_executed is False
        assert dry_report.external_side_effect_performed is False
        assert dry_report.raw_provider_output_persisted is False


def test_noop_failure_gate_audit_and_report_readiness() -> None:
    report = _report()

    assert report.noop_plans
    for noop in report.noop_plans:
        assert noop.noop_available is True
        assert set(noop.fallback_decisions) >= {
            "deny",
            "defer",
            "mock_only",
            "dry_run_only",
            "require_v0296_approval",
            "require_v0298_preview_gate",
        }
        assert noop.noop_is_execution is False
        assert noop.side_effect_performed is False

    for failure in report.failure_mode_previews:
        assert "missing_permission" in failure.possible_failure_modes
        assert "missing_credential_boundary" in failure.possible_failure_modes
        assert "missing_network_boundary" in failure.possible_failure_modes
        assert "missing_approval" in failure.possible_failure_modes
        assert "schema_mismatch" in failure.possible_failure_modes
        assert "provider_error" in failure.possible_failure_modes
        assert "timeout" in failure.possible_failure_modes
        assert "auth_failure" in failure.possible_failure_modes
        assert "rate_limit" in failure.possible_failure_modes
        assert "unsafe_payload" in failure.possible_failure_modes
        assert failure.failure_classification_required_later is True
        assert failure.rollback_or_noop_required_later is True

    gate = report.readiness_gate
    assert gate.candidate_generation_complete is True
    assert gate.payload_previews_complete is True
    assert gate.output_schema_previews_complete is True
    assert gate.credential_checks_passed_or_deferred is True
    assert gate.network_checks_passed_or_deferred is True
    assert gate.permission_safety_checks_passed_or_deferred is True
    assert gate.effect_previews_complete is True
    assert gate.risk_previews_complete is True
    assert gate.dry_run_plans_complete is True
    assert gate.dry_run_reports_complete_or_safely_deferred is True
    assert gate.noop_plans_available is True
    assert gate.no_provider_invocation is True
    assert gate.no_network_call is True
    assert gate.no_credential_access is True
    assert gate.no_command_execution is True
    assert gate.no_external_side_effect is True
    assert gate.ready_for_v0_29_6 is True
    assert gate.ready_for_approval_audit_rollback_boundary is True
    assert gate.ready_for_provider_invocation is False
    assert gate.ready_for_network_access is False
    assert gate.ready_for_credential_access is False
    assert gate.ready_for_command_execution is False

    assert report.audit_trail.raw_content_included is False
    assert report.audit_trail.credential_value_included is False
    assert report.audit_trail.raw_payload_included is False
    assert report.audit_trail.raw_provider_output_included is False
    assert report.report_status == "warning"
    assert report.ready_for_v0_29_6 is True
    assert report.ready_for_approval_audit_rollback_boundary is True


def test_report_forbidden_flags_remain_false_and_mappings_exist() -> None:
    report = _report()

    assert report.ready_for_provider_invocation is False
    assert report.ready_for_network_access is False
    assert report.ready_for_credential_access is False
    assert report.ready_for_command_execution is False
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

    assert "adapter_invocation_candidate_policy" in V0295_OBJECT_TYPES
    assert "adapter_invocation_candidate_report" in V0295_OBJECT_TYPES
    assert "adapter_invocation_candidate_created" in V0295_EFFECT_TYPES
    assert "adapter_dry_run_plan_created" in V0295_EFFECT_TYPES
    assert "state_candidate_created" in V0295_EFFECT_TYPES
    assert "provider_invoked" in V0295_FORBIDDEN_EFFECT_TYPES
    assert "network_called" in V0295_FORBIDDEN_EFFECT_TYPES
    assert "credential_accessed" in V0295_FORBIDDEN_EFFECT_TYPES

    finding_types = {finding.finding_type for finding in report.findings}
    assert "invocation_candidate_policy_created" in finding_types
    assert "dry_run_plan_created" in finding_types
    assert "readiness_gate_created" in finding_types
    assert "provider_invocation_attempted" in AdapterInvocationCandidateFindingService.BLOCKED_FINDINGS
    assert "llm_judge_detected" in AdapterInvocationCandidateFindingService.BLOCKED_FINDINGS


def test_pig_ocpx_and_cli_report_build() -> None:
    service = AdapterInvocationCandidateReportService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert pig["version"] == "v0.29.5"
    assert pig["subject"] == "adapter_invocation_candidate_dry_run_plan"
    assert pig["safety_boundary"]["provider_invoked"] is False
    assert pig["safety_boundary"]["network_called"] is False
    assert pig["safety_boundary"]["credential_accessed"] is False
    assert pig["next_step"] == "v0.29.6 Provider Invocation Approval / Audit / Rollback Boundary"
    assert ocpx["state"] == "adapter_invocation_candidate_dry_run_plan_created"
    assert "AdapterInvocationCandidateState" in ocpx["target_read_models"]
    assert "AdapterDryRunPlanState" in ocpx["target_read_models"]
    assert "adapter_invocation_readiness_gate_evaluated" in ocpx["effect_types"]

    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exit_code = main(["adapter", "invocation", "report"])
    output = stdout.getvalue()
    assert exit_code == 0
    assert "version=v0.29.5" in output
    assert "ready_for_v0_29_6=true" in output
    assert "ready_for_provider_invocation=false" in output
    assert "ready_for_network_access=false" in output
    assert "ready_for_credential_access=false" in output
    assert "ready_for_command_execution=false" in output
