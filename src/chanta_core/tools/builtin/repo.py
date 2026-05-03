from __future__ import annotations

from chanta_core.repo import RepoScanner, RepoSearchService, RepoSymbolScanner
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.request import ToolRequest
from chanta_core.tools.result import ToolResult
from chanta_core.tools.tool import Tool
from chanta_core.workspace import WorkspaceInspector


def create_repo_tool() -> Tool:
    return Tool(
        tool_id="tool:repo",
        tool_name="repo",
        description="Read-only repository search and lightweight symbol scan gateway.",
        tool_kind="internal",
        safety_level="internal_readonly",
        supported_operations=[
            "find_files",
            "search_text",
            "scan_symbols",
            "find_definitions_light",
            "scan_tree",
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
            "parser": "lightweight_regex",
        },
    )


def execute_repo_tool(
    *,
    tool: Tool,
    request: ToolRequest,
    context: ToolExecutionContext,
    repo_search_service: RepoSearchService | None = None,
    repo_symbol_scanner: RepoSymbolScanner | None = None,
    repo_scanner: RepoScanner | None = None,
    workspace_inspector: WorkspaceInspector | None = None,
    **_,
) -> ToolResult:
    inspector = workspace_inspector or WorkspaceInspector()
    scanner = repo_scanner or RepoScanner(inspector)
    search_service = repo_search_service or RepoSearchService(inspector, scanner=scanner)
    symbol_scanner = repo_symbol_scanner or RepoSymbolScanner(inspector, scanner=scanner)
    operation = request.operation
    try:
        if operation == "find_files":
            result = search_service.find_files(
                str(request.input_attrs.get("name_pattern") or "*"),
                limit=int(request.input_attrs.get("limit", 100)),
            )
            return _success(
                tool,
                request,
                output_text=f"Repo files matched: {len(result.file_matches)}",
                output_attrs={"search_result": result.to_dict()},
            )
        if operation == "search_text":
            result = search_service.search_text(
                str(request.input_attrs.get("query") or ""),
                path=str(request.input_attrs.get("path") or "."),
                limit=int(request.input_attrs.get("limit", 100)),
                case_sensitive=bool(request.input_attrs.get("case_sensitive", False)),
            )
            return _success(
                tool,
                request,
                output_text=f"Repo text matches: {len(result.matches)}",
                output_attrs={"search_result": result.to_dict()},
            )
        if operation == "scan_symbols":
            symbols = symbol_scanner.scan_symbols(
                path=str(request.input_attrs.get("path") or "."),
                limit=int(request.input_attrs.get("limit", 200)),
            )
            return _success(
                tool,
                request,
                output_text=f"Repo symbols found: {len(symbols)}",
                output_attrs={"symbols": [item.to_dict() for item in symbols]},
            )
        if operation == "find_definitions_light":
            symbols = symbol_scanner.find_definitions_light(
                name=str(request.input_attrs.get("name") or ""),
                path=str(request.input_attrs.get("path") or "."),
                limit=int(request.input_attrs.get("limit", 100)),
            )
            return _success(
                tool,
                request,
                output_text=f"Definition candidates found: {len(symbols)}",
                output_attrs={"symbols": [item.to_dict() for item in symbols]},
            )
        if operation == "scan_tree":
            tree = scanner.scan_tree(limit=int(request.input_attrs.get("limit", 500)))
            return _success(
                tool,
                request,
                output_text=(
                    "Repo tree: "
                    f"{tree.get('file_count', 0)} files, "
                    f"{tree.get('directory_count', 0)} directories"
                ),
                output_attrs={"tree": tree},
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
                "failure_stage": "repo_tool",
                "operation": operation,
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
            "failure_stage": "repo_tool",
            "operation": operation,
        },
        error=f"Unsupported tool:repo operation: {operation}",
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
