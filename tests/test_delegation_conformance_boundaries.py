from pathlib import Path


CONFORMANCE_FILE = Path("src/chanta_core/delegation/conformance.py")


def test_delegation_conformance_has_no_active_runtime_execution_imports() -> None:
    conformance_text = CONFORMANCE_FILE.read_text(encoding="utf-8")
    forbidden = [
        "AgentRuntime",
        "run_child",
        "execute_subagent",
        "call_llm",
        "complete_text",
        "complete_json",
        "ToolDispatcher",
        "os.system",
        "requests",
        "httpx",
        "socket",
        "write_text",
        "load_mcp",
        "load_plugin",
        "auto_fix",
        "mutate_sidechain",
    ]

    for token in forbidden:
        assert token not in conformance_text


def test_delegation_conformance_records_boundaries_as_structural_only() -> None:
    conformance_text = CONFORMANCE_FILE.read_text(encoding="utf-8")

    assert "delegation_conformance_structural_only" in conformance_text
    assert "runtime_effect" in conformance_text
    assert "enforcement_enabled" in conformance_text
    assert "replace(" in conformance_text
    assert "contains_full_parent_transcript" in conformance_text
    assert "contains_full_child_transcript" in conformance_text
