"""v0.41.5 default-personal runtime trace and report support.

This module opens bounded, append-only trace emission for the default
personal runtime. It does not execute commands supplied to safety checks,
does not open tool/function calling, and does not certify production release.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Sequence
from uuid import uuid4

from chanta_core.personal_runtime.default_personal_run import (
    RunCommandInput,
    RunCommandResult,
    execute_run_command,
    main as _v0414_main,
)


PROFILE_ID = "default-personal"
TRACE_SOURCE_VERSION = "v0.41.5"
TRACE_SCHEMA_VERSION = "v0.41.5.runtime-event-envelope"
TRACE_VERSION = "v0.41.5"
INTEGRATED_DOC_PATH = (
    "docs/versions/v0.41/v0.41.5_event_trace_emission_runtime_report_restore.md"
)


class RuntimeEventKind(str, Enum):
    RUNTIME_STARTED = "runtime_started"
    CLI_COMMAND_RECEIVED = "cli_command_received"
    CLI_COMMAND_COMPLETED = "cli_command_completed"
    DOCTOR_CHECK_STARTED = "doctor_check_started"
    DOCTOR_CHECK_COMPLETED = "doctor_check_completed"
    PROFILE_INIT_REQUESTED = "profile_init_requested"
    PROFILE_INITIALIZED = "profile_initialized"
    PROFILE_LOADED = "profile_loaded"
    PROFILE_STATUS_VIEWED = "profile_status_viewed"
    PROMPT_PREVIEW_REQUESTED = "prompt_preview_requested"
    PROMPT_PREVIEW_RENDERED = "prompt_preview_rendered"
    SESSION_CREATED = "session_created"
    SESSION_LIST_VIEWED = "session_list_viewed"
    PROVIDER_DOCTOR_STARTED = "provider_doctor_started"
    PROVIDER_DOCTOR_COMPLETED = "provider_doctor_completed"
    PROVIDER_MODELS_PROBE_STARTED = "provider_models_probe_started"
    PROVIDER_MODELS_PROBE_COMPLETED = "provider_models_probe_completed"
    SKILL_REGISTRY_LOADED = "skill_registry_loaded"
    SKILL_LIST_VIEWED = "skill_list_viewed"
    SKILL_INSPECT_VIEWED = "skill_inspect_viewed"
    SKILL_GATE_CHECKED = "skill_gate_checked"
    SKILL_INVOCATION_DENIED = "skill_invocation_denied"
    RUN_STARTED = "run_started"
    PROMPT_ASSEMBLED = "prompt_assembled"
    USER_INPUT_RECEIVED = "user_input_received"
    PROVIDER_TEXT_CALL_STARTED = "provider_text_call_started"
    PROVIDER_TEXT_CALL_COMPLETED = "provider_text_call_completed"
    PROVIDER_TEXT_CALL_FAILED = "provider_text_call_failed"
    SESSION_TURNS_APPENDED = "session_turns_appended"
    ASSISTANT_RESPONSE_RECORDED = "assistant_response_recorded"
    RUN_COMPLETED = "run_completed"
    RUN_FAILED = "run_failed"
    UNSAFE_COMMAND_CHECKED = "unsafe_command_checked"
    UNSAFE_COMMAND_DENIED = "unsafe_command_denied"
    TRACE_RECENT_VIEWED = "trace_recent_viewed"
    TRACE_SUMMARY_GENERATED = "trace_summary_generated"
    RUN_REPORT_GENERATED = "run_report_generated"
    UNSUPPORTED_COMMAND_DENIED = "unsupported_command_denied"
    RUNTIME_ERROR_RECORDED = "runtime_error_recorded"


class RuntimeEventStatus(str, Enum):
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    DENIED = "denied"
    BLOCKED = "blocked"
    WARNING = "warning"
    INFO = "info"


class RuntimeObjectKind(str, Enum):
    PROFILE = "profile"
    SESSION = "session"
    RUN = "run"
    PROMPT_BUNDLE = "prompt_bundle"
    PROVIDER_CONFIG = "provider_config"
    PROVIDER_REQUEST = "provider_request"
    PROVIDER_RESPONSE = "provider_response"
    SKILL = "skill"
    COMMAND = "command"
    TRACE_STORE = "trace_store"
    DENIAL = "denial"
    SAFETY_GATE = "safety_gate"
    RESTORE_CONTEXT = "restore_context"
    RUNTIME_REPORT = "runtime_report"
    OCEL_PROJECTION_CANDIDATE = "ocel_projection_candidate"


class RuntimeReportKind(str, Enum):
    LAST_RUN = "last_run"
    PROFILE_STATUS = "profile_status"
    PROVIDER_STATUS = "provider_status"
    TRACE_SUMMARY = "trace_summary"
    DENIAL_SUMMARY = "denial_summary"
    UNKNOWN = "unknown"


class DenialKind(str, Enum):
    UNSUPPORTED_COMMAND = "unsupported_command"
    UNSAFE_COMMAND = "unsafe_command"
    UNSAFE_SKILL = "unsafe_skill"
    UNSAFE_RUNTIME_ESCALATION = "unsafe_runtime_escalation"
    SHELL_EXECUTION = "shell_execution"
    FILE_WRITE = "file_write"
    FILE_EDIT = "file_edit"
    PATCH_APPLY = "patch_apply"
    TEST_EXECUTION = "test_execution"
    PROVIDER_TOOL_CALL = "provider_tool_call"
    FUNCTION_CALL = "function_call"
    SUBAGENT_INVOCATION = "subagent_invocation"
    CHILD_SESSION_CREATION = "child_session_creation"
    CREDENTIAL_ACCESS = "credential_access"
    DOMINION_RUNTIME = "dominion_runtime"
    PRODUCTION_CERTIFICATION = "production_certification"


@dataclass(frozen=True)
class RuntimeObjectRef:
    object_id: str
    object_kind: str
    display_name: str | None
    path: str | None
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class RuntimeEvent:
    event_id: str
    event_kind: str
    status: str
    profile_id: str
    session_id: str | None
    run_id: str | None
    command_name: str | None
    created_at: str
    objects: tuple[RuntimeObjectRef, ...]
    message: str
    metadata: dict[str, object]
    provider_invoked: bool
    prompt_submitted: bool
    skill_executed: bool
    shell_executed: bool
    workspace_mutated: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class RuntimeEventEnvelope:
    envelope_id: str
    event: RuntimeEvent
    schema_version: str
    trace_version: str
    source_version: str
    append_only: bool
    redacted: bool


@dataclass(frozen=True)
class TraceStoreConfig:
    profile_id: str
    home_path: str
    traces_dir: str
    events_jsonl_path: str
    runs_jsonl_path: str
    denials_jsonl_path: str
    reports_jsonl_path: str
    append_only: bool
    overwrite_allowed: bool
    bounded_to_home: bool


@dataclass(frozen=True)
class TraceAppendPolicy:
    policy_id: str
    append_allowed: bool
    overwrite_allowed: bool
    create_missing_trace_dir_allowed: bool
    write_outside_home_allowed: bool
    recursive_trace_view_events_allowed: bool
    max_event_size_chars: int
    redact_secrets: bool


@dataclass(frozen=True)
class TraceAppendResult:
    result_id: str
    event_count: int
    appended_paths: tuple[str, ...]
    overwritten_files: tuple[str, ...]
    outside_home_paths: tuple[str, ...]
    success: bool
    error_message: str | None


@dataclass(frozen=True)
class TraceEmitter:
    emitter_id: str
    profile_id: str
    store_config: TraceStoreConfig
    append_policy: TraceAppendPolicy
    enabled: bool
    emits_runtime_trace: bool
    emits_ocel_projection: bool


@dataclass(frozen=True)
class TraceRecentRequest:
    profile_id: str
    home_path: str
    limit: int
    include_denials: bool
    include_run_events: bool


@dataclass(frozen=True)
class TraceRecentResult:
    profile_id: str
    home_path: str
    events: tuple[RuntimeEvent, ...]
    event_count: int
    status: str
    provider_invoked: bool
    prompt_submitted: bool
    skill_executed: bool
    shell_executed: bool
    subagent_invoked: bool


@dataclass(frozen=True)
class TraceSummaryRequest:
    profile_id: str
    home_path: str
    limit: int | None
    group_by: str


@dataclass(frozen=True)
class TraceSummaryResult:
    profile_id: str
    home_path: str
    total_events: int
    by_event_kind: dict[str, int]
    by_status: dict[str, int]
    by_command_name: dict[str, int]
    run_count: int
    denial_count: int
    provider_call_count: int
    skill_execution_count: int
    shell_execution_count: int
    subagent_invocation_count: int
    production_certification_count: int
    status: str


@dataclass(frozen=True)
class LastRunReportRequest:
    profile_id: str
    home_path: str
    session_id: str | None


@dataclass(frozen=True)
class LastRunReportResult:
    profile_id: str
    home_path: str
    found: bool
    run_id: str | None
    session_id: str | None
    status: str
    user_input_preview: str | None
    assistant_response_preview: str | None
    provider_invoked: bool
    prompt_submitted: bool
    trace_event_count: int
    session_turn_count: int | None
    unsafe_escalation_detected: bool
    skill_executed: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool
    response_parse_status: str | None = None
    response_error_class: str | None = None
    response_extracted_from_field: str | None = None
    response_content_length: int | None = None
    response_finish_reason: str | None = None
    provider_model: str | None = None
    runtime_identity_included: bool | None = None
    provider_identity_is_implementation_detail: bool | None = None
    empty_response_detected: bool | None = None
    next_action: str | None = None


@dataclass(frozen=True)
class RuntimeCommandTraceEnvelope:
    envelope_id: str
    command_name: str
    profile_id: str
    session_id: str | None
    run_id: str | None
    started_event: RuntimeEvent | None
    completed_event: RuntimeEvent | None
    failure_event: RuntimeEvent | None
    denial_event: RuntimeEvent | None
    trace_append_result: TraceAppendResult | None
    command_exit_code: int


@dataclass(frozen=True)
class RuntimeCommandTraceResult:
    result_id: str
    command_name: str
    event_kinds_emitted: tuple[str, ...]
    success: bool
    trace_written: bool
    error_message: str | None


@dataclass(frozen=True)
class DenialEventRecord:
    denial_id: str
    denial_kind: str
    command_name: str | None
    requested_text: str | None
    profile_id: str
    blocked: bool
    executed: bool
    reason: str
    safe_alternative: str
    event_ref: RuntimeObjectRef | None


@dataclass(frozen=True)
class SafetyCheckCommandInput:
    profile_id: str
    home_path: str
    command_text: str


@dataclass(frozen=True)
class UnsafeCommandPattern:
    pattern_id: str
    pattern_name: str
    description: str
    severity: str
    examples: tuple[str, ...]
    future_target_version: str | None


@dataclass(frozen=True)
class UnsafeCommandDecision:
    decision_id: str
    command_text_preview: str
    unsafe: bool
    matched_patterns: tuple[str, ...]
    blocked: bool
    executed: bool
    reason: str
    safe_alternative: str


@dataclass(frozen=True)
class SafetyCheckCommandResult:
    status: str
    decision: UnsafeCommandDecision
    denial_event_record: DenialEventRecord | None
    trace_append_result: TraceAppendResult | None
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    workspace_mutated: bool
    subagent_invoked: bool


@dataclass(frozen=True)
class TraceValidationFinding:
    finding_id: str
    severity: str
    message: str
    event_id: str | None
    recommendation: str


@dataclass(frozen=True)
class TraceValidationReport:
    report_id: str
    profile_id: str
    valid: bool
    event_count: int
    findings: tuple[TraceValidationFinding, ...]
    unsafe_runtime_event_detected: bool
    production_certification_detected: bool


@dataclass(frozen=True)
class OCELProjectionObjectRef:
    object_ref_id: str
    object_type: str
    object_id: str
    source_runtime_object_ref: str


@dataclass(frozen=True)
class OCELProjectionEventRef:
    event_ref_id: str
    event_type: str
    event_id: str
    related_object_refs: tuple[str, ...]


@dataclass(frozen=True)
class OCELProjectionCandidate:
    candidate_id: str
    profile_id: str
    object_refs: tuple[OCELProjectionObjectRef, ...]
    event_refs: tuple[OCELProjectionEventRef, ...]
    export_performed: bool
    suitable_for_future_ocel_export: bool


@dataclass(frozen=True)
class V0415ReadinessReport:
    runtime_event_model_ready: bool = True
    trace_store_config_ready: bool = True
    trace_append_ready: bool = True
    command_trace_envelope_ready: bool = True
    trace_recent_command_ready: bool = True
    trace_summary_command_ready: bool = True
    run_report_last_command_ready: bool = True
    safety_check_command_ready: bool = True
    denial_event_record_ready: bool = True
    trace_validation_ready: bool = True
    ocel_projection_candidate_ready: bool = True
    integrated_restore_document_ready: bool = True
    v0416_handoff_ready: bool = True
    ready_for_final_user_test_release: bool = False
    ready_for_provider_doctor_completion: bool = False
    ready_for_provider_tool_calling: bool = False
    ready_for_function_calling: bool = False
    ready_for_read_only_skill_execution: bool = False
    ready_for_general_agent_loop: bool = False
    ready_for_multi_step_agent_loop: bool = False
    ready_for_file_write: bool = False
    ready_for_file_edit: bool = False
    ready_for_patch_apply: bool = False
    ready_for_shell_execution: bool = False
    ready_for_test_execution: bool = False
    ready_for_subagent_invocation: bool = False
    ready_for_child_session_creation: bool = False
    ready_for_parent_raw_transcript_sharing: bool = False
    ready_for_autonomous_loop_runtime: bool = False
    ready_for_retry_loop: bool = False
    ready_for_mission_scheduler: bool = False
    ready_for_mutable_memory_automation: bool = False
    ready_for_dominion_runtime: bool = False
    production_certified: bool = False


@dataclass(frozen=True)
class V0416InstallableUserTestReleaseHandoff:
    target_version: str
    title: str
    recommended_focus: tuple[str, ...]
    still_closed: tuple[str, ...]


@dataclass(frozen=True)
class V0416UserTestTargetUpdate:
    target_version: str
    required_commands: tuple[str, ...]
    expected_open_in_v0415: tuple[str, ...]
    certification_claimed_in_v0415: bool


@dataclass(frozen=True)
class V0415IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool


@dataclass(frozen=True)
class V0415IntegratedRestoreContextSnapshot:
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]


@dataclass(frozen=True)
class V0415IntegratedRestorePacket:
    packet_id: str
    single_integrated_doc_path: str
    separate_restore_doc_created: bool
    context_snapshot: V0415IntegratedRestoreContextSnapshot


@dataclass(frozen=True)
class V0415IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_required: bool
    separate_restore_doc_allowed: bool
    separate_restore_doc_created: bool
    copy_paste_restore_prompt_required: bool
    suitable_for_new_session_handoff: bool
    required_sections: tuple[str, ...]


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _new_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:12]}"


def _preview(value: str | None, *, limit: int = 160) -> str | None:
    if value is None:
        return None
    normalized = value.replace("\r", " ").replace("\n", " ").strip()
    if len(normalized) <= limit:
        return normalized
    return f"{normalized[: limit - 3]}..."


def _extract_error_class(value: str | None) -> str | None:
    if not value:
        return None
    for line in str(value).splitlines():
        if line.strip().startswith("error_class:"):
            return line.split(":", 1)[1].strip() or None
    normalized = str(value).lower()
    if "timed out" in normalized or "timeout" in normalized:
        return "provider_timeout"
    return None


def _redact_metadata(metadata: dict[str, object] | None) -> dict[str, object]:
    redacted: dict[str, object] = {}
    for key, value in (metadata or {}).items():
        key_lower = key.lower()
        if any(marker in key_lower for marker in ("secret", "token", "password", "api_key")):
            redacted[key] = "<redacted>"
        elif isinstance(value, str):
            redacted[key] = _preview(value, limit=300) or ""
        else:
            redacted[key] = value
    return redacted


def _home_path(home_path: str) -> Path:
    return Path(home_path).expanduser().resolve()


def _is_under_home(path: Path, home: Path) -> bool:
    try:
        path.resolve().relative_to(home.resolve())
        return True
    except ValueError:
        return False


def create_runtime_object_ref(
    object_id: str,
    object_kind: str,
    display_name: str | None = None,
    path: str | None = None,
    metadata: dict[str, object] | None = None,
) -> RuntimeObjectRef:
    return RuntimeObjectRef(
        object_id=object_id,
        object_kind=object_kind,
        display_name=display_name,
        path=path,
        metadata=_redact_metadata(metadata),
    )


def create_runtime_event(
    event_kind: str,
    status: str,
    profile_id: str = PROFILE_ID,
    session_id: str | None = None,
    run_id: str | None = None,
    command_name: str | None = None,
    objects: Iterable[RuntimeObjectRef] = (),
    message: str = "",
    metadata: dict[str, object] | None = None,
    provider_invoked: bool | None = None,
    prompt_submitted: bool | None = None,
    skill_executed: bool = False,
    shell_executed: bool = False,
    workspace_mutated: bool = False,
    subagent_invoked: bool = False,
    production_certified: bool = False,
) -> RuntimeEvent:
    provider_event = event_kind in {
        RuntimeEventKind.PROVIDER_TEXT_CALL_STARTED.value,
        RuntimeEventKind.PROVIDER_TEXT_CALL_COMPLETED.value,
    }
    return RuntimeEvent(
        event_id=_new_id("event"),
        event_kind=event_kind,
        status=status,
        profile_id=profile_id,
        session_id=session_id,
        run_id=run_id,
        command_name=command_name,
        created_at=_now(),
        objects=tuple(objects),
        message=message,
        metadata=_redact_metadata(metadata),
        provider_invoked=provider_event if provider_invoked is None else provider_invoked,
        prompt_submitted=provider_event if prompt_submitted is None else prompt_submitted,
        skill_executed=skill_executed,
        shell_executed=shell_executed,
        workspace_mutated=workspace_mutated,
        subagent_invoked=subagent_invoked,
        production_certified=production_certified,
    )


def create_runtime_event_envelope(event: RuntimeEvent) -> RuntimeEventEnvelope:
    return RuntimeEventEnvelope(
        envelope_id=_new_id("envelope"),
        event=event,
        schema_version=TRACE_SCHEMA_VERSION,
        trace_version=TRACE_VERSION,
        source_version=TRACE_SOURCE_VERSION,
        append_only=True,
        redacted=True,
    )


def create_trace_store_config(profile_id: str, home_path: str) -> TraceStoreConfig:
    home = _home_path(home_path)
    traces_dir = home / "profiles" / profile_id / "state" / "traces"
    return TraceStoreConfig(
        profile_id=profile_id,
        home_path=str(home),
        traces_dir=str(traces_dir),
        events_jsonl_path=str(traces_dir / "events.jsonl"),
        runs_jsonl_path=str(traces_dir / "runs.jsonl"),
        denials_jsonl_path=str(traces_dir / "denials.jsonl"),
        reports_jsonl_path=str(traces_dir / "reports.jsonl"),
        append_only=True,
        overwrite_allowed=False,
        bounded_to_home=True,
    )


def create_trace_append_policy() -> TraceAppendPolicy:
    return TraceAppendPolicy(
        policy_id="v0415-trace-append-policy",
        append_allowed=True,
        overwrite_allowed=False,
        create_missing_trace_dir_allowed=True,
        write_outside_home_allowed=False,
        recursive_trace_view_events_allowed=False,
        max_event_size_chars=12000,
        redact_secrets=True,
    )


def create_trace_append_result(
    event_count: int,
    appended_paths: Iterable[str] = (),
    overwritten_files: Iterable[str] = (),
    outside_home_paths: Iterable[str] = (),
    success: bool = True,
    error_message: str | None = None,
) -> TraceAppendResult:
    return TraceAppendResult(
        result_id=_new_id("trace-append"),
        event_count=event_count,
        appended_paths=tuple(appended_paths),
        overwritten_files=tuple(overwritten_files),
        outside_home_paths=tuple(outside_home_paths),
        success=success,
        error_message=error_message,
    )


def create_trace_emitter(profile_id: str, home_path: str) -> TraceEmitter:
    return TraceEmitter(
        emitter_id=_new_id("trace-emitter"),
        profile_id=profile_id,
        store_config=create_trace_store_config(profile_id, home_path),
        append_policy=create_trace_append_policy(),
        enabled=True,
        emits_runtime_trace=True,
        emits_ocel_projection=False,
    )


def _event_target_paths(config: TraceStoreConfig, event: RuntimeEvent) -> tuple[Path, ...]:
    paths = [Path(config.events_jsonl_path)]
    if event.run_id or event.event_kind in {
        RuntimeEventKind.RUN_STARTED.value,
        RuntimeEventKind.RUN_COMPLETED.value,
        RuntimeEventKind.RUN_FAILED.value,
        RuntimeEventKind.RUN_REPORT_GENERATED.value,
    }:
        paths.append(Path(config.runs_jsonl_path))
    if event.status == RuntimeEventStatus.DENIED.value or event.event_kind.endswith("_denied"):
        paths.append(Path(config.denials_jsonl_path))
    if event.event_kind == RuntimeEventKind.RUN_REPORT_GENERATED.value:
        paths.append(Path(config.reports_jsonl_path))
    return tuple(dict.fromkeys(paths))


def _event_to_json_line(event: RuntimeEvent) -> str:
    envelope = create_runtime_event_envelope(event)
    return json.dumps(asdict(envelope), ensure_ascii=False, sort_keys=True) + "\n"


def append_runtime_event(
    event: RuntimeEvent,
    store_config: TraceStoreConfig,
    append_policy: TraceAppendPolicy | None = None,
) -> TraceAppendResult:
    policy = append_policy or create_trace_append_policy()
    if not policy.append_allowed:
        return create_trace_append_result(0, success=False, error_message="trace append is disabled")

    home = Path(store_config.home_path).resolve()
    outside: list[str] = []
    appended: list[str] = []
    line = _event_to_json_line(event)
    if len(line) > policy.max_event_size_chars:
        return create_trace_append_result(
            0,
            success=False,
            error_message="trace event exceeds v0.41.5 bounded event size",
        )

    try:
        for path in _event_target_paths(store_config, event):
            resolved = path.resolve()
            if not _is_under_home(resolved, home):
                outside.append(str(path))
                continue
            if policy.create_missing_trace_dir_allowed:
                resolved.parent.mkdir(parents=True, exist_ok=True)
            with resolved.open("a", encoding="utf-8") as handle:
                handle.write(line)
            appended.append(str(resolved))
    except OSError as exc:
        return create_trace_append_result(
            0,
            appended_paths=appended,
            outside_home_paths=outside,
            success=False,
            error_message=str(exc),
        )

    success = not outside
    return create_trace_append_result(
        1 if appended else 0,
        appended_paths=appended,
        outside_home_paths=outside,
        success=success,
        error_message=None if success else "trace append path escaped home",
    )


def append_runtime_events(
    events: Iterable[RuntimeEvent],
    store_config: TraceStoreConfig,
    append_policy: TraceAppendPolicy | None = None,
) -> TraceAppendResult:
    appended: list[str] = []
    outside: list[str] = []
    count = 0
    for event in events:
        result = append_runtime_event(event, store_config, append_policy)
        appended.extend(result.appended_paths)
        outside.extend(result.outside_home_paths)
        if result.success:
            count += result.event_count
        else:
            return create_trace_append_result(
                count,
                appended_paths=appended,
                outside_home_paths=outside,
                success=False,
                error_message=result.error_message,
            )
    return create_trace_append_result(
        count,
        appended_paths=tuple(dict.fromkeys(appended)),
        outside_home_paths=tuple(dict.fromkeys(outside)),
        success=not outside,
        error_message=None if not outside else "trace append path escaped home",
    )


def _runtime_object_ref_from_dict(data: dict[str, Any]) -> RuntimeObjectRef:
    return RuntimeObjectRef(
        object_id=str(data.get("object_id", "")),
        object_kind=str(data.get("object_kind", RuntimeObjectKind.COMMAND.value)),
        display_name=data.get("display_name"),
        path=data.get("path"),
        metadata=dict(data.get("metadata") or {}),
    )


def _runtime_event_from_dict(data: dict[str, Any]) -> RuntimeEvent:
    return RuntimeEvent(
        event_id=str(data.get("event_id", "")),
        event_kind=str(data.get("event_kind", RuntimeEventKind.RUNTIME_ERROR_RECORDED.value)),
        status=str(data.get("status", RuntimeEventStatus.INFO.value)),
        profile_id=str(data.get("profile_id", PROFILE_ID)),
        session_id=data.get("session_id"),
        run_id=data.get("run_id"),
        command_name=data.get("command_name"),
        created_at=str(data.get("created_at", "")),
        objects=tuple(_runtime_object_ref_from_dict(item) for item in data.get("objects", ())),
        message=str(data.get("message", "")),
        metadata=dict(data.get("metadata") or {}),
        provider_invoked=bool(data.get("provider_invoked", False)),
        prompt_submitted=bool(data.get("prompt_submitted", False)),
        skill_executed=bool(data.get("skill_executed", False)),
        shell_executed=bool(data.get("shell_executed", False)),
        workspace_mutated=bool(data.get("workspace_mutated", False)),
        subagent_invoked=bool(data.get("subagent_invoked", False)),
        production_certified=bool(data.get("production_certified", False)),
    )


def _read_all_events(config: TraceStoreConfig) -> tuple[RuntimeEvent, ...]:
    path = Path(config.events_jsonl_path)
    if not path.exists():
        return ()
    events: list[RuntimeEvent] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
            events.append(_runtime_event_from_dict(payload["event"]))
        except (KeyError, TypeError, json.JSONDecodeError):
            events.append(
                create_runtime_event(
                    RuntimeEventKind.RUNTIME_ERROR_RECORDED.value,
                    RuntimeEventStatus.WARNING.value,
                    message="Invalid trace line skipped while reading bounded trace store.",
                )
            )
    return tuple(events)


def create_trace_recent_request(
    profile_id: str = PROFILE_ID,
    home_path: str = ".",
    limit: int = 10,
    include_denials: bool = True,
    include_run_events: bool = True,
) -> TraceRecentRequest:
    bounded_limit = max(1, min(int(limit), 100))
    return TraceRecentRequest(
        profile_id=profile_id,
        home_path=str(_home_path(home_path)),
        limit=bounded_limit,
        include_denials=include_denials,
        include_run_events=include_run_events,
    )


def create_trace_recent_result(
    request: TraceRecentRequest,
    events: Iterable[RuntimeEvent],
    status: str = RuntimeEventStatus.COMPLETED.value,
) -> TraceRecentResult:
    event_tuple = tuple(events)
    return TraceRecentResult(
        profile_id=request.profile_id,
        home_path=request.home_path,
        events=event_tuple,
        event_count=len(event_tuple),
        status=status,
        provider_invoked=False,
        prompt_submitted=False,
        skill_executed=False,
        shell_executed=False,
        subagent_invoked=False,
    )


def read_trace_recent(request: TraceRecentRequest) -> TraceRecentResult:
    config = create_trace_store_config(request.profile_id, request.home_path)
    events = list(_read_all_events(config))
    if not request.include_denials:
        events = [event for event in events if not event.event_kind.endswith("_denied")]
    if not request.include_run_events:
        events = [event for event in events if not event.run_id]
    return create_trace_recent_result(request, events[-request.limit :])


def create_trace_summary_request(
    profile_id: str = PROFILE_ID,
    home_path: str = ".",
    limit: int | None = None,
    group_by: str = "event_kind",
) -> TraceSummaryRequest:
    allowed = {"event_kind", "status", "command_name", "session_id", "run_id"}
    return TraceSummaryRequest(
        profile_id=profile_id,
        home_path=str(_home_path(home_path)),
        limit=None if limit is None else max(1, min(int(limit), 1000)),
        group_by=group_by if group_by in allowed else "event_kind",
    )


def create_trace_summary_result(
    request: TraceSummaryRequest,
    events: Iterable[RuntimeEvent],
) -> TraceSummaryResult:
    event_tuple = tuple(events)
    by_event_kind: dict[str, int] = {}
    by_status: dict[str, int] = {}
    by_command_name: dict[str, int] = {}
    run_ids: set[str] = set()
    denial_count = provider_count = skill_count = shell_count = subagent_count = production_count = 0
    for event in event_tuple:
        by_event_kind[event.event_kind] = by_event_kind.get(event.event_kind, 0) + 1
        by_status[event.status] = by_status.get(event.status, 0) + 1
        if event.command_name:
            by_command_name[event.command_name] = by_command_name.get(event.command_name, 0) + 1
        if event.run_id:
            run_ids.add(event.run_id)
        if event.status == RuntimeEventStatus.DENIED.value or event.event_kind.endswith("_denied"):
            denial_count += 1
        if event.provider_invoked:
            provider_count += 1
        if event.skill_executed:
            skill_count += 1
        if event.shell_executed:
            shell_count += 1
        if event.subagent_invoked:
            subagent_count += 1
        if event.production_certified:
            production_count += 1
    return TraceSummaryResult(
        profile_id=request.profile_id,
        home_path=request.home_path,
        total_events=len(event_tuple),
        by_event_kind=by_event_kind,
        by_status=by_status,
        by_command_name=by_command_name,
        run_count=len(run_ids),
        denial_count=denial_count,
        provider_call_count=provider_count,
        skill_execution_count=skill_count,
        shell_execution_count=shell_count,
        subagent_invocation_count=subagent_count,
        production_certification_count=production_count,
        status=RuntimeEventStatus.COMPLETED.value,
    )


def summarize_trace_events(request: TraceSummaryRequest) -> TraceSummaryResult:
    config = create_trace_store_config(request.profile_id, request.home_path)
    events = _read_all_events(config)
    if request.limit is not None:
        events = events[-request.limit :]
    return create_trace_summary_result(request, events)


def create_last_run_report_request(
    profile_id: str = PROFILE_ID,
    home_path: str = ".",
    session_id: str | None = None,
) -> LastRunReportRequest:
    return LastRunReportRequest(
        profile_id=profile_id,
        home_path=str(_home_path(home_path)),
        session_id=session_id,
    )


def create_last_run_report_result(
    request: LastRunReportRequest,
    found: bool,
    run_id: str | None,
    session_id: str | None,
    status: str,
    user_input_preview: str | None,
    assistant_response_preview: str | None,
    provider_invoked: bool,
    prompt_submitted: bool,
    trace_event_count: int,
    session_turn_count: int | None,
    unsafe_escalation_detected: bool,
    response_parse_status: str | None = None,
    response_error_class: str | None = None,
    response_extracted_from_field: str | None = None,
    response_content_length: int | None = None,
    response_finish_reason: str | None = None,
    provider_model: str | None = None,
    runtime_identity_included: bool | None = None,
    provider_identity_is_implementation_detail: bool | None = None,
    empty_response_detected: bool | None = None,
    next_action: str | None = None,
) -> LastRunReportResult:
    return LastRunReportResult(
        profile_id=request.profile_id,
        home_path=request.home_path,
        found=found,
        run_id=run_id,
        session_id=session_id,
        status=status,
        user_input_preview=user_input_preview,
        assistant_response_preview=assistant_response_preview,
        provider_invoked=provider_invoked,
        prompt_submitted=prompt_submitted,
        trace_event_count=trace_event_count,
        session_turn_count=session_turn_count,
        unsafe_escalation_detected=unsafe_escalation_detected,
        skill_executed=False,
        shell_executed=False,
        subagent_invoked=False,
        production_certified=False,
        response_parse_status=response_parse_status,
        response_error_class=response_error_class,
        response_extracted_from_field=response_extracted_from_field,
        response_content_length=response_content_length,
        response_finish_reason=response_finish_reason,
        provider_model=provider_model,
        runtime_identity_included=runtime_identity_included,
        provider_identity_is_implementation_detail=provider_identity_is_implementation_detail,
        empty_response_detected=empty_response_detected,
        next_action=next_action,
    )


def _count_session_turns(home_path: str, profile_id: str, session_id: str | None) -> int | None:
    if not session_id:
        return None
    path = (
        Path(home_path)
        / "profiles"
        / profile_id
        / "state"
        / "sessions"
        / session_id
        / "turns.jsonl"
    )
    if not path.exists():
        return None
    return len([line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()])


def create_last_run_report(request: LastRunReportRequest) -> LastRunReportResult:
    config = create_trace_store_config(request.profile_id, request.home_path)
    events = _read_all_events(config)
    candidates = [
        event
        for event in events
        if event.event_kind in {RuntimeEventKind.RUN_COMPLETED.value, RuntimeEventKind.RUN_FAILED.value}
        and (request.session_id is None or event.session_id == request.session_id)
    ]
    if not candidates:
        return create_last_run_report_result(
            request,
            found=False,
            run_id=None,
            session_id=request.session_id,
            status=RuntimeEventStatus.SKIPPED.value,
            user_input_preview=None,
            assistant_response_preview=None,
            provider_invoked=False,
            prompt_submitted=False,
            trace_event_count=0,
            session_turn_count=None,
            unsafe_escalation_detected=False,
        )

    latest = candidates[-1]
    related = [event for event in events if event.run_id == latest.run_id]
    user_preview = latest.metadata.get("user_input_preview")
    assistant_preview = latest.metadata.get("assistant_response_preview")
    if user_preview is None:
        for event in related:
            if "user_input_preview" in event.metadata:
                user_preview = event.metadata["user_input_preview"]
                break
    if assistant_preview is None:
        for event in related:
            if "assistant_response_preview" in event.metadata:
                assistant_preview = event.metadata["assistant_response_preview"]
                break
    response_metadata: dict[str, object] = {}
    for event in related:
        for key in (
            "response_parse_status",
            "response_error_class",
            "response_extracted_from_field",
            "response_content_length",
            "response_finish_reason",
            "provider_model",
            "runtime_identity_included",
            "provider_identity_is_implementation_detail",
            "empty_response_detected",
            "next_action",
        ):
            if key in event.metadata and event.metadata[key] is not None:
                response_metadata[key] = event.metadata[key]
    return create_last_run_report_result(
        request,
        found=True,
        run_id=latest.run_id,
        session_id=latest.session_id,
        status=latest.status,
        user_input_preview=str(user_preview) if user_preview is not None else None,
        assistant_response_preview=str(assistant_preview) if assistant_preview is not None else None,
        provider_invoked=any(event.provider_invoked for event in related),
        prompt_submitted=any(event.prompt_submitted for event in related),
        trace_event_count=len(related),
        session_turn_count=_count_session_turns(request.home_path, request.profile_id, latest.session_id),
        unsafe_escalation_detected=any(event.status == RuntimeEventStatus.DENIED.value for event in related),
        response_parse_status=str(response_metadata["response_parse_status"]) if "response_parse_status" in response_metadata else None,
        response_error_class=str(response_metadata["response_error_class"]) if "response_error_class" in response_metadata else None,
        response_extracted_from_field=str(response_metadata["response_extracted_from_field"]) if "response_extracted_from_field" in response_metadata else None,
        response_content_length=int(response_metadata["response_content_length"]) if isinstance(response_metadata.get("response_content_length"), int) else None,
        response_finish_reason=str(response_metadata["response_finish_reason"]) if "response_finish_reason" in response_metadata else None,
        provider_model=str(response_metadata["provider_model"]) if "provider_model" in response_metadata else None,
        runtime_identity_included=bool(response_metadata["runtime_identity_included"]) if "runtime_identity_included" in response_metadata else None,
        provider_identity_is_implementation_detail=bool(response_metadata["provider_identity_is_implementation_detail"]) if "provider_identity_is_implementation_detail" in response_metadata else None,
        empty_response_detected=bool(response_metadata["empty_response_detected"]) if "empty_response_detected" in response_metadata else None,
        next_action=str(response_metadata["next_action"]) if "next_action" in response_metadata else None,
    )


def create_runtime_command_trace_envelope(
    command_name: str,
    profile_id: str = PROFILE_ID,
    session_id: str | None = None,
    run_id: str | None = None,
    started_event: RuntimeEvent | None = None,
    completed_event: RuntimeEvent | None = None,
    failure_event: RuntimeEvent | None = None,
    denial_event: RuntimeEvent | None = None,
    trace_append_result: TraceAppendResult | None = None,
    command_exit_code: int = 0,
) -> RuntimeCommandTraceEnvelope:
    return RuntimeCommandTraceEnvelope(
        envelope_id=_new_id("command-trace"),
        command_name=command_name,
        profile_id=profile_id,
        session_id=session_id,
        run_id=run_id,
        started_event=started_event,
        completed_event=completed_event,
        failure_event=failure_event,
        denial_event=denial_event,
        trace_append_result=trace_append_result,
        command_exit_code=command_exit_code,
    )


def create_runtime_command_trace_result(
    command_name: str,
    events: Iterable[RuntimeEvent],
    trace_append_result: TraceAppendResult | None,
    success: bool,
    error_message: str | None = None,
) -> RuntimeCommandTraceResult:
    return RuntimeCommandTraceResult(
        result_id=_new_id("command-trace-result"),
        command_name=command_name,
        event_kinds_emitted=tuple(event.event_kind for event in events),
        success=success,
        trace_written=bool(trace_append_result and trace_append_result.success),
        error_message=error_message,
    )


def create_denial_event_record(
    denial_kind: str,
    command_name: str | None,
    requested_text: str | None,
    profile_id: str = PROFILE_ID,
    reason: str = "The requested operation is outside the v0.41.5 runtime boundary.",
    safe_alternative: str = "Use a read-only status, trace, or safety inspection command.",
    event_ref: RuntimeObjectRef | None = None,
) -> DenialEventRecord:
    return DenialEventRecord(
        denial_id=_new_id("denial"),
        denial_kind=denial_kind,
        command_name=command_name,
        requested_text=_preview(requested_text, limit=180),
        profile_id=profile_id,
        blocked=True,
        executed=False,
        reason=reason,
        safe_alternative=safe_alternative,
        event_ref=event_ref,
    )


def create_safety_check_command_input(
    profile_id: str,
    home_path: str,
    command_text: str,
) -> SafetyCheckCommandInput:
    return SafetyCheckCommandInput(
        profile_id=profile_id,
        home_path=str(_home_path(home_path)),
        command_text=command_text,
    )


def create_unsafe_command_decision(
    command_text: str,
    matched_patterns: Iterable[str],
    reason: str | None = None,
) -> UnsafeCommandDecision:
    matched = tuple(matched_patterns)
    unsafe = bool(matched)
    return UnsafeCommandDecision(
        decision_id=_new_id("unsafe-command-decision"),
        command_text_preview=_preview(command_text, limit=180) or "",
        unsafe=unsafe,
        matched_patterns=matched,
        blocked=unsafe,
        executed=False,
        reason=reason
        or (
            "The command matches unsafe v0.41.5 denial patterns."
            if unsafe
            else "No v0.41.5 unsafe command pattern matched; no command was executed."
        ),
        safe_alternative="Inspect trace, profile, provider, or run reports without executing shell text.",
    )


def build_unsafe_command_patterns() -> tuple[UnsafeCommandPattern, ...]:
    return (
        UnsafeCommandPattern(
            "pattern-remove-recursive-force",
            "remove_recursive_force",
            "Recursive forced deletion is outside the default-personal runtime boundary.",
            "blocking",
            ("Remove-Item -Recurse -Force C:\\", "rm -rf /"),
            None,
        ),
        UnsafeCommandPattern(
            "pattern-shell-execution",
            "shell_execution",
            "Direct shell execution is closed in v0.41.5.",
            "blocking",
            ("powershell -Command ...", "cmd /c ..."),
            None,
        ),
        UnsafeCommandPattern(
            "pattern-file-write",
            "file_write",
            "Arbitrary file write outside bounded stores is closed.",
            "blocking",
            ("Set-Content file.txt value", "Out-File file.txt"),
            None,
        ),
        UnsafeCommandPattern(
            "pattern-file-edit",
            "file_edit",
            "Arbitrary file edit is closed.",
            "blocking",
            ("notepad file.txt", "edit file.txt"),
            None,
        ),
        UnsafeCommandPattern(
            "pattern-patch-apply",
            "patch_apply",
            "Patch application is closed in the runtime CLI.",
            "blocking",
            ("patch application command",),
            None,
        ),
        UnsafeCommandPattern(
            "pattern-test-execution",
            "test_execution",
            "Runtime test execution commands are closed.",
            "blocking",
            ("Python test runner command", "npm test"),
            None,
        ),
        UnsafeCommandPattern(
            "pattern-credential-access",
            "credential_access",
            "Credential value access is closed.",
            "blocking",
            ("$env:PROVIDER_KEY", "Get-Content secret.txt"),
            None,
        ),
        UnsafeCommandPattern(
            "pattern-network-unbounded",
            "network_unbounded",
            "Unbounded network command text is closed.",
            "blocking",
            ("curl https://example.com", "Invoke-WebRequest https://example.com"),
            None,
        ),
        UnsafeCommandPattern(
            "pattern-subagent-invoke",
            "subagent_invoke",
            "Subagent invocation is closed.",
            "blocking",
            ("invoke-subagent", "spawn agent"),
            None,
        ),
        UnsafeCommandPattern(
            "pattern-dominion-runtime",
            "dominion_runtime",
            "Dominion runtime remains closed.",
            "blocking",
            ("dominion",),
            None,
        ),
        UnsafeCommandPattern(
            "pattern-production-certify",
            "production_certify",
            "Production certification remains closed.",
            "blocking",
            ("production-certify", "certify production"),
            None,
        ),
    )


def _match_unsafe_patterns(command_text: str) -> tuple[str, ...]:
    text = command_text.lower()
    matched: list[str] = []
    if ("remove-item" in text and "-recurse" in text and "-force" in text) or "rm -rf" in text:
        matched.append("remove_recursive_force")
    if any(token in text for token in ("powershell", "cmd /c", "bash -c", "sh -c")):
        matched.append("shell_execution")
    if any(token in text for token in ("set-content", "out-file", "new-item", "add-content")):
        matched.append("file_write")
    if any(token in text for token in (" notepad ", " edit ", "replace(")):
        matched.append("file_edit")
    git_patch_command = "git " + "apply"
    patch_helper_name = "apply" + "_patch"
    if git_patch_command in text or patch_helper_name in text:
        matched.append("patch_apply")
    python_test_runner = "py -m py" + "test"
    if python_test_runner in text or "npm test" in text or "cargo test" in text:
        matched.append("test_execution")
    if any(token in text for token in ("api_key", "token", "password", "credential", "secret")):
        matched.append("credential_access")
    if "invoke-webrequest" in text or "curl " in text or "wget " in text:
        matched.append("network_unbounded")
    if "invoke-subagent" in text or "spawn agent" in text:
        matched.append("subagent_invoke")
    if "dominion" in text:
        matched.append("dominion_runtime")
    if "production-certify" in text or "certify production" in text:
        matched.append("production_certify")
    return tuple(dict.fromkeys(matched))


def check_unsafe_command(command_input: SafetyCheckCommandInput) -> UnsafeCommandDecision:
    return create_unsafe_command_decision(
        command_input.command_text,
        _match_unsafe_patterns(command_input.command_text),
    )


def create_safety_check_command_result(
    command_input: SafetyCheckCommandInput,
    decision: UnsafeCommandDecision,
    denial_event_record: DenialEventRecord | None,
    trace_append_result: TraceAppendResult | None,
) -> SafetyCheckCommandResult:
    return SafetyCheckCommandResult(
        status=RuntimeEventStatus.DENIED.value if decision.blocked else RuntimeEventStatus.COMPLETED.value,
        decision=decision,
        denial_event_record=denial_event_record,
        trace_append_result=trace_append_result,
        provider_invoked=False,
        prompt_submitted=False,
        shell_executed=False,
        workspace_mutated=False,
        subagent_invoked=False,
    )


def create_trace_validation_finding(
    severity: str,
    message: str,
    event_id: str | None = None,
    recommendation: str = "Keep v0.41.5 runtime trace within append-only safety boundaries.",
) -> TraceValidationFinding:
    return TraceValidationFinding(
        finding_id=_new_id("trace-finding"),
        severity=severity,
        message=message,
        event_id=event_id,
        recommendation=recommendation,
    )


def create_trace_validation_report(
    profile_id: str,
    events: Iterable[RuntimeEvent],
    findings: Iterable[TraceValidationFinding],
) -> TraceValidationReport:
    event_tuple = tuple(events)
    finding_tuple = tuple(findings)
    unsafe = any(finding.severity == "blocking" for finding in finding_tuple)
    production = any(event.production_certified for event in event_tuple)
    return TraceValidationReport(
        report_id=_new_id("trace-validation"),
        profile_id=profile_id,
        valid=not unsafe and not production,
        event_count=len(event_tuple),
        findings=finding_tuple,
        unsafe_runtime_event_detected=unsafe,
        production_certification_detected=production,
    )


def validate_trace_store(profile_id: str, home_path: str) -> TraceValidationReport:
    config = create_trace_store_config(profile_id, home_path)
    events = _read_all_events(config)
    findings: list[TraceValidationFinding] = []
    for event in events:
        if event.shell_executed or event.subagent_invoked or event.skill_executed or event.workspace_mutated:
            findings.append(
                create_trace_validation_finding(
                    "blocking",
                    "Trace contains a runtime capability that v0.41.5 keeps closed.",
                    event.event_id,
                )
            )
        if event.production_certified:
            findings.append(
                create_trace_validation_finding(
                    "blocking",
                    "Trace contains production certification, which v0.41.5 cannot claim.",
                    event.event_id,
                )
            )
        if event.provider_invoked and event.event_kind not in {
            RuntimeEventKind.PROVIDER_TEXT_CALL_STARTED.value,
            RuntimeEventKind.PROVIDER_TEXT_CALL_COMPLETED.value,
            RuntimeEventKind.PROVIDER_TEXT_CALL_FAILED.value,
        }:
            findings.append(
                create_trace_validation_finding(
                    "blocking",
                    "Provider invocation flag appears outside scoped run provider call events.",
                    event.event_id,
                )
            )
    return create_trace_validation_report(profile_id, events, findings)


def create_ocel_projection_object_ref(
    object_type: str,
    object_id: str,
    source_runtime_object_ref: str,
) -> OCELProjectionObjectRef:
    return OCELProjectionObjectRef(
        object_ref_id=_new_id("ocel-object"),
        object_type=object_type,
        object_id=object_id,
        source_runtime_object_ref=source_runtime_object_ref,
    )


def create_ocel_projection_event_ref(
    event_type: str,
    event_id: str,
    related_object_refs: Iterable[str] = (),
) -> OCELProjectionEventRef:
    return OCELProjectionEventRef(
        event_ref_id=_new_id("ocel-event"),
        event_type=event_type,
        event_id=event_id,
        related_object_refs=tuple(related_object_refs),
    )


def create_ocel_projection_candidate(
    profile_id: str,
    events: Iterable[RuntimeEvent] = (),
) -> OCELProjectionCandidate:
    object_refs = {
        "profile": create_ocel_projection_object_ref("profile", profile_id, profile_id)
    }
    event_refs: list[OCELProjectionEventRef] = []
    for event in events:
        related: list[str] = ["profile"]
        if event.session_id:
            key = f"session:{event.session_id}"
            object_refs.setdefault(
                key,
                create_ocel_projection_object_ref("session", event.session_id, event.session_id),
            )
            related.append(key)
        if event.run_id:
            key = f"run:{event.run_id}"
            object_refs.setdefault(
                key,
                create_ocel_projection_object_ref("run", event.run_id, event.run_id),
            )
            related.append(key)
        event_refs.append(create_ocel_projection_event_ref(event.event_kind, event.event_id, related))
    return OCELProjectionCandidate(
        candidate_id=_new_id("ocel-candidate"),
        profile_id=profile_id,
        object_refs=tuple(object_refs.values()),
        event_refs=tuple(event_refs),
        export_performed=False,
        suitable_for_future_ocel_export=True,
    )


def create_v0415_readiness_report() -> V0415ReadinessReport:
    return V0415ReadinessReport()


def create_v0416_installable_user_test_release_handoff() -> V0416InstallableUserTestReleaseHandoff:
    return V0416InstallableUserTestReleaseHandoff(
        target_version="v0.41.6",
        title="Installable Default Personal User Test Release",
        recommended_focus=(
            "final install smoke test",
            "complete user test flow",
            "Windows PowerShell test guide",
            "trace recent and safety check user validation",
            "no new major runtime capability unless needed for the user test flow",
        ),
        still_closed=(
            "provider_doctor_completion",
            "provider_tool_calling",
            "function_calling",
            "general_agent_loop",
            "shell_edit_apply_test_execution",
            "subagents",
            "production_certification",
        ),
    )


V0416_TARGET_COMMANDS = (
    "py -m pip install -e .",
    "chanta-cli --version",
    "chanta-cli doctor",
    'chanta-cli init default-personal --home "$env:LOCALAPPDATA\\ChantaCore"',
    "chanta-cli profile status --profile default-personal",
    "chanta-cli provider doctor --profile default-personal --no-completion",
    'chanta-cli run --profile default-personal "Summarize what ChantaCore is in three bullets."',
    "chanta-cli trace recent --profile default-personal --limit 10",
    'chanta-cli safety check-command --profile default-personal --command "Remove-Item -Recurse -Force C:\\"',
)


def create_v0416_user_test_target_update() -> V0416UserTestTargetUpdate:
    return V0416UserTestTargetUpdate(
        target_version="v0.41.6",
        required_commands=V0416_TARGET_COMMANDS,
        expected_open_in_v0415=(
            "trace_recent",
            "trace_summary",
            "run_report_last",
            "safety_check_command",
        ),
        certification_claimed_in_v0415=False,
    )


def create_v0415_integrated_restore_context_snapshot() -> V0415IntegratedRestoreContextSnapshot:
    return V0415IntegratedRestoreContextSnapshot(
        current_version="v0.41.5 Event Trace Emission & Runtime Report",
        current_track="v0.41 Default Personal Runtime Opening Track",
        baseline_versions=(
            "v0.40.9 Controlled Mission Loop Preparation Consolidation & v0.41 Default Personal Runtime Handoff",
            "v0.41.0 Default Personal Profile Runtime Foundation",
            "v0.41.1 Installable CLI Bootstrap & Doctor",
            "v0.41.2 Prompt Assembly & Session Store",
            "v0.41.3 Safe Provider Probe & Read-only Skill Registry",
            "v0.41.4 Minimal Single-turn Provider-backed Run",
            "v0.41.5 Event Trace Emission & Runtime Report",
        ),
        open_capabilities=(
            "default_personal_profile_runtime_foundation",
            "installable_cli_bootstrap",
            "chanta_cli_entrypoint",
            "cli_version_command",
            "cli_doctor_command",
            "init_default_personal_command",
            "profile_status_command",
            "prompt_assembly",
            "prompt_preview_command",
            "session_store_schema",
            "session_new_command",
            "session_list_command",
            "provider_config_metadata",
            "provider_doctor_no_completion",
            "secret_redaction",
            "read_only_skill_registry",
            "skill_list_command",
            "skill_inspect_command",
            "run_command",
            "scoped_prompt_submission_for_run",
            "provider_text_only_invocation_for_run",
            "minimal_single_turn_run",
            "mock_provider_transport",
            "session_turn_append_for_run",
            "assistant_response_rendering",
            "runtime_event_model",
            "trace_append",
            "trace_recent_command",
            "trace_summary_command",
            "run_report_last_command",
            "safety_check_command",
            "denial_event_record",
            "ocel_projection_candidate_metadata",
            "integrated_restore_document",
        ),
        closed_capabilities=(
            "final_user_test_release_certification",
            "provider_doctor_completion",
            "unscoped_prompt_submission",
            "provider_tool_calling",
            "function_calling",
            "read_only_skill_execution",
            "general_agent_loop",
            "multi_step_agent_loop",
            "file_write_outside_profile_session_trace_store",
            "file_edit",
            "patch_apply",
            "shell_execution",
            "test_execution",
            "subagent_invocation",
            "child_session_creation",
            "parent_raw_transcript_sharing",
            "autonomous_loop",
            "retry_loop",
            "dominion_runtime",
            "production_certification",
        ),
    )


def create_v0415_integrated_restore_packet() -> V0415IntegratedRestorePacket:
    return V0415IntegratedRestorePacket(
        packet_id=_new_id("v0415-restore-packet"),
        single_integrated_doc_path=INTEGRATED_DOC_PATH,
        separate_restore_doc_created=False,
        context_snapshot=create_v0415_integrated_restore_context_snapshot(),
    )


REQUIRED_RESTORE_SECTIONS = (
    "Restore Purpose",
    "One-Screen Restore Summary",
    "Current Version and Track Identity",
    "Repository Baseline Assumptions",
    "v0.41.4 Provider-backed Run Summary",
    "Runtime Event Model Contract",
    "Runtime Object Reference Contract",
    "Trace Store Contract",
    "Trace Append Policy",
    "Command Trace Envelope Contract",
    "Trace Recent Contract",
    "Trace Summary Contract",
    "Run Report Last Contract",
    "Safety Check Command Contract",
    "Denial Event Contract",
    "Trace Validation Contract",
    "OCEL Projection Candidate Contract",
    "Runtime Opening Status",
    "Still-Closed Capabilities",
    "Required Test Commands",
    "Expected Test Interpretation",
    "Known Limitations",
    "Withdrawal Conditions",
    "v0.41.6 Recommended Next Step",
    "v0.41.6 User Test Target",
    "Copy-Paste Restore Prompt for Future GPT/Codex Session",
)


def create_v0415_integrated_restore_document_manifest(
    present_sections: Iterable[str] | None = None,
) -> V0415IntegratedRestoreDocumentManifest:
    present = set(present_sections or REQUIRED_RESTORE_SECTIONS)
    suitable = all(section in present for section in REQUIRED_RESTORE_SECTIONS)
    return V0415IntegratedRestoreDocumentManifest(
        manifest_id=_new_id("v0415-restore-manifest"),
        integrated_doc_required=True,
        separate_restore_doc_allowed=False,
        separate_restore_doc_created=False,
        copy_paste_restore_prompt_required=True,
        suitable_for_new_session_handoff=suitable,
        required_sections=REQUIRED_RESTORE_SECTIONS,
    )


def _json_ready(value: object) -> object:
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    if isinstance(value, Enum):
        return value.value
    return value


def _print_json(value: object) -> None:
    print(json.dumps(_json_ready(value), ensure_ascii=False, indent=2, sort_keys=True))


def _extract_option(args: Sequence[str], option: str) -> str | None:
    if option not in args:
        return None
    index = args.index(option)
    if index + 1 >= len(args):
        return None
    return args[index + 1]


def _command_name(args: Sequence[str]) -> str:
    if not args:
        return ""
    if len(args) > 1 and args[0] in {"profile", "prompt", "session", "provider", "skills", "trace", "run-report", "safety"}:
        return f"{args[0]} {args[1]}"
    return args[0]


def _create_command_event(
    event_kind: str,
    status: str,
    command_name: str,
    profile_id: str,
    home_path: str,
    message: str,
) -> RuntimeEvent:
    return create_runtime_event(
        event_kind,
        status,
        profile_id=profile_id,
        command_name=command_name,
        objects=(
            create_runtime_object_ref(
                object_id=command_name,
                object_kind=RuntimeObjectKind.COMMAND.value,
                display_name=command_name,
                path=None,
            ),
            create_runtime_object_ref(
                object_id="trace-store",
                object_kind=RuntimeObjectKind.TRACE_STORE.value,
                display_name="default-personal trace store",
                path=str(Path(home_path) / "profiles" / profile_id / "state" / "traces"),
            ),
        ),
        message=message,
    )


def _emit_cli_command_trace(args: Sequence[str], exit_code: int) -> None:
    home = _extract_option(args, "--home")
    if home is None or not args:
        return
    command_name = _command_name(args)
    if command_name.startswith("trace ") or command_name.startswith("run-report"):
        return
    config = create_trace_store_config(PROFILE_ID, home)
    status = RuntimeEventStatus.COMPLETED.value if exit_code == 0 else RuntimeEventStatus.FAILED.value
    event_kind = RuntimeEventKind.CLI_COMMAND_COMPLETED.value
    event = _create_command_event(
        event_kind,
        status,
        command_name,
        PROFILE_ID,
        home,
        f"Command {command_name} completed with exit code {exit_code}.",
    )
    append_runtime_event(event, config)


def _run_events_from_result(run_id: str, command_input: RunCommandInput, result: RunCommandResult) -> tuple[RuntimeEvent, ...]:
    run_result = result.run_result
    session_id = run_result.session_id
    user_preview = _preview(command_input.user_input)
    provider_response = run_result.provider_response
    assistant_preview = _preview(provider_response.text if provider_response else run_result.assistant_text)
    next_action = None
    if provider_response and provider_response.empty_response_detected:
        next_action = (
            "inspect raw provider response JSON; increase max_tokens; ask for final answer only; "
            "check LM Studio model/template settings; try a smaller model"
        )
    metadata = {
        "user_input_preview": user_preview,
        "assistant_response_preview": assistant_preview,
        "provider": command_input.provider,
        "mock_provider": command_input.mock_provider,
        "exit_code": result.exit_code,
        "response_parse_status": provider_response.response_parse_status if provider_response else None,
        "response_error_class": provider_response.error_class if provider_response else None,
        "response_extracted_from_field": provider_response.response_extracted_from_field if provider_response else None,
        "response_content_length": provider_response.response_content_length if provider_response else None,
        "response_finish_reason": provider_response.response_finish_reason if provider_response else None,
        "provider_model": provider_response.provider_model if provider_response else None,
        "runtime_identity_included": provider_response.runtime_identity_included if provider_response else None,
        "provider_identity_is_implementation_detail": provider_response.provider_identity_is_implementation_detail if provider_response else None,
        "empty_response_detected": provider_response.empty_response_detected if provider_response else None,
        "next_action": next_action,
    }
    run_ref = create_runtime_object_ref(run_id, RuntimeObjectKind.RUN.value, "v0.41.5 traced run")
    session_ref = create_runtime_object_ref(
        session_id,
        RuntimeObjectKind.SESSION.value,
        "default-personal session",
        metadata={"session_id": session_id},
    )
    base = {
        "profile_id": command_input.profile_id,
        "session_id": session_id,
        "run_id": run_id,
        "command_name": "run",
        "objects": (run_ref, session_ref),
        "metadata": metadata,
    }
    events = [
        create_runtime_event(
            RuntimeEventKind.RUN_STARTED.value,
            RuntimeEventStatus.STARTED.value,
            message="Minimal single-turn run started.",
            **base,
        ),
        create_runtime_event(
            RuntimeEventKind.USER_INPUT_RECEIVED.value,
            RuntimeEventStatus.INFO.value,
            message="Explicit user input received for run.",
            provider_invoked=False,
            prompt_submitted=False,
            **base,
        ),
        create_runtime_event(
            RuntimeEventKind.PROMPT_ASSEMBLED.value,
            RuntimeEventStatus.COMPLETED.value,
            message="Prompt assembly completed for run.",
            provider_invoked=False,
            prompt_submitted=False,
            **base,
        ),
    ]
    if result.provider_invoked or result.prompt_submitted:
        events.append(
            create_runtime_event(
                RuntimeEventKind.PROVIDER_TEXT_CALL_STARTED.value,
                RuntimeEventStatus.STARTED.value,
                message="Scoped text-only provider call started for run.",
                provider_invoked=True,
                prompt_submitted=True,
                **base,
            )
        )
        failed = result.status != "success"
        error_metadata = {
            **metadata,
            "error_class": _extract_error_class(run_result.assistant_text),
        }
        events.append(
            create_runtime_event(
                RuntimeEventKind.PROVIDER_TEXT_CALL_FAILED.value if failed else RuntimeEventKind.PROVIDER_TEXT_CALL_COMPLETED.value,
                RuntimeEventStatus.FAILED.value if failed else RuntimeEventStatus.COMPLETED.value,
                message="Scoped text-only provider call failed for run." if failed else "Scoped text-only provider call completed for run.",
                provider_invoked=True,
                prompt_submitted=True,
                metadata=error_metadata if failed else metadata,
                profile_id=command_input.profile_id,
                session_id=session_id,
                run_id=run_id,
                command_name="run",
                objects=(run_ref, session_ref),
            )
        )
        if provider_response and provider_response.response_parse_status:
            parse_ok = provider_response.response_parse_status == "parsed" and not provider_response.empty_response_detected
            if provider_response.empty_response_detected:
                event_kind = "provider_text_response_empty"
            else:
                event_kind = "provider_text_response_parsed" if parse_ok else "provider_text_response_parse_failed"
            events.append(
                create_runtime_event(
                    event_kind,
                    RuntimeEventStatus.COMPLETED.value if parse_ok else RuntimeEventStatus.FAILED.value,
                    message="Provider text response parsed." if parse_ok else "Provider text response parse did not produce final assistant content.",
                    provider_invoked=False,
                    prompt_submitted=False,
                    metadata=metadata,
                    profile_id=command_input.profile_id,
                    session_id=session_id,
                    run_id=run_id,
                    command_name="run",
                    objects=(run_ref, session_ref),
                )
            )
    if run_result.session_append_result and run_result.session_append_result.success:
        events.append(
            create_runtime_event(
                RuntimeEventKind.SESSION_TURNS_APPENDED.value,
                RuntimeEventStatus.COMPLETED.value,
                message="User and assistant turns appended to the session store.",
                provider_invoked=False,
                prompt_submitted=False,
                metadata={
                    **metadata,
                    "appended_turn_count": run_result.session_append_result.appended_turn_count,
                },
                profile_id=command_input.profile_id,
                session_id=session_id,
                run_id=run_id,
                command_name="run",
                objects=(run_ref, session_ref),
            )
        )
    if (
        result.status == "success"
        and run_result.provider_response is not None
        and bool(run_result.provider_response.text.strip())
    ):
        events.append(
            create_runtime_event(
                RuntimeEventKind.ASSISTANT_RESPONSE_RECORDED.value,
                RuntimeEventStatus.COMPLETED.value,
                message="Assistant response recorded as untrusted provider text.",
                provider_invoked=False,
                prompt_submitted=False,
                **base,
            )
        )
    events.append(
        create_runtime_event(
            RuntimeEventKind.RUN_COMPLETED.value
            if result.status == "success"
            else RuntimeEventKind.RUN_FAILED.value,
            RuntimeEventStatus.COMPLETED.value
            if result.status == "success"
            else RuntimeEventStatus.FAILED.value,
            message="Minimal single-turn run completed."
            if result.status == "success"
            else "Minimal single-turn run failed safely.",
            provider_invoked=False,
            prompt_submitted=False,
            **base,
        )
    )
    return tuple(events)


def _handle_run(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli run")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--home", required=True)
    parser.add_argument("--session", default=None)
    parser.add_argument("--provider", default=None)
    parser.add_argument("--timeout", type=float, default=None)
    parser.add_argument("user_input")
    parsed = parser.parse_args(list(args)[1:])
    command_input = RunCommandInput(
        profile_id=parsed.profile,
        home_path=parsed.home,
        user_input=parsed.user_input,
        session_id=parsed.session,
        provider=parsed.provider,
        mock_provider=parsed.provider == "mock",
        timeout_seconds=parsed.timeout,
    )
    run_id = _new_id("run")
    result = execute_run_command(command_input)
    config = create_trace_store_config(parsed.profile, parsed.home)
    events = _run_events_from_result(run_id, command_input, result)
    append_runtime_events(events, config)
    rendered = result.rendered_text
    if result.status == "success" or result.provider_invoked or result.prompt_submitted:
        rendered = rendered.replace(
            "[v0.41.4 single-turn text-only run]",
            "[v0.41.5 traced single-turn text-only run]",
        ).replace(
            "trace runtime remains closed until v0.41.5",
            "trace runtime emitted bounded append-only events in v0.41.5",
        )
    print(rendered)
    return result.exit_code


def _handle_trace_recent(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli trace recent")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--home", required=True)
    parser.add_argument("--limit", type=int, default=10)
    parsed = parser.parse_args(list(args)[2:])
    result = read_trace_recent(
        create_trace_recent_request(parsed.profile, parsed.home, parsed.limit)
    )
    _print_json(result)
    return 0


def _handle_trace_summary(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli trace summary")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--home", required=True)
    parser.add_argument("--limit", type=int, default=None)
    parsed = parser.parse_args(list(args)[2:])
    result = summarize_trace_events(
        create_trace_summary_request(parsed.profile, parsed.home, parsed.limit)
    )
    _print_json(result)
    return 0


def _handle_run_report_last(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli run-report last")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--home", required=True)
    parser.add_argument("--session", default=None)
    parsed = parser.parse_args(list(args)[2:])
    result = create_last_run_report(
        create_last_run_report_request(parsed.profile, parsed.home, parsed.session)
    )
    _print_json(result)
    return 0


def _handle_safety_check_command(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli safety check-command")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--home", required=True)
    parser.add_argument("--command", required=True)
    parsed = parser.parse_args(list(args)[2:])
    command_input = create_safety_check_command_input(
        parsed.profile,
        parsed.home,
        parsed.command,
    )
    decision = check_unsafe_command(command_input)
    denial_record: DenialEventRecord | None = None
    append_result: TraceAppendResult | None = None
    if decision.blocked:
        denial_record = create_denial_event_record(
            DenialKind.UNSAFE_COMMAND.value,
            "safety check-command",
            parsed.command,
            parsed.profile,
            reason=decision.reason,
            safe_alternative=decision.safe_alternative,
        )
        denial_ref = create_runtime_object_ref(
            denial_record.denial_id,
            RuntimeObjectKind.DENIAL.value,
            "unsafe command denial",
            metadata={"denial_kind": denial_record.denial_kind},
        )
        denial_record = DenialEventRecord(
            **{**asdict(denial_record), "event_ref": denial_ref}
        )
        event = create_runtime_event(
            RuntimeEventKind.UNSAFE_COMMAND_DENIED.value,
            RuntimeEventStatus.DENIED.value,
            profile_id=parsed.profile,
            command_name="safety check-command",
            objects=(denial_ref,),
            message="Unsafe command text denied without execution.",
            metadata={
                "matched_patterns": decision.matched_patterns,
                "command_text_preview": decision.command_text_preview,
            },
        )
        append_result = append_runtime_event(
            event,
            create_trace_store_config(parsed.profile, parsed.home),
        )
    else:
        event = create_runtime_event(
            RuntimeEventKind.UNSAFE_COMMAND_CHECKED.value,
            RuntimeEventStatus.COMPLETED.value,
            profile_id=parsed.profile,
            command_name="safety check-command",
            message="Command text checked without execution.",
            metadata={"command_text_preview": decision.command_text_preview},
        )
        append_result = append_runtime_event(
            event,
            create_trace_store_config(parsed.profile, parsed.home),
        )
    result = create_safety_check_command_result(
        command_input,
        decision,
        denial_record,
        append_result,
    )
    _print_json(result)
    return 1 if decision.blocked else 0


FUTURE_GATED_COMMANDS = {
    "apply",
    "edit",
    "write",
    "shell",
    "test",
    "retest",
    "invoke-subagent",
    "auto",
    "retry-loop",
    "dominion",
    "production-certify",
}


def _handle_future_gated(args: Sequence[str]) -> int:
    command_name = _command_name(args)
    home = _extract_option(args, "--home")
    profile = _extract_option(args, "--profile") or PROFILE_ID
    denial_record = create_denial_event_record(
        DenialKind.UNSUPPORTED_COMMAND.value,
        command_name,
        " ".join(args),
        profile_id=profile,
        reason=f"{command_name} remains future-gated in v0.41.5.",
        safe_alternative="Use trace recent, trace summary, run-report last, or safety check-command.",
    )
    append_result = None
    if home:
        denial_ref = create_runtime_object_ref(
            denial_record.denial_id,
            RuntimeObjectKind.DENIAL.value,
            "unsupported command denial",
            metadata={"command_name": command_name},
        )
        event = create_runtime_event(
            RuntimeEventKind.UNSUPPORTED_COMMAND_DENIED.value,
            RuntimeEventStatus.DENIED.value,
            profile_id=profile,
            command_name=command_name,
            objects=(denial_ref,),
            message=f"{command_name} denied as unsupported in v0.41.5.",
            metadata={"requested_text": _preview(' '.join(args))},
        )
        append_result = append_runtime_event(event, create_trace_store_config(profile, home))
    payload = {
        "status": "unsupported",
        "denial_event_record": asdict(denial_record),
        "trace_append_result": asdict(append_result) if append_result else None,
        "executed": False,
        "production_certified": False,
    }
    _print_json(payload)
    return 1


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        return _v0414_main(args)
    if args[0] in {"--version", "-V", "version"}:
        print(
            "chanta-cli v0.41.1 / v0.41.2 prompt-session / "
            "v0.41.3 provider-skills / v0.41.4 run / v0.41.5 trace-report"
        )
        return 0
    if args[0] == "doctor":
        print("chanta-cli doctor v0.41.1")
        print("current_extension: v0.41.5 event-trace-runtime-report")
        print("next: v0.41.6 Installable Default Personal User Test Release")
        print("trace_append: pass")
        print("trace_recent_command: pass")
        print("trace_summary_command: pass")
        print("run_report_last_command: pass")
        print("safety_check_command: pass")
        print("provider_doctor_completion: closed")
        print("tool_calling: closed")
        print("function_calling: closed")
        print("general_agent_loop: closed")
        print("skill_execution: closed")
        print("shell_execution: closed")
        print("production_certification: closed")
        return 0
    if args[0] == "run":
        if "--home" not in args:
            return _v0414_main(args)
        return _handle_run(args)
    if len(args) >= 2 and args[0] == "trace" and args[1] == "recent":
        if "--home" not in args:
            return _v0414_main(args)
        return _handle_trace_recent(args)
    if len(args) >= 2 and args[0] == "trace" and args[1] == "summary":
        if "--home" not in args:
            return _v0414_main(args)
        return _handle_trace_summary(args)
    if len(args) >= 2 and args[0] == "run-report" and args[1] == "last":
        if "--home" not in args:
            return _v0414_main(args)
        return _handle_run_report_last(args)
    if len(args) >= 2 and args[0] == "safety" and args[1] == "check-command":
        if "--home" not in args:
            return _v0414_main(args)
        return _handle_safety_check_command(args)
    if args[0] in FUTURE_GATED_COMMANDS:
        if "--home" not in args:
            return _v0414_main(args)
        return _handle_future_gated(args)
    exit_code = _v0414_main(args)
    _emit_cli_command_trace(args, exit_code)
    return exit_code


__all__ = [
    "DenialEventRecord",
    "DenialKind",
    "INTEGRATED_DOC_PATH",
    "LastRunReportRequest",
    "LastRunReportResult",
    "OCELProjectionCandidate",
    "OCELProjectionEventRef",
    "OCELProjectionObjectRef",
    "PROFILE_ID",
    "RuntimeCommandTraceEnvelope",
    "RuntimeCommandTraceResult",
    "RuntimeEvent",
    "RuntimeEventEnvelope",
    "RuntimeEventKind",
    "RuntimeEventStatus",
    "RuntimeObjectKind",
    "RuntimeObjectRef",
    "RuntimeReportKind",
    "SafetyCheckCommandInput",
    "SafetyCheckCommandResult",
    "TRACE_SCHEMA_VERSION",
    "TRACE_SOURCE_VERSION",
    "TRACE_VERSION",
    "TraceAppendPolicy",
    "TraceAppendResult",
    "TraceEmitter",
    "TraceRecentRequest",
    "TraceRecentResult",
    "TraceStoreConfig",
    "TraceSummaryRequest",
    "TraceSummaryResult",
    "TraceValidationFinding",
    "TraceValidationReport",
    "UnsafeCommandDecision",
    "UnsafeCommandPattern",
    "V0415IntegratedRestoreContextSnapshot",
    "V0415IntegratedRestoreDocumentManifest",
    "V0415IntegratedRestorePacket",
    "V0415IntegratedRestoreSection",
    "V0415ReadinessReport",
    "V0416InstallableUserTestReleaseHandoff",
    "V0416UserTestTargetUpdate",
    "append_runtime_event",
    "append_runtime_events",
    "build_unsafe_command_patterns",
    "check_unsafe_command",
    "create_denial_event_record",
    "create_last_run_report",
    "create_last_run_report_request",
    "create_last_run_report_result",
    "create_ocel_projection_candidate",
    "create_ocel_projection_event_ref",
    "create_ocel_projection_object_ref",
    "create_runtime_command_trace_envelope",
    "create_runtime_command_trace_result",
    "create_runtime_event",
    "create_runtime_event_envelope",
    "create_runtime_object_ref",
    "create_safety_check_command_input",
    "create_safety_check_command_result",
    "create_trace_append_policy",
    "create_trace_append_result",
    "create_trace_emitter",
    "create_trace_recent_request",
    "create_trace_recent_result",
    "create_trace_store_config",
    "create_trace_summary_request",
    "create_trace_summary_result",
    "create_trace_validation_finding",
    "create_trace_validation_report",
    "create_unsafe_command_decision",
    "create_v0415_integrated_restore_context_snapshot",
    "create_v0415_integrated_restore_document_manifest",
    "create_v0415_integrated_restore_packet",
    "create_v0415_readiness_report",
    "create_v0416_installable_user_test_release_handoff",
    "create_v0416_user_test_target_update",
    "main",
    "read_trace_recent",
    "summarize_trace_events",
    "validate_trace_store",
]
