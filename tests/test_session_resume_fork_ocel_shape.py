from chanta_core.ocel.store import OCELStore
from chanta_core.session import SessionContinuityService, SessionService
from chanta_core.traces.trace_service import TraceService


def test_resume_fork_ocel_shape(tmp_path) -> None:
    store = OCELStore(tmp_path / "continuity_shape.sqlite")
    trace_service = TraceService(ocel_store=store)
    session_service = SessionService(trace_service=trace_service)
    session = session_service.start_session(session_name="shape")
    user = session_service.record_user_message(
        session_id=session.session_id,
        turn_id=None,
        content="shape",
    )
    service = SessionContinuityService(trace_service=trace_service)

    resume = service.resume_session(session_id=session.session_id)
    fork = service.fork_session(
        parent_session_id=session.session_id,
        from_message_id=user.message_id,
    )

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}

    assert resume.snapshot.snapshot_id
    assert fork.snapshot.snapshot_id
    assert {
        "session_resume_requested",
        "session_context_snapshot_created",
        "session_context_reconstructed",
        "session_resumed",
        "session_fork_requested",
        "session_forked",
        "session_permissions_reset",
    }.issubset(activities)
    assert store.fetch_objects_by_type("session_context_snapshot")
    assert store.fetch_objects_by_type("session_resume")
    assert store.fetch_objects_by_type("session_fork")
    assert store.fetch_objects_by_type("session")
    child_relations = store.fetch_object_object_relations_for_object(
        fork.child_session_id
    ) or store.fetch_object_object_relations_for_object(
        f"session:{fork.child_session_id}"
    )
    assert any(item["qualifier"] == "forked_from_session" for item in child_relations)
