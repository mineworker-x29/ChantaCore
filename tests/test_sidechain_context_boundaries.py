from pathlib import Path


SIDECHAIN_FILE = Path("src/chanta_core/delegation/sidechain.py")


def test_sidechain_context_has_no_active_runtime_execution_imports() -> None:
    sidechain_text = SIDECHAIN_FILE.read_text(encoding="utf-8")
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
    ]

    for token in forbidden:
        assert token not in sidechain_text


def test_sidechain_context_records_boundaries_as_data_only() -> None:
    sidechain_text = SIDECHAIN_FILE.read_text(encoding="utf-8")

    assert "contains_full_parent_transcript=False" in sidechain_text
    assert "contains_full_child_transcript=False" in sidechain_text
    assert "inherited_permissions=False" in sidechain_text
    assert "sidechain_context_model_only" in sidechain_text
    assert "PIGConformance" not in sidechain_text
    assert "record_return_envelope" in sidechain_text
    assert "TraceService" in sidechain_text
