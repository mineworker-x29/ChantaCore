from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.context.errors import ContextBudgetError


@dataclass(frozen=True)
class MicrocompactPolicy:
    max_lines: int = 40
    max_line_chars: int = 500
    max_activity_items: int = 30
    max_mapping_items: int = 20
    max_report_chars: int = 2500
    max_json_chars: int = 2000
    preserve_refs: bool = True
    policy_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "max_lines": self.max_lines,
            "max_line_chars": self.max_line_chars,
            "max_activity_items": self.max_activity_items,
            "max_mapping_items": self.max_mapping_items,
            "max_report_chars": self.max_report_chars,
            "max_json_chars": self.max_json_chars,
            "preserve_refs": self.preserve_refs,
            "policy_attrs": self.policy_attrs,
        }

    def validate(self) -> None:
        for name in [
            "max_lines",
            "max_line_chars",
            "max_activity_items",
            "max_mapping_items",
            "max_report_chars",
            "max_json_chars",
        ]:
            if getattr(self, name) <= 0:
                raise ContextBudgetError(f"{name} must be > 0")
        if not isinstance(self.preserve_refs, bool):
            raise ContextBudgetError("preserve_refs must be a bool")
