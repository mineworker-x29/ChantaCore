"""Theme and glyph contract for deterministic v0.43.9 snapshots."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class V0439ThemeGlyphSet:
    horizontal: str
    vertical: str
    top_left: str
    top_right: str
    bottom_left: str
    bottom_right: str
    tee_right: str
    tee_left: str
    tee_down: str
    tee_up: str
    cross: str
    input_top_left: str
    input_top_right: str
    input_bottom_left: str
    input_bottom_right: str
    input_horizontal: str
    input_vertical: str
    status_ok: str
    status_none: str


def create_v0439_theme_glyphs(plain: bool = False, **overrides: Any) -> V0439ThemeGlyphSet:
    if plain:
        defaults = {
            "horizontal": "-",
            "vertical": "|",
            "top_left": "+",
            "top_right": "+",
            "bottom_left": "+",
            "bottom_right": "+",
            "tee_right": "+",
            "tee_left": "+",
            "tee_down": "+",
            "tee_up": "+",
            "cross": "+",
            "input_top_left": "+",
            "input_top_right": "+",
            "input_bottom_left": "+",
            "input_bottom_right": "+",
            "input_horizontal": "-",
            "input_vertical": "|",
            "status_ok": "*",
            "status_none": "o",
        }
    else:
        defaults = {
            "horizontal": "─",
            "vertical": "│",
            "top_left": "┌",
            "top_right": "┐",
            "bottom_left": "└",
            "bottom_right": "┘",
            "tee_right": "├",
            "tee_left": "┤",
            "tee_down": "┬",
            "tee_up": "┴",
            "cross": "┼",
            "input_top_left": "╭",
            "input_top_right": "╮",
            "input_bottom_left": "╰",
            "input_bottom_right": "╯",
            "input_horizontal": "─",
            "input_vertical": "│",
            "status_ok": "●",
            "status_none": "○",
        }
    defaults.update(overrides)
    return V0439ThemeGlyphSet(**defaults)


__all__ = ["V0439ThemeGlyphSet", "create_v0439_theme_glyphs"]
