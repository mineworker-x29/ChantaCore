from __future__ import annotations

from chanta_core.context.history import ContextHistoryEntry, new_context_history_entry_id
from chanta_core.sandbox.models import (
    WorkspaceWriteIntent,
    WorkspaceWriteSandboxDecision,
    WorkspaceWriteSandboxViolation,
)


def workspace_write_intents_to_history_entries(
    intents: list[WorkspaceWriteIntent],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=intent.session_id,
            process_instance_id=intent.process_instance_id,
            role="context",
            content=f"Workspace write intent: {intent.operation}\nTarget: {intent.target_path}",
            created_at=intent.created_at,
            source="workspace_write_sandbox",
            priority=55,
            refs=[_intent_ref(intent)],
            entry_attrs={"intent_id": intent.intent_id, "operation": intent.operation},
        )
        for intent in intents
    ]


def workspace_write_sandbox_decisions_to_history_entries(
    decisions: list[WorkspaceWriteSandboxDecision],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Workspace write sandbox decision: {decision.decision}\nBasis: {decision.decision_basis}",
            created_at=decision.created_at,
            source="workspace_write_sandbox",
            priority=_decision_priority(decision),
            refs=[
                {
                    "ref_type": "workspace_write_sandbox_decision",
                    "ref_id": decision.decision_id,
                    "decision_id": decision.decision_id,
                    "intent_id": decision.intent_id,
                    "workspace_root_id": decision.workspace_root_id,
                    "violation_ids": decision.violation_ids,
                    "matched_boundary_ids": decision.matched_boundary_ids,
                }
            ],
            entry_attrs={"decision_id": decision.decision_id, "decision": decision.decision},
        )
        for decision in decisions
    ]


def workspace_write_sandbox_violations_to_history_entries(
    violations: list[WorkspaceWriteSandboxViolation],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Workspace write sandbox violation: {violation.violation_type}\n{violation.message}",
            created_at=violation.created_at,
            source="workspace_write_sandbox",
            priority=90,
            refs=[
                {
                    "ref_type": "workspace_write_sandbox_violation",
                    "ref_id": violation.violation_id,
                    "violation_id": violation.violation_id,
                    "intent_id": violation.intent_id,
                    "workspace_root_id": violation.workspace_root_id,
                }
            ],
            entry_attrs={"violation_id": violation.violation_id, "violation_type": violation.violation_type},
        )
        for violation in violations
    ]


def _intent_ref(intent: WorkspaceWriteIntent) -> dict:
    return {
        "ref_type": "workspace_write_intent",
        "ref_id": intent.intent_id,
        "intent_id": intent.intent_id,
        "workspace_root_id": intent.workspace_root_id,
        "session_id": intent.session_id,
        "turn_id": intent.turn_id,
        "process_instance_id": intent.process_instance_id,
        "permission_request_id": intent.permission_request_id,
        "session_permission_resolution_id": intent.session_permission_resolution_id,
    }


def _decision_priority(decision: WorkspaceWriteSandboxDecision) -> int:
    if decision.decision == "denied":
        return 90
    if decision.decision in {"needs_review", "inconclusive", "error"}:
        return 80
    return 55
