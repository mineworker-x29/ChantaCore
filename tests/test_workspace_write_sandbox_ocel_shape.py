from chanta_core.ocel.store import OCELStore
from chanta_core.sandbox import WorkspaceWriteSandboxService
from chanta_core.traces.trace_service import TraceService


def test_workspace_write_sandbox_ocel_shape_contains_expected_objects_and_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "workspace_write_sandbox_shape.sqlite")
    service = WorkspaceWriteSandboxService(trace_service=TraceService(ocel_store=store))
    root = service.register_workspace_root(root_path=str(tmp_path / "workspace"))
    boundary = service.register_write_boundary(
        workspace_root_id=root.workspace_root_id,
        boundary_type="denied_path",
        path_ref="blocked",
    )
    intent = service.create_write_intent(
        workspace_root_id=root.workspace_root_id,
        target_path=str(tmp_path / "workspace" / "blocked" / "file.txt"),
        operation="write_file",
    )
    decision = service.evaluate_write_intent(intent=intent, workspace_root=root, boundaries=[boundary])

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}
    assert {
        "workspace_root_registered",
        "workspace_write_boundary_registered",
        "workspace_write_intent_created",
        "workspace_write_sandbox_evaluated",
        "workspace_write_sandbox_decision_recorded",
        "workspace_write_sandbox_violation_recorded",
    }.issubset(activities)
    assert store.fetch_objects_by_type("workspace_root")
    assert store.fetch_objects_by_type("workspace_write_boundary")
    assert store.fetch_objects_by_type("workspace_write_intent")
    assert store.fetch_objects_by_type("workspace_write_sandbox_decision")
    assert store.fetch_objects_by_type("workspace_write_sandbox_violation")
    attrs = store.fetch_objects_by_type("workspace_write_sandbox_decision")[0]["object_attrs"]
    assert attrs["enforcement_enabled"] is False
    assert decision.decision == "denied"
