from chanta_core.capabilities import (
    CapabilityDecision,
    CapabilityDecisionSurface,
    CapabilityRequestIntent,
    capability_decision_surfaces_to_history_entries,
    capability_decisions_to_history_entries,
    capability_request_intents_to_history_entries,
)
from chanta_core.utility.time import utc_now_iso


def test_capability_decision_history_entries() -> None:
    now = utc_now_iso()
    intent = CapabilityRequestIntent(
        intent_id="capability_request_intent:test",
        session_id="session:test",
        turn_id="conversation_turn:test",
        message_id="message:test",
        user_prompt_preview="powershell",
        requested_operation="shell_execution",
        target_refs=[],
        inferred_requirement_ids=["capability_requirement:test"],
        created_at=now,
        intent_attrs={},
    )
    decision = CapabilityDecision(
        decision_id="capability_decision:test",
        intent_id=intent.intent_id,
        requirement_id="capability_requirement:test",
        capability_name="shell execution",
        availability="requires_permission",
        can_execute_now=False,
        requires_review=False,
        requires_permission=True,
        reason="permission required",
        recommended_response="state limitation",
        evidence_ids=["capability_decision_evidence:test"],
        created_at=now,
        decision_attrs={},
    )
    surface = CapabilityDecisionSurface(
        surface_id="capability_decision_surface:test",
        session_id="session:test",
        turn_id="conversation_turn:test",
        message_id="message:test",
        capability_snapshot_id="runtime_capability_snapshot:test",
        intent_id=intent.intent_id,
        decision_ids=[decision.decision_id],
        overall_availability="requires_permission",
        can_fulfill_now=False,
        recommended_agent_mode="requires_permission",
        limitation_summary="permission required",
        created_at=now,
        surface_attrs={},
    )

    intent_entry = capability_request_intents_to_history_entries([intent])[0]
    decision_entry = capability_decisions_to_history_entries([decision])[0]
    surface_entry = capability_decision_surfaces_to_history_entries([surface])[0]

    assert intent_entry.source == "capability_decision"
    assert decision_entry.priority == 90
    assert surface_entry.entry_attrs["can_fulfill_now"] is False
