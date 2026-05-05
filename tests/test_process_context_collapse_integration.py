from chanta_core.context import ContextBudget, make_context_block
from chanta_core.runtime.loop.context import ProcessContextAssembler


def test_process_context_assembler_renders_collapsed_context_without_llm() -> None:
    extra_blocks = [
        make_context_block(
            block_id=f"tool:{index}",
            block_type="tool_result",
            title=f"Tool {index}",
            content=f"raw-tool-{index}-" + ("x" * 900),
            priority=5 + index,
            source="tool",
            refs=[{"ref_type": "tool_result", "ref_id": f"tool:{index}"}],
        )
        for index in range(4)
    ]

    messages = ProcessContextAssembler().assemble_for_llm_chat(
        user_input="current request",
        system_prompt="system prompt",
        extra_blocks=extra_blocks,
        context_budget=ContextBudget(max_total_chars=1000, reserve_chars=100),
    )

    rendered = "\n".join(message["content"] for message in messages)
    assert "current request" in [
        message["content"] for message in messages if message["role"] == "user"
    ]
    assert "system prompt" in rendered
    assert "[collapsed_context] Collapsed Context References" in rendered
    assert "Raw content preserved in source stores" in rendered
    assert "raw-tool-0" not in rendered
