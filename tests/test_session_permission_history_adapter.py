from chanta_core.permissions import (
    session_permission_contexts_to_history_entries,
    session_permission_resolutions_to_history_entries,
    session_permission_snapshots_to_history_entries,
)
from chanta_core.permissions.session import (
    SessionPermissionContext,
    SessionPermissionResolution,
    SessionPermissionSnapshot,
)
from chanta_core.utility.time import utc_now_iso


def test_session_permission_history_adapters_convert_objects() -> None:
    now = utc_now_iso()
    context = SessionPermissionContext(
        context_id="session_permission_context:history",
        session_id="session:history",
        status="active",
        created_at=now,
        updated_at=now,
        active_scope_ids=[],
        active_grant_ids=["permission_grant:history"],
        active_denial_ids=[],
        pending_request_ids=["permission_request:history"],
    )
    snapshot = SessionPermissionSnapshot(
        snapshot_id="session_permission_snapshot:history",
        session_id="session:history",
        context_id=context.context_id,
        created_at=now,
        active_grant_ids=context.active_grant_ids,
        active_denial_ids=[],
        pending_request_ids=context.pending_request_ids,
        expired_grant_ids=["permission_grant:expired"],
        revoked_grant_ids=[],
        summary=None,
    )
    allow_resolution = SessionPermissionResolution(
        resolution_id="session_permission_resolution:allow",
        session_id="session:history",
        request_id="permission_request:history",
        resolved_decision="allow",
        resolution_basis="matching_grant",
        matched_grant_ids=["permission_grant:history"],
        matched_denial_ids=[],
        expired_grant_ids=[],
        confidence=1.0,
        reason=None,
        enforcement_enabled=False,
        created_at=now,
    )
    deny_resolution = SessionPermissionResolution(
        resolution_id="session_permission_resolution:deny",
        session_id="session:history",
        request_id="permission_request:history",
        resolved_decision="deny",
        resolution_basis="matching_denial",
        matched_grant_ids=[],
        matched_denial_ids=["permission_denial:history"],
        expired_grant_ids=[],
        confidence=1.0,
        reason=None,
        enforcement_enabled=False,
        created_at=now,
    )

    context_entry = session_permission_contexts_to_history_entries([context])[0]
    snapshot_entry = session_permission_snapshots_to_history_entries([snapshot])[0]
    resolution_entries = session_permission_resolutions_to_history_entries([allow_resolution, deny_resolution])

    assert context_entry.source == "session_permission"
    assert snapshot_entry.refs[0]["snapshot_id"] == snapshot.snapshot_id
    assert resolution_entries[0].refs[0]["resolution_id"] == allow_resolution.resolution_id
    assert resolution_entries[0].refs[0]["matched_grant_ids"] == ["permission_grant:history"]
    assert resolution_entries[1].refs[0]["matched_denial_ids"] == ["permission_denial:history"]
    assert resolution_entries[1].priority > resolution_entries[0].priority
