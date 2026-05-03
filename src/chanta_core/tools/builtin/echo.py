from __future__ import annotations

from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.request import ToolRequest
from chanta_core.tools.result import ToolResult
from chanta_core.tools.tool import Tool


def create_echo_tool() -> Tool:
    return Tool(
        tool_id="tool:echo",
        tool_name="echo",
        description="Return input text as-is.",
        tool_kind="builtin",
        safety_level="readonly",
        supported_operations=["echo"],
        input_schema={},
        output_schema={},
        tool_attrs={"is_builtin": True, "requires_llm": False},
    )


def execute_echo_tool(
    *,
    tool: Tool,
    request: ToolRequest,
    context: ToolExecutionContext,
    **_,
) -> ToolResult:
    text = str(request.input_attrs.get("text") or "")
    return ToolResult.create(
        tool_request_id=request.tool_request_id,
        tool_id=tool.tool_id,
        operation=request.operation,
        success=True,
        output_text=text,
        output_attrs={
            "echoed": True,
            "response_length": len(text),
            "process_instance_id": context.process_instance_id,
        },
    )
