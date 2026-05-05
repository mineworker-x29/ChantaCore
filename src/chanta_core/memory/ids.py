from __future__ import annotations

from uuid import uuid4


def new_memory_entry_id() -> str:
    return f"memory:{uuid4()}"


def new_memory_revision_id() -> str:
    return f"memory_revision:{uuid4()}"
