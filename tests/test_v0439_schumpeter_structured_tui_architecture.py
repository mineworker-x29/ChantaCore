from pathlib import Path

from chanta_core.schumpeter_tui import architecture as arch
from chanta_core.schumpeter_tui import command_registry, display_width, layout, runtime_adapter, safety, snapshot, state
from chanta_core.schumpeter_tui.components import chat_view, code_block, command_palette, header, input_box, sidebar, status_bar
from chanta_core.schumpeter_tui.renderers import (
    artifact_renderer,
    diagnostic_renderer,
    error_renderer,
    message_renderer,
    status_renderer,
)


ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "versions" / "v0.43" / "v0.43.9_schumpeter_structured_tui_architecture_restore.md"
TUI_ROOT = ROOT / "src" / "chanta_core" / "schumpeter_tui"
SCAN_PATHS = (
    TUI_ROOT / "architecture.py",
    TUI_ROOT / "app_contract.py",
    TUI_ROOT / "state.py",
    TUI_ROOT / "runtime_adapter.py",
    TUI_ROOT / "layout.py",
    TUI_ROOT / "theme.py",
    TUI_ROOT / "display_width.py",
    TUI_ROOT / "command_registry.py",
    TUI_ROOT / "snapshot.py",
    TUI_ROOT / "safety.py",
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_work_session.py",
)


def test_v0439_tui_engine_kinds_declared():
    values = {item.value for item in arch.V0439TUIEngineKind}
    assert {"pure_snapshot_renderer", "prompt_toolkit_shell", "textual_full_tui", "rich_static_layout", "plain_terminal", "unknown"}.issubset(values)


def test_v0439_library_decision_does_not_add_textual_now_unless_optional():
    decision = arch.create_v0439_tui_library_decision()
    assert decision.recommended_v0439_engine == "pure_snapshot_renderer"
    assert decision.textual_dependency_added_now is False
    assert decision.prompt_toolkit_required_now is False
    assert decision.rich_required_now is False
    assert decision.production_certified is False


def test_v0439_architecture_policy_separates_runtime_adapter_ui_state_components_renderers():
    policy = arch.create_v0439_tui_architecture_policy()
    assert policy.runtime_core_separated_from_tui is True
    assert policy.runtime_adapter_required is True
    assert policy.ui_state_required is True
    assert policy.components_are_pure_renderers is True
    assert policy.renderers_separated_by_surface is True
    assert policy.snapshot_mode_required is True
    assert policy.no_side_effect_rendering_required is True


def test_v0439_runtime_adapter_policy_blocks_provider_prompt_shell_git_repo_workspace_memory():
    policy = runtime_adapter.create_v0439_runtime_adapter_policy()
    assert policy.provider_completion_allowed is False
    assert policy.prompt_submission_allowed is False
    assert policy.shell_execution_allowed is False
    assert policy.git_execution_allowed is False
    assert policy.repo_search_allowed is False
    assert policy.workspace_read_allowed is False
    assert policy.memory_mutation_allowed is False
    assert policy.core_memory_write_allowed is False
    assert policy.unavailable_sources_return_unknown is True


def test_v0439_runtime_snapshot_contains_schumpeter_and_high_risk_flags_false():
    snap = runtime_adapter.create_v0439_runtime_snapshot()
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


def test_v0439_ui_state_is_display_only_and_hides_secrets_debug_metadata():
    ui = state.create_v0439_ui_state()
    assert ui.product_name == "Schumpeter"
    assert ui.contains_secret_values is False
    assert ui.contains_raw_debug_metadata is False
    assert ui.production_certified is False


def test_v0439_display_message_kinds_declared():
    values = {item.value for item in state.V0439DisplayMessageKind}
    assert {"user", "assistant", "artifact", "diagnostic", "status", "error", "system_notice", "unknown"}.issubset(values)


def test_v0439_pane_kinds_declared():
    values = {item.value for item in layout.V0439PaneKind}
    assert {"sidebar", "main_chat", "input_box", "status_bar", "command_palette", "header", "unknown"}.issubset(values)


def test_v0439_layout_modes_declared():
    values = {item.value for item in layout.V0439LayoutMode}
    assert {"two_column", "stacked_compact", "plain", "snapshot", "unknown"}.issubset(values)


def test_v0439_layout_policy_uses_display_width_not_naive_len():
    policy = layout.create_v0439_layout_policy()
    assert policy.use_display_width is True
    assert policy.use_naive_len_for_layout is False
    assert policy.fallback_to_stacked_when_narrow is True


def test_v0439_component_specs_exist_for_sidebar_header_chat_input_status_palette_codeblock():
    kinds = {"sidebar", "header", "chat_view", "input_box", "status_bar", "command_palette", "code_block"}
    for kind in kinds:
        spec = sidebar.create_v0439_component_spec(kind)
        assert spec.renders_from_ui_state_only is True
        assert spec.executes_runtime_action is False


def test_v0439_renderer_boundaries_exist_for_message_artifact_diagnostic_status_error():
    kinds = {"message", "artifact", "diagnostic", "status", "error"}
    for kind in kinds:
        boundary = message_renderer.create_v0439_renderer_boundary(kind)
        assert boundary.renderer_kind == kind
        assert boundary.shows_raw_metadata_by_default is False


def test_v0439_renderer_boundaries_do_not_execute_runtime_actions():
    boundary = message_renderer.create_v0439_renderer_boundary("message")
    assert boundary.executes_runtime_action is False
    assert boundary.provider_invoked is False
    assert boundary.shell_executed is False
    assert boundary.repo_search_used is False
    assert boundary.workspace_read_opened is False


def test_v0439_display_width_handles_korean_and_ansi():
    assert display_width.display_width_v0439("한글") == 4
    assert display_width.display_width_v0439("\x1b[31m한글\x1b[0m") == 4
    assert display_width.pad_to_display_width_v0439("한글", 6) == "한글  "
    assert display_width.truncate_to_display_width_v0439("한글abc", 5) == "한글a"


def test_v0439_snapshot_120_contains_sidebar_main_chat_input_status_and_brand():
    result = snapshot.render_v0439_snapshot(width=120)
    assert result.contains_schumpeter_brand is True
    assert result.contains_sidebar is True
    assert result.contains_main_chat is True
    assert result.contains_input_box is True
    assert result.contains_status_bar is True
    assert "PI MONITOR" in result.rendered_text


def test_v0439_snapshot_120_lines_within_width():
    result = snapshot.render_v0439_snapshot(width=120)
    assert result.all_lines_within_width is True
    assert display_width.assert_v0439_lines_within_width(result.rendered_text, 120) is True


def test_v0439_snapshot_120_hides_forbidden_default_strings():
    result = snapshot.render_v0439_snapshot(width=120)
    assert result.contains_forbidden_default_strings is False
    assert snapshot.assert_v0439_no_forbidden_default_strings(result.rendered_text) is True


def test_v0439_snapshot_100_safe_layout():
    result = snapshot.render_v0439_snapshot(width=100)
    assert result.all_lines_within_width is True
    assert result.contains_schumpeter_brand is True
    assert result.contains_input_box is True


def test_v0439_snapshot_80_uses_compact_or_safe_layout():
    result = snapshot.render_v0439_snapshot(width=80)
    assert result.mode == "compact"
    assert result.all_lines_within_width is True
    assert "PI Monitor" in result.rendered_text


def test_v0439_plain_snapshot_has_no_unicode_box_dependency():
    result = snapshot.render_v0439_snapshot(width=100, plain=True)
    assert result.mode == "plain"
    for glyph in ("┌", "┐", "└", "┘", "╭", "╰", "─", "│"):
        assert glyph not in result.rendered_text
    for expected in ("Schumpeter", "Project", "Session", "PI Monitor", "Chat", "Input", "Status"):
        assert expected in result.rendered_text


def test_v0439_command_palette_snapshot_uses_registry_and_does_not_execute():
    report = command_registry.create_v0439_command_registry_reuse_report("/")
    result = snapshot.render_v0439_snapshot(width=120, include_command_palette=True)
    assert report.source_registry == "v0.43.8.2 slash command registry"
    assert report.command_executed is False
    for command in ("/summary", "/todo", "/memo", "/decision", "/handoff", "/status", "/exit"):
        assert command in result.rendered_text
    assert result.provider_invoked is False


def test_v0439_snapshot_no_side_effect_flags_false():
    result = snapshot.render_v0439_snapshot(width=120)
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False
    assert result.git_executed is False
    assert result.repo_search_used is False
    assert result.workspace_read_opened is False
    assert result.memory_mutated is False
    assert result.core_memory_written is False
    assert result.production_certified is False


def test_v0439_sidebar_shows_product_project_session_pi_monitor_not_raw_metadata():
    rendered = "\n".join(sidebar.render_v0439_sidebar(state.create_v0439_ui_state()).rendered_lines)
    assert "SCHUMPETER" in rendered
    assert "PROJECT" in rendered
    assert "SESSION" in rendered
    assert "PI MONITOR" in rendered
    assert "safety:" not in rendered


def test_v0439_status_bar_shows_pi_provider_trace_evidence_safety_compactly():
    rendered = status_bar.render_v0439_status_bar(state.create_v0439_ui_state()).rendered_lines[0]
    for expected in ("PI", "Provider", "Trace", "Evidence", "Safety"):
        assert expected in rendered
    assert "safety:" not in rendered


def test_v0439_chat_view_distinguishes_user_assistant_artifact_diagnostic_status_error():
    messages = (
        state.create_v0439_display_message("u", "user"),
        state.create_v0439_display_message("a", "assistant"),
        state.create_v0439_display_message("art", "artifact"),
        state.create_v0439_display_message("diag", "diagnostic"),
        state.create_v0439_display_message("stat", "status"),
        state.create_v0439_display_message("err", "error"),
    )
    ui = state.create_v0439_ui_state(messages=messages)
    rendered = "\n".join(chat_view.render_v0439_chat_view(ui).rendered_lines)
    for expected in ("You>", "Schumpeter>", "Artifact", "Diagnostic", "Status", "Unavailable"):
        assert expected in rendered


def test_v0439_input_box_shows_ask_schumpeter_placeholder():
    rendered = "\n".join(input_box.render_v0439_input_box(state.create_v0439_ui_state()).rendered_lines)
    assert "Ask Schumpeter anything" in rendered


def test_v0439_runtime_adapter_returns_unknown_for_unavailable_bounded_sources():
    snap = runtime_adapter.collect_v0439_runtime_snapshot(project_label="unknown", session_label="unknown")
    assert snap.project_label == "unknown"
    assert snap.session_label == "unknown"


def test_v0439_tui_safety_report_opens_contract_but_not_full_interactive_tui_or_capabilities():
    report = safety.create_v0439_tui_safety_report()
    assert report.structured_tui_contract_opened is True
    assert report.full_interactive_tui_opened is False
    assert report.workspace_read_opened is False
    assert report.repo_search_opened is False
    assert report.shell_execution_opened is False
    assert report.memory_mutation_opened is False


def test_v0439_readiness_report_sets_contract_snapshot_flags_true():
    report = safety.create_v0439_tui_readiness_report()
    assert report.tui_architecture_policy_ready is True
    assert report.runtime_adapter_contract_ready is True
    assert report.ui_state_model_ready is True
    assert report.component_boundary_ready is True
    assert report.renderer_boundary_ready is True
    assert report.snapshot_mode_ready is True
    assert report.golden_snapshot_tests_ready is True


def test_v0439_readiness_report_keeps_full_tui_workspace_repo_shell_git_edit_tools_subagent_memory_core_and_production_false():
    report = safety.create_v0439_tui_readiness_report()
    assert report.ready_for_full_interactive_tui_in_v0439 is False
    assert report.ready_for_workspace_read is False
    assert report.ready_for_arbitrary_file_read is False
    assert report.ready_for_repo_search is False
    assert report.ready_for_git_status_execution is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_file_edit is False
    assert report.ready_for_patch_apply is False
    assert report.ready_for_provider_tool_calling is False
    assert report.ready_for_function_calling is False
    assert report.ready_for_subagent_invocation is False
    assert report.ready_for_memory_mutation is False
    assert report.ready_for_core_memory_write is False
    assert report.production_certified is False


def test_v0439_v04310_handoff_targets_structured_tui_mvp():
    handoff = arch.create_v04310_structured_tui_mvp_handoff()
    assert handoff.target_version == "v0.43.10 Structured TUI MVP"
    assert "workspace read" in handoff.still_closed


def test_v0439_v0440_handoff_keeps_controlled_workspace_read_design_after_tui_gates():
    handoff = arch.create_v0440_controlled_workspace_read_design_handoff()
    assert handoff.target_version == "v0.44.0 Controlled Workspace Read Design Gate"
    assert "workspace read implementation" in handoff.closed_until_gate


def test_v0439_integrated_document_exists_and_has_required_sections():
    text = DOC_PATH.read_text(encoding="utf-8")
    for section in arch.REQUIRED_V0439_RESTORE_SECTIONS:
        assert f"## {section}" in text


def test_v0439_integrated_document_contains_snapshot_contract_and_restore_prompt():
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "Snapshot Mode Contract" in text
    assert "Golden Snapshot Acceptance" in text
    assert "Copy-Paste Restore Prompt for Future GPT/Codex Session" in text


def test_v0439_no_separate_v0439_tui_renderer_adapter_docs_created():
    docs = sorted(path.name for path in (ROOT / "docs" / "versions" / "v0.43").iterdir() if "v0.43.9" in path.name)
    assert docs == [DOC_PATH.name]


def test_v0439_no_forbidden_runtime_call_patterns():
    forbidden = (
        "subprocess",
        "shell=True",
        "os.system",
        "eval(",
        "exec(",
        "apply_patch",
        "git apply",
        "git worktree",
        "git status",
        "invoke_subagent",
        "run_subagent",
        "create_child_session",
        "spawn_agent",
        "os.walk",
        "Path.rglob",
        ".rglob(",
    )
    for path in SCAN_PATHS:
        text = path.read_text(encoding="utf-8")
        for pattern in forbidden:
            assert pattern not in text, f"{pattern} found in {path}"


def test_v0439_no_textual_or_curses_required_for_snapshot_contract():
    decision = arch.create_v0439_tui_library_decision()
    assert decision.textual_dependency_added_now is False
    assert decision.recommended_v0439_engine == "pure_snapshot_renderer"
    for path in SCAN_PATHS:
        text = path.read_text(encoding="utf-8")
        assert "import textual" not in text
        assert "import curses" not in text


def test_v0439_no_repo_scan_shell_git_workspace_read_or_provider_completion_in_snapshot():
    result = snapshot.render_v0439_snapshot(width=120)
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False
    assert result.git_executed is False
    assert result.repo_search_used is False
    assert result.workspace_read_opened is False


def test_v0439_golden_cases_pass():
    cases = (
        snapshot.create_v0439_snapshot_golden_case("120", 120),
        snapshot.create_v0439_snapshot_golden_case("100", 100),
        snapshot.create_v0439_snapshot_golden_case("80", 80, expected_contains=("Schumpeter", "Project", "Session", "PI Monitor", "Input", "/help", "/status", "/exit")),
        snapshot.create_v0439_snapshot_golden_case("plain", 100, plain=True, expected_contains=("Schumpeter", "Project", "Session", "PI Monitor", "Chat", "Input", "Status")),
        snapshot.create_v0439_snapshot_golden_case("palette", 120, include_command_palette=True, expected_contains=("/summary", "/todo", "/memo", "/decision", "/handoff", "/status", "/exit")),
    )
    assert all(snapshot.execute_v0439_snapshot_golden_case(case).passed for case in cases)


def test_v0439_component_renderers_are_importable_and_pure():
    ui = state.create_v0439_ui_state()
    assert header.render_v0439_header(ui).provider_invoked is False
    assert code_block.render_v0439_code_block(ui).provider_invoked is False
    assert command_palette.render_v0439_command_palette(ui).provider_invoked is False
    msg = state.create_v0439_display_message("message")
    assert "message" in message_renderer.render_v0439_message(msg)
    assert "message" in artifact_renderer.render_v0439_artifact(msg)
    assert "message" in diagnostic_renderer.render_v0439_diagnostic(msg)
    assert "message" in status_renderer.render_v0439_status(msg)
    assert "message" in error_renderer.render_v0439_error(msg)
