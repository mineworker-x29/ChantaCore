from chanta_core.context import ContextRenderer, make_context_block


def test_render_block() -> None:
    block = make_context_block(
        block_type="other",
        title="Title",
        content="body",
        priority=1,
        source="test",
    )

    rendered = ContextRenderer().render_block(block)

    assert rendered.startswith("[other] Title\nmetadata:")
    assert rendered.splitlines()[2] == "body"


def test_render_truncated_block_marker() -> None:
    block = make_context_block(
        block_type="other",
        title="Title",
        content="body",
        priority=1,
        source="test",
        was_truncated=True,
    )

    assert "content compacted/truncated by context pipeline" in ContextRenderer().render_block(block)


def test_render_refs_concisely() -> None:
    block = make_context_block(
        block_type="other",
        title="Title",
        content="body",
        priority=1,
        source="test",
        refs=[{"b": 2, "a": 1}],
    )

    rendered = ContextRenderer().render_block(block)

    assert "Refs:" in rendered
    assert "a=1" in rendered
