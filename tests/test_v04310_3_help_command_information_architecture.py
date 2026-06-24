from pathlib import Path

from chanta_core.schumpeter_tui import help_surface
from chanta_core.schumpeter_tui.turn_dispatch import dispatch_v04310_turn
from chanta_core.schumpeter_tui.turn_renderer import run_v04310_plain_interaction_sequence
from chanta_core.schumpeter_tui.runtime_adapter import V04310RuntimeAdapter


ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "versions" / "v0.43" / "v0.43.10.3_help_command_information_architecture_restore.md"


def _text(command: str) -> str:
    return help_surface.render_v04310_help(command).rendered_text


def test_help_topics_declared():
    topic = help_surface.create_v04310_help_topic("commands")
    assert topic.command == "/help commands"
    assert topic.production_certified is False


def test_help_modes_declared():
    values = {item.value for item in help_surface.V04310HelpMode}
    assert {"overview", "commands", "workflows", "evidence", "grounded", "notes", "status", "safety", "tui", "examples", "unknown"}.issubset(values)


def test_help_overview_is_concise_and_user_facing():
    text = _text("/help")
    assert "Schumpeter Help" in text
    assert "Process Intelligence-native 업무 보조 에이전트" in text
    assert len(text.splitlines()) < 30
    assert "provider_invoked" not in text


def test_help_overview_contains_quick_start():
    text = _text("/help")
    for expected in ("빠른 시작", "그냥 입력하기", "/summary", "/todo", "/recall", "/status", "/exit"):
        assert expected in text


def test_help_overview_points_to_detailed_help_topics():
    text = _text("/help")
    for expected in ("/help commands", "/help workflows", "/help evidence", "/help grounded", "/help notes", "/help status", "/help safety", "/help tui", "/help examples"):
        assert expected in text


def test_help_commands_uses_shared_registry():
    report = help_surface.create_v04310_help_registry_consistency_report()
    assert report.shared_registry_used is True
    assert "/summary" in report.help_command_names
    assert "/summary" in report.palette_command_names
    assert report.missing_from_palette == ()


def test_help_commands_grouped_by_category():
    text = _text("/help commands")
    for expected in ("Workflows", "Artifacts", "Notes", "Evidence", "Grounded Workflows", "Status / Diagnostics", "Pilot / Release", "TUI", "Safety", "Exit"):
        assert expected in text


def test_help_workflows_describes_summary_todo_memo_decision_handoff_clarify():
    text = _text("/help workflows")
    for expected in ("/summary", "/todo", "/memo", "/decision", "/handoff", "/clarify"):
        assert expected in text
    assert "may use provider" in text


def test_help_evidence_describes_recall_evidence_sources_use_evidence():
    text = _text("/help evidence")
    for expected in ("/recall", "/evidence sources", "/evidence last", "/evidence explain", "/use-evidence", "/evidence used"):
        assert expected in text
    assert "read-only" in text


def test_help_grounded_describes_grounded_summary_todo_memo_decision_handoff_and_grounding_check():
    text = _text("/help grounded")
    for expected in ("/grounded-summary", "/grounded-todo", "/grounded-memo", "/grounded-decision", "/grounded-handoff", "/grounding-check"):
        assert expected in text


def test_help_notes_describes_note_notes_search_memory_boundary_context():
    text = _text("/help notes")
    for expected in ("/note", "/notes", "/note last", "/note from-artifact", "/notes search", "/memory-boundary", "/context"):
        assert expected in text
    assert "local note write" in text


def test_help_status_describes_status_provider_about_what_happened_report_v044_readiness():
    text = _text("/help status")
    for expected in ("/status", "/provider", "/about", "/what-happened", "/report", "/pilot status", "/v044 readiness"):
        assert expected in text


def test_help_safety_explains_closed_capabilities_without_raw_footer():
    text = _text("/help safety")
    for expected in ("현재 닫혀 있는 기능", "저장소 직접 읽기", "repo search", "셸/git 실행", "파일 수정/apply", "subagent", "production certification", "v0.44"):
        assert expected in text
    assert "shell=false" not in text
    assert "production_certified=false" not in text


def test_help_tui_explains_input_slash_palette_status_exit():
    text = _text("/help tui")
    for expected in ("일반 문장", "slash command", "command suggestions", "/help commands", "/status", "/exit"):
        assert expected in text


def test_help_examples_contains_practical_korean_examples():
    text = _text("/help examples")
    for expected in ("오늘 회의 내용을 정리해줘", "/summary 오늘 테스트 결과를 요약해줘", "/todo", "/decision", "/recall", "/use-evidence", "/grounded-summary"):
        assert expected in text


def test_help_result_has_no_chantagrowthkernel_or_legacy_schumpeter():
    all_text = "\n".join(_text(command) for command in ("/help", "/help commands", "/help examples"))
    assert "ChantaGrowthKernel" not in all_text
    assert "legacy Schumpeter" not in all_text


def test_help_result_has_no_raw_safety_booleans():
    all_text = "\n".join(_text(command) for command in ("/help", "/help commands", "/help safety"))
    for forbidden in ("shell=false", "production_certified=false", "provider_invoked", "prompt_submitted"):
        assert forbidden not in all_text


def test_help_result_has_no_provider_secret_base_url_or_debug_metadata():
    all_text = "\n".join(_text(command) for command in ("/help", "/help commands", "/help status"))
    for forbidden in ("base_url", "api_key", "secret", "Traceback"):
        assert forbidden not in all_text


def test_help_side_effect_labels_are_human_facing_not_raw_flags():
    text = _text("/help workflows")
    assert "mode: may use provider" in text
    assert "provider_invoked" not in text


def test_help_palette_and_help_commands_share_command_names():
    report = help_surface.create_v04310_help_registry_consistency_report()
    assert "/summary" in report.palette_command_names
    assert "/summary" in report.help_command_names
    assert "/exit" in report.help_command_names


def test_help_unknown_topic_returns_clean_error_with_available_topics():
    text = _text("/help unknown")
    assert "Unknown help topic" in text
    assert "/help commands" in text
    assert "Traceback" not in text


def test_help_does_not_render_start_lobby():
    result = dispatch_v04310_turn("/help", V04310RuntimeAdapter(provider="mock"))
    assert "Project\npath:" not in result.rendered_text
    assert "PI Monitor" not in result.rendered_text


def test_help_does_not_reset_transcript():
    text, state = run_v04310_plain_interaction_sequence(("/help", "넌 누구야"), adapter=V04310RuntimeAdapter(provider="mock"))
    kinds = [message.kind for message in state.transcript]
    assert kinds[-4:] == ["user", "status", "user", "assistant"]
    assert text.count("Schumpeter\nProcess Intelligence-native Work Agent") == 1


def test_help_does_not_call_provider_shell_repo_workspace_or_memory():
    result = help_surface.render_v04310_help("/help commands")
    assert result.provider_invoked is False
    assert result.shell_executed is False
    assert result.repo_search_used is False
    assert result.workspace_read_opened is False
    assert result.memory_mutated is False


def test_help_safety_report_keeps_all_high_risk_closed():
    report = help_surface.create_v04310_help_safety_report()
    assert report.help_surface_opened is True
    assert report.workspace_read_opened is False
    assert report.repo_search_opened is False
    assert report.shell_execution_opened is False
    assert report.git_execution_opened is False
    assert report.file_edit_opened is False
    assert report.provider_tool_calling_opened is False
    assert report.function_calling_opened is False
    assert report.subagent_opened is False
    assert report.memory_mutation_opened is False
    assert report.core_memory_write_opened is False
    assert report.production_certified is False


def test_help_readiness_report_sets_help_surface_flags_true():
    report = help_surface.create_v04310_help_readiness_report()
    assert report.help_surface_ready is True
    assert report.help_topics_ready is True
    assert report.shared_registry_consistency_ready is True
    assert report.golden_help_ready is True


def test_help_readiness_report_keeps_workspace_repo_shell_git_edit_tools_functions_subagent_memory_core_and_production_false():
    report = help_surface.create_v04310_help_readiness_report()
    assert report.ready_for_workspace_read is False
    assert report.ready_for_repo_search is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_git_execution is False
    assert report.ready_for_file_edit is False
    assert report.ready_for_provider_tool_calling is False
    assert report.ready_for_function_calling is False
    assert report.ready_for_subagent_invocation is False
    assert report.ready_for_memory_mutation is False
    assert report.ready_for_core_memory_write is False
    assert report.production_certified is False


def test_help_golden_overview_passes():
    assert help_surface.execute_v04310_help_golden_case("/help").passed is True


def test_help_golden_commands_passes():
    assert help_surface.execute_v04310_help_golden_case("/help commands").passed is True


def test_help_golden_safety_passes():
    assert help_surface.execute_v04310_help_golden_case("/help safety").passed is True


def test_help_golden_examples_passes():
    assert help_surface.execute_v04310_help_golden_case("/help examples").passed is True


def test_help_no_forbidden_runtime_call_patterns():
    scanned = (
        ROOT / "src" / "chanta_core" / "schumpeter_tui" / "help_surface.py",
        ROOT / "src" / "chanta_core" / "schumpeter_tui" / "runtime_adapter.py",
        ROOT / "src" / "chanta_core" / "schumpeter_tui" / "turn_dispatch.py",
        ROOT / "src" / "chanta_core" / "schumpeter_tui" / "command_registry.py",
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


def test_help_restore_document_exists_and_has_sections():
    text = DOC_PATH.read_text(encoding="utf-8")
    for title in ("Restore Purpose", "User-Observed Help Problem", "Help Information Architecture", "Command Registry Integration", "Safety Help Contract", "Copy-Paste Restore Prompt"):
        assert f"## {title}" in text
