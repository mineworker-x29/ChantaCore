from chanta_core.observation_digest import ObservationDigestionEcosystemConsolidationService
from chanta_core.ocel.store import OCELStore


def test_ecosystem_ocel_objects_events_emitted(tmp_path) -> None:
    store = OCELStore(tmp_path / "ecosystem.sqlite")
    service = ObservationDigestionEcosystemConsolidationService(ocel_store=store)
    service.consolidate()
    events = store.fetch_recent_events(80)

    assert store.fetch_object_count() >= 8
    activities = {event["event_activity"] for event in events}
    assert "observation_digestion_ecosystem_snapshot_created" in activities
    assert "observation_digestion_ecosystem_component_recorded" in activities
    assert "observation_digestion_capability_map_created" in activities
    assert "observation_digestion_safety_boundary_report_created" in activities
    assert "observation_digestion_gap_registered" in activities
    assert "observation_digestion_release_manifest_created" in activities
    assert "observation_digestion_consolidation_report_recorded" in activities

