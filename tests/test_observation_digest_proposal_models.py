from chanta_core.skills.observation_digest_proposal import (
    ObservationDigestIntentCandidate,
    ObservationDigestProposalBinding,
    ObservationDigestProposalFinding,
    ObservationDigestProposalPolicy,
    ObservationDigestProposalResult,
    ObservationDigestProposalSet,
)
from chanta_core.utility.time import utc_now_iso


def test_observation_digest_proposal_models_to_dict_defaults():
    created_at = utc_now_iso()
    policy = ObservationDigestProposalPolicy(
        policy_id="observation_digest_proposal_policy:demo",
        policy_name="demo",
        allowed_skill_layers=["internal_observation"],
        allowed_skill_ids=["skill:agent_trace_observe"],
        denied_skill_ids=[],
        allow_multi_step_proposal=True,
        allow_execution=False,
        require_review=True,
        max_proposals_per_request=4,
        status="active",
        created_at=created_at,
    )
    intent = ObservationDigestIntentCandidate(
        intent_candidate_id="observation_digest_intent_candidate:demo",
        user_text_preview="public prompt",
        intent_family="observation",
        intent_name="agent_trace_observation",
        confidence=2.0,
        matched_terms=["jsonl"],
        suggested_skill_ids=["skill:agent_trace_observe"],
        missing_inputs=["root_path"],
        created_at=created_at,
    )
    binding = ObservationDigestProposalBinding(
        binding_id="observation_digest_proposal_binding:demo",
        intent_candidate_id=intent.intent_candidate_id,
        skill_id="skill:agent_trace_observe",
        proposal_id="skill_invocation_proposal:demo",
        binding_order=1,
        binding_reason="observation",
        required_inputs=["root_path"],
        provided_inputs={},
        missing_inputs=["root_path"],
        can_create_proposal=True,
        requires_review=True,
        created_at=created_at,
    )
    proposal_set = ObservationDigestProposalSet(
        proposal_set_id="observation_digest_proposal_set:demo",
        user_text_preview="public prompt",
        intent_candidate_ids=[intent.intent_candidate_id],
        proposal_ids=["skill_invocation_proposal:demo"],
        binding_ids=[binding.binding_id],
        family="observation",
        status="needs_more_input",
        requires_review=True,
        execution_performed=False,
        created_at=created_at,
    )
    finding = ObservationDigestProposalFinding(
        finding_id="observation_digest_proposal_finding:demo",
        proposal_set_id=proposal_set.proposal_set_id,
        intent_candidate_id=intent.intent_candidate_id,
        skill_id="skill:agent_trace_observe",
        finding_type="missing_required_input",
        status="needs_more_input",
        severity="medium",
        message="Missing root.",
        subject_ref=None,
        created_at=created_at,
    )
    result = ObservationDigestProposalResult(
        result_id="observation_digest_proposal_result:demo",
        proposal_set_id=proposal_set.proposal_set_id,
        status="needs_more_input",
        created_proposal_count=1,
        finding_ids=[finding.finding_id],
        summary="Demo result.",
        execution_performed=False,
        review_required=True,
        created_at=created_at,
    )

    assert policy.to_dict()["allow_execution"] is False
    assert intent.confidence == 1.0
    assert binding.to_dict()["requires_review"] is True
    assert proposal_set.to_dict()["execution_performed"] is False
    assert finding.to_dict()["finding_type"] == "missing_required_input"
    assert result.to_dict()["review_required"] is True
