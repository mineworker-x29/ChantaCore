from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.execution.ids import (
    new_execution_result_promotion_candidate_id,
    new_execution_result_promotion_decision_id,
    new_execution_result_promotion_finding_id,
    new_execution_result_promotion_policy_id,
    new_execution_result_promotion_result_id,
    new_execution_result_promotion_review_request_id,
)
from chanta_core.execution.models import (
    ExecutionArtifactRef,
    ExecutionEnvelope,
    ExecutionOutcomeSummary,
    ExecutionOutputSnapshot,
)
from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


ALLOWED_TARGET_KINDS = [
    "context_history_candidate",
    "memory_candidate",
    "personal_overlay_candidate",
    "persona_source_candidate",
    "workspace_summary_candidate",
    "manual_note_candidate",
    "process_pattern_candidate",
    "other",
]
DENIED_TARGET_KINDS = [
    "canonical_memory",
    "canonical_persona",
    "direct_overlay_write",
    "direct_file_write",
]
ALLOWED_DECISIONS = {
    "approved_for_later_promotion",
    "rejected",
    "no_action",
    "needs_more_info",
    "archive",
    "error",
}


@dataclass(frozen=True)
class ExecutionResultPromotionPolicy:
    policy_id: str
    policy_name: str
    allowed_target_kinds: list[str]
    denied_target_kinds: list[str]
    require_review: bool
    allow_canonical_promotion: bool
    allow_private_candidate: bool
    max_preview_chars: int
    status: str
    created_at: str
    policy_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "policy_name": self.policy_name,
            "allowed_target_kinds": list(self.allowed_target_kinds),
            "denied_target_kinds": list(self.denied_target_kinds),
            "require_review": self.require_review,
            "allow_canonical_promotion": self.allow_canonical_promotion,
            "allow_private_candidate": self.allow_private_candidate,
            "max_preview_chars": self.max_preview_chars,
            "status": self.status,
            "created_at": self.created_at,
            "policy_attrs": dict(self.policy_attrs),
        }


@dataclass(frozen=True)
class ExecutionResultPromotionCandidate:
    candidate_id: str
    envelope_id: str
    outcome_summary_id: str | None
    output_snapshot_id: str | None
    artifact_ref_id: str | None
    target_kind: str
    candidate_title: str
    candidate_preview: dict[str, Any]
    candidate_hash: str | None
    source_ref_kind: str
    source_ref_id: str | None
    private: bool
    sensitive: bool
    review_status: str
    canonical_promotion_enabled: bool
    created_at: str
    candidate_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "envelope_id": self.envelope_id,
            "outcome_summary_id": self.outcome_summary_id,
            "output_snapshot_id": self.output_snapshot_id,
            "artifact_ref_id": self.artifact_ref_id,
            "target_kind": self.target_kind,
            "candidate_title": self.candidate_title,
            "candidate_preview": dict(self.candidate_preview),
            "candidate_hash": self.candidate_hash,
            "source_ref_kind": self.source_ref_kind,
            "source_ref_id": self.source_ref_id,
            "private": self.private,
            "sensitive": self.sensitive,
            "review_status": self.review_status,
            "canonical_promotion_enabled": self.canonical_promotion_enabled,
            "created_at": self.created_at,
            "candidate_attrs": dict(self.candidate_attrs),
        }


@dataclass(frozen=True)
class ExecutionResultPromotionReviewRequest:
    review_request_id: str
    candidate_id: str
    envelope_id: str
    requested_by: str | None
    session_id: str | None
    turn_id: str | None
    process_instance_id: str | None
    status: str
    created_at: str
    request_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "review_request_id": self.review_request_id,
            "candidate_id": self.candidate_id,
            "envelope_id": self.envelope_id,
            "requested_by": self.requested_by,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "process_instance_id": self.process_instance_id,
            "status": self.status,
            "created_at": self.created_at,
            "request_attrs": dict(self.request_attrs),
        }


@dataclass(frozen=True)
class ExecutionResultPromotionDecision:
    decision_id: str
    review_request_id: str
    candidate_id: str
    decision: str
    reviewer_type: str | None
    reviewer_id: str | None
    reason: str | None
    approved_target_kind: str | None
    can_promote_now: bool
    requires_manual_action: bool
    created_at: str
    decision_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "review_request_id": self.review_request_id,
            "candidate_id": self.candidate_id,
            "decision": self.decision,
            "reviewer_type": self.reviewer_type,
            "reviewer_id": self.reviewer_id,
            "reason": self.reason,
            "approved_target_kind": self.approved_target_kind,
            "can_promote_now": self.can_promote_now,
            "requires_manual_action": self.requires_manual_action,
            "created_at": self.created_at,
            "decision_attrs": dict(self.decision_attrs),
        }


@dataclass(frozen=True)
class ExecutionResultPromotionFinding:
    finding_id: str
    candidate_id: str
    envelope_id: str
    finding_type: str
    status: str
    severity: str
    message: str
    subject_ref: str | None
    created_at: str
    finding_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "candidate_id": self.candidate_id,
            "envelope_id": self.envelope_id,
            "finding_type": self.finding_type,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
            "subject_ref": self.subject_ref,
            "created_at": self.created_at,
            "finding_attrs": dict(self.finding_attrs),
        }


@dataclass(frozen=True)
class ExecutionResultPromotionResult:
    result_id: str
    candidate_id: str
    envelope_id: str
    review_request_id: str | None
    decision_id: str | None
    status: str
    promoted: bool
    canonical_promotion_enabled: bool
    finding_ids: list[str]
    summary: str
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "candidate_id": self.candidate_id,
            "envelope_id": self.envelope_id,
            "review_request_id": self.review_request_id,
            "decision_id": self.decision_id,
            "status": self.status,
            "promoted": self.promoted,
            "canonical_promotion_enabled": self.canonical_promotion_enabled,
            "finding_ids": list(self.finding_ids),
            "summary": self.summary,
            "created_at": self.created_at,
            "result_attrs": dict(self.result_attrs),
        }


class ExecutionResultPromotionService:
    def __init__(
        self,
        *,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        self.ocel_store = ocel_store or OCELStore()
        self.trace_service = trace_service or TraceService(ocel_store=self.ocel_store)
        self.last_policy: ExecutionResultPromotionPolicy | None = None
        self.last_candidate: ExecutionResultPromotionCandidate | None = None
        self.last_review_request: ExecutionResultPromotionReviewRequest | None = None
        self.last_decision: ExecutionResultPromotionDecision | None = None
        self.last_findings: list[ExecutionResultPromotionFinding] = []
        self.last_result: ExecutionResultPromotionResult | None = None

    def create_default_policy(
        self,
        *,
        policy_name: str = "Default Execution Result Promotion Policy",
    ) -> ExecutionResultPromotionPolicy:
        policy = ExecutionResultPromotionPolicy(
            policy_id=new_execution_result_promotion_policy_id(),
            policy_name=policy_name,
            allowed_target_kinds=list(ALLOWED_TARGET_KINDS),
            denied_target_kinds=list(DENIED_TARGET_KINDS),
            require_review=True,
            allow_canonical_promotion=False,
            allow_private_candidate=True,
            max_preview_chars=2000,
            status="active",
            created_at=utc_now_iso(),
            policy_attrs={
                "review_only": True,
                "canonical_promotion_enabled": False,
                "memory_entries_written": False,
                "persona_updated": False,
                "overlay_updated": False,
            },
        )
        self.last_policy = policy
        self._record(
            "execution_result_promotion_policy_registered",
            objects=[_object("execution_result_promotion_policy", policy.policy_id, policy.to_dict())],
            links=[("execution_result_promotion_policy_object", policy.policy_id)],
            object_links=[],
            attrs={"status": policy.status},
        )
        return policy

    def create_candidate_from_envelope(
        self,
        *,
        envelope: ExecutionEnvelope,
        output_snapshot: ExecutionOutputSnapshot | None = None,
        outcome_summary: ExecutionOutcomeSummary | None = None,
        artifact_ref: ExecutionArtifactRef | None = None,
        target_kind: str,
        candidate_title: str | None = None,
        private: bool = False,
        policy: ExecutionResultPromotionPolicy | None = None,
    ) -> ExecutionResultPromotionResult:
        self.last_findings = []
        active_policy = policy or self.create_default_policy()
        denied = target_kind in active_policy.denied_target_kinds
        unsupported = target_kind not in active_policy.allowed_target_kinds
        source_ref_kind, source_ref_id, preview, candidate_hash = _candidate_source(
            output_snapshot=output_snapshot,
            artifact_ref=artifact_ref,
            max_preview_chars=active_policy.max_preview_chars,
        )
        sensitive = private or _preview_has_sensitive_marker(preview)
        candidate = ExecutionResultPromotionCandidate(
            candidate_id=new_execution_result_promotion_candidate_id(),
            envelope_id=envelope.envelope_id,
            outcome_summary_id=outcome_summary.summary_id if outcome_summary else None,
            output_snapshot_id=output_snapshot.output_snapshot_id if output_snapshot else None,
            artifact_ref_id=artifact_ref.artifact_ref_id if artifact_ref else None,
            target_kind=target_kind,
            candidate_title=candidate_title or f"Execution result candidate for {target_kind}",
            candidate_preview=preview,
            candidate_hash=candidate_hash,
            source_ref_kind=source_ref_kind,
            source_ref_id=source_ref_id,
            private=private,
            sensitive=sensitive,
            review_status="rejected" if denied or unsupported else "pending_review",
            canonical_promotion_enabled=False,
            created_at=utc_now_iso(),
            candidate_attrs={
                "review_only": True,
                "full_raw_body_copied": False,
                "memory_entries_written": False,
                "persona_updated": False,
                "overlay_updated": False,
            },
        )
        self.last_candidate = candidate
        self._record_candidate(candidate, envelope, output_snapshot, outcome_summary, artifact_ref)
        if active_policy.require_review and not denied and not unsupported:
            self.record_finding(
                candidate=candidate,
                finding_type="review_required",
                status="pending_review",
                severity="medium",
                message="Promotion candidate requires review before any later promotion workflow.",
                subject_ref=candidate.candidate_id,
            )
        if output_snapshot is None and artifact_ref is None:
            self.record_finding(
                candidate=candidate,
                finding_type="full_output_not_available",
                status="preview_only",
                severity="low",
                message="No output snapshot or artifact reference was provided.",
                subject_ref=envelope.envelope_id,
            )
        if private or sensitive:
            self.record_finding(
                candidate=candidate,
                finding_type="private_content_risk",
                status="needs_review",
                severity="high",
                message="Candidate is marked private or sensitive and requires careful review.",
                subject_ref=candidate.candidate_id,
            )
        if denied or unsupported:
            self.record_finding(
                candidate=candidate,
                finding_type="target_kind_denied" if denied else "target_kind_unsupported",
                status="rejected",
                severity="high",
                message="Target kind is not allowed for promotion candidates.",
                subject_ref=target_kind,
            )
        status = "rejected" if denied or unsupported else "pending_review"
        return self.record_result(
            candidate=candidate,
            status=status,
            review_request=None,
            decision=None,
            summary=f"Promotion candidate {status}.",
        )

    def create_review_request(
        self,
        *,
        candidate: ExecutionResultPromotionCandidate,
        requested_by: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
    ) -> ExecutionResultPromotionReviewRequest:
        request = ExecutionResultPromotionReviewRequest(
            review_request_id=new_execution_result_promotion_review_request_id(),
            candidate_id=candidate.candidate_id,
            envelope_id=candidate.envelope_id,
            requested_by=requested_by,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            status="pending_review",
            created_at=utc_now_iso(),
            request_attrs={"review_only": True, "canonical_promotion_enabled": False},
        )
        self.last_review_request = request
        self._record(
            "execution_result_promotion_review_requested",
            objects=[_object("execution_result_promotion_review_request", request.review_request_id, request.to_dict())],
            links=[
                ("execution_result_promotion_review_request_object", request.review_request_id),
                ("execution_result_promotion_candidate_object", candidate.candidate_id),
            ],
            object_links=[(request.review_request_id, candidate.candidate_id, "reviews_candidate")],
            attrs={"status": request.status},
        )
        return request

    def record_finding(
        self,
        *,
        candidate: ExecutionResultPromotionCandidate,
        finding_type: str,
        status: str,
        severity: str,
        message: str,
        subject_ref: str | None = None,
        finding_attrs: dict[str, Any] | None = None,
    ) -> ExecutionResultPromotionFinding:
        finding = ExecutionResultPromotionFinding(
            finding_id=new_execution_result_promotion_finding_id(),
            candidate_id=candidate.candidate_id,
            envelope_id=candidate.envelope_id,
            finding_type=finding_type,
            status=status,
            severity=severity,
            message=message,
            subject_ref=subject_ref,
            created_at=utc_now_iso(),
            finding_attrs={
                "canonical_promotion_enabled": False,
                "promoted": False,
                **dict(finding_attrs or {}),
            },
        )
        self.last_findings.append(finding)
        self._record(
            "execution_result_promotion_finding_recorded",
            objects=[_object("execution_result_promotion_finding", finding.finding_id, finding.to_dict())],
            links=[
                ("execution_result_promotion_finding_object", finding.finding_id),
                ("execution_result_promotion_candidate_object", candidate.candidate_id),
            ],
            object_links=[(finding.finding_id, candidate.candidate_id, "belongs_to_candidate")],
            attrs={"finding_type": finding.finding_type, "status": finding.status},
        )
        return finding

    def record_decision(
        self,
        *,
        review_request: ExecutionResultPromotionReviewRequest,
        candidate: ExecutionResultPromotionCandidate,
        decision: str,
        reviewer_type: str | None = None,
        reviewer_id: str | None = None,
        reason: str | None = None,
        approved_target_kind: str | None = None,
    ) -> ExecutionResultPromotionDecision:
        normalized = normalize_promotion_decision(decision)
        item = ExecutionResultPromotionDecision(
            decision_id=new_execution_result_promotion_decision_id(),
            review_request_id=review_request.review_request_id,
            candidate_id=candidate.candidate_id,
            decision=normalized,
            reviewer_type=reviewer_type,
            reviewer_id=reviewer_id,
            reason=reason,
            approved_target_kind=approved_target_kind if normalized == "approved_for_later_promotion" else None,
            can_promote_now=False,
            requires_manual_action=normalized == "approved_for_later_promotion",
            created_at=utc_now_iso(),
            decision_attrs={
                "canonical_promotion_enabled": False,
                "promoted": False,
            },
        )
        self.last_decision = item
        self._record(
            "execution_result_promotion_decision_recorded",
            objects=[_object("execution_result_promotion_decision", item.decision_id, item.to_dict())],
            links=[
                ("execution_result_promotion_decision_object", item.decision_id),
                ("execution_result_promotion_review_request_object", review_request.review_request_id),
            ],
            object_links=[(item.decision_id, review_request.review_request_id, "decides_review_request")],
            attrs={"decision": item.decision},
        )
        if item.decision == "approved_for_later_promotion":
            self._record_status_event("execution_result_promotion_approved_for_later", item.decision_id, item.to_dict())
        elif item.decision == "rejected":
            self._record_status_event("execution_result_promotion_rejected", item.decision_id, item.to_dict())
        elif item.decision == "no_action":
            self._record_status_event("execution_result_promotion_no_action_selected", item.decision_id, item.to_dict())
        return item

    def record_result(
        self,
        *,
        candidate: ExecutionResultPromotionCandidate,
        status: str,
        review_request: ExecutionResultPromotionReviewRequest | None,
        decision: ExecutionResultPromotionDecision | None,
        summary: str,
    ) -> ExecutionResultPromotionResult:
        result = ExecutionResultPromotionResult(
            result_id=new_execution_result_promotion_result_id(),
            candidate_id=candidate.candidate_id,
            envelope_id=candidate.envelope_id,
            review_request_id=review_request.review_request_id if review_request else None,
            decision_id=decision.decision_id if decision else None,
            status=status,
            promoted=False,
            canonical_promotion_enabled=False,
            finding_ids=[finding.finding_id for finding in self.last_findings],
            summary=summary,
            created_at=utc_now_iso(),
            result_attrs={
                "target_kind": candidate.target_kind,
                "canonical_promotion_enabled": False,
                "promoted": False,
                "memory_entries_written": False,
                "persona_updated": False,
                "overlay_updated": False,
            },
        )
        self.last_result = result
        links = [
            ("execution_result_promotion_result_object", result.result_id),
            ("execution_result_promotion_candidate_object", candidate.candidate_id),
        ]
        if review_request:
            links.append(("execution_result_promotion_review_request_object", review_request.review_request_id))
        if decision:
            links.append(("execution_result_promotion_decision_object", decision.decision_id))
        self._record(
            "execution_result_promotion_result_recorded",
            objects=[_object("execution_result_promotion_result", result.result_id, result.to_dict())],
            links=links,
            object_links=[(result.result_id, candidate.candidate_id, "summarizes_candidate")],
            attrs={"status": result.status},
        )
        return result

    def review_candidate(
        self,
        *,
        candidate: ExecutionResultPromotionCandidate,
        decision: str,
        reviewer_type: str | None = None,
        reviewer_id: str | None = None,
        reason: str | None = None,
        approved_target_kind: str | None = None,
        requested_by: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
    ) -> ExecutionResultPromotionResult:
        self.last_findings = []
        request = self.create_review_request(
            candidate=candidate,
            requested_by=requested_by,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
        )
        item = self.record_decision(
            review_request=request,
            candidate=candidate,
            decision=decision,
            reviewer_type=reviewer_type,
            reviewer_id=reviewer_id,
            reason=reason,
            approved_target_kind=approved_target_kind or candidate.target_kind,
        )
        status = "archived" if item.decision == "archive" else item.decision
        return self.record_result(
            candidate=candidate,
            status=status,
            review_request=request,
            decision=item,
            summary=f"Promotion review decision recorded: {status}.",
        )

    def list_candidates(self, *, limit: int = 20) -> list[ExecutionResultPromotionCandidate]:
        rows = self.ocel_store.fetch_objects_by_type("execution_result_promotion_candidate")
        candidates = [candidate_from_dict(row["object_attrs"]) for row in rows]
        return sorted(candidates, key=lambda item: item.created_at, reverse=True)[: max(1, min(limit, 100))]

    def show_candidate(self, candidate_id: str) -> ExecutionResultPromotionCandidate | None:
        for candidate in self.list_candidates(limit=100):
            if candidate.candidate_id == candidate_id:
                return candidate
        return None

    def render_candidate_summary(self, result: ExecutionResultPromotionResult | None = None) -> str:
        item = result or self.last_result
        candidate = self.last_candidate
        if item is None:
            return "Execution Result Promotion: unavailable"
        lines = [
            "Execution Result Promotion",
            f"status={item.status}",
            f"result_id={item.result_id}",
            f"candidate_id={item.candidate_id}",
            f"promoted={str(item.promoted).lower()}",
            f"canonical_promotion_enabled={str(item.canonical_promotion_enabled).lower()}",
        ]
        if candidate is not None:
            lines.extend(
                [
                    f"target_kind={candidate.target_kind}",
                    f"review_status={candidate.review_status}",
                    f"source_ref={candidate.source_ref_kind}:{candidate.source_ref_id or 'none'}",
                    f"candidate_preview={candidate.candidate_preview}",
                ]
            )
        return "\n".join(lines)

    def render_promotion_cli(self, result: ExecutionResultPromotionResult | None = None) -> str:
        return self.render_candidate_summary(result)

    def _record_candidate(
        self,
        candidate: ExecutionResultPromotionCandidate,
        envelope: ExecutionEnvelope,
        output_snapshot: ExecutionOutputSnapshot | None,
        outcome_summary: ExecutionOutcomeSummary | None,
        artifact_ref: ExecutionArtifactRef | None,
    ) -> None:
        links = [
            ("execution_result_promotion_candidate_object", candidate.candidate_id),
            ("execution_envelope_object", envelope.envelope_id),
        ]
        object_links = [(candidate.candidate_id, envelope.envelope_id, "derived_from_execution_envelope")]
        if output_snapshot:
            links.append(("execution_output_snapshot_object", output_snapshot.output_snapshot_id))
            object_links.append((candidate.candidate_id, output_snapshot.output_snapshot_id, "uses_output_snapshot"))
        if outcome_summary:
            links.append(("execution_outcome_summary_object", outcome_summary.summary_id))
            object_links.append((candidate.candidate_id, outcome_summary.summary_id, "uses_outcome_summary"))
        if artifact_ref:
            links.append(("execution_artifact_ref_object", artifact_ref.artifact_ref_id))
            object_links.append((candidate.candidate_id, artifact_ref.artifact_ref_id, "uses_artifact_ref"))
        self._record(
            "execution_result_promotion_candidate_created",
            objects=[_object("execution_result_promotion_candidate", candidate.candidate_id, candidate.to_dict())],
            links=links,
            object_links=object_links,
            attrs={"target_kind": candidate.target_kind, "review_status": candidate.review_status},
        )

    def _record_status_event(self, activity: str, object_id: str, attrs: dict[str, Any]) -> None:
        self._record(
            activity,
            objects=[_object("execution_result_promotion_decision", object_id, attrs)],
            links=[("execution_result_promotion_decision_object", object_id)],
            object_links=[],
            attrs={"decision": attrs.get("decision")},
        )

    def _record(
        self,
        activity: str,
        *,
        objects: list[OCELObject],
        links: list[tuple[str, str]],
        object_links: list[tuple[str, str, str]],
        attrs: dict[str, Any],
    ) -> None:
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity=activity,
            event_timestamp=utc_now_iso(),
            event_attrs={
                **attrs,
                "runtime_event_type": activity,
                "source_runtime": "chanta_core",
                "execution_result_promotion": True,
                "review_only": True,
                "canonical_promotion_enabled": False,
                "promoted": False,
                "memory_entries_written": False,
                "persona_updated": False,
                "overlay_updated": False,
                "skills_executed": False,
                "permission_grants_created": False,
            },
        )
        relations = [
            OCELRelation.event_object(event_id=event.event_id, object_id=object_id, qualifier=qualifier)
            for qualifier, object_id in links
            if object_id
        ]
        relations.extend(
            OCELRelation.object_object(source_object_id=source_id, target_object_id=target_id, qualifier=qualifier)
            for source_id, target_id, qualifier in object_links
            if source_id and target_id
        )
        self.trace_service.record_session_ocel_record(OCELRecord(event=event, objects=objects, relations=relations))


def normalize_promotion_decision(value: str) -> str:
    aliases = {
        "approve": "approved_for_later_promotion",
        "approved": "approved_for_later_promotion",
        "approved-for-later": "approved_for_later_promotion",
        "reject": "rejected",
        "no-action": "no_action",
        "more-info": "needs_more_info",
        "needs-more-info": "needs_more_info",
        "archived": "archive",
    }
    normalized = aliases.get(value, value)
    if normalized not in ALLOWED_DECISIONS:
        return "error"
    return normalized


def envelope_from_dict(value: dict[str, Any]) -> ExecutionEnvelope:
    return ExecutionEnvelope(
        envelope_id=str(value["envelope_id"]),
        execution_kind=str(value.get("execution_kind") or "unknown"),
        execution_subject_id=value.get("execution_subject_id"),
        skill_id=value.get("skill_id"),
        session_id=value.get("session_id"),
        turn_id=value.get("turn_id"),
        process_instance_id=value.get("process_instance_id"),
        status=str(value.get("status") or "unknown"),
        execution_allowed=bool(value.get("execution_allowed")),
        execution_performed=bool(value.get("execution_performed")),
        blocked=bool(value.get("blocked")),
        started_at=value.get("started_at"),
        completed_at=value.get("completed_at"),
        created_at=str(value.get("created_at") or utc_now_iso()),
        envelope_attrs=dict(value.get("envelope_attrs") or {}),
    )


def output_snapshot_from_dict(value: dict[str, Any] | None) -> ExecutionOutputSnapshot | None:
    if not isinstance(value, dict):
        return None
    return ExecutionOutputSnapshot(
        output_snapshot_id=str(value["output_snapshot_id"]),
        envelope_id=str(value["envelope_id"]),
        output_kind=str(value.get("output_kind") or "execution_output"),
        output_preview=dict(value.get("output_preview") or {}),
        output_hash=value.get("output_hash"),
        output_ref=value.get("output_ref"),
        truncated=bool(value.get("truncated")),
        redacted_fields=list(value.get("redacted_fields") or []),
        full_output_stored=bool(value.get("full_output_stored")),
        created_at=str(value.get("created_at") or utc_now_iso()),
        output_attrs=dict(value.get("output_attrs") or {}),
    )


def outcome_summary_from_dict(value: dict[str, Any] | None) -> ExecutionOutcomeSummary | None:
    if not isinstance(value, dict):
        return None
    return ExecutionOutcomeSummary(
        summary_id=str(value["summary_id"]),
        envelope_id=str(value["envelope_id"]),
        status=str(value.get("status") or "unknown"),
        succeeded=bool(value.get("succeeded")),
        blocked=bool(value.get("blocked")),
        failed=bool(value.get("failed")),
        skipped=bool(value.get("skipped")),
        violation_ids=list(value.get("violation_ids") or []),
        finding_ids=list(value.get("finding_ids") or []),
        output_snapshot_id=value.get("output_snapshot_id"),
        reason=value.get("reason"),
        created_at=str(value.get("created_at") or utc_now_iso()),
        summary_attrs=dict(value.get("summary_attrs") or {}),
    )


def artifact_ref_from_dict(value: dict[str, Any] | None) -> ExecutionArtifactRef | None:
    if not isinstance(value, dict):
        return None
    return ExecutionArtifactRef(
        artifact_ref_id=str(value["artifact_ref_id"]),
        envelope_id=str(value["envelope_id"]),
        artifact_kind=str(value.get("artifact_kind") or "artifact"),
        artifact_ref=str(value.get("artifact_ref") or ""),
        artifact_hash=value.get("artifact_hash"),
        artifact_preview=dict(value.get("artifact_preview") or {}),
        private=bool(value.get("private")),
        created_at=str(value.get("created_at") or utc_now_iso()),
        artifact_attrs=dict(value.get("artifact_attrs") or {}),
    )


def candidate_from_dict(value: dict[str, Any]) -> ExecutionResultPromotionCandidate:
    return ExecutionResultPromotionCandidate(
        candidate_id=str(value["candidate_id"]),
        envelope_id=str(value["envelope_id"]),
        outcome_summary_id=value.get("outcome_summary_id"),
        output_snapshot_id=value.get("output_snapshot_id"),
        artifact_ref_id=value.get("artifact_ref_id"),
        target_kind=str(value.get("target_kind") or "other"),
        candidate_title=str(value.get("candidate_title") or "Execution result candidate"),
        candidate_preview=dict(value.get("candidate_preview") or {}),
        candidate_hash=value.get("candidate_hash"),
        source_ref_kind=str(value.get("source_ref_kind") or "none"),
        source_ref_id=value.get("source_ref_id"),
        private=bool(value.get("private")),
        sensitive=bool(value.get("sensitive")),
        review_status=str(value.get("review_status") or "pending_review"),
        canonical_promotion_enabled=bool(value.get("canonical_promotion_enabled")),
        created_at=str(value.get("created_at") or utc_now_iso()),
        candidate_attrs=dict(value.get("candidate_attrs") or {}),
    )


def _candidate_source(
    *,
    output_snapshot: ExecutionOutputSnapshot | None,
    artifact_ref: ExecutionArtifactRef | None,
    max_preview_chars: int,
) -> tuple[str, str | None, dict[str, Any], str | None]:
    if output_snapshot is not None:
        return (
            "execution_output_snapshot",
            output_snapshot.output_snapshot_id,
            _trim_preview(output_snapshot.output_preview, max_preview_chars),
            output_snapshot.output_hash,
        )
    if artifact_ref is not None:
        return (
            "execution_artifact_ref",
            artifact_ref.artifact_ref_id,
            _trim_preview(artifact_ref.artifact_preview, max_preview_chars),
            artifact_ref.artifact_hash,
        )
    return "execution_envelope", None, {"preview": "<UNAVAILABLE>"}, None


def _trim_preview(value: dict[str, Any], max_chars: int) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, item in value.items():
        if isinstance(item, str):
            result[str(key)] = item[:max_chars]
        else:
            result[str(key)] = item
    return result


def _preview_has_sensitive_marker(value: dict[str, Any]) -> bool:
    raw = str(value).lower()
    return "<redacted>" in raw or "secret" in raw or "token" in raw


def _object(object_type: str, object_id: str, attrs: dict[str, Any]) -> OCELObject:
    return OCELObject(
        object_id=object_id,
        object_type=object_type,
        object_attrs={
            "object_key": object_id,
            "display_name": object_id,
            **attrs,
        },
    )
