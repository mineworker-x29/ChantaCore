from chanta_core.skills.proposal import SkillInvocationProposal
from chanta_core.skills.proposal_review import SkillProposalReviewService
from chanta_core.skills.reviewed_execution_bridge import ReviewedExecutionBridgeService
from chanta_core.utility.time import utc_now_iso


def make_proposal(skill_id: str, payload: dict[str, object]) -> SkillInvocationProposal:
    return SkillInvocationProposal(
        proposal_id=f"skill_invocation_proposal:{skill_id.replace(':', '_')}",
        intent_id="skill_proposal_intent:workspace",
        requirement_id="skill_proposal_requirement:workspace",
        skill_id=skill_id,
        proposal_status="proposed",
        invocation_mode="review_only",
        proposed_input_payload=dict(payload),
        missing_inputs=[],
        confidence=0.8,
        reason="workspace read bridge",
        review_required=True,
        executable_now=False,
        created_at=utc_now_iso(),
    )


def approve(proposal: SkillInvocationProposal):
    review_service = SkillProposalReviewService()
    review_result = review_service.review_proposal(
        proposal=proposal,
        decision="approve",
        reviewer_type="human",
        reviewer_id="tester",
        reason="approved read-only proposal",
    )
    return review_service.last_decision, review_result


def test_list_workspace_files_bridge_executes(tmp_path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "note.txt").write_bytes(b"public-safe text")
    proposal = make_proposal(
        "skill:list_workspace_files",
        {"root_path": str(tmp_path), "relative_path": "docs"},
    )
    review_decision, review_result = approve(proposal)

    result = ReviewedExecutionBridgeService().bridge_reviewed_proposal(
        proposal=proposal,
        review_decision=review_decision,
        review_result=review_result,
    )

    assert result.executed is True
    assert result.blocked is False


def test_summarize_workspace_markdown_bridge_executes(tmp_path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "note.md").write_bytes(b"# Title\n\nPublic-safe body")
    proposal = make_proposal(
        "skill:summarize_workspace_markdown",
        {"root_path": str(tmp_path), "relative_path": "docs/note.md"},
    )
    review_decision, review_result = approve(proposal)

    result = ReviewedExecutionBridgeService().bridge_reviewed_proposal(
        proposal=proposal,
        review_decision=review_decision,
        review_result=review_result,
    )

    assert result.executed is True
    assert result.blocked is False


def test_workspace_boundary_denial_blocks_bridge(tmp_path) -> None:
    proposal = make_proposal(
        "skill:read_workspace_text_file",
        {"root_path": str(tmp_path), "relative_path": "..\\outside.txt"},
    )
    review_decision, review_result = approve(proposal)

    result = ReviewedExecutionBridgeService().bridge_reviewed_proposal(
        proposal=proposal,
        review_decision=review_decision,
        review_result=review_result,
    )

    assert result.executed is False
    assert result.blocked is True
    assert result.gate_result_id is not None
