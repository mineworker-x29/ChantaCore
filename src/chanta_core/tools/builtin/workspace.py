from __future__ import annotations

from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.request import ToolRequest
from chanta_core.tools.result import ToolResult
from chanta_core.tools.tool import Tool
from chanta_core.workspace.inspector import WorkspaceInspector


def create_workspace_tool() -> Tool:
    return Tool(
        tool_id="tool:workspace",
        tool_name="workspace",
        description="Read-only workspace inspection gateway.",
        tool_kind="internal",
        safety_level="internal_readonly",
        supported_operations=[
            "get_workspace_root",
            "path_exists",
            "list_files",
            "read_text_file",
            "summarize_tree",
        ],
        input_schema={},
        output_schema={},
        tool_attrs={
            "is_builtin": True,
            "read_only": True,
            "requires_external_tool": False,
            "allows_write": False,
            "allows_shell": False,
            "allows_network": False,
        },
    )


def execute_workspace_tool(
    *,
    tool: Tool,
    request: ToolRequest,
    context: ToolExecutionContext,
    workspace_inspector: WorkspaceInspector | None = None,
    **_,
) -> ToolResult:
    inspector = workspace_inspector or WorkspaceInspector()
    operation = request.operation
    try:
        if operation == "get_workspace_root":
            output_attrs = inspector.get_workspace_root()
            return _success(
                tool,
                request,
                output_text=f"Workspace root: {output_attrs['workspace_root_name']}",
                output_attrs=output_attrs,
            )
        if operation == "path_exists":
            output_attrs = inspector.path_exists(str(request.input_attrs.get("path", ".")))
            return _success(
                tool,
                request,
                output_text=f"Path exists: {output_attrs['path']} = {output_attrs['exists']}",
                output_attrs=output_attrs,
            )
        if operation == "list_files":
            output_attrs = inspector.list_files(
                str(request.input_attrs.get("path", ".")),
                recursive=bool(request.input_attrs.get("recursive", False)),
                limit=_optional_int(request.input_attrs.get("limit")),
            )
            return _success(
                tool,
                request,
                output_text=f"Workspace list: {output_attrs['entry_count']} entries",
                output_attrs=output_attrs,
            )
        if operation == "read_text_file":
            output_attrs = inspector.read_text_file(str(request.input_attrs.get("path", "")))
            return _success(
                tool,
                request,
                output_text=(
                    f"Read text file: {output_attrs['path']} "
                    f"({output_attrs['size_bytes']} bytes)"
                ),
                output_attrs=output_attrs,
            )
        if operation == "summarize_tree":
            output_attrs = inspector.summarize_tree(
                str(request.input_attrs.get("path", ".")),
                max_depth=int(request.input_attrs.get("max_depth", 2)),
                limit=_optional_int(request.input_attrs.get("limit")),
            )
            return _success(
                tool,
                request,
                output_text=(
                    "Workspace tree: "
                    f"{output_attrs['file_count']} files, "
                    f"{output_attrs['directory_count']} directories"
                ),
                output_attrs=output_attrs,
            )
    except Exception as error:
        return ToolResult.create(
            tool_request_id=request.tool_request_id,
            tool_id=tool.tool_id,
            operation=request.operation,
            success=False,
            output_text=None,
            output_attrs={
                "exception_type": type(error).__name__,
                "failure_stage": "workspace_tool",
            },
            error=str(error),
        )

    return ToolResult.create(
        tool_request_id=request.tool_request_id,
        tool_id=tool.tool_id,
        operation=request.operation,
        success=False,
        output_text=None,
        output_attrs={
            "exception_type": "ToolDispatchError",
            "failure_stage": "workspace_tool",
        },
        error=f"Unsupported tool:workspace operation: {operation}",
    )


def _success(
    tool: Tool,
    request: ToolRequest,
    *,
    output_text: str,
    output_attrs: dict,
) -> ToolResult:
    return ToolResult.create(
        tool_request_id=request.tool_request_id,
        tool_id=tool.tool_id,
        operation=request.operation,
        success=True,
        output_text=output_text,
        output_attrs={**output_attrs, "read_only": True},
    )


def _optional_int(value) -> int | None:
    if value is None:
        return None
    return int(value)
