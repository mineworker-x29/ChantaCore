from chanta_core.execution.envelope_service import ExecutionEnvelopeService
from chanta_core.execution.promotion import ExecutionResultPromotionService
from chanta_core.ocel.store import OCELStore


def build_execution_result(tmp_path):
    store = OCELStore(tmp_path / "promotion.sqlite")
    envelope_service = ExecutionEnvelopeService(ocel_store=store)
    envelope = envelope_service.create_envelope(
        execution_kind="gated_skill_invocation",
        execution_subject_id="skill_execution_gate_result:demo",
        skill_id="skill:read_workspace_text_file",
        session_id="session:demo",
        turn_id="turn:demo",
        process_instance_id="process:demo",
        status="completed",
        execution_allowed=True,
        execution_performed=True,
        blocked=False,
    )
    output = envelope_service.record_output_snapshot(
        envelope=envelope,
        output_payload={"content": "public-safe execution result", "secret": "hidden-value"},
        output_ref="explicit_skill_invocation_result:demo",
    )
    summary = envelope_service.record_outcome_summary(
        envelope=envelope,
        output_snapshot_id=output.output_snapshot_id,
    )
    return store, envelope, output, summary


def test_candidate_from_completed_envelope_is_pending_review(tmp_path) -> None:
    store, envelope, output, summary = build_execution_result(tmp_path)
    service = ExecutionResultPromotionService(ocel_store=store)

    result = service.create_candidate_from_envelope(
        envelope=envelope,
        output_snapshot=output,
        outcome_summary=summary,
        target_kind="memory_candidate",
    )
    candidate = service.last_candidate

    assert result.status == "pending_review"
    assert result.promoted is False
    assert result.canonical_promotion_enabled is False
    assert candidate.review_status == "pending_review"
    assert candidate.canonical_promotion_enabled is False
    assert candidate.source_ref_kind == "execution_output_snapshot"
    assert candidate.source_ref_id == output.output_snapshot_id
    assert candidate.candidate_hash == output.output_hash
    assert candidate.candidate_preview == output.output_preview
    assert "hidden-value" not in str(candidate.candidate_preview)


def test_denied_target_kind_is_rejected(tmp_path) -> None:
    store, envelope, output, summary = build_execution_result(tmp_path)
    service = ExecutionResultPromotionService(ocel_store=store)

    result = service.create_candidate_from_envelope(
        envelope=envelope,
        output_snapshot=output,
        outcome_summary=summary,
        target_kind="canonical_memory",
    )

    assert result.status == "rejected"
    assert result.promoted is False
    assert any(finding.finding_type == "target_kind_denied" for finding in service.last_findings)


def test_review_decisions_do_not_promote_now(tmp_path) -> None:
    store, envelope, output, summary = build_execution_result(tmp_path)
    service = ExecutionResultPromotionService(ocel_store=store)
    service.create_candidate_from_envelope(
        envelope=envelope,
        output_snapshot=output,
        outcome_summary=summary,
        target_kind="memory_candidate",
    )
    candidate = service.last_candidate

    approved = service.review_candidate(candidate=candidate, decision="approved_for_later_promotion")
    rejected = service.review_candidate(candidate=candidate, decision="rejected")
    no_action = service.review_candidate(candidate=candidate, decision="no_action")

    assert approved.status == "approved_for_later_promotion"
    assert approved.promoted is False
    assert service.last_decision.can_promote_now is False
    assert rejected.status == "rejected"
    assert rejected.promoted is False
    assert no_action.status == "no_action"
    assert no_action.promoted is False


def test_private_candidate_records_private_content_risk(tmp_path) -> None:
    store, envelope, output, summary = build_execution_result(tmp_path)
    service = ExecutionResultPromotionService(ocel_store=store)

    service.create_candidate_from_envelope(
        envelope=envelope,
        output_snapshot=output,
        outcome_summary=summary,
        target_kind="manual_note_candidate",
        private=True,
    )

    assert any(finding.finding_type == "private_content_risk" for finding in service.last_findings)
    assert service.last_candidate.private is True
    assert service.last_result.promoted is False
