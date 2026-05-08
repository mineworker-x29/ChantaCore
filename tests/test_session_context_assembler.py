from chanta_core.ocel.store import OCELStore
from chanta_core.session import ChatSessionContextPolicy, SessionContextAssembler
from chanta_core.session.models import ConversationTurn, SessionMessage
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


def _message(
    message_id: str,
    *,
    session_id: str = "session:one",
    turn_id: str | None = None,
    role: str = "user",
    content: str = "content",
    created_at: str = "2026-01-01T00:00:00+00:00",
) -> SessionMessage:
    return SessionMessage(
        message_id=message_id,
        session_id=session_id,
        turn_id=turn_id,
        role=role,
        content=content,
        content_preview=content,
        content_hash=f"hash:{message_id}",
        created_at=created_at,
        message_attrs={},
    )


def _turn(turn_id: str, started_at: str) -> ConversationTurn:
    return ConversationTurn(
        turn_id=turn_id,
        session_id="session:one",
        status="completed",
        started_at=started_at,
        completed_at=started_at,
        process_instance_id=None,
        user_message_id=None,
        assistant_message_id=None,
        turn_index=None,
        turn_attrs={},
    )


def _policy(**kwargs) -> ChatSessionContextPolicy:
    values = {
        "policy_id": "session_context_policy:test",
        "policy_name": "test",
        "max_turns": 8,
        "max_messages": 16,
        "max_chars": 12000,
        "include_user_messages": True,
        "include_assistant_messages": True,
        "include_system_messages": False,
        "include_tool_messages": False,
        "strategy": "recent_only",
        "status": "active",
        "created_at": utc_now_iso(),
        "policy_attrs": {"canonical": False},
    }
    values.update(kwargs)
    return ChatSessionContextPolicy(**values)


def test_assembler_filters_roles_session_and_excludes_current(tmp_path) -> None:
    assembler = SessionContextAssembler(
        trace_service=TraceService(ocel_store=OCELStore(tmp_path / "ocel.sqlite"))
    )
    messages = [
        _message("message:other", session_id="session:other", content="other"),
        _message("message:system", role="system", content="system"),
        _message("message:tool", role="tool", content="tool"),
        _message("message:user", role="user", content="hello"),
        _message("message:assistant", role="assistant", content="hi"),
        _message("message:current", role="user", content="now"),
    ]

    projection = assembler.assemble_projection_from_messages(
        session_id="session:one",
        messages=messages,
        policy=_policy(),
        exclude_message_ids=["message:current"],
    )

    assert [item["content"] for item in projection.rendered_messages] == ["hello", "hi"]
    assert projection.source_message_ids == ["message:user", "message:assistant"]
    assert projection.projection_attrs["scrollback_source"] is False


def test_assembler_enforces_max_messages_and_chars(tmp_path) -> None:
    assembler = SessionContextAssembler(
        trace_service=TraceService(ocel_store=OCELStore(tmp_path / "ocel.sqlite"))
    )
    messages = [
        _message(f"message:{index}", content=f"message-{index}", created_at=f"2026-01-01T00:00:0{index}+00:00")
        for index in range(5)
    ]

    projection = assembler.assemble_projection_from_messages(
        session_id="session:one",
        messages=messages,
        policy=_policy(max_messages=3, max_chars=18),
    )

    assert projection.truncated is True
    assert set(projection.truncation_reason.split(",")) == {"max_messages", "max_chars"}
    assert projection.total_messages == 2
    assert [item["content"] for item in projection.rendered_messages] == [
        "message-3",
        "message-4",
    ]


def test_assembler_enforces_max_turns(tmp_path) -> None:
    assembler = SessionContextAssembler(
        trace_service=TraceService(ocel_store=OCELStore(tmp_path / "ocel.sqlite"))
    )
    turns = [
        _turn("conversation_turn:one", "2026-01-01T00:00:00+00:00"),
        _turn("conversation_turn:two", "2026-01-01T00:00:01+00:00"),
    ]
    messages = [
        _message("message:old", turn_id="conversation_turn:one", content="old"),
        _message("message:new", turn_id="conversation_turn:two", content="new"),
    ]

    projection = assembler.assemble_projection_from_messages(
        session_id="session:one",
        messages=messages,
        turns=turns,
        policy=_policy(max_turns=1),
    )

    assert projection.source_turn_ids == ["conversation_turn:two"]
    assert [item["content"] for item in projection.rendered_messages] == ["new"]
