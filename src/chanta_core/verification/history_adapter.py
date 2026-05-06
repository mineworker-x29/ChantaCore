from __future__ import annotations

from chanta_core.context.history import ContextHistoryEntry, new_context_history_entry_id
from chanta_core.verification.models import VerificationEvidence, VerificationResult


def verification_results_to_history_entries(
    results: list[VerificationResult],
) -> list[ContextHistoryEntry]:
    entries: list[ContextHistoryEntry] = []
    for index, result in enumerate(results):
        priority = _result_priority(result.status)
        content = _result_content(result)
        entries.append(
            ContextHistoryEntry(
                entry_id=new_context_history_entry_id(),
                session_id=None,
                process_instance_id=None,
                role="context",
                content=content,
                created_at=result.created_at,
                source="verification",
                priority=priority,
                refs=[
                    {
                        "ref_type": "verification_result",
                        "ref_id": result.result_id,
                        "result_id": result.result_id,
                        "run_id": result.run_id,
                        "contract_id": result.contract_id,
                        "target_id": result.target_id,
                        "evidence_ids": result.evidence_ids,
                        "status": result.status,
                    }
                ],
                entry_attrs={
                    "result_id": result.result_id,
                    "run_id": result.run_id,
                    "contract_id": result.contract_id,
                    "target_id": result.target_id,
                    "evidence_ids": result.evidence_ids,
                    "status": result.status,
                    "source_index": index,
                },
            )
        )
    return entries


def verification_evidence_to_history_entries(
    evidence_items: list[VerificationEvidence],
) -> list[ContextHistoryEntry]:
    entries: list[ContextHistoryEntry] = []
    for index, evidence in enumerate(evidence_items):
        entries.append(
            ContextHistoryEntry(
                entry_id=new_context_history_entry_id(),
                session_id=None,
                process_instance_id=None,
                role="context",
                content=evidence.content_preview,
                created_at=evidence.collected_at,
                source="verification",
                priority=55,
                refs=[
                    {
                        "ref_type": "verification_evidence",
                        "ref_id": evidence.evidence_id,
                        "evidence_id": evidence.evidence_id,
                        "run_id": evidence.run_id,
                        "target_id": evidence.target_id,
                        "evidence_kind": evidence.evidence_kind,
                    }
                ],
                entry_attrs={
                    "evidence_id": evidence.evidence_id,
                    "run_id": evidence.run_id,
                    "target_id": evidence.target_id,
                    "evidence_kind": evidence.evidence_kind,
                    "source_index": index,
                },
            )
        )
    return entries


def _result_priority(status: str) -> int:
    if status == "failed":
        return 90
    if status == "error":
        return 85
    if status == "inconclusive":
        return 70
    if status == "passed":
        return 55
    if status == "skipped":
        return 45
    return 50


def _result_content(result: VerificationResult) -> str:
    lines = [
        f"Verification result: {result.status}",
        f"Contract: {result.contract_id}",
    ]
    if result.target_id:
        lines.append(f"Target: {result.target_id}")
    if result.reason:
        lines.append(f"Reason: {result.reason}")
    if result.evidence_ids:
        lines.append(f"Evidence: {', '.join(result.evidence_ids)}")
    return "\n".join(lines)
