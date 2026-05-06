from chanta_core.ocel.store import OCELStore
from chanta_core.permissions import PermissionModelService
from chanta_core.traces.trace_service import TraceService
from chanta_core.tools.dispatcher import ToolDispatcher


def test_permission_model_service_records_lifecycle_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "permission_service.sqlite")
    service = PermissionModelService(trace_service=TraceService(ocel_store=store))

    scope = service.register_scope(
        scope_name="Tool read",
        scope_type="tool",
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        allowed_operations=["read"],
    )
    updated_scope = service.update_scope(scope=scope, risk_level="low")
    service.deprecate_scope(scope=updated_scope, reason="test")
    request = service.create_request(
        request_type="tool_use",
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="read",
        scope_id=scope.scope_id,
        session_id="session:permission",
        turn_id="conversation_turn:permission",
        process_instance_id="process_instance:permission",
        tool_descriptor_id="tool_descriptor:workspace",
        verification_result_ids=["verification_result:permission"],
        outcome_evaluation_ids=["process_outcome_evaluation:permission"],
    )
    pending = service.mark_request_pending(request=request)
    service.cancel_request(request=pending)
    service.expire_request(request=pending)
    decision = service.record_decision(
        request_id=request.request_id,
        decision="ask",
        decision_mode="manual",
        confidence=0.7,
    )
    grant = service.record_grant(
        request_id=request.request_id,
        scope_id=scope.scope_id,
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="read",
        session_id="session:permission",
    )
    service.revoke_grant(grant=grant)
    service.expire_grant(grant=grant)
    denial = service.record_denial(
        request_id=request.request_id,
        scope_id=scope.scope_id,
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="write",
        session_id="session:permission",
    )
    note = service.register_policy_note(
        scope_id=scope.scope_id,
        note_type="review_needed",
        text="Review only.",
        source_kind="test",
    )
    service.update_policy_note(note=note, text="Updated.")
    service.deprecate_policy_note(note=note)

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}
    assert decision.decision == "ask"
    assert grant.grant_attrs["inert_in_v0_12_0"] is True
    assert denial.denial_attrs["inert_in_v0_12_0"] is True
    assert {
        "permission_scope_registered",
        "permission_scope_updated",
        "permission_scope_deprecated",
        "permission_request_created",
        "permission_request_marked_pending",
        "permission_request_cancelled",
        "permission_request_expired",
        "permission_decision_recorded",
        "permission_grant_recorded",
        "permission_grant_revoked",
        "permission_grant_expired",
        "permission_denial_recorded",
        "permission_policy_note_registered",
        "permission_policy_note_updated",
        "permission_policy_note_deprecated",
    }.issubset(activities)


def test_permission_model_service_does_not_mutate_runtime_dispatcher(tmp_path) -> None:
    store = OCELStore(tmp_path / "permission_no_runtime.sqlite")
    service = PermissionModelService(trace_service=TraceService(ocel_store=store))
    before_handlers = dict(ToolDispatcher()._handlers)

    scope = service.register_scope(scope_name="Manual", scope_type="manual")
    request = service.create_request(
        request_type="manual",
        target_type="manual",
        target_ref="manual:test",
        operation="review",
        scope_id=scope.scope_id,
    )
    service.record_decision(request_id=request.request_id, decision="allow", decision_mode="manual")
    service.record_grant(
        request_id=request.request_id,
        scope_id=scope.scope_id,
        target_type="manual",
        target_ref="manual:test",
        operation="review",
    )

    assert ToolDispatcher()._handlers.keys() == before_handlers.keys()
