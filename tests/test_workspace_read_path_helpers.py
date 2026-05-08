from pathlib import Path

import pytest

from chanta_core.workspace import (
    WorkspacePathViolationError,
    extract_markdown_headings,
    hash_content,
    is_binary_bytes,
    is_path_inside_root,
    normalize_workspace_root,
    preview_text,
    resolve_workspace_path,
    validate_relative_workspace_path,
)


def test_resolve_workspace_path_is_root_constrained(tmp_path) -> None:
    root = normalize_workspace_root(tmp_path)
    inside = resolve_workspace_path(root, "notes/a.md")

    assert is_path_inside_root(inside, root)
    assert inside == (Path(tmp_path) / "notes" / "a.md").resolve(strict=False)


def test_absolute_and_traversal_paths_are_rejected(tmp_path) -> None:
    with pytest.raises(WorkspacePathViolationError):
        validate_relative_workspace_path(str(tmp_path / "outside.md"))

    with pytest.raises(WorkspacePathViolationError):
        resolve_workspace_path(tmp_path, "../outside.md")


def test_text_helpers_are_deterministic() -> None:
    text = "# Title\n\n## Section\nBody"

    assert is_binary_bytes(b"a\x00b") is True
    assert is_binary_bytes(b"abc") is False
    assert hash_content("abc") == hash_content("abc")
    assert preview_text("abcdef", max_chars=3) == "abc"
    assert extract_markdown_headings(text) == ["# Title", "## Section"]
