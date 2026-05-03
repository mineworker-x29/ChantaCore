from chanta_core.ocel.store import OCELStore
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.policy import ToolPolicy
from chanta_core.tools.registry import ToolRegistry
from chanta_core.tools.request import ToolRequest
from chanta_core.tools.tool import Tool
from chanta_core.traces.trace_service import TraceService


def context() -> ToolExecutionContext:
    return ToolExecutionContext(
        process_instance_id="process_instance:tool-dispatch",
        session_id="session-tool-dispatch",
        agent_id="chanta_core_default",
    )


def request(tool_id: str = "tool:echo", operation: str = "echo") -> ToolRequest:
    return ToolRequest.create(
        tool_id=tool_id,
        operation=operation,
        process_instance_id="process_instance:tool-dispatch",
        session_id="session-tool-dispatch",
        agent_id="chanta_core_default",
        input_attrs={"text": "hello"},
    )


def test_tool_echo_dispatch_succeeds() -> None:
    result = ToolDispatcher().dispatch(request(), context())

    assert result.success is True
    assert result.output_text == "hello"
    assert result.output_attrs["echoed"] is True


def test_unsupported_operation_fails_deterministically() -> None:
    result = ToolDispatcher().dispatch(request(operation="missing"), context())

    assert result.success is False
    assert "Unsupported operation" in result.error


def test_denied_dangerous_tool_returns_failure() -> None:
    registry = ToolRegistry(include_builtins=False)
    registry.register(
        Tool(
            tool_id="tool:danger",
            tool_name="danger",
            description="Danger",
            tool_kind="builtin",
            safety_level="dangerous",
            supported_operations=["run"],
        )
    )

    result = ToolDispatcher(registry=registry, policy=ToolPolicy()).dispatch(
        request(tool_id="tool:danger", operation="run"),
        context(),
    )

    assert result.success is False
    assert "denied" in result.error


def test_tool_lifecycle_events_recorded_to_ocel(tmp_path) -> None:
    store = OCELStore(tmp_path / "tool_lifecycle.sqlite")
    trace_service = TraceService(ocel_store=store)

    result = ToolDispatcher(trace_service=trace_service, ocel_store=store).dispatch(
        request(),
        context(),
    )

    assert result.success is True
    activities = [
        event["event_activity"]
        for event in store.fetch_events_by_session("session-tool-dispatch")
    ]
    assert activities == [
        "create_tool_request",
        "authorize_tool_request",
        "dispatch_tool",
        "execute_tool_operation",
        "complete_tool_operation",
        "observe_tool_result",
    ]
    assert store.fetch_objects_by_type("tool")
    assert store.fetch_objects_by_type("tool_request")
    assert store.fetch_objects_by_type("tool_result")
