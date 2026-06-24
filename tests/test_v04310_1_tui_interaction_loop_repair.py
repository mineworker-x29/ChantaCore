from pathlib import Path

from chanta_core.personal_runtime import default_personal_conversation_router as router
from chanta_core.personal_runtime import default_personal_schumpeter_lobby as lobby
from chanta_core.schumpeter_tui import app, app_state, runtime_adapter
from chanta_core.schumpeter_tui.plain_shell import run_v04310_plain_interaction_sequence
from chanta_core.schumpeter_tui.transcript import create_v04310_interactive_loop_state, create_v04310_transcript_state
from chanta_core.schumpeter_tui.turn_dispatch import (
    apply_v04310_dispatch_result,
    create_v04310_interaction_golden_result,
    create_v04310_loop_repair_report,
    create_v04310_no_repeat_chrome_policy,
    dispatch_v04310_turn,
)
from chanta_core.schumpeter_tui.turn_renderer import (
    execute_v04310_interaction_golden_case,
    render_v04310_plain_turn,
)


ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "versions" / "v0.43" / "v0.43.10.1_tui_interaction_loop_repair_restore.md"
TUI_ROOT = ROOT / "src" / "chanta_core" / "schumpeter_tui"


def _adapter():
    return runtime_adapter.V04310RuntimeAdapter(provider="mock")


def _sequence_text():
    text, state = run_v04310_plain_interaction_sequence(
        (
            "/status",
            "오늘 작업 계획 정리해줘",
            "/summary 오늘 Schumpeter TUI를 테스트하고 있어.",
            "/what-happened",
            "/exit",
        ),
        width=100,
        adapter=_adapter(),
    )
    return text, state


def test_v04310_1_no_repeat_chrome_policy_declared():
    policy = create_v04310_no_repeat_chrome_policy()
    assert policy.print_static_header_once_in_plain_mode is True
    assert policy.do_not_append_full_frame_after_each_turn is True
    assert policy.snapshot_renderer_used_only_for_snapshot_or_fullscreen_replace is True
    assert policy.turn_renderer_used_for_plain_interactive_turns is True
    assert policy.production_certified is False


def test_v04310_1_interactive_loop_state_tracks_transcript_and_header_once():
    msg = app_state.create_v04310_transcript_message("hello", "assistant")
    state = create_v04310_interactive_loop_state((msg,), header_rendered_once=True, last_input="/status", last_route_kind="slash_command")
    assert state.transcript_messages == (msg,)
    assert state.header_rendered_once is True
    assert state.repeated_static_chrome_count == 0
    assert state.provider_invoked_by_rendering is False
    assert state.production_certified is False
    assert create_v04310_transcript_state((msg,)).messages == (msg,)


def test_v04310_1_turn_dispatch_status_does_not_request_full_static_chrome():
    result = dispatch_v04310_turn("/status", _adapter())
    assert result.message_kind == "status"
    assert result.rerender_full_static_chrome is False
    assert result.append_to_transcript is True


def test_v04310_1_turn_dispatch_general_text_appends_user_and_assistant_messages():
    state = app_state.create_v04310_tui_app_state(_adapter().collect_ui_snapshot())
    result = dispatch_v04310_turn("오늘 작업 계획 정리해줘", _adapter())
    updated = apply_v04310_dispatch_result(state, result)
    assert result.message_kind == "assistant"
    assert updated.transcript[-2].speaker_label == "You>"
    assert updated.transcript[-1].speaker_label == "Schumpeter>"


def test_v04310_1_turn_dispatch_summary_routes_to_artifact_message():
    result = dispatch_v04310_turn("/summary 오늘 Schumpeter TUI를 테스트하고 있어.", _adapter())
    assert result.message_kind == "artifact"
    assert result.rerender_full_static_chrome is False


def test_v04310_1_turn_dispatch_what_happened_routes_to_diagnostic_message():
    result = dispatch_v04310_turn("/what-happened", _adapter())
    assert result.message_kind == "diagnostic"
    assert result.rerender_full_static_chrome is False


def test_v04310_1_turn_dispatch_exit_sets_exit_requested():
    result = dispatch_v04310_turn("/exit", _adapter())
    assert result.app_should_exit is True
    assert result.route_kind == "exit"


def test_v04310_1_plain_fallback_prints_header_once_only():
    text, _state = _sequence_text()
    assert text.count("Schumpeter\nProcess Intelligence-native Work Agent") == 1


def test_v04310_1_plain_fallback_after_status_does_not_reprint_project_session_pi_monitor():
    text, _state = run_v04310_plain_interaction_sequence(("/status",), adapter=_adapter())
    assert text.count("Project\npath:") == 1
    assert text.count("Session\nprofile:") == 1
    assert text.count("PI Monitor") == 1


def test_v04310_1_plain_fallback_after_general_text_does_not_reprint_schumpeter_header():
    text, _state = run_v04310_plain_interaction_sequence(("오늘 작업 계획 정리해줘",), adapter=_adapter())
    assert text.count("Schumpeter\nProcess Intelligence-native Work Agent") == 1
    assert "You> 오늘 작업 계획 정리해줘" in text
    assert "Schumpeter>" in text


def test_v04310_1_transcript_preserves_status_then_general_message_order():
    _text, state = run_v04310_plain_interaction_sequence(("/status", "오늘 작업 계획 정리해줘"), adapter=_adapter())
    kinds = [message.kind for message in state.transcript]
    assert kinds[-4:] == ["user", "status", "user", "assistant"]


def test_v04310_1_chat_view_renders_transcript_not_static_shell_repetition():
    _text, state = run_v04310_plain_interaction_sequence(("/status", "오늘 작업 계획 정리해줘"), adapter=_adapter())
    rendered = app.render_v04310_main_panel(state).rendered_text
    assert rendered.count("PROJECT") == 0
    assert rendered.count("PI MONITOR") == 0
    assert "You>" in rendered
    assert "Status" in rendered


def test_v04310_1_snapshot_mode_still_renders_full_frame_once():
    result = app.render_v04310_snapshot(100, plain=True)
    assert "Project\npath:" in result.rendered_text
    assert "Session\nprofile:" in result.rendered_text
    assert "PI Monitor" in result.rendered_text
    assert result.line_count > 1


def test_v04310_1_snapshot_mode_separate_from_interactive_turn_renderer():
    result = dispatch_v04310_turn("/status", _adapter())
    rendered = render_v04310_plain_turn(result)
    assert "Project\npath:" not in rendered
    assert "PI Monitor" not in rendered
    assert "You> /status" in rendered


def test_v04310_1_interactive_sequence_status_then_text_then_summary_then_what_happened_has_single_static_header():
    text, _state = _sequence_text()
    result = create_v04310_interaction_golden_result(text)
    assert result.schumpeter_header_count == 1
    assert result.notice_count == 1
    assert result.no_repeated_static_chrome is True


def test_v04310_1_interactive_sequence_has_no_duplicate_project_session_pi_monitor_sections():
    text, _state = _sequence_text()
    result = create_v04310_interaction_golden_result(text)
    assert result.project_section_count == 1
    assert result.session_section_count == 1
    assert result.pi_monitor_count == 1


def test_v04310_1_slash_palette_or_help_commands_still_safe():
    palette = app.create_v04310_command_palette_result("/")
    assert "/summary" in palette.rendered_text
    assert palette.command_executed is False
    assert palette.provider_invoked is False


def test_v04310_1_ctrl_c_or_exit_is_graceful():
    policy = app.create_v04310_interactive_loop_policy()
    assert policy.exits_on_ctrl_c is True
    assert dispatch_v04310_turn("/exit", _adapter()).app_should_exit is True


def test_v04310_1_no_provider_completion_from_rendering_status_sidebar_palette_snapshot():
    state = app_state.create_v04310_tui_app_state()
    assert app.render_v04310_sidebar(state).provider_invoked is False
    assert app.render_v04310_status_line(state).provider_invoked is False
    assert app.render_v04310_command_palette(state).provider_invoked is False
    assert app.render_v04310_snapshot(100, plain=True).provider_invoked is False


def test_v04310_1_no_shell_git_repo_workspace_memory_from_rendering():
    result = app.render_v04310_snapshot(100, plain=True)
    assert result.shell_executed is False
    assert result.git_executed is False
    assert result.repo_search_used is False
    assert result.workspace_read_opened is False
    assert result.memory_mutated is False


def test_v04310_1_v0437_identity_regression_still_clean():
    answer = router.render_v0437_default_conversation_answer("넌 누구야")
    assert "ChantaCore default-personal" in answer.rendered_text
    assert "grounding:" not in answer.rendered_text
    assert "source:" not in answer.rendered_text


def test_v04310_1_v0438_start_lobby_regression_still_clean():
    result = lobby.render_v0438_start_lobby(lobby.create_v0438_start_lobby_render_request())
    assert "Schumpeter" in result.rendered_text
    assert "ChantaGrowthKernel" not in result.rendered_text


def test_v04310_1_v0439_snapshot_regression_still_passes():
    from chanta_core.schumpeter_tui.snapshot import render_v0439_snapshot

    result = render_v0439_snapshot(width=100, plain=True)
    assert result.contains_schumpeter_brand is True
    assert result.contains_forbidden_default_strings is False


def test_v04310_1_v04310_tui_mvp_regression_still_passes():
    smoke = app.create_v04310_interactive_smoke_result()
    assert smoke.app_initialized is True
    assert app.render_v04310_snapshot(100, plain=True).contains_schumpeter_brand is True


def test_v04310_1_golden_interaction_sequence_result():
    result = execute_v04310_interaction_golden_case(width=100)
    assert result.no_repeated_static_chrome is True
    assert "You> /status" in result.rendered_text
    assert "Status>" in result.rendered_text
    assert "Artifact>" in result.rendered_text
    assert "Diagnostic>" in result.rendered_text


def test_v04310_1_loop_repair_report_ready_without_production_certification():
    report = create_v04310_loop_repair_report()
    assert report.no_repeat_chrome_policy_ready is True
    assert report.transcript_state_ready is True
    assert report.turn_renderer_ready is True
    assert report.snapshot_interactive_separated is True
    assert report.production_certified is False


def test_v04310_1_no_forbidden_runtime_call_patterns():
    scanned = list(TUI_ROOT.rglob("*.py")) + [
        ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_work_session.py",
    ]
    forbidden = (
        "subprocess",
        "shell=True",
        "os.system",
        "eval(",
        "exec(",
        "import curses",
        "import textual",
        "apply_patch",
        "git apply",
        "git worktree",
        "invoke_subagent",
        "run_subagent",
        "create_child_session",
        "spawn_agent",
        "os.walk",
        "Path.rglob",
        ".rglob(",
        "CORE_MEMORY write",
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in scanned)
    for pattern in forbidden:
        assert pattern not in combined


def test_v04310_1_integrated_hotfix_document_exists_and_has_required_sections():
    text = DOC_PATH.read_text(encoding="utf-8")
    for title in (
        "Restore Purpose",
        "One-Screen Restore Summary",
        "User-Observed Failure",
        "Interactive Loop Repair",
        "Transcript State Repair",
        "No-Repeat-Chrome Policy",
        "Golden Interaction Sequence",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    ):
        assert f"## {title}" in text
