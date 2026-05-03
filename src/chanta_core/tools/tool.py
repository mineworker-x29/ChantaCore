from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.tools.errors import ToolValidationError


ALLOWED_SAFETY_LEVELS = {
    "readonly",
    "internal_readonly",
    "internal_compute",
    "internal_intelligence",
    "write",
    "network",
    "shell",
    "dangerous",
}


@dataclass(frozen=True)
class Tool:
    tool_id: str
    tool_name: str
    description: str
    tool_kind: str
    safety_level: str
    supported_operations: list[str]
    input_schema: dict[str, Any] = field(default_factory=dict)
    output_schema: dict[str, Any] = field(default_factory=dict)
    tool_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "tool_id": self.tool_id,
            "tool_name": self.tool_name,
            "description": self.description,
            "tool_kind": self.tool_kind,
            "safety_level": self.safety_level,
            "supported_operations": self.supported_operations,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "tool_attrs": self.tool_attrs,
        }

    def validate(self) -> None:
        if not self.tool_id or not self.tool_id.startswith("tool:"):
            raise ToolValidationError("tool_id must start with 'tool:'")
        if not self.tool_name:
            raise ToolValidationError("tool_name must not be empty")
        if not self.tool_kind:
            raise ToolValidationError("tool_kind must not be empty")
        if not self.safety_level:
            raise ToolValidationError("safety_level must not be empty")
        if self.safety_level not in ALLOWED_SAFETY_LEVELS:
            raise ToolValidationError(f"Unknown safety_level: {self.safety_level}")
        if not isinstance(self.supported_operations, list) or not self.supported_operations:
            raise ToolValidationError("supported_operations must be a non-empty list[str]")
        if not all(isinstance(item, str) and item for item in self.supported_operations):
            raise ToolValidationError("supported_operations must contain non-empty strings")
        if not isinstance(self.input_schema, dict):
            raise ToolValidationError("input_schema must be a dict")
        if not isinstance(self.output_schema, dict):
            raise ToolValidationError("output_schema must be a dict")
        if not isinstance(self.tool_attrs, dict):
            raise ToolValidationError("tool_attrs must be a dict")
