from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any
from uuid import uuid4

from chanta_core.materialized_views.models import MaterializedView
from chanta_core.ocel.models import OCELObject, OCELRecord, OCELEvent, OCELRelation
from chanta_core.tool_registry.errors import ToolPolicyNoteError
from chanta_core.tool_registry.ids import (
    new_tool_descriptor_id,
    new_tool_policy_note_id,
    new_tool_registry_snapshot_id,
    new_tool_risk_annotation_id,
)
from chanta_core.tool_registry.models import (
    FORBIDDEN_POLICY_NOTE_TYPES,
    ToolDescriptor,
    ToolPolicyNote,
    ToolRegistrySnapshot,
    ToolRiskAnnotation,
    hash_tool_snapshot,
)
from chanta_core.tool_registry.paths import get_tool_view_paths
from chanta_core.tool_registry.renderers import (
    render_tool_policy_view,
    render_tools_view,
)
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


class ToolRegistryViewService:
    def __init__(
        self,
        *,
        trace_service: TraceService | None = None,
        root: Path | str | None = None,
    ) -> None:
        self.trace_service = trace_service or TraceService()
        self.root = Path(root) if root is not None else Path(".")

    def register_tool_descriptor(
        self,
        *,
        tool_name: str,
        tool_type: str,
        description: str | None = None,
        status: str = "active",
        capability_tags: list[str] | None = None,
        input_schema_ref: str | None = None,
        output_schema_ref: str | None = None,
        execution_owner: str | None = None,
        source_kind: str | None = None,
        risk_level: str | None = "unknown",
        tool_attrs: dict[str, Any] | None = None,
    ) -> ToolDescriptor:
        now = utc_now_iso()
        descriptor = ToolDescriptor(
            tool_id=new_tool_descriptor_id(),
            tool_name=tool_name,
            tool_type=tool_type,
            description=description,
            status=status,
            capability_tags=sorted(capability_tags or []),
            input_schema_ref=input_schema_ref,
            output_schema_ref=output_schema_ref,
            execution_owner=execution_owner,
            source_kind=source_kind,
            risk_level=risk_level,
            created_at=now,
            updated_at=now,
            tool_attrs=dict(tool_attrs or {}),
        )
        self._record_tool_event(
            "tool_descriptor_registered",
            descriptor=descriptor,
            event_attrs={},
            event_relations=[("tool_object", descriptor.tool_id)],
            object_relations=[],
        )
        return descriptor

    def update_tool_descriptor(
        self,
        *,
        descriptor: ToolDescriptor,
        description: str | None = None,
        status: str | None = None,
        risk_level: str | None = None,
        capability_tags: list[str] | None = None,
        tool_attrs: dict[str, Any] | None = None,
    ) -> ToolDescriptor:
        updated = replace(
            descriptor,
            description=descriptor.description if description is None else description,
            status=descriptor.status if status is None else status,
            risk_level=descriptor.risk_level if risk_level is None else risk_level,
            capability_tags=descriptor.capability_tags if capability_tags is None else sorted(capability_tags),
            updated_at=utc_now_iso(),
            tool_attrs={**descriptor.tool_attrs, **dict(tool_attrs or {})},
        )
        self._record_tool_event(
            "tool_descriptor_updated",
            descriptor=updated,
            event_attrs={},
            event_relations=[("tool_object", updated.tool_id)],
            object_relations=[],
        )
        return updated

    def deprecate_tool_descriptor(
        self,
        *,
        descriptor: ToolDescriptor,
        reason: str | None = None,
    ) -> ToolDescriptor:
        deprecated = replace(descriptor, status="deprecated", updated_at=utc_now_iso())
        self._record_tool_event(
            "tool_descriptor_deprecated",
            descriptor=deprecated,
            event_attrs={"reason": reason},
            event_relations=[("tool_object", deprecated.tool_id)],
            object_relations=[],
        )
        return deprecated

    def create_registry_snapshot(
        self,
        *,
        tools: list[ToolDescriptor],
        snapshot_name: str | None = None,
        source_kind: str = "manual",
        snapshot_attrs: dict[str, Any] | None = None,
    ) -> ToolRegistrySnapshot:
        tool_ids = sorted(tool.tool_id for tool in tools)
        snapshot = ToolRegistrySnapshot(
            snapshot_id=new_tool_registry_snapshot_id(),
            snapshot_name=snapshot_name,
            created_at=utc_now_iso(),
            tool_ids=tool_ids,
            source_kind=source_kind,
            snapshot_hash=hash_tool_snapshot(tool_ids),
            snapshot_attrs=dict(snapshot_attrs or {}),
        )
        self._record_tool_event(
            "tool_registry_snapshot_created",
            snapshot=snapshot,
            descriptors=tools,
            event_attrs={"snapshot_name": snapshot_name},
            event_relations=[
                ("snapshot_object", snapshot.snapshot_id),
                *[("tool_object", tool.tool_id) for tool in tools],
            ],
            object_relations=[
                (snapshot.snapshot_id, tool.tool_id, "includes_tool")
                for tool in tools
            ],
        )
        return snapshot

    def register_tool_policy_note(
        self,
        *,
        tool_id: str | None = None,
        tool_name: str | None = None,
        note_type: str,
        text: str,
        status: str = "active",
        priority: int | None = None,
        source_kind: str | None = None,
        note_attrs: dict[str, Any] | None = None,
    ) -> ToolPolicyNote:
        if note_type in FORBIDDEN_POLICY_NOTE_TYPES:
            raise ToolPolicyNoteError(f"Forbidden tool policy note type: {note_type}")
        now = utc_now_iso()
        note = ToolPolicyNote(
            policy_note_id=new_tool_policy_note_id(),
            tool_id=tool_id,
            tool_name=tool_name,
            note_type=note_type,
            text=text,
            status=status,
            priority=priority,
            source_kind=source_kind,
            created_at=now,
            updated_at=now,
            note_attrs=dict(note_attrs or {}),
        )
        self._record_tool_event(
            "tool_policy_note_registered",
            policy_note=note,
            event_attrs={},
            event_relations=[
                ("policy_note_object", note.policy_note_id),
                *([("tool_object", tool_id)] if tool_id else []),
            ],
            object_relations=[
                *((note.policy_note_id, tool_id, "describes_tool") for _ in [0] if tool_id),
            ],
        )
        return note

    def update_tool_policy_note(
        self,
        *,
        note: ToolPolicyNote,
        text: str | None = None,
        status: str | None = None,
        priority: int | None = None,
        note_attrs: dict[str, Any] | None = None,
    ) -> ToolPolicyNote:
        updated = replace(
            note,
            text=note.text if text is None else text,
            status=note.status if status is None else status,
            priority=note.priority if priority is None else priority,
            updated_at=utc_now_iso(),
            note_attrs={**note.note_attrs, **dict(note_attrs or {})},
        )
        self._record_tool_event(
            "tool_policy_note_updated",
            policy_note=updated,
            event_attrs={},
            event_relations=[
                ("policy_note_object", updated.policy_note_id),
                *([("tool_object", updated.tool_id)] if updated.tool_id else []),
            ],
            object_relations=[
                *((updated.policy_note_id, updated.tool_id, "describes_tool") for _ in [0] if updated.tool_id),
            ],
        )
        return updated

    def register_tool_risk_annotation(
        self,
        *,
        tool_id: str,
        risk_level: str,
        risk_category: str,
        rationale: str | None = None,
        status: str = "active",
        annotation_attrs: dict[str, Any] | None = None,
    ) -> ToolRiskAnnotation:
        now = utc_now_iso()
        annotation = ToolRiskAnnotation(
            risk_annotation_id=new_tool_risk_annotation_id(),
            tool_id=tool_id,
            risk_level=risk_level,
            risk_category=risk_category,
            rationale=rationale,
            status=status,
            created_at=now,
            updated_at=now,
            annotation_attrs=dict(annotation_attrs or {}),
        )
        self._record_tool_event(
            "tool_risk_annotation_registered",
            risk_annotation=annotation,
            event_attrs={},
            event_relations=[
                ("risk_annotation_object", annotation.risk_annotation_id),
                ("tool_object", tool_id),
            ],
            object_relations=[(annotation.risk_annotation_id, tool_id, "annotates_tool")],
        )
        return annotation

    def update_tool_risk_annotation(
        self,
        *,
        annotation: ToolRiskAnnotation,
        risk_level: str | None = None,
        risk_category: str | None = None,
        rationale: str | None = None,
        status: str | None = None,
        annotation_attrs: dict[str, Any] | None = None,
    ) -> ToolRiskAnnotation:
        updated = replace(
            annotation,
            risk_level=annotation.risk_level if risk_level is None else risk_level,
            risk_category=annotation.risk_category if risk_category is None else risk_category,
            rationale=annotation.rationale if rationale is None else rationale,
            status=annotation.status if status is None else status,
            updated_at=utc_now_iso(),
            annotation_attrs={**annotation.annotation_attrs, **dict(annotation_attrs or {})},
        )
        self._record_tool_event(
            "tool_risk_annotation_updated",
            risk_annotation=updated,
            event_attrs={},
            event_relations=[
                ("risk_annotation_object", updated.risk_annotation_id),
                ("tool_object", updated.tool_id),
            ],
            object_relations=[(updated.risk_annotation_id, updated.tool_id, "annotates_tool")],
        )
        return updated

    def render_tools_view(
        self,
        *,
        tools: list[ToolDescriptor],
        snapshot: ToolRegistrySnapshot | None = None,
        root: Path | str | None = None,
    ) -> MaterializedView:
        target = get_tool_view_paths(root or self.root)["tools"]
        view = render_tools_view(tools=tools, snapshot=snapshot, target_path=str(target))
        self._record_view_event("tool_registry_view_rendered", view, snapshot=snapshot)
        return view

    def render_tool_policy_view(
        self,
        *,
        tools: list[ToolDescriptor],
        policy_notes: list[ToolPolicyNote],
        risk_annotations: list[ToolRiskAnnotation],
        root: Path | str | None = None,
    ) -> MaterializedView:
        target = get_tool_view_paths(root or self.root)["tool_policy"]
        view = render_tool_policy_view(
            tools=tools,
            policy_notes=policy_notes,
            risk_annotations=risk_annotations,
            target_path=str(target),
        )
        self._record_view_event(
            "tool_policy_view_rendered",
            view,
            policy_notes=policy_notes,
            risk_annotations=risk_annotations,
        )
        return view

    def write_tool_views(
        self,
        *,
        tools: list[ToolDescriptor],
        snapshot: ToolRegistrySnapshot | None = None,
        policy_notes: list[ToolPolicyNote] | None = None,
        risk_annotations: list[ToolRiskAnnotation] | None = None,
        root: Path | str | None = None,
        overwrite: bool = True,
    ) -> dict[str, Any]:
        root_path = Path(root) if root is not None else self.root
        tools_view = self.render_tools_view(tools=tools, snapshot=snapshot, root=root_path)
        policy_view = self.render_tool_policy_view(
            tools=tools,
            policy_notes=policy_notes or [],
            risk_annotations=risk_annotations or [],
            root=root_path,
        )
        results: dict[str, Any] = {}
        for key, view, event_activity in [
            ("tools", tools_view, "tool_registry_view_written"),
            ("tool_policy", policy_view, "tool_policy_view_written"),
        ]:
            target = Path(view.target_path)
            if target.exists() and not overwrite:
                results[key] = {"written": False, "target_path": str(target), "skipped_reason": "target exists and overwrite is False"}
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(view.content, encoding="utf-8")
            self._record_view_event(event_activity, view, snapshot=snapshot, policy_notes=policy_notes or [], risk_annotations=risk_annotations or [])
            results[key] = {"written": True, "target_path": str(target), "view": view}
        return results

    def _record_tool_event(
        self,
        event_activity: str,
        *,
        descriptor: ToolDescriptor | None = None,
        descriptors: list[ToolDescriptor] | None = None,
        snapshot: ToolRegistrySnapshot | None = None,
        policy_note: ToolPolicyNote | None = None,
        risk_annotation: ToolRiskAnnotation | None = None,
        event_attrs: dict[str, Any],
        event_relations: list[tuple[str, str]],
        object_relations: list[tuple[str, str, str]],
    ) -> None:
        objects: list[OCELObject] = []
        if descriptor is not None:
            objects.append(self._descriptor_object(descriptor))
        for item in descriptors or []:
            objects.append(self._descriptor_object(item))
        if snapshot is not None:
            objects.append(self._snapshot_object(snapshot))
        if policy_note is not None:
            objects.append(self._policy_note_object(policy_note))
        if risk_annotation is not None:
            objects.append(self._risk_annotation_object(risk_annotation))
        self._append_record(
            event_activity=event_activity,
            objects=objects,
            event_relations=event_relations,
            object_relations=object_relations,
            event_attrs=event_attrs,
        )

    def _record_view_event(
        self,
        event_activity: str,
        view: MaterializedView,
        *,
        snapshot: ToolRegistrySnapshot | None = None,
        policy_notes: list[ToolPolicyNote] | None = None,
        risk_annotations: list[ToolRiskAnnotation] | None = None,
    ) -> None:
        objects = [self._view_object(view)]
        event_relations = [("view_object", view.view_id)]
        object_relations: list[tuple[str, str, str]] = []
        if snapshot is not None:
            objects.append(self._snapshot_object(snapshot))
            event_relations.append(("snapshot_object", snapshot.snapshot_id))
        for note in policy_notes or []:
            objects.append(self._policy_note_object(note))
            event_relations.append(("policy_note_object", note.policy_note_id))
        for annotation in risk_annotations or []:
            objects.append(self._risk_annotation_object(annotation))
            event_relations.append(("risk_annotation_object", annotation.risk_annotation_id))
        self._append_record(
            event_activity=event_activity,
            objects=objects,
            event_relations=event_relations,
            object_relations=object_relations,
            event_attrs={"view_type": view.view_type, "target_path": view.target_path, "canonical": False},
        )

    def _append_record(
        self,
        *,
        event_activity: str,
        objects: list[OCELObject],
        event_relations: list[tuple[str, str]],
        object_relations: list[tuple[str, str, str]],
        event_attrs: dict[str, Any],
    ) -> None:
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity=event_activity,
            event_timestamp=utc_now_iso(),
            event_attrs={
                **event_attrs,
                "runtime_event_type": event_activity,
                "source_runtime": "chanta_core",
                "informational_only": True,
                "enforcement_enabled": False,
                "runtime_registry_mutated": False,
            },
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
        self.trace_service.record_session_ocel_record(
            OCELRecord(event=event, objects=objects, relations=relations)
        )

    @staticmethod
    def _descriptor_object(descriptor: ToolDescriptor) -> OCELObject:
        return OCELObject(
            object_id=descriptor.tool_id,
            object_type="tool_descriptor",
            object_attrs={**descriptor.to_dict(), "object_key": descriptor.tool_id, "display_name": descriptor.tool_name},
        )

    @staticmethod
    def _snapshot_object(snapshot: ToolRegistrySnapshot) -> OCELObject:
        return OCELObject(
            object_id=snapshot.snapshot_id,
            object_type="tool_registry_snapshot",
            object_attrs={**snapshot.to_dict(), "object_key": snapshot.snapshot_id, "display_name": snapshot.snapshot_name or snapshot.snapshot_id},
        )

    @staticmethod
    def _policy_note_object(note: ToolPolicyNote) -> OCELObject:
        return OCELObject(
            object_id=note.policy_note_id,
            object_type="tool_policy_note",
            object_attrs={**note.to_dict(), "object_key": note.policy_note_id, "display_name": note.tool_name or note.policy_note_id},
        )

    @staticmethod
    def _risk_annotation_object(annotation: ToolRiskAnnotation) -> OCELObject:
        return OCELObject(
            object_id=annotation.risk_annotation_id,
            object_type="tool_risk_annotation",
            object_attrs={**annotation.to_dict(), "object_key": annotation.risk_annotation_id, "display_name": annotation.tool_id},
        )

    @staticmethod
    def _view_object(view: MaterializedView) -> OCELObject:
        return OCELObject(
            object_id=view.view_id,
            object_type="materialized_view",
            object_attrs={
                "object_key": view.view_id,
                "display_name": view.title,
                "view_type": view.view_type,
                "title": view.title,
                "target_path": view.target_path,
                "content_hash": view.content_hash,
                "generated_at": view.generated_at,
                "source_kind": view.source_kind,
                "canonical": False,
            },
        )
