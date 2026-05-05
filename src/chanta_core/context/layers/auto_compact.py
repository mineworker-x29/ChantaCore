from __future__ import annotations

from typing import Any

from chanta_core.context.auto_compact import (
    AutoCompactPolicy,
    AutoCompactRequest,
    AutoCompactSummarizer,
    new_auto_compact_request_id,
)
from chanta_core.context.block import ContextBlock
from chanta_core.context.budget import ContextBudget
from chanta_core.context.result import ContextCompactionLayerResult


class AutoCompactLayer:
    name = "AutoCompactLayer"

    def __init__(
        self,
        *,
        policy: AutoCompactPolicy | None = None,
        summarizer: AutoCompactSummarizer | None = None,
        enabled: bool | None = None,
    ) -> None:
        if policy is None:
            policy = AutoCompactPolicy(
                enabled=False if enabled is None else enabled,
            )
        self.policy = policy
        self.summarizer = summarizer

    def apply(
        self,
        blocks: list[ContextBlock],
        budget: ContextBudget,
    ) -> ContextCompactionLayerResult:
        self.policy.validate()
        if not self.policy.enabled:
            return ContextCompactionLayerResult(
                layer_name=self.name,
                blocks=list(blocks),
                changed=False,
                result_attrs={
                    "disabled": True,
                    "policy": self.policy.to_dict(),
                    "used_summarizer": False,
                },
            )

        if not self.policy.allow_llm_summarizer:
            return ContextCompactionLayerResult(
                layer_name=self.name,
                blocks=list(blocks),
                changed=False,
                warnings=["AutoCompact enabled but LLM summarizer is not allowed."],
                result_attrs={
                    "disabled": False,
                    "blocked": True,
                    "block_reason": "llm_summarizer_not_allowed",
                    "policy": self.policy.to_dict(),
                    "used_summarizer": False,
                },
            )

        if self.summarizer is None:
            return ContextCompactionLayerResult(
                layer_name=self.name,
                blocks=list(blocks),
                changed=False,
                warnings=["AutoCompact enabled but no summarizer was provided."],
                result_attrs={
                    "disabled": False,
                    "blocked": True,
                    "block_reason": "missing_summarizer",
                    "policy": self.policy.to_dict(),
                    "used_summarizer": False,
                },
            )

        input_text = "\n\n".join(block.content for block in blocks)
        if len(input_text) > self.policy.max_input_chars:
            return ContextCompactionLayerResult(
                layer_name=self.name,
                blocks=list(blocks),
                changed=False,
                warnings=["AutoCompact input exceeds max_input_chars."],
                result_attrs={
                    "disabled": False,
                    "blocked": True,
                    "block_reason": "input_too_large",
                    "input_chars": len(input_text),
                    "policy": self.policy.to_dict(),
                    "used_summarizer": False,
                },
            )

        request = self._build_request(blocks, input_text)
        result = self.summarizer.summarize(request, self.policy)
        warnings = list(result.warnings)
        if not result.success or result.output_block is None:
            return ContextCompactionLayerResult(
                layer_name=self.name,
                blocks=list(blocks),
                changed=False,
                warnings=warnings,
                result_attrs={
                    "disabled": False,
                    "blocked": False,
                    "request_id": request.request_id,
                    "policy": self.policy.to_dict(),
                    "used_summarizer": result.used_summarizer,
                    "auto_compact_success": False,
                    "error": result.error,
                    "auto_compact_result": result.to_dict(),
                },
            )

        output_block = result.output_block
        if output_block.char_length > self.policy.max_output_chars:
            warnings.append("AutoCompact output exceeds max_output_chars.")
            return ContextCompactionLayerResult(
                layer_name=self.name,
                blocks=list(blocks),
                changed=False,
                warnings=warnings,
                result_attrs={
                    "disabled": False,
                    "blocked": True,
                    "block_reason": "output_too_large",
                    "request_id": request.request_id,
                    "policy": self.policy.to_dict(),
                    "used_summarizer": result.used_summarizer,
                },
            )
        if self.policy.preserve_refs and not output_block.refs:
            warnings.append("AutoCompact output did not preserve references.")
            return ContextCompactionLayerResult(
                layer_name=self.name,
                blocks=list(blocks),
                changed=False,
                warnings=warnings,
                result_attrs={
                    "disabled": False,
                    "blocked": True,
                    "block_reason": "refs_not_preserved",
                    "request_id": request.request_id,
                    "policy": self.policy.to_dict(),
                    "used_summarizer": result.used_summarizer,
                },
            )

        return ContextCompactionLayerResult(
            layer_name=self.name,
            blocks=[output_block],
            changed=True,
            created_block_ids=[output_block.block_id],
            warnings=warnings,
            result_attrs={
                "disabled": False,
                "blocked": False,
                "request_id": request.request_id,
                "policy": self.policy.to_dict(),
                "used_summarizer": result.used_summarizer,
                "auto_compact_success": True,
                "auto_compact_result": result.to_dict(),
            },
        )

    def _build_request(
        self,
        blocks: list[ContextBlock],
        input_text: str,
    ) -> AutoCompactRequest:
        refs: list[dict[str, Any]] = []
        for block in blocks:
            refs.extend(block.refs)
            refs.append(
                {
                    "ref_type": "context_block",
                    "block_id": block.block_id,
                    "block_type": block.block_type,
                    "title": block.title,
                    "source": block.source,
                }
            )
        return AutoCompactRequest(
            request_id=new_auto_compact_request_id(),
            blocks=list(blocks),
            input_text=input_text,
            refs=refs,
            reason="deterministic_layers_insufficient",
            request_attrs={"block_count": len(blocks), "input_chars": len(input_text)},
        )
