from __future__ import annotations

from dataclasses import replace
from typing import Any
from uuid import uuid4

from chanta_core.ocel.models import OCELObject, OCELRecord, OCELEvent, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.permissions.ids import (
    new_permission_decision_id,
    new_permission_denial_id,
    new_permission_grant_id,
    new_permission_policy_note_id,
    new_permission_request_id,
    new_permission_scope_id,
)
from chanta_core.permissions.models import (
    PermissionDecision,
    PermissionDenial,
    PermissionGrant,
    PermissionPolicyNote,
    PermissionRequest,
    PermissionScope,
    reject_forbidden_note_type,
)
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


class PermissionModelService:
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

    def register_scope(
        self,
        *,
        scope_name: str,
        scope_type: str,
        description: str | None = None,
        target_type: str | None = None,
        target_ref: str | None = None,
        allowed_operations: list[str] | None = None,
        denied_operations: list[str] | None = None,
        risk_level: str | None = None,
        status: str = "active",
        scope_attrs: dict[str, Any] | None = None,
    ) -> PermissionScope:
        now = utc_now_iso()
        scope = PermissionScope(
            scope_id=new_permission_scope_id(),
            scope_name=scope_name,
            scope_type=scope_type,
            description=description,
            target_type=target_type,
            target_ref=target_ref,
            allowed_operations=list(allowed_operations or []),
            denied_operations=list(denied_operations or []),
            risk_level=risk_level,
            status=status,
            created_at=now,
            updated_at=now,
            scope_attrs=dict(scope_attrs or {}),
        )
        self._record_permission_event(
            "permission_scope_registered",
            scope=scope,
            event_attrs={},
            event_relations=[("scope_object", scope.scope_id)],
            object_relations=[],
        )
        return scope

    def update_scope(
        self,
        *,
        scope: PermissionScope,
        description: str | None = None,
        status: str | None = None,
        allowed_operations: list[str] | None = None,
        denied_operations: list[str] | None = None,
        risk_level: str | None = None,
        scope_attrs: dict[str, Any] | None = None,
    ) -> PermissionScope:
        updated = replace(
            scope,
            description=scope.description if description is None else description,
            status=scope.status if status is None else status,
            allowed_operations=scope.allowed_operations if allowed_operations is None else list(allowed_operations),
            denied_operations=scope.denied_operations if denied_operations is None else list(denied_operations),
            risk_level=scope.risk_level if risk_level is None else risk_level,
            updated_at=utc_now_iso(),
            scope_attrs={**scope.scope_attrs, **dict(scope_attrs or {})},
        )
        self._record_permission_event(
            "permission_scope_updated",
            scope=updated,
            event_attrs={},
            event_relations=[("scope_object", updated.scope_id)],
            object_relations=[],
        )
        return updated

    def deprecate_scope(
        self,
        *,
        scope: PermissionScope,
        reason: str | None = None,
    ) -> PermissionScope:
        deprecated = replace(scope, status="deprecated", updated_at=utc_now_iso())
        self._record_permission_event(
            "permission_scope_deprecated",
            scope=deprecated,
            event_attrs={"reason": reason},
            event_relations=[("scope_object", deprecated.scope_id)],
            object_relations=[],
        )
        return deprecated

    def create_request(
        self,
        *,
        request_type: str,
        target_type: str,
        target_ref: str,
        operation: str,
        requester_type: str | None = None,
        requester_id: str | None = None,
        scope_id: str | None = None,
        risk_level: str | None = None,
        reason: str | None = None,
        status: str = "created",
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
        tool_descriptor_id: str | None = None,
        verification_result_ids: list[str] | None = None,
        outcome_evaluation_ids: list[str] | None = None,
        request_attrs: dict[str, Any] | None = None,
    ) -> PermissionRequest:
        request = PermissionRequest(
            request_id=new_permission_request_id(),
            request_type=request_type,
            requester_type=requester_type,
            requester_id=requester_id,
            target_type=target_type,
            target_ref=target_ref,
            operation=operation,
            scope_id=scope_id,
            risk_level=risk_level,
            reason=reason,
            status=status,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            tool_descriptor_id=tool_descriptor_id,
            verification_result_ids=list(verification_result_ids or []),
            outcome_evaluation_ids=list(outcome_evaluation_ids or []),
            created_at=utc_now_iso(),
            request_attrs={**dict(request_attrs or {}), "record_only": True},
        )
        self._record_request_event("permission_request_created", request, event_attrs={})
        return request

    def mark_request_pending(
        self,
        *,
        request: PermissionRequest,
        reason: str | None = None,
    ) -> PermissionRequest:
        pending = replace(request, status="pending")
        self._record_request_event("permission_request_marked_pending", pending, event_attrs={"reason": reason})
        return pending

    def cancel_request(
        self,
        *,
        request: PermissionRequest,
        reason: str | None = None,
    ) -> PermissionRequest:
        cancelled = replace(request, status="cancelled")
        self._record_request_event("permission_request_cancelled", cancelled, event_attrs={"reason": reason})
        return cancelled

    def expire_request(
        self,
        *,
        request: PermissionRequest,
        reason: str | None = None,
    ) -> PermissionRequest:
        expired = replace(request, status="expired")
        self._record_request_event("permission_request_expired", expired, event_attrs={"reason": reason})
        return expired

    def record_decision(
        self,
        *,
        request_id: str,
        decision: str,
        decision_mode: str,
        reason: str | None = None,
        decided_by: str | None = None,
        confidence: float | None = None,
        decision_attrs: dict[str, Any] | None = None,
    ) -> PermissionDecision:
        item = PermissionDecision(
            decision_id=new_permission_decision_id(),
            request_id=request_id,
            decision=decision,
            decision_mode=decision_mode,
            reason=reason,
            decided_by=decided_by,
            confidence=confidence,
            created_at=utc_now_iso(),
            decision_attrs={**dict(decision_attrs or {}), "record_only": True, "runtime_effect": False},
        )
        self._record_permission_event(
            "permission_decision_recorded",
            decision=item,
            event_attrs={"decision": decision, "decision_mode": decision_mode},
            event_relations=[
                ("decision_object", item.decision_id),
                ("request_object", request_id),
            ],
            object_relations=[(item.decision_id, request_id, "decides_request")],
        )
        return item

    def record_grant(
        self,
        *,
        target_type: str,
        target_ref: str,
        operation: str,
        request_id: str | None = None,
        scope_id: str | None = None,
        status: str = "active",
        granted_by: str | None = None,
        expires_at: str | None = None,
        session_id: str | None = None,
        grant_attrs: dict[str, Any] | None = None,
    ) -> PermissionGrant:
        grant = PermissionGrant(
            grant_id=new_permission_grant_id(),
            request_id=request_id,
            scope_id=scope_id,
            target_type=target_type,
            target_ref=target_ref,
            operation=operation,
            status=status,
            granted_by=granted_by,
            granted_at=utc_now_iso(),
            expires_at=expires_at,
            session_id=session_id,
            grant_attrs={**dict(grant_attrs or {}), "inert_in_v0_12_0": True, "runtime_effect": False},
        )
        self._record_grant_event("permission_grant_recorded", grant, event_attrs={})
        return grant

    def revoke_grant(
        self,
        *,
        grant: PermissionGrant,
        reason: str | None = None,
    ) -> PermissionGrant:
        revoked = replace(grant, status="revoked", grant_attrs={**grant.grant_attrs, "revoke_reason": reason})
        self._record_grant_event("permission_grant_revoked", revoked, event_attrs={"reason": reason})
        return revoked

    def expire_grant(
        self,
        *,
        grant: PermissionGrant,
        reason: str | None = None,
    ) -> PermissionGrant:
        expired = replace(grant, status="expired", grant_attrs={**grant.grant_attrs, "expire_reason": reason})
        self._record_grant_event("permission_grant_expired", expired, event_attrs={"reason": reason})
        return expired

    def record_denial(
        self,
        *,
        target_type: str,
        target_ref: str,
        operation: str,
        request_id: str | None = None,
        scope_id: str | None = None,
        reason: str | None = None,
        denied_by: str | None = None,
        session_id: str | None = None,
        denial_attrs: dict[str, Any] | None = None,
    ) -> PermissionDenial:
        denial = PermissionDenial(
            denial_id=new_permission_denial_id(),
            request_id=request_id,
            scope_id=scope_id,
            target_type=target_type,
            target_ref=target_ref,
            operation=operation,
            reason=reason,
            denied_by=denied_by,
            denied_at=utc_now_iso(),
            session_id=session_id,
            denial_attrs={**dict(denial_attrs or {}), "inert_in_v0_12_0": True, "runtime_effect": False},
        )
        self._record_denial_event("permission_denial_recorded", denial, event_attrs={"reason": reason})
        return denial

    def register_policy_note(
        self,
        *,
        note_type: str,
        text: str,
        scope_id: str | None = None,
        target_type: str | None = None,
        target_ref: str | None = None,
        status: str = "active",
        priority: int | None = None,
        source_kind: str | None = None,
        note_attrs: dict[str, Any] | None = None,
    ) -> PermissionPolicyNote:
        reject_forbidden_note_type(note_type)
        now = utc_now_iso()
        note = PermissionPolicyNote(
            policy_note_id=new_permission_policy_note_id(),
            scope_id=scope_id,
            target_type=target_type,
            target_ref=target_ref,
            note_type=note_type,
            text=text,
            status=status,
            priority=priority,
            source_kind=source_kind,
            created_at=now,
            updated_at=now,
            note_attrs={**dict(note_attrs or {}), "record_only": True},
        )
        self._record_policy_note_event("permission_policy_note_registered", note, event_attrs={})
        return note

    def update_policy_note(
        self,
        *,
        note: PermissionPolicyNote,
        text: str | None = None,
        status: str | None = None,
        priority: int | None = None,
        note_attrs: dict[str, Any] | None = None,
    ) -> PermissionPolicyNote:
        updated = replace(
            note,
            text=note.text if text is None else text,
            status=note.status if status is None else status,
            priority=note.priority if priority is None else priority,
            updated_at=utc_now_iso(),
            note_attrs={**note.note_attrs, **dict(note_attrs or {})},
        )
        self._record_policy_note_event("permission_policy_note_updated", updated, event_attrs={})
        return updated

    def deprecate_policy_note(
        self,
        *,
        note: PermissionPolicyNote,
        reason: str | None = None,
    ) -> PermissionPolicyNote:
        deprecated = replace(note, status="deprecated", updated_at=utc_now_iso())
        self._record_policy_note_event(
            "permission_policy_note_deprecated",
            deprecated,
            event_attrs={"reason": reason},
        )
        return deprecated

    def _record_request_event(
        self,
        event_activity: str,
        request: PermissionRequest,
        *,
        event_attrs: dict[str, Any],
    ) -> None:
        event_relations = [("request_object", request.request_id)]
        object_relations: list[tuple[str, str, str]] = []
        if request.scope_id:
            event_relations.append(("scope_object", request.scope_id))
            object_relations.append((request.request_id, request.scope_id, "uses_scope"))
        if request.session_id:
            session_object_id = self._session_object_id(request.session_id)
            event_relations.append(("session_context", session_object_id))
            object_relations.append((request.request_id, session_object_id, "belongs_to_session"))
        if request.turn_id:
            event_relations.append(("turn_context", request.turn_id))
            object_relations.append((request.request_id, request.turn_id, "belongs_to_turn"))
        if request.process_instance_id:
            event_relations.append(("process_context", request.process_instance_id))
            object_relations.append((request.request_id, request.process_instance_id, "observes_process_instance"))
        if request.tool_descriptor_id:
            event_relations.append(("tool_object", request.tool_descriptor_id))
            object_relations.append((request.request_id, request.tool_descriptor_id, "targets_tool"))
        for result_id in request.verification_result_ids:
            event_relations.append(("verification_result_object", result_id))
            object_relations.append((request.request_id, result_id, "references_verification_result"))
        for evaluation_id in request.outcome_evaluation_ids:
            event_relations.append(("outcome_evaluation_object", evaluation_id))
            object_relations.append((request.request_id, evaluation_id, "references_outcome_evaluation"))
        self._record_permission_event(
            event_activity,
            request=request,
            event_attrs=event_attrs,
            event_relations=event_relations,
            object_relations=object_relations,
        )

    def _record_grant_event(
        self,
        event_activity: str,
        grant: PermissionGrant,
        *,
        event_attrs: dict[str, Any],
    ) -> None:
        event_relations = [("grant_object", grant.grant_id)]
        object_relations: list[tuple[str, str, str]] = []
        if grant.request_id:
            event_relations.append(("request_object", grant.request_id))
            object_relations.append((grant.grant_id, grant.request_id, "grants_request"))
        if grant.scope_id:
            event_relations.append(("scope_object", grant.scope_id))
        if grant.session_id:
            session_object_id = self._session_object_id(grant.session_id)
            event_relations.append(("session_context", session_object_id))
            object_relations.append((grant.grant_id, session_object_id, "belongs_to_session"))
        self._record_permission_event(
            event_activity,
            grant=grant,
            event_attrs=event_attrs,
            event_relations=event_relations,
            object_relations=object_relations,
        )

    def _record_denial_event(
        self,
        event_activity: str,
        denial: PermissionDenial,
        *,
        event_attrs: dict[str, Any],
    ) -> None:
        event_relations = [("denial_object", denial.denial_id)]
        object_relations: list[tuple[str, str, str]] = []
        if denial.request_id:
            event_relations.append(("request_object", denial.request_id))
            object_relations.append((denial.denial_id, denial.request_id, "denies_request"))
        if denial.scope_id:
            event_relations.append(("scope_object", denial.scope_id))
        if denial.session_id:
            session_object_id = self._session_object_id(denial.session_id)
            event_relations.append(("session_context", session_object_id))
            object_relations.append((denial.denial_id, session_object_id, "belongs_to_session"))
        self._record_permission_event(
            event_activity,
            denial=denial,
            event_attrs=event_attrs,
            event_relations=event_relations,
            object_relations=object_relations,
        )

    def _record_policy_note_event(
        self,
        event_activity: str,
        note: PermissionPolicyNote,
        *,
        event_attrs: dict[str, Any],
    ) -> None:
        event_relations = [("policy_note_object", note.policy_note_id)]
        object_relations: list[tuple[str, str, str]] = []
        if note.scope_id:
            event_relations.append(("scope_object", note.scope_id))
            object_relations.append((note.policy_note_id, note.scope_id, "describes_scope"))
        self._record_permission_event(
            event_activity,
            policy_note=note,
            event_attrs=event_attrs,
            event_relations=event_relations,
            object_relations=object_relations,
        )

    def _record_permission_event(
        self,
        event_activity: str,
        *,
        scope: PermissionScope | None = None,
        request: PermissionRequest | None = None,
        decision: PermissionDecision | None = None,
        grant: PermissionGrant | None = None,
        denial: PermissionDenial | None = None,
        policy_note: PermissionPolicyNote | None = None,
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
                "permission_model_only": True,
                "runtime_effect": False,
            },
        )
        objects = self._objects_for_event(
            scope=scope,
            request=request,
            decision=decision,
            grant=grant,
            denial=denial,
            policy_note=policy_note,
            event_relations=event_relations,
        )
        relations = [
            OCELRelation.event_object(event_id=event.event_id, object_id=object_id, qualifier=qualifier)
            for qualifier, object_id in event_relations
            if object_id
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
        scope: PermissionScope | None,
        request: PermissionRequest | None,
        decision: PermissionDecision | None,
        grant: PermissionGrant | None,
        denial: PermissionDenial | None,
        policy_note: PermissionPolicyNote | None,
        event_relations: list[tuple[str, str]],
    ) -> list[OCELObject]:
        objects: list[OCELObject] = []
        if scope is not None:
            objects.append(self._scope_object(scope))
        if request is not None:
            objects.append(self._request_object(request))
        if decision is not None:
            objects.append(self._decision_object(decision))
        if grant is not None:
            objects.append(self._grant_object(grant))
        if denial is not None:
            objects.append(self._denial_object(denial))
        if policy_note is not None:
            objects.append(self._policy_note_object(policy_note))

        known_ids = {item.object_id for item in objects}
        for qualifier, object_id in event_relations:
            if not object_id or object_id in known_ids:
                continue
            placeholder = self._placeholder_object(qualifier, object_id)
            if placeholder is not None:
                objects.append(placeholder)
                known_ids.add(object_id)
        return objects

    @staticmethod
    def _scope_object(scope: PermissionScope) -> OCELObject:
        return OCELObject(
            object_id=scope.scope_id,
            object_type="permission_scope",
            object_attrs={**scope.to_dict(), "object_key": scope.scope_id, "display_name": scope.scope_name},
        )

    @staticmethod
    def _request_object(request: PermissionRequest) -> OCELObject:
        return OCELObject(
            object_id=request.request_id,
            object_type="permission_request",
            object_attrs={**request.to_dict(), "object_key": request.request_id, "display_name": request.operation},
        )

    @staticmethod
    def _decision_object(decision: PermissionDecision) -> OCELObject:
        return OCELObject(
            object_id=decision.decision_id,
            object_type="permission_decision",
            object_attrs={**decision.to_dict(), "object_key": decision.decision_id, "display_name": decision.decision},
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
                "inert_in_v0_12_0": True,
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
                "inert_in_v0_12_0": True,
            },
        )

    @staticmethod
    def _policy_note_object(note: PermissionPolicyNote) -> OCELObject:
        return OCELObject(
            object_id=note.policy_note_id,
            object_type="permission_policy_note",
            object_attrs={
                **note.to_dict(),
                "object_key": note.policy_note_id,
                "display_name": note.note_type,
                "en" + "forcement_enabled": False,
            },
        )

    @staticmethod
    def _placeholder_object(qualifier: str, object_id: str) -> OCELObject | None:
        placeholder_types = {
            "session_context": "session",
            "turn_context": "conversation_turn",
            "process_context": "process_instance",
            "tool_object": "tool_descriptor",
            "verification_result_object": "verification_result",
            "outcome_evaluation_object": "process_outcome_evaluation",
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
    def _session_object_id(session_id: str) -> str:
        return session_id if session_id.startswith("session:") else f"session:{session_id}"
