from chanta_core.context import ContextBudget, ContextCompactionPipeline
from chanta_core.context.block import make_context_block


def test_context_compactor_alias_runs_default_pipeline() -> None:
    block = make_context_block(
        block_type="tool_result",
        title="Tool",
        content="x" * 1000,
        priority=10,
        source="test",
    )

    result = ContextCompactionPipeline.default().run(
        [block],
        ContextBudget(max_tool_result_chars=100),
    )

    assert result.truncated_block_ids == [block.block_id]
