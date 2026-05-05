from __future__ import annotations

from chanta_core.context.history import ContextHistoryEntry, new_context_history_entry_id
from chanta_core.memory.models import MemoryEntry


def memory_entries_to_history_entries(
    memories: list[MemoryEntry],
) -> list[ContextHistoryEntry]:
    entries: list[ContextHistoryEntry] = []
    for index, memory in enumerate(memories):
        if memory.status in {"archived", "withdrawn"}:
            priority = 20
        elif memory.status == "superseded":
            priority = 30
        elif memory.status == "draft":
            priority = 50
        else:
            priority = 80
        entries.append(
            ContextHistoryEntry(
                entry_id=new_context_history_entry_id(),
                session_id=None,
                process_instance_id=None,
                role="context",
                content=memory.content,
                created_at=memory.updated_at,
                source="memory",
                priority=priority,
                refs=[
                    {
                        "ref_type": "memory_entry",
                        "ref_id": memory.memory_id,
                        "memory_type": memory.memory_type,
                        "status": memory.status,
                        "confidence": memory.confidence,
                        "contradiction_status": memory.contradiction_status,
                        "scope": memory.scope,
                    }
                ],
                entry_attrs={
                    "memory_id": memory.memory_id,
                    "memory_type": memory.memory_type,
                    "status": memory.status,
                    "source_index": index,
                },
            )
        )
    return entries
