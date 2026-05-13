from chanta_core.workspace.summary import WorkspaceReadSummarizationService


def test_python_ast_symbol_preview() -> None:
    service = WorkspaceReadSummarizationService()

    result = service.summarize_python('"""Module doc."""\nimport os\nfrom pathlib import Path\nclass Demo:\n    pass\ndef run():\n    return 1\n')

    assert "os" in result.summary_text
    assert "pathlib" in result.summary_text
    assert "Demo" in result.summary_text
    assert "run" in result.summary_text
