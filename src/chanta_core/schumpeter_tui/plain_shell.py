"""Plain structured shell fallback for v0.43.10."""

from __future__ import annotations

from typing import Sequence

from chanta_core.schumpeter_tui.app_state import create_v04310_tui_app_state
from chanta_core.schumpeter_tui.runtime_adapter import V04310RuntimeAdapter
from chanta_core.schumpeter_tui.turn_dispatch import apply_v04310_dispatch_result, dispatch_v04310_turn
from chanta_core.schumpeter_tui.turn_renderer import (
    render_v04310_plain_header,
    render_v04310_plain_turn,
    run_v04310_plain_interaction_sequence,
)


def run_v04310_plain_tui(inputs: Sequence[str] = (), width: int = 100) -> int:
    adapter = V04310RuntimeAdapter()
    app_state = create_v04310_tui_app_state(adapter.collect_ui_snapshot())
    print(render_v04310_plain_header(app_state, width))
    if inputs:
        for raw in inputs:
            result = dispatch_v04310_turn(raw, adapter)
            app_state = apply_v04310_dispatch_result(app_state, result)
            print(render_v04310_plain_turn(result))
            if result.app_should_exit:
                break
        return 0
    while True:
        try:
            raw = input("> ")
        except (EOFError, KeyboardInterrupt):
            print("Schumpeter session closed.")
            return 0
        result = dispatch_v04310_turn(raw, adapter)
        app_state = apply_v04310_dispatch_result(app_state, result)
        print(render_v04310_plain_turn(result))
        if result.app_should_exit:
            print("Schumpeter session closed.")
            return 0


__all__ = ["run_v04310_plain_tui", "run_v04310_plain_interaction_sequence"]
