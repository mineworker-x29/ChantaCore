from chanta_core.ocel.store import OCELStore
from chanta_core.persona import PersonaLoadingService
from chanta_core.traces.trace_service import TraceService


def test_default_agent_persona_created_with_boundaries(tmp_path) -> None:
    store = OCELStore(tmp_path / "persona.sqlite")
    service = PersonaLoadingService(trace_service=TraceService(ocel_store=store))

    bundle = service.create_default_agent_persona()
    block = service.render_projection_block(bundle.projection)

    assert bundle.soul.soul_name == "ChantaCore Default Agent"
    assert bundle.profile.profile_attrs["capability_boundaries_override_persona"] is True
    assert bundle.loadout.loadout_attrs["persona_mutation_enabled"] is False
    assert "not an autonomous Soul runtime" in bundle.soul.description
    assert "Capability boundaries" in block
    assert "No ambient filesystem access" in block
    assert "No shell execution" in block
    assert "runtime capability boundaries override persona claims" in block


def test_persona_projection_is_bounded(tmp_path) -> None:
    service = PersonaLoadingService()
    bundle = service.create_default_agent_persona(max_chars=120)

    assert bundle.projection.total_chars <= 120
    assert bundle.projection.truncated is True
