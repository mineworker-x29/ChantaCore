from __future__ import annotations

from typing import Any
from uuid import uuid4

from chanta_core.context.history import ContextHistoryEntry, new_context_history_entry_id
from chanta_core.ocel.models import OCELObject, OCELRecord, OCELEvent, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.session.ids import (
    new_session_context_snapshot_id,
    new_session_fork_id,
    new_session_resume_id,
)
from chanta_core.session.models import ConversationTurn, SessionMessage
from chanta_core.session.service import SessionService
from chanta_core.session.snapshots import (
    SessionContextSnapshot,
    SessionForkResult,
    SessionResumeResult,
)
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


class SessionContinuityService:
    def __init__(
        self,
        *,
        session_service: SessionService | None = None,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        self.trace_service = trace_service or TraceService(ocel_store=ocel_store)
        self.session_service = session_service or SessionService(trace_service=self.trace_service)
        self.ocel_store = ocel_store or self.trace_service.ocel_store

    def build_session_context_snapshot(
        self,
        *,
        session_id: str,
        snapshot_type: str = "resume",
        max_turns: int | None = None,
        max_messages: int | None = None,
        include_system_messages: bool = False,
        include_tool_messages: bool = False,
        messages: list[SessionMessage] | None = None,
        turns: list[ConversationTurn] | None = None,
        process_instance_ids: list[str] | None = None,
        snapshot_attrs: dict[str, Any] | None = None,
    ) -> SessionContextSnapshot:
        resolved_messages = (
            list(messages)
            if messages is not None
            else self._load_messages_from_ocel(
                session_id=session_id,
                include_system_messages=include_system_messages,
                include_tool_messages=include_tool_messages,
            )
        )
        resolved_turns = (
            list(turns)
            if turns is not None
            else self._load_turns_from_ocel(session_id=session_id)
        )
        allowed_turn_ids = self._recent_turn_ids(resolved_turns, max_turns)
        if allowed_turn_ids is not None:
            resolved_messages = [
                message
                for message in resolved_messages
                if message.turn_id is None or message.turn_id in allowed_turn_ids
            ]
        resolved_messages = self._sort_messages(resolved_messages)
        if max_messages is not None:
            resolved_messages = resolved_messages[-max_messages:]
        included_message_ids = [message.message_id for message in resolved_messages]
        included_turn_ids = sorted(
            {
                *(turn.turn_id for turn in resolved_turns if allowed_turn_ids is None or turn.turn_id in allowed_turn_ids),
                *(message.turn_id for message in resolved_messages if message.turn_id),
            }
        )
        process_ids = sorted(
            {
                *(process_instance_ids or []),
                *(turn.process_instance_id for turn in resolved_turns if turn.process_instance_id),
                *(
                    str(message.message_attrs["process_instance_id"])
                    for message in resolved_messages
                    if message.message_attrs.get("process_instance_id")
                ),
            }
        )
        context_entries = [
            self._message_context_entry(message, index)
            for index, message in enumerate(resolved_messages)
        ]
        snapshot = SessionContextSnapshot(
            snapshot_id=new_session_context_snapshot_id(),
            source_session_id=session_id,
            snapshot_type=snapshot_type,
            created_at=utc_now_iso(),
            max_turns=max_turns,
            max_messages=max_messages,
            included_turn_ids=included_turn_ids,
            included_message_ids=included_message_ids,
            process_instance_ids=process_ids,
            summary=self._snapshot_summary(len(included_turn_ids), len(included_message_ids), snapshot_type),
            context_entries=context_entries,
            snapshot_attrs=dict(snapshot_attrs or {}),
        )
        self._record_snapshot_event("session_context_snapshot_created", snapshot)
        self._record_snapshot_event("session_context_reconstructed", snapshot)
        return snapshot

    def resume_session(
        self,
        *,
        session_id: str,
        max_turns: int | None = None,
        max_messages: int | None = None,
        include_system_messages: bool = False,
        include_tool_messages: bool = False,
        reason: str | None = None,
        messages: list[SessionMessage] | None = None,
        turns: list[ConversationTurn] | None = None,
    ) -> SessionResumeResult:
        resume_id = new_session_resume_id()
        self._record_resume_requested(session_id=session_id, resume_id=resume_id, reason=reason)
        snapshot = self.build_session_context_snapshot(
            session_id=session_id,
            snapshot_type="resume",
            max_turns=max_turns,
            max_messages=max_messages,
            include_system_messages=include_system_messages,
            include_tool_messages=include_tool_messages,
            messages=messages,
            turns=turns,
            snapshot_attrs={"resume_id": resume_id, "reason": reason},
        )
        resumed_at = utc_now_iso()
        self._record_permission_reset(
            session_id=session_id,
            resume_id=resume_id,
            fork_id=None,
            reason="resume resets permissions and approvals by design",
        )
        self._record_resume_event(
            "session_resumed",
            session_id=session_id,
            resume_id=resume_id,
            snapshot=snapshot,
            reason=reason,
            resumed_at=resumed_at,
        )
        return SessionResumeResult(
            session_id=session_id,
            snapshot=snapshot,
            permission_reset=True,
            resumed_at=resumed_at,
            result_attrs={"resume_id": resume_id, "reason": reason},
        )

    def fork_session(
        self,
        *,
        parent_session_id: str,
        fork_name: str | None = None,
        from_turn_id: str | None = None,
        from_message_id: str | None = None,
        max_turns: int | None = None,
        max_messages: int | None = None,
        include_system_messages: bool = False,
        include_tool_messages: bool = False,
        reason: str | None = None,
        messages: list[SessionMessage] | None = None,
        turns: list[ConversationTurn] | None = None,
    ) -> SessionForkResult:
        fork_id = new_session_fork_id()
        self._record_fork_requested(
            parent_session_id=parent_session_id,
            fork_id=fork_id,
            fork_name=fork_name,
            reason=reason,
        )
        snapshot = self.build_session_context_snapshot(
            session_id=parent_session_id,
            snapshot_type="fork",
            max_turns=max_turns,
            max_messages=max_messages,
            include_system_messages=include_system_messages,
            include_tool_messages=include_tool_messages,
            messages=messages,
            turns=turns,
            snapshot_attrs={
                "fork_id": fork_id,
                "fork_name": fork_name,
                "from_turn_id": from_turn_id,
                "from_message_id": from_message_id,
                "reason": reason,
            },
        )
        child = self.session_service.start_session(
            session_name=fork_name,
            session_attrs={
                "forked_from_session_id": parent_session_id,
                "fork_source_turn_id": from_turn_id,
                "fork_source_message_id": from_message_id,
                "fork_reason": reason,
            },
        )
        forked_at = utc_now_iso()
        self._record_permission_reset(
            session_id=child.session_id,
            resume_id=None,
            fork_id=fork_id,
            reason="fork resets permissions and approvals by design",
        )
        self._record_forked_event(
            parent_session_id=parent_session_id,
            child_session_id=child.session_id,
            fork_id=fork_id,
            snapshot=snapshot,
            fork_name=fork_name,
            from_turn_id=from_turn_id,
            from_message_id=from_message_id,
            reason=reason,
            forked_at=forked_at,
        )
        return SessionForkResult(
            parent_session_id=parent_session_id,
            child_session_id=child.session_id,
            snapshot=snapshot,
            permission_reset=True,
            forked_at=forked_at,
            result_attrs={
                "fork_id": fork_id,
                "fork_name": fork_name,
                "from_turn_id": from_turn_id,
                "from_message_id": from_message_id,
                "reason": reason,
            },
        )

    def session_context_snapshot_to_history_entries(
        self,
        snapshot: SessionContextSnapshot,
    ) -> list[ContextHistoryEntry]:
        return session_context_snapshot_to_history_entries(snapshot)

    def _load_messages_from_ocel(
        self,
        *,
        session_id: str,
        include_system_messages: bool,
        include_tool_messages: bool,
    ) -> list[SessionMessage]:
        view = OCPXLoader(store=self.ocel_store).load_session_view(session_id)
        messages: list[SessionMessage] = []
        allowed_roles = {"user", "assistant"}
        if include_system_messages:
            allowed_roles.add("system")
        if include_tool_messages:
            allowed_roles.add("tool")
        for item in view.objects:
            if item.object_type != "message":
                continue
            attrs = item.object_attrs
            role = str(attrs.get("role") or "other")
            if role not in allowed_roles:
                continue
            messages.append(
                SessionMessage(
                    message_id=str(attrs.get("message_id") or item.object_id),
                    session_id=str(attrs.get("session_id") or session_id),
                    turn_id=attrs.get("turn_id"),
                    role=role,
                    content=str(attrs.get("content") or attrs.get("content_preview") or ""),
                    content_preview=str(attrs.get("content_preview") or ""),
                    content_hash=str(attrs.get("content_hash") or ""),
                    created_at=str(attrs.get("created_at") or ""),
                    message_attrs={
                        key: value
                        for key, value in attrs.items()
                        if key not in {"message_id", "session_id", "turn_id", "role", "content", "content_preview", "content_hash", "created_at"}
                    },
                )
            )
        return messages

    def _load_turns_from_ocel(self, *, session_id: str) -> list[ConversationTurn]:
        view = OCPXLoader(store=self.ocel_store).load_session_view(session_id)
        turns: list[ConversationTurn] = []
        for item in view.objects:
            if item.object_type != "conversation_turn":
                continue
            attrs = item.object_attrs
            turns.append(
                ConversationTurn(
                    turn_id=str(attrs.get("turn_id") or item.object_id),
                    session_id=str(attrs.get("session_id") or session_id),
                    status=str(attrs.get("status") or "started"),
                    started_at=str(attrs.get("started_at") or ""),
                    completed_at=attrs.get("completed_at"),
                    process_instance_id=attrs.get("process_instance_id"),
                    user_message_id=attrs.get("user_message_id"),
                    assistant_message_id=attrs.get("assistant_message_id"),
                    turn_index=attrs.get("turn_index"),
                    turn_attrs={
                        key: value
                        for key, value in attrs.items()
                        if key not in {"turn_id", "session_id", "status", "started_at", "completed_at", "process_instance_id", "user_message_id", "assistant_message_id", "turn_index"}
                    },
                )
            )
        return turns

    @staticmethod
    def _recent_turn_ids(turns: list[ConversationTurn], max_turns: int | None) -> set[str] | None:
        if max_turns is None:
            return None
        sorted_turns = sorted(turns, key=lambda turn: (turn.started_at, turn.turn_id))
        return {turn.turn_id for turn in sorted_turns[-max_turns:]}

    @staticmethod
    def _sort_messages(messages: list[SessionMessage]) -> list[SessionMessage]:
        return sorted(messages, key=lambda message: (message.created_at, message.message_id))

    @staticmethod
    def _message_context_entry(message: SessionMessage, index: int) -> dict[str, Any]:
        return {
            "entry_id": new_context_history_entry_id(),
            "session_id": message.session_id,
            "process_instance_id": message.message_attrs.get("process_instance_id"),
            "role": message.role,
            "content": message.content,
            "created_at": message.created_at,
            "source": "session",
            "priority": 75 if message.role == "user" else 60 if message.role == "assistant" else 45,
            "refs": [
                {"ref_type": "message", "ref_id": message.message_id},
                {"ref_type": "session", "ref_id": message.session_id},
                *(
                    [{"ref_type": "conversation_turn", "ref_id": message.turn_id}]
                    if message.turn_id
                    else []
                ),
            ],
            "entry_attrs": {
                "message_id": message.message_id,
                "turn_id": message.turn_id,
                "content_hash": message.content_hash,
                "source_index": index,
            },
        }

    @staticmethod
    def _snapshot_summary(turn_count: int, message_count: int, snapshot_type: str) -> str:
        return f"{snapshot_type} snapshot with {turn_count} turns and {message_count} messages."

    def _record_resume_requested(self, *, session_id: str, resume_id: str, reason: str | None) -> None:
        self._append_record(
            event_activity="session_resume_requested",
            objects=[self._session_object(session_id), self._resume_object(resume_id, session_id, None, True, reason, utc_now_iso())],
            event_relations=[("session_context", self._session_object_id(session_id)), ("resume_object", resume_id)],
            object_relations=[(resume_id, self._session_object_id(session_id), "targets_session")],
            event_attrs={"session_id": session_id, "resume_id": resume_id, "reason": reason},
        )

    def _record_snapshot_event(self, event_activity: str, snapshot: SessionContextSnapshot) -> None:
        event_relations = [
            ("snapshot_object", snapshot.snapshot_id),
            ("source_session", self._session_object_id(snapshot.source_session_id)),
            *[("included_turn", turn_id) for turn_id in snapshot.included_turn_ids],
            *[("included_message", message_id) for message_id in snapshot.included_message_ids],
            *[("process_context", process_id) for process_id in snapshot.process_instance_ids],
        ]
        object_relations = [
            (snapshot.snapshot_id, self._session_object_id(snapshot.source_session_id), "derived_from_session"),
            *[(snapshot.snapshot_id, turn_id, "includes_turn") for turn_id in snapshot.included_turn_ids],
            *[(snapshot.snapshot_id, message_id, "includes_message") for message_id in snapshot.included_message_ids],
            *[(snapshot.snapshot_id, process_id, "includes_process_instance") for process_id in snapshot.process_instance_ids],
        ]
        self._append_record(
            event_activity=event_activity,
            objects=[
                self._snapshot_object(snapshot),
                self._session_object(snapshot.source_session_id),
                *[self._turn_object(turn_id, snapshot.source_session_id) for turn_id in snapshot.included_turn_ids],
                *[self._message_object(message_id, snapshot.source_session_id) for message_id in snapshot.included_message_ids],
                *[self._process_object(process_id) for process_id in snapshot.process_instance_ids],
            ],
            event_relations=event_relations,
            object_relations=object_relations,
            event_attrs={"snapshot_id": snapshot.snapshot_id, "snapshot_type": snapshot.snapshot_type},
        )

    def _record_resume_event(
        self,
        event_activity: str,
        *,
        session_id: str,
        resume_id: str,
        snapshot: SessionContextSnapshot,
        reason: str | None,
        resumed_at: str,
    ) -> None:
        self._append_record(
            event_activity=event_activity,
            objects=[
                self._session_object(session_id),
                self._snapshot_object(snapshot),
                self._resume_object(resume_id, session_id, snapshot.snapshot_id, True, reason, resumed_at),
            ],
            event_relations=[
                ("session_context", self._session_object_id(session_id)),
                ("snapshot_object", snapshot.snapshot_id),
                ("resume_object", resume_id),
            ],
            object_relations=[
                (resume_id, self._session_object_id(session_id), "targets_session"),
                (resume_id, snapshot.snapshot_id, "uses_snapshot"),
            ],
            event_attrs={"session_id": session_id, "snapshot_id": snapshot.snapshot_id, "resume_id": resume_id, "reason": reason},
        )

    def _record_fork_requested(
        self,
        *,
        parent_session_id: str,
        fork_id: str,
        fork_name: str | None,
        reason: str | None,
    ) -> None:
        self._append_record(
            event_activity="session_fork_requested",
            objects=[self._session_object(parent_session_id), self._fork_object(fork_id, parent_session_id, None, None, fork_name, None, None, True, reason, utc_now_iso())],
            event_relations=[("parent_session", self._session_object_id(parent_session_id)), ("fork_object", fork_id)],
            object_relations=[],
            event_attrs={"parent_session_id": parent_session_id, "fork_id": fork_id, "fork_name": fork_name, "reason": reason},
        )

    def _record_forked_event(
        self,
        *,
        parent_session_id: str,
        child_session_id: str,
        fork_id: str,
        snapshot: SessionContextSnapshot,
        fork_name: str | None,
        from_turn_id: str | None,
        from_message_id: str | None,
        reason: str | None,
        forked_at: str,
    ) -> None:
        parent_object_id = self._session_object_id(parent_session_id)
        child_object_id = self._session_object_id(child_session_id)
        self._append_record(
            event_activity="session_forked",
            objects=[
                self._session_object(parent_session_id),
                self._session_object(child_session_id, attrs={"forked_from_session_id": parent_session_id}),
                self._snapshot_object(snapshot),
                self._fork_object(fork_id, parent_session_id, child_session_id, snapshot.snapshot_id, fork_name, from_turn_id, from_message_id, True, reason, forked_at),
            ],
            event_relations=[
                ("parent_session", parent_object_id),
                ("child_session", child_object_id),
                ("snapshot_object", snapshot.snapshot_id),
                ("fork_object", fork_id),
            ],
            object_relations=[
                (fork_id, parent_object_id, "parent_session"),
                (fork_id, child_object_id, "child_session"),
                (fork_id, snapshot.snapshot_id, "uses_snapshot"),
                (child_object_id, parent_object_id, "forked_from_session"),
            ],
            event_attrs={"parent_session_id": parent_session_id, "child_session_id": child_session_id, "snapshot_id": snapshot.snapshot_id, "fork_id": fork_id, "reason": reason},
        )

    def _record_permission_reset(
        self,
        *,
        session_id: str,
        resume_id: str | None,
        fork_id: str | None,
        reason: str,
    ) -> None:
        event_relations = [("session_context", self._session_object_id(session_id))]
        objects = [self._session_object(session_id)]
        object_relations: list[tuple[str, str, str]] = []
        if resume_id:
            event_relations.append(("resume_object", resume_id))
            objects.append(self._resume_object(resume_id, session_id, None, True, reason, utc_now_iso()))
            object_relations.append((resume_id, self._session_object_id(session_id), "targets_session"))
        if fork_id:
            event_relations.append(("fork_object", fork_id))
            objects.append(self._fork_object(fork_id, None, session_id, None, None, None, None, True, reason, utc_now_iso()))
            object_relations.append((fork_id, self._session_object_id(session_id), "child_session"))
        self._append_record(
            event_activity="session_permissions_reset",
            objects=objects,
            event_relations=event_relations,
            object_relations=object_relations,
            event_attrs={"session_id": session_id, "resume_id": resume_id, "fork_id": fork_id, "reason": reason, "permission_reset": True},
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
                "permission_reset_required": event_activity in {"session_resumed", "session_forked", "session_permissions_reset"},
                "permissions_restored": False,
                "approvals_restored": False,
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
    def _snapshot_object(snapshot: SessionContextSnapshot) -> OCELObject:
        data = snapshot.to_dict()
        return OCELObject(
            object_id=snapshot.snapshot_id,
            object_type="session_context_snapshot",
            object_attrs={
                **data,
                "object_key": snapshot.snapshot_id,
                "display_name": f"{snapshot.snapshot_type} snapshot",
            },
        )

    @staticmethod
    def _resume_object(
        resume_id: str,
        session_id: str | None,
        snapshot_id: str | None,
        permission_reset: bool,
        reason: str | None,
        resumed_at: str,
    ) -> OCELObject:
        return OCELObject(
            object_id=resume_id,
            object_type="session_resume",
            object_attrs={
                "object_key": resume_id,
                "display_name": resume_id,
                "resume_id": resume_id,
                "session_id": session_id,
                "snapshot_id": snapshot_id,
                "permission_reset": permission_reset,
                "reason": reason,
                "resumed_at": resumed_at,
            },
        )

    @staticmethod
    def _fork_object(
        fork_id: str,
        parent_session_id: str | None,
        child_session_id: str | None,
        snapshot_id: str | None,
        fork_name: str | None,
        from_turn_id: str | None,
        from_message_id: str | None,
        permission_reset: bool,
        reason: str | None,
        forked_at: str,
    ) -> OCELObject:
        return OCELObject(
            object_id=fork_id,
            object_type="session_fork",
            object_attrs={
                "object_key": fork_id,
                "display_name": fork_name or fork_id,
                "fork_id": fork_id,
                "parent_session_id": parent_session_id,
                "child_session_id": child_session_id,
                "snapshot_id": snapshot_id,
                "fork_name": fork_name,
                "from_turn_id": from_turn_id,
                "from_message_id": from_message_id,
                "permission_reset": permission_reset,
                "reason": reason,
                "forked_at": forked_at,
            },
        )

    @staticmethod
    def _session_object(session_id: str, attrs: dict[str, Any] | None = None) -> OCELObject:
        object_id = SessionContinuityService._session_object_id(session_id)
        return OCELObject(
            object_id=object_id,
            object_type="session",
            object_attrs={"object_key": object_id, "display_name": object_id, "session_id": session_id, **dict(attrs or {})},
        )

    @staticmethod
    def _turn_object(turn_id: str, session_id: str) -> OCELObject:
        return OCELObject(
            object_id=turn_id,
            object_type="conversation_turn",
            object_attrs={"object_key": turn_id, "display_name": turn_id, "session_id": session_id},
        )

    @staticmethod
    def _message_object(message_id: str, session_id: str) -> OCELObject:
        return OCELObject(
            object_id=message_id,
            object_type="message",
            object_attrs={"object_key": message_id, "display_name": message_id, "session_id": session_id},
        )

    @staticmethod
    def _process_object(process_instance_id: str) -> OCELObject:
        return OCELObject(
            object_id=process_instance_id,
            object_type="process_instance",
            object_attrs={"object_key": process_instance_id, "display_name": process_instance_id},
        )

    @staticmethod
    def _session_object_id(session_id: str) -> str:
        return session_id if session_id.startswith("session:") else f"session:{session_id}"


def session_context_snapshot_to_history_entries(
    snapshot: SessionContextSnapshot,
) -> list[ContextHistoryEntry]:
    source = "session_fork" if snapshot.snapshot_type == "fork" else "session_resume"
    entries: list[ContextHistoryEntry] = []
    for item in snapshot.context_entries:
        entry_attrs = dict(item.get("entry_attrs") or {})
        message_id = entry_attrs.get("message_id")
        turn_id = entry_attrs.get("turn_id")
        entries.append(
            ContextHistoryEntry(
                entry_id=new_context_history_entry_id(),
                session_id=item.get("session_id"),
                process_instance_id=item.get("process_instance_id"),
                role=str(item.get("role") or "other"),
                content=str(item.get("content") or ""),
                created_at=str(item.get("created_at") or snapshot.created_at),
                source=source,
                priority=int(item.get("priority") or 50),
                refs=[
                    {"ref_type": "session_context_snapshot", "ref_id": snapshot.snapshot_id},
                    {"ref_type": "source_session", "ref_id": snapshot.source_session_id},
                    *([{"ref_type": "message", "ref_id": message_id}] if message_id else []),
                    *([{"ref_type": "conversation_turn", "ref_id": turn_id}] if turn_id else []),
                ],
                entry_attrs={
                    **entry_attrs,
                    "snapshot_id": snapshot.snapshot_id,
                    "source_session_id": snapshot.source_session_id,
                    "snapshot_type": snapshot.snapshot_type,
                },
            )
        )
    return entries
