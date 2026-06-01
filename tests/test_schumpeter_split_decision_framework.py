from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.public_alpha_schumpeter_preparation import (
    SchumpeterArchitectureComparison,
    SchumpeterCapabilityComparisonMatrix,
    SchumpeterCapabilityComparisonRow,
    SchumpeterDecisionCriterion,
    SchumpeterDecisionCriterionScore,
    SchumpeterOCELPIGOCPXCompatibilityReview,
    SchumpeterReferenceArtifact,
    SchumpeterReferenceInventory,
    SchumpeterReferenceLicenseReview,
    SchumpeterReferencePrivateRiskReview,
    SchumpeterReferenceSourceView,
    SchumpeterReuseDispositionCandidate,
    SchumpeterReuseDispositionDecision,
    SchumpeterReuseDispositionPolicyRuntime,
    SchumpeterReuseValueAssessment,
    SchumpeterRiskAssessment,
    SchumpeterSplitDecisionAuditTrail,
    SchumpeterSplitDecisionCandidate,
    SchumpeterSplitDecisionFinding,
    SchumpeterSplitDecisionRecord,
    SchumpeterSplitDecisionReport,
    SchumpeterSplitDecisionReportService,
    SchumpeterSplitDecisionRequest,
    SchumpeterSplitDecisionRuntimePolicy,
    SchumpeterSplitOptionAssessment,
    SchumpeterSplitOptionCatalog,
    SchumpeterSplitRecommendation,
    SchumpeterWorkbenchMemoryCompatibilityReview,
    V0284_EFFECT_TYPES,
    V0284_EVENT_TYPES,
    V0284_FORBIDDEN_EFFECT_TYPES,
    V0284_OBJECT_TYPES,
)


def _parts() -> dict:
    return SchumpeterSplitDecisionReportService().build_all_parts()


def test_schumpeter_decision_framework_models_build() -> None:
    parts = _parts()
    report = parts["report"]

    assert isinstance(parts["decision-policy"], SchumpeterSplitDecisionRuntimePolicy)
    assert isinstance(report.request, SchumpeterSplitDecisionRequest)
    assert isinstance(parts["source-view"], SchumpeterReferenceSourceView)
    assert isinstance(parts["inventory"], SchumpeterReferenceInventory)
    assert isinstance(parts["inventory"].artifacts[0], SchumpeterReferenceArtifact)
    assert isinstance(parts["license-review"][0], SchumpeterReferenceLicenseReview)
    assert isinstance(parts["private-risk"][0], SchumpeterReferencePrivateRiskReview)
    assert isinstance(parts["architecture-comparison"], SchumpeterArchitectureComparison)
    assert isinstance(parts["capability-matrix"], SchumpeterCapabilityComparisonMatrix)
    assert isinstance(parts["capability-matrix"].rows[0], SchumpeterCapabilityComparisonRow)
    assert isinstance(parts["ocel-pig-ocpx"], SchumpeterOCELPIGOCPXCompatibilityReview)
    assert isinstance(parts["workbench-memory"], SchumpeterWorkbenchMemoryCompatibilityReview)
    assert isinstance(parts["reuse-value"][0], SchumpeterReuseValueAssessment)
    assert isinstance(parts["risk"][0], SchumpeterRiskAssessment)
    assert isinstance(report.split_option_catalog, SchumpeterSplitOptionCatalog)
    assert isinstance(parts["options"][0], SchumpeterSplitOptionAssessment)
    assert isinstance(parts["criteria"][0], SchumpeterDecisionCriterion)
    assert isinstance(report.criterion_scores[0], SchumpeterDecisionCriterionScore)
    assert isinstance(report.reuse_disposition_policy, SchumpeterReuseDispositionPolicyRuntime)
    assert isinstance(report.reuse_disposition_candidates[0], SchumpeterReuseDispositionCandidate)
    assert isinstance(parts["disposition"][0], SchumpeterReuseDispositionDecision)
    assert isinstance(report.split_decision_candidates[0], SchumpeterSplitDecisionCandidate)
    assert isinstance(parts["recommendation"], SchumpeterSplitRecommendation)
    assert isinstance(parts["decision-record"][0], SchumpeterSplitDecisionRecord)
    assert isinstance(parts["audit"], SchumpeterSplitDecisionAuditTrail)
    assert isinstance(report.findings[0], SchumpeterSplitDecisionFinding)
    assert isinstance(report, SchumpeterSplitDecisionReport)


def test_decision_policy_source_inventory_license_and_private_risk() -> None:
    parts = _parts()
    policy = parts["decision-policy"]
    source = parts["source-view"]
    inventory = parts["inventory"]
    artifact = inventory.artifacts[0]
    license_review = parts["license-review"][0]
    private_review = parts["private-risk"][0]

    assert policy.version == "v0.28.4"
    assert policy.layer == "public_alpha_schumpeter_preparation"
    assert policy.decision_framework_enabled is True
    assert policy.reference_inventory_enabled is True
    assert policy.capability_comparison_enabled is True
    assert policy.license_review_required is True
    assert policy.private_risk_review_required is True
    assert policy.public_private_boundary_required is True
    assert policy.reuse_disposition_required is True
    assert policy.decision_record_required is True
    assert policy.audit_required is True
    assert policy.actual_split_enabled_now is False
    assert policy.company_wrapper_enabled_now is False
    assert policy.private_distribution_runtime_enabled_now is False
    assert policy.separate_private_repo_creation_enabled_now is False
    assert policy.merge_into_public_core_enabled_now is False
    assert policy.references_runtime_dependency_enabled_now is False
    assert policy.references_code_copy_enabled_now is False
    assert policy.file_move_enabled_now is False
    assert policy.destructive_redaction_enabled_now is False
    assert policy.package_publish_enabled_now is False
    assert policy.release_tag_creation_enabled_now is False
    assert policy.external_adapter_enabled_now is False
    assert policy.provider_invocation_enabled_now is False
    assert policy.command_execution_enabled_now is False
    assert policy.runtime_continuity_injection_enabled_now is False
    assert policy.unknown_license_is_safe is False
    assert policy.unknown_private_risk_is_safe is False
    assert policy.default_decision_posture == "keep_reference_only_and_prepare_private_overlay"
    assert policy.no_split_is_valid_outcome is True
    assert policy.defer_split_is_valid_outcome is True
    assert policy.keep_reference_only_is_valid_outcome is True
    assert policy.llm_judge_as_sole_decision_authority_forbidden is True
    assert source.public_private_boundary_report_ref is not None
    assert source.reference_governance_report_ref is not None
    assert source.reference_license_boundary_report_ref is not None
    assert source.references_inventory_ref is not None
    assert source.company_material_detected is False
    assert source.credential_detected is False
    assert source.raw_trace_detected is False
    assert source.raw_transcript_detected is False
    assert source.raw_provider_output_detected is False
    assert inventory.artifact_count >= 1
    assert inventory.license_unknown_count >= 1
    assert inventory.private_risk_unknown_count >= 1
    assert inventory.references_used_as_runtime_dependency is False
    assert inventory.references_code_copied_now is False
    assert artifact.license_status in {"unknown", "known_compatible", "known_incompatible", "not_applicable"}
    assert artifact.private_data_risk in {"none", "low", "medium", "high", "blocked", "unknown"}
    assert artifact.runtime_dependency_allowed_now is False
    assert artifact.code_copy_allowed_now is False
    assert license_review.license_review_required is True
    assert license_review.license_status == "unknown"
    assert license_review.license_blocks_public_core_adoption is True
    assert private_review.private_data_risk == "unknown"
    assert private_review.public_core_adoption_allowed is False
    assert private_review.private_overlay_only is True
    assert private_review.quarantine_required is True


def test_comparisons_reuse_risk_options_criteria_and_disposition() -> None:
    parts = _parts()
    architecture = parts["architecture-comparison"]
    matrix = parts["capability-matrix"]
    compatibility = parts["ocel-pig-ocpx"]
    workbench = parts["workbench-memory"]
    reuse = parts["reuse-value"][0]
    risk = parts["risk"][0]
    option_catalog = parts["report"].split_option_catalog
    option_names = {item.option_name for item in parts["options"]}
    criteria_names = {item.criterion_name for item in parts["criteria"]}
    disposition_policy = parts["report"].reuse_disposition_policy
    disposition = parts["disposition"][0]

    assert {"OCEL_trace", "reflective_substrate", "memory", "workbench", "provider_boundary", "skill_boundary", "runtime_loop", "safety_boundary", "governance_boundary"} <= set(architecture.compared_dimensions)
    assert matrix.compared_capability_count >= 1
    assert all(row.recommended_disposition for row in matrix.rows)
    assert compatibility.blocks_public_core_adoption is True
    assert compatibility.supports_concept_reuse is True
    assert compatibility.supports_future_private_overlay is True
    assert workbench.supports_concept_reuse is True
    assert workbench.supports_future_profile_boundary is True
    assert reuse.recommended_reuse_mode in {"concept_only", "docs_only", "tests_later", "model_later", "private_overlay_later", "reference_only", "discard", "quarantine", "unknown"}
    assert reuse.runtime_dependency_added_now is False
    assert reuse.code_copied_now is False
    assert risk.blocks_public_core_adoption is True
    assert risk.blocks_split_implementation_now is True
    assert {"no_split", "reference_only", "public_core_private_overlay", "private_distribution_profile", "separate_private_repo", "merge_schumpeter_into_core", "deprecate_legacy_schumpeter"} <= set(option_catalog.options)
    assert option_catalog.default_option == "reference_only"
    assert {"reference_only", "public_core_private_overlay_preparation"} <= set(option_catalog.safe_default_combination)
    assert {"no_split", "reference_only", "merge_schumpeter_into_core"} <= option_names
    assert all(item.implementation_allowed_now is False for item in parts["options"])
    assert {"ip_license_risk", "company_private_data_contamination_risk", "public_core_contamination_risk", "architecture_overlap", "code_reuse_value", "concept_reuse_value", "test_reuse_value", "doc_reuse_value", "OCEL_compatibility", "PIG_compatibility", "OCPX_compatibility", "memory_workbench_compatibility", "runtime_dependency_risk", "maintainability", "testability", "deployment_boundary_clarity", "security_credential_exposure_risk", "future_external_adapter_compatibility", "organizational_usefulness"} <= criteria_names
    assert len(parts["report"].criterion_scores) == len(parts["criteria"])
    assert {"adopt_concept", "port_model_later", "port_test_later", "port_document_later", "keep_reference_only", "quarantine_due_to_license_or_private_risk", "discard"} <= set(disposition_policy.allowed_dispositions)
    assert disposition_policy.runtime_dependency_forbidden_now is True
    assert disposition_policy.code_copy_forbidden_now is True
    assert disposition_policy.disposition_decision_is_not_migration is True
    assert disposition.migration_allowed_now is False
    assert disposition.runtime_dependency_added_now is False
    assert disposition.code_copied_now is False


def test_recommendation_decision_record_audit_report_ocel_pig_ocpx_and_cli(capsys) -> None:
    service = SchumpeterSplitDecisionReportService()
    parts = service.build_all_parts()
    report = parts["report"]
    recommendation = parts["recommendation"]
    record = parts["decision-record"][0]
    audit = parts["audit"]
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert report.split_decision_candidates[0].implementation_allowed_now is False
    assert report.split_decision_candidates[0].split_performed_now is False
    assert recommendation.recommended_option == "keep_reference_only_and_prepare_private_overlay"
    assert recommendation.implementation_performed_now is False
    assert "v0.28.5 Schumpeter Split Preparation Profile" in recommendation.required_next_steps
    assert record.decision_type in {"keep_reference_only", "prepare_private_overlay", "defer_split", "block_split", "no_split", "no_op"}
    assert record.split_implemented_now is False
    assert record.company_wrapper_implemented_now is False
    assert record.runtime_dependency_added_now is False
    assert record.code_copied_now is False
    assert record.file_moved_now is False
    assert audit.raw_content_included is False
    assert audit.audit_event_count >= 1
    assert report.ready_for_v0_28_5 is True
    assert report.ready_for_public_alpha_release_claim is False
    assert report.schumpeter_decision_framework_ready is True
    assert report.schumpeter_split_decision_ready is True
    assert report.recommended_default == "keep_reference_only_and_prepare_private_overlay"
    assert report.actual_split_implemented is False
    assert report.company_wrapper_implemented is False
    assert report.private_repo_created is False
    assert report.merge_into_public_core_performed is False
    assert report.references_runtime_dependency_added is False
    assert report.references_code_copied is False
    assert report.file_moved is False
    assert report.destructive_redaction_performed is False
    assert report.external_adapter_implemented is False
    assert report.package_published is False
    assert report.release_tag_created is False
    assert report.provider_invoked is False
    assert report.command_executed is False
    assert report.runtime_continuity_injected is False
    assert report.company_private_material_exposed is False
    assert report.credential_exposed is False
    assert report.secret_exposed is False
    assert report.raw_trace_exposed is False
    assert report.raw_transcript_exposed is False
    assert report.raw_provider_output_exposed is False
    assert report.PIG_execution_authority_enabled is False
    assert report.llm_judge_used is False
    assert report.next_required_step == "v0.28.5 Schumpeter Split Preparation Profile"
    assert "schumpeter_split_decision_report" in V0284_OBJECT_TYPES
    assert "schumpeter_split_decision_report_created" in V0284_EVENT_TYPES
    assert "schumpeter_split_decision_framework_created" in V0284_EFFECT_TYPES
    assert "schumpeter_split_implemented" in V0284_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.28.4"
    assert pig["subject"] == "schumpeter_split_decision_framework"
    assert ocpx["state"] == "schumpeter_split_decision_framework_created"
    assert "SchumpeterSplitDecisionFrameworkState" in ocpx["target_read_models"]

    for command in [
        "decision-policy",
        "source-view",
        "inventory",
        "license-review",
        "private-risk",
        "architecture-comparison",
        "capability-matrix",
        "ocel-pig-ocpx",
        "workbench-memory",
        "reuse-value",
        "risk",
        "options",
        "criteria",
        "disposition",
        "recommendation",
        "decision-record",
        "audit",
        "report",
    ]:
        assert main(["alpha", "schumpeter", command]) == 0
        output = capsys.readouterr().out
        assert "version=v0.28.4" in output
        assert "ready_for_v0_28_5=true" in output
        assert "ready_for_public_alpha_release_claim=false" in output
        assert "recommended_default=keep_reference_only_and_prepare_private_overlay" in output
        assert "actual_split_implemented=false" in output
        assert "company_wrapper_implemented=false" in output
        assert "private_repo_created=false" in output
        assert "merge_into_public_core_performed=false" in output
        assert "references_runtime_dependency_added=false" in output
        assert "references_code_copied=false" in output
        assert "file_moved=false" in output
        assert "destructive_redaction_performed=false" in output
        assert "provider_invoked=false" in output
        assert "command_executed=false" in output
        assert "llm_judge_used=false" in output
