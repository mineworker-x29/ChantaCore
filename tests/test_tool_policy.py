from chanta_core.tools.policy import ToolPolicy
from chanta_core.tools.request import ToolRequest
from chanta_core.tools.tool import Tool


def request() -> ToolRequest:
    return ToolRequest.create(
        tool_id="tool:test",
        operation="echo",
        process_instance_id="process_instance:test",
        session_id="session:test",
        agent_id="agent:test",
    )


def tool(level: str) -> Tool:
    return Tool(
        tool_id="tool:test",
        tool_name="test",
        description="Test",
        tool_kind="builtin",
        safety_level=level,
        supported_operations=["echo"],
    )


def test_allowed_safety_levels() -> None:
    policy = ToolPolicy()

    for level in [
        "readonly",
        "internal_readonly",
        "internal_compute",
        "internal_intelligence",
    ]:
        assert policy.authorize(tool(level), request()).allowed is True


def test_denied_safety_levels() -> None:
    policy = ToolPolicy()

    for level in ["write", "network", "shell", "dangerous"]:
        assert policy.authorize(tool(level), request()).allowed is False


def test_write_requires_approval_only_in_approval_required_mode() -> None:
    decision = ToolPolicy(mode="approval_required").authorize(tool("write"), request())

    assert decision.allowed is False
    assert decision.decision == "approval_required"
    assert decision.requires_approval is True


def test_unknown_safety_level_denied() -> None:
    unsafe = tool("readonly")
    object.__setattr__(unsafe, "safety_level", "unknown")

    authorization = ToolPolicy().authorize(unsafe, request())

    assert authorization.allowed is False
    assert authorization.decision == "deny"
