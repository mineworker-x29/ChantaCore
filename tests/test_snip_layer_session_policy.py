from chanta_core.context import ContextBudget, ContextHistoryPolicy, SessionContextPolicy
from chanta_core.context.block import make_context_block
from chanta_core.context.layers import SnipLayer


def history_block(
    block_id: str,
    *,
    role: str,
    created_at: str,
    priority: int,
    content_length: int = 120,
) :
    return make_context_block(
        block_id=block_id,
        block_type="history",
        title=f"History {role}",
        content=block_id + ("x" * content_length),
        priority=priority,
        source="chat",
        block_attrs={
            "is_history": True,
            "role": role,
            "created_at": created_at,
            "session_id": "session:1",
            "process_instance_id": "pi:1",
        },
    )


def test_session_aware_snip_preserves_protected_and_recent_blocks() -> None:
    blocks = [
        make_context_block(
            block_id="system",
            block_type="system",
            title="System",
            content="system",
            priority=100,
            source="runtime",
        ),
        make_context_block(
            block_id="current-user",
            block_type="user_request",
            title="User",
            content="current user",
            priority=100,
            source="runtime",
        ),
        history_block(
            "old-assistant",
            role="assistant",
            created_at="2026-05-05T00:00:00Z",
            priority=10,
        ),
        history_block(
            "recent-assistant",
            role="assistant",
            created_at="2026-05-05T00:03:00Z",
            priority=10,
        ),
        history_block(
            "recent-user",
            role="user",
            created_at="2026-05-05T00:04:00Z",
            priority=10,
        ),
        make_context_block(
            block_id="old-tool",
            block_type="tool_result",
            title="Tool",
            content="tool" + ("t" * 120),
            priority=5,
            source="tool",
            block_attrs={
                "created_at": "2026-05-05T00:01:00Z",
                "session_id": "session:1",
                "process_instance_id": "pi:1",
            },
        ),
        make_context_block(
            block_id="current-pig",
            block_type="pig_context",
            title="PIG",
            content="pig" + ("p" * 120),
            priority=70,
            source="pig",
            block_attrs={
                "session_id": "session:1",
                "process_instance_id": "pi:1",
            },
        ),
        make_context_block(
            block_id="low-report",
            block_type="pig_report",
            title="Report",
            content="report" + ("r" * 120),
            priority=20,
            source="pig_report",
            block_attrs={"created_at": "2026-05-05T00:02:00Z"},
        ),
        make_context_block(
            block_id="decision",
            block_type="decision",
            title="Decision",
            content="decision" + ("d" * 120),
            priority=80,
            source="decision",
        ),
    ]
    session_policy = SessionContextPolicy(
        session_id="session:1",
        process_instance_id="pi:1",
        history_policy=ContextHistoryPolicy(
            preserve_last_user_blocks=1,
            preserve_last_assistant_blocks=1,
            min_priority_to_keep=50,
        ),
    )
    budget = ContextBudget(max_total_chars=650, reserve_chars=50)

    result = SnipLayer(session_context_policy=session_policy).apply(blocks, budget)

    kept_ids = {block.block_id for block in result.blocks}
    assert {"system", "current-user", "recent-assistant", "recent-user", "current-pig"}.issubset(
        kept_ids
    )
    assert "old-assistant" in result.dropped_block_ids
    assert result.dropped_block_ids[:3] == ["old-tool", "old-assistant", "low-report"]
    assert sum(block.char_length for block in result.blocks) <= budget.usable_chars()
    assert result.result_attrs["dropped_history_block_ids"] == ["old-assistant"]
    assert result.warnings


def test_session_aware_snip_drop_order_is_deterministic() -> None:
    blocks = [
        history_block("old-1", role="assistant", created_at="2026-05-05T00:00:00Z", priority=1),
        history_block("old-2", role="assistant", created_at="2026-05-05T00:01:00Z", priority=1),
        history_block("old-3", role="assistant", created_at="2026-05-05T00:02:00Z", priority=1),
    ]
    budget = ContextBudget(max_total_chars=180, reserve_chars=20)
    policy = SessionContextPolicy(
        session_id="session:1",
        process_instance_id="pi:1",
        history_policy=ContextHistoryPolicy(
            preserve_last_user_blocks=0,
            preserve_last_assistant_blocks=0,
            min_priority_to_keep=50,
        ),
    )

    result_a = SnipLayer(session_context_policy=policy).apply(blocks, budget)
    result_b = SnipLayer(session_context_policy=policy).apply(blocks, budget)

    assert result_a.dropped_block_ids == result_b.dropped_block_ids
    assert result_a.dropped_block_ids == ["old-1", "old-2"]
