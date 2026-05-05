from chanta_core.context import ContextRenderPolicy, ContextRenderer, make_context_block


def test_renderer_includes_header_metadata_and_limited_refs() -> None:
    block = make_context_block(
        block_type="tool_result",
        title="Tool",
        content="body",
        priority=40,
        source="tool",
        refs=[{"ref_type": "x", "ref_id": str(index), "large": "y" * 200} for index in range(8)],
    )

    rendered = ContextRenderer().render_block(block)

    assert rendered.startswith("[tool_result] Tool\nmetadata:")
    assert "source=tool" in rendered
    assert rendered.count("- ref_type=x") == 5
    assert "3 more ref" in rendered
    assert "y" * 120 not in rendered


def test_renderer_does_not_dump_huge_attrs() -> None:
    block = make_context_block(
        block_type="other",
        title="Attrs",
        content="body",
        priority=1,
        source="test",
        block_attrs={"huge": "z" * 1000},
    )

    rendered = ContextRenderer().render_block(block)

    assert "z" * 100 not in rendered


def test_renderer_marks_compacted_or_truncated_blocks() -> None:
    block = make_context_block(
        block_type="other",
        title="Truncated",
        content="body",
        priority=1,
        source="test",
        was_truncated=True,
        block_attrs={"microcompacted": True},
    )

    rendered = ContextRenderer().render_block(block)

    assert "microcompacted=True" in rendered
    assert "content compacted/truncated by context pipeline" in rendered


def test_renderer_policy_can_hide_refs_and_metadata() -> None:
    block = make_context_block(
        block_type="other",
        title="Plain",
        content="body",
        priority=1,
        source="test",
        refs=[{"ref_id": "1"}],
    )

    rendered = ContextRenderer(
        ContextRenderPolicy(include_refs=False, include_block_metadata=False)
    ).render_block(block)

    assert rendered == "[other] Plain\nbody"
