from __future__ import annotations

from pathlib import Path

from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest


def dispatch(dispatcher: ToolDispatcher, operation: str, **input_attrs):
    context = ToolExecutionContext(
        process_instance_id="process_instance:script-workspace-tool",
        session_id="script-workspace-tool",
        agent_id="chanta_core_default",
    )
    return dispatcher.dispatch(
        ToolRequest.create(
            tool_id="tool:workspace",
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
    for operation, attrs in [
        ("get_workspace_root", {}),
        ("summarize_tree", {"path": ".", "max_depth": 1, "limit": 20}),
        ("path_exists", {"path": "README.md"}),
    ]:
        result = dispatch(dispatcher, operation, **attrs)
        print(f"{operation}: success={result.success} text={result.output_text}")
    if Path("README.md").exists():
        result = dispatch(dispatcher, "read_text_file", path="README.md")
        print(
            "read_text_file: "
            f"success={result.success} bytes={result.output_attrs.get('size_bytes')}"
        )


if __name__ == "__main__":
    main()
