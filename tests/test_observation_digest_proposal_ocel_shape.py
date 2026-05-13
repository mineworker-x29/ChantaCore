from chanta_core.ocel.store import OCELStore
from chanta_core.skills.observation_digest_proposal import ObservationDigestProposalService


def test_observation_digest_proposal_emits_ocel_shape(tmp_path):
    store = OCELStore(tmp_path / "proposal.sqlite")
    service = ObservationDigestProposalService(ocel_store=store)

    service.propose("이 JSONL 로그 보고 이 agent가 뭘 했는지 봐줘")

    event_activities = {event["event_activity"] for event in store.fetch_recent_events(limit=80)}
    assert store.fetch_objects_by_type("observation_digest_proposal_policy")
    assert store.fetch_objects_by_type("observation_digest_intent_candidate")
    assert store.fetch_objects_by_type("observation_digest_proposal_binding")
    assert store.fetch_objects_by_type("observation_digest_proposal_set")
    assert store.fetch_objects_by_type("observation_digest_proposal_finding")
    assert store.fetch_objects_by_type("observation_digest_proposal_result")
    assert "observation_digest_intent_classified" in event_activities
    assert "observation_digest_proposal_binding_created" in event_activities
    assert "observation_digest_proposal_set_created" in event_activities
    assert "observation_digest_proposal_result_recorded" in event_activities
    assert store.fetch_object_object_relation_count() > 0
