from chanta_core.skills.proposal import SkillInvocationProposal
from chanta_core.skills.history_adapter import (
    skill_proposal_review_decisions_to_history_entries,
    skill_proposal_review_findings_to_history_entries,
    skill_proposal_review_requests_to_history_entries,
    skill_proposal_review_results_to_history_entries,
)
from chanta_core.skills.proposal_review import SkillProposalReviewService
from chanta_core.utility.time import utc_now_iso


def make_proposal() -> SkillInvocationProposal:
    return SkillInvocationProposal(
        proposal_id="skill_invocation_proposal:history",
        intent_id="skill_proposal_intent:history",
        requirement_id="skill_proposal_requirement:history",
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


def test_skill_proposal_review_history_entries_use_expected_source_and_priority() -> None:
    service = SkillProposalReviewService()
    result = service.review_proposal(
        proposal=make_proposal(),
        decision="approve",
        reviewer_type="human",
        reviewer_id="tester",
        reason="try approve",
    )

    request_entries = skill_proposal_review_requests_to_history_entries([service.last_request])
    decision_entries = skill_proposal_review_decisions_to_history_entries([service.last_decision])
    result_entries = skill_proposal_review_results_to_history_entries([result])
    finding_entries = skill_proposal_review_findings_to_history_entries(service.last_findings)

    assert request_entries[0].source == "skill_proposal_review"
    assert decision_entries[0].entry_attrs["can_bridge_to_execution"] is False
    assert result_entries[0].priority >= 80
    assert finding_entries[0].priority >= 80
    assert finding_entries[0].entry_attrs["status"] == "failed"
