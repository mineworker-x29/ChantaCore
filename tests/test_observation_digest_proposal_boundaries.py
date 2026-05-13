from chanta_core.skills.observation_digest_proposal import ObservationDigestProposalService


def test_observation_digest_proposal_keeps_runtime_inactive():
    service = ObservationDigestProposalService()

    result = service.propose("이 JSONL 로그 보고 이 agent가 뭘 했는지 봐줘")

    assert result.execution_performed is False
    assert result.review_required is True
    assert service.last_set.execution_performed is False
    assert all(proposal.executable_now is False for proposal in service.last_skill_proposals)
    assert all(proposal.review_required is True for proposal in service.last_skill_proposals)
    assert service.last_policy.allow_execution is False
    assert service.last_policy.policy_attrs["permission_grants_created"] is False


def test_observation_digest_proposal_does_not_enable_external_candidates():
    service = ObservationDigestProposalService()

    service.propose("external skill 후보로 assimilate 해줘")

    assert all(
        proposal.proposal_attrs["execution_performed"] is False
        for proposal in service.last_skill_proposals
    )
