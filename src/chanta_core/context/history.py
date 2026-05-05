from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.context.block import ContextBlock, make_context_block


def new_context_history_entry_id() -> str:
    return f"context_history_entry:{uuid4()}"


@dataclass(frozen=True)
class ContextHistoryEntry:
    entry_id: str
    session_id: str | None
    process_instance_id: str | None
    role: str
    content: str
    created_at: str
    source: str
    priority: int
    refs: list[dict[str, Any]] = field(default_factory=list)
    entry_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "session_id": self.session_id,
            "process_instance_id": self.process_instance_id,
            "role": self.role,
            "content": self.content,
            "created_at": self.created_at,
            "source": self.source,
            "priority": self.priority,
            "refs": self.refs,
            "entry_attrs": self.entry_attrs,
        }


def history_entry_to_context_block(entry: ContextHistoryEntry) -> ContextBlock:
    block_type = "history"
    if entry.role == "tool":
        block_type = "tool_result"
    elif entry.role == "pig":
        block_type = "pig_context"
    elif entry.role == "report":
        block_type = "pig_report"
    return make_context_block(
        block_type=block_type,
        title=f"History: {entry.role} / {entry.source}",
        content=entry.content,
        priority=entry.priority,
        source=entry.source,
        refs=entry.refs,
        block_attrs={
            **entry.entry_attrs,
            "history_entry_id": entry.entry_id,
            "session_id": entry.session_id,
            "process_instance_id": entry.process_instance_id,
            "created_at": entry.created_at,
            "role": entry.role,
            "source": entry.source,
            "is_history": True,
        },
    )
