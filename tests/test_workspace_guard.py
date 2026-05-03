from pathlib import Path

import pytest

from chanta_core.workspace import (
    WorkspaceAccessError,
    WorkspaceConfig,
    WorkspacePathGuard,
)


def guard(tmp_path: Path) -> WorkspacePathGuard:
    return WorkspacePathGuard(WorkspaceConfig(workspace_root=tmp_path))


def test_valid_relative_path_allowed(tmp_path) -> None:
    path = tmp_path / "README.md"
    path.write_text("hello", encoding="utf-8")

    resolved = guard(tmp_path).validate_read_path("README.md")

    assert resolved == path.resolve()


def test_path_traversal_denied(tmp_path) -> None:
    outside = tmp_path.parent / "outside.txt"
    outside.write_text("outside", encoding="utf-8")

    with pytest.raises(WorkspaceAccessError):
        guard(tmp_path).validate_read_path("../outside.txt")


def test_absolute_path_outside_root_denied(tmp_path) -> None:
    outside = tmp_path.parent / "outside-absolute.txt"
    outside.write_text("outside", encoding="utf-8")

    with pytest.raises(WorkspaceAccessError):
        guard(tmp_path).validate_read_path(outside)


@pytest.mark.parametrize("blocked", [".env", ".venv/config", "data/test.txt", ".git/config"])
def test_blocked_names_denied(tmp_path, blocked: str) -> None:
    target = tmp_path / blocked
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("blocked", encoding="utf-8")

    with pytest.raises(WorkspaceAccessError):
        guard(tmp_path).validate_read_path(blocked)


@pytest.mark.parametrize("blocked", ["trace.sqlite", "local.db", "secret.pem", "secret.key"])
def test_blocked_suffixes_denied(tmp_path, blocked: str) -> None:
    (tmp_path / blocked).write_text("blocked", encoding="utf-8")

    with pytest.raises(WorkspaceAccessError):
        guard(tmp_path).validate_read_path(blocked)


def test_symlink_outside_root_denied_if_supported(tmp_path) -> None:
    outside = tmp_path.parent / "outside-symlink.txt"
    outside.write_text("outside", encoding="utf-8")
    link = tmp_path / "linked.txt"
    try:
        link.symlink_to(outside)
    except OSError:
        pytest.skip("Symlink creation is not available in this environment.")

    with pytest.raises(WorkspaceAccessError):
        guard(tmp_path).validate_read_path("linked.txt")
