from chanta_core.ocel.store import OCELStore
from chanta_core.permissions import PermissionModelService, SessionPermissionService
from chanta_core.traces.trace_service import TraceService


def main() -> None:
    store = OCELStore("data/permissions/test_session_permission.sqlite")
    trace_service = TraceService(ocel_store=store)
    permission_service = PermissionModelService(trace_service=trace_service)
    session_service = SessionPermissionService(permission_model_service=permission_service)

    context = session_service.create_context(session_id="session:permission-script")
    request = session_service.create_session_permission_request(
        session_id="session:permission-script",
        request_type="tool_use",
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="read",
    )
    grant = session_service.attach_grant_to_session(
        session_id="session:permission-script",
        target_type=request.target_type,
        target_ref=request.target_ref,
        operation=request.operation,
        request_id=request.request_id,
    )
    allow_resolution = session_service.resolve_request(
        session_id="session:permission-script",
        request=request,
        grants=[grant],
    )

    denied_request = session_service.create_session_permission_request(
        session_id="session:permission-script",
        request_type="tool_use",
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="write",
    )
    denial = session_service.attach_denial_to_session(
        session_id="session:permission-script",
        target_type=denied_request.target_type,
        target_ref=denied_request.target_ref,
        operation=denied_request.operation,
        request_id=denied_request.request_id,
    )
    deny_resolution = session_service.resolve_request(
        session_id="session:permission-script",
        request=denied_request,
        denials=[denial],
    )

    expired_request = session_service.create_session_permission_request(
        session_id="session:permission-script",
        request_type="tool_use",
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="list",
    )
    expired_grant = session_service.attach_grant_to_session(
        session_id="session:permission-script",
        target_type=expired_request.target_type,
        target_ref=expired_request.target_ref,
        operation=expired_request.operation,
        request_id=expired_request.request_id,
        expires_at="2020-01-01T00:00:00Z",
    )
    expired_resolution = session_service.resolve_request(
        session_id="session:permission-script",
        request=expired_request,
        grants=[expired_grant],
        now_iso="2026-01-01T00:00:00Z",
    )
    snapshot = session_service.build_snapshot(
        session_id="session:permission-script",
        context_id=context.context_id,
        grants=[grant, expired_grant],
        denials=[denial],
        requests=[request, denied_request, expired_request],
        now_iso="2026-01-01T00:00:00Z",
    )

    print(f"context_id={context.context_id}:{context.status}")
    print(f"request_id={request.request_id}:{request.status}")
    print(f"grant_id={grant.grant_id}:{grant.status}")
    print(f"allow_resolution={allow_resolution.resolution_id}:{allow_resolution.resolved_decision}:enforcement={allow_resolution.enforcement_enabled}")
    print(f"denial_id={denial.denial_id}")
    print(f"deny_resolution={deny_resolution.resolution_id}:{deny_resolution.resolved_decision}:enforcement={deny_resolution.enforcement_enabled}")
    print(f"expired_resolution={expired_resolution.resolution_id}:{expired_resolution.resolution_basis}:{expired_resolution.resolved_decision}")
    print(f"snapshot_id={snapshot.snapshot_id}:active_grants={len(snapshot.active_grant_ids)}:expired_grants={len(snapshot.expired_grant_ids)}")


if __name__ == "__main__":
    main()
