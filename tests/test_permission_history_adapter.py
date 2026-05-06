from chanta_core.permissions.history_adapter import (
    permission_decisions_to_history_entries,
    permission_denials_to_history_entries,
    permission_grants_to_history_entries,
    permission_requests_to_history_entries,
)
from chanta_core.permissions.models import (
    PermissionDecision,
    PermissionDenial,
    PermissionGrant,
    PermissionRequest,
)
from chanta_core.utility.time import utc_now_iso


def test_permission_history_adapters_preserve_refs() -> None:
    now = utc_now_iso()
    request = PermissionRequest(
        request_id="permission_request:test",
        request_type="tool_use",
        requester_type="agent",
        requester_id="agent:test",
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="read",
        scope_id="permission_scope:test",
        risk_level="low",
        reason=None,
        status="pending",
        session_id="session:test",
        turn_id="conversation_turn:test",
        process_instance_id="process_instance:test",
        tool_descriptor_id="tool_descriptor:workspace",
        verification_result_ids=["verification_result:test"],
        outcome_evaluation_ids=["process_outcome_evaluation:test"],
        created_at=now,
        request_attrs={},
    )
    decision = PermissionDecision(
        decision_id="permission_decision:test",
        request_id=request.request_id,
        decision="ask",
        decision_mode="manual",
        reason=None,
        decided_by=None,
        confidence=None,
        created_at=now,
        decision_attrs={},
    )
    grant = PermissionGrant(
        grant_id="permission_grant:test",
        request_id=request.request_id,
        scope_id=request.scope_id,
        target_type=request.target_type,
        target_ref=request.target_ref,
        operation=request.operation,
        status="active",
        granted_by=None,
        granted_at=now,
        expires_at=None,
        session_id=request.session_id,
        grant_attrs={"inert_in_v0_12_0": True},
    )
    denial = PermissionDenial(
        denial_id="permission_denial:test",
        request_id=request.request_id,
        scope_id=request.scope_id,
        target_type=request.target_type,
        target_ref=request.target_ref,
        operation="write",
        reason=None,
        denied_by=None,
        denied_at=now,
        session_id=request.session_id,
        denial_attrs={"inert_in_v0_12_0": True},
    )

    request_entry = permission_requests_to_history_entries([request])[0]
    decision_entry = permission_decisions_to_history_entries([decision])[0]
    grant_entry = permission_grants_to_history_entries([grant])[0]
    denial_entry = permission_denials_to_history_entries([denial])[0]

    assert request_entry.source == "permission"
    assert request_entry.priority > grant_entry.priority
    assert denial_entry.priority > grant_entry.priority
    assert request_entry.refs[0]["request_id"] == request.request_id
    assert request_entry.refs[0]["scope_id"] == request.scope_id
    assert request_entry.refs[0]["tool_descriptor_id"] == request.tool_descriptor_id
    assert request_entry.refs[0]["verification_result_ids"] == request.verification_result_ids
    assert request_entry.refs[0]["outcome_evaluation_ids"] == request.outcome_evaluation_ids
    assert decision_entry.refs[0]["decision_id"] == decision.decision_id
    assert grant_entry.refs[0]["grant_id"] == grant.grant_id
    assert denial_entry.refs[0]["denial_id"] == denial.denial_id
