from pathlib import Path

from chanta_core.persona import PersonalModeLoadoutService


def test_personal_mode_loadout_boundaries_are_design_only() -> None:
    service = PersonalModeLoadoutService()
    core = service.register_core_profile(
        profile_name="dummy_personal_profile",
        profile_type="assistant",
        identity_statement="A public-safe assistant identity.",
    )
    mode = service.register_mode_profile(
        core_profile_id=core.core_profile_id,
        mode_name="coding_mode",
        mode_type="coding_mode",
        role_statement="Reason about code supplied by the caller.",
        limitation_summary="Execution depends on explicit runtime capability binding.",
    )
    boundary = service.register_mode_boundary(
        mode_profile_id=mode.mode_profile_id,
        boundary_type="tool_boundary",
        boundary_text="Do not execute tools from a Personal Mode Loadout.",
        severity="high",
    )
    binding = service.register_capability_binding(
        mode_profile_id=mode.mode_profile_id,
        capability_name="code_execution",
        capability_category="runtime",
        availability="requires_permission",
        can_execute_now=False,
        requires_permission=True,
    )
    loadout = service.create_mode_loadout(
        core_profile=core,
        mode_profile=mode,
        boundaries=[boundary],
        capability_bindings=[binding],
    )

    assert "Runtime capability profile overrides personal/persona claims." in (
        loadout.capability_boundary_block
    )
    assert "can_execute_now=False" in loadout.capability_boundary_block
    assert loadout.loadout_attrs["capability_grants_created"] is False
    assert loadout.loadout_attrs["runtime_mode_selection_enabled"] is False


def test_personal_mode_loadout_public_files_do_not_contain_disallowed_runtime_features() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "src" / "chanta_core" / "persona" / "personal_mode_loadout.py",
        root / "tests" / "test_personal_mode_loadout_models.py",
        root / "tests" / "test_personal_mode_loadout_service.py",
        root / "tests" / "test_personal_mode_loadout_history_adapter.py",
        root / "tests" / "test_personal_mode_loadout_ocel_shape.py",
        root / "tests" / "test_personal_mode_loadout_boundaries.py",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in paths)

    forbidden_fragments = [
        "complete_" + "text",
        "complete_" + "json",
        "Tool" + "Dispatcher",
        "sub" + "process",
        "req" + "uests",
        "ht" + "tpx",
        "so" + "cket",
        "js" + "onl",
    ]
    assert not any(fragment in text for fragment in forbidden_fragments)
    assert ("AgentRuntime" + " mode switch") not in text
    assert ("chanta-cli" + " --mode") not in text
