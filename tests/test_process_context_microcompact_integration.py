from chanta_core.context import ContextBudget, make_context_block
from chanta_core.pig.context import PIGContext
from chanta_core.runtime.loop.context import ProcessContextAssembler


def test_process_context_assembler_microcompacts_extra_blocks_without_llm() -> None:
    pig_context = PIGContext(
        source="pig",
        scope="recent",
        process_instance_id="pi:micro",
        session_id="session:micro",
        activity_sequence=[f"a{index}" for index in range(80)],
        event_activity_counts={},
        object_type_counts={},
        relation_coverage={},
        basic_variant={},
        performance_summary={},
        guide={},
        diagnostics=[],
        recommendations=[],
        context_text="\n".join(f"pig line {index}" for index in range(100)),
    )
    extra_blocks = [
        make_context_block(
            block_type="tool_result",
            title="Tool",
            content='{"b": [1, 2, 3], "a": {"nested": true}}',
            priority=40,
            source="tool",
        ),
        make_context_block(
            block_type="repo",
            title="Repo",
            content="\n".join(f"match-{index}" for index in range(120)),
            priority=60,
            source="repo",
        ),
    ]

    messages = ProcessContextAssembler().assemble_for_llm_chat(
        user_input="current request",
        system_prompt="system prompt",
        pig_context=pig_context,
        extra_blocks=extra_blocks,
        context_budget=ContextBudget(max_total_chars=2000, reserve_chars=200),
    )

    rendered = "\n".join(message["content"] for message in messages)
    assert "current request" in [
        message["content"] for message in messages if message["role"] == "user"
    ]
    assert "system prompt" in rendered
    assert "microcompacted=True" in rendered
    assert "activities omitted" in rendered
