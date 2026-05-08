from __future__ import annotations

from chanta_core.context.history import ContextHistoryEntry, new_context_history_entry_id
from chanta_core.workspace.models import (
    WorkspaceFileListResult,
    WorkspaceMarkdownSummaryResult,
    WorkspaceReadViolation,
    WorkspaceTextFileReadResult,
)


def workspace_file_list_results_to_history_entries(
    results: list[WorkspaceFileListResult],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=result.result_attrs.get("session_id"),
            process_instance_id=result.result_attrs.get("process_instance_id"),
            role="context",
            content=f"Workspace file list result: {result.total_entries} entries",
            created_at=result.created_at,
            source="workspace_read",
            priority=65 if result.violation_ids else 45,
            refs=_result_refs(result.request_id, result.result_id, result.root_id, result.violation_ids),
            entry_attrs={
                "relative_path": result.result_attrs.get("relative_path"),
                "truncated": result.truncated,
            },
        )
        for result in results
    ]


def workspace_text_file_read_results_to_history_entries(
    results: list[WorkspaceTextFileReadResult],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=result.result_attrs.get("session_id"),
            process_instance_id=result.result_attrs.get("process_instance_id"),
            role="context",
            content=result.content_preview,
            created_at=result.created_at,
            source="workspace_read",
            priority=80 if result.denied else 55,
            refs=_result_refs(result.request_id, result.result_id, result.root_id, result.violation_ids),
            entry_attrs={
                "relative_path": result.relative_path,
                "content_hash": result.content_hash,
                "truncated": result.truncated,
                "denied": result.denied,
            },
        )
        for result in results
    ]


def workspace_markdown_summary_results_to_history_entries(
    results: list[WorkspaceMarkdownSummaryResult],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=result.result_attrs.get("session_id"),
            process_instance_id=result.result_attrs.get("process_instance_id"),
            role="context",
            content=result.summary,
            created_at=result.created_at,
            source="workspace_read",
            priority=80 if result.denied else 60,
            refs=_result_refs(result.request_id, result.result_id, result.root_id, result.violation_ids),
            entry_attrs={
                "relative_path": result.relative_path,
                "title": result.title,
                "heading_outline": list(result.heading_outline),
                "content_hash": result.content_hash,
                "truncated": result.truncated,
                "denied": result.denied,
            },
        )
        for result in results
    ]


def workspace_read_violations_to_history_entries(
    violations: list[WorkspaceReadViolation],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=violation.violation_attrs.get("session_id"),
            process_instance_id=violation.violation_attrs.get("process_instance_id"),
            role="context",
            content=violation.message,
            created_at=violation.created_at,
            source="workspace_read",
            priority=90,
            refs=[
                {"ref_type": "workspace_read_violation", "ref_id": violation.violation_id},
                {"ref_type": "workspace_read_request", "ref_id": violation.request_id},
                {"ref_type": "workspace_read_root", "ref_id": violation.root_id},
            ],
            entry_attrs={
                "request_kind": violation.request_kind,
                "relative_path": violation.relative_path,
                "violation_type": violation.violation_type,
                "severity": violation.severity,
            },
        )
        for violation in violations
    ]


def _result_refs(
    request_id: str,
    result_id: str,
    root_id: str,
    violation_ids: list[str],
) -> list[dict[str, str]]:
    return [
        {"ref_type": "workspace_read_request", "ref_id": request_id},
        {"ref_type": "workspace_read_result", "ref_id": result_id},
        {"ref_type": "workspace_read_root", "ref_id": root_id},
        *[
            {"ref_type": "workspace_read_violation", "ref_id": violation_id}
            for violation_id in violation_ids
        ],
    ]
