from dataclasses import fields

from chanta_core.ocel.models import OCELObject, OCELRecord, OCELEvent, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator


def make_record() -> OCELRecord:
    event = OCELEvent(
        event_id="evt:test",
        event_activity="receive_user_request",
        event_timestamp="2026-05-02T00:00:00Z",
        event_attrs={
            "runtime_event_type": "test_event",
            "source_runtime": "pytest",
            "session_id": "session-test",
            "actor_id": "agent-test",
            "lifecycle": "completed",
        },
    )
    session = OCELObject(
        object_id="session:session-test",
        object_type="session",
        object_attrs={
            "object_key": "session-test",
            "display_name": "Test session",
            "created_at": "2026-05-02T00:00:00Z",
        },
    )
    agent = OCELObject(
        object_id="agent:agent-test",
        object_type="agent",
        object_attrs={
            "object_key": "agent-test",
            "display_name": "Test agent",
            "created_at": "2026-05-02T00:00:00Z",
        },
    )
    return OCELRecord(
        event=event,
        objects=[session, agent],
        relations=[
            OCELRelation.event_object(
                event_id=event.event_id,
                object_id=session.object_id,
                qualifier="session_context",
            ),
            OCELRelation.object_object(
                source_object_id=agent.object_id,
                target_object_id=session.object_id,
                qualifier="created_by_agent",
            ),
        ],
    )


def test_ocel_event_uses_minimal_canonical_fields() -> None:
    field_names = {field.name for field in fields(OCELEvent)}

    assert field_names == {
        "event_id",
        "event_activity",
        "event_timestamp",
        "event_attrs",
    }
    assert "event_type" not in field_names
    assert "source_runtime" not in field_names
    assert "session_id" not in field_names
    assert "actor_id" not in field_names
    assert "status" not in field_names


def test_ocel_object_uses_minimal_canonical_fields() -> None:
    field_names = {field.name for field in fields(OCELObject)}

    assert field_names == {"object_id", "object_type", "object_attrs"}

    obj = OCELObject(
        object_id="session:test",
        object_type="session",
        object_attrs={"object_key": "test", "display_name": "Test"},
    )
    assert obj.object_attrs["object_key"] == "test"
    assert obj.object_attrs["display_name"] == "Test"


def test_ocel_store_appends_record(tmp_path) -> None:
    store = OCELStore(tmp_path / "test.sqlite")
    store.initialize()
    store.append_record(make_record())

    assert store.fetch_event_count() == 1
    assert store.fetch_object_count() >= 1
    assert store.fetch_event_object_relation_count() >= 1


def test_append_same_record_does_not_duplicate_relations(tmp_path) -> None:
    store = OCELStore(tmp_path / "test.sqlite")
    record = make_record()

    store.append_record(record)
    store.append_record(record)

    assert store.fetch_event_count() == 1
    assert store.fetch_object_count() == 2
    assert store.fetch_event_object_relation_count() == 1
    assert store.fetch_object_object_relation_count() == 1
    assert OCELValidator(store).validate_duplicate_relations()["valid"] is True
