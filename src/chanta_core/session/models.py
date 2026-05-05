from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any


def hash_content(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def make_content_preview(text: str, max_chars: int = 500) -> str:
    marker = "...[message preview truncated]..."
    if len(text) <= max_chars:
        return text
    if len(marker) >= max_chars:
        return marker[:max_chars]
    return f"{text[: max_chars - len(marker)]}{marker}"


@dataclass(frozen=True)
class AgentSession:
    session_id: str
    session_name: str | None
    status: str
    created_at: str
    updated_at: str
    closed_at: str | None
    agent_id: str | None
    session_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "session_name": self.session_name,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "closed_at": self.closed_at,
            "agent_id": self.agent_id,
            "session_attrs": self.session_attrs,
        }


@dataclass(frozen=True)
class ConversationTurn:
    turn_id: str
    session_id: str
    status: str
    started_at: str
    completed_at: str | None
    process_instance_id: str | None
    user_message_id: str | None
    assistant_message_id: str | None
    turn_index: int | None
    turn_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "turn_id": self.turn_id,
            "session_id": self.session_id,
            "status": self.status,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "process_instance_id": self.process_instance_id,
            "user_message_id": self.user_message_id,
            "assistant_message_id": self.assistant_message_id,
            "turn_index": self.turn_index,
            "turn_attrs": self.turn_attrs,
        }


@dataclass(frozen=True)
class SessionMessage:
    message_id: str
    session_id: str
    turn_id: str | None
    role: str
    content: str
    content_preview: str
    content_hash: str
    created_at: str
    message_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "message_id": self.message_id,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "role": self.role,
            "content": self.content,
            "content_preview": self.content_preview,
            "content_hash": self.content_hash,
            "created_at": self.created_at,
            "message_attrs": self.message_attrs,
        }
