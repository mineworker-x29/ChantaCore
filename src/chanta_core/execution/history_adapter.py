from __future__ import annotations

from chanta_core.context.history import ContextHistoryEntry, new_context_history_entry_id
from chanta_core.execution.models import (
    ExecutionEnvelope,
    ExecutionOutcomeSummary,
    ExecutionProvenanceRecord,
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
