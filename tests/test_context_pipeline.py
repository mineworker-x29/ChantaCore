from chanta_core.context import ContextBudget, ContextCompactionPipeline, make_context_block
from chanta_core.context.layers import (
    AutoCompactLayer,
    BudgetReductionLayer,
    ContextCollapseLayer,
    MicrocompactLayer,
    SnipLayer,
)


def test_default_layer_order() -> None:
    pipeline = ContextCompactionPipeline.default()

    assert [type(layer) for layer in pipeline.layers] == [
        BudgetReductionLayer,
        SnipLayer,
        MicrocompactLayer,
        ContextCollapseLayer,
        AutoCompactLayer,
    ]


def test_pipeline_runs_all_layers_and_respects_budget() -> None:
    blocks = [
        make_context_block(
            block_type="system",
            title="System",
            content="system",
            priority=100,
            source="test",
        ),
        make_context_block(
            block_type="tool_result",
            title="Tool",
            content="x" * 1000,
            priority=10,
            source="test",
        ),
    ]
    budget = ContextBudget(
        max_total_chars=300,
        reserve_chars=50,
        max_tool_result_chars=120,
    )

    result = ContextCompactionPipeline.default().run(blocks, budget)

    assert len(result.layer_results) == 5
    assert result.total_chars <= budget.usable_chars()
    assert result.truncated_block_ids
