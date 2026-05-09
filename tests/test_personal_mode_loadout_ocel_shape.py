from chanta_core.ocel.store import OCELStore
from chanta_core.persona import PersonalModeLoadoutService
from chanta_core.traces.trace_service import TraceService


def test_personal_mode_loadout_ocel_shape_contains_expected_objects_and_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "personal_mode_loadout.sqlite")
    service = PersonalModeLoadoutService(trace_service=TraceService(ocel_store=store))
    core = service.register_core_profile(
        profile_name="dummy_personal_profile",
        profile_type="assistant",
        identity_statement="A public-safe assistant identity.",
    )
    mode = service.register_mode_profile(
        core_profile_id=core.core_profile_id,
        mode_name="local_runtime_mode",
        mode_type="local_runtime_mode",
        role_statement="Use only explicitly bound local runtime capabilities.",
    )
    boundary = service.register_mode_boundary(
        mode_profile_id=mode.mode_profile_id,
        boundary_type="runtime_boundary",
        boundary_text="No ambient shell, network, or plugin access.",
        severity="high",
    )
    binding = service.register_capability_binding(
        mode_profile_id=mode.mode_profile_id,
        capability_name="local_runtime_access",
        capability_category="runtime",
        availability="available_via_explicit_skill",
        can_execute_now=False,
        requires_permission=True,
    )
    loadout = service.create_mode_loadout(
        core_profile=core,
        mode_profile=mode,
        boundaries=[boundary],
        capability_bindings=[binding],
    )
    service.create_mode_loadout_draft(
        core_profile=core,
        mode_profile=mode,
        projected_blocks=[{"kind": "loadout", "content": loadout.loadout_name}],
    )

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}

    for object_type in [
        "personal_core_profile",
        "personal_mode_profile",
        "personal_mode_boundary",
        "personal_mode_capability_binding",
        "personal_mode_loadout",
        "personal_mode_loadout_draft",
    ]:
        assert store.fetch_objects_by_type(object_type)
    assert {
        "personal_core_profile_registered",
        "personal_mode_profile_registered",
        "personal_mode_boundary_registered",
        "personal_mode_capability_binding_registered",
        "personal_mode_loadout_created",
        "personal_mode_loadout_draft_created",
        "personal_mode_capability_boundary_attached",
    }.issubset(activities)
