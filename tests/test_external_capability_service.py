import pytest

from chanta_core.external import ExternalCapabilityImportService
from chanta_core.external.errors import ExternalAssimilationCandidateError
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def _sample_descriptor() -> dict:
    return {
        "name": "external_file_writer",
        "type": "tool",
        "description": "External file writer descriptor.",
        "permissions": ["write_file", "shell"],
        "risks": ["filesystem_write", "shell_execution"],
        "entrypoint": "external.module:run",
    }


def test_external_capability_service_records_import_flow(tmp_path) -> None:
    store = OCELStore(tmp_path / "external_service.sqlite")
    service = ExternalCapabilityImportService(trace_service=TraceService(ocel_store=store))

    source = service.register_source(
        source_name="provided dict",
        source_type="provided_dict",
        trust_level="untrusted",
    )
    descriptor = service.import_descriptor(raw_descriptor=_sample_descriptor(), source_id=source.source_id)
    batch = service.import_descriptors(raw_descriptors=[_sample_descriptor()], source_id=source.source_id)
    normalization = service.normalize_descriptor(descriptor=descriptor)
    note = service.record_risk_note(
        descriptor_id=descriptor.descriptor_id,
        risk_level="high",
        risk_categories=normalization.normalized_risk_categories,
        message="Review required.",
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
        "external_capability_risk_note_recorded",
        "external_assimilation_candidate_created",
    }.issubset(activities)
    assert descriptor.raw_descriptor["entrypoint"] == "external.module:run"
    assert descriptor.declared_entrypoint == "external.module:run"
    assert normalization.normalized_capability_type == "tool"
    assert "filesystem_write" in normalization.normalized_permissions
    assert candidate.execution_enabled is False
    assert candidate.activation_status == "disabled"
    assert batch.imported_descriptor_ids


def test_import_as_disabled_candidate_returns_disabled_candidate(tmp_path) -> None:
    store = OCELStore(tmp_path / "external_disabled.sqlite")
    service = ExternalCapabilityImportService(trace_service=TraceService(ocel_store=store))
    source = service.register_source(
        source_name="provided dict",
        source_type="provided_dict",
        trust_level="untrusted",
    )

    descriptor, normalization, candidate = service.import_as_disabled_candidate(
        raw_descriptor=_sample_descriptor(),
        source=source,
        recommended_next_step="manual review",
    )

    assert descriptor.status == "imported"
    assert normalization.status == "normalized"
    assert candidate.execution_enabled is False
    assert candidate.activation_status == "disabled"
    assert candidate.review_status == "pending_review"
    assert candidate.linked_risk_note_ids


def test_service_rejects_active_external_candidate(tmp_path) -> None:
    store = OCELStore(tmp_path / "external_active.sqlite")
    service = ExternalCapabilityImportService(trace_service=TraceService(ocel_store=store))
    descriptor = service.import_descriptor(raw_descriptor=_sample_descriptor())

    with pytest.raises(ExternalAssimilationCandidateError):
        service.create_assimilation_candidate(descriptor=descriptor, activation_status="active")


def test_invalid_descriptor_records_invalid_event(tmp_path) -> None:
    store = OCELStore(tmp_path / "external_invalid.sqlite")
    service = ExternalCapabilityImportService(trace_service=TraceService(ocel_store=store))

    with pytest.raises(Exception):
        service.import_descriptor(raw_descriptor=[])  # type: ignore[arg-type]

    activities = {event["event_activity"] for event in store.fetch_recent_events(20)}
    assert "external_capability_descriptor_invalid" in activities
