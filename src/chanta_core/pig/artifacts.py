from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PIArtifact:
    artifact_id: str
    artifact_type: str
    source_type: str
    title: str
    content: str
    scope: dict[str, Any]
    evidence_refs: list[dict[str, Any]]
    object_refs: list[dict[str, Any]]
    confidence: float
    status: str
    created_at: str
    artifact_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "artifact_type": self.artifact_type,
            "source_type": self.source_type,
            "title": self.title,
            "content": self.content,
            "scope": self.scope,
            "evidence_refs": self.evidence_refs,
            "object_refs": self.object_refs,
            "confidence": self.confidence,
            "status": self.status,
            "created_at": self.created_at,
            "artifact_attrs": self.artifact_attrs,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PIArtifact":
        return cls(
            artifact_id=str(data["artifact_id"]),
            artifact_type=str(data["artifact_type"]),
            source_type=str(data["source_type"]),
            title=str(data["title"]),
            content=str(data["content"]),
            scope=dict(data.get("scope") or {}),
            evidence_refs=list(data.get("evidence_refs") or []),
            object_refs=list(data.get("object_refs") or []),
            confidence=float(data.get("confidence", 0.0)),
            status=str(data.get("status") or "active"),
            created_at=str(data["created_at"]),
            artifact_attrs=dict(data.get("artifact_attrs") or {}),
        )
