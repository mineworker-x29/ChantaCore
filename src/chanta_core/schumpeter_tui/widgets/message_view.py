"""Message card view contract for the Schumpeter transcript."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from chanta_core.schumpeter_tui.display_width import display_width_v0439, pad_to_display_width_v0439


MESSAGE_CARD_KINDS = ("user", "assistant", "status", "artifact", "diagnostic", "error", "system_notice")

RAW_METADATA_PREFIXES = (
    "type:",
    "grounding:",
    "confidence:",
    "verification_required:",
    "source:",
    "provider_invoked=",
    "prompt_submitted=",
    "shell_executed=",
    "workspace_mutated=",
    "memory_mutated=",
    "production_certified=",
)

RAW_SAFETY_MARKERS = ("shell=", "subagent=", "workspace", "memory", "production_certified")


@dataclass(frozen=True)
class V043117MessageCardStyle:
    kind: str
    title: str
    css_classes: tuple[str, ...]
    border_color: str
    accent_color: str
    horizontal_glyph: str
    indent_columns: int
    production_certified: bool


@dataclass(frozen=True)
class V043117MessageCard:
    kind: str
    title: str
    body: str
    css_classes: tuple[str, ...]
    rendered_text: str
    width: int
    raw_metadata_visible: bool
    debug_surface: bool
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    git_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    memory_mutated: bool
    core_memory_written: bool
    production_certified: bool


MESSAGE_CARD_STYLES: dict[str, V043117MessageCardStyle] = {
    "user": V043117MessageCardStyle("user", "You", ("message-card", "user"), "#5fb3ff", "#5fb3ff", "-", 2, False),
    "assistant": V043117MessageCardStyle(
        "assistant",
        "Schumpeter",
        ("message-card", "assistant"),
        "#6ee7b7",
        "#6ee7b7",
        "=",
        0,
        False,
    ),
    "status": V043117MessageCardStyle("status", "Status", ("message-card", "status"), "#d6b85f", "#d6b85f", "-", 0, False),
    "artifact": V043117MessageCardStyle(
        "artifact",
        "Summary",
        ("message-card", "artifact"),
        "#c9d1d9",
        "#8b949e",
        "-",
        0,
        False,
    ),
    "diagnostic": V043117MessageCardStyle(
        "diagnostic",
        "Diagnostic",
        ("message-card", "diagnostic"),
        "#a5b4fc",
        "#a5b4fc",
        "-",
        0,
        False,
    ),
    "error": V043117MessageCardStyle(
        "error",
        "Unavailable",
        ("message-card", "error"),
        "#f2a272",
        "#f2a272",
        "-",
        0,
        False,
    ),
    "system_notice": V043117MessageCardStyle(
        "system_notice",
        "Notice",
        ("message-card", "system-notice"),
        "#8b949e",
        "#8b949e",
        "-",
        0,
        False,
    ),
}


def message_label(kind: str) -> str:
    return MESSAGE_CARD_STYLES.get(kind, MESSAGE_CARD_STYLES["assistant"]).title


def normalize_message_card_kind(kind: str | None) -> str:
    value = str(kind or "assistant").strip().lower()
    return value if value in MESSAGE_CARD_STYLES else "assistant"


def message_card_style(kind: str | None) -> V043117MessageCardStyle:
    return MESSAGE_CARD_STYLES[normalize_message_card_kind(kind)]


def _is_raw_metadata_line(line: str) -> bool:
    lowered = line.strip().lower()
    if any(lowered.startswith(prefix) for prefix in RAW_METADATA_PREFIXES):
        return True
    if lowered.startswith("safety:"):
        return any(marker in lowered for marker in RAW_SAFETY_MARKERS)
    return False


def sanitize_message_body(text: str, debug_surface: bool = False) -> str:
    if debug_surface:
        return str(text)
    lines = [line.rstrip() for line in str(text).splitlines()]
    visible = [line for line in lines if not _is_raw_metadata_line(line)]
    return "\n".join(visible).strip()


def _wrap_display_line(line: str, width: int) -> tuple[str, ...]:
    target = max(8, int(width))
    if not line:
        return ("",)
    words = line.split(" ")
    if len(words) > 1:
        rows: list[str] = []
        current = ""
        for word in words:
            candidate = word if not current else f"{current} {word}"
            if display_width_v0439(candidate) <= target:
                current = candidate
                continue
            if current:
                rows.append(current)
            if display_width_v0439(word) <= target:
                current = word
            else:
                rows.extend(_wrap_unspaced_text(word, target))
                current = ""
        if current:
            rows.append(current)
        return tuple(rows) or ("",)
    return tuple(_wrap_unspaced_text(line, target))


def _wrap_unspaced_text(text: str, width: int) -> list[str]:
    rows: list[str] = []
    current = ""
    for char in text:
        candidate = current + char
        if current and display_width_v0439(candidate) > width:
            rows.append(current)
            current = char
        else:
            current = candidate
    if current:
        rows.append(current)
    return rows or [""]


def wrap_message_body(text: str, width: int) -> tuple[str, ...]:
    rows: list[str] = []
    for line in str(text).splitlines() or [""]:
        rows.extend(_wrap_display_line(line, width))
    return tuple(rows) or ("",)


def render_v043117_card_text(
    text: str,
    kind: str = "assistant",
    width: int = 78,
    title: str | None = None,
    debug_surface: bool = False,
) -> str:
    style = message_card_style(kind)
    card_width = max(24, int(width) - style.indent_columns)
    inner_width = max(18, card_width - 2)
    body = sanitize_message_body(text, debug_surface=debug_surface)
    wrapped = wrap_message_body(body, inner_width)
    indent = " " * style.indent_columns
    header = f"{title or style.title} [{style.kind}]"
    body_lines = [pad_to_display_width_v0439(f"  {line}", inner_width) for line in wrapped]
    return "\n".join(f"{indent}{line}" for line in (header, *body_lines))


def create_v043117_message_card(
    text: str,
    kind: str = "assistant",
    width: int = 78,
    title: str | None = None,
    debug_surface: bool = False,
    **overrides: Any,
) -> V043117MessageCard:
    style = message_card_style(kind)
    sanitized = sanitize_message_body(text, debug_surface=debug_surface)
    rendered = render_v043117_card_text(sanitized, style.kind, width, title or style.title, debug_surface=debug_surface)
    defaults = {
        "kind": style.kind,
        "title": title or style.title,
        "body": sanitized,
        "css_classes": style.css_classes,
        "rendered_text": rendered,
        "width": int(width),
        "raw_metadata_visible": bool(debug_surface),
        "debug_surface": bool(debug_surface),
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "git_executed": False,
        "repo_search_used": False,
        "workspace_read_opened": False,
        "memory_mutated": False,
        "core_memory_written": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V043117MessageCard(**defaults)


def render_v043117_transcript_cards(
    messages: Sequence[Any],
    width: int = 78,
    include_system_notices: bool = False,
    debug_surface: bool = False,
) -> str:
    rendered: list[str] = []
    for message in messages:
        kind = normalize_message_card_kind(getattr(message, "kind", "assistant"))
        if kind == "system_notice" and not include_system_notices:
            continue
        card = create_v043117_message_card(
            getattr(message, "text", ""),
            kind=kind,
            width=width,
            title=message_label(kind),
            debug_surface=debug_surface,
        )
        rendered.append(card.rendered_text)
    return "\n\n".join(rendered)


class MessageView:
    card_kind = "assistant"

    def __init__(self, text: str = "", width: int = 78, debug_surface: bool = False):
        self.card = create_v043117_message_card(text, self.card_kind, width, debug_surface=debug_surface)
        self.css_classes = self.card.css_classes
        self.rendered_text = self.card.rendered_text


class UserMessageView(MessageView):
    card_kind = "user"


class AssistantMessageView(MessageView):
    card_kind = "assistant"


class StatusCardView(MessageView):
    card_kind = "status"


class ArtifactCardView(MessageView):
    card_kind = "artifact"


class DiagnosticCardView(MessageView):
    card_kind = "diagnostic"


class ErrorCardView(MessageView):
    card_kind = "error"


__all__ = [
    "ArtifactCardView",
    "AssistantMessageView",
    "DiagnosticCardView",
    "ErrorCardView",
    "MESSAGE_CARD_KINDS",
    "MESSAGE_CARD_STYLES",
    "MessageView",
    "RAW_METADATA_PREFIXES",
    "StatusCardView",
    "UserMessageView",
    "V043117MessageCard",
    "V043117MessageCardStyle",
    "create_v043117_message_card",
    "message_card_style",
    "message_label",
    "normalize_message_card_kind",
    "render_v043117_card_text",
    "render_v043117_transcript_cards",
    "sanitize_message_body",
    "wrap_message_body",
]
