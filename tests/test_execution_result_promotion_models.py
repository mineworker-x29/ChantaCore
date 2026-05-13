from chanta_core.execution.promotion import (
    ExecutionResultPromotionCandidate,
    ExecutionResultPromotionDecision,
    ExecutionResultPromotionFinding,
    ExecutionResultPromotionPolicy,
    ExecutionResultPromotionResult,
    ExecutionResultPromotionReviewRequest,
)
from chanta_core.utility.time import utc_now_iso


def test_execution_result_promotion_models_to_dict() -> None:
    now = utc_now_iso()
    policy = ExecutionResultPromotionPolicy(
        policy_id="execution_result_promotion_policy:test",
        policy_name="Default",
        allowed_target_kinds=["memory_candidate"],
        denied_target_kinds=["canonical_memory"],
        require_review=True,
        allow_canonical_promotion=False,
        allow_private_candidate=True,
        max_preview_chars=2000,
        status="active",
        created_at=now,
    )
    candidate = ExecutionResultPromotionCandidate(
        candidate_id="execution_result_promotion_candidate:test",
        envelope_id="execution_envelope:test",
        outcome_summary_id="execution_outcome_summary:test",
        output_snapshot_id="execution_output_snapshot:test",
        artifact_ref_id=None,
        target_kind="memory_candidate",
        candidate_title="Candidate",
        candidate_preview={"content": "preview"},
        candidate_hash="hash:test",
        source_ref_kind="execution_output_snapshot",
        source_ref_id="execution_output_snapshot:test",
        private=False,
        sensitive=False,
        review_status="pending_review",
        canonical_promotion_enabled=False,
        created_at=now,
    )
    request = ExecutionResultPromotionReviewRequest(
        review_request_id="execution_result_promotion_review_request:test",
        candidate_id=candidate.candidate_id,
        envelope_id=candidate.envelope_id,
        requested_by="tester",
        session_id="session:test",
        turn_id=None,
        process_instance_id=None,
        status="pending_review",
        created_at=now,
    )
    decision = ExecutionResultPromotionDecision(
        decision_id="execution_result_promotion_decision:test",
        review_request_id=request.review_request_id,
        candidate_id=candidate.candidate_id,
        decision="no_action",
        reviewer_type="human",
        reviewer_id="tester",
        reason="skip",
        approved_target_kind=None,
        can_promote_now=False,
        requires_manual_action=False,
        created_at=now,
    )
    finding = ExecutionResultPromotionFinding(
        finding_id="execution_result_promotion_finding:test",
        candidate_id=candidate.candidate_id,
        envelope_id=candidate.envelope_id,
        finding_type="review_required",
        status="pending_review",
        severity="medium",
        message="review",
        subject_ref=candidate.candidate_id,
        created_at=now,
    )
    result = ExecutionResultPromotionResult(
        result_id="execution_result_promotion_result:test",
        candidate_id=candidate.candidate_id,
        envelope_id=candidate.envelope_id,
        review_request_id=request.review_request_id,
        decision_id=decision.decision_id,
        status="no_action",
        promoted=False,
        canonical_promotion_enabled=False,
        finding_ids=[finding.finding_id],
        summary="done",
        created_at=now,
    )

    assert policy.to_dict()["allow_canonical_promotion"] is False
    assert candidate.to_dict()["review_status"] == "pending_review"
    assert request.to_dict()["status"] == "pending_review"
    assert decision.to_dict()["can_promote_now"] is False
    assert finding.to_dict()["finding_type"] == "review_required"
    assert result.to_dict()["promoted"] is False
