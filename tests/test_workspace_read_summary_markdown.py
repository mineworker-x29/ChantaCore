from chanta_core.workspace.summary import WorkspaceReadSummarizationService


def test_markdown_headings_produce_sections() -> None:
    service = WorkspaceReadSummarizationService()

    result = service.summarize_markdown("# Title\n\nBody\n\n## Part\nText")

    assert result.status == "completed"
    assert result.summary_title == "Title"
    assert len(service.last_sections) == 2
    assert service.last_sections[0].section_type == "markdown_heading"
    assert "## Part" in result.summary_text
