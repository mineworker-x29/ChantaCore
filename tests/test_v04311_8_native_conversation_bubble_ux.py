from pathlib import Path

import pytest

from chanta_core.schumpeter_tui.display_width import assert_v0439_lines_within_width
from chanta_core.schumpeter_tui.fullscreen import create_v04311_textual_app, render_v04311_text_snapshot
from chanta_core.schumpeter_tui.testing.fake_runtime_adapter import V04311FakeRuntimeAdapter


ROOT = Path(__file__).resolve().parents[1]
FULLSCREEN_PATH = ROOT / "src" / "chanta_core" / "schumpeter_tui" / "fullscreen.py"
STYLE_PATH = ROOT / "src" / "chanta_core" / "schumpeter_tui" / "styles" / "schumpeter.tcss"
DOC_PATH = ROOT / "docs" / "versions" / "v0.43" / "v0.43.11.8_native_conversation_bubble_ux_restore.md"


def test_default_textual_header_is_not_composed():
    text = FULLSCREEN_PATH.read_text(encoding="utf-8")
    assert "yield Header" not in text
    assert "from textual.widgets import Footer, Header" not in text
    assert "RichLog" not in text


def test_snapshot_does_not_show_internal_app_header_or_class_name():
    rendered = render_v04311_text_snapshot(140, 42, demo_conversation=True).rendered_text
    assert "SchumpeterTextualApp" not in rendered
    assert "SCHUMPETER | demo conversation" not in rendered
    assert not rendered.startswith("0")


def test_snapshot_uses_semantic_labels_not_ascii_frames():
    rendered = render_v04311_text_snapshot(140, 42, demo_conversation=True).rendered_text
    assert "You [user]" in rendered
    assert "Schumpeter [assistant]" in rendered
    assert "Status [status]" in rendered
    assert "Summary [artifact]" in rendered
    assert "Diagnostic [diagnostic]" in rendered
    assert "Unavailable [error]" in rendered
    assert "+-" not in rendered
    assert "+=" not in rendered
    assert "| " not in rendered


def test_three_demo_snapshots_keep_input_and_no_overflow():
    for width, height in ((140, 42), (110, 32), (80, 24)):
        result = render_v04311_text_snapshot(width, height, demo_conversation=True)
        assert result.contains_input is True
        assert result.production_certified is False
        assert result.contains_forbidden_default_strings is False
        assert assert_v0439_lines_within_width(result.rendered_text, width)


def test_tcss_declares_native_bubble_rows_and_navy_white_palette():
    text = STYLE_PATH.read_text(encoding="utf-8")
    for selector in (
        ".message-row",
        ".message-row.user-row",
        ".message-card.user",
        ".message-card.assistant",
        ".message-card.status",
        ".message-card.artifact",
        ".message-card.diagnostic",
        ".message-card.error",
    ):
        assert selector in text
    assert "#07111f" in text
    assert "#f4f7fb" in text
    assert "align-horizontal: right" in text


@pytest.mark.anyio
async def test_textual_app_mounts_native_message_widgets_not_richlog_text_frames():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        input_bar = pilot.app.query_one("#main-input")
        input_bar.focus()
        input_bar.value = "넌 누구야"
        await pilot.press("enter")
        input_bar.value = "/summary 오늘 메시지 버블 테스트"
        await pilot.press("enter")
        await pilot.pause()
        assert pilot.app.query(".message-row")
        assert pilot.app.query(".message-card.user")
        assert pilot.app.query(".message-card.assistant")
        assert pilot.app.query(".message-card.artifact")
        assert "+-" not in pilot.app.chat_plain
        assert "+=" not in pilot.app.chat_plain
        assert "|" not in pilot.app.chat_plain


@pytest.mark.anyio
async def test_textual_app_has_no_default_header_widget():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        assert not pilot.app.query("Header")
        assert not pilot.app.query("Footer")
        assert pilot.app.query_one("#sidebar") is not None
        assert pilot.app.query_one("#chat-view") is not None


def test_rendering_side_effect_flags_remain_closed():
    result = render_v04311_text_snapshot(140, 42, demo_conversation=True)
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False
    assert result.repo_search_used is False
    assert result.workspace_read_opened is False
    assert result.memory_mutated is False
    assert result.production_certified is False


def test_documentation_exists_with_required_sections():
    text = DOC_PATH.read_text(encoding="utf-8")
    for section in (
        "Restore Purpose",
        "User-Observed Native Bubble Problem",
        "v0.43.11.8 Goal",
        "Native Textual Bubble Contract",
        "Header Removal",
        "Navy-White Visual Refinement",
        "Status Artifact Diagnostic Error Surfaces",
        "Snapshot Tests",
        "Manual Acceptance",
        "Safety Boundary",
        "Withdrawal Conditions",
        "v0.44 Gate Recommendation",
        "Copy-Paste Restore Prompt",
    ):
        assert f"## {section}" in text
