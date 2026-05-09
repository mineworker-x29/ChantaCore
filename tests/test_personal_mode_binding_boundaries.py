from pathlib import Path

from chanta_core.persona import PersonalModeBindingService, PersonalModeLoadoutService


def test_personal_mode_binding_does_not_mutate_runtime_or_create_capabilities() -> None:
    loadout_service = PersonalModeLoadoutService()
    core = loadout_service.register_core_profile(
        profile_name="sample_personal_assistant",
        profile_type="assistant",
        identity_statement="A public-safe assistant profile.",
    )
    mode = loadout_service.register_mode_profile(
        core_profile_id=core.core_profile_id,
        mode_name="manual_handoff_mode",
        mode_type="manual_handoff_mode",
        role_statement="Use user-provided context only.",
    )
    loadout = loadout_service.create_mode_loadout(core_profile=core, mode_profile=mode)
    service = PersonalModeBindingService()
    selection = service.select_mode(mode_profile=mode, loadout=loadout)
    runtime_binding = service.bind_runtime(selection=selection, runtime_kind="manual_handoff")
    capability = service.register_runtime_capability_binding(
        runtime_binding_id=runtime_binding.binding_id,
        capability_name="manual_context_review",
        capability_category="reasoning",
        availability="metadata_only",
        can_execute_now=False,
    )

    assert runtime_binding.context_ingress == "manual_handoff"
    assert runtime_binding.binding_attrs["runtime_mutated"] is False
    assert runtime_binding.binding_attrs["capability_grants_created"] is False
    assert capability.binding_attrs["capability_grant_created"] is False


def test_personal_mode_binding_public_files_do_not_contain_forbidden_runtime_features() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "src" / "chanta_core" / "persona" / "personal_mode_binding.py",
        root / "tests" / "test_personal_mode_binding_models.py",
        root / "tests" / "test_personal_mode_binding_service.py",
        root / "tests" / "test_personal_mode_binding_history_adapter.py",
        root / "tests" / "test_personal_mode_binding_ocel_shape.py",
        root / "tests" / "test_personal_mode_binding_boundaries.py",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in paths)

    forbidden_fragments = [
        "complete_" + "text",
        "complete_" + "json",
        "Tool" + "Dispatcher",
        "dis" + "patch",
        "sub" + "process",
        "req" + "uests",
        "ht" + "tpx",
        "so" + "cket",
        "connect_" + "mcp",
        "load_" + "plugin",
        "apply_" + "grant",
        "js" + "onl",
    ]
    assert not any(fragment in text for fragment in forbidden_fragments)
    assert ("AgentRuntime" + " mode switch") not in text
