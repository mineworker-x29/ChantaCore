from pathlib import Path

import pytest

from chanta_core.schumpeter_tui import fullscreen
from chanta_core.schumpeter_tui.fullscreen import (
    FORBIDDEN_V04311_DEFAULT_STRINGS,
    create_v04311_entrypoint_policy,
    create_v04311_textual_app,
    detect_v04311_textual,
    render_v04311_text_snapshot,
)
from chanta_core.schumpeter_tui.help_surface import render_v04310_help
from chanta_core.schumpeter_tui.testing.fake_runtime_adapter import V04311FakeRuntimeAdapter


ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "versions" / "v0.43" / "v0.43.11_schumpeter_fullscreen_tui_productization_restore.md"


def test_textual_dependency_declared_and_available_after_install():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    status = detect_v04311_textual()
    assert '"textual>=' in pyproject
    assert status.dependency_declared is True
    assert status.available is True


def test_entrypoint_policy_defaults_to_fullscreen_with_fallbacks():
    policy = create_v04311_entrypoint_policy()
    assert policy.default_start_launches_fullscreen_tui is True
    assert policy.tui_alias_launches_same_app is True
    assert policy.classic_fallback_available is True
    assert policy.plain_fallback_available is True
    assert policy.production_certified is False


def test_missing_textual_dependency_message_is_actionable():
    status = fullscreen.V04311TextualDependencyStatus(False, True, "textual", "Use chanta-cli start --classic", False)
    assert "classic" in status.actionable_message
    assert status.production_certified is False


def test_wide_layout_snapshot_has_sidebar_chat_input_footer():
    result = render_v04311_text_snapshot(140, 42)
    assert result.layout_mode == "wide"
    assert result.contains_sidebar is True
    assert result.contains_chat is True
    assert result.contains_input is True
    assert result.contains_status_bar is True


def test_medium_layout_remains_structured():
    result = render_v04311_text_snapshot(110, 32)
    assert result.layout_mode == "medium"
    assert "Schumpeter | default-personal | Provider ready" in result.rendered_text
    assert result.contains_input is True


def test_narrow_layout_collapses_safely():
    result = render_v04311_text_snapshot(80, 24)
    assert result.layout_mode == "narrow"
    assert "PI ●  Trace ●  Evidence ○  Safety ●" in result.rendered_text
    assert result.contains_input is True


def test_palette_snapshot_passes():
    result = render_v04311_text_snapshot(120, 36, include_palette=True)
    assert result.contains_palette is True
    assert "/summary" in result.rendered_text
    assert "/status" in result.rendered_text


def test_help_modal_snapshot_passes():
    result = render_v04311_text_snapshot(120, 36, include_help=True)
    assert result.contains_help_modal is True
    assert "Schumpeter Help" in result.rendered_text


def test_plain_snapshot_passes():
    result = render_v04311_text_snapshot(100, 30, plain=True)
    assert result.layout_mode == "plain"
    assert result.contains_chat is True


def test_snapshots_have_no_forbidden_default_strings():
    for result in (
        render_v04311_text_snapshot(140, 42),
        render_v04311_text_snapshot(110, 32),
        render_v04311_text_snapshot(80, 24),
        render_v04311_text_snapshot(120, 36, include_palette=True),
        render_v04311_text_snapshot(120, 36, include_help=True),
    ):
        assert result.contains_forbidden_default_strings is False
        for forbidden in FORBIDDEN_V04311_DEFAULT_STRINGS:
            assert forbidden.lower() not in result.rendered_text.lower()


def test_sidebar_contains_brand_project_session_pi_monitor_shortcuts():
    text = render_v04311_text_snapshot(140, 42).rendered_text
    for expected in ("SCHUMPETER", "PROJECT", "SESSION", "PI MONITOR", "SHORTCUTS"):
        assert expected in text
    assert "shell=false" not in text


def test_startup_message_is_clean_not_development_notice():
    text = render_v04311_text_snapshot(140, 42).rendered_text
    assert "Welcome to Schumpeter" in text
    assert "Structured TUI MVP is ready for preview" not in text


def test_fake_adapter_ui_refresh_counters_zero():
    adapter = V04311FakeRuntimeAdapter()
    adapter.collect_ui_snapshot()
    assert adapter.counters.provider_completion_count == 0
    assert adapter.counters.shell_execution_count == 0
    assert adapter.counters.repo_workspace_read_count == 0
    assert adapter.counters.memory_mutation_count == 0


def test_fake_adapter_turn_kinds_are_deterministic():
    adapter = V04311FakeRuntimeAdapter()
    assert adapter.submit_user_input("넌 누구야").message_kind == "assistant"
    assert adapter.execute_slash_command("/summary test").message_kind == "artifact"
    assert adapter.execute_slash_command("/status").message_kind == "status"
    assert adapter.execute_slash_command("/what-happened").message_kind == "diagnostic"


def test_keybindings_include_ctrl_p_f1_escape_and_ctrl_c():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    keys = {binding.key for binding in app.BINDINGS}
    assert "ctrl+p" in keys
    assert "f1" in keys
    assert "escape" in keys
    assert "ctrl+c" in keys


@pytest.mark.anyio
async def test_textual_app_mounts_with_persistent_regions():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        assert pilot.app.query_one("#sidebar") is not None
        assert pilot.app.query_one("#chat-view") is not None
        assert pilot.app.query_one("#main-input") is not None
        assert pilot.app.query_one("#status-bar") is not None


@pytest.mark.anyio
async def test_slash_palette_opens_with_ctrl_p_and_esc_closes():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        pilot.app.action_toggle_palette()
        await pilot.pause()
        assert not pilot.app.query_one("#slash-palette").has_class("hidden")
        await pilot.press("escape")
        await pilot.pause()
        assert pilot.app.query_one("#slash-palette").has_class("hidden")


@pytest.mark.anyio
async def test_help_modal_opens_with_f1_and_esc_closes():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        await pilot.press("f1")
        await pilot.pause()
        assert "Schumpeter Help" in pilot.app.help_plain
        await pilot.press("escape")
        await pilot.pause()
        assert pilot.app.query_one("#help-modal").has_class("hidden")


@pytest.mark.anyio
async def test_about_modal_opens_from_command():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        input_bar = pilot.app.query_one("#main-input")
        input_bar.focus()
        input_bar.value = "/about"
        await pilot.press("enter")
        await pilot.pause()
        assert "Runtime lineage: ChantaCore" in pilot.app.about_plain
        assert "ChantaGrowthKernel" not in pilot.app.about_plain


@pytest.mark.anyio
async def test_normal_message_and_summary_append_without_static_chrome():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        input_bar = pilot.app.query_one("#main-input")
        input_bar.focus()
        input_bar.value = "넌 누구야"
        await pilot.press("enter")
        input_bar.value = "/summary 오늘 Schumpeter 전체 UI를 테스트하고 있어."
        await pilot.press("enter")
        await pilot.pause()
        chat_text = pilot.app.chat_plain
        assert "Schumpeter" in chat_text
        assert "핵심 내용" in chat_text
        assert "PI MONITOR" not in chat_text


@pytest.mark.anyio
async def test_status_and_diagnostic_render_as_distinct_cards():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        input_bar = pilot.app.query_one("#main-input")
        input_bar.focus()
        input_bar.value = "/status"
        await pilot.press("enter")
        input_bar.value = "/what-happened"
        await pilot.press("enter")
        await pilot.pause()
        chat_text = pilot.app.chat_plain
        assert "Safety: protected" in chat_text
        assert "TUI diagnostic" in chat_text


@pytest.mark.anyio
async def test_exit_command_exits_gracefully():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        input_bar = pilot.app.query_one("#main-input")
        input_bar.focus()
        input_bar.value = "/exit"
        await pilot.press("enter")
        await pilot.pause()
        assert pilot.app.exit_requested is True


def test_help_surface_still_has_required_sections():
    text = render_v04310_help("/help commands").rendered_text
    for expected in ("Workflows", "Notes", "Evidence", "Grounded Workflows", "Status / Diagnostics", "TUI", "Safety", "Exit"):
        assert expected in text


def test_snapshot_side_effect_flags_zero():
    result = render_v04311_text_snapshot(140, 42)
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False
    assert result.repo_search_used is False
    assert result.workspace_read_opened is False
    assert result.memory_mutated is False
    assert result.production_certified is False


def test_documentation_exists_with_required_sections():
    text = DOC_PATH.read_text(encoding="utf-8")
    for title in ("Restore Purpose", "Textual Technology Decision", "Entrypoint Migration", "Full-Screen Layout", "Manual UI Acceptance", "Safety Boundary", "Copy-Paste Restore Prompt"):
        assert f"## {title}" in text


def test_no_forbidden_runtime_call_patterns_in_ui_files():
    scanned = [
        ROOT / "src" / "chanta_core" / "schumpeter_tui" / "fullscreen.py",
        ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_work_session.py",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in scanned)
    forbidden_patterns = (
        "sub" + "process",
        "shell" + "=True",
        "os." + "system",
        "ev" + "al(",
        "ex" + "ec(",
        "cur" + "ses",
        "apply" + "_patch",
        "git " + "apply",
        "git " + "worktree",
        "invoke_" + "subagent",
        "run_" + "subagent",
        "create_child_" + "session",
        "spawn_" + "agent",
        "os." + "walk",
        "Path." + "rglob",
        "CORE_MEMORY " + "write",
    )
    for forbidden in forbidden_patterns:
        assert forbidden not in text
