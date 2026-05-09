from chanta_core.persona import (
    PersonaAssimilationDraft,
    PersonaProjectionCandidate,
    PersonaSource,
    PersonaSourceIngestionCandidate,
    PersonaSourceManifest,
    PersonaSourceRiskNote,
    PersonaSourceValidationResult,
)
from chanta_core.persona.ids import (
    new_persona_assimilation_draft_id,
    new_persona_projection_candidate_id,
    new_persona_source_id,
    new_persona_source_ingestion_candidate_id,
    new_persona_source_manifest_id,
    new_persona_source_risk_note_id,
    new_persona_source_validation_result_id,
)


def test_persona_source_import_ids_use_expected_prefixes() -> None:
    assert new_persona_source_id().startswith("persona_source:")
    assert new_persona_source_manifest_id().startswith("persona_source_manifest:")
    assert new_persona_source_ingestion_candidate_id().startswith(
        "persona_source_ingestion_candidate:"
    )
    assert new_persona_source_validation_result_id().startswith(
        "persona_source_validation_result:"
    )
    assert new_persona_assimilation_draft_id().startswith("persona_assimilation_draft:")
    assert new_persona_projection_candidate_id().startswith("persona_projection_candidate:")
    assert new_persona_source_risk_note_id().startswith("persona_source_risk_note:")


def test_persona_source_import_models_to_dict() -> None:
    source = PersonaSource(
        "persona_source:1",
        "profile.md",
        "markdown",
        "profile.md",
        "text/markdown",
        "hash",
        "preview",
        7,
        "unreviewed",
        False,
        "staged",
        "now",
        {},
    )
    manifest = PersonaSourceManifest(
        "persona_source_manifest:1",
        "manifest",
        "root",
        ["*.md"],
        ["archive/**"],
        [source.source_id],
        "now",
        {},
    )
    candidate = PersonaSourceIngestionCandidate(
        "persona_source_ingestion_candidate:1",
        manifest.manifest_id,
        [source.source_id],
        "staged",
        "pending_review",
        False,
        False,
        "review",
        "now",
        {},
    )
    validation = PersonaSourceValidationResult(
        "persona_source_validation_result:1",
        candidate.candidate_id,
        source.source_id,
        "valid",
        "shape",
        [],
        [],
        [],
        "now",
        {},
    )
    draft = PersonaAssimilationDraft(
        "persona_assimilation_draft:1",
        candidate.candidate_id,
        [source.source_id],
        "deterministic",
        "Draft",
        ["identity"],
        ["role"],
        ["boundary"],
        ["style"],
        ["safety"],
        [],
        "now",
        {},
    )
    projection = PersonaProjectionCandidate(
        "persona_projection_candidate:1",
        draft.draft_id,
        candidate.candidate_id,
        "bounded",
        [{"block_type": "identity", "items": ["identity"]}],
        8,
        False,
        False,
        "now",
        {},
    )
    risk_note = PersonaSourceRiskNote(
        "persona_source_risk_note:1",
        source.source_id,
        candidate.candidate_id,
        "low",
        ["review"],
        "Review before activation.",
        True,
        "now",
        {},
    )

    assert source.to_dict()["source_type"] == "markdown"
    assert manifest.to_dict()["source_ids"] == [source.source_id]
    assert candidate.to_dict()["canonical_import_enabled"] is False
    assert validation.to_dict()["status"] == "valid"
    assert draft.to_dict()["identity_points"] == ["identity"]
    assert projection.to_dict()["canonical_import_enabled"] is False
    assert risk_note.to_dict()["review_required"] is True
