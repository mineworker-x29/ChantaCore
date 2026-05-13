from chanta_core.observation_digest import DigestionService, ObservationService
from chanta_core.observation_digest.ids import new_agent_observation_batch_id
from chanta_core.ocel.store import OCELStore


def test_observation_and_digestion_emit_ocel_objects_events(tmp_path):
    store = OCELStore(tmp_path / "ocel.sqlite")
    observation = ObservationService(ocel_store=store)
    digestion = DigestionService(ocel_store=store)

    source = observation.inspect_observation_source(
        root_path=str(tmp_path),
        relative_path="missing.jsonl",
        source_runtime="dummy_runtime",
        format_hint="generic_jsonl",
    )
    events = observation.normalize_observation_records(
        [{"id": "one", "role": "user", "content": "hello"}],
        batch_id=new_agent_observation_batch_id(),
        source_runtime="dummy_runtime",
        source_format="generic_jsonl",
    )
    batch = observation.create_observation_batch(source=source, raw_record_count=1, normalized_events=events)
    run = observation.create_observed_run(source=source, batch=batch, normalized_events=events)
    inference = observation.infer_behavior(observed_run=run, normalized_events=events)
    observation.create_process_narrative(observed_run=run, inference=inference)

    skill_dir = tmp_path / "public_skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_bytes(b"# Public Dummy Skill\nDescription: public fixture.")
    descriptor = digestion.inspect_external_skill_source(
        root_path=str(tmp_path),
        relative_path="public_skill",
        vendor_hint="dummy_vendor",
    )
    profile = digestion.create_static_profile(
        source_descriptor=descriptor,
        root_path=str(tmp_path),
        relative_path="public_skill",
    )
    fingerprint = digestion.create_behavior_fingerprint(observed_run=run, normalized_events=events)
    candidate = digestion.create_assimilation_candidate(static_profile=profile, behavior_fingerprint=fingerprint)
    digestion.create_adapter_candidate(candidate=candidate)

    event_activities = {event["event_activity"] for event in store.fetch_recent_events(limit=50)}

    assert store.fetch_objects_by_type("agent_observation_source")
    assert store.fetch_objects_by_type("agent_observation_batch")
    assert store.fetch_objects_by_type("agent_observation_normalized_event")
    assert store.fetch_objects_by_type("observed_agent_run")
    assert store.fetch_objects_by_type("agent_behavior_inference")
    assert store.fetch_objects_by_type("agent_process_narrative")
    assert store.fetch_objects_by_type("external_skill_source_descriptor")
    assert store.fetch_objects_by_type("external_skill_static_profile")
    assert store.fetch_objects_by_type("external_skill_behavior_fingerprint")
    assert store.fetch_objects_by_type("external_skill_assimilation_candidate")
    assert store.fetch_objects_by_type("external_skill_adapter_candidate")
    assert "agent_observation_source_inspected" in event_activities
    assert "agent_observation_event_normalized" in event_activities
    assert "external_skill_assimilation_candidate_created" in event_activities
    assert store.fetch_object_object_relation_count() > 0
