"""Turn dispatch contract for v0.43.10.1 no-repeat-chrome repair."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from chanta_core.schumpeter_tui.app_state import (
    V04310TUIAppState,
    V04310TUITurnResult,
    append_v04310_transcript_message,
    create_v04310_tui_app_state,
    create_v04310_transcript_message,
)
from chanta_core.schumpeter_tui.runtime_adapter import V04310RuntimeAdapter


@dataclass(frozen=True)
class V04310PlainFallbackRenderPolicy:
    policy_id: str
    print_static_header_once: bool
    render_turns_with_turn_renderer: bool
    append_full_snapshot_after_each_turn: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310FrameRedrawPolicy:
    policy_id: str
    snapshot_renderer_allowed_for_snapshot: bool
    snapshot_renderer_allowed_for_fullscreen_replace: bool
    snapshot_renderer_allowed_for_plain_turn_append: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310NoRepeatChromePolicy:
    policy_id: str
    print_static_header_once_in_plain_mode: bool
    do_not_append_full_frame_after_each_turn: bool
    snapshot_renderer_used_only_for_snapshot_or_fullscreen_replace: bool
    turn_renderer_used_for_plain_interactive_turns: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310TurnDispatchResult:
    result_id: str
    input_text: str
    route_kind: str
    message_kind: str
    rendered_text: str
    run_id: str | None
    session_id: str | None
    response_parse_status: str | None
    response_error_class: str | None
    provider_model: str | None
    assistant_response_preview: str | None
    app_should_exit: bool
    append_to_transcript: bool
    rerender_full_static_chrome: bool
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    git_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    tool_calling_used: bool
    function_calling_used: bool
    subagent_invoked: bool
    memory_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310InteractionGoldenCase:
    case_id: str
    inputs: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V04310InteractionGoldenResult:
    result_id: str
    rendered_text: str
    schumpeter_header_count: int
    project_section_count: int
    session_section_count: int
    pi_monitor_count: int
    notice_count: int
    no_repeated_static_chrome: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310LoopRepairReport:
    report_id: str
    no_repeat_chrome_policy_ready: bool
    transcript_state_ready: bool
    turn_renderer_ready: bool
    snapshot_interactive_separated: bool
    production_certified: bool


@dataclass(frozen=True)
class V043102TUICommandRoute:
    command: str
    route_kind: str
    message_kind: str
    renderer_kind: str
    debug_surface: bool
    rerender_full_static_chrome: bool
    production_certified: bool


ARTIFACT_COMMAND_KINDS = {
    "summary",
    "todo",
    "memo",
    "decision",
    "handoff",
    "grounded_summary",
    "grounded_todo",
    "grounded_memo",
    "grounded_decision",
    "grounded_handoff",
    "artifact_last",
    "revise",
    "clarify",
}

DIAGNOSTIC_COMMAND_KINDS = {
    "what_happened",
    "report",
    "pilot_status",
    "pilot_review",
    "pilot_score",
    "pilot_findings",
    "pilot_next",
    "pilot_report",
    "workflow_score",
    "polish_status",
    "polish_findings",
    "polish_report",
    "pilot_close",
    "v044_readiness",
    "v044_scope",
    "v044_risks",
    "v044_handoff",
    "evidence",
    "evidence_sources",
    "evidence_last",
    "evidence_explain",
    "evidence_used",
    "grounding_check",
}

STATUS_COMMAND_KINDS = {
    "status",
    "help",
    "about",
    "provider",
    "history",
    "trace",
    "capabilities",
    "memory_boundary",
    "context",
    "recall",
}


def create_v043102_tui_command_route(
    command: str,
    route_kind: str,
    message_kind: str,
    renderer_kind: str,
    debug_surface: bool = False,
    **overrides: Any,
) -> V043102TUICommandRoute:
    defaults = {
        "command": command,
        "route_kind": route_kind,
        "message_kind": message_kind,
        "renderer_kind": renderer_kind,
        "debug_surface": bool(debug_surface),
        "rerender_full_static_chrome": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V043102TUICommandRoute(**defaults)


def create_v043102_tui_command_routes() -> tuple[V043102TUICommandRoute, ...]:
    return (
        create_v043102_tui_command_route("/help", "slash_command", "status", "help"),
        create_v043102_tui_command_route("/help commands", "slash_command", "status", "help"),
        create_v043102_tui_command_route("/status", "slash_command", "status", "status"),
        create_v043102_tui_command_route("/status --debug", "slash_command", "status", "debug_status", True),
        create_v043102_tui_command_route("/summary", "slash_command", "artifact", "artifact"),
        create_v043102_tui_command_route("/todo", "slash_command", "artifact", "artifact"),
        create_v043102_tui_command_route("/memo", "slash_command", "artifact", "artifact"),
        create_v043102_tui_command_route("/decision", "slash_command", "artifact", "artifact"),
        create_v043102_tui_command_route("/handoff", "slash_command", "artifact", "artifact"),
        create_v043102_tui_command_route("/what-happened", "slash_command", "diagnostic", "diagnostic"),
        create_v043102_tui_command_route("/what-happened --debug", "slash_command", "diagnostic", "debug_diagnostic", True),
        create_v043102_tui_command_route("/lobby", "slash_command", "status", "lobby"),
        create_v043102_tui_command_route("/exit", "exit", "assistant", "message"),
        create_v043102_tui_command_route("/quit", "exit", "assistant", "message"),
    )


def resolve_v043102_tui_command_route(input_text: str) -> V043102TUICommandRoute | None:
    raw = " ".join(input_text.strip().split())
    lowered = raw.lower()
    if not lowered.startswith("/"):
        return None
    routes = {route.command: route for route in create_v043102_tui_command_routes()}
    if lowered in routes:
        return routes[lowered]
    if lowered.startswith("/summary "):
        return routes["/summary"]
    if lowered.startswith("/todo "):
        return routes["/todo"]
    if lowered.startswith("/memo "):
        return routes["/memo"]
    if lowered.startswith("/decision "):
        return routes["/decision"]
    if lowered.startswith("/handoff "):
        return routes["/handoff"]
    if lowered.startswith("/what-happened --debug"):
        return routes["/what-happened --debug"]
    if lowered.startswith("/what-happened"):
        return routes["/what-happened"]
    if lowered.startswith("/help"):
        return routes["/help"]
    if lowered.startswith("/status --debug"):
        return routes["/status --debug"]
    if lowered.startswith("/status"):
        return routes["/status"]
    if lowered.startswith("/lobby"):
        return routes["/lobby"]
    return None


def create_v04310_plain_fallback_render_policy(**overrides: Any) -> V04310PlainFallbackRenderPolicy:
    defaults = {
        "policy_id": "v04310-plain-fallback-render-policy",
        "print_static_header_once": True,
        "render_turns_with_turn_renderer": True,
        "append_full_snapshot_after_each_turn": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310PlainFallbackRenderPolicy(**defaults)


def create_v04310_frame_redraw_policy(**overrides: Any) -> V04310FrameRedrawPolicy:
    defaults = {
        "policy_id": "v04310-frame-redraw-policy",
        "snapshot_renderer_allowed_for_snapshot": True,
        "snapshot_renderer_allowed_for_fullscreen_replace": True,
        "snapshot_renderer_allowed_for_plain_turn_append": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310FrameRedrawPolicy(**defaults)


def create_v04310_no_repeat_chrome_policy(**overrides: Any) -> V04310NoRepeatChromePolicy:
    defaults = {
        "policy_id": "v04310-no-repeat-chrome-policy",
        "print_static_header_once_in_plain_mode": True,
        "do_not_append_full_frame_after_each_turn": True,
        "snapshot_renderer_used_only_for_snapshot_or_fullscreen_replace": True,
        "turn_renderer_used_for_plain_interactive_turns": True,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310NoRepeatChromePolicy(**defaults)


def classify_v04310_turn_message_kind(command_kind: str, input_text: str = "") -> str:
    normalized = command_kind.strip().lower()
    raw = input_text.strip().lower()
    if normalized == "exit" or raw in {"/exit", "/quit"}:
        return "assistant"
    if normalized in ARTIFACT_COMMAND_KINDS:
        return "artifact"
    if normalized in DIAGNOSTIC_COMMAND_KINDS:
        return "diagnostic"
    if normalized in STATUS_COMMAND_KINDS:
        return "status"
    return "assistant"


def create_v04310_turn_dispatch_result(
    turn: V04310TUITurnResult,
    app_should_exit: bool = False,
    append_to_transcript: bool = True,
    **overrides: Any,
) -> V04310TurnDispatchResult:
    defaults = {
        "result_id": "v04310-turn-dispatch-result",
        "input_text": turn.input_text,
        "route_kind": "exit" if app_should_exit else turn.route_kind,
        "message_kind": turn.message_kind,
        "rendered_text": turn.rendered_text,
        "run_id": turn.run_id,
        "session_id": turn.session_id,
        "response_parse_status": turn.response_parse_status,
        "response_error_class": turn.response_error_class,
        "provider_model": turn.provider_model,
        "assistant_response_preview": turn.assistant_response_preview,
        "app_should_exit": bool(app_should_exit),
        "append_to_transcript": bool(append_to_transcript),
        "rerender_full_static_chrome": False,
        "provider_invoked": turn.provider_invoked,
        "prompt_submitted": turn.prompt_submitted,
        "shell_executed": turn.shell_executed,
        "git_executed": turn.git_executed,
        "repo_search_used": turn.repo_search_used,
        "workspace_read_opened": turn.workspace_read_opened,
        "tool_calling_used": turn.tool_calling_used,
        "function_calling_used": turn.function_calling_used,
        "subagent_invoked": turn.subagent_invoked,
        "memory_mutated": turn.memory_mutated,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310TurnDispatchResult(**defaults)


def dispatch_v04310_turn(
    input_text: str,
    adapter: V04310RuntimeAdapter,
) -> V04310TurnDispatchResult:
    raw = input_text.strip()
    turn = adapter.execute_slash_command(input_text) if raw.startswith("/") else adapter.submit_user_input(input_text)
    app_should_exit = raw in {"/exit", "/quit"} or turn.route_kind == "exit"
    return create_v04310_turn_dispatch_result(turn, app_should_exit=app_should_exit)


def apply_v04310_dispatch_result(
    app_state: V04310TUIAppState,
    result: V04310TurnDispatchResult,
) -> V04310TUIAppState:
    transcript = app_state.transcript
    if result.append_to_transcript:
        transcript = append_v04310_transcript_message(transcript, create_v04310_transcript_message(result.input_text, "user"))
        transcript = append_v04310_transcript_message(
            transcript,
            create_v04310_transcript_message(result.rendered_text, result.message_kind),
        )
    return create_v04310_tui_app_state(
        app_state.runtime_snapshot,
        transcript,
        exit_requested=result.app_should_exit,
    )


def create_v04310_interaction_golden_case(
    inputs: Sequence[str] = (
        "/status",
        "오늘 작업 계획 정리해줘",
        "/summary 오늘 Schumpeter TUI를 테스트하고 있어.",
        "/what-happened",
        "/exit",
    ),
    **overrides: Any,
) -> V04310InteractionGoldenCase:
    defaults = {
        "case_id": "v04310-interaction-golden-case",
        "inputs": tuple(inputs),
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310InteractionGoldenCase(**defaults)


def create_v04310_interaction_golden_result(rendered_text: str, **overrides: Any) -> V04310InteractionGoldenResult:
    schumpeter_header_count = rendered_text.count("Schumpeter\nProcess Intelligence-native Work Agent")
    project_section_count = rendered_text.count("Project\npath:")
    session_section_count = rendered_text.count("Session\nprofile:")
    pi_monitor_count = rendered_text.count("PI Monitor")
    notice_count = rendered_text.count("Notice> ")
    defaults = {
        "result_id": "v04310-interaction-golden-result",
        "rendered_text": rendered_text,
        "schumpeter_header_count": schumpeter_header_count,
        "project_section_count": project_section_count,
        "session_section_count": session_section_count,
        "pi_monitor_count": pi_monitor_count,
        "notice_count": notice_count,
        "no_repeated_static_chrome": all(
            value <= 1
            for value in (
                schumpeter_header_count,
                project_section_count,
                session_section_count,
                pi_monitor_count,
                notice_count,
            )
        ),
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310InteractionGoldenResult(**defaults)


def create_v04310_loop_repair_report(**overrides: Any) -> V04310LoopRepairReport:
    defaults = {
        "report_id": "v04310-loop-repair-report",
        "no_repeat_chrome_policy_ready": True,
        "transcript_state_ready": True,
        "turn_renderer_ready": True,
        "snapshot_interactive_separated": True,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310LoopRepairReport(**defaults)


__all__ = [name for name in globals() if name.startswith("V04310") or name.startswith("create_v04310") or name.startswith("classify_v04310") or name.startswith("dispatch_v04310") or name.startswith("apply_v04310")]
