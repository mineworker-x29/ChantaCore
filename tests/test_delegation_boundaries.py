from pathlib import Path


DELEGATION_DIR = Path("src/chanta_core/delegation")


def test_delegation_service_has_no_active_runtime_execution_imports() -> None:
    service_text = (DELEGATION_DIR / "service.py").read_text(encoding="utf-8")
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
        assert token not in service_text


def test_delegation_package_records_boundaries_as_data_only() -> None:
    service_text = (DELEGATION_DIR / "service.py").read_text(encoding="utf-8")
    models_text = (DELEGATION_DIR / "models.py").read_text(encoding="utf-8")

    assert "inherited_permissions=False" in service_text
    assert "contains_full_parent_transcript" in service_text
    assert "delegation_model_only" in service_text
    assert "sidechain_context" not in service_text
    assert "conformance" not in service_text.lower()
    assert "inherited_permissions must be False" in models_text
