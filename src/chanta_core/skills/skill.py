from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Skill:
    """Minimal skill descriptor; execution contracts will be added later."""

    skill_id: str
    name: str
    description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
