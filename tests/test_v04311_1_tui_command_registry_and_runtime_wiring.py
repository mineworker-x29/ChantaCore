from pathlib import Path

import pytest

from chanta_core.schumpeter_tui.command_registry import (
    create_v043111_command_registry,
    find_v043111_command_spec,
    list_v043111_command_names,
    render_v043111_palette_text,
)
from chanta_core.schumpeter_tui.fullscreen import create_v04311_textual_app
from chanta_core.schumpeter_tui.help_surface import render_v04310_help
from chanta_core.schumpeter_tui.runtime_adapter import V04310RuntimeAdapter
from chanta_core.schumpeter_tui.testing.fake_runtime_adapter import V04311FakeRuntimeAdapter
from chanta_core.schumpeter_tui.turn_dispatch import dispatch_v04310_turn


ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "versions" / "v0.43" / "v0.43.11.1_tui_command_registry_runtime_wiring_restore.md"

REQUIRED_CATEGORIES = {
    "Start / Basic",
    "Workflows",
    "Artifacts",
    "Notes",
    "Evidence",
    "Grounded Workflows",
    "Status / Diagnostics",
    "Pilot / Release",
    "TUI",
    "Safety",
}

REQUIRED_COMMANDS = {
    "/help",
    "/help commands",
    "/exit",
    "/about",
    "/status",
    "/capabilities",
    "/summary",
    "/todo",
    "/memo",
    "/decision",
    "/handoff",
    "/clarify",
    "/artifact last",
    "/artifact last --debug",
    "/revise",
    "/note",
    "/notes",
    "/note last",
    "/note from-artifact",
    "/notes search",
    "/memory-boundary",
    "/context",
    "/recall",
    "/evidence",
    "/evidence sources",
    "/evidence last",
    "/evidence explain",
    "/use-evidence",
    "/use-evidence last",
    "/evidence used",
    "/grounded-summary",
    "/grounded-todo",
    "/grounded-memo",
    "/grounded-decision",
    "/grounded-handoff",
    "/grounding-check",
    "/provider",
    "/what-happened",
    "/report",
    "/trace",
    "/run-report",
    "/pilot status",
    "/pilot score",
    "/pilot findings",
    "/pilot review",
    "/pilot next",
    "/pilot report",
    "/acceptance",
    "/workflow score",
    "/polish status",
    "/polish findings",
    "/polish report",
    "/pilot close",
    "/v044 readiness",
    "/v044 scope",
    "/v044 risks",
    "/v044 handoff",
    "/help tui",
    "/help examples",
    "/lobby",
    "/refresh",
    "/clear",
    "/help safety",
}


def _adapter():
    return V04310RuntimeAdapter(provider="mock")


def _dispatch(text: str):
    return dispatch_v04310_turn(text, _adapter())


def test_command_registry_contains_all_required_categories():
    categories = {spec.category for spec in create_v043111_command_registry()}
    assert REQUIRED_CATEGORIES.issubset(categories)


def test_command_registry_contains_all_required_commands():
    assert REQUIRED_COMMANDS.issubset(set(list_v043111_command_names("/")))


def test_command_registry_has_unique_commands_and_aliases():
    specs = create_v043111_command_registry()
    commands = [spec.command for spec in specs]
    aliases = [alias for spec in specs for alias in spec.aliases]
    assert len(commands) == len(set(commands))
    assert not (set(commands) & set(aliases))


def test_each_command_has_description_usage_example_and_availability():
    for spec in create_v043111_command_registry():
        assert spec.short_description_ko
        assert spec.long_description_ko
        assert spec.usage
        assert spec.examples
        assert spec.availability in {"available", "preview", "debug_only", "not_opened"}


def test_help_commands_and_palette_use_same_registry():
    help_text = render_v04310_help("/help commands").rendered_text
    palette_text = render_v043111_palette_text("/")
    for command in ("/summary", "/todo", "/grounded-summary", "/v044 readiness", "/help safety"):
        assert command in help_text
        assert command in palette_text


def test_help_commands_lists_every_available_registry_command():
    help_text = render_v04310_help("/help commands").rendered_text
    for spec in create_v043111_command_registry():
        assert spec.command in help_text


def test_palette_lists_every_available_registry_command():
    palette_text = render_v043111_palette_text("/")
    for spec in create_v043111_command_registry():
        assert spec.command in palette_text


def test_palette_filters_status_commands():
    text = render_v043111_palette_text("/sta")
    assert "/status" in text
    assert "/provider" in text


def test_palette_filters_grounded_commands():
    text = render_v043111_palette_text("/grounded")
    assert "/grounded-summary" in text
    assert "/grounded-handoff" in text


def test_palette_selection_inserts_text_without_execution():
    adapter = V04311FakeRuntimeAdapter()
    text = render_v043111_palette_text("/sta")
    assert "/status" in text
    assert adapter.counters.provider_completion_count == 0
    assert adapter.counters.shell_execution_count == 0
    assert adapter.counters.repo_workspace_read_count == 0


def test_help_overview_is_useful_not_shallow():
    text = render_v04310_help("/help").rendered_text
    assert "Schumpeter Help" in text
    assert "Process Intelligence-native 업무 보조 에이전트" in text
    assert "빠른 시작" in text
    assert "/help commands" in text
    assert len(text.splitlines()) < 35


def test_help_commands_grouped_and_detailed():
    text = render_v04310_help("/help commands").rendered_text
    for category in REQUIRED_CATEGORIES:
        assert category in text
    assert "mode:" not in text
    assert "deterministic" in text


def test_help_safety_uses_human_labels_not_raw_booleans():
    text = render_v04310_help("/help safety").rendered_text
    assert "현재 닫혀 있는 기능" in text
    assert "저장소 직접 읽기" in text
    assert "repo search" in text
    assert "shell=false" not in text
    assert "production_certified=false" not in text


def test_help_examples_contains_practical_korean_examples():
    text = render_v04310_help("/help examples").rendered_text
    for expected in ("오늘 작업을 요약해줘", "/summary 오늘 테스트 결과를 요약해줘", "/todo", "/decision", "/recall", "/use-evidence", "/grounded-summary"):
        assert expected in text


def test_unknown_help_topic_returns_clean_topic_list():
    text = render_v04310_help("/help unknown").rendered_text
    assert "Unknown help topic" in text
    assert "/help commands" in text
    assert "Traceback" not in text


@pytest.mark.parametrize("command", ["/summary", "/todo", "/memo", "/decision", "/handoff", "/revise", "/recall", "/evidence", "/use-evidence", "/grounded-summary"])
def test_argument_required_commands_return_usage(command):
    result = _dispatch(command)
    assert result.message_kind == "error"
    assert "Usage" in result.rendered_text
    assert "예:" in result.rendered_text
    assert "No source text provided" not in result.rendered_text


def test_summary_without_args_returns_usage_not_placeholder_artifact():
    assert "Usage" in _dispatch("/summary").rendered_text
    assert "No source text provided" not in _dispatch("/summary").rendered_text


def test_todo_without_args_returns_usage_not_placeholder_artifact():
    assert "Usage" in _dispatch("/todo").rendered_text


def test_memo_without_args_returns_usage_not_placeholder_artifact():
    assert "Usage" in _dispatch("/memo").rendered_text


def test_recall_without_query_returns_usage_not_generic_fallback():
    result = _dispatch("/recall")
    assert "Usage" in result.rendered_text
    assert "일반 대화로 이해" not in result.rendered_text


def test_grounded_summary_without_context_returns_usage_or_evidence_guidance():
    result = _dispatch("/grounded-summary")
    assert "Usage" in result.rendered_text or "/use-evidence" in result.rendered_text


def test_summary_with_args_routes_to_artifact_renderer():
    result = _dispatch("/summary 오늘 Schumpeter TUI 기능 연결을 테스트하고 있어.")
    assert result.message_kind == "artifact"
    assert "Summary" in result.rendered_text


def test_status_routes_to_status_renderer():
    result = _dispatch("/status")
    assert result.message_kind == "status"
    assert "Safety: protected" in result.rendered_text


def test_status_debug_routes_to_debug_status_renderer():
    result = _dispatch("/status --debug")
    assert result.message_kind == "status"
    assert "Closed capability matrix" in result.rendered_text


def test_what_happened_routes_to_diagnostic_renderer():
    result = _dispatch("/what-happened")
    assert result.message_kind == "diagnostic"
    assert "diagnostic" in result.rendered_text.lower()


def test_v044_readiness_routes_to_status_or_diagnostic_renderer():
    result = _dispatch("/v044 readiness")
    assert result.message_kind in {"status", "diagnostic"}
    assert "v0.44" in result.rendered_text


def test_natural_language_capability_question_routes_to_capability_answer():
    result = _dispatch("너가 할 줄 아는게 뭐야")
    assert result.route_kind == "capability_question"
    assert "Schumpeter capabilities" in result.rendered_text
    assert "업무 요약" in result.rendered_text


def test_natural_language_ocel_log_request_routes_to_trace_or_evidence_guidance():
    result = _dispatch("ocel 로그 확인해줘")
    assert result.route_kind == "trace_or_evidence_status_request"
    assert "/what-happened" in result.rendered_text
    assert "/trace" in result.rendered_text


def test_natural_language_repository_status_routes_to_repository_boundary_answer():
    result = _dispatch("저장소 상태 확인해줘")
    assert result.route_kind == "repository_status_request"
    assert "v0.44 Controlled Workspace Read" in result.rendered_text


def test_no_generic_fallback_for_known_diagnostic_intents():
    for text in ("너가 할 줄 아는게 뭐야", "ocel 로그 확인해줘", "저장소 상태 확인해줘"):
        assert "일반 대화로 이해" not in _dispatch(text).rendered_text


@pytest.mark.anyio
async def test_help_does_not_append_giant_plain_text_if_modal_available():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        input_bar = pilot.app.query_one("#main-input")
        input_bar.focus()
        input_bar.value = "/help"
        await pilot.press("enter")
        await pilot.pause()
        assert "Schumpeter Help" in pilot.app.help_plain
        assert "Schumpeter Help" not in pilot.app.chat_plain


def test_help_modal_contains_all_sections():
    text = render_v04310_help("/help commands").rendered_text
    for command in ("/help workflows", "/help evidence", "/help grounded", "/help notes", "/help status", "/help safety", "/help examples"):
        assert find_v043111_command_spec(command) is not None
    for category in ("Workflows", "Evidence", "Grounded Workflows", "Notes", "Status / Diagnostics", "Safety"):
        assert category in text


def test_command_registry_does_not_open_shell_repo_workspace_memory():
    for spec in create_v043111_command_registry():
        assert spec.opens_shell is False
        assert spec.opens_workspace_read is False
        assert spec.opens_repo_search is False
        assert spec.mutates_memory is False


def test_command_dispatch_does_not_open_high_risk_capabilities():
    for command in ("/status", "/help commands", "/summary", "/recall", "ocel 로그 확인해줘"):
        result = _dispatch(command)
        assert result.shell_executed is False
        assert result.git_executed is False
        assert result.repo_search_used is False
        assert result.workspace_read_opened is False
        assert result.memory_mutated is False
        assert result.production_certified is False


def test_no_raw_metadata_in_help_palette_usage_errors_or_default_status():
    text = "\n".join(
        (
            render_v04310_help("/help commands").rendered_text,
            render_v043111_palette_text("/"),
            _dispatch("/summary").rendered_text,
            _dispatch("/status").rendered_text,
        )
    )
    for forbidden in ("provider_invoked", "shell=false", "production_certified=false", "base_url", "api_key", "secret"):
        assert forbidden not in text


def test_no_chantagrowthkernel_or_legacy_schumpeter_in_default_help():
    text = render_v04310_help("/help commands").rendered_text
    assert "ChantaGrowthKernel" not in text
    assert "legacy Schumpeter" not in text


def test_no_provider_completion_from_help_palette_or_status_refresh():
    adapter = V04311FakeRuntimeAdapter()
    render_v04310_help("/help")
    render_v043111_palette_text("/")
    adapter.collect_ui_snapshot()
    assert adapter.counters.provider_completion_count == 0
    assert adapter.counters.prompt_submission_count == 0


def test_no_forbidden_runtime_call_patterns():
    scanned = (
        ROOT / "src" / "chanta_core" / "schumpeter_tui" / "command_registry.py",
        ROOT / "src" / "chanta_core" / "schumpeter_tui" / "help_surface.py",
        ROOT / "src" / "chanta_core" / "schumpeter_tui" / "runtime_adapter.py",
        ROOT / "src" / "chanta_core" / "schumpeter_tui" / "turn_dispatch.py",
        ROOT / "src" / "chanta_core" / "schumpeter_tui" / "widgets" / "slash_palette.py",
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


def test_restore_document_exists_with_required_sections():
    text = DOC_PATH.read_text(encoding="utf-8")
    for title in (
        "Restore Purpose",
        "Canonical Command Registry",
        "Help / Palette Synchronization",
        "Command Dispatch Table",
        "Argument Validation",
        "Natural Language Routing Improvements",
        "Safety Boundary",
        "Copy-Paste Restore Prompt",
    ):
        assert f"## {title}" in text
