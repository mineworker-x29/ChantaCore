from chanta_core.ocel.store import OCELStore
from chanta_core.session import SessionContinuityService, SessionService
from chanta_core.traces.trace_service import TraceService


def main() -> None:
    store = OCELStore("data/session/test_session_continuity.sqlite")
    trace_service = TraceService(ocel_store=store)
    session_service = SessionService(trace_service=trace_service)

    session = session_service.start_session(session_name="continuity source")
    turn = session_service.start_turn(
        session_id=session.session_id,
        process_instance_id="process_instance:continuity-smoke",
    )
    user = session_service.record_user_message(
        session_id=session.session_id,
        turn_id=turn.turn_id,
        content="Resume and fork this session.",
    )
    assistant = session_service.record_assistant_message(
        session_id=session.session_id,
        turn_id=turn.turn_id,
        content="Session continuity substrate ready.",
    )
    session_service.complete_turn(
        session_id=session.session_id,
        turn_id=turn.turn_id,
        user_message_id=user.message_id,
        assistant_message_id=assistant.message_id,
        process_instance_id="process_instance:continuity-smoke",
    )

    continuity = SessionContinuityService(trace_service=trace_service)
    resume = continuity.resume_session(session_id=session.session_id, max_messages=4)
    fork = continuity.fork_session(
        parent_session_id=session.session_id,
        fork_name="continuity fork",
        from_turn_id=turn.turn_id,
        from_message_id=user.message_id,
        max_messages=4,
    )

    print(f"source_session_id={session.session_id}")
    print(f"resume_snapshot_id={resume.snapshot.snapshot_id}")
    print(f"resume_permission_reset={resume.permission_reset}")
    print(f"child_session_id={fork.child_session_id}")
    print(f"fork_snapshot_id={fork.snapshot.snapshot_id}")
    print(f"fork_permission_reset={fork.permission_reset}")
    print("recent continuity activities:")
    for event in store.fetch_recent_events(30):
        activity = event["event_activity"]
        if activity.startswith("session_"):
            print(f"- {activity}")


if __name__ == "__main__":
    main()
