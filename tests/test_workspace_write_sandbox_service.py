from chanta_core.ocel.store import OCELStore
from chanta_core.sandbox import WorkspaceWriteSandboxService
from chanta_core.traces.trace_service import TraceService


def _service(tmp_path):
    store = OCELStore(tmp_path / "workspace_write_sandbox.sqlite")
    service = WorkspaceWriteSandboxService(trace_service=TraceService(ocel_store=store))
    return store, service


def test_workspace_write_sandbox_service_records_lifecycle_events(tmp_path) -> None:
    store, service = _service(tmp_path)
    root = service.register_workspace_root(root_path=str(tmp_path / "workspace"), root_name="test")
    updated_root = service.update_workspace_root(root=root, root_name="updated")
    service.deprecate_workspace_root(root=updated_root, reason="test")
    boundary = service.register_write_boundary(
        workspace_root_id=root.workspace_root_id,
        boundary_type="protected_path",
        path_ref="protected",
    )
    updated_boundary = service.update_write_boundary(boundary=boundary, priority=1)
    service.deprecate_write_boundary(boundary=updated_boundary, reason="test")
    intent = service.create_write_intent(
        workspace_root_id=root.workspace_root_id,
        target_path=str(tmp_path / "workspace" / "file.txt"),
        operation="write_file",
        session_id="session:sandbox",
        turn_id="conversation_turn:sandbox",
        process_instance_id="process_instance:sandbox",
        permission_request_id="permission_request:sandbox",
        session_permission_resolution_id="session_permission_resolution:sandbox",
    )
    service.evaluate_write_intent(intent=intent, workspace_root=root, boundaries=[])

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}
    assert {
        "workspace_root_registered",
        "workspace_root_updated",
        "workspace_root_deprecated",
        "workspace_write_boundary_registered",
        "workspace_write_boundary_updated",
        "workspace_write_boundary_deprecated",
        "workspace_write_intent_created",
        "workspace_write_sandbox_evaluated",
        "workspace_write_sandbox_decision_recorded",
    }.issubset(activities)


def test_workspace_write_sandbox_evaluation_policy(tmp_path) -> None:
    store, service = _service(tmp_path)
    root = service.register_workspace_root(root_path=str(tmp_path / "workspace"))
    protected = service.register_write_boundary(
        workspace_root_id=root.workspace_root_id,
        boundary_type="protected_path",
        path_ref="protected",
    )
    inside_intent = service.create_write_intent(
        workspace_root_id=root.workspace_root_id,
        target_path=str(tmp_path / "workspace" / "ok.txt"),
        operation="write_file",
    )
    outside_intent = service.create_write_intent(
        workspace_root_id=root.workspace_root_id,
        target_path=str(tmp_path / "outside.txt"),
        operation="write_file",
    )
    protected_intent = service.create_write_intent(
        workspace_root_id=root.workspace_root_id,
        target_path=str(tmp_path / "workspace" / "protected" / "secret.txt"),
        operation="write_file",
    )
    no_root_intent = service.create_write_intent(target_path="floating.txt", operation="write_file")

    inside_decision = service.evaluate_write_intent(intent=inside_intent, workspace_root=root)
    outside_decision = service.evaluate_write_intent(intent=outside_intent, workspace_root=root)
    protected_decision = service.evaluate_write_intent(
        intent=protected_intent,
        workspace_root=root,
        boundaries=[protected],
    )
    no_root_decision = service.evaluate_write_intent(intent=no_root_intent)

    assert inside_decision.decision == "allowed"
    assert inside_decision.decision_basis == "inside_workspace"
    assert inside_decision.enforcement_enabled is False
    assert outside_decision.decision == "denied"
    assert outside_decision.decision_basis == "outside_workspace"
    assert outside_decision.violation_ids
    assert outside_decision.enforcement_enabled is False
    assert protected_decision.decision == "denied"
    assert protected_decision.decision_basis == "protected_path"
    assert protected.boundary_id in protected_decision.matched_boundary_ids
    assert protected_decision.violation_ids
    assert no_root_decision.decision == "inconclusive"
    assert no_root_decision.decision_basis == "no_workspace_root"
    assert store.fetch_objects_by_type("workspace_write_sandbox_violation")


def test_workspace_write_sandbox_service_does_not_create_target_files(tmp_path) -> None:
    _, service = _service(tmp_path)
    root = service.register_workspace_root(root_path=str(tmp_path / "workspace"))
    target = tmp_path / "workspace" / "future.txt"
    intent = service.create_write_intent(
        workspace_root_id=root.workspace_root_id,
        target_path=str(target),
        operation="write_file",
    )

    decision = service.evaluate_write_intent(intent=intent, workspace_root=root)

    assert decision.decision == "allowed"
    assert not target.exists()
