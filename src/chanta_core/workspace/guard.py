from __future__ import annotations

from pathlib import Path

from chanta_core.workspace.errors import WorkspaceAccessError
from chanta_core.workspace.paths import WorkspaceConfig


class WorkspacePathGuard:
    def __init__(self, config: WorkspaceConfig) -> None:
        self.config = config
        self.workspace_root = config.normalized_root()

    def resolve_relative_path(self, path: str | Path) -> Path:
        candidate = Path(path).expanduser()
        if not candidate.is_absolute():
            candidate = self.workspace_root / candidate
        return candidate.resolve()

    def is_within_workspace(self, path: Path) -> bool:
        try:
            path.resolve().relative_to(self.workspace_root)
            return True
        except ValueError:
            return False

    def is_blocked_path(self, path: Path) -> bool:
        resolved = path.resolve()
        try:
            relative = resolved.relative_to(self.workspace_root)
        except ValueError:
            return True
        blocked_names = {item.lower() for item in self.config.blocked_names}
        blocked_suffixes = {item.lower() for item in self.config.blocked_suffixes}
        for part in relative.parts:
            if part.lower() in blocked_names:
                return True
        return resolved.suffix.lower() in blocked_suffixes

    def validate_read_path(self, path: str | Path) -> Path:
        resolved = self.resolve_relative_path(path)
        if not self.is_within_workspace(resolved):
            raise WorkspaceAccessError("Path is outside the workspace root.")
        if self.is_blocked_path(resolved):
            raise WorkspaceAccessError("Path is blocked by workspace read policy.")
        return resolved
