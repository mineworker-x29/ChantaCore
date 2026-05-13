"""Skill package exports.

Imports are resolved lazily so canonical OCEL modules can import
``chanta_core.skills.skill`` without pulling in runtime dispatch dependencies.
"""

from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = [
    "Skill",
    "SkillExecutionContext",
    "SkillExecutionResult",
    "SkillExecutionPolicy",
    "SkillExecutor",
    "SkillRegistryError",
    "SkillValidationError",
    "SkillRegistry",
    "ExplicitSkillInvocationRequest",
    "ExplicitSkillInvocationInput",
    "ExplicitSkillInvocationDecision",
    "ExplicitSkillInvocationResult",
    "ExplicitSkillInvocationViolation",
    "ExplicitSkillInvocationService",
    "SkillProposalIntent",
    "SkillProposalRequirement",
    "SkillInvocationProposal",
    "SkillProposalDecision",
    "SkillProposalReviewNote",
    "SkillProposalResult",
    "SkillProposalRouterService",
    "SkillProposalReviewContract",
    "SkillProposalReviewRequest",
    "SkillProposalReviewDecision",
    "SkillProposalReviewFinding",
    "SkillProposalReviewResult",
    "SkillProposalReviewService",
    "ReviewedExecutionBridgeRequest",
    "ReviewedExecutionBridgeDecision",
    "ReviewedExecutionBridgeResult",
    "ReviewedExecutionBridgeViolation",
    "ReviewedExecutionBridgeService",
    "ReadOnlyExecutionGatePolicy",
    "SkillExecutionGateRequest",
    "SkillExecutionGateDecision",
    "SkillExecutionGateFinding",
    "SkillExecutionGateResult",
    "SkillExecutionGateService",
    "InternalSkillDescriptor",
    "InternalSkillInputContract",
    "InternalSkillOutputContract",
    "InternalSkillRiskProfile",
    "InternalSkillGateContract",
    "InternalSkillObservabilityContract",
    "InternalSkillOnboardingReview",
    "InternalSkillOnboardingFinding",
    "InternalSkillOnboardingResult",
    "InternalSkillOnboardingService",
    "SkillRegistryView",
    "SkillRegistryEntry",
    "SkillRegistryFilter",
    "SkillRegistryFinding",
    "SkillRegistryResult",
    "SkillRegistryViewService",
    "ObservationDigestProposalPolicy",
    "ObservationDigestIntentCandidate",
    "ObservationDigestProposalBinding",
    "ObservationDigestProposalSet",
    "ObservationDigestProposalFinding",
    "ObservationDigestProposalResult",
    "ObservationDigestProposalService",
    "ObservationDigestSkillRuntimeBinding",
    "ObservationDigestInvocationPolicy",
    "ObservationDigestInvocationFinding",
    "ObservationDigestInvocationResult",
    "ObservationDigestSkillInvocationService",
    "ObservationDigestConformancePolicy",
    "ObservationDigestConformanceCheck",
    "ObservationDigestSmokeCase",
    "ObservationDigestSmokeResult",
    "ObservationDigestConformanceFinding",
    "ObservationDigestConformanceReport",
    "ObservationDigestConformanceService",
    "explicit_skill_invocation_requests_to_history_entries",
    "explicit_skill_invocation_results_to_history_entries",
    "explicit_skill_invocation_violations_to_history_entries",
    "skill_proposal_intents_to_history_entries",
    "skill_invocation_proposals_to_history_entries",
    "skill_proposal_results_to_history_entries",
    "skill_proposal_review_notes_to_history_entries",
    "skill_proposal_review_requests_to_history_entries",
    "skill_proposal_review_decisions_to_history_entries",
    "skill_proposal_review_results_to_history_entries",
    "skill_proposal_review_findings_to_history_entries",
    "reviewed_execution_bridge_requests_to_history_entries",
    "reviewed_execution_bridge_decisions_to_history_entries",
    "reviewed_execution_bridge_results_to_history_entries",
    "reviewed_execution_bridge_violations_to_history_entries",
    "skill_execution_gate_decisions_to_history_entries",
    "skill_execution_gate_results_to_history_entries",
    "skill_execution_gate_findings_to_history_entries",
    "internal_skill_descriptors_to_history_entries",
    "internal_skill_onboarding_results_to_history_entries",
    "internal_skill_onboarding_findings_to_history_entries",
    "internal_skill_observability_contracts_to_history_entries",
    "skill_registry_views_to_history_entries",
    "skill_registry_entries_to_history_entries",
    "skill_registry_results_to_history_entries",
    "skill_registry_findings_to_history_entries",
    "observation_digest_intents_to_history_entries",
    "observation_digest_proposal_sets_to_history_entries",
    "observation_digest_proposal_results_to_history_entries",
    "observation_digest_proposal_findings_to_history_entries",
    "observation_digest_runtime_bindings_to_history_entries",
    "observation_digest_invocation_results_to_history_entries",
    "observation_digest_invocation_findings_to_history_entries",
    "observation_digest_conformance_checks_to_history_entries",
    "observation_digest_smoke_results_to_history_entries",
    "observation_digest_conformance_findings_to_history_entries",
    "observation_digest_conformance_reports_to_history_entries",
    "external_skill_resource_inventories_to_history_entries",
    "external_skill_manifest_profiles_to_history_entries",
    "external_skill_instruction_profiles_to_history_entries",
    "external_skill_declared_capabilities_to_history_entries",
    "external_skill_static_risk_profiles_to_history_entries",
    "external_skill_static_digestion_reports_to_history_entries",
    "external_skill_static_digestion_findings_to_history_entries",
    "agent_instances_to_history_entries",
    "agent_runtime_descriptors_to_history_entries",
    "environment_snapshots_to_history_entries",
    "movement_ontology_terms_to_history_entries",
    "normalized_events_v2_to_history_entries",
    "observed_objects_to_history_entries",
    "observed_relations_to_history_entries",
    "behavior_inferences_v2_to_history_entries",
    "observation_reviews_to_history_entries",
    "observation_corrections_to_history_entries",
    "redaction_policies_to_history_entries",
    "export_policies_to_history_entries",
    "fleet_snapshots_to_history_entries",
    "observation_spine_findings_to_history_entries",
    "observation_spine_results_to_history_entries",
    "builtin_llm_chat_skill",
    "create_agent_behavior_infer_skill",
    "create_agent_observation_normalize_skill",
    "create_agent_observation_source_inspect_skill",
    "create_agent_process_narrative_skill",
    "create_agent_trace_observe_skill",
    "create_check_self_conformance_skill",
    "create_echo_skill",
    "create_external_behavior_fingerprint_skill",
    "create_external_skill_adapter_candidate_skill",
    "create_external_skill_assimilate_skill",
    "create_external_skill_source_inspect_skill",
    "create_external_skill_static_digest_skill",
    "create_ingest_human_pi_skill",
    "create_inspect_ocel_recent_skill",
    "create_llm_chat_skill",
    "create_summarize_pi_artifacts_skill",
    "create_summarize_process_trace_skill",
    "create_summarize_text_skill",
]


def __getattr__(name: str) -> Any:
    if name == "Skill":
        return import_module("chanta_core.skills.skill").Skill
    if name == "SkillExecutionContext":
        return import_module("chanta_core.skills.context").SkillExecutionContext
    if name == "SkillExecutionResult":
        return import_module("chanta_core.skills.result").SkillExecutionResult
    if name == "SkillExecutionPolicy":
        return import_module("chanta_core.skills.executor").SkillExecutionPolicy
    if name == "SkillExecutor":
        return import_module("chanta_core.skills.executor").SkillExecutor
    if name in {"SkillRegistryError", "SkillValidationError"}:
        errors = import_module("chanta_core.skills.errors")
        return getattr(errors, name)
    if name == "SkillRegistry":
        return import_module("chanta_core.skills.registry").SkillRegistry
    if name in {
        "ExplicitSkillInvocationRequest",
        "ExplicitSkillInvocationInput",
        "ExplicitSkillInvocationDecision",
        "ExplicitSkillInvocationResult",
        "ExplicitSkillInvocationViolation",
        "ExplicitSkillInvocationService",
    }:
        invocation = import_module("chanta_core.skills.invocation")
        return getattr(invocation, name)
    if name in {
        "SkillProposalIntent",
        "SkillProposalRequirement",
        "SkillInvocationProposal",
        "SkillProposalDecision",
        "SkillProposalReviewNote",
        "SkillProposalResult",
        "SkillProposalRouterService",
    }:
        proposal = import_module("chanta_core.skills.proposal")
        return getattr(proposal, name)
    if name in {
        "SkillProposalReviewContract",
        "SkillProposalReviewRequest",
        "SkillProposalReviewDecision",
        "SkillProposalReviewFinding",
        "SkillProposalReviewResult",
        "SkillProposalReviewService",
    }:
        proposal_review = import_module("chanta_core.skills.proposal_review")
        return getattr(proposal_review, name)
    if name in {
        "ReviewedExecutionBridgeRequest",
        "ReviewedExecutionBridgeDecision",
        "ReviewedExecutionBridgeResult",
        "ReviewedExecutionBridgeViolation",
        "ReviewedExecutionBridgeService",
    }:
        bridge = import_module("chanta_core.skills.reviewed_execution_bridge")
        return getattr(bridge, name)
    if name in {
        "ReadOnlyExecutionGatePolicy",
        "SkillExecutionGateRequest",
        "SkillExecutionGateDecision",
        "SkillExecutionGateFinding",
        "SkillExecutionGateResult",
        "SkillExecutionGateService",
    }:
        execution_gate = import_module("chanta_core.skills.execution_gate")
        return getattr(execution_gate, name)
    if name in {
        "InternalSkillDescriptor",
        "InternalSkillInputContract",
        "InternalSkillOutputContract",
        "InternalSkillRiskProfile",
        "InternalSkillGateContract",
        "InternalSkillObservabilityContract",
        "InternalSkillOnboardingReview",
        "InternalSkillOnboardingFinding",
        "InternalSkillOnboardingResult",
        "InternalSkillOnboardingService",
    }:
        onboarding = import_module("chanta_core.skills.onboarding")
        return getattr(onboarding, name)
    if name in {
        "SkillRegistryView",
        "SkillRegistryEntry",
        "SkillRegistryFilter",
        "SkillRegistryFinding",
        "SkillRegistryResult",
        "SkillRegistryViewService",
    }:
        registry_view = import_module("chanta_core.skills.registry_view")
        return getattr(registry_view, name)
    if name in {
        "ObservationDigestProposalPolicy",
        "ObservationDigestIntentCandidate",
        "ObservationDigestProposalBinding",
        "ObservationDigestProposalSet",
        "ObservationDigestProposalFinding",
        "ObservationDigestProposalResult",
        "ObservationDigestProposalService",
    }:
        observation_digest_proposal = import_module("chanta_core.skills.observation_digest_proposal")
        return getattr(observation_digest_proposal, name)
    if name in {
        "ObservationDigestSkillRuntimeBinding",
        "ObservationDigestInvocationPolicy",
        "ObservationDigestInvocationFinding",
        "ObservationDigestInvocationResult",
        "ObservationDigestSkillInvocationService",
    }:
        observation_digest_invocation = import_module("chanta_core.skills.observation_digest_invocation")
        return getattr(observation_digest_invocation, name)
    if name in {
        "ObservationDigestConformancePolicy",
        "ObservationDigestConformanceCheck",
        "ObservationDigestSmokeCase",
        "ObservationDigestSmokeResult",
        "ObservationDigestConformanceFinding",
        "ObservationDigestConformanceReport",
        "ObservationDigestConformanceService",
    }:
        observation_digest_conformance = import_module("chanta_core.skills.observation_digest_conformance")
        return getattr(observation_digest_conformance, name)
    if name in {
        "explicit_skill_invocation_requests_to_history_entries",
        "explicit_skill_invocation_results_to_history_entries",
        "explicit_skill_invocation_violations_to_history_entries",
        "skill_proposal_intents_to_history_entries",
        "skill_invocation_proposals_to_history_entries",
        "skill_proposal_results_to_history_entries",
        "skill_proposal_review_notes_to_history_entries",
        "skill_proposal_review_requests_to_history_entries",
        "skill_proposal_review_decisions_to_history_entries",
        "skill_proposal_review_results_to_history_entries",
        "skill_proposal_review_findings_to_history_entries",
        "reviewed_execution_bridge_requests_to_history_entries",
        "reviewed_execution_bridge_decisions_to_history_entries",
        "reviewed_execution_bridge_results_to_history_entries",
        "reviewed_execution_bridge_violations_to_history_entries",
        "skill_execution_gate_decisions_to_history_entries",
        "skill_execution_gate_results_to_history_entries",
        "skill_execution_gate_findings_to_history_entries",
        "internal_skill_descriptors_to_history_entries",
        "internal_skill_onboarding_results_to_history_entries",
        "internal_skill_onboarding_findings_to_history_entries",
        "internal_skill_observability_contracts_to_history_entries",
        "skill_registry_views_to_history_entries",
        "skill_registry_entries_to_history_entries",
        "skill_registry_results_to_history_entries",
        "skill_registry_findings_to_history_entries",
        "observation_digest_intents_to_history_entries",
        "observation_digest_proposal_sets_to_history_entries",
        "observation_digest_proposal_results_to_history_entries",
        "observation_digest_proposal_findings_to_history_entries",
        "observation_digest_runtime_bindings_to_history_entries",
        "observation_digest_invocation_results_to_history_entries",
        "observation_digest_invocation_findings_to_history_entries",
        "observation_digest_conformance_checks_to_history_entries",
        "observation_digest_smoke_results_to_history_entries",
        "observation_digest_conformance_findings_to_history_entries",
        "observation_digest_conformance_reports_to_history_entries",
        "external_skill_resource_inventories_to_history_entries",
        "external_skill_manifest_profiles_to_history_entries",
        "external_skill_instruction_profiles_to_history_entries",
        "external_skill_declared_capabilities_to_history_entries",
        "external_skill_static_risk_profiles_to_history_entries",
        "external_skill_static_digestion_reports_to_history_entries",
        "external_skill_static_digestion_findings_to_history_entries",
        "agent_instances_to_history_entries",
        "agent_runtime_descriptors_to_history_entries",
        "environment_snapshots_to_history_entries",
        "movement_ontology_terms_to_history_entries",
        "normalized_events_v2_to_history_entries",
        "observed_objects_to_history_entries",
        "observed_relations_to_history_entries",
        "behavior_inferences_v2_to_history_entries",
        "observation_reviews_to_history_entries",
        "observation_corrections_to_history_entries",
        "redaction_policies_to_history_entries",
        "export_policies_to_history_entries",
        "fleet_snapshots_to_history_entries",
        "observation_spine_findings_to_history_entries",
        "observation_spine_results_to_history_entries",
    }:
        history_adapter = import_module("chanta_core.skills.history_adapter")
        return getattr(history_adapter, name)
    if name in {
        "builtin_llm_chat_skill",
        "create_agent_behavior_infer_skill",
        "create_agent_observation_normalize_skill",
        "create_agent_observation_source_inspect_skill",
        "create_agent_process_narrative_skill",
        "create_agent_trace_observe_skill",
        "create_check_self_conformance_skill",
        "create_echo_skill",
        "create_external_behavior_fingerprint_skill",
        "create_external_skill_adapter_candidate_skill",
        "create_external_skill_assimilate_skill",
        "create_external_skill_source_inspect_skill",
        "create_external_skill_static_digest_skill",
        "create_ingest_human_pi_skill",
        "create_inspect_ocel_recent_skill",
        "create_llm_chat_skill",
        "create_summarize_pi_artifacts_skill",
        "create_summarize_process_trace_skill",
        "create_summarize_text_skill",
    }:
        builtin = import_module("chanta_core.skills.builtin")
        return getattr(builtin, name)
    raise AttributeError(name)
