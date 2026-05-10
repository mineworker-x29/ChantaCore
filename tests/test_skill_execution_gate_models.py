from chanta_core.skills.execution_gate import (
    ReadOnlyExecutionGatePolicy,
    SkillExecutionGateDecision,
    SkillExecutionGateFinding,
    SkillExecutionGateRequest,
    SkillExecutionGateResult,
)
from chanta_core.utility.time import utc_now_iso


def test_skill_execution_gate_models_to_dict() -> None:
    now = utc_now_iso()
    policy = ReadOnlyExecutionGatePolicy(
        policy_id="read_only_execution_gate_policy:test",
        policy_name="test",
        supported_skill_ids=["skill:read_workspace_text_file"],
        denied_skill_categories=["write"],
        requires_permission_for_read_only=False,
        allow_without_permission_for_read_only=True,
        require_capability_available=False,
        enforce_workspace_boundary=True,
        status="active",
        created_at=now,
    )
    request = SkillExecutionGateRequest(
        gate_request_id="skill_execution_gate_request:test",
        explicit_invocation_request_id=None,
        skill_id="skill:read_workspace_text_file",
        input_payload_preview={"relative_path": "docs/example.txt"},
        invocation_mode="test",
        requester_type="test",
        requester_id="test",
        session_id=None,
        turn_id=None,
        process_instance_id=None,
        capability_decision_id=None,
        permission_request_id=None,
        permission_decision_id=None,
        session_permission_resolution_id=None,
        workspace_read_root_id=None,
        workspace_sandbox_decision_id=None,
        shell_network_decision_id=None,
        created_at=now,
    )
    finding = SkillExecutionGateFinding(
        finding_id="skill_execution_gate_finding:test",
        gate_request_id=request.gate_request_id,
        finding_type="permission_context_absent",
        status="warning",
        severity="medium",
        message="test",
        subject_ref=request.skill_id,
        created_at=now,
    )
    decision = SkillExecutionGateDecision(
        gate_decision_id="skill_execution_gate_decision:test",
        gate_request_id=request.gate_request_id,
        skill_id=request.skill_id,
        decision="allow",
        decision_basis="read_only_workspace_skill_allowed",
        can_execute=True,
        enforcement_enabled=True,
        enforcement_scope="read_only_explicit_skills",
        requires_review=False,
        requires_permission=False,
        finding_ids=[finding.finding_id],
        reason="test",
        created_at=now,
    )
    result = SkillExecutionGateResult(
        gate_result_id="skill_execution_gate_result:test",
        gate_request_id=request.gate_request_id,
        gate_decision_id=decision.gate_decision_id,
        explicit_invocation_result_id="explicit_skill_invocation_result:test",
        status="executed",
        executed=True,
        blocked=False,
        finding_ids=[finding.finding_id],
        created_at=now,
    )

    assert policy.to_dict()["enforce_workspace_boundary"] is True
    assert request.to_dict()["skill_id"] == "skill:read_workspace_text_file"
    assert finding.to_dict()["status"] == "warning"
    assert decision.to_dict()["enforcement_enabled"] is True
    assert result.to_dict()["executed"] is True
