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
        allow_approved_writes: bool = False,
    ) -> None:
        self.mode = mode
        self.risk_classifier = risk_classifier or ToolRiskClassifier()
        self.rule_set = rule_set or ToolPermissionRuleSet.default()
        self.allow_approved_writes = allow_approved_writes

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
        if self._is_allowed_approved_write(tool, request, risk):
            return ToolPermissionDecision(
                allowed=True,
                decision="allow",
                reason="Approved patch application allowed by explicit policy flag.",
                mode=self.mode,
                risk_level=risk.risk_level,
                requires_approval=False,
                decision_attrs={
                    "risk": risk.to_dict(),
                    "allow_approved_writes": self.allow_approved_writes,
                    "approval_validated_by_policy": True,
                },
            )
        if self._is_approval_ready_write(tool, request, risk):
            return ToolPermissionDecision(
                allowed=False,
                decision="approval_required",
                reason=(
                    "Approved patch application requires ToolPolicy"
                    "(allow_approved_writes=True)."
                ),
                mode=self.mode,
                risk_level=risk.risk_level,
                requires_approval=True,
                decision_attrs={
                    "risk": risk.to_dict(),
                    "allow_approved_writes": self.allow_approved_writes,
                    "approval_validated_by_policy": True,
                },
            )
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

    def _is_allowed_approved_write(self, tool: Tool, request: ToolRequest, risk) -> bool:
        if not self.allow_approved_writes:
            return False
        return self._is_approval_ready_write(tool, request, risk)

    def _is_approval_ready_write(self, tool: Tool, request: ToolRequest, risk) -> bool:
        if tool.tool_id != "tool:edit" or request.operation != "apply_approved_proposal":
            return False
        if risk.risk_level != "write":
            return False
        approval_text = str(request.input_attrs.get("approval_text") or "")
        approved_by = str(request.input_attrs.get("approved_by") or "")
        proposal_id = str(request.input_attrs.get("proposal_id") or "")
        return (
            "I APPROVE PATCH APPLICATION" in approval_text
            and bool(approved_by)
            and bool(proposal_id)
        )
