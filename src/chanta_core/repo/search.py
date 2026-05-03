from __future__ import annotations

from chanta_core.repo.models import RepoSearchResult, RepoTextMatch
from chanta_core.repo.scanner import RepoScanner
from chanta_core.workspace import WorkspaceInspector
from chanta_core.workspace.errors import WorkspaceError


class RepoSearchService:
    def __init__(
        self,
        workspace_inspector: WorkspaceInspector,
        scanner: RepoScanner | None = None,
    ) -> None:
        self.workspace_inspector = workspace_inspector
        self.scanner = scanner or RepoScanner(workspace_inspector)

    def search_text(
        self,
        query: str,
        path: str = ".",
        limit: int = 100,
        case_sensitive: bool = False,
    ) -> RepoSearchResult:
        query = str(query)
        if not query:
            return RepoSearchResult(query=query, result_attrs={"read_only": True})
        entries = self.workspace_inspector.list_files(path, recursive=True, limit=limit * 10)[
            "entries"
        ]
        needle = query if case_sensitive else query.lower()
        matches: list[RepoTextMatch] = []
        files_scanned = 0
        files_skipped = 0
        for entry in entries:
            if not entry.get("is_file"):
                continue
            relative_path = str(entry["path"])
            try:
                text_result = self.workspace_inspector.read_text_file(relative_path)
            except WorkspaceError:
                files_skipped += 1
                continue
            files_scanned += 1
            for line_number, line in enumerate(str(text_result["text"]).splitlines(), start=1):
                haystack = line if case_sensitive else line.lower()
                if needle not in haystack:
                    continue
                matches.append(
                    RepoTextMatch(
                        relative_path=relative_path,
                        line_number=line_number,
                        line_text=_truncate(line),
                        match_text=query,
                        attrs={
                            "case_sensitive": case_sensitive,
                            "read_only": True,
                        },
                    )
                )
                if len(matches) >= limit:
                    return RepoSearchResult(
                        query=query,
                        matches=matches,
                        result_attrs={
                            "files_scanned": files_scanned,
                            "files_skipped": files_skipped,
                            "limit": limit,
                            "read_only": True,
                        },
                    )
        return RepoSearchResult(
            query=query,
            matches=matches,
            result_attrs={
                "files_scanned": files_scanned,
                "files_skipped": files_skipped,
                "limit": limit,
                "read_only": True,
            },
        )

    def find_files(self, name_pattern: str, limit: int = 100) -> RepoSearchResult:
        file_matches = self.scanner.find_files(pattern=name_pattern, limit=limit)
        return RepoSearchResult(
            query=name_pattern,
            file_matches=file_matches,
            result_attrs={"limit": limit, "read_only": True},
        )


def _truncate(line: str, max_length: int = 300) -> str:
    if len(line) <= max_length:
        return line
    return line[: max_length - 3] + "..."
