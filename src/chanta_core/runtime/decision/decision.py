from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ProcessDecision:
    selected_skill_id: str
    decision_mode: str
    base_scores: dict[str, float]
    final_scores: dict[str, float]
    applied_guidance_ids: list[str]
    rationale: str
    evidence_refs: list[dict[str, Any]]
    decision_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "selected_skill_id": self.selected_skill_id,
            "decision_mode": self.decision_mode,
            "base_scores": self.base_scores,
            "final_scores": self.final_scores,
            "applied_guidance_ids": self.applied_guidance_ids,
            "rationale": self.rationale,
            "evidence_refs": self.evidence_refs,
            "decision_attrs": self.decision_attrs,
        }
