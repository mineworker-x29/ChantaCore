from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.session.errors import SessionContextPolicyError


STRATEGIES = {"recent_only", "recent_plus_summary", "manual", "other"}
STATUSES = {"active", "draft", "deprecated", "archived"}


@dataclass(frozen=True)
class SessionContextPolicy:
    policy_id: str
    policy_name: str | None
    max_turns: int | None
    max_messages: int | None
    max_chars: int | None
    include_user_messages: bool
    include_assistant_messages: bool
    include_system_messages: bool
    include_tool_messages: bool
    strategy: str
    status: str
    created_at: str
    policy_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.strategy not in STRATEGIES:
            raise SessionContextPolicyError(f"Unsupported strategy: {self.strategy}")
        if self.status not in STATUSES:
            raise SessionContextPolicyError(f"Unsupported status: {self.status}")
        for field_name in ["max_turns", "max_messages", "max_chars"]:
            value = getattr(self, field_name)
            if value is not None and value < 0:
                raise SessionContextPolicyError(f"{field_name} must be non-negative")

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "policy_name": self.policy_name,
            "max_turns": self.max_turns,
            "max_messages": self.max_messages,
            "max_chars": self.max_chars,
            "include_user_messages": self.include_user_messages,
            "include_assistant_messages": self.include_assistant_messages,
            "include_system_messages": self.include_system_messages,
            "include_tool_messages": self.include_tool_messages,
            "strategy": self.strategy,
            "status": self.status,
            "created_at": self.created_at,
            "policy_attrs": dict(self.policy_attrs),
        }
