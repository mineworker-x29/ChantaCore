from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.utility.time import utc_now_iso


def new_context_snapshot_id() -> str:
    return f"context_snapshot:{uuid4()}"


@dataclass(frozen=True)
class ContextBlockSnapshot:
    block_id: str
    block_type: str
    title: str
    source: str
    priority: int
    char_length: int
    token_estimate: int
    was_truncated: bool
    was_dropped: bool
    was_collapsed: bool
    refs: list[dict[str, Any]] = field(default_factory=list)
    snapshot_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "block_id": self.block_id,
            "block_type": self.block_type,
            "title": self.title,
            "source": self.source,
            "priority": self.priority,
            "char_length": self.char_length,
            "token_estimate": self.token_estimate,
            "was_truncated": self.was_truncated,
            "was_dropped": self.was_dropped,
            "was_collapsed": self.was_collapsed,
            "refs": self.refs,
            "snapshot_attrs": self.snapshot_attrs,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ContextBlockSnapshot":
        return cls(
            block_id=str(data["block_id"]),
            block_type=str(data["block_type"]),
            title=str(data["title"]),
            source=str(data["source"]),
            priority=int(data["priority"]),
            char_length=int(data["char_length"]),
            token_estimate=int(data["token_estimate"]),
            was_truncated=bool(data["was_truncated"]),
            was_dropped=bool(data["was_dropped"]),
            was_collapsed=bool(data["was_collapsed"]),
            refs=list(data.get("refs") or []),
            snapshot_attrs=dict(data.get("snapshot_attrs") or {}),
        )


@dataclass(frozen=True)
class ContextMessageSnapshot:
    role: str
    content_preview: str | None
    char_length: int
    token_estimate: int
    message_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "content_preview": self.content_preview,
            "char_length": self.char_length,
            "token_estimate": self.token_estimate,
            "message_attrs": self.message_attrs,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ContextMessageSnapshot":
        return cls(
            role=str(data["role"]),
            content_preview=data.get("content_preview"),
            char_length=int(data["char_length"]),
            token_estimate=int(data["token_estimate"]),
            message_attrs=dict(data.get("message_attrs") or {}),
        )


@dataclass(frozen=True)
class ContextAssemblySnapshot:
    snapshot_id: str
    session_id: str | None
    process_instance_id: str | None
    created_at: str
    storage_mode: str
    budget: dict[str, Any] | None
    block_snapshots: list[ContextBlockSnapshot]
    message_snapshots: list[ContextMessageSnapshot]
    compaction_result: dict[str, Any] | None
    warnings: list[str] = field(default_factory=list)
    snapshot_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "session_id": self.session_id,
            "process_instance_id": self.process_instance_id,
            "created_at": self.created_at,
            "storage_mode": self.storage_mode,
            "budget": self.budget,
            "block_snapshots": [item.to_dict() for item in self.block_snapshots],
            "message_snapshots": [item.to_dict() for item in self.message_snapshots],
            "compaction_result": self.compaction_result,
            "warnings": self.warnings,
            "snapshot_attrs": self.snapshot_attrs,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ContextAssemblySnapshot":
        return cls(
            snapshot_id=str(data["snapshot_id"]),
            session_id=data.get("session_id"),
            process_instance_id=data.get("process_instance_id"),
            created_at=str(data.get("created_at") or utc_now_iso()),
            storage_mode=str(data["storage_mode"]),
            budget=data.get("budget"),
            block_snapshots=[
                ContextBlockSnapshot.from_dict(item)
                for item in data.get("block_snapshots") or []
            ],
            message_snapshots=[
                ContextMessageSnapshot.from_dict(item)
                for item in data.get("message_snapshots") or []
            ],
            compaction_result=data.get("compaction_result"),
            warnings=list(data.get("warnings") or []),
            snapshot_attrs=dict(data.get("snapshot_attrs") or {}),
        )


def create_context_assembly_snapshot(
    *,
    session_id: str | None,
    process_instance_id: str | None,
    storage_mode: str,
    budget: dict[str, Any] | None,
    block_snapshots: list[ContextBlockSnapshot],
    message_snapshots: list[ContextMessageSnapshot],
    compaction_result: dict[str, Any] | None,
    warnings: list[str],
    snapshot_attrs: dict[str, Any] | None = None,
) -> ContextAssemblySnapshot:
    return ContextAssemblySnapshot(
        snapshot_id=new_context_snapshot_id(),
        session_id=session_id,
        process_instance_id=process_instance_id,
        created_at=utc_now_iso(),
        storage_mode=storage_mode,
        budget=budget,
        block_snapshots=block_snapshots,
        message_snapshots=message_snapshots,
        compaction_result=compaction_result,
        warnings=warnings,
        snapshot_attrs=dict(snapshot_attrs or {}),
    )
