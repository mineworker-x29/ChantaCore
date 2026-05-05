from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SessionContextSnapshot:
    snapshot_id: str
    source_session_id: str
    snapshot_type: str
    created_at: str
    max_turns: int | None
    max_messages: int | None
    included_turn_ids: list[str]
    included_message_ids: list[str]
    process_instance_ids: list[str]
    summary: str | None
    context_entries: list[dict[str, Any]]
    snapshot_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "source_session_id": self.source_session_id,
            "snapshot_type": self.snapshot_type,
            "created_at": self.created_at,
            "max_turns": self.max_turns,
            "max_messages": self.max_messages,
            "included_turn_ids": self.included_turn_ids,
            "included_message_ids": self.included_message_ids,
            "process_instance_ids": self.process_instance_ids,
            "summary": self.summary,
            "context_entries": self.context_entries,
            "snapshot_attrs": self.snapshot_attrs,
        }


@dataclass(frozen=True)
class SessionResumeRequest:
    session_id: str
    max_turns: int | None
    max_messages: int | None
    include_system_messages: bool
    include_tool_messages: bool
    reason: str | None
    request_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "max_turns": self.max_turns,
            "max_messages": self.max_messages,
            "include_system_messages": self.include_system_messages,
            "include_tool_messages": self.include_tool_messages,
            "reason": self.reason,
            "request_attrs": self.request_attrs,
        }


@dataclass(frozen=True)
class SessionResumeResult:
    session_id: str
    snapshot: SessionContextSnapshot
    permission_reset: bool
    resumed_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "snapshot": self.snapshot.to_dict(),
            "permission_reset": self.permission_reset,
            "resumed_at": self.resumed_at,
            "result_attrs": self.result_attrs,
        }


@dataclass(frozen=True)
class SessionForkRequest:
    parent_session_id: str
    fork_name: str | None
    from_turn_id: str | None
    from_message_id: str | None
    max_turns: int | None
    max_messages: int | None
    reason: str | None
    request_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "parent_session_id": self.parent_session_id,
            "fork_name": self.fork_name,
            "from_turn_id": self.from_turn_id,
            "from_message_id": self.from_message_id,
            "max_turns": self.max_turns,
            "max_messages": self.max_messages,
            "reason": self.reason,
            "request_attrs": self.request_attrs,
        }


@dataclass(frozen=True)
class SessionForkResult:
    parent_session_id: str
    child_session_id: str
    snapshot: SessionContextSnapshot
    permission_reset: bool
    forked_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "parent_session_id": self.parent_session_id,
            "child_session_id": self.child_session_id,
            "snapshot": self.snapshot.to_dict(),
            "permission_reset": self.permission_reset,
            "forked_at": self.forked_at,
            "result_attrs": self.result_attrs,
        }
