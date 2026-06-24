from pathlib import Path

from chanta_core.personal_runtime import default_personal_command_palette as palette
from chanta_core.personal_runtime import default_personal_conversation_router as router
from chanta_core.personal_runtime import default_personal_schumpeter_lobby as lobby
from chanta_core.personal_runtime import default_personal_work_session as work


ROOT = Path(__file__).resolve().parents[1]
SCAN_PATHS = (
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_command_palette.py",
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_work_session.py",
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_schumpeter_lobby.py",
)


def test_v0438_2_command_categories_declared():
    values = {item.value for item in palette.V0438SlashCommandCategory}
    assert {
        "workflows",
        "artifacts",
        "notes",
        "evidence",
        "grounded_workflows",
        "pilot_release",
        "system",
        "unknown",
    }.issubset(values)


def test_v0438_2_command_registry_contains_workflows_artifacts_notes_evidence_grounded_pilot_system():
    registry = palette.create_v0438_slash_command_registry()
    categories = {command.category for command in registry.commands}
    assert {
        "workflows",
        "artifacts",
        "notes",
        "evidence",
        "grounded_workflows",
        "pilot_release",
        "system",
    }.issubset(categories)


def test_v0438_2_command_registry_is_deterministic_and_read_only():
    first = palette.create_v0438_slash_command_registry()
    second = palette.create_v0438_slash_command_registry()
    assert first.commands == second.commands
    assert first.deterministic is True
    assert first.read_only is True
    assert first.provider_invoked is False
    assert first.prompt_submitted is False
    assert first.shell_executed is False
    assert first.repo_search_used is False
    assert first.workspace_read_opened is False
    assert first.memory_mutated is False


def test_v0438_2_filter_empty_slash_returns_all_primary_commands_grouped():
    commands = palette.filter_v0438_slash_commands("/")
    grouped = palette.group_v0438_slash_commands(commands)
    assert len(commands) >= 40
    assert "workflows" in grouped
    assert "system" in grouped


def test_v0438_2_filter_s_returns_summary_and_status():
    commands = {command.command for command in palette.filter_v0438_slash_commands("/s")}
    assert "/summary" in commands
    assert "/status" in commands


def test_v0438_2_filter_grounded_returns_grounded_commands():
    commands = {command.command for command in palette.filter_v0438_slash_commands("/grounded")}
    assert "/grounded-summary" in commands
    assert "/grounding-check" in commands
    assert all(command.startswith("/ground") for command in commands)


def test_v0438_2_completion_items_insert_text_but_do_not_execute():
    result = palette.complete_v0438_slash_command("/s")
    assert any(item.command == "/summary" for item in result.items)
    assert all(item.executes_command is False for item in result.items)
    assert result.command_executed is False
    assert result.provider_invoked is False


def test_v0438_2_palette_render_shows_grouped_korean_descriptions():
    rendered = palette.render_v0438_command_palette().rendered_text
    assert "Schumpeter command palette" in rendered
    assert "Workflows" in rendered
    assert "/summary" in rendered
    assert "업무 요약 작성" in rendered


def test_v0438_2_palette_render_hides_noisy_metadata():
    rendered = palette.render_v0438_command_palette().rendered_text
    guard = palette.create_v0438_command_palette_noisy_output_guard(rendered)
    assert guard.passed is True


def test_v0438_2_plain_palette_fallback_works_without_prompt_toolkit():
    request = palette.create_v0438_slash_command_palette_request("/", plain=True)
    rendered = palette.render_v0438_command_palette_plain(request)
    assert "/help" in rendered
    assert "/exit" in rendered


def test_v0438_2_prompt_toolkit_detection_safe_when_missing():
    availability = palette.detect_v0438_prompt_toolkit_availability()
    assert availability.import_name == "prompt_toolkit"
    assert availability.safe_optional_dependency is True
    assert availability.production_certified is False


def test_v0438_2_interactive_input_policy_degrades_to_plain_input():
    policy = palette.create_v0438_interactive_input_policy()
    fallback = palette.create_v0438_plain_input_fallback_policy()
    assert policy.prompt_toolkit_optional is True
    assert policy.fallback_on_import_error is True
    assert policy.completion_executes_commands is False
    assert fallback.slash_enter_shows_palette is True
    assert fallback.interactive_completion_required is False


def test_v0438_2_command_palette_does_not_call_provider_prompt_shell_repo_workspace_or_memory():
    result = palette.render_v0438_command_palette()
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False
    assert result.repo_search_used is False
    assert result.workspace_read_opened is False
    assert result.memory_mutated is False
    assert result.core_memory_written is False
    assert result.production_certified is False


def test_v0438_2_command_palette_hides_chantagrowthkernel_and_legacy_schumpeter():
    rendered = palette.render_v0438_command_palette().rendered_text
    assert "ChantaGrowthKernel" not in rendered
    assert "legacy Schumpeter" not in rendered


def test_v0438_2_command_palette_safety_report_keeps_all_high_risk_closed():
    report = palette.create_v0438_command_palette_safety_report()
    assert report.command_palette_opened is True
    assert report.provider_invocation_allowed is False
    assert report.prompt_submission_allowed is False
    assert report.shell_execution_allowed is False
    assert report.git_execution_allowed is False
    assert report.repo_search_allowed is False
    assert report.workspace_read_allowed is False
    assert report.memory_mutation_allowed is False
    assert report.core_memory_write_allowed is False
    assert report.production_certified is False


def test_v0438_2_readiness_report_sets_palette_flags_true():
    report = palette.create_v0438_command_palette_readiness_report()
    assert report.command_registry_ready is True
    assert report.grouped_palette_ready is True
    assert report.completion_ready is True
    assert report.plain_fallback_ready is True
    assert report.start_lobby_hint_ready is True


def test_v0438_2_readiness_report_keeps_workspace_read_repo_shell_git_edit_tools_functions_subagent_memory_core_and_production_false():
    report = palette.create_v0438_command_palette_readiness_report()
    assert report.ready_for_workspace_read is False
    assert report.ready_for_repo_search is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_git_execution is False
    assert report.ready_for_file_edit is False
    assert report.ready_for_patch_apply is False
    assert report.ready_for_provider_tool_calling is False
    assert report.ready_for_function_calling is False
    assert report.ready_for_subagent_invocation is False
    assert report.ready_for_memory_mutation is False
    assert report.ready_for_core_memory_write is False
    assert report.production_certified is False


def test_v0438_2_start_lobby_mentions_slash_command_palette_or_help_hint():
    text = lobby.render_v0438_start_lobby(width=120).rendered_text
    assert "/help commands" in text


def test_v0438_2_regression_start_lobby_still_clean():
    result = lobby.render_v0438_start_lobby(width=120)
    assert result.contains_schumpeter_brand is True
    assert result.contains_raw_debug_metadata is False
    assert result.contains_raw_safety_footer is False
    assert result.provider_invoked is False
    assert result.shell_executed is False


def test_v0438_2_regression_v0437_identity_still_clean():
    answer = router.render_v0437_identity_answer()
    assert "업무 요약" not in answer.rendered_text
    assert "type:" not in answer.rendered_text
    assert "safety:" not in answer.rendered_text
    assert answer.production_certified is False


def test_v0438_2_work_session_slash_and_help_commands_use_same_palette():
    state = work.create_v043_work_session_state()
    slash = work.execute_v043_work_session_input("/", state)
    help_commands = work.execute_v043_work_session_input("/help commands", state)
    assert "Schumpeter command palette" in slash.rendered_text
    assert "Schumpeter command palette" in help_commands.rendered_text
    assert "/summary" in slash.rendered_text
    assert "/summary" in help_commands.rendered_text


def test_v0438_2_work_session_prefix_filter_suggests_without_execution():
    state = work.create_v043_work_session_state()
    result = work.execute_v043_work_session_input("/grounded", state)
    assert "/grounded-summary" in result.rendered_text
    assert result.provider_invoked is False
    assert result.prompt_submitted is False


def test_v0438_2_golden_palette_cases_pass():
    cases = (
        palette.V0438CommandPaletteGoldenCase("slash", "/", ("/summary", "/status", "/exit"), palette.FORBIDDEN_PALETTE_STRINGS, False),
        palette.V0438CommandPaletteGoldenCase("s", "/s", ("/summary", "/status"), palette.FORBIDDEN_PALETTE_STRINGS, False),
        palette.V0438CommandPaletteGoldenCase("grounded", "/grounded", ("/grounded-summary", "/grounding-check"), palette.FORBIDDEN_PALETTE_STRINGS, False),
    )
    assert all(palette.execute_v0438_command_palette_golden_case(case).passed for case in cases)


def test_v0438_2_no_forbidden_runtime_call_patterns():
    forbidden = (
        "subprocess",
        "shell=True",
        "os.system",
        "eval(",
        "exec(",
        "git status",
        "os.walk",
        "Path.rglob",
        "glob(",
        "repo scan",
    )
    for path in SCAN_PATHS:
        text = path.read_text(encoding="utf-8")
        for item in forbidden:
            assert item not in text
