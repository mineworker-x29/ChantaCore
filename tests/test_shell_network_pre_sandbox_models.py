import pytest

from chanta_core.sandbox import (
    NetworkAccessIntent,
    ShellCommandIntent,
    ShellNetworkPreSandboxDecision,
    ShellNetworkRiskAssessment,
    ShellNetworkRiskViolation,
)
from chanta_core.sandbox.errors import ShellNetworkPreSandboxDecisionError, ShellNetworkRiskAssessmentError
from chanta_core.sandbox.ids import (
    new_network_access_intent_id,
    new_shell_command_intent_id,
    new_shell_network_pre_sandbox_decision_id,
    new_shell_network_risk_assessment_id,
    new_shell_network_risk_violation_id,
)


def test_shell_network_pre_sandbox_ids_use_expected_prefixes() -> None:
    assert new_shell_command_intent_id().startswith("shell_command_intent:")
    assert new_network_access_intent_id().startswith("network_access_intent:")
    assert new_shell_network_risk_assessment_id().startswith("shell_network_risk_assessment:")
    assert new_shell_network_pre_sandbox_decision_id().startswith("shell_network_pre_sandbox_decision:")
    assert new_shell_network_risk_violation_id().startswith("shell_network_risk_violation:")


def test_shell_command_intent_to_dict() -> None:
    item = ShellCommandIntent(
        intent_id="shell_command_intent:test",
        command_text="echo hello",
        shell_type="powershell",
        cwd=None,
        requester_type="test",
        requester_id="tester",
        session_id="session:test",
        turn_id="conversation_turn:test",
        process_instance_id="process_instance:test",
        permission_request_id="permission_request:test",
        session_permission_resolution_id="session_permission_resolution:test",
        workspace_write_decision_id="workspace_write_sandbox_decision:test",
        reason="test",
        created_at="2026-01-01T00:00:00Z",
        intent_attrs={"runtime_effect": False},
    )

    data = item.to_dict()

    assert data["intent_id"] == item.intent_id
    assert data["command_text"] == "echo hello"
    assert data["workspace_write_decision_id"] == "workspace_write_sandbox_decision:test"


def test_network_access_intent_to_dict() -> None:
    item = NetworkAccessIntent(
        intent_id="network_access_intent:test",
        url="https://example.com",
        host="example.com",
        port=443,
        protocol="https",
        method="GET",
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

    data = item.to_dict()

    assert data["intent_id"] == item.intent_id
    assert data["host"] == "example.com"
    assert data["protocol"] == "https"


def test_shell_network_assessment_decision_violation_to_dict() -> None:
    assessment = ShellNetworkRiskAssessment(
        assessment_id="shell_network_risk_assessment:test",
        intent_kind="shell_command",
        intent_id="shell_command_intent:test",
        risk_level="low",
        risk_categories=["read_only"],
        detected_tokens=[],
        detected_targets=[],
        summary="safe",
        confidence=1.0,
        created_at="2026-01-01T00:00:00Z",
        assessment_attrs={},
    )
    decision = ShellNetworkPreSandboxDecision(
        decision_id="shell_network_pre_sandbox_decision:test",
        intent_kind="shell_command",
        intent_id="shell_command_intent:test",
        assessment_id=assessment.assessment_id,
        decision="allow_recommended",
        decision_basis="low_risk_read_only",
        risk_level="low",
        violation_ids=[],
        confidence=1.0,
        reason="safe",
        enforcement_enabled=False,
        created_at="2026-01-01T00:00:00Z",
        decision_attrs={},
    )
    violation = ShellNetworkRiskViolation(
        violation_id="shell_network_risk_violation:test",
        intent_kind="shell_command",
        intent_id="shell_command_intent:test",
        violation_type="destructive_command",
        severity="critical",
        message="unsafe",
        detected_value="rm -rf",
        created_at="2026-01-01T00:00:00Z",
        violation_attrs={},
    )

    assert assessment.to_dict()["risk_categories"] == ["read_only"]
    assert decision.to_dict()["enforcement_enabled"] is False
    assert violation.to_dict()["violation_type"] == "destructive_command"


def test_confidence_range_validation() -> None:
    with pytest.raises(ShellNetworkRiskAssessmentError):
        ShellNetworkRiskAssessment(
            assessment_id="shell_network_risk_assessment:test",
            intent_kind="shell_command",
            intent_id="shell_command_intent:test",
            risk_level="low",
            risk_categories=["read_only"],
            detected_tokens=[],
            detected_targets=[],
            summary=None,
            confidence=1.5,
            created_at="2026-01-01T00:00:00Z",
            assessment_attrs={},
        )

    with pytest.raises(ShellNetworkPreSandboxDecisionError):
        ShellNetworkPreSandboxDecision(
            decision_id="shell_network_pre_sandbox_decision:test",
            intent_kind="shell_command",
            intent_id="shell_command_intent:test",
            assessment_id=None,
            decision="allow_recommended",
            decision_basis="low_risk_read_only",
            risk_level="low",
            violation_ids=[],
            confidence=1.0,
            reason=None,
            enforcement_enabled=True,
            created_at="2026-01-01T00:00:00Z",
            decision_attrs={},
        )
