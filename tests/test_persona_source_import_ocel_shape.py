from chanta_core.ocel.store import OCELStore
from chanta_core.persona import PersonaSourceStagedImportService
from chanta_core.traces.trace_service import TraceService


def test_persona_source_import_ocel_shape_contains_expected_objects_and_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "persona_source_import.sqlite")
    service = PersonaSourceStagedImportService(trace_service=TraceService(ocel_store=store))
    source = service.register_source_from_text(
        source_name="profile.md",
        text="identity: public dummy",
        source_ref="profile.md",
        media_type="text/markdown",
    )
    manifest = service.create_manifest(manifest_name="dummy", source_root=".", sources=[source])
    candidate = service.create_ingestion_candidate(manifest=manifest, sources=[source])
    service.validate_candidate(candidate, [source])
    draft = service.create_assimilation_draft(candidate=candidate, sources=[source])
    projection = service.create_projection_candidate(draft=draft, candidate=candidate)
    service.record_risk_note(
        source_id=source.source_id,
        candidate_id=candidate.candidate_id,
        risk_level="low",
        risk_categories=["review"],
        message="Review before use.",
    )

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}

    for object_type in [
        "persona_source",
        "persona_source_manifest",
        "persona_source_ingestion_candidate",
        "persona_source_validation_result",
        "persona_assimilation_draft",
        "persona_projection_candidate",
        "persona_source_risk_note",
    ]:
        assert store.fetch_objects_by_type(object_type)
    assert {
        "persona_source_registered",
        "persona_source_manifest_created",
        "persona_source_ingestion_candidate_created",
        "persona_source_validation_recorded",
        "persona_assimilation_draft_created",
        "persona_projection_candidate_created",
        "persona_source_risk_note_recorded",
        "persona_source_review_required",
    }.issubset(activities)
    assert projection.canonical_import_enabled is False
