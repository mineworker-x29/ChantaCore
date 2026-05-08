from chanta_core.ocel.store import OCELStore
from chanta_core.session import ChatSessionContextPolicy, SessionContextAssembler
from chanta_core.session.models import SessionMessage
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


def _message(message_id: str, content: str) -> SessionMessage:
    return SessionMessage(
        message_id=message_id,
        session_id="session:test",
        turn_id=None,
        role="user",
        content=content,
        content_preview=content,
        content_hash=message_id,
        created_at=f"2026-01-01T00:00:0{message_id[-1]}+00:00",
        message_attrs={},
    )


def test_context_projection_records_ocel_objects_and_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "ocel.sqlite")
    assembler = SessionContextAssembler(trace_service=TraceService(ocel_store=store))
    policy = ChatSessionContextPolicy(
        policy_id="session_context_policy:test",
        policy_name="test",
        max_turns=8,
        max_messages=1,
        max_chars=12000,
        include_user_messages=True,
        include_assistant_messages=True,
        include_system_messages=False,
        include_tool_messages=False,
        strategy="recent_only",
        status="active",
        created_at=utc_now_iso(),
        policy_attrs={"canonical": False},
    )

    projection = assembler.assemble_projection_from_messages(
        session_id="session:test",
        messages=[_message("message:1", "one"), _message("message:2", "two")],
        policy=policy,
    )
    assembler.render_projection_to_llm_messages(
        projection=projection,
        system_prompt="system",
        current_user_message="current",
    )

    event_counts = {
        event["event_activity"]: event["event_attrs"]
        for event in store.fetch_recent_events(limit=20)
    }
    object_types = {
        item["object_type"] for item in store.fetch_objects_by_type("session_context_projection")
    }
    assert "session_context_projection_created" in event_counts
    assert "session_context_projection_truncated" in event_counts
    assert "session_prompt_rendered" in event_counts
    assert "session_context_projection" in object_types
    stored_projection = store.fetch_objects_by_type("session_context_projection")[0]
    assert stored_projection["object_attrs"]["canonical"] is False
