from pathlib import Path

import pytest

from chanta_core.schumpeter_tui.command_registry import list_v043111_command_names
from chanta_core.schumpeter_tui.fullscreen import create_v04311_textual_app, render_v04311_text_snapshot
from chanta_core.schumpeter_tui.help_surface import render_v04310_help
from chanta_core.schumpeter_tui.keybindings import create_v043112_slash_palette_keyboard_policy
from chanta_core.schumpeter_tui.state import (
    create_v043112_slash_palette_input_visibility_policy,
    create_v043112_slash_palette_layout_policy,
    create_v043112_slash_palette_selection_state,
)
from chanta_core.schumpeter_tui.testing.fake_runtime_adapter import V04311FakeRuntimeAdapter
from chanta_core.schumpeter_tui.widgets.slash_palette import (
    create_v043112_palette_state,
    insert_v043112_selected_command,
    move_v043112_palette_selection,
    render_v043112_palette_text,
)


ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "versions" / "v0.43" / "v0.43.11.2_non_obstructive_keyboard_slash_palette_restore.md"


def test_slash_palette_state_declared():
    state = create_v043112_palette_state("/s")
    assert state.visible is True
    assert state.input_remains_visible is True
    assert state.command_executed_by_selection is False
    assert state.production_certified is False


def test_slash_palette_layout_policy_never_covers_input():
    policy = create_v043112_slash_palette_layout_policy()
    assert policy.anchor_above_input is True
    assert policy.may_cover_input is False
    assert policy.reserve_input_line is True
    assert policy.reserve_status_line is True
    assert policy.compact_when_narrow is True
    assert policy.scroll_when_overflow is True


@pytest.mark.anyio
async def test_slash_opens_palette():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        input_bar = pilot.app.query_one("#main-input")
        input_bar.focus()
        input_bar.value = "/"
        await pilot.pause()
        assert not pilot.app.query_one("#slash-palette").has_class("hidden")


@pytest.mark.anyio
async def test_ctrl_p_opens_palette():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        pilot.app.action_toggle_palette()
        await pilot.pause()
        assert not pilot.app.query_one("#slash-palette").has_class("hidden")


@pytest.mark.anyio
async def test_palette_anchors_above_input():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        pilot.app.action_toggle_palette()
        await pilot.pause()
        children = [child.id for child in pilot.app.query_one("#app-root").children]
        assert children.index("palette-region") < children.index("input-region")
        assert pilot.app.palette_anchor == "above_input"


@pytest.mark.anyio
async def test_input_text_visible_when_palette_open():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        input_bar = pilot.app.query_one("#main-input")
        input_bar.focus()
        input_bar.value = "/"
        await pilot.pause()
        assert input_bar.value == "/"
        assert pilot.app.input_visible_with_palette is True


@pytest.mark.anyio
async def test_input_text_visible_after_filtering():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        input_bar = pilot.app.query_one("#main-input")
        input_bar.focus()
        input_bar.value = "/s"
        await pilot.pause()
        assert input_bar.value == "/s"
        assert "/summary" in pilot.app.palette_plain
        assert "/status" in pilot.app.palette_plain


def test_palette_filter_s_shows_summary_and_status():
    text = render_v043112_palette_text(create_v043112_palette_state("/s"))
    assert "/summary" in text
    assert "/status" in text


def test_palette_filter_grounded_shows_grounded_commands():
    text = render_v043112_palette_text(create_v043112_palette_state("/grounded"))
    assert "/grounded-summary" in text
    assert "/grounded-handoff" in text


def test_down_arrow_moves_selection_down():
    state = create_v043112_palette_state("/")
    state, result = move_v043112_palette_selection(state, 1)
    assert state.selected_index == 1
    assert result.moved is True
    assert result.command_executed is False


def test_up_arrow_moves_selection_up():
    state = create_v043112_palette_state("/", selected_index=2)
    state, result = move_v043112_palette_selection(state, -1)
    assert state.selected_index == 1
    assert result.command_executed is False


def test_selection_wrap_or_clamp_policy_defined():
    policy = create_v043112_slash_palette_selection_state(selected_index=0, total_items=5)
    assert policy.wrap_selection is False
    assert policy.clamp_selection is True


@pytest.mark.anyio
async def test_enter_inserts_selected_command_without_execution():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        input_bar = pilot.app.query_one("#main-input")
        input_bar.focus()
        input_bar.value = "/s"
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()
        assert input_bar.value.startswith("/summary")
        assert pilot.app.palette_selection_executed_command is False
        assert "Summary" not in pilot.app.chat_plain


@pytest.mark.anyio
async def test_tab_inserts_selected_command_without_execution():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        input_bar = pilot.app.query_one("#main-input")
        input_bar.focus()
        input_bar.value = "/s"
        await pilot.pause()
        await pilot.press("tab")
        await pilot.pause()
        assert input_bar.value.startswith("/summary")
        assert pilot.app.palette_selection_executed_command is False


def test_selected_command_with_required_argument_inserts_trailing_space():
    state = create_v043112_palette_state("/summary")
    result = insert_v043112_selected_command(state)
    assert result.inserted_text == "/summary "
    assert result.requires_argument is True
    assert result.command_executed is False


@pytest.mark.anyio
async def test_esc_closes_palette_and_preserves_input():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        input_bar = pilot.app.query_one("#main-input")
        input_bar.focus()
        input_bar.value = "/s"
        await pilot.pause()
        await pilot.press("escape")
        await pilot.pause()
        assert pilot.app.query_one("#slash-palette").has_class("hidden")
        assert input_bar.value == "/s"


@pytest.mark.anyio
async def test_backspace_updates_filter_and_keeps_input_visible():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        input_bar = pilot.app.query_one("#main-input")
        input_bar.focus()
        input_bar.value = "/grounded"
        await pilot.pause()
        input_bar.value = "/s"
        await pilot.pause()
        assert input_bar.value == "/s"
        assert "/status" in pilot.app.palette_plain


def test_palette_scrolls_when_many_commands():
    state = create_v043112_palette_state("/", max_visible_items=5)
    text = render_v043112_palette_text(state)
    assert "... " in text
    assert len(text.splitlines()) <= 7


def test_palette_compacts_in_narrow_terminal():
    state = create_v043112_palette_state("/")
    text = render_v043112_palette_text(state, width=40, compact=True)
    assert "Commands" in text
    assert "/help" in text


@pytest.mark.anyio
async def test_palette_does_not_append_to_transcript():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        before = pilot.app.chat_plain
        pilot.app.action_toggle_palette()
        await pilot.pause()
        assert pilot.app.chat_plain == before


def test_palette_uses_canonical_registry():
    assert set(create_v043112_palette_state("/").filtered_commands) == set(list_v043111_command_names("/"))


def test_palette_does_not_execute_command_on_navigation():
    state = create_v043112_palette_state("/")
    _state, result = move_v043112_palette_selection(state, 1)
    assert result.command_executed is False


def test_palette_does_not_call_provider():
    state = create_v043112_palette_state("/")
    assert state.provider_invoked is False


def test_palette_does_not_run_shell_git():
    state = create_v043112_palette_state("/")
    assert state.shell_executed is False


def test_palette_does_not_read_repo_workspace():
    state = create_v043112_palette_state("/")
    assert state.repo_search_used is False
    assert state.workspace_read_opened is False


def test_palette_does_not_mutate_memory():
    state = create_v043112_palette_state("/")
    assert state.memory_mutated is False


def test_palette_snapshot_wide_does_not_cover_input():
    result = render_v04311_text_snapshot(140, 42, include_palette=True)
    assert result.contains_palette is True
    assert result.contains_input is True
    assert result.rendered_text.index("Commands") < result.rendered_text.index("Input")


def test_palette_snapshot_narrow_does_not_cover_input():
    result = render_v04311_text_snapshot(80, 24, include_palette=True)
    assert result.contains_palette is True
    assert result.contains_input is True
    assert result.rendered_text.index("Commands") < result.rendered_text.index("Input")


def test_palette_snapshot_has_no_raw_metadata():
    text = render_v04311_text_snapshot(120, 36, include_palette=True).rendered_text
    for forbidden in ("provider_invoked", "shell=false", "production_certified=false", "base_url", "api_key"):
        assert forbidden not in text


def test_palette_regression_help_and_status_still_work():
    assert "Schumpeter Help" in render_v04310_help("/help").rendered_text
    assert "Safety Help" in render_v04310_help("/help safety").rendered_text


def test_input_visibility_policy_declared():
    policy = create_v043112_slash_palette_input_visibility_policy()
    assert policy.input_text_visible_when_open is True
    assert policy.palette_may_obscure_input is False


def test_keyboard_policy_declared():
    policy = create_v043112_slash_palette_keyboard_policy()
    assert policy.enter_inserts_selection_when_palette_open is True
    assert policy.enter_executes_only_when_palette_closed is True
    assert policy.command_executes_before_final_submit is False


def test_no_forbidden_runtime_call_patterns():
    scanned = (
        ROOT / "src" / "chanta_core" / "schumpeter_tui" / "widgets" / "slash_palette.py",
        ROOT / "src" / "chanta_core" / "schumpeter_tui" / "fullscreen.py",
        ROOT / "src" / "chanta_core" / "schumpeter_tui" / "state.py",
        ROOT / "src" / "chanta_core" / "schumpeter_tui" / "keybindings.py",
    )
    text = "\n".join(path.read_text(encoding="utf-8") for path in scanned)
    forbidden_patterns = (
        "sub" + "process",
        "shell" + "=True",
        "os." + "system",
        "ev" + "al(",
        "ex" + "ec(",
        "git " + "status",
        "os." + "walk",
        "Path." + "rglob",
        "provider completion " + "call",
        "CORE_MEMORY " + "write",
    )
    for forbidden in forbidden_patterns:
        assert forbidden not in text


def test_restore_document_exists_with_required_sections():
    text = DOC_PATH.read_text(encoding="utf-8")
    for title in (
        "Restore Purpose",
        "Non-Obstructive Palette Contract",
        "Input Visibility Invariant",
        "Keyboard Navigation Contract",
        "Selection vs Execution Rule",
        "Safety Boundary",
        "Copy-Paste Restore Prompt",
    ):
        assert f"## {title}" in text
