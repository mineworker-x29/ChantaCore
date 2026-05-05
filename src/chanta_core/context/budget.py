from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.context.errors import ContextBudgetError


@dataclass(frozen=True)
class ContextBudget:
    max_total_chars: int = 12000
    max_total_estimated_tokens: int = 3000
    max_block_chars: int = 3000
    max_tool_result_chars: int = 2000
    max_pig_context_chars: int = 2500
    max_report_chars: int = 2500
    max_artifact_chars: int = 1500
    max_workspace_chars: int = 2000
    max_repo_chars: int = 2000
    reserve_chars: int = 1000
    budget_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "max_total_chars": self.max_total_chars,
            "max_total_estimated_tokens": self.max_total_estimated_tokens,
            "max_block_chars": self.max_block_chars,
            "max_tool_result_chars": self.max_tool_result_chars,
            "max_pig_context_chars": self.max_pig_context_chars,
            "max_report_chars": self.max_report_chars,
            "max_artifact_chars": self.max_artifact_chars,
            "max_workspace_chars": self.max_workspace_chars,
            "max_repo_chars": self.max_repo_chars,
            "reserve_chars": self.reserve_chars,
            "budget_attrs": self.budget_attrs,
        }

    def validate(self) -> None:
        max_values = {
            "max_total_chars": self.max_total_chars,
            "max_total_estimated_tokens": self.max_total_estimated_tokens,
            "max_block_chars": self.max_block_chars,
            "max_tool_result_chars": self.max_tool_result_chars,
            "max_pig_context_chars": self.max_pig_context_chars,
            "max_report_chars": self.max_report_chars,
            "max_artifact_chars": self.max_artifact_chars,
            "max_workspace_chars": self.max_workspace_chars,
            "max_repo_chars": self.max_repo_chars,
        }
        for name, value in max_values.items():
            if value <= 0:
                raise ContextBudgetError(f"{name} must be > 0")
        if self.reserve_chars < 0:
            raise ContextBudgetError("reserve_chars must be >= 0")
        if self.max_total_chars <= self.reserve_chars:
            raise ContextBudgetError("max_total_chars must be > reserve_chars")
        if self.max_total_estimated_tokens <= 0:
            raise ContextBudgetError("max_total_estimated_tokens must be > 0")

    def usable_chars(self) -> int:
        self.validate()
        return self.max_total_chars - self.reserve_chars
