from chanta_core.ocel.store import OCELStore
from chanta_core.persona import PersonalModeBindingService, PersonalModeLoadoutService
from chanta_core.traces.trace_service import TraceService


def test_personal_mode_binding_ocel_shape_contains_expected_objects_and_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "personal_mode_binding.sqlite")
    trace_service = TraceService(ocel_store=store)
    loadout_service = PersonalModeLoadoutService(trace_service=trace_service)
    core = loadout_service.register_core_profile(
        profile_name="sample_personal_assistant",
        profile_type="assistant",
        identity_statement="A public-safe assistant profile.",
    )
    mode = loadout_service.register_mode_profile(
        core_profile_id=core.core_profile_id,
        mode_name="local_runtime_mode",
        mode_type="local_runtime_mode",
        role_statement="Use explicitly bound runtime context.",
    )
    loadout = loadout_service.create_mode_loadout(core_profile=core, mode_profile=mode)
    service = PersonalModeBindingService(trace_service=trace_service)
    selection = service.select_mode(mode_profile=mode, loadout=loadout, selection_source="test")
    runtime_binding = service.bind_runtime(selection=selection, runtime_kind="local_runtime")
    service.register_runtime_capability_binding(
        runtime_binding_id=runtime_binding.binding_id,
        capability_name="ocel_context",
        capability_category="runtime",
        availability="metadata_only",
        can_execute_now=False,
    )
    request = service.create_activation_request(
        mode_profile_id=mode.mode_profile_id,
        loadout_id=loadout.loadout_id,
        runtime_kind="local_runtime",
        requested_by="test",
    )
    service.activate_mode_for_prompt_context(
        request=request,
        mode_profile=mode,
        loadout=loadout,
        runtime_kind="local_runtime",
    )

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}

    for object_type in [
        "personal_mode_selection",
        "personal_runtime_binding",
        "personal_runtime_capability_binding",
        "personal_mode_activation_request",
        "personal_mode_activation_result",
    ]:
        assert store.fetch_objects_by_type(object_type)
    assert {
        "personal_mode_selected",
        "personal_runtime_binding_created",
        "personal_runtime_capability_binding_registered",
        "personal_mode_activation_requested",
        "personal_mode_activation_recorded",
        "personal_mode_binding_attached_to_prompt",
    }.issubset(activities)
