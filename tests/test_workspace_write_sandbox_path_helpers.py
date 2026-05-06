from pathlib import Path

from chanta_core.sandbox import is_path_inside_root, is_same_or_child_path, normalize_path


def test_path_helpers_handle_child_sibling_traversal_and_missing_paths(tmp_path) -> None:
    root = tmp_path / "workspace"
    child = root / "src" / "file.py"
    sibling = tmp_path / "workspace-other" / "file.py"
    traversal_inside = root / "src" / ".." / "README.md"
    traversal_outside = root / ".." / "outside.txt"
    missing = root / "missing" / "future.txt"

    assert normalize_path(child) == str(Path(child).resolve(strict=False))
    assert is_path_inside_root(child, root) is True
    assert is_same_or_child_path(root, root) is True
    assert is_path_inside_root(sibling, root) is False
    assert is_path_inside_root(traversal_inside, root) is True
    assert is_path_inside_root(traversal_outside, root) is False
    assert is_path_inside_root(missing, root) is True


def test_path_helper_does_not_use_common_prefix_as_containment(tmp_path) -> None:
    root = tmp_path / "repo"
    common_prefix_sibling = tmp_path / "repo_backup" / "file.txt"

    assert str(common_prefix_sibling).startswith(str(root))
    assert is_path_inside_root(common_prefix_sibling, root) is False
