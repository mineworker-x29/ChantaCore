from chanta_core.outcomes.history_adapter import process_outcome_evaluations_to_history_entries
from chanta_core.outcomes.models import ProcessOutcomeEvaluation
from chanta_core.utility.time import utc_now_iso


def _evaluation(status: str, score: float | None = None) -> ProcessOutcomeEvaluation:
    return ProcessOutcomeEvaluation(
        evaluation_id=f"process_outcome_evaluation:{status}",
        contract_id="process_outcome_contract:test",
        target_id="process_outcome_target:test",
        outcome_status=status,
        score=score,
        confidence=0.5,
        evidence_coverage=0.5,
        passed_criteria_ids=[],
        failed_criteria_ids=[],
        signal_ids=[f"process_outcome_signal:{status}"] if status in {"success", "partial_success", "failed"} else [],
        verification_result_ids=["verification_result:test"] if status in {"success", "partial_success", "failed"} else [],
        reason=f"{status} reason",
        created_at=utc_now_iso(),
        evaluation_attrs={},
    )


def test_process_outcome_evaluations_to_history_entries() -> None:
    success = _evaluation("success", 1.0)
    failed = _evaluation("failed", 0.0)

    entries = process_outcome_evaluations_to_history_entries([success, failed])

    assert [entry.source for entry in entries] == ["process_outcome", "process_outcome"]
    assert all(entry.role == "context" for entry in entries)
    assert entries[1].priority > entries[0].priority
    refs = entries[0].refs[0]
    assert refs["evaluation_id"] == success.evaluation_id
    assert refs["contract_id"] == success.contract_id
    assert refs["target_id"] == success.target_id
    assert refs["signal_ids"] == success.signal_ids
    assert refs["verification_result_ids"] == success.verification_result_ids
