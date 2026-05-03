from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


def _default_blocked_names() -> set[str]:
    return {
        ".env",
        ".env.local",
        ".env.production",
        ".venv",
        "venv",
        "__pycache__",
        ".git",
        "node_modules",
        "data",
        ".pytest_cache",
        ".pytest-tmp",
    }


def _default_blocked_suffixes() -> set[str]:
    return {
        ".sqlite",
        ".sqlite3",
        ".db",
        ".pem",
        ".key",
        ".p12",
        ".pfx",
    }


@dataclass(frozen=True)
class WorkspaceConfig:
    workspace_root: Path = field(default_factory=lambda: Path.cwd())
    max_file_size_bytes: int = 200_000
    max_list_entries: int = 500
    allowed_extensions: set[str] | None = None
    blocked_names: set[str] = field(default_factory=_default_blocked_names)
    blocked_suffixes: set[str] = field(default_factory=_default_blocked_suffixes)

    def normalized_root(self) -> Path:
        return self.workspace_root.expanduser().resolve()
