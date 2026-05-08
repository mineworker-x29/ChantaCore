from pathlib import Path


def test_shell_network_pre_sandbox_source_has_no_forbidden_runtime_behavior() -> None:
    source = Path("src/chanta_core/sandbox/shell_network.py").read_text(encoding="utf-8")
    forbidden_patterns = [
        "subprocess",
        "os.system",
        "import requests",
        "from requests",
        "httpx",
        "socket",
        "getaddrinfo",
        "write_text",
        "open(",
        "unlink",
        "Path.mkdir",
        ".mkdir",
        "ToolDispatcher",
        "AgentRuntime.run",
        "block_tool",
        "mutate_tool_input",
        "mutate_tool_output",
        "sandbox_enforce",
        "complete_text",
        "complete_json",
        "classifier",
        "apply_grant",
        "auto_deny",
        "markdown_as_sandbox",
        "jsonl",
    ]

    for pattern in forbidden_patterns:
        assert pattern not in source
    assert "enforcement_enabled" in source
    assert "urlparse" in source
    assert "ipaddress" in source
