from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.context.budget import ContextBudget
from chanta_core.context.result import ContextCompactionResult
from chanta_core.utility.time import utc_now_iso


@dataclass(frozen=True)
class ContextCompactionReadiness:
    readiness_id: str
    generated_at: str
    status: str
    total_chars: int
    total_estimated_tokens: int
    budget: dict[str, Any]
    layer_summary: list[dict[str, Any]]
    truncated_block_count: int
    dropped_block_count: int
    collapsed_block_count: int
    remaining_over_budget: bool
    auto_compact_recommended: bool
    warnings: list[str] = field(default_factory=list)
    readiness_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "readiness_id": self.readiness_id,
            "generated_at": self.generated_at,
            "status": self.status,
            "total_chars": self.total_chars,
            "total_estimated_tokens": self.total_estimated_tokens,
            "budget": self.budget,
            "layer_summary": self.layer_summary,
            "truncated_block_count": self.truncated_block_count,
            "dropped_block_count": self.dropped_block_count,
            "collapsed_block_count": self.collapsed_block_count,
            "remaining_over_budget": self.remaining_over_budget,
            "auto_compact_recommended": self.auto_compact_recommended,
            "warnings": self.warnings,
            "readiness_attrs": self.readiness_attrs,
        }


class ContextCompactionReadinessChecker:
    def __init__(
        self,
        *,
        dropped_recommend_threshold: int = 5,
        collapsed_recommend_threshold: int = 5,
    ) -> None:
        self.dropped_recommend_threshold = dropped_recommend_threshold
        self.collapsed_recommend_threshold = collapsed_recommend_threshold

    def evaluate(
        self,
        result: ContextCompactionResult,
        budget: ContextBudget,
    ) -> ContextCompactionReadiness:
        usable = budget.usable_chars()
        remaining_over_budget = result.total_chars > usable
        truncated_count = len(result.truncated_block_ids)
        dropped_count = len(result.dropped_block_ids)
        collapsed_count = int(result.result_attrs.get("collapsed_block_count") or 0)
        severe_warnings = [
            warning for warning in result.warnings if "exceeds" in warning.lower()
        ]
        if remaining_over_budget:
            status = "over_budget"
        elif truncated_count or dropped_count or collapsed_count or result.warnings:
            status = "warning"
        elif severe_warnings:
            status = "warning"
        else:
            status = "ok"
        auto_compact_recommended = (
            remaining_over_budget
            or dropped_count > self.dropped_recommend_threshold
            or collapsed_count > self.collapsed_recommend_threshold
        )
        return ContextCompactionReadiness(
            readiness_id=f"context_readiness:{uuid4()}",
            generated_at=utc_now_iso(),
            status=status,
            total_chars=result.total_chars,
            total_estimated_tokens=result.total_estimated_tokens,
            budget=budget.to_dict(),
            layer_summary=[
                {
                    "layer_name": layer.layer_name,
                    "changed": layer.changed,
                    "truncated_count": len(layer.truncated_block_ids),
                    "dropped_count": len(layer.dropped_block_ids),
                    "created_count": len(layer.created_block_ids),
                    "warnings": list(layer.warnings),
                    "result_attrs": dict(layer.result_attrs),
                }
                for layer in result.layer_results
            ],
            truncated_block_count=truncated_count,
            dropped_block_count=dropped_count,
            collapsed_block_count=collapsed_count,
            remaining_over_budget=remaining_over_budget,
            auto_compact_recommended=auto_compact_recommended,
            warnings=list(result.warnings),
            readiness_attrs={
                "usable_chars": usable,
                "dropped_recommend_threshold": self.dropped_recommend_threshold,
                "collapsed_recommend_threshold": self.collapsed_recommend_threshold,
            },
        )
