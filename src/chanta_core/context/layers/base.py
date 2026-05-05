from __future__ import annotations

from typing import Protocol

from chanta_core.context.block import ContextBlock
from chanta_core.context.budget import ContextBudget
from chanta_core.context.result import ContextCompactionLayerResult


class ContextCompactionLayer(Protocol):
    name: str

    def apply(
        self,
        blocks: list[ContextBlock],
        budget: ContextBudget,
    ) -> ContextCompactionLayerResult:
        ...


def total_chars(blocks: list[ContextBlock]) -> int:
    return sum(block.char_length for block in blocks)


def total_estimated_tokens(blocks: list[ContextBlock]) -> int:
    return sum(block.token_estimate for block in blocks)


def block_char_limit(block: ContextBlock, budget: ContextBudget) -> int:
    if block.block_type == "tool_result":
        return budget.max_tool_result_chars
    if block.block_type == "pig_context":
        return budget.max_pig_context_chars
    if block.block_type == "pig_report":
        return budget.max_report_chars
    if block.block_type == "artifact":
        return budget.max_artifact_chars
    if block.block_type == "workspace":
        return budget.max_workspace_chars
    if block.block_type == "repo":
        return budget.max_repo_chars
    return budget.max_block_chars


def is_protected(block: ContextBlock) -> bool:
    return block.block_type in {"system", "user_request"}
