from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.permission_safety_scope_gate_for_external_adapters import (
    AdapterActionIntent,
    AdapterActionScope,
    AdapterApprovalCandidate,
    AdapterDenyFirstRuleSet,
    AdapterPermissionDecisionCandidate,
    AdapterPermissionDecisionRecord,
    AdapterPermissionPolicy,
    AdapterPermissionSafetyAuditTrail,
    AdapterPermissionSafetyGate,
    AdapterPermissionSafetyReport,
    AdapterPermissionSafetyReportService,
    AdapterPermissionSafetyRequest,
    AdapterPermissionSafetySourceView,
    AdapterPermissionScopeEvaluation,
    AdapterSafetyClassification,
    AdapterSafetyFinding,
    AdapterSafetyPolicy,
    AdapterScopeExpiryPolicy,
    AdapterScopeMatrix,
    AdapterScopeMatrixRow,
    AdapterScopePolicy,
    CommandLikeActionSafetyCheck,
    CredentialReferenceSafetyCheck,
    DataExfiltrationSafetyCheck,
    ExternalAdapterPermissionSafetyPolicy,
    ExternalSideEffectSafetyCheck,
    NetworkNeedSafetyCheck,
    PrivateDataSafetyCheck,
    RPAScopeDeferralCheck,
    UserApprovalRequirement,
    V0293_EFFECT_TYPES,
    V0293_FORBIDDEN_EFFECT_TYPES,
    V0293_OBJECT_TYPES,
)


def _report() -> AdapterPermissionSafetyReport:
    return AdapterPermissionSafetyReportService().build_report()


def test_v0293_permission_safety_models_build() -> None:
    report = _report()

    assert isinstance(report.policy, ExternalAdapterPermissionSafetyPolicy)
    assert isinstance(report.request, AdapterPermissionSafetyRequest)
    assert isinstance(report.source_view, AdapterPermissionSafetySourceView)
    assert isinstance(report.permission_policy, AdapterPermissionPolicy)
    assert isinstance(report.safety_policy, AdapterSafetyPolicy)
    assert isinstance(report.scope_policy, AdapterScopePolicy)
    assert isinstance(report.deny_first_rule_set, AdapterDenyFirstRuleSet)
    assert all(isinstance(item, AdapterActionIntent) for item in report.action_intents)
    assert all(isinstance(item, AdapterActionScope) for item in report.action_scopes)
    assert isinstance(report.scope_matrix, AdapterScopeMatrix)
    assert all(isinstance(item, AdapterScopeMatrixRow) for item in report.scope_matrix.rows)
    assert all(isinstance(item, AdapterPermissionScopeEvaluation) for item in report.permission_scope_evaluations)
    assert all(isinstance(item, AdapterSafetyClassification) for item in report.safety_classifications)
    assert all(isinstance(item, AdapterSafetyFinding) for item in report.safety_findings)
    assert all(isinstance(item, UserApprovalRequirement) for item in report.approval_requirements)
    assert all(isinstance(item, AdapterApprovalCandidate) for item in report.approval_candidates)
    assert all(isinstance(item, AdapterPermissionDecisionCandidate) for item in report.decision_candidates)
    assert all(isinstance(item, AdapterPermissionDecisionRecord) for item in report.decision_records)
    assert isinstance(report.scope_expiry_policy, AdapterScopeExpiryPolicy)
    assert all(isinstance(item, PrivateDataSafetyCheck) for item in report.private_data_safety_checks)
    assert all(isinstance(item, CredentialReferenceSafetyCheck) for item in report.credential_safety_checks)
    assert all(isinstance(item, NetworkNeedSafetyCheck) for item in report.network_safety_checks)
    assert all(isinstance(item, CommandLikeActionSafetyCheck) for item in report.command_like_action_checks)
    assert all(isinstance(item, ExternalSideEffectSafetyCheck) for item in report.external_side_effect_checks)
    assert all(isinstance(item, DataExfiltrationSafetyCheck) for item in report.data_exfiltration_checks)
    assert all(isinstance(item, RPAScopeDeferralCheck) for item in report.rpa_deferral_checks)
    assert isinstance(report.permission_safety_gate, AdapterPermissionSafetyGate)
    assert isinstance(report.audit_trail, AdapterPermissionSafetyAuditTrail)


def test_v0293_policy_source_and_deny_first_rules() -> None:
    report = _report()
    policy = report.policy
    source = report.source_view
    deny_first = report.deny_first_rule_set

    assert report.version == "v0.29.3"
    assert policy.layer == "external_provider_adapter"
    assert policy.permission_safety_gate_enabled is True
    assert policy.deny_first_required is True
    assert policy.scoped_permission_required is True
    assert policy.permission_expiry_required is True
    assert policy.user_approval_requirement_enabled is True
    assert policy.permission_decision_record_required is True
    assert policy.safety_classification_required is True
    assert policy.private_data_check_required is True
    assert policy.credential_sensitivity_check_required is True
    assert policy.network_sensitivity_check_required is True
    assert policy.external_side_effect_check_required is True
    assert policy.data_exfiltration_check_required is True
    assert policy.command_like_action_forbidden_now is True
    assert policy.rpa_action_deferred is True
    assert policy.approval_candidate_is_not_execution is True
    assert policy.permission_gate_is_not_permission_grant is True
    assert policy.safety_gate_is_not_invocation is True
    assert policy.real_permission_grant_enabled_now is False
    assert policy.provider_registration_enabled_now is False
    assert policy.provider_invocation_enabled_now is False
    assert policy.network_access_enabled_now is False
    assert policy.credential_storage_enabled_now is False
    assert policy.command_execution_expansion_enabled_now is False
    assert policy.live_adapter_implementation_enabled_now is False
    assert policy.rpa_adapter_enabled_now is False
    assert policy.external_agent_dominion_enabled_now is False
    assert policy.schumpeter_private_runtime_enabled_now is False
    assert policy.PIG_execution_authority_forbidden is True
    assert policy.llm_judge_as_sole_permission_safety_authority_forbidden is True

    assert source.mock_harness_report_ref is not None
    assert source.mock_harness_gate_ref is not None
    assert source.mock_run_report_refs
    assert source.mock_effect_boundary_validation_refs
    assert source.no_network_boundary_report_refs
    assert source.provider_sdk_isolation_report_refs
    assert source.mock_credential_boundary_report_refs
    assert source.mock_adapter_ocel_trace_report_refs
    assert source.adapter_registry_report_ref is not None
    assert source.adapter_registry_ref is not None
    assert source.adapter_capability_declaration_refs
    assert source.adapter_risk_profile_refs
    assert source.permission_scope_requirement_refs
    assert source.safety_scope_requirement_refs
    assert source.credential_need_declaration_refs
    assert source.network_need_declaration_refs
    assert source.provider_invocation_prohibition_ref is not None
    assert source.command_execution_prohibition_ref is not None
    assert source.mock_harness_ready_for_permission_safety is True
    assert source.provider_invocation_detected is False
    assert source.network_call_detected is False
    assert source.command_execution_detected is False
    assert source.credential_value_detected is False
    assert source.live_adapter_detected is False
    assert source.private_data_detected is False
    assert source.raw_provider_output_detected is False

    assert deny_first.deny_first_enabled is True
    assert deny_first.default_decision == "deny"
    for decision in [
        "deny",
        "defer",
        "require_user_approval",
        "require_future_credential_boundary",
        "require_future_network_boundary",
        "mock_only",
        "dry_run_only",
        "no_op",
    ]:
        assert decision in deny_first.allowed_decisions
    for rule in [
        "deny_if_provider_invocation_required_now",
        "deny_if_network_required_now",
        "deny_if_credential_value_required_now",
        "deny_if_command_execution_required_now",
        "deny_if_private_data_required_now",
        "deny_if_raw_provider_output_persistence_required",
        "deny_if_rpa_action_required_now",
        "deny_if_external_dominion_required_now",
        "deny_if_missing_scope",
        "deny_if_missing_safety_classification",
    ]:
        assert rule in deny_first.deny_rules


def test_v0293_permission_safety_scope_policies_and_matrix() -> None:
    report = _report()

    assert report.permission_policy.deny_first_default is True
    assert report.permission_policy.permission_required_for_external_action is True
    assert report.permission_policy.permission_scope_required is True
    assert report.permission_policy.permission_expiry_required is True
    assert report.permission_policy.approval_record_required is True
    assert report.permission_policy.permission_restoration_without_approval_forbidden is True
    assert report.permission_policy.ambient_permission_forbidden is True
    assert report.permission_policy.wildcard_permission_forbidden is True
    assert report.permission_policy.permission_grant_enabled_now is False
    assert report.permission_policy.permission_grant_candidate_enabled is True

    assert report.safety_policy.safety_classification_required is True
    assert report.safety_policy.safety_gate_required_for_external_action is True
    assert report.safety_policy.private_data_safety_check_required is True
    assert report.safety_policy.credential_safety_check_required is True
    assert report.safety_policy.network_safety_check_required is True
    assert report.safety_policy.external_side_effect_check_required is True
    assert report.safety_policy.data_exfiltration_check_required is True
    assert report.safety_policy.command_like_action_forbidden_now is True
    assert report.safety_policy.rpa_action_future_track is True
    assert report.safety_policy.unsafe_action_blocks_approval_candidate is True

    assert report.scope_policy.scope_required is True
    assert report.scope_policy.scope_must_be_minimal is True
    assert report.scope_policy.scope_must_be_expiring is True
    assert report.scope_policy.scope_must_be_action_specific is True
    assert report.scope_policy.scope_must_reference_adapter_and_capability is True
    assert report.scope_policy.broad_external_scope_forbidden is True
    assert report.scope_policy.wildcard_scope_forbidden is True
    assert report.scope_policy.private_data_scope_requires_future_boundary is True
    assert report.scope_policy.credential_scope_requires_v0294 is True
    assert report.scope_policy.network_scope_requires_v0294 is True
    assert report.scope_policy.command_scope_forbidden_now is True

    action_kinds = {intent.action_kind for intent in report.action_intents}
    assert {"mock_action", "external_read", "external_side_effect", "rpa_action"} <= action_kinds
    assert any(intent.requires_network for intent in report.action_intents)
    assert any(intent.requires_credentials for intent in report.action_intents)
    assert any(intent.requires_command_execution for intent in report.action_intents)
    assert all(scope.scope_grant_allowed_now is False for scope in report.action_scopes)
    assert report.scope_matrix.adapter_count == len(report.action_scopes)
    assert report.scope_matrix.safe_mock_only_count >= 1
    assert report.scope_matrix.approval_required_count >= 1
    assert report.scope_matrix.deferred_count >= 1


def test_v0293_evaluations_classifications_approval_and_decisions_do_not_grant() -> None:
    report = _report()

    assert all(item.scope_expiry_required is True for item in report.permission_scope_evaluations)
    assert all(item.approval_record_required is True for item in report.permission_scope_evaluations)
    assert all(item.real_permission_granted_now is False for item in report.permission_scope_evaluations)

    safety_classes = {item.safety_class for item in report.safety_classifications}
    assert "safe_mock_only" in safety_classes
    assert "blocked_credential_sensitive" in safety_classes
    assert "blocked_network_required" in safety_classes
    assert "blocked_external_side_effect" in safety_classes
    assert "blocked_rpa_future_track" in safety_classes
    assert any(item.blocks_permission_candidate for item in report.safety_classifications)
    assert any(item.requires_future_credential_boundary for item in report.safety_classifications)
    assert any(item.requires_future_network_boundary for item in report.safety_classifications)
    assert any(item.requires_future_audit_rollback for item in report.safety_classifications)

    assert all(requirement.approval_is_execution is False for requirement in report.approval_requirements)
    assert all(requirement.approval_granted_now is False for requirement in report.approval_requirements)
    assert all(candidate.approval_candidate_is_permission_grant is False for candidate in report.approval_candidates)
    assert all(candidate.approval_candidate_is_execution is False for candidate in report.approval_candidates)
    assert all(candidate.provider_invoked_now is False for candidate in report.approval_candidates)
    assert {"mock_only", "require_future_credential_boundary", "require_future_network_boundary", "defer"} <= {item.proposed_decision for item in report.decision_candidates}
    assert all(record.permission_granted_now is False for record in report.decision_records)
    assert all(record.approval_granted_now is False for record in report.decision_records)
    assert all(record.provider_invoked_now is False for record in report.decision_records)
    assert all(record.network_called_now is False for record in report.decision_records)
    assert all(record.command_executed_now is False for record in report.decision_records)


def test_v0293_expiry_safety_checks_gate_and_report_boundaries() -> None:
    report = _report()
    gate = report.permission_safety_gate

    assert report.scope_expiry_policy.scope_expiry_required is True
    assert report.scope_expiry_policy.permanent_permission_forbidden is True
    assert report.scope_expiry_policy.silent_permission_restoration_forbidden is True
    assert report.scope_expiry_policy.expired_permission_must_require_reapproval is True
    assert all(item.private_data_detected is False for item in report.private_data_safety_checks)
    assert all(item.actual_user_data_detected is False for item in report.private_data_safety_checks)
    assert all(item.actual_company_data_detected is False for item in report.private_data_safety_checks)
    assert any(item.credentials_required_later for item in report.credential_safety_checks)
    assert all(item.credential_value_required_now is False for item in report.credential_safety_checks)
    assert all(item.credential_value_detected is False for item in report.credential_safety_checks)
    assert all(item.credential_storage_detected is False for item in report.credential_safety_checks)
    assert all(item.credential_logging_detected is False for item in report.credential_safety_checks)
    assert all(item.credential_boundary_future_version == "v0.29.4" for item in report.credential_safety_checks)
    assert any(item.network_required_later for item in report.network_safety_checks)
    assert all(item.network_required_now is False for item in report.network_safety_checks)
    assert all(item.network_called_now is False for item in report.network_safety_checks)
    assert all(item.provider_sdk_network_detected is False for item in report.network_safety_checks)
    assert all(item.network_boundary_future_version == "v0.29.4" for item in report.network_safety_checks)
    assert all(item.command_executed_now is False for item in report.command_like_action_checks)
    assert all(item.shell_true_detected is False for item in report.command_like_action_checks)
    assert all(item.unbounded_subprocess_detected is False for item in report.command_like_action_checks)
    assert all(item.command_like_action_blocks_now is True for item in report.command_like_action_checks)
    assert any(item.external_side_effect_possible for item in report.external_side_effect_checks)
    assert all(item.external_side_effect_performed_now is False for item in report.external_side_effect_checks)
    assert all(item.requires_future_approval_audit_rollback is True for item in report.external_side_effect_checks)
    assert all(item.future_gate_version == "v0.29.6" for item in report.external_side_effect_checks)
    assert all(item.private_data_exfiltrated_now is False for item in report.data_exfiltration_checks)
    assert all(item.raw_provider_output_persisted_now is False for item in report.data_exfiltration_checks)
    assert any(item.rpa_action for item in report.rpa_deferral_checks)
    assert all(item.rpa_adapter_implemented_now is False for item in report.rpa_deferral_checks)
    assert all(item.rpa_action_deferred is True for item in report.rpa_deferral_checks)

    assert gate.deny_first_passed is True
    assert gate.scope_evaluation_complete is True
    assert gate.safety_classification_complete is True
    assert gate.approval_requirements_complete is True
    assert gate.private_data_checks_passed is True
    assert gate.credential_checks_passed_or_deferred is True
    assert gate.network_checks_passed_or_deferred is True
    assert gate.command_like_actions_blocked is True
    assert gate.external_side_effects_deferred is True
    assert gate.rpa_actions_deferred is True
    assert gate.no_permission_granted is True
    assert gate.no_provider_invocation is True
    assert gate.no_network_call is True
    assert gate.no_credential_storage is True
    assert gate.no_command_execution is True
    assert gate.ready_for_v0_29_4 is True
    assert gate.ready_for_credential_network_boundary is True
    assert gate.ready_for_invocation_candidate is False
    assert gate.ready_for_provider_invocation is False
    assert gate.ready_for_command_execution is False
    assert report.ready_for_v0_29_4 is True
    assert report.ready_for_credential_network_boundary is True
    assert report.ready_for_invocation_candidate is False
    assert report.ready_for_provider_invocation is False
    assert report.ready_for_command_execution is False


def test_v0293_ocel_pig_ocpx_and_cli_commands_work() -> None:
    service = AdapterPermissionSafetyReportService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert "external_adapter_permission_safety_policy" in V0293_OBJECT_TYPES
    assert "adapter_permission_safety_policy_created" in V0293_EFFECT_TYPES
    assert "real_permission_granted" in V0293_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.29.3"
    assert pig["subject"] == "permission_safety_scope_gate_for_external_adapters"
    assert pig["safety_boundary"]["real_permission_granted"] is False
    assert pig["safety_boundary"]["approval_granted"] is False
    assert pig["safety_boundary"]["provider_invoked"] is False
    assert ocpx["state"] == "adapter_permission_safety_scope_gate_created"
    assert "AdapterPermissionSafetyGateState" in ocpx["target_read_models"]
    assert "AdapterScopeMatrixState" in ocpx["target_read_models"]
    assert "AdapterSafetyCheckState" in ocpx["target_read_models"]

    for command in [
        "policy",
        "source-view",
        "permission-policy",
        "safety-policy",
        "scope-policy",
        "deny-first",
        "intents",
        "scopes",
        "scope-matrix",
        "permission-evaluation",
        "safety-classification",
        "approval-requirements",
        "approval-candidates",
        "decision-records",
        "expiry",
        "private-data",
        "credentials",
        "network",
        "command-like",
        "side-effects",
        "exfiltration",
        "rpa-deferral",
        "evaluate",
        "audit",
        "report",
    ]:
        assert main(["adapter", "gate", command]) == 0
