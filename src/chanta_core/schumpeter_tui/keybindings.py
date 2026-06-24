"""Key binding policies for Schumpeter TUI."""

from dataclasses import dataclass

from chanta_core.schumpeter_tui.app import create_v04310_key_binding_policy


@dataclass(frozen=True)
class V043112SlashPaletteKeyboardPolicy:
    slash_opens_palette: bool
    ctrl_p_opens_palette: bool
    up_down_navigate: bool
    tab_inserts_selection: bool
    enter_inserts_selection_when_palette_open: bool
    enter_executes_only_when_palette_closed: bool
    escape_closes_palette: bool
    command_executes_before_final_submit: bool
    production_certified: bool


@dataclass(frozen=True)
class V0431111HelpModalKeyboardPolicy:
    escape_closes_help: bool
    q_closes_help: bool
    f1_toggles_help: bool
    ordinary_typing_trapped: bool
    slash_palette_blocked_while_open: bool
    scroll_keys_documented: tuple[str, ...]
    production_certified: bool


def create_v043112_slash_palette_keyboard_policy() -> V043112SlashPaletteKeyboardPolicy:
    return V043112SlashPaletteKeyboardPolicy(
        slash_opens_palette=True,
        ctrl_p_opens_palette=True,
        up_down_navigate=True,
        tab_inserts_selection=True,
        enter_inserts_selection_when_palette_open=True,
        enter_executes_only_when_palette_closed=True,
        escape_closes_palette=True,
        command_executes_before_final_submit=False,
        production_certified=False,
    )


def create_v0431111_help_modal_keyboard_policy() -> V0431111HelpModalKeyboardPolicy:
    return V0431111HelpModalKeyboardPolicy(
        escape_closes_help=True,
        q_closes_help=True,
        f1_toggles_help=True,
        ordinary_typing_trapped=True,
        slash_palette_blocked_while_open=True,
        scroll_keys_documented=("up", "down", "pageup", "pagedown"),
        production_certified=False,
    )


__all__ = [
    "create_v04310_key_binding_policy",
    "V043112SlashPaletteKeyboardPolicy",
    "create_v043112_slash_palette_keyboard_policy",
    "V0431111HelpModalKeyboardPolicy",
    "create_v0431111_help_modal_keyboard_policy",
]
