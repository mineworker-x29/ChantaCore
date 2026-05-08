from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any
from uuid import uuid4

from chanta_core.delegation.errors import (
    SidechainContextEntryError,
    SidechainContextError,
    SidechainReturnEnvelopeError,
)
from chanta_core.delegation.ids import (
    new_sidechain_context_entry_id,
    new_sidechain_context_id,
    new_sidechain_context_snapshot_id,
    new_sidechain_return_envelope_id,
)
from chanta_core.delegation.models import DelegatedProcessRun, DelegationPacket, RESULT_STATUSES
from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


SIDECHAIN_CONTEXT_TYPES = {"delegation", "subagent", "verification", "analysis", "review", "manual", "other"}
SIDECHAIN_ISOLATION_MODES = {"packet_only", "sidechain", "external", "other"}
SIDECHAIN_STATUSES = {"created", "ready", "sealed", "archived", "error"}
SIDECHAIN_ENTRY_TYPES = {
    "goal",
    "context_summary",
    "structured_input",
    "object_ref",
    "allowed_capability",
    "expected_output_schema",
    "termination_condition",
    "permission_ref",
    "sandbox_ref",
    "risk_ref",
    "outcome_ref",
    "instruction",
    "manual",
    "other",
}


def _require_value(value: str, allowed: set[str], error_type: type[Exception], field_name: str) -> None:
    if value not in allowed:
        raise error_type(f"Unsupported {field_name}: {value}")


@dataclass(frozen=True)
class SidechainContext:
    sidechain_context_id: str
    packet_id: str
    delegated_run_id: str | None
    parent_session_id: str | None
    child_session_id: str | None
    parent_process_instance_id: str | None
    child_process_instance_id: str | None
    context_type: str
    isolation_mode: str
    status: str
    created_at: str
    entry_ids: list[str]
    safety_ref_ids: list[str]
    contains_full_parent_transcript: bool
    inherited_permissions: bool
    context_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.context_type, SIDECHAIN_CONTEXT_TYPES, SidechainContextError, "context_type")
        _require_value(self.isolation_mode, SIDECHAIN_ISOLATION_MODES, SidechainContextError, "isolation_mode")
        _require_value(self.status, SIDECHAIN_STATUSES, SidechainContextError, "status")
        if self.contains_full_parent_transcript is not False:
            raise SidechainContextError("contains_full_parent_transcript must be False in v0.13.1")
        if self.inherited_permissions is not False:
            raise SidechainContextError("inherited_permissions must be False in v0.13.1")

    def to_dict(self) -> dict[str, Any]:
        return {
            "sidechain_context_id": self.sidechain_context_id,
            "packet_id": self.packet_id,
            "delegated_run_id": self.delegated_run_id,
            "parent_session_id": self.parent_session_id,
            "child_session_id": self.child_session_id,
            "parent_process_instance_id": self.parent_process_instance_id,
            "child_process_instance_id": self.child_process_instance_id,
            "context_type": self.context_type,
            "isolation_mode": self.isolation_mode,
            "status": self.status,
            "created_at": self.created_at,
            "entry_ids": self.entry_ids,
            "safety_ref_ids": self.safety_ref_ids,
            "contains_full_parent_transcript": self.contains_full_parent_transcript,
            "inherited_permissions": self.inherited_permissions,
            "context_attrs": self.context_attrs,
        }


@dataclass(frozen=True)
class SidechainContextEntry:
    entry_id: str
    sidechain_context_id: str
    entry_type: str
    title: str | None
    content: str | None
    content_ref: str | None
    payload: dict[str, Any]
    source_kind: str | None
    source_ref: str | None
    priority: int | None
    created_at: str
    entry_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.entry_type, SIDECHAIN_ENTRY_TYPES, SidechainContextEntryError, "entry_type")

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "sidechain_context_id": self.sidechain_context_id,
            "entry_type": self.entry_type,
            "title": self.title,
            "content": self.content,
            "content_ref": self.content_ref,
            "payload": self.payload,
            "source_kind": self.source_kind,
            "source_ref": self.source_ref,
            "priority": self.priority,
            "created_at": self.created_at,
            "entry_attrs": self.entry_attrs,
        }


@dataclass(frozen=True)
class SidechainContextSnapshot:
    snapshot_id: str
    sidechain_context_id: str
    packet_id: str
    delegated_run_id: str | None
    created_at: str
    entry_ids: list[str]
    entry_count: int
    summary: str | None
    snapshot_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "sidechain_context_id": self.sidechain_context_id,
            "packet_id": self.packet_id,
            "delegated_run_id": self.delegated_run_id,
            "created_at": self.created_at,
            "entry_ids": self.entry_ids,
            "entry_count": self.entry_count,
            "summary": self.summary,
            "snapshot_attrs": self.snapshot_attrs,
        }


@dataclass(frozen=True)
class SidechainReturnEnvelope:
    envelope_id: str
    sidechain_context_id: str
    delegated_run_id: str | None
    packet_id: str
    status: str
    summary: str | None
    output_payload: dict[str, Any]
    evidence_refs: list[dict[str, Any]]
    recommendation_refs: list[dict[str, Any]]
    failure: dict[str, Any] | None
    contains_full_child_transcript: bool
    created_at: str
    envelope_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.status, RESULT_STATUSES, SidechainReturnEnvelopeError, "status")
        if self.contains_full_child_transcript is not False:
            raise SidechainReturnEnvelopeError("contains_full_child_transcript must be False in v0.13.1")

    def to_dict(self) -> dict[str, Any]:
        return {
            "envelope_id": self.envelope_id,
            "sidechain_context_id": self.sidechain_context_id,
            "delegated_run_id": self.delegated_run_id,
            "packet_id": self.packet_id,
            "status": self.status,
            "summary": self.summary,
            "output_payload": self.output_payload,
            "evidence_refs": self.evidence_refs,
            "recommendation_refs": self.recommendation_refs,
            "failure": self.failure,
            "contains_full_child_transcript": self.contains_full_child_transcript,
            "created_at": self.created_at,
            "envelope_attrs": self.envelope_attrs,
        }


class SidechainContextService:
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

    def create_sidechain_context_from_packet(
        self,
        *,
        packet: DelegationPacket,
        delegated_run: DelegatedProcessRun | None = None,
        child_session_id: str | None = None,
        child_process_instance_id: str | None = None,
        context_type: str = "delegation",
        isolation_mode: str = "packet_only",
        context_attrs: dict[str, Any] | None = None,
    ) -> SidechainContext:
        safety_ref_ids = self._safety_ref_ids(packet)
        context = SidechainContext(
            sidechain_context_id=new_sidechain_context_id(),
            packet_id=packet.packet_id,
            delegated_run_id=delegated_run.delegated_run_id if delegated_run else None,
            parent_session_id=packet.parent_session_id,
            child_session_id=child_session_id or (delegated_run.child_session_id if delegated_run else None),
            parent_process_instance_id=packet.parent_process_instance_id,
            child_process_instance_id=child_process_instance_id
            or (delegated_run.child_process_instance_id if delegated_run else None),
            context_type=context_type,
            isolation_mode=isolation_mode,
            status="created",
            created_at=utc_now_iso(),
            entry_ids=[],
            safety_ref_ids=safety_ref_ids,
            contains_full_parent_transcript=False,
            inherited_permissions=False,
            context_attrs={
                **dict(context_attrs or {}),
                "packet_id": packet.packet_id,
                "packet_metadata_only": True,
                "runtime_effect": False,
            },
        )
        self._record_context_event("sidechain_context_created", context=context, packet=packet, event_attrs={})
        self._record_context_event(
            "sidechain_parent_transcript_excluded",
            context=context,
            packet=packet,
            event_attrs={"contains_full_parent_transcript": False},
        )
        self._record_context_event(
            "sidechain_permission_inheritance_prevented",
            context=context,
            packet=packet,
            event_attrs={"inherited_permissions": False},
        )
        return context

    def add_context_entry(
        self,
        *,
        sidechain_context_id: str,
        entry_type: str,
        title: str | None = None,
        content: str | None = None,
        content_ref: str | None = None,
        payload: dict[str, Any] | None = None,
        source_kind: str | None = None,
        source_ref: str | None = None,
        priority: int | None = None,
        entry_attrs: dict[str, Any] | None = None,
    ) -> SidechainContextEntry:
        entry = SidechainContextEntry(
            entry_id=new_sidechain_context_entry_id(),
            sidechain_context_id=sidechain_context_id,
            entry_type=entry_type,
            title=title,
            content=content,
            content_ref=content_ref,
            payload=dict(payload or {}),
            source_kind=source_kind,
            source_ref=source_ref,
            priority=priority,
            created_at=utc_now_iso(),
            entry_attrs=dict(entry_attrs or {}),
        )
        self._record_event(
            "sidechain_context_entry_added",
            entry=entry,
            event_attrs={"entry_type": entry.entry_type},
            event_relations=[
                ("sidechain_context_entry_object", entry.entry_id),
                ("sidechain_context_object", sidechain_context_id),
            ],
            object_relations=[(entry.entry_id, sidechain_context_id, "belongs_to_sidechain_context")],
        )
        return entry

    def build_entries_from_packet(
        self,
        *,
        context: SidechainContext,
        packet: DelegationPacket,
    ) -> list[SidechainContextEntry]:
        entries: list[SidechainContextEntry] = [
            self.add_context_entry(
                sidechain_context_id=context.sidechain_context_id,
                entry_type="goal",
                title="Goal",
                content=packet.goal,
                payload={"goal": packet.goal},
                source_kind="delegation_packet",
                source_ref=packet.packet_id,
                priority=70,
                entry_attrs={"packet_id": packet.packet_id},
            )
        ]
        if packet.context_summary:
            entries.append(
                self.add_context_entry(
                    sidechain_context_id=context.sidechain_context_id,
                    entry_type="context_summary",
                    title="Context Summary",
                    content=packet.context_summary,
                    payload={"context_summary": packet.context_summary},
                    source_kind="delegation_packet",
                    source_ref=packet.packet_id,
                    priority=65,
                    entry_attrs={"packet_id": packet.packet_id},
                )
            )
        if packet.structured_inputs:
            entries.append(
                self.add_context_entry(
                    sidechain_context_id=context.sidechain_context_id,
                    entry_type="structured_input",
                    title="Structured Inputs",
                    payload=dict(packet.structured_inputs),
                    source_kind="delegation_packet",
                    source_ref=packet.packet_id,
                    priority=60,
                    entry_attrs={"packet_id": packet.packet_id},
                )
            )
        for object_ref in packet.object_refs:
            entries.append(
                self.add_context_entry(
                    sidechain_context_id=context.sidechain_context_id,
                    entry_type="object_ref",
                    title="Object Reference",
                    payload=dict(object_ref),
                    source_kind="delegation_packet",
                    source_ref=packet.packet_id,
                    priority=55,
                    entry_attrs={"packet_id": packet.packet_id},
                )
            )
        for capability in packet.allowed_capabilities:
            entries.append(
                self.add_context_entry(
                    sidechain_context_id=context.sidechain_context_id,
                    entry_type="allowed_capability",
                    title="Allowed Capability",
                    content=capability,
                    payload={"capability": capability},
                    source_kind="delegation_packet",
                    source_ref=packet.packet_id,
                    priority=50,
                    entry_attrs={"packet_id": packet.packet_id},
                )
            )
        if packet.expected_output_schema:
            entries.append(
                self.add_context_entry(
                    sidechain_context_id=context.sidechain_context_id,
                    entry_type="expected_output_schema",
                    title="Expected Output Schema",
                    payload=dict(packet.expected_output_schema),
                    source_kind="delegation_packet",
                    source_ref=packet.packet_id,
                    priority=55,
                    entry_attrs={"packet_id": packet.packet_id},
                )
            )
        if packet.termination_conditions:
            entries.append(
                self.add_context_entry(
                    sidechain_context_id=context.sidechain_context_id,
                    entry_type="termination_condition",
                    title="Termination Conditions",
                    payload=dict(packet.termination_conditions),
                    source_kind="delegation_packet",
                    source_ref=packet.packet_id,
                    priority=55,
                    entry_attrs={"packet_id": packet.packet_id},
                )
            )
        entries.extend(self._ref_entries(context=context, packet=packet))
        if context.safety_ref_ids:
            self._record_context_event(
                "sidechain_safety_refs_attached",
                context=context,
                packet=packet,
                event_attrs={"safety_ref_count": len(context.safety_ref_ids)},
            )
        return entries

    def mark_context_ready(
        self,
        *,
        context: SidechainContext,
        entry_ids: list[str] | None = None,
        reason: str | None = None,
    ) -> SidechainContext:
        updated = replace(context, status="ready", entry_ids=list(entry_ids or context.entry_ids))
        self._record_context_event(
            "sidechain_context_ready",
            context=updated,
            packet=None,
            event_attrs={"reason": reason, "entry_count": len(updated.entry_ids)},
        )
        return updated

    def seal_context(
        self,
        *,
        context: SidechainContext,
        reason: str | None = None,
    ) -> SidechainContext:
        updated = replace(context, status="sealed")
        self._record_context_event("sidechain_context_sealed", context=updated, packet=None, event_attrs={"reason": reason})
        return updated

    def archive_context(
        self,
        *,
        context: SidechainContext,
        reason: str | None = None,
    ) -> SidechainContext:
        updated = replace(context, status="archived")
        self._record_context_event(
            "sidechain_context_archived",
            context=updated,
            packet=None,
            event_attrs={"reason": reason},
        )
        return updated

    def mark_context_error(
        self,
        *,
        context: SidechainContext,
        failure: dict[str, Any] | None = None,
        reason: str | None = None,
    ) -> SidechainContext:
        updated = replace(context, status="error", context_attrs={**context.context_attrs, "failure": dict(failure or {})})
        self._record_context_event(
            "sidechain_context_error",
            context=updated,
            packet=None,
            event_attrs={"reason": reason, "failure": failure},
        )
        return updated

    def build_snapshot(
        self,
        *,
        context: SidechainContext,
        entries: list[SidechainContextEntry],
        summary: str | None = None,
        snapshot_attrs: dict[str, Any] | None = None,
    ) -> SidechainContextSnapshot:
        entry_ids = [entry.entry_id for entry in entries]
        snapshot = SidechainContextSnapshot(
            snapshot_id=new_sidechain_context_snapshot_id(),
            sidechain_context_id=context.sidechain_context_id,
            packet_id=context.packet_id,
            delegated_run_id=context.delegated_run_id,
            created_at=utc_now_iso(),
            entry_ids=entry_ids,
            entry_count=len(entry_ids),
            summary=summary,
            snapshot_attrs=dict(snapshot_attrs or {}),
        )
        self._record_event(
            "sidechain_context_snapshot_created",
            context=context,
            snapshot=snapshot,
            event_attrs={"entry_count": snapshot.entry_count},
            event_relations=[
                ("snapshot_object", snapshot.snapshot_id),
                ("sidechain_context_object", context.sidechain_context_id),
                ("packet_object", context.packet_id),
                *self._optional_run_relation(context),
            ],
            object_relations=[
                (snapshot.snapshot_id, context.sidechain_context_id, "snapshot_of_sidechain_context"),
            ],
        )
        return snapshot

    def record_return_envelope(
        self,
        *,
        sidechain_context_id: str,
        packet_id: str,
        delegated_run_id: str | None = None,
        status: str,
        summary: str | None = None,
        output_payload: dict[str, Any] | None = None,
        evidence_refs: list[dict[str, Any]] | None = None,
        recommendation_refs: list[dict[str, Any]] | None = None,
        failure: dict[str, Any] | None = None,
        envelope_attrs: dict[str, Any] | None = None,
    ) -> SidechainReturnEnvelope:
        envelope = SidechainReturnEnvelope(
            envelope_id=new_sidechain_return_envelope_id(),
            sidechain_context_id=sidechain_context_id,
            delegated_run_id=delegated_run_id,
            packet_id=packet_id,
            status=status,
            summary=summary,
            output_payload=dict(output_payload or {}),
            evidence_refs=list(evidence_refs or []),
            recommendation_refs=list(recommendation_refs or []),
            failure=failure,
            contains_full_child_transcript=False,
            created_at=utc_now_iso(),
            envelope_attrs=dict(envelope_attrs or {}),
        )
        event_relations = [
            ("envelope_object", envelope.envelope_id),
            ("sidechain_context_object", sidechain_context_id),
            ("packet_object", packet_id),
        ]
        object_relations = [(envelope.envelope_id, sidechain_context_id, "return_of_sidechain_context")]
        if delegated_run_id:
            event_relations.append(("delegated_run_object", delegated_run_id))
            object_relations.append((envelope.envelope_id, delegated_run_id, "return_of_delegated_run"))
        self._record_event(
            "sidechain_return_envelope_recorded",
            envelope=envelope,
            event_attrs={"status": status, "contains_full_child_transcript": False},
            event_relations=event_relations,
            object_relations=object_relations,
        )
        return envelope

    def _ref_entries(self, *, context: SidechainContext, packet: DelegationPacket) -> list[SidechainContextEntry]:
        entries: list[SidechainContextEntry] = []
        entries.extend(
            self._entries_for_ids(
                context=context,
                packet=packet,
                entry_type="permission_ref",
                title="Permission Request Reference",
                source_kind="permission_request",
                ids=packet.permission_request_ids,
                priority=80,
            )
        )
        entries.extend(
            self._entries_for_ids(
                context=context,
                packet=packet,
                entry_type="permission_ref",
                title="Session Permission Resolution Reference",
                source_kind="session_permission_resolution",
                ids=packet.session_permission_resolution_ids,
                priority=80,
            )
        )
        entries.extend(
            self._entries_for_ids(
                context=context,
                packet=packet,
                entry_type="sandbox_ref",
                title="Workspace Write Sandbox Reference",
                source_kind="workspace_write_sandbox_decision",
                ids=packet.workspace_write_sandbox_decision_ids,
                priority=85,
            )
        )
        entries.extend(
            self._entries_for_ids(
                context=context,
                packet=packet,
                entry_type="risk_ref",
                title="Shell Network Pre Sandbox Reference",
                source_kind="shell_network_pre_sandbox_decision",
                ids=packet.shell_network_pre_sandbox_decision_ids,
                priority=85,
            )
        )
        entries.extend(
            self._entries_for_ids(
                context=context,
                packet=packet,
                entry_type="outcome_ref",
                title="Process Outcome Evaluation Reference",
                source_kind="process_outcome_evaluation",
                ids=packet.process_outcome_evaluation_ids,
                priority=75,
            )
        )
        return entries

    def _entries_for_ids(
        self,
        *,
        context: SidechainContext,
        packet: DelegationPacket,
        entry_type: str,
        title: str,
        source_kind: str,
        ids: list[str],
        priority: int,
    ) -> list[SidechainContextEntry]:
        return [
            self.add_context_entry(
                sidechain_context_id=context.sidechain_context_id,
                entry_type=entry_type,
                title=title,
                content_ref=ref_id,
                payload={"ref_id": ref_id, "ref_kind": source_kind},
                source_kind=source_kind,
                source_ref=ref_id,
                priority=priority,
                entry_attrs={"packet_id": packet.packet_id},
            )
            for ref_id in ids
        ]

    def _record_context_event(
        self,
        event_activity: str,
        *,
        context: SidechainContext,
        packet: DelegationPacket | None,
        event_attrs: dict[str, Any],
    ) -> None:
        event_relations, object_relations = self._context_relations(context)
        self._record_event(
            event_activity,
            context=context,
            packet=packet,
            event_attrs={"status": context.status, **event_attrs},
            event_relations=[
                ("sidechain_context_object", context.sidechain_context_id),
                ("packet_object", context.packet_id),
                *event_relations,
            ],
            object_relations=[
                (context.sidechain_context_id, context.packet_id, "derived_from_packet"),
                *object_relations,
            ],
        )

    def _record_event(
        self,
        event_activity: str,
        *,
        context: SidechainContext | None = None,
        entry: SidechainContextEntry | None = None,
        snapshot: SidechainContextSnapshot | None = None,
        envelope: SidechainReturnEnvelope | None = None,
        packet: DelegationPacket | None = None,
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
                "sidechain_context_model_only": True,
                "runtime_effect": False,
                "enforcement_enabled": False,
            },
        )
        objects = self._objects_for_event(
            context=context,
            entry=entry,
            snapshot=snapshot,
            envelope=envelope,
            packet=packet,
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
        context: SidechainContext | None,
        entry: SidechainContextEntry | None,
        snapshot: SidechainContextSnapshot | None,
        envelope: SidechainReturnEnvelope | None,
        packet: DelegationPacket | None,
        event_relations: list[tuple[str, str]],
    ) -> list[OCELObject]:
        objects: list[OCELObject] = []
        if context is not None:
            objects.append(self._context_object(context))
        if entry is not None:
            objects.append(self._entry_object(entry))
        if snapshot is not None:
            objects.append(self._snapshot_object(snapshot))
        if envelope is not None:
            objects.append(self._envelope_object(envelope))
        if packet is not None:
            objects.append(self._packet_object(packet))
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
    def _context_object(context: SidechainContext) -> OCELObject:
        return OCELObject(
            object_id=context.sidechain_context_id,
            object_type="sidechain_context",
            object_attrs={
                **context.to_dict(),
                "object_key": context.sidechain_context_id,
                "display_name": context.context_type,
                "contains_full_parent_transcript": False,
                "inherited_permissions": False,
            },
        )

    @staticmethod
    def _entry_object(entry: SidechainContextEntry) -> OCELObject:
        return OCELObject(
            object_id=entry.entry_id,
            object_type="sidechain_context_entry",
            object_attrs={**entry.to_dict(), "object_key": entry.entry_id, "display_name": entry.title or entry.entry_type},
        )

    @staticmethod
    def _snapshot_object(snapshot: SidechainContextSnapshot) -> OCELObject:
        return OCELObject(
            object_id=snapshot.snapshot_id,
            object_type="sidechain_context_snapshot",
            object_attrs={**snapshot.to_dict(), "object_key": snapshot.snapshot_id, "display_name": "snapshot"},
        )

    @staticmethod
    def _envelope_object(envelope: SidechainReturnEnvelope) -> OCELObject:
        return OCELObject(
            object_id=envelope.envelope_id,
            object_type="sidechain_return_envelope",
            object_attrs={
                **envelope.to_dict(),
                "object_key": envelope.envelope_id,
                "display_name": envelope.status,
                "contains_full_child_transcript": False,
            },
        )

    @staticmethod
    def _packet_object(packet: DelegationPacket) -> OCELObject:
        return OCELObject(
            object_id=packet.packet_id,
            object_type="delegation_packet",
            object_attrs={
                **packet.to_dict(),
                "object_key": packet.packet_id,
                "display_name": packet.packet_name or packet.goal,
                "contains_full_parent_transcript": False,
            },
        )

    @staticmethod
    def _placeholder_object(qualifier: str, object_id: str) -> OCELObject | None:
        placeholder_types = {
            "parent_session": "session",
            "child_session": "session",
            "parent_process": "process_instance",
            "child_process": "process_instance",
        }
        object_type = placeholder_types.get(qualifier)
        if object_type is None:
            return None
        return OCELObject(object_id=object_id, object_type=object_type, object_attrs={"object_key": object_id})

    def _context_relations(self, context: SidechainContext) -> tuple[list[tuple[str, str]], list[tuple[str, str, str]]]:
        event_relations: list[tuple[str, str]] = []
        object_relations: list[tuple[str, str, str]] = []
        if context.delegated_run_id:
            event_relations.append(("delegated_run_object", context.delegated_run_id))
            object_relations.append(
                (context.sidechain_context_id, context.delegated_run_id, "belongs_to_delegated_run")
            )
        if context.parent_session_id:
            session_object_id = self._session_object_id(context.parent_session_id)
            event_relations.append(("parent_session", session_object_id))
            object_relations.append((context.sidechain_context_id, session_object_id, "parent_session"))
        if context.child_session_id:
            session_object_id = self._session_object_id(context.child_session_id)
            event_relations.append(("child_session", session_object_id))
            object_relations.append((context.sidechain_context_id, session_object_id, "child_session"))
        if context.parent_process_instance_id:
            event_relations.append(("parent_process", context.parent_process_instance_id))
            object_relations.append(
                (context.sidechain_context_id, context.parent_process_instance_id, "parent_process_instance")
            )
        if context.child_process_instance_id:
            event_relations.append(("child_process", context.child_process_instance_id))
            object_relations.append(
                (context.sidechain_context_id, context.child_process_instance_id, "child_process_instance")
            )
        return event_relations, object_relations

    @staticmethod
    def _optional_run_relation(context: SidechainContext) -> list[tuple[str, str]]:
        if context.delegated_run_id:
            return [("delegated_run_object", context.delegated_run_id)]
        return []

    @staticmethod
    def _session_object_id(session_id: str) -> str:
        return session_id if session_id.startswith("session:") else f"session:{session_id}"

    @staticmethod
    def _safety_ref_ids(packet: DelegationPacket) -> list[str]:
        return [
            *packet.permission_request_ids,
            *packet.session_permission_resolution_ids,
            *packet.workspace_write_sandbox_decision_ids,
            *packet.shell_network_pre_sandbox_decision_ids,
            *packet.process_outcome_evaluation_ids,
        ]
