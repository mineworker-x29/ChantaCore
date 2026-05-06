from pathlib import Path

from chanta_core.ocel.store import OCELStore
from chanta_core.sandbox import WorkspaceWriteSandboxService
from chanta_core.traces.trace_service import TraceService


def main() -> None:
    root_path = str(Path.cwd())
    service = WorkspaceWriteSandboxService(
        trace_service=TraceService(ocel_store=OCELStore("data/sandbox/test_workspace_write_sandbox.sqlite"))
    )
    root = service.register_workspace_root(root_path=root_path, root_name="ChantaCore")
    protected = service.register_write_boundary(
        workspace_root_id=root.workspace_root_id,
        boundary_type="protected_path",
        path_ref=".git",
        description="Protect repository metadata.",
    )

    inside = service.create_write_intent(
        workspace_root_id=root.workspace_root_id,
        target_path=str(Path(root_path) / "future_file.txt"),
        operation="write_file",
    )
    inside_decision = service.evaluate_write_intent(intent=inside, workspace_root=root)

    outside = service.create_write_intent(
        workspace_root_id=root.workspace_root_id,
        target_path=str(Path(root_path).parent / "outside.txt"),
        operation="write_file",
    )
    outside_decision = service.evaluate_write_intent(intent=outside, workspace_root=root)

    protected_intent = service.create_write_intent(
        workspace_root_id=root.workspace_root_id,
        target_path=str(Path(root_path) / ".git" / "config"),
        operation="write_file",
    )
    protected_decision = service.evaluate_write_intent(
        intent=protected_intent,
        workspace_root=root,
        boundaries=[protected],
    )

    print(f"workspace_root_id={root.workspace_root_id}")
    print(f"inside_decision={inside_decision.decision_id}:{inside_decision.decision}:enforcement={inside_decision.enforcement_enabled}")
    print(f"outside_decision={outside_decision.decision_id}:{outside_decision.decision}:violations={len(outside_decision.violation_ids)}:enforcement={outside_decision.enforcement_enabled}")
    print(f"protected_decision={protected_decision.decision_id}:{protected_decision.decision}:violations={len(protected_decision.violation_ids)}:enforcement={protected_decision.enforcement_enabled}")


if __name__ == "__main__":
    main()
