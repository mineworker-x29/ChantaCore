"""Main screen marker for the Schumpeter Textual app."""

from __future__ import annotations


APP_ROOT_ID = "app-root"
MAIN_BODY_ID = "main-body"
CHAT_PANEL_ID = "chat-panel"
PALETTE_REGION_ID = "palette-region"
INPUT_REGION_ID = "input-region"
STATUS_REGION_ID = "status-region"
HELP_MODAL_ID = "help-modal"
MAIN_SCREEN_REGIONS = ("sidebar", "chat-panel", "palette-region", "input-region", "status-region")
PALETTE_ANCHOR = "above_input"
PALETTE_MAY_COVER_INPUT = False
HELP_MODAL_OWNS_FOCUS = True


__all__ = [
    "APP_ROOT_ID",
    "MAIN_BODY_ID",
    "CHAT_PANEL_ID",
    "PALETTE_REGION_ID",
    "INPUT_REGION_ID",
    "STATUS_REGION_ID",
    "HELP_MODAL_ID",
    "MAIN_SCREEN_REGIONS",
    "PALETTE_ANCHOR",
    "PALETTE_MAY_COVER_INPUT",
    "HELP_MODAL_OWNS_FOCUS",
]
