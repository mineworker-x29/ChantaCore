from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.traces.event import AgentEvent


@dataclass(frozen=True)
class AgentRunResult:
    session_id: str
    agent_id: str
    user_input: str
    response_text: str
    events: list[AgentEvent]
    metadata: dict[str, Any] = field(default_factory=dict)
