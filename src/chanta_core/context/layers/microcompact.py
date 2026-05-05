from __future__ import annotations

from chanta_core.context.block import (
    ContextBlock,
    replace_context_block_content,
    truncate_text,
)
from chanta_core.context.budget import ContextBudget
from chanta_core.context.layers.base import block_char_limit
from chanta_core.context.result import ContextCompactionLayerResult


class MicrocompactLayer:
    name = "MicrocompactLayer"
    line_marker = "...[line truncated by MicrocompactLayer]..."
    list_marker = "...[middle lines omitted by MicrocompactLayer]..."

    def __init__(self, *, first_lines: int = 20, last_lines: int = 5) -> None:
        self.first_lines = first_lines
        self.last_lines = last_lines

    def apply(
        self,
        blocks: list[ContextBlock],
        budget: ContextBudget,
    ) -> ContextCompactionLayerResult:
        next_blocks: list[ContextBlock] = []
        changed_ids: list[str] = []
        for block in blocks:
            compacted = self._microcompact_content(block.content, block, budget)
            if compacted != block.content:
                next_blocks.append(
                    replace_context_block_content(
                        block,
                        compacted,
                        block_attrs={"microcompacted": True},
                    )
                )
                changed_ids.append(block.block_id)
            else:
                next_blocks.append(block)
        return ContextCompactionLayerResult(
            layer_name=self.name,
            blocks=next_blocks,
            changed=bool(changed_ids),
            result_attrs={"microcompacted_block_ids": changed_ids},
        )

    def _microcompact_content(
        self,
        content: str,
        block: ContextBlock,
        budget: ContextBudget,
    ) -> str:
        lines = content.splitlines()
        compacted_lines: list[str] = []
        previous_blank = False
        for line in lines:
            next_line = line.rstrip()
            if len(next_line) > 500:
                next_line, _ = truncate_text(next_line, 500, self.line_marker)
            is_blank = next_line == ""
            if is_blank and previous_blank:
                continue
            compacted_lines.append(next_line)
            previous_blank = is_blank

        compacted = "\n".join(compacted_lines).strip()
        limit = block_char_limit(block, budget)
        if (
            len(compacted) > limit
            and len(compacted_lines) > self.first_lines + self.last_lines
        ):
            compacted = "\n".join(
                compacted_lines[: self.first_lines]
                + [self.list_marker]
                + compacted_lines[-self.last_lines :]
            ).strip()
        return compacted
