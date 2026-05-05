from chanta_core.context import ContextBudget, ContextCompactionPipeline, make_context_block


def test_full_pipeline_microcompact_preserves_system_and_user() -> None:
    blocks = [
        make_context_block(
            block_type="system",
            title="System",
            content="system prompt",
            priority=100,
            source="runtime",
        ),
        make_context_block(
            block_type="pig_context",
            title="PIG",
            content="\n".join(f"pig {index}" for index in range(100)),
            priority=70,
            source="pig",
            block_attrs={"activity_sequence": [f"a{index}" for index in range(60)]},
        ),
        make_context_block(
            block_type="tool_result",
            title="Tool",
            content='{"z": [1, 2, 3], "a": {"nested": true}}',
            priority=40,
            source="tool",
        ),
        make_context_block(
            block_type="repo",
            title="Repo",
            content="\n".join(f"match-{index}" for index in range(120)),
            priority=60,
            source="repo",
        ),
        make_context_block(
            block_type="user_request",
            title="User",
            content="current user request",
            priority=100,
            source="runtime",
        ),
    ]
    budget = ContextBudget(max_total_chars=1800, reserve_chars=200, max_repo_chars=700)

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
    assert result.total_chars <= budget.usable_chars()
    microcompact = result.layer_results[2]
    assert microcompact.layer_name == "MicrocompactLayer"
    assert microcompact.result_attrs["microcompacted_block_count"] >= 1
