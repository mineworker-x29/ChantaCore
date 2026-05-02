from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, TypedDict

Role = Literal["system", "user", "assistant", "tool"]

class ChatMessage(TypedDict):
    role: Role
    content: str


@dataclass(frozen=True)
class ChatRequest:
    messages: list[ChatMessage]
    temperature: float | None = None
    max_tokens: int | None = None

    def as_payload(self, model: str) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": model,
            "messages": self.messages,
        }
        if self.temperature is not None:
            payload["temperature"] = self.temperature
        if self.max_tokens is not None:
            payload["max_tokens"] = self.max_tokens
        return payload


@dataclass(frozen=True)
class ChatResponse:
    text: str
    raw: dict[str, Any]
