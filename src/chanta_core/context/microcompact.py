from __future__ import annotations

import json
from typing import Any


def compact_lines(
    text: str,
    *,
    max_lines: int = 40,
    head_lines: int = 25,
    tail_lines: int = 10,
    marker: str = "...[lines omitted]...",
) -> tuple[str, bool]:
    lines = text.splitlines()
    if len(lines) <= max_lines:
        return text, False
    keep_head = max(0, head_lines)
    keep_tail = max(0, tail_lines)
    omitted = max(0, len(lines) - keep_head - keep_tail)
    compacted = (
        lines[:keep_head]
        + [marker.replace("]", f": {omitted} omitted]")]
        + (lines[-keep_tail:] if keep_tail else [])
    )
    return "\n".join(compacted), True


def compact_long_line(
    line: str,
    *,
    max_chars: int = 500,
    marker: str = "...[line truncated]...",
) -> tuple[str, bool]:
    if len(line) <= max_chars:
        return line, False
    if len(marker) >= max_chars:
        return marker[:max_chars], True
    return f"{line[: max_chars - len(marker)]}{marker}", True


def compact_activity_sequence(
    sequence: list[str],
    *,
    max_items: int = 30,
    head_items: int = 18,
    tail_items: int = 8,
) -> tuple[str, bool]:
    if len(sequence) <= max_items:
        return " -> ".join(sequence), False
    omitted = max(0, len(sequence) - head_items - tail_items)
    items = (
        [str(item) for item in sequence[:head_items]]
        + [f"...[{omitted} activities omitted]..."]
        + [str(item) for item in sequence[-tail_items:]]
    )
    return " -> ".join(items), True


def compact_mapping(
    mapping: dict[str, Any],
    *,
    max_items: int = 20,
) -> tuple[str, bool]:
    keys = sorted(mapping, key=lambda key: str(key))
    changed = len(keys) > max_items
    visible_keys = keys[:max_items]
    lines = [f"{key}: {_compact_value(mapping[key])}" for key in visible_keys]
    if changed:
        lines.append(f"...[{len(keys) - max_items} mapping item(s) omitted]...")
    return "\n".join(lines), changed


def compact_json_like_text(
    text: str,
    *,
    max_chars: int = 2000,
) -> tuple[str, bool]:
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return _compact_plain_text(text, max_chars=max_chars)

    rendered = _render_json_value(parsed)
    if len(rendered) > max_chars:
        rendered, _ = compact_long_line(rendered, max_chars=max_chars)
    return rendered, rendered != text


def compact_report_text(
    text: str,
    *,
    max_sections: int = 12,
    max_chars: int = 2500,
) -> tuple[str, bool]:
    sections = _split_sections(text)
    if not sections:
        return _cap_text(text, max_chars)

    changed = len(sections) > max_sections
    visible = sections[:max_sections]
    parts: list[str] = []
    for header, lines in visible:
        if header:
            parts.append(header)
        kept_lines = [line.rstrip() for line in lines[:6]]
        parts.extend(kept_lines)
        if len(lines) > len(kept_lines):
            parts.append(f"...[{len(lines) - len(kept_lines)} section line(s) omitted]...")
            changed = True
    if len(sections) > max_sections:
        parts.append(f"...[{len(sections) - max_sections} section(s) omitted]...")
    rendered = "\n".join(part for part in parts if part is not None).strip()
    capped, capped_changed = _cap_text(rendered, max_chars)
    return capped, changed or capped_changed or capped != text


def _compact_plain_text(text: str, *, max_chars: int) -> tuple[str, bool]:
    lines: list[str] = []
    changed = False
    for line in text.splitlines():
        compacted, line_changed = compact_long_line(line)
        lines.append(compacted.rstrip())
        changed = changed or line_changed or compacted != line
    rendered = "\n".join(_remove_repeated_blank_lines(lines)).strip()
    if rendered != text:
        changed = True
    rendered, lines_changed = compact_lines(rendered)
    capped, capped_changed = _cap_text(rendered, max_chars)
    return capped, changed or lines_changed or capped_changed


def _remove_repeated_blank_lines(lines: list[str]) -> list[str]:
    compacted: list[str] = []
    previous_blank = False
    for line in lines:
        is_blank = line == ""
        if is_blank and previous_blank:
            continue
        compacted.append(line)
        previous_blank = is_blank
    return compacted


def _render_json_value(value: Any) -> str:
    if isinstance(value, dict):
        rendered, _ = compact_mapping(value)
        return rendered
    if isinstance(value, list):
        lines = [f"- {_compact_value(item)}" for item in value[:20]]
        if len(value) > 20:
            lines.append(f"...[{len(value) - 20} list item(s) omitted]...")
        return "\n".join(lines)
    return _compact_value(value)


def _compact_value(value: Any) -> str:
    if isinstance(value, dict):
        return f"<dict keys={len(value)}>"
    if isinstance(value, list):
        return f"<list items={len(value)}>"
    rendered = repr(value)
    compacted, _ = compact_long_line(rendered, max_chars=160)
    return compacted


def _split_sections(text: str) -> list[tuple[str, list[str]]]:
    sections: list[tuple[str, list[str]]] = []
    current_header = ""
    current_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        is_header = (
            stripped.startswith("#")
            or (stripped.endswith(":") and len(stripped) <= 80)
        )
        if is_header:
            if current_header or current_lines:
                sections.append((current_header, current_lines))
            current_header = line.rstrip()
            current_lines = []
        else:
            current_lines.append(line.rstrip())
    if current_header or current_lines:
        sections.append((current_header, current_lines))
    return sections


def _cap_text(text: str, max_chars: int) -> tuple[str, bool]:
    return compact_long_line(text, max_chars=max_chars, marker="...[text truncated]...")
