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
from chanta_core.context.collapse_policy import ContextCollapsePolicy
from chanta_core.context.microcompact_policy import MicrocompactPolicy
from chanta_core.context.policy import ContextHistoryPolicy, SessionContextPolicy
from chanta_core.context.result import (
    ContextCompactionLayerResult,
    ContextCompactionResult,
)


class ContextCompactionPipeline:
    def __init__(self, layers: list[ContextCompactionLayer] | None = None) -> None:
        self.layers = layers or []

    @classmethod
    def default(
        cls,
        history_policy: ContextHistoryPolicy | None = None,
        session_context_policy: SessionContextPolicy | None = None,
        microcompact_policy: MicrocompactPolicy | None = None,
        collapse_policy: ContextCollapsePolicy | None = None,
    ) -> "ContextCompactionPipeline":
        return cls(
            layers=[
                BudgetReductionLayer(),
                SnipLayer(
                    history_policy=history_policy,
                    session_context_policy=session_context_policy,
                ),
                MicrocompactLayer(policy=microcompact_policy),
                ContextCollapseLayer(policy=collapse_policy),
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
        history_block_count_before = sum(
            1
            for block in current_blocks
            if block.block_type == "history" or block.block_attrs.get("is_history")
        )
        layer_results: list[ContextCompactionLayerResult] = []
        truncated: list[str] = []
        dropped: list[str] = []
        dropped_blocks_by_id: dict[str, ContextBlock] = {}
        warnings: list[str] = []
        for layer in self.layers:
            before_blocks_by_id = {block.block_id: block for block in current_blocks}
            if isinstance(layer, ContextCollapseLayer):
                result = layer.apply_with_projected_blocks(
                    current_blocks,
                    budget,
                    projected_blocks=list(dropped_blocks_by_id.values()),
                )
            else:
                result = layer.apply(current_blocks, budget)
            current_blocks = result.blocks
            layer_results.append(result)
            truncated.extend(result.truncated_block_ids)
            dropped.extend(result.dropped_block_ids)
            for block_id in result.dropped_block_ids:
                if block_id in before_blocks_by_id:
                    dropped_blocks_by_id[block_id] = before_blocks_by_id[block_id]
            warnings.extend(result.warnings)

        chars = total_chars(current_blocks)
        tokens = total_estimated_tokens(current_blocks)
        history_block_count_after = sum(
            1
            for block in current_blocks
            if block.block_type == "history" or block.block_attrs.get("is_history")
        )
        snipped_history_count = sum(
            len(result.result_attrs.get("dropped_history_block_ids") or [])
            for result in layer_results
        )
        protected_block_count = sum(
            len(result.result_attrs.get("protected_block_ids") or [])
            for result in layer_results
        )
        collapsed_reference_count = sum(
            int(result.result_attrs.get("reference_count") or 0)
            for result in layer_results
        )
        collapsed_block_count = sum(
            int(result.result_attrs.get("collapsed_block_count") or 0)
            for result in layer_results
        )
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
            truncated_block_ids=_dedupe_ids(truncated),
            dropped_block_ids=_dedupe_ids(dropped),
            warnings=warnings,
            result_attrs={
                "layer_count": len(self.layers),
                "budget": budget.to_dict(),
                "selected_block_count": len(current_blocks),
                "history_block_count_before": history_block_count_before,
                "history_block_count_after": history_block_count_after,
                "snipped_history_count": snipped_history_count,
                "protected_block_count": protected_block_count,
                "collapsed_reference_count": collapsed_reference_count,
                "collapsed_block_count": collapsed_block_count,
            },
        )


def _dedupe_ids(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result
