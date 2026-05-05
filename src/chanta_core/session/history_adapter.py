from __future__ import annotations

from chanta_core.context.history import ContextHistoryEntry, new_context_history_entry_id
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
