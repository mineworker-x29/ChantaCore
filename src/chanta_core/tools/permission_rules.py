from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.tools.permissions import ToolPermissionDecision
from chanta_core.tools.request import ToolRequest
from chanta_core.tools.risk import ToolOperationRisk
from chanta_core.tools.tool import Tool


SAFE_RISK_LEVELS = {
    "readonly",
    "internal_readonly",
    "internal_compute",
    "internal_intelligence",
}


@dataclass(frozen=True)
class ToolPermissionRule:
    rule_id: str
    effect: str
    tool_id: str | None = None
    operation: str | None = None
    risk_level: str | None = None
    reason: str = ""
    rule_attrs: dict[str, Any] = field(default_factory=dict)

    def matches(
        self,
        tool: Tool,
        request: ToolRequest,
        risk: ToolOperationRisk,
    ) -> bool:
        if self.tool_id is not None and self.tool_id != tool.tool_id:
            return False
        if self.operation is not None and self.operation != request.operation:
            return False
        if self.risk_level is not None and self.risk_level != risk.risk_level:
            return False
        return True

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "effect": self.effect,
            "tool_id": self.tool_id,
            "operation": self.operation,
            "risk_level": self.risk_level,
            "reason": self.reason,
            "rule_attrs": self.rule_attrs,
        }


@dataclass(frozen=True)
class ToolPermissionRuleSet:
    rules: list[ToolPermissionRule] = field(default_factory=list)

    @classmethod
    def default(cls) -> "ToolPermissionRuleSet":
        return cls(
            rules=[
                ToolPermissionRule(
                    rule_id="deny-dangerous",
                    effect="deny",
                    risk_level="dangerous",
                    reason="Dangerous tool operations are denied.",
                ),
                ToolPermissionRule(
                    rule_id="deny-shell",
                    effect="deny",
                    risk_level="shell",
                    reason="Shell tool operations are denied.",
                ),
                ToolPermissionRule(
                    rule_id="deny-network",
                    effect="deny",
                    risk_level="network",
                    reason="Network tool operations are denied.",
                ),
                ToolPermissionRule(
                    rule_id="approval-write",
                    effect="approval_required",
                    risk_level="write",
                    reason="Write tool operations require approval.",
                ),
                *[
                    ToolPermissionRule(
                        rule_id=f"allow-{risk}",
                        effect="allow",
                        risk_level=risk,
                        reason=f"Safe tool risk allowed: {risk}.",
                    )
                    for risk in sorted(SAFE_RISK_LEVELS)
                ],
            ]
        )

    def evaluate(
        self,
        tool: Tool,
        request: ToolRequest,
        risk: ToolOperationRisk,
        *,
        mode: str = "safe_internal",
    ) -> ToolPermissionDecision | None:
        matches = [rule for rule in self.rules if rule.matches(tool, request, risk)]
        for effect in ("deny", "approval_required", "allow"):
            rule = next((item for item in matches if item.effect == effect), None)
            if rule is not None:
                if effect == "deny":
                    return ToolPermissionDecision(
                        allowed=False,
                        decision="deny",
                        reason=rule.reason,
                        mode=mode,
                        risk_level=risk.risk_level,
                        requires_approval=False,
                        decision_attrs={
                            "matched_rule": rule.to_dict(),
                            "risk": risk.to_dict(),
                        },
                    )
                if effect == "approval_required":
                    return ToolPermissionDecision(
                        allowed=False,
                        decision="approval_required",
                        reason=rule.reason,
                        mode=mode,
                        risk_level=risk.risk_level,
                        requires_approval=True,
                        decision_attrs={
                            "matched_rule": rule.to_dict(),
                            "risk": risk.to_dict(),
                        },
                    )
                return ToolPermissionDecision(
                    allowed=True,
                    decision="allow",
                    reason=rule.reason,
                    mode=mode,
                    risk_level=risk.risk_level,
                    requires_approval=False,
                    decision_attrs={
                        "matched_rule": rule.to_dict(),
                        "risk": risk.to_dict(),
                    },
                )
        return None
