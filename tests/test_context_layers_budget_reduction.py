from chanta_core.context import ContextBudget, make_context_block
from chanta_core.context.layers import BudgetReductionLayer


def test_oversized_tool_result_truncated_by_limit() -> None:
    block = make_context_block(
        block_type="tool_result",
        title="Tool",
        content="x" * 500,
        priority=10,
        source="test",
    )
    budget = ContextBudget(max_tool_result_chars=120)

    result = BudgetReductionLayer().apply([block], budget)

    assert result.changed is True
    assert result.blocks[0].char_length <= 120
    assert result.blocks[0].was_truncated is True
    assert "BudgetReductionLayer" in result.blocks[0].content


def test_oversized_pig_context_truncated_by_limit_and_refs_preserved() -> None:
    block = make_context_block(
        block_type="pig_context",
        title="PIG",
        content="p" * 500,
        priority=70,
        source="pig",
        refs=[{"process_instance_id": "pi:1"}],
    )
    budget = ContextBudget(max_pig_context_chars=130)

    result = BudgetReductionLayer().apply([block], budget)

    assert result.blocks[0].char_length <= 130
    assert result.blocks[0].refs == [{"process_instance_id": "pi:1"}]
    assert result.truncated_block_ids == [block.block_id]
