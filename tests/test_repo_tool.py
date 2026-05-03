from pathlib import Path

from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest
from chanta_core.workspace import WorkspaceConfig, WorkspaceInspector


def make_dispatcher(tmp_path: Path) -> ToolDispatcher:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text("class App:\n    pass\n", encoding="utf-8")
    (tmp_path / ".env").write_text("SECRET=1\n", encoding="utf-8")
    return ToolDispatcher(
        workspace_inspector=WorkspaceInspector(WorkspaceConfig(workspace_root=tmp_path))
    )


def context() -> ToolExecutionContext:
    return ToolExecutionContext(
        process_instance_id="process_instance:repo-tool",
        session_id="session-repo-tool",
        agent_id="chanta_core_default",
    )


def request(operation: str, **input_attrs) -> ToolRequest:
    return ToolRequest.create(
        tool_id="tool:repo",
        operation=operation,
        process_instance_id="process_instance:repo-tool",
        session_id="session-repo-tool",
        agent_id="chanta_core_default",
        input_attrs=input_attrs,
    )


def test_repo_tool_operations(tmp_path) -> None:
    dispatcher = make_dispatcher(tmp_path)

    assert dispatcher.dispatch(request("find_files", name_pattern="*.py"), context()).success
    assert dispatcher.dispatch(request("search_text", query="class"), context()).success
    assert dispatcher.dispatch(request("scan_symbols"), context()).success
    assert dispatcher.dispatch(
        request("find_definitions_light", name="App"),
        context(),
    ).success
    assert dispatcher.dispatch(request("scan_tree"), context()).success


def test_invalid_operation_returns_failure(tmp_path) -> None:
    result = make_dispatcher(tmp_path).dispatch(request("missing"), context())

    assert result.success is False
    assert "Unsupported operation" in result.error


def test_blocked_file_not_searched(tmp_path) -> None:
    result = make_dispatcher(tmp_path).dispatch(
        request("search_text", query="SECRET"),
        context(),
    )

    assert result.success is True
    assert result.output_attrs["search_result"]["matches"] == []
