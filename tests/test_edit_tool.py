from chanta_core.editing import EditProposalService, EditProposalStore
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest
from chanta_core.workspace import WorkspaceConfig, WorkspaceInspector


def setup(tmp_path):
    (tmp_path / "app.py").write_text("old\n", encoding="utf-8")
    (tmp_path / ".env").write_text("SECRET=1\n", encoding="utf-8")
    inspector = WorkspaceInspector(WorkspaceConfig(workspace_root=tmp_path))
    store = EditProposalStore(tmp_path / "proposals.jsonl")
    return ToolDispatcher(edit_service=EditProposalService(inspector, store=store))


def context() -> ToolExecutionContext:
    return ToolExecutionContext(
        process_instance_id="process_instance:edit-tool",
        session_id="session-edit-tool",
        agent_id="chanta_core_default",
    )


def request(operation: str, **input_attrs) -> ToolRequest:
    return ToolRequest.create(
        tool_id="tool:edit",
        operation=operation,
        process_instance_id="process_instance:edit-tool",
        session_id="session-edit-tool",
        agent_id="chanta_core_default",
        input_attrs=input_attrs,
    )


def test_propose_text_replacement_tool_result_and_no_mutation(tmp_path) -> None:
    result = setup(tmp_path).dispatch(
        request(
            "propose_text_replacement",
            target_path="app.py",
            proposed_text="new\n",
            title="Replace",
            rationale="Test",
        ),
        context(),
    )

    assert result.success is True
    assert result.output_attrs["proposal_id"].startswith("edit_proposal:")
    assert (tmp_path / "app.py").read_text(encoding="utf-8") == "old\n"


def test_summarize_recent_proposals_and_blocked_path(tmp_path) -> None:
    dispatcher = setup(tmp_path)

    blocked = dispatcher.dispatch(
        request("propose_comment_only", target_path=".env", title="No", rationale="Blocked"),
        context(),
    )
    summary = dispatcher.dispatch(request("summarize_recent_proposals"), context())

    assert blocked.success is False
    assert blocked.output_attrs["failure_stage"] == "edit_tool"
    assert summary.success is True
    assert "summary" in summary.output_attrs


def test_unknown_operation_denied_or_fails(tmp_path) -> None:
    result = setup(tmp_path).dispatch(request("missing"), context())

    assert result.success is False
