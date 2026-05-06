from pathlib import Path


def test_process_outcomes_package_has_no_forbidden_runtime_behavior() -> None:
    package_root = Path("src/chanta_core/outcomes")
    text = "\n".join(path.read_text(encoding="utf-8") for path in package_root.glob("*.py"))
    forbidden = [
        "subprocess",
        "os.system",
        "requests",
        "httpx",
        "socket",
        "complete_text",
        "complete_json",
        "llm",
        "PermissionGrant",
        "sandbox",
        "block_tool",
        "mutate_tool_input",
        "mutate_tool_output",
        "retry",
        "replan",
        "promote_memory",
        "policy_update",
        "embedding",
        "vector",
        "load_mcp",
        "load_plugin",
    ]
    assert {item for item in forbidden if item in text} == set()
