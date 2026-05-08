from chanta_core.capabilities import CapabilityDecisionSurfaceService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def _build(prompt: str, tmp_path):
    service = CapabilityDecisionSurfaceService(
        trace_service=TraceService(ocel_store=OCELStore(tmp_path / "capability.sqlite"))
    )
    surface = service.build_decision_surface(prompt, session_id="session:test")
    return service, surface


def test_chat_and_capability_self_report_available_now(tmp_path) -> None:
    service, surface = _build("넌 뭘 할 수 있어?", tmp_path)

    assert surface.can_fulfill_now is True
    assert surface.overall_availability == "available_now"
    assert {decision.capability_name for decision in service.last_decisions} == {
        "skill:llm_chat",
        "session_context_projection",
    }
    assert all(decision.availability == "available_now" for decision in service.last_decisions)


def test_workspace_read_not_available_now(tmp_path) -> None:
    service, surface = _build("/Souls/ChantaVeraAide markdown 파일 읽어봐", tmp_path)

    assert surface.can_fulfill_now is False
    assert surface.recommended_agent_mode == "requires_explicit_skill"
    assert service.last_decisions[0].availability == "requires_explicit_skill"


def test_shell_network_mcp_plugin_are_not_available_now(tmp_path) -> None:
    prompts = [
        ("powershell 실행", "requires_permission"),
        ("https://example.com 호출", "requires_permission"),
        ("MCP 연결", "not_implemented"),
        ("플러그인 로딩", "not_implemented"),
    ]
    for prompt, expected in prompts:
        service, surface = _build(prompt, tmp_path)
        assert surface.can_fulfill_now is False
        assert service.last_decisions[0].availability == expected


def test_external_candidates_are_disabled_or_review_required(tmp_path) -> None:
    service, _ = _build("external capability 실행", tmp_path)
    assert service.last_decisions[0].availability == "disabled_candidate"

    service, _ = _build("external OCEL import merge", tmp_path)
    assert service.last_decisions[0].availability == "requires_review"


def test_render_decision_surface_block_guides_limitations(tmp_path) -> None:
    service, surface = _build("powershell 실행", tmp_path)

    block = service.render_decision_surface_block(surface)

    assert "Runtime capability decision surface:" in block
    assert "can_fulfill_now: False" in block
    assert "Do not execute tools" in block
