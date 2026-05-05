from __future__ import annotations

from chanta_core.context.block import (
    ContextBlock,
    replace_context_block_content,
    truncate_text,
)
from chanta_core.context.budget import ContextBudget
from chanta_core.context.layers.base import block_char_limit
from chanta_core.context.result import ContextCompactionLayerResult


class BudgetReductionLayer:
    name = "BudgetReductionLayer"
    marker = "\n...[truncated by BudgetReductionLayer]..."

    def apply(
        self,
        blocks: list[ContextBlock],
        budget: ContextBudget,
    ) -> ContextCompactionLayerResult:
        next_blocks: list[ContextBlock] = []
        truncated: list[str] = []
        for block in blocks:
            limit = block_char_limit(block, budget)
            content, changed = truncate_text(block.content, limit, self.marker)
            if changed:
                next_blocks.append(
                    replace_context_block_content(
                        block,
                        content,
                        was_truncated=True,
                    )
                )
                truncated.append(block.block_id)
            else:
                next_blocks.append(block)
        return ContextCompactionLayerResult(
            layer_name=self.name,
            blocks=next_blocks,
            changed=bool(truncated),
            truncated_block_ids=truncated,
        )
