from __future__ import annotations

from chanta_core.repo import RepoSearchService
from chanta_core.workspace import WorkspaceInspector


def main() -> None:
    service = RepoSearchService(WorkspaceInspector())
    files = service.find_files("*.py", limit=10)
    matches = service.search_text("class", limit=10, case_sensitive=False)
    print(f"File matches: {len(files.file_matches)}")
    for item in files.file_matches[:5]:
        print(f"- {item.relative_path}")
    print(f"Text matches: {len(matches.matches)}")
    for item in matches.matches[:5]:
        print(f"- {item.relative_path}:{item.line_number}: {item.line_text}")


if __name__ == "__main__":
    main()
