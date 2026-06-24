"""Plain interactive turn renderer for v0.43.10.1."""

from __future__ import annotations

from typing import Sequence

from chanta_core.schumpeter_tui.app import render_v04310_snapshot
from chanta_core.schumpeter_tui.app_state import V04310TUIAppState, create_v04310_tui_app_state
from chanta_core.schumpeter_tui.runtime_adapter import V04310RuntimeAdapter
from chanta_core.schumpeter_tui.turn_dispatch import (
    V04310TurnDispatchResult,
    apply_v04310_dispatch_result,
    create_v04310_interaction_golden_result,
    dispatch_v04310_turn,
)
from chanta_core.schumpeter_tui.widgets.message_view import render_v043117_card_text


TURN_LABELS = {
    "assistant": "Schumpeter>",
    "artifact": "Artifact>",
    "diagnostic": "Diagnostic>",
    "status": "Status>",
    "error": "Error>",
    "system_notice": "Notice>",
}


def render_v04310_plain_header(app_state: V04310TUIAppState, width: int = 100) -> str:
    return render_v04310_snapshot(width=width, plain=True, app_state=app_state).rendered_text


def render_v04310_plain_turn(result: V04310TurnDispatchResult) -> str:
    return "\n\n".join(
        (
            render_v043117_card_text(result.input_text, "user", width=78),
            render_v043117_card_text(result.rendered_text, result.message_kind, width=78),
        )
    ).rstrip()


def render_v04310_plain_prompt() -> str:
    return ">"


def run_v04310_plain_interaction_sequence(
    inputs: Sequence[str],
    width: int = 100,
    adapter: V04310RuntimeAdapter | None = None,
) -> tuple[str, V04310TUIAppState]:
    adapter = adapter or V04310RuntimeAdapter()
    app_state = create_v04310_tui_app_state(adapter.collect_ui_snapshot())
    rendered_blocks = [render_v04310_plain_header(app_state, width)]
    for raw in inputs:
        result = dispatch_v04310_turn(raw, adapter)
        app_state = apply_v04310_dispatch_result(app_state, result)
        rendered_blocks.append(render_v04310_plain_turn(result))
        if result.app_should_exit:
            break
    return "\n".join(block for block in rendered_blocks if block), app_state


def execute_v04310_interaction_golden_case(width: int = 100):
    from chanta_core.schumpeter_tui.turn_dispatch import create_v04310_interaction_golden_case

    case = create_v04310_interaction_golden_case()
    rendered, _state = run_v04310_plain_interaction_sequence(case.inputs, width=width)
    return create_v04310_interaction_golden_result(rendered)


__all__ = [name for name in globals() if name.startswith("render_v04310") or name.startswith("run_v04310") or name.startswith("execute_v04310")]
