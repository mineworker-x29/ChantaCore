from pathlib import Path


def test_permissions_package_has_no_runtime_gate_or_external_surfaces() -> None:
    package_root = Path("src/chanta_core/permissions")
    text = "\n".join(path.read_text(encoding="utf-8") for path in package_root.glob("*.py"))
    forbidden = [
        "ToolDispatcher",
        "dispatch",
        "block_tool",
        "mutate_tool_input",
        "mutate_tool_output",
        "sandbox",
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
        "open(",
        "write_text",
    ]
    assert {item for item in forbidden if item in text} == set()
