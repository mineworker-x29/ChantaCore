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
    "ReadOnlyExecutionGatePolicy",
    "SkillExecutionGateRequest",
    "SkillExecutionGateDecision",
    "SkillExecutionGateFinding",
    "SkillExecutionGateResult",
    "SkillExecutionGateService",
    "explicit_skill_invocation_requests_to_history_entries",
    "explicit_skill_invocation_results_to_history_entries",
    "explicit_skill_invocation_violations_to_history_entries",
    "skill_proposal_intents_to_history_entries",
    "skill_invocation_proposals_to_history_entries",
    "skill_proposal_results_to_history_entries",
    "skill_proposal_review_notes_to_history_entries",
    "skill_execution_gate_decisions_to_history_entries",
    "skill_execution_gate_results_to_history_entries",
    "skill_execution_gate_findings_to_history_entries",
    "builtin_llm_chat_skill",
    "create_check_self_conformance_skill",
    "create_echo_skill",
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
        "explicit_skill_invocation_requests_to_history_entries",
        "explicit_skill_invocation_results_to_history_entries",
        "explicit_skill_invocation_violations_to_history_entries",
        "skill_proposal_intents_to_history_entries",
        "skill_invocation_proposals_to_history_entries",
        "skill_proposal_results_to_history_entries",
        "skill_proposal_review_notes_to_history_entries",
        "skill_execution_gate_decisions_to_history_entries",
        "skill_execution_gate_results_to_history_entries",
        "skill_execution_gate_findings_to_history_entries",
    }:
        history_adapter = import_module("chanta_core.skills.history_adapter")
        return getattr(history_adapter, name)
    if name in {
        "builtin_llm_chat_skill",
        "create_check_self_conformance_skill",
        "create_echo_skill",
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
