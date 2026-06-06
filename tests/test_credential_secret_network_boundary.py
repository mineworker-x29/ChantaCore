from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.credential_secret_network_boundary import (
    CredentialAccessCandidate,
    CredentialAuditPolicy,
    CredentialBoundaryPolicy,
    CredentialBoundaryReport,
    CredentialMaterialClassification,
    CredentialNetworkBoundaryAuditTrail,
    CredentialNetworkBoundaryGate,
    CredentialNetworkBoundaryReport,
    CredentialNetworkBoundaryReportService,
    CredentialNetworkBoundaryRequest,
    CredentialNetworkBoundarySourceView,
    CredentialRedactionPolicy,
    CredentialScopeBinding,
    CredentialSecretNetworkBoundaryPolicy,
    DataExfiltrationBoundaryPolicy,
    ExternalSecretStoreContract,
    NetworkAuditBoundary,
    NetworkBoundaryPolicy,
    NetworkRequestCandidate,
    NetworkRequestPolicy,
    NetworkTimeoutRetryPolicy,
    OutboundDomainPolicy,
    OutboundDomainRule,
    PayloadBoundaryPolicy,
    ProviderSDKBoundaryPolicy,
    ProviderSDKBoundaryReport,
    RequestResponseRedactionBoundary,
    SecretReferenceDescriptor,
    SecretReferencePolicy,
    V0294_EFFECT_TYPES,
    V0294_FORBIDDEN_EFFECT_TYPES,
    V0294_OBJECT_TYPES,
)


def _report() -> CredentialNetworkBoundaryReport:
    return CredentialNetworkBoundaryReportService().build_report()


def test_v0294_credential_network_boundary_models_build() -> None:
    report = _report()

    assert isinstance(report.policy, CredentialSecretNetworkBoundaryPolicy)
    assert isinstance(report.request, CredentialNetworkBoundaryRequest)
    assert isinstance(report.source_view, CredentialNetworkBoundarySourceView)
    assert isinstance(report.credential_boundary_policy, CredentialBoundaryPolicy)
    assert all(isinstance(item, CredentialMaterialClassification) for item in report.credential_material_classifications)
    assert isinstance(report.secret_reference_policy, SecretReferencePolicy)
    assert all(isinstance(item, SecretReferenceDescriptor) for item in report.secret_reference_descriptors)
    assert isinstance(report.external_secret_store_contract, ExternalSecretStoreContract)
    assert isinstance(report.credential_redaction_policy, CredentialRedactionPolicy)
    assert isinstance(report.credential_audit_policy, CredentialAuditPolicy)
    assert all(isinstance(item, CredentialScopeBinding) for item in report.credential_scope_bindings)
    assert all(isinstance(item, CredentialAccessCandidate) for item in report.credential_access_candidates)
    assert isinstance(report.credential_boundary_report, CredentialBoundaryReport)
    assert isinstance(report.network_boundary_policy, NetworkBoundaryPolicy)
    assert isinstance(report.outbound_domain_policy, OutboundDomainPolicy)
    assert all(isinstance(item, OutboundDomainRule) for item in report.outbound_domain_rules)
    assert isinstance(report.network_request_policy, NetworkRequestPolicy)
    assert all(isinstance(item, NetworkRequestCandidate) for item in report.network_request_candidates)
    assert isinstance(report.timeout_retry_policy, NetworkTimeoutRetryPolicy)
    assert isinstance(report.provider_sdk_boundary_policy, ProviderSDKBoundaryPolicy)
    assert all(isinstance(item, ProviderSDKBoundaryReport) for item in report.provider_sdk_boundary_reports)
    assert isinstance(report.data_exfiltration_boundary_policy, DataExfiltrationBoundaryPolicy)
    assert isinstance(report.payload_boundary_policy, PayloadBoundaryPolicy)
    assert isinstance(report.request_response_redaction_boundary, RequestResponseRedactionBoundary)
    assert isinstance(report.network_audit_boundary, NetworkAuditBoundary)
    assert isinstance(report.credential_network_gate, CredentialNetworkBoundaryGate)
    assert isinstance(report.audit_trail, CredentialNetworkBoundaryAuditTrail)


def test_v0294_policy_and_source_view_preserve_no_value_no_network_defaults() -> None:
    report = _report()
    policy = report.policy
    source = report.source_view

    assert report.version == "v0.29.4"
    assert policy.layer == "external_provider_adapter"
    assert policy.boundary_enabled is True
    assert policy.credential_boundary_required is True
    assert policy.secret_reference_required is True
    assert policy.external_secret_store_contract_required is True
    assert policy.credential_redaction_required is True
    assert policy.credential_audit_required is True
    assert policy.network_boundary_required is True
    assert policy.outbound_domain_policy_required is True
    assert policy.timeout_retry_policy_required is True
    assert policy.data_exfiltration_boundary_required is True
    assert policy.provider_sdk_boundary_required is True
    assert policy.credential_storage_enabled_now is False
    assert policy.credential_logging_enabled_now is False
    assert policy.env_file_creation_enabled_now is False
    assert policy.secret_retrieval_enabled_now is False
    assert policy.network_access_enabled_now is False
    assert policy.provider_sdk_invocation_enabled_now is False
    assert policy.provider_invocation_enabled_now is False
    assert policy.command_execution_expansion_enabled_now is False
    assert policy.live_adapter_implementation_enabled_now is False
    assert policy.rpa_adapter_enabled_now is False
    assert policy.external_agent_dominion_enabled_now is False
    assert policy.no_credential_value_default is True
    assert policy.no_network_default is True
    assert policy.no_provider_invocation_default is True
    assert policy.llm_judge_as_sole_boundary_authority_forbidden is True

    assert source.permission_safety_report_ref is not None
    assert source.permission_safety_gate_ref is not None
    assert source.credential_safety_check_refs
    assert source.network_safety_check_refs
    assert source.permission_decision_record_refs
    assert source.safety_classification_refs
    assert source.action_intent_refs
    assert source.action_scope_refs
    assert source.no_network_boundary_refs
    assert source.provider_sdk_isolation_refs
    assert source.mock_credential_boundary_refs
    assert source.credential_need_declaration_refs
    assert source.network_need_declaration_refs
    assert source.adapter_risk_profile_refs
    assert source.credential_requirement_contract_ref is not None
    assert source.network_requirement_contract_ref is not None
    assert source.audit_requirement_contract_ref is not None
    assert source.provider_invocation_prohibition_ref is not None
    assert source.command_execution_prohibition_ref is not None
    assert source.credential_sensitivity_present is True
    assert source.network_sensitivity_present is True
    assert source.credential_value_detected is False
    assert source.credential_storage_detected is False
    assert source.credential_logging_detected is False
    assert source.env_file_detected is False
    assert source.network_call_detected is False
    assert source.provider_sdk_invocation_detected is False
    assert source.provider_invocation_detected is False
    assert source.command_execution_detected is False
    assert source.private_data_detected is False
    assert source.raw_provider_output_detected is False


def test_v0294_credential_secret_boundary_artifacts_are_reference_only() -> None:
    report = _report()

    credential_policy = report.credential_boundary_policy
    assert credential_policy.credential_values_forbidden_now is True
    assert credential_policy.credential_storage_forbidden_now is True
    assert credential_policy.credential_logging_forbidden_now is True
    assert credential_policy.env_file_creation_forbidden_now is True
    assert credential_policy.committed_credentials_forbidden is True
    assert credential_policy.secret_reference_only_required is True
    assert credential_policy.credential_materialization_forbidden_now is True
    assert credential_policy.credential_access_candidate_allowed is True
    assert credential_policy.credential_access_candidate_is_not_access is True

    assert any(item.credential_required_later for item in report.credential_material_classifications)
    assert all(item.credential_value_present_now is False for item in report.credential_material_classifications)
    assert all(item.credential_storage_allowed_now is False for item in report.credential_material_classifications)
    assert all(item.credential_logging_allowed_now is False for item in report.credential_material_classifications)
    assert all(item.secret_reference_required == item.credential_required_later for item in report.credential_material_classifications)

    assert report.secret_reference_policy.secret_reference_is_not_secret_value is True
    assert report.secret_reference_policy.secret_reference_must_be_opaque is True
    assert report.secret_reference_policy.secret_reference_must_not_include_value is True
    assert report.secret_reference_policy.secret_reference_must_not_be_logged_as_value is True
    assert all(item.secret_value_included is False for item in report.secret_reference_descriptors)
    assert report.external_secret_store_contract.secret_store_integration_enabled_now is False
    assert report.external_secret_store_contract.secret_retrieval_enabled_now is False
    assert report.external_secret_store_contract.secret_write_enabled_now is False
    assert report.external_secret_store_contract.secret_rotation_required_later is True
    assert report.external_secret_store_contract.secret_access_audit_required is True
    assert report.external_secret_store_contract.secret_redaction_required is True

    assert report.credential_redaction_policy.redact_secret_like_values is True
    assert report.credential_redaction_policy.redact_tokens is True
    assert report.credential_redaction_policy.redact_api_keys is True
    assert report.credential_redaction_policy.redact_session_cookies is True
    assert report.credential_redaction_policy.raw_credential_output_forbidden is True
    assert report.credential_redaction_policy.redaction_is_not_access_permission is True
    assert report.credential_audit_policy.audit_secret_reference_only is True
    assert report.credential_audit_policy.audit_credential_value_forbidden is True
    assert all(item.credential_access_allowed_now is False for item in report.credential_scope_bindings)
    assert all(item.credential_access_candidate_is_access is False for item in report.credential_access_candidates)
    assert all(item.credential_value_accessed_now is False for item in report.credential_access_candidates)
    assert all(item.credential_value_stored_now is False for item in report.credential_access_candidates)
    assert all(item.credential_value_logged_now is False for item in report.credential_access_candidates)
    assert report.credential_boundary_report.credential_values_present is False
    assert report.credential_boundary_report.credential_stored is False
    assert report.credential_boundary_report.credential_logged is False
    assert report.credential_boundary_report.env_file_created is False


def test_v0294_network_sdk_payload_and_audit_boundaries_do_not_execute() -> None:
    report = _report()

    assert report.network_boundary_policy.no_network_default is True
    assert report.network_boundary_policy.network_access_enabled_now is False
    assert report.network_boundary_policy.outbound_network_forbidden_now is True
    assert report.network_boundary_policy.provider_sdk_network_forbidden_now is True
    assert report.network_boundary_policy.network_request_candidate_allowed is True
    assert report.network_boundary_policy.network_request_candidate_is_not_request is True
    assert report.network_boundary_policy.future_network_reopen_version == "v0.29.8 Limited Provider Invocation Preview Gate"
    assert report.outbound_domain_policy.allowlist_required_later is True
    assert report.outbound_domain_policy.wildcard_domain_forbidden is True
    assert report.outbound_domain_policy.unknown_domain_forbidden is True
    assert report.outbound_domain_policy.private_network_forbidden_now is True
    assert report.outbound_domain_policy.internal_network_forbidden_now is True
    assert report.outbound_domain_policy.domain_policy_is_not_network_access is True
    assert all(item.network_access_allowed_now is False for item in report.outbound_domain_rules)
    assert all(item.wildcard is False for item in report.outbound_domain_rules)
    assert all(item.internal_domain is False for item in report.outbound_domain_rules)
    assert all(item.private_network is False for item in report.outbound_domain_rules)

    assert report.network_request_policy.real_network_request_forbidden_now is True
    assert report.network_request_policy.request_method_declaration_required is True
    assert report.network_request_policy.endpoint_declaration_required is True
    assert report.network_request_policy.payload_boundary_required is True
    assert report.network_request_policy.response_boundary_required is True
    assert all(item.network_request_candidate_is_request is False for item in report.network_request_candidates)
    assert all(item.network_called_now is False for item in report.network_request_candidates)
    assert all(item.provider_invoked_now is False for item in report.network_request_candidates)
    assert report.timeout_retry_policy.bounded_timeout_required is True
    assert report.timeout_retry_policy.bounded_retry_required is True
    assert report.timeout_retry_policy.infinite_retry_forbidden is True
    assert report.timeout_retry_policy.retry_on_auth_failure_forbidden is True
    assert report.timeout_retry_policy.timeout_retry_policy_is_not_network_execution is True

    assert report.provider_sdk_boundary_policy.provider_sdk_runtime_dependency_forbidden_now is True
    assert report.provider_sdk_boundary_policy.provider_sdk_import_forbidden_now is True
    assert report.provider_sdk_boundary_policy.provider_sdk_invocation_forbidden_now is True
    assert all(item.provider_sdk_runtime_dependency_added is False for item in report.provider_sdk_boundary_reports)
    assert all(item.provider_sdk_imported is False for item in report.provider_sdk_boundary_reports)
    assert all(item.provider_sdk_invoked is False for item in report.provider_sdk_boundary_reports)
    assert all(item.provider_sdk_network_called is False for item in report.provider_sdk_boundary_reports)

    assert report.data_exfiltration_boundary_policy.private_data_exfiltration_forbidden is True
    assert report.data_exfiltration_boundary_policy.credential_exfiltration_forbidden is True
    assert report.data_exfiltration_boundary_policy.raw_provider_output_exfiltration_forbidden is True
    assert report.payload_boundary_policy.outbound_payload_must_exclude_credentials is True
    assert report.payload_boundary_policy.outbound_payload_must_exclude_private_data_by_default is True
    assert report.payload_boundary_policy.outbound_payload_must_exclude_raw_traces is True
    assert report.payload_boundary_policy.outbound_payload_must_exclude_raw_transcripts is True
    assert report.payload_boundary_policy.outbound_payload_must_exclude_raw_provider_outputs is True
    assert report.payload_boundary_policy.payload_preview_is_not_payload_send is True
    assert report.request_response_redaction_boundary.raw_request_logging_forbidden is True
    assert report.request_response_redaction_boundary.raw_response_logging_forbidden is True
    assert report.network_audit_boundary.audit_must_not_include_credentials is True
    assert report.network_audit_boundary.audit_must_not_include_raw_payloads is True


def test_v0294_gate_report_pig_ocpx_and_cli() -> None:
    service = CredentialNetworkBoundaryReportService()
    report = service.build_report()
    gate = report.credential_network_gate
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert gate.credential_boundary_passed is True
    assert gate.secret_reference_boundary_passed is True
    assert gate.no_credential_value_present is True
    assert gate.no_credential_storage is True
    assert gate.no_credential_logging is True
    assert gate.no_env_file_created is True
    assert gate.network_boundary_passed is True
    assert gate.no_network_call is True
    assert gate.provider_sdk_boundary_passed is True
    assert gate.no_provider_sdk_invocation is True
    assert gate.outbound_domain_policy_complete is True
    assert gate.payload_boundary_complete is True
    assert gate.data_exfiltration_boundary_complete is True
    assert gate.audit_boundary_complete is True
    assert gate.ready_for_v0_29_5 is True
    assert gate.ready_for_invocation_candidate is True
    assert gate.ready_for_dry_run_plan is True
    assert gate.ready_for_provider_invocation is False
    assert gate.ready_for_network_access is False
    assert gate.ready_for_credential_access is False
    assert gate.ready_for_command_execution is False
    assert report.audit_trail.raw_content_included is False
    assert report.audit_trail.credential_value_included is False
    assert report.audit_trail.raw_payload_included is False

    forbidden_flags = [
        "ready_for_provider_invocation",
        "ready_for_network_access",
        "ready_for_credential_access",
        "ready_for_command_execution",
        "credential_value_present",
        "credential_stored",
        "credential_logged",
        "env_file_created",
        "secret_retrieved",
        "secret_materialized",
        "provider_sdk_invoked",
        "provider_invoked",
        "network_called",
        "outbound_request_sent",
        "command_executed",
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
    assert all(getattr(report, flag) is False for flag in forbidden_flags)

    assert "credential_secret_network_boundary_policy" in V0294_OBJECT_TYPES
    assert "credential_boundary_policy_created" in V0294_EFFECT_TYPES
    assert "network_called" in V0294_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.29.4"
    assert pig["subject"] == "credential_secret_network_boundary"
    assert pig["safety_boundary"]["credential_stored"] is False
    assert pig["safety_boundary"]["network_called"] is False
    assert ocpx["state"] == "credential_secret_network_boundary_created"
    assert "CredentialBoundaryState" in ocpx["target_read_models"]
    assert "NetworkRequestCandidateState" in ocpx["target_read_models"]

    for command in [
        "policy",
        "source-view",
        "credentials",
        "credential-classification",
        "secret-policy",
        "secret-refs",
        "secret-store-contract",
        "credential-redaction",
        "credential-audit",
        "credential-scope",
        "credential-candidates",
        "network",
        "outbound-domains",
        "network-requests",
        "timeout-retry",
        "provider-sdk",
        "exfiltration",
        "payload",
        "redaction",
        "network-audit",
        "gate",
        "audit",
        "report",
    ]:
        assert main(["adapter", "boundary", command]) == 0
