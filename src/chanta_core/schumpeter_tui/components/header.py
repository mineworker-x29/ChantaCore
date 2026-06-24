"""Header component."""

from __future__ import annotations

from chanta_core.schumpeter_tui.components.sidebar import V0439ComponentKind, _result
from chanta_core.schumpeter_tui.state import V0439UIState


def render_v0439_header(state: V0439UIState):
    return _result(V0439ComponentKind.HEADER.value, ("Welcome to Schumpeter", "Type /help for commands or start with a work request."))


__all__ = ["render_v0439_header"]
