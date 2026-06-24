"""Layout contract and small display-width-safe frame helpers."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from chanta_core.schumpeter_tui.display_width import pad_to_display_width_v0439
from chanta_core.schumpeter_tui.theme import V0439ThemeGlyphSet, create_v0439_theme_glyphs


class V0439PaneKind(StrEnum):
    SIDEBAR = "sidebar"
    MAIN_CHAT = "main_chat"
    INPUT_BOX = "input_box"
    STATUS_BAR = "status_bar"
    COMMAND_PALETTE = "command_palette"
    HEADER = "header"
    UNKNOWN = "unknown"


class V0439LayoutMode(StrEnum):
    TWO_COLUMN = "two_column"
    STACKED_COMPACT = "stacked_compact"
    PLAIN = "plain"
    SNAPSHOT = "snapshot"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V0439LayoutPolicy:
    policy_id: str
    default_width: int
    sidebar_width: int
    min_width_two_column: int
    min_width_stacked: int
    use_display_width: bool
    use_naive_len_for_layout: bool
    fallback_to_stacked_when_narrow: bool
    fallback_to_plain_when_no_unicode: bool
    production_certified: bool


@dataclass(frozen=True)
class V0439LayoutFrame:
    frame_id: str
    width: int
    height: int | None
    layout_mode: str
    sidebar_width: int
    main_width: int
    input_width: int
    status_width: int
    production_certified: bool


def create_v0439_layout_policy(**overrides: Any) -> V0439LayoutPolicy:
    defaults = {
        "policy_id": "v0439-layout-policy",
        "default_width": 120,
        "sidebar_width": 30,
        "min_width_two_column": 90,
        "min_width_stacked": 60,
        "use_display_width": True,
        "use_naive_len_for_layout": False,
        "fallback_to_stacked_when_narrow": True,
        "fallback_to_plain_when_no_unicode": True,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0439LayoutPolicy(**defaults)


def create_v0439_layout_frame(
    width: int = 120,
    height: int | None = None,
    plain: bool = False,
    **overrides: Any,
) -> V0439LayoutFrame:
    policy = create_v0439_layout_policy()
    actual_width = max(40, int(width))
    mode = V0439LayoutMode.PLAIN.value if plain else V0439LayoutMode.TWO_COLUMN.value
    if not plain and actual_width < policy.min_width_two_column:
        mode = V0439LayoutMode.STACKED_COMPACT.value
    sidebar_width = policy.sidebar_width if mode == V0439LayoutMode.TWO_COLUMN.value else actual_width
    main_width = actual_width - sidebar_width - 1 if mode == V0439LayoutMode.TWO_COLUMN.value else actual_width
    defaults = {
        "frame_id": "v0439-layout-frame",
        "width": actual_width,
        "height": height,
        "layout_mode": mode,
        "sidebar_width": sidebar_width,
        "main_width": max(1, main_width),
        "input_width": max(1, main_width),
        "status_width": actual_width,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0439LayoutFrame(**defaults)


def bordered_row_v0439(left: str, right: str, left_width: int, right_width: int, glyphs: V0439ThemeGlyphSet | None = None) -> str:
    glyphs = glyphs or create_v0439_theme_glyphs()
    return f"{glyphs.vertical}{pad_to_display_width_v0439(left, left_width)}{glyphs.vertical}{pad_to_display_width_v0439(right, right_width)}{glyphs.vertical}"


def horizontal_rule_v0439(left_width: int, right_width: int, left: str, middle: str, right: str, glyphs: V0439ThemeGlyphSet | None = None) -> str:
    glyphs = glyphs or create_v0439_theme_glyphs()
    return f"{left}{glyphs.horizontal * left_width}{middle}{glyphs.horizontal * right_width}{right}"


__all__ = [name for name in globals() if name.startswith("V0439") or name.startswith("create_v0439") or name.endswith("_v0439")]
