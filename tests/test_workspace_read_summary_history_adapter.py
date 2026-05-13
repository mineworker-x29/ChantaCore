from chanta_core.workspace.summary_history_adapter import (
    workspace_read_summary_candidates_to_history_entries,
    workspace_read_summary_findings_to_history_entries,
    workspace_read_summary_requests_to_history_entries,
    workspace_read_summary_results_to_history_entries,
)
from chanta_core.workspace.summary import WorkspaceReadSummarizationService


def test_workspace_read_summary_history_entries() -> None:
    service = WorkspaceReadSummarizationService()
    result = service.summarize_from_text(text="abcdef", input_kind="text")
    candidate = service.create_summary_candidate(result=result)

    assert workspace_read_summary_requests_to_history_entries([service.last_request])[0].source == "workspace_read_summary"
    assert workspace_read_summary_results_to_history_entries([result])[0].source == "workspace_read_summary"
    assert workspace_read_summary_candidates_to_history_entries([candidate])[0].source == "workspace_read_summary"
    assert workspace_read_summary_findings_to_history_entries(service.last_findings) == []
