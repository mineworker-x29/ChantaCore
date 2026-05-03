from pathlib import Path

import pytest

from chanta_core.workspace import (
    WorkspaceAccessError,
    WorkspaceConfig,
    WorkspaceFileTooLargeError,
    WorkspaceInspector,
    WorkspaceUnsupportedFileError,
)


def make_workspace(tmp_path: Path) -> WorkspaceInspector:
    (tmp_path / "README.md").write_text("hello\nworld\n", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text("print('hi')\n", encoding="utf-8")
    (tmp_path / ".env").write_text("SECRET=1\n", encoding="utf-8")
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "test.sqlite").write_text("blocked", encoding="utf-8")
    return WorkspaceInspector(WorkspaceConfig(workspace_root=tmp_path, max_file_size_bytes=20))


def test_get_workspace_root(tmp_path) -> None:
    inspector = make_workspace(tmp_path)

    result = inspector.get_workspace_root()

    assert result["workspace_root"] == "."
    assert result["workspace_root_name"] == tmp_path.name
    assert result["read_only"] is True


def test_path_exists(tmp_path) -> None:
    inspector = make_workspace(tmp_path)

    assert inspector.path_exists("README.md")["exists"] is True
    assert inspector.path_exists("missing.txt")["exists"] is False


def test_list_files_excludes_blocked_paths(tmp_path) -> None:
    inspector = make_workspace(tmp_path)

    result = inspector.list_files(".", recursive=True)
    paths = {entry["path"] for entry in result["entries"]}

    assert "README.md" in paths
    assert "src/app.py" in paths
    assert ".env" not in paths
    assert "data/test.sqlite" not in paths
    assert result["skipped_count"] >= 2


def test_read_text_file_reads_text(tmp_path) -> None:
    inspector = make_workspace(tmp_path)

    result = inspector.read_text_file("README.md")

    assert result["text"] == "hello\nworld\n"
    assert result["line_count"] == 2
    assert result["read_only"] is True


@pytest.mark.parametrize("blocked", [".env", "data/test.sqlite"])
def test_read_text_file_denies_blocked_paths(tmp_path, blocked: str) -> None:
    inspector = make_workspace(tmp_path)

    with pytest.raises(WorkspaceAccessError):
        inspector.read_text_file(blocked)


def test_summarize_tree(tmp_path) -> None:
    inspector = make_workspace(tmp_path)

    result = inspector.summarize_tree(".", max_depth=2)

    assert result["file_count"] >= 2
    assert result["directory_count"] >= 1
    assert result["tree"]


def test_large_file_raises(tmp_path) -> None:
    (tmp_path / "large.txt").write_text("x" * 21, encoding="utf-8")
    inspector = WorkspaceInspector(
        WorkspaceConfig(workspace_root=tmp_path, max_file_size_bytes=20)
    )

    with pytest.raises(WorkspaceFileTooLargeError):
        inspector.read_text_file("large.txt")


def test_binary_file_raises(tmp_path) -> None:
    (tmp_path / "binary.bin").write_bytes(b"abc\x00def")
    inspector = WorkspaceInspector(WorkspaceConfig(workspace_root=tmp_path))

    with pytest.raises(WorkspaceUnsupportedFileError):
        inspector.read_text_file("binary.bin")
