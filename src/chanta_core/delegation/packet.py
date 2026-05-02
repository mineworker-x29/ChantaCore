from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class DelegationPacket:
    """Minimal packet for future agent-to-agent delegation."""

    packet_id: str
    target_agent_id: str
    instruction: str
    metadata: dict[str, Any] = field(default_factory=dict)
