from chanta_core.context import ContextBudget, ContextCollapsePolicy, make_context_block
from chanta_core.context.layers import ContextCollapseLayer


def make_block(block_id: str, block_type: str, priority: int, content: str = "raw") :
    return make_context_block(
        block_id=block_id,
        block_type=block_type,
        title=f"{block_type} {block_id}",
        content=content,
        priority=priority,
        source=block_type,
        refs=[{"ref_type": block_type, "ref_id": block_id}],
        block_attrs={"created_at": f"2026-05-05T00:0{priority}:00Z"},
    )


def test_context_collapse_layer_creates_reference_manifest() -> None:
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
            block_id="user",
            block_type="user_request",
            title="User",
            content="user",
            priority=100,
            source="runtime",
        ),
        make_block("tool", "tool_result", 5, "tool raw secret" + ("x" * 300)),
        make_block("report", "pig_report", 10, "report raw secret" + ("y" * 300)),
        make_block("repo", "repo", 15, "repo raw secret" + ("z" * 300)),
        make_block("artifact", "artifact", 20, "artifact raw secret" + ("a" * 300)),
    ]
    layer = ContextCollapseLayer(
        ContextCollapsePolicy(max_collapsed_block_chars=1200, min_blocks_to_collapse=1)
    )

    result = layer.apply(blocks, ContextBudget(max_total_chars=900, reserve_chars=100))

    kept = {block.block_id for block in result.blocks}
    assert {"system", "user"}.issubset(kept)
    collapsed_blocks = [block for block in result.blocks if block.block_type == "collapsed_context"]
    assert collapsed_blocks
    collapsed = collapsed_blocks[0]
    assert "raw secret" not in collapsed.content
    assert "Raw content preserved in source stores" in collapsed.content
    assert collapsed.refs
    assert result.result_attrs["collapsed_block_count"] >= 1
    assert result.result_attrs["reference_count"] >= 1
    assert result.result_attrs["manifest_id"].startswith("collapsed_context_manifest:")


def test_context_collapse_layer_is_deterministic_except_generated_fields() -> None:
    blocks = [
        make_context_block(
            block_type="system",
            title="System",
            content="system",
            priority=100,
            source="runtime",
        ),
        make_block("tool", "tool_result", 5, "tool" * 100),
        make_block("repo", "repo", 5, "repo" * 100),
    ]
    layer = ContextCollapseLayer(ContextCollapsePolicy(min_blocks_to_collapse=1))
    budget = ContextBudget(max_total_chars=300, reserve_chars=50)

    result_a = layer.apply(blocks, budget)
    result_b = layer.apply(blocks, budget)

    assert result_a.dropped_block_ids == result_b.dropped_block_ids
    assert result_a.result_attrs["collapsed_by_type"] == result_b.result_attrs["collapsed_by_type"]


def test_context_collapse_layer_disabled_noop() -> None:
    block = make_block("tool", "tool_result", 1, "x" * 100)

    result = ContextCollapseLayer(ContextCollapsePolicy(enabled=False)).apply(
        [block],
        ContextBudget(max_total_chars=50, reserve_chars=10),
    )

    assert result.blocks == [block]
    assert result.changed is False
    assert result.result_attrs["disabled"] is True
