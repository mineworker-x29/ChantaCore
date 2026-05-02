from __future__ import annotations

from chanta_core.llm.types import ChatMessage


class ProcessContextAssembler:
    def assemble_for_llm_chat(
        self,
        user_input: str,
        system_prompt: str | None = None,
    ) -> list[ChatMessage]:
        messages: list[ChatMessage] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_input})
        return messages
