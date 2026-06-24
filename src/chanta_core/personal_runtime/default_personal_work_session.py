"""v0.43.0 business work session pilot for default-personal runtime.

This layer opens a business/work session command surface. It does not open
shell execution, file edit/apply, repo search, subagents, provider tools,
function calling, or autonomous agent loops.
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Sequence

from chanta_core.personal_runtime.default_personal_cli_bootstrap import PROFILE_ID
from chanta_core.personal_runtime.default_personal_diagnostics_feedback import (
    append_v042_feedback_note,
    create_v042_diagnostic_bundle_request,
    create_v042_diagnostic_bundle_result,
    create_v042_feedback_note_request,
    main as _v0426_main,
)
from chanta_core.personal_runtime.default_personal_final_ux_acceptance import (
    main as _v04210_main,
)
from chanta_core.personal_runtime.default_personal_memory_boundary import (
    V0432_RELEASE_NAME,
    V0432_VERSION,
    append_v043_local_work_note,
    create_v043_context_boundary_request,
    create_v043_context_boundary_result,
    create_v043_local_work_note_list_request,
    create_v043_local_work_note_request,
    create_v043_local_work_note_search_request,
    create_v043_local_work_note_show_request,
    create_v043_memory_boundary_status_request,
    create_v043_memory_boundary_status_result,
    create_v043_note_from_artifact,
    create_v043_note_from_artifact_request,
    list_v043_local_work_notes,
    search_v043_local_work_notes,
    show_v043_local_work_note,
)
from chanta_core.personal_runtime.default_personal_local_evidence_retrieval import (
    V0433_RELEASE_NAME,
    V0433_VERSION,
    create_v043_evidence_explain_request,
    create_v043_evidence_last_request,
    create_v043_evidence_search_request,
    create_v043_evidence_sources_request,
    create_v043_recall_request,
    execute_v043_evidence_explain,
    execute_v043_evidence_last,
    execute_v043_evidence_sources,
    execute_v043_recall,
    search_v043_local_evidence,
)
from chanta_core.personal_runtime.default_personal_grounded_synthesis import (
    V0434_RELEASE_NAME,
    V0434_VERSION,
    V043GroundedWorkflowKind,
    create_v043_evidence_used_request,
    create_v043_grounded_artifact_envelope,
    create_v043_grounded_synthesis_request,
    create_v043_grounding_check_request,
    create_v043_use_evidence_request,
    execute_v043_evidence_used,
    execute_v043_grounded_synthesis,
    execute_v043_grounding_check,
    execute_v043_use_evidence,
)
from chanta_core.personal_runtime.default_personal_pilot_review import (
    V0435_RELEASE_NAME,
    V0435_VERSION,
    create_v043_pilot_acceptance_checklist,
    create_v043_pilot_findings_request,
    create_v043_pilot_next_request,
    create_v043_pilot_report_request,
    create_v043_pilot_review_request,
    create_v043_pilot_score_request,
    create_v043_pilot_status_request,
    create_v043_workflow_score_request,
    execute_v043_pilot_findings,
    execute_v043_pilot_next,
    execute_v043_pilot_report,
    execute_v043_pilot_review,
    execute_v043_pilot_score,
    execute_v043_pilot_status,
    execute_v043_workflow_score,
)
from chanta_core.personal_runtime.default_personal_pilot_closure import (
    V0436_RELEASE_NAME,
    V0436_VERSION,
    create_v0436_pilot_close_request,
    create_v0436_polish_findings_request,
    create_v0436_polish_report_request,
    create_v0436_polish_status_request,
    create_v0436_v044_handoff_request,
    create_v0436_v044_readiness_request,
    create_v0436_v044_risks_request,
    create_v0436_v044_scope_request,
    execute_v0436_pilot_close,
    execute_v0436_polish_findings,
    execute_v0436_polish_report,
    execute_v0436_polish_status,
    execute_v0436_v044_handoff,
    execute_v0436_v044_readiness,
    execute_v0436_v044_risks,
    execute_v0436_v044_scope,
)
from chanta_core.personal_runtime.default_personal_conversation_router import (
    V0437_RELEASE_NAME,
    V0437_VERSION,
    create_v0437_route_decision,
    render_v0437_artifact_debug,
    render_v0437_artifact_default,
    render_v0437_default_conversation_answer,
)
from chanta_core.personal_runtime.default_personal_command_palette import (
    create_v0438_slash_command_palette_request,
    read_v0438_interactive_input,
    render_v0438_command_palette,
)
from chanta_core.personal_runtime.default_personal_schumpeter_lobby import (
    V0438_RELEASE_NAME,
    V0438_VERSION,
    create_v0438_start_lobby_render_request,
    render_v0438_about_card,
    render_v0438_start_lobby,
    render_v0438_status_detail,
)
from chanta_core.personal_runtime.default_personal_work_artifacts import (
    V0431_RELEASE_NAME,
    V0431_VERSION,
    build_v043_artifact_from_provider_output,
    create_v043_artifact_last_request,
    create_v043_clarify_request,
    create_v043_revise_artifact_request,
    execute_v043_artifact_last,
    execute_v043_clarify,
    execute_v043_revise_artifact,
    get_v043_last_business_artifact,
)
from chanta_core.schumpeter_tui.app import render_v04310_snapshot
from chanta_core.schumpeter_tui.fullscreen import render_v04311_text_snapshot, run_v04311_fullscreen_tui
from chanta_core.schumpeter_tui.plain_shell import run_v04310_plain_tui
from chanta_core.schumpeter_tui.prompt_toolkit_shell import run_v04310_prompt_toolkit_tui
from chanta_core.schumpeter_tui.snapshot import render_v0439_snapshot
from chanta_core.personal_runtime.default_personal_run import (
    RunCommandInput,
    execute_run_command,
)
from chanta_core.personal_runtime.default_personal_trace_history import (
    create_v042_run_history_request,
    create_v042_run_history_result,
)
from chanta_core.personal_runtime.default_personal_trace_report import (
    create_last_run_report,
    create_last_run_report_request,
    create_trace_summary_request,
    summarize_trace_events,
)


V043_VERSION = "v0.43.0"
V043_RELEASE_NAME = "v0.43.0 Business Work Session Pilot Baseline & Process Intelligence Review Contract"
V043_TRACK_NAME = "Business Work Session Pilot & Process Intelligence Review Loop"


class V043WorkSessionMode(StrEnum):
    GENERAL = "general"
    WORK_SUMMARY = "work_summary"
    MEETING_MEMO = "meeting_memo"
    DECISION_BRIEF = "decision_brief"
    TODO_EXTRACTION = "todo_extraction"
    HANDOFF_NOTE = "handoff_note"
    PROCESS_REVIEW = "process_review"
    ISSUE_DIAGNOSIS = "issue_diagnosis"
    UNKNOWN = "unknown"


class V043WorkFlowKind(StrEnum):
    SUMMARY = "summary"
    TODO = "todo"
    MEMO = "memo"
    DECISION = "decision"
    HANDOFF = "handoff"
    WHAT_HAPPENED = "what_happened"
    CAPABILITIES = "capabilities"
    FEEDBACK = "feedback"
    REPORT = "report"
    UNKNOWN = "unknown"


class V043WorkSessionStatus(StrEnum):
    STARTED = "started"
    ACTIVE = "active"
    COMMAND_COMPLETED = "command_completed"
    PROVIDER_RUN_COMPLETED = "provider_run_completed"
    PROVIDER_RUN_FAILED = "provider_run_failed"
    DETERMINISTIC_RESULT_COMPLETED = "deterministic_result_completed"
    EXITED = "exited"
    FAILED = "failed"
    BLOCKED = "blocked"


class V043WorkSessionCommandKind(StrEnum):
    NEW = "new"
    SUMMARY = "summary"
    TODO = "todo"
    MEMO = "memo"
    DECISION = "decision"
    HANDOFF = "handoff"
    WHAT_HAPPENED = "what_happened"
    CAPABILITIES = "capabilities"
    FEEDBACK = "feedback"
    REPORT = "report"
    ARTIFACT_LAST = "artifact_last"
    REVISE = "revise"
    CLARIFY = "clarify"
    NOTE = "note"
    NOTES = "notes"
    NOTE_LAST = "note_last"
    NOTE_FROM_ARTIFACT = "note_from_artifact"
    NOTES_SEARCH = "notes_search"
    MEMORY_BOUNDARY = "memory_boundary"
    CONTEXT = "context"
    RECALL = "recall"
    EVIDENCE = "evidence"
    EVIDENCE_SOURCES = "evidence_sources"
    EVIDENCE_LAST = "evidence_last"
    EVIDENCE_EXPLAIN = "evidence_explain"
    USE_EVIDENCE = "use_evidence"
    USE_EVIDENCE_LAST = "use_evidence_last"
    GROUNDED_SUMMARY = "grounded_summary"
    GROUNDED_TODO = "grounded_todo"
    GROUNDED_MEMO = "grounded_memo"
    GROUNDED_DECISION = "grounded_decision"
    GROUNDED_HANDOFF = "grounded_handoff"
    GROUNDING_CHECK = "grounding_check"
    EVIDENCE_USED = "evidence_used"
    PILOT_STATUS = "pilot_status"
    PILOT_REVIEW = "pilot_review"
    PILOT_SCORE = "pilot_score"
    PILOT_FINDINGS = "pilot_findings"
    PILOT_NEXT = "pilot_next"
    PILOT_REPORT = "pilot_report"
    ACCEPTANCE = "acceptance"
    WORKFLOW_SCORE = "workflow_score"
    POLISH_STATUS = "polish_status"
    POLISH_FINDINGS = "polish_findings"
    POLISH_REPORT = "polish_report"
    PILOT_CLOSE = "pilot_close"
    V044_READINESS = "v044_readiness"
    V044_SCOPE = "v044_scope"
    V044_RISKS = "v044_risks"
    V044_HANDOFF = "v044_handoff"
    HELP = "help"
    ABOUT = "about"
    STATUS = "status"
    PROVIDER = "provider"
    HISTORY = "history"
    TRACE = "trace"
    EXIT = "exit"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V043TrackIdentity:
    track_id: str
    version: str
    track_name: str
    track_goal: str
    baseline_track: str
    opens_codex_like_coding_capabilities: bool
    opens_business_work_session_pilot: bool
    production_certified: bool


@dataclass(frozen=True)
class V043WorkSessionState:
    state_id: str
    profile_id: str
    home_path: str
    session_id: str
    mode: str
    started_at: str
    last_command: str | None
    last_flow_kind: str | None
    last_run_id: str | None
    turn_count: int
    provider_mode: str
    exited: bool
    production_certified: bool


@dataclass(frozen=True)
class V043WorkSessionStartRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    provider: str | None
    mode: str
    clean_banner: bool
    debug: bool
    force_plain: bool
    force_no_color: bool
    force_no_logo: bool
    terminal_width: int | None


@dataclass(frozen=True)
class V043WorkSessionStartResult:
    result_id: str
    state: V043WorkSessionState
    rendered_text: str
    command_suggestions: tuple[str, ...]
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V043WorkSessionCommand:
    command_id: str
    command_kind: str
    raw_text: str
    user_content: str | None
    provider_backed: bool
    deterministic: bool
    mutates_feedback_store: bool
    exits_session: bool


@dataclass(frozen=True)
class V043WorkSessionCommandResult:
    result_id: str
    command_kind: str
    status: str
    rendered_text: str
    run_id: str | None
    session_id: str
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    workspace_mutated: bool
    memory_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V043BusinessFlowPromptTemplate:
    template_id: str
    flow_kind: str
    system_instruction: str
    output_structure: tuple[str, ...]
    uncertainty_policy: str
    assumption_policy: str
    forbidden_claims: tuple[str, ...]
    korean_polite_language: bool


@dataclass(frozen=True)
class V043BusinessFlowRequest:
    request_id: str
    flow_kind: str
    profile_id: str
    home_path: str | None
    session_id: str
    provider: str | None
    user_content: str
    debug: bool


@dataclass(frozen=True)
class V043BusinessFlowResult:
    result_id: str
    flow_kind: str
    status: str
    rendered_text: str
    run_id: str | None
    session_id: str
    response_parse_status: str | None
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V043CapabilityMapItem:
    item_id: str
    label: str
    description: str
    available: bool
    evidence: str


@dataclass(frozen=True)
class V043CapabilityMap:
    map_id: str
    can_do: tuple[V043CapabilityMapItem, ...]
    cannot_do_yet: tuple[V043CapabilityMapItem, ...]
    rendered_text: str
    honest: bool
    production_certified: bool


@dataclass(frozen=True)
class V043WhatHappenedRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str
    include_trace: bool
    include_run_history: bool


@dataclass(frozen=True)
class V043WhatHappenedResult:
    result_id: str
    status: str
    rendered_text: str
    trace_summary_used: bool
    run_history_used: bool
    session_used: bool
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V043WorkSessionTraceRecord:
    trace_record_id: str
    event_kind: str
    work_session_id: str
    flow_kind: str
    run_id: str | None
    session_id: str
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V043WorkSessionPIReviewCriterion:
    criterion_id: str
    label: str
    evidence_required: tuple[str, ...]
    pass_condition: str
    withdrawal_condition: str


@dataclass(frozen=True)
class V043WorkSessionPIReviewContract:
    contract_id: str
    criteria: tuple[V043WorkSessionPIReviewCriterion, ...]
    process_instance_reconstructable: bool
    requires_work_session_id: bool
    requires_flow_kind: bool
    requires_run_session_linkage: bool
    production_certified: bool


@dataclass(frozen=True)
class V043WorkSessionSafetyReport:
    report_id: str
    business_work_session_opened: bool
    codex_like_coding_capabilities_opened: bool
    shell_execution_allowed: bool
    file_edit_allowed: bool
    patch_apply_allowed: bool
    arbitrary_file_read_allowed: bool
    repo_search_allowed: bool
    provider_tool_calling_allowed: bool
    function_calling_allowed: bool
    subagent_allowed: bool
    general_agent_loop_allowed: bool
    production_certified: bool


@dataclass(frozen=True)
class V043PilotFeedbackCriterion:
    criterion_id: str
    label: str
    observation_prompt: str
    pass_condition: str
    fail_condition: str


@dataclass(frozen=True)
class V043PilotReadinessReport:
    report_id: str
    business_work_session_start_ready: bool
    work_session_command_surface_ready: bool
    business_flow_templates_ready: bool
    capability_map_ready: bool
    what_happened_ready: bool
    feedback_command_ready: bool
    report_command_ready: bool
    pi_review_contract_ready: bool
    pilot_feedback_criteria_ready: bool
    integrated_restore_document_ready: bool
    ready_for_shell_execution: bool
    ready_for_file_edit: bool
    ready_for_patch_apply: bool
    ready_for_arbitrary_file_read: bool
    ready_for_repo_search: bool
    ready_for_provider_tool_calling: bool
    ready_for_function_calling: bool
    ready_for_subagent_invocation: bool
    ready_for_general_agent_loop: bool
    ready_for_autonomous_coding: bool
    production_certified: bool


@dataclass(frozen=True)
class V0431WorkFlowExpansionHandoff:
    handoff_id: str
    target_version: str
    recommended_focus: tuple[str, ...]
    still_closed: tuple[str, ...]


@dataclass(frozen=True)
class V0430IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool
    content_summary: str
    restore_value: str


@dataclass(frozen=True)
class V0430IntegratedRestoreContextSnapshot:
    snapshot_id: str
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]
    integrated_doc_path: str
    next_recommended_version: str


@dataclass(frozen=True)
class V0430IntegratedRestorePacket:
    restore_packet_id: str
    snapshot: V0430IntegratedRestoreContextSnapshot
    restore_sections: tuple[V0430IntegratedRestoreSection, ...]
    required_test_commands: tuple[str, ...]
    single_integrated_doc_path: str
    separate_restore_doc_created: bool


@dataclass(frozen=True)
class V0430IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_path: str
    integrated_doc_required: bool
    separate_restore_doc_allowed: bool
    separate_restore_doc_created: bool
    copy_paste_restore_prompt_required: bool
    required_sections_present: bool
    suitable_for_new_session_handoff: bool


def _merge(defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    merged.update(overrides)
    return merged


def _new_id(prefix: str) -> str:
    return f"{prefix}-{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}"


def _now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _resolve_home(home_path: str | None) -> str:
    return str(Path(home_path or os.environ.get("CHANTACORE_HOME") or Path.cwd() / ".chantacore-personal").resolve())


def create_v043_track_identity(**overrides: Any) -> V043TrackIdentity:
    defaults = {
        "track_id": "v043-business-work-session-pilot",
        "version": V043_VERSION,
        "track_name": V043_TRACK_NAME,
        "track_goal": "Run controlled business work sessions and collect Process Intelligence evidence.",
        "baseline_track": "v0.42 Default Personal Runtime UX Hardening Track",
        "opens_codex_like_coding_capabilities": False,
        "opens_business_work_session_pilot": True,
        "production_certified": False,
    }
    return V043TrackIdentity(**_merge(defaults, overrides))


def create_v043_work_session_state(
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    session_id: str | None = None,
    mode: str = V043WorkSessionMode.GENERAL.value,
    provider: str | None = None,
    **overrides: Any,
) -> V043WorkSessionState:
    defaults = {
        "state_id": _new_id("v043-work-session-state"),
        "profile_id": profile_id,
        "home_path": _resolve_home(home_path),
        "session_id": session_id or _new_id("work-session"),
        "mode": mode,
        "started_at": _now(),
        "last_command": None,
        "last_flow_kind": None,
        "last_run_id": None,
        "turn_count": 0,
        "provider_mode": provider or "configured",
        "exited": False,
        "production_certified": False,
    }
    return V043WorkSessionState(**_merge(defaults, overrides))


def create_v043_work_session_start_request(
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    provider: str | None = None,
    mode: str = V043WorkSessionMode.GENERAL.value,
    clean_banner: bool = True,
    debug: bool = False,
    force_plain: bool = False,
    force_no_color: bool = False,
    force_no_logo: bool = False,
    terminal_width: int | None = None,
    **overrides: Any,
) -> V043WorkSessionStartRequest:
    defaults = {
        "request_id": _new_id("v043-start-request"),
        "profile_id": profile_id,
        "home_path": home_path,
        "provider": provider,
        "mode": mode,
        "clean_banner": bool(clean_banner),
        "debug": bool(debug),
        "force_plain": bool(force_plain),
        "force_no_color": bool(force_no_color),
        "force_no_logo": bool(force_no_logo),
        "terminal_width": terminal_width,
    }
    return V043WorkSessionStartRequest(**_merge(defaults, overrides))


V043_START_COMMAND_SUGGESTIONS = (
    "/summary",
    "/todo",
    "/memo",
    "/decision",
    "/handoff",
    "/what-happened",
    "/artifact last",
    "/revise",
    "/clarify",
    "/note",
    "/notes",
    "/memory-boundary",
    "/context",
    "/recall",
    "/evidence sources",
    "/use-evidence",
    "/grounded-summary",
    "/grounding-check",
    "/evidence used",
    "/pilot status",
    "/pilot review",
    "/pilot score",
    "/pilot findings",
    "/pilot next",
    "/pilot report",
    "/acceptance",
    "/workflow score",
    "/polish status",
    "/polish findings",
    "/polish report",
    "/pilot close",
    "/v044 readiness",
    "/v044 scope",
    "/v044 risks",
    "/v044 handoff",
    "/about",
    "/capabilities",
    "/exit",
)


def _render_start_screen(
    profile_id: str = PROFILE_ID,
    provider_label: str | None = None,
    mode_label: str = "Business Work Session",
    force_plain: bool = False,
    force_no_color: bool = False,
    force_no_logo: bool = False,
    terminal_width: int | None = None,
) -> str:
    request = create_v0438_start_lobby_render_request(
        profile_id=profile_id,
        provider_label=provider_label,
        mode_label=mode_label,
        terminal_width=terminal_width,
        force_plain=force_plain,
        force_no_color=force_no_color,
        force_no_logo=force_no_logo,
    )
    return render_v0438_start_lobby(request).rendered_text


def start_v043_work_session(request: V043WorkSessionStartRequest, **overrides: Any) -> V043WorkSessionStartResult:
    state = create_v043_work_session_state(request.profile_id, request.home_path, mode=request.mode, provider=request.provider)
    defaults = {
        "result_id": _new_id("v043-start-result"),
        "state": state,
        "rendered_text": _render_start_screen(
            profile_id=request.profile_id,
            provider_label=request.provider,
            force_plain=request.force_plain,
            force_no_color=request.force_no_color,
            force_no_logo=request.force_no_logo,
            terminal_width=request.terminal_width,
        ),
        "command_suggestions": V043_START_COMMAND_SUGGESTIONS,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    return V043WorkSessionStartResult(**_merge(defaults, overrides))


def create_v043_work_session_command(raw_text: str = "/capabilities", **overrides: Any) -> V043WorkSessionCommand:
    return parse_v043_work_session_command(raw_text, **overrides)


def parse_v043_work_session_command(raw_text: str, **overrides: Any) -> V043WorkSessionCommand:
    stripped = raw_text.strip()
    head, _, rest = stripped.partition(" ")
    normalized = head.lower()
    aliases = {
        "/new": V043WorkSessionCommandKind.NEW.value,
        "/summary": V043WorkSessionCommandKind.SUMMARY.value,
        "/todo": V043WorkSessionCommandKind.TODO.value,
        "/memo": V043WorkSessionCommandKind.MEMO.value,
        "/decision": V043WorkSessionCommandKind.DECISION.value,
        "/handoff": V043WorkSessionCommandKind.HANDOFF.value,
        "/what-happened": V043WorkSessionCommandKind.WHAT_HAPPENED.value,
        "/capabilities": V043WorkSessionCommandKind.CAPABILITIES.value,
        "/feedback": V043WorkSessionCommandKind.FEEDBACK.value,
        "/report": V043WorkSessionCommandKind.REPORT.value,
        "/revise": V043WorkSessionCommandKind.REVISE.value,
        "/clarify": V043WorkSessionCommandKind.CLARIFY.value,
        "/memory-boundary": V043WorkSessionCommandKind.MEMORY_BOUNDARY.value,
        "/context": V043WorkSessionCommandKind.CONTEXT.value,
        "/recall": V043WorkSessionCommandKind.RECALL.value,
        "/use-evidence": V043WorkSessionCommandKind.USE_EVIDENCE.value,
        "/grounded-summary": V043WorkSessionCommandKind.GROUNDED_SUMMARY.value,
        "/grounded-todo": V043WorkSessionCommandKind.GROUNDED_TODO.value,
        "/grounded-memo": V043WorkSessionCommandKind.GROUNDED_MEMO.value,
        "/grounded-decision": V043WorkSessionCommandKind.GROUNDED_DECISION.value,
        "/grounded-handoff": V043WorkSessionCommandKind.GROUNDED_HANDOFF.value,
        "/grounding-check": V043WorkSessionCommandKind.GROUNDING_CHECK.value,
        "/acceptance": V043WorkSessionCommandKind.ACCEPTANCE.value,
        "/help": V043WorkSessionCommandKind.HELP.value,
        "/about": V043WorkSessionCommandKind.ABOUT.value,
        "/status": V043WorkSessionCommandKind.STATUS.value,
        "/provider": V043WorkSessionCommandKind.PROVIDER.value,
        "/history": V043WorkSessionCommandKind.HISTORY.value,
        "/trace": V043WorkSessionCommandKind.TRACE.value,
        "/exit": V043WorkSessionCommandKind.EXIT.value,
        "/quit": V043WorkSessionCommandKind.EXIT.value,
    }
    if normalized == "/artifact" and rest.strip().lower().startswith("last"):
        kind = V043WorkSessionCommandKind.ARTIFACT_LAST.value
        rest = rest.strip()[len("last") :].strip()
    elif normalized == "/note" and rest.strip().lower() == "last":
        kind = V043WorkSessionCommandKind.NOTE_LAST.value
    elif normalized == "/note" and rest.strip().lower() == "from-artifact":
        kind = V043WorkSessionCommandKind.NOTE_FROM_ARTIFACT.value
    elif normalized == "/note":
        kind = V043WorkSessionCommandKind.NOTE.value
    elif normalized == "/notes" and rest.strip().lower().startswith("search "):
        kind = V043WorkSessionCommandKind.NOTES_SEARCH.value
        rest = rest.strip()[len("search ") :]
    elif normalized == "/notes":
        kind = V043WorkSessionCommandKind.NOTES.value
    elif normalized == "/evidence" and rest.strip().lower() == "sources":
        kind = V043WorkSessionCommandKind.EVIDENCE_SOURCES.value
    elif normalized == "/evidence" and rest.strip().lower() == "last":
        kind = V043WorkSessionCommandKind.EVIDENCE_LAST.value
    elif normalized == "/evidence" and rest.strip().lower() == "explain":
        kind = V043WorkSessionCommandKind.EVIDENCE_EXPLAIN.value
    elif normalized == "/evidence" and rest.strip().lower() == "used":
        kind = V043WorkSessionCommandKind.EVIDENCE_USED.value
    elif normalized == "/evidence":
        kind = V043WorkSessionCommandKind.EVIDENCE.value
    elif normalized == "/use-evidence" and rest.strip().lower() == "last":
        kind = V043WorkSessionCommandKind.USE_EVIDENCE_LAST.value
    elif normalized == "/pilot" and rest.strip().lower() == "status":
        kind = V043WorkSessionCommandKind.PILOT_STATUS.value
    elif normalized == "/pilot" and rest.strip().lower() == "review":
        kind = V043WorkSessionCommandKind.PILOT_REVIEW.value
    elif normalized == "/pilot" and rest.strip().lower() == "score":
        kind = V043WorkSessionCommandKind.PILOT_SCORE.value
    elif normalized == "/pilot" and rest.strip().lower() == "findings":
        kind = V043WorkSessionCommandKind.PILOT_FINDINGS.value
    elif normalized == "/pilot" and rest.strip().lower() == "next":
        kind = V043WorkSessionCommandKind.PILOT_NEXT.value
    elif normalized == "/pilot" and rest.strip().lower() == "report":
        kind = V043WorkSessionCommandKind.PILOT_REPORT.value
    elif normalized == "/workflow" and rest.strip().lower() == "score":
        kind = V043WorkSessionCommandKind.WORKFLOW_SCORE.value
    elif normalized == "/polish" and rest.strip().lower() == "status":
        kind = V043WorkSessionCommandKind.POLISH_STATUS.value
    elif normalized == "/polish" and rest.strip().lower() == "findings":
        kind = V043WorkSessionCommandKind.POLISH_FINDINGS.value
    elif normalized == "/polish" and rest.strip().lower() == "report":
        kind = V043WorkSessionCommandKind.POLISH_REPORT.value
    elif normalized == "/pilot" and rest.strip().lower() == "close":
        kind = V043WorkSessionCommandKind.PILOT_CLOSE.value
    elif normalized == "/v044" and rest.strip().lower() == "readiness":
        kind = V043WorkSessionCommandKind.V044_READINESS.value
    elif normalized == "/v044" and rest.strip().lower() == "scope":
        kind = V043WorkSessionCommandKind.V044_SCOPE.value
    elif normalized == "/v044" and rest.strip().lower() == "risks":
        kind = V043WorkSessionCommandKind.V044_RISKS.value
    elif normalized == "/v044" and rest.strip().lower() == "handoff":
        kind = V043WorkSessionCommandKind.V044_HANDOFF.value
    else:
        kind = aliases.get(normalized, V043WorkSessionCommandKind.UNKNOWN.value)
    provider_backed = kind in {
        V043WorkSessionCommandKind.SUMMARY.value,
        V043WorkSessionCommandKind.TODO.value,
        V043WorkSessionCommandKind.MEMO.value,
        V043WorkSessionCommandKind.DECISION.value,
        V043WorkSessionCommandKind.HANDOFF.value,
        V043WorkSessionCommandKind.REVISE.value,
        V043WorkSessionCommandKind.GROUNDED_SUMMARY.value,
        V043WorkSessionCommandKind.GROUNDED_TODO.value,
        V043WorkSessionCommandKind.GROUNDED_MEMO.value,
        V043WorkSessionCommandKind.GROUNDED_DECISION.value,
        V043WorkSessionCommandKind.GROUNDED_HANDOFF.value,
    }
    defaults = {
        "command_id": _new_id("v043-command"),
        "command_kind": kind,
        "raw_text": raw_text,
        "user_content": rest.strip() or None,
        "provider_backed": provider_backed,
        "deterministic": not provider_backed,
        "mutates_feedback_store": kind == V043WorkSessionCommandKind.FEEDBACK.value,
        "exits_session": kind == V043WorkSessionCommandKind.EXIT.value,
    }
    return V043WorkSessionCommand(**_merge(defaults, overrides))


FLOW_TEMPLATE_STRUCTURE: dict[str, tuple[str, ...]] = {
    V043WorkFlowKind.SUMMARY.value: ("핵심 요약", "주요 근거", "확실한 사실", "가정/불확실성", "다음 액션"),
    V043WorkFlowKind.TODO.value: ("action", "owner", "due date", "dependency", "confidence / unknowns"),
    V043WorkFlowKind.MEMO.value: ("context", "key points", "decisions", "open questions", "next actions"),
    V043WorkFlowKind.DECISION.value: ("issue", "options", "evidence", "tradeoffs", "decision", "risks", "next actions"),
    V043WorkFlowKind.HANDOFF.value: ("background", "current state", "what was done", "remaining work", "risks", "next action"),
    "issue_diagnosis": ("issue", "symptoms", "evidence", "likely causes", "withdrawal conditions", "next checks"),
}


def _mode_for_flow(flow_kind: str) -> str:
    return {
        V043WorkFlowKind.SUMMARY.value: V043WorkSessionMode.WORK_SUMMARY.value,
        V043WorkFlowKind.TODO.value: V043WorkSessionMode.TODO_EXTRACTION.value,
        V043WorkFlowKind.MEMO.value: V043WorkSessionMode.MEETING_MEMO.value,
        V043WorkFlowKind.DECISION.value: V043WorkSessionMode.DECISION_BRIEF.value,
        V043WorkFlowKind.HANDOFF.value: V043WorkSessionMode.HANDOFF_NOTE.value,
        "issue_diagnosis": V043WorkSessionMode.ISSUE_DIAGNOSIS.value,
    }.get(flow_kind, V043WorkSessionMode.UNKNOWN.value)


def create_v043_business_flow_prompt_template(flow_kind: str, **overrides: Any) -> V043BusinessFlowPromptTemplate:
    structure = FLOW_TEMPLATE_STRUCTURE.get(flow_kind, FLOW_TEMPLATE_STRUCTURE[V043WorkFlowKind.SUMMARY.value])
    defaults = {
        "template_id": f"v043-business-flow-template-{flow_kind}",
        "flow_kind": flow_kind,
        "system_instruction": (
            "당신은 ChantaCore default-personal runtime의 업무 보조 에이전트입니다. "
            "한국어 존댓말을 기본으로 사용하고, 사용자가 제공한 사실과 추정을 구분합니다. "
            "외부 실행, 파일 접근, 셸 실행, 테스트 실행, 자동화 수행을 했다고 주장하지 않습니다."
        ),
        "output_structure": tuple(structure),
        "uncertainty_policy": "확인되지 않은 소유자, 기한, 의존성, 수치는 '알 수 없음'으로 명시합니다.",
        "assumption_policy": "사용자가 준 사실과 모델의 해석 또는 가정을 분리해서 표시합니다.",
        "forbidden_claims": (
            "file access",
            "shell execution",
            "external action",
            "production automation",
            "repo search",
            "subagent invocation",
        ),
        "korean_polite_language": True,
    }
    return V043BusinessFlowPromptTemplate(**_merge(defaults, overrides))


def build_v043_business_flow_prompt(request: V043BusinessFlowRequest, template: V043BusinessFlowPromptTemplate | None = None) -> str:
    template = template or create_v043_business_flow_prompt_template(request.flow_kind)
    structure = "\n".join(f"- {item}" for item in template.output_structure)
    unavailable_claims = "파일 접근, 셸 실행, 외부 조치, 운영 자동화, 저장소 검색, 보조 에이전트 호출"
    return "\n".join(
        (
            template.system_instruction,
            "",
            f"업무 흐름: {request.flow_kind}",
            f"세션: {request.session_id}",
            f"출력 구조:",
            structure,
            "",
            f"불확실성 정책: {template.uncertainty_policy}",
            f"가정 정책: {template.assumption_policy}",
            f"금지 주장: {unavailable_claims}",
            "",
            "사용자 제공 내용:",
            request.user_content,
        )
    )


def create_v043_business_flow_request(
    flow_kind: str,
    user_content: str,
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    session_id: str | None = None,
    provider: str | None = None,
    debug: bool = False,
    **overrides: Any,
) -> V043BusinessFlowRequest:
    defaults = {
        "request_id": _new_id("v043-flow-request"),
        "flow_kind": flow_kind,
        "profile_id": profile_id,
        "home_path": home_path,
        "session_id": session_id or _new_id("work-session"),
        "provider": provider,
        "user_content": user_content,
        "debug": bool(debug),
    }
    return V043BusinessFlowRequest(**_merge(defaults, overrides))


def create_v043_business_flow_result(**overrides: Any) -> V043BusinessFlowResult:
    defaults = {
        "result_id": _new_id("v043-flow-result"),
        "flow_kind": V043WorkFlowKind.SUMMARY.value,
        "status": V043WorkSessionStatus.BLOCKED.value,
        "rendered_text": "업무 흐름을 실행할 입력이 부족합니다.",
        "run_id": None,
        "session_id": "work-session",
        "response_parse_status": None,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    return V043BusinessFlowResult(**_merge(defaults, overrides))


def _provider_run_id(run_result: Any) -> str | None:
    return getattr(getattr(run_result, "run_result", None), "result_id", None)


def _provider_parse_status(run_result: Any) -> str | None:
    provider_response = getattr(getattr(run_result, "run_result", None), "provider_response", None)
    return getattr(provider_response, "response_parse_status", None)


def _render_business_flow_output(raw_text: str) -> str:
    hidden_prefixes = (
        "[v0.41.4",
        "profile:",
        "session:",
        "trace runtime",
        "provider text is untrusted",
    )
    lines = [line for line in raw_text.splitlines() if not line.strip().startswith(hidden_prefixes)]
    while lines and not lines[0].strip():
        lines.pop(0)
    body = "\n".join(lines).strip() or "응답 본문이 비어 있습니다. /what-happened 또는 /report로 상태를 확인해 주세요."
    return "\n".join(("ChantaCore Work Result", "", body))


def execute_v043_business_flow(request: V043BusinessFlowRequest, **overrides: Any) -> V043BusinessFlowResult:
    if not request.user_content.strip():
        return create_v043_business_flow_result(
            flow_kind=request.flow_kind,
            status=V043WorkSessionStatus.BLOCKED.value,
            rendered_text="정리할 업무 내용이 없습니다. 명령 뒤에 내용을 붙여 주세요.",
            session_id=request.session_id,
            **overrides,
        )
    home = _resolve_home(request.home_path)
    prompt = build_v043_business_flow_prompt(request)
    run = execute_run_command(
        RunCommandInput(
            profile_id=request.profile_id,
            home_path=home,
            user_input=prompt,
            session_id=request.session_id,
            provider=request.provider,
            mock_provider=request.provider == "mock",
            timeout_seconds=60.0,
        )
    )
    status = V043WorkSessionStatus.PROVIDER_RUN_COMPLETED.value if run.exit_code == 0 else V043WorkSessionStatus.PROVIDER_RUN_FAILED.value
    envelope = build_v043_artifact_from_provider_output(
        request.flow_kind,
        run.rendered_text,
        run.run_result.session_id,
        _provider_run_id(run),
        run.provider_invoked,
        run.prompt_submitted,
        _provider_parse_status(run),
    )
    return create_v043_business_flow_result(
        result_id=_new_id("v043-flow-result"),
        flow_kind=request.flow_kind,
        status=status,
        rendered_text=envelope.rendered_text,
        run_id=_provider_run_id(run),
        session_id=run.run_result.session_id,
        response_parse_status=_provider_parse_status(run),
        provider_invoked=run.provider_invoked,
        prompt_submitted=run.prompt_submitted,
        shell_executed=False,
        subagent_invoked=False,
        production_certified=False,
        **overrides,
    )


def create_v043_capability_map(**overrides: Any) -> V043CapabilityMap:
    can_do = (
        V043CapabilityMapItem("business-conversation", "business conversation", "업무 대화를 정리하고 답변합니다.", True, "v0.42 run/chat UX"),
        V043CapabilityMapItem("summary", "summary", "현재 입력이나 세션 내용을 요약합니다.", True, "v0.43 /summary"),
        V043CapabilityMapItem("memo", "memo", "회의/업무 메모 형식으로 정리합니다.", True, "v0.43 /memo"),
        V043CapabilityMapItem("todo", "todo extraction", "다음 액션과 미확정 요소를 뽑습니다.", True, "v0.43 /todo"),
        V043CapabilityMapItem("decision", "decision brief", "판단 근거와 리스크를 구조화합니다.", True, "v0.43 /decision"),
        V043CapabilityMapItem("handoff", "handoff note", "다음 사람이나 세션에 넘길 내용을 작성합니다.", True, "v0.43 /handoff"),
        V043CapabilityMapItem("provider-status", "provider status", "provider 상태를 확인하는 기존 표면을 유지합니다.", True, "v0.42 provider UX"),
        V043CapabilityMapItem("trace-review", "trace/run review", "trace와 run history를 검토할 수 있습니다.", True, "v0.42 trace/report"),
        V043CapabilityMapItem("diagnostic-bundle", "diagnostic bundle", "진단 번들을 만들거나 안내합니다.", True, "v0.42.6 report"),
        V043CapabilityMapItem("feedback-note", "feedback note", "bounded feedback note를 남깁니다.", True, "v0.42.6 feedback"),
        V043CapabilityMapItem("read-only-skills", "bounded read-only skill execution", "허용된 읽기 전용 skill 실행 표면을 유지합니다.", True, "v0.42.5 skills"),
    )
    cannot = (
        V043CapabilityMapItem("shell", "shell execution", "셸 명령 실행은 열려 있지 않습니다.", False, "v0.43 safety boundary"),
        V043CapabilityMapItem("file-edit-apply", "file edit/apply", "파일 편집과 패치 적용은 열려 있지 않습니다.", False, "v0.43 safety boundary"),
        V043CapabilityMapItem("arbitrary-file-read", "arbitrary file read", "임의 파일 읽기나 광범위 파일 접근은 열려 있지 않습니다.", False, "v0.43 safety boundary"),
        V043CapabilityMapItem("repo-search", "repo search", "저장소 검색/스캔은 업무 세션 기능으로 열지 않습니다.", False, "v0.43 safety boundary"),
        V043CapabilityMapItem("subagent", "subagents", "subagent 호출은 열려 있지 않습니다.", False, "v0.43 safety boundary"),
        V043CapabilityMapItem("autonomous-coding", "autonomous coding", "자율 코딩 에이전트가 아닙니다.", False, "v0.43 safety boundary"),
        V043CapabilityMapItem("production-automation", "production automation", "production 자동화나 인증은 열려 있지 않습니다.", False, "v0.43 safety boundary"),
    )
    rendered = "\n".join(
        (
            "ChantaCore Capability Map",
            "",
            "지금 할 수 있는 일:",
            *[f"* {item.label}: {item.description}" for item in can_do],
            "",
            "아직 못 하는 일:",
            *[f"* {item.label}: {item.description}" for item in cannot],
            "",
            "production_certified: false",
        )
    )
    defaults = {
        "map_id": "v043-capability-map",
        "can_do": can_do,
        "cannot_do_yet": cannot,
        "rendered_text": rendered,
        "honest": True,
        "production_certified": False,
    }
    return V043CapabilityMap(**_merge(defaults, overrides))


def create_v043_what_happened_request(
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    session_id: str | None = None,
    include_trace: bool = True,
    include_run_history: bool = True,
    **overrides: Any,
) -> V043WhatHappenedRequest:
    defaults = {
        "request_id": _new_id("v043-what-happened-request"),
        "profile_id": profile_id,
        "home_path": home_path,
        "session_id": session_id or "last",
        "include_trace": bool(include_trace),
        "include_run_history": bool(include_run_history),
    }
    return V043WhatHappenedRequest(**_merge(defaults, overrides))


def create_v043_what_happened_result(request: V043WhatHappenedRequest | None = None, **overrides: Any) -> V043WhatHappenedResult:
    request = request or create_v043_what_happened_request()
    home = _resolve_home(request.home_path)
    trace_summary_used = False
    run_history_used = False
    session_used = bool(request.session_id)
    run_line = "최근 run 정보: 알 수 없음"
    history_line = "run history: 알 수 없음"
    trace_line = "trace summary: 알 수 없음"
    if request.include_run_history:
        report = create_last_run_report(create_last_run_report_request(request.profile_id, home, request.session_id if request.session_id != "last" else None))
        run_line = f"최근 run: {report.run_id or '알 수 없음'}, session: {report.session_id or request.session_id}, status: {report.status}"
        history = create_v042_run_history_result(create_v042_run_history_request(request.profile_id, home, 5))
        history_line = "run history를 확인했습니다." if history.rendered_text else "run history가 비어 있습니다."
        run_history_used = True
    if request.include_trace:
        summary = summarize_trace_events(create_trace_summary_request(request.profile_id, home, 20))
        trace_line = f"trace event count: {summary.total_events}, provider: {summary.provider_call_count}, shell: {summary.shell_execution_count}, subagent: {summary.subagent_invocation_count}"
        trace_summary_used = True
    rendered = "\n".join(
        (
            "What happened",
            "",
            "업무 세션에서 확인한 내용입니다.",
            f"* {run_line}",
            f"* {history_line}",
            f"* {trace_line}",
            "* provider 호출: 이 설명 명령에서는 호출하지 않았습니다.",
            "* 안전 상태: shell/edit/subagent/production certification은 열려 있지 않습니다.",
            "* 다음 권장 액션: 필요한 경우 /summary, /todo, /report 중 하나로 이어가시면 됩니다.",
        )
    )
    defaults = {
        "result_id": _new_id("v043-what-happened-result"),
        "status": V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value,
        "rendered_text": rendered,
        "trace_summary_used": trace_summary_used,
        "run_history_used": run_history_used,
        "session_used": session_used,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    return V043WhatHappenedResult(**_merge(defaults, overrides))


def create_v043_work_session_trace_record(**overrides: Any) -> V043WorkSessionTraceRecord:
    defaults = {
        "trace_record_id": _new_id("v043-work-session-trace"),
        "event_kind": "v043_work_session_command",
        "work_session_id": "work-session",
        "flow_kind": V043WorkFlowKind.SUMMARY.value,
        "run_id": None,
        "session_id": "work-session",
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    return V043WorkSessionTraceRecord(**_merge(defaults, overrides))


def create_v043_work_session_pi_review_contract(**overrides: Any) -> V043WorkSessionPIReviewContract:
    criteria = (
        V043WorkSessionPIReviewCriterion("start", "clean start", ("work_session_id", "session_id"), "업무 세션 시작이 재구성됩니다.", "start가 raw debug console처럼 보이면 철회합니다."),
        V043WorkSessionPIReviewCriterion("flow", "business flow", ("flow_kind", "run_id", "prompt_submitted"), "provider-backed 흐름의 run/session 연결이 남습니다.", "flow_kind나 run/session linkage가 없으면 철회합니다."),
        V043WorkSessionPIReviewCriterion("safety", "safety flags", ("shell_executed", "subagent_invoked", "production_certified"), "고위험 플래그가 false로 남습니다.", "shell/edit/subagent/tool/function이 열리면 철회합니다."),
        V043WorkSessionPIReviewCriterion("feedback", "pilot feedback", ("feedback note", "report bundle"), "UX friction이 bounded feedback/report로 남습니다.", "피드백이나 리포트가 깨지면 철회합니다."),
    )
    defaults = {
        "contract_id": "v043-work-session-pi-review-contract",
        "criteria": criteria,
        "process_instance_reconstructable": True,
        "requires_work_session_id": True,
        "requires_flow_kind": True,
        "requires_run_session_linkage": True,
        "production_certified": False,
    }
    return V043WorkSessionPIReviewContract(**_merge(defaults, overrides))


def create_v043_work_session_safety_report(**overrides: Any) -> V043WorkSessionSafetyReport:
    defaults = {
        "report_id": "v043-work-session-safety-report",
        "business_work_session_opened": True,
        "codex_like_coding_capabilities_opened": False,
        "shell_execution_allowed": False,
        "file_edit_allowed": False,
        "patch_apply_allowed": False,
        "arbitrary_file_read_allowed": False,
        "repo_search_allowed": False,
        "provider_tool_calling_allowed": False,
        "function_calling_allowed": False,
        "subagent_allowed": False,
        "general_agent_loop_allowed": False,
        "production_certified": False,
    }
    return V043WorkSessionSafetyReport(**_merge(defaults, overrides))


def create_v043_pilot_feedback_criterion(**overrides: Any) -> V043PilotFeedbackCriterion:
    defaults = {
        "criterion_id": "v043-pilot-feedback-start-ux",
        "label": "start UX feels like business work session",
        "observation_prompt": "chanta-cli start 화면이 개발자 콘솔이 아니라 업무 세션처럼 느껴지는지 기록합니다.",
        "pass_condition": "사용자가 /summary, /todo, /memo, /decision, /handoff 흐름을 자연스럽게 찾을 수 있습니다.",
        "fail_condition": "raw trace/debug banner가 기본 화면을 지배하거나 capability map이 부정확합니다.",
    }
    return V043PilotFeedbackCriterion(**_merge(defaults, overrides))


def create_v043_pilot_readiness_report(**overrides: Any) -> V043PilotReadinessReport:
    defaults = {
        "report_id": "v043-pilot-readiness-report",
        "business_work_session_start_ready": True,
        "work_session_command_surface_ready": True,
        "business_flow_templates_ready": True,
        "capability_map_ready": True,
        "what_happened_ready": True,
        "feedback_command_ready": True,
        "report_command_ready": True,
        "pi_review_contract_ready": True,
        "pilot_feedback_criteria_ready": True,
        "integrated_restore_document_ready": True,
        "ready_for_shell_execution": False,
        "ready_for_file_edit": False,
        "ready_for_patch_apply": False,
        "ready_for_arbitrary_file_read": False,
        "ready_for_repo_search": False,
        "ready_for_provider_tool_calling": False,
        "ready_for_function_calling": False,
        "ready_for_subagent_invocation": False,
        "ready_for_general_agent_loop": False,
        "ready_for_autonomous_coding": False,
        "production_certified": False,
    }
    return V043PilotReadinessReport(**_merge(defaults, overrides))


def create_v0431_work_flow_expansion_handoff(**overrides: Any) -> V0431WorkFlowExpansionHandoff:
    defaults = {
        "handoff_id": "v0431-work-flow-expansion-handoff",
        "target_version": "v0.43.1 Business Work Flow Refinement",
        "recommended_focus": (
            "refine Korean wording from pilot feedback",
            "make /what-happened more explanatory from trace evidence",
            "improve business prompt templates after manual sessions",
            "review whether Schumpeter split contract is ready",
        ),
        "still_closed": (
            "shell execution",
            "file edit/apply",
            "arbitrary file read/write",
            "repo search",
            "provider tool calling",
            "function calling",
            "subagent invocation",
            "general AgentLoop",
            "autonomous coding",
            "production certification",
        ),
    }
    return V0431WorkFlowExpansionHandoff(**_merge(defaults, overrides))


def create_v0430_integrated_restore_context_snapshot(**overrides: Any) -> V0430IntegratedRestoreContextSnapshot:
    safety = create_v0431_work_flow_expansion_handoff().still_closed
    defaults = {
        "snapshot_id": "v0430-integrated-restore-context",
        "current_version": V043_VERSION,
        "current_track": V043_TRACK_NAME,
        "baseline_versions": ("v0.42.10", "v0.42"),
        "open_capabilities": ("business work session pilot", "business slash command surface", "process intelligence review contract"),
        "closed_capabilities": safety,
        "integrated_doc_path": "docs/versions/v0.43/v0.43.0_business_work_session_pilot_restore.md",
        "next_recommended_version": "v0.43.1",
    }
    return V0430IntegratedRestoreContextSnapshot(**_merge(defaults, overrides))


def create_v0430_integrated_restore_packet(**overrides: Any) -> V0430IntegratedRestorePacket:
    titles = (
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "v0.42 Closure Summary",
        "v0.43 Track Goal",
        "Business Work Session Concept",
        "Start Command Contract",
        "Work Session Command Surface",
        "Business Flow Prompt Templates",
        "Capability Map",
        "What Happened Contract",
        "Feedback / Report Integration",
        "Process Intelligence Review Contract",
        "Safety Boundary",
        "Pilot Feedback Criteria",
        "Still-Closed Capabilities",
        "Required Test Commands",
        "Manual Pilot Commands",
        "Withdrawal Conditions",
        "v0.43.1 Recommended Next Step",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    )
    sections = tuple(
        V0430IntegratedRestoreSection(f"v0430-section-{index}", title, True, f"Required v0.43.0 section: {title}", "future-session restore")
        for index, title in enumerate(titles, 1)
    )
    defaults = {
        "restore_packet_id": "v0430-integrated-restore-packet",
        "snapshot": create_v0430_integrated_restore_context_snapshot(),
        "restore_sections": sections,
        "required_test_commands": (
            "py -m pytest tests\\test_v0430_business_work_session_pilot.py",
            "py -m pytest tests\\test_v04210_final_business_ux_acceptance.py",
        ),
        "single_integrated_doc_path": "docs/versions/v0.43/v0.43.0_business_work_session_pilot_restore.md",
        "separate_restore_doc_created": False,
    }
    return V0430IntegratedRestorePacket(**_merge(defaults, overrides))


def create_v0430_integrated_restore_document_manifest(**overrides: Any) -> V0430IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "v0430-integrated-restore-document-manifest",
        "integrated_doc_path": "docs/versions/v0.43/v0.43.0_business_work_session_pilot_restore.md",
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": False,
        "copy_paste_restore_prompt_required": True,
        "required_sections_present": True,
        "suitable_for_new_session_handoff": True,
    }
    return V0430IntegratedRestoreDocumentManifest(**_merge(defaults, overrides))


def _command_result(
    command: V043WorkSessionCommand,
    state: V043WorkSessionState,
    status: str,
    rendered_text: str,
    run_id: str | None = None,
    provider_invoked: bool = False,
    prompt_submitted: bool = False,
    **overrides: Any,
) -> V043WorkSessionCommandResult:
    defaults = {
        "result_id": _new_id("v043-command-result"),
        "command_kind": command.command_kind,
        "status": status,
        "rendered_text": rendered_text,
        "run_id": run_id,
        "session_id": state.session_id,
        "provider_invoked": provider_invoked,
        "prompt_submitted": prompt_submitted,
        "shell_executed": False,
        "subagent_invoked": False,
        "workspace_mutated": False,
        "memory_mutated": False,
        "production_certified": False,
    }
    return V043WorkSessionCommandResult(**_merge(defaults, overrides))


def _business_flow_for_command(kind: str) -> str:
    return {
        V043WorkSessionCommandKind.SUMMARY.value: V043WorkFlowKind.SUMMARY.value,
        V043WorkSessionCommandKind.TODO.value: V043WorkFlowKind.TODO.value,
        V043WorkSessionCommandKind.MEMO.value: V043WorkFlowKind.MEMO.value,
        V043WorkSessionCommandKind.DECISION.value: V043WorkFlowKind.DECISION.value,
        V043WorkSessionCommandKind.HANDOFF.value: V043WorkFlowKind.HANDOFF.value,
    }.get(kind, V043WorkFlowKind.UNKNOWN.value)


def execute_v043_work_session_command(
    command: V043WorkSessionCommand,
    state: V043WorkSessionState,
    **overrides: Any,
) -> V043WorkSessionCommandResult:
    kind = command.command_kind
    if kind == V043WorkSessionCommandKind.CAPABILITIES.value:
        capability_map = create_v043_capability_map()
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, capability_map.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.WHAT_HAPPENED.value:
        result = create_v043_what_happened_result(create_v043_what_happened_request(state.profile_id, state.home_path, state.session_id))
        return _command_result(command, state, result.status, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.PILOT_STATUS.value:
        result = execute_v043_pilot_status(create_v043_pilot_status_request(state.profile_id, state.home_path, state.session_id))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.PILOT_REVIEW.value:
        result = execute_v043_pilot_review(create_v043_pilot_review_request(state.profile_id, state.home_path, state.session_id))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.PILOT_SCORE.value:
        result = execute_v043_pilot_score(create_v043_pilot_score_request(state.profile_id, state.home_path, state.session_id))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.PILOT_FINDINGS.value:
        result = execute_v043_pilot_findings(create_v043_pilot_findings_request(state.profile_id, state.home_path, state.session_id))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.PILOT_NEXT.value:
        result = execute_v043_pilot_next(create_v043_pilot_next_request(state.profile_id, state.home_path, state.session_id))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.PILOT_REPORT.value:
        result = execute_v043_pilot_report(create_v043_pilot_report_request(state.profile_id, state.home_path, state.session_id))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.ACCEPTANCE.value:
        checklist = create_v043_pilot_acceptance_checklist()
        lines = [
            "Pilot acceptance checklist",
            f"passed: {checklist.passed_count}",
            f"warnings: {checklist.warning_count}",
            f"failed: {checklist.failed_count}",
            f"blockers: {checklist.blocker_count}",
            f"ready_for_v044_design: {str(checklist.ready_for_v044_design).lower()}",
            "production_certified: false",
        ]
        lines.extend(f"- {item.area}: {item.status}; blocks_next_track={str(item.blocks_next_track).lower()}" for item in checklist.items)
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, "\n".join(lines), **overrides)
    if kind == V043WorkSessionCommandKind.WORKFLOW_SCORE.value:
        result = execute_v043_workflow_score(create_v043_workflow_score_request(state.profile_id, state.home_path, state.session_id))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value if result.found else V043WorkSessionStatus.BLOCKED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.POLISH_STATUS.value:
        result = execute_v0436_polish_status(create_v0436_polish_status_request(state.profile_id, state.home_path, state.session_id))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.POLISH_FINDINGS.value:
        result = execute_v0436_polish_findings(create_v0436_polish_findings_request(state.profile_id, state.home_path, state.session_id))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.POLISH_REPORT.value:
        result = execute_v0436_polish_report(create_v0436_polish_report_request(state.profile_id, state.home_path, state.session_id))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.PILOT_CLOSE.value:
        result = execute_v0436_pilot_close(create_v0436_pilot_close_request(state.profile_id, state.home_path, state.session_id))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.V044_READINESS.value:
        result = execute_v0436_v044_readiness(create_v0436_v044_readiness_request(state.profile_id, state.home_path, state.session_id))
        rendered = "\n".join(
            (
                result.rendered_text,
                "",
                "v0.43.7 UX repair gate: v0.44 remains blocked until golden transcripts pass.",
                "workspace read remains closed in v0.43.7.",
                "v0.43.8 start lobby gate: v0.44 remains blocked until Schumpeter start lobby golden transcripts pass.",
                "v0.44.0 should begin with Controlled Workspace Read Design & Scope Contract.",
                "workspace read remains closed in v0.43.8.",
            )
        )
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, rendered, **overrides)
    if kind == V043WorkSessionCommandKind.V044_SCOPE.value:
        result = execute_v0436_v044_scope(create_v0436_v044_scope_request(state.profile_id, state.home_path, state.session_id))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.V044_RISKS.value:
        result = execute_v0436_v044_risks(create_v0436_v044_risks_request(state.profile_id, state.home_path, state.session_id))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.V044_HANDOFF.value:
        result = execute_v0436_v044_handoff(create_v0436_v044_handoff_request(state.profile_id, state.home_path, state.session_id))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.ARTIFACT_LAST.value:
        result = execute_v043_artifact_last(create_v043_artifact_last_request(state.profile_id, state.home_path, state.session_id))
        answer = render_v0437_artifact_debug(result.rendered_text) if command.user_content and "--debug" in command.user_content else render_v0437_artifact_default(result.rendered_text)
        return _command_result(command, state, result.status, answer.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.REVISE.value:
        result = execute_v043_revise_artifact(
            create_v043_revise_artifact_request(
                command.user_content or "",
                state.profile_id,
                state.home_path,
                state.session_id,
                state.provider_mode,
                get_v043_last_business_artifact(state.session_id),
            )
        )
        return _command_result(command, state, result.status, result.rendered_text, result.revised_envelope.artifact.run_id if result.revised_envelope else None, result.provider_invoked, result.prompt_submitted, **overrides)
    if kind == V043WorkSessionCommandKind.CLARIFY.value:
        result = execute_v043_clarify(create_v043_clarify_request(state.profile_id, state.home_path, state.session_id, command.user_content, get_v043_last_business_artifact(state.session_id)))
        return _command_result(command, state, result.status, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.NOTE.value:
        if not command.user_content:
            return _command_result(command, state, V043WorkSessionStatus.BLOCKED.value, "local note로 남길 내용을 입력해 주세요.", **overrides)
        result = append_v043_local_work_note(create_v043_local_work_note_request(command.user_content, state.profile_id, state.home_path, state.session_id, state.last_run_id, source_command="/note"))
        text = f"local work note recorded\nnote_id: {result.note_record.note_id if result.note_record else '-'}\nCORE_MEMORY: untouched" if result.appended else f"local work note rejected: {result.rejection_reason}"
        return _command_result(command, state, V043WorkSessionStatus.COMMAND_COMPLETED.value if result.appended else V043WorkSessionStatus.BLOCKED.value, text, **overrides)
    if kind == V043WorkSessionCommandKind.NOTES.value:
        result = list_v043_local_work_notes(create_v043_local_work_note_list_request(state.profile_id, state.home_path, 20))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.NOTE_LAST.value:
        result = show_v043_local_work_note(create_v043_local_work_note_show_request(state.profile_id, state.home_path, "last"))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value if result.found else V043WorkSessionStatus.BLOCKED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.NOTE_FROM_ARTIFACT.value:
        result = create_v043_note_from_artifact(create_v043_note_from_artifact_request(state.profile_id, state.home_path), state.session_id, get_v043_last_business_artifact(state.session_id))
        return _command_result(command, state, V043WorkSessionStatus.COMMAND_COMPLETED.value if result.source_artifact_found else V043WorkSessionStatus.BLOCKED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.NOTES_SEARCH.value:
        result = search_v043_local_work_notes(create_v043_local_work_note_search_request(command.user_content or "", state.profile_id, state.home_path, 20))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.MEMORY_BOUNDARY.value:
        result = create_v043_memory_boundary_status_result(create_v043_memory_boundary_status_request(state.profile_id, state.home_path))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.CONTEXT.value:
        result = create_v043_context_boundary_result(create_v043_context_boundary_request(state.profile_id, state.home_path, state.session_id))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.RECALL.value:
        if not command.user_content:
            return _command_result(command, state, V043WorkSessionStatus.BLOCKED.value, "recall query를 입력해 주세요. 예: /recall retrieval", **overrides)
        result = execute_v043_recall(create_v043_recall_request(command.user_content, state.profile_id, state.home_path, 5))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.EVIDENCE.value:
        if not command.user_content:
            return _command_result(command, state, V043WorkSessionStatus.BLOCKED.value, "evidence query를 입력해 주세요. 예: /evidence retrieval", **overrides)
        result = search_v043_local_evidence(create_v043_evidence_search_request(command.user_content, state.profile_id, state.home_path, limit=10))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.EVIDENCE_SOURCES.value:
        result = execute_v043_evidence_sources(create_v043_evidence_sources_request(state.profile_id, state.home_path))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.EVIDENCE_LAST.value:
        result = execute_v043_evidence_last(create_v043_evidence_last_request(state.profile_id, state.home_path))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value if result.found else V043WorkSessionStatus.BLOCKED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.EVIDENCE_EXPLAIN.value:
        result = execute_v043_evidence_explain(create_v043_evidence_explain_request(state.profile_id, state.home_path))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.USE_EVIDENCE.value:
        if not command.user_content:
            return _command_result(command, state, V043WorkSessionStatus.BLOCKED.value, "use-evidence query를 입력해 주세요. 예: /use-evidence v0.43.4", **overrides)
        result = execute_v043_use_evidence(create_v043_use_evidence_request(command.user_content, state.profile_id, state.home_path, state.session_id, use_last=False, limit=5))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value if result.active_state.evidence_pack_id else V043WorkSessionStatus.BLOCKED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.USE_EVIDENCE_LAST.value:
        result = execute_v043_use_evidence(create_v043_use_evidence_request(None, state.profile_id, state.home_path, state.session_id, use_last=True, limit=5))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value if result.active_state.evidence_pack_id else V043WorkSessionStatus.BLOCKED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.EVIDENCE_USED.value:
        result = execute_v043_evidence_used(create_v043_evidence_used_request(state.profile_id, state.home_path, state.session_id))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value if result.found else V043WorkSessionStatus.BLOCKED.value, result.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.GROUNDING_CHECK.value:
        result = execute_v043_grounding_check(create_v043_grounding_check_request(state.profile_id, state.home_path, state.session_id))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value if result.found else V043WorkSessionStatus.BLOCKED.value, result.rendered_text, **overrides)
    if kind in {
        V043WorkSessionCommandKind.GROUNDED_SUMMARY.value,
        V043WorkSessionCommandKind.GROUNDED_TODO.value,
        V043WorkSessionCommandKind.GROUNDED_MEMO.value,
        V043WorkSessionCommandKind.GROUNDED_DECISION.value,
        V043WorkSessionCommandKind.GROUNDED_HANDOFF.value,
    }:
        workflow_kind = {
            V043WorkSessionCommandKind.GROUNDED_SUMMARY.value: V043GroundedWorkflowKind.GROUNDED_SUMMARY.value,
            V043WorkSessionCommandKind.GROUNDED_TODO.value: V043GroundedWorkflowKind.GROUNDED_TODO.value,
            V043WorkSessionCommandKind.GROUNDED_MEMO.value: V043GroundedWorkflowKind.GROUNDED_MEMO.value,
            V043WorkSessionCommandKind.GROUNDED_DECISION.value: V043GroundedWorkflowKind.GROUNDED_DECISION.value,
            V043WorkSessionCommandKind.GROUNDED_HANDOFF.value: V043GroundedWorkflowKind.GROUNDED_HANDOFF.value,
        }[kind]
        if not command.user_content:
            return _command_result(command, state, V043WorkSessionStatus.BLOCKED.value, "grounded synthesis instruction을 입력해 주세요.", **overrides)
        try:
            request = create_v043_grounded_synthesis_request(
                workflow_kind,
                command.user_content,
                state.profile_id,
                state.home_path,
                state.session_id,
                provider=state.provider_mode,
            )
        except ValueError as exc:
            return _command_result(command, state, V043WorkSessionStatus.BLOCKED.value, f"{exc}\n먼저 /use-evidence <query>를 실행해 주세요.", **overrides)
        result = execute_v043_grounded_synthesis(request)
        envelope = create_v043_grounded_artifact_envelope(result) if result.provider_invoked else None
        text = envelope.rendered_text if envelope else result.rendered_text
        text = render_v0437_artifact_default(text).rendered_text
        return _command_result(command, state, result.status, text, result.run_id, result.provider_invoked, result.prompt_submitted, **overrides)
    if kind in {
        V043WorkSessionCommandKind.SUMMARY.value,
        V043WorkSessionCommandKind.TODO.value,
        V043WorkSessionCommandKind.MEMO.value,
        V043WorkSessionCommandKind.DECISION.value,
        V043WorkSessionCommandKind.HANDOFF.value,
    }:
        flow_kind = _business_flow_for_command(kind)
        flow_request = create_v043_business_flow_request(flow_kind, command.user_content or "", state.profile_id, state.home_path, state.session_id, state.provider_mode)
        flow = execute_v043_business_flow(flow_request)
        text = render_v0437_artifact_default(flow.rendered_text).rendered_text
        return _command_result(command, state, flow.status, text, flow.run_id, flow.provider_invoked, flow.prompt_submitted, **overrides)
    if kind == V043WorkSessionCommandKind.FEEDBACK.value:
        if not command.user_content:
            return _command_result(command, state, V043WorkSessionStatus.BLOCKED.value, '피드백 내용을 함께 입력해 주세요. 예: /feedback start UX가 업무 세션처럼 느껴지는지 테스트 중', **overrides)
        note = append_v042_feedback_note(
            create_v042_feedback_note_request(
                command.user_content,
                state.profile_id,
                state.home_path,
                category="ux",
                severity="normal",
                trace_feedback=True,
            )
        )
        text = "feedback recorded" if note.feedback_record else f"feedback rejected: {note.rejection_reason}"
        return _command_result(command, state, V043WorkSessionStatus.COMMAND_COMPLETED.value, text, **overrides)
    if kind == V043WorkSessionCommandKind.REPORT.value:
        bundle = create_v042_diagnostic_bundle_result(create_v042_diagnostic_bundle_request(state.profile_id, state.home_path, copy_paste=True, max_runs=5, max_trace_items=10, max_feedback_items=5))
        text = "\n".join(("Diagnostic bundle", "chanta-cli report bundle --copy-paste", "", bundle.copy_paste_text[:4000]))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, text, **overrides)
    if kind == V043WorkSessionCommandKind.NEW.value:
        new_state = create_v043_work_session_state(state.profile_id, state.home_path, provider=state.provider_mode)
        text = f"새 업무 세션을 시작했습니다.\nsession_id: {new_state.session_id}\n이전 세션은 삭제하지 않았습니다."
        return _command_result(command, new_state, V043WorkSessionStatus.STARTED.value, text, **overrides)
    if kind == V043WorkSessionCommandKind.EXIT.value:
        return _command_result(command, state, V043WorkSessionStatus.EXITED.value, "업무 세션을 종료합니다.", **overrides)
    if kind == V043WorkSessionCommandKind.HELP.value:
        if (command.user_content or "").strip().lower() == "commands":
            palette = render_v0438_command_palette(create_v0438_slash_command_palette_request("/"))
            return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, palette.rendered_text, **overrides)
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, _render_start_screen(state.profile_id, state.provider_mode), **overrides)
    if kind == V043WorkSessionCommandKind.ABOUT.value:
        about = render_v0438_about_card(debug=bool(command.user_content and "--debug" in command.user_content))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, about.rendered_text, **overrides)
    if kind == V043WorkSessionCommandKind.STATUS.value:
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, render_v0438_status_detail(), **overrides)
    if kind in {V043WorkSessionCommandKind.PROVIDER.value, V043WorkSessionCommandKind.HISTORY.value, V043WorkSessionCommandKind.TRACE.value}:
        text = f"{kind} 정보는 기존 chanta-cli {kind} / trace / run-report 표면에서 확인할 수 있습니다.\n업무 세션에서는 /what-happened 또는 /report를 권장합니다."
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, text, **overrides)
    return _command_result(command, state, V043WorkSessionStatus.BLOCKED.value, "알 수 없는 명령입니다. /capabilities 또는 /help를 입력해 주세요.", **overrides)


def execute_v043_work_session_input(raw_text: str, state: V043WorkSessionState, **overrides: Any) -> V043WorkSessionCommandResult:
    command = parse_v043_work_session_command(raw_text)
    if command.command_kind != V043WorkSessionCommandKind.UNKNOWN.value or not raw_text.strip():
        return execute_v043_work_session_command(command, state, **overrides)
    stripped = raw_text.strip()
    if stripped.startswith("/"):
        palette = render_v0438_command_palette(create_v0438_slash_command_palette_request(stripped))
        return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, palette.rendered_text, **overrides)
    route = create_v0437_route_decision(raw_text)
    if route.routed_to_artifact_renderer:
        return execute_v043_work_session_command(parse_v043_work_session_command(f"/summary {raw_text}"), state, **overrides)
    answer = render_v0437_default_conversation_answer(raw_text, state.session_id, state.provider_mode)
    return _command_result(command, state, V043WorkSessionStatus.DETERMINISTIC_RESULT_COMPLETED.value, answer.rendered_text, **overrides)


def _stdout_safe_start_text(result: V043WorkSessionStartResult) -> str:
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    try:
        result.rendered_text.encode(encoding)
        return result.rendered_text
    except UnicodeEncodeError:
        return _render_start_screen(
            profile_id=result.state.profile_id,
            provider_label=result.state.provider_mode,
            force_plain=True,
        )


def _stdout_safe_tui_snapshot_text(width: int, plain: bool = False, include_command_palette: bool = False, height: int | None = None, include_help: bool = False) -> str:
    result = render_v04311_text_snapshot(width=width, height=height or 36, plain=plain, include_palette=include_command_palette, include_help=include_help)
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    try:
        result.rendered_text.encode(encoding)
        return result.rendered_text
    except UnicodeEncodeError:
        return render_v04311_text_snapshot(width=width, height=height or 36, plain=True, include_palette=include_command_palette, include_help=include_help).rendered_text


def _run_start_interactive(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli start")
    parser.add_argument("--home")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--provider")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--plain", action="store_true")
    parser.add_argument("--no-color", action="store_true")
    parser.add_argument("--no-logo", action="store_true")
    parser.add_argument("--compact", action="store_true")
    parser.add_argument("--snapshot", action="store_true")
    parser.add_argument("--tui", action="store_true")
    parser.add_argument("--classic", action="store_true")
    parser.add_argument("--width", type=int, default=None)
    parser.add_argument("--height", type=int, default=None)
    parser.add_argument("--palette", action="store_true")
    parser.add_argument("--once", nargs=argparse.REMAINDER)
    parsed = parser.parse_args(list(args))
    if parsed.plain:
        once = (" ".join(parsed.once).strip(),) if parsed.once else ()
        return run_v04310_plain_tui(once, parsed.width or 100)
    if parsed.tui:
        once = (" ".join(parsed.once).strip(),) if parsed.once else ()
        if once:
            return run_v04310_prompt_toolkit_tui(once, parsed.width or 100)
        return run_v04311_fullscreen_tui()
    if parsed.snapshot:
        width = parsed.width or (80 if parsed.compact else 120)
        print(_stdout_safe_tui_snapshot_text(width, parsed.plain, parsed.palette, parsed.height))
        return 0
    if not parsed.classic:
        if parsed.once:
            once = (" ".join(parsed.once).strip(),)
            return run_v04310_plain_tui(once, parsed.width or 100)
        return run_v04311_fullscreen_tui()
    result = start_v043_work_session(
        create_v043_work_session_start_request(
            parsed.profile,
            parsed.home,
            parsed.provider,
            debug=parsed.debug,
            force_plain=parsed.plain,
            force_no_color=parsed.no_color,
            force_no_logo=parsed.no_logo,
            terminal_width=parsed.width or (70 if parsed.compact else None),
        )
    )
    print(_stdout_safe_start_text(result))
    state = result.state
    if parsed.once is not None:
        raw = " ".join(parsed.once).strip()
        if raw:
            command_result = execute_v043_work_session_input(raw, state)
            print(command_result.rendered_text)
        return 0
    while True:
        try:
            raw = read_v0438_interactive_input("> ", plain=parsed.plain)
        except EOFError:
            print("업무 세션을 종료합니다.")
            return 0
        command_result = execute_v043_work_session_input(raw, state)
        print(command_result.rendered_text)
        if command_result.status == V043WorkSessionStatus.EXITED.value:
            return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] in {"--version", "version"}:
        print(f"chanta-cli v0.41.1 (runtime {V0438_VERSION}; {V0438_RELEASE_NAME})")
        return 0
    if args and args[0] == "start":
        return _run_start_interactive(args[1:])
    if args and args[0] == "tui":
        if len(args) >= 2 and args[1] == "snapshot":
            parser = argparse.ArgumentParser(prog="chanta-cli tui snapshot", add_help=False)
            parser.add_argument("--width", type=int, default=120)
            parser.add_argument("--height", type=int, default=36)
            parser.add_argument("--plain", action="store_true")
            parser.add_argument("--palette", action="store_true")
            parser.add_argument("--help", action="store_true")
            parsed = parser.parse_args(args[2:])
            print(_stdout_safe_tui_snapshot_text(parsed.width, parsed.plain, parsed.palette, parsed.height, parsed.help))
            return 0
        parser = argparse.ArgumentParser(prog="chanta-cli tui")
        parser.add_argument("--width", type=int, default=100)
        parser.add_argument("--plain", action="store_true")
        parser.add_argument("--classic", action="store_true")
        parser.add_argument("--once", nargs=argparse.REMAINDER)
        parsed = parser.parse_args(args[1:])
        once = (" ".join(parsed.once).strip(),) if parsed.once else ()
        if parsed.plain:
            return run_v04310_plain_tui(once, parsed.width)
        if parsed.classic or once:
            return run_v04310_prompt_toolkit_tui(once, parsed.width)
        return run_v04311_fullscreen_tui()
    if len(args) >= 2 and args[0] == "report" and args[1] == "bundle":
        return _v0426_main(args)
    if len(args) >= 2 and args[0] == "feedback" and args[1] in {"note", "list", "show", "summary"}:
        return _v0426_main(args)
    return _v04210_main(args)


__all__ = [
    name
    for name in globals()
    if name.startswith("V043")
    or name.startswith("create_v043")
    or name.startswith("start_v043")
    or name.startswith("parse_v043")
    or name.startswith("execute_v043")
    or name.startswith("build_v043")
    or name == "main"
]
