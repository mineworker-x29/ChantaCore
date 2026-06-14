"""v0.42.4 interactive manual chat shell support.

This module opens a manual UI loop only. It does not implement an agent loop,
retry loop, tool calling, function calling, shell execution, subagents, file
edit/apply, or production certification.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass, is_dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

from chanta_core.personal_runtime.default_personal_cli_bootstrap import PROFILE_ID
from chanta_core.personal_runtime.default_personal_home_quickstart import (
    create_v042_home_resolution_request,
    resolve_v042_home,
)
from chanta_core.personal_runtime.default_personal_provider_setup import (
    create_v042_provider_status_report,
    create_v042_provider_status_request,
)
from chanta_core.personal_runtime.default_personal_trace_history import (
    create_v042_run_history_request,
    create_v042_run_history_result,
    create_v042_run_show_request,
    create_v042_run_show_result,
    create_v042_session_show_request,
    create_v042_session_show_result,
    create_v042_trace_timeline_request,
    create_v042_trace_timeline_result,
    main as _v0423_main,
)
from chanta_core.personal_runtime.default_personal_trace_report import (
    build_unsafe_command_patterns,
    create_last_run_report,
    create_last_run_report_request,
)


V0424_VERSION = "v0.42.4"
V0424_RELEASE_NAME = "v0.42.4 Interactive Manual Chat Shell"
V042_TRACK_NAME = "v0.42 Default Personal Runtime UX Hardening Track"
INTEGRATED_DOC_PATH = "docs/versions/v0.42/v0.42.4_interactive_manual_chat_shell_restore.md"


class V042ChatShellMode(StrEnum):
    INTERACTIVE = "interactive"
    SCRIPTED_TEST = "scripted_test"
    DRY_RUN = "dry_run"
    UNKNOWN = "unknown"


class V042ChatShellStatus(StrEnum):
    STARTED = "started"
    WAITING_FOR_INPUT = "waiting_for_input"
    TURN_COMPLETED = "turn_completed"
    INTERNAL_COMMAND_COMPLETED = "internal_command_completed"
    DENIED = "denied"
    EXITED = "exited"
    FAILED = "failed"
    BLOCKED = "blocked"


class V042ChatShellInputKind(StrEnum):
    USER_MESSAGE = "user_message"
    INTERNAL_COMMAND = "internal_command"
    EMPTY = "empty"
    EXIT = "exit"
    UNSAFE_COMMAND_LIKE_TEXT = "unsafe_command_like_text"
    UNKNOWN = "unknown"


class V042ChatShellInternalCommandKind(StrEnum):
    HELP = "help"
    EXIT = "exit"
    QUIT = "quit"
    STATUS = "status"
    PROVIDER = "provider"
    HISTORY = "history"
    TRACE = "trace"
    RUN_LAST = "run_last"
    SESSION = "session"
    HANDOFF = "handoff"
    SAFETY = "safety"
    UNKNOWN = "unknown"


class V042ChatShellProviderMode(StrEnum):
    MOCK = "mock"
    CONFIGURED = "configured"
    AUTO = "auto"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V042ChatShellConfig:
    config_id: str
    profile_id: str
    home_path: str | None
    provider_mode: str
    session_id: str | None
    new_session: bool
    max_turns: int | None
    banner_enabled: bool
    internal_commands_enabled: bool
    default_prompt_label: str
    use_default_home_resolver: bool
    allow_real_provider: bool
    allow_mock_provider: bool


@dataclass(frozen=True)
class V042ChatShellStartRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    provider: str | None
    session_id: str | None
    new_session: bool
    max_turns: int | None
    mode: str


@dataclass(frozen=True)
class V042ChatShellSessionState:
    state_id: str
    profile_id: str
    resolved_home_path: str
    session_id: str
    provider_mode: str
    turn_count: int
    run_ids: tuple[str, ...]
    started_at: str
    last_run_id: str | None
    last_assistant_preview: str | None
    exited: bool
    exit_reason: str | None


@dataclass(frozen=True)
class V042ChatShellLoopPolicy:
    policy_id: str
    ui_loop_allowed: bool
    agent_loop_allowed: bool
    autonomous_continuation_allowed: bool
    retry_loop_allowed: bool
    one_run_per_user_message: bool
    internal_commands_call_provider: bool
    internal_commands_mutate_files: bool
    shell_execution_allowed: bool
    subagent_allowed: bool
    tool_calling_allowed: bool
    function_calling_allowed: bool
    production_certified: bool


@dataclass(frozen=True)
class V042ChatShellPromptView:
    view_id: str
    prompt_text: str
    profile_id: str
    session_id: str
    provider_mode: str
    turn_count: int


@dataclass(frozen=True)
class V042ChatShellInputRecord:
    input_id: str
    raw_text: str
    input_kind: str
    normalized_text: str
    created_at: str
    unsafe_pattern_detected: bool
    internal_command_kind: str | None


@dataclass(frozen=True)
class V042ChatShellInternalCommand:
    command_id: str
    command_kind: str
    raw_text: str
    description: str
    provider_call_allowed: bool
    prompt_submission_allowed: bool
    mutates_filesystem: bool
    exits_shell: bool


@dataclass(frozen=True)
class V042ChatShellInternalCommandResult:
    result_id: str
    command_kind: str
    status: str
    rendered_text: str
    exit_requested: bool
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    mutated_filesystem: bool
    production_certified: bool


@dataclass(frozen=True)
class V042ChatShellTurnRequest:
    request_id: str
    profile_id: str
    home_path: str
    session_id: str
    provider: str | None
    user_input: str
    turn_index: int


@dataclass(frozen=True)
class V042ChatShellTurnResult:
    result_id: str
    request_id: str
    status: str
    run_id: str | None
    session_id: str
    assistant_text: str | None
    rendered_text: str
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    skill_executed: bool
    subagent_invoked: bool
    autonomous_continuation_started: bool
    retry_loop_started: bool
    production_certified: bool


@dataclass(frozen=True)
class V042ChatShellRunInvocationRecord:
    record_id: str
    turn_index: int
    user_input_preview: str
    run_id: str | None
    session_id: str
    provider_mode: str
    invoked_existing_run_path: bool
    scoped_single_turn: bool
    tool_calling_used: bool
    function_calling_used: bool
    shell_executed: bool
    subagent_invoked: bool


@dataclass(frozen=True)
class V042ChatShellExitDecision:
    decision_id: str
    exit_requested: bool
    reason: str
    command_kind: str | None
    graceful: bool


@dataclass(frozen=True)
class V042ChatShellSummary:
    summary_id: str
    profile_id: str
    home_path: str
    session_id: str
    provider_mode: str
    total_inputs: int
    user_message_count: int
    internal_command_count: int
    run_count: int
    denial_count: int
    shell_execution_count: int
    skill_execution_count: int
    subagent_invocation_count: int
    production_certification_count: int
    run_ids: tuple[str, ...]
    exited_gracefully: bool


@dataclass(frozen=True)
class V042ChatShellHelpView:
    view_id: str
    rendered_text: str
    commands: tuple[str, ...]
    safety_statement: str


@dataclass(frozen=True)
class V042ChatShellStatusView:
    view_id: str
    profile_id: str
    home_path: str
    session_id: str
    provider_mode: str
    turn_count: int
    latest_run_id: str | None
    high_risk_capabilities_closed: bool
    rendered_text: str


@dataclass(frozen=True)
class V042ChatShellProviderView:
    view_id: str
    rendered_text: str
    provider_invoked: bool
    secret_values_redacted: bool


@dataclass(frozen=True)
class V042ChatShellHistoryView:
    view_id: str
    rendered_text: str
    provider_invoked: bool


@dataclass(frozen=True)
class V042ChatShellTraceView:
    view_id: str
    rendered_text: str
    provider_invoked: bool
    mutated_filesystem: bool


@dataclass(frozen=True)
class V042ChatShellSessionView:
    view_id: str
    rendered_text: str
    provider_invoked: bool
    provider_text_untrusted: bool


@dataclass(frozen=True)
class V042ChatShellDebugHandoff:
    handoff_id: str
    profile_id: str
    home_path: str
    session_id: str
    run_ids: tuple[str, ...]
    provider_mode: str
    total_turns: int
    safety_counts_summary: str
    concise_text: str
    includes_secret_values: bool
    suitable_for_gpt_or_codex: bool


@dataclass(frozen=True)
class V042ChatShellRenderPolicy:
    policy_id: str
    show_banner: bool
    show_prompt: bool
    show_session_id: bool
    show_run_id_after_turn: bool
    show_provider_mode: bool
    mark_provider_text_untrusted: bool
    show_safety_footer: bool
    redact_secrets: bool


@dataclass(frozen=True)
class V042ChatShellSafetyReport:
    report_id: str
    ui_loop_opened: bool
    agent_loop_opened: bool
    autonomous_continuation_allowed: bool
    retry_loop_allowed: bool
    provider_doctor_completion_allowed: bool
    provider_tool_calling_allowed: bool
    function_calling_allowed: bool
    shell_execution_allowed: bool
    file_edit_allowed: bool
    patch_apply_allowed: bool
    subagent_invocation_allowed: bool
    read_only_skill_execution_as_actions_allowed: bool
    production_certified: bool


@dataclass(frozen=True)
class V042ChatShellScriptedRunResult:
    result_id: str
    inputs_processed: int
    outputs: tuple[str, ...]
    summary: V042ChatShellSummary
    turn_results: tuple[V042ChatShellTurnResult, ...]
    internal_command_results: tuple[V042ChatShellInternalCommandResult, ...]
    exited: bool
    provider_invoked_count: int
    prompt_submitted_count: int
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V0424ReadinessReport:
    chat_command_ready: bool
    manual_ui_loop_ready: bool
    one_run_per_user_message_ready: bool
    internal_help_command_ready: bool
    internal_exit_command_ready: bool
    internal_status_command_ready: bool
    internal_provider_command_ready: bool
    internal_history_command_ready: bool
    internal_trace_command_ready: bool
    internal_session_command_ready: bool
    internal_handoff_command_ready: bool
    chat_shell_scripted_test_helper_ready: bool
    chat_shell_safety_report_ready: bool
    integrated_restore_document_ready: bool
    v0425_handoff_ready: bool
    ready_for_autonomous_agent_loop: bool
    ready_for_general_agent_loop: bool
    ready_for_multi_step_agent_loop: bool
    ready_for_retry_loop: bool
    ready_for_provider_doctor_completion: bool
    ready_for_provider_tool_calling: bool
    ready_for_function_calling: bool
    ready_for_read_only_skill_execution_as_actions: bool
    ready_for_shell_execution: bool
    ready_for_file_edit: bool
    ready_for_patch_apply: bool
    ready_for_subagent_invocation: bool
    ready_for_child_session_creation: bool
    ready_for_autonomous_retry_loop: bool
    ready_for_dominion_runtime: bool
    production_certified: bool


@dataclass(frozen=True)
class V0425BoundedReadOnlySkillExecutionHandoff:
    target_version: str
    recommended_focus: tuple[str, ...]
    must_not_open: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V0424IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool


@dataclass(frozen=True)
class V0424IntegratedRestoreContextSnapshot:
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]


@dataclass(frozen=True)
class V0424IntegratedRestorePacket:
    packet_id: str
    context_snapshot: V0424IntegratedRestoreContextSnapshot
    sections: tuple[V0424IntegratedRestoreSection, ...]
    single_integrated_doc_path: str
    separate_restore_doc_created: bool


@dataclass(frozen=True)
class V0424IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_required: bool
    separate_restore_doc_allowed: bool
    separate_restore_doc_created: bool
    copy_paste_restore_prompt_required: bool
    suitable_for_new_session_handoff: bool
    required_sections: tuple[str, ...]


def _merge(defaults: Mapping[str, Any], overrides: Mapping[str, Any]) -> dict[str, Any]:
    data = dict(defaults)
    data.update(overrides)
    return data


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _new_id(prefix: str) -> str:
    return f"{prefix}-{datetime.now(UTC).strftime('%Y%m%dT%H%M%S')}"


def _preview(text: str, limit: int = 120) -> str:
    normalized = " ".join(text.split())
    return normalized if len(normalized) <= limit else normalized[: limit - 3] + "..."


def _render_json(value: Any) -> str:
    def convert(item: Any) -> Any:
        if is_dataclass(item):
            return {key: convert(val) for key, val in asdict(item).items()}
        if isinstance(item, tuple):
            return [convert(val) for val in item]
        return item

    return json.dumps(convert(value), indent=2, sort_keys=True)


def _resolve_home(home_path: str | None, command_name: str = "chat") -> str:
    request = create_v042_home_resolution_request(
        explicit_home=home_path,
        command_name=command_name,
        allow_create=False,
        cwd=os.getcwd(),
    )
    resolved = resolve_v042_home(request)
    return resolved.home_path or ""


def _session_id(explicit: str | None = None) -> str:
    return explicit or f"chat-{datetime.now(UTC).strftime('%Y%m%dT%H%M%S')}"


def create_v042_chat_shell_config(
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    provider_mode: str = V042ChatShellProviderMode.AUTO.value,
    session_id: str | None = None,
    new_session: bool = False,
    max_turns: int | None = None,
    banner_enabled: bool = True,
    **overrides: Any,
) -> V042ChatShellConfig:
    bounded_turns = None if max_turns is None else max(1, min(int(max_turns), 200))
    defaults = {
        "config_id": "v0424-chat-shell-config",
        "profile_id": profile_id,
        "home_path": home_path,
        "provider_mode": provider_mode,
        "session_id": session_id,
        "new_session": new_session,
        "max_turns": bounded_turns,
        "banner_enabled": banner_enabled,
        "internal_commands_enabled": True,
        "default_prompt_label": "chanta",
        "use_default_home_resolver": True,
        "allow_real_provider": provider_mode in {V042ChatShellProviderMode.CONFIGURED.value, V042ChatShellProviderMode.AUTO.value},
        "allow_mock_provider": True,
    }
    return V042ChatShellConfig(**_merge(defaults, overrides))


def create_v042_chat_shell_start_request(
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    provider: str | None = None,
    session_id: str | None = None,
    new_session: bool = False,
    max_turns: int | None = None,
    mode: str = V042ChatShellMode.INTERACTIVE.value,
    **overrides: Any,
) -> V042ChatShellStartRequest:
    bounded_turns = None if max_turns is None else max(1, min(int(max_turns), 200))
    defaults = {
        "request_id": "v0424-chat-shell-start-request",
        "profile_id": profile_id,
        "home_path": home_path,
        "provider": provider,
        "session_id": session_id,
        "new_session": new_session,
        "max_turns": bounded_turns,
        "mode": mode,
    }
    return V042ChatShellStartRequest(**_merge(defaults, overrides))


def create_v042_chat_shell_session_state(
    profile_id: str = PROFILE_ID,
    resolved_home_path: str = "",
    session_id: str | None = None,
    provider_mode: str = V042ChatShellProviderMode.MOCK.value,
    **overrides: Any,
) -> V042ChatShellSessionState:
    defaults = {
        "state_id": "v0424-chat-shell-session-state",
        "profile_id": profile_id,
        "resolved_home_path": resolved_home_path,
        "session_id": _session_id(session_id),
        "provider_mode": provider_mode,
        "turn_count": 0,
        "run_ids": (),
        "started_at": _now(),
        "last_run_id": None,
        "last_assistant_preview": None,
        "exited": False,
        "exit_reason": None,
    }
    return V042ChatShellSessionState(**_merge(defaults, overrides))


def create_v042_chat_shell_loop_policy(**overrides: Any) -> V042ChatShellLoopPolicy:
    defaults = {
        "policy_id": "v0424-chat-shell-loop-policy",
        "ui_loop_allowed": True,
        "agent_loop_allowed": False,
        "autonomous_continuation_allowed": False,
        "retry_loop_allowed": False,
        "one_run_per_user_message": True,
        "internal_commands_call_provider": False,
        "internal_commands_mutate_files": False,
        "shell_execution_allowed": False,
        "subagent_allowed": False,
        "tool_calling_allowed": False,
        "function_calling_allowed": False,
        "production_certified": False,
    }
    return V042ChatShellLoopPolicy(**_merge(defaults, overrides))


def create_v042_chat_shell_prompt_view(state: V042ChatShellSessionState, **overrides: Any) -> V042ChatShellPromptView:
    prompt = f"chanta[{state.provider_mode}:{state.turn_count}]> "
    defaults = {
        "view_id": "v0424-chat-shell-prompt-view",
        "prompt_text": prompt,
        "profile_id": state.profile_id,
        "session_id": state.session_id,
        "provider_mode": state.provider_mode,
        "turn_count": state.turn_count,
    }
    return V042ChatShellPromptView(**_merge(defaults, overrides))


def _unsafe_patterns(text: str) -> tuple[str, ...]:
    lower = text.lower()
    matched: list[str] = []
    for pattern in build_unsafe_command_patterns():
        for example in pattern.examples:
            token = example.lower().replace("...", "").strip()
            if token and token in lower:
                matched.append(pattern.pattern_name)
                break
    direct = ("remove-item -recurse -force", "rm -rf", "cmd /c", "powershell -command")
    matched.extend(item for item in direct if item in lower and item not in matched)
    return tuple(dict.fromkeys(matched))


def parse_v042_chat_shell_internal_command(raw_text: str) -> V042ChatShellInternalCommand:
    normalized = raw_text.strip().lower()
    mapping = {
        "/help": V042ChatShellInternalCommandKind.HELP.value,
        "/exit": V042ChatShellInternalCommandKind.EXIT.value,
        "/quit": V042ChatShellInternalCommandKind.QUIT.value,
        "/status": V042ChatShellInternalCommandKind.STATUS.value,
        "/provider": V042ChatShellInternalCommandKind.PROVIDER.value,
        "/history": V042ChatShellInternalCommandKind.HISTORY.value,
        "/trace": V042ChatShellInternalCommandKind.TRACE.value,
        "/run last": V042ChatShellInternalCommandKind.RUN_LAST.value,
        "/session": V042ChatShellInternalCommandKind.SESSION.value,
        "/handoff": V042ChatShellInternalCommandKind.HANDOFF.value,
        "/safety": V042ChatShellInternalCommandKind.SAFETY.value,
    }
    kind = mapping.get(normalized, V042ChatShellInternalCommandKind.UNKNOWN.value)
    return V042ChatShellInternalCommand(
        command_id=f"v0424-internal-command-{kind}",
        command_kind=kind,
        raw_text=raw_text,
        description=f"chat shell internal command: {kind}",
        provider_call_allowed=False,
        prompt_submission_allowed=False,
        mutates_filesystem=False,
        exits_shell=kind in {V042ChatShellInternalCommandKind.EXIT.value, V042ChatShellInternalCommandKind.QUIT.value},
    )


def classify_v042_chat_shell_input(raw_text: str, **overrides: Any) -> V042ChatShellInputRecord:
    stripped = raw_text.strip()
    command = parse_v042_chat_shell_internal_command(stripped) if stripped.startswith("/") else None
    unsafe = bool(_unsafe_patterns(stripped)) and not stripped.lower().startswith("explain ")
    if not stripped:
        kind = V042ChatShellInputKind.EMPTY.value
    elif command and command.command_kind in {V042ChatShellInternalCommandKind.EXIT.value, V042ChatShellInternalCommandKind.QUIT.value}:
        kind = V042ChatShellInputKind.EXIT.value
    elif command:
        kind = V042ChatShellInputKind.INTERNAL_COMMAND.value
    elif unsafe:
        kind = V042ChatShellInputKind.UNSAFE_COMMAND_LIKE_TEXT.value
    else:
        kind = V042ChatShellInputKind.USER_MESSAGE.value
    defaults = {
        "input_id": _new_id("v0424-input"),
        "raw_text": raw_text,
        "input_kind": kind,
        "normalized_text": stripped,
        "created_at": _now(),
        "unsafe_pattern_detected": unsafe,
        "internal_command_kind": command.command_kind if command else None,
    }
    return V042ChatShellInputRecord(**_merge(defaults, overrides))


def create_v042_chat_shell_help_view(**overrides: Any) -> V042ChatShellHelpView:
    commands = ("/help", "/exit", "/quit", "/status", "/provider", "/history", "/trace", "/run last", "/session", "/handoff", "/safety")
    safety = "Shell commands are not executed. User messages run at most one existing single-turn text run."
    rendered = "\n".join(("ChantaCore Chat Help", "Type a message and press Enter.", "Commands:", *(f"- {item}" for item in commands), safety))
    defaults = {"view_id": "v0424-chat-help-view", "rendered_text": rendered, "commands": commands, "safety_statement": safety}
    return V042ChatShellHelpView(**_merge(defaults, overrides))


def create_v042_chat_shell_status_view(state: V042ChatShellSessionState, **overrides: Any) -> V042ChatShellStatusView:
    rendered = "\n".join(
        (
            "ChantaCore Chat Status",
            f"profile: {state.profile_id}",
            f"home: {state.resolved_home_path}",
            f"session: {state.session_id}",
            f"provider: {state.provider_mode}",
            f"turn_count: {state.turn_count}",
            f"latest_run_id: {state.last_run_id or '-'}",
            "closed: agent_loop retry_loop shell subagent tools functions production",
        )
    )
    defaults = {
        "view_id": "v0424-chat-status-view",
        "profile_id": state.profile_id,
        "home_path": state.resolved_home_path,
        "session_id": state.session_id,
        "provider_mode": state.provider_mode,
        "turn_count": state.turn_count,
        "latest_run_id": state.last_run_id,
        "high_risk_capabilities_closed": True,
        "rendered_text": rendered,
    }
    return V042ChatShellStatusView(**_merge(defaults, overrides))


def create_v042_chat_shell_provider_view(state: V042ChatShellSessionState, **overrides: Any) -> V042ChatShellProviderView:
    report = create_v042_provider_status_report(create_v042_provider_status_request(state.resolved_home_path, state.profile_id))
    rendered = "\n".join(("ChantaCore Chat Provider", report.rendered_text, "secrets: redacted/not included"))
    defaults = {"view_id": "v0424-chat-provider-view", "rendered_text": rendered, "provider_invoked": False, "secret_values_redacted": True}
    return V042ChatShellProviderView(**_merge(defaults, overrides))


def create_v042_chat_shell_history_view(state: V042ChatShellSessionState, **overrides: Any) -> V042ChatShellHistoryView:
    result = create_v042_run_history_result(create_v042_run_history_request(state.profile_id, state.resolved_home_path, 10))
    defaults = {"view_id": "v0424-chat-history-view", "rendered_text": result.rendered_text, "provider_invoked": False}
    return V042ChatShellHistoryView(**_merge(defaults, overrides))


def create_v042_chat_shell_trace_view(state: V042ChatShellSessionState, **overrides: Any) -> V042ChatShellTraceView:
    result = create_v042_trace_timeline_result(create_v042_trace_timeline_request(state.profile_id, state.resolved_home_path, 10))
    defaults = {"view_id": "v0424-chat-trace-view", "rendered_text": result.rendered_text, "provider_invoked": False, "mutated_filesystem": False}
    return V042ChatShellTraceView(**_merge(defaults, overrides))


def create_v042_chat_shell_session_view(state: V042ChatShellSessionState, **overrides: Any) -> V042ChatShellSessionView:
    result = create_v042_session_show_result(create_v042_session_show_request(state.profile_id, state.resolved_home_path, "session_id", state.session_id))
    defaults = {"view_id": "v0424-chat-session-view", "rendered_text": result.rendered_text, "provider_invoked": False, "provider_text_untrusted": True}
    return V042ChatShellSessionView(**_merge(defaults, overrides))


def create_v042_chat_shell_debug_handoff(state: V042ChatShellSessionState, **overrides: Any) -> V042ChatShellDebugHandoff:
    safety = "shell=0 skill=0 subagent=0 production=0"
    text = "\n".join(
        (
            "ChantaCore chat debug handoff",
            f"version: {V0424_VERSION}",
            f"profile_id: {state.profile_id}",
            f"home_path: {state.resolved_home_path}",
            f"session_id: {state.session_id}",
            f"provider_mode: {state.provider_mode}",
            f"run_ids: {', '.join(state.run_ids) if state.run_ids else '(none)'}",
            f"total_turns: {state.turn_count}",
            f"safety_counts: {safety}",
            "secrets: redacted/not included",
        )
    )
    defaults = {
        "handoff_id": "v0424-chat-debug-handoff",
        "profile_id": state.profile_id,
        "home_path": state.resolved_home_path,
        "session_id": state.session_id,
        "run_ids": state.run_ids,
        "provider_mode": state.provider_mode,
        "total_turns": state.turn_count,
        "safety_counts_summary": safety,
        "concise_text": text,
        "includes_secret_values": False,
        "suitable_for_gpt_or_codex": True,
    }
    return V042ChatShellDebugHandoff(**_merge(defaults, overrides))


def create_v042_chat_shell_render_policy(**overrides: Any) -> V042ChatShellRenderPolicy:
    defaults = {
        "policy_id": "v0424-chat-shell-render-policy",
        "show_banner": True,
        "show_prompt": True,
        "show_session_id": True,
        "show_run_id_after_turn": True,
        "show_provider_mode": True,
        "mark_provider_text_untrusted": True,
        "show_safety_footer": True,
        "redact_secrets": True,
    }
    return V042ChatShellRenderPolicy(**_merge(defaults, overrides))


def create_v042_chat_shell_safety_report(**overrides: Any) -> V042ChatShellSafetyReport:
    defaults = {
        "report_id": "v0424-chat-shell-safety-report",
        "ui_loop_opened": True,
        "agent_loop_opened": False,
        "autonomous_continuation_allowed": False,
        "retry_loop_allowed": False,
        "provider_doctor_completion_allowed": False,
        "provider_tool_calling_allowed": False,
        "function_calling_allowed": False,
        "shell_execution_allowed": False,
        "file_edit_allowed": False,
        "patch_apply_allowed": False,
        "subagent_invocation_allowed": False,
        "read_only_skill_execution_as_actions_allowed": False,
        "production_certified": False,
    }
    return V042ChatShellSafetyReport(**_merge(defaults, overrides))


def create_v042_chat_shell_internal_command_result(
    command: V042ChatShellInternalCommand,
    state: V042ChatShellSessionState | None = None,
    **overrides: Any,
) -> V042ChatShellInternalCommandResult:
    kind = command.command_kind
    rendered = ""
    if kind == V042ChatShellInternalCommandKind.HELP.value:
        rendered = create_v042_chat_shell_help_view().rendered_text
    elif kind in {V042ChatShellInternalCommandKind.EXIT.value, V042ChatShellInternalCommandKind.QUIT.value}:
        rendered = "ChantaCore chat exiting."
    elif state and kind == V042ChatShellInternalCommandKind.STATUS.value:
        rendered = create_v042_chat_shell_status_view(state).rendered_text
    elif state and kind == V042ChatShellInternalCommandKind.PROVIDER.value:
        rendered = create_v042_chat_shell_provider_view(state).rendered_text
    elif state and kind == V042ChatShellInternalCommandKind.HISTORY.value:
        rendered = create_v042_chat_shell_history_view(state).rendered_text
    elif state and kind == V042ChatShellInternalCommandKind.TRACE.value:
        rendered = create_v042_chat_shell_trace_view(state).rendered_text
    elif state and kind == V042ChatShellInternalCommandKind.RUN_LAST.value:
        rendered = create_v042_run_show_result(create_v042_run_show_request(state.profile_id, state.resolved_home_path, "last")).rendered_text
    elif state and kind == V042ChatShellInternalCommandKind.SESSION.value:
        rendered = create_v042_chat_shell_session_view(state).rendered_text
    elif state and kind == V042ChatShellInternalCommandKind.HANDOFF.value:
        rendered = create_v042_chat_shell_debug_handoff(state).concise_text
    elif kind == V042ChatShellInternalCommandKind.SAFETY.value:
        rendered = "Chat safety: ui_loop=true; agent_loop=false; retry_loop=false; shell=false; subagent=false; tools=false; functions=false; production=false"
    else:
        rendered = "Unknown chat command. Type /help for safe commands. No shell text was executed."
    defaults = {
        "result_id": _new_id("v0424-internal-result"),
        "command_kind": kind,
        "status": V042ChatShellStatus.INTERNAL_COMMAND_COMPLETED.value,
        "rendered_text": rendered,
        "exit_requested": command.exits_shell,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "mutated_filesystem": False,
        "production_certified": False,
    }
    return V042ChatShellInternalCommandResult(**_merge(defaults, overrides))


def create_v042_chat_shell_turn_request(
    profile_id: str,
    home_path: str,
    session_id: str,
    provider: str | None,
    user_input: str,
    turn_index: int,
    **overrides: Any,
) -> V042ChatShellTurnRequest:
    defaults = {
        "request_id": _new_id("v0424-turn-request"),
        "profile_id": profile_id,
        "home_path": home_path,
        "session_id": session_id,
        "provider": provider,
        "user_input": user_input,
        "turn_index": turn_index,
    }
    return V042ChatShellTurnRequest(**_merge(defaults, overrides))


def execute_v042_chat_shell_turn(request: V042ChatShellTurnRequest, **overrides: Any) -> V042ChatShellTurnResult:
    if _unsafe_patterns(request.user_input):
        rendered = "Denied: command-like shell text is not executed by ChantaCore chat."
        defaults = {
            "result_id": _new_id("v0424-turn-result"),
            "request_id": request.request_id,
            "status": V042ChatShellStatus.DENIED.value,
            "run_id": None,
            "session_id": request.session_id,
            "assistant_text": None,
            "rendered_text": rendered,
            "provider_invoked": False,
            "prompt_submitted": False,
            "shell_executed": False,
            "skill_executed": False,
            "subagent_invoked": False,
            "autonomous_continuation_started": False,
            "retry_loop_started": False,
            "production_certified": False,
        }
        return V042ChatShellTurnResult(**_merge(defaults, overrides))

    args = ["run", "--profile", request.profile_id, "--home", request.home_path, "--session", request.session_id]
    if request.provider:
        args.extend(["--provider", request.provider])
    args.append(request.user_input)
    exit_code = _v0423_main(args)
    report = create_last_run_report(create_last_run_report_request(request.profile_id, request.home_path, request.session_id))
    status = V042ChatShellStatus.TURN_COMPLETED.value if exit_code == 0 and report.found else V042ChatShellStatus.FAILED.value
    assistant = report.assistant_response_preview
    rendered = "\n".join(
        (
            assistant or "(no assistant response recorded)",
            f"run_id: {report.run_id or '-'}",
            f"session_id: {request.session_id}",
            "provider_text_untrusted: true",
        )
    )
    defaults = {
        "result_id": _new_id("v0424-turn-result"),
        "request_id": request.request_id,
        "status": status,
        "run_id": report.run_id,
        "session_id": request.session_id,
        "assistant_text": assistant,
        "rendered_text": rendered,
        "provider_invoked": report.provider_invoked,
        "prompt_submitted": report.prompt_submitted,
        "shell_executed": False,
        "skill_executed": False,
        "subagent_invoked": False,
        "autonomous_continuation_started": False,
        "retry_loop_started": False,
        "production_certified": False,
    }
    return V042ChatShellTurnResult(**_merge(defaults, overrides))


def create_v042_chat_shell_run_invocation_record(turn_result: V042ChatShellTurnResult, user_input: str, turn_index: int, provider_mode: str, **overrides: Any) -> V042ChatShellRunInvocationRecord:
    defaults = {
        "record_id": _new_id("v0424-run-invocation"),
        "turn_index": turn_index,
        "user_input_preview": _preview(user_input),
        "run_id": turn_result.run_id,
        "session_id": turn_result.session_id,
        "provider_mode": provider_mode,
        "invoked_existing_run_path": turn_result.status != V042ChatShellStatus.DENIED.value,
        "scoped_single_turn": True,
        "tool_calling_used": False,
        "function_calling_used": False,
        "shell_executed": False,
        "subagent_invoked": False,
    }
    return V042ChatShellRunInvocationRecord(**_merge(defaults, overrides))


def create_v042_chat_shell_exit_decision(command_kind: str | None = None, reason: str = "user requested exit", **overrides: Any) -> V042ChatShellExitDecision:
    defaults = {
        "decision_id": "v0424-chat-shell-exit-decision",
        "exit_requested": command_kind in {V042ChatShellInternalCommandKind.EXIT.value, V042ChatShellInternalCommandKind.QUIT.value},
        "reason": reason,
        "command_kind": command_kind,
        "graceful": True,
    }
    return V042ChatShellExitDecision(**_merge(defaults, overrides))


def create_v042_chat_shell_summary(
    state: V042ChatShellSessionState,
    total_inputs: int,
    user_message_count: int,
    internal_command_count: int,
    denial_count: int = 0,
    exited_gracefully: bool = True,
    **overrides: Any,
) -> V042ChatShellSummary:
    defaults = {
        "summary_id": "v0424-chat-shell-summary",
        "profile_id": state.profile_id,
        "home_path": state.resolved_home_path,
        "session_id": state.session_id,
        "provider_mode": state.provider_mode,
        "total_inputs": total_inputs,
        "user_message_count": user_message_count,
        "internal_command_count": internal_command_count,
        "run_count": len(state.run_ids),
        "denial_count": denial_count,
        "shell_execution_count": 0,
        "skill_execution_count": 0,
        "subagent_invocation_count": 0,
        "production_certification_count": 0,
        "run_ids": state.run_ids,
        "exited_gracefully": exited_gracefully,
    }
    return V042ChatShellSummary(**_merge(defaults, overrides))


def create_v042_chat_shell_scripted_run_result(
    inputs_processed: int,
    outputs: tuple[str, ...],
    summary: V042ChatShellSummary,
    turn_results: tuple[V042ChatShellTurnResult, ...],
    internal_command_results: tuple[V042ChatShellInternalCommandResult, ...],
    exited: bool,
    **overrides: Any,
) -> V042ChatShellScriptedRunResult:
    defaults = {
        "result_id": "v0424-chat-shell-scripted-run-result",
        "inputs_processed": inputs_processed,
        "outputs": outputs,
        "summary": summary,
        "turn_results": turn_results,
        "internal_command_results": internal_command_results,
        "exited": exited,
        "provider_invoked_count": sum(1 for result in turn_results if result.provider_invoked),
        "prompt_submitted_count": sum(1 for result in turn_results if result.prompt_submitted),
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    return V042ChatShellScriptedRunResult(**_merge(defaults, overrides))


def _provider_arg(provider_mode: str) -> str | None:
    if provider_mode == V042ChatShellProviderMode.MOCK.value:
        return "mock"
    if provider_mode == V042ChatShellProviderMode.CONFIGURED.value:
        return None
    return "mock"


def run_v042_chat_shell_scripted(
    inputs: Iterable[str],
    home_path: str | None = None,
    profile_id: str = PROFILE_ID,
    provider: str | None = "mock",
    session_id: str | None = None,
    new_session: bool = False,
    max_turns: int | None = None,
    banner_enabled: bool = True,
) -> V042ChatShellScriptedRunResult:
    provider_mode = provider or V042ChatShellProviderMode.AUTO.value
    resolved_home = _resolve_home(home_path, "chat")
    state = create_v042_chat_shell_session_state(
        profile_id,
        resolved_home,
        None if new_session else session_id,
        provider_mode,
    )
    outputs: list[str] = []
    if banner_enabled:
        outputs.append(f"ChantaCore chat started. session={state.session_id} provider={state.provider_mode}")
    turn_results: list[V042ChatShellTurnResult] = []
    internal_results: list[V042ChatShellInternalCommandResult] = []
    total = 0
    users = 0
    internals = 0
    denials = 0
    exited = False
    bounded_max = None if max_turns is None else max(1, min(int(max_turns), 200))

    for raw in inputs:
        total += 1
        record = classify_v042_chat_shell_input(raw)
        if record.input_kind == V042ChatShellInputKind.EMPTY.value:
            outputs.append("(empty input ignored)")
            continue
        if record.input_kind in {V042ChatShellInputKind.INTERNAL_COMMAND.value, V042ChatShellInputKind.EXIT.value}:
            internals += 1
            command = parse_v042_chat_shell_internal_command(record.normalized_text)
            result = create_v042_chat_shell_internal_command_result(command, state)
            internal_results.append(result)
            outputs.append(result.rendered_text)
            if result.exit_requested:
                state = replace(state, exited=True, exit_reason=command.command_kind)
                exited = True
                break
            continue
        if record.input_kind == V042ChatShellInputKind.UNSAFE_COMMAND_LIKE_TEXT.value:
            denials += 1
        if bounded_max is not None and users >= bounded_max:
            outputs.append("Chat max_turns reached; no autonomous continuation was started.")
            break
        users += 1
        request = create_v042_chat_shell_turn_request(
            state.profile_id,
            state.resolved_home_path,
            state.session_id,
            _provider_arg(state.provider_mode),
            record.normalized_text,
            users,
        )
        turn = execute_v042_chat_shell_turn(request)
        turn_results.append(turn)
        outputs.append(turn.rendered_text)
        if turn.status == V042ChatShellStatus.DENIED.value:
            denials += 1
        run_ids = state.run_ids + ((turn.run_id,) if turn.run_id else ())
        state = replace(
            state,
            turn_count=users,
            run_ids=run_ids,
            last_run_id=turn.run_id or state.last_run_id,
            last_assistant_preview=turn.assistant_text or state.last_assistant_preview,
        )
    if not exited:
        state = replace(state, exited=True, exit_reason="input exhausted")
    summary = create_v042_chat_shell_summary(state, total, users, internals, denials, exited_gracefully=True)
    return create_v042_chat_shell_scripted_run_result(total, tuple(outputs), summary, tuple(turn_results), tuple(internal_results), state.exited)


def create_v0424_readiness_report(**overrides: Any) -> V0424ReadinessReport:
    defaults = {
        "chat_command_ready": True,
        "manual_ui_loop_ready": True,
        "one_run_per_user_message_ready": True,
        "internal_help_command_ready": True,
        "internal_exit_command_ready": True,
        "internal_status_command_ready": True,
        "internal_provider_command_ready": True,
        "internal_history_command_ready": True,
        "internal_trace_command_ready": True,
        "internal_session_command_ready": True,
        "internal_handoff_command_ready": True,
        "chat_shell_scripted_test_helper_ready": True,
        "chat_shell_safety_report_ready": True,
        "integrated_restore_document_ready": True,
        "v0425_handoff_ready": True,
        "ready_for_autonomous_agent_loop": False,
        "ready_for_general_agent_loop": False,
        "ready_for_multi_step_agent_loop": False,
        "ready_for_retry_loop": False,
        "ready_for_provider_doctor_completion": False,
        "ready_for_provider_tool_calling": False,
        "ready_for_function_calling": False,
        "ready_for_read_only_skill_execution_as_actions": False,
        "ready_for_shell_execution": False,
        "ready_for_file_edit": False,
        "ready_for_patch_apply": False,
        "ready_for_subagent_invocation": False,
        "ready_for_child_session_creation": False,
        "ready_for_autonomous_retry_loop": False,
        "ready_for_dominion_runtime": False,
        "production_certified": False,
    }
    return V0424ReadinessReport(**_merge(defaults, overrides))


def create_v0425_bounded_read_only_skill_execution_handoff(**overrides: Any) -> V0425BoundedReadOnlySkillExecutionHandoff:
    defaults = {
        "target_version": "v0.42.5 Bounded Read-only Skill Execution",
        "recommended_focus": (
            "safe bounded metadata/report skills",
            "profile_status",
            "provider_status",
            "trace_summary",
            "run_report_last",
            "run_history",
            "session_show",
            "config_view",
            "PI-reviewable trace for every skill execution",
        ),
        "must_not_open": (
            "shell_execution",
            "file_edit",
            "patch_apply",
            "provider_tool_calling",
            "function_calling",
            "subagent_invocation",
            "general_agent_loop",
            "autonomous_loop",
            "production_certification",
        ),
        "production_certified": False,
    }
    return V0425BoundedReadOnlySkillExecutionHandoff(**_merge(defaults, overrides))


REQUIRED_V0424_RESTORE_SECTIONS = (
    "Restore Purpose",
    "One-Screen Restore Summary",
    "Current Version and Track Identity",
    "Project Context for New Codex Session",
    "v0.41.6 User Test Baseline",
    "v0.42.0 UX Baseline Summary",
    "v0.42.1 Home / Quickstart Summary",
    "v0.42.2 Provider Setup Summary",
    "v0.42.3 Trace / Run History Summary",
    "Interactive Manual Chat Shell Summary",
    "Chat Command Contract",
    "Manual UI Loop Contract",
    "Internal Command Contract",
    "One-run-per-user-message Contract",
    "Chat Session Contract",
    "Chat Shell Safety Boundary",
    "Scripted Test Helper Contract",
    "Debug Handoff Contract",
    "Runtime Opening Status",
    "Still-Closed Capabilities",
    "Required Test Commands",
    "Expected Test Interpretation",
    "Withdrawal Conditions",
    "v0.42.5 Recommended Next Step",
    "Copy-Paste Restore Prompt for Future GPT/Codex Session",
)


def create_v0424_integrated_restore_context_snapshot(**overrides: Any) -> V0424IntegratedRestoreContextSnapshot:
    defaults = {
        "current_version": V0424_RELEASE_NAME,
        "current_track": V042_TRACK_NAME,
        "baseline_versions": (
            "v0.40.9 Controlled Mission Loop Preparation Consolidation & v0.41 Default Personal Runtime Handoff",
            "v0.41.0 Default Personal Profile Runtime Foundation",
            "v0.41.1 Installable CLI Bootstrap & Doctor",
            "v0.41.2 Prompt Assembly & Session Store",
            "v0.41.3 Safe Provider Probe & Read-only Skill Registry",
            "v0.41.4 Minimal Single-turn Provider-backed Run",
            "v0.41.5 Event Trace Emission & Runtime Report",
            "v0.41.6 Installable Default Personal User Test Release",
            "v0.42.0 Default Personal Runtime UX Baseline & User Journey Contract",
            "v0.42.1 Default Home Resolver & Quickstart",
            "v0.42.2 Provider Setup UX",
            "v0.42.3 Human-readable Trace / Run History",
            V0424_RELEASE_NAME,
        ),
        "open_capabilities": (
            "chat_command",
            "manual_ui_loop",
            "one_run_per_user_message",
            "internal_help_command",
            "internal_exit_command",
            "internal_status_command",
            "internal_provider_command",
            "internal_history_command",
            "internal_trace_command",
            "internal_session_command",
            "internal_handoff_command",
            "chat_shell_debug_handoff",
            "chat_shell_scripted_test_helper",
            "chat_shell_safety_report",
            "integrated_restore_document",
        ),
        "closed_capabilities": (
            "autonomous_agent_loop",
            "general_agent_loop",
            "multi_step_agent_loop",
            "retry_loop",
            "provider_doctor_completion",
            "provider_tool_calling",
            "function_calling",
            "read_only_skill_execution_as_actions",
            "shell_execution",
            "file_edit",
            "patch_apply",
            "test_execution_through_cli",
            "subagent_invocation",
            "child_session_creation",
            "parent_raw_transcript_sharing",
            "autonomous_retry_loop",
            "dominion_runtime",
            "production_certification",
        ),
    }
    return V0424IntegratedRestoreContextSnapshot(**_merge(defaults, overrides))


def create_v0424_integrated_restore_packet(**overrides: Any) -> V0424IntegratedRestorePacket:
    sections = tuple(V0424IntegratedRestoreSection(section.lower().replace(" ", "_").replace("/", "_").replace("-", "_"), section, True) for section in REQUIRED_V0424_RESTORE_SECTIONS)
    defaults = {
        "packet_id": "v0424-integrated-restore-packet",
        "context_snapshot": create_v0424_integrated_restore_context_snapshot(),
        "sections": sections,
        "single_integrated_doc_path": INTEGRATED_DOC_PATH,
        "separate_restore_doc_created": False,
    }
    return V0424IntegratedRestorePacket(**_merge(defaults, overrides))


def create_v0424_integrated_restore_document_manifest(**overrides: Any) -> V0424IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "v0424-integrated-restore-document-manifest",
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": False,
        "copy_paste_restore_prompt_required": True,
        "suitable_for_new_session_handoff": True,
        "required_sections": REQUIRED_V0424_RESTORE_SECTIONS,
    }
    return V0424IntegratedRestoreDocumentManifest(**_merge(defaults, overrides))


def _run_interactive(request: V042ChatShellStartRequest, no_banner: bool = False) -> int:
    home = _resolve_home(request.home_path, "chat")
    state = create_v042_chat_shell_session_state(request.profile_id, home, None if request.new_session else request.session_id, request.provider or V042ChatShellProviderMode.AUTO.value)
    if not no_banner:
        print(f"ChantaCore chat started. session={state.session_id} provider={state.provider_mode}")
        print("Type /help for commands. Type /exit to leave.")
    turns = 0
    while True:
        try:
            raw = input(create_v042_chat_shell_prompt_view(state).prompt_text)
        except (EOFError, KeyboardInterrupt):
            print("\nChantaCore chat exiting.")
            return 0
        result = run_v042_chat_shell_scripted([raw], home, request.profile_id, request.provider or "mock", state.session_id, False, request.max_turns, False)
        for output in result.outputs:
            print(output)
        if result.turn_results:
            turn = result.turn_results[-1]
            if turn.run_id:
                state = replace(state, turn_count=state.turn_count + 1, run_ids=state.run_ids + (turn.run_id,), last_run_id=turn.run_id, last_assistant_preview=turn.assistant_text)
                turns += 1
        if result.exited and result.internal_command_results and result.internal_command_results[-1].exit_requested:
            return 0
        if request.max_turns is not None and turns >= request.max_turns:
            print("max_turns reached; exiting without autonomous continuation.")
            return 0


def _handle_chat(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli chat")
    parser.add_argument("--home")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--provider", default="mock")
    parser.add_argument("--session", dest="session_id")
    parser.add_argument("--new-session", action="store_true")
    parser.add_argument("--max-turns", type=int)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-banner", action="store_true")
    parsed = parser.parse_args(list(args))
    request = create_v042_chat_shell_start_request(parsed.profile, parsed.home, parsed.provider, parsed.session_id, parsed.new_session, parsed.max_turns)
    if parsed.json:
        home = _resolve_home(parsed.home, "chat")
        state = create_v042_chat_shell_session_state(parsed.profile, home, None if parsed.new_session else parsed.session_id, parsed.provider)
        print(_render_json(create_v042_chat_shell_summary(state, 0, 0, 0)))
        return 0
    return _run_interactive(request, parsed.no_banner)


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] in {"--version", "version"}:
        print(f"chanta-cli v0.41.1 (runtime {V0424_VERSION}; {V0424_RELEASE_NAME})")
        return 0
    if args and args[0] == "chat":
        return _handle_chat(args[1:])
    return _v0423_main(args)


__all__ = [
    name
    for name in globals()
    if name.startswith("V042")
    or name.startswith("create_v042")
    or name.startswith("classify_v042")
    or name.startswith("parse_v042")
    or name.startswith("run_v042")
    or name == "execute_v042_chat_shell_turn"
    or name == "main"
]
