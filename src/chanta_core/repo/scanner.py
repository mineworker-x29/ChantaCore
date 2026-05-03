from __future__ import annotations

import fnmatch
from pathlib import Path
from typing import Any

from chanta_core.repo.models import RepoFileMatch
from chanta_core.workspace import WorkspaceInspector


CODE_FILE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".java",
    ".go",
    ".rs",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".cs",
    ".kt",
    ".swift",
    ".rb",
    ".php",
    ".md",
    ".toml",
    ".yaml",
    ".yml",
    ".json",
}


class RepoScanner:
    def __init__(self, workspace_inspector: WorkspaceInspector) -> None:
        self.workspace_inspector = workspace_inspector

    def find_files(self, pattern: str | None = None, limit: int = 200) -> list[RepoFileMatch]:
        entries = self.workspace_inspector.list_files(".", recursive=True, limit=limit * 10)[
            "entries"
        ]
        matches: list[RepoFileMatch] = []
        for entry in entries:
            if not entry.get("is_file"):
                continue
            relative_path = str(entry["path"])
            if pattern and not (
                fnmatch.fnmatch(relative_path, pattern)
                or fnmatch.fnmatch(Path(relative_path).name, pattern)
            ):
                continue
            matches.append(
                RepoFileMatch(
                    relative_path=relative_path,
                    size_bytes=entry.get("size_bytes"),
                    match_reason="pattern" if pattern else "listed_file",
                    attrs={"read_only": True},
                )
            )
            if len(matches) >= limit:
                break
        return matches

    def scan_tree(self, limit: int = 500) -> dict[str, Any]:
        return self.workspace_inspector.summarize_tree(".", max_depth=8, limit=limit)

    def candidate_code_files(self, limit: int = 500) -> list[RepoFileMatch]:
        matches: list[RepoFileMatch] = []
        for item in self.find_files(limit=limit):
            suffix = Path(item.relative_path).suffix.lower()
            if suffix in CODE_FILE_EXTENSIONS:
                matches.append(
                    RepoFileMatch(
                        relative_path=item.relative_path,
                        size_bytes=item.size_bytes,
                        match_reason="candidate_code_extension",
                        attrs={
                            **item.attrs,
                            "extension": suffix,
                            "read_only": True,
                        },
                    )
                )
            if len(matches) >= limit:
                break
        return matches
