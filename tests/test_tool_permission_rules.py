from chanta_core.tools.permission_rules import ToolPermissionRule, ToolPermissionRuleSet
from chanta_core.tools.request import ToolRequest
from chanta_core.tools.risk import ToolOperationRisk
from chanta_core.tools.tool import Tool


def tool() -> Tool:
    return Tool("tool:test", "test", "Test", "custom", "readonly", ["run"])


def request() -> ToolRequest:
    return ToolRequest.create(
        tool_id="tool:test",
        operation="run",
        process_instance_id="process_instance:rules",
        session_id="session-rules",
        agent_id="agent-rules",
    )


def risk(level: str) -> ToolOperationRisk:
    return ToolOperationRisk("tool:test", "run", level, "test")


def test_deny_rule_wins_over_allow() -> None:
    rules = ToolPermissionRuleSet(
        [
            ToolPermissionRule("allow-test", "allow", risk_level="readonly"),
            ToolPermissionRule("deny-test", "deny", risk_level="readonly"),
        ]
    )

    decision = rules.evaluate(tool(), request(), risk("readonly"))

    assert decision.decision == "deny"
    assert decision.allowed is False


def test_approval_required_wins_over_allow() -> None:
    rules = ToolPermissionRuleSet(
        [
            ToolPermissionRule("allow-test", "allow", risk_level="write"),
            ToolPermissionRule("approval-test", "approval_required", risk_level="write"),
        ]
    )

    decision = rules.evaluate(tool(), request(), risk("write"))

    assert decision.decision == "approval_required"
    assert decision.requires_approval is True


def test_default_rules_allow_safe_and_deny_unsafe() -> None:
    rules = ToolPermissionRuleSet.default()

    assert rules.evaluate(tool(), request(), risk("readonly")).allowed is True
    assert rules.evaluate(tool(), request(), risk("internal_readonly")).allowed is True
    assert rules.evaluate(tool(), request(), risk("shell")).decision == "deny"
    assert rules.evaluate(tool(), request(), risk("network")).decision == "deny"
    assert rules.evaluate(tool(), request(), risk("dangerous")).decision == "deny"
    assert rules.evaluate(tool(), request(), risk("write")).decision == "approval_required"
