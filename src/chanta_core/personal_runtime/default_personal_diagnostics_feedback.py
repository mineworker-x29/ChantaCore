"""v0.42.6 diagnostic bundle and bounded feedback loop support.

The diagnostic bundle is read/report only. Feedback writes are bounded to the
default-personal feedback store under the resolved home. This module does not
call providers, submit prompts, execute shell, upload data, mutate memory, edit
workspace files, invoke subagents, or certify production.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass, is_dataclass, replace
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import Any, Mapping, Sequence

from chanta_core.personal_runtime.default_personal_cli_bootstrap import (
    PROFILE_ID,
    DefaultPersonalProfileStatusCommandInput,
    run_profile_status_command,
)
from chanta_core.personal_runtime.default_personal_home_quickstart import (
    create_v042_home_resolution_request,
    create_v042_home_status_command_input,
    create_v042_home_status_command_result,
    resolve_v042_home,
)
from chanta_core.personal_runtime.default_personal_provider_setup import (
    create_v042_provider_config_show_request,
    create_v042_provider_config_show_result,
    create_v042_provider_status_report,
    create_v042_provider_status_request,
)
from chanta_core.personal_runtime.default_personal_read_only_skills import (
    create_v042_skill_list_request,
    create_v042_skill_list_result,
    create_v042_skill_run_command_input,
    create_v042_skill_run_command_result,
    create_v042_skill_safety_report,
    main as _v0425_main,
)
from chanta_core.personal_runtime.default_personal_trace_history import (
    create_v042_run_history_request,
    create_v042_run_history_result,
    create_v042_session_show_request,
    create_v042_session_show_result,
    create_v042_trace_timeline_request,
    create_v042_trace_timeline_result,
)
from chanta_core.personal_runtime.default_personal_trace_report import (
    RuntimeObjectKind,
    append_runtime_event,
    create_last_run_report,
    create_last_run_report_request,
    create_runtime_event,
    create_runtime_object_ref,
    create_trace_store_config,
    create_trace_summary_request,
    summarize_trace_events,
)


V0426_VERSION = "v0.42.6"
V0426_RELEASE_NAME = "v0.42.6 Diagnostic Bundle & User Feedback Loop"
V042_TRACK_NAME = "v0.42 Default Personal Runtime UX Hardening Track"
INTEGRATED_DOC_PATH = "docs/versions/v0.42/v0.42.6_diagnostic_bundle_feedback_loop_restore.md"


class V042DiagnosticBundleMode(StrEnum):
    STANDARD = "standard"
    COPY_PASTE = "copy_paste"
    MARKDOWN = "markdown"
    JSON = "json"
    BRIEF = "brief"
    UNKNOWN = "unknown"


class V042DiagnosticBundleStatus(StrEnum):
    COMPLETED = "completed"
    COMPLETED_WITH_WARNINGS = "completed_with_warnings"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"
    UNKNOWN = "unknown"


class V042DiagnosticBundleSourceKind(StrEnum):
    VERSION = "version"
    HOME_STATUS = "home_status"
    PROFILE_STATUS = "profile_status"
    PROVIDER_STATUS = "provider_status"
    PROVIDER_CONFIG_REDACTED = "provider_config_redacted"
    LAST_RUN_REPORT = "last_run_report"
    RUN_HISTORY = "run_history"
    TRACE_SUMMARY = "trace_summary"
    TRACE_TIMELINE_SUMMARY = "trace_timeline_summary"
    SESSION_SHOW_LAST = "session_show_last"
    SKILL_LIST_SUMMARY = "skill_list_summary"
    SKILL_EXECUTION_SUMMARY = "skill_execution_summary"
    DENIAL_SUMMARY = "denial_summary"
    SAFETY_COUNT_SUMMARY = "safety_count_summary"
    FEEDBACK_SUMMARY = "feedback_summary"
    LATEST_FEEDBACK_NOTES = "latest_feedback_notes"
    KNOWN_LIMITATIONS = "known_limitations"
    CLOSED_CAPABILITY_SNAPSHOT = "closed_capability_snapshot"
    V042_TRACK_CLOSURE = "v042_track_closure"
    NEXT_ACTION = "next_action"
    UNKNOWN = "unknown"


class V042DiagnosticBundleSectionKind(StrEnum):
    HEADER = "header"
    ENVIRONMENT = "environment"
    RUNTIME_STATUS = "runtime_status"
    PROVIDER = "provider"
    RUN = "run"
    TRACE = "trace"
    SESSION = "session"
    SKILLS = "skills"
    DENIALS = "denials"
    FEEDBACK = "feedback"
    SAFETY = "safety"
    LIMITATIONS = "limitations"
    CLOSED_CAPABILITIES = "closed_capabilities"
    PROCESS_INTELLIGENCE_REVIEW = "process_intelligence_review"
    NEXT_STEPS = "next_steps"
    COPY_PASTE_HANDOFF = "copy_paste_handoff"
    UNKNOWN = "unknown"


class V042DiagnosticBundleFormat(StrEnum):
    TEXT = "text"
    MARKDOWN = "markdown"
    JSON = "json"
    COMPACT_TEXT = "compact_text"
    UNKNOWN = "unknown"


class V042FeedbackCategory(StrEnum):
    UX = "ux"
    BUG = "bug"
    PROVIDER = "provider"
    TRACE = "trace"
    SKILL = "skill"
    SAFETY = "safety"
    PROCESS_INTELLIGENCE = "process_intelligence"
    DOCS = "docs"
    PERFORMANCE = "performance"
    IDEA = "idea"
    UNKNOWN = "unknown"


class V042FeedbackSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKER = "blocker"
    UNKNOWN = "unknown"


class V042FeedbackStatus(StrEnum):
    RECORDED = "recorded"
    REDACTED = "redacted"
    REJECTED = "rejected"
    LISTED = "listed"
    SUMMARIZED = "summarized"
    FAILED = "failed"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V042DiagnosticRedactionPolicy:
    policy_id: str
    redact_secrets: bool
    redact_api_keys: bool
    redact_tokens: bool
    redact_env_values: bool
    redact_absolute_paths: bool
    preserve_safe_path_context: bool
    secret_patterns: tuple[str, ...]
    replacement_text: str


@dataclass(frozen=True)
class V042DiagnosticBundleRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    mode: str
    output_format: str
    copy_paste: bool
    include_feedback: bool
    include_trace_timeline: bool
    include_skill_summary: bool
    include_closed_capabilities: bool
    max_runs: int
    max_trace_items: int
    max_feedback_items: int


@dataclass(frozen=True)
class V042DiagnosticBundleSource:
    source_id: str
    source_kind: str
    available: bool
    status: str
    summary: str
    error_message: str | None
    redacted: bool
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V042DiagnosticBundleSection:
    section_id: str
    section_kind: str
    title: str
    content: str
    source_ids: tuple[str, ...]
    redacted: bool
    process_intelligence_relevance: str


@dataclass(frozen=True)
class V042DiagnosticCopyPasteText:
    handoff_id: str
    title: str
    text: str
    includes_secret_values: bool
    includes_required_debug_context: bool
    suitable_for_gpt_or_codex: bool
    max_length_bounded: bool


@dataclass(frozen=True)
class V042DiagnosticSafetyReport:
    report_id: str
    report_bundle_calls_provider: bool
    report_bundle_submits_prompt: bool
    report_bundle_writes_files_by_default: bool
    report_bundle_executes_shell: bool
    report_bundle_invokes_subagent: bool
    report_bundle_reads_arbitrary_paths: bool
    report_bundle_scans_filesystem: bool
    report_bundle_uploads_external: bool
    secrets_redacted: bool
    production_certified: bool


@dataclass(frozen=True)
class V042DiagnosticPIReviewPacket:
    packet_id: str
    profile_id: str
    run_count_summary: str
    provider_count_summary: str
    denial_summary: str
    skill_summary: str
    feedback_summary: str
    safety_summary: str
    process_instance_review_ready: bool
    evidence_handoff_ready: bool
    high_risk_counts_zero: bool


@dataclass(frozen=True)
class V042DiagnosticBundleResult:
    result_id: str
    request_id: str
    profile_id: str
    resolved_home_path: str
    status: str
    sections: tuple[V042DiagnosticBundleSection, ...]
    sources: tuple[V042DiagnosticBundleSource, ...]
    rendered_text: str
    copy_paste_text: str
    pi_review_packet: V042DiagnosticPIReviewPacket
    safety_report: V042DiagnosticSafetyReport
    provider_invoked: bool
    prompt_submitted: bool
    filesystem_written: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V042FeedbackRedactionPolicy:
    policy_id: str
    redact_secret_like_values_before_persistence: bool
    reject_if_unredactable_secret_detected: bool
    secret_patterns: tuple[str, ...]
    replacement_text: str
    preserve_user_intent: bool


@dataclass(frozen=True)
class V042FeedbackStorePolicy:
    policy_id: str
    relative_store_path: str
    bounded_to_home: bool
    append_only: bool
    writes_core_memory: bool
    writes_profile_config: bool
    writes_provider_config: bool
    writes_session_store: bool
    writes_workspace: bool
    stores_secret_values: bool


@dataclass(frozen=True)
class V042FeedbackNoteRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    category: str
    severity: str
    note_text: str
    source_command: str
    trace_feedback: bool


@dataclass(frozen=True)
class V042FeedbackNoteRecord:
    feedback_id: str
    profile_id: str
    category: str
    severity: str
    status: str
    note_text_redacted: str
    created_at: str
    source_command: str
    redacted: bool
    raw_secret_value_persisted: bool
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V042FeedbackAppendResult:
    result_id: str
    feedback_record: V042FeedbackNoteRecord | None
    store_path: str
    appended: bool
    rejected: bool
    rejection_reason: str | None
    trace_event_appended: bool
    outside_home_paths: tuple[str, ...]
    overwritten_files: tuple[str, ...]
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V042FeedbackListRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    limit: int
    category: str | None
    severity: str | None
    display_format: str


@dataclass(frozen=True)
class V042FeedbackListResult:
    result_id: str
    records: tuple[V042FeedbackNoteRecord, ...]
    count: int
    rendered_text: str
    provider_invoked: bool
    prompt_submitted: bool
    filesystem_written: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V042FeedbackShowRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    target: str
    feedback_id: str | None
    display_format: str


@dataclass(frozen=True)
class V042FeedbackShowResult:
    result_id: str
    found: bool
    record: V042FeedbackNoteRecord | None
    rendered_text: str
    provider_invoked: bool
    prompt_submitted: bool
    filesystem_written: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V042FeedbackSummary:
    summary_id: str
    total_feedback_count: int
    by_category: dict[str, int]
    by_severity: dict[str, int]
    latest_feedback_preview: str | None
    blocker_count: int
    high_count: int
    process_intelligence_feedback_count: int
    safety_feedback_count: int
    rendered_text: str


@dataclass(frozen=True)
class V042FeedbackLoopSafetyReport:
    report_id: str
    feedback_writes_bounded_store: bool
    feedback_writes_core_memory: bool
    feedback_writes_profile_config: bool
    feedback_writes_provider_config: bool
    feedback_writes_session_store: bool
    feedback_writes_workspace: bool
    feedback_calls_provider: bool
    feedback_submits_prompt: bool
    feedback_executes_shell: bool
    feedback_invokes_subagent: bool
    feedback_stores_secret_values: bool
    production_certified: bool


@dataclass(frozen=True)
class V042KnownLimitationRecord:
    limitation_id: str
    title: str
    description: str
    severity: str
    target_track: str
    recommended_next_action: str


@dataclass(frozen=True)
class V042ClosedCapabilitySnapshot:
    snapshot_id: str
    shell_execution_closed: bool
    file_edit_closed: bool
    patch_apply_closed: bool
    arbitrary_file_read_closed: bool
    broad_scan_closed: bool
    provider_tool_calling_closed: bool
    function_calling_closed: bool
    provider_doctor_completion_closed: bool
    subagent_closed: bool
    general_agent_loop_closed: bool
    autonomous_loop_closed: bool
    memory_mutation_closed: bool
    dominion_closed: bool
    production_certified: bool


@dataclass(frozen=True)
class V042UXHardeningTrackClosureAssessment:
    assessment_id: str
    track_name: str
    versions_completed: tuple[str, ...]
    user_operability_improved: bool
    installable_runtime_baseline: bool
    default_home_ready: bool
    provider_setup_ux_ready: bool
    trace_history_ux_ready: bool
    manual_chat_ready: bool
    bounded_skill_execution_ready: bool
    diagnostic_bundle_ready: bool
    feedback_loop_ready: bool
    high_risk_capabilities_deferred: bool
    ready_for_v043_user_operation_pilot: bool
    production_certified: bool


@dataclass(frozen=True)
class V0426ReadinessReport:
    diagnostic_bundle_command_ready: bool
    diagnostic_copy_paste_ready: bool
    diagnostic_redaction_ready: bool
    diagnostic_pi_review_packet_ready: bool
    feedback_note_command_ready: bool
    feedback_list_command_ready: bool
    feedback_show_command_ready: bool
    feedback_summary_command_ready: bool
    feedback_store_ready: bool
    feedback_redaction_ready: bool
    known_limitations_ready: bool
    closed_capability_snapshot_ready: bool
    v042_track_closure_assessment_ready: bool
    integrated_restore_document_ready: bool
    v043_handoff_ready: bool
    ready_for_external_upload: bool
    ready_for_network_submission: bool
    ready_for_automatic_issue_creation: bool
    ready_for_automatic_code_fixing: bool
    ready_for_shell_execution: bool
    ready_for_file_edit: bool
    ready_for_patch_apply: bool
    ready_for_arbitrary_file_read: bool
    ready_for_broad_filesystem_scan: bool
    ready_for_repo_search: bool
    ready_for_provider_doctor_completion: bool
    ready_for_provider_tool_calling: bool
    ready_for_function_calling: bool
    ready_for_general_agent_loop: bool
    ready_for_multi_step_agent_loop: bool
    ready_for_subagent_invocation: bool
    ready_for_child_session_creation: bool
    ready_for_memory_write: bool
    ready_for_autonomous_retry_loop: bool
    ready_for_dominion_runtime: bool
    production_certified: bool


@dataclass(frozen=True)
class V043UserOperationPilotHandoff:
    target_version: str
    title: str
    recommended_focus: tuple[str, ...]
    must_not_open: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V0426IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool


@dataclass(frozen=True)
class V0426IntegratedRestoreContextSnapshot:
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]


@dataclass(frozen=True)
class V0426IntegratedRestorePacket:
    packet_id: str
    context_snapshot: V0426IntegratedRestoreContextSnapshot
    sections: tuple[V0426IntegratedRestoreSection, ...]
    single_integrated_doc_path: str
    separate_restore_doc_created: bool


@dataclass(frozen=True)
class V0426IntegratedRestoreDocumentManifest:
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


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _resolve_home(home_path: str | None, command_name: str) -> str | None:
    resolved = resolve_v042_home(
        create_v042_home_resolution_request(
            explicit_home=home_path,
            command_name=command_name,
            allow_create=False,
            cwd=os.getcwd(),
        )
    )
    return resolved.home_path if resolved.safe_to_use else None


def _bounded_int(value: object, default: int, maximum: int) -> int:
    try:
        return max(1, min(int(value), maximum))
    except (TypeError, ValueError):
        return default


def create_v042_diagnostic_redaction_policy(**overrides: Any) -> V042DiagnosticRedactionPolicy:
    defaults = {
        "policy_id": "v0426-diagnostic-redaction-policy",
        "redact_secrets": True,
        "redact_api_keys": True,
        "redact_tokens": True,
        "redact_env_values": True,
        "redact_absolute_paths": False,
        "preserve_safe_path_context": True,
        "secret_patterns": ("sk-", "api_key", "token", "secret", "password", "credential"),
        "replacement_text": "<redacted>",
    }
    return V042DiagnosticRedactionPolicy(**_merge(defaults, overrides))


def _redact_text(text: str, replacement: str = "<redacted>") -> tuple[str, bool]:
    redacted = text
    patterns = (
        re.compile(r"\b[A-Z0-9_]*(?:API_KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL)\s*=\s*\S+", re.IGNORECASE),
        re.compile(r"sk-[A-Za-z0-9._-]+", re.IGNORECASE),
        re.compile(r"(?:token|secret|password|credential)\s*[:=]\s*\S+", re.IGNORECASE),
    )
    changed = False
    for pattern in patterns:
        redacted, count = pattern.subn(replacement, redacted)
        changed = changed or bool(count)
    return redacted, changed


def create_v042_feedback_redaction_policy(**overrides: Any) -> V042FeedbackRedactionPolicy:
    defaults = {
        "policy_id": "v0426-feedback-redaction-policy",
        "redact_secret_like_values_before_persistence": True,
        "reject_if_unredactable_secret_detected": False,
        "secret_patterns": ("sk-", "api_key", "token", "secret", "password", "credential"),
        "replacement_text": "<redacted>",
        "preserve_user_intent": True,
    }
    return V042FeedbackRedactionPolicy(**_merge(defaults, overrides))


def redact_v042_feedback_note_text(note_text: str, policy: V042FeedbackRedactionPolicy | None = None) -> str:
    actual = policy or create_v042_feedback_redaction_policy()
    redacted, _ = _redact_text(note_text, actual.replacement_text)
    return redacted


def create_v042_feedback_store_policy(profile_id: str = PROFILE_ID, **overrides: Any) -> V042FeedbackStorePolicy:
    defaults = {
        "policy_id": "v0426-feedback-store-policy",
        "relative_store_path": f"profiles/{profile_id}/state/feedback/feedback.jsonl",
        "bounded_to_home": True,
        "append_only": True,
        "writes_core_memory": False,
        "writes_profile_config": False,
        "writes_provider_config": False,
        "writes_session_store": False,
        "writes_workspace": False,
        "stores_secret_values": False,
    }
    return V042FeedbackStorePolicy(**_merge(defaults, overrides))


def _feedback_store_path(home_path: str, profile_id: str = PROFILE_ID) -> Path:
    return Path(home_path) / "profiles" / profile_id / "state" / "feedback" / "feedback.jsonl"


def _is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
        return True
    except ValueError:
        return False


def create_v042_feedback_note_request(
    note_text: str,
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    category: str = V042FeedbackCategory.UNKNOWN.value,
    severity: str = V042FeedbackSeverity.LOW.value,
    source_command: str = "feedback note",
    trace_feedback: bool = True,
    **overrides: Any,
) -> V042FeedbackNoteRequest:
    category_value = category if category in {item.value for item in V042FeedbackCategory} else V042FeedbackCategory.UNKNOWN.value
    severity_value = severity if severity in {item.value for item in V042FeedbackSeverity} else V042FeedbackSeverity.UNKNOWN.value
    defaults = {
        "request_id": "v0426-feedback-note-request",
        "profile_id": profile_id,
        "home_path": home_path,
        "category": category_value,
        "severity": severity_value,
        "note_text": note_text,
        "source_command": source_command,
        "trace_feedback": bool(trace_feedback),
    }
    return V042FeedbackNoteRequest(**_merge(defaults, overrides))


def create_v042_feedback_note_record(request: V042FeedbackNoteRequest, **overrides: Any) -> V042FeedbackNoteRecord:
    redacted_text = redact_v042_feedback_note_text(request.note_text)
    redacted = redacted_text != request.note_text
    defaults = {
        "feedback_id": f"feedback-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')}",
        "profile_id": request.profile_id,
        "category": request.category,
        "severity": request.severity,
        "status": V042FeedbackStatus.REDACTED.value if redacted else V042FeedbackStatus.RECORDED.value,
        "note_text_redacted": redacted_text,
        "created_at": _now(),
        "source_command": request.source_command,
        "redacted": redacted,
        "raw_secret_value_persisted": False,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    return V042FeedbackNoteRecord(**_merge(defaults, overrides))


def _record_from_dict(data: Mapping[str, Any]) -> V042FeedbackNoteRecord:
    return V042FeedbackNoteRecord(
        feedback_id=str(data.get("feedback_id", "")),
        profile_id=str(data.get("profile_id", PROFILE_ID)),
        category=str(data.get("category", V042FeedbackCategory.UNKNOWN.value)),
        severity=str(data.get("severity", V042FeedbackSeverity.UNKNOWN.value)),
        status=str(data.get("status", V042FeedbackStatus.UNKNOWN.value)),
        note_text_redacted=str(data.get("note_text_redacted", "")),
        created_at=str(data.get("created_at", "")),
        source_command=str(data.get("source_command", "")),
        redacted=bool(data.get("redacted", False)),
        raw_secret_value_persisted=False,
        provider_invoked=False,
        prompt_submitted=False,
        shell_executed=False,
        subagent_invoked=False,
        production_certified=False,
    )


def _read_feedback_records(home_path: str, profile_id: str = PROFILE_ID) -> tuple[V042FeedbackNoteRecord, ...]:
    path = _feedback_store_path(home_path, profile_id)
    if not path.exists():
        return ()
    records: list[V042FeedbackNoteRecord] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            records.append(_record_from_dict(json.loads(line)))
        except json.JSONDecodeError:
            continue
    return tuple(records)


def _append_feedback_trace(home: str, record: V042FeedbackNoteRecord) -> bool:
    event = create_runtime_event(
        "feedback_note_recorded",
        "completed",
        profile_id=record.profile_id,
        command_name="feedback note",
        objects=(
            create_runtime_object_ref(
                record.feedback_id,
                RuntimeObjectKind.RUNTIME_REPORT.value,
                display_name="feedback note",
                metadata={"category": record.category, "severity": record.severity, "redacted": record.redacted},
            ),
        ),
        message="Bounded feedback note recorded under profile state.",
        metadata={"feedback_id": record.feedback_id, "category": record.category, "severity": record.severity},
        provider_invoked=False,
        prompt_submitted=False,
        skill_executed=False,
        shell_executed=False,
        workspace_mutated=False,
        subagent_invoked=False,
        production_certified=False,
    )
    result = append_runtime_event(event, create_trace_store_config(record.profile_id, home))
    return result.success


def create_v042_feedback_append_result(**overrides: Any) -> V042FeedbackAppendResult:
    defaults = {
        "result_id": "v0426-feedback-append-result",
        "feedback_record": None,
        "store_path": "",
        "appended": False,
        "rejected": False,
        "rejection_reason": None,
        "trace_event_appended": False,
        "outside_home_paths": (),
        "overwritten_files": (),
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    return V042FeedbackAppendResult(**_merge(defaults, overrides))


def append_v042_feedback_note(request: V042FeedbackNoteRequest, **overrides: Any) -> V042FeedbackAppendResult:
    home = _resolve_home(request.home_path, "feedback note")
    if not home:
        return create_v042_feedback_append_result(rejected=True, rejection_reason="home_unresolved")
    if not request.note_text.strip():
        return create_v042_feedback_append_result(rejected=True, rejection_reason="empty_note")
    path = _feedback_store_path(home, request.profile_id)
    if not _is_under(path, Path(home)):
        return create_v042_feedback_append_result(store_path=str(path), rejected=True, rejection_reason="outside_home_blocked", outside_home_paths=(str(path),))
    record = create_v042_feedback_note_record(request)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(_json_ready(record), ensure_ascii=False, sort_keys=True) + "\n")
    trace_appended = _append_feedback_trace(home, record) if request.trace_feedback else False
    return create_v042_feedback_append_result(
        feedback_record=record,
        store_path=str(path),
        appended=True,
        trace_event_appended=trace_appended,
        **overrides,
    )


def create_v042_feedback_list_request(
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    limit: int = 20,
    category: str | None = None,
    severity: str | None = None,
    display_format: str = "text",
    **overrides: Any,
) -> V042FeedbackListRequest:
    defaults = {
        "request_id": "v0426-feedback-list-request",
        "profile_id": profile_id,
        "home_path": home_path,
        "limit": _bounded_int(limit, 20, 100),
        "category": category,
        "severity": severity,
        "display_format": display_format,
    }
    return V042FeedbackListRequest(**_merge(defaults, overrides))


def _render_feedback_records(records: Sequence[V042FeedbackNoteRecord]) -> str:
    lines = ["ChantaCore feedback records", f"count: {len(records)}"]
    lines.extend(f"- {record.feedback_id} [{record.category}/{record.severity}] {record.note_text_redacted}" for record in records)
    return "\n".join(lines)


def create_v042_feedback_list_result(request: V042FeedbackListRequest, **overrides: Any) -> V042FeedbackListResult:
    home = _resolve_home(request.home_path, "feedback list") or ""
    records = list(_read_feedback_records(home, request.profile_id)) if home else []
    if request.category:
        records = [record for record in records if record.category == request.category]
    if request.severity:
        records = [record for record in records if record.severity == request.severity]
    selected = tuple(records[-request.limit :])
    rendered = _render_json(selected) if request.display_format == "json" else _render_feedback_records(selected)
    defaults = {
        "result_id": "v0426-feedback-list-result",
        "records": selected,
        "count": len(selected),
        "rendered_text": rendered,
        "provider_invoked": False,
        "prompt_submitted": False,
        "filesystem_written": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    return V042FeedbackListResult(**_merge(defaults, overrides))


def create_v042_feedback_show_request(
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    target: str = "last",
    feedback_id: str | None = None,
    display_format: str = "text",
    **overrides: Any,
) -> V042FeedbackShowRequest:
    target_value = target if target in {"last", "feedback_id"} else "unknown"
    defaults = {
        "request_id": "v0426-feedback-show-request",
        "profile_id": profile_id,
        "home_path": home_path,
        "target": target_value,
        "feedback_id": feedback_id,
        "display_format": display_format,
    }
    return V042FeedbackShowRequest(**_merge(defaults, overrides))


def create_v042_feedback_show_result(request: V042FeedbackShowRequest, **overrides: Any) -> V042FeedbackShowResult:
    home = _resolve_home(request.home_path, "feedback show") or ""
    records = _read_feedback_records(home, request.profile_id) if home else ()
    record = None
    if request.target == "feedback_id" and request.feedback_id:
        record = next((item for item in records if item.feedback_id == request.feedback_id), None)
    elif records:
        record = records[-1]
    rendered = _render_json(record) if request.display_format == "json" else (
        f"ChantaCore feedback show\nfound: true\nid: {record.feedback_id}\ncategory: {record.category}\nseverity: {record.severity}\nnote: {record.note_text_redacted}"
        if record
        else "ChantaCore feedback show\nfound: false"
    )
    defaults = {
        "result_id": "v0426-feedback-show-result",
        "found": record is not None,
        "record": record,
        "rendered_text": rendered,
        "provider_invoked": False,
        "prompt_submitted": False,
        "filesystem_written": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    return V042FeedbackShowResult(**_merge(defaults, overrides))


def create_v042_feedback_summary(
    records: Sequence[V042FeedbackNoteRecord] = (),
    **overrides: Any,
) -> V042FeedbackSummary:
    by_category: dict[str, int] = {}
    by_severity: dict[str, int] = {}
    for record in records:
        by_category[record.category] = by_category.get(record.category, 0) + 1
        by_severity[record.severity] = by_severity.get(record.severity, 0) + 1
    latest = records[-1].note_text_redacted if records else None
    defaults = {
        "summary_id": "v0426-feedback-summary",
        "total_feedback_count": len(records),
        "by_category": by_category,
        "by_severity": by_severity,
        "latest_feedback_preview": latest,
        "blocker_count": by_severity.get(V042FeedbackSeverity.BLOCKER.value, 0),
        "high_count": by_severity.get(V042FeedbackSeverity.HIGH.value, 0),
        "process_intelligence_feedback_count": by_category.get(V042FeedbackCategory.PROCESS_INTELLIGENCE.value, 0),
        "safety_feedback_count": by_category.get(V042FeedbackCategory.SAFETY.value, 0),
        "rendered_text": "",
    }
    summary = V042FeedbackSummary(**_merge(defaults, overrides))
    rendered = "\n".join(
        (
            "ChantaCore feedback summary",
            f"total_feedback_count: {summary.total_feedback_count}",
            f"by_category: {summary.by_category}",
            f"by_severity: {summary.by_severity}",
            f"process_intelligence_feedback_count: {summary.process_intelligence_feedback_count}",
            f"safety_feedback_count: {summary.safety_feedback_count}",
            f"latest_feedback_preview: {summary.latest_feedback_preview or '-'}",
        )
    )
    return replace(summary, rendered_text=rendered)


def create_v042_feedback_loop_safety_report(**overrides: Any) -> V042FeedbackLoopSafetyReport:
    defaults = {
        "report_id": "v0426-feedback-loop-safety-report",
        "feedback_writes_bounded_store": True,
        "feedback_writes_core_memory": False,
        "feedback_writes_profile_config": False,
        "feedback_writes_provider_config": False,
        "feedback_writes_session_store": False,
        "feedback_writes_workspace": False,
        "feedback_calls_provider": False,
        "feedback_submits_prompt": False,
        "feedback_executes_shell": False,
        "feedback_invokes_subagent": False,
        "feedback_stores_secret_values": False,
        "production_certified": False,
    }
    return V042FeedbackLoopSafetyReport(**_merge(defaults, overrides))


def create_v042_known_limitation_record(limitation_id: str, title: str, description: str, severity: str = "medium", target_track: str = "v0.43", recommended_next_action: str = "review during user operation pilot") -> V042KnownLimitationRecord:
    return V042KnownLimitationRecord(limitation_id, title, description, severity, target_track, recommended_next_action)


def build_v042_known_limitations() -> tuple[V042KnownLimitationRecord, ...]:
    return (
        create_v042_known_limitation_record("configured-provider-manual-setup", "Configured provider setup may require manual environment setup", "Configured real provider flows depend on user-managed local endpoint and environment readiness."),
        create_v042_known_limitation_record("production-certification-false", "Production certification remains false", "v0.42 is not a production certification track."),
        create_v042_known_limitation_record("general-agentloop-closed", "General AgentLoop remains closed", "Manual chat and bounded read-only skills do not open autonomous operation."),
        create_v042_known_limitation_record("shell-edit-apply-subagent-closed", "Shell/edit/apply/subagent remain closed", "High-risk runtime actions remain deferred."),
        create_v042_known_limitation_record("broad-search-closed", "Broad filesystem/repo search remains closed", "Diagnostic bundle reads only bounded runtime state."),
        create_v042_known_limitation_record("feedback-not-issue-fixing", "Feedback is local bounded record, not automatic issue fixing", "Feedback notes do not create issues or patch code."),
        create_v042_known_limitation_record("bundle-not-upload", "Diagnostic bundle is local report, not external upload", "The bundle is rendered locally for copy-paste handoff."),
        create_v042_known_limitation_record("ux-hardening-not-production", "v0.42 is user-operability hardening, not production release", "The track improves usability and reviewability without production certification."),
    )


def create_v042_closed_capability_snapshot(**overrides: Any) -> V042ClosedCapabilitySnapshot:
    defaults = {
        "snapshot_id": "v0426-closed-capability-snapshot",
        "shell_execution_closed": True,
        "file_edit_closed": True,
        "patch_apply_closed": True,
        "arbitrary_file_read_closed": True,
        "broad_scan_closed": True,
        "provider_tool_calling_closed": True,
        "function_calling_closed": True,
        "provider_doctor_completion_closed": True,
        "subagent_closed": True,
        "general_agent_loop_closed": True,
        "autonomous_loop_closed": True,
        "memory_mutation_closed": True,
        "dominion_closed": True,
        "production_certified": False,
    }
    return V042ClosedCapabilitySnapshot(**_merge(defaults, overrides))


def create_v042_ux_hardening_track_closure_assessment(**overrides: Any) -> V042UXHardeningTrackClosureAssessment:
    defaults = {
        "assessment_id": "v0426-ux-hardening-track-closure-assessment",
        "track_name": V042_TRACK_NAME,
        "versions_completed": ("v0.42.0", "v0.42.1", "v0.42.2", "v0.42.3", "v0.42.4", "v0.42.5", "v0.42.6"),
        "user_operability_improved": True,
        "installable_runtime_baseline": True,
        "default_home_ready": True,
        "provider_setup_ux_ready": True,
        "trace_history_ux_ready": True,
        "manual_chat_ready": True,
        "bounded_skill_execution_ready": True,
        "diagnostic_bundle_ready": True,
        "feedback_loop_ready": True,
        "high_risk_capabilities_deferred": True,
        "ready_for_v043_user_operation_pilot": True,
        "production_certified": False,
    }
    return V042UXHardeningTrackClosureAssessment(**_merge(defaults, overrides))


def create_v042_diagnostic_bundle_request(
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    mode: str = V042DiagnosticBundleMode.STANDARD.value,
    output_format: str = V042DiagnosticBundleFormat.TEXT.value,
    copy_paste: bool = False,
    include_feedback: bool = True,
    include_trace_timeline: bool = True,
    include_skill_summary: bool = True,
    include_closed_capabilities: bool = True,
    max_runs: int = 10,
    max_trace_items: int = 20,
    max_feedback_items: int = 10,
    **overrides: Any,
) -> V042DiagnosticBundleRequest:
    defaults = {
        "request_id": "v0426-diagnostic-bundle-request",
        "profile_id": profile_id,
        "home_path": home_path,
        "mode": mode,
        "output_format": output_format,
        "copy_paste": bool(copy_paste),
        "include_feedback": bool(include_feedback),
        "include_trace_timeline": bool(include_trace_timeline),
        "include_skill_summary": bool(include_skill_summary),
        "include_closed_capabilities": bool(include_closed_capabilities),
        "max_runs": _bounded_int(max_runs, 10, 100),
        "max_trace_items": _bounded_int(max_trace_items, 20, 200),
        "max_feedback_items": _bounded_int(max_feedback_items, 10, 100),
    }
    return V042DiagnosticBundleRequest(**_merge(defaults, overrides))


def create_v042_diagnostic_bundle_source(source_kind: str, summary: str, available: bool = True, status: str = "completed", error_message: str | None = None, redacted: bool = True, **overrides: Any) -> V042DiagnosticBundleSource:
    redacted_summary, _ = _redact_text(summary)
    defaults = {
        "source_id": f"v0426-source-{source_kind}",
        "source_kind": source_kind,
        "available": available,
        "status": status,
        "summary": redacted_summary,
        "error_message": error_message,
        "redacted": redacted,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    return V042DiagnosticBundleSource(**_merge(defaults, overrides))


def _profile_status_text(profile_id: str, home: str) -> str:
    result = run_profile_status_command(DefaultPersonalProfileStatusCommandInput(profile_id, home))
    return f"status={result.status}; profile_exists={result.profile_exists}; message={result.message}"


def collect_v042_diagnostic_bundle_sources(request: V042DiagnosticBundleRequest, **overrides: Any) -> tuple[V042DiagnosticBundleSource, ...]:
    home = _resolve_home(request.home_path, "report bundle") or ""
    sources: list[V042DiagnosticBundleSource] = [
        create_v042_diagnostic_bundle_source(V042DiagnosticBundleSourceKind.VERSION.value, f"{V0426_RELEASE_NAME}; track={V042_TRACK_NAME}"),
    ]
    if not home:
        sources.append(create_v042_diagnostic_bundle_source(V042DiagnosticBundleSourceKind.HOME_STATUS.value, "home unresolved", available=False, status="blocked"))
        return tuple(sources)
    home_status = create_v042_home_status_command_result(create_v042_home_status_command_input(home, request.profile_id))
    provider_status = create_v042_provider_status_report(create_v042_provider_status_request(home, request.profile_id))
    provider_config = create_v042_provider_config_show_result(create_v042_provider_config_show_request(home, request.profile_id))
    last_run = create_last_run_report(create_last_run_report_request(request.profile_id, home))
    run_history = create_v042_run_history_result(create_v042_run_history_request(request.profile_id, home, request.max_runs))
    trace_summary = summarize_trace_events(create_trace_summary_request(request.profile_id, home))
    timeline = create_v042_trace_timeline_result(create_v042_trace_timeline_request(request.profile_id, home, request.max_trace_items))
    session = create_v042_session_show_result(create_v042_session_show_request(request.profile_id, home, "last", None, "text", True, 10))
    skills = create_v042_skill_list_result(create_v042_skill_list_request(request.profile_id, home, True))
    skill_summary = create_v042_skill_safety_report()
    feedback_records = _read_feedback_records(home, request.profile_id)
    feedback_summary = create_v042_feedback_summary(feedback_records)
    limitations = build_v042_known_limitations()
    closed = create_v042_closed_capability_snapshot()
    closure = create_v042_ux_hardening_track_closure_assessment()
    sources.extend(
        (
            create_v042_diagnostic_bundle_source(V042DiagnosticBundleSourceKind.HOME_STATUS.value, home_status.rendered_text),
            create_v042_diagnostic_bundle_source(V042DiagnosticBundleSourceKind.PROFILE_STATUS.value, _profile_status_text(request.profile_id, home)),
            create_v042_diagnostic_bundle_source(V042DiagnosticBundleSourceKind.PROVIDER_STATUS.value, provider_status.rendered_text),
            create_v042_diagnostic_bundle_source(V042DiagnosticBundleSourceKind.PROVIDER_CONFIG_REDACTED.value, provider_config.rendered_text),
            create_v042_diagnostic_bundle_source(V042DiagnosticBundleSourceKind.LAST_RUN_REPORT.value, _render_json(last_run)),
            create_v042_diagnostic_bundle_source(V042DiagnosticBundleSourceKind.RUN_HISTORY.value, run_history.rendered_text),
            create_v042_diagnostic_bundle_source(V042DiagnosticBundleSourceKind.TRACE_SUMMARY.value, _render_json(trace_summary)),
            create_v042_diagnostic_bundle_source(V042DiagnosticBundleSourceKind.TRACE_TIMELINE_SUMMARY.value, timeline.rendered_text if request.include_trace_timeline else "trace timeline omitted"),
            create_v042_diagnostic_bundle_source(V042DiagnosticBundleSourceKind.SESSION_SHOW_LAST.value, session.rendered_text),
            create_v042_diagnostic_bundle_source(V042DiagnosticBundleSourceKind.SKILL_LIST_SUMMARY.value, skills.rendered_text),
            create_v042_diagnostic_bundle_source(V042DiagnosticBundleSourceKind.SKILL_EXECUTION_SUMMARY.value, _render_json(skill_summary)),
            create_v042_diagnostic_bundle_source(V042DiagnosticBundleSourceKind.DENIAL_SUMMARY.value, f"denial_count={trace_summary.denial_count}"),
            create_v042_diagnostic_bundle_source(V042DiagnosticBundleSourceKind.SAFETY_COUNT_SUMMARY.value, f"shell={trace_summary.shell_execution_count}; subagent={trace_summary.subagent_invocation_count}; production={trace_summary.production_certification_count}"),
            create_v042_diagnostic_bundle_source(V042DiagnosticBundleSourceKind.FEEDBACK_SUMMARY.value, feedback_summary.rendered_text),
            create_v042_diagnostic_bundle_source(V042DiagnosticBundleSourceKind.LATEST_FEEDBACK_NOTES.value, _render_feedback_records(feedback_records[-request.max_feedback_items :])),
            create_v042_diagnostic_bundle_source(V042DiagnosticBundleSourceKind.KNOWN_LIMITATIONS.value, "\n".join(f"- {item.title}" for item in limitations)),
            create_v042_diagnostic_bundle_source(V042DiagnosticBundleSourceKind.CLOSED_CAPABILITY_SNAPSHOT.value, _render_json(closed)),
            create_v042_diagnostic_bundle_source(V042DiagnosticBundleSourceKind.V042_TRACK_CLOSURE.value, _render_json(closure)),
            create_v042_diagnostic_bundle_source(V042DiagnosticBundleSourceKind.NEXT_ACTION.value, "v0.43 User Operation Pilot & Process Intelligence Review Loop"),
        )
    )
    return tuple(sources)


def create_v042_diagnostic_bundle_section(section_kind: str, title: str, content: str, source_ids: Sequence[str] = (), **overrides: Any) -> V042DiagnosticBundleSection:
    redacted, _ = _redact_text(content)
    defaults = {
        "section_id": f"v0426-section-{section_kind}",
        "section_kind": section_kind,
        "title": title,
        "content": redacted,
        "source_ids": tuple(source_ids),
        "redacted": True,
        "process_intelligence_relevance": "Supports reconstruction of runtime state, evidence, safety posture, and user feedback as process evidence.",
    }
    return V042DiagnosticBundleSection(**_merge(defaults, overrides))


def build_v042_diagnostic_bundle(request: V042DiagnosticBundleRequest, sources: Sequence[V042DiagnosticBundleSource] | None = None) -> tuple[V042DiagnosticBundleSection, ...]:
    actual_sources = tuple(sources or collect_v042_diagnostic_bundle_sources(request))
    source_by_kind = {source.source_kind: source for source in actual_sources}

    def content(*kinds: str) -> str:
        return "\n\n".join(source_by_kind[kind].summary for kind in kinds if kind in source_by_kind)

    return (
        create_v042_diagnostic_bundle_section(V042DiagnosticBundleSectionKind.HEADER.value, "ChantaCore Diagnostic Bundle", content(V042DiagnosticBundleSourceKind.VERSION.value), (source_by_kind.get(V042DiagnosticBundleSourceKind.VERSION.value).source_id,) if V042DiagnosticBundleSourceKind.VERSION.value in source_by_kind else ()),
        create_v042_diagnostic_bundle_section(V042DiagnosticBundleSectionKind.ENVIRONMENT.value, "Environment", content(V042DiagnosticBundleSourceKind.HOME_STATUS.value, V042DiagnosticBundleSourceKind.PROFILE_STATUS.value)),
        create_v042_diagnostic_bundle_section(V042DiagnosticBundleSectionKind.PROVIDER.value, "Provider", content(V042DiagnosticBundleSourceKind.PROVIDER_STATUS.value, V042DiagnosticBundleSourceKind.PROVIDER_CONFIG_REDACTED.value)),
        create_v042_diagnostic_bundle_section(V042DiagnosticBundleSectionKind.RUN.value, "Run", content(V042DiagnosticBundleSourceKind.LAST_RUN_REPORT.value, V042DiagnosticBundleSourceKind.RUN_HISTORY.value)),
        create_v042_diagnostic_bundle_section(V042DiagnosticBundleSectionKind.TRACE.value, "Trace", content(V042DiagnosticBundleSourceKind.TRACE_SUMMARY.value, V042DiagnosticBundleSourceKind.TRACE_TIMELINE_SUMMARY.value)),
        create_v042_diagnostic_bundle_section(V042DiagnosticBundleSectionKind.SESSION.value, "Session", content(V042DiagnosticBundleSourceKind.SESSION_SHOW_LAST.value)),
        create_v042_diagnostic_bundle_section(V042DiagnosticBundleSectionKind.SKILLS.value, "Skills", content(V042DiagnosticBundleSourceKind.SKILL_LIST_SUMMARY.value, V042DiagnosticBundleSourceKind.SKILL_EXECUTION_SUMMARY.value)),
        create_v042_diagnostic_bundle_section(V042DiagnosticBundleSectionKind.DENIALS.value, "Denials", content(V042DiagnosticBundleSourceKind.DENIAL_SUMMARY.value)),
        create_v042_diagnostic_bundle_section(V042DiagnosticBundleSectionKind.FEEDBACK.value, "Feedback", content(V042DiagnosticBundleSourceKind.FEEDBACK_SUMMARY.value, V042DiagnosticBundleSourceKind.LATEST_FEEDBACK_NOTES.value)),
        create_v042_diagnostic_bundle_section(V042DiagnosticBundleSectionKind.SAFETY.value, "Safety", content(V042DiagnosticBundleSourceKind.SAFETY_COUNT_SUMMARY.value)),
        create_v042_diagnostic_bundle_section(V042DiagnosticBundleSectionKind.LIMITATIONS.value, "Known Limitations", content(V042DiagnosticBundleSourceKind.KNOWN_LIMITATIONS.value)),
        create_v042_diagnostic_bundle_section(V042DiagnosticBundleSectionKind.CLOSED_CAPABILITIES.value, "Closed Capabilities", content(V042DiagnosticBundleSourceKind.CLOSED_CAPABILITY_SNAPSHOT.value)),
        create_v042_diagnostic_bundle_section(V042DiagnosticBundleSectionKind.PROCESS_INTELLIGENCE_REVIEW.value, "Process Intelligence Review", content(V042DiagnosticBundleSourceKind.V042_TRACK_CLOSURE.value)),
        create_v042_diagnostic_bundle_section(V042DiagnosticBundleSectionKind.NEXT_STEPS.value, "Next Steps", content(V042DiagnosticBundleSourceKind.NEXT_ACTION.value)),
    )


def create_v042_diagnostic_safety_report(**overrides: Any) -> V042DiagnosticSafetyReport:
    defaults = {
        "report_id": "v0426-diagnostic-safety-report",
        "report_bundle_calls_provider": False,
        "report_bundle_submits_prompt": False,
        "report_bundle_writes_files_by_default": False,
        "report_bundle_executes_shell": False,
        "report_bundle_invokes_subagent": False,
        "report_bundle_reads_arbitrary_paths": False,
        "report_bundle_scans_filesystem": False,
        "report_bundle_uploads_external": False,
        "secrets_redacted": True,
        "production_certified": False,
    }
    return V042DiagnosticSafetyReport(**_merge(defaults, overrides))


def create_v042_diagnostic_pi_review_packet(sources: Sequence[V042DiagnosticBundleSource] = (), **overrides: Any) -> V042DiagnosticPIReviewPacket:
    source_map = {source.source_kind: source.summary for source in sources}
    safety = source_map.get(V042DiagnosticBundleSourceKind.SAFETY_COUNT_SUMMARY.value, "shell=0; subagent=0; production=0")
    high_risk_zero = "shell=0" in safety and "subagent=0" in safety and "production=0" in safety
    defaults = {
        "packet_id": "v0426-diagnostic-pi-review-packet",
        "profile_id": PROFILE_ID,
        "run_count_summary": source_map.get(V042DiagnosticBundleSourceKind.RUN_HISTORY.value, "run history unavailable"),
        "provider_count_summary": source_map.get(V042DiagnosticBundleSourceKind.TRACE_TIMELINE_SUMMARY.value, "provider summary unavailable"),
        "denial_summary": source_map.get(V042DiagnosticBundleSourceKind.DENIAL_SUMMARY.value, "denial summary unavailable"),
        "skill_summary": source_map.get(V042DiagnosticBundleSourceKind.SKILL_EXECUTION_SUMMARY.value, "skill summary unavailable"),
        "feedback_summary": source_map.get(V042DiagnosticBundleSourceKind.FEEDBACK_SUMMARY.value, "feedback summary unavailable"),
        "safety_summary": safety,
        "process_instance_review_ready": V042DiagnosticBundleSourceKind.RUN_HISTORY.value in source_map and V042DiagnosticBundleSourceKind.TRACE_SUMMARY.value in source_map,
        "evidence_handoff_ready": True,
        "high_risk_counts_zero": high_risk_zero,
    }
    return V042DiagnosticPIReviewPacket(**_merge(defaults, overrides))


def create_v042_diagnostic_copy_paste_text(sections: Sequence[V042DiagnosticBundleSection], **overrides: Any) -> V042DiagnosticCopyPasteText:
    text = "\n\n".join(f"## {section.title}\n{section.content}" for section in sections)
    redacted, _ = _redact_text(text)
    bounded = redacted[:24000]
    defaults = {
        "handoff_id": "v0426-diagnostic-copy-paste-text",
        "title": "ChantaCore Diagnostic Bundle for GPT/Codex",
        "text": bounded,
        "includes_secret_values": False,
        "includes_required_debug_context": "ChantaCore" in bounded and "Safety" in bounded,
        "suitable_for_gpt_or_codex": True,
        "max_length_bounded": True,
    }
    return V042DiagnosticCopyPasteText(**_merge(defaults, overrides))


def _render_bundle_text(sections: Sequence[V042DiagnosticBundleSection], output_format: str) -> str:
    if output_format == V042DiagnosticBundleFormat.MARKDOWN.value:
        return "\n\n".join(f"## {section.title}\n\n{section.content}" for section in sections)
    return "\n\n".join(f"{section.title}\n{section.content}" for section in sections)


def create_v042_diagnostic_bundle_result(request: V042DiagnosticBundleRequest, **overrides: Any) -> V042DiagnosticBundleResult:
    home = _resolve_home(request.home_path, "report bundle") or ""
    sources = collect_v042_diagnostic_bundle_sources(request)
    sections = build_v042_diagnostic_bundle(request, sources)
    safety = create_v042_diagnostic_safety_report()
    pi_packet = create_v042_diagnostic_pi_review_packet(sources, profile_id=request.profile_id)
    copy_text = create_v042_diagnostic_copy_paste_text(sections)
    rendered = copy_text.text if request.copy_paste else _render_bundle_text(sections, request.output_format)
    if request.output_format == V042DiagnosticBundleFormat.JSON.value:
        rendered = _render_json({"sources": sources, "sections": sections, "pi_review_packet": pi_packet, "safety_report": safety})
    rendered, _ = _redact_text(rendered)
    defaults = {
        "result_id": "v0426-diagnostic-bundle-result",
        "request_id": request.request_id,
        "profile_id": request.profile_id,
        "resolved_home_path": home,
        "status": V042DiagnosticBundleStatus.COMPLETED.value if home else V042DiagnosticBundleStatus.BLOCKED.value,
        "sections": sections,
        "sources": sources,
        "rendered_text": rendered,
        "copy_paste_text": copy_text.text,
        "pi_review_packet": pi_packet,
        "safety_report": safety,
        "provider_invoked": False,
        "prompt_submitted": False,
        "filesystem_written": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    return V042DiagnosticBundleResult(**_merge(defaults, overrides))


def create_v042_feedback_list_summary(home_path: str | None, profile_id: str = PROFILE_ID) -> V042FeedbackSummary:
    home = _resolve_home(home_path, "feedback summary") or ""
    return create_v042_feedback_summary(_read_feedback_records(home, profile_id) if home else ())


def create_v0426_readiness_report(**overrides: Any) -> V0426ReadinessReport:
    defaults = {
        "diagnostic_bundle_command_ready": True,
        "diagnostic_copy_paste_ready": True,
        "diagnostic_redaction_ready": True,
        "diagnostic_pi_review_packet_ready": True,
        "feedback_note_command_ready": True,
        "feedback_list_command_ready": True,
        "feedback_show_command_ready": True,
        "feedback_summary_command_ready": True,
        "feedback_store_ready": True,
        "feedback_redaction_ready": True,
        "known_limitations_ready": True,
        "closed_capability_snapshot_ready": True,
        "v042_track_closure_assessment_ready": True,
        "integrated_restore_document_ready": True,
        "v043_handoff_ready": True,
        "ready_for_external_upload": False,
        "ready_for_network_submission": False,
        "ready_for_automatic_issue_creation": False,
        "ready_for_automatic_code_fixing": False,
        "ready_for_shell_execution": False,
        "ready_for_file_edit": False,
        "ready_for_patch_apply": False,
        "ready_for_arbitrary_file_read": False,
        "ready_for_broad_filesystem_scan": False,
        "ready_for_repo_search": False,
        "ready_for_provider_doctor_completion": False,
        "ready_for_provider_tool_calling": False,
        "ready_for_function_calling": False,
        "ready_for_general_agent_loop": False,
        "ready_for_multi_step_agent_loop": False,
        "ready_for_subagent_invocation": False,
        "ready_for_child_session_creation": False,
        "ready_for_memory_write": False,
        "ready_for_autonomous_retry_loop": False,
        "ready_for_dominion_runtime": False,
        "production_certified": False,
    }
    return V0426ReadinessReport(**_merge(defaults, overrides))


def create_v043_user_operation_pilot_handoff(**overrides: Any) -> V043UserOperationPilotHandoff:
    defaults = {
        "target_version": "v0.43.0 User Operation Pilot & Process Intelligence Review Loop",
        "title": "User Operation Pilot & Process Intelligence Review Loop",
        "recommended_focus": (
            "operate ChantaCore as a daily/user-tested personal runtime",
            "collect diagnostic bundles and feedback notes",
            "review trace/process semantics from real usage",
            "refine UX based on feedback evidence",
            "possibly add issue triage from local feedback records",
        ),
        "must_not_open": ("shell_execution", "file_edit", "patch_apply", "subagent_invocation", "production_certification"),
        "production_certified": False,
    }
    return V043UserOperationPilotHandoff(**_merge(defaults, overrides))


REQUIRED_V0426_RESTORE_SECTIONS: tuple[str, ...] = (
    "restore_purpose",
    "one_screen_restore_summary",
    "current_version_and_track",
    "project_context_for_new_codex_session",
    "v0416_user_test_baseline",
    "v0420_ux_baseline_summary",
    "v0421_home_quickstart_summary",
    "v0422_provider_setup_summary",
    "v0423_trace_history_summary",
    "v0424_chat_shell_summary",
    "v0425_skill_execution_summary",
    "diagnostic_bundle_summary",
    "diagnostic_bundle_contract",
    "diagnostic_redaction_contract",
    "diagnostic_pi_review_packet",
    "feedback_loop_summary",
    "feedback_store_contract",
    "feedback_redaction_contract",
    "feedback_commands",
    "known_limitations",
    "closed_capability_snapshot",
    "v042_track_closure_assessment",
    "runtime_opening_status",
    "still_closed_capabilities",
    "required_test_commands",
    "expected_test_interpretation",
    "withdrawal_conditions",
    "v043_handoff",
    "copy_paste_restore_prompt",
)


def create_v0426_integrated_restore_context_snapshot(**overrides: Any) -> V0426IntegratedRestoreContextSnapshot:
    defaults = {
        "current_version": "v0.42.6 Diagnostic Bundle & User Feedback Loop",
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
            "v0.42.4 Interactive Manual Chat Shell",
            "v0.42.5 Bounded Read-only Skill Execution",
            "v0.42.6 Diagnostic Bundle & User Feedback Loop",
        ),
        "open_capabilities": (
            "report_bundle_command",
            "diagnostic_copy_paste_text",
            "diagnostic_redaction",
            "diagnostic_pi_review_packet",
            "feedback_note_command",
            "feedback_list_command",
            "feedback_show_command",
            "feedback_summary_command",
            "bounded_feedback_store",
            "feedback_redaction",
            "known_limitations_record",
            "closed_capability_snapshot",
            "v042_track_closure_assessment",
            "v043_handoff",
            "integrated_restore_document",
        ),
        "closed_capabilities": (
            "external_upload",
            "network_submission",
            "automatic_issue_creation",
            "automatic_code_fixing",
            "shell_execution",
            "file_edit",
            "patch_apply",
            "arbitrary_file_read",
            "broad_filesystem_scan",
            "repo_search",
            "provider_doctor_completion",
            "provider_tool_calling",
            "function_calling",
            "general_agent_loop",
            "multi_step_agent_loop",
            "subagent_invocation",
            "child_session_creation",
            "memory_write",
            "autonomous_retry_loop",
            "dominion_runtime",
            "production_certification",
        ),
    }
    return V0426IntegratedRestoreContextSnapshot(**_merge(defaults, overrides))


def create_v0426_integrated_restore_packet(**overrides: Any) -> V0426IntegratedRestorePacket:
    sections = tuple(V0426IntegratedRestoreSection(section, section.replace("_", " ").title(), True) for section in REQUIRED_V0426_RESTORE_SECTIONS)
    defaults = {
        "packet_id": "v0426-integrated-restore-packet",
        "context_snapshot": create_v0426_integrated_restore_context_snapshot(),
        "sections": sections,
        "single_integrated_doc_path": INTEGRATED_DOC_PATH,
        "separate_restore_doc_created": False,
    }
    return V0426IntegratedRestorePacket(**_merge(defaults, overrides))


def create_v0426_integrated_restore_document_manifest(**overrides: Any) -> V0426IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "v0426-integrated-restore-document-manifest",
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": False,
        "copy_paste_restore_prompt_required": True,
        "suitable_for_new_session_handoff": True,
        "required_sections": REQUIRED_V0426_RESTORE_SECTIONS,
    }
    return V0426IntegratedRestoreDocumentManifest(**_merge(defaults, overrides))


def _handle_report_bundle(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli report bundle")
    parser.add_argument("--home")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--copy-paste", action="store_true")
    parser.add_argument("--format", choices=["text", "markdown", "json", "compact_text"], default="text")
    parser.add_argument("--max-runs", type=int, default=10)
    parser.add_argument("--max-trace-items", type=int, default=20)
    parser.add_argument("--max-feedback-items", type=int, default=10)
    parsed = parser.parse_args(list(args))
    mode = V042DiagnosticBundleMode.COPY_PASTE.value if parsed.copy_paste else V042DiagnosticBundleMode.STANDARD.value
    result = create_v042_diagnostic_bundle_result(
        create_v042_diagnostic_bundle_request(
            parsed.profile,
            parsed.home,
            mode,
            parsed.format,
            parsed.copy_paste,
            True,
            True,
            True,
            True,
            parsed.max_runs,
            parsed.max_trace_items,
            parsed.max_feedback_items,
        )
    )
    print(result.rendered_text)
    return 0 if result.status != V042DiagnosticBundleStatus.BLOCKED.value else 1


def _handle_feedback_note(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli feedback note")
    parser.add_argument("note_text")
    parser.add_argument("--home")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--category", default=V042FeedbackCategory.UNKNOWN.value)
    parser.add_argument("--severity", default=V042FeedbackSeverity.LOW.value)
    parser.add_argument("--no-trace", action="store_true")
    parsed = parser.parse_args(list(args))
    result = append_v042_feedback_note(
        create_v042_feedback_note_request(parsed.note_text, parsed.profile, parsed.home, parsed.category, parsed.severity, trace_feedback=not parsed.no_trace)
    )
    if result.feedback_record:
        print(f"feedback recorded: {result.feedback_record.feedback_id}\ncategory: {result.feedback_record.category}\nseverity: {result.feedback_record.severity}\nnote: {result.feedback_record.note_text_redacted}")
    else:
        print(f"feedback rejected: {result.rejection_reason}")
    return 0 if result.appended else 1


def _handle_feedback_list(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli feedback list")
    parser.add_argument("--home")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--category")
    parser.add_argument("--severity")
    parser.add_argument("--json", action="store_true")
    parsed = parser.parse_args(list(args))
    result = create_v042_feedback_list_result(create_v042_feedback_list_request(parsed.profile, parsed.home, parsed.limit, parsed.category, parsed.severity, "json" if parsed.json else "text"))
    print(result.rendered_text)
    return 0


def _handle_feedback_show(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli feedback show")
    parser.add_argument("target", nargs="?", default="last")
    parser.add_argument("--feedback-id")
    parser.add_argument("--home")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--json", action="store_true")
    parsed = parser.parse_args(list(args))
    target = "feedback_id" if parsed.feedback_id else parsed.target
    result = create_v042_feedback_show_result(create_v042_feedback_show_request(parsed.profile, parsed.home, target, parsed.feedback_id, "json" if parsed.json else "text"))
    print(result.rendered_text)
    return 0 if result.found else 1


def _handle_feedback_summary(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli feedback summary")
    parser.add_argument("--home")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--json", action="store_true")
    parsed = parser.parse_args(list(args))
    summary = create_v042_feedback_list_summary(parsed.home, parsed.profile)
    print(_render_json(summary) if parsed.json else summary.rendered_text)
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] in {"--version", "version"}:
        print(f"chanta-cli v0.41.1 (runtime {V0426_VERSION}; {V0426_RELEASE_NAME})")
        return 0
    if len(args) >= 2 and args[0] == "report" and args[1] == "bundle":
        return _handle_report_bundle(args[2:])
    if len(args) >= 2 and args[0] == "feedback" and args[1] == "note":
        return _handle_feedback_note(args[2:])
    if len(args) >= 2 and args[0] == "feedback" and args[1] == "list":
        return _handle_feedback_list(args[2:])
    if len(args) >= 2 and args[0] == "feedback" and args[1] == "show":
        return _handle_feedback_show(args[2:])
    if len(args) >= 2 and args[0] == "feedback" and args[1] == "summary":
        return _handle_feedback_summary(args[2:])
    return _v0425_main(args)


__all__ = [
    name
    for name in globals()
    if name.startswith("V042")
    or name.startswith("V043")
    or name.startswith("create_v042")
    or name.startswith("collect_v042")
    or name.startswith("build_v042")
    or name.startswith("append_v042")
    or name.startswith("redact_v042")
    or name == "main"
]
