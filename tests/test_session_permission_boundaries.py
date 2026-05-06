from pathlib import Path


def test_session_permission_read_model_boundary() -> None:
    source = Path("src/chanta_core/permissions/session.py").read_text(encoding="utf-8")
    forbidden = [
        "ToolDispatcher",
        "AgentRuntime.run",
        "block_tool",
        "mutate_tool_input",
        "mutate_tool_output",
        "subprocess",
        "os.system",
        "import requests",
        "from requests",
        "httpx",
        "socket",
        "complete_text",
        "complete_json",
        "llm",
        "classifier",
        "apply_grant",
        "auto_deny",
        "markdown_as_permission",
        "jsonl",
        "inherit_permissions",
        "restore_permissions",
    ]

    for token in forbidden:
        assert token not in source
    assert "enforcement_enabled" in source
    assert "PermissionModelService" in source
