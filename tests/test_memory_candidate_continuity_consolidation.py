from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.memory_candidate_continuity import (
    MEMORY_CONSOLIDATION_EFFECT_TYPES,
    MEMORY_CONSOLIDATION_EVENT_TYPES,
    MEMORY_CONSOLIDATION_FORBIDDEN_EFFECT_TYPES,
    MEMORY_CONSOLIDATION_OBJECT_TYPES,
    ContinuityInjectionBoundaryConsolidationReport,
    DurableMemoryRegistryConsolidationReport,
    MemoryCandidateQualityConsolidationReport,
    MemoryCapabilityMap,
    MemoryCapabilityMapEntry,
    MemoryConsolidationFinding,
    MemoryConsolidationReport,
    MemoryConsolidationReportService,
    MemoryCoverageMatrix,
    MemoryCoverageMatrixRow,
    MemoryDefaultAgentReadinessReport,
    MemoryEvidenceScoringConsolidationReport,
    MemoryFoundationSnapshot,
    MemoryFoundationSubjectComponent,
    MemoryLifecycleBoundaryConsolidationReport,
    MemoryPrivacyBoundaryConsolidationReport,
    MemoryProcessIntelligenceFeedbackLoopReport,
    MemoryPromotionBoundaryConsolidationReport,
    MemoryPublicAlphaHandoffPacket,
    MemoryReleaseHygieneDependencyReport,
    MemoryReleaseManifest,
    MemorySafetyBoundaryConsolidationReport,
    MemorySourceBoundaryConsolidationReport,
    MemoryV028ReadinessReport,
    SessionContinuityBoundaryConsolidationReport,
)


def _parts() -> dict:
    return MemoryConsolidationReportService().build_all_parts()


def test_memory_consolidation_models_build() -> None:
    parts = _parts()

    assert isinstance(parts["foundation_snapshot"], MemoryFoundationSnapshot)
    assert isinstance(parts["foundation_snapshot"].subject_components[0], MemoryFoundationSubjectComponent)
    assert isinstance(parts["capability_map"], MemoryCapabilityMap)
    assert isinstance(parts["capability_map"].entries[0], MemoryCapabilityMapEntry)
    assert isinstance(parts["coverage_matrix"], MemoryCoverageMatrix)
    assert isinstance(parts["coverage_matrix"].rows[0], MemoryCoverageMatrixRow)
    assert isinstance(parts["safety_boundary_report"], MemorySafetyBoundaryConsolidationReport)
    assert isinstance(parts["privacy_boundary_report"], MemoryPrivacyBoundaryConsolidationReport)
    assert isinstance(parts["source_boundary_consolidation_report"], MemorySourceBoundaryConsolidationReport)
    assert isinstance(parts["candidate_quality_consolidation_report"], MemoryCandidateQualityConsolidationReport)
    assert isinstance(parts["evidence_scoring_consolidation_report"], MemoryEvidenceScoringConsolidationReport)
    assert isinstance(parts["promotion_boundary_consolidation_report"], MemoryPromotionBoundaryConsolidationReport)
    assert isinstance(parts["durable_registry_consolidation_report"], DurableMemoryRegistryConsolidationReport)
    assert isinstance(parts["session_continuity_consolidation_report"], SessionContinuityBoundaryConsolidationReport)
    assert isinstance(parts["injection_boundary_consolidation_report"], ContinuityInjectionBoundaryConsolidationReport)
    assert isinstance(parts["lifecycle_boundary_consolidation_report"], MemoryLifecycleBoundaryConsolidationReport)
    assert isinstance(parts["process_intelligence_feedback_loop_report"], MemoryProcessIntelligenceFeedbackLoopReport)
    assert isinstance(parts["default_agent_readiness_report"], MemoryDefaultAgentReadinessReport)
    assert isinstance(parts["release_hygiene_dependency_report"], MemoryReleaseHygieneDependencyReport)
    assert isinstance(parts["v028_readiness_report"], MemoryV028ReadinessReport)
    assert isinstance(parts["public_alpha_handoff_packet"], MemoryPublicAlphaHandoffPacket)
    assert isinstance(parts["release_manifest"], MemoryReleaseManifest)
    assert isinstance(parts["findings"][0], MemoryConsolidationFinding)
    assert isinstance(parts["report"], MemoryConsolidationReport)


def test_foundation_snapshot_subjects_and_readiness_are_separated() -> None:
    snapshot = _parts()["foundation_snapshot"]
    component_types = {item.component_type for item in snapshot.subject_components}

    assert snapshot.version == "v0.27.9"
    assert snapshot.release_name == "Memory Candidate & Continuity Foundation v1"
    assert snapshot.included_versions == [f"v0.27.{index}" for index in range(10)]
    assert snapshot.previous_foundation_ref and snapshot.previous_foundation_ref["version"] == "v0.26.9"
    assert snapshot.recommended_hardening_ref and snapshot.recommended_hardening_ref["version"] == "v0.26.10"
    assert {
        "contract",
        "source_boundary",
        "candidate_extraction",
        "evidence_scoring",
        "promotion_gate",
        "durable_registry",
        "session_continuity_context",
        "injection_boundary",
        "lifecycle_control",
        "consolidation",
    } <= component_types
    assert snapshot.architecture_ready is True
    assert snapshot.repository_release_ready is False
    assert snapshot.runtime_agent_maturity_ready is False
    assert snapshot.public_alpha_ready is False


def test_capability_map_and_coverage_matrix_represent_boundaries() -> None:
    parts = _parts()
    capability_map = parts["capability_map"]
    coverage = parts["coverage_matrix"]
    categories = {entry.capability_category for entry in capability_map.entries}

    assert "source_boundary" in categories
    assert "candidate_extraction" in categories
    assert "evidence_scoring" in categories
    assert "promotion_gate" in categories
    assert "durable_registry" in categories
    assert "continuity_context" in categories
    assert "injection_boundary" in categories
    assert "lifecycle_control" in categories
    assert capability_map.runtime_injection_capability_count == 0
    assert capability_map.persona_mutation_capability_count == 0
    assert capability_map.external_adapter_capability_count == 0
    assert capability_map.schumpeter_split_capability_count == 0
    assert all(entry.allowed_effect_types for entry in capability_map.entries)
    assert all(entry.forbidden_effect_types for entry in capability_map.entries)
    assert {row.version_introduced for row in coverage.rows} >= {f"v0.27.{index}" for index in range(9)}
    assert coverage.coverage_status == "complete"
    assert coverage.missing_required_coverage_count == 0
    assert all(row.has_model and row.has_service and row.has_docs for row in coverage.rows)
    assert all(row.has_ocel_mapping and row.has_pig_projection and row.has_ocpx_projection for row in coverage.rows)


def test_safety_privacy_and_stage_consolidation_counts_are_safe() -> None:
    parts = _parts()
    safety = parts["safety_boundary_report"]
    privacy = parts["privacy_boundary_report"]
    source = parts["source_boundary_consolidation_report"]
    candidate = parts["candidate_quality_consolidation_report"]
    scoring = parts["evidence_scoring_consolidation_report"]
    promotion = parts["promotion_boundary_consolidation_report"]
    registry = parts["durable_registry_consolidation_report"]
    continuity = parts["session_continuity_consolidation_report"]
    injection = parts["injection_boundary_consolidation_report"]
    lifecycle = parts["lifecycle_boundary_consolidation_report"]

    assert safety.status == "passed"
    dangerous_counts = [
        safety.runtime_injection_count,
        safety.default_agent_mutation_count,
        safety.decision_service_mutation_count,
        safety.skill_router_mutation_count,
        safety.safety_gate_mutation_count,
        safety.permission_policy_mutation_count,
        safety.persona_mutation_count,
        safety.behavior_policy_mutation_count,
        safety.provider_invocation_count,
        safety.command_execution_count,
        safety.file_mutation_count,
        safety.safety_bypass_count,
        safety.permission_bypass_count,
        safety.external_adapter_count,
        safety.schumpeter_split_count,
        safety.llm_judge_as_sole_authority_count,
        safety.raw_transcript_memory_count,
        safety.raw_provider_output_memory_count,
        safety.raw_secret_memory_count,
        safety.credential_memory_count,
        safety.source_data_deletion_count,
        safety.unlogged_deletion_count,
        safety.silent_overwrite_count,
        safety.pig_authority_violation_count,
    ]
    assert dangerous_counts == [0] * len(dangerous_counts)
    assert privacy.credential_exposure_count == 0
    assert privacy.raw_secret_output_count == 0
    assert privacy.private_path_exposure_count == 0
    assert source.raw_source_violation_count == 0
    assert candidate.raw_candidate_violation_count == 0
    assert candidate.candidate_count >= 1
    assert scoring.high_score_auto_promotion_count == 0
    assert scoring.score_as_promotion_violation_count == 0
    assert promotion.promotion_without_gate_count == 0
    assert promotion.promotion_as_write_violation_count == 0
    assert registry.write_without_gate_count == 0
    assert registry.write_without_hygiene_count == 0
    assert continuity.raw_replay_violation_count == 0
    assert continuity.runtime_injection_count == 0
    assert injection.runtime_injection_count == 0
    assert injection.default_agent_mutation_count == 0
    assert injection.decision_service_mutation_count == 0
    assert injection.skill_router_mutation_count == 0
    assert lifecycle.silent_overwrite_count == 0
    assert lifecycle.unlogged_deletion_count == 0
    assert lifecycle.source_data_deletion_count == 0
    assert lifecycle.tombstone_with_recallable_content_count == 0


def test_feedback_agent_hygiene_readiness_handoff_manifest_and_report() -> None:
    parts = _parts()
    feedback = parts["process_intelligence_feedback_loop_report"]
    agent = parts["default_agent_readiness_report"]
    hygiene = parts["release_hygiene_dependency_report"]
    readiness = parts["v028_readiness_report"]
    handoff = parts["public_alpha_handoff_packet"]
    manifest = parts["release_manifest"]
    report = parts["report"]

    assert feedback.ocel_memory_event_visibility_ready is True
    assert feedback.ocpx_memory_view_readiness_ready is True
    assert feedback.pig_guidance_memory_signal_ready is True
    assert feedback.memory_candidate_traceability_ready is True
    assert feedback.memory_scoring_traceability_ready is True
    assert feedback.memory_promotion_traceability_ready is True
    assert feedback.durable_registry_traceability_ready is True
    assert feedback.continuity_context_traceability_ready is True
    assert feedback.lifecycle_traceability_ready is True
    assert feedback.closed_loop_learning_implemented is False
    assert agent.memory_context_available is True
    assert agent.continuity_context_pack_available is True
    assert agent.injection_boundary_available is True
    assert agent.runtime_injection_implemented is False
    assert agent.default_agent_mutation_implemented is False
    assert agent.decision_service_memory_use_implemented is False
    assert agent.skill_router_memory_use_implemented is False
    assert agent.remaining_gaps
    assert hygiene.release_hygiene_status == "unknown"
    assert hygiene.repository_release_ready is False
    assert hygiene.can_claim_foundation_release is False
    assert hygiene.can_claim_public_alpha_ready is False
    assert readiness.target_track == "v0.28.x Public Alpha / Schumpeter Split Preparation"
    assert readiness.ready_for_v0_28 is False
    assert readiness.public_alpha_not_implemented_yet is True
    assert readiness.schumpeter_split_not_implemented_yet is True
    assert readiness.external_adapters_not_implemented_yet is True
    assert handoff.refs_only is True
    assert handoff.implementation_performed_now is False
    assert "public alpha packaging" in handoff.not_implemented_in_v0279
    assert "Schumpeter split" in handoff.not_implemented_in_v0279
    assert "external provider adapters" in handoff.not_implemented_in_v0279
    assert "runtime continuity injection" in handoff.not_implemented_in_v0279
    assert "autonomous memory-driven execution" in handoff.not_implemented_in_v0279
    assert manifest.release_version == "v0.27.9"
    assert manifest.release_name == "Memory Candidate & Continuity Foundation v1"
    assert manifest.included_versions == [f"v0.27.{index}" for index in range(10)]
    assert "Public Alpha Packaging" in manifest.excluded_capabilities
    assert "Schumpeter Split / Company Wrapper" in manifest.excluded_capabilities
    assert "External Provider Adapter" in manifest.excluded_capabilities
    assert "Runtime Continuity Injection" in manifest.excluded_capabilities
    assert "Default Agent Runtime Mutation" in manifest.excluded_capabilities
    assert "DecisionService Runtime Memory Mutation" in manifest.excluded_capabilities
    assert "Autonomous Memory-Driven Execution" in manifest.excluded_capabilities
    assert "Persona Mutation" in manifest.excluded_capabilities
    assert "Behavior Policy Auto-Mutation" in manifest.excluded_capabilities
    assert "Raw Transcript Replay" in manifest.excluded_capabilities
    assert "PIG as Memory Authority" in manifest.excluded_capabilities
    assert manifest.release_status == "releasable_with_warnings"
    assert report.readiness_status == "warning"
    assert report.release_status == "releasable_with_warnings"
    assert report.ready_for_v0_28 is False
    assert report.ready_for_v0_29 is False
    assert report.public_alpha_ready is False
    assert report.next_required_step == "v0.28.0 Public Alpha / Schumpeter Split Preparation Contract"


def test_ocel_pig_ocpx_and_cli_commands_work(capsys) -> None:
    service = MemoryConsolidationReportService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert "memory_foundation_snapshot" in MEMORY_CONSOLIDATION_OBJECT_TYPES
    assert "memory_release_manifest" in MEMORY_CONSOLIDATION_OBJECT_TYPES
    assert "memory_consolidation_report_created" in MEMORY_CONSOLIDATION_EVENT_TYPES
    assert "memory_foundation_snapshot_created" in MEMORY_CONSOLIDATION_EFFECT_TYPES
    assert "memory_candidate_created" in MEMORY_CONSOLIDATION_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.27.9"
    assert pig["subject"] == "memory_candidate_continuity_consolidation"
    assert pig["release_name"] == "Memory Candidate & Continuity Foundation v1"
    assert pig["safety_boundary"]["runtime_injection_performed"] is False
    assert pig["safety_boundary"]["pig_guidance_used_as_authority"] is False
    assert ocpx["state"] == "memory_candidate_continuity_foundation_v1_consolidated"
    assert "MemoryFoundationSnapshotState" in ocpx["target_read_models"]
    assert "MemoryPublicAlphaHandoffState" in ocpx["target_read_models"]

    commands = [
        ["memory", "consolidate"],
        ["memory", "release-manifest"],
        ["memory", "readiness", "--target", "v0.28"],
        ["memory", "coverage"],
        ["memory", "safety-boundary"],
        ["memory", "privacy-boundary"],
        ["memory", "source-boundary-summary"],
        ["memory", "candidate-quality"],
        ["memory", "scoring-summary"],
        ["memory", "promotion-summary"],
        ["memory", "registry-summary"],
        ["memory", "continuity-summary"],
        ["memory", "injection-boundary-summary"],
        ["memory", "lifecycle-summary"],
        ["memory", "pi-feedback"],
        ["memory", "default-agent-readiness"],
        ["memory", "release-hygiene"],
        ["memory", "handoff", "--target", "v0.28"],
        ["memory", "consolidation-report", "--report-id", "memory_consolidation_report:v0.27.9"],
    ]
    for command in commands:
        assert main(command) == 0
        output = capsys.readouterr().out
        assert "version=v0.27.9" in output
        assert "release_name=Memory Candidate & Continuity Foundation v1" in output
        assert "public_alpha_ready=false" in output
        assert "ready_for_v0_29=false" in output
        assert "runtime_injection_performed=false" in output
        assert "default_agent_context_mutated=false" in output
        assert "decision_service_mutated=false" in output
        assert "skill_router_mutated=false" in output
        assert "safety_gate_mutated=false" in output
        assert "permission_policy_mutated=false" in output
        assert "persona_mutated=false" in output
        assert "behavior_policy_mutated=false" in output
        assert "provider_invoked=false" in output
        assert "command_executed=false" in output
        assert "file_mutated=false" in output
        assert "safety_gate_bypassed=false" in output
        assert "permission_boundary_bypassed=false" in output
        assert "external_provider_adapter_implemented=false" in output
        assert "schumpeter_split_introduced=false" in output
        assert "raw_transcript_replayed=false" in output
        assert "raw_provider_output_replayed=false" in output
        assert "raw_secret_output=false" in output
        assert "credential_exposed=false" in output
        assert "pig_guidance_used_as_authority=false" in output
        assert "llm_judge_used=false" in output
        assert "next_required_step=v0.28.0 Public Alpha / Schumpeter Split Preparation Contract" in output
