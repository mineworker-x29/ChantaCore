from chanta_core.schumpeter_tui.command_registry import (
    create_v043111_command_registry,
    group_v043111_command_specs,
    list_v043111_command_names,
)
from chanta_core.schumpeter_tui.help_surface import render_v04310_help
from chanta_core.schumpeter_tui.runtime_adapter import V04310RuntimeAdapter
from chanta_core.schumpeter_tui.turn_dispatch import dispatch_v04310_turn
from chanta_core.schumpeter_tui.widgets.slash_palette import (
    create_v043112_palette_state,
    insert_v043112_selected_command,
    move_v043112_palette_selection,
    render_rows_v043112_palette,
    render_v043112_palette_text,
    selectable_v043112_palette_commands,
)


REQUIRED_BY_GROUP = {
    "Start / Basic": ("/help", "/help commands", "/exit", "/about", "/status", "/status --debug", "/capabilities"),
    "Workflows": ("/summary", "/todo", "/memo", "/decision", "/handoff", "/clarify"),
    "Artifacts": ("/artifact last", "/artifact last --debug", "/revise"),
    "Notes": ("/note", "/notes", "/note last", "/note from-artifact", "/notes search", "/memory-boundary", "/context"),
    "Evidence": ("/recall", "/evidence", "/evidence sources", "/evidence last", "/evidence explain", "/use-evidence", "/use-evidence last", "/evidence used"),
    "Grounded Workflows": ("/grounded-summary", "/grounded-todo", "/grounded-memo", "/grounded-decision", "/grounded-handoff", "/grounding-check"),
    "Status / Diagnostics": ("/provider", "/what-happened", "/report", "/trace", "/run-report", "/v044 readiness"),
    "Pilot / Release": ("/pilot status", "/pilot score", "/pilot findings", "/pilot review", "/pilot next", "/pilot report", "/acceptance", "/workflow score", "/polish status", "/polish findings", "/polish report", "/pilot close", "/v044 scope", "/v044 risks", "/v044 handoff"),
    "TUI": ("/help tui", "/help examples", "/lobby", "/refresh", "/clear"),
    "Safety": ("/help safety",),
}


def _adapter():
    return V04310RuntimeAdapter(provider="mock")


def test_registry_contains_all_required_categories():
    grouped = group_v043111_command_specs(create_v043111_command_registry())
    assert set(REQUIRED_BY_GROUP).issubset(set(grouped))


def test_registry_contains_workflow_commands():
    grouped = group_v043111_command_specs(create_v043111_command_registry())
    assert set(REQUIRED_BY_GROUP["Workflows"]).issubset({spec.command for spec in grouped["Workflows"]})


def test_registry_contains_evidence_commands():
    grouped = group_v043111_command_specs(create_v043111_command_registry())
    assert set(REQUIRED_BY_GROUP["Evidence"]).issubset({spec.command for spec in grouped["Evidence"]})


def test_registry_contains_grounded_commands():
    grouped = group_v043111_command_specs(create_v043111_command_registry())
    assert set(REQUIRED_BY_GROUP["Grounded Workflows"]).issubset({spec.command for spec in grouped["Grounded Workflows"]})


def test_registry_contains_pilot_release_commands():
    grouped = group_v043111_command_specs(create_v043111_command_registry())
    assert set(REQUIRED_BY_GROUP["Pilot / Release"]).issubset({spec.command for spec in grouped["Pilot / Release"]})


def test_palette_does_not_repeat_category_suffix_on_each_row():
    text = render_v043112_palette_text(create_v043112_palette_state("/"))
    command_rows = [line for line in text.splitlines() if line.startswith(("> /", "  /"))]
    assert command_rows
    assert all(not row.rstrip().endswith("Start / Basic") for row in command_rows)
    assert all("  Workflows" not in row for row in command_rows)


def test_palette_renders_group_headers():
    text = render_v043112_palette_text(create_v043112_palette_state("/"))
    for header in ("Start / Basic", "Workflows", "Artifacts", "Notes"):
        assert header in text


def test_palette_slash_shows_multiple_categories():
    rows = render_rows_v043112_palette(create_v043112_palette_state("/"))
    headers = [text for kind, text in rows if kind == "header"]
    assert len(headers) >= 4
    assert "Start / Basic" in headers
    assert "Workflows" in headers


def test_palette_filter_s_searches_all_categories():
    text = render_v043112_palette_text(create_v043112_palette_state("/s"))
    assert "/summary" in text
    assert "/status" in text
    assert "/status --debug" in text


def test_palette_filter_grounded_shows_grounded_category():
    text = render_v043112_palette_text(create_v043112_palette_state("/grounded"))
    assert "Grounded Workflows" in text
    assert "/grounded-summary" in text
    assert "/grounded-handoff" in text


def test_category_headers_not_selectable():
    state = create_v043112_palette_state("/")
    selectable = selectable_v043112_palette_commands(state)
    headers = {text for kind, text in render_rows_v043112_palette(state) if kind == "header"}
    assert selectable
    assert not (set(selectable) & headers)


def test_arrow_navigation_skips_category_headers():
    state = create_v043112_palette_state("/")
    state, result = move_v043112_palette_selection(state, 1)
    assert result.command_executed is False
    assert state.filtered_commands[state.selected_index].startswith("/")


def test_enter_inserts_selected_command_without_execution():
    state = create_v043112_palette_state("/s")
    result = insert_v043112_selected_command(state)
    assert result.inserted_text.startswith("/summary")
    assert result.command_executed is False


def test_help_commands_uses_same_registry_as_palette():
    help_text = render_v04310_help("/help commands").rendered_text
    palette_names = set(list_v043111_command_names("/"))
    for command in palette_names:
        assert command in help_text


def test_no_provider_shell_repo_workspace_memory_side_effects():
    state = create_v043112_palette_state("/")
    assert state.provider_invoked is False
    assert state.shell_executed is False
    assert state.repo_search_used is False
    assert state.workspace_read_opened is False
    assert state.memory_mutated is False


def test_no_chantagrowthkernel_or_legacy_schumpeter():
    text = "\n".join((render_v043112_palette_text(create_v043112_palette_state("/")), render_v04310_help("/help commands").rendered_text))
    assert "ChantaGrowthKernel" not in text
    assert "legacy Schumpeter" not in text


def test_no_raw_safety_booleans():
    text = "\n".join((render_v043112_palette_text(create_v043112_palette_state("/")), render_v04310_help("/help commands").rendered_text))
    for forbidden in ("shell=false", "provider_invoked", "production_certified=false"):
        assert forbidden not in text


def test_unknown_or_unimplemented_command_returns_clean_unavailable_response():
    result = dispatch_v04310_turn("/refresh", _adapter())
    assert result.message_kind == "error"
    assert "Unavailable" in result.rendered_text
    assert "Traceback" not in result.rendered_text
    assert result.provider_invoked is False
