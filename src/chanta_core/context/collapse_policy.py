from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.context.errors import ContextBudgetError


@dataclass(frozen=True)
class ContextCollapsePolicy:
    enabled: bool = True
    min_blocks_to_collapse: int = 2
    max_collapsed_block_chars: int = 1500
    max_references: int = 20
    group_by_block_type: bool = True
    include_titles: bool = True
    include_sources: bool = True
    include_ref_counts: bool = True
    collapse_block_priority: int = 15
    policy_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "min_blocks_to_collapse": self.min_blocks_to_collapse,
            "max_collapsed_block_chars": self.max_collapsed_block_chars,
            "max_references": self.max_references,
            "group_by_block_type": self.group_by_block_type,
            "include_titles": self.include_titles,
            "include_sources": self.include_sources,
            "include_ref_counts": self.include_ref_counts,
            "collapse_block_priority": self.collapse_block_priority,
            "policy_attrs": self.policy_attrs,
        }

    def validate(self) -> None:
        if not isinstance(self.enabled, bool):
            raise ContextBudgetError("enabled must be a bool")
        if self.min_blocks_to_collapse < 1:
            raise ContextBudgetError("min_blocks_to_collapse must be >= 1")
        if self.max_collapsed_block_chars <= 0:
            raise ContextBudgetError("max_collapsed_block_chars must be > 0")
        if self.max_references <= 0:
            raise ContextBudgetError("max_references must be > 0")
        if not isinstance(self.collapse_block_priority, int):
            raise ContextBudgetError("collapse_block_priority must be an int")
