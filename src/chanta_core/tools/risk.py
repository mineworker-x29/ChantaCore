from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.tools.request import ToolRequest
from chanta_core.tools.tool import Tool


RISK_ORDER = {
    "readonly": 0,
    "internal_readonly": 1,
    "internal_compute": 2,
    "internal_intelligence": 3,
    "write": 4,
    "network": 5,
    "shell": 6,
    "dangerous": 7,
    "unknown": 8,
}

KNOWN_TOOL_RISKS = {
    "tool:echo": "readonly",
    "tool:ocel": "internal_readonly",
    "tool:ocpx": "internal_compute",
    "tool:pig": "internal_intelligence",
    "tool:workspace": "internal_readonly",
    "tool:repo": "internal_readonly",
}

EDIT_PROPOSAL_OPERATIONS = {
    "propose_text_replacement",
    "propose_comment_only",
    "summarize_recent_proposals",
}

RISKY_OPERATION_KEYWORDS = {
    "write": "dangerous",
    "delete": "dangerous",
    "remove": "dangerous",
    "move": "dangerous",
    "rename": "dangerous",
    "patch": "dangerous",
    "apply": "dangerous",
    "shell": "shell",
    "exec": "shell",
    "network": "network",
    "fetch": "network",
    "http": "network",
}


@dataclass(frozen=True)
class ToolOperationRisk:
    tool_id: str
    operation: str
    risk_level: str
    reason: str
    risk_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "tool_id": self.tool_id,
            "operation": self.operation,
            "risk_level": self.risk_level,
            "reason": self.reason,
            "risk_attrs": self.risk_attrs,
        }


class ToolRiskClassifier:
    def classify(self, tool: Tool, request: ToolRequest) -> ToolOperationRisk:
        if tool.tool_id == "tool:edit" and request.operation in EDIT_PROPOSAL_OPERATIONS:
            explicit_risk = self._explicit_risk(request)
            risk_level = _stricter("internal_readonly", explicit_risk)
            return ToolOperationRisk(
                tool_id=tool.tool_id,
                operation=request.operation,
                risk_level=risk_level,
                reason="proposal_only_edit_operation",
                risk_attrs={
                    "base_risk": tool.safety_level,
                    "operation_risk": "internal_readonly",
                    "explicit_risk": explicit_risk,
                    "proposal_only": True,
                },
            )
        base_risk = KNOWN_TOOL_RISKS.get(tool.tool_id, str(tool.safety_level or "unknown"))
        reason = "known_tool" if tool.tool_id in KNOWN_TOOL_RISKS else "tool_safety_level"
        operation_risk = self._operation_name_risk(request.operation)
        explicit_risk = self._explicit_risk(request)
        risk_level = _stricter(base_risk, operation_risk, explicit_risk)
        reasons = [reason]
        if operation_risk is not None:
            reasons.append("operation_name_risk")
        if explicit_risk is not None:
            reasons.append("explicit_risk_level")
        return ToolOperationRisk(
            tool_id=tool.tool_id,
            operation=request.operation,
            risk_level=risk_level,
            reason="+".join(reasons),
            risk_attrs={
                "base_risk": base_risk,
                "operation_risk": operation_risk,
                "explicit_risk": explicit_risk,
            },
        )

    def _operation_name_risk(self, operation: str) -> str | None:
        lowered = operation.lower()
        for keyword, risk in RISKY_OPERATION_KEYWORDS.items():
            if keyword in lowered:
                return risk
        return None

    def _explicit_risk(self, request: ToolRequest) -> str | None:
        for attrs in (request.request_attrs, request.input_attrs):
            value = attrs.get("risk_level")
            if value:
                return str(value)
        return None


def _stricter(*levels: str | None) -> str:
    known = [level if level in RISK_ORDER else "unknown" for level in levels if level]
    if not known:
        return "unknown"
    return max(known, key=lambda level: RISK_ORDER[level])
