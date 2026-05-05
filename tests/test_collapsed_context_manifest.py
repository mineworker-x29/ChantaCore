from chanta_core.context import CollapsedContextManifest, ContextReference


def make_reference(index: int) -> ContextReference:
    return ContextReference(
        ref_id=f"context_ref:{index}",
        ref_type="tool_result",
        source="tool",
        title=f"Tool {index}",
        block_id=f"block:{index}",
    )


def test_manifest_to_dict() -> None:
    manifest = CollapsedContextManifest(
        manifest_id="manifest:1",
        collapsed_block_count=2,
        collapsed_by_type={"tool_result": 2},
        references=[make_reference(1), make_reference(2)],
        created_at="2026-05-05T00:00:00Z",
        manifest_attrs={"a": 1},
    )

    data = manifest.to_dict()

    assert data["manifest_id"] == "manifest:1"
    assert data["collapsed_block_count"] == 2
    assert len(data["references"]) == 2


def test_manifest_to_context_block() -> None:
    manifest = CollapsedContextManifest(
        manifest_id="manifest:2",
        collapsed_block_count=2,
        collapsed_by_type={"repo": 1, "tool_result": 1},
        references=[make_reference(1), make_reference(2)],
        created_at="2026-05-05T00:00:00Z",
    )

    block = manifest.to_context_block(priority=11)

    assert block.block_type == "collapsed_context"
    assert block.priority == 11
    assert "Collapsed block count: 2" in block.content
    assert "Raw content preserved in source stores" in block.content
    assert len(block.refs) == 2
    assert block.block_attrs["manifest_id"] == "manifest:2"
    assert block.block_attrs["collapsed_by_type"] == {"repo": 1, "tool_result": 1}
