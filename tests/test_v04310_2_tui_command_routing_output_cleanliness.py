from chanta_core.schumpeter_tui import app, runtime_adapter
from chanta_core.schumpeter_tui.turn_dispatch import dispatch_v04310_turn, resolve_v043102_tui_command_route
from chanta_core.schumpeter_tui.turn_renderer import render_v04310_plain_turn, run_v04310_plain_interaction_sequence


FORBIDDEN_DEFAULT_STATUS_TERMS = (
    "workspace read",
    "repo search",
    "shell",
    "edit/apply",
    "subagents",
    "memory mutation",
    "production certification",
)


def _adapter():
    return runtime_adapter.V04310RuntimeAdapter(provider="mock")


def _turn(command: str):
    return dispatch_v04310_turn(command, _adapter())


def _golden_text():
    text, state = run_v04310_plain_interaction_sequence(
        (
            "/help",
            "/status",
            "넌 누구야",
            "/summary 오늘 TUI 테스트",
            "/what-happened",
            "/exit",
        ),
        width=100,
        adapter=_adapter(),
    )
    return text, state


def test_help_does_not_render_start_lobby():
    rendered = render_v04310_plain_turn(_turn("/help"))
    assert "Project\npath:" not in rendered
    assert "PI Monitor" not in rendered
    assert "Ask Schumpeter anything" not in rendered
    assert "Welcome to Schumpeter" not in rendered


def test_help_contains_command_groups():
    rendered = render_v04310_plain_turn(_turn("/help"))
    for expected in ("빠른 시작", "/help commands", "/help examples"):
        assert expected in rendered
    assert "/summary" in rendered
    assert "/status" in rendered
    assert "/exit" in rendered


def test_status_concise_no_raw_safety_footer():
    rendered = render_v04310_plain_turn(_turn("/status"))
    assert "Safety: protected" in rendered
    for term in FORBIDDEN_DEFAULT_STATUS_TERMS:
        assert term not in rendered


def test_status_debug_may_show_closed_capability_matrix():
    rendered = render_v04310_plain_turn(_turn("/status --debug"))
    assert "Closed capability matrix" in rendered
    assert "workspace read" in rendered
    assert "repo search" in rendered
    assert "production certification" in rendered


def test_normal_text_does_not_render_start_lobby():
    rendered = render_v04310_plain_turn(_turn("넌 누구야"))
    assert "You> 넌 누구야" in rendered
    assert "Schumpeter>" in rendered
    assert "Project\npath:" not in rendered
    assert "PI Monitor" not in rendered


def test_summary_does_not_render_start_lobby():
    rendered = render_v04310_plain_turn(_turn("/summary 오늘 TUI 테스트"))
    assert "Artifact>" in rendered
    assert "Project\npath:" not in rendered
    assert "PI Monitor" not in rendered
    assert "base_url" not in rendered
    assert "api_key" not in rendered


def test_what_happened_does_not_render_start_lobby():
    rendered = render_v04310_plain_turn(_turn("/what-happened"))
    assert "Diagnostic>" in rendered
    assert "Project\npath:" not in rendered
    assert "PI Monitor" not in rendered


def test_static_chrome_rendered_once_per_session():
    text, _state = _golden_text()
    assert text.count("Schumpeter\nProcess Intelligence-native Work Agent") <= 1
    assert text.count("Project\npath:") <= 1
    assert text.count("PI Monitor") <= 1
    assert text.count("Ask anything...") <= 1


def test_lobby_command_explicitly_renders_lobby_if_supported():
    rendered = render_v04310_plain_turn(_turn("/lobby"))
    assert "Lobby" in rendered
    assert "Schumpeter" in rendered
    assert "Project\npath:" not in rendered


def test_no_raw_metadata_in_normal_tui_outputs():
    text, _state = _golden_text()
    assert "base_url" not in text
    assert "api_key" not in text
    assert "grounding:" not in text
    assert "source:" not in text
    for term in FORBIDDEN_DEFAULT_STATUS_TERMS:
        assert term not in text


def test_no_provider_shell_repo_workspace_memory_side_effects_from_rendering():
    result = app.render_v04310_snapshot(100, plain=True)
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False
    assert result.git_executed is False
    assert result.repo_search_used is False
    assert result.workspace_read_opened is False
    assert result.memory_mutated is False


def test_exit_exits_cleanly():
    result = _turn("/exit")
    assert result.app_should_exit is True
    assert result.route_kind == "exit"
    assert "closed" in result.rendered_text.lower()


def test_explicit_command_route_table_maps_required_renderers():
    expected = {
        "/help": "help",
        "/status": "status",
        "/status --debug": "debug_status",
        "/summary": "artifact",
        "/what-happened": "diagnostic",
        "/lobby": "lobby",
    }
    for command, renderer in expected.items():
        route = resolve_v043102_tui_command_route(command)
        assert route is not None
        assert route.renderer_kind == renderer
        assert route.rerender_full_static_chrome is False


def test_golden_interaction_has_clean_distinct_renderer_outputs():
    text, state = _golden_text()
    assert "Schumpeter Help" in text
    assert "Safety: protected" in text
    assert "Schumpeter>" in text
    assert "Artifact>" in text
    assert "Diagnostic>" in text
    assert state.exit_requested is True
