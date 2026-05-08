from chanta_core.ocel.store import OCELStore
from chanta_core.sandbox import ShellNetworkRiskPreSandboxService
from chanta_core.traces.trace_service import TraceService


def test_shell_network_pre_sandbox_ocel_shape_contains_expected_objects_and_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "shell_network_pre_sandbox_shape.sqlite")
    service = ShellNetworkRiskPreSandboxService(trace_service=TraceService(ocel_store=store))
    shell_intent = service.create_shell_command_intent(command_text="rm -rf ./data")
    network_intent = service.create_network_access_intent(url="https://example.com")

    shell_decision = service.evaluate_shell_command_intent(intent=shell_intent)
    network_decision = service.evaluate_network_access_intent(intent=network_intent)

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}
    assert {
        "shell_command_intent_created",
        "network_access_intent_created",
        "shell_network_risk_assessment_recorded",
        "shell_network_pre_sandbox_evaluated",
        "shell_network_pre_sandbox_decision_recorded",
        "shell_network_risk_violation_recorded",
    }.issubset(activities)
    assert store.fetch_objects_by_type("shell_command_intent")
    assert store.fetch_objects_by_type("network_access_intent")
    assert store.fetch_objects_by_type("shell_network_risk_assessment")
    assert store.fetch_objects_by_type("shell_network_pre_sandbox_decision")
    assert store.fetch_objects_by_type("shell_network_risk_violation")
    decision_attrs = store.fetch_objects_by_type("shell_network_pre_sandbox_decision")[0]["object_attrs"]
    assert decision_attrs["enforcement_enabled"] is False
    assert shell_decision.enforcement_enabled is False
    assert network_decision.enforcement_enabled is False
