from chanta_core.skills.history_adapter import (
    reviewed_execution_bridge_decisions_to_history_entries,
    reviewed_execution_bridge_requests_to_history_entries,
    reviewed_execution_bridge_results_to_history_entries,
    reviewed_execution_bridge_violations_to_history_entries,
)
from chanta_core.skills.proposal import SkillInvocationProposal
from chanta_core.skills.proposal_review import SkillProposalReviewService
from chanta_core.skills.reviewed_execution_bridge import ReviewedExecutionBridgeService
from chanta_core.utility.time import utc_now_iso


def make_proposal() -> SkillInvocationProposal:
    return SkillInvocationProposal(
        proposal_id="skill_invocation_proposal:history_bridge",
        intent_id="skill_proposal_intent:history_bridge",
        requirement_id="skill_proposal_requirement:history_bridge",
        skill_id="skill:shell",
        proposal_status="unsupported",
        invocation_mode="review_only",
        proposed_input_payload={},
        missing_inputs=[],
        confidence=0.2,
        reason="unsupported",
        review_required=True,
        executable_now=False,
        created_at=utc_now_iso(),
    )


def test_reviewed_execution_bridge_history_entries() -> None:
    proposal = make_proposal()
    review_service = SkillProposalReviewService()
    review_result = review_service.review_proposal(
        proposal=proposal,
        decision="approve",
        reviewer_type="human",
        reviewer_id="tester",
        reason="try approve",
    )
    bridge_service = ReviewedExecutionBridgeService()
    result = bridge_service.bridge_reviewed_proposal(
        proposal=proposal,
        review_decision=review_service.last_decision,
        review_result=review_result,
    )

    request_entries = reviewed_execution_bridge_requests_to_history_entries([bridge_service.last_request])
    decision_entries = reviewed_execution_bridge_decisions_to_history_entries([bridge_service.last_decision])
    result_entries = reviewed_execution_bridge_results_to_history_entries([result])
    violation_entries = reviewed_execution_bridge_violations_to_history_entries(
        bridge_service.last_violations
    )

    assert request_entries[0].source == "reviewed_execution_bridge"
    assert decision_entries[0].priority >= 80
    assert result_entries[0].entry_attrs["blocked"] is True
    assert violation_entries[0].entry_attrs["severity"] == "high"
