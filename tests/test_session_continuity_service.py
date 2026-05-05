from chanta_core.ocel.store import OCELStore
from chanta_core.session import SessionContinuityService, SessionService
from chanta_core.traces.trace_service import TraceService


def seed_session(trace_service: TraceService):
    session_service = SessionService(trace_service=trace_service)
    session = session_service.start_session(session_name="source")
    turn = session_service.start_turn(
        session_id=session.session_id,
        process_instance_id="process_instance:continuity",
    )
    user = session_service.record_user_message(
        session_id=session.session_id,
        turn_id=turn.turn_id,
        content="resume me",
    )
    assistant = session_service.record_assistant_message(
        session_id=session.session_id,
        turn_id=turn.turn_id,
        content="ready",
    )
    session_service.complete_turn(
        session_id=session.session_id,
        turn_id=turn.turn_id,
        user_message_id=user.message_id,
        assistant_message_id=assistant.message_id,
        process_instance_id="process_instance:continuity",
    )
    return session, turn, user, assistant


def test_resume_session_records_snapshot_reset_and_resume_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "resume.sqlite")
    trace_service = TraceService(ocel_store=store)
    session, *_ = seed_session(trace_service)
    service = SessionContinuityService(trace_service=trace_service)

    result = service.resume_session(session_id=session.session_id, max_messages=2)
    activities = [event["event_activity"] for event in store.fetch_recent_events(50)]

    assert result.permission_reset is True
    assert result.session_id == session.session_id
    assert result.snapshot.included_message_ids
    assert "session_resume_requested" in activities
    assert "session_context_snapshot_created" in activities
    assert "session_context_reconstructed" in activities
    assert "session_resumed" in activities
    assert "session_permissions_reset" in activities
    assert store.fetch_objects_by_type("session_context_snapshot")
    assert store.fetch_objects_by_type("session_resume")


def test_fork_session_creates_child_lineage_and_reset(tmp_path) -> None:
    store = OCELStore(tmp_path / "fork.sqlite")
    trace_service = TraceService(ocel_store=store)
    session, turn, user, _ = seed_session(trace_service)
    service = SessionContinuityService(trace_service=trace_service)

    result = service.fork_session(
        parent_session_id=session.session_id,
        fork_name="branch",
        from_turn_id=turn.turn_id,
        from_message_id=user.message_id,
        max_messages=2,
        reason="test fork",
    )
    activities = [event["event_activity"] for event in store.fetch_recent_events(80)]
    child_objects = [
        item
        for item in store.fetch_objects_by_type("session")
        if item["object_attrs"].get("forked_from_session_id") == session.session_id
    ]
    child_messages = [
        item
        for item in store.fetch_objects_by_type("message")
        if item["object_attrs"].get("session_id") == result.child_session_id
    ]

    assert result.permission_reset is True
    assert result.parent_session_id == session.session_id
    assert result.child_session_id != session.session_id
    assert child_objects
    assert child_messages == []
    assert "session_fork_requested" in activities
    assert "session_forked" in activities
    assert "session_permissions_reset" in activities
    assert store.fetch_objects_by_type("session_fork")
