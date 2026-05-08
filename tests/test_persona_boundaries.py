from pathlib import Path


def test_persona_package_has_no_forbidden_runtime_behavior() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in Path("src/chanta_core/persona").glob("*.py")
    )
    forbidden = [
        "Soul.md as canonical",
        "markdown_as_persona_source",
        "self_modify",
        "mutate_persona",
        "ToolDispatcher",
        "subprocess",
        "requests",
        "httpx",
        "socket",
        "connect_mcp",
        "load_plugin",
        "jsonl",
        "reasoning_content",
    ]

    for token in forbidden:
        assert token not in source
    assert "prompt_projection_only" in source
    assert "executes_tools" in source
