"""Display-width helpers for the v0.43.9 Schumpeter TUI snapshot contract."""

from __future__ import annotations

import re
import unicodedata


ANSI_ESCAPE_PATTERN_V0439 = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def strip_ansi_v0439(text: str) -> str:
    return ANSI_ESCAPE_PATTERN_V0439.sub("", str(text))


def display_width_v0439(text: str) -> int:
    width = 0
    for char in strip_ansi_v0439(text):
        if char == "\t":
            width += 4
            continue
        if unicodedata.combining(char):
            continue
        category = unicodedata.category(char)
        if category.startswith("C") and char not in {"\n", "\r"}:
            continue
        width += 2 if unicodedata.east_asian_width(char) in {"F", "W"} else 1
    return width


def truncate_to_display_width_v0439(text: str, width: int) -> str:
    target = max(0, int(width))
    output: list[str] = []
    used = 0
    for char in strip_ansi_v0439(text):
        char_width = display_width_v0439(char)
        if used + char_width > target:
            break
        output.append(char)
        used += char_width
    return "".join(output)


def pad_to_display_width_v0439(text: str, width: int) -> str:
    target = max(0, int(width))
    value = truncate_to_display_width_v0439(text, target)
    return value + (" " * max(0, target - display_width_v0439(value)))


def assert_v0439_lines_within_width(text: str, width: int) -> bool:
    target = max(1, int(width))
    return all(display_width_v0439(line) <= target for line in str(text).splitlines())


__all__ = [
    "ANSI_ESCAPE_PATTERN_V0439",
    "strip_ansi_v0439",
    "display_width_v0439",
    "truncate_to_display_width_v0439",
    "pad_to_display_width_v0439",
    "assert_v0439_lines_within_width",
]
