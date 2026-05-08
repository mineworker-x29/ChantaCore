from __future__ import annotations

from chanta_core.context.history import ContextHistoryEntry, new_context_history_entry_id
from chanta_core.session.continuity import session_context_snapshot_to_history_entries
from chanta_core.session.context_projection import (
    SessionContextProjection,
    SessionPromptRenderResult,
)
from chanta_core.session.models import SessionMessage


def session_messages_to_history_entries(
    messages: list[SessionMessage],
) -> list[ContextHistoryEntry]:
    entries: list[ContextHistoryEntry] = []
    for index, message in enumerate(messages):
        priority = 75 if message.role == "user" else 60
        if message.role not in {"user", "assistant"}:
            priority = 45
        entries.append(
            ContextHistoryEntry(
                entry_id=new_context_history_entry_id(),
                session_id=message.session_id,
                process_instance_id=message.message_attrs.get("process_instance_id"),
                role=message.role,
                content=message.content,
                created_at=message.created_at,
                source="session",
                priority=priority,
                refs=[
                    {
                        "ref_type": "message",
                        "ref_id": message.message_id,
                    },
                    {
                        "ref_type": "session",
                        "ref_id": message.session_id,
                    },
                    *(
                        [
                            {
                                "ref_type": "conversation_turn",
                                "ref_id": message.turn_id,
                            }
                        ]
                        if message.turn_id
                        else []
                    ),
                ],
                entry_attrs={
                    "message_id": message.message_id,
                    "turn_id": message.turn_id,
                    "content_hash": message.content_hash,
                    "source_index": index,
                },
            )
        )
    return entries


def session_context_projections_to_history_entries(
    projections: list[SessionContextProjection],
) -> list[ContextHistoryEntry]:
    entries: list[ContextHistoryEntry] = []
    for projection in projections:
        priority = 70 if projection.truncated else 55
        entries.append(
            ContextHistoryEntry(
                entry_id=new_context_history_entry_id(),
                session_id=projection.session_id,
                process_instance_id=None,
                role="context",
                content=(
                    "Bounded session context projection: "
                    f"{projection.total_messages} messages, "
                    f"{projection.total_chars} chars"
                ),
                created_at=projection.created_at,
                source="session_context_projection",
                priority=priority,
                refs=[
                    {
                        "ref_type": "session_context_projection",
                        "ref_id": projection.projection_id,
                    },
                    {"ref_type": "session", "ref_id": projection.session_id},
                    *[
                        {"ref_type": "conversation_turn", "ref_id": turn_id}
                        for turn_id in projection.source_turn_ids
                    ],
                    *[
                        {"ref_type": "message", "ref_id": message_id}
                        for message_id in projection.source_message_ids
                    ],
                ],
                entry_attrs={
                    "policy_id": projection.policy_id,
                    "truncated": projection.truncated,
                    "truncation_reason": projection.truncation_reason,
                    "canonical": False,
                },
            )
        )
    return entries


def session_prompt_render_results_to_history_entries(
    renders: list[SessionPromptRenderResult],
) -> list[ContextHistoryEntry]:
    entries: list[ContextHistoryEntry] = []
    for render in renders:
        entries.append(
            ContextHistoryEntry(
                entry_id=new_context_history_entry_id(),
                session_id=None,
                process_instance_id=None,
                role="context",
                content=f"Session prompt render: {len(render.messages)} messages",
                created_at=render.created_at,
                source="session_context_projection",
                priority=50,
                refs=[
                    {"ref_type": "session_prompt_render", "ref_id": render.render_id},
                    {
                        "ref_type": "session_context_projection",
                        "ref_id": render.projection_id,
                    },
                ],
                entry_attrs={
                    "system_prompt_included": render.system_prompt_included,
                    "capability_profile_included": render.capability_profile_included,
                    "canonical": False,
                },
            )
        )
    return entries
