from pathlib import Path

from chanta_core.ocel.store import OCELStore
from chanta_core.session import SessionContinuityService, SessionService
from chanta_core.traces.trace_service import TraceService


def test_session_continuity_source_avoids_forbidden_replay_and_restore_terms() -> None:
    text = Path("src/chanta_core/session/continuity.py").read_text(encoding="utf-8")

    assert "replay_jsonl" not in text
    assert "transcript.jsonl" not in text
    assert "restore_permissions" not in text
    assert "restore_grants" not in text
    assert "restore_approval" not in text
    assert "load_markdown_as_session" not in text
    assert "sync_markdown_to_session" not in text
    assert "connector_state_restore" not in text
    assert "mcp_state_restore" not in text
    assert "plugin_state_restore" not in text


def test_fork_does_not_duplicate_parent_messages_as_child_canonical_messages(tmp_path) -> None:
    store = OCELStore(tmp_path / "continuity_boundary.sqlite")
    trace_service = TraceService(ocel_store=store)
    session_service = SessionService(trace_service=trace_service)
    session = session_service.start_session()
    session_service.record_user_message(
        session_id=session.session_id,
        turn_id=None,
        content="parent only",
    )
    service = SessionContinuityService(trace_service=trace_service)

    fork = service.fork_session(parent_session_id=session.session_id)
    child_messages = [
        item
        for item in store.fetch_objects_by_type("message")
        if item["object_attrs"].get("session_id") == fork.child_session_id
    ]

    assert child_messages == []
