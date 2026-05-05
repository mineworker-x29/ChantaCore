from chanta_core.context import (
    CollapsedContextManifest,
    ContextReference,
    ContextRenderPolicy,
    ContextRenderer,
)


def test_renderer_renders_collapsed_context_clearly() -> None:
    block = CollapsedContextManifest(
        manifest_id="manifest:1",
        collapsed_block_count=12,
        collapsed_by_type={"tool_result": 7, "repo": 5},
        references=[
            ContextReference(
                ref_id=f"context_ref:{index}",
                ref_type="tool_result",
                source="tool",
                title=f"Tool {index}",
                block_id=f"block:{index}",
            )
            for index in range(12)
        ],
        created_at="2026-05-05T00:00:00Z",
    ).to_context_block()

    rendered = ContextRenderer(ContextRenderPolicy(max_collapsed_refs=3)).render_block(block)

    assert rendered.startswith("[collapsed_context] Collapsed Context References")
    assert "Collapsed block count: 12" in rendered
    assert "Raw content preserved in source stores" in rendered
    assert rendered.count("- ref_type=tool_result") == 3
    assert "9 more ref" in rendered


def test_renderer_does_not_dump_raw_collapsed_content() -> None:
    reference = ContextReference(
        ref_id="context_ref:raw",
        ref_type="context_block",
        source="test",
        title="Raw Block",
        block_id="block:raw",
        attrs={"raw_content": "secret should not render"},
    )
    block = CollapsedContextManifest(
        manifest_id="manifest:2",
        collapsed_block_count=1,
        collapsed_by_type={"other": 1},
        references=[reference],
        created_at="2026-05-05T00:00:00Z",
    ).to_context_block()

    rendered = ContextRenderer().render_block(block)

    assert "secret should not render" not in rendered
