from __future__ import annotations

from typing import TYPE_CHECKING

from chanta_core.context import (
    ContextBlock,
    ContextBudget,
    ContextCompactionPipeline,
    ContextCompactionResult,
    ContextRenderer,
    make_context_block,
)
from chanta_core.llm.types import ChatMessage

if TYPE_CHECKING:
    from chanta_core.pig.context import PIGContext


class ProcessContextAssembler:
    def __init__(self) -> None:
        self.last_compaction_result: ContextCompactionResult | None = None

    def assemble_for_llm_chat(
        self,
        user_input: str,
        system_prompt: str | None = None,
        pig_context: PIGContext | None = None,
        extra_blocks: list[ContextBlock] | None = None,
        context_budget: ContextBudget | None = None,
        compaction_pipeline: ContextCompactionPipeline | None = None,
    ) -> list[ChatMessage]:
        self.last_compaction_result = None
        if context_budget is None and not extra_blocks:
            return self._assemble_legacy(
                user_input=user_input,
                system_prompt=system_prompt,
                pig_context=pig_context,
            )

        blocks = self._build_blocks(
            user_input=user_input,
            system_prompt=system_prompt,
            pig_context=pig_context,
            extra_blocks=extra_blocks,
        )
        if context_budget is not None:
            pipeline = compaction_pipeline or ContextCompactionPipeline.default()
            self.last_compaction_result = pipeline.run(blocks, context_budget)
            blocks = self.last_compaction_result.blocks

        renderer = ContextRenderer()
        messages: list[ChatMessage] = []
        for block in blocks:
            if block.block_type == "user_request":
                messages.append({"role": "user", "content": block.content})
            else:
                messages.append({"role": "system", "content": renderer.render_block(block)})
        return messages

    def _assemble_legacy(
        self,
        *,
        user_input: str,
        system_prompt: str | None,
        pig_context: PIGContext | None,
    ) -> list[ChatMessage]:
        messages: list[ChatMessage] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if pig_context is not None:
            messages.append({"role": "system", "content": pig_context.context_text})
        messages.append({"role": "user", "content": user_input})
        return messages

    def _build_blocks(
        self,
        *,
        user_input: str,
        system_prompt: str | None,
        pig_context: PIGContext | None,
        extra_blocks: list[ContextBlock] | None,
    ) -> list[ContextBlock]:
        blocks: list[ContextBlock] = []
        if system_prompt:
            blocks.append(
                make_context_block(
                    block_type="system",
                    title="System Prompt",
                    content=system_prompt,
                    priority=100,
                    source="runtime",
                )
            )
        if pig_context is not None:
            blocks.append(pig_context.to_context_block(priority=70))
        blocks.extend(extra_blocks or [])
        blocks.append(
            make_context_block(
                block_type="user_request",
                title="User Request",
                content=user_input,
                priority=100,
                source="runtime",
            )
        )
        return blocks
