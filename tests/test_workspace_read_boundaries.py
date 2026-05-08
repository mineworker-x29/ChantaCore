from pathlib import Path


def test_workspace_read_boundary_source_has_no_forbidden_behavior() -> None:
    source_files = [
        Path("src/chanta_core/workspace/ids.py"),
        Path("src/chanta_core/workspace/models.py"),
        Path("src/chanta_core/workspace/read_service.py"),
        Path("src/chanta_core/workspace/history_adapter.py"),
        Path("src/chanta_core/skills/builtin/workspace_read.py"),
    ]
    source = "\n".join(path.read_text(encoding="utf-8") for path in source_files)
    forbidden = [
        "subprocess",
        "os.system",
        "requests",
        "httpx",
        "socket",
        "write_text",
        "open(",
        "unlink",
        "chmod",
        "mkdir",
        "rmdir",
        "rename",
        "connect_mcp",
        "load_plugin",
        "apply_grant",
        "jsonl",
        "shell fallback",
    ]

    for token in forbidden:
        assert token not in source
    assert "resolve(strict=False)" in source
    assert "relative_to" in source
    assert "read_bytes" in source
