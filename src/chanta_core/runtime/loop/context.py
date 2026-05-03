from __future__ import annotations

from typing import TYPE_CHECKING

from chanta_core.llm.types import ChatMessage

if TYPE_CHECKING:
    from chanta_core.pig.context import PIGContext


class ProcessContextAssembler:
    def assemble_for_llm_chat(
        self,
        user_input: str,
        system_prompt: str | None = None,
        pig_context: PIGContext | None = None,
    ) -> list[ChatMessage]:
        messages: list[ChatMessage] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if pig_context is not None:
            messages.append({"role": "system", "content": pig_context.context_text})
        messages.append({"role": "user", "content": user_input})
        return messages
