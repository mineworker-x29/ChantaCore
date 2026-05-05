from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any

from chanta_core.instructions import InstructionArtifact, ProjectRule, UserPreference
from chanta_core.memory import MemoryEntry


def hash_content(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class MaterializedView:
    view_id: str
    view_type: str
    title: str
    target_path: str
    content: str
    content_hash: str
    generated_at: str
    source_kind: str
    canonical: bool
    view_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "view_id": self.view_id,
            "view_type": self.view_type,
            "title": self.title,
            "target_path": self.target_path,
            "content": self.content,
            "content_hash": self.content_hash,
            "generated_at": self.generated_at,
            "source_kind": self.source_kind,
            "canonical": self.canonical,
            "view_attrs": self.view_attrs,
        }


@dataclass(frozen=True)
class MaterializedViewInputSnapshot:
    memories: list[MemoryEntry] = field(default_factory=list)
    instructions: list[InstructionArtifact] = field(default_factory=list)
    project_rules: list[ProjectRule] = field(default_factory=list)
    user_preferences: list[UserPreference] = field(default_factory=list)
    pig_report: dict[str, Any] | None = None
    snapshot_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "memories": [item.to_dict() for item in self.memories],
            "instructions": [item.to_dict() for item in self.instructions],
            "project_rules": [item.to_dict() for item in self.project_rules],
            "user_preferences": [item.to_dict() for item in self.user_preferences],
            "pig_report": self.pig_report,
            "snapshot_attrs": self.snapshot_attrs,
        }


@dataclass(frozen=True)
class MaterializedViewRenderResult:
    view: MaterializedView
    written: bool
    target_path: str
    skipped_reason: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "view": self.view.to_dict(),
            "written": self.written,
            "target_path": self.target_path,
            "skipped_reason": self.skipped_reason,
        }
