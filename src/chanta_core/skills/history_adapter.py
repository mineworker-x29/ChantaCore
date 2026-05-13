from __future__ import annotations

from chanta_core.context.history import ContextHistoryEntry, new_context_history_entry_id
from chanta_core.skills.invocation import (
    ExplicitSkillInvocationRequest,
    ExplicitSkillInvocationResult,
    ExplicitSkillInvocationViolation,
)
from chanta_core.skills.execution_gate import (
    SkillExecutionGateDecision,
    SkillExecutionGateFinding,
    SkillExecutionGateResult,
)
from chanta_core.skills.proposal import (
    SkillInvocationProposal,
    SkillProposalIntent,
    SkillProposalResult,
    SkillProposalReviewNote,
)
from chanta_core.skills.proposal_review import (
    SkillProposalReviewDecision,
    SkillProposalReviewFinding,
    SkillProposalReviewRequest,
    SkillProposalReviewResult,
)
from chanta_core.skills.reviewed_execution_bridge import (
    ReviewedExecutionBridgeDecision,
    ReviewedExecutionBridgeRequest,
    ReviewedExecutionBridgeResult,
    ReviewedExecutionBridgeViolation,
)
from chanta_core.skills.onboarding import (
    InternalSkillDescriptor,
    InternalSkillObservabilityContract,
    InternalSkillOnboardingFinding,
    InternalSkillOnboardingResult,
)
from chanta_core.skills.registry_view import (
    SkillRegistryEntry,
    SkillRegistryFinding,
    SkillRegistryResult,
    SkillRegistryView,
)
from chanta_core.skills.observation_digest_proposal import (
    ObservationDigestIntentCandidate,
    ObservationDigestProposalFinding,
    ObservationDigestProposalResult,
    ObservationDigestProposalSet,
)
from chanta_core.skills.observation_digest_invocation import (
    ObservationDigestInvocationFinding,
    ObservationDigestInvocationResult,
    ObservationDigestSkillRuntimeBinding,
)
from chanta_core.skills.observation_digest_conformance import (
    ObservationDigestConformanceCheck,
    ObservationDigestConformanceFinding,
    ObservationDigestConformanceReport,
    ObservationDigestSmokeResult,
)
from chanta_core.digestion import (
    ExternalSkillDeclaredCapability,
    ExternalSkillInstructionProfile,
    ExternalSkillManifestProfile,
    ExternalSkillResourceInventory,
    ExternalSkillStaticDigestionFinding,
    ExternalSkillStaticDigestionReport,
    ExternalSkillStaticRiskProfile,
)
from chanta_core.observation import (
    AgentBehaviorInferenceV2,
    AgentFleetObservationSnapshot,
    AgentInstance,
    AgentMovementOntologyTerm,
    AgentObservationCorrection,
    AgentObservationNormalizedEventV2,
    AgentObservationReview,
    AgentObservationSpineFinding,
    AgentObservationSpineResult,
    AgentRuntimeDescriptor,
    ObservedAgentObject,
    ObservedAgentRelation,
    ObservationExportPolicy,
    ObservationRedactionPolicy,
    RuntimeEnvironmentSnapshot,
    CrossHarnessTraceAdapterPolicy,
    HarnessTraceAdapterContract,
    HarnessTraceAdapterCoverageReport,
    HarnessTraceAdapterFinding,
    HarnessTraceAdapterResult,
    HarnessTraceMappingRule,
    HarnessTraceNormalizationResult,
    HarnessTraceSourceInspection,
)


def explicit_skill_invocation_requests_to_history_entries(
    requests: list[ExplicitSkillInvocationRequest],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=request.session_id,
            process_instance_id=request.process_instance_id,
            role="context",
            content=f"Explicit Skill Invocation requested: {request.skill_id}",
            created_at=request.created_at,
            source="explicit_skill_invocation",
            priority=45,
            refs=[
                {"ref_type": "explicit_skill_invocation_request", "ref_id": request.request_id}
            ],
            entry_attrs={
                "skill_id": request.skill_id,
                "invocation_mode": request.invocation_mode,
                "status": request.status,
            },
        )
        for request in requests
    ]


def explicit_skill_invocation_results_to_history_entries(
    results: list[ExplicitSkillInvocationResult],
) -> list[ContextHistoryEntry]:
    priority_by_status = {
        "completed": 60,
        "denied": 85,
        "unsupported": 85,
        "failed": 85,
        "error": 85,
        "skipped": 35,
    }
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Explicit Skill Invocation result: {result.skill_id}; "
                f"status={result.status}; violations={len(result.violation_ids)}."
            ),
            created_at=result.completed_at,
            source="explicit_skill_invocation",
            priority=priority_by_status.get(result.status, 50),
            refs=[
                {"ref_type": "explicit_skill_invocation_result", "ref_id": result.result_id},
                {"ref_type": "explicit_skill_invocation_request", "ref_id": result.request_id},
            ],
            entry_attrs={
                "skill_id": result.skill_id,
                "status": result.status,
                "violation_count": len(result.violation_ids),
            },
        )
        for result in results
    ]


def explicit_skill_invocation_violations_to_history_entries(
    violations: list[ExplicitSkillInvocationViolation],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Explicit Skill Invocation violation: {violation.violation_type}; "
                f"{violation.message}"
            ),
            created_at=violation.created_at,
            source="explicit_skill_invocation",
            priority=90,
            refs=[
                {"ref_type": "explicit_skill_invocation_violation", "ref_id": violation.violation_id}
            ],
            entry_attrs={
                "skill_id": violation.skill_id,
                "violation_type": violation.violation_type,
                "severity": violation.severity,
            },
        )
        for violation in violations
    ]


def skill_proposal_intents_to_history_entries(
    intents: list[SkillProposalIntent],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=intent.session_id,
            process_instance_id=None,
            role="context",
            content=(
                f"Skill Proposal intent: operation={intent.requested_operation}; "
                f"prompt_preview={intent.user_prompt_preview}"
            ),
            created_at=intent.created_at,
            source="skill_proposal",
            priority=45,
            refs=[{"ref_type": "skill_proposal_intent", "ref_id": intent.intent_id}],
            entry_attrs={
                "requested_operation": intent.requested_operation,
                "proposal_only": True,
            },
        )
        for intent in intents
    ]


def skill_invocation_proposals_to_history_entries(
    proposals: list[SkillInvocationProposal],
) -> list[ContextHistoryEntry]:
    priority_by_status = {
        "proposed": 55,
        "incomplete": 75,
        "unsupported": 80,
        "needs_review": 70,
        "rejected": 80,
        "error": 85,
    }
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Skill Invocation proposal: {proposal.skill_id}; "
                f"status={proposal.proposal_status}; missing={len(proposal.missing_inputs)}."
            ),
            created_at=proposal.created_at,
            source="skill_proposal",
            priority=priority_by_status.get(proposal.proposal_status, 55),
            refs=[
                {"ref_type": "skill_invocation_proposal", "ref_id": proposal.proposal_id},
                {"ref_type": "skill_proposal_intent", "ref_id": proposal.intent_id},
            ],
            entry_attrs={
                "skill_id": proposal.skill_id,
                "proposal_status": proposal.proposal_status,
                "executable_now": proposal.executable_now,
            },
        )
        for proposal in proposals
    ]


def skill_proposal_results_to_history_entries(
    results: list[SkillProposalResult],
) -> list[ContextHistoryEntry]:
    priority_by_status = {
        "proposal_available": 60,
        "incomplete": 75,
        "unsupported": 80,
        "needs_review": 70,
        "no_proposal": 45,
        "error": 85,
    }
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Skill Proposal result: status={result.status}; {result.summary}",
            created_at=result.created_at,
            source="skill_proposal",
            priority=priority_by_status.get(result.status, 55),
            refs=[{"ref_type": "skill_proposal_result", "ref_id": result.result_id}],
            entry_attrs={
                "status": result.status,
                "proposal_count": len(result.proposal_ids),
                "proposal_only": True,
            },
        )
        for result in results
    ]


def skill_proposal_review_notes_to_history_entries(
    review_notes: list[SkillProposalReviewNote],
) -> list[ContextHistoryEntry]:
    priority_by_type = {
        "unsupported_operation": 85,
        "missing_input": 75,
        "capability_boundary": 80,
        "permission_boundary": 80,
        "workspace_boundary": 80,
        "explicit_invocation_required": 60,
        "privacy_note": 80,
    }
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Skill Proposal review note: {note.note_type}; {note.message}",
            created_at=note.created_at,
            source="skill_proposal",
            priority=priority_by_type.get(note.note_type, 65),
            refs=[{"ref_type": "skill_proposal_review_note", "ref_id": note.review_note_id}],
            entry_attrs={
                "note_type": note.note_type,
                "severity": note.severity,
                "proposal_only": True,
            },
        )
        for note in review_notes
    ]


def skill_proposal_review_requests_to_history_entries(
    requests: list[SkillProposalReviewRequest],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=request.session_id,
            process_instance_id=request.process_instance_id,
            role="context",
            content=(
                f"Skill Proposal Review requested: {request.skill_id}; "
                f"missing={len(request.missing_inputs)}."
            ),
            created_at=request.created_at,
            source="skill_proposal_review",
            priority=60 if request.missing_inputs else 50,
            refs=[
                {"ref_type": "skill_proposal_review_request", "ref_id": request.review_request_id},
                {"ref_type": "skill_invocation_proposal", "ref_id": request.proposal_id},
            ],
            entry_attrs={
                "skill_id": request.skill_id,
                "status": request.status,
                "missing_input_count": len(request.missing_inputs),
            },
        )
        for request in requests
    ]


def skill_proposal_review_decisions_to_history_entries(
    decisions: list[SkillProposalReviewDecision],
) -> list[ContextHistoryEntry]:
    priority_by_decision = {
        "approved_for_explicit_invocation": 60,
        "rejected": 85,
        "needs_more_input": 80,
        "revise_proposal": 70,
        "no_action": 60,
        "needs_review": 75,
        "error": 90,
    }
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Skill Proposal Review decision: decision={decision.decision}; "
                f"bridge_candidate={decision.can_bridge_to_execution}."
            ),
            created_at=decision.created_at,
            source="skill_proposal_review",
            priority=priority_by_decision.get(decision.decision, 65),
            refs=[
                {"ref_type": "skill_proposal_review_decision", "ref_id": decision.review_decision_id},
                {"ref_type": "skill_proposal_review_request", "ref_id": decision.review_request_id},
            ],
            entry_attrs={
                "decision": decision.decision,
                "requires_explicit_invocation": decision.requires_explicit_invocation,
                "can_bridge_to_execution": decision.can_bridge_to_execution,
            },
        )
        for decision in decisions
    ]


def skill_proposal_review_results_to_history_entries(
    results: list[SkillProposalReviewResult],
) -> list[ContextHistoryEntry]:
    priority_by_status = {
        "approved": 60,
        "rejected": 85,
        "needs_more_input": 80,
        "revise_proposal": 70,
        "no_action": 60,
        "needs_review": 75,
        "error": 90,
    }
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Skill Proposal Review result: status={result.status}; {result.summary}",
            created_at=result.created_at,
            source="skill_proposal_review",
            priority=priority_by_status.get(result.status, 65),
            refs=[
                {"ref_type": "skill_proposal_review_result", "ref_id": result.review_result_id},
                {"ref_type": "skill_proposal_review_request", "ref_id": result.review_request_id},
                {"ref_type": "skill_proposal_review_decision", "ref_id": result.decision_id},
            ],
            entry_attrs={
                "status": result.status,
                "bridge_candidate": result.bridge_candidate,
                "finding_count": len(result.finding_ids),
            },
        )
        for result in results
    ]


def skill_proposal_review_findings_to_history_entries(
    findings: list[SkillProposalReviewFinding],
) -> list[ContextHistoryEntry]:
    priority_by_type = {
        "unsupported_skill": 90,
        "shell_not_supported": 90,
        "network_not_supported": 90,
        "write_not_supported": 90,
        "mcp_not_supported": 90,
        "plugin_not_supported": 90,
        "external_capability_not_supported": 90,
        "missing_input": 80,
        "invalid_decision": 90,
        "approval_reason_required": 80,
    }
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Skill Proposal Review finding: {finding.finding_type}; {finding.message}",
            created_at=finding.created_at,
            source="skill_proposal_review",
            priority=priority_by_type.get(finding.finding_type, 70),
            refs=[
                {"ref_type": "skill_proposal_review_finding", "ref_id": finding.finding_id},
                {"ref_type": "skill_proposal_review_request", "ref_id": finding.review_request_id},
            ],
            entry_attrs={
                "finding_type": finding.finding_type,
                "status": finding.status,
                "severity": finding.severity,
            },
        )
        for finding in findings
    ]


def reviewed_execution_bridge_requests_to_history_entries(
    requests: list[ReviewedExecutionBridgeRequest],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=request.session_id,
            process_instance_id=request.process_instance_id,
            role="context",
            content=f"Reviewed Execution Bridge requested: {request.skill_id}",
            created_at=request.created_at,
            source="reviewed_execution_bridge",
            priority=55,
            refs=[
                {"ref_type": "reviewed_execution_bridge_request", "ref_id": request.bridge_request_id},
                {"ref_type": "skill_invocation_proposal", "ref_id": request.proposal_id},
                {"ref_type": "skill_proposal_review_decision", "ref_id": request.review_decision_id},
            ],
            entry_attrs={
                "skill_id": request.skill_id,
                "status": request.status,
                "invocation_mode": request.invocation_mode,
            },
        )
        for request in requests
    ]


def reviewed_execution_bridge_decisions_to_history_entries(
    decisions: list[ReviewedExecutionBridgeDecision],
) -> list[ContextHistoryEntry]:
    priority_by_decision = {
        "allow": 60,
        "deny": 90,
        "needs_more_input": 80,
        "unsupported": 90,
        "error": 90,
    }
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Reviewed Execution Bridge decision: {decision.decision}; "
                f"can_bridge={decision.can_bridge}."
            ),
            created_at=decision.created_at,
            source="reviewed_execution_bridge",
            priority=priority_by_decision.get(decision.decision, 70),
            refs=[
                {"ref_type": "reviewed_execution_bridge_decision", "ref_id": decision.bridge_decision_id},
                {"ref_type": "reviewed_execution_bridge_request", "ref_id": decision.bridge_request_id},
            ],
            entry_attrs={
                "decision": decision.decision,
                "decision_basis": decision.decision_basis,
                "can_bridge": decision.can_bridge,
            },
        )
        for decision in decisions
    ]


def reviewed_execution_bridge_results_to_history_entries(
    results: list[ReviewedExecutionBridgeResult],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Reviewed Execution Bridge result: status={result.status}; "
                f"executed={result.executed}; blocked={result.blocked}."
            ),
            created_at=result.created_at,
            source="reviewed_execution_bridge",
            priority=60 if result.executed else 90 if result.blocked else 75,
            refs=[
                {"ref_type": "reviewed_execution_bridge_result", "ref_id": result.bridge_result_id},
                {"ref_type": "reviewed_execution_bridge_decision", "ref_id": result.bridge_decision_id},
            ],
            entry_attrs={
                "status": result.status,
                "executed": result.executed,
                "blocked": result.blocked,
                "gate_result_id": result.gate_result_id,
                "execution_envelope_id": result.execution_envelope_id,
            },
        )
        for result in results
    ]


def reviewed_execution_bridge_violations_to_history_entries(
    violations: list[ReviewedExecutionBridgeViolation],
) -> list[ContextHistoryEntry]:
    priority_by_type = {
        "review_not_approved": 90,
        "review_decision_not_bridgeable": 90,
        "review_result_not_bridge_candidate": 90,
        "missing_input": 80,
        "unsupported_skill": 90,
        "write_not_supported": 90,
        "shell_not_supported": 90,
        "network_not_supported": 90,
        "mcp_not_supported": 90,
        "plugin_not_supported": 90,
        "external_capability_not_supported": 90,
    }
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Reviewed Execution Bridge violation: {violation.violation_type}; {violation.message}",
            created_at=violation.created_at,
            source="reviewed_execution_bridge",
            priority=priority_by_type.get(violation.violation_type, 80),
            refs=[
                {"ref_type": "reviewed_execution_bridge_violation", "ref_id": violation.violation_id},
                {"ref_type": "reviewed_execution_bridge_request", "ref_id": violation.bridge_request_id},
            ],
            entry_attrs={
                "violation_type": violation.violation_type,
                "severity": violation.severity,
                "subject_ref": violation.subject_ref,
            },
        )
        for violation in violations
    ]


def skill_execution_gate_decisions_to_history_entries(
    decisions: list[SkillExecutionGateDecision],
) -> list[ContextHistoryEntry]:
    priority_by_decision = {
        "allow": 55,
        "deny": 90,
        "unsupported": 85,
        "needs_review": 80,
        "error": 90,
    }
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Skill Execution Gate decision: {decision.skill_id}; "
                f"decision={decision.decision}; can_execute={decision.can_execute}."
            ),
            created_at=decision.created_at,
            source="skill_execution_gate",
            priority=priority_by_decision.get(decision.decision, 65),
            refs=[
                {"ref_type": "skill_execution_gate_decision", "ref_id": decision.gate_decision_id},
                {"ref_type": "skill_execution_gate_request", "ref_id": decision.gate_request_id},
            ],
            entry_attrs={
                "skill_id": decision.skill_id,
                "decision": decision.decision,
                "enforcement_scope": decision.enforcement_scope,
            },
        )
        for decision in decisions
    ]


def skill_execution_gate_results_to_history_entries(
    results: list[SkillExecutionGateResult],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Skill Execution Gate result: status={result.status}; "
                f"executed={result.executed}; blocked={result.blocked}."
            ),
            created_at=result.created_at,
            source="skill_execution_gate",
            priority=60 if result.executed else 85,
            refs=[
                {"ref_type": "skill_execution_gate_result", "ref_id": result.gate_result_id},
                {"ref_type": "skill_execution_gate_decision", "ref_id": result.gate_decision_id},
            ],
            entry_attrs={
                "status": result.status,
                "executed": result.executed,
                "blocked": result.blocked,
            },
        )
        for result in results
    ]


def skill_execution_gate_findings_to_history_entries(
    findings: list[SkillExecutionGateFinding],
) -> list[ContextHistoryEntry]:
    priority_by_status = {"failed": 90, "warning": 75, "passed": 45, "skipped": 40}
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Skill Execution Gate finding: {finding.finding_type}; {finding.message}",
            created_at=finding.created_at,
            source="skill_execution_gate",
            priority=priority_by_status.get(finding.status, 70),
            refs=[
                {"ref_type": "skill_execution_gate_finding", "ref_id": finding.finding_id},
                {"ref_type": "skill_execution_gate_request", "ref_id": finding.gate_request_id},
            ],
            entry_attrs={
                "finding_type": finding.finding_type,
                "status": finding.status,
                "severity": finding.severity,
            },
        )
        for finding in findings
    ]


def internal_skill_descriptors_to_history_entries(
    descriptors: list[InternalSkillDescriptor],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Internal Skill descriptor: {descriptor.skill_id}; "
                f"category={descriptor.capability_category}; risk={descriptor.risk_class}."
            ),
            created_at=descriptor.created_at,
            source="internal_skill_onboarding",
            priority=45,
            refs=[
                {"ref_type": "internal_skill_descriptor", "ref_id": descriptor.descriptor_id}
            ],
            entry_attrs={
                "skill_id": descriptor.skill_id,
                "capability_category": descriptor.capability_category,
                "risk_class": descriptor.risk_class,
                "enabled_by_default": descriptor.enabled_by_default,
            },
        )
        for descriptor in descriptors
    ]


def internal_skill_onboarding_results_to_history_entries(
    results: list[InternalSkillOnboardingResult],
) -> list[ContextHistoryEntry]:
    priority_by_status = {
        "blocked": 90,
        "rejected": 90,
        "needs_fix": 80,
        "accepted": 60,
    }
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Internal Skill onboarding result: {result.skill_id}; "
                f"status={result.status}; enabled={result.enabled}."
            ),
            created_at=result.created_at,
            source="internal_skill_onboarding",
            priority=priority_by_status.get(result.status, 70),
            refs=[
                {"ref_type": "internal_skill_onboarding_result", "ref_id": result.result_id},
                {"ref_type": "internal_skill_descriptor", "ref_id": result.descriptor_id},
            ],
            entry_attrs={
                "skill_id": result.skill_id,
                "status": result.status,
                "accepted": result.accepted,
                "enabled": result.enabled,
                "finding_count": len(result.finding_ids),
            },
        )
        for result in results
    ]


def internal_skill_onboarding_findings_to_history_entries(
    findings: list[InternalSkillOnboardingFinding],
) -> list[ContextHistoryEntry]:
    priority_by_severity = {
        "critical": 95,
        "high": 90,
        "medium": 75,
        "low": 55,
    }
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Internal Skill onboarding finding: {finding.finding_type}; {finding.message}",
            created_at=finding.created_at,
            source="internal_skill_onboarding",
            priority=priority_by_severity.get(finding.severity, 70),
            refs=[
                {"ref_type": "internal_skill_onboarding_finding", "ref_id": finding.finding_id}
            ],
            entry_attrs={
                "skill_id": finding.skill_id,
                "finding_type": finding.finding_type,
                "status": finding.status,
                "severity": finding.severity,
            },
        )
        for finding in findings
    ]


def internal_skill_observability_contracts_to_history_entries(
    contracts: list[InternalSkillObservabilityContract],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Internal Skill observability contract: {contract.skill_id}; "
                f"ocel_objects={len(contract.ocel_object_types)}; "
                f"pig_keys={len(contract.pig_report_keys)}."
            ),
            created_at=contract.created_at,
            source="internal_skill_onboarding",
            priority=55,
            refs=[
                {
                    "ref_type": "internal_skill_observability_contract",
                    "ref_id": contract.observability_contract_id,
                }
            ],
            entry_attrs={
                "skill_id": contract.skill_id,
                "envelope_required": contract.envelope_required,
                "audit_visible": contract.audit_visible,
                "workbench_visible": contract.workbench_visible,
            },
        )
        for contract in contracts
    ]


def skill_registry_views_to_history_entries(views: list[SkillRegistryView]) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Skill Registry View: {view.view_name}; "
                f"total={view.total_skill_count}; candidates={view.candidate_skill_count}."
            ),
            created_at=view.created_at,
            source="skill_registry_view",
            priority=45 if view.blocked_skill_count == 0 else 80,
            refs=[{"ref_type": "skill_registry_view", "ref_id": view.registry_view_id}],
            entry_attrs={
                "registry_view_id": view.registry_view_id,
                "observation_skill_count": view.observation_skill_count,
                "digestion_skill_count": view.digestion_skill_count,
                "external_candidate_count": view.external_candidate_count,
            },
        )
        for view in views
    ]


def skill_registry_entries_to_history_entries(entries: list[SkillRegistryEntry]) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Skill Registry entry: {entry.skill_id}; "
                f"layer={entry.skill_layer}; status={entry.status}; execution={entry.execution_enabled}."
            ),
            created_at=entry.created_at,
            source="skill_registry_view",
            priority=_skill_registry_entry_priority(entry),
            refs=[{"ref_type": "skill_registry_entry", "ref_id": entry.registry_entry_id}],
            entry_attrs={
                "skill_id": entry.skill_id,
                "skill_layer": entry.skill_layer,
                "risk_class": entry.risk_class,
                "status": entry.status,
                "execution_enabled": entry.execution_enabled,
            },
        )
        for entry in entries
    ]


def skill_registry_results_to_history_entries(results: list[SkillRegistryResult]) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Skill Registry result: {result.command_name}; {result.summary}",
            created_at=result.created_at,
            source="skill_registry_view",
            priority=50 if result.status == "completed" else 75,
            refs=[{"ref_type": "skill_registry_result", "ref_id": result.registry_result_id}],
            entry_attrs={
                "registry_view_id": result.registry_view_id,
                "status": result.status,
                "entry_count": len(result.entry_ids),
                "finding_count": len(result.finding_ids),
            },
        )
        for result in results
    ]


def skill_registry_findings_to_history_entries(findings: list[SkillRegistryFinding]) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Skill Registry finding: {finding.finding_type}; {finding.message}",
            created_at=finding.created_at,
            source="skill_registry_view",
            priority=_skill_registry_finding_priority(finding),
            refs=[{"ref_type": "skill_registry_finding", "ref_id": finding.finding_id}],
            entry_attrs={
                "skill_id": finding.skill_id,
                "finding_type": finding.finding_type,
                "status": finding.status,
                "severity": finding.severity,
            },
        )
        for finding in findings
    ]


def _skill_registry_entry_priority(entry: SkillRegistryEntry) -> int:
    if entry.status == "blocked" or entry.skill_layer == "blocked":
        return 90
    if entry.execution_enabled and entry.skill_layer in {"external_candidate", "external_adapted"}:
        return 90
    if entry.status == "accepted":
        return 60
    if entry.status == "pending_review":
        return 65
    return 50


def _skill_registry_finding_priority(finding: SkillRegistryFinding) -> int:
    if finding.finding_type in {"unsafe_enabled", "unsafe_external_candidate"}:
        return 90
    if finding.finding_type == "missing_contract":
        return 85 if finding.severity == "high" else 75
    if finding.severity == "high":
        return 85
    if finding.severity == "medium":
        return 70
    return 50


def observation_digest_intents_to_history_entries(
    intents: list[ObservationDigestIntentCandidate],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Observation/Digestion intent: {intent.intent_family}; "
                f"skills={len(intent.suggested_skill_ids)}."
            ),
            created_at=intent.created_at,
            source="observation_digest_proposal",
            priority=70 if intent.confidence < 0.5 else 55,
            refs=[{"ref_type": "observation_digest_intent_candidate", "ref_id": intent.intent_candidate_id}],
            entry_attrs={
                "intent_family": intent.intent_family,
                "intent_name": intent.intent_name,
                "confidence": intent.confidence,
            },
        )
        for intent in intents
    ]


def observation_digest_proposal_sets_to_history_entries(
    sets: list[ObservationDigestProposalSet],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Observation/Digestion proposal set: {item.family}; "
                f"status={item.status}; proposals={len(item.proposal_ids)}."
            ),
            created_at=item.created_at,
            source="observation_digest_proposal",
            priority=_observation_digest_proposal_status_priority(item.status),
            refs=[{"ref_type": "observation_digest_proposal_set", "ref_id": item.proposal_set_id}],
            entry_attrs={
                "family": item.family,
                "status": item.status,
                "execution_performed": item.execution_performed,
                "requires_review": item.requires_review,
            },
        )
        for item in sets
    ]


def observation_digest_proposal_results_to_history_entries(
    results: list[ObservationDigestProposalResult],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Observation/Digestion proposal result: {result.summary}",
            created_at=result.created_at,
            source="observation_digest_proposal",
            priority=_observation_digest_proposal_status_priority(result.status),
            refs=[{"ref_type": "observation_digest_proposal_result", "ref_id": result.result_id}],
            entry_attrs={
                "status": result.status,
                "created_proposal_count": result.created_proposal_count,
                "execution_performed": result.execution_performed,
                "review_required": result.review_required,
            },
        )
        for result in results
    ]


def observation_digest_proposal_findings_to_history_entries(
    findings: list[ObservationDigestProposalFinding],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Observation/Digestion proposal finding: {finding.finding_type}; {finding.message}",
            created_at=finding.created_at,
            source="observation_digest_proposal",
            priority=_observation_digest_proposal_finding_priority(finding),
            refs=[{"ref_type": "observation_digest_proposal_finding", "ref_id": finding.finding_id}],
            entry_attrs={
                "finding_type": finding.finding_type,
                "status": finding.status,
                "severity": finding.severity,
                "skill_id": finding.skill_id,
            },
        )
        for finding in findings
    ]


def _observation_digest_proposal_status_priority(status: str) -> int:
    if status == "no_matching_skill":
        return 90
    if status == "needs_more_input":
        return 75
    if status == "proposal_created":
        return 60
    return 55


def _observation_digest_proposal_finding_priority(finding: ObservationDigestProposalFinding) -> int:
    if finding.finding_type == "no_matching_skill":
        return 90
    if finding.finding_type == "missing_required_input":
        return 75
    if finding.finding_type == "low_confidence_intent":
        return 70
    return 55


def observation_digest_runtime_bindings_to_history_entries(
    bindings: list[ObservationDigestSkillRuntimeBinding],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Observation/Digestion runtime binding: {binding.skill_id}; "
                f"family={binding.skill_family}; read_only={binding.read_only}."
            ),
            created_at=binding.created_at,
            source="observation_digest_invocation",
            priority=55 if binding.enabled else 80,
            refs=[{"ref_type": "observation_digest_skill_runtime_binding", "ref_id": binding.binding_id}],
            entry_attrs={
                "skill_id": binding.skill_id,
                "skill_family": binding.skill_family,
                "enabled": binding.enabled,
                "gate_required": binding.gate_required,
                "envelope_required": binding.envelope_required,
            },
        )
        for binding in bindings
    ]


def observation_digest_invocation_results_to_history_entries(
    results: list[ObservationDigestInvocationResult],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Observation/Digestion invocation result: {result.skill_id}; "
                f"status={result.status}; blocked={result.blocked}."
            ),
            created_at=result.created_at,
            source="observation_digest_invocation",
            priority=_observation_digest_invocation_result_priority(result),
            refs=[{"ref_type": "observation_digest_invocation_result", "ref_id": result.result_id}],
            entry_attrs={
                "skill_id": result.skill_id,
                "status": result.status,
                "executed": result.executed,
                "blocked": result.blocked,
                "envelope_id": result.envelope_id,
            },
        )
        for result in results
    ]


def observation_digest_invocation_findings_to_history_entries(
    findings: list[ObservationDigestInvocationFinding],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Observation/Digestion invocation finding: {finding.finding_type}; {finding.message}",
            created_at=finding.created_at,
            source="observation_digest_invocation",
            priority=_observation_digest_invocation_finding_priority(finding),
            refs=[{"ref_type": "observation_digest_invocation_finding", "ref_id": finding.finding_id}],
            entry_attrs={
                "skill_id": finding.skill_id,
                "finding_type": finding.finding_type,
                "status": finding.status,
                "severity": finding.severity,
            },
        )
        for finding in findings
    ]


def _observation_digest_invocation_result_priority(result: ObservationDigestInvocationResult) -> int:
    if result.blocked:
        return 90
    if result.status == "failed":
        return 85
    if result.status in {"completed", "pending_review"}:
        return 60
    return 55


def _observation_digest_invocation_finding_priority(finding: ObservationDigestInvocationFinding) -> int:
    if finding.finding_type in {
        "external_execution_denied",
        "path_traversal",
        "outside_workspace",
        "workspace_boundary_violation",
        "unsupported_skill",
    }:
        return 90
    if finding.finding_type == "missing_required_input":
        return 75
    if finding.severity == "high":
        return 85
    return 60


def observation_digest_conformance_checks_to_history_entries(
    checks: list[ObservationDigestConformanceCheck],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Observation/Digestion conformance check: {check.check_type}; status={check.status}.",
            created_at=check.created_at,
            source="observation_digest_conformance",
            priority=45 if check.passed else _observation_digest_conformance_severity_priority(check.severity),
            refs=[{"ref_type": "observation_digest_conformance_check", "ref_id": check.check_id}],
            entry_attrs={
                "skill_id": check.skill_id,
                "check_type": check.check_type,
                "status": check.status,
                "passed": check.passed,
            },
        )
        for check in checks
    ]


def observation_digest_smoke_results_to_history_entries(
    results: list[ObservationDigestSmokeResult],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Observation/Digestion smoke result: {result.skill_id}; status={result.status}.",
            created_at=result.created_at,
            source="observation_digest_conformance",
            priority=50 if result.passed else 85,
            refs=[{"ref_type": "observation_digest_smoke_result", "ref_id": result.smoke_result_id}],
            entry_attrs={
                "skill_id": result.skill_id,
                "status": result.status,
                "passed": result.passed,
                "envelope_id": result.envelope_id,
            },
        )
        for result in results
    ]


def observation_digest_conformance_findings_to_history_entries(
    findings: list[ObservationDigestConformanceFinding],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Observation/Digestion conformance finding: {finding.finding_type}; {finding.message}",
            created_at=finding.created_at,
            source="observation_digest_conformance",
            priority=_observation_digest_conformance_finding_priority(finding),
            refs=[{"ref_type": "observation_digest_conformance_finding", "ref_id": finding.finding_id}],
            entry_attrs={
                "skill_id": finding.skill_id,
                "finding_type": finding.finding_type,
                "status": finding.status,
                "severity": finding.severity,
            },
        )
        for finding in findings
    ]


def observation_digest_conformance_reports_to_history_entries(
    reports: list[ObservationDigestConformanceReport],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Observation/Digestion conformance report: status={report.status}; {report.summary}",
            created_at=report.created_at,
            source="observation_digest_conformance",
            priority=50 if report.status == "passed" else 85,
            refs=[{"ref_type": "observation_digest_conformance_report", "ref_id": report.report_id}],
            entry_attrs={
                "status": report.status,
                "failed_skill_count": report.failed_skill_count,
                "failed_check_count": report.failed_check_count,
                "smoke_failed_count": report.smoke_failed_count,
            },
        )
        for report in reports
    ]


def _observation_digest_conformance_severity_priority(severity: str) -> int:
    if severity == "critical":
        return 95
    if severity == "high":
        return 85
    if severity == "medium":
        return 70
    return 55


def _observation_digest_conformance_finding_priority(finding: ObservationDigestConformanceFinding) -> int:
    if finding.finding_type in {
        "external_execution_boundary",
        "mutation_boundary",
        "missing_input_contract",
        "missing_output_contract",
        "missing_gate_contract",
        "missing_observability_contract",
    }:
        return 90
    return _observation_digest_conformance_severity_priority(finding.severity)


def external_skill_resource_inventories_to_history_entries(
    inventories: list[ExternalSkillResourceInventory],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"External skill resource inventory: resources={inventory.resource_count}.",
            created_at=inventory.created_at,
            source="external_skill_static_digestion",
            priority=65 if inventory.script_files else 45,
            refs=[{"ref_type": "external_skill_resource_inventory", "ref_id": inventory.inventory_id}],
            entry_attrs={
                "resource_count": inventory.resource_count,
                "script_count": len(inventory.script_files),
                "private": inventory.private,
                "sensitive": inventory.sensitive,
            },
        )
        for inventory in inventories
    ]


def external_skill_manifest_profiles_to_history_entries(
    profiles: list[ExternalSkillManifestProfile],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"External skill manifest profile: kind={profile.manifest_kind}; status={profile.parse_status}.",
            created_at=profile.created_at,
            source="external_skill_static_digestion",
            priority=70 if profile.parse_status == "failed" else 45,
            refs=[{"ref_type": "external_skill_manifest_profile", "ref_id": profile.manifest_profile_id}],
            entry_attrs={
                "manifest_kind": profile.manifest_kind,
                "parse_status": profile.parse_status,
                "confidence": profile.confidence,
            },
        )
        for profile in profiles
    ]


def external_skill_instruction_profiles_to_history_entries(
    profiles: list[ExternalSkillInstructionProfile],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"External skill instruction profile: title={profile.title or 'unknown'}.",
            created_at=profile.created_at,
            source="external_skill_static_digestion",
            priority=60 if profile.confidence < 0.5 else 45,
            refs=[{"ref_type": "external_skill_instruction_profile", "ref_id": profile.instruction_profile_id}],
            entry_attrs={
                "instruction_kind": profile.instruction_kind,
                "full_body_stored": profile.full_body_stored,
                "confidence": profile.confidence,
            },
        )
        for profile in profiles
    ]


def external_skill_declared_capabilities_to_history_entries(
    capabilities: list[ExternalSkillDeclaredCapability],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"External skill declared capability: {capability.capability_name}; risk={capability.declared_risk_class}.",
            created_at=capability.created_at,
            source="external_skill_static_digestion",
            priority=80 if capability.declared_risk_class == "high" else 55,
            refs=[{"ref_type": "external_skill_declared_capability", "ref_id": capability.declared_capability_id}],
            entry_attrs={
                "capability_category": capability.capability_category,
                "declared_risk_class": capability.declared_risk_class,
            },
        )
        for capability in capabilities
    ]


def external_skill_static_risk_profiles_to_history_entries(
    profiles: list[ExternalSkillStaticRiskProfile],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"External skill static risk profile: risk={profile.risk_class}.",
            created_at=profile.created_at,
            source="external_skill_static_digestion",
            priority=_external_skill_static_risk_priority(profile),
            refs=[{"ref_type": "external_skill_static_risk_profile", "ref_id": profile.static_risk_profile_id}],
            entry_attrs={
                "risk_class": profile.risk_class,
                "execution_allowed_by_default": profile.execution_allowed_by_default,
                "requires_review": profile.requires_review,
            },
        )
        for profile in profiles
    ]


def external_skill_static_digestion_reports_to_history_entries(
    reports: list[ExternalSkillStaticDigestionReport],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"External skill static digestion report: status={report.status}; {report.summary}",
            created_at=report.created_at,
            source="external_skill_static_digestion",
            priority=75 if report.status == "completed_with_findings" else 55,
            refs=[{"ref_type": "external_skill_static_digestion_report", "ref_id": report.report_id}],
            entry_attrs={
                "status": report.status,
                "finding_count": len(report.finding_ids),
                "assimilation_candidate_id": report.assimilation_candidate_id,
            },
        )
        for report in reports
    ]


def external_skill_static_digestion_findings_to_history_entries(
    findings: list[ExternalSkillStaticDigestionFinding],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"External skill static digestion finding: {finding.finding_type}; {finding.message}",
            created_at=finding.created_at,
            source="external_skill_static_digestion",
            priority=_external_skill_static_finding_priority(finding),
            refs=[{"ref_type": "external_skill_static_digestion_finding", "ref_id": finding.finding_id}],
            entry_attrs={
                "finding_type": finding.finding_type,
                "status": finding.status,
                "severity": finding.severity,
            },
        )
        for finding in findings
    ]


def _external_skill_static_risk_priority(profile: ExternalSkillStaticRiskProfile) -> int:
    if profile.declared_shell or profile.declared_network or profile.declared_write or profile.declared_mcp:
        return 90
    if profile.declared_plugin or profile.declared_external_execution or profile.declared_private_context_access:
        return 90
    if profile.risk_class == "high":
        return 85
    if profile.risk_class == "medium":
        return 70
    return 50


def _external_skill_static_finding_priority(finding: ExternalSkillStaticDigestionFinding) -> int:
    if finding.finding_type in {
        "shell_declared",
        "network_declared",
        "write_declared",
        "mcp_declared",
        "plugin_declared",
        "external_execution_declared",
        "private_context_risk",
        "workspace_boundary_violation",
    }:
        return 90
    if finding.severity == "high":
        return 85
    if finding.severity == "medium":
        return 70
    return 55


def agent_instances_to_history_entries(items: list[AgentInstance]) -> list[ContextHistoryEntry]:
    return [_spine_entry("agent_instance", item.agent_instance_id, f"Agent instance observed: runtime={item.source_runtime}.", item.created_at, 50, item.to_dict()) for item in items]


def agent_runtime_descriptors_to_history_entries(items: list[AgentRuntimeDescriptor]) -> list[ContextHistoryEntry]:
    return [_spine_entry("agent_runtime_descriptor", item.runtime_descriptor_id, f"Agent runtime descriptor: {item.runtime_name}.", item.created_at, 45, item.to_dict()) for item in items]


def environment_snapshots_to_history_entries(items: list[RuntimeEnvironmentSnapshot]) -> list[ContextHistoryEntry]:
    return [_spine_entry("runtime_environment_snapshot", item.environment_snapshot_id, f"Runtime environment snapshot: runtime={item.runtime_kind}.", item.created_at, 60, item.to_dict()) for item in items]


def movement_ontology_terms_to_history_entries(items: list[AgentMovementOntologyTerm]) -> list[ContextHistoryEntry]:
    return [_spine_entry("agent_movement_ontology_term", item.ontology_term_id, f"Movement ontology term: {item.term_kind}={item.term_value}.", item.created_at, 35, item.to_dict()) for item in items]


def normalized_events_v2_to_history_entries(items: list[AgentObservationNormalizedEventV2]) -> list[ContextHistoryEntry]:
    return [_spine_entry("agent_observation_normalized_event_v2", item.normalized_event_id, f"Observation V2 event: action={item.canonical_action_type}.", item.created_at, 55 if item.confidence >= 0.5 else 75, item.to_dict()) for item in items]


def observed_objects_to_history_entries(items: list[ObservedAgentObject]) -> list[ContextHistoryEntry]:
    return [_spine_entry("observed_agent_object", item.observed_object_id, f"Observed agent object: type={item.object_type}.", item.created_at, 50, item.to_dict()) for item in items]


def observed_relations_to_history_entries(items: list[ObservedAgentRelation]) -> list[ContextHistoryEntry]:
    return [_spine_entry("observed_agent_relation", item.observed_relation_id, f"Observed agent relation: type={item.relation_type}.", item.created_at, 70 if item.causal_claim else 50, item.to_dict()) for item in items]


def behavior_inferences_v2_to_history_entries(items: list[AgentBehaviorInferenceV2]) -> list[ContextHistoryEntry]:
    return [_spine_entry("agent_behavior_inference_v2", item.inference_id, f"Behavior inference V2: observed_run={item.observed_run_id}.", item.created_at, 65, item.to_dict()) for item in items]


def observation_reviews_to_history_entries(items: list[AgentObservationReview]) -> list[ContextHistoryEntry]:
    return [_spine_entry("agent_observation_review", item.review_id, f"Observation review: status={item.review_status}.", item.created_at, 60, item.to_dict()) for item in items]


def observation_corrections_to_history_entries(items: list[AgentObservationCorrection]) -> list[ContextHistoryEntry]:
    return [_spine_entry("agent_observation_correction", item.correction_id, f"Observation correction: field={item.corrected_field}.", item.created_at, 65, item.to_dict()) for item in items]


def redaction_policies_to_history_entries(items: list[ObservationRedactionPolicy]) -> list[ContextHistoryEntry]:
    return [_spine_entry("observation_redaction_policy", item.redaction_policy_id, "Observation redaction policy registered.", item.created_at, 70, item.to_dict()) for item in items]


def export_policies_to_history_entries(items: list[ObservationExportPolicy]) -> list[ContextHistoryEntry]:
    return [_spine_entry("observation_export_policy", item.export_policy_id, "Observation export policy registered.", item.created_at, 75, item.to_dict()) for item in items]


def fleet_snapshots_to_history_entries(items: list[AgentFleetObservationSnapshot]) -> list[ContextHistoryEntry]:
    return [_spine_entry("agent_fleet_observation_snapshot", item.fleet_snapshot_id, f"Fleet observation snapshot: agents={item.agent_instance_count}; runs={item.observed_run_count}.", item.created_at, 65, item.to_dict()) for item in items]


def observation_spine_findings_to_history_entries(items: list[AgentObservationSpineFinding]) -> list[ContextHistoryEntry]:
    return [_spine_entry("agent_observation_spine_finding", item.finding_id, f"Observation spine finding: {item.finding_type}; {item.message}", item.created_at, _spine_finding_priority(item), item.to_dict()) for item in items]


def observation_spine_results_to_history_entries(items: list[AgentObservationSpineResult]) -> list[ContextHistoryEntry]:
    return [_spine_entry("agent_observation_spine_result", item.result_id, f"Observation spine result: status={item.status}; {item.summary}", item.created_at, 55 if item.status == "completed" else 75, item.to_dict()) for item in items]


def _spine_entry(ref_type: str, ref_id: str, content: str, created_at: str, priority: int, attrs: dict) -> ContextHistoryEntry:
    return ContextHistoryEntry(
        entry_id=new_context_history_entry_id(),
        session_id=None,
        process_instance_id=None,
        role="context",
        content=content,
        created_at=created_at,
        source="agent_observation_spine",
        priority=priority,
        refs=[{"ref_type": ref_type, "ref_id": ref_id}],
        entry_attrs=attrs,
    )


def _spine_finding_priority(finding: AgentObservationSpineFinding) -> int:
    if finding.finding_type in {"privacy_export_boundary", "redaction_required", "low_confidence"}:
        return 90 if finding.severity == "high" else 75
    if finding.severity == "high":
        return 85
    if finding.severity == "medium":
        return 70
    return 55


def cross_harness_adapter_policies_to_history_entries(items: list[CrossHarnessTraceAdapterPolicy]) -> list[ContextHistoryEntry]:
    return [_cross_harness_entry("cross_harness_trace_adapter_policy", item.policy_id, f"Cross-harness trace adapter policy: status={item.status}.", item.created_at, 55, item.to_dict()) for item in items]


def harness_trace_adapter_contracts_to_history_entries(items: list[HarnessTraceAdapterContract]) -> list[ContextHistoryEntry]:
    return [_cross_harness_entry("harness_trace_adapter_contract", item.adapter_contract_id, f"Harness trace adapter contract: {item.adapter_name}; implemented={str(item.implemented).lower()}.", item.created_at, 50 if item.implemented else 65, item.to_dict()) for item in items]


def harness_trace_source_inspections_to_history_entries(items: list[HarnessTraceSourceInspection]) -> list[ContextHistoryEntry]:
    return [_cross_harness_entry("harness_trace_source_inspection", item.inspection_id, f"Harness trace source inspection: adapter={item.selected_adapter_name}; records={item.record_count}.", item.created_at, 55 if item.supported_by_adapter else 75, item.to_dict()) for item in items]


def harness_trace_mapping_rules_to_history_entries(items: list[HarnessTraceMappingRule]) -> list[ContextHistoryEntry]:
    return [_cross_harness_entry("harness_trace_mapping_rule", item.mapping_rule_id, f"Harness trace mapping rule: {item.source_event_pattern} -> {item.target_action_type}.", item.created_at, 45 if item.implemented else 60, item.to_dict()) for item in items]


def harness_trace_normalization_results_to_history_entries(items: list[HarnessTraceNormalizationResult]) -> list[ContextHistoryEntry]:
    return [_cross_harness_entry("harness_trace_normalization_result", item.normalization_result_id, f"Harness trace normalization result: status={item.status}; events={item.normalized_event_count}.", item.created_at, 60 if item.status == "completed" else 80, item.to_dict()) for item in items]


def harness_trace_adapter_coverage_reports_to_history_entries(items: list[HarnessTraceAdapterCoverageReport]) -> list[ContextHistoryEntry]:
    return [_cross_harness_entry("harness_trace_adapter_coverage_report", item.coverage_report_id, f"Harness trace adapter coverage: status={item.coverage_status}; mapped={item.mapped_event_type_count}.", item.created_at, 60 if item.coverage_status == "implemented" else 75, item.to_dict()) for item in items]


def harness_trace_adapter_findings_to_history_entries(items: list[HarnessTraceAdapterFinding]) -> list[ContextHistoryEntry]:
    return [_cross_harness_entry("harness_trace_adapter_finding", item.finding_id, f"Harness trace adapter finding: {item.finding_type}; {item.message}", item.created_at, _cross_harness_finding_priority(item), item.to_dict()) for item in items]


def harness_trace_adapter_results_to_history_entries(items: list[HarnessTraceAdapterResult]) -> list[ContextHistoryEntry]:
    return [_cross_harness_entry("harness_trace_adapter_result", item.adapter_result_id, f"Harness trace adapter result: status={item.status}; {item.summary}", item.created_at, 60 if item.status == "completed" else 75, item.to_dict()) for item in items]


def _cross_harness_entry(ref_type: str, ref_id: str, content: str, created_at: str, priority: int, attrs: dict) -> ContextHistoryEntry:
    return ContextHistoryEntry(
        entry_id=new_context_history_entry_id(),
        session_id=None,
        process_instance_id=None,
        role="context",
        content=content,
        created_at=created_at,
        source="cross_harness_trace_adapter",
        priority=priority,
        refs=[{"ref_type": ref_type, "ref_id": ref_id}],
        entry_attrs=attrs,
    )


def _cross_harness_finding_priority(finding: HarnessTraceAdapterFinding) -> int:
    if finding.finding_type in {"unsupported_format", "workspace_boundary_violation"}:
        return 90
    if finding.finding_type == "adapter_not_implemented":
        return 75
    if finding.severity == "high":
        return 85
    if finding.severity == "medium":
        return 70
    return 55
