from chanta_core.persona import (
    PersonalModeBindingService,
    PersonalModeLoadoutService,
    personal_mode_activation_results_to_history_entries,
    personal_mode_selections_to_history_entries,
    personal_runtime_bindings_to_history_entries,
    personal_runtime_capability_bindings_to_history_entries,
)


def test_personal_mode_binding_history_entries() -> None:
    loadout_service = PersonalModeLoadoutService()
    core = loadout_service.register_core_profile(
        profile_name="sample_personal_assistant",
        profile_type="assistant",
        identity_statement="A public-safe assistant profile.",
    )
    mode = loadout_service.register_mode_profile(
        core_profile_id=core.core_profile_id,
        mode_name="review_mode",
        mode_type="review_mode",
        role_statement="Review provided text.",
    )
    loadout = loadout_service.create_mode_loadout(core_profile=core, mode_profile=mode)
    service = PersonalModeBindingService()
    selection = service.select_mode(mode_profile=mode, loadout=loadout)
    runtime_binding = service.bind_runtime(selection=selection, runtime_kind="review_runtime")
    capability = service.register_runtime_capability_binding(
        runtime_binding_id=runtime_binding.binding_id,
        capability_name="provided_text_review",
        capability_category="reasoning",
        availability="metadata_only",
        can_execute_now=False,
        requires_review=True,
    )
    request = service.create_activation_request(
        mode_profile_id=mode.mode_profile_id,
        runtime_kind="review_runtime",
        loadout_id=loadout.loadout_id,
    )
    result = service.activate_mode_for_prompt_context(
        request=request,
        mode_profile=mode,
        loadout=loadout,
        runtime_kind="review_runtime",
    )

    entries = (
        personal_mode_selections_to_history_entries([selection])
        + personal_runtime_bindings_to_history_entries([runtime_binding])
        + personal_runtime_capability_bindings_to_history_entries([capability])
        + personal_mode_activation_results_to_history_entries([result])
    )

    assert {entry.source for entry in entries} == {"personal_mode_binding"}
    assert max(entry.priority for entry in entries) >= 80
    assert "Personal runtime binding" in entries[1].content
    assert "prompt_context_only" in entries[-1].content
