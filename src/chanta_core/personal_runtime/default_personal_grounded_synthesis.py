"""v0.43.4 evidence-grounded business synthesis.

Provider-backed synthesis is allowed only when the user explicitly invokes a
grounded workflow command. Evidence selection, evidence-used views, and
grounding checks remain deterministic and non-provider by default.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Mapping, Sequence

from chanta_core.personal_runtime.default_personal_cli_bootstrap import PROFILE_ID
from chanta_core.personal_runtime.default_personal_local_evidence_retrieval import (
    V043EvidenceMatch,
    V043EvidencePack,
    create_v043_evidence_last_request,
    create_v043_evidence_pack,
    create_v043_evidence_pack_summary,
    create_v043_evidence_search_request,
    execute_v043_evidence_last,
    get_v043_last_evidence_pack,
    search_v043_local_evidence,
)
from chanta_core.personal_runtime.default_personal_run import RunCommandInput, execute_run_command


V0434_VERSION = "v0.43.4"
V0434_RELEASE_NAME = "v0.43.4 Evidence-Grounded Business Flow Synthesis"


class V043GroundedSynthesisMode(StrEnum):
    EXPLICIT_GROUNDED_SYNTHESIS = "explicit_grounded_synthesis"
    EVIDENCE_SELECTION_ONLY = "evidence_selection_only"
    DETERMINISTIC_GROUNDING_CHECK = "deterministic_grounding_check"
    EVIDENCE_USED_VIEW = "evidence_used_view"
    PROVIDER_SYNTHESIS = "provider_synthesis"
    UNKNOWN = "unknown"


class V043GroundedWorkflowKind(StrEnum):
    GROUNDED_SUMMARY = "grounded_summary"
    GROUNDED_TODO = "grounded_todo"
    GROUNDED_MEMO = "grounded_memo"
    GROUNDED_DECISION = "grounded_decision"
    GROUNDED_HANDOFF = "grounded_handoff"
    GROUNDING_CHECK = "grounding_check"
    EVIDENCE_USED = "evidence_used"
    UNKNOWN = "unknown"


class V043EvidenceUseStatus(StrEnum):
    ACTIVE = "active"
    SELECTED = "selected"
    UNAVAILABLE = "unavailable"
    EMPTY = "empty"
    EXPIRED = "expired"
    NOT_FOUND = "not_found"
    BLOCKED_BY_POLICY = "blocked_by_policy"
    UNKNOWN = "unknown"


class V043ClaimGroundingStatus(StrEnum):
    EVIDENCE_BACKED = "evidence_backed"
    PARTIALLY_SUPPORTED = "partially_supported"
    UNSUPPORTED_ASSUMPTION = "unsupported_assumption"
    UNKNOWN_NEEDS_VERIFICATION = "unknown_needs_verification"
    CONTRADICTED_BY_EVIDENCE = "contradicted_by_evidence"
    NOT_CHECKED = "not_checked"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V043EvidenceUsePolicy:
    policy_id: str
    requires_explicit_user_command_for_provider_synthesis: bool
    active_evidence_pack_required_for_synthesis: bool
    allow_query_to_create_evidence_pack: bool
    allowed_evidence_source_kinds: tuple[str, ...]
    cite_evidence_ids_required: bool
    unsupported_claims_must_be_marked: bool
    arbitrary_file_search_allowed: bool
    repo_search_allowed: bool
    workspace_search_allowed: bool
    external_search_allowed: bool
    shell_execution_allowed: bool
    tool_calling_allowed: bool
    function_calling_allowed: bool
    subagent_allowed: bool
    memory_mutation_allowed: bool
    core_memory_write_allowed: bool
    production_certified: bool


@dataclass(frozen=True)
class V043EvidenceCitation:
    citation_id: str
    evidence_item_id: str
    source_kind: str
    source_id: str | None
    snippet: str
    supports_claim_id: str | None
    bounded_source: bool


@dataclass(frozen=True)
class V043EvidenceBackedClaim:
    claim_id: str
    claim_text: str
    grounding_status: str
    citations: tuple[V043EvidenceCitation, ...]
    confidence: str
    requires_verification: bool


@dataclass(frozen=True)
class V043UnsupportedClaim:
    claim_id: str
    claim_text: str
    reason_unsupported: str
    suggested_label: str
    requires_user_verification: bool


@dataclass(frozen=True)
class V043ActiveEvidencePackState:
    state_id: str
    evidence_pack_id: str | None
    query_text: str | None
    match_count: int
    selected_evidence_item_ids: tuple[str, ...]
    source_kinds: tuple[str, ...]
    status: str
    provider_invoked: bool
    prompt_submitted: bool
    arbitrary_file_search_used: bool
    repo_search_used: bool
    shell_executed: bool
    memory_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V043UseEvidenceRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str | None
    query_text: str | None
    use_last: bool
    limit: int
    debug: bool


@dataclass(frozen=True)
class V043UseEvidenceResult:
    result_id: str
    active_state: V043ActiveEvidencePackState
    rendered_text: str
    source_disclosure_text: str
    provider_invoked: bool
    prompt_submitted: bool
    arbitrary_file_search_used: bool
    repo_search_used: bool
    shell_executed: bool
    memory_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V043GroundedSynthesisRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str
    workflow_kind: str
    user_instruction: str
    evidence_pack_id: str | None
    query_text: str | None
    provider: str | None
    timeout_seconds: int | None
    debug: bool


@dataclass(frozen=True)
class V043GroundedSynthesisPrompt:
    prompt_id: str
    workflow_kind: str
    runtime_identity_included: bool
    evidence_grounding_instruction_included: bool
    evidence_items_included: tuple[str, ...]
    citation_instruction_included: bool
    unsupported_claim_instruction_included: bool
    forbidden_capability_claims_included: bool
    prompt_text: str
    arbitrary_file_content_included: bool
    repo_content_included: bool
    shell_output_included: bool


@dataclass(frozen=True)
class V043GroundedSynthesisResult:
    result_id: str
    workflow_kind: str
    status: str
    rendered_text: str
    run_id: str | None
    session_id: str
    evidence_pack_id: str | None
    used_evidence_item_ids: tuple[str, ...]
    response_parse_status: str | None
    provider_invoked: bool
    prompt_submitted: bool
    arbitrary_file_search_used: bool
    repo_search_used: bool
    shell_executed: bool
    tool_calling_used: bool
    function_calling_used: bool
    subagent_invoked: bool
    memory_mutated: bool
    core_memory_written: bool
    production_certified: bool


@dataclass(frozen=True)
class V043GroundedArtifactSection:
    section_id: str
    title: str
    content: str
    claims: tuple[V043EvidenceBackedClaim, ...]
    unsupported_claims: tuple[V043UnsupportedClaim, ...]
    evidence_item_ids: tuple[str, ...]
    requires_verification: bool


@dataclass(frozen=True)
class V043GroundedArtifact:
    artifact_id: str
    artifact_type: str
    workflow_kind: str
    title: str
    sections: tuple[V043GroundedArtifactSection, ...]
    evidence_pack_id: str | None
    used_evidence_item_ids: tuple[str, ...]
    unsupported_claim_count: int
    created_at: str
    session_id: str
    run_id: str | None
    provider_generated: bool
    evidence_grounded: bool
    production_certified: bool


@dataclass(frozen=True)
class V043GroundedSynthesisPIReviewRecord:
    review_id: str
    synthesis_id: str
    evidence_pack_id: str | None
    workflow_kind: str
    reconstructable_as_process_event: bool
    evidence_lineage_preserved: bool
    citation_policy_applied: bool
    unsupported_claims_marked: bool
    bounded_sources_only: bool
    high_risk_counts_zero: bool
    review_summary: str


@dataclass(frozen=True)
class V043GroundingVerificationReport:
    report_id: str
    artifact_id: str | None
    evidence_pack_id: str | None
    passed: bool
    score: float
    citation_count: int
    unsupported_claim_count: int
    missing_required_criteria: tuple[str, ...]
    warnings: tuple[str, ...]
    blocks_pilot_use: bool


@dataclass(frozen=True)
class V043GroundedArtifactEnvelope:
    envelope_id: str
    artifact: V043GroundedArtifact
    synthesis_result: V043GroundedSynthesisResult
    grounding_report: V043GroundingVerificationReport
    pi_review_record: V043GroundedSynthesisPIReviewRecord
    rendered_text: str
    debug_summary: str
    production_certified: bool


@dataclass(frozen=True)
class _GroundedTemplate:
    template_id: str
    workflow_kind: str
    system_instruction: str
    evidence_instruction: str
    required_sections: tuple[str, ...]
    citation_format: str
    unsupported_claim_policy: str
    output_language: str
    forbidden_claims: tuple[str, ...]


@dataclass(frozen=True)
class V043GroundedSummaryTemplate(_GroundedTemplate):
    pass


@dataclass(frozen=True)
class V043GroundedTodoTemplate(_GroundedTemplate):
    pass


@dataclass(frozen=True)
class V043GroundedMemoTemplate(_GroundedTemplate):
    pass


@dataclass(frozen=True)
class V043GroundedDecisionTemplate(_GroundedTemplate):
    pass


@dataclass(frozen=True)
class V043GroundedHandoffTemplate(_GroundedTemplate):
    pass


@dataclass(frozen=True)
class V043GroundingVerificationCriterion:
    criterion_id: str
    title: str
    description: str
    required: bool
    severity_if_failed: str


@dataclass(frozen=True)
class V043EvidenceUsedRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str | None


@dataclass(frozen=True)
class V043EvidenceUsedResult:
    result_id: str
    found: bool
    evidence_pack_id: str | None
    used_evidence_item_ids: tuple[str, ...]
    rendered_text: str
    provider_invoked: bool
    prompt_submitted: bool
    filesystem_written: bool
    production_certified: bool


@dataclass(frozen=True)
class V043GroundingCheckRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str | None


@dataclass(frozen=True)
class V043GroundingCheckResult:
    result_id: str
    found: bool
    report: V043GroundingVerificationReport | None
    rendered_text: str
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    production_certified: bool


@dataclass(frozen=True)
class V043EvidenceUsageTraceRecord:
    trace_record_id: str
    event_kind: str
    evidence_pack_id: str | None
    used_evidence_item_ids: tuple[str, ...]
    workflow_kind: str
    run_id: str | None
    session_id: str
    provider_invoked: bool
    prompt_submitted: bool
    arbitrary_file_search_used: bool
    repo_search_used: bool
    shell_executed: bool
    tool_calling_used: bool
    function_calling_used: bool
    subagent_invoked: bool
    memory_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V043GroundedSynthesisSafetyReport:
    report_id: str
    explicit_grounded_provider_synthesis_opened: bool
    provider_invocation_requires_explicit_command: bool
    arbitrary_file_search_allowed: bool
    repo_search_allowed: bool
    workspace_search_allowed: bool
    external_search_allowed: bool
    shell_execution_allowed: bool
    provider_tool_calling_allowed: bool
    function_calling_allowed: bool
    subagent_allowed: bool
    memory_mutation_allowed: bool
    core_memory_write_allowed: bool
    production_certified: bool


@dataclass(frozen=True)
class V0434ReadinessReport:
    report_id: str
    evidence_use_policy_ready: bool
    active_evidence_pack_ready: bool
    grounded_synthesis_prompt_ready: bool
    grounded_summary_ready: bool
    grounded_todo_ready: bool
    grounded_memo_ready: bool
    grounded_decision_ready: bool
    grounded_handoff_ready: bool
    grounding_verification_ready: bool
    evidence_used_view_ready: bool
    evidence_usage_trace_ready: bool
    grounded_synthesis_pi_review_ready: bool
    integrated_restore_document_ready: bool
    v0435_handoff_ready: bool
    ready_for_arbitrary_file_search: bool
    ready_for_repo_search: bool
    ready_for_workspace_search: bool
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
class V0435PilotReviewAndWorkflowAcceptanceHandoff:
    handoff_id: str
    target_version: str
    recommended_focus: tuple[str, ...]
    must_not_open: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V0434IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool
    content_summary: str
    restore_value: str


@dataclass(frozen=True)
class V0434IntegratedRestoreContextSnapshot:
    snapshot_id: str
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]
    integrated_doc_path: str
    next_recommended_version: str


@dataclass(frozen=True)
class V0434IntegratedRestorePacket:
    restore_packet_id: str
    snapshot: V0434IntegratedRestoreContextSnapshot
    restore_sections: tuple[V0434IntegratedRestoreSection, ...]
    required_test_commands: tuple[str, ...]
    single_integrated_doc_path: str
    separate_restore_doc_created: bool


@dataclass(frozen=True)
class V0434IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_path: str
    integrated_doc_required: bool
    separate_restore_doc_allowed: bool
    separate_restore_doc_created: bool
    copy_paste_restore_prompt_required: bool
    required_sections_present: bool
    suitable_for_new_session_handoff: bool


_ACTIVE_PACK_BY_SESSION: dict[str, V043EvidencePack] = {}
_ACTIVE_STATE_BY_SESSION: dict[str, V043ActiveEvidencePackState] = {}
_LAST_GROUNDED_BY_SESSION: dict[str, V043GroundedArtifactEnvelope] = {}


def _merge(defaults: dict[str, Any], overrides: Mapping[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    merged.update(overrides)
    return merged


def _now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _new_id(prefix: str) -> str:
    return f"{prefix}-{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}"


def get_v043_last_grounded_artifact(session_id: str) -> V043GroundedArtifactEnvelope | None:
    return _LAST_GROUNDED_BY_SESSION.get(session_id)


def list_v043_grounded_artifacts() -> tuple[V043GroundedArtifactEnvelope, ...]:
    return tuple(_LAST_GROUNDED_BY_SESSION.values())


def _resolve_home(home_path: str | None) -> str:
    return str(Path(home_path or os.environ.get("CHANTACORE_HOME") or Path.cwd() / ".chantacore-personal").resolve())


def _short(text: str, limit: int = 900) -> str:
    normalized = " ".join(str(text).split())
    return normalized if len(normalized) <= limit else normalized[: limit - 3] + "..."


def _item_ref(match: V043EvidenceMatch) -> str:
    item = match.item
    if item.note_id:
        return f"NOTE:{item.note_id}"
    if item.artifact_id:
        return f"ART:{item.artifact_id}"
    if item.feedback_id:
        return f"FB:{item.feedback_id}"
    if item.run_id:
        return f"RUN:{item.run_id}"
    return f"EVID:{item.item_id}"


def _used_item_ids(pack: V043EvidencePack | None) -> tuple[str, ...]:
    if not pack:
        return ()
    return tuple(match.item.item_id for match in pack.matches)


def _source_kinds(pack: V043EvidencePack | None) -> tuple[str, ...]:
    if not pack:
        return ()
    return tuple(dict.fromkeys(match.item.source_kind for match in pack.matches))


def _workflow_artifact_type(workflow_kind: str) -> str:
    return {
        V043GroundedWorkflowKind.GROUNDED_SUMMARY.value: "summary",
        V043GroundedWorkflowKind.GROUNDED_TODO.value: "todo",
        V043GroundedWorkflowKind.GROUNDED_MEMO.value: "memo",
        V043GroundedWorkflowKind.GROUNDED_DECISION.value: "decision_brief",
        V043GroundedWorkflowKind.GROUNDED_HANDOFF.value: "handoff_note",
    }.get(workflow_kind, "unknown")


def _required_sections(workflow_kind: str) -> tuple[str, ...]:
    return {
        V043GroundedWorkflowKind.GROUNDED_SUMMARY.value: ("핵심 요약", "근거", "다음 액션", "불확실 / 확인 필요"),
        V043GroundedWorkflowKind.GROUNDED_TODO.value: ("action", "source evidence ids", "owner", "due date", "dependency", "priority", "unknowns"),
        V043GroundedWorkflowKind.GROUNDED_MEMO.value: ("context", "key points with evidence ids", "decisions with evidence ids", "open questions", "next actions", "unsupported assumptions"),
        V043GroundedWorkflowKind.GROUNDED_DECISION.value: ("decision target", "evidence-backed facts", "interpretations", "options", "tradeoffs", "risks", "recommendation", "unsupported assumptions / unknowns"),
        V043GroundedWorkflowKind.GROUNDED_HANDOFF.value: ("background", "current state", "work completed", "remaining work", "risks", "next actions", "evidence limitations"),
    }.get(workflow_kind, ("grounded content", "evidence ids", "unknowns"))


def create_v043_evidence_use_policy(**overrides: Any) -> V043EvidenceUsePolicy:
    defaults = {
        "policy_id": "v0434-evidence-use-policy",
        "requires_explicit_user_command_for_provider_synthesis": True,
        "active_evidence_pack_required_for_synthesis": True,
        "allow_query_to_create_evidence_pack": True,
        "allowed_evidence_source_kinds": (
            "local_work_note",
            "memory_candidate",
            "business_artifact",
            "feedback_record",
            "trace_summary",
            "run_report",
            "session_summary",
            "current_session",
        ),
        "cite_evidence_ids_required": True,
        "unsupported_claims_must_be_marked": True,
        "arbitrary_file_search_allowed": False,
        "repo_search_allowed": False,
        "workspace_search_allowed": False,
        "external_search_allowed": False,
        "shell_execution_allowed": False,
        "tool_calling_allowed": False,
        "function_calling_allowed": False,
        "subagent_allowed": False,
        "memory_mutation_allowed": False,
        "core_memory_write_allowed": False,
        "production_certified": False,
    }
    return V043EvidenceUsePolicy(**_merge(defaults, overrides))


def create_v043_evidence_citation(
    evidence_item_id: str = "evidence-item",
    source_kind: str = "local_work_note",
    source_id: str | None = None,
    snippet: str = "",
    supports_claim_id: str | None = None,
    **overrides: Any,
) -> V043EvidenceCitation:
    defaults = {
        "citation_id": _new_id("v043-evidence-citation"),
        "evidence_item_id": evidence_item_id,
        "source_kind": source_kind,
        "source_id": source_id,
        "snippet": _short(snippet, 500),
        "supports_claim_id": supports_claim_id,
        "bounded_source": True,
    }
    return V043EvidenceCitation(**_merge(defaults, overrides))


def create_v043_evidence_backed_claim(
    claim_text: str = "Evidence-backed claim",
    citations: Sequence[V043EvidenceCitation] = (),
    grounding_status: str | None = None,
    **overrides: Any,
) -> V043EvidenceBackedClaim:
    actual_citations = tuple(citations)
    status = grounding_status or (V043ClaimGroundingStatus.EVIDENCE_BACKED.value if actual_citations else V043ClaimGroundingStatus.UNKNOWN_NEEDS_VERIFICATION.value)
    if status == V043ClaimGroundingStatus.EVIDENCE_BACKED.value and not actual_citations:
        status = V043ClaimGroundingStatus.UNKNOWN_NEEDS_VERIFICATION.value
    defaults = {
        "claim_id": _new_id("v043-backed-claim"),
        "claim_text": claim_text,
        "grounding_status": status,
        "citations": actual_citations,
        "confidence": "high" if status == V043ClaimGroundingStatus.EVIDENCE_BACKED.value else "unknown",
        "requires_verification": status != V043ClaimGroundingStatus.EVIDENCE_BACKED.value,
    }
    return V043EvidenceBackedClaim(**_merge(defaults, overrides))


def create_v043_unsupported_claim(
    claim_text: str = "Unsupported claim",
    reason_unsupported: str = "No bounded evidence item supports this claim.",
    suggested_label: str = "unknown_needs_verification",
    **overrides: Any,
) -> V043UnsupportedClaim:
    defaults = {
        "claim_id": _new_id("v043-unsupported-claim"),
        "claim_text": claim_text,
        "reason_unsupported": reason_unsupported,
        "suggested_label": suggested_label,
        "requires_user_verification": True,
    }
    return V043UnsupportedClaim(**_merge(defaults, overrides))


def create_v043_active_evidence_pack_state(
    pack: V043EvidencePack | None = None,
    status: str | None = None,
    **overrides: Any,
) -> V043ActiveEvidencePackState:
    defaults = {
        "state_id": _new_id("v043-active-evidence"),
        "evidence_pack_id": pack.pack_id if pack else None,
        "query_text": pack.query_text if pack else None,
        "match_count": len(pack.matches) if pack else 0,
        "selected_evidence_item_ids": _used_item_ids(pack),
        "source_kinds": _source_kinds(pack),
        "status": status or (V043EvidenceUseStatus.ACTIVE.value if pack and pack.matches else V043EvidenceUseStatus.EMPTY.value if pack else V043EvidenceUseStatus.UNAVAILABLE.value),
        "provider_invoked": False,
        "prompt_submitted": False,
        "arbitrary_file_search_used": False,
        "repo_search_used": False,
        "shell_executed": False,
        "memory_mutated": False,
        "production_certified": False,
    }
    return V043ActiveEvidencePackState(**_merge(defaults, overrides))


def create_v043_use_evidence_request(
    query_text: str | None = None,
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    session_id: str | None = None,
    use_last: bool = False,
    limit: int = 5,
    debug: bool = False,
    **overrides: Any,
) -> V043UseEvidenceRequest:
    defaults = {
        "request_id": _new_id("v043-use-evidence-request"),
        "profile_id": profile_id,
        "home_path": home_path,
        "session_id": session_id,
        "query_text": query_text.strip() if query_text else None,
        "use_last": bool(use_last),
        "limit": max(1, min(int(limit), 10)),
        "debug": bool(debug),
    }
    request = V043UseEvidenceRequest(**_merge(defaults, overrides))
    if not request.use_last and not request.query_text:
        raise ValueError("query_text or use_last=True is required")
    return request


def create_v043_use_evidence_result(
    active_state: V043ActiveEvidencePackState | None = None,
    rendered_text: str | None = None,
    source_disclosure_text: str = "",
    **overrides: Any,
) -> V043UseEvidenceResult:
    state = active_state or create_v043_active_evidence_pack_state(None)
    defaults = {
        "result_id": _new_id("v043-use-evidence-result"),
        "active_state": state,
        "rendered_text": rendered_text or _render_use_evidence(state, source_disclosure_text),
        "source_disclosure_text": source_disclosure_text,
        "provider_invoked": False,
        "prompt_submitted": False,
        "arbitrary_file_search_used": False,
        "repo_search_used": False,
        "shell_executed": False,
        "memory_mutated": False,
        "production_certified": False,
    }
    return V043UseEvidenceResult(**_merge(defaults, overrides))


def execute_v043_use_evidence(request: V043UseEvidenceRequest, **overrides: Any) -> V043UseEvidenceResult:
    pack: V043EvidencePack | None
    if request.use_last:
        pack = get_v043_last_evidence_pack(request.profile_id)
        if not pack:
            last = execute_v043_evidence_last(create_v043_evidence_last_request(request.profile_id, request.home_path))
            pack = last.evidence_pack
    else:
        search = search_v043_local_evidence(create_v043_evidence_search_request(request.query_text or "", request.profile_id, request.home_path, limit=request.limit))
        pack = get_v043_last_evidence_pack(request.profile_id)
        if not pack:
            pack = create_v043_evidence_pack(search.query.raw_query, search.matches)
    state = create_v043_active_evidence_pack_state(pack)
    if request.session_id and pack:
        _ACTIVE_PACK_BY_SESSION[request.session_id] = pack
        _ACTIVE_STATE_BY_SESSION[request.session_id] = state
    disclosure = pack.source_disclosure.rendered_text if pack else "No evidence pack selected."
    return create_v043_use_evidence_result(state, source_disclosure_text=disclosure, **overrides)


def create_v043_grounded_synthesis_request(
    workflow_kind: str,
    user_instruction: str,
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    session_id: str = "work-session",
    evidence_pack_id: str | None = None,
    query_text: str | None = None,
    provider: str | None = None,
    timeout_seconds: int | None = 60,
    debug: bool = False,
    **overrides: Any,
) -> V043GroundedSynthesisRequest:
    allowed = {
        V043GroundedWorkflowKind.GROUNDED_SUMMARY.value,
        V043GroundedWorkflowKind.GROUNDED_TODO.value,
        V043GroundedWorkflowKind.GROUNDED_MEMO.value,
        V043GroundedWorkflowKind.GROUNDED_DECISION.value,
        V043GroundedWorkflowKind.GROUNDED_HANDOFF.value,
    }
    if workflow_kind not in allowed:
        raise ValueError("workflow_kind must be a grounded business workflow")
    if not user_instruction.strip():
        raise ValueError("user_instruction must be non-empty")
    if not evidence_pack_id and not query_text and session_id not in _ACTIVE_PACK_BY_SESSION:
        raise ValueError("evidence_pack_id, query_text, or active evidence pack is required")
    defaults = {
        "request_id": _new_id("v043-grounded-synthesis-request"),
        "profile_id": profile_id,
        "home_path": home_path,
        "session_id": session_id,
        "workflow_kind": workflow_kind,
        "user_instruction": user_instruction.strip(),
        "evidence_pack_id": evidence_pack_id,
        "query_text": query_text.strip() if query_text else None,
        "provider": provider,
        "timeout_seconds": timeout_seconds,
        "debug": bool(debug),
    }
    return V043GroundedSynthesisRequest(**_merge(defaults, overrides))


def _pack_for_request(request: V043GroundedSynthesisRequest) -> V043EvidencePack | None:
    active = _ACTIVE_PACK_BY_SESSION.get(request.session_id)
    if active and (request.evidence_pack_id is None or active.pack_id == request.evidence_pack_id):
        return active
    if request.query_text:
        selection = execute_v043_use_evidence(create_v043_use_evidence_request(request.query_text, request.profile_id, request.home_path, request.session_id))
        return _ACTIVE_PACK_BY_SESSION.get(request.session_id) if selection.active_state.evidence_pack_id else None
    last = get_v043_last_evidence_pack(request.profile_id)
    if last and (request.evidence_pack_id is None or last.pack_id == request.evidence_pack_id):
        return last
    return None


def create_v043_grounded_synthesis_prompt(
    workflow_kind: str,
    prompt_text: str,
    evidence_items_included: Sequence[str],
    **overrides: Any,
) -> V043GroundedSynthesisPrompt:
    defaults = {
        "prompt_id": _new_id("v043-grounded-prompt"),
        "workflow_kind": workflow_kind,
        "runtime_identity_included": True,
        "evidence_grounding_instruction_included": True,
        "evidence_items_included": tuple(evidence_items_included),
        "citation_instruction_included": True,
        "unsupported_claim_instruction_included": True,
        "forbidden_capability_claims_included": True,
        "prompt_text": prompt_text,
        "arbitrary_file_content_included": False,
        "repo_content_included": False,
        "shell_output_included": False,
    }
    return V043GroundedSynthesisPrompt(**_merge(defaults, overrides))


def build_v043_grounded_synthesis_prompt(request: V043GroundedSynthesisRequest, pack: V043EvidencePack | None = None) -> V043GroundedSynthesisPrompt:
    actual_pack = pack or _pack_for_request(request)
    evidence_lines: list[str] = []
    included: list[str] = []
    if actual_pack:
        for match in actual_pack.matches[:10]:
            ref = _item_ref(match)
            included.append(match.item.item_id)
            evidence_lines.append(f"- [{ref}] evidence_item_id={match.item.item_id}; source_kind={match.item.source_kind}; source_id={match.item.source_id or '-'}; snippet={match.item.snippet}")
    template = _template_for_workflow(request.workflow_kind)
    prompt = "\n".join(
        (
            "You are ChantaCore default-personal runtime, a Korean polite business/work assistant.",
            "Use only the bounded local evidence pack below and the user's instruction.",
            "Cite local evidence ids for important claims using [EVID:<id>], [NOTE:<id>], [ART:<id>], [FB:<id>], [RUN:<id>], or [TRACE:<id>].",
            "Do not invent evidence ids. If evidence is missing, label it as assumption or unknown / needs verification.",
            "Do not claim arbitrary file access, repository inspection, command execution, delegated-agent use, memory mutation, CORE_MEMORY write, external search, or production automation.",
            f"Workflow: {request.workflow_kind}",
            f"Required sections: {', '.join(template.required_sections)}",
            "",
            "[Evidence Pack]",
            f"evidence_pack_id: {actual_pack.pack_id if actual_pack else '-'}",
            "\n".join(evidence_lines) if evidence_lines else "- no evidence items available",
            "",
            "[User Instruction]",
            request.user_instruction,
        )
    )
    return create_v043_grounded_synthesis_prompt(request.workflow_kind, prompt, included)


def create_v043_grounded_synthesis_result(
    workflow_kind: str,
    rendered_text: str = "",
    session_id: str = "work-session",
    evidence_pack_id: str | None = None,
    used_evidence_item_ids: Sequence[str] = (),
    run_id: str | None = None,
    response_parse_status: str | None = "parsed_text",
    status: str = "completed",
    **overrides: Any,
) -> V043GroundedSynthesisResult:
    defaults = {
        "result_id": _new_id("v043-grounded-synthesis-result"),
        "workflow_kind": workflow_kind,
        "status": status,
        "rendered_text": rendered_text,
        "run_id": run_id,
        "session_id": session_id,
        "evidence_pack_id": evidence_pack_id,
        "used_evidence_item_ids": tuple(used_evidence_item_ids),
        "response_parse_status": response_parse_status,
        "provider_invoked": True,
        "prompt_submitted": True,
        "arbitrary_file_search_used": False,
        "repo_search_used": False,
        "shell_executed": False,
        "tool_calling_used": False,
        "function_calling_used": False,
        "subagent_invoked": False,
        "memory_mutated": False,
        "core_memory_written": False,
        "production_certified": False,
    }
    return V043GroundedSynthesisResult(**_merge(defaults, overrides))


def execute_v043_grounded_synthesis(request: V043GroundedSynthesisRequest, **overrides: Any) -> V043GroundedSynthesisResult:
    pack = _pack_for_request(request)
    if not pack or not pack.matches:
        return create_v043_grounded_synthesis_result(
            request.workflow_kind,
            "No active evidence pack is available. Run /use-evidence <query> first.",
            request.session_id,
            pack.pack_id if pack else None,
            (),
            None,
            None,
            "blocked",
            provider_invoked=False,
            prompt_submitted=False,
            **overrides,
        )
    prompt = build_v043_grounded_synthesis_prompt(request, pack)
    run = execute_run_command(
        RunCommandInput(
            profile_id=request.profile_id,
            home_path=_resolve_home(request.home_path),
            user_input=prompt.prompt_text,
            session_id=request.session_id,
            provider=request.provider,
            mock_provider=request.provider == "mock",
            timeout_seconds=float(request.timeout_seconds or 60),
        )
    )
    refs = ", ".join(_item_ref(match) for match in pack.matches[:5])
    rendered = "\n".join(
        (
            run.rendered_text,
            "",
            "Evidence grounding",
            f"evidence_pack_id: {pack.pack_id}",
            f"used_evidence_item_ids: {', '.join(_used_item_ids(pack))}",
            f"local citations expected: {refs}",
            "unsupported_claim_policy: unsupported claims must be labeled assumption or unknown_needs_verification",
        )
    )
    return create_v043_grounded_synthesis_result(
        request.workflow_kind,
        rendered,
        request.session_id,
        pack.pack_id,
        _used_item_ids(pack),
        getattr(run.run_result, "result_id", None),
        "parsed_text" if run.exit_code == 0 else "provider_error",
        "completed" if run.exit_code == 0 else "provider_run_failed",
        provider_invoked=run.provider_invoked,
        prompt_submitted=run.prompt_submitted,
        **overrides,
    )


def create_v043_grounded_artifact_section(
    title: str = "Grounded section",
    content: str = "",
    claims: Sequence[V043EvidenceBackedClaim] = (),
    unsupported_claims: Sequence[V043UnsupportedClaim] = (),
    evidence_item_ids: Sequence[str] = (),
    **overrides: Any,
) -> V043GroundedArtifactSection:
    defaults = {
        "section_id": _new_id("v043-grounded-section"),
        "title": title,
        "content": content,
        "claims": tuple(claims),
        "unsupported_claims": tuple(unsupported_claims),
        "evidence_item_ids": tuple(evidence_item_ids),
        "requires_verification": bool(unsupported_claims),
    }
    return V043GroundedArtifactSection(**_merge(defaults, overrides))


def create_v043_grounded_artifact(
    workflow_kind: str = V043GroundedWorkflowKind.GROUNDED_SUMMARY.value,
    evidence_pack_id: str | None = "pack-test",
    used_evidence_item_ids: Sequence[str] = ("evidence-item",),
    session_id: str = "work-session",
    run_id: str | None = None,
    sections: Sequence[V043GroundedArtifactSection] | None = None,
    **overrides: Any,
) -> V043GroundedArtifact:
    actual_sections = tuple(sections or (create_v043_grounded_artifact_section("Evidence-backed content", "See cited local evidence.", evidence_item_ids=used_evidence_item_ids),))
    unsupported_count = sum(len(section.unsupported_claims) for section in actual_sections)
    defaults = {
        "artifact_id": _new_id("v043-grounded-artifact"),
        "artifact_type": _workflow_artifact_type(workflow_kind),
        "workflow_kind": workflow_kind,
        "title": workflow_kind.replace("_", " ").title(),
        "sections": actual_sections,
        "evidence_pack_id": evidence_pack_id,
        "used_evidence_item_ids": tuple(used_evidence_item_ids),
        "unsupported_claim_count": unsupported_count,
        "created_at": _now(),
        "session_id": session_id,
        "run_id": run_id,
        "provider_generated": True,
        "evidence_grounded": bool(evidence_pack_id and tuple(used_evidence_item_ids)),
        "production_certified": False,
    }
    return V043GroundedArtifact(**_merge(defaults, overrides))


def create_v043_grounded_artifact_envelope(
    synthesis_result: V043GroundedSynthesisResult | None = None,
    artifact: V043GroundedArtifact | None = None,
    **overrides: Any,
) -> V043GroundedArtifactEnvelope:
    result = synthesis_result or create_v043_grounded_synthesis_result(V043GroundedWorkflowKind.GROUNDED_SUMMARY.value, "grounded output")
    actual_artifact = artifact or create_v043_grounded_artifact(result.workflow_kind, result.evidence_pack_id, result.used_evidence_item_ids, result.session_id, result.run_id)
    report = evaluate_v043_grounding(actual_artifact)
    pi = create_v043_grounded_synthesis_pi_review_record(result.result_id, actual_artifact.evidence_pack_id, actual_artifact.workflow_kind)
    rendered = _render_grounded_artifact(actual_artifact, result.rendered_text)
    defaults = {
        "envelope_id": _new_id("v043-grounded-envelope"),
        "artifact": actual_artifact,
        "synthesis_result": result,
        "grounding_report": report,
        "pi_review_record": pi,
        "rendered_text": rendered,
        "debug_summary": f"artifact_id={actual_artifact.artifact_id}; pack={actual_artifact.evidence_pack_id or '-'}; used={len(actual_artifact.used_evidence_item_ids)}; run={actual_artifact.run_id or '-'}",
        "production_certified": False,
    }
    envelope = V043GroundedArtifactEnvelope(**_merge(defaults, overrides))
    _LAST_GROUNDED_BY_SESSION[actual_artifact.session_id] = envelope
    return envelope


def _template_for_workflow(workflow_kind: str) -> _GroundedTemplate:
    builders = {
        V043GroundedWorkflowKind.GROUNDED_SUMMARY.value: build_v043_grounded_summary_template,
        V043GroundedWorkflowKind.GROUNDED_TODO.value: build_v043_grounded_todo_template,
        V043GroundedWorkflowKind.GROUNDED_MEMO.value: build_v043_grounded_memo_template,
        V043GroundedWorkflowKind.GROUNDED_DECISION.value: build_v043_grounded_decision_template,
        V043GroundedWorkflowKind.GROUNDED_HANDOFF.value: build_v043_grounded_handoff_template,
    }
    return builders.get(workflow_kind, build_v043_grounded_summary_template)()


def _base_template(workflow_kind: str, cls: type[_GroundedTemplate], **overrides: Any) -> _GroundedTemplate:
    defaults = {
        "template_id": f"v0434-template-{workflow_kind}",
        "workflow_kind": workflow_kind,
        "system_instruction": "Use Korean polite business language and ground claims in bounded local evidence only.",
        "evidence_instruction": "Use only supplied evidence items. Preserve evidence_pack_id and cite evidence ids.",
        "required_sections": _required_sections(workflow_kind),
        "citation_format": "[EVID:<evidence_item_id>] [NOTE:<note_id>] [ART:<artifact_id>] [FB:<feedback_id>] [RUN:<run_id>] [TRACE:<trace_record_id>]",
        "unsupported_claim_policy": "Do not present unsupported claims as facts. Mark them as assumption or unknown_needs_verification.",
        "output_language": "ko-KR",
        "forbidden_claims": (
            "web citations",
            "invented evidence ids",
            "arbitrary file access",
            "repo search",
            "shell execution",
            "tool calling",
            "function calling",
            "subagent use",
            "memory mutation",
            "production automation",
        ),
    }
    return cls(**_merge(defaults, overrides))


def build_v043_grounded_summary_template(**overrides: Any) -> V043GroundedSummaryTemplate:
    return _base_template(V043GroundedWorkflowKind.GROUNDED_SUMMARY.value, V043GroundedSummaryTemplate, **overrides)


def build_v043_grounded_todo_template(**overrides: Any) -> V043GroundedTodoTemplate:
    return _base_template(V043GroundedWorkflowKind.GROUNDED_TODO.value, V043GroundedTodoTemplate, **overrides)


def build_v043_grounded_memo_template(**overrides: Any) -> V043GroundedMemoTemplate:
    return _base_template(V043GroundedWorkflowKind.GROUNDED_MEMO.value, V043GroundedMemoTemplate, **overrides)


def build_v043_grounded_decision_template(**overrides: Any) -> V043GroundedDecisionTemplate:
    return _base_template(V043GroundedWorkflowKind.GROUNDED_DECISION.value, V043GroundedDecisionTemplate, **overrides)


def build_v043_grounded_handoff_template(**overrides: Any) -> V043GroundedHandoffTemplate:
    return _base_template(V043GroundedWorkflowKind.GROUNDED_HANDOFF.value, V043GroundedHandoffTemplate, **overrides)


def create_v043_grounding_verification_criterion(criterion_id: str = "has_evidence_pack", **overrides: Any) -> V043GroundingVerificationCriterion:
    descriptions = {
        "has_evidence_pack": "Grounded artifact preserves evidence_pack_id.",
        "cites_evidence_ids": "Important claims cite local evidence ids.",
        "unsupported_claims_marked": "Unsupported claims are labeled assumption or unknown.",
        "no_arbitrary_file_search": "No arbitrary file search is used.",
        "no_repo_search": "No repo search is used.",
        "no_shell": "No shell is used.",
        "no_tool_or_function_calling": "No provider tool/function calling is used.",
        "no_memory_mutation": "No memory mutation is used.",
        "no_core_memory_write": "CORE_MEMORY is untouched.",
        "source_disclosure_preserved": "Evidence source disclosure remains available.",
        "process_reviewable": "Evidence to synthesis to artifact lineage is reviewable.",
    }
    defaults = {
        "criterion_id": criterion_id,
        "title": criterion_id.replace("_", " "),
        "description": descriptions.get(criterion_id, criterion_id),
        "required": True,
        "severity_if_failed": "blocker" if criterion_id.startswith("no_") else "major",
    }
    return V043GroundingVerificationCriterion(**_merge(defaults, overrides))


def evaluate_v043_grounding(artifact: V043GroundedArtifact | None = None, **overrides: Any) -> V043GroundingVerificationReport:
    return create_v043_grounding_verification_report(artifact, **overrides)


def create_v043_grounding_verification_report(artifact: V043GroundedArtifact | None = None, **overrides: Any) -> V043GroundingVerificationReport:
    citation_count = len(artifact.used_evidence_item_ids) if artifact else 0
    unsupported = artifact.unsupported_claim_count if artifact else 0
    missing: list[str] = []
    if not artifact or not artifact.evidence_pack_id:
        missing.append("has_evidence_pack")
    if citation_count == 0:
        missing.append("cites_evidence_ids")
    defaults = {
        "report_id": _new_id("v043-grounding-report"),
        "artifact_id": artifact.artifact_id if artifact else None,
        "evidence_pack_id": artifact.evidence_pack_id if artifact else None,
        "passed": not missing,
        "score": 1.0 if not missing else max(0.0, 1.0 - 0.25 * len(missing)),
        "citation_count": citation_count,
        "unsupported_claim_count": unsupported,
        "missing_required_criteria": tuple(missing),
        "warnings": ("unsupported claims require user verification",) if unsupported else (),
        "blocks_pilot_use": bool(missing),
    }
    return V043GroundingVerificationReport(**_merge(defaults, overrides))


def create_v043_evidence_used_request(profile_id: str = PROFILE_ID, home_path: str | None = None, session_id: str | None = None, **overrides: Any) -> V043EvidenceUsedRequest:
    defaults = {"request_id": _new_id("v043-evidence-used-request"), "profile_id": profile_id, "home_path": home_path, "session_id": session_id}
    return V043EvidenceUsedRequest(**_merge(defaults, overrides))


def create_v043_evidence_used_result(pack: V043EvidencePack | None = None, used_ids: Sequence[str] = (), **overrides: Any) -> V043EvidenceUsedResult:
    found = bool(pack or used_ids)
    rendered = "No grounded evidence has been used yet."
    if found:
        rendered = "\n".join(("Evidence used", f"evidence_pack_id: {pack.pack_id if pack else '-'}", f"used_evidence_item_ids: {', '.join(used_ids) if used_ids else '-'}"))
    defaults = {
        "result_id": _new_id("v043-evidence-used-result"),
        "found": found,
        "evidence_pack_id": pack.pack_id if pack else None,
        "used_evidence_item_ids": tuple(used_ids),
        "rendered_text": rendered,
        "provider_invoked": False,
        "prompt_submitted": False,
        "filesystem_written": False,
        "production_certified": False,
    }
    return V043EvidenceUsedResult(**_merge(defaults, overrides))


def execute_v043_evidence_used(request: V043EvidenceUsedRequest, **overrides: Any) -> V043EvidenceUsedResult:
    envelope = _LAST_GROUNDED_BY_SESSION.get(request.session_id or "")
    if envelope:
        return create_v043_evidence_used_result(_ACTIVE_PACK_BY_SESSION.get(envelope.artifact.session_id), envelope.artifact.used_evidence_item_ids, **overrides)
    pack = _ACTIVE_PACK_BY_SESSION.get(request.session_id or "")
    ids = _used_item_ids(pack)
    return create_v043_evidence_used_result(pack, ids, **overrides)


def create_v043_grounding_check_request(profile_id: str = PROFILE_ID, home_path: str | None = None, session_id: str | None = None, **overrides: Any) -> V043GroundingCheckRequest:
    defaults = {"request_id": _new_id("v043-grounding-check-request"), "profile_id": profile_id, "home_path": home_path, "session_id": session_id}
    return V043GroundingCheckRequest(**_merge(defaults, overrides))


def create_v043_grounding_check_result(report: V043GroundingVerificationReport | None = None, **overrides: Any) -> V043GroundingCheckResult:
    found = report is not None
    rendered = "No grounded artifact is available. Run /grounded-summary, /grounded-decision, or /grounded-handoff first."
    if report:
        rendered = "\n".join(("Grounding check", f"passed: {str(report.passed).lower()}", f"citation_count: {report.citation_count}", f"unsupported_claim_count: {report.unsupported_claim_count}", f"missing_required_criteria: {', '.join(report.missing_required_criteria) if report.missing_required_criteria else '-'}"))
    defaults = {
        "result_id": _new_id("v043-grounding-check-result"),
        "found": found,
        "report": report,
        "rendered_text": rendered,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "production_certified": False,
    }
    return V043GroundingCheckResult(**_merge(defaults, overrides))


def execute_v043_grounding_check(request: V043GroundingCheckRequest, **overrides: Any) -> V043GroundingCheckResult:
    envelope = _LAST_GROUNDED_BY_SESSION.get(request.session_id or "")
    return create_v043_grounding_check_result(envelope.grounding_report if envelope else None, **overrides)


def create_v043_evidence_usage_trace_record(
    evidence_pack_id: str | None = None,
    used_evidence_item_ids: Sequence[str] = (),
    workflow_kind: str = V043GroundedWorkflowKind.GROUNDED_SUMMARY.value,
    run_id: str | None = None,
    session_id: str = "work-session",
    provider_invoked: bool = True,
    prompt_submitted: bool = True,
    **overrides: Any,
) -> V043EvidenceUsageTraceRecord:
    defaults = {
        "trace_record_id": _new_id("v043-evidence-usage-trace"),
        "event_kind": "evidence_used_for_grounded_synthesis",
        "evidence_pack_id": evidence_pack_id,
        "used_evidence_item_ids": tuple(used_evidence_item_ids),
        "workflow_kind": workflow_kind,
        "run_id": run_id,
        "session_id": session_id,
        "provider_invoked": bool(provider_invoked),
        "prompt_submitted": bool(prompt_submitted),
        "arbitrary_file_search_used": False,
        "repo_search_used": False,
        "shell_executed": False,
        "tool_calling_used": False,
        "function_calling_used": False,
        "subagent_invoked": False,
        "memory_mutated": False,
        "production_certified": False,
    }
    return V043EvidenceUsageTraceRecord(**_merge(defaults, overrides))


def create_v043_grounded_synthesis_pi_review_record(
    synthesis_id: str = "synthesis-test",
    evidence_pack_id: str | None = "pack-test",
    workflow_kind: str = V043GroundedWorkflowKind.GROUNDED_SUMMARY.value,
    **overrides: Any,
) -> V043GroundedSynthesisPIReviewRecord:
    defaults = {
        "review_id": _new_id("v043-grounded-pi-review"),
        "synthesis_id": synthesis_id,
        "evidence_pack_id": evidence_pack_id,
        "workflow_kind": workflow_kind,
        "reconstructable_as_process_event": True,
        "evidence_lineage_preserved": True,
        "citation_policy_applied": True,
        "unsupported_claims_marked": True,
        "bounded_sources_only": True,
        "high_risk_counts_zero": True,
        "review_summary": "Evidence pack to provider synthesis to grounded artifact lineage is preserved.",
    }
    return V043GroundedSynthesisPIReviewRecord(**_merge(defaults, overrides))


def create_v043_grounded_synthesis_safety_report(**overrides: Any) -> V043GroundedSynthesisSafetyReport:
    defaults = {
        "report_id": "v0434-grounded-synthesis-safety-report",
        "explicit_grounded_provider_synthesis_opened": True,
        "provider_invocation_requires_explicit_command": True,
        "arbitrary_file_search_allowed": False,
        "repo_search_allowed": False,
        "workspace_search_allowed": False,
        "external_search_allowed": False,
        "shell_execution_allowed": False,
        "provider_tool_calling_allowed": False,
        "function_calling_allowed": False,
        "subagent_allowed": False,
        "memory_mutation_allowed": False,
        "core_memory_write_allowed": False,
        "production_certified": False,
    }
    return V043GroundedSynthesisSafetyReport(**_merge(defaults, overrides))


def create_v0434_readiness_report(**overrides: Any) -> V0434ReadinessReport:
    defaults = {
        "report_id": "v0434-readiness-report",
        "evidence_use_policy_ready": True,
        "active_evidence_pack_ready": True,
        "grounded_synthesis_prompt_ready": True,
        "grounded_summary_ready": True,
        "grounded_todo_ready": True,
        "grounded_memo_ready": True,
        "grounded_decision_ready": True,
        "grounded_handoff_ready": True,
        "grounding_verification_ready": True,
        "evidence_used_view_ready": True,
        "evidence_usage_trace_ready": True,
        "grounded_synthesis_pi_review_ready": True,
        "integrated_restore_document_ready": True,
        "v0435_handoff_ready": True,
        "ready_for_arbitrary_file_search": False,
        "ready_for_repo_search": False,
        "ready_for_workspace_search": False,
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
    return V0434ReadinessReport(**_merge(defaults, overrides))


def create_v0435_pilot_review_and_workflow_acceptance_handoff(**overrides: Any) -> V0435PilotReviewAndWorkflowAcceptanceHandoff:
    defaults = {
        "handoff_id": "v0435-pilot-review-workflow-acceptance-handoff",
        "target_version": "v0.43.5 Pilot Review & Work Session Acceptance Metrics",
        "recommended_focus": (
            "evaluate actual pilot sessions",
            "score work-session usefulness",
            "score evidence-grounded outputs",
            "capture user feedback",
            "define v0.44 controlled workspace-read readiness",
            "keep arbitrary file search, repo search, shell, memory mutation, and production certification closed",
        ),
        "must_not_open": (
            "arbitrary file search",
            "repo search",
            "shell execution",
            "memory mutation",
            "CORE_MEMORY write",
            "production certification",
        ),
        "production_certified": False,
    }
    return V0435PilotReviewAndWorkflowAcceptanceHandoff(**_merge(defaults, overrides))


def create_v0434_integrated_restore_context_snapshot(**overrides: Any) -> V0434IntegratedRestoreContextSnapshot:
    defaults = {
        "snapshot_id": "v0434-integrated-restore-context",
        "current_version": V0434_VERSION,
        "current_track": "v0.43 Business Work Session Pilot & Process Intelligence Review Loop",
        "baseline_versions": ("v0.43.3", "v0.43.2", "v0.43.1", "v0.43.0", "v0.42.10"),
        "open_capabilities": ("explicit evidence-use policy", "active evidence pack", "grounded synthesis prompts", "grounded business artifacts", "/use-evidence", "/grounded-summary", "/grounding-check", "/evidence used"),
        "closed_capabilities": create_v0435_pilot_review_and_workflow_acceptance_handoff().must_not_open,
        "integrated_doc_path": "docs/versions/v0.43/v0.43.4_evidence_grounded_business_synthesis_restore.md",
        "next_recommended_version": "v0.43.5",
    }
    return V0434IntegratedRestoreContextSnapshot(**_merge(defaults, overrides))


def create_v0434_integrated_restore_packet(**overrides: Any) -> V0434IntegratedRestorePacket:
    titles = (
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "v0.43.3 Baseline Summary",
        "v0.43.4 Goal",
        "Evidence-Grounded Synthesis Concept",
        "Evidence Use Policy",
        "Active Evidence Pack",
        "Grounded Synthesis Commands",
        "Grounded Prompt Contract",
        "Evidence Citation Format",
        "Unsupported Claim Policy",
        "Grounded Artifact Model",
        "Grounding Verification",
        "Evidence Used View",
        "Evidence Usage Trace Record",
        "PI Review Contract",
        "Safety Boundary",
        "Required Test Commands",
        "Manual Pilot Commands",
        "Withdrawal Conditions",
        "v0.43.5 Recommended Next Step",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    )
    sections = tuple(V0434IntegratedRestoreSection(f"v0434-section-{index}", title, True, f"Required v0.43.4 section: {title}", "future-session restore") for index, title in enumerate(titles, 1))
    defaults = {
        "restore_packet_id": "v0434-integrated-restore-packet",
        "snapshot": create_v0434_integrated_restore_context_snapshot(),
        "restore_sections": sections,
        "required_test_commands": (
            "py -m pytest tests\\test_v0434_evidence_grounded_business_synthesis.py",
            "py -m pytest tests\\test_v0433_work_session_retrieval_local_evidence.py",
        ),
        "single_integrated_doc_path": "docs/versions/v0.43/v0.43.4_evidence_grounded_business_synthesis_restore.md",
        "separate_restore_doc_created": False,
    }
    return V0434IntegratedRestorePacket(**_merge(defaults, overrides))


def create_v0434_integrated_restore_document_manifest(**overrides: Any) -> V0434IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "v0434-integrated-restore-document-manifest",
        "integrated_doc_path": "docs/versions/v0.43/v0.43.4_evidence_grounded_business_synthesis_restore.md",
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": False,
        "copy_paste_restore_prompt_required": True,
        "required_sections_present": True,
        "suitable_for_new_session_handoff": True,
    }
    return V0434IntegratedRestoreDocumentManifest(**_merge(defaults, overrides))


def _render_use_evidence(state: V043ActiveEvidencePackState, disclosure: str) -> str:
    lines = [
        "Active evidence pack",
        f"status: {state.status}",
        f"evidence_pack_id: {state.evidence_pack_id or '-'}",
        f"matches: {state.match_count}",
        f"selected_evidence_item_ids: {', '.join(state.selected_evidence_item_ids) if state.selected_evidence_item_ids else '-'}",
        f"source_kinds: {', '.join(state.source_kinds) if state.source_kinds else '-'}",
        "provider_invoked: false; prompt_submitted: false; shell=false; memory_mutated=false",
    ]
    if disclosure:
        lines.extend(("", disclosure))
    return "\n".join(lines)


def _render_grounded_artifact(artifact: V043GroundedArtifact, body: str) -> str:
    lines = [
        artifact.title,
        f"workflow_kind: {artifact.workflow_kind}",
        f"evidence_pack_id: {artifact.evidence_pack_id or '-'}",
        f"used_evidence_item_ids: {', '.join(artifact.used_evidence_item_ids) if artifact.used_evidence_item_ids else '-'}",
        "",
        body,
        "",
        "safety: arbitrary_file_search=false; repo_search=false; shell=false; tools=false; functions=false; subagent=false; memory_mutated=false; core_memory_written=false; production_certified=false",
    ]
    return "\n".join(lines)


def _citation_count(text: str, used_ids: Sequence[str]) -> int:
    local_refs = re.findall(r"\[(?:EVID|NOTE|ART|FB|RUN|TRACE):[^\]]+\]", text)
    return max(len(local_refs), len(tuple(used_ids)))


__all__ = [
    name
    for name in globals()
    if name.startswith("V043")
    or name.startswith("create_v043")
    or name.startswith("build_v043")
    or name.startswith("execute_v043")
    or name.startswith("evaluate_v043")
]
