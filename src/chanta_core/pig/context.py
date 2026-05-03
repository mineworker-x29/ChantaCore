from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PIGContext:
    source: str
    scope: str
    process_instance_id: str | None
    session_id: str | None
    activity_sequence: list[str]
    event_activity_counts: dict[str, int]
    object_type_counts: dict[str, int]
    relation_coverage: dict[str, Any]
    basic_variant: dict[str, Any]
    performance_summary: dict[str, Any]
    guide: dict[str, Any]
    diagnostics: list[dict[str, Any]]
    recommendations: list[dict[str, Any]]
    context_text: str
    pi_artifacts: list[dict[str, Any]] = field(default_factory=list)
    context_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "scope": self.scope,
            "process_instance_id": self.process_instance_id,
            "session_id": self.session_id,
            "activity_sequence": self.activity_sequence,
            "event_activity_counts": self.event_activity_counts,
            "object_type_counts": self.object_type_counts,
            "relation_coverage": self.relation_coverage,
            "basic_variant": self.basic_variant,
            "performance_summary": self.performance_summary,
            "guide": self.guide,
            "diagnostics": self.diagnostics,
            "recommendations": self.recommendations,
            "context_text": self.context_text,
            "pi_artifacts": self.pi_artifacts,
            "context_attrs": self.context_attrs,
        }
