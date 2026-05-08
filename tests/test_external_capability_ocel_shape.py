from chanta_core.external import ExternalCapabilityImportService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def test_external_capability_ocel_shape_contains_expected_objects_and_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "external_shape.sqlite")
    service = ExternalCapabilityImportService(trace_service=TraceService(ocel_store=store))
    source = service.register_source(
        source_name="provided dict",
        source_type="provided_dict",
        trust_level="untrusted",
    )
    batch = service.import_descriptors(
        raw_descriptors=[
            {
                "name": "external_file_writer",
                "type": "tool",
                "permissions": ["write_file", "shell"],
                "risks": ["filesystem_write", "shell_execution"],
                "entrypoint": "external.module:run",
            }
        ],
        source_id=source.source_id,
        batch_name="shape",
    )
    descriptor = service.import_descriptor(
        raw_descriptor={
            "name": "external_connector",
            "type": "connector",
            "permissions": ["network"],
            "risks": ["network_access"],
        },
        source_id=source.source_id,
    )
    normalization = service.normalize_descriptor(descriptor=descriptor)
    note = service.record_risk_note(
        descriptor_id=descriptor.descriptor_id,
        risk_level="medium",
        risk_categories=normalization.normalized_risk_categories,
        message="Review connector.",
    )
    candidate = service.create_assimilation_candidate(
        descriptor=descriptor,
        normalization=normalization,
        linked_risk_note_ids=[note.risk_note_id],
    )

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}
    assert {
        "external_capability_source_registered",
        "external_capability_descriptor_imported",
        "external_capability_import_started",
        "external_capability_import_completed",
        "external_capability_normalized",
        "external_assimilation_candidate_created",
        "external_capability_risk_note_recorded",
    }.issubset(activities)
    assert store.fetch_objects_by_type("external_capability_source")
    assert store.fetch_objects_by_type("external_capability_descriptor")
    assert store.fetch_objects_by_type("external_capability_import_batch")
    assert store.fetch_objects_by_type("external_capability_normalization_result")
    assert store.fetch_objects_by_type("external_assimilation_candidate")
    assert store.fetch_objects_by_type("external_capability_risk_note")
    assert store.fetch_object_object_relations_for_object(batch.batch_id)
    assert store.fetch_object_object_relations_for_object(normalization.normalization_id)
    assert store.fetch_object_object_relations_for_object(candidate.candidate_id)
    assert store.fetch_object_object_relations_for_object(note.risk_note_id)
