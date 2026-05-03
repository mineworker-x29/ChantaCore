from pathlib import Path

from chanta_core.tools.builtin.workspace import create_workspace_tool, execute_workspace_tool
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest
from chanta_core.workspace import WorkspaceConfig, WorkspaceInspector


def context() -> ToolExecutionContext:
    return ToolExecutionContext(
        process_instance_id="process_instance:workspace-tool",
        session_id="session-workspace-tool",
        agent_id="chanta_core_default",
    )


def request(operation: str, **input_attrs) -> ToolRequest:
    return ToolRequest.create(
        tool_id="tool:workspace",
        operation=operation,
        process_instance_id="process_instance:workspace-tool",
        session_id="session-workspace-tool",
        agent_id="chanta_core_default",
        input_attrs=input_attrs,
    )


def inspector(tmp_path: Path) -> WorkspaceInspector:
    (tmp_path / "README.md").write_text("hello", encoding="utf-8")
    (tmp_path / ".env").write_text("SECRET=1", encoding="utf-8")
    return WorkspaceInspector(WorkspaceConfig(workspace_root=tmp_path))


def test_execute_workspace_tool_operations(tmp_path) -> None:
    tool = create_workspace_tool()
    workspace_inspector = inspector(tmp_path)

    assert execute_workspace_tool(
        tool=tool,
        request=request("get_workspace_root"),
        context=context(),
        workspace_inspector=workspace_inspector,
    ).success is True
    assert execute_workspace_tool(
        tool=tool,
        request=request("path_exists", path="README.md"),
        context=context(),
        workspace_inspector=workspace_inspector,
    ).output_attrs["exists"] is True
    assert execute_workspace_tool(
        tool=tool,
        request=request("list_files", path="."),
        context=context(),
        workspace_inspector=workspace_inspector,
    ).output_attrs["entry_count"] >= 1
    assert execute_workspace_tool(
        tool=tool,
        request=request("read_text_file", path="README.md"),
        context=context(),
        workspace_inspector=workspace_inspector,
    ).output_attrs["text"] == "hello"
    assert execute_workspace_tool(
        tool=tool,
        request=request("summarize_tree", path="."),
        context=context(),
        workspace_inspector=workspace_inspector,
    ).output_attrs["tree"]


def test_blocked_file_failure_is_tool_result(tmp_path) -> None:
    result = execute_workspace_tool(
        tool=create_workspace_tool(),
        request=request("read_text_file", path=".env"),
        context=context(),
        workspace_inspector=inspector(tmp_path),
    )

    assert result.success is False
    assert result.output_attrs["failure_stage"] == "workspace_tool"
    assert result.output_attrs["exception_type"] == "WorkspaceAccessError"


def test_dispatcher_workspace_tool(tmp_path) -> None:
    result = ToolDispatcher(workspace_inspector=inspector(tmp_path)).dispatch(
        request("read_text_file", path="README.md"),
        context(),
    )

    assert result.success is True
    assert result.tool_id == "tool:workspace"
    assert result.operation == "read_text_file"
