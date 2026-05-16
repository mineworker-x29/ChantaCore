from pathlib import Path


def test_execution_result_promotion_has_no_execution_or_canonical_writes() -> None:
    text = Path("src/chanta_core/execution/promotion.py").read_text(encoding="utf-8")

    forbidden = [
        "write_" + "memory",
        "save_memory_" + "entry",
        "update_" + "persona",
        "update_" + "overlay",
        "promote_to_" + "memory",
        "promote_to_" + "persona",
        "canonical_promotion_enabled" + "=True",
        "promoted" + "=True",
        "invoke_explicit_" + "skill(",
        "gate_explicit_" + "invocation(",
        "complete_" + "text",
        "complete_" + "json",
        "sub" + "process",
        "requ" + "ests",
        "ht" + "tpx",
        "so" + "cket",
        "connect_" + "mcp",
        "load_" + "plugin",
        "write_" + "text",
        "op" + "en(",
        "js" + "onl",
    ]
    for item in forbidden:
        assert item not in text


def test_execution_result_promotion_public_safe_surface() -> None:
    text = (
        Path("src/chanta_core/execution/promotion.py").read_text(encoding="utf-8")
        + Path("docs/versions/v0.18/chanta_core_v0_18_3_restore.md").read_text(encoding="utf-8")
    )

    assert "sample-secret" not in text
    assert "hidden-value" not in text
    assert "C:\\example" not in text
