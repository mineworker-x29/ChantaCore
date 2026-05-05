from chanta_core.context import ContextBudget, make_context_block
from chanta_core.context.layers import AutoCompactLayer


def test_auto_compact_disabled_by_default() -> None:
    block = make_context_block(
        block_type="other",
        title="Text",
        content="content",
        priority=10,
        source="test",
    )

    result = AutoCompactLayer().apply([block], ContextBudget())

    assert result.changed is False
    assert result.blocks == [block]
    assert result.result_attrs["disabled"] is True


def test_auto_compact_enabled_without_allow_flag_is_blocked() -> None:
    block = make_context_block(
        block_type="other",
        title="Text",
        content="content",
        priority=10,
        source="test",
    )

    result = AutoCompactLayer(enabled=True).apply([block], ContextBudget())

    assert result.changed is False
    assert "not allowed" in result.warnings[0]
    assert result.result_attrs["used_summarizer"] is False
