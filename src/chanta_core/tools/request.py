from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


def new_tool_request_id() -> str:
    return f"tool_request:{uuid4()}"


@dataclass(frozen=True)
class ToolRequest:
    tool_request_id: str
    tool_id: str
    operation: str
    process_instance_id: str
    session_id: str
    agent_id: str
    input_attrs: dict[str, Any] = field(default_factory=dict)
    request_attrs: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        tool_id: str,
        operation: str,
        process_instance_id: str,
        session_id: str,
        agent_id: str,
        input_attrs: dict[str, Any] | None = None,
        request_attrs: dict[str, Any] | None = None,
    ) -> "ToolRequest":
        return cls(
            tool_request_id=new_tool_request_id(),
            tool_id=tool_id,
            operation=operation,
            process_instance_id=process_instance_id,
            session_id=session_id,
            agent_id=agent_id,
            input_attrs=input_attrs or {},
            request_attrs=request_attrs or {},
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "tool_request_id": self.tool_request_id,
            "tool_id": self.tool_id,
            "operation": self.operation,
            "process_instance_id": self.process_instance_id,
            "session_id": self.session_id,
            "agent_id": self.agent_id,
            "input_attrs": self.input_attrs,
            "request_attrs": self.request_attrs,
        }
