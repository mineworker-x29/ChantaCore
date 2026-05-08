from pathlib import Path


SOURCE_FILES = [
    Path("src/chanta_core/runtime/capability_contract.py"),
    Path("src/chanta_core/agents/default_agent.py"),
    Path("src/chanta_core/cli/main.py"),
]


def test_default_agent_capability_contract_adds_no_active_execution_paths() -> None:
    source_text = "\n".join(path.read_text(encoding="utf-8") for path in SOURCE_FILES)

    forbidden_identifiers = [
        "subprocess",
        "os.system",
        "requests",
        "httpx",
        "socket",
        "importlib",
        "ToolDispatcher",
        "SkillExecutor",
        "apply_grant",
        "create_permission_grant",
        "execution_enabled=True",
        "connect_mcp",
        "load_plugin",
        "reasoning_content",
        "jsonl",
    ]

    for identifier in forbidden_identifiers:
        assert identifier not in source_text


def test_default_agent_capability_contract_adds_no_workspace_read_skill() -> None:
    source_text = Path("src/chanta_core/runtime/capability_contract.py").read_text(
        encoding="utf-8"
    )

    forbidden_calls = [
        ".read_text(",
        ".read_bytes(",
        "open(",
        "Path(",
        "glob(",
        "rglob(",
    ]

    for call in forbidden_calls:
        assert call not in source_text
