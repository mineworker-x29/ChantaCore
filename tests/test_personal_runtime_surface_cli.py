from pathlib import Path

from chanta_core.cli.main import main


def _dummy_personal_directory(root: Path) -> None:
    for name in ["source", "overlay", "profiles", "mode_loadouts", "validation", "letters"]:
        (root / name).mkdir(parents=True, exist_ok=True)
    (root / "source" / "identity.md").write_text("public-safe source", encoding="utf-8")
    (root / "overlay" / "core.md").write_text("public-safe overlay", encoding="utf-8")
    (root / "profiles" / "profile.md").write_text("public-safe profile", encoding="utf-8")
    (root / "mode_loadouts" / "mode.md").write_text("public-safe mode", encoding="utf-8")
    (root / "letters" / "note.md").write_text("hidden-local-letter-body", encoding="utf-8")


def test_cli_personal_status_no_config_no_traceback(monkeypatch, capsys) -> None:
    monkeypatch.delenv("CHANTA_PERSONAL_DIRECTORY_ROOT", raising=False)

    exit_code = main(["personal", "status"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "status=noop" in captured.out
    assert "Traceback" not in captured.out
    assert captured.err == ""


def test_cli_validate_and_smoke_no_config_controlled_exit(monkeypatch, capsys) -> None:
    monkeypatch.delenv("CHANTA_PERSONAL_DIRECTORY_ROOT", raising=False)

    validate_exit = main(["personal", "validate"])
    validate = capsys.readouterr()
    smoke_exit = main(["personal", "smoke"])
    smoke = capsys.readouterr()

    assert validate_exit == 1
    assert "Personal Directory is not configured" in validate.out
    assert "Traceback" not in validate.out
    assert smoke_exit == 1
    assert "Personal Directory is not configured" in smoke.out
    assert "Traceback" not in smoke.out


def test_cli_personal_subcommands_are_public_safe(monkeypatch, tmp_path, capsys) -> None:
    personal_root = tmp_path / "personal"
    _dummy_personal_directory(personal_root)
    monkeypatch.setenv("CHANTA_PERSONAL_DIRECTORY_ROOT", str(personal_root))

    for subcommand in ["config", "sources", "overlays", "modes"]:
        exit_code = main(["personal", subcommand])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert str(personal_root) not in captured.out
        assert "<redacted:" in captured.out
        assert "hidden-local-letter-body" not in captured.out
        assert "source_bodies_printed=false" in captured.out
        assert "mode_activation_enabled=false" in captured.out
        assert "capability_grants_created=false" in captured.out


def test_cli_personal_modes_lists_dummy_loadouts_without_private_content(monkeypatch, tmp_path, capsys) -> None:
    personal_root = tmp_path / "personal"
    _dummy_personal_directory(personal_root)
    for name in [
        "research_mode_loadout.md",
        "coding_mode_loadout.md",
        "runtime_mode_loadout.md",
    ]:
        (personal_root / "mode_loadouts" / name).write_text(
            f"# {name}\n\nprivate-mode-body-should-not-print",
            encoding="utf-8",
        )
    (personal_root / "mode_loadouts" / "mode.md").unlink()
    monkeypatch.setenv("CHANTA_PERSONAL_DIRECTORY_ROOT", str(personal_root))

    exit_code = main(["personal", "modes"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "loadout_count=3" in captured.out
    assert "mode_loadout=1;" in captured.out
    assert "mode=research" in captured.out
    assert "mode=coding" in captured.out
    assert "mode=runtime" in captured.out
    assert "file=research_mode_loadout.md" in captured.out
    assert "projection_kind=mode_loadout" in captured.out
    assert "size_chars=" in captured.out
    assert "preview_chars=" in captured.out
    assert "safe_for_prompt=True" in captured.out
    assert str(personal_root) not in captured.out
    assert "private-mode-body-should-not-print" not in captured.out
    assert "hidden-local-letter-body" not in captured.out
    assert "source_bodies_printed=false" in captured.out
