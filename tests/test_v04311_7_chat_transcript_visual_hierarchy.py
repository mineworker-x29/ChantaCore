from pathlib import Path

import pytest

from chanta_core.schumpeter_tui.app_state import create_v04310_tui_app_state, create_v04310_transcript_message
from chanta_core.schumpeter_tui.display_width import assert_v0439_lines_within_width, display_width_v0439
from chanta_core.schumpeter_tui.fullscreen import create_v04311_textual_app, render_v04311_text_snapshot
from chanta_core.schumpeter_tui.renderers.artifact_renderer import render_v0439_artifact
from chanta_core.schumpeter_tui.renderers.diagnostic_renderer import render_v0439_diagnostic
from chanta_core.schumpeter_tui.renderers.error_renderer import render_v0439_error
from chanta_core.schumpeter_tui.renderers.message_renderer import create_v0439_renderer_boundary, render_v0439_message
from chanta_core.schumpeter_tui.renderers.status_renderer import render_v0439_status
from chanta_core.schumpeter_tui.state import create_v0439_display_message
from chanta_core.schumpeter_tui.testing.fake_runtime_adapter import V04311FakeRuntimeAdapter
from chanta_core.schumpeter_tui.widgets.message_view import (
    MESSAGE_CARD_KINDS,
    MESSAGE_CARD_STYLES,
    create_v043117_message_card,
    render_v043117_transcript_cards,
)


ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "versions" / "v0.43" / "v0.43.11.7_chat_transcript_visual_hierarchy_restore.md"
SCAN_PATHS = (
    ROOT / "src" / "chanta_core" / "schumpeter_tui" / "widgets" / "message_view.py",
    ROOT / "src" / "chanta_core" / "schumpeter_tui" / "widgets" / "chat_view.py",
    ROOT / "src" / "chanta_core" / "schumpeter_tui" / "widgets" / "artifact_view.py",
    ROOT / "src" / "chanta_core" / "schumpeter_tui" / "widgets" / "diagnostic_view.py",
    ROOT / "src" / "chanta_core" / "schumpeter_tui" / "widgets" / "status_card.py",
    ROOT / "src" / "chanta_core" / "schumpeter_tui" / "widgets" / "error_card.py",
    ROOT / "src" / "chanta_core" / "schumpeter_tui" / "renderers" / "message_renderer.py",
    ROOT / "src" / "chanta_core" / "schumpeter_tui" / "renderers" / "artifact_renderer.py",
    ROOT / "src" / "chanta_core" / "schumpeter_tui" / "renderers" / "status_renderer.py",
    ROOT / "src" / "chanta_core" / "schumpeter_tui" / "renderers" / "diagnostic_renderer.py",
    ROOT / "src" / "chanta_core" / "schumpeter_tui" / "renderers" / "error_renderer.py",
    ROOT / "src" / "chanta_core" / "schumpeter_tui" / "fullscreen.py",
)


def _msg(text: str, kind: str):
    return create_v0439_display_message(text, kind=kind)


def test_message_card_kinds_declared():
    assert set(MESSAGE_CARD_KINDS) >= {"user", "assistant", "status", "artifact", "diagnostic", "error", "system_notice"}


def test_user_message_card_has_user_class_or_kind():
    card = create_v043117_message_card("넌 누구야", "user")
    assert card.kind == "user"
    assert "user" in card.css_classes


def test_assistant_message_card_has_assistant_class_or_kind():
    card = create_v043117_message_card("저는 Schumpeter입니다.", "assistant")
    assert card.kind == "assistant"
    assert "assistant" in card.css_classes


def test_user_and_assistant_cards_have_distinct_styles():
    user = MESSAGE_CARD_STYLES["user"]
    assistant = MESSAGE_CARD_STYLES["assistant"]
    assert user.css_classes != assistant.css_classes
    assert user.border_color != assistant.border_color
    assert user.horizontal_glyph != assistant.horizontal_glyph


def test_status_card_has_status_kind_and_not_assistant_kind():
    rendered = render_v0439_status(_msg("Provider: configured", "status"))
    assert "Status" in rendered
    assert "Schumpeter" not in rendered.splitlines()[0]


def test_artifact_card_has_artifact_kind_and_not_assistant_kind():
    rendered = render_v0439_artifact(_msg("핵심 요약", "artifact"))
    assert "Summary" in rendered
    assert "Schumpeter" not in rendered.splitlines()[0]


def test_diagnostic_card_has_diagnostic_kind():
    assert "Diagnostic" in render_v0439_diagnostic(_msg("trace: active", "diagnostic"))


def test_error_card_has_error_kind():
    assert "Unavailable" in render_v0439_error(_msg("저장소 직접 읽기는 아직 열려 있지 않습니다.", "error"))


def test_chat_view_renders_user_then_assistant_as_distinct_blocks():
    messages = (
        create_v04310_transcript_message("넌 누구야", "user"),
        create_v04310_transcript_message("저는 Schumpeter입니다.", "assistant"),
    )
    text = render_v043117_transcript_cards(messages, width=72)
    assert "You [user]" in text
    assert "Schumpeter [assistant]" in text
    assert text.index("You") < text.index("Schumpeter")


def test_chat_view_renders_status_as_status_card():
    text = render_v043117_transcript_cards((create_v04310_transcript_message("Provider: configured", "status"),))
    assert "Status" in text
    assert "Provider: configured" in text


def test_chat_view_renders_summary_as_artifact_card():
    text = render_v043117_transcript_cards((create_v04310_transcript_message("핵심 요약\n- 완료", "artifact"),))
    assert "Summary" in text
    assert "type: summary" not in text


def test_message_cards_have_spacing_between_turns():
    text = render_v043117_transcript_cards(
        (
            create_v04310_transcript_message("넌 누구야", "user"),
            create_v04310_transcript_message("저는 Schumpeter입니다.", "assistant"),
        )
    )
    assert "\n\n" in text


def test_korean_text_wraps_within_card_width():
    card = create_v043117_message_card("가나다라마바사아자차카타파하" * 4, "assistant", width=34)
    assert all(display_width_v0439(line) <= 34 for line in card.rendered_text.splitlines())


def test_message_cards_do_not_overflow_chat_width():
    result = render_v04311_text_snapshot(80, 24, demo_conversation=True)
    assert assert_v0439_lines_within_width(result.rendered_text, 80)
    assert result.contains_input is True


def test_message_cards_do_not_include_raw_metadata_by_default():
    card = create_v043117_message_card("핵심 요약\ntype: summary\ngrounding: raw\nsafety: shell=false", "artifact")
    assert "type:" not in card.rendered_text
    assert "grounding:" not in card.rendered_text
    assert "safety: shell=false" not in card.rendered_text


def test_debug_metadata_only_in_debug_surfaces():
    default = create_v043117_message_card("핵심 요약\ngrounding: raw", "artifact")
    debug = create_v043117_message_card("핵심 요약\ngrounding: raw", "artifact", debug_surface=True)
    assert "grounding:" not in default.rendered_text
    assert "grounding:" in debug.rendered_text


def test_static_chrome_not_inserted_into_transcript():
    text = render_v043117_transcript_cards((create_v04310_transcript_message("저는 Schumpeter입니다.", "assistant"),))
    assert "PI MONITOR" not in text
    assert "SHORTCUTS" not in text
    assert "Ask Schumpeter anything" not in text


def test_visual_snapshot_contains_distinct_you_and_schumpeter_blocks():
    text = render_v04311_text_snapshot(140, 42, demo_conversation=True).rendered_text
    assert "You [user]" in text
    assert "Schumpeter [assistant]" in text


def test_status_snapshot_contains_status_card():
    text = render_v04311_text_snapshot(140, 42, demo_conversation=True).rendered_text
    assert "Status [status]" in text
    assert "Provider: configured" in text


def test_artifact_snapshot_contains_artifact_card():
    text = render_v04311_text_snapshot(140, 42, demo_conversation=True).rendered_text
    assert "Summary [artifact]" in text
    assert "핵심 요약" in text


def test_error_snapshot_contains_error_card():
    text = render_v04311_text_snapshot(140, 42, demo_conversation=True).rendered_text
    assert "Unavailable [error]" in text
    assert "/v044 readiness" in text


def test_no_provider_shell_repo_workspace_memory_side_effects_from_rendering():
    result = render_v04311_text_snapshot(140, 42, demo_conversation=True)
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False
    assert result.repo_search_used is False
    assert result.workspace_read_opened is False
    assert result.memory_mutated is False
    assert result.production_certified is False
    boundary = create_v0439_renderer_boundary("message", "assistant")
    assert boundary.provider_invoked is False
    assert boundary.workspace_read_opened is False


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
        "glob(",
        "CORE_MEMORY",
    )
    for path in SCAN_PATHS:
        text = path.read_text(encoding="utf-8")
        for pattern in forbidden:
            assert pattern not in text, f"{pattern} found in {path}"


def test_documentation_exists_with_required_sections():
    text = DOC_PATH.read_text(encoding="utf-8")
    for section in (
        "Restore Purpose",
        "User-Observed Message Differentiation Problem",
        "v0.43.11.7 Goal",
        "Message Card Visual Contract",
        "User Message Card",
        "Assistant Message Card",
        "Status Card",
        "Artifact Card",
        "Diagnostic Card",
        "Error Card",
        "Textual CSS / Theme Changes",
        "Snapshot Tests",
        "Manual Acceptance",
        "Safety Boundary",
        "Withdrawal Conditions",
        "v0.44 Gate Recommendation",
        "Copy-Paste Restore Prompt",
    ):
        assert f"## {section}" in text


@pytest.mark.anyio
async def test_textual_chat_plain_uses_cards_after_turns():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        input_bar = pilot.app.query_one("#main-input")
        input_bar.focus()
        input_bar.value = "넌 누구야"
        await pilot.press("enter")
        input_bar.value = "/summary 오늘 메시지 카드 테스트"
        await pilot.press("enter")
        await pilot.pause()
        assert "You" in pilot.app.chat_plain
        assert "Schumpeter" in pilot.app.chat_plain
        assert "Summary" in pilot.app.chat_plain
        assert "PI MONITOR" not in pilot.app.chat_plain
