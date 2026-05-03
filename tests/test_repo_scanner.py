from pathlib import Path

from chanta_core.repo import RepoScanner
from chanta_core.workspace import WorkspaceConfig, WorkspaceInspector


def make_repo(tmp_path: Path) -> RepoScanner:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text("def main():\n    pass\n", encoding="utf-8")
    (tmp_path / "src" / "utils.py").write_text("class Helper:\n    pass\n", encoding="utf-8")
    (tmp_path / ".env").write_text("SECRET=1\n", encoding="utf-8")
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "test.sqlite").write_text("blocked", encoding="utf-8")
    return RepoScanner(WorkspaceInspector(WorkspaceConfig(workspace_root=tmp_path)))


def test_find_files_finds_python_files(tmp_path) -> None:
    scanner = make_repo(tmp_path)

    matches = scanner.find_files("*.py")

    assert [item.relative_path for item in matches] == ["src/app.py", "src/utils.py"]


def test_candidate_code_files_excludes_blocked_files(tmp_path) -> None:
    scanner = make_repo(tmp_path)

    paths = {item.relative_path for item in scanner.candidate_code_files()}

    assert "README.md" in paths
    assert "src/app.py" in paths
    assert ".env" not in paths
    assert "data/test.sqlite" not in paths


def test_scan_tree_works(tmp_path) -> None:
    scanner = make_repo(tmp_path)

    result = scanner.scan_tree()

    assert result["file_count"] >= 3
    assert result["directory_count"] >= 1
    assert result["skipped_count"] >= 2
