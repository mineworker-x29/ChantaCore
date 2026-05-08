from pathlib import Path


REVIEW_FILE = Path("src/chanta_core/external/review.py")
RUNTIME_FILES = [
    Path("src/chanta_core/runtime/agent_runtime.py"),
    Path("src/chanta_core/tools/dispatcher.py"),
    Path("src/chanta_core/skills/executor.py"),
]


def test_external_adapter_review_has_no_forbidden_runtime_calls() -> None:
    text = REVIEW_FILE.read_text(encoding="utf-8")
    forbidden = [
        "subprocess",
        "os.system",
        "requests",
        "httpx",
        "socket",
        "git clone",
        "pip install",
        "npm install",
        "importlib",
        "load_plugin",
        "connect_mcp",
        "MCPClient",
        "ToolDispatcher",
        "SkillExecutor",
        "AgentRuntime",
        "dispatch",
        "execute",
        "apply_grant",
        "create_permission_grant",
        "create_sandbox",
        "auto_enable",
        "execution_enabled=True",
        'activation_status="active"',
        "approve_and_activate",
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


def test_runtime_files_do_not_import_external_adapter_review_service() -> None:
    for path in RUNTIME_FILES:
        text = path.read_text(encoding="utf-8")
        assert "ExternalAdapterReviewService" not in text
        assert "external_adapter_review_queue" not in text
        assert "external_adapter_review_decision" not in text
