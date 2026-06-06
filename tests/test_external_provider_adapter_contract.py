from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.external_provider_adapter_contract import (
    AdapterAuditRequirementContract,
    AdapterCapabilityContract,
    AdapterCertificationRequirementContract,
    AdapterCredentialRequirementContract,
    AdapterEffectBoundaryContract,
    AdapterInputSchemaContract,
    AdapterLifecycleContract,
    AdapterMockNoNetworkRequirementContract,
    AdapterNetworkRequirementContract,
    AdapterOCELVisibilityContract,
    AdapterOutputSchemaContract,
    AdapterPermissionRequirementContract,
    AdapterRollbackNoOpRequirementContract,
    AdapterSafetyRequirementContract,
    CommandExecutionProhibitionContract,
    ExternalAdapterContractReport,
    ExternalAdapterContractReportService,
    ExternalAdapterContractRequest,
    ExternalAdapterContractSourceView,
    ExternalProviderAdapterContract,
    ExternalProviderAdapterTrackPolicy,
    ExternalSkillAdapterContract,
    ProviderInvocationProhibitionContract,
    V0290_EFFECT_TYPES,
    V0290_FORBIDDEN_EFFECT_TYPES,
)


def _report() -> ExternalAdapterContractReport:
    return ExternalAdapterContractReportService().build_report()


def test_v0290_contract_models_build() -> None:
    report = _report()

    assert isinstance(report.track_policy, ExternalProviderAdapterTrackPolicy)
    assert isinstance(report.request, ExternalAdapterContractRequest)
    assert isinstance(report.source_view, ExternalAdapterContractSourceView)
    assert isinstance(report.provider_adapter_contract, ExternalProviderAdapterContract)
    assert isinstance(report.external_skill_adapter_contract, ExternalSkillAdapterContract)
    assert isinstance(report.lifecycle_contract, AdapterLifecycleContract)
    assert isinstance(report.capability_contract, AdapterCapabilityContract)
    assert isinstance(report.input_schema_contract, AdapterInputSchemaContract)
    assert isinstance(report.output_schema_contract, AdapterOutputSchemaContract)
    assert isinstance(report.effect_boundary_contract, AdapterEffectBoundaryContract)
    assert isinstance(report.permission_requirement_contract, AdapterPermissionRequirementContract)
    assert isinstance(report.safety_requirement_contract, AdapterSafetyRequirementContract)
    assert isinstance(report.credential_requirement_contract, AdapterCredentialRequirementContract)
    assert isinstance(report.network_requirement_contract, AdapterNetworkRequirementContract)
    assert isinstance(report.audit_requirement_contract, AdapterAuditRequirementContract)
    assert isinstance(report.rollback_noop_requirement_contract, AdapterRollbackNoOpRequirementContract)
    assert isinstance(report.ocel_visibility_contract, AdapterOCELVisibilityContract)
    assert isinstance(report.mock_no_network_requirement_contract, AdapterMockNoNetworkRequirementContract)
    assert isinstance(report.certification_requirement_contract, AdapterCertificationRequirementContract)
    assert isinstance(report.provider_invocation_prohibition_contract, ProviderInvocationProhibitionContract)
    assert isinstance(report.command_execution_prohibition_contract, CommandExecutionProhibitionContract)


def test_v0290_policy_source_view_and_report_readiness() -> None:
    report = _report()
    policy = report.track_policy
    source = report.source_view

    assert report.version == "v0.29.0"
    assert policy.layer == "external_provider_adapter"
    assert policy.track_name == "External Skill / External Provider Adapter Development"
    assert policy.contract_only is True
    assert policy.adapter_implementation_enabled_now is False
    assert policy.provider_registration_enabled_now is False
    assert policy.provider_invocation_enabled_now is False
    assert policy.network_access_enabled_now is False
    assert policy.credential_storage_enabled_now is False
    assert policy.command_execution_expansion_enabled_now is False
    assert policy.rpa_adapter_enabled_now is False
    assert policy.external_agent_dominion_enabled_now is False
    assert policy.schumpeter_private_runtime_enabled_now is False
    assert policy.mock_no_network_required_before_live is True
    assert policy.permission_gate_required_before_invocation is True
    assert policy.safety_gate_required_before_invocation is True
    assert policy.credential_boundary_required_before_invocation is True
    assert policy.network_boundary_required_before_invocation is True
    assert policy.audit_required_before_invocation is True
    assert policy.rollback_or_noop_required_before_invocation is True
    assert policy.ocel_visibility_required_before_invocation is True
    assert policy.llm_judge_as_sole_contract_authority_forbidden is True

    assert source.v0289_consolidation_report_ref is not None
    assert source.v029_readiness_report_ref is not None
    assert source.v029_handoff_packet_ref is not None
    assert source.external_adapter_preflight_report_ref is not None
    assert source.provider_invocation_reopen_criteria_ref is not None
    assert source.command_execution_reopen_criteria_ref is not None
    assert source.credential_boundary_preflight_ref is not None
    assert source.network_boundary_preflight_ref is not None
    assert source.permission_boundary_preflight_ref is not None
    assert source.safety_gate_preflight_ref is not None
    assert source.audit_rollback_ocel_preflight_ref is not None
    assert source.adapter_certification_preflight_ref is not None
    assert source.ready_for_v0_29_contract is True
    assert source.ready_for_provider_invocation is False
    assert source.ready_for_command_execution is False
    assert source.provider_invocation_detected is False
    assert source.network_call_detected is False
    assert source.command_execution_detected is False
    assert source.credential_value_detected is False
    assert source.private_material_detected is False
    assert source.raw_provider_output_detected is False

    assert report.report_status == "passed"
    assert report.ready_for_v0_29_1 is True
    assert report.ready_for_adapter_registry is True
    assert report.ready_for_adapter_implementation is False
    assert report.ready_for_provider_registration is False
    assert report.ready_for_provider_invocation is False
    assert report.ready_for_network_access is False
    assert report.ready_for_command_execution is False
    assert report.next_required_step == "v0.29.1 Provider Capability Inventory / Adapter Registry"


def test_v0290_provider_skill_lifecycle_capability_schema_and_effect_contracts() -> None:
    report = _report()
    provider = report.provider_adapter_contract
    skill = report.external_skill_adapter_contract
    lifecycle = report.lifecycle_contract
    capability = report.capability_contract
    input_schema = report.input_schema_contract
    output_schema = report.output_schema_contract
    effects = report.effect_boundary_contract

    assert provider.adapter_interface_required is True
    assert provider.capability_declaration_required is True
    assert provider.input_schema_required is True
    assert provider.output_schema_required is True
    assert provider.effect_boundary_required is True
    assert provider.permission_requirement_required is True
    assert provider.safety_requirement_required is True
    assert provider.credential_requirement_required is True
    assert provider.network_requirement_required is True
    assert provider.audit_requirement_required is True
    assert provider.rollback_noop_requirement_required is True
    assert provider.ocel_visibility_required is True
    assert provider.mock_no_network_mode_required is True
    assert provider.certification_required is True
    assert provider.adapter_implemented_now is False
    assert provider.provider_registered_now is False
    assert provider.provider_invoked_now is False

    assert skill.skill_manifest_required is True
    assert skill.skill_capability_declaration_required is True
    assert skill.skill_effect_boundary_required is True
    assert skill.skill_permission_scope_required is True
    assert skill.skill_safety_gate_required is True
    assert skill.skill_ocel_visibility_required is True
    assert skill.skill_mock_mode_required is True
    assert skill.skill_certification_required is True
    assert skill.external_skill_implemented_now is False
    assert skill.external_skill_executed_now is False

    assert {"declared", "inventoried", "registered", "mocked", "certified_mock", "gated", "dry_run_candidate", "approval_required", "preview_allowed", "disabled", "blocked", "deprecated"} <= set(lifecycle.allowed_lifecycle_states)
    assert lifecycle.registration_is_not_execution is True
    assert lifecycle.certification_is_not_live_invocation is True
    assert lifecycle.preview_is_not_unbounded_runtime is True

    assert capability.capability_declaration_required is True
    assert capability.capability_id_required is True
    assert capability.capability_name_required is True
    assert capability.input_capability_schema_required is True
    assert capability.output_capability_schema_required is True
    assert capability.effect_type_declaration_required is True
    assert capability.risk_level_required is True
    assert capability.permission_scope_required is True
    assert capability.capability_declaration_is_not_permission is True
    assert capability.capability_declaration_is_not_invocation is True

    assert input_schema.raw_secret_input_forbidden is True
    assert input_schema.raw_private_payload_forbidden_by_default is True
    assert output_schema.raw_provider_output_persistence_forbidden_by_default is True
    assert output_schema.output_redaction_policy_required is True
    assert output_schema.output_summary_boundary_required is True
    assert output_schema.output_error_schema_required is True
    assert {"read_only_observation", "mock_provider_response", "dry_run_plan_created", "invocation_candidate_created", "approval_record_created", "audit_record_created", "ocel_trace_created"} <= set(effects.allowed_effect_types)
    assert {"provider_invoked", "network_called", "command_executed", "credential_stored", "external_side_effect_performed", "file_mutated_by_adapter", "private_data_exfiltrated"} <= set(effects.forbidden_effect_types)
    assert effects.external_side_effect_requires_future_gate is True


def test_v0290_requirement_and_prohibition_contracts() -> None:
    report = _report()

    assert report.permission_requirement_contract.permission_gate_required is True
    assert report.permission_requirement_contract.scoped_permission_required is True
    assert report.permission_requirement_contract.permission_expiry_required is True
    assert report.permission_requirement_contract.user_approval_surface_required is True
    assert report.permission_requirement_contract.approval_record_required is True
    assert report.permission_requirement_contract.permission_restoration_without_approval_forbidden is True
    assert report.permission_requirement_contract.deny_first_default_required is True

    assert report.safety_requirement_contract.risk_classification_required is True
    assert report.safety_requirement_contract.private_data_check_required is True
    assert report.safety_requirement_contract.credential_check_required is True
    assert report.safety_requirement_contract.external_side_effect_check_required is True
    assert report.safety_requirement_contract.data_exfiltration_check_required is True
    assert report.safety_requirement_contract.unsafe_adapter_blocks_invocation is True

    assert report.credential_requirement_contract.credential_value_storage_enabled_now is False
    assert report.credential_requirement_contract.credential_value_logging_forbidden is True
    assert report.credential_requirement_contract.committed_credentials_forbidden is True
    assert report.credential_requirement_contract.secret_reference_only_required is True
    assert report.network_requirement_contract.network_access_enabled_now is False
    assert report.network_requirement_contract.no_network_default_required is True
    assert report.network_requirement_contract.outbound_domain_policy_required is True
    assert report.network_requirement_contract.request_audit_required is True

    assert report.audit_requirement_contract.audit_required is True
    assert report.audit_requirement_contract.raw_secret_audit_output_forbidden is True
    assert report.rollback_noop_requirement_contract.no_op_fallback_required is True
    assert report.rollback_noop_requirement_contract.rollback_plan_required_before_side_effect is True
    assert report.rollback_noop_requirement_contract.external_side_effect_without_rollback_forbidden is True
    assert report.ocel_visibility_contract.adapter_declared_event_required is True
    assert report.ocel_visibility_contract.future_provider_invocation_event_required is True
    assert report.mock_no_network_requirement_contract.mock_mode_required_before_live is True
    assert report.mock_no_network_requirement_contract.live_provider_disabled_by_default is True
    assert report.mock_no_network_requirement_contract.credential_not_required_for_mock is True
    assert report.mock_no_network_requirement_contract.provider_sdk_not_required_for_mock is True
    assert report.certification_requirement_contract.certification_required_before_preview is True
    assert report.certification_requirement_contract.certification_is_not_live_invocation is True

    assert report.provider_invocation_prohibition_contract.provider_invocation_forbidden_now is True
    assert report.provider_invocation_prohibition_contract.provider_registration_forbidden_now is True
    assert report.provider_invocation_prohibition_contract.provider_sdk_invocation_forbidden_now is True
    assert report.provider_invocation_prohibition_contract.external_api_call_forbidden_now is True
    assert report.provider_invocation_prohibition_contract.network_call_forbidden_now is True
    assert report.provider_invocation_prohibition_contract.ready_for_provider_invocation is False
    assert report.provider_invocation_prohibition_contract.future_reopen_version == "v0.29.8 Limited Provider Invocation Preview Gate"

    assert report.command_execution_prohibition_contract.command_execution_expansion_forbidden_now is True
    assert report.command_execution_prohibition_contract.shell_execution_forbidden_now is True
    assert report.command_execution_prohibition_contract.shell_true_forbidden is True
    assert report.command_execution_prohibition_contract.unbounded_subprocess_forbidden is True
    assert report.command_execution_prohibition_contract.ready_for_command_execution is False


def test_v0290_pig_ocpx_mappings_and_cli_commands() -> None:
    service = ExternalAdapterContractReportService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert pig["version"] == "v0.29.0"
    assert pig["layer"] == "external_provider_adapter"
    assert pig["subject"] == "external_provider_adapter_contract"
    assert ocpx["state"] == "external_provider_adapter_contract_created"
    assert "external_adapter_contract_created" in V0290_EFFECT_TYPES
    assert "adapter_requirement_contract_created" in V0290_EFFECT_TYPES
    assert "provider_invocation_prohibition_declared" in V0290_EFFECT_TYPES
    assert "command_execution_prohibition_declared" in V0290_EFFECT_TYPES
    assert "state_candidate_created" in V0290_EFFECT_TYPES
    assert "provider_invoked" in V0290_FORBIDDEN_EFFECT_TYPES
    assert "network_called" in V0290_FORBIDDEN_EFFECT_TYPES
    assert "ExternalProviderAdapterContractState" in ocpx["target_read_models"]
    assert "ProviderInvocationProhibitionState" in ocpx["target_read_models"]
    assert "V029ReadinessState" in ocpx["target_read_models"]

    commands = ["policy", "source-view", "provider", "external-skill", "lifecycle", "capability", "input-schema", "output-schema", "effects", "permission", "safety", "credentials", "network", "audit", "rollback", "ocel", "mock", "certification", "prohibit-provider-invocation", "prohibit-command-execution", "report"]
    for command in commands:
        assert main(["adapter", "contract", command]) == 0
