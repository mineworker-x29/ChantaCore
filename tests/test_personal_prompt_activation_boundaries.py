from pathlib import Path

from chanta_core.ocel.store import OCELStore
from chanta_core.persona.personal_mode_loadout import PersonalModeLoadoutService
from chanta_core.persona.personal_prompt_activation import PersonalPromptActivationService


def _loadout(store):
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
        boundary_text="Capability truth overrides personal claims.",
    )
    return loadouts.create_mode_loadout(core_profile=core, mode_profile=mode, boundaries=[boundary])


def test_activation_result_has_no_execution_or_grant_flags(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CHANTA_PERSONAL_DIRECTORY_ROOT", raising=False)
    store = OCELStore(tmp_path / "activation.sqlite")
    loadout = _loadout(store)
    service = PersonalPromptActivationService(ocel_store=store)

    result = service.activate_for_prompt_context(explicit_loadout=loadout)

    assert result.result_attrs["runtime_capability_activation"] is False
    assert result.result_attrs["capability_grants_created"] is False
    assert result.result_attrs["tool_execution_used"] is False
    assert result.result_attrs["model_call_used"] is False
    assert result.result_attrs["shell_execution_used"] is False
    assert result.result_attrs["network_access_used"] is False
    assert result.result_attrs["mcp_connection_used"] is False
    assert result.result_attrs["plugin_loading_used"] is False
    assert result.result_attrs["source_bodies_loaded"] is False


def test_activation_source_has_no_private_or_execution_terms() -> None:
    text = Path("src/chanta_core/persona/personal_prompt_activation.py").read_text(encoding="utf-8")
    forbidden = [
        "private_future_message_token",
        "private_relationship_note_token",
        "complete_" + "text(",
        "complete_" + "json(",
        "sub" + "process",
        "requests" + ".",
        "httpx" + ".",
        "socket" + ".",
        "connect_" + "mcp",
        "load_" + "plugin",
        "apply_" + "grant",
        "runtime_store.json",
    ]
    for token in forbidden:
        assert token not in text
