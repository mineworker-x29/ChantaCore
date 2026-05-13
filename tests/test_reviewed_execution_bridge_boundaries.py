from chanta_core.skills.execution_gate import SkillExecutionGateService
from chanta_core.skills.invocation import ExplicitSkillInvocationService
from chanta_core.skills.proposal import SkillInvocationProposal
from chanta_core.skills.proposal_review import SkillProposalReviewService
from chanta_core.skills.reviewed_execution_bridge import ReviewedExecutionBridgeService
from chanta_core.utility.time import utc_now_iso


class CountingGateService(SkillExecutionGateService):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.calls = 0

    def gate_explicit_invocation(self, **kwargs):
        self.calls += 1
        return super().gate_explicit_invocation(**kwargs)


def make_proposal(root_path: str, relative_path: str = "note.txt") -> SkillInvocationProposal:
    return SkillInvocationProposal(
        proposal_id="skill_invocation_proposal:boundary",
        intent_id="skill_proposal_intent:boundary",
        requirement_id="skill_proposal_requirement:boundary",
        skill_id="skill:read_workspace_text_file",
        proposal_status="proposed",
        invocation_mode="review_only",
        proposed_input_payload={"root_path": root_path, "relative_path": relative_path},
        missing_inputs=[],
        confidence=0.8,
        reason="boundary test",
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
        reason="approved",
    )
    return review_service.last_decision, review_result


def test_bridge_calls_execution_gate_and_uses_gate_for_invocation(tmp_path) -> None:
    (tmp_path / "note.txt").write_bytes(b"public-safe text")
    proposal = make_proposal(str(tmp_path))
    review_decision, review_result = approve(proposal)
    explicit_service = ExplicitSkillInvocationService()
    gate_service = CountingGateService(explicit_skill_invocation_service=explicit_service)
    service = ReviewedExecutionBridgeService(
        explicit_skill_invocation_service=explicit_service,
        skill_execution_gate_service=gate_service,
    )

    result = service.bridge_reviewed_proposal(
        proposal=proposal,
        review_decision=review_decision,
        review_result=review_result,
    )

    assert gate_service.calls == 1
    assert result.executed is True
    assert explicit_service.last_request is not None
    assert explicit_service.last_result.status == "completed"


def test_denied_bridge_never_calls_gate_or_invocation(tmp_path) -> None:
    proposal = make_proposal(str(tmp_path))
    review_service = SkillProposalReviewService()
    review_result = review_service.review_proposal(
        proposal=proposal,
        decision="reject",
        reviewer_type="human",
        reviewer_id="tester",
        reason="reject",
    )
    explicit_service = ExplicitSkillInvocationService()
    gate_service = CountingGateService(explicit_skill_invocation_service=explicit_service)
    service = ReviewedExecutionBridgeService(
        explicit_skill_invocation_service=explicit_service,
        skill_execution_gate_service=gate_service,
    )

    result = service.bridge_reviewed_proposal(
        proposal=proposal,
        review_decision=review_service.last_decision,
        review_result=review_result,
    )

    assert result.executed is False
    assert result.blocked is True
    assert gate_service.calls == 0
    assert explicit_service.last_request is None
    assert result.result_attrs["permission_grants_created"] is False
    assert result.result_attrs["natural_language_routing_used"] is False


def test_bridge_service_does_not_mutate_tool_or_skill_executor() -> None:
    service = ReviewedExecutionBridgeService()

    assert not hasattr(service, "tool_dispatcher")
    assert not hasattr(service, "skill_executor")
