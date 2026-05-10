from pathlib import Path

from chanta_core.ocel.store import OCELStore
from chanta_core.persona.personal_runtime_surface import PersonalRuntimeSurfaceService


def _dummy_personal_directory(root: Path) -> None:
    for name in ["source", "overlay", "profiles", "mode_loadouts", "letters", "messages", "archive"]:
        (root / name).mkdir(parents=True, exist_ok=True)
    (root / "source" / "identity.md").write_text("public-safe source", encoding="utf-8")
    (root / "letters" / "letter.md").write_text("private-letter-body", encoding="utf-8")
    (root / "messages" / "message.md").write_text("private-message-body", encoding="utf-8")
    (root / "archive" / "archive.md").write_text("private-archive-body", encoding="utf-8")
    (root / "overlay" / "core.md").write_text("public-safe overlay", encoding="utf-8")
    (root / "profiles" / "profile.md").write_text("public-safe profile", encoding="utf-8")
    (root / "mode_loadouts" / "mode.md").write_text("public-safe mode", encoding="utf-8")


def test_personal_runtime_surface_does_not_print_or_read_excluded_bodies(monkeypatch, tmp_path) -> None:
    personal_root = tmp_path / "personal"
    _dummy_personal_directory(personal_root)
    monkeypatch.setenv("CHANTA_PERSONAL_DIRECTORY_ROOT", str(personal_root))
    service = PersonalRuntimeSurfaceService(
        ocel_store=OCELStore(tmp_path / "surface.sqlite")
    )

    result = service.run_personal_sources()
    rendered = service.render_cli_result(result)

    assert "private-letter-body" not in rendered
    assert "private-message-body" not in rendered
    assert "private-archive-body" not in rendered
    assert result.result_attrs["letters_read_as_source"] is False
    assert result.result_attrs["messages_read_as_source"] is False
    assert result.result_attrs["archive_read_as_source"] is False
    assert result.result_attrs["source_bodies_printed"] is False


def test_personal_runtime_surface_does_not_activate_or_grant(monkeypatch, tmp_path) -> None:
    personal_root = tmp_path / "personal"
    _dummy_personal_directory(personal_root)
    monkeypatch.setenv("CHANTA_PERSONAL_DIRECTORY_ROOT", str(personal_root))
    service = PersonalRuntimeSurfaceService(
        ocel_store=OCELStore(tmp_path / "surface.sqlite")
    )

    result = service.run_personal_modes()

    assert result.result_attrs["mode_activation_enabled"] is False
    assert result.result_attrs["capability_grants_created"] is False
    assert result.result_attrs["tool_execution_used"] is False
    assert result.result_attrs["model_call_used"] is False
    assert result.result_attrs["shell_execution_used"] is False
    assert result.result_attrs["network_access_used"] is False
    assert result.result_attrs["mcp_connection_used"] is False
    assert result.result_attrs["plugin_loading_used"] is False
    assert result.result_attrs["line_delimited_runtime_store_created"] is False


def test_personal_runtime_surface_source_has_no_private_or_execution_terms() -> None:
    text = Path("src/chanta_core/persona/personal_runtime_surface.py").read_text(encoding="utf-8")
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
