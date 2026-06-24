"""Chat view component."""

from __future__ import annotations

from chanta_core.schumpeter_tui.components.sidebar import V0439ComponentKind, _result
from chanta_core.schumpeter_tui.renderers.artifact_renderer import render_v0439_artifact
from chanta_core.schumpeter_tui.renderers.diagnostic_renderer import render_v0439_diagnostic
from chanta_core.schumpeter_tui.renderers.error_renderer import render_v0439_error
from chanta_core.schumpeter_tui.renderers.message_renderer import render_v0439_message
from chanta_core.schumpeter_tui.renderers.status_renderer import render_v0439_status
from chanta_core.schumpeter_tui.state import V0439DisplayMessageKind, V0439UIState


def render_v0439_chat_view(state: V0439UIState):
    lines = ["Welcome to Schumpeter", "Type /help for commands or start with a work request.", ""]
    for message in state.messages:
        if message.kind == V0439DisplayMessageKind.ARTIFACT.value:
            rendered = render_v0439_artifact(message)
        elif message.kind == V0439DisplayMessageKind.DIAGNOSTIC.value:
            rendered = render_v0439_diagnostic(message)
        elif message.kind == V0439DisplayMessageKind.STATUS.value:
            rendered = render_v0439_status(message)
        elif message.kind == V0439DisplayMessageKind.ERROR.value:
            rendered = render_v0439_error(message)
        else:
            rendered = render_v0439_message(message)
        lines.extend(rendered.splitlines())
        lines.append("")
    return _result(V0439ComponentKind.CHAT_VIEW.value, tuple(lines))


__all__ = ["render_v0439_chat_view"]
