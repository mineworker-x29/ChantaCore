from chanta_core.skills.proposal import SkillInvocationProposal
from chanta_core.skills.proposal_review import SkillProposalReviewService
from chanta_core.utility.time import utc_now_iso


def make_proposal(skill_id: str = "skill:read_workspace_text_file") -> SkillInvocationProposal:
    return SkillInvocationProposal(
        proposal_id="skill_invocation_proposal:boundary",
        intent_id="skill_proposal_intent:boundary",
        requirement_id="skill_proposal_requirement:boundary",
        skill_id=skill_id,
        proposal_status="proposed",
        invocation_mode="review_only",
        proposed_input_payload={"root_path": "<WORKSPACE_ROOT>", "relative_path": "docs/example.txt"},
        missing_inputs=[],
        confidence=0.8,
        reason="boundary test",
        review_required=True,
        executable_now=False,
        created_at=utc_now_iso(),
    )


def test_review_service_has_no_invocation_or_gate_dependency() -> None:
    service = SkillProposalReviewService()

    assert not hasattr(service, "explicit_skill_invocation_service")
    assert not hasattr(service, "skill_execution_gate_service")


def test_review_does_not_create_invocation_or_gate_state() -> None:
    service = SkillProposalReviewService()

    result = service.review_proposal(
        proposal=make_proposal(),
        decision="approve",
        reviewer_type="human",
        reviewer_id="tester",
        reason="review only",
    )

    assert result.status == "approved"
    assert result.result_attrs["skills_executed"] is False
    assert result.result_attrs["execution_bridge_created"] is False
    assert service.last_decision is not None
    assert service.last_decision.decision_attrs["execution_bridge_created"] is False


def test_review_creates_no_permission_grants_or_automatic_execution() -> None:
    service = SkillProposalReviewService()

    result = service.review_proposal(
        proposal=make_proposal(),
        decision="approve",
        reviewer_type="human",
        reviewer_id="tester",
        reason="review only",
    )

    assert result.bridge_candidate is True
    assert result.result_attrs["permission_grants_created"] is False
    assert result.result_attrs["skills_executed"] is False
    assert result.result_attrs["execution_bridge_created"] is False
    assert service.last_decision is not None
    assert service.last_decision.decision_attrs["execution_bridge_created"] is False
