from chanta_core.session import SessionService


def main() -> None:
    service = SessionService()
    session = service.start_session(session_name="Script session", agent_id="script-agent")
    turn = service.start_turn(
        session_id=session.session_id,
        process_instance_id="process_instance:script-session",
        turn_index=1,
    )
    user_message = service.record_user_message(
        session_id=session.session_id,
        turn_id=turn.turn_id,
        content="Hello from session service script.",
    )
    assistant_message = service.record_assistant_message(
        session_id=session.session_id,
        turn_id=turn.turn_id,
        content="Hello from assistant.",
    )
    completed_turn = service.complete_turn(
        session_id=session.session_id,
        turn_id=turn.turn_id,
        user_message_id=user_message.message_id,
        assistant_message_id=assistant_message.message_id,
        process_instance_id="process_instance:script-session",
    )

    print(f"session_id={session.session_id}")
    print(f"turn_id={completed_turn.turn_id}")
    print(f"user_message_id={user_message.message_id}")
    print(f"assistant_message_id={assistant_message.message_id}")


if __name__ == "__main__":
    main()
