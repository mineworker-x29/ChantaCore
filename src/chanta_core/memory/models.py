from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any


def hash_content(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def preview_text(text: str, max_chars: int = 240) -> str:
    marker = "...[memory preview truncated]..."
    if len(text) <= max_chars:
        return text
    if len(marker) >= max_chars:
        return marker[:max_chars]
    return f"{text[: max_chars - len(marker)]}{marker}"


@dataclass(frozen=True)
class MemoryEntry:
    memory_id: str
    memory_type: str
    title: str
    content: str
    content_preview: str
    content_hash: str
    status: str
    confidence: float | None
    created_at: str
    updated_at: str
    valid_from: str | None
    valid_until: str | None
    contradiction_status: str
    source_kind: str | None
    scope: str | None
    memory_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "memory_id": self.memory_id,
            "memory_type": self.memory_type,
            "title": self.title,
            "content": self.content,
            "content_preview": self.content_preview,
            "content_hash": self.content_hash,
            "status": self.status,
            "confidence": self.confidence,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "valid_from": self.valid_from,
            "valid_until": self.valid_until,
            "contradiction_status": self.contradiction_status,
            "source_kind": self.source_kind,
            "scope": self.scope,
            "memory_attrs": self.memory_attrs,
        }


@dataclass(frozen=True)
class MemoryRevision:
    revision_id: str
    memory_id: str
    revision_index: int | None
    operation: str
    before_hash: str | None
    after_hash: str | None
    content_preview: str
    content_hash: str
    reason: str | None
    created_at: str
    actor_type: str | None
    revision_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "revision_id": self.revision_id,
            "memory_id": self.memory_id,
            "revision_index": self.revision_index,
            "operation": self.operation,
            "before_hash": self.before_hash,
            "after_hash": self.after_hash,
            "content_preview": self.content_preview,
            "content_hash": self.content_hash,
            "reason": self.reason,
            "created_at": self.created_at,
            "actor_type": self.actor_type,
            "revision_attrs": self.revision_attrs,
        }
