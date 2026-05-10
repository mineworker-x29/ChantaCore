from chanta_core.ocel.store import OCELStore
from chanta_core.persona.personal_mode_loadout import PersonalModeLoadoutService
from chanta_core.persona.personal_prompt_activation import PersonalPromptActivationService


def test_render_activation_blocks_omits_denied_or_none_scope(tmp_path) -> None:
    service = PersonalPromptActivationService(
        ocel_store=OCELStore(tmp_path / "activation.sqlite")
    )
    result = service.activate_for_prompt_context()

    assert service.render_activation_blocks(result=result) == ""


def test_render_activation_blocks_has_boundary_header(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CHANTA_PERSONAL_DIRECTORY_ROOT", raising=False)
    store = OCELStore(tmp_path / "activation.sqlite")
    loadouts = PersonalModeLoadoutService(ocel_store=store)
    core = loadouts.register_core_profile(
        profile_name="public_safe_profile",
        profile_type="test",
        identity_statement="Public-safe identity.",
    )
    mode = loadouts.register_mode_profile(
        core_profile_id=core.core_profile_id,
        mode_name="public_safe_mode",
        mode_type="test",
        role_statement="Public-safe role.",
    )
    boundary = loadouts.register_mode_boundary(
        mode_profile_id=mode.mode_profile_id,
        boundary_type="capability_boundary",
        boundary_text="Capability truth must win.",
    )
    loadout = loadouts.create_mode_loadout(
        core_profile=core,
        mode_profile=mode,
        boundaries=[boundary],
    )
    service = PersonalPromptActivationService(ocel_store=store)

    result = service.activate_for_prompt_context(explicit_loadout=loadout)
    rendered = service.render_activation_blocks(result=result)

    assert rendered.startswith("Personal Mode Prompt Activation:")
    assert "Activation scope: prompt_context_only" in rendered
    assert "does not grant capabilities or execute tools" in rendered
    assert "Capability truth must win." in rendered
