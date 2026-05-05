from __future__ import annotations

from typing import TYPE_CHECKING

from chanta_core.context import (
    ContextAssemblySnapshot,
    ContextAuditService,
    ContextBlock,
    ContextBudget,
    ContextCompactionPipeline,
    ContextCompactionResult,
    ContextHistoryBuilder,
    ContextHistoryEntry,
    ContextRenderer,
    ContextSnapshotPolicy,
    ContextSnapshotStore,
    SessionContextPolicy,
    make_context_block,
)
from chanta_core.llm.types import ChatMessage

if TYPE_CHECKING:
    from chanta_core.pig.context import PIGContext


class ProcessContextAssembler:
    def __init__(self) -> None:
        self.last_compaction_result: ContextCompactionResult | None = None
        self.last_snapshot: ContextAssemblySnapshot | None = None

    def assemble_for_llm_chat(
        self,
        user_input: str,
        system_prompt: str | None = None,
        pig_context: PIGContext | None = None,
        extra_blocks: list[ContextBlock] | None = None,
        context_budget: ContextBudget | None = None,
        compaction_pipeline: ContextCompactionPipeline | None = None,
        history_entries: list[ContextHistoryEntry] | None = None,
        session_context_policy: SessionContextPolicy | None = None,
        context_snapshot_policy: ContextSnapshotPolicy | None = None,
        context_snapshot_store: ContextSnapshotStore | None = None,
        context_audit_service: ContextAuditService | None = None,
        session_id: str | None = None,
        process_instance_id: str | None = None,
    ) -> list[ChatMessage]:
        self.last_compaction_result = None
        self.last_snapshot = None
        snapshot_enabled = self._snapshot_enabled(
            context_snapshot_policy,
            context_audit_service,
        )
        if (
            context_budget is None
            and not extra_blocks
            and not history_entries
            and session_context_policy is None
        ):
            messages = self._assemble_legacy(
                user_input=user_input,
                system_prompt=system_prompt,
                pig_context=pig_context,
            )
            if snapshot_enabled:
                self.last_snapshot = self._maybe_snapshot(
                    blocks=self._build_blocks(
                        user_input=user_input,
                        system_prompt=system_prompt,
                        pig_context=pig_context,
                        history_entries=None,
                        session_context_policy=None,
                        extra_blocks=None,
                    ),
                    messages=messages,
                    context_budget=None,
                    context_snapshot_policy=context_snapshot_policy,
                    context_snapshot_store=context_snapshot_store,
                    context_audit_service=context_audit_service,
                    session_id=session_id,
                    process_instance_id=process_instance_id,
                )
            return messages

        assembled_blocks = self._build_blocks(
            user_input=user_input,
            system_prompt=system_prompt,
            pig_context=pig_context,
            history_entries=history_entries,
            session_context_policy=session_context_policy,
            extra_blocks=extra_blocks,
        )
        blocks = list(assembled_blocks)
        if context_budget is not None:
            pipeline = compaction_pipeline or ContextCompactionPipeline.default(
                session_context_policy=session_context_policy,
            )
            self.last_compaction_result = pipeline.run(blocks, context_budget)
            blocks = self.last_compaction_result.blocks

        renderer = ContextRenderer()
        messages: list[ChatMessage] = []
        for block in blocks:
            if block.block_type == "user_request":
                messages.append({"role": "user", "content": block.content})
            else:
                messages.append({"role": "system", "content": renderer.render_block(block)})
        self.last_snapshot = self._maybe_snapshot(
            blocks=assembled_blocks,
            messages=messages,
            context_budget=context_budget,
            context_snapshot_policy=context_snapshot_policy,
            context_snapshot_store=context_snapshot_store,
            context_audit_service=context_audit_service,
            session_id=session_id,
            process_instance_id=process_instance_id,
        )
        return messages

    def _assemble_legacy(
        self,
        *,
        user_input: str,
        system_prompt: str | None,
        pig_context: PIGContext | None,
    ) -> list[ChatMessage]:
        messages: list[ChatMessage] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if pig_context is not None:
            messages.append({"role": "system", "content": pig_context.context_text})
        messages.append({"role": "user", "content": user_input})
        return messages

    def _build_blocks(
        self,
        *,
        user_input: str,
        system_prompt: str | None,
        pig_context: PIGContext | None,
        history_entries: list[ContextHistoryEntry] | None,
        session_context_policy: SessionContextPolicy | None,
        extra_blocks: list[ContextBlock] | None,
    ) -> list[ContextBlock]:
        blocks: list[ContextBlock] = []
        if system_prompt:
            blocks.append(
                make_context_block(
                    block_type="system",
                    title="System Prompt",
                    content=system_prompt,
                    priority=100,
                    source="runtime",
                )
            )
        if pig_context is not None:
            blocks.append(pig_context.to_context_block(priority=70))
        if history_entries:
            builder = ContextHistoryBuilder()
            if session_context_policy is not None:
                blocks.extend(
                    builder.build_recent_history_blocks(
                        history_entries,
                        session_policy=session_context_policy,
                    )
                )
            else:
                blocks.extend(builder.build_from_entries(history_entries))
        blocks.extend(extra_blocks or [])
        blocks.append(
            make_context_block(
                block_type="user_request",
                title="User Request",
                content=user_input,
                priority=100,
                source="runtime",
            )
        )
        return blocks

    @staticmethod
    def _snapshot_enabled(
        policy: ContextSnapshotPolicy | None,
        audit_service: ContextAuditService | None,
    ) -> bool:
        if audit_service is not None:
            return audit_service.snapshot_policy.enabled
        return bool(policy and policy.enabled)

    def _maybe_snapshot(
        self,
        *,
        blocks: list[ContextBlock],
        messages: list[ChatMessage],
        context_budget: ContextBudget | None,
        context_snapshot_policy: ContextSnapshotPolicy | None,
        context_snapshot_store: ContextSnapshotStore | None,
        context_audit_service: ContextAuditService | None,
        session_id: str | None,
        process_instance_id: str | None,
    ) -> ContextAssemblySnapshot | None:
        audit_service = context_audit_service
        if audit_service is None:
            if context_snapshot_policy is None:
                return None
            audit_service = ContextAuditService(
                snapshot_policy=context_snapshot_policy,
                snapshot_store=context_snapshot_store,
            )
        return audit_service.maybe_store_snapshot(
            blocks=blocks,
            messages=messages,
            compaction_result=self.last_compaction_result,
            budget=context_budget,
            session_id=session_id,
            process_instance_id=process_instance_id,
        )
