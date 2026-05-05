from __future__ import annotations

from chanta_core.context.block import ContextBlock
from chanta_core.context.budget import ContextBudget
from chanta_core.context.layers import (
    AutoCompactLayer,
    BudgetReductionLayer,
    ContextCollapseLayer,
    ContextCompactionLayer,
    MicrocompactLayer,
    SnipLayer,
)
from chanta_core.context.layers.base import total_chars, total_estimated_tokens
from chanta_core.context.result import (
    ContextCompactionLayerResult,
    ContextCompactionResult,
)


class ContextCompactionPipeline:
    def __init__(self, layers: list[ContextCompactionLayer] | None = None) -> None:
        self.layers = layers or []

    @classmethod
    def default(cls) -> "ContextCompactionPipeline":
        return cls(
            layers=[
                BudgetReductionLayer(),
                SnipLayer(),
                MicrocompactLayer(),
                ContextCollapseLayer(),
                AutoCompactLayer(enabled=False),
            ]
        )

    def run(
        self,
        blocks: list[ContextBlock],
        budget: ContextBudget,
    ) -> ContextCompactionResult:
        budget.validate()
        current_blocks = list(blocks)
        layer_results: list[ContextCompactionLayerResult] = []
        truncated: list[str] = []
        dropped: list[str] = []
        warnings: list[str] = []
        for layer in self.layers:
            result = layer.apply(current_blocks, budget)
            current_blocks = result.blocks
            layer_results.append(result)
            truncated.extend(result.truncated_block_ids)
            dropped.extend(result.dropped_block_ids)
            warnings.extend(result.warnings)

        chars = total_chars(current_blocks)
        tokens = total_estimated_tokens(current_blocks)
        if chars > budget.usable_chars():
            warnings.append(
                "Context exceeds usable character budget after all deterministic layers."
            )
        if tokens > budget.max_total_estimated_tokens:
            warnings.append(
                "Context exceeds estimated token budget after deterministic compaction."
            )
        return ContextCompactionResult(
            blocks=current_blocks,
            layer_results=layer_results,
            total_chars=chars,
            total_estimated_tokens=tokens,
            truncated_block_ids=truncated,
            dropped_block_ids=dropped,
            warnings=warnings,
            result_attrs={
                "layer_count": len(self.layers),
                "budget": budget.to_dict(),
            },
        )
