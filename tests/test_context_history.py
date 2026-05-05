from chanta_core.context import (
    ContextHistoryEntry,
    history_entry_to_context_block,
    new_context_history_entry_id,
)


def test_context_history_entry_to_dict() -> None:
    entry = ContextHistoryEntry(
        entry_id="history:1",
        session_id="session:1",
        process_instance_id="pi:1",
        role="assistant",
        content="answer",
        created_at="2026-05-05T00:00:00Z",
        source="chat",
        priority=60,
        refs=[{"event_id": "e:1"}],
        entry_attrs={"turn": 1},
    )

    data = entry.to_dict()

    assert data["entry_id"] == "history:1"
    assert data["refs"] == [{"event_id": "e:1"}]
    assert data["entry_attrs"] == {"turn": 1}


def test_history_entry_to_context_block_preserves_refs_and_attrs() -> None:
    entry = ContextHistoryEntry(
        entry_id="history:2",
        session_id="session:1",
        process_instance_id="pi:1",
        role="assistant",
        content="answer",
        created_at="2026-05-05T00:01:00Z",
        source="chat",
        priority=60,
        refs=[{"event_id": "e:2"}],
    )

    block = history_entry_to_context_block(entry)

    assert block.block_type == "history"
    assert block.title == "History: assistant / chat"
    assert block.content == "answer"
    assert block.priority == 60
    assert block.refs == [{"event_id": "e:2"}]
    assert block.block_attrs["session_id"] == "session:1"
    assert block.block_attrs["process_instance_id"] == "pi:1"
    assert block.block_attrs["created_at"] == "2026-05-05T00:01:00Z"
    assert block.block_attrs["role"] == "assistant"
    assert block.block_attrs["is_history"] is True


def test_new_context_history_entry_id() -> None:
    assert new_context_history_entry_id().startswith("context_history_entry:")
