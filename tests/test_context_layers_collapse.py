from chanta_core.context import ContextBudget, make_context_block
from chanta_core.context.layers import ContextCollapseLayer


def test_collapse_block_created_when_over_budget() -> None:
    blocks = [
        make_context_block(
            block_type="system",
            title="System",
            content="s" * 100,
            priority=100,
            source="test",
        )
    ] + [
        make_context_block(
            block_type="artifact",
            title=f"Artifact {index}",
            content=f"raw-{index}-" + ("x" * 190),
            priority=10 + index,
            source="artifact_store",
            refs=[{"artifact_id": f"a:{index}"}],
        )
        for index in range(3)
    ]
    budget = ContextBudget(max_total_chars=600, reserve_chars=100)

    result = ContextCollapseLayer().apply(blocks, budget)

    collapsed = [block for block in result.blocks if block.title == "Collapsed Context References"]
    assert collapsed
    assert "Artifact 0" in collapsed[0].content
    assert "artifact" in collapsed[0].content
    assert "artifact_id=a:0" in collapsed[0].content
    assert "raw-0-" not in collapsed[0].content
    assert "Raw content preserved in source stores" in collapsed[0].content


def test_collapse_is_deterministic() -> None:
    blocks = [
        make_context_block(
            block_type="artifact",
            title=f"Artifact {index}",
            content="x" * 250,
            priority=10,
            source="test",
        )
        for index in range(4)
    ]
    budget = ContextBudget(max_total_chars=500, reserve_chars=50)

    result_a = ContextCollapseLayer().apply(blocks, budget)
    result_b = ContextCollapseLayer().apply(blocks, budget)

    assert [block.title for block in result_a.blocks] == [
        block.title for block in result_b.blocks
    ]
