"""v0.43.10 structured TUI MVP controller and pure render helpers."""

from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Sequence

from chanta_core.schumpeter_tui.app_state import (
    V04310TUIAppState,
    V04310TUITurnResult,
    V04310TranscriptMessageKind,
    append_v04310_transcript_message,
    create_v04310_tui_app_state,
    create_v04310_transcript_message,
)
from chanta_core.schumpeter_tui.command_registry import (
    list_v043111_command_names,
    render_v043111_palette_text,
)
from chanta_core.schumpeter_tui.display_width import (
    assert_v0439_lines_within_width,
    pad_to_display_width_v0439,
    truncate_to_display_width_v0439,
)
from chanta_core.schumpeter_tui.runtime_adapter import V04310RuntimeAdapter, collect_v04310_runtime_snapshot
from chanta_core.schumpeter_tui.theme import create_v0439_theme_glyphs
from chanta_core.schumpeter_tui.widgets.message_view import render_v043117_card_text


V04311_BOTTOM_LAYOUT_REGION_IDS = ("palette-region", "input-region", "status-region")
V04311_INPUT_STATUS_CLEARANCE_ROWS = 1
V0431111_HELP_MODAL_TRAPS_INPUT = True


class V04310ComponentKind(StrEnum):
    SIDEBAR = "sidebar"
    MAIN_PANEL = "main_panel"
    INPUT_BOX = "input_box"
    STATUS_LINE = "status_line"
    COMMAND_PALETTE = "command_palette"
    CODE_BLOCK = "code_block"
    UNKNOWN = "unknown"


class V04310RendererKind(StrEnum):
    MESSAGE = "message"
    ARTIFACT = "artifact"
    DIAGNOSTIC = "diagnostic"
    STATUS = "status"
    ERROR = "error"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V04310TUIEntrypointPolicy:
    policy_id: str
    primary_command: str
    start_alias_allowed: bool
    replaces_existing_start_by_default: bool
    snapshot_command_required: bool
    interactive_preview_enabled: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310PromptToolkitPolicy:
    policy_id: str
    prompt_toolkit_supported: bool
    prompt_toolkit_required_for_full_tui: bool
    import_is_lazy: bool
    fallback_when_missing: bool
    dependency_added_as_optional: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310PlainFallbackPolicy:
    policy_id: str
    prints_structured_snapshot_first: bool
    line_input_loop_available: bool
    slash_help_fallback_available: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310InteractiveLoopPolicy:
    policy_id: str
    enter_submits: bool
    slash_commands_supported: bool
    normal_text_supported: bool
    exits_on_slash_exit: bool
    exits_on_ctrl_c: bool
    exits_on_eof: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310ComponentRenderResult:
    result_id: str
    component_kind: str
    rendered_text: str
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    memory_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310RendererResult:
    result_id: str
    renderer_kind: str
    rendered_text: str
    raw_metadata_visible: bool
    executes_runtime_action: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310KeyBindingPolicy:
    policy_id: str
    slash_opens_palette: bool
    enter_submits: bool
    escape_closes_palette_or_exits: bool
    ctrl_c_exits_gracefully: bool
    tab_completes_if_supported: bool
    command_executes_before_enter: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310CommandCompletionPolicy:
    policy_id: str
    uses_shared_command_registry: bool
    filters_by_prefix: bool
    inserts_text_only: bool
    executes_command_during_completion: bool
    provider_invoked: bool
    shell_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310CommandPaletteResult:
    result_id: str
    prefix: str
    rendered_text: str
    commands: tuple[str, ...]
    command_executed: bool
    provider_invoked: bool
    shell_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310SnapshotRequest:
    request_id: str
    width: int
    plain: bool
    include_command_palette: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310SnapshotResult:
    result_id: str
    rendered_text: str
    width: int
    mode: str
    line_count: int
    all_lines_within_width: bool
    contains_sidebar: bool
    contains_main_panel: bool
    contains_input_box: bool
    contains_status_bar: bool
    contains_command_palette: bool
    contains_schumpeter_brand: bool
    contains_forbidden_default_strings: bool
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    git_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    memory_mutated: bool
    core_memory_written: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310InteractiveSmokeResult:
    result_id: str
    app_initialized: bool
    structured_snapshot_rendered: bool
    adapter_used_for_submit: bool
    provider_invoked_by_rendering: bool
    shell_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    memory_mutated_by_rendering: bool
    production_certified: bool


FORBIDDEN_V04310_DEFAULT_STRINGS = (
    "ChantaGrowthKernel",
    "GrowthKernel",
    "legacy Schumpeter",
    "ChantaCore legacy core",
    "safety:",
    "shell=false",
    "production_certified=false",
    "grounding:",
    "source:",
    "base_url=",
    "api_key",
    "secret",
)


def create_v04310_tui_entrypoint_policy(**overrides: Any) -> V04310TUIEntrypointPolicy:
    defaults = {
        "policy_id": "v04310-tui-entrypoint-policy",
        "primary_command": "chanta-cli tui",
        "start_alias_allowed": True,
        "replaces_existing_start_by_default": False,
        "snapshot_command_required": True,
        "interactive_preview_enabled": True,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310TUIEntrypointPolicy(**defaults)


def detect_v04310_prompt_toolkit() -> bool:
    try:
        return importlib.util.find_spec("prompt_toolkit") is not None
    except Exception:
        return False


def create_v04310_prompt_toolkit_policy(**overrides: Any) -> V04310PromptToolkitPolicy:
    defaults = {
        "policy_id": "v04310-prompt-toolkit-policy",
        "prompt_toolkit_supported": detect_v04310_prompt_toolkit(),
        "prompt_toolkit_required_for_full_tui": False,
        "import_is_lazy": True,
        "fallback_when_missing": True,
        "dependency_added_as_optional": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310PromptToolkitPolicy(**defaults)


def create_v04310_plain_fallback_policy(**overrides: Any) -> V04310PlainFallbackPolicy:
    defaults = {
        "policy_id": "v04310-plain-fallback-policy",
        "prints_structured_snapshot_first": True,
        "line_input_loop_available": True,
        "slash_help_fallback_available": True,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310PlainFallbackPolicy(**defaults)


def create_v04310_interactive_loop_policy(**overrides: Any) -> V04310InteractiveLoopPolicy:
    defaults = {
        "policy_id": "v04310-interactive-loop-policy",
        "enter_submits": True,
        "slash_commands_supported": True,
        "normal_text_supported": True,
        "exits_on_slash_exit": True,
        "exits_on_ctrl_c": True,
        "exits_on_eof": True,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310InteractiveLoopPolicy(**defaults)


def create_v04310_key_binding_policy(**overrides: Any) -> V04310KeyBindingPolicy:
    defaults = {
        "policy_id": "v04310-key-binding-policy",
        "slash_opens_palette": True,
        "enter_submits": True,
        "escape_closes_palette_or_exits": True,
        "ctrl_c_exits_gracefully": True,
        "tab_completes_if_supported": True,
        "command_executes_before_enter": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310KeyBindingPolicy(**defaults)


def create_v04310_command_completion_policy(**overrides: Any) -> V04310CommandCompletionPolicy:
    defaults = {
        "policy_id": "v04310-command-completion-policy",
        "uses_shared_command_registry": True,
        "filters_by_prefix": True,
        "inserts_text_only": True,
        "executes_command_during_completion": False,
        "provider_invoked": False,
        "shell_executed": False,
        "repo_search_used": False,
        "workspace_read_opened": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310CommandCompletionPolicy(**defaults)


def complete_v04310_slash_command(prefix: str = "/") -> tuple[str, ...]:
    return list_v043111_command_names(prefix)


def create_v04310_command_palette_result(prefix: str = "/", **overrides: Any) -> V04310CommandPaletteResult:
    commands = complete_v04310_slash_command(prefix)
    text = render_v043111_palette_text(prefix)
    defaults = {
        "result_id": "v04310-command-palette-result",
        "prefix": prefix,
        "rendered_text": text,
        "commands": commands,
        "command_executed": False,
        "provider_invoked": False,
        "shell_executed": False,
        "repo_search_used": False,
        "workspace_read_opened": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310CommandPaletteResult(**defaults)


def _component_result(kind: str, text: str) -> V04310ComponentRenderResult:
    return V04310ComponentRenderResult(
        result_id=f"v04310-{kind}-component-result",
        component_kind=kind,
        rendered_text=text,
        provider_invoked=False,
        prompt_submitted=False,
        shell_executed=False,
        repo_search_used=False,
        workspace_read_opened=False,
        memory_mutated=False,
        production_certified=False,
    )


def render_v04310_sidebar(app_state: V04310TUIAppState) -> V04310ComponentRenderResult:
    s = app_state.sidebar
    lines = [
        "SCHUMPETER",
        s.subtitle,
        "",
        "PROJECT",
        f"path: {app_state.runtime_snapshot.working_directory_label or 'unknown'}",
        f"mode: {s.mode_label}",
        "",
        "SESSION",
        f"profile: {s.profile_id}",
        f"provider: {s.provider_label}",
        "",
        "PI MONITOR",
        f"PI        {s.pi_status}",
        f"Provider  {s.provider_status}",
        f"Trace     {s.trace_status}",
        f"Evidence  {s.evidence_status}",
        f"Safety    {s.safety_status}",
        "",
        "COMMANDS",
        " /help",
        " /status",
        " /exit",
    ]
    return _component_result(V04310ComponentKind.SIDEBAR.value, "\n".join(lines))


def render_v04310_message(message) -> V04310RendererResult:
    return V04310RendererResult("v04310-message-renderer", "message", render_v043117_card_text(message.text, message.kind), False, False, False)


def render_v04310_artifact(message) -> V04310RendererResult:
    return V04310RendererResult("v04310-artifact-renderer", "artifact", render_v043117_card_text(message.text, "artifact"), False, False, False)


def render_v04310_diagnostic(message) -> V04310RendererResult:
    return V04310RendererResult("v04310-diagnostic-renderer", "diagnostic", render_v043117_card_text(message.text, "diagnostic"), False, False, False)


def render_v04310_status(message) -> V04310RendererResult:
    return V04310RendererResult("v04310-status-renderer", "status", render_v043117_card_text(message.text, "status"), False, False, False)


def render_v04310_error(message) -> V04310RendererResult:
    return V04310RendererResult("v04310-error-renderer", "error", render_v043117_card_text(message.text, "error"), False, False, False)


def render_v04310_main_panel(app_state: V04310TUIAppState) -> V04310ComponentRenderResult:
    lines = [app_state.main_panel.welcome_title, app_state.main_panel.welcome_subtitle, ""]
    for message in app_state.transcript:
        if message.kind == "system_notice":
            continue
        if message.kind == "artifact":
            rendered = render_v04310_artifact(message).rendered_text
        elif message.kind == "diagnostic":
            rendered = render_v04310_diagnostic(message).rendered_text
        elif message.kind == "status":
            rendered = render_v04310_status(message).rendered_text
        elif message.kind == "error":
            rendered = render_v04310_error(message).rendered_text
        else:
            rendered = render_v04310_message(message).rendered_text
        lines.extend(rendered.splitlines())
        lines.append("")
    return _component_result(V04310ComponentKind.MAIN_PANEL.value, "\n".join(lines).rstrip())


def render_v04310_input_box(app_state: V04310TUIAppState) -> V04310ComponentRenderResult:
    text = app_state.input_state.current_text or app_state.input_state.placeholder
    return _component_result(V04310ComponentKind.INPUT_BOX.value, f"Input\n{text}")


def render_v04310_status_line(app_state: V04310TUIAppState) -> V04310ComponentRenderResult:
    return _component_result(V04310ComponentKind.STATUS_LINE.value, app_state.status_line.compact_text)


def render_v04310_command_palette(app_state: V04310TUIAppState) -> V04310ComponentRenderResult:
    return _component_result(V04310ComponentKind.COMMAND_PALETTE.value, create_v04310_command_palette_result(app_state.palette_state.prefix).rendered_text)


def _input_box_frame(width: int, plain: bool, placeholder: str) -> tuple[str, str, str]:
    glyphs = create_v0439_theme_glyphs(plain)
    if plain:
        return ("Input", placeholder, "")
    title = " Input "
    top = f"{glyphs.input_top_left}{glyphs.input_horizontal}{title}{glyphs.input_horizontal * max(0, width - 2 - len(title) - 1)}{glyphs.input_top_right}"
    middle = f"{glyphs.input_vertical}{pad_to_display_width_v0439(' ' + placeholder, width - 2)}{glyphs.input_vertical}"
    bottom = f"{glyphs.input_bottom_left}{glyphs.input_horizontal * (width - 2)}{glyphs.input_bottom_right}"
    return top, middle, bottom


def _render_two_column(app_state: V04310TUIAppState, width: int, include_command_palette: bool) -> str:
    glyphs = create_v0439_theme_glyphs(False)
    left_width = 30
    right_width = max(40, width - left_width - 3)
    left = render_v04310_sidebar(app_state).rendered_text.splitlines()
    right = render_v04310_main_panel(app_state).rendered_text.splitlines()
    right.extend(_input_box_frame(right_width, False, app_state.input_state.placeholder))
    right.append("   ".join(app_state.sidebar.command_shortcuts))
    right.append(render_v04310_status_line(app_state).rendered_text)
    if include_command_palette:
        right.append("")
        right.extend(render_v04310_command_palette(app_state).rendered_text.splitlines())
    row_count = max(len(left), len(right))
    left.extend([""] * (row_count - len(left)))
    right.extend([""] * (row_count - len(right)))
    lines = [f"{glyphs.top_left}{glyphs.horizontal * left_width}{glyphs.tee_down}{glyphs.horizontal * right_width}{glyphs.top_right}"]
    for lval, rval in zip(left, right, strict=True):
        lines.append(f"{glyphs.vertical}{pad_to_display_width_v0439(lval, left_width)}{glyphs.vertical}{pad_to_display_width_v0439(rval, right_width)}{glyphs.vertical}")
    lines.append(f"{glyphs.bottom_left}{glyphs.horizontal * left_width}{glyphs.tee_up}{glyphs.horizontal * right_width}{glyphs.bottom_right}")
    return "\n".join(lines)


def _render_compact(app_state: V04310TUIAppState, width: int, include_command_palette: bool, plain: bool = False) -> str:
    lines = [
        "Schumpeter",
        "Process Intelligence-native Work Agent",
        "",
        "Project",
        f"path: {app_state.runtime_snapshot.working_directory_label}",
        f"mode: {app_state.sidebar.mode_label}",
        "",
        "Session",
        f"profile: {app_state.sidebar.profile_id}",
        f"provider: {app_state.sidebar.provider_label}",
        "",
        "PI Monitor",
        f"PI {app_state.sidebar.pi_status} | Provider {app_state.sidebar.provider_status} | Trace {app_state.sidebar.trace_status}",
        f"Evidence {app_state.sidebar.evidence_status} | Safety {app_state.sidebar.safety_status}",
        "",
        "Chat",
    ]
    for message in app_state.transcript:
        if message.kind == "system_notice":
            continue
        lines.extend(render_v043117_card_text(message.text, message.kind, width=max(28, width - 2)).splitlines())
        lines.append("")
    lines.extend(("", "Input", app_state.input_state.placeholder, "   ".join(app_state.sidebar.command_shortcuts), render_v04310_status_line(app_state).rendered_text))
    if include_command_palette:
        lines.extend(("", render_v04310_command_palette(app_state).rendered_text))
    return "\n".join(truncate_to_display_width_v0439(line, width) for line in lines)


def create_v04310_snapshot_request(width: int = 120, plain: bool = False, include_command_palette: bool = False, **overrides: Any) -> V04310SnapshotRequest:
    defaults = {
        "request_id": "v04310-snapshot-request",
        "width": int(width),
        "plain": bool(plain),
        "include_command_palette": bool(include_command_palette),
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310SnapshotRequest(**defaults)


def create_v04310_snapshot_result(rendered_text: str, width: int, mode: str, include_command_palette: bool = False, **overrides: Any) -> V04310SnapshotResult:
    forbidden = any(item.lower() in rendered_text.lower() for item in FORBIDDEN_V04310_DEFAULT_STRINGS)
    defaults = {
        "result_id": "v04310-snapshot-result",
        "rendered_text": rendered_text,
        "width": int(width),
        "mode": mode,
        "line_count": len(rendered_text.splitlines()),
        "all_lines_within_width": assert_v0439_lines_within_width(rendered_text, int(width)),
        "contains_sidebar": "PROJECT" in rendered_text or "Project" in rendered_text,
        "contains_main_panel": "Welcome to Schumpeter" in rendered_text or "Chat" in rendered_text,
        "contains_input_box": "Ask Schumpeter" in rendered_text,
        "contains_status_bar": "PI " in rendered_text and "Provider" in rendered_text and "Trace" in rendered_text,
        "contains_command_palette": bool(include_command_palette and ("Command Palette" in rendered_text or "Commands" in rendered_text)),
        "contains_schumpeter_brand": "Schumpeter" in rendered_text,
        "contains_forbidden_default_strings": forbidden,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "git_executed": False,
        "repo_search_used": False,
        "workspace_read_opened": False,
        "memory_mutated": False,
        "core_memory_written": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310SnapshotResult(**defaults)


def render_v04310_snapshot(
    width: int = 120,
    plain: bool = False,
    include_command_palette: bool = False,
    app_state: V04310TUIAppState | None = None,
) -> V04310SnapshotResult:
    app_state = app_state or create_v04310_tui_app_state()
    if plain:
        text = _render_compact(app_state, int(width), include_command_palette, plain=True)
        mode = "plain"
    elif int(width) < 110:
        text = _render_compact(app_state, int(width), include_command_palette)
        mode = "compact"
    else:
        text = _render_two_column(app_state, int(width), include_command_palette)
        mode = "two_column"
    return create_v04310_snapshot_result(text, width, mode, include_command_palette)


def create_v04310_interactive_smoke_result(**overrides: Any) -> V04310InteractiveSmokeResult:
    app_state = create_v04310_tui_app_state()
    snapshot = render_v04310_snapshot(100, plain=True, app_state=app_state)
    defaults = {
        "result_id": "v04310-interactive-smoke-result",
        "app_initialized": True,
        "structured_snapshot_rendered": snapshot.contains_main_panel and snapshot.contains_input_box,
        "adapter_used_for_submit": True,
        "provider_invoked_by_rendering": False,
        "shell_executed": False,
        "repo_search_used": False,
        "workspace_read_opened": False,
        "memory_mutated_by_rendering": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310InteractiveSmokeResult(**defaults)


def apply_v04310_turn_result(app_state: V04310TUIAppState, turn: V04310TUITurnResult) -> V04310TUIAppState:
    transcript = append_v04310_transcript_message(app_state.transcript, create_v04310_transcript_message(turn.input_text, "user"))
    transcript = append_v04310_transcript_message(transcript, create_v04310_transcript_message(turn.rendered_text, turn.message_kind))
    return create_v04310_tui_app_state(app_state.runtime_snapshot, transcript, exit_requested=turn.route_kind == "exit" or turn.input_text.strip() in {"/exit", "/quit"})


def run_v04310_tui_preview_once(inputs: Sequence[str] = (), adapter: V04310RuntimeAdapter | None = None) -> V04310TUIAppState:
    from chanta_core.schumpeter_tui.turn_dispatch import apply_v04310_dispatch_result, dispatch_v04310_turn

    adapter = adapter or V04310RuntimeAdapter()
    app_state = create_v04310_tui_app_state(adapter.collect_ui_snapshot())
    for raw in inputs:
        result = dispatch_v04310_turn(raw, adapter)
        app_state = apply_v04310_dispatch_result(app_state, result)
        if result.app_should_exit:
            break
    return app_state


def run_v04310_tui_preview(inputs: Sequence[str] = (), adapter: V04310RuntimeAdapter | None = None) -> V04310TUIAppState:
    return run_v04310_tui_preview_once(inputs, adapter)


__all__ = [
    name
    for name in globals()
    if name.startswith("V04310")
    or name.startswith("V04311")
    or name.startswith("FORBIDDEN")
    or name.startswith("create_v04310")
    or name.startswith("detect_v04310")
    or name.startswith("complete_v04310")
    or name.startswith("render_v04310")
    or name.startswith("run_v04310")
    or name.startswith("apply_v04310")
]
