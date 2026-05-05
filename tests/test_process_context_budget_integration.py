from chanta_core.context import ContextBudget
from chanta_core.pig.context import PIGContext
from chanta_core.runtime.loop.context import ProcessContextAssembler


def make_long_pig_context() -> PIGContext:
    return PIGContext(
        source="pig",
        scope="recent",
        process_instance_id="pi:budget",
        session_id="session:budget",
        activity_sequence=[],
        event_activity_counts={},
        object_type_counts={},
        relation_coverage={},
        basic_variant={},
        performance_summary={},
        guide={},
        diagnostics=[],
        recommendations=[],
        context_text="Process Intelligence Context:\n" + ("x" * 2000),
    )


def test_long_pig_context_compacted_before_chat_message() -> None:
    assembler = ProcessContextAssembler()
    budget = ContextBudget(
        max_total_chars=1200,
        reserve_chars=100,
        max_pig_context_chars=300,
    )

    messages = assembler.assemble_for_llm_chat(
        user_input="hello",
        system_prompt="system",
        pig_context=make_long_pig_context(),
        context_budget=budget,
    )

    rendered = "\n".join(message["content"] for message in messages)
    assert "hello" in [message["content"] for message in messages if message["role"] == "user"]
    assert "system" in rendered
    assert "Process Intelligence Context" in rendered
    assert "content compacted/truncated by context pipeline" in rendered
    assert len(rendered) < 900
    assert assembler.last_compaction_result is not None
    assert assembler.last_compaction_result.truncated_block_ids
