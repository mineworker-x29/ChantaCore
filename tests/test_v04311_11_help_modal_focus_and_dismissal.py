from pathlib import Path

import pytest

from chanta_core.schumpeter_tui.fullscreen import create_v04311_textual_app
from chanta_core.schumpeter_tui.help_surface import HELP_MODAL_FOOTER_HINT, check_v04310_help_noisy_output, render_v04310_help
from chanta_core.schumpeter_tui.keybindings import create_v0431111_help_modal_keyboard_policy
from chanta_core.schumpeter_tui.testing.fake_runtime_adapter import V04311FakeRuntimeAdapter


ROOT = Path(__file__).resolve().parents[1]
FULLSCREEN_PATH = ROOT / "src" / "chanta_core" / "schumpeter_tui" / "fullscreen.py"
HELP_PATH = ROOT / "src" / "chanta_core" / "schumpeter_tui" / "help_surface.py"
HELP_MODAL_PATH = ROOT / "src" / "chanta_core" / "schumpeter_tui" / "modals" / "help_modal.py"
STYLE_PATH = ROOT / "src" / "chanta_core" / "schumpeter_tui" / "styles" / "schumpeter.tcss"
DOC_PATH = ROOT / "docs" / "versions" / "v0.43" / "v0.43.11.11_help_modal_focus_dismissal_restore.md"


async def _open_help_with_command(pilot, command: str = "/help"):
    input_bar = pilot.app.query_one("#main-input")
    input_bar.focus()
    input_bar.value = command
    await pilot.press("enter")
    await pilot.pause()
    return input_bar


def test_help_copy_typo_fixed():
    text = render_v04310_help("/help").rendered_text
    assert "일반 문장을 입력하거가" not in text
    assert "일반 문장을 입력하거나, slash command로 업무 흐름을 선택할 수 있습니다." in text


def test_help_modal_shows_close_hint():
    text = render_v04310_help("/help").rendered_text
    assert HELP_MODAL_FOOTER_HINT in text
    assert "Esc 닫기" in text
    assert "q 닫기" in text


@pytest.mark.anyio
async def test_help_modal_opens_from_help_command():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        await _open_help_with_command(pilot, "/help")
        assert not pilot.app.query_one("#help-modal").has_class("hidden")
        assert "Schumpeter Help" in pilot.app.help_plain


@pytest.mark.anyio
async def test_help_modal_opens_from_help_commands_topic():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        await _open_help_with_command(pilot, "/help commands")
        assert not pilot.app.query_one("#help-modal").has_class("hidden")
        assert "Schumpeter Commands" in pilot.app.help_plain


@pytest.mark.anyio
async def test_help_modal_receives_focus():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        await _open_help_with_command(pilot, "/help")
        assert pilot.app.help_modal_has_focus is True
        assert pilot.app.focused is pilot.app.query_one("#help-modal")


@pytest.mark.anyio
async def test_input_disabled_or_unchanged_while_help_modal_open():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        input_bar = await _open_help_with_command(pilot, "/help")
        assert input_bar.disabled is True
        before = input_bar.value
        await pilot.press("s")
        await pilot.press("s")
        await pilot.pause()
        assert input_bar.value == before


@pytest.mark.anyio
async def test_typing_ordinary_text_while_help_open_does_not_update_main_input():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        input_bar = await _open_help_with_command(pilot, "/help")
        await pilot.press("s")
        await pilot.press("s")
        await pilot.pause()
        assert input_bar.value == ""
        assert "ss" not in input_bar.value


@pytest.mark.anyio
async def test_slash_palette_does_not_open_behind_help_modal():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        await _open_help_with_command(pilot, "/help")
        pilot.app.action_toggle_palette()
        await pilot.press("/")
        await pilot.pause()
        assert pilot.app.query_one("#slash-palette").has_class("hidden")
        assert pilot.app.query_one("#palette-region").has_class("hidden")


@pytest.mark.anyio
async def test_esc_closes_help_modal():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        await _open_help_with_command(pilot, "/help")
        await pilot.press("escape")
        await pilot.pause()
        assert pilot.app.query_one("#help-modal").has_class("hidden")


@pytest.mark.anyio
async def test_q_closes_help_modal():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        await _open_help_with_command(pilot, "/help")
        await pilot.press("q")
        await pilot.pause()
        assert pilot.app.query_one("#help-modal").has_class("hidden")


@pytest.mark.anyio
async def test_f1_opens_help_modal_if_supported():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        await pilot.press("f1")
        await pilot.pause()
        assert not pilot.app.query_one("#help-modal").has_class("hidden")


@pytest.mark.anyio
async def test_f1_closes_or_toggles_help_when_open_if_supported():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        await pilot.press("f1")
        await pilot.pause()
        await pilot.press("f1")
        await pilot.pause()
        assert pilot.app.query_one("#help-modal").has_class("hidden")


@pytest.mark.anyio
async def test_close_help_returns_focus_to_input():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        await _open_help_with_command(pilot, "/help")
        await pilot.press("escape")
        await pilot.pause()
        assert pilot.app.focused is pilot.app.query_one("#main-input")
        assert pilot.app.query_one("#main-input").disabled is False


@pytest.mark.anyio
async def test_closing_help_preserves_existing_input():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        input_bar = pilot.app.query_one("#main-input")
        input_bar.value = "draft"
        await pilot.press("f1")
        await pilot.pause()
        await pilot.press("escape")
        await pilot.pause()
        assert input_bar.value == "draft"


@pytest.mark.anyio
async def test_closing_help_does_not_execute_command():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        input_bar = pilot.app.query_one("#main-input")
        input_bar.value = "/summary pending"
        chat_before = pilot.app.chat_plain
        await pilot.press("f1")
        await pilot.pause()
        await pilot.press("q")
        await pilot.pause()
        assert input_bar.value == "/summary pending"
        assert pilot.app.chat_plain == chat_before


def test_help_modal_scroll_keys_supported_or_documented():
    policy = create_v0431111_help_modal_keyboard_policy()
    assert policy.scroll_keys_documented == ("up", "down", "pageup", "pagedown")
    assert "↑/↓/PgUp/PgDn 스크롤" in render_v04310_help("/help").rendered_text


@pytest.mark.anyio
async def test_help_modal_does_not_append_to_transcript_as_plain_message():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        before = pilot.app.chat_plain
        await _open_help_with_command(pilot, "/help examples")
        assert pilot.app.chat_plain == before
        assert "Examples" in pilot.app.help_plain


def test_help_modal_does_not_call_provider():
    result = render_v04310_help("/help")
    assert result.provider_invoked is False


def test_help_modal_does_not_submit_prompt():
    result = render_v04310_help("/help")
    assert result.prompt_submitted is False


def test_help_modal_does_not_run_shell_git():
    result = render_v04310_help("/help")
    assert result.shell_executed is False


def test_help_modal_does_not_read_repo_workspace():
    result = render_v04310_help("/help")
    assert result.repo_search_used is False
    assert result.workspace_read_opened is False


def test_help_modal_does_not_mutate_memory():
    result = render_v04310_help("/help")
    assert result.memory_mutated is False
    assert result.core_memory_written is False


def test_help_modal_has_no_raw_safety_booleans():
    text = render_v04310_help("/help").rendered_text
    for forbidden in ("provider_invoked", "prompt_submitted", "shell=false", "production_certified=false"):
        assert forbidden not in text
    assert check_v04310_help_noisy_output(text).passed is True


def test_help_modal_has_no_chantagrowthkernel_or_legacy_schumpeter():
    text = render_v04310_help("/help").rendered_text
    assert "ChantaGrowthKernel" not in text
    assert "legacy Schumpeter" not in text


def test_no_forbidden_runtime_call_patterns():
    forbidden = (
        "requests",
        "httpx",
        "urllib",
        "socket",
        "subprocess",
        "shell=True",
        "os.system",
        "eval(",
        "exec(",
        "git status",
        "os.walk",
        "Path.rglob",
        ".rglob(",
        "CORE_MEMORY",
        "production_certified=True",
    )
    for path in (FULLSCREEN_PATH, HELP_PATH, HELP_MODAL_PATH, STYLE_PATH):
        text = path.read_text(encoding="utf-8")
        for pattern in forbidden:
            assert pattern not in text, f"{pattern} found in {path}"


def test_documentation_exists_with_required_sections():
    text = DOC_PATH.read_text(encoding="utf-8")
    for section in (
        "Restore Purpose",
        "User-Observed Help Modal Issue",
        "v0.43.11.11 Goal",
        "Help Modal Focus Policy",
        "Close / Navigation Hint",
        "Input Isolation While Modal Open",
        "Slash Palette Interaction",
        "Copy Corrections",
        "Tests",
        "Manual Acceptance",
        "Safety Boundary",
        "Withdrawal Conditions",
        "v0.44 Gate Recommendation",
        "Copy-Paste Restore Prompt",
    ):
        assert f"## {section}" in text
