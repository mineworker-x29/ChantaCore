from chanta_core.ocel.store import OCELStore
from chanta_core.sandbox import ShellNetworkRiskPreSandboxService
from chanta_core.traces.trace_service import TraceService


def _service(tmp_path):
    store = OCELStore(tmp_path / "shell_network_pre_sandbox.sqlite")
    service = ShellNetworkRiskPreSandboxService(trace_service=TraceService(ocel_store=store))
    return store, service


def test_shell_network_pre_sandbox_service_records_intents_and_assessments(tmp_path) -> None:
    store, service = _service(tmp_path)
    shell_intent = service.create_shell_command_intent(
        command_text="echo hello",
        shell_type="powershell",
        session_id="session:shell",
        turn_id="conversation_turn:shell",
        process_instance_id="process_instance:shell",
        permission_request_id="permission_request:shell",
        session_permission_resolution_id="session_permission_resolution:shell",
        workspace_write_decision_id="workspace_write_sandbox_decision:shell",
    )
    network_intent = service.create_network_access_intent(url="https://example.com")
    assessment = service.assess_shell_command_intent(intent=shell_intent)
    network_assessment = service.assess_network_access_intent(intent=network_intent)

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}
    assert {
        "shell_command_intent_created",
        "network_access_intent_created",
        "shell_network_risk_assessment_recorded",
    }.issubset(activities)
    assert assessment.risk_level == "low"
    assert network_assessment.risk_level == "medium"


def test_evaluate_shell_command_intent_records_decision_and_violations(tmp_path) -> None:
    store, service = _service(tmp_path)
    safe_intent = service.create_shell_command_intent(command_text="echo hello")
    destructive_intent = service.create_shell_command_intent(command_text="rm -rf ./data")

    safe_decision = service.evaluate_shell_command_intent(intent=safe_intent)
    destructive_decision = service.evaluate_shell_command_intent(intent=destructive_intent)

    assert safe_decision.decision == "allow_recommended"
    assert safe_decision.risk_level == "low"
    assert safe_decision.enforcement_enabled is False
    assert destructive_decision.decision == "deny_recommended"
    assert destructive_decision.violation_ids
    assert destructive_decision.enforcement_enabled is False
    assert store.fetch_objects_by_type("shell_network_risk_violation")


def test_evaluate_network_access_intent_records_decision_without_access(tmp_path) -> None:
    _, service = _service(tmp_path)
    external = service.create_network_access_intent(url="https://example.com")
    local = service.create_network_access_intent(url="http://localhost:8000")
    unknown = service.create_network_access_intent(host=None, protocol=None)

    external_decision = service.evaluate_network_access_intent(intent=external)
    local_decision = service.evaluate_network_access_intent(intent=local)
    unknown_decision = service.evaluate_network_access_intent(intent=unknown)

    assert external_decision.decision == "needs_review"
    assert external_decision.enforcement_enabled is False
    assert local_decision.decision == "allow_recommended"
    assert local_decision.enforcement_enabled is False
    assert unknown_decision.decision == "inconclusive"
    assert unknown_decision.decision_basis == "unknown_host"


def test_service_does_not_create_files_for_shell_text(tmp_path) -> None:
    _, service = _service(tmp_path)
    target = tmp_path / "should_not_exist.txt"
    intent = service.create_shell_command_intent(command_text=f"echo x > {target}")

    decision = service.evaluate_shell_command_intent(intent=intent)

    assert decision.decision in {"needs_review", "deny_recommended"}
    assert not target.exists()
