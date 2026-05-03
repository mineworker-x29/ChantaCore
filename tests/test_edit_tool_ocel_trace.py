from chanta_core.editing import EditProposalService, EditProposalStore
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest
from chanta_core.traces.trace_service import TraceService
from chanta_core.workspace import WorkspaceConfig, WorkspaceInspector


def test_edit_tool_lifecycle_trace(tmp_path) -> None:
    workspace_root = tmp_path / "workspace"
    workspace_root.mkdir()
    (workspace_root / "app.py").write_text("old\n", encoding="utf-8")
    store = OCELStore(tmp_path / "edit_trace.sqlite")
    trace_service = TraceService(ocel_store=store)
    inspector = WorkspaceInspector(WorkspaceConfig(workspace_root=workspace_root))
    edit_service = EditProposalService(
        workspace_inspector=inspector,
        store=EditProposalStore(tmp_path / "proposals.jsonl"),
    )
    context = ToolExecutionContext(
        process_instance_id="process_instance:edit-trace",
        session_id="session-edit-trace",
        agent_id="chanta_core_default",
    )

    result = ToolDispatcher(
        trace_service=trace_service,
        ocel_store=store,
        edit_service=edit_service,
    ).dispatch(
        ToolRequest.create(
            tool_id="tool:edit",
            operation="propose_text_replacement",
            process_instance_id=context.process_instance_id,
            session_id=context.session_id,
            agent_id=context.agent_id,
            input_attrs={
                "target_path": "app.py",
                "proposed_text": "new\n",
                "title": "Replace",
                "rationale": "Trace",
            },
        ),
        context,
    )

    assert result.success is True
    assert result.output_attrs["proposal_id"]
    activities = [
        event["event_activity"] for event in store.fetch_events_by_session("session-edit-trace")
    ]
    assert "execute_tool_operation" in activities
    assert "complete_tool_operation" in activities
    assert OCELValidator(store).validate_duplicate_relations()["valid"] is True
