from chanta_core.tools.policy import ToolPolicy
from chanta_core.tools.registry import ToolRegistry
from chanta_core.tools.request import ToolRequest
from chanta_core.tools.tool import Tool


def request(tool_id: str = "tool:echo", operation: str = "echo") -> ToolRequest:
    return ToolRequest.create(
        tool_id=tool_id,
        operation=operation,
        process_instance_id="process_instance:modes",
        session_id="session-modes",
        agent_id="agent-modes",
    )


def fake_tool(level: str) -> Tool:
    return Tool(
        tool_id=f"tool:test_{level}",
        tool_name=f"test_{level}",
        description="Test",
        tool_kind="test",
        safety_level=level,
        supported_operations=["run"],
    )


def test_safe_internal_allows_existing_internal_tools() -> None:
    policy = ToolPolicy(mode="safe_internal")
    registry = ToolRegistry()

    for tool_id in ["tool:echo", "tool:ocel", "tool:ocpx", "tool:pig", "tool:workspace", "tool:repo"]:
        assert policy.authorize(registry.require(tool_id), request(tool_id)).allowed is True


def test_deny_all_denies_even_echo() -> None:
    decision = ToolPolicy(mode="deny_all").authorize(
        ToolRegistry().require("tool:echo"),
        request("tool:echo"),
    )

    assert decision.allowed is False
    assert decision.decision == "deny"


def test_approval_required_mode_returns_state_for_write() -> None:
    decision = ToolPolicy(mode="approval_required").authorize(
        fake_tool("write"),
        request("tool:test_write", "run"),
    )

    assert decision.allowed is False
    assert decision.decision == "approval_required"
    assert decision.requires_approval is True


def test_approval_required_mode_denies_shell_network_dangerous() -> None:
    policy = ToolPolicy(mode="approval_required")

    for level in ["shell", "network", "dangerous"]:
        decision = policy.authorize(fake_tool(level), request(f"tool:test_{level}", "run"))
        assert decision.allowed is False
        assert decision.decision == "deny"


def test_readonly_mode_denies_write() -> None:
    decision = ToolPolicy(mode="readonly").authorize(
        fake_tool("write"),
        request("tool:test_write", "run"),
    )

    assert decision.allowed is False
    assert decision.decision == "deny"
