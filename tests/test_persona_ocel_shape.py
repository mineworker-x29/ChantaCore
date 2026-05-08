from chanta_core.ocel.store import OCELStore
from chanta_core.persona import PersonaLoadingService
from chanta_core.traces.trace_service import TraceService


def test_persona_ocel_shape_contains_expected_objects_and_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "persona_shape.sqlite")
    service = PersonaLoadingService(trace_service=TraceService(ocel_store=store))
    bundle = service.create_default_agent_persona()
    service.render_projection_block(bundle.projection)

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}
    assert {
        "soul_identity_registered",
        "persona_profile_registered",
        "persona_instruction_artifact_registered",
        "agent_role_binding_registered",
        "persona_loadout_created",
        "persona_projection_created",
        "persona_projection_attached_to_prompt",
        "persona_capability_boundary_attached",
    }.issubset(activities)
    for object_type in [
        "soul_identity",
        "persona_profile",
        "persona_instruction_artifact",
        "agent_role_binding",
        "persona_loadout",
        "persona_projection",
    ]:
        assert store.fetch_objects_by_type(object_type)
