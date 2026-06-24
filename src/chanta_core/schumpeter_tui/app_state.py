"""v0.43.10 Schumpeter structured TUI app state."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Sequence

from chanta_core.schumpeter_tui.runtime_adapter import V04310RuntimeSnapshot, collect_v04310_runtime_snapshot


class V04310TUIEngine(StrEnum):
    PROMPT_TOOLKIT = "prompt_toolkit"
    PLAIN_FALLBACK = "plain_fallback"
    SNAPSHOT = "snapshot"
    UNKNOWN = "unknown"


class V04310TranscriptMessageKind(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    ARTIFACT = "artifact"
    DIAGNOSTIC = "diagnostic"
    STATUS = "status"
    ERROR = "error"
    SYSTEM_NOTICE = "system_notice"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V04310TranscriptPart:
    part_id: str
    kind: str
    text: str
    language: str | None
    debug_metadata_visible: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310TranscriptMessage:
    message_id: str
    kind: str
    speaker_label: str
    text: str
    parts: tuple[V04310TranscriptPart, ...]
    debug_metadata_visible: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310SidebarState:
    product_name: str
    subtitle: str
    project_label: str
    session_label: str
    profile_id: str
    provider_label: str
    mode_label: str
    pi_status: str
    provider_status: str
    trace_status: str
    evidence_status: str
    safety_status: str
    command_shortcuts: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V04310MainPanelState:
    welcome_title: str
    welcome_subtitle: str
    transcript: tuple[V04310TranscriptMessage, ...]
    production_certified: bool


@dataclass(frozen=True)
class V04310InputState:
    placeholder: str
    current_text: str
    multiline_supported: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310PaletteState:
    visible: bool
    prefix: str
    commands: tuple[str, ...]
    command_executed: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310StatusLineState:
    compact_text: str
    pi_status: str
    provider_status: str
    trace_status: str
    evidence_status: str
    safety_status: str
    version_label: str
    production_certified: bool


@dataclass(frozen=True)
class V04310TUIAppState:
    state_id: str
    runtime_snapshot: V04310RuntimeSnapshot
    transcript: tuple[V04310TranscriptMessage, ...]
    sidebar: V04310SidebarState
    main_panel: V04310MainPanelState
    input_state: V04310InputState
    palette_state: V04310PaletteState
    status_line: V04310StatusLineState
    busy: bool
    exit_requested: bool
    contains_secret_values: bool
    contains_raw_debug_metadata: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310TUITurnResult:
    result_id: str
    input_text: str
    route_kind: str
    rendered_text: str
    message_kind: str
    run_id: str | None
    session_id: str | None
    response_parse_status: str | None
    response_error_class: str | None
    provider_model: str | None
    assistant_response_preview: str | None
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
    core_memory_written: bool
    production_certified: bool


def create_v04310_transcript_part(text: str, kind: str = "text", language: str | None = None, **overrides: Any) -> V04310TranscriptPart:
    defaults = {
        "part_id": "v04310-transcript-part",
        "kind": kind,
        "text": text,
        "language": language,
        "debug_metadata_visible": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310TranscriptPart(**defaults)


def create_v04310_transcript_message(
    text: str,
    kind: str = V04310TranscriptMessageKind.ASSISTANT.value,
    speaker_label: str | None = None,
    parts: Sequence[V04310TranscriptPart] = (),
    **overrides: Any,
) -> V04310TranscriptMessage:
    labels = {
        V04310TranscriptMessageKind.USER.value: "You>",
        V04310TranscriptMessageKind.ASSISTANT.value: "Schumpeter>",
        V04310TranscriptMessageKind.ARTIFACT.value: "Artifact>",
        V04310TranscriptMessageKind.DIAGNOSTIC.value: "Diagnostic>",
        V04310TranscriptMessageKind.STATUS.value: "Status>",
        V04310TranscriptMessageKind.ERROR.value: "Error>",
        V04310TranscriptMessageKind.SYSTEM_NOTICE.value: "Notice>",
    }
    defaults = {
        "message_id": "v04310-transcript-message",
        "kind": kind,
        "speaker_label": speaker_label or labels.get(kind, "Schumpeter>"),
        "text": text,
        "parts": tuple(parts),
        "debug_metadata_visible": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310TranscriptMessage(**defaults)


def append_v04310_transcript_message(
    transcript: Sequence[V04310TranscriptMessage],
    message: V04310TranscriptMessage,
) -> tuple[V04310TranscriptMessage, ...]:
    return tuple(transcript) + (message,)


def create_v04310_sidebar_state(snapshot: V04310RuntimeSnapshot | None = None, **overrides: Any) -> V04310SidebarState:
    snapshot = snapshot or collect_v04310_runtime_snapshot()
    defaults = {
        "product_name": snapshot.product_name,
        "subtitle": "Process Intelligence-native Work Agent",
        "project_label": "Schumpeter v0.43",
        "session_label": snapshot.session_label or "structured TUI MVP",
        "profile_id": snapshot.profile_id,
        "provider_label": snapshot.provider_label,
        "mode_label": snapshot.mode_label,
        "pi_status": snapshot.pi_status,
        "provider_status": snapshot.provider_status,
        "trace_status": snapshot.trace_status,
        "evidence_status": snapshot.evidence_status,
        "safety_status": snapshot.safety_status,
        "command_shortcuts": ("/help commands", "/status", "/exit"),
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310SidebarState(**defaults)


def create_v04310_main_panel_state(
    transcript: Sequence[V04310TranscriptMessage] = (),
    **overrides: Any,
) -> V04310MainPanelState:
    defaults = {
        "welcome_title": "Welcome to Schumpeter",
        "welcome_subtitle": "Type /help for commands or start with a work request.",
        "transcript": tuple(transcript),
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310MainPanelState(**defaults)


def create_v04310_input_state(current_text: str = "", **overrides: Any) -> V04310InputState:
    defaults = {
        "placeholder": "Ask Schumpeter anything...",
        "current_text": current_text,
        "multiline_supported": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310InputState(**defaults)


def create_v04310_palette_state(visible: bool = False, prefix: str = "/", commands: Sequence[str] = (), **overrides: Any) -> V04310PaletteState:
    defaults = {
        "visible": bool(visible),
        "prefix": prefix,
        "commands": tuple(commands),
        "command_executed": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310PaletteState(**defaults)


def create_v04310_status_line_state(snapshot: V04310RuntimeSnapshot | None = None, **overrides: Any) -> V04310StatusLineState:
    snapshot = snapshot or collect_v04310_runtime_snapshot()
    compact = f"PI {snapshot.pi_status} | Provider {snapshot.provider_status} | Trace {snapshot.trace_status} | Evidence {snapshot.evidence_status} | Safety {snapshot.safety_status} | v0.43.11"
    defaults = {
        "compact_text": compact,
        "pi_status": snapshot.pi_status,
        "provider_status": snapshot.provider_status,
        "trace_status": snapshot.trace_status,
        "evidence_status": snapshot.evidence_status,
        "safety_status": snapshot.safety_status,
        "version_label": "v0.43.11",
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310StatusLineState(**defaults)


def create_v04310_tui_turn_result(
    input_text: str = "",
    route_kind: str = "conversation",
    rendered_text: str = "",
    message_kind: str = V04310TranscriptMessageKind.ASSISTANT.value,
    **overrides: Any,
) -> V04310TUITurnResult:
    defaults = {
        "result_id": "v04310-tui-turn-result",
        "input_text": input_text,
        "route_kind": route_kind,
        "rendered_text": rendered_text,
        "message_kind": message_kind,
        "run_id": None,
        "session_id": None,
        "response_parse_status": None,
        "response_error_class": None,
        "provider_model": None,
        "assistant_response_preview": None,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "git_executed": False,
        "repo_search_used": False,
        "workspace_read_opened": False,
        "tool_calling_used": False,
        "function_calling_used": False,
        "subagent_invoked": False,
        "memory_mutated": False,
        "core_memory_written": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310TUITurnResult(**defaults)


def create_v04310_tui_app_state(
    runtime_snapshot: V04310RuntimeSnapshot | None = None,
    transcript: Sequence[V04310TranscriptMessage] = (),
    input_text: str = "",
    palette_visible: bool = False,
    exit_requested: bool = False,
    **overrides: Any,
) -> V04310TUIAppState:
    runtime_snapshot = runtime_snapshot or collect_v04310_runtime_snapshot()
    transcript_tuple = tuple(transcript) or (
        create_v04310_transcript_message(
            "Welcome to Schumpeter.\n일반 문장을 입력하거나 /help로 업무 명령을 확인하세요.",
            V04310TranscriptMessageKind.SYSTEM_NOTICE.value,
        ),
    )
    sidebar = create_v04310_sidebar_state(runtime_snapshot)
    main = create_v04310_main_panel_state(transcript_tuple)
    input_state = create_v04310_input_state(input_text)
    palette = create_v04310_palette_state(palette_visible)
    status_line = create_v04310_status_line_state(runtime_snapshot)
    defaults = {
        "state_id": "v04310-tui-app-state",
        "runtime_snapshot": runtime_snapshot,
        "transcript": transcript_tuple,
        "sidebar": sidebar,
        "main_panel": main,
        "input_state": input_state,
        "palette_state": palette,
        "status_line": status_line,
        "busy": False,
        "exit_requested": bool(exit_requested),
        "contains_secret_values": False,
        "contains_raw_debug_metadata": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310TUIAppState(**defaults)


__all__ = [name for name in globals() if name.startswith("V04310") or name.startswith("create_v04310") or name.startswith("append_v04310")]
