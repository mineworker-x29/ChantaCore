from chanta_core.ocel.external_import import ExternalOCELIngestionService
from chanta_core.ocel.external_source import ExternalOCELSource
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.ocpx.loader import OCPXLoader


def raw_external_record() -> dict:
    return {
        "event": {
            "event_id": "evt-1",
            "event_activity": "external_receive_request",
            "event_timestamp": "2026-05-03T00:00:00Z",
            "event_attrs": {"external_status": "done"},
        },
        "objects": [
            {
                "object_id": "case-1",
                "object_type": "case",
                "object_attrs": {"display_name": "Case 1"},
            }
        ],
        "relations": [
            {
                "relation_kind": "event_object",
                "source_id": "evt-1",
                "target_id": "case-1",
                "qualifier": "case_context",
                "relation_attrs": {"weight": 1},
            }
        ],
    }


def external_source() -> ExternalOCELSource:
    return ExternalOCELSource(
        source_id="source-a",
        source_name="Source A",
        source_type="manual_test_log",
        source_format="chanta_ocel_json",
        source_attrs={"purpose": "test"},
    )


def test_external_ocel_ingestion_namespaces_and_preserves_provenance(tmp_path) -> None:
    store = OCELStore(tmp_path / "external_ingestion.sqlite")
    service = ExternalOCELIngestionService(store=store)

    result = service.ingest_records(external_source(), [raw_external_record()])

    assert result.success is True
    assert result.batch.records_accepted == 1
    assert result.batch.records_rejected == 0
    assert result.accepted_record_ids == ["external:source-a:event:evt-1"]
    assert store.fetch_event_count() == 1
    assert store.fetch_object_count() >= 1

    view = OCPXLoader(store).load_recent_view(limit=10)
    event = view.events[0]
    assert event.event_id == "external:source-a:event:evt-1"
    assert event.event_attrs["external_event_id"] == "evt-1"
    assert event.event_attrs["external_source_id"] == "source-a"
    assert event.event_attrs["imported"] is True
    assert view.objects[0].object_id == "external:source-a:object:case-1"
    assert view.objects[0].object_attrs["external_object_id"] == "case-1"
    assert view.objects[0].object_attrs["imported"] is True
    assert event.related_objects[0]["relation_attrs"]["external_source_id"] == "source-a"
    assert OCELValidator(store).validate_duplicate_relations()["valid"] is True


def test_external_ocel_ingestion_rejects_invalid_rows_without_batch_crash(tmp_path) -> None:
    store = OCELStore(tmp_path / "external_ingestion_invalid.sqlite")
    service = ExternalOCELIngestionService(store=store)
    invalid = {"event": {"event_id": "bad"}}

    result = service.ingest_records(external_source(), [raw_external_record(), invalid])

    assert result.success is True
    assert result.batch.records_seen == 2
    assert result.batch.records_accepted == 1
    assert result.batch.records_rejected == 1
    assert len(result.rejected_records) == 1
    assert store.fetch_event_count() == 1
