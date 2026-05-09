from chanta_core.persona import (
    PersonalModeLoadoutService,
    personal_core_profiles_to_history_entries,
    personal_mode_boundaries_to_history_entries,
    personal_mode_loadouts_to_history_entries,
    personal_mode_profiles_to_history_entries,
)


def test_personal_mode_loadout_history_entries_have_source_and_priorities() -> None:
    service = PersonalModeLoadoutService()
    core = service.register_core_profile(
        profile_name="dummy_personal_profile",
        profile_type="assistant",
        identity_statement="A public-safe assistant identity.",
    )
    mode = service.register_mode_profile(
        core_profile_id=core.core_profile_id,
        mode_name="review_mode",
        mode_type="review_mode",
        role_statement="Review provided text.",
    )
    boundary = service.register_mode_boundary(
        mode_profile_id=mode.mode_profile_id,
        boundary_type="capability_boundary",
        boundary_text="Runtime capability profile remains authoritative.",
        severity="high",
    )
    loadout = service.create_mode_loadout(
        core_profile=core,
        mode_profile=mode,
        boundaries=[boundary],
    )

    entries = (
        personal_core_profiles_to_history_entries([core])
        + personal_mode_profiles_to_history_entries([mode])
        + personal_mode_boundaries_to_history_entries([boundary])
        + personal_mode_loadouts_to_history_entries([loadout])
    )

    assert {entry.source for entry in entries} == {"personal_mode_loadout"}
    assert max(entry.priority for entry in entries) >= 80
    assert "Runtime capability profile" in entries[-1].content
