from chanta_core.ocel.store import OCELStore
from chanta_core.skills.registry_view import SkillRegistryViewService


def test_skill_registry_view_emits_ocel_objects_and_events(tmp_path):
    store = OCELStore(tmp_path / "registry.sqlite")
    service = SkillRegistryViewService(ocel_store=store)

    service.build_registry_view()
    filtered = service.apply_filter(skill_layer="internal_observation")
    service.record_result(command_name="observation", entries=filtered)
    service.render_registry_table(filtered)

    event_activities = {event["event_activity"] for event in store.fetch_recent_events(limit=80)}
    assert store.fetch_objects_by_type("skill_registry_view")
    assert store.fetch_objects_by_type("skill_registry_entry")
    assert store.fetch_objects_by_type("skill_registry_filter")
    assert store.fetch_objects_by_type("skill_registry_result")
    assert "skill_registry_view_created" in event_activities
    assert "skill_registry_entry_recorded" in event_activities
    assert "skill_registry_filter_applied" in event_activities
    assert "skill_registry_result_recorded" in event_activities
    assert "skill_registry_rendered" in event_activities
    assert store.fetch_object_object_relation_count() > 0
