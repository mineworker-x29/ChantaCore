from __future__ import annotations

from chanta_core.ocel.store import OCELStore
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest


def dispatch(dispatcher: ToolDispatcher, context: ToolExecutionContext, tool_id: str, operation: str, **input_attrs):
    return dispatcher.dispatch(
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


def main() -> None:
    store = OCELStore()
    dispatcher = ToolDispatcher(ocel_store=store)
    context = ToolExecutionContext(
        process_instance_id="process_instance:script-tool-dispatcher",
        session_id="script-session-tool-dispatcher",
        agent_id="chanta_core_default",
    )

    requests = [
        ("tool:echo", "echo", {"text": "hello tool"}),
        ("tool:ocel", "count_events", {}),
        ("tool:ocpx", "compute_activity_sequence", {"limit": 10}),
        ("tool:pig", "check_self_conformance", {"limit": 10}),
    ]
    for tool_id, operation, attrs in requests:
        result = dispatch(dispatcher, context, tool_id, operation, **attrs)
        print(tool_id, operation, "success:", result.success)
        print("output_text:", result.output_text)
        print("output_keys:", sorted(result.output_attrs.keys()))


if __name__ == "__main__":
    main()
