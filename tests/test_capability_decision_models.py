from chanta_core.capabilities import (
    CapabilityDecision,
    CapabilityDecisionEvidence,
    CapabilityDecisionSurface,
    CapabilityRequestIntent,
    CapabilityRequirement,
    new_capability_decision_evidence_id,
    new_capability_decision_id,
    new_capability_decision_surface_id,
    new_capability_request_intent_id,
    new_capability_requirement_id,
)
from chanta_core.utility.time import utc_now_iso


def test_capability_decision_models_to_dict_and_prefixes() -> None:
    now = utc_now_iso()
    intent = CapabilityRequestIntent(
        intent_id=new_capability_request_intent_id(),
        session_id="session:test",
        turn_id="conversation_turn:test",
        message_id="message:test",
        user_prompt_preview="read file",
        requested_operation="workspace_file_read",
        target_refs=[{"type": "path_hint", "ref": "<PERSONAL_DIRECTORY>/source/test.md"}],
        inferred_requirement_ids=[],
        created_at=now,
        intent_attrs={},
    )
    requirement = CapabilityRequirement(
        requirement_id=new_capability_requirement_id(),
        requirement_type="workspace_file_read",
        capability_name="workspace file read",
        capability_category="workspace",
        target_type="path_hint",
        target_ref="<PERSONAL_DIRECTORY>/source/test.md",
        required_now=True,
        reason="test",
        created_at=now,
        requirement_attrs={},
    )
    decision = CapabilityDecision(
        decision_id=new_capability_decision_id(),
        intent_id=intent.intent_id,
        requirement_id=requirement.requirement_id,
        capability_name=requirement.capability_name,
        availability="requires_permission",
        can_execute_now=False,
        requires_review=False,
        requires_permission=True,
        reason="workspace read unavailable",
        recommended_response="ask for pasted content",
        evidence_ids=[],
        created_at=now,
        decision_attrs={},
    )
    surface = CapabilityDecisionSurface(
        surface_id=new_capability_decision_surface_id(),
        session_id="session:test",
        turn_id="conversation_turn:test",
        message_id="message:test",
        capability_snapshot_id="runtime_capability_snapshot:test",
        intent_id=intent.intent_id,
        decision_ids=[decision.decision_id],
        overall_availability="requires_permission",
        can_fulfill_now=False,
        recommended_agent_mode="ask_for_pasted_content",
        limitation_summary="workspace read unavailable",
        created_at=now,
        surface_attrs={},
    )
    evidence = CapabilityDecisionEvidence(
        evidence_id=new_capability_decision_evidence_id(),
        decision_id=decision.decision_id,
        evidence_type="runtime_capability_snapshot",
        source_kind="runtime_capability_snapshot",
        source_ref="runtime_capability_snapshot:test",
        content="snapshot evidence",
        created_at=now,
        evidence_attrs={},
    )

    assert intent.to_dict()["intent_id"].startswith("capability_request_intent:")
    assert requirement.to_dict()["requirement_id"].startswith("capability_requirement:")
    assert decision.to_dict()["decision_id"].startswith("capability_decision:")
    assert surface.to_dict()["surface_id"].startswith("capability_decision_surface:")
    assert evidence.to_dict()["evidence_id"].startswith("capability_decision_evidence:")
    assert decision.can_execute_now is False
    assert surface.can_fulfill_now is False
