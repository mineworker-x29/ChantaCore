import pytest

from chanta_core.tools.errors import ToolRegistryError
from chanta_core.tools.registry import ToolRegistry
from chanta_core.tools.tool import Tool


def test_builtin_tools_registered() -> None:
    registry = ToolRegistry()

    assert [tool.tool_id for tool in registry.list_tools()] == [
        "tool:echo",
        "tool:ocel",
        "tool:ocpx",
        "tool:pig",
        "tool:workspace",
    ]
    assert registry.get("tool:ocel").tool_name == "ocel"
    assert registry.get("ocpx").tool_id == "tool:ocpx"


def test_duplicate_identical_registration_idempotent() -> None:
    registry = ToolRegistry(include_builtins=False)
    tool = Tool(
        tool_id="tool:test",
        tool_name="test",
        description="Test",
        tool_kind="builtin",
        safety_level="readonly",
        supported_operations=["echo"],
    )

    registry.register(tool)
    registry.register(tool)

    assert len(registry.list_tools()) == 1


def test_duplicate_conflicting_id_raises() -> None:
    registry = ToolRegistry(include_builtins=False)
    registry.register(
        Tool("tool:test", "test", "Test", "builtin", "readonly", ["echo"])
    )

    with pytest.raises(ToolRegistryError):
        registry.register(
            Tool("tool:test", "test2", "Other", "builtin", "readonly", ["echo"])
        )


def test_duplicate_name_with_different_id_raises() -> None:
    registry = ToolRegistry(include_builtins=False)
    registry.register(
        Tool("tool:test", "test", "Test", "builtin", "readonly", ["echo"])
    )

    with pytest.raises(ToolRegistryError):
        registry.register(
            Tool("tool:other", "test", "Other", "builtin", "readonly", ["echo"])
        )
