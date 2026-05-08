from pathlib import Path


MCP_PLUGIN_FILE = Path("src/chanta_core/external/mcp_plugin.py")
RUNTIME_FILES = [
    Path("src/chanta_core/runtime/agent_runtime.py"),
    Path("src/chanta_core/tools/dispatcher.py"),
    Path("src/chanta_core/skills/executor.py"),
]


def test_mcp_plugin_descriptor_has_no_forbidden_runtime_calls() -> None:
    text = MCP_PLUGIN_FILE.read_text(encoding="utf-8")
    forbidden = [
        "subprocess",
        "os.system",
        "requests",
        "httpx",
        "socket",
        "getaddrinfo",
        "importlib",
        "load_plugin",
        "connect_mcp",
        "MCPClient",
        "tools/list",
        "call_tool",
        "ToolDispatcher",
        "SkillExecutor",
        "AgentRuntime",
        "dispatch",
        "execute",
        "apply_grant",
        "create_permission_grant",
        "create_sandbox",
        "create_review_decision",
        "auto_enable",
        "execution_enabled=True",
        'activation_status="active"',
        "sync_markdown",
        "import_from_markdown",
        "complete_text",
        "complete_json",
        "llm",
        "classifier",
        "jsonl",
    ]
    for token in forbidden:
        assert token not in text


def test_runtime_files_do_not_import_mcp_plugin_descriptor_service() -> None:
    for path in RUNTIME_FILES:
        text = path.read_text(encoding="utf-8")
        assert "MCPPluginDescriptorSkeletonService" not in text
        assert "mcp_server_descriptor" not in text
        assert "plugin_descriptor" not in text
        assert "external_descriptor_skeleton" not in text
