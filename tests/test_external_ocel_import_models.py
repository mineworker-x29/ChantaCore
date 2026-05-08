from chanta_core.external.ids import (
    new_external_ocel_import_candidate_id,
    new_external_ocel_import_risk_note_id,
    new_external_ocel_payload_descriptor_id,
    new_external_ocel_preview_snapshot_id,
    new_external_ocel_source_id,
    new_external_ocel_validation_result_id,
)
from chanta_core.external.ocel_import import (
    ExternalOCELImportCandidate,
    ExternalOCELImportRiskNote,
    ExternalOCELPayloadDescriptor,
    ExternalOCELPreviewSnapshot,
    ExternalOCELSource,
    ExternalOCELValidationResult,
)
from chanta_core.utility.time import utc_now_iso


def test_external_ocel_model_to_dict_and_defaults() -> None:
    now = utc_now_iso()
    source = ExternalOCELSource(
        source_id=new_external_ocel_source_id(),
        source_name="provided",
        source_type="provided_dict",
        source_ref=None,
        trust_level="untrusted",
        status="active",
        created_at=now,
        updated_at=now,
    )
    descriptor = ExternalOCELPayloadDescriptor(
        descriptor_id=new_external_ocel_payload_descriptor_id(),
        source_id=source.source_id,
        payload_name="sample",
        payload_kind="ocel_like",
        declared_format="ocel_like",
        declared_schema_version=None,
        event_count=1,
        object_count=1,
        relation_count=1,
        raw_payload_ref=None,
        raw_payload_hash="abc",
        raw_payload_preview={"events": []},
        status="registered",
        created_at=now,
    )
    candidate = ExternalOCELImportCandidate(
        candidate_id=new_external_ocel_import_candidate_id(),
        descriptor_id=descriptor.descriptor_id,
        source_id=source.source_id,
        candidate_name="sample",
        created_at=now,
    )
    validation = ExternalOCELValidationResult(
        validation_id=new_external_ocel_validation_result_id(),
        descriptor_id=descriptor.descriptor_id,
        candidate_id=candidate.candidate_id,
        status="valid",
        schema_status="ocel_like",
        event_count=1,
        object_count=1,
        relation_count=1,
        missing_fields=[],
        warning_messages=[],
        error_messages=[],
        created_at=now,
    )
    preview = ExternalOCELPreviewSnapshot(
        preview_id=new_external_ocel_preview_snapshot_id(),
        descriptor_id=descriptor.descriptor_id,
        candidate_id=candidate.candidate_id,
        event_count=1,
        object_count=1,
        relation_count=1,
        event_activity_counts={"run": 1},
        object_type_counts={"case": 1},
        relation_type_counts={"related": 1},
        timestamp_min="2026-01-01T00:00:00Z",
        timestamp_max="2026-01-01T00:00:00Z",
        sample_event_ids=["e1"],
        sample_object_ids=["o1"],
        created_at=now,
    )
    risk = ExternalOCELImportRiskNote(
        risk_note_id=new_external_ocel_import_risk_note_id(),
        descriptor_id=descriptor.descriptor_id,
        candidate_id=candidate.candidate_id,
        risk_level="medium",
        risk_categories=["untrusted_source", "canonical_pollution_risk"],
        message="Review required.",
        review_required=True,
        created_at=now,
    )

    assert source.to_dict()["source_id"].startswith("external_ocel_source:")
    assert descriptor.to_dict()["descriptor_id"].startswith("external_ocel_payload_descriptor:")
    assert candidate.candidate_status == "pending_review"
    assert candidate.review_status == "pending_review"
    assert candidate.merge_status == "not_merged"
    assert candidate.canonical_import_enabled is False
    assert validation.to_dict()["validation_id"].startswith("external_ocel_validation_result:")
    assert preview.to_dict()["preview_id"].startswith("external_ocel_preview_snapshot:")
    assert risk.to_dict()["risk_note_id"].startswith("external_ocel_import_risk_note:")
