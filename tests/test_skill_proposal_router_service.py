from chanta_core.skills.proposal import SkillProposalRouterService


def test_read_file_prompt_proposes_workspace_read_skill() -> None:
    service = SkillProposalRouterService()

    result = service.propose_from_prompt(
        user_prompt="read file docs/example.txt",
        root_path="<WORKSPACE_ROOT>",
    )

    proposal = service.last_proposals[0]
    decision = service.last_decisions[0]
    assert result.status == "proposal_available"
    assert proposal.skill_id == "skill:read_workspace_text_file"
    assert proposal.executable_now is False
    assert decision.can_execute_now is False
    assert decision.requires_explicit_invocation is True
    assert "chanta-cli skill run skill:read_workspace_text_file" in result.suggested_cli_command


def test_missing_root_or_path_produces_incomplete_proposal() -> None:
    service = SkillProposalRouterService()

    result = service.propose_from_prompt(user_prompt="read file")

    proposal = service.last_proposals[0]
    note_types = {note.note_type for note in service.last_review_notes}
    assert result.status == "incomplete"
    assert proposal.proposal_status == "incomplete"
    assert set(proposal.missing_inputs) == {"root_path", "relative_path"}
    assert "missing_input" in note_types


def test_unsupported_shell_prompt_is_controlled() -> None:
    service = SkillProposalRouterService()

    result = service.propose_from_prompt(user_prompt="run powershell command")

    proposal = service.last_proposals[0]
    decision = service.last_decisions[0]
    assert result.status == "unsupported"
    assert proposal.proposal_status == "unsupported"
    assert decision.decision == "unsupported_capability"
    assert proposal.executable_now is False
    assert result.suggested_cli_command is None


def test_router_does_not_call_invocation_service() -> None:
    class InvocationProbe:
        called = False

        def invoke_explicit_skill(self, **_) -> None:
            self.called = True
            raise AssertionError("proposal router must not invoke skills")

    probe = InvocationProbe()
    service = SkillProposalRouterService(explicit_skill_invocation_service=probe)

    service.propose_from_prompt(
        user_prompt="read file docs/example.txt",
        root_path="<WORKSPACE_ROOT>",
    )

    assert probe.called is False
