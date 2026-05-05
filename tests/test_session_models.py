from chanta_core.session import (
    AgentSession,
    ConversationTurn,
    SessionMessage,
    hash_content,
    new_conversation_turn_id,
    new_session_id,
    new_session_message_id,
)


def test_session_ids_use_expected_prefixes() -> None:
    assert new_session_id().startswith("session:")
    assert new_conversation_turn_id().startswith("conversation_turn:")
    assert new_session_message_id().startswith("message:")


def test_hash_content_is_deterministic() -> None:
    assert hash_content("hello") == hash_content("hello")
    assert hash_content("hello") != hash_content("world")


def test_agent_session_to_dict() -> None:
    session = AgentSession(
        session_id="session:test",
        session_name="Test",
        status="active",
        created_at="2026-05-05T00:00:00Z",
        updated_at="2026-05-05T00:00:00Z",
        closed_at=None,
        agent_id="agent:test",
    )

    assert session.to_dict()["session_id"] == "session:test"


def test_conversation_turn_to_dict() -> None:
    turn = ConversationTurn(
        turn_id="conversation_turn:test",
        session_id="session:test",
        status="started",
        started_at="2026-05-05T00:00:00Z",
        completed_at=None,
        process_instance_id="process_instance:test",
        user_message_id=None,
        assistant_message_id=None,
        turn_index=1,
    )

    assert turn.to_dict()["process_instance_id"] == "process_instance:test"


def test_session_message_to_dict() -> None:
    message = SessionMessage(
        message_id="message:test",
        session_id="session:test",
        turn_id="conversation_turn:test",
        role="user",
        content="hello",
        content_preview="hello",
        content_hash=hash_content("hello"),
        created_at="2026-05-05T00:00:00Z",
    )

    data = message.to_dict()

    assert data["role"] == "user"
    assert data["content_hash"] == hash_content("hello")
