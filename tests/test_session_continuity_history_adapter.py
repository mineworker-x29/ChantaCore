from chanta_core.session import (
    SessionContextSnapshot,
    session_context_snapshot_to_history_entries,
)


def test_session_context_snapshot_to_history_entries_preserves_roles_and_refs() -> None:
    snapshot = SessionContextSnapshot(
        snapshot_id="session_context_snapshot:test",
        source_session_id="session:source",
        snapshot_type="fork",
        created_at="2026-01-01T00:00:00Z",
        max_turns=None,
        max_messages=None,
        included_turn_ids=["conversation_turn:1"],
        included_message_ids=["message:1", "message:2"],
        process_instance_ids=[],
        summary=None,
        context_entries=[
            {
                "session_id": "session:source",
                "role": "user",
                "content": "hello",
                "created_at": "2026-01-01T00:00:01Z",
                "priority": 75,
                "refs": [],
                "entry_attrs": {"message_id": "message:1", "turn_id": "conversation_turn:1"},
            },
            {
                "session_id": "session:source",
                "role": "assistant",
                "content": "hi",
                "created_at": "2026-01-01T00:00:02Z",
                "priority": 60,
                "refs": [],
                "entry_attrs": {"message_id": "message:2", "turn_id": "conversation_turn:1"},
            },
        ],
    )

    entries = session_context_snapshot_to_history_entries(snapshot)

    assert [entry.role for entry in entries] == ["user", "assistant"]
    assert all(entry.source == "session_fork" for entry in entries)
    refs = entries[0].refs
    assert {"ref_type": "session_context_snapshot", "ref_id": snapshot.snapshot_id} in refs
    assert {"ref_type": "source_session", "ref_id": "session:source"} in refs
    assert {"ref_type": "message", "ref_id": "message:1"} in refs
    assert {"ref_type": "conversation_turn", "ref_id": "conversation_turn:1"} in refs
