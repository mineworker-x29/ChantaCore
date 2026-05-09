from chanta_core.persona import PersonaSourceStagedImportService


def _write(path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_discovers_included_files_and_excludes_private_like_areas(tmp_path) -> None:
    root = tmp_path / "sources"
    _write(root / "profile.md", "# Identity\npublic dummy")
    _write(root / "profile.txt", "role: public dummy")
    _write(root / "profile.html", "<p>safety: public dummy</p>")
    _write(root / "archive" / "old.md", "excluded archive")
    _write(root / "letters" / "note.md", "excluded letter")
    _write(root / "messages" / "note.md", "excluded message")
    _write(root / "message_to_personal_profile_001.md", "excluded profile note")
    _write(root / "message_to_user_001.md", "excluded user note")

    service = PersonaSourceStagedImportService()
    sources = service.discover_sources(root)

    assert {source.source_name for source in sources} == {
        "profile.md",
        "profile.txt",
        "profile.html",
    }


def test_discovery_honors_custom_include_exclude_patterns(tmp_path) -> None:
    root = tmp_path / "sources"
    _write(root / "keep" / "profile.md", "identity keep")
    _write(root / "drop" / "profile.md", "identity drop")

    service = PersonaSourceStagedImportService()
    sources = service.discover_sources(
        root,
        include_patterns=["keep/*.md", "drop/*.md"],
        exclude_patterns=["drop/**"],
    )

    assert [source.source_name for source in sources] == ["profile.md"]
    assert "keep" in sources[0].source_ref

