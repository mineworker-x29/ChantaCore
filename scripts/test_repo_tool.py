from __future__ import annotations

from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest


def dispatch(dispatcher: ToolDispatcher, operation: str, **input_attrs):
    context = ToolExecutionContext(
        process_instance_id="process_instance:script-repo-tool",
        session_id="script-repo-tool",
        agent_id="chanta_core_default",
    )
    return dispatcher.dispatch(
        ToolRequest.create(
            tool_id="tool:repo",
            operation=operation,
            process_instance_id=context.process_instance_id,
            session_id=context.session_id,
            agent_id=context.agent_id,
            input_attrs=input_attrs,
        ),
        context,
    )


def main() -> None:
    dispatcher = ToolDispatcher()
    commands = [
        ("find_files", {"name_pattern": "*.py", "limit": 10}),
        ("search_text", {"query": "class", "limit": 10}),
        ("scan_symbols", {"limit": 10}),
    ]
    for operation, attrs in commands:
        result = dispatch(dispatcher, operation, **attrs)
        print(f"{operation}: success={result.success} text={result.output_text}")


if __name__ == "__main__":
    main()
