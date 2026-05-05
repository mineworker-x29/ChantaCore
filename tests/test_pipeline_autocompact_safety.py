from chanta_core.context import ContextBudget, ContextCompactionPipeline, make_context_block
from chanta_core.context.layers import AutoCompactLayer


def test_default_pipeline_has_disabled_autocompact_and_is_deterministic() -> None:
    blocks = [
        make_context_block(
            block_type="system",
            title="System",
            content="system",
            priority=100,
            source="test",
        ),
        make_context_block(
            block_type="user_request",
            title="User",
            content="hello",
            priority=100,
            source="test",
        ),
    ]
    pipeline = ContextCompactionPipeline.default()

    result_a = pipeline.run(blocks, ContextBudget())
    result_b = pipeline.run(blocks, ContextBudget())

    assert isinstance(pipeline.layers[-1], AutoCompactLayer)
    assert result_a.layer_results[-1].layer_name == "AutoCompactLayer"
    assert result_a.layer_results[-1].result_attrs["disabled"] is True
    assert result_a.layer_results[-1].result_attrs["used_summarizer"] is False
    assert [block.content for block in result_a.blocks] == [
        block.content for block in result_b.blocks
    ]
