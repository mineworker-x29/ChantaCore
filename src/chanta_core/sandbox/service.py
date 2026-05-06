from __future__ import annotations

from pathlib import Path
from typing import Any
from uuid import uuid4

from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.sandbox.ids import (
    new_workspace_root_id,
    new_workspace_write_boundary_id,
    new_workspace_write_intent_id,
    new_workspace_write_sandbox_decision_id,
    new_workspace_write_sandbox_violation_id,
)
from chanta_core.sandbox.models import (
    WorkspaceRoot,
    WorkspaceWriteBoundary,
    WorkspaceWriteIntent,
    WorkspaceWriteSandboxDecision,
    WorkspaceWriteSandboxViolation,
)
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


def normalize_path(path: str | Path) -> str:
    return str(Path(path).expanduser().resolve(strict=False))


def is_same_or_child_path(path: str | Path, parent: str | Path) -> bool:
    resolved_path = Path(path).expanduser().resolve(strict=False)
    resolved_parent = Path(parent).expanduser().resolve(strict=False)
    try:
        resolved_path.relative_to(resolved_parent)
        return True
    except ValueError:
        return False


def is_path_inside_root(path: str | Path, root: str | Path) -> bool:
    return is_same_or_child_path(path, root)


class WorkspaceWriteSandboxService:
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

    def register_workspace_root(
        self,
        *,
        root_path: str,
        root_name: str | None = None,
        status: str = "active",
        root_attrs: dict[str, Any] | None = None,
    ) -> WorkspaceRoot:
        now = utc_now_iso()
        root = WorkspaceRoot(
            workspace_root_id=new_workspace_root_id(),
            root_path=root_path,
            root_name=root_name,
            status=status,
            created_at=now,
            updated_at=now,
            root_attrs={**dict(root_attrs or {}), "normalized_root_path": normalize_path(root_path)},
        )
        self._record_event(
            "workspace_root_registered",
            root=root,
            event_attrs={},
            event_relations=[("workspace_root_object", root.workspace_root_id)],
            object_relations=[],
        )
        return root

    def update_workspace_root(
        self,
        *,
        root: WorkspaceRoot,
        root_name: str | None = None,
        status: str | None = None,
        root_attrs: dict[str, Any] | None = None,
    ) -> WorkspaceRoot:
        updated = WorkspaceRoot(
            workspace_root_id=root.workspace_root_id,
            root_path=root.root_path,
            root_name=root.root_name if root_name is None else root_name,
            status=root.status if status is None else status,
            created_at=root.created_at,
            updated_at=utc_now_iso(),
            root_attrs={**root.root_attrs, **dict(root_attrs or {})},
        )
        self._record_event(
            "workspace_root_updated",
            root=updated,
            event_attrs={},
            event_relations=[("workspace_root_object", updated.workspace_root_id)],
            object_relations=[],
        )
        return updated

    def deprecate_workspace_root(
        self,
        *,
        root: WorkspaceRoot,
        reason: str | None = None,
    ) -> WorkspaceRoot:
        deprecated = WorkspaceRoot(
            workspace_root_id=root.workspace_root_id,
            root_path=root.root_path,
            root_name=root.root_name,
            status="deprecated",
            created_at=root.created_at,
            updated_at=utc_now_iso(),
            root_attrs={**root.root_attrs, "deprecation_reason": reason},
        )
        self._record_event(
            "workspace_root_deprecated",
            root=deprecated,
            event_attrs={"reason": reason},
            event_relations=[("workspace_root_object", deprecated.workspace_root_id)],
            object_relations=[],
        )
        return deprecated

    def register_write_boundary(
        self,
        *,
        workspace_root_id: str,
        boundary_type: str,
        path_ref: str,
        description: str | None = None,
        status: str = "active",
        priority: int | None = None,
        boundary_attrs: dict[str, Any] | None = None,
    ) -> WorkspaceWriteBoundary:
        boundary = WorkspaceWriteBoundary(
            boundary_id=new_workspace_write_boundary_id(),
            workspace_root_id=workspace_root_id,
            boundary_type=boundary_type,
            path_ref=path_ref,
            description=description,
            status=status,
            priority=priority,
            boundary_attrs={**dict(boundary_attrs or {}), "normalized_path_ref": normalize_path(path_ref)},
        )
        self._record_event(
            "workspace_write_boundary_registered",
            boundary=boundary,
            event_attrs={},
            event_relations=[
                ("boundary_object", boundary.boundary_id),
                ("workspace_root_object", workspace_root_id),
            ],
            object_relations=[
                (boundary.boundary_id, workspace_root_id, "belongs_to_workspace_root"),
            ],
        )
        return boundary

    def update_write_boundary(
        self,
        *,
        boundary: WorkspaceWriteBoundary,
        description: str | None = None,
        status: str | None = None,
        priority: int | None = None,
        boundary_attrs: dict[str, Any] | None = None,
    ) -> WorkspaceWriteBoundary:
        updated = WorkspaceWriteBoundary(
            boundary_id=boundary.boundary_id,
            workspace_root_id=boundary.workspace_root_id,
            boundary_type=boundary.boundary_type,
            path_ref=boundary.path_ref,
            description=boundary.description if description is None else description,
            status=boundary.status if status is None else status,
            priority=boundary.priority if priority is None else priority,
            boundary_attrs={**boundary.boundary_attrs, **dict(boundary_attrs or {})},
        )
        self._record_event(
            "workspace_write_boundary_updated",
            boundary=updated,
            event_attrs={},
            event_relations=[
                ("boundary_object", updated.boundary_id),
                ("workspace_root_object", updated.workspace_root_id),
            ],
            object_relations=[
                (updated.boundary_id, updated.workspace_root_id, "belongs_to_workspace_root"),
            ],
        )
        return updated

    def deprecate_write_boundary(
        self,
        *,
        boundary: WorkspaceWriteBoundary,
        reason: str | None = None,
    ) -> WorkspaceWriteBoundary:
        deprecated = WorkspaceWriteBoundary(
            boundary_id=boundary.boundary_id,
            workspace_root_id=boundary.workspace_root_id,
            boundary_type=boundary.boundary_type,
            path_ref=boundary.path_ref,
            description=boundary.description,
            status="deprecated",
            priority=boundary.priority,
            boundary_attrs={**boundary.boundary_attrs, "deprecation_reason": reason},
        )
        self._record_event(
            "workspace_write_boundary_deprecated",
            boundary=deprecated,
            event_attrs={"reason": reason},
            event_relations=[
                ("boundary_object", deprecated.boundary_id),
                ("workspace_root_object", deprecated.workspace_root_id),
            ],
            object_relations=[
                (deprecated.boundary_id, deprecated.workspace_root_id, "belongs_to_workspace_root"),
            ],
        )
        return deprecated

    def create_write_intent(
        self,
        *,
        target_path: str,
        operation: str,
        workspace_root_id: str | None = None,
        requester_type: str | None = None,
        requester_id: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
        permission_request_id: str | None = None,
        session_permission_resolution_id: str | None = None,
        reason: str | None = None,
        intent_attrs: dict[str, Any] | None = None,
    ) -> WorkspaceWriteIntent:
        intent = WorkspaceWriteIntent(
            intent_id=new_workspace_write_intent_id(),
            workspace_root_id=workspace_root_id,
            target_path=target_path,
            operation=operation,
            requester_type=requester_type,
            requester_id=requester_id,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            permission_request_id=permission_request_id,
            session_permission_resolution_id=session_permission_resolution_id,
            reason=reason,
            created_at=utc_now_iso(),
            intent_attrs={**dict(intent_attrs or {}), "runtime_effect": False},
        )
        event_relations = [("intent_object", intent.intent_id)]
        object_relations: list[tuple[str, str, str]] = []
        if workspace_root_id:
            event_relations.append(("workspace_root_object", workspace_root_id))
            object_relations.append((intent.intent_id, workspace_root_id, "targets_workspace_root"))
        if session_id:
            event_relations.append(("session_context", self._session_object_id(session_id)))
            object_relations.append((intent.intent_id, self._session_object_id(session_id), "belongs_to_session"))
        if turn_id:
            event_relations.append(("turn_context", turn_id))
            object_relations.append((intent.intent_id, turn_id, "belongs_to_turn"))
        if process_instance_id:
            event_relations.append(("process_context", process_instance_id))
            object_relations.append((intent.intent_id, process_instance_id, "observes_process_instance"))
        if permission_request_id:
            event_relations.append(("permission_request_object", permission_request_id))
            object_relations.append((intent.intent_id, permission_request_id, "references_permission_request"))
        if session_permission_resolution_id:
            event_relations.append(("session_permission_resolution_object", session_permission_resolution_id))
            object_relations.append((intent.intent_id, session_permission_resolution_id, "references_session_permission_resolution"))
        self._record_event(
            "workspace_write_intent_created",
            intent=intent,
            event_attrs={},
            event_relations=event_relations,
            object_relations=object_relations,
        )
        return intent

    def record_violation(
        self,
        *,
        intent_id: str,
        violation_type: str,
        message: str,
        target_path: str,
        workspace_root_id: str | None = None,
        severity: str | None = None,
        violation_attrs: dict[str, Any] | None = None,
    ) -> WorkspaceWriteSandboxViolation:
        violation = WorkspaceWriteSandboxViolation(
            violation_id=new_workspace_write_sandbox_violation_id(),
            intent_id=intent_id,
            violation_type=violation_type,
            severity=severity,
            message=message,
            target_path=target_path,
            workspace_root_id=workspace_root_id,
            created_at=utc_now_iso(),
            violation_attrs={**dict(violation_attrs or {}), "runtime_effect": False},
        )
        event_relations = [
            ("violation_object", violation.violation_id),
            ("intent_object", intent_id),
        ]
        object_relations = [(violation.violation_id, intent_id, "violation_of_intent")]
        if workspace_root_id:
            event_relations.append(("workspace_root_object", workspace_root_id))
            object_relations.append((violation.violation_id, workspace_root_id, "references_workspace_root"))
        self._record_event(
            "workspace_write_sandbox_violation_recorded",
            violation=violation,
            event_attrs={"violation_type": violation_type},
            event_relations=event_relations,
            object_relations=object_relations,
        )
        return violation

    def record_decision(
        self,
        *,
        intent_id: str,
        decision: str,
        decision_basis: str,
        workspace_root_id: str | None = None,
        normalized_target_path: str | None = None,
        normalized_root_path: str | None = None,
        inside_workspace: bool | None = None,
        matched_boundary_ids: list[str] | None = None,
        violation_ids: list[str] | None = None,
        confidence: float | None = None,
        reason: str | None = None,
        decision_attrs: dict[str, Any] | None = None,
    ) -> WorkspaceWriteSandboxDecision:
        item = WorkspaceWriteSandboxDecision(
            decision_id=new_workspace_write_sandbox_decision_id(),
            intent_id=intent_id,
            workspace_root_id=workspace_root_id,
            decision=decision,
            decision_basis=decision_basis,
            normalized_target_path=normalized_target_path,
            normalized_root_path=normalized_root_path,
            inside_workspace=inside_workspace,
            matched_boundary_ids=list(matched_boundary_ids or []),
            violation_ids=list(violation_ids or []),
            confidence=confidence,
            reason=reason,
            enforcement_enabled=False,
            created_at=utc_now_iso(),
            decision_attrs={**dict(decision_attrs or {}), "runtime_effect": False},
        )
        event_relations = [
            ("decision_object", item.decision_id),
            ("intent_object", intent_id),
        ]
        object_relations = [(item.decision_id, intent_id, "decides_intent")]
        if workspace_root_id:
            event_relations.append(("workspace_root_object", workspace_root_id))
        for boundary_id in item.matched_boundary_ids:
            event_relations.append(("boundary_object", boundary_id))
            object_relations.append((item.decision_id, boundary_id, "uses_boundary"))
        for violation_id in item.violation_ids:
            event_relations.append(("violation_object", violation_id))
        self._record_event(
            "workspace_write_sandbox_decision_recorded",
            decision=item,
            event_attrs={"decision": decision, "decision_basis": decision_basis},
            event_relations=event_relations,
            object_relations=object_relations,
        )
        return item

    def evaluate_write_intent(
        self,
        *,
        intent: WorkspaceWriteIntent,
        workspace_root: WorkspaceRoot | None = None,
        boundaries: list[WorkspaceWriteBoundary] | None = None,
    ) -> WorkspaceWriteSandboxDecision:
        self._record_event(
            "workspace_write_sandbox_evaluated",
            intent=intent,
            event_attrs={"intent_id": intent.intent_id},
            event_relations=[("intent_object", intent.intent_id)],
            object_relations=[],
        )
        if workspace_root is None:
            return self.record_decision(
                intent_id=intent.intent_id,
                workspace_root_id=intent.workspace_root_id,
                decision="inconclusive",
                decision_basis="no_workspace_root",
                inside_workspace=None,
                confidence=1.0,
                reason="No workspace root was provided for evaluation.",
            )

        try:
            normalized_target = normalize_path(intent.target_path)
            normalized_root = normalize_path(workspace_root.root_path)
            inside = is_path_inside_root(normalized_target, normalized_root)
        except (OSError, RuntimeError, ValueError) as error:
            violation = self.record_violation(
                intent_id=intent.intent_id,
                violation_type="path_resolution_error",
                severity="high",
                message=str(error),
                target_path=intent.target_path,
                workspace_root_id=workspace_root.workspace_root_id,
            )
            return self.record_decision(
                intent_id=intent.intent_id,
                workspace_root_id=workspace_root.workspace_root_id,
                decision="error",
                decision_basis="path_resolution_error",
                violation_ids=[violation.violation_id],
                confidence=1.0,
                reason=str(error),
            )
        if not inside:
            violation = self.record_violation(
                intent_id=intent.intent_id,
                violation_type="outside_workspace",
                severity="high",
                message="Target path is outside the workspace root.",
                target_path=intent.target_path,
                workspace_root_id=workspace_root.workspace_root_id,
                violation_attrs={"normalized_target_path": normalized_target, "normalized_root_path": normalized_root},
            )
            return self.record_decision(
                intent_id=intent.intent_id,
                workspace_root_id=workspace_root.workspace_root_id,
                decision="denied",
                decision_basis="outside_workspace",
                normalized_target_path=normalized_target,
                normalized_root_path=normalized_root,
                inside_workspace=False,
                violation_ids=[violation.violation_id],
                confidence=1.0,
                reason="Target path is outside the workspace root.",
            )

        active_boundaries = [
            boundary for boundary in boundaries or []
            if boundary.workspace_root_id == workspace_root.workspace_root_id and boundary.status == "active"
        ]
        matched = [
            boundary for boundary in active_boundaries
            if boundary.boundary_type in {"denied_path", "protected_path"}
            and is_same_or_child_path(normalized_target, self._boundary_path(boundary, workspace_root))
        ]
        if matched:
            selected = sorted(matched, key=lambda item: (item.priority is None, item.priority or 0, item.boundary_id))[0]
            violation_type = "protected_path" if selected.boundary_type == "protected_path" else "denied_path"
            basis = "protected_path" if selected.boundary_type == "protected_path" else "denied_boundary"
            violation = self.record_violation(
                intent_id=intent.intent_id,
                violation_type=violation_type,
                severity="high",
                message=f"Target path matches {selected.boundary_type} boundary.",
                target_path=intent.target_path,
                workspace_root_id=workspace_root.workspace_root_id,
                violation_attrs={"boundary_id": selected.boundary_id},
            )
            return self.record_decision(
                intent_id=intent.intent_id,
                workspace_root_id=workspace_root.workspace_root_id,
                decision="denied",
                decision_basis=basis,
                normalized_target_path=normalized_target,
                normalized_root_path=normalized_root,
                inside_workspace=True,
                matched_boundary_ids=[selected.boundary_id],
                violation_ids=[violation.violation_id],
                confidence=1.0,
                reason=f"Target path matches {selected.boundary_type} boundary.",
            )

        return self.record_decision(
            intent_id=intent.intent_id,
            workspace_root_id=workspace_root.workspace_root_id,
            decision="allowed",
            decision_basis="inside_workspace",
            normalized_target_path=normalized_target,
            normalized_root_path=normalized_root,
            inside_workspace=True,
            confidence=1.0,
            reason="Target path is inside workspace and no denying boundary matched.",
        )

    def _record_event(
        self,
        event_activity: str,
        *,
        root: WorkspaceRoot | None = None,
        boundary: WorkspaceWriteBoundary | None = None,
        intent: WorkspaceWriteIntent | None = None,
        decision: WorkspaceWriteSandboxDecision | None = None,
        violation: WorkspaceWriteSandboxViolation | None = None,
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
                "workspace_write_guard_model_only": True,
                "runtime_effect": False,
            },
        )
        objects = self._objects_for_event(
            root=root,
            boundary=boundary,
            intent=intent,
            decision=decision,
            violation=violation,
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
        root: WorkspaceRoot | None,
        boundary: WorkspaceWriteBoundary | None,
        intent: WorkspaceWriteIntent | None,
        decision: WorkspaceWriteSandboxDecision | None,
        violation: WorkspaceWriteSandboxViolation | None,
        event_relations: list[tuple[str, str]],
    ) -> list[OCELObject]:
        objects: list[OCELObject] = []
        if root is not None:
            objects.append(self._root_object(root))
        if boundary is not None:
            objects.append(self._boundary_object(boundary))
        if intent is not None:
            objects.append(self._intent_object(intent))
        if decision is not None:
            objects.append(self._decision_object(decision))
        if violation is not None:
            objects.append(self._violation_object(violation))
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
    def _root_object(root: WorkspaceRoot) -> OCELObject:
        return OCELObject(
            object_id=root.workspace_root_id,
            object_type="workspace_root",
            object_attrs={
                **root.to_dict(),
                "object_key": root.workspace_root_id,
                "display_name": root.root_name or root.root_path,
                "normalized_root_path": root.root_attrs.get("normalized_root_path"),
            },
        )

    @staticmethod
    def _boundary_object(boundary: WorkspaceWriteBoundary) -> OCELObject:
        return OCELObject(
            object_id=boundary.boundary_id,
            object_type="workspace_write_boundary",
            object_attrs={
                **boundary.to_dict(),
                "object_key": boundary.boundary_id,
                "display_name": boundary.boundary_type,
                "normalized_path_ref": boundary.boundary_attrs.get("normalized_path_ref"),
            },
        )

    @staticmethod
    def _intent_object(intent: WorkspaceWriteIntent) -> OCELObject:
        return OCELObject(
            object_id=intent.intent_id,
            object_type="workspace_write_intent",
            object_attrs={**intent.to_dict(), "object_key": intent.intent_id, "display_name": intent.operation},
        )

    @staticmethod
    def _decision_object(decision: WorkspaceWriteSandboxDecision) -> OCELObject:
        return OCELObject(
            object_id=decision.decision_id,
            object_type="workspace_write_sandbox_decision",
            object_attrs={**decision.to_dict(), "object_key": decision.decision_id, "display_name": decision.decision},
        )

    @staticmethod
    def _violation_object(violation: WorkspaceWriteSandboxViolation) -> OCELObject:
        return OCELObject(
            object_id=violation.violation_id,
            object_type="workspace_write_sandbox_violation",
            object_attrs={**violation.to_dict(), "object_key": violation.violation_id, "display_name": violation.violation_type},
        )

    @staticmethod
    def _placeholder_object(qualifier: str, object_id: str) -> OCELObject | None:
        placeholder_types = {
            "session_context": "session",
            "turn_context": "conversation_turn",
            "process_context": "process_instance",
            "permission_request_object": "permission_request",
            "session_permission_resolution_object": "session_permission_resolution",
        }
        object_type = placeholder_types.get(qualifier)
        if object_type is None:
            return None
        return OCELObject(object_id=object_id, object_type=object_type, object_attrs={"object_key": object_id})

    @staticmethod
    def _boundary_path(boundary: WorkspaceWriteBoundary, root: WorkspaceRoot) -> str:
        path = Path(boundary.path_ref)
        if path.is_absolute():
            return normalize_path(path)
        return normalize_path(Path(root.root_path) / path)

    @staticmethod
    def _session_object_id(session_id: str) -> str:
        return session_id if session_id.startswith("session:") else f"session:{session_id}"
