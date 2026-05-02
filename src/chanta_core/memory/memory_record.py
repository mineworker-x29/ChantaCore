from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class MemoryRecord:
    """Minimal memory item placeholder for future persistent memory."""

    record_id: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
