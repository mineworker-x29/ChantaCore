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
