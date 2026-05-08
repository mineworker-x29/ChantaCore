from chanta_core.external.ocel_import import ExternalOCELImportCandidateService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def test_external_ocel_import_records_expected_ocel_shape(tmp_path) -> None:
    store = OCELStore(tmp_path / "external_ocel_shape.sqlite")
    service = ExternalOCELImportCandidateService(trace_service=TraceService(ocel_store=store))
    source = service.register_source(source_name="provided")
    service.register_as_candidate(
        payload={
            "events": [{"id": "e1", "activity": "start", "timestamp": "2026-01-01T00:00:00Z"}],
            "objects": [{"id": "o1", "type": "case"}],
            "relations": [{"type": "event_object", "event_id": "e1", "object_id": "o1"}],
        },
        source=source,
    )

    for object_type in [
        "external_ocel_source",
        "external_ocel_payload_descriptor",
        "external_ocel_import_candidate",
        "external_ocel_validation_result",
        "external_ocel_preview_snapshot",
        "external_ocel_import_risk_note",
    ]:
        assert store.fetch_objects_by_type(object_type)

    activities = {event["event_activity"] for event in store.fetch_recent_events(limit=20)}
    assert {
        "external_ocel_source_registered",
        "external_ocel_payload_registered",
        "external_ocel_validation_started",
        "external_ocel_validation_recorded",
        "external_ocel_preview_created",
        "external_ocel_candidate_created",
        "external_ocel_candidate_review_required",
        "external_ocel_risk_note_recorded",
    }.issubset(activities)

    candidate = store.fetch_objects_by_type("external_ocel_import_candidate")[0]
    assert candidate["object_attrs"]["canonical_import_enabled"] is False
    assert candidate["object_attrs"]["merge_status"] == "not_merged"
