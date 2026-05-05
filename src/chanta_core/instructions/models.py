from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.memory.models import hash_content, preview_text


@dataclass(frozen=True)
class InstructionArtifact:
    instruction_id: str
    instruction_type: str
    title: str
    body: str
    body_preview: str
    body_hash: str
    status: str
    scope: str | None
    priority: int | None
    created_at: str
    updated_at: str
    source_path: str | None
    instruction_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "instruction_id": self.instruction_id,
            "instruction_type": self.instruction_type,
            "title": self.title,
            "body": self.body,
            "body_preview": self.body_preview,
            "body_hash": self.body_hash,
            "status": self.status,
            "scope": self.scope,
            "priority": self.priority,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "source_path": self.source_path,
            "instruction_attrs": self.instruction_attrs,
        }


@dataclass(frozen=True)
class ProjectRule:
    rule_id: str
    rule_type: str
    text: str
    status: str
    priority: int | None
    created_at: str
    updated_at: str
    source_instruction_id: str | None
    rule_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "rule_type": self.rule_type,
            "text": self.text,
            "status": self.status,
            "priority": self.priority,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "source_instruction_id": self.source_instruction_id,
            "rule_attrs": self.rule_attrs,
        }


@dataclass(frozen=True)
class UserPreference:
    preference_id: str
    preference_key: str
    preference_value: str
    status: str
    confidence: float | None
    source_kind: str | None
    created_at: str
    updated_at: str
    preference_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "preference_id": self.preference_id,
            "preference_key": self.preference_key,
            "preference_value": self.preference_value,
            "status": self.status,
            "confidence": self.confidence,
            "source_kind": self.source_kind,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "preference_attrs": self.preference_attrs,
        }


def hash_body(text: str) -> str:
    return hash_content(text)


def preview_body(text: str, max_chars: int = 240) -> str:
    return preview_text(text, max_chars=max_chars)
