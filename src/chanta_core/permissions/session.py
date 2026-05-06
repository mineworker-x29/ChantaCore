from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime
from typing import Any
from uuid import uuid4

from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.permissions.errors import (
    SessionPermissionContextError,
    SessionPermissionResolutionError,
)
from chanta_core.permissions.ids import (
    new_session_permission_context_id,
    new_session_permission_resolution_id,
    new_session_permission_snapshot_id,
)
from chanta_core.permissions.models import PermissionDenial, PermissionGrant, PermissionRequest
from chanta_core.permissions.service import PermissionModelService
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


CONTEXT_STATUSES = {"active", "closed", "reset", "archived"}
RESOLVED_DECISIONS = {"allow", "deny", "ask", "defer", "inconclusive"}
RESOLUTION_BASES = {
    "matching_grant",
    "matching_denial",
    "no_match",
    "expired_grant",
    "manual",
    "test",
    "other",
}


def _require_probability(value: float | None, error_type: type[Exception], field_name: str) -> None:
    if value is None:
        return
    if value < 0.0 or value > 1.0:
        raise error_type(f"{field_name} must be between 0.0 and 1.0")


@dataclass(frozen=True)
class SessionPermissionContext:
    context_id: str
    session_id: str
    status: str
    created_at: str
    updated_at: str
    active_scope_ids: list[str]
    active_grant_ids: list[str]
    active_denial_ids: list[str]
    pending_request_ids: list[str]
    context_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.status not in CONTEXT_STATUSES:
            raise SessionPermissionContextError(f"Unsupported status: {self.status}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "context_id": self.context_id,
            "session_id": self.session_id,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "active_scope_ids": self.active_scope_ids,
            "active_grant_ids": self.active_grant_ids,
            "active_denial_ids": self.active_denial_ids,
            "pending_request_ids": self.pending_request_ids,
            "context_attrs": self.context_attrs,
        }


@dataclass(frozen=True)
class SessionPermissionSnapshot:
    snapshot_id: str
    session_id: str
    context_id: str | None
    created_at: str
    active_grant_ids: list[str]
    active_denial_ids: list[str]
    pending_request_ids: list[str]
    expired_grant_ids: list[str]
    revoked_grant_ids: list[str]
    summary: str | None
    snapshot_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "session_id": self.session_id,
            "context_id": self.context_id,
            "created_at": self.created_at,
            "active_grant_ids": self.active_grant_ids,
            "active_denial_ids": self.active_denial_ids,
            "pending_request_ids": self.pending_request_ids,
            "expired_grant_ids": self.expired_grant_ids,
            "revoked_grant_ids": self.revoked_grant_ids,
            "summary": self.summary,
            "snapshot_attrs": self.snapshot_attrs,
        }


@dataclass(frozen=True)
class SessionPermissionResolution:
    resolution_id: str
    session_id: str
    request_id: str
    resolved_decision: str
    resolution_basis: str
    matched_grant_ids: list[str]
    matched_denial_ids: list[str]
    expired_grant_ids: list[str]
    confidence: float | None
    reason: str | None
    enforcement_enabled: bool
    created_at: str
    resolution_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.resolved_decision not in RESOLVED_DECISIONS:
            raise SessionPermissionResolutionError(f"Unsupported resolved_decision: {self.resolved_decision}")
        if self.resolution_basis not in RESOLUTION_BASES:
            raise SessionPermissionResolutionError(f"Unsupported resolution_basis: {self.resolution_basis}")
        if self.enforcement_enabled is not False:
            raise SessionPermissionResolutionError("enforcement_enabled must be False in v0.12.1")
        _require_probability(self.confidence, SessionPermissionResolutionError, "confidence")

    def to_dict(self) -> dict[str, Any]:
        return {
            "resolution_id": self.resolution_id,
            "session_id": self.session_id,
            "request_id": self.request_id,
            "resolved_decision": self.resolved_decision,
            "resolution_basis": self.resolution_basis,
            "matched_grant_ids": self.matched_grant_ids,
            "matched_denial_ids": self.matched_denial_ids,
            "expired_grant_ids": self.expired_grant_ids,
            "confidence": self.confidence,
            "reason": self.reason,
            "enforcement_enabled": self.enforcement_enabled,
            "created_at": self.created_at,
            "resolution_attrs": self.resolution_attrs,
        }


class SessionPermissionService:
    def __init__(
        self,
        *,
        permission_model_service: PermissionModelService,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        self.permission_model_service = permission_model_service
        if trace_service is not None:
            self.trace_service = trace_service
        elif ocel_store is not None:
            self.trace_service = TraceService(ocel_store=ocel_store)
        else:
            self.trace_service = permission_model_service.trace_service

    def create_context(
        self,
        *,
        session_id: str,
        active_scope_ids: list[str] | None = None,
        context_attrs: dict[str, Any] | None = None,
    ) -> SessionPermissionContext:
        now = utc_now_iso()
        context = SessionPermissionContext(
            context_id=new_session_permission_context_id(),
            session_id=session_id,
            status="active",
            created_at=now,
            updated_at=now,
            active_scope_ids=list(active_scope_ids or []),
            active_grant_ids=[],
            active_denial_ids=[],
            pending_request_ids=[],
            context_attrs={**dict(context_attrs or {}), "runtime_effect": False},
        )
        self._record_session_event(
            "session_permission_context_created",
            context=context,
            event_attrs={},
            event_relations=[
                ("session_permission_context_object", context.context_id),
                ("session_context", self._session_object_id(session_id)),
            ],
            object_relations=[
                (context.context_id, self._session_object_id(session_id), "belongs_to_session"),
            ],
        )
        return context

    def reset_context(
        self,
        *,
        session_id: str,
        reason: str | None = None,
        parent_session_id: str | None = None,
        reset_attrs: dict[str, Any] | None = None,
    ) -> SessionPermissionContext:
        now = utc_now_iso()
        context = SessionPermissionContext(
            context_id=new_session_permission_context_id(),
            session_id=session_id,
            status="reset",
            created_at=now,
            updated_at=now,
            active_scope_ids=[],
            active_grant_ids=[],
            active_denial_ids=[],
            pending_request_ids=[],
            context_attrs={
                **dict(reset_attrs or {}),
                "reason": reason,
                "parent_session_id": parent_session_id,
                "parent_grants_copied": False,
                "runtime_effect": False,
            },
        )
        event_relations = [
            ("session_permission_context_object", context.context_id),
            ("session_context", self._session_object_id(session_id)),
        ]
        object_relations = [(context.context_id, self._session_object_id(session_id), "belongs_to_session")]
        if parent_session_id:
            event_relations.append(("parent_session_context", self._session_object_id(parent_session_id)))
        self._record_session_event(
            "session_permission_context_reset",
            context=context,
            event_attrs={"reason": reason, "parent_session_id": parent_session_id, "parent_grants_copied": False},
            event_relations=event_relations,
            object_relations=object_relations,
        )
        if parent_session_id:
            self._record_session_event(
                "session_permission_non_inheritance_recorded",
                context=context,
                event_attrs={"parent_session_id": parent_session_id, "child_session_id": session_id},
                event_relations=event_relations,
                object_relations=object_relations,
            )
        return context

    def update_context(
        self,
        *,
        context: SessionPermissionContext,
        active_scope_ids: list[str] | None = None,
        active_grant_ids: list[str] | None = None,
        active_denial_ids: list[str] | None = None,
        pending_request_ids: list[str] | None = None,
        context_attrs: dict[str, Any] | None = None,
    ) -> SessionPermissionContext:
        updated = replace(
            context,
            updated_at=utc_now_iso(),
            active_scope_ids=context.active_scope_ids if active_scope_ids is None else list(active_scope_ids),
            active_grant_ids=context.active_grant_ids if active_grant_ids is None else list(active_grant_ids),
            active_denial_ids=context.active_denial_ids if active_denial_ids is None else list(active_denial_ids),
            pending_request_ids=context.pending_request_ids if pending_request_ids is None else list(pending_request_ids),
            context_attrs={**context.context_attrs, **dict(context_attrs or {})},
        )
        event_relations = [
            ("session_permission_context_object", updated.context_id),
            ("session_context", self._session_object_id(updated.session_id)),
        ]
        object_relations = [
            (updated.context_id, self._session_object_id(updated.session_id), "belongs_to_session"),
        ]
        for grant_id in updated.active_grant_ids:
            event_relations.append(("permission_grant_object", grant_id))
            object_relations.append((updated.context_id, grant_id, "includes_grant"))
        for denial_id in updated.active_denial_ids:
            event_relations.append(("permission_denial_object", denial_id))
            object_relations.append((updated.context_id, denial_id, "includes_denial"))
        for request_id in updated.pending_request_ids:
            event_relations.append(("permission_request_object", request_id))
            object_relations.append((updated.context_id, request_id, "includes_request"))
        self._record_session_event(
            "session_permission_context_updated",
            context=updated,
            event_attrs={},
            event_relations=event_relations,
            object_relations=object_relations,
        )
        return updated

    def close_context(
        self,
        *,
        context: SessionPermissionContext,
        reason: str | None = None,
    ) -> SessionPermissionContext:
        closed = replace(
            context,
            status="closed",
            updated_at=utc_now_iso(),
            context_attrs={**context.context_attrs, "close_reason": reason},
        )
        self._record_session_event(
            "session_permission_context_closed",
            context=closed,
            event_attrs={"reason": reason},
            event_relations=[
                ("session_permission_context_object", closed.context_id),
                ("session_context", self._session_object_id(closed.session_id)),
            ],
            object_relations=[
                (closed.context_id, self._session_object_id(closed.session_id), "belongs_to_session"),
            ],
        )
        return closed

    def create_session_permission_request(
        self,
        *,
        session_id: str,
        request_type: str,
        target_type: str,
        target_ref: str,
        operation: str,
        requester_type: str | None = None,
        requester_id: str | None = None,
        scope_id: str | None = None,
        risk_level: str | None = None,
        reason: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
        tool_descriptor_id: str | None = None,
        verification_result_ids: list[str] | None = None,
        outcome_evaluation_ids: list[str] | None = None,
        request_attrs: dict[str, Any] | None = None,
    ) -> PermissionRequest:
        request = self.permission_model_service.create_request(
            request_type=request_type,
            target_type=target_type,
            target_ref=target_ref,
            operation=operation,
            requester_type=requester_type,
            requester_id=requester_id,
            scope_id=scope_id,
            risk_level=risk_level,
            reason=reason,
            status="pending",
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            tool_descriptor_id=tool_descriptor_id,
            verification_result_ids=verification_result_ids,
            outcome_evaluation_ids=outcome_evaluation_ids,
            request_attrs={**dict(request_attrs or {}), "session_scoped": True, "runtime_effect": False},
        )
        event_relations = [
            ("permission_request_object", request.request_id),
            ("session_context", self._session_object_id(session_id)),
        ]
        object_relations = [(request.request_id, self._session_object_id(session_id), "belongs_to_session")]
        if turn_id:
            event_relations.append(("turn_context", turn_id))
            object_relations.append((request.request_id, turn_id, "belongs_to_turn"))
        if process_instance_id:
            event_relations.append(("process_context", process_instance_id))
            object_relations.append((request.request_id, process_instance_id, "observes_process_instance"))
        self._record_session_event(
            "session_permission_request_created",
            request=request,
            event_attrs={"request_id": request.request_id},
            event_relations=event_relations,
            object_relations=object_relations,
        )
        return request

    def attach_grant_to_session(
        self,
        *,
        session_id: str,
        target_type: str,
        target_ref: str,
        operation: str,
        request_id: str | None = None,
        scope_id: str | None = None,
        granted_by: str | None = None,
        expires_at: str | None = None,
        grant_attrs: dict[str, Any] | None = None,
    ) -> PermissionGrant:
        grant = self.permission_model_service.record_grant(
            target_type=target_type,
            target_ref=target_ref,
            operation=operation,
            request_id=request_id,
            scope_id=scope_id,
            granted_by=granted_by,
            expires_at=expires_at,
            session_id=session_id,
            grant_attrs={**dict(grant_attrs or {}), "enforcement_enabled": False, "session_scoped": True},
        )
        self._record_session_event(
            "session_permission_grant_attached",
            grant=grant,
            event_attrs={"grant_id": grant.grant_id},
            event_relations=[
                ("permission_grant_object", grant.grant_id),
                ("session_context", self._session_object_id(session_id)),
            ],
            object_relations=[
                (grant.grant_id, self._session_object_id(session_id), "belongs_to_session"),
            ],
        )
        return grant

    def attach_denial_to_session(
        self,
        *,
        session_id: str,
        target_type: str,
        target_ref: str,
        operation: str,
        request_id: str | None = None,
        scope_id: str | None = None,
        reason: str | None = None,
        denied_by: str | None = None,
        denial_attrs: dict[str, Any] | None = None,
    ) -> PermissionDenial:
        denial = self.permission_model_service.record_denial(
            target_type=target_type,
            target_ref=target_ref,
            operation=operation,
            request_id=request_id,
            scope_id=scope_id,
            reason=reason,
            denied_by=denied_by,
            session_id=session_id,
            denial_attrs={**dict(denial_attrs or {}), "enforcement_enabled": False, "session_scoped": True},
        )
        self._record_session_event(
            "session_permission_denial_attached",
            denial=denial,
            event_attrs={"denial_id": denial.denial_id, "reason": reason},
            event_relations=[
                ("permission_denial_object", denial.denial_id),
                ("session_context", self._session_object_id(session_id)),
            ],
            object_relations=[
                (denial.denial_id, self._session_object_id(session_id), "belongs_to_session"),
            ],
        )
        return denial

    def revoke_session_grant(
        self,
        *,
        grant: PermissionGrant,
        reason: str | None = None,
    ) -> PermissionGrant:
        revoked = self.permission_model_service.revoke_grant(grant=grant, reason=reason)
        session_id = revoked.session_id
        self._record_session_event(
            "session_permission_grant_revoked",
            grant=revoked,
            event_attrs={"reason": reason},
            event_relations=[
                ("permission_grant_object", revoked.grant_id),
                ("session_context", self._session_object_id(session_id)) if session_id else ("", ""),
            ],
            object_relations=[
                (revoked.grant_id, self._session_object_id(session_id), "belongs_to_session")
            ] if session_id else [],
        )
        return revoked

    def expire_session_grants(
        self,
        *,
        session_id: str,
        grants: list[PermissionGrant],
        now_iso: str | None = None,
    ) -> list[PermissionGrant]:
        now = now_iso or utc_now_iso()
        expired: list[PermissionGrant] = []
        for grant in grants:
            if grant.session_id != session_id:
                continue
            if self._is_expired(grant, now):
                expired_grant = self.permission_model_service.expire_grant(grant=grant, reason="session grant expired")
                expired.append(expired_grant)
                self._record_session_event(
                    "session_permission_grant_expired",
                    grant=expired_grant,
                    event_attrs={"now_iso": now},
                    event_relations=[
                        ("permission_grant_object", expired_grant.grant_id),
                        ("session_context", self._session_object_id(session_id)),
                    ],
                    object_relations=[
                        (expired_grant.grant_id, self._session_object_id(session_id), "belongs_to_session"),
                    ],
                )
        return expired

    def build_snapshot(
        self,
        *,
        session_id: str,
        context_id: str | None = None,
        grants: list[PermissionGrant] | None = None,
        denials: list[PermissionDenial] | None = None,
        requests: list[PermissionRequest] | None = None,
        now_iso: str | None = None,
        snapshot_attrs: dict[str, Any] | None = None,
    ) -> SessionPermissionSnapshot:
        now = now_iso or utc_now_iso()
        session_grants = [grant for grant in grants or [] if grant.session_id == session_id]
        active_grants = [
            grant for grant in session_grants if grant.status == "active" and not self._is_expired(grant, now)
        ]
        expired_grants = [
            grant for grant in session_grants if grant.status == "expired" or self._is_expired(grant, now)
        ]
        revoked_grants = [grant for grant in session_grants if grant.status == "revoked"]
        active_denials = [denial for denial in denials or [] if denial.session_id == session_id]
        pending_requests = [
            request for request in requests or [] if request.session_id == session_id and request.status == "pending"
        ]
        snapshot = SessionPermissionSnapshot(
            snapshot_id=new_session_permission_snapshot_id(),
            session_id=session_id,
            context_id=context_id,
            created_at=utc_now_iso(),
            active_grant_ids=[grant.grant_id for grant in active_grants],
            active_denial_ids=[denial.denial_id for denial in active_denials],
            pending_request_ids=[request.request_id for request in pending_requests],
            expired_grant_ids=[grant.grant_id for grant in expired_grants],
            revoked_grant_ids=[grant.grant_id for grant in revoked_grants],
            summary=(
                f"active_grants={len(active_grants)}, active_denials={len(active_denials)}, "
                f"pending_requests={len(pending_requests)}"
            ),
            snapshot_attrs={**dict(snapshot_attrs or {}), "runtime_effect": False},
        )
        event_relations = [
            ("session_permission_snapshot_object", snapshot.snapshot_id),
            ("session_context", self._session_object_id(session_id)),
        ]
        object_relations = [(snapshot.snapshot_id, self._session_object_id(session_id), "belongs_to_session")]
        if context_id:
            event_relations.append(("session_permission_context_object", context_id))
            object_relations.append((snapshot.snapshot_id, context_id, "snapshot_of_context"))
        for grant in active_grants + expired_grants + revoked_grants:
            event_relations.append(("permission_grant_object", grant.grant_id))
        for denial in active_denials:
            event_relations.append(("permission_denial_object", denial.denial_id))
        for request in pending_requests:
            event_relations.append(("permission_request_object", request.request_id))
        self._record_session_event(
            "session_permission_snapshot_created",
            snapshot=snapshot,
            extra_grants=active_grants + expired_grants + revoked_grants,
            extra_denials=active_denials,
            extra_requests=pending_requests,
            event_attrs={"now_iso": now},
            event_relations=event_relations,
            object_relations=object_relations,
        )
        return snapshot

    def resolve_request(
        self,
        *,
        session_id: str,
        request: PermissionRequest,
        grants: list[PermissionGrant] | None = None,
        denials: list[PermissionDenial] | None = None,
        now_iso: str | None = None,
    ) -> SessionPermissionResolution:
        now = now_iso or utc_now_iso()
        session_denials = [denial for denial in denials or [] if denial.session_id == session_id]
        matching_denials = [denial for denial in session_denials if self._matches_request(denial, request)]
        session_grants = [grant for grant in grants or [] if grant.session_id == session_id]
        matching_grants = [grant for grant in session_grants if self._matches_request(grant, request)]
        active_matching_grants = [
            grant for grant in matching_grants if grant.status == "active" and not self._is_expired(grant, now)
        ]
        expired_matching_grants = [
            grant for grant in matching_grants if grant.status == "expired" or self._is_expired(grant, now)
        ]
        if matching_denials:
            decision = "deny"
            basis = "matching_denial"
            reason = "Matching session denial record."
        elif active_matching_grants:
            decision = "allow"
            basis = "matching_grant"
            reason = "Matching active session grant record."
        elif expired_matching_grants:
            decision = "ask"
            basis = "expired_grant"
            reason = "Matching session grant is expired."
        else:
            decision = "ask"
            basis = "no_match"
            reason = "No matching session grant or denial record."
        resolution = SessionPermissionResolution(
            resolution_id=new_session_permission_resolution_id(),
            session_id=session_id,
            request_id=request.request_id,
            resolved_decision=decision,
            resolution_basis=basis,
            matched_grant_ids=[grant.grant_id for grant in active_matching_grants],
            matched_denial_ids=[denial.denial_id for denial in matching_denials],
            expired_grant_ids=[grant.grant_id for grant in expired_matching_grants],
            confidence=1.0,
            reason=reason,
            enforcement_enabled=False,
            created_at=utc_now_iso(),
            resolution_attrs={"runtime_effect": False, "read_model_only": True},
        )
        event_relations = [
            ("session_permission_resolution_object", resolution.resolution_id),
            ("permission_request_object", request.request_id),
            ("session_context", self._session_object_id(session_id)),
        ]
        object_relations = [
            (resolution.resolution_id, request.request_id, "resolves_request"),
            (resolution.resolution_id, self._session_object_id(session_id), "belongs_to_session"),
        ]
        for grant_id in resolution.matched_grant_ids:
            event_relations.append(("permission_grant_object", grant_id))
            object_relations.append((resolution.resolution_id, grant_id, "uses_grant"))
        for denial_id in resolution.matched_denial_ids:
            event_relations.append(("permission_denial_object", denial_id))
            object_relations.append((resolution.resolution_id, denial_id, "uses_denial"))
        self._record_session_event(
            "session_permission_resolution_recorded",
            resolution=resolution,
            request=request,
            extra_grants=active_matching_grants,
            extra_denials=matching_denials,
            event_attrs={"resolved_decision": decision, "resolution_basis": basis},
            event_relations=event_relations,
            object_relations=object_relations,
        )
        self._record_session_event(
            "session_permission_request_resolved",
            resolution=resolution,
            request=request,
            extra_grants=active_matching_grants,
            extra_denials=matching_denials,
            event_attrs={"resolved_decision": decision, "resolution_basis": basis},
            event_relations=event_relations,
            object_relations=object_relations,
        )
        return resolution

    def _record_session_event(
        self,
        event_activity: str,
        *,
        context: SessionPermissionContext | None = None,
        snapshot: SessionPermissionSnapshot | None = None,
        resolution: SessionPermissionResolution | None = None,
        request: PermissionRequest | None = None,
        grant: PermissionGrant | None = None,
        denial: PermissionDenial | None = None,
        extra_requests: list[PermissionRequest] | None = None,
        extra_grants: list[PermissionGrant] | None = None,
        extra_denials: list[PermissionDenial] | None = None,
        event_attrs: dict[str, Any],
        event_relations: list[tuple[str, str]],
        object_relations: list[tuple[str, str, str]],
    ) -> None:
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity=event_activity,
            event_timestamp=utc_now_iso(),
            event_attrs={
                **event_attrs,
                "runtime_event_type": event_activity,
                "source_runtime": "chanta_core",
                "observability_only": True,
                "session_permission_read_model_only": True,
                "runtime_effect": False,
            },
        )
        objects = self._objects_for_event(
            context=context,
            snapshot=snapshot,
            resolution=resolution,
            request=request,
            grant=grant,
            denial=denial,
            extra_requests=extra_requests,
            extra_grants=extra_grants,
            extra_denials=extra_denials,
            event_relations=event_relations,
        )
        relations = [
            OCELRelation.event_object(event_id=event.event_id, object_id=object_id, qualifier=qualifier)
            for qualifier, object_id in event_relations
            if qualifier and object_id
        ]
        relations.extend(
            OCELRelation.object_object(source_object_id=source, target_object_id=target, qualifier=qualifier)
            for source, target, qualifier in object_relations
            if source and target
        )
        self.trace_service.record_session_ocel_record(OCELRecord(event=event, objects=objects, relations=relations))

    def _objects_for_event(
        self,
        *,
        context: SessionPermissionContext | None,
        snapshot: SessionPermissionSnapshot | None,
        resolution: SessionPermissionResolution | None,
        request: PermissionRequest | None,
        grant: PermissionGrant | None,
        denial: PermissionDenial | None,
        extra_requests: list[PermissionRequest] | None,
        extra_grants: list[PermissionGrant] | None,
        extra_denials: list[PermissionDenial] | None,
        event_relations: list[tuple[str, str]],
    ) -> list[OCELObject]:
        objects: list[OCELObject] = []
        if context is not None:
            objects.append(self._context_object(context))
        if snapshot is not None:
            objects.append(self._snapshot_object(snapshot))
        if resolution is not None:
            objects.append(self._resolution_object(resolution))
        if request is not None:
            objects.append(self._request_object(request))
        if grant is not None:
            objects.append(self._grant_object(grant))
        if denial is not None:
            objects.append(self._denial_object(denial))
        for item in extra_requests or []:
            objects.append(self._request_object(item))
        for item in extra_grants or []:
            objects.append(self._grant_object(item))
        for item in extra_denials or []:
            objects.append(self._denial_object(item))
        known_ids = {item.object_id for item in objects}
        for qualifier, object_id in event_relations:
            if not qualifier or not object_id or object_id in known_ids:
                continue
            placeholder = self._placeholder_object(qualifier, object_id)
            if placeholder is not None:
                objects.append(placeholder)
                known_ids.add(object_id)
        return objects

    @staticmethod
    def _context_object(context: SessionPermissionContext) -> OCELObject:
        return OCELObject(
            object_id=context.context_id,
            object_type="session_permission_context",
            object_attrs={
                **context.to_dict(),
                "object_key": context.context_id,
                "display_name": context.session_id,
                "enforcement_enabled": False,
            },
        )

    @staticmethod
    def _snapshot_object(snapshot: SessionPermissionSnapshot) -> OCELObject:
        return OCELObject(
            object_id=snapshot.snapshot_id,
            object_type="session_permission_snapshot",
            object_attrs={
                **snapshot.to_dict(),
                "object_key": snapshot.snapshot_id,
                "display_name": snapshot.session_id,
                "enforcement_enabled": False,
            },
        )

    @staticmethod
    def _resolution_object(resolution: SessionPermissionResolution) -> OCELObject:
        return OCELObject(
            object_id=resolution.resolution_id,
            object_type="session_permission_resolution",
            object_attrs={
                **resolution.to_dict(),
                "object_key": resolution.resolution_id,
                "display_name": resolution.resolved_decision,
            },
        )

    @staticmethod
    def _request_object(request: PermissionRequest) -> OCELObject:
        return OCELObject(
            object_id=request.request_id,
            object_type="permission_request",
            object_attrs={**request.to_dict(), "object_key": request.request_id, "display_name": request.operation},
        )

    @staticmethod
    def _grant_object(grant: PermissionGrant) -> OCELObject:
        return OCELObject(
            object_id=grant.grant_id,
            object_type="permission_grant",
            object_attrs={
                **grant.to_dict(),
                "object_key": grant.grant_id,
                "display_name": grant.operation,
                "enforcement_enabled": False,
            },
        )

    @staticmethod
    def _denial_object(denial: PermissionDenial) -> OCELObject:
        return OCELObject(
            object_id=denial.denial_id,
            object_type="permission_denial",
            object_attrs={
                **denial.to_dict(),
                "object_key": denial.denial_id,
                "display_name": denial.operation,
                "enforcement_enabled": False,
            },
        )

    @staticmethod
    def _placeholder_object(qualifier: str, object_id: str) -> OCELObject | None:
        placeholder_types = {
            "session_context": "session",
            "parent_session_context": "session",
            "turn_context": "conversation_turn",
            "process_context": "process_instance",
            "permission_request_object": "permission_request",
            "permission_grant_object": "permission_grant",
            "permission_denial_object": "permission_denial",
            "session_permission_context_object": "session_permission_context",
            "session_permission_snapshot_object": "session_permission_snapshot",
            "session_permission_resolution_object": "session_permission_resolution",
        }
        object_type = placeholder_types.get(qualifier)
        if object_type is None:
            return None
        return OCELObject(
            object_id=object_id,
            object_type=object_type,
            object_attrs={"object_key": object_id, "display_name": object_id},
        )

    @staticmethod
    def _session_object_id(session_id: str | None) -> str:
        if not session_id:
            return ""
        return session_id if session_id.startswith("session:") else f"session:{session_id}"

    @staticmethod
    def _matches_request(item: PermissionGrant | PermissionDenial, request: PermissionRequest) -> bool:
        return (
            item.target_type == request.target_type
            and item.target_ref == request.target_ref
            and item.operation == request.operation
        )

    @staticmethod
    def _is_expired(grant: PermissionGrant, now_iso: str) -> bool:
        if not grant.expires_at:
            return False
        return _parse_iso(grant.expires_at) < _parse_iso(now_iso)


def _parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
