from chanta_core.skills.reviewed_execution_bridge import (
    ReviewedExecutionBridgeDecision,
    ReviewedExecutionBridgeRequest,
    ReviewedExecutionBridgeResult,
    ReviewedExecutionBridgeViolation,
)
from chanta_core.utility.time import utc_now_iso


def test_reviewed_execution_bridge_models_to_dict() -> None:
    now = utc_now_iso()
    request = ReviewedExecutionBridgeRequest(
        bridge_request_id="reviewed_execution_bridge_request:test",
        proposal_id="skill_invocation_proposal:test",
        review_request_id="skill_proposal_review_request:test",
        review_decision_id="skill_proposal_review_decision:test",
        review_result_id="skill_proposal_review_result:test",
        skill_id="skill:read_workspace_text_file",
        proposed_input_preview={"relative_path": "docs/example.txt"},
        approved_input_payload={"root_path": "<ROOT>", "relative_path": "docs/example.txt"},
        invocation_mode="explicit_api",
        requester_type="test",
        requester_id="tester",
        session_id="session:test",
        turn_id="turn:test",
        process_instance_id="process:test",
        status="created",
        created_at=now,
    )
    decision = ReviewedExecutionBridgeDecision(
        bridge_decision_id="reviewed_execution_bridge_decision:test",
        bridge_request_id=request.bridge_request_id,
        proposal_id=request.proposal_id,
        review_decision_id=request.review_decision_id,
        decision="allow",
        decision_basis="approved_complete_read_only_review",
        can_bridge=True,
        can_invoke_explicit_skill=True,
        requires_gate=True,
        requires_review=False,
        violation_ids=[],
        reason="approved",
        created_at=now,
    )
    violation = ReviewedExecutionBridgeViolation(
        violation_id="reviewed_execution_bridge_violation:test",
        bridge_request_id=request.bridge_request_id,
        proposal_id=request.proposal_id,
        review_decision_id=request.review_decision_id,
        violation_type="missing_input",
        severity="high",
        message="missing",
        subject_ref="root_path",
        created_at=now,
    )
    result = ReviewedExecutionBridgeResult(
        bridge_result_id="reviewed_execution_bridge_result:test",
        bridge_request_id=request.bridge_request_id,
        bridge_decision_id=decision.bridge_decision_id,
        status="bridged_executed",
        explicit_invocation_request_id="explicit_skill_invocation_request:test",
        explicit_invocation_result_id="explicit_skill_invocation_result:test",
        gate_request_id="skill_execution_gate_request:test",
        gate_decision_id="skill_execution_gate_decision:test",
        gate_result_id="skill_execution_gate_result:test",
        execution_envelope_id="execution_envelope:test",
        executed=True,
        blocked=False,
        violation_ids=[violation.violation_id],
        created_at=now,
    )

    assert request.to_dict()["skill_id"] == "skill:read_workspace_text_file"
    assert decision.to_dict()["can_bridge"] is True
    assert violation.to_dict()["violation_type"] == "missing_input"
    assert result.to_dict()["executed"] is True
