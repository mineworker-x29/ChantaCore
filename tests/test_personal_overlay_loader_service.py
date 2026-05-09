from chanta_core.persona import PersonalOverlayLoaderService


def _write(path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _dummy_root(tmp_path):
    root = tmp_path / "dummy_personal_directory"
    _write(root / "source" / "identity.md", "source body must not be prompt")
    _write(root / "overlay" / "core_projection.md", "core projection block")
    _write(root / "profiles" / "default_profile.md", "profile projection block")
    _write(root / "mode_loadouts" / "codex_mode.md", "codex mode block")
    _write(root / "validation" / "validation_report.md", "validation summary")
    _write(root / "letters" / "to_future" / "note.md", "letter body")
    _write(root / "archive" / "old.md", "archived body")
    return root


def test_load_config_from_env_absent_is_noop(monkeypatch) -> None:
    monkeypatch.delenv("CHANTA_PERSONAL_DIRECTORY_ROOT", raising=False)

    assert PersonalOverlayLoaderService().load_config_from_env() is None


def test_config_manifest_refs_and_prompt_loading(monkeypatch, tmp_path) -> None:
    root = _dummy_root(tmp_path)
    monkeypatch.setenv("CHANTA_PERSONAL_DIRECTORY_ROOT", str(root))
    service = PersonalOverlayLoaderService()

    config = service.load_config_from_env()
    assert config is not None
    manifest = service.load_manifest(config)
    findings = service.check_overlay_boundaries(manifest, public_repo_root=tmp_path / "public_repo")
    refs = service.register_projection_refs(manifest)
    result = service.load_projection_for_prompt(
        manifest=manifest,
        projection_refs=refs,
        requested_mode="codex",
        boundary_findings=findings,
        max_chars=100,
    )
    block = service.render_personal_overlay_block(result)

    assert manifest.source_root.endswith("source")
    assert manifest.overlay_dir.endswith("overlay")
    assert manifest.profiles_dir.endswith("profiles")
    assert manifest.mode_loadouts_dir.endswith("mode_loadouts")
    assert manifest.validation_dir.endswith("validation")
    assert any(path.endswith("letters") for path in manifest.excluded_roots)
    assert any(path.endswith("archive") for path in manifest.excluded_roots)
    assert {ref.projection_kind for ref in refs} == {
        "core_projection",
        "profile_projection",
        "mode_loadout",
    }
    assert all(ref.safe_for_prompt for ref in refs)
    assert result.denied is False
    assert result.loaded_projection_ref_ids
    assert block is not None
    assert "codex mode block" in block
    assert "source body must not be prompt" not in block
    assert "letter body" not in block
    assert "validation summary" not in block


def test_prompt_block_is_bounded(tmp_path) -> None:
    root = tmp_path / "dummy_personal_directory"
    _write(root / "overlay" / "core_projection.md", "x" * 100)
    service = PersonalOverlayLoaderService()
    config = service.register_config(directory_name="dummy", directory_root=root)
    manifest = service.load_manifest(config)
    refs = service.register_projection_refs(manifest)

    result = service.load_projection_for_prompt(
        manifest=manifest,
        projection_refs=refs,
        max_chars=12,
    )

    assert result.truncated is True
    assert result.total_chars == 12
    assert result.rendered_blocks[0]["content"] == "x" * 12


