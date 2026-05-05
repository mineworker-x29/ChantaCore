from pathlib import Path


DEFAULT_CHANTA_DIRNAME = ".chanta"
TOOLS_VIEW_FILENAME = "TOOLS.md"
TOOL_POLICY_VIEW_FILENAME = "TOOL_POLICY.md"


def get_chanta_dir(root: Path | str) -> Path:
    return Path(root) / DEFAULT_CHANTA_DIRNAME


def get_tool_view_paths(root: Path | str) -> dict[str, Path]:
    chanta_dir = get_chanta_dir(root)
    return {
        "tools": chanta_dir / TOOLS_VIEW_FILENAME,
        "tool_policy": chanta_dir / TOOL_POLICY_VIEW_FILENAME,
    }
