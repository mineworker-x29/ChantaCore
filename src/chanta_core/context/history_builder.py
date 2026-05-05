from __future__ import annotations

from chanta_core.context.block import ContextBlock
from chanta_core.context.history import ContextHistoryEntry, history_entry_to_context_block
from chanta_core.context.policy import SessionContextPolicy


class ContextHistoryBuilder:
    def build_from_entries(
        self,
        entries: list[ContextHistoryEntry],
    ) -> list[ContextBlock]:
        return [
            history_entry_to_context_block(entry)
            for entry in self._sorted_entries(entries)
        ]

    def build_recent_history_blocks(
        self,
        entries: list[ContextHistoryEntry],
        *,
        session_policy: SessionContextPolicy,
    ) -> list[ContextBlock]:
        if not session_policy.include_history:
            return []
        session_policy.history_policy.validate()
        filtered = list(entries)
        policy = session_policy.history_policy
        if policy.preserve_current_session_blocks and session_policy.session_id is not None:
            filtered = [
                entry for entry in filtered if entry.session_id == session_policy.session_id
            ]
        if (
            policy.preserve_current_process_blocks
            and session_policy.process_instance_id is not None
        ):
            filtered = [
                entry
                for entry in filtered
                if entry.process_instance_id == session_policy.process_instance_id
            ]
        filtered = self._sorted_entries(filtered)
        max_blocks = min(
            policy.max_history_blocks,
            policy.max_recent_history_blocks,
        )
        if len(filtered) > max_blocks:
            filtered = filtered[-max_blocks:]
        return [history_entry_to_context_block(entry) for entry in filtered]

    @staticmethod
    def _sorted_entries(
        entries: list[ContextHistoryEntry],
    ) -> list[ContextHistoryEntry]:
        return sorted(entries, key=lambda entry: (entry.created_at, entry.entry_id))
