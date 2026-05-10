from chanta_core.skills.invocation import (
    ExplicitSkillInvocationDecision,
    ExplicitSkillInvocationInput,
    ExplicitSkillInvocationRequest,
    ExplicitSkillInvocationResult,
    ExplicitSkillInvocationViolation,
)


def test_explicit_skill_invocation_models_to_dict() -> None:
    created_at = "2026-01-01T00:00:00Z"
    request = ExplicitSkillInvocationRequest(
        request_id="explicit_skill_invocation_request:test",
        skill_id="skill:list_workspace_files",
        requester_type="test",
        requester_id="tester",
        session_id="session:test",
        turn_id="turn:test",
        process_instance_id="process_instance:test",
        capability_decision_id=None,
        permission_request_id=None,
        session_permission_resolution_id=None,
        workspace_sandbox_decision_id=None,
        shell_network_decision_id=None,
        invocation_mode="test",
        status="created",
        created_at=created_at,
    )
    invocation_input = ExplicitSkillInvocationInput(
        input_id="explicit_skill_invocation_input:test",
        request_id=request.request_id,
        skill_id=request.skill_id,
        input_payload={"root_path": "<root>", "relative_path": "."},
        input_preview={"root_path": "<root>", "relative_path": "."},
        input_hash="hash",
        validation_status="valid",
        validation_messages=[],
        created_at=created_at,
    )
    violation = ExplicitSkillInvocationViolation(
        violation_id="explicit_skill_invocation_violation:test",
        request_id=request.request_id,
        skill_id=request.skill_id,
        violation_type="unsupported_skill",
        severity="high",
        message="unsupported",
        subject_ref=request.skill_id,
        created_at=created_at,
    )
    decision = ExplicitSkillInvocationDecision(
        decision_id="explicit_skill_invocation_decision:test",
        request_id=request.request_id,
        skill_id=request.skill_id,
        decision="allow_explicit",
        decision_basis="input_valid",
        can_execute=True,
        requires_permission=False,
        requires_review=False,
        reason=None,
        violation_ids=[],
        created_at=created_at,
    )
    result = ExplicitSkillInvocationResult(
        result_id="explicit_skill_invocation_result:test",
        request_id=request.request_id,
        skill_id=request.skill_id,
        status="completed",
        output_payload={"success": True},
        output_preview={"success": True},
        violation_ids=[violation.violation_id],
        started_at=created_at,
        completed_at=created_at,
        error_message=None,
    )

    assert request.to_dict()["skill_id"] == "skill:list_workspace_files"
    assert invocation_input.to_dict()["validation_status"] == "valid"
    assert decision.to_dict()["can_execute"] is True
    assert result.to_dict()["status"] == "completed"
    assert violation.to_dict()["violation_type"] == "unsupported_skill"
