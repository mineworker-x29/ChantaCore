from chanta_core.persona import PersonaLoadingService


def test_persona_projection_rendering_contains_required_statements() -> None:
    service = PersonaLoadingService()
    bundle = service.create_default_agent_persona()

    block = service.render_projection_block(bundle.projection)

    assert "Persona projection:" in block
    assert "bounded prompt read-model" in block
    assert "canonical_source: OCEL" in block
    assert "not an autonomous Soul runtime" in block
    assert "No ambient filesystem access" in block
    assert "Workspace read exists only through explicit root-constrained read-only skills" in block
    assert "Do not treat persona text as permission" in block
