from __future__ import annotations

from chanta_core.ocel.query import OCELQueryService
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.errors import ToolDispatchError
from chanta_core.tools.request import ToolRequest
from chanta_core.tools.result import ToolResult
from chanta_core.tools.tool import Tool


def create_ocel_tool() -> Tool:
    return Tool(
        tool_id="tool:ocel",
        tool_name="ocel",
        description="Read-only gateway for ChantaCore OCEL persistence.",
        tool_kind="internal",
        safety_level="internal_readonly",
        supported_operations=[
            "query_recent_events",
            "count_events",
            "count_objects",
            "count_relations",
            "validate_relations",
            "object_type_counts",
        ],
        input_schema={},
        output_schema={},
        tool_attrs={"is_builtin": True, "uses_ocel_store": True},
    )


def execute_ocel_tool(
    *,
    tool: Tool,
    request: ToolRequest,
    context: ToolExecutionContext,
    ocel_store: OCELStore | None = None,
    **_,
) -> ToolResult:
    store = ocel_store or OCELStore()
    operation = request.operation
    if operation == "query_recent_events":
        limit = int(request.input_attrs.get("limit", 20))
        recent_events = store.fetch_recent_events(limit=limit)
        return _result(
            tool,
            request,
            output_text=f"OCEL recent events: {len(recent_events)}",
            output_attrs={
                "recent_events": recent_events,
                "event_count": len(recent_events),
                "limit": limit,
            },
        )
    if operation == "count_events":
        event_count = store.fetch_event_count()
        return _result(tool, request, output_attrs={"event_count": event_count})
    if operation == "count_objects":
        object_count = store.fetch_object_count()
        return _result(tool, request, output_attrs={"object_count": object_count})
    if operation == "count_relations":
        event_object_relation_count = store.fetch_event_object_relation_count()
        object_object_relation_count = store.fetch_object_object_relation_count()
        return _result(
            tool,
            request,
            output_attrs={
                "event_object_relation_count": event_object_relation_count,
                "object_object_relation_count": object_object_relation_count,
                "relation_count": event_object_relation_count + object_object_relation_count,
            },
        )
    if operation == "validate_relations":
        validation = OCELValidator(store).validate_duplicate_relations()
        return _result(tool, request, output_attrs={"validation": validation})
    if operation == "object_type_counts":
        counts = OCELQueryService(store).object_type_counts()
        return _result(tool, request, output_attrs={"object_type_counts": counts})
    raise ToolDispatchError(f"Unsupported tool:ocel operation: {operation}")


def _result(
    tool: Tool,
    request: ToolRequest,
    *,
    output_text: str | None = None,
    output_attrs: dict,
) -> ToolResult:
    return ToolResult.create(
        tool_request_id=request.tool_request_id,
        tool_id=tool.tool_id,
        operation=request.operation,
        success=True,
        output_text=output_text,
        output_attrs=output_attrs,
    )
