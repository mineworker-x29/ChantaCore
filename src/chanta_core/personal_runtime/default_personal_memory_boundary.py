"""v0.43.2 memory boundary and local note discipline.

This module opens bounded local work notes and memory candidates under the
resolved ChantaCore profile home. It does not write CORE_MEMORY, profile config,
provider config, workspace files, arbitrary files, or persistent memory.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass, is_dataclass
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Mapping, Sequence

from chanta_core.personal_runtime.default_personal_cli_bootstrap import PROFILE_ID
from chanta_core.personal_runtime.default_personal_work_artifacts import (
    V043BusinessArtifactEnvelope,
    get_v043_last_business_artifact,
)


V0432_VERSION = "v0.43.2"
V0432_RELEASE_NAME = "v0.43.2 Work Session Memory Boundary & Local Note Discipline"


class V043MemoryBoundaryClass(StrEnum):
    SESSION_CONTEXT = "session_context"
    BUSINESS_ARTIFACT = "business_artifact"
    LOCAL_WORK_NOTE = "local_work_note"
    FEEDBACK_RECORD = "feedback_record"
    MEMORY_CANDIDATE = "memory_candidate"
    PERSISTENT_MEMORY = "persistent_memory"
    PROFILE_CONFIG = "profile_config"
    PROVIDER_CONFIG = "provider_config"
    WORKSPACE_FILE = "workspace_file"
    UNKNOWN = "unknown"


class V043MemoryMutationStatus(StrEnum):
    OPEN_FOR_BOUNDED_LOCAL_NOTE = "open_for_bounded_local_note"
    OPEN_FOR_MEMORY_CANDIDATE_ONLY = "open_for_memory_candidate_only"
    CLOSED_FOR_PERSISTENT_MEMORY = "closed_for_persistent_memory"
    CLOSED_FOR_CORE_MEMORY = "closed_for_core_memory"
    DENIED = "denied"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class V043LocalNoteStatus(StrEnum):
    RECORDED = "recorded"
    REDACTED = "redacted"
    REJECTED = "rejected"
    LISTED = "listed"
    SHOWN = "shown"
    SEARCHED = "searched"
    NOT_FOUND = "not_found"
    FAILED = "failed"
    UNKNOWN = "unknown"


class V043LocalNoteCategory(StrEnum):
    WORK = "work"
    MEETING = "meeting"
    DECISION = "decision"
    HANDOFF = "handoff"
    PROCESS_REVIEW = "process_review"
    ISSUE = "issue"
    IDEA = "idea"
    REMINDER = "reminder"
    UNKNOWN = "unknown"


class V043MemoryCandidateStatus(StrEnum):
    PROPOSED = "proposed"
    RECORDED_AS_CANDIDATE = "recorded_as_candidate"
    REJECTED = "rejected"
    NOT_PROMOTED = "not_promoted"
    PROMOTED_NOT_ALLOWED = "promoted_not_allowed"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V043MemoryBoundaryPolicy:
    policy_id: str
    session_context_is_memory: bool
    business_artifact_is_memory: bool
    local_note_is_persistent_memory: bool
    feedback_is_memory: bool
    memory_candidate_is_persistent_memory: bool
    automatic_core_memory_write_allowed: bool
    explicit_core_memory_write_allowed: bool
    profile_config_write_allowed: bool
    provider_config_write_allowed: bool
    workspace_write_allowed: bool
    arbitrary_file_read_allowed: bool
    repo_search_allowed: bool
    production_certified: bool


@dataclass(frozen=True)
class V043LocalWorkNoteStorePolicy:
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
    max_note_chars: int
    max_list_limit: int
    max_search_results: int


@dataclass(frozen=True)
class V043MemoryCandidateStorePolicy:
    policy_id: str
    relative_store_path: str
    bounded_to_home: bool
    append_only: bool
    auto_promote_allowed: bool
    core_memory_write_allowed: bool
    stores_secret_values: bool
    requires_future_gate_for_promotion: bool


@dataclass(frozen=True)
class V043LocalWorkNoteRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str | None
    run_id: str | None
    category: str
    note_text: str
    source_command: str
    trace_note: bool


@dataclass(frozen=True)
class V043LocalWorkNoteRecord:
    note_id: str
    profile_id: str
    session_id: str | None
    run_id: str | None
    category: str
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
    core_memory_written: bool
    workspace_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V043LocalWorkNoteAppendResult:
    result_id: str
    note_record: V043LocalWorkNoteRecord | None
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
    core_memory_written: bool
    workspace_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V043LocalWorkNoteListRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    limit: int
    category: str | None
    display_format: str


@dataclass(frozen=True)
class V043LocalWorkNoteListResult:
    result_id: str
    records: tuple[V043LocalWorkNoteRecord, ...]
    count: int
    rendered_text: str
    provider_invoked: bool
    prompt_submitted: bool
    filesystem_written: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V043LocalWorkNoteShowRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    target: str
    note_id: str | None
    display_format: str


@dataclass(frozen=True)
class V043LocalWorkNoteShowResult:
    result_id: str
    found: bool
    record: V043LocalWorkNoteRecord | None
    rendered_text: str
    provider_invoked: bool
    prompt_submitted: bool
    filesystem_written: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V043LocalWorkNoteSearchRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    query: str
    limit: int
    category: str | None
    display_format: str


@dataclass(frozen=True)
class V043LocalWorkNoteSearchResult:
    result_id: str
    query: str
    records: tuple[V043LocalWorkNoteRecord, ...]
    count: int
    searched_only_local_note_store: bool
    broad_filesystem_scan_used: bool
    repo_search_used: bool
    rendered_text: str
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    production_certified: bool


@dataclass(frozen=True)
class V043NoteFromArtifactRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    artifact_id: str | None
    source: str
    category: str
    trace_note: bool


@dataclass(frozen=True)
class V043NoteFromArtifactResult:
    result_id: str
    source_artifact_found: bool
    source_artifact_id: str | None
    note_append_result: V043LocalWorkNoteAppendResult | None
    rendered_text: str
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    core_memory_written: bool
    workspace_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V043MemoryCandidateRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str | None
    candidate_text: str
    reason: str
    source_command: str


@dataclass(frozen=True)
class V043MemoryCandidateRecord:
    candidate_id: str
    profile_id: str
    session_id: str | None
    candidate_text_redacted: str
    reason: str
    status: str
    created_at: str
    promoted_to_persistent_memory: bool
    core_memory_written: bool
    raw_secret_value_persisted: bool
    production_certified: bool


@dataclass(frozen=True)
class V043MemoryCandidateAppendResult:
    result_id: str
    candidate_record: V043MemoryCandidateRecord | None
    store_path: str
    appended: bool
    rejected: bool
    rejection_reason: str | None
    outside_home_paths: tuple[str, ...]
    core_memory_written: bool
    production_certified: bool


@dataclass(frozen=True)
class V043MemoryBoundaryStatusRequest:
    request_id: str
    profile_id: str
    home_path: str | None


@dataclass(frozen=True)
class V043MemoryBoundaryStatusResult:
    result_id: str
    rendered_text: str
    policy: V043MemoryBoundaryPolicy
    local_note_store_policy: V043LocalWorkNoteStorePolicy
    memory_candidate_store_policy: V043MemoryCandidateStorePolicy
    persistent_memory_write_allowed: bool
    automatic_memory_mutation_allowed: bool
    core_memory_written: bool
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    production_certified: bool


@dataclass(frozen=True)
class V043ContextBoundaryRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str | None


@dataclass(frozen=True)
class V043ContextBoundaryResult:
    result_id: str
    rendered_text: str
    session_context_available: bool
    last_artifact_available: bool
    local_notes_available: bool
    feedback_available: bool
    arbitrary_files_available: bool
    repo_search_available: bool
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    production_certified: bool


@dataclass(frozen=True)
class V043LocalNoteTraceRecord:
    trace_record_id: str
    event_kind: str
    note_id: str | None
    candidate_id: str | None
    profile_id: str
    session_id: str | None
    status: str
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    core_memory_written: bool
    workspace_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V043MemoryBoundaryPIReviewRecord:
    review_id: str
    object_kind: str
    object_id: str
    boundary_class: str
    reconstructable_as_process_event: bool
    bounded_store_used: bool
    persistent_memory_untouched: bool
    high_risk_counts_zero: bool
    review_summary: str


@dataclass(frozen=True)
class V043MemoryBoundarySafetyReport:
    report_id: str
    local_note_store_opened: bool
    memory_candidate_store_opened: bool
    persistent_memory_write_allowed: bool
    automatic_memory_mutation_allowed: bool
    core_memory_write_allowed: bool
    profile_config_write_allowed: bool
    provider_config_write_allowed: bool
    workspace_write_allowed: bool
    arbitrary_file_read_allowed: bool
    repo_search_allowed: bool
    shell_execution_allowed: bool
    subagent_allowed: bool
    production_certified: bool


@dataclass(frozen=True)
class V0432ReadinessReport:
    report_id: str
    memory_boundary_policy_ready: bool
    local_work_note_store_ready: bool
    memory_candidate_store_ready: bool
    note_command_ready: bool
    notes_list_show_search_ready: bool
    note_from_artifact_ready: bool
    memory_boundary_status_ready: bool
    context_boundary_status_ready: bool
    local_note_trace_record_ready: bool
    memory_boundary_pi_review_ready: bool
    integrated_restore_document_ready: bool
    v0433_handoff_ready: bool
    ready_for_persistent_memory_write: bool
    ready_for_automatic_memory_mutation: bool
    ready_for_core_memory_write: bool
    ready_for_profile_config_write: bool
    ready_for_provider_config_write: bool
    ready_for_workspace_write: bool
    ready_for_arbitrary_file_read: bool
    ready_for_repo_search: bool
    ready_for_shell_execution: bool
    ready_for_subagent_invocation: bool
    ready_for_general_agent_loop: bool
    ready_for_autonomous_coding: bool
    production_certified: bool


@dataclass(frozen=True)
class V0433WorkSessionRetrievalHandoff:
    handoff_id: str
    target_version: str
    recommended_focus: tuple[str, ...]
    must_not_open: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V0432IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool
    content_summary: str
    restore_value: str


@dataclass(frozen=True)
class V0432IntegratedRestoreContextSnapshot:
    snapshot_id: str
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]
    integrated_doc_path: str
    next_recommended_version: str


@dataclass(frozen=True)
class V0432IntegratedRestorePacket:
    restore_packet_id: str
    snapshot: V0432IntegratedRestoreContextSnapshot
    restore_sections: tuple[V0432IntegratedRestoreSection, ...]
    required_test_commands: tuple[str, ...]
    single_integrated_doc_path: str
    separate_restore_doc_created: bool


@dataclass(frozen=True)
class V0432IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_path: str
    integrated_doc_required: bool
    separate_restore_doc_allowed: bool
    separate_restore_doc_created: bool
    copy_paste_restore_prompt_required: bool
    required_sections_present: bool
    suitable_for_new_session_handoff: bool


def _merge(defaults: dict[str, Any], overrides: Mapping[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    merged.update(overrides)
    return merged


def _now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _new_id(prefix: str) -> str:
    return f"{prefix}-{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}"


def _resolve_home(home_path: str | None) -> str:
    return str(Path(home_path or os.environ.get("CHANTACORE_HOME") or Path.cwd() / ".chantacore-personal").resolve())


def _under_home(path: Path, home: Path) -> bool:
    try:
        path.resolve().relative_to(home.resolve())
        return True
    except ValueError:
        return False


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


def _write_jsonl(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(_json_ready(value), ensure_ascii=False, sort_keys=True) + "\n")


def _read_jsonl(path: Path) -> tuple[dict[str, Any], ...]:
    if not path.exists():
        return ()
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return tuple(rows)


def create_v043_memory_boundary_policy(**overrides: Any) -> V043MemoryBoundaryPolicy:
    defaults = {
        "policy_id": "v0432-memory-boundary-policy",
        "session_context_is_memory": False,
        "business_artifact_is_memory": False,
        "local_note_is_persistent_memory": False,
        "feedback_is_memory": False,
        "memory_candidate_is_persistent_memory": False,
        "automatic_core_memory_write_allowed": False,
        "explicit_core_memory_write_allowed": False,
        "profile_config_write_allowed": False,
        "provider_config_write_allowed": False,
        "workspace_write_allowed": False,
        "arbitrary_file_read_allowed": False,
        "repo_search_allowed": False,
        "production_certified": False,
    }
    return V043MemoryBoundaryPolicy(**_merge(defaults, overrides))


def create_v043_local_work_note_store_policy(**overrides: Any) -> V043LocalWorkNoteStorePolicy:
    defaults = {
        "policy_id": "v0432-local-work-note-store-policy",
        "relative_store_path": "profiles/default-personal/state/work_notes/notes.jsonl",
        "bounded_to_home": True,
        "append_only": True,
        "writes_core_memory": False,
        "writes_profile_config": False,
        "writes_provider_config": False,
        "writes_session_store": False,
        "writes_workspace": False,
        "stores_secret_values": False,
        "max_note_chars": 4000,
        "max_list_limit": 100,
        "max_search_results": 50,
    }
    return V043LocalWorkNoteStorePolicy(**_merge(defaults, overrides))


def create_v043_memory_candidate_store_policy(**overrides: Any) -> V043MemoryCandidateStorePolicy:
    defaults = {
        "policy_id": "v0432-memory-candidate-store-policy",
        "relative_store_path": "profiles/default-personal/state/work_notes/memory_candidates.jsonl",
        "bounded_to_home": True,
        "append_only": True,
        "auto_promote_allowed": False,
        "core_memory_write_allowed": False,
        "stores_secret_values": False,
        "requires_future_gate_for_promotion": True,
    }
    return V043MemoryCandidateStorePolicy(**_merge(defaults, overrides))


def _note_store_path(home_path: str | None) -> Path:
    home = Path(_resolve_home(home_path))
    return home / create_v043_local_work_note_store_policy().relative_store_path


def _candidate_store_path(home_path: str | None) -> Path:
    home = Path(_resolve_home(home_path))
    return home / create_v043_memory_candidate_store_policy().relative_store_path


def create_v043_local_work_note_request(
    note_text: str,
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    session_id: str | None = None,
    run_id: str | None = None,
    category: str = V043LocalNoteCategory.WORK.value,
    source_command: str = "/note",
    trace_note: bool = True,
    **overrides: Any,
) -> V043LocalWorkNoteRequest:
    defaults = {
        "request_id": _new_id("v043-note-request"),
        "profile_id": profile_id,
        "home_path": home_path,
        "session_id": session_id,
        "run_id": run_id,
        "category": category if category in {item.value for item in V043LocalNoteCategory} else V043LocalNoteCategory.UNKNOWN.value,
        "note_text": note_text,
        "source_command": source_command,
        "trace_note": bool(trace_note),
    }
    return V043LocalWorkNoteRequest(**_merge(defaults, overrides))


def redact_v043_local_note_text(text: str, max_chars: int | None = None) -> tuple[str, bool]:
    policy = create_v043_local_work_note_store_policy()
    limit = max_chars or policy.max_note_chars
    redacted = str(text)[:limit]
    patterns = (
        r"sk-[A-Za-z0-9_\-]{12,}",
        r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*[^,\s]+",
        r"Bearer\s+[A-Za-z0-9_\-\.]+",
    )
    changed = len(str(text)) > limit
    for pattern in patterns:
        new_text = re.sub(pattern, "[REDACTED]", redacted)
        changed = changed or new_text != redacted
        redacted = new_text
    return redacted, changed


def create_v043_local_work_note_record(request: V043LocalWorkNoteRequest, **overrides: Any) -> V043LocalWorkNoteRecord:
    redacted, changed = redact_v043_local_note_text(request.note_text)
    defaults = {
        "note_id": _new_id("v043-note"),
        "profile_id": request.profile_id,
        "session_id": request.session_id,
        "run_id": request.run_id,
        "category": request.category,
        "status": V043LocalNoteStatus.REDACTED.value if changed else V043LocalNoteStatus.RECORDED.value,
        "note_text_redacted": redacted,
        "created_at": _now(),
        "source_command": request.source_command,
        "redacted": changed,
        "raw_secret_value_persisted": False,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "core_memory_written": False,
        "workspace_mutated": False,
        "production_certified": False,
    }
    return V043LocalWorkNoteRecord(**_merge(defaults, overrides))


def create_v043_local_work_note_append_result(**overrides: Any) -> V043LocalWorkNoteAppendResult:
    defaults = {
        "result_id": _new_id("v043-note-append-result"),
        "note_record": None,
        "store_path": "",
        "appended": False,
        "rejected": True,
        "rejection_reason": "note_text is empty",
        "trace_event_appended": False,
        "outside_home_paths": (),
        "overwritten_files": (),
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "core_memory_written": False,
        "workspace_mutated": False,
        "production_certified": False,
    }
    return V043LocalWorkNoteAppendResult(**_merge(defaults, overrides))


def append_v043_local_work_note(request: V043LocalWorkNoteRequest, **overrides: Any) -> V043LocalWorkNoteAppendResult:
    home = Path(_resolve_home(request.home_path))
    store_path = _note_store_path(str(home))
    if not request.note_text.strip():
        return create_v043_local_work_note_append_result(store_path=str(store_path), **overrides)
    outside = (str(store_path),) if not _under_home(store_path, home) else ()
    if outside:
        return create_v043_local_work_note_append_result(store_path=str(store_path), rejection_reason="store path outside home", outside_home_paths=outside, **overrides)
    record = create_v043_local_work_note_record(request)
    _write_jsonl(store_path, record)
    return create_v043_local_work_note_append_result(
        note_record=record,
        store_path=str(store_path),
        appended=True,
        rejected=False,
        rejection_reason=None,
        trace_event_appended=False,
        outside_home_paths=(),
        overwritten_files=(),
        **overrides,
    )


def _record_from_row(row: Mapping[str, Any]) -> V043LocalWorkNoteRecord:
    return V043LocalWorkNoteRecord(**{field: row.get(field) for field in V043LocalWorkNoteRecord.__dataclass_fields__})


def _read_note_records(home_path: str | None, profile_id: str) -> tuple[V043LocalWorkNoteRecord, ...]:
    rows = _read_jsonl(_note_store_path(home_path))
    return tuple(_record_from_row(row) for row in rows if row.get("profile_id") == profile_id)


def create_v043_local_work_note_list_request(
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    limit: int = 20,
    category: str | None = None,
    display_format: str = "text",
    **overrides: Any,
) -> V043LocalWorkNoteListRequest:
    bounded_limit = max(1, min(int(limit), create_v043_local_work_note_store_policy().max_list_limit))
    defaults = {"request_id": _new_id("v043-note-list-request"), "profile_id": profile_id, "home_path": home_path, "limit": bounded_limit, "category": category, "display_format": display_format}
    return V043LocalWorkNoteListRequest(**_merge(defaults, overrides))


def create_v043_local_work_note_list_result(**overrides: Any) -> V043LocalWorkNoteListResult:
    defaults = {
        "result_id": _new_id("v043-note-list-result"),
        "records": (),
        "count": 0,
        "rendered_text": "Local work notes\nnotes: 0",
        "provider_invoked": False,
        "prompt_submitted": False,
        "filesystem_written": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    return V043LocalWorkNoteListResult(**_merge(defaults, overrides))


def list_v043_local_work_notes(request: V043LocalWorkNoteListRequest, **overrides: Any) -> V043LocalWorkNoteListResult:
    records = _read_note_records(request.home_path, request.profile_id)
    if request.category:
        records = tuple(record for record in records if record.category == request.category)
    selected = records[-request.limit :]
    rendered = _render_notes("Local work notes", selected)
    return create_v043_local_work_note_list_result(records=selected, count=len(selected), rendered_text=rendered, **overrides)


def create_v043_local_work_note_show_request(
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    target: str = "last",
    note_id: str | None = None,
    display_format: str = "text",
    **overrides: Any,
) -> V043LocalWorkNoteShowRequest:
    defaults = {"request_id": _new_id("v043-note-show-request"), "profile_id": profile_id, "home_path": home_path, "target": target, "note_id": note_id, "display_format": display_format}
    return V043LocalWorkNoteShowRequest(**_merge(defaults, overrides))


def create_v043_local_work_note_show_result(**overrides: Any) -> V043LocalWorkNoteShowResult:
    defaults = {
        "result_id": _new_id("v043-note-show-result"),
        "found": False,
        "record": None,
        "rendered_text": "Local work note not found.",
        "provider_invoked": False,
        "prompt_submitted": False,
        "filesystem_written": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    return V043LocalWorkNoteShowResult(**_merge(defaults, overrides))


def show_v043_local_work_note(request: V043LocalWorkNoteShowRequest, **overrides: Any) -> V043LocalWorkNoteShowResult:
    records = _read_note_records(request.home_path, request.profile_id)
    record = None
    if request.target == "note_id" and request.note_id:
        record = next((item for item in records if item.note_id == request.note_id), None)
    elif request.target == "last" and records:
        record = records[-1]
    if not record:
        return create_v043_local_work_note_show_result(**overrides)
    return create_v043_local_work_note_show_result(found=True, record=record, rendered_text=_render_notes("Local work note", (record,)), **overrides)


def create_v043_local_work_note_search_request(
    query: str,
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    limit: int = 20,
    category: str | None = None,
    display_format: str = "text",
    **overrides: Any,
) -> V043LocalWorkNoteSearchRequest:
    bounded_limit = max(1, min(int(limit), create_v043_local_work_note_store_policy().max_search_results))
    defaults = {"request_id": _new_id("v043-note-search-request"), "profile_id": profile_id, "home_path": home_path, "query": query, "limit": bounded_limit, "category": category, "display_format": display_format}
    return V043LocalWorkNoteSearchRequest(**_merge(defaults, overrides))


def create_v043_local_work_note_search_result(**overrides: Any) -> V043LocalWorkNoteSearchResult:
    defaults = {
        "result_id": _new_id("v043-note-search-result"),
        "query": "",
        "records": (),
        "count": 0,
        "searched_only_local_note_store": True,
        "broad_filesystem_scan_used": False,
        "repo_search_used": False,
        "rendered_text": "Local note search\nmatches: 0",
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "production_certified": False,
    }
    return V043LocalWorkNoteSearchResult(**_merge(defaults, overrides))


def search_v043_local_work_notes(request: V043LocalWorkNoteSearchRequest, **overrides: Any) -> V043LocalWorkNoteSearchResult:
    query = request.query.strip().lower()
    records = _read_note_records(request.home_path, request.profile_id)
    if request.category:
        records = tuple(record for record in records if record.category == request.category)
    matches = tuple(record for record in records if query and query in record.note_text_redacted.lower())[: request.limit]
    rendered = _render_notes(f"Local note search: {request.query}", matches)
    return create_v043_local_work_note_search_result(query=request.query, records=matches, count=len(matches), rendered_text=rendered, **overrides)


def create_v043_note_from_artifact_request(
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    artifact_id: str | None = None,
    source: str = "last_artifact",
    category: str = V043LocalNoteCategory.WORK.value,
    trace_note: bool = True,
    **overrides: Any,
) -> V043NoteFromArtifactRequest:
    defaults = {"request_id": _new_id("v043-note-from-artifact-request"), "profile_id": profile_id, "home_path": home_path, "artifact_id": artifact_id, "source": source, "category": category, "trace_note": bool(trace_note)}
    return V043NoteFromArtifactRequest(**_merge(defaults, overrides))


def create_v043_note_from_artifact_result(**overrides: Any) -> V043NoteFromArtifactResult:
    defaults = {
        "result_id": _new_id("v043-note-from-artifact-result"),
        "source_artifact_found": False,
        "source_artifact_id": None,
        "note_append_result": None,
        "rendered_text": "저장할 최근 업무 산출물이 없습니다.",
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "core_memory_written": False,
        "workspace_mutated": False,
        "production_certified": False,
    }
    return V043NoteFromArtifactResult(**_merge(defaults, overrides))


def create_v043_note_from_artifact(
    request: V043NoteFromArtifactRequest,
    session_id: str | None = None,
    artifact: V043BusinessArtifactEnvelope | None = None,
    **overrides: Any,
) -> V043NoteFromArtifactResult:
    source = artifact or (get_v043_last_business_artifact(session_id or "") if session_id else None)
    if not source:
        return create_v043_note_from_artifact_result(**overrides)
    note_text = f"[artifact:{source.artifact.artifact_id}] {source.artifact.title}\n{source.rendered_text[:3000]}"
    append = append_v043_local_work_note(
        create_v043_local_work_note_request(
            note_text,
            request.profile_id,
            request.home_path,
            session_id,
            source.artifact.run_id,
            request.category,
            "/note from-artifact",
            request.trace_note,
        )
    )
    return create_v043_note_from_artifact_result(
        source_artifact_found=True,
        source_artifact_id=source.artifact.artifact_id,
        note_append_result=append,
        rendered_text=f"업무 산출물을 local work note로 저장했습니다.\nnote_id: {append.note_record.note_id if append.note_record else '-'}\nsource_artifact_id: {source.artifact.artifact_id}\nCORE_MEMORY: untouched",
        **overrides,
    )


def create_v043_memory_candidate_request(
    candidate_text: str,
    reason: str,
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    session_id: str | None = None,
    source_command: str = "/memory-candidate",
    **overrides: Any,
) -> V043MemoryCandidateRequest:
    defaults = {"request_id": _new_id("v043-memory-candidate-request"), "profile_id": profile_id, "home_path": home_path, "session_id": session_id, "candidate_text": candidate_text, "reason": reason, "source_command": source_command}
    return V043MemoryCandidateRequest(**_merge(defaults, overrides))


def create_v043_memory_candidate_record(request: V043MemoryCandidateRequest, **overrides: Any) -> V043MemoryCandidateRecord:
    text, _ = redact_v043_local_note_text(request.candidate_text)
    reason, _ = redact_v043_local_note_text(request.reason, 1000)
    defaults = {
        "candidate_id": _new_id("v043-memory-candidate"),
        "profile_id": request.profile_id,
        "session_id": request.session_id,
        "candidate_text_redacted": text,
        "reason": reason,
        "status": V043MemoryCandidateStatus.RECORDED_AS_CANDIDATE.value,
        "created_at": _now(),
        "promoted_to_persistent_memory": False,
        "core_memory_written": False,
        "raw_secret_value_persisted": False,
        "production_certified": False,
    }
    return V043MemoryCandidateRecord(**_merge(defaults, overrides))


def create_v043_memory_candidate_append_result(**overrides: Any) -> V043MemoryCandidateAppendResult:
    defaults = {
        "result_id": _new_id("v043-memory-candidate-append-result"),
        "candidate_record": None,
        "store_path": "",
        "appended": False,
        "rejected": True,
        "rejection_reason": "candidate_text is empty",
        "outside_home_paths": (),
        "core_memory_written": False,
        "production_certified": False,
    }
    return V043MemoryCandidateAppendResult(**_merge(defaults, overrides))


def append_v043_memory_candidate(request: V043MemoryCandidateRequest, **overrides: Any) -> V043MemoryCandidateAppendResult:
    home = Path(_resolve_home(request.home_path))
    store_path = _candidate_store_path(str(home))
    if not request.candidate_text.strip():
        return create_v043_memory_candidate_append_result(store_path=str(store_path), **overrides)
    outside = (str(store_path),) if not _under_home(store_path, home) else ()
    if outside:
        return create_v043_memory_candidate_append_result(store_path=str(store_path), rejection_reason="candidate store outside home", outside_home_paths=outside, **overrides)
    record = create_v043_memory_candidate_record(request)
    _write_jsonl(store_path, record)
    return create_v043_memory_candidate_append_result(candidate_record=record, store_path=str(store_path), appended=True, rejected=False, rejection_reason=None, outside_home_paths=(), **overrides)


def create_v043_memory_boundary_status_request(profile_id: str = PROFILE_ID, home_path: str | None = None, **overrides: Any) -> V043MemoryBoundaryStatusRequest:
    defaults = {"request_id": _new_id("v043-memory-boundary-status-request"), "profile_id": profile_id, "home_path": home_path}
    return V043MemoryBoundaryStatusRequest(**_merge(defaults, overrides))


def create_v043_memory_boundary_status_result(request: V043MemoryBoundaryStatusRequest | None = None, **overrides: Any) -> V043MemoryBoundaryStatusResult:
    request = request or create_v043_memory_boundary_status_request()
    policy = create_v043_memory_boundary_policy()
    note_policy = create_v043_local_work_note_store_policy()
    candidate_policy = create_v043_memory_candidate_store_policy()
    rendered = "\n".join(
        (
            "Memory Boundary",
            "session context: current context only, not persistent memory",
            "business artifact: session artifact, not persistent memory",
            "local work note: bounded local operational note, not CORE_MEMORY",
            "feedback: improvement evidence, not memory",
            "memory candidate: proposal only, not promoted",
            "persistent memory: closed in v0.43.2",
            "open now: bounded local notes and memory candidates",
            "closed: CORE_MEMORY write, profile/provider config write, workspace write, arbitrary files, repo search, shell, subagents, production certification",
        )
    )
    defaults = {
        "result_id": _new_id("v043-memory-boundary-status-result"),
        "rendered_text": rendered,
        "policy": policy,
        "local_note_store_policy": note_policy,
        "memory_candidate_store_policy": candidate_policy,
        "persistent_memory_write_allowed": False,
        "automatic_memory_mutation_allowed": False,
        "core_memory_written": False,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "production_certified": False,
    }
    return V043MemoryBoundaryStatusResult(**_merge(defaults, overrides))


def create_v043_context_boundary_request(profile_id: str = PROFILE_ID, home_path: str | None = None, session_id: str | None = None, **overrides: Any) -> V043ContextBoundaryRequest:
    defaults = {"request_id": _new_id("v043-context-boundary-request"), "profile_id": profile_id, "home_path": home_path, "session_id": session_id}
    return V043ContextBoundaryRequest(**_merge(defaults, overrides))


def create_v043_context_boundary_result(request: V043ContextBoundaryRequest | None = None, last_artifact_available: bool | None = None, **overrides: Any) -> V043ContextBoundaryResult:
    request = request or create_v043_context_boundary_request()
    records = _read_note_records(request.home_path, request.profile_id)
    artifact_available = bool(last_artifact_available if last_artifact_available is not None else (get_v043_last_business_artifact(request.session_id or "") is not None if request.session_id else False))
    rendered = "\n".join(
        (
            "Context Boundary",
            "can use: explicit user content, bounded recent session turns, last business artifact, last run/report summaries, trace summary",
            f"last artifact available: {str(artifact_available).lower()}",
            f"local notes available: {str(bool(records)).lower()} (only when explicitly shown or searched)",
            "feedback: improvement evidence, not default answer context",
            "arbitrary files: unavailable",
            "repo search: unavailable",
        )
    )
    defaults = {
        "result_id": _new_id("v043-context-boundary-result"),
        "rendered_text": rendered,
        "session_context_available": bool(request.session_id),
        "last_artifact_available": artifact_available,
        "local_notes_available": bool(records),
        "feedback_available": True,
        "arbitrary_files_available": False,
        "repo_search_available": False,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "production_certified": False,
    }
    return V043ContextBoundaryResult(**_merge(defaults, overrides))


def create_v043_local_note_trace_record(
    note_id: str | None = None,
    candidate_id: str | None = None,
    profile_id: str = PROFILE_ID,
    session_id: str | None = None,
    status: str = V043LocalNoteStatus.RECORDED.value,
    event_kind: str | None = None,
    **overrides: Any,
) -> V043LocalNoteTraceRecord:
    defaults = {
        "trace_record_id": _new_id("v043-local-note-trace"),
        "event_kind": event_kind or ("memory_candidate_recorded" if candidate_id else "local_work_note_recorded"),
        "note_id": note_id,
        "candidate_id": candidate_id,
        "profile_id": profile_id,
        "session_id": session_id,
        "status": status,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "core_memory_written": False,
        "workspace_mutated": False,
        "production_certified": False,
    }
    return V043LocalNoteTraceRecord(**_merge(defaults, overrides))


def create_v043_memory_boundary_pi_review_record(
    object_kind: str = "local_work_note",
    object_id: str = "note-test",
    boundary_class: str = V043MemoryBoundaryClass.LOCAL_WORK_NOTE.value,
    **overrides: Any,
) -> V043MemoryBoundaryPIReviewRecord:
    defaults = {
        "review_id": _new_id("v043-memory-boundary-pi-review"),
        "object_kind": object_kind,
        "object_id": object_id,
        "boundary_class": boundary_class,
        "reconstructable_as_process_event": True,
        "bounded_store_used": True,
        "persistent_memory_untouched": True,
        "high_risk_counts_zero": True,
        "review_summary": "Object is bounded operational evidence and does not mutate persistent memory.",
    }
    return V043MemoryBoundaryPIReviewRecord(**_merge(defaults, overrides))


def create_v043_memory_boundary_safety_report(**overrides: Any) -> V043MemoryBoundarySafetyReport:
    defaults = {
        "report_id": "v0432-memory-boundary-safety-report",
        "local_note_store_opened": True,
        "memory_candidate_store_opened": True,
        "persistent_memory_write_allowed": False,
        "automatic_memory_mutation_allowed": False,
        "core_memory_write_allowed": False,
        "profile_config_write_allowed": False,
        "provider_config_write_allowed": False,
        "workspace_write_allowed": False,
        "arbitrary_file_read_allowed": False,
        "repo_search_allowed": False,
        "shell_execution_allowed": False,
        "subagent_allowed": False,
        "production_certified": False,
    }
    return V043MemoryBoundarySafetyReport(**_merge(defaults, overrides))


def create_v0432_readiness_report(**overrides: Any) -> V0432ReadinessReport:
    defaults = {
        "report_id": "v0432-readiness-report",
        "memory_boundary_policy_ready": True,
        "local_work_note_store_ready": True,
        "memory_candidate_store_ready": True,
        "note_command_ready": True,
        "notes_list_show_search_ready": True,
        "note_from_artifact_ready": True,
        "memory_boundary_status_ready": True,
        "context_boundary_status_ready": True,
        "local_note_trace_record_ready": True,
        "memory_boundary_pi_review_ready": True,
        "integrated_restore_document_ready": True,
        "v0433_handoff_ready": True,
        "ready_for_persistent_memory_write": False,
        "ready_for_automatic_memory_mutation": False,
        "ready_for_core_memory_write": False,
        "ready_for_profile_config_write": False,
        "ready_for_provider_config_write": False,
        "ready_for_workspace_write": False,
        "ready_for_arbitrary_file_read": False,
        "ready_for_repo_search": False,
        "ready_for_shell_execution": False,
        "ready_for_subagent_invocation": False,
        "ready_for_general_agent_loop": False,
        "ready_for_autonomous_coding": False,
        "production_certified": False,
    }
    return V0432ReadinessReport(**_merge(defaults, overrides))


def create_v0433_work_session_retrieval_handoff(**overrides: Any) -> V0433WorkSessionRetrievalHandoff:
    defaults = {
        "handoff_id": "v0433-work-session-retrieval-handoff",
        "target_version": "v0.43.3 Work Session Retrieval & Local Evidence Search",
        "recommended_focus": (
            "bounded retrieval over local work notes, feedback, artifacts, and trace summaries",
            "no arbitrary filesystem search",
            "no repo search",
            "no shell",
            "no provider tool calling",
            "no automatic memory mutation",
            "no production certification",
        ),
        "must_not_open": (
            "arbitrary file read/write",
            "repo search",
            "shell execution",
            "subagent invocation",
            "provider tool calling",
            "automatic memory mutation",
            "production certification",
        ),
        "production_certified": False,
    }
    return V0433WorkSessionRetrievalHandoff(**_merge(defaults, overrides))


def create_v0432_integrated_restore_context_snapshot(**overrides: Any) -> V0432IntegratedRestoreContextSnapshot:
    defaults = {
        "snapshot_id": "v0432-integrated-restore-context",
        "current_version": V0432_VERSION,
        "current_track": "v0.43 Business Work Session Pilot & Process Intelligence Review Loop",
        "baseline_versions": ("v0.43.1", "v0.43.0", "v0.42.10"),
        "open_capabilities": ("memory boundary model", "local work note store", "memory candidate store", "bounded note search"),
        "closed_capabilities": create_v0433_work_session_retrieval_handoff().must_not_open,
        "integrated_doc_path": "docs/versions/v0.43/v0.43.2_work_session_memory_boundary_restore.md",
        "next_recommended_version": "v0.43.3",
    }
    return V0432IntegratedRestoreContextSnapshot(**_merge(defaults, overrides))


def create_v0432_integrated_restore_packet(**overrides: Any) -> V0432IntegratedRestorePacket:
    titles = (
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "v0.43.1 Baseline Summary",
        "v0.43.2 Goal",
        "Memory Boundary Model",
        "Session Context vs Persistent Memory",
        "Business Artifacts vs Local Notes",
        "Feedback vs Memory",
        "Memory Candidates",
        "Local Work Note Store",
        "Memory Candidate Store",
        "Note Commands",
        "Memory Boundary Command",
        "Context Boundary Command",
        "Process Intelligence Review Contract",
        "Safety Boundary",
        "Required Test Commands",
        "Manual Pilot Commands",
        "Withdrawal Conditions",
        "v0.43.3 Recommended Next Step",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    )
    sections = tuple(V0432IntegratedRestoreSection(f"v0432-section-{index}", title, True, f"Required v0.43.2 section: {title}", "future-session restore") for index, title in enumerate(titles, 1))
    defaults = {
        "restore_packet_id": "v0432-integrated-restore-packet",
        "snapshot": create_v0432_integrated_restore_context_snapshot(),
        "restore_sections": sections,
        "required_test_commands": (
            "py -m pytest tests\\test_v0432_work_session_memory_boundary.py",
            "py -m pytest tests\\test_v0431_business_flow_artifact_quality.py",
        ),
        "single_integrated_doc_path": "docs/versions/v0.43/v0.43.2_work_session_memory_boundary_restore.md",
        "separate_restore_doc_created": False,
    }
    return V0432IntegratedRestorePacket(**_merge(defaults, overrides))


def create_v0432_integrated_restore_document_manifest(**overrides: Any) -> V0432IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "v0432-integrated-restore-document-manifest",
        "integrated_doc_path": "docs/versions/v0.43/v0.43.2_work_session_memory_boundary_restore.md",
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": False,
        "copy_paste_restore_prompt_required": True,
        "required_sections_present": True,
        "suitable_for_new_session_handoff": True,
    }
    return V0432IntegratedRestoreDocumentManifest(**_merge(defaults, overrides))


def _render_notes(title: str, records: Sequence[V043LocalWorkNoteRecord]) -> str:
    lines = [title, f"notes: {len(records)}"]
    for record in records:
        lines.append(f"- {record.note_id} [{record.category}] {record.note_text_redacted}")
    lines.append("persistent_memory: untouched")
    return "\n".join(lines)


__all__ = [
    name
    for name in globals()
    if name.startswith("V043")
    or name.startswith("create_v043")
    or name.startswith("append_v043")
    or name.startswith("list_v043")
    or name.startswith("show_v043")
    or name.startswith("search_v043")
    or name.startswith("redact_v043")
]
