"""Command palette component backed by the v0.43.8.2 slash registry."""

from __future__ import annotations

from chanta_core.schumpeter_tui.command_registry import list_v0439_palette_commands
from chanta_core.schumpeter_tui.components.sidebar import V0439ComponentKind, _result
from chanta_core.schumpeter_tui.state import V0439UIState


def render_v0439_command_palette(state: V0439UIState):
    commands = list_v0439_palette_commands("/", None)
    required = ("/summary", "/todo", "/memo", "/decision", "/handoff", "/status", "/exit")
    primary = tuple(command for command in required if command in commands)
    return _result(V0439ComponentKind.COMMAND_PALETTE.value, ("Command Palette",) + primary)


__all__ = ["render_v0439_command_palette"]
