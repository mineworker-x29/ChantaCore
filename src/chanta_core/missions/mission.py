from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Mission:
    """Minimal mission descriptor for future multi-step agent work."""

    mission_id: str
    objective: str
    metadata: dict[str, Any] = field(default_factory=dict)
