from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService
from chanta_core.workspace import WorkspaceReadService


def test_workspace_read_ocel_shape_contains_expected_objects_and_events(tmp_path) -> None:
    (tmp_path / "doc.md").write_text("# Main\nBody", encoding="utf-8")
    store = OCELStore(tmp_path / "workspace_read_shape.sqlite")
    service = WorkspaceReadService(trace_service=TraceService(ocel_store=store))
    root = service.register_read_root(tmp_path)
    service.register_read_boundary(root_id=root.root_id, boundary_type="root_constrained", path_ref=".")
    service.list_workspace_files(root=root)
    service.read_workspace_text_file(root=root, relative_path="doc.md")
    service.summarize_workspace_markdown(root=root, relative_path="doc.md")
    service.read_workspace_text_file(root=root, relative_path="../outside.md")

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}
    assert {
        "workspace_read_root_registered",
        "workspace_read_boundary_registered",
        "workspace_file_list_requested",
        "workspace_file_list_completed",
        "workspace_text_file_read_requested",
        "workspace_text_file_read_completed",
        "workspace_markdown_summary_requested",
        "workspace_markdown_summary_completed",
        "workspace_text_file_read_denied",
        "workspace_read_violation_recorded",
    }.issubset(activities)
    for object_type in [
        "workspace_read_root",
        "workspace_read_boundary",
        "workspace_file_list_request",
        "workspace_file_list_result",
        "workspace_text_file_read_request",
        "workspace_text_file_read_result",
        "workspace_markdown_summary_request",
        "workspace_markdown_summary_result",
        "workspace_read_violation",
    ]:
        assert store.fetch_objects_by_type(object_type)
