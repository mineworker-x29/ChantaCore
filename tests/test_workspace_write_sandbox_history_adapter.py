from chanta_core.sandbox import (
    workspace_write_intents_to_history_entries,
    workspace_write_sandbox_decisions_to_history_entries,
    workspace_write_sandbox_violations_to_history_entries,
)
from chanta_core.sandbox.models import (
    WorkspaceWriteIntent,
    WorkspaceWriteSandboxDecision,
    WorkspaceWriteSandboxViolation,
)
from chanta_core.utility.time import utc_now_iso


def test_workspace_write_sandbox_history_adapters_convert_objects() -> None:
    now = utc_now_iso()
    intent = WorkspaceWriteIntent(
        intent_id="workspace_write_intent:history",
        workspace_root_id="workspace_root:history",
        target_path="file.txt",
        operation="write_file",
        requester_type="test",
        requester_id="tester",
        session_id="session:history",
        turn_id="conversation_turn:history",
        process_instance_id="process_instance:history",
        permission_request_id="permission_request:history",
        session_permission_resolution_id="session_permission_resolution:history",
        reason=None,
        created_at=now,
    )
    allowed = WorkspaceWriteSandboxDecision(
        decision_id="workspace_write_sandbox_decision:allowed",
        intent_id=intent.intent_id,
        workspace_root_id=intent.workspace_root_id,
        decision="allowed",
        decision_basis="inside_workspace",
        normalized_target_path="file.txt",
        normalized_root_path=".",
        inside_workspace=True,
        matched_boundary_ids=[],
        violation_ids=[],
        confidence=1.0,
        reason=None,
        enforcement_enabled=False,
        created_at=now,
    )
    denied = WorkspaceWriteSandboxDecision(
        decision_id="workspace_write_sandbox_decision:denied",
        intent_id=intent.intent_id,
        workspace_root_id=intent.workspace_root_id,
        decision="denied",
        decision_basis="outside_workspace",
        normalized_target_path="outside.txt",
        normalized_root_path=".",
        inside_workspace=False,
        matched_boundary_ids=[],
        violation_ids=["workspace_write_sandbox_violation:history"],
        confidence=1.0,
        reason=None,
        enforcement_enabled=False,
        created_at=now,
    )
    violation = WorkspaceWriteSandboxViolation(
        violation_id="workspace_write_sandbox_violation:history",
        intent_id=intent.intent_id,
        violation_type="outside_workspace",
        severity="high",
        message="outside",
        target_path="outside.txt",
        workspace_root_id=intent.workspace_root_id,
        created_at=now,
    )

    intent_entry = workspace_write_intents_to_history_entries([intent])[0]
    decision_entries = workspace_write_sandbox_decisions_to_history_entries([allowed, denied])
    violation_entry = workspace_write_sandbox_violations_to_history_entries([violation])[0]

    assert intent_entry.source == "workspace_write_sandbox"
    assert intent_entry.refs[0]["permission_request_id"] == "permission_request:history"
    assert decision_entries[1].priority > decision_entries[0].priority
    assert decision_entries[1].refs[0]["violation_ids"] == ["workspace_write_sandbox_violation:history"]
    assert violation_entry.priority == 90
    assert violation_entry.refs[0]["violation_id"] == violation.violation_id
