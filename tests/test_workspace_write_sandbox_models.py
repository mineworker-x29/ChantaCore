import pytest

from chanta_core.sandbox.errors import WorkspaceWriteSandboxDecisionError
from chanta_core.sandbox.ids import (
    new_workspace_root_id,
    new_workspace_write_boundary_id,
    new_workspace_write_intent_id,
    new_workspace_write_sandbox_decision_id,
    new_workspace_write_sandbox_violation_id,
)
from chanta_core.sandbox.models import (
    WorkspaceRoot,
    WorkspaceWriteBoundary,
    WorkspaceWriteIntent,
    WorkspaceWriteSandboxDecision,
    WorkspaceWriteSandboxViolation,
)
from chanta_core.utility.time import utc_now_iso


def test_workspace_write_sandbox_models_to_dict() -> None:
    now = utc_now_iso()
    root = WorkspaceRoot(
        workspace_root_id=new_workspace_root_id(),
        root_path="C:/workspace",
        root_name="workspace",
        status="active",
        created_at=now,
        updated_at=now,
        root_attrs={"normalized_root_path": "C:/workspace"},
    )
    boundary = WorkspaceWriteBoundary(
        boundary_id=new_workspace_write_boundary_id(),
        workspace_root_id=root.workspace_root_id,
        boundary_type="protected_path",
        path_ref="secrets",
        description="protected",
        status="active",
        priority=1,
    )
    intent = WorkspaceWriteIntent(
        intent_id=new_workspace_write_intent_id(),
        workspace_root_id=root.workspace_root_id,
        target_path="C:/workspace/file.txt",
        operation="write_file",
        requester_type="test",
        requester_id="tester",
        session_id="session:sandbox",
        turn_id="conversation_turn:sandbox",
        process_instance_id="process_instance:sandbox",
        permission_request_id="permission_request:sandbox",
        session_permission_resolution_id="session_permission_resolution:sandbox",
        reason="test",
        created_at=now,
    )
    decision = WorkspaceWriteSandboxDecision(
        decision_id=new_workspace_write_sandbox_decision_id(),
        intent_id=intent.intent_id,
        workspace_root_id=root.workspace_root_id,
        decision="allowed",
        decision_basis="inside_workspace",
        normalized_target_path="C:/workspace/file.txt",
        normalized_root_path="C:/workspace",
        inside_workspace=True,
        matched_boundary_ids=[],
        violation_ids=[],
        confidence=1.0,
        reason="inside",
        enforcement_enabled=False,
        created_at=now,
    )
    violation = WorkspaceWriteSandboxViolation(
        violation_id=new_workspace_write_sandbox_violation_id(),
        intent_id=intent.intent_id,
        violation_type="outside_workspace",
        severity="high",
        message="outside",
        target_path="C:/outside.txt",
        workspace_root_id=root.workspace_root_id,
        created_at=now,
    )

    assert root.to_dict()["workspace_root_id"].startswith("workspace_root:")
    assert boundary.to_dict()["boundary_id"].startswith("workspace_write_boundary:")
    assert intent.to_dict()["intent_id"].startswith("workspace_write_intent:")
    assert decision.to_dict()["decision_id"].startswith("workspace_write_sandbox_decision:")
    assert decision.to_dict()["enforcement_enabled"] is False
    assert violation.to_dict()["violation_id"].startswith("workspace_write_sandbox_violation:")


def test_workspace_write_sandbox_ids_use_expected_prefixes() -> None:
    assert new_workspace_root_id().startswith("workspace_root:")
    assert new_workspace_write_boundary_id().startswith("workspace_write_boundary:")
    assert new_workspace_write_intent_id().startswith("workspace_write_intent:")
    assert new_workspace_write_sandbox_decision_id().startswith("workspace_write_sandbox_decision:")
    assert new_workspace_write_sandbox_violation_id().startswith("workspace_write_sandbox_violation:")


def test_workspace_write_sandbox_decision_validates_confidence_and_marker() -> None:
    now = utc_now_iso()
    with pytest.raises(WorkspaceWriteSandboxDecisionError):
        WorkspaceWriteSandboxDecision(
            decision_id=new_workspace_write_sandbox_decision_id(),
            intent_id="workspace_write_intent:x",
            workspace_root_id=None,
            decision="allowed",
            decision_basis="inside_workspace",
            normalized_target_path=None,
            normalized_root_path=None,
            inside_workspace=True,
            matched_boundary_ids=[],
            violation_ids=[],
            confidence=1.5,
            reason=None,
            enforcement_enabled=False,
            created_at=now,
        )
    with pytest.raises(WorkspaceWriteSandboxDecisionError):
        WorkspaceWriteSandboxDecision(
            decision_id=new_workspace_write_sandbox_decision_id(),
            intent_id="workspace_write_intent:x",
            workspace_root_id=None,
            decision="allowed",
            decision_basis="inside_workspace",
            normalized_target_path=None,
            normalized_root_path=None,
            inside_workspace=True,
            matched_boundary_ids=[],
            violation_ids=[],
            confidence=1.0,
            reason=None,
            enforcement_enabled=True,
            created_at=now,
        )
