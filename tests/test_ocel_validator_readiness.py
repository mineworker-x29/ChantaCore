from chanta_core.ocel.models import OCELObject, OCELRecord, OCELRelation, OCELEvent
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator


def test_validate_canonical_model_and_export_readiness(tmp_path) -> None:
    store = OCELStore(tmp_path / "ready.sqlite")
    event = OCELEvent(
        event_id="event:ready",
        event_activity="receive_user_request",
        event_timestamp="2026-05-03T00:00:00Z",
        event_attrs={},
    )
    obj = OCELObject("session:ready", "session", {})
    store.append_record(
        OCELRecord(
            event=event,
            objects=[obj],
            relations=[
                OCELRelation.event_object(
                    event_id=event.event_id,
                    object_id=obj.object_id,
                    qualifier="session_context",
                )
            ],
        )
    )
    validator = OCELValidator(store)

    canonical = validator.validate_canonical_model()
    readiness = validator.validate_export_readiness()

    assert canonical["valid"] is True
    assert canonical["canonical_event_model"] == "event_activity/event_timestamp/event_attrs_json"
    assert readiness["valid"] is True
    assert readiness["event_count"] == 1
    assert readiness["object_count"] == 1
    assert readiness["relation_count"] == 1
    assert readiness["malformed_attrs_json_count"] == 0
