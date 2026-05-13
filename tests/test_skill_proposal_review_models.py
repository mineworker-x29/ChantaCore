from chanta_core.skills.proposal_review import (
    SkillProposalReviewContract,
    SkillProposalReviewDecision,
    SkillProposalReviewFinding,
    SkillProposalReviewRequest,
    SkillProposalReviewResult,
)
from chanta_core.utility.time import utc_now_iso


def test_skill_proposal_review_models_to_dict() -> None:
    now = utc_now_iso()
    contract = SkillProposalReviewContract(
        contract_id="skill_proposal_review_contract:test",
        contract_name="default",
        contract_type="human_in_the_loop",
        description="review only",
        allowed_decisions=["approved_for_explicit_invocation", "no_action"],
        supported_skill_ids=["skill:read_workspace_text_file"],
        denied_skill_categories=["shell"],
        require_explicit_reviewer=True,
        require_reason_for_approval=True,
        require_reason_for_rejection=False,
        status="active",
        created_at=now,
        updated_at=now,
    )
    request = SkillProposalReviewRequest(
        review_request_id="skill_proposal_review_request:test",
        contract_id=contract.contract_id,
        proposal_id="skill_invocation_proposal:test",
        intent_id="skill_proposal_intent:test",
        requirement_id="skill_proposal_requirement:test",
        skill_id="skill:read_workspace_text_file",
        proposed_input_preview={"relative_path": "docs/example.txt"},
        missing_inputs=[],
        requested_by="tester",
        session_id="session:test",
        turn_id="turn:test",
        process_instance_id="process:test",
        status="created",
        created_at=now,
    )
    decision = SkillProposalReviewDecision(
        review_decision_id="skill_proposal_review_decision:test",
        review_request_id=request.review_request_id,
        proposal_id=request.proposal_id,
        decision="approved_for_explicit_invocation",
        reviewer_type="human",
        reviewer_id="tester",
        reason="safe read-only input",
        approved_input_payload={"root_path": "<ROOT>", "relative_path": "docs/example.txt"},
        revised_input_payload=None,
        requires_explicit_invocation=True,
        can_bridge_to_execution=True,
        expires_at=None,
        created_at=now,
    )
    finding = SkillProposalReviewFinding(
        finding_id="skill_proposal_review_finding:test",
        review_request_id=request.review_request_id,
        proposal_id=request.proposal_id,
        finding_type="missing_input",
        status="failed",
        severity="high",
        message="missing",
        subject_ref="root_path",
        created_at=now,
    )
    result = SkillProposalReviewResult(
        review_result_id="skill_proposal_review_result:test",
        review_request_id=request.review_request_id,
        proposal_id=request.proposal_id,
        decision_id=decision.review_decision_id,
        finding_ids=[finding.finding_id],
        status="approved",
        summary="test",
        bridge_candidate=True,
        created_at=now,
    )

    assert contract.to_dict()["require_explicit_reviewer"] is True
    assert request.to_dict()["skill_id"] == "skill:read_workspace_text_file"
    assert decision.to_dict()["can_bridge_to_execution"] is True
    assert finding.to_dict()["finding_type"] == "missing_input"
    assert result.to_dict()["bridge_candidate"] is True
