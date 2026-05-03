__all__ = [
    "Tool",
    "ToolAuthorization",
    "ToolAuthorizationError",
    "ToolDispatchError",
    "ToolDispatcher",
    "ToolExecutionContext",
    "ToolPolicy",
    "ToolRegistry",
    "ToolRegistryError",
    "ToolRequest",
    "ToolResult",
    "ToolValidationError",
]


def __getattr__(name: str):
    if name == "Tool":
        from chanta_core.tools.tool import Tool

        return Tool
    if name == "ToolAuthorization":
        from chanta_core.tools.policy import ToolAuthorization

        return ToolAuthorization
    if name == "ToolAuthorizationError":
        from chanta_core.tools.errors import ToolAuthorizationError

        return ToolAuthorizationError
    if name == "ToolDispatchError":
        from chanta_core.tools.errors import ToolDispatchError

        return ToolDispatchError
    if name == "ToolDispatcher":
        from chanta_core.tools.dispatcher import ToolDispatcher

        return ToolDispatcher
    if name == "ToolExecutionContext":
        from chanta_core.tools.context import ToolExecutionContext

        return ToolExecutionContext
    if name == "ToolPolicy":
        from chanta_core.tools.policy import ToolPolicy

        return ToolPolicy
    if name == "ToolRegistry":
        from chanta_core.tools.registry import ToolRegistry

        return ToolRegistry
    if name == "ToolRegistryError":
        from chanta_core.tools.errors import ToolRegistryError

        return ToolRegistryError
    if name == "ToolRequest":
        from chanta_core.tools.request import ToolRequest

        return ToolRequest
    if name == "ToolResult":
        from chanta_core.tools.result import ToolResult

        return ToolResult
    if name == "ToolValidationError":
        from chanta_core.tools.errors import ToolValidationError

        return ToolValidationError
    raise AttributeError(name)
