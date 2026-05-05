from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.session import SessionService
from chanta_core.traces.trace_service import TraceService


def test_session_service_records_lifecycle_events_to_ocel(tmp_path) -> None:
    store = OCELStore(tmp_path / "session.sqlite")
    service = SessionService(trace_service=TraceService(ocel_store=store))

    session = service.start_session(session_name="Test", agent_id="agent:test")
    turn = service.start_turn(
        session_id=session.session_id,
        process_instance_id="process_instance:test",
        turn_index=1,
    )
    user_message = service.record_user_message(
        session_id=session.session_id,
        turn_id=turn.turn_id,
        content="hello",
    )
    assistant_message = service.record_assistant_message(
        session_id=session.session_id,
        turn_id=turn.turn_id,
        content="hi",
    )
    completed_turn = service.complete_turn(
        session_id=session.session_id,
        turn_id=turn.turn_id,
        user_message_id=user_message.message_id,
        assistant_message_id=assistant_message.message_id,
        process_instance_id="process_instance:test",
    )

    activities = [
        event["event_activity"]
        for event in store.fetch_events_by_session(session.session_id)
    ]

    assert completed_turn.status == "completed"
    assert "session_started" in activities
    assert "conversation_turn_started" in activities
    assert "process_instance_attached_to_turn" in activities
    assert "user_message_received" in activities
    assert "assistant_message_emitted" in activities
    assert "message_attached_to_turn" in activities
    assert "conversation_turn_completed" in activities
    assert store.fetch_objects_by_type("session")
    assert store.fetch_objects_by_type("conversation_turn")
    assert store.fetch_objects_by_type("message")
    assert OCELValidator(store).validate_duplicate_relations()["valid"] is True


def test_session_service_close_and_fail_turn(tmp_path) -> None:
    store = OCELStore(tmp_path / "session_fail.sqlite")
    service = SessionService(trace_service=TraceService(ocel_store=store))
    session = service.start_session(session_id="manual-session")
    turn = service.start_turn(session_id=session.session_id)

    service.fail_turn(
        session_id=session.session_id,
        turn_id=turn.turn_id,
        error="failed",
    )
    closed = service.close_session(session.session_id, reason="done")

    activities = [
        event["event_activity"]
        for event in store.fetch_events_by_session(session.session_id)
    ]

    assert closed.status == "closed"
    assert "conversation_turn_failed" in activities
    assert "session_closed" in activities
