from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.memory_candidate_continuity import (
    MEMORY_CANDIDATE_EXTRACTION_EFFECT_TYPES,
    MEMORY_CANDIDATE_EXTRACTION_EVENT_TYPES,
    MEMORY_CANDIDATE_EXTRACTION_FORBIDDEN_EFFECT_TYPES,
    MEMORY_CANDIDATE_EXTRACTION_OBJECT_TYPES,
    MEMORY_CANDIDATE_EXTRACTION_REQUIRED_RULES,
    MEMORY_CANDIDATE_TYPES,
    MemoryCandidate,
    MemoryCandidateBatch,
    MemoryCandidateContext,
    MemoryCandidateExtractionAuditTrail,
    MemoryCandidateExtractionDecision,
    MemoryCandidateExtractionFinding,
    MemoryCandidateExtractionPolicy,
    MemoryCandidateExtractionReport,
    MemoryCandidateExtractionReportService,
    MemoryCandidateExtractionRequest,
    MemoryCandidateExtractionRule,
    MemoryCandidateExtractionSkipRecord,
    MemoryCandidateExtractionDeferredRecord,
    MemoryCandidateExtractionBlockedRecord,
    MemoryCandidateExtractionSourceView,
    MemoryCandidatePIGSignal,
    MemoryCandidateProvenance,
    MemoryCandidateRedactionView,
    MemoryCandidateRiskFlag,
    MemoryCandidateSourceLink,
    MemoryCandidateClaim,
    MemoryCandidateTypeClassifier,
    MemoryCandidateExtractionRecordService,
)


def _parts() -> dict:
    return MemoryCandidateExtractionReportService().build_all_parts()


def test_memory_candidate_extraction_models_build() -> None:
    parts = _parts()
    candidate = parts["candidates"][0]
    record_service = MemoryCandidateExtractionRecordService()
    sample_ref = candidate.source_refs[0]

    assert isinstance(parts["extraction_policy"], MemoryCandidateExtractionPolicy)
    assert isinstance(parts["request"], MemoryCandidateExtractionRequest)
    assert isinstance(parts["source_view"], MemoryCandidateExtractionSourceView)
    assert isinstance(parts["extraction_rules"][0], MemoryCandidateExtractionRule)
    assert isinstance(parts["type_classifier"], MemoryCandidateTypeClassifier)
    assert isinstance(parts["candidate_batch"], MemoryCandidateBatch)
    assert isinstance(candidate, MemoryCandidate)
    assert isinstance(candidate.source_links[0], MemoryCandidateSourceLink)
    assert isinstance(candidate.candidate_claims[0], MemoryCandidateClaim)
    assert isinstance(candidate.context, MemoryCandidateContext)
    assert isinstance(candidate.provenance, MemoryCandidateProvenance)
    assert isinstance(candidate.pig_signals[0], MemoryCandidatePIGSignal)
    assert isinstance(candidate.risk_flags[0], MemoryCandidateRiskFlag)
    assert isinstance(candidate.redaction_view, MemoryCandidateRedactionView)
    assert isinstance(parts["decisions"][0], MemoryCandidateExtractionDecision)
    assert isinstance(record_service.build_skip_record(sample_ref), MemoryCandidateExtractionSkipRecord)
    assert isinstance(record_service.build_deferred_record(sample_ref), MemoryCandidateExtractionDeferredRecord)
    assert isinstance(record_service.build_blocked_record(sample_ref), MemoryCandidateExtractionBlockedRecord)
    assert isinstance(parts["audit_trail"], MemoryCandidateExtractionAuditTrail)
    assert isinstance(parts["findings"][0], MemoryCandidateExtractionFinding)
    assert isinstance(parts["report"], MemoryCandidateExtractionReport)


def test_policy_source_view_rules_and_classifier() -> None:
    parts = _parts()
    policy = parts["extraction_policy"]
    source_view = parts["source_view"]
    rules = parts["extraction_rules"]
    classifier = parts["type_classifier"]
    rule_names = {rule.rule_name for rule in rules}

    assert policy.version == "v0.27.2"
    assert policy.layer == "memory_candidate_continuity"
    assert policy.extraction_enabled is True
    assert policy.extraction_from_eligible_sources_only is True
    assert policy.candidate_is_not_memory is True
    assert policy.source_refs_required is True
    assert policy.evidence_refs_required is True
    assert policy.provenance_required is True
    assert policy.risk_flags_required is True
    assert policy.redaction_required is True
    assert policy.candidate_type_required is True
    assert policy.candidate_context_required is True
    assert policy.pig_guidance_refs_allowed is True
    assert policy.pig_guidance_is_not_memory is True
    assert policy.raw_transcript_source_forbidden is True
    assert policy.raw_provider_output_source_forbidden is True
    assert policy.raw_secret_source_forbidden is True
    assert policy.credential_source_forbidden is True
    assert policy.private_full_path_source_forbidden is True
    assert policy.scoring_enabled_now is False
    assert policy.promotion_enabled_now is False
    assert policy.persistent_memory_write_enabled_now is False
    assert policy.durable_memory_write_enabled_now is False
    assert policy.session_continuity_injection_enabled_now is False
    assert policy.persona_mutation_enabled_now is False
    assert policy.behavior_policy_mutation_enabled_now is False
    assert policy.provider_invocation_enabled_now is False
    assert policy.command_execution_enabled_now is False
    assert policy.safety_bypass_enabled_now is False
    assert policy.llm_judge_as_sole_authority_forbidden is True
    assert source_view.source_boundary_report_ref is not None
    assert source_view.candidate_readiness_boundary_ref is not None
    assert source_view.eligible_source_count == len(source_view.eligible_source_refs)
    assert source_view.deferred_source_count == len(source_view.deferred_source_refs)
    assert source_view.blocked_source_count == len(source_view.blocked_source_refs)
    assert source_view.raw_transcript_included is False
    assert source_view.raw_provider_output_included is False
    assert source_view.raw_secret_included is False
    assert source_view.credential_included is False
    assert source_view.private_full_path_included is False
    assert set(MEMORY_CANDIDATE_EXTRACTION_REQUIRED_RULES).issubset(rule_names)
    assert set(MEMORY_CANDIDATE_TYPES).issubset(set(classifier.supported_candidate_types))
    assert classifier.classification_method in {"deterministic_rules", "source_category_mapping", "explicit_source_metadata", "mixed_deterministic"}
    assert classifier.llm_judge_used is False


def test_candidates_are_candidate_only_and_refs_only() -> None:
    parts = _parts()
    batch = parts["candidate_batch"]
    candidates = parts["candidates"]

    assert batch.candidate_count == len(candidates)
    assert batch.skipped_count == len(parts["skipped_records"])
    assert batch.deferred_count == len(parts["deferred_records"])
    assert batch.blocked_count == len(parts["blocked_records"])
    assert batch.memory_promoted is False
    assert batch.persistent_memory_written is False
    assert candidates

    for candidate in candidates:
        assert candidate.candidate_type in MEMORY_CANDIDATE_TYPES
        assert candidate.title
        assert candidate.summary
        assert candidate.candidate_status == "candidate_only"
        assert candidate.promotion_status == "candidate_only"
        assert candidate.source_refs
        assert candidate.evidence_refs
        assert isinstance(candidate.created_from_workbench_refs, bool)
        assert candidate.created_from_raw_transcript is False
        assert candidate.created_from_raw_provider_output is False
        assert candidate.raw_content_included is False
        assert candidate.raw_secret_included is False
        assert candidate.score_created is False
        assert candidate.promoted_to_memory is False
        assert candidate.persistent_memory_written is False
        assert candidate.persona_mutation is False
        assert candidate.behavior_policy_mutation is False
        assert candidate.source_links
        assert candidate.source_links[0].raw_content_linked is False
        assert candidate.source_links[0].source_support_role in {"primary", "supporting", "context", "contradiction_warning", "risk_signal", "pig_guidance", "unknown"}
        assert candidate.candidate_claims
        assert candidate.candidate_claims[0].sanitized is True
        assert candidate.candidate_claims[0].asserted_as_truth is False
        assert candidate.candidate_claims[0].score_created is False
        assert candidate.candidate_claims[0].support_status in {"ref_supported", "weakly_supported", "missing_support", "blocked"}
        assert candidate.context.context_is_not_injection is True
        assert candidate.context.continuity_context_created is False
        assert candidate.provenance.originating_versions
        assert candidate.provenance.originating_surfaces
        assert candidate.provenance.source_ref_ids
        assert candidate.provenance.extraction_rule_ids
        assert candidate.provenance.extraction_request_id
        assert candidate.pig_signals
        assert candidate.pig_signals[0].pig_guidance_is_memory is False
        assert candidate.pig_signals[0].pig_guidance_promotes_memory is False
        assert candidate.pig_signals[0].pig_guidance_mutates_policy is False
        assert candidate.pig_signals[0].pig_guidance_executes is False
        assert candidate.risk_flags
        assert candidate.risk_flags[0].risk_type
        assert candidate.risk_flags[0].risk_level in {"none", "low", "medium", "high", "blocked", "unknown"}
        assert isinstance(candidate.risk_flags[0].blocks_future_promotion, bool)
        assert isinstance(candidate.risk_flags[0].requires_more_evidence, bool)
        assert isinstance(candidate.risk_flags[0].requires_user_confirmation, bool)
        assert candidate.redaction_view is not None
        assert candidate.redaction_view.raw_content_included is False
        assert candidate.redaction_view.raw_secret_included is False


def test_report_pig_ocpx_ocel_and_cli(capsys) -> None:
    service = MemoryCandidateExtractionReportService()
    parts = _parts()
    report = parts["report"]
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert report.report_status in {"passed", "warning"}
    assert report.ready_for_v0_27_3 is True
    assert report.ready_for_v0_28 is False
    assert report.extraction_policy_created is True
    assert report.extraction_source_view_created is True
    assert report.extraction_rules_created is True
    assert report.type_classifier_created is True
    assert report.candidate_batch_created is True
    assert report.memory_candidates_created is True
    assert report.candidate_source_links_created is True
    assert report.candidate_claims_created is True
    assert report.candidate_contexts_created is True
    assert report.candidate_provenance_created is True
    assert report.candidate_pig_signals_created is True
    assert report.candidate_risk_flags_created is True
    assert report.candidate_redaction_views_created is True
    assert report.extraction_decisions_created is True
    assert report.extraction_audit_trail_created is True
    assert report.memory_candidate_count == len(parts["candidates"])
    assert report.memory_scored is False
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.durable_memory_written is False
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
    assert report.next_required_step == "v0.27.3 Memory Evidence Binder & Scoring"
    assert "memory_candidate" in MEMORY_CANDIDATE_EXTRACTION_OBJECT_TYPES
    assert "memory_candidate_created" in MEMORY_CANDIDATE_EXTRACTION_EVENT_TYPES
    assert "memory_candidate_created" in MEMORY_CANDIDATE_EXTRACTION_EFFECT_TYPES
    assert "memory_candidate_scored" in MEMORY_CANDIDATE_EXTRACTION_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.27.2"
    assert pig["subject"] == "memory_candidate_extraction"
    assert pig["safety_boundary"]["memory_scored"] is False
    assert ocpx["state"] == "memory_candidate_extraction_created"
    assert "MemoryCandidateExtractionState" in ocpx["target_read_models"]
    assert "MemoryCandidateState" in ocpx["target_read_models"]

    assert main(["memory", "candidates", "extract"]) == 0
    output = capsys.readouterr().out
    assert "version=v0.27.2" in output
    assert "layer=memory_candidate_continuity" in output
    assert "extraction_policy_created=true" in output
    assert "extraction_source_view_created=true" in output
    assert "candidate_batch_created=true" in output
    assert "memory_candidates_created=true" in output
    assert "ready_for_v0_27_3=true" in output
    assert "ready_for_v0_28=false" in output
    assert "memory_scored=false" in output
    assert "memory_promoted=false" in output
    assert "persistent_memory_written=false" in output
    assert "durable_memory_written=false" in output
    assert "session_continuity_injected=false" in output
    assert "persona_mutated=false" in output
    assert "behavior_policy_mutated=false" in output
    assert "raw_transcript_memory_created=false" in output
    assert "raw_provider_output_memory_created=false" in output
    assert "pig_memory_promoted=false" in output
    assert "pig_policy_mutated=false" in output
    assert "pig_executed=false" in output
    assert "provider_invoked=false" in output
    assert "command_executed=false" in output
    assert "safety_gate_bypassed=false" in output
    assert "external_provider_adapter_implemented=false" in output
    assert "schumpeter_split_introduced=false" in output
    assert "raw_secret_output=false" in output
    assert "credential_exposed=false" in output
    assert "llm_judge_used=false" in output
