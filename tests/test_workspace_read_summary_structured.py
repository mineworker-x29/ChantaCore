from chanta_core.workspace.summary import WorkspaceReadSummarizationService


def test_json_yaml_toml_shallow_summaries() -> None:
    service = WorkspaceReadSummarizationService()

    json_result = service.summarize_json('{"name": "demo", "count": 2, "items": [1, 2]}')
    assert "name:str" in json_result.summary_text
    assert "items:list" in json_result.summary_text

    yaml_result = service.summarize_yaml("name: demo\ncount: 2\nitems:\n  - one\n")
    assert "name" in yaml_result.summary_text
    assert "count" in yaml_result.summary_text

    toml_result = service.summarize_toml('name = "demo"\ncount = 2\n[tool]\nkind = "test"\n')
    assert "name" in toml_result.summary_text
    assert "tool" in toml_result.summary_text
