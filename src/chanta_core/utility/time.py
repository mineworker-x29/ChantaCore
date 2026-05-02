from __future__ import annotations

from datetime import UTC, datetime


def utc_now_iso() -> str:
    """Return a timezone-aware UTC timestamp formatted with a trailing Z."""
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")
