from chanta_core.capabilities import CapabilityDecisionSurfaceService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def test_workspace_read_decision_requires_explicit_skill_not_ambient_access(tmp_path) -> None:
    store = OCELStore(tmp_path / "capability_workspace_read.sqlite")
    service = CapabilityDecisionSurfaceService(
        trace_service=TraceService(ocel_store=store)
    )

    surface = service.build_decision_surface("read /PersonalDirectory/sample_profile.md")

    assert surface.can_fulfill_now is False
    assert surface.overall_availability == "requires_explicit_skill"
    assert surface.recommended_agent_mode == "requires_explicit_skill"
    assert service.last_decisions[0].availability == "requires_explicit_skill"
    assert service.last_decisions[0].can_execute_now is False
    assert "explicit root-constrained read-only skills" in (service.last_decisions[0].reason or "")

