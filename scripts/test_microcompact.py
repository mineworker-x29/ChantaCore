from chanta_core.context import (
    ContextBudget,
    ContextCompactionPipeline,
    ContextRenderer,
    MicrocompactPolicy,
    compact_activity_sequence,
    make_context_block,
)
from chanta_core.context.layers import MicrocompactLayer


def main() -> None:
    sequence = [f"activity_{index}" for index in range(80)]
    sequence_text, sequence_changed = compact_activity_sequence(sequence)
    print(f"activity_sequence_changed={sequence_changed}")
    print(sequence_text)

    blocks = [
        make_context_block(
            block_type="pig_context",
            title="Long PIG Context",
            content="\n".join(f"pig context line {index}" for index in range(120)),
            priority=70,
            source="pig",
            block_attrs={"activity_sequence": sequence, "scope": "recent"},
        ),
        make_context_block(
            block_type="tool_result",
            title="JSON Tool Result",
            content='{"z": [1, 2, 3], "a": {"nested": true}, "b": "value"}',
            priority=40,
            source="tool",
        ),
        make_context_block(
            block_type="pig_report",
            title="Long PIG Report",
            content="\n".join(["# Report"] + [f"report line {index}" for index in range(120)]),
            priority=50,
            source="pig_report",
        ),
    ]
    before_chars = sum(block.char_length for block in blocks)
    layer_result = MicrocompactLayer(
        policy=MicrocompactPolicy(max_lines=30, max_report_chars=1200)
    ).apply(blocks, ContextBudget(max_block_chars=1500))
    after_layer_chars = sum(block.char_length for block in layer_result.blocks)
    pipeline_result = ContextCompactionPipeline.default().run(
        blocks,
        ContextBudget(max_total_chars=3000, reserve_chars=250),
    )
    print(f"before_chars={before_chars}")
    print(f"after_microcompact_chars={after_layer_chars}")
    print(f"pipeline_after_chars={pipeline_result.total_chars}")
    print(f"microcompacted_block_count={layer_result.result_attrs['microcompacted_block_count']}")
    print("--- rendered context ---")
    print(ContextRenderer().render_blocks(pipeline_result.blocks))


if __name__ == "__main__":
    main()
