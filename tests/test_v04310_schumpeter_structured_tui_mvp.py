from pathlib import Path

from chanta_core.personal_runtime import default_personal_command_palette as palette
from chanta_core.personal_runtime import default_personal_conversation_router as router
from chanta_core.personal_runtime import default_personal_schumpeter_lobby as lobby
from chanta_core.schumpeter_tui import app, app_state, architecture, runtime_adapter, safety
from chanta_core.schumpeter_tui.plain_shell import run_v04310_plain_tui


ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "versions" / "v0.43" / "v0.43.10_schumpeter_structured_tui_mvp_restore.md"
TUI_ROOT = ROOT / "src" / "chanta_core" / "schumpeter_tui"
SCAN_PATHS = tuple(path for path in TUI_ROOT.iterdir() if path.suffix == ".py") + (
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_work_session.py",
)


def test_v04310_tui_entrypoint_policy_prefers_chanta_cli_tui_and_does_not_replace_start_by_default():
    policy = app.create_v04310_tui_entrypoint_policy()
    assert policy.primary_command == "chanta-cli tui"
    assert policy.start_alias_allowed is True
    assert policy.replaces_existing_start_by_default is False
    assert policy.snapshot_command_required is True
    assert policy.interactive_preview_enabled is True
    assert policy.production_certified is False


def test_v04310_prompt_toolkit_policy_lazy_imports_and_has_plain_fallback():
    policy = app.create_v04310_prompt_toolkit_policy()
    assert policy.import_is_lazy is True
    assert policy.fallback_when_missing is True
    assert policy.prompt_toolkit_required_for_full_tui is False
    assert policy.production_certified is False


def test_v04310_runtime_adapter_policy_blocks_render_side_effects():
    policy = runtime_adapter.create_v04310_runtime_adapter_policy()
    assert policy.render_collect_snapshot_side_effect_free is True
    assert policy.component_direct_runtime_access_allowed is False
    assert policy.provider_completion_from_rendering_allowed is False
    assert policy.prompt_submission_from_rendering_allowed is False
    assert policy.shell_execution_allowed is False
    assert policy.git_execution_allowed is False
    assert policy.repo_search_allowed is False
    assert policy.workspace_read_allowed is False
    assert policy.memory_mutation_allowed is False
    assert policy.core_memory_write_allowed is False


def test_v04310_runtime_snapshot_is_schumpeter_and_high_risk_flags_false():
    snap = runtime_adapter.create_v04310_runtime_snapshot()
    assert snap.product_name == "Schumpeter"
    assert snap.provider_invoked is False
    assert snap.prompt_submitted is False
    assert snap.shell_executed is False
    assert snap.git_executed is False
    assert snap.repo_search_used is False
    assert snap.workspace_read_opened is False
    assert snap.memory_mutated is False
    assert snap.core_memory_written is False
    assert snap.production_certified is False


def test_v04310_tui_app_state_is_display_only_and_hides_secrets_debug_metadata():
    state = app_state.create_v04310_tui_app_state()
    assert state.contains_secret_values is False
    assert state.contains_raw_debug_metadata is False
    assert state.production_certified is False
    assert state.runtime_snapshot.product_name == "Schumpeter"


def test_v04310_transcript_message_kinds_declared():
    values = {item.value for item in app_state.V04310TranscriptMessageKind}
    assert {"user", "assistant", "artifact", "diagnostic", "status", "error", "system_notice", "unknown"}.issubset(values)


def test_v04310_keybinding_policy_slash_palette_enter_submit_no_execute_before_enter():
    policy = app.create_v04310_key_binding_policy()
    assert policy.slash_opens_palette is True
    assert policy.enter_submits is True
    assert policy.ctrl_c_exits_gracefully is True
    assert policy.command_executes_before_enter is False


def test_v04310_command_completion_uses_shared_registry_and_inserts_text_only():
    policy = app.create_v04310_command_completion_policy()
    assert policy.uses_shared_command_registry is True
    assert policy.inserts_text_only is True
    assert policy.executes_command_during_completion is False
    assert policy.provider_invoked is False
    assert "/summary" in app.complete_v04310_slash_command("/s")


def test_v04310_sidebar_renders_product_project_session_pi_monitor():
    rendered = app.render_v04310_sidebar(app_state.create_v04310_tui_app_state()).rendered_text
    for expected in ("SCHUMPETER", "PROJECT", "SESSION", "PI MONITOR"):
        assert expected in rendered


def test_v04310_main_panel_renders_welcome_user_assistant_artifact_status_error():
    messages = (
        app_state.create_v04310_transcript_message("u", "user"),
        app_state.create_v04310_transcript_message("a", "assistant"),
        app_state.create_v04310_transcript_message("art", "artifact"),
        app_state.create_v04310_transcript_message("diag", "diagnostic"),
        app_state.create_v04310_transcript_message("stat", "status"),
        app_state.create_v04310_transcript_message("err", "error"),
    )
    state = app_state.create_v04310_tui_app_state(transcript=messages)
    rendered = app.render_v04310_main_panel(state).rendered_text
    for expected in ("Welcome to Schumpeter", "You>", "Schumpeter>", "Artifact", "Diagnostic", "Status", "Unavailable"):
        assert expected in rendered


def test_v04310_input_box_renders_schumpeter_placeholder():
    rendered = app.render_v04310_input_box(app_state.create_v04310_tui_app_state()).rendered_text
    assert "Ask Schumpeter anything" in rendered


def test_v04310_status_line_renders_pi_provider_trace_evidence_safety():
    rendered = app.render_v04310_status_line(app_state.create_v04310_tui_app_state()).rendered_text
    for expected in ("PI", "Provider", "Trace", "Evidence", "Safety"):
        assert expected in rendered


def test_v04310_command_palette_renders_grouped_slash_commands_without_execution():
    result = app.create_v04310_command_palette_result("/")
    for command in ("/summary", "/todo", "/memo", "/decision", "/handoff", "/status", "/exit"):
        assert command in result.rendered_text
    assert result.command_executed is False
    assert result.provider_invoked is False


def test_v04310_message_renderer_hides_raw_metadata():
    msg = app_state.create_v04310_transcript_message("hello", "assistant")
    result = app.render_v04310_message(msg)
    assert result.raw_metadata_visible is False
    assert result.executes_runtime_action is False


def test_v04310_artifact_renderer_hides_raw_metadata_by_default():
    msg = app_state.create_v04310_transcript_message("artifact", "artifact")
    assert app.render_v04310_artifact(msg).raw_metadata_visible is False


def test_v04310_diagnostic_renderer_is_explicit_surface():
    msg = app_state.create_v04310_transcript_message("diagnostic", "diagnostic")
    result = app.render_v04310_diagnostic(msg)
    assert result.renderer_kind == "diagnostic"


def test_v04310_error_renderer_handles_unavailable_workspace_read_cleanly():
    msg = app_state.create_v04310_transcript_message("workspace read is not open in this TUI preview", "error")
    rendered = app.render_v04310_error(msg).rendered_text
    assert "Unavailable" in rendered
    assert "Traceback" not in rendered


def test_v04310_snapshot_120_contains_sidebar_main_input_status_brand():
    result = app.render_v04310_snapshot(120)
    assert result.contains_sidebar is True
    assert result.contains_main_panel is True
    assert result.contains_input_box is True
    assert result.contains_status_bar is True
    assert result.contains_schumpeter_brand is True


def test_v04310_snapshot_120_lines_within_width():
    assert app.render_v04310_snapshot(120).all_lines_within_width is True


def test_v04310_snapshot_80_uses_compact_safe_layout():
    result = app.render_v04310_snapshot(80)
    assert result.mode == "compact"
    assert result.all_lines_within_width is True
    assert "PI Monitor" in result.rendered_text


def test_v04310_snapshot_plain_has_no_unicode_box_dependency():
    result = app.render_v04310_snapshot(100, plain=True)
    for glyph in ("┌", "┐", "└", "┘", "│", "─", "╭", "╯"):
        assert glyph not in result.rendered_text
    assert result.mode == "plain"


def test_v04310_snapshot_palette_contains_slash_commands_and_no_execution():
    result = app.render_v04310_snapshot(120, include_command_palette=True)
    for command in ("/summary", "/todo", "/memo", "/decision", "/handoff", "/status", "/exit"):
        assert command in result.rendered_text
    assert result.contains_command_palette is True
    assert result.provider_invoked is False


def test_v04310_snapshot_no_forbidden_default_strings():
    result = app.render_v04310_snapshot(120)
    assert result.contains_forbidden_default_strings is False


def test_v04310_snapshot_no_side_effect_flags_false():
    result = app.render_v04310_snapshot(120)
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False
    assert result.git_executed is False
    assert result.repo_search_used is False
    assert result.workspace_read_opened is False
    assert result.memory_mutated is False
    assert result.core_memory_written is False
    assert result.production_certified is False


def test_v04310_plain_shell_fallback_available_when_prompt_toolkit_missing():
    policy = app.create_v04310_plain_fallback_policy()
    assert policy.line_input_loop_available is True
    assert policy.slash_help_fallback_available is True
    assert callable(run_v04310_plain_tui)


def test_v04310_interactive_smoke_initializes_app_without_provider_shell_repo_workspace_memory():
    smoke = app.create_v04310_interactive_smoke_result()
    assert smoke.app_initialized is True
    assert smoke.structured_snapshot_rendered is True
    assert smoke.provider_invoked_by_rendering is False
    assert smoke.shell_executed is False
    assert smoke.repo_search_used is False
    assert smoke.workspace_read_opened is False
    assert smoke.memory_mutated_by_rendering is False


def test_v04310_submit_user_input_routes_through_runtime_adapter_not_components():
    adapter = runtime_adapter.V04310RuntimeAdapter(provider="mock")
    result = adapter.submit_user_input("넌 누구야")
    assert result.route_kind in {"conversation", "identity_question"}
    assert result.shell_executed is False
    assert result.repo_search_used is False
    assert result.workspace_read_opened is False


def test_v04310_submit_user_input_appends_user_and_assistant_messages():
    state = app.run_v04310_tui_preview(("넌 누구야",), runtime_adapter.V04310RuntimeAdapter(provider="mock"))
    rendered = app.render_v04310_main_panel(state).rendered_text
    assert "You>" in rendered
    assert "Schumpeter>" in rendered


def test_v04310_slash_exit_sets_exit_requested():
    state = app.run_v04310_tui_preview(("/exit",), runtime_adapter.V04310RuntimeAdapter(provider="mock"))
    assert state.exit_requested is True


def test_v04310_ctrl_c_or_exit_policy_is_graceful():
    policy = app.create_v04310_interactive_loop_policy()
    assert policy.exits_on_ctrl_c is True
    assert policy.exits_on_slash_exit is True
    assert policy.exits_on_eof is True


def test_v04310_about_status_summary_commands_render_in_main_panel():
    adapter = runtime_adapter.V04310RuntimeAdapter(provider="mock")
    for command in ("/about", "/status", "/summary test"):
        result = adapter.execute_slash_command(command)
        assert result.rendered_text
        assert result.shell_executed is False


def test_v04310_v0437_identity_regression_still_clean():
    answer = router.render_v0437_identity_answer()
    assert "safety:" not in answer.rendered_text
    assert "type:" not in answer.rendered_text


def test_v04310_v0438_start_lobby_regression_still_clean():
    result = lobby.render_v0438_start_lobby(width=120)
    assert result.contains_schumpeter_brand is True
    assert result.contains_raw_debug_metadata is False
    assert result.contains_raw_safety_footer is False


def test_v04310_command_palette_regression_still_safe():
    result = palette.render_v0438_command_palette()
    assert result.provider_invoked is False
    assert result.shell_executed is False
    assert result.workspace_read_opened is False


def test_v04310_tui_safety_report_opens_tui_mvp_but_keeps_dangerous_fields_false():
    report = safety.create_v04310_tui_safety_report()
    assert report.structured_tui_mvp_opened is True
    assert report.workspace_read_opened is False
    assert report.repo_search_opened is False
    assert report.shell_execution_opened is False
    assert report.git_execution_opened is False
    assert report.provider_tool_calling_opened is False
    assert report.subagent_opened is False


def test_v04310_readiness_report_sets_tui_mvp_flags_true():
    report = safety.create_v04310_readiness_report()
    assert report.tui_entrypoint_ready is True
    assert report.prompt_toolkit_or_plain_fallback_ready is True
    assert report.interactive_loop_ready is True
    assert report.runtime_adapter_ready is True
    assert report.sidebar_ready is True
    assert report.snapshot_mode_ready is True


def test_v04310_readiness_report_keeps_workspace_repo_shell_git_edit_tools_subagent_memory_core_and_production_false():
    report = safety.create_v04310_readiness_report()
    assert report.ready_for_workspace_read is False
    assert report.ready_for_repo_search is False
    assert report.ready_for_git_status_execution is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_file_edit is False
    assert report.ready_for_patch_apply is False
    assert report.ready_for_provider_tool_calling is False
    assert report.ready_for_function_calling is False
    assert report.ready_for_subagent_invocation is False
    assert report.ready_for_memory_mutation_by_rendering is False
    assert report.ready_for_core_memory_write is False
    assert report.production_certified is False


def test_v04310_v04311_handoff_targets_user_feedback_visual_polish():
    handoff = architecture.create_v04311_user_feedback_polish_handoff()
    assert handoff.target_version == "v0.43.11 User Feedback Visual Polish"
    assert "workspace read" in handoff.still_closed


def test_v04310_v044_handoff_remains_controlled_workspace_read_design_after_ui_acceptance():
    handoff = architecture.create_v0440_controlled_workspace_read_design_handoff()
    assert "Workspace Read" in handoff.target_version
    assert "workspace read implementation" in handoff.closed_until_gate


def test_v04310_integrated_document_exists_and_has_required_sections():
    text = DOC_PATH.read_text(encoding="utf-8")
    for section in architecture.REQUIRED_V04310_RESTORE_SECTIONS:
        assert f"## {section}" in text


def test_v04310_integrated_document_contains_manual_ui_acceptance_and_restore_prompt():
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "Manual UI Acceptance Guide" in text
    assert "Copy-Paste Restore Prompt for Future GPT/Codex Session" in text


def test_v04310_no_separate_v04310_tui_user_guide_docs_created():
    docs = sorted(path.name for path in (ROOT / "docs" / "versions" / "v0.43").iterdir() if "v0.43.10_" in path.name)
    assert docs == [DOC_PATH.name]


def test_v04310_no_forbidden_runtime_call_patterns():
    forbidden = ("subprocess", "shell=True", "os.system", "eval(", "exec(", "import curses", "import textual", "apply_patch", "git apply", "git worktree", "git status", "invoke_subagent", "run_subagent", "create_child_session", "spawn_agent", "os.walk", "Path.rglob", ".rglob(")
    for path in SCAN_PATHS:
        text = path.read_text(encoding="utf-8")
        for pattern in forbidden:
            assert pattern not in text, f"{pattern} found in {path}"


def test_v04310_no_provider_completion_shell_git_repo_workspace_read_in_rendering_or_snapshot():
    result = app.render_v04310_snapshot(120)
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False
    assert result.git_executed is False
    assert result.repo_search_used is False
    assert result.workspace_read_opened is False


def test_v04310_interactive_loop_does_not_append_full_snapshot_after_each_turn():
    from chanta_core.schumpeter_tui.turn_renderer import run_v04310_plain_interaction_sequence

    text, _state = run_v04310_plain_interaction_sequence(("/status", "오늘 작업 계획 정리해줘"), adapter=runtime_adapter.V04310RuntimeAdapter(provider="mock"))
    assert text.count("Schumpeter\nProcess Intelligence-native Work Agent") == 1
    assert text.count("Project\npath:") == 1
    assert text.count("Session\nprofile:") == 1
    assert text.count("PI Monitor") == 1


def test_v04310_plain_tui_sequence_has_one_header_and_multiple_messages():
    from chanta_core.schumpeter_tui.turn_renderer import run_v04310_plain_interaction_sequence

    text, _state = run_v04310_plain_interaction_sequence(("/status", "/summary test", "/what-happened"), adapter=runtime_adapter.V04310RuntimeAdapter(provider="mock"))
    assert text.count("Schumpeter\nProcess Intelligence-native Work Agent") == 1
    assert "Status>" in text
    assert "Artifact>" in text
    assert "Diagnostic>" in text


def test_v04310_chat_view_not_reinitialized_after_every_input():
    from chanta_core.schumpeter_tui.turn_renderer import run_v04310_plain_interaction_sequence

    _text, state = run_v04310_plain_interaction_sequence(("/status", "오늘 작업 계획 정리해줘"), adapter=runtime_adapter.V04310RuntimeAdapter(provider="mock"))
    rendered = app.render_v04310_main_panel(state).rendered_text
    assert rendered.count("Welcome to Schumpeter") == 1
    assert rendered.count("PROJECT") == 0
    assert rendered.count("PI MONITOR") == 0
