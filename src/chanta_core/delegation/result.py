from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class DelegationResult:
    """Minimal delegation result placeholder."""

    packet_id: str
    status: str
    response: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
