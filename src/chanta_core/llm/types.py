from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, TypedDict

Role = Literal["system", "user", "assistant", "tool"]

class ChatMessage(TypedDict):
    role: Role
    content: str