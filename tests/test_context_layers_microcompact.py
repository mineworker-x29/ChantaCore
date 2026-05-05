from chanta_core.context import ContextBudget, make_context_block
from chanta_core.context.layers import MicrocompactLayer


def test_repeated_blank_lines_are_removed() -> None:
    block = make_context_block(
        block_type="other",
        title="Text",
        content="a\n\n\nb  \n\n\nc",
        priority=10,
        source="test",
    )

    result = MicrocompactLayer().apply([block], ContextBudget())

    assert result.blocks[0].content == "a\n\nb\n\nc"
    assert result.blocks[0].block_attrs["microcompacted"] is True


def test_long_lines_are_truncated_deterministically() -> None:
    block = make_context_block(
        block_type="other",
        title="Long",
        content="x" * 700,
        priority=10,
        source="test",
    )

    result_a = MicrocompactLayer().apply([block], ContextBudget())
    result_b = MicrocompactLayer().apply([block], ContextBudget())

    assert result_a.blocks[0].content == result_b.blocks[0].content
    assert len(result_a.blocks[0].content) == 500
    assert "MicrocompactLayer" in result_a.blocks[0].content
