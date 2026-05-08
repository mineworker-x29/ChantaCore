from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _source_text() -> str:
    paths = [
        ROOT / "src/chanta_core/session/context_assembler.py",
        ROOT / "src/chanta_core/session/prompt_renderer.py",
        ROOT / "src/chanta_core/runtime/agent_runtime.py",
        ROOT / "src/chanta_core/skills/builtin/llm_chat.py",
    ]
    return "\n".join(path.read_text(encoding="utf-8") for path in paths)


def test_no_canonical_jsonl_transcript_or_scrollback_source() -> None:
    text = _source_text()
    forbidden = [
        "session.jsonl",
        "chat_history.jsonl",
        "conversation.jsonl",
        "terminal" + "_scrollback",
    ]
    for term in forbidden:
        assert term not in text


def test_no_workspace_shell_network_or_runtime_tool_execution_added() -> None:
    text = _source_text()
    forbidden = [
        "read_workspace",
        ".read_text(",
        "subprocess",
        "requests",
        "httpx",
        "socket",
        "connect_mcp",
        "load_plugin",
        "ToolDispatcher",
        "execution_enabled=True",
    ]
    for term in forbidden:
        assert term not in text


def test_reasoning_content_is_not_emitted_as_assistant_output() -> None:
    text = _source_text()
    assert "content = str(item.get(\"content\") or \"\")" in text
    assert ".get(\"reasoning_content\")" not in text
