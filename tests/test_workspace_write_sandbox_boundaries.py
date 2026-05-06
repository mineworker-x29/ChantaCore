from pathlib import Path


def test_workspace_write_sandbox_package_boundary() -> None:
    package_files = Path("src/chanta_core/sandbox").glob("*.py")
    source = "\n".join(path.read_text(encoding="utf-8") for path in package_files)
    forbidden = [
        "write_text",
        "open(",
        "unlink",
        "Path.mkdir",
        ".mkdir",
        "rmdir",
        "chmod",
        "rename",
        "ToolDispatcher",
        "AgentRuntime.run",
        "block_tool",
        "mutate_tool_input",
        "mutate_tool_output",
        "sandbox_enforce",
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
        "markdown_as_sandbox",
        "jsonl",
    ]

    for token in forbidden:
        assert token not in source
    assert "resolve(strict=False)" in source
    assert "relative_to" in source
    assert "enforcement_enabled" in source
