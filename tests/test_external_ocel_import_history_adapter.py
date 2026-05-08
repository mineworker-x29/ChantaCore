from chanta_core.external.history_adapter import (
    external_ocel_candidates_to_history_entries,
    external_ocel_preview_snapshots_to_history_entries,
    external_ocel_risk_notes_to_history_entries,
    external_ocel_validation_results_to_history_entries,
)
from chanta_core.external.ocel_import import ExternalOCELImportCandidateService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def test_external_ocel_history_adapters_convert_records(tmp_path) -> None:
    store = OCELStore(tmp_path / "external_ocel_history.sqlite")
    service = ExternalOCELImportCandidateService(trace_service=TraceService(ocel_store=store))
    descriptor, validation, preview, candidate = service.register_as_candidate(
        payload={
            "events": [{"id": "e1", "activity": "start"}],
            "objects": [{"id": "o1", "type": "case"}],
            "relations": [],
        },
        payload_name="history payload",
    )
    risk = service.record_risk_note(
        descriptor_id=descriptor.descriptor_id,
        candidate_id=candidate.candidate_id,
        risk_level="high",
        risk_categories=["unknown_schema"],
        message="Review.",
    )

    candidate_entry = external_ocel_candidates_to_history_entries([candidate])[0]
    validation_entry = external_ocel_validation_results_to_history_entries([validation])[0]
    preview_entry = external_ocel_preview_snapshots_to_history_entries([preview])[0]
    risk_entry = external_ocel_risk_notes_to_history_entries([risk])[0]

    assert candidate_entry.source == "external_ocel_import"
    assert candidate_entry.refs[0]["candidate_id"] == candidate.candidate_id
    assert candidate_entry.entry_attrs["canonical_import_enabled"] is False
    assert validation_entry.refs[0]["validation_id"] == validation.validation_id
    assert preview_entry.refs[0]["preview_id"] == preview.preview_id
    assert risk_entry.refs[0]["risk_note_id"] == risk.risk_note_id
    assert risk_entry.priority == 90
