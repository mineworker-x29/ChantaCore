from __future__ import annotations

from pathlib import Path
from typing import Any

from chanta_core.workspace.errors import (
    WorkspaceFileTooLargeError,
    WorkspaceUnsupportedFileError,
)
from chanta_core.workspace.guard import WorkspacePathGuard
from chanta_core.workspace.paths import WorkspaceConfig


class WorkspaceInspector:
    def __init__(
        self,
        config: WorkspaceConfig | None = None,
        guard: WorkspacePathGuard | None = None,
    ) -> None:
        self.config = config or WorkspaceConfig()
        self.guard = guard or WorkspacePathGuard(self.config)

    def get_workspace_root(self) -> dict[str, Any]:
        root = self.guard.workspace_root
        return {
            "workspace_root_name": root.name,
            "workspace_root": ".",
            "read_only": True,
            "max_file_size_bytes": self.config.max_file_size_bytes,
            "max_list_entries": self.config.max_list_entries,
        }

    def path_exists(self, path: str | Path) -> dict[str, Any]:
        resolved = self.guard.validate_read_path(path)
        return {
            "path": self._relative(resolved),
            "exists": resolved.exists(),
            "is_file": resolved.is_file(),
            "is_dir": resolved.is_dir(),
        }

    def list_files(
        self,
        path: str | Path = ".",
        *,
        recursive: bool = False,
        limit: int | None = None,
    ) -> dict[str, Any]:
        resolved = self.guard.validate_read_path(path)
        max_entries = self._limit(limit)
        entries: list[dict[str, Any]] = []
        skipped_count = 0
        if resolved.is_file():
            entries.append(self._entry(resolved))
        elif resolved.exists():
            pending = [resolved]
            while pending and len(entries) < max_entries:
                current = pending.pop(0)
                try:
                    children = sorted(current.iterdir(), key=lambda item: item.name.lower())
                except OSError:
                    skipped_count += 1
                    continue
                for child in children:
                    if self.guard.is_blocked_path(child):
                        skipped_count += 1
                        continue
                    entries.append(self._entry(child))
                    if len(entries) >= max_entries:
                        break
                    if recursive and child.is_dir():
                        pending.append(child)
        return {
            "path": self._relative(resolved),
            "recursive": recursive,
            "limit": max_entries,
            "entry_count": len(entries),
            "skipped_count": skipped_count,
            "entries": entries,
        }

    def read_text_file(self, path: str | Path) -> dict[str, Any]:
        resolved = self.guard.validate_read_path(path)
        if not resolved.exists() or not resolved.is_file():
            raise WorkspaceUnsupportedFileError("Path is not a readable file.")
        if self.config.allowed_extensions is not None:
            allowed = {item.lower() for item in self.config.allowed_extensions}
            if resolved.suffix.lower() not in allowed:
                raise WorkspaceUnsupportedFileError("File extension is not allowed.")
        size_bytes = resolved.stat().st_size
        if size_bytes > self.config.max_file_size_bytes:
            raise WorkspaceFileTooLargeError("File exceeds workspace read size limit.")
        with resolved.open("rb") as handle:
            first_chunk = handle.read(4096)
        if b"\x00" in first_chunk:
            raise WorkspaceUnsupportedFileError("Binary files are not supported.")
        text = resolved.read_text(encoding="utf-8", errors="replace")
        return {
            "path": self._relative(resolved),
            "size_bytes": size_bytes,
            "text": text,
            "line_count": len(text.splitlines()),
            "read_only": True,
        }

    def summarize_tree(
        self,
        path: str | Path = ".",
        *,
        max_depth: int = 2,
        limit: int | None = None,
    ) -> dict[str, Any]:
        resolved = self.guard.validate_read_path(path)
        max_entries = self._limit(limit)
        tree: list[dict[str, Any]] = []
        file_count = 0
        dir_count = 0
        skipped_count = 0
        if not resolved.exists():
            return {
                "path": self._relative(resolved),
                "max_depth": max_depth,
                "limit": max_entries,
                "file_count": 0,
                "directory_count": 0,
                "skipped_count": 0,
                "tree": [],
            }
        pending: list[tuple[Path, int]] = [(resolved, 0)]
        while pending and len(tree) < max_entries:
            current, depth = pending.pop(0)
            if self.guard.is_blocked_path(current):
                skipped_count += 1
                continue
            if current != resolved:
                item = self._entry(current)
                item["depth"] = depth
                tree.append(item)
                if current.is_dir():
                    dir_count += 1
                else:
                    file_count += 1
            if current.is_dir() and depth < max_depth:
                try:
                    children = sorted(current.iterdir(), key=lambda item: item.name.lower())
                except OSError:
                    skipped_count += 1
                    continue
                for child in children:
                    if self.guard.is_blocked_path(child):
                        skipped_count += 1
                        continue
                    pending.append((child, depth + 1))
        return {
            "path": self._relative(resolved),
            "max_depth": max_depth,
            "limit": max_entries,
            "file_count": file_count,
            "directory_count": dir_count,
            "skipped_count": skipped_count,
            "tree": tree,
        }

    def _entry(self, path: Path) -> dict[str, Any]:
        return {
            "path": self._relative(path),
            "name": path.name,
            "is_file": path.is_file(),
            "is_dir": path.is_dir(),
            "size_bytes": path.stat().st_size if path.is_file() else None,
        }

    def _relative(self, path: Path) -> str:
        try:
            relative = path.resolve().relative_to(self.guard.workspace_root)
        except ValueError:
            return "."
        value = relative.as_posix()
        return value or "."

    def _limit(self, value: int | None) -> int:
        if value is None:
            return self.config.max_list_entries
        return max(0, min(int(value), self.config.max_list_entries))
