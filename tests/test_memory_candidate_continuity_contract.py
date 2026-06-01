from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.memory_candidate_continuity import (
    MEMORY_ALLOWED_SOURCE_CATEGORIES,
    MEMORY_CANDIDATE_TYPES,
    MEMORY_CONTRACT_EFFECT_TYPES,
    MEMORY_CONTRACT_EVENT_TYPES,
    MEMORY_CONTRACT_FORBIDDEN_EFFECT_TYPES,
    MEMORY_CONTRACT_OBJECT_TYPES,
    MEMORY_CONTRACT_RELATION_TYPES,
    MEMORY_CONTRACT_VERSION,
    MEMORY_SCORE_DIMENSIONS,
    ContinuityInjectionPolicy,
    DurableMemoryPolicy,
    MemoryAuditPolicy,
    MemoryCandidateContinuityContract,
    MemoryCandidatePolicy,
    MemoryCandidateTypeCatalog,
    MemoryContractFinding,
    MemoryContractReport,
    MemoryContractReportService,
    MemoryEvidencePolicy,
    MemoryGovernancePolicy,
    MemoryPIGGuidancePolicy,
    MemoryPrivacyPolicy,
    MemoryPromotionGatePolicy,
    MemoryReleasePrerequisitePolicy,
    MemorySafetyBoundaryPolicy,
    MemoryScoringPolicy,
    MemorySourceBoundaryPolicy,
    MemorySourceEligibilityPolicy,
    MemoryTrackRoadmap,
    MemoryTrackVersionPlan,
    SessionContinuityPolicy,
)


def _parts() -> dict:
    return MemoryContractReportService().build_all_parts()


def test_memory_contract_models_build() -> None:
    parts = _parts()

    assert isinstance(parts["contract"], MemoryCandidateContinuityContract)
    assert isinstance(parts["roadmap"], MemoryTrackRoadmap)
    assert isinstance(parts["roadmap"].versions[0], MemoryTrackVersionPlan)
    assert isinstance(parts["source_boundary_policy"], MemorySourceBoundaryPolicy)
    assert isinstance(parts["source_eligibility_policy"], MemorySourceEligibilityPolicy)
    assert isinstance(parts["candidate_policy"], MemoryCandidatePolicy)
    assert isinstance(parts["candidate_type_catalog"], MemoryCandidateTypeCatalog)
    assert isinstance(parts["evidence_policy"], MemoryEvidencePolicy)
    assert isinstance(parts["scoring_policy"], MemoryScoringPolicy)
    assert isinstance(parts["promotion_gate_policy"], MemoryPromotionGatePolicy)
    assert isinstance(parts["durable_memory_policy"], DurableMemoryPolicy)
    assert isinstance(parts["session_continuity_policy"], SessionContinuityPolicy)
    assert isinstance(parts["continuity_injection_policy"], ContinuityInjectionPolicy)
    assert isinstance(parts["audit_policy"], MemoryAuditPolicy)
    assert isinstance(parts["privacy_policy"], MemoryPrivacyPolicy)
    assert isinstance(parts["governance_policy"], MemoryGovernancePolicy)
    assert isinstance(parts["pig_guidance_policy"], MemoryPIGGuidancePolicy)
    assert isinstance(parts["safety_boundary_policy"], MemorySafetyBoundaryPolicy)
    assert isinstance(parts["release_prerequisite_policy"], MemoryReleasePrerequisitePolicy)
    assert isinstance(parts["findings"][0], MemoryContractFinding)
    assert isinstance(parts["report"], MemoryContractReport)


def test_contract_identity_roadmap_and_prerequisite() -> None:
    parts = _parts()
    contract = parts["contract"]
    roadmap = parts["roadmap"]
    version_numbers = [plan.version_number for plan in roadmap.versions]

    assert MEMORY_CONTRACT_VERSION == "v0.27.0"
    assert contract.version == "v0.27.0"
    assert contract.layer == "memory_candidate_continuity"
    assert contract.track == "Memory Candidate & Continuity"
    assert contract.status == "contract_only"
    assert contract.previous_release_ref is not None
    assert contract.previous_release_ref["version"] == "v0.26.9"
    assert contract.recommended_prerequisite_ref is not None
    assert contract.recommended_prerequisite_ref["version"] == "v0.26.10"
    assert version_numbers == [f"v0.27.{index}" for index in range(10)]
    assert roadmap.next_version == "v0.27.1 Memory Source / Ref Boundary"
    assert roadmap.consolidation_version == "v0.27.9 Memory Candidate & Continuity Consolidation"
    assert any(not plan.persistent_memory_write_allowed for plan in roadmap.versions if plan.version_number == "v0.27.0")
    assert any(plan.persistent_memory_write_allowed for plan in roadmap.versions if plan.version_number == "v0.27.5")
    assert all(plan.persona_mutation_allowed is False for plan in roadmap.versions)
    assert all(plan.external_adapter_allowed is False for plan in roadmap.versions)


def test_source_boundary_candidate_evidence_and_scoring_policies() -> None:
    parts = _parts()
    source = parts["source_boundary_policy"]
    eligibility = parts["source_eligibility_policy"]
    candidate = parts["candidate_policy"]
    catalog = parts["candidate_type_catalog"]
    evidence = parts["evidence_policy"]
    scoring = parts["scoring_policy"]

    assert set(MEMORY_ALLOWED_SOURCE_CATEGORIES).issubset(set(source.allowed_source_categories))
    assert source.refs_only_source_required is True
    assert source.raw_transcript_default_source_forbidden is True
    assert source.raw_provider_output_source_forbidden is True
    assert source.raw_secret_source_forbidden is True
    assert source.credential_source_forbidden is True
    assert source.private_full_path_source_forbidden is True
    assert source.unredacted_file_content_source_forbidden is True
    assert source.source_quality_required is True
    assert source.redaction_required is True
    assert eligibility.source_without_ref_blocked is True
    assert eligibility.raw_content_source_blocked is True
    assert candidate.memory_candidate_enabled_future is True
    assert candidate.memory_candidate_extraction_deferred_to == "v0.27.2"
    assert candidate.candidate_is_not_memory is True
    assert candidate.candidate_requires_source_refs is True
    assert candidate.candidate_requires_evidence_refs is True
    assert candidate.candidate_requires_type is True
    assert candidate.candidate_requires_risk_flags is True
    assert candidate.candidate_requires_promotion_status_candidate_only is True
    assert candidate.raw_transcript_candidate_forbidden_by_default is True
    assert candidate.automatic_promotion_forbidden is True
    assert set(MEMORY_CANDIDATE_TYPES).issubset(set(catalog.candidate_types))
    assert evidence.evidence_binding_deferred_to == "v0.27.3"
    assert evidence.evidence_bundle_required_for_scoring is True
    assert evidence.source_refs_required is True
    assert evidence.pig_guidance_refs_allowed is True
    assert evidence.event_quality_refs_allowed is True
    assert evidence.trace_coverage_refs_allowed is True
    assert evidence.raw_provider_output_evidence_forbidden is True
    assert evidence.raw_transcript_evidence_forbidden_by_default is True
    assert evidence.raw_secret_evidence_forbidden is True
    assert scoring.scoring_deferred_to == "v0.27.3"
    assert scoring.score_is_not_promotion is True
    assert scoring.high_score_is_not_automatic_memory is True
    assert set(MEMORY_SCORE_DIMENSIONS).issubset(set(scoring.required_score_dimensions))
    assert scoring.pig_guidance_may_inform_score is True
    assert scoring.pig_guidance_cannot_promote_memory is True
    assert scoring.llm_judge_cannot_be_sole_scoring_authority is True


def test_promotion_durable_continuity_injection_audit_privacy_governance() -> None:
    parts = _parts()
    promotion = parts["promotion_gate_policy"]
    durable = parts["durable_memory_policy"]
    continuity = parts["session_continuity_policy"]
    injection = parts["continuity_injection_policy"]
    audit = parts["audit_policy"]
    privacy = parts["privacy_policy"]
    governance = parts["governance_policy"]

    assert promotion.promotion_gate_deferred_to == "v0.27.4"
    assert promotion.promotion_is_not_persona_mutation is True
    assert promotion.automatic_promotion_forbidden is True
    assert promotion.promotion_requires_source_refs is True
    assert promotion.promotion_requires_evidence_bundle is True
    assert promotion.promotion_requires_score is True
    assert promotion.promotion_requires_privacy_risk_assessment is True
    assert promotion.promotion_requires_scope is True
    assert promotion.promotion_requires_lifecycle_policy is True
    assert promotion.promotion_requires_audit_trail is True
    assert promotion.promotion_requires_forget_revoke_path is True
    assert promotion.promotion_without_gate_blocked is True
    assert durable.durable_memory_registry_deferred_to == "v0.27.5"
    assert durable.persistent_memory_write_forbidden_in_v0270 is True
    assert durable.persistent_memory_write_allowed_future_only_after_promotion is True
    assert durable.durable_memory_requires_provenance is True
    assert durable.durable_memory_requires_scope is True
    assert durable.durable_memory_requires_evidence_index is True
    assert durable.durable_memory_requires_lifecycle_policy is True
    assert durable.durable_memory_must_be_revocable is True
    assert durable.durable_memory_must_be_forgettable is True
    assert durable.durable_memory_does_not_mutate_persona_by_default is True
    assert continuity.session_continuity_context_deferred_to == "v0.27.6"
    assert continuity.session_continuity_is_not_raw_transcript_replay is True
    assert continuity.raw_transcript_replay_forbidden is True
    assert continuity.unbounded_context_stuffing_forbidden is True
    assert continuity.stale_memory_warning_required is True
    assert continuity.contradiction_surface_required is True
    assert injection.continuity_injection_deferred_to == "v0.27.7"
    assert injection.injection_is_guidance_not_override is True
    assert injection.explicit_user_instruction_outranks_memory is True
    assert injection.safety_gate_must_remain_active is True
    assert injection.permission_boundary_must_remain_active is True
    assert injection.injection_must_be_previewable is True
    assert injection.injection_requires_boundary_trace is True
    assert injection.injection_must_not_invoke_provider is True
    assert injection.injection_must_not_execute_command is True
    assert injection.injection_must_not_mutate_persona is True
    assert audit.audit_lifecycle_deferred_to == "v0.27.8"
    assert audit.audit_required_for_promotion is True
    assert audit.audit_required_for_update is True
    assert audit.audit_required_for_revoke is True
    assert audit.audit_required_for_forget is True
    assert audit.silent_memory_overwrite_forbidden is True
    assert audit.unlogged_memory_deletion_forbidden is True
    assert privacy.privacy_check_required is True
    assert privacy.sensitive_memory_requires_stricter_gate is True
    assert privacy.raw_secret_memory_forbidden is True
    assert privacy.credential_memory_forbidden is True
    assert privacy.private_full_path_memory_forbidden is True
    assert privacy.personal_sensitive_attribute_memory_blocked_by_default is True
    assert governance.v02610_hardening_recommended_before_persistent_write is True
    assert governance.clean_repo_recommended_before_durable_memory is True
    assert governance.runtime_data_hygiene_required_before_memory_registry is True


def test_pig_safety_report_ocel_ocpx_and_cli(capsys) -> None:
    service = MemoryContractReportService()
    parts = _parts()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()
    safety = parts["safety_boundary_policy"]
    report = parts["report"]

    assert parts["pig_guidance_policy"].pig_guidance_is_not_memory is True
    assert parts["pig_guidance_policy"].pig_guidance_cannot_promote_memory is True
    assert parts["pig_guidance_policy"].pig_guidance_cannot_mutate_persona is True
    assert parts["pig_guidance_policy"].pig_guidance_cannot_mutate_behavior_policy is True
    assert parts["pig_guidance_policy"].pig_guidance_cannot_execute is True
    assert safety.memory_candidate_extraction_enabled_now is False
    assert safety.memory_scoring_enabled_now is False
    assert safety.memory_promotion_enabled_now is False
    assert safety.persistent_memory_write_enabled_now is False
    assert safety.session_continuity_injection_enabled_now is False
    assert safety.persona_mutation_forbidden is True
    assert safety.behavior_policy_auto_mutation_forbidden is True
    assert safety.raw_transcript_memory_forbidden is True
    assert safety.raw_provider_output_memory_forbidden is True
    assert safety.memory_without_evidence_forbidden is True
    assert safety.memory_without_source_refs_forbidden is True
    assert safety.memory_without_promotion_gate_forbidden is True
    assert safety.memory_triggered_provider_invocation_forbidden is True
    assert safety.memory_triggered_command_execution_forbidden is True
    assert safety.memory_triggered_safety_bypass_forbidden is True
    assert report.report_status == "warning"
    assert report.ready_for_v0_27_1 is True
    assert report.ready_for_v0_28 is False
    assert report.contract_created is True
    assert report.roadmap_created is True
    assert report.source_boundary_policy_created is True
    assert report.candidate_policy_created is True
    assert report.evidence_policy_created is True
    assert report.scoring_policy_created is True
    assert report.promotion_gate_policy_created is True
    assert report.durable_memory_policy_created is True
    assert report.session_continuity_policy_created is True
    assert report.continuity_injection_policy_created is True
    assert report.audit_policy_created is True
    assert report.privacy_policy_created is True
    assert report.governance_policy_created is True
    assert report.pig_guidance_policy_created is True
    assert report.safety_boundary_policy_created is True
    assert "memory_candidate_continuity_contract" in MEMORY_CONTRACT_OBJECT_TYPES
    assert "memory_contract_report_created" in MEMORY_CONTRACT_EVENT_TYPES
    assert "declares_memory_candidate_continuity_contract" in MEMORY_CONTRACT_RELATION_TYPES
    assert "memory_contract_declared" in MEMORY_CONTRACT_EFFECT_TYPES
    assert "memory_candidate_created" in MEMORY_CONTRACT_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.27.0"
    assert pig["subject"] == "memory_candidate_continuity_contract"
    assert pig["safety_boundary"]["memory_candidate_extracted"] is False
    assert ocpx["state"] == "memory_candidate_continuity_contract_declared"
    assert "MemoryCandidateContinuityContractState" in ocpx["target_read_models"]
    assert "V027ReadinessState" in ocpx["target_read_models"]

    assert main(["memory", "contract"]) == 0
    output = capsys.readouterr().out
    assert "version=v0.27.0" in output
    assert "layer=memory_candidate_continuity" in output
    assert "status=contract_only" in output
    assert "ready_for_v0_27_1=true" in output
    assert "ready_for_v0_28=false" in output
    assert "memory_candidate_extracted=false" in output
    assert "memory_scored=false" in output
    assert "memory_promoted=false" in output
    assert "persistent_memory_written=false" in output
    assert "persona_mutated=false" in output
    assert "behavior_policy_mutated=false" in output
    assert "raw_transcript_memory_created=false" in output
    assert "raw_provider_output_memory_created=false" in output
    assert "pig_memory_promoted=false" in output
    assert "provider_invoked=false" in output
    assert "command_executed=false" in output
    assert "safety_gate_bypassed=false" in output
    assert "next_required_step=v0.27.1 Memory Source / Ref Boundary" in output
