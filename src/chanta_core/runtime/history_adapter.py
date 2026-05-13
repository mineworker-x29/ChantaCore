from __future__ import annotations

from chanta_core.context.history import ContextHistoryEntry, new_context_history_entry_id
from chanta_core.runtime.workbench import (
    PersonalRuntimeWorkbenchFinding,
    PersonalRuntimeWorkbenchPendingItem,
    PersonalRuntimeWorkbenchRecentActivity,
    PersonalRuntimeWorkbenchResult,
    PersonalRuntimeWorkbenchSnapshot,
)


def personal_runtime_workbench_snapshots_to_history_entries(
    snapshots: list[PersonalRuntimeWorkbenchSnapshot],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Personal Runtime Workbench snapshot: activation={item.activation_status}; pending={item.pending_review_count}.",
            created_at=item.created_at,
            source="personal_runtime_workbench",
            priority=55 if item.pending_review_count else 40,
            refs=[{"ref_type": "personal_runtime_workbench_snapshot", "ref_id": item.snapshot_id}],
            entry_attrs={
                "activation_status": item.activation_status,
                "conformance_status": item.conformance_status,
                "smoke_status": item.smoke_status,
                "read_only": True,
            },
        )
        for item in snapshots
    ]


def personal_runtime_workbench_results_to_history_entries(
    results: list[PersonalRuntimeWorkbenchResult],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=item.summary,
            created_at=item.created_at,
            source="personal_runtime_workbench",
            priority=60 if item.status == "needs_review" else 45,
            refs=[
                {"ref_type": "personal_runtime_workbench_result", "ref_id": item.result_id},
                {"ref_type": "personal_runtime_workbench_snapshot", "ref_id": item.snapshot_id},
            ],
            entry_attrs={"command_name": item.command_name, "status": item.status, "read_only": True},
        )
        for item in results
    ]


def personal_runtime_workbench_pending_items_to_history_entries(
    items: list[PersonalRuntimeWorkbenchPendingItem],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Workbench pending item: {item.item_type}; status={item.status}.",
            created_at=item.created_at,
            source="personal_runtime_workbench",
            priority=75 if "review" in item.item_type else 60,
            refs=[{"ref_type": "personal_runtime_workbench_pending_item", "ref_id": item.pending_item_id}],
            entry_attrs={"item_type": item.item_type, "status": item.status, "priority": item.priority},
        )
        for item in items
    ]


def personal_runtime_workbench_recent_activities_to_history_entries(
    activities: list[PersonalRuntimeWorkbenchRecentActivity],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Workbench recent activity: {item.activity_type}; status={item.status}.",
            created_at=item.created_at,
            source="personal_runtime_workbench",
            priority=85 if item.blocked or item.failed else 50,
            refs=[{"ref_type": "personal_runtime_workbench_recent_activity", "ref_id": item.activity_id}],
            entry_attrs={
                "activity_type": item.activity_type,
                "status": item.status,
                "blocked": item.blocked,
                "failed": item.failed,
                "skill_id": item.skill_id,
            },
        )
        for item in activities
    ]


def personal_runtime_workbench_findings_to_history_entries(
    findings: list[PersonalRuntimeWorkbenchFinding],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=item.message,
            created_at=item.created_at,
            source="personal_runtime_workbench",
            priority=75 if item.finding_type == "missing_personal_directory" else 85 if item.severity == "high" else 60,
            refs=[{"ref_type": "personal_runtime_workbench_finding", "ref_id": item.finding_id}],
            entry_attrs={
                "finding_type": item.finding_type,
                "status": item.status,
                "severity": item.severity,
            },
        )
        for item in findings
    ]
