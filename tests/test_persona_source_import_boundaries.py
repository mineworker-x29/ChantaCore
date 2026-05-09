from pathlib import Path


def test_persona_source_import_has_no_forbidden_runtime_behavior() -> None:
    source = Path("src/chanta_core/persona/source_import.py").read_text(encoding="utf-8")

    for forbidden in [
        "complete" + "_text",
        "complete" + "_json",
        "htt" + "px",
        "soc" + "ket",
        "sub" + "process",
        "os." + "system",
        "connect" + "_mcp",
        "load" + "_plugin",
        "overwrite" + "_persona",
        "self" + "_modify",
        "canonical_import_enabled" + "=True",
        "Soul.md" + " as canonical",
        "markdown_as" + "_persona_source",
    ]:
        assert forbidden not in source
    assert "canonical_import_enabled=False" in source
    assert "safe_read_text_file" in source


def test_public_tests_do_not_use_real_private_content() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            Path("tests/test_persona_source_import_models.py"),
            Path("tests/test_persona_source_import_service.py"),
            Path("tests/test_persona_source_import_discovery.py"),
            Path("tests/test_persona_source_import_validation.py"),
            Path("tests/test_persona_source_import_history_adapter.py"),
            Path("tests/test_persona_source_import_ocel_shape.py"),
            Path("tests/test_persona_source_import_boundaries.py"),
        ]
    )

    assert ("real_" + "private_persona_name") not in combined
    assert ("real_" + "private_directory_name") not in combined
    assert ("real_" + "private_letter_filename") not in combined

