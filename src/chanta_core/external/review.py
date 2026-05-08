from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any
from uuid import uuid4

from chanta_core.external.errors import (
    ExternalAdapterReviewChecklistError,
    ExternalAdapterReviewDecisionError,
    ExternalAdapterReviewFindingError,
    ExternalAdapterReviewItemError,
    ExternalAdapterReviewQueueError,
)
from chanta_core.external.ids import (
    new_external_adapter_review_checklist_id,
    new_external_adapter_review_decision_id,
    new_external_adapter_review_finding_id,
    new_external_adapter_review_item_id,
    new_external_adapter_review_queue_id,
)
from chanta_core.external.models import (
    ExternalAssimilationCandidate,
    ExternalCapabilityDescriptor,
    ExternalCapabilityRiskNote,
)
from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


QUEUE_TYPES = {"external_capability", "adapter", "mcp_descriptor", "plugin_descriptor", "manual", "other"}
QUEUE_STATUSES = {"active", "paused", "closed", "archived"}
ITEM_STATUSES = {"pending_review", "in_review", "needs_more_info", "approved_for_design", "rejected", "archived"}
CHECKLIST_TYPES = {"safety", "permission", "sandbox", "risk", "descriptor_quality", "manual", "other"}
CHECKLIST_STATUSES = {"open", "completed", "failed", "needs_review", "skipped"}
FINDING_TYPES = {
    "risk",
    "missing_descriptor_field",
    "permission_concern",
    "sandbox_concern",
    "runtime_activation_concern",
    "external_code_concern",
    "network_concern",
    "credential_concern",
    "manual_note",
    "other",
}
FINDING_STATUSES = {"open", "resolved", "accepted_risk", "dismissed", "informational"}
FINDING_SEVERITIES = {"info", "low", "medium", "high", "critical"}
DECISIONS = {"approved_for_design", "rejected", "needs_more_info", "defer", "archive"}
REQUIRED_CHECKS = [
    "descriptor_has_name",
    "descriptor_has_type",
    "candidate_disabled",
    "execution_disabled",
    "review_status_pending",
    "risk_notes_reviewed",
    "permissions_declared_or_empty",
    "no_runtime_activation",
]
_ACTIVE = "active"


def _require_value(value: str, allowed: set[str], error_type: type[Exception], field_name: str) -> None:
    if value not in allowed:
        raise error_type(f"Unsupported {field_name}: {value}")


@dataclass(frozen=True)
class ExternalAdapterReviewQueue:
    queue_id: str
    queue_name: str
    queue_type: str
    status: str
    created_at: str
    updated_at: str
    item_ids: list[str] = field(default_factory=list)
    queue_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.queue_name:
            raise ExternalAdapterReviewQueueError("queue_name is required")
        _require_value(self.queue_type, QUEUE_TYPES, ExternalAdapterReviewQueueError, "queue_type")
        _require_value(self.status, QUEUE_STATUSES, ExternalAdapterReviewQueueError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "queue_id": self.queue_id,
            "queue_name": self.queue_name,
            "queue_type": self.queue_type,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "item_ids": self.item_ids,
            "queue_attrs": self.queue_attrs,
        }


@dataclass(frozen=True)
class ExternalAdapterReviewItem:
    item_id: str
    queue_id: str
    candidate_id: str
    descriptor_id: str | None
    source_id: str | None
    risk_note_ids: list[str]
    priority: int | None
    review_status: str
    assigned_reviewer: str | None
    created_at: str
    updated_at: str
    item_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.queue_id:
            raise ExternalAdapterReviewItemError("queue_id is required")
        if not self.candidate_id:
            raise ExternalAdapterReviewItemError("candidate_id is required")
        _require_value(self.review_status, ITEM_STATUSES, ExternalAdapterReviewItemError, "review_status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "queue_id": self.queue_id,
            "candidate_id": self.candidate_id,
            "descriptor_id": self.descriptor_id,
            "source_id": self.source_id,
            "risk_note_ids": self.risk_note_ids,
            "priority": self.priority,
            "review_status": self.review_status,
            "assigned_reviewer": self.assigned_reviewer,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "item_attrs": self.item_attrs,
        }


@dataclass(frozen=True)
class ExternalAdapterReviewChecklist:
    checklist_id: str
    item_id: str
    checklist_type: str
    required_checks: list[str]
    completed_checks: list[str]
    failed_checks: list[str]
    status: str
    created_at: str
    updated_at: str
    checklist_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.item_id:
            raise ExternalAdapterReviewChecklistError("item_id is required")
        _require_value(self.checklist_type, CHECKLIST_TYPES, ExternalAdapterReviewChecklistError, "checklist_type")
        _require_value(self.status, CHECKLIST_STATUSES, ExternalAdapterReviewChecklistError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "checklist_id": self.checklist_id,
            "item_id": self.item_id,
            "checklist_type": self.checklist_type,
            "required_checks": self.required_checks,
            "completed_checks": self.completed_checks,
            "failed_checks": self.failed_checks,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "checklist_attrs": self.checklist_attrs,
        }


@dataclass(frozen=True)
class ExternalAdapterReviewFinding:
    finding_id: str
    item_id: str
    finding_type: str
    status: str
    severity: str | None
    message: str
    source_kind: str | None
    source_ref: str | None
    created_at: str
    finding_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.item_id:
            raise ExternalAdapterReviewFindingError("item_id is required")
        if not self.message:
            raise ExternalAdapterReviewFindingError("message is required")
        _require_value(self.finding_type, FINDING_TYPES, ExternalAdapterReviewFindingError, "finding_type")
        _require_value(self.status, FINDING_STATUSES, ExternalAdapterReviewFindingError, "status")
        if self.severity is not None:
            _require_value(self.severity, FINDING_SEVERITIES, ExternalAdapterReviewFindingError, "severity")

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "item_id": self.item_id,
            "finding_type": self.finding_type,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
            "source_kind": self.source_kind,
            "source_ref": self.source_ref,
            "created_at": self.created_at,
            "finding_attrs": self.finding_attrs,
        }


@dataclass(frozen=True)
class ExternalAdapterReviewDecision:
    decision_id: str
    item_id: str
    queue_id: str
    candidate_id: str
    decision: str
    decided_by: str | None
    decision_reason: str | None
    finding_ids: list[str]
    checklist_id: str | None
    activation_allowed: bool
    runtime_registration_allowed: bool
    execution_enabled_after_decision: bool
    created_at: str
    decision_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.item_id:
            raise ExternalAdapterReviewDecisionError("item_id is required")
        if not self.queue_id:
            raise ExternalAdapterReviewDecisionError("queue_id is required")
        if not self.candidate_id:
            raise ExternalAdapterReviewDecisionError("candidate_id is required")
        _require_value(self.decision, DECISIONS, ExternalAdapterReviewDecisionError, "decision")
        if self.activation_allowed is not False:
            raise ExternalAdapterReviewDecisionError("activation_allowed must be False in v0.14.2")
        if self.runtime_registration_allowed is not False:
            raise ExternalAdapterReviewDecisionError("runtime_registration_allowed must be False in v0.14.2")
        if self.execution_enabled_after_decision is not False:
            raise ExternalAdapterReviewDecisionError("execution_enabled_after_decision must be False in v0.14.2")

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "item_id": self.item_id,
            "queue_id": self.queue_id,
            "candidate_id": self.candidate_id,
            "decision": self.decision,
            "decided_by": self.decided_by,
            "decision_reason": self.decision_reason,
            "finding_ids": self.finding_ids,
            "checklist_id": self.checklist_id,
            "activation_allowed": self.activation_allowed,
            "runtime_registration_allowed": self.runtime_registration_allowed,
            "execution_enabled_after_decision": self.execution_enabled_after_decision,
            "created_at": self.created_at,
            "decision_attrs": self.decision_attrs,
        }


class ExternalAdapterReviewService:
    def __init__(
        self,
        *,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        if trace_service is not None:
            self.trace_service = trace_service
        elif ocel_store is not None:
            self.trace_service = TraceService(ocel_store=ocel_store)
        else:
            self.trace_service = TraceService()

    def create_review_queue(
        self,
        *,
        queue_name: str,
        queue_type: str = "external_capability",
        status: str = "active",
        queue_attrs: dict[str, Any] | None = None,
    ) -> ExternalAdapterReviewQueue:
        now = utc_now_iso()
        queue = ExternalAdapterReviewQueue(
            queue_id=new_external_adapter_review_queue_id(),
            queue_name=queue_name,
            queue_type=queue_type,
            status=status,
            created_at=now,
            updated_at=now,
            item_ids=[],
            queue_attrs=dict(queue_attrs or {}),
        )
        self._record(
            "external_adapter_review_queue_created",
            queue=queue,
            attrs={"queue_type": queue.queue_type, "status": queue.status},
            links=[("queue_object", queue.queue_id)],
            object_links=[],
        )
        return queue

    def create_review_item(
        self,
        *,
        queue_id: str,
        candidate: ExternalAssimilationCandidate,
        descriptor_id: str | None = None,
        source_id: str | None = None,
        risk_note_ids: list[str] | None = None,
        priority: int | None = None,
        assigned_reviewer: str | None = None,
        item_attrs: dict[str, Any] | None = None,
    ) -> ExternalAdapterReviewItem:
        now = utc_now_iso()
        attrs = dict(item_attrs or {})
        if candidate.execution_enabled is True:
            attrs["candidate_execution_enabled_detected"] = True
        if candidate.activation_status == _ACTIVE:
            attrs["candidate_activation_enabled_detected"] = True
        item = ExternalAdapterReviewItem(
            item_id=new_external_adapter_review_item_id(),
            queue_id=queue_id,
            candidate_id=candidate.candidate_id,
            descriptor_id=descriptor_id or candidate.descriptor_id,
            source_id=source_id or candidate.source_id,
            risk_note_ids=list(risk_note_ids or candidate.linked_risk_note_ids),
            priority=priority,
            review_status="pending_review",
            assigned_reviewer=assigned_reviewer,
            created_at=now,
            updated_at=now,
            item_attrs=attrs,
        )
        self._record(
            "external_adapter_review_item_created",
            item=item,
            candidate_id=item.candidate_id,
            descriptor_id=item.descriptor_id,
            risk_note_ids=item.risk_note_ids,
            attrs={"review_status": item.review_status, "activation_allowed": False},
            links=[
                ("item_object", item.item_id),
                ("queue_object", item.queue_id),
                ("candidate_object", item.candidate_id),
                ("descriptor_object", item.descriptor_id or ""),
            ]
            + [("risk_note_object", note_id) for note_id in item.risk_note_ids],
            object_links=[
                (item.item_id, item.queue_id, "belongs_to_queue"),
                (item.item_id, item.candidate_id, "reviews_candidate"),
                (item.item_id, item.descriptor_id or "", "reviews_descriptor"),
            ]
            + [(item.item_id, note_id, "references_risk_note") for note_id in item.risk_note_ids],
        )
        return item

    def assign_review_item(
        self,
        *,
        item: ExternalAdapterReviewItem,
        assigned_reviewer: str,
        reason: str | None = None,
    ) -> ExternalAdapterReviewItem:
        updated = replace(
            item,
            assigned_reviewer=assigned_reviewer,
            updated_at=utc_now_iso(),
            item_attrs={**item.item_attrs, "assignment_reason": reason},
        )
        self._record(
            "external_adapter_review_item_assigned",
            item=updated,
            attrs={"assigned_reviewer": assigned_reviewer, "reason": reason},
            links=[("item_object", updated.item_id), ("queue_object", updated.queue_id)],
            object_links=[(updated.item_id, updated.queue_id, "belongs_to_queue")],
        )
        return updated

    def update_review_item_status(
        self,
        *,
        item: ExternalAdapterReviewItem,
        review_status: str,
        reason: str | None = None,
    ) -> ExternalAdapterReviewItem:
        _require_value(review_status, ITEM_STATUSES, ExternalAdapterReviewItemError, "review_status")
        updated = replace(
            item,
            review_status=review_status,
            updated_at=utc_now_iso(),
            item_attrs={**item.item_attrs, "status_reason": reason},
        )
        self._record(
            "external_adapter_review_item_status_updated",
            item=updated,
            attrs={"review_status": review_status, "reason": reason, "activation_allowed": False},
            links=[("item_object", updated.item_id), ("queue_object", updated.queue_id)],
            object_links=[(updated.item_id, updated.queue_id, "belongs_to_queue")],
        )
        return updated

    def build_default_checklist_for_candidate(
        self,
        *,
        item: ExternalAdapterReviewItem,
        candidate: ExternalAssimilationCandidate,
        descriptor: ExternalCapabilityDescriptor | None = None,
        risk_notes: list[ExternalCapabilityRiskNote] | None = None,
    ) -> ExternalAdapterReviewChecklist:
        completed: list[str] = []
        failed: list[str] = []
        _add_check(completed, failed, "descriptor_has_name", descriptor is not None and bool(descriptor.capability_name))
        _add_check(completed, failed, "descriptor_has_type", descriptor is not None and bool(descriptor.capability_type))
        _add_check(completed, failed, "candidate_disabled", candidate.activation_status != _ACTIVE)
        _add_check(completed, failed, "execution_disabled", candidate.execution_enabled is False)
        _add_check(completed, failed, "review_status_pending", item.review_status == "pending_review")
        _add_check(completed, failed, "risk_notes_reviewed", bool(risk_notes))
        _add_check(completed, failed, "permissions_declared_or_empty", True)
        _add_check(completed, failed, "no_runtime_activation", True)
        now = utc_now_iso()
        checklist = ExternalAdapterReviewChecklist(
            checklist_id=new_external_adapter_review_checklist_id(),
            item_id=item.item_id,
            checklist_type="safety",
            required_checks=list(REQUIRED_CHECKS),
            completed_checks=completed,
            failed_checks=failed,
            status="completed" if not failed else "needs_review",
            created_at=now,
            updated_at=now,
            checklist_attrs={"candidate_id": candidate.candidate_id, "descriptor_id": item.descriptor_id},
        )
        self._record(
            "external_adapter_review_checklist_created",
            item=item,
            checklist=checklist,
            attrs={"status": checklist.status, "failed_checks": checklist.failed_checks},
            links=[("checklist_object", checklist.checklist_id), ("item_object", item.item_id)],
            object_links=[(checklist.checklist_id, item.item_id, "belongs_to_review_item")],
        )
        return checklist

    def update_checklist(
        self,
        *,
        checklist: ExternalAdapterReviewChecklist,
        completed_checks: list[str] | None = None,
        failed_checks: list[str] | None = None,
        status: str | None = None,
        reason: str | None = None,
    ) -> ExternalAdapterReviewChecklist:
        if status is not None:
            _require_value(status, CHECKLIST_STATUSES, ExternalAdapterReviewChecklistError, "status")
        updated = replace(
            checklist,
            completed_checks=list(completed_checks if completed_checks is not None else checklist.completed_checks),
            failed_checks=list(failed_checks if failed_checks is not None else checklist.failed_checks),
            status=status or checklist.status,
            updated_at=utc_now_iso(),
            checklist_attrs={**checklist.checklist_attrs, "update_reason": reason},
        )
        self._record(
            "external_adapter_review_checklist_updated",
            checklist=updated,
            attrs={"status": updated.status, "reason": reason},
            links=[("checklist_object", updated.checklist_id), ("item_object", updated.item_id)],
            object_links=[(updated.checklist_id, updated.item_id, "belongs_to_review_item")],
        )
        return updated

    def record_finding(
        self,
        *,
        item_id: str,
        finding_type: str,
        message: str,
        status: str = "open",
        severity: str | None = None,
        source_kind: str | None = None,
        source_ref: str | None = None,
        finding_attrs: dict[str, Any] | None = None,
    ) -> ExternalAdapterReviewFinding:
        finding = ExternalAdapterReviewFinding(
            finding_id=new_external_adapter_review_finding_id(),
            item_id=item_id,
            finding_type=finding_type,
            status=status,
            severity=severity,
            message=message,
            source_kind=source_kind,
            source_ref=source_ref,
            created_at=utc_now_iso(),
            finding_attrs=dict(finding_attrs or {}),
        )
        risk_note_links = [("risk_note_object", source_ref)] if source_kind == "risk_note" and source_ref else []
        self._record(
            "external_adapter_review_finding_recorded",
            finding=finding,
            attrs={"finding_type": finding_type, "severity": severity, "status": status},
            links=[("finding_object", finding.finding_id), ("item_object", finding.item_id)] + risk_note_links,
            object_links=[(finding.finding_id, finding.item_id, "belongs_to_review_item")]
            + ([(finding.finding_id, source_ref or "", "derived_from_risk_note")] if risk_note_links else []),
        )
        return finding

    def resolve_finding(
        self,
        *,
        finding: ExternalAdapterReviewFinding,
        status: str = "resolved",
        reason: str | None = None,
    ) -> ExternalAdapterReviewFinding:
        _require_value(status, FINDING_STATUSES, ExternalAdapterReviewFindingError, "status")
        updated = replace(
            finding,
            status=status,
            finding_attrs={**finding.finding_attrs, "resolution_reason": reason, "resolved_at": utc_now_iso()},
        )
        self._record(
            "external_adapter_review_finding_resolved",
            finding=updated,
            attrs={"status": status, "reason": reason},
            links=[("finding_object", updated.finding_id), ("item_object", updated.item_id)],
            object_links=[(updated.finding_id, updated.item_id, "belongs_to_review_item")],
        )
        return updated

    def record_decision(
        self,
        *,
        item: ExternalAdapterReviewItem,
        decision: str,
        decided_by: str | None = None,
        decision_reason: str | None = None,
        finding_ids: list[str] | None = None,
        checklist_id: str | None = None,
        decision_attrs: dict[str, Any] | None = None,
    ) -> ExternalAdapterReviewDecision:
        review_decision = ExternalAdapterReviewDecision(
            decision_id=new_external_adapter_review_decision_id(),
            item_id=item.item_id,
            queue_id=item.queue_id,
            candidate_id=item.candidate_id,
            decision=decision,
            decided_by=decided_by,
            decision_reason=decision_reason,
            finding_ids=list(finding_ids or []),
            checklist_id=checklist_id,
            activation_allowed=False,
            runtime_registration_allowed=False,
            execution_enabled_after_decision=False,
            created_at=utc_now_iso(),
            decision_attrs={**dict(decision_attrs or {}), "non_activating": True},
        )
        links = [
            ("decision_object", review_decision.decision_id),
            ("item_object", item.item_id),
            ("queue_object", item.queue_id),
            ("candidate_object", item.candidate_id),
            ("checklist_object", checklist_id or ""),
        ] + [("finding_object", finding_id) for finding_id in review_decision.finding_ids]
        object_links = [
            (review_decision.decision_id, item.item_id, "decides_review_item"),
            (review_decision.decision_id, item.candidate_id, "references_candidate"),
            (review_decision.decision_id, checklist_id or "", "uses_checklist"),
        ] + [
            (review_decision.decision_id, finding_id, "based_on_finding")
            for finding_id in review_decision.finding_ids
        ]
        self._record(
            "external_adapter_review_decision_recorded",
            item=item,
            decision=review_decision,
            attrs={"decision": decision, "activation_allowed": False, "runtime_registration_allowed": False},
            links=links,
            object_links=object_links,
        )
        self._record(
            "external_adapter_review_decision_marked_non_activating",
            item=item,
            decision=review_decision,
            attrs={"decision": decision, "execution_enabled_after_decision": False},
            links=[("decision_object", review_decision.decision_id), ("candidate_object", item.candidate_id)],
            object_links=[(review_decision.decision_id, item.candidate_id, "references_candidate")],
        )
        return review_decision

    def _record(
        self,
        activity: str,
        *,
        attrs: dict[str, Any],
        links: list[tuple[str, str]],
        object_links: list[tuple[str, str, str]],
        queue: ExternalAdapterReviewQueue | None = None,
        item: ExternalAdapterReviewItem | None = None,
        checklist: ExternalAdapterReviewChecklist | None = None,
        finding: ExternalAdapterReviewFinding | None = None,
        decision: ExternalAdapterReviewDecision | None = None,
        candidate_id: str | None = None,
        descriptor_id: str | None = None,
        risk_note_ids: list[str] | None = None,
    ) -> None:
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity=activity,
            event_timestamp=utc_now_iso(),
            event_attrs={
                **attrs,
                "runtime_event_type": activity,
                "source_runtime": "chanta_core",
                "observability_only": True,
                "external_adapter_review_only": True,
                "runtime_effect": False,
                "activation_allowed": False,
                "runtime_registration_allowed": False,
            },
        )
        objects = self._objects(
            queue=queue,
            item=item,
            checklist=checklist,
            finding=finding,
            decision=decision,
            candidate_id=candidate_id,
            descriptor_id=descriptor_id,
            risk_note_ids=risk_note_ids or [],
            links=links,
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

    def _objects(
        self,
        *,
        queue: ExternalAdapterReviewQueue | None,
        item: ExternalAdapterReviewItem | None,
        checklist: ExternalAdapterReviewChecklist | None,
        finding: ExternalAdapterReviewFinding | None,
        decision: ExternalAdapterReviewDecision | None,
        candidate_id: str | None,
        descriptor_id: str | None,
        risk_note_ids: list[str],
        links: list[tuple[str, str]],
    ) -> list[OCELObject]:
        objects: list[OCELObject] = []
        if queue is not None:
            objects.append(_queue_object(queue))
        if item is not None:
            objects.append(_item_object(item))
        if checklist is not None:
            objects.append(_checklist_object(checklist))
        if finding is not None:
            objects.append(_finding_object(finding))
        if decision is not None:
            objects.append(_decision_object(decision))
        ids = {item.object_id for item in objects}
        explicit_ids = set(risk_note_ids)
        if candidate_id:
            explicit_ids.add(candidate_id)
        if descriptor_id:
            explicit_ids.add(descriptor_id)
        for _, object_id in links:
            if object_id:
                explicit_ids.add(object_id)
        for object_id in sorted(explicit_ids):
            if object_id in ids:
                continue
            placeholder = _placeholder_object(object_id)
            if placeholder is not None:
                objects.append(placeholder)
                ids.add(object_id)
        return objects


def _add_check(completed: list[str], failed: list[str], check_name: str, condition: bool) -> None:
    if condition:
        completed.append(check_name)
    else:
        failed.append(check_name)


def _queue_object(queue: ExternalAdapterReviewQueue) -> OCELObject:
    return OCELObject(
        object_id=queue.queue_id,
        object_type="external_adapter_review_queue",
        object_attrs={**queue.to_dict(), "object_key": queue.queue_id, "display_name": queue.queue_name},
    )


def _item_object(item: ExternalAdapterReviewItem) -> OCELObject:
    return OCELObject(
        object_id=item.item_id,
        object_type="external_adapter_review_item",
        object_attrs={
            **item.to_dict(),
            "object_key": item.item_id,
            "display_name": item.review_status,
            "activation_allowed": False,
            "runtime_registration_allowed": False,
        },
    )


def _checklist_object(checklist: ExternalAdapterReviewChecklist) -> OCELObject:
    return OCELObject(
        object_id=checklist.checklist_id,
        object_type="external_adapter_review_checklist",
        object_attrs={**checklist.to_dict(), "object_key": checklist.checklist_id, "display_name": checklist.status},
    )


def _finding_object(finding: ExternalAdapterReviewFinding) -> OCELObject:
    return OCELObject(
        object_id=finding.finding_id,
        object_type="external_adapter_review_finding",
        object_attrs={**finding.to_dict(), "object_key": finding.finding_id, "display_name": finding.finding_type},
    )


def _decision_object(decision: ExternalAdapterReviewDecision) -> OCELObject:
    return OCELObject(
        object_id=decision.decision_id,
        object_type="external_adapter_review_decision",
        object_attrs={**decision.to_dict(), "object_key": decision.decision_id, "display_name": decision.decision},
    )


def _placeholder_object(object_id: str) -> OCELObject | None:
    if object_id.startswith("external_capability_source:"):
        return OCELObject(
            object_id=object_id,
            object_type="external_capability_source",
            object_attrs={"object_key": object_id},
        )
    return None
