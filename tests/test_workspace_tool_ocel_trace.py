from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest
from chanta_core.traces.trace_service import TraceService
from chanta_core.workspace import WorkspaceConfig, WorkspaceInspector


def test_workspace_tool_lifecycle_ocel_trace(tmp_path) -> None:
    workspace_root = tmp_path / "workspace"
    workspace_root.mkdir()
    (workspace_root / "README.md").write_text("hello", encoding="utf-8")
    store = OCELStore(tmp_path / "workspace_trace.sqlite")
    trace_service = TraceService(ocel_store=store)
    dispatcher = ToolDispatcher(
        trace_service=trace_service,
        ocel_store=store,
        workspace_inspector=WorkspaceInspector(WorkspaceConfig(workspace_root=workspace_root)),
    )
    context = ToolExecutionContext(
        process_instance_id="process_instance:workspace-trace",
        session_id="session-workspace-trace",
        agent_id="chanta_core_default",
    )

    result = dispatcher.dispatch(
        ToolRequest.create(
            tool_id="tool:workspace",
            operation="read_text_file",
            process_instance_id=context.process_instance_id,
            session_id=context.session_id,
            agent_id=context.agent_id,
            input_attrs={"path": "README.md"},
        ),
        context,
    )

    assert result.success is True
    activities = [
        event["event_activity"]
        for event in store.fetch_events_by_session("session-workspace-trace")
    ]
    assert "execute_tool_operation" in activities
    assert "complete_tool_operation" in activities
    assert "observe_tool_result" in activities
    assert store.fetch_objects_by_type("tool")
    assert store.fetch_objects_by_type("tool_request")
    assert store.fetch_objects_by_type("tool_result")
    assert store.fetch_objects_by_type("workspace")
    assert store.fetch_objects_by_type("file")
    assert OCELValidator(store).validate_duplicate_relations()["valid"] is True
