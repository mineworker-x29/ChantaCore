from __future__ import annotations

from chanta_core.workspace import WorkspaceAccessError, WorkspaceInspector


def main() -> None:
    inspector = WorkspaceInspector()
    root = inspector.get_workspace_root()
    tree = inspector.summarize_tree(".", max_depth=1, limit=20)
    print(f"Workspace root: {root['workspace_root_name']}")
    print(
        "Tree summary: "
        f"{tree['file_count']} files, "
        f"{tree['directory_count']} directories, "
        f"{tree['skipped_count']} skipped"
    )
    try:
        inspector.read_text_file(".env")
    except WorkspaceAccessError as error:
        print(f"Blocked path check: passed ({type(error).__name__})")
    else:
        print("Blocked path check: failed")


if __name__ == "__main__":
    main()
