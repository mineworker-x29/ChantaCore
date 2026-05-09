from pathlib import Path

from chanta_core.persona import PersonalOverlayLoaderService


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_boundary_finding_when_personal_directory_inside_public_repo(tmp_path) -> None:
    public_repo = tmp_path / "public_repo"
    root = public_repo / "local_personal_directory"
    _write(root / "overlay" / "core.md", "projection")
    service = PersonalOverlayLoaderService()
    config = service.register_config(directory_name="dummy", directory_root=root)
    manifest = service.load_manifest(config)

    findings = service.check_overlay_boundaries(manifest, public_repo_root=public_repo)
    refs = service.register_projection_refs(manifest)
    result = service.load_projection_for_prompt(
        manifest=manifest,
        projection_refs=refs,
        boundary_findings=findings,
    )

    assert any(finding.finding_type == "personal_root_inside_public_repo" for finding in findings)
    assert result.denied is True
    assert result.rendered_blocks == []


def test_letters_and_message_patterns_under_source_are_failed(tmp_path) -> None:
    root = tmp_path / "dummy_personal_directory"
    _write(root / "source" / "letters" / "example.md", "excluded letter")
    _write(root / "source" / "message_to_personal_profile_001.md", "excluded future")
    _write(root / "source" / "message_to_user_001.md", "excluded personal")
    _write(root / "overlay" / "core.md", "projection")
    service = PersonalOverlayLoaderService()
    config = service.register_config(directory_name="dummy", directory_root=root)
    manifest = service.load_manifest(config)

    findings = service.check_overlay_boundaries(manifest, public_repo_root=tmp_path / "public_repo")

    finding_types = {finding.finding_type for finding in findings}
    assert "letters_source_import_attempt" in finding_types


def test_personal_overlay_module_has_no_forbidden_runtime_behavior() -> None:
    source = Path("src/chanta_core/persona/personal_overlay.py").read_text(encoding="utf-8")

    for forbidden in [
        "D:" + "\\ExamplePersonal" + "Directory",
        "complete" + "_text",
        "complete" + "_json",
        "htt" + "px",
        "soc" + "ket",
        "sub" + "process",
        "os." + "system",
        "connect" + "_mcp",
        "load" + "_plugin",
        "json" + "l",
    ]:
        assert forbidden not in source


