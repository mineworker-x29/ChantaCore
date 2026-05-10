from chanta_core.skills.proposal import SkillProposalRouterService


def test_list_files_prompt_proposes_workspace_list_skill() -> None:
    service = SkillProposalRouterService()

    result = service.propose_from_prompt(
        user_prompt="list files in this folder",
        root_path="<WORKSPACE_ROOT>",
        recursive=True,
    )

    proposal = service.last_proposals[0]
    assert result.status == "proposal_available"
    assert proposal.skill_id == "skill:list_workspace_files"
    assert proposal.proposed_input_payload["relative_path"] == "."
    assert proposal.proposed_input_payload["recursive"] is True


def test_markdown_summary_prompt_proposes_markdown_summary_skill() -> None:
    service = SkillProposalRouterService()

    result = service.propose_from_prompt(
        user_prompt="문서 요약 docs/guide.md",
        root_path="<WORKSPACE_ROOT>",
    )

    proposal = service.last_proposals[0]
    assert result.status == "proposal_available"
    assert proposal.skill_id == "skill:summarize_workspace_markdown"
    assert proposal.proposed_input_payload["relative_path"] == "docs/guide.md"


def test_write_and_network_prompts_are_unsupported() -> None:
    service = SkillProposalRouterService()

    write_result = service.propose_from_prompt(user_prompt="edit file docs/guide.md")
    network_result = service.propose_from_prompt(user_prompt="웹 요청 https://example.invalid")

    assert write_result.status == "unsupported"
    assert network_result.status == "unsupported"
