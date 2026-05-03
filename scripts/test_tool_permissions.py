from __future__ import annotations

from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.policy import ToolPolicy
from chanta_core.tools.registry import ToolRegistry
from chanta_core.tools.request import ToolRequest
from chanta_core.tools.tool import Tool


def context() -> ToolExecutionContext:
    return ToolExecutionContext(
        process_instance_id="process_instance:script-permissions",
        session_id="script-permissions",
        agent_id="chanta_core_default",
    )


def request(tool_id: str, operation: str = "run") -> ToolRequest:
    return ToolRequest.create(
        tool_id=tool_id,
        operation=operation,
        process_instance_id="process_instance:script-permissions",
        session_id="script-permissions",
        agent_id="chanta_core_default",
        input_attrs={"text": "hello"},
    )


def registry_for(level: str) -> ToolRegistry:
    registry = ToolRegistry(include_builtins=False)
    registry.register(
        Tool(
            tool_id=f"tool:test_{level}",
            tool_name=f"test_{level}",
            description="Permission fixture",
            tool_kind="test",
            safety_level=level,
            supported_operations=["run"],
        )
    )
    return registry


def main() -> None:
    safe = ToolDispatcher().dispatch(request("tool:echo", "echo"), context())
    print(f"tool:echo -> success={safe.success}, text={safe.output_text}")

    for level in ["write", "shell", "network", "dangerous"]:
        dispatcher = ToolDispatcher(
            registry=registry_for(level),
            policy=ToolPolicy(mode="approval_required"),
        )
        result = dispatcher.dispatch(request(f"tool:test_{level}"), context())
        decision = result.output_attrs.get("authorization_decision") or {}
        print(
            f"tool:test_{level} -> success={result.success}, "
            f"decision={decision.get('decision')}, "
            f"requires_approval={decision.get('requires_approval')}"
        )


if __name__ == "__main__":
    main()
