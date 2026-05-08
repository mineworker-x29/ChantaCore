from pathlib import Path


def test_external_ocel_import_has_no_forbidden_runtime_behavior() -> None:
    source_text = Path("src/chanta_core/external/ocel_import.py").read_text(encoding="utf-8")

    forbidden = [
        "canonical_import_enabled=True",
        "merge_into_canonical",
        "import_into_ocel_store",
        "insert_external_events",
        "requests",
        "httpx",
        "socket",
        "subprocess",
        "os.system",
        "MCPClient",
        "connect_mcp",
        "load_plugin",
        "ToolDispatcher",
        "SkillExecutor",
        "AgentRuntime",
        "execution_enabled=True",
        "jsonl",
    ]

    for item in forbidden:
        assert item not in source_text


def test_external_ocel_import_does_not_read_files_or_fetch_urls() -> None:
    source_text = Path("src/chanta_core/external/ocel_import.py").read_text(encoding="utf-8")

    for item in [".read_text(", ".read_bytes(", "open(", "urlopen", "Path("]:
        assert item not in source_text
