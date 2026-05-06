from chanta_core.ocel.store import OCELStore
from chanta_core.permissions import PermissionModelService, SessionPermissionService
from chanta_core.traces.trace_service import TraceService


def test_session_permission_ocel_shape_contains_expected_objects_and_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "session_permission_shape.sqlite")
    trace_service = TraceService(ocel_store=store)
    permission_service = PermissionModelService(trace_service=trace_service)
    service = SessionPermissionService(permission_model_service=permission_service)

    context = service.create_context(session_id="session:shape")
    request = service.create_session_permission_request(
        session_id="session:shape",
        request_type="tool_use",
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="read",
    )
    grant = service.attach_grant_to_session(
        session_id="session:shape",
        target_type=request.target_type,
        target_ref=request.target_ref,
        operation=request.operation,
        request_id=request.request_id,
    )
    denial = service.attach_denial_to_session(
        session_id="session:shape",
        target_type=request.target_type,
        target_ref=request.target_ref,
        operation="write",
        request_id=request.request_id,
    )
    service.build_snapshot(
        session_id="session:shape",
        context_id=context.context_id,
        grants=[grant],
        denials=[denial],
        requests=[request],
    )
    resolution = service.resolve_request(session_id="session:shape", request=request, grants=[grant], denials=[])

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}
    assert {
        "session_permission_context_created",
        "session_permission_request_created",
        "session_permission_grant_attached",
        "session_permission_denial_attached",
        "session_permission_snapshot_created",
        "session_permission_resolution_recorded",
        "session_permission_request_resolved",
    }.issubset(activities)
    assert store.fetch_objects_by_type("session_permission_context")
    assert store.fetch_objects_by_type("session_permission_snapshot")
    assert store.fetch_objects_by_type("session_permission_resolution")
    assert store.fetch_objects_by_type("permission_request")
    assert store.fetch_objects_by_type("permission_grant")
    assert store.fetch_objects_by_type("permission_denial")
    resolution_attrs = store.fetch_objects_by_type("session_permission_resolution")[0]["object_attrs"]
    assert resolution_attrs["enforcement_enabled"] is False
    assert resolution.resolved_decision == "allow"
