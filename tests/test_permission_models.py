import pytest

from chanta_core.permissions.errors import PermissionDecisionError, PermissionPolicyNoteError
from chanta_core.permissions.ids import (
    new_permission_decision_id,
    new_permission_denial_id,
    new_permission_grant_id,
    new_permission_policy_note_id,
    new_permission_request_id,
    new_permission_scope_id,
)
from chanta_core.permissions.models import (
    PermissionDecision,
    PermissionDenial,
    PermissionGrant,
    PermissionPolicyNote,
    PermissionRequest,
    PermissionScope,
)
from chanta_core.utility.time import utc_now_iso


def test_permission_models_to_dict_and_ids() -> None:
    now = utc_now_iso()
    scope = PermissionScope(
        scope_id=new_permission_scope_id(),
        scope_name="Workspace read",
        scope_type="workspace",
        description="Read scope.",
        target_type="directory",
        target_ref=".",
        allowed_operations=["read"],
        denied_operations=["write"],
        risk_level="low",
        status="active",
        created_at=now,
        updated_at=now,
        scope_attrs={},
    )
    request = PermissionRequest(
        request_id=new_permission_request_id(),
        request_type="tool_use",
        requester_type="agent",
        requester_id="agent:test",
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="read",
        scope_id=scope.scope_id,
        risk_level="low",
        reason="test",
        status="created",
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
        decision_id=new_permission_decision_id(),
        request_id=request.request_id,
        decision="ask",
        decision_mode="manual",
        reason="test",
        decided_by="tester",
        confidence=0.5,
        created_at=now,
        decision_attrs={},
    )
    grant = PermissionGrant(
        grant_id=new_permission_grant_id(),
        request_id=request.request_id,
        scope_id=scope.scope_id,
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="read",
        status="active",
        granted_by="tester",
        granted_at=now,
        expires_at=None,
        session_id="session:test",
        grant_attrs={"inert_in_v0_12_0": True},
    )
    denial = PermissionDenial(
        denial_id=new_permission_denial_id(),
        request_id=request.request_id,
        scope_id=scope.scope_id,
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="write",
        reason="test",
        denied_by="tester",
        denied_at=now,
        session_id="session:test",
        denial_attrs={"inert_in_v0_12_0": True},
    )
    note = PermissionPolicyNote(
        policy_note_id=new_permission_policy_note_id(),
        scope_id=scope.scope_id,
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        note_type="review_needed",
        text="Review before future use.",
        status="active",
        priority=10,
        source_kind="test",
        created_at=now,
        updated_at=now,
        note_attrs={},
    )

    assert scope.to_dict()["scope_id"].startswith("permission_scope:")
    assert request.to_dict()["request_id"].startswith("permission_request:")
    assert decision.to_dict()["decision_id"].startswith("permission_decision:")
    assert grant.to_dict()["grant_id"].startswith("permission_grant:")
    assert denial.to_dict()["denial_id"].startswith("permission_denial:")
    assert note.to_dict()["policy_note_id"].startswith("permission_policy_note:")


def test_permission_decision_confidence_validation() -> None:
    with pytest.raises(PermissionDecisionError):
        PermissionDecision(
            decision_id=new_permission_decision_id(),
            request_id="permission_request:test",
            decision="ask",
            decision_mode="manual",
            reason=None,
            decided_by=None,
            confidence=1.5,
            created_at=utc_now_iso(),
            decision_attrs={},
        )


def test_forbidden_permission_policy_note_types_are_rejected() -> None:
    for note_type in ["enforce", "auto_allow", "auto_deny", "auto_block", "sandbox"]:
        with pytest.raises(PermissionPolicyNoteError):
            PermissionPolicyNote(
                policy_note_id=new_permission_policy_note_id(),
                scope_id=None,
                target_type=None,
                target_ref=None,
                note_type=note_type,
                text="forbidden",
                status="active",
                priority=None,
                source_kind="test",
                created_at=utc_now_iso(),
                updated_at=utc_now_iso(),
                note_attrs={},
            )
