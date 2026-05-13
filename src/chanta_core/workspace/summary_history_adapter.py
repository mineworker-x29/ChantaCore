from __future__ import annotations

from chanta_core.context.history import ContextHistoryEntry, new_context_history_entry_id
from chanta_core.workspace.summary import (
    WorkspaceReadSummaryCandidate,
    WorkspaceReadSummaryFinding,
    WorkspaceReadSummaryRequest,
    WorkspaceReadSummaryResult,
)


def workspace_read_summary_requests_to_history_entries(
    requests: list[WorkspaceReadSummaryRequest],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=request.session_id,
            process_instance_id=request.process_instance_id,
            role="context",
            content=f"Workspace Read Summary requested: input_kind={request.input_kind}.",
            created_at=request.created_at,
            source="workspace_read_summary",
            priority=45,
            refs=[{"ref_type": "workspace_read_summary_request", "ref_id": request.summary_request_id}],
            entry_attrs={"input_kind": request.input_kind, "source_kind": request.source_kind},
        )
        for request in requests
    ]


def workspace_read_summary_results_to_history_entries(
    results: list[WorkspaceReadSummaryResult],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=result.summary_text,
            created_at=result.created_at,
            source="workspace_read_summary",
            priority=85 if result.status in {"failed", "error"} else 55,
            refs=[
                {"ref_type": "workspace_read_summary_result", "ref_id": result.summary_result_id},
                {"ref_type": "workspace_read_summary_request", "ref_id": result.summary_request_id},
            ],
            entry_attrs={
                "status": result.status,
                "input_kind": result.input_kind,
                "truncated": result.truncated,
                "section_count": len(result.section_ids),
            },
        )
        for result in results
    ]


def workspace_read_summary_candidates_to_history_entries(
    candidates: list[WorkspaceReadSummaryCandidate],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Workspace Read Summary Candidate: target={candidate.target_kind}; status={candidate.review_status}.",
            created_at=candidate.created_at,
            source="workspace_read_summary",
            priority=65 if candidate.review_status == "pending_review" else 50,
            refs=[
                {"ref_type": "workspace_read_summary_candidate", "ref_id": candidate.summary_candidate_id},
                {"ref_type": "workspace_read_summary_result", "ref_id": candidate.summary_result_id},
            ],
            entry_attrs={
                "target_kind": candidate.target_kind,
                "review_status": candidate.review_status,
                "canonical_promotion_enabled": candidate.canonical_promotion_enabled,
            },
        )
        for candidate in candidates
    ]


def workspace_read_summary_findings_to_history_entries(
    findings: list[WorkspaceReadSummaryFinding],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Workspace Read Summary Finding: {finding.finding_type}; status={finding.status}.",
            created_at=finding.created_at,
            source="workspace_read_summary",
            priority=90 if finding.finding_type == "private_content_risk" or finding.status in {"failed", "error"} else 60,
            refs=[{"ref_type": "workspace_read_summary_finding", "ref_id": finding.finding_id}],
            entry_attrs={
                "finding_type": finding.finding_type,
                "status": finding.status,
                "severity": finding.severity,
            },
        )
        for finding in findings
    ]
