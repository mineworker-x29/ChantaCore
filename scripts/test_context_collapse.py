from chanta_core.context import ContextBudget, ContextCompactionPipeline, ContextRenderer
from chanta_core.context.block import make_context_block


def long_block(index: int, block_type: str):
    return make_context_block(
        block_id=f"{block_type}:{index}",
        block_type=block_type,
        title=f"{block_type} {index}",
        content=f"raw-{block_type}-{index}-" + ("x" * 900),
        priority=5 + index,
        source=block_type,
        refs=[{"ref_type": block_type, "ref_id": f"{block_type}:{index}"}],
    )


def main() -> None:
    blocks = [
        make_context_block(
            block_type="system",
            title="System Prompt",
            content="system",
            priority=100,
            source="script",
        ),
        *[long_block(index, "tool_result") for index in range(3)],
        *[long_block(index, "repo") for index in range(3)],
        make_context_block(
            block_type="user_request",
            title="User Request",
            content="current request",
            priority=100,
            source="script",
        ),
    ]
    result = ContextCompactionPipeline.default().run(
        blocks,
        ContextBudget(max_total_chars=1200, reserve_chars=150),
    )
    for layer_result in result.layer_results:
        print(
            f"{layer_result.layer_name}: changed={layer_result.changed} "
            f"dropped={len(layer_result.dropped_block_ids)} "
            f"created={len(layer_result.created_block_ids)} "
            f"attrs={layer_result.result_attrs}"
        )
    collapsed = [block for block in result.blocks if block.block_type == "collapsed_context"]
    print(f"collapsed_manifest_blocks={len(collapsed)}")
    if collapsed:
        print("--- collapsed manifest block ---")
        print(collapsed[0].content)
    print("--- rendered context ---")
    print(ContextRenderer().render_blocks(result.blocks))


if __name__ == "__main__":
    main()
