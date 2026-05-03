from __future__ import annotations

from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.ocpx.models import OCPXProcessView
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.errors import ToolDispatchError
from chanta_core.tools.request import ToolRequest
from chanta_core.tools.result import ToolResult
from chanta_core.tools.tool import Tool


def create_ocpx_tool() -> Tool:
    return Tool(
        tool_id="tool:ocpx",
        tool_name="ocpx",
        description="Internal compute gateway for lightweight OCPX process views.",
        tool_kind="internal",
        safety_level="internal_compute",
        supported_operations=[
            "load_recent_view",
            "compute_activity_sequence",
            "compute_variant_summary",
            "compute_relation_coverage",
            "compute_basic_performance",
            "summarize_for_pig_context",
        ],
        input_schema={},
        output_schema={},
        tool_attrs={"is_builtin": True, "uses_ocpx": True},
    )


def execute_ocpx_tool(
    *,
    tool: Tool,
    request: ToolRequest,
    context: ToolExecutionContext,
    ocel_store: OCELStore | None = None,
    ocpx_loader: OCPXLoader | None = None,
    ocpx_engine: OCPXEngine | None = None,
    **_,
) -> ToolResult:
    loader = ocpx_loader or OCPXLoader(store=ocel_store)
    engine = ocpx_engine or OCPXEngine()
    view = _load_view(request, context, loader)
    operation = request.operation
    if operation == "load_recent_view":
        return _result(tool, request, output_attrs={"view": view.to_dict()})
    if operation == "compute_activity_sequence":
        activity_sequence = engine.activity_sequence(view)
        return _result(
            tool,
            request,
            output_attrs={"activity_sequence": activity_sequence},
        )
    if operation == "compute_variant_summary":
        summary = engine.compute_variant_summary(view).to_dict()
        return _result(tool, request, output_attrs={"variant_summary": summary})
    if operation == "compute_relation_coverage":
        coverage = engine.compute_relation_coverage(view)
        return _result(tool, request, output_attrs={"relation_coverage": coverage})
    if operation == "compute_basic_performance":
        performance = engine.compute_basic_performance(view)
        return _result(tool, request, output_attrs={"performance_summary": performance})
    if operation == "summarize_for_pig_context":
        summary = engine.summarize_for_pig_context(view)
        return _result(tool, request, output_attrs={"pig_context_summary": summary})
    raise ToolDispatchError(f"Unsupported tool:ocpx operation: {operation}")


def _load_view(
    request: ToolRequest,
    context: ToolExecutionContext,
    loader: OCPXLoader,
) -> OCPXProcessView:
    scope = str(request.input_attrs.get("scope") or "recent")
    if scope == "process_instance":
        process_instance_id = (
            request.input_attrs.get("process_instance_id")
            or context.process_instance_id
        )
        return loader.load_process_instance_view(str(process_instance_id))
    if scope == "session":
        session_id = request.input_attrs.get("session_id") or context.session_id
        return loader.load_session_view(str(session_id))
    limit = int(request.input_attrs.get("limit", 20))
    return loader.load_recent_view(limit=limit)


def _result(
    tool: Tool,
    request: ToolRequest,
    *,
    output_attrs: dict,
    output_text: str | None = None,
) -> ToolResult:
    return ToolResult.create(
        tool_request_id=request.tool_request_id,
        tool_id=tool.tool_id,
        operation=request.operation,
        success=True,
        output_text=output_text,
        output_attrs=output_attrs,
    )
