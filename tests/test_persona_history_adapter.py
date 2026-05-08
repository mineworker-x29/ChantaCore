from chanta_core.persona import (
    PersonaLoadingService,
    persona_instruction_artifacts_to_history_entries,
    persona_profiles_to_history_entries,
    persona_projections_to_history_entries,
)


def test_persona_history_adapters_convert_records() -> None:
    service = PersonaLoadingService()
    bundle = service.create_default_agent_persona()

    profile_entry = persona_profiles_to_history_entries([bundle.profile])[0]
    artifact_entry = persona_instruction_artifacts_to_history_entries(bundle.artifacts)[0]
    projection_entry = persona_projections_to_history_entries([bundle.projection])[0]

    assert profile_entry.source == "persona"
    assert artifact_entry.priority == 75
    assert projection_entry.refs[0]["ref_id"] == bundle.projection.projection_id
