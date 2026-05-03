from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class OCPXVariantSummary:
    variant_key: str
    activity_sequence: list[str]
    trace_count: int
    success_count: int
    failure_count: int
    skill_ids: list[str]
    example_process_instance_ids: list[str]
    variant_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "variant_key": self.variant_key,
            "activity_sequence": self.activity_sequence,
            "trace_count": self.trace_count,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "skill_ids": self.skill_ids,
            "example_process_instance_ids": self.example_process_instance_ids,
            "variant_attrs": self.variant_attrs,
        }
