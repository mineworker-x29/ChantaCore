from chanta_core.sandbox import (
    NetworkAccessIntent,
    ShellCommandIntent,
    ShellNetworkPreSandboxDecision,
    ShellNetworkRiskAssessment,
    ShellNetworkRiskViolation,
    network_access_intents_to_history_entries,
    shell_command_intents_to_history_entries,
    shell_network_pre_sandbox_decisions_to_history_entries,
    shell_network_risk_assessments_to_history_entries,
    shell_network_risk_violations_to_history_entries,
)


def test_shell_network_history_adapters_convert_objects() -> None:
    shell_intent = ShellCommandIntent(
        intent_id="shell_command_intent:test",
        command_text="echo hello",
        shell_type=None,
        cwd=None,
        requester_type=None,
        requester_id=None,
        session_id="session:test",
        turn_id="conversation_turn:test",
        process_instance_id="process_instance:test",
        permission_request_id="permission_request:test",
        session_permission_resolution_id="session_permission_resolution:test",
        workspace_write_decision_id="workspace_write_sandbox_decision:test",
        reason=None,
        created_at="2026-01-01T00:00:00Z",
        intent_attrs={},
    )
    network_intent = NetworkAccessIntent(
        intent_id="network_access_intent:test",
        url="https://example.com",
        host="example.com",
        port=443,
        protocol="https",
        method=None,
        requester_type=None,
        requester_id=None,
        session_id="session:test",
        turn_id=None,
        process_instance_id=None,
        permission_request_id=None,
        session_permission_resolution_id=None,
        reason=None,
        created_at="2026-01-01T00:00:00Z",
        intent_attrs={},
    )
    assessment = ShellNetworkRiskAssessment(
        assessment_id="shell_network_risk_assessment:test",
        intent_kind="shell_command",
        intent_id=shell_intent.intent_id,
        risk_level="critical",
        risk_categories=["destructive_filesystem"],
        detected_tokens=["rm -rf"],
        detected_targets=[],
        summary=None,
        confidence=1.0,
        created_at="2026-01-01T00:00:00Z",
        assessment_attrs={},
    )
    decision = ShellNetworkPreSandboxDecision(
        decision_id="shell_network_pre_sandbox_decision:test",
        intent_kind="shell_command",
        intent_id=shell_intent.intent_id,
        assessment_id=assessment.assessment_id,
        decision="deny_recommended",
        decision_basis="destructive_token_detected",
        risk_level="critical",
        violation_ids=["shell_network_risk_violation:test"],
        confidence=1.0,
        reason=None,
        enforcement_enabled=False,
        created_at="2026-01-01T00:00:00Z",
        decision_attrs={},
    )
    violation = ShellNetworkRiskViolation(
        violation_id="shell_network_risk_violation:test",
        intent_kind="shell_command",
        intent_id=shell_intent.intent_id,
        violation_type="destructive_command",
        severity="critical",
        message="unsafe",
        detected_value="rm -rf",
        created_at="2026-01-01T00:00:00Z",
        violation_attrs={},
    )

    shell_entry = shell_command_intents_to_history_entries([shell_intent])[0]
    network_entry = network_access_intents_to_history_entries([network_intent])[0]
    assessment_entry = shell_network_risk_assessments_to_history_entries([assessment])[0]
    decision_entry = shell_network_pre_sandbox_decisions_to_history_entries([decision])[0]
    violation_entry = shell_network_risk_violations_to_history_entries([violation])[0]

    assert shell_entry.source == "shell_network_pre_sandbox"
    assert network_entry.source == "shell_network_pre_sandbox"
    assert shell_entry.refs[0]["workspace_write_decision_id"] == "workspace_write_sandbox_decision:test"
    assert assessment_entry.refs[0]["assessment_id"] == assessment.assessment_id
    assert decision_entry.priority >= shell_entry.priority
    assert violation_entry.priority >= decision_entry.priority
