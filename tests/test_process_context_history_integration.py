from chanta_core.context import (
    ContextBudget,
    ContextHistoryEntry,
    ContextHistoryPolicy,
    SessionContextPolicy,
)
from chanta_core.runtime.loop.context import ProcessContextAssembler


def history_entry(index: int, role: str, content: str, priority: int = 20) -> ContextHistoryEntry:
    return ContextHistoryEntry(
        entry_id=f"history:{index}",
        session_id="session:1",
        process_instance_id="pi:1",
        role=role,
        content=content,
        created_at=f"2026-05-05T00:{index:02d}:00Z",
        source="chat",
        priority=priority,
    )


def test_process_context_assembler_snips_old_history_without_llm() -> None:
    entries = [
        history_entry(1, "assistant", "old assistant" + ("a" * 400), priority=5),
        history_entry(2, "user", "old user" + ("u" * 400), priority=5),
        history_entry(3, "assistant", "recent assistant"),
        history_entry(4, "user", "recent user"),
    ]
    session_policy = SessionContextPolicy(
        session_id="session:1",
        process_instance_id="pi:1",
        history_policy=ContextHistoryPolicy(
            max_history_blocks=4,
            max_recent_history_blocks=4,
            preserve_last_user_blocks=1,
            preserve_last_assistant_blocks=1,
            min_priority_to_keep=50,
        ),
    )
    assembler = ProcessContextAssembler()

    messages = assembler.assemble_for_llm_chat(
        user_input="current request",
        system_prompt="system prompt",
        history_entries=entries,
        session_context_policy=session_policy,
        context_budget=ContextBudget(max_total_chars=550, reserve_chars=100),
    )

    rendered = "\n".join(message["content"] for message in messages)
    assert "system prompt" in rendered
    assert any(
        message["role"] == "user" and message["content"] == "current request"
        for message in messages
    )
    assert "recent assistant" in rendered
    assert "recent user" in rendered
    assert "old assistant" not in rendered
    assert "old user" not in rendered
    assert len(rendered) <= 900
    assert assembler.last_compaction_result is not None
    assert assembler.last_compaction_result.result_attrs["snipped_history_count"] == 2


def test_process_context_assembler_default_behavior_unchanged_without_history() -> None:
    messages = ProcessContextAssembler().assemble_for_llm_chat(
        user_input="hello",
        system_prompt="system",
    )

    assert messages == [
        {"role": "system", "content": "system"},
        {"role": "user", "content": "hello"},
    ]
