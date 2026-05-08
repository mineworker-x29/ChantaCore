import sqlite3

from chanta_core.external.ocel_import import ExternalOCELImportCandidateService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def sample_payload() -> dict:
    return {
        "events": [
            {"id": "e1", "activity": "start", "timestamp": "2026-01-01T00:00:00Z"},
            {"id": "e2", "activity": "finish", "timestamp": "2026-01-01T00:01:00Z"},
        ],
        "objects": [{"id": "o1", "type": "case"}],
        "relations": [{"type": "event_object", "event_id": "e1", "object_id": "o1"}],
    }


def test_register_as_candidate_records_review_required_candidate_without_merge(tmp_path) -> None:
    store = OCELStore(tmp_path / "external_ocel_service.sqlite")
    service = ExternalOCELImportCandidateService(trace_service=TraceService(ocel_store=store))
    source = service.register_source(source_name="provided dict")

    descriptor, validation, preview, candidate = service.register_as_candidate(
        payload=sample_payload(),
        source=source,
        payload_name="sample external ocel",
    )

    assert descriptor.payload_kind == "ocel_like"
    assert validation.status == "valid"
    assert preview.event_count == 2
    assert preview.object_count == 1
    assert preview.relation_count == 1
    assert candidate.candidate_status == "pending_review"
    assert candidate.review_status == "pending_review"
    assert candidate.merge_status == "not_merged"
    assert candidate.canonical_import_enabled is False
    assert candidate.validation_result_ids == [validation.validation_id]
    assert candidate.preview_snapshot_ids == [preview.preview_id]
    assert candidate.risk_note_ids

    assert store.fetch_objects_by_type("external_ocel_source")
    assert store.fetch_objects_by_type("external_ocel_payload_descriptor")
    assert store.fetch_objects_by_type("external_ocel_validation_result")
    assert store.fetch_objects_by_type("external_ocel_preview_snapshot")
    assert store.fetch_objects_by_type("external_ocel_import_candidate")
    assert store.fetch_objects_by_type("external_ocel_import_risk_note")
    assert not store.fetch_objects_by_type("event")
    assert not store.fetch_objects_by_type("case")
    with sqlite3.connect(store.db_path) as connection:
        external_fact_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM chanta_object_state
            WHERE object_id IN ('e1', 'e2', 'o1')
            """
        ).fetchone()[0]
    assert int(external_fact_count) == 0


def test_invalid_payload_validation_is_structural_only(tmp_path) -> None:
    store = OCELStore(tmp_path / "external_ocel_invalid.sqlite")
    service = ExternalOCELImportCandidateService(trace_service=TraceService(ocel_store=store))
    descriptor = service.register_payload_descriptor(payload={"objects": []}, payload_name="invalid")

    validation = service.validate_payload(payload={"objects": []}, descriptor=descriptor)

    assert validation.status == "invalid"
    assert validation.schema_status == "invalid"
    assert "events" in validation.missing_fields
    assert store.fetch_event_count() >= 2
    assert not store.fetch_objects_by_type("process_instance")
