"""Input box component."""

from __future__ import annotations

from chanta_core.schumpeter_tui.components.sidebar import V0439ComponentKind, _result
from chanta_core.schumpeter_tui.state import V0439UIState


def render_v0439_input_box(state: V0439UIState):
    return _result(V0439ComponentKind.INPUT_BOX.value, ("Input", "Ask Schumpeter anything..."))


__all__ = ["render_v0439_input_box"]
