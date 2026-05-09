from chanta_core.persona import (
    PersonalOverlayLoaderService,
    personal_overlay_boundary_findings_to_history_entries,
    personal_overlay_load_results_to_history_entries,
    personal_directory_manifests_to_history_entries,
    personal_projection_refs_to_history_entries,
)


def _write(path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_personal_overlay_history_entries_redact_paths(tmp_path) -> None:
    root = tmp_path / "dummy_personal_directory"
    _write(root / "overlay" / "core.md", "projection")
    service = PersonalOverlayLoaderService()
    config = service.register_config(directory_name="dummy", directory_root=root)
    manifest = service.load_manifest(config)
    findings = service.check_overlay_boundaries(manifest, public_repo_root=tmp_path / "public_repo")
    refs = service.register_projection_refs(manifest)
    result = service.load_projection_for_prompt(
        manifest=manifest,
        projection_refs=refs,
        boundary_findings=findings,
    )

    entries = (
        personal_directory_manifests_to_history_entries([manifest])
        + personal_projection_refs_to_history_entries(refs)
        + personal_overlay_load_results_to_history_entries([result])
        + personal_overlay_boundary_findings_to_history_entries(findings)
    )
    combined_content = "\n".join(entry.content for entry in entries)

    assert entries
    assert {entry.source for entry in entries} == {"personal_overlay"}
    assert str(root) not in combined_content
    assert "projection refs" in combined_content
    assert entries[0].entry_attrs["directory_root_hash"]




