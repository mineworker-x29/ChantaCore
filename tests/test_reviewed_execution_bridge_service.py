from chanta_core.execution import ExecutionEnvelopeService
from chanta_core.skills.proposal import SkillInvocationProposal
from chanta_core.skills.proposal_review import SkillProposalReviewService
from chanta_core.skills.reviewed_execution_bridge import ReviewedExecutionBridgeService
from chanta_core.utility.time import utc_now_iso


def make_proposal(
    *,
    root_path: str,
    relative_path: str = "note.txt",
    skill_id: str = "skill:read_workspace_text_file",
    missing_inputs: list[str] | None = None,
) -> SkillInvocationProposal:
    missing = list(missing_inputs or [])
    return SkillInvocationProposal(
        proposal_id=f"skill_invocation_proposal:{skill_id.replace(':', '_')}",
        intent_id="skill_proposal_intent:bridge",
        requirement_id="skill_proposal_requirement:bridge",
        skill_id=skill_id,
        proposal_status="incomplete" if missing else "proposed",
        invocation_mode="review_only",
        proposed_input_payload={"root_path": root_path, "relative_path": relative_path},
        missing_inputs=missing,
        confidence=0.8,
        reason="bridge test",
        review_required=True,
        executable_now=False,
        created_at=utc_now_iso(),
    )


def approve(proposal: SkillInvocationProposal):
    review_service = SkillProposalReviewService()
    result = review_service.review_proposal(
        proposal=proposal,
        decision="approve",
        reviewer_type="human",
        reviewer_id="tester",
        reason="approved read-only proposal",
    )
    return review_service.last_decision, result


def test_approved_read_workspace_text_file_bridges_to_gate_and_executes(tmp_path) -> None:
    (tmp_path / "note.txt").write_bytes(b"public-safe text")
    proposal = make_proposal(root_path=str(tmp_path))
    review_decision, review_result = approve(proposal)
    service = ReviewedExecutionBridgeService()

    result = service.bridge_reviewed_proposal(
        proposal=proposal,
        review_decision=review_decision,
        review_result=review_result,
    )

    assert result.status == "bridged_executed"
    assert result.executed is True
    assert result.blocked is False
    assert result.gate_result_id is not None
    assert result.explicit_invocation_result_id is not None
    assert service.skill_execution_gate_service.last_result.executed is True
    assert service.explicit_skill_invocation_service.last_result.status == "completed"


def test_gate_denial_blocks_bridge_execution(tmp_path) -> None:
    proposal = make_proposal(root_path=str(tmp_path), relative_path="..\\secret.txt")
    review_decision, review_result = approve(proposal)
    service = ReviewedExecutionBridgeService()

    result = service.bridge_reviewed_proposal(
        proposal=proposal,
        review_decision=review_decision,
        review_result=review_result,
    )

    assert result.status == "bridged_blocked"
    assert result.executed is False
    assert result.blocked is True
    assert result.gate_result_id is not None
    assert result.explicit_invocation_result_id is None


def test_non_approved_reviews_do_not_bridge(tmp_path) -> None:
    proposal = make_proposal(root_path=str(tmp_path))
    review_service = SkillProposalReviewService()
    bridge_service = ReviewedExecutionBridgeService()

    for decision in ["reject", "no-action", "more-input"]:
        review_result = review_service.review_proposal(
            proposal=proposal,
            decision=decision,
            reviewer_type="human",
            reviewer_id="tester",
            reason="not approved",
        )
        result = bridge_service.bridge_reviewed_proposal(
            proposal=proposal,
            review_decision=review_service.last_decision,
            review_result=review_result,
        )

        assert result.executed is False
        assert result.blocked is True
        assert result.gate_result_id is None


def test_missing_input_approved_review_still_does_not_execute(tmp_path) -> None:
    proposal = make_proposal(root_path=str(tmp_path), missing_inputs=["relative_path"])
    review_decision, review_result = approve(proposal)
    service = ReviewedExecutionBridgeService()

    result = service.bridge_reviewed_proposal(
        proposal=proposal,
        review_decision=review_decision,
        review_result=review_result,
    )

    assert result.status == "needs_more_input"
    assert result.executed is False
    assert result.blocked is True
    assert result.gate_result_id is None
    assert service.last_violations[0].violation_type in {
        "review_decision_not_bridgeable",
        "review_result_not_bridge_candidate",
        "missing_input",
    }


def test_unsupported_skill_categories_are_denied(tmp_path) -> None:
    for skill_id in [
        "skill:shell",
        "skill:network_request",
        "skill:write_file",
        "skill:mcp_connect",
        "skill:plugin_runtime",
    ]:
        proposal = make_proposal(root_path=str(tmp_path), skill_id=skill_id)
        review_decision, review_result = approve(proposal)
        service = ReviewedExecutionBridgeService()

        result = service.bridge_reviewed_proposal(
            proposal=proposal,
            review_decision=review_decision,
            review_result=review_result,
        )

        assert result.executed is False
        assert result.blocked is True
        assert result.gate_result_id is None
        assert service.last_violations


def test_execution_envelope_created_when_service_available(tmp_path) -> None:
    (tmp_path / "note.txt").write_bytes(b"public-safe text")
    proposal = make_proposal(root_path=str(tmp_path))
    review_decision, review_result = approve(proposal)
    envelope_service = ExecutionEnvelopeService()
    service = ReviewedExecutionBridgeService(execution_envelope_service=envelope_service)

    result = service.bridge_reviewed_proposal(
        proposal=proposal,
        review_decision=review_decision,
        review_result=review_result,
    )

    assert result.executed is True
    assert result.execution_envelope_id is not None
    assert envelope_service.last_envelope.envelope_id == result.execution_envelope_id
    assert envelope_service.last_provenance.proposal_id == proposal.proposal_id
    assert envelope_service.last_provenance.gate_result_id == result.gate_result_id
    assert envelope_service.last_provenance.explicit_invocation_result_id == result.explicit_invocation_result_id
