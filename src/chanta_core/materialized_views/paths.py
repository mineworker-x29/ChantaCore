from __future__ import annotations

from pathlib import Path

DEFAULT_CHANTA_DIRNAME = ".chanta"
MEMORY_VIEW_FILENAME = "MEMORY.md"
PROJECT_VIEW_FILENAME = "PROJECT.md"
USER_VIEW_FILENAME = "USER.md"
PIG_GUIDANCE_VIEW_FILENAME = "PIG_GUIDANCE.md"
CONTEXT_RULES_VIEW_FILENAME = "CONTEXT_RULES.md"


def get_chanta_dir(root: Path | str) -> Path:
    return Path(root) / DEFAULT_CHANTA_DIRNAME


def get_default_view_paths(root: Path | str) -> dict[str, Path]:
    chanta_dir = get_chanta_dir(root)
    return {
        "memory": chanta_dir / MEMORY_VIEW_FILENAME,
        "project": chanta_dir / PROJECT_VIEW_FILENAME,
        "user": chanta_dir / USER_VIEW_FILENAME,
        "pig_guidance": chanta_dir / PIG_GUIDANCE_VIEW_FILENAME,
        "context_rules": chanta_dir / CONTEXT_RULES_VIEW_FILENAME,
    }
