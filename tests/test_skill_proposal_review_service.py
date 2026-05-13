from chanta_core.skills.proposal import SkillInvocationProposal
from chanta_core.skills.proposal_review import SkillProposalReviewService
from chanta_core.utility.time import utc_now_iso


def make_proposal(
    *,
    skill_id: str = "skill:read_workspace_text_file",
    missing_inputs: list[str] | None = None,
    payload: dict[str, object] | None = None,
) -> SkillInvocationProposal:
    missing = list(missing_inputs or [])
    return SkillInvocationProposal(
        proposal_id="skill_invocation_proposal:test",
        intent_id="skill_proposal_intent:test",
        requirement_id="skill_proposal_requirement:test",
        skill_id=skill_id,
        proposal_status="incomplete" if missing else "proposed",
        invocation_mode="review_only",
        proposed_input_payload=payload
        or {"root_path": "<WORKSPACE_ROOT>", "relative_path": "docs/example.txt"},
        missing_inputs=missing,
        confidence=0.86,
        reason="test proposal",
        review_required=True,
        executable_now=False,
        created_at=utc_now_iso(),
    )


def test_default_contract_supports_read_only_workspace_family_only() -> None:
    contract = SkillProposalReviewService().create_default_contract()

    assert contract.supported_skill_ids == [
        "skill:list_workspace_files",
        "skill:read_workspace_text_file",
        "skill:summarize_workspace_markdown",
    ]
    assert "shell" in contract.denied_skill_categories
    assert "write" in contract.denied_skill_categories


def test_complete_read_workspace_proposal_can_be_approved_as_bridge_candidate() -> None:
    service = SkillProposalReviewService()

    result = service.review_proposal(
        proposal=make_proposal(),
        decision="approved_for_explicit_invocation",
        reviewer_type="human",
        reviewer_id="tester",
        reason="complete read-only proposal",
    )

    assert result.status == "approved"
    assert result.bridge_candidate is True
    assert service.last_decision is not None
    assert service.last_decision.requires_explicit_invocation is True
    assert service.last_decision.can_bridge_to_execution is True


def test_approved_result_records_no_execution() -> None:
    service = SkillProposalReviewService()

    result = service.review_proposal(
        proposal=make_proposal(),
        decision="approve",
        reviewer_type="human",
        reviewer_id="tester",
        reason="complete read-only proposal",
    )

    assert result.result_attrs["skills_executed"] is False
    assert result.result_attrs["permission_grants_created"] is False
    assert result.result_attrs["execution_bridge_created"] is False
    assert service.last_decision is not None
    assert service.last_decision.decision_attrs["skills_executed"] is False


def test_missing_input_approval_becomes_needs_more_input() -> None:
    service = SkillProposalReviewService()

    result = service.review_proposal(
        proposal=make_proposal(missing_inputs=["root_path"]),
        decision="approve",
        reviewer_type="human",
        reviewer_id="tester",
        reason="try approve",
    )

    assert result.status == "needs_more_input"
    assert result.bridge_candidate is False
    assert service.last_decision is not None
    assert service.last_decision.can_bridge_to_execution is False
    assert any(finding.finding_type == "missing_input" for finding in service.last_findings)


def test_reject_and_no_action_do_not_create_bridge_candidate() -> None:
    service = SkillProposalReviewService()

    rejected = service.review_proposal(
        proposal=make_proposal(),
        decision="reject",
        reviewer_type="human",
        reviewer_id="tester",
        reason="not needed",
    )
    no_action = service.review_proposal(
        proposal=make_proposal(),
        decision="no-action",
        reviewer_type="human",
        reviewer_id="tester",
        reason="do nothing",
    )

    assert rejected.status == "rejected"
    assert rejected.bridge_candidate is False
    assert no_action.status == "no_action"
    assert no_action.bridge_candidate is False


def test_revise_and_needs_more_input_decisions_work() -> None:
    service = SkillProposalReviewService()

    revise = service.review_proposal(
        proposal=make_proposal(),
        decision="revise",
        reviewer_type="human",
        reviewer_id="tester",
        reason="change path",
        revised_input_payload={"root_path": "<WORKSPACE_ROOT>", "relative_path": "docs/revised.txt"},
    )
    more_input = service.review_proposal(
        proposal=make_proposal(missing_inputs=["relative_path"]),
        decision="more-input",
        reviewer_type="human",
        reviewer_id="tester",
        reason="missing path",
    )

    assert revise.status == "revise_proposal"
    assert revise.bridge_candidate is False
    assert more_input.status == "needs_more_input"
    assert more_input.bridge_candidate is False


def test_shell_network_write_mcp_plugin_proposals_are_rejected() -> None:
    for skill_id in [
        "skill:shell",
        "skill:network_request",
        "skill:write_file",
        "skill:mcp_connect",
        "skill:plugin_runtime",
    ]:
        service = SkillProposalReviewService()
        result = service.review_proposal(
            proposal=make_proposal(skill_id=skill_id),
            decision="approve",
            reviewer_type="human",
            reviewer_id="tester",
            reason="try approve",
        )

        assert result.status == "rejected"
        assert result.bridge_candidate is False
        assert service.last_findings
