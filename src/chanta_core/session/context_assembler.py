from __future__ import annotations

from typing import Any
from uuid import uuid4

from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.session.context_policy import SessionContextPolicy
from chanta_core.session.context_projection import SessionContextProjection
from chanta_core.session.ids import (
    new_session_context_policy_id,
    new_session_context_projection_id,
    new_session_prompt_render_id,
)
from chanta_core.session.models import ConversationTurn, SessionMessage
from chanta_core.session.prompt_renderer import render_projection_to_llm_messages
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


class SessionContextAssembler:
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

    def create_default_policy(
        self,
        *,
        policy_name: str | None = "default_recent_session_context",
        max_turns: int | None = 8,
        max_messages: int | None = 16,
        max_chars: int | None = 12000,
    ) -> SessionContextPolicy:
        policy = SessionContextPolicy(
            policy_id=new_session_context_policy_id(),
            policy_name=policy_name,
            max_turns=max_turns,
            max_messages=max_messages,
            max_chars=max_chars,
            include_user_messages=True,
            include_assistant_messages=True,
            include_system_messages=False,
            include_tool_messages=False,
            strategy="recent_only",
            status="active",
            created_at=utc_now_iso(),
            policy_attrs={"canonical": False, "read_model_policy": True},
        )
        self._record_policy(policy)
        return policy

    def assemble_projection_from_messages(
        self,
        *,
        session_id: str,
        messages: list[SessionMessage],
        turns: list[ConversationTurn] | None = None,
        policy: SessionContextPolicy | None = None,
        exclude_message_ids: list[str] | None = None,
    ) -> SessionContextProjection:
        policy = policy or self.create_default_policy()
        excluded = set(exclude_message_ids or [])
        turn_ids = _recent_turn_ids(turns or [], policy.max_turns)
        enforce_turn_limit = turns is not None and policy.max_turns is not None
        filtered_with_order = [
            (index, message)
            for index, message in enumerate(messages)
            if message.session_id == session_id
            and message.message_id not in excluded
            and _role_allowed(message.role, policy)
            and (not enforce_turn_limit or message.turn_id in turn_ids)
        ]
        filtered_with_order.sort(key=lambda item: (item[1].created_at, item[0]))
        filtered = [message for _, message in filtered_with_order]
        truncated = False
        reasons: list[str] = []
        if policy.max_messages is not None and len(filtered) > policy.max_messages:
            filtered = filtered[-policy.max_messages :]
            truncated = True
            reasons.append("max_messages")
        if policy.max_chars is not None:
            while _total_chars(filtered) > policy.max_chars and filtered:
                filtered = filtered[1:]
                truncated = True
                reasons.append("max_chars")
        rendered_messages = [
            {
                "role": message.role,
                "content": message.content,
                "message_id": message.message_id,
                "turn_id": message.turn_id,
            }
            for message in filtered
        ]
        projection = SessionContextProjection(
            projection_id=new_session_context_projection_id(),
            session_id=session_id,
            policy_id=policy.policy_id,
            source_turn_ids=_ordered_unique(
                [message.turn_id for message in filtered if message.turn_id]
            ),
            source_message_ids=[message.message_id for message in filtered],
            rendered_messages=rendered_messages,
            total_messages=len(rendered_messages),
            total_chars=sum(len(str(message["content"])) for message in rendered_messages),
            truncated=truncated,
            truncation_reason=",".join(_ordered_unique(reasons)) if reasons else None,
            created_at=utc_now_iso(),
            projection_attrs={
                "canonical": False,
                "source": "session_message_records",
                "scrollback_source": False,
            },
        )
        self._record_projection(projection, policy=policy)
        if projection.truncated:
            self._record_projection_truncated(projection)
        return projection

    def render_projection_to_llm_messages(
        self,
        *,
        projection: SessionContextProjection,
        system_prompt: str | None = None,
        persona_projection_block: str | None = None,
        capability_profile_block: str | None = None,
        current_user_message: str | None = None,
        avoid_duplicate_current_message: bool = True,
    ) -> list[dict[str, str]]:
        messages = render_projection_to_llm_messages(
            projection=projection,
            system_prompt=system_prompt,
            persona_projection_block=persona_projection_block,
            capability_profile_block=capability_profile_block,
            current_user_message=current_user_message,
            avoid_duplicate_current_message=avoid_duplicate_current_message,
        )
        self._record_prompt_render(projection, messages)
        return messages

    def _record_policy(self, policy: SessionContextPolicy) -> None:
        self._record(
            "session_context_policy_registered",
            objects=[_policy_object(policy)],
            links=[("policy_object", policy.policy_id)],
            object_links=[],
            attrs={"policy_id": policy.policy_id, "canonical": False},
        )

    def _record_projection(self, projection: SessionContextProjection, *, policy: SessionContextPolicy) -> None:
        links = [
            ("projection_object", projection.projection_id),
            ("session_context", _session_object_id(projection.session_id)),
            ("policy_object", policy.policy_id),
        ]
        links.extend(("source_turn", turn_id) for turn_id in projection.source_turn_ids)
        links.extend(("source_message", message_id) for message_id in projection.source_message_ids)
        object_links = [
            (projection.projection_id, _session_object_id(projection.session_id), "projects_session"),
            (projection.projection_id, policy.policy_id, "uses_policy"),
        ]
        object_links.extend(
            (projection.projection_id, turn_id, "includes_turn") for turn_id in projection.source_turn_ids
        )
        object_links.extend(
            (projection.projection_id, message_id, "includes_message")
            for message_id in projection.source_message_ids
        )
        self._record(
            "session_context_projection_created",
            objects=[_projection_object(projection), _policy_object(policy)],
            links=links,
            object_links=object_links,
            attrs={
                "session_id": projection.session_id,
                "total_messages": projection.total_messages,
                "total_chars": projection.total_chars,
                "truncated": projection.truncated,
                "canonical": False,
            },
        )

    def _record_projection_truncated(self, projection: SessionContextProjection) -> None:
        self._record(
            "session_context_projection_truncated",
            objects=[_projection_object(projection)],
            links=[("projection_object", projection.projection_id)],
            object_links=[],
            attrs={"truncation_reason": projection.truncation_reason, "canonical": False},
        )

    def _record_prompt_render(self, projection: SessionContextProjection, messages: list[dict[str, str]]) -> None:
        render_id = new_session_prompt_render_id()
        render_object = OCELObject(
            object_id=render_id,
            object_type="session_prompt_render",
            object_attrs={
                "object_key": render_id,
                "display_name": "Session prompt render",
                "render_id": render_id,
                "projection_id": projection.projection_id,
                "message_count": len(messages),
                "canonical": False,
                "created_at": utc_now_iso(),
            },
        )
        self._record(
            "session_prompt_rendered",
            objects=[_projection_object(projection), render_object],
            links=[
                ("projection_object", projection.projection_id),
                ("prompt_render_object", render_id),
            ],
            object_links=[(render_id, projection.projection_id, "renders_projection")],
            attrs={"projection_id": projection.projection_id, "message_count": len(messages)},
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
                "session_context_projection_read_model": True,
                "canonical": False,
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


def _role_allowed(role: str, policy: SessionContextPolicy) -> bool:
    return (
        (role == "user" and policy.include_user_messages)
        or (role == "assistant" and policy.include_assistant_messages)
        or (role == "system" and policy.include_system_messages)
        or (role == "tool" and policy.include_tool_messages)
    )


def _recent_turn_ids(turns: list[ConversationTurn], max_turns: int | None) -> set[str]:
    if max_turns is None:
        return {turn.turn_id for turn in turns}
    if max_turns == 0:
        return set()
    ordered = sorted(turns, key=lambda item: (item.started_at, item.turn_id))
    return {turn.turn_id for turn in ordered[-max_turns:]}


def _total_chars(messages: list[SessionMessage]) -> int:
    return sum(len(message.content) for message in messages)


def _ordered_unique(items: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for item in items:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result


def _session_object_id(session_id: str) -> str:
    return session_id if session_id.startswith("session:") else f"session:{session_id}"


def _policy_object(policy: SessionContextPolicy) -> OCELObject:
    return OCELObject(
        object_id=policy.policy_id,
        object_type="session_context_policy",
        object_attrs={
            **policy.to_dict(),
            "object_key": policy.policy_id,
            "display_name": policy.policy_name or policy.policy_id,
            "canonical": False,
        },
    )


def _projection_object(projection: SessionContextProjection) -> OCELObject:
    return OCELObject(
        object_id=projection.projection_id,
        object_type="session_context_projection",
        object_attrs={
            **projection.to_dict(),
            "object_key": projection.projection_id,
            "display_name": f"Session context projection {projection.session_id}",
            "canonical": False,
        },
    )
