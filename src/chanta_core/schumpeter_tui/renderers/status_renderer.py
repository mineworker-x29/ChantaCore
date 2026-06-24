"""Status renderer for compact status surfaces."""

from __future__ import annotations

from chanta_core.schumpeter_tui.state import V0439DisplayMessage
from chanta_core.schumpeter_tui.widgets.message_view import render_v043117_card_text


def render_v0439_status(message: V0439DisplayMessage, width: int = 78) -> str:
    return render_v043117_card_text(message.text, kind="status", width=width)


__all__ = ["render_v0439_status"]
