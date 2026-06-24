"""Deterministic Schumpeter TUI snapshot renderer for v0.43.9."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from chanta_core.schumpeter_tui.command_registry import list_v0439_palette_commands
from chanta_core.schumpeter_tui.components.chat_view import render_v0439_chat_view
from chanta_core.schumpeter_tui.components.command_palette import render_v0439_command_palette
from chanta_core.schumpeter_tui.components.input_box import render_v0439_input_box
from chanta_core.schumpeter_tui.components.sidebar import render_v0439_sidebar
from chanta_core.schumpeter_tui.components.status_bar import render_v0439_status_bar
from chanta_core.schumpeter_tui.display_width import (
    assert_v0439_lines_within_width,
    display_width_v0439,
    pad_to_display_width_v0439,
    truncate_to_display_width_v0439,
)
from chanta_core.schumpeter_tui.layout import V0439LayoutMode, create_v0439_layout_frame
from chanta_core.schumpeter_tui.runtime_adapter import collect_v0439_runtime_snapshot
from chanta_core.schumpeter_tui.state import create_v0439_command_palette_state, create_v0439_status_monitor_state, create_v0439_ui_state
from chanta_core.schumpeter_tui.theme import create_v0439_theme_glyphs


class V0439SnapshotRenderMode(StrEnum):
    SNAPSHOT = "snapshot"
    COMPACT = "compact"
    PLAIN = "plain"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V0439SnapshotRequest:
    request_id: str
    width: int
    height: int | None
    plain: bool
    no_color: bool
    no_logo: bool
    fake_data: bool
    include_command_palette: bool
    production_certified: bool


@dataclass(frozen=True)
class V0439SnapshotResult:
    result_id: str
    rendered_text: str
    width: int
    mode: str
    line_count: int
    all_lines_within_width: bool
    contains_sidebar: bool
    contains_main_chat: bool
    contains_input_box: bool
    contains_status_bar: bool
    contains_command_hints: bool
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
class V0439SnapshotGoldenCase:
    case_id: str
    width: int
    plain: bool
    include_command_palette: bool
    expected_contains: tuple[str, ...]
    forbidden_strings: tuple[str, ...]
    production_certified_allowed: bool


@dataclass(frozen=True)
class V0439SnapshotGoldenResult:
    result_id: str
    case: V0439SnapshotGoldenCase
    passed: bool
    rendered_text: str
    missing_expected: tuple[str, ...]
    forbidden_found: tuple[str, ...]
    high_risk_flags_zero: bool
    production_certified: bool


FORBIDDEN_V0439_DEFAULT_STRINGS = (
    "ChantaGrowthKernel",
    "GrowthKernel",
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


def create_v0439_snapshot_request(
    width: int = 120,
    height: int | None = None,
    plain: bool = False,
    no_color: bool = True,
    no_logo: bool = False,
    fake_data: bool = True,
    include_command_palette: bool = False,
    **overrides: Any,
) -> V0439SnapshotRequest:
    defaults = {
        "request_id": "v0439-snapshot-request",
        "width": int(width),
        "height": height,
        "plain": bool(plain),
        "no_color": bool(no_color),
        "no_logo": bool(no_logo),
        "fake_data": bool(fake_data),
        "include_command_palette": bool(include_command_palette),
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0439SnapshotRequest(**defaults)


def _state_for_request(request: V0439SnapshotRequest):
    runtime = collect_v0439_runtime_snapshot()
    commands = list_v0439_palette_commands("/", 12) if request.include_command_palette else ()
    palette = create_v0439_command_palette_state(request.include_command_palette, "/", commands) if request.include_command_palette else None
    return create_v0439_ui_state(
        profile_id=runtime.profile_id,
        provider_label=runtime.provider_label,
        mode_label=runtime.mode_label,
        working_directory_label=runtime.working_directory_label,
        project_label=runtime.project_label,
        session_label=runtime.session_label,
        status_monitor=create_v0439_status_monitor_state(
            runtime.pi_status,
            runtime.provider_status,
            runtime.trace_status,
            runtime.evidence_status,
            runtime.safety_status,
        ),
        command_palette=palette,
        render_mode=V0439SnapshotRenderMode.PLAIN.value if request.plain else V0439SnapshotRenderMode.SNAPSHOT.value,
    )


def _input_box_lines(content_width: int, plain: bool) -> tuple[str, str, str]:
    glyphs = create_v0439_theme_glyphs(plain)
    title = " Input "
    top_fill = max(0, content_width - 2 - display_width_v0439(title) - 1)
    top = f"{glyphs.input_top_left}{glyphs.input_horizontal}{title}{glyphs.input_horizontal * top_fill}{glyphs.input_top_right}"
    middle = f"{glyphs.input_vertical}{pad_to_display_width_v0439(' Ask Schumpeter anything...', content_width - 2)}{glyphs.input_vertical}"
    bottom = f"{glyphs.input_bottom_left}{glyphs.input_horizontal * (content_width - 2)}{glyphs.input_bottom_right}"
    return top, middle, bottom


def _two_column_text(request: V0439SnapshotRequest) -> str:
    state = _state_for_request(request)
    frame = create_v0439_layout_frame(request.width, request.height, request.plain)
    glyphs = create_v0439_theme_glyphs(False)
    left_width = frame.sidebar_width
    right_width = request.width - left_width - 3
    sidebar = list(render_v0439_sidebar(state).rendered_lines)
    chat = list(render_v0439_chat_view(state).rendered_lines)
    input_top, input_mid, input_bottom = _input_box_lines(right_width, False)
    chat.extend((input_top, input_mid, input_bottom, "   ".join(state.command_hints), render_v0439_status_bar(state).rendered_lines[0]))
    if request.include_command_palette:
        chat.extend(("",) + render_v0439_command_palette(state).rendered_lines)
    row_count = max(len(sidebar), len(chat))
    sidebar.extend([""] * (row_count - len(sidebar)))
    chat.extend([""] * (row_count - len(chat)))
    lines = [f"{glyphs.top_left}{glyphs.horizontal * left_width}{glyphs.tee_down}{glyphs.horizontal * right_width}{glyphs.top_right}"]
    for left, right in zip(sidebar, chat, strict=True):
        lines.append(f"{glyphs.vertical}{pad_to_display_width_v0439(left, left_width)}{glyphs.vertical}{pad_to_display_width_v0439(right, right_width)}{glyphs.vertical}")
    lines.append(f"{glyphs.bottom_left}{glyphs.horizontal * left_width}{glyphs.tee_up}{glyphs.horizontal * right_width}{glyphs.bottom_right}")
    return "\n".join(lines)


def render_v0439_snapshot_compact(width: int = 80, include_command_palette: bool = False) -> str:
    request = create_v0439_snapshot_request(width, include_command_palette=include_command_palette)
    state = _state_for_request(request)
    limit = max(40, int(width))
    lines = [
        "Schumpeter",
        "PI-native Work Agent",
        "",
        "Project",
        f"path: {state.working_directory_label}",
        f"mode: {state.mode_label}",
        "",
        "Session",
        f"profile: {state.profile_id}",
        f"provider: {state.provider_label}",
        "",
        "PI Monitor",
        f"PI {state.status_monitor.pi_status} | Provider {state.status_monitor.provider_status} | Trace {state.status_monitor.trace_status}",
        f"Evidence {state.status_monitor.evidence_status} | Safety {state.status_monitor.safety_status}",
        "",
        "Chat",
        "You> 오늘 v0.44 준비 상태를 요약해줘",
        "Schumpeter> 현재 v0.44 진입 전에는 UX gate와 start lobby gate가 우선입니다.",
        "",
        "Input",
        "Ask Schumpeter anything...",
        "   ".join(state.command_hints),
        render_v0439_status_bar(state).rendered_lines[0],
    ]
    if include_command_palette:
        required = ("/summary", "/todo", "/memo", "/decision", "/handoff", "/status", "/exit")
        commands = list_v0439_palette_commands("/", None)
        lines.extend(("", "Command Palette", " ".join(command for command in required if command in commands)))
    return "\n".join(truncate_to_display_width_v0439(line, limit) for line in lines)


def render_v0439_snapshot_plain(width: int = 100, include_command_palette: bool = False) -> str:
    request = create_v0439_snapshot_request(width, plain=True, include_command_palette=include_command_palette)
    state = _state_for_request(request)
    lines = [
        "Schumpeter",
        "Process Intelligence-native Work Agent",
        "",
        "Project",
        f"path: {state.working_directory_label}",
        f"mode: {state.mode_label}",
        "",
        "Session",
        f"profile: {state.profile_id}",
        f"provider: {state.provider_label}",
        "",
        "PI Monitor",
        f"PI {state.status_monitor.pi_status} | Provider {state.status_monitor.provider_status} | Trace {state.status_monitor.trace_status} | Evidence {state.status_monitor.evidence_status} | Safety {state.status_monitor.safety_status}",
        "",
        "Chat",
        "You> 오늘 v0.44 준비 상태를 요약해줘",
        "Schumpeter> 현재 v0.44 진입 전에는 UX gate와 start lobby gate가 우선입니다.",
        "",
        "Input",
        "Ask Schumpeter anything...",
        "",
        "Status",
        render_v0439_status_bar(state).rendered_lines[0],
        "   ".join(state.command_hints),
    ]
    if include_command_palette:
        required = ("/summary", "/todo", "/memo", "/decision", "/handoff", "/status", "/exit")
        commands = list_v0439_palette_commands("/", None)
        lines.extend(("", "Command Palette", " ".join(command for command in required if command in commands)))
    return "\n".join(truncate_to_display_width_v0439(line, int(width)) for line in lines)


def create_v0439_snapshot_result(rendered_text: str, width: int, mode: str, **overrides: Any) -> V0439SnapshotResult:
    forbidden = assert_v0439_no_forbidden_default_strings(rendered_text) is False
    defaults = {
        "result_id": "v0439-snapshot-result",
        "rendered_text": rendered_text,
        "width": int(width),
        "mode": mode,
        "line_count": len(rendered_text.splitlines()),
        "all_lines_within_width": assert_v0439_lines_within_width(rendered_text, int(width)),
        "contains_sidebar": "PROJECT" in rendered_text or "Project" in rendered_text,
        "contains_main_chat": "Schumpeter>" in rendered_text or "Chat" in rendered_text,
        "contains_input_box": "Ask Schumpeter" in rendered_text,
        "contains_status_bar": "PI " in rendered_text and "Provider" in rendered_text and "Trace" in rendered_text,
        "contains_command_hints": "/help" in rendered_text and "/status" in rendered_text and "/exit" in rendered_text,
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
    return V0439SnapshotResult(**defaults)


def render_v0439_snapshot(
    width: int = 120,
    plain: bool = False,
    include_command_palette: bool = False,
    request: V0439SnapshotRequest | None = None,
) -> V0439SnapshotResult:
    request = request or create_v0439_snapshot_request(width=width, plain=plain, include_command_palette=include_command_palette)
    if request.plain:
        text = render_v0439_snapshot_plain(request.width, request.include_command_palette)
        mode = V0439SnapshotRenderMode.PLAIN.value
    elif int(request.width) < 90:
        text = render_v0439_snapshot_compact(request.width, request.include_command_palette)
        mode = V0439SnapshotRenderMode.COMPACT.value
    else:
        text = _two_column_text(request)
        mode = V0439LayoutMode.TWO_COLUMN.value
    return create_v0439_snapshot_result(text, request.width, mode)


def assert_v0439_no_forbidden_default_strings(text: str) -> bool:
    lowered = text.lower()
    return not any(item.lower() in lowered for item in FORBIDDEN_V0439_DEFAULT_STRINGS)


def create_v0439_snapshot_golden_case(
    case_id: str = "width-120",
    width: int = 120,
    plain: bool = False,
    include_command_palette: bool = False,
    expected_contains: tuple[str, ...] = ("Schumpeter", "PROJECT", "SESSION", "PI MONITOR", "You>", "Schumpeter>", "Ask Schumpeter", "/help", "/status", "/exit"),
    forbidden_strings: tuple[str, ...] = FORBIDDEN_V0439_DEFAULT_STRINGS,
    **overrides: Any,
) -> V0439SnapshotGoldenCase:
    defaults = {
        "case_id": case_id,
        "width": int(width),
        "plain": bool(plain),
        "include_command_palette": bool(include_command_palette),
        "expected_contains": expected_contains,
        "forbidden_strings": forbidden_strings,
        "production_certified_allowed": False,
    }
    defaults.update(overrides)
    return V0439SnapshotGoldenCase(**defaults)


def create_v0439_snapshot_golden_result(case: V0439SnapshotGoldenCase, result: V0439SnapshotResult, **overrides: Any) -> V0439SnapshotGoldenResult:
    missing = tuple(item for item in case.expected_contains if item not in result.rendered_text)
    forbidden = tuple(item for item in case.forbidden_strings if item.lower() in result.rendered_text.lower())
    high_risk_zero = not any(
        (
            result.provider_invoked,
            result.prompt_submitted,
            result.shell_executed,
            result.git_executed,
            result.repo_search_used,
            result.workspace_read_opened,
            result.memory_mutated,
            result.core_memory_written,
        )
    )
    defaults = {
        "result_id": "v0439-snapshot-golden-result",
        "case": case,
        "passed": not missing and not forbidden and high_risk_zero and result.all_lines_within_width and not result.production_certified,
        "rendered_text": result.rendered_text,
        "missing_expected": missing,
        "forbidden_found": forbidden,
        "high_risk_flags_zero": high_risk_zero,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0439SnapshotGoldenResult(**defaults)


def execute_v0439_snapshot_golden_case(case: V0439SnapshotGoldenCase) -> V0439SnapshotGoldenResult:
    result = render_v0439_snapshot(case.width, case.plain, case.include_command_palette)
    return create_v0439_snapshot_golden_result(case, result)


__all__ = [name for name in globals() if name.startswith("V0439") or name.startswith("FORBIDDEN") or name.startswith("create_v0439") or name.startswith("render_v0439") or name.startswith("execute_v0439") or name.startswith("assert_v0439")]
