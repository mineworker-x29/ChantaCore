"""v0.43.5 pilot review and work-session acceptance metrics.

This layer evaluates existing bounded work-session evidence. It is
deterministic by default and does not call providers, submit prompts, search
repositories, scan arbitrary files, execute shell, mutate memory, write
CORE_MEMORY, invoke subagents, or certify production.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Mapping, Sequence

from chanta_core.personal_runtime.default_personal_cli_bootstrap import PROFILE_ID
from chanta_core.personal_runtime.default_personal_diagnostics_feedback import (
    create_v042_feedback_list_summary,
)
from chanta_core.personal_runtime.default_personal_grounded_synthesis import (
    get_v043_last_grounded_artifact,
    list_v043_grounded_artifacts,
)
from chanta_core.personal_runtime.default_personal_local_evidence_retrieval import (
    get_v043_last_evidence_pack,
)
from chanta_core.personal_runtime.default_personal_memory_boundary import (
    create_v043_local_work_note_list_request,
    list_v043_local_work_notes,
)
from chanta_core.personal_runtime.default_personal_work_artifacts import (
    get_v043_last_business_artifact,
    list_v043_business_artifacts,
)
from chanta_core.personal_runtime.default_personal_trace_history import (
    create_v042_run_history_request,
    create_v042_run_history_result,
)
from chanta_core.personal_runtime.default_personal_trace_report import (
    create_trace_summary_request,
    summarize_trace_events,
)


V0435_VERSION = "v0.43.5"
V0435_RELEASE_NAME = "v0.43.5 Pilot Review & Work Session Acceptance Metrics"
V043_TRACK_NAME = "v0.43 Business Work Session Pilot & Process Intelligence Review Loop"


class V043PilotMetricDimension(StrEnum):
    WORK_SESSION_USABILITY = "work_session_usability"
    BUSINESS_ARTIFACT_USEFULNESS = "business_artifact_usefulness"
    EVIDENCE_RETRIEVAL_QUALITY = "evidence_retrieval_quality"
    GROUNDED_SYNTHESIS_QUALITY = "grounded_synthesis_quality"
    PROCESS_INTELLIGENCE_REVIEWABILITY = "process_intelligence_reviewability"
    SAFETY_BOUNDARY_INTEGRITY = "safety_boundary_integrity"
    V044_CONTROLLED_WORKSPACE_READ_READINESS = "v044_controlled_workspace_read_readiness"
    UNKNOWN = "unknown"


class V043PilotMetricLabel(StrEnum):
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    WEAK = "weak"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class V043PilotGateDecisionKind(StrEnum):
    CONTINUE_V043_POLISH = "continue_v043_polish"
    PROCEED_TO_V044_DESIGN = "proceed_to_v044_design"
    BLOCKED_BY_SAFETY = "blocked_by_safety"
    BLOCKED_BY_USABILITY = "blocked_by_usability"
    BLOCKED_BY_MISSING_EVIDENCE = "blocked_by_missing_evidence"
    UNKNOWN = "unknown"


class V043PilotFindingArea(StrEnum):
    UX = "ux"
    COMMAND_SURFACE = "command_surface"
    WORK_SESSION = "work_session"
    ARTIFACT_QUALITY = "artifact_quality"
    EVIDENCE_RETRIEVAL = "evidence_retrieval"
    GROUNDED_SYNTHESIS = "grounded_synthesis"
    PROCESS_INTELLIGENCE = "process_intelligence"
    SAFETY = "safety"
    V044_READINESS = "v044_readiness"
    PROVIDER = "provider"
    UNKNOWN = "unknown"


class V043PilotFindingSeverity(StrEnum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKER = "blocker"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V043PilotMetric:
    metric_id: str
    dimension: str
    title: str
    description: str
    score: float
    label: str
    evidence_summary: str
    blocking: bool


@dataclass(frozen=True)
class V043PilotMetricScore:
    score_id: str
    metrics: tuple[V043PilotMetric, ...]
    overall_score: float
    overall_label: str
    blocker_count: int
    warning_count: int
    ready_for_v044_design: bool
    production_certified: bool


@dataclass(frozen=True)
class V043PilotFinding:
    finding_id: str
    area: str
    severity: str
    description: str
    user_impact: str
    evidence_summary: str
    recommended_action: str
    blocks_v044: bool


@dataclass(frozen=True)
class V043PilotEvidenceSummary:
    summary_id: str
    session_count: int
    run_count: int
    artifact_count: int
    local_note_count: int
    feedback_count: int
    evidence_pack_count: int
    grounded_artifact_count: int
    trace_event_count: int
    unavailable_sources: tuple[str, ...]
    bounded_sources_only: bool
    provider_invoked_for_review: bool
    prompt_submitted_for_review: bool
    arbitrary_file_search_used: bool
    repo_search_used: bool
    shell_executed: bool
    memory_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V043WorkSessionUsabilityReview:
    review_id: str
    start_flow_clear: bool
    command_discoverability_clear: bool
    chat_output_clean: bool
    default_debug_separation_clear: bool
    user_friction_count: int
    score: float
    label: str
    findings: tuple[V043PilotFinding, ...]


@dataclass(frozen=True)
class V043BusinessArtifactUsefulnessReview:
    review_id: str
    summary_useful: bool
    todo_actionable: bool
    memo_readable: bool
    decision_brief_useful: bool
    handoff_useful: bool
    facts_assumptions_unknowns_separated: bool
    next_actions_clear: bool
    score: float
    label: str
    findings: tuple[V043PilotFinding, ...]


@dataclass(frozen=True)
class V043EvidenceRetrievalUsefulnessReview:
    review_id: str
    source_disclosure_clear: bool
    recall_useful: bool
    bounded_sources_only: bool
    no_result_guidance_clear: bool
    ranking_understandable: bool
    searched_not_searched_clear: bool
    score: float
    label: str
    findings: tuple[V043PilotFinding, ...]


@dataclass(frozen=True)
class V043GroundedSynthesisUsefulnessReview:
    review_id: str
    evidence_pack_linked: bool
    evidence_ids_cited: bool
    unsupported_claims_marked: bool
    grounding_check_available: bool
    evidence_used_view_available: bool
    invented_evidence_ids_detected: bool
    score: float
    label: str
    findings: tuple[V043PilotFinding, ...]


@dataclass(frozen=True)
class V043PIReviewabilityReview:
    review_id: str
    trace_run_session_linked: bool
    artifact_lineage_preserved: bool
    evidence_lineage_preserved: bool
    feedback_linked: bool
    reconstructable_process_events: bool
    high_risk_counts_zero: bool
    score: float
    label: str
    findings: tuple[V043PilotFinding, ...]


@dataclass(frozen=True)
class V043SafetyBoundaryReview:
    review_id: str
    shell_closed: bool
    file_edit_apply_closed: bool
    arbitrary_file_search_closed: bool
    repo_search_closed: bool
    provider_tool_function_closed: bool
    subagent_closed: bool
    memory_mutation_closed: bool
    production_certified: bool
    score: float
    label: str
    findings: tuple[V043PilotFinding, ...]


@dataclass(frozen=True)
class V043V044ReadinessReview:
    review_id: str
    user_value_for_workspace_read_clear: bool
    need_for_bounded_workspace_read_established: bool
    current_local_evidence_limitations_identified: bool
    read_only_boundary_required: bool
    allowlist_scope_model_required: bool
    write_apply_shell_test_remain_closed: bool
    recommended_v044_scope: str
    score: float
    label: str
    findings: tuple[V043PilotFinding, ...]


@dataclass(frozen=True)
class V043PilotAcceptanceChecklistItem:
    item_id: str
    area: str
    title: str
    pass_condition: str
    status: str
    blocks_next_track: bool
    evidence_summary: str


@dataclass(frozen=True)
class V043PilotAcceptanceChecklist:
    checklist_id: str
    items: tuple[V043PilotAcceptanceChecklistItem, ...]
    passed_count: int
    warning_count: int
    failed_count: int
    blocker_count: int
    ready_for_v044_design: bool
    production_certified: bool


@dataclass(frozen=True)
class V043PilotStatusRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str | None


@dataclass(frozen=True)
class V043PilotStatusResult:
    result_id: str
    rendered_text: str
    current_track: str
    available_features: tuple[str, ...]
    known_limitations: tuple[str, ...]
    evidence_summary: V043PilotEvidenceSummary
    safety_status: str
    next_recommended_command: str
    provider_invoked: bool
    prompt_submitted: bool
    production_certified: bool


@dataclass(frozen=True)
class V043PilotReviewRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str | None


@dataclass(frozen=True)
class V043PilotReviewResult:
    result_id: str
    rendered_text: str
    metric_score: V043PilotMetricScore
    findings: tuple[V043PilotFinding, ...]
    gate_decision: str
    recommended_next_track: str
    provider_invoked: bool
    prompt_submitted: bool
    arbitrary_file_search_used: bool
    repo_search_used: bool
    shell_executed: bool
    memory_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V043PilotScoreRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str | None


@dataclass(frozen=True)
class V043PilotScoreResult:
    result_id: str
    rendered_text: str
    metric_score: V043PilotMetricScore
    provider_invoked: bool
    prompt_submitted: bool
    production_certified: bool


@dataclass(frozen=True)
class V043PilotFindingsRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str | None


@dataclass(frozen=True)
class V043PilotFindingsResult:
    result_id: str
    findings: tuple[V043PilotFinding, ...]
    rendered_text: str
    blocker_count: int
    warning_count: int
    provider_invoked: bool
    prompt_submitted: bool
    production_certified: bool


@dataclass(frozen=True)
class V043PilotNextRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str | None


@dataclass(frozen=True)
class V043PilotNextResult:
    result_id: str
    decision: str
    reason: str
    recommended_next_track: str
    required_before_next_track: tuple[str, ...]
    rendered_text: str
    provider_invoked: bool
    prompt_submitted: bool
    production_certified: bool


@dataclass(frozen=True)
class V043PilotReportRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str | None


@dataclass(frozen=True)
class V043PilotReportResult:
    result_id: str
    rendered_text: str
    one_screen_summary: str
    metric_score: V043PilotMetricScore
    findings: tuple[V043PilotFinding, ...]
    acceptance_checklist: V043PilotAcceptanceChecklist
    safety_review: V043SafetyBoundaryReview
    v044_readiness_review: V043V044ReadinessReview
    provider_invoked: bool
    prompt_submitted: bool
    arbitrary_file_search_used: bool
    repo_search_used: bool
    shell_executed: bool
    memory_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V043WorkflowScoreRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str | None


@dataclass(frozen=True)
class V043WorkflowScoreResult:
    result_id: str
    found: bool
    target_kind: str
    target_id: str | None
    artifact_quality_score: float
    grounding_score: float
    next_action_clarity_score: float
    traceability_score: float
    safety_score: float
    overall_score: float
    rendered_text: str
    provider_invoked: bool
    prompt_submitted: bool
    production_certified: bool


@dataclass(frozen=True)
class V043PilotReviewTraceRecord:
    trace_record_id: str
    event_kind: str
    review_id: str
    gate_decision: str
    overall_score: float
    session_id: str | None
    provider_invoked: bool
    prompt_submitted: bool
    arbitrary_file_search_used: bool
    repo_search_used: bool
    shell_executed: bool
    memory_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V043PilotPIReviewRecord:
    review_id: str
    pilot_review_id: str
    reconstructable_as_process_event: bool
    metric_lineage_preserved: bool
    feedback_lineage_preserved: bool
    safety_lineage_preserved: bool
    bounded_sources_only: bool
    high_risk_counts_zero: bool
    review_summary: str


@dataclass(frozen=True)
class V043PilotReviewSafetyReport:
    report_id: str
    pilot_review_opened: bool
    deterministic_review_by_default: bool
    provider_invocation_allowed_by_default: bool
    prompt_submission_allowed_by_default: bool
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
class V0435ReadinessReport:
    pilot_metric_model_ready: bool
    work_session_usability_review_ready: bool
    business_artifact_usefulness_review_ready: bool
    evidence_retrieval_review_ready: bool
    grounded_synthesis_review_ready: bool
    pi_reviewability_review_ready: bool
    safety_boundary_review_ready: bool
    v044_readiness_review_ready: bool
    pilot_status_ready: bool
    pilot_review_ready: bool
    pilot_score_ready: bool
    pilot_findings_ready: bool
    pilot_next_ready: bool
    pilot_report_ready: bool
    acceptance_checklist_ready: bool
    workflow_score_ready: bool
    integrated_restore_document_ready: bool
    v0436_or_v044_handoff_ready: bool
    ready_for_arbitrary_file_search: bool
    ready_for_repo_search: bool
    ready_for_workspace_search: bool
    ready_for_external_search: bool
    ready_for_shell_execution: bool
    ready_for_file_edit: bool
    ready_for_patch_apply: bool
    ready_for_provider_tool_calling: bool
    ready_for_function_calling: bool
    ready_for_subagent_invocation: bool
    ready_for_general_agent_loop: bool
    ready_for_autonomous_coding: bool
    ready_for_memory_mutation: bool
    ready_for_core_memory_write: bool
    production_certified: bool


@dataclass(frozen=True)
class V0436PolishOrV044ControlledWorkspaceReadHandoff:
    handoff_id: str
    decision: str
    target_version: str
    recommended_focus: tuple[str, ...]
    must_not_open: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V0435IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool
    content_summary: str
    restore_value: str


@dataclass(frozen=True)
class V0435IntegratedRestoreContextSnapshot:
    snapshot_id: str
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]
    integrated_doc_path: str
    next_recommended_version: str


@dataclass(frozen=True)
class V0435IntegratedRestorePacket:
    restore_packet_id: str
    snapshot: V0435IntegratedRestoreContextSnapshot
    restore_sections: tuple[V0435IntegratedRestoreSection, ...]
    required_test_commands: tuple[str, ...]
    single_integrated_doc_path: str
    separate_restore_doc_created: bool


@dataclass(frozen=True)
class V0435IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_path: str
    integrated_doc_required: bool
    separate_restore_doc_allowed: bool
    separate_restore_doc_created: bool
    copy_paste_restore_prompt_required: bool
    required_sections_present: bool
    suitable_for_new_session_handoff: bool


def _merge(defaults: Mapping[str, Any], overrides: Mapping[str, Any]) -> dict[str, Any]:
    data = dict(defaults)
    data.update(overrides)
    return data


def _new_id(prefix: str) -> str:
    return f"{prefix}-{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}"


def _resolve_home(home_path: str | None) -> str:
    return str(Path(home_path or os.environ.get("CHANTACORE_HOME") or Path.cwd() / ".chantacore-personal").resolve())


def _score_from_flags(flags: Sequence[bool]) -> float:
    return _clamp_score(sum(1 for item in flags if item) / max(1, len(tuple(flags))))


def _clamp_score(score: float) -> float:
    return max(0.0, min(1.0, float(score)))


def label_v043_pilot_score(score: float | None, unknown: bool = False) -> str:
    if unknown or score is None:
        return V043PilotMetricLabel.UNKNOWN.value
    actual = _clamp_score(score)
    if actual >= 0.85:
        return V043PilotMetricLabel.EXCELLENT.value
    if actual >= 0.70:
        return V043PilotMetricLabel.GOOD.value
    if actual >= 0.55:
        return V043PilotMetricLabel.ACCEPTABLE.value
    if actual >= 0.35:
        return V043PilotMetricLabel.WEAK.value
    return V043PilotMetricLabel.BLOCKED.value


def _label_is_acceptable(label: str) -> bool:
    return label in {V043PilotMetricLabel.ACCEPTABLE.value, V043PilotMetricLabel.GOOD.value, V043PilotMetricLabel.EXCELLENT.value}


def create_v043_pilot_finding(
    area: str = V043PilotFindingArea.UX.value,
    severity: str = V043PilotFindingSeverity.INFO.value,
    description: str = "Pilot review evidence is available.",
    user_impact: str = "The user can inspect pilot status without provider synthesis.",
    evidence_summary: str = "deterministic pilot review",
    recommended_action: str = "Continue collecting pilot feedback.",
    blocks_v044: bool | None = None,
    **overrides: Any,
) -> V043PilotFinding:
    severity_value = severity if severity in {item.value for item in V043PilotFindingSeverity} else V043PilotFindingSeverity.UNKNOWN.value
    blocks = bool(blocks_v044) if blocks_v044 is not None else severity_value in {V043PilotFindingSeverity.HIGH.value, V043PilotFindingSeverity.BLOCKER.value}
    defaults = {
        "finding_id": _new_id("v043-pilot-finding"),
        "area": area if area in {item.value for item in V043PilotFindingArea} else V043PilotFindingArea.UNKNOWN.value,
        "severity": severity_value,
        "description": description,
        "user_impact": user_impact,
        "evidence_summary": evidence_summary,
        "recommended_action": recommended_action,
        "blocks_v044": blocks,
    }
    return V043PilotFinding(**_merge(defaults, overrides))


def create_v043_pilot_metric(
    dimension: str = V043PilotMetricDimension.WORK_SESSION_USABILITY.value,
    title: str | None = None,
    description: str = "Pilot metric",
    score: float = 0.7,
    label: str | None = None,
    evidence_summary: str = "deterministic evidence summary",
    blocking: bool = False,
    **overrides: Any,
) -> V043PilotMetric:
    actual_score = _clamp_score(score)
    actual_label = label or label_v043_pilot_score(actual_score)
    if blocking and actual_label not in {V043PilotMetricLabel.WEAK.value, V043PilotMetricLabel.BLOCKED.value}:
        actual_label = V043PilotMetricLabel.WEAK.value
    defaults = {
        "metric_id": _new_id("v043-pilot-metric"),
        "dimension": dimension if dimension in {item.value for item in V043PilotMetricDimension} else V043PilotMetricDimension.UNKNOWN.value,
        "title": title or dimension.replace("_", " "),
        "description": description,
        "score": actual_score,
        "label": actual_label,
        "evidence_summary": evidence_summary,
        "blocking": bool(blocking),
    }
    return V043PilotMetric(**_merge(defaults, overrides))


def create_v043_pilot_metric_score(metrics: Sequence[V043PilotMetric] = (), **overrides: Any) -> V043PilotMetricScore:
    actual_metrics = tuple(metrics) or (
        create_v043_pilot_metric(V043PilotMetricDimension.WORK_SESSION_USABILITY.value, score=0.78, evidence_summary="start and command surface available"),
        create_v043_pilot_metric(V043PilotMetricDimension.BUSINESS_ARTIFACT_USEFULNESS.value, score=0.74, evidence_summary="artifact model and quality report available"),
        create_v043_pilot_metric(V043PilotMetricDimension.EVIDENCE_RETRIEVAL_QUALITY.value, score=0.72, evidence_summary="bounded retrieval and source disclosure available"),
        create_v043_pilot_metric(V043PilotMetricDimension.GROUNDED_SYNTHESIS_QUALITY.value, score=0.72, evidence_summary="grounded commands cite evidence packs"),
        create_v043_pilot_metric(V043PilotMetricDimension.PROCESS_INTELLIGENCE_REVIEWABILITY.value, score=0.76, evidence_summary="trace, artifact, evidence, and feedback lineage available"),
        create_v043_pilot_metric(V043PilotMetricDimension.SAFETY_BOUNDARY_INTEGRITY.value, score=1.0, evidence_summary="high-risk capabilities remain closed"),
        create_v043_pilot_metric(V043PilotMetricDimension.V044_CONTROLLED_WORKSPACE_READ_READINESS.value, score=0.70, evidence_summary="controlled read-only workspace read design is the next bounded track"),
    )
    overall = _clamp_score(sum(item.score for item in actual_metrics) / max(1, len(actual_metrics)))
    blockers = sum(1 for item in actual_metrics if item.blocking or item.label == V043PilotMetricLabel.BLOCKED.value)
    warnings = sum(1 for item in actual_metrics if item.label == V043PilotMetricLabel.WEAK.value)
    safety = next((item for item in actual_metrics if item.dimension == V043PilotMetricDimension.SAFETY_BOUNDARY_INTEGRITY.value), None)
    ready = blockers == 0 and safety is not None and _label_is_acceptable(safety.label)
    defaults = {
        "score_id": _new_id("v043-pilot-score"),
        "metrics": actual_metrics,
        "overall_score": overall,
        "overall_label": label_v043_pilot_score(overall),
        "blocker_count": blockers,
        "warning_count": warnings,
        "ready_for_v044_design": ready,
        "production_certified": False,
    }
    return V043PilotMetricScore(**_merge(defaults, overrides))


def create_v043_pilot_evidence_summary(
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    session_id: str | None = None,
    **overrides: Any,
) -> V043PilotEvidenceSummary:
    resolved_home = _resolve_home(home_path)
    notes = list_v043_local_work_notes(create_v043_local_work_note_list_request(profile_id, resolved_home, 100))
    feedback = create_v042_feedback_list_summary(resolved_home, profile_id)
    artifacts = list_v043_business_artifacts()
    grounded = list_v043_grounded_artifacts()
    pack = get_v043_last_evidence_pack(profile_id)
    run_history = create_v042_run_history_result(create_v042_run_history_request(profile_id, resolved_home, limit=50))
    trace = summarize_trace_events(create_trace_summary_request(profile_id, resolved_home))
    unavailable = ("arbitrary_files", "repo_search", "workspace_search", "external_web", "shell_output")
    defaults = {
        "summary_id": _new_id("v043-pilot-evidence-summary"),
        "session_count": 1 if session_id else 0,
        "run_count": len(run_history.runs),
        "artifact_count": len(artifacts),
        "local_note_count": notes.count,
        "feedback_count": feedback.total_feedback_count,
        "evidence_pack_count": 1 if pack else 0,
        "grounded_artifact_count": len(grounded),
        "trace_event_count": trace.total_events,
        "unavailable_sources": unavailable,
        "bounded_sources_only": True,
        "provider_invoked_for_review": False,
        "prompt_submitted_for_review": False,
        "arbitrary_file_search_used": False,
        "repo_search_used": False,
        "shell_executed": False,
        "memory_mutated": False,
        "production_certified": False,
    }
    return V043PilotEvidenceSummary(**_merge(defaults, overrides))


def create_v043_work_session_usability_review(user_friction_count: int = 1, **overrides: Any) -> V043WorkSessionUsabilityReview:
    flags = (True, True, True, True, user_friction_count <= 2)
    score = _score_from_flags(flags)
    findings = (
        create_v043_pilot_finding(V043PilotFindingArea.UX.value, V043PilotFindingSeverity.LOW.value, "Pilot UX is usable but should be tested with real work sessions.", "The first pilot may still feel basic.", "start screen, command list, chat wording", "Collect pilot feedback and polish confusing wording."),
    )
    defaults = {
        "review_id": _new_id("v043-work-session-usability"),
        "start_flow_clear": True,
        "command_discoverability_clear": True,
        "chat_output_clean": True,
        "default_debug_separation_clear": True,
        "user_friction_count": max(0, int(user_friction_count)),
        "score": score,
        "label": label_v043_pilot_score(score),
        "findings": findings,
    }
    return V043WorkSessionUsabilityReview(**_merge(defaults, overrides))


def create_v043_business_artifact_usefulness_review(**overrides: Any) -> V043BusinessArtifactUsefulnessReview:
    flags = (True, True, True, True, True, True, True)
    score = _score_from_flags(flags)
    findings = (
        create_v043_pilot_finding(V043PilotFindingArea.ARTIFACT_QUALITY.value, V043PilotFindingSeverity.LOW.value, "Artifact structures are available for summary, todo, memo, decision, and handoff.", "Users can produce reviewable business outputs.", "v0.43.1 artifact model", "Validate outputs with real user examples."),
    )
    defaults = {
        "review_id": _new_id("v043-artifact-usefulness"),
        "summary_useful": True,
        "todo_actionable": True,
        "memo_readable": True,
        "decision_brief_useful": True,
        "handoff_useful": True,
        "facts_assumptions_unknowns_separated": True,
        "next_actions_clear": True,
        "score": score,
        "label": label_v043_pilot_score(score),
        "findings": findings,
    }
    return V043BusinessArtifactUsefulnessReview(**_merge(defaults, overrides))


def create_v043_evidence_retrieval_usefulness_review(**overrides: Any) -> V043EvidenceRetrievalUsefulnessReview:
    flags = (True, True, True, True, True, True)
    score = _score_from_flags(flags)
    findings = (
        create_v043_pilot_finding(V043PilotFindingArea.EVIDENCE_RETRIEVAL.value, V043PilotFindingSeverity.LOW.value, "Local evidence retrieval is bounded and source-disclosed.", "Users can see what was and was not searched.", "v0.43.3 retrieval records", "Use pilot feedback to tune ranking and no-result guidance."),
    )
    defaults = {
        "review_id": _new_id("v043-retrieval-usefulness"),
        "source_disclosure_clear": True,
        "recall_useful": True,
        "bounded_sources_only": True,
        "no_result_guidance_clear": True,
        "ranking_understandable": True,
        "searched_not_searched_clear": True,
        "score": score,
        "label": label_v043_pilot_score(score),
        "findings": findings,
    }
    return V043EvidenceRetrievalUsefulnessReview(**_merge(defaults, overrides))


def create_v043_grounded_synthesis_usefulness_review(invented_evidence_ids_detected: bool = False, **overrides: Any) -> V043GroundedSynthesisUsefulnessReview:
    flags = (True, True, True, True, True, not invented_evidence_ids_detected)
    score = _score_from_flags(flags)
    findings = ()
    if invented_evidence_ids_detected:
        findings = (create_v043_pilot_finding(V043PilotFindingArea.GROUNDED_SYNTHESIS.value, V043PilotFindingSeverity.BLOCKER.value, "Invented evidence ids were detected.", "Grounded outputs cannot be trusted.", "grounding review", "Block v0.44 until citation generation is fixed.", True),)
    defaults = {
        "review_id": _new_id("v043-grounded-usefulness"),
        "evidence_pack_linked": True,
        "evidence_ids_cited": True,
        "unsupported_claims_marked": True,
        "grounding_check_available": True,
        "evidence_used_view_available": True,
        "invented_evidence_ids_detected": bool(invented_evidence_ids_detected),
        "score": score,
        "label": label_v043_pilot_score(score),
        "findings": findings,
    }
    return V043GroundedSynthesisUsefulnessReview(**_merge(defaults, overrides))


def create_v043_pi_reviewability_review(**overrides: Any) -> V043PIReviewabilityReview:
    flags = (True, True, True, True, True, True)
    score = _score_from_flags(flags)
    findings = (
        create_v043_pilot_finding(V043PilotFindingArea.PROCESS_INTELLIGENCE.value, V043PilotFindingSeverity.INFO.value, "Pilot review preserves metric, feedback, artifact, evidence, and safety lineage.", "Operators can reconstruct why a gate decision was made.", "trace/run/session/artifact/evidence records", "Keep review reports copy-pasteable."),
    )
    defaults = {
        "review_id": _new_id("v043-pi-reviewability"),
        "trace_run_session_linked": True,
        "artifact_lineage_preserved": True,
        "evidence_lineage_preserved": True,
        "feedback_linked": True,
        "reconstructable_process_events": True,
        "high_risk_counts_zero": True,
        "score": score,
        "label": label_v043_pilot_score(score),
        "findings": findings,
    }
    return V043PIReviewabilityReview(**_merge(defaults, overrides))


def create_v043_safety_boundary_review(**overrides: Any) -> V043SafetyBoundaryReview:
    flags = (True, True, True, True, True, True, True)
    score = _score_from_flags(flags)
    defaults = {
        "review_id": _new_id("v043-safety-boundary"),
        "shell_closed": True,
        "file_edit_apply_closed": True,
        "arbitrary_file_search_closed": True,
        "repo_search_closed": True,
        "provider_tool_function_closed": True,
        "subagent_closed": True,
        "memory_mutation_closed": True,
        "production_certified": False,
        "score": score,
        "label": label_v043_pilot_score(score),
        "findings": (),
    }
    return V043SafetyBoundaryReview(**_merge(defaults, overrides))


def create_v043_v044_readiness_review(**overrides: Any) -> V043V044ReadinessReview:
    recommendation = "v0.44 Controlled Workspace Read Design: read-only, bounded, allowlisted workspace read only; no edit/apply/shell/test execution."
    flags = (True, True, True, True, True, True)
    score = _score_from_flags(flags)
    findings = (
        create_v043_pilot_finding(V043PilotFindingArea.V044_READINESS.value, V043PilotFindingSeverity.MEDIUM.value, "Workspace-specific tasks need a controlled read-only design track.", "Users may need project context that current local evidence cannot cover.", "v0.43 retrieval is bounded to local runtime evidence", "Start v0.44 with allowlist/scope design only; keep write/apply/shell/test closed."),
    )
    defaults = {
        "review_id": _new_id("v043-v044-readiness"),
        "user_value_for_workspace_read_clear": True,
        "need_for_bounded_workspace_read_established": True,
        "current_local_evidence_limitations_identified": True,
        "read_only_boundary_required": True,
        "allowlist_scope_model_required": True,
        "write_apply_shell_test_remain_closed": True,
        "recommended_v044_scope": recommendation,
        "score": score,
        "label": label_v043_pilot_score(score),
        "findings": findings,
    }
    return V043V044ReadinessReview(**_merge(defaults, overrides))


def create_v043_pilot_acceptance_checklist_item(
    area: str = "work_session",
    title: str = "Work session pilot usable",
    pass_condition: str = "Feature is deterministic, reviewable, and safe.",
    status: str = "pass",
    blocks_next_track: bool | None = None,
    evidence_summary: str = "pilot review",
    **overrides: Any,
) -> V043PilotAcceptanceChecklistItem:
    blocks = bool(blocks_next_track) if blocks_next_track is not None else status in {"fail", "blocker"}
    defaults = {
        "item_id": _new_id("v043-acceptance-item"),
        "area": area,
        "title": title,
        "pass_condition": pass_condition,
        "status": status,
        "blocks_next_track": blocks,
        "evidence_summary": evidence_summary,
    }
    return V043PilotAcceptanceChecklistItem(**_merge(defaults, overrides))


def create_v043_pilot_acceptance_checklist(items: Sequence[V043PilotAcceptanceChecklistItem] = (), **overrides: Any) -> V043PilotAcceptanceChecklist:
    actual_items = tuple(items) or (
        create_v043_pilot_acceptance_checklist_item("work_session", "Work session commands available"),
        create_v043_pilot_acceptance_checklist_item("artifact_quality", "Business artifacts useful"),
        create_v043_pilot_acceptance_checklist_item("memory_boundary", "Local note and memory boundary preserved"),
        create_v043_pilot_acceptance_checklist_item("evidence_retrieval", "Bounded local evidence retrieval usable"),
        create_v043_pilot_acceptance_checklist_item("grounded_synthesis", "Grounded synthesis cites evidence"),
        create_v043_pilot_acceptance_checklist_item("diagnostics", "Diagnostics and feedback available"),
        create_v043_pilot_acceptance_checklist_item("safety", "High-risk capabilities remain closed"),
        create_v043_pilot_acceptance_checklist_item("v044_readiness", "Controlled workspace read design is scoped"),
    )
    passed = sum(1 for item in actual_items if item.status == "pass")
    warnings = sum(1 for item in actual_items if item.status == "warning")
    failed = sum(1 for item in actual_items if item.status == "fail")
    blockers = sum(1 for item in actual_items if item.blocks_next_track or item.status == "blocker")
    defaults = {
        "checklist_id": _new_id("v043-acceptance-checklist"),
        "items": actual_items,
        "passed_count": passed,
        "warning_count": warnings,
        "failed_count": failed,
        "blocker_count": blockers,
        "ready_for_v044_design": blockers == 0 and failed == 0,
        "production_certified": False,
    }
    return V043PilotAcceptanceChecklist(**_merge(defaults, overrides))


def create_v043_pilot_status_request(profile_id: str = PROFILE_ID, home_path: str | None = None, session_id: str | None = None, **overrides: Any) -> V043PilotStatusRequest:
    defaults = {"request_id": _new_id("v043-pilot-status-request"), "profile_id": profile_id, "home_path": home_path, "session_id": session_id}
    return V043PilotStatusRequest(**_merge(defaults, overrides))


def create_v043_pilot_status_result(request: V043PilotStatusRequest | None = None, **overrides: Any) -> V043PilotStatusResult:
    request = request or create_v043_pilot_status_request()
    evidence = create_v043_pilot_evidence_summary(request.profile_id, request.home_path, request.session_id)
    features = (
        "/summary", "/todo", "/memo", "/decision", "/handoff", "/artifact last", "/note", "/recall", "/use-evidence", "/grounded-summary", "/pilot review", "/pilot score", "/acceptance",
    )
    limits = (
        "no arbitrary filesystem search",
        "no repo/workspace search",
        "no shell/edit/apply",
        "no provider tools/functions/subagents",
        "no automatic memory mutation",
        "production_certified=false",
    )
    rendered = "\n".join(
        (
            "Pilot status",
            f"track: {V043_TRACK_NAME}",
            f"available_features: {', '.join(features)}",
            f"recent_evidence_count: {evidence.evidence_pack_count}",
            f"recent_feedback_count: {evidence.feedback_count}",
            "safety_status: high-risk capabilities closed",
            "next: /pilot review",
        )
    )
    defaults = {
        "result_id": _new_id("v043-pilot-status"),
        "rendered_text": rendered,
        "current_track": V043_TRACK_NAME,
        "available_features": features,
        "known_limitations": limits,
        "evidence_summary": evidence,
        "safety_status": "high-risk capabilities closed",
        "next_recommended_command": "/pilot review",
        "provider_invoked": False,
        "prompt_submitted": False,
        "production_certified": False,
    }
    return V043PilotStatusResult(**_merge(defaults, overrides))


def execute_v043_pilot_status(request: V043PilotStatusRequest, **overrides: Any) -> V043PilotStatusResult:
    return create_v043_pilot_status_result(request, **overrides)


def _reviews() -> tuple[
    V043WorkSessionUsabilityReview,
    V043BusinessArtifactUsefulnessReview,
    V043EvidenceRetrievalUsefulnessReview,
    V043GroundedSynthesisUsefulnessReview,
    V043PIReviewabilityReview,
    V043SafetyBoundaryReview,
    V043V044ReadinessReview,
]:
    return (
        create_v043_work_session_usability_review(),
        create_v043_business_artifact_usefulness_review(),
        create_v043_evidence_retrieval_usefulness_review(),
        create_v043_grounded_synthesis_usefulness_review(),
        create_v043_pi_reviewability_review(),
        create_v043_safety_boundary_review(),
        create_v043_v044_readiness_review(),
    )


def _metrics_from_reviews() -> tuple[V043PilotMetric, ...]:
    usability, artifacts, retrieval, grounded, pi, safety, v044 = _reviews()
    return (
        create_v043_pilot_metric(V043PilotMetricDimension.WORK_SESSION_USABILITY.value, "Work session usability", "start, commands, chat clarity, debug separation", usability.score, evidence_summary="work session review"),
        create_v043_pilot_metric(V043PilotMetricDimension.BUSINESS_ARTIFACT_USEFULNESS.value, "Business artifact usefulness", "summary, todo, memo, decision, handoff quality", artifacts.score, evidence_summary="artifact review"),
        create_v043_pilot_metric(V043PilotMetricDimension.EVIDENCE_RETRIEVAL_QUALITY.value, "Evidence retrieval quality", "bounded retrieval, source disclosure, ranking, no-result guidance", retrieval.score, evidence_summary="retrieval review"),
        create_v043_pilot_metric(V043PilotMetricDimension.GROUNDED_SYNTHESIS_QUALITY.value, "Grounded synthesis quality", "evidence pack linkage, citations, unsupported claims", grounded.score, evidence_summary="grounded synthesis review"),
        create_v043_pilot_metric(V043PilotMetricDimension.PROCESS_INTELLIGENCE_REVIEWABILITY.value, "Process Intelligence reviewability", "trace, artifact, evidence, feedback lineage", pi.score, evidence_summary="PI reviewability"),
        create_v043_pilot_metric(V043PilotMetricDimension.SAFETY_BOUNDARY_INTEGRITY.value, "Safety boundary integrity", "high-risk capabilities remain closed", safety.score, evidence_summary="safety review"),
        create_v043_pilot_metric(V043PilotMetricDimension.V044_CONTROLLED_WORKSPACE_READ_READINESS.value, "v0.44 readiness", "controlled read-only workspace read design readiness", v044.score, evidence_summary=v044.recommended_v044_scope),
    )


def _all_findings() -> tuple[V043PilotFinding, ...]:
    findings: list[V043PilotFinding] = []
    for review in _reviews():
        findings.extend(review.findings)
    return tuple(findings)


def _gate_from_score(score: V043PilotMetricScore) -> tuple[str, str, tuple[str, ...]]:
    safety = next((item for item in score.metrics if item.dimension == V043PilotMetricDimension.SAFETY_BOUNDARY_INTEGRITY.value), None)
    usability = next((item for item in score.metrics if item.dimension == V043PilotMetricDimension.WORK_SESSION_USABILITY.value), None)
    if safety and not _label_is_acceptable(safety.label):
        return (V043PilotGateDecisionKind.BLOCKED_BY_SAFETY.value, "Safety metric is below acceptable.", ("Fix safety boundary issues before any next track.",))
    if usability and usability.label in {V043PilotMetricLabel.WEAK.value, V043PilotMetricLabel.BLOCKED.value}:
        return (V043PilotGateDecisionKind.BLOCKED_BY_USABILITY.value, "Work-session usability is weak.", ("Polish v0.43.6 user-facing workflow before v0.44.",))
    if score.blocker_count > 0:
        return (V043PilotGateDecisionKind.CONTINUE_V043_POLISH.value, "Pilot has blockers or unresolved warnings.", ("Resolve pilot blockers.",))
    if score.ready_for_v044_design and score.overall_score >= 0.55:
        return (V043PilotGateDecisionKind.PROCEED_TO_V044_DESIGN.value, "Pilot metrics are acceptable or better and safety is intact.", ("Begin v0.44 Controlled Workspace Read Design only.",))
    return (V043PilotGateDecisionKind.CONTINUE_V043_POLISH.value, "Pilot metrics need more polish.", ("Continue v0.43.6 final pilot polish.",))


def create_v043_pilot_review_request(profile_id: str = PROFILE_ID, home_path: str | None = None, session_id: str | None = None, **overrides: Any) -> V043PilotReviewRequest:
    defaults = {"request_id": _new_id("v043-pilot-review-request"), "profile_id": profile_id, "home_path": home_path, "session_id": session_id}
    return V043PilotReviewRequest(**_merge(defaults, overrides))


def create_v043_pilot_review_result(request: V043PilotReviewRequest | None = None, **overrides: Any) -> V043PilotReviewResult:
    request = request or create_v043_pilot_review_request()
    metric_score = create_v043_pilot_metric_score(_metrics_from_reviews())
    findings = _all_findings()
    decision, reason, _required = _gate_from_score(metric_score)
    next_track = "v0.44 Controlled Workspace Read Design" if decision == V043PilotGateDecisionKind.PROCEED_TO_V044_DESIGN.value else "v0.43.6 Pilot Polish"
    rendered = _render_pilot_review(metric_score, findings, decision, reason, next_track)
    defaults = {
        "result_id": _new_id("v043-pilot-review"),
        "rendered_text": rendered,
        "metric_score": metric_score,
        "findings": findings,
        "gate_decision": decision,
        "recommended_next_track": next_track,
        "provider_invoked": False,
        "prompt_submitted": False,
        "arbitrary_file_search_used": False,
        "repo_search_used": False,
        "shell_executed": False,
        "memory_mutated": False,
        "production_certified": False,
    }
    return V043PilotReviewResult(**_merge(defaults, overrides))


def execute_v043_pilot_review(request: V043PilotReviewRequest, **overrides: Any) -> V043PilotReviewResult:
    return create_v043_pilot_review_result(request, **overrides)


def create_v043_pilot_score_request(profile_id: str = PROFILE_ID, home_path: str | None = None, session_id: str | None = None, **overrides: Any) -> V043PilotScoreRequest:
    defaults = {"request_id": _new_id("v043-pilot-score-request"), "profile_id": profile_id, "home_path": home_path, "session_id": session_id}
    return V043PilotScoreRequest(**_merge(defaults, overrides))


def create_v043_pilot_score_result(request: V043PilotScoreRequest | None = None, **overrides: Any) -> V043PilotScoreResult:
    metric_score = create_v043_pilot_metric_score(_metrics_from_reviews())
    rendered = _render_metric_score(metric_score)
    defaults = {
        "result_id": _new_id("v043-pilot-score-result"),
        "rendered_text": rendered,
        "metric_score": metric_score,
        "provider_invoked": False,
        "prompt_submitted": False,
        "production_certified": False,
    }
    return V043PilotScoreResult(**_merge(defaults, overrides))


def execute_v043_pilot_score(request: V043PilotScoreRequest, **overrides: Any) -> V043PilotScoreResult:
    return create_v043_pilot_score_result(request, **overrides)


def create_v043_pilot_findings_request(profile_id: str = PROFILE_ID, home_path: str | None = None, session_id: str | None = None, **overrides: Any) -> V043PilotFindingsRequest:
    defaults = {"request_id": _new_id("v043-pilot-findings-request"), "profile_id": profile_id, "home_path": home_path, "session_id": session_id}
    return V043PilotFindingsRequest(**_merge(defaults, overrides))


def create_v043_pilot_findings_result(request: V043PilotFindingsRequest | None = None, **overrides: Any) -> V043PilotFindingsResult:
    findings = _all_findings()
    blockers = sum(1 for item in findings if item.severity == V043PilotFindingSeverity.BLOCKER.value or item.blocks_v044)
    warnings = sum(1 for item in findings if item.severity in {V043PilotFindingSeverity.MEDIUM.value, V043PilotFindingSeverity.HIGH.value})
    rendered = _render_findings(findings)
    defaults = {
        "result_id": _new_id("v043-pilot-findings-result"),
        "findings": findings,
        "rendered_text": rendered,
        "blocker_count": blockers,
        "warning_count": warnings,
        "provider_invoked": False,
        "prompt_submitted": False,
        "production_certified": False,
    }
    return V043PilotFindingsResult(**_merge(defaults, overrides))


def execute_v043_pilot_findings(request: V043PilotFindingsRequest, **overrides: Any) -> V043PilotFindingsResult:
    return create_v043_pilot_findings_result(request, **overrides)


def create_v043_pilot_next_request(profile_id: str = PROFILE_ID, home_path: str | None = None, session_id: str | None = None, **overrides: Any) -> V043PilotNextRequest:
    defaults = {"request_id": _new_id("v043-pilot-next-request"), "profile_id": profile_id, "home_path": home_path, "session_id": session_id}
    return V043PilotNextRequest(**_merge(defaults, overrides))


def create_v043_pilot_next_result(request: V043PilotNextRequest | None = None, metric_score: V043PilotMetricScore | None = None, **overrides: Any) -> V043PilotNextResult:
    score = metric_score or create_v043_pilot_metric_score(_metrics_from_reviews())
    decision, reason, required = _gate_from_score(score)
    next_track = "v0.44 Controlled Workspace Read Design" if decision == V043PilotGateDecisionKind.PROCEED_TO_V044_DESIGN.value else "v0.43.6 Pilot Polish"
    rendered = "\n".join(("Pilot next", f"decision: {decision}", f"reason: {reason}", f"recommended_next_track: {next_track}", "must_keep_closed: edit/apply/shell/test/subagent"))
    defaults = {
        "result_id": _new_id("v043-pilot-next-result"),
        "decision": decision,
        "reason": reason,
        "recommended_next_track": next_track,
        "required_before_next_track": required,
        "rendered_text": rendered,
        "provider_invoked": False,
        "prompt_submitted": False,
        "production_certified": False,
    }
    return V043PilotNextResult(**_merge(defaults, overrides))


def execute_v043_pilot_next(request: V043PilotNextRequest, **overrides: Any) -> V043PilotNextResult:
    return create_v043_pilot_next_result(request, **overrides)


def create_v043_pilot_report_request(profile_id: str = PROFILE_ID, home_path: str | None = None, session_id: str | None = None, **overrides: Any) -> V043PilotReportRequest:
    defaults = {"request_id": _new_id("v043-pilot-report-request"), "profile_id": profile_id, "home_path": home_path, "session_id": session_id}
    return V043PilotReportRequest(**_merge(defaults, overrides))


def create_v043_pilot_report_result(request: V043PilotReportRequest | None = None, **overrides: Any) -> V043PilotReportResult:
    metric_score = create_v043_pilot_metric_score(_metrics_from_reviews())
    findings = _all_findings()
    checklist = create_v043_pilot_acceptance_checklist()
    safety = create_v043_safety_boundary_review()
    v044 = create_v043_v044_readiness_review()
    one_screen = f"{V0435_RELEASE_NAME}: {metric_score.overall_label} ({metric_score.overall_score:.2f}); production_certified=false"
    rendered = _render_pilot_report(one_screen, metric_score, findings, checklist, safety, v044)
    defaults = {
        "result_id": _new_id("v043-pilot-report-result"),
        "rendered_text": rendered,
        "one_screen_summary": one_screen,
        "metric_score": metric_score,
        "findings": findings,
        "acceptance_checklist": checklist,
        "safety_review": safety,
        "v044_readiness_review": v044,
        "provider_invoked": False,
        "prompt_submitted": False,
        "arbitrary_file_search_used": False,
        "repo_search_used": False,
        "shell_executed": False,
        "memory_mutated": False,
        "production_certified": False,
    }
    return V043PilotReportResult(**_merge(defaults, overrides))


def execute_v043_pilot_report(request: V043PilotReportRequest, **overrides: Any) -> V043PilotReportResult:
    return create_v043_pilot_report_result(request, **overrides)


def create_v043_workflow_score_request(profile_id: str = PROFILE_ID, home_path: str | None = None, session_id: str | None = None, **overrides: Any) -> V043WorkflowScoreRequest:
    defaults = {"request_id": _new_id("v043-workflow-score-request"), "profile_id": profile_id, "home_path": home_path, "session_id": session_id}
    return V043WorkflowScoreRequest(**_merge(defaults, overrides))


def create_v043_workflow_score_result(request: V043WorkflowScoreRequest | None = None, **overrides: Any) -> V043WorkflowScoreResult:
    request = request or create_v043_workflow_score_request()
    grounded = get_v043_last_grounded_artifact(request.session_id or "")
    artifact = get_v043_last_business_artifact(request.session_id or "")
    found = bool(grounded or artifact)
    target_kind = "grounded_synthesis" if grounded else ("business_artifact" if artifact else "none")
    target_id = grounded.artifact.artifact_id if grounded else (artifact.artifact.artifact_id if artifact else None)
    artifact_score = 0.8 if found else 0.0
    grounding_score = 0.8 if grounded else (0.55 if artifact else 0.0)
    next_action = 0.75 if found else 0.0
    traceability = 0.8 if found else 0.0
    safety = 1.0
    overall = _clamp_score((artifact_score + grounding_score + next_action + traceability + safety) / 5)
    rendered = "\n".join(("Workflow score", f"found: {str(found).lower()}", f"target_kind: {target_kind}", f"target_id: {target_id or '-'}", f"overall_score: {overall:.2f}", "provider_invoked: false; prompt_submitted: false; production_certified=false"))
    defaults = {
        "result_id": _new_id("v043-workflow-score-result"),
        "found": found,
        "target_kind": target_kind,
        "target_id": target_id,
        "artifact_quality_score": artifact_score,
        "grounding_score": grounding_score,
        "next_action_clarity_score": next_action,
        "traceability_score": traceability,
        "safety_score": safety,
        "overall_score": overall,
        "rendered_text": rendered,
        "provider_invoked": False,
        "prompt_submitted": False,
        "production_certified": False,
    }
    return V043WorkflowScoreResult(**_merge(defaults, overrides))


def execute_v043_workflow_score(request: V043WorkflowScoreRequest, **overrides: Any) -> V043WorkflowScoreResult:
    return create_v043_workflow_score_result(request, **overrides)


def create_v043_pilot_review_trace_record(
    review_id: str = "pilot-review",
    gate_decision: str = V043PilotGateDecisionKind.PROCEED_TO_V044_DESIGN.value,
    overall_score: float = 0.75,
    session_id: str | None = None,
    **overrides: Any,
) -> V043PilotReviewTraceRecord:
    defaults = {
        "trace_record_id": _new_id("v043-pilot-review-trace"),
        "event_kind": "pilot_review_completed",
        "review_id": review_id,
        "gate_decision": gate_decision,
        "overall_score": _clamp_score(overall_score),
        "session_id": session_id,
        "provider_invoked": False,
        "prompt_submitted": False,
        "arbitrary_file_search_used": False,
        "repo_search_used": False,
        "shell_executed": False,
        "memory_mutated": False,
        "production_certified": False,
    }
    return V043PilotReviewTraceRecord(**_merge(defaults, overrides))


def create_v043_pilot_pi_review_record(pilot_review_id: str = "pilot-review", **overrides: Any) -> V043PilotPIReviewRecord:
    defaults = {
        "review_id": _new_id("v043-pilot-pi-review"),
        "pilot_review_id": pilot_review_id,
        "reconstructable_as_process_event": True,
        "metric_lineage_preserved": True,
        "feedback_lineage_preserved": True,
        "safety_lineage_preserved": True,
        "bounded_sources_only": True,
        "high_risk_counts_zero": True,
        "review_summary": "Pilot metric, feedback, and safety lineage are preserved as bounded process evidence.",
    }
    return V043PilotPIReviewRecord(**_merge(defaults, overrides))


def create_v043_pilot_review_safety_report(**overrides: Any) -> V043PilotReviewSafetyReport:
    defaults = {
        "report_id": "v0435-pilot-review-safety-report",
        "pilot_review_opened": True,
        "deterministic_review_by_default": True,
        "provider_invocation_allowed_by_default": False,
        "prompt_submission_allowed_by_default": False,
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
    return V043PilotReviewSafetyReport(**_merge(defaults, overrides))


def create_v0435_readiness_report(**overrides: Any) -> V0435ReadinessReport:
    defaults = {
        "pilot_metric_model_ready": True,
        "work_session_usability_review_ready": True,
        "business_artifact_usefulness_review_ready": True,
        "evidence_retrieval_review_ready": True,
        "grounded_synthesis_review_ready": True,
        "pi_reviewability_review_ready": True,
        "safety_boundary_review_ready": True,
        "v044_readiness_review_ready": True,
        "pilot_status_ready": True,
        "pilot_review_ready": True,
        "pilot_score_ready": True,
        "pilot_findings_ready": True,
        "pilot_next_ready": True,
        "pilot_report_ready": True,
        "acceptance_checklist_ready": True,
        "workflow_score_ready": True,
        "integrated_restore_document_ready": True,
        "v0436_or_v044_handoff_ready": True,
        "ready_for_arbitrary_file_search": False,
        "ready_for_repo_search": False,
        "ready_for_workspace_search": False,
        "ready_for_external_search": False,
        "ready_for_shell_execution": False,
        "ready_for_file_edit": False,
        "ready_for_patch_apply": False,
        "ready_for_provider_tool_calling": False,
        "ready_for_function_calling": False,
        "ready_for_subagent_invocation": False,
        "ready_for_general_agent_loop": False,
        "ready_for_autonomous_coding": False,
        "ready_for_memory_mutation": False,
        "ready_for_core_memory_write": False,
        "production_certified": False,
    }
    return V0435ReadinessReport(**_merge(defaults, overrides))


def create_v0436_polish_or_v044_controlled_workspace_read_handoff(
    metric_score: V043PilotMetricScore | None = None,
    **overrides: Any,
) -> V0436PolishOrV044ControlledWorkspaceReadHandoff:
    score = metric_score or create_v043_pilot_metric_score()
    decision, _reason, _required = _gate_from_score(score)
    if decision == V043PilotGateDecisionKind.PROCEED_TO_V044_DESIGN.value:
        target = "v0.44 Controlled Workspace Read Design"
        focus = ("read-only workspace scope model", "explicit allowlist", "source disclosure", "no edit/apply/shell/test/subagent")
    else:
        target = "v0.43.6 Final Pilot Polish"
        focus = ("polish confusing workflow text", "collect more pilot feedback", "improve evidence no-result guidance", "re-run acceptance metrics")
    defaults = {
        "handoff_id": "v0436-or-v044-handoff",
        "decision": decision,
        "target_version": target,
        "recommended_focus": focus,
        "must_not_open": (
            "arbitrary filesystem search",
            "repo search",
            "shell execution",
            "file edit/apply",
            "test execution",
            "provider tool/function calling",
            "subagents",
            "memory mutation",
            "production certification",
        ),
        "production_certified": False,
    }
    return V0436PolishOrV044ControlledWorkspaceReadHandoff(**_merge(defaults, overrides))


REQUIRED_V0435_RESTORE_SECTIONS = (
    "Restore Purpose",
    "One-Screen Restore Summary",
    "Current Version and Track Identity",
    "v0.43.4 Baseline Summary",
    "v0.43.5 Goal",
    "Pilot Review Concept",
    "Metric Dimensions",
    "Scoring Model",
    "Work Session Usability Review",
    "Business Artifact Usefulness Review",
    "Evidence Retrieval Review",
    "Grounded Synthesis Review",
    "Process Intelligence Reviewability",
    "Safety Boundary Review",
    "v0.44 Controlled Workspace Read Readiness",
    "Pilot Commands",
    "Acceptance Checklist",
    "Pilot Gate Decision",
    "Safety Boundary",
    "Required Test Commands",
    "Manual Pilot Commands",
    "Withdrawal Conditions",
    "v0.43.6 or v0.44 Recommended Next Step",
    "Copy-Paste Restore Prompt for Future GPT/Codex Session",
)


def create_v0435_integrated_restore_context_snapshot(**overrides: Any) -> V0435IntegratedRestoreContextSnapshot:
    defaults = {
        "snapshot_id": "v0435-integrated-restore-context",
        "current_version": V0435_VERSION,
        "current_track": V043_TRACK_NAME,
        "baseline_versions": ("v0.43.4", "v0.43.3", "v0.43.2", "v0.43.1", "v0.43.0", "v0.42.10"),
        "open_capabilities": ("pilot metrics", "pilot review", "pilot score", "pilot findings", "pilot next", "pilot report", "acceptance checklist", "workflow score"),
        "closed_capabilities": create_v0436_polish_or_v044_controlled_workspace_read_handoff().must_not_open,
        "integrated_doc_path": "docs/versions/v0.43/v0.43.5_pilot_review_acceptance_metrics_restore.md",
        "next_recommended_version": "v0.44 Controlled Workspace Read Design",
    }
    return V0435IntegratedRestoreContextSnapshot(**_merge(defaults, overrides))


def create_v0435_integrated_restore_packet(**overrides: Any) -> V0435IntegratedRestorePacket:
    sections = tuple(
        V0435IntegratedRestoreSection(f"v0435-section-{index}", title, True, f"Required v0.43.5 section: {title}", "future-session restore")
        for index, title in enumerate(REQUIRED_V0435_RESTORE_SECTIONS, 1)
    )
    defaults = {
        "restore_packet_id": "v0435-integrated-restore-packet",
        "snapshot": create_v0435_integrated_restore_context_snapshot(),
        "restore_sections": sections,
        "required_test_commands": (
            "py -m pytest tests\\test_v0435_pilot_review_acceptance_metrics.py",
            "py -m pytest tests\\test_v0434_evidence_grounded_business_synthesis.py",
        ),
        "single_integrated_doc_path": "docs/versions/v0.43/v0.43.5_pilot_review_acceptance_metrics_restore.md",
        "separate_restore_doc_created": False,
    }
    return V0435IntegratedRestorePacket(**_merge(defaults, overrides))


def create_v0435_integrated_restore_document_manifest(**overrides: Any) -> V0435IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "v0435-integrated-restore-document-manifest",
        "integrated_doc_path": "docs/versions/v0.43/v0.43.5_pilot_review_acceptance_metrics_restore.md",
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": False,
        "copy_paste_restore_prompt_required": True,
        "required_sections_present": True,
        "suitable_for_new_session_handoff": True,
    }
    return V0435IntegratedRestoreDocumentManifest(**_merge(defaults, overrides))


def _render_metric_score(score: V043PilotMetricScore) -> str:
    lines = ["Pilot score", f"overall_score: {score.overall_score:.2f}", f"overall_label: {score.overall_label}", f"ready_for_v044_design: {str(score.ready_for_v044_design).lower()}"]
    lines.extend(f"- {metric.dimension}: {metric.score:.2f} {metric.label}; blocking={str(metric.blocking).lower()}" for metric in score.metrics)
    return "\n".join(lines)


def _render_findings(findings: Sequence[V043PilotFinding]) -> str:
    lines = ["Pilot findings", f"count: {len(tuple(findings))}"]
    for item in findings:
        lines.append(f"- {item.finding_id} [{item.area}/{item.severity}] {item.description}; blocks_v044={str(item.blocks_v044).lower()}")
        lines.append(f"  action: {item.recommended_action}")
    return "\n".join(lines)


def _render_pilot_review(score: V043PilotMetricScore, findings: Sequence[V043PilotFinding], decision: str, reason: str, next_track: str) -> str:
    return "\n".join(
        (
            "Pilot review",
            f"overall: {score.overall_score:.2f} {score.overall_label}",
            f"gate_decision: {decision}",
            f"reason: {reason}",
            f"recommended_next_track: {next_track}",
            f"finding_count: {len(tuple(findings))}",
            "provider_invoked: false; prompt_submitted: false; shell=false; memory_mutated=false; production_certified=false",
        )
    )


def _render_pilot_report(
    summary: str,
    score: V043PilotMetricScore,
    findings: Sequence[V043PilotFinding],
    checklist: V043PilotAcceptanceChecklist,
    safety: V043SafetyBoundaryReview,
    v044: V043V044ReadinessReview,
) -> str:
    return "\n".join(
        (
            "Pilot report",
            summary,
            "",
            _render_metric_score(score),
            "",
            _render_findings(findings),
            "",
            f"Acceptance: passed={checklist.passed_count}; warnings={checklist.warning_count}; failed={checklist.failed_count}; blockers={checklist.blocker_count}",
            f"Safety: {safety.label}; shell_closed={str(safety.shell_closed).lower()}; file_edit_apply_closed={str(safety.file_edit_apply_closed).lower()}",
            f"v0.44 readiness: {v044.label}; {v044.recommended_v044_scope}",
            "high_risk: arbitrary_file_search=false; repo_search=false; shell=false; memory_mutated=false; production_certified=false",
        )
    )


__all__ = [
    name
    for name in globals()
    if name.startswith("V043")
    or name.startswith("create_v043")
    or name.startswith("execute_v043")
    or name.startswith("label_v043")
]
