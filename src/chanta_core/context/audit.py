from __future__ import annotations

from typing import Any

from chanta_core.context.block import ContextBlock, estimate_tokens
from chanta_core.context.budget import ContextBudget
from chanta_core.context.redaction import make_preview, redact_sensitive_text
from chanta_core.context.result import ContextCompactionResult
from chanta_core.context.snapshot import (
    ContextAssemblySnapshot,
    ContextBlockSnapshot,
    ContextMessageSnapshot,
    create_context_assembly_snapshot,
)
from chanta_core.context.snapshot_policy import ContextSnapshotPolicy
from chanta_core.context.snapshot_store import ContextSnapshotStore
from chanta_core.llm.types import ChatMessage


class ContextAuditService:
    def __init__(
        self,
        *,
        snapshot_policy: ContextSnapshotPolicy | None = None,
        snapshot_store: ContextSnapshotStore | None = None,
    ) -> None:
        self.snapshot_policy = snapshot_policy or ContextSnapshotPolicy()
        self.snapshot_store = snapshot_store or ContextSnapshotStore()

    def build_snapshot(
        self,
        *,
        blocks: list[ContextBlock],
        messages: list[ChatMessage],
        compaction_result: ContextCompactionResult | None = None,
        budget: ContextBudget | None = None,
        session_id: str | None = None,
        process_instance_id: str | None = None,
        snapshot_attrs: dict[str, Any] | None = None,
    ) -> ContextAssemblySnapshot:
        policy = self.snapshot_policy
        policy.validate()
        dropped_ids = set(compaction_result.dropped_block_ids if compaction_result else [])
        truncated_ids = set(
            compaction_result.truncated_block_ids if compaction_result else []
        )
        collapsed_ids = self._collapsed_ids(compaction_result)
        block_snapshots = [
            ContextBlockSnapshot(
                block_id=block.block_id,
                block_type=block.block_type,
                title=block.title,
                source=block.source,
                priority=block.priority,
                char_length=block.char_length,
                token_estimate=block.token_estimate,
                was_truncated=block.was_truncated or block.block_id in truncated_ids,
                was_dropped=block.block_id in dropped_ids,
                was_collapsed=block.block_id in collapsed_ids,
                refs=list(block.refs) if policy.include_block_refs else [],
                snapshot_attrs={
                    "ref_count": len(block.refs),
                    "block_attrs_keys": sorted(str(key) for key in block.block_attrs),
                },
            )
            for block in blocks
        ]
        message_snapshots = [
            self._message_snapshot(message, policy) for message in messages
        ]
        return create_context_assembly_snapshot(
            session_id=session_id,
            process_instance_id=process_instance_id,
            storage_mode=policy.storage_mode,
            budget=budget.to_dict() if budget is not None else None,
            block_snapshots=block_snapshots,
            message_snapshots=message_snapshots,
            compaction_result=(
                compaction_result.to_dict()
                if compaction_result is not None and policy.include_compaction_result
                else None
            ),
            warnings=list(compaction_result.warnings) if compaction_result else [],
            snapshot_attrs={
                **dict(snapshot_attrs or {}),
                "policy": policy.to_dict(),
                "block_count": len(blocks),
                "message_count": len(messages),
            },
        )

    def maybe_store_snapshot(
        self,
        *,
        blocks: list[ContextBlock],
        messages: list[ChatMessage],
        compaction_result: ContextCompactionResult | None = None,
        budget: ContextBudget | None = None,
        session_id: str | None = None,
        process_instance_id: str | None = None,
        snapshot_attrs: dict[str, Any] | None = None,
    ) -> ContextAssemblySnapshot | None:
        self.snapshot_policy.validate()
        if not self.snapshot_policy.enabled:
            return None
        snapshot = self.build_snapshot(
            blocks=blocks,
            messages=messages,
            compaction_result=compaction_result,
            budget=budget,
            session_id=session_id,
            process_instance_id=process_instance_id,
            snapshot_attrs=snapshot_attrs,
        )
        self.snapshot_store.append(snapshot)
        return snapshot

    @staticmethod
    def _message_snapshot(
        message: ChatMessage,
        policy: ContextSnapshotPolicy,
    ) -> ContextMessageSnapshot:
        content = message["content"]
        if policy.storage_mode == "metadata_only":
            preview = None
        elif policy.storage_mode == "preview":
            preview = make_preview(
                content,
                policy.max_preview_chars,
                redact=policy.redact_sensitive,
            )
        else:
            preview = (
                redact_sensitive_text(content) if policy.redact_sensitive else content
            )
        return ContextMessageSnapshot(
            role=message["role"],
            content_preview=preview,
            char_length=len(content),
            token_estimate=estimate_tokens(content),
            message_attrs={"storage_mode": policy.storage_mode},
        )

    @staticmethod
    def _collapsed_ids(
        compaction_result: ContextCompactionResult | None,
    ) -> set[str]:
        if compaction_result is None:
            return set()
        result: set[str] = set()
        for layer_result in compaction_result.layer_results:
            if layer_result.layer_name == "ContextCollapseLayer":
                result.update(layer_result.dropped_block_ids)
        return result
