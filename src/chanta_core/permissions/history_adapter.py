from __future__ import annotations

from chanta_core.context.history import ContextHistoryEntry, new_context_history_entry_id
from chanta_core.permissions.models import (
    PermissionDecision,
    PermissionDenial,
    PermissionGrant,
    PermissionRequest,
)
from chanta_core.permissions.session import (
    SessionPermissionContext,
    SessionPermissionResolution,
    SessionPermissionSnapshot,
)


def permission_requests_to_history_entries(requests: list[PermissionRequest]) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=request.session_id,
            process_instance_id=request.process_instance_id,
            role="context",
            content=f"Permission request: {request.status}\nTarget: {request.target_type}:{request.target_ref}\nOperation: {request.operation}",
            created_at=request.created_at,
            source="permission",
            priority=85 if request.status == "pending" else 55,
            refs=[_request_ref(request)],
            entry_attrs={"request_id": request.request_id, "status": request.status},
        )
        for request in requests
    ]


def permission_decisions_to_history_entries(decisions: list[PermissionDecision]) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Permission decision: {decision.decision}\nRequest: {decision.request_id}",
            created_at=decision.created_at,
            source="permission",
            priority=75 if decision.decision in {"ask", "defer", "inconclusive"} else 55,
            refs=[
                {
                    "ref_type": "permission_decision",
                    "ref_id": decision.decision_id,
                    "decision_id": decision.decision_id,
                    "request_id": decision.request_id,
                    "decision": decision.decision,
                }
            ],
            entry_attrs={"decision_id": decision.decision_id, "request_id": decision.request_id},
        )
        for decision in decisions
    ]


def permission_grants_to_history_entries(grants: list[PermissionGrant]) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=grant.session_id,
            process_instance_id=None,
            role="context",
            content=f"Permission grant record: {grant.status}\nTarget: {grant.target_type}:{grant.target_ref}\nOperation: {grant.operation}",
            created_at=grant.granted_at,
            source="permission",
            priority=60,
            refs=[
                {
                    "ref_type": "permission_grant",
                    "ref_id": grant.grant_id,
                    "grant_id": grant.grant_id,
                    "request_id": grant.request_id,
                    "scope_id": grant.scope_id,
                    "session_id": grant.session_id,
                }
            ],
            entry_attrs={"grant_id": grant.grant_id, "request_id": grant.request_id, "scope_id": grant.scope_id},
        )
        for grant in grants
    ]


def permission_denials_to_history_entries(denials: list[PermissionDenial]) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=denial.session_id,
            process_instance_id=None,
            role="context",
            content=f"Permission denial record\nTarget: {denial.target_type}:{denial.target_ref}\nOperation: {denial.operation}",
            created_at=denial.denied_at,
            source="permission",
            priority=90,
            refs=[
                {
                    "ref_type": "permission_denial",
                    "ref_id": denial.denial_id,
                    "denial_id": denial.denial_id,
                    "request_id": denial.request_id,
                    "scope_id": denial.scope_id,
                    "session_id": denial.session_id,
                }
            ],
            entry_attrs={"denial_id": denial.denial_id, "request_id": denial.request_id, "scope_id": denial.scope_id},
        )
        for denial in denials
    ]


def session_permission_contexts_to_history_entries(
    contexts: list[SessionPermissionContext],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=context.session_id,
            process_instance_id=None,
            role="context",
            content=(
                f"Session permission context: {context.status}\n"
                f"Active grants: {len(context.active_grant_ids)}\n"
                f"Active denials: {len(context.active_denial_ids)}\n"
                f"Pending requests: {len(context.pending_request_ids)}"
            ),
            created_at=context.created_at,
            source="session_permission",
            priority=50 if context.status == "active" else 60,
            refs=[
                {
                    "ref_type": "session_permission_context",
                    "ref_id": context.context_id,
                    "context_id": context.context_id,
                    "session_id": context.session_id,
                    "active_grant_ids": context.active_grant_ids,
                    "active_denial_ids": context.active_denial_ids,
                    "pending_request_ids": context.pending_request_ids,
                }
            ],
            entry_attrs={"context_id": context.context_id, "status": context.status},
        )
        for context in contexts
    ]


def session_permission_snapshots_to_history_entries(
    snapshots: list[SessionPermissionSnapshot],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=snapshot.session_id,
            process_instance_id=None,
            role="context",
            content=(
                f"Session permission snapshot\n"
                f"Active grants: {len(snapshot.active_grant_ids)}\n"
                f"Active denials: {len(snapshot.active_denial_ids)}\n"
                f"Pending requests: {len(snapshot.pending_request_ids)}"
            ),
            created_at=snapshot.created_at,
            source="session_permission",
            priority=55 if snapshot.expired_grant_ids else 45,
            refs=[
                {
                    "ref_type": "session_permission_snapshot",
                    "ref_id": snapshot.snapshot_id,
                    "snapshot_id": snapshot.snapshot_id,
                    "context_id": snapshot.context_id,
                    "session_id": snapshot.session_id,
                    "active_grant_ids": snapshot.active_grant_ids,
                    "active_denial_ids": snapshot.active_denial_ids,
                    "pending_request_ids": snapshot.pending_request_ids,
                    "expired_grant_ids": snapshot.expired_grant_ids,
                    "revoked_grant_ids": snapshot.revoked_grant_ids,
                }
            ],
            entry_attrs={"snapshot_id": snapshot.snapshot_id, "context_id": snapshot.context_id},
        )
        for snapshot in snapshots
    ]


def session_permission_resolutions_to_history_entries(
    resolutions: list[SessionPermissionResolution],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=resolution.session_id,
            process_instance_id=None,
            role="context",
            content=(
                f"Session permission resolution: {resolution.resolved_decision}\n"
                f"Basis: {resolution.resolution_basis}\n"
                f"Request: {resolution.request_id}"
            ),
            created_at=resolution.created_at,
            source="session_permission",
            priority=_resolution_priority(resolution),
            refs=[
                {
                    "ref_type": "session_permission_resolution",
                    "ref_id": resolution.resolution_id,
                    "resolution_id": resolution.resolution_id,
                    "session_id": resolution.session_id,
                    "request_id": resolution.request_id,
                    "matched_grant_ids": resolution.matched_grant_ids,
                    "matched_denial_ids": resolution.matched_denial_ids,
                    "expired_grant_ids": resolution.expired_grant_ids,
                }
            ],
            entry_attrs={
                "resolution_id": resolution.resolution_id,
                "request_id": resolution.request_id,
                "resolved_decision": resolution.resolved_decision,
                "resolution_basis": resolution.resolution_basis,
            },
        )
        for resolution in resolutions
    ]


def _request_ref(request: PermissionRequest) -> dict:
    return {
        "ref_type": "permission_request",
        "ref_id": request.request_id,
        "request_id": request.request_id,
        "scope_id": request.scope_id,
        "session_id": request.session_id,
        "turn_id": request.turn_id,
        "process_instance_id": request.process_instance_id,
        "tool_descriptor_id": request.tool_descriptor_id,
        "verification_result_ids": request.verification_result_ids,
        "outcome_evaluation_ids": request.outcome_evaluation_ids,
    }


def _resolution_priority(resolution: SessionPermissionResolution) -> int:
    if resolution.resolved_decision == "deny":
        return 90
    if resolution.resolved_decision in {"ask", "inconclusive"}:
        return 85 if resolution.expired_grant_ids else 80
    if resolution.resolved_decision == "allow":
        return 60
    return 55
