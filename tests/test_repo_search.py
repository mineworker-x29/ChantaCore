from pathlib import Path

from chanta_core.repo import RepoSearchService
from chanta_core.workspace import WorkspaceConfig, WorkspaceInspector


def service(tmp_path: Path) -> RepoSearchService:
    (tmp_path / "README.md").write_text("Hello Process\n", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text(
        "def main():\n    return 'process'\n",
        encoding="utf-8",
    )
    (tmp_path / ".env").write_text("process secret\n", encoding="utf-8")
    return RepoSearchService(WorkspaceInspector(WorkspaceConfig(workspace_root=tmp_path)))


def test_search_text_finds_lines(tmp_path) -> None:
    result = service(tmp_path).search_text("process", case_sensitive=False)

    assert [item.relative_path for item in result.matches] == [
        "README.md",
        "src/app.py",
    ]
    assert [item.line_number for item in result.matches] == [1, 2]


def test_case_sensitive_search(tmp_path) -> None:
    result = service(tmp_path).search_text("Process", case_sensitive=True)

    assert len(result.matches) == 1
    assert result.matches[0].relative_path == "README.md"


def test_find_files_by_pattern(tmp_path) -> None:
    result = service(tmp_path).find_files("*.py")

    assert [item.relative_path for item in result.file_matches] == ["src/app.py"]


def test_blocked_files_not_searched(tmp_path) -> None:
    result = service(tmp_path).search_text("secret", case_sensitive=False)

    assert result.matches == []
    assert result.result_attrs["files_skipped"] == 0
