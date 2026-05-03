from __future__ import annotations

from chanta_core.tools.permission_rules import SAFE_RISK_LEVELS, ToolPermissionRuleSet
from chanta_core.tools.permissions import (
    ToolPermissionDecision,
    ToolPermissionMode,
)
from chanta_core.tools.request import ToolRequest
from chanta_core.tools.risk import ToolRiskClassifier
from chanta_core.tools.tool import Tool


ToolAuthorization = ToolPermissionDecision


class ToolPolicy:
    def __init__(
        self,
        mode: ToolPermissionMode = "safe_internal",
        risk_classifier: ToolRiskClassifier | None = None,
        rule_set: ToolPermissionRuleSet | None = None,
    ) -> None:
        self.mode = mode
        self.risk_classifier = risk_classifier or ToolRiskClassifier()
        self.rule_set = rule_set or ToolPermissionRuleSet.default()

    def authorize(self, tool: Tool, request: ToolRequest) -> ToolPermissionDecision:
        if self.mode == "deny_all":
            risk = self.risk_classifier.classify(tool, request)
            return ToolPermissionDecision(
                allowed=False,
                decision="deny",
                reason="Tool policy mode deny_all denies every operation.",
                mode=self.mode,
                risk_level=risk.risk_level,
                requires_approval=False,
                decision_attrs={"risk": risk.to_dict()},
            )

        risk = self.risk_classifier.classify(tool, request)
        decision = self.rule_set.evaluate(tool, request, risk, mode=self.mode)
        if decision is None:
            return ToolPermissionDecision(
                allowed=False,
                decision="deny",
                reason=f"No permission rule matched risk level: {risk.risk_level}",
                mode=self.mode,
                risk_level=risk.risk_level,
                requires_approval=False,
                decision_attrs={"risk": risk.to_dict()},
            )

        if self.mode in {"readonly", "safe_internal"}:
            if risk.risk_level in SAFE_RISK_LEVELS and decision.decision == "allow":
                return decision
            return ToolPermissionDecision(
                allowed=False,
                decision="deny",
                reason=f"Tool policy mode {self.mode} denied risk level: {risk.risk_level}",
                mode=self.mode,
                risk_level=risk.risk_level,
                requires_approval=False,
                decision_attrs=decision.decision_attrs,
            )

        if self.mode == "approval_required":
            if risk.risk_level in SAFE_RISK_LEVELS and decision.decision == "allow":
                return decision
            if risk.risk_level == "write" and decision.decision == "approval_required":
                return decision
            return ToolPermissionDecision(
                allowed=False,
                decision="deny",
                reason=(
                    f"Tool policy mode approval_required denied risk level: "
                    f"{risk.risk_level}"
                ),
                mode=self.mode,
                risk_level=risk.risk_level,
                requires_approval=False,
                decision_attrs=decision.decision_attrs,
            )

        return ToolPermissionDecision(
            allowed=False,
            decision="deny",
            reason=f"Unknown tool permission mode: {self.mode}",
            mode=str(self.mode),
            risk_level=risk.risk_level,
            requires_approval=False,
            decision_attrs={"risk": risk.to_dict()},
        )
