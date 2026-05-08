from __future__ import annotations

from chanta_core.capabilities.models import (
    CapabilityDecision,
    CapabilityDecisionSurface,
    CapabilityRequestIntent,
)
from chanta_core.context.history import ContextHistoryEntry, new_context_history_entry_id


def capability_request_intents_to_history_entries(
    intents: list[CapabilityRequestIntent],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=intent.session_id,
            process_instance_id=None,
            role="context",
            content=f"Capability request intent: {intent.requested_operation}",
            created_at=intent.created_at,
            source="capability_decision",
            priority=55,
            refs=[
                {"ref_type": "capability_request_intent", "ref_id": intent.intent_id},
                *[
                    {"ref_type": "capability_requirement", "ref_id": requirement_id}
                    for requirement_id in intent.inferred_requirement_ids
                ],
            ],
            entry_attrs={
                "turn_id": intent.turn_id,
                "message_id": intent.message_id,
                "requested_operation": intent.requested_operation,
            },
        )
        for intent in intents
    ]


def capability_decisions_to_history_entries(
    decisions: list[CapabilityDecision],
) -> list[ContextHistoryEntry]:
    entries: list[ContextHistoryEntry] = []
    for decision in decisions:
        entries.append(
            ContextHistoryEntry(
                entry_id=new_context_history_entry_id(),
                session_id=None,
                process_instance_id=None,
                role="context",
                content=f"Capability decision: {decision.capability_name} -> {decision.availability}",
                created_at=decision.created_at,
                source="capability_decision",
                priority=_priority(decision.availability),
                refs=[
                    {"ref_type": "capability_decision", "ref_id": decision.decision_id},
                    {"ref_type": "capability_request_intent", "ref_id": decision.intent_id},
                    *(
                        [
                            {
                                "ref_type": "capability_requirement",
                                "ref_id": decision.requirement_id,
                            }
                        ]
                        if decision.requirement_id
                        else []
                    ),
                    *[
                        {"ref_type": "capability_decision_evidence", "ref_id": evidence_id}
                        for evidence_id in decision.evidence_ids
                    ],
                ],
                entry_attrs={
                    "availability": decision.availability,
                    "can_execute_now": decision.can_execute_now,
                    "requires_review": decision.requires_review,
                    "requires_permission": decision.requires_permission,
                },
            )
        )
    return entries


def capability_decision_surfaces_to_history_entries(
    surfaces: list[CapabilityDecisionSurface],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=surface.session_id,
            process_instance_id=None,
            role="context",
            content=(
                "Capability decision surface: "
                f"{surface.overall_availability}, mode={surface.recommended_agent_mode}"
            ),
            created_at=surface.created_at,
            source="capability_decision",
            priority=_priority(surface.overall_availability),
            refs=[
                {"ref_type": "capability_decision_surface", "ref_id": surface.surface_id},
                {"ref_type": "capability_request_intent", "ref_id": surface.intent_id},
                *[
                    {"ref_type": "capability_decision", "ref_id": decision_id}
                    for decision_id in surface.decision_ids
                ],
            ],
            entry_attrs={
                "turn_id": surface.turn_id,
                "message_id": surface.message_id,
                "can_fulfill_now": surface.can_fulfill_now,
                "recommended_agent_mode": surface.recommended_agent_mode,
            },
        )
        for surface in surfaces
    ]


def _priority(availability: str) -> int:
    if availability in {"not_implemented", "requires_permission", "requires_explicit_skill"}:
        return 90
    if availability in {"requires_review", "disabled_candidate"}:
        return 75
    if availability == "metadata_only":
        return 60
    if availability == "available_now":
        return 45
    return 65
