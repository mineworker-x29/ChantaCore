from chanta_core.ocel.store import OCELStore
from chanta_core.permissions import PermissionModelService, SessionPermissionService
from chanta_core.traces.trace_service import TraceService


def _services(tmp_path):
    store = OCELStore(tmp_path / "session_permission.sqlite")
    trace_service = TraceService(ocel_store=store)
    permission_service = PermissionModelService(trace_service=trace_service)
    session_service = SessionPermissionService(permission_model_service=permission_service)
    return store, permission_service, session_service


def test_session_permission_service_records_lifecycle_events(tmp_path) -> None:
    store, _, service = _services(tmp_path)

    context = service.create_context(session_id="session:sp", active_scope_ids=["permission_scope:sp"])
    request = service.create_session_permission_request(
        session_id="session:sp",
        request_type="tool_use",
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="read",
        turn_id="conversation_turn:sp",
        process_instance_id="process_instance:sp",
    )
    grant = service.attach_grant_to_session(
        session_id="session:sp",
        target_type=request.target_type,
        target_ref=request.target_ref,
        operation=request.operation,
        request_id=request.request_id,
    )
    denial = service.attach_denial_to_session(
        session_id="session:sp",
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="write",
        request_id=request.request_id,
    )
    context = service.update_context(
        context=context,
        active_grant_ids=[grant.grant_id],
        active_denial_ids=[denial.denial_id],
        pending_request_ids=[request.request_id],
    )
    service.build_snapshot(
        session_id="session:sp",
        context_id=context.context_id,
        grants=[grant],
        denials=[denial],
        requests=[request],
    )
    service.resolve_request(session_id="session:sp", request=request, grants=[grant], denials=[])
    service.close_context(context=context)
    service.revoke_session_grant(grant=grant)
    service.expire_session_grants(
        session_id="session:sp",
        grants=[
            service.attach_grant_to_session(
                session_id="session:sp",
                target_type="tool_descriptor",
                target_ref="tool_descriptor:workspace",
                operation="list",
                expires_at="2020-01-01T00:00:00Z",
            )
        ],
        now_iso="2026-01-01T00:00:00Z",
    )
    service.reset_context(session_id="session:child", parent_session_id="session:sp")

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}
    assert {
        "session_permission_context_created",
        "session_permission_context_updated",
        "session_permission_context_closed",
        "session_permission_context_reset",
        "session_permission_request_created",
        "session_permission_grant_attached",
        "session_permission_grant_revoked",
        "session_permission_grant_expired",
        "session_permission_denial_attached",
        "session_permission_snapshot_created",
        "session_permission_resolution_recorded",
        "session_permission_request_resolved",
        "session_permission_non_inheritance_recorded",
    }.issubset(activities)


def test_session_permission_resolution_policy(tmp_path) -> None:
    _, _, service = _services(tmp_path)
    request = service.create_session_permission_request(
        session_id="session:sp",
        request_type="tool_use",
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="read",
    )
    grant = service.attach_grant_to_session(
        session_id="session:sp",
        target_type=request.target_type,
        target_ref=request.target_ref,
        operation=request.operation,
    )
    other_session_grant = service.attach_grant_to_session(
        session_id="session:other",
        target_type=request.target_type,
        target_ref=request.target_ref,
        operation=request.operation,
    )
    denial = service.attach_denial_to_session(
        session_id="session:sp",
        target_type=request.target_type,
        target_ref=request.target_ref,
        operation=request.operation,
    )
    expired = service.attach_grant_to_session(
        session_id="session:sp",
        target_type=request.target_type,
        target_ref=request.target_ref,
        operation="write",
        expires_at="2020-01-01T00:00:00Z",
    )
    expired_request = service.create_session_permission_request(
        session_id="session:sp",
        request_type="tool_use",
        target_type=request.target_type,
        target_ref=request.target_ref,
        operation="write",
    )
    missing_request = service.create_session_permission_request(
        session_id="session:sp",
        request_type="tool_use",
        target_type=request.target_type,
        target_ref=request.target_ref,
        operation="delete",
    )

    allow_resolution = service.resolve_request(session_id="session:sp", request=request, grants=[grant], denials=[])
    deny_resolution = service.resolve_request(session_id="session:sp", request=request, grants=[grant], denials=[denial])
    other_session_resolution = service.resolve_request(
        session_id="session:sp",
        request=request,
        grants=[other_session_grant],
        denials=[],
    )
    expired_resolution = service.resolve_request(
        session_id="session:sp",
        request=expired_request,
        grants=[expired],
        denials=[],
        now_iso="2026-01-01T00:00:00Z",
    )
    missing_resolution = service.resolve_request(session_id="session:sp", request=missing_request)

    assert allow_resolution.resolved_decision == "allow"
    assert allow_resolution.resolution_basis == "matching_grant"
    assert allow_resolution.enforcement_enabled is False
    assert deny_resolution.resolved_decision == "deny"
    assert deny_resolution.resolution_basis == "matching_denial"
    assert deny_resolution.enforcement_enabled is False
    assert other_session_resolution.resolved_decision == "ask"
    assert other_session_resolution.resolution_basis == "no_match"
    assert expired_resolution.resolved_decision == "ask"
    assert expired_resolution.resolution_basis == "expired_grant"
    assert expired.grant_id in expired_resolution.expired_grant_ids
    assert missing_resolution.resolved_decision == "ask"
    assert missing_resolution.resolution_basis == "no_match"


def test_session_permission_snapshot_and_reset_do_not_copy_parent_grants(tmp_path) -> None:
    _, _, service = _services(tmp_path)
    parent_grant = service.attach_grant_to_session(
        session_id="session:parent",
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="read",
    )
    child_context = service.reset_context(session_id="session:child", parent_session_id="session:parent")
    snapshot = service.build_snapshot(
        session_id="session:child",
        context_id=child_context.context_id,
        grants=[parent_grant],
    )

    assert child_context.active_grant_ids == []
    assert child_context.context_attrs["parent_grants_copied"] is False
    assert snapshot.active_grant_ids == []
