"""v0.43.3 bounded local evidence retrieval for work sessions.

This module searches only ChantaCore-managed local evidence stores under the
resolved profile home. It does not search arbitrary files, scan repositories,
execute shell commands, call providers, submit prompts, mutate memory, or write
CORE_MEMORY.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Mapping, Sequence

from chanta_core.personal_runtime.default_personal_cli_bootstrap import PROFILE_ID
from chanta_core.personal_runtime.default_personal_trace_history import (
    create_v042_session_show_request,
    create_v042_session_show_result,
)
from chanta_core.personal_runtime.default_personal_trace_report import (
    create_last_run_report,
    create_last_run_report_request,
    create_trace_summary_request,
    summarize_trace_events,
)
from chanta_core.personal_runtime.default_personal_work_artifacts import (
    V043BusinessArtifactEnvelope,
    list_v043_business_artifacts,
)


V0433_VERSION = "v0.43.3"
V0433_RELEASE_NAME = "v0.43.3 Work Session Retrieval & Local Evidence Search"


class V043EvidenceSourceKind(StrEnum):
    LOCAL_WORK_NOTE = "local_work_note"
    MEMORY_CANDIDATE = "memory_candidate"
    BUSINESS_ARTIFACT = "business_artifact"
    FEEDBACK_RECORD = "feedback_record"
    TRACE_SUMMARY = "trace_summary"
    RUN_REPORT = "run_report"
    SESSION_SUMMARY = "session_summary"
    CURRENT_SESSION = "current_session"
    UNKNOWN = "unknown"


class V043EvidenceSourceStatus(StrEnum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    EMPTY = "empty"
    UNREADABLE = "unreadable"
    SKIPPED_BY_POLICY = "skipped_by_policy"
    FAILED = "failed"
    UNKNOWN = "unknown"


class V043EvidenceRetrievalMode(StrEnum):
    DETERMINISTIC_LOCAL = "deterministic_local"
    PROVIDER_SYNTHESIS_DISABLED = "provider_synthesis_disabled"
    SOURCE_DISCLOSURE = "source_disclosure"
    LAST_RESULT = "last_result"
    EXPLAIN = "explain"
    UNKNOWN = "unknown"


class V043EvidenceMatchStrategy(StrEnum):
    SUBSTRING = "substring"
    TOKEN_OVERLAP = "token_overlap"
    EXACT_ID = "exact_id"
    SOURCE_KIND_FILTER = "source_kind_filter"
    TIMESTAMP_HINT = "timestamp_hint"
    NONE = "none"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V043EvidenceBoundaryPolicy:
    policy_id: str
    deterministic_by_default: bool
    provider_invocation_allowed_by_default: bool
    prompt_submission_allowed_by_default: bool
    allowed_source_kinds: tuple[str, ...]
    arbitrary_file_search_allowed: bool
    repo_search_allowed: bool
    workspace_search_allowed: bool
    broad_filesystem_scan_allowed: bool
    external_search_allowed: bool
    shell_execution_allowed: bool
    memory_mutation_allowed: bool
    core_memory_write_allowed: bool
    production_certified: bool


@dataclass(frozen=True)
class V043EvidenceSourcePolicy:
    policy_id: str
    source_kind: str
    relative_path: str | None
    bounded_to_home: bool
    read_only: bool
    append_allowed: bool
    search_allowed: bool
    max_records: int
    max_chars_per_record: int
    secrets_redacted: bool
    unavailable_ok: bool


@dataclass(frozen=True)
class V043EvidenceSourceDescriptor:
    descriptor_id: str
    source_kind: str
    status: str
    resolved_path: str | None
    bounded_to_home: bool
    read_only: bool
    record_count_estimate: int | None
    unavailable_reason: str | None
    searched: bool


@dataclass(frozen=True)
class V043EvidenceSearchRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    query_text: str
    source_kinds: tuple[str, ...]
    limit: int
    include_snippets: bool
    include_source_disclosure: bool
    debug: bool


@dataclass(frozen=True)
class V043EvidenceQuery:
    query_id: str
    raw_query: str
    normalized_query: str
    tokens: tuple[str, ...]
    source_kind_filter: tuple[str, ...]
    limit: int
    match_strategy: str


@dataclass(frozen=True)
class V043EvidenceItem:
    item_id: str
    source_kind: str
    source_id: str | None
    source_path_label: str | None
    title: str
    text: str
    snippet: str
    created_at: str | None
    session_id: str | None
    run_id: str | None
    artifact_id: str | None
    note_id: str | None
    feedback_id: str | None
    memory_candidate_id: str | None
    redacted: bool
    bounded_source: bool
    provider_invoked: bool
    prompt_submitted: bool
    arbitrary_file_read: bool
    repo_search_used: bool
    shell_executed: bool
    production_certified: bool


@dataclass(frozen=True)
class V043EvidenceMatch:
    match_id: str
    item: V043EvidenceItem
    score: float
    score_label: str
    matched_terms: tuple[str, ...]
    match_strategy: str
    rank: int
    explanation: str


@dataclass(frozen=True)
class V043EvidenceSearchResult:
    result_id: str
    query: V043EvidenceQuery
    matches: tuple[V043EvidenceMatch, ...]
    count: int
    searched_sources: tuple[V043EvidenceSourceDescriptor, ...]
    skipped_sources: tuple[V043EvidenceSourceDescriptor, ...]
    rendered_text: str
    provider_invoked: bool
    prompt_submitted: bool
    arbitrary_file_search_used: bool
    repo_search_used: bool
    workspace_search_used: bool
    broad_filesystem_scan_used: bool
    shell_executed: bool
    memory_mutated: bool
    core_memory_written: bool
    production_certified: bool


@dataclass(frozen=True)
class V043EvidenceSourceDisclosure:
    disclosure_id: str
    searched_source_kinds: tuple[str, ...]
    unavailable_source_kinds: tuple[str, ...]
    explicitly_not_searched: tuple[str, ...]
    arbitrary_files_searched: bool
    repo_searched: bool
    external_web_searched: bool
    shell_used: bool
    memory_mutated: bool
    rendered_text: str


@dataclass(frozen=True)
class V043EvidencePack:
    pack_id: str
    query_text: str
    matches: tuple[V043EvidenceMatch, ...]
    source_disclosure: V043EvidenceSourceDisclosure
    created_at: str
    session_id: str | None
    bounded: bool
    provider_invoked: bool
    prompt_submitted: bool
    production_certified: bool


@dataclass(frozen=True)
class V043EvidencePackSummary:
    summary_id: str
    pack_id: str
    match_count: int
    top_source_kinds: tuple[str, ...]
    top_snippets: tuple[str, ...]
    limitations: tuple[str, ...]
    rendered_text: str


@dataclass(frozen=True)
class V043RecallRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    query_text: str
    limit: int


@dataclass(frozen=True)
class V043RecallResult:
    result_id: str
    query_text: str
    evidence_pack: V043EvidencePack
    rendered_text: str
    user_friendly_summary: str
    next_actions: tuple[str, ...]
    no_results_guidance: str | None
    provider_invoked: bool
    prompt_submitted: bool
    production_certified: bool


@dataclass(frozen=True)
class V043EvidenceSourcesRequest:
    request_id: str
    profile_id: str
    home_path: str | None


@dataclass(frozen=True)
class V043EvidenceSourcesResult:
    result_id: str
    source_descriptors: tuple[V043EvidenceSourceDescriptor, ...]
    rendered_text: str
    arbitrary_files_available: bool
    repo_search_available: bool
    external_search_available: bool
    provider_invoked: bool
    prompt_submitted: bool
    production_certified: bool


@dataclass(frozen=True)
class V043EvidenceLastRequest:
    request_id: str
    profile_id: str
    home_path: str | None


@dataclass(frozen=True)
class V043EvidenceLastResult:
    result_id: str
    found: bool
    evidence_pack: V043EvidencePack | None
    rendered_text: str
    provider_invoked: bool
    prompt_submitted: bool
    filesystem_written: bool
    production_certified: bool


@dataclass(frozen=True)
class V043EvidenceExplainRequest:
    request_id: str
    profile_id: str
    home_path: str | None


@dataclass(frozen=True)
class V043EvidenceExplainResult:
    result_id: str
    rendered_text: str
    deterministic_local_search: bool
    arbitrary_file_search_allowed: bool
    repo_search_allowed: bool
    external_search_allowed: bool
    provider_invoked: bool
    prompt_submitted: bool
    memory_mutation_allowed: bool
    production_certified: bool


@dataclass(frozen=True)
class V043EvidenceRetrievalTraceRecord:
    trace_record_id: str
    event_kind: str
    query_text: str
    result_count: int
    searched_source_kinds: tuple[str, ...]
    session_id: str | None
    provider_invoked: bool
    prompt_submitted: bool
    arbitrary_file_search_used: bool
    repo_search_used: bool
    shell_executed: bool
    memory_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V043EvidenceRetrievalPIReviewRecord:
    review_id: str
    retrieval_id: str
    query_text: str
    reconstructable_as_process_event: bool
    bounded_sources_only: bool
    searched_source_kinds: tuple[str, ...]
    explicitly_not_searched: tuple[str, ...]
    high_risk_counts_zero: bool
    review_summary: str


@dataclass(frozen=True)
class V043EvidenceRetrievalSafetyReport:
    report_id: str
    bounded_local_evidence_search_opened: bool
    arbitrary_file_search_allowed: bool
    repo_search_allowed: bool
    workspace_search_allowed: bool
    broad_filesystem_scan_allowed: bool
    external_search_allowed: bool
    shell_execution_allowed: bool
    provider_invocation_by_default_allowed: bool
    prompt_submission_by_default_allowed: bool
    memory_mutation_allowed: bool
    core_memory_write_allowed: bool
    production_certified: bool


@dataclass(frozen=True)
class V0433ReadinessReport:
    report_id: str
    evidence_boundary_policy_ready: bool
    evidence_source_policy_ready: bool
    evidence_source_disclosure_ready: bool
    deterministic_local_search_ready: bool
    recall_command_ready: bool
    evidence_command_ready: bool
    evidence_sources_ready: bool
    evidence_last_ready: bool
    evidence_explain_ready: bool
    retrieval_trace_record_ready: bool
    retrieval_pi_review_ready: bool
    integrated_restore_document_ready: bool
    v0434_handoff_ready: bool
    ready_for_arbitrary_file_search: bool
    ready_for_repo_search: bool
    ready_for_workspace_search: bool
    ready_for_broad_filesystem_scan: bool
    ready_for_external_search: bool
    ready_for_shell_execution: bool
    ready_for_provider_tool_calling: bool
    ready_for_function_calling: bool
    ready_for_subagent_invocation: bool
    ready_for_general_agent_loop: bool
    ready_for_autonomous_coding: bool
    ready_for_memory_mutation: bool
    ready_for_core_memory_write: bool
    production_certified: bool


@dataclass(frozen=True)
class V0434EvidenceGroundedWorkFlowHandoff:
    handoff_id: str
    target_version: str
    recommended_focus: tuple[str, ...]
    must_not_open: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V0433IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool
    content_summary: str
    restore_value: str


@dataclass(frozen=True)
class V0433IntegratedRestoreContextSnapshot:
    snapshot_id: str
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]
    integrated_doc_path: str
    next_recommended_version: str


@dataclass(frozen=True)
class V0433IntegratedRestorePacket:
    restore_packet_id: str
    snapshot: V0433IntegratedRestoreContextSnapshot
    restore_sections: tuple[V0433IntegratedRestoreSection, ...]
    required_test_commands: tuple[str, ...]
    single_integrated_doc_path: str
    separate_restore_doc_created: bool


@dataclass(frozen=True)
class V0433IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_path: str
    integrated_doc_required: bool
    separate_restore_doc_allowed: bool
    separate_restore_doc_created: bool
    copy_paste_restore_prompt_required: bool
    required_sections_present: bool
    suitable_for_new_session_handoff: bool


_LAST_EVIDENCE_PACK_BY_PROFILE: dict[str, V043EvidencePack] = {}


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


def _short(text: str, limit: int = 700) -> str:
    normalized = " ".join(str(text).split())
    return normalized if len(normalized) <= limit else normalized[: limit - 3] + "..."


def _tokens(text: str) -> tuple[str, ...]:
    return tuple(token.lower() for token in re.findall(r"[0-9A-Za-z가-힣_.-]+", text) if token.strip())


def _read_jsonl(path: Path, max_records: int) -> tuple[dict[str, Any], ...]:
    if not path.exists():
        return ()
    rows: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return ()
    for line in lines[-max_records:]:
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            rows.append(value)
    return tuple(rows)


def create_v043_evidence_boundary_policy(**overrides: Any) -> V043EvidenceBoundaryPolicy:
    allowed = (
        V043EvidenceSourceKind.LOCAL_WORK_NOTE.value,
        V043EvidenceSourceKind.MEMORY_CANDIDATE.value,
        V043EvidenceSourceKind.BUSINESS_ARTIFACT.value,
        V043EvidenceSourceKind.FEEDBACK_RECORD.value,
        V043EvidenceSourceKind.TRACE_SUMMARY.value,
        V043EvidenceSourceKind.RUN_REPORT.value,
        V043EvidenceSourceKind.SESSION_SUMMARY.value,
        V043EvidenceSourceKind.CURRENT_SESSION.value,
    )
    defaults = {
        "policy_id": "v0433-evidence-boundary-policy",
        "deterministic_by_default": True,
        "provider_invocation_allowed_by_default": False,
        "prompt_submission_allowed_by_default": False,
        "allowed_source_kinds": allowed,
        "arbitrary_file_search_allowed": False,
        "repo_search_allowed": False,
        "workspace_search_allowed": False,
        "broad_filesystem_scan_allowed": False,
        "external_search_allowed": False,
        "shell_execution_allowed": False,
        "memory_mutation_allowed": False,
        "core_memory_write_allowed": False,
        "production_certified": False,
    }
    return V043EvidenceBoundaryPolicy(**_merge(defaults, overrides))


def create_v043_evidence_source_policy(source_kind: str = V043EvidenceSourceKind.LOCAL_WORK_NOTE.value, **overrides: Any) -> V043EvidenceSourcePolicy:
    relative_paths = {
        V043EvidenceSourceKind.LOCAL_WORK_NOTE.value: "profiles/default-personal/state/work_notes/notes.jsonl",
        V043EvidenceSourceKind.MEMORY_CANDIDATE.value: "profiles/default-personal/state/work_notes/memory_candidates.jsonl",
        V043EvidenceSourceKind.FEEDBACK_RECORD.value: f"profiles/{PROFILE_ID}/state/feedback/feedback.jsonl",
    }
    defaults = {
        "policy_id": f"v0433-evidence-source-policy-{source_kind}",
        "source_kind": source_kind,
        "relative_path": relative_paths.get(source_kind),
        "bounded_to_home": True,
        "read_only": True,
        "append_allowed": False,
        "search_allowed": source_kind in create_v043_evidence_boundary_policy().allowed_source_kinds,
        "max_records": 100,
        "max_chars_per_record": 4000,
        "secrets_redacted": True,
        "unavailable_ok": True,
    }
    return V043EvidenceSourcePolicy(**_merge(defaults, overrides))


def create_v043_evidence_source_descriptor(
    source_kind: str = V043EvidenceSourceKind.LOCAL_WORK_NOTE.value,
    home_path: str | None = None,
    **overrides: Any,
) -> V043EvidenceSourceDescriptor:
    policy = create_v043_evidence_source_policy(source_kind)
    home = Path(_resolve_home(home_path))
    resolved_path = str((home / policy.relative_path).resolve()) if policy.relative_path else None
    status = V043EvidenceSourceStatus.AVAILABLE.value
    count: int | None = None
    reason: str | None = None
    searched = policy.search_allowed
    if source_kind not in create_v043_evidence_boundary_policy().allowed_source_kinds:
        status = V043EvidenceSourceStatus.SKIPPED_BY_POLICY.value
        reason = "source kind is not allowed by v0.43.3 evidence boundary policy"
        searched = False
    elif resolved_path:
        path = Path(resolved_path)
        if not _under_home(path, home):
            status = V043EvidenceSourceStatus.SKIPPED_BY_POLICY.value
            reason = "source path escaped resolved ChantaCore home"
            searched = False
        elif not path.exists():
            status = V043EvidenceSourceStatus.UNAVAILABLE.value
            reason = "bounded evidence store does not exist yet"
        else:
            rows = _read_jsonl(path, policy.max_records)
            count = len(rows)
            status = V043EvidenceSourceStatus.AVAILABLE.value if rows else V043EvidenceSourceStatus.EMPTY.value
    elif source_kind == V043EvidenceSourceKind.BUSINESS_ARTIFACT.value:
        count = len(list_v043_business_artifacts())
        status = V043EvidenceSourceStatus.AVAILABLE.value if count else V043EvidenceSourceStatus.EMPTY.value
    defaults = {
        "descriptor_id": _new_id("v043-evidence-source"),
        "source_kind": source_kind,
        "status": status,
        "resolved_path": resolved_path,
        "bounded_to_home": True,
        "read_only": True,
        "record_count_estimate": count,
        "unavailable_reason": reason,
        "searched": searched,
    }
    return V043EvidenceSourceDescriptor(**_merge(defaults, overrides))


def resolve_v043_evidence_source_descriptors(
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    source_kinds: Sequence[str] | None = None,
    **overrides: Any,
) -> tuple[V043EvidenceSourceDescriptor, ...]:
    del profile_id
    kinds = tuple(source_kinds or create_v043_evidence_boundary_policy().allowed_source_kinds)
    return tuple(create_v043_evidence_source_descriptor(kind, home_path, **overrides) for kind in kinds)


def create_v043_evidence_search_request(
    query_text: str,
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    source_kinds: Sequence[str] | None = None,
    limit: int = 10,
    include_snippets: bool = True,
    include_source_disclosure: bool = True,
    debug: bool = False,
    **overrides: Any,
) -> V043EvidenceSearchRequest:
    bounded_limit = max(1, min(int(limit), 25))
    defaults = {
        "request_id": _new_id("v043-evidence-search-request"),
        "profile_id": profile_id,
        "home_path": home_path,
        "query_text": query_text.strip(),
        "source_kinds": tuple(source_kinds or create_v043_evidence_boundary_policy().allowed_source_kinds),
        "limit": bounded_limit,
        "include_snippets": bool(include_snippets),
        "include_source_disclosure": bool(include_source_disclosure),
        "debug": bool(debug),
    }
    request = V043EvidenceSearchRequest(**_merge(defaults, overrides))
    if not request.query_text:
        raise ValueError("query_text must be non-empty")
    return request


def normalize_v043_evidence_query(query_text: str) -> str:
    return " ".join(str(query_text).lower().split())


def create_v043_evidence_query(request: V043EvidenceSearchRequest, **overrides: Any) -> V043EvidenceQuery:
    normalized = normalize_v043_evidence_query(request.query_text)
    defaults = {
        "query_id": _new_id("v043-evidence-query"),
        "raw_query": request.query_text,
        "normalized_query": normalized,
        "tokens": _tokens(normalized),
        "source_kind_filter": tuple(kind for kind in request.source_kinds if kind in create_v043_evidence_boundary_policy().allowed_source_kinds),
        "limit": request.limit,
        "match_strategy": V043EvidenceMatchStrategy.SUBSTRING.value,
    }
    return V043EvidenceQuery(**_merge(defaults, overrides))


def create_v043_evidence_item(
    source_kind: str = V043EvidenceSourceKind.UNKNOWN.value,
    text: str = "",
    title: str | None = None,
    source_id: str | None = None,
    source_path_label: str | None = None,
    created_at: str | None = None,
    session_id: str | None = None,
    run_id: str | None = None,
    artifact_id: str | None = None,
    note_id: str | None = None,
    feedback_id: str | None = None,
    memory_candidate_id: str | None = None,
    redacted: bool = True,
    **overrides: Any,
) -> V043EvidenceItem:
    clean_text = _short(text, 4000)
    defaults = {
        "item_id": _new_id("v043-evidence-item"),
        "source_kind": source_kind,
        "source_id": source_id,
        "source_path_label": source_path_label,
        "title": title or source_kind.replace("_", " ").title(),
        "text": clean_text,
        "snippet": _short(clean_text, 300),
        "created_at": created_at,
        "session_id": session_id,
        "run_id": run_id,
        "artifact_id": artifact_id,
        "note_id": note_id,
        "feedback_id": feedback_id,
        "memory_candidate_id": memory_candidate_id,
        "redacted": bool(redacted),
        "bounded_source": True,
        "provider_invoked": False,
        "prompt_submitted": False,
        "arbitrary_file_read": False,
        "repo_search_used": False,
        "shell_executed": False,
        "production_certified": False,
    }
    return V043EvidenceItem(**_merge(defaults, overrides))


def _item_from_note(row: Mapping[str, Any], path_label: str) -> V043EvidenceItem:
    note_id = str(row.get("note_id") or "")
    return create_v043_evidence_item(
        V043EvidenceSourceKind.LOCAL_WORK_NOTE.value,
        str(row.get("note_text_redacted") or ""),
        title=f"Local work note {note_id or '-'}",
        source_id=note_id or None,
        source_path_label=path_label,
        created_at=row.get("created_at"),
        session_id=row.get("session_id"),
        run_id=row.get("run_id"),
        note_id=note_id or None,
        redacted=bool(row.get("redacted", True)),
    )


def _item_from_candidate(row: Mapping[str, Any], path_label: str) -> V043EvidenceItem:
    candidate_id = str(row.get("candidate_id") or "")
    text = "\n".join(part for part in (str(row.get("candidate_text_redacted") or ""), str(row.get("reason") or "")) if part)
    return create_v043_evidence_item(
        V043EvidenceSourceKind.MEMORY_CANDIDATE.value,
        text,
        title=f"Memory candidate {candidate_id or '-'}",
        source_id=candidate_id or None,
        source_path_label=path_label,
        created_at=row.get("created_at"),
        session_id=row.get("session_id"),
        memory_candidate_id=candidate_id or None,
        redacted=True,
    )


def _item_from_feedback(row: Mapping[str, Any], path_label: str) -> V043EvidenceItem:
    feedback_id = str(row.get("feedback_id") or row.get("record_id") or "")
    text = str(row.get("note_text_redacted") or row.get("feedback_text_redacted") or row.get("note_text") or "")
    return create_v043_evidence_item(
        V043EvidenceSourceKind.FEEDBACK_RECORD.value,
        text,
        title=f"Feedback {feedback_id or '-'}",
        source_id=feedback_id or None,
        source_path_label=path_label,
        created_at=row.get("created_at"),
        session_id=row.get("session_id"),
        feedback_id=feedback_id or None,
        redacted=True,
    )


def _item_from_artifact(envelope: V043BusinessArtifactEnvelope) -> V043EvidenceItem:
    artifact = envelope.artifact
    text = "\n".join((artifact.title, envelope.rendered_text, envelope.debug_summary))
    return create_v043_evidence_item(
        V043EvidenceSourceKind.BUSINESS_ARTIFACT.value,
        text,
        title=artifact.title,
        source_id=artifact.artifact_id,
        source_path_label="current in-session business artifact cache",
        created_at=artifact.created_at,
        session_id=artifact.session_id,
        run_id=artifact.run_id,
        artifact_id=artifact.artifact_id,
        redacted=True,
    )


def _trace_summary_item(profile_id: str, home_path: str | None) -> tuple[V043EvidenceItem, ...]:
    try:
        summary = summarize_trace_events(create_trace_summary_request(profile_id, _resolve_home(home_path), 50))
    except Exception:
        return ()
    text = "\n".join(
        (
            f"trace events: {summary.total_events}",
            f"run count: {summary.run_count}",
            f"provider calls: {summary.provider_call_count}",
            f"shell executions: {summary.shell_execution_count}",
            f"subagents: {summary.subagent_invocation_count}",
            f"commands: {summary.by_command_name}",
        )
    )
    return (create_v043_evidence_item(V043EvidenceSourceKind.TRACE_SUMMARY.value, text, title="Trace summary", source_id="trace-summary", source_path_label="bounded trace summary"),)


def _run_report_item(profile_id: str, home_path: str | None) -> tuple[V043EvidenceItem, ...]:
    try:
        report = create_last_run_report(create_last_run_report_request(profile_id, _resolve_home(home_path)))
    except Exception:
        return ()
    if not getattr(report, "found", False):
        return ()
    text = "\n".join(
        (
            f"run_id: {report.run_id}",
            f"session_id: {report.session_id}",
            f"status: {report.status}",
            f"user: {report.user_input_preview or '-'}",
            f"assistant: {report.assistant_response_preview or '-'}",
            f"response_parse_status: {getattr(report, 'response_parse_status', None) or '-'}",
        )
    )
    return (
        create_v043_evidence_item(
            V043EvidenceSourceKind.RUN_REPORT.value,
            text,
            title="Last run report",
            source_id=report.run_id,
            source_path_label="bounded last run report",
            created_at=getattr(report, "created_at", None),
            session_id=report.session_id,
            run_id=report.run_id,
        ),
    )


def _session_summary_item(profile_id: str, home_path: str | None) -> tuple[V043EvidenceItem, ...]:
    try:
        result = create_v042_session_show_result(create_v042_session_show_request(profile_id, _resolve_home(home_path), "last", None, "text", True, 10))
    except Exception:
        return ()
    if not getattr(result, "found", False):
        return ()
    text = getattr(result, "rendered_text", "") or str(result)
    return (
        create_v043_evidence_item(
            V043EvidenceSourceKind.SESSION_SUMMARY.value,
            text,
            title="Session summary",
            source_id=getattr(result, "session_id", None),
            source_path_label="bounded session show summary",
            session_id=getattr(result, "session_id", None),
        ),
    )


def load_v043_evidence_items_from_source(
    descriptor: V043EvidenceSourceDescriptor,
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    **overrides: Any,
) -> tuple[V043EvidenceItem, ...]:
    del overrides
    policy = create_v043_evidence_source_policy(descriptor.source_kind)
    if descriptor.status in {V043EvidenceSourceStatus.UNAVAILABLE.value, V043EvidenceSourceStatus.SKIPPED_BY_POLICY.value, V043EvidenceSourceStatus.UNREADABLE.value}:
        return ()
    if descriptor.source_kind == V043EvidenceSourceKind.LOCAL_WORK_NOTE.value and descriptor.resolved_path:
        rows = _read_jsonl(Path(descriptor.resolved_path), policy.max_records)
        return tuple(_item_from_note(row, policy.relative_path or "local note store") for row in rows)
    if descriptor.source_kind == V043EvidenceSourceKind.MEMORY_CANDIDATE.value and descriptor.resolved_path:
        rows = _read_jsonl(Path(descriptor.resolved_path), policy.max_records)
        return tuple(_item_from_candidate(row, policy.relative_path or "memory candidate store") for row in rows)
    if descriptor.source_kind == V043EvidenceSourceKind.FEEDBACK_RECORD.value and descriptor.resolved_path:
        rows = _read_jsonl(Path(descriptor.resolved_path), policy.max_records)
        return tuple(_item_from_feedback(row, policy.relative_path or "feedback store") for row in rows)
    if descriptor.source_kind == V043EvidenceSourceKind.BUSINESS_ARTIFACT.value:
        return tuple(_item_from_artifact(envelope) for envelope in list_v043_business_artifacts())
    if descriptor.source_kind == V043EvidenceSourceKind.TRACE_SUMMARY.value:
        return _trace_summary_item(profile_id, home_path)
    if descriptor.source_kind == V043EvidenceSourceKind.RUN_REPORT.value:
        return _run_report_item(profile_id, home_path)
    if descriptor.source_kind in {V043EvidenceSourceKind.SESSION_SUMMARY.value, V043EvidenceSourceKind.CURRENT_SESSION.value}:
        return _session_summary_item(profile_id, home_path)
    return ()


def load_v043_bounded_evidence_items(
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    source_kinds: Sequence[str] | None = None,
) -> tuple[V043EvidenceItem, ...]:
    items: list[V043EvidenceItem] = []
    for descriptor in resolve_v043_evidence_source_descriptors(profile_id, home_path, source_kinds):
        items.extend(load_v043_evidence_items_from_source(descriptor, profile_id, home_path))
    return tuple(items)


def score_v043_evidence_item(item: V043EvidenceItem, query: V043EvidenceQuery) -> tuple[float, tuple[str, ...], str]:
    text = normalize_v043_evidence_query(" ".join((item.title, item.text, item.source_id or "", item.source_kind)))
    if query.normalized_query and query.normalized_query in text:
        return 1.0, (query.normalized_query,), V043EvidenceMatchStrategy.SUBSTRING.value
    ids = (item.source_id, item.artifact_id, item.note_id, item.feedback_id, item.memory_candidate_id)
    if query.normalized_query and any(query.normalized_query == str(value).lower() for value in ids if value):
        return 1.0, (query.normalized_query,), V043EvidenceMatchStrategy.EXACT_ID.value
    item_tokens = set(_tokens(text))
    query_tokens = set(query.tokens)
    if not query_tokens:
        return 0.0, (), V043EvidenceMatchStrategy.NONE.value
    matched = tuple(sorted(query_tokens & item_tokens))
    score = len(matched) / len(query_tokens)
    return score, matched, V043EvidenceMatchStrategy.TOKEN_OVERLAP.value if matched else V043EvidenceMatchStrategy.NONE.value


def create_v043_evidence_match(
    item: V043EvidenceItem,
    score: float,
    matched_terms: Sequence[str] = (),
    match_strategy: str = V043EvidenceMatchStrategy.NONE.value,
    rank: int = 0,
    **overrides: Any,
) -> V043EvidenceMatch:
    label = "high" if score >= 0.75 else "medium" if score >= 0.35 else "low"
    defaults = {
        "match_id": _new_id("v043-evidence-match"),
        "item": item,
        "score": round(float(score), 4),
        "score_label": label,
        "matched_terms": tuple(matched_terms),
        "match_strategy": match_strategy,
        "rank": int(rank),
        "explanation": f"{match_strategy} match over bounded {item.source_kind} evidence.",
    }
    return V043EvidenceMatch(**_merge(defaults, overrides))


def create_v043_evidence_search_result(
    query: V043EvidenceQuery,
    matches: Sequence[V043EvidenceMatch] = (),
    searched_sources: Sequence[V043EvidenceSourceDescriptor] = (),
    skipped_sources: Sequence[V043EvidenceSourceDescriptor] = (),
    rendered_text: str | None = None,
    **overrides: Any,
) -> V043EvidenceSearchResult:
    defaults = {
        "result_id": _new_id("v043-evidence-search-result"),
        "query": query,
        "matches": tuple(matches),
        "count": len(tuple(matches)),
        "searched_sources": tuple(searched_sources),
        "skipped_sources": tuple(skipped_sources),
        "rendered_text": rendered_text or _render_evidence_search(query.raw_query, tuple(matches), tuple(searched_sources), tuple(skipped_sources), operator_style=True),
        "provider_invoked": False,
        "prompt_submitted": False,
        "arbitrary_file_search_used": False,
        "repo_search_used": False,
        "workspace_search_used": False,
        "broad_filesystem_scan_used": False,
        "shell_executed": False,
        "memory_mutated": False,
        "core_memory_written": False,
        "production_certified": False,
    }
    return V043EvidenceSearchResult(**_merge(defaults, overrides))


def search_v043_local_evidence(request: V043EvidenceSearchRequest, **overrides: Any) -> V043EvidenceSearchResult:
    query = create_v043_evidence_query(request)
    descriptors = resolve_v043_evidence_source_descriptors(request.profile_id, request.home_path, query.source_kind_filter)
    matches: list[V043EvidenceMatch] = []
    for descriptor in descriptors:
        for item in load_v043_evidence_items_from_source(descriptor, request.profile_id, request.home_path):
            score, terms, strategy = score_v043_evidence_item(item, query)
            if score > 0:
                matches.append(create_v043_evidence_match(item, score, terms, strategy))
    ranked = sorted(matches, key=lambda match: (match.score, match.item.created_at or ""), reverse=True)[: query.limit]
    ranked = [create_v043_evidence_match(match.item, match.score, match.matched_terms, match.match_strategy, index + 1) for index, match in enumerate(ranked)]
    searched = tuple(descriptor for descriptor in descriptors if descriptor.searched and descriptor.status != V043EvidenceSourceStatus.SKIPPED_BY_POLICY.value)
    skipped = tuple(descriptor for descriptor in descriptors if descriptor.status in {V043EvidenceSourceStatus.UNAVAILABLE.value, V043EvidenceSourceStatus.EMPTY.value, V043EvidenceSourceStatus.SKIPPED_BY_POLICY.value, V043EvidenceSourceStatus.UNREADABLE.value, V043EvidenceSourceStatus.FAILED.value})
    result = create_v043_evidence_search_result(query, ranked, searched, skipped, **overrides)
    _LAST_EVIDENCE_PACK_BY_PROFILE[request.profile_id] = create_v043_evidence_pack(request.query_text, ranked, create_v043_evidence_source_disclosure(result), session_id=None)
    return result


def create_v043_evidence_source_disclosure(result: V043EvidenceSearchResult | None = None, **overrides: Any) -> V043EvidenceSourceDisclosure:
    searched = tuple(descriptor.source_kind for descriptor in result.searched_sources) if result else ()
    unavailable = tuple(descriptor.source_kind for descriptor in result.skipped_sources) if result else ()
    not_searched = ("arbitrary files", "repo", "workspace", "external web", "shell output", "CORE_MEMORY mutation")
    rendered = "\n".join(
        (
            "Evidence source disclosure",
            f"searched: {', '.join(searched) if searched else '-'}",
            f"unavailable/skipped: {', '.join(unavailable) if unavailable else '-'}",
            "not searched: arbitrary files, repo, workspace, external web, shell output",
            "memory mutated: false",
        )
    )
    defaults = {
        "disclosure_id": _new_id("v043-evidence-disclosure"),
        "searched_source_kinds": searched,
        "unavailable_source_kinds": unavailable,
        "explicitly_not_searched": not_searched,
        "arbitrary_files_searched": False,
        "repo_searched": False,
        "external_web_searched": False,
        "shell_used": False,
        "memory_mutated": False,
        "rendered_text": rendered,
    }
    return V043EvidenceSourceDisclosure(**_merge(defaults, overrides))


def create_v043_evidence_pack(
    query_text: str,
    matches: Sequence[V043EvidenceMatch] = (),
    source_disclosure: V043EvidenceSourceDisclosure | None = None,
    session_id: str | None = None,
    **overrides: Any,
) -> V043EvidencePack:
    defaults = {
        "pack_id": _new_id("v043-evidence-pack"),
        "query_text": query_text,
        "matches": tuple(matches),
        "source_disclosure": source_disclosure or create_v043_evidence_source_disclosure(),
        "created_at": _now(),
        "session_id": session_id,
        "bounded": True,
        "provider_invoked": False,
        "prompt_submitted": False,
        "production_certified": False,
    }
    return V043EvidencePack(**_merge(defaults, overrides))


def create_v043_evidence_pack_summary(pack: V043EvidencePack, **overrides: Any) -> V043EvidencePackSummary:
    source_kinds = tuple(dict.fromkeys(match.item.source_kind for match in pack.matches[:5]))
    snippets = tuple(match.item.snippet for match in pack.matches[:5])
    limitations = ("arbitrary files not searched", "repo not searched", "external web not searched", "provider synthesis disabled by default")
    rendered = "\n".join((f"evidence_pack: {pack.pack_id}", f"matches: {len(pack.matches)}", f"sources: {', '.join(source_kinds) if source_kinds else '-'}", "limitations: " + "; ".join(limitations)))
    defaults = {
        "summary_id": _new_id("v043-evidence-pack-summary"),
        "pack_id": pack.pack_id,
        "match_count": len(pack.matches),
        "top_source_kinds": source_kinds,
        "top_snippets": snippets,
        "limitations": limitations,
        "rendered_text": rendered,
    }
    return V043EvidencePackSummary(**_merge(defaults, overrides))


def create_v043_recall_request(query_text: str, profile_id: str = PROFILE_ID, home_path: str | None = None, limit: int = 5, **overrides: Any) -> V043RecallRequest:
    defaults = {"request_id": _new_id("v043-recall-request"), "profile_id": profile_id, "home_path": home_path, "query_text": query_text.strip(), "limit": max(1, min(int(limit), 10))}
    request = V043RecallRequest(**_merge(defaults, overrides))
    if not request.query_text:
        raise ValueError("query_text must be non-empty")
    return request


def create_v043_recall_result(
    request: V043RecallRequest,
    evidence_pack: V043EvidencePack,
    rendered_text: str | None = None,
    **overrides: Any,
) -> V043RecallResult:
    summary = f"{request.query_text} query found {len(evidence_pack.matches)} bounded local evidence item(s)."
    next_actions = ("Open /evidence <query> for operator-style details.", "Use /evidence sources to inspect retrieval boundaries.")
    no_results = "No bounded local evidence matched. I did not search arbitrary files, repo, web, or shell output." if not evidence_pack.matches else None
    defaults = {
        "result_id": _new_id("v043-recall-result"),
        "query_text": request.query_text,
        "evidence_pack": evidence_pack,
        "rendered_text": rendered_text or _render_recall(request.query_text, evidence_pack),
        "user_friendly_summary": summary,
        "next_actions": next_actions,
        "no_results_guidance": no_results,
        "provider_invoked": False,
        "prompt_submitted": False,
        "production_certified": False,
    }
    return V043RecallResult(**_merge(defaults, overrides))


def execute_v043_recall(request: V043RecallRequest, **overrides: Any) -> V043RecallResult:
    search = search_v043_local_evidence(create_v043_evidence_search_request(request.query_text, request.profile_id, request.home_path, limit=request.limit))
    pack = _LAST_EVIDENCE_PACK_BY_PROFILE.get(request.profile_id) or create_v043_evidence_pack(request.query_text, search.matches, create_v043_evidence_source_disclosure(search))
    return create_v043_recall_result(request, pack, **overrides)


def create_v043_evidence_sources_request(profile_id: str = PROFILE_ID, home_path: str | None = None, **overrides: Any) -> V043EvidenceSourcesRequest:
    defaults = {"request_id": _new_id("v043-evidence-sources-request"), "profile_id": profile_id, "home_path": home_path}
    return V043EvidenceSourcesRequest(**_merge(defaults, overrides))


def create_v043_evidence_sources_result(request: V043EvidenceSourcesRequest, **overrides: Any) -> V043EvidenceSourcesResult:
    descriptors = resolve_v043_evidence_source_descriptors(request.profile_id, request.home_path)
    lines = ["Evidence sources"]
    for descriptor in descriptors:
        label = descriptor.resolved_path or "bounded helper/cache"
        lines.append(f"- {descriptor.source_kind}: {descriptor.status}; path={label}; searched={str(descriptor.searched).lower()}")
    lines.extend(("arbitrary files: unavailable", "repo search: unavailable", "external web: unavailable", "persistent memory mutation: unavailable"))
    defaults = {
        "result_id": _new_id("v043-evidence-sources-result"),
        "source_descriptors": descriptors,
        "rendered_text": "\n".join(lines),
        "arbitrary_files_available": False,
        "repo_search_available": False,
        "external_search_available": False,
        "provider_invoked": False,
        "prompt_submitted": False,
        "production_certified": False,
    }
    return V043EvidenceSourcesResult(**_merge(defaults, overrides))


def execute_v043_evidence_sources(request: V043EvidenceSourcesRequest, **overrides: Any) -> V043EvidenceSourcesResult:
    return create_v043_evidence_sources_result(request, **overrides)


def create_v043_evidence_last_request(profile_id: str = PROFILE_ID, home_path: str | None = None, **overrides: Any) -> V043EvidenceLastRequest:
    defaults = {"request_id": _new_id("v043-evidence-last-request"), "profile_id": profile_id, "home_path": home_path}
    return V043EvidenceLastRequest(**_merge(defaults, overrides))


def create_v043_evidence_last_result(request: V043EvidenceLastRequest, pack: V043EvidencePack | None = None, **overrides: Any) -> V043EvidenceLastResult:
    found = pack is not None
    rendered = create_v043_evidence_pack_summary(pack).rendered_text + "\n\n" + pack.source_disclosure.rendered_text if pack else "No evidence pack is available in this process yet. Run /recall <query> or /evidence <query> first."
    defaults = {
        "result_id": _new_id("v043-evidence-last-result"),
        "found": found,
        "evidence_pack": pack,
        "rendered_text": rendered,
        "provider_invoked": False,
        "prompt_submitted": False,
        "filesystem_written": False,
        "production_certified": False,
    }
    return V043EvidenceLastResult(**_merge(defaults, overrides))


def execute_v043_evidence_last(request: V043EvidenceLastRequest, **overrides: Any) -> V043EvidenceLastResult:
    return create_v043_evidence_last_result(request, _LAST_EVIDENCE_PACK_BY_PROFILE.get(request.profile_id), **overrides)


def get_v043_last_evidence_pack(profile_id: str = PROFILE_ID) -> V043EvidencePack | None:
    return _LAST_EVIDENCE_PACK_BY_PROFILE.get(profile_id)


def create_v043_evidence_explain_request(profile_id: str = PROFILE_ID, home_path: str | None = None, **overrides: Any) -> V043EvidenceExplainRequest:
    defaults = {"request_id": _new_id("v043-evidence-explain-request"), "profile_id": profile_id, "home_path": home_path}
    return V043EvidenceExplainRequest(**_merge(defaults, overrides))


def create_v043_evidence_explain_result(request: V043EvidenceExplainRequest | None = None, **overrides: Any) -> V043EvidenceExplainResult:
    del request
    rendered = "\n".join(
        (
            "Bounded evidence retrieval",
            "method: deterministic local substring and token-overlap search",
            "searched: known ChantaCore evidence stores under resolved home only",
            "not searched: arbitrary files, repo, workspace, external web, shell output",
            "provider: not invoked by default",
            "prompt: not submitted by default",
            "memory: not mutated; CORE_MEMORY untouched",
            "evidence is operational local evidence, not persistent memory.",
        )
    )
    defaults = {
        "result_id": _new_id("v043-evidence-explain-result"),
        "rendered_text": rendered,
        "deterministic_local_search": True,
        "arbitrary_file_search_allowed": False,
        "repo_search_allowed": False,
        "external_search_allowed": False,
        "provider_invoked": False,
        "prompt_submitted": False,
        "memory_mutation_allowed": False,
        "production_certified": False,
    }
    return V043EvidenceExplainResult(**_merge(defaults, overrides))


def execute_v043_evidence_explain(request: V043EvidenceExplainRequest, **overrides: Any) -> V043EvidenceExplainResult:
    return create_v043_evidence_explain_result(request, **overrides)


def create_v043_evidence_retrieval_trace_record(
    query_text: str = "test",
    result_count: int = 0,
    searched_source_kinds: Sequence[str] = (),
    session_id: str | None = None,
    **overrides: Any,
) -> V043EvidenceRetrievalTraceRecord:
    defaults = {
        "trace_record_id": _new_id("v043-evidence-retrieval-trace"),
        "event_kind": "local_evidence_retrieved",
        "query_text": query_text,
        "result_count": int(result_count),
        "searched_source_kinds": tuple(searched_source_kinds),
        "session_id": session_id,
        "provider_invoked": False,
        "prompt_submitted": False,
        "arbitrary_file_search_used": False,
        "repo_search_used": False,
        "shell_executed": False,
        "memory_mutated": False,
        "production_certified": False,
    }
    return V043EvidenceRetrievalTraceRecord(**_merge(defaults, overrides))


def create_v043_evidence_retrieval_pi_review_record(
    retrieval_id: str = "retrieval-test",
    query_text: str = "test",
    searched_source_kinds: Sequence[str] = (),
    explicitly_not_searched: Sequence[str] | None = None,
    **overrides: Any,
) -> V043EvidenceRetrievalPIReviewRecord:
    defaults = {
        "review_id": _new_id("v043-evidence-retrieval-pi-review"),
        "retrieval_id": retrieval_id,
        "query_text": query_text,
        "reconstructable_as_process_event": True,
        "bounded_sources_only": True,
        "searched_source_kinds": tuple(searched_source_kinds),
        "explicitly_not_searched": tuple(explicitly_not_searched or ("arbitrary files", "repo", "external web", "shell output")),
        "high_risk_counts_zero": True,
        "review_summary": "Retrieval is deterministic, source-disclosed, and limited to bounded ChantaCore evidence stores.",
    }
    return V043EvidenceRetrievalPIReviewRecord(**_merge(defaults, overrides))


def create_v043_evidence_retrieval_safety_report(**overrides: Any) -> V043EvidenceRetrievalSafetyReport:
    defaults = {
        "report_id": "v0433-evidence-retrieval-safety-report",
        "bounded_local_evidence_search_opened": True,
        "arbitrary_file_search_allowed": False,
        "repo_search_allowed": False,
        "workspace_search_allowed": False,
        "broad_filesystem_scan_allowed": False,
        "external_search_allowed": False,
        "shell_execution_allowed": False,
        "provider_invocation_by_default_allowed": False,
        "prompt_submission_by_default_allowed": False,
        "memory_mutation_allowed": False,
        "core_memory_write_allowed": False,
        "production_certified": False,
    }
    return V043EvidenceRetrievalSafetyReport(**_merge(defaults, overrides))


def create_v0433_readiness_report(**overrides: Any) -> V0433ReadinessReport:
    defaults = {
        "report_id": "v0433-readiness-report",
        "evidence_boundary_policy_ready": True,
        "evidence_source_policy_ready": True,
        "evidence_source_disclosure_ready": True,
        "deterministic_local_search_ready": True,
        "recall_command_ready": True,
        "evidence_command_ready": True,
        "evidence_sources_ready": True,
        "evidence_last_ready": True,
        "evidence_explain_ready": True,
        "retrieval_trace_record_ready": True,
        "retrieval_pi_review_ready": True,
        "integrated_restore_document_ready": True,
        "v0434_handoff_ready": True,
        "ready_for_arbitrary_file_search": False,
        "ready_for_repo_search": False,
        "ready_for_workspace_search": False,
        "ready_for_broad_filesystem_scan": False,
        "ready_for_external_search": False,
        "ready_for_shell_execution": False,
        "ready_for_provider_tool_calling": False,
        "ready_for_function_calling": False,
        "ready_for_subagent_invocation": False,
        "ready_for_general_agent_loop": False,
        "ready_for_autonomous_coding": False,
        "ready_for_memory_mutation": False,
        "ready_for_core_memory_write": False,
        "production_certified": False,
    }
    return V0433ReadinessReport(**_merge(defaults, overrides))


def create_v0434_evidence_grounded_workflow_handoff(**overrides: Any) -> V0434EvidenceGroundedWorkFlowHandoff:
    defaults = {
        "handoff_id": "v0434-evidence-grounded-workflow-handoff",
        "target_version": "v0.43.4 Evidence-Grounded Business Flow Synthesis",
        "recommended_focus": (
            "explicitly use a retrieved evidence pack as context for summary, decision, and handoff",
            "provider-backed synthesis only when the user explicitly requests it",
            "cite local evidence source ids in generated artifacts",
            "keep arbitrary file search, repo search, shell, and memory mutation closed",
        ),
        "must_not_open": (
            "arbitrary filesystem search",
            "repo search",
            "shell execution",
            "provider tool calling",
            "function calling",
            "subagent invocation",
            "memory mutation",
            "production certification",
        ),
        "production_certified": False,
    }
    return V0434EvidenceGroundedWorkFlowHandoff(**_merge(defaults, overrides))


def create_v0433_integrated_restore_context_snapshot(**overrides: Any) -> V0433IntegratedRestoreContextSnapshot:
    defaults = {
        "snapshot_id": "v0433-integrated-restore-context",
        "current_version": V0433_VERSION,
        "current_track": "v0.43 Business Work Session Pilot & Process Intelligence Review Loop",
        "baseline_versions": ("v0.43.2", "v0.43.1", "v0.43.0", "v0.42.10"),
        "open_capabilities": ("bounded local evidence retrieval", "deterministic local evidence search", "evidence pack", "source disclosure", "/recall", "/evidence"),
        "closed_capabilities": create_v0434_evidence_grounded_workflow_handoff().must_not_open,
        "integrated_doc_path": "docs/versions/v0.43/v0.43.3_work_session_retrieval_local_evidence_restore.md",
        "next_recommended_version": "v0.43.4",
    }
    return V0433IntegratedRestoreContextSnapshot(**_merge(defaults, overrides))


def create_v0433_integrated_restore_packet(**overrides: Any) -> V0433IntegratedRestorePacket:
    titles = (
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "v0.43.2 Baseline Summary",
        "v0.43.3 Goal",
        "Local Evidence Retrieval Concept",
        "Allowed Evidence Sources",
        "Disallowed Search Sources",
        "Evidence Boundary Policy",
        "Evidence Source Policy",
        "Retrieval Commands",
        "Recall Result Format",
        "Evidence Source Disclosure",
        "Evidence Pack",
        "Retrieval Trace Record",
        "PI Review Contract",
        "Safety Boundary",
        "Required Test Commands",
        "Manual Pilot Commands",
        "Withdrawal Conditions",
        "v0.43.4 Recommended Next Step",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    )
    sections = tuple(V0433IntegratedRestoreSection(f"v0433-section-{index}", title, True, f"Required v0.43.3 section: {title}", "future-session restore") for index, title in enumerate(titles, 1))
    defaults = {
        "restore_packet_id": "v0433-integrated-restore-packet",
        "snapshot": create_v0433_integrated_restore_context_snapshot(),
        "restore_sections": sections,
        "required_test_commands": (
            "py -m pytest tests\\test_v0433_work_session_retrieval_local_evidence.py",
            "py -m pytest tests\\test_v0432_work_session_memory_boundary.py",
        ),
        "single_integrated_doc_path": "docs/versions/v0.43/v0.43.3_work_session_retrieval_local_evidence_restore.md",
        "separate_restore_doc_created": False,
    }
    return V0433IntegratedRestorePacket(**_merge(defaults, overrides))


def create_v0433_integrated_restore_document_manifest(**overrides: Any) -> V0433IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "v0433-integrated-restore-document-manifest",
        "integrated_doc_path": "docs/versions/v0.43/v0.43.3_work_session_retrieval_local_evidence_restore.md",
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": False,
        "copy_paste_restore_prompt_required": True,
        "required_sections_present": True,
        "suitable_for_new_session_handoff": True,
    }
    return V0433IntegratedRestoreDocumentManifest(**_merge(defaults, overrides))


def _render_evidence_search(
    query_text: str,
    matches: Sequence[V043EvidenceMatch],
    searched_sources: Sequence[V043EvidenceSourceDescriptor],
    skipped_sources: Sequence[V043EvidenceSourceDescriptor],
    operator_style: bool,
) -> str:
    lines = ["Evidence search" if operator_style else "Recall", f"query: {query_text}", f"matches: {len(matches)}"]
    for match in matches:
        lines.append(f"- rank={match.rank or '-'} score={match.score_label} source={match.item.source_kind} id={match.item.source_id or match.item.item_id}")
        lines.append(f"  snippet: {match.item.snippet}")
    lines.append("searched sources: " + (", ".join(descriptor.source_kind for descriptor in searched_sources) if searched_sources else "-"))
    lines.append("unavailable/skipped sources: " + (", ".join(descriptor.source_kind for descriptor in skipped_sources) if skipped_sources else "-"))
    lines.append("not searched: arbitrary files, repo, workspace, external web, shell output")
    return "\n".join(lines)


def _render_recall(query_text: str, pack: V043EvidencePack) -> str:
    lines = [f"검색어: {query_text}", "찾은 근거:"]
    if not pack.matches:
        lines.append("- 일치하는 bounded local evidence가 없습니다.")
    for match in pack.matches:
        lines.append(f"- [{match.score_label}] {match.item.source_kind} {match.item.source_id or match.item.item_id}")
        lines.append(f"  출처: {match.item.source_path_label or match.item.source_kind}")
        lines.append(f"  요약: {match.item.snippet}")
    lines.extend(("다음 액션:", "- /evidence <query>로 source-oriented 목록을 확인할 수 있습니다.", "- /evidence sources로 검색 경계를 확인할 수 있습니다.", "검색하지 않은 범위: arbitrary files, repo, workspace, external web, shell output"))
    return "\n".join(lines)


__all__ = [
    name
    for name in globals()
    if name.startswith("V043")
    or name.startswith("create_v043")
    or name.startswith("resolve_v043")
    or name.startswith("normalize_v043")
    or name.startswith("load_v043")
    or name.startswith("score_v043")
    or name.startswith("search_v043")
    or name.startswith("execute_v043")
]
