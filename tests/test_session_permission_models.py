import pytest

from chanta_core.permissions.errors import SessionPermissionResolutionError
from chanta_core.permissions.ids import (
    new_session_permission_context_id,
    new_session_permission_resolution_id,
    new_session_permission_snapshot_id,
)
from chanta_core.permissions.session import (
    SessionPermissionContext,
    SessionPermissionResolution,
    SessionPermissionSnapshot,
)
from chanta_core.utility.time import utc_now_iso


def test_session_permission_models_to_dict() -> None:
    now = utc_now_iso()
    context = SessionPermissionContext(
        context_id=new_session_permission_context_id(),
        session_id="session:model",
        status="active",
        created_at=now,
        updated_at=now,
        active_scope_ids=["permission_scope:1"],
        active_grant_ids=["permission_grant:1"],
        active_denial_ids=["permission_denial:1"],
        pending_request_ids=["permission_request:1"],
        context_attrs={"k": "v"},
    )
    snapshot = SessionPermissionSnapshot(
        snapshot_id=new_session_permission_snapshot_id(),
        session_id="session:model",
        context_id=context.context_id,
        created_at=now,
        active_grant_ids=context.active_grant_ids,
        active_denial_ids=context.active_denial_ids,
        pending_request_ids=context.pending_request_ids,
        expired_grant_ids=["permission_grant:expired"],
        revoked_grant_ids=["permission_grant:revoked"],
        summary="summary",
        snapshot_attrs={"s": True},
    )
    resolution = SessionPermissionResolution(
        resolution_id=new_session_permission_resolution_id(),
        session_id="session:model",
        request_id="permission_request:1",
        resolved_decision="allow",
        resolution_basis="matching_grant",
        matched_grant_ids=["permission_grant:1"],
        matched_denial_ids=[],
        expired_grant_ids=[],
        confidence=1.0,
        reason="test",
        enforcement_enabled=False,
        created_at=now,
        resolution_attrs={"r": True},
    )

    assert context.to_dict()["context_id"].startswith("session_permission_context:")
    assert snapshot.to_dict()["snapshot_id"].startswith("session_permission_snapshot:")
    assert resolution.to_dict()["resolution_id"].startswith("session_permission_resolution:")
    assert resolution.to_dict()["enforcement_enabled"] is False


def test_session_permission_ids_use_expected_prefixes() -> None:
    assert new_session_permission_context_id().startswith("session_permission_context:")
    assert new_session_permission_snapshot_id().startswith("session_permission_snapshot:")
    assert new_session_permission_resolution_id().startswith("session_permission_resolution:")


def test_session_permission_resolution_validates_confidence_and_runtime_marker() -> None:
    now = utc_now_iso()
    with pytest.raises(SessionPermissionResolutionError):
        SessionPermissionResolution(
            resolution_id=new_session_permission_resolution_id(),
            session_id="session:model",
            request_id="permission_request:1",
            resolved_decision="allow",
            resolution_basis="matching_grant",
            matched_grant_ids=[],
            matched_denial_ids=[],
            expired_grant_ids=[],
            confidence=1.5,
            reason=None,
            enforcement_enabled=False,
            created_at=now,
        )
    with pytest.raises(SessionPermissionResolutionError):
        SessionPermissionResolution(
            resolution_id=new_session_permission_resolution_id(),
            session_id="session:model",
            request_id="permission_request:1",
            resolved_decision="allow",
            resolution_basis="matching_grant",
            matched_grant_ids=[],
            matched_denial_ids=[],
            expired_grant_ids=[],
            confidence=1.0,
            reason=None,
            enforcement_enabled=True,
            created_at=now,
        )
