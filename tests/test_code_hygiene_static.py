from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "chanta_core"


def source_text() -> str:
    parts: list[str] = []
    for path in SRC.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        parts.append(path.read_text(encoding="utf-8"))
    return "\n".join(parts)


def test_no_local_naive_datetime_helpers() -> None:
    offenders = []
    for path in SRC.rglob("*.py"):
        if path.as_posix().endswith("utility/time.py"):
            continue
        text = path.read_text(encoding="utf-8")
        if "datetime.utcnow" in text or "datetime.now(" in text:
            offenders.append(str(path.relative_to(ROOT)))
    assert offenders == []


def test_no_retired_pig_names_or_forbidden_directories() -> None:
    text = source_text()

    assert "PIGGraphBuilder" not in text
    assert "PIGGuideService" not in text
    assert not (SRC / "process_intelligence").exists()
    assert not (SRC / "pi").exists()
    assert not (SRC / "intelligence").exists()


def test_ocel_canonical_constructor_names() -> None:
    text = source_text()

    assert "OCELEvent(event_type=" not in text
    assert "OCELObject(object_key=" not in text
    assert "OCELObject(display_name=" not in text
