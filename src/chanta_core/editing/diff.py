from __future__ import annotations

import difflib


def create_unified_diff(
    *,
    original_text: str,
    proposed_text: str,
    fromfile: str = "original",
    tofile: str = "proposed",
) -> str:
    return "".join(
        difflib.unified_diff(
            original_text.splitlines(keepends=True),
            proposed_text.splitlines(keepends=True),
            fromfile=fromfile,
            tofile=tofile,
        )
    )


def safe_preview(text: str, max_chars: int = 2000) -> str:
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3] + "..."
