from __future__ import annotations

import re


SENSITIVE_KEYS = (
    "API_KEY",
    "SECRET",
    "TOKEN",
    "PASSWORD",
    "PRIVATE_KEY",
    "ACCESS_KEY",
)


def redact_sensitive_text(text: str) -> str:
    redacted = _redact_private_key_blocks(text)
    redacted = re.sub(
        r"Bearer\s+[A-Za-z0-9._~+/=-]+",
        "Bearer [REDACTED]",
        redacted,
    )
    lines = []
    for line in redacted.splitlines():
        upper = line.upper()
        if any(key in upper for key in SENSITIVE_KEYS):
            lines.append(_redact_assignment_line(line))
        else:
            lines.append(_redact_long_token_line(line))
    return "\n".join(lines)


def make_preview(text: str, max_chars: int, redact: bool = True) -> str:
    content = redact_sensitive_text(text) if redact else text
    marker = "...[preview truncated]..."
    if len(content) <= max_chars:
        return content
    if len(marker) >= max_chars:
        return marker[:max_chars]
    return f"{content[: max_chars - len(marker)]}{marker}"


def _redact_private_key_blocks(text: str) -> str:
    pattern = re.compile(
        r"-----BEGIN [^-]*PRIVATE KEY-----.*?-----END [^-]*PRIVATE KEY-----",
        re.DOTALL,
    )
    return pattern.sub("[REDACTED PRIVATE KEY]", text)


def _redact_assignment_line(line: str) -> str:
    key_pattern = "|".join(re.escape(key) for key in SENSITIVE_KEYS)
    redacted = re.sub(
        rf"\b({key_pattern}[A-Z0-9_]*)(\s*[:=]\s*)(\S+)",
        lambda match: f"{match.group(1)}{match.group(2)}[REDACTED]",
        line,
        flags=re.IGNORECASE,
    )
    if redacted != line:
        return redacted
    return "[REDACTED SENSITIVE LINE]"


def _redact_long_token_line(line: str) -> str:
    return re.sub(
        r"\b[A-Za-z0-9+/=_-]{32,}\b",
        "[REDACTED TOKEN]",
        line,
    )
