from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


ToolPermissionMode = Literal[
    "readonly",
    "safe_internal",
    "approval_required",
    "deny_all",
]

ToolRiskLevel = Literal[
    "readonly",
    "internal_readonly",
    "internal_compute",
    "internal_intelligence",
    "write",
    "network",
    "shell",
    "dangerous",
    "unknown",
]


@dataclass(frozen=True)
class ToolPermissionDecision:
    allowed: bool
    decision: str
    reason: str
    mode: str
    risk_level: str
    requires_approval: bool = False
    decision_attrs: dict[str, Any] = field(default_factory=dict)

    @property
    def policy_attrs(self) -> dict[str, Any]:
        return self.decision_attrs

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed": self.allowed,
            "decision": self.decision,
            "reason": self.reason,
            "mode": self.mode,
            "risk_level": self.risk_level,
            "requires_approval": self.requires_approval,
            "decision_attrs": self.decision_attrs,
            # Backward-compatible key used by older callers/tests.
            "policy_attrs": self.decision_attrs,
        }
