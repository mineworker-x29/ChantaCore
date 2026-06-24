"""v0.43.1 business artifact quality layer for work sessions.

Business artifacts are structured assistant outputs held in the current
session/run surface. This module does not export files, edit files, scan repos,
invoke subagents, call provider tools, or mutate persistent memory.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Sequence

from chanta_core.personal_runtime.default_personal_cli_bootstrap import PROFILE_ID
from chanta_core.personal_runtime.default_personal_run import RunCommandInput, execute_run_command
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


V0431_VERSION = "v0.43.1"
V0431_RELEASE_NAME = "v0.43.1 Business Flow Artifact Quality & Session Context Stabilization"


class V043BusinessArtifactType(StrEnum):
    SUMMARY = "summary"
    TODO = "todo"
    MEMO = "memo"
    DECISION_BRIEF = "decision_brief"
    HANDOFF_NOTE = "handoff_note"
    CLARIFICATION_QUESTIONS = "clarification_questions"
    PROCESS_REVIEW = "process_review"
    ISSUE_DIAGNOSIS = "issue_diagnosis"
    UNKNOWN = "unknown"


class V043GroundingClass(StrEnum):
    CONFIRMED_FROM_USER = "confirmed_from_user"
    SESSION_EVIDENCE = "session_evidence"
    DATA_BASED_INTERPRETATION = "data_based_interpretation"
    LIKELY_HYPOTHESIS = "likely_hypothesis"
    ASSUMPTION = "assumption"
    UNKNOWN_NEEDS_VERIFICATION = "unknown_needs_verification"
    NEXT_ACTION = "next_action"
    RISK = "risk"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V043BusinessArtifactSection:
    section_id: str
    title: str
    content: str
    grounding_class: str
    confidence: str
    source_summary: str | None
    requires_verification: bool


@dataclass(frozen=True)
class V043BusinessArtifact:
    artifact_id: str
    artifact_type: str
    title: str
    sections: tuple[V043BusinessArtifactSection, ...]
    created_at: str
    session_id: str
    run_id: str | None
    flow_kind: str
    language: str
    provider_generated: bool
    grounded_in_session: bool
    contains_unverified_assumption: bool
    next_actions_present: bool
    production_certified: bool


@dataclass(frozen=True)
class V043BusinessArtifactVersion:
    version_id: str
    artifact_id: str
    version_index: int
    revision_instruction: str | None
    previous_version_id: str | None
    preserved_original: bool
    session_id: str
    run_id: str | None


@dataclass(frozen=True)
class V043SessionContextSource:
    source_id: str
    source_kind: str
    available: bool
    bounded: bool
    content_summary: str
    used_for_artifact: bool
    provider_invoked: bool
    prompt_submitted: bool
    arbitrary_file_read: bool
    shell_executed: bool


@dataclass(frozen=True)
class V043SessionContextPack:
    pack_id: str
    session_id: str
    sources: tuple[V043SessionContextSource, ...]
    context_text: str
    bounded: bool
    max_turns: int
    max_chars: int
    arbitrary_file_read: bool
    repo_search_used: bool
    shell_executed: bool


@dataclass(frozen=True)
class V043ContextSelectionPolicy:
    policy_id: str
    prefer_explicit_user_content: bool
    allow_recent_session_turns: bool
    allow_last_business_artifact: bool
    allow_last_run_report: bool
    allow_trace_summary: bool
    allow_arbitrary_file_read: bool
    allow_repo_search: bool
    max_turns: int
    max_chars: int


@dataclass(frozen=True)
class V043BusinessArtifactQualityCriterion:
    criterion_id: str
    artifact_type: str
    title: str
    description: str
    required: bool
    severity_if_missing: str


@dataclass(frozen=True)
class V043BusinessArtifactQualityReport:
    report_id: str
    artifact_id: str
    passed: bool
    score: float
    missing_required_criteria: tuple[str, ...]
    warnings: tuple[str, ...]
    blocks_pilot_use: bool


@dataclass(frozen=True)
class V043BusinessArtifactTraceRecord:
    trace_record_id: str
    event_kind: str
    artifact_id: str
    artifact_type: str
    session_id: str
    run_id: str | None
    flow_kind: str
    provider_invoked: bool
    prompt_submitted: bool
    response_parse_status: str | None
    shell_executed: bool
    subagent_invoked: bool
    workspace_mutated: bool
    memory_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V043BusinessArtifactPIReviewRecord:
    review_id: str
    artifact_id: str
    artifact_type: str
    process_instance_id: str | None
    reconstructable_from_trace: bool
    context_sources_bounded: bool
    facts_assumptions_unknowns_separated: bool
    high_risk_counts_zero: bool
    review_summary: str


@dataclass(frozen=True)
class V043BusinessArtifactEnvelope:
    envelope_id: str
    artifact: V043BusinessArtifact
    version: V043BusinessArtifactVersion
    quality_report: V043BusinessArtifactQualityReport
    pi_review_record: V043BusinessArtifactPIReviewRecord
    rendered_text: str
    debug_summary: str
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    workspace_mutated: bool
    memory_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class _BaseArtifactTemplate:
    template_id: str
    artifact_type: str
    system_instruction: str
    required_sections: tuple[str, ...]
    grounding_instruction: str
    uncertainty_instruction: str
    output_language: str
    unavailable_capability_warning: str


@dataclass(frozen=True)
class V043SummaryArtifactTemplate(_BaseArtifactTemplate):
    pass


@dataclass(frozen=True)
class V043TodoArtifactTemplate(_BaseArtifactTemplate):
    pass


@dataclass(frozen=True)
class V043MemoArtifactTemplate(_BaseArtifactTemplate):
    pass


@dataclass(frozen=True)
class V043DecisionBriefArtifactTemplate(_BaseArtifactTemplate):
    pass


@dataclass(frozen=True)
class V043HandoffArtifactTemplate(_BaseArtifactTemplate):
    pass


@dataclass(frozen=True)
class V043ClarificationArtifactTemplate(_BaseArtifactTemplate):
    pass


@dataclass(frozen=True)
class V043WhatHappenedArtifactTemplate(_BaseArtifactTemplate):
    pass


@dataclass(frozen=True)
class V043ArtifactLastRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str


@dataclass(frozen=True)
class V043ArtifactLastResult:
    result_id: str
    status: str
    rendered_text: str
    envelope: V043BusinessArtifactEnvelope | None
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    workspace_mutated: bool
    memory_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V043ReviseArtifactRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str
    provider: str | None
    revision_instruction: str
    previous_envelope: V043BusinessArtifactEnvelope | None


@dataclass(frozen=True)
class V043ReviseArtifactResult:
    result_id: str
    status: str
    rendered_text: str
    original_envelope: V043BusinessArtifactEnvelope | None
    revised_envelope: V043BusinessArtifactEnvelope | None
    preserved_original: bool
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    workspace_mutated: bool
    memory_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V043ClarifyRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str
    user_content: str | None
    last_envelope: V043BusinessArtifactEnvelope | None


@dataclass(frozen=True)
class V043ClarifyResult:
    result_id: str
    status: str
    rendered_text: str
    envelope: V043BusinessArtifactEnvelope
    missing_information: tuple[str, ...]
    why_it_matters: tuple[str, ...]
    questions: tuple[str, ...]
    suggested_default_assumptions: tuple[str, ...]
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    workspace_mutated: bool
    memory_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V043BusinessFlowAcceptanceReport:
    report_id: str
    summary_flow_ready: bool
    todo_flow_ready: bool
    memo_flow_ready: bool
    decision_flow_ready: bool
    handoff_flow_ready: bool
    clarify_flow_ready: bool
    what_happened_ready: bool
    artifact_last_ready: bool
    revise_artifact_ready: bool
    context_pack_ready: bool
    quality_report_ready: bool
    pi_review_ready: bool
    production_certified: bool


@dataclass(frozen=True)
class V0431ReadinessReport:
    report_id: str
    work_artifact_model_ready: bool
    session_context_pack_ready: bool
    bounded_context_policy_ready: bool
    business_flow_templates_ready: bool
    artifact_quality_report_ready: bool
    artifact_trace_record_ready: bool
    artifact_pi_review_record_ready: bool
    artifact_last_command_ready: bool
    revise_command_ready: bool
    clarify_command_ready: bool
    integrated_restore_document_ready: bool
    v0432_handoff_ready: bool
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
    ready_for_memory_mutation: bool
    production_certified: bool


@dataclass(frozen=True)
class V0432WorkSessionMemoryBoundaryHandoff:
    handoff_id: str
    target_version: str
    recommended_focus: tuple[str, ...]
    must_not_open: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V0431IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool
    content_summary: str
    restore_value: str


@dataclass(frozen=True)
class V0431IntegratedRestoreContextSnapshot:
    snapshot_id: str
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]
    integrated_doc_path: str
    next_recommended_version: str


@dataclass(frozen=True)
class V0431IntegratedRestorePacket:
    restore_packet_id: str
    snapshot: V0431IntegratedRestoreContextSnapshot
    restore_sections: tuple[V0431IntegratedRestoreSection, ...]
    required_test_commands: tuple[str, ...]
    single_integrated_doc_path: str
    separate_restore_doc_created: bool


@dataclass(frozen=True)
class V0431IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_path: str
    integrated_doc_required: bool
    separate_restore_doc_allowed: bool
    separate_restore_doc_created: bool
    copy_paste_restore_prompt_required: bool
    required_sections_present: bool
    suitable_for_new_session_handoff: bool


_LAST_ARTIFACT_BY_SESSION: dict[str, V043BusinessArtifactEnvelope] = {}


def _merge(defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    merged.update(overrides)
    return merged


def _now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _new_id(prefix: str) -> str:
    return f"{prefix}-{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}"


def _resolve_home(home_path: str | None) -> str:
    return str(Path(home_path or os.environ.get("CHANTACORE_HOME") or Path.cwd() / ".chantacore-personal").resolve())


def _short(text: str, limit: int = 700) -> str:
    normalized = " ".join(str(text).split())
    return normalized if len(normalized) <= limit else normalized[: limit - 3] + "..."


def _artifact_type_for_flow(flow_kind: str) -> str:
    return {
        "summary": V043BusinessArtifactType.SUMMARY.value,
        "todo": V043BusinessArtifactType.TODO.value,
        "memo": V043BusinessArtifactType.MEMO.value,
        "decision": V043BusinessArtifactType.DECISION_BRIEF.value,
        "handoff": V043BusinessArtifactType.HANDOFF_NOTE.value,
        "what_happened": V043BusinessArtifactType.PROCESS_REVIEW.value,
        "issue_diagnosis": V043BusinessArtifactType.ISSUE_DIAGNOSIS.value,
    }.get(flow_kind, V043BusinessArtifactType.UNKNOWN.value)


def _required_sections_for_artifact(artifact_type: str) -> tuple[str, ...]:
    return {
        V043BusinessArtifactType.SUMMARY.value: ("핵심 요약", "배경 / 맥락", "중요한 결정 또는 변화", "다음 액션", "불확실 / 확인 필요"),
        V043BusinessArtifactType.TODO.value: ("action", "owner", "due date", "dependency", "priority", "confidence / unknowns"),
        V043BusinessArtifactType.MEMO.value: ("제목", "맥락", "주요 내용", "결정 사항", "미해결 질문", "다음 액션"),
        V043BusinessArtifactType.DECISION_BRIEF.value: ("판단 대상", "선택지", "확인된 근거", "해석", "장단점 / tradeoff", "리스크", "권고안", "다음 액션", "불확실 / 확인 필요"),
        V043BusinessArtifactType.HANDOFF_NOTE.value: ("배경", "현재 상태", "지금까지 한 일", "남은 일", "리스크 / 주의사항", "다음 액션", "참고할 명령 또는 report bundle 안내"),
        V043BusinessArtifactType.CLARIFICATION_QUESTIONS.value: ("missing information", "why it matters", "question to ask", "suggested default assumption"),
        V043BusinessArtifactType.PROCESS_REVIEW.value: ("최근 실행된 흐름", "provider / mode", "run/session 상태", "response parse status", "trace/session/report state", "safety status", "next recommended action"),
        V043BusinessArtifactType.ISSUE_DIAGNOSIS.value: ("issue", "symptoms", "evidence", "likely causes", "risks", "next checks"),
    }.get(artifact_type, ("확인된 내용", "불확실 / 확인 필요", "다음 액션"))


def create_v043_business_artifact_section(
    title: str = "확인된 내용",
    content: str = "알 수 없음",
    grounding_class: str = V043GroundingClass.UNKNOWN_NEEDS_VERIFICATION.value,
    confidence: str = "unknown",
    source_summary: str | None = None,
    requires_verification: bool = True,
    **overrides: Any,
) -> V043BusinessArtifactSection:
    defaults = {
        "section_id": _new_id("v043-artifact-section"),
        "title": title,
        "content": content,
        "grounding_class": grounding_class,
        "confidence": confidence,
        "source_summary": source_summary,
        "requires_verification": bool(requires_verification),
    }
    return V043BusinessArtifactSection(**_merge(defaults, overrides))


def create_v043_business_artifact(
    artifact_type: str = V043BusinessArtifactType.SUMMARY.value,
    title: str | None = None,
    sections: Sequence[V043BusinessArtifactSection] | None = None,
    session_id: str = "work-session",
    run_id: str | None = None,
    flow_kind: str = "summary",
    provider_generated: bool = False,
    grounded_in_session: bool = True,
    **overrides: Any,
) -> V043BusinessArtifact:
    actual_sections = tuple(sections or _default_sections(artifact_type, "알 수 없음"))
    assumptions = any(section.grounding_class == V043GroundingClass.ASSUMPTION.value or section.requires_verification for section in actual_sections)
    next_actions = any("action" in section.title.lower() or "액션" in section.title for section in actual_sections)
    defaults = {
        "artifact_id": _new_id("v043-artifact"),
        "artifact_type": artifact_type,
        "title": title or _title_for_artifact(artifact_type),
        "sections": actual_sections,
        "created_at": _now(),
        "session_id": session_id,
        "run_id": run_id,
        "flow_kind": flow_kind,
        "language": "ko-KR",
        "provider_generated": bool(provider_generated),
        "grounded_in_session": bool(grounded_in_session),
        "contains_unverified_assumption": assumptions,
        "next_actions_present": next_actions,
        "production_certified": False,
    }
    return V043BusinessArtifact(**_merge(defaults, overrides))


def _title_for_artifact(artifact_type: str) -> str:
    return {
        V043BusinessArtifactType.SUMMARY.value: "업무 요약",
        V043BusinessArtifactType.TODO.value: "다음 액션",
        V043BusinessArtifactType.MEMO.value: "업무 메모",
        V043BusinessArtifactType.DECISION_BRIEF.value: "판단 브리프",
        V043BusinessArtifactType.HANDOFF_NOTE.value: "인수인계문",
        V043BusinessArtifactType.CLARIFICATION_QUESTIONS.value: "확인 질문",
        V043BusinessArtifactType.PROCESS_REVIEW.value: "세션 진행 설명",
        V043BusinessArtifactType.ISSUE_DIAGNOSIS.value: "이슈 진단",
    }.get(artifact_type, "업무 산출물")


def _default_sections(artifact_type: str, content: str) -> tuple[V043BusinessArtifactSection, ...]:
    sections: list[V043BusinessArtifactSection] = []
    for title in _required_sections_for_artifact(artifact_type):
        grounding = V043GroundingClass.NEXT_ACTION.value if "action" in title.lower() or "액션" in title else V043GroundingClass.SESSION_EVIDENCE.value
        if "불확실" in title or "unknown" in title.lower() or "질문" in title or "missing" in title.lower():
            grounding = V043GroundingClass.UNKNOWN_NEEDS_VERIFICATION.value
        if "리스크" in title or "risk" in title.lower():
            grounding = V043GroundingClass.RISK.value
        sections.append(
            create_v043_business_artifact_section(
                title=title,
                content=content if title == _required_sections_for_artifact(artifact_type)[0] else "알 수 없음",
                grounding_class=grounding,
                confidence="medium" if grounding != V043GroundingClass.UNKNOWN_NEEDS_VERIFICATION.value else "unknown",
                source_summary="explicit user content or bounded session context",
                requires_verification=grounding == V043GroundingClass.UNKNOWN_NEEDS_VERIFICATION.value,
            )
        )
    return tuple(sections)


def create_v043_business_artifact_envelope(
    artifact: V043BusinessArtifact | None = None,
    version: V043BusinessArtifactVersion | None = None,
    provider_invoked: bool = False,
    prompt_submitted: bool = False,
    response_parse_status: str | None = None,
    previous_version_id: str | None = None,
    revision_instruction: str | None = None,
    **overrides: Any,
) -> V043BusinessArtifactEnvelope:
    artifact = artifact or create_v043_business_artifact()
    version = version or V043BusinessArtifactVersion(
        version_id=_new_id("v043-artifact-version"),
        artifact_id=artifact.artifact_id,
        version_index=1 if previous_version_id is None else 2,
        revision_instruction=revision_instruction,
        previous_version_id=previous_version_id,
        preserved_original=previous_version_id is not None,
        session_id=artifact.session_id,
        run_id=artifact.run_id,
    )
    quality = evaluate_v043_business_artifact_quality(artifact)
    pi = create_v043_business_artifact_pi_review_record(artifact=artifact, context_sources_bounded=True)
    rendered = _render_artifact(artifact)
    defaults = {
        "envelope_id": _new_id("v043-artifact-envelope"),
        "artifact": artifact,
        "version": version,
        "quality_report": quality,
        "pi_review_record": pi,
        "rendered_text": rendered,
        "debug_summary": f"artifact_id={artifact.artifact_id}; type={artifact.artifact_type}; session={artifact.session_id}; run={artifact.run_id or '-'}; parse={response_parse_status or '-'}",
        "provider_invoked": bool(provider_invoked),
        "prompt_submitted": bool(prompt_submitted),
        "shell_executed": False,
        "subagent_invoked": False,
        "workspace_mutated": False,
        "memory_mutated": False,
        "production_certified": False,
    }
    return V043BusinessArtifactEnvelope(**_merge(defaults, overrides))


def remember_v043_business_artifact(envelope: V043BusinessArtifactEnvelope) -> V043BusinessArtifactEnvelope:
    _LAST_ARTIFACT_BY_SESSION[envelope.artifact.session_id] = envelope
    return envelope


def get_v043_last_business_artifact(session_id: str) -> V043BusinessArtifactEnvelope | None:
    return _LAST_ARTIFACT_BY_SESSION.get(session_id)


def list_v043_business_artifacts() -> tuple[V043BusinessArtifactEnvelope, ...]:
    return tuple(_LAST_ARTIFACT_BY_SESSION.values())


def create_v043_session_context_source(
    source_kind: str = "explicit_user_content",
    content_summary: str = "",
    available: bool = True,
    used_for_artifact: bool = True,
    provider_invoked: bool = False,
    prompt_submitted: bool = False,
    **overrides: Any,
) -> V043SessionContextSource:
    defaults = {
        "source_id": _new_id("v043-context-source"),
        "source_kind": source_kind,
        "available": bool(available),
        "bounded": True,
        "content_summary": _short(content_summary, 700),
        "used_for_artifact": bool(used_for_artifact),
        "provider_invoked": bool(provider_invoked),
        "prompt_submitted": bool(prompt_submitted),
        "arbitrary_file_read": False,
        "shell_executed": False,
    }
    return V043SessionContextSource(**_merge(defaults, overrides))


def create_v043_context_selection_policy(
    max_turns: int = 6,
    max_chars: int = 3000,
    **overrides: Any,
) -> V043ContextSelectionPolicy:
    defaults = {
        "policy_id": "v0431-bounded-context-selection-policy",
        "prefer_explicit_user_content": True,
        "allow_recent_session_turns": True,
        "allow_last_business_artifact": True,
        "allow_last_run_report": True,
        "allow_trace_summary": True,
        "allow_arbitrary_file_read": False,
        "allow_repo_search": False,
        "max_turns": max(1, min(int(max_turns), 20)),
        "max_chars": max(500, min(int(max_chars), 12000)),
    }
    return V043ContextSelectionPolicy(**_merge(defaults, overrides))


def build_v043_session_context_pack(
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    session_id: str = "work-session",
    explicit_user_content: str | None = None,
    last_artifact: V043BusinessArtifactEnvelope | None = None,
    policy: V043ContextSelectionPolicy | None = None,
    **overrides: Any,
) -> V043SessionContextPack:
    policy = policy or create_v043_context_selection_policy()
    home = _resolve_home(home_path)
    sources: list[V043SessionContextSource] = []
    chunks: list[str] = []
    if explicit_user_content and policy.prefer_explicit_user_content:
        sources.append(create_v043_session_context_source("explicit_user_content", explicit_user_content))
        chunks.append(f"[explicit_user_content]\n{explicit_user_content}")
    if policy.allow_recent_session_turns:
        session = create_v042_session_show_result(create_v042_session_show_request(profile_id, home, "session_id", session_id, include_turns=True, max_turns=policy.max_turns))
        summary = "; ".join(f"{turn.role}: {turn.content_preview}" for turn in session.turn_previews)
        sources.append(create_v043_session_context_source("recent_session_turns", summary, available=session.found, used_for_artifact=bool(summary)))
        if summary:
            chunks.append(f"[recent_session_turns]\n{summary}")
    actual_last = last_artifact or get_v043_last_business_artifact(session_id)
    if policy.allow_last_business_artifact:
        summary = actual_last.rendered_text if actual_last else ""
        sources.append(create_v043_session_context_source("last_business_artifact", summary, available=actual_last is not None, used_for_artifact=actual_last is not None))
        if actual_last:
            chunks.append(f"[last_business_artifact]\n{actual_last.rendered_text}")
    if policy.allow_last_run_report:
        report = create_last_run_report(create_last_run_report_request(profile_id, home, session_id))
        sources.append(create_v043_session_context_source("last_run_report", report.status, available=True, used_for_artifact=True))
        chunks.append(f"[last_run_report]\nstatus={report.status}; run_id={report.run_id or 'unknown'}; parse={report.response_parse_status or 'unknown'}")
    if policy.allow_trace_summary:
        trace = summarize_trace_events(create_trace_summary_request(profile_id, home, 20))
        trace_summary = f"events={trace.total_events}; provider={trace.provider_call_count}; shell={trace.shell_execution_count}; subagent={trace.subagent_invocation_count}; production={trace.production_certification_count}"
        sources.append(create_v043_session_context_source("trace_summary", trace_summary, available=True, used_for_artifact=True))
        chunks.append(f"[trace_summary]\n{trace_summary}")
    context_text = "\n\n".join(chunks)[: policy.max_chars]
    defaults = {
        "pack_id": _new_id("v043-context-pack"),
        "session_id": session_id,
        "sources": tuple(sources),
        "context_text": context_text,
        "bounded": True,
        "max_turns": policy.max_turns,
        "max_chars": policy.max_chars,
        "arbitrary_file_read": False,
        "repo_search_used": False,
        "shell_executed": False,
    }
    return V043SessionContextPack(**_merge(defaults, overrides))


def create_v043_business_artifact_quality_criterion(
    criterion_id: str = "has_clear_title",
    artifact_type: str = "all",
    **overrides: Any,
) -> V043BusinessArtifactQualityCriterion:
    descriptions = {
        "has_clear_title": "Artifact has a clear business title.",
        "has_business_context": "Artifact includes context or background.",
        "separates_facts_and_assumptions": "Facts, interpretations, assumptions, and unknowns are separated.",
        "includes_next_actions_when_relevant": "Next actions are explicit where relevant.",
        "includes_risks_when_relevant": "Risks are present for decisions, handoffs, and process review.",
        "includes_unknowns_when_relevant": "Unknowns and verification needs are visible.",
        "avoids_unavailable_capability_claims": "Artifact does not claim file, shell, repo, external action, or automation powers.",
        "uses_korean_polite_language": "Korean user-facing output uses polite business language.",
        "bounded_context_only": "Context comes only from explicit input or bounded session/run/trace surfaces.",
        "process_reviewable": "Artifact can be reconstructed from run/session/trace evidence.",
    }
    defaults = {
        "criterion_id": criterion_id,
        "artifact_type": artifact_type,
        "title": criterion_id.replace("_", " "),
        "description": descriptions.get(criterion_id, criterion_id),
        "required": True,
        "severity_if_missing": "high" if criterion_id in {"avoids_unavailable_capability_claims", "bounded_context_only"} else "medium",
    }
    return V043BusinessArtifactQualityCriterion(**_merge(defaults, overrides))


def _quality_criteria(artifact_type: str = "all") -> tuple[V043BusinessArtifactQualityCriterion, ...]:
    ids = (
        "has_clear_title",
        "has_business_context",
        "separates_facts_and_assumptions",
        "includes_next_actions_when_relevant",
        "includes_risks_when_relevant",
        "includes_unknowns_when_relevant",
        "avoids_unavailable_capability_claims",
        "uses_korean_polite_language",
        "bounded_context_only",
        "process_reviewable",
    )
    return tuple(create_v043_business_artifact_quality_criterion(item, artifact_type) for item in ids)


def evaluate_v043_business_artifact_quality(artifact: V043BusinessArtifact, **overrides: Any) -> V043BusinessArtifactQualityReport:
    text = _render_artifact(artifact).lower()
    missing: list[str] = []
    if not artifact.title.strip():
        missing.append("has_clear_title")
    if not artifact.sections:
        missing.append("has_business_context")
    if not any(section.grounding_class in {V043GroundingClass.ASSUMPTION.value, V043GroundingClass.UNKNOWN_NEEDS_VERIFICATION.value} for section in artifact.sections):
        missing.append("separates_facts_and_assumptions")
    if artifact.artifact_type != V043BusinessArtifactType.CLARIFICATION_QUESTIONS.value and not artifact.next_actions_present:
        missing.append("includes_next_actions_when_relevant")
    if artifact.artifact_type in {V043BusinessArtifactType.DECISION_BRIEF.value, V043BusinessArtifactType.HANDOFF_NOTE.value, V043BusinessArtifactType.PROCESS_REVIEW.value} and "리스크" not in text and "risk" not in text:
        missing.append("includes_risks_when_relevant")
    if not any(section.requires_verification for section in artifact.sections):
        missing.append("includes_unknowns_when_relevant")
    forbidden_claims = ("shell executed", "file edited", "repo searched", "subagent invoked", "production certified")
    if any(item in text for item in forbidden_claims):
        missing.append("avoids_unavailable_capability_claims")
    if artifact.production_certified:
        missing.append("process_reviewable")
    criteria = _quality_criteria(artifact.artifact_type)
    score = max(0.0, (len(criteria) - len(set(missing))) / len(criteria))
    defaults = {
        "report_id": _new_id("v043-quality-report"),
        "artifact_id": artifact.artifact_id,
        "passed": not missing,
        "score": round(score, 2),
        "missing_required_criteria": tuple(sorted(set(missing))),
        "warnings": tuple(f"missing: {item}" for item in sorted(set(missing))),
        "blocks_pilot_use": any(item in {"avoids_unavailable_capability_claims", "bounded_context_only"} for item in missing),
    }
    return V043BusinessArtifactQualityReport(**_merge(defaults, overrides))


def create_v043_business_artifact_quality_report(artifact: V043BusinessArtifact | None = None, **overrides: Any) -> V043BusinessArtifactQualityReport:
    return evaluate_v043_business_artifact_quality(artifact or create_v043_business_artifact(), **overrides)


def create_v043_business_artifact_trace_record(
    artifact: V043BusinessArtifact | None = None,
    provider_invoked: bool = False,
    prompt_submitted: bool = False,
    response_parse_status: str | None = None,
    **overrides: Any,
) -> V043BusinessArtifactTraceRecord:
    artifact = artifact or create_v043_business_artifact()
    defaults = {
        "trace_record_id": _new_id("v043-artifact-trace"),
        "event_kind": "business_artifact_created",
        "artifact_id": artifact.artifact_id,
        "artifact_type": artifact.artifact_type,
        "session_id": artifact.session_id,
        "run_id": artifact.run_id,
        "flow_kind": artifact.flow_kind,
        "provider_invoked": bool(provider_invoked),
        "prompt_submitted": bool(prompt_submitted),
        "response_parse_status": response_parse_status,
        "shell_executed": False,
        "subagent_invoked": False,
        "workspace_mutated": False,
        "memory_mutated": False,
        "production_certified": False,
    }
    return V043BusinessArtifactTraceRecord(**_merge(defaults, overrides))


def create_v043_business_artifact_pi_review_record(
    artifact: V043BusinessArtifact | None = None,
    context_sources_bounded: bool = True,
    **overrides: Any,
) -> V043BusinessArtifactPIReviewRecord:
    artifact = artifact or create_v043_business_artifact()
    separated = any(section.grounding_class in {V043GroundingClass.CONFIRMED_FROM_USER.value, V043GroundingClass.SESSION_EVIDENCE.value} for section in artifact.sections) and any(section.requires_verification for section in artifact.sections)
    defaults = {
        "review_id": _new_id("v043-artifact-pi-review"),
        "artifact_id": artifact.artifact_id,
        "artifact_type": artifact.artifact_type,
        "process_instance_id": artifact.run_id or artifact.session_id,
        "reconstructable_from_trace": True,
        "context_sources_bounded": bool(context_sources_bounded),
        "facts_assumptions_unknowns_separated": separated,
        "high_risk_counts_zero": True,
        "review_summary": "Business artifact is reviewable from bounded session/run/trace evidence; high-risk counts remain zero.",
    }
    return V043BusinessArtifactPIReviewRecord(**_merge(defaults, overrides))


def _template(
    cls: type[_BaseArtifactTemplate],
    template_id: str,
    artifact_type: str,
    required_sections: tuple[str, ...],
) -> _BaseArtifactTemplate:
    return cls(
        template_id=template_id,
        artifact_type=artifact_type,
        system_instruction="ChantaCore 업무 보조 에이전트로서 한국어 존댓말을 사용하고, 확인된 내용과 가정/불확실성을 분리합니다.",
        required_sections=required_sections,
        grounding_instruction="확인된 내용, 해석, 가능성 높은 가설, 가정, 불확실 / 확인 필요, 다음 액션, 리스크를 구분합니다.",
        uncertainty_instruction="확인되지 않은 소유자, 기한, 의존성, 수치는 알 수 없음으로 표시합니다.",
        output_language="ko-KR polite business Korean",
        unavailable_capability_warning="파일 접근, 셸 실행, repo search, subagent, 외부 실행, production automation을 했다고 주장하지 않습니다.",
    )


def build_v043_summary_artifact_template() -> V043SummaryArtifactTemplate:
    return _template(V043SummaryArtifactTemplate, "v0431-summary-artifact-template", V043BusinessArtifactType.SUMMARY.value, _required_sections_for_artifact(V043BusinessArtifactType.SUMMARY.value))


def build_v043_todo_artifact_template() -> V043TodoArtifactTemplate:
    return _template(V043TodoArtifactTemplate, "v0431-todo-artifact-template", V043BusinessArtifactType.TODO.value, _required_sections_for_artifact(V043BusinessArtifactType.TODO.value))


def build_v043_memo_artifact_template() -> V043MemoArtifactTemplate:
    return _template(V043MemoArtifactTemplate, "v0431-memo-artifact-template", V043BusinessArtifactType.MEMO.value, _required_sections_for_artifact(V043BusinessArtifactType.MEMO.value))


def build_v043_decision_brief_artifact_template() -> V043DecisionBriefArtifactTemplate:
    return _template(V043DecisionBriefArtifactTemplate, "v0431-decision-brief-artifact-template", V043BusinessArtifactType.DECISION_BRIEF.value, _required_sections_for_artifact(V043BusinessArtifactType.DECISION_BRIEF.value))


def build_v043_handoff_artifact_template() -> V043HandoffArtifactTemplate:
    return _template(V043HandoffArtifactTemplate, "v0431-handoff-artifact-template", V043BusinessArtifactType.HANDOFF_NOTE.value, _required_sections_for_artifact(V043BusinessArtifactType.HANDOFF_NOTE.value))


def build_v043_clarification_artifact_template() -> V043ClarificationArtifactTemplate:
    return _template(V043ClarificationArtifactTemplate, "v0431-clarification-artifact-template", V043BusinessArtifactType.CLARIFICATION_QUESTIONS.value, _required_sections_for_artifact(V043BusinessArtifactType.CLARIFICATION_QUESTIONS.value))


def build_v043_what_happened_artifact_template() -> V043WhatHappenedArtifactTemplate:
    return _template(V043WhatHappenedArtifactTemplate, "v0431-what-happened-artifact-template", V043BusinessArtifactType.PROCESS_REVIEW.value, _required_sections_for_artifact(V043BusinessArtifactType.PROCESS_REVIEW.value))


def create_v043_artifact_last_request(
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    session_id: str = "work-session",
    **overrides: Any,
) -> V043ArtifactLastRequest:
    defaults = {"request_id": _new_id("v043-artifact-last-request"), "profile_id": profile_id, "home_path": home_path, "session_id": session_id}
    return V043ArtifactLastRequest(**_merge(defaults, overrides))


def create_v043_artifact_last_result(**overrides: Any) -> V043ArtifactLastResult:
    defaults = {
        "result_id": _new_id("v043-artifact-last-result"),
        "status": "not_found",
        "rendered_text": "아직 생성된 업무 산출물이 없습니다. /summary, /todo, /memo, /decision, /handoff 중 하나를 먼저 실행해 주세요.",
        "envelope": None,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "workspace_mutated": False,
        "memory_mutated": False,
        "production_certified": False,
    }
    return V043ArtifactLastResult(**_merge(defaults, overrides))


def execute_v043_artifact_last(request: V043ArtifactLastRequest, **overrides: Any) -> V043ArtifactLastResult:
    envelope = get_v043_last_business_artifact(request.session_id)
    if not envelope:
        return create_v043_artifact_last_result(**overrides)
    return create_v043_artifact_last_result(status="completed", rendered_text=envelope.rendered_text, envelope=envelope, **overrides)


def create_v043_revise_artifact_request(
    revision_instruction: str,
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    session_id: str = "work-session",
    provider: str | None = None,
    previous_envelope: V043BusinessArtifactEnvelope | None = None,
    **overrides: Any,
) -> V043ReviseArtifactRequest:
    defaults = {
        "request_id": _new_id("v043-revise-request"),
        "profile_id": profile_id,
        "home_path": home_path,
        "session_id": session_id,
        "provider": provider,
        "revision_instruction": revision_instruction,
        "previous_envelope": previous_envelope,
    }
    return V043ReviseArtifactRequest(**_merge(defaults, overrides))


def create_v043_revise_artifact_result(**overrides: Any) -> V043ReviseArtifactResult:
    defaults = {
        "result_id": _new_id("v043-revise-result"),
        "status": "blocked",
        "rendered_text": "수정할 이전 업무 산출물이 없습니다. 먼저 /summary, /memo, /decision, /handoff 중 하나를 실행해 주세요.",
        "original_envelope": None,
        "revised_envelope": None,
        "preserved_original": True,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "workspace_mutated": False,
        "memory_mutated": False,
        "production_certified": False,
    }
    return V043ReviseArtifactResult(**_merge(defaults, overrides))


def execute_v043_revise_artifact(request: V043ReviseArtifactRequest, **overrides: Any) -> V043ReviseArtifactResult:
    original = request.previous_envelope or get_v043_last_business_artifact(request.session_id)
    if not original:
        return create_v043_revise_artifact_result(**overrides)
    prompt = "\n".join(
        (
            "다음 업무 산출물을 사용자의 지시에 맞게 새 버전으로 다시 작성해 주세요.",
            "원본은 보존되며 파일 편집이나 외부 적용은 하지 않습니다.",
            "",
            "[원본 산출물]",
            _revision_safe_text(original.rendered_text),
            "",
            "[수정 지시]",
            request.revision_instruction,
        )
    )
    run = execute_run_command(
        RunCommandInput(
            profile_id=request.profile_id,
            home_path=_resolve_home(request.home_path),
            user_input=prompt,
            session_id=request.session_id,
            provider=request.provider,
            mock_provider=request.provider == "mock",
            timeout_seconds=60.0,
        )
    )
    section = create_v043_business_artifact_section(
        title="수정본",
        content=_clean_provider_text(run.rendered_text),
        grounding_class=V043GroundingClass.DATA_BASED_INTERPRETATION.value,
        confidence="medium",
        source_summary="previous business artifact and explicit revision instruction",
        requires_verification=False,
    )
    unknown = create_v043_business_artifact_section(
        title="불확실 / 확인 필요",
        content="수정 지시 외의 추가 사실은 확인하지 않았습니다.",
        grounding_class=V043GroundingClass.UNKNOWN_NEEDS_VERIFICATION.value,
        confidence="unknown",
        source_summary="bounded revision context",
        requires_verification=True,
    )
    artifact = create_v043_business_artifact(
        artifact_type=original.artifact.artifact_type,
        title=f"{original.artifact.title} - 수정본",
        sections=(section, unknown),
        session_id=request.session_id,
        run_id=getattr(getattr(run, "run_result", None), "result_id", None),
        flow_kind=original.artifact.flow_kind,
        provider_generated=run.provider_invoked,
    )
    envelope = create_v043_business_artifact_envelope(
        artifact,
        provider_invoked=run.provider_invoked,
        prompt_submitted=run.prompt_submitted,
        previous_version_id=original.version.version_id,
        revision_instruction=request.revision_instruction,
    )
    remember_v043_business_artifact(envelope)
    return create_v043_revise_artifact_result(
        status="completed" if run.exit_code == 0 else "provider_run_failed",
        rendered_text=envelope.rendered_text,
        original_envelope=original,
        revised_envelope=envelope,
        preserved_original=True,
        provider_invoked=run.provider_invoked,
        prompt_submitted=run.prompt_submitted,
        **overrides,
    )


def create_v043_clarify_request(
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    session_id: str = "work-session",
    user_content: str | None = None,
    last_envelope: V043BusinessArtifactEnvelope | None = None,
    **overrides: Any,
) -> V043ClarifyRequest:
    defaults = {
        "request_id": _new_id("v043-clarify-request"),
        "profile_id": profile_id,
        "home_path": home_path,
        "session_id": session_id,
        "user_content": user_content,
        "last_envelope": last_envelope,
    }
    return V043ClarifyRequest(**_merge(defaults, overrides))


def create_v043_clarify_result(envelope: V043BusinessArtifactEnvelope | None = None, **overrides: Any) -> V043ClarifyResult:
    envelope = envelope or create_v043_business_artifact_envelope(create_v043_business_artifact(V043BusinessArtifactType.CLARIFICATION_QUESTIONS.value))
    defaults = {
        "result_id": _new_id("v043-clarify-result"),
        "status": "completed",
        "rendered_text": envelope.rendered_text,
        "envelope": envelope,
        "missing_information": ("owner", "due date", "decision criterion"),
        "why_it_matters": ("담당자와 기한이 없으면 실행 가능성이 낮습니다.", "판단 기준이 없으면 권고안의 근거가 약해집니다."),
        "questions": ("담당자는 누구로 보면 될까요?", "희망 완료일이나 마감일이 있습니까?", "가장 중요한 판단 기준은 비용, 속도, 안정성 중 무엇입니까?"),
        "suggested_default_assumptions": ("사용자가 원하면 담당자와 기한은 알 수 없음으로 두고 진행합니다.",),
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "workspace_mutated": False,
        "memory_mutated": False,
        "production_certified": False,
    }
    return V043ClarifyResult(**_merge(defaults, overrides))


def execute_v043_clarify(request: V043ClarifyRequest, **overrides: Any) -> V043ClarifyResult:
    context = request.user_content or (request.last_envelope.rendered_text if request.last_envelope else "")
    missing = ("담당자", "기한", "성공 기준")
    why = ("액션의 책임 경계를 정해야 합니다.", "일정 판단과 우선순위 산정에 필요합니다.", "결론의 반증 조건과 품질 기준에 필요합니다.")
    questions = ("이 일의 담당자는 누구입니까?", "언제까지 완료되어야 합니까?", "성공/실패를 가르는 기준은 무엇입니까?")
    assumptions = ("답이 없으면 담당자/기한/기준은 '알 수 없음'으로 표시하고 진행합니다.",)
    sections = (
        create_v043_business_artifact_section("missing information", "\n".join(f"- {item}" for item in missing), V043GroundingClass.UNKNOWN_NEEDS_VERIFICATION.value, "unknown", "bounded session context", True),
        create_v043_business_artifact_section("why it matters", "\n".join(f"- {item}" for item in why), V043GroundingClass.DATA_BASED_INTERPRETATION.value, "medium", "artifact quality rubric", False),
        create_v043_business_artifact_section("question to ask", "\n".join(f"- {item}" for item in questions), V043GroundingClass.NEXT_ACTION.value, "high", "clarification template", False),
        create_v043_business_artifact_section("suggested default assumption", "\n".join(f"- {item}" for item in assumptions), V043GroundingClass.ASSUMPTION.value, "low", "default bounded assumption", True),
        create_v043_business_artifact_section("확인된 내용", _short(context or "현재 세션에서 추가 확인된 내용은 알 수 없습니다."), V043GroundingClass.SESSION_EVIDENCE.value, "medium" if context else "unknown", "explicit user content or last artifact", not bool(context)),
    )
    artifact = create_v043_business_artifact(
        V043BusinessArtifactType.CLARIFICATION_QUESTIONS.value,
        title="확인 질문",
        sections=sections,
        session_id=request.session_id,
        flow_kind="clarify",
        provider_generated=False,
    )
    envelope = create_v043_business_artifact_envelope(artifact)
    remember_v043_business_artifact(envelope)
    return create_v043_clarify_result(
        envelope,
        missing_information=missing,
        why_it_matters=why,
        questions=questions,
        suggested_default_assumptions=assumptions,
        **overrides,
    )


def create_v043_business_flow_acceptance_report(**overrides: Any) -> V043BusinessFlowAcceptanceReport:
    defaults = {
        "report_id": "v0431-business-flow-acceptance-report",
        "summary_flow_ready": True,
        "todo_flow_ready": True,
        "memo_flow_ready": True,
        "decision_flow_ready": True,
        "handoff_flow_ready": True,
        "clarify_flow_ready": True,
        "what_happened_ready": True,
        "artifact_last_ready": True,
        "revise_artifact_ready": True,
        "context_pack_ready": True,
        "quality_report_ready": True,
        "pi_review_ready": True,
        "production_certified": False,
    }
    return V043BusinessFlowAcceptanceReport(**_merge(defaults, overrides))


def create_v0431_readiness_report(**overrides: Any) -> V0431ReadinessReport:
    defaults = {
        "report_id": "v0431-readiness-report",
        "work_artifact_model_ready": True,
        "session_context_pack_ready": True,
        "bounded_context_policy_ready": True,
        "business_flow_templates_ready": True,
        "artifact_quality_report_ready": True,
        "artifact_trace_record_ready": True,
        "artifact_pi_review_record_ready": True,
        "artifact_last_command_ready": True,
        "revise_command_ready": True,
        "clarify_command_ready": True,
        "integrated_restore_document_ready": True,
        "v0432_handoff_ready": True,
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
        "ready_for_memory_mutation": False,
        "production_certified": False,
    }
    return V0431ReadinessReport(**_merge(defaults, overrides))


def create_v0432_work_session_memory_boundary_handoff(**overrides: Any) -> V0432WorkSessionMemoryBoundaryHandoff:
    defaults = {
        "handoff_id": "v0432-work-session-memory-boundary-handoff",
        "target_version": "v0.43.2 Work Session Memory Boundary & Local Note Discipline",
        "recommended_focus": (
            "local session notes vs persistent memory boundary",
            "when feedback becomes memory-like evidence",
            "how to keep work artifacts retrievable without mutating CORE_MEMORY",
            "no automatic memory mutation",
            "no arbitrary file write",
            "no external export",
        ),
        "must_not_open": (
            "shell execution",
            "file edit/apply",
            "arbitrary file read/write",
            "repo search",
            "subagent invocation",
            "general AgentLoop",
            "memory mutation",
            "production certification",
        ),
        "production_certified": False,
    }
    return V0432WorkSessionMemoryBoundaryHandoff(**_merge(defaults, overrides))


def create_v0431_integrated_restore_context_snapshot(**overrides: Any) -> V0431IntegratedRestoreContextSnapshot:
    defaults = {
        "snapshot_id": "v0431-integrated-restore-context",
        "current_version": V0431_VERSION,
        "current_track": "v0.43 Business Work Session Pilot & Process Intelligence Review Loop",
        "baseline_versions": ("v0.43.0", "v0.42.10"),
        "open_capabilities": ("business artifact model", "bounded session context pack", "artifact quality report", "artifact PI review record", "/artifact last", "/revise", "/clarify"),
        "closed_capabilities": create_v0432_work_session_memory_boundary_handoff().must_not_open,
        "integrated_doc_path": "docs/versions/v0.43/v0.43.1_business_flow_artifact_quality_restore.md",
        "next_recommended_version": "v0.43.2",
    }
    return V0431IntegratedRestoreContextSnapshot(**_merge(defaults, overrides))


def create_v0431_integrated_restore_packet(**overrides: Any) -> V0431IntegratedRestorePacket:
    titles = (
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "v0.43.0 Baseline Summary",
        "v0.43.1 Goal",
        "Business Artifact Model",
        "Session Context Pack",
        "Bounded Context Selection Policy",
        "Grounding Classes",
        "Artifact Quality Criteria",
        "Summary Flow Standard",
        "Todo Flow Standard",
        "Memo Flow Standard",
        "Decision Brief Standard",
        "Handoff Note Standard",
        "Clarification Flow",
        "What Happened Refinement",
        "Artifact Last / Revise Commands",
        "PI Review Contract",
        "Safety Boundary",
        "Required Test Commands",
        "Manual Pilot Commands",
        "Withdrawal Conditions",
        "v0.43.2 Recommended Next Step",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    )
    sections = tuple(V0431IntegratedRestoreSection(f"v0431-section-{index}", title, True, f"Required v0.43.1 section: {title}", "future-session restore") for index, title in enumerate(titles, 1))
    defaults = {
        "restore_packet_id": "v0431-integrated-restore-packet",
        "snapshot": create_v0431_integrated_restore_context_snapshot(),
        "restore_sections": sections,
        "required_test_commands": (
            "py -m pytest tests\\test_v0431_business_flow_artifact_quality.py",
            "py -m pytest tests\\test_v0430_business_work_session_pilot.py",
        ),
        "single_integrated_doc_path": "docs/versions/v0.43/v0.43.1_business_flow_artifact_quality_restore.md",
        "separate_restore_doc_created": False,
    }
    return V0431IntegratedRestorePacket(**_merge(defaults, overrides))


def create_v0431_integrated_restore_document_manifest(**overrides: Any) -> V0431IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "v0431-integrated-restore-document-manifest",
        "integrated_doc_path": "docs/versions/v0.43/v0.43.1_business_flow_artifact_quality_restore.md",
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": False,
        "copy_paste_restore_prompt_required": True,
        "required_sections_present": True,
        "suitable_for_new_session_handoff": True,
    }
    return V0431IntegratedRestoreDocumentManifest(**_merge(defaults, overrides))


def build_v043_artifact_from_provider_output(
    flow_kind: str,
    rendered_text: str,
    session_id: str,
    run_id: str | None,
    provider_invoked: bool,
    prompt_submitted: bool,
    response_parse_status: str | None = None,
) -> V043BusinessArtifactEnvelope:
    artifact_type = _artifact_type_for_flow(flow_kind)
    first = create_v043_business_artifact_section(
        title=_required_sections_for_artifact(artifact_type)[0],
        content=_clean_provider_text(rendered_text),
        grounding_class=V043GroundingClass.DATA_BASED_INTERPRETATION.value if provider_invoked else V043GroundingClass.SESSION_EVIDENCE.value,
        confidence="medium",
        source_summary="provider output over explicit user/session context" if provider_invoked else "bounded session context",
        requires_verification=False,
    )
    sections = (first,) + tuple(section for section in _default_sections(artifact_type, "알 수 없음") if section.title != first.title)
    artifact = create_v043_business_artifact(
        artifact_type=artifact_type,
        title=_title_for_artifact(artifact_type),
        sections=sections,
        session_id=session_id,
        run_id=run_id,
        flow_kind=flow_kind,
        provider_generated=provider_invoked,
        grounded_in_session=True,
    )
    envelope = create_v043_business_artifact_envelope(
        artifact,
        provider_invoked=provider_invoked,
        prompt_submitted=prompt_submitted,
        response_parse_status=response_parse_status,
    )
    return remember_v043_business_artifact(envelope)


def _clean_provider_text(text: str) -> str:
    hidden = ("[v0.41.4", "profile:", "session:", "trace runtime", "provider text is untrusted")
    lines = [line for line in text.splitlines() if not line.strip().startswith(hidden)]
    return "\n".join(lines).strip() or "응답 본문이 비어 있습니다."


def _revision_safe_text(text: str) -> str:
    blocked_fragments = ("safety:", "shell=", "subagent=", "workspace_mutated=", "memory_mutated=", "production_certified=")
    return "\n".join(line for line in text.splitlines() if not any(fragment in line for fragment in blocked_fragments)).strip()


def _render_artifact(artifact: V043BusinessArtifact) -> str:
    lines = [artifact.title, f"type: {artifact.artifact_type}", ""]
    for section in artifact.sections:
        lines.append(f"## {section.title}")
        lines.append(section.content)
        lines.append(f"grounding: {section.grounding_class}; confidence: {section.confidence}; verification_required: {str(section.requires_verification).lower()}")
        if section.source_summary:
            lines.append(f"source: {section.source_summary}")
        lines.append("")
    lines.append("safety: shell=false; subagent=false; workspace_mutated=false; memory_mutated=false; production_certified=false")
    return "\n".join(lines).strip()


__all__ = [
    name
    for name in globals()
    if name.startswith("V043")
    or name.startswith("create_v043")
    or name.startswith("build_v043")
    or name.startswith("execute_v043")
    or name.startswith("evaluate_v043")
    or name.startswith("remember_v043")
    or name.startswith("get_v043")
]
