from chanta_core.materialized_views import (
    MaterializedViewInputSnapshot,
    MaterializedViewService,
)


def test_render_default_views_returns_all_five_without_writing(tmp_path) -> None:
    service = MaterializedViewService(root=tmp_path)

    views = service.render_default_views(MaterializedViewInputSnapshot())

    assert set(views) == {"memory", "project", "user", "pig_guidance", "context_rules"}
    assert not (tmp_path / ".chanta").exists()
    for view in views.values():
        assert view.canonical is False
        assert ".chanta" in view.target_path


def test_write_view_writes_and_skip_without_overwrite(tmp_path) -> None:
    service = MaterializedViewService(root=tmp_path)
    view = service.render_default_views(MaterializedViewInputSnapshot())["memory"]

    result = service.write_view(view)
    skipped = service.write_view(view, overwrite=False)

    assert result.written is True
    assert (tmp_path / ".chanta" / "MEMORY.md").exists()
    assert skipped.written is False
    assert skipped.skipped_reason is not None


def test_refresh_default_views_writes_all_expected_files(tmp_path) -> None:
    service = MaterializedViewService(root=tmp_path)

    results = service.refresh_default_views(MaterializedViewInputSnapshot())

    assert all(result.written for result in results.values())
    assert sorted(path.name for path in (tmp_path / ".chanta").glob("*.md")) == [
        "CONTEXT_RULES.md",
        "MEMORY.md",
        "PIG_GUIDANCE.md",
        "PROJECT.md",
        "USER.md",
    ]
    assert not (tmp_path / "memory.jsonl").exists()
    assert not (tmp_path / "instructions.jsonl").exists()
