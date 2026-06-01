from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.public_alpha_schumpeter_preparation import (
    V028_EFFECT_TYPES,
    V028_EVENT_TYPES,
    V028_FORBIDDEN_EFFECT_TYPES,
    V028_OBJECT_TYPES,
    ExternalAdapterPreflightBoundary,
    HygieneDebtDisposition,
    PackagingReadinessPolicy,
    PublicAlphaSafetyBoundaryPolicy,
    PublicAlphaSchumpeterPreparationContract,
    PublicAlphaScopePolicy,
    PublicAlphaStagePolicy,
    PublicPrivateBoundaryPolicy,
    ReleaseHygieneBlockingPolicy,
    ReleaseHygieneDebtPolicy,
    SchumpeterReferenceInventoryPolicy,
    SchumpeterReuseDispositionPolicy,
    SchumpeterSplitDecisionFramework,
    SchumpeterSplitDecisionOption,
    SchumpeterSplitEvaluationCriterion,
    SchumpeterSplitPreparationPolicy,
    V028ContractFinding,
    V028ContractPrerequisiteSourceService,
    V028ContractReport,
    V028ContractReportService,
    V028Roadmap,
    V028VersionPlan,
    V029RiskReopenCriteria,
)


def _parts() -> dict:
    return V028ContractReportService().build_all_parts()


def test_v028_contract_models_build() -> None:
    parts = _parts()

    assert isinstance(parts["contract"], PublicAlphaSchumpeterPreparationContract)
    assert isinstance(parts["roadmap"], V028Roadmap)
    assert isinstance(parts["version_plans"][0], V028VersionPlan)
    assert isinstance(parts["scope_policy"], PublicAlphaScopePolicy)
    assert isinstance(parts["stage_policy"], PublicAlphaStagePolicy)
    assert isinstance(parts["hygiene_debt_policy"], ReleaseHygieneDebtPolicy)
    assert isinstance(parts["hygiene_debt_dispositions"][0], HygieneDebtDisposition)
    assert isinstance(parts["hygiene_blocking_policy"], ReleaseHygieneBlockingPolicy)
    assert isinstance(parts["packaging_policy"], PackagingReadinessPolicy)
    assert isinstance(parts["public_private_policy"], PublicPrivateBoundaryPolicy)
    assert isinstance(parts["schumpeter_preparation_policy"], SchumpeterSplitPreparationPolicy)
    assert isinstance(parts["schumpeter_decision_framework"], SchumpeterSplitDecisionFramework)
    assert isinstance(parts["schumpeter_options"][0], SchumpeterSplitDecisionOption)
    assert isinstance(parts["schumpeter_criteria"][0], SchumpeterSplitEvaluationCriterion)
    assert isinstance(parts["schumpeter_reference_policy"], SchumpeterReferenceInventoryPolicy)
    assert isinstance(parts["schumpeter_reuse_policy"], SchumpeterReuseDispositionPolicy)
    assert isinstance(parts["external_adapter_preflight"], ExternalAdapterPreflightBoundary)
    assert isinstance(parts["v029_risk_reopen"], V029RiskReopenCriteria)
    assert isinstance(parts["safety_boundary"], PublicAlphaSafetyBoundaryPolicy)
    assert isinstance(parts["findings"][0], V028ContractFinding)
    assert isinstance(parts["report"], V028ContractReport)


def test_contract_identity_and_roadmap() -> None:
    parts = _parts()
    contract = parts["contract"]
    roadmap = parts["roadmap"]
    version_names = {plan.version_number: plan.version_name for plan in roadmap.versions}

    assert contract.version == "v0.28.0"
    assert contract.layer == "public_alpha_schumpeter_preparation"
    assert contract.track == "Public Alpha / Schumpeter Split Preparation"
    assert contract.status == "contract_only"
    assert contract.previous_foundation_ref and contract.previous_foundation_ref["version"] == "v0.27.9"
    assert contract.workbench_foundation_ref and contract.workbench_foundation_ref["version"] == "v0.26.9"
    assert contract.release_hygiene_ref and contract.release_hygiene_ref["version"] == "v0.26.10"
    assert contract.public_alpha_implemented is False
    assert contract.schumpeter_split_implemented is False
    assert contract.external_adapter_implemented is False
    assert contract.provider_invoked is False
    assert contract.command_executed is False
    assert contract.package_published is False
    assert contract.release_tag_created is False
    assert set(version_names) == {f"v0.28.{index}" for index in range(10)}
    assert version_names["v0.28.1"] == "Release Hygiene / Repository Governance Blocking Gate"
    assert version_names["v0.28.4"] == "Schumpeter Split Decision Framework"
    assert version_names["v0.28.8"] == "Alpha Readiness Validation / External Adapter Preflight Gate"
    assert roadmap.next_version == "v0.28.1 Release Hygiene / Repository Governance Blocking Gate"
    assert roadmap.next_track == "v0.29.x External Skill / External Provider Adapter Development"
    assert all(plan.public_alpha_release_allowed is False for plan in roadmap.versions)
    assert all(plan.provider_invocation_allowed is False for plan in roadmap.versions)
    assert all(plan.command_execution_allowed is False for plan in roadmap.versions)


def test_public_alpha_scope_stage_and_hygiene_policies() -> None:
    parts = _parts()
    scope = parts["scope_policy"]
    stage = parts["stage_policy"]
    hygiene = parts["hygiene_debt_policy"]
    dispositions = parts["hygiene_debt_dispositions"]
    blocking = parts["hygiene_blocking_policy"]

    assert scope.public_alpha_scope_defined is True
    assert scope.public_alpha_is_not_production_ready is True
    assert scope.public_alpha_is_not_company_deployment is True
    assert scope.public_alpha_is_not_external_adapter_runtime is True
    assert scope.public_alpha_is_not_schumpeter_split is True
    assert "public_docs" in scope.public_alpha_allowed_surfaces
    assert "sanitized_examples" in scope.public_alpha_allowed_surfaces
    assert "synthetic_demo_data" in scope.public_alpha_allowed_surfaces
    assert "OCEL_store_validation" in scope.public_alpha_allowed_surfaces
    assert "Workbench_report_surfaces" in scope.public_alpha_allowed_surfaces
    assert "Memory_foundation_report_surfaces" in scope.public_alpha_allowed_surfaces
    assert "CLI_smoke_surfaces" in scope.public_alpha_allowed_surfaces
    assert "company_private_material" in scope.public_alpha_forbidden_surfaces
    assert "credentials" in scope.public_alpha_forbidden_surfaces
    assert "raw_runtime_trace" in scope.public_alpha_forbidden_surfaces
    assert "raw_transcript" in scope.public_alpha_forbidden_surfaces
    assert "raw_provider_output" in scope.public_alpha_forbidden_surfaces
    assert "external_provider_invocation" in scope.public_alpha_forbidden_surfaces
    assert "runtime_continuity_injection" in scope.public_alpha_forbidden_surfaces
    assert "Schumpeter_company_wrapper" in scope.public_alpha_forbidden_surfaces
    assert "RPA_adapter" in scope.public_alpha_forbidden_surfaces
    assert stage.stages == [
        "alpha_architecture_candidate",
        "alpha_repository_candidate",
        "alpha_package_candidate",
        "alpha_release_candidate",
    ]
    assert stage.stage_order_required is True
    assert stage.architecture_ready_is_not_release_ready is True
    assert stage.repository_ready_is_not_package_ready is True
    assert stage.package_ready_is_not_production_ready is True
    assert stage.public_alpha_ready_requires_all_gates is True
    assert stage.no_release_is_valid_outcome is True
    assert hygiene.v02610_hygiene_debt_must_be_resolved_or_explicitly_dispositioned is True
    assert hygiene.hygiene_unknown_is_not_passed is True
    assert hygiene.hygiene_failed_blocks_public_alpha_release_claim is True
    assert hygiene.clean_worktree_required_for_release_claim is True
    assert hygiene.release_tag_required_for_release_claim is True
    assert hygiene.license_required_for_release_claim is True
    assert hygiene.changelog_required_for_release_claim is True
    assert hygiene.third_party_notice_required_when_references_exist is True
    assert hygiene.runtime_data_hygiene_required is True
    assert hygiene.reference_license_policy_required is True
    assert hygiene.no_release_allowed is True
    assert {"resolve_in_v0281", "defer_with_blocker", "accept_warning", "block_public_alpha", "no_release"} <= {
        item.disposition_type for item in dispositions
    }
    assert blocking.v0281_is_blocking_gate is True
    assert blocking.public_alpha_release_claim_requires_v0281_pass is True
    assert blocking.repository_release_ready_requires_hygiene_pass is True
    assert blocking.repository_release_ready_must_be_false_when_hygiene_unknown is True
    assert blocking.public_alpha_ready_must_be_false_when_hygiene_failed is True


def test_packaging_public_private_schumpeter_and_adapter_policies() -> None:
    parts = _parts()
    packaging = parts["packaging_policy"]
    public_private = parts["public_private_policy"]
    preparation = parts["schumpeter_preparation_policy"]
    inventory = parts["schumpeter_reference_policy"]
    reuse = parts["schumpeter_reuse_policy"]
    preflight = parts["external_adapter_preflight"]
    v029 = parts["v029_risk_reopen"]

    assert packaging.packaging_boundary_deferred_to == "v0.28.2"
    assert packaging.pyproject_validation_required is True
    assert packaging.runtime_dev_dependency_separation_required is True
    assert packaging.pytest_must_not_be_runtime_dependency is True
    assert packaging.py_typed_required is True
    assert packaging.package_include_exclude_policy_required is True
    assert packaging.runtime_data_excluded_from_package is True
    assert packaging.references_excluded_or_policy_controlled is True
    assert packaging.wheel_build_smoke_required is True
    assert packaging.sdist_build_smoke_required is True
    assert packaging.import_smoke_required is True
    assert packaging.cli_smoke_required is True
    assert packaging.package_publish_enabled_now is False
    assert public_private.boundary_deferred_to == "v0.28.3"
    assert public_private.public_core_private_overlay_required is True
    assert public_private.public_repo_must_not_contain_company_material is True
    assert public_private.public_repo_must_not_contain_credentials is True
    assert public_private.public_repo_must_not_contain_internal_endpoints is True
    assert public_private.public_repo_must_not_contain_raw_traces is True
    assert public_private.public_repo_must_not_contain_raw_transcripts is True
    assert public_private.public_repo_must_not_contain_raw_provider_outputs is True
    assert public_private.public_repo_may_contain_sanitized_examples is True
    assert public_private.public_repo_may_contain_synthetic_demo_data is True
    assert public_private.private_overlay_required_for_schumpeter is True
    assert preparation.split_preparation_deferred_to == "v0.28.5"
    assert preparation.decision_framework_required_before_split is True
    assert preparation.actual_split_enabled_now is False
    assert preparation.company_wrapper_enabled_now is False
    assert preparation.private_distribution_enabled_now is False
    assert preparation.company_config_forbidden_in_public_core is True
    assert preparation.company_credentials_forbidden_in_public_core is True
    assert preparation.company_endpoint_forbidden_in_public_core is True
    assert preparation.company_rpa_integration_forbidden_now is True
    assert preparation.references_schumpeter_reference_only_by_default is True
    assert inventory.inventory_deferred_to == "v0.28.4"
    assert inventory.references_schumpeter_is_not_runtime_dependency is True
    assert inventory.references_schumpeter_is_not_copied_into_core_by_default is True
    assert inventory.origin_required is True
    assert inventory.license_status_required is True
    assert inventory.private_data_risk_required is True
    assert inventory.company_material_risk_required is True
    assert inventory.OCEL_compatibility_required is True
    assert {"adopt_concept", "port_model_later", "port_test_later", "port_document_later", "keep_reference_only", "quarantine_due_to_license_or_private_risk", "discard"} <= set(reuse.allowed_dispositions)
    assert reuse.reuse_requires_decision_record is True
    assert reuse.reuse_requires_license_review is True
    assert reuse.reuse_requires_public_private_boundary_review is True
    assert reuse.runtime_dependency_forbidden_now is True
    assert reuse.code_copy_forbidden_now is True
    assert preflight.preflight_deferred_to == "v0.28.8"
    assert preflight.external_adapter_implementation_deferred_to == "v0.29.x"
    assert preflight.provider_invocation_forbidden_now is True
    assert preflight.adapter_registration_forbidden_now is True
    assert preflight.capability_declaration_is_not_permission is True
    assert preflight.provider_adapter_contract_is_not_provider_invocation is True
    assert preflight.safety_gate_required_before_invocation is True
    assert preflight.permission_gate_required_before_invocation is True
    assert preflight.audit_required_before_invocation is True
    assert preflight.rollback_boundary_required_before_invocation is True
    assert preflight.credential_boundary_required_before_invocation is True
    assert preflight.network_boundary_required_before_invocation is True
    assert v029.contract_first_required is True
    assert v029.provider_invocation_reopen_requires_preflight is True
    assert v029.command_execution_reopen_requires_preflight is True
    assert v029.credential_handling_reopen_requires_boundary is True
    assert v029.network_access_reopen_requires_boundary is True
    assert v029.adapter_certification_required is True
    assert v029.OCEL_visibility_required is True
    assert v029.permission_gate_required is True
    assert v029.safety_gate_required is True
    assert v029.no_background_execution_without_gate is True


def test_schumpeter_decision_framework_and_safety_boundary() -> None:
    parts = _parts()
    framework = parts["schumpeter_decision_framework"]
    safety = parts["safety_boundary"]

    assert framework.decision_framework_deferred_to == "v0.28.4"
    assert framework.decision_required_before_split is True
    assert framework.default_option == "keep_reference_only_and_prepare_private_overlay"
    assert framework.actual_decision_made_now is False
    assert framework.split_implemented_now is False
    assert {
        "keep_reference_only",
        "prepare_private_overlay",
        "prepare_distribution_profile",
        "defer_split",
        "block_split",
        "deprecate_legacy_schumpeter",
        "extract_concepts_only",
        "extract_tests_only",
        "extract_docs_only",
        "migrate_specific_module_later",
    } <= set(framework.decision_outputs)
    assert {"no_split", "reference_only", "public_core_private_overlay", "private_distribution_profile", "separate_private_repo", "merge_schumpeter_into_core", "deprecate_legacy_schumpeter"} <= {
        option.option_name for option in framework.options
    }
    assert all(option.implementation_now is False for option in framework.options)
    assert {
        "ip_license_risk",
        "company_private_data_contamination_risk",
        "public_core_contamination_risk",
        "architecture_overlap",
        "code_reuse_value",
        "concept_reuse_value",
        "test_reuse_value",
        "doc_reuse_value",
        "OCEL_compatibility",
        "PIG_compatibility",
        "memory_workbench_compatibility",
        "runtime_dependency_risk",
        "maintainability",
        "testability",
        "deployment_boundary_clarity",
        "security_credential_exposure_risk",
        "future_external_adapter_compatibility",
        "organizational_usefulness",
    } <= {criterion.criterion_name for criterion in framework.criteria}
    assert safety.public_alpha_safety_boundary_required is True
    assert safety.provider_invocation_enabled_now is False
    assert safety.command_execution_enabled_now is False
    assert safety.file_mutation_expansion_enabled_now is False
    assert safety.runtime_continuity_injection_enabled_now is False
    assert safety.autonomous_memory_driven_execution_enabled_now is False
    assert safety.external_adapter_enabled_now is False
    assert safety.schumpeter_split_enabled_now is False
    assert safety.company_deployment_enabled_now is False
    assert safety.secret_exposure_forbidden is True
    assert safety.credential_exposure_forbidden is True
    assert safety.raw_trace_exposure_forbidden is True
    assert safety.raw_transcript_exposure_forbidden is True
    assert safety.raw_provider_output_exposure_forbidden is True
    assert safety.PIG_execution_authority_forbidden is True
    assert safety.llm_judge_as_sole_readiness_authority_forbidden is True


def test_report_flags_prerequisites_ocel_pig_ocpx_and_cli(capsys) -> None:
    service = V028ContractReportService()
    parts = service.build_all_parts()
    report = parts["report"]
    source = V028ContractPrerequisiteSourceService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert source.load_v0279_memory_consolidation_report().version == "v0.27.9"
    assert source.load_v02610_release_hygiene_report_if_available() is None
    assert report.report_status == "warning"
    assert report.ready_for_v0_28_1 is True
    assert report.ready_for_v0_29 is False
    assert report.contract_created is True
    assert report.roadmap_created is True
    assert report.public_alpha_scope_policy_created is True
    assert report.public_alpha_stage_policy_created is True
    assert report.release_hygiene_debt_policy_created is True
    assert report.release_hygiene_blocking_policy_created is True
    assert report.packaging_readiness_policy_created is True
    assert report.public_private_boundary_policy_created is True
    assert report.schumpeter_split_preparation_policy_created is True
    assert report.schumpeter_split_decision_framework_created is True
    assert report.schumpeter_reference_inventory_policy_created is True
    assert report.schumpeter_reuse_disposition_policy_created is True
    assert report.external_adapter_preflight_boundary_created is True
    assert report.v029_risk_reopen_criteria_created is True
    assert report.public_alpha_safety_boundary_policy_created is True
    assert report.public_alpha_implemented is False
    assert report.public_alpha_ready is False
    assert report.schumpeter_split_implemented is False
    assert report.company_wrapper_implemented is False
    assert report.external_adapter_implemented is False
    assert report.external_dominion_bridge_implemented is False
    assert report.provider_invoked is False
    assert report.command_executed is False
    assert report.runtime_continuity_injected is False
    assert report.autonomous_memory_execution_enabled is False
    assert report.package_published is False
    assert report.release_tag_created is False
    assert report.references_schumpeter_runtime_dependency_added is False
    assert report.references_schumpeter_code_copied is False
    assert report.company_private_material_exposed is False
    assert report.credential_exposed is False
    assert report.raw_trace_exposed is False
    assert report.raw_transcript_exposed is False
    assert report.raw_provider_output_exposed is False
    assert report.PIG_execution_authority_enabled is False
    assert report.llm_judge_used is False
    assert report.next_required_step == "v0.28.1 Release Hygiene / Repository Governance Blocking Gate"
    assert "public_alpha_schumpeter_preparation_contract" in V028_OBJECT_TYPES
    assert "v028_contract_report_created" in V028_EVENT_TYPES
    assert "public_alpha_schumpeter_contract_declared" in V028_EFFECT_TYPES
    assert "public_alpha_implemented" in V028_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.28.0"
    assert pig["subject"] == "public_alpha_schumpeter_preparation_contract"
    assert pig["safety_boundary"]["public_alpha_implemented"] is False
    assert pig["safety_boundary"]["PIG_execution_authority_enabled"] is False
    assert ocpx["state"] == "public_alpha_schumpeter_preparation_contract_declared"
    assert "PublicAlphaSchumpeterPreparationContractState" in ocpx["target_read_models"]
    assert "V029RiskReopenCriteriaState" in ocpx["target_read_models"]

    commands = [
        ["alpha", "contract"],
        ["alpha", "roadmap"],
        ["alpha", "scope-policy"],
        ["alpha", "stage-policy"],
        ["alpha", "hygiene-debt"],
        ["alpha", "hygiene-blocking-policy"],
        ["alpha", "packaging-policy"],
        ["alpha", "public-private-policy"],
        ["alpha", "schumpeter-preparation"],
        ["alpha", "schumpeter-decision-framework"],
        ["alpha", "schumpeter-reference-policy"],
        ["alpha", "external-adapter-preflight"],
        ["alpha", "v029-risk-reopen"],
        ["alpha", "safety-boundary"],
        ["alpha", "contract-report"],
    ]
    for command in commands:
        assert main(command) == 0
        output = capsys.readouterr().out
        assert "version=v0.28.0" in output
        assert "layer=public_alpha_schumpeter_preparation" in output
        assert "status=contract_only" in output
        assert "ready_for_v0_28_1=true" in output
        assert "ready_for_v0_29=false" in output
        assert "public_alpha_implemented=false" in output
        assert "public_alpha_ready=false" in output
        assert "schumpeter_split_implemented=false" in output
        assert "company_wrapper_implemented=false" in output
        assert "external_adapter_implemented=false" in output
        assert "external_dominion_bridge_implemented=false" in output
        assert "provider_invoked=false" in output
        assert "command_executed=false" in output
        assert "runtime_continuity_injected=false" in output
        assert "autonomous_memory_execution_enabled=false" in output
        assert "package_published=false" in output
        assert "release_tag_created=false" in output
        assert "references_schumpeter_runtime_dependency_added=false" in output
        assert "references_schumpeter_code_copied=false" in output
        assert "company_private_material_exposed=false" in output
        assert "credential_exposed=false" in output
        assert "raw_trace_exposed=false" in output
        assert "raw_transcript_exposed=false" in output
        assert "raw_provider_output_exposed=false" in output
        assert "PIG_execution_authority_enabled=false" in output
        assert "llm_judge_used=false" in output
        assert "next_required_step=v0.28.1 Release Hygiene / Repository Governance Blocking Gate" in output
