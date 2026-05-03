import pytest

from chanta_core.tools.errors import ToolValidationError
from chanta_core.tools.tool import Tool


def make_tool(**overrides) -> Tool:
    values = {
        "tool_id": "tool:test",
        "tool_name": "test",
        "description": "Test tool",
        "tool_kind": "builtin",
        "safety_level": "readonly",
        "supported_operations": ["echo"],
        "input_schema": {},
        "output_schema": {},
        "tool_attrs": {},
    }
    values.update(overrides)
    return Tool(**values)


def test_valid_tool_validates() -> None:
    tool = make_tool()

    tool.validate()

    assert tool.to_dict()["tool_id"] == "tool:test"


def test_invalid_tool_id_fails() -> None:
    with pytest.raises(ToolValidationError):
        make_tool(tool_id="bad:test").validate()


def test_empty_operations_fail() -> None:
    with pytest.raises(ToolValidationError):
        make_tool(supported_operations=[]).validate()


def test_unknown_safety_level_fails_validation() -> None:
    with pytest.raises(ToolValidationError):
        make_tool(safety_level="unknown").validate()
