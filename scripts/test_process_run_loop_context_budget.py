from chanta_core.context import ContextBudget
from chanta_core.pig.context import PIGContext
from chanta_core.runtime.loop.context import ProcessContextAssembler


def main() -> None:
    pig_context = PIGContext(
        source="pig",
        scope="recent",
        process_instance_id="pi:script",
        session_id="session:script",
        activity_sequence=[],
        event_activity_counts={},
        object_type_counts={},
        relation_coverage={},
        basic_variant={},
        performance_summary={},
        guide={},
        diagnostics=[],
        recommendations=[],
        context_text="Process Intelligence Context:\n" + ("long context line\n" * 400),
    )
    assembler = ProcessContextAssembler()
    messages = assembler.assemble_for_llm_chat(
        user_input="script test",
        system_prompt="system",
        pig_context=pig_context,
        context_budget=ContextBudget(
            max_total_chars=1800,
            reserve_chars=200,
            max_pig_context_chars=500,
        ),
    )
    result = assembler.last_compaction_result
    print(f"message_count={len(messages)}")
    print(f"truncation_happened={bool(result and result.truncated_block_ids)}")
    print(f"after_chars={result.total_chars if result else 'unknown'}")
    print("--- messages ---")
    for message in messages:
        print(f"[{message['role']}] {message['content'][:300]}")


if __name__ == "__main__":
    main()
