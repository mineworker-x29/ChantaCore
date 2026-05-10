from chanta_core.skills.proposal import (
    SkillInvocationProposal,
    SkillProposalDecision,
    SkillProposalIntent,
    SkillProposalRequirement,
    SkillProposalResult,
    SkillProposalReviewNote,
)
from chanta_core.utility.time import utc_now_iso


def test_skill_proposal_models_to_dict() -> None:
    now = utc_now_iso()
    intent = SkillProposalIntent(
        intent_id="skill_proposal_intent:test",
        user_prompt_preview="read file docs/example.md",
        session_id="session:test",
        turn_id="turn:test",
        message_id="message:test",
        requested_operation="workspace_file_read",
        target_refs=[{"target_type": "relative_path", "target_ref": "docs/example.md"}],
        created_at=now,
        intent_attrs={"deterministic_heuristic": True},
    )
    requirement = SkillProposalRequirement(
        requirement_id="skill_proposal_requirement:test",
        intent_id=intent.intent_id,
        requirement_type="capability_requirement",
        capability_name="workspace_file_read",
        capability_category="workspace_read",
        required_inputs=["root_path", "relative_path"],
        missing_inputs=["root_path"],
        target_type="relative_path",
        target_ref="docs/example.md",
        required_now=True,
        reason="test",
        created_at=now,
    )
    proposal = SkillInvocationProposal(
        proposal_id="skill_invocation_proposal:test",
        intent_id=intent.intent_id,
        requirement_id=requirement.requirement_id,
        skill_id="skill:read_workspace_text_file",
        proposal_status="incomplete",
        invocation_mode="review_only",
        proposed_input_payload={"root_path": "<ROOT_PATH>", "relative_path": "docs/example.md"},
        missing_inputs=["root_path"],
        confidence=0.74,
        reason="test",
        review_required=True,
        executable_now=False,
        created_at=now,
    )
    decision = SkillProposalDecision(
        decision_id="skill_proposal_decision:test",
        intent_id=intent.intent_id,
        proposal_id=proposal.proposal_id,
        decision="needs_more_input",
        decision_basis="missing_required_input",
        selected_skill_id=proposal.skill_id,
        can_execute_now=False,
        requires_explicit_invocation=True,
        requires_review=True,
        requires_permission=False,
        reason="test",
        created_at=now,
    )
    note = SkillProposalReviewNote(
        review_note_id="skill_proposal_review_note:test",
        intent_id=intent.intent_id,
        proposal_id=proposal.proposal_id,
        note_type="missing_input",
        severity="medium",
        message="root_path is required",
        created_at=now,
    )
    result = SkillProposalResult(
        result_id="skill_proposal_result:test",
        intent_id=intent.intent_id,
        proposal_ids=[proposal.proposal_id],
        decision_ids=[decision.decision_id],
        review_note_ids=[note.review_note_id],
        status="incomplete",
        summary="test",
        suggested_cli_command="chanta-cli skill run skill:read_workspace_text_file",
        created_at=now,
    )

    assert intent.to_dict()["requested_operation"] == "workspace_file_read"
    assert requirement.to_dict()["missing_inputs"] == ["root_path"]
    assert proposal.to_dict()["executable_now"] is False
    assert decision.to_dict()["can_execute_now"] is False
    assert note.to_dict()["note_type"] == "missing_input"
    assert result.to_dict()["status"] == "incomplete"
