from __future__ import annotations

from chanta_core.tools.builtin import (
    create_edit_tool,
    create_echo_tool,
    create_ocel_tool,
    create_ocpx_tool,
    create_pig_tool,
    create_repo_tool,
    create_worker_tool,
    create_workspace_tool,
)
from chanta_core.tools.errors import ToolRegistryError
from chanta_core.tools.tool import Tool


class ToolRegistry:
    def __init__(self, *, include_builtins: bool = True) -> None:
        self._tools_by_id: dict[str, Tool] = {}
        self._ids_by_name: dict[str, str] = {}
        if include_builtins:
            self.register_builtin_tools()

    def register(self, tool: Tool) -> None:
        tool.validate()
        existing = self._tools_by_id.get(tool.tool_id)
        if existing is not None:
            if existing == tool:
                return
            raise ToolRegistryError(
                f"Tool already registered with different definition: {tool.tool_id}"
            )
        existing_id_for_name = self._ids_by_name.get(tool.tool_name)
        if existing_id_for_name is not None and existing_id_for_name != tool.tool_id:
            raise ToolRegistryError(
                f"Tool name already registered for another tool_id: {tool.tool_name}"
            )
        self._tools_by_id[tool.tool_id] = tool
        self._ids_by_name[tool.tool_name] = tool.tool_id

    def get(self, tool_id_or_name: str) -> Tool | None:
        if tool_id_or_name in self._tools_by_id:
            return self._tools_by_id[tool_id_or_name]
        tool_id = self._ids_by_name.get(tool_id_or_name)
        if tool_id is None:
            return None
        return self._tools_by_id.get(tool_id)

    def require(self, tool_id_or_name: str) -> Tool:
        tool = self.get(tool_id_or_name)
        if tool is None:
            raise ToolRegistryError(f"Tool is not registered: {tool_id_or_name}")
        return tool

    def list_tools(self) -> list[Tool]:
        return [self._tools_by_id[tool_id] for tool_id in sorted(self._tools_by_id)]

    def register_builtin_tools(self) -> None:
        self.register(create_edit_tool())
        self.register(create_echo_tool())
        self.register(create_ocel_tool())
        self.register(create_ocpx_tool())
        self.register(create_pig_tool())
        self.register(create_repo_tool())
        self.register(create_worker_tool())
        self.register(create_workspace_tool())
