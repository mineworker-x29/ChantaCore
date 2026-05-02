from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Skill:
    """Minimal skill descriptor for object-centric runtime tracing."""

    skill_id: str
    skill_name: str
    description: str
    execution_type: str
    input_schema: dict[str, Any] = field(default_factory=dict)
    output_schema: dict[str, Any] = field(default_factory=dict)
    skill_attrs: dict[str, Any] = field(default_factory=dict)
