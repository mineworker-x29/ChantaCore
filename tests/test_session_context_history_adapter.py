from chanta_core.session import SessionMessage, hash_content, session_messages_to_history_entries


def test_session_messages_to_history_entries_preserves_roles_and_refs() -> None:
    messages = [
        SessionMessage(
            message_id="message:user",
            session_id="session:test",
            turn_id="conversation_turn:test",
            role="user",
            content="hello",
            content_preview="hello",
            content_hash=hash_content("hello"),
            created_at="2026-05-05T00:00:00Z",
        ),
        SessionMessage(
            message_id="message:assistant",
            session_id="session:test",
            turn_id="conversation_turn:test",
            role="assistant",
            content="hi",
            content_preview="hi",
            content_hash=hash_content("hi"),
            created_at="2026-05-05T00:00:01Z",
        ),
    ]

    entries = session_messages_to_history_entries(messages)

    assert [entry.role for entry in entries] == ["user", "assistant"]
    assert entries[0].source == "session"
    assert entries[0].session_id == "session:test"
    assert {ref["ref_id"] for ref in entries[0].refs} == {
        "message:user",
        "session:test",
        "conversation_turn:test",
    }
    assert entries[0].priority > entries[1].priority
