from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.memory_candidate_continuity import (
    MEMORY_SOURCE_ALLOWED_CATEGORIES,
    MEMORY_SOURCE_EFFECT_TYPES,
    MEMORY_SOURCE_EVENT_TYPES,
    MEMORY_SOURCE_FORBIDDEN_CATEGORIES,
    MEMORY_SOURCE_FORBIDDEN_EFFECT_TYPES,
    MEMORY_SOURCE_OBJECT_TYPES,
    MEMORY_SOURCE_REQUIRED_ELIGIBILITY_RULES,
    MemoryCandidateReadinessBoundary,
    MemoryForbiddenSourceReport,
    MemorySourceBoundaryFinding,
    MemorySourceBoundaryPolicyView,
    MemorySourceBoundaryReport,
    MemorySourceBoundaryReportService,
    MemorySourceBoundaryRequest,
    MemorySourceCategoryCatalog,
    MemorySourceEligibilityDecision,
    MemorySourceEligibilityEvaluation,
    MemorySourceEligibilityRule,
    MemorySourceQualityPolicy,
    MemorySourceQualityReport,
    MemorySourceQualitySignal,
    MemorySourceRedactionPolicy,
    MemorySourceRedactionReport,
    MemorySourceRedactionView,
    MemorySourceRef,
    MemorySourceRefBundle,
    MemorySourceRefRegistryView,
    MemorySourceRiskFlag,
)


def _parts() -> dict:
    return MemorySourceBoundaryReportService().build_all_parts()


def test_memory_source_boundary_models_build() -> None:
    parts = _parts()

    assert isinstance(parts["boundary_policy_view"], MemorySourceBoundaryPolicyView)
    assert isinstance(parts["request"], MemorySourceBoundaryRequest)
    assert isinstance(parts["category_catalog"], MemorySourceCategoryCatalog)
    assert isinstance(parts["source_refs"][0], MemorySourceRef)
    assert isinstance(parts["source_bundle"], MemorySourceRefBundle)
    assert isinstance(parts["source_registry_view"], MemorySourceRefRegistryView)
    assert isinstance(parts["eligibility_rules"][0], MemorySourceEligibilityRule)
    assert isinstance(parts["eligibility_evaluations"][0], MemorySourceEligibilityEvaluation)
    assert isinstance(parts["eligibility_decisions"][0], MemorySourceEligibilityDecision)
    assert isinstance(parts["redaction_policy"], MemorySourceRedactionPolicy)
    assert isinstance(parts["redaction_views"][0], MemorySourceRedactionView)
    assert isinstance(parts["redaction_report"], MemorySourceRedactionReport)
    assert isinstance(parts["quality_policy"], MemorySourceQualityPolicy)
    assert isinstance(parts["quality_signals"][0], MemorySourceQualitySignal)
    assert isinstance(parts["quality_report"], MemorySourceQualityReport)
    assert isinstance(parts["risk_flags"][0], MemorySourceRiskFlag)
    assert isinstance(parts["forbidden_source_report"], MemoryForbiddenSourceReport)
    assert isinstance(parts["candidate_readiness_boundary"], MemoryCandidateReadinessBoundary)
    assert isinstance(parts["findings"][0], MemorySourceBoundaryFinding)
    assert isinstance(parts["report"], MemorySourceBoundaryReport)


def test_policy_view_catalog_and_source_refs_are_refs_only() -> None:
    parts = _parts()
    policy = parts["boundary_policy_view"]
    catalog = parts["category_catalog"]
    source_refs = parts["source_refs"]

    assert policy.version == "v0.27.1"
    assert policy.refs_only_source_required is True
    assert policy.raw_transcript_default_source_forbidden is True
    assert policy.raw_provider_output_source_forbidden is True
    assert policy.raw_secret_source_forbidden is True
    assert policy.credential_source_forbidden is True
    assert policy.private_full_path_source_forbidden is True
    assert policy.unredacted_file_content_source_forbidden is True
    assert policy.redaction_required is True
    assert policy.source_quality_required is True
    assert policy.candidate_extraction_enabled_now is False
    assert policy.memory_scoring_enabled_now is False
    assert policy.memory_promotion_enabled_now is False
    assert policy.persistent_memory_write_enabled_now is False
    assert set(MEMORY_SOURCE_ALLOWED_CATEGORIES).issubset(set(catalog.allowed_source_categories))
    assert set(MEMORY_SOURCE_FORBIDDEN_CATEGORIES).issubset(set(catalog.forbidden_source_categories))
    for source in source_refs:
        assert source.source_category in catalog.allowed_source_categories
        assert source.source_kind
        assert source.source_ref
        assert source.source_summary
        assert source.originating_version is not None
        assert source.originating_surface is not None
        assert source.evidence_refs
        assert source.refs_only is True
        assert source.raw_content_included is False
        assert source.raw_transcript_included is False
        assert source.raw_provider_output_included is False
        assert source.raw_secret_included is False
        assert source.credential_included is False
        assert source.private_full_path_included is False
        assert source.memory_candidate_created is False


def test_bundle_registry_eligibility_redaction_quality_and_readiness() -> None:
    parts = _parts()
    bundle = parts["source_bundle"]
    registry = parts["source_registry_view"]
    rules = parts["eligibility_rules"]
    evaluations = parts["eligibility_evaluations"]
    decisions = parts["eligibility_decisions"]
    redaction_policy = parts["redaction_policy"]
    redaction_report = parts["redaction_report"]
    quality_policy = parts["quality_policy"]
    quality_report = parts["quality_report"]
    forbidden = parts["forbidden_source_report"]
    readiness = parts["candidate_readiness_boundary"]
    rule_names = {rule.rule_name for rule in rules}
    signal_types = {signal.signal_type for signal in parts["quality_signals"]}

    assert bundle.source_count == len(parts["source_refs"])
    assert bundle.eligible_count == len(parts["source_refs"])
    assert bundle.memory_candidate_created is False
    assert bundle.memory_promoted is False
    assert bundle.persistent_memory_written is False
    assert registry.registry_is_not_durable_memory is True
    assert registry.durable_memory_written is False
    assert set(MEMORY_SOURCE_REQUIRED_ELIGIBILITY_RULES).issubset(rule_names)
    assert all(evaluation.evaluation_status == "passed" for evaluation in evaluations)
    assert all(evaluation.memory_candidate_created is False for evaluation in evaluations)
    assert all(decision.decision_type == "eligible_for_candidate_extraction" for decision in decisions)
    assert all(decision.candidate_extraction_performed_now is False for decision in decisions)
    assert all(decision.memory_created_now is False for decision in decisions)
    assert redaction_policy.redact_raw_transcript is True
    assert redaction_policy.redact_raw_provider_output is True
    assert redaction_policy.redact_raw_secret is True
    assert redaction_policy.redact_credentials is True
    assert redaction_policy.redact_private_full_path is True
    assert redaction_policy.preserve_refs is True
    assert redaction_policy.preserve_sanitized_summary is True
    assert redaction_policy.redaction_is_not_source_deletion is True
    assert all(view.source_deleted is False for view in parts["redaction_views"])
    assert redaction_report.source_data_deleted is False
    assert quality_policy.source_quality_required is True
    assert quality_policy.event_quality_required is True
    assert quality_policy.trace_coverage_preferred is True
    assert quality_policy.evidence_density_required is True
    assert {"event_quality", "trace_coverage", "evidence_density", "provenance_strength", "redaction_status", "recency", "stability", "privacy_risk", "contradiction_warning", "release_hygiene_status"}.issubset(signal_types)
    assert quality_report.candidate_extraction_performed_now is False
    assert quality_report.candidate_extraction_ready_count == bundle.eligible_count
    assert forbidden.report_status == "ready"
    assert forbidden.raw_transcript_detected is False
    assert forbidden.raw_provider_output_detected is False
    assert forbidden.raw_secret_detected is False
    assert forbidden.credential_detected is False
    assert forbidden.private_full_path_detected is False
    assert readiness.candidate_extraction_ready is True
    assert readiness.candidate_extraction_ready_count == bundle.eligible_count
    assert readiness.candidate_extraction_not_performed_now is True
    assert readiness.memory_created_now is False
    assert readiness.next_required_step == "v0.27.2 Memory Candidate Extraction"


def test_report_forbidden_flags_ocel_pig_ocpx_and_cli(capsys) -> None:
    service = MemorySourceBoundaryReportService()
    parts = _parts()
    report = parts["report"]
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert report.report_status == "warning"
    assert report.ready_for_v0_27_2 is True
    assert report.ready_for_v0_28 is False
    assert report.source_boundary_created is True
    assert report.source_refs_created is True
    assert report.source_bundle_created is True
    assert report.eligibility_evaluations_created is True
    assert report.eligibility_decisions_created is True
    assert report.redaction_report_created is True
    assert report.source_quality_report_created is True
    assert report.forbidden_source_report_created is True
    assert report.candidate_readiness_boundary_created is True
    assert report.memory_candidate_extracted is False
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
    assert report.next_required_step == "v0.27.2 Memory Candidate Extraction"
    assert "memory_source_ref" in MEMORY_SOURCE_OBJECT_TYPES
    assert "memory_source_boundary_report_created" in MEMORY_SOURCE_EVENT_TYPES
    assert "memory_source_boundary_created" in MEMORY_SOURCE_EFFECT_TYPES
    assert "memory_candidate_created" in MEMORY_SOURCE_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.27.1"
    assert pig["subject"] == "memory_source_ref_boundary"
    assert pig["safety_boundary"]["memory_candidate_extracted"] is False
    assert ocpx["state"] == "memory_source_ref_boundary_created"
    assert "MemorySourceBoundaryState" in ocpx["target_read_models"]
    assert "MemoryCandidateReadinessBoundaryState" in ocpx["target_read_models"]

    assert main(["memory", "sources", "boundary"]) == 0
    output = capsys.readouterr().out
    assert "version=v0.27.1" in output
    assert "layer=memory_candidate_continuity" in output
    assert "source_boundary_created=true" in output
    assert "source_refs_created=true" in output
    assert "source_bundle_created=true" in output
    assert "ready_for_v0_27_2=true" in output
    assert "ready_for_v0_28=false" in output
    assert "memory_candidate_extracted=false" in output
    assert "memory_scored=false" in output
    assert "memory_promoted=false" in output
    assert "persistent_memory_written=false" in output
    assert "durable_memory_written=false" in output
    assert "session_continuity_injected=false" in output
    assert "persona_mutated=false" in output
    assert "behavior_policy_mutated=false" in output
    assert "provider_invoked=false" in output
    assert "command_executed=false" in output
    assert "safety_gate_bypassed=false" in output
    assert "next_required_step=v0.27.2 Memory Candidate Extraction" in output
