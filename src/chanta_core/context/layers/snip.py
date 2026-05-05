from __future__ import annotations

from chanta_core.context.block import ContextBlock
from chanta_core.context.budget import ContextBudget
from chanta_core.context.layers.base import is_protected, total_chars
from chanta_core.context.result import ContextCompactionLayerResult


class SnipLayer:
    name = "SnipLayer"

    def apply(
        self,
        blocks: list[ContextBlock],
        budget: ContextBudget,
    ) -> ContextCompactionLayerResult:
        usable = budget.usable_chars()
        if total_chars(blocks) <= usable:
            return ContextCompactionLayerResult(
                layer_name=self.name,
                blocks=list(blocks),
                changed=False,
            )

        keep_by_id = {block.block_id for block in blocks}
        dropped: list[str] = []
        candidates = [
            (index, block)
            for index, block in enumerate(blocks)
            if not is_protected(block)
        ]
        candidates.sort(key=lambda item: (item[1].priority, -item[0]))
        current_total = total_chars(blocks)
        for _, block in candidates:
            if current_total <= usable:
                break
            keep_by_id.remove(block.block_id)
            dropped.append(block.block_id)
            current_total -= block.char_length

        remaining = [block for block in blocks if block.block_id in keep_by_id]
        warnings: list[str] = []
        if total_chars(remaining) > usable:
            warnings.append(
                "Context remains over budget after SnipLayer; protected blocks were kept."
            )
        elif dropped:
            warnings.append(f"SnipLayer dropped {len(dropped)} low-priority block(s).")
        return ContextCompactionLayerResult(
            layer_name=self.name,
            blocks=remaining,
            changed=bool(dropped),
            dropped_block_ids=dropped,
            warnings=warnings,
        )
