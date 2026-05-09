from chanta_core.persona import (
    PersonaSourceStagedImportService,
    persona_assimilation_drafts_to_history_entries,
    persona_ingestion_candidates_to_history_entries,
    persona_projection_candidates_to_history_entries,
    persona_source_risk_notes_to_history_entries,
    persona_sources_to_history_entries,
)


def test_persona_source_import_history_adapters_convert_records() -> None:
    service = PersonaSourceStagedImportService()
    source = service.register_source_from_text(
        source_name="profile.md",
        text="identity: public dummy",
        source_ref="profile.md",
        media_type="text/markdown",
    )
    manifest = service.create_manifest(manifest_name="dummy", source_root=".", sources=[source])
    candidate = service.create_ingestion_candidate(manifest=manifest, sources=[source])
    draft = service.create_assimilation_draft(candidate=candidate, sources=[source])
    projection = service.create_projection_candidate(draft=draft, candidate=candidate)
    risk_note = service.record_risk_note(
        source_id=source.source_id,
        candidate_id=candidate.candidate_id,
        risk_level="low",
        risk_categories=["review"],
        message="Review before use.",
    )

    entries = (
        persona_sources_to_history_entries([source])
        + persona_ingestion_candidates_to_history_entries([candidate])
        + persona_assimilation_drafts_to_history_entries([draft])
        + persona_projection_candidates_to_history_entries([projection])
        + persona_source_risk_notes_to_history_entries([risk_note])
    )

    assert {entry.source for entry in entries} == {"persona_source_import"}
    assert any(entry.refs[0]["ref_type"] == "persona_source" for entry in entries)
    assert any("canonical_import_enabled" in entry.entry_attrs for entry in entries)
