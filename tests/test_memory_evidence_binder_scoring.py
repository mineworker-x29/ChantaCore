from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.memory_candidate_continuity import (
    MEMORY_EVIDENCE_BINDING_REQUIRED_RULES,
    MEMORY_EVIDENCE_SCORING_EFFECT_TYPES,
    MEMORY_EVIDENCE_SCORING_EVENT_TYPES,
    MEMORY_EVIDENCE_SCORING_FORBIDDEN_EFFECT_TYPES,
    MEMORY_EVIDENCE_SCORING_OBJECT_TYPES,
    MEMORY_SCORE_DIMENSIONS,
    MemoryCandidateEvidenceBundle,
    MemoryCandidateScore,
    MemoryCandidateScoreBreakdown,
    MemoryCandidateScoringBatch,
    MemoryCandidateScoringDecision,
    MemoryClaimSupportAssessment,
    MemoryContradictionCheck,
    MemoryEvidenceBindingRule,
    MemoryEvidenceItem,
    MemoryEvidenceScoringAuditTrail,
    MemoryEvidenceScoringFinding,
    MemoryEvidenceScoringPolicy,
    MemoryEvidenceScoringReport,
    MemoryEvidenceScoringReportService,
    MemoryEvidenceScoringRequest,
    MemoryEvidenceScoringSourceView,
    MemoryEvidenceStrengthAssessment,
    MemoryEvidenceSupportLink,
    MemoryPIGScoringSignal,
    MemoryPrivacyRiskAssessment,
    MemoryPromotionReadinessPreview,
    MemoryRecencyAssessment,
    MemoryReuseValueAssessment,
    MemoryScoreDimensionValue,
    MemorySourceQualityAssessment,
    MemorySpecificityAssessment,
    MemoryStabilityAssessment,
    MemoryUserControlRequirementAssessment,
)


def _parts() -> dict:
    return MemoryEvidenceScoringReportService().build_all_parts()


def test_memory_evidence_scoring_models_build() -> None:
    parts = _parts()
    bundle = parts["evidence_bundles"][0]
    breakdown = parts["score_breakdowns"][0]

    assert isinstance(parts["evidence_scoring_policy"], MemoryEvidenceScoringPolicy)
    assert isinstance(parts["request"], MemoryEvidenceScoringRequest)
    assert isinstance(parts["source_view"], MemoryEvidenceScoringSourceView)
    assert isinstance(parts["binding_rules"][0], MemoryEvidenceBindingRule)
    assert isinstance(bundle, MemoryCandidateEvidenceBundle)
    assert isinstance(bundle.evidence_items[0], MemoryEvidenceItem)
    assert isinstance(bundle.support_links[0], MemoryEvidenceSupportLink)
    assert isinstance(bundle.claim_support_assessments[0], MemoryClaimSupportAssessment)
    assert isinstance(parts["evidence_strength_assessments"][0], MemoryEvidenceStrengthAssessment)
    assert isinstance(parts["source_quality_assessments"][0], MemorySourceQualityAssessment)
    assert isinstance(parts["recency_assessments"][0], MemoryRecencyAssessment)
    assert isinstance(parts["stability_assessments"][0], MemoryStabilityAssessment)
    assert isinstance(parts["reuse_value_assessments"][0], MemoryReuseValueAssessment)
    assert isinstance(parts["specificity_assessments"][0], MemorySpecificityAssessment)
    assert isinstance(parts["privacy_risk_assessments"][0], MemoryPrivacyRiskAssessment)
    assert isinstance(parts["contradiction_checks"][0], MemoryContradictionCheck)
    assert isinstance(parts["user_control_assessments"][0], MemoryUserControlRequirementAssessment)
    assert isinstance(parts["pig_scoring_signals"][0], MemoryPIGScoringSignal)
    assert isinstance(breakdown.dimension_values[0], MemoryScoreDimensionValue)
    assert isinstance(breakdown, MemoryCandidateScoreBreakdown)
    assert isinstance(parts["candidate_scores"][0], MemoryCandidateScore)
    assert isinstance(parts["scoring_decisions"][0], MemoryCandidateScoringDecision)
    assert isinstance(parts["scoring_batch"], MemoryCandidateScoringBatch)
    assert isinstance(parts["promotion_readiness_previews"][0], MemoryPromotionReadinessPreview)
    assert isinstance(parts["audit_trail"], MemoryEvidenceScoringAuditTrail)
    assert isinstance(parts["findings"][0], MemoryEvidenceScoringFinding)
    assert isinstance(parts["report"], MemoryEvidenceScoringReport)


def test_policy_source_view_rules_and_evidence_bundles() -> None:
    parts = _parts()
    policy = parts["evidence_scoring_policy"]
    source_view = parts["source_view"]
    rule_names = {rule.rule_name for rule in parts["binding_rules"]}
    bundle = parts["evidence_bundles"][0]

    assert policy.version == "v0.27.3"
    assert policy.layer == "memory_candidate_continuity"
    assert policy.evidence_binding_enabled is True
    assert policy.scoring_enabled is True
    assert policy.score_is_not_promotion is True
    assert policy.high_score_is_not_automatic_memory is True
    assert policy.promotion_deferred_to == "v0.27.4"
    assert policy.persistent_memory_write_enabled_now is False
    assert policy.durable_memory_write_enabled_now is False
    assert policy.durable_registry_update_enabled_now is False
    assert policy.session_continuity_injection_enabled_now is False
    assert policy.persona_mutation_enabled_now is False
    assert policy.behavior_policy_mutation_enabled_now is False
    assert policy.evidence_bundle_required is True
    assert policy.source_refs_required is True
    assert policy.candidate_refs_required is True
    assert policy.score_breakdown_required is True
    assert policy.contradiction_check_required is True
    assert policy.privacy_risk_assessment_required is True
    assert policy.user_control_requirement_required is True
    assert policy.pig_guidance_refs_allowed is True
    assert policy.pig_guidance_is_not_memory is True
    assert policy.pig_guidance_cannot_promote_memory is True
    assert policy.raw_transcript_evidence_forbidden is True
    assert policy.raw_provider_output_evidence_forbidden is True
    assert policy.raw_secret_evidence_forbidden is True
    assert policy.credential_evidence_forbidden is True
    assert policy.private_full_path_evidence_forbidden is True
    assert policy.llm_judge_as_sole_scoring_authority_forbidden is True
    assert policy.provider_invocation_enabled_now is False
    assert policy.command_execution_enabled_now is False
    assert policy.safety_bypass_enabled_now is False
    assert source_view.candidate_extraction_report_ref is not None
    assert source_view.candidate_batch_ref is not None
    assert source_view.candidate_count == len(source_view.candidate_refs)
    assert source_view.candidate_claim_refs
    assert source_view.candidate_source_link_refs
    assert source_view.candidate_pig_signal_refs
    assert source_view.raw_transcript_included is False
    assert source_view.raw_provider_output_included is False
    assert source_view.raw_secret_included is False
    assert source_view.credential_included is False
    assert source_view.private_full_path_included is False
    assert set(MEMORY_EVIDENCE_BINDING_REQUIRED_RULES).issubset(rule_names)
    assert bundle.evidence_count == len(bundle.evidence_items)
    assert bundle.support_link_count == len(bundle.support_links)
    assert bundle.raw_transcript_included is False
    assert bundle.raw_provider_output_included is False
    assert bundle.raw_secret_included is False
    assert all(item.sanitized for item in bundle.evidence_items)
    assert all(item.raw_content_included is False for item in bundle.evidence_items)
    assert bundle.claim_support_assessments[0].claim_asserted_as_truth is False


def test_assessments_scores_decisions_and_previews_are_non_promoting() -> None:
    parts = _parts()
    dimensions = {value.dimension for breakdown in parts["score_breakdowns"] for value in breakdown.dimension_values}
    score = parts["candidate_scores"][0]
    decision = parts["scoring_decisions"][0]
    batch = parts["scoring_batch"]
    preview = parts["promotion_readiness_previews"][0]

    assert set(MEMORY_SCORE_DIMENSIONS).issubset(dimensions)
    assert parts["evidence_strength_assessments"][0].strength_level in {"none", "weak", "moderate", "strong", "unknown"}
    assert parts["source_quality_assessments"][0].source_quality_level in {"low", "medium", "high", "blocked", "unknown"}
    assert parts["recency_assessments"][0].recency_level in {"stale", "aging", "current", "unknown"}
    assert parts["stability_assessments"][0].stability_level in {"unstable", "tentative", "stable", "unknown"}
    assert parts["reuse_value_assessments"][0].reuse_value_level in {"low", "medium", "high", "unknown"}
    assert parts["specificity_assessments"][0].specificity_level in {"vague", "moderate", "specific", "over_specific", "unknown"}
    assert parts["privacy_risk_assessments"][0].privacy_risk_level in {"none", "low", "medium", "high", "blocked", "unknown"}
    assert parts["contradiction_checks"][0].contradiction_level in {"none", "weak", "moderate", "strong", "unknown"}
    assert parts["contradiction_checks"][0].contradiction_detected is False
    assert parts["user_control_assessments"][0].requires_promotion_gate_review is True
    assert parts["pig_scoring_signals"][0].pig_guidance_is_memory is False
    assert parts["pig_scoring_signals"][0].pig_guidance_promotes_memory is False
    assert parts["pig_scoring_signals"][0].pig_guidance_mutates_policy is False
    assert parts["pig_scoring_signals"][0].pig_guidance_executes is False
    assert score.score_band in {"low", "medium", "high", "blocked", "unknown"}
    assert score.promotion_readiness in {"not_ready", "needs_more_evidence", "needs_user_confirmation", "ready_for_gate_review", "blocked", "unknown"}
    assert score.score_is_promotion is False
    assert score.high_score_auto_promotes is False
    assert score.persistent_memory_written is False
    assert score.durable_memory_record_created is False
    assert decision.decision_type in {"score_candidate", "defer_more_evidence", "defer_user_confirmation", "block_privacy", "block_contradiction", "block_raw_source", "skip_incomplete_candidate", "unknown"}
    assert decision.promotes_memory is False
    assert decision.writes_persistent_memory is False
    assert batch.scored_candidate_count == len(parts["candidate_scores"])
    assert batch.memory_promoted is False
    assert batch.persistent_memory_written is False
    assert preview.preview_is_not_promotion is True
    assert preview.promotion_performed_now is False


def test_report_ocel_pig_ocpx_and_cli(capsys) -> None:
    service = MemoryEvidenceScoringReportService()
    parts = _parts()
    report = parts["report"]
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert report.report_status in {"passed", "warning"}
    assert report.ready_for_v0_27_4 is True
    assert report.ready_for_v0_28 is False
    assert report.evidence_bundles_created is True
    assert report.candidate_scores_created is True
    assert report.scoring_batch_created is True
    assert report.promotion_readiness_previews_created is True
    assert report.memory_scored is True
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.durable_memory_written is False
    assert report.durable_registry_updated is False
    assert report.session_continuity_injected is False
    assert report.persona_mutated is False
    assert report.behavior_policy_mutated is False
    assert report.raw_transcript_memory_created is False
    assert report.raw_provider_output_memory_created is False
    assert report.pig_memory_promoted is False
    assert report.pig_policy_mutated is False
    assert report.pig_executed is False
    assert report.provider_invoked is False
    assert report.command_executed is False
    assert report.safety_gate_bypassed is False
    assert report.external_provider_adapter_implemented is False
    assert report.schumpeter_split_introduced is False
    assert report.raw_secret_output is False
    assert report.credential_exposed is False
    assert report.llm_judge_used is False
    assert report.next_required_step == "v0.27.4 Memory Promotion Gate"
    assert "memory_candidate_score" in MEMORY_EVIDENCE_SCORING_OBJECT_TYPES
    assert "memory_candidate_score_created" in MEMORY_EVIDENCE_SCORING_EVENT_TYPES
    assert "memory_candidate_scored" in MEMORY_EVIDENCE_SCORING_EFFECT_TYPES
    assert "memory_promoted" in MEMORY_EVIDENCE_SCORING_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.27.3"
    assert pig["subject"] == "memory_evidence_binder_scoring"
    assert pig["safety_boundary"]["memory_promoted"] is False
    assert ocpx["state"] == "memory_evidence_binder_scoring_created"
    assert "MemoryCandidateScoreState" in ocpx["target_read_models"]
    assert "MemoryPromotionReadinessPreviewState" in ocpx["target_read_models"]

    assert main(["memory", "scoring", "bind-evidence"]) == 0
    output = capsys.readouterr().out
    assert "version=v0.27.3" in output
    assert "evidence_bundles_created=true" in output
    assert "candidate_scores_created=true" in output
    assert "memory_scored=true" in output
    assert "ready_for_v0_27_4=true" in output
    assert "ready_for_v0_28=false" in output
    assert "memory_promoted=false" in output
    assert "persistent_memory_written=false" in output
    assert "durable_memory_written=false" in output
    assert "durable_registry_updated=false" in output
    assert "session_continuity_injected=false" in output
    assert "persona_mutated=false" in output
    assert "behavior_policy_mutated=false" in output
    assert "provider_invoked=false" in output
    assert "command_executed=false" in output
    assert "safety_gate_bypassed=false" in output
    assert "next_required_step=v0.27.4 Memory Promotion Gate" in output
