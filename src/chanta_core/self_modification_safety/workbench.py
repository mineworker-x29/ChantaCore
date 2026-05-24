from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.self_modification_safety.mapping import (
    SELF_MODIFICATION_OCEL_EVENT_TYPES,
    SELF_MODIFICATION_OCEL_OBJECT_TYPES,
    SELF_MODIFICATION_OCEL_RELATION_TYPES,
)
from chanta_core.self_modification_safety.registry import (
    SELF_MODIFICATION_SEED_SUBJECT_IDS,
    SelfModificationRegistryService,
)
from chanta_core.utility.time import utc_now_iso


SELF_MODIFICATION_WORKBENCH_VERSION = "v0.22.8"
SELF_MODIFICATION_WORKBENCH_STATE = "self_modification_workbench_snapshot_created"
WORKBENCH_VIEW_SKILL_ID = "skill:self_modification_workbench_view"
TIMELINE_VIEW_SKILL_ID = "skill:self_modification_timeline_view"
FINDINGS_VIEW_SKILL_ID = "skill:self_modification_findings_view"
WORKBENCH_EFFECT_TYPES = ["read_only_observation"]
WORKBENCH_SECTIONS = {
    "overview",
    "pipeline",
    "requests",
    "candidates",
    "drafts",
    "safety",
    "dry_run",
    "dry-run",
    "review",
    "apply_gate",
    "apply",
    "bounded_apply",
    "post_apply",
    "post-apply",
    "outcomes",
    "findings",
    "timeline",
    "coverage",
    "readiness",
}


@dataclass(frozen=True)
class SelfModificationWorkbenchRequest:
    section: str = "overview"
    include_requests: bool = True
    include_candidates: bool = True
    include_drafts: bool = True
    include_static_safety: bool = True
    include_dry_run: bool = True
    include_review_gate: bool = True
    include_bounded_apply: bool = True
    include_post_apply: bool = True
    include_outcomes: bool = True
    include_findings: bool = True
    include_safety_boundary: bool = True
    include_ocel_coverage: bool = True
    max_recent_items: int = 30
    strictness: str = "standard"

    def normalized(self) -> "SelfModificationWorkbenchRequest":
        section = (self.section or "overview").strip()
        if section not in WORKBENCH_SECTIONS:
            section = "overview"
        return SelfModificationWorkbenchRequest(
            section=section,
            include_requests=bool(self.include_requests),
            include_candidates=bool(self.include_candidates),
            include_drafts=bool(self.include_drafts),
            include_static_safety=bool(self.include_static_safety),
            include_dry_run=bool(self.include_dry_run),
            include_review_gate=bool(self.include_review_gate),
            include_bounded_apply=bool(self.include_bounded_apply),
            include_post_apply=bool(self.include_post_apply),
            include_outcomes=bool(self.include_outcomes),
            include_findings=bool(self.include_findings),
            include_safety_boundary=bool(self.include_safety_boundary),
            include_ocel_coverage=bool(self.include_ocel_coverage),
            max_recent_items=max(1, int(self.max_recent_items)),
            strictness=self.strictness or "standard",
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "section": self.section,
            "include_requests": self.include_requests,
            "include_candidates": self.include_candidates,
            "include_drafts": self.include_drafts,
            "include_static_safety": self.include_static_safety,
            "include_dry_run": self.include_dry_run,
            "include_review_gate": self.include_review_gate,
            "include_bounded_apply": self.include_bounded_apply,
            "include_post_apply": self.include_post_apply,
            "include_outcomes": self.include_outcomes,
            "include_findings": self.include_findings,
            "include_safety_boundary": self.include_safety_boundary,
            "include_ocel_coverage": self.include_ocel_coverage,
            "max_recent_items": self.max_recent_items,
            "strictness": self.strictness,
        }


@dataclass(frozen=True)
class SelfModificationSubjectStatusView:
    subject_id: str
    subject_name: str
    version_introduced: str
    status: str
    latest_artifact_id: str | None
    artifact_count: int
    pending_count: int
    failed_count: int
    blocked_count: int
    open_finding_count: int
    stale: bool
    limitations: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "subject_id": self.subject_id,
            "subject_name": self.subject_name,
            "version_introduced": self.version_introduced,
            "status": self.status,
            "latest_artifact_id": self.latest_artifact_id,
            "artifact_count": self.artifact_count,
            "pending_count": self.pending_count,
            "failed_count": self.failed_count,
            "blocked_count": self.blocked_count,
            "open_finding_count": self.open_finding_count,
            "stale": self.stale,
            "limitations": list(self.limitations),
        }


@dataclass(frozen=True)
class SelfModificationPipelineItem:
    item_id: str
    request_id: str | None
    patch_candidate_id: str | None
    draft_id: str | None
    preview_id: str | None
    static_safety_report_id: str | None
    dry_run_report_id: str | None
    review_request_id: str | None
    review_decision_id: str | None
    apply_gate_id: str | None
    authorization_id: str | None
    rollback_plan_id: str | None
    bounded_apply_report_id: str | None
    transaction_id: str | None
    post_apply_verification_report_id: str | None
    outcome_id: str | None
    current_stage: str
    current_status: str
    next_required_action: str | None
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "request_id": self.request_id,
            "patch_candidate_id": self.patch_candidate_id,
            "draft_id": self.draft_id,
            "preview_id": self.preview_id,
            "static_safety_report_id": self.static_safety_report_id,
            "dry_run_report_id": self.dry_run_report_id,
            "review_request_id": self.review_request_id,
            "review_decision_id": self.review_decision_id,
            "apply_gate_id": self.apply_gate_id,
            "authorization_id": self.authorization_id,
            "rollback_plan_id": self.rollback_plan_id,
            "bounded_apply_report_id": self.bounded_apply_report_id,
            "transaction_id": self.transaction_id,
            "post_apply_verification_report_id": self.post_apply_verification_report_id,
            "outcome_id": self.outcome_id,
            "current_stage": self.current_stage,
            "current_status": self.current_status,
            "next_required_action": self.next_required_action,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class SelfModificationSafetyBoundarySummary:
    file_write_count: int
    bounded_writer_write_count: int
    unauthorized_write_count: int
    workspace_file_changed_count: int
    workspace_file_changed_without_transaction_count: int
    apply_without_gate_count: int
    consumed_authorization_reuse_count: int
    rollback_executed_count: int
    shell_executed_count: int
    test_lint_executed_count: int
    external_patch_command_count: int
    llm_judge_count: int
    memory_mutation_count: int
    persona_overlay_mutation_count: int
    raw_secret_exposure_count: int
    safety_status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "file_write_count": self.file_write_count,
            "bounded_writer_write_count": self.bounded_writer_write_count,
            "unauthorized_write_count": self.unauthorized_write_count,
            "workspace_file_changed_count": self.workspace_file_changed_count,
            "workspace_file_changed_without_transaction_count": self.workspace_file_changed_without_transaction_count,
            "apply_without_gate_count": self.apply_without_gate_count,
            "consumed_authorization_reuse_count": self.consumed_authorization_reuse_count,
            "rollback_executed_count": self.rollback_executed_count,
            "shell_executed_count": self.shell_executed_count,
            "test_lint_executed_count": self.test_lint_executed_count,
            "external_patch_command_count": self.external_patch_command_count,
            "llm_judge_count": self.llm_judge_count,
            "memory_mutation_count": self.memory_mutation_count,
            "persona_overlay_mutation_count": self.persona_overlay_mutation_count,
            "raw_secret_exposure_count": self.raw_secret_exposure_count,
            "safety_status": self.safety_status,
        }


@dataclass(frozen=True)
class SelfModificationAuthorizationView:
    authorization_id: str
    apply_gate_id: str
    patch_candidate_id: str
    authorized_for_stage: str
    authorized_next_version: str
    single_use: bool
    consumed: bool
    expired: bool
    consumed_by_transaction_id: str | None
    patch_applied: bool
    authorization_status: str
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "authorization_id": self.authorization_id,
            "apply_gate_id": self.apply_gate_id,
            "patch_candidate_id": self.patch_candidate_id,
            "authorized_for_stage": self.authorized_for_stage,
            "authorized_next_version": self.authorized_next_version,
            "single_use": self.single_use,
            "consumed": self.consumed,
            "expired": self.expired,
            "consumed_by_transaction_id": self.consumed_by_transaction_id,
            "patch_applied": self.patch_applied,
            "authorization_status": self.authorization_status,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class SelfModificationChangeView:
    change_id: str
    transaction_id: str
    relative_path: str
    before_hash: str | None
    after_hash: str | None
    workspace_file_changed_event_id: str | None
    post_apply_verification_report_id: str | None
    outcome_id: str | None
    verification_status: str | None
    outcome_status: str | None
    rollback_recommended: bool
    raw_content_emitted: bool
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "change_id": self.change_id,
            "transaction_id": self.transaction_id,
            "relative_path": self.relative_path,
            "before_hash": self.before_hash,
            "after_hash": self.after_hash,
            "workspace_file_changed_event_id": self.workspace_file_changed_event_id,
            "post_apply_verification_report_id": self.post_apply_verification_report_id,
            "outcome_id": self.outcome_id,
            "verification_status": self.verification_status,
            "outcome_status": self.outcome_status,
            "rollback_recommended": self.rollback_recommended,
            "raw_content_emitted": self.raw_content_emitted,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class SelfModificationFindingView:
    total_findings: int
    critical_count: int
    error_count: int
    warning_count: int
    info_count: int
    by_stage: dict[str, int]
    open_blocker_count: int
    rollback_recommended_count: int
    needs_more_input_count: int
    recent_findings: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_findings": self.total_findings,
            "critical_count": self.critical_count,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "info_count": self.info_count,
            "by_stage": dict(self.by_stage),
            "open_blocker_count": self.open_blocker_count,
            "rollback_recommended_count": self.rollback_recommended_count,
            "needs_more_input_count": self.needs_more_input_count,
            "recent_findings": [dict(item) for item in self.recent_findings],
        }


@dataclass(frozen=True)
class SelfModificationTimelineEvent:
    timeline_event_id: str
    occurred_at: str | None
    stage: str
    event_type: str
    object_refs: list[dict[str, Any]]
    status: str
    summary: str
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "timeline_event_id": self.timeline_event_id,
            "occurred_at": self.occurred_at,
            "stage": self.stage,
            "event_type": self.event_type,
            "object_refs": [dict(item) for item in self.object_refs],
            "status": self.status,
            "summary": self.summary,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class SelfModificationOCELCoverageView:
    object_type_count: int
    event_type_count: int
    relation_type_count: int
    required_object_types_missing: list[str]
    required_event_types_missing: list[str]
    required_relation_types_missing: list[str]
    workspace_file_changed_trace_complete: bool
    coverage_status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "object_type_count": self.object_type_count,
            "event_type_count": self.event_type_count,
            "relation_type_count": self.relation_type_count,
            "required_object_types_missing": list(self.required_object_types_missing),
            "required_event_types_missing": list(self.required_event_types_missing),
            "required_relation_types_missing": list(self.required_relation_types_missing),
            "workspace_file_changed_trace_complete": self.workspace_file_changed_trace_complete,
            "coverage_status": self.coverage_status,
        }


@dataclass(frozen=True)
class SelfModificationReadinessView:
    readiness_id: str
    ready_for_consolidation: bool
    readiness_status: str
    blocker_count: int
    warning_count: int
    incomplete_pipeline_count: int
    unverified_apply_count: int
    rollback_recommended_count: int
    required_next_actions: list[str]
    v0_22_9_recommendation: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "readiness_id": self.readiness_id,
            "ready_for_consolidation": self.ready_for_consolidation,
            "readiness_status": self.readiness_status,
            "blocker_count": self.blocker_count,
            "warning_count": self.warning_count,
            "incomplete_pipeline_count": self.incomplete_pipeline_count,
            "unverified_apply_count": self.unverified_apply_count,
            "rollback_recommended_count": self.rollback_recommended_count,
            "required_next_actions": list(self.required_next_actions),
            "v0_22_9_recommendation": self.v0_22_9_recommendation,
        }


@dataclass(frozen=True)
class SelfModificationWorkbenchSnapshot:
    snapshot_id: str
    created_at: str
    request: SelfModificationWorkbenchRequest
    subject_statuses: list[SelfModificationSubjectStatusView]
    pipeline_items: list[SelfModificationPipelineItem]
    authorizations: list[SelfModificationAuthorizationView]
    changes: list[SelfModificationChangeView]
    findings_view: SelfModificationFindingView
    timeline: list[SelfModificationTimelineEvent]
    safety_boundary: SelfModificationSafetyBoundarySummary
    ocel_coverage: SelfModificationOCELCoverageView
    readiness: SelfModificationReadinessView
    findings: list[dict[str, Any]]
    limitations: list[str]
    read_only: bool = True
    mutation_performed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "created_at": self.created_at,
            "request": self.request.to_dict(),
            "subject_statuses": [item.to_dict() for item in self.subject_statuses],
            "pipeline_items": [item.to_dict() for item in self.pipeline_items],
            "authorizations": [item.to_dict() for item in self.authorizations],
            "changes": [item.to_dict() for item in self.changes],
            "findings_view": self.findings_view.to_dict(),
            "timeline": [item.to_dict() for item in self.timeline],
            "safety_boundary": self.safety_boundary.to_dict(),
            "ocel_coverage": self.ocel_coverage.to_dict(),
            "readiness": self.readiness.to_dict(),
            "findings": [dict(item) for item in self.findings],
            "limitations": list(self.limitations),
            "read_only": self.read_only,
            "mutation_performed": self.mutation_performed,
        }


class SelfModificationWorkbenchSourceService:
    def __init__(
        self,
        *,
        requests: list[Any] | None = None,
        patch_candidates: list[Any] | None = None,
        patch_drafts: list[Any] | None = None,
        diff_previews: list[Any] | None = None,
        static_safety_reports: list[Any] | None = None,
        dry_run_reports: list[Any] | None = None,
        human_reviews: list[Any] | None = None,
        review_decisions: list[Any] | None = None,
        apply_gates: list[Any] | None = None,
        authorizations: list[Any] | None = None,
        rollback_plans: list[Any] | None = None,
        bounded_apply_reports: list[Any] | None = None,
        post_apply_reports: list[Any] | None = None,
        outcomes: list[Any] | None = None,
        events: list[dict[str, Any]] | None = None,
    ) -> None:
        self.requests = list(requests or [])
        self.patch_candidates = list(patch_candidates or [])
        self.patch_drafts = list(patch_drafts or [])
        self.diff_previews = list(diff_previews or [])
        self.static_safety_reports = list(static_safety_reports or [])
        self.dry_run_reports = list(dry_run_reports or [])
        self.human_reviews = list(human_reviews or [])
        self.review_decisions = list(review_decisions or [])
        self.apply_gates = list(apply_gates or [])
        self.authorizations = list(authorizations or [])
        self.rollback_plans = list(rollback_plans or [])
        self.bounded_apply_reports = list(bounded_apply_reports or [])
        self.post_apply_reports = list(post_apply_reports or [])
        self.outcomes = list(outcomes or [])
        self.events = [dict(item) for item in events or []]

    def load_requests(self) -> list[Any]:
        return list(self.requests)

    def load_patch_candidates(self) -> list[Any]:
        return list(self.patch_candidates)

    def load_patch_drafts(self) -> list[Any]:
        return list(self.patch_drafts)

    def load_diff_previews(self) -> list[Any]:
        return list(self.diff_previews)

    def load_static_safety_reports(self) -> list[Any]:
        return list(self.static_safety_reports)

    def load_dry_run_reports(self) -> list[Any]:
        return list(self.dry_run_reports)

    def load_human_reviews(self) -> list[Any]:
        return list(self.human_reviews)

    def load_review_decisions(self) -> list[Any]:
        return list(self.review_decisions)

    def load_apply_gates(self) -> list[Any]:
        return list(self.apply_gates)

    def load_authorizations(self) -> list[Any]:
        authorizations = list(self.authorizations)
        for gate in self.apply_gates:
            auth = getattr(gate, "authorization", None)
            if auth is not None and auth not in authorizations:
                authorizations.append(auth)
        return authorizations

    def load_rollback_plans(self) -> list[Any]:
        return list(self.rollback_plans)

    def load_bounded_apply_reports(self) -> list[Any]:
        return list(self.bounded_apply_reports)

    def load_post_apply_reports(self) -> list[Any]:
        return list(self.post_apply_reports)

    def load_outcomes(self) -> list[Any]:
        return list(self.outcomes)

    def load_events(self) -> list[dict[str, Any]]:
        return [dict(item) for item in self.events]

    def collect(self) -> dict[str, list[Any]]:
        return {
            "requests": self.load_requests(),
            "patch_candidates": self.load_patch_candidates(),
            "patch_drafts": self.load_patch_drafts(),
            "diff_previews": self.load_diff_previews(),
            "static_safety_reports": self.load_static_safety_reports(),
            "dry_run_reports": self.load_dry_run_reports(),
            "human_reviews": self.load_human_reviews(),
            "review_decisions": self.load_review_decisions(),
            "apply_gates": self.load_apply_gates(),
            "authorizations": self.load_authorizations(),
            "rollback_plans": self.load_rollback_plans(),
            "bounded_apply_reports": self.load_bounded_apply_reports(),
            "post_apply_reports": self.load_post_apply_reports(),
            "outcomes": self.load_outcomes(),
            "events": self.load_events(),
        }


class SelfModificationSubjectStatusService:
    def build_subject_statuses(self, sources: dict[str, list[Any]]) -> list[SelfModificationSubjectStatusView]:
        views: list[SelfModificationSubjectStatusView] = []
        for subject_id in ["subject:self_modification_safety_contract"] + SELF_MODIFICATION_SEED_SUBJECT_IDS + [
            "subject:self_modification_workbench"
        ]:
            source_key = _subject_source_key(subject_id)
            artifacts = sources.get(source_key, [])
            findings = _collect_stage_findings(subject_id, artifacts)
            failed = sum(1 for item in artifacts if _status_of(item) == "failed")
            blocked = sum(1 for item in artifacts if _status_of(item) == "blocked")
            pending = 1 if not artifacts and subject_id != "subject:self_modification_workbench" else 0
            status = _subject_status(artifacts, failed, blocked)
            latest = _artifact_id(artifacts[-1]) if artifacts else None
            views.append(
                SelfModificationSubjectStatusView(
                    subject_id=subject_id,
                    subject_name=subject_id.removeprefix("subject:"),
                    version_introduced=_subject_version(subject_id),
                    status=status,
                    latest_artifact_id=latest,
                    artifact_count=len(artifacts),
                    pending_count=pending,
                    failed_count=failed,
                    blocked_count=blocked,
                    open_finding_count=len(findings),
                    stale=bool(artifacts and subject_id != "subject:self_modification_workbench" and status == "not_available"),
                    limitations=[] if artifacts else ["No local artifact source was supplied for this subject."],
                )
            )
        return views


class SelfModificationPipelineViewService:
    def build_pipeline_items(self, sources: dict[str, list[Any]]) -> list[SelfModificationPipelineItem]:
        request = _latest(sources["requests"])
        candidate = _latest(sources["patch_candidates"])
        draft = _latest(sources["patch_drafts"])
        preview = _latest(sources["diff_previews"])
        static_report = _latest(sources["static_safety_reports"])
        dry_run = _latest(sources["dry_run_reports"])
        review_request = _latest(sources["human_reviews"])
        review_decision = _latest(sources["review_decisions"])
        gate = _latest(sources["apply_gates"])
        authorization = _latest(sources["authorizations"]) or getattr(gate, "authorization", None)
        rollback_plan = _latest(sources["rollback_plans"])
        bounded_apply = _latest(sources["bounded_apply_reports"])
        transaction = getattr(bounded_apply, "transaction", None)
        post_apply = _latest(sources["post_apply_reports"])
        outcome = _latest(sources["outcomes"])
        stage = _current_stage(
            request,
            candidate,
            draft,
            preview,
            static_report,
            dry_run,
            review_decision,
            gate,
            bounded_apply,
            post_apply,
            outcome,
        )
        status = _pipeline_status(stage, static_report, dry_run, gate, bounded_apply, post_apply, outcome)
        return [
            SelfModificationPipelineItem(
                item_id=f"self_modification_pipeline_item:{uuid4()}",
                request_id=_artifact_id(request),
                patch_candidate_id=_artifact_id(candidate) or _value(draft, "patch_candidate_id") or _value(preview, "patch_candidate_id"),
                draft_id=_artifact_id(draft) or _value(preview, "draft_id"),
                preview_id=_artifact_id(preview),
                static_safety_report_id=_artifact_id(static_report),
                dry_run_report_id=_artifact_id(dry_run),
                review_request_id=_artifact_id(review_request),
                review_decision_id=_artifact_id(review_decision) or _value(gate, "review_decision_id"),
                apply_gate_id=_artifact_id(gate) or _value(authorization, "apply_gate_id"),
                authorization_id=_artifact_id(authorization),
                rollback_plan_id=_artifact_id(rollback_plan) or _value(gate, "rollback_plan_id"),
                bounded_apply_report_id=_artifact_id(bounded_apply),
                transaction_id=_artifact_id(transaction),
                post_apply_verification_report_id=_artifact_id(post_apply),
                outcome_id=_artifact_id(outcome),
                current_stage=stage,
                current_status=status,
                next_required_action=_next_action(stage, status),
                evidence_refs=[{"ref_type": "workbench_pipeline", "version": SELF_MODIFICATION_WORKBENCH_VERSION}],
            )
        ]


class SelfModificationAuthorizationViewService:
    def build_authorization_views(self, sources: dict[str, list[Any]]) -> list[SelfModificationAuthorizationView]:
        transactions = [
            getattr(report, "transaction", None)
            for report in sources["bounded_apply_reports"]
            if getattr(report, "transaction", None) is not None
        ]
        views: list[SelfModificationAuthorizationView] = []
        for authorization in sources["authorizations"]:
            consumed = bool(getattr(authorization, "consumed", False))
            expired = bool(getattr(authorization, "expired", False))
            consumed_by = _transaction_for_authorization(transactions, _artifact_id(authorization))
            if expired:
                status = "expired"
            elif consumed:
                status = "consumed"
            elif not getattr(authorization, "single_use", True):
                status = "invalid"
            else:
                status = "open"
            views.append(
                SelfModificationAuthorizationView(
                    authorization_id=_artifact_id(authorization) or "",
                    apply_gate_id=_value(authorization, "apply_gate_id") or "",
                    patch_candidate_id=_value(authorization, "patch_candidate_id") or "",
                    authorized_for_stage=_value(authorization, "authorized_for_stage") or "",
                    authorized_next_version=_value(authorization, "authorized_next_version") or "",
                    single_use=bool(getattr(authorization, "single_use", True)),
                    consumed=consumed,
                    expired=expired,
                    consumed_by_transaction_id=consumed_by,
                    patch_applied=bool(getattr(authorization, "patch_applied", False)),
                    authorization_status=status,
                    evidence_refs=[{"ref_type": "authorization_view", "authorization_id": _artifact_id(authorization)}],
                )
            )
        return views


class SelfModificationChangeViewService:
    def build_change_views(self, sources: dict[str, list[Any]]) -> list[SelfModificationChangeView]:
        post_report = _latest(sources["post_apply_reports"])
        outcome = _latest(sources["outcomes"])
        views: list[SelfModificationChangeView] = []
        for report in sources["bounded_apply_reports"]:
            transaction = getattr(report, "transaction", None)
            if transaction is None:
                continue
            for change in getattr(transaction, "file_changes", []):
                views.append(
                    SelfModificationChangeView(
                        change_id=_artifact_id(change) or "",
                        transaction_id=_artifact_id(transaction) or "",
                        relative_path=_sanitize_relative_path(_value(change, "relative_path")),
                        before_hash=_value(change, "before_hash"),
                        after_hash=_value(change, "after_hash"),
                        workspace_file_changed_event_id=_value(change, "workspace_file_changed_event_id"),
                        post_apply_verification_report_id=_artifact_id(post_report),
                        outcome_id=_artifact_id(outcome),
                        verification_status=_value(post_report, "verification_status"),
                        outcome_status=_value(outcome, "outcome_status"),
                        rollback_recommended=bool(getattr(post_report, "rollback_recommended", False)),
                        raw_content_emitted=bool(getattr(change, "raw_content_emitted", False)),
                        evidence_refs=[{"ref_type": "change_view", "change_id": _artifact_id(change)}],
                    )
                )
        return views


class SelfModificationFindingViewService:
    def build_findings_view(self, sources: dict[str, list[Any]], max_recent_items: int) -> SelfModificationFindingView:
        findings = _all_findings(sources)
        by_stage: dict[str, int] = {}
        for finding in findings:
            stage = str(finding.get("stage", "unknown"))
            by_stage[stage] = by_stage.get(stage, 0) + 1
        severities = [str(item.get("severity", "info")) for item in findings]
        rollback_count = sum(1 for item in findings if item.get("finding_type") == "rollback_recommended")
        needs_more_count = sum(1 for item in findings if "needs_more_input" in str(item.get("finding_type", "")))
        return SelfModificationFindingView(
            total_findings=len(findings),
            critical_count=severities.count("critical"),
            error_count=severities.count("error"),
            warning_count=severities.count("warning"),
            info_count=severities.count("info"),
            by_stage=by_stage,
            open_blocker_count=sum(1 for item in severities if item in {"critical", "error"}),
            rollback_recommended_count=rollback_count,
            needs_more_input_count=needs_more_count,
            recent_findings=findings[:max_recent_items],
        )


class SelfModificationTimelineService:
    def build_timeline(self, sources: dict[str, list[Any]], max_recent_items: int) -> list[SelfModificationTimelineEvent]:
        events: list[SelfModificationTimelineEvent] = []
        for stage, key, event_type in [
            ("request", "requests", "self_modification_request_received"),
            ("candidate", "patch_candidates", "self_modification_patch_candidate_created"),
            ("draft", "patch_drafts", "self_modification_patch_operation_drafted"),
            ("diff_preview", "diff_previews", "self_modification_diff_preview_created"),
            ("static_safety", "static_safety_reports", "self_modification_static_safety_report_created"),
            ("dry_run", "dry_run_reports", "self_modification_dry_run_report_created"),
            ("review", "review_decisions", "self_modification_human_review_decision_recorded"),
            ("apply_gate", "apply_gates", "self_modification_apply_gate_opened"),
            ("bounded_apply", "bounded_apply_reports", "self_modification_bounded_apply_report_created"),
            ("post_apply", "post_apply_reports", "self_modification_post_apply_verification_report_created"),
            ("outcome", "outcomes", "self_modification_outcome_recorded"),
        ]:
            for artifact in sources[key]:
                status = _timeline_status(artifact)
                events.append(
                    SelfModificationTimelineEvent(
                        timeline_event_id=f"self_modification_timeline_event:{uuid4()}",
                        occurred_at=_value(artifact, "created_at") or _value(artifact, "decided_at"),
                        stage=stage,
                        event_type=event_type,
                        object_refs=[{"ref_type": stage, "object_id": _artifact_id(artifact)}],
                        status=status,
                        summary=f"{stage} artifact visible in workbench.",
                        evidence_refs=[{"ref_type": "workbench_timeline", "stage": stage}],
                    )
                )
        events.sort(key=lambda item: (item.occurred_at or "", item.stage, item.event_type))
        return events[:max_recent_items]


class SelfModificationSafetyBoundaryService:
    def build_safety_summary(self, sources: dict[str, list[Any]]) -> SelfModificationSafetyBoundarySummary:
        transactions = [
            getattr(report, "transaction", None)
            for report in sources["bounded_apply_reports"]
            if getattr(report, "transaction", None) is not None
        ]
        changes = [change for transaction in transactions for change in getattr(transaction, "file_changes", [])]
        changed_count = sum(1 for change in changes if _value(change, "workspace_file_changed_event_id"))
        without_transaction = sum(1 for event in sources["events"] if event.get("event_type") == "workspace_file_changed" and not event.get("transaction_id"))
        apply_without_gate = sum(
            1
            for transaction in transactions
            if not getattr(getattr(transaction, "validation_result", None), "gate_status_open", True)
        )
        consumed_reuse = _authorization_reuse_count(sources["authorizations"], transactions)
        rollback_executed = sum(1 for item in sources["rollback_plans"] if bool(getattr(item, "rollback_executed", False)))
        shell_count = _flag_count(sources, "shell_executed")
        lint_count = _flag_count(sources, "test_lint_executed")
        raw_secret = sum(1 for item in _all_findings(sources) if "secret" in str(item.get("finding_type", "")).lower())
        unauthorized = max(0, changed_count - len(changes)) + without_transaction
        violation_count = unauthorized + apply_without_gate + consumed_reuse + rollback_executed + shell_count + lint_count + raw_secret
        status = "violation" if violation_count else ("warning" if changed_count and len(changes) != changed_count else "ok")
        return SelfModificationSafetyBoundarySummary(
            file_write_count=len(changes),
            bounded_writer_write_count=len(changes),
            unauthorized_write_count=unauthorized,
            workspace_file_changed_count=changed_count,
            workspace_file_changed_without_transaction_count=without_transaction,
            apply_without_gate_count=apply_without_gate,
            consumed_authorization_reuse_count=consumed_reuse,
            rollback_executed_count=rollback_executed,
            shell_executed_count=shell_count,
            test_lint_executed_count=lint_count,
            external_patch_command_count=0,
            llm_judge_count=0,
            memory_mutation_count=0,
            persona_overlay_mutation_count=0,
            raw_secret_exposure_count=raw_secret,
            safety_status=status,
        )


class SelfModificationOCELCoverageService:
    def build_coverage(self, sources: dict[str, list[Any]]) -> SelfModificationOCELCoverageView:
        required_objects = [
            "self_modification_workbench_snapshot",
            "self_modification_subject_status_view",
            "self_modification_pipeline_item",
            "self_modification_safety_boundary_summary",
            "self_modification_authorization_view",
            "self_modification_change_view",
            "self_modification_finding_view",
            "self_modification_timeline_event",
            "self_modification_ocel_coverage_view",
            "self_modification_readiness_view",
        ]
        required_events = [
            "self_modification_workbench_requested",
            "self_modification_workbench_snapshot_created",
            "self_modification_findings_viewed",
            "self_modification_timeline_viewed",
            "self_modification_safety_boundary_viewed",
        ]
        required_relations = [
            "views_self_modification_pipeline",
            "views_authorization_state",
            "views_safety_boundary",
            "views_timeline",
            "views_findings",
            "computes_self_modification_readiness",
        ]
        missing_objects = [item for item in required_objects if item not in SELF_MODIFICATION_OCEL_OBJECT_TYPES]
        missing_events = [item for item in required_events if item not in SELF_MODIFICATION_OCEL_EVENT_TYPES]
        missing_relations = [item for item in required_relations if item not in SELF_MODIFICATION_OCEL_RELATION_TYPES]
        trace_complete = not any(
            event.get("event_type") == "workspace_file_changed" and not event.get("transaction_id")
            for event in sources["events"]
        )
        status = "complete" if not (missing_objects or missing_events or missing_relations) else "partial"
        if missing_objects and missing_events and missing_relations:
            status = "missing"
        return SelfModificationOCELCoverageView(
            object_type_count=len(SELF_MODIFICATION_OCEL_OBJECT_TYPES),
            event_type_count=len(SELF_MODIFICATION_OCEL_EVENT_TYPES),
            relation_type_count=len(SELF_MODIFICATION_OCEL_RELATION_TYPES),
            required_object_types_missing=missing_objects,
            required_event_types_missing=missing_events,
            required_relation_types_missing=missing_relations,
            workspace_file_changed_trace_complete=trace_complete,
            coverage_status=status,
        )


class SelfModificationReadinessService:
    def build_readiness(
        self,
        pipeline_items: list[SelfModificationPipelineItem],
        safety_boundary: SelfModificationSafetyBoundarySummary,
        findings_view: SelfModificationFindingView,
        ocel_coverage: SelfModificationOCELCoverageView,
    ) -> SelfModificationReadinessView:
        incomplete = sum(1 for item in pipeline_items if item.current_status != "completed")
        unverified_apply = sum(1 for item in pipeline_items if item.bounded_apply_report_id and not item.post_apply_verification_report_id)
        blockers = 0
        if safety_boundary.safety_status == "violation":
            blockers += 1
        if findings_view.critical_count or findings_view.error_count:
            blockers += findings_view.critical_count + findings_view.error_count
        if unverified_apply:
            blockers += unverified_apply
        if not ocel_coverage.workspace_file_changed_trace_complete:
            blockers += 1
        warnings = findings_view.warning_count + incomplete + findings_view.rollback_recommended_count
        status = "blocked" if blockers else ("warning" if warnings else "ready")
        actions = []
        if unverified_apply:
            actions.append("Complete post-apply verification before consolidation.")
        if findings_view.rollback_recommended_count:
            actions.append("Review rollback recommendations before consolidation.")
        if incomplete:
            actions.append("Resolve pending pipeline stages before consolidation.")
        if safety_boundary.safety_status == "violation":
            actions.append("Resolve safety boundary violations.")
        recommendation = (
            "Proceed to v0.22.9 Self-Modification Safety Consolidation."
            if status == "ready"
            else "Delay v0.22.9 consolidation until blockers and warnings are resolved."
        )
        return SelfModificationReadinessView(
            readiness_id=f"self_modification_readiness_view:{uuid4()}",
            ready_for_consolidation=status == "ready",
            readiness_status=status,
            blocker_count=blockers,
            warning_count=warnings,
            incomplete_pipeline_count=incomplete,
            unverified_apply_count=unverified_apply,
            rollback_recommended_count=findings_view.rollback_recommended_count,
            required_next_actions=actions,
            v0_22_9_recommendation=recommendation,
        )


class SelfModificationWorkbenchService:
    def __init__(
        self,
        *,
        source_service: SelfModificationWorkbenchSourceService | None = None,
        subject_status_service: SelfModificationSubjectStatusService | None = None,
        pipeline_service: SelfModificationPipelineViewService | None = None,
        safety_service: SelfModificationSafetyBoundaryService | None = None,
        authorization_service: SelfModificationAuthorizationViewService | None = None,
        change_service: SelfModificationChangeViewService | None = None,
        finding_service: SelfModificationFindingViewService | None = None,
        timeline_service: SelfModificationTimelineService | None = None,
        coverage_service: SelfModificationOCELCoverageService | None = None,
        readiness_service: SelfModificationReadinessService | None = None,
    ) -> None:
        self.source_service = source_service or SelfModificationWorkbenchSourceService()
        self.subject_status_service = subject_status_service or SelfModificationSubjectStatusService()
        self.pipeline_service = pipeline_service or SelfModificationPipelineViewService()
        self.safety_service = safety_service or SelfModificationSafetyBoundaryService()
        self.authorization_service = authorization_service or SelfModificationAuthorizationViewService()
        self.change_service = change_service or SelfModificationChangeViewService()
        self.finding_service = finding_service or SelfModificationFindingViewService()
        self.timeline_service = timeline_service or SelfModificationTimelineService()
        self.coverage_service = coverage_service or SelfModificationOCELCoverageService()
        self.readiness_service = readiness_service or SelfModificationReadinessService()

    def build_snapshot(self, request: SelfModificationWorkbenchRequest | None = None) -> SelfModificationWorkbenchSnapshot:
        request = (request or SelfModificationWorkbenchRequest()).normalized()
        sources = self.source_service.collect()
        subject_statuses = self.subject_status_service.build_subject_statuses(sources)
        pipeline_items = self.pipeline_service.build_pipeline_items(sources)
        authorizations = self.authorization_service.build_authorization_views(sources)
        changes = self.change_service.build_change_views(sources)
        findings_view = self.finding_service.build_findings_view(sources, request.max_recent_items)
        timeline = self.timeline_service.build_timeline(sources, request.max_recent_items)
        safety_boundary = self.safety_service.build_safety_summary(sources)
        ocel_coverage = self.coverage_service.build_coverage(sources)
        readiness = self.readiness_service.build_readiness(pipeline_items, safety_boundary, findings_view, ocel_coverage)
        findings = _snapshot_findings(readiness, safety_boundary, findings_view)
        return SelfModificationWorkbenchSnapshot(
            snapshot_id=f"self_modification_workbench_snapshot:{uuid4()}",
            created_at=utc_now_iso(),
            request=request,
            subject_statuses=subject_statuses,
            pipeline_items=pipeline_items,
            authorizations=authorizations,
            changes=changes,
            findings_view=findings_view,
            timeline=timeline,
            safety_boundary=safety_boundary,
            ocel_coverage=ocel_coverage,
            readiness=readiness,
            findings=findings,
            limitations=["Workbench is read-only and does not authorize apply, consume authorization, verify post-apply state, or execute rollback."],
        )

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": SELF_MODIFICATION_WORKBENCH_VERSION,
            "layer": "self_modification_safety",
            "subject": "self_modification_workbench",
            "principles": [
                "workbench is not modification",
                "workbench visibility does not authorize apply",
                "workbench does not consume authorization",
                "workbench does not execute rollback",
                "workbench does not run tests or shell",
            ],
            "read_only": True,
            "mutation_performed": False,
            "safe_to_apply": False,
            "file_write_enabled": False,
            "apply_patch_enabled": False,
            "post_apply_verified": False,
            "file_write_performed": False,
            "workspace_file_changed_emitted": False,
            "rollback_executed": False,
            "shell_executed": False,
            "test_lint_executed": False,
            "llm_judge_enabled": False,
            "no_file_mutation_occurred": True,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "version": SELF_MODIFICATION_WORKBENCH_VERSION,
            "layer": "self_modification_safety",
            "state": SELF_MODIFICATION_WORKBENCH_STATE,
            "source_read_models": [
                "SelfModificationRequestState",
                "PatchCandidateState",
                "PatchDraftState",
                "DiffPreviewState",
                "PatchStaticSafetyState",
                "PatchDryRunState",
                "HumanReviewState",
                "ApplyGateState",
                "BoundedPatchApplyState",
                "WorkspaceFileChangeState",
                "PostApplyVerificationState",
                "ModificationOutcomeState",
            ],
            "target_read_models": [
                "SelfModificationWorkbenchState",
                "SelfModificationPipelineState",
                "SelfModificationSafetyBoundaryState",
                "SelfModificationReadinessState",
            ],
            "effect_types": list(WORKBENCH_EFFECT_TYPES),
            "read_only": True,
            "mutation_performed": False,
            "safe_to_apply": False,
            "file_write_enabled": False,
            "apply_patch_enabled": False,
            "post_apply_verified": False,
            "no_file_mutation_occurred": True,
        }

    def render_snapshot_cli(self, snapshot: SelfModificationWorkbenchSnapshot) -> str:
        item = snapshot.pipeline_items[0] if snapshot.pipeline_items else None
        return "\n".join(
            [
                "Self-Modification Workbench",
                f"version={SELF_MODIFICATION_WORKBENCH_VERSION}",
                "layer=self_modification_safety",
                f"section={snapshot.request.section}",
                f"snapshot_id={snapshot.snapshot_id}",
                f"pipeline_status={item.current_status if item else 'not_available'}",
                f"current_stage={item.current_stage if item else 'not_available'}",
                f"next_required_action={item.next_required_action if item else 'unknown'}",
                f"safety_status={snapshot.safety_boundary.safety_status}",
                f"pending_count={sum(status.pending_count for status in snapshot.subject_statuses)}",
                f"unverified_apply_count={snapshot.readiness.unverified_apply_count}",
                f"rollback_recommended_count={snapshot.readiness.rollback_recommended_count}",
                f"workspace_file_changed_trace_complete={str(snapshot.ocel_coverage.workspace_file_changed_trace_complete).lower()}",
                f"readiness_status={snapshot.readiness.readiness_status}",
                f"ready_for_v0.22.9={str(snapshot.readiness.ready_for_consolidation).lower()}",
                f"v0_22_9_recommendation={snapshot.readiness.v0_22_9_recommendation}",
                f"read_only={str(snapshot.read_only).lower()}",
                f"mutation_performed={str(snapshot.mutation_performed).lower()}",
                "raw_full_file_content_printed=False",
                "private_full_paths_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_pig_report_cli(self) -> str:
        report = self.build_pig_report()
        return "\n".join(
            [
                "Self-Modification Workbench PIG Report",
                f"version={report['version']}",
                f"layer={report['layer']}",
                f"subject={report['subject']}",
                f"principles={','.join(report['principles'])}",
                f"read_only={str(report['read_only']).lower()}",
                f"mutation_performed={str(report['mutation_performed']).lower()}",
                f"safe_to_apply={str(report['safe_to_apply']).lower()}",
                f"file_write_enabled={str(report['file_write_enabled']).lower()}",
                f"apply_patch_enabled={str(report['apply_patch_enabled']).lower()}",
                f"post_apply_verified={str(report['post_apply_verified']).lower()}",
                f"file_write_performed={str(report['file_write_performed']).lower()}",
                f"workspace_file_changed_emitted={str(report['workspace_file_changed_emitted']).lower()}",
                f"rollback_executed={str(report['rollback_executed']).lower()}",
                f"shell_executed={str(report['shell_executed']).lower()}",
                f"test_lint_executed={str(report['test_lint_executed']).lower()}",
                f"llm_judge_enabled={str(report['llm_judge_enabled']).lower()}",
                f"no_file_mutation_occurred={str(report['no_file_mutation_occurred']).lower()}",
                "No file mutation occurred.",
                "raw_file_content_printed=False",
                "raw_full_file_content_printed=False",
                "private_full_paths_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_ocpx_projection_cli(self) -> str:
        projection = self.build_ocpx_projection()
        return "\n".join(
            [
                "Self-Modification Workbench OCPX Projection",
                f"version={projection['version']}",
                f"layer={projection['layer']}",
                f"state={projection['state']}",
                f"source_read_models={','.join(projection['source_read_models'])}",
                f"target_read_models={','.join(projection['target_read_models'])}",
                f"effect_types={','.join(projection['effect_types'])}",
                f"read_only={str(projection['read_only']).lower()}",
                f"mutation_performed={str(projection['mutation_performed']).lower()}",
                f"safe_to_apply={str(projection['safe_to_apply']).lower()}",
                f"file_write_enabled={str(projection['file_write_enabled']).lower()}",
                f"apply_patch_enabled={str(projection['apply_patch_enabled']).lower()}",
                f"post_apply_verified={str(projection['post_apply_verified']).lower()}",
                f"no_file_mutation_occurred={str(projection['no_file_mutation_occurred']).lower()}",
                "No file mutation occurred.",
                "raw_file_content_printed=False",
                "raw_full_file_content_printed=False",
                "private_full_paths_printed=False",
                "raw_secrets_printed=False",
            ]
        )


def _artifact_id(item: Any) -> str | None:
    if item is None:
        return None
    for name in [
        "outcome_id",
        "change_id",
        "transaction_id",
        "authorization_id",
        "apply_gate_id",
        "rollback_plan_id",
        "decision_id",
        "review_request_id",
        "report_id",
        "preview_id",
        "draft_id",
        "patch_candidate_id",
        "request_id",
    ]:
        value = getattr(item, name, None)
        if value:
            return str(value)
    if isinstance(item, dict):
        for name in ["id", "object_id", "event_id", "report_id"]:
            if item.get(name):
                return str(item[name])
    return None


def _value(item: Any, name: str) -> str | None:
    if item is None:
        return None
    if isinstance(item, dict):
        value = item.get(name)
    else:
        value = getattr(item, name, None)
    return str(value) if value is not None else None


def _latest(items: list[Any]) -> Any | None:
    return items[-1] if items else None


def _subject_source_key(subject_id: str) -> str:
    return {
        "subject:self_modification_safety_contract": "events",
        "subject:modification_request": "requests",
        "subject:patch_candidate": "patch_candidates",
        "subject:diff_preview": "diff_previews",
        "subject:patch_static_safety": "static_safety_reports",
        "subject:patch_dry_run": "dry_run_reports",
        "subject:modification_review_gate": "review_decisions",
        "subject:patch_apply_gate": "apply_gates",
        "subject:rollback_plan": "rollback_plans",
        "subject:bounded_patch_apply": "bounded_apply_reports",
        "subject:post_apply_verification": "post_apply_reports",
        "subject:modification_outcome": "outcomes",
        "subject:self_modification_workbench": "events",
    }.get(subject_id, "events")


def _subject_version(subject_id: str) -> str:
    return {
        "subject:self_modification_safety_contract": "v0.22.0",
        "subject:modification_request": "v0.22.1",
        "subject:patch_candidate": "v0.22.1",
        "subject:diff_preview": "v0.22.2",
        "subject:patch_static_safety": "v0.22.3",
        "subject:patch_dry_run": "v0.22.4",
        "subject:modification_review_gate": "v0.22.5",
        "subject:patch_apply_gate": "v0.22.5",
        "subject:rollback_plan": "v0.22.5",
        "subject:bounded_patch_apply": "v0.22.6",
        "subject:post_apply_verification": "v0.22.7",
        "subject:modification_outcome": "v0.22.7",
        "subject:self_modification_workbench": "v0.22.8",
    }.get(subject_id, "v0.22.0")


def _subject_status(artifacts: list[Any], failed: int, blocked: int) -> str:
    if blocked:
        return "blocked"
    if failed:
        return "failed"
    if artifacts:
        return "ok"
    return "not_available"


def _status_of(item: Any) -> str:
    for name in [
        "static_safety_status",
        "dry_run_status",
        "gate_status",
        "apply_status",
        "verification_status",
        "outcome_status",
        "report_status",
    ]:
        value = getattr(item, name, None)
        if value in {"blocked", "failed", "rollback_recommended", "verification_failed"}:
            return "blocked" if value == "blocked" else "failed"
    return "ok"


def _current_stage(*items: Any) -> str:
    labels = [
        "request",
        "candidate",
        "draft",
        "diff_preview",
        "static_safety",
        "dry_run",
        "review",
        "apply_gate",
        "bounded_apply",
        "post_apply",
        "outcome",
    ]
    stage = "contract"
    for label, item in zip(labels, items):
        if item is not None:
            stage = label
    return stage


def _pipeline_status(stage: str, static_report: Any, dry_run: Any, gate: Any, bounded_apply: Any, post_apply: Any, outcome: Any) -> str:
    for item in [static_report, dry_run, gate, bounded_apply, post_apply, outcome]:
        if _status_of(item) == "blocked":
            return "blocked"
        if _status_of(item) == "failed":
            return "failed"
    if stage == "outcome":
        return "completed"
    if stage in {"static_safety", "dry_run", "review", "apply_gate", "bounded_apply", "post_apply"}:
        return "ready"
    return "pending"


def _next_action(stage: str, status: str) -> str | None:
    if status in {"blocked", "failed"}:
        return "Resolve blocker before continuing self-modification pipeline."
    return {
        "contract": "Create self-modification request.",
        "request": "Create patch candidate.",
        "candidate": "Create patch draft and diff preview.",
        "draft": "Create diff preview.",
        "diff_preview": "Run static safety check.",
        "static_safety": "Run dry-run/applicability check.",
        "dry_run": "Request human review.",
        "review": "Evaluate apply gate.",
        "apply_gate": "Run bounded patch apply only with explicit authorization.",
        "bounded_apply": "Run post-apply verification and outcome recording.",
        "post_apply": "Record modification outcome.",
        "outcome": "Ready for v0.22.9 consolidation review.",
    }.get(stage)


def _transaction_for_authorization(transactions: list[Any], authorization_id: str | None) -> str | None:
    if not authorization_id:
        return None
    for transaction in transactions:
        if _value(transaction, "authorization_id") == authorization_id:
            return _artifact_id(transaction)
    return None


def _authorization_reuse_count(authorizations: list[Any], transactions: list[Any]) -> int:
    count = 0
    for authorization in authorizations:
        if bool(getattr(authorization, "consumed", False)) and _transaction_for_authorization(transactions, _artifact_id(authorization)) is None:
            count += 1
    return count


def _flag_count(sources: dict[str, list[Any]], flag_name: str) -> int:
    total = 0
    for key in ["bounded_apply_reports", "post_apply_reports", "outcomes"]:
        for item in sources[key]:
            total += int(bool(getattr(item, flag_name, False)))
            transaction = getattr(item, "transaction", None)
            total += int(bool(getattr(transaction, flag_name, False)))
    return total


def _collect_stage_findings(subject_id: str, artifacts: list[Any]) -> list[dict[str, Any]]:
    stage = subject_id.removeprefix("subject:")
    findings: list[dict[str, Any]] = []
    for artifact in artifacts:
        for finding in getattr(artifact, "findings", []) or []:
            findings.append(_finding_dict(finding, stage))
    return findings


def _all_findings(sources: dict[str, list[Any]]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    stage_map = {
        "patch_candidates": "candidate",
        "patch_drafts": "draft",
        "static_safety_reports": "static_safety",
        "dry_run_reports": "dry_run",
        "apply_gates": "apply_gate",
        "bounded_apply_reports": "bounded_apply",
        "post_apply_reports": "post_apply",
    }
    for key, stage in stage_map.items():
        for artifact in sources[key]:
            for finding in getattr(artifact, "findings", []) or []:
                findings.append(_finding_dict(finding, stage))
            if stage == "post_apply" and bool(getattr(artifact, "rollback_recommended", False)):
                findings.append({"severity": "warning", "finding_type": "rollback_recommended", "stage": stage})
    return findings


def _finding_dict(finding: Any, stage: str) -> dict[str, Any]:
    if isinstance(finding, dict):
        payload = dict(finding)
    else:
        payload = {
            "finding_id": getattr(finding, "finding_id", None),
            "severity": getattr(finding, "severity", "info"),
            "finding_type": getattr(finding, "finding_type", "unknown"),
            "message": getattr(finding, "message", ""),
        }
    payload["stage"] = stage
    if "target_ref" in payload:
        payload["target_ref"] = _sanitize_ref(payload.get("target_ref"))
    return payload


def _timeline_status(artifact: Any) -> str:
    status = _status_of(artifact)
    if status == "ok":
        return "ok"
    return status


def _sanitize_relative_path(relative_path: str | None) -> str:
    if not relative_path:
        return ""
    return str(relative_path).replace("\\", "/").split("/")[-1] if ":" in str(relative_path) else str(relative_path).replace("\\", "/")


def _sanitize_ref(ref: Any) -> Any:
    if not isinstance(ref, dict):
        return ref
    clean = dict(ref)
    if "relative_path" in clean:
        clean["relative_path"] = _sanitize_relative_path(str(clean["relative_path"]))
    return clean


def _snapshot_findings(
    readiness: SelfModificationReadinessView,
    safety_boundary: SelfModificationSafetyBoundarySummary,
    findings_view: SelfModificationFindingView,
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if readiness.readiness_status == "blocked":
        findings.append({"severity": "error", "finding_type": "workbench_blocker", "stage": "readiness"})
    if safety_boundary.safety_status == "violation":
        findings.append({"severity": "critical", "finding_type": "safety_boundary_violation", "stage": "safety"})
    if findings_view.warning_count:
        findings.append({"severity": "warning", "finding_type": "open_warnings", "stage": "findings"})
    return findings
