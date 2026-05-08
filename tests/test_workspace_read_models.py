from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace.ids import (
    new_workspace_file_list_request_id,
    new_workspace_file_list_result_id,
    new_workspace_markdown_summary_request_id,
    new_workspace_markdown_summary_result_id,
    new_workspace_read_boundary_id,
    new_workspace_read_root_id,
    new_workspace_read_violation_id,
    new_workspace_text_file_read_request_id,
    new_workspace_text_file_read_result_id,
)
from chanta_core.workspace.models import (
    WorkspaceFileListRequest,
    WorkspaceFileListResult,
    WorkspaceMarkdownSummaryRequest,
    WorkspaceMarkdownSummaryResult,
    WorkspaceReadBoundary,
    WorkspaceReadRoot,
    WorkspaceReadViolation,
    WorkspaceTextFileReadRequest,
    WorkspaceTextFileReadResult,
)


def test_workspace_read_ids_use_expected_prefixes() -> None:
    assert new_workspace_read_root_id().startswith("workspace_read_root:")
    assert new_workspace_read_boundary_id().startswith("workspace_read_boundary:")
    assert new_workspace_file_list_request_id().startswith("workspace_file_list_request:")
    assert new_workspace_file_list_result_id().startswith("workspace_file_list_result:")
    assert new_workspace_text_file_read_request_id().startswith("workspace_text_file_read_request:")
    assert new_workspace_text_file_read_result_id().startswith("workspace_text_file_read_result:")
    assert new_workspace_markdown_summary_request_id().startswith("workspace_markdown_summary_request:")
    assert new_workspace_markdown_summary_result_id().startswith("workspace_markdown_summary_result:")
    assert new_workspace_read_violation_id().startswith("workspace_read_violation:")


def test_workspace_read_models_to_dict() -> None:
    now = utc_now_iso()
    root = WorkspaceReadRoot("root", "/repo", "repo", "active", now, now, {"read_only": True})
    boundary = WorkspaceReadBoundary("boundary", "root", "allow_root", ".", None, "active", 1, {})
    list_request = WorkspaceFileListRequest("list_req", "root", ".", None, False, 10, "session:1", None, None, None, None, now, {})
    list_result = WorkspaceFileListResult("list_res", "list_req", "root", [{"name": "a.md"}], 1, False, [], now, {})
    text_request = WorkspaceTextFileReadRequest("text_req", "root", "a.md", 10, 10, "utf-8", None, None, None, None, None, now, {})
    text_result = WorkspaceTextFileReadResult("text_res", "text_req", "root", "a.md", "abc", "abc", "hash", 3, False, False, [], now, {})
    md_request = WorkspaceMarkdownSummaryRequest("md_req", "root", "a.md", 10, 10, "outline_preview", None, None, None, now, {})
    md_result = WorkspaceMarkdownSummaryResult("md_res", "md_req", "root", "a.md", "Title", ["# Title"], "preview", "summary", "hash", False, False, [], now, {})
    violation = WorkspaceReadViolation("vio", "text_file_read", "text_req", "root", "../x", "path_traversal", "high", "denied", now, {})

    assert root.to_dict()["root_attrs"]["read_only"] is True
    assert boundary.to_dict()["boundary_type"] == "allow_root"
    assert list_request.to_dict()["max_results"] == 10
    assert list_result.to_dict()["entries"][0]["name"] == "a.md"
    assert text_request.to_dict()["encoding"] == "utf-8"
    assert text_result.to_dict()["denied"] is False
    assert md_request.to_dict()["summary_style"] == "outline_preview"
    assert md_result.to_dict()["heading_outline"] == ["# Title"]
    assert violation.to_dict()["violation_type"] == "path_traversal"
