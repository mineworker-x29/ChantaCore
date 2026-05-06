from __future__ import annotations

from chanta_core.context.history import ContextHistoryEntry, new_context_history_entry_id
from chanta_core.outcomes.models import ProcessOutcomeEvaluation


def process_outcome_evaluations_to_history_entries(
    evaluations: list[ProcessOutcomeEvaluation],
) -> list[ContextHistoryEntry]:
    entries: list[ContextHistoryEntry] = []
    for index, evaluation in enumerate(evaluations):
        entries.append(
            ContextHistoryEntry(
                entry_id=new_context_history_entry_id(),
                session_id=None,
                process_instance_id=None,
                role="context",
                content=_evaluation_content(evaluation),
                created_at=evaluation.created_at,
                source="process_outcome",
                priority=_evaluation_priority(evaluation.outcome_status),
                refs=[
                    {
                        "ref_type": "process_outcome_evaluation",
                        "ref_id": evaluation.evaluation_id,
                        "evaluation_id": evaluation.evaluation_id,
                        "contract_id": evaluation.contract_id,
                        "target_id": evaluation.target_id,
                        "signal_ids": evaluation.signal_ids,
                        "verification_result_ids": evaluation.verification_result_ids,
                        "outcome_status": evaluation.outcome_status,
                    }
                ],
                entry_attrs={
                    "evaluation_id": evaluation.evaluation_id,
                    "contract_id": evaluation.contract_id,
                    "target_id": evaluation.target_id,
                    "signal_ids": evaluation.signal_ids,
                    "verification_result_ids": evaluation.verification_result_ids,
                    "outcome_status": evaluation.outcome_status,
                    "score": evaluation.score,
                    "confidence": evaluation.confidence,
                    "evidence_coverage": evaluation.evidence_coverage,
                    "source_index": index,
                },
            )
        )
    return entries


def _evaluation_priority(outcome_status: str) -> int:
    if outcome_status in {"failed", "error", "needs_review"}:
        return 90
    if outcome_status in {"partial_success", "inconclusive"}:
        return 70
    if outcome_status == "success":
        return 55
    if outcome_status == "skipped":
        return 45
    return 50


def _evaluation_content(evaluation: ProcessOutcomeEvaluation) -> str:
    lines = [
        f"Process outcome: {evaluation.outcome_status}",
        f"Contract: {evaluation.contract_id}",
        f"Target: {evaluation.target_id}",
    ]
    if evaluation.score is not None:
        lines.append(f"Score: {evaluation.score}")
    if evaluation.confidence is not None:
        lines.append(f"Confidence: {evaluation.confidence}")
    if evaluation.evidence_coverage is not None:
        lines.append(f"Evidence coverage: {evaluation.evidence_coverage}")
    if evaluation.reason:
        lines.append(f"Reason: {evaluation.reason}")
    return "\n".join(lines)
