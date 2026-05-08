from chanta_core.capabilities import CapabilityDecisionSurfaceService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def test_capability_decision_records_ocel_shape(tmp_path) -> None:
    store = OCELStore(tmp_path / "capability_ocel.sqlite")
    service = CapabilityDecisionSurfaceService(
        trace_service=TraceService(ocel_store=store)
    )

    service.build_decision_surface("powershell 실행", session_id="session:test")

    object_types = {
        "capability_request_intent": store.fetch_objects_by_type("capability_request_intent"),
        "capability_requirement": store.fetch_objects_by_type("capability_requirement"),
        "capability_decision": store.fetch_objects_by_type("capability_decision"),
        "capability_decision_surface": store.fetch_objects_by_type("capability_decision_surface"),
        "capability_decision_evidence": store.fetch_objects_by_type("capability_decision_evidence"),
    }
    assert all(object_types.values())
    activities = {
        event["event_activity"] for event in store.fetch_recent_events(limit=20)
    }
    assert {
        "capability_request_intent_created",
        "capability_requirement_recorded",
        "capability_decision_evidence_recorded",
        "capability_decision_recorded",
        "capability_decision_surface_created",
        "capability_limitation_detected",
        "capability_request_unfulfillable",
    }.issubset(activities)
