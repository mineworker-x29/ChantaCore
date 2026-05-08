from pathlib import Path


VIEWS_FILE = Path("src/chanta_core/external/views.py")
RUNTIME_FILES = [
    Path("src/chanta_core/runtime/agent_runtime.py"),
    Path("src/chanta_core/tools/dispatcher.py"),
    Path("src/chanta_core/skills/executor.py"),
]


def test_external_view_file_has_no_external_system_calls_or_review_lifecycle() -> None:
    text = VIEWS_FILE.read_text(encoding="utf-8")
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
        "apply_grant",
        "auto_enable",
        "execution_enabled=True",
        "approve_candidate",
        "reject_candidate",
        "review_decision",
        "sync_markdown",
        "import_from_markdown",
        "jsonl",
        "markdown_as_external_source",
    ]
    for token in forbidden:
        assert token not in text


def test_runtime_files_do_not_integrate_external_registry_views() -> None:
    for path in RUNTIME_FILES:
        text = path.read_text(encoding="utf-8")
        assert "ExternalCapabilityRegistryViewService" not in text
        assert "external_capability_registry_snapshot" not in text
        assert "EXTERNAL_CAPABILITIES" not in text


def test_external_views_make_markdown_non_canonical() -> None:
    text = VIEWS_FILE.read_text(encoding="utf-8")
    assert "canonical=False" in text
    assert "source_kind=\"ocel_materialized_projection\"" in text
    assert "read_text" not in text
