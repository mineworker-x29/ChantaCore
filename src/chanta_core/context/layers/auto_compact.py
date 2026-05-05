from __future__ import annotations

from chanta_core.context.block import ContextBlock
from chanta_core.context.budget import ContextBudget
from chanta_core.context.result import ContextCompactionLayerResult


class AutoCompactLayer:
    name = "AutoCompactLayer"

    def __init__(self, *, enabled: bool = False) -> None:
        self.enabled = enabled

    def apply(
        self,
        blocks: list[ContextBlock],
        budget: ContextBudget,
    ) -> ContextCompactionLayerResult:
        if not self.enabled:
            return ContextCompactionLayerResult(
                layer_name=self.name,
                blocks=list(blocks),
                changed=False,
                result_attrs={"disabled": True},
            )
        return ContextCompactionLayerResult(
            layer_name=self.name,
            blocks=list(blocks),
            changed=False,
            warnings=["LLM-based auto-compact is not implemented in v0.9.0"],
            result_attrs={"disabled": False, "implemented": False},
        )
