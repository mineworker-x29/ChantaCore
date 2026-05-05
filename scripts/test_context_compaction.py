from chanta_core.context import ContextBudget, ContextCompactionPipeline, ContextRenderer
from chanta_core.context.block import make_context_block


def main() -> None:
    blocks = [
        make_context_block(
            block_type="pig_context",
            title="Process Intelligence Context",
            content="Process Intelligence Context:\n" + ("activity\n" * 600),
            priority=70,
            source="pig",
            refs=[{"scope": "recent"}],
        ),
        make_context_block(
            block_type="tool_result",
            title="Tool Result: tool:repo / search",
            content="result\n" * 500,
            priority=40,
            source="tool",
            refs=[{"tool_result_id": "tool_result:demo"}],
        ),
    ]
    budget = ContextBudget(max_total_chars=6000, reserve_chars=500)
    before_chars = sum(block.char_length for block in blocks)
    result = ContextCompactionPipeline.default().run(blocks, budget)

    print(f"before_chars={before_chars}")
    print(f"after_chars={result.total_chars}")
    for layer_result in result.layer_results:
        print(
            f"{layer_result.layer_name}: changed={layer_result.changed} "
            f"truncated={len(layer_result.truncated_block_ids)} "
            f"dropped={len(layer_result.dropped_block_ids)}"
        )
    print("--- rendered context ---")
    print(ContextRenderer().render_blocks(result.blocks))


if __name__ == "__main__":
    main()
