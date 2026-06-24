"""Focusable Help modal boundary."""

from textual.widgets import Static

from chanta_core.schumpeter_tui.help_surface import HELP_MODAL_FOOTER_HINT, render_v04310_help


HELP_MODAL_ID = "help-modal"
HELP_MODAL_CLOSE_KEYS = ("escape", "q")
HELP_MODAL_SCROLL_KEYS = ("up", "down", "pageup", "pagedown")


class HelpModal(Static, can_focus=True):
    """Static help content that can own keyboard focus while open."""


def help_modal_text(topic: str = "/help") -> str:
    return render_v04310_help(topic).rendered_text


__all__ = [
    "HELP_MODAL_ID",
    "HELP_MODAL_CLOSE_KEYS",
    "HELP_MODAL_SCROLL_KEYS",
    "HELP_MODAL_FOOTER_HINT",
    "HelpModal",
    "help_modal_text",
]
