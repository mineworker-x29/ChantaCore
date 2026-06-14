"""v0.42.3 human-readable trace and run history support.

This module is a read/report UX layer over existing trace and session data.
It does not call providers, submit prompts, append trace events, execute shell,
invoke subagents, or certify production.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass, is_dataclass, replace
from enum import StrEnum
from pathlib import Path
from typing import Any, Mapping, Sequence

from chanta_core.personal_runtime.default_personal_cli_bootstrap import PROFILE_ID
from chanta_core.personal_runtime.default_personal_home_quickstart import (
    create_v042_home_resolution_request,
    resolve_v042_home,
)
from chanta_core.personal_runtime.default_personal_provider_setup import (
    main as _v0422_main,
)


V0423_VERSION = "v0.42.3"
V0423_RELEASE_NAME = "v0.42.3 Human-readable Trace / Run History"
V042_TRACK_NAME = "v0.42 Default Personal Runtime UX Hardening Track"
INTEGRATED_DOC_PATH = "docs/versions/v0.42/v0.42.3_human_readable_trace_run_history_restore.md"


class V042TraceHistoryDisplayMode(StrEnum):
    TIMELINE = "timeline"
    RUN_HISTORY = "run_history"
    RUN_SHOW = "run_show"
    SESSION_SHOW = "session_show"
    DEBUG_HANDOFF = "debug_handoff"
    JSON = "json"
    UNKNOWN = "unknown"


class V042HumanReadableFormat(StrEnum):
    TEXT = "text"
    COMPACT_TEXT = "compact_text"
    MARKDOWN = "markdown"
    JSON = "json"
    UNKNOWN = "unknown"


class V042TraceTimelineItemKind(StrEnum):
    COMMAND = "command"
    PROFILE = "profile"
    PROVIDER = "provider"
    PROMPT = "prompt"
    RUN = "run"
    SESSION = "session"
    ASSISTANT_RESPONSE = "assistant_response"
    DENIAL = "denial"
    SAFETY = "safety"
    TRACE = "trace"
    UNKNOWN = "unknown"


class V042TraceTimelineStatus(StrEnum):
    COMPLETED = "completed"
    STARTED = "started"
    INFO = "info"
    DENIED = "denied"
    FAILED = "failed"
    WARNING = "warning"
    SKIPPED = "skipped"
    UNKNOWN = "unknown"


class V042RunLifecycleStatus(StrEnum):
    COMPLETED = "completed"
    STARTED = "started"
    FAILED = "failed"
    INCOMPLETE = "incomplete"
    UNKNOWN = "unknown"


class V042RunShowTarget(StrEnum):
    LAST = "last"
    RUN_ID = "run_id"
    UNKNOWN = "unknown"


class V042SessionShowTarget(StrEnum):
    LAST = "last"
    SESSION_ID = "session_id"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V042TraceTimelineItem:
    item_id: str
    order_index: int
    created_at: str
    event_kind: str
    status: str
    command_name: str | None
    run_id: str | None
    session_id: str | None
    title: str
    summary: str
    process_relevance: str
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    skill_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V042TraceTimelineRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    limit: int
    display_format: str
    include_denials: bool
    include_provider_events: bool
    include_debug_handoff: bool


@dataclass(frozen=True)
class V042ProviderCallCountSemantics:
    semantics_id: str
    provider_call_event_count: int
    provider_call_transaction_count: int
    started_event_count: int
    completed_event_count: int
    explanation: str
    user_facing_label: str


@dataclass(frozen=True)
class V042TraceTimelineResult:
    result_id: str
    profile_id: str
    resolved_home_path: str
    items: tuple[V042TraceTimelineItem, ...]
    event_count: int
    denial_count: int
    run_count: int
    provider_call_event_count: int
    provider_call_transaction_count: int
    shell_execution_count: int
    skill_execution_count: int
    subagent_invocation_count: int
    production_certification_count: int
    rendered_text: str
    debug_handoff_text: str | None
    provider_invoked: bool
    prompt_submitted: bool
    mutated_filesystem: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V042RunHistoryItem:
    item_id: str
    run_id: str
    session_id: str | None
    created_at: str
    status: str
    provider: str | None
    mock_provider: bool
    user_input_preview: str | None
    assistant_response_preview: str | None
    provider_call_transaction_count: int
    session_turns_appended: bool
    trace_event_count: int
    denial_count: int
    shell_executed: bool
    skill_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V042RunHistoryRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    limit: int
    display_format: str


@dataclass(frozen=True)
class V042RunHistoryResult:
    result_id: str
    profile_id: str
    resolved_home_path: str
    runs: tuple[V042RunHistoryItem, ...]
    run_count: int
    rendered_text: str
    provider_invoked: bool
    prompt_submitted: bool
    mutated_filesystem: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V042RunProcessStep:
    step_id: str
    order_index: int
    event_kind: str
    status: str
    title: str
    evidence_message: str
    created_at: str
    completed: bool
    process_relevance: str


@dataclass(frozen=True)
class V042SafetyCountSummary:
    summary_id: str
    shell_execution_count: int
    skill_execution_count: int
    subagent_invocation_count: int
    production_certification_count: int
    unsafe_denial_count: int
    provider_tool_calling_count: int
    function_calling_count: int
    safe_for_v0423_review: bool


@dataclass(frozen=True)
class V042RunProcessInstanceView:
    view_id: str
    run_id: str
    session_id: str | None
    profile_id: str
    lifecycle_status: str
    steps: tuple[V042RunProcessStep, ...]
    user_input_preview: str | None
    assistant_response_preview: str | None
    provider: str | None
    mock_provider: bool
    provider_call_event_count: int
    provider_call_transaction_count: int
    session_turn_count: int | None
    denial_count: int
    safety_summary: V042SafetyCountSummary
    process_instance_reconstructable: bool


@dataclass(frozen=True)
class V042RunShowRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    target: str
    run_id: str | None
    display_format: str
    include_debug_handoff: bool


@dataclass(frozen=True)
class V042DenialEvidenceView:
    view_id: str
    denial_count: int
    denied_commands: tuple[str, ...]
    matched_patterns: tuple[str, ...]
    evidence_summary: str
    proves_non_execution: bool


@dataclass(frozen=True)
class V042DebugHandoffText:
    handoff_id: str
    profile_id: str
    home_path: str
    run_id: str | None
    session_id: str | None
    concise_text: str
    includes_secret_values: bool
    suitable_for_gpt_or_codex: bool


@dataclass(frozen=True)
class V042RunShowResult:
    result_id: str
    profile_id: str
    resolved_home_path: str
    found: bool
    process_instance_view: V042RunProcessInstanceView | None
    denial_evidence: V042DenialEvidenceView | None
    rendered_text: str
    debug_handoff_text: str | None
    provider_invoked: bool
    prompt_submitted: bool
    mutated_filesystem: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V042SessionRunLink:
    link_id: str
    session_id: str
    run_id: str
    run_status: str
    created_at: str
    assistant_response_preview: str | None


@dataclass(frozen=True)
class V042SessionTurnPreview:
    turn_id: str
    role: str
    content_preview: str
    provider_generated: bool
    trusted_for_memory: bool
    trusted_for_execution: bool


@dataclass(frozen=True)
class V042SessionShowRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    target: str
    session_id: str | None
    display_format: str
    include_turns: bool
    max_turns: int


@dataclass(frozen=True)
class V042SessionShowResult:
    result_id: str
    profile_id: str
    resolved_home_path: str
    found: bool
    session_id: str | None
    run_links: tuple[V042SessionRunLink, ...]
    turn_previews: tuple[V042SessionTurnPreview, ...]
    session_turn_count: int
    related_trace_event_count: int
    rendered_text: str
    provider_invoked: bool
    prompt_submitted: bool
    mutated_filesystem: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V042HumanReadableRenderPolicy:
    policy_id: str
    default_format: str
    json_still_available: bool
    max_preview_chars: int
    redact_secrets: bool
    include_process_relevance: bool
    include_safety_counts: bool
    include_debug_handoff: bool
    mutate_on_read: bool


@dataclass(frozen=True)
class V042TraceHistorySafetyReport:
    report_id: str
    trace_commands_call_provider: bool
    trace_commands_submit_prompt: bool
    trace_commands_mutate_filesystem: bool
    trace_commands_execute_shell: bool
    trace_commands_invoke_subagent: bool
    trace_commands_certify_production: bool
    raw_secrets_redacted: bool
    provider_text_remains_untrusted: bool


@dataclass(frozen=True)
class V0423ReadinessReport:
    trace_timeline_command_ready: bool
    run_history_command_ready: bool
    run_show_last_command_ready: bool
    run_show_by_id_command_ready: bool
    session_show_last_command_ready: bool
    session_show_by_id_command_ready: bool
    provider_call_count_semantics_ready: bool
    process_instance_view_ready: bool
    denial_evidence_view_ready: bool
    safety_count_summary_ready: bool
    debug_handoff_text_ready: bool
    human_readable_render_policy_ready: bool
    integrated_restore_document_ready: bool
    v0424_handoff_ready: bool
    ready_for_interactive_chat_shell: bool
    ready_for_read_only_skill_execution_as_actions: bool
    ready_for_provider_doctor_completion: bool
    ready_for_provider_tool_calling: bool
    ready_for_function_calling: bool
    ready_for_general_agent_loop: bool
    ready_for_multi_step_agent_loop: bool
    ready_for_shell_execution: bool
    ready_for_file_edit: bool
    ready_for_patch_apply: bool
    ready_for_subagent_invocation: bool
    ready_for_autonomous_retry_loop: bool
    ready_for_dominion_runtime: bool
    production_certified: bool


@dataclass(frozen=True)
class V0424InteractiveManualChatShellHandoff:
    target_version: str
    title: str
    recommended_focus: tuple[str, ...]
    must_not_open: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V0423IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool


@dataclass(frozen=True)
class V0423IntegratedRestoreContextSnapshot:
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]


@dataclass(frozen=True)
class V0423IntegratedRestorePacket:
    packet_id: str
    context_snapshot: V0423IntegratedRestoreContextSnapshot
    sections: tuple[V0423IntegratedRestoreSection, ...]
    single_integrated_doc_path: str
    separate_restore_doc_created: bool


@dataclass(frozen=True)
class V0423IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_required: bool
    separate_restore_doc_allowed: bool
    separate_restore_doc_created: bool
    copy_paste_restore_prompt_required: bool
    suitable_for_new_session_handoff: bool
    required_sections: tuple[str, ...]


def _merge(defaults: Mapping[str, Any], overrides: Mapping[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    merged.update(overrides)
    return merged


def _json_ready(value: Any) -> Any:
    if is_dataclass(value):
        return {key: _json_ready(item) for key, item in asdict(value).items()}
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    return value


def _render_json(value: Any) -> str:
    return json.dumps(_json_ready(value), indent=2, sort_keys=True)


def _preview(value: str | None, limit: int = 140) -> str | None:
    if value is None:
        return None
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def _resolve_home(home_path: str | None, command_name: str) -> str:
    resolved = resolve_v042_home(create_v042_home_resolution_request(explicit_home=home_path, command_name=command_name, allow_create=False, cwd=os.getcwd()))
    return resolved.home_path or ""


def _events_path(home_path: str, profile_id: str) -> Path:
    return Path(home_path) / "profiles" / profile_id / "state" / "traces" / "events.jsonl"


def _sessions_dir(home_path: str, profile_id: str) -> Path:
    return Path(home_path) / "profiles" / profile_id / "state" / "sessions"


def _event_payload(line: str) -> dict[str, Any] | None:
    if not line.strip():
        return None
    data = json.loads(line)
    event = data.get("event", data)
    return event if isinstance(event, dict) else None


def load_v042_trace_events(home_path: str, profile_id: str = PROFILE_ID, limit: int | None = None) -> tuple[dict[str, Any], ...]:
    path = _events_path(home_path, profile_id)
    if not path.exists():
        return ()
    events = tuple(event for line in path.read_text(encoding="utf-8").splitlines() if (event := _event_payload(line)))
    return events[-limit:] if limit else events


def _event_bool(event: Mapping[str, Any], key: str) -> bool:
    return bool(event.get(key, False))


def _event_metadata(event: Mapping[str, Any]) -> dict[str, Any]:
    metadata = event.get("metadata", {})
    return metadata if isinstance(metadata, dict) else {}


def _item_kind(event_kind: str) -> str:
    if "provider" in event_kind:
        return V042TraceTimelineItemKind.PROVIDER.value
    if "prompt" in event_kind or "user_input" in event_kind:
        return V042TraceTimelineItemKind.PROMPT.value
    if event_kind.startswith("run_"):
        return V042TraceTimelineItemKind.RUN.value
    if "session" in event_kind:
        return V042TraceTimelineItemKind.SESSION.value
    if "assistant_response" in event_kind:
        return V042TraceTimelineItemKind.ASSISTANT_RESPONSE.value
    if "denied" in event_kind or "denial" in event_kind:
        return V042TraceTimelineItemKind.DENIAL.value
    if "safety" in event_kind or "unsafe" in event_kind:
        return V042TraceTimelineItemKind.SAFETY.value
    if "trace" in event_kind:
        return V042TraceTimelineItemKind.TRACE.value
    if "profile" in event_kind:
        return V042TraceTimelineItemKind.PROFILE.value
    if "command" in event_kind:
        return V042TraceTimelineItemKind.COMMAND.value
    return V042TraceTimelineItemKind.UNKNOWN.value


def create_v042_human_readable_render_policy(**overrides: Any) -> V042HumanReadableRenderPolicy:
    defaults = {
        "policy_id": "v0423-human-readable-render-policy",
        "default_format": V042HumanReadableFormat.TEXT.value,
        "json_still_available": True,
        "max_preview_chars": 140,
        "redact_secrets": True,
        "include_process_relevance": True,
        "include_safety_counts": True,
        "include_debug_handoff": True,
        "mutate_on_read": False,
    }
    return V042HumanReadableRenderPolicy(**_merge(defaults, overrides))


def create_v042_trace_timeline_request(
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    limit: int = 20,
    display_format: str = V042HumanReadableFormat.TEXT.value,
    include_denials: bool = True,
    include_provider_events: bool = True,
    include_debug_handoff: bool = False,
    **overrides: Any,
) -> V042TraceTimelineRequest:
    defaults = {
        "request_id": "v0423-trace-timeline-request",
        "profile_id": profile_id,
        "home_path": home_path,
        "limit": max(1, min(int(limit), 200)),
        "display_format": display_format,
        "include_denials": include_denials,
        "include_provider_events": include_provider_events,
        "include_debug_handoff": include_debug_handoff,
    }
    return V042TraceTimelineRequest(**_merge(defaults, overrides))


def create_v042_trace_timeline_item(event: Mapping[str, Any], order_index: int, **overrides: Any) -> V042TraceTimelineItem:
    event_kind = str(event.get("event_kind", "unknown"))
    title = f"{_item_kind(event_kind)}: {event_kind}"
    defaults = {
        "item_id": str(event.get("event_id", f"timeline-{order_index}")),
        "order_index": order_index,
        "created_at": str(event.get("created_at", "")),
        "event_kind": event_kind,
        "status": str(event.get("status", "unknown")),
        "command_name": event.get("command_name"),
        "run_id": event.get("run_id"),
        "session_id": event.get("session_id"),
        "title": title,
        "summary": str(event.get("message", event_kind)),
        "process_relevance": "Links command/session/run/provider evidence for process reconstruction.",
        "provider_invoked": _event_bool(event, "provider_invoked"),
        "prompt_submitted": _event_bool(event, "prompt_submitted"),
        "shell_executed": _event_bool(event, "shell_executed"),
        "skill_executed": _event_bool(event, "skill_executed"),
        "subagent_invoked": _event_bool(event, "subagent_invoked"),
        "production_certified": _event_bool(event, "production_certified"),
    }
    return V042TraceTimelineItem(**_merge(defaults, overrides))


def create_v042_provider_call_count_semantics(events: Sequence[Mapping[str, Any]], **overrides: Any) -> V042ProviderCallCountSemantics:
    provider_events = [event for event in events if str(event.get("event_kind")) in {"provider_text_call_started", "provider_text_call_completed"}]
    started = [event for event in provider_events if event.get("event_kind") == "provider_text_call_started"]
    completed = [event for event in provider_events if event.get("event_kind") == "provider_text_call_completed"]
    run_ids = {str(event.get("run_id")) for event in provider_events if event.get("run_id")}
    defaults = {
        "semantics_id": "v0423-provider-call-count-semantics",
        "provider_call_event_count": len(provider_events),
        "provider_call_transaction_count": len(run_ids),
        "started_event_count": len(started),
        "completed_event_count": len(completed),
        "explanation": "Provider call event count counts provider_text_call_started and provider_text_call_completed events. Provider call transaction count estimates actual provider run transactions by grouping started/completed events by run_id.",
        "user_facing_label": "provider events vs provider transactions",
    }
    return V042ProviderCallCountSemantics(**_merge(defaults, overrides))


def create_v042_safety_count_summary(events: Sequence[Mapping[str, Any]], **overrides: Any) -> V042SafetyCountSummary:
    shell = sum(1 for event in events if _event_bool(event, "shell_executed"))
    skill = sum(1 for event in events if _event_bool(event, "skill_executed"))
    subagent = sum(1 for event in events if _event_bool(event, "subagent_invoked"))
    production = sum(1 for event in events if _event_bool(event, "production_certified"))
    denials = sum(1 for event in events if str(event.get("status")) == "denied" or str(event.get("event_kind", "")).endswith("_denied"))
    defaults = {
        "summary_id": "v0423-safety-count-summary",
        "shell_execution_count": shell,
        "skill_execution_count": skill,
        "subagent_invocation_count": subagent,
        "production_certification_count": production,
        "unsafe_denial_count": denials,
        "provider_tool_calling_count": 0,
        "function_calling_count": 0,
        "safe_for_v0423_review": shell == 0 and subagent == 0 and production == 0 and skill == 0,
    }
    return V042SafetyCountSummary(**_merge(defaults, overrides))


def create_v042_debug_handoff_text(
    profile_id: str,
    home_path: str,
    events: Sequence[Mapping[str, Any]] | None = None,
    run_id: str | None = None,
    session_id: str | None = None,
    provider_mode: str | None = None,
    safety_summary: V042SafetyCountSummary | None = None,
    provider_call_event_count: int | None = None,
    provider_call_transaction_count: int | None = None,
    **overrides: Any,
) -> V042DebugHandoffText:
    event_rows = tuple(events or ())
    safety = safety_summary or create_v042_safety_count_summary(event_rows)
    semantics = create_v042_provider_call_count_semantics(event_rows)
    event_count = provider_call_event_count if provider_call_event_count is not None else semantics.provider_call_event_count
    transaction_count = provider_call_transaction_count if provider_call_transaction_count is not None else semantics.provider_call_transaction_count
    text = "\n".join(
        (
            "ChantaCore debug handoff",
            f"version: {V0423_VERSION}",
            f"profile_id: {profile_id}",
            f"home_path: {home_path}",
            f"run_id: {run_id or '(none)'}",
            f"session_id: {session_id or '(none)'}",
            f"event_count: {len(event_rows)}",
            f"provider_mode: {provider_mode or '(unknown)'}",
            f"provider_call_event_count: {event_count}",
            f"provider_call_transaction_count: {transaction_count}",
            f"shell_execution_count: {safety.shell_execution_count}",
            f"skill_execution_count: {safety.skill_execution_count}",
            f"subagent_invocation_count: {safety.subagent_invocation_count}",
            f"production_certification_count: {safety.production_certification_count}",
            "secrets: redacted/not included",
        )
    )
    defaults = {
        "handoff_id": "v0423-debug-handoff-text",
        "profile_id": profile_id,
        "home_path": home_path,
        "run_id": run_id,
        "session_id": session_id,
        "concise_text": text,
        "includes_secret_values": False,
        "suitable_for_gpt_or_codex": True,
    }
    return V042DebugHandoffText(**_merge(defaults, overrides))


def build_v042_trace_timeline(request: V042TraceTimelineRequest) -> tuple[V042TraceTimelineItem, ...]:
    home = _resolve_home(request.home_path, "trace timeline")
    events = load_v042_trace_events(home, request.profile_id, request.limit)
    if not request.include_denials:
        events = tuple(event for event in events if str(event.get("status")) != "denied")
    if not request.include_provider_events:
        events = tuple(event for event in events if "provider_text_call" not in str(event.get("event_kind")))
    return tuple(create_v042_trace_timeline_item(event, index + 1) for index, event in enumerate(events))


def create_v042_trace_timeline_result(request: V042TraceTimelineRequest, **overrides: Any) -> V042TraceTimelineResult:
    home = _resolve_home(request.home_path, "trace timeline")
    events = load_v042_trace_events(home, request.profile_id, request.limit)
    items = build_v042_trace_timeline(request)
    semantics = create_v042_provider_call_count_semantics(events)
    safety = create_v042_safety_count_summary(events)
    run_count = len({event.get("run_id") for event in events if event.get("run_id")})
    handoff = create_v042_debug_handoff_text(request.profile_id, home, events).concise_text if request.include_debug_handoff else None
    defaults = {
        "result_id": "v0423-trace-timeline-result",
        "profile_id": request.profile_id,
        "resolved_home_path": home,
        "items": items,
        "event_count": len(events),
        "denial_count": safety.unsafe_denial_count,
        "run_count": run_count,
        "provider_call_event_count": semantics.provider_call_event_count,
        "provider_call_transaction_count": semantics.provider_call_transaction_count,
        "shell_execution_count": safety.shell_execution_count,
        "skill_execution_count": safety.skill_execution_count,
        "subagent_invocation_count": safety.subagent_invocation_count,
        "production_certification_count": safety.production_certification_count,
        "rendered_text": "",
        "debug_handoff_text": handoff,
        "provider_invoked": False,
        "prompt_submitted": False,
        "mutated_filesystem": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    result = V042TraceTimelineResult(**_merge(defaults, overrides))
    return replace(result, rendered_text=_render_json(result) if request.display_format == "json" else render_v042_trace_timeline_text(result))


def create_v042_run_history_request(profile_id: str = PROFILE_ID, home_path: str | None = None, limit: int = 20, display_format: str = "text", **overrides: Any) -> V042RunHistoryRequest:
    defaults = {"request_id": "v0423-run-history-request", "profile_id": profile_id, "home_path": home_path, "limit": max(1, min(int(limit), 200)), "display_format": display_format}
    return V042RunHistoryRequest(**_merge(defaults, overrides))


def _events_by_run(events: Sequence[Mapping[str, Any]]) -> dict[str, list[Mapping[str, Any]]]:
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for event in events:
        run_id = event.get("run_id")
        if run_id:
            grouped.setdefault(str(run_id), []).append(event)
    return grouped


def _run_status(events: Sequence[Mapping[str, Any]]) -> str:
    kinds = [event.get("event_kind") for event in events]
    if "run_completed" in kinds:
        return V042RunLifecycleStatus.COMPLETED.value
    if "run_failed" in kinds:
        return V042RunLifecycleStatus.FAILED.value
    if "run_started" in kinds:
        return V042RunLifecycleStatus.STARTED.value
    return V042RunLifecycleStatus.UNKNOWN.value


def build_v042_run_history_item(run_id: str, events: Sequence[Mapping[str, Any]], **overrides: Any) -> V042RunHistoryItem:
    metadata = {}
    for event in reversed(events):
        metadata.update(_event_metadata(event))
    semantics = create_v042_provider_call_count_semantics(events)
    defaults = {
        "item_id": f"v0423-run-history-{run_id}",
        "run_id": run_id,
        "session_id": next((event.get("session_id") for event in events if event.get("session_id")), None),
        "created_at": str(events[0].get("created_at", "")) if events else "",
        "status": _run_status(events),
        "provider": metadata.get("provider"),
        "mock_provider": bool(metadata.get("mock_provider", False)),
        "user_input_preview": metadata.get("user_input_preview"),
        "assistant_response_preview": metadata.get("assistant_response_preview"),
        "provider_call_transaction_count": semantics.provider_call_transaction_count,
        "session_turns_appended": any(event.get("event_kind") == "session_turns_appended" for event in events),
        "trace_event_count": len(events),
        "denial_count": sum(1 for event in events if str(event.get("status")) == "denied"),
        "shell_executed": any(_event_bool(event, "shell_executed") for event in events),
        "skill_executed": any(_event_bool(event, "skill_executed") for event in events),
        "subagent_invoked": any(_event_bool(event, "subagent_invoked") for event in events),
        "production_certified": any(_event_bool(event, "production_certified") for event in events),
    }
    return V042RunHistoryItem(**_merge(defaults, overrides))


def build_v042_run_history(request: V042RunHistoryRequest) -> tuple[V042RunHistoryItem, ...]:
    home = _resolve_home(request.home_path, "run history")
    grouped = _events_by_run(load_v042_trace_events(home, request.profile_id))
    items = [build_v042_run_history_item(run_id, events) for run_id, events in grouped.items()]
    items.sort(key=lambda item: item.created_at)
    return tuple(items[-request.limit :])


def create_v042_run_history_result(request: V042RunHistoryRequest, **overrides: Any) -> V042RunHistoryResult:
    home = _resolve_home(request.home_path, "run history")
    runs = build_v042_run_history(request)
    defaults = {
        "result_id": "v0423-run-history-result",
        "profile_id": request.profile_id,
        "resolved_home_path": home,
        "runs": runs,
        "run_count": len(runs),
        "rendered_text": "",
        "provider_invoked": False,
        "prompt_submitted": False,
        "mutated_filesystem": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    result = V042RunHistoryResult(**_merge(defaults, overrides))
    return replace(result, rendered_text=_render_json(result) if request.display_format == "json" else render_v042_run_history_text(result))


def create_v042_run_show_request(profile_id: str = PROFILE_ID, home_path: str | None = None, target: str = "last", run_id: str | None = None, display_format: str = "text", include_debug_handoff: bool = True, **overrides: Any) -> V042RunShowRequest:
    defaults = {"request_id": "v0423-run-show-request", "profile_id": profile_id, "home_path": home_path, "target": target, "run_id": run_id, "display_format": display_format, "include_debug_handoff": include_debug_handoff}
    return V042RunShowRequest(**_merge(defaults, overrides))


def build_v042_run_process_step(event: Mapping[str, Any], order_index: int, **overrides: Any) -> V042RunProcessStep:
    event_kind = str(event.get("event_kind", "unknown"))
    defaults = {
        "step_id": f"v0423-run-step-{order_index:02d}-{event_kind}",
        "order_index": order_index,
        "event_kind": event_kind,
        "status": str(event.get("status", "unknown")),
        "title": event_kind.replace("_", " "),
        "evidence_message": str(event.get("message", "")),
        "created_at": str(event.get("created_at", "")),
        "completed": str(event.get("status")) in {"completed", "info", "started"},
        "process_relevance": "Lifecycle evidence for run-as-process-instance reconstruction.",
    }
    return V042RunProcessStep(**_merge(defaults, overrides))


EXPECTED_LIFECYCLE = (
    "run_started",
    "user_input_received",
    "prompt_assembled",
    "provider_text_call_started",
    "provider_text_call_completed",
    "session_turns_appended",
    "assistant_response_recorded",
    "run_completed",
)


def _turn_count(home: str, profile_id: str, session_id: str | None) -> int | None:
    if not session_id:
        return None
    path = _sessions_dir(home, profile_id) / session_id / "turns.jsonl"
    if not path.exists():
        return None
    return len([line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()])


def build_v042_run_process_instance_view(home: str, profile_id: str, run_id: str, events: Sequence[Mapping[str, Any]], **overrides: Any) -> V042RunProcessInstanceView:
    steps = tuple(build_v042_run_process_step(event, index + 1) for index, event in enumerate(events))
    metadata: dict[str, Any] = {}
    for event in reversed(events):
        metadata.update(_event_metadata(event))
    semantics = create_v042_provider_call_count_semantics(events)
    safety = create_v042_safety_count_summary(events)
    kinds = {step.event_kind for step in steps}
    session_id = next((event.get("session_id") for event in events if event.get("session_id")), None)
    defaults = {
        "view_id": f"v0423-run-process-instance-{run_id}",
        "run_id": run_id,
        "session_id": session_id,
        "profile_id": profile_id,
        "lifecycle_status": _run_status(events),
        "steps": steps,
        "user_input_preview": metadata.get("user_input_preview"),
        "assistant_response_preview": metadata.get("assistant_response_preview"),
        "provider": metadata.get("provider"),
        "mock_provider": bool(metadata.get("mock_provider", False)),
        "provider_call_event_count": semantics.provider_call_event_count,
        "provider_call_transaction_count": semantics.provider_call_transaction_count,
        "session_turn_count": _turn_count(home, profile_id, str(session_id) if session_id else None),
        "denial_count": safety.unsafe_denial_count,
        "safety_summary": safety,
        "process_instance_reconstructable": bool(run_id and set(EXPECTED_LIFECYCLE).issubset(kinds)),
    }
    return V042RunProcessInstanceView(**_merge(defaults, overrides))


def create_v042_denial_evidence_view(events: Sequence[Mapping[str, Any]], **overrides: Any) -> V042DenialEvidenceView:
    denials = [event for event in events if str(event.get("status")) == "denied" or str(event.get("event_kind", "")).endswith("_denied")]
    commands: list[str] = []
    patterns: list[str] = []
    for event in denials:
        metadata = _event_metadata(event)
        if metadata.get("command_text_preview"):
            commands.append(str(metadata["command_text_preview"]))
        elif metadata.get("command"):
            commands.append(str(metadata["command"]))
        matched = metadata.get("matched_patterns", ())
        if isinstance(matched, list):
            patterns.extend(str(item) for item in matched)
    proves = bool(denials and all(not _event_bool(event, "shell_executed") for event in denials))
    defaults = {
        "view_id": "v0423-denial-evidence-view",
        "denial_count": len(denials),
        "denied_commands": tuple(commands),
        "matched_patterns": tuple(patterns),
        "evidence_summary": "Denial events show dangerous text was checked and not executed." if proves else "No denial evidence found.",
        "proves_non_execution": proves,
    }
    return V042DenialEvidenceView(**_merge(defaults, overrides))


def _select_run_events(home: str, profile_id: str, target: str, run_id: str | None) -> tuple[str | None, tuple[dict[str, Any], ...]]:
    grouped = _events_by_run(load_v042_trace_events(home, profile_id))
    selected = run_id if target == "run_id" else None
    if selected is None and grouped:
        selected = sorted(grouped.items(), key=lambda item: item[1][-1].get("created_at", ""))[-1][0]
    return selected, tuple(grouped.get(selected, ())) if selected else ()


def create_v042_run_show_result(request: V042RunShowRequest, **overrides: Any) -> V042RunShowResult:
    home = _resolve_home(request.home_path, "run show")
    selected, events = _select_run_events(home, request.profile_id, request.target, request.run_id)
    view = build_v042_run_process_instance_view(home, request.profile_id, selected, events) if selected and events else None
    denial = create_v042_denial_evidence_view(events) if events else None
    handoff = create_v042_debug_handoff_text(request.profile_id, home, events, selected, view.session_id if view else None).concise_text if request.include_debug_handoff and selected else None
    defaults = {
        "result_id": "v0423-run-show-result",
        "profile_id": request.profile_id,
        "resolved_home_path": home,
        "found": view is not None,
        "process_instance_view": view,
        "denial_evidence": denial,
        "rendered_text": "",
        "debug_handoff_text": handoff,
        "provider_invoked": False,
        "prompt_submitted": False,
        "mutated_filesystem": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    result = V042RunShowResult(**_merge(defaults, overrides))
    return replace(result, rendered_text=_render_json(result) if request.display_format == "json" else render_v042_run_show_text(result))


def create_v042_session_show_request(profile_id: str = PROFILE_ID, home_path: str | None = None, target: str = "last", session_id: str | None = None, display_format: str = "text", include_turns: bool = True, max_turns: int = 10, **overrides: Any) -> V042SessionShowRequest:
    defaults = {"request_id": "v0423-session-show-request", "profile_id": profile_id, "home_path": home_path, "target": target, "session_id": session_id, "display_format": display_format, "include_turns": include_turns, "max_turns": max(1, min(int(max_turns), 50))}
    return V042SessionShowRequest(**_merge(defaults, overrides))


def build_v042_session_run_link(session_id: str, run_id: str, events: Sequence[Mapping[str, Any]], **overrides: Any) -> V042SessionRunLink:
    item = build_v042_run_history_item(run_id, events)
    defaults = {"link_id": f"v0423-session-run-link-{run_id}", "session_id": session_id, "run_id": run_id, "run_status": item.status, "created_at": item.created_at, "assistant_response_preview": item.assistant_response_preview}
    return V042SessionRunLink(**_merge(defaults, overrides))


def build_v042_session_turn_preview(turn: Mapping[str, Any], **overrides: Any) -> V042SessionTurnPreview:
    defaults = {
        "turn_id": str(turn.get("turn_id", "")),
        "role": str(turn.get("role", "")),
        "content_preview": _preview(str(turn.get("content", ""))) or "",
        "provider_generated": bool(turn.get("provider_generated", False)),
        "trusted_for_memory": bool(turn.get("trusted_for_memory", False)),
        "trusted_for_execution": bool(turn.get("trusted_for_execution", False)),
    }
    return V042SessionTurnPreview(**_merge(defaults, overrides))


def _read_turns(home: str, profile_id: str, session_id: str, limit: int) -> tuple[V042SessionTurnPreview, ...]:
    path = _sessions_dir(home, profile_id) / session_id / "turns.jsonl"
    if not path.exists():
        return ()
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return tuple(build_v042_session_turn_preview(row) for row in rows[-limit:])


def _select_session_id(home: str, profile_id: str, target: str, session_id: str | None, events: Sequence[Mapping[str, Any]]) -> str | None:
    if target == "session_id" and session_id:
        return session_id
    ids = [str(event.get("session_id")) for event in events if event.get("session_id")]
    if ids:
        return ids[-1]
    sessions = _sessions_dir(home, profile_id)
    if not sessions.exists():
        return None
    dirs = sorted([path for path in sessions.iterdir() if path.is_dir()], key=lambda path: path.name)
    return dirs[-1].name if dirs else None


def create_v042_session_show_result(request: V042SessionShowRequest, **overrides: Any) -> V042SessionShowResult:
    home = _resolve_home(request.home_path, "session show")
    events = load_v042_trace_events(home, request.profile_id)
    selected = _select_session_id(home, request.profile_id, request.target, request.session_id, events)
    related = tuple(event for event in events if selected and event.get("session_id") == selected)
    grouped = _events_by_run(related)
    links = tuple(build_v042_session_run_link(str(selected), run_id, run_events) for run_id, run_events in grouped.items()) if selected else ()
    turns = _read_turns(home, request.profile_id, selected, request.max_turns) if selected and request.include_turns else ()
    defaults = {
        "result_id": "v0423-session-show-result",
        "profile_id": request.profile_id,
        "resolved_home_path": home,
        "found": selected is not None,
        "session_id": selected,
        "run_links": links,
        "turn_previews": turns,
        "session_turn_count": len(turns),
        "related_trace_event_count": len(related),
        "rendered_text": "",
        "provider_invoked": False,
        "prompt_submitted": False,
        "mutated_filesystem": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    result = V042SessionShowResult(**_merge(defaults, overrides))
    return replace(result, rendered_text=_render_json(result) if request.display_format == "json" else render_v042_session_show_text(result))


def render_v042_trace_timeline_text(result: V042TraceTimelineResult) -> str:
    lines = ["ChantaCore Trace Timeline", f"home: {result.resolved_home_path}", f"events: {result.event_count}", f"provider_call_event_count: {result.provider_call_event_count}", f"provider_call_transaction_count: {result.provider_call_transaction_count}"]
    lines.extend(f"- {item.created_at} [{item.status}] {item.event_kind} run={item.run_id or '-'} session={item.session_id or '-'} :: {item.summary}" for item in result.items)
    lines.append(f"safety: shell={result.shell_execution_count}, skill={result.skill_execution_count}, subagent={result.subagent_invocation_count}, production={result.production_certification_count}")
    if result.debug_handoff_text:
        lines.append(result.debug_handoff_text)
    return "\n".join(lines)


def render_v042_run_history_text(result: V042RunHistoryResult) -> str:
    lines = ["ChantaCore Run History", f"home: {result.resolved_home_path}", f"runs: {result.run_count}"]
    lines.extend(f"- {item.created_at} {item.run_id} session={item.session_id or '-'} status={item.status} provider={item.provider or '-'} mock={str(item.mock_provider).lower()} events={item.trace_event_count}" for item in result.runs)
    return "\n".join(lines)


def render_v042_run_show_text(result: V042RunShowResult) -> str:
    if not result.found or not result.process_instance_view:
        return f"ChantaCore Run Show\nhome: {result.resolved_home_path}\nfound: false"
    view = result.process_instance_view
    lines = ["ChantaCore Run Process Instance", f"run_id: {view.run_id}", f"session_id: {view.session_id or '-'}", f"status: {view.lifecycle_status}", f"reconstructable: {str(view.process_instance_reconstructable).lower()}", f"provider events: {view.provider_call_event_count}; provider transactions: {view.provider_call_transaction_count}", "steps:"]
    lines.extend(f"- {step.order_index}. {step.event_kind} [{step.status}] {step.evidence_message}" for step in view.steps)
    lines.append(f"safety: shell={view.safety_summary.shell_execution_count}, skill={view.safety_summary.skill_execution_count}, subagent={view.safety_summary.subagent_invocation_count}, production={view.safety_summary.production_certification_count}")
    if result.debug_handoff_text:
        lines.append(result.debug_handoff_text)
    return "\n".join(lines)


def render_v042_session_show_text(result: V042SessionShowResult) -> str:
    if not result.found:
        return f"ChantaCore Session Show\nhome: {result.resolved_home_path}\nfound: false"
    lines = ["ChantaCore Session Show", f"session_id: {result.session_id}", f"turns: {result.session_turn_count}", f"related_trace_events: {result.related_trace_event_count}", "runs:"]
    lines.extend(f"- {link.run_id} status={link.run_status} assistant={link.assistant_response_preview or '-'}" for link in result.run_links)
    lines.append("turn previews:")
    lines.extend(f"- {turn.role}: {turn.content_preview} trusted_memory={str(turn.trusted_for_memory).lower()} trusted_execution={str(turn.trusted_for_execution).lower()}" for turn in result.turn_previews)
    return "\n".join(lines)


def create_v042_trace_history_safety_report(**overrides: Any) -> V042TraceHistorySafetyReport:
    defaults = {
        "report_id": "v0423-trace-history-safety-report",
        "trace_commands_call_provider": False,
        "trace_commands_submit_prompt": False,
        "trace_commands_mutate_filesystem": False,
        "trace_commands_execute_shell": False,
        "trace_commands_invoke_subagent": False,
        "trace_commands_certify_production": False,
        "raw_secrets_redacted": True,
        "provider_text_remains_untrusted": True,
    }
    return V042TraceHistorySafetyReport(**_merge(defaults, overrides))


def create_v0423_readiness_report(**overrides: Any) -> V0423ReadinessReport:
    defaults = {
        "trace_timeline_command_ready": True,
        "run_history_command_ready": True,
        "run_show_last_command_ready": True,
        "run_show_by_id_command_ready": True,
        "session_show_last_command_ready": True,
        "session_show_by_id_command_ready": True,
        "provider_call_count_semantics_ready": True,
        "process_instance_view_ready": True,
        "denial_evidence_view_ready": True,
        "safety_count_summary_ready": True,
        "debug_handoff_text_ready": True,
        "human_readable_render_policy_ready": True,
        "integrated_restore_document_ready": True,
        "v0424_handoff_ready": True,
        "ready_for_interactive_chat_shell": False,
        "ready_for_read_only_skill_execution_as_actions": False,
        "ready_for_provider_doctor_completion": False,
        "ready_for_provider_tool_calling": False,
        "ready_for_function_calling": False,
        "ready_for_general_agent_loop": False,
        "ready_for_multi_step_agent_loop": False,
        "ready_for_shell_execution": False,
        "ready_for_file_edit": False,
        "ready_for_patch_apply": False,
        "ready_for_subagent_invocation": False,
        "ready_for_autonomous_retry_loop": False,
        "ready_for_dominion_runtime": False,
        "production_certified": False,
    }
    return V0423ReadinessReport(**_merge(defaults, overrides))


def create_v0424_interactive_manual_chat_shell_handoff(**overrides: Any) -> V0424InteractiveManualChatShellHandoff:
    defaults = {
        "target_version": "v0.42.4 Interactive Manual Chat Shell",
        "title": "Interactive Manual Chat Shell",
        "recommended_focus": ("chanta-cli chat or chanta-cli start", "manual multi-turn shell only", "one user input triggers one existing single-turn run", "trace every turn", "show session id and run id", "exit/help/status commands"),
        "must_not_open": ("autonomous_continuation", "retry_loop", "subagent_invocation", "shell_execution", "file_edit", "patch_apply", "production_certification"),
        "production_certified": False,
    }
    return V0424InteractiveManualChatShellHandoff(**_merge(defaults, overrides))


REQUIRED_V0423_RESTORE_SECTIONS: tuple[str, ...] = (
    "restore_purpose", "one_screen_restore_summary", "current_version_and_track", "project_context_for_new_codex_session", "v0416_user_test_baseline", "v0420_ux_baseline_summary", "v0421_home_quickstart_summary", "v0422_provider_setup_summary", "human_readable_trace_summary", "trace_timeline_contract", "run_history_contract", "run_show_contract", "session_show_contract", "provider_call_count_semantics", "process_instance_view_contract", "denial_evidence_contract", "safety_count_summary_contract", "debug_handoff_text_contract", "trace_history_safety_boundary", "runtime_opening_status", "still_closed_capabilities", "required_test_commands", "expected_test_interpretation", "withdrawal_conditions", "v0424_handoff", "copy_paste_restore_prompt",
)


def create_v0423_integrated_restore_context_snapshot(**overrides: Any) -> V0423IntegratedRestoreContextSnapshot:
    defaults = {
        "current_version": "v0.42.3 Human-readable Trace / Run History",
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
        ),
        "open_capabilities": ("trace_timeline_command", "run_history_command", "run_show_last_command", "run_show_by_id_command", "session_show_last_command", "session_show_by_id_command", "provider_call_event_vs_transaction_semantics", "run_process_instance_view", "denial_evidence_view", "safety_count_summary_view", "debug_handoff_text", "human_readable_trace_rendering", "integrated_restore_document"),
        "closed_capabilities": ("interactive_chat_shell", "read_only_skill_execution_as_actions", "provider_doctor_completion", "provider_tool_calling", "function_calling", "general_agent_loop", "multi_step_agent_loop", "shell_execution", "file_edit", "patch_apply", "test_execution_through_cli", "subagent_invocation", "child_session_creation", "autonomous_retry_loop", "dominion_runtime", "production_certification"),
    }
    return V0423IntegratedRestoreContextSnapshot(**_merge(defaults, overrides))


def create_v0423_integrated_restore_packet(**overrides: Any) -> V0423IntegratedRestorePacket:
    sections = tuple(V0423IntegratedRestoreSection(section_id, section_id.replace("_", " ").title(), True) for section_id in REQUIRED_V0423_RESTORE_SECTIONS)
    defaults = {"packet_id": "v0423-integrated-restore-packet", "context_snapshot": create_v0423_integrated_restore_context_snapshot(), "sections": sections, "single_integrated_doc_path": INTEGRATED_DOC_PATH, "separate_restore_doc_created": False}
    return V0423IntegratedRestorePacket(**_merge(defaults, overrides))


def create_v0423_integrated_restore_document_manifest(**overrides: Any) -> V0423IntegratedRestoreDocumentManifest:
    defaults = {"manifest_id": "v0423-integrated-restore-document-manifest", "integrated_doc_required": True, "separate_restore_doc_allowed": False, "separate_restore_doc_created": False, "copy_paste_restore_prompt_required": True, "suitable_for_new_session_handoff": True, "required_sections": REQUIRED_V0423_RESTORE_SECTIONS}
    return V0423IntegratedRestoreDocumentManifest(**_merge(defaults, overrides))


def _handle_trace_timeline(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli trace timeline")
    parser.add_argument("--home")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--json", action="store_true")
    parsed = parser.parse_args(list(args))
    fmt = "json" if parsed.json else "text"
    result = create_v042_trace_timeline_result(create_v042_trace_timeline_request(parsed.profile, parsed.home, parsed.limit, fmt))
    print(result.rendered_text)
    return 0


def _handle_run_history(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli run history")
    parser.add_argument("--home")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--json", action="store_true")
    parsed = parser.parse_args(list(args))
    fmt = "json" if parsed.json else "text"
    result = create_v042_run_history_result(create_v042_run_history_request(parsed.profile, parsed.home, parsed.limit, fmt))
    print(result.rendered_text)
    return 0


def _handle_run_show(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli run show")
    parser.add_argument("target", nargs="?", default=None)
    parser.add_argument("--run-id")
    parser.add_argument("--home")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--json", action="store_true")
    parsed = parser.parse_args(list(args))
    target = "run_id" if parsed.run_id else "last"
    result = create_v042_run_show_result(create_v042_run_show_request(parsed.profile, parsed.home, target, parsed.run_id, "json" if parsed.json else "text"))
    print(result.rendered_text)
    return 0 if result.found else 1


def _handle_session_show(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli session show")
    parser.add_argument("target", nargs="?", default=None)
    parser.add_argument("--session-id")
    parser.add_argument("--home")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--json", action="store_true")
    parsed = parser.parse_args(list(args))
    target = "session_id" if parsed.session_id else "last"
    result = create_v042_session_show_result(create_v042_session_show_request(parsed.profile, parsed.home, target, parsed.session_id, "json" if parsed.json else "text"))
    print(result.rendered_text)
    return 0 if result.found else 1


def _delegate_existing_with_resolved_home(args: Sequence[str]) -> int | None:
    if "--home" in args or len(args) < 2:
        return None
    if (args[0], args[1]) not in {("trace", "summary"), ("safety", "check-command")}:
        return None
    home = _resolve_home(None, f"{args[0]} {args[1]}")
    if not home or not Path(home).exists():
        print(
            "\n".join(
                (
                    "ChantaCore home is not ready.",
                    f"resolved_home: {home or '(unresolved)'}",
                    "next: run chanta-cli quickstart, pass --home, or set CHANTACORE_HOME.",
                )
            )
        )
        return 1
    return _v0422_main(list(args[:2]) + ["--home", home] + list(args[2:]))


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] in {"--version", "version"}:
        print(f"chanta-cli v0.41.1 (runtime {V0423_VERSION}; {V0423_RELEASE_NAME})")
        return 0
    if len(args) >= 2 and args[0] == "trace" and args[1] == "timeline":
        return _handle_trace_timeline(args[2:])
    if len(args) >= 2 and args[0] == "run" and args[1] == "history":
        return _handle_run_history(args[2:])
    if len(args) >= 2 and args[0] == "run" and args[1] == "show":
        return _handle_run_show(args[2:])
    if len(args) >= 2 and args[0] == "session" and args[1] == "show":
        return _handle_session_show(args[2:])
    delegated = _delegate_existing_with_resolved_home(args)
    if delegated is not None:
        return delegated
    return _v0422_main(args)


__all__ = [name for name in globals() if name.startswith("V042") or name.startswith("create_v042") or name.startswith("build_v042") or name.startswith("render_v042") or name.startswith("load_v042") or name == "main"]
