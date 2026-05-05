from __future__ import annotations

from typing import Any
from uuid import uuid4

from chanta_core.ocel.models import OCELObject, OCELRecord, OCELEvent, OCELRelation
from chanta_core.session.ids import (
    new_conversation_turn_id,
    new_session_id,
    new_session_message_id,
)
from chanta_core.session.models import (
    AgentSession,
    ConversationTurn,
    SessionMessage,
    hash_content,
    make_content_preview,
)
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


class SessionService:
    def __init__(
        self,
        *,
        trace_service: TraceService | None = None,
    ) -> None:
        self.trace_service = trace_service or TraceService()

    def start_session(
        self,
        *,
        session_id: str | None = None,
        session_name: str | None = None,
        agent_id: str | None = None,
        session_attrs: dict[str, Any] | None = None,
    ) -> AgentSession:
        now = utc_now_iso()
        session = AgentSession(
            session_id=session_id or new_session_id(),
            session_name=session_name,
            status="active",
            created_at=now,
            updated_at=now,
            closed_at=None,
            agent_id=agent_id,
            session_attrs=dict(session_attrs or {}),
        )
        self._append_record(
            event_activity="session_started",
            lifecycle="started",
            session=session,
            event_attrs={"session_name": session_name},
            event_relations=[
                ("session_context", self._session_object_id(session.session_id)),
                *(
                    [("acting_agent", self._agent_object_id(agent_id))]
                    if agent_id
                    else []
                ),
            ],
            objects=[
                self._session_object(session),
                *([self._agent_object(agent_id, now)] if agent_id else []),
            ],
            object_relations=[],
        )
        return session

    def close_session(
        self,
        session_id: str,
        *,
        reason: str | None = None,
    ) -> AgentSession:
        now = utc_now_iso()
        session = AgentSession(
            session_id=session_id,
            session_name=None,
            status="closed",
            created_at=now,
            updated_at=now,
            closed_at=now,
            agent_id=None,
            session_attrs={"close_reason": reason},
        )
        self._append_record(
            event_activity="session_closed",
            lifecycle="closed",
            session=session,
            event_attrs={"reason": reason},
            event_relations=[("session_context", self._session_object_id(session_id))],
            objects=[self._session_object(session)],
            object_relations=[],
        )
        return session

    def start_turn(
        self,
        *,
        session_id: str,
        process_instance_id: str | None = None,
        turn_index: int | None = None,
        turn_attrs: dict[str, Any] | None = None,
    ) -> ConversationTurn:
        now = utc_now_iso()
        turn = ConversationTurn(
            turn_id=new_conversation_turn_id(),
            session_id=session_id,
            status="started",
            started_at=now,
            completed_at=None,
            process_instance_id=process_instance_id,
            user_message_id=None,
            assistant_message_id=None,
            turn_index=turn_index,
            turn_attrs=dict(turn_attrs or {}),
        )
        self._append_turn_record(
            event_activity="conversation_turn_started",
            lifecycle="started",
            turn=turn,
            event_attrs={},
            event_relations=[
                ("session_context", self._session_object_id(session_id)),
                ("turn_context", turn.turn_id),
            ],
            object_relations=[
                (turn.turn_id, self._session_object_id(session_id), "belongs_to_session"),
                *(
                    [
                        (
                            turn.turn_id,
                            process_instance_id,
                            "runs_process_instance",
                        )
                    ]
                    if process_instance_id
                    else []
                ),
            ],
        )
        if process_instance_id:
            self._append_turn_record(
                event_activity="process_instance_attached_to_turn",
                lifecycle="attached",
                turn=turn,
                event_attrs={"process_instance_id": process_instance_id},
                event_relations=[
                    ("session_context", self._session_object_id(session_id)),
                    ("turn_context", turn.turn_id),
                    ("process_context", process_instance_id),
                ],
                object_relations=[
                    (turn.turn_id, process_instance_id, "runs_process_instance"),
                ],
            )
        return turn

    def record_user_message(
        self,
        *,
        session_id: str,
        turn_id: str | None,
        content: str,
        message_attrs: dict[str, Any] | None = None,
    ) -> SessionMessage:
        return self._record_message(
            session_id=session_id,
            turn_id=turn_id,
            role="user",
            content=content,
            event_activity="user_message_received",
            message_attrs=message_attrs,
        )

    def record_assistant_message(
        self,
        *,
        session_id: str,
        turn_id: str | None,
        content: str,
        message_attrs: dict[str, Any] | None = None,
    ) -> SessionMessage:
        return self._record_message(
            session_id=session_id,
            turn_id=turn_id,
            role="assistant",
            content=content,
            event_activity="assistant_message_emitted",
            message_attrs=message_attrs,
        )

    def complete_turn(
        self,
        *,
        session_id: str,
        turn_id: str,
        user_message_id: str | None = None,
        assistant_message_id: str | None = None,
        process_instance_id: str | None = None,
        turn_attrs: dict[str, Any] | None = None,
    ) -> ConversationTurn:
        now = utc_now_iso()
        turn = ConversationTurn(
            turn_id=turn_id,
            session_id=session_id,
            status="completed",
            started_at=now,
            completed_at=now,
            process_instance_id=process_instance_id,
            user_message_id=user_message_id,
            assistant_message_id=assistant_message_id,
            turn_index=None,
            turn_attrs=dict(turn_attrs or {}),
        )
        event_relations = [
            ("session_context", self._session_object_id(session_id)),
            ("turn_context", turn_id),
        ]
        object_relations = [
            (turn_id, self._session_object_id(session_id), "belongs_to_session"),
        ]
        if user_message_id:
            event_relations.append(("user_message", user_message_id))
            object_relations.append((turn_id, user_message_id, "has_user_message"))
        if assistant_message_id:
            event_relations.append(("assistant_message", assistant_message_id))
            object_relations.append(
                (turn_id, assistant_message_id, "has_assistant_message")
            )
        if process_instance_id:
            event_relations.append(("process_context", process_instance_id))
            object_relations.append(
                (turn_id, process_instance_id, "runs_process_instance")
            )
        self._append_turn_record(
            event_activity="conversation_turn_completed",
            lifecycle="completed",
            turn=turn,
            event_attrs={
                "user_message_id": user_message_id,
                "assistant_message_id": assistant_message_id,
                "process_instance_id": process_instance_id,
            },
            event_relations=event_relations,
            object_relations=object_relations,
        )
        return turn

    def fail_turn(
        self,
        *,
        session_id: str,
        turn_id: str,
        error: str,
        process_instance_id: str | None = None,
    ) -> ConversationTurn:
        now = utc_now_iso()
        turn = ConversationTurn(
            turn_id=turn_id,
            session_id=session_id,
            status="failed",
            started_at=now,
            completed_at=now,
            process_instance_id=process_instance_id,
            user_message_id=None,
            assistant_message_id=None,
            turn_index=None,
            turn_attrs={"error": error},
        )
        self._append_turn_record(
            event_activity="conversation_turn_failed",
            lifecycle="failed",
            turn=turn,
            event_attrs={"error": error, "process_instance_id": process_instance_id},
            event_relations=[
                ("session_context", self._session_object_id(session_id)),
                ("turn_context", turn_id),
                *(
                    [("process_context", process_instance_id)]
                    if process_instance_id
                    else []
                ),
            ],
            object_relations=[
                (turn_id, self._session_object_id(session_id), "belongs_to_session"),
                *(
                    [(turn_id, process_instance_id, "runs_process_instance")]
                    if process_instance_id
                    else []
                ),
            ],
        )
        return turn

    def _record_message(
        self,
        *,
        session_id: str,
        turn_id: str | None,
        role: str,
        content: str,
        event_activity: str,
        message_attrs: dict[str, Any] | None,
    ) -> SessionMessage:
        now = utc_now_iso()
        message = SessionMessage(
            message_id=new_session_message_id(),
            session_id=session_id,
            turn_id=turn_id,
            role=role,
            content=content,
            content_preview=make_content_preview(content),
            content_hash=hash_content(content),
            created_at=now,
            message_attrs=dict(message_attrs or {}),
        )
        event_relations = [
            ("session_context", self._session_object_id(session_id)),
            ("message_object", message.message_id),
        ]
        object_relations = [
            (
                message.message_id,
                self._session_object_id(session_id),
                "belongs_to_session",
            )
        ]
        if turn_id:
            event_relations.append(("turn_context", turn_id))
            object_relations.append(
                (message.message_id, turn_id, "belongs_to_turn")
            )
        self._append_record(
            event_activity=event_activity,
            lifecycle="received" if role == "user" else "emitted",
            session=self._session_placeholder(session_id, now),
            event_attrs={
                "message_id": message.message_id,
                "role": role,
                "turn_id": turn_id,
            },
            event_relations=event_relations,
            objects=[
                self._session_object(self._session_placeholder(session_id, now)),
                self._message_object(message),
                *([self._turn_object_placeholder(turn_id, session_id, now)] if turn_id else []),
            ],
            object_relations=object_relations,
        )
        if turn_id:
            self._append_record(
                event_activity="message_attached_to_turn",
                lifecycle="attached",
                session=self._session_placeholder(session_id, now),
                event_attrs={"message_id": message.message_id, "turn_id": turn_id},
                event_relations=[
                    ("session_context", self._session_object_id(session_id)),
                    ("turn_context", turn_id),
                    ("message_object", message.message_id),
                ],
                objects=[
                    self._message_object(message),
                    self._turn_object_placeholder(turn_id, session_id, now),
                ],
                object_relations=[
                    (message.message_id, turn_id, "belongs_to_turn"),
                ],
            )
        return message

    def _append_turn_record(
        self,
        *,
        event_activity: str,
        lifecycle: str,
        turn: ConversationTurn,
        event_attrs: dict[str, Any],
        event_relations: list[tuple[str, str]],
        object_relations: list[tuple[str, str, str]],
    ) -> None:
        now = utc_now_iso()
        self._append_record(
            event_activity=event_activity,
            lifecycle=lifecycle,
            session=self._session_placeholder(turn.session_id, now),
            event_attrs=event_attrs,
            event_relations=event_relations,
            objects=[
                self._session_object(self._session_placeholder(turn.session_id, now)),
                self._turn_object(turn),
                *(
                    [self._process_object_placeholder(turn.process_instance_id, now)]
                    if turn.process_instance_id
                    else []
                ),
            ],
            object_relations=object_relations,
        )

    def _append_record(
        self,
        *,
        event_activity: str,
        lifecycle: str,
        session: AgentSession,
        event_attrs: dict[str, Any],
        event_relations: list[tuple[str, str]],
        objects: list[OCELObject],
        object_relations: list[tuple[str, str, str]],
    ) -> None:
        timestamp = utc_now_iso()
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity=event_activity,
            event_timestamp=timestamp,
            event_attrs={
                **event_attrs,
                "runtime_event_type": event_activity,
                "lifecycle": lifecycle,
                "source_runtime": "chanta_core",
                "session_id": session.session_id,
                "actor_id": session.agent_id,
            },
        )
        relations = [
            OCELRelation.event_object(
                event_id=event.event_id,
                object_id=object_id,
                qualifier=qualifier,
            )
            for qualifier, object_id in event_relations
            if object_id
        ]
        relations.extend(
            OCELRelation.object_object(
                source_object_id=source_id,
                target_object_id=target_id,
                qualifier=qualifier,
            )
            for source_id, target_id, qualifier in object_relations
            if source_id and target_id
        )
        self.trace_service.record_session_ocel_record(
            OCELRecord(event=event, objects=objects, relations=relations)
        )

    def _session_placeholder(self, session_id: str, timestamp: str) -> AgentSession:
        return AgentSession(
            session_id=session_id,
            session_name=None,
            status="active",
            created_at=timestamp,
            updated_at=timestamp,
            closed_at=None,
            agent_id=None,
            session_attrs={},
        )

    def _session_object(self, session: AgentSession) -> OCELObject:
        return OCELObject(
            object_id=self._session_object_id(session.session_id),
            object_type="session",
            object_attrs={
                "object_key": session.session_id,
                "display_name": session.session_name or f"Session {session.session_id}",
                "session_id": session.session_id,
                "status": session.status,
                "session_name": session.session_name,
                "created_at": session.created_at,
                "updated_at": session.updated_at,
                "closed_at": session.closed_at,
                "agent_id": session.agent_id,
                **session.session_attrs,
            },
        )

    def _turn_object(self, turn: ConversationTurn) -> OCELObject:
        return OCELObject(
            object_id=turn.turn_id,
            object_type="conversation_turn",
            object_attrs={
                "object_key": turn.turn_id,
                "display_name": f"Conversation turn {turn.turn_id}",
                "turn_id": turn.turn_id,
                "session_id": turn.session_id,
                "status": turn.status,
                "started_at": turn.started_at,
                "completed_at": turn.completed_at,
                "turn_index": turn.turn_index,
                "process_instance_id": turn.process_instance_id,
                "user_message_id": turn.user_message_id,
                "assistant_message_id": turn.assistant_message_id,
                **turn.turn_attrs,
            },
        )

    def _turn_object_placeholder(
        self,
        turn_id: str,
        session_id: str,
        timestamp: str,
    ) -> OCELObject:
        return OCELObject(
            object_id=turn_id,
            object_type="conversation_turn",
            object_attrs={
                "object_key": turn_id,
                "display_name": f"Conversation turn {turn_id}",
                "turn_id": turn_id,
                "session_id": session_id,
                "status": "started",
                "started_at": timestamp,
                "updated_at": timestamp,
            },
        )

    @staticmethod
    def _message_object(message: SessionMessage) -> OCELObject:
        return OCELObject(
            object_id=message.message_id,
            object_type="message",
            object_attrs={
                "object_key": message.message_id,
                "display_name": f"{message.role} message",
                "message_id": message.message_id,
                "session_id": message.session_id,
                "turn_id": message.turn_id,
                "role": message.role,
                "content_preview": message.content_preview,
                "content_hash": message.content_hash,
                "content": message.content,
                "created_at": message.created_at,
                **message.message_attrs,
            },
        )

    @staticmethod
    def _agent_object_id(agent_id: str) -> str:
        return agent_id if agent_id.startswith("agent:") else f"agent:{agent_id}"

    def _agent_object(self, agent_id: str, timestamp: str) -> OCELObject:
        object_id = self._agent_object_id(agent_id)
        return OCELObject(
            object_id=object_id,
            object_type="agent",
            object_attrs={
                "object_key": agent_id,
                "display_name": agent_id,
                "agent_id": agent_id,
                "created_at": timestamp,
                "updated_at": timestamp,
            },
        )

    @staticmethod
    def _process_object_placeholder(process_instance_id: str, timestamp: str) -> OCELObject:
        return OCELObject(
            object_id=process_instance_id,
            object_type="process_instance",
            object_attrs={
                "object_key": process_instance_id,
                "display_name": process_instance_id,
                "process_instance_id": process_instance_id,
                "created_at": timestamp,
                "updated_at": timestamp,
            },
        )

    @staticmethod
    def _session_object_id(session_id: str) -> str:
        return session_id if session_id.startswith("session:") else f"session:{session_id}"
