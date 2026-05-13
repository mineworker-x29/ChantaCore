from __future__ import annotations

from chanta_core.context.history import ContextHistoryEntry, new_context_history_entry_id
from chanta_core.execution.models import (
    ExecutionEnvelope,
    ExecutionOutcomeSummary,
    ExecutionProvenanceRecord,
)
from chanta_core.execution.audit import (
    ExecutionAuditFinding,
    ExecutionAuditQuery,
    ExecutionAuditResult,
)
from chanta_core.execution.promotion import (
    ExecutionResultPromotionCandidate,
    ExecutionResultPromotionDecision,
    ExecutionResultPromotionFinding,
    ExecutionResultPromotionResult,
)


def execution_envelopes_to_history_entries(
    envelopes: list[ExecutionEnvelope],
) -> list[ContextHistoryEntry]:
    priority_by_status = {
        "completed": 60,
        "blocked": 85,
        "denied": 85,
        "failed": 90,
        "unsupported": 80,
        "needs_review": 75,
        "skipped": 45,
        "error": 90,
    }
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=envelope.session_id,
            process_instance_id=envelope.process_instance_id,
            role="context",
            content=(
                f"Execution Envelope: kind={envelope.execution_kind}; "
                f"skill={envelope.skill_id or 'none'}; status={envelope.status}."
            ),
            created_at=envelope.created_at,
            source="execution_envelope",
            priority=priority_by_status.get(envelope.status, 55),
            refs=[{"ref_type": "execution_envelope", "ref_id": envelope.envelope_id}],
            entry_attrs={
                "execution_kind": envelope.execution_kind,
                "skill_id": envelope.skill_id,
                "status": envelope.status,
                "execution_performed": envelope.execution_performed,
                "blocked": envelope.blocked,
            },
        )
        for envelope in envelopes
    ]


def execution_outcome_summaries_to_history_entries(
    summaries: list[ExecutionOutcomeSummary],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Execution Outcome Summary: status={summary.status}; "
                f"blocked={summary.blocked}; failed={summary.failed}."
            ),
            created_at=summary.created_at,
            source="execution_envelope",
            priority=85 if summary.blocked or summary.failed else 60,
            refs=[
                {"ref_type": "execution_outcome_summary", "ref_id": summary.summary_id},
                {"ref_type": "execution_envelope", "ref_id": summary.envelope_id},
            ],
            entry_attrs={
                "status": summary.status,
                "blocked": summary.blocked,
                "failed": summary.failed,
                "violation_count": len(summary.violation_ids),
                "finding_count": len(summary.finding_ids),
            },
        )
        for summary in summaries
    ]


def execution_provenance_records_to_history_entries(
    records: list[ExecutionProvenanceRecord],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                "Execution Provenance: "
                f"invocation={record.explicit_invocation_result_id or 'none'}; "
                f"gate={record.gate_result_id or 'none'}."
            ),
            created_at=record.created_at,
            source="execution_envelope",
            priority=50,
            refs=[
                {"ref_type": "execution_provenance_record", "ref_id": record.provenance_id},
                {"ref_type": "execution_envelope", "ref_id": record.envelope_id},
            ],
            entry_attrs={
                "runtime_kind": record.runtime_kind,
                "invocation_mode": record.invocation_mode,
                "has_gate": bool(record.gate_result_id),
                "has_invocation": bool(record.explicit_invocation_result_id),
            },
        )
        for record in records
    ]


def execution_audit_queries_to_history_entries(
    queries: list[ExecutionAuditQuery],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=query.session_id,
            process_instance_id=None,
            role="context",
            content=f"Execution Audit Query: type={query.query_type}; limit={query.limit}.",
            created_at=query.created_at,
            source="execution_audit",
            priority=45,
            refs=[{"ref_type": "execution_audit_query", "ref_id": query.audit_query_id}],
            entry_attrs={
                "query_type": query.query_type,
                "show_paths": query.show_paths,
                "show_full_payloads": query.show_full_payloads,
                "read_only": True,
            },
        )
        for query in queries
    ]


def execution_audit_results_to_history_entries(
    results: list[ExecutionAuditResult],
) -> list[ContextHistoryEntry]:
    priority_by_status = {
        "completed": 50,
        "empty": 40,
        "not_found": 65,
        "error": 85,
    }
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Execution Audit Result: status={result.status}; "
                f"matched={result.matched_count}; returned={result.returned_count}."
            ),
            created_at=result.created_at,
            source="execution_audit",
            priority=priority_by_status.get(result.status, 50),
            refs=[
                {"ref_type": "execution_audit_result", "ref_id": result.audit_result_id},
                {"ref_type": "execution_audit_query", "ref_id": result.audit_query_id},
            ],
            entry_attrs={
                "status": result.status,
                "matched_count": result.matched_count,
                "returned_count": result.returned_count,
            },
        )
        for result in results
    ]


def execution_audit_findings_to_history_entries(
    findings: list[ExecutionAuditFinding],
) -> list[ContextHistoryEntry]:
    def priority(finding: ExecutionAuditFinding) -> int:
        if finding.status in {"blocked", "failed"} or finding.severity == "high":
            return 85
        if finding.status == "not_found":
            return 65
        if finding.status == "empty":
            return 45
        return 50

    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Execution Audit Finding: type={finding.finding_type}; "
                f"status={finding.status}; severity={finding.severity}."
            ),
            created_at=finding.created_at,
            source="execution_audit",
            priority=priority(finding),
            refs=[
                {"ref_type": "execution_audit_finding", "ref_id": finding.finding_id},
                {"ref_type": "execution_audit_query", "ref_id": finding.audit_query_id},
            ]
            + (
                [{"ref_type": "execution_envelope", "ref_id": finding.envelope_id}]
                if finding.envelope_id
                else []
            ),
            entry_attrs={
                "finding_type": finding.finding_type,
                "status": finding.status,
                "severity": finding.severity,
            },
        )
        for finding in findings
    ]


def execution_result_promotion_candidates_to_history_entries(
    candidates: list[ExecutionResultPromotionCandidate],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Execution Result Promotion Candidate: target={candidate.target_kind}; "
                f"status={candidate.review_status}."
            ),
            created_at=candidate.created_at,
            source="execution_result_promotion",
            priority=65 if candidate.review_status == "pending_review" else 55,
            refs=[
                {"ref_type": "execution_result_promotion_candidate", "ref_id": candidate.candidate_id},
                {"ref_type": "execution_envelope", "ref_id": candidate.envelope_id},
            ],
            entry_attrs={
                "target_kind": candidate.target_kind,
                "review_status": candidate.review_status,
                "canonical_promotion_enabled": candidate.canonical_promotion_enabled,
                "private": candidate.private,
                "sensitive": candidate.sensitive,
            },
        )
        for candidate in candidates
    ]


def execution_result_promotion_results_to_history_entries(
    results: list[ExecutionResultPromotionResult],
) -> list[ContextHistoryEntry]:
    priority_by_status = {
        "approved_for_later_promotion": 75,
        "pending_review": 65,
        "rejected": 60,
        "no_action": 55,
        "archived": 45,
    }
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Execution Result Promotion Result: status={result.status}; "
                f"promoted={result.promoted}."
            ),
            created_at=result.created_at,
            source="execution_result_promotion",
            priority=priority_by_status.get(result.status, 60),
            refs=[
                {"ref_type": "execution_result_promotion_result", "ref_id": result.result_id},
                {"ref_type": "execution_result_promotion_candidate", "ref_id": result.candidate_id},
            ],
            entry_attrs={
                "status": result.status,
                "promoted": result.promoted,
                "canonical_promotion_enabled": result.canonical_promotion_enabled,
            },
        )
        for result in results
    ]


def execution_result_promotion_findings_to_history_entries(
    findings: list[ExecutionResultPromotionFinding],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Execution Result Promotion Finding: type={finding.finding_type}; "
                f"status={finding.status}; severity={finding.severity}."
            ),
            created_at=finding.created_at,
            source="execution_result_promotion",
            priority=90 if finding.finding_type == "private_content_risk" else 65,
            refs=[
                {"ref_type": "execution_result_promotion_finding", "ref_id": finding.finding_id},
                {"ref_type": "execution_result_promotion_candidate", "ref_id": finding.candidate_id},
                {"ref_type": "execution_envelope", "ref_id": finding.envelope_id},
            ],
            entry_attrs={
                "finding_type": finding.finding_type,
                "status": finding.status,
                "severity": finding.severity,
            },
        )
        for finding in findings
    ]


def execution_result_promotion_decisions_to_history_entries(
    decisions: list[ExecutionResultPromotionDecision],
) -> list[ContextHistoryEntry]:
    priority_by_decision = {
        "approved_for_later_promotion": 75,
        "rejected": 60,
        "no_action": 55,
        "needs_more_info": 65,
        "archive": 45,
        "error": 85,
    }
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Execution Result Promotion Decision: decision={decision.decision}; "
                f"can_promote_now={decision.can_promote_now}."
            ),
            created_at=decision.created_at,
            source="execution_result_promotion",
            priority=priority_by_decision.get(decision.decision, 60),
            refs=[
                {"ref_type": "execution_result_promotion_decision", "ref_id": decision.decision_id},
                {"ref_type": "execution_result_promotion_candidate", "ref_id": decision.candidate_id},
            ],
            entry_attrs={
                "decision": decision.decision,
                "can_promote_now": decision.can_promote_now,
                "requires_manual_action": decision.requires_manual_action,
            },
        )
        for decision in decisions
    ]
