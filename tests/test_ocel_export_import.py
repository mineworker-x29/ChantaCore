import json

from chanta_core.ocel.export import OCELExporter
from chanta_core.ocel.external_import import ExternalOCELIngestionService
from chanta_core.ocel.external_source import ExternalOCELSource
from chanta_core.ocel.importers import OCELImporter
from chanta_core.ocel.models import OCELObject, OCELRecord, OCELRelation, OCELEvent
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator


def record() -> OCELRecord:
    event = OCELEvent(
        event_id="event:export-import",
        event_activity="receive_user_request",
        event_timestamp="2026-05-03T00:00:00Z",
        event_attrs={"source_runtime": "pytest"},
    )
    session = OCELObject(
        object_id="session:export-import",
        object_type="session",
        object_attrs={"name": "export-import"},
    )
    agent = OCELObject(
        object_id="agent:export-import",
        object_type="agent",
        object_attrs={"name": "agent"},
    )
    return OCELRecord(
        event=event,
        objects=[session, agent],
        relations=[
            OCELRelation.event_object(
                event_id=event.event_id,
                object_id=session.object_id,
                qualifier="session_context",
                relation_attrs={"kind": "test"},
            ),
            OCELRelation.object_object(
                source_object_id=agent.object_id,
                target_object_id=session.object_id,
                qualifier="created_by_agent",
                relation_attrs={"kind": "test"},
            ),
        ],
    )


def test_chanta_json_export_import_round_trip(tmp_path) -> None:
    source_store = OCELStore(tmp_path / "source.sqlite")
    source_store.append_record(record())
    export_path = tmp_path / "export" / "chanta_ocel.json"

    OCELExporter(source_store).export_chanta_json(export_path)
    payload = json.loads(export_path.read_text(encoding="utf-8"))

    assert payload["format"] == "chanta_ocel_json"
    assert payload["export_attrs"]["full_ocel2_json"] is False
    assert "event_activity" in payload["events"][0]
    assert "event_type" not in payload["events"][0]
    assert "object_attrs" in payload["objects"][0]
    assert "object_key" not in payload["objects"][0]
    assert "relation_attrs" in payload["relations"][0]

    target_store = OCELStore(tmp_path / "target.sqlite")
    result = OCELImporter(target_store).import_chanta_json(export_path)

    assert result.success is True
    assert target_store.fetch_event_count() == source_store.fetch_event_count()
    assert target_store.fetch_object_count() == source_store.fetch_object_count()
    assert target_store.fetch_event_object_relation_count() == source_store.fetch_event_object_relation_count()
    assert target_store.fetch_object_object_relation_count() == source_store.fetch_object_object_relation_count()
    imported_event = target_store.fetch_recent_events(1)[0]
    assert imported_event["event_attrs"]["imported_from_chanta_json"] is True
    imported_object = target_store.fetch_objects_by_type("session")[0]
    assert imported_object["object_attrs"]["imported_from_chanta_json"] is True
    related = target_store.fetch_related_objects_for_event("event:export-import")
    assert related[0]["relation_attrs"]["imported_from_chanta_json"] is True
    assert OCELValidator(target_store).validate_duplicate_relations()["valid"] is True


def test_external_ingestion_service_accepts_chanta_json_export(tmp_path) -> None:
    source_store = OCELStore(tmp_path / "external-source.sqlite")
    source_store.append_record(record())
    export_path = OCELExporter(source_store).export_chanta_json(tmp_path / "external.json")
    target_store = OCELStore(tmp_path / "external-target.sqlite")
    source = ExternalOCELSource(
        source_id="external-test",
        source_name="external-test",
        source_type="file",
        source_format="chanta_ocel_json",
    )

    result = ExternalOCELIngestionService(store=target_store).ingest_json_file(
        source,
        export_path,
    )

    assert result.success is True
    assert target_store.fetch_event_count() == source_store.fetch_event_count()
