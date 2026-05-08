from chanta_core.workspace import (
    WorkspaceReadService,
    workspace_file_list_results_to_history_entries,
    workspace_markdown_summary_results_to_history_entries,
    workspace_read_violations_to_history_entries,
    workspace_text_file_read_results_to_history_entries,
)


def test_workspace_read_history_adapters_convert_results_and_violations(tmp_path) -> None:
    (tmp_path / "doc.md").write_text("# Main\nBody", encoding="utf-8")
    service = WorkspaceReadService()
    root = service.register_read_root(tmp_path)

    listed = service.list_workspace_files(root=root, session_id="session:history")
    read = service.read_workspace_text_file(root=root, relative_path="doc.md", session_id="session:history")
    summary = service.summarize_workspace_markdown(root=root, relative_path="doc.md", session_id="session:history")
    denied = service.read_workspace_text_file(root=root, relative_path="../outside.md", session_id="session:history")
    violation = service.record_violation(
        request_kind="text_file_read",
        request_id=denied.request_id,
        root_id=root.root_id,
        relative_path="../outside.md",
        violation_type="path_traversal",
        message="denied",
        violation_attrs={"session_id": "session:history"},
    )

    list_entries = workspace_file_list_results_to_history_entries([listed])
    read_entries = workspace_text_file_read_results_to_history_entries([read])
    summary_entries = workspace_markdown_summary_results_to_history_entries([summary])
    violation_entries = workspace_read_violations_to_history_entries([violation])

    assert list_entries[0].source == "workspace_read"
    assert read_entries[0].refs[1]["ref_id"] == read.result_id
    assert summary_entries[0].entry_attrs["title"] == "Main"
    assert denied.denied is True
    assert violation_entries[0].source == "workspace_read"
    assert violation_entries[0].priority == 90
