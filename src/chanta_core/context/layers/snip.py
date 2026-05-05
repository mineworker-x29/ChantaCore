from __future__ import annotations

from typing import Any

from chanta_core.context.block import ContextBlock
from chanta_core.context.budget import ContextBudget
from chanta_core.context.layers.base import is_protected, total_chars
from chanta_core.context.policy import ContextHistoryPolicy, SessionContextPolicy
from chanta_core.context.result import ContextCompactionLayerResult


class SnipLayer:
    name = "SnipLayer"

    def __init__(
        self,
        history_policy: ContextHistoryPolicy | None = None,
        protected_block_types: set[str] | None = None,
        session_context_policy: SessionContextPolicy | None = None,
    ) -> None:
        self.session_context_policy = session_context_policy
        self.history_policy = (
            history_policy
            or (session_context_policy.history_policy if session_context_policy else None)
        )
        self.protected_block_types = protected_block_types or {"system", "user_request"}

    def apply(
        self,
        blocks: list[ContextBlock],
        budget: ContextBudget,
    ) -> ContextCompactionLayerResult:
        usable = budget.usable_chars()
        protected_ids, protect_reasons = self._protected_blocks(blocks)
        history_ids = {block.block_id for block in blocks if self._is_history_block(block)}

        if total_chars(blocks) <= usable:
            return ContextCompactionLayerResult(
                layer_name=self.name,
                blocks=list(blocks),
                changed=False,
                result_attrs={
                    "protected_block_ids": sorted(protected_ids),
                    "snip_reason_by_block_id": {},
                    "dropped_history_block_ids": [],
                },
            )

        keep_by_id = {block.block_id for block in blocks}
        dropped: list[str] = []
        snip_reason_by_block_id: dict[str, str] = {}
        candidates = [
            (index, block)
            for index, block in enumerate(blocks)
            if block.block_id not in protected_ids
        ]
        candidates.sort(key=lambda item: self._drop_sort_key(item[0], item[1]))
        current_total = total_chars(blocks)
        for _, block in candidates:
            if current_total <= usable:
                break
            keep_by_id.remove(block.block_id)
            dropped.append(block.block_id)
            snip_reason_by_block_id[block.block_id] = self._drop_reason(block)
            current_total -= block.char_length

        remaining = [block for block in blocks if block.block_id in keep_by_id]
        warnings: list[str] = []
        if total_chars(remaining) > usable:
            warnings.append(
                "Context remains over budget after SnipLayer; protected blocks were kept."
            )
        elif dropped:
            warnings.append(f"SnipLayer dropped {len(dropped)} low-priority block(s).")
        return ContextCompactionLayerResult(
            layer_name=self.name,
            blocks=remaining,
            changed=bool(dropped),
            dropped_block_ids=dropped,
            warnings=warnings,
            result_attrs={
                "snip_reason_by_block_id": snip_reason_by_block_id,
                "protected_block_ids": sorted(protected_ids),
                "protected_reason_by_block_id": protect_reasons,
                "dropped_history_block_ids": [
                    block_id for block_id in dropped if block_id in history_ids
                ],
            },
        )

    def _protected_blocks(
        self,
        blocks: list[ContextBlock],
    ) -> tuple[set[str], dict[str, str]]:
        protected: set[str] = set()
        reasons: dict[str, str] = {}
        for block in blocks:
            if block.block_type in self.protected_block_types or is_protected(block):
                protected.add(block.block_id)
                reasons[block.block_id] = "protected_block_type"

        for block_id, reason in self._recent_history_protections(blocks).items():
            protected.add(block_id)
            reasons[block_id] = reason

        if self.session_context_policy is not None:
            policy = self.session_context_policy.history_policy
            for block in blocks:
                if block.block_id in protected:
                    continue
                if block.priority < policy.min_priority_to_keep:
                    continue
                if (
                    policy.preserve_current_process_blocks
                    and self.session_context_policy.process_instance_id is not None
                    and block.block_attrs.get("process_instance_id")
                    == self.session_context_policy.process_instance_id
                ):
                    protected.add(block.block_id)
                    reasons[block.block_id] = "current_process"
                    continue
                if (
                    policy.preserve_current_session_blocks
                    and self.session_context_policy.session_id is not None
                    and block.block_attrs.get("session_id")
                    == self.session_context_policy.session_id
                ):
                    protected.add(block.block_id)
                    reasons[block.block_id] = "current_session"
        return protected, reasons

    def _recent_history_protections(
        self,
        blocks: list[ContextBlock],
    ) -> dict[str, str]:
        if self.history_policy is None:
            return {}
        self.history_policy.validate()
        result: dict[str, str] = {}
        for role, count, reason in [
            ("user", self.history_policy.preserve_last_user_blocks, "recent_user_history"),
            (
                "assistant",
                self.history_policy.preserve_last_assistant_blocks,
                "recent_assistant_history",
            ),
        ]:
            if count <= 0:
                continue
            role_blocks = [
                (index, block)
                for index, block in enumerate(blocks)
                if self._is_history_block(block) and block.block_attrs.get("role") == role
            ]
            role_blocks.sort(key=lambda item: self._history_order_key(item[0], item[1]))
            for _, block in role_blocks[-count:]:
                result[block.block_id] = reason
        return result

    def _drop_sort_key(self, index: int, block: ContextBlock) -> tuple[int, int, str, int]:
        return (
            self._drop_group(block),
            block.priority,
            str(block.block_attrs.get("created_at") or ""),
            index,
        )

    def _drop_group(self, block: ContextBlock) -> int:
        if self._is_history_block(block) or block.block_type in {
            "tool_result",
            "pig_report",
            "artifact",
        }:
            return 0
        if block.block_type in {"workspace", "repo", "worker", "scheduler", "edit", "patch"}:
            return 1
        return 2

    def _drop_reason(self, block: ContextBlock) -> str:
        if self._is_history_block(block):
            return "history_over_budget"
        if block.block_type in {"tool_result", "pig_report", "artifact"}:
            return f"{block.block_type}_over_budget"
        return "context_over_budget"

    @staticmethod
    def _history_order_key(index: int, block: ContextBlock) -> tuple[str, int]:
        return (str(block.block_attrs.get("created_at") or ""), index)

    @staticmethod
    def _is_history_block(block: ContextBlock) -> bool:
        return bool(block.block_attrs.get("is_history")) or block.block_type == "history"
