from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.policy import ToolPolicy
from chanta_core.tools.registry import ToolRegistry
from chanta_core.tools.request import ToolRequest
from chanta_core.tools.tool import Tool
from chanta_core.traces.trace_service import TraceService


def context() -> ToolExecutionContext:
    return ToolExecutionContext(
        process_instance_id="process_instance:permissions",
        session_id="session-permissions",
        agent_id="chanta_core_default",
    )


def request(tool_id: str, operation: str = "run") -> ToolRequest:
    return ToolRequest.create(
        tool_id=tool_id,
        operation=operation,
        process_instance_id="process_instance:permissions",
        session_id="session-permissions",
        agent_id="chanta_core_default",
        input_attrs={"text": "hello"},
    )


def registry_with_fake_tool(level: str) -> ToolRegistry:
    registry = ToolRegistry(include_builtins=False)
    registry.register(
        Tool(
            tool_id=f"tool:test_{level}",
            tool_name=f"test_{level}",
            description="Test unsafe fixture",
            tool_kind="test",
            safety_level=level,
            supported_operations=["run"],
        )
    )
    return registry


def test_safe_tool_executes() -> None:
    result = ToolDispatcher().dispatch(request("tool:echo", "echo"), context())

    assert result.success is True
    assert result.output_text == "hello"


def test_denied_tool_does_not_execute() -> None:
    result = ToolDispatcher(
        registry=registry_with_fake_tool("shell"),
        policy=ToolPolicy(mode="approval_required"),
    ).dispatch(request("tool:test_shell"), context())

    assert result.success is False
    assert result.output_attrs["authorization_decision"]["decision"] == "deny"
    assert result.output_attrs["risk_level"] == "shell"


def test_approval_required_tool_does_not_execute() -> None:
    result = ToolDispatcher(
        registry=registry_with_fake_tool("write"),
        policy=ToolPolicy(mode="approval_required"),
    ).dispatch(request("tool:test_write"), context())

    assert result.success is False
    assert result.output_attrs["requires_approval"] is True
    assert result.output_attrs["approval_required"] is True
    assert "requires approval" in result.error


def test_authorization_trace_records_and_no_execute_for_denied(tmp_path) -> None:
    store = OCELStore(tmp_path / "tool_permissions.sqlite")
    trace_service = TraceService(ocel_store=store)

    result = ToolDispatcher(
        registry=registry_with_fake_tool("network"),
        policy=ToolPolicy(mode="approval_required"),
        trace_service=trace_service,
        ocel_store=store,
    ).dispatch(request("tool:test_network"), context())

    assert result.success is False
    events = store.fetch_events_by_session("session-permissions")
    activities = [event["event_activity"] for event in events]
    assert "authorize_tool_request" in activities
    assert "execute_tool_operation" not in activities
    assert "complete_tool_operation" not in activities
    authorization_event = next(
        event for event in events if event["event_activity"] == "authorize_tool_request"
    )
    attrs = authorization_event["event_attrs"]
    assert attrs["decision"] == "deny"
    assert attrs["allowed"] is False
    assert attrs["requires_approval"] is False
    assert attrs["risk_level"] == "network"
    assert attrs["permission_mode"] == "approval_required"
    assert attrs["reason"]
    assert OCELValidator(store).validate_duplicate_relations()["valid"] is True
