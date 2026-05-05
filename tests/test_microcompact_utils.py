from chanta_core.context import (
    compact_activity_sequence,
    compact_json_like_text,
    compact_lines,
    compact_long_line,
    compact_mapping,
    compact_report_text,
)


def test_compact_lines_unchanged_when_short() -> None:
    text = "a\nb\nc"

    compacted, changed = compact_lines(text, max_lines=5)

    assert compacted == text
    assert changed is False


def test_compact_lines_preserves_head_and_tail() -> None:
    text = "\n".join(f"line-{index}" for index in range(10))

    compacted, changed = compact_lines(
        text,
        max_lines=5,
        head_lines=2,
        tail_lines=2,
    )

    assert changed is True
    assert "line-0" in compacted
    assert "line-9" in compacted
    assert "6 omitted" in compacted
    assert "line-5" not in compacted


def test_compact_long_line_truncates_deterministically() -> None:
    line = "x" * 100

    compacted_a, changed_a = compact_long_line(line, max_chars=30)
    compacted_b, changed_b = compact_long_line(line, max_chars=30)

    assert changed_a is True
    assert changed_b is True
    assert compacted_a == compacted_b
    assert len(compacted_a) == 30


def test_compact_activity_sequence_head_tail_behavior() -> None:
    sequence = [f"a{index}" for index in range(12)]

    compacted, changed = compact_activity_sequence(
        sequence,
        max_items=6,
        head_items=3,
        tail_items=2,
    )

    assert changed is True
    assert compacted.startswith("a0 -> a1 -> a2")
    assert compacted.endswith("a10 -> a11")
    assert "7 activities omitted" in compacted


def test_compact_mapping_sorts_keys() -> None:
    compacted, changed = compact_mapping({"b": 2, "a": 1, "c": 3}, max_items=2)

    assert changed is True
    assert compacted.splitlines()[0].startswith("a:")
    assert "1 mapping item" in compacted


def test_compact_json_like_text_valid_json() -> None:
    compacted, changed = compact_json_like_text('{"z": [1, 2], "a": {"nested": true}}')

    assert changed is True
    assert compacted.splitlines()[0].startswith("a:")
    assert "<dict keys=1>" in compacted


def test_compact_json_like_text_fallback_invalid_json() -> None:
    compacted, changed = compact_json_like_text("x" * 700, max_chars=200)

    assert changed is True
    assert len(compacted) <= 200


def test_compact_report_text_preserves_section_headers() -> None:
    text = "\n".join(
        ["# Section A"] + [f"a-{index}" for index in range(10)] + ["# Section B", "b-1"]
    )

    compacted, changed = compact_report_text(text, max_chars=500)

    assert changed is True
    assert "# Section A" in compacted
    assert "# Section B" in compacted
    assert "section line" in compacted
