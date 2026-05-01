from __future__ import annotations

from chanta_core.llm.types import ChatMessage

def build_messages(
    user_message: str,
    system_message: str | None = None,
) -> list[ChatMessage]:
    messages: list[ChatMessage] = []

    if system_message:
        messages.append({"role": "system", "content": system_message})

    messages.append({"role": "user", "content": user_message})

    return messages