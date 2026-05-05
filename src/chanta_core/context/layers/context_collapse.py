from __future__ import annotations

from typing import Any

from chanta_core.context.block import ContextBlock, make_context_block
from chanta_core.context.budget import ContextBudget
from chanta_core.context.layers.base import is_protected, total_chars
from chanta_core.context.result import ContextCompactionLayerResult


class ContextCollapseLayer:
    name = "ContextCollapseLayer"

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

        candidates = [
            (index, block)
            for index, block in enumerate(blocks)
            if not is_protected(block)
        ]
        candidates.sort(key=lambda item: (item[1].priority, -item[0]))
        if not candidates:
            return ContextCompactionLayerResult(
                layer_name=self.name,
                blocks=list(blocks),
                changed=False,
                warnings=[
                    "ContextCollapseLayer could not collapse context; only protected blocks remain."
                ],
            )

        collapsed: list[ContextBlock] = []
        keep_ids = {block.block_id for block in blocks}
        remaining = list(blocks)
        collapse_block: ContextBlock | None = None
        for _, block in candidates:
            collapsed.append(block)
            keep_ids.remove(block.block_id)
            remaining = [item for item in blocks if item.block_id in keep_ids]
            collapse_block = self._make_collapse_block(collapsed)
            if total_chars(remaining) + collapse_block.char_length <= usable:
                break

        dropped_ids = [block.block_id for block in collapsed]
        warnings: list[str] = [
            f"ContextCollapseLayer collapsed {len(collapsed)} low-priority block(s)."
        ]
        if collapse_block and total_chars(remaining) + collapse_block.char_length <= usable:
            next_blocks = remaining + [collapse_block]
            created = [collapse_block.block_id]
        else:
            next_blocks = remaining
            created = []
            warnings.append("Collapsed reference block did not fit and was dropped.")

        if total_chars(next_blocks) > usable:
            warnings.append(
                "Context remains over budget after ContextCollapseLayer; protected blocks were kept."
            )
        return ContextCompactionLayerResult(
            layer_name=self.name,
            blocks=next_blocks,
            changed=True,
            dropped_block_ids=dropped_ids,
            created_block_ids=created,
            warnings=warnings,
        )

    def _make_collapse_block(self, blocks: list[ContextBlock]) -> ContextBlock:
        priority = min((block.priority for block in blocks), default=10)
        lines = [
            f"Collapsed block count: {len(blocks)}",
            "Collapsed blocks:",
        ]
        refs: list[dict[str, Any]] = []
        for block in blocks:
            lines.append(f"- {block.title} ({block.block_type})")
            for ref in block.refs:
                refs.append(ref)
                lines.append(f"  ref: {self._format_ref(ref)}")
        lines.append(
            "Raw content preserved in source stores; not included in prompt context."
        )
        return make_context_block(
            block_type="other",
            title="Collapsed Context References",
            content="\n".join(lines),
            priority=priority,
            source="context_collapse",
            refs=refs,
            block_attrs={"collapsed_block_count": len(blocks)},
        )

    @staticmethod
    def _format_ref(ref: dict[str, Any]) -> str:
        visible = []
        for key in sorted(ref):
            value = ref[key]
            if value is not None:
                visible.append(f"{key}={value}")
            if len(visible) >= 4:
                break
        return ", ".join(visible) if visible else "none"
