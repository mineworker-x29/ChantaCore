from dataclasses import fields
import inspect

import pytest

from chanta_core.agent_runtime import (
    RepairProposalDoNothingEvidence,
    RepairProposalDoNothingEvidenceKind,
    RepairProposalEligibilityDecision,
    RepairProposalEligibilityKind,
    RepairProposalEvidenceAssessment,
    RepairProposalEvidenceBundle,
    RepairProposalEvidenceConfidenceLevel,
    RepairProposalEvidenceContract,
    RepairProposalEvidenceDecisionKind,
    RepairProposalEvidenceFlagSet,
    RepairProposalEvidenceGap,
    RepairProposalEvidenceGapKind,
    RepairProposalEvidenceInput,
    RepairProposalEvidenceItem,
    RepairProposalEvidenceItemKind,
    RepairProposalEvidenceMode,
    RepairProposalEvidenceNoGenerationGuarantee,
    RepairProposalEvidencePolicy,
    RepairProposalEvidenceReadinessLevel,
    RepairProposalEvidenceReport,
    RepairProposalEvidenceRiskKind,
    RepairProposalEvidenceRunPreview,
    RepairProposalEvidenceSourceKind,
    RepairProposalEvidenceSourceRef,
    RepairProposalEvidenceStatus,
    RepairProposalEvidenceStrength,
    RepairProposalEvidenceUseKind,
    RepairProposalEvidenceValidationFinding,
    RepairProposalEvidenceValidationReport,
    V0381ReadinessReport,
    assess_repair_proposal_evidence,
    build_repair_proposal_do_nothing_evidence,
    build_repair_proposal_eligibility_decision,
    build_repair_proposal_evidence_assessment,
    build_repair_proposal_evidence_bundle,
    build_repair_proposal_evidence_contract,
    build_repair_proposal_evidence_flags,
    build_repair_proposal_evidence_gap,
    build_repair_proposal_evidence_input,
    build_repair_proposal_evidence_input_from_v037_artifacts,
    build_repair_proposal_evidence_item,
    build_repair_proposal_evidence_no_generation_guarantee,
    build_repair_proposal_evidence_policy,
    build_repair_proposal_evidence_report,
    build_repair_proposal_evidence_run_preview,
    build_repair_proposal_evidence_source_ref,
    build_repair_proposal_evidence_validation_finding,
    build_repair_proposal_evidence_validation_report,
    build_v0381_readiness_report,
    collect_repair_proposal_evidence_items,
    create_repair_proposal_do_nothing_evidence,
    create_repair_proposal_evidence_bundle,
    create_repair_proposal_evidence_contract,
    decide_repair_proposal_eligibility,
    default_repair_proposal_evidence_policy,
    identify_repair_proposal_evidence_gaps,
    repair_proposal_evidence_bundle_is_not_proposal,
    repair_proposal_evidence_flags_preserve_no_generation,
    repair_proposal_evidence_policy_blocks_generation,
    repair_proposal_eligibility_is_not_permission,
    v0381_readiness_report_is_not_execution_ready,
    validate_repair_proposal_evidence_bundle,
)


SAFE_FLAG_NAMES = {
    "ready_for_v0382_read_only_sandbox_source_context",
    "ready_for_v0383_repair_scope_planner_change_intent",
    "ready_for_v0384_proposed_diff_code_hunk_metadata",
    "ready_for_repair_proposal_evidence_contract",
    "ready_for_repair_proposal_evidence_bundle",
    "ready_for_repair_proposal_evidence_assessment",
    "ready_for_repair_proposal_eligibility_decision",
    "ready_for_repair_proposal_evidence_gap_register",
    "ready_for_repair_proposal_do_nothing_evidence",
    "ready_for_future_read_only_sandbox_source_context_input",
    "ready_for_future_repair_scope_planning_input",
    "ready_for_future_change_intent_input",
    "ready_for_future_proposed_diff_metadata_input",
    "ready_for_future_proposed_code_hunk_metadata_input",
}


def _unsafe_flag_names(cls):
    return [
        field.name
        for field in fields(cls)
        if field.name.startswith("ready_for_") and field.name not in SAFE_FLAG_NAMES
    ]


def test_taxonomies_have_required_values():
    assert {item.value for item in RepairProposalEvidenceMode} == {
        "evidence_contract",
        "evidence_bundle",
        "evidence_assessment",
        "eligibility_decision",
        "do_nothing_evidence",
        "future_source_context_input",
        "future_scope_planning_input",
        "future_patch_metadata_input",
        "blocked",
        "no_op",
        "unknown",
    }
    assert "v0380_repair_proposal_boundary" in {item.value for item in RepairProposalEvidenceSourceKind}
    assert "eligible_for_future_patch_metadata" in {item.value for item in RepairProposalEvidenceStatus}
    assert "design_handoff_ready_for_v0382" in {item.value for item in RepairProposalEvidenceReadinessLevel}
    assert "allow_future_patch_metadata_input" in {item.value for item in RepairProposalEvidenceDecisionKind}
    assert "timeout_retry_confusion_risk" in {item.value for item in RepairProposalEvidenceRiskKind}
    assert "test_result_envelope_evidence" in {item.value for item in RepairProposalEvidenceItemKind}
    assert {item.value for item in RepairProposalEvidenceStrength} == {
        "strong",
        "adequate",
        "weak",
        "insufficient",
        "contradictory",
        "missing",
        "unknown",
    }
    assert "inconclusive" in {item.value for item in RepairProposalEvidenceConfidenceLevel}
    assert "blocked_by_safety_boundary" in {item.value for item in RepairProposalEligibilityKind}
    assert "missing_do_nothing_comparison" in {item.value for item in RepairProposalEvidenceGapKind}
    assert "blocks_future_proposal_path" in {item.value for item in RepairProposalEvidenceUseKind}
    assert "do_nothing_preferred_due_to_passed_tests" in {item.value for item in RepairProposalDoNothingEvidenceKind}


def test_required_models_are_exported():
    for model in (
        RepairProposalEvidenceFlagSet,
        RepairProposalEvidenceSourceRef,
        RepairProposalEvidencePolicy,
        RepairProposalEvidenceInput,
        RepairProposalEvidenceItem,
        RepairProposalEvidenceGap,
        RepairProposalEvidenceAssessment,
        RepairProposalDoNothingEvidence,
        RepairProposalEligibilityDecision,
        RepairProposalEvidenceContract,
        RepairProposalEvidenceBundle,
        RepairProposalEvidenceValidationFinding,
        RepairProposalEvidenceValidationReport,
        RepairProposalEvidenceReport,
        RepairProposalEvidenceRunPreview,
        RepairProposalEvidenceNoGenerationGuarantee,
        V0381ReadinessReport,
    ):
        assert model is not None


def test_flags_allow_evidence_readiness_and_preserve_no_generation():
    flags = build_repair_proposal_evidence_flags()
    assert flags.repair_proposal_evidence_layer_constructed
    assert flags.repair_proposal_evidence_contract_available
    assert flags.repair_proposal_evidence_bundle_available
    assert flags.repair_proposal_evidence_assessment_available
    assert flags.repair_proposal_eligibility_decision_available
    assert flags.repair_proposal_evidence_gap_register_available
    assert flags.repair_proposal_do_nothing_evidence_available
    for name in SAFE_FLAG_NAMES:
        assert getattr(flags, name) is True
    assert repair_proposal_evidence_flags_preserve_no_generation(flags)
    for name in _unsafe_flag_names(RepairProposalEvidenceFlagSet) + ["production_certified"]:
        assert getattr(flags, name) is False


@pytest.mark.parametrize("field_name", _unsafe_flag_names(RepairProposalEvidenceFlagSet) + ["production_certified"])
def test_flags_reject_unsafe_true(field_name):
    with pytest.raises(ValueError):
        build_repair_proposal_evidence_flags(**{field_name: True})


def test_source_ref_is_not_source_read_or_generation():
    source = build_repair_proposal_evidence_source_ref()
    assert source.source_kind == RepairProposalEvidenceSourceKind.V0380_REPAIR_PROPOSAL_BOUNDARY
    assert source.evidence_refs


def test_evidence_policy_allows_evidence_only_and_blocks_runtime():
    policy = default_repair_proposal_evidence_policy()
    assert policy.allow_evidence_contract
    assert policy.allow_evidence_bundle
    assert policy.allow_evidence_assessment
    assert policy.allow_eligibility_decision
    assert policy.allow_future_source_context_input
    assert policy.allow_future_scope_planning_input
    assert policy.allow_future_patch_metadata_input
    assert policy.require_v0380_boundary
    assert policy.require_test_result_evidence
    assert policy.require_feedback_evidence
    assert policy.require_do_nothing_evidence
    assert policy.require_human_review_marker
    assert policy.reject_missing_dependency_install
    assert policy.reject_timeout_retry
    assert repair_proposal_evidence_policy_blocks_generation(policy)
    for name in (
        "allow_source_file_read",
        "allow_sandbox_source_read",
        "allow_repair_proposal_generation",
        "allow_proposed_diff_generation",
        "allow_proposed_code_hunk_generation",
        "allow_proposed_patch_envelope_generation",
        "allow_repair_patch_proposal",
        "allow_repair_execution",
        "allow_patch_application",
        "allow_apply_patch",
        "allow_git_apply",
        "allow_test_execution",
        "allow_subprocess",
        "allow_shell",
        "allow_dependency_install",
        "allow_network_access",
        "allow_model_provider_invocation",
        "allow_external_agent_execution",
        "allow_dominion_runtime",
    ):
        assert getattr(policy, name) is False
        with pytest.raises(ValueError):
            build_repair_proposal_evidence_policy(**{name: True})


def test_evidence_input_is_not_proposal_generation_request():
    evidence_input = build_repair_proposal_evidence_input_from_v037_artifacts()
    assert evidence_input.boundary_id
    assert evidence_input.test_result_envelope_id
    assert evidence_input.feedback_report_id
    required = {
        "source_read",
        "proposal_generation",
        "diff_generation",
        "hunk_generation",
        "file_write",
        "patch_apply",
        "repair_execution",
        "test_execution",
        "subprocess",
        "shell",
        "dependency_install",
        "network",
        "model_provider",
        "external_agent",
        "dominion",
    }
    assert required.issubset(set(evidence_input.prohibited_runtime_actions))
    with pytest.raises(ValueError):
        build_repair_proposal_evidence_input(prohibited_runtime_actions=["source_read"])


def test_evidence_item_gap_and_assessment_rules():
    missing_item = build_repair_proposal_evidence_item(
        evidence_item_id="missing-test-result",
        required=True,
        present=False,
        evidence_kind=RepairProposalEvidenceItemKind.TEST_RESULT_ENVELOPE_EVIDENCE,
    )
    gaps = identify_repair_proposal_evidence_gaps([missing_item])
    assert any(RepairProposalEvidenceGapKind(gap.gap_kind) == RepairProposalEvidenceGapKind.MISSING_TEST_RESULT for gap in gaps)
    assessment = assess_repair_proposal_evidence([missing_item], gaps)
    assert assessment.insufficient_evidence
    assert assessment.sufficient_for_future_source_context is False
    assert assessment.sufficient_for_future_scope_planning is False
    assert assessment.sufficient_for_future_patch_metadata is False

    contradictory_item = build_repair_proposal_evidence_item(
        evidence_item_id="contradictory-feedback",
        evidence_kind=RepairProposalEvidenceItemKind.FEEDBACK_REPORT_EVIDENCE,
        evidence_summary="contradictory evidence requires review",
        contradictory=True,
        evidence_strength=RepairProposalEvidenceStrength.CONTRADICTORY,
        confidence=RepairProposalEvidenceConfidenceLevel.LOW,
    )
    contradictory_gaps = identify_repair_proposal_evidence_gaps([contradictory_item])
    contradictory_assessment = assess_repair_proposal_evidence([contradictory_item], contradictory_gaps)
    assert contradictory_assessment.contradictory_evidence
    assert contradictory_assessment.human_review_required
    with pytest.raises(ValueError):
        build_repair_proposal_evidence_assessment(
            overall_strength=RepairProposalEvidenceStrength.WEAK,
            confidence=RepairProposalEvidenceConfidenceLevel.HIGH,
        )


def test_complete_evidence_can_support_future_inputs_without_current_permissions():
    evidence_input = build_repair_proposal_evidence_input()
    policy = build_repair_proposal_evidence_policy(
        min_strength_for_future_patch_metadata=RepairProposalEvidenceStrength.ADEQUATE,
    )
    items = collect_repair_proposal_evidence_items(evidence_input, policy)
    items.append(build_repair_proposal_evidence_item(
        evidence_item_id="do-nothing-item",
        evidence_kind=RepairProposalEvidenceItemKind.DO_NOTHING_EVIDENCE,
        source_ref_id=None,
        evidence_use=RepairProposalEvidenceUseKind.SUPPORTS_DO_NOTHING,
        required=True,
        present=True,
    ))
    gaps = identify_repair_proposal_evidence_gaps(items, policy)
    assert gaps == []
    assessment = assess_repair_proposal_evidence(items, gaps, policy)
    assert assessment.sufficient_for_future_source_context
    assert assessment.sufficient_for_future_scope_planning
    assert assessment.sufficient_for_future_patch_metadata
    do_nothing = create_repair_proposal_do_nothing_evidence(assessment)
    decision = decide_repair_proposal_eligibility(assessment, do_nothing)
    assert decision.eligible_for_future_source_context
    assert decision.eligible_for_future_scope_planning
    assert decision.eligible_for_future_patch_metadata
    assert repair_proposal_eligibility_is_not_permission(decision)
    assert decision.source_read_allowed_now is False
    assert decision.proposal_generation_allowed_now is False
    assert decision.diff_generation_allowed_now is False
    assert decision.hunk_generation_allowed_now is False
    assert decision.patch_envelope_generation_allowed_now is False
    assert decision.repair_execution_allowed_now is False


@pytest.mark.parametrize(
    "field_name",
    [
        "source_read_allowed_now",
        "proposal_generation_allowed_now",
        "diff_generation_allowed_now",
        "hunk_generation_allowed_now",
        "patch_envelope_generation_allowed_now",
        "repair_execution_allowed_now",
    ],
)
def test_eligibility_rejects_current_permissions(field_name):
    with pytest.raises(ValueError):
        build_repair_proposal_eligibility_decision(**{field_name: True})


def test_no_repair_needed_and_do_nothing_preferred_paths():
    do_nothing = create_repair_proposal_do_nothing_evidence(passed_or_no_failure=True)
    assert do_nothing.do_nothing_preferred
    assessment = build_repair_proposal_evidence_assessment(
        evidence_assessment_id="passed-assessment",
        overall_strength=RepairProposalEvidenceStrength.ADEQUATE,
        confidence=RepairProposalEvidenceConfidenceLevel.MEDIUM,
        sufficient_for_future_source_context=False,
        sufficient_for_future_scope_planning=False,
        sufficient_for_future_patch_metadata=False,
    )
    decision = decide_repair_proposal_eligibility(assessment, do_nothing)
    assert decision.eligibility_kind == RepairProposalEligibilityKind.DO_NOTHING_PREFERRED
    assert decision.eligible_for_future_source_context is False
    no_repair = build_repair_proposal_eligibility_decision(
        eligibility_kind=RepairProposalEligibilityKind.NO_REPAIR_NEEDED,
        decision_kind=RepairProposalEvidenceDecisionKind.CHOOSE_NO_REPAIR_NEEDED,
        decision_summary="no repair needed",
        rationale_summary="no failure evidence",
        eligible_for_future_source_context=False,
        eligible_for_future_scope_planning=False,
        eligible_for_future_patch_metadata=False,
    )
    assert repair_proposal_eligibility_is_not_permission(no_repair)


def test_missing_dependency_and_timeout_do_not_grant_install_or_retry():
    policy = build_repair_proposal_evidence_policy()
    assert policy.reject_missing_dependency_install
    assert policy.reject_timeout_retry
    assert policy.allow_dependency_install is False
    assert "retry" not in RepairProposalEvidenceFlagSet.__dataclass_fields__ or not build_repair_proposal_evidence_flags().ready_for_retry_loop


def test_contract_allows_no_now_permissions():
    contract = create_repair_proposal_evidence_contract(build_repair_proposal_evidence_input())
    assert contract.requires_boundary
    assert contract.requires_test_result
    assert contract.requires_feedback_or_diagnosis
    assert contract.requires_do_nothing_evidence
    assert contract.requires_human_review_marker
    for name in (
        "allows_source_read_now",
        "allows_proposal_generation_now",
        "allows_diff_generation_now",
        "allows_hunk_generation_now",
        "allows_patch_envelope_generation_now",
        "allows_repair_execution_now",
    ):
        assert getattr(contract, name) is False
        with pytest.raises(ValueError):
            build_repair_proposal_evidence_contract(**{name: True})


def test_bundle_validation_report_preview_and_no_generation_guarantee():
    bundle = create_repair_proposal_evidence_bundle(build_repair_proposal_evidence_input())
    assert repair_proposal_evidence_bundle_is_not_proposal(bundle)
    assert bundle.source_read_performed is False
    assert bundle.proposal_generated is False
    assert bundle.diff_generated is False
    assert bundle.hunk_generated is False
    assert bundle.patch_envelope_generated is False
    assert bundle.repair_executed is False
    assert bundle.production_certified is False
    assert bundle.ready_for_execution is False
    validation = validate_repair_proposal_evidence_bundle(bundle)
    assert validation.evidence_contract_confirmed
    assert validation.evidence_gaps_confirmed
    assert validation.do_nothing_evidence_confirmed
    assert validation.no_source_read_confirmed
    assert validation.no_proposal_generation_confirmed
    assert validation.no_diff_generation_confirmed
    assert validation.no_hunk_generation_confirmed
    assert validation.no_patch_envelope_generation_confirmed
    assert validation.no_repair_execution_confirmed
    report = build_repair_proposal_evidence_report(bundle=bundle, validation_report=validation)
    assert report.ready_for_execution is False
    assert report.production_certified is False
    preview = build_repair_proposal_evidence_run_preview()
    assert preview.would_create_contract
    assert preview.would_read_source is False
    assert preview.would_generate_proposal is False
    guarantee = build_repair_proposal_evidence_no_generation_guarantee()
    for field in fields(RepairProposalEvidenceNoGenerationGuarantee):
        if field.name.startswith("no_"):
            assert getattr(guarantee, field.name) is True


@pytest.mark.parametrize(
    "field_name",
    [
        "source_read_performed",
        "proposal_generated",
        "diff_generated",
        "hunk_generated",
        "patch_envelope_generated",
        "repair_executed",
        "production_certified",
        "ready_for_execution",
    ],
)
def test_bundle_rejects_runtime_or_generation_state(field_name):
    with pytest.raises(ValueError):
        build_repair_proposal_evidence_bundle(**{field_name: True})


def test_v0381_readiness_report_preserves_unsafe_false():
    report = build_v0381_readiness_report()
    assert report.repair_proposal_evidence_layer_constructed
    assert report.ready_for_v0382_read_only_sandbox_source_context
    assert report.ready_for_v0383_repair_scope_planner_change_intent
    assert report.ready_for_v0384_proposed_diff_code_hunk_metadata
    assert report.ready_for_repair_proposal_evidence_contract
    assert report.ready_for_repair_proposal_evidence_bundle
    assert report.ready_for_repair_proposal_evidence_assessment
    assert report.ready_for_repair_proposal_eligibility_decision
    assert report.ready_for_repair_proposal_evidence_gap_register
    assert report.ready_for_repair_proposal_do_nothing_evidence
    assert report.ready_for_future_read_only_sandbox_source_context_input
    assert report.ready_for_future_repair_scope_planning_input
    assert report.ready_for_future_change_intent_input
    assert report.ready_for_future_proposed_diff_metadata_input
    assert report.ready_for_future_proposed_code_hunk_metadata_input
    assert v0381_readiness_report_is_not_execution_ready(report)
    for name in _unsafe_flag_names(V0381ReadinessReport) + ["production_certified"]:
        assert getattr(report, name) is False
        with pytest.raises(ValueError):
            build_v0381_readiness_report(**{name: True})


def test_helpers_do_not_contain_runtime_execution_patterns():
    import chanta_core.agent_runtime.repair_proposal_evidence as module

    source = inspect.getsource(module)
    forbidden = [
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "Path.read_text",
        "Path.read_bytes",
        "Path.write_text",
        "Path.write_bytes",
        "open(",
        "import requests",
        "import httpx",
        "import urllib",
        "import aiohttp",
        "import socket",
        "eval(",
        "exec(",
        "apply_patch(",
    ]
    for pattern in forbidden:
        assert pattern not in source
