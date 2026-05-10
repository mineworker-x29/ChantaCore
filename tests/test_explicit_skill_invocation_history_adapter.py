from chanta_core.skills.history_adapter import (
    explicit_skill_invocation_requests_to_history_entries,
    explicit_skill_invocation_results_to_history_entries,
    explicit_skill_invocation_violations_to_history_entries,
)
from chanta_core.skills.invocation import (
    ExplicitSkillInvocationRequest,
    ExplicitSkillInvocationResult,
    ExplicitSkillInvocationViolation,
)


def test_explicit_skill_invocation_history_entries() -> None:
    created_at = "2026-01-01T00:00:00Z"
    request = ExplicitSkillInvocationRequest(
        request_id="explicit_skill_invocation_request:test",
        skill_id="skill:read_workspace_text_file",
        requester_type="test",
        requester_id="tester",
        session_id="session:test",
        turn_id=None,
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
    result = ExplicitSkillInvocationResult(
        result_id="explicit_skill_invocation_result:test",
        request_id=request.request_id,
        skill_id=request.skill_id,
        status="denied",
        output_payload={},
        output_preview={},
        violation_ids=["explicit_skill_invocation_violation:test"],
        started_at=None,
        completed_at=created_at,
        error_message="denied",
    )
    violation = ExplicitSkillInvocationViolation(
        violation_id="explicit_skill_invocation_violation:test",
        request_id=request.request_id,
        skill_id=request.skill_id,
        violation_type="invalid_input",
        severity="high",
        message="invalid",
        subject_ref=request.skill_id,
        created_at=created_at,
    )

    request_entry = explicit_skill_invocation_requests_to_history_entries([request])[0]
    result_entry = explicit_skill_invocation_results_to_history_entries([result])[0]
    violation_entry = explicit_skill_invocation_violations_to_history_entries([violation])[0]

    assert request_entry.source == "explicit_skill_invocation"
    assert result_entry.priority == 85
    assert violation_entry.priority == 90
