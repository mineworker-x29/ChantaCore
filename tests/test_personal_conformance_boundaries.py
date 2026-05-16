from pathlib import Path

from chanta_core.persona.personal_conformance import PersonalConformanceService


def test_personal_conformance_public_files_do_not_contain_forbidden_terms() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "src" / "chanta_core" / "persona" / "personal_conformance.py",
        root / "tests" / "test_personal_conformance_models.py",
        root / "tests" / "test_personal_conformance_service.py",
        root / "tests" / "test_personal_conformance_history_adapter.py",
        root / "tests" / "test_personal_conformance_ocel_shape.py",
        root / "tests" / "test_personal_conformance_boundaries.py",
        root / "docs" / "versions" / "v0.16" / "chanta_core_v0_16_4_restore.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in paths)

    forbidden_fragments = [
        "message_to_" + "future",
        "message_to_" + "user",
        "complete_" + "text",
        "complete_" + "json",
        "Tool" + "Dispatcher",
        "sub" + "process",
        "req" + "uests",
        "ht" + "tpx",
        "so" + "cket",
        "connect_" + "mcp",
        "load_" + "plugin",
        "js" + "onl",
    ]

    assert not any(fragment in text for fragment in forbidden_fragments)
    assert "auto_" + "fix" not in text
    assert "mutate_" + "persona" not in text
    assert "mutate_" + "overlay" not in text


def test_conformance_does_not_mutate_checked_objects() -> None:
    service = PersonalConformanceService()
    candidate = type(
        "DummyCandidate",
        (),
        {
            "candidate_id": "candidate:test",
            "canonical_import_enabled": False,
        },
    )()
    before = dict(candidate.__dict__)

    service.evaluate_personal_source_conformance(candidate=candidate, sources=[])

    assert candidate.__dict__ == before
