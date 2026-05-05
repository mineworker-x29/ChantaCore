from chanta_core.context import ContextBudget, ContextCompactionPipeline, make_context_block


def long_block(block_id: str, block_type: str, priority: int):
    return make_context_block(
        block_id=block_id,
        block_type=block_type,
        title=f"{block_type} {block_id}",
        content=f"raw-{block_id}-" + ("x" * 1000),
        priority=priority,
        source=block_type,
        refs=[{"ref_type": block_type, "ref_id": block_id}],
    )


def test_full_pipeline_creates_collapsed_context_for_dropped_blocks() -> None:
    blocks = [
        make_context_block(
            block_id="system",
            block_type="system",
            title="System",
            content="system",
            priority=100,
            source="runtime",
        ),
        long_block("tool", "tool_result", 5),
        long_block("repo", "repo", 10),
        long_block("artifact", "artifact", 15),
        make_context_block(
            block_id="user",
            block_type="user_request",
            title="User",
            content="user",
            priority=100,
            source="runtime",
        ),
    ]
    budget = ContextBudget(max_total_chars=900, reserve_chars=100)

    result = ContextCompactionPipeline.default().run(blocks, budget)

    assert [layer.layer_name for layer in result.layer_results] == [
        "BudgetReductionLayer",
        "SnipLayer",
        "MicrocompactLayer",
        "ContextCollapseLayer",
        "AutoCompactLayer",
    ]
    assert any(block.block_type == "system" for block in result.blocks)
    assert any(block.block_type == "user_request" for block in result.blocks)
    collapsed = [block for block in result.blocks if block.block_type == "collapsed_context"]
    assert collapsed
    assert "raw-tool" not in collapsed[0].content
    assert result.total_chars <= budget.usable_chars()
    collapse_result = result.layer_results[3]
    assert collapse_result.result_attrs["collapsed_block_count"] >= 1
    assert collapse_result.created_block_ids
