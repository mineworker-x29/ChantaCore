from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

from chanta_core.tool_registry.errors import ToolPolicyNoteError


FORBIDDEN_POLICY_NOTE_TYPES = {
    "allow",
    "deny",
    "ask",
    "grant",
    "revoke",
    "block",
    "sandbox",
}


def hash_tool_snapshot(tool_ids: list[str]) -> str:
    raw = json.dumps(sorted(tool_ids), ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ToolDescriptor:
    tool_id: str
    tool_name: str
    tool_type: str
    description: str | None
    status: str
    capability_tags: list[str]
    input_schema_ref: str | None
    output_schema_ref: str | None
    execution_owner: str | None
    source_kind: str | None
    risk_level: str | None
    created_at: str
    updated_at: str
    tool_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "tool_id": self.tool_id,
            "tool_name": self.tool_name,
            "tool_type": self.tool_type,
            "description": self.description,
            "status": self.status,
            "capability_tags": self.capability_tags,
            "input_schema_ref": self.input_schema_ref,
            "output_schema_ref": self.output_schema_ref,
            "execution_owner": self.execution_owner,
            "source_kind": self.source_kind,
            "risk_level": self.risk_level,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "tool_attrs": self.tool_attrs,
        }


@dataclass(frozen=True)
class ToolRegistrySnapshot:
    snapshot_id: str
    snapshot_name: str | None
    created_at: str
    tool_ids: list[str]
    source_kind: str
    snapshot_hash: str
    snapshot_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "snapshot_name": self.snapshot_name,
            "created_at": self.created_at,
            "tool_ids": self.tool_ids,
            "source_kind": self.source_kind,
            "snapshot_hash": self.snapshot_hash,
            "snapshot_attrs": self.snapshot_attrs,
        }


@dataclass(frozen=True)
class ToolPolicyNote:
    policy_note_id: str
    tool_id: str | None
    tool_name: str | None
    note_type: str
    text: str
    status: str
    priority: int | None
    source_kind: str | None
    created_at: str
    updated_at: str
    note_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.note_type in FORBIDDEN_POLICY_NOTE_TYPES:
            raise ToolPolicyNoteError(f"Forbidden tool policy note type: {self.note_type}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_note_id": self.policy_note_id,
            "tool_id": self.tool_id,
            "tool_name": self.tool_name,
            "note_type": self.note_type,
            "text": self.text,
            "status": self.status,
            "priority": self.priority,
            "source_kind": self.source_kind,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "note_attrs": self.note_attrs,
        }


@dataclass(frozen=True)
class ToolRiskAnnotation:
    risk_annotation_id: str
    tool_id: str
    risk_level: str
    risk_category: str
    rationale: str | None
    status: str
    created_at: str
    updated_at: str
    annotation_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "risk_annotation_id": self.risk_annotation_id,
            "tool_id": self.tool_id,
            "risk_level": self.risk_level,
            "risk_category": self.risk_category,
            "rationale": self.rationale,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "annotation_attrs": self.annotation_attrs,
        }
