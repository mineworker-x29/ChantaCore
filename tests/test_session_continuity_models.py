from chanta_core.session import (
    SessionContextSnapshot,
    SessionForkRequest,
    SessionForkResult,
    SessionResumeRequest,
    SessionResumeResult,
    new_session_context_snapshot_id,
    new_session_fork_id,
    new_session_resume_id,
)


def make_snapshot() -> SessionContextSnapshot:
    return SessionContextSnapshot(
        snapshot_id=new_session_context_snapshot_id(),
        source_session_id="session:source",
        snapshot_type="resume",
        created_at="2026-01-01T00:00:00Z",
        max_turns=2,
        max_messages=4,
        included_turn_ids=["conversation_turn:1"],
        included_message_ids=["message:1"],
        process_instance_ids=["process_instance:1"],
        summary="test",
        context_entries=[{"role": "user", "content": "hello"}],
        snapshot_attrs={"k": "v"},
    )


def test_session_continuity_models_to_dict_and_ids() -> None:
    snapshot = make_snapshot()
    resume_request = SessionResumeRequest(
        session_id="session:source",
        max_turns=2,
        max_messages=4,
        include_system_messages=False,
        include_tool_messages=False,
        reason="continue",
    )
    resume_result = SessionResumeResult(
        session_id="session:source",
        snapshot=snapshot,
        permission_reset=True,
        resumed_at="2026-01-01T00:01:00Z",
    )
    fork_request = SessionForkRequest(
        parent_session_id="session:source",
        fork_name="fork",
        from_turn_id="conversation_turn:1",
        from_message_id="message:1",
        max_turns=2,
        max_messages=4,
        reason="branch",
    )
    fork_result = SessionForkResult(
        parent_session_id="session:source",
        child_session_id="session:child",
        snapshot=snapshot,
        permission_reset=True,
        forked_at="2026-01-01T00:02:00Z",
    )

    assert snapshot.to_dict()["snapshot_id"].startswith("session_context_snapshot:")
    assert resume_request.to_dict()["session_id"] == "session:source"
    assert resume_result.to_dict()["permission_reset"] is True
    assert fork_request.to_dict()["from_message_id"] == "message:1"
    assert fork_result.to_dict()["child_session_id"] == "session:child"
    assert new_session_resume_id().startswith("session_resume:")
    assert new_session_fork_id().startswith("session_fork:")
