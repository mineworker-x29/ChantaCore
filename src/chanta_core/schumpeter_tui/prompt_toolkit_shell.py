"""Lazy optional prompt_toolkit shell for v0.43.10."""

from __future__ import annotations

from typing import Sequence

from chanta_core.schumpeter_tui.app import complete_v04310_slash_command, create_v04310_prompt_toolkit_policy
from chanta_core.schumpeter_tui.plain_shell import run_v04310_plain_tui


def run_v04310_prompt_toolkit_tui(inputs: Sequence[str] = (), width: int = 100) -> int:
    policy = create_v04310_prompt_toolkit_policy()
    if inputs or not policy.prompt_toolkit_supported:
        return run_v04310_plain_tui(inputs, width)
    try:
        from prompt_toolkit import prompt
        from prompt_toolkit.completion import Completer, Completion
    except Exception:
        return run_v04310_plain_tui(inputs, width)

    from chanta_core.schumpeter_tui.app_state import create_v04310_tui_app_state
    from chanta_core.schumpeter_tui.runtime_adapter import V04310RuntimeAdapter
    from chanta_core.schumpeter_tui.turn_dispatch import apply_v04310_dispatch_result, dispatch_v04310_turn
    from chanta_core.schumpeter_tui.turn_renderer import render_v04310_plain_header, render_v04310_plain_turn

    class SlashCompleter(Completer):
        def get_completions(self, document, complete_event):
            text = document.text_before_cursor
            if not text.startswith("/"):
                return
            for command in complete_v04310_slash_command(text):
                yield Completion(command + (" " if " " not in command else ""), start_position=-len(text), display=command)

    adapter = V04310RuntimeAdapter()
    app_state = create_v04310_tui_app_state(adapter.collect_ui_snapshot())
    print(render_v04310_plain_header(app_state, width))
    while True:
        try:
            raw = prompt("> ", completer=SlashCompleter(), complete_while_typing=True)
        except (EOFError, KeyboardInterrupt):
            print("Schumpeter session closed.")
            return 0
        result = dispatch_v04310_turn(raw, adapter)
        app_state = apply_v04310_dispatch_result(app_state, result)
        print(render_v04310_plain_turn(result))
        if result.app_should_exit:
            print("Schumpeter session closed.")
            return 0


__all__ = ["run_v04310_prompt_toolkit_tui"]
