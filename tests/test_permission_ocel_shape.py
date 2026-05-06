from chanta_core.ocel.store import OCELStore
from chanta_core.permissions import PermissionModelService
from chanta_core.traces.trace_service import TraceService


def test_permission_ocel_shape_contains_expected_objects_and_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "permission_shape.sqlite")
    service = PermissionModelService(trace_service=TraceService(ocel_store=store))

    scope = service.register_scope(scope_name="Tool scope", scope_type="tool")
    request = service.create_request(
        request_type="tool_use",
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="read",
        scope_id=scope.scope_id,
    )
    service.record_decision(request_id=request.request_id, decision="ask", decision_mode="manual")
    service.record_grant(
        request_id=request.request_id,
        scope_id=scope.scope_id,
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="read",
    )
    service.record_denial(
        request_id=request.request_id,
        scope_id=scope.scope_id,
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="write",
    )
    service.register_policy_note(scope_id=scope.scope_id, note_type="review_needed", text="Review.")

    activities = {event["event_activity"] for event in store.fetch_recent_events(50)}
    assert {
        "permission_scope_registered",
        "permission_request_created",
        "permission_decision_recorded",
        "permission_grant_recorded",
        "permission_denial_recorded",
        "permission_policy_note_registered",
    }.issubset(activities)
    assert store.fetch_objects_by_type("permission_scope")
    assert store.fetch_objects_by_type("permission_request")
    assert store.fetch_objects_by_type("permission_decision")
    assert store.fetch_objects_by_type("permission_grant")
    assert store.fetch_objects_by_type("permission_denial")
    assert store.fetch_objects_by_type("permission_policy_note")
    grant_attrs = store.fetch_objects_by_type("permission_grant")[0]["object_attrs"]
    note_attrs = store.fetch_objects_by_type("permission_policy_note")[0]["object_attrs"]
    assert grant_attrs["inert_in_v0_12_0"] is True
    assert note_attrs["enforcement_enabled"] is False
