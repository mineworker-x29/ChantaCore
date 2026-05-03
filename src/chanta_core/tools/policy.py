from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.tools.request import ToolRequest
from chanta_core.tools.tool import Tool


@dataclass(frozen=True)
class ToolAuthorization:
    allowed: bool
    decision: str
    reason: str
    policy_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed": self.allowed,
            "decision": self.decision,
            "reason": self.reason,
            "policy_attrs": self.policy_attrs,
        }


class ToolPolicy:
    ALLOWED_LEVELS = {
        "readonly",
        "internal_readonly",
        "internal_compute",
        "internal_intelligence",
    }

    DENIED_LEVELS = {"write", "network", "shell", "dangerous"}

    def authorize(self, tool: Tool, request: ToolRequest) -> ToolAuthorization:
        safety_level = str(tool.safety_level or "unknown")
        if safety_level in self.ALLOWED_LEVELS:
            return ToolAuthorization(
                allowed=True,
                decision="allow",
                reason=f"safety_level allowed: {safety_level}",
                policy_attrs={
                    "safety_level": safety_level,
                    "tool_id": tool.tool_id,
                    "operation": request.operation,
                },
            )
        reason = (
            f"safety_level denied: {safety_level}"
            if safety_level in self.DENIED_LEVELS
            else f"safety_level denied or unknown: {safety_level}"
        )
        return ToolAuthorization(
            allowed=False,
            decision="deny",
            reason=reason,
            policy_attrs={
                "safety_level": safety_level,
                "tool_id": tool.tool_id,
                "operation": request.operation,
            },
        )
