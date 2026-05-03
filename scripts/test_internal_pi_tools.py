from __future__ import annotations

from chanta_core.ocel.store import OCELStore
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest


def run_tool(dispatcher: ToolDispatcher, context: ToolExecutionContext, tool_id: str, operation: str, **input_attrs):
    result = dispatcher.dispatch(
        ToolRequest.create(
            tool_id=tool_id,
            operation=operation,
            process_instance_id=context.process_instance_id,
            session_id=context.session_id,
            agent_id=context.agent_id,
            input_attrs=input_attrs,
        ),
        context,
    )
    print(tool_id, operation, "success:", result.success)
    print("output_attrs:", result.output_attrs)


def main() -> None:
    store = OCELStore()
    dispatcher = ToolDispatcher(ocel_store=store)
    context = ToolExecutionContext(
        process_instance_id="process_instance:script-internal-pi-tools",
        session_id="script-session-internal-pi-tools",
        agent_id="chanta_core_default",
    )

    run_tool(dispatcher, context, "tool:ocel", "query_recent_events", limit=5)
    run_tool(dispatcher, context, "tool:ocpx", "compute_activity_sequence", limit=10)
    run_tool(dispatcher, context, "tool:pig", "build_context", limit=10)
    run_tool(dispatcher, context, "tool:pig", "check_self_conformance", limit=10)


if __name__ == "__main__":
    main()
