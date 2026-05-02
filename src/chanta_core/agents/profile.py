from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentProfile:
    agent_id: str
    name: str
    role: str
    system_prompt: str
    default_temperature: float
    max_tokens: int
