from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.public_alpha_schumpeter_preparation import (
    CompanyMaterialExclusionPolicy,
    CredentialExclusionPolicy,
    DocumentationExposurePolicy,
    ExampleDataPolicy,
    PackageExposureBoundaryReport,
    PrivateArtifactPolicy,
    PublicArtifactPolicy,
    PublicDatasetPolicy,
    PublicPrivateArtifactClassification,
    PublicPrivateBoundaryFinding,
    PublicPrivateBoundaryReport,
    PublicPrivateBoundaryReportService,
    PublicPrivateBoundaryRequest,
    PublicPrivateBoundaryRuntimePolicy,
    PublicPrivateBoundarySourceView,
    PublicPrivateClassificationRule,
    PublicPrivateQuarantineRecommendation,
    PublicPrivateReleaseGate,
    PublicPrivateRemediationPlan,
    RawProviderOutputExclusionPolicy,
    RawTraceExclusionPolicy,
    RawTranscriptExclusionPolicy,
    RedactionDecisionRecord,
    RedactionPolicy,
    RedactionPreview,
    ReferenceCodePolicy,
    ReferenceGovernanceReport,
    ReferenceLicenseBoundaryReport,
    SanitizedExamplePolicy,
    SecretExclusionPolicy,
    SyntheticDataPolicy,
    ThirdPartyReferenceInventoryBoundary,
    V0283_EFFECT_TYPES,
    V0283_EVENT_TYPES,
    V0283_FORBIDDEN_EFFECT_TYPES,
    V0283_OBJECT_TYPES,
)


def _parts() -> dict:
    return PublicPrivateBoundaryReportService().build_all_parts()


def test_public_private_boundary_models_build() -> None:
    parts = _parts()
    report = parts["report"]

    assert isinstance(parts["policy"], PublicPrivateBoundaryRuntimePolicy)
    assert isinstance(report.request, PublicPrivateBoundaryRequest)
    assert isinstance(parts["source-view"], PublicPrivateBoundarySourceView)
    assert isinstance(parts["public-policy"], PublicArtifactPolicy)
    assert isinstance(parts["private-policy"], PrivateArtifactPolicy)
    assert isinstance(report.classification_rules[0], PublicPrivateClassificationRule)
    assert isinstance(parts["classify"][0], PublicPrivateArtifactClassification)
    assert isinstance(parts["redaction-policy"], RedactionPolicy)
    assert isinstance(parts["redaction-preview"][0], RedactionPreview)
    assert isinstance(report.redaction_decision_records[0], RedactionDecisionRecord)
    assert isinstance(parts["secrets"], SecretExclusionPolicy)
    assert isinstance(parts["credentials"], CredentialExclusionPolicy)
    assert isinstance(parts["company-material"], CompanyMaterialExclusionPolicy)
    assert isinstance(parts["raw-traces"], RawTraceExclusionPolicy)
    assert isinstance(parts["raw-transcripts"], RawTranscriptExclusionPolicy)
    assert isinstance(parts["raw-provider-outputs"], RawProviderOutputExclusionPolicy)
    assert isinstance(report.reference_code_policy, ReferenceCodePolicy)
    assert isinstance(report.third_party_reference_inventory_boundary, ThirdPartyReferenceInventoryBoundary)
    assert isinstance(parts["references"], ReferenceGovernanceReport)
    assert isinstance(parts["reference-license"], ReferenceLicenseBoundaryReport)
    assert isinstance(parts["datasets"], PublicDatasetPolicy)
    assert isinstance(parts["examples"], ExampleDataPolicy)
    assert isinstance(report.sanitized_example_policy, SanitizedExamplePolicy)
    assert isinstance(report.synthetic_data_policy, SyntheticDataPolicy)
    assert isinstance(parts["docs"], DocumentationExposurePolicy)
    assert isinstance(parts["package-exposure"], PackageExposureBoundaryReport)
    assert isinstance(parts["remediation"].quarantine_recommendations[0], PublicPrivateQuarantineRecommendation)
    assert isinstance(parts["remediation"], PublicPrivateRemediationPlan)
    assert isinstance(parts["release-gate"], PublicPrivateReleaseGate)
    assert isinstance(report.findings[0], PublicPrivateBoundaryFinding)
    assert isinstance(report, PublicPrivateBoundaryReport)


def test_boundary_runtime_public_private_policy_and_source_view() -> None:
    parts = _parts()
    policy = parts["policy"]
    source = parts["source-view"]
    public = parts["public-policy"]
    private = parts["private-policy"]

    assert policy.version == "v0.28.3"
    assert policy.layer == "public_alpha_schumpeter_preparation"
    assert policy.boundary_enabled is True
    assert policy.public_core_private_overlay_required is True
    assert policy.public_artifact_classification_required is True
    assert policy.redaction_policy_required is True
    assert policy.reference_policy_required is True
    assert policy.public_dataset_policy_required is True
    assert policy.example_data_policy_required is True
    assert policy.package_exposure_boundary_required is True
    assert policy.destructive_redaction_enabled_now is False
    assert policy.source_file_deletion_enabled_now is False
    assert policy.repo_split_enabled_now is False
    assert policy.schumpeter_split_enabled_now is False
    assert policy.company_wrapper_enabled_now is False
    assert policy.package_publish_enabled_now is False
    assert policy.release_tag_creation_enabled_now is False
    assert policy.external_adapter_enabled_now is False
    assert policy.provider_invocation_enabled_now is False
    assert policy.command_execution_enabled_now is False
    assert policy.runtime_continuity_injection_enabled_now is False
    assert policy.references_runtime_dependency_forbidden is True
    assert policy.references_code_copy_forbidden_now is True
    assert policy.public_secret_forbidden is True
    assert policy.public_raw_provider_output_forbidden is True
    assert policy.llm_judge_as_sole_boundary_authority_forbidden is True
    assert source.packaging_readiness_report_ref is not None
    assert source.package_data_boundary_report_ref is not None
    assert source.release_hygiene_gate_report_ref is not None
    assert source.forbidden_artifact_scan_report_ref is not None
    assert source.company_private_material_detected is False
    assert source.credential_detected is False
    assert source.secret_detected is False
    assert source.raw_trace_detected is False
    assert source.raw_transcript_detected is False
    assert source.raw_provider_output_detected is False
    assert "public_docs" in public.public_artifacts_allowed
    assert "architecture_docs" in public.public_artifacts_allowed
    assert "sanitized_examples" in public.public_artifacts_allowed
    assert "synthetic_demo_data" in public.public_artifacts_allowed
    assert "generic_OCEL_samples" in public.public_artifacts_allowed
    assert "package_source_code" in public.public_artifacts_allowed
    assert "company_private_material" in public.public_artifacts_forbidden
    assert "credentials" in public.public_artifacts_forbidden
    assert "secrets" in public.public_artifacts_forbidden
    assert "raw_provider_outputs" in public.public_artifacts_forbidden
    assert "runtime_db" in public.public_artifacts_forbidden
    assert "backup_files" in public.public_artifacts_forbidden
    assert "company_config" in private.private_artifacts
    assert "A360_connection_details" in private.private_artifacts
    assert "Brity_connection_details" in private.private_artifacts
    assert "UiPath_connection_details" in private.private_artifacts
    assert private.public_core_must_not_depend_on_private_artifacts is True


def test_classification_redaction_exclusion_and_reference_policies() -> None:
    parts = _parts()
    rule_names = {rule.rule_name for rule in parts["report"].classification_rules}
    required = {
        "credentials_are_private_only",
        "secrets_are_private_only",
        "company_endpoints_are_private_only",
        "raw_traces_are_private_only",
        "raw_transcripts_are_private_only",
        "raw_provider_outputs_are_private_only",
        "runtime_db_is_forbidden_public_artifact",
        "backup_files_are_forbidden_public_artifact",
        "references_are_reference_only_by_default",
        "references_are_not_runtime_dependency",
        "references_code_copy_forbidden_now",
        "examples_must_be_sanitized_or_synthetic",
        "docs_must_not_expose_company_material",
        "package_data_must_not_include_private_artifacts",
        "Schumpeter_reference_is_not_split_implementation",
        "RPA_adapter_details_are_private_or_future_track",
    }
    classifications = parts["classify"]
    redaction_policy = parts["redaction-policy"]
    preview = parts["redaction-preview"][0]
    decision = parts["report"].redaction_decision_records[0]
    reference_policy = parts["report"].reference_code_policy
    reference_governance = parts["references"]

    assert required <= rule_names
    assert any(item.classification == "reference_only" for item in classifications)
    assert any(item.classification == "private_only" for item in classifications)
    assert any(item.public_release_blocker for item in classifications)
    assert redaction_policy.redaction_preview_enabled is True
    assert redaction_policy.destructive_redaction_enabled_now is False
    assert redaction_policy.source_file_mutation_enabled_now is False
    assert redaction_policy.source_file_deletion_enabled_now is False
    assert redaction_policy.redact_credentials is True
    assert redaction_policy.redact_secrets is True
    assert redaction_policy.redact_internal_endpoints is True
    assert redaction_policy.redact_raw_trace_content is True
    assert redaction_policy.redact_raw_transcript_content is True
    assert redaction_policy.redact_raw_provider_output_content is True
    assert preview.redaction_apply_performed_now is False
    assert preview.source_file_mutated is False
    assert preview.source_file_deleted is False
    assert decision.applies_redaction_now is False
    assert decision.mutates_file_now is False
    assert decision.deletes_file_now is False
    assert parts["secrets"].secrets_forbidden_in_public_core is True
    assert parts["credentials"].credentials_forbidden_in_public_core is True
    assert parts["company-material"].company_rpa_details_forbidden_in_public_core is True
    assert parts["raw-traces"].raw_traces_forbidden_in_public_core is True
    assert parts["raw-transcripts"].raw_transcripts_forbidden_in_public_core is True
    assert parts["raw-provider-outputs"].raw_provider_outputs_forbidden_in_public_core is True
    assert reference_policy.references_are_reference_only_by_default is True
    assert reference_policy.references_not_runtime_dependency is True
    assert reference_policy.references_code_copy_forbidden_now is True
    assert reference_policy.schumpeter_reference_split_decision_deferred_to_v0284 is True
    assert reference_governance.references_runtime_dependency_count == 0
    assert reference_governance.references_code_copy_count == 0


def test_dataset_docs_package_exposure_gate_report_ocel_pig_ocpx_and_cli(capsys) -> None:
    service = PublicPrivateBoundaryReportService()
    parts = service.build_all_parts()
    report = parts["report"]
    package_exposure = parts["package-exposure"]
    remediation = parts["remediation"]
    gate = parts["release-gate"]
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert parts["datasets"].actual_user_data_forbidden is True
    assert parts["datasets"].actual_company_data_forbidden is True
    assert parts["datasets"].synthetic_data_allowed is True
    assert parts["examples"].examples_allowed_if_sanitized is True
    assert parts["examples"].examples_allowed_if_synthetic is True
    assert parts["examples"].examples_must_not_contain_credentials is True
    assert report.sanitized_example_policy.sanitized_example_must_not_be_reversible_to_private_data is True
    assert report.synthetic_data_policy.synthetic_data_must_not_be_actual_user_or_company_data is True
    assert parts["docs"].docs_must_not_expose_company_material is True
    assert parts["docs"].docs_must_not_expose_internal_endpoints is True
    assert parts["docs"].docs_may_reference_private_overlay_conceptually is True
    assert package_exposure.runtime_data_in_package_count == 0
    assert package_exposure.references_in_package_count == 0
    assert package_exposure.credential_in_package_count == 0
    assert package_exposure.raw_trace_in_package_count == 0
    assert package_exposure.raw_transcript_in_package_count == 0
    assert package_exposure.raw_provider_output_in_package_count == 0
    assert package_exposure.company_material_in_package_count == 0
    assert remediation.auto_redaction_performed is False
    assert remediation.file_deleted is False
    assert remediation.file_moved is False
    assert remediation.quarantine_recommendations[0].file_moved_now is False
    assert remediation.quarantine_recommendations[0].file_deleted_now is False
    assert gate.classification_complete is True
    assert gate.redaction_preview_complete is True
    assert gate.no_private_material_exposure is True
    assert gate.no_credential_exposure is True
    assert gate.no_secret_exposure is True
    assert gate.no_reference_runtime_dependency is True
    assert gate.no_reference_code_copy is True
    assert report.ready_for_v0_28_4 is True
    assert report.destructive_redaction_performed is False
    assert report.source_file_deleted is False
    assert report.file_moved is False
    assert report.repo_split_performed is False
    assert report.schumpeter_split_implemented is False
    assert report.company_wrapper_implemented is False
    assert report.package_published is False
    assert report.release_tag_created is False
    assert report.external_adapter_implemented is False
    assert report.provider_invoked is False
    assert report.command_executed is False
    assert report.runtime_continuity_injected is False
    assert report.references_runtime_dependency_added is False
    assert report.references_code_copied is False
    assert report.company_private_material_exposed is False
    assert report.credential_exposed is False
    assert report.secret_exposed is False
    assert report.raw_trace_exposed is False
    assert report.raw_transcript_exposed is False
    assert report.raw_provider_output_exposed is False
    assert report.llm_judge_used is False
    assert report.next_required_step == "v0.28.4 Schumpeter Split Decision Framework"
    assert "public_private_boundary_report" in V0283_OBJECT_TYPES
    assert "public_private_boundary_report_created" in V0283_EVENT_TYPES
    assert "public_private_boundary_created" in V0283_EFFECT_TYPES
    assert "destructive_redaction_performed" in V0283_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.28.3"
    assert pig["subject"] == "public_private_boundary_redaction_reference_policy"
    assert ocpx["state"] == "public_private_boundary_redaction_reference_policy_created"
    assert "PublicPrivateBoundaryState" in ocpx["target_read_models"]

    for command in [
        "policy",
        "source-view",
        "public-policy",
        "private-policy",
        "classify",
        "redaction-policy",
        "redaction-preview",
        "secrets",
        "credentials",
        "company-material",
        "raw-traces",
        "raw-transcripts",
        "raw-provider-outputs",
        "references",
        "reference-license",
        "datasets",
        "examples",
        "docs",
        "package-exposure",
        "remediation",
        "release-gate",
        "report",
    ]:
        assert main(["alpha", "boundary", command]) == 0
        output = capsys.readouterr().out
        assert "version=v0.28.3" in output
        assert "ready_for_v0_28_4=true" in output
        assert "destructive_redaction_performed=false" in output
        assert "source_file_deleted=false" in output
        assert "file_moved=false" in output
        assert "repo_split_performed=false" in output
        assert "schumpeter_split_implemented=false" in output
        assert "package_published=false" in output
        assert "release_tag_created=false" in output
        assert "provider_invoked=false" in output
        assert "command_executed=false" in output
        assert "references_runtime_dependency_added=false" in output
        assert "references_code_copied=false" in output
        assert "secret_exposed=false" in output
        assert "llm_judge_used=false" in output
