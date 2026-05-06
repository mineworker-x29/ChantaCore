from __future__ import annotations

from pathlib import Path

from chanta_core.ocel.store import OCELStore
from chanta_core.permissions import PermissionModelService
from chanta_core.traces.trace_service import TraceService


def main() -> None:
    store = OCELStore(Path("data/permissions/test_permission_model.sqlite"))
    service = PermissionModelService(trace_service=TraceService(ocel_store=store))

    scope = service.register_scope(
        scope_name="Tool descriptor read",
        scope_type="tool",
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        allowed_operations=["read"],
        risk_level="low",
    )
    request = service.create_request(
        request_type="tool_use",
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="read",
        scope_id=scope.scope_id,
        session_id="session:permission-script",
    )
    decision = service.record_decision(
        request_id=request.request_id,
        decision="ask",
        decision_mode="manual",
        reason="Manual review record.",
    )
    grant = service.record_grant(
        request_id=request.request_id,
        scope_id=scope.scope_id,
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="read",
        granted_by="test",
        session_id="session:permission-script",
    )
    denial = service.record_denial(
        request_id=request.request_id,
        scope_id=scope.scope_id,
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="write",
        reason="Write is outside this record.",
        denied_by="test",
        session_id="session:permission-script",
    )
    note = service.register_policy_note(
        scope_id=scope.scope_id,
        note_type="review_needed",
        text="Review before future activation.",
        priority=10,
        source_kind="test",
    )

    print(f"scope_id={scope.scope_id}")
    print(f"request_id={request.request_id}:{request.status}")
    print(f"decision_id={decision.decision_id}:{decision.decision}")
    print(f"grant_id={grant.grant_id}:{grant.status}:inert={grant.grant_attrs['inert_in_v0_12_0']}")
    print(f"denial_id={denial.denial_id}:inert={denial.denial_attrs['inert_in_v0_12_0']}")
    print(f"policy_note_id={note.policy_note_id}:{note.note_type}")


if __name__ == "__main__":
    main()
