"""Non-obstructive slash palette helpers for the Schumpeter TUI."""

from __future__ import annotations

from chanta_core.schumpeter_tui.command_registry import (
    V043111CommandCategory,
    V043111CommandSpec,
    extract_v043111_command_argument,
    find_v043111_command_spec,
    group_v043111_command_specs,
    list_v043111_command_specs,
)
from chanta_core.schumpeter_tui.state import (
    V043112SlashPaletteInsertionResult,
    V043112SlashPaletteNavigationResult,
    V043112SlashPaletteState,
    create_v043112_slash_palette_state,
)


PALETTE_REGION_ID = "palette-region"
SLASH_PALETTE_ID = "slash-palette"
PALETTE_ANCHOR = "above_input"
PALETTE_BLOCKED_BY_HELP_MODAL = True


def create_v043112_palette_state(query: str = "/", selected_index: int = 0, visible: bool = True, max_visible_items: int = 10) -> V043112SlashPaletteState:
    specs = list_v043111_command_specs(query)
    max_index = max(0, len(specs) - 1)
    selected = min(max(0, selected_index), max_index)
    return create_v043112_slash_palette_state(
        visible=visible,
        query=query,
        selected_index=selected,
        filtered_commands=tuple(spec.command for spec in specs),
        max_visible_items=max_visible_items,
    )


def move_v043112_palette_selection(state: V043112SlashPaletteState, direction: int) -> tuple[V043112SlashPaletteState, V043112SlashPaletteNavigationResult]:
    count = len(state.filtered_commands)
    if count == 0:
        new_index = 0
    else:
        new_index = min(max(state.selected_index + direction, 0), count - 1)
    new_state = create_v043112_palette_state(state.query, new_index, state.visible, state.max_visible_items)
    return (
        new_state,
        V043112SlashPaletteNavigationResult(
            selected_index=new_index,
            moved=new_index != state.selected_index,
            command_executed=False,
            provider_invoked=False,
            shell_executed=False,
            repo_search_used=False,
            workspace_read_opened=False,
            memory_mutated=False,
            production_certified=False,
        ),
    )


def insert_v043112_selected_command(state: V043112SlashPaletteState) -> V043112SlashPaletteInsertionResult:
    command = state.filtered_commands[state.selected_index] if state.filtered_commands else state.query
    spec = find_v043111_command_spec(command)
    requires_argument = bool(spec and spec.requires_argument)
    inserted = command + (" " if requires_argument else "")
    return V043112SlashPaletteInsertionResult(
        inserted_text=inserted,
        command=command,
        requires_argument=requires_argument,
        command_executed=False,
        input_remains_visible=True,
        production_certified=False,
    )


def _visible_specs_for_state(state: V043112SlashPaletteState) -> tuple[V043111CommandSpec, ...]:
    specs = list_v043111_command_specs(state.query)
    if not specs:
        return ()
    selected_command = state.filtered_commands[state.selected_index] if state.filtered_commands else specs[0].command
    selected_spec = next((spec for spec in specs if spec.command == selected_command), specs[0])

    if state.query.strip() in {"", "/"}:
        grouped = group_v043111_command_specs(specs)
        balanced: list[V043111CommandSpec] = []
        per_category = 2
        command_budget = state.max_visible_items
        if state.max_visible_items < 8:
            command_budget = max(1, state.max_visible_items - 2)
        for category in (category.value for category in V043111CommandCategory):
            balanced.extend(grouped.get(category, ())[:per_category])
            if len(balanced) >= command_budget:
                break
        if selected_spec.command not in {spec.command for spec in balanced}:
            balanced = [selected_spec, *balanced[: max(0, command_budget - 1)]]
        return tuple(balanced[:command_budget])

    selected_position = next((index for index, spec in enumerate(specs) if spec.command == selected_spec.command), 0)
    start = 0
    if selected_position >= state.max_visible_items:
        start = selected_position - state.max_visible_items + 1
    return tuple(specs[start : start + state.max_visible_items])


def render_v043112_palette_text(state: V043112SlashPaletteState, width: int = 80, compact: bool = False) -> str:
    specs = list_v043111_command_specs(state.query)
    visible_specs = _visible_specs_for_state(state)
    selected_command = state.filtered_commands[state.selected_index] if state.filtered_commands else ""
    grouped = group_v043111_command_specs(visible_specs)
    lines = ["Commands"]
    for category in (category.value for category in V043111CommandCategory):
        items = grouped.get(category, ())
        if not items:
            continue
        lines.append(category)
        for spec in items:
            marker = ">" if spec.command == selected_command else " "
            suffix = f" [{spec.availability}]" if spec.availability != "available" else ""
            if compact:
                line = f"{marker} {spec.command:<22} {spec.short_description_ko}{suffix}"
            else:
                line = f"{marker} {spec.usage:<28} {spec.short_description_ko}{suffix}"
            lines.append(line[: max(20, width)])
    if len(specs) > state.max_visible_items:
        lines.append(f"... {len(specs) - state.max_visible_items} more")
    return "\n".join(lines)


def selectable_v043112_palette_commands(state: V043112SlashPaletteState) -> tuple[str, ...]:
    return state.filtered_commands


def render_rows_v043112_palette(state: V043112SlashPaletteState) -> tuple[tuple[str, str], ...]:
    rows: list[tuple[str, str]] = [("title", "Commands")]
    grouped = group_v043111_command_specs(_visible_specs_for_state(state))
    for category in (category.value for category in V043111CommandCategory):
        items = grouped.get(category, ())
        if not items:
            continue
        rows.append(("header", category))
        rows.extend(("command", spec.command) for spec in items)
    return tuple(rows)


def slash_palette_text(prefix: str = "/") -> str:
    return render_v043112_palette_text(create_v043112_palette_state(prefix))


def palette_query_has_argument(query: str) -> bool:
    spec = find_v043111_command_spec(query)
    return bool(spec and extract_v043111_command_argument(query, spec))


__all__ = [
    "PALETTE_REGION_ID",
    "SLASH_PALETTE_ID",
    "PALETTE_ANCHOR",
    "PALETTE_BLOCKED_BY_HELP_MODAL",
    "create_v043112_palette_state",
    "move_v043112_palette_selection",
    "insert_v043112_selected_command",
    "render_v043112_palette_text",
    "selectable_v043112_palette_commands",
    "render_rows_v043112_palette",
    "slash_palette_text",
    "palette_query_has_argument",
]
