from chanta_core.context import ContextBudget, make_context_block
from chanta_core.context.layers import SnipLayer


def test_low_priority_blocks_are_dropped_until_budget_is_respected() -> None:
    blocks = [
        make_context_block(
            block_type="system",
            title="System",
            content="system",
            priority=100,
            source="test",
        ),
        make_context_block(
            block_type="other",
            title="Low",
            content="x" * 200,
            priority=1,
            source="test",
        ),
        make_context_block(
            block_type="other",
            title="High",
            content="y" * 20,
            priority=90,
            source="test",
        ),
    ]
    budget = ContextBudget(max_total_chars=100, reserve_chars=10)

    result = SnipLayer().apply(blocks, budget)

    assert blocks[1].block_id in result.dropped_block_ids
    assert sum(block.char_length for block in result.blocks) <= budget.usable_chars()


def test_system_and_user_request_are_protected() -> None:
    blocks = [
        make_context_block(
            block_type="system",
            title="System",
            content="s" * 80,
            priority=100,
            source="test",
        ),
        make_context_block(
            block_type="user_request",
            title="User",
            content="u" * 80,
            priority=100,
            source="test",
        ),
        make_context_block(
            block_type="other",
            title="Low",
            content="x" * 80,
            priority=1,
            source="test",
        ),
    ]
    budget = ContextBudget(max_total_chars=100, reserve_chars=10)

    result = SnipLayer().apply(blocks, budget)

    kept_types = {block.block_type for block in result.blocks}
    assert {"system", "user_request"}.issubset(kept_types)
    assert result.warnings
