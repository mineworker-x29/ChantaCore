from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.context.errors import ContextBudgetError


@dataclass(frozen=True)
class ContextHistoryPolicy:
    max_history_blocks: int = 12
    max_recent_history_blocks: int = 6
    preserve_last_user_blocks: int = 2
    preserve_last_assistant_blocks: int = 2
    preserve_current_process_blocks: bool = True
    preserve_current_session_blocks: bool = True
    min_priority_to_keep: int = 50
    history_block_priority_decay: int = 5
    policy_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "max_history_blocks": self.max_history_blocks,
            "max_recent_history_blocks": self.max_recent_history_blocks,
            "preserve_last_user_blocks": self.preserve_last_user_blocks,
            "preserve_last_assistant_blocks": self.preserve_last_assistant_blocks,
            "preserve_current_process_blocks": self.preserve_current_process_blocks,
            "preserve_current_session_blocks": self.preserve_current_session_blocks,
            "min_priority_to_keep": self.min_priority_to_keep,
            "history_block_priority_decay": self.history_block_priority_decay,
            "policy_attrs": self.policy_attrs,
        }

    def validate(self) -> None:
        if self.max_history_blocks <= 0:
            raise ContextBudgetError("max_history_blocks must be > 0")
        if self.max_recent_history_blocks <= 0:
            raise ContextBudgetError("max_recent_history_blocks must be > 0")
        if self.preserve_last_user_blocks < 0:
            raise ContextBudgetError("preserve_last_user_blocks must be >= 0")
        if self.preserve_last_assistant_blocks < 0:
            raise ContextBudgetError("preserve_last_assistant_blocks must be >= 0")
        if not 0 <= self.min_priority_to_keep <= 100:
            raise ContextBudgetError("min_priority_to_keep must be between 0 and 100")
        if self.history_block_priority_decay < 0:
            raise ContextBudgetError("history_block_priority_decay must be >= 0")


@dataclass(frozen=True)
class SessionContextPolicy:
    session_id: str | None
    process_instance_id: str | None
    include_history: bool = True
    include_pig_context: bool = False
    include_reports: bool = False
    include_tool_results: bool = True
    history_policy: ContextHistoryPolicy = field(default_factory=ContextHistoryPolicy)
    policy_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "process_instance_id": self.process_instance_id,
            "include_history": self.include_history,
            "include_pig_context": self.include_pig_context,
            "include_reports": self.include_reports,
            "include_tool_results": self.include_tool_results,
            "history_policy": self.history_policy.to_dict(),
            "policy_attrs": self.policy_attrs,
        }
