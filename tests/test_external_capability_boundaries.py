from pathlib import Path


EXTERNAL_DIR = Path("src/chanta_core/external")
RUNTIME_FILES = [
    Path("src/chanta_core/runtime/agent_runtime.py"),
    Path("src/chanta_core/tools/dispatcher.py"),
    Path("src/chanta_core/skills/executor.py"),
]


def test_external_package_has_no_active_external_system_calls() -> None:
    text = "\n".join(path.read_text(encoding="utf-8") for path in EXTERNAL_DIR.glob("*.py"))
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
        "complete_text",
        "complete_json",
        "auto_enable",
        "execution_enabled=True",
        "markdown_as_external_source",
    ]
    for token in forbidden:
        assert token not in text


def test_runtime_files_do_not_import_external_capability_service() -> None:
    for path in RUNTIME_FILES:
        text = path.read_text(encoding="utf-8")
        assert "ExternalCapabilityImportService" not in text
        assert "external_assimilation_candidate" not in text
        assert "external_capability_descriptor" not in text


def test_external_capability_persistence_is_ocel_not_jsonl_or_markdown() -> None:
    text = "\n".join(path.read_text(encoding="utf-8") for path in EXTERNAL_DIR.glob("*.py"))
    assert "OCELRecord" in text
    assert "OCELObject" in text
    assert "jsonl" not in text.lower()
    assert "markdown" not in text.lower()
