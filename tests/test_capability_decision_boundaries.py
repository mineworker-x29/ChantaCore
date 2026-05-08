from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _capability_source() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            ROOT / "src/chanta_core/capabilities/decision_surface.py",
            ROOT / "src/chanta_core/capabilities/models.py",
            ROOT / "src/chanta_core/capabilities/history_adapter.py",
        ]
    )


def test_no_execution_or_external_access_in_capability_decision_surface() -> None:
    text = _capability_source()
    forbidden = [
        "ToolDispatcher",
        "Path.read_text",
        "open(",
        "subprocess",
        "requests",
        "httpx",
        "socket",
        "connect_mcp",
        "load_plugin",
        "apply_grant",
        "execution_enabled=True",
        "terminal" + "_scrollback",
    ]
    for term in forbidden:
        assert term not in text


def test_no_jsonl_or_llm_classifier_in_capability_decision_surface() -> None:
    text = _capability_source()
    assert "jsonl" not in text.casefold()
    assert "llm classifier" not in text.casefold()
    assert "uses_llm_classifier" in text
