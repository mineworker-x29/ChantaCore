from chanta_core.context import ContextBlock, estimate_tokens, make_context_block


def test_estimate_tokens_is_deterministic() -> None:
    assert estimate_tokens("abcd" * 10) == 10
    assert estimate_tokens("") == 1


def test_context_block_to_dict() -> None:
    block = ContextBlock(
        block_id="block:1",
        block_type="other",
        title="Title",
        content="content",
        priority=10,
        source="test",
        token_estimate=1,
        char_length=7,
        refs=[{"ref_id": "x"}],
        block_attrs={"a": 1},
    )

    data = block.to_dict()

    assert data["block_id"] == "block:1"
    assert data["refs"] == [{"ref_id": "x"}]
    assert data["block_attrs"] == {"a": 1}


def test_make_context_block_creates_consistent_fields() -> None:
    block = make_context_block(
        block_type="tool_result",
        title="Tool",
        content="abcdef",
        priority=20,
        source="tool",
    )

    assert block.block_id.startswith("context_block:")
    assert block.char_length == 6
    assert block.token_estimate == 1
    assert block.was_truncated is False
