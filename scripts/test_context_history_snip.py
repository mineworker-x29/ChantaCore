from chanta_core.context import (
    ContextBudget,
    ContextHistoryEntry,
    ContextHistoryPolicy,
    ContextRenderer,
    SessionContextPolicy,
)
from chanta_core.context.history_builder import ContextHistoryBuilder
from chanta_core.context.pipeline import ContextCompactionPipeline
from chanta_core.context.block import make_context_block


def entry(index: int, role: str, content: str, priority: int) -> ContextHistoryEntry:
    return ContextHistoryEntry(
        entry_id=f"history:{index}",
        session_id="session:script",
        process_instance_id="pi:script",
        role=role,
        content=content,
        created_at=f"2026-05-05T00:{index:02d}:00Z",
        source="script",
        priority=priority,
        refs=[{"entry_id": f"history:{index}"}],
    )


def main() -> None:
    entries = [
        entry(1, "assistant", "old assistant " + ("a" * 500), 5),
        entry(2, "user", "old user " + ("u" * 500), 5),
        entry(3, "assistant", "recent assistant", 60),
        entry(4, "user", "recent user", 60),
    ]
    session_policy = SessionContextPolicy(
        session_id="session:script",
        process_instance_id="pi:script",
        history_policy=ContextHistoryPolicy(
            max_history_blocks=4,
            max_recent_history_blocks=4,
            preserve_last_user_blocks=1,
            preserve_last_assistant_blocks=1,
            min_priority_to_keep=50,
        ),
    )
    history_blocks = ContextHistoryBuilder().build_recent_history_blocks(
        entries,
        session_policy=session_policy,
    )
    blocks = [
        make_context_block(
            block_type="system",
            title="System Prompt",
            content="system",
            priority=100,
            source="script",
        ),
        *history_blocks,
        make_context_block(
            block_type="user_request",
            title="User Request",
            content="current request",
            priority=100,
            source="script",
        ),
    ]
    result = ContextCompactionPipeline.default(
        session_context_policy=session_policy,
    ).run(
        blocks,
        ContextBudget(max_total_chars=550, reserve_chars=100),
    )
    print(f"before_block_count={len(blocks)}")
    print(f"after_block_count={len(result.blocks)}")
    print(f"dropped_block_ids={result.dropped_block_ids}")
    print(f"snipped_history_count={result.result_attrs['snipped_history_count']}")
    print("--- rendered context ---")
    print(ContextRenderer().render_blocks(result.blocks))


if __name__ == "__main__":
    main()
