from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.context.budget import ContextBudget
from chanta_core.context.readiness import ContextCompactionReadinessChecker
from chanta_core.context.result import ContextCompactionResult
from chanta_core.utility.time import utc_now_iso


@dataclass(frozen=True)
class ContextCompactionReport:
    report_id: str
    generated_at: str
    status: str
    total_chars: int
    total_estimated_tokens: int
    layer_reports: list[dict[str, Any]]
    readiness: dict[str, Any]
    report_text: str
    report_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "generated_at": self.generated_at,
            "status": self.status,
            "total_chars": self.total_chars,
            "total_estimated_tokens": self.total_estimated_tokens,
            "layer_reports": self.layer_reports,
            "readiness": self.readiness,
            "report_text": self.report_text,
            "report_attrs": self.report_attrs,
        }


class ContextCompactionReporter:
    def __init__(
        self,
        readiness_checker: ContextCompactionReadinessChecker | None = None,
    ) -> None:
        self.readiness_checker = readiness_checker or ContextCompactionReadinessChecker()

    def build_report(
        self,
        result: ContextCompactionResult,
        budget: ContextBudget,
    ) -> ContextCompactionReport:
        readiness = self.readiness_checker.evaluate(result, budget)
        layer_reports = [
            {
                "layer_name": layer.layer_name,
                "changed": layer.changed,
                "truncated_count": len(layer.truncated_block_ids),
                "dropped_count": len(layer.dropped_block_ids),
                "created_count": len(layer.created_block_ids),
                "auto_compact_disabled": layer.result_attrs.get("disabled")
                if layer.layer_name == "AutoCompactLayer"
                else None,
                "warnings": list(layer.warnings),
            }
            for layer in result.layer_results
        ]
        report_text = self._render_text(
            result=result,
            budget=budget,
            readiness=readiness.to_dict(),
            layer_reports=layer_reports,
        )
        return ContextCompactionReport(
            report_id=f"context_compaction_report:{uuid4()}",
            generated_at=utc_now_iso(),
            status=readiness.status,
            total_chars=result.total_chars,
            total_estimated_tokens=result.total_estimated_tokens,
            layer_reports=layer_reports,
            readiness=readiness.to_dict(),
            report_text=report_text,
            report_attrs={
                "usable_chars": budget.usable_chars(),
                "auto_compact_recommended": readiness.auto_compact_recommended,
            },
        )

    @staticmethod
    def _render_text(
        *,
        result: ContextCompactionResult,
        budget: ContextBudget,
        readiness: dict[str, Any],
        layer_reports: list[dict[str, Any]],
    ) -> str:
        auto_compact_layer = next(
            (
                layer
                for layer in layer_reports
                if layer["layer_name"] == "AutoCompactLayer"
            ),
            None,
        )
        auto_compact_disabled = (
            auto_compact_layer.get("auto_compact_disabled")
            if auto_compact_layer
            else "unknown"
        )
        lines = [
            "Context Compaction Report",
            f"Status: {readiness['status']}",
            f"Total chars: {result.total_chars}",
            f"Estimated tokens: {result.total_estimated_tokens}",
            f"Usable char budget: {budget.usable_chars()}",
            f"Truncated blocks: {len(result.truncated_block_ids)}",
            f"Dropped blocks: {len(result.dropped_block_ids)}",
            f"Collapsed blocks: {result.result_attrs.get('collapsed_block_count', 0)}",
            f"AutoCompact disabled: {auto_compact_disabled}",
            f"AutoCompact recommended: {readiness['auto_compact_recommended']}",
            "Layers:",
        ]
        for layer in layer_reports:
            lines.append(
                "- "
                f"{layer['layer_name']}: changed={layer['changed']}, "
                f"truncated={layer['truncated_count']}, "
                f"dropped={layer['dropped_count']}, created={layer['created_count']}"
            )
        if result.warnings:
            lines.append("Warnings:")
            lines.extend(f"- {warning}" for warning in result.warnings)
        return "\n".join(lines)
