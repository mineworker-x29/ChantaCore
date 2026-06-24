from chanta_core.personal_runtime import default_personal_conversation_router as router
from chanta_core.personal_runtime import default_personal_schumpeter_lobby as lobby


FORBIDDEN_NOISY_STRINGS = (
    "ChantaGrowthKernel",
    "legacy Schumpeter",
    "ChantaCore legacy core",
    "Closed in this track",
    "safety:",
    "shell=false",
    "production_certified=false",
    "grounding:",
    "source:",
    "base_url=",
    "api_key",
    "secret",
)


def _box_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip().startswith(("╭", "│", "╰"))]


def test_v0438_1_display_width_counts_korean_as_wide():
    assert lobby.display_width("abc") == 3
    assert lobby.display_width("오늘") == 4
    assert lobby.display_width('Ask "오늘"') == 10


def test_v0438_1_pad_to_display_width_handles_korean():
    padded = lobby.pad_to_display_width("오늘", 8)
    assert lobby.display_width(padded) == 8
    assert padded.startswith("오늘")


def test_v0438_1_truncate_to_display_width_handles_korean_without_breaking():
    truncated = lobby.truncate_to_display_width("오늘 작업을 요약해줘", 7)
    assert lobby.display_width(truncated) <= 7
    assert "\ufffd" not in truncated


def test_v0438_1_box_lines_have_equal_display_width():
    lines = [
        lobby.render_box_line("Ask anything...", 40),
        lobby.render_box_line('"오늘 작업을 요약해줘"', 40),
        lobby.render_box_line("default-personal   configured   Work Session", 40),
    ]
    assert {lobby.display_width(line) for line in lines} == {40}
    assert all(line.endswith("│") for line in lines)


def test_v0438_1_default_lobby_box_right_border_aligns_with_korean_placeholder():
    result = lobby.render_v0438_start_lobby(width=120)
    lines = _box_lines(result.rendered_text)
    assert len(lines) >= 6
    assert {lobby.display_width(line) for line in lines} == {lobby.display_width(lines[0])}
    assert all(line.endswith(("╮", "│", "╯")) for line in lines)


def test_v0438_1_provider_mode_row_does_not_overflow_card_width():
    result = lobby.render_v0438_start_lobby(
        width=120,
        provider_label="configured provider with a very long display label",
        mode_label="Business Work Session",
    )
    lines = _box_lines(result.rendered_text)
    row_lines = [line for line in lines if "default-personal" in line]
    assert row_lines
    assert all(lobby.display_width(line) == lobby.display_width(lines[0]) for line in row_lines)
    assert "configured provider" not in result.rendered_text


def test_v0438_1_compact_fallback_used_for_narrow_terminal():
    result = lobby.render_v0438_start_lobby(width=70)
    assert result.render_mode == "compact"
    assert "Profile:" in result.rendered_text
    assert "PI=" in result.rendered_text
    assert "╭" not in result.rendered_text


def test_v0438_1_plain_mode_has_no_box_drawing_dependency():
    result = lobby.render_v0438_start_lobby(width=120, force_plain=True)
    assert result.render_mode == "plain"
    assert "╭" not in result.rendered_text
    assert "│" not in result.rendered_text
    assert "╰" not in result.rendered_text


def test_v0438_1_default_lobby_contains_schumpeter_brand():
    text = lobby.render_v0438_start_lobby(width=120).rendered_text
    assert "Schumpeter" in text
    assert "Process Intelligence-native Work Agent" in text
    assert "Ask anything" in text
    assert "오늘 작업을 요약해줘" in text


def test_v0438_1_default_lobby_hides_forbidden_noisy_strings():
    text = lobby.render_v0438_start_lobby(width=120).rendered_text
    for forbidden in FORBIDDEN_NOISY_STRINGS:
        assert forbidden not in text


def test_v0438_1_lobby_does_not_call_provider_prompt_shell_repo_workspace_or_memory():
    result = lobby.render_v0438_start_lobby(width=120)
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False
    assert result.repo_search_used is False
    assert result.workspace_read_opened is False
    assert result.memory_mutated is False
    assert result.core_memory_written is False
    assert result.production_certified is False


def test_v0438_1_regression_v0437_identity_output_still_clean():
    answer = router.render_v0437_identity_answer()
    text = answer.rendered_text
    assert answer.intent_kind == "identity_question"
    assert "업무 요약" not in text
    assert "type:" not in text
    assert "grounding:" not in text
    assert "source:" not in text
    assert "safety:" not in text
    assert answer.workspace_read_opened is False
    assert answer.production_certified is False
