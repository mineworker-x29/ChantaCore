from pathlib import Path

from chanta_core.ocel.store import OCELStore
from chanta_core.persona.personal_runtime_surface import PersonalRuntimeSurfaceService


def _dummy_personal_directory(root: Path) -> None:
    for name in ["source", "overlay", "profiles", "mode_loadouts", "validation", "letters", "messages", "archive"]:
        (root / name).mkdir(parents=True, exist_ok=True)
    (root / "source" / "identity.md").write_text("public-safe source summary", encoding="utf-8")
    (root / "overlay" / "core.md").write_text("public-safe overlay projection", encoding="utf-8")
    (root / "profiles" / "profile.md").write_text("public-safe profile projection", encoding="utf-8")
    (root / "mode_loadouts" / "mode.md").write_text("public-safe mode projection", encoding="utf-8")
    (root / "letters" / "private.md").write_text("do-not-print-private-body", encoding="utf-8")


def test_status_env_absent_is_noop(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CHANTA_PERSONAL_DIRECTORY_ROOT", raising=False)
    service = PersonalRuntimeSurfaceService(
        ocel_store=OCELStore(tmp_path / "surface.sqlite")
    )

    result = service.run_personal_status()
    rendered = service.render_cli_result(result)

    assert result.exit_code == 0
    assert result.status == "noop"
    assert "not configured" in rendered
    assert "Traceback" not in rendered


def test_status_env_present_redacts_paths_and_counts_refs(monkeypatch, tmp_path) -> None:
    personal_root = tmp_path / "personal"
    _dummy_personal_directory(personal_root)
    monkeypatch.setenv("CHANTA_PERSONAL_DIRECTORY_ROOT", str(personal_root))
    service = PersonalRuntimeSurfaceService(
        ocel_store=OCELStore(tmp_path / "surface.sqlite")
    )

    result = service.run_personal_status()
    rendered = service.render_cli_result(result)

    assert result.exit_code == 0
    assert result.status in {"passed", "needs_review"}
    assert str(personal_root) not in rendered
    assert "<redacted:" in rendered
    assert "projection_count=1" in rendered
    assert "profile_count=1" in rendered
    assert "loadout_count=1" in rendered
    assert "do-not-print-private-body" not in rendered


def test_show_paths_can_show_configured_root(monkeypatch, tmp_path) -> None:
    personal_root = tmp_path / "personal"
    _dummy_personal_directory(personal_root)
    monkeypatch.setenv("CHANTA_PERSONAL_DIRECTORY_ROOT", str(personal_root))
    service = PersonalRuntimeSurfaceService(
        ocel_store=OCELStore(tmp_path / "surface.sqlite")
    )

    result = service.run_personal_config(show_paths=True)
    rendered = service.render_cli_result(result)

    assert str(personal_root.resolve(strict=False)) in rendered
    assert "paths_redacted=False" in rendered


def test_validate_and_smoke_summarize_without_source_bodies(monkeypatch, tmp_path) -> None:
    personal_root = tmp_path / "personal"
    _dummy_personal_directory(personal_root)
    monkeypatch.setenv("CHANTA_PERSONAL_DIRECTORY_ROOT", str(personal_root))
    service = PersonalRuntimeSurfaceService(
        ocel_store=OCELStore(tmp_path / "surface.sqlite")
    )

    validate = service.run_personal_validate()
    validate_text = service.render_cli_result(validate)
    smoke = service.run_personal_smoke()
    smoke_text = service.render_cli_result(smoke)

    assert validate.exit_code == 0
    assert validate.conformance_result_ids
    assert "Personal Conformance completed" in validate.summary
    assert smoke.exit_code == 0
    assert smoke.smoke_result_ids
    assert "Personal Runtime Smoke Test completed" in smoke.summary
    assert "do-not-print-private-body" not in validate_text
    assert "do-not-print-private-body" not in smoke_text
