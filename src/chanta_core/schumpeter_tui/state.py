"""Display-only state model for the v0.43.9 Schumpeter TUI contract."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Sequence


class V0439DisplayMessageKind(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    ARTIFACT = "artifact"
    DIAGNOSTIC = "diagnostic"
    STATUS = "status"
    ERROR = "error"
    SYSTEM_NOTICE = "system_notice"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V0439DisplayPart:
    part_id: str
    kind: str
    text: str
    language: str | None
    debug_metadata_visible: bool
    production_certified: bool


@dataclass(frozen=True)
class V0439DisplayMessage:
    message_id: str
    kind: str
    speaker_label: str
    text: str
    parts: tuple[V0439DisplayPart, ...]
    timestamp_label: str | None
    debug_metadata_visible: bool
    production_certified: bool


@dataclass(frozen=True)
class V0439SidebarState:
    product_name: str
    subtitle: str
    project_label: str | None
    working_directory_label: str | None
    mode_label: str
    profile_id: str
    provider_label: str
    command_groups: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V0439MainChatState:
    welcome_title: str
    welcome_subtitle: str
    messages: tuple[V0439DisplayMessage, ...]
    production_certified: bool


@dataclass(frozen=True)
class V0439InputBoxState:
    placeholder: str
    focused: bool
    production_certified: bool


@dataclass(frozen=True)
class V0439StatusBarState:
    pi_status: str
    provider_status: str
    trace_status: str
    evidence_status: str
    safety_status: str
    compact_label: str
    production_certified: bool


@dataclass(frozen=True)
class V0439CommandPaletteState:
    visible: bool
    prefix: str
    commands: tuple[str, ...]
    grouped: bool
    command_executed: bool
    production_certified: bool


@dataclass(frozen=True)
class V0439PIStatusMonitorState:
    pi_status: str
    provider_status: str
    trace_status: str
    evidence_status: str
    safety_status: str
    raw_debug_metadata_visible: bool
    production_certified: bool


@dataclass(frozen=True)
class V0439UIState:
    state_id: str
    product_name: str
    subtitle: str
    profile_id: str
    provider_label: str
    mode_label: str
    working_directory_label: str | None
    project_label: str | None
    session_label: str | None
    status_monitor: V0439PIStatusMonitorState
    messages: tuple[V0439DisplayMessage, ...]
    command_hints: tuple[str, ...]
    command_palette: V0439CommandPaletteState | None
    version_label: str
    render_mode: str
    contains_secret_values: bool
    contains_raw_debug_metadata: bool
    production_certified: bool


def create_v0439_display_part(
    text: str,
    kind: str = "text",
    language: str | None = None,
    **overrides: Any,
) -> V0439DisplayPart:
    defaults = {
        "part_id": "v0439-display-part",
        "kind": kind,
        "text": text,
        "language": language,
        "debug_metadata_visible": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0439DisplayPart(**defaults)


def create_v0439_display_message(
    text: str,
    kind: str = V0439DisplayMessageKind.ASSISTANT.value,
    speaker_label: str | None = None,
    parts: Sequence[V0439DisplayPart] = (),
    **overrides: Any,
) -> V0439DisplayMessage:
    labels = {
        V0439DisplayMessageKind.USER.value: "You>",
        V0439DisplayMessageKind.ASSISTANT.value: "Schumpeter>",
        V0439DisplayMessageKind.ARTIFACT.value: "Artifact>",
        V0439DisplayMessageKind.DIAGNOSTIC.value: "Diagnostic>",
        V0439DisplayMessageKind.STATUS.value: "Status>",
        V0439DisplayMessageKind.ERROR.value: "Error>",
        V0439DisplayMessageKind.SYSTEM_NOTICE.value: "Notice>",
    }
    defaults = {
        "message_id": "v0439-display-message",
        "kind": kind,
        "speaker_label": speaker_label or labels.get(kind, "Schumpeter>"),
        "text": text,
        "parts": tuple(parts),
        "timestamp_label": None,
        "debug_metadata_visible": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0439DisplayMessage(**defaults)


def create_v0439_status_monitor_state(
    pi_status: str = "ok",
    provider_status: str = "ok",
    trace_status: str = "active",
    evidence_status: str = "none",
    safety_status: str = "closed",
    **overrides: Any,
) -> V0439PIStatusMonitorState:
    defaults = {
        "pi_status": pi_status,
        "provider_status": provider_status,
        "trace_status": trace_status,
        "evidence_status": evidence_status,
        "safety_status": safety_status,
        "raw_debug_metadata_visible": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0439PIStatusMonitorState(**defaults)


def create_v0439_command_palette_state(
    visible: bool = False,
    prefix: str = "/",
    commands: Sequence[str] = (),
    **overrides: Any,
) -> V0439CommandPaletteState:
    defaults = {
        "visible": bool(visible),
        "prefix": prefix,
        "commands": tuple(commands),
        "grouped": True,
        "command_executed": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0439CommandPaletteState(**defaults)


def create_v0439_ui_state(
    messages: Sequence[V0439DisplayMessage] | None = None,
    command_palette: V0439CommandPaletteState | None = None,
    render_mode: str = "snapshot",
    **overrides: Any,
) -> V0439UIState:
    default_messages = (
        create_v0439_display_message("오늘 v0.44 준비 상태를 요약해줘", V0439DisplayMessageKind.USER.value),
        create_v0439_display_message(
            "현재 v0.44 진입 전에는 UX gate와 start lobby gate가 우선입니다.",
            V0439DisplayMessageKind.ASSISTANT.value,
        ),
        create_v0439_display_message("handoff: v0.43.10 structured TUI MVP", V0439DisplayMessageKind.ARTIFACT.value),
        create_v0439_display_message("snapshot renderer: no side effects", V0439DisplayMessageKind.STATUS.value),
    )
    defaults = {
        "state_id": "v0439-ui-state",
        "product_name": "Schumpeter",
        "subtitle": "PI-native Work Agent",
        "profile_id": "default-personal",
        "provider_label": "configured",
        "mode_label": "Work Session",
        "working_directory_label": "D:\\...\\ChantaCore",
        "project_label": "Schumpeter v0.43",
        "session_label": "structured TUI contract",
        "status_monitor": create_v0439_status_monitor_state(),
        "messages": tuple(messages) if messages is not None else default_messages,
        "command_hints": ("/help commands", "/status", "/exit"),
        "command_palette": command_palette,
        "version_label": "v0.43.9",
        "render_mode": render_mode,
        "contains_secret_values": False,
        "contains_raw_debug_metadata": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0439UIState(**defaults)


@dataclass(frozen=True)
class V043112SlashPaletteState:
    visible: bool
    query: str
    selected_index: int
    filtered_commands: tuple[str, ...]
    max_visible_items: int
    anchor: str
    input_remains_visible: bool
    command_executed_by_selection: bool
    provider_invoked: bool
    shell_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    memory_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V043112SlashPaletteLayoutPolicy:
    anchor_above_input: bool
    may_cover_input: bool
    reserve_input_line: bool
    reserve_status_line: bool
    max_visible_items: int
    compact_when_narrow: bool
    scroll_when_overflow: bool
    production_certified: bool


@dataclass(frozen=True)
class V043112SlashPaletteSelectionState:
    selected_index: int
    total_items: int
    wrap_selection: bool
    clamp_selection: bool
    production_certified: bool


@dataclass(frozen=True)
class V043112SlashPaletteInputVisibilityPolicy:
    input_text_visible_when_open: bool
    current_query_visible: bool
    cursor_state_preserved: bool
    palette_may_obscure_input: bool
    production_certified: bool


@dataclass(frozen=True)
class V043112SlashPaletteNavigationResult:
    selected_index: int
    moved: bool
    command_executed: bool
    provider_invoked: bool
    shell_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    memory_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V043112SlashPaletteInsertionResult:
    inserted_text: str
    command: str
    requires_argument: bool
    command_executed: bool
    input_remains_visible: bool
    production_certified: bool


def create_v043112_slash_palette_layout_policy(**overrides: Any) -> V043112SlashPaletteLayoutPolicy:
    defaults = {
        "anchor_above_input": True,
        "may_cover_input": False,
        "reserve_input_line": True,
        "reserve_status_line": True,
        "max_visible_items": 10,
        "compact_when_narrow": True,
        "scroll_when_overflow": True,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V043112SlashPaletteLayoutPolicy(**defaults)


def create_v043112_slash_palette_state(
    visible: bool = False,
    query: str = "/",
    selected_index: int = 0,
    filtered_commands: Sequence[str] = (),
    **overrides: Any,
) -> V043112SlashPaletteState:
    policy = create_v043112_slash_palette_layout_policy()
    defaults = {
        "visible": bool(visible),
        "query": query,
        "selected_index": max(0, int(selected_index)),
        "filtered_commands": tuple(filtered_commands),
        "max_visible_items": policy.max_visible_items,
        "anchor": "above_input",
        "input_remains_visible": True,
        "command_executed_by_selection": False,
        "provider_invoked": False,
        "shell_executed": False,
        "repo_search_used": False,
        "workspace_read_opened": False,
        "memory_mutated": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V043112SlashPaletteState(**defaults)


def create_v043112_slash_palette_selection_state(
    selected_index: int = 0,
    total_items: int = 0,
    **overrides: Any,
) -> V043112SlashPaletteSelectionState:
    defaults = {
        "selected_index": max(0, int(selected_index)),
        "total_items": max(0, int(total_items)),
        "wrap_selection": False,
        "clamp_selection": True,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V043112SlashPaletteSelectionState(**defaults)


def create_v043112_slash_palette_input_visibility_policy(**overrides: Any) -> V043112SlashPaletteInputVisibilityPolicy:
    defaults = {
        "input_text_visible_when_open": True,
        "current_query_visible": True,
        "cursor_state_preserved": True,
        "palette_may_obscure_input": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V043112SlashPaletteInputVisibilityPolicy(**defaults)


__all__ = [name for name in globals() if name.startswith("V0439") or name.startswith("V043112") or name.startswith("create_v0439") or name.startswith("create_v043112")]
