from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.public_alpha_schumpeter_preparation import (
    V0285_EFFECT_TYPES,
    V0285_FORBIDDEN_EFFECT_TYPES,
    SchumpeterConfigOverlayContract,
    SchumpeterDataBoundaryPolicy,
    SchumpeterDeploymentBoundaryPolicy,
    SchumpeterMemoryWorkbenchBoundaryPolicy,
    SchumpeterNamingPolicy,
    SchumpeterPreparationAuditTrail,
    SchumpeterPreparationHandoffPacket,
    SchumpeterPreparationReport,
    SchumpeterPreparationReportService,
    SchumpeterPreparationSourceView,
    SchumpeterPrivateOverlayContract,
    SchumpeterPrivateOverlayManifestPreview,
    SchumpeterProfileBoundary,
    SchumpeterProfileCapabilityEntry,
    SchumpeterProfileCapabilityMap,
    SchumpeterProfilePreparationRequest,
    SchumpeterProfileRiskItem,
    SchumpeterProfileRiskRegister,
    SchumpeterProviderBoundaryPolicy,
    SchumpeterRPAAdapterDeferralPolicy,
    SchumpeterRuntimeBoundaryPolicy,
    SchumpeterSkillBoundaryPolicy,
    SchumpeterSplitPreparationProfilePolicy,
    PublicCorePrivateOverlayPolicy,
)


def _parts():
    return SchumpeterPreparationReportService().build_all_parts()


def test_v0285_preparation_profile_models_build() -> None:
    parts = _parts()

    assert isinstance(parts["policy"], SchumpeterSplitPreparationProfilePolicy)
    assert isinstance(parts["source-view"], SchumpeterPreparationSourceView)
    assert isinstance(parts["profile-boundary"], SchumpeterProfileBoundary)
    assert isinstance(parts["naming"], SchumpeterNamingPolicy)
    assert isinstance(parts["overlay-policy"], PublicCorePrivateOverlayPolicy)
    assert isinstance(parts["overlay-contract"], SchumpeterPrivateOverlayContract)
    assert isinstance(parts["config-contract"], SchumpeterConfigOverlayContract)
    assert isinstance(parts["data-boundary"], SchumpeterDataBoundaryPolicy)
    assert isinstance(parts["skill-boundary"], SchumpeterSkillBoundaryPolicy)
    assert isinstance(parts["provider-boundary"], SchumpeterProviderBoundaryPolicy)
    assert isinstance(parts["rpa-deferral"], SchumpeterRPAAdapterDeferralPolicy)
    assert isinstance(parts["runtime-boundary"], SchumpeterRuntimeBoundaryPolicy)
    assert isinstance(parts["memory-workbench"], SchumpeterMemoryWorkbenchBoundaryPolicy)
    assert isinstance(parts["deployment-boundary"], SchumpeterDeploymentBoundaryPolicy)
    assert isinstance(parts["manifest-preview"], SchumpeterPrivateOverlayManifestPreview)
    assert isinstance(parts["capability-map"], SchumpeterProfileCapabilityMap)
    assert isinstance(parts["risk-register"], SchumpeterProfileRiskRegister)
    assert isinstance(parts["handoff"], SchumpeterPreparationHandoffPacket)
    assert isinstance(parts["audit"], SchumpeterPreparationAuditTrail)
    assert isinstance(parts["request"], SchumpeterProfilePreparationRequest) if "request" in parts else True
    assert isinstance(parts["report"], SchumpeterPreparationReport)


def test_v0285_policy_and_boundaries_are_preparation_only() -> None:
    report = _parts()["report"]
    policy = report.preparation_policy

    assert policy.version == "v0.28.5"
    assert policy.preparation_profile_enabled is True
    assert policy.private_overlay_contract_enabled is True
    assert policy.actual_split_enabled_now is False
    assert policy.company_wrapper_runtime_enabled_now is False
    assert policy.private_repo_creation_enabled_now is False
    assert policy.config_file_creation_enabled_now is False
    assert policy.credential_creation_enabled_now is False
    assert policy.endpoint_creation_enabled_now is False
    assert policy.provider_adapter_enabled_now is False
    assert policy.rpa_adapter_enabled_now is False
    assert policy.command_execution_enabled_now is False
    assert policy.provider_invocation_enabled_now is False
    assert policy.references_runtime_dependency_enabled_now is False
    assert policy.references_code_copy_enabled_now is False
    assert policy.public_core_must_not_depend_on_private_overlay is True
    assert policy.llm_judge_as_sole_preparation_authority_forbidden is True

    assert report.profile_boundary.profile_name == "Schumpeter"
    assert report.profile_boundary.public_core_depends_on_private_overlay is False
    assert report.profile_boundary.private_overlay_implemented_now is False
    assert report.naming_policy.public_name == "ChantaCore"
    assert report.naming_policy.schumpeter_name_is_not_runtime_implementation is True
    assert report.public_core_private_overlay_policy.private_overlay_contract_is_not_runtime is True
    assert report.private_overlay_contract.overlay_implemented_now is False


def test_v0285_contracts_manifest_capability_and_risk_register() -> None:
    report = _parts()["report"]

    assert report.config_overlay_contract.config_file_created_now is False
    assert report.config_overlay_contract.company_endpoint_forbidden_now is True
    assert report.config_overlay_contract.committed_secret_forbidden is True
    assert report.data_boundary_policy.company_data_private_only is True
    assert report.data_boundary_policy.public_core_must_not_store_company_data is True
    assert report.skill_boundary_policy.A360_skill_forbidden_now is True
    assert report.skill_boundary_policy.Brity_skill_forbidden_now is True
    assert report.skill_boundary_policy.UiPath_skill_forbidden_now is True
    assert report.provider_boundary_policy.provider_adapter_implementation_forbidden_now is True
    assert report.provider_boundary_policy.provider_invocation_forbidden_now is True
    assert report.RPA_adapter_deferral_policy.RPA_adapter_deferred_to_v029_or_later is True
    assert report.runtime_boundary_policy.runtime_wrapper_implementation_forbidden_now is True
    assert report.memory_workbench_boundary_policy.private_memory_records_for_company_forbidden_now is True
    assert report.deployment_boundary_policy.company_deployment_forbidden_now is True

    manifest = report.overlay_manifest_preview
    assert manifest.preview_is_not_file_creation is True
    assert manifest.manifest_file_created_now is False
    assert manifest.private_config_created_now is False

    capability_map = report.capability_map
    assert capability_map.public_core_capability_count >= 1
    assert capability_map.private_overlay_candidate_count >= 1
    assert capability_map.future_adapter_candidate_count >= 1
    assert capability_map.forbidden_now_count >= 1
    assert all(isinstance(item, SchumpeterProfileCapabilityEntry) for item in capability_map.entries)
    assert all(item.implementation_allowed_now is False for item in capability_map.entries if item.capability_category != "public_core")

    risk_register = report.risk_register
    risk_types = {item.risk_type for item in risk_register.risk_items}
    assert "public_private_contamination" in risk_types
    assert "credential_exposure" in risk_types
    assert "provider_invocation_without_gate" in risk_types
    assert "RPA_adapter_scope_creep" in risk_types
    assert "reference_code_copy" in risk_types
    assert all(isinstance(item, SchumpeterProfileRiskItem) for item in risk_register.risk_items)


def test_v0285_decision_handoff_report_pig_ocpx_and_cli() -> None:
    service = SchumpeterPreparationReportService()
    parts = service.build_all_parts()
    report = parts["report"]

    assert report.preparation_decisions
    assert report.preparation_decisions[0].implementation_performed_now is False
    assert report.preparation_decisions[0].config_created_now is False
    assert report.preparation_decisions[0].provider_adapter_created_now is False
    assert report.preparation_decisions[0].RPA_adapter_created_now is False
    assert report.handoff_packet.target_version == "v0.28.6"
    assert report.handoff_packet.refs_only is True
    assert report.handoff_packet.implementation_performed_now is False
    assert "actual_schumpeter_split" in report.handoff_packet.not_implemented_now
    assert "private_config_generation" in report.handoff_packet.not_implemented_now
    assert report.audit_trail.raw_content_included is False
    assert report.ready_for_v0_28_6 is True
    assert report.ready_for_public_alpha_release_claim is False
    assert report.schumpeter_preparation_profile_ready is True
    assert report.private_overlay_boundary_ready is True
    assert report.next_required_step == "v0.28.6 Public Alpha Runtime Profile / Smoke Demo Flow"

    false_flags = [
        "actual_split_implemented",
        "company_wrapper_implemented",
        "private_repo_created",
        "private_config_created",
        "credential_created",
        "endpoint_created",
        "provider_adapter_created",
        "RPA_adapter_created",
        "A360_adapter_created",
        "Brity_adapter_created",
        "UiPath_adapter_created",
        "references_runtime_dependency_added",
        "references_code_copied",
        "file_moved",
        "package_published",
        "release_tag_created",
        "provider_invoked",
        "command_executed",
        "runtime_continuity_injected",
        "company_private_material_exposed",
        "credential_exposed",
        "secret_exposed",
        "raw_trace_exposed",
        "raw_transcript_exposed",
        "raw_provider_output_exposed",
        "PIG_execution_authority_enabled",
        "llm_judge_used",
    ]
    assert all(getattr(report, flag) is False for flag in false_flags)

    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()
    assert pig["version"] == "v0.28.5"
    assert pig["subject"] == "schumpeter_split_preparation_profile"
    assert ocpx["state"] == "schumpeter_split_preparation_profile_created"
    assert "schumpeter_preparation_profile_created" in V0285_EFFECT_TYPES
    assert "actual_split_implemented" in V0285_FORBIDDEN_EFFECT_TYPES
    assert "SchumpeterPreparationProfileState" in ocpx["target_read_models"]

    for command_name in [
        "policy",
        "source-view",
        "profile-boundary",
        "naming",
        "overlay-policy",
        "overlay-contract",
        "config-contract",
        "data-boundary",
        "skill-boundary",
        "provider-boundary",
        "rpa-deferral",
        "runtime-boundary",
        "memory-workbench",
        "deployment-boundary",
        "manifest-preview",
        "capability-map",
        "risk-register",
        "decision",
        "handoff",
        "audit",
        "report",
    ]:
        assert main(["alpha", "schumpeter-prep", command_name]) == 0
