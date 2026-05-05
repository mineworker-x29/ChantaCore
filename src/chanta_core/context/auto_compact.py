from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol
from uuid import uuid4

from chanta_core.context.block import ContextBlock, make_context_block
from chanta_core.context.errors import ContextBudgetError


def new_auto_compact_request_id() -> str:
    return f"auto_compact_request:{uuid4()}"


@dataclass(frozen=True)
class AutoCompactPolicy:
    enabled: bool = False
    require_explicit_enable: bool = True
    max_input_chars: int = 24000
    max_output_chars: int = 4000
    preserve_refs: bool = True
    allow_llm_summarizer: bool = False
    policy_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "require_explicit_enable": self.require_explicit_enable,
            "max_input_chars": self.max_input_chars,
            "max_output_chars": self.max_output_chars,
            "preserve_refs": self.preserve_refs,
            "allow_llm_summarizer": self.allow_llm_summarizer,
            "policy_attrs": self.policy_attrs,
        }

    def validate(self) -> None:
        if not isinstance(self.enabled, bool):
            raise ContextBudgetError("enabled must be a bool")
        if not isinstance(self.require_explicit_enable, bool):
            raise ContextBudgetError("require_explicit_enable must be a bool")
        if self.max_input_chars <= 0:
            raise ContextBudgetError("max_input_chars must be > 0")
        if self.max_output_chars <= 0:
            raise ContextBudgetError("max_output_chars must be > 0")
        if not isinstance(self.preserve_refs, bool):
            raise ContextBudgetError("preserve_refs must be a bool")
        if not isinstance(self.allow_llm_summarizer, bool):
            raise ContextBudgetError("allow_llm_summarizer must be a bool")


@dataclass(frozen=True)
class AutoCompactRequest:
    request_id: str
    blocks: list[ContextBlock]
    input_text: str
    refs: list[dict[str, Any]]
    reason: str
    request_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "blocks": [block.to_dict() for block in self.blocks],
            "input_text": self.input_text,
            "refs": self.refs,
            "reason": self.reason,
            "request_attrs": self.request_attrs,
        }


@dataclass(frozen=True)
class AutoCompactResult:
    success: bool
    output_block: ContextBlock | None
    output_text: str | None
    used_summarizer: bool
    warnings: list[str] = field(default_factory=list)
    error: str | None = None
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "output_block": (
                self.output_block.to_dict() if self.output_block is not None else None
            ),
            "output_text": self.output_text,
            "used_summarizer": self.used_summarizer,
            "warnings": self.warnings,
            "error": self.error,
            "result_attrs": self.result_attrs,
        }


class AutoCompactSummarizer(Protocol):
    def summarize(
        self,
        request: AutoCompactRequest,
        policy: AutoCompactPolicy,
    ) -> AutoCompactResult:
        ...


class NullAutoCompactSummarizer:
    def summarize(
        self,
        request: AutoCompactRequest,
        policy: AutoCompactPolicy,
    ) -> AutoCompactResult:
        return AutoCompactResult(
            success=False,
            output_block=None,
            output_text=None,
            used_summarizer=False,
            warnings=["No AutoCompact summarizer is configured."],
            error="AutoCompact summarizer unavailable",
            result_attrs={"request_id": request.request_id, "policy": policy.to_dict()},
        )


def make_auto_compact_output_block(
    *,
    content: str,
    refs: list[dict[str, Any]],
    priority: int = 20,
) -> ContextBlock:
    return make_context_block(
        block_type="other",
        title="AutoCompact Output",
        content=content,
        priority=priority,
        source="auto_compact",
        refs=refs,
        block_attrs={"auto_compacted": True},
    )
