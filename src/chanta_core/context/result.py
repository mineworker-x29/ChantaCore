from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.context.block import ContextBlock


@dataclass(frozen=True)
class ContextCompactionLayerResult:
    layer_name: str
    blocks: list[ContextBlock]
    changed: bool
    truncated_block_ids: list[str] = field(default_factory=list)
    dropped_block_ids: list[str] = field(default_factory=list)
    created_block_ids: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "layer_name": self.layer_name,
            "blocks": [block.to_dict() for block in self.blocks],
            "changed": self.changed,
            "truncated_block_ids": self.truncated_block_ids,
            "dropped_block_ids": self.dropped_block_ids,
            "created_block_ids": self.created_block_ids,
            "warnings": self.warnings,
            "result_attrs": self.result_attrs,
        }


@dataclass(frozen=True)
class ContextCompactionResult:
    blocks: list[ContextBlock]
    layer_results: list[ContextCompactionLayerResult]
    total_chars: int
    total_estimated_tokens: int
    truncated_block_ids: list[str] = field(default_factory=list)
    dropped_block_ids: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "blocks": [block.to_dict() for block in self.blocks],
            "layer_results": [result.to_dict() for result in self.layer_results],
            "total_chars": self.total_chars,
            "total_estimated_tokens": self.total_estimated_tokens,
            "truncated_block_ids": self.truncated_block_ids,
            "dropped_block_ids": self.dropped_block_ids,
            "warnings": self.warnings,
            "result_attrs": self.result_attrs,
        }
