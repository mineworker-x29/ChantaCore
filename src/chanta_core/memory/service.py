from __future__ import annotations

from dataclasses import replace
from typing import Any
from uuid import uuid4

from chanta_core.memory.ids import new_memory_entry_id, new_memory_revision_id
from chanta_core.memory.models import (
    MemoryEntry,
    MemoryRevision,
    hash_content,
    preview_text,
)
from chanta_core.ocel.models import OCELObject, OCELRecord, OCELEvent, OCELRelation
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


MEMORY_EVENTS = {
    "memory_entry_created",
    "memory_entry_revised",
    "memory_entry_superseded",
    "memory_entry_archived",
    "memory_entry_withdrawn",
    "memory_revision_recorded",
    "memory_derived_from_message",
    "memory_attached_to_session",
    "memory_attached_to_turn",
}


class MemoryService:
    def __init__(self, *, trace_service: TraceService | None = None) -> None:
        self.trace_service = trace_service or TraceService()

    def create_memory_entry(
        self,
        *,
        memory_type: str,
        title: str,
        content: str,
        status: str = "active",
        confidence: float | None = None,
        valid_from: str | None = None,
        valid_until: str | None = None,
        contradiction_status: str = "unknown",
        source_kind: str | None = None,
        scope: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        message_id: str | None = None,
        memory_attrs: dict[str, Any] | None = None,
    ) -> MemoryEntry:
        now = utc_now_iso()
        memory = MemoryEntry(
            memory_id=new_memory_entry_id(),
            memory_type=memory_type,
            title=title,
            content=content,
            content_preview=preview_text(content),
            content_hash=hash_content(content),
            status=status,
            confidence=confidence,
            created_at=now,
            updated_at=now,
            valid_from=valid_from,
            valid_until=valid_until,
            contradiction_status=contradiction_status,
            source_kind=source_kind,
            scope=scope,
            memory_attrs=dict(memory_attrs or {}),
        )
        revision = self._revision(
            memory=memory,
            operation="create",
            before_hash=None,
            reason="initial memory creation",
            actor_type=None,
            revision_index=1,
        )
        self._record_memory_event(
            "memory_entry_created",
            memory=memory,
            revision=None,
            event_attrs={"session_id": session_id, "turn_id": turn_id, "message_id": message_id},
            session_id=session_id,
            turn_id=turn_id,
            message_id=message_id,
            object_relations=self._source_relations(memory, session_id, turn_id, message_id),
        )
        self._record_revision_event(revision, memory)
        if message_id:
            self._record_memory_event(
                "memory_derived_from_message",
                memory=memory,
                revision=None,
                event_attrs={"message_id": message_id},
                session_id=session_id,
                turn_id=turn_id,
                message_id=message_id,
                object_relations=self._source_relations(memory, session_id, turn_id, message_id),
            )
        return memory

    def revise_memory_entry(
        self,
        *,
        memory: MemoryEntry,
        new_content: str,
        reason: str | None = None,
        actor_type: str | None = None,
        memory_attrs: dict[str, Any] | None = None,
    ) -> tuple[MemoryEntry, MemoryRevision]:
        updated = replace(
            memory,
            content=new_content,
            content_preview=preview_text(new_content),
            content_hash=hash_content(new_content),
            updated_at=utc_now_iso(),
            memory_attrs={**memory.memory_attrs, **dict(memory_attrs or {})},
        )
        revision = self._revision(
            memory=updated,
            operation="revise",
            before_hash=memory.content_hash,
            reason=reason,
            actor_type=actor_type,
            revision_index=None,
        )
        self._record_memory_event(
            "memory_entry_revised",
            memory=updated,
            revision=revision,
            event_attrs={"reason": reason},
            session_id=None,
            turn_id=None,
            message_id=None,
            object_relations=[(revision.revision_id, updated.memory_id, "revises")],
        )
        self._record_revision_event(revision, updated)
        return updated, revision

    def supersede_memory_entry(
        self,
        *,
        old_memory: MemoryEntry,
        new_memory: MemoryEntry,
        reason: str | None = None,
    ) -> dict[str, Any]:
        self._record_memory_event(
            "memory_entry_superseded",
            memory=new_memory,
            revision=None,
            event_attrs={"old_memory_id": old_memory.memory_id, "reason": reason},
            session_id=None,
            turn_id=None,
            message_id=None,
            object_relations=[(new_memory.memory_id, old_memory.memory_id, "supersedes")],
            extra_objects=[self._memory_object(old_memory)],
        )
        return {"old_memory_id": old_memory.memory_id, "new_memory_id": new_memory.memory_id}

    def archive_memory_entry(
        self,
        *,
        memory: MemoryEntry,
        reason: str | None = None,
    ) -> MemoryEntry:
        archived = replace(memory, status="archived", updated_at=utc_now_iso())
        self._record_memory_event(
            "memory_entry_archived",
            memory=archived,
            revision=None,
            event_attrs={"reason": reason},
            session_id=None,
            turn_id=None,
            message_id=None,
            object_relations=[],
        )
        return archived

    def withdraw_memory_entry(
        self,
        *,
        memory: MemoryEntry,
        reason: str | None = None,
    ) -> MemoryEntry:
        withdrawn = replace(memory, status="withdrawn", updated_at=utc_now_iso())
        self._record_memory_event(
            "memory_entry_withdrawn",
            memory=withdrawn,
            revision=None,
            event_attrs={"reason": reason},
            session_id=None,
            turn_id=None,
            message_id=None,
            object_relations=[],
        )
        return withdrawn

    def attach_memory_to_session(
        self,
        *,
        memory_id: str,
        session_id: str,
        reason: str | None = None,
    ) -> dict[str, Any]:
        self._record_attachment_event(
            "memory_attached_to_session",
            memory_id=memory_id,
            session_id=session_id,
            turn_id=None,
            reason=reason,
        )
        return {"memory_id": memory_id, "session_id": session_id}

    def attach_memory_to_turn(
        self,
        *,
        memory_id: str,
        session_id: str | None,
        turn_id: str,
        reason: str | None = None,
    ) -> dict[str, Any]:
        self._record_attachment_event(
            "memory_attached_to_turn",
            memory_id=memory_id,
            session_id=session_id,
            turn_id=turn_id,
            reason=reason,
        )
        return {"memory_id": memory_id, "session_id": session_id, "turn_id": turn_id}

    def _revision(
        self,
        *,
        memory: MemoryEntry,
        operation: str,
        before_hash: str | None,
        reason: str | None,
        actor_type: str | None,
        revision_index: int | None,
    ) -> MemoryRevision:
        return MemoryRevision(
            revision_id=new_memory_revision_id(),
            memory_id=memory.memory_id,
            revision_index=revision_index,
            operation=operation,
            before_hash=before_hash,
            after_hash=memory.content_hash,
            content_preview=memory.content_preview,
            content_hash=memory.content_hash,
            reason=reason,
            created_at=utc_now_iso(),
            actor_type=actor_type,
        )

    def _record_revision_event(self, revision: MemoryRevision, memory: MemoryEntry) -> None:
        self._record_memory_event(
            "memory_revision_recorded",
            memory=memory,
            revision=revision,
            event_attrs={"operation": revision.operation},
            session_id=None,
            turn_id=None,
            message_id=None,
            object_relations=[(revision.revision_id, memory.memory_id, "revises")],
        )

    def _record_memory_event(
        self,
        event_activity: str,
        *,
        memory: MemoryEntry,
        revision: MemoryRevision | None,
        event_attrs: dict[str, Any],
        session_id: str | None,
        turn_id: str | None,
        message_id: str | None,
        object_relations: list[tuple[str, str, str]],
        extra_objects: list[OCELObject] | None = None,
    ) -> None:
        objects = [self._memory_object(memory), *(extra_objects or [])]
        event_relations = [("memory_object", memory.memory_id)]
        if revision is not None:
            objects.append(self._revision_object(revision))
            event_relations.append(("revision_object", revision.revision_id))
        if session_id:
            objects.append(self._session_object(session_id))
            event_relations.append(("source_session", self._session_object_id(session_id)))
        if turn_id:
            objects.append(self._turn_object(turn_id, session_id))
            event_relations.append(("source_turn", turn_id))
        if message_id:
            objects.append(self._message_object(message_id, session_id, turn_id))
            event_relations.append(("source_message", message_id))
        self._append_record(
            event_activity,
            objects=objects,
            event_relations=event_relations,
            object_relations=object_relations,
            event_attrs=event_attrs,
        )

    def _record_attachment_event(
        self,
        event_activity: str,
        *,
        memory_id: str,
        session_id: str | None,
        turn_id: str | None,
        reason: str | None,
    ) -> None:
        objects = [self._memory_placeholder(memory_id)]
        event_relations = [("memory_object", memory_id)]
        object_relations: list[tuple[str, str, str]] = []
        if session_id:
            objects.append(self._session_object(session_id))
            event_relations.append(("source_session", self._session_object_id(session_id)))
            object_relations.append((memory_id, self._session_object_id(session_id), "belongs_to_session"))
        if turn_id:
            objects.append(self._turn_object(turn_id, session_id))
            event_relations.append(("source_turn", turn_id))
            object_relations.append((memory_id, turn_id, "derived_from_turn"))
        self._append_record(
            event_activity,
            objects=objects,
            event_relations=event_relations,
            object_relations=object_relations,
            event_attrs={"reason": reason},
        )

    def _append_record(
        self,
        event_activity: str,
        *,
        objects: list[OCELObject],
        event_relations: list[tuple[str, str]],
        object_relations: list[tuple[str, str, str]],
        event_attrs: dict[str, Any],
    ) -> None:
        timestamp = utc_now_iso()
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity=event_activity,
            event_timestamp=timestamp,
            event_attrs={
                **event_attrs,
                "runtime_event_type": event_activity,
                "lifecycle": event_activity.removeprefix("memory_entry_"),
                "source_runtime": "chanta_core",
            },
        )
        relations = [
            OCELRelation.event_object(
                event_id=event.event_id,
                object_id=object_id,
                qualifier=qualifier,
            )
            for qualifier, object_id in event_relations
        ]
        relations.extend(
            OCELRelation.object_object(
                source_object_id=source,
                target_object_id=target,
                qualifier=qualifier,
            )
            for source, target, qualifier in object_relations
        )
        self.trace_service.record_session_ocel_record(
            OCELRecord(event=event, objects=objects, relations=relations)
        )

    def _source_relations(
        self,
        memory: MemoryEntry,
        session_id: str | None,
        turn_id: str | None,
        message_id: str | None,
    ) -> list[tuple[str, str, str]]:
        relations: list[tuple[str, str, str]] = []
        if session_id:
            relations.append((memory.memory_id, self._session_object_id(session_id), "belongs_to_session"))
        if turn_id:
            relations.append((memory.memory_id, turn_id, "derived_from_turn"))
        if message_id:
            relations.append((memory.memory_id, message_id, "derived_from_message"))
        return relations

    @staticmethod
    def _memory_object(memory: MemoryEntry) -> OCELObject:
        return OCELObject(
            object_id=memory.memory_id,
            object_type="memory_entry",
            object_attrs={**memory.to_dict(), "object_key": memory.memory_id, "display_name": memory.title},
        )

    @staticmethod
    def _memory_placeholder(memory_id: str) -> OCELObject:
        return OCELObject(
            object_id=memory_id,
            object_type="memory_entry",
            object_attrs={"object_key": memory_id, "display_name": memory_id},
        )

    @staticmethod
    def _revision_object(revision: MemoryRevision) -> OCELObject:
        return OCELObject(
            object_id=revision.revision_id,
            object_type="memory_revision",
            object_attrs={**revision.to_dict(), "object_key": revision.revision_id, "display_name": revision.operation},
        )

    @staticmethod
    def _session_object_id(session_id: str) -> str:
        return session_id if session_id.startswith("session:") else f"session:{session_id}"

    def _session_object(self, session_id: str) -> OCELObject:
        object_id = self._session_object_id(session_id)
        return OCELObject(
            object_id=object_id,
            object_type="session",
            object_attrs={"object_key": session_id, "display_name": f"Session {session_id}", "session_id": session_id},
        )

    @staticmethod
    def _turn_object(turn_id: str, session_id: str | None) -> OCELObject:
        return OCELObject(
            object_id=turn_id,
            object_type="conversation_turn",
            object_attrs={"object_key": turn_id, "display_name": turn_id, "session_id": session_id},
        )

    @staticmethod
    def _message_object(message_id: str, session_id: str | None, turn_id: str | None) -> OCELObject:
        return OCELObject(
            object_id=message_id,
            object_type="message",
            object_attrs={"object_key": message_id, "display_name": message_id, "session_id": session_id, "turn_id": turn_id},
        )
