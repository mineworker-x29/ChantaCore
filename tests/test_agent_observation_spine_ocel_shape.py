from chanta_core.observation import AgentObservationSpineService
from chanta_core.ocel.store import OCELStore


def test_spine_emits_ocel_objects_and_events() -> None:
    store = OCELStore()
    service = AgentObservationSpineService(ocel_store=store)
    service.create_default_policy()
    service.register_collector_contracts()
    service.register_adapter_profiles()
    service.register_movement_ontology_terms()
    service.normalize_event_v2({"id": "u1", "role": "user", "content": "hello"})
    service.create_redaction_policy()
    service.create_export_policy()
    service.create_fleet_snapshot()

    assert store.fetch_objects_by_type("agent_observation_spine_policy")
    assert store.fetch_objects_by_type("agent_observation_collector_contract")
    assert store.fetch_objects_by_type("agent_observation_adapter_profile")
    assert store.fetch_objects_by_type("agent_movement_ontology_term")
    assert store.fetch_objects_by_type("agent_observation_normalized_event_v2")
    assert store.fetch_objects_by_type("observation_redaction_policy")
    assert store.fetch_objects_by_type("observation_export_policy")
    activities = {row["event_activity"] for row in store.fetch_recent_events(limit=50)}
    assert "agent_observation_event_v2_normalized" in activities
    assert "agent_fleet_observation_snapshot_created" in activities
