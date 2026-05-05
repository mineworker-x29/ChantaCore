from chanta_core.memory import MemoryService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def test_memory_service_records_memory_lifecycle_to_ocel(tmp_path) -> None:
    store = OCELStore(tmp_path / "memory.sqlite")
    service = MemoryService(trace_service=TraceService(ocel_store=store))

    memory = service.create_memory_entry(
        memory_type="semantic",
        title="Preference",
        content="ChantaCore memory is OCEL-native.",
        session_id="session:test",
        turn_id="conversation_turn:test",
        message_id="message:test",
    )
    revised, revision = service.revise_memory_entry(
        memory=memory,
        new_content="ChantaCore memory persists through OCEL.",
        reason="clarify",
    )
    archived = service.archive_memory_entry(memory=revised, reason="test")

    activities = [event["event_activity"] for event in store.fetch_recent_events(20)]

    assert archived.status == "archived"
    assert revision.operation == "revise"
    assert "memory_entry_created" in activities
    assert "memory_revision_recorded" in activities
    assert "memory_derived_from_message" in activities
    assert "memory_entry_revised" in activities
    assert "memory_entry_archived" in activities
    assert store.fetch_objects_by_type("memory_entry")
    assert store.fetch_objects_by_type("memory_revision")


def test_memory_service_attachment_and_withdraw_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "memory_attach.sqlite")
    service = MemoryService(trace_service=TraceService(ocel_store=store))
    memory = service.create_memory_entry(
        memory_type="operational",
        title="Attach",
        content="Attach me.",
    )

    service.attach_memory_to_session(memory_id=memory.memory_id, session_id="session:test")
    service.attach_memory_to_turn(
        memory_id=memory.memory_id,
        session_id="session:test",
        turn_id="conversation_turn:test",
    )
    withdrawn = service.withdraw_memory_entry(memory=memory, reason="test")

    activities = [event["event_activity"] for event in store.fetch_recent_events(20)]

    assert withdrawn.status == "withdrawn"
    assert "memory_attached_to_session" in activities
    assert "memory_attached_to_turn" in activities
    assert "memory_entry_withdrawn" in activities
