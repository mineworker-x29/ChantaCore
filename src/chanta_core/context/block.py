from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.context.errors import ContextBlockValidationError


BLOCK_TYPES = {
    "system",
    "user_request",
    "pig_context",
    "pig_report",
    "tool_result",
    "conformance",
    "decision",
    "memory",
    "artifact",
    "workspace",
    "repo",
    "worker",
    "scheduler",
    "edit",
    "patch",
    "other",
}


@dataclass(frozen=True)
class ContextBlock:
    block_id: str
    block_type: str
    title: str
    content: str
    priority: int
    source: str
    token_estimate: int
    char_length: int
    was_truncated: bool = False
    refs: list[dict[str, Any]] = field(default_factory=list)
    block_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "block_id": self.block_id,
            "block_type": self.block_type,
            "title": self.title,
            "content": self.content,
            "priority": self.priority,
            "source": self.source,
            "token_estimate": self.token_estimate,
            "char_length": self.char_length,
            "was_truncated": self.was_truncated,
            "refs": self.refs,
            "block_attrs": self.block_attrs,
        }


def new_context_block_id() -> str:
    return f"context_block:{uuid4()}"


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def make_context_block(
    *,
    block_type: str,
    title: str,
    content: str,
    priority: int,
    source: str,
    block_id: str | None = None,
    was_truncated: bool = False,
    refs: list[dict[str, Any]] | None = None,
    block_attrs: dict[str, Any] | None = None,
) -> ContextBlock:
    if not block_type:
        raise ContextBlockValidationError("block_type must not be empty")
    if block_type not in BLOCK_TYPES:
        raise ContextBlockValidationError(f"unsupported block_type: {block_type}")
    if not title:
        raise ContextBlockValidationError("title must not be empty")
    if not isinstance(content, str):
        raise ContextBlockValidationError("content must be a string")
    if not isinstance(priority, int):
        raise ContextBlockValidationError("priority must be an int")
    return ContextBlock(
        block_id=block_id or new_context_block_id(),
        block_type=block_type,
        title=title,
        content=content,
        priority=priority,
        source=source,
        token_estimate=estimate_tokens(content),
        char_length=len(content),
        was_truncated=was_truncated,
        refs=list(refs or []),
        block_attrs=dict(block_attrs or {}),
    )


def replace_context_block_content(
    block: ContextBlock,
    content: str,
    *,
    was_truncated: bool | None = None,
    block_attrs: dict[str, Any] | None = None,
) -> ContextBlock:
    attrs = dict(block.block_attrs)
    if block_attrs:
        attrs.update(block_attrs)
    return make_context_block(
        block_id=block.block_id,
        block_type=block.block_type,
        title=block.title,
        content=content,
        priority=block.priority,
        source=block.source,
        was_truncated=block.was_truncated if was_truncated is None else was_truncated,
        refs=block.refs,
        block_attrs=attrs,
    )


def truncate_text(text: str, max_chars: int, marker: str) -> tuple[str, bool]:
    if len(text) <= max_chars:
        return text, False
    if max_chars <= 0:
        return "", True
    if len(marker) >= max_chars:
        return marker[:max_chars], True
    return f"{text[: max_chars - len(marker)]}{marker}", True


def _compact_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def from_pig_context(pig_context: Any, priority: int = 70) -> ContextBlock:
    refs: list[dict[str, Any]] = [
        {
            "ref_type": "pig_context",
            "source": getattr(pig_context, "source", None),
            "scope": getattr(pig_context, "scope", None),
            "process_instance_id": getattr(pig_context, "process_instance_id", None),
            "session_id": getattr(pig_context, "session_id", None),
        }
    ]
    pi_artifacts = getattr(pig_context, "pi_artifacts", None) or []
    return make_context_block(
        block_type="pig_context",
        title="Process Intelligence Context",
        content=getattr(pig_context, "context_text", "") or "",
        priority=priority,
        source="pig",
        refs=refs,
        block_attrs={
            "activity_count": len(getattr(pig_context, "activity_sequence", None) or []),
            "diagnostic_count": len(getattr(pig_context, "diagnostics", None) or []),
            "recommendation_count": len(
                getattr(pig_context, "recommendations", None) or []
            ),
            "has_conformance_report": getattr(
                pig_context, "conformance_report", None
            )
            is not None,
            "pi_artifact_count": len(pi_artifacts),
        },
    )


def from_tool_result(tool_result: Any, priority: int = 40) -> ContextBlock:
    output_text = getattr(tool_result, "output_text", None)
    output_attrs = getattr(tool_result, "output_attrs", None) or {}
    content = output_text if output_text is not None else _compact_json(output_attrs)
    if getattr(tool_result, "error", None):
        content = f"{content}\nError: {getattr(tool_result, 'error')}" if content else str(
            getattr(tool_result, "error")
        )
    return make_context_block(
        block_type="tool_result",
        title=(
            f"Tool Result: {getattr(tool_result, 'tool_id', 'unknown')} / "
            f"{getattr(tool_result, 'operation', 'unknown')}"
        ),
        content=content,
        priority=priority,
        source="tool",
        refs=[
            {
                "ref_type": "tool_result",
                "tool_result_id": getattr(tool_result, "tool_result_id", None),
                "tool_request_id": getattr(tool_result, "tool_request_id", None),
            }
        ],
        block_attrs={"success": bool(getattr(tool_result, "success", False))},
    )


def from_process_report(report: Any, priority: int = 50) -> ContextBlock:
    return make_context_block(
        block_type="pig_report",
        title="PIG Report",
        content=getattr(report, "report_text", "") or "",
        priority=priority,
        source="pig_report",
        refs=[
            {
                "ref_type": "pig_report",
                "report_id": getattr(report, "report_id", None),
                "process_instance_id": getattr(report, "process_instance_id", None),
                "session_id": getattr(report, "session_id", None),
            }
        ],
        block_attrs={
            "scope": getattr(report, "scope", None),
            "generated_at": getattr(report, "generated_at", None),
        },
    )
