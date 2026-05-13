from pathlib import Path


def test_execution_audit_does_not_execute_or_grant_or_promote() -> None:
    text = Path("src/chanta_core/execution/audit.py").read_text(encoding="utf-8")

    forbidden = [
        "invoke_explicit_" + "skill(",
        "gate_explicit_" + "invocation(",
        "bridge_reviewed_" + "proposal(",
        "create_permission_" + "grant",
        "promote_to_" + "memory",
        "promote_to_" + "persona",
        "complete_" + "text",
        "complete_" + "json",
        "sub" + "process",
        "os." + "system",
        "import " + "requ" + "ests",
        "from " + "requ" + "ests",
        "import " + "ht" + "tpx",
        "from " + "ht" + "tpx",
        "import " + "so" + "cket",
        "from " + "so" + "cket",
        "connect_" + "mcp",
        "load_" + "plugin",
        "write_" + "text",
        "op" + "en(",
        "js" + "onl",
    ]
    for item in forbidden:
        assert item not in text


def test_execution_audit_public_safe_dummy_values_only() -> None:
    text = (
        Path("src/chanta_core/execution/audit.py").read_text(encoding="utf-8")
        + Path("docs/chanta_core_v0_18_2_restore.md").read_text(encoding="utf-8")
    )

    assert "C:\\example\\workspace" not in text
    assert "sample-token" not in text
    assert "sample-secret" not in text
