from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.context.errors import ContextBudgetError


STORAGE_MODES = {"metadata_only", "preview", "full"}


@dataclass(frozen=True)
class ContextSnapshotPolicy:
    enabled: bool = False
    storage_mode: str = "preview"
    max_preview_chars: int = 500
    redact_sensitive: bool = True
    include_block_refs: bool = True
    include_compaction_result: bool = True
    policy_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "storage_mode": self.storage_mode,
            "max_preview_chars": self.max_preview_chars,
            "redact_sensitive": self.redact_sensitive,
            "include_block_refs": self.include_block_refs,
            "include_compaction_result": self.include_compaction_result,
            "policy_attrs": self.policy_attrs,
        }

    def validate(self) -> None:
        if not isinstance(self.enabled, bool):
            raise ContextBudgetError("enabled must be a bool")
        if self.storage_mode not in STORAGE_MODES:
            raise ContextBudgetError("storage_mode must be metadata_only, preview, or full")
        if self.max_preview_chars <= 0:
            raise ContextBudgetError("max_preview_chars must be > 0")
        if not isinstance(self.redact_sensitive, bool):
            raise ContextBudgetError("redact_sensitive must be a bool")
