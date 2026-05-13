from chanta_core.execution.history_adapter import (
    execution_result_promotion_candidates_to_history_entries,
    execution_result_promotion_decisions_to_history_entries,
    execution_result_promotion_findings_to_history_entries,
    execution_result_promotion_results_to_history_entries,
)
from chanta_core.execution.promotion import ExecutionResultPromotionService
from tests.test_execution_result_promotion_service import build_execution_result


def test_execution_result_promotion_history_entries(tmp_path) -> None:
    store, envelope, output, summary = build_execution_result(tmp_path)
    service = ExecutionResultPromotionService(ocel_store=store)
    service.create_candidate_from_envelope(
        envelope=envelope,
        output_snapshot=output,
        outcome_summary=summary,
        target_kind="memory_candidate",
        private=True,
    )
    candidate = service.last_candidate
    result = service.review_candidate(candidate=candidate, decision="approved_for_later_promotion")

    candidate_entries = execution_result_promotion_candidates_to_history_entries([candidate])
    result_entries = execution_result_promotion_results_to_history_entries([result])
    finding_entries = execution_result_promotion_findings_to_history_entries(service.last_findings)
    decision_entries = execution_result_promotion_decisions_to_history_entries([service.last_decision])

    assert candidate_entries[0].source == "execution_result_promotion"
    assert result_entries[0].source == "execution_result_promotion"
    assert decision_entries[0].source == "execution_result_promotion"
    assert finding_entries == []
