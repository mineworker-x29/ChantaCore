from __future__ import annotations

from uuid import uuid4


def new_workspace_read_root_id() -> str:
    return f"workspace_read_root:{uuid4()}"


def new_workspace_read_boundary_id() -> str:
    return f"workspace_read_boundary:{uuid4()}"


def new_workspace_file_list_request_id() -> str:
    return f"workspace_file_list_request:{uuid4()}"


def new_workspace_file_list_result_id() -> str:
    return f"workspace_file_list_result:{uuid4()}"


def new_workspace_text_file_read_request_id() -> str:
    return f"workspace_text_file_read_request:{uuid4()}"


def new_workspace_text_file_read_result_id() -> str:
    return f"workspace_text_file_read_result:{uuid4()}"


def new_workspace_markdown_summary_request_id() -> str:
    return f"workspace_markdown_summary_request:{uuid4()}"


def new_workspace_markdown_summary_result_id() -> str:
    return f"workspace_markdown_summary_result:{uuid4()}"


def new_workspace_read_violation_id() -> str:
    return f"workspace_read_violation:{uuid4()}"
