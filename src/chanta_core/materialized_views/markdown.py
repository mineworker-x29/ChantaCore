from __future__ import annotations

from typing import Any


def markdown_heading(text: str, level: int = 1) -> str:
    normalized = max(1, min(level, 6))
    return f"{'#' * normalized} {text.strip()}"


def markdown_bullet(key: str, value: Any) -> str:
    rendered = "none" if value is None else str(value)
    return f"- **{key}:** {rendered}"


def markdown_code_block(text: str, language: str = "") -> str:
    return f"```{language}\n{text.rstrip()}\n```"


def render_generated_warning(*, view_type: str) -> str:
    return "\n".join(
        [
            "> Generated materialized view.",
            "> Canonical source: OCEL.",
            "> This file is not canonical memory.",
            "> Do not treat edits to this file as canonical updates.",
            f"> View type: {view_type}.",
        ]
    )


def render_view_metadata_block(
    *,
    view_id: str,
    view_type: str,
    target_path: str,
    generated_at: str,
    content_hash: str,
    source_kind: str,
    canonical: bool,
) -> str:
    return "\n".join(
        [
            markdown_heading("View Metadata", 2),
            markdown_bullet("view_id", view_id),
            markdown_bullet("view_type", view_type),
            markdown_bullet("target_path", target_path),
            markdown_bullet("generated_at", generated_at),
            markdown_bullet("content_hash", content_hash),
            markdown_bullet("source_kind", source_kind),
            markdown_bullet("canonical", canonical),
        ]
    )
