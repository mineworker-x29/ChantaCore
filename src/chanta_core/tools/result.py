from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


def new_tool_result_id() -> str:
    return f"tool_result:{uuid4()}"


@dataclass(frozen=True)
class ToolResult:
    tool_result_id: str
    tool_request_id: str
    tool_id: str
    operation: str
    success: bool
    output_text: str | None
    output_attrs: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    @classmethod
    def create(
        cls,
        *,
        tool_request_id: str,
        tool_id: str,
        operation: str,
        success: bool,
        output_text: str | None = None,
        output_attrs: dict[str, Any] | None = None,
        error: str | None = None,
    ) -> "ToolResult":
        return cls(
            tool_result_id=new_tool_result_id(),
            tool_request_id=tool_request_id,
            tool_id=tool_id,
            operation=operation,
            success=success,
            output_text=output_text,
            output_attrs=output_attrs or {},
            error=error,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "tool_result_id": self.tool_result_id,
            "tool_request_id": self.tool_request_id,
            "tool_id": self.tool_id,
            "operation": self.operation,
            "success": self.success,
            "output_text": self.output_text,
            "output_attrs": self.output_attrs,
            "error": self.error,
        }
