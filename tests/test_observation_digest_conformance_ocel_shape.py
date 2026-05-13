from chanta_core.ocel.store import OCELStore
from chanta_core.skills.observation_digest_conformance import ObservationDigestConformanceService


def test_observation_digest_conformance_emits_ocel_shape(tmp_path):
    store = OCELStore(tmp_path / "conformance.sqlite")
    service = ObservationDigestConformanceService(ocel_store=store)

    service.run_conformance(skill_id="skill:agent_trace_observe")

    event_activities = {event["event_activity"] for event in store.fetch_recent_events(limit=120)}
    assert store.fetch_objects_by_type("observation_digest_conformance_policy")
    assert store.fetch_objects_by_type("observation_digest_conformance_check")
    assert store.fetch_objects_by_type("observation_digest_conformance_report")
    assert "observation_digest_conformance_policy_registered" in event_activities
    assert "observation_digest_conformance_check_completed" in event_activities
    assert "observation_digest_conformance_report_recorded" in event_activities
    assert store.fetch_event_object_relation_count() > 0
